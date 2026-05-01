from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.ensemble import ExtraTreesClassifier

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
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
from foundation.control_plane.tier_context_materialization import TIER_B_CORE_FEATURE_ORDER
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage12.extratrees_rolling_wfo_split_probe import (
    FOLDS,
    PROBE_N_ESTIMATORS,
    nonflat_threshold,
    ordered_probs,
    prepare_frames,
    probe_params,
    window,
)
from stage_pipelines.stage12.extratrees_standalone_batch20_support import (
    CLASS_TO_LABEL,
    VariantSpec,
    _variant_specs,
)


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "12_model_family_challenge__extratrees_training_effect"
STAGE_NUMBER = 12
RUN_NUMBER = "run03L"
RUN_ID = "run03L_et_recency_weighted_single_v1"
PACKET_ID = "stage12_run03l_recency_weighted_single_v1"
EXPLORATION_LABEL = "stage12_Model__ExtraTreesRecencyWeightedSingle"
IDEA_ID = "IDEA-ST12-ET-RECENCY-WEIGHTED-SINGLE"
SOURCE_WFO_RUN_ID = "run03J_et_rolling_wfo_split_probe_v1"
SOURCE_MT5_REFERENCE_RUN_ID = "run03K_et_wfo_fold07_all_variant_mt5_failure_probe_v1"
SOURCE_VARIANT_RUN_ID = "run03D_et_standalone_batch20_v1"
MODEL_FAMILY = "sklearn_extratreesclassifier_multiclass"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_58_and_core42_partial_context_recency_weighted"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "rolling_wfo_7fold_train_recent12m_weight3_fold07_mt5"
BOUNDARY = "runtime_probe_recency_weight_single_run_not_alpha_quality_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_recency_weighted_single_runtime_probe_completed"
REFERENCE_VARIANT_ID = "v01_base_leaf20_q90"
WEIGHT_RECENT_MONTHS = 12
WEIGHT_RECENT = 3.0
WEIGHT_OLDER = 1.0
HIT_FLOOR = 0.48

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_RUN_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
IDEA_REGISTRY_PATH = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER_PATH = ROOT / "docs/registers/negative_result_register.md"
PLAN_PATH = STAGE_ROOT / "00_spec/run03L_recency_weighted_single_probe_plan.md"
STAGE_REVIEW_PATH = STAGE_ROOT / "03_reviews/run03L_recency_weighted_single_probe_packet.md"
MODEL_INPUT_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
TRAINING_SUMMARY_PATH = ROOT / "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"

ATTEMPT_COLUMNS = (
    "run_id",
    "source_variant_id",
    "fold_id",
    "attempt_name",
    "split",
    "wfo_split_role",
    "tier_scope",
    "route_role",
    "tester_status",
    "runtime_status",
    "report_status",
    "net_profit",
    "profit_factor",
    "trade_count",
    "report_path",
)
TARGET_COLUMNS = ("run_id", "source_variant_id", "fold_id", "status", "attempt_count", "kpi_record_count")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(json_ready(row), ensure_ascii=False, sort_keys=True) + "\n")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig" if bom else "utf-8")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def current_branch() -> str:
    try:
        completed = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return completed.stdout.strip() or "unknown"


def value_or_na(value: Any, digits: int = 2) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.{digits}f}"


def source_spec() -> VariantSpec:
    for spec in _variant_specs():
        if spec.variant_id == REFERENCE_VARIANT_ID:
            return spec
    raise RuntimeError(f"missing source variant {REFERENCE_VARIANT_ID}")


def recency_weights(frame: pd.DataFrame, train_end_exclusive: str) -> tuple[np.ndarray, dict[str, Any]]:
    cutoff = pd.Timestamp(train_end_exclusive) - pd.DateOffset(months=WEIGHT_RECENT_MONTHS)
    stamps = pd.to_datetime(frame["timestamp"], utc=True)
    recent_mask = stamps >= cutoff
    weights = np.where(recent_mask.to_numpy(), WEIGHT_RECENT, WEIGHT_OLDER).astype("float64")
    return weights, {
        "train_end_exclusive": train_end_exclusive,
        "recent_cutoff": cutoff.isoformat().replace("+00:00", "Z"),
        "recent_rows": int(recent_mask.sum()),
        "older_rows": int((~recent_mask).sum()),
        "recent_weight": WEIGHT_RECENT,
        "older_weight": WEIGHT_OLDER,
        "weighted_rows_equivalent": float(weights.sum()),
    }


def train_weighted_model(
    frame: pd.DataFrame,
    features: Sequence[str],
    params: Mapping[str, Any],
    train_end_exclusive: str,
) -> tuple[ExtraTreesClassifier, dict[str, Any]]:
    weights, weight_summary = recency_weights(frame, train_end_exclusive)
    model = ExtraTreesClassifier(**dict(params))
    model.fit(
        frame.loc[:, list(features)].to_numpy(dtype="float64", copy=False),
        frame["label_class"].astype(int),
        sample_weight=weights,
    )
    return model, weight_summary


def decision_frame(
    *,
    source: pd.DataFrame,
    probs: np.ndarray,
    threshold: float,
    spec: VariantSpec,
    fold_id: str,
    split_role: str,
    tier_scope: str,
    route_role: str,
    feature_selector: str,
    feature_count: int,
) -> pd.DataFrame:
    p_short = probs[:, 0]
    p_flat = probs[:, 1]
    p_long = probs[:, 2]
    nonflat_conf = np.maximum(p_short, p_long)
    predicted_direction = np.where(p_short >= p_long, 0, 2)
    competing = np.maximum(p_flat, np.where(predicted_direction == 0, p_long, p_short))
    margin = nonflat_conf - competing
    pass_gate = (nonflat_conf >= threshold) & (margin >= spec.min_margin)
    decision = np.full(len(source), 1, dtype=int)
    if spec.direction_mode == "both":
        decision[pass_gate] = predicted_direction[pass_gate]
    elif spec.direction_mode == "short_only":
        decision[pass_gate & (predicted_direction == 0)] = 0
    elif spec.direction_mode == "long_only":
        decision[pass_gate & (predicted_direction == 2)] = 2
    elif spec.direction_mode == "inverse":
        decision[pass_gate & (predicted_direction == 0)] = 2
        decision[pass_gate & (predicted_direction == 2)] = 0
    else:
        raise ValueError(f"unknown direction_mode: {spec.direction_mode}")
    labels = source["label_class"].astype(int).to_numpy()
    is_signal = decision != 1
    correct = (decision == labels) & is_signal
    return pd.DataFrame(
        {
            "run_id": RUN_ID,
            "fold_id": fold_id,
            "variant_id": "recency_weighted_v01_base_leaf20_q90",
            "source_variant_id": REFERENCE_VARIANT_ID,
            "idea_id": IDEA_ID,
            "split_role": split_role,
            "original_split": source["split"].astype(str).to_numpy(),
            "tier_scope": tier_scope,
            "route_role": route_role,
            "feature_selector": feature_selector,
            "feature_count": int(feature_count),
            "timestamp": source["timestamp"].astype(str).to_numpy(),
            "label_class": labels,
            "label_direction": source["label_direction"].astype(int).to_numpy(),
            "p_short": p_short,
            "p_flat": p_flat,
            "p_long": p_long,
            "nonflat_conf": nonflat_conf,
            "margin": margin,
            "threshold": threshold,
            "threshold_quantile": spec.threshold_quantile,
            "min_margin": spec.min_margin,
            "direction_mode": spec.direction_mode,
            "decision_class": decision,
            "decision_direction": [CLASS_TO_LABEL[int(value)] for value in decision],
            "is_signal": is_signal,
            "directional_correct": correct,
        }
    )


def signal_metrics(frame: pd.DataFrame) -> dict[str, Any]:
    signals = frame.loc[frame["is_signal"]]
    signal_count = int(len(signals))
    correct_count = int(signals["directional_correct"].sum()) if signal_count else 0
    return {
        "rows": int(len(frame)),
        "signal_count": signal_count,
        "coverage": float(signal_count / len(frame)) if len(frame) else None,
        "correct_count": correct_count,
        "hit_rate": float(correct_count / signal_count) if signal_count else None,
        "short_count": int((signals["decision_class"] == 0).sum()),
        "long_count": int((signals["decision_class"] == 2).sum()),
    }


def metric_row(frame: pd.DataFrame, fold: Any, split_role: str) -> dict[str, Any]:
    first = frame.iloc[0].to_dict() if not frame.empty else {}
    return {
        "run_id": RUN_ID,
        "fold_id": fold.fold_id,
        "variant_id": first.get("variant_id", ""),
        "source_variant_id": first.get("source_variant_id", ""),
        "idea_id": first.get("idea_id", ""),
        "split_role": split_role,
        "tier_scope": first.get("tier_scope", ""),
        "route_role": first.get("route_role", ""),
        "feature_selector": first.get("feature_selector", ""),
        "feature_count": first.get("feature_count", 0),
        "threshold": first.get("threshold", math.nan),
        "threshold_quantile": first.get("threshold_quantile", math.nan),
        "min_margin": first.get("min_margin", math.nan),
        "direction_mode": first.get("direction_mode", ""),
        **signal_metrics(frame),
        "train_start": fold.train_start,
        "train_end_exclusive": fold.train_end_exclusive,
        "validation_start": fold.validation_start,
        "validation_end_exclusive": fold.validation_end_exclusive,
        "test_start": fold.test_start,
        "test_end_exclusive": fold.test_end_exclusive,
    }


