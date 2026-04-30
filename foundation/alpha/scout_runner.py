from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.alpha.decision_views import (
    DECISION_CLASS_NO_TRADE,
    DECISION_LABEL_NO_TRADE,
    PROBABILITY_COLUMNS,
    TIER_A,
    TIER_AB,
    TIER_B,
    TIER_COLUMN,
    ThresholdRule,
    apply_threshold_rule,
    build_paired_tier_records as _build_paired_tier_records,
    build_prediction_frame,
    build_tier_prediction_views,
    materialize_tier_prediction_views,
    probability_matrix,
    select_threshold_from_sweep,
    sweep_threshold_rules,
    threshold_rule_from_values,
    threshold_rule_payload,
    validate_threshold_rule,
)
from foundation.alpha.specs import default_common_run_root, run_output_root, stage_review_ledger_path
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path as _io_path,
    json_ready as _json_ready,
    ledger_pairs as _ledger_pairs,
    ledger_path as _ledger_path,
    ledger_status as _ledger_status,
    path_exists as _path_exists,
)
from foundation.control_plane.mt5_kpi_records import (
    ROUTING_MODE_A_B_FALLBACK,
    ROUTING_MODE_A_ONLY,
    build_mt5_kpi_records,
    enrich_mt5_kpi_records_with_route_coverage,
)
from foundation.control_plane.routing_coverage import (
    SESSION_SLICE_DEFINITIONS,
    apply_session_slice,
    build_eval_route_coverage_summary,
    session_slice_payload,
)
from foundation.control_plane.tier_context_materialization import (
    ROUTE_ROLE_A_PRIMARY,
    TIER_B_CORE_FEATURE_ORDER,
    TIER_B_PARTIAL_CONTEXT_DATASET_ID,
    TIER_B_PARTIAL_CONTEXT_FEATURE_SET_ID,
    TIER_B_PARTIAL_CONTEXT_POLICY_ID,
    build_tier_b_partial_context_frames,
)
from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, load_feature_order
from foundation.models.onnx_bridge import (
    _find_probability_output,
    _onnx_output_shape,
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
)
from foundation.mt5 import runtime_artifacts as mt5_artifacts
from foundation.mt5.runtime_support import (
    EA_SOURCE_PATH,
    EA_TESTER_SET_NAME,
    TesterMaterializationConfig,
    compile_mql5_ea,
    copy_to_common_files,
    export_mt5_feature_matrix_csv,
    mt5_runtime_module_hashes,
    run_mt5_tester,
    sha256_file,
    sha256_file_lf_normalized,
    validate_mt5_runtime_outputs,
    wait_for_mt5_runtime_outputs,
    write_json,
)
from foundation.mt5.tester_files import materialize_tester_ini_file, materialize_tester_set_file
from foundation.pipelines.materialize_training_label_split_dataset import TrainingLabelSplitSpec


STAGE_ID = "10_alpha_scout__default_split_model_threshold_scan"
RUN_NUMBER = "run01A"
RUN_ID = "run01A_logreg_threshold_mt5_scout_v1"
EXPLORATION_LABEL = "stage10_Model__LogReg_MT5Scout"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/stage10/run01A_logreg_threshold_mt5_scout_v1"
FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
TIER_B_MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_feature_set_v1_no_placeholder_top3_weights"
TIER_B_FEATURE_SET_ID = "feature_set_v1_no_placeholder_top3_weight_features"
MT5_RECORD_TIER_A_ONLY_PREFIX = "mt5_tier_a_only"
MT5_RECORD_TIER_B_FALLBACK_ONLY_PREFIX = "mt5_tier_b_fallback_only"


@dataclass(frozen=True)
class ScoutRunContext:
    stage_id: str
    stage_number: int
    run_number: str
    run_id: str
    exploration_label: str
    output_root: Path
    common_run_root: str
    common_files_root: Path
    terminal_data_root: Path
    tester_profile_root: Path

    def common_ref(self, *parts: str) -> str:
        return "/".join([self.common_run_root, *parts])


def build_run_context(
    *,
    stage_id: str,
    stage_number: int,
    run_number: str,
    run_id: str,
    exploration_label: str,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    output_root: Path | None = None,
    common_run_root: str | None = None,
) -> ScoutRunContext:
    return ScoutRunContext(
        stage_id=stage_id,
        stage_number=stage_number,
        run_number=run_number,
        run_id=run_id,
        exploration_label=exploration_label,
        output_root=output_root or run_output_root(stage_id, run_id),
        common_run_root=common_run_root or default_common_run_root(stage_number, run_id),
        common_files_root=common_files_root,
        terminal_data_root=terminal_data_root,
        tester_profile_root=tester_profile_root,
    )


