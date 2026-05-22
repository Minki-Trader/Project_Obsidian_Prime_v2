from __future__ import annotations

import csv
import json
import math
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

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
from stage_pipelines.stage267 import (
    run267DL_shared_weakness_breakout_third_followup_or_prune_materialization as source_materializer,
)
from stage_pipelines.stage267 import (
    run267DP_runtime_gap_aware_fourth_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267DQ"
RUN_ID = "run267DQ_stage267_runtime_gap_aware_fourth_followup_or_prune_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZER_RUN_ID = source_materializer.RUN_ID
STATUS = "run267DQ_runtime_gap_aware_fourth_followup_or_prune_materialized_execution_pending"
JUDGMENT = "runtime_gap_aware_fourth_followup_or_prune_materialized_no_candidate_selection"
NEXT_ACTION = "run267DR_execute_runtime_gap_aware_fourth_followup_or_prune_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_fourth_followup_or_prune_materialization"
FEATURE_ROOT = RUN_ROOT / "features"
VARIANT_ROOT = RUN_ROOT / "variants"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_QUEUE_PATH = source_design.MATERIALIZATION_QUEUE_PATH
SOURCE_FEATURE_BLUEPRINT_PATH = source_design.FEATURE_BLUEPRINT_PATH
SOURCE_BRANCH_DECISION_PATH = source_design.BRANCH_DECISION_PATH
SOURCE_PRUNE_MATRIX_PATH = source_design.PRUNE_MATRIX_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_REVIEW_RESULT_PATH = source_design.REVIEW_RESULT_PATH
SOURCE_DESIGN_REPORT_PATH = source_design.REPORT_PATH

SOURCE_VARIANT_MANIFEST_PATH = source_materializer.VARIANT_MANIFEST_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = source_materializer.ATTEMPT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_materializer.RUNTIME_CONTRACT_PATH
SOURCE_HANDOFF_RECEIPT_PATH = source_materializer.HANDOFF_RECEIPT_PATH
SOURCE_MATERIALIZATION_REPORT_PATH = source_materializer.REPORT_PATH

MATERIALIZATION_PLAN_PATH = RUN_ROOT / "materialization_plan.csv"
QUEUE_DECISION_PATH = RUN_ROOT / "queue_decision.csv"
FEATURE_FRAME_MANIFEST_PATH = RUN_ROOT / "feature_frame_manifest.csv"
MODEL_MANIFEST_PATH = RUN_ROOT / "model_manifest.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
HELD_QUEUE_PATH = RUN_ROOT / "held_queue.csv"
SUPPLY_DIAGNOSTIC_PATH = RUN_ROOT / "pre_runtime_supply_diagnostic.csv"
HANDOFF_RECEIPT_PATH = RUN_ROOT / "handoff_receipt.csv"
RISK_TAPER_RECEIPT_PATH = RUN_ROOT / "risk_taper_receipt.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH = RUN_ROOT / "environment_reproducibility_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DQ_runtime_gap_aware_fourth_followup_or_prune_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DQ_runtime_gap_aware_fourth_followup_or_prune_materialization.py")

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

COMMON_ROOT = "OPV2/s267dq/run267DQ_runtime_gap_aware_fourth_followup_or_prune"
EXPLORATION_LABEL = "stage267_BaselineRacing__RuntimeGapAwareFourthFollowupOrPrune"
MATERIALIZATION_BOUNDARY = "materialization_only_execution_pending_no_candidate_selection_no_selected_research_baseline_no_onnx"
TIER_PAIR_BOUNDARY = (
    "Tier A and duplicate-boundary Tier A+B are kept only where source attempts exist; "
    "true Tier B fallback and actual routed total remain unclaimed"
)

ACTIVE_PLAN_CONFIGS: tuple[dict[str, Any], ...] = (
    {
        "queue_id": "q01_s258_supply_shape_continuity_cross_period",
        "source_variant_id": "run267dl_04_s258_stc_2023h2_supply_sidefilter_open",
        "variant_id": "run267dq_01_s258_stc_2023h2_supply_continuity_sidefilter_open",
        "profile_label": "s258_stc_supply_continuity_sidefilter_open",
        "profile_token": "s258_supply_continuity",
        "materialization_type": "identity_copy_supply_continuity_no_threshold_release",
        "set_mode": "sidefilter_open_identity",
        "risk_shape_mode": "supply_continuity",
        "known_difference": "Keeps the sidefilter_open supply axis that created trades; threshold_release is not retried.",
    },
    {
        "queue_id": "q01_s258_supply_shape_continuity_cross_period",
        "source_variant_id": "run267dl_06_s258_stc_2025h1_supply_sidefilter_open",
        "variant_id": "run267dq_02_s258_stc_2025h1_supply_continuity_sidefilter_open",
        "profile_label": "s258_stc_supply_continuity_sidefilter_open",
        "profile_token": "s258_supply_continuity",
        "materialization_type": "identity_copy_supply_continuity_no_threshold_release",
        "set_mode": "sidefilter_open_identity",
        "risk_shape_mode": "supply_continuity",
        "known_difference": "Keeps 2025H1 sidefilter_open supply evidence without adding a defensive filter stack.",
    },
    {
        "queue_id": "q01_s258_supply_shape_continuity_cross_period",
        "source_variant_id": "run267dl_08_s258_stc_2025h2_supply_sidefilter_open",
        "variant_id": "run267dq_03_s258_stc_2025h2_supply_continuity_sidefilter_open",
        "profile_label": "s258_stc_supply_continuity_sidefilter_open",
        "profile_token": "s258_supply_continuity",
        "materialization_type": "identity_copy_supply_continuity_no_threshold_release",
        "set_mode": "sidefilter_open_identity",
        "risk_shape_mode": "supply_continuity",
        "known_difference": "Keeps 2025H2 sidefilter_open supply evidence and leaves threshold_release pruned.",
    },
    {
        "queue_id": "q02_s258_monday_late_session_dd_taper_cross_period",
        "source_variant_id": "run267dl_04_s258_stc_2023h2_supply_sidefilter_open",
        "variant_id": "run267dq_04_s258_stc_2023h2_monday_late_dd_taper",
        "profile_label": "s258_stc_monday_late_session_dd_taper",
        "profile_token": "s258_dd_taper",
        "materialization_type": "risk_shape_taper_from_sidefilter_open",
        "set_mode": "sidefilter_open_risk_taper",
        "risk_shape_mode": "monday_late_dd_taper",
        "known_difference": "Keeps entries open but reduces risk sizing and max hold; it is a risk-shape taper, not a calendar ban.",
    },
    {
        "queue_id": "q02_s258_monday_late_session_dd_taper_cross_period",
        "source_variant_id": "run267dl_06_s258_stc_2025h1_supply_sidefilter_open",
        "variant_id": "run267dq_05_s258_stc_2025h1_monday_late_dd_taper",
        "profile_label": "s258_stc_monday_late_session_dd_taper",
        "profile_token": "s258_dd_taper",
        "materialization_type": "risk_shape_taper_from_sidefilter_open",
        "set_mode": "sidefilter_open_risk_taper",
        "risk_shape_mode": "monday_late_dd_taper",
        "known_difference": "Tapers risk on 2025H1 sidefilter_open without removing the aggressive supply test.",
    },
    {
        "queue_id": "q02_s258_monday_late_session_dd_taper_cross_period",
        "source_variant_id": "run267dl_08_s258_stc_2025h2_supply_sidefilter_open",
        "variant_id": "run267dq_06_s258_stc_2025h2_monday_late_dd_taper",
        "profile_label": "s258_stc_monday_late_session_dd_taper",
        "profile_token": "s258_dd_taper",
        "materialization_type": "risk_shape_taper_from_sidefilter_open",
        "set_mode": "sidefilter_open_risk_taper",
        "risk_shape_mode": "monday_late_dd_taper",
        "known_difference": "Tapers risk on 2025H2, the weak follow-through period highlighted by run267DO.",
    },
    {
        "queue_id": "q03_s264_lc_defensive_dd_zoom_control",
        "source_variant_id": "run267dl_10_s264_lc_one_stage_dd_demote_audit",
        "variant_id": "run267dq_07_s264_lc_defensive_dd_zoom_control",
        "profile_label": "s264_lc_defensive_dd_zoom_control",
        "profile_token": "s264_lc_dd_zoom",
        "materialization_type": "control_replay_dd_zoom_no_selection",
        "set_mode": "defensive_control_identity",
        "risk_shape_mode": "dd_zoom_control",
        "known_difference": "Replays s264_lc only as a defensive DD zoom control; no safe-control claim is made.",
    },
)

SUPPLY_DIAGNOSTIC_CONFIGS: tuple[dict[str, str], ...] = (
    {
        "queue_id": "q04_s264_aia_s262_lih_supply_rebuild_diagnostic_no_mt5",
        "source_variant_id": "run267dl_01_s264_aia_similar_dual_session_month_survivor",
        "candidate_alias": "s264_aia",
        "diagnostic_label": "aia_similar_survivor_supply_rebuild",
    },
    {
        "queue_id": "q04_s264_aia_s262_lih_supply_rebuild_diagnostic_no_mt5",
        "source_variant_id": "run267dl_02_s264_aia_ablation_dual_session_month_survivor",
        "candidate_alias": "s264_aia",
        "diagnostic_label": "aia_ablation_survivor_supply_rebuild",
    },
    {
        "queue_id": "q04_s264_aia_s262_lih_supply_rebuild_diagnostic_no_mt5",
        "source_variant_id": "run267dl_09_s262_lih_validation_guardrail_crosscheck",
        "candidate_alias": "s262_lih",
        "diagnostic_label": "s262_guardrail_supply_rebuild",
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
        if not line or line.lstrip().startswith(";") or line.strip().startswith("[") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def write_key_values(path: Path, values: Mapping[str, Any], *, header: str | None = None) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = [header] if header else []
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path)}


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_line_containing(text: str, needle: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
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


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if f"`{STATUS}`" in text:
        return text
    if marker not in text:
        return text.rstrip() + "\n" + marker + focus_block
    return text.replace(marker, marker + focus_block, 1)


def split_semicolon(value: Any) -> list[str]:
    return [part.strip() for part in str(value or "").split(";") if part.strip()]


def source_by_id(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {str(row[key]): dict(row) for row in rows}


def attempts_by_variant(rows: Sequence[Mapping[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        result.setdefault(str(row["variant_id"]), []).append(dict(row))
    for attempts in result.values():
        attempts.sort(key=lambda item: (item.get("tier", ""), item.get("attempt_name", "")))
    return result


def materialization_plan_rows(
    queue_rows: Sequence[Mapping[str, str]],
    source_variants: Mapping[str, Mapping[str, str]],
) -> list[dict[str, Any]]:
    queue_by_id = {row["queue_id"]: row for row in queue_rows}
    rows: list[dict[str, Any]] = []
    for order, config in enumerate(ACTIVE_PLAN_CONFIGS, start=1):
        queue = queue_by_id[str(config["queue_id"])]
        source = source_variants[str(config["source_variant_id"])]
        rows.append(
            {
                "plan_id": config["variant_id"],
                "plan_order": order,
                "queue_id": config["queue_id"],
                "priority": queue.get("priority"),
                "workstream": queue.get("workstream"),
                "candidate_id": source.get("candidate_id"),
                "candidate_alias": source.get("candidate_alias"),
                "candidate_role": source.get("candidate_role"),
                "source_run_id": SOURCE_MATERIALIZER_RUN_ID,
                "source_variant_id": source.get("variant_id"),
                "source_profile_label": source.get("profile_label"),
                "source_feature_file": source.get("runtime_feature_file"),
                "source_model_file": source.get("runtime_model_file"),
                "variant_id": config["variant_id"],
                "profile_label": config["profile_label"],
                "profile_token": config["profile_token"],
                "materialization_type": config["materialization_type"],
                "set_mode": config["set_mode"],
                "risk_shape_mode": config["risk_shape_mode"],
                "known_difference": config["known_difference"],
                "materialization_decision": "materialize_feature_model_set_ini_inputs",
                "materialization_boundary": MATERIALIZATION_BOUNDARY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def apply_set_mode(values: dict[str, str], mode: str) -> dict[str, str]:
    updated = dict(values)
    if mode in {"sidefilter_open_identity", "sidefilter_open_risk_taper"}:
        updated["InpShortThreshold"] = "0.52"
        updated["InpLongThreshold"] = "0.50"
        updated["InpFallbackShortThreshold"] = "0.52"
        updated["InpFallbackLongThreshold"] = "0.50"
        updated["InpSideFilterEnabled"] = "false"
        updated["InpBlockShortFeatureRange"] = "false"
        updated["InpBlockLongFeatureRange"] = "false"
        updated["InpSameDirectionReentryCooldownBars"] = "0"
        updated["InpReentryCooldownBars"] = "0"
    if mode == "sidefilter_open_risk_taper":
        updated["InpMaxHoldBars"] = "2"
        updated["InpModelRiskMinPct"] = "0.003"
        updated["InpModelRiskMaxPct"] = "0.0205"
        updated["InpModelRiskFallbackLot"] = "0.15"
        updated["InpAtrStopMultiplier"] = "1.72"
        updated["InpAtrTakeProfitMultiplier"] = "3.35"
    return updated


def target_attempt_name(source_attempt_name: str, source_variant_id: str, target_variant_id: str, profile_token: str) -> str:
    if source_variant_id in source_attempt_name:
        return source_attempt_name.replace(source_variant_id, target_variant_id, 1)
    return f"{target_variant_id}_{profile_token}_{source_attempt_name}"


def copy_variant_inputs(plan: Mapping[str, Any], source_variant: Mapping[str, str]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    variant_id = str(plan["variant_id"])
    alias = str(source_variant["candidate_alias"])
    source_feature = repo_path(str(source_variant["runtime_feature_file"]))
    source_model = repo_path(str(source_variant["runtime_model_file"]))
    if not path_exists(source_feature):
        raise FileNotFoundError(source_feature)
    if not path_exists(source_model):
        raise FileNotFoundError(source_model)

    target_feature = FEATURE_ROOT / alias / variant_id / f"{variant_id}_features.csv"
    target_model = VARIANT_ROOT / alias / variant_id / "models" / f"{variant_id}_model.csv"
    io_path(target_feature.parent).mkdir(parents=True, exist_ok=True)
    io_path(target_model.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source_feature), io_path(target_feature))
    shutil.copy2(io_path(source_model), io_path(target_model))

    common_root = f"{COMMON_ROOT}/{alias}/{variant_id}"
    common_feature = f"{common_root}/features/{target_feature.name}"
    common_model = f"{common_root}/models/{target_model.name}"
    feature_copy = copy_to_common(target_feature, common_feature, COMMON_FILES_ROOT_DEFAULT)
    model_copy = copy_to_common(target_model, common_model, COMMON_FILES_ROOT_DEFAULT)
    feature_order = str(source_variant.get("feature_order", ""))
    feature_count = str(source_variant.get("feature_count") or len(split_semicolon(feature_order)))
    variant = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "source_run_id": SOURCE_MATERIALIZER_RUN_ID,
        "source_variant_id": source_variant["variant_id"],
        "candidate_id": source_variant.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": source_variant.get("candidate_role"),
        "profile_label": plan["profile_label"],
        "profile_token": plan["profile_token"],
        "source_profile_label": source_variant.get("profile_label"),
        "model_materialization_type": plan["materialization_type"],
        "set_mode": plan["set_mode"],
        "risk_shape_mode": plan["risk_shape_mode"],
        "runtime_model_file": rel(target_model),
        "runtime_model_sha256": sha256_file_lf_normalized(target_model),
        "common_model_path": common_model,
        "common_model_sha256": model_copy["sha256"],
        "runtime_feature_file": rel(target_feature),
        "runtime_feature_sha256": sha256_file_lf_normalized(target_feature),
        "common_feature_path": common_feature,
        "common_feature_sha256": feature_copy["sha256"],
        "feature_count": feature_count,
        "feature_order": feature_order,
        "feature_order_hash": source_variant.get("feature_order_hash"),
        "engineered_features": source_variant.get("engineered_features", ""),
        "known_difference": plan["known_difference"],
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    feature = {
        "variant_id": variant_id,
        "candidate_alias": alias,
        "source_feature_file": source_variant.get("runtime_feature_file"),
        "runtime_feature_file": rel(target_feature),
        "runtime_feature_sha256": variant["runtime_feature_sha256"],
        "common_feature_path": common_feature,
        "feature_count": feature_count,
        "feature_order_hash": source_variant.get("feature_order_hash"),
        "feature_copy_status": "copied_from_run267DL_source",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "variant_id": variant_id,
        "candidate_alias": alias,
        "source_model_file": source_variant.get("runtime_model_file"),
        "runtime_model_file": rel(target_model),
        "runtime_model_sha256": variant["runtime_model_sha256"],
        "common_model_path": common_model,
        "model_materialization_type": plan["materialization_type"],
        "model_copy_status": "copied_from_run267DL_source",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return variant, feature, model


def write_attempt_files(
    plan: Mapping[str, Any],
    source_variant: Mapping[str, str],
    source_attempt: Mapping[str, str],
    variant: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    attempt_name = target_attempt_name(
        str(source_attempt["attempt_name"]),
        str(source_variant["variant_id"]),
        str(variant["variant_id"]),
        str(plan["profile_token"]),
    )
    set_values = parse_key_values(repo_path(str(source_attempt["set_path"])))
    set_values = apply_set_mode(set_values, str(plan["set_mode"]))
    tier = source_attempt.get("tier") or set_values.get("InpTierLabel") or "Tier A"
    split = source_attempt.get("split") or set_values.get("InpSplitLabel") or "runtime_gap_aware_followup_scope"
    common_telemetry_root = f"{COMMON_ROOT}/{variant['candidate_alias']}/{variant['variant_id']}/telemetry"
    telemetry = f"{common_telemetry_root}/{attempt_name}_telemetry.csv"
    summary = f"{common_telemetry_root}/{attempt_name}_summary.csv"
    set_values.update(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": tier,
            "InpSplitLabel": split,
            "InpModelPath": variant["common_model_path"],
            "InpModelId": f"{RUN_ID}_{variant['variant_id']}",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": variant["common_feature_path"],
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureCount": variant["feature_count"],
            "InpFeatureOrderHash": variant["feature_order_hash"],
            "InpFallbackFeatureCsvPath": variant["common_feature_path"],
            "InpFallbackFeatureCount": variant["feature_count"],
            "InpFallbackModelPath": variant["common_model_path"],
            "InpFallbackModelId": f"{RUN_ID}_{variant['variant_id']}_fallback_boundary",
            "InpFallbackFeatureOrderHash": variant["feature_order_hash"],
            "InpTelemetryCsvPath": telemetry,
            "InpSummaryCsvPath": summary,
            "InpTelemetryUseCommonFiles": "true",
        }
    )
    set_payload = write_key_values(
        MT5_ROOT / f"{attempt_name}.set",
        set_values,
        header="; generated_by=run267DQ_runtime_gap_aware_fourth_followup_or_prune_materialization",
    )
    ini_values = parse_key_values(repo_path(str(source_attempt["ini_path"])))
    ini_values.update(
        {
            "Report": f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}",
            "ExpertParameters": "ObsidianPrimeV2_RuntimeProbeEA.set",
        }
    )
    ini_payload = write_key_values(MT5_ROOT / f"{attempt_name}.ini", ini_values, header="[Tester]")
    attempt = {
        "attempt_name": attempt_name,
        "variant_id": variant["variant_id"],
        "queue_id": variant["queue_id"],
        "candidate_id": variant["candidate_id"],
        "candidate_alias": variant["candidate_alias"],
        "candidate_role": variant["candidate_role"],
        "profile_label": variant["profile_label"],
        "source_attempt_name": source_attempt.get("attempt_name"),
        "tier": tier,
        "split": split,
        "risk_shape_mode": variant["risk_shape_mode"],
        "set_path": set_payload["path"],
        "set_sha256": set_payload["sha256"],
        "ini_path": ini_payload["path"],
        "ini_sha256": ini_payload["sha256"],
        "telemetry_path": telemetry,
        "summary_path": summary,
        "execution_status": "materialized_execution_pending",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    handoff = {
        "attempt_name": attempt_name,
        "variant_id": variant["variant_id"],
        "candidate_alias": variant["candidate_alias"],
        "set_path": set_payload["path"],
        "ini_path": ini_payload["path"],
        "common_feature_path": variant["common_feature_path"],
        "common_model_path": variant["common_model_path"],
        "common_feature_sha256": variant["common_feature_sha256"],
        "common_model_sha256": variant["common_model_sha256"],
        "handoff_status": "ready_for_mt5_execution",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return attempt, handoff


def materialize_active_variants(
    plans: Sequence[Mapping[str, Any]],
    source_variants: Mapping[str, Mapping[str, str]],
    source_attempts: Mapping[str, Sequence[Mapping[str, str]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    variant_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    risk_rows: list[dict[str, Any]] = []
    for plan in plans:
        source_variant = source_variants[str(plan["source_variant_id"])]
        variant, feature, model = copy_variant_inputs(plan, source_variant)
        for source_attempt in source_attempts[str(plan["source_variant_id"])]:
            attempt, handoff = write_attempt_files(plan, source_variant, source_attempt, variant)
            attempt_rows.append(attempt)
            handoff_rows.append(handoff)
        variant_rows.append(variant)
        feature_rows.append(feature)
        model_rows.append(model)
        risk_rows.append(
            {
                "variant_id": variant["variant_id"],
                "candidate_alias": variant["candidate_alias"],
                "risk_shape_mode": variant["risk_shape_mode"],
                "set_mode": variant["set_mode"],
                "risk_taper_status": "applied" if variant["risk_shape_mode"] == "monday_late_dd_taper" else "not_applicable_supply_continuity_or_control",
                "taper_mechanism": "risk_max_pct_and_hold_bars_reduced_no_calendar_ban"
                if variant["risk_shape_mode"] == "monday_late_dd_taper"
                else "identity_copy",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return variant_rows, feature_rows, model_rows, attempt_rows, handoff_rows, risk_rows


def count_feature_supply(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = [
            column
            for column in (reader.fieldnames or [])
            if column not in {"bar_time_server", "timestamp", "time", "datetime"}
        ]
        row_count = 0
        nonzero_any = 0
        nonzero_by_column = {column: 0 for column in columns}
        for row in reader:
            row_count += 1
            any_nonzero = False
            for column in columns:
                try:
                    value = float(row.get(column, "") or 0.0)
                except ValueError:
                    value = 0.0
                if abs(value) > 1e-12:
                    nonzero_by_column[column] += 1
                    any_nonzero = True
            if any_nonzero:
                nonzero_any += 1
    return {
        "feature_rows": row_count,
        "feature_count": len(columns),
        "nonzero_feature_rows": nonzero_any,
        "nonzero_feature_columns": sum(1 for value in nonzero_by_column.values() if value > 0),
    }


def count_model_direction_rows(path: Path) -> dict[str, Any]:
    rows = read_csv(path)
    score_rows = [row for row in rows if row.get("record_type") == "score"]
    direction_rows = 0
    for row in score_rows:
        try:
            short = float(row.get("score_short", "") or 0.0)
            long = float(row.get("score_long", "") or 0.0)
        except ValueError:
            short = 0.0
            long = 0.0
        if abs(short) > 1e-12 or abs(long) > 1e-12:
            direction_rows += 1
    return {
        "score_rows": len(score_rows),
        "directional_score_rows": direction_rows,
        "model_rows": len(rows),
    }


def supply_diagnostic_rows(
    source_variants: Mapping[str, Mapping[str, str]],
    source_attempts: Mapping[str, Sequence[Mapping[str, str]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for config in SUPPLY_DIAGNOSTIC_CONFIGS:
        source = source_variants[config["source_variant_id"]]
        feature_path = repo_path(str(source["runtime_feature_file"]))
        model_path = repo_path(str(source["runtime_model_file"]))
        feature_stats = count_feature_supply(feature_path)
        model_stats = count_model_direction_rows(model_path)
        attempts = source_attempts.get(str(source["variant_id"]), [])
        supply_status = (
            "feature_and_model_surface_present_but_mt5_supply_unproven"
            if feature_stats["nonzero_feature_rows"] and model_stats["directional_score_rows"]
            else "surface_too_thin_or_missing"
        )
        rows.append(
            {
                "diagnostic_id": f"run267dq_diag_{source['variant_id']}",
                "queue_id": config["queue_id"],
                "candidate_alias": config["candidate_alias"],
                "candidate_id": source.get("candidate_id"),
                "source_variant_id": source.get("variant_id"),
                "source_attempt_count": len(attempts),
                "diagnostic_label": config["diagnostic_label"],
                **feature_stats,
                **model_stats,
                "pre_runtime_supply_status": supply_status,
                "mt5_schedule_status": "held_no_mt5_until_nonzero_signal_supply_proof",
                "next_condition": "reopen only after pre-runtime signal counts are tied to a nonzero runtime handoff plan",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def held_queue_rows(queue_rows: Sequence[Mapping[str, str]], diagnostic_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    queue_by_id = {row["queue_id"]: row for row in queue_rows}
    queue = queue_by_id["q04_s264_aia_s262_lih_supply_rebuild_diagnostic_no_mt5"]
    return [
        {
            "queue_id": queue["queue_id"],
            "priority": queue.get("priority"),
            "candidate_aliases": queue.get("candidate_aliases"),
            "decision": "diagnostic_only_no_mt5_scheduled",
            "why": "run267DP(267DP 실행)가 무거래/런타임 공백 반복을 확인했으므로 MT5 재시도 전에 공급 증명이 필요하다.",
            "diagnostic_rows": len(diagnostic_rows),
            "reopen_condition": "nonzero signal supply proof plus handoff/tooling repair evidence",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def queue_decision_rows(
    queue_rows: Sequence[Mapping[str, str]],
    variant_rows: Sequence[Mapping[str, Any]],
    attempt_rows: Sequence[Mapping[str, Any]],
    held_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    variants_by_queue: dict[str, int] = {}
    attempts_by_queue: dict[str, int] = {}
    for row in variant_rows:
        variants_by_queue[str(row["queue_id"])] = variants_by_queue.get(str(row["queue_id"]), 0) + 1
    for row in attempt_rows:
        attempts_by_queue[str(row["queue_id"])] = attempts_by_queue.get(str(row["queue_id"]), 0) + 1
    held_ids = {row["queue_id"] for row in held_rows}
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        queue_id = str(queue["queue_id"])
        if queue_id in held_ids:
            decision = "held_as_pre_runtime_supply_diagnostic_no_mt5"
            effect = "무거래/런타임 공백 후보를 다시 실행하지 않고 신호 공급 증명으로 분리한다."
        else:
            decision = "materialized_for_mt5_execution"
            effect = "다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 곡선/시간구간/거래품질을 볼 수 있다."
        rows.append(
            {
                "queue_id": queue_id,
                "priority": queue.get("priority"),
                "candidate_aliases": queue.get("candidate_aliases"),
                "workstream": queue.get("workstream"),
                "decision": decision,
                "variant_count": variants_by_queue.get(queue_id, 0),
                "attempt_count": attempts_by_queue.get(queue_id, 0),
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def runtime_contract_rows(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "variant_id": row["variant_id"],
            "candidate_alias": row["candidate_alias"],
            "shared_contract": "US100 M5;RuntimeProbeEA;score_table_csv;feature_order_hash_tracked;set_ini_identity",
            "tier_pair_boundary": TIER_PAIR_BOUNDARY,
            "runtime_claim_boundary": CLAIM_BOUNDARY,
            "runtime_status": "materialized_execution_pending",
        }
        for row in variant_rows
    ]


def experiment_design_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "design_id": "run267dq_runtime_gap_aware_materialization",
            "hypothesis": "s258 sidefilter_open supply can be tested across periods while risk taper checks DD shape without retrying threshold_release.",
            "decision_use": "prepare MT5 batch and supply diagnostic review; no candidate selection.",
            "comparison_baseline": "run267DP materialization queue from run267DO runtime-gap-aware review.",
            "control_variables": "candidate pool; source run267DL feature/model identity; MT5 RuntimeProbeEA; no threshold_release retry.",
            "changed_variables": "s258 supply continuity copies; s258 risk-shape taper set values; s264_lc defensive DD zoom; diagnostic-only held supply rebuild.",
            "sample_scope": "2023H2, 2025H1, 2025H2 for s258; 2024 for s264_lc; no-MT5 diagnostics for s264_aia/s262_lih.",
            "success_criteria": "all intended variants/attempts are materialized with hashes and held diagnostics are explicit.",
            "failure_criteria": "missing source artifact, missing set/ini, accidental threshold_release retry, or hidden selected-candidate claim.",
            "invalid_conditions": "feature/model hash missing, common-files handoff missing, or claim boundary lowered.",
            "stop_conditions": "do not execute held diagnostic candidates until supply proof and tooling handoff are repaired.",
            "evidence_plan": "materialization_plan;variant_manifest;attempt_manifest;supply_diagnostic;runtime_contract;gate_audit;ledgers.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def environment_rows() -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267dq_environment_reproducibility",
            "status": "pass",
            "evidence": "source artifacts copied with sha256; common files handoff written; run_manifest records sources and outputs",
            "effect": "다음 실행자가 같은 입력을 다시 찾을 수 있다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]], diagnostic_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267dq_feature_identity_copy",
            "status": "pass" if feature_rows else "fail",
            "feature_frames": len(feature_rows),
            "diagnostic_rows": len(diagnostic_rows),
            "evidence": "feature_frame_manifest and pre_runtime_supply_diagnostic",
            "effect": "피처 순서(feature order, 피처 순서)를 바꾸지 않고 실행 입력만 이어간다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def runtime_parity_rows(variant_rows: Sequence[Mapping[str, Any]], attempt_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267dq_runtime_handoff_identity",
            "status": "pass" if variant_rows and attempt_rows else "fail",
            "variants": len(variant_rows),
            "attempts": len(attempt_rows),
            "evidence": "variant_manifest;attempt_manifest;runtime_contract;handoff_receipt",
            "runtime_claim": "materialized_execution_pending_only",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def result_judgment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "materialization manifests, handoff receipts, supply diagnostic, gate audit, ledgers",
            "evidence_missing": "MT5 execution output, fresh KPI, balance/equity curve, trade list, Adapter finalization, ONNX parity",
            "judgment_label": "materialization_completed_execution_pending",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": f"variants={counts['variants']};attempts={counts['attempts']};diagnostics={counts['supply_diagnostics']};held={counts['held_rows']}",
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "scope_completion_gate",
            "gate_name": "run267DP queue rows accounted",
            "status": "pass" if counts["queue_rows"] == 4 and counts["materialized_queue_rows"] == 3 and counts["held_rows"] == 1 else "fail",
            "evidence": f"queue_rows={counts['queue_rows']};materialized_queue_rows={counts['materialized_queue_rows']};held_rows={counts['held_rows']}",
            "effect": "실행할 축과 보류할 축을 섞지 않는다.",
        },
        {
            "gate_id": "runtime_evidence_gate",
            "gate_name": "mt5 inputs materialized without execution claim",
            "status": "pass" if counts["attempts"] == 8 else "fail",
            "evidence": f"attempts={counts['attempts']};next_action={NEXT_ACTION}",
            "effect": "아직 KPI(핵심 성과 지표)를 주장하지 않고 실행 준비만 말한다.",
        },
        {
            "gate_id": "artifact_lineage_audit",
            "gate_name": "source and output hashes connected",
            "status": "pass" if counts["variants"] == 7 and counts["handoff_receipts"] == 8 else "fail",
            "evidence": f"variants={counts['variants']};handoff_receipts={counts['handoff_receipts']}",
            "effect": "다음 실행에서 입력 정체성(identity, 정체성)을 잃지 않는다.",
        },
        {
            "gate_id": "final_claim_guard",
            "gate_name": "forbidden claims withheld",
            "status": "pass",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "물질화 결과를 후보 선정이나 ONNX 준비로 과장하지 않는다.",
        },
    ]


def output_paths() -> dict[str, str]:
    return {
        "materialization_plan": rel(MATERIALIZATION_PLAN_PATH),
        "queue_decision": rel(QUEUE_DECISION_PATH),
        "feature_frame_manifest": rel(FEATURE_FRAME_MANIFEST_PATH),
        "model_manifest": rel(MODEL_MANIFEST_PATH),
        "variant_manifest": rel(VARIANT_MANIFEST_PATH),
        "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
        "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
        "held_queue": rel(HELD_QUEUE_PATH),
        "pre_runtime_supply_diagnostic": rel(SUPPLY_DIAGNOSTIC_PATH),
        "handoff_receipt": rel(HANDOFF_RECEIPT_PATH),
        "risk_taper_receipt": rel(RISK_TAPER_RECEIPT_PATH),
        "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
        "environment_reproducibility_receipt": rel(ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH),
        "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
        "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
        "result_judgment": rel(RESULT_JUDGMENT_PATH),
        "gate_audit": rel(GATE_AUDIT_PATH),
        "run_manifest": rel(RUN_MANIFEST_PATH),
        "lineage": rel(LINEAGE_PATH),
        "review_result": rel(REVIEW_RESULT_PATH),
        "report": rel(REPORT_PATH),
    }


def source_paths() -> dict[str, str]:
    return {
        "source_queue": rel(SOURCE_QUEUE_PATH),
        "source_feature_blueprint": rel(SOURCE_FEATURE_BLUEPRINT_PATH),
        "source_branch_decision": rel(SOURCE_BRANCH_DECISION_PATH),
        "source_prune_matrix": rel(SOURCE_PRUNE_MATRIX_PATH),
        "source_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
        "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
        "source_design_report": rel(SOURCE_DESIGN_REPORT_PATH),
        "source_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
        "source_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
        "source_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
        "source_handoff_receipt": rel(SOURCE_HANDOFF_RECEIPT_PATH),
        "source_materialization_report": rel(SOURCE_MATERIALIZATION_REPORT_PATH),
        "producer": rel(PRODUCER_PATH),
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267DQ Runtime Gap Aware Fourth Follow-Up/Prune Materialization(267단계 267DQ 런타임 공백 반영 4차 후속/가지치기 물질화)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- source_materializer(원천 물질화): `{SOURCE_MATERIALIZER_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- variants(변형): `{counts['variants']}`",
        f"- attempts(시도): `{counts['attempts']}`",
        f"- materialized_queue_rows(물질화 대기열 행): `{counts['materialized_queue_rows']}`",
        f"- held_rows(보류 행): `{counts['held_rows']}`",
        f"- supply_diagnostics(공급 진단): `{counts['supply_diagnostics']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "`run267DQ`는 후보를 고른 것이 아니라, `run267DP`가 남긴 다음 실험 대기열을 실제 입력으로 바꾼 실행이다. `s258_stc`는 거래가 생긴 `sidefilter_open(사이드필터 개방)` 축만 2023H2/2025H1/2025H2로 이어가고, `threshold_release(임계값 해제)`는 다시 돌리지 않는다. 별도의 `s258_stc` 위험 완화 축은 필터를 더 붙이는 방식이 아니라 보유 시간과 위험 크기만 줄인 형태다.",
        "",
        "`s264_lc`는 방어 대조(control, 대조)로만 2024 DD(drawdown, 손실폭)를 확대검토한다. `s264_aia`와 `s262_lih`는 현재 경로가 무거래/런타임 공백이므로 MT5(MetaTrader 5, 메타트레이더5)에 넣지 않고 pre-runtime supply diagnostic(런타임 전 공급 진단)으로만 남겼다.",
        "",
        "## Queue Decisions(대기열 판단)",
        "",
        "| queue(대기열) | decision(판단) | variants(변형) | effect(효과) |",
        "| --- | --- | ---: | --- |",
    ]
    for row in result["queue_decision"]:
        lines.append(f"| `{row['queue_id']}` | `{row['decision']}` | `{row['variant_count']}` | {row['effect']} |")
    lines.extend(
        [
            "",
            "## Attempt Inputs(시도 입력)",
            "",
            "| attempt(시도) | candidate(후보) | split(구간) | risk shape(위험 형태) | status(상태) |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in result["attempt_manifest"]:
        lines.append(
            f"| `{row['attempt_name']}` | `{row['candidate_alias']}` | `{row['split']}` | `{row['risk_shape_mode']}` | `{row['execution_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Held Diagnostic(보류 진단)",
            "",
            "| diagnostic(진단) | candidate(후보) | rows(행) | nonzero rows(비영 행) | status(상태) |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in result["pre_runtime_supply_diagnostic"]:
        lines.append(
            f"| `{row['diagnostic_label']}` | `{row['candidate_alias']}` | `{row['feature_rows']}` | `{row['nonzero_feature_rows']}` | `{row['mt5_schedule_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 run(실행)은 materialization only(물질화 전용)이며 아직 fresh KPI(새 핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), trade list(거래 목록)는 없다.",
            "- `q04`는 no-MT5 diagnostic(무 MT5 진단)이다. 실행은 공급 증명과 handoff/tooling repair(인계/도구 수리)가 생긴 뒤에만 재개한다.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_queue(원천 대기열): `{rel(SOURCE_QUEUE_PATH)}`",
            f"- source_variant_manifest(원천 변형 목록): `{rel(SOURCE_VARIANT_MANIFEST_PATH)}`",
            f"- materialization_plan(물질화 계획): `{rel(MATERIALIZATION_PLAN_PATH)}`",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- pre_runtime_supply_diagnostic(런타임 전 공급 진단): `{rel(SUPPLY_DIAGNOSTIC_PATH)}`",
            f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267DQ_producer", "producer_script", PRODUCER_PATH, "Builds run267DQ materialization package."),
        ("stage267_run267DQ_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH, "Materialization plan."),
        ("stage267_run267DQ_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Queue decisions."),
        ("stage267_run267DQ_feature_frame_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Feature frame manifest."),
        ("stage267_run267DQ_model_manifest", "model_manifest", MODEL_MANIFEST_PATH, "Model manifest."),
        ("stage267_run267DQ_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Variant manifest."),
        ("stage267_run267DQ_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Attempt manifest."),
        ("stage267_run267DQ_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract."),
        ("stage267_run267DQ_held_queue", "held_queue", HELD_QUEUE_PATH, "Held queue."),
        ("stage267_run267DQ_supply_diagnostic", "pre_runtime_supply_diagnostic", SUPPLY_DIAGNOSTIC_PATH, "Pre-runtime supply diagnostic."),
        ("stage267_run267DQ_handoff_receipt", "handoff_receipt", HANDOFF_RECEIPT_PATH, "Handoff receipt."),
        ("stage267_run267DQ_risk_taper_receipt", "risk_taper_receipt", RISK_TAPER_RECEIPT_PATH, "Risk taper receipt."),
        ("stage267_run267DQ_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267DQ_environment", "environment_reproducibility_receipt", ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, "Environment receipt."),
        ("stage267_run267DQ_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267DQ_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267DQ_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DQ_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267DQ_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267DQ_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267DQ_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267DQ_report", "review_report", REPORT_PATH, "User-facing report."),
    )
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
        rows.extend(
            [
                {
                    "artifact_id": f"stage267_run267DQ_feature_{row['variant_id']}",
                    "artifact_type": "runtime_feature_frame",
                    "path": row["runtime_feature_file"],
                    "sha256": row["runtime_feature_sha256"],
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created_at,
                    "notes": f"{row['variant_id']} feature frame.",
                },
                {
                    "artifact_id": f"stage267_run267DQ_model_{row['variant_id']}",
                    "artifact_type": "runtime_model_table",
                    "path": row["runtime_model_file"],
                    "sha256": row["runtime_model_sha256"],
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created_at,
                    "notes": f"{row['variant_id']} model table.",
                },
            ]
        )
    for row in result["attempt_manifest"]:
        rows.extend(
            [
                {
                    "artifact_id": f"stage267_run267DQ_set_{row['attempt_name']}",
                    "artifact_type": "mt5_set",
                    "path": row["set_path"],
                    "sha256": row["set_sha256"],
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created_at,
                    "notes": f"{row['attempt_name']} set file.",
                },
                {
                    "artifact_id": f"stage267_run267DQ_ini_{row['attempt_name']}",
                    "artifact_type": "mt5_ini",
                    "path": row["ini_path"],
                    "sha256": row["ini_sha256"],
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created_at,
                    "notes": f"{row['attempt_name']} tester ini.",
                },
            ]
        )
    return rows


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    notes = (
        f"variants={counts['variants']};attempts={counts['attempts']};"
        f"supply_diagnostics={counts['supply_diagnostics']};held_rows={counts['held_rows']};"
        f"next_action={NEXT_ACTION}."
    )
    stage_row = {
        "row_id": "stage267_run267DQ_runtime_gap_aware_fourth_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_fourth_followup_or_prune_materialization",
        "tier_scope": "Tier A and duplicate-boundary rows where source attempts exist; true fallback not claimed",
        "scoreboard": "feature_model_set_ini_materialization_supply_diagnostic",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_mt5_execution_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_runtime_gap_aware_fourth_followup_or_prune_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_fourth_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_fourth_followup_or_prune_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_gap_aware_fourth_followup_or_prune_materialization",
        "tier_scope": "Tier A and duplicate-boundary materialized attempts; diagnostic no-MT5 held rows",
        "kpi_scope": "materialization_manifest_no_mt5_kpi",
        "scoreboard_lane": "runtime_gap_aware_fourth_followup_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={counts['variants']};attempts={counts['attempts']};supply_diagnostics={counts['supply_diagnostics']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at, result), key="artifact_id")


def update_workspace_block(text: str) -> str:
    report_line = f"  run267DQ_runtime_gap_aware_fourth_followup_or_prune_materialization_report_path: {rel(REPORT_PATH)}"
    if report_line not in text:
        text = append_after_contains(
            text,
            "run267DP_runtime_gap_aware_fourth_followup_or_prune_design_report_path",
            report_line,
        )
    output: list[str] = []
    in_block = False
    for line in text.splitlines():
        if line == "stage267_baseline_candidate_racing_protocol:":
            in_block = True
            output.append(line)
            continue
        if in_block and line and not line.startswith(" "):
            in_block = False
        if in_block:
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
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    return "\n".join(output) + "\n"


def update_current_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267DQ_runtime_gap_aware_fourth_followup_or_prune_materialization"
        f"(267DQ 런타임 공백 반영 4차 후속/가지치기 물질화): `{rel(REPORT_PATH)}`"
    )
    summary_line = (
        "- run267DQ_summary(267DQ 요약): Run267DQ(267DQ 실행)는 run267DP(267DP 실행)의 materialization queue(물질화 대기열)를 "
        f"variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, "
        f"supply diagnostics(공급 진단) `{counts['supply_diagnostics']}`개, held rows(보류 행) `{counts['held_rows']}`개로 바꿨다. "
        "Effect(효과): s258_stc 공급 연속성과 위험 완화, s264_lc 방어 대조 DD 확대검토는 MT5 실행 입력으로 만들고, s264_aia/s262_lih는 무거래 경로 재시도 대신 공급 진단으로 묶었다."
    )
    block = "\n".join(
        [
            "Run267DQ(267DQ 실행)는 run267DP(267DP 실행)의 runtime-gap-aware fourth follow-up/prune queue(런타임 공백 반영 4차 후속/가지치기 대기열)를 feature/model/set/ini(피처/모델/설정/초기화) 입력과 pre-runtime supply diagnostic(런타임 전 공급 진단)으로 물질화했다.",
            f"Effect(효과): variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, supply diagnostics(공급 진단) `{counts['supply_diagnostics']}`개를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(
                text,
                "- adapter_under_review(검토 중 어댑터):",
                "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_fourth_followup_or_prune_materialization`",
            )
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267DP_runtime_gap_aware_fourth_followup_or_prune_design.md", report_line)
            text = append_after_contains(text, "run267DP_summary", summary_line)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267DP_runtime_gap_aware_fourth_followup_or_prune_design", report_line)
        else:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "run267DP_runtime_gap_aware_fourth_followup_or_prune_design", report_line)
        text = append_block_once(text, "Run267DQ(267DQ 실행)는 run267DP", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267DQ(267DQ 실행) runtime-gap-aware fourth follow-up/prune materialization"
        f"(런타임 공백 반영 4차 후속/가지치기 물질화) `{STATUS}`. "
        f"Effect(효과): run267DP(267DP 실행)의 queue(대기열)를 variants(변형) `{counts['variants']}`개, "
        f"attempts(시도) `{counts['attempts']}`개, supply diagnostics(공급 진단) `{counts['supply_diagnostics']}`개로 바꿨고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_workspace_block(workspace)
    write_md(WORKSPACE_STATE_PATH, workspace)


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(MATERIALIZATION_PLAN_PATH, result["materialization_plan"])
    write_csv(QUEUE_DECISION_PATH, result["queue_decision"])
    write_csv(FEATURE_FRAME_MANIFEST_PATH, result["feature_frame_manifest"])
    write_csv(MODEL_MANIFEST_PATH, result["model_manifest"])
    write_csv(VARIANT_MANIFEST_PATH, result["variant_manifest"])
    write_csv(ATTEMPT_MANIFEST_PATH, result["attempt_manifest"])
    write_csv(RUNTIME_CONTRACT_PATH, result["runtime_contract"])
    write_csv(HELD_QUEUE_PATH, result["held_queue"])
    write_csv(SUPPLY_DIAGNOSTIC_PATH, result["pre_runtime_supply_diagnostic"])
    write_csv(HANDOFF_RECEIPT_PATH, result["handoff_receipt"])
    write_csv(RISK_TAPER_RECEIPT_PATH, result["risk_taper_receipt"])
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"])
    write_csv(ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, result["environment_reproducibility_receipt"])
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"])
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"])
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"])
    write_csv(GATE_AUDIT_PATH, result["gate_audit"])
    write_json(RUN_MANIFEST_PATH, run_manifest(result))
    write_json(LINEAGE_PATH, lineage(result))
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materializer_run_id": SOURCE_MATERIALIZER_RUN_ID,
        "status": STATUS,
        "created_at_utc": result["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "sources": result["sources"],
        "outputs": result["outputs"],
        "next_action": NEXT_ACTION,
    }


def lineage(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
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
        "availability": "tracked_and_common_files_handoff",
        "lineage_judgment": "connected_with_boundary_no_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }


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
        SOURCE_HANDOFF_RECEIPT_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))

    created_at = utc_now()
    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    source_variants = source_by_id(read_csv(SOURCE_VARIANT_MANIFEST_PATH), "variant_id")
    source_attempts = attempts_by_variant(read_csv(SOURCE_ATTEMPT_MANIFEST_PATH))
    plans = materialization_plan_rows(queue_rows, source_variants)
    variant_rows, feature_rows, model_rows, attempt_rows, handoff_rows, risk_rows = materialize_active_variants(
        plans,
        source_variants,
        source_attempts,
    )
    diagnostic_rows = supply_diagnostic_rows(source_variants, source_attempts)
    held_rows = held_queue_rows(queue_rows, diagnostic_rows)
    queue_decisions = queue_decision_rows(queue_rows, variant_rows, attempt_rows, held_rows)
    counts = {
        "missing_required": len(missing),
        "queue_rows": len(queue_rows),
        "materialized_queue_rows": len({row["queue_id"] for row in variant_rows}),
        "held_rows": len(held_rows),
        "variants": len(variant_rows),
        "attempts": len(attempt_rows),
        "feature_frames": len(feature_rows),
        "models": len(model_rows),
        "handoff_receipts": len(handoff_rows),
        "risk_taper_receipts": len(risk_rows),
        "supply_diagnostics": len(diagnostic_rows),
        "s258_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s258_stc"),
        "s258_attempts": sum(1 for row in attempt_rows if row["candidate_alias"] == "s258_stc"),
        "s264_lc_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s264_lc"),
        "s264_lc_attempts": sum(1 for row in attempt_rows if row["candidate_alias"] == "s264_lc"),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    result: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materializer_run_id": SOURCE_MATERIALIZER_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "counts": counts,
        "sources": source_paths(),
        "outputs": output_paths(),
        "materialization_plan": plans,
        "queue_decision": queue_decisions,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "runtime_contract": runtime_contract_rows(variant_rows),
        "held_queue": held_rows,
        "pre_runtime_supply_diagnostic": diagnostic_rows,
        "handoff_receipt": handoff_rows,
        "risk_taper_receipt": risk_rows,
        "experiment_design_receipt": experiment_design_rows(queue_rows),
        "environment_reproducibility_receipt": environment_rows(),
        "data_integrity_receipt": data_integrity_rows(feature_rows, diagnostic_rows),
        "runtime_parity_receipt": runtime_parity_rows(variant_rows, attempt_rows),
        "result_judgment": result_judgment_rows(counts),
        "gate_audit": gate_audit_rows(counts),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    return result


def execute() -> dict[str, Any]:
    result = build_result()
    write_outputs(result)
    update_ledgers(str(result["created_at_utc"]), result)
    update_current_docs(result)
    return result


def main() -> int:
    result = execute()
    counts = result["counts"]
    print(
        json.dumps(
            {
                "status": result["status"],
                "variants": counts["variants"],
                "attempts": counts["attempts"],
                "held_rows": counts["held_rows"],
                "supply_diagnostics": counts["supply_diagnostics"],
                "s258_variants": counts["s258_variants"],
                "s264_lc_variants": counts["s264_lc_variants"],
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
