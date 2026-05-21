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

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
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
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage267 import historical_2024_mt5_executor as run267b_executor
from stage_pipelines.stage267 import run267AC_noncalendar_state_guard_score_table_materialization as materializer


STAGE_ID = materializer.STAGE_ID
SOURCE_RUN_ID = materializer.RUN_ID
RUN_NUMBER = "run267AD"
RUN_ID = "run267AD_stage267_noncalendar_state_guard_score_table_mt5_execution_v1"
STATUS_INPUT = materializer.STATUS
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY

STAGE_ROOT = materializer.STAGE_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "noncalendar_state_guard_score_table_mt5_execution"
SOURCE_RUN_ROOT = materializer.RUN_ROOT
SOURCE_RUN_MANIFEST_PATH = materializer.RUN_MANIFEST_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = materializer.ATTEMPT_MANIFEST_PATH
SOURCE_VARIANT_MANIFEST_PATH = materializer.VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = materializer.RUNTIME_CONTRACT_PATH
SOURCE_REPORT_PATH = materializer.REPORT_PATH

STAGE_LEDGER_PATH = materializer.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = materializer.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = materializer.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = materializer.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = materializer.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = materializer.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = materializer.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = materializer.REVIEW_INDEX_PATH

EXECUTION_RESULT_PATH = RUN_ROOT / "execution_result.json"
KPI_RECORDS_PATH = RUN_ROOT / "kpi_records.json"
KPI_SUMMARY_PATH = RUN_ROOT / "kpi_summary.csv"
FORENSICS_PATH = RUN_ROOT / "backtest_forensics.csv"
EXECUTED_ATTEMPTS_PATH = RUN_ROOT / "attempts_executed.csv"
COMPILE_LOG_PATH = RUN_ROOT / "mt5" / "compile_run267ad.log"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AD_noncalendar_state_guard_score_table_mt5_execution.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AD_noncalendar_state_guard_score_table_mt5_executor.py")

COMPLETED_STATUS = "run267AD_noncalendar_state_guard_score_table_mt5_batch_completed"
PARTIAL_STATUS = "run267AD_noncalendar_state_guard_score_table_mt5_batch_partial"
BLOCKED_STATUS = "run267AD_noncalendar_state_guard_score_table_mt5_batch_blocked"
NEXT_ACTION_COMPLETED = "run267AE_review_noncalendar_state_guard_score_table_mt5_results"
NEXT_ACTION_PARTIAL = "run267AD_execute_remaining_noncalendar_state_guard_score_table_mt5_batch"
NEXT_ACTION_BLOCKED = "run267AD_repair_noncalendar_state_guard_score_table_mt5_execution_blocker"

STAGE_LEDGER_COLUMNS = materializer.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = materializer.ARTIFACT_COLUMNS


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


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


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def selected_attempts(names: Sequence[str], limit: int | None) -> tuple[list[dict[str, Any]], int]:
    manifest = read_json(SOURCE_RUN_MANIFEST_PATH)
    rows = [dict(row) for row in manifest.get("attempts", [])]
    selected = rows
    if names:
        wanted = set(names)
        selected = [row for row in rows if row.get("attempt_name") in wanted]
    if limit is not None:
        selected = selected[: max(0, int(limit))]
    for row in selected:
        row.setdefault("split", "historical_2024_tier_a_train_era_stress")
        if bool_text(row.get("fallback_enabled")):
            row["routing_mode"] = mt5.ROUTING_MODE_A_B_FALLBACK
            row["routing_detail"] = "tier_a_primary_tier_b_partial_context_fallback"
    return selected, len(rows)


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


