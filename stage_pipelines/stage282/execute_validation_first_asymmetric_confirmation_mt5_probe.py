from __future__ import annotations

import argparse
import hashlib
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
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
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


STAGE_ID = "282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild"
RUN_ID = "run282B_validation_first_asymmetric_confirmation_mt5_probe_v1"
RUN_NUMBER = "run282B"
SOURCE_RUN_ID = "run282A_design_materialize_validation_first_asymmetric_confirmation_candidate_packet_v1"
STATUS_PREPARED = "prepared_validation_first_asymmetric_confirmation_mt5_probe_no_runtime_kpi"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_proDUCTION_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
).replace("proDUCTION", "production")
EXPLORATION_LABEL = "stage282_Model__ValidationFirstAsymmetricConfirmationReplay"
SIGNAL_COLUMN = "run282b_route_signal"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage282/run282B_validation_first_asymmetric"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN282A = STAGE_ROOT / "02_runs" / "run282A"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
FEATURE_DIR = RUN_ROOT / "features"
MODEL_DIR = RUN_ROOT / "models"
MT5_DIR = RUN_ROOT / "mt5"
MT5_QUEUE = RUN282A / "mt5_probe_queue.csv"
SOURCE_MANIFEST = RUN282A / "candidate_payload_manifest.csv"
SOURCE_RUN_MANIFEST = RUN282A / "run_manifest.json"
PRODUCER = Path("stage_pipelines/stage282/execute_validation_first_asymmetric_confirmation_mt5_probe.py")

ATTEMPT_SUMMARY = RUN_ROOT / "attempt_summary.csv"
RUNTIME_SUPPLY = RUN_ROOT / "runtime_supply_matrix.csv"
EXECUTION_RESULT = RUN_ROOT / "execution_result.json"
MT5_KPI_SUMMARY = RUN_ROOT / "mt5_kpi_summary.csv"
RUNTIME_PARITY_RECEIPT = RUN_ROOT / "runtime_parity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run282B_validation_first_asymmetric_confirmation_mt5_probe_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def sha256_file(path: Path) -> str:
    return sha256_file_lf_normalized(path)


def configure_base() -> None:
    base.STAGE_ID = STAGE_ID
    base.RUN_ID = RUN_ID
    base.RUN_NUMBER = RUN_NUMBER
    base.SOURCE_RUN_ID = SOURCE_RUN_ID
    base.PARENT_RUN_ID = "run281C_review_drawdown_normalized_directional_mt5_probe_v1"
    base.STATUS_PREPARED = STATUS_PREPARED
    base.UPDATED_ON = UPDATED_ON
    base.BOUNDARY = BOUNDARY
    base.EXPLORATION_LABEL = EXPLORATION_LABEL
    base.SIGNAL_COLUMN = SIGNAL_COLUMN
    base.COMMON_ROOT = COMMON_ROOT
    base.STAGE_ROOT = STAGE_ROOT
    base.RUN279B = RUN282A
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
    base.RUN279B_REPORT = REVIEWS / "run282A_candidate_packet_materialization_report.md"
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

    def stage282_attempt_payload(**kwargs: Any) -> dict[str, Any]:
        kwargs["stage_number"] = 282
        return original_attempt_payload(**kwargs)

    base.attempt_payload = stage282_attempt_payload


