from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
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
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import run267DZ_runtime_gap_aware_sixth_followup_or_prune_mt5_executor as source_executor
from stage_pipelines.stage267 import run267O_pool_wide_balance_timeslice_trade_quality_review as review_base


STAGE_ID = source_executor.STAGE_ID
SOURCE_RUN_ID = source_executor.RUN_ID
RUN_NUMBER = "run267EA"
RUN_ID = "run267EA_stage267_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review_v1"
STATUS = "run267EA_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review_completed"
PARTIAL_STATUS = "run267EA_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review_partial_parser_errors"
NEXT_ACTION = "run267EB_design_runtime_gap_aware_seventh_followup_or_prune_from_run267EA_review"
NEXT_ACTION_PARTIAL = "run267EA_repair_trade_report_parser_before_seventh_followup_design"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review"
SOURCE_ROOT = source_executor.RUN_ROOT
SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
SOURCE_REPORT_PATH = source_executor.REPORT_PATH
SOURCE_KPI_SUMMARY_PATH = source_executor.KPI_SUMMARY_PATH
SOURCE_FORENSICS_PATH = source_executor.FORENSICS_PATH

TRADE_RECORDS_PATH = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = RUN_ROOT / "curve_diagnostics.csv"
CANDIDATE_PROFILE_REVIEW_PATH = RUN_ROOT / "candidate_profile_review.csv"
ATTEMPT_OUTCOME_REVIEW_PATH = RUN_ROOT / "attempt_outcome_review.csv"
NEGATIVE_SLICE_PATH = RUN_ROOT / "negative_slice_summary.csv"
PARSER_CHECKS_PATH = RUN_ROOT / "parser_checks.csv"
ATTRIBUTION_SUMMARY_PATH = RUN_ROOT / "performance_attribution_summary.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267EA_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267EA_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review.py")

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
    if not rows:
        return tuple(fallback)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(str(key))
    return tuple(ordered)


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
    review_base.slice_read = slice_read


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
        next_attempt["test_type"] = next_attempt.get("attempt_role") or profile
        next_attempt["materialization_boundary"] = (
            next_attempt.get("tier_pair_boundary")
            or next_attempt.get("materialization_boundary")
            or "Tier A and duplicate-boundary only(티어 A 및 중복 경계만)"
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


def group_by(rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, list[Mapping[str, Any]]]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(key) or "")].append(row)
    return grouped


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


def slice_read(item: Mapping[str, Any]) -> str:
    count = as_int(item.get("trade_count"))
    net = as_float(item.get("net_profit"))
    dd_pct = as_float(item.get("closed_balance_max_drawdown_percent"))
    if count < 3:
        return "thin_slice(얇은 구간)"
    if net <= -150.0 or dd_pct >= 30.0:
        return "deep_negative_or_dd_slice(깊은 음수 또는 손실폭 구간)"
    if net < -50.0:
        return "negative_fragile_slice(음수 취약 구간)"
    if net < 0.0:
        return "minor_negative_slice(작은 음수 구간)"
    return "measured_slice(측정 구간)"


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
        return "negative_or_fragile_no_selection(음수 또는 취약, 선택 아님)"
    if equity_dd >= 22.0 or worst_month_net <= -160.0:
        return "profit_with_uncomfortable_dd_or_month_hole(수익은 있으나 손실폭 또는 월별 구멍 불편)"
    if trades < 80 and pf >= 1.10:
        return "thin_final_month_probe_no_selection(얇은 마지막 달 탐침, 선택 아님)"
    if trades >= 250 and net >= 900.0 and pf >= 1.45 and equity_dd <= 16.0 and positive_month_ratio >= 0.50:
        return "constructive_cross_period_watch_no_selection(건설적 확장 기간 관찰, 선택 아님)"
    if net > 0.0 and pf > 1.05:
        return "positive_but_needs_slice_review_no_selection(양수지만 구간 검토 필요, 선택 아님)"
    return "mixed_or_fragile_no_selection(혼합 또는 취약, 선택 아님)"


