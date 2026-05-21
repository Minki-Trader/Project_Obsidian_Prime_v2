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
from foundation.mt5 import runtime_support as mt5
from foundation.mt5.runtime_artifacts import extract_mt5_strategy_report_metrics
from stage_pipelines.stage267 import historical_2024_mt5_executor as historical_executor
from stage_pipelines.stage267 import run267BS_pool_wide_directional_impulse_followup_materialization as materializer


STAGE_ID = materializer.STAGE_ID
RUN_NUMBER = "run267BT"
RUN_ID = "run267BT_stage267_pool_wide_directional_impulse_followup_mt5_execution_v1"
SOURCE_RUN_ID = materializer.RUN_ID
PARENT_RUN_ID = materializer.PARENT_RUN_ID
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY

STAGE_ROOT = materializer.STAGE_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_directional_impulse_followup_mt5_execution"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_RUN_MANIFEST_PATH = materializer.RUN_MANIFEST_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = materializer.ATTEMPT_MANIFEST_PATH
SOURCE_VARIANT_MANIFEST_PATH = materializer.VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = materializer.RUNTIME_CONTRACT_PATH
SOURCE_ROUTE_GAP_AUDIT_PATH = materializer.ROUTE_GAP_AUDIT_PATH
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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BT_pool_wide_directional_impulse_followup_mt5_execution.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BT_pool_wide_directional_impulse_followup_mt5_executor.py")
COMPILE_LOG_PATH = MT5_ROOT / "compile_run267bt.log"

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

COMPLETED_STATUS = "run267BT_pool_wide_directional_impulse_followup_mt5_batch_completed"
PARTIAL_STATUS = "run267BT_pool_wide_directional_impulse_followup_mt5_batch_partial"
BLOCKED_STATUS = "run267BT_pool_wide_directional_impulse_followup_mt5_batch_blocked"
NEXT_COMPLETED = "run267BU_review_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality"
NEXT_PARTIAL = "run267BT_execute_remaining_pool_wide_directional_impulse_followup_mt5_batch"
NEXT_BLOCKED = "run267BT_repair_pool_wide_directional_impulse_followup_mt5_execution_blocker"

TIER_PAIR_BOUNDARY = materializer.MATERIALIZATION_BOUNDARY
MATERIALIZATION_BOUNDARY = materializer.MATERIALIZATION_BOUNDARY
COMMON_TELEMETRY_ROOT = "OPV2/s267bt/run267BT_directional_impulse_followup/telemetry"
EXPLORATION_LABEL = "stage267_BaselineRacing__DirectionalImpulseFollowupMT5"


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


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


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def parse_key_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        if not line or line.lstrip().startswith(";") or "=" not in line or line.startswith("["):
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def write_set(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["; generated_by=run267BT_pool_wide_directional_impulse_followup_mt5_executor"]
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


def source_attempt_rows() -> list[dict[str, str]]:
    rows = read_csv(SOURCE_ATTEMPT_MANIFEST_PATH)
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

    set_values = parse_key_values(source_set_path)
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

    ini_values = parse_key_values(source_ini_path)
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


def status_token(base_status: str, selected_count: int, total_count: int, kpi_count: int) -> str:
    if base_status == "completed" and selected_count == total_count and kpi_count == selected_count:
        return COMPLETED_STATUS
    if kpi_count:
        return PARTIAL_STATUS
    return BLOCKED_STATUS


def next_action_for(status: str, selected_count: int, total_count: int, kpi_count: int) -> str:
    if not kpi_count:
        return NEXT_BLOCKED
    if status == COMPLETED_STATUS and selected_count == total_count:
        return NEXT_COMPLETED
    return NEXT_PARTIAL


def profile_has_bom(path: Path) -> tuple[bool, str]:
    if not path_exists(path):
        return False, ""
    head = io_path(path).read_bytes()[:4]
    return head.startswith(b"\xef\xbb\xbf"), head.hex()


def profile_encoding_rows(execution_results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in execution_results:
        copy_payload = result.get("tester_profile_ini_copy") if isinstance(result, Mapping) else None
        destination = Path(str(copy_payload.get("destination"))) if isinstance(copy_payload, Mapping) else None
        has_bom, head_hex = profile_has_bom(destination) if destination else (False, "")
        rows.append(
            {
                "attempt_name": result.get("attempt_name"),
                "tester_profile_path": destination.as_posix() if destination else "",
                "exists": path_exists(destination) if destination else False,
                "has_bom": has_bom,
                "head_hex": head_hex,
                "encoding_policy": copy_payload.get("encoding_policy") if isinstance(copy_payload, Mapping) else "",
                "status": "checked" if destination else "missing",
            }
        )
    return rows


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
                "split": attempt.get("split"),
                "report_name": mt5.report_name_from_attempt(attempt, run_id=RUN_ID),
                "status": "missing",
            },
        )
        if record.get("status") == "completed":
            repaired.append(record)
            continue
        report_name = str(record.get("report_name") or mt5.report_name_from_attempt(attempt, run_id=RUN_ID))
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
        record["metrics"] = extract_mt5_strategy_report_metrics(html_destination)
        record["status"] = record["metrics"]["status"]
        record["truncated_report_salvage"] = "completed_from_dot_h"
        repaired.append(record)
    return repaired


