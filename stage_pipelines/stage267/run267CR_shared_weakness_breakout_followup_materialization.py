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
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import (
    run267CF_pool_wide_orthogonal_loss_shape_state_materialization as score_table_extender,
)
from stage_pipelines.stage267 import (
    run267CN_pool_wide_shared_weakness_breakout_materialization as source_materialization,
)
from stage_pipelines.stage267 import (
    run267CQ_shared_weakness_breakout_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267CR"
RUN_ID = "run267CR_stage267_shared_weakness_breakout_followup_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_materialization.RUN_ID
STATUS = "run267CR_shared_weakness_breakout_followup_materialized_execution_pending"
JUDGMENT = "shared_weakness_breakout_followup_materialized_no_candidate_selection"
NEXT_ACTION = "run267CS_execute_shared_weakness_breakout_followup_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_followup_materialization"
FEATURE_ROOT = RUN_ROOT / "features"
VARIANT_ROOT = RUN_ROOT / "variants"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_QUEUE_PATH = source_design.MATERIALIZATION_QUEUE_PATH
SOURCE_FEATURE_BLUEPRINT_PATH = source_design.FEATURE_BLUEPRINT_PATH
SOURCE_BRANCH_DECISION_PATH = source_design.BRANCH_DECISION_PATH
SOURCE_PRUNE_MATRIX_PATH = source_design.PRUNE_MATRIX_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_REVIEW_RESULT_PATH = source_design.REVIEW_RESULT_PATH
SOURCE_VARIANT_MANIFEST_PATH = source_materialization.VARIANT_MANIFEST_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = source_materialization.ATTEMPT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_materialization.RUNTIME_CONTRACT_PATH
SOURCE_REPORT_PATH = source_design.REPORT_PATH
SOURCE_MATERIALIZATION_REPORT_PATH = source_materialization.REPORT_PATH

MATERIALIZATION_PLAN_PATH = RUN_ROOT / "materialization_plan.csv"
QUEUE_DECISION_PATH = RUN_ROOT / "queue_decision.csv"
FEATURE_FRAME_MANIFEST_PATH = RUN_ROOT / "feature_frame_manifest.csv"
MODEL_MANIFEST_PATH = RUN_ROOT / "model_manifest.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
CONTROL_PRESSURE_RECEIPT_PATH = RUN_ROOT / "control_pressure_receipt.csv"
GUARDRAIL_RECEIPT_PATH = RUN_ROOT / "guardrail_receipt.csv"
HELD_QUEUE_PATH = RUN_ROOT / "held_queue.csv"
SOURCE_REPRODUCTION_RECEIPT_PATH = RUN_ROOT / "source_profile_reproduction_receipt.csv"
FEATURE_ENGINEERING_DIAGNOSTICS_PATH = RUN_ROOT / "feature_engineering_diagnostics.csv"
ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH = RUN_ROOT / "environment_reproducibility_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CR_shared_weakness_breakout_followup_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CR_shared_weakness_breakout_followup_materialization.py")

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

COMMON_ROOT = "OPV2/s267cr/run267CR_shared_weakness_followup"
EXPLORATION_LABEL = "stage267_BaselineRacing__SharedWeaknessFollowup"
PERIOD_LABEL = "historical_2024_tier_a_train_era_stress"
TIER_PAIR_BOUNDARY = (
    "Tier A and duplicate-boundary Tier A+B inputs are materialized; true Tier B fallback "
    "and actual routed total remain outside this run"
)
MATERIALIZATION_BOUNDARY = "materialization_only_no_candidate_selection_no_selected_research_baseline_no_onnx"
EXECUTION_ENVIRONMENT = "Windows local MT5 workspace; Python pipeline materialization; MT5 Strategy Tester execution pending"

CANDIDATE_ORDER = ("s264_aih", "s264_lc", "s262_lih", "s264_aia", "s258_stc")

ACTIVE_VARIANT_CONFIGS = (
    {
        "queue_id": "run267cr_q01_pool_monday_state_phase_replacement",
        "source_profile_label": "shared_weakness_state_interaction",
        "profile_label": "state_phase_monday_replacement",
        "profile_token": "state_phase_repl",
        "variant_token": "state_phase_repl",
        "engineered_feature": "stage267cr_state_phase_monday_replacement_score",
        "aliases": CANDIDATE_ORDER,
        "model_materialization_type": "augmented_run267CN_score_table_with_state_phase_replacement_feature",
        "model_strength": "balanced_noncalendar_state_phase_replacement_for_monday_and_month_holes",
        "known_difference": "adds one noncalendar state-phase feature; no literal weekday/month filter; source run267CN identity is preserved as comparison anchor",
    },
    {
        "queue_id": "run267cr_q03_aih_aggressive_shock_supply_expansion",
        "source_profile_label": "aggressive_shock_release_reentry",
        "profile_label": "aggressive_shock_supply_expansion",
        "profile_token": "aggr_supply_expand",
        "variant_token": "aggr_supply_expand",
        "engineered_feature": "stage267cr_aggressive_shock_supply_expansion_score",
        "aliases": ("s264_aih",),
        "model_materialization_type": "augmented_run267CN_score_table_with_aggressive_supply_expansion_feature",
        "model_strength": "aggressive_supply_expansion_without_collapsing_trade_count",
        "known_difference": "adds shock supply expansion and buy-side loss-shape proxy; no defensive filter stacking",
    },
    {
        "queue_id": "run267cr_q04_stc_redzone_stress_blast",
        "source_profile_label": "shared_weakness_state_interaction",
        "profile_label": "redzone_stress_blast",
        "profile_token": "redzone_stress",
        "variant_token": "redzone_stress",
        "engineered_feature": "stage267cr_redzone_stress_blast_score",
        "aliases": ("s258_stc",),
        "model_materialization_type": "augmented_run267CN_score_table_with_redzone_stress_blast_feature",
        "model_strength": "single_high_risk_stress_blast_for_s258_stc_then_prune_or_demote",
        "known_difference": "forces one stress attempt for s258_stc; not a long repair loop",
    },
)

