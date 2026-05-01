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
    read_csv_rows,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.control_plane.mt5_kpi_records import build_mt5_kpi_records
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
RUN_NUMBER = "run03R"
RUN_ID = "run03R_et_gap_overnight_context_probe_v1"
PACKET_ID = "stage12_run03r_gap_overnight_context_probe_v1"
EXPLORATION_LABEL = "stage12_Model__ExtraTreesGapOvernightContext"
IDEA_ID = "IDEA-ST12-ET-GAP-OVERNIGHT-CONTEXT"
SOURCE_WFO_RUN_ID = "run03J_et_rolling_wfo_split_probe_v1"
SOURCE_RECENCY_RUN_ID = "run03L_et_recency_weighted_single_v1"
SOURCE_VARIANT_RUN_ID = "run03D_et_standalone_batch20_v1"
REFERENCE_VARIANT_ID = "v01_base_leaf20_q90"
MODEL_FAMILY = "sklearn_extratreesclassifier_multiclass"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_58_and_core42_partial_context_gap_overnight_context"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "rolling_wfo_fold01_to_fold06_gap_overnight_context_buckets_mt5_fold05_no_fold07"
BOUNDARY = "runtime_probe_gap_overnight_context_not_alpha_quality_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_gap_overnight_context_runtime_probe_completed"
HIT_FLOOR = 0.48
MT5_FOLD_ID = "fold05"

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
PLAN_PATH = STAGE_ROOT / "00_spec/run03R_gap_overnight_context_probe_plan.md"
STAGE_REVIEW_PATH = STAGE_ROOT / "03_reviews/run03R_gap_overnight_context_probe_packet.md"
MODEL_INPUT_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
TRAINING_SUMMARY_PATH = ROOT / "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"

SESSION_BUCKETS = (
    {"id": "down_open", "label": "gap_or_overnight_down_context", "flag_min": -1, "flag_max": -1},
    {"id": "flat_open", "label": "flat_gap_overnight_context", "flag_min": 0, "flag_max": 0},
    {"id": "up_open", "label": "gap_or_overnight_up_context", "flag_min": 1, "flag_max": 1},
)
BUCKET_BY_ID = {bucket["id"]: bucket for bucket in SESSION_BUCKETS}
PYTHON_FOLDS = tuple(fold for fold in FOLDS if fold.fold_id != "fold07")
OPEN_CONTEXT_THRESHOLD = 0.002
GAP_CONTEXT_WEIGHT = 5.0

