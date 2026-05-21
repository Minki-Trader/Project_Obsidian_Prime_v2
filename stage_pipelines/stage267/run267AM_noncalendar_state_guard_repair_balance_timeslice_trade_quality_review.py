from __future__ import annotations

import copy
import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
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
from stage_pipelines.stage267 import (
    run267AI_noncalendar_state_guard_followup_balance_timeslice_trade_quality_review as review_helper,
)
from stage_pipelines.stage267 import run267AL_noncalendar_state_guard_repair_mt5_executor as source_executor


STAGE_ID = source_executor.STAGE_ID
RUN_NUMBER = "run267AM"
RUN_ID = "run267AM_stage267_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review_v1"
PARENT_RUN_ID = source_executor.RUN_ID
STATUS = "run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review_completed"
PARTIAL_STATUS = "run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review_partial_parser_errors"
JUDGMENT = "diagnostic_repair_curve_timeslice_trade_quality_review_completed_no_candidate_selection"
PARTIAL_JUDGMENT = "diagnostic_repair_review_partial_parser_errors_no_candidate_selection"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY
NEXT_ACTION = "run267AN_design_noncalendar_state_guard_repair_followup_or_prune"
NEXT_ACTION_PARTIAL = "run267AM_repair_trade_report_parser_errors"

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "noncalendar_state_guard_repair_balance_timeslice_trade_quality_review"

SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
SOURCE_KPI_SUMMARY_PATH = source_executor.KPI_SUMMARY_PATH
SOURCE_FORENSICS_PATH = source_executor.FORENSICS_PATH
SOURCE_EXECUTED_ATTEMPTS_PATH = source_executor.EXECUTED_ATTEMPTS_PATH
SOURCE_REPORT_PATH = source_executor.REPORT_PATH
BASELINE_REVIEW_PATH = review_helper.CANDIDATE_TEST_REVIEW_PATH
BASELINE_TIME_SLICE_PATH = review_helper.TIME_SLICE_KPI_PATH

TRADE_RECORDS_PATH = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = RUN_ROOT / "curve_diagnostics.csv"
CANDIDATE_TEST_REVIEW_PATH = RUN_ROOT / "candidate_test_review.csv"
CANDIDATE_SUMMARY_PATH = RUN_ROOT / "candidate_balance_timeslice_summary.csv"
REPAIR_PROFILE_SUMMARY_PATH = RUN_ROOT / "repair_profile_balance_timeslice_summary.csv"
NEGATIVE_SLICE_PATH = RUN_ROOT / "negative_slice_summary.csv"
PARSER_CHECKS_PATH = RUN_ROOT / "parser_checks.csv"
PARSER_ERRORS_PATH = RUN_ROOT / "parser_errors.csv"
TIER_DUPLICATE_REVIEW_PATH = RUN_ROOT / "tier_duplicate_review.csv"
BASELINE_COMPARISON_PATH = RUN_ROOT / "run267AI_baseline_comparison.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review.py")

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
METRIC_COLUMNS = review_helper.METRIC_COLUMNS


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isinf(value):
            return "inf"
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def prepare_execution_result(execution_result: Mapping[str, Any]) -> dict[str, Any]:
    prepared = copy.deepcopy(execution_result)
    for attempt in prepared.get("attempts_executed", []):
        attempt["followup_profile"] = attempt.get("repair_profile") or attempt.get("followup_profile") or ""
    return prepared


