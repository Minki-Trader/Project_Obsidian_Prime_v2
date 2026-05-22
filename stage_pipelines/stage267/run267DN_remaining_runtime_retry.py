from __future__ import annotations

import argparse
import csv
import json
import shutil
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
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    EA_TESTER_SET_NAME,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    clear_runtime_outputs,
)
from stage_pipelines.stage267 import historical_2024_mt5_executor as historical_executor
from stage_pipelines.stage267 import run267DM_shared_weakness_breakout_third_followup_or_prune_mt5_executor as source_executor


STAGE_ID = source_executor.STAGE_ID
RUN_NUMBER = "run267DN"
RUN_ID = "run267DN_stage267_shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry_v1"
SOURCE_RUN_ID = source_executor.RUN_ID
SOURCE_MATERIALIZATION_RUN_ID = source_executor.SOURCE_RUN_ID
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = source_executor.SOURCE_ATTEMPT_MANIFEST_PATH
SOURCE_VARIANT_MANIFEST_PATH = source_executor.SOURCE_VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_executor.SOURCE_RUNTIME_CONTRACT_PATH
SOURCE_REPORT_PATH = source_executor.REPORT_PATH

EXECUTION_RESULT_PATH = RUN_ROOT / "execution_result.json"
KPI_RECORDS_PATH = RUN_ROOT / "kpi_records.json"
KPI_SUMMARY_PATH = RUN_ROOT / "kpi_summary.csv"
FORENSICS_PATH = RUN_ROOT / "backtest_forensics.csv"
EXECUTED_ATTEMPTS_PATH = RUN_ROOT / "attempts_executed.csv"
PROFILE_ENCODING_RECEIPT_PATH = RUN_ROOT / "profile_encoding_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DN_shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DN_remaining_runtime_retry.py")
COMPILE_LOG_PATH = MT5_ROOT / "compile_run267dn.log"

STAGE_LEDGER_PATH = source_executor.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_executor.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_executor.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_executor.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_executor.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_executor.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_executor.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_executor.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_executor.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_executor.ARTIFACT_COLUMNS

COMPLETED_STATUS = "run267DN_shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry_completed"
PARTIAL_STATUS = "run267DN_shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry_partial"
BLOCKED_STATUS = "run267DN_shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry_blocked"
NEXT_REVIEW = "run267DO_review_run267DM_run267DN_balance_timeslice_trade_quality_with_runtime_gaps"
NEXT_RETRY = "run267DN_retry_remaining_runtime_gap_only_if_new_blocker_found"

COMMON_TELEMETRY_ROOT = "OPV2/s267dn/run267DN_shared_weakness_third_followup_or_prune_retry/telemetry"
EXPLORATION_LABEL = "stage267_BaselineRacing__SharedWeaknessThirdFollowupOrPruneRuntimeRetry"
DEFAULT_SPLIT = "run267DM_missing_runtime_scope"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return str(value)


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered or ("status", "notes"))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def source_execution_result() -> dict[str, Any]:
    return json.loads(read_text(SOURCE_EXECUTION_RESULT_PATH))


def missing_attempt_names() -> list[str]:
    result = source_execution_result()
    names: list[str] = []
    for row in result.get("execution_results", []):
        runtime = dict(row.get("runtime_outputs", {}))
        if runtime.get("status") != "completed":
            names.append(str(row.get("attempt_name")))
    return names


def configure_source_executor_for_retry() -> None:
    source_executor.RUN_NUMBER = RUN_NUMBER
    source_executor.RUN_ID = RUN_ID
    source_executor.RUN_ROOT = RUN_ROOT
    source_executor.MT5_ROOT = MT5_ROOT
    source_executor.COMPILE_LOG_PATH = COMPILE_LOG_PATH
    source_executor.COMMON_TELEMETRY_ROOT = COMMON_TELEMETRY_ROOT
    source_executor.EXPLORATION_LABEL = EXPLORATION_LABEL
    source_executor.DEFAULT_SPLIT = DEFAULT_SPLIT
    source_executor.configure_base_executor()


