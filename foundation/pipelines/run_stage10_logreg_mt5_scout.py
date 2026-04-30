from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.models.baseline_training import (  # noqa: E402
    BaselineTrainingConfig,
    load_feature_order,
    train_baseline_model,
)
from foundation.alpha.decision_views import (  # noqa: E402
    DECISION_CLASS_NO_TRADE,
    DECISION_LABEL_NO_TRADE,
    PROBABILITY_COLUMNS,
    REQUIRED_TIER_VIEWS,
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
    normalize_tier_label,
    probability_matrix,
    prediction_view_metrics,
    select_threshold_from_sweep,
    sweep_threshold_rules,
    threshold_id as _threshold_id,
    threshold_rule_from_values,
    threshold_rule_payload,
    validate_threshold_rule,
)
from foundation.alpha import scout_runner as alpha_scout_runner  # noqa: E402
from foundation.control_plane import alpha_run_ledgers  # noqa: E402
from foundation.control_plane import packet_writers  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path as _io_path,
    json_ready as _json_ready,
    ledger_pairs as _ledger_pairs,
    ledger_path as _ledger_path,
    ledger_status as _ledger_status,
    ledger_value as _ledger_value,
    path_exists as _path_exists,
    read_csv_rows as _read_csv_rows,
    upsert_csv_rows as _upsert_csv_rows,
    write_csv_rows as _write_csv_rows,
)
from foundation.control_plane.mt5_kpi_records import (  # noqa: E402
    ROUTING_MODE_A_B_FALLBACK,
    ROUTING_MODE_A_ONLY,
    build_mt5_kpi_records,
    enrich_mt5_kpi_records_with_route_coverage,
    mt5_metrics_with_runtime_counts,
    routed_component_metrics,
)
from foundation.control_plane.routing_coverage import (  # noqa: E402
    SESSION_SLICE_DEFINITIONS,
    apply_session_slice,
    build_eval_route_coverage_summary,
    session_slice_payload,
)
from foundation.control_plane.tier_context import (  # noqa: E402
    TIER_B_CONTEXT_GROUPS,
    TIER_B_PARTIAL_CONTEXT_SUBTYPES,
    apply_tier_b_fallback_subtype_filter,
    classify_tier_b_partial_context,
    normalize_tier_b_fallback_allowed_subtypes,
    parse_tier_b_fallback_allowed_subtypes,
)
from foundation.control_plane.tier_context_materialization import (  # noqa: E402
    ROUTE_ROLE_A_PRIMARY,
    ROUTE_ROLE_B_FALLBACK,
    ROUTE_ROLE_NO_TIER,
    TIER_B_CORE_FEATURE_ORDER,
    TIER_B_PARTIAL_CONTEXT_DATASET_ID,
    TIER_B_PARTIAL_CONTEXT_FEATURE_SET_ID,
    TIER_B_PARTIAL_CONTEXT_POLICY_ID,
    build_tier_b_partial_context_frames,
)
from foundation.models.onnx_bridge import (  # noqa: E402
    _find_probability_output,
    _onnx_output_shape,
    check_onnxruntime_probability_parity,
    classifier_classes,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
)
from foundation.mt5 import runtime_artifacts as mt5_artifacts  # noqa: E402
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics  # noqa: E402
from foundation.mt5.mql5_compile import compile_mql5_ea, metaeditor_command_log_path  # noqa: E402
from foundation.mt5.runtime_artifacts import (  # noqa: E402
    EA_EXPERT_PATH,
    EA_SOURCE_PATH,
    EA_TESTER_SET_NAME,
    copy_to_common_files,
    export_mt5_feature_matrix_csv,
    mt5_runtime_module_hashes,
    sha256_file,
    sha256_file_lf_normalized,
    validate_feature_matrix,
    write_json,
)
from foundation.mt5.terminal_runner import (  # noqa: E402
    run_mt5_tester,
    validate_mt5_runtime_outputs,
    wait_for_mt5_runtime_outputs,
)
from foundation.mt5.tester_files import (  # noqa: E402
    TesterMaterializationConfig,
    materialize_tester_ini_file,
    materialize_tester_set_file,
)


