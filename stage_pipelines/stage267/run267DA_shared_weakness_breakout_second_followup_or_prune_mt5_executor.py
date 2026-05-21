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
from stage_pipelines.stage267 import run267CO_pool_wide_shared_weakness_breakout_mt5_executor as base_executor
from stage_pipelines.stage267 import run267CZ_shared_weakness_breakout_second_followup_or_prune_materialization as materializer


STAGE_ID = materializer.STAGE_ID
RUN_NUMBER = "run267DA"
RUN_ID = "run267DA_stage267_shared_weakness_breakout_second_followup_or_prune_mt5_execution_v1"
SOURCE_RUN_ID = materializer.RUN_ID
PARENT_RUN_ID = materializer.PARENT_RUN_ID
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY

STAGE_ROOT = materializer.STAGE_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_second_followup_or_prune_mt5_execution"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_RUN_MANIFEST_PATH = materializer.RUN_MANIFEST_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = materializer.ATTEMPT_MANIFEST_PATH
SOURCE_VARIANT_MANIFEST_PATH = materializer.VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = materializer.RUNTIME_CONTRACT_PATH
SOURCE_GATE_AUDIT_PATH = materializer.GATE_AUDIT_PATH
SOURCE_REPORT_PATH = materializer.REPORT_PATH

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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DA_shared_weakness_breakout_second_followup_or_prune_mt5_execution.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DA_shared_weakness_breakout_second_followup_or_prune_mt5_executor.py")
COMPILE_LOG_PATH = MT5_ROOT / "compile_run267da.log"

STAGE_LEDGER_PATH = materializer.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = materializer.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = materializer.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = materializer.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = materializer.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = materializer.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = materializer.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = materializer.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = materializer.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = materializer.ARTIFACT_COLUMNS

COMPLETED_STATUS = "run267DA_shared_weakness_breakout_second_followup_or_prune_mt5_batch_completed"
PARTIAL_STATUS = "run267DA_shared_weakness_breakout_second_followup_or_prune_mt5_batch_partial"
BLOCKED_STATUS = "run267DA_shared_weakness_breakout_second_followup_or_prune_mt5_batch_blocked"
NEXT_COMPLETED = "run267DB_review_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality"
NEXT_PARTIAL = "run267DA_execute_remaining_shared_weakness_breakout_second_followup_or_prune_mt5_batch"
NEXT_BLOCKED = "run267DA_repair_shared_weakness_breakout_second_followup_or_prune_mt5_execution_blocker"

TIER_PAIR_BOUNDARY = materializer.TIER_PAIR_BOUNDARY
MATERIALIZATION_BOUNDARY = materializer.MATERIALIZATION_BOUNDARY
COMMON_TELEMETRY_ROOT = "OPV2/s267da/run267DA_shared_weakness_second_followup_or_prune/telemetry"
EXPLORATION_LABEL = "stage267_BaselineRacing__SharedWeaknessSecondFollowupOrPruneMT5"
DEFAULT_SPLIT = "historical_2024"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else REPO_ROOT / path


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


def write_set(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["; generated_by=run267DA_shared_weakness_breakout_second_followup_or_prune_mt5_executor"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path), "format": "mt5_set"}


