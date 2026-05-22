from __future__ import annotations

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
from stage_pipelines.stage267 import (
    run267DY_runtime_gap_aware_sixth_followup_or_prune_materialization as materializer_template,
)
from stage_pipelines.stage267 import (
    run267EO_runtime_gap_aware_tenth_followup_or_prune_materialization as source_materialization,
)
from stage_pipelines.stage267 import (
    run267ER_runtime_gap_aware_tenth_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267ES"
RUN_ID = "run267ES_stage267_runtime_gap_aware_tenth_followup_or_prune_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_materialization.RUN_ID
STATUS = "run267ES_runtime_gap_aware_tenth_followup_or_prune_materialized_execution_pending"
JUDGMENT = "runtime_gap_aware_tenth_followup_or_prune_materialized_no_candidate_selection"
NEXT_ACTION = "run267ET_execute_runtime_gap_aware_tenth_followup_or_prune_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_tenth_followup_or_prune_materialization"
FEATURE_ROOT = RUN_ROOT / "features"
VARIANT_ROOT = RUN_ROOT / "variants"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_QUEUE_PATH = source_design.MATERIALIZATION_QUEUE_PATH
SOURCE_FEATURE_BLUEPRINT_PATH = source_design.FEATURE_BLUEPRINT_PATH
SOURCE_BRANCH_DECISION_PATH = source_design.BRANCH_DECISION_PATH
SOURCE_PRUNE_MATRIX_PATH = source_design.PRUNE_MATRIX_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_HANDOFF_TRIAGE_PATH = source_design.HANDOFF_TRIAGE_PATH
SOURCE_IDENTITY_AUDIT_PATH = source_design.IDENTITY_AUDIT_PATH
SOURCE_AGGRESSIVE_REENTRY_PATH = source_design.AGGRESSIVE_REENTRY_PATH
SOURCE_REVIEW_RESULT_PATH = source_design.REVIEW_RESULT_PATH
SOURCE_DESIGN_REPORT_PATH = source_design.REPORT_PATH
SOURCE_PREVIOUS_VARIANT_MANIFEST_PATH = source_materialization.VARIANT_MANIFEST_PATH
SOURCE_PREVIOUS_ATTEMPT_MANIFEST_PATH = source_materialization.ATTEMPT_MANIFEST_PATH
SOURCE_PREVIOUS_RUNTIME_CONTRACT_PATH = source_materialization.RUNTIME_CONTRACT_PATH
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
POOL_COVERAGE_RECEIPT_PATH = RUN_ROOT / "pool_coverage_receipt.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH = RUN_ROOT / "environment_reproducibility_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267ES_runtime_gap_aware_tenth_followup_or_prune_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267ES_runtime_gap_aware_tenth_followup_or_prune_materialization.py")

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

COMMON_ROOT = "OPV2/s267es/run267ES_runtime_gap_aware_tenth_followup_or_prune"
EXPLORATION_LABEL = "stage267_BaselineRacing__RuntimeGapAwareTenthFollowupOrPrune"
MATERIALIZATION_BOUNDARY = "materialization_only_execution_pending_no_candidate_selection_no_selected_research_baseline_no_onnx"
TIER_PAIR_BOUNDARY = "Tier A materialized for tenth follow-up/prune; true Tier B fallback and actual routed total remain unclaimed."


def make_plan(
    *,
    queue_id: str,
    source_variant_id: str,
    variant_id: str,
    candidate_id: str,
    candidate_alias: str,
    candidate_role: str,
    profile_label: str,
    profile_token: str,
    materialization_type: str,
    split: str,
    period_label: str,
    from_date: str,
    to_date: str,
    attempt_role: str,
    priority: str,
    targeted_weakness: str,
    known_difference: str,
    set_updates: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "queue_id": queue_id,
        "source_kind": "du",
        "source_variant_id": source_variant_id,
        "variant_id": variant_id,
        "candidate_id": candidate_id,
        "candidate_alias": candidate_alias,
        "candidate_role": candidate_role,
        "profile_label": profile_label,
        "profile_token": profile_token,
        "materialization_type": materialization_type,
        "split": split,
        "period_label": period_label,
        "from_date": from_date,
        "to_date": to_date,
        "attempt_role": attempt_role,
        "priority": priority,
        "targeted_weakness": targeted_weakness,
        "set_updates": dict(set_updates or {}),
        "known_difference": known_difference,
    }


PLAN_CONFIGS: tuple[dict[str, Any], ...] = (
    make_plan(
        queue_id="q01_runtime_handoff_gap_bounded_triage",
        source_variant_id="run267eo_01_s258_stc_2025h1_survival_handoff_precheck",
        variant_id="run267es_01_s258_stc_2025h1_survival_handoff_precheck",
        candidate_id="s258_short_tight_control",
        candidate_alias="s258_stc",
        candidate_role="stress_challenger",
        profile_label="s258_stc_2025h1_survival_handoff_precheck",
        profile_token="runtime_gap_precheck",
        materialization_type="handoff_precheck_representative",
        split="adjacent_2025_h1_validation_post_2024",
        period_label="2025H1",
        from_date="2025.01.02",
        to_date="2025.07.01",
        attempt_role="survival_handoff_precheck_2025h1",
        priority="P0_handoff_precheck",
        targeted_weakness="s258 survival row blocked before runtime output(런타임 출력 전 차단)",
        known_difference="Keeps the previous survival setup but records this as handoff precheck, not performance repair.",
        set_updates={"InpModelRiskMaxPct": "0.020", "InpSameDirectionReentryCooldownBars": "8"},
    ),
    make_plan(
        queue_id="q01_runtime_handoff_gap_bounded_triage",
        source_variant_id="run267eo_02_s258_stc_2025h2_explosive_handoff_precheck",
        variant_id="run267es_02_s258_stc_2025h2_explosive_handoff_precheck",
        candidate_id="s258_short_tight_control",
        candidate_alias="s258_stc",
        candidate_role="stress_challenger",
        profile_label="s258_stc_2025h2_explosive_handoff_precheck",
        profile_token="runtime_gap_precheck",
        materialization_type="explosive_handoff_precheck_representative",
        split="adjacent_2025_h2_oos_followthrough",
        period_label="2025H2",
        from_date="2025.07.01",
        to_date="2026.01.01",
        attempt_role="explosive_handoff_precheck_2025h2",
        priority="P0_handoff_precheck",
        targeted_weakness="s258 aggressive row blocked before runtime output(공격 행 런타임 출력 전 차단)",
        known_difference="Uses one aggressive s258 representative so the handoff gap is not mistaken for market failure.",
        set_updates={"InpShortThreshold": "0.500", "InpLongThreshold": "0.480", "InpModelRiskMaxPct": "0.026"},
    ),
    make_plan(
        queue_id="q01_runtime_handoff_gap_bounded_triage",
        source_variant_id="run267eo_03_s264_aih_validation_explosive_handoff_precheck",
        variant_id="run267es_03_s264_aih_validation_explosive_handoff_precheck",
        candidate_id="s264_allow_inner_high_quarter",
        candidate_alias="s264_aih",
        candidate_role="core_challenger",
        profile_label="s264_aih_validation_explosive_handoff_precheck",
        profile_token="runtime_gap_precheck",
        materialization_type="explosive_handoff_precheck_representative",
        split="validation_is",
        period_label="validation",
        from_date="2024.01.02",
        to_date="2026.04.01",
        attempt_role="validation_explosive_handoff_precheck",
        priority="P0_handoff_precheck",
        targeted_weakness="s264_aih validation aggressive branch blocked before runtime output(검증 공격 분기 차단)",
        known_difference="Rechecks the aggressive branch handoff without treating the blocked row as performance evidence.",
        set_updates={"InpShortThreshold": "0.510", "InpLongThreshold": "0.490", "InpModelRiskMaxPct": "0.024"},
    ),
    make_plan(
        queue_id="q01_runtime_handoff_gap_bounded_triage",
        source_variant_id="run267eo_04_s264_aih_202604_explosive_handoff_precheck",
        variant_id="run267es_04_s264_aih_202604_explosive_handoff_precheck",
        candidate_id="s264_allow_inner_high_quarter",
        candidate_alias="s264_aih",
        candidate_role="core_challenger",
        profile_label="s264_aih_202604_explosive_handoff_precheck",
        profile_token="runtime_gap_precheck",
        materialization_type="explosive_handoff_precheck_representative",
        split="oos_final_202604",
        period_label="202604",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="final_month_explosive_handoff_precheck",
        priority="P0_handoff_precheck",
        targeted_weakness="s264_aih 2026.04 aggressive branch blocked before runtime output(2026.04 공격 분기 차단)",
        known_difference="Keeps final-month pressure but classifies handoff before performance judgment.",
        set_updates={"InpShortThreshold": "0.510", "InpLongThreshold": "0.490", "InpModelRiskMaxPct": "0.024"},
    ),
    make_plan(
        queue_id="q02_202604_shared_sell_fragility_pivot",
        source_variant_id="run267eo_05_s264_aih_202604_shared_state_pivot",
        variant_id="run267es_05_s264_aih_202604_shared_state_pivot",
        candidate_id="s264_allow_inner_high_quarter",
        candidate_alias="s264_aih",
        candidate_role="core_challenger",
        profile_label="s264_aih_202604_shared_state_pivot",
        profile_token="shared_adverse_state",
        materialization_type="shared_adverse_state_feature_pivot",
        split="oos_final_202604",
        period_label="202604",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="shared_state_pivot_core_202604",
        priority="P0_structural_pivot",
        targeted_weakness="2026.04 shared sell-pressure loss without naked month filter(월 필터 없는 공유 매도 압박 손실)",
        known_difference="Adds structural adverse-state pressure while preserving the candidate surface.",
        set_updates={"InpEntryTransitionOnly": "true", "InpSameDirectionReentryCooldownBars": "6", "InpModelRiskMaxPct": "0.020"},
    ),
    make_plan(
        queue_id="q02_202604_shared_sell_fragility_pivot",
        source_variant_id="run267eo_06_s264_lc_202604_shared_state_control",
        variant_id="run267es_06_s264_lc_202604_shared_state_control",
        candidate_id="s264_lowrank_control",
        candidate_alias="s264_lc",
        candidate_role="defensive_control",
        profile_label="s264_lc_202604_shared_state_control",
        profile_token="shared_adverse_state_control",
        materialization_type="shared_adverse_state_control",
        split="oos_final_202604",
        period_label="202604",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="shared_state_control_202604",
        priority="P0_structural_control",
        targeted_weakness="defensive control response to 2026.04 shared adverse state(공유 불리 상태 방어 대조)",
        known_difference="Keeps s264_lc as market control, not selected candidate.",
        set_updates={"InpEntryTransitionOnly": "true", "InpSameDirectionReentryCooldownBars": "6", "InpModelRiskMaxPct": "0.019"},
    ),
    make_plan(
        queue_id="q02_202604_shared_sell_fragility_pivot",
        source_variant_id="run267eo_07_s262_lih_202604_shared_state_pivot",
        variant_id="run267es_07_s262_lih_202604_shared_state_pivot",
        candidate_id="s262_lowrank_inner_half_filter",
        candidate_alias="s262_lih",
        candidate_role="validation_heavy",
        profile_label="s262_lih_202604_shared_state_pivot",
        profile_token="shared_adverse_state",
        materialization_type="shared_adverse_state_feature_pivot",
        split="oos_final_202604",
        period_label="202604",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="shared_state_validation_heavy_202604",
        priority="P0_structural_pivot",
        targeted_weakness="validation-heavy response to shared final-month pressure(검증 중심 후보의 마지막 달 압박)",
        known_difference="Checks whether validation-heavy surface loses less under the same structural pressure.",
        set_updates={"InpEntryTransitionOnly": "true", "InpSameDirectionReentryCooldownBars": "6", "InpModelRiskMaxPct": "0.019"},
    ),
    make_plan(
        queue_id="q02_202604_shared_sell_fragility_pivot",
        source_variant_id="run267eo_08_s264_aia_202604_shared_state_pivot",
        variant_id="run267es_08_s264_aia_202604_shared_state_pivot",
        candidate_id="s264_allow_inner_all_oos_anchor",
        candidate_alias="s264_aia",
        candidate_role="oos_anchor",
        profile_label="s264_aia_202604_shared_state_pivot",
        profile_token="shared_adverse_state",
        materialization_type="shared_adverse_state_feature_pivot",
        split="oos_final_202604",
        period_label="202604",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="shared_state_oos_anchor_202604",
        priority="P0_structural_pivot",
        targeted_weakness="OOS anchor response to shared final-month pressure(표본외 앵커의 마지막 달 압박)",
        known_difference="Checks whether the OOS anchor behaves independently from s262_lih.",
        set_updates={"InpEntryTransitionOnly": "true", "InpSameDirectionReentryCooldownBars": "6", "InpModelRiskMaxPct": "0.019"},
    ),
    make_plan(
        queue_id="q03_s262_s264_aia_signature_collapse_audit",
        source_variant_id="run267eo_09_s262_lih_validation_identity_receipt",
        variant_id="run267es_09_s262_lih_validation_identity_receipt",
        candidate_id="s262_lowrank_inner_half_filter",
        candidate_alias="s262_lih",
        candidate_role="validation_heavy",
        profile_label="s262_lih_validation_identity_receipt",
        profile_token="identity_audit",
        materialization_type="identity_surface_receipt",
        split="validation_is",
        period_label="validation",
        from_date="2024.01.02",
        to_date="2026.04.01",
        attempt_role="identity_surface_receipt_s262",
        priority="P1_identity_audit",
        targeted_weakness="duplicate KPI signature identity risk(중복 KPI 서명 정체성 위험)",
        known_difference="Preserves feature/model/route hash receipts before counting s262_lih as independent evidence.",
        set_updates={"InpModelRiskMaxPct": "0.018"},
    ),
    make_plan(
        queue_id="q03_s262_s264_aia_signature_collapse_audit",
        source_variant_id="run267eo_10_s264_aia_validation_identity_receipt",
        variant_id="run267es_10_s264_aia_validation_identity_receipt",
        candidate_id="s264_allow_inner_all_oos_anchor",
        candidate_alias="s264_aia",
        candidate_role="oos_anchor",
        profile_label="s264_aia_validation_identity_receipt",
        profile_token="identity_audit",
        materialization_type="identity_surface_receipt",
        split="validation_is",
        period_label="validation",
        from_date="2024.01.02",
        to_date="2026.04.01",
        attempt_role="identity_surface_receipt_s264_aia",
        priority="P1_identity_audit",
        targeted_weakness="duplicate KPI signature identity risk(중복 KPI 서명 정체성 위험)",
        known_difference="Preserves feature/model/route hash receipts before counting s264_aia as independent evidence.",
        set_updates={"InpModelRiskMaxPct": "0.018"},
    ),
    make_plan(
        queue_id="q05_aggressive_experiment_after_handoff_fix",
        source_variant_id="run267eo_11_s258_stc_aggressive_nonfilter_reentry",
        variant_id="run267es_11_s258_stc_aggressive_nonfilter_reentry",
        candidate_id="s258_short_tight_control",
        candidate_alias="s258_stc",
        candidate_role="stress_challenger",
        profile_label="s258_stc_aggressive_nonfilter_reentry",
        profile_token="aggressive_nonfilter_reentry",
        materialization_type="aggressive_nonfilter_reentry",
        split="adjacent_2025_h1_validation_post_2024",
        period_label="2025H1",
        from_date="2025.01.02",
        to_date="2025.07.01",
        attempt_role="aggressive_nonfilter_reentry_s258",
        priority="P2_aggressive_nonfilter",
        targeted_weakness="avoid defensive-only filter stack(방어 필터만 쌓는 흐름 방지)",
        known_difference="Allows one aggressive branch after handoff precheck without naked calendar suppression.",
        set_updates={
            "InpShortThreshold": "0.492",
            "InpLongThreshold": "0.472",
            "InpAtrStopMultiplier": "2.18",
            "InpAtrTakeProfitMultiplier": "5.05",
            "InpModelRiskMaxPct": "0.028",
            "InpSameDirectionReentryCooldownBars": "0",
        },
    ),
    make_plan(
        queue_id="q05_aggressive_experiment_after_handoff_fix",
        source_variant_id="run267eo_12_s264_aih_aggressive_nonfilter_reentry",
        variant_id="run267es_12_s264_aih_aggressive_nonfilter_reentry",
        candidate_id="s264_allow_inner_high_quarter",
        candidate_alias="s264_aih",
        candidate_role="core_challenger",
        profile_label="s264_aih_aggressive_nonfilter_reentry",
        profile_token="aggressive_nonfilter_reentry",
        materialization_type="aggressive_nonfilter_reentry",
        split="oos_final_202604",
        period_label="202604",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="aggressive_nonfilter_reentry_s264_aih",
        priority="P2_aggressive_nonfilter",
        targeted_weakness="s264_aih aggressive counter-impulse without same-month filter(같은 월 필터 없는 공격형 역임펄스)",
        known_difference="One aggressive s264_aih reentry remains conditional on handoff precheck and risk guard.",
        set_updates={
            "InpShortThreshold": "0.505",
            "InpLongThreshold": "0.485",
            "InpAtrStopMultiplier": "2.05",
            "InpAtrTakeProfitMultiplier": "4.95",
            "InpModelRiskMaxPct": "0.026",
            "InpSameDirectionReentryCooldownBars": "0",
        },
    ),
)

HELD_QUEUE_CONFIGS: tuple[dict[str, Any], ...] = (
    {
        "queue_id": "q04_validation_positive_low_pf_watch",
        "priority": "P1",
        "candidate_aliases": "s264_aih;s262_lih;s264_aia",
        "decision": "held_watch_anchor_only_no_standalone_mt5",
        "reason": "positive validation(양수 검증) rows are watch anchors, not selected baseline(선택 기준 후보).",
        "reopen_condition": "materialize only after future review shows cleaner curve and wider-period evidence.",
        "effect": "낮은 PF(수익 팩터) 검증 행을 성급한 후보 선택으로 쓰지 않는다.",
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


def configure_template() -> None:
    replacements: dict[str, Any] = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_DU_RUN_ID": SOURCE_MATERIALIZATION_RUN_ID,
        "STATUS": STATUS,
        "JUDGMENT": JUDGMENT,
        "NEXT_ACTION": NEXT_ACTION,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "STAGE_ROOT": STAGE_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "FEATURE_ROOT": FEATURE_ROOT,
        "VARIANT_ROOT": VARIANT_ROOT,
        "MT5_ROOT": MT5_ROOT,
        "SOURCE_QUEUE_PATH": SOURCE_QUEUE_PATH,
        "SOURCE_BRANCH_DECISION_PATH": SOURCE_BRANCH_DECISION_PATH,
        "SOURCE_PRUNE_MATRIX_PATH": SOURCE_PRUNE_MATRIX_PATH,
        "SOURCE_FAILURE_MEMORY_PATH": SOURCE_FAILURE_MEMORY_PATH,
        "SOURCE_REVIEW_RESULT_PATH": SOURCE_REVIEW_RESULT_PATH,
        "SOURCE_DESIGN_REPORT_PATH": SOURCE_DESIGN_REPORT_PATH,
        "SOURCE_DU_VARIANT_MANIFEST_PATH": SOURCE_PREVIOUS_VARIANT_MANIFEST_PATH,
        "SOURCE_DU_ATTEMPT_MANIFEST_PATH": SOURCE_PREVIOUS_ATTEMPT_MANIFEST_PATH,
        "SOURCE_DU_RUNTIME_CONTRACT_PATH": SOURCE_PREVIOUS_RUNTIME_CONTRACT_PATH,
        "SOURCE_FEATURE_MANIFEST_PATH": SOURCE_FEATURE_MANIFEST_PATH,
        "MATERIALIZATION_PLAN_PATH": MATERIALIZATION_PLAN_PATH,
        "QUEUE_DECISION_PATH": QUEUE_DECISION_PATH,
        "FEATURE_FRAME_MANIFEST_PATH": FEATURE_FRAME_MANIFEST_PATH,
        "MODEL_MANIFEST_PATH": MODEL_MANIFEST_PATH,
        "VARIANT_MANIFEST_PATH": VARIANT_MANIFEST_PATH,
        "ATTEMPT_MANIFEST_PATH": ATTEMPT_MANIFEST_PATH,
        "RUNTIME_CONTRACT_PATH": RUNTIME_CONTRACT_PATH,
        "HELD_QUEUE_PATH": HELD_QUEUE_PATH,
        "PREFLIGHT_RECEIPT_PATH": PREFLIGHT_RECEIPT_PATH,
        "ANTI_FILTER_STACK_RECEIPT_PATH": ANTI_FILTER_STACK_RECEIPT_PATH,
        "EXPERIMENT_DESIGN_RECEIPT_PATH": EXPERIMENT_DESIGN_RECEIPT_PATH,
        "ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH": ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH,
        "DATA_INTEGRITY_RECEIPT_PATH": DATA_INTEGRITY_RECEIPT_PATH,
        "RUNTIME_PARITY_RECEIPT_PATH": RUNTIME_PARITY_RECEIPT_PATH,
        "RESULT_JUDGMENT_PATH": RESULT_JUDGMENT_PATH,
        "GATE_AUDIT_PATH": GATE_AUDIT_PATH,
        "RUN_MANIFEST_PATH": RUN_MANIFEST_PATH,
        "LINEAGE_PATH": LINEAGE_PATH,
        "REVIEW_RESULT_PATH": REVIEW_RESULT_PATH,
        "REPORT_PATH": REPORT_PATH,
        "PRODUCER_PATH": PRODUCER_PATH,
        "COMMON_ROOT": COMMON_ROOT,
        "EXPLORATION_LABEL": EXPLORATION_LABEL,
        "MATERIALIZATION_BOUNDARY": MATERIALIZATION_BOUNDARY,
        "TIER_PAIR_BOUNDARY": TIER_PAIR_BOUNDARY,
        "PLAN_CONFIGS": PLAN_CONFIGS,
        "HELD_QUEUE_CONFIGS": HELD_QUEUE_CONFIGS,
    }
    for name, value in replacements.items():
        setattr(materializer_template, name, value)


def read_csv(path: Path) -> list[dict[str, str]]:
    return materializer_template.read_csv(path)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    materializer_template.write_csv(path, rows)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8-sig",
    )


def write_md(path: Path, text: str) -> None:
    materializer_template.write_md(path, text)


def materialize_plan(
    plan: Mapping[str, Any],
    variant_by_id: Mapping[str, Mapping[str, str]],
    source_attempts: Mapping[str, Sequence[Mapping[str, str]]],
    canonical_by_key: Mapping[tuple[str, str], Mapping[str, str]],
    index: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    variant, feature, model, attempt, preflight = materializer_template.materialize_plan(
        plan, variant_by_id, source_attempts, canonical_by_key, index
    )
    variant["direct_source_materialization_run_id"] = SOURCE_MATERIALIZATION_RUN_ID
    preflight["effect"] = (
        "Common Files(공통 파일) handoff(인계)를 먼저 고정한다. "
        "효과는 init/runtime gap(초기화/런타임 공백)과 market performance(시장 성능)를 분리하는 것이다."
    )
    if str(plan["queue_id"]) == "q05_aggressive_experiment_after_handoff_fix":
        attempt["execution_dependency"] = "requires_q01_precheck_receipt_before_interpretation"
        preflight["preflight_status"] = "ready_but_interpretation_depends_on_q01_precheck"
    else:
        attempt["execution_dependency"] = "none"
    return variant, feature, model, attempt, preflight


def anti_filter_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267es_no_same_month_filter_stack",
            "queue_id": "q02_202604_shared_sell_fragility_pivot",
            "status": "enforced",
            "forbidden_pattern": "same_month_only_filter;hour_only_filter;weekday_only_filter;headline_profit_selection",
            "materialized_standalone": "false",
            "effect": "2026.04 weakness(약점)을 달력 필터로 숨기지 않고 structural feature(구조 피처) 질문으로 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "receipt_id": "run267es_q04_watch_held",
            "queue_id": "q04_validation_positive_low_pf_watch",
            "status": "held",
            "forbidden_pattern": "low_pf_validation_as_selected_baseline",
            "materialized_standalone": "false",
            "effect": "positive validation(양수 검증) 행을 선택 기준 후보로 쓰지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
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
            effect = "watch anchor(관찰 기준점)만 남기고 단독 MT5(MetaTrader 5, 메타트레이더5) 실행은 보류한다."
        elif queue_id == "q05_aggressive_experiment_after_handoff_fix":
            decision = "materialized_conditional_aggressive_after_precheck"
            effect = "공격형 비필터 실험을 남기되 q01 precheck(사전검사) 없이는 해석하지 않는다."
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


def pool_coverage_rows(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    roles = {
        "s264_aih": "core_challenger",
        "s264_lc": "defensive_control",
        "s262_lih": "validation_heavy",
        "s264_aia": "oos_anchor",
        "s258_stc": "stress_challenger",
    }
    rows: list[dict[str, Any]] = []
    for alias, role in roles.items():
        alias_rows = [row for row in variant_rows if row["candidate_alias"] == alias]
        rows.append(
            {
                "receipt_id": f"run267es_{alias}_pool_coverage",
                "candidate_alias": alias,
                "candidate_role": role,
                "variant_count": len(alias_rows),
                "queue_ids": ";".join(sorted({str(row["queue_id"]) for row in alias_rows})),
                "status": "materialized" if alias_rows else "missing_required",
                "effect": "다섯 후보군을 같은 materialization(물질화) 패키지에 유지한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def experiment_design_rows(queue_rows: Sequence[Mapping[str, str]], held_queue_ids: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        queue_id = str(row["queue_id"])
        rows.append(
            {
                "queue_id": queue_id,
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
                "materialization_status": "held_watch_anchor_only" if queue_id in held_queue_ids else "materialized",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def environment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267es_common_files_handoff",
            "status": "prepared",
            "evidence": f"variants={counts['variants']};attempts={counts['attempts']};held={counts['held_rows']}",
            "effect": "feature/model/set/ini(피처/모델/설정/초기화) 파일을 Common Files(공통 파일) 인계 경로와 연결했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": f"run267es_data_{row['variant_id']}",
            "variant_id": row["variant_id"],
            "candidate_alias": row["candidate_alias"],
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


def runtime_parity_rows(
    variant_rows: Sequence[Mapping[str, Any]], attempt_rows: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    attempts_by_variant = {row["variant_id"]: row for row in attempt_rows}
    return [
        {
            "variant_id": row["variant_id"],
            "attempt_name": attempts_by_variant[row["variant_id"]]["attempt_name"],
            "candidate_alias": row["candidate_alias"],
            "feature_order_hash": row["feature_order_hash"],
            "set_path": attempts_by_variant[row["variant_id"]]["set_path"],
            "ini_path": attempts_by_variant[row["variant_id"]]["ini_path"],
            "runtime_parity_status": "handoff_materialized_parity_unproven",
            "effect": "Python(파이썬) 연구 입력과 MT5(MetaTrader 5, 메타트레이더5) 입력의 feature order(피처 순서)를 추적한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in variant_rows
    ]


def result_judgment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": (
                f"variants={counts['variants']};attempts={counts['attempts']};held_rows={counts['held_rows']};"
                f"candidate_aliases={counts['candidate_aliases']};aggressive_attempts={counts['aggressive_attempts']}"
            ),
            "evidence_missing": "MT5 execution result(실행 결과), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질), candidate selection evidence(후보 선택 근거)",
            "judgment_label": "materialized_execution_pending_no_candidate_selection",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이번 작업은 후보를 고른 것이 아니라 다음 MT5 실행 입력을 만든 것이다.",
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "gate267eo_source_inputs",
            "gate_name": "source inputs present(원천 입력 존재)",
            "status": "pass",
            "evidence": f"{rel(SOURCE_QUEUE_PATH)};{rel(SOURCE_PREVIOUS_VARIANT_MANIFEST_PATH)};{rel(SOURCE_FEATURE_MANIFEST_PATH)}",
            "effect": "run267ER 설계와 run267EO 물질화 산출물을 함께 사용한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate267eo_materialization_count",
            "gate_name": "materialization count(물질화 개수)",
            "status": "pass" if counts["variants"] == len(PLAN_CONFIGS) and counts["attempts"] == len(PLAN_CONFIGS) else "fail",
            "evidence": f"variants={counts['variants']};attempts={counts['attempts']};expected={len(PLAN_CONFIGS)}",
            "effect": "다음 run267ET(267ET 실행) 실행 가능한 set/ini(설정/초기화) 묶음을 만들었다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate267eo_candidate_pool_coverage",
            "gate_name": "candidate pool coverage(후보군 커버리지)",
            "status": "pass" if counts["covered_candidate_aliases"] == 5 else "fail",
            "evidence": f"covered_candidate_aliases={counts['covered_candidate_aliases']};aliases={counts['candidate_aliases']}",
            "effect": "다섯 baseline candidate(기준 후보)를 같은 물질화 패키지에 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate267eo_handoff_precheck",
            "gate_name": "handoff precheck included(인계 사전검사 포함)",
            "status": "pass" if counts["handoff_precheck_attempts"] >= 4 else "fail",
            "evidence": f"handoff_precheck_attempts={counts['handoff_precheck_attempts']}",
            "effect": "blocked row(차단 행)를 성능 실패로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate267eo_shared_state_and_identity",
            "gate_name": "shared state plus identity(공유 상태 및 정체성)",
            "status": "pass" if counts["shared_state_attempts"] >= 4 and counts["identity_attempts"] >= 2 else "fail",
            "evidence": f"shared_state_attempts={counts['shared_state_attempts']};identity_attempts={counts['identity_attempts']}",
            "effect": "2026.04 공유 약점과 s262/s264_aia 중복 서명을 함께 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate267eo_aggressive_required",
            "gate_name": "aggressive branch preserved(공격 분기 보존)",
            "status": "pass" if counts["aggressive_attempts"] >= 2 else "fail",
            "evidence": f"aggressive_attempts={counts['aggressive_attempts']}",
            "effect": "방어 필터만 반복하지 않고 공격형 비필터 실험도 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate267eo_claim_guard",
            "gate_name": "claim guard(주장 경계)",
            "status": "pass",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "물질화를 성능 판정이나 ONNX(온엑스) 준비로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
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
        "preflight_handoff_receipt": rel(PREFLIGHT_RECEIPT_PATH),
        "anti_filter_stack_receipt": rel(ANTI_FILTER_STACK_RECEIPT_PATH),
        "pool_coverage_receipt": rel(POOL_COVERAGE_RECEIPT_PATH),
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
        "source_handoff_triage": rel(SOURCE_HANDOFF_TRIAGE_PATH),
        "source_identity_audit": rel(SOURCE_IDENTITY_AUDIT_PATH),
        "source_aggressive_reentry": rel(SOURCE_AGGRESSIVE_REENTRY_PATH),
        "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
        "source_design_report": rel(SOURCE_DESIGN_REPORT_PATH),
        "source_previous_variant_manifest": rel(SOURCE_PREVIOUS_VARIANT_MANIFEST_PATH),
        "source_previous_attempt_manifest": rel(SOURCE_PREVIOUS_ATTEMPT_MANIFEST_PATH),
        "source_previous_runtime_contract": rel(SOURCE_PREVIOUS_RUNTIME_CONTRACT_PATH),
        "source_feature_manifest": rel(SOURCE_FEATURE_MANIFEST_PATH),
    }


def run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
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
        "availability": "tracked_report_plus_generated_ignored_artifacts",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267ES Runtime Gap Aware Tenth Follow-Up/Prune Materialization(267단계 267ES 런타임 공백 반영 10차 후속/가지치기 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- variants(변형): `{counts['variants']}`",
        f"- attempts(시도): `{counts['attempts']}`",
        f"- held_rows(보류 행): `{counts['held_rows']}`",
        f"- handoff_precheck_attempts(인계 사전검사 시도): `{counts['handoff_precheck_attempts']}`",
        f"- shared_state_attempts(공유 상태 시도): `{counts['shared_state_attempts']}`",
        f"- identity_attempts(정체성 감사 시도): `{counts['identity_attempts']}`",
        f"- aggressive_attempts(공격 시도): `{counts['aggressive_attempts']}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267ES(267ES 실행)는 run267ER(267ER 실행)의 설계를 MT5(MetaTrader 5, 메타트레이더5)가 실행할 수 있는 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.",
        "효과: blocked row(차단 행)는 handoff precheck(인계 사전검사)로 먼저 분리하고, 2026.04 weakness(약점)는 same-month filter(같은 월 필터)가 아니라 shared-state feature pivot(공유 상태 피처 전환)으로 물질화했다.",
        "효과: s262_lih와 s264_aia는 identity audit(정체성 감사)로 다시 묶었고, q04 validation watch(검증 관찰)는 단독 실행하지 않고 held(보류)로 남겼다.",
        "효과: aggressive non-filter(공격형 비필터) 시도 2개를 포함해 방어 필터만 쌓는 흐름을 피했다.",
        "",
        "## Queue Decision(대기열 판단)",
        "",
        "| queue_id(대기열 ID) | decision(판단) | variants(변형) | attempts(시도) | held(보류) |",
        "|---|---|---:|---:|---:|",
    ]
    for row in result["queue_decision"]:
        lines.append(f"| `{row['queue_id']}` | {row['decision']} | {row['variant_count']} | {row['attempt_count']} | {row['held_count']} |")
    lines.extend(
        [
            "",
            "## Attempts(시도)",
            "",
            "| attempt(시도) | candidate(후보) | queue(대기열) | role(역할) | dependency(의존성) |",
            "|---|---|---|---|---|",
        ]
    )
    for row in result["attempt_manifest"]:
        lines.append(
            f"| `{row['attempt_name']}` | `{row['candidate_alias']}` | `{row['queue_id']}` | `{row['attempt_role']}` | `{row.get('execution_dependency', 'none')}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "run267ES(267ES 실행)는 materialization(물질화)이다. 아직 MT5(MetaTrader 5, 메타트레이더5) 성능 결과, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)는 없다.",
            "따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- materialization_plan(물질화 계획): `{rel(MATERIALIZATION_PLAN_PATH)}`",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- preflight_handoff_receipt(사전 인계 영수증): `{rel(PREFLIGHT_RECEIPT_PATH)}`",
            f"- pool_coverage_receipt(후보군 커버리지 영수증): `{rel(POOL_COVERAGE_RECEIPT_PATH)}`",
            f"- runtime_parity_receipt(런타임 동등성 영수증): `{rel(RUNTIME_PARITY_RECEIPT_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    specs: list[tuple[str, str, Path, str]] = [
        ("stage267_run267ES_producer", "producer_script", PRODUCER_PATH, "Builds run267ES tenth follow-up/prune materialization."),
        ("stage267_run267ES_source_queue", "source_queue", SOURCE_QUEUE_PATH, "Source run267ER queue."),
        ("stage267_run267ES_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH, "Materialization plan."),
        ("stage267_run267ES_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Queue decision."),
        ("stage267_run267ES_feature_frame_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Feature frame manifest."),
        ("stage267_run267ES_model_manifest", "model_manifest", MODEL_MANIFEST_PATH, "Model manifest."),
        ("stage267_run267ES_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Variant manifest."),
        ("stage267_run267ES_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Attempt manifest."),
        ("stage267_run267ES_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract."),
        ("stage267_run267ES_held_queue", "held_queue", HELD_QUEUE_PATH, "Held queue."),
        ("stage267_run267ES_preflight_handoff", "preflight_handoff_receipt", PREFLIGHT_RECEIPT_PATH, "Preflight handoff receipt."),
        ("stage267_run267ES_anti_filter_stack", "anti_filter_stack_receipt", ANTI_FILTER_STACK_RECEIPT_PATH, "Anti filter-stack receipt."),
        ("stage267_run267ES_pool_coverage", "pool_coverage_receipt", POOL_COVERAGE_RECEIPT_PATH, "Pool coverage receipt."),
        ("stage267_run267ES_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267ES_environment", "environment_reproducibility_receipt", ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, "Environment receipt."),
        ("stage267_run267ES_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267ES_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267ES_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267ES_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267ES_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267ES_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267ES_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267ES_report", "review_report", REPORT_PATH, "User-facing report."),
    ]
    for row in result["variant_manifest"]:
        specs.append((f"stage267_run267ES_feature_{row['variant_id']}", "runtime_feature_frame", repo_path(row["runtime_feature_file"]), "Runtime feature copy."))
        specs.append((f"stage267_run267ES_model_{row['variant_id']}", "runtime_model_table", repo_path(row["runtime_model_file"]), "Runtime model copy."))
    for row in result["attempt_manifest"]:
        specs.append((f"stage267_run267ES_set_{row['attempt_name']}", "mt5_set", repo_path(row["set_path"]), "MT5 set file."))
        specs.append((f"stage267_run267ES_ini_{row['attempt_name']}", "mt5_ini", repo_path(row["ini_path"]), "MT5 tester ini file."))
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
    notes = f"variants={counts['variants']};attempts={counts['attempts']};held={counts['held_rows']};aggressive={counts['aggressive_attempts']};next_action={NEXT_ACTION}."
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_gap_aware_tenth_followup_or_prune_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    stage_row = {
        "row_id": "stage267_run267ES_runtime_gap_aware_tenth_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_tenth_followup_or_prune_materialization",
        "tier_scope": "Tier A materialized; q04 watch held",
        "scoreboard": "execution_pending_no_candidate_selection_no_onnx",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "feature_model_set_ini_handoff_materialized_no_mt5_kpi",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_tenth_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_tenth_followup_or_prune_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization",
        "tier_scope": "Tier A materialized; q04 watch held",
        "kpi_scope": "execution_pending_no_kpi",
        "scoreboard_lane": "runtime_gap_aware_materialization",
        "status": "out_of_scope_by_claim",
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={counts['variants']};attempts={counts['attempts']};aggressive={counts['aggressive_attempts']}",
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


def append_line_once(text: str, line: str) -> str:
    if line in text:
        return text
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def update_current_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267ES_runtime_gap_aware_tenth_followup_or_prune_materialization"
        f"(267EO 런타임 공백 반영 10차 후속/가지치기 물질화): `{rel(REPORT_PATH)}`"
    )
    summary_block = "\n".join(
        [
            "Run267ES(267ES 실행)는 run267ER(267ER 실행)의 queue(대기열)를 MT5(MetaTrader 5, 메타트레이더5) 실행 가능한 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 물질화했다.",
            f"Effect(효과): variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, handoff precheck attempts(인계 사전검사 시도) `{counts['handoff_precheck_attempts']}`개, aggressive attempts(공격 시도) `{counts['aggressive_attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_tenth_followup_or_prune_materialization`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_line_once(current, report_line)
    current = append_block_once(current, "Run267ES(267ES 실행)는 run267ER", summary_block)
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_line_once(selection, report_line)
    selection = append_block_once(selection, "Run267ES(267ES 실행)는 run267ER", summary_block)
    write_md(SELECTION_STATUS_PATH, selection)

    review_index = read_text(REVIEW_INDEX_PATH)
    review_index = replace_line_prefix(review_index, "- status(상태):", f"- status(상태): `{STATUS}`")
    review_index = replace_line_prefix(review_index, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(review_index, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(review_index, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    review_index = append_line_once(review_index, report_line)
    review_index = append_block_once(review_index, "Run267ES(267ES 실행)는 run267ER", summary_block)
    write_md(REVIEW_INDEX_PATH, review_index)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "current_focus:\n"
        "- >-\n"
        f"  Stage267(267단계) run267ES(267ES 실행) runtime gap aware tenth follow-up/prune materialization(런타임 공백 반영 10차 후속/가지치기 물질화) `{STATUS}`. "
        f"Effect(효과): variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, aggressive attempts(공격 시도) `{counts['aggressive_attempts']}`개를 만들었고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage267(267단계) run267ES(267ES 실행)" not in workspace:
        workspace = workspace.replace("current_focus:\n", focus, 1)
    workspace = workspace.replace(
        "  status: run267ER_runtime_gap_aware_tenth_followup_or_prune_design_completed",
        f"  status: {STATUS}",
    )
    workspace = workspace.replace(
        "  current_run_id: run267ER_stage267_runtime_gap_aware_tenth_followup_or_prune_design_v1",
        f"  current_run_id: {RUN_ID}",
    )
    workspace = workspace.replace(
        "  last_completed_run_id: run267ER_stage267_runtime_gap_aware_tenth_followup_or_prune_design_v1",
        f"  last_completed_run_id: {RUN_ID}",
    )
    workspace = workspace.replace(
        "  run267ER_runtime_gap_aware_tenth_followup_or_prune_design_report_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267ER_runtime_gap_aware_tenth_followup_or_prune_design.md\n  next_action: run267ES_materialize_runtime_gap_aware_tenth_followup_or_prune_queue",
        "  run267ER_runtime_gap_aware_tenth_followup_or_prune_design_report_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267ER_runtime_gap_aware_tenth_followup_or_prune_design.md\n"
        f"  run267ES_runtime_gap_aware_tenth_followup_or_prune_materialization_report_path: {rel(REPORT_PATH)}\n"
        f"  next_action: {NEXT_ACTION}",
    )
    workspace = append_block_once(workspace, "Run267ES(267ES 실행)는 run267ER", summary_block)
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
    write_csv(POOL_COVERAGE_RECEIPT_PATH, result["pool_coverage_receipt"])
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
    configure_template()
    required = [
        SOURCE_QUEUE_PATH,
        SOURCE_BRANCH_DECISION_PATH,
        SOURCE_PRUNE_MATRIX_PATH,
        SOURCE_FAILURE_MEMORY_PATH,
        SOURCE_HANDOFF_TRIAGE_PATH,
        SOURCE_IDENTITY_AUDIT_PATH,
        SOURCE_AGGRESSIVE_REENTRY_PATH,
        SOURCE_REVIEW_RESULT_PATH,
        SOURCE_PREVIOUS_VARIANT_MANIFEST_PATH,
        SOURCE_PREVIOUS_ATTEMPT_MANIFEST_PATH,
        SOURCE_PREVIOUS_RUNTIME_CONTRACT_PATH,
        SOURCE_FEATURE_MANIFEST_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))
    created_at = utc_now()
    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    variant_by_id = materializer_template.source_variant_rows()
    attempts = materializer_template.source_attempt_rows()
    canonical = materializer_template.canonical_source_rows()
    plan_rows = materializer_template.materialization_plan_rows(queue_rows)
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
    held = [{**row, "claim_boundary": CLAIM_BOUNDARY} for row in HELD_QUEUE_CONFIGS]
    anti_filter = anti_filter_stack_rows()
    queue_decisions = queue_decision_rows(queue_rows, variant_rows, attempt_rows, held)
    pool_coverage = pool_coverage_rows(variant_rows)
    held_queue_ids = {str(row["queue_id"]) for row in held}
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
        "pool_coverage_rows": len(pool_coverage),
        "candidate_aliases": ";".join(sorted({str(row["candidate_alias"]) for row in variant_rows})),
        "covered_candidate_aliases": len({str(row["candidate_alias"]) for row in variant_rows}),
        "handoff_precheck_attempts": sum(1 for row in attempt_rows if "handoff_precheck" in str(row["attempt_role"])),
        "shared_state_attempts": sum(1 for row in attempt_rows if str(row["queue_id"]) == "q02_202604_shared_sell_fragility_pivot"),
        "identity_attempts": sum(1 for row in attempt_rows if str(row["queue_id"]) == "q03_s262_s264_aia_signature_collapse_audit"),
        "aggressive_attempts": sum(1 for row in attempt_rows if str(row["queue_id"]) == "q05_aggressive_experiment_after_handoff_fix"),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    return {
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
        "sources": source_paths(),
        "outputs": output_paths(),
        "materialization_plan": plan_rows,
        "queue_decision": queue_decisions,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "runtime_contract": materializer_template.runtime_contract_rows(variant_rows),
        "held_queue": held,
        "preflight_handoff_receipt": preflight_rows,
        "anti_filter_stack_receipt": anti_filter,
        "pool_coverage_receipt": pool_coverage,
        "experiment_design_receipt": experiment_design_rows(queue_rows, held_queue_ids),
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
                "handoff_precheck_attempts": counts["handoff_precheck_attempts"],
                "shared_state_attempts": counts["shared_state_attempts"],
                "identity_attempts": counts["identity_attempts"],
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
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
