from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

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
    EA_TESTER_SET_NAME,
    copy_to_common,
)
from foundation.models.ebm_score_table import FIELDNAMES
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import (
    run267BS_pool_wide_directional_impulse_followup_materialization as score_table_tools,
)
from stage_pipelines.stage267 import (
    run267BW_aggressive_impulse_dd_shape_cross_period_materialization as source_materialization,
)
from stage_pipelines.stage267 import (
    run267BZ_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267CA"
RUN_ID = "run267CA_stage267_aggressive_impulse_dd_shape_followup_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_materialization.RUN_ID
STATUS = "run267CA_aggressive_impulse_dd_shape_followup_materialized_execution_pending"
JUDGMENT = "aggressive_impulse_dd_shape_followup_materialized_no_candidate_selection"
NEXT_ACTION = "run267CB_execute_aggressive_impulse_dd_shape_followup_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "aggressive_impulse_dd_shape_followup_materialization"
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

QUEUE_DECISION_PATH = RUN_ROOT / "queue_decision.csv"
SOURCE_REUSE_MANIFEST_PATH = RUN_ROOT / "source_reuse_manifest.csv"
CURVE_ZOOM_PLAN_PATH = RUN_ROOT / "curve_zoom_review_plan.csv"
FEATURE_FRAME_MANIFEST_PATH = RUN_ROOT / "feature_frame_manifest.csv"
MODEL_MANIFEST_PATH = RUN_ROOT / "model_manifest.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
FAILURE_MEMORY_SEED_PATH = RUN_ROOT / "failure_memory_seed.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CA_aggressive_impulse_dd_shape_followup_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CA_aggressive_impulse_dd_shape_followup_materialization.py")

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

COMMON_ROOT = "OPV2/s267ca/run267CA_dd_shape_followup"
TIER_PAIR_BOUNDARY = source_materialization.TIER_PAIR_BOUNDARY
MATERIALIZATION_BOUNDARY = "run267CA_clones_run267BW_2025h2_sources_and_appends_state_shaped_dd_guard"

PERIOD_BY_TARGET = {
    "2023H2": "adjacent_2023_h2_train_pre_2024",
    "2025H1": "adjacent_2025_h1_validation_post_2024",
    "2025H2": "adjacent_2025_h2_oos_followthrough",
}