def write_ini(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["[Tester]"]
    lines.extend(f"{key}={cell(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path),
        "format": "mt5_tester_ini",
        "tester": dict(values),
    }


def configure_base_executor() -> None:
    assignments: dict[str, Any] = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "SOURCE_RUN_ID": SOURCE_RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "STAGE_ROOT": STAGE_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "MT5_ROOT": MT5_ROOT,
        "SOURCE_RUN_MANIFEST_PATH": SOURCE_RUN_MANIFEST_PATH,
        "SOURCE_ATTEMPT_MANIFEST_PATH": SOURCE_ATTEMPT_MANIFEST_PATH,
        "SOURCE_VARIANT_MANIFEST_PATH": SOURCE_VARIANT_MANIFEST_PATH,
        "SOURCE_RUNTIME_CONTRACT_PATH": SOURCE_RUNTIME_CONTRACT_PATH,
        "SOURCE_GATE_AUDIT_PATH": SOURCE_GATE_AUDIT_PATH,
        "SOURCE_REPORT_PATH": SOURCE_REPORT_PATH,
        "EXECUTION_RESULT_PATH": EXECUTION_RESULT_PATH,
        "KPI_RECORDS_PATH": KPI_RECORDS_PATH,
        "KPI_SUMMARY_PATH": KPI_SUMMARY_PATH,
        "FORENSICS_PATH": FORENSICS_PATH,
        "EXECUTED_ATTEMPTS_PATH": EXECUTED_ATTEMPTS_PATH,
        "PROFILE_ENCODING_RECEIPT_PATH": PROFILE_ENCODING_RECEIPT_PATH,
        "RUNTIME_PARITY_RECEIPT_PATH": RUNTIME_PARITY_RECEIPT_PATH,
        "RESULT_JUDGMENT_PATH": RESULT_JUDGMENT_PATH,
        "RUN_MANIFEST_PATH": RUN_MANIFEST_PATH,
        "LINEAGE_PATH": LINEAGE_PATH,
        "REPORT_PATH": REPORT_PATH,
        "PRODUCER_PATH": PRODUCER_PATH,
        "COMPILE_LOG_PATH": COMPILE_LOG_PATH,
        "COMPLETED_STATUS": COMPLETED_STATUS,
        "PARTIAL_STATUS": PARTIAL_STATUS,
        "BLOCKED_STATUS": BLOCKED_STATUS,
        "NEXT_COMPLETED": NEXT_COMPLETED,
        "NEXT_PARTIAL": NEXT_PARTIAL,
        "NEXT_BLOCKED": NEXT_BLOCKED,
        "TIER_PAIR_BOUNDARY": TIER_PAIR_BOUNDARY,
        "MATERIALIZATION_BOUNDARY": MATERIALIZATION_BOUNDARY,
        "COMMON_TELEMETRY_ROOT": COMMON_TELEMETRY_ROOT,
        "EXPLORATION_LABEL": EXPLORATION_LABEL,
        "DEFAULT_SPLIT": DEFAULT_SPLIT,
        "write_set": write_set,
        "write_ini": write_ini,
    }
    for name, value in assignments.items():
        setattr(base_executor, name, value)


def source_attempt_rows() -> list[dict[str, str]]:
    rows = base_executor.read_csv(SOURCE_ATTEMPT_MANIFEST_PATH)
    if not rows:
        raise RuntimeError(f"missing source attempt manifest: {rel(SOURCE_ATTEMPT_MANIFEST_PATH)}")
    return rows


def prepare_execution_attempt(row: Mapping[str, str]) -> dict[str, Any]:
    attempt_name = str(row["attempt_name"])
    source_set_path = repo_path(str(row["set_path"]))
    source_ini_path = repo_path(str(row["ini_path"]))
    if not path_exists(source_set_path):
        raise FileNotFoundError(source_set_path)
    if not path_exists(source_ini_path):
        raise FileNotFoundError(source_ini_path)

    telemetry = f"{COMMON_TELEMETRY_ROOT}/{attempt_name}_telemetry.csv"
    summary = f"{COMMON_TELEMETRY_ROOT}/{attempt_name}_summary.csv"

    set_values = base_executor.parse_key_values(source_set_path)
    set_values.update(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTelemetryCsvPath": telemetry,
            "InpSummaryCsvPath": summary,
            "InpTelemetryUseCommonFiles": "true",
        }
    )
    set_payload = write_set(MT5_ROOT / f"{attempt_name}.set", set_values)

    ini_values = base_executor.parse_key_values(source_ini_path)
    ini_values.update(
        {
            "ExpertParameters": EA_TESTER_SET_NAME,
            "Report": f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}",
            "ReplaceReport": 1,
            "ShutdownTerminal": 1,
        }
    )
    ini_payload = write_ini(MT5_ROOT / f"{attempt_name}.ini", ini_values)

    attempt = dict(row)
    attempt.update(
        {
            "split": row.get("split") or DEFAULT_SPLIT,
            "source_set_path": row.get("set_path"),
            "source_ini_path": row.get("ini_path"),
            "source_set_sha256": row.get("set_sha256"),
            "source_ini_sha256": row.get("ini_sha256"),
            "set": set_payload,
            "ini": ini_payload,
            "common_telemetry_path": telemetry,
            "common_summary_path": summary,
            "tier_pair_boundary": row.get("tier_pair_boundary") or TIER_PAIR_BOUNDARY,
            "materialization_boundary": MATERIALIZATION_BOUNDARY,
            "execution_status": "execution_prepared",
        }
    )
    return attempt