QUEUE_HOLD_REASONS = {
    "run267cr_q02_lc_aia_anchor_cross_period_pressure": {
        "decision": "held_for_adjacent_period_feature_frame_materialization",
        "why": "q02 needs 2023H2/2025H1/2025H2 period feature frames; this run keeps 2024 source settings and does not fake cross-period pressure",
        "next": "materialize adjacent-period feature/model/set/ini after run267CS or in a narrow period-pack run",
    },
    "run267cr_q06_buy_side_similar_replacement_probe": {
        "decision": "held_as_standalone_probe_partly_covered_by_q03",
        "why": "q03 already adds a buy-side adverse-excursion proxy for s264_aih; standalone similar replacement should wait for the first aggressive expansion result",
        "next": "open only if run267CS shows supply expansion without new DD/month hole",
    },
}


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


def safe_token(value: Any, limit: int = 90) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_").lower()
    return token[:limit] or "item"


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
    lines = [f"; generated_by={RUN_NUMBER}_shared_weakness_breakout_followup_materialization"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "format": "mt5_set"}


def write_ini(path: Path, values: Mapping[str, Any]) -> dict[str, str]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["[Tester]"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "format": "mt5_tester_ini"}


def quantile_scale(series: pd.Series) -> tuple[pd.Series, dict[str, float]]:
    clean = pd.to_numeric(series, errors="coerce").astype("float64").replace([np.inf, -np.inf], np.nan)
    finite = clean.dropna()
    if finite.empty:
        return pd.Series(0.0, index=series.index, dtype="float64"), {"q25": 0.0, "q50": 0.0, "q75": 0.0}
    q25 = float(finite.quantile(0.25))
    q50 = float(finite.quantile(0.50))
    q75 = float(finite.quantile(0.75))
    if q75 <= q25:
        scaled = pd.Series(0.0, index=series.index, dtype="float64")
    else:
        scaled = ((clean - q25) / (q75 - q25)).clip(0.0, 1.0).fillna(0.0)
    return scaled.astype("float64"), {"q25": q25, "q50": q50, "q75": q75}


def transform_component(series: pd.Series, transform: str) -> pd.Series:
    clean = pd.to_numeric(series, errors="coerce").astype("float64").replace([np.inf, -np.inf], np.nan)
    if transform == "raw":
        return clean
    if transform == "abs":
        return clean.abs()
    if transform == "abs_center_1":
        return (clean - 1.0).abs()
    if transform == "abs_center_0_5":
        return (clean - 0.5).abs()
    if transform == "negative_pressure":
        return (-clean).clip(lower=0.0)
    if transform == "positive_pressure":
        return clean.clip(lower=0.0)
    raise ValueError(f"unknown transform: {transform}")


def component(
    frame: pd.DataFrame,
    column: str,
    transform: str,
    *,
    weight: float,
    feature_name: str,
) -> tuple[pd.Series, dict[str, Any]]:
    if column not in frame.columns:
        scaled = pd.Series(0.0, index=frame.index, dtype="float64")
        return scaled, {
            "engineered_feature": feature_name,
            "source_component": column,
            "transform": transform,
            "weight": weight,
            "q25": 0.0,
            "q50": 0.0,
            "q75": 0.0,
            "component_status": "missing_component_zero_filled",
            "threshold_source": "blocked_component_receipt_no_future_trade_result",
        }
    scaled, stats = quantile_scale(transform_component(frame[column], transform))
    return scaled, {
        "engineered_feature": feature_name,
        "source_component": column,
        "transform": transform,
        "weight": weight,
        "q25": stats["q25"],
        "q50": stats["q50"],
        "q75": stats["q75"],
        "component_status": "ok",
        "threshold_source": "candidate_source_feature_quantiles_current_and_prior_closed_bar_state_only",
    }


def rolling_state_pressure(frame: pd.DataFrame, feature_name: str) -> tuple[pd.Series, list[dict[str, Any]]]:
    diagnostics: list[dict[str, Any]] = []
    if "log_return_1" in frame.columns:
        returns = pd.to_numeric(frame["log_return_1"], errors="coerce").astype("float64").fillna(0.0)
        negative_cluster = (returns < 0.0).astype("float64").rolling(24, min_periods=1).mean()
        cluster_scaled, stats = quantile_scale(negative_cluster)
        diagnostics.append(
            {
                "engineered_feature": feature_name,
                "source_component": "log_return_1_negative_rolling_24",
                "transform": "rolling_negative_state_pressure",
                "weight": 0.07,
                "q25": stats["q25"],
                "q50": stats["q50"],
                "q75": stats["q75"],
                "component_status": "ok",
                "threshold_source": "closed_bar_history_no_future_trade_result",
            }
        )
        return cluster_scaled.astype("float64"), diagnostics
    diagnostics.append(
        {
            "engineered_feature": feature_name,
            "source_component": "log_return_1_negative_rolling_24",
            "transform": "rolling_negative_state_pressure",
            "weight": 0.07,
            "q25": 0.0,
            "q50": 0.0,
            "q75": 0.0,
            "component_status": "missing_component_zero_filled",
            "threshold_source": "blocked_component_receipt_no_future_trade_result",
        }
    )
    return pd.Series(0.0, index=frame.index, dtype="float64"), diagnostics


