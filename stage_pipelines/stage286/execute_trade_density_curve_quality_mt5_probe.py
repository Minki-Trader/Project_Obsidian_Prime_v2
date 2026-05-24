from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.alpha.discrete_signal_table import export_single_discrete_signal_score_table  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    json_ready,
    write_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
)
from stage_pipelines.stage279 import execute_or_prepare_directional_runtime_mapping_mt5_probe as base  # noqa: E402


STAGE_ID = "286_onnx_candidate_campaign__trade_density_curve_quality_rebuild"
RUN_ID = "run286B_trade_density_curve_quality_mt5_probe_v1"
RUN_NUMBER = "run286B"
SOURCE_RUN_ID = "run286A_design_materialize_trade_density_curve_quality_candidates_v1"
STATUS_PREPARED = "prepared_trade_density_curve_quality_mt5_probe_no_runtime_kpi"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)
EXPLORATION_LABEL = "stage286_Model__TradeDensityCurveQualityReplay"
SIGNAL_COLUMN = "run286b_route_signal"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage286/run286B_trade_density_curve_quality"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN286A = STAGE_ROOT / "02_runs" / "run286A"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
FEATURE_DIR = RUN_ROOT / "features"
MODEL_DIR = RUN_ROOT / "models"
MT5_DIR = RUN_ROOT / "mt5"
MT5_QUEUE = RUN286A / "mt5_probe_queue.csv"
SOURCE_MANIFEST = RUN286A / "candidate_payload_manifest.csv"
SOURCE_RUN_MANIFEST = RUN286A / "run_manifest.json"
PRODUCER = Path("stage_pipelines/stage286/execute_trade_density_curve_quality_mt5_probe.py")

ATTEMPT_SUMMARY = RUN_ROOT / "attempt_summary.csv"
RUNTIME_SUPPLY = RUN_ROOT / "runtime_supply_matrix.csv"
EXECUTION_RESULT = RUN_ROOT / "execution_result.json"
MT5_KPI_SUMMARY = RUN_ROOT / "mt5_kpi_summary.csv"
RUNTIME_PARITY_RECEIPT = RUN_ROOT / "runtime_parity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run286B_trade_density_curve_quality_mt5_probe_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def configure_base() -> None:
    base.STAGE_ID = STAGE_ID
    base.RUN_ID = RUN_ID
    base.RUN_NUMBER = RUN_NUMBER
    base.SOURCE_RUN_ID = SOURCE_RUN_ID
    base.PARENT_RUN_ID = "run285A_export_cp282d_adapter_to_onnx_and_runtime_reproduction_v1"
    base.STATUS_PREPARED = STATUS_PREPARED
    base.UPDATED_ON = UPDATED_ON
    base.BOUNDARY = BOUNDARY
    base.EXPLORATION_LABEL = EXPLORATION_LABEL
    base.SIGNAL_COLUMN = SIGNAL_COLUMN
    base.COMMON_ROOT = COMMON_ROOT
    base.STAGE_ROOT = STAGE_ROOT
    base.RUN279B = RUN286A
    base.RUN_ROOT = RUN_ROOT
    base.REVIEWS = REVIEWS
    base.SELECTED = SELECTED
    base.REPORT_PATH = REPORT
    base.FEATURE_DIR = FEATURE_DIR
    base.MODEL_DIR = MODEL_DIR
    base.MT5_DIR = MT5_DIR
    base.MT5_QUEUE = MT5_QUEUE
    base.RUN279B_MANIFEST = SOURCE_RUN_MANIFEST
    base.RUN279B_PAYLOAD_MANIFEST = SOURCE_MANIFEST
    base.RUN279B_SIGNAL_RECEIPT = SOURCE_MANIFEST
    base.RUN279B_REPORT = REVIEWS / "run286A_trade_density_curve_quality_materialization_report.md"
    base.RUN_REGISTRY = RUN_REGISTRY
    base.ALPHA_LEDGER = ALPHA_LEDGER
    base.ARTIFACT_REGISTRY = ARTIFACT_REGISTRY
    base.STAGE_LEDGER = STAGE_LEDGER
    base.CURRENT_STATE = CURRENT_STATE
    base.WORKSPACE_STATE = WORKSPACE_STATE
    base.CHANGELOG = CHANGELOG
    base.REVIEW_INDEX = REVIEW_INDEX
    base.PRODUCER_PATH = PRODUCER
    base.ATTEMPT_SUMMARY = ATTEMPT_SUMMARY
    base.RUNTIME_SUPPLY = RUNTIME_SUPPLY
    base.EXECUTION_RESULT = EXECUTION_RESULT
    base.MT5_KPI_SUMMARY = MT5_KPI_SUMMARY
    base.RUNTIME_PARITY_RECEIPT = RUNTIME_PARITY_RECEIPT
    base.RESULT_JUDGMENT = RESULT_JUDGMENT
    base.GATE_AUDIT = GATE_AUDIT
    base.RUN_MANIFEST = RUN_MANIFEST
    base.LINEAGE_RECEIPT = LINEAGE
    original_attempt_payload = base.attempt_payload

    def stage286_attempt_payload(**kwargs: Any) -> dict[str, Any]:
        kwargs["stage_number"] = 286
        return original_attempt_payload(**kwargs)

    base.attempt_payload = stage286_attempt_payload


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(str(key))
    write_csv_rows(path, columns or ["status"], rows)


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    queue_rows = base.load_queue_rows()
    feature_exports, split_frames, supply_rows = base.export_feature_matrices(queue_rows)
    write_csv(RUNTIME_SUPPLY, supply_rows)
    model_artifact = export_single_discrete_signal_score_table(
        MODEL_DIR / "stage286_run286B_route_signal_score_table.csv",
        feature_order=(SIGNAL_COLUMN,),
    )
    common_copies = base.copy_runtime_inputs(feature_exports, model_artifact, Path(args.common_files_root))
    full_attempts = base.build_all_attempts(queue_rows, feature_exports, split_frames, model_artifact, include_routed=not args.no_routed)
    start_index = max(0, int(args.start_index))
    end_index = start_index + int(args.limit) if args.limit is not None else None
    attempts = full_attempts[start_index:end_index]
    return {
        "stage_id": STAGE_ID,
        "stage_number": 286,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "run_root": RUN_ROOT,
        "attempts": attempts,
        "planned_attempt_count": len(full_attempts),
        "common_copies": common_copies,
        "feature_exports": feature_exports,
        "model_artifact": model_artifact,
        "runtime_supply_matrix": supply_rows,
        "route_coverage": base.route_coverage_from_supply(supply_rows),
        "model_family": "single_discrete_signal_score_table",
        "feature_set_id": "stage286_trade_density_route_signal_replay",
        "label_id": "not_applicable_precomputed_route_signal",
        "split_contract": "Stage286 run286A payload split labels validation and oos",
        "claim_boundary": BOUNDARY,
    }


