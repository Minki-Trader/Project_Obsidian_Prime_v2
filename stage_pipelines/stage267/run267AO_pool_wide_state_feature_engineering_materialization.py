from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import dataclass
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
    attempt_payload,
    copy_to_common,
)
from foundation.models.ebm_score_table import load_ebm_score_table, score_ebm_table_probabilities
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import run267AN_noncalendar_state_guard_repair_followup_or_prune_design as source_design
from stage_pipelines.stage267 import run267W_true_internal_ablation_score_table_materialization as source_tables
from stage_pipelines.stage267.run267AC_noncalendar_state_guard_score_table_materialization import (
    append_after_contains,
    append_block_once,
    as_float,
    cell,
    prepend_current_focus,
    read_text,
    rel,
    repo_path,
    safe_token,
    utc_now,
    write_json,
    write_md,
    write_runtime_csv,
    write_text,
)


STAGE_ID = input_probe.STAGE_ID
RUN_NUMBER = "run267AO"
RUN_ID = "run267AO_stage267_pool_wide_state_feature_engineering_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_SCORE_TABLE_RUN_ID = source_tables.RUN_ID
STATUS = "run267AO_pool_wide_state_feature_engineering_materialized_execution_pending"
JUDGMENT = "pool_wide_state_feature_engineering_materialized_execution_pending_no_candidate_selection"
NEXT_ACTION = "run267AP_execute_pool_wide_state_feature_engineering_mt5_batch"
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY

STAGE_ROOT = input_probe.STAGE_ROOT
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_state_feature_engineering_materialization"
VARIANT_ROOT = RUN_ROOT / "variants"

SOURCE_QUEUE_PATH = source_design.NEXT_EXPERIMENT_QUEUE_PATH
SOURCE_REPAIR_DECISION_PATH = source_design.REPAIR_BRANCH_DECISION_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_VARIANT_MANIFEST_PATH = source_tables.VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_tables.RUNTIME_CONTRACT_PATH
SOURCE_DESIGN_REPORT_PATH = source_design.REPORT_PATH
SOURCE_SCORE_TABLE_REPORT_PATH = source_tables.REPORT_PATH

STATE_FEATURE_MATRIX_PATH = RUN_ROOT / "state_feature_engineering_matrix.csv"
MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "state_feature_materialization_queue.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "state_feature_variant_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
STATE_FEATURE_DIAGNOSTICS_PATH = RUN_ROOT / "state_feature_diagnostics.csv"
PARITY_CHECK_PATH = RUN_ROOT / "zero_state_feature_parity_check.csv"
SURFACE_ALIGNMENT_PATH = RUN_ROOT / "surface_alignment_check.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempts.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AO_pool_wide_state_feature_engineering_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AO_pool_wide_state_feature_engineering_materialization.py")

STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

COMMON_ROOT = "OPV2/s267ao/run267AO_pool_wide_state_feature_engineering"
PERIOD_LABEL = input_probe.PERIOD_LABEL
MODEL_MATERIALIZATION_TYPE = "research_score_table_pool_wide_state_feature_engineering_extension_not_retrained_v1"
CSV_MODEL_COLUMNS = ("record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long")
STATE_FEATURE_CUTS = (0.25, 0.50, 0.75)
STATE_FEATURE_TERMS = (
    (0.0, 0.0, 0.0),
    (0.0, 0.0, 0.0),
    (-0.018, 0.036, -0.018),
    (-0.040, 0.080, -0.040),
    (-0.065, 0.130, -0.065),
)

STAGE_LEDGER_COLUMNS = source_tables.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_tables.ARTIFACT_COLUMNS

CANDIDATE_ROLES = {
    "s264_aih": ("s264_allow_inner_high_quarter", "challenger_core"),
    "s264_lc": ("s264_lowrank_control", "defensive_control"),
    "s262_lih": ("s262_lowrank_inner_half_filter", "validation_heavy"),
    "s264_aia": ("s264_allow_inner_all_oos_anchor", "oos_anchor"),
    "s258_stc": ("s258_short_tight_control", "stress_challenger"),
}


@dataclass(frozen=True)
class StateFeatureProfile:
    profile_id: str
    feature_name: str
    source_test_preferences: tuple[str, ...]
    components: tuple[tuple[str, str], ...]
    aggregation: str
    intent: str


