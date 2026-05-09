from __future__ import annotations

from pathlib import Path

from stage_pipelines.stage35 import atlas_config as base
from stage_pipelines.stage35.common import ROOT


STAGE_ID = base.STAGE_ID
STAGE_NUMBER = base.STAGE_NUMBER
RUN_NUMBER = "run29B"
RUN_ID = "run29B_stage35_worthwhile_deep_sweep_mt5_probe_v1"
PACKET_ID = "stage35_run29B_worthwhile_deep_sweep_mt5_probe_v1"
EXPLORATION_LABEL = "stage35_ContextMap__WorthwhileDeepSweep"
IDEA_ID = "IDEA-ST35-WORTHWHILE-DEEP-SWEEP"
BOUNDARY = "stage35_worthwhile_deep_sweep_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_stage35_worthwhile_deep_sweep_mt5_completed"
JUDGMENT_BLOCKED = "blocked_stage35_worthwhile_deep_sweep_mt5_after_attempt"
RUN_ROOT = base.STAGE_ROOT / "02_runs" / RUN_ID
RESULT_ROOT = RUN_ROOT / "results"
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
REPORT_PATH = base.STAGE_ROOT / "03_reviews" / "run29B_worthwhile_deep_sweep_packet.md"
DECISION_PATH = ROOT / "docs" / "decisions" / "2026-05-09_stage35_run29B_worthwhile_deep_sweep.md"
STAGE_ROOT = base.STAGE_ROOT
STAGE_LEDGER_PATH = base.STAGE_LEDGER_PATH
MODEL_FAMILY = "stage35_worthwhile_context_row_omission_constant_ebm_runtime_probe"
FEATURE_SET_ID = base.FEATURE_SET_ID
LABEL_ID = base.LABEL_ID
SPLIT_CONTRACT = base.SPLIT_CONTRACT
FEATURE_ORDER = base.FEATURE_ORDER
FEATURE_ORDER_HASH = base.FEATURE_ORDER_HASH
MAX_HOLD_BARS = base.MAX_HOLD_BARS
MIN_VALIDATION_ROWS = 200
SOURCE_PACKET_ID = base.PACKET_ID
SOURCE_RUN_ID = base.RUN_ID


__all__ = [
    "BOUNDARY",
    "DECISION_PATH",
    "EXPLORATION_LABEL",
    "FEATURE_ORDER",
    "FEATURE_ORDER_HASH",
    "FEATURE_SET_ID",
    "IDEA_ID",
    "JUDGMENT_BLOCKED",
    "JUDGMENT_COMPLETED",
    "LABEL_ID",
    "MAX_HOLD_BARS",
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