def load_attempts(names: Sequence[str], limit: int | None) -> tuple[list[dict[str, Any]], int]:
    rows = source_attempt_rows()
    selected = rows
    if names:
        wanted = set(names)
        selected = [row for row in rows if row.get("attempt_name") in wanted]
    if limit is not None:
        selected = selected[: max(0, limit)]
    attempts = [prepare_execution_attempt(row) for row in selected]
    return attempts, len(rows)


def runtime_parity_rows(
    profile_rows: Sequence[Mapping[str, Any]],
    kpi_count: int,
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
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
            "status": "completed" if kpi_count else "blocked",
            "value": str(kpi_count),
            "effect": "CSV handoff(CSV 인계)와 strategy report(전략 보고서)가 KPI(핵심 성과 지표)로 이어지는지 확인했다.",
            "runtime_claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "field": "tier_boundary",
            "status": "duplicate_boundary_only",
            "value": TIER_PAIR_BOUNDARY,
            "effect": "Tier A+B(티어 A+B)는 true fallback(실제 대체)이 아니라 duplicate-boundary(중복 경계)임을 고정했다.",
            "runtime_claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "field": "attempt_count",
            "status": "checked",
            "value": str(len(attempts)),
            "effect": "run267CZ(267CZ 실행) 물질화 입력이 run267DA(267DA 실행) 범위로 이어졌는지 확인했다.",
            "runtime_claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def result_judgment_rows(status: str, next_action: str) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267DA shared weakness second follow-up/prune MT5 execution(267DA 공유 약점 후속/가지치기 MT5 실행)",
            "evidence_available": "MT5 compile log(MT5 컴파일 로그), tester profiles(테스터 프로필), runtime outputs(런타임 출력), strategy reports(전략 보고서), KPI rows(KPI 행) if produced",
            "evidence_missing": "balance/equity curve review(잔액/평가금 곡선 검토), trade-list time-slice review(거래 목록 시간구간 검토), Adapter package(어댑터 패키지), ONNX parity(ONNX 동등성)",
            "judgment_label": "runtime_probe(런타임 탐침)" if status != BLOCKED_STATUS else "blocked(차단)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": "이번 실행은 후보 선택이 아니라 run267CZ 입력이 MT5에서 실제 결과로 이어지는지 확인하는 작업이다.",
        }
    ]