def annotate_kpi_rows(rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    annotated: list[dict[str, Any]] = []
    prefixes = [(str(attempt.get("record_view_prefix")), attempt) for attempt in attempts]
    for row in rows:
        next_row = dict(row)
        record_view = str(row.get("record_view", ""))
        for prefix, attempt in prefixes:
            if prefix and record_view.startswith(prefix):
                next_row["queue_id"] = attempt.get("queue_id")
                next_row["candidate_id"] = attempt.get("candidate_id")
                next_row["candidate_alias"] = attempt.get("candidate_alias")
                next_row["candidate_role"] = attempt.get("candidate_role")
                next_row["source_test_id"] = attempt.get("source_test_id")
                next_row["guard_rule_family"] = attempt.get("guard_rule_family")
                next_row["model_materialization_type"] = attempt.get("model_materialization_type")
                next_row["materialization_boundary"] = "noncalendar_state_guard_score_table_extension_not_retrained"
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
                "attempt_name": attempt.get("attempt_name"),
                "queue_id": attempt.get("queue_id"),
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "source_test_id": attempt.get("source_test_id"),
                "guard_rule_family": attempt.get("guard_rule_family"),
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
                "execution_status": result.get("status", "not_executed"),
                "runtime_status": result.get("runtime_outputs", {}).get("status") if isinstance(result, Mapping) else "",
                "report_status": result.get("strategy_tester_report", {}).get("status") if isinstance(result, Mapping) else "",
            }
        )
    return rows


def metric_text(row: Mapping[str, Any], key: str) -> str:
    value = row.get(key, "")
    return "" if value is None else str(value)


def row_count(rows: Sequence[Mapping[str, Any]], status: str) -> int:
    return sum(1 for row in rows if row.get("status") == status)


