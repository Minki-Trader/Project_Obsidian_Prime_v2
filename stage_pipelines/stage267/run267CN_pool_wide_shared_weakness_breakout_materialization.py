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
    run267CF_pool_wide_orthogonal_loss_shape_state_materialization as source_materialization,
)
from stage_pipelines.stage267 import (
    run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267CN"
RUN_ID = "run267CN_stage267_pool_wide_shared_weakness_breakout_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_materialization.RUN_ID
STATUS = "run267CN_pool_wide_shared_weakness_breakout_materialized_execution_pending"
JUDGMENT = "shared_weakness_breakout_materialized_no_candidate_selection"
NEXT_ACTION = "run267CO_execute_pool_wide_shared_weakness_breakout_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_shared_weakness_breakout_materialization"
FEATURE_ROOT = RUN_ROOT / "features"
VARIANT_ROOT = RUN_ROOT / "variants"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_QUEUE_PATH = source_design.MATERIALIZATION_QUEUE_PATH
SOURCE_BRANCH_DECISION_PATH = source_design.BRANCH_DECISION_PATH
SOURCE_PRUNE_MATRIX_PATH = source_design.PRUNE_MATRIX_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_REVIEW_RESULT_PATH = source_design.REVIEW_RESULT_PATH
SOURCE_VARIANT_MANIFEST_PATH = source_materialization.VARIANT_MANIFEST_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = source_materialization.ATTEMPT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_materialization.RUNTIME_CONTRACT_PATH
SOURCE_REPORT_PATH = source_design.REPORT_PATH
SOURCE_CL_CANDIDATE_REVIEW_PATH = source_design.SOURCE_CANDIDATE_REVIEW_PATH
SOURCE_CL_NEGATIVE_SLICE_PATH = source_design.SOURCE_NEGATIVE_SLICE_PATH
SOURCE_CJ_VARIANT_MANIFEST_PATH = (
    STAGE_ROOT
    / "02_runs"
    / "run267CJ"
    / "pool_wide_orthogonal_loss_shape_state_followup_materialization"
    / "variant_manifest.csv"
)

MATERIALIZATION_PLAN_PATH = RUN_ROOT / "materialization_plan.csv"
QUEUE_DECISION_PATH = RUN_ROOT / "queue_decision.csv"
SOURCE_REPRODUCTION_RECEIPT_PATH = RUN_ROOT / "source_profile_reproduction_receipt.csv"
FEATURE_FRAME_MANIFEST_PATH = RUN_ROOT / "feature_frame_manifest.csv"
MODEL_MANIFEST_PATH = RUN_ROOT / "model_manifest.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
CONTROL_HOLDOUT_RECEIPT_PATH = RUN_ROOT / "control_holdout_receipt.csv"
GUARDRAIL_RECEIPT_PATH = RUN_ROOT / "guardrail_receipt.csv"
HELD_QUEUE_PATH = RUN_ROOT / "held_queue.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CN_pool_wide_shared_weakness_breakout_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CN_pool_wide_shared_weakness_breakout_materialization.py")

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

COMMON_ROOT = "OPV2/s267cn/run267CN_shared_weakness_breakout"
EXPLORATION_LABEL = "stage267_BaselineRacing__SharedWeaknessBreakout"
PERIOD_LABEL = "historical_2024_tier_a_train_era_stress"
TIER_PAIR_BOUNDARY = (
    "Tier A and duplicate-boundary Tier A+B inputs are materialized; true Tier B fallback "
    "and actual routed total remain outside this run"
)
MATERIALIZATION_BOUNDARY = "materialization_only_no_candidate_selection_no_selected_research_baseline_no_onnx"