def attempt_read(exec_row: Mapping[str, Any], report_row: Mapping[str, Any]) -> str:
    runtime, _, deinit_reason = runtime_status(exec_row)
    trades = as_int(report_metrics(report_row).get("trade_count"))
    if runtime == "completed" and trades > 0:
        return "usable_runtime_trade_evidence(사용 가능한 런타임 거래 근거)"
    if deinit_reason == "init_failed":
        return "init_failure_blocks_candidate_evidence(초기화 실패로 후보 근거 차단)"
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
        output.append(
            {
                "attempt_name": attempt_name,
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "profile_label": attempt.get("profile_label"),
                "attempt_role": attempt.get("attempt_role"),
                "queue_id": attempt.get("queue_id"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "execution_status": exec_row.get("status", ""),
                "runtime_status": runtime,
                "runtime_wait_status": wait_status,
                "runtime_deinit_reason": deinit_reason,
                "report_status": report_row.get("status", ""),
                "report_trade_count": metrics.get("trade_count", ""),
                "report_net_profit": metrics.get("net_profit", ""),
                "report_profit_factor": metrics.get("profit_factor", ""),
                "report_equity_dd_percent": metrics.get("equity_drawdown_maximal_percent", ""),
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
            "attempt_role": attempt.get("attempt_role") or "",
        }
    return output


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
    if net <= 0.0 or pf <= 1.0:
        return "final_month_break_no_selection(마지막 달 붕괴, 선택 아님)"
    if "uncomfortable" in label or dd >= 22.0 or worst_month_net <= -160.0:
        return "profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)"
    if trades < 80:
        return "thin_probe_only_no_selection(얇은 탐침일 뿐, 선택 아님)"
    if net >= 900.0 and pf >= 1.45 and trades >= 250:
        return "constructive_watch_but_not_baseline_selection(건설적 관찰이나 기준 후보 선택 아님)"
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
                "attempt_role": record_link.get("attempt_role", ""),
                "split": record_link.get("split", ""),
                "tier": record_link.get("tier", ""),
                "runtime_status": outcome.get("runtime_status", ""),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "expectancy": row.get("expectancy"),
                "report_equity_drawdown_percent": row.get("report_equity_drawdown_percent"),
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
                "curve_read": row.get("curve_read"),
                "profile_read": profile_read(row, weak_month),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 80) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in time_rows
        if as_int(row.get("trade_count")) >= 3 and as_float(row.get("net_profit")) < 0.0
    ]
    rows.sort(key=lambda row: (as_float(row.get("net_profit")), -as_int(row.get("trade_count"))))
    return rows[:limit]