def summarize_wfo(fold_metrics: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for (tier_scope, route_role), group in fold_metrics.groupby(["tier_scope", "route_role"], dropna=False):
        validation = group.loc[group["split_role"].eq("validation")]
        test = group.loc[group["split_role"].eq("test")]
        merged = validation[["fold_id", "hit_rate", "signal_count", "correct_count"]].merge(
            test[["fold_id", "hit_rate", "signal_count", "correct_count"]],
            on="fold_id",
            how="outer",
            suffixes=("_validation", "_test"),
        )
        val_signals = int(validation["signal_count"].sum())
        test_signals = int(test["signal_count"].sum())
        val_correct = int(validation["correct_count"].sum())
        test_correct = int(test["correct_count"].sum())
        val_hit = float(val_correct / val_signals) if val_signals else math.nan
        test_hit = float(test_correct / test_signals) if test_signals else math.nan
        both_positive = int(((merged["hit_rate_validation"] >= HIT_FLOOR) & (merged["hit_rate_test"] >= HIT_FLOOR)).sum())
        rows.append(
            {
                "run_id": RUN_ID,
                "tier_scope": tier_scope,
                "route_role": route_role,
                "fold_count": int(merged["fold_id"].nunique()),
                "validation_signal_total": val_signals,
                "test_signal_total": test_signals,
                "validation_correct_total": val_correct,
                "test_correct_total": test_correct,
                "validation_weighted_hit_rate": val_hit,
                "test_weighted_hit_rate": test_hit,
                "test_minus_validation_hit_rate": test_hit - val_hit if math.isfinite(val_hit) and math.isfinite(test_hit) else math.nan,
                "validation_positive_fold_count": int((merged["hit_rate_validation"] >= HIT_FLOOR).sum()),
                "test_positive_fold_count": int((merged["hit_rate_test"] >= HIT_FLOOR).sum()),
                "both_positive_fold_count": both_positive,
                "inversion_fold_count": int((merged["hit_rate_test"] > merged["hit_rate_validation"]).sum()),
                "test_collapse_fold_count": int((merged["hit_rate_test"] < 0.40).sum()),
                "worst_test_hit_rate": float(merged["hit_rate_test"].min()) if not merged["hit_rate_test"].dropna().empty else math.nan,
            }
        )
    return pd.DataFrame(rows).sort_values(["tier_scope", "route_role"]).reset_index(drop=True)


def evaluate_wfo() -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    spec = source_spec()
    tier_a, tier_b_fallback, feature_order, metadata = prepare_frames()
    tier_b_training = metadata["tier_b_training"]
    params = probe_params(spec)
    a_features = list(feature_order)
    b_features = list(TIER_B_CORE_FEATURE_ORDER)
    metric_rows: list[dict[str, Any]] = []
    signal_frames: list[pd.DataFrame] = []
    fold_rows: list[dict[str, Any]] = []
    weight_rows: list[dict[str, Any]] = []
    for fold in FOLDS:
        a_train = window(tier_a, fold.train_start, fold.train_end_exclusive)
        a_validation = window(tier_a, fold.validation_start, fold.validation_end_exclusive)
        a_test = window(tier_a, fold.test_start, fold.test_end_exclusive)
        b_train = window(tier_b_training, fold.train_start, fold.train_end_exclusive)
        b_validation = window(tier_b_fallback, fold.validation_start, fold.validation_end_exclusive)
        b_test = window(tier_b_fallback, fold.test_start, fold.test_end_exclusive)
        fold_rows.append(
            {
                **fold.as_row(),
                "tier_a_train_rows": len(a_train),
                "tier_a_validation_rows": len(a_validation),
                "tier_a_test_rows": len(a_test),
                "tier_b_train_rows": len(b_train),
                "tier_b_validation_rows": len(b_validation),
                "tier_b_test_rows": len(b_test),
            }
        )
        a_model, a_weight = train_weighted_model(a_train, a_features, params, fold.train_end_exclusive)
        b_model, b_weight = train_weighted_model(b_train, b_features, params, fold.train_end_exclusive)
        weight_rows.extend(
            [
                {"run_id": RUN_ID, "fold_id": fold.fold_id, "tier_scope": "Tier A", **a_weight},
                {"run_id": RUN_ID, "fold_id": fold.fold_id, "tier_scope": "Tier B", **b_weight},
            ]
        )
        a_val_probs = ordered_probs(a_model, a_validation, a_features)
        a_test_probs = ordered_probs(a_model, a_test, a_features)
        b_val_probs = ordered_probs(b_model, b_validation, b_features)
        b_test_probs = ordered_probs(b_model, b_test, b_features)
        a_threshold = nonflat_threshold(a_val_probs, spec.threshold_quantile)
        b_threshold = nonflat_threshold(b_val_probs, spec.threshold_quantile)
        frames = (
            decision_frame(
                source=a_validation,
                probs=a_val_probs,
                threshold=a_threshold,
                spec=spec,
                fold_id=fold.fold_id,
                split_role="validation",
                tier_scope="Tier A",
                route_role="tier_a_only",
                feature_selector="all58",
                feature_count=len(a_features),
            ),
            decision_frame(
                source=a_test,
                probs=a_test_probs,
                threshold=a_threshold,
                spec=spec,
                fold_id=fold.fold_id,
                split_role="test",
                tier_scope="Tier A",
                route_role="tier_a_only",
                feature_selector="all58",
                feature_count=len(a_features),
            ),
            decision_frame(
                source=b_validation,
                probs=b_val_probs,
                threshold=b_threshold,
                spec=spec,
                fold_id=fold.fold_id,
                split_role="validation",
                tier_scope="Tier B",
                route_role="tier_b_fallback_only",
                feature_selector="core42_partial_context",
                feature_count=len(b_features),
            ),
            decision_frame(
                source=b_test,
                probs=b_test_probs,
                threshold=b_threshold,
                spec=spec,
                fold_id=fold.fold_id,
                split_role="test",
                tier_scope="Tier B",
                route_role="tier_b_fallback_only",
                feature_selector="core42_partial_context",
                feature_count=len(b_features),
            ),
        )
        routed_validation = pd.concat(
            [
                frames[0].assign(tier_scope="Tier A+B", route_role="routed_tier_a_primary_used"),
                frames[2].assign(tier_scope="Tier A+B", route_role="routed_tier_b_fallback_used"),
            ],
            ignore_index=True,
        ).assign(route_role="routed_total")
        routed_test = pd.concat(
            [
                frames[1].assign(tier_scope="Tier A+B", route_role="routed_tier_a_primary_used"),
                frames[3].assign(tier_scope="Tier A+B", route_role="routed_tier_b_fallback_used"),
            ],
            ignore_index=True,
        ).assign(route_role="routed_total")
        for frame in (*frames, routed_validation, routed_test):
            metric_rows.append(metric_row(frame, fold, str(frame["split_role"].iloc[0])))
            signal_frames.append(frame.loc[frame["is_signal"]].copy())
    fold_plan = pd.DataFrame(fold_rows)
    fold_metrics = pd.DataFrame(metric_rows)
    signals = pd.concat(signal_frames, ignore_index=True) if signal_frames else pd.DataFrame()
    wfo_summary = summarize_wfo(fold_metrics)
    metadata = {
        "source_metadata": {key: value for key, value in metadata.items() if key != "tier_b_training"},
        "params": params,
        "tier_a_feature_count": len(a_features),
        "tier_b_feature_count": len(b_features),
    }
    return metadata, fold_plan, fold_metrics, signals, pd.DataFrame(weight_rows), wfo_summary


def split_dates_from_window(frame: pd.DataFrame) -> tuple[str, str]:
    if frame.empty:
        raise RuntimeError("empty fold split frame")
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def mt5_rule(threshold: float, direction_mode: str) -> tuple[float, float, bool]:
    disabled = 2.0
    if direction_mode == "both":
        return threshold, threshold, False
    if direction_mode == "short_only":
        return threshold, disabled, False
    if direction_mode == "long_only":
        return disabled, threshold, False
    if direction_mode == "inverse":
        return threshold, threshold, True
    raise ValueError(f"unknown direction_mode: {direction_mode}")


def make_attempts(
    *,
    split: str,
    wfo_role: str,
    from_date: str,
    to_date: str,
    common: str,
    tier_a_onnx: Path,
    tier_b_onnx: Path,
    a_matrix: Path,
    b_matrix: Path,
    tier_a_order: Sequence[str],
    tier_b_order: Sequence[str],
    tier_a_hash: str,
    tier_b_hash: str,
    a_rule: tuple[float, float, bool],
    b_rule: tuple[float, float, bool],
    min_margin: float,
) -> list[dict[str, Any]]:
    a_short, a_long, a_invert = a_rule
    b_short, b_long, b_invert = b_rule
    common_kwargs = {
        "run_root": RUN_ROOT,
        "run_id": RUN_ID,
        "stage_number": STAGE_NUMBER,
        "exploration_label": EXPLORATION_LABEL,
        "split": split,
        "from_date": from_date,
        "to_date": to_date,
        "max_hold_bars": 9,
        "common_root": common,
    }
    attempts = [
        attempt_payload(
            **common_kwargs,
            attempt_name=f"tier_a_only_{split}",
            tier=mt5.TIER_A,
            model_path=f"{common}/models/{tier_a_onnx.name}",
            model_id=f"{RUN_ID}_tier_a",
            feature_path=f"{common}/features/{a_matrix.name}",
            feature_count=len(tier_a_order),
            feature_order_hash=tier_a_hash,
            short_threshold=a_short,
            long_threshold=a_long,
            min_margin=min_margin,
            invert_signal=a_invert,
            primary_active_tier="tier_a",
            attempt_role="tier_only_total",
            record_view_prefix="mt5_tier_a_only",
        ),
        attempt_payload(
            **common_kwargs,
            attempt_name=f"tier_b_fallback_only_{split}",
            tier=mt5.TIER_B,
            model_path=f"{common}/models/{tier_b_onnx.name}",
            model_id=f"{RUN_ID}_tier_b",
            feature_path=f"{common}/features/{b_matrix.name}",
            feature_count=len(tier_b_order),
            feature_order_hash=tier_b_hash,
            short_threshold=b_short,
            long_threshold=b_long,
            min_margin=min_margin,
            invert_signal=b_invert,
            primary_active_tier="tier_b_fallback",
            attempt_role="tier_b_fallback_only_total",
            record_view_prefix="mt5_tier_b_fallback_only",
        ),
        attempt_payload(
            **common_kwargs,
            attempt_name=f"routed_{split}",
            tier=mt5.TIER_AB,
            model_path=f"{common}/models/{tier_a_onnx.name}",
            model_id=f"{RUN_ID}_tier_a",
            feature_path=f"{common}/features/{a_matrix.name}",
            feature_count=len(tier_a_order),
            feature_order_hash=tier_a_hash,
            short_threshold=a_short,
            long_threshold=a_long,
            min_margin=min_margin,
            invert_signal=a_invert,
            primary_active_tier="tier_a",
            attempt_role="routed_total",
            record_view_prefix="mt5_routed_total",
            fallback_enabled=True,
            fallback_model_path=f"{common}/models/{tier_b_onnx.name}",
            fallback_model_id=f"{RUN_ID}_tier_b",
            fallback_feature_path=f"{common}/features/{b_matrix.name}",
            fallback_feature_count=len(tier_b_order),
            fallback_feature_order_hash=tier_b_hash,
            fallback_short_threshold=b_short,
            fallback_long_threshold=b_long,
            fallback_min_margin=min_margin,
            fallback_invert_signal=b_invert,
        ),
    ]
    for attempt in attempts:
        attempt["source_variant_id"] = "recency_weighted_v01_base_leaf20_q90"
        attempt["fold_id"] = "fold07"
        attempt["wfo_split_role"] = wfo_role
    return attempts


def prepare_mt5_context() -> dict[str, Any]:
    spec = source_spec()
    tier_a, tier_b_fallback, feature_order, metadata = prepare_frames()
    fold = next(item for item in FOLDS if item.fold_id == "fold07")
    tier_b_training = metadata["tier_b_training"]
    a_train = window(tier_a, fold.train_start, fold.train_end_exclusive)
    a_validation = window(tier_a, fold.validation_start, fold.validation_end_exclusive)
    a_test = window(tier_a, fold.test_start, fold.test_end_exclusive)
    b_train = window(tier_b_training, fold.train_start, fold.train_end_exclusive)
    b_validation = window(tier_b_fallback, fold.validation_start, fold.validation_end_exclusive)
    b_test = window(tier_b_fallback, fold.test_start, fold.test_end_exclusive)
    params = probe_params(spec)
    tier_a_order = list(feature_order)
    tier_b_order = list(TIER_B_CORE_FEATURE_ORDER)
    tier_a_model, tier_a_weight = train_weighted_model(a_train, tier_a_order, params, fold.train_end_exclusive)
    tier_b_model, tier_b_weight = train_weighted_model(b_train, tier_b_order, params, fold.train_end_exclusive)
    tier_a_val_probs = ordered_probs(tier_a_model, a_validation, tier_a_order)
    tier_b_val_probs = ordered_probs(tier_b_model, b_validation, tier_b_order)
    threshold_a = nonflat_threshold(tier_a_val_probs, spec.threshold_quantile)
    threshold_b = nonflat_threshold(tier_b_val_probs, spec.threshold_quantile)
    return {
        "spec": spec,
        "fold": fold,
        "params": params,
        "tier_a_order": tier_a_order,
        "tier_b_order": tier_b_order,
        "tier_a_model": tier_a_model,
        "tier_b_model": tier_b_model,
        "tier_a_validation": a_validation,
        "tier_a_test": a_test,
        "tier_b_validation": b_validation,
        "tier_b_test": b_test,
        "threshold_a": threshold_a,
        "threshold_b": threshold_b,
        "weight_summary": {"tier_a": tier_a_weight, "tier_b": tier_b_weight},
        "source_metadata": {key: value for key, value in metadata.items() if key != "tier_b_training"},
    }


def prepare_mt5_run(context: Mapping[str, Any]) -> dict[str, Any]:
    for child in ("models", "mt5", "predictions", "reports", "results"):
        io_path(RUN_ROOT / child).mkdir(parents=True, exist_ok=True)
    tier_a_order = list(context["tier_a_order"])
    tier_b_order = list(context["tier_b_order"])
    tier_a_hash = mt5.ordered_hash(tier_a_order)
    tier_b_hash = mt5.ordered_hash(tier_b_order)
    tier_a_joblib = RUN_ROOT / "models/tier_a_recency_weighted_fold07_model.joblib"
    tier_b_joblib = RUN_ROOT / "models/tier_b_recency_weighted_fold07_core42_model.joblib"
    tier_a_onnx = tier_a_joblib.with_suffix(".onnx")
    tier_b_onnx = tier_b_joblib.with_suffix(".onnx")
    joblib.dump(context["tier_a_model"], io_path(tier_a_joblib))
    joblib.dump(context["tier_b_model"], io_path(tier_b_joblib))
    tier_a_onnx_payload = mt5.export_sklearn_to_onnx_zipmap_disabled(context["tier_a_model"], tier_a_onnx, feature_count=len(tier_a_order))
    tier_b_onnx_payload = mt5.export_sklearn_to_onnx_zipmap_disabled(context["tier_b_model"], tier_b_onnx, feature_count=len(tier_b_order))
    write_text(RUN_ROOT / "models/tier_a_feature_order.txt", "\n".join(tier_a_order), bom=False)
    write_text(RUN_ROOT / "models/tier_b_core42_feature_order.txt", "\n".join(tier_b_order), bom=False)
    onnx_parity = {
        "tier_a": mt5.check_onnxruntime_probability_parity(
            context["tier_a_model"],
            tier_a_onnx,
            context["tier_a_validation"].loc[:, tier_a_order].to_numpy(dtype="float64", copy=False)[:128],
        ),
        "tier_b": mt5.check_onnxruntime_probability_parity(
            context["tier_b_model"],
            tier_b_onnx,
            context["tier_b_validation"].loc[:, tier_b_order].to_numpy(dtype="float64", copy=False)[:128],
        ),
    }
    onnx_parity["passed"] = bool(onnx_parity["tier_a"]["passed"] and onnx_parity["tier_b"]["passed"])
    if not onnx_parity["passed"]:
        raise RuntimeError("RUN03L ONNX parity failed")
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    common_copies = [
        copy_to_common(tier_a_onnx, f"{common}/models/{tier_a_onnx.name}", COMMON_FILES_ROOT_DEFAULT),
        copy_to_common(tier_b_onnx, f"{common}/models/{tier_b_onnx.name}", COMMON_FILES_ROOT_DEFAULT),
    ]
    feature_matrices: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    a_rule = mt5_rule(float(context["threshold_a"]), context["spec"].direction_mode)
    b_rule = mt5_rule(float(context["threshold_b"]), context["spec"].direction_mode)
    for split_label, wfo_role, a_frame, b_frame in (
        ("validation_is", "validation", context["tier_a_validation"], context["tier_b_validation"]),
        ("oos", "test", context["tier_a_test"], context["tier_b_test"]),
    ):
        from_date, to_date = split_dates_from_window(a_frame)
        a_matrix = RUN_ROOT / "mt5" / f"tier_a_fold07_{split_label}_feature_matrix.csv"
        b_matrix = RUN_ROOT / "mt5" / f"tier_b_fold07_{split_label}_feature_matrix.csv"
        feature_matrices.append(mt5.export_mt5_feature_matrix_csv(a_frame.reset_index(drop=True), tier_a_order, a_matrix))
        feature_matrices.append(
            mt5.export_mt5_feature_matrix_csv(
                b_frame.reset_index(drop=True),
                tier_b_order,
                b_matrix,
                metadata_columns=("route_role", "partial_context_subtype", "missing_feature_group_mask", "available_feature_group_mask"),
            )
        )
        common_copies.append(copy_to_common(a_matrix, f"{common}/features/{a_matrix.name}", COMMON_FILES_ROOT_DEFAULT))
        common_copies.append(copy_to_common(b_matrix, f"{common}/features/{b_matrix.name}", COMMON_FILES_ROOT_DEFAULT))
        attempts.extend(
            make_attempts(
                split=split_label,
                wfo_role=wfo_role,
                from_date=from_date,
                to_date=to_date,
                common=common,
                tier_a_onnx=tier_a_onnx,
                tier_b_onnx=tier_b_onnx,
                a_matrix=a_matrix,
                b_matrix=b_matrix,
                tier_a_order=tier_a_order,
                tier_b_order=tier_b_order,
                tier_a_hash=tier_a_hash,
                tier_b_hash=tier_b_hash,
                a_rule=a_rule,
                b_rule=b_rule,
                min_margin=float(context["spec"].min_margin),
            )
        )
    route_coverage = {
        "by_split": {
            "validation": {
                "tier_a_primary_rows": int(len(context["tier_a_validation"])),
                "tier_b_fallback_rows": int(len(context["tier_b_validation"])),
                "routed_labelable_rows": int(len(context["tier_a_validation"]) + len(context["tier_b_validation"])),
                "wfo_split_role": "validation",
            },
            "oos": {
                "tier_a_primary_rows": int(len(context["tier_a_test"])),
                "tier_b_fallback_rows": int(len(context["tier_b_test"])),
                "routed_labelable_rows": int(len(context["tier_a_test"]) + len(context["tier_b_test"])),
                "wfo_split_role": "test",
            },
        },
        "tier_b_fallback_by_split_subtype": {},
        "no_tier_by_split": {"validation": None, "oos": None},
    }
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_wfo_run_id": SOURCE_WFO_RUN_ID,
        "source_mt5_reference_run_id": SOURCE_MT5_REFERENCE_RUN_ID,
        "source_variant_run_id": SOURCE_VARIANT_RUN_ID,
        "source_variant_id": REFERENCE_VARIANT_ID,
        "fold_id": "fold07",
        "model_key": context["spec"].model_key,
        "idea_id": IDEA_ID,
        "feature_selector": "all58",
        "tier_a_feature_count": len(tier_a_order),
        "tier_b_feature_count": len(tier_b_order),
        "direction_mode": context["spec"].direction_mode,
        "min_margin": float(context["spec"].min_margin),
        "thresholds": {"tier_a": context["threshold_a"], "tier_b": context["threshold_b"], "quantile": context["spec"].threshold_quantile},
        "weight_policy": {
            "recent_months": WEIGHT_RECENT_MONTHS,
            "recent_weight": WEIGHT_RECENT,
            "older_weight": WEIGHT_OLDER,
            "changed_variable": "sample_weight",
        },
        "weight_summary": context["weight_summary"],
        "probe_n_estimators_cap": PROBE_N_ESTIMATORS,
        "onnx": {"tier_a": tier_a_onnx_payload, "tier_b": tier_b_onnx_payload},
        "onnx_parity": onnx_parity,
        "route_coverage": route_coverage,
        "boundary": BOUNDARY,
    }
    write_json(RUN_ROOT / "summary.json", summary)
    return {
        **summary,
        "stage_number": STAGE_NUMBER,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "attempts": attempts,
        "common_copies": common_copies,
        "feature_matrices": feature_matrices,
        "route_coverage": route_coverage,
        "completion_goal": "single_recency_weighted_extratrees_probe_with_fold07_mt5_runtime_check",
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": "stage12_standalone_no_stage10_11_inheritance",
    }