STAGE_ID = "10_alpha_scout__default_split_model_threshold_scan"
RUN_NUMBER = "run01A"
RUN_ID = "run01A_logreg_threshold_mt5_scout_v1"
EXPLORATION_LABEL = "stage10_Model__LogReg_MT5Scout"
MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
TIER_B_MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_feature_set_v1_no_placeholder_top3_weights"
TIER_B_FEATURE_SET_ID = "feature_set_v1_no_placeholder_top3_weight_features"
FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
DEFAULT_MODEL_INPUT_PATH = Path(
    "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
DEFAULT_FEATURE_ORDER_PATH = DEFAULT_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
DEFAULT_TIER_B_MODEL_INPUT_PATH = Path(
    "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1/model_input_dataset.parquet"
)
DEFAULT_TIER_B_FEATURE_ORDER_PATH = DEFAULT_TIER_B_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
DEFAULT_RAW_ROOT = Path("data/raw/mt5_bars/m5")
DEFAULT_TRAINING_SUMMARY_PATH = Path(
    "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"
)
DEFAULT_STAGE07_MODEL_PATH = Path(
    "stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/"
    "20260425_stage07_baseline_training_smoke_v1/model.joblib"
)
DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
STAGE_RUN_LEDGER_PATH = Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
DEFAULT_COMMON_FILES_ROOT = Path.home() / "AppData/Roaming/MetaQuotes/Terminal/Common/Files"
DEFAULT_TERMINAL_DATA_ROOT = REPO_ROOT.parents[2]
DEFAULT_TESTER_PROFILE_ROOT = REPO_ROOT.parents[1] / "Profiles" / "Tester"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/stage10/run01A_logreg_threshold_mt5_scout_v1"
MT5_RECORD_TIER_A_ONLY_PREFIX = "mt5_tier_a_only"
MT5_RECORD_TIER_B_FALLBACK_ONLY_PREFIX = "mt5_tier_b_fallback_only"


def default_common_run_root(run_id: str) -> str:
    return f"Project_Obsidian_Prime_v2/stage10/{run_id}"


def configure_run_identity(
    *,
    run_number: str,
    run_id: str,
    exploration_label: str,
    common_run_root: str | None = None,
) -> None:
    global RUN_NUMBER, RUN_ID, EXPLORATION_LABEL, DEFAULT_RUN_OUTPUT_ROOT, COMMON_RUN_ROOT

    RUN_NUMBER = run_number
    RUN_ID = run_id
    EXPLORATION_LABEL = exploration_label
    DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
    COMMON_RUN_ROOT = common_run_root or default_common_run_root(run_id)
    alpha_scout_runner.configure_run_identity(
        run_number=RUN_NUMBER,
        run_id=RUN_ID,
        exploration_label=EXPLORATION_LABEL,
        common_run_root=COMMON_RUN_ROOT,
        stage_id=STAGE_ID,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize a Stage 10 logistic MT5 scout payload.")
    parser.add_argument("--run-number", default=RUN_NUMBER)
    parser.add_argument("--run-id", default=RUN_ID)
    parser.add_argument("--exploration-label", default=EXPLORATION_LABEL)
    parser.add_argument("--common-run-root", default=None)
    parser.add_argument("--model-input-path", default=str(DEFAULT_MODEL_INPUT_PATH))
    parser.add_argument("--feature-order-path", default=str(DEFAULT_FEATURE_ORDER_PATH))
    parser.add_argument("--tier-b-model-input-path", default=str(DEFAULT_TIER_B_MODEL_INPUT_PATH))
    parser.add_argument("--tier-b-feature-order-path", default=str(DEFAULT_TIER_B_FEATURE_ORDER_PATH))
    parser.add_argument("--raw-root", default=str(DEFAULT_RAW_ROOT))
    parser.add_argument("--training-summary-path", default=str(DEFAULT_TRAINING_SUMMARY_PATH))
    parser.add_argument("--stage07-model-path", default=str(DEFAULT_STAGE07_MODEL_PATH))
    parser.add_argument("--run-output-root", default=None)
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--tier-column", default=TIER_COLUMN)
    parser.add_argument("--random-seed", type=int, default=10)
    parser.add_argument("--max-iter", type=int, default=2000)
    parser.add_argument("--parity-rows", type=int, default=128)
    parser.add_argument("--max-hold-bars", type=int, default=12)
    parser.add_argument("--tier-a-threshold-id", default=None)
    parser.add_argument("--tier-a-short-threshold", type=float, default=None)
    parser.add_argument("--tier-a-long-threshold", type=float, default=None)
    parser.add_argument("--tier-a-min-margin", type=float, default=None)
    parser.add_argument("--tier-b-threshold-id", default=None)
    parser.add_argument("--tier-b-short-threshold", type=float, default=None)
    parser.add_argument("--tier-b-long-threshold", type=float, default=None)
    parser.add_argument("--tier-b-min-margin", type=float, default=None)
    parser.add_argument("--disable-routed-fallback", action="store_true")
    parser.add_argument("--tier-b-fallback-allowed-subtypes", default=None)
    parser.add_argument("--session-slice-id", choices=sorted(SESSION_SLICE_DEFINITIONS), default=None)
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args()


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


common_ref = alpha_scout_runner.common_ref
mt5_short_profile_ini_name = alpha_scout_runner.mt5_short_profile_ini_name
materialize_mt5_attempt_files = alpha_scout_runner.materialize_mt5_attempt_files
materialize_mt5_routed_attempt_files = alpha_scout_runner.materialize_mt5_routed_attempt_files
report_name_from_attempt = alpha_scout_runner.report_name_from_attempt
remove_existing_mt5_report_artifacts = alpha_scout_runner.remove_existing_mt5_report_artifacts
collect_mt5_strategy_report_artifacts = alpha_scout_runner.collect_mt5_strategy_report_artifacts
attach_mt5_report_metrics = alpha_scout_runner.attach_mt5_report_metrics

def build_alpha_ledger_rows(
    *,
    tier_records: Sequence[Mapping[str, Any]],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    selected_threshold_id: str,
    run_output_root: Path,
    external_verification_status: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for record in tier_records:
        record_view = str(record.get("record_view"))
        metrics = record.get("metrics", {})
        row_view = f"python_{record_view}"
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{row_view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": row_view,
                "parent_run_id": RUN_ID,
                "record_view": row_view,
                "tier_scope": str(record.get("tier_scope")),
                "kpi_scope": "signal_probability_threshold",
                "scoreboard_lane": "structural_scout",
                "status": _ledger_status(record.get("status")),
                "judgment": "inconclusive_single_split_scout_payload",
                "path": _ledger_path(record.get("path")),
                "primary_kpi": _ledger_pairs(
                    (
                        ("rows", metrics.get("rows")),
                        ("signal_coverage", metrics.get("signal_coverage")),
                        ("signal_count", metrics.get("signal_count")),
                        ("short", metrics.get("short_count")),
                        ("long", metrics.get("long_count")),
                    )
                ),
                "guardrail_kpi": _ledger_pairs(
                    (
                        ("prob_sum_err", metrics.get("probability_row_sum_max_abs_error")),
                        ("selected_threshold", selected_threshold_id),
                        ("threshold_ids", metrics.get("threshold_ids")),
                        ("subtype_counts", metrics.get("partial_context_subtype_counts")),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim",
                "notes": (
                    "Tier B partial-context fallback-only view"
                    if record.get("tier_scope") == TIER_B
                    else "Tier A primary plus Tier B fallback routed Python view"
                    if record.get("tier_scope") == TIER_AB
                    else "Tier A full-context primary view"
                ),
            }
        )

    rows.extend(
        alpha_run_ledgers.build_mt5_alpha_ledger_rows(
            run_id=RUN_ID,
            stage_id=STAGE_ID,
            mt5_kpi_records=mt5_kpi_records,
            run_output_root=run_output_root,
            external_verification_status=external_verification_status,
            tier_b=TIER_B,
        )
    )
    return rows

def materialize_alpha_ledgers(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return alpha_run_ledgers.materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_RUN_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_ALPHA_LEDGER_PATH,
        rows=rows,
    )


def materialize_run_registry_row(
    *,
    route_coverage: Mapping[str, Any],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    run_output_root: Path,
    external_verification_status: str,
    routing_mode: str = ROUTING_MODE_A_B_FALLBACK,
) -> dict[str, Any]:
    by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in mt5_kpi_records}
    validation = by_view.get("mt5_routed_total_validation_is", {})
    oos = by_view.get("mt5_routed_total_oos", {})
    a_validation = by_view.get(f"{MT5_RECORD_TIER_A_ONLY_PREFIX}_validation_is", {})
    a_oos = by_view.get(f"{MT5_RECORD_TIER_A_ONLY_PREFIX}_oos", {})
    b_validation = by_view.get(f"{MT5_RECORD_TIER_B_FALLBACK_ONLY_PREFIX}_validation_is", {})
    b_oos = by_view.get(f"{MT5_RECORD_TIER_B_FALLBACK_ONLY_PREFIX}_oos", {})
    mt5_views = (
        "tier_a_only;tier_b_fallback_only;tier_a_primary_no_fallback"
        if routing_mode == ROUTING_MODE_A_ONLY
        else "tier_a_only;tier_b_fallback_only;tier_a_primary_tier_b_fallback"
    )
    notes = _ledger_pairs(
        (
            ("mt5_views", mt5_views),
            ("routing_mode", routing_mode),
            ("tier_b_fallback_rows", route_coverage.get("tier_b_fallback_rows")),
            ("tier_b_fallback_allowed_subtypes", route_coverage.get("tier_b_fallback_allowed_subtypes")),
            ("tier_b_fallback_filtered_out_rows", route_coverage.get("tier_b_fallback_filtered_out_rows")),
            ("no_tier_labelable_rows", route_coverage.get("no_tier_labelable_rows")),
            ("validation_a_only_net_profit", a_validation.get("net_profit")),
            ("validation_a_only_pf", a_validation.get("profit_factor")),
            ("validation_b_only_net_profit", b_validation.get("net_profit")),
            ("validation_b_only_pf", b_validation.get("profit_factor")),
            ("validation_net_profit", validation.get("net_profit")),
            ("validation_pf", validation.get("profit_factor")),
            ("validation_b_fallback_used", validation.get("tier_b_fallback_used_count")),
            ("oos_a_only_net_profit", a_oos.get("net_profit")),
            ("oos_a_only_pf", a_oos.get("profit_factor")),
            ("oos_b_only_net_profit", b_oos.get("net_profit")),
            ("oos_b_only_pf", b_oos.get("profit_factor")),
            ("oos_net_profit", oos.get("net_profit")),
            ("oos_pf", oos.get("profit_factor")),
            ("oos_b_fallback_used", oos.get("tier_b_fallback_used_count")),
            ("external_verification", external_verification_status),
            ("boundary", "runtime_probe_only"),
        )
    )
    row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if external_verification_status == "completed" else "payload_only",
        "judgment": "inconclusive_single_split_scout_mt5_routed_completed"
        if external_verification_status == "completed"
        else "inconclusive_single_split_scout_payload",
        "path": run_output_root.as_posix(),
        "notes": notes,
    }
    return _upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [row], key="run_id")



def build_run_manifest_payload(
    *,
    run_id: str,
    run_number: str,
    stage_id: str,
    exploration_label: str,
    input_refs: Mapping[str, Any],
    artifacts: Sequence[Mapping[str, Any]],
    threshold_selection: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    onnx_parity: Mapping[str, Any],
    external_verification_status: str = "out_of_scope_by_claim",
) -> dict[str, Any]:
    return {
        "identity": {
            "run_id": run_id,
            "run_number": run_number,
            "stage_id": stage_id,
            "exploration_label": exploration_label,
            "lane": "single_split_scout",
            "scoreboard_lane": "structural_scout",
            "model_family": "sklearn_logistic_regression_multiclass",
        },
        "inputs": dict(input_refs),
        "artifacts": list(artifacts),
        "threshold": dict(threshold_selection),
        "tier_pair_records": list(tier_records),
        "onnx_probability_parity": dict(onnx_parity),
        "external_verification_status": external_verification_status,
        "judgment_boundary": {
            "status": "payload_generated_not_reviewed",
            "claim": "single_split_scout_payload_only",
            "not_claimed": [
                "alpha_quality",
                "live_readiness",
                "runtime_authority_expansion",
                "operating_promotion",
            ],
        },
    }


def build_kpi_record_payload(
    *,
    run_id: str,
    stage_id: str,
    threshold_sweep: pd.DataFrame,
    threshold_sweeps: Mapping[str, pd.DataFrame] | None = None,
    tier_records: Sequence[Mapping[str, Any]],
    onnx_parity: Mapping[str, Any],
    mt5_kpi_records: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    best = select_threshold_from_sweep(threshold_sweep) if not threshold_sweep.empty else {}
    mt5_kpi_records = list(mt5_kpi_records or [])
    return {
        "run_id": run_id,
        "stage_id": stage_id,
        "scoreboard_lane": "runtime_probe",
        "kpi_scope": "signal_probability_threshold_trading_risk_execution",
        "signal": {
            "tier_pair_records": [
                {
                    "record_view": record.get("record_view"),
                    "tier_scope": record.get("tier_scope"),
                    "signal_count": record.get("metrics", {}).get("signal_count"),
                    "short_count": record.get("metrics", {}).get("short_count"),
                    "long_count": record.get("metrics", {}).get("long_count"),
                    "signal_coverage": record.get("metrics", {}).get("signal_coverage"),
                }
                for record in tier_records
            ],
        },
        "probability": {
            "onnx_probability_parity_passed": onnx_parity.get("passed"),
            "onnx_probability_max_abs_diff": onnx_parity.get("max_abs_diff"),
            "row_sum_guardrail": [
                {
                    "record_view": record.get("record_view"),
                    "tier_scope": record.get("tier_scope"),
                    "probability_row_sum_max_abs_error": record.get("metrics", {}).get("probability_row_sum_max_abs_error"),
                }
                for record in tier_records
            ],
        },
        "threshold": {
            "selection_scope": "validation_is_routed_tier_a_primary_tier_b_fallback_only",
            "selected_threshold_id": best.get("threshold_id"),
            "directional_hit_rate": best.get("directional_hit_rate"),
            "coverage": best.get("coverage"),
            "sweeps": {
                view: {
                    "rows": int(len(sweep)),
                    "best": select_threshold_from_sweep(sweep) if not sweep.empty else {},
                }
                for view, sweep in (threshold_sweeps or {"tier_ab_combined": threshold_sweep}).items()
            },
        },
        "routing": {
            "routing_mode": "tier_a_primary_tier_b_fallback",
            "primary_tier": TIER_A,
            "fallback_tier": TIER_B,
            "route_source_required": True,
            "fallback_reason_required": True,
            "records": [
                {
                    "record_view": record.get("record_view"),
                    "tier_scope": record.get("tier_scope"),
                    "split": record.get("split"),
                    "route_role": record.get("route_role"),
                    "aggregation": record.get("metrics", {}).get("aggregation"),
                    "profit_attribution": record.get("metrics", {}).get("profit_attribution"),
                    "route_bar_count": record.get("metrics", {}).get("route_bar_count"),
                    "route_share": record.get("metrics", {}).get("route_share"),
                    "partial_context_subtype_counts": record.get("metrics", {}).get("partial_context_subtype_counts"),
                    "no_tier_labelable_rows": record.get("metrics", {}).get("no_tier_labelable_rows"),
                    "routed_labelable_rows": record.get("metrics", {}).get("routed_labelable_rows"),
                }
                for record in mt5_kpi_records
            ],
        },
        "trading": [
            {
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "net_profit": record.get("metrics", {}).get("net_profit"),
                "profit_factor": record.get("metrics", {}).get("profit_factor"),
                "expectancy": record.get("metrics", {}).get("expectancy"),
                "trade_count": record.get("metrics", {}).get("trade_count"),
                "win_rate_percent": record.get("metrics", {}).get("win_rate_percent"),
            }
            for record in mt5_kpi_records
        ],
        "risk": [
            {
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "max_drawdown_amount": record.get("metrics", {}).get("max_drawdown_amount"),
                "max_drawdown_percent": record.get("metrics", {}).get("max_drawdown_percent"),
                "recovery_factor": record.get("metrics", {}).get("recovery_factor"),
            }
            for record in mt5_kpi_records
        ],
        "execution": [
            {
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "fill_count": record.get("metrics", {}).get("fill_count"),
                "reject_count": record.get("metrics", {}).get("reject_count"),
                "skip_count": record.get("metrics", {}).get("skip_count"),
                "fill_rate": record.get("metrics", {}).get("fill_rate"),
            }
            for record in mt5_kpi_records
        ],
        "judgment_read": {
            "judgment": "inconclusive_single_split_scout_mt5_routed_completed" if mt5_kpi_records else "inconclusive_payload_only",
            "boundary": "runtime_probe only; not live readiness, runtime authority expansion, or operating promotion.",
            "mt5_record_count": len(mt5_kpi_records),
        },
        "tier_pair_records": list(tier_records),
    }


def materialize_manifest_and_kpi(
    output_root: Path,
    *,
    manifest_payload: Mapping[str, Any],
    kpi_payload: Mapping[str, Any],
) -> dict[str, Any]:
    return packet_writers.materialize_manifest_and_kpi(
        output_root,
        manifest_payload=manifest_payload,
        kpi_payload=kpi_payload,
    )


def run_stage10_logreg_mt5_scout(
    *,
    model_input_path: Path,
    feature_order_path: Path,
    tier_b_model_input_path: Path,
    tier_b_feature_order_path: Path,
    raw_root: Path,
    training_summary_path: Path,
    stage07_model_path: Path,
    run_output_root: Path,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    tier_column: str = TIER_COLUMN,
    random_seed: int = 10,
    max_iter: int = 2000,
    parity_rows: int = 128,
    max_hold_bars: int = 12,
    tier_a_threshold_rule: ThresholdRule | None = None,
    tier_b_threshold_rule: ThresholdRule | None = None,
    routed_fallback_enabled: bool = True,
    session_slice_id: str | None = None,
    tier_b_fallback_allowed_subtypes: Sequence[str] | None = None,
    attempt_mt5: bool = False,
    terminal_path: Path = Path(r"C:\Program Files\MetaTrader 5\terminal64.exe"),
    metaeditor_path: Path = Path(r"C:\Program Files\MetaTrader 5\MetaEditor64.exe"),
) -> dict[str, Any]:
    routing_mode = ROUTING_MODE_A_B_FALLBACK if routed_fallback_enabled else ROUTING_MODE_A_ONLY
    routing_detail = (
        "tier_a_primary_tier_b_partial_context_fallback"
        if routed_fallback_enabled
        else "tier_a_primary_no_fallback"
    )
    session_slice = session_slice_payload(session_slice_id)
    allowed_fallback_subtypes = normalize_tier_b_fallback_allowed_subtypes(tier_b_fallback_allowed_subtypes)
    tier_a_feature_order = load_feature_order(feature_order_path)
    tier_a_feature_hash = ordered_hash(tier_a_feature_order)
    if tier_a_feature_hash != FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {tier_a_feature_hash} != {FEATURE_ORDER_HASH}")

    stage04_tier_b_feature_order = load_feature_order(tier_b_feature_order_path)
    tier_b_feature_order = list(TIER_B_CORE_FEATURE_ORDER)
    missing_core_features = sorted(set(tier_b_feature_order).difference(stage04_tier_b_feature_order))
    if missing_core_features:
        raise RuntimeError(f"Tier B core feature order is missing Stage04 reference features: {missing_core_features}")
    tier_b_feature_hash = ordered_hash(tier_b_feature_order)
    label_threshold = load_label_threshold(training_summary_path)

    tier_a_frame = pd.read_parquet(_io_path(model_input_path))
    tier_a_frame["timestamp"] = pd.to_datetime(tier_a_frame["timestamp"], utc=True)
    tier_a_frame["route_role"] = ROUTE_ROLE_A_PRIMARY
    tier_a_frame["partial_context_subtype"] = "Tier_A_full_context"
    tier_a_frame["missing_feature_group_mask"] = "none"
    tier_a_frame["available_feature_group_mask"] = "macro|constituent|basket"
    tier_a_frame["tier_a_primary_available"] = True
    tier_a_frame["tier_a_full_feature_ready"] = True
    tier_a_frame["tier_b_core_ready"] = True
    tier_b_context = build_tier_b_partial_context_frames(
        raw_root=raw_root,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=label_threshold,
    )
    tier_b_training_frame = tier_b_context["tier_b_training_frame"]
    tier_b_frame = tier_b_context["tier_b_fallback_frame"]
    no_tier_frame = tier_b_context["no_tier_frame"]
    route_coverage = tier_b_context["summary"]
    config = BaselineTrainingConfig(random_seed=random_seed, max_iter=max_iter)
    tier_a_model = joblib.load(_io_path(stage07_model_path))
    tier_b_model = train_baseline_model(tier_b_training_frame, list(tier_b_feature_order), config)

    _io_path(run_output_root).mkdir(parents=True, exist_ok=True)
    models_root = run_output_root / "models"
    predictions_root = run_output_root / "predictions"
    sweeps_root = run_output_root / "sweeps"
    mt5_root = run_output_root / "mt5"
    reports_root = run_output_root / "reports"

    tier_a_model_path = models_root / "tier_a_stage07_model.joblib"
    tier_b_model_path = models_root / "tier_b_logreg_core42_model.joblib"
    tier_b_feature_order_path_run = models_root / "tier_b_core42_feature_order.txt"
    tier_a_predictions_path = predictions_root / "tier_a_predictions.parquet"
    tier_b_predictions_path = predictions_root / "tier_b_predictions.parquet"
    no_tier_route_path = predictions_root / "no_tier_route_rows.parquet"
    route_coverage_path = predictions_root / "route_coverage_summary.json"
    combined_predictions_path = predictions_root / "tier_ab_combined_predictions.parquet"
    threshold_sweep_path = sweeps_root / "threshold_sweep_validation_combined.csv"
    tier_a_onnx_path = models_root / "tier_a_stage07_logreg.onnx"
    tier_b_onnx_path = models_root / "tier_b_logreg_core42_partial_context.onnx"

    validation_a = tier_a_frame.loc[tier_a_frame["split"].astype(str).eq("validation")].copy()
    validation_b = tier_b_frame.loc[tier_b_frame["split"].astype(str).eq("validation")].copy()
    values_a = validation_a.loc[:, list(tier_a_feature_order)].to_numpy(dtype="float64", copy=False)
    values_b = validation_b.loc[:, list(tier_b_feature_order)].to_numpy(dtype="float64", copy=False)
    validation_probabilities = np.vstack(
        [
            ordered_sklearn_probabilities(tier_a_model, values_a),
            ordered_sklearn_probabilities(tier_b_model, values_b),
        ]
    )
    validation_labels = np.concatenate(
        [
            validation_a["label_class"].astype("int64").to_numpy(),
            validation_b["label_class"].astype("int64").to_numpy(),
        ]
    )
    threshold_sweeps = {
        "tier_a_separate": sweep_threshold_rules(
            ordered_sklearn_probabilities(tier_a_model, values_a),
            validation_a["label_class"].astype("int64").to_numpy(),
        ),
        "tier_b_separate": sweep_threshold_rules(
            ordered_sklearn_probabilities(tier_b_model, values_b),
            validation_b["label_class"].astype("int64").to_numpy(),
        ),
        "tier_ab_combined": sweep_threshold_rules(
            validation_probabilities,
            validation_labels,
        ),
    }
    _io_path(sweeps_root).mkdir(parents=True, exist_ok=True)
    threshold_sweep_paths = {
        "tier_a_separate": sweeps_root / "threshold_sweep_validation_tier_a.csv",
        "tier_b_separate": sweeps_root / "threshold_sweep_validation_tier_b.csv",
        "tier_ab_combined": threshold_sweep_path,
    }
    for view_name, sweep in threshold_sweeps.items():
        sweep.to_csv(_io_path(threshold_sweep_paths[view_name]), index=False)
    threshold_sweep = threshold_sweeps["tier_ab_combined"]
    selected = select_threshold_from_sweep(threshold_sweep)
    selected_sweep_rule = ThresholdRule(
        threshold_id=str(selected["threshold_id"]),
        short_threshold=float(selected["short_threshold"]),
        long_threshold=float(selected["long_threshold"]),
        min_margin=float(selected["min_margin"]),
    )
    tier_a_rule = tier_a_threshold_rule or selected_sweep_rule
    tier_b_rule = tier_b_threshold_rule or tier_a_rule
    rule = tier_a_rule
    threshold_selection = dict(selected)
    threshold_selection.update(
        {
            "selection_source": "explicit_override" if tier_a_threshold_rule or tier_b_threshold_rule else "validation_combined_sweep",
            "threshold_id": (
                (
                    f"a_{tier_a_rule.threshold_id}__b_{tier_b_rule.threshold_id}__hold{int(max_hold_bars)}"
                    if routed_fallback_enabled
                    else f"a_{tier_a_rule.threshold_id}__b_disabled__hold{int(max_hold_bars)}"
                )
                + (f"__slice_{session_slice_id}" if session_slice_id else "")
                + (
                    "__bsub_" + "_".join(re.sub(r"[^A-Za-z0-9]+", "", subtype) for subtype in allowed_fallback_subtypes)
                    if allowed_fallback_subtypes
                    else ""
                )
            ),
            "selected_combined_sweep_rule": threshold_rule_payload(selected_sweep_rule),
            "tier_a_rule": threshold_rule_payload(tier_a_rule),
            "tier_b_fallback_rule": threshold_rule_payload(tier_b_rule),
            "routed_fallback_enabled": bool(routed_fallback_enabled),
            "session_slice": session_slice,
            "tier_b_fallback_allowed_subtypes": list(allowed_fallback_subtypes) if allowed_fallback_subtypes else None,
            "max_hold_bars": int(max_hold_bars),
            "short_threshold": tier_a_rule.short_threshold,
            "long_threshold": tier_a_rule.long_threshold,
            "min_margin": tier_a_rule.min_margin,
        }
    )

    tier_a_eval_frame = apply_session_slice(tier_a_frame, session_slice)
    tier_b_eval_frame_unfiltered = apply_session_slice(tier_b_frame, session_slice)
    tier_b_eval_frame, tier_b_filtered_out_frame = apply_tier_b_fallback_subtype_filter(
        tier_b_eval_frame_unfiltered,
        allowed_fallback_subtypes,
    )
    no_tier_eval_frame_base = apply_session_slice(no_tier_frame, session_slice)
    no_tier_eval_frame = (
        pd.concat([no_tier_eval_frame_base, tier_b_filtered_out_frame], ignore_index=True, sort=False)
        if not tier_b_filtered_out_frame.empty
        else no_tier_eval_frame_base
    )
    if tier_a_eval_frame.empty:
        raise RuntimeError(f"Tier A evaluation frame is empty for session slice: {session_slice_id}")
    route_coverage = build_eval_route_coverage_summary(
        base_summary=route_coverage,
        tier_a_eval_frame=tier_a_eval_frame,
        tier_b_eval_frame=tier_b_eval_frame,
        no_tier_eval_frame=no_tier_eval_frame,
        session_slice=session_slice,
        tier_b_filtered_out_frame=tier_b_filtered_out_frame,
        tier_b_allowed_subtypes=allowed_fallback_subtypes,
    )

    tier_a_predictions = build_prediction_frame(tier_a_model, tier_a_eval_frame, tier_a_feature_order, tier_a_rule)
    tier_b_predictions = build_prediction_frame(tier_b_model, tier_b_eval_frame, tier_b_feature_order, tier_b_rule)
    tier_a_predictions[tier_column] = TIER_A
    tier_b_predictions[tier_column] = TIER_B
    tier_a_predictions["feature_count"] = len(tier_a_feature_order)
    tier_b_predictions["feature_count"] = len(tier_b_feature_order)
    tier_a_predictions["feature_order_hash"] = tier_a_feature_hash
    tier_b_predictions["feature_order_hash"] = tier_b_feature_hash
    predictions = pd.concat([tier_a_predictions, tier_b_predictions], ignore_index=True)
    _io_path(predictions_root).mkdir(parents=True, exist_ok=True)
    tier_a_predictions.to_parquet(_io_path(tier_a_predictions_path), index=False)
    tier_b_predictions.to_parquet(_io_path(tier_b_predictions_path), index=False)
    no_tier_eval_frame.to_parquet(_io_path(no_tier_route_path), index=False)
    predictions.to_parquet(_io_path(combined_predictions_path), index=False)
    write_json(route_coverage_path, route_coverage)

    tier_views = build_tier_prediction_views(predictions, tier_column=tier_column)
    tier_outputs = materialize_tier_prediction_views(tier_views, predictions_root)
    tier_records = build_paired_tier_records(tier_views, base_path=predictions_root)

    _io_path(models_root).mkdir(parents=True, exist_ok=True)
    _io_path(tier_b_feature_order_path_run).write_text("\n".join(tier_b_feature_order) + "\n", encoding="utf-8")
    joblib.dump(tier_a_model, _io_path(tier_a_model_path))
    joblib.dump(tier_b_model, _io_path(tier_b_model_path))
    tier_a_onnx_export = export_sklearn_to_onnx_zipmap_disabled(
        tier_a_model, tier_a_onnx_path, feature_count=len(tier_a_feature_order)
    )
    tier_b_onnx_export = export_sklearn_to_onnx_zipmap_disabled(
        tier_b_model, tier_b_onnx_path, feature_count=len(tier_b_feature_order)
    )
    tier_a_parity_values = values_a[: max(1, min(parity_rows, len(values_a)))]
    tier_b_parity_values = values_b[: max(1, min(parity_rows, len(values_b)))]
    tier_a_onnx_parity = check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx_path, tier_a_parity_values)
    tier_b_onnx_parity = check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx_path, tier_b_parity_values)
    onnx_parity = {
        "passed": bool(tier_a_onnx_parity["passed"] and tier_b_onnx_parity["passed"]),
        "tier_a": tier_a_onnx_parity,
        "tier_b": tier_b_onnx_parity,
    }

    split_specs = {
        "validation_is": ("validation", "2025.01.01", "2025.10.01"),
        "oos": ("oos", "2025.10.01", "2026.04.14"),
    }
    mt5_attempts: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    _io_path(mt5_root).mkdir(parents=True, exist_ok=True)
    common_copies.append(copy_to_common_files(common_files_root, tier_a_onnx_path, common_ref("models", tier_a_onnx_path.name)))
    common_copies.append(copy_to_common_files(common_files_root, tier_b_onnx_path, common_ref("models", tier_b_onnx_path.name)))

    mt5_feature_matrices: dict[tuple[str, str], dict[str, Any]] = {}
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
        mt5_feature_matrices[(TIER_A, split_label)] = tier_a_matrix_payload
        mt5_feature_matrices[(TIER_B, split_label)] = tier_b_matrix_payload
        tier_a_attempt = materialize_mt5_attempt_files(
            run_output_root=run_output_root,
            tier_name=TIER_A,
            split_name=split_label,
            local_onnx_path=tier_a_onnx_path,
            local_feature_matrix_path=tier_a_feature_matrix_path,
            feature_count=len(tier_a_feature_order),
            feature_order_hash=tier_a_feature_hash,
            rule=rule,
            from_date=from_date,
            to_date=to_date,
            stem_prefix="tier_a_only",
            record_view_prefix=MT5_RECORD_TIER_A_ONLY_PREFIX,
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
            record_view_prefix=MT5_RECORD_TIER_B_FALLBACK_ONLY_PREFIX,
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
            rule=rule,
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

    mt5_report_records = collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=run_output_root,
        attempts=mt5_attempts,
    ) if attempt_mt5 else []
    attach_mt5_report_metrics(mt5_execution_results, mt5_report_records)
    mt5_kpi_records = build_mt5_kpi_records(mt5_execution_results)
    mt5_kpi_records = enrich_mt5_kpi_records_with_route_coverage(mt5_kpi_records, route_coverage)
    mt5_module_hashes = mt5_runtime_module_hashes()

    artifacts = [
        {"role": "tier_a_sklearn_model", "path": tier_a_model_path.as_posix(), "format": "joblib", "sha256": sha256_file(tier_a_model_path)},
        {"role": "tier_b_sklearn_model", "path": tier_b_model_path.as_posix(), "format": "joblib", "sha256": sha256_file(tier_b_model_path)},
        {"role": "tier_a_predictions", "path": tier_a_predictions_path.as_posix(), "format": "parquet", "sha256": sha256_file(tier_a_predictions_path)},
        {"role": "tier_b_predictions", "path": tier_b_predictions_path.as_posix(), "format": "parquet", "sha256": sha256_file(tier_b_predictions_path)},
        {"role": "no_tier_route_rows", "path": no_tier_route_path.as_posix(), "format": "parquet", "sha256": sha256_file(no_tier_route_path)},
        {"role": "route_coverage_summary", "path": route_coverage_path.as_posix(), "format": "json", "sha256": sha256_file(route_coverage_path)},
        {"role": "combined_predictions", "path": combined_predictions_path.as_posix(), "format": "parquet", "sha256": sha256_file(combined_predictions_path)},
        {"role": "tier_b_core42_feature_order", "path": tier_b_feature_order_path_run.as_posix(), "format": "txt", "sha256": sha256_file(tier_b_feature_order_path_run)},
        {"role": "threshold_sweep", "path": threshold_sweep_path.as_posix(), "format": "csv", "sha256": sha256_file(threshold_sweep_path)},
        *[
            {
                "role": f"threshold_sweep_{view_name}",
                "path": path.as_posix(),
                "format": "csv",
                "sha256": sha256_file(path),
            }
            for view_name, path in threshold_sweep_paths.items()
        ],
        {"role": "tier_a_onnx_model", **tier_a_onnx_export, "format": "onnx"},
        {"role": "tier_b_onnx_model", **tier_b_onnx_export, "format": "onnx"},
        {"role": "mt5_attempts", "attempts": mt5_attempts},
        {"role": "mt5_common_file_copies", "copies": common_copies},
        {"role": "mt5_runtime_module_hashes", "modules": mt5_module_hashes},
        {"role": "mt5_strategy_tester_reports", "reports": mt5_report_records},
        {"role": "tier_prediction_views", "views": tier_outputs},
    ]
    input_refs = {
        "tier_a": {
            "model_input_dataset_id": MODEL_INPUT_DATASET_ID,
            "feature_set_id": FEATURE_SET_ID,
            "model_input_path": model_input_path.as_posix(),
            "model_input_sha256": sha256_file(model_input_path),
            "feature_order_path": feature_order_path.as_posix(),
            "feature_order_sha256": sha256_file(feature_order_path),
            "feature_count": len(tier_a_feature_order),
            "feature_order_hash": tier_a_feature_hash,
            "source_model_path": stage07_model_path.as_posix(),
            "source_model_sha256": sha256_file(stage07_model_path),
        },
        "tier_b": {
            "model_input_dataset_id": TIER_B_PARTIAL_CONTEXT_DATASET_ID,
            "feature_set_id": TIER_B_PARTIAL_CONTEXT_FEATURE_SET_ID,
            "model_input_path": "materialized_in_run_from_raw_feature_frame_and_label_contract",
            "model_input_sha256": None,
            "feature_order_path": tier_b_feature_order_path_run.as_posix(),
            "feature_order_sha256": sha256_file(tier_b_feature_order_path_run),
            "feature_count": len(tier_b_feature_order),
            "feature_order_hash": tier_b_feature_hash,
            "policy_id": TIER_B_PARTIAL_CONTEXT_POLICY_ID,
            "boundary": "partial-context fallback surface; Stage04 56-feature quarantine artifact is a reference only",
            "route_coverage": route_coverage,
            "stage04_quarantine_reference": {
                "model_input_dataset_id": TIER_B_MODEL_INPUT_DATASET_ID,
                "feature_set_id": TIER_B_FEATURE_SET_ID,
                "model_input_path": tier_b_model_input_path.as_posix(),
                "model_input_sha256": sha256_file(tier_b_model_input_path),
                "feature_order_path": tier_b_feature_order_path.as_posix(),
                "feature_order_sha256": sha256_file(tier_b_feature_order_path),
            },
        },
    }
    expected_mt5_kpi_record_count = sum(
        3 if attempt.get("routing_mode") == "tier_a_primary_tier_b_fallback" else 1 for attempt in mt5_attempts
    )
    mt5_runtime_completed = bool(mt5_execution_results) and all(item["status"] == "completed" for item in mt5_execution_results)
    mt5_reports_completed = len(mt5_kpi_records) >= expected_mt5_kpi_record_count and all(
        item.get("status") == "completed" for item in mt5_kpi_records
    )
    external_status = "completed" if mt5_runtime_completed and mt5_reports_completed else (
        "blocked" if attempt_mt5 else "out_of_scope_by_claim"
    )
    ledger_rows = build_alpha_ledger_rows(
        tier_records=tier_records,
        mt5_kpi_records=mt5_kpi_records,
        selected_threshold_id=str(threshold_selection["threshold_id"]),
        run_output_root=run_output_root,
        external_verification_status=external_status,
    )
    ledger_payload = materialize_alpha_ledgers(ledger_rows)
    run_registry_payload = materialize_run_registry_row(
        route_coverage=route_coverage,
        mt5_kpi_records=mt5_kpi_records,
        run_output_root=run_output_root,
        external_verification_status=external_status,
        routing_mode=routing_mode,
    )
    artifacts.extend(
        [
            {"role": "stage_run_ledger", **ledger_payload["stage_run_ledger"]},
            {"role": "project_alpha_run_ledger", **ledger_payload["project_alpha_run_ledger"]},
            {"role": "project_run_registry", **run_registry_payload},
        ]
    )
    manifest = build_run_manifest_payload(
        run_id=RUN_ID,
        run_number=RUN_NUMBER,
        stage_id=STAGE_ID,
        exploration_label=EXPLORATION_LABEL,
        input_refs=input_refs,
        artifacts=artifacts,
        threshold_selection=threshold_selection,
        tier_records=tier_records,
        onnx_parity=onnx_parity,
        external_verification_status=external_status,
    )
    manifest["routing_design"] = {
        "routing_mode": routing_detail,
        "primary_tier": TIER_A,
        "fallback_enabled": bool(routed_fallback_enabled),
        "fallback_tier": TIER_B if routed_fallback_enabled else None,
        "fallback_policy_id": TIER_B_PARTIAL_CONTEXT_POLICY_ID if routed_fallback_enabled else "out_of_scope_by_claim",
        "fallback_allowed_subtypes": list(allowed_fallback_subtypes) if allowed_fallback_subtypes else None,
        "route_coverage": route_coverage,
    }
    manifest["mt5"] = {
        "attempted": bool(attempt_mt5),
        "compile": compile_payload,
        "execution_results": mt5_execution_results,
        "strategy_tester_reports": mt5_report_records,
        "kpi_records": mt5_kpi_records,
        "module_hashes": mt5_module_hashes,
        "tester_defaults": {
            "symbol": "US100",
            "period": "M5",
            "model": 4,
            "deposit": 500,
            "leverage": "1:100",
            "fixed_lot": 0.1,
            "max_hold_bars": int(max_hold_bars),
            "max_concurrent_positions": 1,
        },
    }
    kpi = build_kpi_record_payload(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        threshold_sweep=threshold_sweep,
        threshold_sweeps=threshold_sweeps,
        tier_records=tier_records,
        onnx_parity=onnx_parity,
        mt5_kpi_records=mt5_kpi_records,
    )
    kpi["threshold"]["selected_threshold_id"] = threshold_selection["threshold_id"]
    kpi["threshold"]["actual_selection"] = threshold_selection
    kpi["routing"]["routing_mode"] = routing_detail
    kpi["routing"]["fallback_enabled"] = bool(routed_fallback_enabled)
    kpi["routing"]["route_coverage_design"] = route_coverage
    kpi["mt5"] = {
        "scoreboard_lane": "runtime_probe",
        "external_verification_status": external_status,
        "compile": compile_payload,
        "execution_results": mt5_execution_results,
        "strategy_tester_reports": mt5_report_records,
        "kpi_records": mt5_kpi_records,
        "attempt_count": len(mt5_attempts),
    }
    payload_paths = materialize_manifest_and_kpi(run_output_root, manifest_payload=manifest, kpi_payload=kpi)
    summary_path = run_output_root / "summary.json"
    result_summary_path = reports_root / "result_summary.md"
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": "completed_payload" if onnx_parity["passed"] else "invalid_payload",
        "judgment": "inconclusive_single_split_scout_payload" if external_status != "completed" else "inconclusive_single_split_scout_mt5_routed_completed",
        "selected_threshold": threshold_selection,
        "tier_records": tier_records,
        "onnx_parity": onnx_parity,
        "external_verification_status": external_status,
        "mt5_attempted": bool(attempt_mt5),
        "mt5_execution_results": mt5_execution_results,
        "mt5_kpi_records": mt5_kpi_records,
        "ledger_rows": ledger_rows,
        "ledger_payload": ledger_payload,
        "run_registry_payload": run_registry_payload,
        "boundary": "single_split_scout only; not alpha quality, live readiness, runtime authority expansion, or operating promotion",
    }
    write_json(summary_path, summary)
    _io_path(result_summary_path.parent).mkdir(parents=True, exist_ok=True)
    mt5_records_by_view = {str(record.get("record_view")): record for record in mt5_kpi_records}

    def result_metric(record_view: str, metric_name: str) -> Any:
        record = mt5_records_by_view.get(record_view, {})
        return record.get("metrics", {}).get(metric_name)

    routed_view_label = (
        "`Tier A+B routed total(Tier A+B 라우팅 전체)`"
        if routed_fallback_enabled
        else "`Tier A-only routed total(Tier A 단독 라우팅 전체)`"
    )

    result_summary_lines = [
        f"# Stage 10 {RUN_NUMBER} LogReg Threshold MT5 Scout(로지스틱 임계값 MT5 탐색)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- selected threshold(선택 임계값): `{threshold_selection['threshold_id']}`",
        f"- Tier A rule(Tier A 규칙): `{tier_a_rule.threshold_id}`",
        f"- Tier B fallback rule(Tier B 대체 규칙): `{tier_b_rule.threshold_id}`",
        f"- routed fallback enabled(라우팅 대체 사용): `{bool(routed_fallback_enabled)}`",
        f"- Tier B fallback allowed subtypes(Tier B 대체 허용 하위유형): "
        f"`{list(allowed_fallback_subtypes) if allowed_fallback_subtypes else 'all'}`",
        f"- session slice(시간대 조각): `{session_slice_id or 'full'}`",
        f"- max hold bars(최대 보유 봉 수): `{int(max_hold_bars)}`",
        f"- external verification status(외부 검증 상태): `{external_status}`",
        f"- Tier A rows(Tier A 행): `{len(tier_a_predictions)}`",
        f"- Tier B fallback rows(Tier B 대체 행): `{len(tier_b_predictions)}`",
        f"- no_tier labelable rows(티어 없음 라벨 가능 행): `{len(no_tier_eval_frame)}`",
        f"- MT5 KPI records(MT5 핵심 성과 지표 기록): `{len(mt5_kpi_records)}`",
        "- MT5 comparison views(MT5 비교 보기): `Tier A only(Tier A 단독)`, "
        "`Tier B fallback-only(Tier B 대체 구간 단독)`, "
        f"{routed_view_label}",
        f"- Tier B fallback subtype counts(Tier B 대체 하위유형 수): `{route_coverage.get('tier_b_fallback_by_subtype', {})}`",
        "",
        "## Validation IS(검증 표본내)",
        "",
        f"- Tier A only net profit(Tier A 단독 순수익): `{result_metric('mt5_tier_a_only_validation_is', 'net_profit')}`",
        f"- Tier A only profit factor(Tier A 단독 수익 팩터): `{result_metric('mt5_tier_a_only_validation_is', 'profit_factor')}`",
        f"- Tier B fallback-only net profit(Tier B 대체 구간 단독 순수익): `{result_metric('mt5_tier_b_fallback_only_validation_is', 'net_profit')}`",
        f"- Tier B fallback-only profit factor(Tier B 대체 구간 단독 수익 팩터): `{result_metric('mt5_tier_b_fallback_only_validation_is', 'profit_factor')}`",
        f"- Routed net profit(라우팅 순수익): `{result_metric('mt5_routed_total_validation_is', 'net_profit')}`",
        f"- Routed profit factor(라우팅 수익 팩터): `{result_metric('mt5_routed_total_validation_is', 'profit_factor')}`",
        f"- Routed Tier A used(라우팅 Tier A 사용): `{result_metric('mt5_routed_total_validation_is', 'tier_a_used_count')}`",
        f"- Routed Tier B fallback used(라우팅 Tier B 대체 사용): `{result_metric('mt5_routed_total_validation_is', 'tier_b_fallback_used_count')}`",
        "",
        "## OOS(표본외)",
        "",
        f"- Tier A only net profit(Tier A 단독 순수익): `{result_metric('mt5_tier_a_only_oos', 'net_profit')}`",
        f"- Tier A only profit factor(Tier A 단독 수익 팩터): `{result_metric('mt5_tier_a_only_oos', 'profit_factor')}`",
        f"- Tier B fallback-only net profit(Tier B 대체 구간 단독 순수익): `{result_metric('mt5_tier_b_fallback_only_oos', 'net_profit')}`",
        f"- Tier B fallback-only profit factor(Tier B 대체 구간 단독 수익 팩터): `{result_metric('mt5_tier_b_fallback_only_oos', 'profit_factor')}`",
        f"- Routed net profit(라우팅 순수익): `{result_metric('mt5_routed_total_oos', 'net_profit')}`",
        f"- Routed profit factor(라우팅 수익 팩터): `{result_metric('mt5_routed_total_oos', 'profit_factor')}`",
        f"- Routed Tier A used(라우팅 Tier A 사용): `{result_metric('mt5_routed_total_oos', 'tier_a_used_count')}`",
        f"- Routed Tier B fallback used(라우팅 Tier B 대체 사용): `{result_metric('mt5_routed_total_oos', 'tier_b_fallback_used_count')}`",
        "",
        "## Boundary(경계)",
        "",
        "`single_split_scout(단일 분할 탐색)`이며 alpha quality(알파 품질), "
        "live readiness(실거래 준비), runtime authority expansion(런타임 권위 확장), "
        "operating promotion(운영 승격)을 주장하지 않는다.",
        "",
    ]
    _io_path(result_summary_path).write_text("\n".join(result_summary_lines), encoding="utf-8-sig")

    return {
        "status": "ok" if onnx_parity["passed"] else "failed",
        "run_id": RUN_ID,
        "run_output_root": run_output_root.as_posix(),
        "threshold_id": str(threshold_selection["threshold_id"]),
        "onnx_parity": onnx_parity,
        "external_verification_status": external_status,
        "mt5_attempted": attempt_mt5,
        "payload_paths": payload_paths,
        "summary_path": summary_path.as_posix(),
        "result_summary_path": result_summary_path.as_posix(),
        "ledger_payload": ledger_payload,
        "run_registry_payload": run_registry_payload,
    }


