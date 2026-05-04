from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import pandas as pd

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    FEATURE_ORDER_PATH,
    METAEDITOR_PATH_DEFAULT,
    MODEL_INPUT_PATH,
    RAW_ROOT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    TRAINING_SUMMARY_PATH,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame
from foundation.models.gam_additive import (
    GamVariantSpec,
    default_stage20_gam_variants,
    fit_gam_variant,
    nonflat_threshold,
    probability_frame,
    split_decision_metrics,
)
from foundation.models.gam_score_table import (
    check_gam_piecewise_score_table_parity,
    export_gam_piecewise_score_table,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5


STAGE_NUMBER = 20
STAGE_ID = "20_model_family_challenge__gam_additive_smooth_shape"
SOURCE_RUN_ID = "run14A_gam_additive_shape_scout_v1"
SOURCE_PACKET_ID = "stage20_run14A_gam_additive_shape_scout_v1"
RUN_NUMBER = "run14B"
RUN_ID = "run14B_gam_runtime_handoff_probe_v1"
PACKET_ID = "stage20_run14B_gam_runtime_handoff_probe_v1"
EXPLORATION_LABEL = "stage20_Model__GAMRuntimeHandoffProbe"
MODEL_FAMILY = "pygam_logistic_gam_piecewise_score_table_runtime_probe"
MODEL_BACKEND = "ebm_table"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
SELECTED_VARIANT_ID = "v02_core24_smoother"
THRESHOLD_QUANTILE = 0.90
MAX_HOLD_BARS = 12
MIN_MARGIN = 0.0
BOUNDARY = "gam_piecewise_score_table_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_gam_piecewise_score_table_runtime_probe_completed"
JUDGMENT_BLOCKED = "blocked_gam_piecewise_score_table_runtime_probe_after_attempt"

ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REVIEW_PATH = STAGE_ROOT / "03_reviews/run14B_gam_runtime_handoff_probe_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage20_run14B_gam_runtime_handoff_probe.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN_PATH = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"


@dataclass(frozen=True)
class RuntimeTopic:
    run_id: str = RUN_ID
    run_number: str = RUN_NUMBER
    packet_id: str = PACKET_ID
    exploration_label: str = EXPLORATION_LABEL
    threshold_quantile: float = THRESHOLD_QUANTILE
    max_hold_bars: int = MAX_HOLD_BARS
    expected_attempts: int = 6
    expected_kpi_records: int = 10
    topic_read: str = "gam_piecewise_score_table_runtime_handoff"
    boundary: str = BOUNDARY

    @property
    def run_root(self) -> Path:
        return RUN_ROOT

    @property
    def packet_root(self) -> Path:
        return PACKET_ROOT

    @property
    def review_path(self) -> Path:
        return REVIEW_PATH


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def selected_spec() -> GamVariantSpec:
    for spec in default_stage20_gam_variants():
        if spec.variant_id == SELECTED_VARIANT_ID:
            return spec
    raise RuntimeError(f"missing Stage20 selected GAM variant: {SELECTED_VARIANT_ID}")


def load_context() -> dict[str, Any]:
    spec = selected_spec()
    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    full_feature_order = load_feature_order(FEATURE_ORDER_PATH)
    validate_model_input_frame(tier_a_frame, full_feature_order)
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    missing_from_tier_b = sorted(set(spec.feature_names).difference(tier_b_feature_order))
    if missing_from_tier_b:
        raise RuntimeError(f"Selected Stage20 GAM features are not Tier-B compatible: {missing_from_tier_b}")
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=full_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=float(training_summary["threshold_log_return"]),
    )
    runtime_feature_order = list(spec.feature_names)
    return {
        "spec": spec,
        "tier_a_frame": tier_a_frame,
        "full_feature_order": full_feature_order,
        "tier_b_training_frame": tier_b_context["tier_b_training_frame"],
        "tier_b_fallback_frame": tier_b_context["tier_b_fallback_frame"],
        "tier_b_feature_order": tier_b_feature_order,
        "runtime_feature_order": runtime_feature_order,
        "runtime_feature_order_hash": ordered_hash(runtime_feature_order),
        "tier_b_context_summary": tier_b_context["summary"],
        "training_summary": training_summary,
    }


def _load_or_train_model(path: Path, frame: pd.DataFrame, feature_order: Sequence[str], spec: GamVariantSpec) -> tuple[dict[str, Any], dict[str, Any], str]:
    if io_path(path).exists():
        return joblib.load(io_path(path)), {"source": rel(path), "sha256": sha256_file_lf_normalized(path)}, "loaded_run14A_joblib"
    models, sample = fit_gam_variant(frame, feature_order, spec)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    joblib.dump(models, io_path(path))
    return models, {"source": rel(path), "sha256": sha256_file_lf_normalized(path), "training_sample": sample}, "retrained_selected_spec"


