from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
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
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import (
    run267DV_runtime_gap_aware_fifth_followup_or_prune_mt5_executor as source_executor,
)
from stage_pipelines.stage267 import run267O_pool_wide_balance_timeslice_trade_quality_review as review_base


STAGE_ID = source_executor.STAGE_ID
SOURCE_RUN_ID = source_executor.RUN_ID
RUN_NUMBER = "run267DW"
RUN_ID = "run267DW_stage267_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures_v1"
STATUS = "run267DW_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures_completed"
PARTIAL_STATUS = "run267DW_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures_partial_parser_errors"
NEXT_ACTION = "run267DX_design_runtime_gap_aware_sixth_followup_or_prune_from_run267DW_review"
NEXT_ACTION_PARTIAL = "run267DW_repair_trade_report_parser_before_init_failure_review"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures"
SOURCE_ROOT = source_executor.RUN_ROOT
SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
SOURCE_REPORT_PATH = source_executor.REPORT_PATH
SOURCE_KPI_SUMMARY_PATH = source_executor.KPI_SUMMARY_PATH
SOURCE_FORENSICS_PATH = source_executor.FORENSICS_PATH

TRADE_RECORDS_PATH = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = RUN_ROOT / "curve_diagnostics.csv"
CANDIDATE_PROFILE_REVIEW_PATH = RUN_ROOT / "candidate_profile_review.csv"
CANDIDATE_INIT_FAILURE_SUMMARY_PATH = RUN_ROOT / "candidate_init_failure_summary.csv"
ATTEMPT_OUTCOME_REVIEW_PATH = RUN_ROOT / "attempt_outcome_review.csv"
NEGATIVE_SLICE_PATH = RUN_ROOT / "negative_slice_summary.csv"
PARSER_CHECKS_PATH = RUN_ROOT / "parser_checks.csv"
ATTRIBUTION_SUMMARY_PATH = RUN_ROOT / "performance_attribution_summary.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DW_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DW_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_review.py")

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

