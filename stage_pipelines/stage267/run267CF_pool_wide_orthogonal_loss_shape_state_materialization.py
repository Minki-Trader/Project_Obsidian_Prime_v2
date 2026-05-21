from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    copy_to_common,
)
from foundation.models.ebm_score_table import load_ebm_score_table, score_ebm_table_probabilities
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import (
    run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267CF"
RUN_ID = "run267CF_stage267_pool_wide_orthogonal_loss_shape_state_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
STATUS = "run267CF_pool_wide_orthogonal_loss_shape_state_materialized_execution_pending"
JUDGMENT = "orthogonal_loss_shape_state_materialized_no_candidate_selection"
NEXT_ACTION = "run267CG_execute_pool_wide_orthogonal_loss_shape_state_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_orthogonal_loss_shape_state_materialization"
VARIANT_ROOT = RUN_ROOT / "variants"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_REVIEW_RESULT_PATH = source_design.REVIEW_RESULT_PATH
SOURCE_MATERIALIZATION_QUEUE_PATH = source_design.MATERIALIZATION_QUEUE_PATH
SOURCE_FEATURE_BLUEPRINT_PATH = source_design.FEATURE_BLUEPRINT_PATH
SOURCE_CANDIDATE_PIVOT_PATH = source_design.CANDIDATE_PIVOT_MATRIX_PATH
SOURCE_PRUNE_OR_HOLD_PATH = source_design.PRUNE_OR_HOLD_RULES_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_REPORT_PATH = source_design.REPORT_PATH

SOURCE_RUN267W_ROOT = STAGE_ROOT / "02_runs" / "run267W" / "true_internal_ablation_score_table_materialization"
SOURCE_VARIANT_MANIFEST_PATH = SOURCE_RUN267W_ROOT / "true_internal_ablation_variant_manifest.csv"
SOURCE_ATTEMPT_MANIFEST_PATH = SOURCE_RUN267W_ROOT / "attempts.csv"
SOURCE_RUNTIME_CONTRACT_PATH = SOURCE_RUN267W_ROOT / "runtime_contract.csv"

MATERIALIZATION_PLAN_PATH = RUN_ROOT / "materialization_plan.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "orthogonal_variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
FEATURE_ENGINEERING_DIAGNOSTICS_PATH = RUN_ROOT / "feature_engineering_diagnostics.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
ARTIFACT_LINEAGE_RECEIPT_PATH = RUN_ROOT / "artifact_lineage_receipt.csv"
CONTROL_REANCHOR_AUDIT_PATH = RUN_ROOT / "control_reanchor_audit.csv"
FEATURE_ORDER_DATA_AUDIT_PATH = RUN_ROOT / "feature_order_data_audit.csv"
HELD_QUEUE_PATH = RUN_ROOT / "held_queue.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CF_pool_wide_orthogonal_loss_shape_state_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CF_pool_wide_orthogonal_loss_shape_state_materialization.py")

STAGE_LEDGER_PATH = source_design.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_design.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_design.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_design.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_design.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_design.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_design.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_design.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_design.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_design.ARTIFACT_COLUMNS

PERIOD_LABEL = "historical_2024_tier_a_train_era_stress"
COMMON_ROOT = "OPV2/s267cf/run267CF_orthogonal_loss_shape_state"
EXPLORATION_LABEL = "stage267_BaselineRacing__OrthogonalLossShapeState"
MATERIALIZATION_BOUNDARY = (
    "Tier_A_and_Tier_A_plus_B_duplicate_2024_execution_inputs_materialized; "
    "true_Tier_B_fallback_and_runtime_results_remain_future_work"
)
SOURCE_LIMITATION = (
    "uses_run267W_bar_state_surface; true_trade_path_MAE_MFE_and_closed_trade_loss_cluster_not_available_yet"
)

CANDIDATE_ORDER = ("s264_aih", "s264_lc", "s262_lih", "s264_aia", "s258_stc")
CONTROL_ALIASES = {"s264_lc", "s262_lih", "s264_aia"}

PROFILE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "loss_shape_proxy_minimal": {
        "source_queue_id": "run267cf_q01_loss_shape_state_minimal_bundle",
        "profile_token": "loss_shape_proxy",
        "profile_label": "loss_shape_proxy_minimal",
        "source_test_preferences": (
            "rep_volatility_atr",
            "rep_trend_strength_adx",
            "abl_volatility_bandwidth",
            "abl_price_return_range",
        ),
        "engineered_features": [
            "stage267cf_adverse_excursion_proxy_score",
            "stage267cf_profit_giveback_proxy_score",
            "stage267cf_loss_cluster_bar_state_proxy_score",
        ],
        "model_terms": "soft_flat_bias_when_loss_shape_proxy_is_high",
        "materialization_note": (
            "trade-path MAE/MFE unavailable, so this is a bar-state proxy materialization "
            "with explicit data-integrity boundary"
        ),
    },
    "similar_replacement_impulse": {
        "source_queue_id": "run267cf_q02_similar_feature_replacement_bundle",
        "profile_token": "similar_repl",
        "profile_label": "similar_replacement_impulse",
        "source_test_preferences": (
            "rep_trend_strength_adx",
            "rep_volatility_atr",
            "abl_trend_strength_direction",
        ),
        "engineered_features": [
            "stage267cf_trend_strength_replacement_score",
            "stage267cf_volatility_energy_transition_score",
            "stage267cf_range_pressure_asymmetry_score",
        ],
        "model_terms": "nonflat_impulse_pressure_for_similar_feature_replacement",
        "materialization_note": (
            "keeps the branch aggressive enough to test similar market meaning instead of only adding filters"
        ),
    },
}

FEATURE_COMPONENTS: dict[str, tuple[tuple[str, str], ...]] = {
    "stage267cf_adverse_excursion_proxy_score": (
        ("return_zscore_20", "abs"),
        ("return_1_over_atr_14", "abs"),
        ("atr_14_over_atr_50", "raw"),
        ("gap_percent", "abs"),
    ),
    "stage267cf_profit_giveback_proxy_score": (
        ("bb_position_20", "abs_center_0_5"),
        ("close_open_ratio", "abs_center_1"),
        ("close_prev_close_ratio", "abs_center_1"),
        ("historical_vol_5_over_20", "raw"),
    ),
    "stage267cf_trend_strength_replacement_score": (
        ("di_spread_14", "abs"),
        ("vortex_indicator", "abs_center_1"),
        ("supertrend_10_3", "raw"),
        ("ema20_ema50_diff", "abs"),
    ),
    "stage267cf_volatility_energy_transition_score": (
        ("atr_14_over_atr_50", "raw"),
        ("historical_vol_5_over_20", "raw"),
        ("bollinger_width_20", "raw"),
        ("historical_vol_20", "raw"),
    ),
    "stage267cf_range_pressure_asymmetry_score": (
        ("hl_range", "raw"),
        ("close_open_ratio", "abs_center_1"),
        ("gap_percent", "abs"),
        ("bb_position_20", "abs_center_0_5"),
    ),
}

