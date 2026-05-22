from __future__ import annotations

import csv
import json
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
    run267DU_runtime_gap_aware_fifth_followup_or_prune_materialization as source_materialization,
)
from stage_pipelines.stage267 import (
    run267DX_runtime_gap_aware_sixth_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267DY"
RUN_ID = "run267DY_stage267_runtime_gap_aware_sixth_followup_or_prune_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_DU_RUN_ID = source_materialization.RUN_ID
STATUS = "run267DY_runtime_gap_aware_sixth_followup_or_prune_materialized_execution_pending"
JUDGMENT = "runtime_gap_aware_sixth_followup_or_prune_materialized_no_candidate_selection"
NEXT_ACTION = "run267DZ_execute_runtime_gap_aware_sixth_followup_or_prune_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_sixth_followup_or_prune_materialization"
FEATURE_ROOT = RUN_ROOT / "features"
VARIANT_ROOT = RUN_ROOT / "variants"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_QUEUE_PATH = source_design.MATERIALIZATION_QUEUE_PATH
SOURCE_BRANCH_DECISION_PATH = source_design.BRANCH_DECISION_PATH
SOURCE_PRUNE_MATRIX_PATH = source_design.PRUNE_MATRIX_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_REVIEW_RESULT_PATH = source_design.REVIEW_RESULT_PATH
SOURCE_DESIGN_REPORT_PATH = source_design.REPORT_PATH
SOURCE_DU_VARIANT_MANIFEST_PATH = source_materialization.VARIANT_MANIFEST_PATH
SOURCE_DU_ATTEMPT_MANIFEST_PATH = source_materialization.ATTEMPT_MANIFEST_PATH
SOURCE_DU_RUNTIME_CONTRACT_PATH = source_materialization.RUNTIME_CONTRACT_PATH
SOURCE_DU_REPORT_PATH = source_materialization.REPORT_PATH
SOURCE_FEATURE_MANIFEST_PATH = STAGE_ROOT / "02_runs" / "run267B" / "source_feature_manifest.csv"

MATERIALIZATION_PLAN_PATH = RUN_ROOT / "materialization_plan.csv"
QUEUE_DECISION_PATH = RUN_ROOT / "queue_decision.csv"
FEATURE_FRAME_MANIFEST_PATH = RUN_ROOT / "feature_frame_manifest.csv"
MODEL_MANIFEST_PATH = RUN_ROOT / "model_manifest.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
HELD_QUEUE_PATH = RUN_ROOT / "held_queue.csv"
PREFLIGHT_RECEIPT_PATH = RUN_ROOT / "preflight_handoff_receipt.csv"
ANTI_FILTER_STACK_RECEIPT_PATH = RUN_ROOT / "anti_filter_stack_receipt.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH = RUN_ROOT / "environment_reproducibility_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DY_runtime_gap_aware_sixth_followup_or_prune_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DY_runtime_gap_aware_sixth_followup_or_prune_materialization.py")

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

COMMON_ROOT = "OPV2/s267dy/run267DY_runtime_gap_aware_sixth_followup_or_prune"
EXPLORATION_LABEL = "stage267_BaselineRacing__RuntimeGapAwareSixthFollowupOrPrune"
MATERIALIZATION_BOUNDARY = "materialization_only_execution_pending_no_candidate_selection_no_selected_research_baseline_no_onnx"
TIER_PAIR_BOUNDARY = (
    "Tier A rows are materialized for the sixth follow-up; true Tier B fallback and actual routed total remain unclaimed."
)

PLAN_CONFIGS: tuple[dict[str, Any], ...] = (
    {
        "queue_id": "q01_s258_stc_structural_dd_shape_split",
        "source_kind": "du",
        "source_variant_id": "run267du_01_s258_stc_2023h2_handoff_repair",
        "variant_id": "run267dy_01_s258_stc_2023h2_dd_shape_split",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_structural_dd_shape_2023h2",
        "profile_token": "s258_structural_dd_shape",
        "materialization_type": "risk_shape_compression_from_handoff_repair",
        "split": "adjacent_2023_h2_train_pre_2024",
        "period_label": "2023H2",
        "from_date": "2023.07.05",
        "to_date": "2024.01.01",
        "attempt_role": "structural_dd_shape_split",
        "priority": "P0_structural",
        "targeted_weakness": "hour16 loss concentration(16시 손실 집중)",
        "set_updates": {
            "InpShortThreshold": "0.52",
            "InpLongThreshold": "0.50",
            "InpAtrStopMultiplier": "1.85",
            "InpAtrTakeProfitMultiplier": "4.40",
            "InpModelRiskMaxPct": "0.026",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpSameDirectionReentryCooldownBars": "3",
        },
        "known_difference": "Compresses risk shape without excluding hour16 or other calendar buckets.",
    },
    {
        "queue_id": "q01_s258_stc_structural_dd_shape_split",
        "source_kind": "du",
        "source_variant_id": "run267du_02_s258_stc_2025h1_handoff_repair",
        "variant_id": "run267dy_02_s258_stc_2025h1_dd_shape_split",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_structural_dd_shape_2025h1",
        "profile_token": "s258_structural_dd_shape",
        "materialization_type": "risk_shape_compression_from_handoff_repair",
        "split": "adjacent_2025_h1_validation_post_2024",
        "period_label": "2025H1",
        "from_date": "2025.01.02",
        "to_date": "2025.07.01",
        "attempt_role": "structural_dd_shape_split",
        "priority": "P0_structural",
        "targeted_weakness": "2025-05 and late-session drawdown(2025-05 및 후반 세션 손실폭)",
        "set_updates": {
            "InpShortThreshold": "0.52",
            "InpLongThreshold": "0.50",
            "InpAtrStopMultiplier": "1.85",
            "InpAtrTakeProfitMultiplier": "4.40",
            "InpModelRiskMaxPct": "0.026",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpSameDirectionReentryCooldownBars": "3",
        },
        "known_difference": "Separates 2025H1 DD shape from simple month or hour filtering.",
    },
    {
        "queue_id": "q01_s258_stc_structural_dd_shape_split",
        "source_kind": "du",
        "source_variant_id": "run267du_03_s258_stc_2025h2_handoff_repair",
        "variant_id": "run267dy_03_s258_stc_2025h2_dd_shape_split",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_structural_dd_shape_2025h2",
        "profile_token": "s258_structural_dd_shape",
        "materialization_type": "risk_shape_compression_from_handoff_repair",
        "split": "adjacent_2025_h2_oos_followthrough",
        "period_label": "2025H2",
        "from_date": "2025.07.01",
        "to_date": "2026.01.01",
        "attempt_role": "structural_dd_shape_split",
        "priority": "P0_structural",
        "targeted_weakness": "Monday and 2025-12 loss concentration(월요일 및 2025-12 손실 집중)",
        "set_updates": {
            "InpShortThreshold": "0.52",
            "InpLongThreshold": "0.50",
            "InpAtrStopMultiplier": "1.85",
            "InpAtrTakeProfitMultiplier": "4.40",
            "InpModelRiskMaxPct": "0.026",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpSameDirectionReentryCooldownBars": "3",
        },
        "known_difference": "Pressures 2025H2 DD without a Monday or December ban.",
    },
    {
        "queue_id": "q02_s258_stc_adverse_slice_falsification",
        "source_kind": "du",
        "source_variant_id": "run267du_04_s258_stc_2023h2_noncalendar_impulse",
        "variant_id": "run267dy_04_s258_stc_2023h2_state_falsification",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_adverse_slice_state_2023h2",
        "profile_token": "s258_adverse_state_falsification",
        "materialization_type": "noncalendar_state_falsification",
        "split": "adjacent_2023_h2_train_pre_2024",
        "period_label": "2023H2",
        "from_date": "2023.07.05",
        "to_date": "2024.01.01",
        "attempt_role": "adverse_slice_state_falsification",
        "priority": "P0_falsification",
        "targeted_weakness": "hour16 but no hour filter(16시 약점, 시간 필터 없음)",
        "set_updates": {
            "InpShortThreshold": "0.51",
            "InpLongThreshold": "0.49",
            "InpAtrStopMultiplier": "2.05",
            "InpAtrTakeProfitMultiplier": "4.85",
            "InpModelRiskMaxPct": "0.029",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.015",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Tests whether impulse transition state, not the hour bucket itself, explains the loss.",
    },
    {
        "queue_id": "q02_s258_stc_adverse_slice_falsification",
        "source_kind": "du",
        "source_variant_id": "run267du_05_s258_stc_2025h1_noncalendar_impulse",
        "variant_id": "run267dy_05_s258_stc_2025h1_state_falsification",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_adverse_slice_state_2025h1",
        "profile_token": "s258_adverse_state_falsification",
        "materialization_type": "noncalendar_state_falsification",
        "split": "adjacent_2025_h1_validation_post_2024",
        "period_label": "2025H1",
        "from_date": "2025.01.02",
        "to_date": "2025.07.01",
        "attempt_role": "adverse_slice_state_falsification",
        "priority": "P0_falsification",
        "targeted_weakness": "2025-05 and close_hour22 without bucket exclusion(2025-05 및 22시 약점, 구간 제외 없음)",
        "set_updates": {
            "InpShortThreshold": "0.51",
            "InpLongThreshold": "0.49",
            "InpAtrStopMultiplier": "2.05",
            "InpAtrTakeProfitMultiplier": "4.85",
            "InpModelRiskMaxPct": "0.029",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.015",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Tests noncalendar transition quality against the 2025H1 weak slices.",
    },
    {
        "queue_id": "q02_s258_stc_adverse_slice_falsification",
        "source_kind": "du",
        "source_variant_id": "run267du_06_s258_stc_2025h2_noncalendar_impulse",
        "variant_id": "run267dy_06_s258_stc_2025h2_state_falsification",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_adverse_slice_state_2025h2",
        "profile_token": "s258_adverse_state_falsification",
        "materialization_type": "noncalendar_state_falsification",
        "split": "adjacent_2025_h2_oos_followthrough",
        "period_label": "2025H2",
        "from_date": "2025.07.01",
        "to_date": "2026.01.01",
        "attempt_role": "adverse_slice_state_falsification",
        "priority": "P0_falsification",
        "targeted_weakness": "Monday and 2025-12 without bucket exclusion(월요일 및 2025-12 약점, 구간 제외 없음)",
        "set_updates": {
            "InpShortThreshold": "0.51",
            "InpLongThreshold": "0.49",
            "InpAtrStopMultiplier": "2.05",
            "InpAtrTakeProfitMultiplier": "4.85",
            "InpModelRiskMaxPct": "0.029",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.015",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Falsifies Monday and December weakness through state shape, not exclusion.",
    },
    {
        "queue_id": "q03_s264_aih_validation_anchor_one_repair",
        "source_kind": "canonical",
        "source_candidate_id": "s264_allow_inner_high_quarter",
        "source_split": "validation_is",
        "variant_id": "run267dy_07_s264_aih_validation_anchor_repair",
        "candidate_id": "s264_allow_inner_high_quarter",
        "candidate_alias": "s264_aih",
        "candidate_role": "challenger_core",
        "profile_label": "s264_aih_validation_anchor_repair",
        "profile_token": "s264_aih_validation_repair",
        "materialization_type": "canonical_validation_anchor_handoff_repair",
        "split": "validation_is",
        "period_label": "validation_is",
        "from_date": "2025.01.02",
        "to_date": "2025.10.01",
        "attempt_role": "validation_anchor_one_repair",
        "priority": "P0_repair",
        "targeted_weakness": "validation anchor init failure(검증 앵커 초기화 실패)",
        "set_updates": {
            "InpShortThreshold": "0.53",
            "InpLongThreshold": "0.51",
            "InpAtrStopMultiplier": "2.05",
            "InpAtrTakeProfitMultiplier": "4.70",
            "InpModelRiskMaxPct": "0.027",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Repairs the Common Files handoff once and keeps the validation anchor paired to q04.",
    },
    {
        "queue_id": "q04_s264_aih_counter_shock_final_month_probe",
        "source_kind": "canonical",
        "source_candidate_id": "s264_allow_inner_high_quarter",
        "source_split": "oos",
        "variant_id": "run267dy_08_s264_aih_202604_counter_shock_probe",
        "candidate_id": "s264_allow_inner_high_quarter",
        "candidate_alias": "s264_aih",
        "candidate_role": "challenger_core",
        "profile_label": "s264_aih_202604_counter_shock_probe",
        "profile_token": "s264_aih_counter_shock",
        "materialization_type": "counter_shock_oos_final_month_probe",
        "split": "oos_final_month_2026_04",
        "period_label": "2026.04",
        "from_date": "2026.04.01",
        "to_date": "2026.04.14",
        "attempt_role": "counter_shock_final_month_falsification",
        "priority": "P0_explosive",
        "targeted_weakness": "2026.04 final-month negative(2026.04 마지막 달 음수)",
        "set_updates": {
            "InpShortThreshold": "0.56",
            "InpLongThreshold": "0.54",
            "InpAtrStopMultiplier": "1.95",
            "InpAtrTakeProfitMultiplier": "4.35",
            "InpModelRiskMaxPct": "0.026",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.02",
            "InpSameDirectionReentryCooldownBars": "2",
        },
        "known_difference": "Counter-shock falsification for 2026.04; it is not a selection run.",
    },
    {
        "queue_id": "q05_s264_lc_same_month_control_hold",
        "source_kind": "canonical",
        "source_candidate_id": "s264_lowrank_control",
        "source_split": "oos",
        "variant_id": "run267dy_09_s264_lc_202604_same_month_control",
        "candidate_id": "s264_lowrank_control",
        "candidate_alias": "s264_lc",
        "candidate_role": "defensive_control",
        "profile_label": "s264_lc_202604_same_month_control",
        "profile_token": "s264_lc_control",
        "materialization_type": "paired_same_month_control_for_q03_q04",
        "split": "oos_final_month_2026_04",
        "period_label": "2026.04",
        "from_date": "2026.04.01",
        "to_date": "2026.04.14",
        "attempt_role": "paired_same_month_control",
        "priority": "P1_control",
        "targeted_weakness": "same-month market control(같은 달 시장 대조)",
        "set_updates": {
            "InpShortThreshold": "0.54",
            "InpLongThreshold": "0.52",
            "InpAtrStopMultiplier": "2.0325",
            "InpAtrTakeProfitMultiplier": "4.615",
            "InpModelRiskMaxPct": "0.0305",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "true",
            "InpSameDirectionReentryCooldownBars": "8",
        },
        "known_difference": "Materialized only because q03/q04 need a paired same-month control.",
    },
)

HELD_QUEUE_CONFIGS: tuple[dict[str, str], ...] = (
    {
        "queue_id": "q06_prune_micro_filter_stack",
        "priority": "P0_guardrail",
        "candidate_aliases": "s258_stc;s264_aih;s264_lc",
        "decision": "guardrail_only_no_standalone_mt5(가드레일 전용, 단독 MT5 없음)",
        "why": "hour-only(시간만), weekday-only(요일만), month-only(월만) 제외는 후보 구조 개선 증거가 아니다.",
        "reopen_condition": "structural feature/route change(구조 피처/경로 변화)와 함께 여러 기간에서 살아남을 때만 재개한다.",
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
    ordered: list[str] = list(columns or [])
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(str(key))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: cell(row.get(key, "")) for key in ordered})


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8-sig")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def copy_file(source: Path, destination: Path) -> dict[str, str]:
    return source_materialization.copy_file(source, destination)


def feature_stats(path: Path) -> dict[str, Any]:
    return source_materialization.feature_stats(path)


def parse_key_values(path: Path) -> dict[str, str]:
    return source_materialization.parse_key_values(path)


def write_key_values(path: Path, values: Mapping[str, Any], header: str | None = None) -> dict[str, str]:
    return source_materialization.write_key_values(path, values, header=header)


def rows_by_id(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row[key]): row for row in rows if row.get(key)}


def attempts_by_variant(rows: Sequence[Mapping[str, str]]) -> dict[str, list[Mapping[str, str]]]:
    out: dict[str, list[Mapping[str, str]]] = {}
    for row in rows:
        out.setdefault(str(row.get("variant_id", "")), []).append(row)
    return out


def canonical_source_rows() -> dict[tuple[str, str], Mapping[str, str]]:
    return {(row["candidate_id"], row["split"]): row for row in read_csv(SOURCE_FEATURE_MANIFEST_PATH)}


def source_variant_rows() -> dict[str, Mapping[str, str]]:
    return rows_by_id(read_csv(SOURCE_DU_VARIANT_MANIFEST_PATH), "variant_id")


def source_attempt_rows() -> dict[str, list[Mapping[str, str]]]:
    return attempts_by_variant(read_csv(SOURCE_DU_ATTEMPT_MANIFEST_PATH))


def source_inputs_for_plan(
    plan: Mapping[str, Any],
    variant_by_id: Mapping[str, Mapping[str, str]],
    canonical_by_key: Mapping[tuple[str, str], Mapping[str, str]],
) -> dict[str, Any]:
    if plan["source_kind"] == "du":
        source = variant_by_id[str(plan["source_variant_id"])]
        return {
            "source_run_id": source.get("source_run_id") or SOURCE_DU_RUN_ID,
            "source_variant_id": source["variant_id"],
            "source_feature_path": source["runtime_feature_file"],
            "source_model_path": source["runtime_model_file"],
            "source_feature_sha256": source.get("runtime_feature_sha256", ""),
            "source_model_sha256": source.get("runtime_model_sha256", ""),
        }
    source = canonical_by_key[(str(plan["source_candidate_id"]), str(plan["source_split"]))]
    feature = repo_path(source["feature_file"])
    model = repo_path(source["model_file"])
    return {
        "source_run_id": "stage267_run267B_source_feature_manifest",
        "source_variant_id": f"{source['candidate_id']}_{source['split']}",
        "source_feature_path": source["feature_file"],
        "source_model_path": source["model_file"],
        "source_feature_sha256": sha256_file_lf_normalized(feature),
        "source_model_sha256": sha256_file_lf_normalized(model),
    }


def source_attempt_for_plan(
    plan: Mapping[str, Any],
    source_attempts: Mapping[str, Sequence[Mapping[str, str]]],
) -> Mapping[str, str] | None:
    if plan["source_kind"] != "du":
        return None
    attempts = source_attempts.get(str(plan["source_variant_id"]), [])
    if not attempts:
        return None
    period = str(plan["period_label"]).lower().replace(".", "")
    for attempt in attempts:
        if period in str(attempt.get("attempt_name", "")).lower():
            return attempt
    return attempts[0]


def base_set_values(plan: Mapping[str, Any], source_attempt: Mapping[str, str] | None) -> dict[str, str]:
    if source_attempt and source_attempt.get("set_path"):
        values = parse_key_values(repo_path(str(source_attempt["set_path"])))
    else:
        values = {
            "InpMainSymbol": "US100",
            "InpTimeframe": "5",
            "InpModelBackend": "ebm_table",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpFeatureStrictHeader": "true",
            "InpCsvTimestampIsBarClose": "true",
            "InpFallbackEnabled": "false",
            "InpTelemetryUseCommonFiles": "true",
            "InpShortThreshold": "0.54",
            "InpLongThreshold": "0.52",
            "InpMinMargin": "0",
            "InpInvertSignal": "false",
            "InpAllowTrading": "true",
            "InpFixedLot": "0.25",
            "InpCloseOnFlatSignal": "false",
            "InpReverseOnOppositeSignal": "true",
            "InpCloseOnlyOnOppositeSignal": "false",
            "InpMaxHoldBars": "3",
            "InpMaxConcurrentPositions": "1",
            "InpAtrSltpEnabled": "true",
            "InpAtrPeriod": "14",
            "InpAtrStopMultiplier": "2.0325",
            "InpAtrTakeProfitMultiplier": "4.615",
            "InpModelRiskSizingEnabled": "true",
            "InpModelRiskMinPct": "0.005",
            "InpModelRiskMaxPct": "0.0305",
            "InpModelRiskConfidenceFloor": "0.5",
            "InpModelRiskConfidenceCeiling": "0.6",
            "InpModelRiskFallbackLot": "0.25",
            "InpFallbackUseOnPrimaryFlat": "false",
            "InpFallbackUseOnPrimaryLowConfidence": "false",
            "InpReentryCooldownBars": "0",
            "InpSameDirectionReentryCooldownBars": "8",
            "InpEntryTransitionOnly": "false",
            "InpEntryTransitionRearmMinConfidenceDelta": "0",
            "InpSideFilterEnabled": "true",
            "InpSideFilterFeatureIndex": "2",
            "InpFallbackSideFilterFeatureIndex": "2",
            "InpBlockShortFeatureRange": "false",
            "InpBlockLongFeatureRange": "false",
        }
    values.update({key: str(value) for key, value in plan.get("set_updates", {}).items()})
    return values


def materialize_plan(
    plan: Mapping[str, Any],
    variant_by_id: Mapping[str, Mapping[str, str]],
    source_attempts: Mapping[str, Sequence[Mapping[str, str]]],
    canonical_by_key: Mapping[tuple[str, str], Mapping[str, str]],
    magic_index: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    source_info = source_inputs_for_plan(plan, variant_by_id, canonical_by_key)
    variant_id = str(plan["variant_id"])
    candidate_alias = str(plan["candidate_alias"])
    source_feature = repo_path(str(source_info["source_feature_path"]))
    source_model = repo_path(str(source_info["source_model_path"]))
    feature_path = FEATURE_ROOT / candidate_alias / variant_id / f"{variant_id}_features.csv"
    model_path = VARIANT_ROOT / candidate_alias / variant_id / "models" / f"{variant_id}_model.csv"
    feature_copy = copy_file(source_feature, feature_path)
    model_copy = copy_file(source_model, model_path)
    stats = feature_stats(feature_path)
    common_base = f"{COMMON_ROOT}/{candidate_alias}/{variant_id}"
    common_feature_path = f"{common_base}/features/{feature_path.name}"
    common_model_path = f"{common_base}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)
    source_attempt = source_attempt_for_plan(plan, source_attempts)
    attempt_name = f"{variant_id}_{str(plan['period_label']).lower().replace('.', '')}"
    telemetry = f"{common_base}/telemetry/{attempt_name}_telemetry.csv"
    summary = f"{common_base}/telemetry/{attempt_name}_summary.csv"
    set_values = base_set_values(plan, source_attempt)
    set_values.update(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": plan["split"],
            "InpMainSymbol": "US100",
            "InpTimeframe": "5",
            "InpModelPath": common_model_path,
            "InpModelId": f"{RUN_ID}_{variant_id}",
            "InpModelBackend": "ebm_table",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": common_feature_path,
            "InpFeatureCount": str(stats["feature_count"]),
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpFeatureStrictHeader": "true",
            "InpCsvTimestampIsBarClose": "true",
            "InpFeatureOrderHash": stats["feature_order_hash"],
            "InpFallbackEnabled": "false",
            "InpFallbackFeatureCsvPath": common_feature_path,
            "InpFallbackFeatureCount": str(stats["feature_count"]),
            "InpFallbackModelPath": common_model_path,
            "InpFallbackModelId": f"{RUN_ID}_{variant_id}_fallback_boundary_disabled",
            "InpFallbackModelBackend": "ebm_table",
            "InpFallbackFeatureOrderHash": stats["feature_order_hash"],
            "InpTelemetryCsvPath": telemetry,
            "InpSummaryCsvPath": summary,
            "InpTelemetryUseCommonFiles": "true",
            "InpMagic": str(26742000 + magic_index),
        }
    )
    set_payload = write_key_values(
        MT5_ROOT / f"{attempt_name}.set",
        set_values,
        header="; generated_by=run267DY_runtime_gap_aware_sixth_followup_or_prune_materialization",
    )
    ini_payload = write_key_values(
        MT5_ROOT / f"{attempt_name}.ini",
        {
            "Expert": r"Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.ex5",
            "Symbol": "US100",
            "Period": "M5",
            "Model": "4",
            "Deposit": "500",
            "Leverage": "1:100",
            "Optimization": "0",
            "ExecutionMode": "0",
            "ForwardMode": "0",
            "UseLocal": "1",
            "UseRemote": "0",
            "UseCloud": "0",
            "ReplaceReport": "1",
            "ShutdownTerminal": "1",
            "FromDate": plan["from_date"],
            "ToDate": plan["to_date"],
            "Report": f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}",
            "ExpertParameters": f"{attempt_name}.set",
        },
        header="[Tester]",
    )
    variant = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "priority": plan["priority"],
        "source_run_id": source_info["source_run_id"],
        "source_variant_id": source_info["source_variant_id"],
        "candidate_id": plan["candidate_id"],
        "candidate_alias": candidate_alias,
        "candidate_role": plan["candidate_role"],
        "profile_label": plan["profile_label"],
        "profile_token": plan["profile_token"],
        "materialization_type": plan["materialization_type"],
        "split": plan["split"],
        "period_label": plan["period_label"],
        "targeted_weakness": plan["targeted_weakness"],
        "runtime_model_file": model_copy["path"],
        "runtime_model_sha256": model_copy["sha256"],
        "common_model_path": common_model["common_path"],
        "common_model_sha256": common_model["sha256"],
        "runtime_feature_file": feature_copy["path"],
        "runtime_feature_sha256": feature_copy["sha256"],
        "common_feature_path": common_feature["common_path"],
        "common_feature_sha256": common_feature["sha256"],
        "feature_count": stats["feature_count"],
        "feature_order": stats["feature_order"],
        "feature_order_hash": stats["feature_order_hash"],
        "known_difference": plan["known_difference"],
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    feature_row = {
        "variant_id": variant_id,
        "candidate_alias": candidate_alias,
        "source_feature_path": source_info["source_feature_path"],
        "runtime_feature_file": feature_copy["path"],
        "runtime_feature_sha256": feature_copy["sha256"],
        "common_feature_path": common_feature["common_path"],
        "feature_rows": stats["feature_rows"],
        "feature_count": stats["feature_count"],
        "first_time": stats["first_time"],
        "last_time": stats["last_time"],
        "feature_order_hash": stats["feature_order_hash"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_row = {
        "variant_id": variant_id,
        "candidate_alias": candidate_alias,
        "source_model_path": source_info["source_model_path"],
        "runtime_model_file": model_copy["path"],
        "runtime_model_sha256": model_copy["sha256"],
        "common_model_path": common_model["common_path"],
        "common_model_sha256": common_model["sha256"],
        "model_backend": "ebm_table",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    attempt = {
        "attempt_name": attempt_name,
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "priority": plan["priority"],
        "candidate_id": plan["candidate_id"],
        "candidate_alias": candidate_alias,
        "candidate_role": plan["candidate_role"],
        "profile_label": plan["profile_label"],
        "tier": "Tier A",
        "split": plan["split"],
        "period_label": plan["period_label"],
        "from_date": plan["from_date"],
        "to_date": plan["to_date"],
        "attempt_role": plan["attempt_role"],
        "set_path": set_payload["path"],
        "set_sha256": set_payload["sha256"],
        "ini_path": ini_payload["path"],
        "ini_sha256": ini_payload["sha256"],
        "telemetry_path": telemetry,
        "summary_path": summary,
        "execution_status": "materialized_execution_pending",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    preflight = {
        "attempt_name": attempt_name,
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "candidate_alias": candidate_alias,
        "feature_exists": path_exists(feature_path),
        "model_exists": path_exists(model_path),
        "common_feature_path": common_feature["common_path"],
        "common_feature_sha256": common_feature["sha256"],
        "common_model_path": common_model["common_path"],
        "common_model_sha256": common_model["sha256"],
        "set_path": set_payload["path"],
        "ini_path": ini_payload["path"],
        "preflight_status": "ready_for_mt5_execution",
        "effect": "Common Files(공통 파일) 인계가 먼저 증명되어 init failure(초기화 실패)와 성능 실패를 분리한다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return variant, feature_row, model_row, attempt, preflight


def materialization_plan_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    queue_by_id = {row["queue_id"]: row for row in queue_rows}
    rows: list[dict[str, Any]] = []
    for plan in PLAN_CONFIGS:
        queue = queue_by_id[str(plan["queue_id"])]
        rows.append(
            {
                "plan_id": plan["variant_id"],
                "queue_id": plan["queue_id"],
                "priority": plan["priority"],
                "candidate_alias": plan["candidate_alias"],
                "candidate_id": plan["candidate_id"],
                "workstream": queue.get("workstream"),
                "materialization_type": plan["materialization_type"],
                "split": plan["split"],
                "period_label": plan["period_label"],
                "targeted_weakness": plan["targeted_weakness"],
                "source_kind": plan["source_kind"],
                "source_variant_id": plan.get("source_variant_id") or f"{plan.get('source_candidate_id')}_{plan.get('source_split')}",
                "changed_variables": queue.get("changed_variables"),
                "control_variables": queue.get("control_variables"),
                "known_difference": plan["known_difference"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def held_queue_rows() -> list[dict[str, Any]]:
    return [{**row, "claim_boundary": CLAIM_BOUNDARY} for row in HELD_QUEUE_CONFIGS]


def anti_filter_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267dy_q06_anti_filter_stack",
            "queue_id": "q06_prune_micro_filter_stack",
            "status": "enforced",
            "forbidden_pattern": "hour-only;weekday-only;month-only exclusion",
            "materialized_standalone": "false",
            "effect": "약한 구간을 단순 제외하지 않고 q01/q02 구조 시험으로 바꾼다.",
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
        queue_id = str(row["queue_id"])
        variants_by_queue[queue_id] = variants_by_queue.get(queue_id, 0) + 1
    for row in attempt_rows:
        queue_id = str(row["queue_id"])
        attempts_by_queue[queue_id] = attempts_by_queue.get(queue_id, 0) + 1
    held_by_id = {str(row["queue_id"]): row for row in held_rows}
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        queue_id = str(queue["queue_id"])
        held = held_by_id.get(queue_id)
        if held:
            decision = str(held["decision"])
            effect = "standalone MT5(MetaTrader 5, 메타트레이더5) 실행을 만들지 않아 필터 누적 루프를 막는다."
        elif queue_id == "q05_s264_lc_same_month_control_hold":
            decision = "materialized_as_paired_control(쌍 대조로 물질화)"
            effect = "q03/q04 해석용 같은 월 control(대조)을 제공한다."
        else:
            decision = "materialized_for_mt5_execution"
            effect = "다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 곡선/약점 구간/거래 품질을 볼 수 있다."
        rows.append(
            {
                "queue_id": queue_id,
                "priority": queue.get("priority"),
                "candidate_aliases": queue.get("candidate_aliases"),
                "workstream": queue.get("workstream"),
                "decision": decision,
                "variant_count": variants_by_queue.get(queue_id, 0),
                "attempt_count": attempts_by_queue.get(queue_id, 0),
                "held_count": 1 if held else 0,
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
            "queue_id": row["queue_id"],
            "shared_contract": "US100 M5;RuntimeProbeEA;ebm_table_csv;feature_order_hash_tracked;Common Files handoff",
            "tier_pair_boundary": TIER_PAIR_BOUNDARY,
            "runtime_status": "materialized_execution_pending",
            "runtime_claim": "runtime reproduction pending(런타임 재현 대기)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in variant_rows
    ]


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
            "evidence_plan": row.get("evidence_plan"),
            "materialization_status": "materialized" if row["queue_id"] != "q06_prune_micro_filter_stack" else "held_guardrail_only",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in queue_rows
    ]


def environment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267dy_common_files_handoff",
            "status": "prepared",
            "evidence": f"variants={counts['variants']};attempts={counts['attempts']}",
            "effect": "MT5(MetaTrader 5, 메타트레이더5) 실행 전 feature/model(피처/모델) 경로를 Common Files(공통 파일)에 복사했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": f"run267dy_data_{row['variant_id']}",
            "variant_id": row["variant_id"],
            "feature_rows": row["feature_rows"],
            "feature_count": row["feature_count"],
            "first_time": row["first_time"],
            "last_time": row["last_time"],
            "feature_order_hash": row["feature_order_hash"],
            "status": "feature_frame_copied_order_tracked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in feature_rows
    ]


def runtime_parity_rows(variant_rows: Sequence[Mapping[str, Any]], attempt_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    attempts_by_variant = {row["variant_id"]: row for row in attempt_rows}
    return [
        {
            "variant_id": row["variant_id"],
            "attempt_name": attempts_by_variant[row["variant_id"]]["attempt_name"],
            "feature_order_hash": row["feature_order_hash"],
            "set_path": attempts_by_variant[row["variant_id"]]["set_path"],
            "ini_path": attempts_by_variant[row["variant_id"]]["ini_path"],
            "runtime_parity_status": "handoff_materialized_parity_unproven",
            "effect": "Python(파이썬) 연구 표면과 MT5(MetaTrader 5, 메타트레이더5) 입력의 feature order(피처 순서)를 추적한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in variant_rows
    ]


def result_judgment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"variants={counts['variants']};attempts={counts['attempts']};held_rows={counts['held_rows']}",
            "evidence_missing": "MT5 execution result(실행 결과), balance/equity review(잔액/평가금 검토)",
            "judgment_label": "materialized_execution_pending_no_candidate_selection",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이번 작업은 실험 입력을 만든 것이며 아직 성능 판정이 아니다.",
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "gate267dy_source_inputs",
            "gate_name": "source inputs present(원천 입력 존재)",
            "status": "pass",
            "evidence": f"{rel(SOURCE_QUEUE_PATH)};{rel(SOURCE_DU_VARIANT_MANIFEST_PATH)};{rel(SOURCE_FEATURE_MANIFEST_PATH)}",
            "effect": "run267DX 설계와 이전 materialization(물질화) 근거에서 시작한다.",
        },
        {
            "gate_id": "gate267dy_materialization_count",
            "gate_name": "materialization count(물질화 수)",
            "status": "pass",
            "evidence": f"variants={counts['variants']};attempts={counts['attempts']}",
            "effect": "run267DZ 실행 가능한 set/ini(설정/초기화)를 만들었다.",
        },
        {
            "gate_id": "gate267dy_repair_cap",
            "gate_name": "repair cap preserved(수리 제한 보존)",
            "status": "pass",
            "evidence": "q03 has one validation anchor repair attempt",
            "effect": "s264_aih 수리 분기를 길게 끌지 않는다.",
        },
        {
            "gate_id": "gate267dy_anti_filter_stack",
            "gate_name": "anti filter stack enforced(필터 누적 방지)",
            "status": "pass",
            "evidence": "q06 held; no hour-only/weekday-only/month-only standalone attempt",
            "effect": "약한 구간 제외형 미세 조정을 물질화하지 않았다.",
        },
        {
            "gate_id": "gate267dy_claim_guard",
            "gate_name": "claim guard(주장 가드)",
            "status": "pass",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "R&D racing(연구개발 경주) 입력 생성으로만 경계를 둔다.",
        },
    ]


def source_paths() -> dict[str, str]:
    return {
        "source_queue": rel(SOURCE_QUEUE_PATH),
        "source_branch_decision": rel(SOURCE_BRANCH_DECISION_PATH),
        "source_prune_matrix": rel(SOURCE_PRUNE_MATRIX_PATH),
        "source_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
        "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
        "source_design_report": rel(SOURCE_DESIGN_REPORT_PATH),
        "source_du_variant_manifest": rel(SOURCE_DU_VARIANT_MANIFEST_PATH),
        "source_du_attempt_manifest": rel(SOURCE_DU_ATTEMPT_MANIFEST_PATH),
        "source_feature_manifest": rel(SOURCE_FEATURE_MANIFEST_PATH),
    }


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
        "preflight_handoff_receipt": rel(PREFLIGHT_RECEIPT_PATH),
        "anti_filter_stack_receipt": rel(ANTI_FILTER_STACK_RECEIPT_PATH),
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


def run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_du_run_id": SOURCE_DU_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "counts": result["counts"],
        "next_action": NEXT_ACTION,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def lineage(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_inputs": source_paths(),
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": output_paths(),
        "artifact_hashes": {
            key: sha256_file_lf_normalized(repo_path(path))
            for key, path in output_paths().items()
            if path_exists(repo_path(path))
        },
        "registry_links": {
            "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
            "run_registry": rel(RUN_REGISTRY_PATH),
            "alpha_ledger": rel(PROJECT_LEDGER_PATH),
            "stage_ledger": rel(STAGE_LEDGER_PATH),
        },
        "availability": "tracked_after_commit",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267DY Runtime Gap Aware Sixth Follow-Up/Prune Materialization(267단계 267DY 런타임 공백 반영 6차 후속/가지치기 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- variants(변형): `{counts['variants']}`",
        f"- attempts(시도): `{counts['attempts']}`",
        f"- held_rows(보류 행): `{counts['held_rows']}`",
        f"- aggressive_or_explosive_attempts(공격/폭발 시도): `{counts['aggressive_attempts']}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267DY(267DY 실행)는 run267DX(267DX 실행)의 설계를 MT5(MetaTrader 5, 메타트레이더5)가 실행할 수 있는 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.",
        "효과: s258_stc(258 STC 후보)는 DD(drawdown, 손실폭) 구조 분리 3개와 불리 구간 반증 3개로 나뉘었다.",
        "효과: s264_aih(264 AIH 후보)는 validation anchor(검증 앵커) 1회 수리와 2026.04 counter shock(반대 충격) 탐침으로 제한했다.",
        "효과: s264_lc(264 LC 후보)는 q03/q04 해석용 같은 달 control(대조)로만 물질화했다.",
        "효과: q06 filter-stack(필터 누적) 분기는 단독 실행하지 않고 held(보류)로 기록했다.",
        "",
        "## Queue Decision(대기열 판단)",
        "",
        "| queue_id(대기열 ID) | decision(판단) | variants(변형) | attempts(시도) |",
        "|---|---|---:|---:|",
    ]
    for row in result["queue_decision"]:
        lines.append(f"| `{row['queue_id']}` | {row['decision']} | {row['variant_count']} | {row['attempt_count']} |")
    lines.extend(
        [
            "",
            "## Attempts(시도)",
            "",
            "| attempt(시도) | candidate(후보) | split(구간) | role(역할) |",
            "|---|---|---|---|",
        ]
    )
    for row in result["attempt_manifest"]:
        lines.append(f"| `{row['attempt_name']}` | `{row['candidate_alias']}` | `{row['split']}` | `{row['attempt_role']}` |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "run267DY(267DY 실행)는 materialization(물질화)이다. MT5(MetaTrader 5, 메타트레이더5) 성능 결과와 balance/equity curve(잔액/평가금 곡선) 검토는 아직 없다.",
            "따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- materialization_plan(물질화 계획): `{rel(MATERIALIZATION_PLAN_PATH)}`",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- preflight_handoff_receipt(사전 인계 영수증): `{rel(PREFLIGHT_RECEIPT_PATH)}`",
            f"- anti_filter_stack_receipt(필터 누적 방지 영수증): `{rel(ANTI_FILTER_STACK_RECEIPT_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    specs: list[tuple[str, str, Path, str]] = [
        ("stage267_run267DY_producer", "producer_script", PRODUCER_PATH, "Builds run267DY sixth follow-up/prune materialization."),
        ("stage267_run267DY_source_queue", "source_queue", SOURCE_QUEUE_PATH, "Source run267DX queue."),
        ("stage267_run267DY_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH, "Materialization plan."),
        ("stage267_run267DY_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Queue decision."),
        ("stage267_run267DY_feature_frame_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Feature frame manifest."),
        ("stage267_run267DY_model_manifest", "model_manifest", MODEL_MANIFEST_PATH, "Model manifest."),
        ("stage267_run267DY_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Variant manifest."),
        ("stage267_run267DY_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Attempt manifest."),
        ("stage267_run267DY_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract."),
        ("stage267_run267DY_held_queue", "held_queue", HELD_QUEUE_PATH, "Held queue."),
        ("stage267_run267DY_preflight_handoff", "preflight_handoff_receipt", PREFLIGHT_RECEIPT_PATH, "Preflight handoff receipt."),
        ("stage267_run267DY_anti_filter_stack", "anti_filter_stack_receipt", ANTI_FILTER_STACK_RECEIPT_PATH, "Anti filter-stack receipt."),
        ("stage267_run267DY_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267DY_environment", "environment_reproducibility_receipt", ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, "Environment receipt."),
        ("stage267_run267DY_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267DY_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267DY_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DY_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267DY_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267DY_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267DY_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267DY_report", "review_report", REPORT_PATH, "User-facing report."),
    ]
    for row in result["variant_manifest"]:
        specs.append((f"stage267_run267DY_feature_{row['variant_id']}", "runtime_feature_frame", repo_path(row["runtime_feature_file"]), "Runtime feature copy."))
        specs.append((f"stage267_run267DY_model_{row['variant_id']}", "runtime_model_table", repo_path(row["runtime_model_file"]), "Runtime model copy."))
    for row in result["attempt_manifest"]:
        specs.append((f"stage267_run267DY_set_{row['attempt_name']}", "mt5_set", repo_path(row["set_path"]), "MT5 set file."))
        specs.append((f"stage267_run267DY_ini_{row['attempt_name']}", "mt5_ini", repo_path(row["ini_path"]), "MT5 tester ini file."))
    rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, notes in specs:
        rows.append(
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
        )
    return rows


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    notes = f"variants={counts['variants']};attempts={counts['attempts']};held={counts['held_rows']};next_action={NEXT_ACTION}."
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_gap_aware_sixth_followup_or_prune_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    stage_row = {
        "row_id": "stage267_run267DY_runtime_gap_aware_sixth_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_sixth_followup_or_prune_materialization",
        "tier_scope": "Tier A materialized; q06 guardrail held",
        "scoreboard": "execution_pending_no_candidate_selection_no_onnx",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "feature_model_set_ini_handoff_materialized_no_mt5_kpi",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_sixth_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_sixth_followup_or_prune_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization",
        "tier_scope": "Tier A materialized; q06 guardrail held",
        "kpi_scope": "execution_pending_no_kpi",
        "scoreboard_lane": "runtime_gap_aware_materialization",
        "status": "out_of_scope_by_claim",
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={counts['variants']};attempts={counts['attempts']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"Next action: {NEXT_ACTION}. Materialization only; MT5 output missing.",
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at, result), key="artifact_id")


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


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def stage267_report_entry() -> str:
    return f"  run267DY_runtime_gap_aware_sixth_followup_or_prune_materialization_report_path: {rel(REPORT_PATH)}"


def update_stage267_workspace_block(text: str) -> str:
    report_entry = stage267_report_entry()
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    report_seen = report_entry in text
    for line in lines:
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" "):
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


def update_current_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267DY_runtime_gap_aware_sixth_followup_or_prune_materialization"
        f"(267DY 런타임 공백 반영 6차 후속/가지치기 물질화): `{rel(REPORT_PATH)}`"
    )
    latest_line = (
        f"- latest_materialization(최신 물질화): run267DY(267DY 실행) variants(변형) `{counts['variants']}`, "
        f"attempts(시도) `{counts['attempts']}`, held_rows(보류 행) `{counts['held_rows']}`, report(보고서) `{rel(REPORT_PATH)}`."
    )
    block = "\n".join(
        [
            "Run267DY(267DY 실행)는 run267DX(267DX 실행)의 6차 follow-up/prune queue(후속/가지치기 대기열)를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.",
            f"Effect(효과): variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개를 만들었고, q06 filter-stack(필터 누적) 분기는 단독 실행하지 않았다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_sixth_followup_or_prune_materialization`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_after_contains(current, "stage267_run267DX_runtime_gap_aware_sixth_followup_or_prune_design.md", report_line)
    current = append_after_contains(current, "## Current Next Action", latest_line)
    current = append_block_once(current, "Run267DY(267DY 실행)는 run267DX", block)
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_after_contains(selection, "stage267_run267DX_runtime_gap_aware_sixth_followup_or_prune_design", report_line)
    selection = append_block_once(selection, "Run267DY(267DY 실행)는 run267DX", block)
    write_md(SELECTION_STATUS_PATH, selection)

    review_index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_index = replace_line_prefix(review_index, "- status(상태):", f"- status(상태): `{STATUS}`")
    review_index = replace_line_prefix(review_index, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(review_index, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review_index = append_after_contains(review_index, "stage267_run267DX_runtime_gap_aware_sixth_followup_or_prune_design.md", report_line)
    review_index = append_block_once(review_index, "Run267DY(267DY 실행)는 run267DX", block)
    write_md(REVIEW_INDEX_PATH, review_index)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = update_stage267_workspace_block(workspace)
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267DY(267DY 실행) runtime gap aware sixth follow-up/prune materialization"
        f"(런타임 공백 반영 6차 후속/가지치기 물질화) `{STATUS}`. "
        f"Effect(효과): run267DX(267DX 실행)의 queue(대기열)를 variants(변형) `{counts['variants']}`개와 attempts(시도) `{counts['attempts']}`개로 바꿨고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_line, 1)
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
    write_csv(PREFLIGHT_RECEIPT_PATH, result["preflight_handoff_receipt"])
    write_csv(ANTI_FILTER_STACK_RECEIPT_PATH, result["anti_filter_stack_receipt"])
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


def build_result() -> dict[str, Any]:
    required = [
        SOURCE_QUEUE_PATH,
        SOURCE_BRANCH_DECISION_PATH,
        SOURCE_PRUNE_MATRIX_PATH,
        SOURCE_FAILURE_MEMORY_PATH,
        SOURCE_REVIEW_RESULT_PATH,
        SOURCE_DU_VARIANT_MANIFEST_PATH,
        SOURCE_DU_ATTEMPT_MANIFEST_PATH,
        SOURCE_DU_RUNTIME_CONTRACT_PATH,
        SOURCE_FEATURE_MANIFEST_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))
    created_at = utc_now()
    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    variant_by_id = source_variant_rows()
    attempts = source_attempt_rows()
    canonical = canonical_source_rows()
    plan_rows = materialization_plan_rows(queue_rows)
    variant_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    preflight_rows: list[dict[str, Any]] = []
    for index, plan in enumerate(PLAN_CONFIGS, start=1):
        variant, feature, model, attempt, preflight = materialize_plan(plan, variant_by_id, attempts, canonical, index)
        variant_rows.append(variant)
        feature_rows.append(feature)
        model_rows.append(model)
        attempt_rows.append(attempt)
        preflight_rows.append(preflight)
    held = held_queue_rows()
    anti_filter = anti_filter_stack_rows()
    queue_decisions = queue_decision_rows(queue_rows, variant_rows, attempt_rows, held)
    counts = {
        "missing_required": len(missing),
        "queue_rows": len(queue_rows),
        "variants": len(variant_rows),
        "attempts": len(attempt_rows),
        "feature_frames": len(feature_rows),
        "models": len(model_rows),
        "preflight_receipts": len(preflight_rows),
        "held_rows": len(held),
        "anti_filter_stack_receipts": len(anti_filter),
        "aggressive_attempts": sum(1 for row in attempt_rows if row["priority"] in {"P0_falsification", "P0_explosive"}),
        "structural_attempts": sum(1 for row in attempt_rows if row["priority"] == "P0_structural"),
        "repair_attempts": sum(1 for row in attempt_rows if row["priority"] == "P0_repair"),
        "control_attempts": sum(1 for row in attempt_rows if "control" in str(row["priority"])),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_du_run_id": SOURCE_DU_RUN_ID,
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
        "materialization_plan": plan_rows,
        "queue_decision": queue_decisions,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "runtime_contract": runtime_contract_rows(variant_rows),
        "held_queue": held,
        "preflight_handoff_receipt": preflight_rows,
        "anti_filter_stack_receipt": anti_filter,
        "experiment_design_receipt": experiment_design_rows(queue_rows),
        "environment_reproducibility_receipt": environment_rows(counts),
        "data_integrity_receipt": data_integrity_rows(feature_rows),
        "runtime_parity_receipt": runtime_parity_rows(variant_rows, attempt_rows),
        "result_judgment": result_judgment_rows(counts),
        "gate_audit": gate_audit_rows(counts),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


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
                "aggressive_attempts": counts["aggressive_attempts"],
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