METRIC_COLUMNS = (
    "trade_count",
    "net_profit",
    "gross_profit",
    "gross_loss",
    "profit_factor",
    "expectancy",
    "win_rate",
    "avg_win",
    "avg_loss",
    "payoff_ratio",
    "closed_balance_max_drawdown",
    "closed_balance_max_drawdown_percent",
    "longest_underwater_trades",
    "underwater_trade_share",
    "max_losing_streak",
    "recovery_factor_closed",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def columns(rows: Sequence[Mapping[str, Any]], fallback: Sequence[str]) -> tuple[str, ...]:
    if rows:
        ordered: list[str] = []
        for row in rows:
            for key in row:
                if key not in ordered:
                    ordered.append(str(key))
        return tuple(ordered)
    return tuple(fallback)


def configure_review_base() -> None:
    review_base.RUN_ID = RUN_ID
    review_base.SOURCE_RUN_ID = SOURCE_RUN_ID
    review_base.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    review_base.SOURCE_ROOT = SOURCE_ROOT
    review_base.SOURCE_EXECUTION_RESULT_PATH = SOURCE_EXECUTION_RESULT_PATH
    review_base.SOURCE_KPI_SUMMARY_PATH = SOURCE_KPI_SUMMARY_PATH
    review_base.SOURCE_FORENSICS_PATH = SOURCE_FORENSICS_PATH
    review_base.SOURCE_KPI_DELTA_PATH = RUN_ROOT / "not_applicable_kpi_delta_review.csv"
    review_base.TRADE_RECORDS_PATH = TRADE_RECORDS_PATH
    review_base.TIME_SLICE_KPI_PATH = TIME_SLICE_KPI_PATH
    review_base.CURVE_DIAGNOSTICS_PATH = CURVE_DIAGNOSTICS_PATH
    review_base.NEGATIVE_SLICE_PATH = NEGATIVE_SLICE_PATH
    review_base.PARSER_CHECKS_PATH = PARSER_CHECKS_PATH
    review_base.REVIEW_RESULT_PATH = REVIEW_RESULT_PATH
    review_base.REPORT_PATH = REPORT_PATH
    review_base.PRODUCER_PATH = PRODUCER_PATH
    review_base.STATUS = STATUS
    review_base.PARTIAL_STATUS = PARTIAL_STATUS
    review_base.NEXT_ACTION = NEXT_ACTION
    review_base.NEXT_ACTION_PARTIAL = NEXT_ACTION_PARTIAL
    review_base.curve_read = curve_read


def normalize_route_role(record: Mapping[str, Any]) -> str:
    tier = str(record.get("tier_scope") or record.get("report", {}).get("tier") or "")
    if tier == "Tier A+B":
        return "duplicate_boundary_total_not_true_fallback"
    if tier == "Tier A":
        return "tier_a_only"
    return str(record.get("route_role") or "unknown_tier_boundary")


def normalize_execution_result(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    attempts: list[dict[str, Any]] = []
    for attempt in normalized.get("attempts_executed", []):
        next_attempt = dict(attempt)
        profile = str(next_attempt.get("profile_label") or next_attempt.get("variant_id") or "unknown_profile")
        next_attempt["queue_id"] = next_attempt.get("queue_id") or next_attempt.get("variant_id")
        next_attempt["test_id"] = profile
        next_attempt["test_type"] = next_attempt.get("risk_shape_mode") or profile
        next_attempt["materialization_boundary"] = (
            next_attempt.get("tier_pair_boundary")
            or next_attempt.get("materialization_boundary")
            or "Tier A and duplicate-boundary only(티어 A와 중복 경계만)"
        )
        attempts.append(next_attempt)
    normalized["attempts_executed"] = attempts

    records: list[dict[str, Any]] = []
    for record in normalized.get("mt5_kpi_records", []):
        next_record = dict(record)
        base_record_view = str(next_record.get("record_view") or "")
        report = next_record.get("report", {})
        attempt_name = str(report.get("attempt_name") or "") if isinstance(report, Mapping) else ""
        if base_record_view:
            next_record["source_record_view"] = base_record_view
            next_record["record_view"] = f"{base_record_view}__{attempt_name}" if attempt_name else base_record_view
        next_record["route_role"] = normalize_route_role(next_record)
        records.append(next_record)
    normalized["mt5_kpi_records"] = records
    return normalized


def attempt_by_name(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in payload.get("attempts_executed", [])}


def report_by_attempt(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in payload.get("strategy_tester_reports", [])}


def execution_by_attempt(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in payload.get("execution_results", [])}


def report_metrics(row: Mapping[str, Any]) -> Mapping[str, Any]:
    metrics = row.get("metrics", {})
    return metrics if isinstance(metrics, Mapping) else {}


def runtime_outputs(row: Mapping[str, Any]) -> Mapping[str, Any]:
    output = row.get("runtime_outputs", {})
    return output if isinstance(output, Mapping) else {}


def runtime_status(row: Mapping[str, Any]) -> tuple[str, str, str]:
    runtime = runtime_outputs(row)
    summary = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
    return (
        str(runtime.get("status") or row.get("status") or ""),
        str(runtime.get("wait_status") or ""),
        str(summary.get("deinit_reason") or ""),
    )


def telemetry_detail(row: Mapping[str, Any]) -> str:
    runtime = runtime_outputs(row)
    path_text = str(runtime.get("telemetry_path") or "")
    if not path_text:
        return ""
    path = Path(path_text)
    if not path.is_absolute():
        path = REPO_ROOT / path
    if not path_exists(path):
        return ""
    try:
        text = io_path(path).read_text(encoding="utf-8-sig", errors="ignore")
    except TypeError:
        text = io_path(path).read_text(encoding="utf-8-sig")
    for needle in ("ebm_table_open_failed:5003", "init_failed"):
        if needle in text:
            return needle
    return ""


def attempt_read(exec_row: Mapping[str, Any], report_row: Mapping[str, Any]) -> str:
    runtime, _, deinit_reason = runtime_status(exec_row)
    trades = as_int(report_metrics(report_row).get("trade_count"))
    detail = telemetry_detail(exec_row)
    if runtime == "completed" and trades > 0:
        return "usable_runtime_trade_evidence(사용 가능한 런타임 거래 근거)"
    if deinit_reason == "init_failed" or "ebm_table_open_failed" in detail:
        return "init_failure_ebm_table_open_blocks_candidate_evidence(EBM 테이블 열기 초기화 실패로 후보 근거 차단)"
    if trades == 0:
        return "zero_trade_report_no_candidate_evidence(무거래 보고서라 후보 근거 없음)"
    return "mixed_report_runtime_boundary_needed(보고서와 런타임 경계 추가 확인 필요)"


def build_attempt_outcomes(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts = attempt_by_name(payload)
    reports = report_by_attempt(payload)
    execs = execution_by_attempt(payload)
    output: list[dict[str, Any]] = []
    for attempt_name, attempt in sorted(attempts.items()):
        exec_row = execs.get(attempt_name, {})
        report_row = reports.get(attempt_name, {})
        runtime, wait_status, deinit_reason = runtime_status(exec_row)
        metrics = report_metrics(report_row)
        detail = telemetry_detail(exec_row)
        output.append(
            {
                "attempt_name": attempt_name,
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "profile_label": attempt.get("profile_label"),
                "risk_shape_mode": attempt.get("risk_shape_mode"),
                "queue_id": attempt.get("queue_id"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "execution_status": exec_row.get("status", ""),
                "runtime_status": runtime,
                "runtime_wait_status": wait_status,
                "runtime_deinit_reason": deinit_reason,
                "runtime_detail": detail,
                "report_status": report_row.get("status", ""),
                "report_trade_count": metrics.get("trade_count", ""),
                "report_net_profit": metrics.get("net_profit", ""),
                "report_profit_factor": metrics.get("profit_factor", ""),
                "report_equity_dd_percent": metrics.get("equity_drawdown_maximal_percent", ""),
                "report_path": rel(report_row.get("html_report", {}).get("path", "")) if report_row.get("html_report") else "",
                "attempt_read": attempt_read(exec_row, report_row),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def record_attempt_map(payload: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    attempts = attempt_by_name(payload)
    output: dict[str, dict[str, Any]] = {}
    for record in payload.get("mt5_kpi_records", []):
        record_view = str(record.get("record_view") or "")
        attempt_name = str(record.get("report", {}).get("attempt_name") or "")
        attempt = attempts.get(attempt_name, {})
        output[record_view] = {
            "attempt_name": attempt_name,
            "split": record.get("split") or attempt.get("split"),
            "tier": attempt.get("tier") or record.get("tier_scope"),
            "attempt_role": record.get("route_role") or "",
        }
    return output


def curve_read(item: Mapping[str, Any], report_metrics_row: Mapping[str, Any], month_rows: Sequence[Mapping[str, Any]]) -> str:
    equity_dd = as_float(report_metrics_row.get("equity_drawdown_maximal_percent") or item.get("closed_balance_max_drawdown_percent"))
    pf = as_float(item.get("profit_factor"))
    net = as_float(item.get("net_profit"))
    trades = as_int(item.get("trade_count"))
    worst_month_net = min((as_float(row.get("net_profit")) for row in month_rows), default=0.0)
    positive_month_ratio = (
        sum(1 for row in month_rows if as_float(row.get("net_profit")) >= 0.0) / len(month_rows)
        if month_rows
        else 0.0
    )
    if trades == 0 or net <= 0.0 or pf <= 1.0:
        return "empty_or_fragile_no_selection(비었거나 취약, 선택 아님)"
    if equity_dd >= 24.0 or worst_month_net <= -220.0:
        return "profit_with_uncomfortable_dd_or_month_hole(수익은 있으나 손실폭 또는 월별 구멍 불편)"
    if trades < 300 and pf >= 1.20 and equity_dd <= 16.0:
        return "constructive_but_supply_thin_no_selection(건설적이나 거래 공급 얇음, 선택 아님)"
    if net >= 1000.0 and pf >= 1.35 and trades >= 300 and positive_month_ratio >= 0.60:
        return "constructive_control_watch_no_selection(건설적 대조 관찰, 선택 아님)"
    if net > 0.0 and pf > 1.0:
        return "positive_but_quality_decay_watch_no_selection(양수지만 품질 약화 관찰, 선택 아님)"
    return "mixed_or_insufficient_no_selection(혼합 또는 근거 부족, 선택 아님)"


def weakest_bucket(time_rows: Sequence[Mapping[str, Any]], record_view: str, axis: str) -> Mapping[str, Any]:
    rows = [
        row
        for row in time_rows
        if row.get("record_view") == record_view and row.get("axis") == axis and as_int(row.get("trade_count")) >= 3
    ]
    return min(rows, key=lambda row: as_float(row.get("net_profit")), default={})


def profile_read(curve: Mapping[str, Any], weak_month: Mapping[str, Any]) -> str:
    net = as_float(curve.get("net_profit"))
    pf = as_float(curve.get("profit_factor"))
    trades = as_int(curve.get("trade_count"))
    dd = as_float(curve.get("report_equity_drawdown_percent"))
    worst_month_net = as_float(weak_month.get("net_profit"))
    label = str(curve.get("curve_read"))
    if "uncomfortable" in label or dd >= 24.0 or worst_month_net <= -220.0:
        return "profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)"
    if net <= 0.0 or pf <= 1.0:
        return "validation_or_quality_break_no_selection(검증 또는 품질 붕괴, 선택 아님)"
    if trades < 300:
        return "constructive_but_trade_supply_thin_no_selection(건설적이나 거래 수 얇음, 선택 아님)"
    if net >= 1000.0 and pf >= 1.35:
        return "constructive_defensive_control_only_no_selection(건설적 방어 대조 전용, 선택 아님)"
    return "positive_but_not_strong_enough_no_selection(양수지만 충분히 강하지 않음, 선택 아님)"


def build_candidate_profile_review(
    curve_rows: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
    attempt_outcomes: Sequence[Mapping[str, Any]],
    record_links: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    outcome_by_attempt = {str(row.get("attempt_name")): row for row in attempt_outcomes}
    output: list[dict[str, Any]] = []
    for row in curve_rows:
        record_link = record_links.get(str(row.get("record_view")), {})
        attempt_name = str(record_link.get("attempt_name") or "")
        outcome = outcome_by_attempt.get(attempt_name, {})
        weak_month = weakest_bucket(time_rows, str(row.get("record_view")), "month")
        weak_weekday = weakest_bucket(time_rows, str(row.get("record_view")), "weekday")
        weak_session = weakest_bucket(time_rows, str(row.get("record_view")), "session_report")
        weak_hour = weakest_bucket(time_rows, str(row.get("record_view")), "close_hour_report")
        weak_chron = weakest_bucket(time_rows, str(row.get("record_view")), "chron_segment")
        output.append(
            {
                "attempt_name": attempt_name,
                "record_view": row.get("record_view"),
                "candidate_id": row.get("candidate_id"),
                "candidate_alias": row.get("candidate_alias"),
                "candidate_role": row.get("candidate_role"),
                "profile_label": row.get("test_id"),
                "tier_scope": row.get("route_role"),
                "split": record_link.get("split", ""),
                "tier": record_link.get("tier", ""),
                "runtime_status": outcome.get("runtime_status", ""),
                "runtime_deinit_reason": outcome.get("runtime_deinit_reason", ""),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "expectancy": row.get("expectancy"),
                "report_equity_drawdown_percent": row.get("report_equity_drawdown_percent"),
                "report_balance_drawdown_percent": row.get("report_balance_drawdown_percent"),
                "recovery_factor": row.get("report_recovery_factor"),
                "positive_month_ratio": row.get("positive_month_ratio"),
                "negative_month_count": row.get("negative_month_count"),
                "worst_month": weak_month.get("bucket", ""),
                "worst_month_net": weak_month.get("net_profit", ""),
                "weakest_weekday": weak_weekday.get("bucket", ""),
                "weakest_weekday_net": weak_weekday.get("net_profit", ""),
                "weakest_session": weak_session.get("bucket", ""),
                "weakest_session_net": weak_session.get("net_profit", ""),
                "weakest_hour": weak_hour.get("bucket", ""),
                "weakest_hour_net": weak_hour.get("net_profit", ""),
                "weakest_chron_segment": weak_chron.get("bucket", ""),
                "weakest_chron_net": weak_chron.get("net_profit", ""),
                "source_chart_path": row.get("source_chart_path"),
                "curve_read": row.get("curve_read"),
                "profile_read": profile_read(row, weak_month),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(output, key=lambda item: (-as_float(item.get("net_profit")), str(item.get("candidate_alias"))))


def init_summary_read(alias: str, attempts: Sequence[Mapping[str, Any]], completed: Sequence[Mapping[str, Any]]) -> str:
    init_failures = [row for row in attempts if str(row.get("runtime_deinit_reason")) == "init_failed"]
    total_net = sum(as_float(row.get("net_profit")) for row in completed)
    max_dd = max((as_float(row.get("report_equity_drawdown_percent")) for row in completed), default=0.0)
    if alias == "s258_stc" and completed and max_dd >= 25.0:
        return "profit_survives_but_dd_and_weak_slices_fragile_no_selection(수익은 살아남지만 손실폭과 약한 구간 취약, 선택 아님)"
    if alias == "s264_aih" and init_failures and completed and total_net < 0:
        return "final_month_negative_and_validation_init_failure_no_selection(마지막 달 음수와 검증 초기화 실패, 선택 아님)"
    if alias == "s264_lc" and completed and total_net < 0:
        return "defensive_control_final_month_negative_no_selection(방어 대조 마지막 달 음수, 선택 아님)"
    if init_failures and not completed:
        return "init_failure_dominant_prune_or_rebuild(초기화 실패 지배, 가지치기 또는 재구성)"
    return "reviewed_no_selection(검토 완료, 선택 아님)"


def next_probe_for_candidate(alias: str) -> str:
    if alias == "s258_stc":
        return "separate_hour16_monday_202512_weakness_from_impulse_or_prune(16시, 월요일, 2025-12 약점을 충격 구조와 분리하거나 가지치기)"
    if alias == "s264_aih":
        return "repair_validation_anchor_once_then_prune_if_final_month_negative_persists(검증 앵커를 한 번만 수리하고 마지막 달 음수가 지속되면 가지치기)"
    if alias == "s264_lc":
        return "keep_as_same_month_control_only_no_challenger_claim(같은 월 대조로만 유지, 도전자 주장 없음)"
    return "no_followup_until_runtime_evidence_exists(런타임 근거 전까지 후속 보류)"


def build_candidate_init_failure_summary(
    attempt_outcomes: Sequence[Mapping[str, Any]],
    candidate_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    attempts_by_candidate: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    rows_by_candidate: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in attempt_outcomes:
        attempts_by_candidate[str(row.get("candidate_alias"))].append(row)
    for row in candidate_rows:
        rows_by_candidate[str(row.get("candidate_alias"))].append(row)

    output: list[dict[str, Any]] = []
    for alias in sorted(attempts_by_candidate):
        attempts = attempts_by_candidate[alias]
        completed = rows_by_candidate.get(alias, [])
        output.append(
            {
                "candidate_alias": alias,
                "candidate_roles": ";".join(sorted({str(row.get("candidate_role")) for row in attempts if row.get("candidate_role")})),
                "attempt_count": len(attempts),
                "runtime_completed_attempts": sum(1 for row in attempts if row.get("runtime_status") == "completed"),
                "runtime_blocked_attempts": sum(1 for row in attempts if row.get("runtime_status") != "completed"),
                "init_failure_attempts": sum(1 for row in attempts if row.get("runtime_deinit_reason") == "init_failed"),
                "ebm_table_open_failure_attempts": sum(1 for row in attempts if "ebm_table_open_failed" in str(row.get("runtime_detail"))),
                "zero_trade_report_attempts": sum(1 for row in attempts if as_int(row.get("report_trade_count")) == 0),
                "completed_profile_rows": len(completed),
                "avg_completed_net_profit": mean(as_float(row.get("net_profit")) for row in completed) if completed else "",
                "avg_completed_profit_factor": mean(as_float(row.get("profit_factor")) for row in completed) if completed else "",
                "max_completed_dd_percent": max((as_float(row.get("report_equity_drawdown_percent")) for row in completed), default=""),
                "worst_completed_month_net": min((as_float(row.get("worst_month_net")) for row in completed), default=""),
                "summary_read": init_summary_read(alias, attempts, completed),
                "next_probe": next_probe_for_candidate(alias),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 100) -> list[dict[str, Any]]:
    rows = [
        row
        for row in time_rows
        if as_float(row.get("net_profit")) < 0.0 and as_int(row.get("trade_count")) >= 3
    ]
    return [dict(row) for row in sorted(rows, key=lambda row: as_float(row.get("net_profit")))[:limit]]


def likely_driver(alias: str) -> str:
    if alias == "s258_stc":
        return "monday_late_dd_taper(월요일/후반 손실폭 완화)는 거래를 만들었지만 2025 H1 validation(2025 상반기 검증)과 2025 H2 OOS(2025 하반기 표본외)에서 품질이 약했고, supply_continuity(공급 연속성)는 EBM table open failure(EBM 테이블 열기 실패)로 막혔다."
    if alias == "s264_lc":
        return "dd_zoom_control(손실폭 확대 대조)은 2024 historical(2024 과거 기간)에서 수익과 거래 수를 만들었지만 DD(drawdown, 손실폭) 24%대가 방어 대조로도 불편하다."
    return "runtime evidence(런타임 근거)가 부족하다."


def build_attribution_summary(candidate_summary: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in candidate_summary:
        alias = str(row.get("candidate_alias"))
        output.append(
            {
                "candidate_alias": alias,
                "observed_change": (
                    f"attempts={row.get('attempt_count')};completed={row.get('runtime_completed_attempts')};"
                    f"init_failures={row.get('init_failure_attempts')};avg_net={row.get('avg_completed_net_profit')};"
                    f"max_dd={row.get('max_completed_dd_percent')}"
                ),
                "comparison_baseline": "run267DV MT5 execution(267DV MT5 실행) source KPI(원천 핵심 성과 지표) and telemetry(텔레메트리)",
                "likely_drivers": likely_driver(alias),
                "segment_checks": "month/weekday/session/hour/chron_segment(월/요일/세션/시간/시간순 구간) from completed runtime rows; init failure(초기화 실패)는 별도 실패 기억으로 분리",
                "trade_shape": (
                    f"completed_profile_rows={row.get('completed_profile_rows')};"
                    f"avg_pf={row.get('avg_completed_profit_factor')};zero_trade={row.get('zero_trade_report_attempts')}"
                ),
                "alternative_explanations": "feature/model table handoff(피처/모델 테이블 인계) 오류, overly narrow risk shape(과하게 좁은 위험 형태), duplicate-boundary Tier A+B(중복 경계 티어 A+B) 해석 한계",
                "attribution_confidence": "medium" if as_int(row.get("completed_profile_rows")) else "low",
                "next_probe": row.get("next_probe"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def result_status(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return PARTIAL_STATUS if parser_errors else STATUS


def result_next_action(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return NEXT_ACTION_PARTIAL if parser_errors else NEXT_ACTION


def build_result_judgment(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267DW runtime gap aware fifth follow-up/prune balance/time-slice/trade-quality review(267DW 런타임 공백 반영 5차 후속/가지치기 잔액/시간구간/거래품질 검토)",
            "evidence_available": "run267DV Strategy Tester reports(267DV 전략 테스터 보고서), runtime telemetry(런타임 텔레메트리), trade records(거래 기록), time-slice KPI(시간구간 핵심 성과 지표), init failure summary(초기화 실패 요약)",
            "evidence_missing": "Adapter package(어댑터 패키지), runtime reproduction closure(런타임 재현 종결), ONNX parity(ONNX 동등성), final candidate race package(최종 후보 경주 패키지)",
            "judgment_label": "review_completed_with_init_failures_no_candidate_selection",
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_condition": result["next_action"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_rows = list(result["candidate_profile_review"])
    summary_rows = list(result["candidate_init_failure_summary"])
    attempt_rows = list(result["attempt_outcome_review"])
    negative = sorted(result["negative_slices"], key=lambda row: as_float(row.get("net_profit")))[:12]
    lines = [
        "# Stage267 Run267DW Runtime Gap Aware Fifth Follow-Up/Prune Review(267단계 267DW 런타임 공백 반영 5차 후속/가지치기 검토)",
        "",
        f"- status(상태): `{result['status']}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- attempts_reviewed(검토 시도): `{len(attempt_rows)}`",
        f"- runtime_completed_attempts(런타임 완료 시도): `{sum(1 for row in attempt_rows if row.get('runtime_status') == 'completed')}`",
        f"- init_failure_attempts(초기화 실패 시도): `{sum(1 for row in attempt_rows if row.get('runtime_deinit_reason') == 'init_failed')}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- candidate_profile_rows(후보-프로필 행): `{len(candidate_rows)}`",
        f"- negative_slices(음수 구간): `{len(result['negative_slices'])}`",
        f"- next_action(다음 행동): `{result['next_action']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267DW(267DW 실행)는 run267DV(267DV 실행)의 MT5(MetaTrader 5, 메타트레이더5) 결과를 숫자만 보지 않고 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), init failure(초기화 실패)로 다시 읽었다.",
        "효과: s258_stc(258 STC 후보)는 table handoff repair(테이블 인계 수리)와 aggressive noncalendar impulse(공격형 비달력 충격) 모두 거래 근거가 생겼지만, 2025H1/2025H2의 DD(drawdown, 손실폭)와 recovery(회복)가 불편한지 분리해 본다.",
        "효과: s264_aih(264 AIH 후보)는 2026.04 final-month explosive probe(마지막 달 폭발형 탐침)가 음수이고 validation anchor(검증 앵커)는 init failure(초기화 실패)라서, 공격형 단서와 수리 필요성을 같은 표면에서 분리한다. s264_lc(264 LC 후보)는 같은 2026.04 방어 대조로 비교한다.",
        "",
        "## Candidate Summary(후보 요약)",
        "",
        "| candidate(후보) | attempts(시도) | completed(완료) | init_fail(초기화 실패) | avg_net(평균 순수익) | max_DD%(최대 손실폭 %) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in summary_rows:
        avg_net = row.get("avg_completed_net_profit")
        max_dd = row.get("max_completed_dd_percent")
        lines.append(
            "| "
            f"`{row.get('candidate_alias')}` | {row.get('attempt_count')} | {row.get('runtime_completed_attempts')} | "
            f"{row.get('init_failure_attempts')} | "
            f"{round(as_float(avg_net), 2) if avg_net != '' else ''} | "
            f"{round(as_float(max_dd), 2) if max_dd != '' else ''} | "
            f"`{row.get('summary_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Completed Profiles(완료 프로필)",
            "",
            "| candidate(후보) | profile(프로필) | split(구간) | tier(티어) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst_month(최악 월) | read(판독) |",
            "|---|---|---|---|---:|---:|---:|---:|---|---|",
        ]
    )
    for row in candidate_rows:
        lines.append(
            "| "
            f"`{row.get('candidate_alias')}` | `{row.get('profile_label')}` | `{row.get('split')}` | `{row.get('tier_scope')}` | "
            f"{round(as_float(row.get('net_profit')), 2)} | {round(as_float(row.get('profit_factor')), 4)} | "
            f"{as_int(row.get('trade_count'))} | {round(as_float(row.get('report_equity_drawdown_percent')), 2)} | "
            f"`{row.get('worst_month')}` | `{row.get('profile_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Weak Slice Watch(약한 구간 관찰)",
            "",
            "| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | net_profit(순수익) | trades(거래 수) |",
            "|---|---|---|---|---:|---:|",
        ]
    )
    for row in negative:
        lines.append(
            "| "
            f"`{row.get('candidate_alias')}` | `{row.get('test_id')}` | `{row.get('axis')}` | `{row.get('bucket')}` | "
            f"{round(as_float(row.get('net_profit')), 2)} | {as_int(row.get('trade_count'))} |"
        )
    lines.extend(
        [
            "",
            "## Init Failure Boundary(초기화 실패 경계)",
            "",
            "- run267du_07(267DU 07 시도)은 Strategy Tester report(전략 테스터 보고서)는 생성됐지만 runtime telemetry(런타임 텔레메트리)가 `init_failed`를 남긴 init failure(초기화 실패) 행이다.",
            "- 이 행은 zero-trade success(무거래 성공)가 아니라 candidate evidence blocked(후보 근거 차단)로 해석한다.",
            "- Tier A+B(티어 A+B)는 duplicate-boundary(중복 경계)라 실제 fallback(대체) 복원 근거로 쓰지 않는다.",
            "",
            "## Boundary(경계)",
            "",
            "Run267DW(267DW 실행)는 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간구간 핵심 성과 지표): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            f"- candidate_profile_review(후보 프로필 검토): `{rel(CANDIDATE_PROFILE_REVIEW_PATH)}`",
            f"- candidate_init_failure_summary(후보 초기화 실패 요약): `{rel(CANDIDATE_INIT_FAILURE_SUMMARY_PATH)}`",
            f"- attempt_outcome_review(시도 결과 검토): `{rel(ATTEMPT_OUTCOME_REVIEW_PATH)}`",
            f"- performance_attribution_summary(성과 귀속 요약): `{rel(ATTRIBUTION_SUMMARY_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267DW_producer", "producer_script", PRODUCER_PATH, "Builds run267DW balance/time-slice review with init failures."),
        ("stage267_run267DW_source_execution_result", "source_execution_result", SOURCE_EXECUTION_RESULT_PATH, "Source run267DV execution result."),
        ("stage267_run267DW_trade_records", "trade_records", TRADE_RECORDS_PATH, "Parsed completed runtime trade records."),
        ("stage267_run267DW_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Time-slice KPI for completed runtime rows."),
        ("stage267_run267DW_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Curve diagnostics for completed runtime rows."),
        ("stage267_run267DW_candidate_profile_review", "candidate_profile_review", CANDIDATE_PROFILE_REVIEW_PATH, "Candidate-profile completed runtime review."),
        ("stage267_run267DW_candidate_init_failure_summary", "candidate_init_failure_summary", CANDIDATE_INIT_FAILURE_SUMMARY_PATH, "Candidate init failure summary."),
        ("stage267_run267DW_attempt_outcome_review", "attempt_outcome_review", ATTEMPT_OUTCOME_REVIEW_PATH, "Attempt-level runtime/report outcome review."),
        ("stage267_run267DW_negative_slice", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Weak negative time slices."),
        ("stage267_run267DW_attribution", "performance_attribution_summary", ATTRIBUTION_SUMMARY_PATH, "Performance attribution with init failure boundary."),
        ("stage267_run267DW_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DW_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Parser checks."),
        ("stage267_run267DW_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267DW_report", "review_report", REPORT_PATH, "User-facing review report."),
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


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    notes = (
        f"candidate_profile_rows={len(result['candidate_profile_review'])};"
        f"init_failure_attempts={result['init_failure_attempts']};"
        f"negative_slices={len(result['negative_slices'])};"
        f"next_action={result['next_action']}."
    )
    stage_row = {
        "row_id": "stage267_run267DW_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures",
        "tier_scope": "Tier A completed rows and duplicate-boundary Tier A+B row; true fallback not claimed",
        "scoreboard": "trade_curve_time_slice_trade_quality_init_failure",
        "status": status,
        "judgment": "review_completed_with_init_failures_no_candidate_selection",
        "evidence_boundary": "mt5_trade_list_curve_time_slice_init_failure_review_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_gap_aware_init_failure_balance_timeslice_trade_quality_review",
        "status": status,
        "judgment": "review_completed_with_init_failures_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__balance_timeslice_trade_quality_init_failure_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "balance_timeslice_trade_quality_init_failure_review",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures",
        "tier_scope": "Tier A and duplicate Tier A+B rows with init failure boundary",
        "kpi_scope": "trade_curve_time_slice_trade_quality_init_failure",
        "scoreboard_lane": "runtime_gap_aware_init_failure_review",
        "status": status,
        "judgment": "review_completed_with_init_failures_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "primary_kpi": f"candidate_profile_rows={len(result['candidate_profile_review'])};init_failure_attempts={result['init_failure_attempts']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "completed",
        "notes": f"Next action: {result['next_action']}. Init failures are failure memory, not candidate evidence.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


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
            insert_at = index + 1
            while insert_at < len(lines) and lines[insert_at].startswith("  "):
                insert_at += 1
            lines.insert(insert_at, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def update_stage267_workspace_block(text: str, *, status: str, next_action: str) -> str:
    report_entry = f"  run267DW_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}"
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


def update_current_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    completed_attempts = sum(1 for row in result["attempt_outcome_review"] if row.get("runtime_status") == "completed")
    report_line = (
        "- run267DW_runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_review"
        f"(267DW 런타임 공백 반영 5차 후속/가지치기 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    )
    latest_line = (
        f"- latest_review(최신 검토): run267DW(267DW 실행) candidate_profile_rows(후보-프로필 행) "
        f"`{len(result['candidate_profile_review'])}`, init_failure_attempts(초기화 실패 시도) "
        f"`{result['init_failure_attempts']}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    block = "\n".join(
        [
            "Run267DW(267DW 실행)는 run267DV(267DV 실행)의 completed runtime(완료 런타임) 행과 init failure(초기화 실패) 행을 분리해 balance/time-slice/trade-quality(잔액/시간구간/거래품질)로 다시 읽었다.",
            f"Effect(효과): candidate_profile_rows(후보-프로필 행) `{len(result['candidate_profile_review'])}`, init_failure_attempts(초기화 실패 시도) `{result['init_failure_attempts']}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`를 만들었고, 다음은 runtime gap aware sixth follow-up/prune design(런타임 공백 반영 6차 후속/가지치기 설계)이다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(
        current,
        "- adapter_under_review(검토 중 어댑터):",
        "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_fifth_followup_or_prune_balance_timeslice_trade_quality_with_init_failures`",
    )
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    current = append_after_contains(current, "stage267_run267DV_runtime_gap_aware_fifth_followup_or_prune_mt5_execution.md", report_line)
    current = append_after_contains(current, "## Current Next Action", latest_line)
    current = append_block_once(current, "Run267DW(267DW 실행)는 run267DV", block)
    review_base.write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selection = append_after_contains(selection, "stage267_run267DV_runtime_gap_aware_fifth_followup_or_prune_mt5_execution", report_line)
    selection = append_block_once(selection, "Run267DW(267DW 실행)는 run267DV", block)
    review_base.write_md(SELECTION_STATUS_PATH, selection)

    review_index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_index = replace_line_prefix(review_index, "- status(상태):", f"- status(상태): `{status}`")
    review_index = replace_line_prefix(review_index, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(review_index, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review_index = append_after_contains(review_index, "stage267_run267DV_runtime_gap_aware_fifth_followup_or_prune_mt5_execution.md", report_line)
    review_index = append_block_once(review_index, "Run267DW(267DW 실행)는 run267DV", block)
    review_base.write_md(REVIEW_INDEX_PATH, review_index)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = update_stage267_workspace_block(workspace, status=status, next_action=next_action)
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267DW(267DW 실행) runtime gap aware fifth follow-up/prune balance/time-slice/trade-quality review"
        f"(런타임 공백 반영 5차 후속/가지치기 잔액/시간구간/거래품질 검토) `{status}`. "
        f"Effect(효과): run267DV(267DV 실행)의 completed runtime(완료 런타임) `{completed_attempts}`개와 init failure(초기화 실패) `{result['init_failure_attempts']}`개를 분리했고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if f"`{status}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_line, 1)
    review_base.write_md(WORKSPACE_STATE_PATH, workspace)


def build_review() -> dict[str, Any]:
    configure_review_base()
    created_at = utc_now()
    payload = normalize_execution_result(review_base.read_json(SOURCE_EXECUTION_RESULT_PATH))
    attempt_outcomes = build_attempt_outcomes(payload)
    trade_rows, parser_errors, parser_checks = review_base.build_trade_records(payload)
    time_rows = review_base.build_time_slice_rows(trade_rows)
    curve_rows = review_base.build_curve_rows(trade_rows, time_rows, payload)
    candidate_rows = build_candidate_profile_review(curve_rows, time_rows, attempt_outcomes, record_attempt_map(payload))
    candidate_summary = build_candidate_init_failure_summary(attempt_outcomes, candidate_rows)
    negative = negative_slices(time_rows)
    attribution = build_attribution_summary(candidate_summary)
    status = result_status(parser_errors)
    next_action = result_next_action(parser_errors)
    result = {
        "status": status,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_outcome_review": attempt_outcomes,
        "init_failure_attempts": sum(1 for row in attempt_outcomes if row.get("runtime_deinit_reason") == "init_failed"),
        "ebm_table_open_failure_attempts": sum(1 for row in attempt_outcomes if "ebm_table_open_failed" in str(row.get("runtime_detail"))),
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "candidate_profile_review": candidate_rows,
        "candidate_init_failure_summary": candidate_summary,
        "negative_slices": negative,
        "performance_attribution_summary": attribution,
        "parser_errors": parser_errors,
        "parser_checks": parser_checks,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
        "outputs": {
            "trade_records": rel(TRADE_RECORDS_PATH),
            "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
            "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
            "candidate_profile_review": rel(CANDIDATE_PROFILE_REVIEW_PATH),
            "candidate_init_failure_summary": rel(CANDIDATE_INIT_FAILURE_SUMMARY_PATH),
            "attempt_outcome_review": rel(ATTEMPT_OUTCOME_REVIEW_PATH),
            "negative_slice_summary": rel(NEGATIVE_SLICE_PATH),
            "performance_attribution_summary": rel(ATTRIBUTION_SUMMARY_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "parser_checks": rel(PARSER_CHECKS_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    result_judgment = build_result_judgment(result)

    review_base.write_csv(
        TRADE_RECORDS_PATH,
        trade_rows,
        (
            "run_id",
            "source_run_id",
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "test_type",
            "materialization_boundary",
            "record_view",
            "attempt_name",
            "tier_scope",
            "route_role",
            "split",
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
        ),
    )
    review_base.write_csv(
        TIME_SLICE_KPI_PATH,
        time_rows,
        (
            "record_view",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "test_type",
            "materialization_boundary",
            "route_role",
            "axis",
            "bucket",
            *METRIC_COLUMNS,
            "slice_read",
        ),
    )
    review_base.write_csv(
        CURVE_DIAGNOSTICS_PATH,
        curve_rows,
        (
            "record_view",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "test_type",
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
        ),
    )
    review_base.write_csv(CANDIDATE_PROFILE_REVIEW_PATH, candidate_rows, columns(candidate_rows, ("candidate_alias", "profile_label", "net_profit")))
    review_base.write_csv(CANDIDATE_INIT_FAILURE_SUMMARY_PATH, candidate_summary, columns(candidate_summary, ("candidate_alias", "summary_read")))
    review_base.write_csv(ATTEMPT_OUTCOME_REVIEW_PATH, attempt_outcomes, columns(attempt_outcomes, ("attempt_name", "attempt_read")))
    review_base.write_csv(NEGATIVE_SLICE_PATH, negative, columns(negative, ("candidate_alias", "test_id", "axis", "bucket", "net_profit")))
    review_base.write_csv(PARSER_CHECKS_PATH, parser_checks, columns(parser_checks, ("attempt_name", "parser_status")))
    review_base.write_csv(ATTRIBUTION_SUMMARY_PATH, attribution, columns(attribution, ("candidate_alias", "observed_change", "next_probe")))
    review_base.write_csv(RESULT_JUDGMENT_PATH, result_judgment, columns(result_judgment, ("result_subject", "judgment_label")))
    review_base.write_json(REVIEW_RESULT_PATH, result)
    review_base.write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_docs(result)
    return result


def main() -> int:
    result = build_review()
    print(
        json.dumps(
            {
                "status": result["status"],
                "attempts_reviewed": len(result["attempt_outcome_review"]),
                "init_failure_attempts": result["init_failure_attempts"],
                "ebm_table_open_failure_attempts": result["ebm_table_open_failure_attempts"],
                "trade_records": result["trade_record_count"],
                "candidate_profile_rows": len(result["candidate_profile_review"]),
                "negative_slices": len(result["negative_slices"]),
                "parser_errors": len(result["parser_errors"]),
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
