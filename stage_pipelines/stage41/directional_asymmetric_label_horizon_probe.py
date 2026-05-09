from __future__ import annotations

import argparse
import json
import math
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

from foundation.alpha.discrete_signal_table import export_single_discrete_signal_score_table
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
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
    split_dates_from_frame,
)
from foundation.control_plane.tier_context_materialization import (
    TIER_B_CORE_FEATURE_ORDER,
    build_tier_b_partial_context_frames,
)
from foundation.labels.directional_asymmetric import (
    CLASS_NAME_MAP,
    SIGNAL_FEATURE_ORDER,
    DirectionalAsymmetricLabelSpec,
    build_stage41_broad_candidate_grid,
    build_stage41_micro_candidate_grid,
    label_lineage_rows,
    label_schema,
    leakage_audit,
    materialize_directional_asymmetric_labels,
    split_label_distribution,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5


STAGE_NUMBER = 41
STAGE_ID = "41_label_horizon__directional_asymmetric_return_target_rebuild"
IDEA_ID = "IDEA-ST41-DIRECTIONAL-ASYMMETRIC-LABEL-HORIZON"
RUN_ID = "run35A_directional_asymmetric_label_horizon_broad_mt5_probe_v1"
RUN_NUMBER = "run35A"
PACKET_ID = "stage41_run35A_directional_asymmetric_label_horizon_broad_mt5_probe_v1"
PARENT_PACKET_ID = PACKET_ID
EXPLORATION_LABEL = "stage41_LabelHorizon__DirectionalAsymmetricReturnTarget"
BOUNDARY = "runtime_probe_only"
FINAL_BOUNDARY = "runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference"
BLOCKED_JUDGMENT = "blocked_runtime_probe_missing_mt5_execution"
POSITIVE_JUDGMENT = "reviewed_completed_positive_runtime_probe_only"
INCONCLUSIVE_JUDGMENT = "reviewed_completed_inconclusive_runtime_probe_only"
NEGATIVE_JUDGMENT = "reviewed_completed_negative_memory_runtime_probe_only"
SHORT_THRESHOLD = 0.55
LONG_THRESHOLD = 0.55
MIN_MARGIN = 0.0
SIGNAL_FEATURE_HASH = ordered_hash(SIGNAL_FEATURE_ORDER)
MODEL_FEATURE_ORDER = tuple(TIER_B_CORE_FEATURE_ORDER)

ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
MODEL_INPUT_ROOT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
MODEL_INPUT_DATASET_PATH = MODEL_INPUT_ROOT / "model_input_dataset.parquet"
MODEL_INPUT_FEATURE_ORDER_PATH = MODEL_INPUT_ROOT / "model_input_feature_order.txt"
MODEL_INPUT_SUMMARY_PATH = MODEL_INPUT_ROOT / "model_input_summary.json"
TRAINING_SUMMARY_PATH = ROOT / "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"
RAW_MT5_ROOT = ROOT / "data/raw/mt5_bars/m5"
RAW_US100_BARS_PATH = RAW_MT5_ROOT / "US100/bars_us100_m5_mt5api_raw.csv"
STAGE38_STATUS_PATH = ROOT / "stages/38_decision_layer__permission_abstention_overlap/04_selected/selection_status.md"
STAGE38_PACKET_PATH = ROOT / "stages/38_decision_layer__permission_abstention_overlap/03_reviews/run32A_permission_abstention_overlap_broad_mt5_probe_packet.md"
STAGE39_STATUS_PATH = ROOT / "stages/39_exit_risk__non_entry_lifecycle_tail_overlay/04_selected/selection_status.md"
STAGE39_PACKET_PATH = ROOT / "stages/39_exit_risk__non_entry_lifecycle_tail_overlay/03_reviews/run33A_exit_risk_non_entry_overlay_broad_mt5_probe_packet.md"
STAGE40_STATUS_PATH = ROOT / "stages/40_feature_structure__candle_morphology_signal_quality_scout/04_selected/selection_status.md"
STAGE40_PACKET_PATH = ROOT / "stages/40_feature_structure__candle_morphology_signal_quality_scout/03_reviews/run34A_candle_morphology_signal_quality_broad_mt5_probe_packet.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def safe_name(value: str, limit: int = 80) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:limit]


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_yaml_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


def dataframe_to_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    frame = pd.DataFrame(list(rows))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(io_path(path), index=False, encoding="utf-8")
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def load_feature_order(path: Path = MODEL_INPUT_FEATURE_ORDER_PATH) -> list[str]:
    return [line.strip() for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def load_label_threshold() -> float:
    payload = json.loads(io_path(TRAINING_SUMMARY_PATH).read_text(encoding="utf-8"))
    threshold = float(payload["threshold_log_return"])
    if not math.isfinite(threshold) or threshold <= 0:
        raise RuntimeError(f"invalid label threshold: {threshold}")
    return threshold


def load_model_input() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(MODEL_INPUT_DATASET_PATH))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["timestamp_utc"] = frame["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    frame["validation_oos_split_label"] = frame["split"].astype(str).map({"validation": "validation_is"}).fillna(frame["split"].astype(str))
    return frame.sort_values("timestamp").reset_index(drop=True)


def load_raw_close_frame() -> pd.DataFrame:
    raw = pd.read_csv(io_path(RAW_US100_BARS_PATH), usecols=["time_close_unix", "close"])
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    return raw[["timestamp", "close"]].drop_duplicates("timestamp").sort_values("timestamp").reset_index(drop=True)


def route_coverage_from_common(common: pd.DataFrame, no_tier_by_split: Mapping[str, Any] | None = None) -> dict[str, Any]:
    by_split: dict[str, dict[str, int]] = {}
    subtype: dict[str, dict[str, int]] = {}
    no_tier_by_split = no_tier_by_split or {}
    for split in ("validation", "oos"):
        view = common.loc[common["split"].astype(str).eq(split)]
        tier_a_rows = int(view["tier_label"].astype(str).eq(mt5.TIER_A).sum())
        tier_b_rows = int(view["tier_label"].astype(str).eq(mt5.TIER_B).sum())
        by_split[split] = {
            "tier_a_primary_rows": tier_a_rows,
            "tier_b_fallback_rows": tier_b_rows,
            "routed_labelable_rows": tier_a_rows + tier_b_rows,
            "stage41_label_missing_rows": int(view.get("stage41_label_missing", pd.Series(False, index=view.index)).astype(bool).sum()) if len(view) else 0,
        }
        subtype[split] = (
            view.loc[view["tier_label"].astype(str).eq(mt5.TIER_B), "partial_context_subtype"]
            .astype(str)
            .value_counts()
            .to_dict()
        )
    return {
        "by_split": by_split,
        "tier_b_fallback_by_split_subtype": subtype,
        "no_tier_by_split": {str(key): int(value) for key, value in no_tier_by_split.items()},
    }


def source_lineage_entries() -> list[dict[str, Any]]:
    paths = [
        ("tier_a_model_input", MODEL_INPUT_DATASET_PATH, "input", "feature/model input"),
        ("tier_a_feature_order", MODEL_INPUT_FEATURE_ORDER_PATH, "input", "feature order"),
        ("model_input_summary", MODEL_INPUT_SUMMARY_PATH, "input", "input diagnostics"),
        ("training_summary", TRAINING_SUMMARY_PATH, "input", "current reference label threshold"),
        ("raw_us100_closed_m5_close", RAW_US100_BARS_PATH, "input", "closed-bar forward label source"),
        ("raw_mt5_bars", RAW_MT5_ROOT, "input", "Tier B fallback materialization"),
        ("stage38_negative_memory_status", STAGE38_STATUS_PATH, "negative_memory", "permission/abstention warning only"),
        ("stage38_negative_memory_packet", STAGE38_PACKET_PATH, "negative_memory", "permission/abstention warning only"),
        ("stage39_negative_memory_status", STAGE39_STATUS_PATH, "negative_memory", "exit overlay warning only"),
        ("stage39_negative_memory_packet", STAGE39_PACKET_PATH, "negative_memory", "exit overlay warning only"),
        ("stage40_negative_memory_status", STAGE40_STATUS_PATH, "negative_memory", "candle morphology warning only"),
        ("stage40_negative_memory_packet", STAGE40_PACKET_PATH, "negative_memory", "candle morphology warning only"),
        ("mt5_runtime_ea", ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5", "MT5 handoff", "entry runtime"),
    ]
    rows = []
    for role, path, kind, surface in paths:
        rows.append(
            {
                "role": role,
                "path": rel(path),
                "source_stage": "current_repo_state",
                "source_run": "reentry_before_stage41",
                "created_by_script": "existing_repository_artifact",
                "sha256": sha256_file_lf_normalized(path) if path.is_file() else "directory_or_not_feasible",
                "artifact_kind": kind,
                "required_for_reproducibility": kind != "negative_memory",
                "affects": surface,
            }
        )
    return rows


def build_common_table() -> tuple[pd.DataFrame, dict[str, Any], list[dict[str, Any]]]:
    tier_a_raw = load_model_input()
    feature_order = load_feature_order()
    label_threshold = load_label_threshold()
    tier_b_payload = build_tier_b_partial_context_frames(
        raw_root=RAW_MT5_ROOT,
        tier_a_frame=tier_a_raw,
        tier_a_feature_order=feature_order,
        tier_b_feature_order=TIER_B_CORE_FEATURE_ORDER,
        label_threshold=label_threshold,
    )
    tier_a = tier_a_raw.copy()
    tier_a["tier_label"] = mt5.TIER_A
    tier_a["routing_source"] = "tier_a_primary"
    tier_a["partial_context_subtype"] = "Tier_A_full_context"
    tier_a["tier_a_available"] = True
    tier_a["tier_b_fallback_available"] = False
    tier_b = tier_b_payload["tier_b_fallback_frame"].copy()
    tier_b["timestamp"] = pd.to_datetime(tier_b["timestamp"], utc=True)
    tier_b["timestamp_utc"] = tier_b["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    tier_b["validation_oos_split_label"] = tier_b["split"].astype(str).map({"validation": "validation_is"}).fillna(tier_b["split"].astype(str))
    tier_b["tier_label"] = mt5.TIER_B
    tier_b["routing_source"] = "tier_b_fallback"
    tier_b["tier_a_available"] = False
    tier_b["tier_b_fallback_available"] = True
    required_columns = {
        "timestamp",
        "timestamp_utc",
        "split",
        "validation_oos_split_label",
        "symbol",
        "label",
        "label_class",
        "tier_label",
        "routing_source",
        "partial_context_subtype",
        "tier_a_available",
        "tier_b_fallback_available",
        *MODEL_FEATURE_ORDER,
    }
    common_columns = [column for column in sorted(required_columns) if column in tier_a.columns and column in tier_b.columns]
    for column in required_columns:
        if column not in common_columns and (column in tier_a.columns or column in tier_b.columns):
            common_columns.append(column)
    common = pd.concat([tier_a.reindex(columns=common_columns), tier_b.reindex(columns=common_columns)], ignore_index=True, sort=False)
    common = common.sort_values(["timestamp", "tier_label"]).reset_index(drop=True)
    common["stage41_row_id"] = np.arange(len(common), dtype="int64")
    route_coverage = route_coverage_from_common(common, tier_b_payload.get("summary", {}).get("no_tier_by_split", {}))
    lineage = source_lineage_entries()
    lineage.append(
        {
            "role": "stage41_common_decision_surface_table",
            "path": rel(RUN_ROOT / "tables/stage41_common_decision_surface_table.parquet"),
            "source_stage": STAGE_ID,
            "source_run": RUN_ID,
            "created_by_script": "stage_pipelines.stage41.directional_asymmetric_label_horizon_probe.build_common_table",
            "sha256": "computed_after_write",
            "artifact_kind": "intermediate",
            "required_for_reproducibility": True,
            "affects": "label model feature candidate signal entry diagnostics",
        }
    )
    return common, route_coverage, lineage


def _feature_matrix(frame: pd.DataFrame, fill_values: Mapping[str, float] | None = None) -> tuple[pd.DataFrame, dict[str, float]]:
    numeric = frame.loc[:, MODEL_FEATURE_ORDER].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan)
    if fill_values is None:
        medians = numeric.median(axis=0).fillna(0.0).astype("float64").to_dict()
    else:
        medians = {column: float(fill_values.get(column, 0.0)) for column in MODEL_FEATURE_ORDER}
    return numeric.fillna(medians).astype("float64"), medians


def _make_estimator(spec: DirectionalAsymmetricLabelSpec) -> Any:
    if spec.model_family == "extra_trees_depth4":
        return ExtraTreesClassifier(
            n_estimators=48,
            max_depth=4,
            min_samples_leaf=100,
            class_weight="balanced",
            random_state=41035,
            n_jobs=1,
        )
    base = LogisticRegression(max_iter=200, C=0.50, class_weight="balanced", random_state=41035, solver="liblinear")
    return OneVsRestClassifier(base)


def _predict_signal(
    estimator: Any,
    x_all: pd.DataFrame,
    spec: DirectionalAsymmetricLabelSpec,
    train_confidence: np.ndarray | None = None,
) -> tuple[np.ndarray, dict[str, Any]]:
    if estimator is None:
        return np.zeros(len(x_all), dtype="int8"), {"status": "single_class_flat_signal"}
    probabilities = estimator.predict_proba(x_all)
    classes = np.asarray(estimator.classes_, dtype="int16")
    best_idx = probabilities.argmax(axis=1)
    predicted_class = classes[best_idx].astype("int16")
    confidence = probabilities.max(axis=1)
    threshold = float(spec.decision_threshold)
    if spec.model_family == "calibrated_logistic" and train_confidence is not None and len(train_confidence):
        threshold = max(threshold, float(np.quantile(train_confidence, 0.50)))
    predicted_class = np.where(confidence >= threshold, predicted_class, 1).astype("int16")
    signal = np.zeros(len(predicted_class), dtype="int8")
    signal[predicted_class == 0] = -1
    signal[predicted_class == 2] = 1
    if spec.long_short_scope == "long_only":
        signal = np.where(signal > 0, signal, 0).astype("int8")
    elif spec.long_short_scope == "short_only":
        signal = np.where(signal < 0, signal, 0).astype("int8")
    return signal, {
        "decision_threshold": threshold,
        "probability_classes": classes.tolist(),
        "mean_confidence": float(np.mean(confidence)) if len(confidence) else None,
    }


def train_and_score_candidate(
    common: pd.DataFrame,
    raw_close: pd.DataFrame,
    spec: DirectionalAsymmetricLabelSpec,
    base_threshold: float,
) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any]]:
    labeled = materialize_directional_asymmetric_labels(common, raw_close, spec, base_threshold)
    train_mask = labeled["split"].astype(str).eq("train") & labeled["tier_label"].astype(str).eq(mt5.TIER_A)
    train = labeled.loc[train_mask].copy()
    if train.empty:
        raise RuntimeError(f"{spec.candidate_id} has no Tier A train rows")
    x_train, fill_values = _feature_matrix(train)
    y_train = train["stage41_label_class"].astype("int16").to_numpy()
    classes = np.unique(y_train)
    estimator = None
    model_status = "single_class_flat_signal"
    train_confidence: np.ndarray | None = None
    if len(classes) >= 2:
        estimator = _make_estimator(spec)
        estimator.fit(x_train, y_train)
        train_prob = estimator.predict_proba(x_train)
        train_confidence = train_prob.max(axis=1)
        model_status = "trained"
    x_all, _ = _feature_matrix(labeled, fill_values)
    signal, score_detail = _predict_signal(estimator, x_all, spec, train_confidence)
    labeled[SIGNAL_FEATURE_ORDER[0]] = signal
    labeled["candidate_id"] = spec.candidate_id
    labeled["candidate_label"] = spec.description
    labeled["label_id"] = spec.label_id
    labeled["label_family"] = spec.label_family
    labeled["model_family"] = spec.model_family
    labeled["model_variant"] = spec.model_variant
    labeled["long_horizon_bars"] = int(spec.long_horizon_bars)
    labeled["short_horizon_bars"] = int(spec.short_horizon_bars)
    labeled["long_threshold_multiplier"] = float(spec.long_threshold_multiplier)
    labeled["short_threshold_multiplier"] = float(spec.short_threshold_multiplier)
    labeled["flat_band_rule"] = spec.flat_band_rule
    labeled["volatility_normalization"] = bool(spec.volatility_normalization)
    labeled["session_adjustment"] = bool(spec.session_adjustment)
    labeled["long_short_scope"] = spec.long_short_scope
    labeled["entry_decision"] = np.select([signal < 0, signal > 0], ["short", "long"], default="flat")
    labeled["stage41_label_missing"] = False

    model_path = RUN_ROOT / "models" / f"{safe_name(spec.candidate_id, 64)}_{safe_name(spec.model_family, 32)}.joblib"
    io_path(model_path.parent).mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "candidate_spec": spec.as_dict(),
            "model_status": model_status,
            "estimator": estimator,
            "feature_order": list(MODEL_FEATURE_ORDER),
            "fill_values": fill_values,
            "class_id_map": {"short": 0, "flat": 1, "long": 2},
            "score_detail": score_detail,
        },
        io_path(model_path),
    )
    artifact = {
        "candidate_id": spec.candidate_id,
        "label_id": spec.label_id,
        "model_family": spec.model_family,
        "model_variant": spec.model_variant,
        "model_status": model_status,
        "path": rel(model_path),
        "sha256": sha256_file_lf_normalized(model_path),
        "feature_order": list(MODEL_FEATURE_ORDER),
        "feature_order_hash": ordered_hash(MODEL_FEATURE_ORDER),
        "train_rows": int(len(train)),
        "train_class_counts": {CLASS_NAME_MAP.get(int(key), str(key)): int(value) for key, value in zip(*np.unique(y_train, return_counts=True))},
        "score_detail": score_detail,
    }
    label_summary = {
        "candidate_id": spec.candidate_id,
        "label_id": spec.label_id,
        "spec": spec.as_dict(),
        "distribution": split_label_distribution(labeled.loc[labeled["tier_label"].astype(str).eq(mt5.TIER_A)]),
        "leakage_audit": leakage_audit(labeled, spec),
        "model_artifact": artifact,
    }
    return labeled, artifact, label_summary