def threshold_rule_from_cli(
    *,
    label: str,
    threshold_id: str | None,
    short_threshold: float | None,
    long_threshold: float | None,
    min_margin: float | None,
) -> ThresholdRule | None:
    values = (short_threshold, long_threshold, min_margin)
    if all(value is None for value in values):
        return None
    if any(value is None for value in values):
        raise ValueError(f"{label} threshold override requires short, long, and min-margin values.")
    return threshold_rule_from_values(
        threshold_id=threshold_id,
        short_threshold=float(short_threshold),
        long_threshold=float(long_threshold),
        min_margin=float(min_margin),
    )


def main() -> int:
    args = parse_args()
    configure_run_identity(
        run_number=args.run_number,
        run_id=args.run_id,
        exploration_label=args.exploration_label,
        common_run_root=args.common_run_root or default_common_run_root(args.run_id),
    )
    run_output_root = (
        Path(args.run_output_root)
        if args.run_output_root
        else Path("stages") / STAGE_ID / "02_runs" / args.run_id
    )
    tier_a_rule = threshold_rule_from_cli(
        label="Tier A",
        threshold_id=args.tier_a_threshold_id,
        short_threshold=args.tier_a_short_threshold,
        long_threshold=args.tier_a_long_threshold,
        min_margin=args.tier_a_min_margin,
    )
    tier_b_rule = threshold_rule_from_cli(
        label="Tier B",
        threshold_id=args.tier_b_threshold_id,
        short_threshold=args.tier_b_short_threshold,
        long_threshold=args.tier_b_long_threshold,
        min_margin=args.tier_b_min_margin,
    )
    payload = run_stage10_logreg_mt5_scout(
        model_input_path=Path(args.model_input_path),
        feature_order_path=Path(args.feature_order_path),
        tier_b_model_input_path=Path(args.tier_b_model_input_path),
        tier_b_feature_order_path=Path(args.tier_b_feature_order_path),
        raw_root=Path(args.raw_root),
        training_summary_path=Path(args.training_summary_path),
        stage07_model_path=Path(args.stage07_model_path),
        run_output_root=run_output_root,
        common_files_root=Path(args.common_files_root),
        terminal_data_root=Path(args.terminal_data_root),
        tester_profile_root=Path(args.tester_profile_root),
        tier_column=args.tier_column,
        random_seed=args.random_seed,
        max_iter=args.max_iter,
        parity_rows=args.parity_rows,
        max_hold_bars=args.max_hold_bars,
        tier_a_threshold_rule=tier_a_rule,
        tier_b_threshold_rule=tier_b_rule,
        routed_fallback_enabled=not args.disable_routed_fallback,
        session_slice_id=args.session_slice_id,
        tier_b_fallback_allowed_subtypes=parse_tier_b_fallback_allowed_subtypes(
            args.tier_b_fallback_allowed_subtypes
        ),
        attempt_mt5=args.attempt_mt5,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
    )
    print(json.dumps(_json_ready(payload), indent=2))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