def dynamic_columns(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(str(key))
    return columns or ["status"]


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    queue_rows = base.load_queue_rows()
    feature_exports, split_frames, supply_rows = base.export_feature_matrices(queue_rows)
    write_csv(RUNTIME_SUPPLY, tuple(supply_rows[0].keys()) if supply_rows else ("status",), supply_rows)
    model_artifact = export_single_discrete_signal_score_table(
        MODEL_DIR / "stage282_run282B_route_signal_score_table.csv",
        feature_order=(SIGNAL_COLUMN,),
    )
    common_copies = base.copy_runtime_inputs(feature_exports, model_artifact, Path(args.common_files_root))
    full_attempts = base.build_all_attempts(queue_rows, feature_exports, split_frames, model_artifact, include_routed=not args.no_routed)
    start_index = max(0, int(args.start_index))
    end_index = start_index + int(args.limit) if args.limit is not None else None
    attempts = full_attempts[start_index:end_index]
    return {
        "stage_id": STAGE_ID,
        "stage_number": 282,
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
        "feature_set_id": "stage282_validation_first_route_signal_replay",
        "label_id": "not_applicable_precomputed_route_signal",
        "split_contract": "Stage282 run282A payload split labels validation and oos",
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
            "runtime_probe_prepared_no_external_execution",
            "out_of_scope_by_claim_materialize_only",
            "run282B_execute_validation_first_asymmetric_confirmation_mt5_probe_external_check",
        )
    completed_exec = sum(1 for item in execution_results if item.get("status") == "completed")
    if planned and completed_exec >= planned and len(kpis) >= planned:
        return (
            "completed_validation_first_asymmetric_confirmation_mt5_probe_no_candidate_selection",
            "runtime_probe_completed_requires_review_no_candidate_selection",
            "completed",
            "run282C_review_validation_first_asymmetric_confirmation_mt5_probe",
        )
    if kpis:
        return (
            "partial_validation_first_asymmetric_confirmation_mt5_probe_no_candidate_selection",
            "runtime_probe_partial_requires_continuation_no_candidate_selection",
            "partial_or_blocked",
            "run282B_continue_validation_first_asymmetric_confirmation_mt5_probe" if limited else "run282C_review_with_runtime_gaps",
        )
    return (
        "blocked_validation_first_asymmetric_confirmation_mt5_probe_no_kpi",
        "runtime_probe_blocked_no_kpi_no_candidate_selection",
        "blocked_or_invalid",
        "run282B_repair_or_block_validation_first_asymmetric_confirmation_mt5_probe",
    )


def run_probe(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    for path in (RUN_ROOT, FEATURE_DIR, MODEL_DIR, MT5_DIR, REVIEWS):
        io_path(path).mkdir(parents=True, exist_ok=True)
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
    final_paths = write_outputs(result, status, judgment, external_status, next_action, created_at)
    update_registers_and_docs(result, status, judgment, external_status, next_action, created_at, final_paths)
    return result


def write_outputs(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str, created_at: str) -> list[Path]:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    attempt_rows = base.attempt_summary_rows(result)
    write_json(EXECUTION_RESULT, result)
    write_csv(ATTEMPT_SUMMARY, dynamic_columns(attempt_rows), attempt_rows)
    write_csv(RUNTIME_SUPPLY, dynamic_columns(result.get("runtime_supply_matrix", [])), result.get("runtime_supply_matrix", []))
    write_csv(MT5_KPI_SUMMARY, dynamic_columns(kpis), kpis)
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(ROOT / PRODUCER),
            "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
            "shared_contract": "single feature route_signal_value mapped to short/flat/long score table",
            "parity_check": external_status,
            "attempt_count": len(attempts),
            "execution_result_count": len(execution_results),
            "mt5_kpi_record_count": len(kpis),
            "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"attempts={len(attempts)};execution_results={len(execution_results)};mt5_kpi_records={len(kpis)}",
                "evidence_missing": "run282C stability review;selected candidate package;Adapter package;ONNX parity",
                "judgment_label": judgment,
                "judgment_class": "runtime_probe",
                "claim_boundary": BOUNDARY,
                "next_condition": next_action,
                "user_explanation_hook": "MT5 탐침 결과가 생겼지만 아직 후보 선택은 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "feature_handoff_materialized(피처 인계 물질화)",
                "status": "passed",
                "evidence_path": rel(RUNTIME_SUPPLY),
                "effect": "EA가 읽을 route_signal_value CSV를 만들었다.",
            },
            {
                "gate_name": "external_runtime_attempt(외부 런타임 시도)",
                "status": external_status,
                "evidence_path": rel(EXECUTION_RESULT),
                "effect": "MT5 전략 테스터 실행 또는 준비 상태를 기록한다.",
            },
            {
                "gate_name": "candidate_claim_boundary(후보 주장 경계)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "후보 선택, 어댑터 패키지, 온엑스 준비를 주장하지 않는다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(result, status, judgment, external_status, next_action))
    core_paths = [EXECUTION_RESULT, ATTEMPT_SUMMARY, RUNTIME_SUPPLY, MT5_KPI_SUMMARY, RUNTIME_PARITY_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, REPORT]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": status,
            "judgment": judgment,
            "external_verification_status": external_status,
            "created_at_utc": created_at,
            "attempt_count": len(attempts),
            "planned_attempt_count": result.get("planned_attempt_count"),
            "execution_result_count": len(execution_results),
            "mt5_kpi_record_count": len(kpis),
            "output_hashes": {rel(path): sha256_file(path) for path in core_paths if path_exists(path)},
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": next_action,
            "claim_boundary": BOUNDARY,
        },
    )
    core_paths.append(RUN_MANIFEST)
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "source_inputs": [rel(MT5_QUEUE), rel(SOURCE_MANIFEST), rel(SOURCE_RUN_MANIFEST), rel(ROOT / PRODUCER)],
            "source_hashes": {
                rel(path): sha256_file(path)
                for path in [MT5_QUEUE, SOURCE_MANIFEST, SOURCE_RUN_MANIFEST, ROOT / PRODUCER]
                if path_exists(path)
            },
            "artifact_paths": [rel(path) for path in core_paths if path_exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in core_paths if path_exists(path)},
            "lineage_judgment": "connected_with_boundary_no_candidate_no_onnx_claim",
        },
    )
    core_paths.append(LINEAGE)
    return core_paths