ATTEMPT_COLUMNS = (
    "run_id",
    "session_bucket_id",
    "session_bucket_label",
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


def gap_overnight_context_flag_count(frame: pd.DataFrame) -> pd.Series:
    overnight = pd.to_numeric(frame["overnight_return"], errors="coerce").fillna(0.0)
    gap = pd.to_numeric(frame["gap_percent"], errors="coerce").fillna(0.0)
    open_score = overnight + gap * GAP_CONTEXT_WEIGHT
    score = pd.Series(0, index=frame.index, dtype="int64")
    score.loc[open_score <= -OPEN_CONTEXT_THRESHOLD] = -1
    score.loc[open_score >= OPEN_CONTEXT_THRESHOLD] = 1
    return score


def assign_session_bucket(frame: pd.DataFrame) -> pd.Series:
    score = gap_overnight_context_flag_count(frame)
    out = pd.Series("flat_open", index=frame.index, dtype="object")
    out.loc[score.lt(0)] = "down_open"
    out.loc[score.gt(0)] = "up_open"
    return out


def filter_bucket(frame: pd.DataFrame, bucket_id: str) -> pd.DataFrame:
    if "session_bucket_id" in frame.columns:
        mask = frame["session_bucket_id"].astype(str).eq(bucket_id)
    else:
        mask = assign_session_bucket(frame).eq(bucket_id)
    return frame.loc[mask].copy().reset_index(drop=True)


def train_model(frame: pd.DataFrame, features: Sequence[str], params: Mapping[str, Any]) -> ExtraTreesClassifier:
    model = ExtraTreesClassifier(**dict(params))
    model.fit(frame.loc[:, list(features)].to_numpy(dtype="float64", copy=False), frame["label_class"].astype(int))
    return model


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
    bucket_id = assign_session_bucket(source).to_numpy()
    vol_flags = gap_overnight_context_flag_count(source).to_numpy()
    return pd.DataFrame(
        {
            "run_id": RUN_ID,
            "fold_id": fold_id,
            "variant_id": "gap_overnight_context_v01_base_leaf20_q90",
            "source_variant_id": REFERENCE_VARIANT_ID,
            "idea_id": IDEA_ID,
            "split_role": split_role,
            "tier_scope": tier_scope,
            "route_role": route_role,
            "feature_selector": feature_selector,
            "feature_count": int(feature_count),
            "timestamp": source["timestamp"].astype(str).to_numpy(),
            "minutes_from_cash_open": source["minutes_from_cash_open"].to_numpy(),
            "session_bucket_id": bucket_id,
            "session_bucket_label": [BUCKET_BY_ID.get(str(item), {}).get("label", "outside") for item in bucket_id],
            "gap_overnight_context_flag_count": vol_flags,
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
            "directional_correct": (decision == labels) & is_signal,
        }
    )


def signal_metrics(frame: pd.DataFrame) -> dict[str, Any]:
    signals = frame.loc[frame["is_signal"]]
    count = int(len(signals))
    correct = int(signals["directional_correct"].sum()) if count else 0
    return {
        "rows": int(len(frame)),
        "signal_count": count,
        "coverage": float(count / len(frame)) if len(frame) else None,
        "correct_count": correct,
        "hit_rate": float(correct / count) if count else None,
        "short_count": int((signals["decision_class"] == 0).sum()),
        "long_count": int((signals["decision_class"] == 2).sum()),
    }


def metric_row(frame: pd.DataFrame, fold: Any, split_role: str, bucket_id: str) -> dict[str, Any]:
    first = frame.iloc[0].to_dict() if not frame.empty else {}
    bucket = BUCKET_BY_ID[bucket_id]
    return {
        "run_id": RUN_ID,
        "fold_id": fold.fold_id,
        "session_bucket_id": bucket_id,
        "session_bucket_label": bucket["label"],
        "session_bucket_start": bucket["flag_min"],
        "session_bucket_end": bucket["flag_max"],
        "variant_id": first.get("variant_id", "gap_overnight_context_v01_base_leaf20_q90"),
        "source_variant_id": REFERENCE_VARIANT_ID,
        "idea_id": IDEA_ID,
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


def summarize_session_metrics(metrics: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    keys = ["session_bucket_id", "session_bucket_label", "tier_scope", "route_role"]
    for key, group in metrics.groupby(keys, dropna=False):
        bucket_id, bucket_label, tier_scope, route_role = key
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
        gap = merged["hit_rate_test"] - merged["hit_rate_validation"]
        rows.append(
            {
                "run_id": RUN_ID,
                "session_bucket_id": bucket_id,
                "session_bucket_label": bucket_label,
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
                "both_positive_fold_count": int(((merged["hit_rate_validation"] >= HIT_FLOOR) & (merged["hit_rate_test"] >= HIT_FLOOR)).sum()),
                "inversion_fold_count": int((merged["hit_rate_test"] > merged["hit_rate_validation"]).sum()),
                "test_collapse_fold_count": int((merged["hit_rate_test"] < 0.40).sum()),
                "mean_abs_fold_gap": float(gap.abs().mean()) if not gap.dropna().empty else math.nan,
                "worst_test_hit_rate": float(merged["hit_rate_test"].min()) if not merged["hit_rate_test"].dropna().empty else math.nan,
            }
        )
    return pd.DataFrame(rows).sort_values(["tier_scope", "session_bucket_id"]).reset_index(drop=True)


def evaluate_python_wfo() -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    spec = source_spec()
    tier_a, tier_b_fallback, feature_order, metadata = prepare_frames()
    tier_b_training = metadata["tier_b_training"]
    params = probe_params(spec)
    a_features = list(feature_order)
    b_features = list(TIER_B_CORE_FEATURE_ORDER)
    metric_rows: list[dict[str, Any]] = []
    signal_frames: list[pd.DataFrame] = []
    fold_rows: list[dict[str, Any]] = []
    for fold in PYTHON_FOLDS:
        a_train = window(tier_a, fold.train_start, fold.train_end_exclusive)
        a_validation = window(tier_a, fold.validation_start, fold.validation_end_exclusive)
        a_test = window(tier_a, fold.test_start, fold.test_end_exclusive)
        b_train = window(tier_b_training, fold.train_start, fold.train_end_exclusive)
        b_validation = window(tier_b_fallback, fold.validation_start, fold.validation_end_exclusive)
        b_test = window(tier_b_fallback, fold.test_start, fold.test_end_exclusive)
        fold_rows.append({**fold.as_row(), "fold_scope": "python_wfo_no_fold07"})
        a_model = train_model(a_train, a_features, params)
        b_model = train_model(b_train, b_features, params)
        a_val_probs = ordered_probs(a_model, a_validation, a_features)
        a_test_probs = ordered_probs(a_model, a_test, a_features)
        b_val_probs = ordered_probs(b_model, b_validation, b_features)
        b_test_probs = ordered_probs(b_model, b_test, b_features)
        a_threshold = nonflat_threshold(a_val_probs, spec.threshold_quantile)
        b_threshold = nonflat_threshold(b_val_probs, spec.threshold_quantile)
        frames = (
            decision_frame(source=a_validation, probs=a_val_probs, threshold=a_threshold, spec=spec, fold_id=fold.fold_id, split_role="validation", tier_scope="Tier A", route_role="tier_a_only", feature_selector="all58", feature_count=len(a_features)),
            decision_frame(source=a_test, probs=a_test_probs, threshold=a_threshold, spec=spec, fold_id=fold.fold_id, split_role="test", tier_scope="Tier A", route_role="tier_a_only", feature_selector="all58", feature_count=len(a_features)),
            decision_frame(source=b_validation, probs=b_val_probs, threshold=b_threshold, spec=spec, fold_id=fold.fold_id, split_role="validation", tier_scope="Tier B", route_role="tier_b_fallback_only", feature_selector="core42_partial_context", feature_count=len(b_features)),
            decision_frame(source=b_test, probs=b_test_probs, threshold=b_threshold, spec=spec, fold_id=fold.fold_id, split_role="test", tier_scope="Tier B", route_role="tier_b_fallback_only", feature_selector="core42_partial_context", feature_count=len(b_features)),
        )
        routed_validation = pd.concat(
            [frames[0].assign(tier_scope="Tier A+B", route_role="routed_tier_a_primary_used"), frames[2].assign(tier_scope="Tier A+B", route_role="routed_tier_b_fallback_used")],
            ignore_index=True,
        ).assign(route_role="routed_total")
        routed_test = pd.concat(
            [frames[1].assign(tier_scope="Tier A+B", route_role="routed_tier_a_primary_used"), frames[3].assign(tier_scope="Tier A+B", route_role="routed_tier_b_fallback_used")],
            ignore_index=True,
        ).assign(route_role="routed_total")
        for frame in (*frames, routed_validation, routed_test):
            split_role = str(frame["split_role"].iloc[0])
            for bucket in SESSION_BUCKETS:
                bucket_frame = filter_bucket(frame, str(bucket["id"]))
                if not bucket_frame.empty:
                    metric_rows.append(metric_row(bucket_frame, fold, split_role, str(bucket["id"])))
                    signal_frames.append(bucket_frame.loc[bucket_frame["is_signal"]].copy())
    fold_plan = pd.DataFrame(fold_rows)
    bucket_metrics = pd.DataFrame(metric_rows)
    bucket_summary = summarize_session_metrics(bucket_metrics)
    signals = pd.concat(signal_frames, ignore_index=True) if signal_frames else pd.DataFrame()
    metadata = {
        "source_metadata": {key: value for key, value in metadata.items() if key != "tier_b_training"},
        "params": params,
        "tier_a_feature_count": len(a_features),
        "tier_b_feature_count": len(b_features),
        "folds_used": [fold.fold_id for fold in PYTHON_FOLDS],
        "folds_excluded": ["fold07"],
    }
    return metadata, fold_plan, bucket_metrics, bucket_summary, signals


def split_dates_from_frame(frame: pd.DataFrame) -> tuple[str, str]:
    if frame.empty:
        raise RuntimeError("empty split frame")
    stamps = pd.to_datetime(frame["timestamp"], utc=True)
    return stamps.min().strftime("%Y.%m.%d"), (stamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


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
    bucket_id: str,
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
            attempt_name=f"{bucket_id}_tier_a_only_{split}",
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
            record_view_prefix=f"mt5_{bucket_id}_tier_a_only",
        ),
        attempt_payload(
            **common_kwargs,
            attempt_name=f"{bucket_id}_tier_b_fallback_only_{split}",
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
            record_view_prefix=f"mt5_{bucket_id}_tier_b_fallback_only",
        ),
        attempt_payload(
            **common_kwargs,
            attempt_name=f"{bucket_id}_routed_{split}",
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
            record_view_prefix=f"mt5_{bucket_id}_routed_total",
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
        bucket = BUCKET_BY_ID[bucket_id]
        attempt["session_bucket_id"] = bucket_id
        attempt["session_bucket_label"] = bucket["label"]
        attempt["source_variant_id"] = "gap_overnight_context_v01_base_leaf20_q90"
        attempt["fold_id"] = MT5_FOLD_ID
        attempt["wfo_split_role"] = wfo_role
    return attempts


def prepare_mt5_run() -> dict[str, Any]:
    for child in ("models", "mt5", "predictions", "reports", "results"):
        io_path(RUN_ROOT / child).mkdir(parents=True, exist_ok=True)
    spec = source_spec()
    tier_a, tier_b_fallback, feature_order, metadata = prepare_frames()
    fold = next(item for item in FOLDS if item.fold_id == MT5_FOLD_ID)
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
    tier_a_model = train_model(a_train, tier_a_order, params)
    tier_b_model = train_model(b_train, tier_b_order, params)
    tier_a_val_probs = ordered_probs(tier_a_model, a_validation, tier_a_order)
    tier_b_val_probs = ordered_probs(tier_b_model, b_validation, tier_b_order)
    threshold_a = nonflat_threshold(tier_a_val_probs, spec.threshold_quantile)
    threshold_b = nonflat_threshold(tier_b_val_probs, spec.threshold_quantile)
    tier_a_hash = mt5.ordered_hash(tier_a_order)
    tier_b_hash = mt5.ordered_hash(tier_b_order)
    tier_a_joblib = RUN_ROOT / "models/tier_a_gap_overnight_context_fold05_model.joblib"
    tier_b_joblib = RUN_ROOT / "models/tier_b_gap_overnight_context_fold05_core42_model.joblib"
    tier_a_onnx = tier_a_joblib.with_suffix(".onnx")
    tier_b_onnx = tier_b_joblib.with_suffix(".onnx")
    joblib.dump(tier_a_model, io_path(tier_a_joblib))
    joblib.dump(tier_b_model, io_path(tier_b_joblib))
    tier_a_onnx_payload = mt5.export_sklearn_to_onnx_zipmap_disabled(tier_a_model, tier_a_onnx, feature_count=len(tier_a_order))
    tier_b_onnx_payload = mt5.export_sklearn_to_onnx_zipmap_disabled(tier_b_model, tier_b_onnx, feature_count=len(tier_b_order))
    write_text(RUN_ROOT / "models/tier_a_feature_order.txt", "\n".join(tier_a_order), bom=False)
    write_text(RUN_ROOT / "models/tier_b_core42_feature_order.txt", "\n".join(tier_b_order), bom=False)
    onnx_parity = {
        "tier_a": mt5.check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx, a_validation.loc[:, tier_a_order].to_numpy(dtype="float64", copy=False)[:128]),
        "tier_b": mt5.check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx, b_validation.loc[:, tier_b_order].to_numpy(dtype="float64", copy=False)[:128]),
    }
    onnx_parity["passed"] = bool(onnx_parity["tier_a"]["passed"] and onnx_parity["tier_b"]["passed"])
    if not onnx_parity["passed"]:
        raise RuntimeError("RUN03R ONNX parity failed")
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    copies = [
        copy_to_common(tier_a_onnx, f"{common}/models/{tier_a_onnx.name}", COMMON_FILES_ROOT_DEFAULT),
        copy_to_common(tier_b_onnx, f"{common}/models/{tier_b_onnx.name}", COMMON_FILES_ROOT_DEFAULT),
    ]
    attempts: list[dict[str, Any]] = []
    feature_matrices: list[dict[str, Any]] = []
    a_rule = mt5_rule(float(threshold_a), spec.direction_mode)
    b_rule = mt5_rule(float(threshold_b), spec.direction_mode)
    route_coverage = {"by_split": {}, "session_buckets": {}, "no_tier_by_split": {"validation": None, "oos": None}}
    for split_label, wfo_role, a_frame, b_frame in (
        ("validation_is", "validation", a_validation, b_validation),
        ("oos", "test", a_test, b_test),
    ):
        split_key = "validation" if split_label == "validation_is" else "oos"
        route_coverage["by_split"][split_key] = {"tier_a_primary_rows": int(len(a_frame)), "tier_b_fallback_rows": int(len(b_frame)), "routed_labelable_rows": int(len(a_frame) + len(b_frame)), "wfo_split_role": wfo_role}
        for bucket in SESSION_BUCKETS:
            bucket_id = str(bucket["id"])
            a_bucket = filter_bucket(a_frame, bucket_id)
            b_bucket = filter_bucket(b_frame, bucket_id)
            if a_bucket.empty or b_bucket.empty:
                continue
            from_date, to_date = split_dates_from_frame(a_bucket)
            a_matrix = RUN_ROOT / "mt5" / f"{bucket_id}_tier_a_{split_label}_feature_matrix.csv"
            b_matrix = RUN_ROOT / "mt5" / f"{bucket_id}_tier_b_{split_label}_feature_matrix.csv"
            feature_matrices.append(mt5.export_mt5_feature_matrix_csv(a_bucket, tier_a_order, a_matrix))
            feature_matrices.append(
                mt5.export_mt5_feature_matrix_csv(
                    b_bucket,
                    tier_b_order,
                    b_matrix,
                    metadata_columns=("route_role", "partial_context_subtype", "missing_feature_group_mask", "available_feature_group_mask"),
                )
            )
            copies.append(copy_to_common(a_matrix, f"{common}/features/{a_matrix.name}", COMMON_FILES_ROOT_DEFAULT))
            copies.append(copy_to_common(b_matrix, f"{common}/features/{b_matrix.name}", COMMON_FILES_ROOT_DEFAULT))
            route_coverage["session_buckets"][f"{bucket_id}_{split_key}"] = {"tier_a_primary_rows": int(len(a_bucket)), "tier_b_fallback_rows": int(len(b_bucket)), "routed_labelable_rows": int(len(a_bucket) + len(b_bucket))}
            attempts.extend(
                make_attempts(
                    bucket_id=bucket_id,
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
                    min_margin=float(spec.min_margin),
                )
            )
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_wfo_run_id": SOURCE_WFO_RUN_ID,
        "source_recency_run_id": SOURCE_RECENCY_RUN_ID,
        "source_variant_run_id": SOURCE_VARIANT_RUN_ID,
        "source_variant_id": REFERENCE_VARIANT_ID,
        "fold_id": MT5_FOLD_ID,
        "model_key": spec.model_key,
        "idea_id": IDEA_ID,
        "thresholds": {"tier_a": threshold_a, "tier_b": threshold_b, "quantile": spec.threshold_quantile},
        "gap_overnight_context_buckets": SESSION_BUCKETS,
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
        "common_copies": copies,
        "feature_matrices": feature_matrices,
        "route_coverage": route_coverage,
        "completion_goal": "gap_overnight_context_probe_no_fold07_with_fold05_mt5",
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": "stage12_standalone_no_stage10_11_inheritance",
    }


def bucket_from_view(record_view: str) -> str:
    for bucket in BUCKET_BY_ID:
        if f"_{bucket}_" in record_view:
            return bucket
    return "unknown"


def bucket_from_attempt_name(attempt_name: str) -> str:
    for marker in ("_tier_a_only_", "_tier_b_fallback_only_", "_routed_"):
        if marker in attempt_name:
            bucket_id = attempt_name.split(marker, 1)[0]
            if bucket_id in BUCKET_BY_ID:
                return bucket_id
    return bucket_from_view(attempt_name)


def completed_record_count_for_execution(execution: Mapping[str, Any]) -> int:
    routing_mode = str(execution.get("routing_mode", ""))
    if routing_mode == "tier_a_primary_tier_b_fallback":
        return 3
    if routing_mode == "tier_a_primary_no_fallback":
        return 2
    return 1


def bucket_record_view(bucket_id: str, record: Mapping[str, Any]) -> str:
    split = str(record.get("split"))
    route_role = str(record.get("route_role", ""))
    tier_scope = str(record.get("tier_scope", ""))
    if route_role == "primary_used":
        return f"mt5_{bucket_id}_routed_tier_a_used_{split}"
    if route_role == "fallback_used":
        return f"mt5_{bucket_id}_routed_tier_b_fallback_used_{split}"
    if route_role == "routed_total":
        return f"mt5_{bucket_id}_routed_total_{split}"
    if route_role == "tier_b_fallback_only_total" or tier_scope == "Tier B":
        return f"mt5_{bucket_id}_tier_b_fallback_only_{split}"
    return f"mt5_{bucket_id}_tier_a_only_{split}"


def repair_mt5_record_identities(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    records = [dict(record) for record in result.get("mt5_kpi_records", [])]
    completed_executions = [record for record in result.get("execution_results", []) if record.get("status") == "completed"]
    record_index = 0
    for execution in completed_executions:
        bucket_id = bucket_from_attempt_name(str(execution.get("attempt_name", "")))
        expected_records = completed_record_count_for_execution(execution)
        for _ in range(expected_records):
            if record_index >= len(records):
                break
            record = records[record_index]
            if bucket_id == "unknown":
                bucket_id = bucket_from_view(str(record.get("record_view", "")))
            record["session_bucket_id"] = bucket_id
            record["session_bucket_label"] = BUCKET_BY_ID.get(bucket_id, {}).get("label", "unknown")
            if bucket_id != "unknown":
                record["record_view"] = bucket_record_view(bucket_id, record)
            record["source_variant_id"] = "gap_overnight_context_v01_base_leaf20_q90"
            record["fold_id"] = MT5_FOLD_ID
            record["wfo_split_role"] = "validation" if record.get("split") == "validation_is" else "test"
            record_index += 1
    for record in records[record_index:]:
        bucket_id = bucket_from_view(str(record.get("record_view", "")))
        record["session_bucket_id"] = bucket_id
        record["session_bucket_label"] = BUCKET_BY_ID.get(bucket_id, {}).get("label", "unknown")
        record["source_variant_id"] = "gap_overnight_context_v01_base_leaf20_q90"
        record["fold_id"] = MT5_FOLD_ID
        record["wfo_split_role"] = "validation" if record.get("split") == "validation_is" else "test"
    return records


def finalize_result(result: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(result)
    completed = out.get("external_verification_status") == "completed"
    out["judgment"] = JUDGMENT if completed else "blocked_gap_overnight_context_mt5_probe"
    out["mt5_kpi_records"] = repair_mt5_record_identities(out)
    return out


def correct_execution_report_links(result: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(result)
    reports_by_name = {report.get("report_name"): report for report in out.get("strategy_tester_reports", [])}
    attempts_by_name = {attempt.get("attempt_name"): attempt for attempt in out.get("attempts", [])}
    corrected_executions: list[dict[str, Any]] = []
    for execution in out.get("execution_results", []):
        corrected = dict(execution)
        attempt = attempts_by_name.get(execution.get("attempt_name"), {})
        report = reports_by_name.get(mt5.report_name_from_attempt(attempt), {}) if attempt else {}
        if report:
            corrected["strategy_tester_report"] = report
        corrected_executions.append(corrected)
    out["execution_results"] = corrected_executions
    out["mt5_kpi_records"] = build_mt5_kpi_records(corrected_executions)
    return out


def execute_mt5(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        result = {**dict(prepared), "compile": {"status": "not_attempted_materialize_only"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": "blocked_materialize_only_no_mt5_execution"}
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
        result = correct_execution_report_links(result)
    return finalize_result(result)


def write_preliminary_kpi(result: Mapping[str, Any]) -> None:
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
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
            "kpi_scope": "gap_overnight_context_probe_preliminary",
            "model_family": MODEL_FAMILY,
            "feature_set_id": FEATURE_SET_ID,
            "label_id": LABEL_ID,
            "split_contract": SPLIT_CONTRACT,
            "mt5": {"scoreboard_lane": "runtime_probe_gap_overnight_context", "kpi_records": result.get("mt5_kpi_records", [])},
        },
    )


def normalized_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    return mt5_kpi_recorder.build_normalized_records(ROOT, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "path": rel(RUN_ROOT)}])


def attempt_summary_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    reports = {record.get("report_name"): record for record in result.get("strategy_tester_reports", [])}
    attempts = {attempt["attempt_name"]: attempt for attempt in result.get("attempts", [])}
    for execution in result.get("execution_results", []):
        attempt = attempts.get(execution.get("attempt_name"), {})
        report = reports.get(mt5.report_name_from_attempt(attempt), {}) if attempt else {}
        metrics = report.get("metrics", {}) if isinstance(report, Mapping) else {}
        bucket_id = str(attempt.get("session_bucket_id", "unknown"))
        rows.append(
            {
                "run_id": RUN_ID,
                "session_bucket_id": bucket_id,
                "session_bucket_label": BUCKET_BY_ID.get(bucket_id, {}).get("label", "unknown"),
                "fold_id": MT5_FOLD_ID,
                "attempt_name": execution.get("attempt_name"),
                "split": execution.get("split"),
                "wfo_split_role": "validation" if execution.get("split") == "validation_is" else "test",
                "tier_scope": execution.get("tier"),
                "route_role": execution.get("attempt_role") or ("routed_total if routing else tier_only_total"),
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


def mt5_summary_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for record in result.get("mt5_kpi_records", []):
        if record.get("route_role") in {"primary_used", "fallback_used"}:
            continue
        metrics = record.get("metrics", {})
        bucket_id = str(record.get("session_bucket_id", "unknown"))
        rows.append(
            {
                "run_id": RUN_ID,
                "session_bucket_id": bucket_id,
                "session_bucket_label": BUCKET_BY_ID.get(bucket_id, {}).get("label", "unknown"),
                "record_view": record.get("record_view"),
                "split": record.get("split"),
                "wfo_split_role": record.get("wfo_split_role"),
                "tier_scope": record.get("tier_scope"),
                "route_role": record.get("route_role"),
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "status": record.get("status"),
            }
        )
    return rows


def build_packet_summary(
    result: Mapping[str, Any],
    bucket_summary: pd.DataFrame,
    normalized_records: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    trade_parser_errors: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    routed = bucket_summary.loc[bucket_summary["tier_scope"].eq("Tier A+B")].copy()
    best_test = routed.sort_values(["test_weighted_hit_rate", "test_signal_total"], ascending=[False, False]).iloc[0].to_dict()
    mt5_rows = mt5_summary_rows(result)
    mt5_routed = [row for row in mt5_rows if row.get("tier_scope") == "Tier A+B"]
    completed = result.get("external_verification_status") == "completed"
    return {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "idea_id": IDEA_ID,
        "source_wfo_run_id": SOURCE_WFO_RUN_ID,
        "source_recency_run_id": SOURCE_RECENCY_RUN_ID,
        "source_variant_run_id": SOURCE_VARIANT_RUN_ID,
        "source_variant_id": REFERENCE_VARIANT_ID,
        "folds_used": [fold.fold_id for fold in PYTHON_FOLDS],
        "folds_excluded": ["fold07"],
        "mt5_fold_id": MT5_FOLD_ID,
        "bucket_count": len(SESSION_BUCKETS),
        "python_bucket_summary_rows": int(len(bucket_summary)),
        "python_bucket_metric_rows": int(len(PYTHON_FOLDS) * len(SESSION_BUCKETS) * 6),
        "best_python_routed_bucket": best_test,
        "mt5_routed_rows": mt5_routed,
        "mt5_attempts_total": len(result.get("attempts", [])),
        "mt5_reports_total": len(result.get("strategy_tester_reports", [])),
        "mt5_kpi_records": len(result.get("mt5_kpi_records", [])),
        "normalized_records": len(normalized_records),
        "trade_level_rows": len(trade_rows),
        "trade_parser_errors": len(trade_parser_errors),
        "external_verification_status": "completed" if completed else "blocked",
        "status": "completed" if completed else "partial",
        "completed_forbidden": not completed,
        "judgment": JUDGMENT if completed else "blocked_gap_overnight_context_mt5_probe",
        "boundary": BOUNDARY,
        "allowed_claims": ["runtime_probe_gap_overnight_context_completed", "no_fold07_gap_overnight_context_probe_completed"] if completed else ["blocked"],
        "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
    }


def runtime_evidence_gate(summary: Mapping[str, Any]) -> dict[str, Any]:
    passed = summary.get("external_verification_status") == "completed" and int(summary.get("mt5_attempts_total", 0)) == 18
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
            "bucket_count": summary.get("bucket_count"),
            "fold07_used": False,
        },
        "allowed_claims": ["runtime_probe_gap_overnight_context_completed"] if passed else ["blocked"],
        "forbidden_claims": [] if passed else ["completed", "reviewed", "verified"],
    }


def write_ledgers(packet_summary: Mapping[str, Any], result: Mapping[str, Any], bucket_summary: pd.DataFrame) -> dict[str, Any]:
    status = "reviewed" if packet_summary["external_verification_status"] == "completed" else "blocked"
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "gap_overnight_context_runtime_probe",
            "status": status,
            "judgment": packet_summary["judgment"],
            "path": rel(RUN_ROOT),
            "notes": ledger_pairs((("source_wfo_run_id", SOURCE_WFO_RUN_ID), ("mt5_fold_id", MT5_FOLD_ID), ("fold07_used", False), ("bucket_count", packet_summary.get("bucket_count")), ("boundary", BOUNDARY))),
        }
    ]
    ledger_rows = python_ledger_rows(packet_summary, bucket_summary) + mt5_ledger_rows(packet_summary, result)
    prune_existing_run_rows(PROJECT_ALPHA_LEDGER_PATH)
    prune_existing_run_rows(STAGE_RUN_LEDGER_PATH)
    return {
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id"),
        "project_alpha_ledger": upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id"),
        "stage_run_ledger": upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id"),
        "rows_written": len(ledger_rows),
    }


def prune_existing_run_rows(path: Path) -> None:
    existing = read_csv_rows(path)
    kept = [row for row in existing if row.get("run_id") != RUN_ID]
    if len(kept) != len(existing):
        write_csv_rows(path, ALPHA_LEDGER_COLUMNS, kept)


def python_ledger_rows(summary: Mapping[str, Any], bucket_summary: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for record in bucket_summary.to_dict("records"):
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__python__{record['session_bucket_id']}__{record['tier_scope'].replace('+', 'plus').replace(' ', '_').lower()}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"python_{record['session_bucket_id']}_{record['tier_scope']}",
                "parent_run_id": SOURCE_WFO_RUN_ID,
                "record_view": f"python_session_{record['session_bucket_id']}_{record['route_role']}",
                "tier_scope": record.get("tier_scope"),
                "kpi_scope": "gap_overnight_context_python_wfo_no_fold07",
                "scoreboard_lane": "runtime_probe_gap_overnight_context",
                "status": summary["status"],
                "judgment": summary["judgment"],
                "path": rel(RUN_ROOT / "results/session_bucket_summary.csv"),
                "primary_kpi": ledger_pairs((("validation_hit", record.get("validation_weighted_hit_rate")), ("test_hit", record.get("test_weighted_hit_rate")), ("test_signal_total", record.get("test_signal_total")), ("both_positive_fold_count", record.get("both_positive_fold_count")))),
                "guardrail_kpi": ledger_pairs((("session_bucket", record.get("session_bucket_label")), ("folds_used", "fold01-fold06"), ("fold07_used", False), ("boundary", BOUNDARY))),
                "external_verification_status": summary["external_verification_status"],
                "notes": "RUN03R Python gap-overnight-context-regime WFO row; not alpha quality or promotion.",
            }
        )
    return rows


def mt5_ledger_rows(summary: Mapping[str, Any], result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for record in result.get("mt5_kpi_records", []):
        metrics = record.get("metrics", {})
        bucket_id = str(record.get("session_bucket_id", "unknown"))
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{record.get('record_view')}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": str(record.get("record_view")),
                "parent_run_id": SOURCE_WFO_RUN_ID,
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "kpi_scope": "gap_overnight_context_mt5_fold05",
                "scoreboard_lane": "runtime_probe_gap_overnight_context",
                "status": record.get("status"),
                "judgment": summary["judgment"],
                "path": record.get("report", {}).get("html_report", {}).get("path", ""),
                "primary_kpi": ledger_pairs((("net_profit", metrics.get("net_profit")), ("profit_factor", metrics.get("profit_factor")), ("trade_count", metrics.get("trade_count")), ("signal_count", metrics.get("signal_count")))),
                "guardrail_kpi": ledger_pairs((("session_bucket", BUCKET_BY_ID.get(bucket_id, {}).get("label", "unknown")), ("mt5_fold_id", MT5_FOLD_ID), ("wfo_split_role", record.get("wfo_split_role")), ("route_role", record.get("route_role")), ("fold07_used", False), ("boundary", BOUNDARY))),
                "external_verification_status": summary["external_verification_status"],
                "notes": "RUN03R MT5 fold05 gap-overnight-context-regime row; runtime probe only.",
            }
        )
    return rows