def source_attempt_rows() -> list[dict[str, str]]:
    rows = source_executor.base_executor.read_csv(SOURCE_ATTEMPT_MANIFEST_PATH)
    if not rows:
        raise RuntimeError(f"missing source attempt manifest: {rel(SOURCE_ATTEMPT_MANIFEST_PATH)}")
    return rows


def load_attempts(names: Sequence[str], limit: int | None) -> tuple[list[dict[str, Any]], int, list[str]]:
    configure_source_executor_for_retry()
    retry_names = list(names or missing_attempt_names())
    if limit is not None:
        retry_names = retry_names[: max(0, limit)]
    wanted = set(retry_names)
    rows = [row for row in source_attempt_rows() if row.get("attempt_name") in wanted]
    attempts = [source_executor.prepare_execution_attempt(row) for row in rows]
    return attempts, len(retry_names), retry_names


def retry_status(kpi_count: int, attempts: Sequence[Mapping[str, Any]], compile_status: str) -> str:
    if compile_status != "completed" or not attempts:
        return BLOCKED_STATUS
    if kpi_count == len(attempts):
        return COMPLETED_STATUS
    if kpi_count:
        return PARTIAL_STATUS
    return BLOCKED_STATUS


def next_action_for(status: str) -> str:
    return NEXT_REVIEW if status in {COMPLETED_STATUS, PARTIAL_STATUS, BLOCKED_STATUS} else NEXT_RETRY


