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
    run267DM_shared_weakness_breakout_third_followup_or_prune_mt5_executor as source_executor,
)
from stage_pipelines.stage267 import run267DN_remaining_runtime_retry as retry_executor
from stage_pipelines.stage267 import run267O_pool_wide_balance_timeslice_trade_quality_review as review_base


STAGE_ID = source_executor.STAGE_ID
SOURCE_RUN_ID = source_executor.RUN_ID
RETRY_RUN_ID = retry_executor.RUN_ID
RUN_NUMBER = "run267DO"
RUN_ID = "run267DO_stage267_shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps_v1"
STATUS = "run267DO_shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps_completed"
PARTIAL_STATUS = "run267DO_shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps_partial_parser_errors"
NEXT_ACTION = "run267DP_design_runtime_gap_aware_fourth_followup_or_prune_from_run267DO_review"
NEXT_ACTION_PARTIAL = "run267DO_repair_trade_report_parser_before_runtime_gap_review"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps"
SOURCE_ROOT = source_executor.RUN_ROOT
RETRY_ROOT = retry_executor.RUN_ROOT
SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
RETRY_EXECUTION_RESULT_PATH = retry_executor.EXECUTION_RESULT_PATH
SOURCE_REPORT_PATH = source_executor.REPORT_PATH
RETRY_REPORT_PATH = retry_executor.REPORT_PATH
SOURCE_KPI_SUMMARY_PATH = source_executor.KPI_SUMMARY_PATH
SOURCE_FORENSICS_PATH = source_executor.FORENSICS_PATH

TRADE_RECORDS_PATH = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = RUN_ROOT / "curve_diagnostics.csv"
CANDIDATE_PROFILE_REVIEW_PATH = RUN_ROOT / "candidate_profile_review.csv"
CANDIDATE_RUNTIME_GAP_SUMMARY_PATH = RUN_ROOT / "candidate_runtime_gap_summary.csv"
ATTEMPT_OUTCOME_REVIEW_PATH = RUN_ROOT / "attempt_outcome_review.csv"
NEGATIVE_SLICE_PATH = RUN_ROOT / "negative_slice_summary.csv"
PARSER_CHECKS_PATH = RUN_ROOT / "parser_checks.csv"
ATTRIBUTION_SUMMARY_PATH = RUN_ROOT / "performance_attribution_summary.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DO_shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DO_runtime_gap_aware_balance_timeslice_trade_quality_review.py")

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