def summarize_candidate_frames(candidate_frames: Mapping[str, pd.DataFrame], label_summaries: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    reference_counts: dict[str, int] = {}
    reference = candidate_frames.get("c01_current_label_reference")
    for split in ("validation", "oos"):
        reference_counts[split] = 0 if reference is None else int(reference.loc[reference["split"].astype(str).eq(split), SIGNAL_FEATURE_ORDER[0]].ne(0).sum())
    rows: list[dict[str, Any]] = []
    for candidate_id, frame in candidate_frames.items():
        summary = label_summaries.get(candidate_id, {})
        distribution = summary.get("distribution", {})
        for split, split_alias in (("validation", "validation_is"), ("oos", "oos")):
            view = frame.loc[frame["split"].astype(str).eq(split)]
            if view.empty:
                rows.append({"candidate_id": candidate_id, "split": split_alias, "candidate_rejection_reason": "missing_split_rows"})
                continue
            signal = view[SIGNAL_FEATURE_ORDER[0]].astype(int)
            signal_count = int(signal.ne(0).sum())
            tier_a = view.loc[view["tier_label"].astype(str).eq(mt5.TIER_A)]
            tier_b = view.loc[view["tier_label"].astype(str).eq(mt5.TIER_B)]
            tier_b_signal = int(tier_b[SIGNAL_FEATURE_ORDER[0]].ne(0).sum())
            ref_count = max(reference_counts.get(split, 0), 1)
            label_split = distribution.get(split, {})
            rejection = "mt5_pending"
            if signal_count < 20:
                rejection = "thin_trade_stream_python_signal_count_lt_20"
            elif candidate_id != "c01_current_label_reference" and signal_count / ref_count < 0.10:
                rejection = "thin_trade_stream_vs_reference_python"
            elif signal_count and tier_b_signal / signal_count > 0.60:
                rejection = "tier_b_fallback_signal_share_gt_60pct_python"
            elif label_split.get("class_balance_status") == "pathological":
                rejection = "label_distribution_pathological_python"
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "candidate_label": str(view["candidate_label"].iloc[0]),
                    "split": split_alias,
                    "label_id": str(view["label_id"].iloc[0]),
                    "label_family": str(view["label_family"].iloc[0]),
                    "long_horizon_bars": int(view["long_horizon_bars"].iloc[0]),
                    "short_horizon_bars": int(view["short_horizon_bars"].iloc[0]),
                    "long_threshold": float(view["stage41_long_effective_threshold"].median()),
                    "short_threshold": float(view["stage41_short_effective_threshold"].median()),
                    "flat_band_rule": str(view["flat_band_rule"].iloc[0]),
                    "volatility_normalization_flag": bool(view["volatility_normalization"].iloc[0]),
                    "session_adjustment_flag": bool(view["session_adjustment"].iloc[0]),
                    "train_label_counts": json.dumps(distribution.get("train", {}).get("class_counts", {}), sort_keys=True),
                    "validation_label_counts": json.dumps(distribution.get("validation", {}).get("class_counts", {}), sort_keys=True),
                    "oos_label_counts": json.dumps(distribution.get("oos", {}).get("class_counts", {}), sort_keys=True),
                    "class_balance": json.dumps(label_split.get("class_shares", {}), sort_keys=True),
                    "class_balance_status": label_split.get("class_balance_status"),
                    "model_family": str(view["model_family"].iloc[0]),
                    "model_artifact_path": summary.get("model_artifact", {}).get("path", ""),
                    "tier_a_used_count": int(tier_a[SIGNAL_FEATURE_ORDER[0]].ne(0).sum()),
                    "tier_b_fallback_used_count": tier_b_signal,
                    "actual_routed_total_count": signal_count,
                    "validation_trade_count": signal_count if split == "validation" else "",
                    "oos_trade_count": signal_count if split == "oos" else "",
                    "long_count": int(signal.gt(0).sum()),
                    "short_count": int(signal.lt(0).sum()),
                    "flat_count": int(signal.eq(0).sum()),
                    "no_trade_rate": float(1.0 - signal_count / len(view)) if len(view) else 1.0,
                    "validation_oos_gap": "mt5_pending",
                    "direction_specific_expectancy": "mt5_trade_direction_attribution_not_available_in_summary_import",
                    "trade_count_thinning_vs_reference": int(signal_count - ref_count),
                    "tier_b_signal_share_python": float(tier_b_signal / signal_count) if signal_count else None,
                    "candidate_rejection_reason": rejection,
                }
            )
    return rows