def annotate_kpi_rows(rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    prefixes = [(str(attempt.get("record_view_prefix")), attempt) for attempt in attempts]
    annotated: list[dict[str, Any]] = []
    for row in rows:
        next_row = dict(row)
        record_view = str(row.get("record_view", ""))
        for prefix, attempt in prefixes:
            if prefix and record_view.startswith(prefix):
                next_row["queue_id"] = attempt.get("queue_id")
                next_row["candidate_id"] = attempt.get("candidate_id")
                next_row["candidate_alias"] = attempt.get("candidate_alias")
                next_row["candidate_role"] = attempt.get("candidate_role")
                next_row["variant_id"] = attempt.get("variant_id")
                next_row["profile_label"] = attempt.get("profile_label")
                next_row["tier_pair_boundary"] = attempt.get("tier_pair_boundary")
                break
        annotated.append(next_row)
    return annotated


def annotate_forensic_rows(rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_name = {str(attempt.get("attempt_name")): attempt for attempt in attempts}
    output: list[dict[str, Any]] = []
    for row in rows:
        next_row = dict(row)
        attempt = by_name.get(str(row.get("attempt_name")))
        if attempt:
            next_row["variant_id"] = attempt.get("variant_id")
            next_row["queue_id"] = attempt.get("queue_id")
            next_row["profile_label"] = attempt.get("profile_label")
            next_row["source_set_path"] = attempt.get("source_set_path")
            next_row["source_ini_path"] = attempt.get("source_ini_path")
        output.append(next_row)
    return output


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
                "variant_id": attempt.get("variant_id"),
                "profile_label": attempt.get("profile_label"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "set_path": attempt.get("set", {}).get("path"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "execution_status": result.get("status", "not_executed"),
                "runtime_status": result.get("runtime_outputs", {}).get("status") if isinstance(result, Mapping) else "",
                "report_status": result.get("strategy_tester_report", {}).get("status") if isinstance(result, Mapping) else "",
            }
        )
    return rows


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
            "effect": "tester profile(테스터 프로필) BOM(바이트 순서 표시) 차단 재발 여부를 확인한다.",
        },
        {
            "field": "runtime_outputs",
            "status": "completed" if kpi_count else "blocked",
            "value": str(kpi_count),
            "effect": "CSV handoff(CSV 인계)와 strategy report(전략 보고서)가 KPI(핵심 성과 지표)로 이어졌는지 확인한다.",
        },
        {
            "field": "tier_boundary",
            "status": "blocked_for_fallback",
            "value": TIER_PAIR_BOUNDARY,
            "effect": "Tier B(티어 B)와 actual routed total(실제 라우팅 전체)을 합성하지 않는다.",
        },
        {
            "field": "attempt_count",
            "status": "checked",
            "value": str(len(attempts)),
            "effect": "directional/impulse follow-up(방향/임펄스 후속) 실행 범위를 고정한다.",
        },
    ]


def result_judgment_rows(status: str, next_action: str) -> list[dict[str, Any]]:
    return [
        {"field": "run_status", "value": status, "judgment": "mt5_execution_completed_or_partial" if status != BLOCKED_STATUS else "blocked"},
        {"field": "selected_candidate", "value": "none", "judgment": "not_selected"},
        {"field": "selected_research_baseline", "value": "none", "judgment": "not_selected"},
        {"field": "onnx_readiness", "value": "not_claimed", "judgment": "not_ready"},
        {"field": "goal_achieve", "value": "not_claimed", "judgment": "not_claimed"},
        {"field": "next_action", "value": next_action, "judgment": "review_or_repair_next"},
    ]