GUARD_BY_QUEUE = {
    "run267bz_q01_s264_aih_2025h2_late_session_dd_shape_guard": {
        "mode": "late_session_dd_shape_guard",
        "feature": "stage267ca_late_session_dd_shape_guard_score",
        "attempt_suffix": "ddshape_guard",
        "model_strength": "moderate_flat_bias",
    },
    "run267bz_q02_s258_stc_2025h2_stress_dd_cap": {
        "mode": "stress_dd_cap",
        "feature": "stage267ca_stress_dd_cap_score",
        "attempt_suffix": "stress_ddcap",
        "model_strength": "strong_flat_bias",
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


def split_semicolon(value: Any) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


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
    lines = ["; generated_by=run267CA_aggressive_impulse_dd_shape_followup_materialization"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "format": "mt5_set"}


def write_ini(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["[Tester]"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path),
        "format": "mt5_tester_ini",
        "tester": dict(values),
    }


def source_variants() -> list[dict[str, str]]:
    rows = read_csv(SOURCE_VARIANT_MANIFEST_PATH)
    if not rows:
        raise RuntimeError(f"missing source variant manifest: {rel(SOURCE_VARIANT_MANIFEST_PATH)}")
    return rows


def source_attempts() -> dict[str, dict[str, str]]:
    rows = read_csv(SOURCE_ATTEMPT_MANIFEST_PATH)
    if not rows:
        raise RuntimeError(f"missing source attempt manifest: {rel(SOURCE_ATTEMPT_MANIFEST_PATH)}")
    return {str(row["variant_id"]): row for row in rows}


def source_variant_for(alias: str, target_period: str) -> dict[str, str]:
    for row in source_variants():
        if row.get("candidate_alias") == alias and row.get("target_period") == target_period:
            return row
    raise RuntimeError(f"missing run267BW source variant for {alias}/{target_period}")


def materializable_queue_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    return [dict(row) for row in queue_rows if str(row.get("queue_id")) in GUARD_BY_QUEUE]


def held_queue_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    return [dict(row) for row in queue_rows if str(row.get("queue_id")) not in GUARD_BY_QUEUE]


def compute_guard_feature(frame: pd.DataFrame, feature_order: Sequence[str], *, mode: str) -> pd.Series:
    parsed = pd.to_datetime(frame["bar_time_server"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    hour = parsed.dt.hour.fillna(-1).astype(int)
    late = hour.isin([20, 21, 22, 23]).astype(float)
    signal = pd.to_numeric(frame["stage56_context_et_event_signal"], errors="coerce").fillna(0.0).abs().clip(0.0, 1.0)
    rank_column = next((name for name in feature_order if "rank_bucket" in name), "")
    gate_column = next((name for name in feature_order if "_gate_" in name), "")
    rank = pd.to_numeric(frame[rank_column], errors="coerce").fillna(0.0) if rank_column else pd.Series(0.0, index=frame.index)
    rank_norm = (rank / max(float(rank.max()), 1.0)).clip(0.0, 1.0)
    gate = pd.to_numeric(frame[gate_column], errors="coerce").fillna(0.0).clip(0.0, 1.0) if gate_column else pd.Series(0.0, index=frame.index)
    gate_risk = (1.0 - gate).clip(0.0, 1.0)
    if mode == "stress_dd_cap":
        score = 0.62 * late * signal + 0.28 * late * gate_risk + 0.10 * late * rank_norm
    else:
        score = 0.52 * late * signal + 0.26 * late * gate_risk + 0.22 * late * rank_norm
    return score.clip(0.0, 1.0)


def score_rows_for_mode(mode: str, feature_index: int) -> list[dict[str, Any]]:
    cuts = [0.25, 0.55, 0.8]
    if mode == "stress_dd_cap":
        scores = [
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            (-0.06, 0.12, -0.06),
            (-0.14, 0.28, -0.14),
            (-0.22, 0.44, -0.22),
        ]
    else:
        scores = [
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            (-0.03, 0.06, -0.03),
            (-0.08, 0.16, -0.08),
            (-0.14, 0.28, -0.14),
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
    for index, (short_score, flat_score, long_score) in enumerate(scores):
        rows.append(
            {
                "record_type": "score",
                "feature_index": feature_index,
                "item_index": index,
                "value": "",
                "score_short": short_score,
                "score_flat": flat_score,
                "score_long": long_score,
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


def materialize_attempt(
    queue: Mapping[str, str],
    *,
    source_attempt_by_variant: Mapping[str, Mapping[str, str]],
    order: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    alias = str(queue["candidate_alias"])
    target_period = str(queue["target_period"])
    guard = GUARD_BY_QUEUE[str(queue["queue_id"])]
    source_variant = source_variant_for(alias, target_period)
    source_attempt = dict(source_attempt_by_variant[str(source_variant["variant_id"])])
    source_feature_path = repo_path(str(source_variant["runtime_feature_file"]))
    source_model_path = repo_path(str(source_variant["runtime_model_file"]))
    source_set_path = repo_path(str(source_attempt["set_path"]))
    source_ini_path = repo_path(str(source_attempt["ini_path"]))
    for path in (source_feature_path, source_model_path, source_set_path, source_ini_path):
        if not path_exists(path):
            raise FileNotFoundError(rel(path))

    base_feature_order = split_semicolon(source_variant["feature_order"])
    guard_feature = str(guard["feature"])
    feature_order = [*base_feature_order, guard_feature]
    feature_order_hash = ordered_hash(feature_order)
    period_token = safe_token(target_period, 16)
    suffix = safe_token(guard["attempt_suffix"], 24)
    attempt_name = f"run267ca_{order:02d}_{alias}_{period_token}_{suffix}"
    variant_id = f"{attempt_name}_variant"

    frame = pd.read_csv(io_path(source_feature_path), encoding="utf-8-sig")
    frame[guard_feature] = compute_guard_feature(frame, base_feature_order, mode=str(guard["mode"]))
    runtime_feature_path = FEATURE_ROOT / alias / period_token / f"{attempt_name}_features.csv"
    write_runtime_csv(runtime_feature_path, frame, ["bar_time_server", *feature_order])

    runtime_model_path = VARIANT_ROOT / alias / variant_id / "models" / f"{variant_id}_model.csv"
    model_meta = augment_model(
        source_model_path,
        runtime_model_path,
        feature_index=len(base_feature_order),
        mode=str(guard["mode"]),
    )
    validation = score_table_tools.validate_score_table(runtime_feature_path, runtime_model_path, feature_order)

    common_root = f"{COMMON_ROOT}/{alias}/{period_token}/{attempt_name}"
    common_feature_path = f"{common_root}/features/{runtime_feature_path.name}"
    common_model_path = f"{common_root}/models/{runtime_model_path.name}"
    common_feature = copy_to_common(runtime_feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(runtime_model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    set_values = parse_key_values(source_set_path)
    ini_values = parse_key_values(source_ini_path)
    telemetry = f"{common_root}/telemetry/{attempt_name}_telemetry.csv"
    summary = f"{common_root}/telemetry/{attempt_name}_summary.csv"
    report_name = f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}"
    magic = 26724000 + order
    next_set_values = dict(set_values)
    next_set_values.update(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": f"stage267_AggressiveImpulseDDShapeFollowup__{alias}_{period_token}",
            "InpTierLabel": input_probe.mt5.TIER_A,
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": source_attempt.get("split", target_period),
            "InpModelPath": common_model_path,
            "InpModelId": f"{RUN_ID}_{alias}_{period_token}_{suffix}",
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
            "InpFallbackUseOnPrimaryFlat": "false",
            "InpFallbackUseOnPrimaryLowConfidence": "false",
            "InpFallbackFeatureCsvPath": common_feature_path,
            "InpFallbackFeatureCount": len(feature_order),
            "InpFallbackModelPath": common_model_path,
            "InpFallbackModelId": f"{RUN_ID}_{alias}_{period_token}_{suffix}_fallback_disabled",
            "InpFallbackModelBackend": "ebm_table",
            "InpFallbackFeatureOrderHash": feature_order_hash,
            "InpTelemetryCsvPath": telemetry,
            "InpSummaryCsvPath": summary,
            "InpTelemetryUseCommonFiles": "true",
            "InpMagic": magic,
        }
    )
    set_payload = write_set(MT5_ROOT / f"{attempt_name}.set", next_set_values)
    next_ini_values = dict(ini_values)
    next_ini_values.update(
        {
            "Report": report_name,
            "ExpertParameters": EA_TESTER_SET_NAME,
            "ReplaceReport": 1,
            "ShutdownTerminal": 1,
        }
    )
    ini_payload = write_ini(MT5_ROOT / f"{attempt_name}.ini", next_ini_values)

    feature_row = {
        "attempt_name": attempt_name,
        "variant_id": variant_id,
        "queue_id": queue["queue_id"],
        "candidate_alias": alias,
        "candidate_id": queue.get("candidate_id"),
        "target_period": target_period,
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
        "appended_feature": guard_feature,
        "guard_mode": guard["mode"],
        "guard_min": float(frame[guard_feature].min()) if len(frame) else 0.0,
        "guard_max": float(frame[guard_feature].max()) if len(frame) else 0.0,
        "guard_mean": float(frame[guard_feature].mean()) if len(frame) else 0.0,
        "guard_nonzero_rows": int((frame[guard_feature] > 0).sum()) if len(frame) else 0,
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
        "attempt_name": attempt_name,
        "variant_id": variant_id,
        "queue_id": queue["queue_id"],
        "candidate_alias": alias,
        "target_period": target_period,
        "source_model_file": rel(source_model_path),
        "source_model_sha256": sha256_file_lf_normalized(source_model_path),
        "runtime_model_file": model_meta["runtime_model_file"],
        "runtime_model_sha256": model_meta["runtime_model_sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "appended_feature": guard_feature,
        "model_strength": guard["model_strength"],
        "appended_model_rows": model_meta["appended_model_rows"],
        "model_rows": model_meta["model_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    variant_row = {
        "variant_id": variant_id,
        "attempt_name": attempt_name,
        "queue_id": queue["queue_id"],
        "source_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "source_variant_id": source_variant["variant_id"],
        "candidate_id": queue.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": queue.get("candidate_role"),
        "profile_label": "aggressive_impulse_dd_shape_followup",
        "target_period": target_period,
        "period_id": source_variant.get("period_id"),
        "period_label": source_variant.get("period_label"),
        "model_materialization_type": "augmented_run267BW_score_table_with_state_shaped_dd_guard",
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
        "engineered_features": guard_feature,
        "changed_variables": queue.get("changed_variables"),
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    attempt_row = {
        "attempt_name": attempt_name,
        "variant_id": variant_id,
        "queue_id": queue["queue_id"],
        "source_variant_id": source_variant["variant_id"],
        "source_attempt_name": source_attempt["attempt_name"],
        "candidate_id": queue.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": queue.get("candidate_role"),
        "profile_label": "aggressive_impulse_dd_shape_followup",
        "tier": input_probe.mt5.TIER_A,
        "target_period": target_period,
        "split": source_attempt.get("split"),
        "attempt_role": "tier_only_total",
        "record_view_prefix": f"mt5_ta_{alias}_{period_token}_ca",
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
    source_reuse_row = {
        "queue_id": queue["queue_id"],
        "attempt_name": attempt_name,
        "candidate_alias": alias,
        "target_period": target_period,
        "source_variant_id": source_variant["variant_id"],
        "source_attempt_name": source_attempt["attempt_name"],
        "source_feature_file": rel(source_feature_path),
        "source_model_file": rel(source_model_path),
        "source_set_path": source_attempt["set_path"],
        "source_ini_path": source_attempt["ini_path"],
        "reuse_boundary": "source copied then augmented with one state-shaped guard feature and score-table term(원천 복제 후 상태형 방어 피처와 점수표 항 1개 추가)",
    }
    return variant_row, attempt_row, feature_row, model_row, source_reuse_row


def queue_decision_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        queue_id = str(row.get("queue_id"))
        if queue_id in GUARD_BY_QUEUE:
            decision = "materialized_execution_pending"
            effect = "P0 guard variant is ready for MT5 execution(P0 방어 변형을 MT5 실행 입력으로 준비)"
        else:
            decision = "held_review_only_no_mt5"
            effect = "P1 curve zoom sanity remains a review plan until P0 execution evidence exists(P1 곡선 확대 점검은 P0 실행 근거 전까지 검토 계획으로 보류)"
        rows.append(
            {
                "queue_id": queue_id,
                "priority": row.get("priority"),
                "workstream": row.get("workstream"),
                "candidate_alias": row.get("candidate_alias"),
                "target_period": row.get("target_period"),
                "run267CA_decision": decision,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def curve_zoom_plan_rows(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        output.append(
            {
                "plan_id": f"run267ca_curve_zoom_{safe_token(row.get('queue_id'))}",
                "source_queue_id": row.get("queue_id"),
                "candidate_alias": row.get("candidate_alias"),
                "target_period": row.get("target_period"),
                "status": "held_until_p0_mt5_review",
                "reason": row.get("hypothesis"),
                "required_evidence": "P0 MT5 execution report, trade_records, curve_diagnostics, negative_slice_summary(P0 MT5 실행 보고, 거래 기록, 곡선 진단, 음수 구간 요약)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def experiment_design_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": f"run267ca_{safe_token(row.get('queue_id'))}",
            "hypothesis": row.get("hypothesis"),
            "decision_use": row.get("workstream"),
            "comparison_baseline": row.get("comparison_baseline"),
            "control_variables": row.get("control_variables"),
            "changed_variables": row.get("changed_variables"),
            "sample_scope": row.get("target_period"),
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
            "check_id": "run267ca_runtime_features",
            "status": "passed" if duplicate_rows == 0 and missing_cells == 0 else "warning",
            "evidence": f"feature_frames={len(feature_rows)};duplicate_bar_time_rows={duplicate_rows};runtime_missing_feature_cells={missing_cells}",
            "effect": "MT5 input feature frames are timestamp-ordered and complete enough for execution handoff(MT5 입력 피처 프레임이 실행 인계에 필요한 시간 순서와 완전성을 가진지 확인)",
        }
    ]


def runtime_parity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267ca_feature_order_and_score_table_load",
            "status": "passed",
            "evidence": f"attempts={len(feature_rows)};score_table_validation=passed",
            "effect": "Python score-table loader accepts the augmented feature order(파이썬 점수표 로더가 확장 피처 순서를 수용)",
            "claim_boundary": "handoff_contract_only_no_runtime_parity_claim(인계 계약만, 런타임 동등성 주장 아님)",
        },
        {
            "check_id": "run267ca_tier_b_routing",
            "status": "blocked",
            "evidence": TIER_PAIR_BOUNDARY,
            "effect": "Tier B fallback and actual routed total remain outside this materialization(Tier B 대체와 실제 라우팅 전체는 이번 물질화 밖)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def failure_memory_rows() -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "run267ca_guard_is_state_shaped_not_calendar_delete",
            "pattern": "avoid_calendar_only_repair(달력 전용 수리 회피)",
            "evidence": rel(SOURCE_PRUNE_MATRIX_PATH),
            "why_failed_or_fragile": "run267BZ blocked a pure 22h deletion because it can hide risk-shape fragility(run267BZ가 위험 형태 취약성을 숨길 수 있어 순수 22시 삭제를 차단)",
            "do_not_repeat": "do not create a variant that only removes one clock bucket(시각 구간 하나만 제거하는 변형 금지)",
            "salvage_angle": "use late-session plus impulse/rank/gate risk score(후반 세션과 임펄스/순위/게이트 위험 점수 결합)",
            "reopen_condition": "only after run267CB shows whether guard improves without shifting loss(run267CB가 손실 이동 없이 개선되는지 보여준 뒤)",
            "boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "run267ca_repair_loop_limit",
            "pattern": "bounded_repair_loop(제한 수리 루프)",
            "evidence": rel(SOURCE_QUEUE_PATH),
            "why_failed_or_fragile": "this branch is already a follow-up of run267BY/run267BZ(이 분기는 이미 run267BY/run267BZ의 후속)",
            "do_not_repeat": "after run267CB review, deepen once at most or prune(267CB 검토 뒤 최대 한 번만 심화하거나 가지치기)",
            "salvage_angle": "strong evidence can move to broader Adapter branch(강한 근거만 넓은 어댑터 분기로 이동)",
            "reopen_condition": "new cross-period or feature replacement evidence(새 확장 기간 또는 피처 대체 근거)",
            "boundary": CLAIM_BOUNDARY,
        },
    ]


def result_judgment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"queue_rows={counts['queue_rows']};materialized_attempts={counts['attempts']};held_rows={counts['held_rows']};feature_frames={counts['feature_frames']}",
            "evidence_missing": "MT5 reports, KPI, trade records, balance/equity curve, time-slice KPI, Adapter decision, ONNX parity(MT5 보고서, 핵심 성과 지표, 거래 기록, 잔액/평가금 곡선, 시간 구간 지표, 어댑터 판단, ONNX 동등성)",
            "judgment_label": "exploratory_materialization_only(탐색 물질화 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이번 실행은 후보를 고른 것이 아니라, 후반 세션 손실폭 형태를 실제 MT5에서 눌러볼 입력을 만든 것이다.",
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "source_queue_present(원천 대기열 존재)",
            "status": "passed" if counts["queue_rows"] == 3 else "warning",
            "evidence": f"queue_rows={counts['queue_rows']}",
            "effect": "run267BZ 대기열을 누락 없이 소비했는지 확인한다.",
        },
        {
            "gate_id": "p0_attempts_materialized(P0 시도 물질화)",
            "status": "passed" if counts["attempts"] == 2 else "failed",
            "evidence": f"attempts={counts['attempts']};held_rows={counts['held_rows']}",
            "effect": "P0 두 개는 실행 입력으로 만들고 P1 하나는 보류했음을 확인한다.",
        },
        {
            "gate_id": "score_table_validation(점수표 검증)",
            "status": "passed",
            "evidence": "all materialized rows passed score-table probability smoke check(모든 물질화 행이 점수표 확률 스모크 확인 통과)",
            "effect": "새 피처 순서와 점수표 폭이 맞는지 확인한다.",
        },
        {
            "gate_id": "claim_boundary(주장 경계)",
            "status": "passed",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "물질화를 후보 선택이나 ONNX 검토로 과장하지 않는다.",
        },
    ]


def runtime_contract_rows(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "variant_id": row["variant_id"],
            "attempt_name": row["attempt_name"],
            "candidate_alias": row["candidate_alias"],
            "target_period": row["target_period"],
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
    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    if not queue_rows:
        raise RuntimeError(f"missing source queue: {rel(SOURCE_QUEUE_PATH)}")
    material_rows = materializable_queue_rows(queue_rows)
    held_rows = held_queue_rows(queue_rows)
    source_attempt_by_variant = source_attempts()
    variant_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    source_reuse_rows: list[dict[str, Any]] = []
    for order, row in enumerate(material_rows, start=1):
        variant_row, attempt_row, feature_row, model_row, source_reuse_row = materialize_attempt(
            row,
            source_attempt_by_variant=source_attempt_by_variant,
            order=order,
        )
        variant_rows.append(variant_row)
        attempt_rows.append(attempt_row)
        feature_rows.append(feature_row)
        model_rows.append(model_row)
        source_reuse_rows.append(source_reuse_row)
    queue_decisions = queue_decision_rows(queue_rows)
    curve_zoom_plan = curve_zoom_plan_rows(held_rows)
    counts = {
        "queue_rows": len(queue_rows),
        "materialized_queue_rows": len(material_rows),
        "held_rows": len(held_rows),
        "attempts": len(attempt_rows),
        "variants": len(variant_rows),
        "feature_frames": len(feature_rows),
        "model_rows": len(model_rows),
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
        "source_reuse_manifest": source_reuse_rows,
        "curve_zoom_review_plan": curve_zoom_plan,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "runtime_contract": runtime_contract_rows(variant_rows),
        "experiment_design_receipt": experiment_design_rows(queue_rows),
        "data_integrity_receipt": data_integrity_rows(feature_rows),
        "runtime_parity_receipt": runtime_parity_rows(feature_rows),
        "failure_memory_seed": failure_memory_rows(),
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
            "source_report": rel(SOURCE_REPORT_PATH),
            "producer": rel(PRODUCER_PATH),
        },
        "outputs": {
            "queue_decision": rel(QUEUE_DECISION_PATH),
            "source_reuse_manifest": rel(SOURCE_REUSE_MANIFEST_PATH),
            "curve_zoom_review_plan": rel(CURVE_ZOOM_PLAN_PATH),
            "feature_frame_manifest": rel(FEATURE_FRAME_MANIFEST_PATH),
            "model_manifest": rel(MODEL_MANIFEST_PATH),
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
            "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
            "failure_memory_seed": rel(FAILURE_MEMORY_SEED_PATH),
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
    write_csv(SOURCE_REUSE_MANIFEST_PATH, result["source_reuse_manifest"])
    write_csv(CURVE_ZOOM_PLAN_PATH, result["curve_zoom_review_plan"])
    write_csv(FEATURE_FRAME_MANIFEST_PATH, result["feature_frame_manifest"])
    write_csv(MODEL_MANIFEST_PATH, result["model_manifest"])
    write_csv(VARIANT_MANIFEST_PATH, result["variant_manifest"])
    write_csv(ATTEMPT_MANIFEST_PATH, result["attempt_manifest"])
    write_csv(RUNTIME_CONTRACT_PATH, result["runtime_contract"])
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"])
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"])
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"])
    write_csv(FAILURE_MEMORY_SEED_PATH, result["failure_memory_seed"])
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
            "queue_rows": result["counts"]["queue_rows"],
            "materialized_attempts": result["counts"]["attempts"],
            "held_rows": result["counts"]["held_rows"],
            "feature_frame_count": result["counts"]["feature_frames"],
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
        "# Stage267 Run267CA Aggressive Impulse DD-shape Follow-up Materialization(267단계 267CA 공격형 임펄스 손실폭 형태 후속 물질화)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- source_materialization(원천 물질화): `{SOURCE_MATERIALIZATION_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- queue_rows(대기열 행): `{counts['queue_rows']}`",
        f"- materialized_attempts(물질화 시도): `{counts['attempts']}`",
        f"- held_rows(보류 행): `{counts['held_rows']}`",
        f"- feature_frames(피처 프레임): `{counts['feature_frames']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267BZ(267BZ 실행)의 P0 대기열 두 개를 MT5(MetaTrader 5, 메타트레이더5) 입력으로 만들고, P1 곡선 확대 점검은 보류 계획으로 남겼다.",
        "Effect(효과): `s264_aih`는 후반 세션 손실폭 형태 방어, `s258_stc`는 손실폭 상한 압박으로 다음 실행에서 직접 깨뜨려 볼 수 있다.",
        "",
        "## Queue Decision(대기열 판단)",
        "",
        "| queue(대기열) | candidate(후보) | period(기간) | decision(판단) |",
        "| --- | --- | --- | --- |",
    ]
    for row in result["queue_decisions"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['candidate_alias']}` | `{row['target_period']}` | `{row['run267CA_decision']}` |"
        )
    lines.extend(
        [
            "",
            "## Attempt Inputs(시도 입력)",
            "",
            "| attempt(시도) | candidate(후보) | feature_count(피처 수) | guard_mean(방어 평균) | feature_hash(피처 해시) | status(상태) |",
            "| --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in result["feature_frame_manifest"]:
        lines.append(
            f"| `{row['attempt_name']}` | `{row['candidate_alias']}` | {row['feature_count']} | "
            f"{as_float(row['guard_mean'])} | `{row['feature_order_hash']}` | `{row['materialization_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- run267CA(267CA 실행)는 materialization-only(물질화 전용) 증거다.",
            "- MT5 execution(MT5 실행), KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표)는 아직 없다.",
            "- selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "- P1 curve zoom sanity(P1 곡선 확대 정상성)는 P0 실행 근거가 나온 뒤 재개한다.",
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
        ("stage267_run267CA_producer", "producer_script", PRODUCER_PATH, "Builds run267CA aggressive impulse DD-shape follow-up materialization."),
        ("stage267_run267CA_source_queue", "source_queue", SOURCE_QUEUE_PATH, "Run267BZ materialization queue."),
        ("stage267_run267CA_source_variant_manifest", "source_variant_manifest", SOURCE_VARIANT_MANIFEST_PATH, "Run267BW variant manifest."),
        ("stage267_run267CA_source_attempt_manifest", "source_attempt_manifest", SOURCE_ATTEMPT_MANIFEST_PATH, "Run267BW attempt manifest."),
        ("stage267_run267CA_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Run267CA queue decisions."),
        ("stage267_run267CA_source_reuse_manifest", "source_reuse_manifest", SOURCE_REUSE_MANIFEST_PATH, "Run267CA source reuse manifest."),
        ("stage267_run267CA_curve_zoom_plan", "curve_zoom_review_plan", CURVE_ZOOM_PLAN_PATH, "Run267CA curve zoom plan."),
        ("stage267_run267CA_feature_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Run267CA feature frame manifest."),
        ("stage267_run267CA_model_manifest", "model_manifest", MODEL_MANIFEST_PATH, "Run267CA model manifest."),
        ("stage267_run267CA_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Run267CA variant manifest."),
        ("stage267_run267CA_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267CA MT5 attempt manifest."),
        ("stage267_run267CA_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267CA runtime contract."),
        ("stage267_run267CA_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267CA experiment design receipt."),
        ("stage267_run267CA_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267CA data integrity receipt."),
        ("stage267_run267CA_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Run267CA runtime boundary receipt."),
        ("stage267_run267CA_failure_memory", "failure_memory_seed", FAILURE_MEMORY_SEED_PATH, "Run267CA failure memory seed."),
        ("stage267_run267CA_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267CA result judgment."),
        ("stage267_run267CA_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267CA gate audit."),
        ("stage267_run267CA_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267CA run manifest."),
        ("stage267_run267CA_lineage", "lineage", LINEAGE_PATH, "Run267CA lineage."),
        ("stage267_run267CA_review_result", "review_result", REVIEW_RESULT_PATH, "Run267CA review result."),
        ("stage267_run267CA_report", "review_report", REPORT_PATH, "Run267CA report."),
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
                "artifact_id": f"stage267_run267CA_feature_{safe_token(row['attempt_name'], 72)}",
                "artifact_type": "runtime_feature_csv",
                "path": rel(feature_path),
                "sha256": sha256_file_lf_normalized(feature_path) if path_exists(feature_path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Runtime feature CSV for {row['attempt_name']}.",
            }
        )
    for row in result["model_manifest"]:
        model_path = repo_path(str(row["runtime_model_file"]))
        rows.append(
            {
                "artifact_id": f"stage267_run267CA_model_{safe_token(row['attempt_name'], 72)}",
                "artifact_type": "runtime_model_csv",
                "path": rel(model_path),
                "sha256": sha256_file_lf_normalized(model_path) if path_exists(model_path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Runtime score-table model for {row['attempt_name']}.",
            }
        )
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    stage_row = {
        "row_id": "stage267_run267CA_aggressive_impulse_dd_shape_followup_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "aggressive_impulse_dd_shape_followup_materialization",
        "tier_scope": "Tier A 2025H2 P0 attempt inputs; Tier B and actual routed total blocked",
        "scoreboard": "feature_model_set_ini_materialization_no_mt5_kpi",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"queue_rows={counts['queue_rows']};attempts={counts['attempts']};held_rows={counts['held_rows']};next_action={NEXT_ACTION}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "aggressive_impulse_dd_shape_followup_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"attempts={counts['attempts']};held_rows={counts['held_rows']};selected_candidate=none;onnx_readiness=not_claimed.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__aggressive_impulse_dd_shape_followup_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "aggressive_impulse_dd_shape_followup_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "attempt_input_materialization",
        "tier_scope": "Tier A P0 follow-up; true fallback blocked",
        "kpi_scope": "materialization_no_mt5_kpi",
        "scoreboard_lane": "aggressive_impulse_dd_shape_followup_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"queue_rows={counts['queue_rows']};attempts={counts['attempts']};held_rows={counts['held_rows']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(str(result["created_at_utc"]), result), key="artifact_id")


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


def update_stage267_workspace_block(text: str, report_entry: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    report_seen = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not report_seen:
                output.append(report_entry)
                report_seen = True
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
                if not report_seen:
                    output.append(report_entry)
                    report_seen = True
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    if in_stage267 and not report_seen:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def update_docs(result: Mapping[str, Any]) -> None:
    report_line = f"- run267CA_aggressive_impulse_dd_shape_followup_materialization(267CA 공격형 임펄스 손실폭 형태 후속 물질화): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            "Run267CA(267CA 실행)는 run267BZ(267BZ 실행)의 P0 후속 두 개를 MT5(MetaTrader 5, 메타트레이더5) 입력으로 물질화했다.",
            f"Effect(효과): materialized attempts(물질화 시도) `{result['counts']['attempts']}`개, held rows(보류 행) `{result['counts']['held_rows']}`개를 만들고 다음 행동을 `{NEXT_ACTION}`으로 고정했다.",
            "Boundary(경계): 아직 MT5 실행, KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), selected candidate(선택 후보), ONNX readiness(ONNX 준비)는 없다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `aggressive_impulse_dd_shape_followup_materialization`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = append_after_contains(text, "stage267_run267BZ_aggressive_impulse_dd_shape_cross_period_followup_or_prune_design.md", report_line)
        text = append_block_once(text, "Run267CA(267CA 실행)는", block)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267CA(267CA 실행) aggressive impulse DD-shape follow-up materialization(공격형 임펄스 손실폭 형태 후속 물질화) `{STATUS}`. "
        f"Effect(효과): run267BZ(267BZ 실행)의 P0 대기열 2개를 MT5(MetaTrader 5, 메타트레이더5) 입력으로 만들고 P1 곡선 확대 점검 1개는 보류했으며 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        f"  run267CA_aggressive_impulse_dd_shape_followup_materialization_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def execute() -> dict[str, Any]:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_docs(result)
    return result


def main() -> int:
    result = execute()
    print(
        json.dumps(
            {
                "status": result["status"],
                "queue_rows": result["counts"]["queue_rows"],
                "materialized_attempts": result["counts"]["attempts"],
                "held_rows": result["counts"]["held_rows"],
                "feature_frames": result["counts"]["feature_frames"],
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
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