def required_skills() -> list[str]:
    return ["obsidian-runtime-parity", "obsidian-experiment-design", "obsidian-model-validation", "obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-exploration-mandate", "obsidian-result-judgment"]


def required_gates() -> list[str]:
    return ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "work_packet_schema_lint", "skill_receipt_lint", "skill_receipt_schema_lint", "state_sync_audit", "required_gate_coverage_audit", "final_claim_guard"]


def write_work_packet(created_at: str, summary: Mapping[str, Any]) -> None:
    packet = {
        "version": "work_packet_schema_v2",
        "packet_id": PACKET_ID,
        "created_at_utc": created_at,
        "user_request": {"user_quote": "하나씩 run으로 구성해서 mt5까지 연동해서 검증해줘", "requested_action": "run gap/overnight context regime probe without fold07 and include MT5 verification", "requested_count": {"value": 1, "n_a_reason": None}, "ambiguous_terms": ["one at a time means RUN03R first."]},
        "current_truth": {"active_stage": STAGE_ID, "current_run_before_packet": SOURCE_RECENCY_RUN_ID, "current_run_after_packet": RUN_ID, "branch": current_branch(), "source_documents": [rel(WORKSPACE_STATE_PATH), rel(CURRENT_STATE_PATH), rel(SELECTION_STATUS_PATH)]},
        "work_classification": {"primary_family": "runtime_backtest", "detected_families": ["runtime_backtest", "experiment_execution", "kpi_evidence", "state_sync"], "touched_surfaces": ["stage12_run_artifacts", "mt5_strategy_tester", "run_ledgers", "current_truth_docs"], "mutation_intent": True, "execution_intent": True},
        "risk_vector_scan": {"risks": {"single_bucket_overread_risk": "high", "runtime_evidence_risk": "high", "fold07_leakage_risk": "medium", "claim_overstatement_risk": "high"}, "hard_stop_risks": [], "required_decision_locks": [], "required_gates": required_gates(), "forbidden_claims": summary["forbidden_claims"]},
        "decision_lock": {"mode": "user_explicit_one_run_no_variant", "assumptions": {"fold07_excluded": True, "python_folds": "fold01-fold06", "mt5_fold": MT5_FOLD_ID, "gap_overnight_context_buckets": [b["label"] for b in SESSION_BUCKETS]}, "questions": [], "required_user_decisions": []},
        "interpreted_scope": {"work_families": ["runtime_backtest"], "target_surfaces": [rel(RUN_ROOT), rel(PACKET_ROOT), rel(STAGE_RUN_LEDGER_PATH), rel(PROJECT_ALPHA_LEDGER_PATH)], "scope_units": ["single_idea", "gap_overnight_context_bucket", "fold", "tier_view", "mt5_attempt", "kpi_record", "ledger"], "execution_layers": ["python_wfo", "onnx_export", "mt5_strategy_tester", "kpi_recording", "ledger_update", "document_edit"], "mutation_policy": {"allowed": True, "boundary": "new RUN03R artifacts and current truth only"}, "evidence_layers": ["python_gap_overnight_context_metrics", "mt5_reports", "normalized_kpi", "trade_attribution", "ledgers", "work_packet"], "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False}, "claim_boundary": {"allowed_claims": summary["allowed_claims"], "forbidden_claims": summary["forbidden_claims"]}},
        "acceptance_criteria": [
            {"id": "AC-001", "text": "fold07 is excluded.", "expected_artifact": rel(RUN_ROOT / "results/fold_plan.csv"), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Three gap/overnight context buckets are recorded for Tier A, Tier B, and Tier A+B.", "expected_artifact": rel(RUN_ROOT / "results/session_bucket_summary.csv"), "verification_method": "kpi_contract_audit", "required": True},
            {"id": "AC-003", "text": "MT5 fold05 bucket attempts are recorded.", "expected_artifact": rel(PACKET_ROOT / "attempt_summary.csv"), "verification_method": "runtime_evidence_gate", "required": True},
        ],
        "work_plan": {"phases": [{"id": "python_wfo", "actions": ["train_fold01_to_fold06", "score_gap_overnight_context_buckets"]}, {"id": "execute_mt5", "actions": ["train_fold05_models", "export_bucket_feature_matrices", "run_18_strategy_tester_attempts"]}, {"id": "closeout", "actions": ["record_kpi", "record_trade_attribution", "update_ledgers", "sync_current_truth", "run_gates"]}], "expected_outputs": [rel(RUN_ROOT / "reports/result_summary.md"), rel(PACKET_ROOT / "closeout_gate.json")], "stop_conditions": ["fold07_used", "missing_mt5_reports", "parser_errors", "ledger_rows_missing"]},
        "skill_routing": {"primary_family": "runtime_backtest", "primary_skill": "obsidian-runtime-parity", "support_skills": ["obsidian-experiment-design", "obsidian-model-validation", "obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-exploration-mandate", "obsidian-result-judgment"], "skills_considered": required_skills(), "skills_selected": required_skills(), "skills_not_used": {}, "required_skill_receipts": required_skills(), "required_gates": required_gates()},
        "evidence_contract": {"raw_evidence": [rel(PACKET_ROOT / "execution_results.json"), rel(PACKET_ROOT / "trade_level_records.csv")], "machine_readable": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "kpi_record.json"), rel(PACKET_ROOT / "normalized_kpi_records.jsonl")], "human_readable": [rel(RUN_ROOT / "reports/result_summary.md"), rel(STAGE_REVIEW_PATH)]},
        "gates": {"required": required_gates(), "actual_status_source": rel(PACKET_ROOT / "closeout_gate.json"), "not_applicable_with_reason": {}},
        "final_claim_policy": {"allowed_claims": summary["allowed_claims"], "forbidden_claims": summary["forbidden_claims"], "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml"},
    }
    write_yaml(PACKET_ROOT / "work_packet.yaml", packet)


