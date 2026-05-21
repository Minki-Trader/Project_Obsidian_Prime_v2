from __future__ import annotations

import csv
import json
import math
import re
import shutil
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
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import (
    run267BC_materialize_adjacent_period_replacement_frames as period_tools,
)
from stage_pipelines.stage267 import (
    run267BS_pool_wide_directional_impulse_followup_materialization as source_materialization,
)
from stage_pipelines.stage267 import (
    run267BV_directional_impulse_followup_or_prune_design as source_design,
)
from stage_pipelines.stage267 import (
    run267K_retrained_soft_context_adapter_materialization as source_retrain,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267BW"
RUN_ID = "run267BW_stage267_aggressive_impulse_dd_shape_cross_period_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_materialization.RUN_ID
STATUS = "run267BW_aggressive_impulse_dd_shape_cross_period_materialized_execution_pending"
JUDGMENT = "aggressive_impulse_cross_period_materialized_no_candidate_selection"
NEXT_ACTION = "run267BX_execute_aggressive_impulse_dd_shape_cross_period_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "aggressive_impulse_dd_shape_cross_period_materialization"
FEATURE_ROOT = RUN_ROOT / "features"
VARIANT_ROOT = RUN_ROOT / "variants"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_QUEUE_PATH = source_design.MATERIALIZATION_QUEUE_PATH
SOURCE_AGGRESSIVE_WATCHLIST_PATH = source_design.AGGRESSIVE_WATCHLIST_PATH
SOURCE_BRANCH_DECISION_PATH = source_design.BRANCH_DECISION_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_VARIANT_MANIFEST_PATH = source_materialization.VARIANT_MANIFEST_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = source_materialization.ATTEMPT_MANIFEST_PATH

QUEUE_DECISION_PATH = RUN_ROOT / "queue_decision.csv"
PERIOD_AVAILABILITY_PATH = RUN_ROOT / "period_availability.csv"
FEATURE_FRAME_MANIFEST_PATH = RUN_ROOT / "feature_frame_manifest.csv"
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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BW_aggressive_impulse_dd_shape_cross_period_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BW_aggressive_impulse_dd_shape_cross_period_materialization.py")

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

COMMON_ROOT = "OPV2/s267bw/run267BW_aggressive_impulse_dd_shape_cross_period"
TIER_PAIR_BOUNDARY = "Tier_B_and_actual_routed_total_blocked_until_true_fallback_manifest_exists"
MATERIALIZATION_BOUNDARY = "run267BS_aggressive_impulse_score_table_rebuilt_on_adjacent_period_frames"
ENGINEERED_FEATURE = "stage267bs_impulse_replacement_score"

PERIOD_BY_TARGET = {
    "2023H2": "adjacent_2023_h2_train_pre_2024",
    "2025H1": "adjacent_2025_h1_validation_post_2024",
    "2025H2": "adjacent_2025_h2_oos_followthrough",
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


def split_semicolon(value: Any) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


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


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def parse_key_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        if not line or line.lstrip().startswith(";") or "=" not in line or line.startswith("["):
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def write_set(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["; generated_by=run267BW_aggressive_impulse_dd_shape_cross_period_materialization"]
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


def copy_model_to_variant(source: Path, destination: Path) -> dict[str, str]:
    if not path_exists(source):
        raise FileNotFoundError(rel(source))
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def source_variants_by_alias() -> dict[str, dict[str, str]]:
    rows = read_csv(SOURCE_VARIANT_MANIFEST_PATH)
    output: dict[str, dict[str, str]] = {}
    for row in rows:
        if row.get("profile_label") == "aggressive_impulse_replacement":
            output[str(row["candidate_alias"])] = row
    return output


def source_attempts_by_variant() -> dict[str, dict[str, str]]:
    return {str(row["variant_id"]): row for row in read_csv(SOURCE_ATTEMPT_MANIFEST_PATH)}


def candidate_specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def queue_decision_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        workstream = str(row.get("workstream", ""))
        if workstream == "prune_receipt":
            decision = "prune_receipt_consumed_no_mt5"
            effect = "방향 비대칭 독립 분기는 다시 실행하지 않고 실패 기억으로만 남긴다."
        elif workstream == "aggressive_impulse_cross_period_pressure":
            decision = "materialized_execution_pending"
            effect = "공격형 임펄스 단서가 다른 기간에서도 덜 깨지는지 MT5 실행으로 확인할 수 있게 만든다."
        elif workstream == "similar_feature_replacement_probe":
            decision = "blocked_feature_availability_audit_before_mt5"
            effect = "유사 피처 대체는 원천 피처 계보가 먼저 연결되어야 하므로 이번 MT5 물질화에서 제외한다."
        else:
            decision = "not_materialized_unrecognized_scope"
            effect = "workstream(작업 흐름)이 명확하지 않아 실행 입력으로 만들지 않는다."
        rows.append(
            {
                "queue_id": row.get("queue_id"),
                "priority": row.get("priority"),
                "workstream": workstream,
                "candidate_alias": row.get("candidate_alias"),
                "target_period": row.get("target_period"),
                "target_split": row.get("target_split"),
                "run267BW_decision": decision,
                "effect": effect,
                "claim_boundary": "no_selected_candidate_no_onnx_no_goal_achieve",
            }
        )
    return rows


def materializable_queue_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    rows = [dict(row) for row in queue_rows if row.get("workstream") == "aggressive_impulse_cross_period_pressure"]
    if len(rows) != 9:
        raise RuntimeError(f"expected 9 aggressive impulse cross-period rows, found {len(rows)}")
    return rows


def period_lookup(period_rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row["period_id"]): row for row in period_rows}


def build_aggressive_period_feature_file(
    frame: pd.DataFrame,
    spec: Any,
    variant: Mapping[str, str],
    *,
    base_destination: Path,
    final_destination: Path,
) -> dict[str, Any]:
    full_feature_order = split_semicolon(variant["feature_order"])
    source_feature_count = as_int(variant.get("source_feature_count"), 0)
    base_feature_order = full_feature_order[:source_feature_count]
    engineered_features = split_semicolon(variant.get("engineered_features"))
    if engineered_features != [ENGINEERED_FEATURE]:
        raise RuntimeError(f"unexpected engineered feature list for {variant['variant_id']}: {engineered_features}")
    if ordered_hash(full_feature_order) != str(variant.get("feature_order_hash")):
        raise RuntimeError(f"source feature order hash mismatch for {variant['variant_id']}")

    base_meta, runtime = period_tools.build_runtime_feature_file(frame, spec, base_feature_order, base_destination)
    signal = pd.to_numeric(runtime["stage56_context_et_event_signal"], errors="coerce").fillna(0.0)
    rank = pd.to_numeric(runtime[str(variant["rank_column"])], errors="coerce").fillna(0.0)
    gate = pd.to_numeric(runtime[str(variant["gate_column"])], errors="coerce").fillna(0.0)
    rank_norm = (rank / max(float(rank.max()), 1.0)).clip(0.0, 1.0)
    gate_norm = (gate / max(float(gate.max()), 1.0)).clip(0.0, 1.0)
    impulse = signal.abs().clip(0.0, 1.0)
    runtime[ENGINEERED_FEATURE] = (0.4 * impulse + 0.35 * rank_norm + 0.25 * gate_norm).clip(0.0, 1.0)

    runtime_columns = ["bar_time_server", *full_feature_order]
    write_runtime_csv(final_destination, runtime, runtime_columns)
    validation = source_materialization.validate_score_table(
        final_destination,
        repo_path(str(variant["runtime_model_file"])),
        full_feature_order,
    )
    return {
        "base_feature_file": base_meta["feature_file"],
        "base_feature_sha256": base_meta["feature_sha256"],
        "runtime_feature_file": rel(final_destination),
        "runtime_feature_sha256": sha256_file_lf_normalized(final_destination),
        "rows": int(len(runtime)),
        "first_bar_time_server": str(runtime["bar_time_server"].iloc[0]) if len(runtime) else "",
        "last_bar_time_server": str(runtime["bar_time_server"].iloc[-1]) if len(runtime) else "",
        "duplicate_bar_time_rows": int(runtime["bar_time_server"].duplicated().sum()) if len(runtime) else 0,
        "runtime_missing_feature_cells": int(runtime.loc[:, full_feature_order].isna().sum().sum()) if len(runtime) else 0,
        "source_feature_count": len(base_feature_order),
        "engineered_feature_count": len(engineered_features),
        "feature_count": len(full_feature_order),
        "feature_order": full_feature_order,
        "feature_order_hash": ordered_hash(full_feature_order),
        "engineered_feature_min": float(runtime[ENGINEERED_FEATURE].min()) if len(runtime) else 0.0,
        "engineered_feature_max": float(runtime[ENGINEERED_FEATURE].max()) if len(runtime) else 0.0,
        "engineered_feature_mean": float(runtime[ENGINEERED_FEATURE].mean()) if len(runtime) else 0.0,
        **validation,
    }


def materialize_attempt(
    row: Mapping[str, str],
    variant_by_alias: Mapping[str, Mapping[str, str]],
    attempt_by_variant: Mapping[str, Mapping[str, str]],
    specs_by_alias: Mapping[str, Any],
    frames: Mapping[str, pd.DataFrame],
    period_by_id: Mapping[str, Mapping[str, Any]],
    *,
    order: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    alias = str(row["candidate_alias"])
    target_period = str(row["target_period"])
    period_id = PERIOD_BY_TARGET[target_period]
    period_meta = period_by_id[period_id]
    variant = dict(variant_by_alias[alias])
    source_variant_id = str(variant["variant_id"])
    source_attempt = dict(attempt_by_variant[source_variant_id])
    source_set_path = repo_path(str(source_attempt["set_path"]))
    source_ini_path = repo_path(str(source_attempt["ini_path"]))
    source_model_path = repo_path(str(variant["runtime_model_file"]))

    period_token = safe_token(target_period, 16)
    attempt_name = f"run267bw_{order:02d}_{alias}_{period_token}_impulse_repl"
    variant_id = f"{attempt_name}_variant"
    base_feature_path = FEATURE_ROOT / alias / period_id / f"{attempt_name}_base_features.csv"
    final_feature_path = FEATURE_ROOT / alias / period_id / f"{attempt_name}_features.csv"
    model_path = VARIANT_ROOT / alias / variant_id / "models" / f"{variant_id}_model.csv"

    feature_meta = build_aggressive_period_feature_file(
        frames[period_id],
        specs_by_alias[alias],
        variant,
        base_destination=base_feature_path,
        final_destination=final_feature_path,
    )
    model_meta = copy_model_to_variant(source_model_path, model_path)

    common_root = f"{COMMON_ROOT}/{alias}/{period_token}/{attempt_name}"
    common_feature_path = f"{common_root}/features/{final_feature_path.name}"
    common_model_path = f"{common_root}/models/{model_path.name}"
    common_feature = copy_to_common(final_feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    set_values = parse_key_values(source_set_path)
    ini_values = parse_key_values(source_ini_path)
    telemetry = f"{common_root}/telemetry/{attempt_name}_telemetry.csv"
    summary = f"{common_root}/telemetry/{attempt_name}_summary.csv"
    report_name = f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}"
    magic = 26723000 + order

    next_set_values = dict(set_values)
    next_set_values.update(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": f"stage267_AggressiveImpulseCrossPeriod__{alias}_{period_token}",
            "InpTierLabel": input_probe.mt5.TIER_A,
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": str(period_meta["period_label"]),
            "InpModelPath": common_model_path,
            "InpModelId": f"{RUN_ID}_{alias}_{period_token}",
            "InpModelBackend": "ebm_table",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": common_feature_path,
            "InpFeatureCount": feature_meta["feature_count"],
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpFeatureStrictHeader": "true",
            "InpFeatureOrderHash": feature_meta["feature_order_hash"],
            "InpFallbackEnabled": "false",
            "InpFallbackUseOnPrimaryFlat": "false",
            "InpFallbackUseOnPrimaryLowConfidence": "false",
            "InpFallbackFeatureCsvPath": common_feature_path,
            "InpFallbackFeatureCount": feature_meta["feature_count"],
            "InpFallbackModelPath": common_model_path,
            "InpFallbackModelId": f"{RUN_ID}_{alias}_{period_token}_fallback_disabled",
            "InpFallbackModelBackend": "ebm_table",
            "InpFallbackFeatureOrderHash": feature_meta["feature_order_hash"],
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
            "FromDate": period_meta["tester_from_date"],
            "ToDate": period_meta["tester_to_date"],
            "Report": report_name,
            "ExpertParameters": EA_TESTER_SET_NAME,
            "ReplaceReport": 1,
            "ShutdownTerminal": 1,
        }
    )
    ini_payload = write_ini(MT5_ROOT / f"{attempt_name}.ini", next_ini_values)

    variant_row = {
        "variant_id": variant_id,
        "attempt_name": attempt_name,
        "queue_id": row["queue_id"],
        "source_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "source_variant_id": source_variant_id,
        "source_attempt_name": source_attempt["attempt_name"],
        "candidate_id": row.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": row.get("candidate_role"),
        "source_profile": row.get("source_profile"),
        "target_period": target_period,
        "period_id": period_id,
        "period_label": period_meta["period_label"],
        "model_materialization_type": "cloned_run267BS_aggressive_impulse_score_table",
        "source_model_file": rel(source_model_path),
        "source_model_sha256": sha256_file_lf_normalized(source_model_path),
        "runtime_model_file": model_meta["path"],
        "runtime_model_sha256": model_meta["sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "runtime_feature_file": feature_meta["runtime_feature_file"],
        "runtime_feature_sha256": feature_meta["runtime_feature_sha256"],
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "feature_count": feature_meta["feature_count"],
        "feature_order": feature_meta["feature_order"],
        "feature_order_hash": feature_meta["feature_order_hash"],
        "engineered_features": ENGINEERED_FEATURE,
        "rank_column": variant["rank_column"],
        "gate_column": variant["gate_column"],
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    attempt_row = {
        "attempt_name": attempt_name,
        "variant_id": variant_id,
        "queue_id": row["queue_id"],
        "source_variant_id": source_variant_id,
        "candidate_id": row.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": row.get("candidate_role"),
        "profile_label": "aggressive_impulse_replacement",
        "tier": input_probe.mt5.TIER_A,
        "target_period": target_period,
        "split": period_meta["period_label"],
        "attempt_role": "tier_only_total",
        "record_view_prefix": f"mt5_ta_{alias}_{period_token}_bw",
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
    feature_row = {
        "attempt_name": attempt_name,
        "variant_id": variant_id,
        "queue_id": row["queue_id"],
        "source_variant_id": source_variant_id,
        "candidate_alias": alias,
        "target_period": target_period,
        "period_id": period_id,
        "period_role": period_meta["period_role"],
        **feature_meta,
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "runtime_model_file": model_meta["path"],
        "runtime_model_sha256": model_meta["sha256"],
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "materialization_status": "materialized_execution_pending",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return variant_row, attempt_row, feature_row


def experiment_design_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        rows.append(
            {
                "receipt_id": f"run267bw_{safe_token(row.get('queue_id'))}",
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
        )
    return rows


def data_integrity_rows(period_rows: Sequence[Mapping[str, Any]], feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    duplicate_periods = sum(as_int(row.get("duplicate_timestamp_rows")) for row in period_rows)
    missing_period_cells = sum(as_int(row.get("missing_raw_feature_cells")) for row in period_rows)
    duplicate_runtime = sum(as_int(row.get("duplicate_bar_time_rows")) for row in feature_rows)
    missing_runtime = sum(as_int(row.get("runtime_missing_feature_cells")) for row in feature_rows)
    return [
        {
            "check_id": "run267bw_period_frames",
            "status": "passed" if duplicate_periods == 0 else "warning",
            "evidence": f"periods={len(period_rows)};duplicate_timestamp_rows={duplicate_periods};missing_raw_feature_cells={missing_period_cells}",
            "effect": "확장 기간 프레임이 비어 있지 않고 MT5 입력으로 재구성 가능한지 확인한다.",
        },
        {
            "check_id": "run267bw_runtime_features",
            "status": "passed" if duplicate_runtime == 0 and missing_runtime == 0 else "warning",
            "evidence": f"feature_frames={len(feature_rows)};duplicate_bar_time_rows={duplicate_runtime};runtime_missing_feature_cells={missing_runtime}",
            "effect": "최종 runtime feature(런타임 피처)가 타임스탬프와 피처 수 기준으로 깨지지 않았는지 확인한다.",
        },
    ]


def runtime_parity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267bw_score_table_feature_order",
            "status": "passed",
            "evidence": f"attempts={len(feature_rows)};all use run267BS aggressive impulse feature order and cloned score tables",
            "effect": "Python 물질화와 MT5 score table(점수표) 입력의 피처 순서가 같은지 추적한다.",
            "claim_boundary": "handoff_contract_only_no_runtime_parity_claim",
        },
        {
            "check_id": "run267bw_tier_b_routing",
            "status": "blocked",
            "evidence": TIER_PAIR_BOUNDARY,
            "effect": "Tier B 대체와 actual routed total(실제 라우팅 전체)을 합성 합산으로 오해하지 않게 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def failure_memory_rows() -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "run267bw_directional_asymmetry_prune_consumed",
            "pattern": "directional_asymmetry_standalone_profile_failed",
            "evidence": rel(SOURCE_BRANCH_DECISION_PATH),
            "why_failed_or_fragile": "다섯 후보 전체에서 독립 방향 비대칭은 음수 또는 PF 손상으로 닫혔다.",
            "do_not_repeat": "구조 변경 없이 같은 directional_asymmetry 독립 MT5 분기를 다시 만들지 않는다.",
            "salvage_angle": "방향 압력 진단 피처로만 남길 수 있다.",
            "reopen_condition": "다른 feature family(피처 묶음)와 결합해 명확한 새로운 가설이 생길 때만 재개한다.",
        },
        {
            "memory_id": "run267bw_similar_replacement_feature_lineage_blocked",
            "pattern": "similar_replacement_requires_source_feature_audit",
            "evidence": rel(QUEUE_DECISION_PATH),
            "why_failed_or_fragile": "유사 피처 대체는 원천 피처 계보와 feature order(피처 순서)가 아직 연결되지 않았다.",
            "do_not_repeat": "원천 피처 가용성 감사 없이 replacement(대체) MT5 입력을 만들지 않는다.",
            "salvage_angle": "다음 run에서 volatility expansion/trend-strength/range-shock 대체 후보를 설계한다.",
            "reopen_condition": "feature availability audit(피처 가용성 감사)이 통과할 때 재개한다.",
        },
    ]


def result_judgment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"queue_rows={counts['queue_rows']};attempts={counts['attempts']};feature_frames={counts['feature_frames']};period_rows={counts['period_rows']}",
            "evidence_missing": "MT5 reports, KPI, trade records, balance/equity curve, time-slice KPI, Adapter decision, ONNX parity",
            "judgment_label": "exploratory_materialization_only",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이번 실행은 후보를 고른 것이 아니라, 공격형 임펄스 단서가 다른 기간에서 깨지는지 볼 입력을 만든 것이다.",
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "source_queue_present",
            "status": "passed" if counts["queue_rows"] == 11 else "failed",
            "evidence": f"queue_rows={counts['queue_rows']}",
            "effect": "run267BV 후속 큐를 빠뜨리지 않고 소비했는지 확인한다.",
        },
        {
            "gate_id": "attempts_materialized",
            "status": "passed" if counts["attempts"] == 9 else "failed",
            "evidence": f"attempts={counts['attempts']};feature_frames={counts['feature_frames']}",
            "effect": "상위 3개 공격형 관찰 후보 x 3개 기간 입력이 모두 만들어졌는지 확인한다.",
        },
        {
            "gate_id": "claim_boundary",
            "status": "passed",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "물질화 완료를 후보 선정이나 ONNX 검토로 과장하지 않는다.",
        },
    ]


def runtime_contract_rows(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in variant_rows:
        rows.append(
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
        )
    return rows


def build_result() -> dict[str, Any]:
    created_at = utc_now()
    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    if not queue_rows:
        raise RuntimeError(f"missing source queue: {rel(SOURCE_QUEUE_PATH)}")
    aggressive_rows = materializable_queue_rows(queue_rows)
    variant_by_alias = source_variants_by_alias()
    attempt_by_variant = source_attempts_by_variant()
    specs_by_alias = candidate_specs_by_alias()
    required_aliases = sorted({row["candidate_alias"] for row in aggressive_rows})
    missing_variants = [alias for alias in required_aliases if alias not in variant_by_alias]
    missing_specs = [alias for alias in required_aliases if alias not in specs_by_alias]
    if missing_variants or missing_specs:
        raise RuntimeError(f"missing source variants/specs: variants={missing_variants}; specs={missing_specs}")
    missing_attempts = [
        variant_by_alias[alias]["variant_id"]
        for alias in required_aliases
        if variant_by_alias[alias]["variant_id"] not in attempt_by_variant
    ]
    if missing_attempts:
        raise RuntimeError(f"missing source attempts: {missing_attempts}")

    source_frame, source_info = source_retrain.source_frame()
    period_rows, frames = period_tools.build_period_availability(source_frame)
    period_by_id = period_lookup(period_rows)
    variant_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    for order, row in enumerate(aggressive_rows, start=1):
        variant_row, attempt_row, feature_row = materialize_attempt(
            row,
            variant_by_alias,
            attempt_by_variant,
            specs_by_alias,
            frames,
            period_by_id,
            order=order,
        )
        variant_rows.append(variant_row)
        attempt_rows.append(attempt_row)
        feature_rows.append(feature_row)

    queue_decisions = queue_decision_rows(queue_rows)
    blocked_or_audit_rows = [
        row for row in queue_decisions if row["run267BW_decision"] != "materialized_execution_pending"
    ]
    counts = {
        "queue_rows": len(queue_rows),
        "materialized_queue_rows": len(aggressive_rows),
        "blocked_or_audit_rows": len(blocked_or_audit_rows),
        "period_rows": len(period_rows),
        "attempts": len(attempt_rows),
        "feature_frames": len(feature_rows),
        "variants": len(variant_rows),
        "source_rows": source_info.get("rows"),
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
        "source_info": source_info,
        "counts": counts,
        "queue_decisions": queue_decisions,
        "period_availability": period_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "feature_frame_manifest": feature_rows,
        "runtime_contract": runtime_contract_rows(variant_rows),
        "experiment_design_receipt": experiment_design_rows(queue_rows),
        "data_integrity_receipt": data_integrity_rows(period_rows, feature_rows),
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
            "source_aggressive_watchlist": rel(SOURCE_AGGRESSIVE_WATCHLIST_PATH),
            "source_branch_decision": rel(SOURCE_BRANCH_DECISION_PATH),
            "source_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
            "source_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
            "source_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
            "producer": rel(PRODUCER_PATH),
        },
        "outputs": {
            "queue_decision": rel(QUEUE_DECISION_PATH),
            "period_availability": rel(PERIOD_AVAILABILITY_PATH),
            "feature_frame_manifest": rel(FEATURE_FRAME_MANIFEST_PATH),
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
    write_csv(PERIOD_AVAILABILITY_PATH, result["period_availability"])
    write_csv(FEATURE_FRAME_MANIFEST_PATH, result["feature_frame_manifest"])
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
            "attempt_count": result["counts"]["attempts"],
            "feature_frame_count": result["counts"]["feature_frames"],
            "blocked_or_audit_rows": result["counts"]["blocked_or_audit_rows"],
            "next_action": NEXT_ACTION,
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_md(REPORT_PATH, report_markdown(result))


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267BW Aggressive Impulse DD-shape Cross-period Materialization(267단계 267BW 공격형 임펄스 손실폭 형태 확장 기간 물질화)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- source_materialization(원천 물질화): `{SOURCE_MATERIALIZATION_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- queue_rows(대기열 행): `{counts['queue_rows']}`",
        f"- materialized_attempts(물질화 시도): `{counts['attempts']}`",
        f"- feature_frames(피처 프레임): `{counts['feature_frames']}`",
        f"- blocked_or_audit_rows(차단/감사 행): `{counts['blocked_or_audit_rows']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267BV(267BV 실행)의 materialization queue(물질화 대기열)를 받아 상위 3개 aggressive impulse(공격형 임펄스) 관찰 후보를 2023H2, 2025H1, 2025H2 기간별 MT5(MetaTrader 5, 메타트레이더5) 입력으로 만들었다.",
        "Effect(효과): 다음 run267BX(267BX 실행)에서 후보를 바로 고르지 않고, 기간을 바꿔도 PF/DD(수익 팩터/손실폭)와 거래 품질이 덜 깨지는지 확인할 수 있다.",
        "",
        "이번 실행은 baseline(기준 후보) 선택이 아니다. 숫자가 좋아 보여도 아직 MT5 실행 결과, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)가 없다.",
        "",
        "## Queue Decision(대기열 판단)",
        "",
        "| queue(대기열) | candidate(후보) | period(기간) | decision(판단) |",
        "| --- | --- | --- | --- |",
    ]
    for row in result["queue_decisions"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['candidate_alias']}` | `{row['target_period']}` | `{row['run267BW_decision']}` |"
        )
    lines.extend(
        [
            "",
            "## Attempt Inputs(시도 입력)",
            "",
            "| attempt(시도) | candidate(후보) | period(기간) | rows(행) | feature_hash(피처 해시) | status(상태) |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in result["feature_frame_manifest"]:
        lines.append(
            f"| `{row['attempt_name']}` | `{row['candidate_alias']}` | `{row['target_period']}` | {row['rows']} | `{row['feature_order_hash']}` | `{row['materialization_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- MT5 execution(MT5 실행): `not_executed`, 다음 run267BX(267BX 실행)에서 확인한다.",
            "- similar replacement(유사 피처 대체): `blocked_feature_availability_audit_before_mt5`, 원천 피처 계보 감사가 먼저 필요하다.",
            "- Tier B fallback(Tier B 대체): `blocked`, true fallback manifest(실제 대체 목록)이 아직 없다.",
            "- Adapter(어댑터): 보류. cross-period MT5 KPI(확장 기간 MT5 핵심 성과 지표), 거래 목록, 곡선, 시간 구간 검토 뒤 판단한다.",
            "- ONNX parity(ONNX 동등성): 금지. Goal gate(목표 게이트) 전에는 검토하지 않는다.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source queue(원천 대기열): `{rel(SOURCE_QUEUE_PATH)}`",
            f"- source variant manifest(원천 변형 목록): `{rel(SOURCE_VARIANT_MANIFEST_PATH)}`",
            f"- source attempt manifest(원천 시도 목록): `{rel(SOURCE_ATTEMPT_MANIFEST_PATH)}`",
            f"- feature manifest(피처 목록): `{rel(FEATURE_FRAME_MANIFEST_PATH)}`",
            f"- attempt manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- runtime contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
        ]
    )
    return "\n".join(lines) + "\n"


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267BW_producer", "producer_script", PRODUCER_PATH, "Builds run267BW aggressive impulse cross-period materialization."),
        ("stage267_run267BW_source_queue", "source_queue", SOURCE_QUEUE_PATH, "Run267BV materialization queue."),
        ("stage267_run267BW_source_variant_manifest", "source_variant_manifest", SOURCE_VARIANT_MANIFEST_PATH, "Run267BS aggressive impulse variant manifest."),
        ("stage267_run267BW_source_attempt_manifest", "source_attempt_manifest", SOURCE_ATTEMPT_MANIFEST_PATH, "Run267BS aggressive impulse attempt manifest."),
        ("stage267_run267BW_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Run267BW queue decisions."),
        ("stage267_run267BW_period_availability", "period_availability", PERIOD_AVAILABILITY_PATH, "Run267BW period availability."),
        ("stage267_run267BW_feature_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Run267BW feature frame manifest."),
        ("stage267_run267BW_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Run267BW variant manifest."),
        ("stage267_run267BW_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Run267BW MT5 attempt manifest."),
        ("stage267_run267BW_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Run267BW runtime contract."),
        ("stage267_run267BW_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267BW experiment design receipt."),
        ("stage267_run267BW_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267BW data integrity receipt."),
        ("stage267_run267BW_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Run267BW runtime boundary receipt."),
        ("stage267_run267BW_failure_memory", "failure_memory_seed", FAILURE_MEMORY_SEED_PATH, "Run267BW failure memory seed."),
        ("stage267_run267BW_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267BW result judgment."),
        ("stage267_run267BW_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267BW gate audit."),
        ("stage267_run267BW_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267BW run manifest."),
        ("stage267_run267BW_lineage", "lineage", LINEAGE_PATH, "Run267BW lineage."),
        ("stage267_run267BW_review_result", "review_result", REVIEW_RESULT_PATH, "Run267BW review result."),
        ("stage267_run267BW_report", "review_report", REPORT_PATH, "Run267BW report."),
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
                "artifact_id": f"stage267_run267BW_feature_{safe_token(row['attempt_name'], 72)}",
                "artifact_type": "runtime_feature_csv",
                "path": rel(feature_path),
                "sha256": sha256_file_lf_normalized(feature_path) if path_exists(feature_path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Runtime feature CSV for {row['attempt_name']}.",
            }
        )
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    stage_row = {
        "row_id": "stage267_run267BW_aggressive_impulse_dd_shape_cross_period_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "aggressive_impulse_dd_shape_cross_period_materialization",
        "tier_scope": "Tier A adjacent-period attempt inputs; Tier B and actual routed total blocked",
        "scoreboard": "feature_model_set_ini_materialization_no_mt5_kpi",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"queue_rows={counts['queue_rows']};attempts={counts['attempts']};feature_frames={counts['feature_frames']};next_action={NEXT_ACTION}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "aggressive_impulse_cross_period_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"attempts={counts['attempts']};selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__aggressive_impulse_dd_shape_cross_period_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "aggressive_impulse_dd_shape_cross_period_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "attempt_input_materialization",
        "tier_scope": "Tier A adjacent periods; true fallback blocked",
        "kpi_scope": "materialization_no_mt5_kpi",
        "scoreboard_lane": "aggressive_impulse_cross_period_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"queue_rows={counts['queue_rows']};attempts={counts['attempts']};feature_frames={counts['feature_frames']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ARTIFACT_COLUMNS,
        artifact_rows(str(result["created_at_utc"]), result),
        key="artifact_id",
    )


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


def update_workspace_stage_block(text: str, report_entry: str) -> str:
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


def update_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = f"- run267BW_aggressive_impulse_dd_shape_cross_period_materialization(267BW 공격형 임펄스 손실폭 형태 확장 기간 물질화): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            "Run267BW(267BW 실행)는 run267BV(267BV 실행)의 aggressive impulse cross-period pressure(공격형 임펄스 확장 기간 압박) 큐를 MT5(MetaTrader 5, 메타트레이더5) 입력으로 물질화했다.",
            f"Effect(효과): 상위 3개 관찰 후보 x 3개 기간 = `{counts['attempts']}`개 attempt(시도)를 만들었고, 다음 run267BX(267BX 실행)에서 기간별 PF/DD(수익 팩터/손실폭), curve(곡선), time-slice(시간 구간), trade quality(거래 품질)를 확인할 수 있다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = replace_line_prefix(
            text,
            "- adapter_under_review(검토 중 어댑터):",
            "- adapter_under_review(검토 중 어댑터): `aggressive_impulse_dd_shape_cross_period_materialization`",
        )
        text = append_after_contains(text, "stage267_run267BV_directional_impulse_followup_or_prune_design.md", report_line)
        text = append_block_once(text, "Run267BW(267BW 실행)는 run267BV", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BW(267BW 실행) aggressive impulse DD-shape cross-period materialization(공격형 임펄스 손실폭 형태 확장 기간 물질화) `{STATUS}`. "
        f"Effect(효과): run267BV(267BV 실행)의 대기열 11개를 소비해 방향 비대칭 가지치기 영수증 1개, 공격형 임펄스 확장 기간 MT5 시도 입력 {counts['attempts']}개, 유사 피처 대체 차단 감사 1개로 나눴고 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_workspace_stage_block(
        workspace,
        f"  run267BW_aggressive_impulse_dd_shape_cross_period_materialization_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_docs(result)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "queue_rows": result["counts"]["queue_rows"],
                "attempt_count": result["counts"]["attempts"],
                "feature_frame_count": result["counts"]["feature_frames"],
                "blocked_or_audit_rows": result["counts"]["blocked_or_audit_rows"],
                "next_action": NEXT_ACTION,
                "report": rel(REPORT_PATH),
                "selected_candidate": "none",
                "selected_research_baseline": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