def helper_review_inputs(execution_result: Mapping[str, Any]) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    review_helper.RUN_ID = RUN_ID
    review_helper.PARENT_RUN_ID = PARENT_RUN_ID
    prepared = prepare_execution_result(execution_result)
    trade_rows, parser_errors, parser_checks = review_helper.build_trade_records(prepared)
    for row in trade_rows:
        row["repair_profile"] = row.get("followup_profile")
        row["materialization_boundary"] = "noncalendar_state_guard_repair_score_table_terms_only_not_retrained"
    time_rows = review_helper.build_time_slice_rows(trade_rows)
    for row in time_rows:
        row["repair_profile"] = row.get("followup_profile")
        row["materialization_boundary"] = "noncalendar_state_guard_repair_score_table_terms_only_not_retrained"
    curve_rows = review_helper.build_curve_rows(trade_rows, time_rows, prepared)
    for row in curve_rows:
        row["repair_profile"] = row.get("followup_profile")
        row["materialization_boundary"] = "noncalendar_state_guard_repair_score_table_terms_only_not_retrained"
    candidate_tests = review_helper.build_candidate_test_review(curve_rows, time_rows)
    for row in candidate_tests:
        row["repair_profile"] = row.get("followup_profile")
    candidate_summary = review_helper.build_candidate_summary(candidate_tests)
    profile_summary = review_helper.build_profile_summary(candidate_tests)
    for row in profile_summary:
        row["repair_profile"] = row.get("followup_profile")
    negative = review_helper.negative_slices(time_rows)
    for row in negative:
        row["repair_profile"] = row.get("followup_profile")
    tier_duplicate_review = review_helper.build_tier_duplicate_review(curve_rows)
    return (
        trade_rows,
        time_rows,
        curve_rows,
        candidate_tests,
        candidate_summary,
        profile_summary,
        negative,
        tier_duplicate_review,
        parser_errors,
        parser_checks,
    )


def slice_net(rows: Sequence[Mapping[str, Any]], alias: str, test_id: str, axis: str, bucket: str) -> float:
    matches = [
        row
        for row in rows
        if row.get("tier_scope") == "Tier A"
        and row.get("candidate_alias") == alias
        and row.get("source_test_id") == test_id
        and row.get("axis") == axis
        and row.get("bucket") == bucket
    ]
    return as_float(matches[0].get("net_profit")) if matches else 0.0


def baseline_row_map(rows: Sequence[Mapping[str, Any]]) -> dict[tuple[str, str], Mapping[str, Any]]:
    return {
        (str(row.get("candidate_alias")), str(row.get("source_test_id"))): row
        for row in rows
        if row.get("candidate_alias") and row.get("source_test_id")
    }


def comparison_read(row: Mapping[str, Any]) -> str:
    meets_gate = (
        as_int(row.get("repair_trade_count")) >= 280
        and as_float(row.get("repair_net_profit")) >= 900.0
        and as_float(row.get("repair_profit_factor")) >= 1.35
        and as_float(row.get("repair_equity_drawdown_percent")) <= 18.0
        and as_float(row.get("repair_monday_net")) > -180.0
        and as_float(row.get("repair_december_net")) > -120.0
    )
    if meets_gate and as_float(row.get("monday_delta")) > 0.0 and as_float(row.get("december_delta")) > 0.0:
        return "repair_watch_passes_named_weak_slice_gate_no_selection"
    if as_float(row.get("repair_net_profit")) >= 900.0 and as_int(row.get("repair_trade_count")) >= 280:
        return "headline_survives_but_named_weak_slice_gate_incomplete"
    return "repair_does_not_clear_watch_gate"