def skill_receipts(created_at: str, summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"packet_id": PACKET_ID, "created_at_utc": created_at, "triggered": True, "blocking": False, "skill": "obsidian-runtime-parity", "status": "executed", "python_artifact": rel(RUN_ROOT / "results/session_bucket_summary.csv"), "runtime_artifact": rel(RUN_ROOT / "run_manifest.json"), "compared_surface": "Python gap/overnight context bucket WFO, ONNX exports, bucket feature matrices, and MT5 Strategy Tester reports", "parity_level": "runtime_probe", "tester_identity": f"US100 M5, deposit=500, leverage=1:100, mt5_fold={MT5_FOLD_ID}, attempts={summary.get('mt5_attempts_total')}", "missing_evidence": "none" if summary["external_verification_status"] == "completed" else "blocked_mt5_attempts", "allowed_claims": ["runtime_probe_gap_overnight_context_completed"], "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"]},
        {"packet_id": PACKET_ID, "created_at_utc": created_at, "triggered": True, "blocking": False, "skill": "obsidian-experiment-design", "status": "executed", "hypothesis": "ExtraTrees signal quality may depend on broad gap_overnight_context regimes.", "baseline": SOURCE_WFO_RUN_ID, "changed_variables": ["post-score gap/overnight context bucket segmentation", "fold07 exclusion"], "invalid_conditions": ["fold07 included", "missing tier view", "missing MT5 reports"], "evidence_plan": [rel(RUN_ROOT / "results/session_bucket_summary.csv"), rel(PACKET_ROOT / "normalized_kpi_records.jsonl")]},
        {"packet_id": PACKET_ID, "created_at_utc": created_at, "triggered": True, "blocking": False, "skill": "obsidian-model-validation", "status": "executed", "model_or_threshold_surface": "ExtraTrees v01 base leaf20 q90 with gap-overnight-context-regime post-score segmentation", "validation_split": "Python fold01-fold06 only and MT5 fold05 only; fold07 excluded", "overfit_checks": "bucket hit-rate gaps, both-positive folds, collapse folds, and MT5 validation/test bucket comparison", "selection_metric_boundary": "exploratory bucket read only; no operating selection metric", "allowed_claims": ["runtime_probe_gap_overnight_context_completed"], "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"]},
        {"packet_id": PACKET_ID, "created_at_utc": created_at, "triggered": True, "blocking": False, "skill": "obsidian-backtest-forensics", "status": "executed", "tester_report": rel(PACKET_ROOT / "attempt_summary.csv"), "tester_settings": f"US100 M5, tester model=4, deposit=500, leverage=1:100, mt5_fold={MT5_FOLD_ID}", "spread_commission_slippage": "broker terminal Strategy Tester report; no synthetic cost overlay", "trade_list_identity": rel(PACKET_ROOT / "trade_level_records.csv"), "forensic_gaps": "none" if summary["external_verification_status"] == "completed" else "blocked_attempts_recorded"},
        {"packet_id": PACKET_ID, "created_at_utc": created_at, "triggered": True, "blocking": False, "skill": "obsidian-artifact-lineage", "status": "executed", "source_inputs": [rel(MODEL_INPUT_PATH), rel(TRAINING_SUMMARY_PATH), rel(ROOT / "stage_pipelines/stage12/extratrees_rolling_wfo_split_probe.py")], "produced_artifacts": [rel(RUN_ROOT / "run_manifest.json"), rel(PACKET_ROOT / "packet_summary.json")], "raw_evidence": [rel(PACKET_ROOT / "execution_results.json"), rel(PACKET_ROOT / "trade_level_records.csv")], "machine_readable": [rel(RUN_ROOT / "summary.json"), rel(PACKET_ROOT / "normalized_kpi_records.jsonl")], "human_readable": [rel(RUN_ROOT / "reports/result_summary.md"), rel(STAGE_REVIEW_PATH)], "hashes_or_missing_reasons": "hashes are recorded in run manifest, packet summary, and normalized KPI where available", "lineage_boundary": "connected_with_boundary; no alpha quality, promotion, or runtime authority claim"},
        {"packet_id": PACKET_ID, "created_at_utc": created_at, "triggered": True, "blocking": False, "skill": "obsidian-exploration-mandate", "status": "executed", "exploration_lane": "Stage 12 ExtraTrees gap-overnight-context-regime probe without fold07", "idea_boundary": "market gap/overnight context structure axis, not model variant or baseline", "negative_memory_effect": "Weak bucket behavior is retained as failure memory and should not trigger micro tuning.", "operating_claim_boundary": "No alpha quality, promotion candidate, operating promotion, or runtime authority."},
        {"packet_id": PACKET_ID, "created_at_utc": created_at, "triggered": True, "blocking": False, "skill": "obsidian-result-judgment", "status": "executed", "judgment_boundary": BOUNDARY, "allowed_claims": ["runtime_probe_gap_overnight_context_completed", "no_fold07_gap_overnight_context_probe_completed"], "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"], "evidence_used": [rel(RUN_ROOT / "results/session_bucket_summary.csv"), rel(PACKET_ROOT / "normalized_kpi_records.jsonl")]},
    ]