def report_markdown(result: Mapping[str, Any], status: str, next_action: str) -> str:
    rows = list(result.get("kpi_summary_rows", []))
    blocked_rows = [
        row
        for row in result.get("execution_results", [])
        if row.get("status") != "completed"
        or row.get("runtime_outputs", {}).get("status") != "completed"
        or row.get("strategy_tester_report", {}).get("status") != "completed"
    ]
    lines = [
        "# Stage267 Run267BT Pool-Wide Directional/Impulse Follow-Up MT5 Execution(267단계 267BT 후보군 전체 방향/임펄스 후속 MT5 실행)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- status(상태): `{status}`",
        f"- attempts_executed(실행 시도): `{len(result.get('attempts_executed', []))}`",
        f"- kpi_records(KPI 기록): `{len(result.get('mt5_kpi_records', []))}`",
        f"- blocked_or_gap_attempts(차단 또는 공백 시도): `{len(blocked_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267BS(267BS 실행)의 방향 비대칭(directional asymmetry, 방향 비대칭)과 공격형 임펄스 대체(aggressive impulse replacement, 공격형 임펄스 대체) 10개 attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5) Strategy Tester(전략 테스터)로 실행했다.",
        "Effect(효과): 다섯 baseline candidates(기준 후보)가 새 feature engineering(피처 엔지니어링) 압박을 받을 때 실제 tester output(테스터 출력), runtime output(런타임 출력), KPI(핵심 성과 지표)까지 이어지는지 확인한다.",
        "",
        "## KPI Snapshot(KPI 요약)",
        "",
        "| candidate(후보) | profile(프로필) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | max_DD%(최대 손실폭 %) |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| `{candidate}` | `{profile}` | {net} | {pf} | {trades} | {dd} |".format(
                candidate=row.get("candidate_alias", ""),
                profile=row.get("profile_label", ""),
                net=row.get("net_profit", ""),
                pf=row.get("profit_factor", ""),
                trades=row.get("trade_count", ""),
                dd=row.get("max_drawdown_percent", ""),
            )
        )
    if not rows:
        lines.append("| `none` |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Blocked / Gap Attempts(차단/공백 시도)",
            "",
            "| attempt(시도) | candidate(후보) | profile(프로필) | tester(테스터) | runtime(런타임) | report(보고서) | note(메모) |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in blocked_rows:
        report_metrics = row.get("strategy_tester_report", {}).get("metrics", {})
        runtime_outputs = row.get("runtime_outputs", {})
        note = "trade_count={trades}; runtime_summary_exists={summary}; runtime_telemetry_exists={telemetry}".format(
            trades=report_metrics.get("trade_count", ""),
            summary=runtime_outputs.get("summary_exists", ""),
            telemetry=runtime_outputs.get("telemetry_exists", ""),
        )
        lines.append(
            "| `{attempt}` | `{candidate}` | `{profile}` | `{tester}` | `{runtime}` | `{report}` | {note} |".format(
                attempt=row.get("attempt_name", ""),
                candidate=row.get("candidate_alias", ""),
                profile=row.get("profile_label", ""),
                tester=row.get("status", ""),
                runtime=runtime_outputs.get("status", ""),
                report=row.get("strategy_tester_report", {}).get("status", ""),
                note=note,
            )
        )
    if not blocked_rows:
        lines.append("| `none` |  |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 실행은 R&D racing(연구개발 경주) 실행이며 candidate selection(후보 선택)이 아니다.",
            "- balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질) 검토 전에는 좋은 후보라고 말하지 않는다.",
            "- ONNX parity(ONNX 동등성)나 ONNX conversion(ONNX 변환)은 시작하지 않는다.",
            "- Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 true fallback manifest(진짜 대체 목록)가 생기기 전까지 blocked(차단)이다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- execution_result(실행 결과): `{rel(EXECUTION_RESULT_PATH)}`",
            f"- kpi_summary(KPI 요약): `{rel(KPI_SUMMARY_PATH)}`",
            f"- forensics(포렌식): `{rel(FORENSICS_PATH)}`",
            f"- runtime_parity_receipt(런타임 동등성 영수증): `{rel(RUNTIME_PARITY_RECEIPT_PATH)}`",
            f"- next_action(다음 행동): `{next_action}`",
        ]
    )
    return "\n".join(lines) + "\n"


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
    write_csv(EXECUTED_ATTEMPTS_PATH, executed_attempt_rows(result.get("attempts_executed", []), result.get("execution_results", [])))
    write_csv(PROFILE_ENCODING_RECEIPT_PATH, profile_rows)
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, runtime_parity_rows(profile_rows, len(result.get("mt5_kpi_records", [])), result.get("attempts_executed", [])))
    write_csv(RESULT_JUDGMENT_PATH, result_judgment_rows(status, next_action))
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": status,
            "created_at_utc": result["created_at_utc"],
            "attempt_count": len(result.get("attempts_executed", [])),
            "attempts_total_available": result.get("attempts_total_available"),
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
                "source_route_gap_audit": rel(SOURCE_ROUTE_GAP_AUDIT_PATH),
                "source_report": rel(SOURCE_REPORT_PATH),
            },
            "outputs": {
                "execution_result": rel(EXECUTION_RESULT_PATH),
                "kpi_summary": rel(KPI_SUMMARY_PATH),
                "backtest_forensics": rel(FORENSICS_PATH),
                "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
                "report": rel(REPORT_PATH),
            },
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_md(REPORT_PATH, report_markdown(result, status, next_action))