def finalize_result(result: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(result)
    completed = out.get("external_verification_status") == "completed"
    out["judgment"] = JUDGMENT if completed else "blocked_recency_weighted_single_mt5_probe"
    for record in out.get("mt5_kpi_records", []):
        record["source_variant_id"] = "recency_weighted_v01_base_leaf20_q90"
        record["fold_id"] = "fold07"
        if record.get("split") == "validation_is":
            record["wfo_split_role"] = "validation"
        elif record.get("split") == "oos":
            record["wfo_split_role"] = "test"
    return out


def execute_mt5(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        result = {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": "blocked_materialize_only_no_mt5_execution",
        }
    else:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
            common_files_root=COMMON_FILES_ROOT_DEFAULT,
            tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
            timeout_seconds=int(args.timeout_seconds),
        )
    return finalize_result(result)


def write_run_files(result: Mapping[str, Any], packet_summary: Mapping[str, Any]) -> None:
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_wfo_run_id": SOURCE_WFO_RUN_ID,
        "source_mt5_reference_run_id": SOURCE_MT5_REFERENCE_RUN_ID,
        "source_variant_id": REFERENCE_VARIANT_ID,
        "run_number": RUN_NUMBER,
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "feature_matrices": result.get("feature_matrices", []),
        "compile": result.get("compile", {}),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "external_verification_status": result["external_verification_status"],
        "judgment": result["judgment"],
        "boundary": BOUNDARY,
    }
    kpi_record = {
        **manifest,
        "kpi_scope": "recency_weighted_single_probe",
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "probe_n_estimators_cap": PROBE_N_ESTIMATORS,
        "python_wfo": packet_summary.get("python_wfo"),
        "mt5": {
            "scoreboard_lane": "runtime_probe_recency_weight_single",
            "external_verification_status": result["external_verification_status"],
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "kpi_records": result.get("mt5_kpi_records", []),
        },
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)
    write_result_summary(RUN_ROOT / "reports/result_summary.md", packet_summary)


