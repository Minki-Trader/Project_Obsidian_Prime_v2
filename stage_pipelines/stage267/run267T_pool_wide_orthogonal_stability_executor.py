from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    EA_TESTER_SET_NAME,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    clear_runtime_outputs,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage267 import historical_2024_mt5_executor as run267b_executor
from stage_pipelines.stage267 import run267T_build_pool_wide_orthogonal_stability_mt5_attempts as materializer


STAGE_ID = materializer.STAGE_ID
RUN_ID = materializer.RUN_ID
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY
RUN_ROOT = materializer.RUN_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
ATTEMPT_MANIFEST_PATH = materializer.ATTEMPT_MANIFEST_PATH
VARIANT_MANIFEST_PATH = materializer.VARIANT_MANIFEST_PATH
RUNTIME_CONTRACT_PATH = materializer.RUNTIME_CONTRACT_PATH
STAGE_LEDGER_PATH = materializer.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = materializer.ARTIFACT_REGISTRY_PATH
RUN_REGISTRY_PATH = materializer.RUN_REGISTRY_PATH
PROJECT_LEDGER_PATH = materializer.PROJECT_LEDGER_PATH
CURRENT_WORKING_STATE_PATH = materializer.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = materializer.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = materializer.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = materializer.REVIEW_INDEX_PATH

EXECUTION_RESULT_PATH = RUN_ROOT / "execution_result.json"
KPI_RECORDS_PATH = RUN_ROOT / "kpi_records.json"
KPI_SUMMARY_PATH = RUN_ROOT / "kpi_summary.csv"
FORENSICS_PATH = RUN_ROOT / "backtest_forensics.csv"
EXECUTED_ATTEMPTS_PATH = RUN_ROOT / "attempts_executed.csv"
COMPILE_LOG_PATH = RUN_ROOT / "mt5" / "compile_run267t.log"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267T_pool_wide_orthogonal_stability_mt5_execution.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267T_pool_wide_orthogonal_stability_executor.py")