def stage_paths(stage_id: str, run_id: str) -> dict[str, Path]:
    output_root = run_output_root(stage_id, run_id)
    return {
        "run_output_root": output_root,
        "stage_run_ledger": stage_review_ledger_path(stage_id),
        "project_alpha_ledger": Path("docs/registers/alpha_run_ledger.csv"),
        "run_registry": Path("docs/registers/run_registry.csv"),
        "mt5_root": output_root / "mt5",
        "predictions_root": output_root / "predictions",
        "models_root": output_root / "models",
    }


def artifact_record(
    *,
    role: str,
    path: Path,
    sha256: str | None = None,
    format: str | None = None,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {"role": role, "path": path.as_posix()}
    if format is not None:
        record["format"] = format
    if sha256 is not None:
        record["sha256"] = sha256
    if extra:
        record.update(dict(extra))
    return record


def extend_stage_specs(existing: Sequence[Mapping[str, Any]], *new_specs: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return copy-on-write specs so Stage13+ can append runs without mutating Stage10-12 definitions."""
    return [dict(item) for item in existing] + [dict(item) for item in new_specs]


def configure_run_identity(
    *,
    run_number: str,
    run_id: str,
    exploration_label: str,
    common_run_root: str | None = None,
    stage_id: str | None = None,
) -> None:
    global STAGE_ID, RUN_NUMBER, RUN_ID, EXPLORATION_LABEL, COMMON_RUN_ROOT

    if stage_id is not None:
        STAGE_ID = stage_id
    RUN_NUMBER = run_number
    RUN_ID = run_id
    EXPLORATION_LABEL = exploration_label
    COMMON_RUN_ROOT = common_run_root or default_common_run_root(STAGE_ID.split("_", 1)[0], run_id)


def common_ref(*parts: str) -> str:
    return "/".join([COMMON_RUN_ROOT, *parts])


def load_label_threshold(summary_path: Path) -> float:
    payload = json.loads(_io_path(summary_path).read_text(encoding="utf-8"))
    threshold = float(payload["threshold_log_return"])
    if not np.isfinite(threshold) or threshold <= 0:
        raise RuntimeError(f"Invalid label threshold in {summary_path}: {threshold}")
    return threshold


def build_paired_tier_records(
    tier_views: Mapping[str, pd.DataFrame],
    *,
    run_id: str | None = None,
    stage_id: str | None = None,
    base_path: str | Path | None = None,
    kpi_scope: str = "signal_probability_threshold",
    scoreboard_lane: str = "structural_scout",
    external_verification_status: str = "out_of_scope_by_claim",
) -> list[dict[str, Any]]:
    return _build_paired_tier_records(
        tier_views,
        run_id=run_id or RUN_ID,
        stage_id=stage_id or STAGE_ID,
        base_path=base_path,
        kpi_scope=kpi_scope,
        scoreboard_lane=scoreboard_lane,
        external_verification_status=external_verification_status,
    )


def mt5_short_profile_ini_name(tier_name: str, split_name: str) -> str:
    if tier_name == TIER_AB:
        tier_code = "rt"
    else:
        tier_code = "ta" if tier_name == TIER_A else "tb"
    split_code = "v" if split_name == "validation_is" else "o"
    return f"opv2_{RUN_NUMBER}_{tier_code}_{split_code}.ini"


def materialize_mt5_attempt_files(
    *,
    run_output_root: Path,
    tier_name: str,
    split_name: str,
    local_onnx_path: Path,
    local_feature_matrix_path: Path,
    rule: ThresholdRule,
    feature_count: int,
    feature_order_hash: str,
    from_date: str,
    to_date: str,
    stem_prefix: str | None = None,
    record_view_prefix: str | None = None,
    primary_active_tier: str = "tier_a",
    attempt_role: str = "tier_only_total",
    invert_signal: bool = False,
    max_hold_bars: int = 12,
) -> dict[str, Any]:
    tier_slug = tier_name.lower().replace(" ", "_").replace("+", "ab")
    stem = f"{stem_prefix or tier_slug}_{split_name}"
    common_model = common_ref("models", local_onnx_path.name)
    common_matrix = common_ref("features", local_feature_matrix_path.name)
    common_telemetry = common_ref("telemetry", f"{stem}_telemetry.csv")
    common_summary = common_ref("telemetry", f"{stem}_summary.csv")
    set_path = run_output_root / "mt5" / f"{stem}.set"
    ini_path = run_output_root / "mt5" / f"{stem}.ini"
    set_payload = materialize_tester_set_file(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": tier_name,
            "InpPrimaryActiveTier": primary_active_tier,
            "InpSplitLabel": split_name,
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpModelPath": common_model,
            "InpModelId": f"{RUN_ID}_{stem_prefix or tier_slug}",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": common_matrix,
            "InpFeatureCount": feature_count,
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpFeatureStrictHeader": "true",
            "InpCsvTimestampIsBarClose": "true",
            "InpFallbackEnabled": "false",
            "InpTelemetryCsvPath": common_telemetry,
            "InpSummaryCsvPath": common_summary,
            "InpTelemetryUseCommonFiles": "true",
            "InpShortThreshold": rule.short_threshold,
            "InpLongThreshold": rule.long_threshold,
            "InpMinMargin": rule.min_margin,
            "InpInvertSignal": bool(invert_signal),
            "InpFallbackShortThreshold": rule.short_threshold,
            "InpFallbackLongThreshold": rule.long_threshold,
            "InpFallbackMinMargin": rule.min_margin,
            "InpFallbackInvertSignal": bool(invert_signal),
            "InpAllowTrading": "true",
            "InpFixedLot": 0.1,
            "InpMaxHoldBars": int(max_hold_bars),
            "InpMaxConcurrentPositions": 1,
            "InpFeatureOrderHash": feature_order_hash,
            "InpMagic": 1001001 if tier_name == TIER_A else 1001002,
        },
        set_path,
    )
    report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{stem}"
    ini_payload = materialize_tester_ini_file(
        TesterMaterializationConfig(from_date=from_date, to_date=to_date, report=report_name, shutdown_terminal=1),
        ini_path,
        set_file_path=Path(EA_TESTER_SET_NAME),
    )
    return {
        "tier": tier_name,
        "split": split_name,
        "attempt_role": attempt_role,
        "record_view_prefix": record_view_prefix or f"mt5_{stem_prefix or tier_slug}",
        "set": set_payload,
        "ini": ini_payload,
        "common_model_path": common_model,
        "common_feature_matrix_path": common_matrix,
        "common_telemetry_path": common_telemetry,
        "common_summary_path": common_summary,
        "local_feature_matrix_path": local_feature_matrix_path.as_posix(),
        "threshold_rule": threshold_rule_payload(rule),
        "invert_signal": bool(invert_signal),
        "max_hold_bars": int(max_hold_bars),
    }


def materialize_mt5_routed_attempt_files(
    *,
    run_output_root: Path,
    split_name: str,
    primary_onnx_path: Path,
    primary_feature_matrix_path: Path,
    primary_feature_count: int,
    primary_feature_order_hash: str,
    fallback_onnx_path: Path,
    fallback_feature_matrix_path: Path,
    fallback_feature_count: int,
    fallback_feature_order_hash: str,
    rule: ThresholdRule,
    from_date: str,
    to_date: str,
    fallback_rule: ThresholdRule | None = None,
    invert_signal: bool = False,
    fallback_invert_signal: bool = False,
    max_hold_bars: int = 12,
    fallback_enabled: bool = True,
) -> dict[str, Any]:
    fallback_rule = fallback_rule or rule
    routing_mode = ROUTING_MODE_A_B_FALLBACK if fallback_enabled else ROUTING_MODE_A_ONLY
    routing_detail = (
        "tier_a_primary_tier_b_partial_context_fallback"
        if fallback_enabled
        else "tier_a_primary_no_fallback"
    )
    stem = f"routed_{split_name}"
    common_primary_model = common_ref("models", primary_onnx_path.name)
    common_primary_matrix = common_ref("features", primary_feature_matrix_path.name)
    common_fallback_model = common_ref("models", fallback_onnx_path.name)
    common_fallback_matrix = common_ref("features", fallback_feature_matrix_path.name)
    common_telemetry = common_ref("telemetry", f"{stem}_telemetry.csv")
    common_summary = common_ref("telemetry", f"{stem}_summary.csv")
    set_path = run_output_root / "mt5" / f"{stem}.set"
    ini_path = run_output_root / "mt5" / f"{stem}.ini"
    primary_model_id = f"{RUN_ID}_tier_a_primary"
    fallback_model_id = f"{RUN_ID}_tier_b_fallback"
    set_payload = materialize_tester_set_file(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": TIER_AB,
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": split_name,
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpModelPath": common_primary_model,
            "InpModelId": primary_model_id,
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": common_primary_matrix,
            "InpFeatureCount": primary_feature_count,
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpFeatureStrictHeader": "true",
            "InpCsvTimestampIsBarClose": "true",
            "InpFeatureOrderHash": primary_feature_order_hash,
            "InpFallbackEnabled": "true" if fallback_enabled else "false",
            "InpFallbackTierLabel": "Tier B partial-context fallback",
            "InpFallbackFeatureCsvPath": common_fallback_matrix,
            "InpFallbackFeatureCount": fallback_feature_count,
            "InpFallbackModelPath": common_fallback_model,
            "InpFallbackModelId": fallback_model_id,
            "InpFallbackFeatureOrderHash": fallback_feature_order_hash,
            "InpTelemetryCsvPath": common_telemetry,
            "InpSummaryCsvPath": common_summary,
            "InpTelemetryUseCommonFiles": "true",
            "InpShortThreshold": rule.short_threshold,
            "InpLongThreshold": rule.long_threshold,
            "InpMinMargin": rule.min_margin,
            "InpInvertSignal": bool(invert_signal),
            "InpFallbackShortThreshold": fallback_rule.short_threshold,
            "InpFallbackLongThreshold": fallback_rule.long_threshold,
            "InpFallbackMinMargin": fallback_rule.min_margin,
            "InpFallbackInvertSignal": bool(fallback_invert_signal),
            "InpAllowTrading": "true",
            "InpFixedLot": 0.1,
            "InpMaxHoldBars": int(max_hold_bars),
            "InpMaxConcurrentPositions": 1,
            "InpMagic": 1001010,
        },
        set_path,
    )
    report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{stem}"
    ini_payload = materialize_tester_ini_file(
        TesterMaterializationConfig(from_date=from_date, to_date=to_date, report=report_name, shutdown_terminal=1),
        ini_path,
        set_file_path=Path(EA_TESTER_SET_NAME),
    )
    return {
        "tier": TIER_AB,
        "split": split_name,
        "routing_mode": routing_mode,
        "routing_detail": routing_detail,
        "fallback_enabled": bool(fallback_enabled),
        "set": set_payload,
        "ini": ini_payload,
        "common_model_path": common_primary_model,
        "common_feature_matrix_path": common_primary_matrix,
        "common_telemetry_path": common_telemetry,
        "common_summary_path": common_summary,
        "primary": {
            "tier": TIER_A,
            "model_id": primary_model_id,
            "common_model_path": common_primary_model,
            "common_feature_matrix_path": common_primary_matrix,
            "feature_count": primary_feature_count,
            "feature_order_hash": primary_feature_order_hash,
            "local_feature_matrix_path": primary_feature_matrix_path.as_posix(),
            "threshold_rule": threshold_rule_payload(rule),
            "invert_signal": bool(invert_signal),
        },
        "fallback": {
            "tier": TIER_B,
            "model_id": fallback_model_id,
            "common_model_path": common_fallback_model,
            "common_feature_matrix_path": common_fallback_matrix,
            "feature_count": fallback_feature_count,
            "feature_order_hash": fallback_feature_order_hash,
            "policy_id": TIER_B_PARTIAL_CONTEXT_POLICY_ID,
            "local_feature_matrix_path": fallback_feature_matrix_path.as_posix(),
            "threshold_rule": threshold_rule_payload(fallback_rule),
            "invert_signal": bool(fallback_invert_signal),
        },
        "threshold_rule": threshold_rule_payload(rule),
        "fallback_threshold_rule": threshold_rule_payload(fallback_rule),
        "invert_signal": bool(invert_signal),
        "fallback_invert_signal": bool(fallback_invert_signal),
        "max_hold_bars": int(max_hold_bars),
    }


def materialize_mt5_probe_bundle(
    *,
    run_output_root: Path,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    mt5_root: Path,
    tier_a_onnx_path: Path,
    tier_b_onnx_path: Path,
    tier_a_eval_frame: pd.DataFrame,
    tier_b_eval_frame: pd.DataFrame,
    tier_a_feature_order: Sequence[str],
    tier_b_feature_order: Sequence[str],
    tier_a_feature_hash: str,
    tier_b_feature_hash: str,
    tier_a_rule: ThresholdRule,
    tier_b_rule: ThresholdRule,
    route_coverage: Mapping[str, Any],
    routed_fallback_enabled: bool,
    attempt_mt5: bool,
    terminal_path: Path,
    metaeditor_path: Path,
    max_hold_bars: int = 12,
    tier_a_only_prefix: str = MT5_RECORD_TIER_A_ONLY_PREFIX,
    tier_b_fallback_only_prefix: str = MT5_RECORD_TIER_B_FALLBACK_ONLY_PREFIX,
) -> dict[str, Any]:
    split_specs = {
        "validation_is": ("validation", "2025.01.01", "2025.10.01"),
        "oos": ("oos", "2025.10.01", "2026.04.14"),
    }
    mt5_attempts: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    _io_path(mt5_root).mkdir(parents=True, exist_ok=True)
    common_copies.append(copy_to_common_files(common_files_root, tier_a_onnx_path, common_ref("models", tier_a_onnx_path.name)))
    common_copies.append(copy_to_common_files(common_files_root, tier_b_onnx_path, common_ref("models", tier_b_onnx_path.name)))

    for split_label, (source_split, from_date, to_date) in split_specs.items():
        tier_a_split = tier_a_eval_frame.loc[tier_a_eval_frame["split"].astype(str).eq(source_split)].copy()
        tier_b_split = tier_b_eval_frame.loc[tier_b_eval_frame["split"].astype(str).eq(source_split)].copy()
        tier_a_feature_matrix_path = mt5_root / f"tier_a_{split_label}_feature_matrix.csv"
        tier_b_feature_matrix_path = mt5_root / f"tier_b_{split_label}_feature_matrix.csv"
        tier_a_matrix_payload = export_mt5_feature_matrix_csv(
            tier_a_split,
            tier_a_feature_order,
            tier_a_feature_matrix_path,
            metadata_columns=("route_role", "partial_context_subtype", "missing_feature_group_mask", "available_feature_group_mask"),
        )
        tier_b_matrix_payload = export_mt5_feature_matrix_csv(
            tier_b_split,
            tier_b_feature_order,
            tier_b_feature_matrix_path,
            metadata_columns=("route_role", "partial_context_subtype", "missing_feature_group_mask", "available_feature_group_mask"),
        )
        common_copies.append(
            copy_to_common_files(common_files_root, tier_a_feature_matrix_path, common_ref("features", tier_a_feature_matrix_path.name))
        )
        common_copies.append(
            copy_to_common_files(common_files_root, tier_b_feature_matrix_path, common_ref("features", tier_b_feature_matrix_path.name))
        )
        tier_a_attempt = materialize_mt5_attempt_files(
            run_output_root=run_output_root,
            tier_name=TIER_A,
            split_name=split_label,
            local_onnx_path=tier_a_onnx_path,
            local_feature_matrix_path=tier_a_feature_matrix_path,
            feature_count=len(tier_a_feature_order),
            feature_order_hash=tier_a_feature_hash,
            rule=tier_a_rule,
            from_date=from_date,
            to_date=to_date,
            stem_prefix="tier_a_only",
            record_view_prefix=tier_a_only_prefix,
            primary_active_tier="tier_a",
            attempt_role="tier_only_total",
            max_hold_bars=max_hold_bars,
        )
        tier_a_attempt["feature_matrix"] = tier_a_matrix_payload
        mt5_attempts.append(tier_a_attempt)

        tier_b_attempt = materialize_mt5_attempt_files(
            run_output_root=run_output_root,
            tier_name=TIER_B,
            split_name=split_label,
            local_onnx_path=tier_b_onnx_path,
            local_feature_matrix_path=tier_b_feature_matrix_path,
            feature_count=len(tier_b_feature_order),
            feature_order_hash=tier_b_feature_hash,
            rule=tier_b_rule,
            from_date=from_date,
            to_date=to_date,
            stem_prefix="tier_b_fallback_only",
            record_view_prefix=tier_b_fallback_only_prefix,
            primary_active_tier="tier_b_fallback",
            attempt_role="tier_b_fallback_only_total",
            max_hold_bars=max_hold_bars,
        )
        tier_b_attempt["feature_matrix"] = tier_b_matrix_payload
        mt5_attempts.append(tier_b_attempt)

        routed_attempt = materialize_mt5_routed_attempt_files(
            run_output_root=run_output_root,
            split_name=split_label,
            primary_onnx_path=tier_a_onnx_path,
            primary_feature_matrix_path=tier_a_feature_matrix_path,
            primary_feature_count=len(tier_a_feature_order),
            primary_feature_order_hash=tier_a_feature_hash,
            fallback_onnx_path=tier_b_onnx_path,
            fallback_feature_matrix_path=tier_b_feature_matrix_path,
            fallback_feature_count=len(tier_b_feature_order),
            fallback_feature_order_hash=tier_b_feature_hash,
            rule=tier_a_rule,
            fallback_rule=tier_b_rule,
            max_hold_bars=max_hold_bars,
            fallback_enabled=routed_fallback_enabled,
            from_date=from_date,
            to_date=to_date,
        )
        routed_attempt["primary_feature_matrix"] = tier_a_matrix_payload
        routed_attempt["fallback_feature_matrix"] = tier_b_matrix_payload
        mt5_attempts.append(routed_attempt)

    compile_payload = None
    mt5_execution_results: list[dict[str, Any]] = []
    if attempt_mt5:
        for attempt in mt5_attempts:
            for common_output_key in ("common_telemetry_path", "common_summary_path"):
                output_path = common_files_root / Path(str(attempt[common_output_key]))
                if _path_exists(output_path):
                    _io_path(output_path).unlink()
            remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        compile_payload = compile_mql5_ea(metaeditor_path, EA_SOURCE_PATH, run_output_root / "mt5" / "mt5_compile.log")
        if compile_payload["status"] == "completed":
            for attempt in mt5_attempts:
                result = run_mt5_tester(
                    terminal_path,
                    Path(attempt["ini"]["path"]),
                    set_path=Path(attempt["set"]["path"]),
                    tester_profile_set_path=tester_profile_root / EA_TESTER_SET_NAME,
                    tester_profile_ini_path=tester_profile_root / mt5_short_profile_ini_name(attempt["tier"], attempt["split"]),
                )
                result["tier"] = attempt["tier"]
                result["split"] = attempt["split"]
                if "routing_mode" in attempt:
                    result["routing_mode"] = attempt["routing_mode"]
                if "attempt_role" in attempt:
                    result["attempt_role"] = attempt["attempt_role"]
                if "record_view_prefix" in attempt:
                    result["record_view_prefix"] = attempt["record_view_prefix"]
                result["ini_path"] = attempt["ini"]["path"]
                result["runtime_outputs"] = wait_for_mt5_runtime_outputs(common_files_root, attempt)
                if result["runtime_outputs"]["status"] != "completed":
                    result["status"] = "blocked"
                mt5_execution_results.append(result)

    mt5_report_records = (
        collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=run_output_root,
            attempts=mt5_attempts,
        )
        if attempt_mt5
        else []
    )
    attach_mt5_report_metrics(mt5_execution_results, mt5_report_records)
    mt5_kpi_records = build_mt5_kpi_records(mt5_execution_results)
    mt5_kpi_records = enrich_mt5_kpi_records_with_route_coverage(mt5_kpi_records, route_coverage)
    return {
        "mt5_attempts": mt5_attempts,
        "common_copies": common_copies,
        "compile_payload": compile_payload,
        "execution_results": mt5_execution_results,
        "report_records": mt5_report_records,
        "kpi_records": mt5_kpi_records,
        "module_hashes": mt5_runtime_module_hashes(),
    }


def report_name_from_attempt(attempt: Mapping[str, Any]) -> str:
    return mt5_artifacts.report_name_from_attempt(attempt, run_id=RUN_ID)


def remove_existing_mt5_report_artifacts(terminal_data_root: Path, attempt: Mapping[str, Any]) -> None:
    mt5_artifacts.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)


def collect_mt5_strategy_report_artifacts(
    *,
    terminal_data_root: Path,
    run_output_root: Path,
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    return mt5_artifacts.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=run_output_root,
        attempts=attempts,
        run_id=RUN_ID,
    )


def attach_mt5_report_metrics(
    execution_results: list[dict[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
) -> None:
    mt5_artifacts.attach_mt5_report_metrics(execution_results, report_records)