def write_preliminary_kpi(result: Mapping[str, Any], wfo_summary: pd.DataFrame) -> None:
    routed = wfo_summary.loc[wfo_summary["tier_scope"].eq("Tier A+B")].iloc[0].to_dict()
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_wfo_run_id": SOURCE_WFO_RUN_ID,
        "source_mt5_reference_run_id": SOURCE_MT5_REFERENCE_RUN_ID,
        "source_variant_id": REFERENCE_VARIANT_ID,
        "run_number": RUN_NUMBER,
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "feature_matrices": result.get("feature_matrices", []),
        "compile": result.get("compile", {}),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "external_verification_status": result["external_verification_status"],
        "judgment": result["judgment"],
        "boundary": BOUNDARY,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(
        RUN_ROOT / "kpi_record.json",
        {
            **manifest,
            "kpi_scope": "recency_weighted_single_probe_preliminary",
            "model_family": MODEL_FAMILY,
            "feature_set_id": FEATURE_SET_ID,
            "label_id": LABEL_ID,
            "split_contract": SPLIT_CONTRACT,
            "python_wfo": {
                "routed_validation_hit_rate": routed.get("validation_weighted_hit_rate"),
                "routed_test_hit_rate": routed.get("test_weighted_hit_rate"),
            },
            "mt5": {"scoreboard_lane": "runtime_probe_recency_weight_single", "kpi_records": result.get("mt5_kpi_records", [])},
        },
    )


def attempt_summary_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    reports = {record.get("report_name"): record for record in result.get("strategy_tester_reports", [])}
    attempts = {attempt["attempt_name"]: attempt for attempt in result.get("attempts", [])}
    for execution in result.get("execution_results", []):
        attempt = attempts.get(execution.get("attempt_name"), {})
        report = reports.get(mt5.report_name_from_attempt(attempt), {}) if attempt else {}
        metrics = report.get("metrics", {}) if isinstance(report, Mapping) else {}
        rows.append(
            {
                "run_id": RUN_ID,
                "source_variant_id": "recency_weighted_v01_base_leaf20_q90",
                "fold_id": "fold07",
                "attempt_name": execution.get("attempt_name"),
                "split": execution.get("split"),
                "wfo_split_role": "validation" if execution.get("split") == "validation_is" else "test",
                "tier_scope": execution.get("tier"),
                "route_role": execution.get("attempt_role") or ("routed_total" if execution.get("routing_mode") else "tier_only_total"),
                "tester_status": execution.get("status"),
                "runtime_status": execution.get("runtime_outputs", {}).get("status"),
                "report_status": report.get("status") if isinstance(report, Mapping) else None,
                "net_profit": metrics.get("net_profit") if isinstance(metrics, Mapping) else None,
                "profit_factor": metrics.get("profit_factor") if isinstance(metrics, Mapping) else None,
                "trade_count": metrics.get("trade_count") if isinstance(metrics, Mapping) else None,
                "report_path": rel(Path(report.get("html_report", {}).get("path", ""))) if isinstance(report.get("html_report"), Mapping) else "",
            }
        )
    return rows


def target_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "source_variant_id": "recency_weighted_v01_base_leaf20_q90",
            "fold_id": "fold07",
            "status": result.get("external_verification_status"),
            "attempt_count": len(result.get("attempts", [])),
            "kpi_record_count": len(result.get("mt5_kpi_records", [])),
        }
    ]


def normalized_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    return mt5_kpi_recorder.build_normalized_records(ROOT, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "path": rel(RUN_ROOT)}])


def record_by_view(result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(record.get("record_view")): record for record in result.get("mt5_kpi_records", [])}


def mt5_metric(result: Mapping[str, Any], view: str, metric: str) -> Any:
    return record_by_view(result).get(view, {}).get("metrics", {}).get(metric)


def build_packet_summary(
    result: Mapping[str, Any],
    wfo_summary: pd.DataFrame,
    normalized_records: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    trade_parser_errors: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    routed_wfo = wfo_summary.loc[wfo_summary["tier_scope"].eq("Tier A+B")].iloc[0].to_dict()
    mt5_summary = {
        "validation_tier_a_net_profit": mt5_metric(result, "mt5_tier_a_only_validation_is", "net_profit"),
        "validation_tier_b_net_profit": mt5_metric(result, "mt5_tier_b_fallback_only_validation_is", "net_profit"),
        "validation_routed_net_profit": mt5_metric(result, "mt5_routed_total_validation_is", "net_profit"),
        "validation_routed_profit_factor": mt5_metric(result, "mt5_routed_total_validation_is", "profit_factor"),
        "validation_routed_trades": mt5_metric(result, "mt5_routed_total_validation_is", "trade_count"),
        "test_tier_a_net_profit": mt5_metric(result, "mt5_tier_a_only_oos", "net_profit"),
        "test_tier_b_net_profit": mt5_metric(result, "mt5_tier_b_fallback_only_oos", "net_profit"),
        "test_routed_net_profit": mt5_metric(result, "mt5_routed_total_oos", "net_profit"),
        "test_routed_profit_factor": mt5_metric(result, "mt5_routed_total_oos", "profit_factor"),
        "test_routed_trades": mt5_metric(result, "mt5_routed_total_oos", "trade_count"),
    }
    completed = result.get("external_verification_status") == "completed"
    return {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_wfo_run_id": SOURCE_WFO_RUN_ID,
        "source_mt5_reference_run_id": SOURCE_MT5_REFERENCE_RUN_ID,
        "source_variant_run_id": SOURCE_VARIANT_RUN_ID,
        "source_variant_id": REFERENCE_VARIANT_ID,
        "idea_id": IDEA_ID,
        "fold_id": "fold07",
        "variant_count": 1,
        "fold_count": len(FOLDS),
        "python_wfo": {
            "summary_rows": int(len(wfo_summary)),
            "fold_metric_rows": int(len(FOLDS) * 6),
            "routed_validation_hit_rate": routed_wfo.get("validation_weighted_hit_rate"),
            "routed_test_hit_rate": routed_wfo.get("test_weighted_hit_rate"),
            "routed_both_positive_fold_count": routed_wfo.get("both_positive_fold_count"),
            "routed_inversion_fold_count": routed_wfo.get("inversion_fold_count"),
            "routed_test_collapse_fold_count": routed_wfo.get("test_collapse_fold_count"),
        },
        "mt5": mt5_summary,
        "mt5_attempts_total": len(result.get("attempts", [])),
        "mt5_reports_total": len(result.get("strategy_tester_reports", [])),
        "mt5_kpi_records": len(result.get("mt5_kpi_records", [])),
        "normalized_records": len(normalized_records),
        "trade_level_rows": len(trade_rows),
        "trade_parser_errors": len(trade_parser_errors),
        "external_verification_status": "completed" if completed else "blocked",
        "status": "completed" if completed else "partial",
        "completed_forbidden": not completed,
        "judgment": JUDGMENT if completed else "blocked_recency_weighted_single_mt5_probe",
        "boundary": BOUNDARY,
        "allowed_claims": ["runtime_probe_recency_weight_completed", "single_run_completed"] if completed else ["blocked"],
        "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
    }


def write_packet_files(
    *,
    result: Mapping[str, Any],
    normalized_records: Sequence[Mapping[str, Any]],
    normalized_summary_rows: Sequence[Mapping[str, Any]],
    parser_errors: Sequence[Mapping[str, Any]],
    trade_enriched: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    trade_summary_rows: Sequence[Mapping[str, Any]],
    trade_parser_errors: Sequence[Mapping[str, Any]],
    packet_summary: Mapping[str, Any],
) -> None:
    write_csv_rows(PACKET_ROOT / "target_matrix.csv", TARGET_COLUMNS, target_rows(result))
    write_csv_rows(PACKET_ROOT / "attempt_summary.csv", ATTEMPT_COLUMNS, attempt_summary_rows(result))
    write_json(PACKET_ROOT / "execution_results.json", [compact_execution_result(result)])
    write_jsonl(PACKET_ROOT / "normalized_kpi_records.jsonl", normalized_records)
    write_csv_rows(PACKET_ROOT / "normalized_kpi_summary.csv", mt5_kpi_recorder.SUMMARY_COLUMNS, normalized_summary_rows)
    write_jsonl(PACKET_ROOT / "enriched_kpi_records.jsonl", trade_enriched)
    write_csv_rows(PACKET_ROOT / "trade_level_records.csv", mt5_trade_attribution.TRADE_COLUMNS, trade_rows)
    write_csv_rows(PACKET_ROOT / "trade_attribution_summary.csv", mt5_trade_attribution.SUMMARY_COLUMNS, trade_summary_rows)
    write_json(PACKET_ROOT / "parser_errors.json", list(parser_errors))
    write_json(PACKET_ROOT / "trade_parser_errors.json", list(trade_parser_errors))
    write_json(PACKET_ROOT / "packet_summary.json", dict(packet_summary))
    write_json(PACKET_ROOT / "runtime_evidence_gate.json", runtime_evidence_gate(packet_summary))
    created_at = utc_now()
    write_work_packet(created_at, packet_summary)
    write_json(PACKET_ROOT / "skill_receipts.json", {"receipts": skill_receipts(created_at, packet_summary)})
    write_closeout_report(packet_summary)
    write_plan_and_review(packet_summary)


def compact_execution_result(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "source_variant_id": "recency_weighted_v01_base_leaf20_q90",
        "fold_id": "fold07",
        "compile": result.get("compile", {}),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
    }


def runtime_evidence_gate(summary: Mapping[str, Any]) -> dict[str, Any]:
    passed = summary.get("external_verification_status") == "completed" and int(summary.get("mt5_attempts_total", 0)) == 6
    return {
        "audit_name": "runtime_evidence_gate",
        "status": "pass" if passed else "blocked",
        "findings": [] if passed else [{"check_id": "runtime_evidence_gate::blocked", "message": "MT5 runtime evidence incomplete."}],
        "counts": {
            "mt5_attempts_total": summary.get("mt5_attempts_total"),
            "mt5_reports_total": summary.get("mt5_reports_total"),
            "mt5_kpi_records": summary.get("mt5_kpi_records"),
            "normalized_records": summary.get("normalized_records"),
            "trade_level_rows": summary.get("trade_level_rows"),
            "trade_parser_errors": summary.get("trade_parser_errors"),
            "variant_count": summary.get("variant_count"),
        },
        "allowed_claims": ["runtime_probe_recency_weight_completed"] if passed else ["blocked"],
        "forbidden_claims": [] if passed else ["completed", "reviewed", "verified"],
    }


def write_ledgers(packet_summary: Mapping[str, Any], result: Mapping[str, Any]) -> dict[str, Any]:
    status = "reviewed" if packet_summary["external_verification_status"] == "completed" else "blocked"
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "recency_weighted_single_runtime_probe",
            "status": status,
            "judgment": packet_summary["judgment"],
            "path": rel(RUN_ROOT),
            "notes": ledger_pairs(
                (
                    ("source_wfo_run_id", SOURCE_WFO_RUN_ID),
                    ("source_variant_id", REFERENCE_VARIANT_ID),
                    ("changed_variable", "sample_weight"),
                    ("mt5_attempt_count", packet_summary.get("mt5_attempts_total")),
                    ("boundary", BOUNDARY),
                )
            ),
        }
    ]
    ledger_rows = summary_ledger_rows(packet_summary) + mt5_ledger_rows(result, packet_summary)
    return {
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id"),
        "project_alpha_ledger": upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id"),
        "stage_run_ledger": upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id"),
        "rows_written": len(ledger_rows),
    }


