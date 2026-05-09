from __future__ import annotations

from stage_pipelines.stage35 import atlas_config as base
from stage_pipelines.stage35.common import ROOT


STAGE_ID = base.STAGE_ID
STAGE_NUMBER = base.STAGE_NUMBER
STAGE_ROOT = base.STAGE_ROOT
STAGE_LEDGER_PATH = base.STAGE_LEDGER_PATH
RUN_NUMBER = "run29C"
RUN_ID = "run29C_stage35_candidate_four_deep_dive_mt5_probe_v1"
PACKET_ID = "stage35_run29C_candidate_four_deep_dive_mt5_probe_v1"
EXPLORATION_LABEL = "stage35_ContextMap__CandidateFourDeepDive"
IDEA_ID = "IDEA-ST35-CANDIDATE-FOUR-DEEP-DIVE"
BOUNDARY = "stage35_candidate_four_deep_dive_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_stage35_candidate_four_deep_dive_mt5_completed"
JUDGMENT_BLOCKED = "blocked_stage35_candidate_four_deep_dive_mt5_after_attempt"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
RESULT_ROOT = RUN_ROOT / "results"
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / "run29C_candidate_four_deep_dive_packet.md"
DECISION_PATH = ROOT / "docs" / "decisions" / "2026-05-09_stage35_run29C_candidate_four_deep_dive.md"
MODEL_FAMILY = "stage35_candidate_four_row_omission_constant_ebm_runtime_probe"
SOURCE_RUN_ID = "run29B_stage35_worthwhile_deep_sweep_mt5_probe_v1"
SOURCE_PACKET_ID = "stage35_run29B_worthwhile_deep_sweep_mt5_probe_v1"
FEATURE_ORDER = base.FEATURE_ORDER
FEATURE_ORDER_HASH = base.FEATURE_ORDER_HASH
FEATURE_SET_ID = base.FEATURE_SET_ID
LABEL_ID = base.LABEL_ID
SPLIT_CONTRACT = base.SPLIT_CONTRACT
CANDIDATE_IDS = (
    "return_volatility_shape_state2",
    "trend_momentum_pressure_state1",
    "session_cash_open_0_30",
    "session_cash_mid_180_330",
)
HOLD_VALUES = (6, 12, 24)


__all__ = [
    "BOUNDARY",
    "CANDIDATE_IDS",
    "DECISION_PATH",
    "EXPLORATION_LABEL",
    "FEATURE_ORDER",
    "FEATURE_ORDER_HASH",
    "FEATURE_SET_ID",
    "HOLD_VALUES",
    "IDEA_ID",
    "JUDGMENT_BLOCKED",
    "JUDGMENT_COMPLETED",
    "LABEL_ID",
    "MODEL_FAMILY",
    "PACKET_ID",
    "PACKET_ROOT",
    "REPORT_PATH",
    "RESULT_ROOT",
    "RUN_ID",
    "RUN_NUMBER",
    "RUN_ROOT",
    "SOURCE_PACKET_ID",
    "SOURCE_RUN_ID",
    "SPLIT_CONTRACT",
    "STAGE_ID",
    "STAGE_LEDGER_PATH",
    "STAGE_NUMBER",
    "STAGE_ROOT",
]