def report_markdown(result: Mapping[str, Any], status: str, next_action: str) -> str:
    kpi_rows = list(result.get("kpi_summary_rows", []))
    executed_count = len(result.get("attempts_executed", []))
    total_count = int(result.get("attempts_total_available", executed_count))
    completed_reports = row_count(list(result.get("strategy_tester_reports", [])), "completed")
    blocked = executed_count - completed_reports
    kpi_count = len(result.get("mt5_kpi_records", []))
    lines = [
        "# Stage267 Run267AD Noncalendar State Guard Score Table MT5 Execution(267단계 267AD 비달력 상태 방어 점수표 MT5 실행)",
        "",
        f"- action(행동): `{executed_count}` of `{total_count}` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.",
        "- effect(효과): run267AC(267AC 실행)의 score table/model/set/ini(점수표/모델/설정/초기화)가 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)로 이어지는지 확인한다.",
        f"- status(상태): `{status}`",
        f"- completed_reports(완료 보고서): `{completed_reports}`",
        f"- blocked_or_missing_reports(차단 또는 누락 보고서): `{blocked}`",
        f"- kpi_records(KPI 기록): `{kpi_count}`",
        f"- selected_candidate(선택 후보): `none`",
        f"- ONNX readiness(ONNX 준비): `not_claimed`",
        f"- Goal Achieve(목표 달성): `not_claimed`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267AB(267AB 실행)는 약한 거래가 몰리는 시장 상태를 찾았고, run267AC(267AC 실행)는 그 상태를 직접 잘라내지 않고 점수표에 작은 soft guard(부드러운 방어 장치)로 붙였다.",
        "run267AD(267AD 실행)는 그 입력을 MT5(MetaTrader 5, 메타트레이더5)에 실제로 넣어 본다. 효과(effect, 효과)는 숫자가 예뻐 보이는 설계와 실제 tester output(테스터 출력)을 분리하는 것이다.",
        "이번 실행은 후보 선택(candidate selection, 후보 선택)이나 ONNX(온닉스) 검토가 아니다. 다음 review(검토)에서 거래 수, 손실폭, 곡선, 시간 구간을 따로 봐야 한다.",
        "",
        "## Backtest Forensics(백테스트 포렌식)",
        "",
        f"- tester_identity(테스터 정체성): terminal(터미널) `{TERMINAL_PATH_DEFAULT}`, broker symbol(브로커 심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, modeling mode(모델링 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.",
        f"- ea_identity(EA 정체성): entrypoint(진입점) `{mt5.EA_SOURCE_PATH}`, tester set(테스터 설정) `{EA_TESTER_SET_NAME}`, module hashes(모듈 해시)는 `{rel(EXECUTION_RESULT_PATH)}`에 기록했다.",
        f"- report_identity(보고서 정체성): execution result(실행 결과) `{rel(EXECUTION_RESULT_PATH)}`, forensics(포렌식) `{rel(FORENSICS_PATH)}`, KPI summary(KPI 요약) `{rel(KPI_SUMMARY_PATH)}`.",
        f"- trade_evidence(거래 근거): completed reports(완료 보고서) `{completed_reports}`, KPI records(KPI 기록) `{kpi_count}`, attempt manifest(시도 목록) `{rel(EXECUTED_ATTEMPTS_PATH)}`.",
        "- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)는 MT5 Strategy Tester(MT5 전략 테스터)와 broker history(브로커 이력) 조건에 따른다. 별도 비용 우위 주장은 하지 않는다.",
        "- forensic_checks(포렌식 확인): set/ini hash(설정/초기화 해시), runtime summary(런타임 요약), Strategy Tester report(전략 테스터 보고서), copied report hash(복사 보고서 해시)를 확인했다.",
        f"- backtest_judgment(백테스트 판정): `{status}` with boundary(경계) `diagnostic_evidence_only_no_candidate_selection`.",
        "",
        "## KPI Read(KPI 판독)",
        "",
    ]
    if kpi_rows:
        lines.extend(
            [
                "| candidate(후보) | source_test(원천 시험) | tier(티어) | record_view(기록 보기) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |",
                "| --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in kpi_rows:
            lines.append(
                f"| `{row.get('candidate_alias', '')}` | `{row.get('source_test_id', '')}` | `{row.get('tier_scope', '')}` | `{row.get('record_view', '')}` | "
                f"{metric_text(row, 'net_profit')} | {metric_text(row, 'profit_factor')} | "
                f"{metric_text(row, 'trade_count')} | {metric_text(row, 'max_drawdown_percent')} |"
            )
    else:
        lines.append("- KPI(핵심 성과 지표)가 없다. Effect(효과): 실행 차단 원인을 먼저 고쳐야 하며 성능 판정은 하지 않는다.")
    lines.extend(
        [
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(SOURCE_RUN_MANIFEST_PATH)}`, `{rel(SOURCE_ATTEMPT_MANIFEST_PATH)}`, `{rel(SOURCE_VARIANT_MANIFEST_PATH)}`, `{rel(SOURCE_RUNTIME_CONTRACT_PATH)}`.",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
            f"- consumer(소비자): `{next_action}`.",
            f"- artifact_paths(산출물 경로): `{rel(EXECUTION_RESULT_PATH)}`, `{rel(KPI_RECORDS_PATH)}`, `{rel(KPI_SUMMARY_PATH)}`, `{rel(FORENSICS_PATH)}`, `{rel(REPORT_PATH)}`.",
            "- lineage_judgment(계보 판정): `connected_with_boundary`이다. MT5 execution(MT5 실행)은 연결됐지만 candidate selection(후보 선택)은 없다.",
            "",
            "## Result Judgment(결과 판정)",
            "",
            "- result_subject(결과 대상): `run267AD_noncalendar_state_guard_score_table_mt5_execution`.",
            "- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식), execution result(실행 결과).",
            "- evidence_missing(부족 근거): balance/equity curve(잔액/평가금 곡선) 상세 검토, time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질) 검토, 후보 탈락/유지 판단, ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            f"- next_condition(다음 조건): `{next_action}`.",
            "- user_explanation_hook(사용자 설명 핵심): 지금은 방어 점수표가 실제 MT5에서 돌아가는지 확인한 단계이고, 좋은 후보인지 여부는 다음 검토에서 곡선과 약한 구간까지 본 뒤에만 말할 수 있다.",
        ]
    )
    return "\n".join(lines)


def upsert_stage_ledger(status: str, kpi_count: int, next_action: str) -> None:
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267AD_noncalendar_state_guard_score_table_mt5_execution",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "noncalendar_state_guard_score_table_mt5_execution",
                "tier_scope": "Tier A and Tier A+B historical 2024 noncalendar state guard score table attempts",
                "scoreboard": "runtime_full_batch_or_tranche",
                "status": status,
                "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_mt5_execution",
                "evidence_boundary": "mt5_runtime_batch_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"kpi_records={kpi_count};next_action={next_action};selected_candidate=none.",
            }
        ],
        key="row_id",
    )


def upsert_run_registers(status: str, next_action: str, kpi_count: int) -> None:
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_candidate_racing_noncalendar_state_guard_score_table_mt5_execution",
                "status": status,
                "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_or_no_kpi",
                "path": rel(REPORT_PATH),
                "notes": (
                    "Run267AD noncalendar state guard score table MT5 execution; "
                    f"kpi_records={kpi_count}; selected_candidate=none; "
                    f"onnx_readiness=not_claimed; next_action={next_action}."
                ),
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__noncalendar_state_guard_score_table_mt5_execution",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "noncalendar_state_guard_score_table_mt5_execution",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "noncalendar_state_guard_score_table_mt5_execution",
                "tier_scope": "Tier A and Tier A+B historical 2024 noncalendar state guard score table attempts",
                "kpi_scope": "mt5_runtime_noncalendar_state_guard_score_table",
                "scoreboard_lane": "runtime_full_batch_or_tranche",
                "status": status,
                "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_or_no_kpi",
                "path": rel(REPORT_PATH),
                "primary_kpi": f"kpi_records={kpi_count}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "completed" if kpi_count else "blocked",
                "notes": f"Next action: {next_action}.",
            }
        ],
        key="ledger_row_id",
    )


def upsert_artifacts(created_at: str) -> None:
    entries = (
        ("stage267_run267AD_noncalendar_state_guard_executor", "producer_script", PRODUCER_PATH, "Executes run267AC noncalendar state guard score tables in MT5."),
        ("stage267_run267AD_source_run_manifest", "source_manifest", SOURCE_RUN_MANIFEST_PATH, "Source run267AC run manifest."),
        ("stage267_run267AD_source_attempt_manifest", "source_manifest", SOURCE_ATTEMPT_MANIFEST_PATH, "Source run267AC attempt manifest."),
        ("stage267_run267AD_source_variant_manifest", "source_manifest", SOURCE_VARIANT_MANIFEST_PATH, "Source run267AC variant manifest."),
        ("stage267_run267AD_source_runtime_contract", "source_contract", SOURCE_RUNTIME_CONTRACT_PATH, "Source run267AC runtime contract."),
        ("stage267_run267AD_compile_log", "compile_log", COMPILE_LOG_PATH, "MetaEditor compile log for run267AD."),
        ("stage267_run267AD_execution_result", "execution_result", EXECUTION_RESULT_PATH, "MT5 execution result payload for run267AD."),
        ("stage267_run267AD_kpi_records", "kpi_records", KPI_RECORDS_PATH, "MT5 KPI records for run267AD."),
        ("stage267_run267AD_kpi_summary", "kpi_summary", KPI_SUMMARY_PATH, "MT5 KPI summary for run267AD."),
        ("stage267_run267AD_forensics", "backtest_forensics", FORENSICS_PATH, "Tester identity and report evidence for run267AD."),
        ("stage267_run267AD_attempts_executed", "attempt_manifest", EXECUTED_ATTEMPTS_PATH, "Attempt list executed for run267AD."),
        ("stage267_run267AD_execution_report", "review_report", REPORT_PATH, "User-facing run267AD MT5 execution report."),
    )
    rows = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows = [
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
    replacement_ids = {row["artifact_id"] for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement_ids]
    merged.extend(new_rows)
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ARTIFACT_COLUMNS)


def update_workspace_state_text(text: str, status: str, next_action: str) -> str:
    lines = text.splitlines()
    in_stage267 = False
    inserted_path = False
    out: list[str] = []
    focus_block = [
        "- >-",
        f"  Stage267(267단계) run267AD(267AD 실행) noncalendar state guard score table MT5 execution(비달력 상태 방어 점수표 MT5 실행) `{status}`. Effect(효과): run267AC(267AC 실행)의 14개 MT5(MetaTrader 5, 메타트레이더5) 시도를 실행했고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    ]
    focus_inserted = False
    for line in lines:
        if line.startswith("current_run_id:"):
            out.append(f"current_run_id: {RUN_ID}")
            continue
        if line == "current_focus:" and not focus_inserted:
            out.append(line)
            out.extend(focus_block)
            focus_inserted = True
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            out.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                out.append(f"  status: {status}")
                continue
            if stripped.startswith("current_run_id:"):
                out.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                out.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                out.append(f"  next_action: {next_action}")
                continue
            if "run267AC_noncalendar_state_guard_score_table_materialization_report_path" in stripped and not inserted_path:
                out.append(line)
                out.append(f"  run267AD_noncalendar_state_guard_score_table_mt5_execution_report_path: {rel(REPORT_PATH)}")
                inserted_path = True
                continue
        out.append(line)
    if in_stage267 and not inserted_path:
        out.append(f"  run267AD_noncalendar_state_guard_score_table_mt5_execution_report_path: {rel(REPORT_PATH)}")
    return "\n".join(out) + "\n"


def update_current_truth_docs(status: str, next_action: str, attempt_count: int, total_count: int, kpi_count: int) -> None:
    report_line = f"- run267AD_noncalendar_state_guard_score_table_mt5_execution(267AD 비달력 상태 방어 점수표 MT5 실행): `{rel(REPORT_PATH)}`"
    latest_line = (
        f"- latest_mt5_execution(최신 MT5 실행): attempts(시도) `{attempt_count}` of `{total_count}`, "
        f"KPI records(KPI 기록) `{kpi_count}`, report(보고서) `{rel(REPORT_PATH)}`."
    )
    closing_block = "\n".join(
        [
            "Run267AD(267AD 실행)는 run267AC(267AC 실행)의 noncalendar state guard score table(비달력 상태 방어 점수표)을 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.",
            "Effect(효과): 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)를 얻었지만, 선택 후보(selected candidate, 선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.",
        ]
    )

    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_run(다음 실행):", f"- next_run(다음 실행): `{next_action}`")
    current = replace_line_prefix(
        current,
        "- action(행동):",
        "- action(행동): run267AD(267AD 실행)는 run267AC(267AC 실행)의 14개 noncalendar state guard score table MT5 attempts(비달력 상태 방어 점수표 MT5 시도)를 실행했다.",
    )
    current = replace_line_prefix(
        current,
        "- effect(효과):",
        "- effect(효과): 다음 run267AE(267AE 실행)에서 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 검토할 수 있게 실제 tester output(테스터 출력)을 확보했다.",
    )
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    current = append_after_contains(current, "run267AC_noncalendar_state_guard_score_table_materialization", report_line)
    current = append_after_contains(current, "## Current Next Action", latest_line)
    current = append_block_once(current, "Run267AD(267AD 실행)는 run267AC", closing_block)
    write_text(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selection = append_after_contains(selection, "run267AC_noncalendar_state_guard_score_table_materialization", report_line)
    selection = append_block_once(selection, "Run267AD(267AD 실행)는 run267AC", closing_block)
    write_text(SELECTION_STATUS_PATH, selection)

    review = read_text(REVIEW_INDEX_PATH)
    review = replace_line_prefix(review, "- status(상태):", f"- status(상태): `{status}`")
    review = replace_line_prefix(review, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review = replace_line_prefix(review, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review = replace_line_prefix(review, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    review = append_after_contains(review, "run267AC_noncalendar_state_guard_score_table_materialization", report_line)
    review = append_block_once(review, "Run267AD(267AD 실행)는 run267AC", closing_block)
    write_text(REVIEW_INDEX_PATH, review)

    workspace = read_text(WORKSPACE_STATE_PATH)
    write_text(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace, status, next_action))


def execute(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    attempts, total_count = selected_attempts(args.attempt_name or [], args.limit)
    if not attempts:
        raise RuntimeError("no run267AD attempts selected")

    compile_payload = mt5.compile_mql5_ea(
        args.metaeditor_path,
        mt5.EA_SOURCE_PATH,
        COMPILE_LOG_PATH,
    )
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            clear_runtime_outputs(args.common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(args.terminal_data_root, attempt, run_id=RUN_ID)
            tester_result = mt5.run_mt5_tester(
                args.terminal_path,
                Path(str(attempt["ini"]["path"])),
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=args.tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=args.tester_profile_root / f"opv2_s267ad_{attempt['attempt_name']}.ini",
                timeout_seconds=args.timeout_seconds,
            )
            tester_result.update(
                {
                    "queue_id": attempt.get("queue_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "source_test_id": attempt.get("source_test_id"),
                    "guard_rule_family": attempt.get("guard_rule_family"),
                    "model_materialization_type": attempt.get("model_materialization_type"),
                    "materialization_boundary": "noncalendar_state_guard_score_table_extension_not_retrained",
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
        run_id=RUN_ID,
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
        "source_run_id": SOURCE_RUN_ID,
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
        "input_manifest": rel(SOURCE_RUN_MANIFEST_PATH),
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
    result = read_json(EXECUTION_RESULT_PATH)
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
    parser = argparse.ArgumentParser(description="Execute run267AD noncalendar state guard score table MT5 batch.")
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
                "next_action": result["next_action"],
                "selected_candidate": result.get("selected_candidate"),
                "onnx_readiness": result.get("onnx_readiness"),
                "goal_achieve": result.get("goal_achieve"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