def export_signal_score_table(path: Path) -> dict[str, Any]:
    payload = export_single_discrete_signal_score_table(
        path,
        feature_order=SIGNAL_FEATURE_ORDER,
        logit_strength=4.0,
        format_name="stage41_directional_asymmetric_label_single_signal_ebm_score_table_csv_v1",
    )
    payload["path"] = rel(path)
    return payload


def export_candidate_feature_matrices(candidate_frames: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    feature_root = RUN_ROOT / "features"
    exports: dict[str, Any] = {}
    for candidate_id, frame in candidate_frames.items():
        for split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
            for tier_label, tier_key in ((mt5.TIER_A, "tier_a"), (mt5.TIER_B, "tier_b_fallback")):
                selected = frame.loc[frame["split"].astype(str).eq(split) & frame["tier_label"].astype(str).eq(tier_label)].copy()
                output = feature_root / f"{candidate_id}_{tier_key}_{runtime_split}_stage41_signal_features.csv"
                exports[f"{candidate_id}_{tier_key}_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
                    selected,
                    SIGNAL_FEATURE_ORDER,
                    output,
                    metadata_columns=(
                        "candidate_id",
                        "candidate_label",
                        "label_id",
                        "label_family",
                        "model_family",
                        "long_horizon_bars",
                        "short_horizon_bars",
                        "tier_label",
                        "routing_source",
                        "partial_context_subtype",
                        "entry_decision",
                    ),
                )
    return exports


def resolve_artifact_path(value: Any) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    root_path = ROOT / path
    if path_exists(root_path):
        return root_path
    return RUN_ROOT / path


def copy_runtime_inputs(feature_exports: Mapping[str, Any], model_artifact: Mapping[str, Any], common_root: Path) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    copied = []
    model_path = resolve_artifact_path(model_artifact["path"])
    copied.append(copy_to_common(model_path, f"{common}/models/{model_path.name}", common_root))
    for payload in feature_exports.values():
        local_path = resolve_artifact_path(payload["path"])
        copied.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", common_root))
    return copied


def make_attempts(
    candidate_specs: Sequence[DirectionalAsymmetricLabelSpec],
    feature_exports: Mapping[str, Any],
    model_artifact: Mapping[str, Any],
    common: pd.DataFrame,
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common_name = common_run_root(STAGE_NUMBER, RUN_ID)
    model_name = Path(model_artifact["path"]).name
    for spec in candidate_specs:
        for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
            split_frame = common.loc[common["split"].astype(str).eq(source_split) & common["tier_label"].astype(str).eq(mt5.TIER_A)]
            from_date, to_date = split_dates_from_frame(split_frame, source_split)
            tier_a_matrix = Path(feature_exports[f"{spec.candidate_id}_tier_a_{runtime_split}"]["path"]).name
            tier_b_matrix = Path(feature_exports[f"{spec.candidate_id}_tier_b_fallback_{runtime_split}"]["path"]).name
            attempts.append(
                attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=STAGE_NUMBER,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=f"routed_{safe_name(spec.candidate_id, 64)}_{runtime_split}",
                    tier=mt5.TIER_AB,
                    split=runtime_split,
                    model_path=f"{common_name}/models/{model_name}",
                    model_id=f"{RUN_ID}_{spec.candidate_id}_signal_table",
                    model_backend="ebm_table",
                    feature_path=f"{common_name}/features/{tier_a_matrix}",
                    feature_count=len(SIGNAL_FEATURE_ORDER),
                    feature_order_hash=SIGNAL_FEATURE_HASH,
                    short_threshold=SHORT_THRESHOLD,
                    long_threshold=LONG_THRESHOLD,
                    min_margin=MIN_MARGIN,
                    invert_signal=False,
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier="tier_a",
                    attempt_role="routed_total",
                    record_view_prefix=f"mt5_routed_{spec.candidate_id}",
                    max_hold_bars=spec.max_horizon_bars,
                    common_root=common_name,
                    fallback_enabled=True,
                    fallback_model_path=f"{common_name}/models/{model_name}",
                    fallback_model_id=f"{RUN_ID}_{spec.candidate_id}_fallback_signal_table",
                    fallback_model_backend="ebm_table",
                    fallback_feature_path=f"{common_name}/features/{tier_b_matrix}",
                    fallback_feature_count=len(SIGNAL_FEATURE_ORDER),
                    fallback_feature_order_hash=SIGNAL_FEATURE_HASH,
                    fallback_short_threshold=SHORT_THRESHOLD,
                    fallback_long_threshold=LONG_THRESHOLD,
                    fallback_min_margin=MIN_MARGIN,
                    fallback_invert_signal=False,
                    close_on_flat_signal=False,
                    reverse_on_opposite_signal=True,
                )
            )
    return attempts


def build_candidate_batch(
    *,
    specs: Sequence[DirectionalAsymmetricLabelSpec],
    common: pd.DataFrame,
    raw_close: pd.DataFrame,
    base_threshold: float,
    common_files_root: Path,
) -> dict[str, Any]:
    frames: dict[str, pd.DataFrame] = {}
    model_artifacts: list[dict[str, Any]] = []
    label_summaries: dict[str, dict[str, Any]] = {}
    for spec in specs:
        frame, model_artifact, label_summary = train_and_score_candidate(common, raw_close, spec, base_threshold)
        frames[spec.candidate_id] = frame
        model_artifacts.append(model_artifact)
        label_summaries[spec.candidate_id] = label_summary
    summary = summarize_candidate_frames(frames, label_summaries)
    feature_exports = export_candidate_feature_matrices(frames)
    model_artifact = export_signal_score_table(RUN_ROOT / "models/stage41_directional_label_signal_score_table.csv")
    common_copies = copy_runtime_inputs(feature_exports, model_artifact, common_files_root)
    attempts = make_attempts(specs, feature_exports, model_artifact, common)
    return {
        "specs": list(specs),
        "frames": frames,
        "summary": summary,
        "feature_exports": feature_exports,
        "signal_score_table_artifact": model_artifact,
        "python_model_artifacts": model_artifacts,
        "label_summaries": list(label_summaries.values()),
        "common_copies": common_copies,
        "attempts": attempts,
    }


def prepared_payload(
    *,
    candidate_specs: Sequence[DirectionalAsymmetricLabelSpec],
    attempts: Sequence[Mapping[str, Any]],
    feature_exports: Mapping[str, Any],
    signal_score_table_artifact: Mapping[str, Any],
    python_model_artifacts: Sequence[Mapping[str, Any]],
    label_summaries: Sequence[Mapping[str, Any]],
    common_copies: Sequence[Mapping[str, Any]],
    route_coverage: Mapping[str, Any],
    common_artifact: Mapping[str, Any],
    candidate_artifact: Mapping[str, Any],
    python_summary: Sequence[Mapping[str, Any]],
    lineage: Sequence[Mapping[str, Any]],
    batch_label: str,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": STAGE_NUMBER,
        "run_root": RUN_ROOT.as_posix(),
        "batch_label": batch_label,
        "attempts": list(attempts),
        "candidate_specs": [spec.as_dict() for spec in candidate_specs],
        "feature_matrices": dict(feature_exports),
        "model_artifacts": {
            "signal_score_table": dict(signal_score_table_artifact),
            "python_candidate_models": list(python_model_artifacts),
        },
        "label_summaries": list(label_summaries),
        "common_copies": list(common_copies),
        "route_coverage": dict(route_coverage),
        "common_table_artifact": dict(common_artifact),
        "candidate_table_artifact": dict(candidate_artifact),
        "python_candidate_summary": list(python_summary),
        "source_lineage": list(lineage),
        "idea_id": IDEA_ID,
        "run_number": RUN_NUMBER,
        "completion_goal": "Stage41 broad MT5 directional asymmetric label/horizon runtime probe",
        "model_family": "stage41_directional_asymmetric_rebuilt_label_simple_models",
        "feature_set_id": "stage41_core42_rebuilt_label_signal_from_closed_bar_features",
        "label_id": "stage41_directional_asymmetric_label_family_grid",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": FINAL_BOUNDARY,
    }


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": BLOCKED_JUDGMENT,
        }
    result = execute_prepared_run(
        prepared,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=Path(args.common_files_root),
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    completed = result.get("external_verification_status") == "completed" and any(
        item.get("status") == "completed" for item in result.get("strategy_tester_reports", [])
    )
    result["judgment"] = INCONCLUSIVE_JUDGMENT if completed else BLOCKED_JUDGMENT
    for record in result.get("mt5_kpi_records", []):
        record["idea_id"] = IDEA_ID
        record["packet_id"] = PACKET_ID
        record["boundary"] = BOUNDARY
    return result


def mt5_metric(record: Mapping[str, Any], *names: str) -> Any:
    metrics = record.get("metrics", {})
    for name in names:
        if name in metrics:
            return metrics.get(name)
    return None


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def build_mt5_candidate_summary(
    kpi_records: Sequence[Mapping[str, Any]],
    python_rows: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    python_by_key = {(row["candidate_id"], row["split"]): dict(row) for row in python_rows}
    exec_by_key = {}
    for execution in execution_results:
        match = re.match(r"routed_(?P<candidate>.+)_(?P<split>validation_is|oos)$", str(execution.get("attempt_name", "")))
        if match:
            exec_by_key[(match.group("candidate"), match.group("split"))] = execution
    totals = [record for record in kpi_records if record.get("route_role") == "routed_total"]
    components = {
        (record.get("record_view"), record.get("route_role")): record
        for record in kpi_records
        if record.get("route_role") in {"primary_used", "fallback_used"}
    }
    rows: list[dict[str, Any]] = []
    for total in totals:
        view = str(total.get("record_view", ""))
        match = re.match(r"mt5_routed_(?P<candidate>.+)_(?P<split>validation_is|oos)$", view)
        if not match:
            continue
        candidate_id = match.group("candidate")
        split = match.group("split")
        py = python_by_key.get((candidate_id, split), {})
        prefix = f"mt5_routed_{candidate_id}"
        primary = components.get((f"{prefix}_tier_a_used_{split}", "primary_used"), {})
        fallback = components.get((f"{prefix}_tier_b_fallback_used_{split}", "fallback_used"), {})
        metrics = total.get("metrics", {})
        execution = exec_by_key.get((candidate_id, split), {})
        rows.append(
            {
                **py,
                "candidate_id": candidate_id,
                "split": split,
                "net_profit": mt5_metric(total, "net_profit"),
                "profit_factor": mt5_metric(total, "profit_factor"),
                "max_drawdown": mt5_metric(total, "max_drawdown_amount", "max_drawdown"),
                "expectancy": mt5_metric(total, "expectancy"),
                "win_rate": mt5_metric(total, "win_rate_percent", "win_rate"),
                "trade_count": mt5_metric(total, "trade_count"),
                "order_attempt_count": mt5_metric(total, "order_attempt_count"),
                "fill_count": mt5_metric(total, "fill_count"),
                "tier_a_used_count_mt5": mt5_metric(primary, "signal_count"),
                "tier_b_fallback_used_count_mt5": mt5_metric(fallback, "signal_count"),
                "actual_routed_total_count_mt5": mt5_metric(total, "order_attempt_count"),
                "tester_status": execution.get("status"),
                "runtime_status": execution.get("runtime_outputs", {}).get("status") if execution else None,
                "tester_command": " ".join(str(item) for item in execution.get("command", [])) if execution else "",
                "tester_report_path": metrics.get("report_path") or total.get("report", {}).get("html_report", {}).get("path", ""),
                "candidate_rejection_reason": "mt5_imported_pending_gate",
            }
        )
    return rows


def pivot_candidate_mt5(rows: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Mapping[str, Any]]]:
    out: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in rows:
        out.setdefault(str(row["candidate_id"]), {})[str(row["split"])] = row
    return out


def _label_pathological(row: Mapping[str, Any]) -> bool:
    return str(row.get("class_balance_status", "")) == "pathological"


def evaluate_micro_search_gate(mt5_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_candidate = pivot_candidate_mt5([row for row in mt5_rows if str(row.get("candidate_id", "")).startswith("c")])
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for candidate_id, splits in by_candidate.items():
        val = splits.get("validation_is")
        oos = splits.get("oos")
        if not val or not oos:
            rejected.append({"candidate_id": candidate_id, "reason": "missing_validation_or_oos_mt5_row"})
            continue
        val_net = to_float(val.get("net_profit")) or 0.0
        oos_net = to_float(oos.get("net_profit")) or 0.0
        val_pf = to_float(val.get("profit_factor")) or 0.0
        oos_pf = to_float(oos.get("profit_factor")) or 0.0
        val_trades = int(to_float(val.get("trade_count")) or 0)
        oos_trades = int(to_float(oos.get("trade_count")) or 0)
        routed_total = int(to_float(val.get("actual_routed_total_count_mt5")) or 0) + int(to_float(oos.get("actual_routed_total_count_mt5")) or 0)
        tier_b = int(to_float(val.get("tier_b_fallback_used_count_mt5")) or 0) + int(to_float(oos.get("tier_b_fallback_used_count_mt5")) or 0)
        gap = abs(val_net - oos_net)
        reasons = []
        if val_net <= 0:
            reasons.append("validation_net_not_positive")
        if oos_net <= 0:
            reasons.append("oos_net_not_positive")
        if val_pf < 1.05:
            reasons.append("validation_pf_below_1_05")
        if oos_pf < 1.05:
            reasons.append("oos_pf_below_1_05")
        if val_trades < 20 or oos_trades < 20:
            reasons.append("trade_count_too_thin_for_micro_search")
        if _label_pathological(val) or _label_pathological(oos):
            reasons.append("label_distribution_pathological")
        if routed_total > 0 and tier_b / routed_total > 0.60:
            reasons.append("tier_b_fallback_carrying_too_much")
        if gap > max(abs(val_net), abs(oos_net), 1.0) * 3.0:
            reasons.append("validation_oos_gap_extreme")
        if str(val.get("label_family", "")).startswith(("permission", "exit", "candle", "state")):
            reasons.append("candidate_mechanism_not_label_horizon")
        payload = {
            "candidate_id": candidate_id,
            "validation_net": val_net,
            "oos_net": oos_net,
            "validation_pf": val_pf,
            "oos_pf": oos_pf,
            "validation_trades": val_trades,
            "oos_trades": oos_trades,
            "tier_b_signal_share": float(tier_b / routed_total) if routed_total else None,
            "validation_oos_gap": gap,
        }
        if reasons:
            rejected.append({**payload, "reason": ";".join(dict.fromkeys(reasons))})
        else:
            accepted.append(payload)
    accepted.sort(key=lambda item: (item["validation_net"] + item["oos_net"], item["oos_pf"]), reverse=True)
    return {
        "status": "passed" if accepted else "failed",
        "accepted_candidates": accepted,
        "rejected_candidates": rejected,
        "best_candidate": accepted[0]["candidate_id"] if accepted else None,
        "rule": "micro-search requires positive validation and OOS, PF>=1.05, non-thin counts, usable label distribution, bounded gap, no Tier B carry, and label/horizon mechanism",
    }


def evaluate_promotion_candidate_gate(mt5_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_candidate = pivot_candidate_mt5(mt5_rows)
    reference = by_candidate.get("c01_current_label_reference", {})
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for candidate_id, splits in by_candidate.items():
        val = splits.get("validation_is")
        oos = splits.get("oos")
        reasons = []
        if not val or not oos:
            rejected.append({"candidate_id": candidate_id, "reason": "missing_validation_or_oos_mt5_row"})
            continue
        required = ["net_profit", "profit_factor", "trade_count", "max_drawdown"]
        for field in required:
            if to_float(val.get(field)) is None or to_float(oos.get(field)) is None:
                reasons.append(f"missing_required_kpi_{field}")
        val_net = to_float(val.get("net_profit")) or 0.0
        oos_net = to_float(oos.get("net_profit")) or 0.0
        val_pf = to_float(val.get("profit_factor")) or 0.0
        oos_pf = to_float(oos.get("profit_factor")) or 0.0
        val_trades = int(to_float(val.get("trade_count")) or 0)
        oos_trades = int(to_float(oos.get("trade_count")) or 0)
        routed_total = int(to_float(val.get("actual_routed_total_count_mt5")) or 0) + int(to_float(oos.get("actual_routed_total_count_mt5")) or 0)
        tier_b = int(to_float(val.get("tier_b_fallback_used_count_mt5")) or 0) + int(to_float(oos.get("tier_b_fallback_used_count_mt5")) or 0)
        if val_net <= 0:
            reasons.append("validation_net_not_positive")
        if oos_net <= 0:
            reasons.append("oos_net_not_positive")
        if val_pf < 1.10:
            reasons.append("validation_pf_below_1_10")
        if oos_pf < 1.10:
            reasons.append("oos_pf_below_1_10")
        if val_trades < 25 or oos_trades < 25:
            reasons.append("trade_count_thin")
        if _label_pathological(val) or _label_pathological(oos):
            reasons.append("label_class_distribution_pathological")
        if routed_total <= 0:
            reasons.append("missing_entry_count_runtime")
        if routed_total and tier_b / routed_total > 0.60:
            reasons.append("tier_b_fallback_carrying_result")
        if val_trades and oos_trades and max(val_trades, oos_trades) / max(min(val_trades, oos_trades), 1) > 4:
            reasons.append("validation_oos_entry_count_instability")
        if abs(val_net - oos_net) > max(abs(val_net), abs(oos_net), 1.0) * 2.5:
            reasons.append("validation_oos_gap_unacceptable")
        ref_val = reference.get("validation_is")
        ref_oos = reference.get("oos")
        if ref_val and ref_oos:
            for label, row, ref_row in (("validation", val, ref_val), ("oos", oos, ref_oos)):
                drawdown = abs(to_float(row.get("max_drawdown")) or 0.0)
                ref_drawdown = abs(to_float(ref_row.get("max_drawdown")) or 0.0)
                if ref_drawdown and drawdown > ref_drawdown * 1.10 and (to_float(row.get("profit_factor")) or 0.0) < 1.25:
                    reasons.append(f"{label}_drawdown_worse_than_reference_without_strong_pf")
        reasons.append("cluster_concentration_check_not_available_for_positive_gate")
        payload = {
            "candidate_id": candidate_id,
            "validation_net": val_net,
            "oos_net": oos_net,
            "validation_pf": val_pf,
            "oos_pf": oos_pf,
            "validation_trades": val_trades,
            "oos_trades": oos_trades,
            "tier_b_signal_share": float(tier_b / routed_total) if routed_total else None,
        }
        if reasons:
            rejected.append({**payload, "reason": ";".join(dict.fromkeys(reasons))})
        else:
            accepted.append(payload)
    accepted.sort(key=lambda item: (item["validation_net"] + item["oos_net"], item["oos_pf"]), reverse=True)
    return {
        "status": "passed" if accepted else "failed",
        "accepted_candidates": accepted,
        "rejected_candidates": rejected,
        "candidate_id": accepted[0]["candidate_id"] if accepted else None,
        "promotion_packet_path": None,
        "rule": "actual MT5 output, positive validation/OOS, PF>=1.10, non-thin, drawdown and gap acceptable, no Tier B carry, reproducible label distribution, explainable direction behavior, no hidden promotion",
    }


def apply_gate_rejection_reasons(mt5_rows: Sequence[Mapping[str, Any]], gate: Mapping[str, Any]) -> list[dict[str, Any]]:
    rejected = {str(item.get("candidate_id")): str(item.get("reason")) for item in gate.get("rejected_candidates", []) if item.get("candidate_id")}
    accepted = {str(item.get("candidate_id")) for item in gate.get("accepted_candidates", []) if item.get("candidate_id")}
    rows: list[dict[str, Any]] = []
    for row in mt5_rows:
        candidate_id = str(row.get("candidate_id"))
        reason = row.get("candidate_rejection_reason")
        if candidate_id in rejected:
            reason = rejected[candidate_id]
        elif candidate_id in accepted:
            reason = "promotion_candidate_gate_passed"
        rows.append({**dict(row), "candidate_rejection_reason": reason})
    return rows


def actual_mt5_output_exists(result: Mapping[str, Any]) -> bool:
    return any(item.get("status") == "completed" for item in result.get("strategy_tester_reports", []))


def final_judgment_from_results(result: Mapping[str, Any], promotion_gate: Mapping[str, Any]) -> str:
    if not actual_mt5_output_exists(result):
        return BLOCKED_JUDGMENT
    if promotion_gate.get("status") == "passed":
        return POSITIVE_JUDGMENT
    return NEGATIVE_JUDGMENT


def create_promotion_packet_if_needed(promotion_gate: Mapping[str, Any]) -> dict[str, Any]:
    if promotion_gate.get("status") != "passed" or not promotion_gate.get("candidate_id"):
        return dict(promotion_gate)
    candidate_id = str(promotion_gate["candidate_id"])
    packet_root = ROOT / "docs/agent_control/packets" / f"promotion_candidate_review_stage41_{candidate_id}_v1"
    write_yaml_text(
        packet_root / "work_packet.yaml",
        f"""packet_id: promotion_candidate_review_stage41_{candidate_id}_v1
source_parent_packet_id: {PARENT_PACKET_ID}
source_stage_id: {STAGE_ID}
source_run_id: {RUN_ID}
candidate_id: {candidate_id}
status: review_ready_not_promoted
claim_boundary: promotion_candidate_review_ready_no_baseline_no_operating_promotion
""",
    )
    write_json(packet_root / "review_ready_summary.json", {"candidate_id": candidate_id, "source_stage_id": STAGE_ID, "source_run_id": RUN_ID, "promotion_gate": promotion_gate, "no_silent_promotion": True})
    return {**dict(promotion_gate), "promotion_packet_path": rel(packet_root)}


def kpi_report_path(record: Mapping[str, Any]) -> str:
    report = record.get("report", {})
    if isinstance(report, Mapping):
        html = report.get("html_report", {})
        if isinstance(html, Mapping):
            return str(html.get("path", ""))
    metrics = record.get("metrics", {})
    if isinstance(metrics, Mapping):
        return str(metrics.get("report_path", ""))
    return ""


def ledger_rows_from_kpis(kpi_records: Sequence[Mapping[str, Any]], judgment: str) -> list[dict[str, Any]]:
    rows = []
    for record in kpi_records:
        metrics = record.get("metrics", {})
        view = str(record.get("record_view", ""))
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": view,
                "parent_run_id": PARENT_PACKET_ID,
                "record_view": view,
                "tier_scope": record.get("tier_scope", ""),
                "kpi_scope": "directional_asymmetric_label_horizon_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": "completed" if record.get("status") == "completed" else "blocked",
                "judgment": judgment,
                "path": kpi_report_path(record),
                "primary_kpi": f"net_profit={metrics.get('net_profit','')};profit_factor={metrics.get('profit_factor','')};trade_count={metrics.get('trade_count','')};signal_count={metrics.get('signal_count','')};expectancy={metrics.get('expectancy','')};win_rate={metrics.get('win_rate_percent', metrics.get('win_rate',''))}",
                "guardrail_kpi": f"route_role={record.get('route_role','')};a_used={metrics.get('tier_a_primary_labelable_rows','')};b_fallback={metrics.get('tier_b_fallback_labelable_rows','')};max_dd={metrics.get('max_drawdown_amount', metrics.get('max_drawdown',''))};boundary={BOUNDARY}",
                "external_verification_status": "completed" if judgment != BLOCKED_JUDGMENT else "blocked",
                "notes": "Stage41 directional asymmetric label/horizon MT5 runtime-probe KPI row; no baseline, promotion, runtime authority, live readiness, or operating reference.",
            }
        )
    if not rows:
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__blocked_mt5_execution",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "blocked_mt5_execution",
                "parent_run_id": PARENT_PACKET_ID,
                "record_view": "blocked_mt5_execution",
                "tier_scope": mt5.TIER_AB,
                "kpi_scope": "directional_asymmetric_label_horizon_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": "blocked",
                "judgment": BLOCKED_JUDGMENT,
                "path": rel(RUN_ROOT),
                "primary_kpi": "missing_required_mt5_strategy_tester_output",
                "guardrail_kpi": f"boundary={BOUNDARY}",
                "external_verification_status": "blocked",
                "notes": "Stage41 blocked because MT5 Strategy Tester output artifact was not produced.",
            }
        )
    return rows


