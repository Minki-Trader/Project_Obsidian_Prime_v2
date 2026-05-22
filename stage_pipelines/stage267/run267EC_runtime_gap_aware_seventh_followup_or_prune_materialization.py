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
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import (
    run267DY_runtime_gap_aware_sixth_followup_or_prune_materialization as materializer_template,
)
from stage_pipelines.stage267 import (
    run267EB_runtime_gap_aware_seventh_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267EC"
RUN_ID = "run267EC_stage267_runtime_gap_aware_seventh_followup_or_prune_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = materializer_template.RUN_ID
STATUS = "run267EC_runtime_gap_aware_seventh_followup_or_prune_materialized_execution_pending"
JUDGMENT = "runtime_gap_aware_seventh_followup_or_prune_materialized_no_candidate_selection"
NEXT_ACTION = "run267ED_execute_runtime_gap_aware_seventh_followup_or_prune_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_seventh_followup_or_prune_materialization"
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

SOURCE_DY_VARIANT_MANIFEST_PATH = materializer_template.VARIANT_MANIFEST_PATH
SOURCE_DY_ATTEMPT_MANIFEST_PATH = materializer_template.ATTEMPT_MANIFEST_PATH
SOURCE_DY_RUNTIME_CONTRACT_PATH = materializer_template.RUNTIME_CONTRACT_PATH
SOURCE_DY_REPORT_PATH = materializer_template.REPORT_PATH
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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267EC_runtime_gap_aware_seventh_followup_or_prune_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267EC_runtime_gap_aware_seventh_followup_or_prune_materialization.py")

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

COMMON_ROOT = "OPV2/s267ec/run267EC_runtime_gap_aware_seventh_followup_or_prune"
EXPLORATION_LABEL = "stage267_BaselineRacing__RuntimeGapAwareSeventhFollowupOrPrune"
MATERIALIZATION_BOUNDARY = "materialization_only_execution_pending_no_candidate_selection_no_selected_research_baseline_no_onnx"
TIER_PAIR_BOUNDARY = (
    "Tier A materialized for seventh follow-up/prune; true Tier B fallback and actual routed total remain unclaimed."
)

PLAN_CONFIGS: tuple[dict[str, Any], ...] = (
    {
        "queue_id": "q01_s258_2025h1_period_survival_gate",
        "source_kind": "du",
        "source_variant_id": "run267dy_02_s258_stc_2025h1_dd_shape_split",
        "variant_id": "run267ec_01_s258_stc_2025h1_period_survival_gate",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_2025h1_period_survival_gate",
        "profile_token": "s258_period_survival",
        "materialization_type": "period_survival_state_gate_from_dd_shape",
        "split": "adjacent_2025_h1_validation_post_2024",
        "period_label": "2025H1",
        "from_date": "2025.01.02",
        "to_date": "2025.07.01",
        "attempt_role": "period_survival_gate_2025h1",
        "priority": "P0_survival_gate",
        "targeted_weakness": "2025H1 DD and weak May/session damage(2025H1 손실폭 및 5월/세션 손상)",
        "set_updates": {
            "InpShortThreshold": "0.535",
            "InpLongThreshold": "0.515",
            "InpAtrStopMultiplier": "1.78",
            "InpAtrTakeProfitMultiplier": "4.20",
            "InpModelRiskMaxPct": "0.024",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.012",
            "InpSameDirectionReentryCooldownBars": "4",
        },
        "known_difference": "Compresses 2025H1 survival risk without a May/hour/session hard ban.",
    },
    {
        "queue_id": "q02_s258_2025h2_period_survival_gate",
        "source_kind": "du",
        "source_variant_id": "run267dy_03_s258_stc_2025h2_dd_shape_split",
        "variant_id": "run267ec_02_s258_stc_2025h2_period_survival_gate",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_2025h2_period_survival_gate",
        "profile_token": "s258_period_survival",
        "materialization_type": "period_survival_state_gate_from_dd_shape",
        "split": "adjacent_2025_h2_oos_followthrough",
        "period_label": "2025H2",
        "from_date": "2025.07.01",
        "to_date": "2026.01.01",
        "attempt_role": "period_survival_gate_2025h2",
        "priority": "P0_survival_gate",
        "targeted_weakness": "2025H2 Monday and December DD(2025H2 월요일/12월 손실폭)",
        "set_updates": {
            "InpShortThreshold": "0.54",
            "InpLongThreshold": "0.52",
            "InpAtrStopMultiplier": "1.75",
            "InpAtrTakeProfitMultiplier": "4.15",
            "InpModelRiskMaxPct": "0.023",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.014",
            "InpSameDirectionReentryCooldownBars": "5",
        },
        "known_difference": "Separates 2025H2 survival pressure without banning Monday or December.",
    },
    {
        "queue_id": "q03_s258_explosive_impulse_supply_probe",
        "source_kind": "du",
        "source_variant_id": "run267dy_04_s258_stc_2023h2_state_falsification",
        "variant_id": "run267ec_03_s258_stc_2023h2_explosive_impulse_supply",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_2023h2_explosive_impulse_supply",
        "profile_token": "s258_explosive_impulse",
        "materialization_type": "explosive_impulse_supply_probe",
        "split": "adjacent_2023_h2_train_pre_2024",
        "period_label": "2023H2",
        "from_date": "2023.07.05",
        "to_date": "2024.01.01",
        "attempt_role": "explosive_impulse_supply_2023h2",
        "priority": "P0_aggressive_explosive",
        "targeted_weakness": "s258 strong-supply confirmation without calendar exclusion(s258 강한 공급 확인, 달력 제외 없음)",
        "set_updates": {
            "InpShortThreshold": "0.49",
            "InpLongThreshold": "0.47",
            "InpAtrStopMultiplier": "2.38",
            "InpAtrTakeProfitMultiplier": "5.45",
            "InpModelRiskMaxPct": "0.036",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.018",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Adds impulse supply pressure rather than a defensive filter.",
    },
    {
        "queue_id": "q03_s258_explosive_impulse_supply_probe",
        "source_kind": "du",
        "source_variant_id": "run267dy_05_s258_stc_2025h1_state_falsification",
        "variant_id": "run267ec_04_s258_stc_2025h1_explosive_impulse_supply",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_2025h1_explosive_impulse_supply",
        "profile_token": "s258_explosive_impulse",
        "materialization_type": "explosive_impulse_supply_probe",
        "split": "adjacent_2025_h1_validation_post_2024",
        "period_label": "2025H1",
        "from_date": "2025.01.02",
        "to_date": "2025.07.01",
        "attempt_role": "explosive_impulse_supply_2025h1",
        "priority": "P0_aggressive_explosive",
        "targeted_weakness": "2025H1 supply recovery without May/session ban(2025H1 공급 회복, 5월/세션 금지 없음)",
        "set_updates": {
            "InpShortThreshold": "0.49",
            "InpLongThreshold": "0.47",
            "InpAtrStopMultiplier": "2.35",
            "InpAtrTakeProfitMultiplier": "5.35",
            "InpModelRiskMaxPct": "0.034",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.018",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Pressures 2025H1 supply with an aggressive noncalendar impulse surface.",
    },
    {
        "queue_id": "q03_s258_explosive_impulse_supply_probe",
        "source_kind": "du",
        "source_variant_id": "run267dy_06_s258_stc_2025h2_state_falsification",
        "variant_id": "run267ec_05_s258_stc_2025h2_explosive_impulse_supply",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_2025h2_explosive_impulse_supply",
        "profile_token": "s258_explosive_impulse",
        "materialization_type": "explosive_impulse_supply_probe",
        "split": "adjacent_2025_h2_oos_followthrough",
        "period_label": "2025H2",
        "from_date": "2025.07.01",
        "to_date": "2026.01.01",
        "attempt_role": "explosive_impulse_supply_2025h2",
        "priority": "P0_aggressive_explosive",
        "targeted_weakness": "2025H2 supply recovery without Monday/December ban(2025H2 공급 회복, 월요일/12월 금지 없음)",
        "set_updates": {
            "InpShortThreshold": "0.495",
            "InpLongThreshold": "0.475",
            "InpAtrStopMultiplier": "2.32",
            "InpAtrTakeProfitMultiplier": "5.30",
            "InpModelRiskMaxPct": "0.033",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.018",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Tests whether the s258 branch can add OOS follow-through supply rather than hide weak months.",
    },
    {
        "queue_id": "q04_s264_aih_validation_anchor_integrity_check",
        "source_kind": "du",
        "source_variant_id": "run267dy_07_s264_aih_validation_anchor_repair",
        "variant_id": "run267ec_06_s264_aih_validation_anchor_integrity",
        "candidate_id": "s264_allow_inner_high_quarter",
        "candidate_alias": "s264_aih",
        "candidate_role": "challenger_core",
        "profile_label": "s264_aih_validation_anchor_integrity",
        "profile_token": "s264_aih_validation_integrity",
        "materialization_type": "validation_anchor_integrity_replay",
        "split": "validation_is",
        "period_label": "validation_is",
        "from_date": "2025.01.02",
        "to_date": "2025.10.01",
        "attempt_role": "validation_anchor_integrity",
        "priority": "P1_validation_integrity",
        "targeted_weakness": "validation anchor preservation before final-month repair(마지막 달 수리 전 검증 앵커 보존)",
        "set_updates": {
            "InpShortThreshold": "0.535",
            "InpLongThreshold": "0.515",
            "InpAtrStopMultiplier": "2.00",
            "InpAtrTakeProfitMultiplier": "4.55",
            "InpModelRiskMaxPct": "0.026",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpSameDirectionReentryCooldownBars": "2",
        },
        "known_difference": "Keeps validation integrity separate from the 2026.04 repair branch.",
    },
    {
        "queue_id": "q05_s264_aih_202604_counter_shock_rebuild",
        "source_kind": "du",
        "source_variant_id": "run267dy_08_s264_aih_202604_counter_shock_probe",
        "variant_id": "run267ec_07_s264_aih_202604_counter_shock_rebuild",
        "candidate_id": "s264_allow_inner_high_quarter",
        "candidate_alias": "s264_aih",
        "candidate_role": "challenger_core",
        "profile_label": "s264_aih_202604_counter_shock_rebuild",
        "profile_token": "s264_aih_counter_shock_rebuild",
        "materialization_type": "final_month_counter_shock_rebuild_cap",
        "split": "oos_final_month_2026_04",
        "period_label": "2026.04",
        "from_date": "2026.04.01",
        "to_date": "2026.04.14",
        "attempt_role": "final_month_counter_shock_rebuild",
        "priority": "P0_repair_cap",
        "targeted_weakness": "s264_aih 2026.04 negative final month(s264_aih 2026.04 음수 마지막 달)",
        "set_updates": {
            "InpShortThreshold": "0.555",
            "InpLongThreshold": "0.535",
            "InpAtrStopMultiplier": "1.88",
            "InpAtrTakeProfitMultiplier": "4.25",
            "InpModelRiskMaxPct": "0.024",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.02",
            "InpSameDirectionReentryCooldownBars": "3",
        },
        "known_difference": "One bounded final-month rebuild; it cannot become a third repair loop.",
    },
    {
        "queue_id": "q05_s264_aih_202604_counter_shock_rebuild",
        "source_kind": "du",
        "source_variant_id": "run267dy_09_s264_lc_202604_same_month_control",
        "variant_id": "run267ec_08_s264_lc_202604_counter_shock_control",
        "candidate_id": "s264_lowrank_control",
        "candidate_alias": "s264_lc",
        "candidate_role": "defensive_control",
        "profile_label": "s264_lc_202604_counter_shock_control",
        "profile_token": "s264_lc_counter_shock_control",
        "materialization_type": "paired_final_month_market_control",
        "split": "oos_final_month_2026_04",
        "period_label": "2026.04",
        "from_date": "2026.04.01",
        "to_date": "2026.04.14",
        "attempt_role": "paired_final_month_control",
        "priority": "P1_control",
        "targeted_weakness": "same-month market control for s264_aih repair(s264_aih 수리용 같은 달 시장 대조)",
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
        "known_difference": "Paired control only; one-month control cannot become a selected candidate.",
    },
    {
        "queue_id": "q06_s264_aih_explosive_counter_impulse_probe",
        "source_kind": "du",
        "source_variant_id": "run267dy_07_s264_aih_validation_anchor_repair",
        "variant_id": "run267ec_09_s264_aih_validation_explosive_counter_impulse",
        "candidate_id": "s264_allow_inner_high_quarter",
        "candidate_alias": "s264_aih",
        "candidate_role": "challenger_core",
        "profile_label": "s264_aih_validation_explosive_counter_impulse",
        "profile_token": "s264_aih_explosive_counter_impulse",
        "materialization_type": "explosive_counter_impulse_validation_probe",
        "split": "validation_is",
        "period_label": "validation_is",
        "from_date": "2025.01.02",
        "to_date": "2025.10.01",
        "attempt_role": "validation_explosive_counter_impulse",
        "priority": "P1_aggressive_explosive",
        "targeted_weakness": "validation damage check for aggressive s264_aih supply(공격형 s264_aih 공급의 검증 손상 확인)",
        "set_updates": {
            "InpShortThreshold": "0.49",
            "InpLongThreshold": "0.47",
            "InpAtrStopMultiplier": "2.24",
            "InpAtrTakeProfitMultiplier": "5.05",
            "InpModelRiskMaxPct": "0.033",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.018",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Aggressive validation pass to catch damage before reading the final month.",
    },
    {
        "queue_id": "q06_s264_aih_explosive_counter_impulse_probe",
        "source_kind": "du",
        "source_variant_id": "run267dy_08_s264_aih_202604_counter_shock_probe",
        "variant_id": "run267ec_10_s264_aih_202604_explosive_counter_impulse",
        "candidate_id": "s264_allow_inner_high_quarter",
        "candidate_alias": "s264_aih",
        "candidate_role": "challenger_core",
        "profile_label": "s264_aih_202604_explosive_counter_impulse",
        "profile_token": "s264_aih_explosive_counter_impulse",
        "materialization_type": "explosive_counter_impulse_final_month_probe",
        "split": "oos_final_month_2026_04",
        "period_label": "2026.04",
        "from_date": "2026.04.01",
        "to_date": "2026.04.14",
        "attempt_role": "final_month_explosive_counter_impulse",
        "priority": "P1_aggressive_explosive",
        "targeted_weakness": "2026.04 counter-impulse supply without final-month exclusion(2026.04 역임펄스 공급, 마지막 달 제외 없음)",
        "set_updates": {
            "InpShortThreshold": "0.49",
            "InpLongThreshold": "0.47",
            "InpAtrStopMultiplier": "2.20",
            "InpAtrTakeProfitMultiplier": "5.00",
            "InpModelRiskMaxPct": "0.032",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpEntryTransitionOnly": "true",
            "InpEntryTransitionRearmMinConfidenceDelta": "0.018",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Aggressive final-month supply probe; it is not a same-month rescue selection.",
    },
    {
        "queue_id": "q07_s262_s264_aia_pool_coverage_rejoin",
        "source_kind": "canonical",
        "source_candidate_id": "s262_lowrank_inner_half_filter",
        "source_split": "validation_is",
        "variant_id": "run267ec_11_s262_lih_validation_coverage_rejoin",
        "candidate_id": "s262_lowrank_inner_half_filter",
        "candidate_alias": "s262_lih",
        "candidate_role": "validation_heavy",
        "profile_label": "s262_lih_validation_coverage_rejoin",
        "profile_token": "s262_lih_coverage",
        "materialization_type": "pool_coverage_validation_rejoin",
        "split": "validation_is",
        "period_label": "validation_is",
        "from_date": "2025.01.02",
        "to_date": "2025.10.01",
        "attempt_role": "coverage_rejoin_validation",
        "priority": "P1_pool_coverage",
        "targeted_weakness": "missing validation-heavy pool axis(누락 검증 중심 후보축)",
        "set_updates": {},
        "known_difference": "Restores s262_lih validation coverage before narrowing the pool.",
    },
    {
        "queue_id": "q07_s262_s264_aia_pool_coverage_rejoin",
        "source_kind": "canonical",
        "source_candidate_id": "s262_lowrank_inner_half_filter",
        "source_split": "oos",
        "variant_id": "run267ec_12_s262_lih_202604_coverage_rejoin",
        "candidate_id": "s262_lowrank_inner_half_filter",
        "candidate_alias": "s262_lih",
        "candidate_role": "validation_heavy",
        "profile_label": "s262_lih_202604_coverage_rejoin",
        "profile_token": "s262_lih_coverage",
        "materialization_type": "pool_coverage_final_month_rejoin",
        "split": "oos_final_month_2026_04",
        "period_label": "2026.04",
        "from_date": "2026.04.01",
        "to_date": "2026.04.14",
        "attempt_role": "coverage_rejoin_final_month",
        "priority": "P1_pool_coverage",
        "targeted_weakness": "s262_lih final-month coverage gap(s262_lih 마지막 달 커버리지 공백)",
        "set_updates": {},
        "known_difference": "Checks whether the validation-heavy candidate breaks less in the same 2026.04 slice.",
    },
    {
        "queue_id": "q07_s262_s264_aia_pool_coverage_rejoin",
        "source_kind": "canonical",
        "source_candidate_id": "s264_allow_inner_all_oos_anchor",
        "source_split": "validation_is",
        "variant_id": "run267ec_13_s264_aia_validation_coverage_rejoin",
        "candidate_id": "s264_allow_inner_all_oos_anchor",
        "candidate_alias": "s264_aia",
        "candidate_role": "oos_anchor",
        "profile_label": "s264_aia_validation_coverage_rejoin",
        "profile_token": "s264_aia_coverage",
        "materialization_type": "pool_coverage_validation_rejoin",
        "split": "validation_is",
        "period_label": "validation_is",
        "from_date": "2025.01.02",
        "to_date": "2025.10.01",
        "attempt_role": "coverage_rejoin_validation",
        "priority": "P1_pool_coverage",
        "targeted_weakness": "missing OOS-anchor validation damage axis(누락 OOS 앵커 검증 손상 축)",
        "set_updates": {},
        "known_difference": "Restores s264_aia validation damage coverage before narrowing the pool.",
    },
    {
        "queue_id": "q07_s262_s264_aia_pool_coverage_rejoin",
        "source_kind": "canonical",
        "source_candidate_id": "s264_allow_inner_all_oos_anchor",
        "source_split": "oos",
        "variant_id": "run267ec_14_s264_aia_202604_coverage_rejoin",
        "candidate_id": "s264_allow_inner_all_oos_anchor",
        "candidate_alias": "s264_aia",
        "candidate_role": "oos_anchor",
        "profile_label": "s264_aia_202604_coverage_rejoin",
        "profile_token": "s264_aia_coverage",
        "materialization_type": "pool_coverage_final_month_rejoin",
        "split": "oos_final_month_2026_04",
        "period_label": "2026.04",
        "from_date": "2026.04.01",
        "to_date": "2026.04.14",
        "attempt_role": "coverage_rejoin_final_month",
        "priority": "P1_pool_coverage",
        "targeted_weakness": "s264_aia final-month coverage gap(s264_aia 마지막 달 커버리지 공백)",
        "set_updates": {},
        "known_difference": "Checks whether the OOS-anchor candidate explains the same final-month weakness differently.",
    },
)

HELD_QUEUE_CONFIGS: tuple[dict[str, str], ...] = (
    {
        "queue_id": "q08_filter_stack_prune_guard_hold",
        "priority": "P0_prune_guard",
        "candidate_aliases": "pool",
        "decision": "held_guardrail_only_no_standalone_mt5(가드레일 전용 보류, 단독 MT5 없음)",
        "why": "month/day/hour exclusion-only repair(월/요일/시간 제외 전용 수리)는 구조 증거가 아니다.",
        "reopen_condition": "Only with a market-state feature explanation(시장 상태 피처 설명) and cross-period survival.",
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
        "SOURCE_DU_VARIANT_MANIFEST_PATH": SOURCE_DY_VARIANT_MANIFEST_PATH,
        "SOURCE_DU_ATTEMPT_MANIFEST_PATH": SOURCE_DY_ATTEMPT_MANIFEST_PATH,
        "SOURCE_DU_RUNTIME_CONTRACT_PATH": SOURCE_DY_RUNTIME_CONTRACT_PATH,
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
    materializer_template.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    materializer_template.write_md(path, text)


def rewrite_set_header(attempt: dict[str, Any]) -> dict[str, Any]:
    path = repo_path(str(attempt["set_path"]))
    text = io_path(path).read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if lines and lines[0].startswith("; generated_by="):
        lines[0] = "; generated_by=run267EC_runtime_gap_aware_seventh_followup_or_prune_materialization"
        io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
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
    if str(plan["source_kind"]) == "du":
        variant["direct_source_materialization_run_id"] = SOURCE_MATERIALIZATION_RUN_ID
    else:
        variant["direct_source_materialization_run_id"] = "stage267_run267B_source_feature_manifest"
    attempt = rewrite_set_header(attempt)
    preflight["set_sha256"] = attempt["set_sha256"]
    return variant, feature, model, attempt, preflight


def anti_filter_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267ec_q08_anti_filter_stack",
            "queue_id": "q08_filter_stack_prune_guard_hold",
            "status": "enforced",
            "forbidden_pattern": "hour-only;weekday-only;month-only exclusion",
            "materialized_standalone": "false",
            "effect": "약한 구간을 단순 제외하지 않고 구조/상태/공급 실험으로 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def pool_coverage_rows(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for alias in ("s262_lih", "s264_aia"):
        alias_rows = [row for row in variant_rows if row["candidate_alias"] == alias]
        rows.append(
            {
                "receipt_id": f"run267ec_{alias}_coverage_rejoin",
                "candidate_alias": alias,
                "variant_count": len(alias_rows),
                "splits": ";".join(str(row["split"]) for row in alias_rows),
                "status": "materialized" if alias_rows else "missing_required",
                "effect": "누락 후보축을 다시 비교 표면으로 올려 후보군이 좁아지는 착시를 막는다.",
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
            "check_id": "run267ec_common_files_handoff",
            "status": "prepared",
            "evidence": f"variants={counts['variants']};attempts={counts['attempts']};held={counts['held_rows']}",
            "effect": "MT5(MetaTrader 5, 메타트레이더5) 실행 전 feature/model(피처/모델)을 Common Files(공통 파일)에 복사했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": f"run267ec_data_{row['variant_id']}",
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


def runtime_parity_rows(
    variant_rows: Sequence[Mapping[str, Any]], attempt_rows: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
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
            "evidence_available": (
                f"variants={counts['variants']};attempts={counts['attempts']};"
                f"held_rows={counts['held_rows']};coverage_variants={counts['coverage_variants']}"
            ),
            "evidence_missing": "MT5 execution result(실행 결과), balance/equity review(잔액/평가금 검토), candidate selection evidence(후보 선택 근거)",
            "judgment_label": "materialized_execution_pending_no_candidate_selection",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이번 작업은 다음 MT5 실행 입력을 만든 것이며 아직 성능 판정이나 후보 선택이 아니다.",
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "gate267ec_source_inputs",
            "gate_name": "source inputs present(원천 입력 존재)",
            "status": "pass",
            "evidence": f"{rel(SOURCE_QUEUE_PATH)};{rel(SOURCE_DY_VARIANT_MANIFEST_PATH)};{rel(SOURCE_FEATURE_MANIFEST_PATH)}",
            "effect": "run267EB 설계와 run267DY 물질화 근거, canonical source(정식 원천)를 같이 사용한다.",
        },
        {
            "gate_id": "gate267ec_materialization_count",
            "gate_name": "materialization count(물질화 수)",
            "status": "pass",
            "evidence": f"variants={counts['variants']};attempts={counts['attempts']}",
            "effect": "run267ED 실행 가능한 set/ini(설정/초기화)를 만들었다.",
        },
        {
            "gate_id": "gate267ec_aggressive_required",
            "gate_name": "aggressive rows preserved(공격형 행 보존)",
            "status": "pass" if counts["aggressive_attempts"] >= 2 else "fail",
            "evidence": f"aggressive_attempts={counts['aggressive_attempts']}",
            "effect": "방어형 필터 루프만 반복하지 않고 공급 확장 실험을 포함한다.",
        },
        {
            "gate_id": "gate267ec_pool_coverage",
            "gate_name": "pool coverage rejoined(후보군 커버리지 재합류)",
            "status": "pass" if counts["coverage_variants"] >= 4 else "fail",
            "evidence": f"coverage_variants={counts['coverage_variants']};s262={counts['s262_lih_variants']};s264_aia={counts['s264_aia_variants']}",
            "effect": "s262_lih/s264_aia 누락으로 후보군이 조기 축소되는 일을 막는다.",
        },
        {
            "gate_id": "gate267ec_anti_filter_stack",
            "gate_name": "anti filter stack enforced(필터 누적 방지)",
            "status": "pass",
            "evidence": "q08 held; no standalone hour/day/month exclusion attempt",
            "effect": "약점 구간을 숨기는 미세 조정 대신 구조 실험으로 남겼다.",
        },
        {
            "gate_id": "gate267ec_claim_guard",
            "gate_name": "claim guard(주장 경계)",
            "status": "pass",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx=not_claimed;goal=not_claimed",
            "effect": "물질화와 성능 판정을 섞지 않는다.",
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
        "source_dy_variant_manifest": rel(SOURCE_DY_VARIANT_MANIFEST_PATH),
        "source_dy_attempt_manifest": rel(SOURCE_DY_ATTEMPT_MANIFEST_PATH),
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
        "artifact_lineage_id": "stage267_run267EC_runtime_gap_aware_seventh_followup_or_prune_materialization",
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
        "# Stage267 Run267EC Runtime Gap Aware Seventh Follow-Up/Prune Materialization(267단계 267EC 런타임 공백 반영 7차 후속/가지치기 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- source_materialization(원천 물질화): `{SOURCE_MATERIALIZATION_RUN_ID}`",
        f"- variants(변형): `{counts['variants']}`",
        f"- attempts(시도): `{counts['attempts']}`",
        f"- held_rows(보류 행): `{counts['held_rows']}`",
        f"- aggressive_attempts(공격형 시도): `{counts['aggressive_attempts']}`",
        f"- coverage_variants(커버리지 변형): `{counts['coverage_variants']}`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267EC(267EC 실행)는 run267EB(267EB 실행)의 8개 queue(대기열)를 실제 MT5(MetaTrader 5, 메타트레이더5) 입력으로 바꾼 단계다.",
        "q01-q02는 s258_stc의 2025H1/H2 생존 압박을 따로 본다. q03은 s258_stc의 aggressive/explosive(공격/폭발) 공급 실험을 2023H2, 2025H1, 2025H2로 나눴다.",
        "q04-q06은 s264_aih 검증 앵커, 2026.04 제한 수리, 공격형 역임펄스를 분리했다. s264_lc는 같은 달 시장 대조(control, 대조)로만 둔다.",
        "q07은 빠졌던 s262_lih와 s264_aia를 validation(검증)과 2026.04 final month(마지막 달)에 다시 붙였다. q08은 필터 누적 방지 held(보류)로 남겼다.",
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
            "run267EC(267EC 실행)는 materialization(물질화)이다. 아직 MT5(MetaTrader 5, 메타트레이더5) 성능 결과, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표)는 없다.",
            "따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- materialization_plan(물질화 계획): `{rel(MATERIALIZATION_PLAN_PATH)}`",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- preflight_handoff_receipt(사전 인계 영수증): `{rel(PREFLIGHT_RECEIPT_PATH)}`",
            f"- anti_filter_stack_receipt(필터 누적 방지 영수증): `{rel(ANTI_FILTER_STACK_RECEIPT_PATH)}`",
            f"- pool_coverage_receipt(후보군 커버리지 영수증): `{rel(POOL_COVERAGE_RECEIPT_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    specs: list[tuple[str, str, Path, str]] = [
        ("stage267_run267EC_producer", "producer_script", PRODUCER_PATH, "Builds run267EC seventh follow-up/prune materialization."),
        ("stage267_run267EC_source_queue", "source_queue", SOURCE_QUEUE_PATH, "Source run267EB queue."),
        ("stage267_run267EC_source_feature_blueprint", "source_feature_blueprint", SOURCE_FEATURE_BLUEPRINT_PATH, "Source run267EB feature blueprint."),
        ("stage267_run267EC_source_branch_decision", "source_branch_decision", SOURCE_BRANCH_DECISION_PATH, "Source run267EB branch decisions."),
        ("stage267_run267EC_source_prune_matrix", "source_prune_matrix", SOURCE_PRUNE_MATRIX_PATH, "Source run267EB prune matrix."),
        ("stage267_run267EC_source_dy_variant_manifest", "source_variant_manifest", SOURCE_DY_VARIANT_MANIFEST_PATH, "Source run267DY variant manifest."),
        ("stage267_run267EC_source_feature_manifest", "source_feature_manifest", SOURCE_FEATURE_MANIFEST_PATH, "Canonical pool source feature manifest."),
        ("stage267_run267EC_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH, "Materialization plan."),
        ("stage267_run267EC_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Queue decision."),
        ("stage267_run267EC_feature_frame_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Feature frame manifest."),
        ("stage267_run267EC_model_manifest", "model_manifest", MODEL_MANIFEST_PATH, "Model manifest."),
        ("stage267_run267EC_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Variant manifest."),
        ("stage267_run267EC_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Attempt manifest."),
        ("stage267_run267EC_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract."),
        ("stage267_run267EC_held_queue", "held_queue", HELD_QUEUE_PATH, "Held queue."),
        ("stage267_run267EC_preflight_handoff", "preflight_handoff_receipt", PREFLIGHT_RECEIPT_PATH, "Preflight handoff receipt."),
        ("stage267_run267EC_anti_filter_stack", "anti_filter_stack_receipt", ANTI_FILTER_STACK_RECEIPT_PATH, "Anti filter-stack receipt."),
        ("stage267_run267EC_pool_coverage", "pool_coverage_receipt", POOL_COVERAGE_RECEIPT_PATH, "Pool coverage receipt."),
        ("stage267_run267EC_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267EC_environment", "environment_reproducibility_receipt", ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, "Environment receipt."),
        ("stage267_run267EC_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267EC_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267EC_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267EC_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267EC_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267EC_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267EC_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267EC_report", "review_report", REPORT_PATH, "User-facing report."),
    ]
    for row in result["variant_manifest"]:
        specs.append(
            (
                f"stage267_run267EC_feature_{row['variant_id']}",
                "runtime_feature_frame",
                repo_path(row["runtime_feature_file"]),
                "Runtime feature copy.",
            )
        )
        specs.append(
            (
                f"stage267_run267EC_model_{row['variant_id']}",
                "runtime_model_table",
                repo_path(row["runtime_model_file"]),
                "Runtime model copy.",
            )
        )
    for row in result["attempt_manifest"]:
        specs.append((f"stage267_run267EC_set_{row['attempt_name']}", "mt5_set", repo_path(row["set_path"]), "MT5 set file."))
        specs.append((f"stage267_run267EC_ini_{row['attempt_name']}", "mt5_ini", repo_path(row["ini_path"]), "MT5 tester ini file."))

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
        "lane": "runtime_gap_aware_seventh_followup_or_prune_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    stage_row = {
        "row_id": "stage267_run267EC_runtime_gap_aware_seventh_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_seventh_followup_or_prune_materialization",
        "tier_scope": "Tier A materialized; q08 guardrail held; s262/s264_aia coverage rejoined",
        "scoreboard": "execution_pending_no_candidate_selection_no_onnx",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "feature_model_set_ini_handoff_materialized_no_mt5_kpi",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_seventh_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_seventh_followup_or_prune_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization",
        "tier_scope": "Tier A materialized; q08 guardrail held; missing pool axes rejoined",
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
    line = f"  run267EC_runtime_gap_aware_seventh_followup_or_prune_materialization_report_path: {rel(REPORT_PATH)}"
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
        "- run267EC_runtime_gap_aware_seventh_followup_or_prune_materialization"
        f"(267EC 런타임 공백 반영 7차 후속/가지치기 물질화): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267EC(267EC 실행)는 run267EB(267EB 실행)의 materialization queue(물질화 대기열)를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 바꿨다.",
            f"Effect(효과): variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개, aggressive attempts(공격형 시도) `{counts['aggressive_attempts']}`개, coverage variants(커버리지 변형) `{counts['coverage_variants']}`개를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(
        current,
        "- adapter_under_review(검토 중 어댑터):",
        "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_seventh_followup_or_prune_materialization`",
    )
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_after_contains(current, "stage267_run267EB_runtime_gap_aware_seventh_followup_or_prune_design.md", report_line)
    current = replace_line_prefix(
        current,
        "- latest_materialization(최신 물질화):",
        f"- latest_materialization(최신 물질화): run267EC(267EC 실행) variants(변형) `{counts['variants']}`, "
        f"attempts(시도) `{counts['attempts']}`, held_rows(보류 행) `{counts['held_rows']}`, "
        f"aggressive_attempts(공격형 시도) `{counts['aggressive_attempts']}`, "
        f"coverage_variants(커버리지 변형) `{counts['coverage_variants']}`, report(보고서) `{rel(REPORT_PATH)}`.",
    )
    current = append_block_once(current, "Run267EC(267EC 실행)는 run267EB", block)
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_after_contains(selection, "run267EB_runtime_gap_aware_seventh_followup_or_prune_design", report_line)
    selection = append_block_once(selection, "Run267EC(267EC 실행)는 run267EB", block)
    write_md(SELECTION_STATUS_PATH, selection)

    review_index = read_text(REVIEW_INDEX_PATH)
    review_index = replace_line_containing(review_index, "- status(", f"- status(상태): `{STATUS}`")
    review_index = replace_line_containing(review_index, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_containing(review_index, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review_index = append_after_contains(review_index, "stage267_run267EB_runtime_gap_aware_seventh_followup_or_prune_design.md", report_line)
    review_index = append_block_once(review_index, "Run267EC(267EC 실행)는 run267EB", block)
    write_md(REVIEW_INDEX_PATH, review_index)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        "  Stage267(267단계) run267EC(267EC 실행) runtime gap aware seventh follow-up/prune materialization"
        f"(런타임 공백 반영 7차 후속/가지치기 물질화) `{STATUS}`. "
        f"Effect(효과): run267EB(267EB 실행)의 queue(대기열)를 variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, "
        f"held rows(보류 행) `{counts['held_rows']}`개로 바꿨고, selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), "
        "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
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
        SOURCE_DY_VARIANT_MANIFEST_PATH,
        SOURCE_DY_ATTEMPT_MANIFEST_PATH,
        SOURCE_DY_RUNTIME_CONTRACT_PATH,
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
        "aggressive_attempts": sum(1 for row in attempt_rows if "aggressive" in str(row["priority"]).lower() or "explosive" in str(row["priority"]).lower()),
        "survival_attempts": sum(1 for row in attempt_rows if "survival" in str(row["priority"]).lower()),
        "repair_attempts": sum(1 for row in attempt_rows if "repair" in str(row["priority"]).lower()),
        "control_attempts": sum(1 for row in attempt_rows if "control" in str(row["priority"]).lower()),
        "coverage_variants": sum(1 for row in variant_rows if row["queue_id"] == "q07_s262_s264_aia_pool_coverage_rejoin"),
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
        json.dumps(
            {
                "status": result["status"],
                "variants": counts["variants"],
                "attempts": counts["attempts"],
                "held_rows": counts["held_rows"],
                "aggressive_attempts": counts["aggressive_attempts"],
                "coverage_variants": counts["coverage_variants"],
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