def write_reports(summary: Mapping[str, Any]) -> None:
    best = summary["best_python_routed_bucket"]
    routed = [row for row in summary["mt5_routed_rows"] if row.get("route_role") == "routed_total"]
    lines = [
        "# RUN03R Gap/Overnight Context Regime Probe(RUN03R 갭/야간 문맥 국면 탐침)",
        "",
        f"- run(실행): `{RUN_ID}`",
        "- fold07(접힘 7): `excluded(제외)`",
        f"- Python folds(파이썬 접힘): `{','.join(summary['folds_used'])}`",
        f"- MT5 fold(MT5 접힘): `{MT5_FOLD_ID}`",
        "- gap/overnight context bucket(갭/야간 문맥 구간): `down_open/flat_open/up_open`",
        f"- best Python routed bucket(최상위 파이썬 라우팅 구간): `{best.get('session_bucket_label')}`",
        f"- best Python routed validation/test hit(최상위 파이썬 라우팅 검증/시험 적중): `{value_or_na(best.get('validation_weighted_hit_rate'), 6)}` / `{value_or_na(best.get('test_weighted_hit_rate'), 6)}`",
        f"- judgment(판정): `{summary.get('judgment')}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| bucket(구간) | split(분할) | net(순수익) | PF(수익 팩터) | trades(거래) |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in routed:
        lines.append(f"| {row.get('session_bucket_label')} | {row.get('wfo_split_role')} | {row.get('net_profit')} | {row.get('profit_factor')} | {row.get('trade_count')} |")
    lines.extend(["", "효과(effect, 효과): gap/overnight context regime(갭/야간 문맥 국면)이 신호 품질을 가르는지 확인했지만, alpha quality(알파 품질), promotion candidate(승격 후보), runtime authority(런타임 권위)는 아니다."])
    write_text(RUN_ROOT / "reports/result_summary.md", "\n".join(lines))
    closeout = f"""# {PACKET_ID} Closeout Report(마감 보고서)

## Conclusion(결론)

RUN03R(실행 03R)는 fold07(접힘 7)을 쓰지 않고 gap/overnight context regime(갭/야간 문맥 국면)을 탐침했다.

## What changed(무엇이 바뀌었나)

- fold01~fold06(접힘 1~6)만 Python WFO(파이썬 워크포워드 최적화)에 사용했다.
- MT5(메타트레이더5)는 fold05(접힘 5)만 사용했다.
- 신호를 3개 gap/overnight context bucket(갭/야간 문맥 구간)으로 나눴다.

## What gates passed(통과한 관문)

runtime_evidence_gate(런타임 근거 관문), scope_completion_gate(범위 완료 관문), kpi_contract_audit(KPI 계약 감사), work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_lint(스킬 영수증 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 관문 커버리지 감사), final_claim_guard(최종 주장 보호)를 확인했다.

## What gates were not applicable(해당 없음 관문)

없음. MT5(메타트레이더5) runtime evidence(런타임 근거)를 직접 실행했다.

## What is still not enforced(아직 강제하지 않는 것)

full MT5 WFO(전체 MT5 워크포워드 최적화)는 실행하지 않았다. 이 packet(묶음)은 fold07(접힘 7) 없는 gap/overnight context runtime probe(갭/야간 문맥 런타임 탐침)다.

## Allowed claims(허용 주장)

`runtime_probe_gap_overnight_context_completed`, `no_fold07_gap_overnight_context_probe_completed`.

## Forbidden claims(금지 주장)

`alpha_quality(알파 품질)`, `promotion_candidate(승격 후보)`, `operating_promotion(운영 승격)`, `runtime_authority(런타임 권위)`.

## Next hardening step(다음 경화 단계)

특정 bucket(구간)이 반복되면 해당 구간만 별도 model/label(모델/라벨) 축으로 열고, 아니면 failure memory(실패 기억)로 남긴다.
"""
    write_text(PACKET_ROOT / "closeout_report.md", closeout, bom=False)
    plan = "# RUN03R Gap/Overnight Context Regime Probe Plan(RUN03R 갭/야간 문맥 국면 탐침 계획)\n\nfold07(접힘 7)을 제외하고 gap/overnight context regime(갭/야간 문맥 국면) 주제를 탐색한다.\n\n효과(effect, 효과): 모델 변형이 아니라 시장 갭/야간 문맥 구조를 본다.\n"
    review = f"# RUN03R Review Packet(RUN03R 검토 묶음)\n\n`{RUN_ID}` completed(완료). 효과(effect, 효과): fold07(접힘 7) 없이 gap/overnight context bucket(갭/야간 문맥 구간) 근거를 남겼다.\n"
    write_text(PLAN_PATH, plan)
    write_text(STAGE_REVIEW_PATH, review)


def write_run_files(result: Mapping[str, Any], summary: Mapping[str, Any]) -> None:
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
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
    write_json(RUN_ROOT / "kpi_record.json", {**manifest, "kpi_scope": "gap_overnight_context_probe", "model_family": MODEL_FAMILY, "feature_set_id": FEATURE_SET_ID, "label_id": LABEL_ID, "split_contract": SPLIT_CONTRACT, "python_wfo": summary.get("best_python_routed_bucket"), "mt5": {"scoreboard_lane": "runtime_probe_gap_overnight_context", "kpi_records": result.get("mt5_kpi_records", [])}})
    write_reports(summary)


def update_current_truth(summary: Mapping[str, Any]) -> None:
    update_workspace_state(summary)
    update_current_working_state(summary)
    update_selection_status(summary)
    update_changelog(summary)
    update_idea_registry(summary)
    update_negative_register(summary)


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    best = summary["best_python_routed_bucket"]
    block = f"""stage12_model_family_challenge:
  stage_id: {STAGE_ID}
  status: active_gap_overnight_context_probe_completed
  lane: gap_overnight_context_runtime_probe
  current_run_id: {RUN_ID}
  current_run_label: {EXPLORATION_LABEL}
  current_status: reviewed
  current_summary:
    boundary: {BOUNDARY}
    source_wfo_run_id: {SOURCE_WFO_RUN_ID}
    source_recency_run_id: {SOURCE_RECENCY_RUN_ID}
    fold07_used: false
    python_folds_used: fold01,fold02,fold03,fold04,fold05,fold06
    mt5_fold_id: {MT5_FOLD_ID}
    bucket_count: {summary['bucket_count']}
    mt5_attempts_total: {summary['mt5_attempts_total']}
    normalized_records: {summary['normalized_records']}
    trade_level_rows: {summary['trade_level_rows']}
    best_python_routed_bucket: {best.get('session_bucket_label')}
    best_python_routed_validation_hit_rate: {value_or_na(best.get('validation_weighted_hit_rate'), 6)}
    best_python_routed_test_hit_rate: {value_or_na(best.get('test_weighted_hit_rate'), 6)}
    judgment: {summary['judgment']}
    external_verification_status: {summary['external_verification_status']}
    result_summary_path: {rel(RUN_ROOT / 'reports/result_summary.md')}
    packet_summary_path: {rel(PACKET_ROOT / 'packet_summary.json')}
    next_action: continue_stage12_case_collection_one_run_at_a_time
"""
    text = re.sub(r"stage12_model_family_challenge:\n.*?(?=\nagent_control_kpi_rebuild:)", block + "\n", read_text(WORKSPACE_STATE_PATH), flags=re.S)
    write_text(WORKSPACE_STATE_PATH, text)


def replace_section(text: str, heading: str, replacement: str) -> str:
    pattern = rf"\n{re.escape(heading)}.*?(?=\n## |\Z)"
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, "\n" + replacement.rstrip() + "\n", text, flags=re.S)
    return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"