def report_markdown(result: Mapping[str, Any], status: str, next_action: str) -> str:
    kpi_rows = list(result.get("kpi_summary_rows", []))
    forensics = list(result.get("backtest_forensics", []))
    profile_rows = list(result.get("profile_encoding_rows", []))
    lines = [
        "# Stage267 Run267DA Shared Weakness Second Follow-up/Prune MT5 Execution(267단계 267DA 공유 약점 후속/가지치기 MT5 실행)",
        "",
        f"- status(상태): `{status}`",
        f"- attempts(시도): `{len(result.get('attempts_executed', []))}/{result.get('attempts_total_available')}`",
        f"- KPI records(KPI 기록): `{len(result.get('mt5_kpi_records', []))}`",
        f"- next_action(다음 행동): `{next_action}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267DA(267DA 실행)는 run267CZ(267CZ 실행)가 만든 10개 MT5(MetaTrader 5, 메타트레이더5) 입력을 Strategy Tester(전략 테스터)에 넘겼다.",
        "효과: redzone Monday/DD pressure(위험 구역 월요일/손실폭 압박), explosive shock-state combo(폭발형 충격-상태 조합), s264_aih supply repair(s264_aih 공급 수리)가 실제 report(보고서)와 KPI(핵심 성과 지표)로 이어지는지 확인한다.",
        "",
        "## Boundary(경계)",
        "",
        "- 이 실행은 runtime probe(런타임 탐침)이며 runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포)를 주장하지 않는다.",
        "- Tier A+B(티어 A+B)는 duplicate-boundary(중복 경계) 입력이다. true Tier B fallback(실제 티어 B 대체) 근거로 해석하지 않는다.",
        "- 다음 run267DB(267DB 실행)에서 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 봐야 한다.",
        "",
        "## KPI Preview(KPI 미리보기)",
        "",
        "| candidate(후보) | profile(프로필) | tier(티어) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | status(상태) |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]
    for row in kpi_rows:
        lines.append(
            "| "
            f"`{row.get('candidate_alias', '')}` | `{row.get('profile_label', '')}` | `{row.get('tier_scope', '')}` | "
            f"{row.get('net_profit', '')} | {row.get('profit_factor', '')} | {row.get('trade_count', '')} | "
            f"{row.get('max_drawdown_percent', '')} | `{row.get('status', '')}` |"
        )
    if not kpi_rows:
        lines.append("| missing(누락) | missing(누락) | missing(누락) |  |  |  |  | `no_kpi_records` |")
    lines.extend(
        [
            "",
            "## Forensics(포렌식)",
            "",
            f"- forensics rows(포렌식 행): `{len(forensics)}`",
            f"- tester profile rows(테스터 프로필 행): `{len(profile_rows)}`",
            f"- compile status(컴파일 상태): `{dict(result.get('compile', {})).get('status')}`",
            f"- runtime module hashes(런타임 모듈 해시): `{len(result.get('runtime_module_hashes', []))}`",
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
        "judgment": "mt5_runtime_probe_no_candidate_selection" if result.get("mt5_kpi_records") else "blocked_no_kpi",
        "attempt_count": len(result.get("attempts_executed", [])),
        "attempts_total_available": result.get("attempts_total_available"),
        "kpi_records": len(result.get("mt5_kpi_records", [])),
        "next_action": next_action,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_run_payloads(
    result: Mapping[str, Any],
    status: str,
    next_action: str,
    profile_rows: Sequence[Mapping[str, Any]],
) -> None:
    write_json(EXECUTION_RESULT_PATH, result)
    write_json(KPI_RECORDS_PATH, result.get("mt5_kpi_records", []))
    write_csv(KPI_SUMMARY_PATH, result.get("kpi_summary_rows", []))
    write_csv(FORENSICS_PATH, result.get("backtest_forensics", []))
    write_csv(EXECUTED_ATTEMPTS_PATH, base_executor.executed_attempt_rows(result.get("attempts_executed", []), result.get("execution_results", [])))
    write_csv(PROFILE_ENCODING_RECEIPT_PATH, profile_rows)
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, runtime_parity_rows(profile_rows, len(result.get("mt5_kpi_records", [])), result.get("attempts_executed", [])))
    write_csv(RESULT_JUDGMENT_PATH, result_judgment_rows(status, next_action))
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "source_run_id": SOURCE_RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "stage_id": STAGE_ID,
            "status": status,
            "attempt_count": len(result.get("attempts_executed", [])),
            "attempts_total_available": result.get("attempts_total_available"),
            "kpi_records": len(result.get("mt5_kpi_records", [])),
            "kpi_record_count": len(result.get("mt5_kpi_records", [])),
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
            "sources": {
                "source_run_manifest": rel(SOURCE_RUN_MANIFEST_PATH),
                "source_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
                "source_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
                "source_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
                "source_gate_audit": rel(SOURCE_GATE_AUDIT_PATH),
                "source_report": rel(SOURCE_REPORT_PATH),
            },
            "outputs": {
                "execution_result": rel(EXECUTION_RESULT_PATH),
                "kpi_summary": rel(KPI_SUMMARY_PATH),
                "backtest_forensics": rel(FORENSICS_PATH),
                "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
                "report": rel(REPORT_PATH),
            },
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(REVIEW_RESULT_PATH, review_result_payload(result, status, next_action))
    write_md(REPORT_PATH, report_markdown(result, status, next_action))


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267DA_producer", "producer_script", PRODUCER_PATH, "Executes run267DA shared weakness second follow-up/prune MT5 batch."),
        ("stage267_run267DA_source_manifest", "source_manifest", SOURCE_RUN_MANIFEST_PATH, "Source run267CZ manifest."),
        ("stage267_run267DA_compile_log", "compile_log", COMPILE_LOG_PATH, "MetaEditor compile log."),
        ("stage267_run267DA_execution_result", "execution_result", EXECUTION_RESULT_PATH, "MT5 execution result payload."),
        ("stage267_run267DA_kpi_records", "kpi_records", KPI_RECORDS_PATH, "MT5 KPI records."),
        ("stage267_run267DA_kpi_summary", "kpi_summary", KPI_SUMMARY_PATH, "MT5 KPI summary."),
        ("stage267_run267DA_forensics", "backtest_forensics", FORENSICS_PATH, "Backtest forensics."),
        ("stage267_run267DA_attempts_executed", "attempts_executed", EXECUTED_ATTEMPTS_PATH, "Executed attempts."),
        ("stage267_run267DA_profile_encoding", "profile_encoding_receipt", PROFILE_ENCODING_RECEIPT_PATH, "Profile encoding receipt."),
        ("stage267_run267DA_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267DA_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DA_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267DA_lineage", "lineage", LINEAGE_PATH, "Lineage map."),
        ("stage267_run267DA_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267DA_report", "review_report", REPORT_PATH, "User-facing report."),
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


def upsert_ledgers(status: str, next_action: str, kpi_count: int, attempt_count: int, total_count: int) -> None:
    judgment = "mt5_runtime_probe_no_candidate_selection" if kpi_count else "blocked_no_kpi"
    stage_row = {
        "row_id": "stage267_run267DA_shared_weakness_breakout_second_followup_or_prune_mt5_execution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_second_followup_or_prune_mt5_execution",
        "tier_scope": "Tier A and duplicate Tier A+B boundary; true fallback not claimed",
        "scoreboard": "mt5_runtime_shared_weakness_second_followup_or_prune",
        "status": status,
        "judgment": judgment,
        "evidence_boundary": "mt5_strategy_tester_reports_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"kpi_records={kpi_count};attempts={attempt_count}/{total_count};next_action={next_action}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "shared_weakness_breakout_second_followup_or_prune_mt5_execution",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "notes": f"kpi_records={kpi_count};selected_candidate=none;onnx_readiness=not_claimed.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__shared_weakness_breakout_second_followup_or_prune_mt5_execution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "shared_weakness_breakout_second_followup_or_prune_mt5_execution",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "shared_weakness_breakout_second_followup_or_prune_mt5_execution",
        "tier_scope": "Tier A and duplicate Tier A+B boundary",
        "kpi_scope": "mt5_runtime_shared_weakness_second_followup_or_prune",
        "scoreboard_lane": "shared_weakness_second_followup_or_prune_execution",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"kpi_records={kpi_count};attempts={attempt_count}/{total_count}",
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
            lines.insert(index + 1, line)
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
    report_entry = f"  run267DA_shared_weakness_breakout_second_followup_or_prune_mt5_execution_report_path: {rel(REPORT_PATH)}"
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


def update_docs(status: str, next_action: str, kpi_count: int, attempt_count: int, total_count: int) -> None:
    report_line = (
        "- run267DA_shared_weakness_breakout_second_followup_or_prune_mt5_execution"
        f"(267DA 공유 약점 후속/가지치기 MT5 실행): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267DA(267DA 실행)는 run267CZ(267CZ 실행)의 shared weakness second follow-up/prune(공유 약점 후속/가지치기) attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.",
            f"Effect(효과): attempt(시도) `{attempt_count}/{total_count}`개 중 KPI records(KPI 기록) `{kpi_count}`개를 만들었고, 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- status(", f"- status(상태): `{status}`")
            text = replace_line_containing(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_second_followup_or_prune_mt5_execution`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "stage267_run267CZ_shared_weakness_breakout_second_followup_or_prune_materialization.md", report_line)
            text = append_block_once(text, "Run267DA(267DA 실행)는 run267CZ", block)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_containing(text, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "stage267_run267CZ_shared_weakness_breakout_second_followup_or_prune_materialization.md", report_line)
            text = append_block_once(text, "Run267DA(267DA 실행)는 run267CZ", block)
        else:
            text = replace_line_containing(text, "- status(", f"- status(상태): `{status}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "stage267_run267CZ_shared_weakness_breakout_second_followup_or_prune_materialization.md", report_line)
            text = append_block_once(text, "Run267DA(267DA 실행)는 run267CZ", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_containing(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267DA(267DA 실행) shared weakness breakout second follow-up/prune MT5 execution"
        f"(공유 약점 돌파 후속/가지치기 MT5 실행) `{status}`. "
        f"Effect(효과): run267CZ(267CZ 실행)의 attempt(시도) `{attempt_count}/{total_count}`개를 MT5(MetaTrader 5, 메타트레이더5) tester output(테스터 출력)과 KPI(핵심 성과 지표)에 연결했고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(workspace, status=status, next_action=next_action)
    write_md(WORKSPACE_STATE_PATH, workspace)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    configure_base_executor()
    created_at = utc_now()
    attempts, total_count = load_attempts(args.attempt_name or [], args.limit)
    if not attempts:
        raise RuntimeError("no run267DA attempts selected")

    for attempt in attempts:
        clear_runtime_outputs(args.common_files_root, attempt)
        base_executor.mt5.remove_existing_mt5_report_artifacts(args.terminal_data_root, attempt, run_id=RUN_ID)

    compile_payload = base_executor.mt5.compile_mql5_ea(args.metaeditor_path, base_executor.mt5.EA_SOURCE_PATH, COMPILE_LOG_PATH)
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            tester_result = base_executor.mt5.run_mt5_tester(
                args.terminal_path,
                Path(str(attempt["ini"]["path"])),
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=args.tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=args.tester_profile_root / f"opv2_s267da_{attempt['attempt_name']}.ini",
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
            tester_result["runtime_outputs"] = base_executor.mt5.wait_for_mt5_runtime_outputs(
                args.common_files_root,
                attempt,
                timeout_seconds=args.runtime_timeout_seconds,
                poll_seconds=2,
            )
            if tester_result["runtime_outputs"].get("status") != "completed":
                tester_result["status"] = "blocked"
            execution_results.append(tester_result)

    report_records = base_executor.mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=args.terminal_data_root,
        run_output_root=RUN_ROOT,
        attempts=attempts,
        run_id=RUN_ID,
    )
    report_records = supplement_truncated_html_reports(
        report_records,
        attempts,
        terminal_data_root=args.terminal_data_root,
        run_output_root=RUN_ROOT,
    )
    base_executor.mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = base_executor.mt5.build_mt5_kpi_records(execution_results)
    kpi_rows = base_executor.annotate_kpi_rows(historical_executor.kpi_summary_rows(kpi_records), attempts)
    forensics = base_executor.annotate_forensic_rows(historical_executor.forensic_rows(attempts, execution_results, report_records), attempts)
    base_status = historical_executor.execution_status(execution_results, kpi_records)
    status = base_executor.status_token(base_status, len(attempts), total_count, len(kpi_records))
    next_action = base_executor.next_action_for(status, len(attempts), total_count, len(kpi_records))
    profile_rows = base_executor.profile_encoding_rows(execution_results)
    result = {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
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
        "profile_encoding_rows": profile_rows,
        "runtime_module_hashes": base_executor.mt5.mt5_runtime_module_hashes(),
        "input_manifest": rel(SOURCE_RUN_MANIFEST_PATH),
        "source_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
    }
    write_run_payloads(result, status, next_action, profile_rows)
    upsert_ledgers(status, next_action, len(kpi_records), len(attempts), total_count)
    update_docs(status, next_action, len(kpi_records), len(attempts), total_count)
    return result


def supplement_truncated_html_reports(
    report_records: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    *,
    terminal_data_root: Path,
    run_output_root: Path,
) -> list[dict[str, Any]]:
    reports_root = run_output_root / "mt5" / "reports"
    io_path(reports_root).mkdir(parents=True, exist_ok=True)
    by_attempt = {str(record.get("attempt_name")): dict(record) for record in report_records}
    repaired: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt.get("attempt_name"))
        record = by_attempt.get(
            attempt_name,
            {
                "attempt_name": attempt_name,
                "tier": attempt.get("tier"),
                "report_name": base_executor.mt5.report_name_from_attempt(attempt, run_id=RUN_ID),
                "status": "missing",
            },
        )
        if record.get("status") == "completed":
            repaired.append(record)
            continue
        report_name = str(record.get("report_name") or base_executor.mt5.report_name_from_attempt(attempt, run_id=RUN_ID))
        truncated_source = terminal_data_root / f"{report_name}.h"
        if not path_exists(truncated_source):
            repaired.append(record)
            continue
        html_destination = reports_root / f"{report_name}.htm"
        shutil.copy2(io_path(truncated_source), io_path(html_destination))
        record["html_report"] = {
            "source_path": truncated_source.as_posix(),
            "path": html_destination.as_posix(),
            "sha256": sha256_file_lf_normalized(html_destination),
            "salvage_note": "truncated_htm_extension_from_mt5_dot_h",
        }
        record["metrics"] = base_executor.extract_mt5_strategy_report_metrics(html_destination)
        record["status"] = record["metrics"]["status"]
        record["truncated_report_salvage"] = "completed_from_dot_h"
        repaired.append(record)
    return repaired


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute run267DA shared weakness second follow-up/prune attempts in MT5.")
    parser.add_argument("--attempt-name", action="append", default=[])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=120)
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
                "attempt_count": len(result.get("attempts_executed", [])),
                "attempts_total_available": result.get("attempts_total_available"),
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