PLAN_COLUMNS = (
    "plan_id",
    "source_queue_id",
    "priority",
    "candidate_id",
    "candidate_alias",
    "candidate_role",
    "profile_label",
    "profile_token",
    "source_test_id",
    "source_queue_id_run267W",
    "source_feature_file",
    "source_model_file",
    "source_feature_order_hash",
    "source_feature_count",
    "engineered_features",
    "materialization_decision",
    "source_limitation",
    "claim_boundary",
)

VARIANT_COLUMNS = (
    "variant_id",
    "plan_id",
    "source_queue_id",
    "priority",
    "candidate_id",
    "candidate_alias",
    "candidate_role",
    "profile_label",
    "profile_token",
    "source_test_id",
    "source_feature_file",
    "source_feature_sha256",
    "runtime_feature_file",
    "runtime_feature_sha256",
    "source_model_file",
    "source_model_sha256",
    "runtime_model_file",
    "runtime_model_sha256",
    "common_feature_path",
    "common_feature_sha256",
    "common_model_path",
    "common_model_sha256",
    "source_feature_count",
    "engineered_feature_count",
    "feature_count",
    "feature_order",
    "feature_order_hash",
    "engineered_features",
    "runtime_rows",
    "missing_feature_cells",
    "score_table_validation",
    "probability_rows_checked",
    "probability_sum_max_abs_error",
    "source_limitation",
    "claim_boundary",
)

ATTEMPT_COLUMNS = (
    "attempt_name",
    "variant_id",
    "candidate_id",
    "candidate_alias",
    "candidate_role",
    "profile_label",
    "source_test_id",
    "tier",
    "attempt_role",
    "record_view_prefix",
    "set_path",
    "set_sha256",
    "ini_path",
    "ini_sha256",
    "common_telemetry_path",
    "common_summary_path",
    "execution_status",
)

RUNTIME_CONTRACT_COLUMNS = (
    "variant_id",
    "candidate_id",
    "candidate_alias",
    "candidate_role",
    "profile_label",
    "source_test_id",
    "shared_contract",
    "feature_count",
    "feature_order_hash",
    "model_backend",
    "model_materialization_type",
    "short_threshold",
    "long_threshold",
    "min_margin",
    "max_hold_bars",
    "engineered_features",
    "known_difference",
    "runtime_claim_boundary",
)

DIAGNOSTIC_COLUMNS = (
    "variant_id",
    "candidate_alias",
    "profile_label",
    "engineered_feature",
    "source_component",
    "transform",
    "q25",
    "q50",
    "q75",
    "threshold_source",
)

RECEIPT_COLUMNS = (
    "receipt_id",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
)

DATA_INTEGRITY_COLUMNS = (
    "check_id",
    "data_source",
    "time_axis",
    "sample_scope",
    "missing_or_duplicate_check",
    "feature_label_boundary",
    "split_boundary",
    "leakage_risk",
    "data_hash_or_identity",
    "integrity_judgment",
)

AUDIT_COLUMNS = (
    "audit_id",
    "status",
    "evidence",
    "effect",
)

HELD_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "hold_reason",
    "next_condition",
    "claim_boundary",
)

RESULT_JUDGMENT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else REPO_ROOT / path


def safe_token(value: Any, limit: int = 72) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_").lower()
    return token[:limit] or "item"


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}" if math.isfinite(value) else ""
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return str(value)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered or ("status", "notes"))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in fieldnames})