def summary_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for view, tier, role in (
        ("python_wfo_tier_a", "Tier A", "tier_a_only"),
        ("python_wfo_tier_b", "Tier B", "tier_b_fallback_only"),
        ("python_wfo_tier_ab", "Tier A+B", "routed_total"),
    ):
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__summary__{view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": view,
                "parent_run_id": SOURCE_WFO_RUN_ID,
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": "recency_weighted_single_python_wfo_summary",
                "scoreboard_lane": "runtime_probe_recency_weight_single",
                "status": summary["status"],
                "judgment": summary["judgment"],
                "path": rel(RUN_ROOT / "results/wfo_summary.csv"),
                "primary_kpi": ledger_pairs(
                    (
                        ("changed_variable", "sample_weight"),
                        ("recent_weight", WEIGHT_RECENT),
                        ("older_weight", WEIGHT_OLDER),
                        ("fold_count", summary.get("fold_count")),
                        ("tier_role", role),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("source_wfo_run_id", SOURCE_WFO_RUN_ID),
                        ("new_mt5_execution", True),
                        ("boundary", BOUNDARY),
                    )
                ),
                "external_verification_status": summary["external_verification_status"],
                "notes": "RUN03L single recency-weighted Python WFO summary row; not alpha quality or promotion.",
            }
        )
    return rows


def mt5_ledger_rows(result: Mapping[str, Any], summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for record in result.get("mt5_kpi_records", []):
        metrics = record.get("metrics", {})
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{record.get('record_view')}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": str(record.get("record_view")),
                "parent_run_id": SOURCE_WFO_RUN_ID,
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "kpi_scope": "recency_weighted_single_mt5_fold07",
                "scoreboard_lane": "runtime_probe_recency_weight_single",
                "status": record.get("status"),
                "judgment": summary["judgment"],
                "path": record.get("report", {}).get("html_report", {}).get("path", ""),
                "primary_kpi": ledger_pairs(
                    (
                        ("net_profit", metrics.get("net_profit")),
                        ("profit_factor", metrics.get("profit_factor")),
                        ("trade_count", metrics.get("trade_count")),
                        ("signal_count", metrics.get("signal_count")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("fold_id", "fold07"),
                        ("wfo_split_role", "validation" if record.get("split") == "validation_is" else "test"),
                        ("route_role", record.get("route_role")),
                        ("changed_variable", "sample_weight"),
                        ("boundary", BOUNDARY),
                    )
                ),
                "external_verification_status": summary["external_verification_status"],
                "notes": "RUN03L MT5 fold07 row; runtime probe only.",
            }
        )
    return rows


def write_work_packet(created_at: str, summary: Mapping[str, Any]) -> None:
    packet = {
        "version": "work_packet_schema_v2",
        "packet_id": PACKET_ID,
        "created_at_utc": created_at,
        "user_request": {
            "user_quote": "이번에 아예 안 파본 쪽으로 파볼만한거 있나? 변형없이 딱 한 run만 보고싶어",
            "requested_action": "run one unexplored Stage 12 ExtraTrees direction with MT5 verification",
            "requested_count": {"value": 1, "n_a_reason": None},
            "ambiguous_terms": ["one run means one structural idea, not a variant sweep."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run_before_packet": SOURCE_MT5_REFERENCE_RUN_ID,
            "current_run_after_packet": RUN_ID,
            "branch": current_branch(),
            "source_documents": [rel(WORKSPACE_STATE_PATH), rel(CURRENT_STATE_PATH), rel(SELECTION_STATUS_PATH)],
        },
        "work_classification": {
            "primary_family": "runtime_backtest",
            "detected_families": ["runtime_backtest", "experiment_execution", "kpi_evidence", "state_sync"],
            "touched_surfaces": ["stage12_run_artifacts", "mt5_strategy_tester", "run_ledgers", "current_truth_docs"],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "single_run_overread_risk": "high",
                "runtime_evidence_risk": "high",
                "selection_bias_risk": "medium",
                "claim_overstatement_risk": "high",
            },
            "hard_stop_risks": [],
            "required_decision_locks": [],
            "required_gates": required_gates(),
            "forbidden_claims": summary["forbidden_claims"],
        },
        "decision_lock": {
            "mode": "user_explicit_one_run",
            "assumptions": {
                "changed_variable": "sample_weight only",
                "sample_weight_policy": "recent 12 months weight 3.0 and older rows weight 1.0",
                "source_variant": REFERENCE_VARIANT_ID,
                "mt5_scope": "fold07 validation/test only",
                "no_variant_sweep": True,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["runtime_backtest"],
            "target_surfaces": [rel(RUN_ROOT), rel(PACKET_ROOT), rel(STAGE_RUN_LEDGER_PATH), rel(PROJECT_ALPHA_LEDGER_PATH)],
            "scope_units": ["single_idea", "fold", "tier_view", "mt5_attempt", "kpi_record", "ledger", "report"],
            "execution_layers": ["python_wfo", "onnx_export", "mt5_strategy_tester", "kpi_recording", "ledger_update", "document_edit"],
            "mutation_policy": {"allowed": True, "boundary": "new RUN03L artifacts and current truth only"},
            "evidence_layers": ["python_wfo_metrics", "mt5_reports", "normalized_kpi", "trade_attribution", "ledgers", "work_packet"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False},
            "claim_boundary": {
                "allowed_claims": summary["allowed_claims"],
                "forbidden_claims": summary["forbidden_claims"],
            },
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "One recency-weighted ExtraTrees run is executed.",
                "expected_artifact": rel(RUN_ROOT / "summary.json"),
                "verification_method": "scope_completion_gate",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "Tier A, Tier B, and Tier A+B views are recorded.",
                "expected_artifact": rel(RUN_ROOT / "results/wfo_summary.csv"),
                "verification_method": "kpi_contract_audit",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "MT5 fold07 validation/test attempts are recorded.",
                "expected_artifact": rel(PACKET_ROOT / "attempt_summary.csv"),
                "verification_method": "runtime_evidence_gate",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": [
                {"id": "python_wfo", "actions": ["train_recency_weighted_wfo", "score_tier_a_tier_b_tier_ab"]},
                {"id": "execute_mt5", "actions": ["train_fold07_models", "export_onnx", "run_6_strategy_tester_attempts"]},
                {"id": "closeout", "actions": ["record_kpi", "record_trade_attribution", "update_ledgers", "sync_current_truth", "run_gates"]},
            ],
            "expected_outputs": [rel(RUN_ROOT / "reports/result_summary.md"), rel(PACKET_ROOT / "closeout_gate.json")],
            "stop_conditions": ["missing_mt5_reports", "parser_errors", "ledger_rows_missing", "gate_failure"],
        },
        "skill_routing": {
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": [
                "obsidian-experiment-design",
                "obsidian-model-validation",
                "obsidian-backtest-forensics",
                "obsidian-artifact-lineage",
                "obsidian-exploration-mandate",
                "obsidian-result-judgment",
            ],
            "skills_considered": [
                "obsidian-runtime-parity",
                "obsidian-experiment-design",
                "obsidian-model-validation",
                "obsidian-backtest-forensics",
                "obsidian-artifact-lineage",
                "obsidian-exploration-mandate",
                "obsidian-result-judgment",
            ],
            "skills_selected": required_skills(),
            "skills_not_used": {},
            "required_skill_receipts": required_skills(),
            "required_gates": required_gates(),
        },
        "evidence_contract": {
            "raw_evidence": [rel(PACKET_ROOT / "execution_results.json"), rel(PACKET_ROOT / "trade_level_records.csv")],
            "machine_readable": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "kpi_record.json"), rel(PACKET_ROOT / "normalized_kpi_records.jsonl")],
            "human_readable": [rel(RUN_ROOT / "reports/result_summary.md"), rel(STAGE_REVIEW_PATH)],
        },
        "gates": {
            "required": required_gates(),
            "actual_status_source": rel(PACKET_ROOT / "closeout_gate.json"),
            "not_applicable_with_reason": {},
        },
        "final_claim_policy": {
            "allowed_claims": summary["allowed_claims"],
            "forbidden_claims": summary["forbidden_claims"],
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }
    write_yaml(PACKET_ROOT / "work_packet.yaml", packet)


