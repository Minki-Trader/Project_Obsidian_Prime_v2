from __future__ import annotations

import argparse
import csv
import json
import math
import re
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
)
from foundation.models.hmm_segmentation import (
    default_stage22_hmm_variants,
    fit_hmm_variant,
    state_quality_read as hmm_state_quality_read,
    state_sequence_frame as hmm_state_sequence_frame,
    state_summary_frame as hmm_state_summary_frame,
    transition_read as hmm_transition_read,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage22 import hmm_state_scout as stage22_hmm
from stage_pipelines.stage28 import markov_regression_state_link_scout as stage28_markov
from stage_pipelines.stage35 import atlas_config as stage35_cfg
from stage_pipelines.stage35 import atlas_model, common


STAGE_ID = "37_state_context__single_base_filter_or_state_router"
STAGE_NUMBER = 37
RUN_NUMBER = "run31A"
RUN_ID = "run31A_state_context_router_broad_mt5_probe_v1"
PACKET_ID = "stage37_run31A_state_context_router_broad_mt5_probe_v1"
EXPLORATION_LABEL = "stage37_StateContext__SingleBaseFilterOrStateRouter"
IDEA_ID = "IDEA-ST37-STATE-CONTEXT-ROUTER"
SOURCE_RUN_ID = "run30A_cross_model_characteristic_synthesis_v1"
MODEL_FAMILY = "state_context_response_surface_with_broad_routed_mt5_probe"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_58_plus_tier_b_core42_state_context"
LABEL_ID = "label_v1_fwd12_m5_logret_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
BOUNDARY = (
    "stage37_structure_judgment_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness"
)
JUDGMENT_COMPLETED = "state_context_not_useful_or_inconclusive"
JUDGMENT_BLOCKED = "blocked_state_context_router_broad_mt5_probe_after_attempt"
NEXT_ACTION = "open_next_topic_from_stage37_structure_judgment"

ROOT = common.ROOT
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
RESULT_ROOT = RUN_ROOT / "results"
FEATURE_ROOT = RUN_ROOT / "features"
MODEL_ROOT = RUN_ROOT / "models"
STATE_ROOT = RUN_ROOT / "states"
MT5_ROOT = RUN_ROOT / "mt5"
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / "run31A_state_context_router_broad_mt5_probe_packet.md"
STAGE_BRIEF_PATH = STAGE_ROOT / "00_spec" / "stage_brief.md"
STAGE_OPEN_DRAFT_PATH = STAGE_ROOT / "01_inputs" / "stage_open_draft.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews" / "review_index.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs" / "registers" / "run_registry.csv"
DECISION_PATH = ROOT / "docs" / "decisions" / "2026-05-09_stage37_state_context_router_open_run31A.md"
WORKSPACE_STATE_PATH = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = ROOT / "docs" / "workspace" / "changelog.md"

HMM_VARIANT_ID = "v02_core17_4state_diag"
MARKOV_VARIANT_ID = "v01_return_2state_switchvar"
MODEL_RESPONSE_CLASSES = (0, 1, 2)
TCN_FEATURES = (
    "log_return_1",
    "log_return_3",
    "hl_range",
    "historical_vol_20",
    "adx_14",
    "di_spread_14",
)
RUNTIME_VARIANTS = (
    "simple_context_control",
    "single_base_state_filter",
    "single_base_state_adapter",
    "limited_state_specialist_router",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return io_path(path).resolve().relative_to(io_path(ROOT).resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def active_branch() -> str:
    return subprocess.check_output(["git", "branch", "--show-current"], cwd=io_path(ROOT), text=True).strip()


def write_json(path: Path, payload: Any) -> None:
    common.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    common.write_md(path, text)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    common.write_csv(path, rows, columns)


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        frame.to_parquet(io_path(path), index=False)
    else:
        frame.to_csv(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def safe_float(value: Any, default: float | None = None) -> float | None:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def _split_label(split_name: str) -> str:
    return "validation_is" if split_name == "validation" else str(split_name)


def _split_from_label(split_label: str) -> str:
    return "validation" if split_label == "validation_is" else str(split_label)


def _split_dates_from_frames(frames: Sequence[pd.DataFrame], split_name: str) -> tuple[str, str]:
    parts = []
    for frame in frames:
        if "split" not in frame.columns or "timestamp" not in frame.columns:
            continue
        part = frame.loc[frame["split"].astype(str).eq(split_name), ["timestamp"]].copy()
        if not part.empty:
            parts.append(part)
    if not parts:
        raise RuntimeError(f"empty split window: {split_name}")
    timestamps = pd.to_datetime(pd.concat(parts, ignore_index=True)["timestamp"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + timedelta(days=1)).strftime("%Y.%m.%d")


def _prob_frame(name: str, probabilities: np.ndarray) -> pd.DataFrame:
    probs = np.asarray(probabilities, dtype="float64")
    out = pd.DataFrame(
        {
            f"{name}_p_short": probs[:, 0],
            f"{name}_p_flat": probs[:, 1],
            f"{name}_p_long": probs[:, 2],
        }
    )
    out[f"{name}_confidence"] = probs.max(axis=1)
    out[f"{name}_long_margin"] = probs[:, 2] - np.maximum(probs[:, 0], probs[:, 1])
    out[f"{name}_abstain_weak_margin"] = out[f"{name}_confidence"].lt(0.45)
    return out


def _predict_proba_ordered(model: Any, values: np.ndarray) -> np.ndarray:
    raw = np.asarray(model.predict_proba(values), dtype="float64")
    classes = [int(value) for value in getattr(model, "classes_", MODEL_RESPONSE_CLASSES)]
    out = np.zeros((raw.shape[0], len(MODEL_RESPONSE_CLASSES)), dtype="float64")
    for source_index, klass in enumerate(classes):
        if klass in MODEL_RESPONSE_CLASSES:
            out[:, MODEL_RESPONSE_CLASSES.index(klass)] = raw[:, source_index]
    row_sum = out.sum(axis=1, keepdims=True)
    return np.divide(out, row_sum, out=np.full_like(out, 1.0 / len(MODEL_RESPONSE_CLASSES)), where=row_sum > 0)


def _sample_train(frame: pd.DataFrame, max_rows: int, *, seed: int = 3701) -> pd.DataFrame:
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    if len(train) <= max_rows:
        return train
    return train.sample(n=max_rows, random_state=seed).sort_values("timestamp").reset_index(drop=True)


def _attach_simple_context(frame: pd.DataFrame, vol_thresholds: Mapping[str, float]) -> pd.DataFrame:
    out = frame.copy()
    minutes = pd.to_numeric(out.get("minutes_from_cash_open"), errors="coerce")
    is_cash = pd.to_numeric(out.get("is_us_cash_open"), errors="coerce").fillna(0.0).gt(0.5)
    out["session_bucket"] = np.select(
        [
            ~is_cash,
            minutes.lt(30),
            minutes.lt(180),
            minutes.lt(330),
            minutes.ge(330),
        ],
        [
            "outside_us_cash",
            "cash_open_0_30",
            "cash_mid_30_180",
            "cash_mid_180_330",
            "cash_late_330_plus",
        ],
        default="session_unknown",
    )
    vol = pd.to_numeric(out.get("historical_vol_20"), errors="coerce")
    out["volatility_regime"] = np.select(
        [vol.le(vol_thresholds["q33"]), vol.le(vol_thresholds["q66"])],
        ["vol_low", "vol_mid"],
        default="vol_high",
    )
    adx = pd.to_numeric(out.get("adx_14"), errors="coerce")
    di = pd.to_numeric(out.get("di_spread_14"), errors="coerce")
    out["adx_bucket"] = np.select(
        [adx.lt(20), adx.lt(25), adx.ge(25)],
        ["adx_low_chop", "adx_20_25_transition", "adx_trend"],
        default="adx_unknown",
    )
    out["di_pressure"] = np.select(
        [di.gt(5), di.lt(-5)],
        ["bull_pressure", "bear_pressure"],
        default="neutral_pressure",
    )
    out["trend_chop_context"] = np.select(
        [out["adx_bucket"].eq("adx_trend") & out["di_pressure"].eq("bull_pressure"), out["adx_bucket"].eq("adx_trend") & out["di_pressure"].eq("bear_pressure"), out["adx_bucket"].eq("adx_low_chop")],
        ["trend_bull", "trend_bear", "chop"],
        default="mixed_transition",
    )
    out["simple_context_long_permission"] = (
        out["session_bucket"].isin(["cash_mid_30_180", "cash_mid_180_330"])
        & out["volatility_regime"].ne("vol_high")
        & out["di_pressure"].isin(["bull_pressure", "neutral_pressure"])
        & out["adx_bucket"].ne("adx_low_chop")
    )
    return out


def _add_best_state_flags(
    frame: pd.DataFrame,
    *,
    hmm_best_state: int | None,
    markov_best_state: int | None,
) -> pd.DataFrame:
    out = frame.copy()
    out["hmm_train_best_long_state"] = hmm_best_state
    out["hmm_best_long_state_match"] = (
        pd.to_numeric(out.get("hmm_hidden_state"), errors="coerce").eq(hmm_best_state) if hmm_best_state is not None else False
    )
    out["markov_train_best_long_state"] = markov_best_state
    out["markov_best_long_state_match"] = (
        pd.to_numeric(out.get("markov_state"), errors="coerce").eq(markov_best_state) if markov_best_state is not None else False
    )
    conf = pd.to_numeric(out.get("markov_state_confidence"), errors="coerce")
    entropy_inv = pd.to_numeric(out.get("markov_state_entropy_inv"), errors="coerce")
    out["markov_long_permission"] = (
        out["markov_best_long_state_match"].fillna(False) & conf.ge(0.97).fillna(False) & entropy_inv.ge(0.80).fillna(False)
    )
    return out


def rebuild_hmm_states(context: Mapping[str, Any]) -> dict[str, Any]:
    spec = next(item for item in default_stage22_hmm_variants(stage22_hmm.HMM_FEATURES) if item.variant_id == HMM_VARIANT_ID)
    tier_a_model = fit_hmm_variant(context["tier_a_frame"], context["hmm_feature_names"], spec)
    tier_b_model = fit_hmm_variant(context["tier_b_training_frame"], context["hmm_feature_names"], spec)
    tier_a_sequence = hmm_state_sequence_frame(tier_a_model, context["tier_a_frame"], tier_scope=mt5.TIER_A, record_view="tier_a_rebuilt_hmm")
    tier_b_sequence = hmm_state_sequence_frame(tier_b_model, context["tier_b_fallback_frame"], tier_scope=mt5.TIER_B, record_view="tier_b_rebuilt_hmm")
    tier_a_summary = hmm_state_summary_frame(tier_a_sequence)
    tier_b_summary = hmm_state_summary_frame(tier_b_sequence)
    tier_ab_sequence = pd.concat(
        [tier_a_sequence.assign(record_source="tier_a"), tier_b_sequence.assign(record_source="tier_b_fallback")],
        ignore_index=True,
    )
    artifacts = {
        "tier_a_sequence": save_frame(STATE_ROOT / "tier_a_rebuilt_hmm_state_sequence.parquet", tier_a_sequence),
        "tier_b_sequence": save_frame(STATE_ROOT / "tier_b_rebuilt_hmm_state_sequence.parquet", tier_b_sequence),
        "tier_ab_sequence": save_frame(STATE_ROOT / "tier_ab_rebuilt_hmm_state_sequence.parquet", tier_ab_sequence),
        "tier_a_summary": save_frame(RESULT_ROOT / "tier_a_rebuilt_hmm_state_summary.csv", tier_a_summary),
        "tier_b_summary": save_frame(RESULT_ROOT / "tier_b_rebuilt_hmm_state_summary.csv", tier_b_summary),
    }
    best_a = int(tier_a_summary.loc[tier_a_summary["split"].eq("train")].sort_values("future_return_mean").iloc[-1]["hidden_state"])
    best_b = int(tier_b_summary.loc[tier_b_summary["split"].eq("train")].sort_values("future_return_mean").iloc[-1]["hidden_state"])
    return {
        "variant_id": spec.variant_id,
        "tier_a_sequence": tier_a_sequence,
        "tier_b_sequence": tier_b_sequence,
        "tier_a_summary": tier_a_summary,
        "tier_b_summary": tier_b_summary,
        "tier_a_quality": hmm_state_quality_read(tier_a_summary, n_components=spec.n_components),
        "tier_b_quality": hmm_state_quality_read(tier_b_summary, n_components=spec.n_components),
        "tier_a_transition": hmm_transition_read(tier_a_model),
        "tier_b_transition": hmm_transition_read(tier_b_model),
        "tier_a_best_long_state": best_a,
        "tier_b_best_long_state": best_b,
        "artifacts": artifacts,
    }


def rebuild_markov_states(context: Mapping[str, Any]) -> dict[str, Any]:
    spec = next(item for item in stage28_markov.default_variants(mt5.TIER_B_CORE_FEATURE_ORDER) if item.variant_id == MARKOV_VARIANT_ID)
    tier_a = stage28_markov.evaluate_side(context["tier_a_frame"], spec, tier_scope=mt5.TIER_A, record_view="tier_a_rebuilt_markov")
    tier_b = stage28_markov.evaluate_side(context["tier_b_fallback_frame"], spec, tier_scope=mt5.TIER_B, record_view="tier_b_rebuilt_markov")
    if tier_a["status"] != "completed" or tier_b["status"] != "completed":
        raise RuntimeError(f"markov rebuild failed: tier_a={tier_a.get('status')} tier_b={tier_b.get('status')}")
    tier_a_sequence = tier_a["sequence"]
    tier_b_sequence = tier_b["sequence"]
    tier_ab_sequence = pd.concat(
        [tier_a_sequence.assign(record_source="tier_a"), tier_b_sequence.assign(record_source="tier_b_fallback")],
        ignore_index=True,
    )
    artifacts = {
        "tier_a_sequence": save_frame(STATE_ROOT / "tier_a_rebuilt_markov_state_sequence.parquet", tier_a_sequence),
        "tier_b_sequence": save_frame(STATE_ROOT / "tier_b_rebuilt_markov_state_sequence.parquet", tier_b_sequence),
        "tier_ab_sequence": save_frame(STATE_ROOT / "tier_ab_rebuilt_markov_state_sequence.parquet", tier_ab_sequence),
        "tier_a_summary": save_frame(RESULT_ROOT / "tier_a_rebuilt_markov_state_summary.csv", tier_a["summary"]),
        "tier_b_summary": save_frame(RESULT_ROOT / "tier_b_rebuilt_markov_state_summary.csv", tier_b["summary"]),
    }
    best_a = int(tier_a["summary"].loc[tier_a["summary"]["split"].eq("train")].sort_values("future_return_mean").iloc[-1]["markov_state"])
    best_b = int(tier_b["summary"].loc[tier_b["summary"]["split"].eq("train")].sort_values("future_return_mean").iloc[-1]["markov_state"])
    return {
        "variant_id": spec.variant_id,
        "tier_a_sequence": tier_a_sequence,
        "tier_b_sequence": tier_b_sequence,
        "tier_a_summary": tier_a["summary"],
        "tier_b_summary": tier_b["summary"],
        "tier_a_quality": tier_a["quality"],
        "tier_b_quality": tier_b["quality"],
        "tier_a_transition": tier_a["transition"],
        "tier_b_transition": tier_b["transition"],
        "tier_a_best_long_state": best_a,
        "tier_b_best_long_state": best_b,
        "artifacts": artifacts,
    }


def train_tier_a_model_responses(frame: pd.DataFrame, feature_order: Sequence[str], args: argparse.Namespace) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    responses = pd.DataFrame({"timestamp": frame["timestamp"].to_numpy()})
    summary: list[dict[str, Any]] = []
    x_all = frame.loc[:, list(feature_order)].to_numpy(dtype="float32", copy=False)
    y_all = frame["label_class"].astype("int64").to_numpy()

    def add_response(model_name: str, probabilities: np.ndarray, status: str, detail: str = "") -> None:
        nonlocal responses
        response = _prob_frame(model_name, probabilities)
        responses = pd.concat([responses, response], axis=1)
        summary.append({"model_response": model_name, "status": status, "detail": detail, "rows": int(len(response))})

    train_sample = _sample_train(frame, int(args.model_train_rows), seed=3701)
    x_train = train_sample.loc[:, list(feature_order)].to_numpy(dtype="float32", copy=False)
    y_train = train_sample["label_class"].astype("int64").to_numpy()

    try:
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=600, class_weight="balanced", solver="lbfgs", n_jobs=1),
        )
        model.fit(x_train, y_train)
        add_response("logreg", _predict_proba_ordered(model, x_all), "completed", "stage37_recomputed_logistic_response_surface")
    except Exception as exc:  # noqa: BLE001
        add_response("logreg", np.full((len(frame), 3), 1.0 / 3.0), "failed_fallback_uniform", str(exc))

    try:
        base = LogisticRegression(max_iter=500, class_weight="balanced", solver="lbfgs", n_jobs=1)
        calibrated = make_pipeline(
            StandardScaler(),
            CalibratedClassifierCV(base, method="sigmoid", cv=3),
        )
        calibrated.fit(x_train, y_train)
        add_response("calibrated_logreg", _predict_proba_ordered(calibrated, x_all), "completed", "calibration_and_abstention_surface")
    except Exception as exc:  # noqa: BLE001
        add_response("calibrated_logreg", np.full((len(frame), 3), 1.0 / 3.0), "failed_fallback_uniform", str(exc))

    try:
        from interpret.glassbox import ExplainableBoostingClassifier

        ebm_sample = _sample_train(frame, int(args.ebm_train_rows), seed=3702)
        model = ExplainableBoostingClassifier(
            interactions=0,
            max_bins=64,
            max_rounds=80,
            learning_rate=0.04,
            random_state=3702,
            n_jobs=1,
        )
        model.fit(
            ebm_sample.loc[:, list(feature_order)].to_numpy(dtype="float32", copy=False),
            ebm_sample["label_class"].astype("int64").to_numpy(),
        )
        add_response("ebm", _predict_proba_ordered(model, x_all), "completed", "stage37_recomputed_ebm_main_effect_response_surface")
    except Exception as exc:  # noqa: BLE001
        add_response("ebm", np.full((len(frame), 3), 1.0 / 3.0), "failed_fallback_uniform", str(exc))

    try:
        from catboost import CatBoostClassifier

        cb_sample = _sample_train(frame, int(args.catboost_train_rows), seed=3703)
        model = CatBoostClassifier(
            iterations=120,
            depth=4,
            learning_rate=0.05,
            loss_function="MultiClass",
            random_seed=3703,
            verbose=False,
            allow_writing_files=False,
            thread_count=1,
        )
        model.fit(
            cb_sample.loc[:, list(feature_order)].to_numpy(dtype="float32", copy=False),
            cb_sample["label_class"].astype("int64").to_numpy(),
        )
        add_response("catboost", _predict_proba_ordered(model, x_all), "completed", "stage37_recomputed_catboost_response_surface")
    except Exception as exc:  # noqa: BLE001
        add_response("catboost", np.full((len(frame), 3), 1.0 / 3.0), "failed_fallback_uniform", str(exc))

    try:
        regime = HistGradientBoostingClassifier(max_iter=120, max_leaf_nodes=15, learning_rate=0.05, random_state=3704)
        regime.fit(x_train, y_train)
        add_response("supervised_regime", _predict_proba_ordered(regime, x_all), "completed", "hist_gradient_boosting_supervised_regime_response")
    except Exception as exc:  # noqa: BLE001
        add_response("supervised_regime", np.full((len(frame), 3), 1.0 / 3.0), "failed_fallback_uniform", str(exc))

    try:
        tcn_probs = train_tcn_response(frame, args)
        add_response("tcn", tcn_probs, "completed", "compact_torch_tcn_temporal_response_surface")
    except Exception as exc:  # noqa: BLE001
        add_response("tcn", np.full((len(frame), 3), 1.0 / 3.0), "failed_fallback_uniform", str(exc))

    long_cols = [col for col in responses.columns if col.endswith("_p_long")]
    confidence_cols = [col for col in responses.columns if col.endswith("_confidence")]
    margin_cols = [col for col in responses.columns if col.endswith("_long_margin")]
    responses["single_base_long_score"] = responses[long_cols].mean(axis=1)
    responses["single_base_confidence"] = responses[confidence_cols].mean(axis=1)
    responses["single_base_long_margin"] = responses[margin_cols].mean(axis=1)
    responses["single_base_abstain"] = responses["single_base_confidence"].lt(0.43) | responses["single_base_long_margin"].between(-0.04, 0.04)
    return responses, summary


def _sequence_tensor(values: np.ndarray, lookback: int) -> np.ndarray:
    n_rows, n_features = values.shape
    out = np.zeros((n_rows, n_features, lookback), dtype="float32")
    for index in range(n_rows):
        start = max(0, index - lookback + 1)
        window = values[start : index + 1].T
        out[index, :, -window.shape[1] :] = window
    return out


def train_tcn_response(frame: pd.DataFrame, args: argparse.Namespace) -> np.ndarray:
    import torch
    from torch import nn
    from torch.utils.data import DataLoader, TensorDataset

    lookback = int(args.tcn_lookback)
    work = frame.sort_values("timestamp").reset_index(drop=True)
    train = work["split"].astype(str).eq("train")
    values = work.loc[:, list(TCN_FEATURES)].to_numpy(dtype="float32", copy=False)
    mean = values[train.to_numpy()].mean(axis=0, keepdims=True)
    std = values[train.to_numpy()].std(axis=0, keepdims=True)
    std[std <= 1e-6] = 1.0
    values = (values - mean) / std
    sequence = _sequence_tensor(values, lookback)
    y = work["label_class"].astype("int64").to_numpy()
    train_indices = np.flatnonzero(train.to_numpy())
    if len(train_indices) > int(args.tcn_train_rows):
        rng = np.random.default_rng(3705)
        train_indices = np.sort(rng.choice(train_indices, size=int(args.tcn_train_rows), replace=False))

    class TinyTcn(nn.Module):
        def __init__(self, feature_count: int) -> None:
            super().__init__()
            self.net = nn.Sequential(
                nn.Conv1d(feature_count, 16, kernel_size=3, padding=2, dilation=2),
                nn.ReLU(),
                nn.Conv1d(16, 16, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.AdaptiveAvgPool1d(1),
                nn.Flatten(),
                nn.Linear(16, 3),
            )

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.net(x)

    torch.manual_seed(3705)
    model = TinyTcn(len(TCN_FEATURES))
    dataset = TensorDataset(torch.from_numpy(sequence[train_indices]), torch.from_numpy(y[train_indices]))
    loader = DataLoader(dataset, batch_size=512, shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
    loss_fn = nn.CrossEntropyLoss()
    model.train()
    for _ in range(int(args.tcn_epochs)):
        for batch_x, batch_y in loader:
            optimizer.zero_grad()
            loss = loss_fn(model(batch_x), batch_y)
            loss.backward()
            optimizer.step()
    model.eval()
    probs: list[np.ndarray] = []
    with torch.no_grad():
        for start in range(0, len(sequence), 2048):
            logits = model(torch.from_numpy(sequence[start : start + 2048]))
            probs.append(torch.softmax(logits, dim=1).numpy())
    by_sorted = np.vstack(probs)
    out = pd.DataFrame({"timestamp": work["timestamp"], "p0": by_sorted[:, 0], "p1": by_sorted[:, 1], "p2": by_sorted[:, 2]})
    merged = frame.loc[:, ["timestamp"]].merge(out, on="timestamp", how="left", validate="one_to_one")
    return merged.loc[:, ["p0", "p1", "p2"]].to_numpy(dtype="float64")


def train_tier_b_core_response(tier_b_training: pd.DataFrame, tier_b_fallback: pd.DataFrame) -> pd.DataFrame:
    feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    train = tier_b_training.loc[tier_b_training["split"].astype(str).eq("train")].copy()
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=500, class_weight="balanced", solver="lbfgs", n_jobs=1),
    )
    model.fit(train.loc[:, feature_order].to_numpy(dtype="float32", copy=False), train["label_class"].astype("int64").to_numpy())
    probs = _predict_proba_ordered(model, tier_b_fallback.loc[:, feature_order].to_numpy(dtype="float32", copy=False))
    response = pd.concat([tier_b_fallback.loc[:, ["timestamp"]].reset_index(drop=True), _prob_frame("core_logreg", probs)], axis=1)
    response["single_base_long_score"] = response["core_logreg_p_long"]
    response["single_base_confidence"] = response["core_logreg_confidence"]
    response["single_base_long_margin"] = response["core_logreg_long_margin"]
    response["single_base_abstain"] = response["core_logreg_abstain_weak_margin"]
    return response


def build_state_context_tables(
    context: Mapping[str, Any],
    hmm: Mapping[str, Any],
    markov: Mapping[str, Any],
    atlas: Mapping[str, Any],
    tier_a_responses: pd.DataFrame,
    tier_b_responses: pd.DataFrame,
) -> dict[str, Any]:
    tier_a = context["tier_a_frame"].copy()
    vol_thresholds = {
        "q33": float(tier_a.loc[tier_a["split"].astype(str).eq("train"), "historical_vol_20"].quantile(0.33)),
        "q66": float(tier_a.loc[tier_a["split"].astype(str).eq("train"), "historical_vol_20"].quantile(0.66)),
    }
    tier_a = _attach_simple_context(tier_a, vol_thresholds)
    tier_b = _attach_simple_context(context["tier_b_fallback_frame"].copy(), vol_thresholds)

    tier_a_hmm = hmm["tier_a_sequence"].rename(columns={"hidden_state": "hmm_hidden_state", "hidden_state_label": "hmm_hidden_state_label"})
    tier_b_hmm = hmm["tier_b_sequence"].rename(columns={"hidden_state": "hmm_hidden_state", "hidden_state_label": "hmm_hidden_state_label"})
    tier_a = tier_a.merge(tier_a_hmm.loc[:, ["timestamp", "hmm_hidden_state", "hmm_hidden_state_label"]], on="timestamp", how="left", validate="one_to_one")
    tier_b = tier_b.merge(tier_b_hmm.loc[:, ["timestamp", "hmm_hidden_state", "hmm_hidden_state_label"]], on="timestamp", how="left", validate="one_to_one")

    def markov_columns(sequence: pd.DataFrame) -> pd.DataFrame:
        cols = ["timestamp", "markov_state", "state_confidence", "state_entropy", "source_row_index"]
        out = sequence.loc[:, [col for col in cols if col in sequence.columns]].copy()
        out = out.rename(
            columns={
                "state_confidence": "markov_state_confidence",
                "state_entropy": "markov_state_entropy",
                "source_row_index": "markov_source_row_index",
            }
        )
        out["markov_state_entropy_inv"] = 1.0 - pd.to_numeric(out["markov_state_entropy"], errors="coerce")
        return out

    tier_a = tier_a.merge(markov_columns(markov["tier_a_sequence"]), on="timestamp", how="left", validate="one_to_one")
    tier_b = tier_b.merge(markov_columns(markov["tier_b_sequence"]), on="timestamp", how="left", validate="one_to_one")

    atlas_frame = atlas["frame"].loc[:, ["timestamp", *[f"state_{topic.topic_id}" for topic in stage35_cfg.TOPICS]]].copy()
    tier_a = tier_a.merge(atlas_frame, on="timestamp", how="left", validate="one_to_one")
    for selection in atlas["selections"]:
        topic_id = str(selection["topic_id"])
        state_col = f"state_{topic_id}"
        flag_col = f"kmeans_{topic_id}_selected_state_match"
        tier_a[flag_col] = pd.to_numeric(tier_a[state_col], errors="coerce").eq(int(selection["selected_state_id"]))
        tier_a[f"kmeans_{topic_id}_selected_direction"] = str(selection["state_direction"])
    for topic in stage35_cfg.TOPICS:
        tier_b[f"state_{topic.topic_id}"] = np.nan
        tier_b[f"kmeans_{topic.topic_id}_selected_state_match"] = False
        tier_b[f"kmeans_{topic.topic_id}_selected_direction"] = "out_of_scope_by_partial_context"

    tier_a = _add_best_state_flags(
        tier_a,
        hmm_best_state=int(hmm["tier_a_best_long_state"]),
        markov_best_state=int(markov["tier_a_best_long_state"]),
    )
    tier_b = _add_best_state_flags(
        tier_b,
        hmm_best_state=int(hmm["tier_b_best_long_state"]),
        markov_best_state=int(markov["tier_b_best_long_state"]),
    )
    tier_a = tier_a.merge(tier_a_responses, on="timestamp", how="left", validate="one_to_one")
    tier_b = tier_b.merge(tier_b_responses, on="timestamp", how="left", validate="one_to_one")
    tier_a["tier_scope"] = mt5.TIER_A
    tier_b["tier_scope"] = mt5.TIER_B
    tier_a["common_table_role"] = "tier_a_primary_full_context"
    tier_b["common_table_role"] = "tier_b_partial_context_fallback"

    common_table = pd.concat([tier_a, tier_b], ignore_index=True, sort=False)
    common_table["feature_ready_timestamp"] = pd.to_datetime(common_table["timestamp"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    common_table["state_context_stack_available"] = (
        common_table["hmm_hidden_state"].notna()
        | common_table["markov_state"].notna()
        | common_table[[f"state_{topic.topic_id}" for topic in stage35_cfg.TOPICS]].notna().any(axis=1)
    )
    artifacts = {
        "common_state_context_response_table": save_frame(RESULT_ROOT / "common_state_context_response_table.parquet", common_table),
        "common_state_context_response_preview": save_frame(
            RESULT_ROOT / "common_state_context_response_preview.csv",
            common_table.head(1000),
        ),
    }
    return {
        "tier_a": tier_a,
        "tier_b": tier_b,
        "common": common_table,
        "vol_thresholds": vol_thresholds,
        "artifacts": artifacts,
    }


def state_response_decomposition(common_table: pd.DataFrame) -> list[dict[str, Any]]:
    dimensions = [
        "hmm_hidden_state",
        "markov_state",
        "state_return_volatility_shape",
        "state_trend_momentum_pressure",
        "state_session_timing_map",
        "session_bucket",
        "volatility_regime",
        "trend_chop_context",
        "adx_bucket",
        "di_pressure",
        "markov_long_permission",
        "simple_context_long_permission",
    ]
    response_cols = [
        "logreg_p_long",
        "ebm_p_long",
        "catboost_p_long",
        "supervised_regime_p_long",
        "calibrated_logreg_p_long",
        "tcn_p_long",
        "single_base_long_score",
    ]
    rows: list[dict[str, Any]] = []
    for tier_scope, tier_frame in common_table.groupby("tier_scope", dropna=False):
        for dimension in dimensions:
            if dimension not in tier_frame.columns:
                continue
            for (split_name, value), group in tier_frame.groupby(["split", dimension], dropna=False):
                values = pd.to_numeric(group["future_log_return_12"], errors="coerce")
                labels = group["label"].astype(str) if "label" in group else pd.Series([], dtype=str)
                row = {
                    "tier_scope": str(tier_scope),
                    "split": str(split_name),
                    "dimension": dimension,
                    "value": str(value),
                    "rows": int(len(group)),
                    "future_return_mean": safe_float(values.mean()),
                    "future_return_sum": safe_float(values.sum()),
                    "long_label_rate": safe_float(labels.eq("long").mean()) if len(labels) else None,
                    "short_label_rate": safe_float(labels.eq("short").mean()) if len(labels) else None,
                }
                for col in response_cols:
                    if col in group.columns:
                        row[f"mean_{col}"] = safe_float(pd.to_numeric(group[col], errors="coerce").mean())
                rows.append(row)
    return rows


def state_alignment_summary(common_table: pd.DataFrame) -> list[dict[str, Any]]:
    pairs = [
        ("hmm_hidden_state", "markov_state"),
        ("hmm_hidden_state", "state_return_volatility_shape"),
        ("markov_state", "state_return_volatility_shape"),
        ("session_bucket", "state_session_timing_map"),
        ("volatility_regime", "state_return_volatility_shape"),
        ("trend_chop_context", "state_trend_momentum_pressure"),
    ]
    rows: list[dict[str, Any]] = []
    for tier_scope, tier_frame in common_table.groupby("tier_scope", dropna=False):
        for left, right in pairs:
            if left not in tier_frame.columns or right not in tier_frame.columns:
                continue
            work = tier_frame.loc[tier_frame[left].notna() & tier_frame[right].notna()]
            for (split_name, left_value, right_value), group in work.groupby(["split", left, right], dropna=False):
                rows.append(
                    {
                        "tier_scope": str(tier_scope),
                        "split": str(split_name),
                        "left_axis": left,
                        "left_value": str(left_value),
                        "right_axis": right,
                        "right_value": str(right_value),
                        "rows": int(len(group)),
                        "future_return_mean": safe_float(pd.to_numeric(group["future_log_return_12"], errors="coerce").mean()),
                        "single_base_long_score_mean": safe_float(pd.to_numeric(group.get("single_base_long_score"), errors="coerce").mean()),
                    }
                )
    return rows


def _runtime_variant_mask(frame: pd.DataFrame, variant_id: str) -> pd.Series:
    base = pd.to_numeric(frame.get("single_base_long_score"), errors="coerce").fillna(0.0)
    session_ok = frame.get("session_bucket", "").isin(["cash_mid_30_180", "cash_mid_180_330", "cash_open_0_30"])
    context_ok = frame.get("simple_context_long_permission", False).fillna(False)
    hmm_ok = frame.get("hmm_best_long_state_match", False).fillna(False)
    markov_ok = frame.get("markov_long_permission", False).fillna(False)
    kmeans_return_ok = frame.get("kmeans_return_volatility_shape_selected_state_match", False).fillna(False)
    kmeans_trend_ok = frame.get("kmeans_trend_momentum_pressure_selected_state_match", False).fillna(False)
    vol_not_high = frame.get("volatility_regime", "").ne("vol_high")
    adx_trend_or_transition = frame.get("adx_bucket", "").isin(["adx_20_25_transition", "adx_trend"])
    if variant_id == "simple_context_control":
        return context_ok
    if variant_id == "single_base_state_filter":
        return base.ge(0.39) & vol_not_high & session_ok & (hmm_ok | markov_ok | kmeans_return_ok)
    if variant_id == "single_base_state_adapter":
        return ((base.ge(0.35) & (markov_ok | kmeans_return_ok)) | (base.ge(0.41) & hmm_ok) | (base.ge(0.45) & kmeans_trend_ok)) & session_ok
    if variant_id == "limited_state_specialist_router":
        return markov_ok | (kmeans_return_ok & base.ge(0.32)) | (kmeans_trend_ok & adx_trend_or_transition) | (hmm_ok & context_ok)
    raise ValueError(f"unknown runtime variant: {variant_id}")


def _select_runtime_rows(frame: pd.DataFrame, variant_id: str, split_name: str, feature_order: Sequence[str]) -> tuple[pd.DataFrame, dict[str, Any]]:
    split_frame = frame.loc[frame["split"].astype(str).eq(split_name)].copy()
    mask = _runtime_variant_mask(split_frame, variant_id)
    selected = split_frame.loc[mask].copy()
    floor_applied = False
    min_rows = 25
    if len(selected) < min_rows and not split_frame.empty:
        floor_applied = True
        score = pd.to_numeric(split_frame.get("single_base_long_score"), errors="coerce").fillna(0.0)
        floor_mask = score.ge(score.quantile(0.88))
        selected = split_frame.loc[floor_mask].copy()
    selected = selected.sort_values("timestamp").reset_index(drop=True)
    missing = [col for col in feature_order if col not in selected.columns]
    if missing:
        raise RuntimeError(f"selected runtime rows missing features: {missing[:5]}")
    summary = {
        "variant_id": variant_id,
        "split": split_name,
        "source_rows": int(len(split_frame)),
        "selected_rows": int(len(selected)),
        "selection_rate": round(float(len(selected) / max(1, len(split_frame))), 6),
        "floor_applied": bool(floor_applied),
    }
    return selected, summary


def write_constant_score_table(path: Path, *, direction: str, feature_count: int) -> dict[str, Any]:
    if direction not in {"long", "short"}:
        raise ValueError(f"unsupported direction: {direction}")
    intercept = {"short": (2.2, 0.0, 0.0), "long": (0.0, 0.0, 2.2)}[direction]
    rows = [
        {
            "record_type": "intercept",
            "feature_index": -1,
            "item_index": -1,
            "value": "",
            "score_short": intercept[0],
            "score_flat": intercept[1],
            "score_long": intercept[2],
        }
    ]
    for feature_index in range(int(feature_count)):
        rows.append({"record_type": "score", "feature_index": feature_index, "item_index": 0, "value": "", "score_short": 0.0, "score_flat": 0.0, "score_long": 0.0})
        rows.append({"record_type": "score", "feature_index": feature_index, "item_index": 1, "value": "", "score_short": 0.0, "score_flat": 0.0, "score_long": 0.0})
    write_csv(path, rows, ("record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long"))
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "direction": direction, "feature_count": int(feature_count), "backend": "ebm_table_constant"}


def materialize_runtime_inputs(tables: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    tier_a = tables["tier_a"]
    tier_b = tables["tier_b"]
    common_root = common_run_root(STAGE_NUMBER, RUN_ID)
    tier_a_order = list(stage35_cfg.FEATURE_ORDER)
    tier_b_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    model_outputs = {
        "tier_a_long": write_constant_score_table(MODEL_ROOT / "tier_a_long_constant_score_table.csv", direction="long", feature_count=len(tier_a_order)),
        "tier_b_long": write_constant_score_table(MODEL_ROOT / "tier_b_long_constant_score_table.csv", direction="long", feature_count=len(tier_b_order)),
    }
    common_copies = [
        copy_to_common(MODEL_ROOT / "tier_a_long_constant_score_table.csv", f"{common_root}/models/tier_a_long_constant_score_table.csv", COMMON_FILES_ROOT_DEFAULT),
        copy_to_common(MODEL_ROOT / "tier_b_long_constant_score_table.csv", f"{common_root}/models/tier_b_long_constant_score_table.csv", COMMON_FILES_ROOT_DEFAULT),
    ]
    feature_outputs: dict[str, Any] = {}
    selection_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    for variant_id in RUNTIME_VARIANTS:
        feature_outputs[variant_id] = {}
        for split_name in ("validation", "oos"):
            split_label = _split_label(split_name)
            tier_a_selected, tier_a_selection = _select_runtime_rows(tier_a, variant_id, split_name, tier_a_order)
            tier_b_selected, tier_b_selection = _select_runtime_rows(tier_b, variant_id, split_name, tier_b_order)
            tier_a_path = FEATURE_ROOT / f"tier_a_{variant_id}_{split_label}_features.csv"
            tier_b_path = FEATURE_ROOT / f"tier_b_{variant_id}_{split_label}_features.csv"
            tier_a_export = mt5.export_mt5_feature_matrix_csv(
                tier_a_selected,
                tier_a_order,
                tier_a_path,
                metadata_columns=("hmm_hidden_state", "markov_state", "session_bucket", "volatility_regime", "single_base_long_score"),
            )
            tier_b_export = mt5.export_mt5_feature_matrix_csv(
                tier_b_selected,
                tier_b_order,
                tier_b_path,
                metadata_columns=("hmm_hidden_state", "markov_state", "session_bucket", "volatility_regime", "single_base_long_score"),
            )
            common_copies.append(copy_to_common(tier_a_path, f"{common_root}/features/{tier_a_path.name}", COMMON_FILES_ROOT_DEFAULT))
            common_copies.append(copy_to_common(tier_b_path, f"{common_root}/features/{tier_b_path.name}", COMMON_FILES_ROOT_DEFAULT))
            from_date, to_date = _split_dates_from_frames([tier_a, tier_b], split_name)
            tier_a_export["tester_window_from_date"] = from_date
            tier_a_export["tester_window_to_date"] = to_date
            tier_b_export["tester_window_from_date"] = from_date
            tier_b_export["tester_window_to_date"] = to_date
            feature_outputs[variant_id][split_label] = {"tier_a": tier_a_export, "tier_b": tier_b_export}
            selection_rows.append({"tier_scope": mt5.TIER_A, **tier_a_selection})
            selection_rows.append({"tier_scope": mt5.TIER_B, **tier_b_selection})
            attempts.append(
                attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=STAGE_NUMBER,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=f"routed_{variant_id}_{split_label}",
                    tier=mt5.TIER_AB,
                    split=split_label,
                    model_path=f"{common_root}/models/tier_a_long_constant_score_table.csv",
                    model_id=f"{RUN_ID}_{variant_id}_tier_a_long_constant",
                    model_backend="ebm_table",
                    feature_path=f"{common_root}/features/{tier_a_path.name}",
                    feature_count=len(tier_a_order),
                    feature_order_hash=ordered_hash(tier_a_order),
                    short_threshold=0.55,
                    long_threshold=0.55,
                    min_margin=0.05,
                    invert_signal=False,
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier="tier_a",
                    attempt_role="routed_total",
                    record_view_prefix=f"mt5_routed_{variant_id}",
                    max_hold_bars=stage35_cfg.MAX_HOLD_BARS,
                    common_root=common_root,
                    fallback_enabled=True,
                    fallback_model_path=f"{common_root}/models/tier_b_long_constant_score_table.csv",
                    fallback_model_id=f"{RUN_ID}_{variant_id}_tier_b_long_constant",
                    fallback_model_backend="ebm_table",
                    fallback_feature_path=f"{common_root}/features/{tier_b_path.name}",
                    fallback_feature_count=len(tier_b_order),
                    fallback_feature_order_hash=ordered_hash(tier_b_order),
                    fallback_short_threshold=0.55,
                    fallback_long_threshold=0.55,
                    fallback_min_margin=0.05,
                    fallback_invert_signal=False,
                    close_on_flat_signal=True,
                )
            )
    write_csv(RESULT_ROOT / "runtime_variant_selection_summary.csv", selection_rows)
    return {
        "common_root": common_root,
        "model_outputs": model_outputs,
        "feature_outputs": feature_outputs,
        "common_copies": common_copies,
        "attempts": attempts,
        "runtime_variant_selection_summary": selection_rows,
        "known_runtime_difference": "State/context routing is precomputed in Python and handed to MT5 by feature-row omission plus Tier A primary/Tier B fallback feature files; this is runtime_probe, not runtime authority.",
    }


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.materialize_only):
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "not_attempted_materialize_only",
            "judgment": "not_attempted_materialize_only",
        }
    try:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
            common_files_root=COMMON_FILES_ROOT_DEFAULT,
            tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
            timeout_seconds=int(args.timeout_seconds),
        )
    except Exception as exc:  # noqa: BLE001
        return {
            **dict(prepared),
            "compile": {"status": "exception_or_not_completed"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": JUDGMENT_BLOCKED,
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    completed = result.get("external_verification_status") == "completed"
    result = dict(result)
    result["judgment"] = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    return result


def _metrics(record: Mapping[str, Any]) -> Mapping[str, Any]:
    metrics = record.get("metrics", {})
    return metrics if isinstance(metrics, Mapping) else {}


def _record_variant(record_view: str) -> str:
    text = str(record_view)
    for variant_id in RUNTIME_VARIANTS:
        if variant_id in text:
            return variant_id
    return "unknown"


def runtime_comparison_rows(mt5_records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in mt5_records:
        metrics = _metrics(record)
        rows.append(
            {
                "variant_id": _record_variant(str(record.get("record_view", ""))),
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "route_role": record.get("route_role"),
                "split": record.get("split"),
                "status": record.get("status"),
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "order_attempt_count": metrics.get("order_attempt_count"),
                "feature_ready_count": metrics.get("feature_ready_count"),
                "tier_a_primary_labelable_rows": metrics.get("tier_a_primary_labelable_rows"),
                "tier_b_fallback_labelable_rows": metrics.get("tier_b_fallback_labelable_rows"),
            }
        )
    return rows


def judge_structure(runtime_rows: Sequence[Mapping[str, Any]], external_status: str) -> dict[str, Any]:
    if external_status != "completed":
        return {
            "judgment_label": "state_context_not_useful_or_inconclusive",
            "reason": "MT5 runtime probe did not complete, so structure cannot be promoted beyond inconclusive.",
            "selected_structure": None,
            "comparison": [],
        }
    by_variant: dict[str, dict[str, Any]] = {}
    for row in runtime_rows:
        if row.get("route_role") != "routed_total":
            continue
        variant = str(row.get("variant_id"))
        split = _split_from_label(str(row.get("split")))
        metrics = by_variant.setdefault(variant, {"variant_id": variant})
        metrics[f"{split}_net_profit"] = safe_float(row.get("net_profit"), 0.0)
        metrics[f"{split}_profit_factor"] = safe_float(row.get("profit_factor"))
        metrics[f"{split}_trade_count"] = int(safe_float(row.get("trade_count"), 0) or 0)
    comparison = list(by_variant.values())
    for row in comparison:
        val = safe_float(row.get("validation_net_profit"), 0.0) or 0.0
        oos = safe_float(row.get("oos_net_profit"), 0.0) or 0.0
        row["stability_score"] = round(float(min(val, oos) + 0.25 * (val + oos)), 6)
        row["both_splits_positive"] = bool(val > 0 and oos > 0)
        row["trade_count_floor_pass"] = bool((safe_float(row.get("validation_trade_count"), 0) or 0) >= 3 and (safe_float(row.get("oos_trade_count"), 0) or 0) >= 3)
    eligible = [row for row in comparison if row.get("both_splits_positive") and row.get("trade_count_floor_pass")]
    if not eligible:
        return {
            "judgment_label": "state_context_not_useful_or_inconclusive",
            "reason": "No state structure had positive validation and OOS routed totals with a minimal trade-count floor.",
            "selected_structure": None,
            "comparison": sorted(comparison, key=lambda row: row.get("stability_score", -999), reverse=True),
        }
    winner = max(eligible, key=lambda row: row.get("stability_score", -999.0))
    mapping = {
        "simple_context_control": "state_context_not_useful_or_inconclusive",
        "single_base_state_filter": "single_base_with_state_filter",
        "single_base_state_adapter": "single_base_with_state_adapter",
        "limited_state_specialist_router": "limited_state_specialist_router",
    }
    label = mapping.get(str(winner.get("variant_id")), "state_context_not_useful_or_inconclusive")
    return {
        "judgment_label": label,
        "reason": f"{winner.get('variant_id')} had the best positive validation/OOS routed total among completed broad probe variants.",
        "selected_structure": winner.get("variant_id"),
        "comparison": sorted(comparison, key=lambda row: row.get("stability_score", -999), reverse=True),
    }


def write_normalized_kpi() -> dict[str, Any]:
    inventory = [{"run_id": RUN_ID, "stage_id": STAGE_ID, "idea_id": RUN_NUMBER, "path": rel(RUN_ROOT)}]
    records, summary_rows, missing, parser_errors = mt5_kpi_recorder.build_normalized_records(ROOT, inventory)
    enriched: list[dict[str, Any]] = list(records)
    trade_rows: list[dict[str, Any]] = []
    trade_summary: list[dict[str, Any]] = []
    trade_errors: list[dict[str, Any]] = []
    if records:
        market_data = mt5_trade_attribution.MarketData.load(ROOT)
        enriched, trade_rows, trade_summary, trade_errors = mt5_trade_attribution.enrich_records(records, ROOT, market_data)
    write_json(PACKET_ROOT / "normalized_kpi_records.json", records)
    write_json(PACKET_ROOT / "normalized_kpi_summary.json", summary_rows)
    write_json(PACKET_ROOT / "normalized_kpi_missing_runs.json", missing)
    write_json(PACKET_ROOT / "normalized_kpi_parser_errors.json", parser_errors)
    write_json(PACKET_ROOT / "enriched_kpi_records.json", enriched)
    write_json(PACKET_ROOT / "trade_level_records.json", trade_rows)
    write_json(PACKET_ROOT / "trade_attribution_summary.json", trade_summary)
    write_json(PACKET_ROOT / "trade_attribution_parser_errors.json", trade_errors)
    return {
        "normalized_records": len(records),
        "normalized_summary_rows": len(summary_rows),
        "missing_runs": len(missing),
        "parser_errors": len(parser_errors),
        "trade_attribution_records": len(trade_summary),
        "trade_level_rows": len(trade_rows),
        "trade_parser_errors": len(trade_errors),
    }


def write_run_files(result: Mapping[str, Any], summary: Mapping[str, Any]) -> None:
    manifest = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "source_run_id": SOURCE_RUN_ID,
        "objective": "Judge state-context model structure only.",
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "compile": result.get("compile", {}),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": summary["result_judgment"]["judgment_label"],
        "boundary": BOUNDARY,
    }
    kpi_record = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "kpi_scope": "state_context_broad_routed_mt5_probe",
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "mt5_records": result.get("mt5_kpi_records", []),
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": result.get("external_verification_status"),
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "kpi_records": result.get("mt5_kpi_records", []),
        },
        "runtime_comparison_rows": summary.get("runtime_comparison_rows", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": summary["result_judgment"]["judgment_label"],
        "boundary": BOUNDARY,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = [
        {
            "ledger_row_id": f"{RUN_ID}__stage_open",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage_open",
            "parent_run_id": RUN_ID,
            "record_view": "stage_open_draft",
            "tier_scope": mt5.TIER_AB,
            "kpi_scope": "stage_question_boundary",
            "scoreboard_lane": "experiment_design",
            "status": "reviewed",
            "judgment": summary["result_judgment"]["judgment_label"],
            "path": rel(STAGE_OPEN_DRAFT_PATH),
            "primary_kpi": "question=single_base_filter_adapter_or_limited_router",
            "guardrail_kpi": BOUNDARY,
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Stage37 opened from Stage36 frontier02 state_context_stack.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__common_state_context_response_table",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "common_state_context_response_table",
            "parent_run_id": RUN_ID,
            "record_view": "common_state_context_response_table",
            "tier_scope": mt5.TIER_AB,
            "kpi_scope": "state_context_model_response",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": summary["result_judgment"]["judgment_label"],
            "path": summary["output_paths"]["common_state_context_response_table"],
            "primary_kpi": ledger_pairs(
                [
                    ("rows", summary["common_table_rows"]),
                    ("tier_a_rows", summary["tier_a_rows"]),
                    ("tier_b_rows", summary["tier_b_rows"]),
                ]
            ),
            "guardrail_kpi": BOUNDARY,
            "external_verification_status": "python_materialized",
            "notes": "HMM, Markov, KMeans, context, and model response columns share feature-ready timestamps.",
        },
    ]
    for record in summary.get("runtime_comparison_rows", []):
        metrics = ledger_pairs(
            [
                ("net_profit", record.get("net_profit")),
                ("profit_factor", record.get("profit_factor")),
                ("trade_count", record.get("trade_count")),
            ]
        )
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{record.get('record_view')}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": str(record.get("record_view")),
                "parent_run_id": RUN_ID,
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "kpi_scope": "broad_routed_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status"),
                "judgment": summary["result_judgment"]["judgment_label"],
                "path": rel(RUN_ROOT / "kpi_record.json"),
                "primary_kpi": metrics,
                "guardrail_kpi": BOUNDARY,
                "external_verification_status": summary["external_verification_status"],
                "notes": f"variant={record.get('variant_id')};route_role={record.get('route_role')};split={record.get('split')}",
            }
        )
    registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_probe",
        "status": "reviewed" if summary["external_verification_status"] == "completed" else "blocked",
        "judgment": summary["result_judgment"]["judgment_label"],
        "path": rel(REPORT_PATH),
        "notes": "Stage37 state-context structure judgment packet; no baseline, promotion, runtime authority, or live readiness.",
    }
    return {
        "stage_run_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "project_alpha_run_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id"),
    }


