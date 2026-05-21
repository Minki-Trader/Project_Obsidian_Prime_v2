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
from foundation.models.ebm_score_table import FIELDNAMES
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import (
    run267CF_pool_wide_orthogonal_loss_shape_state_materialization as source_materialization,
)
from stage_pipelines.stage267 import (
    run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267CJ"
RUN_ID = "run267CJ_stage267_pool_wide_orthogonal_loss_shape_state_followup_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_materialization.RUN_ID
STATUS = "run267CJ_pool_wide_orthogonal_loss_shape_state_followup_materialized_execution_pending"
JUDGMENT = "orthogonal_loss_shape_state_followup_materialized_no_candidate_selection"
NEXT_ACTION = "run267CK_execute_pool_wide_orthogonal_loss_shape_state_followup_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_orthogonal_loss_shape_state_followup_materialization"
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
SOURCE_NEGATIVE_SLICE_PATH = source_design.SOURCE_NEGATIVE_SLICE_PATH

QUEUE_DECISION_PATH = RUN_ROOT / "queue_decision.csv"
SOURCE_REPRODUCTION_RECEIPT_PATH = RUN_ROOT / "source_profile_reproduction_receipt.csv"
FEATURE_FRAME_MANIFEST_PATH = RUN_ROOT / "feature_frame_manifest.csv"
MODEL_MANIFEST_PATH = RUN_ROOT / "model_manifest.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
HELD_QUEUE_PATH = RUN_ROOT / "held_queue.csv"
STATE_ATTRIBUTION_SEED_PATH = RUN_ROOT / "state_attribution_seed.csv"
STRESS_COMPARATOR_RECEIPT_PATH = RUN_ROOT / "stress_comparator_receipt.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CJ_pool_wide_orthogonal_loss_shape_state_followup_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CJ_pool_wide_orthogonal_loss_shape_state_followup_materialization.py")

STAGE_LEDGER_PATH = source_design.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_design.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_design.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_design.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_design.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_design.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_design.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_design.REVIEW_INDEX_PATH

COMMON_ROOT = "OPV2/s267cj/run267CJ_orthogonal_followup"
EXPLORATION_LABEL = "stage267_BaselineRacing__OrthogonalLossShapeStateFollowup"
PERIOD_LABEL = "historical_2024_tier_a_train_era_stress"
TIER_PAIR_BOUNDARY = (
    "Tier A and duplicate-boundary Tier A+B inputs are materialized; true Tier B fallback "
    "and actual routed total remain outside this run"
)
MATERIALIZATION_BOUNDARY = (
    "materialization_only_no_candidate_selection_no_selected_research_baseline_no_onnx"
)