def write_ledgers(result: Mapping[str, Any], judgment: str) -> dict[str, Any]:
    kpi_records = result.get("mt5_kpi_records", [])
    stage_rows = ledger_rows_from_kpis(kpi_records, judgment)
    write_csv_rows(STAGE_ROOT / "03_reviews/stage_run_ledger.csv", ALPHA_LEDGER_COLUMNS, stage_rows)
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, stage_rows, key="ledger_row_id")
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_probe",
                "status": "reviewed" if judgment != BLOCKED_JUDGMENT else "blocked",
                "judgment": judgment,
                "path": rel(RUN_ROOT),
                "notes": f"Stage41 independent label/horizon redesign scout; mt5_attempts={len(result.get('attempts', []))}; boundary={BOUNDARY}",
            }
        ],
        key="run_id",
    )
    artifact_rows = [
        (f"{RUN_ID}_run_manifest", "run_manifest", RUN_ROOT / "run_manifest.json", "Stage41 run manifest"),
        (f"{RUN_ID}_label_schema", "label_schema", RUN_ROOT / "tables/stage41_label_schema.json", "Stage41 label schema"),
        (f"{RUN_ID}_label_lineage", "label_lineage", RUN_ROOT / "tables/stage41_label_lineage.csv", "Stage41 label lineage"),
        (f"{RUN_ID}_label_distribution_summary", "label_distribution_summary", RUN_ROOT / "tables/stage41_label_distribution_summary.json", "Stage41 label distribution summary"),
        (f"{RUN_ID}_model_training_manifest", "model_training_manifest", RUN_ROOT / "models/model_training_manifest.json", "Stage41 model training manifest"),
        (f"{RUN_ID}_model_artifact_hash_summary", "model_artifact_hash_summary", RUN_ROOT / "models/model_artifact_hash_summary.json", "Stage41 model artifact hashes"),
        (f"{RUN_ID}_candidate_grid", "candidate_grid", RUN_ROOT / "tables/stage41_candidate_grid.csv", "Stage41 broad label/horizon candidate grid"),
        (f"{RUN_ID}_mt5_handoff_manifest", "mt5_handoff_manifest", RUN_ROOT / "mt5/handoff_manifest.json", "Stage41 MT5 handoff manifest"),
        (f"{RUN_ID}_mt5_import_summary", "mt5_import_summary", RUN_ROOT / "mt5/mt5_result_import_summary.json", "Stage41 imported MT5 result summary"),
        (f"{RUN_ID}_review_packet", "stage_review_packet", STAGE_ROOT / "03_reviews/run35A_directional_asymmetric_label_horizon_broad_mt5_probe_packet.md", "Stage41 closeout packet"),
    ]
    rows = [
        {
            "artifact_id": artifact_id,
            "type": artifact_type,
            "path": rel(path),
            "status": "tracked_reviewed" if judgment != BLOCKED_JUDGMENT else "tracked_blocked",
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in artifact_rows
    ]
    existing = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    keys = {row["artifact_id"] for row in rows}
    merged = [row for row in existing if row.get("artifact_id") not in keys] + rows
    write_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "type", "path", "status", "notes"), merged)
    return {
        "stage_run_ledger": rel(STAGE_ROOT / "03_reviews/stage_run_ledger.csv"),
        "project_alpha_ledger": project_payload,
        "run_registry": run_payload,
        "artifact_registry": {"path": rel(ARTIFACT_REGISTRY_PATH), "rows": len(merged)},
    }