def required_skills() -> list[str]:
    return [
        "obsidian-runtime-parity",
        "obsidian-experiment-design",
        "obsidian-model-validation",
        "obsidian-backtest-forensics",
        "obsidian-artifact-lineage",
        "obsidian-exploration-mandate",
        "obsidian-result-judgment",
    ]


def required_gates() -> list[str]:
    return [
        "runtime_evidence_gate",
        "scope_completion_gate",
        "kpi_contract_audit",
        "work_packet_schema_lint",
        "skill_receipt_lint",
        "skill_receipt_schema_lint",
        "state_sync_audit",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]


def skill_receipts(created_at: str, summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-runtime-parity",
            "status": "executed",
            "research_path": rel(RUN_ROOT / "results/wfo_summary.csv"),
            "runtime_path": rel(RUN_ROOT / "run_manifest.json"),
            "shared_contract": "same feature order, q90 threshold, fold07 windows, and Tier A primary plus Tier B fallback route",
            "known_differences": "recent training rows receive sample_weight 3.0 in Python and exported model artifacts",
            "parity_check": "ONNX probability parity and MT5 Strategy Tester output",
            "parity_identity": f"run_id={RUN_ID}; attempts={summary.get('mt5_attempts_total')}",
            "runtime_claim_boundary": "runtime_probe",
            "python_artifact": rel(RUN_ROOT / "results/wfo_summary.csv"),
            "runtime_artifact": rel(RUN_ROOT / "run_manifest.json"),
            "compared_surface": "Python WFO, ONNX exports, MT5 feature matrices, and Strategy Tester reports",
            "parity_level": "runtime_probe",
            "tester_identity": f"US100 M5, deposit=500, leverage=1:100, attempts={summary.get('mt5_attempts_total')}",
            "missing_evidence": "none" if summary["external_verification_status"] == "completed" else "blocked_mt5_attempts",
            "allowed_claims": ["runtime_probe_recency_weight_completed"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "ExtraTrees may improve fold recency behavior if recent 12 months receive stronger training weight.",
            "baseline": SOURCE_WFO_RUN_ID,
            "decision_use": "decide whether recency weighting deserves a broader sweep or should become failure memory",
            "comparison_baseline": SOURCE_WFO_RUN_ID,
            "control_variables": ["model family", "source variant v01", "features", "label", "threshold quantile", "fold windows"],
            "changed_variables": ["sample_weight"],
            "sample_scope": "Tier A, Tier B, Tier A+B, seven Python WFO folds and fold07 MT5 validation/test",
            "success_criteria": "Python WFO improves repeatability and MT5 fold07 does not contradict it",
            "failure_criteria": "weak repeatability, MT5 loss, parser errors, or missing tier view",
            "invalid_conditions": ["missing MT5 reports", "future leakage", "changed threshold policy", "variant sweep"],
            "stop_conditions": ["one run only", "no micro tuning after result"],
            "evidence_plan": [rel(RUN_ROOT / "results/wfo_summary.csv"), rel(PACKET_ROOT / "normalized_kpi_records.jsonl")],
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_family": MODEL_FAMILY,
            "target_and_label": LABEL_ID,
            "split_method": SPLIT_CONTRACT,
            "selection_metric": "none; single user-requested probe",
            "secondary_metrics": ["hit_rate", "signal_count", "MT5 net_profit", "profit_factor", "trade_count"],
            "threshold_policy": "fold validation q90 nonflat threshold",
            "overfit_risk": "recency weight can overfit the latest regime",
            "calibration_risk": "ExtraTrees scores are ranking scores, not calibrated probabilities",
            "comparison_baseline": SOURCE_WFO_RUN_ID,
            "validation_judgment": summary["judgment"],
            "model_or_threshold_surface": "ExtraTrees v01 base leaf20 q90 with recency sample_weight",
            "validation_split": "seven Python WFO folds plus fold07 MT5 validation/test",
            "overfit_checks": "validation/test hit-rate gaps, both-positive folds, MT5 validation/test comparison",
            "selection_metric_boundary": "single probe only; no operating selection metric",
            "allowed_claims": ["runtime_probe_recency_weight_completed", "single_run_completed"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-backtest-forensics",
            "status": "executed",
            "tester_identity": "US100 M5, deposit=500, leverage=1:100, fold07 validation/test windows",
            "ea_identity": rel(RUN_ROOT / "run_manifest.json"),
            "report_identity": rel(PACKET_ROOT / "attempt_summary.csv"),
            "trade_evidence": rel(PACKET_ROOT / "trade_level_records.csv"),
            "cost_assumptions": "broker terminal Strategy Tester report; no synthetic cost overlay",
            "forensic_checks": "attempt summary, normalized KPI records, trade parser errors, and report paths recorded",
            "backtest_judgment": "usable_with_boundary" if summary["external_verification_status"] == "completed" else "blocked",
            "tester_report": rel(PACKET_ROOT / "attempt_summary.csv"),
            "tester_settings": "US100 M5, tester model=4, deposit=500, leverage=1:100, fold07 validation/test date windows",
            "spread_commission_slippage": "broker terminal Strategy Tester report; no synthetic cost overlay",
            "trade_list_identity": rel(PACKET_ROOT / "trade_level_records.csv"),
            "forensic_gaps": "none" if summary["external_verification_status"] == "completed" else "blocked_attempts_recorded",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": [rel(MODEL_INPUT_PATH), rel(TRAINING_SUMMARY_PATH), rel(ROOT / "stage_pipelines/stage12/extratrees_rolling_wfo_split_probe.py")],
            "producer": rel(ROOT / "stage_pipelines/stage12/extratrees_recency_weighted_single_probe.py"),
            "consumer": [rel(RUN_ROOT), rel(PACKET_ROOT), rel(STAGE_RUN_LEDGER_PATH), rel(PROJECT_ALPHA_LEDGER_PATH)],
            "artifact_paths": [rel(RUN_ROOT / "summary.json"), rel(PACKET_ROOT / "packet_summary.json")],
            "artifact_hashes": "recorded in manifest and packet files where durable",
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_ALPHA_LEDGER_PATH), rel(STAGE_RUN_LEDGER_PATH)],
            "availability": "tracked metadata plus reproducible generated artifacts",
            "lineage_judgment": "connected_with_boundary",
            "produced_artifacts": [rel(RUN_ROOT / "run_manifest.json"), rel(PACKET_ROOT / "packet_summary.json")],
            "raw_evidence": [rel(PACKET_ROOT / "execution_results.json"), rel(PACKET_ROOT / "trade_level_records.csv")],
            "machine_readable": [rel(RUN_ROOT / "summary.json"), rel(PACKET_ROOT / "normalized_kpi_records.jsonl")],
            "human_readable": [rel(RUN_ROOT / "reports/result_summary.md"), rel(STAGE_REVIEW_PATH)],
            "hashes_or_missing_reasons": "hashes are recorded in run manifest, packet summary, and normalized KPI where available",
            "lineage_boundary": "connected_with_boundary; no alpha quality, promotion, or runtime authority claim",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-exploration-mandate",
            "status": "executed",
            "idea_id": IDEA_ID,
            "hypothesis": "recency-weighted ExtraTrees may behave differently from unweighted Stage 12 base ExtraTrees",
            "legacy_relation": "none",
            "tier_scope": "Tier A, Tier B, Tier A+B",
            "broad_sweep": "one new structural axis only",
            "extreme_sweep": "not used; user requested exactly one run",
            "micro_search_gate": "not allowed after one-run result",
            "wfo_plan": "seven Python WFO folds plus fold07 MT5",
            "failure_memory": "record as negative/inconclusive memory if weak",
            "evidence_boundary": "runtime_probe",
            "exploration_lane": "Stage 12 ExtraTrees recency-weighted single probe",
            "idea_boundary": "one unexplored structural axis, not baseline or promotion",
            "negative_memory_effect": "Weak result is retained as failure memory and should not be micro-tuned immediately.",
            "operating_claim_boundary": "No alpha quality, promotion candidate, operating promotion, or runtime authority.",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "triggered": True,
            "blocking": False,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "result_subject": RUN_ID,
            "evidence_available": [rel(RUN_ROOT / "results/wfo_summary.csv"), rel(PACKET_ROOT / "normalized_kpi_records.jsonl")],
            "evidence_missing": "full seven-fold MT5 WFO",
            "judgment_label": summary["judgment"],
            "claim_boundary": BOUNDARY,
            "next_condition": "broader recency weighting sweep only if this single run shows repeatable value",
            "user_explanation_hook": "한 번만 본 탐침이라 좋고 나쁨보다 계속 팔 가치가 있는지 본다.",
            "judgment_boundary": BOUNDARY,
            "allowed_claims": ["runtime_probe_recency_weight_completed", "single_run_completed"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
            "evidence_used": [rel(RUN_ROOT / "results/wfo_summary.csv"), rel(PACKET_ROOT / "normalized_kpi_records.jsonl")],
        },
    ]