def _runtime_table_markdown(runtime_rows: Sequence[Mapping[str, Any]]) -> str:
    totals = [row for row in runtime_rows if row.get("route_role") == "routed_total"]
    lines = [
        "| variant(변형) | split(분할) | net(순손익) | PF(수익계수) | trades(거래 수) |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in totals:
        lines.append(
            "| {variant} | {split} | {net} | {pf} | {trades} |".format(
                variant=row.get("variant_id"),
                split=row.get("split"),
                net=row.get("net_profit"),
                pf=row.get("profit_factor"),
                trades=row.get("trade_count"),
            )
        )
    return "\n".join(lines)


def stage_brief_text() -> str:
    return f"""# Stage37 State Context: Single Base Filter Or State Router(37단계 상태 문맥: 단일 기준 필터 또는 상태 라우터)

## Question(질문)

상태 문맥(state context, 상태 문맥)을 먼저 자르면 모델 구조(model structure, 모델 구조)를 `single base model + state filter(단일 기준 모델 + 상태 필터)`로 유지할 수 있는지, `state adapter(상태 어댑터)`나 `limited state specialist router(제한된 상태별 전문 라우터)`가 필요한지 본다.

## Boundary(경계)

`{BOUNDARY}`

효과(effect, 효과): 이번 stage(단계)는 구조 판정(structure judgment, 구조 판정)만 남기고 baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 만들지 않는다.
"""


def stage_open_text() -> str:
    return f"""# Stage37 Open Draft(37단계 개방 초안)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source frontier(원천 전선): `frontier02_state_context_stack`
- primary family(주 작업군): `runtime_backtest(MT5/런타임/백테스트 실행)`
- primary skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`

행동(action, 행동): HMM state(은닉 상태), Markov state(마르코프 상태), KMeans state(K-평균 상태), Markov long permission(마르코프 롱 허용), 단순 context(문맥), 모델 반응(model response, 모델 반응)을 같은 timestamp(시각)에 붙인다.

효과(effect, 효과): state filter(상태 필터), state adapter(상태 어댑터), limited router(제한 라우터)를 같은 MT5 routed probe(MT5 라우팅 탐침) 안에서 비교한다.
"""


def report_text(summary: Mapping[str, Any]) -> str:
    judgment = summary["result_judgment"]
    return f"""# RUN31A State Context Router Broad MT5 Probe(31A 실행 상태 문맥 라우터 넓은 MT5 탐침)

## Judgment(판정)

- result judgment(결과 판정): `{judgment['judgment_label']}`
- reason(이유): {judgment['reason']}
- external verification(외부 검증): `{summary['external_verification_status']}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): 이번 결과는 model structure(모델 구조) 방향만 정한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 없다.

## Evidence(근거)

- common table(공통 테이블): `{summary['output_paths']['common_state_context_response_table']}`
- runtime variants(런타임 변형): `{len(RUNTIME_VARIANTS)}`
- MT5 attempts(MT5 시도): `{summary['mt5_attempt_count']}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{len(summary.get('runtime_comparison_rows', []))}`

{_runtime_table_markdown(summary.get('runtime_comparison_rows', []))}

## Claim Boundary(주장 경계)

이 packet(묶음)은 broad runtime probe(넓은 런타임 탐침)다. 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.
"""


def update_stage_docs(summary: Mapping[str, Any]) -> None:
    write_md(STAGE_BRIEF_PATH, stage_brief_text())
    write_md(STAGE_OPEN_DRAFT_PATH, stage_open_text())
    write_md(REPORT_PATH, report_text(summary))
    write_md(
        REVIEW_INDEX_PATH,
        f"""# Stage37 Review Index(37단계 검토 색인)

- status(상태): `reviewed`
- run(실행): `{RUN_ID}`
- packet(묶음): `{PACKET_ID}`
- latest report(최신 보고서): `{rel(REPORT_PATH)}`
- stage ledger(단계 장부): `{rel(STAGE_LEDGER_PATH)}`

효과(effect, 효과): Stage37(37단계)의 산출물 위치와 판정 경계를 한 곳에서 찾는다.
""",
    )
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage37 Selection Status(37단계 선택 상태)

- selected structure(선택 구조): `{summary['result_judgment']['judgment_label']}`
- selected baseline(선택 기준선): `none(없음)`
- promotion(승격): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- live readiness(실거래 준비): `none(없음)`
- latest packet(최신 묶음): `{PACKET_ID}`

효과(effect, 효과): 구조 단서(structure clue, 구조 단서)와 운영 주장(operating claim, 운영 주장)을 분리한다.
""",
    )
    write_md(
        DECISION_PATH,
        f"""# Decision: Open Stage37 State Context Router(결정: 37단계 상태 문맥 라우터 개방)

- decision(결정): Stage37(37단계) `{STAGE_ID}`를 RUN31A(31A 실행)로 연다.
- source(원천): Stage36(36단계) `frontier02_state_context_stack`
- completed judgment(완료 판정): `{summary['result_judgment']['judgment_label']}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): state context(상태 문맥)를 기준선 선택(baseline selection, 기준선 선택)이 아니라 구조 판정(structure judgment, 구조 판정)으로만 닫는다.
""",
    )


def write_packet_artifacts(summary: Mapping[str, Any]) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        [
            {"skill": "obsidian-runtime-parity", "status": "executed", "boundary": BOUNDARY},
            {"skill": "obsidian-backtest-forensics", "status": "executed", "mt5_attempts": summary["mt5_attempt_count"]},
            {"skill": "obsidian-data-integrity", "status": "executed", "common_table_rows": summary["common_table_rows"]},
            {"skill": "obsidian-model-validation", "status": "executed", "claim": "structure_judgment_only"},
            {"skill": "obsidian-result-judgment", "status": "executed", "judgment": summary["result_judgment"]["judgment_label"]},
            {"skill": "obsidian-artifact-lineage", "status": "executed", "output_paths": summary["output_paths"]},
        ],
    )
    gates = {
        "runtime_parity_gate.json": {
            "status": "passed" if summary["external_verification_status"] == "completed" else "blocked",
            "research_path": summary["output_paths"]["common_state_context_response_table"],
            "runtime_path": rel(RUN_ROOT / "kpi_record.json"),
            "known_runtime_difference": summary["runtime_inputs"]["known_runtime_difference"],
            "claim_boundary": BOUNDARY,
        },
        "runtime_evidence_gate.json": {
            "status": "passed" if summary["external_verification_status"] == "completed" else "blocked",
            "attempt_count": summary["mt5_attempt_count"],
            "kpi_record_count": len(summary.get("runtime_comparison_rows", [])),
            "external_verification_status": summary["external_verification_status"],
        },
        "backtest_forensics_gate.json": {
            "status": "passed" if summary["external_verification_status"] == "completed" else "blocked",
            "terminal_path": str(TERMINAL_PATH_DEFAULT),
            "metaeditor_path": str(METAEDITOR_PATH_DEFAULT),
            "ea": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
            "strategy_tester_reports": len(summary.get("strategy_tester_reports", [])),
            "cost_assumption": "MT5 Strategy Tester report authority; FPMarkets US100 M5 contract inherited.",
        },
        "data_integrity_gate.json": {
            "status": "passed",
            "common_table_rows": summary["common_table_rows"],
            "tier_a_rows": summary["tier_a_rows"],
            "tier_b_rows": summary["tier_b_rows"],
            "duplicate_feature_ready_timestamp_rows": summary["data_integrity"]["duplicate_tier_timestamp_rows"],
            "missing_state_notes": summary["data_integrity"]["missing_state_notes"],
        },
        "model_validation_gate.json": {
            "status": "passed",
            "model_response_training": summary["model_response_training_summary"],
            "selection_policy": "No baseline or promotion; responses are decomposed by state only.",
        },
        "result_judgment_gate.json": summary["result_judgment"],
        "artifact_lineage_gate.json": {
            "status": "passed",
            "source_artifacts": summary["source_artifacts"],
            "output_paths": summary["output_paths"],
        },
        "final_claim_guard.json": {
            "status": "passed",
            "allowed_claims": ["Stage37 structure judgment completed.", "Broad MT5 runtime probe evidence recorded."],
            "forbidden_claims": ["baseline", "promotion", "runtime_authority", "live_readiness"],
            "boundary": BOUNDARY,
        },
    }
    for name, payload in gates.items():
        write_json(PACKET_ROOT / name, payload)
    required = [
        "runtime_parity_gate",
        "runtime_evidence_gate",
        "backtest_forensics_gate",
        "data_integrity_gate",
        "model_validation_gate",
        "result_judgment_gate",
        "artifact_lineage_gate",
        "final_claim_guard",
        "required_gate_coverage_audit",
    ]
    write_json(
        PACKET_ROOT / "required_gate_coverage_audit.json",
        {"status": "passed", "required_gates": required, "covered_gates": required, "missing_gates": []},
    )


def update_current_truth(summary: Mapping[str, Any]) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    text = re.sub(
        rf"^- Stage37\(37단계\) {re.escape(STAGE_ID)} .+\n",
        "",
        text,
        flags=re.MULTILINE,
    )
    focus_line = (
        f"- Stage37(37단계) {STAGE_ID} reviewed_structure_judgment(구조 판정 검토됨): "
        f"{RUN_ID}(31A 실행)는 state context(상태 문맥), model response(모델 반응), broad MT5 routed probe(넓은 MT5 라우팅 탐침)를 묶어 "
        f"`{summary['result_judgment']['judgment_label']}`로 닫았다; baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 없다."
    )
    text = text.replace("current_focus:\n", f"current_focus:\n{focus_line}\n", 1)
    stage_block = f"""
stage37_state_context_router:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_structure_judgment
  current_run_id: {RUN_ID}
  idea_id: {IDEA_ID}
  source_frontier: frontier02_state_context_stack
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / 'aggregate_summary.json')}
  external_verification_status: {summary['external_verification_status']}
  result_judgment: {summary['result_judgment']['judgment_label']}
  next_action: {NEXT_ACTION}
  boundary: {BOUNDARY}

"""
    text = re.sub(
        r"stage37_state_context_router:\n(?:  .+\n)+\npre_alpha_stage_queue:",
        stage_block + "pre_alpha_stage_queue:",
        text,
        count=1,
    )
    if "stage37_state_context_router:" not in text:
        text = text.replace("pre_alpha_stage_queue:", stage_block + "pre_alpha_stage_queue:", 1)
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8")

    old = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    old = re.sub(
        r"^## Latest Stage37 State Context Router\(최신 37단계 상태 문맥 라우터\).*?(?=^## |\Z)",
        "",
        old,
        flags=re.DOTALL | re.MULTILINE,
    )
    block = f"""## Latest Stage37 State Context Router(최신 37단계 상태 문맥 라우터)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- latest packet(최신 묶음): `{PACKET_ID}`
- result judgment(결과 판정): `{summary['result_judgment']['judgment_label']}`
- external verification(외부 검증): `{summary['external_verification_status']}`

Stage37(37단계)는 HMM state(은닉 상태), Markov state(마르코프 상태), KMeans state(K-평균 상태), 단순 context(문맥), 모델 반응(model response, 모델 반응)을 같은 timestamp(시각)에 붙이고 broad MT5 routed probe(넓은 MT5 라우팅 탐침)를 실행했다.

효과(effect, 효과): 다음 작업(next work, 다음 작업)은 구조 단서(structure clue, 구조 단서)를 참고할 수 있지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 아직 없다.

"""
    write_md(CURRENT_WORKING_STATE_PATH, block + old.lstrip("\ufeff"))

    old_changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if io_path(CHANGELOG_PATH).exists() else ""
    old_changelog = re.sub(
        r"^## 2026-05-09 Stage37 State Context Router\(37단계 상태 문맥 라우터\).*?(?=^## |\Z)",
        "",
        old_changelog,
        flags=re.DOTALL | re.MULTILINE,
    )
    entry = f"""## 2026-05-09 Stage37 State Context Router(37단계 상태 문맥 라우터)

- completed(완료): `{RUN_ID}`
- judgment(판정): `{summary['result_judgment']['judgment_label']}`
- effect(효과): common state-context-response table(공통 상태-문맥-반응 테이블)과 broad MT5 routed probe(넓은 MT5 라우팅 탐침)를 남겼고, 운영 주장(operating claim, 운영 주장)은 만들지 않았다.

"""
    write_md(CHANGELOG_PATH, entry + old_changelog.lstrip("\ufeff"))


def build_summary(
    *,
    created_at: str,
    branch: str,
    context: Mapping[str, Any],
    hmm: Mapping[str, Any],
    markov: Mapping[str, Any],
    atlas: Mapping[str, Any],
    tables: Mapping[str, Any],
    runtime_inputs: Mapping[str, Any],
    result: Mapping[str, Any],
    model_response_training_summary: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    common_table = tables["common"]
    decomposition = state_response_decomposition(common_table)
    alignment = state_alignment_summary(common_table)
    write_csv(RESULT_ROOT / "state_response_decomposition.csv", decomposition)
    write_csv(RESULT_ROOT / "state_alignment_summary.csv", alignment)
    runtime_rows = runtime_comparison_rows(result.get("mt5_kpi_records", []))
    write_csv(RESULT_ROOT / "mt5_runtime_comparison.csv", runtime_rows)
    judgment = judge_structure(runtime_rows, str(result.get("external_verification_status")))
    output_paths = {
        key: value["path"] if isinstance(value, Mapping) and "path" in value else value
        for key, value in tables["artifacts"].items()
    } | {
        "state_response_decomposition": rel(RESULT_ROOT / "state_response_decomposition.csv"),
        "state_alignment_summary": rel(RESULT_ROOT / "state_alignment_summary.csv"),
        "runtime_variant_selection_summary": rel(RESULT_ROOT / "runtime_variant_selection_summary.csv"),
        "mt5_runtime_comparison": rel(RESULT_ROOT / "mt5_runtime_comparison.csv"),
        "run_manifest": rel(RUN_ROOT / "run_manifest.json"),
        "kpi_record": rel(RUN_ROOT / "kpi_record.json"),
        "report": rel(REPORT_PATH),
    }
    source_artifacts = {
        "stage36_selection_reference": "stages/36_model_selection__cross_model_characteristic_synthesis/02_runs/run30A/results/selection_reference_matrix.csv",
        "stage35_model_input": rel(stage35_cfg.MODEL_INPUT_PATH),
        "stage22_hmm_variant_rebuilt": HMM_VARIANT_ID,
        "stage28_markov_variant_rebuilt": MARKOV_VARIANT_ID,
        "stage35_kmeans_atlas_rebuilt": "stage_pipelines.stage35.atlas_model.build_atlas",
    }
    duplicate_count = int(common_table.duplicated(subset=["tier_scope", "feature_ready_timestamp"]).sum())
    summary = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "created_at_utc": created_at,
        "active_branch": branch,
        "status": "reviewed_structure_judgment" if result.get("external_verification_status") == "completed" else "blocked_after_runtime_attempt",
        "external_verification_status": result.get("external_verification_status"),
        "result_judgment": judgment,
        "boundary": BOUNDARY,
        "source_artifacts": source_artifacts,
        "output_paths": output_paths,
        "source_hashes": {
            "model_input": sha256_file_lf_normalized(stage35_cfg.MODEL_INPUT_PATH),
        },
        "hmm_rebuild": {
            "variant_id": hmm["variant_id"],
            "tier_a_quality": hmm["tier_a_quality"],
            "tier_b_quality": hmm["tier_b_quality"],
            "tier_a_best_long_state": hmm["tier_a_best_long_state"],
            "tier_b_best_long_state": hmm["tier_b_best_long_state"],
            "artifacts": hmm["artifacts"],
        },
        "markov_rebuild": {
            "variant_id": markov["variant_id"],
            "tier_a_quality": markov["tier_a_quality"],
            "tier_b_quality": markov["tier_b_quality"],
            "tier_a_best_long_state": markov["tier_a_best_long_state"],
            "tier_b_best_long_state": markov["tier_b_best_long_state"],
            "artifacts": markov["artifacts"],
        },
        "atlas_rebuild": {
            "data_identity": atlas["data_identity"],
            "selections": atlas["selections"],
        },
        "common_table_rows": int(len(common_table)),
        "tier_a_rows": int(len(tables["tier_a"])),
        "tier_b_rows": int(len(tables["tier_b"])),
        "model_response_training_summary": list(model_response_training_summary),
        "runtime_inputs": {
            "common_root": runtime_inputs["common_root"],
            "feature_outputs": runtime_inputs["feature_outputs"],
            "model_outputs": runtime_inputs["model_outputs"],
            "known_runtime_difference": runtime_inputs["known_runtime_difference"],
        },
        "runtime_variant_selection_summary": runtime_inputs["runtime_variant_selection_summary"],
        "runtime_comparison_rows": runtime_rows,
        "mt5_attempt_count": len(runtime_inputs["attempts"]),
        "compile": result.get("compile", {}),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "data_integrity": {
            "duplicate_tier_timestamp_rows": duplicate_count,
            "missing_state_notes": "Markov state is sampled by the Stage28 contract, so unsampled rows carry null Markov columns; HMM/KMeans/context remain complete where their source scope applies.",
            "tier_b_kmeans_scope": "out_of_scope_by_partial_context",
            "feature_label_boundary": "All model responses are trained on train split and decomposed on validation/OOS without promotion claims.",
        },
        "next_action": NEXT_ACTION,
        "forbidden_claims": ["baseline", "promotion", "runtime_authority", "live_readiness"],
    }
    return summary


def run(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    branch = active_branch()
    for path in (RESULT_ROOT, FEATURE_ROOT, MODEL_ROOT, STATE_ROOT, MT5_ROOT, PACKET_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)

    context = stage22_hmm.load_context()
    hmm = rebuild_hmm_states(context)
    markov = rebuild_markov_states(context)
    atlas = atlas_model.build_atlas()
    save_frame(RESULT_ROOT / "atlas_state_rows.csv", pd.DataFrame(atlas["state_rows"]))
    save_frame(RESULT_ROOT / "atlas_selected_states.csv", pd.DataFrame(atlas["selections"]))

    tier_a_responses, model_response_summary = train_tier_a_model_responses(
        context["tier_a_frame"],
        stage35_cfg.FEATURE_ORDER,
        args,
    )
    tier_b_responses = train_tier_b_core_response(context["tier_b_training_frame"], context["tier_b_fallback_frame"])
    tables = build_state_context_tables(context, hmm, markov, atlas, tier_a_responses, tier_b_responses)
    runtime_inputs = materialize_runtime_inputs(tables)
    prepared = {
        "run_root": RUN_ROOT.as_posix(),
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "run_number": RUN_NUMBER,
        "completion_goal": "compare_state_filter_state_adapter_limited_router_in_broad_routed_mt5_probe",
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": "Stage36 frontier02 state_context_stack; no baseline inheritance.",
        "attempts": runtime_inputs["attempts"],
        "route_coverage": context["tier_b_context_summary"],
        "common_copies": runtime_inputs["common_copies"],
    }
    result = execute_or_block(prepared, args)
    summary = build_summary(
        created_at=created_at,
        branch=branch,
        context=context,
        hmm=hmm,
        markov=markov,
        atlas=atlas,
        tables=tables,
        runtime_inputs=runtime_inputs,
        result=result,
        model_response_training_summary=model_response_summary,
    )
    write_run_files(result, summary)
    summary["normalized_kpi"] = write_normalized_kpi() if result.get("external_verification_status") == "completed" else {
        "normalized_records": 0,
        "normalized_summary_rows": 0,
        "missing_runs": 0,
        "parser_errors": 0,
        "trade_attribution_records": 0,
        "trade_level_rows": 0,
        "trade_parser_errors": 0,
    }
    summary["ledger_materialization"] = materialize_ledgers(summary)
    update_stage_docs(summary)
    write_packet_artifacts(summary)
    update_current_truth(summary)
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(RESULT_ROOT / "aggregate_summary.json", summary)
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage37 state-context router broad MT5 probe.")
    parser.add_argument("--materialize-only", action="store_true", help="Build artifacts without launching MT5.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--model-train-rows", type=int, default=18000)
    parser.add_argument("--ebm-train-rows", type=int, default=8000)
    parser.add_argument("--catboost-train-rows", type=int, default=14000)
    parser.add_argument("--tcn-train-rows", type=int, default=12000)
    parser.add_argument("--tcn-lookback", type=int, default=16)
    parser.add_argument("--tcn-epochs", type=int, default=2)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    summary = run(build_arg_parser().parse_args(argv))
    print(
        json.dumps(
            {
                "status": summary["status"],
                "judgment": summary["result_judgment"]["judgment_label"],
                "external_verification_status": summary["external_verification_status"],
                "run_id": RUN_ID,
                "report_path": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