COMPLETED_STATUS = "run267T_pool_wide_orthogonal_stability_mt5_batch_completed"
PARTIAL_STATUS = "run267T_pool_wide_orthogonal_stability_mt5_batch_partial"
BLOCKED_STATUS = "run267T_pool_wide_orthogonal_stability_mt5_batch_blocked"
NEXT_ACTION_COMPLETED = "run267T_review_pool_wide_orthogonal_stability_mt5_results"
NEXT_ACTION_PARTIAL = "run267T_execute_remaining_pool_wide_orthogonal_stability_mt5_batch"
NEXT_ACTION_BLOCKED = "run267T_repair_pool_wide_orthogonal_stability_mt5_execution_blocker"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in fieldnames})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_ini(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    text = io_path(path).read_text(encoding="utf-8-sig")
    for line in text.splitlines():
        if not line or line.lstrip().startswith("[") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def variant_lookup() -> dict[str, dict[str, str]]:
    return {row["variant_id"]: row for row in read_csv_rows(VARIANT_MANIFEST_PATH)}


def attempt_payload(row: Mapping[str, str], variants: Mapping[str, Mapping[str, str]]) -> dict[str, Any]:
    ini_path = Path(str(row["ini_path"]))
    variant = dict(variants.get(str(row.get("queue_id")), {}))
    payload: dict[str, Any] = {
        "queue_id": row.get("queue_id"),
        "source_queue_id": row.get("source_queue_id"),
        "axis_id": row.get("axis_id"),
        "candidate_id": row.get("candidate_id"),
        "candidate_alias": row.get("candidate_alias"),
        "candidate_role": row.get("candidate_role"),
        "test_id": row.get("test_id"),
        "test_type": variant.get("test_type", row.get("test_type", "")),
        "priority": row.get("priority"),
        "attempt_name": row["attempt_name"],
        "tier": row["tier"],
        "split": row["split"],
        "attempt_role": row["attempt_role"],
        "record_view_prefix": row["record_view_prefix"],
        "set": {"path": row["set_path"], "sha256": row["set_sha256"], "format": "mt5_set"},
        "ini": {
            "path": row["ini_path"],
            "sha256": row["ini_sha256"],
            "format": "mt5_tester_ini",
            "tester": read_ini(ini_path),
        },
        "common_telemetry_path": row["common_telemetry_path"],
        "common_summary_path": row["common_summary_path"],
        "fallback_enabled": bool_text(row.get("fallback_enabled")),
        "materialization_boundary": variant.get("materialization_boundary", ""),
        "feature_order_hash": variant.get("feature_order_hash", ""),
        "source_feature_sha256": variant.get("feature_sha256", ""),
        "source_model_sha256": variant.get("model_sha256", ""),
    }
    if payload["fallback_enabled"]:
        payload["routing_mode"] = mt5.ROUTING_MODE_A_B_FALLBACK
        payload["routing_detail"] = "tier_a_primary_tier_b_partial_context_fallback"
    return payload


def load_attempts(names: Sequence[str], limit: int | None) -> tuple[list[dict[str, Any]], int]:
    rows = read_csv_rows(ATTEMPT_MANIFEST_PATH)
    selected = rows
    if names:
        wanted = set(names)
        selected = [row for row in rows if row.get("attempt_name") in wanted]
    if limit is not None:
        selected = selected[: max(0, int(limit))]
    variants = variant_lookup()
    return [attempt_payload(row, variants) for row in selected], len(rows)


def status_token(base_status: str, selected_count: int, total_count: int) -> str:
    if base_status == "completed" and selected_count == total_count:
        return COMPLETED_STATUS
    if base_status in {"completed", "partial"} and selected_count > 0:
        return PARTIAL_STATUS
    return BLOCKED_STATUS


def next_action_for(status: str, kpi_count: int, selected_count: int, total_count: int) -> str:
    if not kpi_count:
        return NEXT_ACTION_BLOCKED
    if status == PARTIAL_STATUS or selected_count < total_count:
        return NEXT_ACTION_PARTIAL
    return NEXT_ACTION_COMPLETED


def backtest_judgment(status: str, kpi_count: int) -> str:
    if kpi_count and status == COMPLETED_STATUS:
        return "usable_with_boundary"
    if kpi_count:
        return "inconclusive"
    return "blocked"


def external_verification_status(status: str, kpi_count: int) -> str:
    if kpi_count and status == COMPLETED_STATUS:
        return "completed"
    if kpi_count:
        return "partial"
    return "blocked"


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv_rows(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def annotate_kpi_rows(
    rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    annotated: list[dict[str, Any]] = []
    prefixes = [(str(attempt.get("record_view_prefix")), attempt) for attempt in attempts]
    for row in rows:
        next_row = dict(row)
        record_view = str(row.get("record_view", ""))
        for prefix, attempt in prefixes:
            if prefix and record_view.startswith(prefix):
                next_row["queue_id"] = attempt.get("queue_id")
                next_row["source_queue_id"] = attempt.get("source_queue_id")
                next_row["axis_id"] = attempt.get("axis_id")
                next_row["candidate_id"] = attempt.get("candidate_id")
                next_row["candidate_alias"] = attempt.get("candidate_alias")
                next_row["candidate_role"] = attempt.get("candidate_role")
                next_row["test_id"] = attempt.get("test_id")
                next_row["test_type"] = attempt.get("test_type")
                next_row["priority"] = attempt.get("priority")
                next_row["materialization_boundary"] = attempt.get("materialization_boundary")
                break
        annotated.append(next_row)
    return annotated


def executed_attempt_rows(
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_name = {str(item.get("attempt_name")): item for item in execution_results}
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        result = by_name.get(str(attempt.get("attempt_name")), {})
        rows.append(
            {
                "queue_id": attempt.get("queue_id"),
                "source_queue_id": attempt.get("source_queue_id"),
                "axis_id": attempt.get("axis_id"),
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "test_id": attempt.get("test_id"),
                "test_type": attempt.get("test_type"),
                "materialization_boundary": attempt.get("materialization_boundary"),
                "attempt_name": attempt.get("attempt_name"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "ini_sha256": attempt.get("ini", {}).get("sha256"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "fallback_enabled": attempt.get("fallback_enabled", False),
                "execution_status": result.get("status", "not_executed"),
                "runtime_status": result.get("runtime_outputs", {}).get("status") if isinstance(result, Mapping) else "",
            }
        )
    return rows


def upsert_stage_ledger(status: str, kpi_count: int, next_action: str) -> None:
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267T_pool_wide_orthogonal_stability_mt5_execution",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "pool_wide_orthogonal_stability_mt5_execution",
            "tier_scope": "Tier A and Tier A+B historical 2024 orthogonal stability attempts",
            "scoreboard": "runtime_tranche_or_full_batch",
            "status": status,
            "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_mt5_execution",
            "evidence_boundary": "mt5_runtime_batch_no_candidate_selection_no_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"kpi_records={kpi_count};next_action={next_action};selected_candidate=none.",
        },
        (
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
        ),
    )


def upsert_run_registers(status: str, next_action: str, kpi_count: int) -> None:
    judgment = "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_or_no_kpi"
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "pool_wide_orthogonal_stability_mt5_execution",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "notes": f"Run267T pool-wide orthogonal stability MT5 execution; kpi_records={kpi_count}; selected_candidate=none; onnx_readiness=not_claimed; next_action={next_action}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__pool_wide_orthogonal_stability_mt5_execution",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "pool_wide_orthogonal_stability_mt5_execution",
            "parent_run_id": RUN_ID,
            "record_view": "pool_wide_orthogonal_stability_mt5_execution",
            "tier_scope": "Tier A and Tier A+B historical 2024 orthogonal stability attempts",
            "kpi_scope": "mt5_runtime_pool_wide_orthogonal_stability",
            "scoreboard_lane": "runtime_tranche_or_full_batch",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"kpi_records={kpi_count}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": external_verification_status(status, kpi_count),
            "notes": f"Next action: {next_action}.",
        },
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "subrun_id",
            "parent_run_id",
            "record_view",
            "tier_scope",
            "kpi_scope",
            "scoreboard_lane",
            "status",
            "judgment",
            "path",
            "primary_kpi",
            "guardrail_kpi",
            "external_verification_status",
            "notes",
        ),
    )


def upsert_artifacts(created_at: str) -> None:
    entries = (
        ("stage267_run267T_orthogonal_executor", "producer_script", PRODUCER_PATH, "Executes run267T pool-wide orthogonal stability MT5 tranche or full batch."),
        ("stage267_run267T_orthogonal_compile_log", "compile_log", COMPILE_LOG_PATH, "MetaEditor compile log for run267T."),
        ("stage267_run267T_orthogonal_execution_result", "execution_result", EXECUTION_RESULT_PATH, "MT5 execution result payload for run267T."),
        ("stage267_run267T_orthogonal_kpi_records", "kpi_records", KPI_RECORDS_PATH, "MT5 KPI records for run267T."),
        ("stage267_run267T_orthogonal_kpi_summary", "kpi_summary", KPI_SUMMARY_PATH, "MT5 KPI summary for run267T."),
        ("stage267_run267T_orthogonal_forensics", "backtest_forensics", FORENSICS_PATH, "Tester identity and report evidence for run267T."),
        ("stage267_run267T_orthogonal_attempts_executed", "attempt_manifest", EXECUTED_ATTEMPTS_PATH, "Attempt list selected for run267T execution."),
        ("stage267_run267T_orthogonal_execution_report", "review_report", REPORT_PATH, "User-facing run267T MT5 execution report."),
    )
    rows = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, notes in entries:
        new_rows.append(
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
        )
    replacement_ids = {row["artifact_id"] for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement_ids]
    merged.extend(new_rows)
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def remove_lines_containing(text: str, required: Sequence[str]) -> str:
    lines = []
    for line in text.splitlines():
        if all(token in line for token in required):
            continue
        lines.append(line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def replace_status_and_next_action(text: str, status: str, next_action: str) -> str:
    for token in (materializer.STATUS, COMPLETED_STATUS, PARTIAL_STATUS, BLOCKED_STATUS):
        text = text.replace(token, status)
    for token in (materializer.NEXT_ACTION, NEXT_ACTION_COMPLETED, NEXT_ACTION_PARTIAL, NEXT_ACTION_BLOCKED):
        text = text.replace(token, next_action)
    return text


def update_current_truth_docs(status: str, next_action: str, attempt_count: int, total_count: int, kpi_count: int) -> None:
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_status_and_next_action(current, status, next_action)
    current = remove_lines_containing(
        current,
        ("latest_mt5_execution", "stage267_run267T_pool_wide_orthogonal_stability_mt5_execution.md"),
    )
    current = append_after_contains(
        current,
        "stage267_run267T_pool_wide_orthogonal_stability_mt5_attempts.md",
        f"- Stage267(267단계) run267T pool-wide orthogonal stability MT5 execution(후보군 전체 직교 안정성 MT5 실행): `{rel(REPORT_PATH)}`",
    )
    current = append_after_contains(
        current,
        "## Current Next Action",
        f"- latest_mt5_execution(최신 MT5 실행): attempts(시도) `{attempt_count}` of `{total_count}`, KPI records(핵심 성과 지표 기록) `{kpi_count}`, report(보고서) `{rel(REPORT_PATH)}`.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_status_and_next_action(selection, status, next_action)
    selection = append_after_contains(
        selection,
        "run267T_pool_wide_orthogonal_stability_mt5_attempts",
        f"- run267T_pool_wide_orthogonal_stability_mt5_execution(267T 후보군 전체 직교 안정성 MT5 실행): `{rel(REPORT_PATH)}`",
    )
    write_md(SELECTION_STATUS_PATH, selection)

    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = replace_status_and_next_action(review, status, next_action)
    review = append_after_contains(
        review,
        "run267T_pool_wide_orthogonal_stability_mt5_attempts",
        f"- run267T_pool_wide_orthogonal_stability_mt5_execution(267T 후보군 전체 직교 안정성 MT5 실행): `{rel(REPORT_PATH)}`",
    )
    write_md(REVIEW_INDEX_PATH, review)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_status_and_next_action(workspace, status, next_action)
    workspace = append_after_contains(
        workspace,
        "run267T_pool_wide_orthogonal_stability_mt5_attempts",
        f"  run267T_pool_wide_orthogonal_stability_mt5_execution_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def report_markdown(result: Mapping[str, Any], status: str, next_action: str) -> str:
    kpi_rows = list(result.get("kpi_summary_rows", []))
    attempts = list(result.get("attempts_executed", []))
    total_count = int(result.get("attempts_total_available", len(attempts)))
    completed_reports = sum(1 for row in result.get("strategy_tester_reports", []) if row.get("status") == "completed")
    blocked = len(attempts) - completed_reports
    judgment = backtest_judgment(status, len(result.get("mt5_kpi_records", [])))
    axis_count = len({str(row.get("axis_id")) for row in attempts if row.get("axis_id")})
    candidate_count = len({str(row.get("candidate_alias")) for row in attempts if row.get("candidate_alias")})
    lines = [
        "# Stage267 Run267T Pool-Wide Orthogonal Stability MT5 Execution(267단계 267T 후보군 전체 직교 안정성 MT5 실행)",
        "",
        f"- action(행동): `{len(attempts)}` of `{total_count}` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.",
        "- effect(효과): run267S(267S 실행)의 orthogonal stability matrix(직교 안정성 행렬)와 run267T(267T 실행)의 set/ini(설정/초기화) 묶음이 실제 tester output(테스터 출력), runtime telemetry(런타임 기록), KPI(핵심 성과 지표)로 이어지는지 확인한다.",
        f"- status(상태): `{status}`",
        f"- completed_reports(완료 보고서): `{completed_reports}`",
        f"- blocked_or_missing_reports(차단 또는 누락 보고서): `{blocked}`",
        f"- kpi_records(KPI 기록): `{len(result.get('mt5_kpi_records', []))}`",
        f"- candidates_touched(건드린 후보 수): `{candidate_count}`",
        f"- axes_touched(건드린 축 수): `{axis_count}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "이번 실행은 candidate selection(후보 선택)이 아니다. 효과는 후보군 전체 ablation/replacement(제거/대체)와 weak-slice resilience(약점 구간 견고성) 축이 MT5(MetaTrader 5, 메타트레이더5)에서 실제로 돌아가는지 먼저 확인하는 것이다.",
        "small tranche(작은 묶음)로 실행했다면, 효과는 고장난 batch(묶음)를 오래 밀지 않고 terminal/report/runtime(터미널/보고서/런타임) 경로를 먼저 확인하는 것이다.",
        "따라서 selected_candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 안 함)이다.",
        "",
        "## Runtime Parity(런타임 동등성)",
        "",
        f"- research_path(연구 경로): `{rel(materializer.PRODUCER_PATH)}` and `{rel(PRODUCER_PATH)}`.",
        f"- runtime_path(런타임 경로): EA entrypoint(EA 진입점) `{mt5.EA_SOURCE_PATH}`, attempt manifest(시도 목록) `{rel(ATTEMPT_MANIFEST_PATH)}`.",
        "- shared_contract(공유 계약): bar_time_server(서버 봉 시간), feature order hash(피처 순서 해시), CSV model table(CSV 모델 표), threshold(임계값), historical 2024 date range(2024 과거 기간).",
        "- known_differences(알려진 차이): axis03 prune/restore(가지치기/복귀) 축은 MT5 실행 축이 아니라 decision-only(판정 전용) 축이라 gap register(공백 등록부)에 남아 있다.",
        "- parity_check(동등성 확인): compile(컴파일), Strategy Tester report(전략 테스터 보고서), runtime telemetry(런타임 기록), KPI records(KPI 기록).",
        f"- parity_identity(동등성 정체성): execution result(실행 결과) `{rel(EXECUTION_RESULT_PATH)}`, runtime module hashes(런타임 모듈 해시)는 같은 파일에 기록했다.",
        "- runtime_claim_boundary(런타임 주장 경계): `runtime_probe(런타임 탐침)` only; runtime authority(런타임 권위)는 주장하지 않는다.",
        "",
        "## Backtest Forensics(백테스트 포렌식)",
        "",
        f"- tester_identity(테스터 정체성): terminal(터미널) `{TERMINAL_PATH_DEFAULT}`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델 방식) `4`, date range(기간) `2024.01.02` to `2025.01.01`.",
        f"- ea_identity(EA 정체성): entrypoint(진입점) `{mt5.EA_SOURCE_PATH}`, tester set(테스터 설정) `{EA_TESTER_SET_NAME}`.",
        f"- report_identity(보고서 정체성): execution result(실행 결과) `{rel(EXECUTION_RESULT_PATH)}`, forensics(포렌식) `{rel(FORENSICS_PATH)}`, KPI summary(KPI 요약) `{rel(KPI_SUMMARY_PATH)}`.",
        f"- trade_evidence(거래 근거): KPI records(KPI 기록) `{len(result.get('mt5_kpi_records', []))}`, strategy reports(전략 보고서) `{completed_reports}`.",
        "- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)는 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건을 따른다. 별도 비용 우위는 주장하지 않는다.",
        "- forensic_checks(포렌식 확인): settings drift(설정 이탈), missing report(보고서 누락), runtime telemetry(런타임 기록), malformed KPI(형식 오류 KPI)를 산출물로 분리했다.",
        f"- backtest_judgment(백테스트 판정): `{judgment}`.",
        "",
        "## Artifact Lineage(산출물 계보)",
        "",
        f"- source_inputs(원천 입력): `{rel(ATTEMPT_MANIFEST_PATH)}`, `{rel(VARIANT_MANIFEST_PATH)}`, `{rel(RUNTIME_CONTRACT_PATH)}`.",
        f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
        f"- consumer(소비자): next action(다음 행동) `{next_action}`.",
        f"- artifact_paths(산출물 경로): `{rel(EXECUTION_RESULT_PATH)}`, `{rel(KPI_SUMMARY_PATH)}`, `{rel(FORENSICS_PATH)}`, `{rel(EXECUTED_ATTEMPTS_PATH)}`.",
        "- artifact_hashes(산출물 해시): artifact_registry.csv(산출물 등록부)에 기록한다.",
        "- registry_links(등록부 연결): artifact_registry.csv, run_registry.csv, alpha_run_ledger.csv, stage_run_ledger.csv.",
        "- availability(가용성): tracked(추적됨) plus Common Files(공통 파일) runtime handoff(런타임 인계).",
        "- lineage_judgment(계보 판정): `connected_with_boundary`.",
        "",
        "## KPI Read(KPI 판독)",
        "",
    ]
    if kpi_rows:
        lines.extend(
            [
                "| candidate(후보) | axis(축) | test(시험) | record_view(기록 보기) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |",
                "| --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in kpi_rows:
            lines.append(
                f"| `{row.get('candidate_alias', '')}` | `{row.get('axis_id', '')}` | `{row.get('test_id', '')}` | `{row.get('record_view', '')}` | "
                f"{row.get('net_profit', '')} | {row.get('profit_factor', '')} | {row.get('trade_count', '')} | {row.get('max_drawdown_percent', '')} |"
            )
    else:
        lines.append("- KPI(핵심 성과 지표)가 없다. Effect(효과): 실행 차단 원인을 먼저 고쳐야 한다.")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- result_subject(결과 대상): `run267T_pool_wide_orthogonal_stability_mt5_execution`.",
            "- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식).",
            "- evidence_missing(빠진 근거): full batch completion(전체 묶음 완료) if partial(부분 실행이면), balance/equity curve(잔액/평가금 곡선) 확대 검토, time-slice KPI(시간 구간 핵심 성과 지표) 검토, final candidate selection(최종 후보 선택), ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- next_action(다음 행동): `{next_action}`.",
        ]
    )
    return "\n".join(lines)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    attempts, total_count = load_attempts(args.attempt_name or [], args.limit)
    if not attempts:
        raise RuntimeError("no run267T attempts selected")

    compile_payload = mt5.compile_mql5_ea(
        args.metaeditor_path,
        mt5.EA_SOURCE_PATH,
        COMPILE_LOG_PATH,
    )
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            clear_runtime_outputs(args.common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(args.terminal_data_root, attempt)
            tester_result = mt5.run_mt5_tester(
                args.terminal_path,
                Path(str(attempt["ini"]["path"])),
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=args.tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=args.tester_profile_root / f"opv2_s267t_{attempt['attempt_name']}.ini",
                timeout_seconds=args.timeout_seconds,
            )
            tester_result.update(
                {
                    "queue_id": attempt.get("queue_id"),
                    "source_queue_id": attempt.get("source_queue_id"),
                    "axis_id": attempt.get("axis_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "test_id": attempt.get("test_id"),
                    "test_type": attempt.get("test_type"),
                    "materialization_boundary": attempt.get("materialization_boundary"),
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "attempt_name": attempt["attempt_name"],
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "ini_path": attempt["ini"]["path"],
                }
            )
            if "routing_mode" in attempt:
                tester_result["routing_mode"] = attempt["routing_mode"]
            tester_result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(
                args.common_files_root,
                attempt,
                timeout_seconds=args.runtime_timeout_seconds,
                poll_seconds=2,
            )
            if tester_result["runtime_outputs"].get("status") != "completed":
                tester_result["status"] = "blocked"
            execution_results.append(tester_result)

    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=args.terminal_data_root,
        run_output_root=RUN_ROOT,
        attempts=attempts,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_rows = annotate_kpi_rows(run267b_executor.kpi_summary_rows(kpi_records), attempts)
    forensics = run267b_executor.forensic_rows(attempts, execution_results, report_records)
    base_status = run267b_executor.execution_status(execution_results, kpi_records)
    status = status_token(base_status, len(attempts), total_count)
    next_action = next_action_for(status, len(kpi_records), len(attempts), total_count)
    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "execution_status": status,
        "base_execution_status": base_status,
        "claim_boundary": CLAIM_BOUNDARY,
        "compile": compile_payload,
        "attempts_total_available": total_count,
        "attempts_executed": attempts,
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
        "kpi_summary_rows": kpi_rows,
        "backtest_forensics": forensics,
        "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
        "input_manifest": rel(ATTEMPT_MANIFEST_PATH),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
    }
    write_json(EXECUTION_RESULT_PATH, result)
    write_json(KPI_RECORDS_PATH, kpi_records)
    write_csv(KPI_SUMMARY_PATH, kpi_rows)
    write_csv(FORENSICS_PATH, forensics)
    write_csv(EXECUTED_ATTEMPTS_PATH, executed_attempt_rows(attempts, execution_results))
    write_md(REPORT_PATH, report_markdown(result, status, next_action))
    upsert_stage_ledger(status, len(kpi_records), next_action)
    upsert_run_registers(status, next_action, len(kpi_records))
    update_current_truth_docs(status, next_action, len(attempts), total_count, len(kpi_records))
    upsert_artifacts(created_at)
    return result


def finalize_existing() -> dict[str, Any]:
    if not path_exists(EXECUTION_RESULT_PATH):
        raise FileNotFoundError(EXECUTION_RESULT_PATH)
    result = json.loads(io_path(EXECUTION_RESULT_PATH).read_text(encoding="utf-8-sig"))
    status = str(result.get("execution_status") or BLOCKED_STATUS)
    next_action = str(result.get("next_action") or NEXT_ACTION_BLOCKED)
    attempt_count = len(result.get("attempts_executed", []))
    total_count = int(result.get("attempts_total_available", attempt_count))
    kpi_count = len(result.get("mt5_kpi_records", []))
    write_md(REPORT_PATH, report_markdown(result, status, next_action))
    upsert_stage_ledger(status, kpi_count, next_action)
    upsert_run_registers(status, next_action, kpi_count)
    update_current_truth_docs(status, next_action, attempt_count, total_count, kpi_count)
    upsert_artifacts(str(result.get("created_at_utc") or utc_now()))
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute run267T pool-wide orthogonal stability MT5 batch or tranche.")
    parser.add_argument("--attempt-name", action="append", default=[])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--finalize-existing", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=180)
    parser.add_argument("--terminal-path", type=Path, default=TERMINAL_PATH_DEFAULT)
    parser.add_argument("--metaeditor-path", type=Path, default=METAEDITOR_PATH_DEFAULT)
    parser.add_argument("--terminal-data-root", type=Path, default=TERMINAL_DATA_ROOT_DEFAULT)
    parser.add_argument("--common-files-root", type=Path, default=COMMON_FILES_ROOT_DEFAULT)
    parser.add_argument("--tester-profile-root", type=Path, default=TESTER_PROFILE_ROOT_DEFAULT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    result = finalize_existing() if args.finalize_existing else execute(args)
    print(
        json.dumps(
            {
                "execution_status": result["execution_status"],
                "attempt_count": len(result.get("attempts_executed", [])),
                "attempts_total_available": result.get("attempts_total_available"),
                "kpi_records": len(result.get("mt5_kpi_records", [])),
                "selected_candidate": result.get("selected_candidate"),
                "onnx_readiness": result.get("onnx_readiness"),
                "goal_achieve": result.get("goal_achieve"),
                "next_action": result.get("next_action"),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