def classify_status(result: Mapping[str, Any], materialize_only: bool) -> tuple[str, str, str, str]:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    planned = int(result.get("planned_attempt_count", len(attempts)) or len(attempts))
    limited = len(execution_results) < planned
    if materialize_only:
        return (
            STATUS_PREPARED,
            "trade_density_runtime_probe_prepared_no_external_execution",
            "out_of_scope_by_claim_materialize_only",
            "run286B_execute_trade_density_curve_quality_mt5_probe_external_check",
        )
    completed_exec = sum(1 for item in execution_results if item.get("status") == "completed")
    if planned and completed_exec >= planned and len(kpis) >= planned:
        return (
            "completed_trade_density_curve_quality_mt5_probe_no_selection",
            "runtime_probe_completed_requires_curve_quality_review_no_selection",
            "completed",
            "run286C_review_trade_density_curve_quality_mt5_probe",
        )
    if kpis:
        return (
            "partial_trade_density_curve_quality_mt5_probe_no_selection",
            "runtime_probe_partial_requires_continuation_no_selection",
            "partial_or_blocked",
            "run286B_continue_trade_density_curve_quality_mt5_probe" if limited else "run286C_review_with_runtime_gaps",
        )
    return (
        "blocked_trade_density_curve_quality_mt5_probe_no_kpi",
        "runtime_probe_blocked_no_kpi_no_selection",
        "blocked_or_invalid",
        "run286B_repair_or_block_trade_density_curve_quality_mt5_probe",
    )


def run_probe(args: argparse.Namespace) -> dict[str, Any]:
    configure_base()
    created_at = utc_now()
    for path in (RUN_ROOT, FEATURE_DIR, MODEL_DIR, MT5_DIR, REVIEWS):
        base.io_path(path).mkdir(parents=True, exist_ok=True)
    prepared = prepare(args)
    if args.materialize_only:
        result = {
            **prepared,
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
        }
    else:
        result = base.execute_prepared(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=Path(args.terminal_data_root),
            common_files_root=Path(args.common_files_root),
            tester_profile_root=Path(args.tester_profile_root),
            timeout_seconds=int(args.timeout_seconds),
            runtime_timeout_seconds=int(args.runtime_timeout_seconds),
        )
    if args.merge_existing:
        result = base.merge_existing_result(result, start_index=max(0, int(args.start_index)), limit=args.limit)
    status, judgment, external_status, next_action = classify_status(result, bool(args.materialize_only))
    result = {
        **dict(result),
        "status": status,
        "judgment": judgment,
        "external_verification_status": external_status,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
        "created_at_utc": created_at,
    }
    final_paths = base.write_outputs(result, status, judgment, external_status, next_action, created_at)
    base.upsert_ledgers(result, status, judgment, external_status, next_action)
    base.update_artifact_registry(final_paths, created_at)
    base.update_docs(status, judgment, next_action, len(result.get("mt5_kpi_records", [])), len(result.get("attempts", [])))
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute or prepare Stage286 trade density curve quality MT5 probe.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--merge-existing", action="store_true")
    parser.add_argument("--no-routed", action="store_true")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=180)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    result = run_probe(parse_args(argv or sys.argv[1:]))
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": result["status"],
                "judgment": result["judgment"],
                "external_verification_status": result["external_verification_status"],
                "attempt_count": len(result.get("attempts", [])),
                "planned_attempt_count": result.get("planned_attempt_count"),
                "execution_result_count": len(result.get("execution_results", [])),
                "mt5_kpi_records": len(result.get("mt5_kpi_records", [])),
                "selected_candidate": result.get("selected_candidate"),
                "adapter_package": result.get("adapter_package"),
                "onnx_readiness": result.get("onnx_readiness"),
                "goal_achieve": result.get("goal_achieve"),
                "next_action": result.get("next_action"),
                "report": base.rel(REPORT),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