STATE_FEATURE_PROFILES = (
    StateFeatureProfile(
        profile_id="return_shock_absorption",
        feature_name="stage267_state_return_shock_absorption_score",
        source_test_preferences=("abl_price_return_range", "rep_volatility_atr", "abl_volatility_bandwidth"),
        components=(
            ("return_zscore_20", "abs"),
            ("return_1_over_atr_14", "abs"),
            ("log_return_3", "abs"),
            ("close_prev_close_ratio", "abs_center_1"),
        ),
        aggregation="mean_high_pressure",
        intent="check_if_candidates_survive_return_shock_state_without_literal_calendar_filter",
    ),
    StateFeatureProfile(
        profile_id="volatility_regime_expansion",
        feature_name="stage267_state_volatility_regime_expansion_score",
        source_test_preferences=("rep_volatility_atr", "abl_volatility_bandwidth", "abl_price_return_range"),
        components=(
            ("atr_14_over_atr_50", "raw"),
            ("historical_vol_5_over_20", "raw"),
            ("historical_vol_20", "raw"),
            ("bollinger_width_20", "raw"),
        ),
        aggregation="mean_high_pressure",
        intent="check_if_volatility_regime_width_reduces_repeated_month_weekday_holes_without_threshold_tweak",
    ),
    StateFeatureProfile(
        profile_id="range_expansion_pressure",
        feature_name="stage267_state_range_expansion_pressure_score",
        source_test_preferences=("abl_price_return_range", "rep_volatility_atr", "abl_volatility_bandwidth"),
        components=(
            ("hl_range", "raw"),
            ("close_open_ratio", "abs_center_1"),
            ("gap_percent", "abs"),
            ("bb_position_20", "abs_center_0_5"),
        ),
        aggregation="mean_high_pressure",
        intent="check_if_range_expansion_state_is_more_structural_than_single_ATR_or_ADX_repair",
    ),
    StateFeatureProfile(
        profile_id="trend_strength_disagreement",
        feature_name="stage267_state_trend_strength_disagreement_score",
        source_test_preferences=("rep_trend_strength_adx", "abl_trend_strength_direction"),
        components=(
            ("adx_14", "raw"),
            ("di_spread_14", "abs"),
            ("vortex_indicator", "abs_center_1"),
            ("ema20_ema50_diff", "abs"),
        ),
        aggregation="dispersion_plus_pressure",
        intent="check_if_trend_strength_meaning_survives_ADX_similar_axis_replacement",
    ),
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def require_inputs() -> None:
    required = [
        SOURCE_QUEUE_PATH,
        SOURCE_REPAIR_DECISION_PATH,
        SOURCE_FAILURE_MEMORY_PATH,
        SOURCE_VARIANT_MANIFEST_PATH,
        SOURCE_RUNTIME_CONTRACT_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def source_variants_by_alias() -> dict[str, list[dict[str, str]]]:
    rows = read_csv(SOURCE_VARIANT_MANIFEST_PATH)
    result: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        result.setdefault(str(row.get("candidate_alias", "")), []).append(row)
    return result


def source_contracts_by_alias_test() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (str(row.get("candidate_alias", "")), str(row.get("test_id", ""))): row
        for row in read_csv(SOURCE_RUNTIME_CONTRACT_PATH)
        if row.get("candidate_alias") and row.get("test_id")
    }


def select_source_variant(alias: str, profile: StateFeatureProfile, by_alias: Mapping[str, Sequence[Mapping[str, str]]]) -> Mapping[str, str]:
    candidates = list(by_alias.get(alias, []))
    for test_id in profile.source_test_preferences:
        for row in candidates:
            if row.get("test_id") == test_id:
                return row
    if not candidates:
        raise KeyError(f"missing source variants for {alias}")
    return candidates[0]


def transformed_series(surface: pd.DataFrame, component: tuple[str, str]) -> pd.Series:
    column, transform = component
    if column not in surface.columns:
        raise KeyError(f"missing engineered feature source column: {column}")
    series = pd.to_numeric(surface[column], errors="coerce").astype("float64")
    if transform == "raw":
        return series
    if transform == "abs":
        return series.abs()
    if transform == "abs_center_1":
        return (series - 1.0).abs()
    if transform == "abs_center_0_5":
        return (series - 0.5).abs()
    raise ValueError(f"unknown transform: {transform}")


def component_thresholds(surface: pd.DataFrame, profile: StateFeatureProfile) -> dict[str, dict[str, float]]:
    thresholds: dict[str, dict[str, float]] = {}
    for component in profile.components:
        key = f"{component[0]}:{component[1]}"
        series = transformed_series(surface, component).replace([np.inf, -np.inf], np.nan).dropna()
        if series.empty:
            thresholds[key] = {"q25": 0.0, "q50": 0.0, "q75": 0.0}
            continue
        thresholds[key] = {
            "q25": float(series.quantile(0.25)),
            "q50": float(series.quantile(0.50)),
            "q75": float(series.quantile(0.75)),
        }
    return thresholds


def scaled_component(value: float, q25: float, q75: float) -> float:
    if not math.isfinite(value):
        return 0.0
    if q75 <= q25:
        return 0.0
    return max(0.0, min(1.0, (value - q25) / (q75 - q25)))


def component_scalar(raw_row: Mapping[str, Any], component: tuple[str, str]) -> float:
    column, transform = component
    value = as_float(raw_row.get(column), float("nan"))
    if transform == "raw":
        return value
    if transform == "abs":
        return abs(value)
    if transform == "abs_center_1":
        return abs(value - 1.0)
    if transform == "abs_center_0_5":
        return abs(value - 0.5)
    raise ValueError(f"unknown transform: {transform}")


def profile_score(raw_row: Mapping[str, Any], thresholds: Mapping[str, Mapping[str, float]], profile: StateFeatureProfile) -> float:
    scaled: list[float] = []
    for component in profile.components:
        key = f"{component[0]}:{component[1]}"
        value = component_scalar(raw_row, component)
        current = thresholds[key]
        scaled.append(scaled_component(value, current["q25"], current["q75"]))
    if not scaled:
        return 0.0
    if profile.aggregation == "mean_high_pressure":
        return float(sum(scaled) / len(scaled))
    if profile.aggregation == "dispersion_plus_pressure":
        return float(max(0.0, min(1.0, 0.55 * (sum(scaled) / len(scaled)) + 0.45 * (max(scaled) - min(scaled)))))
    raise ValueError(f"unknown aggregation: {profile.aggregation}")


def append_state_feature_to_runtime(
    source_variant: Mapping[str, str],
    profile: StateFeatureProfile,
    destination: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], pd.DataFrame]:
    source_feature_path = repo_path(str(source_variant["runtime_feature_file"]))
    raw_surface_path = repo_path(str(source_variant["input_surface_file"]))
    feature_frame = pd.read_csv(io_path(source_feature_path), encoding="utf-8-sig")
    raw_surface = pd.read_csv(io_path(raw_surface_path), encoding="utf-8-sig")
    raw_by_time = {str(row["bar_time_server"]): row for row in raw_surface.to_dict("records")}
    thresholds = component_thresholds(raw_surface, profile)
    source_feature_order = [column for column in feature_frame.columns if column != "bar_time_server"]
    extended_feature_order = [*source_feature_order, profile.feature_name]

    rows: list[dict[str, Any]] = []
    scores: list[float] = []
    signal_scores: list[float] = []
    signal_rows = 0
    high_signal_rows = 0
    context_missing_rows = 0
    for row in feature_frame.to_dict("records"):
        current = dict(row)
        raw_row = raw_by_time.get(str(row.get("bar_time_server", "")))
        if raw_row is None:
            context_missing_rows += 1
            score = 0.0
        else:
            score = profile_score(raw_row, thresholds, profile)
        current[profile.feature_name] = score
        scores.append(score)
        signal = int(round(as_float(row.get(source_tables.SOURCE_SIGNAL_COLUMN), 0.0)))
        if signal != 0:
            signal_rows += 1
            signal_scores.append(score)
            if score >= 0.75:
                high_signal_rows += 1
        rows.append(current)

    write_runtime_csv(destination, rows, ("bar_time_server", *extended_feature_order))
    raw_times = list(raw_surface["bar_time_server"].astype(str))
    feature_times = list(feature_frame["bar_time_server"].astype(str))
    runtime_missing_feature_cells = int(pd.DataFrame(rows).loc[:, extended_feature_order].isna().sum().sum()) if rows else 0
    diagnostics: list[dict[str, Any]] = []
    for component in profile.components:
        key = f"{component[0]}:{component[1]}"
        current = thresholds[key]
        diagnostics.append(
            {
                "state_profile": profile.profile_id,
                "state_feature": profile.feature_name,
                "source_component": component[0],
                "transform": component[1],
                "q25": current["q25"],
                "q50": current["q50"],
                "q75": current["q75"],
                "threshold_source": "run267V_raw_surface_candidate_specific_quantiles",
            }
        )

    meta = {
        "source_feature_file": rel(source_feature_path),
        "raw_surface_file": rel(raw_surface_path),
        "runtime_feature_file": rel(destination),
        "runtime_feature_sha256": sha256_file_lf_normalized(destination),
        "rows": int(len(rows)),
        "source_feature_count": len(source_feature_order),
        "extended_feature_count": len(extended_feature_order),
        "source_feature_order": ";".join(source_feature_order),
        "source_feature_order_hash": ordered_hash(source_feature_order),
        "feature_order": ";".join(extended_feature_order),
        "feature_order_hash": ordered_hash(extended_feature_order),
        "state_feature": profile.feature_name,
        "state_feature_index": len(extended_feature_order) - 1,
        "state_score_q50": float(pd.Series(scores, dtype="float64").quantile(0.50)) if scores else 0.0,
        "state_score_q80": float(pd.Series(scores, dtype="float64").quantile(0.80)) if scores else 0.0,
        "state_score_q95": float(pd.Series(scores, dtype="float64").quantile(0.95)) if scores else 0.0,
        "signal_rows": signal_rows,
        "signal_state_score_q80": float(pd.Series(signal_scores, dtype="float64").quantile(0.80)) if signal_scores else 0.0,
        "high_state_signal_rows": high_signal_rows,
        "high_state_signal_ratio": high_signal_rows / signal_rows if signal_rows else 0.0,
        "context_missing_rows": context_missing_rows,
        "bar_time_order_match": raw_times[: len(feature_times)] == feature_times or all(time in raw_by_time for time in feature_times),
        "duplicate_bar_time_rows": int(feature_frame["bar_time_server"].duplicated().sum()),
        "runtime_missing_feature_cells": runtime_missing_feature_cells,
    }
    return meta, diagnostics, feature_frame