def build_attribution_summary(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for alias, rows in group_by(candidate_rows, "candidate_alias").items():
        total_net = sum(as_float(row.get("net_profit")) for row in rows)
        worst_dd = max((as_float(row.get("report_equity_drawdown_percent")) for row in rows), default=0.0)
        weakest = min(rows, key=lambda row: as_float(row.get("net_profit")), default={})
        best = max(rows, key=lambda row: as_float(row.get("net_profit")), default={})
        if alias == "s258_stc":
            observed = "s258_stc는 2023H2는 강하지만 2025H1/H2에서 PF(수익 팩터)와 DD(손실폭)가 불편해 stress challenger(압박 도전자) 위험이 계속 남는다."
            next_probe = "seventh follow-up(7차 후속)에서는 DD shape(손실폭 형태)와 adverse state(불리 상태)를 합치기보다 약한 기간별 생존 조건을 먼저 판정한다."
        elif alias == "s264_aih":
            observed = "s264_aih는 validation anchor(검증 앵커)는 회복됐지만 2026.04 counter shock(역충격)에서 음수라 final-month hole(마지막 달 구멍)이 남는다."
            next_probe = "validation repair(검증 수리)와 final-month shock(마지막 달 충격)을 분리해 repair cap(수리 제한) 안에서 살릴지 버릴지 결정한다."
        else:
            observed = "s264_lc control(대조)은 같은 2026.04에서 음수라 s264_aih 약점이 후보 단독 문제가 아니라 시장 구간 문제일 수 있음을 보여준다."
            next_probe = "control(대조)은 selection(선택)용이 아니라 해석 기준으로만 유지한다."
        output.append(
            {
                "candidate_alias": alias,
                "rows": len(rows),
                "total_net_profit": total_net,
                "worst_equity_dd_percent": worst_dd,
                "best_profile": best.get("profile_label", ""),
                "best_net_profit": best.get("net_profit", ""),
                "weakest_profile": weakest.get("profile_label", ""),
                "weakest_net_profit": weakest.get("net_profit", ""),
                "observed_change": observed,
                "next_probe": next_probe,
                "selection_boundary": "no_selected_candidate_no_selected_research_baseline_no_onnx",
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
            "result_subject": "run267EA balance/time-slice/trade-quality review(267EA 잔액/시간구간/거래품질 검토)",
            "evidence_available": "trade_records(거래 기록), time_slice_kpi(시간구간 KPI), curve_diagnostics(곡선 진단), candidate_profile_review(후보 프로필 검토), negative_slice_summary(음수 구간 요약)",
            "evidence_missing": "visual curve inspection(시각 곡선 검사), next materialization(다음 물질화), Adapter package(어댑터 패키지), ONNX parity(ONNX 동등성)",
            "judgment_label": "exploratory_review_completed_no_selection",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": result["next_action"],
            "user_explanation_hook": "이번 검토는 후보 선택이 아니라 run267DZ의 거래·곡선·약한 구간을 다음 설계 재료로 바꾸는 작업이다.",
        }
    ]


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267EA_producer", "producer_script", PRODUCER_PATH, "Builds run267EA balance/time-slice/trade-quality review."),
        ("stage267_run267EA_source_execution", "source_execution_result", SOURCE_EXECUTION_RESULT_PATH, "Source run267DZ execution result."),
        ("stage267_run267EA_trade_records", "trade_records", TRADE_RECORDS_PATH, "Parsed trade records."),
        ("stage267_run267EA_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Time-slice KPI."),
        ("stage267_run267EA_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Curve diagnostics."),
        ("stage267_run267EA_candidate_profile_review", "candidate_profile_review", CANDIDATE_PROFILE_REVIEW_PATH, "Candidate profile review."),
        ("stage267_run267EA_attempt_outcome_review", "attempt_outcome_review", ATTEMPT_OUTCOME_REVIEW_PATH, "Attempt outcome review."),
        ("stage267_run267EA_negative_slices", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Negative slice summary."),
        ("stage267_run267EA_attribution_summary", "performance_attribution_summary", ATTRIBUTION_SUMMARY_PATH, "Performance attribution summary."),
        ("stage267_run267EA_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267EA_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267EA_report", "review_report", REPORT_PATH, "User-facing review report."),
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
    notes = (
        f"candidate_profile_rows={len(result['candidate_profile_review'])};"
        f"negative_slices={len(result['negative_slices'])};"
        f"next_action={result['next_action']}."
    )
    stage_row = {
        "row_id": "stage267_run267EA_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review",
        "tier_scope": "Tier A completed rows; true fallback not claimed",
        "scoreboard": "trade_curve_time_slice_trade_quality",
        "status": result["status"],
        "judgment": "review_completed_no_candidate_selection",
        "evidence_boundary": "mt5_trade_list_curve_time_slice_review_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review",
        "status": result["status"],
        "judgment": "review_completed_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "balance_timeslice_trade_quality_review",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review",
        "tier_scope": "Tier A completed rows",
        "kpi_scope": "trade_curve_time_slice_trade_quality",
        "scoreboard_lane": "runtime_gap_aware_sixth_followup_or_prune_review",
        "status": result["status"],
        "judgment": "review_completed_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "primary_kpi": f"candidate_profile_rows={len(result['candidate_profile_review'])};negative_slices={len(result['negative_slices'])}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "completed",
        "notes": f"Next action: {result['next_action']}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


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
    report_entry = f"  run267EA_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}"
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
    report_line = (
        "- run267EA_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review"
        f"(267EA 런타임 공백 반영 6차 후속/가지치기 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267EA(267EA 실행)는 run267DZ(267DZ 실행)의 9개 MT5(MetaTrader 5, 메타트레이더5) 결과를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.",
            f"Effect(효과): candidate_profile_rows(후보-프로필 행) `{len(result['candidate_profile_review'])}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`를 만들었고, 다음은 seventh follow-up/prune design(7차 후속/가지치기 설계)이다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- status(", f"- status(상태): `{status}`")
            text = replace_line_containing(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "stage267_run267DZ_runtime_gap_aware_sixth_followup_or_prune_mt5_execution.md", report_line)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_containing(text, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "stage267_run267DZ_runtime_gap_aware_sixth_followup_or_prune_mt5_execution", report_line)
        else:
            text = replace_line_containing(text, "- status(", f"- status(상태): `{status}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "stage267_run267DZ_runtime_gap_aware_sixth_followup_or_prune_mt5_execution.md", report_line)
        text = append_block_once(text, "Run267EA(267EA 실행)는 run267DZ", block)
        review_base.write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_containing(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267EA(267EA 실행) runtime gap aware sixth follow-up/prune balance/time-slice/trade-quality review"
        f"(런타임 공백 반영 6차 후속/가지치기 잔액/시간구간/거래품질 검토) `{status}`. "
        f"Effect(효과): run267DZ(267DZ 실행)의 candidate_profile_rows(후보-프로필 행) `{len(result['candidate_profile_review'])}`와 negative_slices(음수 구간) `{len(result['negative_slices'])}`를 만들었고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(workspace, status=status, next_action=next_action)
    review_base.write_md(WORKSPACE_STATE_PATH, workspace)


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_rows = list(result["candidate_profile_review"])
    attribution = list(result["performance_attribution_summary"])
    lines = [
        "# Stage267 Run267EA Balance/Time-Slice/Trade-Quality Review(267단계 267EA 잔액/시간구간/거래품질 검토)",
        "",
        f"- status(상태): `{result['status']}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- candidate_profile_rows(후보-프로필 행): `{len(candidate_rows)}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- negative_slices(음수 구간): `{len(result['negative_slices'])}`",
        f"- parser_errors(파서 오류): `{len(result['parser_errors'])}`",
        f"- next_action(다음 행동): `{result['next_action']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267DZ(267DZ 실행)는 9개 모두 KPI(핵심 성과 지표)까지 나왔지만, 검토 결과는 아직 후보 선택이 아니다.",
        "s258_stc는 2023H2에서 강하지만 2025H1/H2로 갈수록 PF(수익 팩터)와 DD(손실폭)가 약해진다. s264_aih는 validation anchor(검증 앵커)는 살아났지만 2026.04 final-month probe(마지막 달 탐침)가 음수다. s264_lc control(대조)도 같은 달 음수라 그 달 자체가 불리한 시장 구간일 수 있다.",
        "",
        "## Candidate Profile(후보 프로필)",
        "",
        "| candidate(후보) | profile(프로필) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | weakest(최약점) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for row in candidate_rows:
        lines.append(
            "| "
            f"`{row.get('candidate_alias')}` | `{row.get('profile_label')}` | "
            f"{row.get('net_profit')} | {row.get('profit_factor')} | {row.get('trade_count')} | "
            f"{row.get('report_equity_drawdown_percent')} | `{row.get('worst_month')}={row.get('worst_month_net')}` | "
            f"`{row.get('profile_read')}` |"
        )
    lines.extend(["", "## Attribution(성과 귀속)", ""])
    for row in attribution:
        lines.append(f"- `{row.get('candidate_alias')}`: {row.get('observed_change')} Next(다음): {row.get('next_probe')}")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 검토는 exploratory review(탐색 검토)이며 후보 선택, 연구 기준선 선택, ONNX(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
            "- 다음 run267EB(267EB 실행)는 같은 repair(수리)를 오래 끌지 말고 s258_stc DD shape(손실폭 형태), s264_aih final-month hole(마지막 달 구멍), q06 filter-stack prune(필터 누적 가지치기)을 분명히 나눠야 한다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간구간 KPI): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            f"- candidate_profile_review(후보 프로필 검토): `{rel(CANDIDATE_PROFILE_REVIEW_PATH)}`",
            f"- negative_slice_summary(음수 구간 요약): `{rel(NEGATIVE_SLICE_PATH)}`",
            f"- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def build_review() -> dict[str, Any]:
    configure_review_base()
    created_at = utc_now()
    payload = normalize_execution_result(review_base.read_json(SOURCE_EXECUTION_RESULT_PATH))
    attempt_outcomes = build_attempt_outcomes(payload)
    trade_rows, parser_errors, parser_checks = review_base.build_trade_records(payload)
    time_rows = review_base.build_time_slice_rows(trade_rows)
    curve_rows = review_base.build_curve_rows(trade_rows, time_rows, payload)
    candidate_rows = build_candidate_profile_review(curve_rows, time_rows, attempt_outcomes, record_attempt_map(payload))
    negative = negative_slices(time_rows)
    attribution = build_attribution_summary(candidate_rows)
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
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "candidate_profile_review": candidate_rows,
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

    review_base.write_csv(TRADE_RECORDS_PATH, trade_rows, columns(trade_rows, ("run_id", "record_view", "net_profit")))
    review_base.write_csv(TIME_SLICE_KPI_PATH, time_rows, columns(time_rows, ("record_view", "axis", "bucket", "net_profit")))
    review_base.write_csv(CURVE_DIAGNOSTICS_PATH, curve_rows, columns(curve_rows, ("record_view", "net_profit", "curve_read")))
    review_base.write_csv(CANDIDATE_PROFILE_REVIEW_PATH, candidate_rows, columns(candidate_rows, ("candidate_alias", "profile_label", "net_profit")))
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