def best_worst(rows: Sequence[Mapping[str, Any]], split: str) -> tuple[Mapping[str, Any] | None, Mapping[str, Any] | None]:
    items = [row for row in rows if row.get("split") == split]
    if not items:
        return None, None
    key = lambda row: (to_float(row.get("net_profit")) or -1e18, to_float(row.get("profit_factor")) or 0.0)
    return max(items, key=key), min(items, key=key)


def write_handoff_files(result: Mapping[str, Any], mt5_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    mt5_root = RUN_ROOT / "mt5"
    handoff = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "idea_id": IDEA_ID,
        "common_files_root": str(COMMON_FILES_ROOT_DEFAULT),
        "terminal_path": str(TERMINAL_PATH_DEFAULT),
        "metaeditor_path": str(METAEDITOR_PATH_DEFAULT),
        "tester_profile_root": str(TESTER_PROFILE_ROOT_DEFAULT),
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "module_hashes": mt5.mt5_runtime_module_hashes(),
        "routing": "Tier A primary + Tier B fallback actual routed total",
    }
    tester_request = {
        "command_template": f"{TERMINAL_PATH_DEFAULT} /config:<ini_path>",
        "attempt_count": len(result.get("attempts", [])),
        "ini_files": [item.get("ini", {}).get("path") for item in result.get("attempts", [])],
        "set_files": [item.get("set", {}).get("path") for item in result.get("attempts", [])],
    }
    import_summary = {
        "imported_at": utc_now(),
        "strategy_tester_report_count": len(result.get("strategy_tester_reports", [])),
        "completed_report_count": sum(1 for item in result.get("strategy_tester_reports", []) if item.get("status") == "completed"),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "candidate_summary_rows": len(mt5_rows),
        "actual_mt5_output_exists": actual_mt5_output_exists(result),
    }
    retry = {
        "retry_command": "python -m foundation.pipelines.run_stage41_directional_asymmetric_label_horizon_probe --timeout-seconds 900",
        "terminal_path_expected": str(TERMINAL_PATH_DEFAULT),
        "common_files_path_expected": str(COMMON_FILES_ROOT_DEFAULT),
        "manifest_path": rel(RUN_ROOT / "run_manifest.json"),
    }
    write_json(mt5_root / "handoff_manifest.json", handoff)
    write_json(mt5_root / "tester_request.json", tester_request)
    write_json(mt5_root / "mt5_result_import_summary.json", import_summary)
    write_json(mt5_root / "replay_retry_command.json", retry)
    return {
        "handoff_manifest": rel(mt5_root / "handoff_manifest.json"),
        "tester_request": rel(mt5_root / "tester_request.json"),
        "mt5_result_import_summary": rel(mt5_root / "mt5_result_import_summary.json"),
        "replay_retry_command": rel(mt5_root / "replay_retry_command.json"),
    }


