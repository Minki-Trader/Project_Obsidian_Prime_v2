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
    run267DD_shared_weakness_breakout_second_followup_or_prune_materialization as source_materializer,
)
from stage_pipelines.stage267 import (
    run267DG_shared_weakness_breakout_second_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267DH"
RUN_ID = "run267DH_stage267_shared_weakness_breakout_second_followup_or_prune_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZER_RUN_ID = source_materializer.RUN_ID
STATUS = "run267DH_shared_weakness_breakout_second_followup_or_prune_materialized_execution_pending"
JUDGMENT = "shared_weakness_second_followup_or_prune_materialized_no_candidate_selection"
NEXT_ACTION = "run267DI_execute_shared_weakness_breakout_second_followup_or_prune_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_second_followup_or_prune_materialization"
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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DH_shared_weakness_breakout_second_followup_or_prune_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DH_shared_weakness_breakout_second_followup_or_prune_materialization.py")

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

COMMON_ROOT = "OPV2/s267dh/run267DH_shared_weakness_second_followup_or_prune"
EXPLORATION_LABEL = "stage267_BaselineRacing__SharedWeaknessSecondFollowupOrPruneMaterialization"
MATERIALIZATION_BOUNDARY = "materialization_only_no_candidate_selection_no_selected_research_baseline_no_onnx"
TIER_PAIR_BOUNDARY = (
    "Tier A and duplicate-boundary Tier A+B are kept only where source attempts exist; "
    "true Tier B fallback and actual routed total remain unclaimed"
)

PLAN_CONFIGS = (
    {
        "queue_id": "dg_q01_s264_aia_survivor_replacement_ablation_cross_period",
        "source_variant_id": "run267dd_04_s264_aia_similar_replacement_watch",
        "variant_id": "run267dh_01_s264_aia_similar_survivor_gate",
        "profile_label": "s264_aia_similar_survivor_gate",
        "model_materialization_type": "source_replay_from_run267DD_s264_aia_similar_replacement_survivor_gate",
        "known_difference": "reclassifies run267DF similar replacement survivor as cross-period/feature-reliance gate input; no signal mutation.",
    },
    {
        "queue_id": "dg_q01_s264_aia_survivor_replacement_ablation_cross_period",
        "source_variant_id": "run267dd_05_s264_aia_ablation_neutralized_watch",
        "variant_id": "run267dh_02_s264_aia_ablation_survivor_gate",
        "profile_label": "s264_aia_ablation_survivor_gate",
        "model_materialization_type": "source_replay_from_run267DD_s264_aia_ablation_neutralized_survivor_gate",
        "known_difference": "reclassifies run267DF ablation survivor as cross-period/feature-reliance gate input; no signal mutation.",
    },
    {
        "queue_id": "dg_q02_s262_lih_validation_heavy_control_crosscheck",
        "source_variant_id": "run267dd_08_s262_lih_weekday_dd_control",
        "variant_id": "run267dh_03_s262_lih_validation_control_crosscheck",
        "profile_label": "s262_lih_validation_control_crosscheck",
        "model_materialization_type": "source_replay_from_run267DD_s262_lih_control_guardrail",
        "known_difference": "keeps s262_lih as validation-heavy control guardrail; no candidate selection.",
    },
    {
        "queue_id": "dg_q03_s258_stc_thin_supply_impulse_stress",
        "source_variant_id": "run267dd_01_s258_stc_2023h2_session_cross_stress",
        "variant_id": "run267dh_04_s258_stc_2023h2_thin_supply_impulse",
        "profile_label": "s258_stc_thin_supply_impulse_stress",
        "model_materialization_type": "source_replay_from_run267DD_s258_2023h2_supply_stress",
        "known_difference": "reuses 2023H2 adjacent-period stress as thin-supply impulse check; no Adapter claim.",
    },
    {
        "queue_id": "dg_q03_s258_stc_thin_supply_impulse_stress",
        "source_variant_id": "run267dd_02_s258_stc_2025h1_session_cross_stress",
        "variant_id": "run267dh_05_s258_stc_2025h1_thin_supply_impulse",
        "profile_label": "s258_stc_thin_supply_impulse_stress",
        "model_materialization_type": "source_replay_from_run267DD_s258_2025h1_supply_stress",
        "known_difference": "reuses 2025H1 adjacent-period stress as thin-supply impulse check; no Adapter claim.",
    },
    {
        "queue_id": "dg_q03_s258_stc_thin_supply_impulse_stress",
        "source_variant_id": "run267dd_03_s258_stc_2025h2_session_cross_stress",
        "variant_id": "run267dh_06_s258_stc_2025h2_thin_supply_impulse",
        "profile_label": "s258_stc_thin_supply_impulse_stress",
        "model_materialization_type": "source_replay_from_run267DD_s258_2025h2_supply_stress",
        "known_difference": "reuses 2025H2 adjacent-period stress as thin-supply impulse check; no Adapter claim.",
    },
    {
        "queue_id": "dg_q04_s264_lc_weekday_dd_deescalation_control",
        "source_variant_id": "run267dd_07_s264_lc_weekday_dd_control",
        "variant_id": "run267dh_07_s264_lc_weekday_dd_deescalation",
        "profile_label": "s264_lc_weekday_dd_deescalation",
        "model_materialization_type": "source_replay_from_run267DD_s264_lc_dd_deescalation_audit",
        "known_difference": "keeps s264_lc as DD caution/de-escalation audit, not a safe control claim.",
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


def replace_line_containing(text: str, needle: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


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


def prepend_current_focus(text: str, focus_line: str) -> str:
    if f"`{STATUS}`" in text:
        return text
    return text.replace("current_focus:\n", "current_focus:\n" + focus_line, 1)


def split_semicolon(value: Any) -> list[str]:
    return [part.strip() for part in str(value or "").split(";") if part.strip()]


def source_by_id(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {str(row[key]): dict(row) for row in rows}


def attempts_by_variant(rows: Sequence[Mapping[str, str]]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        result.setdefault(str(row["variant_id"]), []).append(dict(row))
    return result


def queue_by_id(rows: Sequence[Mapping[str, str]]) -> dict[str, dict[str, str]]:
    return {str(row["queue_id"]): dict(row) for row in rows}


def target_attempt_name(source_attempt_name: str, source_variant_id: str, target_variant_id: str) -> str:
    if source_variant_id in source_attempt_name:
        return source_attempt_name.replace(source_variant_id, target_variant_id, 1)
    return f"{target_variant_id}_{source_attempt_name}"


def write_attempt_files(
    *,
    source_attempt: Mapping[str, str],
    source_variant: Mapping[str, str],
    target_variant: Mapping[str, Any],
    attempt_name: str,
    common_feature_path: str,
    common_model_path: str,
) -> tuple[dict[str, Any], dict[str, Any], str, str]:
    source_set = repo_path(str(source_attempt["set_path"]))
    source_ini = repo_path(str(source_attempt["ini_path"]))
    set_values = parse_key_values(source_set)
    tier = source_attempt.get("tier") or set_values.get("InpTierLabel") or "Tier A"
    split = source_attempt.get("split") or set_values.get("InpSplitLabel") or "run267DH_materialized_scope"
    common_telemetry_root = f"{COMMON_ROOT}/{target_variant['candidate_alias']}/{target_variant['variant_id']}/telemetry"
    telemetry = f"{common_telemetry_root}/{attempt_name}_telemetry.csv"
    summary = f"{common_telemetry_root}/{attempt_name}_summary.csv"
    set_values.update(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": tier,
            "InpSplitLabel": split,
            "InpModelPath": common_model_path,
            "InpModelId": f"{RUN_ID}_{target_variant['variant_id']}",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": common_feature_path,
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureCount": target_variant["feature_count"],
            "InpFeatureOrderHash": target_variant["feature_order_hash"],
            "InpFallbackFeatureCsvPath": common_feature_path,
            "InpFallbackFeatureCount": target_variant["feature_count"],
            "InpFallbackModelPath": common_model_path,
            "InpFallbackModelId": f"{RUN_ID}_{target_variant['variant_id']}_fallback_boundary",
            "InpFallbackFeatureOrderHash": target_variant["feature_order_hash"],
            "InpTelemetryCsvPath": telemetry,
            "InpSummaryCsvPath": summary,
            "InpTelemetryUseCommonFiles": "true",
        }
    )
    set_payload = write_key_values(
        MT5_ROOT / f"{attempt_name}.set",
        set_values,
        header="; generated_by=run267DH_shared_weakness_breakout_second_followup_or_prune_materialization",
    )

    ini_values = parse_key_values(source_ini)
    ini_values.update(
        {
            "Report": f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}",
            "ExpertParameters": source_materializer.EA_TESTER_SET_NAME
            if hasattr(source_materializer, "EA_TESTER_SET_NAME")
            else "ObsidianPrimeV2_RuntimeProbeEA.set",
        }
    )
    ini_payload = write_key_values(MT5_ROOT / f"{attempt_name}.ini", ini_values, header="[Tester]")
    return set_payload, ini_payload, telemetry, summary


def materialize_plan(
    *,
    plan: Mapping[str, str],
    source_variant: Mapping[str, str],
    source_attempts: Sequence[Mapping[str, str]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
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
    feature_order = source_variant.get("feature_order", "")
    feature_count = str(len(split_semicolon(feature_order)))
    target_variant = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "source_run_id": SOURCE_MATERIALIZER_RUN_ID,
        "source_variant_id": source_variant["variant_id"],
        "candidate_id": source_variant.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": source_variant.get("candidate_role"),
        "profile_label": plan["profile_label"],
        "source_profile_label": source_variant.get("profile_label"),
        "model_materialization_type": plan["model_materialization_type"],
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
    feature_row = {
        "variant_id": variant_id,
        "candidate_alias": alias,
        "source_feature_file": source_variant["runtime_feature_file"],
        "runtime_feature_file": rel(target_feature),
        "runtime_feature_sha256": target_variant["runtime_feature_sha256"],
        "common_feature_path": common_feature,
        "common_feature_sha256": feature_copy["sha256"],
        "feature_count": feature_count,
        "feature_order_hash": target_variant["feature_order_hash"],
        "availability": "tracked_and_common_copied",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_row = {
        "variant_id": variant_id,
        "candidate_alias": alias,
        "source_model_file": source_variant["runtime_model_file"],
        "runtime_model_file": rel(target_model),
        "runtime_model_sha256": target_variant["runtime_model_sha256"],
        "common_model_path": common_model,
        "common_model_sha256": model_copy["sha256"],
        "model_backend": "ebm_table",
        "availability": "tracked_and_common_copied",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    attempt_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    for source_attempt in source_attempts:
        attempt_name = target_attempt_name(str(source_attempt["attempt_name"]), str(source_variant["variant_id"]), variant_id)
        set_payload, ini_payload, telemetry, summary = write_attempt_files(
            source_attempt=source_attempt,
            source_variant=source_variant,
            target_variant=target_variant,
            attempt_name=attempt_name,
            common_feature_path=common_feature,
            common_model_path=common_model,
        )
        attempt_rows.append(
            {
                "attempt_name": attempt_name,
                "variant_id": variant_id,
                "queue_id": plan["queue_id"],
                "source_run_id": SOURCE_MATERIALIZER_RUN_ID,
                "source_variant_id": source_variant["variant_id"],
                "source_attempt_name": source_attempt.get("attempt_name"),
                "candidate_id": source_variant.get("candidate_id"),
                "candidate_alias": alias,
                "candidate_role": source_variant.get("candidate_role"),
                "profile_label": plan["profile_label"],
                "tier": source_attempt.get("tier"),
                "attempt_role": source_attempt.get("attempt_role"),
                "target_period": source_attempt.get("target_period"),
                "split": source_attempt.get("split"),
                "record_view_prefix": source_attempt.get("record_view_prefix"),
                "set_path": set_payload["path"],
                "set_sha256": set_payload["sha256"],
                "ini_path": ini_payload["path"],
                "ini_sha256": ini_payload["sha256"],
                "common_telemetry_path": telemetry,
                "common_summary_path": summary,
                "common_feature_path": common_feature,
                "common_model_path": common_model,
                "tier_pair_boundary": TIER_PAIR_BOUNDARY,
                "execution_status": "execution_prepared",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        handoff_rows.append(
            {
                "receipt_id": f"run267dh_handoff_{attempt_name}",
                "variant_id": variant_id,
                "attempt_name": attempt_name,
                "candidate_alias": alias,
                "feature_order_hash": target_variant["feature_order_hash"],
                "model_sha256": target_variant["runtime_model_sha256"],
                "set_sha256": set_payload["sha256"],
                "ini_sha256": ini_payload["sha256"],
                "handoff_status": "model_feature_set_ini_manifest_ready",
                "runtime_claim": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    contract = {
        "variant_id": variant_id,
        "candidate_id": source_variant.get("candidate_id"),
        "candidate_alias": alias,
        "candidate_role": source_variant.get("candidate_role"),
        "profile_label": plan["profile_label"],
        "source_profile_label": source_variant.get("profile_label"),
        "source_run_id": SOURCE_MATERIALIZER_RUN_ID,
        "shared_contract": "US100 M5; MT5 RuntimeProbeEA handoff; score table model; feature order hash tracked",
        "feature_count": feature_count,
        "feature_order_hash": target_variant["feature_order_hash"],
        "model_backend": "ebm_table",
        "model_materialization_type": plan["model_materialization_type"],
        "known_difference": plan["known_difference"],
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "runtime_claim_boundary": CLAIM_BOUNDARY,
    }
    mutation = {
        "mutation_id": f"run267dh_mutation_{variant_id}",
        "variant_id": variant_id,
        "candidate_alias": alias,
        "mutation_type": "source_replay_no_signal_mutation",
        "source_variant_id": source_variant["variant_id"],
        "feature_order_hash": target_variant["feature_order_hash"],
        "effect": "preserves source feature/model while changing research role and handoff identity for run267DH.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return target_variant, feature_row, model_row, attempt_rows, contract, mutation, handoff_rows


def materialization_plan_rows(source_variants: Mapping[str, Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for config in PLAN_CONFIGS:
        source = source_variants[config["source_variant_id"]]
        rows.append(
            {
                **config,
                "source_run_id": SOURCE_MATERIALIZER_RUN_ID,
                "candidate_alias": source.get("candidate_alias"),
                "candidate_id": source.get("candidate_id"),
                "source_profile_label": source.get("profile_label"),
                "materialization_action": "copy_source_feature_model_set_ini_with_new_handoff_identity",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def queue_decision_rows(queue_rows: Sequence[Mapping[str, str]], variants: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    queue = queue_by_id(queue_rows)
    counts: dict[str, int] = {}
    for variant in variants:
        counts[str(variant["queue_id"])] = counts.get(str(variant["queue_id"]), 0) + 1
    return [
        {
            "queue_id": queue_id,
            "priority": row.get("priority"),
            "candidate_aliases": row.get("candidate_aliases"),
            "decision": "materialized" if queue_id in counts else "held",
            "variant_count": counts.get(queue_id, 0),
            "why": {
                "dg_q05_s264_aih_prune_or_rebuild_supply_gate": "held because run267DF destructive prune failed; only new supply structure may reopen.",
                "dg_q06_runtime_adapter_handoff_gap_for_survivors": "converted into handoff receipts; no MT5 performance attempt.",
            }.get(queue_id, "source run267DD artifacts are available and connected to run267DG decision use."),
            "effect": "keeps active research lanes executable while preventing failed/prerequisite lanes from becoming noise.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for queue_id, row in queue.items()
    ]


def held_queue_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    queue = queue_by_id(queue_rows)
    return [
        {
            "queue_id": "dg_q05_s264_aih_prune_or_rebuild_supply_gate",
            "priority": queue.get("dg_q05_s264_aih_prune_or_rebuild_supply_gate", {}).get("priority", ""),
            "candidate_aliases": "s264_aih",
            "hold_status": "held_failed_destructive_path",
            "why_held": "run267DF destructive prune produced net=-59.74 PF=0.4933 trades=27; repeating it would extend a repair loop.",
            "next_action": "reopen only with a materially new supply-structure hypothesis.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "dg_q06_runtime_adapter_handoff_gap_for_survivors",
            "priority": queue.get("dg_q06_runtime_adapter_handoff_gap_for_survivors", {}).get("priority", ""),
            "candidate_aliases": "s264_aia;s262_lih;s258_stc",
            "hold_status": "converted_to_handoff_receipts_no_mt5_attempt",
            "why_held": "this queue is an identity and handoff guardrail, not a performance experiment.",
            "next_action": "block next MT5 execution if any executable attempt lacks model/feature/set/ini identity.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def experiment_design_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": f"run267dh_design_{row['queue_id']}",
            "queue_id": row.get("queue_id"),
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


def environment_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267dh_environment_reproducibility",
            "status": "pass",
            "evidence": "source run267DD feature/model/set/ini artifacts exist and are copied into run267DH plus Common Files paths.",
            "effect": "next executor can prepare MT5 attempts from tracked manifest rows.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267dh_data_integrity",
            "status": "pass",
            "evidence": "feature_order_hash and feature_count are preserved from source variants; no feature columns are modified.",
            "effect": "materialization is an identity/handoff package, not a hidden feature rewrite.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def runtime_parity_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267dh_runtime_parity_boundary",
            "status": "not_claimed",
            "evidence": "model, feature, set, and ini handoff is prepared; MT5 execution and runtime reproduction are not done in this run.",
            "effect": "keeps ONNX/runtime claims outside materialization.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def result_judgment_rows() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267DH shared weakness second follow-up/prune materialization",
            "evidence_available": "run267DG design queue; run267DD source feature/model/set/ini artifacts; run267DH manifests, receipts, and gate audit.",
            "evidence_missing": "MT5 execution, balance/equity review, time-slice review, Adapter package, runtime reproduction, ONNX parity.",
            "judgment_label": JUDGMENT,
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_condition": NEXT_ACTION,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def gate_audit_rows(
    *,
    variants: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    held: Sequence[Mapping[str, Any]],
    handoff: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    aliases = {row.get("candidate_alias") for row in variants}
    checks = [
        ("source_design_present", path_exists(SOURCE_REVIEW_RESULT_PATH), rel(SOURCE_REVIEW_RESULT_PATH), "connects run267DG design to materialization."),
        ("source_materializer_present", path_exists(SOURCE_VARIANT_MANIFEST_PATH) and path_exists(SOURCE_ATTEMPT_MANIFEST_PATH), rel(SOURCE_VARIANT_MANIFEST_PATH), "connects executable artifacts to prior source manifests."),
        ("active_variants_materialized", len(variants) == 7, f"variants={len(variants)}", "materializes survivor/control/stress/deescalation lanes."),
        ("attempts_prepared", len(attempts) == 11, f"attempts={len(attempts)}", "prepares next MT5 batch without s264_aih failed lane."),
        ("held_rows_present", len(held) == 2, f"held_rows={len(held)}", "keeps failed prune and handoff-only queues explicit."),
        ("s264_aih_not_executable", "s264_aih" not in aliases, "s264_aih absent from executable variants", "prevents a failed destructive path from being repeated."),
        ("handoff_receipts_complete", len(handoff) == len(attempts), f"handoff_receipts={len(handoff)}", "every attempt has set/ini/model/feature identity."),
        ("no_selection_or_onnx_claim", True, "selected_candidate=none;onnx=not_claimed", "keeps claim boundary correct."),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "pass" if ok else "fail",
            "evidence": evidence,
            "effect": effect,
        }
        for gate_id, ok, evidence, effect in checks
    ]


def run_manifest(created_at: str, result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "parent_run_id": PARENT_RUN_ID,
        "source_materializer_run_id": SOURCE_MATERIALIZER_RUN_ID,
        "purpose": "Materialize run267DG survivor/control/stress/prune queue into executable MT5 handoff package.",
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "counts": result["counts"],
        "sources": result["sources"],
        "outputs": result["outputs"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def lineage(created_at: str) -> dict[str, Any]:
    return {
        "lineage_id": "stage267_run267DH_lineage",
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "parent_run": PARENT_RUN_ID,
        "source_materializer_run": SOURCE_MATERIALIZER_RUN_ID,
        "source_inputs": [
            rel(SOURCE_QUEUE_PATH),
            rel(SOURCE_FEATURE_BLUEPRINT_PATH),
            rel(SOURCE_BRANCH_DECISION_PATH),
            rel(SOURCE_PRUNE_MATRIX_PATH),
            rel(SOURCE_FAILURE_MEMORY_PATH),
            rel(SOURCE_REVIEW_RESULT_PATH),
            rel(SOURCE_VARIANT_MANIFEST_PATH),
            rel(SOURCE_ATTEMPT_MANIFEST_PATH),
            rel(SOURCE_RUNTIME_CONTRACT_PATH),
            rel(SOURCE_HANDOFF_RECEIPT_PATH),
        ],
        "artifact_paths": [
            rel(MATERIALIZATION_PLAN_PATH),
            rel(VARIANT_MANIFEST_PATH),
            rel(ATTEMPT_MANIFEST_PATH),
            rel(RUNTIME_CONTRACT_PATH),
            rel(HANDOFF_RECEIPT_PATH),
            rel(REVIEW_RESULT_PATH),
            rel(REPORT_PATH),
        ],
        "availability": "tracked",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267DH Shared Weakness Second Follow-up/Prune Materialization(267단계 267DH 공유 약점 2차 후속/가지치기 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- source_design(원천 설계): `{PARENT_RUN_ID}`",
        f"- source_materializer(원천 물질화): `{SOURCE_MATERIALIZER_RUN_ID}`",
        f"- variants(변형): `{counts['variants']}`",
        f"- attempts(시도): `{counts['attempts']}`",
        f"- held_rows(보류 행): `{counts['held_rows']}`",
        f"- handoff_receipts(인계 영수증): `{counts['handoff_receipts']}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "`run267DH`는 새 승자를 고른 것이 아니다. `run267DG`가 정한 생존/대조/압박/강등 큐를 실제 MT5(MetaTrader 5, 메타트레이더5) 실행 입력으로 묶었다. `s264_aia`, `s262_lih`, `s258_stc`, `s264_lc`는 실행 입력으로 만들고, `s264_aih`는 현재 파괴형 경로가 실패했기 때문에 보류했다.",
        "",
        "## Queue Decisions(대기열 판단)",
        "",
        "| queue(대기열) | decision(판단) | variants(변형) | why(이유) |",
        "|---|---|---:|---|",
    ]
    for row in result["queue_decision"]:
        lines.append(f"| `{row['queue_id']}` | `{row['decision']}` | `{row['variant_count']}` | {row['why']} |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "이 실행은 materialization(물질화)이다. MT5 실행, balance/equity curve(잔액/평가금 곡선) 검토, Adapter(어댑터) 확정, runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성)는 아직 아니다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- materialization_plan(물질화 계획): `{rel(MATERIALIZATION_PLAN_PATH)}`",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- held_queue(보류 대기열): `{rel(HELD_QUEUE_PATH)}`",
            f"- handoff_receipt(인계 영수증): `{rel(HANDOFF_RECEIPT_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267DH_producer", "producer_script", PRODUCER_PATH, "Builds run267DH materialization package."),
        ("stage267_run267DH_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH, "Materialization plan."),
        ("stage267_run267DH_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Queue decisions."),
        ("stage267_run267DH_feature_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Feature manifest."),
        ("stage267_run267DH_model_manifest", "model_manifest", MODEL_MANIFEST_PATH, "Model manifest."),
        ("stage267_run267DH_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Variant manifest."),
        ("stage267_run267DH_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Attempt manifest."),
        ("stage267_run267DH_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract."),
        ("stage267_run267DH_held_queue", "held_queue", HELD_QUEUE_PATH, "Held queue."),
        ("stage267_run267DH_handoff_receipt", "handoff_receipt", HANDOFF_RECEIPT_PATH, "Handoff receipt."),
        ("stage267_run267DH_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DH_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267DH_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267DH_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267DH_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267DH_report", "review_report", REPORT_PATH, "User-facing report."),
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
        f"held_rows={counts['held_rows']};next_action={NEXT_ACTION}."
    )
    stage_row = {
        "row_id": "stage267_run267DH_shared_weakness_breakout_second_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_second_followup_or_prune_materialization",
        "tier_scope": "Tier A and duplicate-boundary rows where source attempts exist; true fallback not claimed",
        "scoreboard": "feature_model_set_ini_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_mt5_execution_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_shared_weakness_second_followup_prune_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__shared_weakness_breakout_second_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "shared_weakness_breakout_second_followup_or_prune_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "shared_weakness_breakout_second_followup_or_prune_materialization",
        "tier_scope": "Tier A and duplicate-boundary materialized attempts",
        "kpi_scope": "materialization_manifest_no_mt5_kpi",
        "scoreboard_lane": "shared_weakness_followup_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={counts['variants']};attempts={counts['attempts']};held_rows={counts['held_rows']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "not_applicable",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


def update_current_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267DH_shared_weakness_breakout_second_followup_or_prune_materialization"
        f"(267DH 공유 약점 2차 후속/가지치기 물질화): `{rel(REPORT_PATH)}`"
    )
    summary_line = (
        f"- latest_materialization(최신 물질화): run267DH(267DH 실행) variants(변형) `{counts['variants']}`, "
        f"attempts(시도) `{counts['attempts']}`, held_rows(보류 행) `{counts['held_rows']}`, "
        f"handoff_receipts(인계 영수증) `{counts['handoff_receipts']}`, report(보고서) `{rel(REPORT_PATH)}`."
    )
    block = "\n".join(
        [
            "Run267DH(267DH 실행)는 run267DG(267DG 실행)의 materialization queue(물질화 대기열)를 실제 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.",
            f"Effect(효과): variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개, handoff receipts(인계 영수증) `{counts['handoff_receipts']}`개를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_second_followup_or_prune_materialization`")
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267DG_shared_weakness_breakout_second_followup_or_prune_design.md", report_line)
            text = append_after_contains(text, "## Current Next Action", summary_line)
            text = append_block_once(text, "Run267DH(267DH 실행)는 run267DG", block)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_containing(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267DG_shared_weakness_breakout_second_followup_or_prune_design", report_line)
            text = append_block_once(text, "Run267DH(267DH 실행)는 run267DG", block)
        else:
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "run267DG_shared_weakness_breakout_second_followup_or_prune_design", report_line)
            text = append_block_once(text, "Run267DH(267DH 실행)는 run267DG", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267DH(267DH 실행) shared weakness breakout second follow-up/prune materialization"
        f"(공유 약점 돌파 2차 후속/가지치기 물질화) `{STATUS}`. "
        f"Effect(효과): run267DG(267DG 실행)의 queue(대기열)를 variants(변형) `{counts['variants']}`개, "
        f"attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개로 나눴고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), "
        "Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_design.STATUS}", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  next_action: {source_design.NEXT_ACTION}", f"  next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267DG_shared_weakness_breakout_second_followup_or_prune_design_report_path",
        f"  run267DH_shared_weakness_breakout_second_followup_or_prune_materialization_report_path: {rel(REPORT_PATH)}",
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
    plan_rows = materialization_plan_rows(source_variants)

    variant_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    contract_rows: list[dict[str, Any]] = []
    mutation_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    for plan in plan_rows:
        source_variant = source_variants[str(plan["source_variant_id"])]
        variant, feature, model, attempts, contract, mutation, handoff = materialize_plan(
            plan=plan,
            source_variant=source_variant,
            source_attempts=source_attempts[str(plan["source_variant_id"])],
        )
        variant_rows.append(variant)
        feature_rows.append(feature)
        model_rows.append(model)
        attempt_rows.extend(attempts)
        contract_rows.append(contract)
        mutation_rows.append(mutation)
        handoff_rows.extend(handoff)

    held_rows = held_queue_rows(queue_rows)
    queue_decisions = queue_decision_rows(queue_rows, variant_rows)
    experiment_rows = experiment_design_rows(queue_rows)
    env_rows = environment_rows()
    data_rows = data_integrity_rows()
    runtime_rows = runtime_parity_rows()
    judgment_rows = result_judgment_rows()
    gates = gate_audit_rows(variants=variant_rows, attempts=attempt_rows, held=held_rows, handoff=handoff_rows)
    counts = {
        "missing_required": len(missing),
        "queue_rows": len(queue_rows),
        "variants": len(variant_rows),
        "attempts": len(attempt_rows),
        "held_rows": len(held_rows),
        "handoff_receipts": len(handoff_rows),
        "gate_passes": sum(1 for row in gates if row["status"] == "pass"),
        "gate_rows": len(gates),
    }
    sources = {
        "source_queue": rel(SOURCE_QUEUE_PATH),
        "source_feature_blueprint": rel(SOURCE_FEATURE_BLUEPRINT_PATH),
        "source_branch_decision": rel(SOURCE_BRANCH_DECISION_PATH),
        "source_prune_matrix": rel(SOURCE_PRUNE_MATRIX_PATH),
        "source_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
        "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
        "source_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
        "source_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
        "source_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
        "source_handoff_receipt": rel(SOURCE_HANDOFF_RECEIPT_PATH),
        "source_design_report": rel(SOURCE_DESIGN_REPORT_PATH),
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
        "materialization_plan": plan_rows,
        "queue_decision": queue_decisions,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "runtime_contract": contract_rows,
        "held_queue": held_rows,
        "handoff_receipt": handoff_rows,
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

    write_csv(MATERIALIZATION_PLAN_PATH, plan_rows)
    write_csv(QUEUE_DECISION_PATH, queue_decisions)
    write_csv(FEATURE_FRAME_MANIFEST_PATH, feature_rows)
    write_csv(MODEL_MANIFEST_PATH, model_rows)
    write_csv(VARIANT_MANIFEST_PATH, variant_rows)
    write_csv(ATTEMPT_MANIFEST_PATH, attempt_rows)
    write_csv(RUNTIME_CONTRACT_PATH, contract_rows)
    write_csv(HELD_QUEUE_PATH, held_rows)
    write_csv(HANDOFF_RECEIPT_PATH, handoff_rows)
    write_csv(FEATURE_MUTATION_RECEIPT_PATH, mutation_rows)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, experiment_rows)
    write_csv(ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, env_rows)
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, data_rows)
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, runtime_rows)
    write_csv(RESULT_JUDGMENT_PATH, judgment_rows)
    write_csv(GATE_AUDIT_PATH, gates)
    write_json(RUN_MANIFEST_PATH, run_manifest(created_at, result))
    write_json(LINEAGE_PATH, lineage(created_at))
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
                "held_rows": result["counts"]["held_rows"],
                "handoff_receipts": result["counts"]["handoff_receipts"],
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