P0_QUEUE_CONFIG: dict[str, dict[str, Any]] = {
    "run267cj_q01_s264_lc_impulse_dd_constrained_state": {
        "alias": "s264_lc",
        "source_profile": "similar_replacement_impulse",
        "variant_token": "impulse_dd_state_throttle",
        "engineered_feature": "stage267cj_impulse_dd_state_throttle_score",
        "mode": "controlled_impulse_dd_state_throttle",
        "model_strength": "moderate_flat_bias_when_noncalendar_loss_state_is_high",
        "attempt_suffix": "state_throttle",
    },
    "run267cj_q02_s264_aia_oos_anchor_impulse_pressure": {
        "alias": "s264_aia",
        "source_profile": "similar_replacement_impulse",
        "variant_token": "oos_anchor_impulse_pressure",
        "engineered_feature": "stage267cj_oos_anchor_impulse_pressure_score",
        "mode": "oos_anchor_impulse_pressure",
        "model_strength": "strong_flat_bias_when_impulse_dd_pressure_is_high",
        "attempt_suffix": "anchor_pressure",
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


def safe_token(value: Any, limit: int = 80) -> str:
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


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def split_semicolon(value: Any) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


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
    lines = ["; generated_by=run267CJ_pool_wide_orthogonal_loss_shape_state_followup_materialization"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "format": "mt5_set"}


def write_ini(path: Path, values: Mapping[str, Any]) -> dict[str, str]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["[Tester]"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "format": "mt5_tester_ini"}


def scale_series(series: pd.Series) -> tuple[pd.Series, dict[str, float]]:
    clean = pd.to_numeric(series, errors="coerce").astype("float64").replace([np.inf, -np.inf], np.nan)
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


def component(frame: pd.DataFrame, column: str, transform: str = "raw") -> pd.Series:
    if column not in frame.columns:
        raise KeyError(f"missing component column: {column}")
    series = pd.to_numeric(frame[column], errors="coerce").astype("float64")
    if transform == "raw":
        return series
    if transform == "abs":
        return series.abs()
    if transform == "abs_center_0_5":
        return (series - 0.5).abs()
    if transform == "abs_center_1":
        return (series - 1.0).abs()
    raise ValueError(f"unknown transform: {transform}")


def loss_cluster_proxy(frame: pd.DataFrame) -> pd.Series:
    if "log_return_1" not in frame.columns:
        return pd.Series(0.0, index=frame.index)
    returns = pd.to_numeric(frame["log_return_1"], errors="coerce").astype("float64").fillna(0.0)
    negative_frequency = (returns < 0.0).astype("float64").rolling(24, min_periods=1).mean()
    magnitude_scaled, _ = scale_series(returns.abs())
    return (0.65 * negative_frequency + 0.35 * magnitude_scaled).clip(0.0, 1.0)


def compute_followup_feature(frame: pd.DataFrame, *, mode: str) -> tuple[pd.Series, list[dict[str, Any]]]:
    components: list[tuple[str, pd.Series, float]] = []
    shock_a, qa = scale_series(component(frame, "return_zscore_20", "abs"))
    shock_b, qb = scale_series(component(frame, "return_1_over_atr_14", "abs"))
    vol_a, qv_a = scale_series(component(frame, "atr_14_over_atr_50", "raw"))
    vol_b, qv_b = scale_series(component(frame, "historical_vol_5_over_20", "raw"))
    range_a, qr_a = scale_series(component(frame, "gap_percent", "abs"))
    range_b, qr_b = scale_series(component(frame, "bb_position_20", "abs_center_0_5"))
    cluster = loss_cluster_proxy(frame)
    components.extend(
        [
            ("return_zscore_20_abs", shock_a, 0.20),
            ("return_1_over_atr_14_abs", shock_b, 0.20),
            ("atr_14_over_atr_50", vol_a, 0.16),
            ("historical_vol_5_over_20", vol_b, 0.14),
            ("gap_percent_abs", range_a, 0.12),
            ("bb_position_20_center_pressure", range_b, 0.08),
            ("rolling_negative_return_cluster_24", cluster, 0.10),
        ]
    )
    if mode == "oos_anchor_impulse_pressure":
        weights = {
            "return_zscore_20_abs": 0.18,
            "return_1_over_atr_14_abs": 0.22,
            "atr_14_over_atr_50": 0.18,
            "historical_vol_5_over_20": 0.16,
            "gap_percent_abs": 0.14,
            "bb_position_20_center_pressure": 0.06,
            "rolling_negative_return_cluster_24": 0.06,
        }
        components = [(name, series, weights[name]) for name, series, _ in components]
    score = sum(weight * series for name, series, weight in components)
    quantiles_by_name = {
        "return_zscore_20_abs": qa,
        "return_1_over_atr_14_abs": qb,
        "atr_14_over_atr_50": qv_a,
        "historical_vol_5_over_20": qv_b,
        "gap_percent_abs": qr_a,
        "bb_position_20_center_pressure": qr_b,
        "rolling_negative_return_cluster_24": {
            "q25": float(cluster.quantile(0.25)),
            "q50": float(cluster.quantile(0.50)),
            "q75": float(cluster.quantile(0.75)),
        },
    }
    diagnostics = [
        {
            "source_component": name,
            "weight": weight,
            "q25": quantiles_by_name[name]["q25"],
            "q50": quantiles_by_name[name]["q50"],
            "q75": quantiles_by_name[name]["q75"],
            "transform": "scaled_noncalendar_bar_state",
        }
        for name, _, weight in components
    ]
    return score.clip(0.0, 1.0).astype("float64"), diagnostics


def score_rows_for_mode(mode: str, feature_index: int) -> list[dict[str, Any]]:
    cuts = [0.25, 0.50, 0.75]
    if mode == "oos_anchor_impulse_pressure":
        scores = [
            (0.0, 0.0, 0.0),
            (-0.020, 0.040, -0.020),
            (-0.060, 0.120, -0.060),
            (-0.120, 0.240, -0.120),
            (-0.180, 0.360, -0.180),
        ]
    else:
        scores = [
            (0.0, 0.0, 0.0),
            (-0.015, 0.030, -0.015),
            (-0.045, 0.090, -0.045),
            (-0.090, 0.180, -0.090),
            (-0.140, 0.280, -0.140),
        ]
    rows: list[dict[str, Any]] = []
    for index, value in enumerate(cuts):
        rows.append(
            {
                "record_type": "cut",
                "feature_index": feature_index,
                "item_index": index,
                "value": value,
                "score_short": "",
                "score_flat": "",
                "score_long": "",
            }
        )
    for index, (score_short, score_flat, score_long) in enumerate(scores):
        rows.append(
            {
                "record_type": "score",
                "feature_index": feature_index,
                "item_index": index,
                "value": "",
                "score_short": score_short,
                "score_flat": score_flat,
                "score_long": score_long,
            }
        )
    return rows


def augment_model(source_model_path: Path, destination: Path, *, feature_index: int, mode: str) -> dict[str, Any]:
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    with io_path(source_model_path).open("r", encoding="utf-8-sig", newline="") as handle:
        source_rows = [dict(row) for row in csv.DictReader(handle)]
    output_rows = [*source_rows, *score_rows_for_mode(mode, feature_index)]
    with io_path(destination).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in output_rows:
            writer.writerow({field: cell(row.get(field)) for field in FIELDNAMES})
    return {
        "runtime_model_file": rel(destination),
        "runtime_model_sha256": sha256_file_lf_normalized(destination),
        "appended_feature_index": feature_index,
        "appended_model_rows": len(output_rows) - len(source_rows),
        "source_model_rows": len(source_rows),
        "model_rows": len(output_rows),
    }


def source_variants() -> list[dict[str, str]]:
    rows = read_csv(SOURCE_VARIANT_MANIFEST_PATH)
    if not rows:
        raise RuntimeError(f"missing source variant manifest: {rel(SOURCE_VARIANT_MANIFEST_PATH)}")
    return rows


def source_variant_for(alias: str, profile: str) -> dict[str, str]:
    for row in source_variants():
        if row.get("candidate_alias") == alias and row.get("profile_label") == profile:
            return row
    raise RuntimeError(f"missing source variant for {alias}/{profile}")


def source_attempts_by_variant_tier() -> dict[tuple[str, str], dict[str, str]]:
    rows = read_csv(SOURCE_ATTEMPT_MANIFEST_PATH)
    if not rows:
        raise RuntimeError(f"missing source attempt manifest: {rel(SOURCE_ATTEMPT_MANIFEST_PATH)}")
    return {(row["variant_id"], row["tier"]): row for row in rows if row.get("variant_id") and row.get("tier")}


def materializable_queue_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    return [dict(row) for row in queue_rows if str(row.get("queue_id")) in P0_QUEUE_CONFIG]


def held_queue_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        queue_id = str(row.get("queue_id"))
        if queue_id in P0_QUEUE_CONFIG:
            continue
        if queue_id == "run267cj_q04_monday_noncalendar_state_attribution":
            decision = "analysis_seed_created_no_mt5_attempt"
            hold_reason = "state attribution(상태 귀속) must happen before another MT5(MetaTrader 5, 메타트레이더5) attempt(시도)"
        elif queue_id == "run267cj_q05_s258_stc_stress_comparator_receipt":
            decision = "prune_receipt_created_no_mt5_attempt"
            hold_reason = "s258_stc is stress comparator(압박 비교군) only in this branch(분기)"
        else:
            decision = "held_until_p0_execution_review"
            hold_reason = "P1 supply-lift(거래 공급 확장) waits for P0 execution(실행) and curve review(곡선 검토)"
        rows.append(
            {
                "queue_id": queue_id,
                "priority": row.get("priority"),
                "candidate_aliases": row.get("candidate_aliases"),
                "source_profile": row.get("source_profile"),
                "decision": decision,
                "hold_reason": hold_reason,
                "next_condition": NEXT_ACTION,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def materialize_variant(
    queue: Mapping[str, str],
    *,
    source_attempts: Mapping[tuple[str, str], Mapping[str, str]],
    order: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    config = P0_QUEUE_CONFIG[str(queue["queue_id"])]
    alias = str(config["alias"])
    source_variant = source_variant_for(alias, str(config["source_profile"]))
    source_feature_path = repo_path(source_variant["runtime_feature_file"])
    source_model_path = repo_path(source_variant["runtime_model_file"])
    for path in (source_feature_path, source_model_path):
        if not path_exists(path):
            raise FileNotFoundError(rel(path))

    base_feature_order = split_semicolon(source_variant["feature_order"])
    engineered_feature = str(config["engineered_feature"])
    feature_order = [*base_feature_order, engineered_feature]
    feature_order_hash = ordered_hash(feature_order)
    variant_id = f"run267cj_{order:02d}_{alias}_{config['variant_token']}"
    runtime_feature_path = FEATURE_ROOT / alias / variant_id / f"{variant_id}_features.csv"
    runtime_model_path = VARIANT_ROOT / alias / variant_id / "models" / f"{variant_id}_model.csv"

    frame = pd.read_csv(io_path(source_feature_path), encoding="utf-8-sig")
    frame[engineered_feature], diagnostic_rows = compute_followup_feature(frame, mode=str(config["mode"]))
    write_runtime_csv(runtime_feature_path, frame, ["bar_time_server", *feature_order])
    model_meta = augment_model(
        source_model_path,
        runtime_model_path,
        feature_index=len(base_feature_order),
        mode=str(config["mode"]),
    )
    validation = source_materialization.validate_score_table(runtime_feature_path, runtime_model_path, feature_order)

    common_root = f"{COMMON_ROOT}/{alias}/{variant_id}"
    common_feature_path = f"{common_root}/features/{runtime_feature_path.name}"
    common_model_path = f"{common_root}/models/{runtime_model_path.name}"
    common_feature = copy_to_common(runtime_feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(runtime_model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    feature_row = {
        "variant_id": variant_id,
        "queue_id": queue["queue_id"],
        "candidate_alias": alias,
        "candidate_id": source_variant.get("candidate_id"),
        "candidate_role": source_variant.get("candidate_role"),
        "source_variant_id": source_variant["variant_id"],
        "source_feature_file": rel(source_feature_path),
        "source_feature_sha256": sha256_file_lf_normalized(source_feature_path),
        "runtime_feature_file": rel(runtime_feature_path),
        "runtime_feature_sha256": sha256_file_lf_normalized(runtime_feature_path),
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "source_feature_count": len(base_feature_order),
        "feature_count": len(feature_order),
        "feature_order": feature_order,
        "feature_order_hash": feature_order_hash,
        "appended_feature": engineered_feature,
        "feature_mode": config["mode"],
        "feature_min": float(frame[engineered_feature].min()) if len(frame) else 0.0,
        "feature_max": float(frame[engineered_feature].max()) if len(frame) else 0.0,
        "feature_mean": float(frame[engineered_feature].mean()) if len(frame) else 0.0,
        "feature_nonzero_rows": int((frame[engineered_feature] > 0).sum()) if len(frame) else 0,
        "rows": int(len(frame)),
        "first_bar_time_server": str(frame["bar_time_server"].iloc[0]) if len(frame) else "",
        "last_bar_time_server": str(frame["bar_time_server"].iloc[-1]) if len(frame) else "",
        "duplicate_bar_time_rows": int(frame["bar_time_server"].duplicated().sum()) if len(frame) else 0,
        "runtime_missing_feature_cells": int(frame.loc[:, feature_order].isna().sum().sum()) if len(frame) else 0,
        **validation,
        "materialization_status": "materialized_execution_pending",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_row = {
        "variant_id": variant_id,
        "queue_id": queue["queue_id"],
        "candidate_alias": alias,
        "source_model_file": rel(source_model_path),
        "source_model_sha256": sha256_file_lf_normalized(source_model_path),
        "runtime_model_file": model_meta["runtime_model_file"],
        "runtime_model_sha256": model_meta["runtime_model_sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "appended_feature": engineered_feature,
        "model_strength": config["model_strength"],
        "appended_model_rows": model_meta["appended_model_rows"],
        "model_rows": model_meta["model_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    variant_row = {
        "variant_id": variant_id,
        "queue_id": queue["queue_id"],
        "source_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "source_variant_id": source_variant["variant_id"],
        "candidate_id": source_variant.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": source_variant.get("candidate_role"),
        "profile_label": config["mode"],
        "source_profile_label": source_variant.get("profile_label"),
        "model_materialization_type": "augmented_run267CF_score_table_with_noncalendar_loss_state_pressure",
        "runtime_model_file": model_row["runtime_model_file"],
        "runtime_model_sha256": model_row["runtime_model_sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "runtime_feature_file": feature_row["runtime_feature_file"],
        "runtime_feature_sha256": feature_row["runtime_feature_sha256"],
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "feature_count": len(feature_order),
        "feature_order": feature_order,
        "feature_order_hash": feature_order_hash,
        "engineered_features": engineered_feature,
        "changed_variables": queue.get("changed_variables"),
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    attempt_rows: list[dict[str, Any]] = []
    reproduction_rows: list[dict[str, Any]] = []
    for tier_index, (tier, attempt_role, tier_token) in enumerate(
        (
            ("Tier A", "tier_only_total", "ta"),
            ("Tier A+B", "routed_total_duplicate_boundary", "rt"),
        ),
        start=1,
    ):
        source_attempt = dict(source_attempts[(source_variant["variant_id"], tier)])
        source_set_path = repo_path(source_attempt["set_path"])
        source_ini_path = repo_path(source_attempt["ini_path"])
        source_set_values = parse_key_values(source_set_path)
        source_ini_values = parse_key_values(source_ini_path)
        attempt_name = f"{variant_id}_{tier_token}_2024"
        telemetry = f"{common_root}/telemetry/{attempt_name}_telemetry.csv"
        summary = f"{common_root}/telemetry/{attempt_name}_summary.csv"
        set_values = dict(source_set_values)
        model_id = f"{RUN_ID}_{variant_id}_score_table"
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
                "InpMagic": 26736000 + order * 10 + tier_index,
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
                "queue_id": queue["queue_id"],
                "source_variant_id": source_variant["variant_id"],
                "source_attempt_name": source_attempt["attempt_name"],
                "candidate_id": source_variant.get("candidate_id"),
                "candidate_alias": alias,
                "candidate_role": source_variant.get("candidate_role"),
                "profile_label": config["mode"],
                "tier": tier,
                "attempt_role": attempt_role,
                "record_view_prefix": f"mt5_{tier_token}_{alias}_{config['attempt_suffix']}",
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
                "queue_id": queue["queue_id"],
                "candidate_alias": alias,
                "source_profile_label": source_variant.get("profile_label"),
                "source_variant_id": source_variant["variant_id"],
                "source_attempt_name": source_attempt["attempt_name"],
                "tier": tier,
                "source_set_path": source_attempt["set_path"],
                "source_ini_path": source_attempt["ini_path"],
                "source_feature_file": rel(source_feature_path),
                "source_model_file": rel(source_model_path),
                "reproduction_status": "source_profile_reuse_receipt_no_new_source_attempt",
                "effect": "source profile is kept as comparison reference for the modified run267CJ variant",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    diagnostic_rows = [
        {
            "variant_id": variant_id,
            "queue_id": queue["queue_id"],
            "candidate_alias": alias,
            "engineered_feature": engineered_feature,
            **row,
        }
        for row in diagnostic_rows
    ]
    return variant_row, attempt_rows, feature_row, model_row, source_variant, diagnostic_rows, reproduction_rows


def queue_decision_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        queue_id = str(row.get("queue_id"))
        if queue_id in P0_QUEUE_CONFIG:
            decision = "materialized_execution_pending"
            effect = "P0 feature/model/set/ini(피처/모델/설정/초기화) inputs(입력)이 next MT5 batch(다음 MT5 묶음) 준비 상태다"
        elif queue_id == "run267cj_q04_monday_noncalendar_state_attribution":
            decision = "analysis_seed_created_no_mt5_attempt"
            effect = "weak Monday rows(약한 월요일 행)를 calendar rule(달력 규칙) 전에 state attribution seed(상태 귀속 씨앗)로 바꿨다"
        elif queue_id == "run267cj_q05_s258_stc_stress_comparator_receipt":
            decision = "stress_comparator_prune_receipt_no_mt5_attempt"
            effect = "s258_stc를 repair loop(수리 반복) 없이 stress comparator(압박 비교군)로 기록했다"
        else:
            decision = "held_until_p0_execution_review"
            effect = "P1 supply-lift pool(거래 공급 확장 묶음)은 P0 curve/trade-quality evidence(P0 곡선/거래 품질 근거) 뒤로 보류했다"
        rows.append(
            {
                "queue_id": queue_id,
                "priority": row.get("priority"),
                "workstream": row.get("workstream"),
                "candidate_aliases": row.get("candidate_aliases"),
                "source_profile": row.get("source_profile"),
                "run267CJ_decision": decision,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def state_attribution_seed_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    seed_queue = next((row for row in queue_rows if row.get("queue_id") == "run267cj_q04_monday_noncalendar_state_attribution"), {})
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    monday_rows = [row for row in negative_rows if row.get("axis") == "weekday" and row.get("bucket") == "Monday"]
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(monday_rows, start=1):
        rows.append(
            {
                "seed_id": f"run267cj_state_attr_{index:02d}",
                "source_queue_id": seed_queue.get("queue_id", "run267cj_q04_monday_noncalendar_state_attribution"),
                "candidate_alias": row.get("candidate_alias"),
                "profile_label": row.get("profile_label") or row.get("test_id"),
                "axis": row.get("axis"),
                "bucket": row.get("bucket"),
                "net_profit": row.get("net_profit"),
                "trade_count": row.get("trade_count"),
                "source_negative_slice_path": rel(SOURCE_NEGATIVE_SLICE_PATH),
                "analysis_status": "seed_only_no_mt5_attempt",
                "next_join_target": "trade_records_plus_upstream_feature_state_surface",
                "noncalendar_boundary": "weekday is treated as symptom label, not permission filter",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if not rows:
        rows.append(
            {
                "seed_id": "run267cj_state_attr_no_monday_rows",
                "source_queue_id": seed_queue.get("queue_id", "run267cj_q04_monday_noncalendar_state_attribution"),
                "candidate_alias": "none",
                "profile_label": "none",
                "axis": "weekday",
                "bucket": "Monday",
                "net_profit": "",
                "trade_count": "",
                "source_negative_slice_path": rel(SOURCE_NEGATIVE_SLICE_PATH),
                "analysis_status": "blocked_missing_monday_negative_slice",
                "next_join_target": "inspect_run267CH_negative_slice_schema",
                "noncalendar_boundary": "no calendar-only rule",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def stress_comparator_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    source = next((row for row in queue_rows if row.get("queue_id") == "run267cj_q05_s258_stc_stress_comparator_receipt"), {})
    return [
        {
            "receipt_id": "run267cj_s258_stc_stress_comparator_prune_receipt",
            "source_queue_id": source.get("queue_id", "run267cj_q05_s258_stc_stress_comparator_receipt"),
            "candidate_alias": "s258_stc",
            "role": "stress_comparator_only",
            "decision": "no_mt5_attempt_no_deep_repair_in_run267CJ",
            "why": "run267CI records high headline net(대표 순수익) but uncomfortable DD(drawdown, 손실폭) and Monday loss(월요일 손실)",
            "reopen_condition": "different non-calendar structure(비달력 구조)가 DD(drawdown, 손실폭)를 trade-count collapse(거래 수 붕괴) 없이 낮출 때",
            "effect": "stress evidence(압박 근거)를 보존하면서 repair-loop depth(수리 반복 깊이)를 제한한다",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def experiment_design_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": f"run267cj_{safe_token(row.get('queue_id'))}",
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
            "evidence_plan": row.get("evidence_plan"),
        }
        for row in queue_rows
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    duplicate_rows = sum(as_int(row.get("duplicate_bar_time_rows")) for row in feature_rows)
    missing_cells = sum(as_int(row.get("runtime_missing_feature_cells")) for row in feature_rows)
    return [
        {
            "check_id": "run267cj_runtime_feature_frames",
            "status": "passed" if duplicate_rows == 0 and missing_cells == 0 else "warning",
            "evidence": f"feature_frames={len(feature_rows)};duplicate_bar_time_rows={duplicate_rows};runtime_missing_feature_cells={missing_cells}",
            "effect": "MT5 handoff inputs have timestamp and feature completeness checks before execution",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def runtime_parity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267cj_python_score_table_smoke",
            "status": "passed",
            "evidence": f"feature_frames={len(feature_rows)};score_table_validation=passed",
            "effect": "Python score-table loader accepts the augmented feature order",
            "claim_boundary": "handoff_contract_only_no_runtime_parity_claim",
        },
        {
            "check_id": "run267cj_true_tier_b_fallback",
            "status": "blocked_by_scope",
            "evidence": TIER_PAIR_BOUNDARY,
            "effect": "true fallback and actual routed total remain future evidence, not hidden robustness proof",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def result_judgment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": (
                f"queue_rows={counts['queue_rows']};materialized_attempts={counts['attempts']};"
                f"held_rows={counts['held_rows']};state_attribution_seed_rows={counts['state_attribution_seed_rows']};"
                f"stress_receipts={counts['stress_receipts']}"
            ),
            "evidence_missing": "MT5 reports, KPI, trade records, balance/equity curve, time-slice KPI, Adapter package, ONNX parity",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이번 실행은 후보를 고른 것이 아니라, P0 두 후보를 바로 깨뜨려 볼 입력으로 만든 것이다.",
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "source_queue_present",
            "status": "passed" if counts["queue_rows"] == 5 else "warning",
            "evidence": f"queue_rows={counts['queue_rows']}",
            "effect": "run267CI queue(대기열)를 silently dropping rows(행 누락) 없이 소비했다",
        },
        {
            "gate_id": "p0_attempts_materialized",
            "status": "passed" if counts["attempts"] == 4 else "failed",
            "evidence": f"attempts={counts['attempts']};variants={counts['variants']}",
            "effect": "two P0 variants(P0 변형 2개)에 Tier A(티어 A)와 duplicate-boundary Tier A+B(중복 경계 티어 A+B) inputs(입력)가 있다",
        },
        {
            "gate_id": "held_or_receipt_rows_preserved",
            "status": "passed" if counts["held_rows"] == 3 else "warning",
            "evidence": f"held_rows={counts['held_rows']};state_seed_rows={counts['state_attribution_seed_rows']};stress_receipts={counts['stress_receipts']}",
            "effect": "P1/P2 rows(P1/P2 행)를 hidden MT5 attempts(숨은 MT5 시도)로 바꾸지 않았다",
        },
        {
            "gate_id": "score_table_validation",
            "status": "passed",
            "evidence": "all materialized feature/model rows passed probability smoke check",
            "effect": "invalid feature/model ordering(무효 피처/모델 순서)을 tester batch(테스터 묶음) 전에 차단했다",
        },
        {
            "gate_id": "claim_boundary_preserved",
            "status": "passed",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "materialization(물질화)이 candidate selection(후보 선택)으로 바뀌지 않게 했다",
        },
    ]


def runtime_contract_rows(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "variant_id": row["variant_id"],
            "candidate_alias": row["candidate_alias"],
            "feature_count": row["feature_count"],
            "feature_order_hash": row["feature_order_hash"],
            "model_backend": "ebm_table",
            "model_materialization_type": row["model_materialization_type"],
            "runtime_feature_file": row["runtime_feature_file"],
            "runtime_model_file": row["runtime_model_file"],
            "common_feature_path": row["common_feature_path"],
            "common_model_path": row["common_model_path"],
            "tier_pair_boundary": TIER_PAIR_BOUNDARY,
            "runtime_claim_boundary": CLAIM_BOUNDARY,
        }
        for row in variant_rows
    ]


def build_result() -> dict[str, Any]:
    created_at = utc_now()
    required = [
        SOURCE_QUEUE_PATH,
        SOURCE_BRANCH_DECISION_PATH,
        SOURCE_PRUNE_MATRIX_PATH,
        SOURCE_REVIEW_RESULT_PATH,
        SOURCE_VARIANT_MANIFEST_PATH,
        SOURCE_ATTEMPT_MANIFEST_PATH,
        SOURCE_RUNTIME_CONTRACT_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))

    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    source_attempts = source_attempts_by_variant_tier()
    material_rows = materializable_queue_rows(queue_rows)
    held_rows = held_queue_rows(queue_rows)
    variant_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    diagnostic_rows: list[dict[str, Any]] = []
    reproduction_rows: list[dict[str, Any]] = []
    for order, row in enumerate(material_rows, start=1):
        variant, attempts, feature, model, _source_variant, diagnostics, reproduction = materialize_variant(
            row,
            source_attempts=source_attempts,
            order=order,
        )
        variant_rows.append(variant)
        attempt_rows.extend(attempts)
        feature_rows.append(feature)
        model_rows.append(model)
        diagnostic_rows.extend(diagnostics)
        reproduction_rows.extend(reproduction)

    state_seed_rows = state_attribution_seed_rows(queue_rows)
    stress_rows = stress_comparator_rows(queue_rows)
    queue_decisions = queue_decision_rows(queue_rows)
    counts = {
        "queue_rows": len(queue_rows),
        "materialized_queue_rows": len(material_rows),
        "held_rows": len(held_rows),
        "variants": len(variant_rows),
        "attempts": len(attempt_rows),
        "feature_frames": len(feature_rows),
        "models": len(model_rows),
        "diagnostics": len(diagnostic_rows),
        "source_reproduction_receipts": len(reproduction_rows),
        "state_attribution_seed_rows": len(state_seed_rows),
        "stress_receipts": len(stress_rows),
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
        "queue_decisions": queue_decisions,
        "source_profile_reproduction_receipt": reproduction_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "feature_engineering_diagnostics": diagnostic_rows,
        "runtime_contract": runtime_contract_rows(variant_rows),
        "held_queue": held_rows,
        "state_attribution_seed": state_seed_rows,
        "stress_comparator_receipt": stress_rows,
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
            "source_negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
            "producer": rel(PRODUCER_PATH),
        },
        "outputs": {
            "queue_decision": rel(QUEUE_DECISION_PATH),
            "source_profile_reproduction_receipt": rel(SOURCE_REPRODUCTION_RECEIPT_PATH),
            "feature_frame_manifest": rel(FEATURE_FRAME_MANIFEST_PATH),
            "model_manifest": rel(MODEL_MANIFEST_PATH),
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "held_queue": rel(HELD_QUEUE_PATH),
            "state_attribution_seed": rel(STATE_ATTRIBUTION_SEED_PATH),
            "stress_comparator_receipt": rel(STRESS_COMPARATOR_RECEIPT_PATH),
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
    write_csv(QUEUE_DECISION_PATH, result["queue_decisions"])
    write_csv(SOURCE_REPRODUCTION_RECEIPT_PATH, result["source_profile_reproduction_receipt"])
    write_csv(FEATURE_FRAME_MANIFEST_PATH, result["feature_frame_manifest"])
    write_csv(MODEL_MANIFEST_PATH, result["model_manifest"])
    write_csv(VARIANT_MANIFEST_PATH, result["variant_manifest"])
    write_csv(ATTEMPT_MANIFEST_PATH, result["attempt_manifest"])
    write_csv(RUNTIME_CONTRACT_PATH, result["runtime_contract"])
    write_csv(HELD_QUEUE_PATH, result["held_queue"])
    write_csv(STATE_ATTRIBUTION_SEED_PATH, result["state_attribution_seed"])
    write_csv(STRESS_COMPARATOR_RECEIPT_PATH, result["stress_comparator_receipt"])
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
        "# Stage267 Run267CJ Follow-up Materialization(267단계 267CJ 후속 물질화)",
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
        f"- held_rows(보류 행): `{counts['held_rows']}`",
        f"- state_attribution_seed_rows(상태 귀속 씨앗 행): `{counts['state_attribution_seed_rows']}`",
        f"- stress_receipts(압박 영수증): `{counts['stress_receipts']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267CI(267CI 실행)의 P0 두 줄을 실제 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 만들었다.",
        "Effect(효과): `s264_lc`와 `s264_aia`를 다음 MT5(MetaTrader 5, 메타트레이더5) batch(묶음)에서 곧바로 깨뜨려 볼 수 있다.",
        "",
        "## Queue Decision(대기열 판단)",
        "",
        "| queue(대기열) | candidates(후보) | decision(판단) | effect(효과) |",
        "| --- | --- | --- | --- |",
    ]
    for row in result["queue_decisions"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['candidate_aliases']}` | `{row['run267CJ_decision']}` | {row['effect']} |"
        )
    lines.extend(
        [
            "",
            "## Attempt Inputs(시도 입력)",
            "",
            "| attempt(시도) | candidate(후보) | tier(티어) | feature_count(피처 수) | feature_hash(피처 해시) | status(상태) |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
    )
    feature_by_variant = {row["variant_id"]: row for row in result["feature_frame_manifest"]}
    for row in result["attempt_manifest"]:
        feature = feature_by_variant[row["variant_id"]]
        lines.append(
            f"| `{row['attempt_name']}` | `{row['candidate_alias']}` | `{row['tier']}` | "
            f"{feature['feature_count']} | `{feature['feature_order_hash']}` | `{row['execution_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- run267CJ(267CJ 실행)는 materialization-only(물질화 전용) 근거다.",
            "- MT5 execution(MT5 실행), KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표)는 아직 없다.",
            "- selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "- q04는 MT5 시도 대신 state attribution seed(상태 귀속 씨앗)로 남겼다. 효과는 weekday(요일)를 permission rule(허용 규칙)로 착각하지 않는 것이다.",
            "- q05는 stress comparator receipt(압박 비교 영수증)로 남겼다. 효과는 s258_stc(258 짧은 타이트 대조)를 깊은 repair loop(수리 반복)로 끌고 가지 않는 것이다.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source queue(원천 대기열): `{rel(SOURCE_QUEUE_PATH)}`",
            f"- source variant manifest(원천 변형 목록): `{rel(SOURCE_VARIANT_MANIFEST_PATH)}`",
            f"- source attempt manifest(원천 시도 목록): `{rel(SOURCE_ATTEMPT_MANIFEST_PATH)}`",
            f"- feature manifest(피처 목록): `{rel(FEATURE_FRAME_MANIFEST_PATH)}`",
            f"- model manifest(모델 목록): `{rel(MODEL_MANIFEST_PATH)}`",
            f"- attempt manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- runtime contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267CJ_producer", "producer_script", PRODUCER_PATH, "Builds run267CJ follow-up materialization."),
        ("stage267_run267CJ_source_queue", "source_queue", SOURCE_QUEUE_PATH, "Run267CI materialization queue."),
        ("stage267_run267CJ_source_variant_manifest", "source_variant_manifest", SOURCE_VARIANT_MANIFEST_PATH, "Run267CF source variant manifest."),
        ("stage267_run267CJ_source_attempt_manifest", "source_attempt_manifest", SOURCE_ATTEMPT_MANIFEST_PATH, "Run267CF source attempt manifest."),
        ("stage267_run267CJ_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Run267CJ queue decisions."),
        ("stage267_run267CJ_source_reproduction_receipt", "source_reproduction_receipt", SOURCE_REPRODUCTION_RECEIPT_PATH, "Run267CJ source profile reproduction receipt."),
        ("stage267_run267CJ_feature_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Run267CJ feature frame manifest."),
        ("stage267_run267CJ_model_manifest", "model_manifest", MODEL_MANIFEST_PATH, "Run267CJ model manifest."),
        ("stage267_run267CJ_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Run267CJ variant manifest."),
        ("stage267_run267CJ_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267CJ MT5 attempt manifest."),
        ("stage267_run267CJ_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267CJ runtime contract."),
        ("stage267_run267CJ_held_queue", "held_queue", HELD_QUEUE_PATH, "Run267CJ held queue."),
        ("stage267_run267CJ_state_attribution_seed", "state_attribution_seed", STATE_ATTRIBUTION_SEED_PATH, "Run267CJ state attribution seed."),
        ("stage267_run267CJ_stress_comparator_receipt", "stress_comparator_receipt", STRESS_COMPARATOR_RECEIPT_PATH, "Run267CJ stress comparator receipt."),
        ("stage267_run267CJ_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267CJ experiment design receipt."),
        ("stage267_run267CJ_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267CJ data integrity receipt."),
        ("stage267_run267CJ_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Run267CJ runtime handoff boundary receipt."),
        ("stage267_run267CJ_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267CJ result judgment."),
        ("stage267_run267CJ_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267CJ gate audit."),
        ("stage267_run267CJ_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267CJ run manifest."),
        ("stage267_run267CJ_lineage", "lineage", LINEAGE_PATH, "Run267CJ lineage."),
        ("stage267_run267CJ_review_result", "review_result", REVIEW_RESULT_PATH, "Run267CJ review result."),
        ("stage267_run267CJ_report", "review_report", REPORT_PATH, "Run267CJ report."),
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
    for row in result["feature_frame_manifest"]:
        feature_path = repo_path(str(row["runtime_feature_file"]))
        rows.append(
            {
                "artifact_id": f"stage267_run267CJ_feature_{safe_token(row['variant_id'], 72)}",
                "artifact_type": "runtime_feature_csv",
                "path": rel(feature_path),
                "sha256": sha256_file_lf_normalized(feature_path) if path_exists(feature_path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Runtime feature CSV for {row['variant_id']}.",
            }
        )
    for row in result["model_manifest"]:
        model_path = repo_path(str(row["runtime_model_file"]))
        rows.append(
            {
                "artifact_id": f"stage267_run267CJ_model_{safe_token(row['variant_id'], 72)}",
                "artifact_type": "runtime_model_csv",
                "path": rel(model_path),
                "sha256": sha256_file_lf_normalized(model_path) if path_exists(model_path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Runtime score-table model for {row['variant_id']}.",
            }
        )
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    stage_row = {
        "row_id": "stage267_run267CJ_pool_wide_orthogonal_loss_shape_state_followup_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "pool_wide_orthogonal_loss_shape_state_followup_materialization",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B P0 attempt inputs; true Tier B fallback blocked",
        "scoreboard": "feature_model_set_ini_materialization_no_mt5_kpi",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"variants={counts['variants']};attempts={counts['attempts']};held_rows={counts['held_rows']};next_action={NEXT_ACTION}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_orthogonal_loss_shape_state_followup_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"attempts={counts['attempts']};held_rows={counts['held_rows']};selected_candidate=none;onnx_readiness=not_claimed.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__pool_wide_orthogonal_loss_shape_state_followup_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pool_wide_orthogonal_loss_shape_state_followup_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B P0 attempt inputs; true fallback blocked",
        "kpi_scope": "feature_model_set_ini_materialization_no_trading_kpi",
        "scoreboard_lane": "orthogonal_loss_shape_state_followup_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={counts['variants']};attempts={counts['attempts']};held_rows={counts['held_rows']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
        [stage_row],
        key="row_id",
    )
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "subrun_id",
            "parent_run_id",
            "record_view",
            "tier_scope",
            "kpi_scope",
            "scoreboard_lane",
            "status",
            "judgment",
            "path",
            "primary_kpi",
            "guardrail_kpi",
            "external_verification_status",
            "notes",
        ),
        [project_row],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows(str(result["created_at_utc"]), result),
        key="artifact_id",
    )


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def update_current_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = f"- run267CJ_pool_wide_orthogonal_loss_shape_state_followup_materialization(267CJ 후보군 전체 직교 손실 형태/상태 후속 물질화): `{rel(REPORT_PATH)}`"
    summary_line = (
        "Run267CJ(267CJ 실행)는 run267CI(267CI 실행)의 materialization queue(물질화 대기열)를 "
        f"variants(변형) `{counts['variants']}`개와 attempts(시도) `{counts['attempts']}`개, "
        f"held rows(보류 행) `{counts['held_rows']}`개로 나눴다. Effect(효과): P0 두 후보는 다음 MT5(MetaTrader 5, 메타트레이더5) 실행 입력으로 준비했고, "
        "P1/P2는 분석 씨앗과 가지치기 영수증으로 남겨 repair loop(수리 반복)를 짧게 유지한다."
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_orthogonal_loss_shape_state_followup_materialization`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design.md", report_line)
            text = append_after_contains(text, "Run267CI(267CI 실행)는", summary_line)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design", report_line)
        else:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "stage267_run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design.md", report_line)
        write_md(path, text)

    focus_line = (
        "- >-\n"
        "  Stage267(267단계) run267CJ(267CJ 실행) pool-wide orthogonal loss-shape/state follow-up materialization"
        f"(후보군 전체 직교 손실 형태/상태 후속 물질화) `{STATUS}`. Effect(효과): run267CI(267CI 실행)의 대기열을 "
        f"variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개, "
        f"state attribution seed(상태 귀속 씨앗) `{counts['state_attribution_seed_rows']}`개로 나눴으며 selected candidate(선택 후보), "
        "selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_design.STATUS}", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {PARENT_RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {PARENT_RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace("  next_action: run267CJ_materialize_pool_wide_orthogonal_loss_shape_state_followup_queue", f"  next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design_report_path",
        f"  run267CJ_pool_wide_orthogonal_loss_shape_state_followup_materialization_report_path: {rel(REPORT_PATH)}",
    )
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_line + "\n", 1)
    write_md(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_current_docs(result)
    print(
        json.dumps(
            {
                "status": result["status"],
                "variants": result["counts"]["variants"],
                "attempts": result["counts"]["attempts"],
                "held_rows": result["counts"]["held_rows"],
                "state_attribution_seed_rows": result["counts"]["state_attribution_seed_rows"],
                "stress_receipts": result["counts"]["stress_receipts"],
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
