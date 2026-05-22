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
    run267EC_runtime_gap_aware_seventh_followup_or_prune_materialization as source_materialization,
)
from stage_pipelines.stage267 import (
    run267EF_runtime_gap_aware_eighth_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267EG"
RUN_ID = "run267EG_stage267_runtime_gap_aware_eighth_followup_or_prune_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_materialization.RUN_ID
STATUS = "run267EG_runtime_gap_aware_eighth_followup_or_prune_materialized_execution_pending"
JUDGMENT = "runtime_gap_aware_eighth_followup_or_prune_materialized_no_candidate_selection"
NEXT_ACTION = "run267EH_execute_runtime_gap_aware_eighth_followup_or_prune_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_eighth_followup_or_prune_materialization"
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
SOURCE_PREVIOUS_VARIANT_MANIFEST_PATH = source_materialization.VARIANT_MANIFEST_PATH
SOURCE_PREVIOUS_ATTEMPT_MANIFEST_PATH = source_materialization.ATTEMPT_MANIFEST_PATH
SOURCE_PREVIOUS_RUNTIME_CONTRACT_PATH = source_materialization.RUNTIME_CONTRACT_PATH
SOURCE_PREVIOUS_REPORT_PATH = source_materialization.REPORT_PATH
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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267EG_runtime_gap_aware_eighth_followup_or_prune_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267EG_runtime_gap_aware_eighth_followup_or_prune_materialization.py")

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

COMMON_ROOT = "OPV2/s267eg/run267EG_runtime_gap_aware_eighth_followup_or_prune"
EXPLORATION_LABEL = "stage267_BaselineRacing__RuntimeGapAwareEighthFollowupOrPrune"
MATERIALIZATION_BOUNDARY = "materialization_only_execution_pending_no_candidate_selection_no_selected_research_baseline_no_onnx"
TIER_PAIR_BOUNDARY = (
    "Tier A materialized for eighth follow-up/prune; true Tier B fallback and actual routed total remain unclaimed."
)


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
        queue_id="q01_s258_period_survival_quality_split",
        source_variant_id="run267ec_01_s258_stc_2025h1_period_survival_gate",
        variant_id="run267eg_01_s258_stc_2025h1_survival_quality_recheck",
        candidate_id="s258_short_tight_control",
        candidate_alias="s258_stc",
        candidate_role="stress_challenger",
        profile_label="s258_stc_2025h1_survival_quality_recheck",
        profile_token="s258_period_survival_quality",
        materialization_type="period_survival_quality_recheck",
        split="adjacent_2025_h1_validation_post_2024",
        period_label="2025H1",
        from_date="2025.01.02",
        to_date="2025.07.01",
        attempt_role="survival_quality_recheck_2025h1",
        priority="P0_survival_quality",
        targeted_weakness="2025H1 DD(drawdown, 손실폭) and trade quality(거래 품질) fragility without calendar exclusion(달력 제외 없음)",
        known_difference="Tightens risk and reentry quality to test whether s258_stc survives without hiding weak months.",
        set_updates={
            "InpShortThreshold": "0.545",
            "InpLongThreshold": "0.525",
            "InpAtrStopMultiplier": "1.70",
            "InpAtrTakeProfitMultiplier": "4.10",
            "InpModelRiskMaxPct": "0.021",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.016",
            "InpSameDirectionReentryCooldownBars": "6",
        },
    ),
    make_plan(
        queue_id="q01_s258_period_survival_quality_split",
        source_variant_id="run267ec_02_s258_stc_2025h2_period_survival_gate",
        variant_id="run267eg_02_s258_stc_2025h2_survival_quality_recheck",
        candidate_id="s258_short_tight_control",
        candidate_alias="s258_stc",
        candidate_role="stress_challenger",
        profile_label="s258_stc_2025h2_survival_quality_recheck",
        profile_token="s258_period_survival_quality",
        materialization_type="period_survival_quality_recheck",
        split="adjacent_2025_h2_oos_followthrough",
        period_label="2025H2",
        from_date="2025.07.01",
        to_date="2026.01.01",
        attempt_role="survival_quality_recheck_2025h2",
        priority="P0_survival_quality",
        targeted_weakness="2025H2 OOS(out-of-sample, 표본외) follow-through and DD(drawdown, 손실폭) fragility without weekday/month exclusion(요일/월 제외 없음)",
        known_difference="Keeps the same survival quality idea on a second period so a single pretty slice cannot drive the decision.",
        set_updates={
            "InpShortThreshold": "0.550",
            "InpLongThreshold": "0.530",
            "InpAtrStopMultiplier": "1.68",
            "InpAtrTakeProfitMultiplier": "4.05",
            "InpModelRiskMaxPct": "0.0205",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.017",
            "InpSameDirectionReentryCooldownBars": "6",
        },
    ),
    make_plan(
        queue_id="q02_s258_explosive_init_failure_triage",
        source_variant_id="run267ec_04_s258_stc_2025h1_explosive_impulse_supply",
        variant_id="run267eg_03_s258_stc_2025h1_explosive_handoff_triage",
        candidate_id="s258_short_tight_control",
        candidate_alias="s258_stc",
        candidate_role="stress_challenger",
        profile_label="s258_stc_2025h1_explosive_handoff_triage",
        profile_token="s258_explosive_init_triage",
        materialization_type="explosive_handoff_init_triage",
        split="adjacent_2025_h1_validation_post_2024",
        period_label="2025H1",
        from_date="2025.01.02",
        to_date="2025.07.01",
        attempt_role="explosive_handoff_triage_2025h1",
        priority="P0_aggressive_init_triage",
        targeted_weakness="run267ED init failure(초기화 실패) separation from performance failure(성능 실패)",
        known_difference="Re-materializes one aggressive s258_stc handoff so initialization can be separated from the trade result.",
        set_updates={
            "InpShortThreshold": "0.495",
            "InpLongThreshold": "0.475",
            "InpAtrStopMultiplier": "2.20",
            "InpAtrTakeProfitMultiplier": "5.05",
            "InpModelRiskMaxPct": "0.030",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.018",
            "InpSameDirectionReentryCooldownBars": "0",
        },
    ),
    make_plan(
        queue_id="q02_s258_explosive_init_failure_triage",
        source_variant_id="run267ec_05_s258_stc_2025h2_explosive_impulse_supply",
        variant_id="run267eg_04_s258_stc_2025h2_explosive_handoff_triage",
        candidate_id="s258_short_tight_control",
        candidate_alias="s258_stc",
        candidate_role="stress_challenger",
        profile_label="s258_stc_2025h2_explosive_handoff_triage",
        profile_token="s258_explosive_init_triage",
        materialization_type="explosive_handoff_init_triage",
        split="adjacent_2025_h2_oos_followthrough",
        period_label="2025H2",
        from_date="2025.07.01",
        to_date="2026.01.01",
        attempt_role="explosive_handoff_triage_2025h2",
        priority="P0_aggressive_init_triage",
        targeted_weakness="second-period init failure(초기화 실패) reproducibility for aggressive s258_stc",
        known_difference="Checks the same aggressive handoff on a second period before pruning the explosive s258 branch.",
        set_updates={
            "InpShortThreshold": "0.500",
            "InpLongThreshold": "0.480",
            "InpAtrStopMultiplier": "2.18",
            "InpAtrTakeProfitMultiplier": "5.00",
            "InpModelRiskMaxPct": "0.029",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.018",
            "InpSameDirectionReentryCooldownBars": "0",
        },
    ),
    make_plan(
        queue_id="q03_s264_aih_validation_final_month_bounded_repair",
        source_variant_id="run267ec_06_s264_aih_validation_anchor_integrity",
        variant_id="run267eg_05_s264_aih_validation_integrity_recheck",
        candidate_id="s264_allow_inner_high_quarter",
        candidate_alias="s264_aih",
        candidate_role="challenger_core",
        profile_label="s264_aih_validation_integrity_recheck",
        profile_token="s264_aih_bounded_repair",
        materialization_type="validation_integrity_before_bounded_repair",
        split="validation_is",
        period_label="validation_is",
        from_date="2025.01.02",
        to_date="2025.10.01",
        attempt_role="validation_integrity_recheck",
        priority="P0_repair_guard",
        targeted_weakness="validation(검증) late damage before any final-month bounded repair(마지막 월 제한 수리 전 손상 확인)",
        known_difference="Keeps validation integrity as the first read before a 2026.04 repair can be trusted.",
        set_updates={
            "InpShortThreshold": "0.540",
            "InpLongThreshold": "0.520",
            "InpAtrStopMultiplier": "1.95",
            "InpAtrTakeProfitMultiplier": "4.40",
            "InpModelRiskMaxPct": "0.024",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.012",
            "InpSameDirectionReentryCooldownBars": "3",
        },
    ),
    make_plan(
        queue_id="q03_s264_aih_validation_final_month_bounded_repair",
        source_variant_id="run267ec_07_s264_aih_202604_counter_shock_rebuild",
        variant_id="run267eg_06_s264_aih_202604_bounded_repair",
        candidate_id="s264_allow_inner_high_quarter",
        candidate_alias="s264_aih",
        candidate_role="challenger_core",
        profile_label="s264_aih_202604_bounded_repair",
        profile_token="s264_aih_bounded_repair",
        materialization_type="final_month_bounded_repair",
        split="oos_final_month_2026_04",
        period_label="2026.04",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="final_month_bounded_repair",
        priority="P0_repair_guard",
        targeted_weakness="2026.04 OOS(out-of-sample, 표본외) final-month loss without stretching repair loop(수리 루프 연장 없음)",
        known_difference="One bounded final-month repair check only; a third repair branch is not opened.",
        set_updates={
            "InpShortThreshold": "0.560",
            "InpLongThreshold": "0.540",
            "InpAtrStopMultiplier": "1.78",
            "InpAtrTakeProfitMultiplier": "4.10",
            "InpModelRiskMaxPct": "0.0215",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.024",
            "InpSameDirectionReentryCooldownBars": "4",
        },
    ),
    make_plan(
        queue_id="q03_s264_aih_validation_final_month_bounded_repair",
        source_variant_id="run267ec_08_s264_lc_202604_counter_shock_control",
        variant_id="run267eg_07_s264_lc_202604_paired_control",
        candidate_id="s264_lowrank_control",
        candidate_alias="s264_lc",
        candidate_role="defensive_control",
        profile_label="s264_lc_202604_paired_control",
        profile_token="s264_lc_bounded_control",
        materialization_type="paired_final_month_control",
        split="oos_final_month_2026_04",
        period_label="2026.04",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="paired_final_month_control",
        priority="P0_control",
        targeted_weakness="same-market control(같은 시장 대조) for s264_aih final-month repair",
        known_difference="Uses s264_lowrank_control as a defensive control, not as an operating baseline.",
        set_updates={
            "InpShortThreshold": "0.540",
            "InpLongThreshold": "0.520",
            "InpAtrStopMultiplier": "2.0325",
            "InpAtrTakeProfitMultiplier": "4.615",
            "InpModelRiskMaxPct": "0.0305",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "true",
            "InpSameDirectionReentryCooldownBars": "8",
        },
    ),
    make_plan(
        queue_id="q04_pool_202604_shared_sell_fragility_pressure",
        source_variant_id="run267ec_07_s264_aih_202604_counter_shock_rebuild",
        variant_id="run267eg_08_s264_aih_202604_shared_sell_pressure",
        candidate_id="s264_allow_inner_high_quarter",
        candidate_alias="s264_aih",
        candidate_role="challenger_core",
        profile_label="s264_aih_202604_shared_sell_pressure",
        profile_token="pool_202604_sell_fragility",
        materialization_type="shared_sell_fragility_pressure",
        split="oos_final_month_2026_04",
        period_label="2026.04",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="shared_sell_fragility_pressure",
        priority="P1_pool_pressure",
        targeted_weakness="shared 2026.04 sell-side fragility(공유 매도 취약성) across pool candidates",
        known_difference="Same pressure surface is applied across candidates to reveal who breaks less.",
        set_updates={
            "InpShortThreshold": "0.555",
            "InpLongThreshold": "0.535",
            "InpAtrStopMultiplier": "1.86",
            "InpAtrTakeProfitMultiplier": "4.20",
            "InpModelRiskMaxPct": "0.023",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.018",
            "InpSameDirectionReentryCooldownBars": "4",
        },
    ),
    make_plan(
        queue_id="q04_pool_202604_shared_sell_fragility_pressure",
        source_variant_id="run267ec_08_s264_lc_202604_counter_shock_control",
        variant_id="run267eg_09_s264_lc_202604_shared_sell_pressure",
        candidate_id="s264_lowrank_control",
        candidate_alias="s264_lc",
        candidate_role="defensive_control",
        profile_label="s264_lc_202604_shared_sell_pressure",
        profile_token="pool_202604_sell_fragility",
        materialization_type="shared_sell_fragility_pressure",
        split="oos_final_month_2026_04",
        period_label="2026.04",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="shared_sell_fragility_pressure",
        priority="P1_pool_pressure",
        targeted_weakness="defensive control(방어 대조) response to shared 2026.04 sell-side fragility",
        known_difference="Keeps the lowrank control in the same final-month pressure surface.",
        set_updates={
            "InpShortThreshold": "0.550",
            "InpLongThreshold": "0.530",
            "InpAtrStopMultiplier": "1.90",
            "InpAtrTakeProfitMultiplier": "4.25",
            "InpModelRiskMaxPct": "0.024",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.016",
            "InpSameDirectionReentryCooldownBars": "5",
        },
    ),
    make_plan(
        queue_id="q04_pool_202604_shared_sell_fragility_pressure",
        source_variant_id="run267ec_12_s262_lih_202604_coverage_rejoin",
        variant_id="run267eg_10_s262_lih_202604_shared_sell_pressure",
        candidate_id="s262_lowrank_inner_half_filter",
        candidate_alias="s262_lih",
        candidate_role="validation_heavy",
        profile_label="s262_lih_202604_shared_sell_pressure",
        profile_token="pool_202604_sell_fragility",
        materialization_type="shared_sell_fragility_pressure",
        split="oos_final_month_2026_04",
        period_label="2026.04",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="shared_sell_fragility_pressure",
        priority="P1_pool_pressure",
        targeted_weakness="validation-heavy(검증 중심) candidate response to shared final-month fragility",
        known_difference="Checks whether validation-heavy structure breaks less on the same OOS final-month slice.",
        set_updates={
            "InpShortThreshold": "0.550",
            "InpLongThreshold": "0.530",
            "InpAtrStopMultiplier": "1.88",
            "InpAtrTakeProfitMultiplier": "4.20",
            "InpModelRiskMaxPct": "0.023",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.016",
            "InpSameDirectionReentryCooldownBars": "5",
        },
    ),
    make_plan(
        queue_id="q04_pool_202604_shared_sell_fragility_pressure",
        source_variant_id="run267ec_14_s264_aia_202604_coverage_rejoin",
        variant_id="run267eg_11_s264_aia_202604_shared_sell_pressure",
        candidate_id="s264_allow_inner_all_oos_anchor",
        candidate_alias="s264_aia",
        candidate_role="oos_anchor",
        profile_label="s264_aia_202604_shared_sell_pressure",
        profile_token="pool_202604_sell_fragility",
        materialization_type="shared_sell_fragility_pressure",
        split="oos_final_month_2026_04",
        period_label="2026.04",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="shared_sell_fragility_pressure",
        priority="P1_pool_pressure",
        targeted_weakness="OOS anchor(표본외 앵커) response to shared final-month fragility",
        known_difference="Checks whether OOS anchor recovery survives the same shared pressure.",
        set_updates={
            "InpShortThreshold": "0.555",
            "InpLongThreshold": "0.535",
            "InpAtrStopMultiplier": "1.86",
            "InpAtrTakeProfitMultiplier": "4.20",
            "InpModelRiskMaxPct": "0.023",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.016",
            "InpSameDirectionReentryCooldownBars": "5",
        },
    ),
    make_plan(
        queue_id="q05_s262_s264_aia_identity_and_feature_order_audit",
        source_variant_id="run267ec_11_s262_lih_validation_coverage_rejoin",
        variant_id="run267eg_12_s262_lih_validation_identity_audit",
        candidate_id="s262_lowrank_inner_half_filter",
        candidate_alias="s262_lih",
        candidate_role="validation_heavy",
        profile_label="s262_lih_validation_identity_audit",
        profile_token="identity_feature_order_audit",
        materialization_type="identity_feature_order_audit",
        split="validation_is",
        period_label="validation_is",
        from_date="2025.01.02",
        to_date="2025.10.01",
        attempt_role="identity_feature_order_audit_validation",
        priority="P1_identity_audit",
        targeted_weakness="feature order(피처 순서) and candidate identity(후보 정체성) drift risk before any comparison",
        known_difference="Preserves the previous settings so feature/model identity can be audited cleanly.",
        set_updates={},
    ),
    make_plan(
        queue_id="q05_s262_s264_aia_identity_and_feature_order_audit",
        source_variant_id="run267ec_13_s264_aia_validation_coverage_rejoin",
        variant_id="run267eg_13_s264_aia_validation_identity_audit",
        candidate_id="s264_allow_inner_all_oos_anchor",
        candidate_alias="s264_aia",
        candidate_role="oos_anchor",
        profile_label="s264_aia_validation_identity_audit",
        profile_token="identity_feature_order_audit",
        materialization_type="identity_feature_order_audit",
        split="validation_is",
        period_label="validation_is",
        from_date="2025.01.02",
        to_date="2025.10.01",
        attempt_role="identity_feature_order_audit_validation",
        priority="P1_identity_audit",
        targeted_weakness="feature order(피처 순서) and OOS anchor(표본외 앵커) identity drift risk before any comparison",
        known_difference="Preserves the previous settings so feature/model identity can be audited cleanly.",
        set_updates={},
    ),
    make_plan(
        queue_id="q06_s264_aih_explosive_counter_impulse_handoff_triage",
        source_variant_id="run267ec_09_s264_aih_validation_explosive_counter_impulse",
        variant_id="run267eg_14_s264_aih_validation_explosive_handoff_triage",
        candidate_id="s264_allow_inner_high_quarter",
        candidate_alias="s264_aih",
        candidate_role="challenger_core",
        profile_label="s264_aih_validation_explosive_handoff_triage",
        profile_token="s264_aih_explosive_handoff_triage",
        materialization_type="explosive_counter_impulse_handoff_triage",
        split="validation_is",
        period_label="validation_is",
        from_date="2025.01.02",
        to_date="2025.10.01",
        attempt_role="validation_explosive_handoff_triage",
        priority="P1_aggressive_handoff_triage",
        targeted_weakness="s264_aih aggressive handoff(공격형 인계) init/runtime split before judging damage",
        known_difference="Separates handoff validity from validation performance for the aggressive counter-impulse branch.",
        set_updates={
            "InpShortThreshold": "0.500",
            "InpLongThreshold": "0.480",
            "InpAtrStopMultiplier": "2.10",
            "InpAtrTakeProfitMultiplier": "4.85",
            "InpModelRiskMaxPct": "0.029",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.018",
            "InpSameDirectionReentryCooldownBars": "0",
        },
    ),
    make_plan(
        queue_id="q06_s264_aih_explosive_counter_impulse_handoff_triage",
        source_variant_id="run267ec_10_s264_aih_202604_explosive_counter_impulse",
        variant_id="run267eg_15_s264_aih_202604_explosive_handoff_triage",
        candidate_id="s264_allow_inner_high_quarter",
        candidate_alias="s264_aih",
        candidate_role="challenger_core",
        profile_label="s264_aih_202604_explosive_handoff_triage",
        profile_token="s264_aih_explosive_handoff_triage",
        materialization_type="explosive_counter_impulse_handoff_triage",
        split="oos_final_month_2026_04",
        period_label="2026.04",
        from_date="2026.04.01",
        to_date="2026.04.14",
        attempt_role="final_month_explosive_handoff_triage",
        priority="P1_aggressive_handoff_triage",
        targeted_weakness="s264_aih aggressive final-month handoff(마지막 월 인계) before pruning or repairing",
        known_difference="Runs one final-month aggressive handoff check without turning it into a same-month rescue branch.",
        set_updates={
            "InpShortThreshold": "0.500",
            "InpLongThreshold": "0.480",
            "InpAtrStopMultiplier": "2.08",
            "InpAtrTakeProfitMultiplier": "4.80",
            "InpModelRiskMaxPct": "0.028",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.018",
            "InpSameDirectionReentryCooldownBars": "0",
        },
    ),
)