def report_markdown(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> str:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    completed = sum(1 for item in execution_results if item.get("status") == "completed")
    blocked = sum(1 for item in execution_results if item.get("status") == "blocked")
    return "\n".join(
        [
            "# run282B Report(282B 보고서): Validation-First Asymmetric Confirmation MT5 Probe(검증 우선 비대칭 확인 MT5 탐침)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- status(상태): `{status}`",
            f"- judgment(판정): `{judgment}`",
            f"- external_verification_status(외부 검증 상태): `{external_status}`",
            f"- attempts(시도): `{len(execution_results)}/{len(attempts)}`",
            f"- completed_attempts(완료 시도): `{completed}`",
            f"- blocked_attempts(차단 시도): `{blocked}`",
            f"- mt5_kpi_records(MT5 핵심 성과 지표 기록): `{len(kpis)}`",
            "- selected_candidate(선택 후보): `none`",
            "- Adapter package(어댑터 패키지): `none`",
            "- ONNX readiness(온엑스 준비): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            f"- next_action(다음 행동): `{next_action}`",
            "",
            "Effect(효과): 검증 우선 비대칭 확인 표면을 MT5(`MetaTrader 5`, 메타트레이더5)로 실행했거나 준비했고, 다음 검토에서 후보 생존 여부를 판정한다.",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def update_registers_and_docs(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str, created_at: str, paths: Sequence[Path]) -> None:
    kpi_count = len(result.get("mt5_kpi_records", []))
    attempt_count = len(result.get("attempts", []))
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "validation_first_asymmetric_confirmation_mt5_probe",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count};selected_candidate=none;next_action={next_action}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__mt5_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "run282B_mt5_probe",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "validation_first_asymmetric_confirmation_mt5_probe(검증 우선 비대칭 확인 MT5 탐침)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "runtime_probe_no_candidate_selection",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "primary_kpi": f"attempts={attempt_count};mt5_kpi_records={kpi_count}",
                "guardrail_kpi": "selected_candidate=none;adapter_package=none;onnx_readiness=not_claimed",
                "external_verification_status": external_status,
                "notes": f"next_action={next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__mt5_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "validation_first_asymmetric_confirmation_mt5_probe",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "runtime_probe",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "runtime_probe_no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage282_mt5_probe_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run282B MT5 probe(282B MT5 탐침)",
        }
        for path in paths
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selected = append_once(selected, "run282B_report", f"- run282B_report(282B 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "run282B_execution_result", f"- run282B_execution_result(282B 실행 결과): `{rel(EXECUTION_RESULT)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage282 Review Index(282단계 검토 색인)\n"
    review_index = append_once(review_index, "run282B_report", f"- run282B_report(282B 보고서): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    current = append_once(
        current,
        "run282B_summary",
        f"- run282B_summary(282B 요약): 검증 우선 비대칭 확인 MT5 탐침을 실행/준비했다. Effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 핵심 성과 지표 기록) `{kpi_count}`개를 기록했거나 준비했고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage282(282단계) run282B(282B 실행) MT5 probe(MT5 탐침) `{RUN_ID}` produced or prepared `{kpi_count}` KPI records(핵심 성과 지표 기록). "
        f"Effect(효과): 다음 run282C(282C 실행)에서 안정성 생존 여부를 판정한다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run282B Validation-first MT5 probe(282B 검증 우선 MT5 탐침)\n\n- status(상태): `{status}`\n- judgment(판정): `{judgment}`\n- effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 핵심 성과 지표 기록) `{kpi_count}`개를 기록했거나 준비했다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute Stage282 validation-first asymmetric confirmation MT5 probe.")
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
    configure_base()
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
                "report": rel(REPORT),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