def write_state_feature_model(source: Path, destination: Path, state_feature_index: int) -> dict[str, Any]:
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    with io_path(destination).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_MODEL_COLUMNS), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in source_rows:
            writer.writerow({column: row.get(column, "") for column in CSV_MODEL_COLUMNS})
        for index, cut in enumerate(STATE_FEATURE_CUTS):
            writer.writerow(
                {
                    "record_type": "cut",
                    "feature_index": state_feature_index,
                    "item_index": index,
                    "value": f"{cut:.17g}",
                    "score_short": "",
                    "score_flat": "",
                    "score_long": "",
                }
            )
        for index, scores in enumerate(STATE_FEATURE_TERMS):
            writer.writerow(
                {
                    "record_type": "score",
                    "feature_index": state_feature_index,
                    "item_index": index,
                    "value": "",
                    "score_short": f"{scores[0]:.17g}",
                    "score_flat": f"{scores[1]:.17g}",
                    "score_long": f"{scores[2]:.17g}",
                }
            )
    return {
        "source_model_rows": len(source_rows),
        "added_cut_rows": len(STATE_FEATURE_CUTS),
        "added_score_rows": len(STATE_FEATURE_TERMS),
        "runtime_model_file": rel(destination),
        "runtime_model_sha256": sha256_file_lf_normalized(destination),
        "state_feature_cuts": ";".join(f"{value:.2f}" for value in STATE_FEATURE_CUTS),
        "state_feature_terms": ";".join("/".join(f"{score:.3f}" for score in row) for row in STATE_FEATURE_TERMS),
    }


def zero_state_feature_parity_row(
    queue_id: str,
    alias: str,
    source_test_id: str,
    state_profile: str,
    source_model: Path,
    extended_model: Path,
    source_features: pd.DataFrame,
    source_feature_order: Sequence[str],
    extended_feature_order: Sequence[str],
) -> dict[str, Any]:
    rows = min(2048, len(source_features))
    source_matrix = source_features.loc[: rows - 1, list(source_feature_order)].to_numpy(dtype="float64")
    extended_matrix = np.column_stack([source_matrix, np.zeros(rows, dtype="float64")])
    source_table = load_ebm_score_table(source_model, feature_count=len(source_feature_order))
    extended_table = load_ebm_score_table(extended_model, feature_count=len(extended_feature_order))
    source_prob = score_ebm_table_probabilities(source_table, source_matrix)
    extended_prob = score_ebm_table_probabilities(extended_table, extended_matrix)
    max_abs_diff = float(np.max(np.abs(source_prob - extended_prob))) if rows else 0.0
    tolerance = 1.0e-10
    return {
        "queue_id": queue_id,
        "candidate_alias": alias,
        "source_test_id": source_test_id,
        "state_profile": state_profile,
        "passed": max_abs_diff <= tolerance,
        "max_abs_diff": max_abs_diff,
        "tolerance": tolerance,
        "rows": rows,
        "source_feature_count": len(source_feature_order),
        "extended_feature_count": len(extended_feature_order),
        "zero_state_feature_policy": "state_feature_zero_must_equal_source_score_table",
        "table_path": rel(extended_model),
    }


def source_contract_for(
    source_contracts: Mapping[tuple[str, str], Mapping[str, str]],
    alias: str,
    test_id: str,
) -> Mapping[str, str]:
    return source_contracts.get((alias, test_id), {})


def materialization_queue() -> list[dict[str, Any]]:
    q01 = next(
        row for row in read_csv(SOURCE_QUEUE_PATH) if row.get("queue_id") == "run267AO_q01_pool_wide_noncalendar_state_feature_engineering_matrix"
    )
    by_alias = source_variants_by_alias()
    rows: list[dict[str, Any]] = []
    for alias, (candidate_id, role) in CANDIDATE_ROLES.items():
        for profile in STATE_FEATURE_PROFILES:
            source_variant = select_source_variant(alias, profile, by_alias)
            rows.append(
                {
                    "queue_id": f"run267AO_{alias}_{profile.profile_id}",
                    "source_queue_id": q01["queue_id"],
                    "priority": "P0",
                    "candidate_id": candidate_id,
                    "candidate_alias": alias,
                    "candidate_role": role,
                    "state_profile": profile.profile_id,
                    "state_feature": profile.feature_name,
                    "source_test_id": source_variant.get("test_id"),
                    "source_queue_id_run267W": source_variant.get("queue_id"),
                    "source_feature_family": source_variant.get("feature_family"),
                    "component_columns": ";".join(column for column, _transform in profile.components),
                    "component_transforms": ";".join(transform for _column, transform in profile.components),
                    "aggregation": profile.aggregation,
                    "intent": profile.intent,
                    "materialization_status": "ready_for_score_table_materialization",
                    "source_evidence": q01.get("source_evidence"),
                    "success_criteria": q01.get("success_criteria"),
                    "failure_criteria": q01.get("failure_criteria"),
                    "stop_conditions": q01.get("stop_conditions"),
                    "claim_boundary": "materialization_only_no_candidate_selection_no_onnx",
                }
            )
    return rows