HELD_QUEUE_CONFIGS: tuple[dict[str, str], ...] = (
    {
        "queue_id": "q07_pool_prune_guard_and_next_pivot_receipt",
        "priority": "P2_prune_guard",
        "candidate_aliases": "pool",
        "decision": "held_guardrail_only_no_standalone_mt5(가드레일 보류, 단독 MT5 없음)",
        "why": "No candidate(후보) is pruned by a single metric(단일 지표), single month(단일 월), or single feature(단일 피처).",
        "reopen_condition": "Reopen only after run267EH execution(실행) and balance/equity(잔액/평가금) plus time-slice(시간 구간) review identify a structural pivot.",
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


def rewrite_set_header(attempt: dict[str, Any]) -> dict[str, Any]:
    path = repo_path(str(attempt["set_path"]))
    text = io_path(path).read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if lines and lines[0].startswith("; generated_by="):
        lines[0] = "; generated_by=run267EG_runtime_gap_aware_eighth_followup_or_prune_materialization"
        io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
        attempt["set_sha256"] = sha256_file_lf_normalized(path)
    return attempt


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
    attempt = rewrite_set_header(attempt)
    preflight["set_sha256"] = attempt["set_sha256"]
    preflight["effect"] = (
        "Common Files(공통 파일) handoff(인계)를 먼저 고정한다. "
        "효과는 init failure(초기화 실패)와 성능 실패를 분리해 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 해석 오류를 줄이는 것이다."
    )
    return variant, feature, model, attempt, preflight


def anti_filter_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267eg_q07_prune_guard",
            "queue_id": "q07_pool_prune_guard_and_next_pivot_receipt",
            "status": "enforced",
            "forbidden_pattern": "single_metric_prune;single_month_prune;single_feature_prune;calendar_only_filter_stack",
            "materialized_standalone": "false",
            "effect": "후보를 한 지표나 한 달만 보고 버리지 않는다. 효과는 과한 미세 조정 루프를 막고 구조적 비교를 유지하는 것이다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def pool_coverage_rows(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    candidate_roles = {
        "s264_aih": "challenger_core",
        "s264_lc": "defensive_control",
        "s262_lih": "validation_heavy",
        "s264_aia": "oos_anchor",
        "s258_stc": "stress_challenger",
    }
    rows: list[dict[str, Any]] = []
    for alias, role in candidate_roles.items():
        alias_rows = [row for row in variant_rows if row["candidate_alias"] == alias]
        rows.append(
            {
                "receipt_id": f"run267eg_{alias}_candidate_pool_coverage",
                "candidate_alias": alias,
                "candidate_role": role,
                "variant_count": len(alias_rows),
                "queue_ids": ";".join(sorted({str(row["queue_id"]) for row in alias_rows})),
                "splits": ";".join(sorted({str(row["split"]) for row in alias_rows})),
                "status": "materialized" if alias_rows else "missing_required",
                "effect": "다섯 후보군을 같은 follow-up(후속) 패키지 안에 유지한다. 효과는 좋은 숫자 하나보다 덜 깨지는 후보를 찾는 것이다.",
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
                "materialization_status": "held_guardrail_only" if queue_id in held_queue_ids else "materialized",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def environment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267eg_common_files_handoff",
            "status": "prepared",
            "evidence": f"variants={counts['variants']};attempts={counts['attempts']};held={counts['held_rows']}",
            "effect": "feature/model/set/ini(피처/모델/설정/초기화) 파일을 Common Files(공통 파일) 인계 경로와 연결했다. 효과는 다음 MT5(MetaTrader 5, 메타트레이더5) 실행 입력을 재현 가능하게 만드는 것이다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": f"run267eg_data_{row['variant_id']}",
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
            "effect": "Python(파이썬) 연구 입력과 MT5(MetaTrader 5, 메타트레이더5) 입력의 feature order(피처 순서)를 추적한다. 효과는 실행 뒤 parity(동등성) 문제를 분리하기 쉬워지는 것이다.",
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
            "user_explanation_hook": "이번 작업은 후보를 고른 것이 아니라 다음 MT5 실행 입력을 만든 것이다. 효과는 이제 같은 큐를 실행해 덜 깨지는 후보를 비교할 수 있다는 점이다.",
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "gate267eg_source_inputs",
            "gate_name": "source inputs present(원천 입력 존재)",
            "status": "pass",
            "evidence": f"{rel(SOURCE_QUEUE_PATH)};{rel(SOURCE_PREVIOUS_VARIANT_MANIFEST_PATH)};{rel(SOURCE_FEATURE_MANIFEST_PATH)}",
            "effect": "run267EF 설계와 run267EC 물질화 산출물을 함께 사용한다. 효과는 이전 연구를 다음 실행 입력으로 실제 연결하는 것이다.",
        },
        {
            "gate_id": "gate267eg_materialization_count",
            "gate_name": "materialization count(물질화 개수)",
            "status": "pass" if counts["variants"] == len(PLAN_CONFIGS) and counts["attempts"] == len(PLAN_CONFIGS) else "fail",
            "evidence": f"variants={counts['variants']};attempts={counts['attempts']};expected={len(PLAN_CONFIGS)}",
            "effect": "다음 run267EH 실행 가능한 set/ini(설정/초기화) 묶음을 만들었다.",
        },
        {
            "gate_id": "gate267eg_candidate_pool_coverage",
            "gate_name": "candidate pool coverage(후보군 커버리지)",
            "status": "pass" if counts["covered_candidate_aliases"] == 5 else "fail",
            "evidence": f"covered_candidate_aliases={counts['covered_candidate_aliases']};aliases={counts['candidate_aliases']}",
            "effect": "다섯 baseline candidate(기준 후보)를 같은 물질화 패키지에 남긴다.",
        },
        {
            "gate_id": "gate267eg_survival_and_init_triage",
            "gate_name": "survival plus init triage(생존성 및 초기화 분리)",
            "status": "pass" if counts["survival_attempts"] >= 2 and counts["init_triage_attempts"] >= 2 else "fail",
            "evidence": f"survival_attempts={counts['survival_attempts']};init_triage_attempts={counts['init_triage_attempts']}",
            "effect": "s258_stc를 숫자만 보고 버리지 않고 생존성/초기화 문제를 분리한다.",
        },
        {
            "gate_id": "gate267eg_shared_pressure_and_identity",
            "gate_name": "shared pressure plus identity audit(공유 압박 및 정체성 감사)",
            "status": "pass" if counts["shared_pressure_attempts"] >= 4 and counts["identity_attempts"] >= 2 else "fail",
            "evidence": f"shared_pressure_attempts={counts['shared_pressure_attempts']};identity_attempts={counts['identity_attempts']}",
            "effect": "한 후보만 수리하지 않고 같은 약점 표면과 feature order(피처 순서)를 함께 검토한다.",
        },
        {
            "gate_id": "gate267eg_aggressive_required",
            "gate_name": "aggressive rows preserved(공격 행 보존)",
            "status": "pass" if counts["aggressive_attempts"] >= 2 else "fail",
            "evidence": f"aggressive_attempts={counts['aggressive_attempts']}",
            "effect": "방어적 필터만 반복하지 않고 공격형 handoff(인계)도 분리 검증한다.",
        },
        {
            "gate_id": "gate267eg_prune_guard",
            "gate_name": "prune guard held(가지치기 보류)",
            "status": "pass" if counts["held_rows"] >= 1 else "fail",
            "evidence": f"held_rows={counts['held_rows']};held_queue=q07_pool_prune_guard_and_next_pivot_receipt",
            "effect": "단일 지표/월/피처로 후보를 조기 제거하지 않는다.",
        },
        {
            "gate_id": "gate267eg_claim_guard",
            "gate_name": "claim guard(주장 경계)",
            "status": "pass",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx=not_claimed;goal=not_claimed",
            "effect": "물질화를 성능 판정이나 ONNX(온엑스) 준비로 오해하지 않게 한다.",
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
        "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
        "source_design_report": rel(SOURCE_DESIGN_REPORT_PATH),
        "source_previous_variant_manifest": rel(SOURCE_PREVIOUS_VARIANT_MANIFEST_PATH),
        "source_previous_attempt_manifest": rel(SOURCE_PREVIOUS_ATTEMPT_MANIFEST_PATH),
        "source_previous_runtime_contract": rel(SOURCE_PREVIOUS_RUNTIME_CONTRACT_PATH),
        "source_feature_manifest": rel(SOURCE_FEATURE_MANIFEST_PATH),
    }


def run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": result["created_at_utc"],
        "next_action": NEXT_ACTION,
        "counts": result["counts"],
        "sources": source_paths(),
        "outputs": output_paths(),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def lineage(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_lineage_id": "stage267_run267EG_runtime_gap_aware_eighth_followup_or_prune_materialization",
        "producer": rel(PRODUCER_PATH),
        "created_at_utc": result["created_at_utc"],
        "inputs": source_paths(),
        "outputs": output_paths(),
        "materialized_variants": [row["variant_id"] for row in result["variant_manifest"]],
        "held_queues": [row["queue_id"] for row in result["held_queue"]],
        "consumer": NEXT_ACTION,
        "boundary": "Materialization only; no MT5 KPI, candidate selection, selected research baseline, ONNX readiness, or Goal Achieve claim.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267EG Runtime Gap Aware Eighth Follow-Up/Prune Materialization(267단계 267EG 런타임 공백 반영 8차 후속/가지치기 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- source_materialization(원천 물질화): `{SOURCE_MATERIALIZATION_RUN_ID}`",
        f"- variants(변형): `{counts['variants']}`",
        f"- attempts(시도): `{counts['attempts']}`",
        f"- held_rows(보류 행): `{counts['held_rows']}`",
        f"- covered_candidates(커버된 후보): `{counts['covered_candidate_aliases']}/5`",
        f"- aggressive_attempts(공격형 시도): `{counts['aggressive_attempts']}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267EG(267EG 실행)는 후보를 뽑은 것이 아니다. run267EF(267EF 실행)의 materialization queue(물질화 대기열)를 MT5(MetaTrader 5, 메타트레이더5)가 실행할 수 있는 입력으로 바꾼 단계다.",
        "효과는 다음 run267EH(267EH 실행)에서 s258_stc 생존성, s264_aih 제한 수리, 2026.04 공유 매도 취약성, s262/s264_aia feature order(피처 순서), 공격형 handoff(인계)를 같은 묶음으로 검증할 수 있다는 것이다.",
        "",
        "baseline candidate(기준 후보) 정리가 오래 걸리는 이유는 숫자 1등을 뽑는 일이 아니기 때문이다. 각 후보가 여러 기간, 약한 구간, feature/order(피처/순서), runtime handoff(런타임 인계)에서 덜 깨지는지 확인해야 한다.",
        "",
        "## Queue Decision(대기열 판단)",
        "",
        "| queue_id(대기열 ID) | decision(판단) | variants(변형) | attempts(시도) | held(보류) |",
        "|---|---|---:|---:|---:|",
    ]
    for row in result["queue_decision"]:
        lines.append(
            f"| `{row['queue_id']}` | {row['decision']} | {row['variant_count']} | {row['attempt_count']} | {row['held_count']} |"
        )
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
            "run267EG(267EG 실행)는 materialization(물질화)이다. 아직 MT5(MetaTrader 5, 메타트레이더5) 성능 결과, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)는 없다.",
            "따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- materialization_plan(물질화 계획): `{rel(MATERIALIZATION_PLAN_PATH)}`",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- preflight_handoff_receipt(사전 인계 영수증): `{rel(PREFLIGHT_RECEIPT_PATH)}`",
            f"- pool_coverage_receipt(후보군 커버리지 영수증): `{rel(POOL_COVERAGE_RECEIPT_PATH)}`",
            f"- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    specs: list[tuple[str, str, Path, str]] = [
        ("stage267_run267EG_producer", "producer_script", PRODUCER_PATH, "Builds run267EG eighth follow-up/prune materialization."),
        ("stage267_run267EG_source_queue", "source_queue", SOURCE_QUEUE_PATH, "Source run267EF queue."),
        ("stage267_run267EG_source_feature_blueprint", "source_feature_blueprint", SOURCE_FEATURE_BLUEPRINT_PATH, "Source run267EF feature blueprint."),
        ("stage267_run267EG_source_branch_decision", "source_branch_decision", SOURCE_BRANCH_DECISION_PATH, "Source run267EF branch decisions."),
        ("stage267_run267EG_source_prune_matrix", "source_prune_matrix", SOURCE_PRUNE_MATRIX_PATH, "Source run267EF prune matrix."),
        ("stage267_run267EG_source_previous_variant_manifest", "source_variant_manifest", SOURCE_PREVIOUS_VARIANT_MANIFEST_PATH, "Source run267EC variant manifest."),
        ("stage267_run267EG_source_previous_attempt_manifest", "source_attempt_manifest", SOURCE_PREVIOUS_ATTEMPT_MANIFEST_PATH, "Source run267EC attempt manifest."),
        ("stage267_run267EG_source_feature_manifest", "source_feature_manifest", SOURCE_FEATURE_MANIFEST_PATH, "Canonical pool source feature manifest."),
        ("stage267_run267EG_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH, "Materialization plan."),
        ("stage267_run267EG_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Queue decision."),
        ("stage267_run267EG_feature_frame_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Feature frame manifest."),
        ("stage267_run267EG_model_manifest", "model_manifest", MODEL_MANIFEST_PATH, "Model manifest."),
        ("stage267_run267EG_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Variant manifest."),
        ("stage267_run267EG_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Attempt manifest."),
        ("stage267_run267EG_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract."),
        ("stage267_run267EG_held_queue", "held_queue", HELD_QUEUE_PATH, "Held queue."),
        ("stage267_run267EG_preflight_handoff", "preflight_handoff_receipt", PREFLIGHT_RECEIPT_PATH, "Preflight handoff receipt."),
        ("stage267_run267EG_anti_filter_stack", "anti_filter_stack_receipt", ANTI_FILTER_STACK_RECEIPT_PATH, "Anti filter-stack receipt."),
        ("stage267_run267EG_pool_coverage", "pool_coverage_receipt", POOL_COVERAGE_RECEIPT_PATH, "Pool coverage receipt."),
        ("stage267_run267EG_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267EG_environment", "environment_reproducibility_receipt", ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, "Environment receipt."),
        ("stage267_run267EG_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267EG_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267EG_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267EG_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267EG_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267EG_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267EG_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267EG_report", "review_report", REPORT_PATH, "User-facing report."),
    ]
    for row in result["variant_manifest"]:
        specs.append(
            (
                f"stage267_run267EG_feature_{row['variant_id']}",
                "runtime_feature_frame",
                repo_path(row["runtime_feature_file"]),
                "Runtime feature copy.",
            )
        )
        specs.append(
            (
                f"stage267_run267EG_model_{row['variant_id']}",
                "runtime_model_table",
                repo_path(row["runtime_model_file"]),
                "Runtime model copy.",
            )
        )
    for row in result["attempt_manifest"]:
        specs.append((f"stage267_run267EG_set_{row['attempt_name']}", "mt5_set", repo_path(row["set_path"]), "MT5 set file."))
        specs.append((f"stage267_run267EG_ini_{row['attempt_name']}", "mt5_ini", repo_path(row["ini_path"]), "MT5 tester ini file."))

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
        "lane": "runtime_gap_aware_eighth_followup_or_prune_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    stage_row = {
        "row_id": "stage267_run267EG_runtime_gap_aware_eighth_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_eighth_followup_or_prune_materialization",
        "tier_scope": "Tier A materialized; q07 guardrail held; five-candidate pool covered",
        "scoreboard": "execution_pending_no_candidate_selection_no_onnx",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "feature_model_set_ini_handoff_materialized_no_mt5_kpi",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_eighth_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_eighth_followup_or_prune_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization",
        "tier_scope": "Tier A materialized; q07 guardrail held; five-candidate pool covered",
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


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_line_containing(text: str, needle: str, replacement: str) -> str:
    return "\n".join(replacement if needle in line else line for line in text.splitlines()) + "\n"


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


def replace_stage267_field(text: str, field: str, replacement: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index("stage267_baseline_candidate_racing_protocol:")
    except ValueError:
        return text
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index] and not lines[index].startswith(" "):
            end = index
            break
    prefix = f"  {field}:"
    for index in range(start + 1, end):
        if lines[index].startswith(prefix):
            lines[index] = f"  {field}: {replacement}"
            return "\n".join(lines) + "\n"
    lines.insert(end, f"  {field}: {replacement}")
    return "\n".join(lines) + "\n"


def insert_stage267_report_path(text: str) -> str:
    line = f"  run267EG_runtime_gap_aware_eighth_followup_or_prune_materialization_report_path: {rel(REPORT_PATH)}"
    if line in text:
        return text
    lines = text.splitlines()
    try:
        start = lines.index("stage267_baseline_candidate_racing_protocol:")
    except ValueError:
        return text
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index] and not lines[index].startswith(" "):
            end = index
            break
    for index in range(start + 1, end):
        if lines[index].startswith("  next_action:"):
            lines.insert(index, line)
            return "\n".join(lines) + "\n"
    lines.insert(end, line)
    return "\n".join(lines) + "\n"


def update_current_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267EG_runtime_gap_aware_eighth_followup_or_prune_materialization"
        f"(267EG 런타임 공백 반영 8차 후속/가지치기 물질화): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267EG(267EG 실행)는 run267EF(267EF 실행)의 materialization queue(물질화 대기열)를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.",
            f"Effect(효과): variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개, covered candidates(커버된 후보) `{counts['covered_candidate_aliases']}/5`, aggressive attempts(공격형 시도) `{counts['aggressive_attempts']}`개를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(
        current,
        "- adapter_under_review(검토 중 어댑터):",
        "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_eighth_followup_or_prune_materialization`",
    )
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_after_contains(current, "run267EF_runtime_gap_aware_eighth_followup_or_prune_design", report_line)
    current = replace_line_prefix(
        current,
        "- latest_materialization(최신 물질화):",
        f"- latest_materialization(최신 물질화): run267EG(267EG 실행) variants(변형) `{counts['variants']}`, "
        f"attempts(시도) `{counts['attempts']}`, held_rows(보류 행) `{counts['held_rows']}`, "
        f"covered_candidates(커버된 후보) `{counts['covered_candidate_aliases']}/5`, "
        f"aggressive_attempts(공격형 시도) `{counts['aggressive_attempts']}`, report(보고서) `{rel(REPORT_PATH)}`.",
    )
    current = append_block_once(current, "Run267EG(267EG 실행)는 run267EF", block)
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_after_contains(selection, "run267EF_runtime_gap_aware_eighth_followup_or_prune_design", report_line)
    selection = append_block_once(selection, "Run267EG(267EG 실행)는 run267EF", block)
    write_md(SELECTION_STATUS_PATH, selection)

    review_index = read_text(REVIEW_INDEX_PATH)
    review_index = replace_line_containing(review_index, "- status(", f"- status(상태): `{STATUS}`")
    review_index = replace_line_containing(review_index, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_containing(review_index, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review_index = append_after_contains(review_index, "run267EF_runtime_gap_aware_eighth_followup_or_prune_design", report_line)
    review_index = append_block_once(review_index, "Run267EG(267EG 실행)는 run267EF", block)
    write_md(REVIEW_INDEX_PATH, review_index)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        "  Stage267(267단계) run267EG(267EG 실행) runtime gap aware eighth follow-up/prune materialization"
        f"(런타임 공백 반영 8차 후속/가지치기 물질화) `{STATUS}`. "
        f"Effect(효과): run267EF(267EF 실행)의 queue(대기열)를 variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, "
        f"held rows(보류 행) `{counts['held_rows']}`개로 바꿨고, selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), "
        "ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    workspace = replace_stage267_field(workspace, "status", STATUS)
    workspace = replace_stage267_field(workspace, "current_run_id", RUN_ID)
    workspace = replace_stage267_field(workspace, "last_completed_run_id", RUN_ID)
    workspace = insert_stage267_report_path(workspace)
    workspace = replace_stage267_field(workspace, "next_action", NEXT_ACTION)
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
        SOURCE_FEATURE_BLUEPRINT_PATH,
        SOURCE_BRANCH_DECISION_PATH,
        SOURCE_PRUNE_MATRIX_PATH,
        SOURCE_FAILURE_MEMORY_PATH,
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
    source_attempts = materializer_template.source_attempt_rows()
    canonical = materializer_template.canonical_source_rows()
    materialization_plan = materializer_template.materialization_plan_rows(queue_rows)

    variant_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    preflight_rows: list[dict[str, Any]] = []
    for index, plan in enumerate(PLAN_CONFIGS, start=1):
        variant, feature, model, attempt, preflight = materialize_plan(plan, variant_by_id, source_attempts, canonical, index)
        variant_rows.append(variant)
        feature_rows.append(feature)
        model_rows.append(model)
        attempt_rows.append(attempt)
        preflight_rows.append(preflight)

    held = materializer_template.held_queue_rows()
    held_ids = {str(row["queue_id"]) for row in held}
    anti_filter = anti_filter_stack_rows()
    coverage_receipt = pool_coverage_rows(variant_rows)
    queue_decisions = materializer_template.queue_decision_rows(queue_rows, variant_rows, attempt_rows, held)
    candidate_aliases = sorted({str(row["candidate_alias"]) for row in variant_rows})
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
        "pool_coverage_receipts": len(coverage_receipt),
        "aggressive_attempts": sum(1 for row in attempt_rows if "aggressive" in str(row["priority"]).lower()),
        "survival_attempts": sum(1 for row in attempt_rows if "survival" in str(row["priority"]).lower()),
        "init_triage_attempts": sum(1 for row in attempt_rows if "init_triage" in str(row["priority"]).lower()),
        "repair_attempts": sum(1 for row in attempt_rows if "repair" in str(row["priority"]).lower()),
        "control_attempts": sum(1 for row in attempt_rows if "control" in str(row["priority"]).lower()),
        "shared_pressure_attempts": sum(1 for row in attempt_rows if row["queue_id"] == "q04_pool_202604_shared_sell_fragility_pressure"),
        "identity_attempts": sum(1 for row in attempt_rows if row["queue_id"] == "q05_s262_s264_aia_identity_and_feature_order_audit"),
        "covered_candidate_aliases": len(candidate_aliases),
        "candidate_aliases": ";".join(candidate_aliases),
        "s258_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s258_stc"),
        "s264_aih_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s264_aih"),
        "s264_lc_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s264_lc"),
        "s262_lih_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s262_lih"),
        "s264_aia_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s264_aia"),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    result = {
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
        "materialization_plan": materialization_plan,
        "queue_decision": queue_decisions,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "runtime_contract": materializer_template.runtime_contract_rows(variant_rows),
        "held_queue": held,
        "preflight_handoff_receipt": preflight_rows,
        "anti_filter_stack_receipt": anti_filter,
        "pool_coverage_receipt": coverage_receipt,
        "experiment_design_receipt": experiment_design_rows(queue_rows, held_ids),
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
        f"{RUN_ID}: variants={counts['variants']} attempts={counts['attempts']} "
        f"held={counts['held_rows']} next_action={NEXT_ACTION}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