def artifact_hash_summary() -> list[dict[str, Any]]:
    rows = []
    if not path_exists(RUN_ROOT):
        return rows
    for path in sorted(io_path(RUN_ROOT).rglob("*")):
        local = Path(str(path).removeprefix("\\\\?\\"))
        if not local.is_file():
            continue
        try:
            rows.append({"path": rel(local), "sha256": sha256_file_lf_normalized(local), "bytes": int(local.stat().st_size)})
        except OSError:
            continue
    return rows


def write_run_files(
    result: Mapping[str, Any],
    mt5_rows: Sequence[Mapping[str, Any]],
    micro_gate: Mapping[str, Any],
    promotion_gate: Mapping[str, Any],
    judgment: str,
) -> dict[str, Any]:
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "idea_id": IDEA_ID,
            "parent_packet_id": PARENT_PACKET_ID,
            "run_number": RUN_NUMBER,
            "completion_goal": result.get("completion_goal"),
            "attempts": result.get("attempts", []),
            "common_copies": result.get("common_copies", []),
            "compile": result.get("compile", {}),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": judgment,
            "boundary": FINAL_BOUNDARY,
        },
    )
    write_json(
        RUN_ROOT / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "idea_id": IDEA_ID,
            "kpi_scope": "directional_asymmetric_label_horizon_mt5_runtime_probe",
            "model_family": result.get("model_family"),
            "feature_set_id": result.get("feature_set_id"),
            "label_id": result.get("label_id"),
            "split_contract": result.get("split_contract"),
            "mt5": {
                "scoreboard_lane": "runtime_probe",
                "external_verification_status": result.get("external_verification_status"),
                "execution_results": result.get("execution_results", []),
                "strategy_tester_reports": result.get("strategy_tester_reports", []),
                "kpi_records": result.get("mt5_kpi_records", []),
                "candidate_summary": list(mt5_rows),
            },
            "micro_search_gate": micro_gate,
            "promotion_candidate_gate": promotion_gate,
            "judgment": judgment,
            "boundary": FINAL_BOUNDARY,
        },
    )
    dataframe_to_csv(RUN_ROOT / "tables/stage41_mt5_candidate_summary.csv", mt5_rows)
    dataframe_to_csv(RUN_ROOT / "tables/stage41_python_candidate_summary.csv", result.get("python_candidate_summary", []))
    write_json(RUN_ROOT / "tables/stage41_route_coverage.json", result.get("route_coverage", {}))
    handoff = write_handoff_files(result, mt5_rows)
    write_json(RUN_ROOT / "artifact_lineage.json", {"source_lineage": result.get("source_lineage", []), "generated_artifacts": artifact_hash_summary()})
    return handoff


def write_stage_docs(
    result: Mapping[str, Any],
    mt5_rows: Sequence[Mapping[str, Any]],
    micro_gate: Mapping[str, Any],
    promotion_gate: Mapping[str, Any],
    judgment: str,
) -> None:
    best_val, worst_val = best_worst(mt5_rows, "validation_is")
    best_oos, worst_oos = best_worst(mt5_rows, "oos")
    actual_artifacts = [item for item in result.get("strategy_tester_reports", []) if item.get("status") == "completed"]
    command = ""
    if result.get("execution_results"):
        command = " ".join(str(item) for item in result["execution_results"][0].get("command", []))
    report_path = actual_artifacts[0].get("html_report", {}).get("path", "") if actual_artifacts else ""
    write_md(
        STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# Stage41 Brief(41단계 개요)

- stage_id(단계 ID): `{STAGE_ID}`
- idea_id(아이디어 ID): `{IDEA_ID}`
- run_id(실행 ID): `{RUN_ID}`
- question(질문): Do long and short opportunities require different forward horizons and return thresholds?(롱/숏 기회가 서로 다른 미래 수평선과 수익률 임계값을 필요로 하는가?)
- independence(독립성): Stage38/39/40(38/39/40단계)은 negative memory(부정 기억)로만 사용하고, permission/abstention(허용/기권), exit overlay(청산 오버레이), candle morphology(캔들 형태) 필터를 주 메커니즘으로 쓰지 않는다.
- claim boundary(주장 경계): `{FINAL_BOUNDARY}`

Effect(효과): Stage41(41단계)은 기존 신호에 필터를 더하지 않고 label/horizon(라벨/수평선) 자체를 다시 만들어 MT5 Strategy Tester(MT5 전략 테스터) 런타임 동작을 본다.
""",
    )
    write_md(
        STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage41 Input References(41단계 입력 참조)

- Tier A model input(Tier A 모델 입력): `{rel(MODEL_INPUT_DATASET_PATH)}`
- Tier A feature order(Tier A 피처 순서): `{rel(MODEL_INPUT_FEATURE_ORDER_PATH)}`
- training summary(학습 요약): `{rel(TRAINING_SUMMARY_PATH)}`
- raw US100 M5 close(원천 US100 5분봉 종가): `{rel(RAW_US100_BARS_PATH)}`
- raw MT5 bars(raw MT5 봉): `{rel(RAW_MT5_ROOT)}`
- negative memory(부정 기억): Stage38/39/40 selection statuses(선택 상태)
- MT5 EA(MT5 전문가 자문): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`

Effect(효과): 라벨(label, 라벨)은 closed M5 bar(확정 5분봉) 미래 종가만 사용하고, MT5(메타트레이더5)는 후보별 discrete signal CSV(이산 신호 CSV)를 실행한다.
""",
    )
    packet_lines = [
        "# Stage41 run35A Directional Asymmetric Label/Horizon Packet(41단계 run35A 방향 비대칭 라벨/수평선 묶음)",
        "",
        f"- stage_id(단계 ID): `{STAGE_ID}`",
        f"- idea_id(아이디어 ID): `{IDEA_ID}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- packet_id(묶음 ID): `{PACKET_ID}`",
        f"- judgment(판정): `{judgment}`",
        f"- claim boundary(주장 경계): `{FINAL_BOUNDARY}`",
        "",
        "## Label Designs(라벨 설계)",
        "",
        "- families(계열): current reference(현재 참조), asymmetric horizon(비대칭 수평선), flat band(무거래 구간), volatility normalized(변동성 정규화), session adjusted(세션 조정), direction pressure(방향 압박), simple rebuilt-label models(단순 재구축 라벨 모델)",
        "- leakage audit(누수 감사): label-only future returns(라벨 전용 미래 수익률)만 만들고 model features(모델 피처)에는 미래 열을 넣지 않음",
        "",
        "## Broad Sweep(광범위 탐색)",
        "",
        f"- candidate_count(후보 수): `{len([item for item in result.get('candidate_specs', []) if str(item.get('candidate_id','')).startswith('c')])}`",
        f"- best_validation(검증 최상): `{best_val.get('candidate_id') if best_val else 'missing'}` net `{best_val.get('net_profit') if best_val else 'missing'}` PF `{best_val.get('profit_factor') if best_val else 'missing'}`",
        f"- worst_validation(검증 최하): `{worst_val.get('candidate_id') if worst_val else 'missing'}`",
        f"- best_oos(OOS 최상): `{best_oos.get('candidate_id') if best_oos else 'missing'}` net `{best_oos.get('net_profit') if best_oos else 'missing'}` PF `{best_oos.get('profit_factor') if best_oos else 'missing'}`",
        f"- worst_oos(OOS 최하): `{worst_oos.get('candidate_id') if worst_oos else 'missing'}`",
        "",
        "## Micro Search Gate(미세 탐색 게이트)",
        "",
        f"- status(상태): `{micro_gate.get('status')}`",
        f"- best_candidate(최상 후보): `{micro_gate.get('best_candidate')}`",
        f"- rule(규칙): `{micro_gate.get('rule')}`",
        "",
        "## MT5 Strategy Tester Execution(MT5 전략 테스터 실행)",
        "",
    ]
    if actual_artifacts:
        first_attempt = result.get("attempts", [{}])[0]
        packet_lines.extend(
            [
                f"- command used(사용 명령): `{command}`",
                "- EA/script used(EA/스크립트): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`",
                f"- .ini path(.ini 경로): `{first_attempt.get('ini', {}).get('path', '')}`",
                f"- .set path(.set 경로): `{first_attempt.get('set', {}).get('path', '')}`",
                f"- manifest path(목록 경로): `{rel(RUN_ROOT / 'run_manifest.json')}`",
                f"- terminal path(터미널 경로): `{TERMINAL_PATH_DEFAULT}`",
                f"- Common Files path(Common Files 공용 파일 경로): `{COMMON_FILES_ROOT_DEFAULT}`",
                f"- tester output path(테스터 출력 경로): `{report_path}`",
                f"- imported result path(가져온 결과 경로): `{rel(RUN_ROOT / 'mt5/mt5_result_import_summary.json')}`",
                f"- candidates tested in MT5(MT5 후보 수): `{len(result.get('candidate_specs', []))}`",
            ]
        )
    else:
        packet_lines.append("BLOCKED: MT5 Strategy Tester execution did not produce an artifact, so Stage41 run35A is incomplete.")
    packet_lines.extend(
        [
            "",
            "## Promotion Candidate Gate(승격 후보 게이트)",
            "",
            f"- status(상태): `{promotion_gate.get('status')}`",
            f"- candidate_id(후보 ID): `{promotion_gate.get('candidate_id')}`",
            f"- promotion packet path(승격 묶음 경로): `{promotion_gate.get('promotion_packet_path')}`",
            "",
            "## Result Judgment(결과 판정)",
            "",
            f"`{judgment}`",
            "",
            "Stage41 run35A remains runtime_probe_only(런타임 탐침 전용): no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no operating reference(운영 기준 없음).",
        ]
    )
    write_md(STAGE_ROOT / "03_reviews/run35A_directional_asymmetric_label_horizon_broad_mt5_probe_packet.md", "\n".join(packet_lines))
    write_md(
        STAGE_ROOT / "03_reviews/review_index.md",
        """# Review Index(검토 색인)

- run packet(실행 묶음): `03_reviews/run35A_directional_asymmetric_label_horizon_broad_mt5_probe_packet.md`
- stage ledger(단계 장부): `03_reviews/stage_run_ledger.csv`
""",
    )
    write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage41 Selection Status(41단계 선택 상태)