def runtime_parity_rows(profile_rows: Sequence[Mapping[str, Any]], kpi_count: int, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    no_bom_count = sum(1 for row in profile_rows if str(row.get("has_bom")).lower() == "false" and row.get("exists"))
    return [
        {
            "field": "tester_profile_encoding",
            "status": "completed" if no_bom_count == len(profile_rows) and profile_rows else "blocked",
            "value": f"no_bom={no_bom_count}/{len(profile_rows)}",
            "effect": "tester profile(테스터 프로필)이 UTF-8 no BOM(UTF-8 BOM 없음)으로 인계되는지 확인했다.",
            "runtime_claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "field": "runtime_outputs",
            "status": "completed" if kpi_count == len(attempts) and attempts else "partial" if kpi_count else "blocked",
            "value": f"{kpi_count}/{len(attempts)}",
            "effect": "missing runtime output(누락 런타임 출력)을 좁게 재시도해 CSV handoff(CSV 인계) 회복 여부를 확인했다.",
            "runtime_claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "field": "source_boundary",
            "status": "checked",
            "value": SOURCE_RUN_ID,
            "effect": "run267DM(267DM 실행)의 partial runtime probe(부분 런타임 탐침)를 덮어쓰지 않고 별도 재시도로 연결했다.",
            "runtime_claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def result_judgment_rows(status: str, next_action: str) -> list[dict[str, Any]]:
    label = "runtime_probe_partial(부분 런타임 탐침)" if status == PARTIAL_STATUS else "runtime_probe(런타임 탐침)" if status == COMPLETED_STATUS else "blocked(차단)"
    return [
        {
            "result_subject": "run267DN remaining runtime retry(267DN 남은 런타임 재시도)",
            "evidence_available": "MT5 compile log(MT5 컴파일 로그), tester profiles(테스터 프로필), strategy reports(전략 보고서), runtime outputs(런타임 출력), KPI rows(KPI 행) if recovered",
            "evidence_missing": "full 14/14 runtime completion(전체 14/14 런타임 완료), balance/equity curve review(잔액/평가금 곡선 검토), trade quality review(거래 품질 검토), Adapter package(어댑터 패키지), ONNX parity(ONNX 동등성)",
            "judgment_label": label,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": "이번 실행은 run267DM에서 runtime CSV가 안 잡힌 attempt만 다시 확인하는 좁은 재시도다.",
        }
    ]


def report_markdown(result: Mapping[str, Any], status: str, next_action: str) -> str:
    kpi_rows = list(result.get("kpi_summary_rows", []))
    attempts = list(result.get("attempts_executed", []))
    execution_results = list(result.get("execution_results", []))
    lines = [
        "# Stage267 Run267DN Remaining Runtime Retry(267단계 267DN 남은 런타임 재시도)",
        "",
        f"- status(상태): `{status}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- retry_attempts(재시도 시도): `{len(attempts)}`",
        f"- recovered_kpi_records(회복 KPI 기록): `{len(result.get('mt5_kpi_records', []))}`",
        f"- next_action(다음 행동): `{next_action}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267DN(267DN 실행)은 run267DM(267DM 실행)에서 Strategy Tester report(전략 테스터 보고서)는 있었지만 runtime CSV(런타임 CSV)가 안 잡힌 attempt(시도)만 다시 실행했다.",
        "효과: 같은 후보를 다시 고르는 것이 아니라, runtime handoff(런타임 인계)가 우연히 누락된 것인지 실제 blocker(차단 사유)인지 분리한다.",
        "",
        "## Retry Outcome(재시도 결과)",
        "",
        "| attempt(시도) | candidate(후보) | profile(프로필) | tier(티어) | runtime(런타임) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) |",
        "|---|---|---|---|---|---:|---:|---:|",
    ]
    kpi_by_attempt = {str(row.get("attempt_name")): row for row in kpi_rows}
    for row in execution_results:
        attempt_name = str(row.get("attempt_name"))
        kpi = kpi_by_attempt.get(attempt_name, {})
        runtime = dict(row.get("runtime_outputs", {})).get("status", "")
        lines.append(
            "| "
            f"`{attempt_name}` | `{row.get('candidate_alias', '')}` | `{row.get('profile_label', '')}` | `{row.get('tier', '')}` | "
            f"`{runtime}` | {kpi.get('net_profit', '')} | {kpi.get('profit_factor', '')} | {kpi.get('trade_count', '')} |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 실행은 runtime probe(런타임 탐침)이며 runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포)를 주장하지 않는다.",
            "- selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 없다.",
            "- 다음 검토는 run267DM/run267DN을 같이 보고 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질), missing runtime gap(누락 런타임 공백)을 분리해야 한다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- execution_result(실행 결과): `{rel(EXECUTION_RESULT_PATH)}`",
            f"- kpi_summary(KPI 요약): `{rel(KPI_SUMMARY_PATH)}`",
            f"- backtest_forensics(백테스트 포렌식): `{rel(FORENSICS_PATH)}`",
            f"- runtime_parity_receipt(런타임 동등성 영수증): `{rel(RUNTIME_PARITY_RECEIPT_PATH)}`",
            f"- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def review_result_payload(result: Mapping[str, Any], status: str, next_action: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "status": status,
        "source_run_id": SOURCE_RUN_ID,
        "retry_attempts": len(result.get("attempts_executed", [])),
        "kpi_records": len(result.get("mt5_kpi_records", [])),
        "next_action": next_action,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_run_payloads(result: Mapping[str, Any], status: str, next_action: str, profile_rows: Sequence[Mapping[str, Any]]) -> None:
    write_json(EXECUTION_RESULT_PATH, result)
    write_json(KPI_RECORDS_PATH, result.get("mt5_kpi_records", []))
    write_csv(KPI_SUMMARY_PATH, result.get("kpi_summary_rows", []))
    write_csv(FORENSICS_PATH, result.get("backtest_forensics", []))
    write_csv(EXECUTED_ATTEMPTS_PATH, source_executor.base_executor.executed_attempt_rows(result.get("attempts_executed", []), result.get("execution_results", [])))
    write_csv(PROFILE_ENCODING_RECEIPT_PATH, profile_rows)
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, runtime_parity_rows(profile_rows, len(result.get("mt5_kpi_records", [])), result.get("attempts_executed", [])))
    write_csv(RESULT_JUDGMENT_PATH, result_judgment_rows(status, next_action))
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "source_run_id": SOURCE_RUN_ID,
            "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
            "stage_id": STAGE_ID,
            "status": status,
            "retry_attempt_count": len(result.get("attempts_executed", [])),
            "kpi_records": len(result.get("mt5_kpi_records", [])),
            "next_action": next_action,
            "claim_boundary": CLAIM_BOUNDARY,
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "source_inputs": {
                "source_execution_result": rel(SOURCE_EXECUTION_RESULT_PATH),
                "source_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
                "source_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
                "source_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
                "source_report": rel(SOURCE_REPORT_PATH),
            },
            "artifact_paths": {
                "execution_result": rel(EXECUTION_RESULT_PATH),
                "kpi_summary": rel(KPI_SUMMARY_PATH),
                "backtest_forensics": rel(FORENSICS_PATH),
                "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
                "report": rel(REPORT_PATH),
            },
            "availability": "tracked_after_closeout",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(REVIEW_RESULT_PATH, review_result_payload(result, status, next_action))
    write_md(REPORT_PATH, report_markdown(result, status, next_action))


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267DN_producer", "producer_script", PRODUCER_PATH, "Executes run267DN remaining runtime retry."),
        ("stage267_run267DN_source_execution_result", "source_execution_result", SOURCE_EXECUTION_RESULT_PATH, "Source run267DM execution result."),
        ("stage267_run267DN_compile_log", "compile_log", COMPILE_LOG_PATH, "MetaEditor compile log."),
        ("stage267_run267DN_execution_result", "execution_result", EXECUTION_RESULT_PATH, "Retry execution result payload."),
        ("stage267_run267DN_kpi_records", "kpi_records", KPI_RECORDS_PATH, "Recovered KPI records."),
        ("stage267_run267DN_kpi_summary", "kpi_summary", KPI_SUMMARY_PATH, "Recovered KPI summary."),
        ("stage267_run267DN_forensics", "backtest_forensics", FORENSICS_PATH, "Retry backtest forensics."),
        ("stage267_run267DN_attempts_executed", "attempts_executed", EXECUTED_ATTEMPTS_PATH, "Retried attempts."),
        ("stage267_run267DN_profile_encoding", "profile_encoding_receipt", PROFILE_ENCODING_RECEIPT_PATH, "Profile encoding receipt."),
        ("stage267_run267DN_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267DN_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DN_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267DN_lineage", "lineage", LINEAGE_PATH, "Lineage map."),
        ("stage267_run267DN_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267DN_report", "review_report", REPORT_PATH, "User-facing report."),
    )
    return [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    ]


def upsert_ledgers(status: str, next_action: str, kpi_count: int, attempt_count: int) -> None:
    judgment = "remaining_runtime_retry_partial" if status == PARTIAL_STATUS else "remaining_runtime_retry_completed" if status == COMPLETED_STATUS else "remaining_runtime_retry_blocked"
    stage_row = {
        "row_id": "stage267_run267DN_remaining_runtime_retry",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry",
        "tier_scope": "remaining run267DM runtime gaps only",
        "scoreboard": "mt5_runtime_remaining_gap_retry",
        "status": status,
        "judgment": judgment,
        "evidence_boundary": "runtime_retry_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"kpi_records={kpi_count};attempts={attempt_count};next_action={next_action}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "shared_weakness_remaining_runtime_retry",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "notes": f"kpi_records={kpi_count};selected_candidate=none;onnx_readiness=not_claimed.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__remaining_runtime_retry",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "remaining_runtime_retry",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry",
        "tier_scope": "remaining run267DM runtime gaps only",
        "kpi_scope": "mt5_runtime_gap_retry",
        "scoreboard_lane": "remaining_runtime_retry",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"kpi_records={kpi_count};attempts={attempt_count}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "completed" if kpi_count else "blocked",
        "notes": f"Next action: {next_action}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(utc_now()), key="artifact_id")


def replace_line_containing(text: str, needle: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            insert_at = index + 1
            while insert_at < len(lines) and lines[insert_at].startswith("  "):
                insert_at += 1
            lines.insert(insert_at, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + focus_block, 1)


def update_stage267_workspace_block(text: str, *, status: str, next_action: str) -> str:
    report_entry = f"  run267DN_remaining_runtime_retry_report_path: {rel(REPORT_PATH)}"
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    report_seen = report_entry in text
    for line in lines:
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" "):
            if not report_seen:
                output.append(report_entry)
                report_seen = True
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {status}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                if not report_seen:
                    output.append(report_entry)
                    report_seen = True
                output.append(f"  next_action: {next_action}")
                continue
        output.append(line)
    if in_stage267 and not report_seen:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def update_docs(status: str, next_action: str, kpi_count: int, attempt_count: int) -> None:
    report_line = (
        "- run267DN_remaining_runtime_retry"
        f"(267DN 남은 런타임 재시도): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267DN(267DN 실행)은 run267DM(267DM 실행)의 missing runtime output(누락 런타임 출력) attempt(시도)를 좁게 재시도했다.",
            f"Effect(효과): retry attempts(재시도 시도) `{attempt_count}`개 중 recovered KPI records(회복 KPI 기록) `{kpi_count}`개를 만들었고, 다음에는 run267DM/run267DN(267DM/267DN 실행)을 함께 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 본다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- status(", f"- status(상태): `{status}`")
            text = replace_line_containing(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "stage267_run267DM_shared_weakness_breakout_third_followup_or_prune_mt5_execution.md", report_line)
            text = append_block_once(text, "Run267DN(267DN 실행)은 run267DM", block)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_containing(text, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "stage267_run267DM_shared_weakness_breakout_third_followup_or_prune_mt5_execution", report_line)
            text = append_block_once(text, "Run267DN(267DN 실행)은 run267DM", block)
        else:
            text = replace_line_containing(text, "- status(", f"- status(상태): `{status}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "run267DM_shared_weakness_breakout_third_followup_or_prune_mt5_execution", report_line)
            text = append_block_once(text, "Run267DN(267DN 실행)은 run267DM", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_containing(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267DN(267DN 실행) remaining runtime retry(남은 런타임 재시도) `{status}`. "
        f"Effect(효과): run267DM(267DM 실행)의 missing runtime output(누락 런타임 출력) attempt(시도) `{attempt_count}`개를 재시도해 recovered KPI records(회복 KPI 기록) `{kpi_count}`개를 만들었고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(workspace, status=status, next_action=next_action)
    write_md(WORKSPACE_STATE_PATH, workspace)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    attempts, total_missing, retry_names = load_attempts(args.attempt_name or [], args.limit)
    if not attempts:
        raise RuntimeError("no run267DN retry attempts selected")

    for attempt in attempts:
        clear_runtime_outputs(args.common_files_root, attempt)
        source_executor.base_executor.mt5.remove_existing_mt5_report_artifacts(args.terminal_data_root, attempt, run_id=RUN_ID)

    compile_payload = source_executor.base_executor.mt5.compile_mql5_ea(
        args.metaeditor_path,
        source_executor.base_executor.mt5.EA_SOURCE_PATH,
        COMPILE_LOG_PATH,
    )
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            tester_result = source_executor.base_executor.mt5.run_mt5_tester(
                args.terminal_path,
                Path(str(attempt["ini"]["path"])),
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=args.tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=args.tester_profile_root / f"opv2_s267dn_{attempt['attempt_name']}.ini",
                timeout_seconds=args.timeout_seconds,
            )
            tester_result.update(
                {
                    "attempt_name": attempt.get("attempt_name"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "variant_id": attempt.get("variant_id"),
                    "profile_label": attempt.get("profile_label"),
                    "source_variant_id": attempt.get("source_variant_id"),
                    "split": attempt.get("split"),
                    "tier": attempt.get("tier"),
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "tier_pair_boundary": attempt.get("tier_pair_boundary"),
                    "materialization_boundary": attempt.get("materialization_boundary"),
                    "ini_path": attempt["ini"]["path"],
                }
            )
            tester_result["runtime_outputs"] = source_executor.base_executor.mt5.wait_for_mt5_runtime_outputs(
                args.common_files_root,
                attempt,
                timeout_seconds=args.runtime_timeout_seconds,
                poll_seconds=2,
            )
            if tester_result["runtime_outputs"].get("status") != "completed":
                tester_result["status"] = "blocked"
            execution_results.append(tester_result)

    report_records = source_executor.base_executor.mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=args.terminal_data_root,
        run_output_root=RUN_ROOT,
        attempts=attempts,
        run_id=RUN_ID,
    )
    report_records = source_executor.supplement_truncated_html_reports(
        report_records,
        attempts,
        terminal_data_root=args.terminal_data_root,
        run_output_root=RUN_ROOT,
    )
    source_executor.base_executor.mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = source_executor.base_executor.mt5.build_mt5_kpi_records(execution_results)
    kpi_rows = source_executor.base_executor.annotate_kpi_rows(historical_executor.kpi_summary_rows(kpi_records), attempts)
    forensics = source_executor.base_executor.annotate_forensic_rows(historical_executor.forensic_rows(attempts, execution_results, report_records), attempts)
    profile_rows = source_executor.base_executor.profile_encoding_rows(execution_results)
    status = retry_status(len(kpi_records), attempts, str(compile_payload.get("status")))
    next_action = next_action_for(status)
    result = {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "execution_status": status,
        "claim_boundary": CLAIM_BOUNDARY,
        "compile": compile_payload,
        "retry_attempts_total_available": total_missing,
        "retry_attempt_names": retry_names,
        "attempts_executed": attempts,
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
        "kpi_summary_rows": kpi_rows,
        "backtest_forensics": forensics,
        "profile_encoding_rows": profile_rows,
        "runtime_module_hashes": source_executor.base_executor.mt5.mt5_runtime_module_hashes(),
        "input_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
    }
    write_run_payloads(result, status, next_action, profile_rows)
    upsert_ledgers(status, next_action, len(kpi_records), len(attempts))
    update_docs(status, next_action, len(kpi_records), len(attempts))
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retry run267DM missing runtime outputs as run267DN.")
    parser.add_argument("--attempt-name", action="append", default=[])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=45)
    parser.add_argument("--terminal-path", type=Path, default=TERMINAL_PATH_DEFAULT)
    parser.add_argument("--metaeditor-path", type=Path, default=METAEDITOR_PATH_DEFAULT)
    parser.add_argument("--terminal-data-root", type=Path, default=TERMINAL_DATA_ROOT_DEFAULT)
    parser.add_argument("--common-files-root", type=Path, default=COMMON_FILES_ROOT_DEFAULT)
    parser.add_argument("--tester-profile-root", type=Path, default=TESTER_PROFILE_ROOT_DEFAULT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    result = execute(args)
    print(
        json.dumps(
            {
                "execution_status": result["execution_status"],
                "retry_attempt_count": len(result.get("attempts_executed", [])),
                "kpi_records": len(result.get("mt5_kpi_records", [])),
                "next_action": result["next_action"],
                "selected_candidate": result.get("selected_candidate"),
                "onnx_readiness": result.get("onnx_readiness"),
                "goal_achieve": result.get("goal_achieve"),
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