def update_current_working_state(summary: Mapping[str, Any]) -> None:
    best = summary["best_python_routed_bucket"]
    text = re.sub(r"- current run.*?: `[^`]+`", f"- current run(현재 실행): `{RUN_ID}`", read_text(CURRENT_STATE_PATH), count=1)
    section = f"""## RUN03R gap/overnight context regime probe(갭/야간 문맥 국면 탐침)

- run(실행): `{RUN_ID}`
- fold07(접힘 7): `excluded(제외)`
- Python folds(파이썬 접힘): `fold01~fold06`
- MT5 fold(MT5 접힘): `{MT5_FOLD_ID}`
- best Python routed bucket(최상위 파이썬 라우팅 구간): `{best.get('session_bucket_label')}`
- judgment(판정): `{summary['judgment']}`
- boundary(경계): `{BOUNDARY}`
- effect(효과): 모델 변형이 아니라 gap/overnight context regime(갭/야간 문맥 국면) 축을 확인했고, alpha quality(알파 품질)나 promotion candidate(승격 후보)는 만들지 않는다.
"""
    write_text(CURRENT_STATE_PATH, replace_section(text, "## RUN03R gap/overnight context regime probe(갭/야간 문맥 국면 탐침)", section))


def update_selection_status(summary: Mapping[str, Any]) -> None:
    best = summary["best_python_routed_bucket"]
    current = f"""# Stage 12 Selection Status

## Current Read - RUN03R gap/overnight context regime probe(현재 판독 - RUN03R 갭/야간 문맥 국면 탐침)

- current run(현재 실행): `{RUN_ID}`
- fold07(접힘 7): `excluded(제외)`
- Python folds(파이썬 접힘): `fold01~fold06`
- MT5 fold(MT5 접힘): `{MT5_FOLD_ID}`
- best Python routed bucket(최상위 파이썬 라우팅 구간): `{best.get('session_bucket_label')}`
- best Python routed validation/test hit(최상위 파이썬 라우팅 검증/시험 적중): `{value_or_na(best.get('validation_weighted_hit_rate'), 6)}` / `{value_or_na(best.get('test_weighted_hit_rate'), 6)}`
- judgment(판정): `{summary['judgment']}`
- boundary(경계): `{BOUNDARY}`

Effect(효과): fold07(접힘 7) 없이 gap/overnight context regime(갭/야간 문맥 국면) 주제를 확인했다. baseline(기준선)이나 promotion candidate(승격 후보)는 아니다.
"""
    text = read_text(SELECTION_STATUS_PATH) if path_exists(SELECTION_STATUS_PATH) else "# Stage 12 Selection Status\n"
    marker = "\n# Selection Status"
    rest = text[text.find(marker) + 1 :] if marker in text else ""
    write_text(SELECTION_STATUS_PATH, current.rstrip() + "\n\n" + rest.lstrip())


