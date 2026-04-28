from __future__ import annotations

"""MT5 runtime support compatibility owner.

This module gives non-pipeline code a stable MT5 owner import while the older
Stage 10 orchestration file is being decomposed. New shared MT5 runtime logic
should move here or into narrower modules instead of adding more helpers to a
stage pipeline.
"""

from foundation.pipelines import run_stage10_logreg_mt5_scout as _stage10


collect_mt5_strategy_report_artifacts = _stage10.collect_mt5_strategy_report_artifacts
attach_mt5_report_metrics = _stage10.attach_mt5_report_metrics
build_mt5_kpi_records = _stage10.build_mt5_kpi_records
enrich_mt5_kpi_records_with_route_coverage = _stage10.enrich_mt5_kpi_records_with_route_coverage
remove_existing_mt5_report_artifacts = _stage10.remove_existing_mt5_report_artifacts
report_name_from_attempt = _stage10.report_name_from_attempt
run_mt5_tester = _stage10.run_mt5_tester
wait_for_mt5_runtime_outputs = _stage10.wait_for_mt5_runtime_outputs

build_tier_b_partial_context_frames = _stage10.build_tier_b_partial_context_frames
check_onnxruntime_probability_parity = _stage10.check_onnxruntime_probability_parity
compile_mql5_ea = _stage10.compile_mql5_ea
copy_to_common_files = _stage10.copy_to_common_files
export_mt5_feature_matrix_csv = _stage10.export_mt5_feature_matrix_csv
export_sklearn_to_onnx_zipmap_disabled = _stage10.export_sklearn_to_onnx_zipmap_disabled
ordered_hash = _stage10.ordered_hash
ordered_sklearn_probabilities = _stage10.ordered_sklearn_probabilities
threshold_rule_from_values = _stage10.threshold_rule_from_values
threshold_rule_payload = _stage10.threshold_rule_payload

EA_SOURCE_PATH = _stage10.EA_SOURCE_PATH
FEATURE_ORDER_HASH = _stage10.FEATURE_ORDER_HASH
LABEL_ORDER = _stage10.LABEL_ORDER
TIER_A = _stage10.TIER_A
TIER_B = _stage10.TIER_B
TIER_AB = _stage10.TIER_AB
TIER_B_CORE_FEATURE_ORDER = _stage10.TIER_B_CORE_FEATURE_ORDER
ThresholdRule = _stage10.ThresholdRule
TrainingLabelSplitSpec = _stage10.TrainingLabelSplitSpec
ROUTING_MODE_A_B_FALLBACK = _stage10.ROUTING_MODE_A_B_FALLBACK
ROUTING_MODE_A_ONLY = _stage10.ROUTING_MODE_A_ONLY