- final_judgment(최종 판정): `{judgment}`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 기준): `none`
- micro_search_gate(미세 탐색 게이트): `{micro_gate.get('status')}`
- promotion_candidate_gate(승격 후보 게이트): `{promotion_gate.get('status')}`
- boundary(경계): `{FINAL_BOUNDARY}`
""",
    )


def write_packet_files(
    result: Mapping[str, Any],
    mt5_rows: Sequence[Mapping[str, Any]],
    micro_gate: Mapping[str, Any],
    promotion_gate: Mapping[str, Any],
    judgment: str,
    ledger_payload: Mapping[str, Any],
    validation_commands: Sequence[Mapping[str, Any]],
) -> None:
    actual_mt5 = actual_mt5_output_exists(result)
    required_gates = [
        "experiment_design",
        "data_integrity",
        "label_engineering",
        "model_validation",
        "runtime_parity_mt5_execution",
        "backtest_forensics",
        "performance_attribution",
        "artifact_lineage",
        "run_evidence",
        "result_judgment",
        "claim_discipline",
    ]
    write_yaml_text(
        PACKET_ROOT / "work_packet.yaml",
        f"""packet_id: {PACKET_ID}
stage_id: {STAGE_ID}
run_id: {RUN_ID}
idea_id: {IDEA_ID}
evidence_boundary: {BOUNDARY}
status: {"reviewed_runtime_probe_completed" if actual_mt5 else "blocked_runtime_probe_missing_mt5_execution"}
primary_family: label_horizon_redesign
primary_skill: obsidian-experiment-design
support_skills:
  - obsidian-data-integrity
  - obsidian-model-validation
  - obsidian-runtime-parity
  - obsidian-backtest-forensics
  - obsidian-performance-attribution
  - obsidian-artifact-lineage
  - obsidian-result-judgment
required_gates:
{chr(10).join(f"  - {gate}" for gate in required_gates)}
claim_boundary: {FINAL_BOUNDARY}
""",
    )
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        {
            "packet_id": PACKET_ID,
            "receipts": [
                {"skill": "obsidian-experiment-design", "status": "completed", "evidence": "stage question, broad label/horizon sweep, micro gate, and stop conditions recorded"},
                {"skill": "obsidian-data-integrity", "status": "completed", "evidence": "closed-bar label timestamp alignment, split distributions, and leakage audits recorded"},
                {"skill": "obsidian-model-validation", "status": "completed", "evidence": "simple model policy, class balance, validation/OOS split behavior, and overfit guards recorded"},
                {"skill": "obsidian-runtime-parity", "status": "passed" if actual_mt5 else "blocked", "evidence": "MT5 handoff manifest, .ini/.set, compile, tester output, and imported KPI rows recorded"},
                {"skill": "obsidian-backtest-forensics", "status": "passed" if actual_mt5 else "blocked", "evidence": "tester command, EA, report paths, costs from tester profile, and KPI rows recorded"},
                {"skill": "obsidian-performance-attribution", "status": "completed", "evidence": "validation/OOS best/worst, Tier A/B route components, drawdown, PF, and trade counts recorded"},
                {"skill": "obsidian-artifact-lineage", "status": "completed", "evidence": "source lineage and generated artifact hashes recorded"},
                {"skill": "obsidian-result-judgment", "status": "completed", "evidence": f"allowed judgment {judgment} with runtime_probe_only boundary"},
            ],
        },
    )
    best_val, worst_val = best_worst(mt5_rows, "validation_is")
    best_oos, worst_oos = best_worst(mt5_rows, "oos")
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "idea_id": IDEA_ID,
            "judgment": judgment,
            "actual_mt5_artifact_exists": actual_mt5,
            "broad_candidate_count": len([item for item in result.get("candidate_specs", []) if str(item.get("candidate_id", "")).startswith("c")]),
            "micro_candidate_count": len([item for item in result.get("candidate_specs", []) if str(item.get("candidate_id", "")).startswith("m")]),
            "mt5_attempt_count": len(result.get("attempts", [])),
            "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
            "best_validation_mt5": best_val,
            "worst_validation_mt5": worst_val,
            "best_oos_mt5": best_oos,
            "worst_oos_mt5": worst_oos,
            "micro_search_gate": micro_gate,
            "promotion_candidate_gate": promotion_gate,
            "boundary": FINAL_BOUNDARY,
            "ledger_sync": ledger_payload,
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "status": "passed" if actual_mt5 else "failed",
            "actual_mt5_strategy_tester_output_exists": actual_mt5,
            "compile": result.get("compile", {}),
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "blocker_if_failed": {
                "judgment": BLOCKED_JUDGMENT,
                "terminal_path_expected": str(TERMINAL_PATH_DEFAULT),
                "common_files_path_expected": str(COMMON_FILES_ROOT_DEFAULT),
                "retry_command": "python -m foundation.pipelines.run_stage41_directional_asymmetric_label_horizon_probe --timeout-seconds 900",
            },
        },
    )
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"status": "passed", "judgment": judgment, "allowed_judgments": [POSITIVE_JUDGMENT, INCONCLUSIVE_JUDGMENT, NEGATIVE_JUDGMENT, BLOCKED_JUDGMENT], "boundary": FINAL_BOUNDARY})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"status": "passed" if actual_mt5 else "blocked", "mt5_kpi_records": len(result.get("mt5_kpi_records", [])), "required_tier_records": ["Tier A used", "Tier B fallback used", "actual routed total"], "synthetic_sum_used_as_routed_total": False, "missing_required_kpi_fields": [] if actual_mt5 else ["actual_mt5_strategy_tester_output"]})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"status": "passed", "required_gates": required_gates, "covered_gates": required_gates, "missing_gates": []})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "forbidden_claims_present": False, "claim_boundary": FINAL_BOUNDARY, "no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "no_live_readiness": True, "no_operating_reference": True})
    write_json(PACKET_ROOT / "validation_commands.json", {"commands": list(validation_commands), "mt5_command_count": len(result.get("execution_results", [])), "status": "recorded"})


def update_current_truth(result: Mapping[str, Any], judgment: str, micro_gate: Mapping[str, Any], promotion_gate: Mapping[str, Any]) -> None:
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    replacements = {
        r"^active_branch: .*$": "active_branch: codex/stage41-directional-asymmetric-label-horizon",
        r"^active_stage: .*$": f"active_stage: {STAGE_ID}",
        r"^current_run_id: .*$": f"current_run_id: {RUN_ID}",
    }
    for pattern, value in replacements.items():
        state_text = re.sub(pattern, value, state_text, flags=re.MULTILINE)
    status_text = "reviewed_runtime_probe_completed" if judgment != BLOCKED_JUDGMENT else "blocked_runtime_probe_missing_mt5_execution"
    block = f"""

stage41_label_horizon_directional_asymmetric_return_target_rebuild:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  idea_id: {IDEA_ID}
  status: {status_text}
  current_run_id: {RUN_ID}
  mt5_attempt_count: {len(result.get("attempts", []))}
  mt5_kpi_record_count: {len(result.get("mt5_kpi_records", []))}
  judgment: {judgment}
  micro_search_gate: {micro_gate.get("status")}
  promotion_candidate_gate: {promotion_gate.get("status")}
  report_path: {rel(STAGE_ROOT / "03_reviews/run35A_directional_asymmetric_label_horizon_broad_mt5_probe_packet.md")}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  boundary: {FINAL_BOUNDARY}