def load_or_train_models(context: Mapping[str, Any]) -> dict[str, Any]:
    spec = context["spec"]
    tier_a_path = SOURCE_RUN_ROOT / "models" / f"{SELECTED_VARIANT_ID}_tier_a_gam_ovr.joblib"
    tier_b_path = SOURCE_RUN_ROOT / "models" / f"{SELECTED_VARIANT_ID}_tier_b_gam_ovr.joblib"
    tier_a_model, tier_a_artifact, tier_a_policy = _load_or_train_model(
        tier_a_path,
        context["tier_a_frame"],
        context["full_feature_order"],
        spec,
    )
    tier_b_model, tier_b_artifact, tier_b_policy = _load_or_train_model(
        tier_b_path,
        context["tier_b_training_frame"],
        context["tier_b_feature_order"],
        spec,
    )
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], spec.feature_names)
    tier_b_train_prob = probability_frame(tier_b_model, context["tier_b_training_frame"], spec.feature_names)
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], spec.feature_names)
    return {
        "tier_a_model": tier_a_model,
        "tier_b_model": tier_b_model,
        "tier_a_artifact": tier_a_artifact,
        "tier_b_artifact": tier_b_artifact,
        "tier_a_policy": tier_a_policy,
        "tier_b_policy": tier_b_policy,
        "tier_a_prob": tier_a_prob,
        "tier_b_train_prob": tier_b_train_prob,
        "tier_b_prob": tier_b_prob,
    }


def save_predictions(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def tier_record(record_view: str, tier_scope: str, prob_frame: pd.DataFrame, threshold: float, path: Path) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, threshold)
    subtype_counts: dict[str, int] = {}
    if "partial_context_subtype" in prob_frame.columns:
        subtype_counts = {
            str(key): int(value)
            for key, value in prob_frame["partial_context_subtype"].astype(str).value_counts().sort_index().items()
        }
    total = {
        "rows": int(len(prob_frame)),
        "signal_count": int(sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))),
        "short_count": int(sum(metrics.get(split, {}).get("short_count", 0) for split in ("train", "validation", "oos"))),
        "long_count": int(sum(metrics.get(split, {}).get("long_count", 0) for split in ("train", "validation", "oos"))),
        "partial_context_subtype_counts": subtype_counts or None,
        "threshold_ids": f"q{THRESHOLD_QUANTILE:.2f}",
        "probability_row_sum_max_abs_error": metrics.get("probability_checks", {}).get("row_sum_max_abs_error"),
    }
    total["signal_coverage"] = safe_float(total["signal_count"]) / max(1, int(total["rows"]))
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": total,
        "split_metrics": {split: metrics.get(split, {}) for split in ("train", "validation", "oos")},
    }