def update_changelog(summary: Mapping[str, Any]) -> None:
    text = read_text(CHANGELOG_PATH)
    if RUN_ID in text:
        return
    entry = f"- 2026-05-01: `{RUN_ID}` completed(완료). fold07(접힘 7) 없이 gap/overnight context-regime probe(갭/야간 문맥 국면 탐침)를 실행했다. attempts(시도) `{summary['mt5_attempts_total']}`, normalized KPI(정규화 KPI) `{summary['normalized_records']}`. Effect(효과): 모델 미세조정이 아니라 갭/야간 문맥 구조 축을 failure/salvage memory(실패/회수 기억)로 남겼다.\n"
    text = text.replace("## 2026-05-01\n\n", "## 2026-05-01\n\n" + entry, 1) if "## 2026-05-01" in text else text.rstrip() + "\n\n## 2026-05-01\n\n" + entry
    write_text(CHANGELOG_PATH, text)


def update_idea_registry(summary: Mapping[str, Any]) -> None:
    text = read_text(IDEA_REGISTRY_PATH)
    if IDEA_ID in text:
        return
    best = summary["best_python_routed_bucket"]
    row = f"| `{IDEA_ID}` | `{STAGE_ID}` | ExtraTrees(엑스트라 트리) 신호는 특정 gap/overnight context regime(갭/야간 문맥 국면)에 집중될 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `runtime_probe_completed_inconclusive` | RUN03R(실행 03R); fold07(접힘 7) 제외; best bucket(최상위 구간) `{best.get('session_bucket_label')}` |\n"
    write_text(IDEA_REGISTRY_PATH, text.replace("## Rule\n", row + "\n## Rule\n", 1) if "## Rule\n" in text else text.rstrip() + "\n" + row)