def normalize_execution_result(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    attempts: list[dict[str, Any]] = []
    for attempt in normalized.get("attempts_executed", []):
        next_attempt = dict(attempt)
        profile = str(next_attempt.get("profile_label") or next_attempt.get("variant_id") or "unknown_profile")
        next_attempt["queue_id"] = next_attempt.get("queue_id") or next_attempt.get("variant_id")
        next_attempt["test_id"] = profile
        next_attempt["test_type"] = profile
        next_attempt["materialization_boundary"] = (
            next_attempt.get("tier_pair_boundary")
            or next_attempt.get("materialization_boundary")
            or "Tier_A_and_duplicate_boundary_only"
        )
        attempts.append(next_attempt)
    normalized["attempts_executed"] = attempts

    records: list[dict[str, Any]] = []
    for record in normalized.get("mt5_kpi_records", []):
        next_record = dict(record)
        route_role = str(next_record.get("route_role") or "")
        if route_role == "routed_total_duplicate_boundary":
            next_record["route_role"] = "routed_total"
        elif route_role == "tier_only_total":
            next_record["route_role"] = "tier_a_only"
        records.append(next_record)
    normalized["mt5_kpi_records"] = records
    return normalized


def report_by_attempt(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in payload.get("strategy_tester_reports", [])}


def execution_by_attempt(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in payload.get("execution_results", [])}


def attempt_by_name(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in payload.get("attempts_executed", [])}


def report_metrics(row: Mapping[str, Any]) -> Mapping[str, Any]:
    return row.get("metrics", {}) if isinstance(row.get("metrics"), Mapping) else {}


def runtime_status(row: Mapping[str, Any]) -> tuple[str, str]:
    runtime = row.get("runtime_outputs", {}) if isinstance(row.get("runtime_outputs"), Mapping) else {}
    return str(runtime.get("status") or row.get("status") or ""), str(runtime.get("wait_status") or "")


def attempt_read(dm_exec: Mapping[str, Any], dm_report: Mapping[str, Any], dn_exec: Mapping[str, Any], dn_report: Mapping[str, Any]) -> str:
    dm_runtime, _ = runtime_status(dm_exec)
    dm_trades = as_int(report_metrics(dm_report).get("trade_count"))
    dn_trades = as_int(report_metrics(dn_report).get("trade_count"))
    if dm_runtime == "completed" and dm_trades > 0:
        return "usable_runtime_trade_evidence(사용 가능한 런타임 거래 근거)"
    if dn_exec and dm_trades == 0 and dn_trades == 0:
        return "retry_confirmed_zero_trade_runtime_gap_no_blind_retry(재시도 확인 무거래/런타임 공백, 맹목 재시도 금지)"
    if dm_trades == 0:
        return "zero_trade_report_runtime_gap_no_candidate_evidence(무거래 보고/런타임 공백, 후보 근거 없음)"
    return "mixed_report_runtime_gap_needs_boundary(혼합 보고/런타임 공백, 경계 필요)"


def build_attempt_outcomes(dm_payload: Mapping[str, Any], dn_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    dm_attempts = attempt_by_name(dm_payload)
    dm_reports = report_by_attempt(dm_payload)
    dm_execs = execution_by_attempt(dm_payload)
    dn_reports = report_by_attempt(dn_payload)
    dn_execs = execution_by_attempt(dn_payload)
    output: list[dict[str, Any]] = []
    for attempt_name, attempt in sorted(dm_attempts.items()):
        dm_exec = dm_execs.get(attempt_name, {})
        dn_exec = dn_execs.get(attempt_name, {})
        dm_report = dm_reports.get(attempt_name, {})
        dn_report = dn_reports.get(attempt_name, {})
        dm_runtime, dm_wait = runtime_status(dm_exec)
        dn_runtime, dn_wait = runtime_status(dn_exec)
        dm_metrics = report_metrics(dm_report)
        dn_metrics = report_metrics(dn_report)
        output.append(
            {
                "attempt_name": attempt_name,
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "profile_label": attempt.get("profile_label"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "dm_status": dm_exec.get("status", ""),
                "dm_runtime_status": dm_runtime,
                "dm_runtime_wait_status": dm_wait,
                "dm_report_trade_count": dm_metrics.get("trade_count", ""),
                "dm_report_net_profit": dm_metrics.get("net_profit", ""),
                "dm_report_profit_factor": dm_metrics.get("profit_factor", ""),
                "dm_report_equity_dd_percent": dm_metrics.get("equity_drawdown_maximal_percent", ""),
                "dm_report_path": rel(dm_report.get("html_report", {}).get("path", "")) if dm_report.get("html_report") else "",
                "dn_retry_present": "true" if attempt_name in dn_execs else "false",
                "dn_status": dn_exec.get("status", ""),
                "dn_runtime_status": dn_runtime,
                "dn_runtime_wait_status": dn_wait,
                "dn_report_trade_count": dn_metrics.get("trade_count", ""),
                "dn_report_net_profit": dn_metrics.get("net_profit", ""),
                "dn_report_profit_factor": dn_metrics.get("profit_factor", ""),
                "dn_report_equity_dd_percent": dn_metrics.get("equity_drawdown_maximal_percent", ""),
                "dn_report_path": rel(dn_report.get("html_report", {}).get("path", "")) if dn_report.get("html_report") else "",
                "attempt_read": attempt_read(dm_exec, dm_report, dn_exec, dn_report),
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
            "attempt_role": attempt.get("attempt_role") or record.get("route_role"),
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
        return "profit_with_uncomfortable_dd_or_month_hole(수익은 있으나 손실폭/월별 구멍 불편)"
    if trades < 300 and pf >= 1.45 and equity_dd <= 16.0:
        return "constructive_but_supply_thin_no_selection(건설적이나 공급 얇음, 선택 아님)"
    if net >= 1000.0 and pf >= 1.35 and trades >= 300 and equity_dd <= 20.0 and positive_month_ratio >= 0.60:
        return "constructive_curve_watch_no_selection(건설적 곡선 관찰, 선택 아님)"
    if net > 0.0 and pf >= 1.10:
        return "positive_but_quality_decay_watch(양수이나 품질 저하 관찰)"
    return "mixed_or_insufficient_no_selection(혼합 또는 근거 부족, 선택 아님)"


def weakest_bucket(time_rows: Sequence[Mapping[str, Any]], record_view: str, axis: str) -> Mapping[str, Any]:
    rows = [
        row
        for row in time_rows
        if row.get("record_view") == record_view and row.get("axis") == axis and as_int(row.get("trade_count")) >= 3
    ]
    return min(rows, key=lambda row: as_float(row.get("net_profit")), default={})


def profile_read(curve: Mapping[str, Any], attempt: Mapping[str, Any], weak_month: Mapping[str, Any]) -> str:
    net = as_float(curve.get("net_profit"))
    pf = as_float(curve.get("profit_factor"))
    trades = as_int(curve.get("trade_count"))
    dd = as_float(curve.get("report_equity_drawdown_percent"))
    worst_month_net = as_float(weak_month.get("net_profit"))
    label = str(curve.get("curve_read"))
    if "uncomfortable" in label or dd >= 24.0 or worst_month_net <= -220.0:
        return "profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)"
    if trades < 300:
        return "constructive_but_trade_supply_thin_no_selection(건설적이나 거래 공급 얇음, 선택 아님)"
    if net >= 1000.0 and pf >= 1.35:
        return "constructive_control_or_followup_clue_no_selection(건설적 대조/후속 단서, 선택 아님)"
    if net > 0.0 and pf > 1.0:
        return "positive_but_weak_quality_or_decay_no_selection(양수이나 품질 약화/감쇠, 선택 아님)"
    return "insufficient_profile_evidence_no_selection(프로필 근거 부족, 선택 아님)"


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
                "attempt_role": record_link.get("attempt_role", ""),
                "runtime_status": outcome.get("dm_runtime_status", ""),
                "runtime_wait_status": outcome.get("dm_runtime_wait_status", ""),
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
                "profile_read": profile_read(row, outcome, weak_month),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(output, key=lambda item: (-as_float(item.get("net_profit")), str(item.get("candidate_alias"))))


def gap_read(items: Sequence[Mapping[str, Any]], completed: Sequence[Mapping[str, Any]]) -> str:
    blocked = [row for row in items if "runtime_gap" in str(row.get("attempt_read")) or "zero_trade" in str(row.get("attempt_read"))]
    retry_confirmed = [row for row in items if str(row.get("dn_retry_present")) == "true"]
    avg_net = mean(as_float(row.get("net_profit")) for row in completed) if completed else 0.0
    worst_dd = max((as_float(row.get("report_equity_drawdown_percent")) for row in completed), default=0.0)
    if blocked and not completed:
        return "runtime_gap_and_zero_trade_dominant_prune_or_rebuild(런타임 공백과 무거래 우세, 가지치기 또는 재구축)"
    if blocked and retry_confirmed and completed:
        return "mixed_completed_companion_but_retry_gap_blocks_selection(완료 동반 행은 있으나 재시도 공백이 선택 차단)"
    if completed and worst_dd >= 24.0:
        return "completed_runtime_but_curve_dd_uncomfortable(런타임 완료이나 곡선 손실폭 불편)"
    if completed and avg_net > 0.0:
        return "completed_runtime_constructive_watch_no_selection(런타임 완료 건설적 관찰, 선택 아님)"
    return "insufficient_runtime_curve_evidence_no_selection(런타임/곡선 근거 부족, 선택 아님)"


def build_candidate_runtime_gap_summary(
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
                "runtime_completed_attempts": sum(1 for row in attempts if row.get("dm_runtime_status") == "completed"),
                "runtime_blocked_attempts": sum(1 for row in attempts if row.get("dm_runtime_status") == "blocked"),
                "retry_attempts": sum(1 for row in attempts if row.get("dn_retry_present") == "true"),
                "retry_recovered_attempts": sum(1 for row in attempts if row.get("dn_runtime_status") == "completed"),
                "zero_trade_report_attempts": sum(1 for row in attempts if as_int(row.get("dm_report_trade_count")) == 0),
                "completed_profile_rows": len(completed),
                "avg_completed_net_profit": mean(as_float(row.get("net_profit")) for row in completed) if completed else "",
                "avg_completed_profit_factor": mean(as_float(row.get("profit_factor")) for row in completed) if completed else "",
                "max_completed_dd_percent": max((as_float(row.get("report_equity_drawdown_percent")) for row in completed), default=""),
                "worst_completed_month_net": min((as_float(row.get("worst_month_net")) for row in completed), default=""),
                "gap_read": gap_read(attempts, completed),
                "next_probe": next_probe_for_candidate(alias, attempts, completed),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def next_probe_for_candidate(alias: str, attempts: Sequence[Mapping[str, Any]], completed: Sequence[Mapping[str, Any]]) -> str:
    if alias == "s258_stc":
        return "compare_supply_sidefilter_signal_shape_before_more_threshold_release(s258 공급 사이드필터 신호 형태 비교 후 threshold_release 추가 여부 결정)"
    if alias == "s264_lc":
        return "use_as_defensive_control_only_with_dd_zoom(s264_lc는 손실폭 확대 검토 포함 방어 대조로만 사용)"
    if alias == "s264_aia":
        return "prune_current_similarity_ablation_runtime_gap_or_rebuild_feature_surface(s264_aia 현 유사/제거 런타임 공백 가지치기 또는 피처 표면 재구축)"
    if alias == "s262_lih":
        return "prune_current_guardrail_crosscheck_until_signal_supply_repaired(s262_lih 현 guardrail crosscheck는 신호 공급 수리 전 가지치기)"
    return "review_before_followup_no_selection(후속 전 검토, 선택 아님)"


def build_attribution_summary(candidate_summary: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in candidate_summary:
        alias = str(row.get("candidate_alias"))
        output.append(
            {
                "candidate_alias": alias,
                "observed_change": (
                    f"attempts={row.get('attempt_count')};completed={row.get('runtime_completed_attempts')};"
                    f"blocked={row.get('runtime_blocked_attempts')};zero_trade={row.get('zero_trade_report_attempts')};"
                    f"avg_net={row.get('avg_completed_net_profit')}"
                ),
                "comparison_baseline": "run267DM runtime output(런타임 출력) plus run267DN retry(재시도)",
                "likely_drivers": likely_driver(alias),
                "segment_checks": "month/weekday/session/hour/chron_segment(월/요일/세션/시간/시간순 구간) from completed runtime rows; runtime gap rows tracked separately",
                "trade_shape": (
                    f"completed_profile_rows={row.get('completed_profile_rows')};"
                    f"avg_pf={row.get('avg_completed_profit_factor')};max_dd={row.get('max_completed_dd_percent')}"
                ),
                "alternative_explanations": "zero-trade Strategy Tester report(무거래 전략 테스터 보고서), runtime handoff timeout(런타임 인계 시간 초과), overly tight gate(과도하게 좁은 관문)",
                "attribution_confidence": "medium" if as_int(row.get("completed_profile_rows")) else "low",
                "next_probe": row.get("next_probe"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def likely_driver(alias: str) -> str:
    if alias == "s258_stc":
        return "threshold_release(임계값 해제)는 무거래였고 sidefilter_open(사이드필터 개방)은 거래를 만들었으나 2025 구간에서 품질이 감쇠했다."
    if alias == "s264_lc":
        return "one_stage_dd_demote(1단계 손실폭 강등)는 거래와 수익을 만들었지만 손실폭이 방어 대조로도 불편하다."
    if alias == "s264_aia":
        return "similar/ablation survivor(유사/제거 생존) 경로가 2024에서 무거래와 런타임 공백으로 멈췄다."
    if alias == "s262_lih":
        return "validation guardrail crosscheck(검증 가드레일 교차확인)가 2024에서 신호 공급을 만들지 못했다."
    return "mixed runtime and report evidence(혼합 런타임/보고 근거)"


def result_status(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return PARTIAL_STATUS if parser_errors else STATUS


def result_next_action(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return NEXT_ACTION_PARTIAL if parser_errors else NEXT_ACTION


def build_result_judgment(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267DO runtime-gap-aware balance/time-slice/trade-quality review(267DO 런타임 공백 포함 잔액/시간구간/거래품질 검토)",
            "evidence_available": "run267DM Strategy Tester reports(전략 테스터 보고서), run267DM runtime outputs(런타임 출력) where completed, run267DN retry reports(재시도 보고서), trade records(거래 기록), time-slice KPI(시간구간 핵심 성과 지표), runtime gap summary(런타임 공백 요약)",
            "evidence_missing": "recovered runtime CSV for 9 blocked attempts(9개 차단 시도 런타임 CSV 회복), Adapter package(어댑터 패키지), runtime reproduction closure(런타임 재현 폐쇄), ONNX parity(ONNX 동등성)",
            "judgment_label": "review_completed_with_runtime_gaps_no_candidate_selection",
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
    gap_rows = list(result["candidate_runtime_gap_summary"])
    attempt_rows = list(result["attempt_outcome_review"])
    negative = sorted(result["negative_slices"], key=lambda row: as_float(row.get("net_profit")))[:10]
    lines = [
        "# Stage267 Run267DO Runtime-Gap-Aware Review(267단계 267DO 런타임 공백 포함 검토)",
        "",
        f"- status(상태): `{result['status']}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- retry_run(재시도 실행): `{RETRY_RUN_ID}`",
        f"- attempts_reviewed(검토 시도): `{len(attempt_rows)}`",
        f"- runtime_completed_attempts(런타임 완료 시도): `{sum(1 for row in attempt_rows if row.get('dm_runtime_status') == 'completed')}`",
        f"- runtime_gap_attempts(런타임 공백 시도): `{sum(1 for row in attempt_rows if row.get('dm_runtime_status') == 'blocked')}`",
        f"- recovered_retry_kpi_records(재시도 회복 KPI 기록): `{result['retry_recovered_kpi_records']}`",
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
        "run267DO(267DO 실행)는 run267DM(267DM 실행)의 completed runtime(완료 런타임) 5개를 곡선/시간구간/거래품질로 읽고, run267DN(267DN 실행)의 retry(재시도) 9개가 모두 runtime gap(런타임 공백)과 zero-trade report(무거래 보고)로 끝난 점을 같이 기록했다.",
        "효과: 같은 attempt(시도)를 계속 재시도하는 병목을 끊고, 어떤 후보가 거래 공급을 만들었는지와 어떤 후보가 런타임/무거래 공백으로 막혔는지를 다음 설계 입력으로 분리한다.",
        "",
        "## Candidate Runtime Gap Summary(후보 런타임 공백 요약)",
        "",
        "| candidate(후보) | attempts(시도) | completed(완료) | blocked(차단) | retry(재시도) | zero_trade(무거래) | avg_net(평균 순수익) | max_DD%(최대 손실폭 %) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in gap_rows:
        lines.append(
            "| "
            f"`{row.get('candidate_alias')}` | {row.get('attempt_count')} | {row.get('runtime_completed_attempts')} | "
            f"{row.get('runtime_blocked_attempts')} | {row.get('retry_attempts')} | {row.get('zero_trade_report_attempts')} | "
            f"{round(as_float(row.get('avg_completed_net_profit')), 2) if row.get('avg_completed_net_profit') != '' else ''} | "
            f"{round(as_float(row.get('max_completed_dd_percent')), 2) if row.get('max_completed_dd_percent') != '' else ''} | "
            f"`{row.get('gap_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Completed Runtime Profiles(완료 런타임 프로필)",
            "",
            "| candidate(후보) | profile(프로필) | split(구간) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst_month(최악 월) | read(판독) |",
            "|---|---|---|---:|---:|---:|---:|---|---|",
        ]
    )
    for row in candidate_rows:
        lines.append(
            "| "
            f"`{row.get('candidate_alias')}` | `{row.get('profile_label')}` | `{row.get('split')}` | "
            f"{round(as_float(row.get('net_profit')), 2)} | {round(as_float(row.get('profit_factor')), 4)} | "
            f"{as_int(row.get('trade_count'))} | {round(as_float(row.get('report_equity_drawdown_percent')), 2)} | "
            f"`{row.get('worst_month')}` | `{row.get('profile_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Weak Slice Watch(약점 구간 관찰)",
            "",
            "| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | net_profit(순수익) | trades(거래 수) |",
            "|---|---|---|---|---:|---:|",
        ]
    )
    for row in negative:
        lines.append(
            "| "
            f"`{row.get('candidate_alias')}` | `{row.get('test_id')}` | `{row.get('axis')}` | "
            f"`{row.get('bucket')}` | {round(as_float(row.get('net_profit')), 2)} | {as_int(row.get('trade_count'))} |"
        )
    lines.extend(
        [
            "",
            "## Runtime Gap Boundary(런타임 공백 경계)",
            "",
            "- run267DN(267DN 실행) retry(재시도)는 recovered KPI records(회복 KPI 기록) `0`개다.",
            "- s264_aia(264 AIA 후보) similar/ablation(유사/제거), s262_lih(262 LIH 후보) guardrail(가드레일), s258_stc(258 STC 후보) threshold_release(임계값 해제)는 현 상태에서 zero-trade report(무거래 보고)와 runtime gap(런타임 공백)이 같이 남았다.",
            "- s258_stc(258 STC 후보) sidefilter_open(사이드필터 개방)은 거래 공급을 만들었지만 2025 구간에서 PF(수익 팩터)와 DD(drawdown, 손실폭)가 약해졌다.",
            "- s264_lc(264 LC 후보)는 수익과 거래 수가 있으나 DD(drawdown, 손실폭)가 방어 대조로도 불편하다.",
            "",
            "## Boundary(경계)",
            "",
            "Run267DO(267DO 실행)는 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 선언하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간구간 핵심 성과 지표): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            f"- candidate_profile_review(후보 프로필 검토): `{rel(CANDIDATE_PROFILE_REVIEW_PATH)}`",
            f"- candidate_runtime_gap_summary(후보 런타임 공백 요약): `{rel(CANDIDATE_RUNTIME_GAP_SUMMARY_PATH)}`",
            f"- attempt_outcome_review(시도 결과 검토): `{rel(ATTEMPT_OUTCOME_REVIEW_PATH)}`",
            f"- performance_attribution_summary(성과 귀속 요약): `{rel(ATTRIBUTION_SUMMARY_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267DO_producer", "producer_script", PRODUCER_PATH, "Builds run267DO runtime-gap-aware review."),
        ("stage267_run267DO_source_dm_execution_result", "source_execution_result", SOURCE_EXECUTION_RESULT_PATH, "Source run267DM execution result."),
        ("stage267_run267DO_source_dn_execution_result", "source_retry_execution_result", RETRY_EXECUTION_RESULT_PATH, "Source run267DN retry execution result."),
        ("stage267_run267DO_trade_records", "trade_records", TRADE_RECORDS_PATH, "Parsed completed runtime trade records."),
        ("stage267_run267DO_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Time-slice KPI for completed runtime rows."),
        ("stage267_run267DO_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Curve diagnostics for completed runtime rows."),
        ("stage267_run267DO_candidate_profile_review", "candidate_profile_review", CANDIDATE_PROFILE_REVIEW_PATH, "Candidate-profile completed runtime review."),
        ("stage267_run267DO_candidate_runtime_gap_summary", "candidate_runtime_gap_summary", CANDIDATE_RUNTIME_GAP_SUMMARY_PATH, "Candidate runtime gap summary."),
        ("stage267_run267DO_attempt_outcome_review", "attempt_outcome_review", ATTEMPT_OUTCOME_REVIEW_PATH, "Attempt-level runtime/report outcome review."),
        ("stage267_run267DO_negative_slice", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Weak negative time slices."),
        ("stage267_run267DO_attribution", "performance_attribution_summary", ATTRIBUTION_SUMMARY_PATH, "Performance attribution with runtime gaps."),
        ("stage267_run267DO_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DO_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Parser checks."),
        ("stage267_run267DO_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267DO_report", "review_report", REPORT_PATH, "User-facing review report."),
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
        f"runtime_gap_attempts={result['runtime_gap_attempts']};"
        f"negative_slices={len(result['negative_slices'])};"
        f"next_action={result['next_action']}."
    )
    stage_row = {
        "row_id": "stage267_run267DO_runtime_gap_aware_balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps",
        "tier_scope": "run267DM completed runtime rows plus run267DN retry gap rows; true fallback not claimed",
        "scoreboard": "trade_curve_time_slice_trade_quality_runtime_gap",
        "status": status,
        "judgment": "review_completed_with_runtime_gaps_no_candidate_selection",
        "evidence_boundary": "mt5_trade_list_curve_time_slice_runtime_gap_review_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "shared_weakness_runtime_gap_aware_balance_timeslice_trade_quality_review",
        "status": status,
        "judgment": "review_completed_with_runtime_gaps_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_balance_timeslice_trade_quality_review",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps",
        "tier_scope": "Tier A and duplicate Tier A+B rows with runtime gap boundary",
        "kpi_scope": "trade_curve_time_slice_trade_quality_runtime_gap",
        "scoreboard_lane": "shared_weakness_runtime_gap_review",
        "status": status,
        "judgment": "review_completed_with_runtime_gaps_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "primary_kpi": f"candidate_profile_rows={len(result['candidate_profile_review'])};runtime_gap_attempts={result['runtime_gap_attempts']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "completed",
        "notes": f"Next action: {result['next_action']}. Runtime gaps remain evidence boundary, not a retry loop.",
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
    report_entry = f"  run267DO_runtime_gap_aware_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}"
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
        "- run267DO_runtime_gap_aware_balance_timeslice_trade_quality_review"
        f"(267DO 런타임 공백 포함 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    )
    latest_line = (
        f"- latest_review(최신 검토): run267DO(267DO 실행) candidate_profile_rows(후보-프로필 행) "
        f"`{len(result['candidate_profile_review'])}`, runtime_gap_attempts(런타임 공백 시도) "
        f"`{result['runtime_gap_attempts']}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    block = "\n".join(
        [
            "Run267DO(267DO 실행)는 run267DM/run267DN(267DM/267DN 실행)을 함께 읽어 completed runtime(완료 런타임) 행은 곡선/시간구간/거래품질로, blocked retry(차단 재시도) 행은 runtime gap(런타임 공백)으로 분리했다.",
            f"Effect(효과): candidate_profile_rows(후보-프로필 행) `{len(result['candidate_profile_review'])}`, runtime_gap_attempts(런타임 공백 시도) `{result['runtime_gap_attempts']}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`를 만들었고, 다음은 runtime gap aware fourth follow-up/prune design(런타임 공백 반영 4차 후속/가지치기 설계)이다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(
        current,
        "- adapter_under_review(검토 중 어댑터):",
        "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_third_followup_or_prune_balance_timeslice_trade_quality_with_runtime_gaps`",
    )
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    current = append_after_contains(current, "stage267_run267DN_shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry.md", report_line)
    current = append_after_contains(current, "## Current Next Action", latest_line)
    current = append_block_once(current, "Run267DO(267DO 실행)는 run267DM/run267DN", block)
    review_base.write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selection = append_after_contains(selection, "stage267_run267DN_shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry", report_line)
    selection = append_block_once(selection, "Run267DO(267DO 실행)는 run267DM/run267DN", block)
    review_base.write_md(SELECTION_STATUS_PATH, selection)

    review_index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_index = replace_line_prefix(review_index, "- status(상태):", f"- status(상태): `{status}`")
    review_index = replace_line_prefix(review_index, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(
        review_index,
        "- last_completed_run(마지막 완료 실행):",
        f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`",
    )
    review_index = append_after_contains(review_index, "stage267_run267DN_shared_weakness_breakout_third_followup_or_prune_remaining_runtime_retry.md", report_line)
    review_index = append_block_once(review_index, "Run267DO(267DO 실행)는 run267DM/run267DN", block)
    review_base.write_md(REVIEW_INDEX_PATH, review_index)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = update_stage267_workspace_block(workspace, status=status, next_action=next_action)
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267DO(267DO 실행) runtime-gap-aware balance/time-slice/trade-quality review"
        f"(런타임 공백 포함 잔액/시간구간/거래품질 검토) `{status}`. "
        f"Effect(효과): run267DM/run267DN(267DM/267DN 실행)의 completed runtime(완료 런타임)과 runtime gap(런타임 공백)을 분리했고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if f"`{status}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_line, 1)
    review_base.write_md(WORKSPACE_STATE_PATH, workspace)


def build_review() -> dict[str, Any]:
    configure_review_base()
    created_at = utc_now()
    dm_payload = normalize_execution_result(review_base.read_json(SOURCE_EXECUTION_RESULT_PATH))
    dn_payload = review_base.read_json(RETRY_EXECUTION_RESULT_PATH)
    attempt_outcomes = build_attempt_outcomes(dm_payload, dn_payload)
    trade_rows, parser_errors, parser_checks = review_base.build_trade_records(dm_payload)
    time_rows = review_base.build_time_slice_rows(trade_rows)
    curve_rows = review_base.build_curve_rows(trade_rows, time_rows, dm_payload)
    candidate_rows = build_candidate_profile_review(curve_rows, time_rows, attempt_outcomes, record_attempt_map(dm_payload))
    candidate_gap_summary = build_candidate_runtime_gap_summary(attempt_outcomes, candidate_rows)
    negative = review_base.negative_slices(time_rows)
    attribution = build_attribution_summary(candidate_gap_summary)
    status = result_status(parser_errors)
    next_action = result_next_action(parser_errors)
    result = {
        "status": status,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "retry_run_id": RETRY_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_outcome_review": attempt_outcomes,
        "runtime_gap_attempts": sum(1 for row in attempt_outcomes if row.get("dm_runtime_status") == "blocked"),
        "retry_recovered_kpi_records": len(dn_payload.get("mt5_kpi_records", [])),
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "candidate_profile_review": candidate_rows,
        "candidate_runtime_gap_summary": candidate_gap_summary,
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
            "candidate_runtime_gap_summary": rel(CANDIDATE_RUNTIME_GAP_SUMMARY_PATH),
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
    review_base.write_csv(CANDIDATE_RUNTIME_GAP_SUMMARY_PATH, candidate_gap_summary, columns(candidate_gap_summary, ("candidate_alias", "gap_read")))
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
                "runtime_gap_attempts": result["runtime_gap_attempts"],
                "retry_recovered_kpi_records": result["retry_recovered_kpi_records"],
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