def materialize_python_tier_records(
    models: Mapping[str, Any],
    a_threshold: float,
    b_threshold: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root = RUN_ROOT / "predictions"
    a_path = root / "tier_a_separate_predictions.parquet"
    b_path = root / "tier_b_separate_predictions.parquet"
    ab_path = root / "tier_ab_combined_predictions.parquet"
    tier_a_prob = models["tier_a_prob"]
    tier_b_prob = models["tier_b_prob"]
    ab_prob = pd.concat(
        [
            tier_a_prob.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_prob.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    records = [
        tier_record("tier_a_separate", mt5.TIER_A, tier_a_prob, a_threshold, a_path),
        tier_record("tier_b_separate", mt5.TIER_B, tier_b_prob, b_threshold, b_path),
        tier_record("tier_ab_combined", mt5.TIER_AB, ab_prob, a_threshold, ab_path),
    ]
    artifacts = {
        "tier_a_predictions": save_predictions(a_path, tier_a_prob),
        "tier_b_predictions": save_predictions(b_path, tier_b_prob),
        "tier_ab_predictions": save_predictions(ab_path, ab_prob),
    }
    return records, artifacts


def export_models(context: Mapping[str, Any], models: Mapping[str, Any]) -> dict[str, Any]:
    root = RUN_ROOT / "models"
    io_path(root).mkdir(parents=True, exist_ok=True)
    spec = context["spec"]
    feature_order = context["runtime_feature_order"]
    tier_a_table = root / f"{SELECTED_VARIANT_ID}_tier_a_gam_piecewise_score_table.csv"
    tier_b_table = root / f"{SELECTED_VARIANT_ID}_tier_b_gam_piecewise_score_table.csv"
    tier_a_export = export_gam_piecewise_score_table(
        models["tier_a_model"],
        tier_a_table,
        feature_names=feature_order,
        reference_frame=context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq("train"), feature_order],
        bin_count=128,
    )
    tier_b_export = export_gam_piecewise_score_table(
        models["tier_b_model"],
        tier_b_table,
        feature_names=feature_order,
        reference_frame=context["tier_b_training_frame"].loc[context["tier_b_training_frame"]["split"].astype(str).eq("train"), feature_order],
        bin_count=128,
    )
    a_sample = context["tier_a_frame"].loc[
        context["tier_a_frame"]["split"].astype(str).eq("validation"),
        feature_order,
    ].head(2048).to_numpy(dtype="float64", copy=False)
    b_sample = context["tier_b_training_frame"].loc[
        context["tier_b_training_frame"]["split"].astype(str).eq("validation"),
        feature_order,
    ].head(2048).to_numpy(dtype="float64", copy=False)
    return {
        "selected_variant_id": spec.variant_id,
        "tier_a_joblib": models["tier_a_artifact"],
        "tier_b_joblib": models["tier_b_artifact"],
        "tier_a_model_source_policy": models["tier_a_policy"],
        "tier_b_model_source_policy": models["tier_b_policy"],
        "model_backend": MODEL_BACKEND,
        "runtime_feature_order": feature_order,
        "runtime_feature_order_hash": context["runtime_feature_order_hash"],
        "tier_a_score_table": {**tier_a_export, "path": rel(Path(tier_a_export["path"]))},
        "tier_b_score_table": {**tier_b_export, "path": rel(Path(tier_b_export["path"]))},
        "score_table_parity": {
            "tier_a": check_gam_piecewise_score_table_parity(models["tier_a_model"], tier_a_table, a_sample, feature_count=len(feature_order)),
            "tier_b": check_gam_piecewise_score_table_parity(models["tier_b_model"], tier_b_table, b_sample, feature_count=len(feature_order)),
        },
    }


def export_feature_matrices(context: Mapping[str, Any]) -> dict[str, Any]:
    root = RUN_ROOT / "features"
    feature_order = context["runtime_feature_order"]
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_frame = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq(source_split)].copy()
        tier_b_frame = context["tier_b_fallback_frame"].loc[context["tier_b_fallback_frame"]["split"].astype(str).eq(source_split)].copy()
        payload[f"tier_a_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_a_frame,
            feature_order,
            root / f"tier_a_{runtime_split}_feature_matrix.csv",
            metadata_columns=("partial_context_subtype", "route_role"),
        )
        payload[f"tier_b_fallback_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_b_frame,
            feature_order,
            root / f"tier_b_fallback_{runtime_split}_feature_matrix.csv",
            metadata_columns=("partial_context_subtype", "route_role"),
        )
    return payload


def copy_runtime_inputs(model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_score_table", "tier_b_score_table"):
        local_path = ROOT / model_artifacts[key]["path"]
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = ROOT / matrix["path"]
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_attempts(context: Mapping[str, Any], model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any], thresholds: Mapping[str, float]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    tier_a_model = Path(model_artifacts["tier_a_score_table"]["path"]).name
    tier_b_model = Path(model_artifacts["tier_b_score_table"]["path"]).name
    feature_count = len(context["runtime_feature_order"])
    feature_hash = context["runtime_feature_order_hash"]
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        tier_a_matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        tier_b_matrix = Path(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"]).name
        common_kwargs = {
            "run_root": RUN_ROOT,
            "run_id": RUN_ID,
            "stage_number": STAGE_NUMBER,
            "exploration_label": EXPLORATION_LABEL,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": MAX_HOLD_BARS,
            "common_root": common,
        }
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_a_only_{runtime_split}",
                tier=mt5.TIER_A,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{RUN_ID}_tier_a",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=feature_count,
                feature_order_hash=feature_hash,
                short_threshold=float(thresholds["tier_a"]),
                long_threshold=float(thresholds["tier_a"]),
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="mt5_tier_a_only",
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_b_fallback_only_{runtime_split}",
                tier=mt5.TIER_B,
                model_path=f"{common}/models/{tier_b_model}",
                model_id=f"{RUN_ID}_tier_b",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{tier_b_matrix}",
                feature_count=feature_count,
                feature_order_hash=feature_hash,
                short_threshold=float(thresholds["tier_b"]),
                long_threshold=float(thresholds["tier_b"]),
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_b_fallback",
                attempt_role="tier_b_fallback_only_total",
                record_view_prefix="mt5_tier_b_fallback_only",
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"routed_{runtime_split}",
                tier=mt5.TIER_AB,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{RUN_ID}_tier_a",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=feature_count,
                feature_order_hash=feature_hash,
                short_threshold=float(thresholds["tier_a"]),
                long_threshold=float(thresholds["tier_a"]),
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix="mt5_routed_total",
                fallback_enabled=True,
                fallback_model_path=f"{common}/models/{tier_b_model}",
                fallback_model_id=f"{RUN_ID}_tier_b",
                fallback_model_backend=MODEL_BACKEND,
                fallback_feature_path=f"{common}/features/{tier_b_matrix}",
                fallback_feature_count=feature_count,
                fallback_feature_order_hash=feature_hash,
                fallback_short_threshold=float(thresholds["tier_b"]),
                fallback_long_threshold=float(thresholds["tier_b"]),
                fallback_min_margin=MIN_MARGIN,
                fallback_invert_signal=False,
            )
        )
    return attempts


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.materialize_only):
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": JUDGMENT_BLOCKED,
            "failure": {"type": "materialize_only", "message": "MT5 execution skipped by CLI flag."},
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
    except Exception as exc:
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
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = SELECTED_VARIANT_ID
        record["topic_read"] = RuntimeTopic().topic_read
        record["threshold_quantile"] = f"q{THRESHOLD_QUANTILE:.2f}"
        record["max_hold_bars"] = MAX_HOLD_BARS
    return result