def update_negative_register(summary: Mapping[str, Any]) -> None:
    best = summary["best_python_routed_bucket"]
    if int(best.get("both_positive_fold_count", 0)) > 0:
        return
    text = read_text(NEGATIVE_REGISTER_PATH)
    if IDEA_ID in text:
        return
    row = f"| `NR-024` | `{IDEA_ID}` | gap/overnight context regime(갭/야간 문맥 국면)만으로 ExtraTrees(엑스트라 트리) 신호가 안정될 수 있다 | RUN03R(실행 03R) best bucket(최상위 구간)의 both-positive fold(양쪽 양수 접힘)는 `{best.get('both_positive_fold_count')}`다 | gap/overnight context bucket(갭/야간 문맥 구간)은 보조 설명 축으로 남긴다 | 특정 bucket(구간)이 다른 label/model(라벨/모델)에서 반복될 때 |\n"
    write_text(NEGATIVE_REGISTER_PATH, text.rstrip() + "\n" + row)


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
    write_csv_rows(PACKET_ROOT / "attempt_summary.csv", ATTEMPT_COLUMNS, attempt_summary_rows(result))
    write_csv_rows(PACKET_ROOT / "mt5_bucket_summary.csv", ("run_id", "session_bucket_id", "session_bucket_label", "record_view", "split", "wfo_split_role", "tier_scope", "route_role", "net_profit", "profit_factor", "trade_count", "status"), mt5_summary_rows(result))
    write_json(PACKET_ROOT / "execution_results.json", [{"run_id": RUN_ID, "compile": result.get("compile", {}), "external_verification_status": result.get("external_verification_status"), "execution_results": result.get("execution_results", []), "strategy_tester_reports": result.get("strategy_tester_reports", [])}])
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


def run_closeout_gate(summary: Mapping[str, Any]) -> None:
    cmd = ["python", "-m", "foundation.control_plane.closeout_gate", "--packet-id", PACKET_ID, "--requested-claim", "completed", "--work-packet", str(PACKET_ROOT / "work_packet.yaml"), "--validate-work-packet-schema", "--state-sync-audit"]
    for check in (
        ("session_summary_rows", "9", RUN_ROOT / "results/session_bucket_summary.csv", "three-gap_overnight_context-buckets-three-tier-summary"),
        ("session_metric_rows", "108", RUN_ROOT / "results/session_bucket_metrics.csv", "fold01-fold06-gap_overnight_context-bucket-metrics"),
        ("mt5_attempt_rows", "18", PACKET_ROOT / "attempt_summary.csv", "fold05-gap_overnight_context-bucket-mt5-attempts"),
        ("normalized_rows", "30", PACKET_ROOT / "normalized_kpi_summary.csv", "normalized-mt5-kpi-summary"),
    ):
        cmd.extend(["--scope-csv-rows", check[0], check[1], str(check[2]), check[3]])
    cmd.extend(["--scope-count", "trade_level_rows", str(summary.get("trade_level_rows")), str(summary.get("trade_level_rows")), "trade-level-record-count"])
    for skill in required_skills():
        cmd.extend(["--required-skill", skill])
    cmd.extend(["--skill-receipt-json", str(PACKET_ROOT / "skill_receipts.json"), "--skill-receipt-schema", "docs/agent_control/skill_receipt_schema.yaml", "--extra-audit-json", str(PACKET_ROOT / "runtime_evidence_gate.json"), "--required-gate-coverage", "--closeout-report", str(PACKET_ROOT / "closeout_report.md"), "--kpi-run-id", RUN_ID, "--kpi-stage-id", STAGE_ID, "--kpi-run-root", str(RUN_ROOT), "--stage-ledger", str(STAGE_RUN_LEDGER_PATH), "--project-ledger", str(PROJECT_ALPHA_LEDGER_PATH), "--expected-stage-ledger-rows", "39", "--expected-project-ledger-rows", "39", "--output-json", str(PACKET_ROOT / "closeout_gate.json")])
    completed = subprocess.run(cmd, cwd=ROOT, check=False, text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stdout + completed.stderr)


def run_probe(args: argparse.Namespace) -> dict[str, Any]:
    for child in ("results", "predictions", "reports"):
        io_path(RUN_ROOT / child).mkdir(parents=True, exist_ok=True)
    metadata, fold_plan, bucket_metrics, bucket_summary, signals = evaluate_python_wfo()
    fold_plan.to_csv(io_path(RUN_ROOT / "results/fold_plan.csv"), index=False, encoding="utf-8")
    bucket_metrics.to_csv(io_path(RUN_ROOT / "results/session_bucket_metrics.csv"), index=False, encoding="utf-8")
    bucket_summary.to_csv(io_path(RUN_ROOT / "results/session_bucket_summary.csv"), index=False, encoding="utf-8")
    signals.to_csv(io_path(RUN_ROOT / "predictions/session_bucket_signal_rows.csv"), index=False, encoding="utf-8")
    prepared = prepare_mt5_run()
    result = execute_mt5(prepared, args)
    write_preliminary_kpi(result)
    normalized_records, normalized_summary_rows, _missing, parser_errors = normalized_rows()
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    trade_enriched, trade_rows, trade_summary_rows, trade_parser_errors = mt5_trade_attribution.enrich_records(normalized_records, ROOT, market_data)
    packet_summary = build_packet_summary(result, bucket_summary, normalized_records, trade_rows, trade_parser_errors)
    packet_summary["metadata"] = metadata
    packet_summary["created_at_utc"] = utc_now()
    ledger_outputs = write_ledgers(packet_summary, result, bucket_summary)
    packet_summary["ledger_outputs"] = ledger_outputs
    write_run_files(result, packet_summary)
    write_packet_files(result=result, normalized_records=normalized_records, normalized_summary_rows=normalized_summary_rows, parser_errors=parser_errors, trade_enriched=trade_enriched, trade_rows=trade_rows, trade_summary_rows=trade_summary_rows, trade_parser_errors=trade_parser_errors, packet_summary=packet_summary)
    update_current_truth(packet_summary)
    run_closeout_gate(packet_summary)
    write_json(RUN_ROOT / "summary.json", packet_summary)
    return packet_summary


def repair_existing_run() -> dict[str, Any]:
    manifest_path = RUN_ROOT / "run_manifest.json"
    kpi_path = RUN_ROOT / "kpi_record.json"
    bucket_summary_path = RUN_ROOT / "results/session_bucket_summary.csv"
    if not path_exists(manifest_path) or not path_exists(kpi_path) or not path_exists(bucket_summary_path):
        raise RuntimeError("RUN03R existing artifacts are incomplete; cannot repair without rerunning.")
    manifest = json.loads(io_path(manifest_path).read_text(encoding="utf-8"))
    result = dict(manifest)
    result = correct_execution_report_links(result)
    result = finalize_result(result)
    write_preliminary_kpi(result)
    normalized_records, normalized_summary_rows, _missing, parser_errors = normalized_rows()
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    trade_enriched, trade_rows, trade_summary_rows, trade_parser_errors = mt5_trade_attribution.enrich_records(normalized_records, ROOT, market_data)
    bucket_summary = pd.read_csv(io_path(bucket_summary_path))
    packet_summary = build_packet_summary(result, bucket_summary, normalized_records, trade_rows, trade_parser_errors)
    existing_summary_path = RUN_ROOT / "summary.json"
    if path_exists(existing_summary_path):
        existing_summary = json.loads(io_path(existing_summary_path).read_text(encoding="utf-8"))
        packet_summary["metadata"] = existing_summary.get("metadata", {})
    packet_summary["created_at_utc"] = utc_now()
    ledger_outputs = write_ledgers(packet_summary, result, bucket_summary)
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
    parser = argparse.ArgumentParser(description="Run Stage 12 gap_overnight_context regime probe without fold07.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--repair-existing", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    summary = repair_existing_run() if args.repair_existing else run_probe(args)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["external_verification_status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())