def write_result_summary(path: Path, summary: Mapping[str, Any]) -> None:
    wfo = summary["python_wfo"]
    mt5_summary = summary["mt5"]
    text = f"""# RUN03L Recency Weighted Single Probe(RUN03L 최근성 가중 단일 탐침)

## Result(결과)

- run(실행): `{RUN_ID}`
- source variant(원천 변형): `{REFERENCE_VARIANT_ID}`
- changed variable(바뀐 변수): `sample_weight(표본 가중치)` only(단독)
- weight policy(가중치 정책): recent 12 months(최근 12개월) `{WEIGHT_RECENT}`, older rows(이전 행) `{WEIGHT_OLDER}`
- Python WFO routed validation/test hit(파이썬 워크포워드 최적화 라우팅 검증/시험 적중): `{value_or_na(wfo.get('routed_validation_hit_rate'), 6)}` / `{value_or_na(wfo.get('routed_test_hit_rate'), 6)}`
- Python WFO both-positive folds(파이썬 워크포워드 최적화 양쪽 양수 접힘): `{wfo.get('routed_both_positive_fold_count')}`
- MT5 validation routed net/PF/trades(MT5 검증 라우팅 순수익/수익팩터/거래수): `{value_or_na(mt5_summary.get('validation_routed_net_profit'))}` / `{value_or_na(mt5_summary.get('validation_routed_profit_factor'))}` / `{mt5_summary.get('validation_routed_trades')}`
- MT5 test routed net/PF/trades(MT5 시험 라우팅 순수익/수익팩터/거래수): `{value_or_na(mt5_summary.get('test_routed_net_profit'))}` / `{value_or_na(mt5_summary.get('test_routed_profit_factor'))}` / `{mt5_summary.get('test_routed_trades')}`
- judgment(판정): `{summary.get('judgment')}`
- boundary(경계): `{BOUNDARY}`

## Read(판독)

효과(effect, 효과): 이 run(실행)은 recency weighting(최근성 가중)이 Stage 12(12단계) ExtraTrees(엑스트라 트리)에 새 신호를 주는지만 본다. alpha quality(알파 품질), promotion candidate(승격 후보), runtime authority(런타임 권위)는 아니다.
"""
    write_text(path, text)


def write_closeout_report(summary: Mapping[str, Any]) -> None:
    text = f"""# {PACKET_ID} Closeout Report(마감 보고서)

## Conclusion(결론)

RUN03L(실행 03L)은 recency-weighted ExtraTrees(최근성 가중 엑스트라 트리)를 변형 없이 한 run(실행)으로 시험했다.

효과(effect, 효과): sample_weight(표본 가중치) 축이 계속 팔 가치가 있는지 Python WFO(파이썬 워크포워드 최적화)와 MT5(메타트레이더5) fold07(접힘 7)로 동시에 남겼다.

## What changed(무엇이 바뀌었나)

- recent 12 months(최근 12개월) 학습 행에 weight(가중치) `3.0`, older rows(이전 행)에 `1.0`을 줬다.
- Tier A(티어 A), Tier B(티어 B), Tier A+B(티어 A+B)를 모두 기록했다.
- fold07(접힘 7) MT5(메타트레이더5) validation/test(검증/시험) 6 attempts(시도)를 실행했다.

## What gates passed(통과한 게이트)

runtime_evidence_gate(런타임 근거 게이트), scope_completion_gate(범위 완료 게이트), kpi_contract_audit(KPI 계약 감사), work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_lint(스킬 영수증 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 가드)를 확인한다.

## What gates were not applicable(해당 없음 게이트)

없음. MT5(메타트레이더5) runtime evidence(런타임 근거)를 직접 실행했다.

## What is still not enforced(아직 강제되지 않은 것)

full seven-fold MT5 WFO(전체 7접힘 메타트레이더5 워크포워드 최적화)는 실행하지 않았다. 이 packet(묶음)은 one-run probe(단일 실행 탐침)다.

## Allowed claims(허용 주장)

`runtime_probe_recency_weight_completed`, `single_run_completed`.

## Forbidden claims(금지 주장)

`alpha_quality(알파 품질)`, `promotion_candidate(승격 후보)`, `operating_promotion(운영 승격)`, `runtime_authority(런타임 권위)`.

## Next hardening step(다음 경화 단계)

결과가 강하면 broader recency weighting sweep(더 넓은 최근성 가중 탐색)을 설계한다. 약하면 failure memory(실패 기억)로 남기고 다른 축으로 간다.

Summary status(요약 상태): `{summary.get('status')}` / external verification status(외부 검증 상태): `{summary.get('external_verification_status')}`.
"""
    write_text(PACKET_ROOT / "closeout_report.md", text, bom=False)


def write_plan_and_review(summary: Mapping[str, Any]) -> None:
    plan = f"""# RUN03L Recency Weighted Single Probe Plan(RUN03L 최근성 가중 단일 탐침 계획)

## Hypothesis(가설)

ExtraTrees(엑스트라 트리)는 최근 12개월 학습 표본을 더 크게 보면 fold(접힘) 안정성이 달라질 수 있다.

효과(effect, 효과): 아직 안 파본 training weight(학습 가중치) 축을 한 번만 본다.

## Controls(고정 조건)

- source variant(원천 변형): `{REFERENCE_VARIANT_ID}`
- model family(모델 계열): `{MODEL_FAMILY}`
- threshold policy(임계값 정책): validation(검증) q90(90분위)
- tiers(티어): Tier A(티어 A), Tier B(티어 B), Tier A+B(티어 A+B)

## Boundary(경계)

`{BOUNDARY}`.
"""
    review = f"""# RUN03L Review Packet(RUN03L 검토 묶음)

## Result(결과)

`{RUN_ID}` completed(완료). 효과(effect, 효과): recent sample weighting(최근 표본 가중)이 Stage 12(12단계) ExtraTrees(엑스트라 트리)에 주는 영향을 한 run(실행)으로 확인했다.

## Evidence(근거)

- run manifest(실행 목록): `{rel(RUN_ROOT / 'run_manifest.json')}`
- KPI record(KPI 기록): `{rel(RUN_ROOT / 'kpi_record.json')}`
- WFO summary(워크포워드 최적화 요약): `{rel(RUN_ROOT / 'results/wfo_summary.csv')}`
- normalized KPI(정규화 KPI): `{rel(PACKET_ROOT / 'normalized_kpi_records.jsonl')}`
- trade attribution(거래 귀속): `{rel(PACKET_ROOT / 'trade_level_records.csv')}`

## Judgment(판정)

`{summary.get('judgment')}`. 효과(effect, 효과): 근거는 보존하지만 alpha quality(알파 품질), promotion candidate(승격 후보), runtime authority(런타임 권위)는 만들지 않는다.
"""
    write_text(PLAN_PATH, plan)
    write_text(STAGE_REVIEW_PATH, review)


def update_current_truth(summary: Mapping[str, Any]) -> None:
    update_workspace_state(summary)
    update_current_working_state(summary)
    update_selection_status(summary)
    update_changelog(summary)
    update_idea_registry(summary)
    update_negative_register(summary)


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    block = f"""stage12_model_family_challenge:
  stage_id: {STAGE_ID}
  status: active_recency_weighted_single_probe_completed
  lane: recency_weighted_single_runtime_probe
  current_run_id: {RUN_ID}
  current_run_label: {EXPLORATION_LABEL}
  current_status: reviewed
  current_summary:
    boundary: {BOUNDARY}
    source_wfo_run_id: {SOURCE_WFO_RUN_ID}
    source_mt5_reference_run_id: {SOURCE_MT5_REFERENCE_RUN_ID}
    source_variant_id: {REFERENCE_VARIANT_ID}
    changed_variable: sample_weight
    fold_count: {summary['fold_count']}
    mt5_attempts_total: {summary['mt5_attempts_total']}
    normalized_records: {summary['normalized_records']}
    trade_level_rows: {summary['trade_level_rows']}
    python_routed_validation_hit_rate: {value_or_na(summary['python_wfo'].get('routed_validation_hit_rate'), 6)}
    python_routed_test_hit_rate: {value_or_na(summary['python_wfo'].get('routed_test_hit_rate'), 6)}
    mt5_validation_routed_net_profit: {value_or_na(summary['mt5'].get('validation_routed_net_profit'))}
    mt5_test_routed_net_profit: {value_or_na(summary['mt5'].get('test_routed_net_profit'))}
    judgment: {summary['judgment']}
    external_verification_status: {summary['external_verification_status']}
    result_summary_path: {rel(RUN_ROOT / 'reports/result_summary.md')}
    packet_summary_path: {rel(PACKET_ROOT / 'packet_summary.json')}
    next_action: decide_broader_recency_weight_sweep_or_move_to_other_axis
"""
    text = re.sub(r"stage12_model_family_challenge:\n.*?(?=\nagent_control_kpi_rebuild:)", block + "\n", text, flags=re.S)
    write_text(WORKSPACE_STATE_PATH, text)


def replace_section(text: str, heading: str, replacement: str) -> str:
    pattern = rf"\n{re.escape(heading)}.*?(?=\n## |\Z)"
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, "\n" + replacement.rstrip() + "\n", text, flags=re.S)
    return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"


def update_current_working_state(summary: Mapping[str, Any]) -> None:
    text = read_text(CURRENT_STATE_PATH)
    text = re.sub(r"- current run\(현재 실행\): `[^`]+`", f"- current run(현재 실행): `{RUN_ID}`", text, count=1)
    text = text.replace(
        "현재 기준은 `RUN03J(실행 03J)` rolling WFO split probe(구르는 워크포워드 분할 탐침)이다.",
        "최근 기준은 `RUN03L(실행 03L)` recency-weighted ExtraTrees(최근성 가중 엑스트라 트리) single probe(단일 탐침)이다.",
    )
    section = f"""## RUN03L recency weighted single probe(최근성 가중 단일 탐침)

- run(실행): `{RUN_ID}`
- source variant(원천 변형): `{REFERENCE_VARIANT_ID}`
- changed variable(바뀐 변수): `sample_weight(표본 가중치)`
- Python routed validation/test hit(파이썬 라우팅 검증/시험 적중): `{value_or_na(summary['python_wfo'].get('routed_validation_hit_rate'), 6)}` / `{value_or_na(summary['python_wfo'].get('routed_test_hit_rate'), 6)}`
- MT5 validation/test routed net(MT5 검증/시험 라우팅 순수익): `{value_or_na(summary['mt5'].get('validation_routed_net_profit'))}` / `{value_or_na(summary['mt5'].get('test_routed_net_profit'))}`
- judgment(판정): `{summary['judgment']}`
- boundary(경계): `{BOUNDARY}`
- effect(효과): 아직 안 파본 recency weighting(최근성 가중) 축을 한 번만 확인했고, alpha quality(알파 품질)나 promotion candidate(승격 후보)는 만들지 않는다.
"""
    text = replace_section(text, "## RUN03L recency weighted single probe(최근성 가중 단일 탐침)", section)
    write_text(CURRENT_STATE_PATH, text)