CANDIDATE_ORDER = ("s264_aih", "s264_lc", "s262_lih", "s264_aia", "s258_stc")
ACTIVE_VARIANT_CONFIGS = (
    {
        "queue_id": "run267cn_q01_shared_monday_december_state_interaction",
        "source_profile_label": "similar_replacement_impulse",
        "profile_label": "shared_weakness_state_interaction",
        "profile_token": "shared_state_breakout",
        "variant_token": "shared_state_breakout",
        "engineered_feature": "stage267cn_shared_weakness_state_interaction_score",
        "attempt_suffix": "shared_breakout",
        "model_strength": "moderate_directional_permission_when_noncalendar_shared_weakness_state_is_high",
        "aliases": CANDIDATE_ORDER,
    },
    {
        "queue_id": "run267cn_q02_s264_aih_aggressive_shock_release_reentry",
        "source_profile_label": "loss_shape_proxy_minimal",
        "profile_label": "aggressive_shock_release_reentry",
        "profile_token": "shock_release_reentry",
        "variant_token": "aggressive_shock_release_reentry",
        "engineered_feature": "stage267cn_aggressive_shock_release_reentry_score",
        "attempt_suffix": "shock_release",
        "model_strength": "stronger_directional_permission_when_shock_release_structure_is_high",
        "aliases": ("s264_aih",),
    },
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


def safe_token(value: Any, limit: int = 80) -> str:
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
    lines = [f"; generated_by={RUN_NUMBER}_pool_wide_shared_weakness_breakout_materialization"]
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
        scaled = ((clean - q25) / (q75 - q25)).clip(0.0, 1.0).fillna(0.0).astype("float64")
    return scaled, {"q25": q25, "q50": q50, "q75": q75}


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
            "threshold_source": "blocked_component_receipt_not_future_trade_result",
        }
    raw = pd.to_numeric(frame[column], errors="coerce").astype("float64")
    if transform == "raw":
        transformed = raw
    elif transform == "abs":
        transformed = raw.abs()
    elif transform == "positive":
        transformed = raw.clip(lower=0.0)
    elif transform == "abs_center_1":
        transformed = (raw - 1.0).abs()
    elif transform == "abs_center_0_5":
        transformed = (raw - 0.5).abs()
    else:
        raise ValueError(f"unknown transform: {transform}")
    scaled, stats = quantile_scale(transformed)
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


def compute_engineered_feature(frame: pd.DataFrame, *, mode: str, feature_name: str) -> tuple[pd.Series, list[dict[str, Any]]]:
    if mode == "shared_weakness_state_interaction":
        parts = [
            ("return_zscore_20", "abs", 0.22),
            ("return_1_over_atr_14", "abs", 0.18),
            ("atr_14_over_atr_50", "abs_center_1", 0.17),
            ("historical_vol_5_over_20", "abs_center_1", 0.15),
            ("stage267cf_volatility_energy_transition_score", "raw", 0.12),
            ("stage267cf_range_pressure_asymmetry_score", "raw", 0.10),
            ("bb_position_20", "abs_center_0_5", 0.06),
        ]
    elif mode == "aggressive_shock_release_reentry":
        parts = [
            ("return_zscore_20", "abs", 0.24),
            ("return_1_over_atr_14", "abs", 0.18),
            ("gap_percent", "abs", 0.12),
            ("stage267cf_trend_strength_replacement_score", "raw", 0.16),
            ("stage267cf_volatility_energy_transition_score", "raw", 0.14),
            ("close_prev_close_ratio", "abs_center_1", 0.08),
        ]
    else:
        raise ValueError(f"unknown feature mode: {mode}")

    diagnostics: list[dict[str, Any]] = []
    score = pd.Series(0.0, index=frame.index, dtype="float64")
    weight_sum = 0.0
    for column, transform, weight in parts:
        scaled, row = component(frame, column, transform, weight=weight, feature_name=feature_name)
        score = score + float(weight) * scaled
        weight_sum += float(weight)
        diagnostics.append(row)
    if mode == "aggressive_shock_release_reentry":
        if {"log_return_1", "log_return_3"}.issubset(frame.columns):
            one = pd.to_numeric(frame["log_return_1"], errors="coerce").astype("float64").fillna(0.0)
            three = pd.to_numeric(frame["log_return_3"], errors="coerce").astype("float64").fillna(0.0)
            release_raw = (-np.sign(three) * one * three.abs()).clip(lower=0.0)
            release_scaled, stats = quantile_scale(release_raw)
            score = score + 0.08 * release_scaled
            weight_sum += 0.08
            diagnostics.append(
                {
                    "engineered_feature": feature_name,
                    "source_component": "log_return_1_against_log_return_3_direction",
                    "transform": "shock_release_slope_proxy",
                    "weight": 0.08,
                    "q25": stats["q25"],
                    "q50": stats["q50"],
                    "q75": stats["q75"],
                    "component_status": "ok",
                    "threshold_source": "closed_bar_return_interaction_no_future_trade_result",
                }
            )
        else:
            diagnostics.append(
                {
                    "engineered_feature": feature_name,
                    "source_component": "log_return_1_against_log_return_3_direction",
                    "transform": "shock_release_slope_proxy",
                    "weight": 0.08,
                    "q25": 0.0,
                    "q50": 0.0,
                    "q75": 0.0,
                    "component_status": "missing_component_zero_filled",
                    "threshold_source": "blocked_component_receipt_not_future_trade_result",
                }
            )
    if weight_sum <= 0:
        return score.clip(0.0, 1.0).astype("float64"), diagnostics
    return (score / weight_sum).clip(0.0, 1.0).astype("float64"), diagnostics