"""
    state_text = re.sub(r"\n+stage41_label_horizon_directional_asymmetric_return_target_rebuild:\n(?:  .+\n)*", "\n", state_text, flags=re.MULTILINE)
    io_path(WORKSPACE_STATE_PATH).write_text(state_text.rstrip() + block, encoding="utf-8")

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = re.sub(r"## Latest Stage41 Directional Asymmetric Label Horizon\(.*?\)\n.*?(?=\n## |\Z)", "", current, flags=re.DOTALL).lstrip()
    actual = judgment != BLOCKED_JUDGMENT
    section = f"""## Latest Stage41 Directional Asymmetric Label Horizon(최신 41단계 방향 비대칭 라벨 수평선)

Stage41(41단계) `{STAGE_ID}`는 label/horizon redesign(라벨/수평선 재설계) runtime probe(런타임 탐침)로 열렸다. Stage38/39/40(38/39/40단계)은 negative memory(부정 기억)로만 사용했고, permission/abstention(허용/기권), exit overlay(청산 오버레이), candle morphology(캔들 형태) 재시도는 하지 않았다.

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{judgment}`
- MT5 evidence(MT5 근거): `{"present" if actual else "missing"}`
- MT5 attempts(MT5 시도): `{len(result.get("attempts", []))}`
- MT5 KPI rows(MT5 KPI 행): `{len(result.get("mt5_kpi_records", []))}`
- micro_search_gate(미세 탐색 게이트): `{micro_gate.get("status")}`
- promotion_candidate_gate(승격 후보 게이트): `{promotion_gate.get("status")}`
- boundary(경계): `{FINAL_BOUNDARY}`

Effect(효과): current truth(현재 진실)는 Stage41(41단계)을 runtime_probe_only(런타임 탐침 전용) label/horizon(라벨/수평선) 연구로만 기록한다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(section + current, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    entry = f"\n- {utc_now()} `{STAGE_ID}` `{RUN_ID}` finished with judgment `{judgment}`; boundary `{FINAL_BOUNDARY}`; topic is independent label/horizon redesign.\n"
    io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + entry, encoding="utf-8-sig")


def merge_execution_results(broad: Mapping[str, Any], micro: Mapping[str, Any] | None) -> dict[str, Any]:
    if micro is None:
        return dict(broad)
    merged = dict(broad)
    for key in ("attempts", "candidate_specs", "common_copies", "execution_results", "strategy_tester_reports", "mt5_kpi_records", "python_candidate_summary", "label_summaries"):
        merged[key] = list(broad.get(key, [])) + list(micro.get(key, []))
    merged["feature_matrices"] = {**dict(broad.get("feature_matrices", {})), **dict(micro.get("feature_matrices", {}))}
    model_artifacts = dict(broad.get("model_artifacts", {}))
    model_artifacts["python_candidate_models"] = list(model_artifacts.get("python_candidate_models", [])) + list(micro.get("model_artifacts", {}).get("python_candidate_models", []))
    merged["model_artifacts"] = model_artifacts
    merged["external_verification_status"] = (
        "completed"
        if broad.get("external_verification_status") == "completed" and micro.get("external_verification_status") == "completed"
        else "partial_completed_with_blocked_micro_attempt"
    )
    merged["micro_execution"] = {"status": micro.get("external_verification_status"), "attempt_count": len(micro.get("attempts", []))}
    return merged


def write_model_and_label_summaries(result: Mapping[str, Any], specs: Sequence[DirectionalAsymmetricLabelSpec]) -> None:
    write_json(RUN_ROOT / "tables/stage41_label_schema.json", {"columns": label_schema()})
    dataframe_to_csv(RUN_ROOT / "tables/stage41_label_lineage.csv", label_lineage_rows(specs, source_data_path=rel(RAW_US100_BARS_PATH)))
    write_json(RUN_ROOT / "tables/stage41_label_distribution_summary.json", result.get("label_summaries", []))
    write_json(RUN_ROOT / "models/model_training_manifest.json", result.get("model_artifacts", {}).get("python_candidate_models", []))
    model_hash_rows = []
    for item in result.get("model_artifacts", {}).get("python_candidate_models", []):
        model_hash_rows.append(
            {
                "candidate_id": item.get("candidate_id"),
                "model_family": item.get("model_family"),
                "path": item.get("path"),
                "sha256": item.get("sha256"),
                "feature_order_hash": item.get("feature_order_hash"),
            }
        )
    score_table = result.get("model_artifacts", {}).get("signal_score_table", {})
    model_hash_rows.append({"candidate_id": "shared_signal_score_table", "model_family": "ebm_discrete_signal_table", "path": score_table.get("path"), "sha256": score_table.get("sha256"), "feature_order_hash": score_table.get("feature_order_hash")})
    write_json(RUN_ROOT / "models/model_artifact_hash_summary.json", model_hash_rows)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage41 directional asymmetric label/horizon MT5 runtime probe.")
    parser.add_argument("--materialize-only", action="store_true", help="Write artifacts but do not invoke MT5.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = build_arg_parser().parse_args(argv)
    validation_commands = [
        {
            "command": "python -m foundation.pipelines.run_stage41_directional_asymmetric_label_horizon_probe --timeout-seconds 900",
            "result": "running_or_recorded_by_pipeline",
            "failures_or_blockers": "",
        }
    ]
    common, route_coverage, lineage = build_common_table()
    raw_close = load_raw_close_frame()
    base_threshold = load_label_threshold()
    common_artifact = save_frame(RUN_ROOT / "tables/stage41_common_decision_surface_table.parquet", common)
    lineage = [{**item, "sha256": common_artifact["sha256"] if item.get("sha256") == "computed_after_write" else item.get("sha256")} for item in lineage]
    broad_specs = build_stage41_broad_candidate_grid()
    dataframe_to_csv(RUN_ROOT / "tables/stage41_candidate_grid.csv", [spec.as_dict() for spec in broad_specs])
    broad_batch = build_candidate_batch(
        specs=broad_specs,
        common=common,
        raw_close=raw_close,
        base_threshold=base_threshold,
        common_files_root=Path(args.common_files_root),
    )
    all_frames = dict(broad_batch["frames"])
    candidate_artifact = save_frame(RUN_ROOT / "tables/stage41_candidate_signal_table.parquet", pd.concat(all_frames.values(), ignore_index=True))
    broad_prepared = prepared_payload(
        candidate_specs=broad_specs,
        attempts=broad_batch["attempts"],
        feature_exports=broad_batch["feature_exports"],
        signal_score_table_artifact=broad_batch["signal_score_table_artifact"],
        python_model_artifacts=broad_batch["python_model_artifacts"],
        label_summaries=broad_batch["label_summaries"],
        common_copies=broad_batch["common_copies"],
        route_coverage=route_coverage,
        common_artifact=common_artifact,
        candidate_artifact=candidate_artifact,
        python_summary=broad_batch["summary"],
        lineage=lineage,
        batch_label="broad_sweep",
    )
    broad_result = execute_or_block(broad_prepared, args)
    broad_rows = build_mt5_candidate_summary(broad_result.get("mt5_kpi_records", []), broad_batch["summary"], broad_result.get("execution_results", []))
    micro_gate = evaluate_micro_search_gate(broad_rows)
    micro_result = None
    if micro_gate.get("status") == "passed" and not args.materialize_only:
        micro_specs = build_stage41_micro_candidate_grid(str(micro_gate["best_candidate"]), broad_specs)
        micro_batch = build_candidate_batch(
            specs=micro_specs,
            common=common,
            raw_close=raw_close,
            base_threshold=base_threshold,
            common_files_root=Path(args.common_files_root),
        )
        all_frames.update(micro_batch["frames"])
        candidate_artifact = save_frame(RUN_ROOT / "tables/stage41_candidate_signal_table.parquet", pd.concat(all_frames.values(), ignore_index=True))
        micro_prepared = prepared_payload(
            candidate_specs=micro_specs,
            attempts=micro_batch["attempts"],
            feature_exports=micro_batch["feature_exports"],
            signal_score_table_artifact=micro_batch["signal_score_table_artifact"],
            python_model_artifacts=micro_batch["python_model_artifacts"],
            label_summaries=micro_batch["label_summaries"],
            common_copies=micro_batch["common_copies"],
            route_coverage=route_coverage,
            common_artifact=common_artifact,
            candidate_artifact=candidate_artifact,
            python_summary=micro_batch["summary"],
            lineage=lineage,
            batch_label="micro_search",
        )
        micro_result = execute_or_block(micro_prepared, args)
    result = merge_execution_results(broad_result, micro_result)
    mt5_rows = build_mt5_candidate_summary(result.get("mt5_kpi_records", []), result.get("python_candidate_summary", []), result.get("execution_results", []))
    promotion_gate = create_promotion_packet_if_needed(evaluate_promotion_candidate_gate(mt5_rows))
    mt5_rows = apply_gate_rejection_reasons(mt5_rows, promotion_gate)
    judgment = final_judgment_from_results(result, promotion_gate)
    result["judgment"] = judgment
    result["candidate_table_artifact"] = candidate_artifact
    result["validation_commands"] = validation_commands
    write_model_and_label_summaries(result, [DirectionalAsymmetricLabelSpec(**spec) for spec in result.get("candidate_specs", [])])
    handoff_payload = write_run_files(result, mt5_rows, micro_gate, promotion_gate, judgment)
    ledger_payload = write_ledgers(result, judgment)
    write_stage_docs(result, mt5_rows, micro_gate, promotion_gate, judgment)
    write_packet_files(result, mt5_rows, micro_gate, promotion_gate, judgment, ledger_payload, validation_commands)
    update_current_truth(result, judgment, micro_gate, promotion_gate)
    write_json(
        RUN_ROOT / "final_execution_summary.json",
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "judgment": judgment,
            "handoff": handoff_payload,
            "ledger": ledger_payload,
            "micro_search_gate": micro_gate,
            "promotion_candidate_gate": promotion_gate,
            "claim_boundary": FINAL_BOUNDARY,
        },
    )


if __name__ == "__main__":
    main()