def write_runtime_csv(path: Path, frame: pd.DataFrame, columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.loc[:, list(columns)].to_csv(io_path(path), index=False, encoding="utf-8", lineterminator="\n")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def parse_key_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        if not line or line.lstrip().startswith(";") or "=" not in line or line.startswith("["):
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def write_set(path: Path, values: Mapping[str, Any]) -> dict[str, str]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["; generated_by=run267CF_pool_wide_orthogonal_loss_shape_state_materialization"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "format": "mt5_set"}


def write_ini(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["[Tester]"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "format": "mt5_tester_ini"}


def source_feature_order(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    if not header or header[0] != "bar_time_server":
        raise RuntimeError(f"unexpected feature header: {rel(path)}")
    return list(header[1:])


def transform_series(frame: pd.DataFrame, column: str, transform: str) -> pd.Series:
    if column not in frame.columns:
        raise KeyError(f"missing component column: {column}")
    series = pd.to_numeric(frame[column], errors="coerce").astype("float64")
    if transform == "raw":
        return series
    if transform == "abs":
        return series.abs()
    if transform == "abs_center_1":
        return (series - 1.0).abs()
    if transform == "abs_center_0_5":
        return (series - 0.5).abs()
    raise ValueError(f"unknown transform: {transform}")


def scale_series(series: pd.Series) -> tuple[pd.Series, dict[str, float]]:
    clean = series.replace([np.inf, -np.inf], np.nan)
    finite = clean.dropna()
    if finite.empty:
        return pd.Series(0.0, index=series.index), {"q25": 0.0, "q50": 0.0, "q75": 0.0}
    q25 = float(finite.quantile(0.25))
    q50 = float(finite.quantile(0.50))
    q75 = float(finite.quantile(0.75))
    if q75 <= q25:
        scaled = pd.Series(0.0, index=series.index)
    else:
        scaled = ((clean - q25) / (q75 - q25)).clip(0.0, 1.0).fillna(0.0)
    return scaled.astype("float64"), {"q25": q25, "q50": q50, "q75": q75}


def loss_cluster_proxy(frame: pd.DataFrame) -> tuple[pd.Series, list[dict[str, Any]]]:
    if "log_return_1" not in frame.columns:
        raise KeyError("missing component column: log_return_1")
    returns = pd.to_numeric(frame["log_return_1"], errors="coerce").astype("float64").fillna(0.0)
    negative_pressure = (returns < 0.0).astype("float64").rolling(24, min_periods=1).mean()
    magnitude_scaled, magnitude_quantiles = scale_series(returns.abs())
    cluster = (0.65 * negative_pressure + 0.35 * magnitude_scaled).clip(0.0, 1.0)
    diagnostics = [
        {
            "source_component": "log_return_1_negative_rolling_24",
            "transform": "past_bar_loss_cluster_proxy",
            "q25": float(negative_pressure.quantile(0.25)),
            "q50": float(negative_pressure.quantile(0.50)),
            "q75": float(negative_pressure.quantile(0.75)),
            "threshold_source": "current_and_prior_closed_bar_state_no_future_trade_result",
        },
        {
            "source_component": "abs_log_return_1",
            "transform": "abs_scaled",
            "q25": magnitude_quantiles["q25"],
            "q50": magnitude_quantiles["q50"],
            "q75": magnitude_quantiles["q75"],
            "threshold_source": "candidate_specific_quantiles",
        },
    ]
    return cluster.astype("float64"), diagnostics


def build_engineered_frame(
    source_feature_path: Path,
    destination_feature_path: Path,
    *,
    feature_order: Sequence[str],
    profile_label: str,
    engineered_features: Sequence[str],
    variant_id: str,
    candidate_alias: str,
) -> tuple[list[dict[str, Any]], int]:
    frame = pd.read_csv(io_path(source_feature_path), encoding="utf-8-sig")
    output = frame.copy()
    diagnostics: list[dict[str, Any]] = []
    for feature_name in engineered_features:
        if feature_name == "stage267cf_loss_cluster_bar_state_proxy_score":
            output[feature_name], rows = loss_cluster_proxy(frame)
            for row in rows:
                diagnostics.append(
                    {
                        "variant_id": variant_id,
                        "candidate_alias": candidate_alias,
                        "profile_label": profile_label,
                        "engineered_feature": feature_name,
                        **row,
                    }
                )
            continue
        components = FEATURE_COMPONENTS[feature_name]
        scaled_components: list[pd.Series] = []
        for column, transform in components:
            raw = transform_series(frame, column, transform)
            scaled, quantiles = scale_series(raw)
            scaled_components.append(scaled)
            diagnostics.append(
                {
                    "variant_id": variant_id,
                    "candidate_alias": candidate_alias,
                    "profile_label": profile_label,
                    "engineered_feature": feature_name,
                    "source_component": column,
                    "transform": transform,
                    "q25": quantiles["q25"],
                    "q50": quantiles["q50"],
                    "q75": quantiles["q75"],
                    "threshold_source": "candidate_specific_quantiles",
                }
            )
        output[feature_name] = pd.concat(scaled_components, axis=1).mean(axis=1).clip(0.0, 1.0)
    output_columns = ["bar_time_server", *feature_order, *engineered_features]
    missing_cells = int(output.loc[:, output_columns].isna().sum().sum())
    output.loc[:, engineered_features] = output.loc[:, engineered_features].fillna(0.0)
    write_runtime_csv(destination_feature_path, output, output_columns)
    return diagnostics, missing_cells


def score_terms_for_feature(profile_label: str, feature_name: str) -> tuple[list[float], list[tuple[float, float, float]]]:
    cuts = [0.25, 0.50, 0.75]
    if profile_label == "loss_shape_proxy_minimal":
        scores = [
            (0.0, 0.0, 0.0),
            (-0.008, 0.016, -0.008),
            (-0.025, 0.050, -0.025),
            (-0.055, 0.110, -0.055),
            (-0.085, 0.170, -0.085),
        ]
    elif feature_name == "stage267cf_trend_strength_replacement_score":
        scores = [
            (0.0, 0.0, 0.0),
            (0.015, -0.015, 0.015),
            (0.040, -0.035, 0.040),
            (0.070, -0.060, 0.070),
            (0.105, -0.090, 0.105),
        ]
    elif feature_name == "stage267cf_volatility_energy_transition_score":
        scores = [
            (0.0, 0.0, 0.0),
            (0.010, -0.010, 0.010),
            (0.030, -0.022, 0.030),
            (0.052, -0.040, 0.052),
            (0.075, -0.060, 0.075),
        ]
    else:
        scores = [
            (0.0, 0.0, 0.0),
            (0.012, -0.010, 0.012),
            (0.035, -0.026, 0.035),
            (0.060, -0.045, 0.060),
            (0.090, -0.070, 0.090),
        ]
    return cuts, scores


def append_model_features(
    source_model_path: Path,
    destination_model_path: Path,
    *,
    source_feature_count: int,
    profile_label: str,
    engineered_features: Sequence[str],
) -> None:
    io_path(destination_model_path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(source_model_path).open("r", encoding="utf-8-sig", newline="") as source_handle:
        rows = list(csv.DictReader(source_handle))
    fieldnames = ["record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long"]
    for offset, feature_name in enumerate(engineered_features):
        feature_index = int(source_feature_count) + offset
        cuts, scores = score_terms_for_feature(profile_label, feature_name)
        for cut_index, cut_value in enumerate(cuts):
            rows.append(
                {
                    "record_type": "cut",
                    "feature_index": str(feature_index),
                    "item_index": str(cut_index),
                    "value": f"{cut_value:.17g}",
                    "score_short": "",
                    "score_flat": "",
                    "score_long": "",
                }
            )
        for item_index, (score_short, score_flat, score_long) in enumerate(scores):
            rows.append(
                {
                    "record_type": "score",
                    "feature_index": str(feature_index),
                    "item_index": str(item_index),
                    "value": "",
                    "score_short": f"{score_short:.17g}",
                    "score_flat": f"{score_flat:.17g}",
                    "score_long": f"{score_long:.17g}",
                }
            )
    with io_path(destination_model_path).open("w", encoding="utf-8", newline="") as destination_handle:
        writer = csv.DictWriter(destination_handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def validate_score_table(feature_path: Path, model_path: Path, feature_order: Sequence[str]) -> dict[str, Any]:
    frame = pd.read_csv(io_path(feature_path), encoding="utf-8-sig")
    values = frame.loc[:, list(feature_order)].head(64).to_numpy(dtype="float64")
    table = load_ebm_score_table(model_path, feature_count=len(feature_order))
    probabilities = score_ebm_table_probabilities(table, values)
    error = float(abs(probabilities.sum(axis=1) - 1.0).max()) if len(probabilities) else 0.0
    return {
        "score_table_validation": "passed",
        "probability_rows_checked": int(len(probabilities)),
        "probability_sum_max_abs_error": error,
    }


def source_variants_by_alias() -> dict[str, list[dict[str, str]]]:
    rows = read_csv(SOURCE_VARIANT_MANIFEST_PATH)
    by_alias: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_alias.setdefault(row["candidate_alias"], []).append(row)
    return by_alias


def source_attempts_by_alias_test_tier() -> dict[tuple[str, str, str], dict[str, str]]:
    return {
        (row["candidate_alias"], row["test_id"], row["tier"]): row
        for row in read_csv(SOURCE_ATTEMPT_MANIFEST_PATH)
        if row.get("candidate_alias") and row.get("test_id") and row.get("tier")
    }


def source_contracts_by_alias_test() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row["candidate_alias"], row["test_id"]): row
        for row in read_csv(SOURCE_RUNTIME_CONTRACT_PATH)
        if row.get("candidate_alias") and row.get("test_id")
    }


def required_component_columns(profile: Mapping[str, Any]) -> set[str]:
    required: set[str] = set()
    for feature_name in profile["engineered_features"]:
        if feature_name == "stage267cf_loss_cluster_bar_state_proxy_score":
            required.add("log_return_1")
            continue
        required.update(column for column, _ in FEATURE_COMPONENTS[feature_name])
    return required


def select_source_variant(alias: str, profile: Mapping[str, Any], by_alias: Mapping[str, Sequence[Mapping[str, str]]]) -> Mapping[str, str]:
    rows = list(by_alias.get(alias, []))
    required = required_component_columns(profile)
    for test_id in profile["source_test_preferences"]:
        for row in rows:
            if row.get("test_id") != test_id:
                continue
            feature_columns = set(source_feature_order(repo_path(row["runtime_feature_file"])))
            if required.issubset(feature_columns):
                return row
    for row in rows:
        feature_columns = set(source_feature_order(repo_path(row["runtime_feature_file"])))
        if required.issubset(feature_columns):
            return row
    if not rows:
        raise KeyError(f"missing source variants for {alias}")
    raise KeyError(f"missing source variant with required components for {alias}: {sorted(required)}")


def materialization_plan_rows() -> list[dict[str, Any]]:
    queue_by_id = {row["queue_id"]: row for row in read_csv(SOURCE_MATERIALIZATION_QUEUE_PATH)}
    by_alias = source_variants_by_alias()
    rows: list[dict[str, Any]] = []
    order = 0
    for profile_label, profile in PROFILE_DEFINITIONS.items():
        source_queue_id = str(profile["source_queue_id"])
        queue = queue_by_id[source_queue_id]
        for alias in CANDIDATE_ORDER:
            source = select_source_variant(alias, profile, by_alias)
            order += 1
            plan_id = f"run267cf_{order:02d}_{alias}_{profile['profile_token']}"
            rows.append(
                {
                    "plan_id": plan_id,
                    "source_queue_id": source_queue_id,
                    "priority": queue.get("priority", "P0"),
                    "candidate_id": source["candidate_id"],
                    "candidate_alias": alias,
                    "candidate_role": source["candidate_role"],
                    "profile_label": profile_label,
                    "profile_token": profile["profile_token"],
                    "source_test_id": source["test_id"],
                    "source_queue_id_run267W": source["queue_id"],
                    "source_feature_file": source["runtime_feature_file"],
                    "source_model_file": source["runtime_model_file"],
                    "source_feature_order_hash": source["feature_order_hash"],
                    "source_feature_count": source["feature_count"],
                    "engineered_features": ";".join(profile["engineered_features"]),
                    "materialization_decision": "materialize_tier_a_and_duplicate_boundary_attempt_inputs",
                    "source_limitation": SOURCE_LIMITATION,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def materialize_variant(
    plan: Mapping[str, Any],
    attempts_by_key: Mapping[tuple[str, str, str], Mapping[str, str]],
    contracts_by_key: Mapping[tuple[str, str], Mapping[str, str]],
    *,
    order: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    alias = str(plan["candidate_alias"])
    source_test_id = str(plan["source_test_id"])
    profile_label = str(plan["profile_label"])
    profile_token = str(plan["profile_token"])
    plan_id = str(plan["plan_id"])
    variant_id = plan_id
    engineered_features = [part for part in str(plan["engineered_features"]).split(";") if part]
    source_feature_path = repo_path(str(plan["source_feature_file"]))
    source_model_path = repo_path(str(plan["source_model_file"]))
    base_feature_order = source_feature_order(source_feature_path)
    output_feature_order = [*base_feature_order, *engineered_features]
    feature_order_hash = ordered_hash(output_feature_order)

    variant_dir = VARIANT_ROOT / alias / variant_id
    feature_path = variant_dir / "features" / f"{variant_id}_features.csv"
    model_path = variant_dir / "models" / f"{variant_id}_model.csv"
    diagnostics, missing_cells = build_engineered_frame(
        source_feature_path,
        feature_path,
        feature_order=base_feature_order,
        profile_label=profile_label,
        engineered_features=engineered_features,
        variant_id=variant_id,
        candidate_alias=alias,
    )
    append_model_features(
        source_model_path,
        model_path,
        source_feature_count=len(base_feature_order),
        profile_label=profile_label,
        engineered_features=engineered_features,
    )
    validation = validate_score_table(feature_path, model_path, output_feature_order)
    common_feature_path = f"{COMMON_ROOT}/{alias}/{variant_id}/features/{feature_path.name}"
    common_model_path = f"{COMMON_ROOT}/{alias}/{variant_id}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    variant_row = {
        "variant_id": variant_id,
        "plan_id": plan_id,
        "source_queue_id": plan["source_queue_id"],
        "priority": plan["priority"],
        "candidate_id": plan["candidate_id"],
        "candidate_alias": alias,
        "candidate_role": plan["candidate_role"],
        "profile_label": profile_label,
        "profile_token": profile_token,
        "source_test_id": source_test_id,
        "source_feature_file": rel(source_feature_path),
        "source_feature_sha256": sha256_file_lf_normalized(source_feature_path),
        "runtime_feature_file": rel(feature_path),
        "runtime_feature_sha256": sha256_file_lf_normalized(feature_path),
        "source_model_file": rel(source_model_path),
        "source_model_sha256": sha256_file_lf_normalized(source_model_path),
        "runtime_model_file": rel(model_path),
        "runtime_model_sha256": sha256_file_lf_normalized(model_path),
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "source_feature_count": len(base_feature_order),
        "engineered_feature_count": len(engineered_features),
        "feature_count": len(output_feature_order),
        "feature_order": ";".join(output_feature_order),
        "feature_order_hash": feature_order_hash,
        "engineered_features": ";".join(engineered_features),
        "runtime_rows": int(pd.read_csv(io_path(feature_path), encoding="utf-8-sig", usecols=["bar_time_server"]).shape[0]),
        "missing_feature_cells": missing_cells,
        "score_table_validation": validation["score_table_validation"],
        "probability_rows_checked": validation["probability_rows_checked"],
        "probability_sum_max_abs_error": validation["probability_sum_max_abs_error"],
        "source_limitation": plan["source_limitation"],
        "claim_boundary": "materialization_only_no_candidate_selection_no_onnx",
    }

    contract_source = contracts_by_key.get((alias, source_test_id), {})
    runtime_contract = {
        "variant_id": variant_id,
        "candidate_id": plan["candidate_id"],
        "candidate_alias": alias,
        "candidate_role": plan["candidate_role"],
        "profile_label": profile_label,
        "source_test_id": source_test_id,
        "shared_contract": "US100 M5;2024 historical stress window;RuntimeProbeEA;run267W feature order plus run267CF engineered features;EBM score table extension;attempt set/ini identity",
        "feature_count": len(output_feature_order),
        "feature_order_hash": feature_order_hash,
        "model_backend": "ebm_table",
        "model_materialization_type": "research_score_table_orthogonal_loss_shape_state_extension_not_retrained_v1",
        "short_threshold": contract_source.get("short_threshold", "0.54"),
        "long_threshold": contract_source.get("long_threshold", "0.52"),
        "min_margin": contract_source.get("min_margin", "0"),
        "max_hold_bars": contract_source.get("max_hold_bars", "3"),
        "engineered_features": ";".join(engineered_features),
        "known_difference": (
            "appends orthogonal loss-shape/state or similar-replacement engineered features to run267W score table; "
            "no retraining; no weekday/month/hour hard filter"
        ),
        "runtime_claim_boundary": "research_only_execution_pending_no_selected_candidate_no_onnx",
    }

    attempt_rows: list[dict[str, Any]] = []
    for tier_index, (tier, role, token) in enumerate(
        (
            ("Tier A", "tier_only_total", "ta"),
            ("Tier A+B", "routed_total_duplicate_boundary", "rt"),
        ),
        start=1,
    ):
        source_attempt = attempts_by_key[(alias, source_test_id, tier)]
        source_set_path = repo_path(source_attempt["set_path"])
        source_ini_path = repo_path(source_attempt["ini_path"])
        source_set_values = parse_key_values(source_set_path)
        source_ini_values = parse_key_values(source_ini_path)
        attempt_name = f"{variant_id}_{token}_2024"
        telemetry = f"{COMMON_ROOT}/{alias}/{variant_id}/telemetry/{attempt_name}_telemetry.csv"
        summary = f"{COMMON_ROOT}/{alias}/{variant_id}/telemetry/{attempt_name}_summary.csv"
        model_id = f"{RUN_ID}_{variant_id}_score_table"
        set_values = dict(source_set_values)
        set_values.update(
            {
                "InpRunId": RUN_ID,
                "InpExplorationLabel": EXPLORATION_LABEL,
                "InpTierLabel": tier,
                "InpPrimaryActiveTier": "tier_a",
                "InpSplitLabel": PERIOD_LABEL,
                "InpModelPath": common_model_path,
                "InpModelId": model_id,
                "InpModelBackend": "ebm_table",
                "InpModelUseCommonFiles": "true",
                "InpFeatureCsvPath": common_feature_path,
                "InpFeatureCount": len(output_feature_order),
                "InpFeatureCsvUseCommonFiles": "true",
                "InpFeatureOrderHash": feature_order_hash,
                "InpFallbackEnabled": "false",
                "InpFallbackFeatureCsvPath": common_feature_path,
                "InpFallbackFeatureCount": len(output_feature_order),
                "InpFallbackModelPath": common_model_path,
                "InpFallbackModelId": model_id,
                "InpFallbackModelBackend": "ebm_table",
                "InpFallbackFeatureOrderHash": feature_order_hash,
                "InpTelemetryCsvPath": telemetry,
                "InpSummaryCsvPath": summary,
                "InpTelemetryUseCommonFiles": "true",
                "InpMagic": 26735000 + order * 10 + tier_index,
            }
        )
        set_payload = write_set(MT5_ROOT / f"{attempt_name}.set", set_values)
        ini_values = dict(source_ini_values)
        ini_values.update(
            {
                "ExpertParameters": Path(set_payload["path"]).name,
                "Report": f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}",
            }
        )
        ini_payload = write_ini(MT5_ROOT / f"{attempt_name}.ini", ini_values)
        attempt_rows.append(
            {
                "attempt_name": attempt_name,
                "variant_id": variant_id,
                "candidate_id": plan["candidate_id"],
                "candidate_alias": alias,
                "candidate_role": plan["candidate_role"],
                "profile_label": profile_label,
                "source_test_id": source_test_id,
                "tier": tier,
                "attempt_role": role,
                "record_view_prefix": f"mt5_{token}_{alias}_{profile_token}",
                "set_path": set_payload["path"],
                "set_sha256": set_payload["sha256"],
                "ini_path": ini_payload["path"],
                "ini_sha256": ini_payload["sha256"],
                "common_telemetry_path": telemetry,
                "common_summary_path": summary,
                "execution_status": "not_executed",
            }
        )
    return variant_row, attempt_rows, runtime_contract, diagnostics


def build_receipts(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    for row in queue_rows:
        if row.get("queue_id") not in {PROFILE_DEFINITIONS["loss_shape_proxy_minimal"]["source_queue_id"], PROFILE_DEFINITIONS["similar_replacement_impulse"]["source_queue_id"]}:
            continue
        receipts.append(
            {
                "receipt_id": row["queue_id"],
                "hypothesis": row.get("hypothesis"),
                "decision_use": row.get("decision_use"),
                "comparison_baseline": row.get("comparison_baseline"),
                "control_variables": row.get("control_variables"),
                "changed_variables": row.get("changed_variables"),
                "sample_scope": row.get("sample_scope"),
                "success_criteria": row.get("success_criteria"),
                "failure_criteria": row.get("failure_criteria"),
                "invalid_conditions": row.get("invalid_conditions"),
                "stop_conditions": row.get("stop_conditions"),
                "evidence_plan": (
                    "feature/model/set/ini manifests, feature-order hash, data-integrity receipt, "
                    "next MT5 KPI/trade/curve/time-slice review"
                ),
            }
        )
    return receipts


def held_queue_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    held_ids = {
        "run267cf_q04_s264_aih_trace_watch": "P1 trace watch waits for P0 materialized evidence(P1 추적 관찰은 P0 물질화 근거 이후)",
        "run267cf_q05_s258_stc_stress_reopen_rule": "P1 stress reopen waits for P0 control read(P1 압박 재개는 P0 대조 판독 이후)",
    }
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        queue_id = row.get("queue_id", "")
        if queue_id in held_ids:
            rows.append(
                {
                    "queue_id": queue_id,
                    "priority": row.get("priority"),
                    "hold_reason": held_ids[queue_id],
                    "next_condition": NEXT_ACTION,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def data_integrity_receipts(variant_count: int) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267cf_source_surface_time_axis",
            "data_source": rel(SOURCE_VARIANT_MANIFEST_PATH),
            "time_axis": "bar_time_server from run267W runtime feature files; 2024 historical stress window",
            "sample_scope": "US100 M5; five candidate aliases; two orthogonal profiles; Tier A and duplicate-boundary Tier A+B attempt inputs",
            "missing_or_duplicate_check": "runtime feature files materialized with row counts and missing engineered cells recorded",
            "feature_label_boundary": "engineered features use bar-state columns and current/prior closed-bar rolling state only; no future trade result",
            "split_boundary": PERIOD_LABEL,
            "leakage_risk": "true MAE/MFE and trade-loss cluster unavailable; q01 is proxy-only and must not be read as true trade-path evidence",
            "data_hash_or_identity": f"variants={variant_count};source_manifest_sha256={sha256_file_lf_normalized(SOURCE_VARIANT_MANIFEST_PATH)}",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        }
    ]


def control_reanchor_audit(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for alias in sorted(CONTROL_ALIASES):
        profiles = sorted({str(row["profile_label"]) for row in variant_rows if row.get("candidate_alias") == alias})
        rows.append(
            {
                "audit_id": f"control_reanchor_{alias}",
                "status": "passed" if len(profiles) == len(PROFILE_DEFINITIONS) else "failed",
                "evidence": f"profiles={';'.join(profiles)}",
                "effect": "control candidate stays in the same P0 tranche as challengers(대조 후보가 도전자와 같은 P0 묶음에 남음)",
            }
        )
    return rows


def feature_order_data_audit(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in variant_rows:
        passed = (
            int(row["feature_count"]) == int(row["source_feature_count"]) + int(row["engineered_feature_count"])
            and str(row["score_table_validation"]) == "passed"
            and float(row["probability_sum_max_abs_error"]) <= 1e-9
        )
        rows.append(
            {
                "audit_id": f"feature_order_{row['variant_id']}",
                "status": "passed" if passed else "failed",
                "evidence": (
                    f"feature_count={row['feature_count']};source={row['source_feature_count']};"
                    f"engineered={row['engineered_feature_count']};hash={row['feature_order_hash']}"
                ),
                "effect": "blocks MT5 execution if feature/model order is not coherent(피처/모델 순서가 맞지 않으면 MT5 실행 차단)",
            }
        )
    return rows


def result_judgment_rows(variant_count: int, attempt_count: int) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267CF pool-wide orthogonal loss-shape/state materialization(267CF 후보군 전체 직교 손실 형태/상태 물질화)",
            "evidence_available": f"variants={variant_count};attempts={attempt_count};feature_order_audit=completed;data_integrity=usable_with_boundary",
            "evidence_missing": "MT5 tester output, KPI, trade list, balance/equity curve, time-slice review, Adapter implementation, ONNX parity",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이번 실행은 후보를 고른 것이 아니라, 다음 MT5 실행에 올릴 실제 입력 파일을 만든 것이다.",
        }
    ]


def gate_audit_rows(variant_count: int, attempt_count: int, held_count: int, audit_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    audit_passed = all(row.get("status") == "passed" for row in audit_rows)
    return [
        {
            "gate_id": "run267ce_queue_consumed(267CE 큐 소비)",
            "status": "passed",
            "evidence": f"source_queue={rel(SOURCE_MATERIALIZATION_QUEUE_PATH)}",
            "effect": "run267CF follows the current next action(267CF가 현재 다음 행동을 따름)",
        },
        {
            "gate_id": "p0_variants_materialized(P0 변형 물질화)",
            "status": "passed" if variant_count == 10 else "failed",
            "evidence": f"variants={variant_count}",
            "effect": "five candidates x two profiles are ready for MT5 input(다섯 후보 x 두 프로필이 MT5 입력 준비)",
        },
        {
            "gate_id": "attempts_materialized(시도 물질화)",
            "status": "passed" if attempt_count == 20 else "failed",
            "evidence": f"attempts={attempt_count}",
            "effect": "Tier A and duplicate-boundary Tier A+B attempt files exist(Tier A와 중복 경계 Tier A+B 시도 파일 존재)",
        },
        {
            "gate_id": "feature_order_data_audit(피처 순서/데이터 감사)",
            "status": "passed" if audit_passed else "failed",
            "evidence": f"audit_rows={len(audit_rows)}",
            "effect": "prevents invalid tester batch(무효 테스터 묶음 방지)",
        },
        {
            "gate_id": "p1_held_not_silently_dropped(P1 보류 누락 방지)",
            "status": "passed" if held_count == 2 else "failed",
            "evidence": f"held_rows={held_count}",
            "effect": "s264_aih trace watch and s258 stress reopen are held with conditions(s264_aih 추적과 s258 압박 재개가 조건부 보류됨)",
        },
        {
            "gate_id": "claim_boundary_preserved(주장 경계 보존)",
            "status": "passed",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "materialization cannot become candidate selection(물질화가 후보 선택으로 바뀌지 않음)",
        },
    ]


def build_lineage_receipt(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267cf_lineage",
            "source_inputs": ";".join(result["sources"].values()),
            "producer": rel(PRODUCER_PATH),
            "consumer": NEXT_ACTION,
            "artifact_paths": ";".join(result["outputs"].values()),
            "artifact_hashes": "registered_in_artifact_registry(산출물 등록부에 기록)",
            "registry_links": f"{rel(STAGE_LEDGER_PATH)};{rel(PROJECT_LEDGER_PATH)};{rel(RUN_REGISTRY_PATH)};{rel(ARTIFACT_REGISTRY_PATH)}",
            "availability": "tracked_and_common_files_handoff(추적됨 및 공통 파일 인계)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        }
    ]


def build_result() -> dict[str, Any]:
    required = [
        SOURCE_REVIEW_RESULT_PATH,
        SOURCE_MATERIALIZATION_QUEUE_PATH,
        SOURCE_FEATURE_BLUEPRINT_PATH,
        SOURCE_CANDIDATE_PIVOT_PATH,
        SOURCE_VARIANT_MANIFEST_PATH,
        SOURCE_ATTEMPT_MANIFEST_PATH,
        SOURCE_RUNTIME_CONTRACT_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))

    created_at = utc_now()
    queue_rows = read_csv(SOURCE_MATERIALIZATION_QUEUE_PATH)
    plan_rows = materialization_plan_rows()
    attempts_by_key = source_attempts_by_alias_test_tier()
    contracts_by_key = source_contracts_by_alias_test()
    variant_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    runtime_rows: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    for index, plan in enumerate(plan_rows, start=1):
        variant, attempts, runtime_contract, diagnostic_rows = materialize_variant(
            plan,
            attempts_by_key,
            contracts_by_key,
            order=index,
        )
        variant_rows.append(variant)
        attempt_rows.extend(attempts)
        runtime_rows.append(runtime_contract)
        diagnostics.extend(diagnostic_rows)

    held_rows = held_queue_rows(queue_rows)
    control_rows = control_reanchor_audit(variant_rows)
    feature_audit_rows = feature_order_data_audit(variant_rows)
    data_receipts = data_integrity_receipts(len(variant_rows))
    experiment_receipts = build_receipts(queue_rows)
    result_judgment = result_judgment_rows(len(variant_rows), len(attempt_rows))
    gate_rows = gate_audit_rows(len(variant_rows), len(attempt_rows), len(held_rows), feature_audit_rows)
    outputs = {
        "materialization_plan": rel(MATERIALIZATION_PLAN_PATH),
        "variant_manifest": rel(VARIANT_MANIFEST_PATH),
        "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
        "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
        "feature_engineering_diagnostics": rel(FEATURE_ENGINEERING_DIAGNOSTICS_PATH),
        "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
        "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
        "artifact_lineage_receipt": rel(ARTIFACT_LINEAGE_RECEIPT_PATH),
        "control_reanchor_audit": rel(CONTROL_REANCHOR_AUDIT_PATH),
        "feature_order_data_audit": rel(FEATURE_ORDER_DATA_AUDIT_PATH),
        "held_queue": rel(HELD_QUEUE_PATH),
        "result_judgment": rel(RESULT_JUDGMENT_PATH),
        "gate_audit": rel(GATE_AUDIT_PATH),
        "run_manifest": rel(RUN_MANIFEST_PATH),
        "lineage": rel(LINEAGE_PATH),
        "review_result": rel(REVIEW_RESULT_PATH),
        "report": rel(REPORT_PATH),
    }
    result: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "source_limitation": SOURCE_LIMITATION,
        "plan_rows": plan_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "runtime_contract": runtime_rows,
        "feature_engineering_diagnostics": diagnostics,
        "data_integrity_receipt": data_receipts,
        "experiment_design_receipt": experiment_receipts,
        "control_reanchor_audit": control_rows,
        "feature_order_data_audit": feature_audit_rows,
        "held_queue": held_rows,
        "result_judgment": result_judgment,
        "gate_audit": gate_rows,
        "variant_count": len(variant_rows),
        "attempt_count": len(attempt_rows),
        "runtime_contract_count": len(runtime_rows),
        "diagnostic_row_count": len(diagnostics),
        "held_queue_count": len(held_rows),
        "control_reanchor_count": len(control_rows),
        "feature_order_audit_count": len(feature_audit_rows),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": {
            "run267CE_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "run267CE_materialization_queue": rel(SOURCE_MATERIALIZATION_QUEUE_PATH),
            "run267CE_feature_blueprint": rel(SOURCE_FEATURE_BLUEPRINT_PATH),
            "run267CE_candidate_pivot": rel(SOURCE_CANDIDATE_PIVOT_PATH),
            "run267CE_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
            "run267W_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
            "run267W_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
            "run267W_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
        },
        "outputs": outputs,
    }
    result["artifact_lineage_receipt"] = build_lineage_receipt(result)
    return result


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(MATERIALIZATION_PLAN_PATH, result["plan_rows"], PLAN_COLUMNS)
    write_csv(VARIANT_MANIFEST_PATH, result["variant_manifest"], VARIANT_COLUMNS)
    write_csv(ATTEMPT_MANIFEST_PATH, result["attempt_manifest"], ATTEMPT_COLUMNS)
    write_csv(RUNTIME_CONTRACT_PATH, result["runtime_contract"], RUNTIME_CONTRACT_COLUMNS)
    write_csv(FEATURE_ENGINEERING_DIAGNOSTICS_PATH, result["feature_engineering_diagnostics"], DIAGNOSTIC_COLUMNS)
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"], DATA_INTEGRITY_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], RECEIPT_COLUMNS)
    write_csv(ARTIFACT_LINEAGE_RECEIPT_PATH, result["artifact_lineage_receipt"])
    write_csv(CONTROL_REANCHOR_AUDIT_PATH, result["control_reanchor_audit"], AUDIT_COLUMNS)
    write_csv(FEATURE_ORDER_DATA_AUDIT_PATH, result["feature_order_data_audit"], AUDIT_COLUMNS)
    write_csv(HELD_QUEUE_PATH, result["held_queue"], HELD_QUEUE_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"], RESULT_JUDGMENT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, result["gate_audit"])
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": STATUS,
            "created_at_utc": result["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "materialization_boundary": MATERIALIZATION_BOUNDARY,
            "sources": result["sources"],
            "outputs": result["outputs"],
            "next_action": NEXT_ACTION,
        },
    )
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": result["sources"],
            "producer": rel(PRODUCER_PATH),
            "consumer": NEXT_ACTION,
            "artifact_paths": result["outputs"],
            "artifact_hashes": "registered_in_artifact_registry(산출물 등록부에 기록)",
            "registry_links": {
                "stage_ledger": rel(STAGE_LEDGER_PATH),
                "project_ledger": rel(PROJECT_LEDGER_PATH),
                "run_registry": rel(RUN_REGISTRY_PATH),
                "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
            },
            "availability": "tracked_and_common_files_handoff(추적됨 및 공통 파일 인계)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267CF Pool-wide Orthogonal Loss-shape/State Materialization(267단계 267CF 후보군 전체 직교 손실 형태/상태 물질화)",
        "",
        "- action(행동): run267CE(267CE 실행)의 P0 queue(P0 큐)를 실제 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 물질화했다.",
        "- effect(효과): 다음 run267CG(267CG 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질)를 볼 수 있다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- variants(변형): `{result['variant_count']}`",
        f"- attempts(시도): `{result['attempt_count']}`",
        f"- held_queue(보류 큐): `{result['held_queue_count']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "이번에는 후보를 고르지 않았다. 대신 다섯 후보 전체를 같은 두 실험 축에 올렸다.",
        "Effect(효과): `s264_aih`만 밀거나 `s258_stc`만 다시 수리하지 않고, 방어 대조군과 검증 중심 후보까지 같은 조건에서 깨지는지 보게 된다.",
        "",
        "첫 축은 loss-shape proxy(손실 형태 대체값)다. 실제 MAE/MFE(최대 불리/유리 이동) trade path(거래 경로)는 아직 없으므로 bar-state proxy(봉 상태 대체값)로만 물질화했다.",
        "Effect(효과): 이 결과는 진짜 거래 경로 검증이 아니라 다음 MT5 실행 전 단계의 연구 입력이라는 경계를 보존한다.",
        "",
        "둘째 축은 similar replacement impulse(유사 대체 임펄스)다. ADX(평균 방향성 지수) 하나에 붙은 우연인지, 비슷한 시장 의미에서도 버티는지 보려는 공격적 축이다.",
        "Effect(효과): 필터를 덧붙이는 것만 하지 않고, non-flat impulse(비평탄 임펄스) 점수도 함께 시험한다.",
        "",
        "## Variants(변형)",
        "",
        "| variant(변형) | candidate(후보) | profile(프로필) | source test(원천 시험) | features(피처 수) | validation(검증) |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    for row in result["variant_manifest"]:
        lines.append(
            f"| `{row['variant_id']}` | `{row['candidate_alias']}` | `{row['profile_label']}` | "
            f"`{row['source_test_id']}` | {row['feature_count']} | `{row['score_table_validation']}` |"
        )
    lines.extend(
        [
            "",
            "## Held Queue(보류 큐)",
            "",
            "| queue(큐) | reason(이유) | next condition(다음 조건) |",
            "| --- | --- | --- |",
        ]
    )
    for row in result["held_queue"]:
        lines.append(f"| `{row['queue_id']}` | {row['hold_reason']} | `{row['next_condition']}` |")
    lines.extend(
        [
            "",
            "## Data Integrity(데이터 무결성)",
            "",
            "- data_source(데이터 원천): run267W(267W 실행) true internal ablation runtime feature surface(진짜 내부 제거 런타임 피처 표면).",
            "- time_axis(시간축): `bar_time_server`, 2024 historical stress window(2024 과거 압박 구간).",
            "- feature_label_boundary(피처/라벨 경계): 새 피처는 현재/과거 닫힌 봉 상태만 쓰며, 미래 거래 결과를 쓰지 않는다.",
            "- leakage_risk(누수 위험): 진짜 MAE/MFE(최대 불리/유리 이동)와 trade loss cluster(거래 손실 군집)는 아직 없으므로 q01은 proxy(대체값)로만 읽어야 한다.",
            "- integrity_judgment(무결성 판정): `usable_with_boundary(경계 포함 사용 가능)`.",
            "",
            "## Result Judgment(결과 판정)",
            "",
            "- result_subject(결과 대상): `run267CF_pool_wide_orthogonal_loss_shape_state_materialization`.",
            "- evidence_available(사용 가능 근거): feature/model/set/ini manifests(피처/모델/설정/초기화 목록), feature order hash(피처 순서 해시), data integrity receipt(데이터 무결성 영수증).",
            "- evidence_missing(부족한 근거): MT5 tester output(테스터 출력), KPI(핵심 성과 지표), trade list(거래 목록), curve/time-slice/trade-quality review(곡선/시간구간/거래품질 검토), Adapter(어댑터), ONNX parity(ONNX 동등성).",
            f"- judgment_label(판정 라벨): `{JUDGMENT}`.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            f"- next_condition(다음 조건): `{NEXT_ACTION}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_queue(원천 큐): `{rel(SOURCE_MATERIALIZATION_QUEUE_PATH)}`.",
            f"- source_surface(원천 표면): `{rel(SOURCE_VARIANT_MANIFEST_PATH)}`.",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`.",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`.",
            f"- report(보고서): `{rel(REPORT_PATH)}`.",
        ]
    )
    return "\n".join(lines)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + focus_block, 1)


def update_stage267_workspace_block(text: str, *, report_entry: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_report = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not inserted_report:
                output.append(report_entry)
                inserted_report = True
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {STATUS}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                if not inserted_report:
                    output.append(report_entry)
                    inserted_report = True
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    if in_stage267 and not inserted_report:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267CF_pool_wide_orthogonal_loss_shape_state_materialization"
        f"(267CF 후보군 전체 직교 손실 형태/상태 물질화): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267CF(267CF 실행)는 run267CE(267CE 실행)의 P0 materialization queue(P0 물질화 큐)를 실제 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.",
            f"Effect(효과): variants(변형) `{result['variant_count']}`개와 MT5(MetaTrader 5, 메타트레이더5) attempts(시도) `{result['attempt_count']}`개를 만들고 다음 행동을 `{NEXT_ACTION}`으로 고정했다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(
            text,
            "- adapter_under_review(검토 중 어댑터):",
            "- adapter_under_review(검토 중 어댑터): `pool_wide_orthogonal_loss_shape_state_materialization`",
        )
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = append_after_contains(
            text,
            "stage267_run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design.md",
            report_line,
        )
        text = append_block_once(text, "Run267CF(267CF 실행)는 run267CE", block)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267CF(267CF 실행) pool-wide orthogonal loss-shape/state materialization"
        f"(후보군 전체 직교 손실 형태/상태 물질화) `{STATUS}`. "
        f"Effect(효과): run267CE(267CE 실행)의 설계 큐를 variants(변형) `{result['variant_count']}`개와 "
        f"MT5(MetaTrader 5, 메타트레이더5) attempts(시도) `{result['attempt_count']}`개로 물질화했으며, "
        "selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        report_entry=f"  run267CF_pool_wide_orthogonal_loss_shape_state_materialization_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267CF_design_script", "producer_script", PRODUCER_PATH, "Builds run267CF orthogonal materialization."),
        ("stage267_run267CF_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267CE review result."),
        ("stage267_run267CF_source_materialization_queue", "source_materialization_queue", SOURCE_MATERIALIZATION_QUEUE_PATH, "Source run267CE materialization queue."),
        ("stage267_run267CF_source_run267W_variant_manifest", "source_variant_manifest", SOURCE_VARIANT_MANIFEST_PATH, "Source run267W feature/model surface."),
        ("stage267_run267CF_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH, "Run267CF materialization plan."),
        ("stage267_run267CF_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Run267CF variant manifest."),
        ("stage267_run267CF_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267CF MT5 attempt manifest."),
        ("stage267_run267CF_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267CF runtime contract."),
        ("stage267_run267CF_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267CF data integrity receipt."),
        ("stage267_run267CF_feature_order_data_audit", "feature_order_data_audit", FEATURE_ORDER_DATA_AUDIT_PATH, "Run267CF feature order/data audit."),
        ("stage267_run267CF_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267CF result judgment."),
        ("stage267_run267CF_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267CF gate audit."),
        ("stage267_run267CF_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267CF run manifest."),
        ("stage267_run267CF_lineage", "lineage", LINEAGE_PATH, "Run267CF lineage."),
        ("stage267_run267CF_review_result", "review_result", REVIEW_RESULT_PATH, "Run267CF review result."),
        ("stage267_run267CF_report", "review_report", REPORT_PATH, "Run267CF user-facing report."),
    ]
    rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    ]
    for row in result["variant_manifest"]:
        rows.append(
            {
                "artifact_id": f"stage267_run267CF_feature_{safe_token(row['variant_id'])}",
                "artifact_type": "runtime_feature_csv",
                "path": row["runtime_feature_file"],
                "sha256": row["runtime_feature_sha256"],
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Runtime feature CSV for {row['variant_id']}.",
            }
        )
        rows.append(
            {
                "artifact_id": f"stage267_run267CF_model_{safe_token(row['variant_id'])}",
                "artifact_type": "runtime_score_table_model",
                "path": row["runtime_model_file"],
                "sha256": row["runtime_model_sha256"],
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Runtime score-table model for {row['variant_id']}.",
            }
        )
    return rows


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    notes = (
        f"variants={result['variant_count']};attempts={result['attempt_count']};"
        f"held_queue={result['held_queue_count']};next_action={NEXT_ACTION};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267CF_pool_wide_orthogonal_loss_shape_state_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "pool_wide_orthogonal_loss_shape_state_materialization",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B 2024 attempt inputs; true Tier B fallback blocked",
        "scoreboard": "feature_model_set_ini_materialization_no_trading_kpi",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_mt5_kpi_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_pool_wide_orthogonal_loss_shape_state_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__pool_wide_orthogonal_loss_shape_state_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pool_wide_orthogonal_loss_shape_state_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "feature_model_set_ini_materialization",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B 2024 attempt inputs; true Tier B fallback blocked",
        "kpi_scope": "materialization_no_trading_kpi",
        "scoreboard_lane": "orthogonal_loss_shape_state_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={result['variant_count']};attempts={result['attempt_count']};held_queue={result['held_queue_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at, result), key="artifact_id")


def execute() -> dict[str, Any]:
    result = build_result()
    write_outputs(result)
    update_ledgers_and_artifacts(str(result["created_at_utc"]), result)
    update_current_truth_docs(result)
    return result


def main() -> int:
    result = execute()
    print(
        json.dumps(
            {
                "status": result["status"],
                "variants": result["variant_count"],
                "attempts": result["attempt_count"],
                "held_queue": result["held_queue_count"],
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