def source_feature_order(path: Path) -> list[str]:
    return source_materialization.source_feature_order(path)


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
    variants = source_variants_by_alias_profile()
    rows: list[dict[str, Any]] = []
    order = 0
    for config in ACTIVE_VARIANT_CONFIGS:
        queue = queue_by_id[str(config["queue_id"])]
        for alias in config["aliases"]:
            source = variants[(alias, str(config["source_profile_label"]))]
            order += 1
            variant_id = f"run267cn_{order:02d}_{alias}_{config['variant_token']}"
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
                    "model_strength": config["model_strength"],
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
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
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
    source_materialization.append_model_features(
        source_model_path,
        model_path,
        source_feature_count=len(base_feature_order),
        profile_label=profile_label,
        engineered_features=[engineered_feature],
    )
    validation = source_materialization.validate_score_table(feature_path, model_path, feature_order)

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
        "model_materialization_type": "augmented_run267CF_score_table_with_shared_weakness_breakout_feature",
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
        "shared_contract": "US100 M5;2024 historical stress window;RuntimeProbeEA;run267CF feature order plus run267CN engineered feature;EBM score table extension;attempt set/ini identity",
        "feature_count": len(feature_order),
        "feature_order_hash": feature_order_hash,
        "model_backend": "ebm_table",
        "model_materialization_type": model_row["model_materialization_type"],
        "engineered_features": engineered_feature,
        "known_difference": "adds one noncalendar state-interaction feature; no weekday/month hard filter; no EA copy",
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
                "InpMagic": 26737000 + order * 10 + tier_index,
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
                "record_view_prefix": f"mt5_{token}_{alias}_{plan['profile_token']}",
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
                "reproduction_status": "source_profile_reuse_receipt_no_new_source_attempt",
                "effect": "source profile is kept as comparison reference for the modified run267CN variant",
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


