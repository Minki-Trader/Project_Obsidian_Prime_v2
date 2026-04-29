from __future__ import annotations

"""Stable MT5 runtime support imports for non-orchestration code."""

from foundation.control_plane.mt5_kpi_records import (
    ROUTING_MODE_A_B_FALLBACK,
    ROUTING_MODE_A_ONLY,
    TIER_A,
    TIER_AB,
    TIER_B,
    build_mt5_kpi_records,
    enrich_mt5_kpi_records_with_route_coverage,
)
from foundation.control_plane.tier_context_materialization import (
    TIER_B_CORE_FEATURE_ORDER,
    build_tier_b_partial_context_frames,
)
from foundation.models.baseline_training import LABEL_ORDER
from foundation.models.decision_surface import (
    DECISION_CLASS_NO_TRADE,
    DECISION_LABEL_NO_TRADE,
    PROBABILITY_COLUMNS,
    ThresholdRule,
    apply_threshold_rule,
    probability_matrix,
    threshold_rule_from_values,
    threshold_rule_payload,
    validate_threshold_rule,
)
from foundation.models.onnx_bridge import (
    _find_probability_output,
    _onnx_output_shape,
    check_onnxruntime_probability_parity,
    ordered_hash,
    ordered_sklearn_probabilities,
    export_sklearn_to_onnx_zipmap_disabled,
)
from foundation.mt5.mql5_compile import compile_mql5_ea, metaeditor_command_log_path
from foundation.mt5.runtime_artifacts import (
    EA_EXPERT_PATH,
    EA_SOURCE_PATH,
    EA_TESTER_SET_NAME,
    _io_path,
    _json_ready,
    _path_exists,
    attach_mt5_report_metrics,
    collect_mt5_strategy_report_artifacts,
    copy_to_common_files,
    export_mt5_feature_matrix_csv,
    mt5_runtime_module_hashes,
    remove_existing_mt5_report_artifacts,
    report_name_from_attempt,
    sha256_file,
    sha256_file_lf_normalized,
    validate_feature_matrix,
    write_json,
)
from foundation.mt5.terminal_runner import run_mt5_tester, validate_mt5_runtime_outputs, wait_for_mt5_runtime_outputs
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file


FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
