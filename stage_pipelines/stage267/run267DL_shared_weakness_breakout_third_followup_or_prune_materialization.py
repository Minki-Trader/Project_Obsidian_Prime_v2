from __future__ import annotations

import csv
import json
import math
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
    copy_to_common,
)
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import (
    run267DH_shared_weakness_breakout_second_followup_or_prune_materialization as source_materializer,
)
from stage_pipelines.stage267 import (
    run267DK_shared_weakness_breakout_third_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267DL"
RUN_ID = "run267DL_stage267_shared_weakness_breakout_third_followup_or_prune_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZER_RUN_ID = source_materializer.RUN_ID
STATUS = "run267DL_shared_weakness_breakout_third_followup_or_prune_materialized_execution_pending"
JUDGMENT = "third_followup_or_prune_materialized_no_candidate_selection"
NEXT_ACTION = "run267DM_execute_shared_weakness_breakout_third_followup_or_prune_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_third_followup_or_prune_materialization"
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
HANDOFF_RECEIPT_PATH = RUN_ROOT / "handoff_receipt.csv"
ADAPTER_HANDOFF_GAP_RECEIPT_PATH = RUN_ROOT / "adapter_handoff_gap_receipt.csv"
FEATURE_MUTATION_RECEIPT_PATH = RUN_ROOT / "feature_mutation_receipt.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH = RUN_ROOT / "environment_reproducibility_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DL_shared_weakness_breakout_third_followup_or_prune_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DL_shared_weakness_breakout_third_followup_or_prune_materialization.py")

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

COMMON_ROOT = "OPV2/s267dl/run267DL_shared_weakness_third_followup_or_prune"
EXPLORATION_LABEL = "stage267_BaselineRacing__SharedWeaknessThirdFollowupOrPruneMaterialization"
MATERIALIZATION_BOUNDARY = "materialization_only_no_candidate_selection_no_selected_research_baseline_no_onnx"
TIER_PAIR_BOUNDARY = (
    "Tier A and duplicate-boundary Tier A+B are kept only where source attempts exist; "
    "true Tier B fallback and actual routed total remain unclaimed"
)

PLAN_CONFIGS: tuple[dict[str, Any], ...] = (
    {
        "queue_id": "dk_q01_s264_aia_dual_survivor_ablation_replacement",
        "source_variant_id": "run267dh_01_s264_aia_similar_survivor_gate",
        "variant_id": "run267dl_01_s264_aia_similar_dual_session_month_survivor",
        "profile_label": "s264_aia_similar_dual_session_month_survivor",
        "profile_token": "aia_similar_dual_survivor",
        "materialization_type": "source_replay_dual_survivor_gate_no_signal_mutation",
        "set_mode": "survivor_replay",
        "known_difference": "Rebinds run267DH similar replacement survivor to run267DK dual session/month survivor gate; no calendar-only filter.",
    },
    {
        "queue_id": "dk_q01_s264_aia_dual_survivor_ablation_replacement",
        "source_variant_id": "run267dh_02_s264_aia_ablation_survivor_gate",
        "variant_id": "run267dl_02_s264_aia_ablation_dual_session_month_survivor",
        "profile_label": "s264_aia_ablation_dual_session_month_survivor",
        "profile_token": "aia_ablation_dual_survivor",
        "materialization_type": "source_replay_dual_ablation_survivor_gate_no_signal_mutation",
        "set_mode": "survivor_replay",
        "known_difference": "Rebinds run267DH ablation survivor to run267DK dual session/month survivor gate; no new safety filter.",
    },
    {
        "queue_id": "dk_q02_s258_explosive_supply_expansion_stress",
        "source_variant_id": "run267dh_04_s258_stc_2023h2_thin_supply_impulse",
        "variant_id": "run267dl_03_s258_stc_2023h2_supply_threshold_release",
        "profile_label": "s258_stc_explosive_supply_threshold_release",
        "profile_token": "s258_threshold_release",
        "materialization_type": "execution_supply_expansion_threshold_release",
        "set_mode": "threshold_release",
        "known_difference": "Aggressively lowers entry thresholds and same-direction cooldown to test trade supply, without adding defensive filters.",
    },
    {
        "queue_id": "dk_q02_s258_explosive_supply_expansion_stress",
        "source_variant_id": "run267dh_04_s258_stc_2023h2_thin_supply_impulse",
        "variant_id": "run267dl_04_s258_stc_2023h2_supply_sidefilter_open",
        "profile_label": "s258_stc_explosive_supply_sidefilter_open",
        "profile_token": "s258_sidefilter_open",
        "materialization_type": "execution_supply_expansion_sidefilter_open",
        "set_mode": "sidefilter_open",
        "known_difference": "Opens the side filter and cooldown to test whether sparse high-PF rows can become real supply.",
    },
    {
        "queue_id": "dk_q02_s258_explosive_supply_expansion_stress",
        "source_variant_id": "run267dh_05_s258_stc_2025h1_thin_supply_impulse",
        "variant_id": "run267dl_05_s258_stc_2025h1_supply_threshold_release",
        "profile_label": "s258_stc_explosive_supply_threshold_release",
        "profile_token": "s258_threshold_release",
        "materialization_type": "execution_supply_expansion_threshold_release",
        "set_mode": "threshold_release",
        "known_difference": "Aggressively lowers entry thresholds and same-direction cooldown to test 2025H1 trade supply.",
    },
    {
        "queue_id": "dk_q02_s258_explosive_supply_expansion_stress",
        "source_variant_id": "run267dh_05_s258_stc_2025h1_thin_supply_impulse",
        "variant_id": "run267dl_06_s258_stc_2025h1_supply_sidefilter_open",
        "profile_label": "s258_stc_explosive_supply_sidefilter_open",
        "profile_token": "s258_sidefilter_open",
        "materialization_type": "execution_supply_expansion_sidefilter_open",
        "set_mode": "sidefilter_open",
        "known_difference": "Opens the side filter and cooldown for 2025H1; this is an aggressive stress, not a safety patch.",
    },
    {
        "queue_id": "dk_q02_s258_explosive_supply_expansion_stress",
        "source_variant_id": "run267dh_06_s258_stc_2025h2_thin_supply_impulse",
        "variant_id": "run267dl_07_s258_stc_2025h2_supply_threshold_release",
        "profile_label": "s258_stc_explosive_supply_threshold_release",
        "profile_token": "s258_threshold_release",
        "materialization_type": "execution_supply_expansion_threshold_release",
        "set_mode": "threshold_release",
        "known_difference": "Aggressively lowers entry thresholds and same-direction cooldown to test 2025H2 trade supply.",
    },
    {
        "queue_id": "dk_q02_s258_explosive_supply_expansion_stress",
        "source_variant_id": "run267dh_06_s258_stc_2025h2_thin_supply_impulse",
        "variant_id": "run267dl_08_s258_stc_2025h2_supply_sidefilter_open",
        "profile_label": "s258_stc_explosive_supply_sidefilter_open",
        "profile_token": "s258_sidefilter_open",
        "materialization_type": "execution_supply_expansion_sidefilter_open",
        "set_mode": "sidefilter_open",
        "known_difference": "Opens the side filter and cooldown for 2025H2; no defensive filter is added.",
    },
    {
        "queue_id": "dk_q03_s262_lih_validation_guardrail_crosscheck",
        "source_variant_id": "run267dh_03_s262_lih_validation_control_crosscheck",
        "variant_id": "run267dl_09_s262_lih_validation_guardrail_crosscheck",
        "profile_label": "s262_lih_validation_guardrail_crosscheck",
        "profile_token": "s262_guardrail",
        "materialization_type": "source_replay_validation_guardrail_no_signal_mutation",
        "set_mode": "guardrail_replay",
        "known_difference": "Keeps s262_lih beside the aggressive branch as a validation-heavy guardrail, not a selected candidate.",
    },
    {
        "queue_id": "dk_q04_s264_lc_one_stage_dd_demote_audit",
        "source_variant_id": "run267dh_07_s264_lc_weekday_dd_deescalation",
        "variant_id": "run267dl_10_s264_lc_one_stage_dd_demote_audit",
        "profile_label": "s264_lc_one_stage_dd_demote_audit",
        "profile_token": "s264_lc_demote_audit",
        "materialization_type": "source_replay_one_stage_dd_demote_audit_no_signal_mutation",
        "set_mode": "demote_audit_replay",
        "known_difference": "Runs only one bounded DD/Monday audit for s264_lc and does not preserve a safe-control claim.",
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


def plan_rows(queue_rows: Sequence[Mapping[str, str]], source_variants: Mapping[str, Mapping[str, str]]) -> list[dict[str, Any]]:
    queue_by_id = {row["queue_id"]: row for row in queue_rows}
    rows: list[dict[str, Any]] = []
    for order, config in enumerate(PLAN_CONFIGS, start=1):
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
                "known_difference": config["known_difference"],
                "materialization_decision": "materialize_feature_model_set_ini_inputs",
                "materialization_boundary": MATERIALIZATION_BOUNDARY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def apply_set_mode(values: dict[str, str], mode: str) -> dict[str, str]:
    updated = dict(values)
    if mode == "threshold_release":
        updated["InpShortThreshold"] = "0.50"
        updated["InpLongThreshold"] = "0.50"
        updated["InpFallbackShortThreshold"] = "0.50"
        updated["InpFallbackLongThreshold"] = "0.50"
        updated["InpSameDirectionReentryCooldownBars"] = "0"
        updated["InpReentryCooldownBars"] = "0"
    elif mode == "sidefilter_open":
        updated["InpShortThreshold"] = "0.52"
        updated["InpLongThreshold"] = "0.50"
        updated["InpFallbackShortThreshold"] = "0.52"
        updated["InpFallbackLongThreshold"] = "0.50"
        updated["InpSideFilterEnabled"] = "false"
        updated["InpBlockShortFeatureRange"] = "false"
        updated["InpBlockLongFeatureRange"] = "false"
        updated["InpSameDirectionReentryCooldownBars"] = "0"
        updated["InpReentryCooldownBars"] = "0"
    return updated


def target_attempt_name(source_attempt_name: str, source_variant_id: str, target_variant_id: str) -> str:
    if source_variant_id in source_attempt_name:
        return source_attempt_name.replace(source_variant_id, target_variant_id, 1)
    return f"{target_variant_id}_{source_attempt_name}"


def copy_feature_and_model(plan: Mapping[str, Any], source_variant: Mapping[str, str]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    variant_id = str(plan["variant_id"])
    alias = str(source_variant["candidate_alias"])
    source_feature = repo_path(str(source_variant["runtime_feature_file"]))
    source_model = repo_path(str(source_variant["runtime_model_file"]))
    if not path_exists(source_feature):
        raise FileNotFoundError(source_feature)
    if not path_exists(source_model):
        raise FileNotFoundError(source_model)

    feature_order = split_semicolon(source_variant.get("feature_order"))
    frame = pd.read_csv(io_path(source_feature), encoding="utf-8-sig")
    missing_features = [column for column in feature_order if column not in frame.columns]
    if missing_features:
        raise RuntimeError(f"missing runtime feature columns for {variant_id}: {missing_features}")
    feature_order_hash = ordered_hash(feature_order)
    if feature_order_hash != source_variant.get("feature_order_hash"):
        raise RuntimeError(f"feature order hash mismatch for {variant_id}")

    target_feature = FEATURE_ROOT / alias / variant_id / f"{variant_id}_features.csv"
    target_model = VARIANT_ROOT / alias / variant_id / "models" / f"{variant_id}_model.csv"
    io_path(target_feature.parent).mkdir(parents=True, exist_ok=True)
    io_path(target_model.parent).mkdir(parents=True, exist_ok=True)
    frame.loc[:, ["bar_time_server", *feature_order]].to_csv(
        io_path(target_feature),
        index=False,
        encoding="utf-8",
        lineterminator="\n",
    )
    shutil.copy2(io_path(source_model), io_path(target_model))

    common_root = f"{COMMON_ROOT}/{alias}/{variant_id}"
    common_feature_path = f"{common_root}/features/{target_feature.name}"
    common_model_path = f"{common_root}/models/{target_model.name}"
    common_feature = copy_to_common(target_feature, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(target_model, common_model_path, COMMON_FILES_ROOT_DEFAULT)

    variant_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "source_run_id": SOURCE_MATERIALIZER_RUN_ID,
        "source_variant_id": source_variant["variant_id"],
        "candidate_id": source_variant.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": source_variant.get("candidate_role"),
        "profile_label": plan["profile_label"],
        "source_profile_label": source_variant.get("profile_label"),
        "model_materialization_type": plan["materialization_type"],
        "set_mode": plan["set_mode"],
        "runtime_model_file": rel(target_model),
        "runtime_model_sha256": sha256_file_lf_normalized(target_model),
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "runtime_feature_file": rel(target_feature),
        "runtime_feature_sha256": sha256_file_lf_normalized(target_feature),
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "feature_count": len(feature_order),
        "feature_order": ";".join(feature_order),
        "feature_order_hash": feature_order_hash,
        "engineered_features": source_variant.get("engineered_features", ""),
        "known_difference": plan["known_difference"],
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    feature_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "candidate_alias": alias,
        "source_run_id": SOURCE_MATERIALIZER_RUN_ID,
        "source_variant_id": source_variant["variant_id"],
        "source_feature_file": rel(source_feature),
        "source_feature_sha256": sha256_file_lf_normalized(source_feature),
        "runtime_feature_file": rel(target_feature),
        "runtime_feature_sha256": sha256_file_lf_normalized(target_feature),
        "common_feature_path": common_feature_path,
        "common_feature_sha256": common_feature["sha256"],
        "feature_count": len(feature_order),
        "feature_order_hash": feature_order_hash,
        "rows": int(len(frame)),
        "first_bar_time_server": str(frame["bar_time_server"].iloc[0]) if len(frame) else "",
        "last_bar_time_server": str(frame["bar_time_server"].iloc[-1]) if len(frame) else "",
        "duplicate_bar_time_rows": int(frame["bar_time_server"].duplicated().sum()) if len(frame) else 0,
        "runtime_missing_feature_cells": int(frame.loc[:, feature_order].isna().sum().sum()) if len(frame) else 0,
        "feature_frame_status": "copied_and_hash_checked",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_row = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "candidate_alias": alias,
        "source_run_id": SOURCE_MATERIALIZER_RUN_ID,
        "source_variant_id": source_variant["variant_id"],
        "source_model_file": rel(source_model),
        "source_model_sha256": sha256_file_lf_normalized(source_model),
        "runtime_model_file": rel(target_model),
        "runtime_model_sha256": sha256_file_lf_normalized(target_model),
        "common_model_path": common_model_path,
        "common_model_sha256": common_model["sha256"],
        "model_materialization_type": plan["materialization_type"],
        "model_backend": "ebm_table",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return variant_row, feature_row, model_row


def write_attempts(
    plan: Mapping[str, Any],
    source_variant: Mapping[str, str],
    source_attempts: Sequence[Mapping[str, str]],
    variant_row: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    handoffs: list[dict[str, Any]] = []
    for source_attempt in source_attempts:
        source_set = repo_path(str(source_attempt["set_path"]))
        source_ini = repo_path(str(source_attempt["ini_path"]))
        attempt_name = target_attempt_name(
            str(source_attempt["attempt_name"]),
            str(source_variant["variant_id"]),
            str(plan["variant_id"]),
        )
        common_telemetry_root = f"{COMMON_ROOT}/{variant_row['candidate_alias']}/{variant_row['variant_id']}/telemetry"
        telemetry = f"{common_telemetry_root}/{attempt_name}_telemetry.csv"
        summary = f"{common_telemetry_root}/{attempt_name}_summary.csv"
        set_values = parse_key_values(source_set)
        set_values = apply_set_mode(set_values, str(plan["set_mode"]))
        tier = source_attempt.get("tier") or set_values.get("InpTierLabel") or "Tier A"
        split = source_attempt.get("split") or set_values.get("InpSplitLabel") or "run267DL_materialized_scope"
        set_values.update(
            {
                "InpRunId": RUN_ID,
                "InpExplorationLabel": EXPLORATION_LABEL,
                "InpTierLabel": tier,
                "InpSplitLabel": split,
                "InpModelPath": variant_row["common_model_path"],
                "InpModelId": f"{RUN_ID}_{variant_row['variant_id']}",
                "InpModelUseCommonFiles": "true",
                "InpFeatureCsvPath": variant_row["common_feature_path"],
                "InpFeatureCsvUseCommonFiles": "true",
                "InpFeatureCount": variant_row["feature_count"],
                "InpFeatureOrderHash": variant_row["feature_order_hash"],
                "InpFallbackFeatureCsvPath": variant_row["common_feature_path"],
                "InpFallbackFeatureCount": variant_row["feature_count"],
                "InpFallbackModelPath": variant_row["common_model_path"],
                "InpFallbackModelId": f"{RUN_ID}_{variant_row['variant_id']}_fallback_boundary",
                "InpFallbackFeatureOrderHash": variant_row["feature_order_hash"],
                "InpTelemetryCsvPath": telemetry,
                "InpSummaryCsvPath": summary,
                "InpTelemetryUseCommonFiles": "true",
            }
        )
        set_payload = write_key_values(
            MT5_ROOT / f"{attempt_name}.set",
            set_values,
            header="; generated_by=run267DL_shared_weakness_breakout_third_followup_or_prune_materialization",
        )
        ini_values = parse_key_values(source_ini)
        ini_values.update({"Report": f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}"})
        ini_payload = write_key_values(MT5_ROOT / f"{attempt_name}.ini", ini_values, header="[Tester]")
        attempt_row = {
            "attempt_name": attempt_name,
            "variant_id": variant_row["variant_id"],
            "queue_id": plan["queue_id"],
            "source_run_id": SOURCE_MATERIALIZER_RUN_ID,
            "source_variant_id": source_variant["variant_id"],
            "source_attempt_name": source_attempt.get("attempt_name"),
            "candidate_id": variant_row.get("candidate_id"),
            "candidate_alias": variant_row.get("candidate_alias"),
            "candidate_role": variant_row.get("candidate_role"),
            "profile_label": variant_row.get("profile_label"),
            "tier": tier,
            "attempt_role": source_attempt.get("attempt_role"),
            "target_period": source_attempt.get("target_period"),
            "split": split,
            "record_view_prefix": source_attempt.get("record_view_prefix"),
            "set_mode": plan["set_mode"],
            "set_path": set_payload["path"],
            "set_sha256": set_payload["sha256"],
            "ini_path": ini_payload["path"],
            "ini_sha256": ini_payload["sha256"],
            "common_telemetry_path": telemetry,
            "common_summary_path": summary,
            "common_feature_path": variant_row["common_feature_path"],
            "common_model_path": variant_row["common_model_path"],
            "tier_pair_boundary": TIER_PAIR_BOUNDARY,
            "execution_status": "materialized_execution_pending",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        attempts.append(attempt_row)
        handoffs.append(
            {
                "receipt_id": f"run267dl_handoff_{attempt_name}",
                "variant_id": variant_row["variant_id"],
                "attempt_name": attempt_name,
                "candidate_alias": variant_row["candidate_alias"],
                "feature_order_hash": variant_row["feature_order_hash"],
                "model_sha256": variant_row["runtime_model_sha256"],
                "set_sha256": set_payload["sha256"],
                "ini_sha256": ini_payload["sha256"],
                "handoff_status": "model_feature_set_ini_manifest_ready",
                "runtime_claim": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    contract = {
        "variant_id": variant_row["variant_id"],
        "candidate_id": variant_row.get("candidate_id"),
        "candidate_alias": variant_row.get("candidate_alias"),
        "candidate_role": variant_row.get("candidate_role"),
        "profile_label": variant_row.get("profile_label"),
        "source_profile_label": source_variant.get("profile_label"),
        "source_run_id": SOURCE_MATERIALIZER_RUN_ID,
        "shared_contract": "US100 M5; MT5 RuntimeProbeEA handoff; score table model; feature order hash tracked",
        "feature_count": variant_row["feature_count"],
        "feature_order_hash": variant_row["feature_order_hash"],
        "model_backend": "ebm_table",
        "model_materialization_type": variant_row["model_materialization_type"],
        "set_mode": plan["set_mode"],
        "known_difference": variant_row["known_difference"],
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "runtime_claim_boundary": CLAIM_BOUNDARY,
    }
    return attempts, contract, handoffs


def queue_decision_rows(queue_rows: Sequence[Mapping[str, str]], variants: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    variant_counts: dict[str, int] = {}
    attempt_counts: dict[str, int] = {}
    for variant in variants:
        queue_id = str(variant["queue_id"])
        variant_counts[queue_id] = variant_counts.get(queue_id, 0) + 1
    for plan in PLAN_CONFIGS:
        source_attempts = read_csv(SOURCE_ATTEMPT_MANIFEST_PATH)
        count = sum(1 for row in source_attempts if row.get("variant_id") == plan["source_variant_id"])
        attempt_counts[str(plan["queue_id"])] = attempt_counts.get(str(plan["queue_id"]), 0) + count
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        queue_id = queue["queue_id"]
        if queue_id == "dk_q05_adapter_handoff_gap_receipts":
            decision = "receipt_only_materialized(영수증 전용 물질화)"
            why = "Adapter(어댑터) 후보가 아니라 생존 후보의 handoff gap(인계 공백)을 추적한다."
            count = 0
            attempts = 0
        else:
            decision = "materialized_execution_pending(실행 대기 물질화)"
            why = queue.get("materialization_instruction", "")
            count = variant_counts.get(queue_id, 0)
            attempts = attempt_counts.get(queue_id, 0)
        rows.append(
            {
                "queue_id": queue_id,
                "priority": queue.get("priority"),
                "candidate_aliases": queue.get("candidate_aliases"),
                "workstream": queue.get("workstream"),
                "run267DL_decision": decision,
                "variant_count": count,
                "attempt_count": attempts,
                "why": why,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def held_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "held_id": "run267dl_hold_s264_aih_rebuild_only",
            "candidate_alias": "s264_aih",
            "candidate_id": "s264_allow_inner_high_quarter",
            "held_reason": "run267DK(267DK 실행)이 s264_aih를 같은 repair loop(수리 반복)로 끌지 말고 새 supply/impulse structure(공급/충격 구조) 전까지 보류하라고 정했다.",
            "reopen_condition": "기존 threshold(임계값) 미세 조정이 아닌 새 구조가 있을 때만 재개한다.",
            "next_use": "held_rebuild_only(보류 재구축 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def feature_mutation_rows(variants: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in variants:
        set_mode = str(row.get("set_mode"))
        if set_mode in {"threshold_release", "sidefilter_open"}:
            mutation_type = "execution_supply_parameter_release_no_feature_order_change"
            effect = "Feature(피처)와 model(모델)은 유지하고 set(설정)에서 공급을 넓혀 trade count(거래 수)를 압박한다."
        else:
            mutation_type = "source_replay_no_signal_mutation"
            effect = "Source feature/model(원천 피처/모델)을 보존하고 연구 역할과 handoff identity(인계 정체성)만 바꾼다."
        rows.append(
            {
                "mutation_id": f"run267dl_mutation_{row['variant_id']}",
                "variant_id": row["variant_id"],
                "candidate_alias": row["candidate_alias"],
                "mutation_type": mutation_type,
                "set_mode": set_mode,
                "source_variant_id": row["source_variant_id"],
                "feature_order_hash": row["feature_order_hash"],
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def adapter_handoff_gap_rows(variants: Sequence[Mapping[str, Any]], handoffs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    target_aliases = ("s264_aia", "s258_stc", "s262_lih")
    rows: list[dict[str, Any]] = []
    for alias in target_aliases:
        alias_variants = [row for row in variants if row.get("candidate_alias") == alias]
        alias_handoffs = [row for row in handoffs if row.get("candidate_alias") == alias]
        rows.append(
            {
                "receipt_id": f"run267dl_adapter_gap_{alias}",
                "candidate_alias": alias,
                "variant_count": len(alias_variants),
                "attempt_count": len(alias_handoffs),
                "feature_order_hashes": ";".join(sorted({str(row["feature_order_hash"]) for row in alias_variants})),
                "model_hashes": ";".join(sorted({str(row["runtime_model_sha256"]) for row in alias_variants})),
                "handoff_ready": "model_feature_set_ini_manifest_ready" if alias_handoffs else "missing_attempt_handoff",
                "remaining_gap": "MT5 execution(MT5 실행);balance/equity review(잔액/평가금 검토);Adapter package(어댑터 패키지);runtime reproduction(런타임 재현);ONNX parity(ONNX 동등성)",
                "runtime_claim": "not_claimed",
                "onnx_readiness": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def experiment_design_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        rows.append(
            {
                "queue_id": queue["queue_id"],
                "hypothesis": queue.get("hypothesis"),
                "decision_use": queue.get("decision_use"),
                "comparison_baseline": queue.get("comparison_baseline"),
                "control_variables": queue.get("control_variables"),
                "changed_variables": queue.get("changed_variables"),
                "sample_scope": queue.get("sample_scope"),
                "success_criteria": queue.get("success_criteria"),
                "failure_criteria": queue.get("failure_criteria"),
                "invalid_conditions": queue.get("invalid_conditions"),
                "stop_conditions": queue.get("stop_conditions"),
                "evidence_plan": queue.get("evidence_plan"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def environment_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267dl_environment_reproducibility",
            "python_version": sys.version.split()[0],
            "producer": rel(PRODUCER_PATH),
            "source_materializer": rel(source_materializer.PRODUCER_PATH),
            "common_files_root": str(COMMON_FILES_ROOT_DEFAULT),
            "status": "reproducible_from_committed_script_and_registered_inputs",
            "effect": "같은 source manifest(원천 목록)와 producer script(생산 스크립트)로 materialization(물질화)을 다시 만들 수 있다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "variant_id": row["variant_id"],
            "candidate_alias": row["candidate_alias"],
            "rows": row["rows"],
            "first_bar_time_server": row["first_bar_time_server"],
            "last_bar_time_server": row["last_bar_time_server"],
            "duplicate_bar_time_rows": row["duplicate_bar_time_rows"],
            "runtime_missing_feature_cells": row["runtime_missing_feature_cells"],
            "status": "pass" if int(row["runtime_missing_feature_cells"]) == 0 else "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in feature_rows
    ]


def runtime_parity_rows(variants: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "variant_id": row["variant_id"],
            "candidate_alias": row["candidate_alias"],
            "feature_order_hash": row["feature_order_hash"],
            "model_sha256": row["runtime_model_sha256"],
            "common_feature_path": row["common_feature_path"],
            "common_model_path": row["common_model_path"],
            "parity_status": "handoff_ready_no_runtime_execution_yet",
            "missing_for_runtime_reproduction": "MT5 execution output(MT5 실행 출력);tester report(테스터 보고서);runtime reproduction(런타임 재현)",
            "runtime_authority": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in variants
    ]


def result_judgment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267DL shared weakness third follow-up/prune materialization(267DL 공유 약점 3차 후속/가지치기 물질화)",
            "evidence_available": f"variants={counts['variants']};attempts={counts['attempts']};adapter_gap_receipts={counts['adapter_gap_receipts']};held_rows={counts['held_rows']}",
            "evidence_missing": "MT5 execution(MT5 실행), balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), Adapter package(어댑터 패키지), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성)",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "실험 입력을 만들었을 뿐이며, 후보 선택이나 ONNX(ONNX 준비)는 아니다.",
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    gates = [
        (
            "source_queue_and_manifests_present",
            counts["missing_required"] == 0 and counts["queue_rows"] == 5,
            "run267DK queue(대기열)와 run267DH source manifest(원천 목록)가 모두 있다.",
        ),
        (
            "s264_aia_dual_survivor_materialized",
            counts["s264_aia_variants"] == 2 and counts["s264_aia_attempts"] == 4,
            "s264_aia similar/ablation(유사/제거) 생존 관문이 둘 다 물질화됐다.",
        ),
        (
            "aggressive_s258_supply_expansion_materialized",
            counts["s258_variants"] == 6 and counts["s258_attempts"] == 6,
            "s258_stc는 세 기간에 threshold release(임계값 개방)와 sidefilter open(사이드필터 개방)을 강행했다.",
        ),
        (
            "guardrail_and_demote_audit_materialized",
            counts["s262_variants"] == 1 and counts["s264_lc_variants"] == 1,
            "s262_lih guardrail(가드레일)과 s264_lc demote audit(강등 감사)이 들어갔다.",
        ),
        (
            "adapter_handoff_gap_receipts_present",
            counts["adapter_gap_receipts"] == 3,
            "s264_aia, s258_stc, s262_lih의 Adapter handoff gap(어댑터 인계 공백)을 기록했다.",
        ),
        (
            "s264_aih_rebuild_only_hold_present",
            counts["held_rows"] == 1,
            "s264_aih는 repair loop(수리 반복)가 아니라 rebuild-only hold(재구축 전용 보류)로 남겼다.",
        ),
        (
            "no_selection_or_onnx_claim",
            counts["selected_candidate"] == "none"
            and counts["selected_research_baseline"] == "none"
            and counts["onnx_readiness"] == "not_claimed"
            and counts["goal_achieve"] == "not_claimed",
            "후보 선택, 연구 기준 후보 선택, ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "pass" if passed else "fail",
            "evidence": evidence,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, evidence in gates
    ]


def run_manifest(created_at: str, result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "parent_run_id": PARENT_RUN_ID,
        "source_materializer_run_id": SOURCE_MATERIALIZER_RUN_ID,
        "created_at_utc": created_at,
        "purpose": "Materialize run267DK third follow-up/prune queue into MT5 execution inputs.",
        "counts": result["counts"],
        "sources": result["sources"],
        "outputs": result["outputs"],
        "next_action": NEXT_ACTION,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def lineage(created_at: str, result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "lineage_id": "stage267_run267DL_lineage",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
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
        "lineage_judgment": "connected_with_boundary_no_candidate_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267DL Shared Weakness Third Follow-up/Prune Materialization(267단계 267DL 공유 약점 3차 후속/가지치기 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- source_materializer(원천 물질화 실행): `{SOURCE_MATERIALIZER_RUN_ID}`",
        f"- variants(변형): `{counts['variants']}`",
        f"- attempts(시도): `{counts['attempts']}`",
        f"- aggressive_s258_variants(공격형 s258 변형): `{counts['s258_variants']}`",
        f"- adapter_handoff_gap_receipts(어댑터 인계 공백 영수증): `{counts['adapter_gap_receipts']}`",
        f"- held_rows(보류 행): `{counts['held_rows']}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267DL(267DL 실행)은 run267DK(267DK 실행)의 설계를 실제 MT5(MetaTrader 5, 메타트레이더5) 입력으로 바꿨다. s258_stc는 방어 필터를 붙이지 않고 threshold release(임계값 개방)와 sidefilter open(사이드필터 개방)으로 세 기간을 공격적으로 넓혔다. s264_aia는 similar/ablation(유사/제거) 생존 관문으로, s262_lih는 guardrail(가드레일)로, s264_lc는 한 단계 demote audit(강등 감사)로만 둔다.",
        "",
        "## Queue Decisions(대기열 판단)",
        "",
        "| queue(대기열) | decision(판단) | variants(변형) | attempts(시도) |",
        "|---|---|---:|---:|",
    ]
    for row in result["queue_decision"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['run267DL_decision']}` | `{row['variant_count']}` | `{row['attempt_count']}` |"
        )
    lines.extend(
        [
            "",
            "## Attempt Inputs(시도 입력)",
            "",
            "| attempt(시도) | candidate(후보) | profile(프로필) | tier(티어) | set_mode(설정 모드) |",
            "|---|---|---|---|---|",
        ]
    )
    for row in result["attempt_manifest"]:
        lines.append(
            f"| `{row['attempt_name']}` | `{row['candidate_alias']}` | `{row['profile_label']}` | `{row['tier']}` | `{row['set_mode']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 run(실행)은 materialization(물질화)만 완료했다.",
            "- MT5 execution(MT5 실행), balance/equity review(잔액/평가금 검토), trade quality(거래 품질), Adapter package(어댑터 패키지), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성)는 아직 없다.",
            "- headline KPI(대표 핵심 성과 지표)나 improved number(개선 숫자)만으로 후보를 선택하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- materialization_plan(물질화 계획): `{rel(MATERIALIZATION_PLAN_PATH)}`",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- adapter_handoff_gap_receipt(어댑터 인계 공백 영수증): `{rel(ADAPTER_HANDOFF_GAP_RECEIPT_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267DL_producer", "producer_script", PRODUCER_PATH, "Builds run267DL materialization package."),
        ("stage267_run267DL_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH, "Materialization plan."),
        ("stage267_run267DL_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Queue decisions."),
        ("stage267_run267DL_feature_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Feature frame manifest."),
        ("stage267_run267DL_model_manifest", "model_manifest", MODEL_MANIFEST_PATH, "Model manifest."),
        ("stage267_run267DL_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Variant manifest."),
        ("stage267_run267DL_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Attempt manifest."),
        ("stage267_run267DL_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract."),
        ("stage267_run267DL_held_queue", "held_queue", HELD_QUEUE_PATH, "Held queue."),
        ("stage267_run267DL_handoff_receipt", "handoff_receipt", HANDOFF_RECEIPT_PATH, "Handoff receipt."),
        ("stage267_run267DL_adapter_gap_receipt", "adapter_handoff_gap_receipt", ADAPTER_HANDOFF_GAP_RECEIPT_PATH, "Adapter handoff gap receipt."),
        ("stage267_run267DL_feature_mutation", "feature_mutation_receipt", FEATURE_MUTATION_RECEIPT_PATH, "Feature mutation receipt."),
        ("stage267_run267DL_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267DL_environment", "environment_reproducibility_receipt", ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, "Environment receipt."),
        ("stage267_run267DL_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267DL_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267DL_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DL_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267DL_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267DL_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267DL_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267DL_report", "review_report", REPORT_PATH, "User-facing report."),
    )
    return [
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


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    notes = (
        f"variants={counts['variants']};attempts={counts['attempts']};"
        f"s258_aggressive_variants={counts['s258_variants']};held_rows={counts['held_rows']};"
        f"next_action={NEXT_ACTION}."
    )
    stage_row = {
        "row_id": "stage267_run267DL_shared_weakness_breakout_third_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_third_followup_or_prune_materialization",
        "tier_scope": "Tier A and duplicate-boundary rows where source attempts exist; true fallback not claimed",
        "scoreboard": "feature_model_set_ini_materialization_aggressive_supply_expansion",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_mt5_execution_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_shared_weakness_third_followup_prune_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__shared_weakness_breakout_third_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "shared_weakness_breakout_third_followup_or_prune_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "shared_weakness_breakout_third_followup_or_prune_materialization",
        "tier_scope": "Tier A and duplicate-boundary materialized attempts",
        "kpi_scope": "materialization_manifest_no_mt5_kpi",
        "scoreboard_lane": "shared_weakness_third_followup_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={counts['variants']};attempts={counts['attempts']};s258_aggressive_variants={counts['s258_variants']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


def update_current_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267DL_shared_weakness_breakout_third_followup_or_prune_materialization"
        f"(267DL 공유 약점 3차 후속/가지치기 물질화): `{rel(REPORT_PATH)}`"
    )
    summary_line = (
        f"- latest_materialization(최신 물질화): run267DL(267DL 실행) variants(변형) `{counts['variants']}`, "
        f"attempts(시도) `{counts['attempts']}`, aggressive_s258_variants(공격형 s258 변형) `{counts['s258_variants']}`, "
        f"held_rows(보류 행) `{counts['held_rows']}`, report(보고서) `{rel(REPORT_PATH)}`."
    )
    block = "\n".join(
        [
            "Run267DL(267DL 실행)은 run267DK(267DK 실행)의 third follow-up/prune queue(3차 후속/가지치기 대기열)를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 물질화했다.",
            f"Effect(효과): variants(변형) `{counts['variants']}`, attempts(시도) `{counts['attempts']}`, s258 aggressive supply variants(s258 공격형 공급 변형) `{counts['s258_variants']}`, adapter handoff gap receipts(어댑터 인계 공백 영수증) `{counts['adapter_gap_receipts']}`를 만들었다.",
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
                "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_third_followup_or_prune_materialization`",
            )
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(
                text,
                "Effect(효과): run267DJ(267DJ 실행)의 balance/time-slice/trade-quality",
                report_line,
            )
            text = append_after_contains(text, "## Current Next Action", summary_line)
            text = append_block_once(text, "Run267DL(267DL 실행)은 run267DK", block)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267DK_shared_weakness_breakout_third_followup_or_prune_design", report_line)
            text = append_block_once(text, "Run267DL(267DL 실행)은 run267DK", block)
        else:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "run267DK_shared_weakness_breakout_third_followup_or_prune_design", report_line)
            text = append_block_once(text, "Run267DL(267DL 실행)은 run267DK", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267DL(267DL 실행) shared weakness breakout third follow-up/prune materialization"
        f"(공유 약점 돌파 3차 후속/가지치기 물질화) `{STATUS}`. "
        f"Effect(효과): run267DK(267DK 실행)의 queue(대기열)를 variants(변형) `{counts['variants']}`개, "
        f"attempts(시도) `{counts['attempts']}`개, aggressive s258 supply variants(공격형 s258 공급 변형) `{counts['s258_variants']}`개로 바꿨고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_design.STATUS}", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {PARENT_RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {PARENT_RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  next_action: {source_design.NEXT_ACTION}", f"  next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267DK_shared_weakness_breakout_third_followup_or_prune_design_report_path",
        f"  run267DL_shared_weakness_breakout_third_followup_or_prune_materialization_report_path: {rel(REPORT_PATH)}",
    )
    workspace = prepend_current_focus(workspace, focus)
    write_md(WORKSPACE_STATE_PATH, workspace)


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
    plans = plan_rows(queue_rows, source_variants)

    variant_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    contract_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    for plan in plans:
        source_variant = source_variants[str(plan["source_variant_id"])]
        variant, feature, model = copy_feature_and_model(plan, source_variant)
        attempts, contract, handoffs = write_attempts(
            plan,
            source_variant,
            source_attempts[str(plan["source_variant_id"])],
            variant,
        )
        variant_rows.append(variant)
        feature_rows.append(feature)
        model_rows.append(model)
        attempt_rows.extend(attempts)
        contract_rows.append(contract)
        handoff_rows.extend(handoffs)

    held_rows = held_queue_rows()
    adapter_gap_rows = adapter_handoff_gap_rows(variant_rows, handoff_rows)
    queue_decisions = queue_decision_rows(queue_rows, variant_rows)
    mutation_rows = feature_mutation_rows(variant_rows)
    experiment_rows = experiment_design_rows(queue_rows)
    env_rows = environment_rows()
    data_rows = data_integrity_rows(feature_rows)
    runtime_rows = runtime_parity_rows(variant_rows)
    counts = {
        "missing_required": len(missing),
        "queue_rows": len(queue_rows),
        "variants": len(variant_rows),
        "attempts": len(attempt_rows),
        "feature_frames": len(feature_rows),
        "models": len(model_rows),
        "runtime_contracts": len(contract_rows),
        "handoff_receipts": len(handoff_rows),
        "adapter_gap_receipts": len(adapter_gap_rows),
        "held_rows": len(held_rows),
        "s264_aia_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s264_aia"),
        "s264_aia_attempts": sum(1 for row in attempt_rows if row["candidate_alias"] == "s264_aia"),
        "s258_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s258_stc"),
        "s258_attempts": sum(1 for row in attempt_rows if row["candidate_alias"] == "s258_stc"),
        "s262_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s262_lih"),
        "s264_lc_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s264_lc"),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    judgment_rows = result_judgment_rows(counts)
    gates = gate_audit_rows(counts)
    counts["gate_rows"] = len(gates)
    counts["gate_passes"] = sum(1 for row in gates if row["status"] == "pass")

    sources = {
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
    outputs = {
        "materialization_plan": rel(MATERIALIZATION_PLAN_PATH),
        "queue_decision": rel(QUEUE_DECISION_PATH),
        "feature_frame_manifest": rel(FEATURE_FRAME_MANIFEST_PATH),
        "model_manifest": rel(MODEL_MANIFEST_PATH),
        "variant_manifest": rel(VARIANT_MANIFEST_PATH),
        "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
        "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
        "held_queue": rel(HELD_QUEUE_PATH),
        "handoff_receipt": rel(HANDOFF_RECEIPT_PATH),
        "adapter_handoff_gap_receipt": rel(ADAPTER_HANDOFF_GAP_RECEIPT_PATH),
        "feature_mutation_receipt": rel(FEATURE_MUTATION_RECEIPT_PATH),
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
        "counts": counts,
        "sources": sources,
        "outputs": outputs,
        "materialization_plan": plans,
        "queue_decision": queue_decisions,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "runtime_contract": contract_rows,
        "held_queue": held_rows,
        "handoff_receipt": handoff_rows,
        "adapter_handoff_gap_receipt": adapter_gap_rows,
        "feature_mutation_receipt": mutation_rows,
        "experiment_design_receipt": experiment_rows,
        "environment_reproducibility_receipt": env_rows,
        "data_integrity_receipt": data_rows,
        "runtime_parity_receipt": runtime_rows,
        "result_judgment": judgment_rows,
        "gate_audit": gates,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }

    write_csv(MATERIALIZATION_PLAN_PATH, plans)
    write_csv(QUEUE_DECISION_PATH, queue_decisions)
    write_csv(FEATURE_FRAME_MANIFEST_PATH, feature_rows)
    write_csv(MODEL_MANIFEST_PATH, model_rows)
    write_csv(VARIANT_MANIFEST_PATH, variant_rows)
    write_csv(ATTEMPT_MANIFEST_PATH, attempt_rows)
    write_csv(RUNTIME_CONTRACT_PATH, contract_rows)
    write_csv(HELD_QUEUE_PATH, held_rows)
    write_csv(HANDOFF_RECEIPT_PATH, handoff_rows)
    write_csv(ADAPTER_HANDOFF_GAP_RECEIPT_PATH, adapter_gap_rows)
    write_csv(FEATURE_MUTATION_RECEIPT_PATH, mutation_rows)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, experiment_rows)
    write_csv(ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, env_rows)
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, data_rows)
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, runtime_rows)
    write_csv(RESULT_JUDGMENT_PATH, judgment_rows)
    write_csv(GATE_AUDIT_PATH, gates)
    write_json(RUN_MANIFEST_PATH, run_manifest(created_at, result))
    write_json(LINEAGE_PATH, lineage(created_at, result))
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_docs(result)
    return result


def main() -> None:
    result = build_result()
    print(
        json.dumps(
            {
                "status": result["status"],
                "variants": result["counts"]["variants"],
                "attempts": result["counts"]["attempts"],
                "s258_aggressive_variants": result["counts"]["s258_variants"],
                "adapter_gap_receipts": result["counts"]["adapter_gap_receipts"],
                "held_rows": result["counts"]["held_rows"],
                "gate_passes": result["counts"]["gate_passes"],
                "gate_rows": result["counts"]["gate_rows"],
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": result["outputs"]["report"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
