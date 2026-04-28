from __future__ import annotations

"""MT5 runtime support compatibility owner.

This module gives non-pipeline code a stable MT5 owner import while the older
Stage 10 orchestration file is being decomposed. New shared MT5 runtime logic
should move here or into narrower modules instead of adding more helpers to a
stage pipeline.
"""

from foundation.pipelines import run_stage10_logreg_mt5_scout as _stage10


collect_mt5_strategy_report_artifacts = _stage10.collect_mt5_strategy_report_artifacts
remove_existing_mt5_report_artifacts = _stage10.remove_existing_mt5_report_artifacts
report_name_from_attempt = _stage10.report_name_from_attempt
run_mt5_tester = _stage10.run_mt5_tester
wait_for_mt5_runtime_outputs = _stage10.wait_for_mt5_runtime_outputs