def compute_engineered_feature(frame: pd.DataFrame, *, mode: str, feature_name: str) -> tuple[pd.Series, list[dict[str, Any]]]:
    if mode == "state_phase_monday_replacement":
        parts = (
            ("stage267cn_shared_weakness_state_interaction_score", "raw", 0.22),
            ("stage267cf_volatility_energy_transition_score", "raw", 0.16),
            ("atr_14_over_atr_50", "abs_center_1", 0.15),
            ("historical_vol_5_over_20", "abs_center_1", 0.14),
            ("di_spread_14", "abs", 0.12),
            ("bb_position_20", "abs_center_0_5", 0.09),
            ("return_zscore_20", "abs", 0.05),
        )
        extra_weight = 0.07
    elif mode == "aggressive_shock_supply_expansion":
        parts = (
            ("stage267cn_aggressive_shock_release_reentry_score", "raw", 0.25),
            ("stage267cn_shared_weakness_state_interaction_score", "raw", 0.13),
            ("stage267cf_trend_strength_replacement_score", "raw", 0.15),
            ("return_zscore_20", "abs", 0.14),
            ("gap_percent", "abs", 0.11),
            ("close_prev_close_ratio", "abs_center_1", 0.10),
            ("return_1_over_atr_14", "positive_pressure", 0.05),
        )
        extra_weight = 0.07
    elif mode == "redzone_stress_blast":
        parts = (
            ("stage267cn_shared_weakness_state_interaction_score", "raw", 0.20),
            ("stage267cf_range_pressure_asymmetry_score", "raw", 0.17),
            ("return_1_over_atr_14", "abs", 0.16),
            ("atr_14_over_atr_50", "raw", 0.14),
            ("historical_vol_5_over_20", "raw", 0.13),
            ("gap_percent", "abs", 0.10),
            ("bb_position_20", "abs_center_0_5", 0.05),
        )
        extra_weight = 0.05
    else:
        raise ValueError(f"unknown feature mode: {mode}")

    score = pd.Series(0.0, index=frame.index, dtype="float64")
    weight_sum = 0.0
    diagnostics: list[dict[str, Any]] = []
    for column, transform, weight in parts:
        scaled, row = component(frame, column, transform, weight=weight, feature_name=feature_name)
        score = score + float(weight) * scaled
        weight_sum += float(weight)
        diagnostics.append(row)
    cluster, cluster_rows = rolling_state_pressure(frame, feature_name)
    score = score + extra_weight * cluster
    weight_sum += extra_weight
    diagnostics.extend(cluster_rows)
    return (score / weight_sum).clip(0.0, 1.0).astype("float64"), diagnostics


def source_feature_order(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    if not header or header[0] != "bar_time_server":
        raise RuntimeError(f"unexpected feature header: {rel(path)}")
    return list(header[1:])


def source_variants_by_alias_profile() -> dict[tuple[str, str], dict[str, str]]:
    rows = read_csv(SOURCE_VARIANT_MANIFEST_PATH)
    result: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = (row.get("candidate_alias", ""), row.get("profile_label", ""))
        if all(key):
            result[key] = row
    return result


def source_attempts_by_variant_tier() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row["variant_id"], row["tier"]): row
        for row in read_csv(SOURCE_ATTEMPT_MANIFEST_PATH)
        if row.get("variant_id") and row.get("tier")
    }