def upsert_artifacts(created_at: str) -> None:
    entries = (
        ("stage267_run267BT_producer", "producer_script", PRODUCER_PATH, "Executes run267BT pool-wide directional/impulse follow-up MT5 batch."),
        ("stage267_run267BT_source_manifest", "source_manifest", SOURCE_RUN_MANIFEST_PATH, "Source run267BS manifest."),
        ("stage267_run267BT_compile_log", "compile_log", COMPILE_LOG_PATH, "MetaEditor compile log."),
        ("stage267_run267BT_execution_result", "execution_result", EXECUTION_RESULT_PATH, "MT5 execution result payload."),
        ("stage267_run267BT_kpi_records", "kpi_records", KPI_RECORDS_PATH, "MT5 KPI records."),
        ("stage267_run267BT_kpi_summary", "kpi_summary", KPI_SUMMARY_PATH, "MT5 KPI summary."),
        ("stage267_run267BT_forensics", "backtest_forensics", FORENSICS_PATH, "Backtest forensics."),
        ("stage267_run267BT_attempts_executed", "attempts_executed", EXECUTED_ATTEMPTS_PATH, "Executed attempts."),
        ("stage267_run267BT_profile_encoding", "profile_encoding_receipt", PROFILE_ENCODING_RECEIPT_PATH, "Profile encoding receipt."),
        ("stage267_run267BT_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267BT_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267BT_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267BT_lineage", "lineage", LINEAGE_PATH, "Lineage map."),
        ("stage267_run267BT_report", "review_report", REPORT_PATH, "User-facing report."),
    )
    rows = [
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
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, rows, key="artifact_id")


def upsert_ledgers(status: str, next_action: str, kpi_count: int, attempt_count: int, total_count: int) -> None:
    stage_row = {
        "row_id": "stage267_run267BT_pool_wide_directional_impulse_followup_mt5_execution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "pool_wide_directional_impulse_followup_mt5_execution",
        "tier_scope": "Tier A first; Tier B and actual routed total blocked until true fallback manifest exists",
        "scoreboard": "mt5_runtime_pool_wide_directional_impulse_followup",
        "status": status,
        "judgment": "mt5_runtime_evidence_no_candidate_selection" if kpi_count else "blocked_no_kpi",
        "evidence_boundary": "mt5_strategy_tester_reports_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"kpi_records={kpi_count};attempts={attempt_count}/{total_count};next_action={next_action}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "pool_wide_directional_impulse_followup_mt5_execution",
        "status": status,
        "judgment": "mt5_runtime_evidence_no_candidate_selection" if kpi_count else "blocked_no_kpi",
        "path": rel(REPORT_PATH),
        "notes": f"kpi_records={kpi_count};selected_candidate=none;onnx_readiness=not_claimed.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__pool_wide_directional_impulse_followup_mt5_execution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pool_wide_directional_impulse_followup_mt5_execution",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "pool_wide_directional_impulse_followup_mt5_execution",
        "tier_scope": "Tier A first; true fallback blocked",
        "kpi_scope": "mt5_runtime_pool_wide_directional_impulse_followup",
        "scoreboard_lane": "directional_impulse_followup_execution",
        "status": status,
        "judgment": "mt5_runtime_evidence_no_candidate_selection" if kpi_count else "blocked_no_kpi",
        "path": rel(REPORT_PATH),
        "primary_kpi": f"kpi_records={kpi_count};attempts={attempt_count}/{total_count}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "completed" if kpi_count else "blocked",
        "notes": f"Next action: {next_action}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")


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


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + focus_block, 1)