def build_baseline_comparison(
    candidate_tests: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    baseline_tests = read_csv(BASELINE_REVIEW_PATH)
    baseline_time = read_csv(BASELINE_TIME_SLICE_PATH)
    baseline = baseline_row_map(baseline_tests)
    rows: list[dict[str, Any]] = []
    for repair in candidate_tests:
        repair_tier_scope = str(repair.get("tier_scope") or "")
        repair_record_view = str(repair.get("record_view") or "")
        if repair_tier_scope and repair_tier_scope != "Tier A":
            continue
        if not repair_tier_scope and not repair_record_view.startswith("mt5_ta_"):
            continue
        alias = str(repair.get("candidate_alias"))
        test_id = str(repair.get("source_test_id"))
        base = baseline.get((alias, test_id), {})
        item = {
            "candidate_alias": alias,
            "candidate_id": repair.get("candidate_id"),
            "candidate_role": repair.get("candidate_role"),
            "source_test_id": test_id,
            "repair_profile": repair.get("repair_profile") or repair.get("followup_profile"),
            "repair_tier_scope": repair_tier_scope or "Tier A inferred from mt5_ta record_view",
            "baseline_record_view": base.get("record_view", ""),
            "repair_record_view": repair.get("record_view"),
            "baseline_net_profit": as_float(base.get("net_profit")),
            "repair_net_profit": as_float(repair.get("net_profit")),
            "net_profit_delta": as_float(repair.get("net_profit")) - as_float(base.get("net_profit")),
            "baseline_profit_factor": as_float(base.get("profit_factor")),
            "repair_profit_factor": as_float(repair.get("profit_factor")),
            "profit_factor_delta": as_float(repair.get("profit_factor")) - as_float(base.get("profit_factor")),
            "baseline_trade_count": as_int(base.get("trade_count")),
            "repair_trade_count": as_int(repair.get("trade_count")),
            "trade_count_delta": as_int(repair.get("trade_count")) - as_int(base.get("trade_count")),
            "baseline_equity_drawdown_percent": as_float(base.get("report_equity_drawdown_percent")),
            "repair_equity_drawdown_percent": as_float(repair.get("report_equity_drawdown_percent")),
            "equity_drawdown_percent_delta": as_float(repair.get("report_equity_drawdown_percent"))
            - as_float(base.get("report_equity_drawdown_percent")),
            "baseline_worst_month": base.get("worst_month", ""),
            "baseline_worst_month_net": as_float(base.get("worst_month_net")),
            "repair_worst_month": repair.get("worst_month"),
            "repair_worst_month_net": as_float(repair.get("worst_month_net")),
            "baseline_monday_net": slice_net(baseline_time, alias, test_id, "weekday", "Monday"),
            "repair_monday_net": slice_net(time_rows, alias, test_id, "weekday", "Monday"),
            "baseline_december_net": slice_net(baseline_time, alias, test_id, "month", "2024-12"),
            "repair_december_net": slice_net(time_rows, alias, test_id, "month", "2024-12"),
            "baseline_curve_read": base.get("curve_read", ""),
            "repair_curve_read": repair.get("curve_read"),
        }
        item["monday_delta"] = as_float(item["repair_monday_net"]) - as_float(item["baseline_monday_net"])
        item["december_delta"] = as_float(item["repair_december_net"]) - as_float(item["baseline_december_net"])
        item["comparison_read"] = comparison_read(item)
        rows.append(item)
    return sorted(rows, key=lambda row: (-as_float(row.get("repair_net_profit")), as_float(row.get("repair_equity_drawdown_percent"))))


def result_status(parser_errors: Sequence[Mapping[str, Any]], parser_checks: Sequence[Mapping[str, Any]]) -> str:
    mismatches = [row for row in parser_checks if row.get("parser_status") != "matched"]
    if parser_errors or mismatches:
        return PARTIAL_STATUS
    return STATUS


def result_judgment(status: str) -> str:
    return JUDGMENT if status == STATUS else PARTIAL_JUDGMENT


def result_next_action(status: str) -> str:
    return NEXT_ACTION if status == STATUS else NEXT_ACTION_PARTIAL


def forensics_summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return review_helper.forensics_summary(rows)


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


def remove_lines_starting(text: str, prefix: str) -> str:
    return "\n".join(line for line in text.splitlines() if not line.startswith(prefix)) + "\n"


def update_workspace_state_text(text: str, result: Mapping[str, Any]) -> str:
    status = str(result["status"])
    next_action = str(result["next_action"])
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_focus = "run267AM(" in text
    inserted_path = "run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review_report_path" in text
    focus_block = [
        "- >-",
        f"  Stage267(267단계) run267AM(267AM 실행) noncalendar state guard repair balance/time-slice/trade-quality review(비달력 상태 방어 수리 잔액/시간구간/거래품질 검토) `{status}`. Effect(효과): run267AL(267AL 실행)의 4개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 거래 단위로 다시 읽어 weak slice(약한 구간)와 repair gate(수리 게이트)를 검토했고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    ]
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line == "current_focus:" and not inserted_focus:
            output.append(line)
            output.extend(focus_block)
            inserted_focus = True
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
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
                output.append(f"  next_action: {next_action}")
                continue
            if "run267AL_noncalendar_state_guard_repair_mt5_execution_report_path" in stripped and not inserted_path:
                output.append(line)
                output.append(
                    f"  run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}"
                )
                inserted_path = True
                continue
        output.append(line)
    return "\n".join(output) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    report_line = (
        "- run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review"
        f"(267AM 비달력 상태 방어 수리 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    )
    latest_line = (
        "- latest_repair_review(최신 수리 검토): run267AM(267AM 실행) "
        f"trade records(거래 기록) `{result['trade_record_count']}`, "
        f"candidate-test rows(후보-시험 행) `{len(result['candidate_test_review'])}`, "
        f"repair comparisons(수리 비교 행) `{len(result['baseline_comparison'])}`, "
        f"negative Tier A slices(음수 Tier A 구간) `{len(result['negative_slices'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    closing_block = "\n".join(
        [
            "Run267AM(267AM 실행)은 run267AL(267AL 실행)의 repair MT5 reports(수리 MT5 보고서)를 거래 단위로 다시 읽었다.",
            "Effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 Monday(월요일), 2024-12(2024년 12월), chron segment(시간 순서 구간), session(세션)을 비교해 다음 설계/가지치기 조건을 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = remove_lines_starting(text, "- latest_repair_review(")
            text = replace_line_prefix(text, "- status(", f"- status(상태): `{status}`")
            text = replace_line_prefix(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
            text = replace_line_prefix(text, "- next_run(", f"- next_run(다음 실행): `{next_action}`")
            text = replace_line_prefix(
                text,
                "- action(",
                "- action(행동): run267AM(267AM 실행)은 run267AL(267AL 실행)의 4개 repair MT5 reports(수리 MT5 보고서)를 거래 단위로 검토했다.",
            )
            text = replace_line_prefix(
                text,
                "- effect(",
                "- effect(효과): 다음 run267AN(267AN 실행)에서 repair branch(수리 분기)를 유지할지, 더 압박할지, 짧게 종료할지 결정할 수 있다.",
            )
            text = replace_line_prefix(
                text,
                "- adapter_under_review(",
                "- adapter_under_review(검토 중 어댑터): `noncalendar_state_guard_repair_balance_timeslice_trade_quality_review`",
            )
            text = append_after_contains(text, "run267AL_noncalendar_state_guard_repair_mt5_execution", report_line)
            text = append_after_contains(text, "## Current Next Action", latest_line)
        else:
            text = replace_line_prefix(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
            if path == SELECTION_STATUS_PATH:
                text = replace_line_prefix(text, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
            if path == REVIEW_INDEX_PATH:
                text = replace_line_prefix(text, "- status(", f"- status(상태): `{status}`")
            text = append_after_contains(text, "run267AL_noncalendar_state_guard_repair_mt5_execution", report_line)
        text = append_block_once(text, "Run267AM(267AM 실행)은 run267AL", closing_block)
        write_md(path, text)
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    write_md(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace, result))


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    judgment = str(result["judgment"])
    next_action = str(result["next_action"])
    trade_count = int(result["trade_record_count"])
    candidate_count = len(result["candidate_test_review"])
    negative_count = len(result["negative_slices"])
    comparison_count = len(result["baseline_comparison"])
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "noncalendar_state_guard_repair_balance_timeslice_trade_quality_review",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate boundary",
                "scoreboard": "curve_time_slice_trade_quality_repair_comparison",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "diagnostic_repair_curve_time_slice_trade_quality_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"trade_records={trade_count};candidate_test_rows={candidate_count};comparison_rows={comparison_count};next_action={next_action}.",
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_candidate_racing_noncalendar_state_guard_repair_review",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT_PATH),
                "notes": (
                    "Run267AM repair MT5 curve/time-slice/trade-quality review; "
                    f"trade_records={trade_count}; comparison_rows={comparison_count}; "
                    f"selected_candidate=none; onnx_readiness=not_claimed; next_action={next_action}."
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
                "ledger_row_id": f"{RUN_ID}__noncalendar_state_guard_repair_balance_timeslice_trade_quality_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "noncalendar_state_guard_repair_balance_timeslice_trade_quality_review",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "noncalendar_state_guard_repair_balance_timeslice_trade_quality_review",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate boundary",
                "kpi_scope": "curve_time_slice_trade_quality_repair_comparison",
                "scoreboard_lane": "trade_shape_curve_time_slice_review",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT_PATH),
                "primary_kpi": (
                    f"trade_records={trade_count};candidate_test_rows={candidate_count};"
                    f"comparison_rows={comparison_count};negative_slices={negative_count}"
                ),
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "completed_for_run267AL_mt5_report_review",
                "notes": f"Next action: {next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    entries = (
        ("stage267_run267AM_review_script", "producer_script", PRODUCER_PATH, "Builds run267AM repair curve/time-slice/trade-quality review."),
        ("stage267_run267AM_source_execution_result", "source_execution_result", SOURCE_EXECUTION_RESULT_PATH, "Source run267AL execution result."),
        ("stage267_run267AM_source_kpi_summary", "source_kpi_summary", SOURCE_KPI_SUMMARY_PATH, "Source run267AL KPI summary."),
        ("stage267_run267AM_source_forensics", "source_forensics", SOURCE_FORENSICS_PATH, "Source run267AL backtest forensics."),
        ("stage267_run267AM_source_attempts", "source_attempt_manifest", SOURCE_EXECUTED_ATTEMPTS_PATH, "Source run267AL executed attempts."),
        ("stage267_run267AM_source_baseline_review", "source_review", BASELINE_REVIEW_PATH, "Source run267AI candidate-test review baseline."),
        ("stage267_run267AM_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267AM paired trade records from run267AL reports."),
        ("stage267_run267AM_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267AM month/weekday/hour/session/direction/chron-segment KPI."),
        ("stage267_run267AM_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267AM closed-balance curve diagnostics."),
        ("stage267_run267AM_candidate_test_review", "candidate_test_review", CANDIDATE_TEST_REVIEW_PATH, "Run267AM candidate-test curve and weak-slice review."),
        ("stage267_run267AM_candidate_summary", "candidate_summary", CANDIDATE_SUMMARY_PATH, "Run267AM candidate balance/time-slice summary."),
        ("stage267_run267AM_repair_profile_summary", "repair_profile_summary", REPAIR_PROFILE_SUMMARY_PATH, "Run267AM repair profile summary."),
        ("stage267_run267AM_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267AM worst negative Tier A slices."),
        ("stage267_run267AM_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Run267AM parser reconciliation checks."),
        ("stage267_run267AM_parser_errors", "parser_errors", PARSER_ERRORS_PATH, "Run267AM parser errors."),
        ("stage267_run267AM_tier_duplicate_review", "audit_matrix", TIER_DUPLICATE_REVIEW_PATH, "Run267AM Tier A versus Tier A+B duplicate boundary."),
        ("stage267_run267AM_baseline_comparison", "comparison_matrix", BASELINE_COMPARISON_PATH, "Run267AM comparison against run267AI baseline rows."),
        ("stage267_run267AM_review_result", "review_result", REVIEW_RESULT_PATH, "Run267AM review JSON payload."),
        ("stage267_run267AM_review_report", "review_report", REPORT_PATH, "User-facing run267AM repair balance/time-slice/trade-quality review."),
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


def top_rows(rows: Sequence[Mapping[str, Any]], limit: int = 12) -> list[Mapping[str, Any]]:
    return list(rows[:limit])


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_tests = result["candidate_test_review"]
    comparisons = result["baseline_comparison"]
    negative = result["negative_slices"][:12]
    forensic = result["forensics_summary"]
    lines = [
        "# Stage267 Run267AM Noncalendar State Guard Repair Balance/Time-Slice/Trade-Quality Review(267단계 267AM 비달력 상태 방어 수리 잔액/시간구간/거래품질 검토)",
        "",
        f"- action(행동): run267AL(267AL 실행)의 `{len(result['parser_checks'])}`개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록) 단위로 다시 읽었다.",
        "- effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 repair(수리)가 Monday(월요일), 2024-12(2024년 12월), session(세션), chron segment(시간 순서 구간)에서 덜 깨지는지 확인했다.",
        f"- status(상태): `{result['status']}`",
        f"- judgment(판정): `{result['judgment']}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- candidate_test_rows(후보-시험 행): `{len(candidate_tests)}`",
        f"- baseline_comparison_rows(기준 비교 행): `{len(comparisons)}`",
        f"- negative_tier_a_slices(음수 Tier A 구간): `{len(result['negative_slices'])}`",
        f"- parser_errors(파서 오류): `{len(result['parser_errors'])}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267AL(267AL 실행)의 대표 숫자는 좋아 보인다. 하지만 이번 goal(목표)은 숫자만 보는 것이 아니라 누가 덜 깨지는지 보는 것이다.",
        "Effect(효과): run267AM(267AM 실행)은 run267AI(267AI 실행)의 약점 기준과 비교해 수리 후에도 Monday(월요일)와 December(12월) 구멍이 남는지 확인한다.",
        "Tier A+B(Tier A+B 합산)는 fallback disabled(대체 비활성) 중복 경계다. 따라서 routed robustness(라우팅 견고성)이나 runtime authority(런타임 권위)는 주장하지 않는다.",
        "",
        "## Repair Comparison(수리 비교)",
        "",
        "| candidate(후보) | test(시험) | net delta(순수익 변화) | PF delta(PF 변화) | trade delta(거래 변화) | DD delta(손실폭 변화) | Monday delta(월요일 변화) | Dec delta(12월 변화) | read(판독) |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in comparisons:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('source_test_id')}` | "
            f"{as_float(row.get('net_profit_delta')):.2f} | {as_float(row.get('profit_factor_delta')):.2f} | "
            f"{as_int(row.get('trade_count_delta'))} | {as_float(row.get('equity_drawdown_percent_delta')):.2f} | "
            f"{as_float(row.get('monday_delta')):.2f} | {as_float(row.get('december_delta')):.2f} | "
            f"`{row.get('comparison_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Candidate-Test Watchlist(후보-시험 관찰 목록)",
            "",
            "| rank(순위) | candidate(후보) | test(시험) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst month(최악 월) | worst slice(최악 구간) | read(판독) |",
            "| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |",
        ]
    )
    for index, row in enumerate(top_rows(candidate_tests), start=1):
        lines.append(
            f"| {index} | `{row.get('candidate_alias')}` | `{row.get('source_test_id')}` | "
            f"{as_float(row.get('net_profit')):.2f} | {as_float(row.get('profit_factor')):.2f} | "
            f"{as_int(row.get('trade_count'))} | {as_float(row.get('report_equity_drawdown_percent')):.2f} | "
            f"`{row.get('worst_month')}` {as_float(row.get('worst_month_net')):.2f} | "
            f"`{row.get('worst_slice_axis')}`/`{row.get('worst_slice_bucket')}` {as_float(row.get('worst_slice_net')):.2f} | "
            f"`{row.get('curve_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Worst Tier A Slices(최악 Tier A 구간)",
            "",
            "| candidate(후보) | test(시험) | axis(축) | bucket(구간) | net profit(순수익) | trades(거래 수) | read(판독) |",
            "| --- | --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in negative:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('source_test_id')}` | `{row.get('axis')}` | `{row.get('bucket')}` | "
            f"{as_float(row.get('net_profit')):.2f} | {as_int(row.get('trade_count'))} | `{row.get('slice_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Performance Attribution(성과 귀인)",
            "",
            "- observed_change(관찰 변화): repair(수리) 후 대표 KPI(핵심 성과 지표)는 net profit(순수익) 1017~1018, PF(수익 팩터) 1.59~1.66, trade count(거래 수) 290으로 유지됐다.",
            "- comparison_baseline(비교 기준): run267AI(267AI 실행)의 s264_aia Tier A follow-up rows(후속 행)를 기준으로 삼았다.",
            "- likely_drivers(가능 원인): 새 학습이 아니라 score table guard terms(점수표 방어 항) 변경이므로, 성능 변화는 decision surface(결정 표면)의 일부 상태 구간 억제에서 온 것으로 본다.",
            "- segment_checks(구간 확인): month(월), weekday(요일), hour(시간), session(세션), direction(방향), chron segment(시간 순서 구간)를 확인했다.",
            "- trade_shape(거래 형태): trade count(거래 수), expectancy(기대값), win rate(승률), payoff ratio(손익비), drawdown(손실폭), underwater(회복 전 체류)를 기록했다.",
            "- alternative_explanations(대체 설명): 2024 단일 기간 stress(압박)라서 우연 적합 가능성이 남고, Tier A+B(Tier A+B 합산)는 실제 fallback(대체) 검증이 아니다.",
            "- attribution_confidence(귀인 신뢰도): `medium_diagnostic_only`.",
            f"- next_probe(다음 탐침): `{result['next_action']}`.",
            "",
            "## Forensics Boundary(포렌식 경계)",
            "",
            f"- tester_identity(테스터 정체성): terminal count(터미널 수) `{forensic['terminal_count']}`, symbol(심볼) `{';'.join(forensic['symbols'])}`, timeframe(시간 프레임) `{';'.join(forensic['timeframes'])}`, date range(날짜 범위) `{';'.join(forensic['from_dates'])}` to `{';'.join(forensic['to_dates'])}`.",
            f"- trade_evidence(거래 근거): trade records(거래 기록) `{result['trade_record_count']}`, parser checks(파서 확인) `{len(result['parser_checks'])}`.",
            f"- cost_assumptions(비용 가정): `{forensic['cost_assumption_boundary']}`.",
            f"- backtest_judgment(백테스트 판정): `{forensic['backtest_judgment']}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(SOURCE_EXECUTION_RESULT_PATH)}`, `{rel(SOURCE_KPI_SUMMARY_PATH)}`, `{rel(SOURCE_FORENSICS_PATH)}`, `{rel(SOURCE_EXECUTED_ATTEMPTS_PATH)}`, `{rel(BASELINE_REVIEW_PATH)}`.",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
            f"- consumer(소비자): `{result['next_action']}`.",
            f"- artifact_paths(산출물 경로): `{rel(TRADE_RECORDS_PATH)}`, `{rel(TIME_SLICE_KPI_PATH)}`, `{rel(CURVE_DIAGNOSTICS_PATH)}`, `{rel(BASELINE_COMPARISON_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
            "- lineage_judgment(계보 판정): `connected_with_boundary`.",
            "",
            "## Boundary(경계)",
            "",
            "- positive_claim(긍정 주장): `none`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            "- missing_required(필수 누락): broader period pressure(더 넓은 기간 압박), real fallback/routed robustness(실제 대체 라우팅 견고성), Adapter follow-up(어댑터 후속), ONNX parity(ONNX 동등성).",
            f"- next_action(다음 행동): `{result['next_action']}`.",
        ]
    )
    return "\n".join(lines)


def review() -> dict[str, Any]:
    if not path_exists(SOURCE_EXECUTION_RESULT_PATH):
        raise FileNotFoundError(SOURCE_EXECUTION_RESULT_PATH)
    created_at = utc_now()
    execution_result = read_json(SOURCE_EXECUTION_RESULT_PATH)
    forensics_rows = read_csv(SOURCE_FORENSICS_PATH)
    (
        trade_rows,
        time_rows,
        curve_rows,
        candidate_tests,
        candidate_summary,
        profile_summary,
        negative,
        tier_duplicate_review,
        parser_errors,
        parser_checks,
    ) = helper_review_inputs(execution_result)
    baseline_comparison = build_baseline_comparison(candidate_tests, time_rows)
    status = result_status(parser_errors, parser_checks)
    judgment = result_judgment(status)
    next_action = result_next_action(status)
    result = {
        "status": status,
        "judgment": judgment,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "candidate_test_review": candidate_tests,
        "candidate_summary": candidate_summary,
        "repair_profile_summary": profile_summary,
        "negative_slices": negative,
        "tier_duplicate_review": tier_duplicate_review,
        "baseline_comparison": baseline_comparison,
        "parser_errors": parser_errors,
        "parser_checks": parser_checks,
        "forensics_summary": forensics_summary(forensics_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
        "outputs": {
            "trade_records": rel(TRADE_RECORDS_PATH),
            "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
            "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
            "candidate_test_review": rel(CANDIDATE_TEST_REVIEW_PATH),
            "candidate_summary": rel(CANDIDATE_SUMMARY_PATH),
            "repair_profile_summary": rel(REPAIR_PROFILE_SUMMARY_PATH),
            "negative_slice_summary": rel(NEGATIVE_SLICE_PATH),
            "parser_checks": rel(PARSER_CHECKS_PATH),
            "parser_errors": rel(PARSER_ERRORS_PATH),
            "tier_duplicate_review": rel(TIER_DUPLICATE_REVIEW_PATH),
            "baseline_comparison": rel(BASELINE_COMPARISON_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    trade_columns = (
        "run_id",
        "source_run_id",
        "queue_id",
        "candidate_id",
        "candidate_alias",
        "candidate_role",
        "source_test_id",
        "source_queue_id",
        "followup_profile",
        "repair_profile",
        "model_materialization_type",
        "materialization_boundary",
        "record_view",
        "attempt_name",
        "tier_scope",
        "route_role",
        "split",
        "fallback_enabled",
        "trade_index",
        "direction",
        "open_time",
        "close_time",
        "holding_minutes",
        "month",
        "weekday",
        "close_hour_report",
        "session_report",
        "chron_segment",
        "volume",
        "gross_profit",
        "net_profit",
        "commission",
        "swap",
        "source_report_path",
    )
    time_columns = (
        "record_view",
        "tier_scope",
        "candidate_id",
        "candidate_alias",
        "candidate_role",
        "source_test_id",
        "followup_profile",
        "repair_profile",
        "materialization_boundary",
        "route_role",
        "axis",
        "bucket",
        *METRIC_COLUMNS,
        "slice_read",
    )
    curve_columns = (
        "record_view",
        "tier_scope",
        "candidate_id",
        "candidate_alias",
        "candidate_role",
        "source_test_id",
        "followup_profile",
        "repair_profile",
        "materialization_boundary",
        "route_role",
        *METRIC_COLUMNS,
        "report_equity_drawdown_percent",
        "report_balance_drawdown_percent",
        "report_recovery_factor",
        "tier_b_fallback_used_count",
        "tier_b_fallback_order_fill_count",
        "positive_month_ratio",
        "negative_month_count",
        "worst_month",
        "worst_month_net",
        "best_month",
        "best_month_net",
        "chron_early_net",
        "chron_mid_net",
        "chron_late_net",
        "source_chart_path",
        "curve_read",
    )
    write_csv(TRADE_RECORDS_PATH, trade_rows, trade_columns)
    write_csv(TIME_SLICE_KPI_PATH, time_rows, time_columns)
    write_csv(CURVE_DIAGNOSTICS_PATH, curve_rows, curve_columns)
    write_csv(CANDIDATE_TEST_REVIEW_PATH, candidate_tests, tuple(candidate_tests[0].keys()) if candidate_tests else ())
    write_csv(CANDIDATE_SUMMARY_PATH, candidate_summary, tuple(candidate_summary[0].keys()) if candidate_summary else ())
    write_csv(REPAIR_PROFILE_SUMMARY_PATH, profile_summary, tuple(profile_summary[0].keys()) if profile_summary else ())
    write_csv(NEGATIVE_SLICE_PATH, negative, tuple(negative[0].keys()) if negative else time_columns)
    write_csv(
        PARSER_CHECKS_PATH,
        parser_checks,
        ("attempt_name", "record_view", "tier_scope", "report_path", "expected_trade_count", "parsed_trade_count", "trade_count_delta", "parser_status"),
    )
    write_csv(PARSER_ERRORS_PATH, parser_errors, ("attempt_name", "report_path", "error"))
    write_csv(TIER_DUPLICATE_REVIEW_PATH, tier_duplicate_review, tuple(tier_duplicate_review[0].keys()) if tier_duplicate_review else ())
    write_csv(BASELINE_COMPARISON_PATH, baseline_comparison, tuple(baseline_comparison[0].keys()) if baseline_comparison else ())
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_truth_docs(result)
    return result


def main() -> int:
    result = review()
    print(
        json.dumps(
            {
                "status": result["status"],
                "trade_records": result["trade_record_count"],
                "time_slice_rows": result["time_slice_row_count"],
                "curve_rows": result["curve_row_count"],
                "candidate_test_rows": len(result["candidate_test_review"]),
                "baseline_comparison_rows": len(result["baseline_comparison"]),
                "negative_slices": len(result["negative_slices"]),
                "parser_errors": len(result["parser_errors"]),
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