def materialize_variant(
    queue_row: Mapping[str, Any],
    source_variant: Mapping[str, str],
    source_contract: Mapping[str, str],
    spec: Any,
    profile: StateFeatureProfile,
    index: int,
) -> dict[str, Any]:
    alias = str(queue_row["candidate_alias"])
    source_test_id = str(queue_row["source_test_id"])
    queue_id = str(queue_row["queue_id"])
    queue_token = safe_token(queue_id, 78)
    local_root = VARIANT_ROOT / alias / queue_token
    feature_path = local_root / "features" / f"{alias}_{safe_token(profile.profile_id, 42)}_state_features.csv"
    model_path = local_root / "models" / f"{alias}_{safe_token(profile.profile_id, 42)}_state_feature_model.csv"

    feature_meta, diagnostics, source_feature_frame = append_state_feature_to_runtime(source_variant, profile, feature_path)
    source_feature_order = str(feature_meta["source_feature_order"]).split(";")
    extended_feature_order = str(feature_meta["feature_order"]).split(";")
    source_model_path = repo_path(str(source_variant["runtime_model_file"]))
    model_meta = write_state_feature_model(source_model_path, model_path, int(feature_meta["state_feature_index"]))
    parity = zero_state_feature_parity_row(
        queue_id,
        alias,
        source_test_id,
        profile.profile_id,
        source_model_path,
        model_path,
        source_feature_frame,
        source_feature_order,
        extended_feature_order,
    )

    common_feature_path = f"{COMMON_ROOT}/{alias}/{queue_token}/features/{feature_path.name}"
    common_model_path = f"{COMMON_ROOT}/{alias}/{queue_token}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    _full_order, _rank_column, gate_column = source_tables.candidate_full_feature_order(spec)
    attempts: list[dict[str, Any]] = []
    for role_index, (tier, attempt_role, prefix, token) in enumerate(
        (
            (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{alias}_{safe_token(profile.profile_id, 28)}", "ta"),
            (input_probe.mt5.TIER_AB, "routed_total_duplicate_boundary", f"mt5_rt_{alias}_{safe_token(profile.profile_id, 28)}", "rt"),
        ),
        start=1,
    ):
        magic = 26734000 + index * 100 + role_index
        payload = attempt_payload(
            run_root=RUN_ROOT,
            run_id=RUN_ID,
            stage_number=267,
            exploration_label=f"stage267_StateFeatureEngineering__{safe_token(profile.profile_id, 32)}",
            attempt_name=f"{queue_token}_{token}_2024",
            tier=tier,
            split=PERIOD_LABEL,
            model_path=common_model_path,
            model_id=f"{RUN_ID}_{alias}_{safe_token(profile.profile_id, 32)}_v1",
            model_backend="ebm_table",
            feature_path=common_feature_path,
            feature_count=len(extended_feature_order),
            feature_order_hash=ordered_hash(extended_feature_order),
            short_threshold=as_float(source_contract.get("short_threshold"), spec.variant.short_threshold),
            long_threshold=as_float(source_contract.get("long_threshold"), spec.variant.long_threshold),
            min_margin=as_float(source_contract.get("min_margin"), 0.0),
            invert_signal=False,
            from_date="2024.01.02",
            to_date="2025.01.01",
            primary_active_tier="tier_a",
            attempt_role=attempt_role,
            record_view_prefix=prefix,
            max_hold_bars=as_int(source_contract.get("max_hold_bars"), spec.variant.max_hold_bars),
            common_root=f"{COMMON_ROOT}/{alias}/{queue_token}",
            fallback_enabled=False,
            close_on_flat_signal=str(source_contract.get("close_on_flat_signal", spec.variant.close_on_flat_signal)).lower() == "true",
            reverse_on_opposite_signal=str(source_contract.get("reverse_on_opposite_signal", spec.variant.reverse_on_opposite_signal)).lower() == "true",
            close_only_on_opposite_signal=str(source_contract.get("close_only_on_opposite_signal", spec.variant.close_only_on_opposite_signal)).lower() == "true",
            extra_set_values=source_tables.extra_set_for_feature_order(spec, extended_feature_order, gate_column, magic),
        )
        payload.update(
            {
                "queue_id": queue_id,
                "candidate_id": queue_row.get("candidate_id"),
                "candidate_alias": alias,
                "candidate_role": queue_row.get("candidate_role"),
                "source_test_id": source_test_id,
                "state_profile": profile.profile_id,
                "state_feature": profile.feature_name,
                "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
                "execution_status": "not_executed",
            }
        )
        attempts.append(payload)

    variant = {
        "queue_id": queue_id,
        "source_queue_id": queue_row.get("source_queue_id"),
        "priority": queue_row.get("priority"),
        "candidate_id": queue_row.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": queue_row.get("candidate_role"),
        "source_test_id": source_test_id,
        "source_run267W_queue_id": queue_row.get("source_queue_id_run267W"),
        "state_profile": profile.profile_id,
        "state_feature": profile.feature_name,
        "component_columns": queue_row.get("component_columns"),
        "aggregation": profile.aggregation,
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "source_runtime_feature_file": feature_meta["source_feature_file"],
        "runtime_feature_file": feature_meta["runtime_feature_file"],
        "runtime_feature_sha256": feature_meta["runtime_feature_sha256"],
        "source_runtime_model_file": rel(source_model_path),
        "runtime_model_file": model_meta["runtime_model_file"],
        "runtime_model_sha256": model_meta["runtime_model_sha256"],
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "source_feature_count": feature_meta["source_feature_count"],
        "feature_count": feature_meta["extended_feature_count"],
        "source_feature_order_hash": feature_meta["source_feature_order_hash"],
        "feature_order": feature_meta["feature_order"],
        "feature_order_hash": feature_meta["feature_order_hash"],
        "state_feature_index": feature_meta["state_feature_index"],
        "state_feature_cuts": model_meta["state_feature_cuts"],
        "state_feature_terms": model_meta["state_feature_terms"],
        "runtime_rows": feature_meta["rows"],
        "signal_rows": feature_meta["signal_rows"],
        "high_state_signal_rows": feature_meta["high_state_signal_rows"],
        "high_state_signal_ratio": feature_meta["high_state_signal_ratio"],
        "state_score_q50": feature_meta["state_score_q50"],
        "state_score_q80": feature_meta["state_score_q80"],
        "state_score_q95": feature_meta["state_score_q95"],
        "zero_state_feature_parity_passed": parity["passed"],
        "zero_state_feature_parity_max_abs_diff": parity["max_abs_diff"],
        "claim_boundary": "materialization_only_no_candidate_selection_no_onnx",
    }
    contract = {
        "queue_id": queue_id,
        "candidate_id": queue_row.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": queue_row.get("candidate_role"),
        "source_test_id": source_test_id,
        "state_profile": profile.profile_id,
        "shared_contract": "US100 M5;2024 historical stress window;RuntimeProbeEA;true_internal_feature_order_plus_pool_wide_state_feature;EBM score table extension;attempt set/ini identity",
        "feature_count": feature_meta["extended_feature_count"],
        "feature_order_hash": feature_meta["feature_order_hash"],
        "model_backend": "ebm_table",
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "short_threshold": as_float(source_contract.get("short_threshold"), spec.variant.short_threshold),
        "long_threshold": as_float(source_contract.get("long_threshold"), spec.variant.long_threshold),
        "min_margin": as_float(source_contract.get("min_margin"), 0.0),
        "max_hold_bars": as_int(source_contract.get("max_hold_bars"), spec.variant.max_hold_bars),
        "state_feature": profile.feature_name,
        "state_feature_index": feature_meta["state_feature_index"],
        "known_difference": "extends run267W true internal score table with one engineered noncalendar state feature; no retraining; no literal weekday/month filter",
        "runtime_claim_boundary": "research_only_execution_pending_no_selected_candidate_no_onnx",
    }
    alignment = {
        "queue_id": queue_id,
        "candidate_alias": alias,
        "source_test_id": source_test_id,
        "state_profile": profile.profile_id,
        "runtime_rows": feature_meta["rows"],
        "bar_time_order_match": feature_meta["bar_time_order_match"],
        "duplicate_bar_time_rows": feature_meta["duplicate_bar_time_rows"],
        "runtime_missing_feature_cells": feature_meta["runtime_missing_feature_cells"],
        "context_missing_rows": feature_meta["context_missing_rows"],
        "alignment_status": "pass"
        if feature_meta["bar_time_order_match"] and not feature_meta["context_missing_rows"] and not feature_meta["runtime_missing_feature_cells"]
        else "invalid",
    }
    if alignment["alignment_status"] != "pass":
        raise RuntimeError(f"surface alignment failed for {queue_id}: {alignment}")
    return {
        "variant": variant,
        "contract": contract,
        "diagnostics": diagnostics,
        "parity": parity,
        "alignment": alignment,
        "attempts": attempts,
        "feature_path": feature_path,
        "model_path": model_path,
    }


def build_receipts(result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    design = [
        {"field": "hypothesis", "value": "pool_wide_noncalendar_state_features_may_reduce_repeated_weekday_month_holes_without_literal_calendar_filter"},
        {"field": "decision_use", "value": "materialize_MT5_attempt_inputs_only_no_candidate_selection"},
        {"field": "comparison_baseline", "value": "run267W true internal score tables plus run267AN repair failure memory"},
        {"field": "control_variables", "value": "same_five_candidate_pool_same_2024_period_same_MT5_cost_boundary_same_thresholds"},
        {"field": "changed_variables", "value": "adds_one_engineered_state_feature_per_profile_return_shock_volatility_regime_range_expansion_trend_disagreement"},
        {"field": "sample_scope", "value": "Tier A separate plus Tier A+B duplicate boundary until real fallback is explicitly enabled"},
        {"field": "success_criteria", "value": "future_run267AP_must_check_trade_count_PF_DD_Monday_December_no_single_feature_dependency"},
        {"field": "failure_criteria", "value": "same_named_weak_slices_remain_or_trade_count_collapses_or_single_candidate_survives_by_threshold_tweak"},
        {"field": "invalid_conditions", "value": "literal_weekday_month_filter_or_feature_order_untracked_or_Tier_A_plus_B_called_real_routing"},
        {"field": "stop_conditions", "value": "if_state_feature_engineering_fails_named_weak_slices_close_branch_and_pivot_to_new_model_family_or_period_design"},
        {"field": "evidence_plan", "value": "state_feature_matrix;variant_manifest;runtime_contract;attempt_manifest;future_MT5_KPI;future_balance_time_slice_trade_quality_review"},
    ]
    integrity = [
        {"field": "data_source", "value": f"{rel(SOURCE_QUEUE_PATH)} and {rel(SOURCE_VARIANT_MANIFEST_PATH)}"},
        {"field": "time_axis", "value": "bar_time_server from run267W runtime feature files aligned to run267V raw surface"},
        {"field": "sample_scope", "value": "US100 M5 2024 historical stress runtime surface"},
        {"field": "missing_or_duplicate_check", "value": f"context_missing_rows={result['context_missing_rows']};surface_alignment_pass={result['surface_alignment_pass_count']}/{result['variant_count']}"},
        {"field": "feature_label_boundary", "value": "state features use raw market feature quantile scaling only; no MT5 PnL is used as a training label"},
        {"field": "split_boundary", "value": "materialization only; execution and review remain pending"},
        {"field": "leakage_risk", "value": "profiles were chosen after weak-slice repair failure, so future MT5 review must treat them as exploratory"},
        {"field": "data_hash_or_identity", "value": f"variant_manifest={rel(VARIANT_MANIFEST_PATH)}"},
        {"field": "integrity_judgment", "value": "usable_with_boundary" if result["surface_alignment_pass_count"] == result["variant_count"] else "inconclusive"},
    ]
    parity = [
        {"field": "runtime_feature_order", "value": "extended_feature_order_hash_recorded_per_variant"},
        {"field": "score_table_extension", "value": "one appended state feature with zero-score first live bin parity check"},
        {"field": "zero_state_feature_parity", "value": f"{result['zero_state_feature_parity_passed_count']}/{result['variant_count']}"},
        {"field": "MT5_execution_status", "value": "not_executed_materialization_only"},
        {"field": "runtime_claim_boundary", "value": "no_runtime_authority_no_ONNX_no_candidate_selection"},
    ]
    judgment = [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"variants={result['variant_count']};attempts={result['attempt_count']};zero_parity={result['zero_state_feature_parity_passed_count']}/{result['variant_count']}",
            "evidence_missing": "MT5_execution;trade_list_review;balance_equity_curve;time_slice_KPI;trade_quality_after_state_feature",
            "judgment_label": JUDGMENT,
            "claim_boundary": "score_table_materialization_only_no_candidate_selection_no_onnx_no_operating_claim",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "쉽게 말하면 기존 후보 5개에 새 상태 피처를 붙여 다음 MT5 실행 대기 입력으로 만든 단계다.",
        }
    ]
    return design, integrity, parity, judgment


def build_materialization() -> dict[str, Any]:
    require_inputs()
    specs = specs_by_alias()
    source_by_alias = source_variants_by_alias()
    source_contracts = source_contracts_by_alias_test()
    queue_rows = materialization_queue()
    profiles = {profile.profile_id: profile for profile in STATE_FEATURE_PROFILES}

    variants: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    alignment_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    dynamic_artifacts: list[dict[str, Any]] = []

    for index, queue_row in enumerate(queue_rows, start=1):
        alias = str(queue_row["candidate_alias"])
        source_test_id = str(queue_row["source_test_id"])
        source_variant = select_source_variant(alias, profiles[str(queue_row["state_profile"])], source_by_alias)
        contract = source_contract_for(source_contracts, alias, source_test_id)
        item = materialize_variant(queue_row, source_variant, contract, specs[alias], profiles[str(queue_row["state_profile"])], index)
        variants.append(item["variant"])
        contracts.append(item["contract"])
        diagnostics.extend(
            dict(row, queue_id=queue_row["queue_id"], candidate_alias=alias, source_test_id=source_test_id) for row in item["diagnostics"]
        )
        parity_rows.append(item["parity"])
        alignment_rows.append(item["alignment"])
        attempts.extend(item["attempts"])
        dynamic_artifacts.extend(
            [
                {
                    "artifact_id": f"stage267_run267AO_{safe_token(str(queue_row['queue_id']), 72)}_runtime_feature",
                    "artifact_type": "runtime_feature_csv",
                    "path": rel(item["feature_path"]),
                    "notes": f"Run267AO runtime feature CSV for {queue_row['queue_id']}.",
                },
                {
                    "artifact_id": f"stage267_run267AO_{safe_token(str(queue_row['queue_id']), 72)}_runtime_model",
                    "artifact_type": "runtime_model_csv",
                    "path": rel(item["model_path"]),
                    "notes": f"Run267AO EBM score table CSV for {queue_row['queue_id']}.",
                },
            ]
        )

    created_at = utc_now()
    result: dict[str, Any] = {
        "created_at_utc": created_at,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_score_table_run_id": SOURCE_SCORE_TABLE_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "candidate_count": len({row["candidate_alias"] for row in variants}),
        "profile_count": len({row["state_profile"] for row in variants}),
        "variant_count": len(variants),
        "attempt_count": len(attempts),
        "zero_state_feature_parity_passed_count": sum(1 for row in parity_rows if row.get("passed") is True or str(row.get("passed")).lower() == "true"),
        "surface_alignment_pass_count": sum(1 for row in alignment_rows if row.get("alignment_status") == "pass"),
        "context_missing_rows": sum(int(row.get("context_missing_rows", 0)) for row in alignment_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable_materialization_only",
        "claim_boundary": CLAIM_BOUNDARY,
        "state_feature_matrix": queue_rows,
        "variant_manifest": variants,
        "runtime_contract": contracts,
        "state_feature_diagnostics": diagnostics,
        "zero_state_feature_parity": parity_rows,
        "surface_alignment": alignment_rows,
        "attempts": attempts,
        "dynamic_artifacts": dynamic_artifacts,
        "inputs": {
            "run267AN_next_experiment_queue": rel(SOURCE_QUEUE_PATH),
            "run267AN_repair_branch_decision": rel(SOURCE_REPAIR_DECISION_PATH),
            "run267AN_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
            "run267W_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
            "run267W_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
            "run267AN_report": rel(SOURCE_DESIGN_REPORT_PATH),
            "run267W_report": rel(SOURCE_SCORE_TABLE_REPORT_PATH),
        },
        "outputs": {
            "state_feature_matrix": rel(STATE_FEATURE_MATRIX_PATH),
            "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "state_feature_diagnostics": rel(STATE_FEATURE_DIAGNOSTICS_PATH),
            "zero_state_feature_parity": rel(PARITY_CHECK_PATH),
            "surface_alignment": rel(SURFACE_ALIGNMENT_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "review_result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "artifact_hashes": {},
    }
    design, integrity, runtime_parity, judgment = build_receipts(result)
    result["experiment_design_receipt"] = design
    result["data_integrity_receipt"] = integrity
    result["runtime_parity_receipt"] = runtime_parity
    result["result_judgment"] = judgment
    return result


def attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "attempt_name": attempt.get("attempt_name"),
                "queue_id": attempt.get("queue_id"),
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "source_test_id": attempt.get("source_test_id"),
                "state_profile": attempt.get("state_profile"),
                "state_feature": attempt.get("state_feature"),
                "tier": attempt.get("tier"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "ini_sha256": attempt.get("ini", {}).get("sha256"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "execution_status": attempt.get("execution_status", "not_executed"),
            }
        )
    return rows


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(
        STATE_FEATURE_MATRIX_PATH,
        result["state_feature_matrix"],
        (
            "queue_id",
            "source_queue_id",
            "priority",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "state_profile",
            "state_feature",
            "source_test_id",
            "source_queue_id_run267W",
            "source_feature_family",
            "component_columns",
            "component_transforms",
            "aggregation",
            "intent",
            "materialization_status",
            "source_evidence",
            "success_criteria",
            "failure_criteria",
            "stop_conditions",
            "claim_boundary",
        ),
    )
    write_csv(MATERIALIZATION_QUEUE_PATH, result["state_feature_matrix"], (
        "queue_id",
        "priority",
        "candidate_alias",
        "state_profile",
        "source_test_id",
        "materialization_status",
        "claim_boundary",
    ))
    write_csv(
        VARIANT_MANIFEST_PATH,
        result["variant_manifest"],
        (
            "queue_id",
            "source_queue_id",
            "priority",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_test_id",
            "source_run267W_queue_id",
            "state_profile",
            "state_feature",
            "component_columns",
            "aggregation",
            "model_materialization_type",
            "source_runtime_feature_file",
            "runtime_feature_file",
            "runtime_feature_sha256",
            "source_runtime_model_file",
            "runtime_model_file",
            "runtime_model_sha256",
            "common_feature_path",
            "common_feature_sha256",
            "common_model_path",
            "common_model_sha256",
            "source_feature_count",
            "feature_count",
            "source_feature_order_hash",
            "feature_order",
            "feature_order_hash",
            "state_feature_index",
            "state_feature_cuts",
            "state_feature_terms",
            "runtime_rows",
            "signal_rows",
            "high_state_signal_rows",
            "high_state_signal_ratio",
            "state_score_q50",
            "state_score_q80",
            "state_score_q95",
            "zero_state_feature_parity_passed",
            "zero_state_feature_parity_max_abs_diff",
            "claim_boundary",
        ),
    )
    write_csv(
        RUNTIME_CONTRACT_PATH,
        result["runtime_contract"],
        (
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_test_id",
            "state_profile",
            "shared_contract",
            "feature_count",
            "feature_order_hash",
            "model_backend",
            "model_materialization_type",
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "state_feature",
            "state_feature_index",
            "known_difference",
            "runtime_claim_boundary",
        ),
    )
    write_csv(
        STATE_FEATURE_DIAGNOSTICS_PATH,
        result["state_feature_diagnostics"],
        ("queue_id", "candidate_alias", "source_test_id", "state_profile", "state_feature", "source_component", "transform", "q25", "q50", "q75", "threshold_source"),
    )
    write_csv(
        PARITY_CHECK_PATH,
        result["zero_state_feature_parity"],
        (
            "queue_id",
            "candidate_alias",
            "source_test_id",
            "state_profile",
            "passed",
            "max_abs_diff",
            "tolerance",
            "rows",
            "source_feature_count",
            "extended_feature_count",
            "zero_state_feature_policy",
            "table_path",
        ),
    )
    write_csv(
        SURFACE_ALIGNMENT_PATH,
        result["surface_alignment"],
        ("queue_id", "candidate_alias", "source_test_id", "state_profile", "runtime_rows", "bar_time_order_match", "duplicate_bar_time_rows", "runtime_missing_feature_cells", "context_missing_rows", "alignment_status"),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        attempt_rows(result["attempts"]),
        (
            "attempt_name",
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_test_id",
            "state_profile",
            "state_feature",
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
        ),
    )
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], ("field", "value"))
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"], ("field", "value"))
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"], ("field", "value"))
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"], ("result_subject", "evidence_available", "evidence_missing", "judgment_label", "claim_boundary", "next_condition", "user_explanation_hook"))

    run_manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_score_table_run_id": SOURCE_SCORE_TABLE_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "variant_manifest": rel(VARIANT_MANIFEST_PATH),
        "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
        "attempts": result["attempts"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST_PATH, run_manifest)
    lineage = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_score_table_run_id": SOURCE_SCORE_TABLE_RUN_ID,
        "source_inputs": result["inputs"],
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": result["outputs"],
        "registry_links": {
            "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
            "run_registry": rel(RUN_REGISTRY_PATH),
            "alpha_run_ledger": rel(PROJECT_LEDGER_PATH),
            "stage_run_ledger": rel(STAGE_LEDGER_PATH),
        },
        "availability": "tracked_generated_with_manifest_and_common_file_copies",
        "lineage_judgment": "connected_with_boundary",
        "boundary": CLAIM_BOUNDARY,
    }
    write_json(LINEAGE_PATH, lineage)

    artifact_hashes = {
        "state_feature_matrix": sha256_file_lf_normalized(STATE_FEATURE_MATRIX_PATH),
        "materialization_queue": sha256_file_lf_normalized(MATERIALIZATION_QUEUE_PATH),
        "variant_manifest": sha256_file_lf_normalized(VARIANT_MANIFEST_PATH),
        "runtime_contract": sha256_file_lf_normalized(RUNTIME_CONTRACT_PATH),
        "state_feature_diagnostics": sha256_file_lf_normalized(STATE_FEATURE_DIAGNOSTICS_PATH),
        "zero_state_feature_parity": sha256_file_lf_normalized(PARITY_CHECK_PATH),
        "surface_alignment": sha256_file_lf_normalized(SURFACE_ALIGNMENT_PATH),
        "experiment_design_receipt": sha256_file_lf_normalized(EXPERIMENT_DESIGN_RECEIPT_PATH),
        "data_integrity_receipt": sha256_file_lf_normalized(DATA_INTEGRITY_RECEIPT_PATH),
        "runtime_parity_receipt": sha256_file_lf_normalized(RUNTIME_PARITY_RECEIPT_PATH),
        "result_judgment": sha256_file_lf_normalized(RESULT_JUDGMENT_PATH),
        "attempt_manifest": sha256_file_lf_normalized(ATTEMPT_MANIFEST_PATH),
        "run_manifest": sha256_file_lf_normalized(RUN_MANIFEST_PATH),
        "lineage": sha256_file_lf_normalized(LINEAGE_PATH),
    }
    result_with_hashes = dict(result)
    result_with_hashes["artifact_hashes"] = artifact_hashes
    write_json(RESULT_PATH, result_with_hashes)
    write_md(REPORT_PATH, report_markdown(result_with_hashes))


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267AO Pool-wide State Feature Engineering Materialization(267단계 267AO 후보군 전체 상태 피처 엔지니어링 물질화)",
        "",
        "- action(행동): run267AN(267AN 실행)의 수리 실패 기억을 후보군 전체 state feature engineering(상태 피처 엔지니어링) score table(점수표) 입력으로 물질화했다.",
        "- effect(효과): 같은 s264_aia repair(수리)를 반복하지 않고, 다섯 Baseline candidates(기준 후보)를 네 개 비달력 상태 피처 축에서 다음 MT5(MetaTrader 5, 메타트레이더5) 실행으로 넘길 수 있다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267AM(267AM 실행)에서 Monday(월요일)와 2024-12(2024년 12월) 구멍이 남았다.",
        "run267AN(267AN 실행)은 같은 repair(수리)를 더 하지 말고, 후보군 전체에 적용할 market state feature(시장 상태 피처)를 만들라고 정리했다.",
        "run267AO(267AO 실행)는 그 지시를 실제 feature/model/set/ini(피처/모델/설정/초기화) 파일로 바꿨다.",
        "Effect(효과): 다음 run267AP(267AP 실행)에서 누가 덜 깨지는지 MT5(MetaTrader 5, 메타트레이더5)로 볼 수 있다.",
        "",
        "## Materialization Summary(물질화 요약)",
        "",
        f"- candidates(후보): `{result['candidate_count']}`",
        f"- state_profiles(상태 프로필): `{result['profile_count']}`",
        f"- variants(변형): `{result['variant_count']}`",
        f"- attempts queued(대기 시도): `{result['attempt_count']}`",
        f"- zero_state_feature_parity passed(제로 상태 피처 동등성 통과): `{result['zero_state_feature_parity_passed_count']}/{result['variant_count']}`",
        f"- surface_alignment passed(표면 정렬 통과): `{result['surface_alignment_pass_count']}/{result['variant_count']}`",
        f"- context_missing_rows(문맥 누락 행): `{result['context_missing_rows']}`",
        "",
        "## State Axes(상태 축)",
        "",
        "- return_shock_absorption(수익률 충격 흡수): return_zscore/ATR-normalized return(수익률 z점수/ATR 정규화 수익률) 계열이다.",
        "- volatility_regime_expansion(변동성 국면 확장): ATR ratio/historical volatility/bollinger width(ATR 비율/역사 변동성/볼린저 폭) 계열이다.",
        "- range_expansion_pressure(범위 확장 압박): high-low range/gap/close-open shape(고저 범위/갭/시종가 형태) 계열이다.",
        "- trend_strength_disagreement(추세 강도 불일치): ADX/DI/vortex/MA spread(ADX/DI/보텍스/이동평균 차이) 계열이다.",
        "",
        "## Boundary(경계)",
        "",
        "- MT5 execution(MT5 실행): `not_executed`",
        "- trading KPI(거래 핵심 성과 지표): `not_claimed`",
        "- balance/equity curve(잔액/평가금 곡선): `pending_MT5`",
        "- candidate selection(후보 선택): `none`",
        "- ONNX(ONNX): `not_reviewed`",
        "",
        "## Outputs(산출물)",
        "",
        f"- state_feature_matrix(상태 피처 행렬): `{rel(STATE_FEATURE_MATRIX_PATH)}`",
        f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
        f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
        f"- state_feature_diagnostics(상태 피처 진단): `{rel(STATE_FEATURE_DIAGNOSTICS_PATH)}`",
        f"- zero_state_feature_parity(제로 상태 피처 동등성): `{rel(PARITY_CHECK_PATH)}`",
        f"- surface_alignment(표면 정렬): `{rel(SURFACE_ALIGNMENT_PATH)}`",
        f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
        "",
        "## Next Action(다음 행동)",
        "",
        f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        "- effect(효과): 40개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 실행해 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 확인한다.",
        "",
    ]
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    static = [
        ("stage267_run267AO_materialization_script", "producer_script", PRODUCER_PATH, "Builds run267AO pool-wide state feature engineering inputs."),
        ("stage267_run267AO_state_feature_matrix", "state_feature_matrix", STATE_FEATURE_MATRIX_PATH, "Run267AO state feature engineering matrix."),
        ("stage267_run267AO_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267AO materialization queue."),
        ("stage267_run267AO_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Run267AO state feature variant manifest."),
        ("stage267_run267AO_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267AO runtime contract."),
        ("stage267_run267AO_state_feature_diagnostics", "state_feature_diagnostics", STATE_FEATURE_DIAGNOSTICS_PATH, "Run267AO state feature diagnostics."),
        ("stage267_run267AO_zero_parity", "zero_state_feature_parity_check", PARITY_CHECK_PATH, "Run267AO zero state feature parity check."),
        ("stage267_run267AO_surface_alignment", "surface_alignment_check", SURFACE_ALIGNMENT_PATH, "Run267AO surface alignment check."),
        ("stage267_run267AO_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267AO experiment design receipt."),
        ("stage267_run267AO_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267AO data integrity receipt."),
        ("stage267_run267AO_runtime_parity_receipt", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Run267AO runtime parity receipt."),
        ("stage267_run267AO_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267AO result judgment."),
        ("stage267_run267AO_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267AO MT5 attempt manifest."),
        ("stage267_run267AO_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267AO run manifest."),
        ("stage267_run267AO_lineage", "lineage", LINEAGE_PATH, "Run267AO lineage."),
        ("stage267_run267AO_review_result", "review_result_json", RESULT_PATH, "Run267AO review result JSON."),
        ("stage267_run267AO_report", "review_report", REPORT_PATH, "Run267AO review report."),
    ]
    rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in static
    ]
    for item in result["dynamic_artifacts"]:
        path = repo_path(str(item["path"]))
        rows.append(
            {
                "artifact_id": item["artifact_id"],
                "artifact_type": item["artifact_type"],
                "path": item["path"],
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": item["notes"],
            }
        )
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    created_at = str(result["created_at_utc"])
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "pool_wide_state_feature_engineering_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RUN_ROOT),
        "notes": (
            f"variants={result['variant_count']};attempts={result['attempt_count']};"
            f"zero_parity={result['zero_state_feature_parity_passed_count']}/{result['variant_count']};"
            f"selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;next_action={NEXT_ACTION}."
        ),
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__pool_wide_state_feature_engineering_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pool_wide_state_feature_engineering_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "pool_wide_state_feature_engineering_materialization",
        "tier_scope": "Tier A and Tier A+B 2024 historical runtime attempts planned; Tier A+B duplicate boundary until fallback enabled",
        "kpi_scope": "materialization_no_mt5_kpi",
        "scoreboard_lane": "experiment_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={result['variant_count']};attempts={result['attempt_count']};zero_parity={result['zero_state_feature_parity_passed_count']}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;mt5_execution=not_executed",
        "external_verification_status": "not_applicable_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    stage_row = {
        "row_id": "stage267_run267AO_pool_wide_state_feature_engineering_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "pool_wide_state_feature_engineering_materialization",
        "tier_scope": "Tier A and Tier A+B historical 2024 state feature attempts planned",
        "scoreboard": "feature_model_set_ini_manifest",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "score_table_materialization_only_no_mt5_kpi_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"variants={result['variant_count']};attempts={result['attempt_count']};next_action={NEXT_ACTION}.",
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at, result), key="artifact_id")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def update_docs() -> None:
    report_line = f"- run267AO_pool_wide_state_feature_engineering_materialization(267AO 후보군 전체 상태 피처 엔지니어링 물질화): `{rel(REPORT_PATH)}`"

    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_state_feature_engineering_materialization`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = append_after_contains(current, "run267AN_noncalendar_state_guard_repair_followup_or_prune_design", report_line)
    current = current.replace(
        "- next_run(다음 실행): `run267AO_materialize_pool_wide_state_feature_engineering_queue`",
        f"- next_run(다음 실행): `{NEXT_ACTION}`",
    )
    current = current.replace(
        "- next_action(다음 행동): `run267AO_materialize_pool_wide_state_feature_engineering_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    current = append_block_once(
        current,
        "Run267AO(267AO 실행)는 run267AN",
        "\n".join(
            [
                "Run267AO(267AO 실행)는 run267AN(267AN 실행)의 pool-wide state feature engineering queue(후보군 전체 상태 피처 엔지니어링 큐)를 물질화했다.",
                "Effect(효과): 다섯 Baseline candidates(기준 후보)에 네 개 비달력 상태 피처 축을 붙인 20개 variant(변형)와 40개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 만들었고, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 없다.",
            ]
        ),
    )
    write_text(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = append_after_contains(selection, "run267AN_noncalendar_state_guard_repair_followup_or_prune_design", report_line)
    selection = selection.replace(
        "- next_action(다음 행동): `run267AO_materialize_pool_wide_state_feature_engineering_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    selection = append_block_once(
        selection,
        "Run267AO(267AO 실행)는 pool-wide state feature engineering",
        "\n".join(
            [
                "Run267AO(267AO 실행)는 pool-wide state feature engineering materialization(후보군 전체 상태 피처 엔지니어링 물질화)을 완료했다.",
                "Effect(효과): 다음 run267AP(267AP 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 실제 거래/곡선/시간구간 영향을 확인한다. 선택 후보(selected candidate, 선택 후보)는 없다.",
            ]
        ),
    )
    write_text(SELECTION_STATUS_PATH, selection)

    review = read_text(REVIEW_INDEX_PATH)
    review = replace_line_prefix(review, "- status(상태):", f"- status(상태): `{STATUS}`")
    review = replace_line_prefix(review, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review = replace_line_prefix(review, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review = append_after_contains(review, "run267AN_noncalendar_state_guard_repair_followup_or_prune_design", report_line)
    review = review.replace(
        "- next_action(다음 행동): `run267AO_materialize_pool_wide_state_feature_engineering_queue`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    write_text(REVIEW_INDEX_PATH, review)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus_block = (
        "- >-\n"
        f"  Stage267(267단계) run267AO(267AO 실행) pool-wide state feature engineering materialization(후보군 전체 상태 피처 엔지니어링 물질화) `{STATUS}`. "
        "Effect(효과): run267AN(267AN 실행)의 실패 기억을 후보 5개 x 상태 피처 4개 = 20개 score table/model(점수표/모델)과 40개 MT5(MetaTrader 5, 메타트레이더5) 시도 입력으로 만들었고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus_block)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = append_after_contains(
        workspace,
        "run267AN",
        f"  run267AO_pool_wide_state_feature_engineering_materialization_report_path: {rel(REPORT_PATH)}",
    )
    write_text(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    result = build_materialization()
    write_outputs(result)
    final_result = json.loads(io_path(RESULT_PATH).read_text(encoding="utf-8"))
    update_ledgers(final_result)
    update_docs()
    print(
        json.dumps(
            {
                "status": STATUS,
                "candidate_count": final_result["candidate_count"],
                "profile_count": final_result["profile_count"],
                "variant_count": final_result["variant_count"],
                "attempt_count": final_result["attempt_count"],
                "zero_state_feature_parity_passed_count": final_result["zero_state_feature_parity_passed_count"],
                "surface_alignment_pass_count": final_result["surface_alignment_pass_count"],
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