def queue_decision_rows(queue_rows: Sequence[Mapping[str, str]], material_plan: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    materialized_by_queue: dict[str, int] = {}
    for row in material_plan:
        materialized_by_queue[str(row["queue_id"])] = materialized_by_queue.get(str(row["queue_id"]), 0) + 1
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        queue_id = row["queue_id"]
        if queue_id in materialized_by_queue:
            decision = "materialized_execution_pending"
            effect = (
                f"`{materialized_by_queue[queue_id]}`개 variant rows(변형 행)을 "
                "feature/model/set/ini(피처/모델/설정/초기화) 입력으로 만들었다"
            )
        elif queue_id == "run267cn_q03_anchor_control_holdout_trace":
            decision = "control_holdout_receipt_no_new_attempt"
            effect = "run267CJ/run267CL(267CJ/267CL 실행)의 수익 행을 변경 없는 control(대조)로 남겼다"
        else:
            decision = "guardrail_receipt_no_new_attempt"
            effect = "validation-heavy/stress(검증 중심/압박) 역할을 실패 조건 guardrail(가드레일)로 연결했다"
        rows.append(
            {
                "queue_id": queue_id,
                "priority": row.get("priority"),
                "workstream": row.get("workstream"),
                "candidate_aliases": row.get("candidate_aliases"),
                "run267CN_decision": decision,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def held_queue_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    held_ids = {
        "run267cn_q03_anchor_control_holdout_trace": "control_receipt_only_no_new_attempt",
        "run267cn_q04_validation_and_stress_guardrails": "guardrail_receipt_only_no_new_attempt",
    }
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        if row.get("queue_id") not in held_ids:
            continue
        rows.append(
            {
                "queue_id": row["queue_id"],
                "priority": row.get("priority"),
                "candidate_aliases": row.get("candidate_aliases"),
                "hold_status": held_ids[row["queue_id"]],
                "why_held": "run267CN(267CN 실행)의 P0 MT5(MetaTrader 5, 메타트레이더5) 실행 묶음에는 포함하지 않는다",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def control_holdout_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    queue = next((row for row in queue_rows if row.get("queue_id") == "run267cn_q03_anchor_control_holdout_trace"), {})
    control_sources = {row.get("candidate_alias"): row for row in read_csv(SOURCE_CJ_VARIANT_MANIFEST_PATH)}
    review_rows = {row.get("candidate_alias"): row for row in read_csv(SOURCE_CL_CANDIDATE_REVIEW_PATH)}
    rows: list[dict[str, Any]] = []
    for alias in ("s264_lc", "s264_aia"):
        source = control_sources.get(alias, {})
        review = review_rows.get(alias, {})
        rows.append(
            {
                "queue_id": queue.get("queue_id", "run267cn_q03_anchor_control_holdout_trace"),
                "candidate_alias": alias,
                "source_variant_id": source.get("variant_id", ""),
                "source_profile_label": source.get("profile_label", ""),
                "source_runtime_feature_file": source.get("runtime_feature_file", ""),
                "source_runtime_model_file": source.get("runtime_model_file", ""),
                "run267CL_net_profit": review.get("net_profit", ""),
                "run267CL_profit_factor": review.get("profit_factor", ""),
                "run267CL_trade_count": review.get("trade_count", ""),
                "holdout_status": "unchanged_control_reference_no_new_attempt",
                "effect": "새 state-breakout(상태 돌파) 분기를 측정하는 동안 headline KPI(대표 핵심 성과 지표) 선택을 막는다",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def guardrail_rows(queue_rows: Sequence[Mapping[str, str]], plan_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    queue = next((row for row in queue_rows if row.get("queue_id") == "run267cn_q04_validation_and_stress_guardrails"), {})
    materialized_aliases = {str(row["candidate_alias"]) for row in plan_rows}
    rows: list[dict[str, Any]] = []
    for alias, role in (
        ("s262_lih", "validation-heavy role"),
        ("s258_stc", "stress challenger role"),
    ):
        rows.append(
            {
                "queue_id": queue.get("queue_id", "run267cn_q04_validation_and_stress_guardrails"),
                "candidate_alias": alias,
                "candidate_role": role,
                "active_materialization_status": "present_in_q01_shared_state_batch" if alias in materialized_aliases else "not_materialized",
                "guardrail_condition": "validation damage(검증 손상), DD expansion(손실폭 확대), trade-count collapse(거래 수 붕괴), weak-month concentration(약한 월 집중)을 본다",
                "effect": "새 feature branch(피처 분기)를 net profit(순수익)만으로 판단하지 못하게 한다",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def experiment_design_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": row["queue_id"],
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
            "evidence_plan": "variant_manifest;attempt_manifest;runtime_contract;control_holdout_receipt;guardrail_receipt;next MT5 batch KPI and curve review",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in queue_rows
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in feature_rows:
        status = "passed"
        reasons: list[str] = []
        if int(row["rows"]) <= 0:
            status = "failed"
            reasons.append("no feature rows")
        if int(row["duplicate_bar_time_rows"]) > 0:
            status = "failed"
            reasons.append("duplicate bar_time_server rows")
        if int(row["runtime_missing_feature_cells"]) > 0:
            status = "failed"
            reasons.append("missing feature cells")
        rows.append(
            {
                "variant_id": row["variant_id"],
                "candidate_alias": row["candidate_alias"],
                "runtime_feature_file": row["runtime_feature_file"],
                "rows": row["rows"],
                "duplicate_bar_time_rows": row["duplicate_bar_time_rows"],
                "runtime_missing_feature_cells": row["runtime_missing_feature_cells"],
                "first_bar_time_server": row["first_bar_time_server"],
                "last_bar_time_server": row["last_bar_time_server"],
                "data_integrity_status": status,
                "notes": ";".join(reasons) if reasons else "no duplicate/missing feature cells detected",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def runtime_parity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "variant_id": row["variant_id"],
            "candidate_alias": row["candidate_alias"],
            "feature_count": row["feature_count"],
            "feature_order_hash": row["feature_order_hash"],
            "runtime_feature_file": row["runtime_feature_file"],
            "common_feature_path": row["common_feature_path"],
            "runtime_model_file": next(
                (
                    model["runtime_model_file"]
                    for model in getattr(runtime_parity_rows, "_model_rows", [])
                    if model["variant_id"] == row["variant_id"]
                ),
                "",
            ),
            "runtime_parity_status": "handoff_materialized_parity_not_executed",
            "effect": "MT5(MetaTrader 5, 메타트레이더5) 실행 전 feature order(피처 순서)와 common-file handoff(공통 파일 인계)를 추적할 수 있다",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in feature_rows
    ]


def result_judgment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "judgment_id": "run267cn_materialization_boundary",
            "judgment": JUDGMENT,
            "evidence": f"variants={counts['variants']};attempts={counts['attempts']};control_receipts={counts['control_receipts']};guardrail_receipts={counts['guardrail_receipts']}",
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks = [
        ("source_queue_exists", path_exists(SOURCE_QUEUE_PATH), rel(SOURCE_QUEUE_PATH)),
        ("source_variant_manifest_exists", path_exists(SOURCE_VARIANT_MANIFEST_PATH), rel(SOURCE_VARIANT_MANIFEST_PATH)),
        ("source_attempt_manifest_exists", path_exists(SOURCE_ATTEMPT_MANIFEST_PATH), rel(SOURCE_ATTEMPT_MANIFEST_PATH)),
        ("materialized_variant_count", int(counts["variants"]) == 6, f"variants={counts['variants']}"),
        ("materialized_attempt_count", int(counts["attempts"]) == 12, f"attempts={counts['attempts']}"),
        ("control_holdout_receipt_count", int(counts["control_receipts"]) == 2, f"control_receipts={counts['control_receipts']}"),
        ("guardrail_receipt_count", int(counts["guardrail_receipts"]) == 2, f"guardrail_receipts={counts['guardrail_receipts']}"),
        ("score_table_validation", int(counts["score_table_validation_passed"]) == int(counts["variants"]), f"passed={counts['score_table_validation_passed']}"),
    ]
    return [
        {
            "gate": name,
            "status": "passed" if passed else "failed",
            "evidence": evidence,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, passed, evidence in checks
    ]


def runtime_contract_rows(contracts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [dict(row) for row in contracts]


def build_result() -> dict[str, Any]:
    required = [
        SOURCE_QUEUE_PATH,
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

    setattr(runtime_parity_rows, "_model_rows", model_rows)
    control_rows = control_holdout_rows(queue_rows)
    guardrail = guardrail_rows(queue_rows, plan_rows)
    held_rows = held_queue_rows(queue_rows)
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
        "control_receipts": len(control_rows),
        "guardrail_receipts": len(guardrail),
        "score_table_validation_passed": sum(
            1 for row in feature_rows if str(row.get("score_table_validation")) == "passed"
        ),
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
        "source_profile_reproduction_receipt": reproduction_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "feature_engineering_diagnostics": diagnostic_rows,
        "runtime_contract": runtime_contract_rows(contracts),
        "control_holdout_receipt": control_rows,
        "guardrail_receipt": guardrail,
        "held_queue": held_rows,
        "experiment_design_receipt": experiment_design_rows(queue_rows),
        "data_integrity_receipt": data_integrity_rows(feature_rows),
        "runtime_parity_receipt": runtime_parity_rows(feature_rows),
        "result_judgment": result_judgment_rows(counts),
        "gate_audit": gate_audit_rows(counts),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "sources": {
            "source_queue": rel(SOURCE_QUEUE_PATH),
            "source_branch_decision": rel(SOURCE_BRANCH_DECISION_PATH),
            "source_prune_matrix": rel(SOURCE_PRUNE_MATRIX_PATH),
            "source_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
            "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "source_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
            "source_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
            "source_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
            "source_run267CL_candidate_review": rel(SOURCE_CL_CANDIDATE_REVIEW_PATH),
            "source_run267CL_negative_slice": rel(SOURCE_CL_NEGATIVE_SLICE_PATH),
            "source_run267CJ_variant_manifest": rel(SOURCE_CJ_VARIANT_MANIFEST_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
            "producer": rel(PRODUCER_PATH),
        },
        "outputs": {
            "materialization_plan": rel(MATERIALIZATION_PLAN_PATH),
            "queue_decision": rel(QUEUE_DECISION_PATH),
            "source_profile_reproduction_receipt": rel(SOURCE_REPRODUCTION_RECEIPT_PATH),
            "feature_frame_manifest": rel(FEATURE_FRAME_MANIFEST_PATH),
            "model_manifest": rel(MODEL_MANIFEST_PATH),
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "control_holdout_receipt": rel(CONTROL_HOLDOUT_RECEIPT_PATH),
            "guardrail_receipt": rel(GUARDRAIL_RECEIPT_PATH),
            "held_queue": rel(HELD_QUEUE_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
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
    write_csv(SOURCE_REPRODUCTION_RECEIPT_PATH, result["source_profile_reproduction_receipt"])
    write_csv(FEATURE_FRAME_MANIFEST_PATH, result["feature_frame_manifest"])
    write_csv(MODEL_MANIFEST_PATH, result["model_manifest"])
    write_csv(VARIANT_MANIFEST_PATH, result["variant_manifest"])
    write_csv(ATTEMPT_MANIFEST_PATH, result["attempt_manifest"])
    write_csv(RUNTIME_CONTRACT_PATH, result["runtime_contract"])
    write_csv(CONTROL_HOLDOUT_RECEIPT_PATH, result["control_holdout_receipt"])
    write_csv(GUARDRAIL_RECEIPT_PATH, result["guardrail_receipt"])
    write_csv(HELD_QUEUE_PATH, result["held_queue"])
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"])
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"])
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"])
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"])
    write_csv(GATE_AUDIT_PATH, result["gate_audit"])
    write_json(RUN_MANIFEST_PATH, result)
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
            "source_inputs": result["sources"],
            "producer": rel(PRODUCER_PATH),
            "consumer": NEXT_ACTION,
            "artifact_paths": result["outputs"],
            "registry_links": {
                "stage_ledger": rel(STAGE_LEDGER_PATH),
                "project_ledger": rel(PROJECT_LEDGER_PATH),
                "run_registry": rel(RUN_REGISTRY_PATH),
                "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
            },
            "availability": "tracked_and_common_files_handoff",
            "lineage_judgment": "connected_with_boundary_no_selection",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        REVIEW_RESULT_PATH,
        {
            "run_id": RUN_ID,
            "status": result["status"],
            "judgment": result["judgment"],
            "counts": result["counts"],
            "next_action": NEXT_ACTION,
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_md(REPORT_PATH, report_markdown(result))


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267CN Shared Weakness Breakout Materialization(267단계 267CN 공유 약점 돌파 물질화)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- source_materialization(원천 물질화): `{SOURCE_MATERIALIZATION_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- queue_rows(대기열 행): `{counts['queue_rows']}`",
        f"- materialized_variants(물질화 변형): `{counts['variants']}`",
        f"- materialized_attempts(물질화 시도): `{counts['attempts']}`",
        f"- control_receipts(대조 영수증): `{counts['control_receipts']}`",
        f"- guardrail_receipts(가드레일 영수증): `{counts['guardrail_receipts']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267CM(267CM 실행)의 shared weakness/state breakout(공유 약점/상태 돌파) 큐를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 만들었다.",
        "Effect(효과): 다음 run267CO(267CO 실행)에서 headline KPI(대표 핵심 성과 지표)가 아니라 weak slice(약점 구간), curve(곡선), trade quality(거래 품질)로 다시 깨뜨려 볼 수 있다.",
        "",
        "## Queue Decision(대기열 판단)",
        "",
        "| queue(대기열) | candidates(후보) | decision(판단) | effect(효과) |",
        "| --- | --- | --- | --- |",
    ]
    for row in result["queue_decisions"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['candidate_aliases']}` | `{row['run267CN_decision']}` | {row['effect']} |"
        )
    lines.extend(
        [
            "",
            "## Attempt Inputs(시도 입력)",
            "",
            "| attempt(시도) | candidate(후보) | profile(프로필) | tier(티어) | status(상태) |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in result["attempt_manifest"]:
        lines.append(
            f"| `{row['attempt_name']}` | `{row['candidate_alias']}` | `{row['profile_label']}` | `{row['tier']}` | `{row['execution_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 run(실행)은 materialization only(물질화 전용)이고 아직 MT5 KPI(MT5 핵심 성과 지표)는 없다.",
            "- The unchanged s264_lc/s264_aia controls(변경 없는 s264_lc/s264_aia 대조군)는 control_holdout_receipt(대조 보류 영수증)로 남겼다.",
            "- s262_lih/s258_stc guardrails(가드레일)는 q01 active batch(q01 활성 묶음)에 포함되지만 선택 후보 주장에는 쓰지 않는다.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_queue(원천 대기열): `{rel(SOURCE_QUEUE_PATH)}`",
            f"- source_variant_manifest(원천 변형 목록): `{rel(SOURCE_VARIANT_MANIFEST_PATH)}`",
            f"- source_attempt_manifest(원천 시도 목록): `{rel(SOURCE_ATTEMPT_MANIFEST_PATH)}`",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    pairs = [
        ("stage267_run267CN_source_queue", "source_queue", SOURCE_QUEUE_PATH, "Run267CM materialization queue."),
        ("stage267_run267CN_source_variant_manifest", "source_variant_manifest", SOURCE_VARIANT_MANIFEST_PATH, "Run267CF source variant manifest."),
        ("stage267_run267CN_source_attempt_manifest", "source_attempt_manifest", SOURCE_ATTEMPT_MANIFEST_PATH, "Run267CF source attempt manifest."),
        ("stage267_run267CN_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH, "Run267CN materialization plan."),
        ("stage267_run267CN_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Run267CN variant manifest."),
        ("stage267_run267CN_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267CN MT5 attempt manifest."),
        ("stage267_run267CN_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267CN runtime contract."),
        ("stage267_run267CN_control_holdout_receipt", "control_holdout_receipt", CONTROL_HOLDOUT_RECEIPT_PATH, "Run267CN control holdout receipt."),
        ("stage267_run267CN_guardrail_receipt", "guardrail_receipt", GUARDRAIL_RECEIPT_PATH, "Run267CN guardrail receipt."),
        ("stage267_run267CN_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267CN run manifest."),
        ("stage267_run267CN_lineage", "lineage", LINEAGE_PATH, "Run267CN artifact lineage."),
        ("stage267_run267CN_review_result", "review_result", REVIEW_RESULT_PATH, "Run267CN review result."),
        ("stage267_run267CN_report", "report", REPORT_PATH, "Run267CN materialization report."),
        ("stage267_run267CN_producer", "producer_script", PRODUCER_PATH, "Run267CN producer script."),
    ]
    rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, notes in pairs:
        full_path = repo_path(str(path))
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(full_path) if path_exists(full_path) else "",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": f"{notes} artifact(산출물).",
        }
    )
    for row in result["variant_manifest"]:
        for kind, key in (("runtime_feature", "runtime_feature_file"), ("runtime_model", "runtime_model_file")):
            path = repo_path(str(row[key]))
            rows.append(
                {
                    "artifact_id": f"stage267_run267CN_{kind}_{safe_token(row['variant_id'])}",
                    "artifact_type": kind,
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created_at,
                    "notes": f"{row['variant_id']} {kind}(런타임 산출물).",
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
        f"- run267CN_summary(267CN 요약): Run267CN(267CN 실행)은 run267CM(267CM 실행)의 공유 약점 돌파 큐를 "
        f"variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, "
        f"control receipts(대조 영수증) `{counts['control_receipts']}`개, guardrail receipts(가드레일 영수증) `{counts['guardrail_receipts']}`개로 물질화했다. "
        "Effect(효과): 다음 run267CO(267CO 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 곡선/약점 구간/거래 품질을 검증할 수 있다."
    )
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(
        current,
        "- adapter_under_review(검토 중 어댑터):",
        "- adapter_under_review(검토 중 어댑터): `pool_wide_shared_weakness_breakout_materialization`",
    )
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_after_contains(current, "run267CM_summary", summary_line)
    current = append_after_contains(
        current,
        "stage267_run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design.md",
        f"- run267CN_pool_wide_shared_weakness_breakout_materialization(267CN 공유 약점 돌파 물질화): `{rel(REPORT_PATH)}`",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selected = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_after_contains(selected, "run267CM_summary", summary_line)
    selected = append_after_contains(
        selected,
        "stage267_run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design.md",
        f"- run267CN_pool_wide_shared_weakness_breakout_materialization(267CN 공유 약점 돌파 물질화): `{rel(REPORT_PATH)}`",
    )
    write_md(SELECTION_STATUS_PATH, selected)

    focus_block = (
        "- >-\n"
        f"  Stage267(267단계) run267CN(267CN 실행) pool-wide shared weakness breakout materialization"
        f"(후보군 전체 공유 약점 돌파 물질화) `{STATUS}`. Effect(효과): run267CM(267CM 실행)의 "
        f"materialization queue(물질화 대기열)를 variants(변형) `{counts['variants']}`개와 attempts(시도) `{counts['attempts']}`개로 만들고, "
        "s264_lc/s264_aia control(대조)과 s262_lih/s258_stc guardrail(가드레일)을 영수증으로 연결했다. "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = prepend_current_focus(workspace, focus_block)
    workspace = workspace.replace(
        "  next_action: run267CN_materialize_pool_wide_shared_weakness_breakout_queue",
        f"  next_action: {NEXT_ACTION}",
        1,
    )
    workspace = append_after_contains(
        workspace,
        "run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design_report_path",
        f"  run267CN_pool_wide_shared_weakness_breakout_materialization_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)

    index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    index = append_after_contains(
        index,
        "run267CM_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design",
        f"- run267CN_pool_wide_shared_weakness_breakout_materialization(267CN 후보군 전체 공유 약점 돌파 물질화): `{rel(REPORT_PATH)}`",
    )
    block = (
        "\nRun267CN(267CN 실행)는 run267CM(267CM 실행)의 P0 공유 약점/공격형 재진입 큐를 MT5(MetaTrader 5, 메타트레이더5) 입력으로 물질화했다.\n"
        f"Effect(효과): variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, "
        f"control receipts(대조 영수증) `{counts['control_receipts']}`개, guardrail receipts(가드레일 영수증) `{counts['guardrail_receipts']}`개를 남기고 "
        f"다음 행동을 `{NEXT_ACTION}`으로 고정했다.\n"
        "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.\n"
    )
    if "Run267CN(267CN 실행)는" not in index:
        index = index.rstrip() + "\n" + block
    write_md(REVIEW_INDEX_PATH, index)


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    notes = (
        f"variants={counts['variants']};attempts={counts['attempts']};"
        f"controls={counts['control_receipts']};guardrails={counts['guardrail_receipts']};"
        f"next_action={NEXT_ACTION};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267CN_pool_wide_shared_weakness_breakout_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "pool_wide_shared_weakness_breakout_materialization",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B P0 attempt inputs; true Tier B fallback blocked",
        "scoreboard": "feature_model_set_ini_materialization_control_guardrail_receipts",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_mt5_kpi_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_pool_wide_shared_weakness_breakout_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__pool_wide_shared_weakness_breakout_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pool_wide_shared_weakness_breakout_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "pool_wide_shared_weakness_breakout_materialization",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B P0 attempt inputs; true Tier B fallback blocked",
        "kpi_scope": "feature_model_set_ini_materialization_no_mt5_kpi",
        "scoreboard_lane": "shared_weakness_breakout_materialization",
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