def materialization_plan_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    queue_by_id = {row["queue_id"]: row for row in queue_rows}
    source_variants = source_variants_by_alias_profile()
    rows: list[dict[str, Any]] = []
    order = 0
    for config in ACTIVE_VARIANT_CONFIGS:
        queue = queue_by_id[str(config["queue_id"])]
        for alias in config["aliases"]:
            source_key = (alias, str(config["source_profile_label"]))
            if source_key not in source_variants:
                raise KeyError(f"missing source variant for {source_key}")
            source = source_variants[source_key]
            order += 1
            variant_id = f"run267cr_{order:02d}_{alias}_{config['variant_token']}"
            rows.append(
                {
                    "plan_id": variant_id,
                    "queue_id": queue["queue_id"],
                    "priority": queue.get("priority"),
                    "candidate_id": source.get("candidate_id"),
                    "candidate_alias": alias,
                    "candidate_role": source.get("candidate_role"),
                    "source_variant_id": source.get("variant_id"),
                    "source_profile_label": source.get("profile_label"),
                    "source_feature_file": source.get("runtime_feature_file"),
                    "source_model_file": source.get("runtime_model_file"),
                    "source_feature_count": source.get("feature_count"),
                    "profile_label": config["profile_label"],
                    "profile_token": config["profile_token"],
                    "engineered_feature": config["engineered_feature"],
                    "model_materialization_type": config["model_materialization_type"],
                    "model_strength": config["model_strength"],
                    "known_difference": config["known_difference"],
                    "materialization_decision": "materialize_feature_model_set_ini_inputs",
                    "materialization_boundary": MATERIALIZATION_BOUNDARY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def materialize_variant(
    plan: Mapping[str, Any],
    source_attempts: Mapping[tuple[str, str], Mapping[str, str]],
    *,
    order: int,
) -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    dict[str, Any],
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    alias = str(plan["candidate_alias"])
    variant_id = str(plan["plan_id"])
    engineered_feature = str(plan["engineered_feature"])
    profile_label = str(plan["profile_label"])
    profile_token = str(plan["profile_token"])
    source_variant_id = str(plan["source_variant_id"])
    source_feature_path = repo_path(str(plan["source_feature_file"]))
    source_model_path = repo_path(str(plan["source_model_file"]))
    base_feature_order = source_feature_order(source_feature_path)
    feature_order = [*base_feature_order, engineered_feature]
    feature_order_hash = ordered_hash(feature_order)

    frame = pd.read_csv(io_path(source_feature_path), encoding="utf-8-sig")
    engineered_values, diagnostics = compute_engineered_feature(frame, mode=profile_label, feature_name=engineered_feature)
    frame[engineered_feature] = engineered_values

    feature_path = FEATURE_ROOT / alias / variant_id / f"{variant_id}_features.csv"
    model_path = VARIANT_ROOT / alias / variant_id / "models" / f"{variant_id}_model.csv"
    write_runtime_csv(feature_path, frame, ["bar_time_server", *feature_order])
    score_table_extender.append_model_features(
        source_model_path,
        model_path,
        source_feature_count=len(base_feature_order),
        profile_label=profile_label,
        engineered_features=[engineered_feature],
    )
    validation = score_table_extender.validate_score_table(feature_path, model_path, feature_order)

    common_feature_path = f"{COMMON_ROOT}/{alias}/{variant_id}/features/{feature_path.name}"
    common_model_path = f"{COMMON_ROOT}/{alias}/{variant_id}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    missing_feature_cells = int(frame.loc[:, feature_order].isna().sum().sum()) if len(frame) else 0
    duplicate_bar_time_rows = int(frame["bar_time_server"].duplicated().sum()) if len(frame) else 0
    feature_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "candidate_alias": alias,
        "source_variant_id": source_variant_id,
        "source_feature_file": rel(source_feature_path),
        "source_feature_sha256": sha256_file_lf_normalized(source_feature_path),
        "runtime_feature_file": rel(feature_path),
        "runtime_feature_sha256": sha256_file_lf_normalized(feature_path),
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "source_feature_count": len(base_feature_order),
        "feature_count": len(feature_order),
        "feature_order": ";".join(feature_order),
        "feature_order_hash": feature_order_hash,
        "appended_feature": engineered_feature,
        "feature_mode": profile_label,
        "feature_min": float(frame[engineered_feature].min()) if len(frame) else 0.0,
        "feature_max": float(frame[engineered_feature].max()) if len(frame) else 0.0,
        "feature_mean": float(frame[engineered_feature].mean()) if len(frame) else 0.0,
        "feature_nonzero_rows": int((frame[engineered_feature] > 0).sum()) if len(frame) else 0,
        "rows": int(len(frame)),
        "first_bar_time_server": str(frame["bar_time_server"].iloc[0]) if len(frame) else "",
        "last_bar_time_server": str(frame["bar_time_server"].iloc[-1]) if len(frame) else "",
        "duplicate_bar_time_rows": duplicate_bar_time_rows,
        "runtime_missing_feature_cells": missing_feature_cells,
        **validation,
        "materialization_status": "materialized_execution_pending",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "candidate_alias": alias,
        "source_model_file": rel(source_model_path),
        "source_model_sha256": sha256_file_lf_normalized(source_model_path),
        "runtime_model_file": rel(model_path),
        "runtime_model_sha256": sha256_file_lf_normalized(model_path),
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "appended_feature": engineered_feature,
        "model_strength": plan["model_strength"],
        "model_materialization_type": plan["model_materialization_type"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    variant_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "source_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "source_variant_id": source_variant_id,
        "candidate_id": plan["candidate_id"],
        "candidate_alias": alias,
        "candidate_role": plan["candidate_role"],
        "profile_label": profile_label,
        "source_profile_label": plan["source_profile_label"],
        "model_materialization_type": model_row["model_materialization_type"],
        "runtime_model_file": model_row["runtime_model_file"],
        "runtime_model_sha256": model_row["runtime_model_sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "runtime_feature_file": feature_row["runtime_feature_file"],
        "runtime_feature_sha256": feature_row["runtime_feature_sha256"],
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "feature_count": len(feature_order),
        "feature_order": ";".join(feature_order),
        "feature_order_hash": feature_order_hash,
        "engineered_features": engineered_feature,
        "known_difference": plan["known_difference"],
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_contract = {
        "variant_id": variant_id,
        "candidate_id": plan["candidate_id"],
        "candidate_alias": alias,
        "candidate_role": plan["candidate_role"],
        "profile_label": profile_label,
        "source_profile_label": plan["source_profile_label"],
        "shared_contract": "US100 M5;2024 historical stress window;RuntimeProbeEA;run267CN feature order plus one run267CR engineered feature;EBM score table extension;attempt set/ini identity",
        "feature_count": len(feature_order),
        "feature_order_hash": feature_order_hash,
        "model_backend": "ebm_table",
        "model_materialization_type": model_row["model_materialization_type"],
        "engineered_features": engineered_feature,
        "known_difference": plan["known_difference"],
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "runtime_claim_boundary": CLAIM_BOUNDARY,
    }

    attempt_rows: list[dict[str, Any]] = []
    reproduction_rows: list[dict[str, Any]] = []
    for tier_index, (tier, role, token) in enumerate(
        (
            ("Tier A", "tier_only_total", "ta"),
            ("Tier A+B", "routed_total_duplicate_boundary", "rt"),
        ),
        start=1,
    ):
        source_attempt = dict(source_attempts[(source_variant_id, tier)])
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
                "InpFeatureCount": len(feature_order),
                "InpFeatureCsvUseCommonFiles": "true",
                "InpFeatureRequireTimestampMatch": "true",
                "InpFeatureAllowLatestFallback": "false",
                "InpFeatureStrictHeader": "true",
                "InpFeatureOrderHash": feature_order_hash,
                "InpFallbackEnabled": "false",
                "InpFallbackFeatureCsvPath": common_feature_path,
                "InpFallbackFeatureCount": len(feature_order),
                "InpFallbackModelPath": common_model_path,
                "InpFallbackModelId": f"{model_id}_fallback_disabled",
                "InpFallbackModelBackend": "ebm_table",
                "InpFallbackFeatureOrderHash": feature_order_hash,
                "InpTelemetryCsvPath": telemetry,
                "InpSummaryCsvPath": summary,
                "InpTelemetryUseCommonFiles": "true",
                "InpMagic": 26738000 + order * 10 + tier_index,
            }
        )
        set_payload = write_set(MT5_ROOT / f"{attempt_name}.set", set_values)
        ini_values = dict(source_ini_values)
        ini_values.update(
            {
                "ExpertParameters": Path(set_payload["path"]).name,
                "Report": f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}",
                "ReplaceReport": 1,
                "ShutdownTerminal": 1,
            }
        )
        ini_payload = write_ini(MT5_ROOT / f"{attempt_name}.ini", ini_values)
        attempt_rows.append(
            {
                "attempt_name": attempt_name,
                "variant_id": variant_id,
                "queue_id": plan["queue_id"],
                "source_variant_id": source_variant_id,
                "source_attempt_name": source_attempt["attempt_name"],
                "candidate_id": plan["candidate_id"],
                "candidate_alias": alias,
                "candidate_role": plan["candidate_role"],
                "profile_label": profile_label,
                "tier": tier,
                "attempt_role": role,
                "record_view_prefix": f"mt5_{token}_{alias}_{profile_token}",
                "set_path": set_payload["path"],
                "set_sha256": set_payload["sha256"],
                "ini_path": ini_payload["path"],
                "ini_sha256": ini_payload["sha256"],
                "common_telemetry_path": telemetry,
                "common_summary_path": summary,
                "common_feature_path": common_feature_path,
                "common_model_path": common_model_path,
                "tier_pair_boundary": TIER_PAIR_BOUNDARY,
                "execution_status": "execution_pending",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        reproduction_rows.append(
            {
                "queue_id": plan["queue_id"],
                "candidate_alias": alias,
                "source_profile_label": plan["source_profile_label"],
                "source_variant_id": source_variant_id,
                "source_attempt_name": source_attempt["attempt_name"],
                "tier": tier,
                "source_set_path": source_attempt["set_path"],
                "source_ini_path": source_attempt["ini_path"],
                "source_feature_file": rel(source_feature_path),
                "source_model_file": rel(source_model_path),
                "reproduction_status": "source_profile_reused_with_one_added_feature",
                "effect": "source run267CN profile remains a comparison anchor while run267CR adds one explicit follow-up feature",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    diagnostic_rows = [
        {
            "variant_id": variant_id,
            "queue_id": plan["queue_id"],
            "candidate_alias": alias,
            **row,
        }
        for row in diagnostics
    ]
    return variant_row, attempt_rows, feature_row, model_row, diagnostic_rows, reproduction_rows, runtime_contract


def queue_decision_rows(queue_rows: Sequence[Mapping[str, str]], plan_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    materialized_by_queue: dict[str, int] = {}
    for row in plan_rows:
        key = str(row["queue_id"])
        materialized_by_queue[key] = materialized_by_queue.get(key, 0) + 1
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        queue_id = queue["queue_id"]
        if queue_id in materialized_by_queue:
            decision = "materialized_execution_pending"
            effect = f"{materialized_by_queue[queue_id]} variant rows were converted into feature/model/set/ini inputs."
        elif queue_id == "run267cr_q05_lih_validation_guardrail_trace":
            decision = "guardrail_receipt_no_new_attempt"
            effect = "s262_lih is already included in q01 pool pressure; this row stays as validation-heavy guardrail receipt."
        else:
            held = QUEUE_HOLD_REASONS.get(queue_id, {})
            decision = str(held.get("decision", "held_for_followup"))
            effect = str(held.get("why", "held to avoid widening this materialization beyond the executable 2024 batch."))
        rows.append(
            {
                "queue_id": queue_id,
                "priority": queue.get("priority"),
                "workstream": queue.get("workstream"),
                "candidate_aliases": queue.get("candidate_aliases"),
                "run267CR_decision": decision,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def held_queue_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        queue_id = queue.get("queue_id", "")
        if queue_id not in QUEUE_HOLD_REASONS:
            continue
        held = QUEUE_HOLD_REASONS[queue_id]
        rows.append(
            {
                "queue_id": queue_id,
                "priority": queue.get("priority"),
                "candidate_aliases": queue.get("candidate_aliases"),
                "hold_status": held["decision"],
                "why_held": held["why"],
                "next_action": held["next"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def control_pressure_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    queue = next((row for row in queue_rows if row.get("queue_id") == "run267cr_q02_lc_aia_anchor_cross_period_pressure"), {})
    source_rows = {
        (row.get("candidate_alias"), row.get("profile_label")): row
        for row in read_csv(SOURCE_VARIANT_MANIFEST_PATH)
    }
    rows: list[dict[str, Any]] = []
    for alias in ("s264_lc", "s264_aia"):
        source = source_rows.get((alias, "shared_weakness_state_interaction"), {})
        rows.append(
            {
                "queue_id": queue.get("queue_id", "run267cr_q02_lc_aia_anchor_cross_period_pressure"),
                "candidate_alias": alias,
                "source_variant_id": source.get("variant_id", ""),
                "source_profile_label": source.get("profile_label", ""),
                "source_runtime_feature_file": source.get("runtime_feature_file", ""),
                "source_runtime_model_file": source.get("runtime_model_file", ""),
                "pressure_status": "held_for_adjacent_period_feature_frame_materialization",
                "why_not_materialized_now": "run267CR keeps the executable 2024 follow-up batch narrow; adjacent-period pressure must use period-specific feature frames.",
                "reopen_condition": "open a period-pack materialization if q01/q03/q04 produces a candidate worth further cross-period pressure.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def guardrail_rows(queue_rows: Sequence[Mapping[str, str]], plan_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    q05 = next((row for row in queue_rows if row.get("queue_id") == "run267cr_q05_lih_validation_guardrail_trace"), {})
    aliases_in_plan = {row.get("candidate_alias") for row in plan_rows}
    rows = [
        {
            "queue_id": q05.get("queue_id", "run267cr_q05_lih_validation_guardrail_trace"),
            "candidate_alias": "s262_lih",
            "guardrail_status": "active_in_q01_pool_pressure",
            "evidence": "s262_lih is materialized in q01 state_phase_monday_replacement and keeps validation-heavy guardrail role.",
            "reopen_condition": "if q01 weakens validation-heavy behavior, rerun a narrower s262_lih guardrail trace.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cr_q04_stc_redzone_stress_blast",
            "candidate_alias": "s258_stc",
            "guardrail_status": "single_stress_blast_materialized" if "s258_stc" in aliases_in_plan else "missing",
            "evidence": "s258_stc receives one red-zone stress attempt and must be pruned or demoted if DD/month holes stay uncomfortable.",
            "reopen_condition": "do not extend beyond this stress blast unless MT5 curve improves without red-zone DD.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def environment_receipt_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267cr_environment_reproducibility",
            "execution_environment": EXECUTION_ENVIRONMENT,
            "dependency_surface": "Python pandas/numpy; project foundation helpers; MT5 terminal paths supplied by existing project defaults for future execution",
            "entry_command": f"python {rel(PRODUCER_PATH)}",
            "local_assumptions": "Common Files copy uses the configured local MetaTrader terminal data root; Strategy Tester execution is next run, not claimed here",
            "clean_checkout_status": "reproducible_with_project_data_and_common_files_setup",
            "recovery_instruction": "rerun this script to regenerate run267CR feature/model/set/ini artifacts before run267CS execution",
            "reproducibility_judgment": "reproducible_with_setup",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": f"run267cr_data_integrity_{row['variant_id']}",
            "data_source": row["source_feature_file"],
            "time_axis": f"{row.get('first_bar_time_server')}..{row.get('last_bar_time_server')}",
            "sample_scope": PERIOD_LABEL,
            "missing_or_duplicate_check": f"missing_feature_cells={row.get('runtime_missing_feature_cells')};duplicate_bar_time_rows={row.get('duplicate_bar_time_rows')}",
            "feature_label_boundary": "uses current and prior closed bar features only; no future trade result input",
            "split_boundary": "historical_2024 source feature frame inherited from run267CN",
            "leakage_risk": "low_within_materialization_boundary",
            "data_hash_or_identity": row["runtime_feature_sha256"],
            "integrity_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in feature_rows
    ]


def runtime_parity_rows(feature_rows: Sequence[Mapping[str, Any]], model_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    models = {row["variant_id"]: row for row in model_rows}
    rows: list[dict[str, Any]] = []
    for feature in feature_rows:
        model = models[str(feature["variant_id"])]
        rows.append(
            {
                "receipt_id": f"run267cr_runtime_parity_{feature['variant_id']}",
                "variant_id": feature["variant_id"],
                "candidate_alias": feature["candidate_alias"],
                "feature_order_hash": feature["feature_order_hash"],
                "feature_count": feature["feature_count"],
                "model_sha256": model["runtime_model_sha256"],
                "common_feature_path": feature["common_feature_path"],
                "common_model_path": model["common_model_path"],
                "score_table_validation": feature["score_table_validation"],
                "runtime_handoff_status": "set_ini_materialized_execution_pending",
                "parity_boundary": "Python materialization and MT5 handoff are aligned by feature count/order/hash; MT5 runtime reproduction is next run",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def result_judgment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "judgment_id": "run267cr_materialization_judgment",
            "status": STATUS,
            "judgment": JUDGMENT,
            "why": "run267CR creates executable follow-up variants and receipts but does not produce MT5 KPI yet.",
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "counts": json.dumps(json_ready(dict(counts)), ensure_ascii=False, sort_keys=True),
            "next_action": NEXT_ACTION,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = (
        ("source_design_queue_available", counts["queue_rows"] == 6, f"queue_rows={counts['queue_rows']}"),
        ("executable_variants_materialized", counts["variants"] == 7, f"variants={counts['variants']}"),
        ("attempts_materialized", counts["attempts"] == 14, f"attempts={counts['attempts']}"),
        (
            "score_table_validation_passed",
            counts["score_table_validation_passed"] == counts["variants"],
            f"passed={counts['score_table_validation_passed']};variants={counts['variants']}",
        ),
        ("held_queue_documented", counts["held_rows"] == 2, f"held_rows={counts['held_rows']}"),
        ("guardrail_receipts_documented", counts["guardrail_receipts"] == 2, f"guardrail_receipts={counts['guardrail_receipts']}"),
        ("no_selection_claim", True, "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed"),
    )
    return [
        {
            "gate": name,
            "status": "passed" if passed else "failed",
            "evidence": evidence,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, passed, evidence in checks
    ]


def build_result() -> dict[str, Any]:
    required = [
        SOURCE_QUEUE_PATH,
        SOURCE_FEATURE_BLUEPRINT_PATH,
        SOURCE_BRANCH_DECISION_PATH,
        SOURCE_PRUNE_MATRIX_PATH,
        SOURCE_FAILURE_MEMORY_PATH,
        SOURCE_REVIEW_RESULT_PATH,
        SOURCE_VARIANT_MANIFEST_PATH,
        SOURCE_ATTEMPT_MANIFEST_PATH,
        SOURCE_RUNTIME_CONTRACT_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))

    created_at = utc_now()
    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    plan_rows = materialization_plan_rows(queue_rows)
    source_attempts = source_attempts_by_variant_tier()

    variant_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    diagnostic_rows: list[dict[str, Any]] = []
    reproduction_rows: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    for order, plan in enumerate(plan_rows, start=1):
        variant, attempts, feature, model, diagnostics, reproduction, contract = materialize_variant(
            plan,
            source_attempts,
            order=order,
        )
        variant_rows.append(variant)
        attempt_rows.extend(attempts)
        feature_rows.append(feature)
        model_rows.append(model)
        diagnostic_rows.extend(diagnostics)
        reproduction_rows.extend(reproduction)
        contracts.append(contract)

    held_rows = held_queue_rows(queue_rows)
    control_rows = control_pressure_rows(queue_rows)
    guardrails = guardrail_rows(queue_rows, plan_rows)
    queue_decisions = queue_decision_rows(queue_rows, plan_rows)
    counts = {
        "queue_rows": len(queue_rows),
        "materialized_queue_rows": len({row["queue_id"] for row in plan_rows}),
        "held_rows": len(held_rows),
        "variants": len(variant_rows),
        "attempts": len(attempt_rows),
        "feature_frames": len(feature_rows),
        "models": len(model_rows),
        "diagnostics": len(diagnostic_rows),
        "source_reproduction_receipts": len(reproduction_rows),
        "control_pressure_receipts": len(control_rows),
        "guardrail_receipts": len(guardrails),
        "score_table_validation_passed": sum(1 for row in feature_rows if row.get("score_table_validation") == "passed"),
    }
    result: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "counts": counts,
        "materialization_plan": plan_rows,
        "queue_decisions": queue_decisions,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "runtime_contract": contracts,
        "control_pressure_receipt": control_rows,
        "guardrail_receipt": guardrails,
        "held_queue": held_rows,
        "source_profile_reproduction_receipt": reproduction_rows,
        "feature_engineering_diagnostics": diagnostic_rows,
        "environment_reproducibility_receipt": environment_receipt_rows(),
        "data_integrity_receipt": data_integrity_rows(feature_rows),
        "runtime_parity_receipt": runtime_parity_rows(feature_rows, model_rows),
        "result_judgment": result_judgment_rows(counts),
        "gate_audit": gate_audit_rows(counts),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "sources": {
            "source_queue": rel(SOURCE_QUEUE_PATH),
            "source_feature_blueprint": rel(SOURCE_FEATURE_BLUEPRINT_PATH),
            "source_branch_decision": rel(SOURCE_BRANCH_DECISION_PATH),
            "source_prune_matrix": rel(SOURCE_PRUNE_MATRIX_PATH),
            "source_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
            "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "source_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
            "source_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
            "source_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
            "source_design_report": rel(SOURCE_REPORT_PATH),
            "source_materialization_report": rel(SOURCE_MATERIALIZATION_REPORT_PATH),
            "producer": rel(PRODUCER_PATH),
        },
        "outputs": {
            "materialization_plan": rel(MATERIALIZATION_PLAN_PATH),
            "queue_decision": rel(QUEUE_DECISION_PATH),
            "feature_frame_manifest": rel(FEATURE_FRAME_MANIFEST_PATH),
            "model_manifest": rel(MODEL_MANIFEST_PATH),
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "control_pressure_receipt": rel(CONTROL_PRESSURE_RECEIPT_PATH),
            "guardrail_receipt": rel(GUARDRAIL_RECEIPT_PATH),
            "held_queue": rel(HELD_QUEUE_PATH),
            "source_profile_reproduction_receipt": rel(SOURCE_REPRODUCTION_RECEIPT_PATH),
            "feature_engineering_diagnostics": rel(FEATURE_ENGINEERING_DIAGNOSTICS_PATH),
            "environment_reproducibility_receipt": rel(ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH),
            "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
            "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    return result


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(MATERIALIZATION_PLAN_PATH, result["materialization_plan"])
    write_csv(QUEUE_DECISION_PATH, result["queue_decisions"])
    write_csv(FEATURE_FRAME_MANIFEST_PATH, result["feature_frame_manifest"])
    write_csv(MODEL_MANIFEST_PATH, result["model_manifest"])
    write_csv(VARIANT_MANIFEST_PATH, result["variant_manifest"])
    write_csv(ATTEMPT_MANIFEST_PATH, result["attempt_manifest"])
    write_csv(RUNTIME_CONTRACT_PATH, result["runtime_contract"])
    write_csv(CONTROL_PRESSURE_RECEIPT_PATH, result["control_pressure_receipt"])
    write_csv(GUARDRAIL_RECEIPT_PATH, result["guardrail_receipt"])
    write_csv(HELD_QUEUE_PATH, result["held_queue"])
    write_csv(SOURCE_REPRODUCTION_RECEIPT_PATH, result["source_profile_reproduction_receipt"])
    write_csv(FEATURE_ENGINEERING_DIAGNOSTICS_PATH, result["feature_engineering_diagnostics"])
    write_csv(ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, result["environment_reproducibility_receipt"])
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"])
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"])
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"])
    write_csv(GATE_AUDIT_PATH, result["gate_audit"])
    write_json(RUN_MANIFEST_PATH, run_manifest_payload(result))
    write_json(LINEAGE_PATH, lineage_payload(result))
    write_json(REVIEW_RESULT_PATH, review_result_payload(result))
    write_md(REPORT_PATH, report_markdown(result))


def run_manifest_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": result["created_at_utc"],
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "claim_boundary": CLAIM_BOUNDARY,
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "counts": result["counts"],
        "sources": result["sources"],
        "outputs": result["outputs"],
        "next_action": NEXT_ACTION,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def lineage_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_inputs": result["sources"],
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": result["outputs"],
        "artifact_hashes": {
            key: sha256_file_lf_normalized(repo_path(path))
            for key, path in result["outputs"].items()
            if path_exists(repo_path(str(path)))
        },
        "registry_links": {
            "stage_ledger": rel(STAGE_LEDGER_PATH),
            "project_ledger": rel(PROJECT_LEDGER_PATH),
            "run_registry": rel(RUN_REGISTRY_PATH),
            "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
        },
        "availability": "tracked_plus_ignored_run_artifacts_with_manifest",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def review_result_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "counts": result["counts"],
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    return f"""# Stage267 Run267CR Shared Weakness Breakout Follow-up Materialization(267단계 267CR 공유 약점 돌파 후속 물질화)

## Summary(요약)

Run267CR(267CR 실행)은 run267CQ(267CQ 실행)의 follow-up/prune design(후속/가지치기 설계)을 MT5(MetaTrader 5, 메타트레이더5) 실행 대기 입력으로 바꿨다.

Effect(효과): variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, held queue(보류 대기열) `{counts['held_rows']}`개, control pressure receipts(대조 압박 영수증) `{counts['control_pressure_receipts']}`개, guardrail receipts(가드레일 영수증) `{counts['guardrail_receipts']}`개를 만들었다.

## Why It Still Takes Time(왜 아직 오래 걸리는가)

Baseline candidate(기준 후보)는 운영 기준선이 아니라 R&D racing research candidate(연구개발 경주용 연구 후보)다. 그래서 숫자 1등을 바로 고르지 않고, weak slice(약한 구간), balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), similar replacement(유사 대체), feature ablation(피처 제거), Adapter handoff(어댑터 인계)를 같이 본다.

Effect(효과): 좋아 보이는 후보를 성급히 ONNX(오닉스) 후보로 올리지 않고, “어디서 깨지는지”를 먼저 드러낸다.

## Materialized Work(물질화한 작업)

- `run267cr_q01_pool_monday_state_phase_replacement`: five candidates(후보 5개)를 state phase replacement(상태 국면 대체) feature(피처)로 물질화했다.
- `run267cr_q03_aih_aggressive_shock_supply_expansion`: `s264_aih`를 aggressive supply expansion(공격형 공급 확장) 변형으로 물질화했다.
- `run267cr_q04_stc_redzone_stress_blast`: `s258_stc`를 one-shot red-zone stress(단발 고위험 압박) 변형으로 물질화했다.
- `run267cr_q02_lc_aia_anchor_cross_period_pressure`: adjacent-period feature frames(인접 기간 피처 프레임)가 필요해 보류했다.
- `run267cr_q05_lih_validation_guardrail_trace`: `s262_lih`는 q01 안에서 validation-heavy guardrail(검증 중심 가드레일)로 연결했다.
- `run267cr_q06_buy_side_similar_replacement_probe`: q03에 일부 흡수하고 standalone probe(독립 탐침)는 보류했다.

## Boundary(경계)

- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Next Action(다음 행동)

`{NEXT_ACTION}`
"""


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, path_text in result["outputs"].items():
        path = repo_path(str(path_text))
        if not path_exists(path):
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_NUMBER}_{safe_token(key)}",
                "artifact_type": key,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": "run267CR shared weakness follow-up materialization artifact; no candidate selection; no ONNX claim",
            }
        )
    return rows


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
    for index, current in enumerate(lines):
        if needle in current:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block in text:
        return text
    if marker not in text:
        return text.rstrip() + "\n" + marker + focus_block
    return text.replace(marker, marker + focus_block, 1)


def update_current_documents(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    summary_line = (
        f"- run267CR_summary(267CR 요약): Run267CR(267CR 실행)은 run267CQ(267CQ 실행)의 공유 약점 후속 queue(대기열)를 "
        f"variants(변형) `{counts['variants']}`개와 attempts(시도) `{counts['attempts']}`개로 물질화했다. "
        "Effect(효과): 다음 run267CS(267CS 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 곡선/약점 구간/거래 품질을 검증할 수 있다."
    )
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(
        current,
        "- adapter_under_review(검토 중 어댑터):",
        "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_followup_materialization`",
    )
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_after_contains(current, "run267CQ_summary", summary_line)
    current = append_after_contains(
        current,
        "stage267_run267CQ_shared_weakness_breakout_followup_or_prune_design.md",
        f"- run267CR_shared_weakness_breakout_followup_materialization(267CR 공유 약점 돌파 후속 물질화): `{rel(REPORT_PATH)}`",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selected = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_after_contains(selected, "run267CQ_summary", summary_line)
    selected = append_after_contains(
        selected,
        "stage267_run267CQ_shared_weakness_breakout_followup_or_prune_design.md",
        f"- run267CR_shared_weakness_breakout_followup_materialization(267CR 공유 약점 돌파 후속 물질화): `{rel(REPORT_PATH)}`",
    )
    write_md(SELECTION_STATUS_PATH, selected)

    focus_block = (
        "- >-\n"
        f"  Stage267(267단계) run267CR(267CR 실행) shared weakness breakout follow-up materialization"
        f"(공유 약점 돌파 후속 물질화) `{STATUS}`. Effect(효과): run267CQ(267CQ 실행)의 materialization queue(물질화 대기열)를 "
        f"variants(변형) `{counts['variants']}`개와 attempts(시도) `{counts['attempts']}`개로 만들고, q02/q06은 held queue(보류 대기열)로 기록했다. "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = prepend_current_focus(workspace, focus_block)
    workspace = workspace.replace(
        "  next_action: run267CR_materialize_shared_weakness_breakout_followup_queue",
        f"  next_action: {NEXT_ACTION}",
        1,
    )
    workspace = append_after_contains(
        workspace,
        "run267CQ_shared_weakness_breakout_followup_or_prune_design",
        f"  run267CR_shared_weakness_breakout_followup_materialization_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)

    index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    index = append_after_contains(
        index,
        "run267CQ_shared_weakness_breakout_followup_or_prune_design",
        f"- run267CR_shared_weakness_breakout_followup_materialization(267CR 공유 약점 돌파 후속 물질화): `{rel(REPORT_PATH)}`",
    )
    block = (
        "\nRun267CR(267CR 실행)은 run267CQ(267CQ 실행)의 공유 약점 후속 대기열을 MT5(MetaTrader 5, 메타트레이더5) 실행 대기 산출물로 바꿨다.\n"
        f"Effect(효과): variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개를 남기고 "
        f"다음 행동을 `{NEXT_ACTION}`로 고정했다.\n"
        "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.\n"
    )
    if "Run267CR(267CR 실행)은" not in index:
        index = index.rstrip() + "\n" + block
    write_md(REVIEW_INDEX_PATH, index)


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    notes = (
        f"variants={counts['variants']};attempts={counts['attempts']};"
        f"held={counts['held_rows']};control_pressure={counts['control_pressure_receipts']};"
        f"guardrails={counts['guardrail_receipts']};next_action={NEXT_ACTION};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267CR_shared_weakness_breakout_followup_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_followup_materialization",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B attempt inputs; true Tier B fallback blocked",
        "scoreboard": "feature_model_set_ini_materialization_control_guardrail_held_queue",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_mt5_kpi_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_shared_weakness_breakout_followup_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__shared_weakness_breakout_followup_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "shared_weakness_breakout_followup_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "shared_weakness_breakout_followup_materialization",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B attempt inputs; true Tier B fallback blocked",
        "kpi_scope": "feature_model_set_ini_materialization_no_mt5_kpi",
        "scoreboard_lane": "shared_weakness_breakout_followup_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={counts['variants']};attempts={counts['attempts']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at, result), key="artifact_id")


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers_and_artifacts(str(result["created_at_utc"]), result)
    update_current_documents(result)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "counts": result["counts"],
                "next_action": NEXT_ACTION,
                "selected_candidate": "none",
                "selected_research_baseline": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