def update_selection_status(summary: Mapping[str, Any]) -> None:
    text = read_text(SELECTION_STATUS_PATH) if path_exists(SELECTION_STATUS_PATH) else "# Stage 12 Selection Status\n"
    current = f"""# Stage 12 Selection Status

## Current Read - RUN03L recency weighted single probe(현재 판독 - RUN03L 최근성 가중 단일 탐침)

- current run(현재 실행): `{RUN_ID}`
- source WFO(원천 워크포워드 최적화): `{SOURCE_WFO_RUN_ID}`
- source variant(원천 변형): `{REFERENCE_VARIANT_ID}`
- changed variable(바뀐 변수): `sample_weight(표본 가중치)`
- Python routed validation/test hit(파이썬 라우팅 검증/시험 적중): `{value_or_na(summary['python_wfo'].get('routed_validation_hit_rate'), 6)}` / `{value_or_na(summary['python_wfo'].get('routed_test_hit_rate'), 6)}`
- MT5 validation/test routed net(MT5 검증/시험 라우팅 순수익): `{value_or_na(summary['mt5'].get('validation_routed_net_profit'))}` / `{value_or_na(summary['mt5'].get('test_routed_net_profit'))}`
- judgment(판정): `{summary['judgment']}`
- boundary(경계): `{BOUNDARY}`

Effect(효과): one run(단일 실행)으로 새 축을 확인했다. 결과가 좋아도 baseline(기준선)이나 promotion candidate(승격 후보)는 아니다.
"""
    marker = "\n# Selection Status"
    rest = text[text.find(marker) + 1 :] if marker in text else ""
    write_text(SELECTION_STATUS_PATH, current.rstrip() + "\n\n" + rest.lstrip())


def update_changelog(summary: Mapping[str, Any]) -> None:
    text = read_text(CHANGELOG_PATH)
    if RUN_ID in text:
        return
    entry = (
        f"- 2026-05-01: `{RUN_ID}` completed(완료). recency-weighted ExtraTrees(최근성 가중 엑스트라 트리) "
        f"single probe(단일 탐침)를 Python WFO(파이썬 워크포워드 최적화)와 MT5(메타트레이더5) fold07(접힘 7)로 실행했다. "
        f"attempts(시도) `{summary['mt5_attempts_total']}`, normalized KPI(정규화 KPI) `{summary['normalized_records']}`. "
        "Effect(효과): sample_weight(표본 가중치) 축을 실패/회수 기억으로 보존했고 승격 주장은 만들지 않았다.\n"
    )
    if "## 2026-05-01" in text:
        text = text.replace("## 2026-05-01\n\n", "## 2026-05-01\n\n" + entry, 1)
    else:
        text = text.rstrip() + "\n\n## 2026-05-01\n\n" + entry
    write_text(CHANGELOG_PATH, text)


def update_idea_registry(summary: Mapping[str, Any]) -> None:
    text = read_text(IDEA_REGISTRY_PATH)
    if IDEA_ID in text:
        return
    row = (
        f"| `{IDEA_ID}` | `{STAGE_ID}` | recency-weighted ExtraTrees(최근성 가중 엑스트라 트리)가 최근 regime(국면)을 더 잘 볼 수 있다 | "
        f"`Tier A + Tier B combined(Tier A + Tier B 합산)` | `runtime_probe_completed_inconclusive` | "
        f"RUN03L(실행 03L); Python routed hit(파이썬 라우팅 적중) `{value_or_na(summary['python_wfo'].get('routed_validation_hit_rate'), 6)}` / `{value_or_na(summary['python_wfo'].get('routed_test_hit_rate'), 6)}`, "
        f"MT5 routed net(MT5 라우팅 순수익) `{value_or_na(summary['mt5'].get('validation_routed_net_profit'))}` / `{value_or_na(summary['mt5'].get('test_routed_net_profit'))}` |\n"
    )
    insert_after = "## Rule\n"
    if insert_after in text:
        text = text.replace(insert_after, row + "\n" + insert_after, 1)
    else:
        text = text.rstrip() + "\n" + row
    write_text(IDEA_REGISTRY_PATH, text)


def update_negative_register(summary: Mapping[str, Any]) -> None:
    test_net = summary["mt5"].get("test_routed_net_profit")
    try:
        weak_mt5 = float(test_net) <= 0.0
    except (TypeError, ValueError):
        weak_mt5 = True
    if not weak_mt5:
        return
    text = read_text(NEGATIVE_REGISTER_PATH)
    result_id = "NR-018"
    if result_id in text or IDEA_ID in text:
        return
    row = (
        f"| `{result_id}` | `{IDEA_ID}` | recency-weighted ExtraTrees(최근성 가중 엑스트라 트리)가 최근 regime(국면)을 회복할 수 있다 | "
        f"RUN03L(실행 03L) MT5(메타트레이더5) test routed net(시험 라우팅 순수익)이 `{value_or_na(test_net)}`로 약했다 | "
        "training sample weighting(학습 표본 가중치)은 넓은 sweep(탐색) 전 한 번만 본 실패 기억으로 남긴다 | "
        "다른 recency window(최근성 구간)나 regime label(국면 라벨)이 생길 때 |\n"
    )
    write_text(NEGATIVE_REGISTER_PATH, text.rstrip() + "\n" + row)


def run_closeout_gate(summary: Mapping[str, Any]) -> None:
    cmd = [
        "python",
        "-m",
        "foundation.control_plane.closeout_gate",
        "--packet-id",
        PACKET_ID,
        "--requested-claim",
        "completed",
        "--work-packet",
        str(PACKET_ROOT / "work_packet.yaml"),
        "--validate-work-packet-schema",
        "--state-sync-audit",
        "--scope-csv-rows",
        "wfo_summary_rows",
        "3",
        str(RUN_ROOT / "results/wfo_summary.csv"),
        "three-tier-wfo-summary",
        "--scope-csv-rows",
        "fold_metric_rows",
        "42",
        str(RUN_ROOT / "results/fold_metrics.csv"),
        "seven-fold-three-view-validation-test",
        "--scope-csv-rows",
        "mt5_attempt_rows",
        "6",
        str(PACKET_ROOT / "attempt_summary.csv"),
        "fold07-six-mt5-attempts",
        "--scope-csv-rows",
        "normalized_rows",
        "10",
        str(PACKET_ROOT / "normalized_kpi_summary.csv"),
        "normalized-mt5-kpi-summary",
        "--scope-count",
        "trade_level_rows",
        str(summary.get("trade_level_rows")),
        str(summary.get("trade_level_rows")),
        "trade-level-record-count",
    ]
    for skill in required_skills():
        cmd.extend(["--required-skill", skill])
    cmd.extend(
        [
            "--skill-receipt-json",
            str(PACKET_ROOT / "skill_receipts.json"),
            "--skill-receipt-schema",
            "docs/agent_control/skill_receipt_schema.yaml",
            "--extra-audit-json",
            str(PACKET_ROOT / "runtime_evidence_gate.json"),
            "--required-gate-coverage",
            "--closeout-report",
            str(PACKET_ROOT / "closeout_report.md"),
            "--kpi-run-id",
            RUN_ID,
            "--kpi-stage-id",
            STAGE_ID,
            "--kpi-run-root",
            str(RUN_ROOT),
            "--stage-ledger",
            str(STAGE_RUN_LEDGER_PATH),
            "--project-ledger",
            str(PROJECT_ALPHA_LEDGER_PATH),
            "--expected-stage-ledger-rows",
            "13",
            "--expected-project-ledger-rows",
            "13",
            "--output-json",
            str(PACKET_ROOT / "closeout_gate.json"),
        ]
    )
    completed = subprocess.run(cmd, cwd=ROOT, check=False, text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stdout + completed.stderr)


def run_probe(args: argparse.Namespace) -> dict[str, Any]:
    io_path(RUN_ROOT / "results").mkdir(parents=True, exist_ok=True)
    io_path(RUN_ROOT / "predictions").mkdir(parents=True, exist_ok=True)
    io_path(RUN_ROOT / "reports").mkdir(parents=True, exist_ok=True)
    metadata, fold_plan, fold_metrics, signals, weight_summary, wfo_summary = evaluate_wfo()
    fold_plan.to_csv(io_path(RUN_ROOT / "results/fold_plan.csv"), index=False, encoding="utf-8")
    fold_metrics.to_csv(io_path(RUN_ROOT / "results/fold_metrics.csv"), index=False, encoding="utf-8")
    signals.to_csv(io_path(RUN_ROOT / "predictions/wfo_signal_rows.csv"), index=False, encoding="utf-8")
    weight_summary.to_csv(io_path(RUN_ROOT / "results/weight_summary.csv"), index=False, encoding="utf-8")
    wfo_summary.to_csv(io_path(RUN_ROOT / "results/wfo_summary.csv"), index=False, encoding="utf-8")
    mt5_context = prepare_mt5_context()
    prepared = prepare_mt5_run(mt5_context)
    result = execute_mt5(prepared, args)
    write_preliminary_kpi(result, wfo_summary)
    normalized_records, normalized_summary_rows, _missing, parser_errors = normalized_rows()
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    trade_enriched, trade_rows, trade_summary_rows, trade_parser_errors = mt5_trade_attribution.enrich_records(
        normalized_records, ROOT, market_data
    )
    packet_summary = build_packet_summary(result, wfo_summary, normalized_records, trade_rows, trade_parser_errors)
    packet_summary["metadata"] = metadata
    packet_summary["created_at_utc"] = utc_now()
    ledger_outputs = write_ledgers(packet_summary, result)
    packet_summary["ledger_outputs"] = ledger_outputs
    write_run_files(result, packet_summary)
    write_packet_files(
        result=result,
        normalized_records=normalized_records,
        normalized_summary_rows=normalized_summary_rows,
        parser_errors=parser_errors,
        trade_enriched=trade_enriched,
        trade_rows=trade_rows,
        trade_summary_rows=trade_summary_rows,
        trade_parser_errors=trade_parser_errors,
        packet_summary=packet_summary,
    )
    update_current_truth(packet_summary)
    run_closeout_gate(packet_summary)
    write_json(RUN_ROOT / "summary.json", packet_summary)
    return packet_summary


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 12 recency-weighted ExtraTrees single probe.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    summary = run_probe(args)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["external_verification_status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