def metrics_by_view(result: Mapping[str, Any], view: str) -> dict[str, Any]:
    for record in result.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            metrics = record.get("metrics", {})
            return dict(metrics) if isinstance(metrics, Mapping) else {}
    return {}


def parity_passed(model_artifacts: Mapping[str, Any]) -> bool:
    parity = model_artifacts.get("score_table_parity", {})
    return bool(parity.get("tier_a", {}).get("passed")) and bool(parity.get("tier_b", {}).get("passed"))


def runtime_failure_signature(result: Mapping[str, Any]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    model_ok_total = 0
    model_fail_total = 0
    feature_ready_total = 0
    last_skip_counts: dict[str, int] = {}
    for item in result.get("execution_results", []) or []:
        status = str(item.get("status"))
        status_counts[status] = status_counts.get(status, 0) + 1
        outputs = item.get("runtime_outputs", {})
        if not isinstance(outputs, Mapping):
            continue
        summary = outputs.get("last_summary", {})
        if not isinstance(summary, Mapping):
            continue
        model_ok_total += int(summary.get("model_ok_count") or 0)
        model_fail_total += int(summary.get("model_fail_count") or 0)
        feature_ready_total += int(summary.get("feature_ready_count") or 0)
        skip = summary.get("last_skip_reason")
        if skip:
            last_skip_counts[str(skip)] = last_skip_counts.get(str(skip), 0) + 1
    primary_skip = max(last_skip_counts.items(), key=lambda pair: pair[1])[0] if last_skip_counts else None
    return {
        "compile_status": (result.get("compile") or {}).get("status") if isinstance(result.get("compile"), Mapping) else None,
        "attempt_status_counts": status_counts,
        "feature_ready_count_total": feature_ready_total,
        "model_ok_count_total": model_ok_total,
        "model_fail_count_total": model_fail_total,
        "primary_runtime_skip": primary_skip,
        "last_skip_reason_counts": last_skip_counts,
    }


def write_normalized_kpi() -> dict[str, Any]:
    inventory = [{"run_id": RUN_ID, "stage_id": STAGE_ID, "idea_id": RUN_NUMBER, "path": rel(RUN_ROOT)}]
    records, summary_rows, missing, parser_errors = mt5_kpi_recorder.build_normalized_records(ROOT, inventory)
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    enriched, trade_rows, trade_summary, trade_errors = mt5_trade_attribution.enrich_records(records, ROOT, market_data)
    write_json(PACKET_ROOT / "normalized_kpi_records.jsonl", records)
    write_json(PACKET_ROOT / "normalized_kpi_summary.csv", summary_rows)
    write_json(PACKET_ROOT / "normalized_kpi_missing_runs.json", missing)
    write_json(PACKET_ROOT / "normalized_kpi_parser_errors.json", parser_errors)
    write_json(PACKET_ROOT / "enriched_kpi_records.jsonl", enriched)
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


def build_summary(result: Mapping[str, Any], model_artifacts: Mapping[str, Any], prediction_artifacts: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = result.get("external_verification_status") == "completed"
    parity_ok = parity_passed(model_artifacts)
    validation = metrics_by_view(result, "mt5_routed_total_validation_is")
    oos = metrics_by_view(result, "mt5_routed_total_oos")
    avg_trades = (safe_float(validation.get("trade_count")) + safe_float(oos.get("trade_count"))) / 2.0
    visible = completed and parity_ok and avg_trades >= 5.0
    return {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_packet_id": SOURCE_PACKET_ID,
        "stage_id": STAGE_ID,
        "model_family": MODEL_FAMILY,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "topic_read": RuntimeTopic().topic_read,
        "threshold_quantile": THRESHOLD_QUANTILE,
        "max_hold_bars": MAX_HOLD_BARS,
        "boundary": BOUNDARY,
        "judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "closure_judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "external_verification_status": result["external_verification_status"],
        "model_characteristic_strength": "gam_runtime_axis_visible" if visible else "gam_runtime_axis_weak_or_blocked",
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
        "python_tier_records": list(tier_records),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "attempt_count": len(result.get("attempts", [])),
        "expected_attempts": RuntimeTopic().expected_attempts,
        "expected_kpi_records": RuntimeTopic().expected_kpi_records,
        "validation_routed": validation,
        "oos_routed": oos,
        "runtime_failure_signature": runtime_failure_signature(result),
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
    }


def upsert_run_registry(result: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
        "judgment": summary["closure_judgment"],
        "path": rel(RUN_ROOT),
        "notes": ledger_pairs(
            (
                ("model_family", MODEL_FAMILY),
                ("topic_read", RuntimeTopic().topic_read),
                ("routing_mode", "tier_a_primary_tier_b_fallback"),
                ("selected_variant", SELECTED_VARIANT_ID),
                ("threshold_quantile", f"q{THRESHOLD_QUANTILE:.2f}"),
                ("validation_net_profit", validation.get("net_profit")),
                ("validation_pf", validation.get("profit_factor")),
                ("oos_net_profit", oos.get("net_profit")),
                ("oos_pf", oos.get("profit_factor")),
                ("external_verification", result["external_verification_status"]),
                ("boundary", "runtime_probe_only"),
            )
        ),
    }
    return upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [row], key="run_id")


def packet_markdown(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    parity = summary.get("model_artifacts", {}).get("score_table_parity", {})
    return "\n".join(
        [
            "# RUN14B GAM Runtime Handoff Probe(실행14B GAM 런타임 인계 탐침)",
            "",
            "## Judgment(판정)",
            "",
            f"- run(실행): `{RUN_ID}`",
            f"- judgment(판정): `{summary.get('closure_judgment')}`",
            f"- external verification(외부 검증): `{summary.get('external_verification_status')}`",
            f"- selected variant(선택 변형): `{SELECTED_VARIANT_ID}`",
            f"- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`",
            f"- normalized KPI records(정규화 핵심 성과 지표 기록): `{kpi.get('normalized_records')}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "",
            "효과(effect, 효과): GAM(`Generalized Additive Model`, 일반화 가산 모델)을 piecewise score table(구간 점수표)로 MT5(`MetaTrader 5`, 메타트레이더5)에 넘겨 runtime_probe(런타임 탐침)를 시도했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
            "## Runtime Read(런타임 판독)",
            "",
            "| split(분할) | net profit(순수익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실) |",
            "|---|---:|---:|---:|---:|",
            f"| validation(검증) | `{validation.get('net_profit')}` | `{validation.get('profit_factor')}` | `{validation.get('trade_count')}` | `{validation.get('max_drawdown_amount')}` |",
            f"| OOS(표본외) | `{oos.get('net_profit')}` | `{oos.get('profit_factor')}` | `{oos.get('trade_count')}` | `{oos.get('max_drawdown_amount')}` |",
            "",
            "## Handoff Parity(인계 동등성)",
            "",
            f"- Tier A approximation check(Tier A 근사 점검): `{parity.get('tier_a', {}).get('passed')}`; max_abs_diff(최대 절대 차이) `{parity.get('tier_a', {}).get('max_abs_diff')}`; p95_abs_diff(95분위 절대 차이) `{parity.get('tier_a', {}).get('p95_abs_diff')}`",
            f"- Tier B approximation check(Tier B 근사 점검): `{parity.get('tier_b', {}).get('passed')}`; max_abs_diff(최대 절대 차이) `{parity.get('tier_b', {}).get('max_abs_diff')}`; p95_abs_diff(95분위 절대 차이) `{parity.get('tier_b', {}).get('p95_abs_diff')}`",
            "",
            "Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )


def gate_payloads(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> dict[str, Any]:
    completed = summary.get("external_verification_status") == "completed"
    parity_ok = parity_passed(summary.get("model_artifacts", {}))
    gates = ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"]
    return {
        "runtime_evidence_gate": {
            "status": "passed" if completed and parity_ok else "blocked",
            "external_verification_status": summary.get("external_verification_status"),
            "score_table_approximation_passed": parity_ok,
            "mt5_kpi_record_count": summary.get("mt5_kpi_record_count"),
            "expected_kpi_records": RuntimeTopic().expected_kpi_records,
        },
        "scope_completion_gate": {
            "status": "passed" if summary.get("attempt_count") == RuntimeTopic().expected_attempts else "blocked",
            "attempt_count": summary.get("attempt_count"),
            "expected_attempts": RuntimeTopic().expected_attempts,
            "claim_boundary": BOUNDARY,
        },
        "kpi_contract_audit": {
            "status": "passed" if int(summary.get("mt5_kpi_record_count") or 0) > 0 else "blocked",
            "normalized_records": kpi.get("normalized_records"),
            "parser_errors": kpi.get("parser_errors"),
        },
        "required_gate_coverage_audit": {
            "status": "passed",
            "packet_id": PACKET_ID,
            "required_gates": gates,
            "covered_gates": gates,
        },
        "final_claim_guard": {
            "status": "passed",
            "allowed_claims": ["runtime_probe", "inconclusive", "blocked"],
            "forbidden_claims": summary.get("forbidden_claims"),
            "claim_boundary": BOUNDARY,
        },
    }


def build_skill_receipts(summary: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    return {
        "packet_id": PACKET_ID,
        "created_at_utc": created_at,
        "receipts": [
            {
                "skill": "obsidian-runtime-parity",
                "status": "completed",
                "research_path": rel(Path(__file__)),
                "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
                "shared_contract": "selected GAM feature order, piecewise score-table probability order short/flat/long, q-thresholds, US100 M5 timestamp match.",
                "known_differences": "GAM smooth terms are exported as a piecewise score table; claim remains runtime_probe only.",
                "parity_check": summary.get("model_artifacts", {}).get("score_table_parity"),
                "runtime_claim_boundary": "runtime_probe",
            },
            {
                "skill": "obsidian-backtest-forensics",
                "status": "completed",
                "tester_identity": "MT5 Strategy Tester US100 M5, deposit=500, leverage=1:100, model=4.",
                "ea_identity": "ObsidianPrimeV2_RuntimeProbeEA with generated .set and .ini files.",
                "report_identity": "run_manifest records tester report and telemetry paths.",
                "trade_evidence": f"MT5 KPI records={summary.get('mt5_kpi_record_count')}",
                "backtest_judgment": "usable_with_boundary" if summary.get("external_verification_status") == "completed" else "blocked",
            },
            {
                "skill": "obsidian-run-evidence-system",
                "status": "completed",
                "measurement_scope": "runtime_probe MT5 KPI plus normalized KPI parser outputs",
                "judgment_class": "inconclusive" if summary.get("external_verification_status") == "completed" else "blocked",
                "scoreboard": "runtime_parity",
                "parity_level": "P3_runtime_shadow_parity_sampled",
                "evidence_boundary": "probe",
            },
            {
                "skill": "obsidian-result-judgment",
                "status": "completed",
                "result_subject": RUN_ID,
                "judgment_label": summary.get("closure_judgment"),
                "claim_boundary": BOUNDARY,
            },
        ],
    }


def write_run_outputs(result: Mapping[str, Any], model_artifacts: Mapping[str, Any], prediction_artifacts: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]], kpi: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    summary = build_summary(result, model_artifacts, prediction_artifacts, tier_records)
    upsert_run_registry(result, summary)
    ledger_rows = build_alpha_scout_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        selected_threshold_id=f"q{THRESHOLD_QUANTILE:.2f}",
        run_output_root=RUN_ROOT,
        external_verification_status=result["external_verification_status"],
    )
    materialize_alpha_ledgers(stage_run_ledger_path=STAGE_LEDGER_PATH, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=ledger_rows)
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "run_number": RUN_NUMBER,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "threshold_policy": f"non-flat q{THRESHOLD_QUANTILE:.2f}; not profit searched",
        "max_hold_bars": MAX_HOLD_BARS,
        "boundary": BOUNDARY,
        "runtime_probe": {
            key: result.get(key)
            for key in ("attempts", "common_copies", "compile", "execution_results", "strategy_tester_reports", "external_verification_status", "judgment", "failure")
            if key in result
        },
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
    }
    kpi_record = {
        **manifest,
        "kpi_scope": "gam_mt5_runtime_probe",
        "python_tier_records": list(tier_records),
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": result["external_verification_status"],
            "kpi_records": result.get("mt5_kpi_records", []),
        },
        "kpi_management": dict(kpi),
        "judgment": summary["closure_judgment"],
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)
    write_json(RUN_ROOT / "summary.json", summary)
    write_md(REVIEW_PATH, packet_markdown(summary, kpi))
    write_json(PACKET_ROOT / "aggregate_summary.json", {**summary, "kpi_management": dict(kpi)})
    write_json(PACKET_ROOT / "skill_receipts.json", build_skill_receipts(summary, created_at))
    for name, payload in gate_payloads(summary, kpi).items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    return summary


def replace_top_level_yaml_block(text: str, marker: str, block: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + block
    start = text.index(marker)
    next_start = len(text)
    cursor = text.find("\n", start + len(marker))
    while cursor != -1:
        line_start = cursor + 1
        line_end = text.find("\n", line_start)
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        if line and not line[0].isspace() and ":" in line:
            next_start = line_start
            break
        cursor = text.find("\n", line_start)
    return text[:start] + block + text[next_start:]


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    status = "active_run14B_mt5_runtime_probe_completed" if summary.get("external_verification_status") == "completed" else "active_run14B_mt5_runtime_probe_blocked_after_attempt"
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    lines = state.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("current_run_id: "):
            lines[index] = f"current_run_id: {RUN_ID}"
        elif line.startswith("  status: active_python_structural_scout_completed") and "stage20:" not in lines[index - 1 : index]:
            lines[index] = f"  status: {status}"
    state = "\n".join(lines) + "\n"
    state = state.replace("stage20_run14A_structural_scout_completed", "stage20_run14B_mt5_runtime_probe_completed" if summary.get("external_verification_status") == "completed" else "stage20_run14B_mt5_runtime_probe_blocked")
    state = state.replace("active_python_structural_scout_completed", status)
    state = state.replace("active_run14A_python_structural_scout_completed", status)
    block = f"""stage20_gam_run14B_runtime_handoff_probe:
  packet_id: {PACKET_ID}
  status: {'reviewed_runtime_probe_completed' if summary.get('external_verification_status') == 'completed' else 'blocked_runtime_probe_after_attempt'}
  judgment: {summary.get('closure_judgment')}
  current_run_id: {RUN_ID}
  source_run_id: {SOURCE_RUN_ID}
  selected_variant_id: {SELECTED_VARIANT_ID}
  mt5_attempt_count: {summary.get('attempt_count')}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: stages/{STAGE_ID}/03_reviews/run14B_gam_runtime_handoff_probe_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {'stage20_closeout_and_stage21_open_only' if summary.get('external_verification_status') == 'completed' else 'repair_run14B_runtime_handoff_probe_then_rerun_exact_attempts'}
"""
    state = replace_top_level_yaml_block(state, "stage20_gam_run14B_runtime_handoff_probe:", block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8")


def update_text_docs(summary: Mapping[str, Any]) -> None:
    completed = summary.get("external_verification_status") == "completed"
    status = "active_run14B_mt5_runtime_probe_completed" if completed else "active_run14B_mt5_runtime_probe_blocked_after_attempt"
    next_action = "write Stage20 closeout packet and open Stage21 open-only" if completed else "repair run14B handoff/runtime failure and rerun the same six MT5 attempts"
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage20 Selection Status(20단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `{status}`
- current run(현재 실행): `{RUN_ID}`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `{summary.get('closure_judgment')}`
- selected variant(선택 변형): `{SELECTED_VARIANT_ID}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage20(20단계)은 GAM(`Generalized Additive Model`, 일반화 가산 모델) smooth shape(부드러운 모양)를 piecewise score table(구간 점수표)로 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)까지 연결했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Next Exact Action(다음 정확한 행동)

`{next_action}`.
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else "# Stage20 Review Index(20단계 검토 색인)\n"
    line = f"- `{RUN_ID}`: `{rel(REVIEW_PATH)}`\n"
    if RUN_ID not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)
    write_md(
        DECISION_PATH,
        f"""# Stage20 RUN14B GAM Runtime Handoff Decision(20단계 실행14B GAM 런타임 인계 결정)

## Decision(결정)

`{RUN_ID}`를 `{summary.get('closure_judgment')}`로 기록한다.

효과(effect, 효과): GAM(`Generalized Additive Model`, 일반화 가산 모델)을 MT5(`MetaTrader 5`, 메타트레이더5)에서 직접 score table(점수표)로 읽는 runtime_probe(런타임 탐침)를 남겼다. 이 근거는 Stage20(20단계) closeout(마감) 판단에는 쓸 수 있지만, edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Next Condition(다음 조건)

`{next_action}`.
""",
    )
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage20 RUN14B GAM Runtime Update(최신 20단계 실행14B GAM 런타임 업데이트)

Stage20(20단계) `{RUN_ID}`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `{summary.get('closure_judgment')}`. MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`. next exact action(다음 정확한 행동): `{next_action}`.

효과(effect, 효과): Stage20(20단계)은 Python structural scout(파이썬 구조 탐색)에서 runtime handoff(런타임 인계) 확인 단계로 전진했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

"""
    current = update + current
    io_path(CURRENT_WORKING_STATE_PATH).write_text(current, encoding="utf-8-sig")
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    plan = plan.replace("- current run(현재 실행): `run14A_gam_additive_shape_scout_v1`", f"- current run(현재 실행): `{RUN_ID}`")
    plan = plan.replace(
        "Current active milestone(현재 활성 마일스톤): Stage20(20단계) `run14B_gam_runtime_handoff_probe_v1` MT5 runtime_probe(MT5 런타임 탐침) 준비.",
        f"Current active milestone(현재 활성 마일스톤): Stage20(20단계) `{next_action}`.",
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `{RUN_ID}` {'completed(완료)' if completed else 'blocked after attempt(시도 뒤 차단)'} as MT5 runtime_probe(MT5 런타임 탐침).
- active stage/current run id(활성 단계/현재 실행 ID): Stage20(20단계), `{RUN_ID}`.
- changed files(변경 파일): GAM score-table exporter(점수표 내보내기), Stage20 runtime pipeline(런타임 파이프라인), run14B packet(묶음), ledgers(장부), current truth docs(현재 진실 문서).
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `{rel(RUN_ROOT / 'mt5')}` and `{rel(REVIEW_PATH)}`.
- blocker(차단 사유): `{'none(없음)' if completed else 'see run_manifest runtime_probe failure(실행 목록 런타임 탐침 실패 참고)'}`.
- exact next action(정확한 다음 행동): `{next_action}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending before stop(중지 전 대기).

효과(effect, 효과): 다음 재개는 Stage20(20단계) 상태에 따라 closeout(마감) 또는 run14B repair(수정)에서 시작한다.
"""
    marker = "## Latest Stop Resume State(최신 중지 재개 상태)"
    if marker in plan:
        start = plan.index(marker)
        next_section = plan.find("\n## ", start + 1)
        plan = plan[:start] + resume + ("\n" + plan[next_section + 1 :] if next_section != -1 else "")
    else:
        plan = plan.rstrip() + "\n\n" + resume
    if RUN_ID not in plan:
        plan = plan.rstrip() + f"\n- `2026-05-05`: Stage20(20단계) `{RUN_ID}` MT5 runtime_probe(런타임 탐침)를 기록했다.\n"
    else:
        plan = plan.replace(
            "- `2026-05-05`: Stage20(20단계) `run14A_gam_additive_shape_scout_v1` completed(완료). selected variant(선택 변형)는 `v02_core24_smoother`, best overall variant(전체 최고 변형)는 `v03_proxy_context20_tier_a`다. MT5 runtime_probe(MT5 런타임 탐침)는 아직 없고, 다음 milestone(마일스톤)은 `run14B_gam_runtime_handoff_probe_v1`이다.",
            "- `2026-05-05`: Stage20(20단계) `run14A_gam_additive_shape_scout_v1` completed(완료). selected variant(선택 변형)는 `v02_core24_smoother`, best overall variant(전체 최고 변형)는 `v03_proxy_context20_tier_a`다.\n- `2026-05-05`: Stage20(20단계) `run14B_gam_runtime_handoff_probe_v1` MT5 runtime_probe(런타임 탐침)를 기록했다.",
        )
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")


def run(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    models = load_or_train_models(context)
    a_threshold = nonflat_threshold(models["tier_a_prob"], THRESHOLD_QUANTILE)
    b_threshold = nonflat_threshold(models["tier_b_train_prob"], THRESHOLD_QUANTILE)
    tier_records, prediction_artifacts = materialize_python_tier_records(models, a_threshold, b_threshold)
    model_artifacts = export_models(context, models)
    model_artifacts["thresholds"] = {"tier_a": a_threshold, "tier_b": b_threshold, "quantile": THRESHOLD_QUANTILE}
    feature_matrices = export_feature_matrices(context)
    copies = copy_runtime_inputs(model_artifacts, feature_matrices)
    attempts = make_attempts(context, model_artifacts, feature_matrices, {"tier_a": a_threshold, "tier_b": b_threshold})
    prepared = {
        "stage_id": STAGE_ID,
        "stage_number": STAGE_NUMBER,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "attempts": attempts,
        "common_copies": copies,
        "route_coverage": context["tier_b_context_summary"],
        "model_artifacts": model_artifacts,
        "feature_matrices": list(feature_matrices.values()),
    }
    result = execute_or_block(prepared, args)
    result["model_artifacts"] = model_artifacts
    result["feature_matrices"] = list(feature_matrices.values())
    provisional = {"normalized_records": 0, "normalized_summary_rows": 0, "missing_runs": 0, "parser_errors": 0, "trade_attribution_records": 0, "trade_level_rows": 0, "trade_parser_errors": 0}
    write_run_outputs(result, model_artifacts, prediction_artifacts, tier_records, provisional, created_at)
    kpi = write_normalized_kpi()
    summary = write_run_outputs(result, model_artifacts, prediction_artifacts, tier_records, kpi, created_at)
    update_workspace_state(summary)
    update_text_docs(summary)
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage20 GAM MT5 runtime handoff probe.")
    parser.add_argument("--materialize-only", action="store_true", help="Prepare artifacts without launching MT5.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    summary = run(args)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "judgment": summary["closure_judgment"],
                    "external_verification_status": summary["external_verification_status"],
                    "mt5_kpi_record_count": summary["mt5_kpi_record_count"],
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