def update_stage267_workspace_block(text: str, *, status: str, next_action: str) -> str:
    report_entry = f"  run267BT_pool_wide_directional_impulse_followup_mt5_execution_report_path: {rel(REPORT_PATH)}"
    source_entry = f"  run267BS_pool_wide_directional_impulse_followup_materialization_report_path: {rel(SOURCE_REPORT_PATH)}"
    lines = text.splitlines()
    out: list[str] = []
    in_stage267 = False
    source_seen = source_entry in text
    report_seen = report_entry in text
    for line in lines:
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            out.append(line)
            continue
        if in_stage267 and line and not line.startswith(" "):
            if not source_seen:
                out.append(source_entry)
                source_seen = True
            if not report_seen:
                out.append(report_entry)
                report_seen = True
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
                if not source_seen:
                    out.append(source_entry)
                    source_seen = True
                if not report_seen:
                    out.append(report_entry)
                    report_seen = True
                out.append(f"  next_action: {next_action}")
                continue
        out.append(line)
    if in_stage267:
        if not source_seen:
            out.append(source_entry)
        if not report_seen:
            out.append(report_entry)
    return "\n".join(out) + "\n"


def update_docs(status: str, next_action: str, kpi_count: int, attempt_count: int, total_count: int) -> None:
    report_line = f"- run267BT_pool_wide_directional_impulse_followup_mt5_execution(267BT 후보군 전체 방향/임펄스 후속 MT5 실행): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            "Run267BT(267BT 실행)는 run267BS(267BS 실행)의 후보군 전체 방향/임펄스 후속 attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.",
            f"Effect(효과): attempt(시도) `{attempt_count}/{total_count}`개 중 KPI records(KPI 기록) `{kpi_count}`개를 만들었고, 다음에는 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 본다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH):
        text = read_text(path)
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_directional_impulse_followup_mt5_execution`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
        text = append_after_contains(text, "stage267_run267BS_pool_wide_directional_impulse_followup_materialization.md", report_line)
        text = append_block_once(text, "Run267BT(267BT 실행)는", block)
        write_md(path, text)

    review = read_text(REVIEW_INDEX_PATH)
    review = append_after_contains(review, "stage267_run267BS_pool_wide_directional_impulse_followup_materialization.md", report_line)
    review = append_block_once(review, "Run267BT(267BT 실행)는", block)
    write_md(REVIEW_INDEX_PATH, review)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BT(267BT 실행) pool-wide directional/impulse follow-up MT5 execution(후보군 전체 방향/임펄스 후속 MT5 실행) `{status}`. "
        f"Effect(효과): run267BS(267BS 실행)의 10개 attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5) tester output(테스터 출력)과 KPI(핵심 성과 지표)로 연결했고, selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(workspace, status=status, next_action=next_action)
    write_md(WORKSPACE_STATE_PATH, workspace)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    attempts, total_count = load_attempts(args.attempt_name or [], args.limit)
    if not attempts:
        raise RuntimeError("no run267BT attempts selected")

    for attempt in attempts:
        clear_runtime_outputs(args.common_files_root, attempt)
        mt5.remove_existing_mt5_report_artifacts(args.terminal_data_root, attempt, run_id=RUN_ID)

    compile_payload = mt5.compile_mql5_ea(args.metaeditor_path, mt5.EA_SOURCE_PATH, COMPILE_LOG_PATH)
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            tester_result = mt5.run_mt5_tester(
                args.terminal_path,
                Path(str(attempt["ini"]["path"])),
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=args.tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=args.tester_profile_root / f"opv2_s267bt_{attempt['attempt_name']}.ini",
                timeout_seconds=args.timeout_seconds,
            )
            tester_result.update(
                {
                    "attempt_name": attempt.get("attempt_name"),
                    "queue_id": attempt.get("queue_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "variant_id": attempt.get("variant_id"),
                    "profile_label": attempt.get("profile_label"),
                    "tier": attempt.get("tier"),
                    "split": attempt.get("split"),
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "tier_pair_boundary": attempt.get("tier_pair_boundary"),
                    "materialization_boundary": attempt.get("materialization_boundary"),
                    "ini_path": attempt["ini"]["path"],
                }
            )
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
    report_records = supplement_truncated_html_reports(
        report_records,
        attempts,
        terminal_data_root=args.terminal_data_root,
        run_output_root=RUN_ROOT,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_rows = annotate_kpi_rows(historical_executor.kpi_summary_rows(kpi_records), attempts)
    forensics = annotate_forensic_rows(historical_executor.forensic_rows(attempts, execution_results, report_records), attempts)
    base_status = historical_executor.execution_status(execution_results, kpi_records)
    status = status_token(base_status, len(attempts), total_count, len(kpi_records))
    next_action = next_action_for(status, len(attempts), total_count, len(kpi_records))
    profile_rows = profile_encoding_rows(execution_results)
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
        "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
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
    upsert_artifacts(created_at)
    update_docs(status, next_action, len(kpi_records), len(attempts), total_count)
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute run267BT pool-wide directional/impulse follow-up attempts in MT5.")
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
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
