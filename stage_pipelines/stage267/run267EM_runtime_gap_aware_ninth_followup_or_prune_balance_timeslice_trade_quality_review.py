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
from stage_pipelines.stage267 import run267EL_runtime_gap_aware_ninth_followup_or_prune_mt5_executor as source_executor
from stage_pipelines.stage267 import run267O_pool_wide_balance_timeslice_trade_quality_review as review_base


STAGE_ID = source_executor.STAGE_ID
SOURCE_RUN_ID = source_executor.RUN_ID
RUN_NUMBER = "run267EM"
RUN_ID = "run267EM_stage267_runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review_v1"
STATUS = "run267EM_runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review_completed_with_init_failures"
PARTIAL_STATUS = "run267EM_runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review_partial_parser_errors"
NEXT_ACTION = "run267EN_design_runtime_gap_aware_tenth_followup_or_prune_from_run267EM_review"
NEXT_ACTION_PARTIAL = "run267EM_repair_trade_report_parser_before_tenth_followup_design"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review"
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
INIT_FAILURE_SUMMARY_PATH = RUN_ROOT / "init_failure_summary.csv"
NEGATIVE_SLICE_PATH = RUN_ROOT / "negative_slice_summary.csv"
ATTRIBUTION_SUMMARY_PATH = RUN_ROOT / "performance_attribution_summary.csv"
FOLLOWUP_DECISION_QUEUE_PATH = RUN_ROOT / "followup_decision_queue.csv"
PARSER_CHECKS_PATH = RUN_ROOT / "parser_checks.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267EM_runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267EM_runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review.py")

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
            or "Tier A and duplicate-boundary only(Tier A 및 중복 경계만)"
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
        return "profit_with_uncomfortable_dd_or_month_hole(수익은 있으나 손실폭 또는 월 구멍 불편)"
    if trades < 80 and pf >= 1.10:
        return "thin_final_month_probe_no_selection(얇은 마지막 월 탐침, 선택 아님)"
    if trades >= 250 and net >= 900.0 and pf >= 1.45 and equity_dd <= 16.0 and positive_month_ratio >= 0.50:
        return "constructive_cross_period_watch_no_selection(건설적 기간 관찰, 선택 아님)"
    if net > 0.0 and pf > 1.05:
        return "positive_but_needs_slice_review_no_selection(양수지만 구간 검토 필요, 선택 아님)"
    return "mixed_or_fragile_no_selection(혼합 또는 취약, 선택 아님)"


def attempt_read(exec_row: Mapping[str, Any], report_row: Mapping[str, Any]) -> str:
    runtime, _, deinit_reason = runtime_status(exec_row)
    trades = as_int(report_metrics(report_row).get("trade_count"))
    if runtime == "completed" and trades > 0:
        return "usable_runtime_trade_evidence(사용 가능한 런타임 거래 근거)"
    if runtime == "blocked" and str(report_row.get("status")) == "completed":
        return "runtime_output_gap_blocks_candidate_evidence(런타임 출력 공백으로 후보 근거 차단)"
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
        report = record.get("report", {})
        attempt_name = str(report.get("attempt_name") or "") if isinstance(report, Mapping) else ""
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
        return "breaks_on_measured_slice_no_selection(측정 구간에서 깨짐, 선택 아님)"
    if trades < 30:
        return "thin_final_month_negative_context_no_selection(얇은 마지막 월 문맥, 선택 아님)"
    if "uncomfortable" in label or dd >= 22.0 or worst_month_net <= -160.0:
        return "positive_but_curve_risk_no_selection(양수지만 곡선 위험, 선택 아님)"
    if pf < 1.30:
        return "positive_low_pf_watch_no_selection(양수지만 PF 낮음, 선택 아님)"
    return "constructive_watch_but_not_baseline_selection(건설적 관찰이나 기준 후보 선택 아님)"


def metric_signature(row: Mapping[str, Any]) -> str:
    keys = ("net_profit", "profit_factor", "trade_count", "report_equity_drawdown_percent")
    return "|".join(str(row.get(key, "")) for key in keys)


def duplicate_signature_map(curve_rows: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for row in curve_rows:
        counts[metric_signature(row)] += 1
    return counts


def build_candidate_profile_review(
    curve_rows: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
    attempt_outcomes: Sequence[Mapping[str, Any]],
    record_links: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    outcome_by_attempt = {str(row.get("attempt_name")): row for row in attempt_outcomes}
    signature_counts = duplicate_signature_map(curve_rows)
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
        signature = metric_signature(row)
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
                "metric_signature": signature,
                "duplicate_signature_count": signature_counts[signature],
                "curve_read": row.get("curve_read"),
                "profile_read": profile_read(row, weak_month),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 90) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in time_rows
        if as_int(row.get("trade_count")) >= 3 and as_float(row.get("net_profit")) < 0.0
    ]
    rows.sort(key=lambda row: (as_float(row.get("net_profit")), -as_int(row.get("trade_count"))))
    return rows[:limit]


def build_init_failure_summary(attempt_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    blocked = [row for row in attempt_rows if str(row.get("runtime_status")) != "completed"]
    grouped: dict[tuple[str, str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for row in blocked:
        grouped[(str(row.get("candidate_alias")), str(row.get("queue_id")), str(row.get("attempt_role")))].append(row)
    output: list[dict[str, Any]] = []
    for (alias, queue_id, role), rows in sorted(grouped.items()):
        output.append(
            {
                "candidate_alias": alias,
                "queue_id": queue_id,
                "attempt_role": role,
                "blocked_attempts": len(rows),
                "attempt_names": ";".join(str(row.get("attempt_name")) for row in rows),
                "report_statuses": ";".join(sorted({str(row.get("report_status")) for row in rows})),
                "read": "runtime_output_gap_or_init_failure_requires_bounded_handoff_triage(런타임 출력 공백 또는 초기화 실패라 제한된 인계 진단 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_attribution_summary(
    candidate_rows: Sequence[Mapping[str, Any]],
    attempt_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    aliases = ("s258_stc", "s264_aih", "s264_lc", "s262_lih", "s264_aia")
    output: list[dict[str, Any]] = []
    rows_by_alias = group_by(candidate_rows, "candidate_alias")
    attempts_by_alias = group_by(attempt_rows, "candidate_alias")
    for alias in aliases:
        rows = rows_by_alias.get(alias, [])
        attempts = attempts_by_alias.get(alias, [])
        blocked = [row for row in attempts if str(row.get("runtime_status")) != "completed"]
        completed = [row for row in attempts if str(row.get("runtime_status")) == "completed"]
        total_net = sum(as_float(row.get("net_profit")) for row in rows)
        worst_dd = max((as_float(row.get("report_equity_drawdown_percent")) for row in rows), default=0.0)
        weakest = min(rows, key=lambda row: as_float(row.get("net_profit")), default={})
        best = max(rows, key=lambda row: as_float(row.get("net_profit")), default={})
        duplicate_rows = [row for row in rows if as_int(row.get("duplicate_signature_count")) > 1]
        if alias == "s258_stc":
            observed = "all_s258_runtime_outputs_blocked(모든 s258 런타임 출력 차단)"
            next_probe = "bounded_handoff_triage_before_any_performance_judgment(성능 판단 전 제한된 인계 진단)"
        elif alias == "s264_aih":
            observed = "validation_positive_but_202604_negative_and_aggressive_handoff_blocked(검증 양수지만 2026.04 음수이고 공격형 인계 차단)"
            next_probe = "separate_final_month_structure_from_runtime_handoff_gap(마지막 월 구조와 런타임 인계 공백 분리)"
        elif alias == "s264_lc":
            observed = "defensive_control_also_negative_on_202604(방어 대조도 2026.04에서 음수)"
            next_probe = "use_as_market_control_not_selection_candidate(시장 대조로만 사용, 선택 후보 아님)"
        elif alias == "s262_lih":
            observed = "validation_identity_positive_but_202604_pressure_negative(검증 정체성은 양수지만 2026.04 압박은 음수)"
            next_probe = "keep_validation_heavy_watch_but_test_identity_collapse(검증 중심 관찰 유지, 정체성 붕괴 검사)"
        else:
            observed = "oos_anchor_identity_duplicates_s262_and_202604_pressure_negative(표본외 앵커가 s262와 중복되고 2026.04 압박 음수)"
            next_probe = "do_not_treat_oos_anchor_as_distinct_until_signature_separates(서명이 분리되기 전 독립 후보로 보지 않음)"
        output.append(
            {
                "candidate_alias": alias,
                "completed_attempts": len(completed),
                "blocked_attempts": len(blocked),
                "profile_rows": len(rows),
                "total_net_profit": total_net,
                "worst_equity_dd_percent": worst_dd,
                "best_profile": best.get("profile_label", ""),
                "best_net_profit": best.get("net_profit", ""),
                "weakest_profile": weakest.get("profile_label", ""),
                "weakest_net_profit": weakest.get("net_profit", ""),
                "duplicate_signature_rows": len(duplicate_rows),
                "observed_change": observed,
                "next_probe": next_probe,
                "selection_boundary": "no_selected_candidate_no_selected_research_baseline_no_onnx",
            }
        )
    return output


def build_followup_decision_queue(
    attribution_rows: Sequence[Mapping[str, Any]],
    init_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "q01_runtime_handoff_gap_bounded_triage",
            "priority": "P0",
            "candidate_aliases": "s258_stc;s264_aih",
            "evidence": f"blocked_groups={len(init_rows)}",
            "decision_use": "repair_or_prune_runtime_handoff_gap_before_performance_claim(성능 주장 전 런타임 인계 공백 수리 또는 가지치기)",
            "stop_condition": "maximum_two_stage_repair_loop(최대 2단계 수리 루프)",
            "effect": "s258과 공격형 s264_aih를 숫자 실패로 오해하지 않고 런타임 실패로 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q02_202604_shared_sell_fragility_pivot",
            "priority": "P0",
            "candidate_aliases": "s264_aih;s264_lc;s262_lih;s264_aia",
            "evidence": f"negative_slices={len(negative_rows)}",
            "decision_use": "pivot_to_structure_or_feature_engineering_not_more_same_month_filtering(같은 월 필터 반복이 아니라 구조/피처 엔지니어링으로 전환)",
            "stop_condition": "no_calendar_only_filter_stack(달력 필터만 쌓기 금지)",
            "effect": "2026.04가 공통으로 약한 시장 구간인지, 후보 구조 문제인지 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q03_s262_s264_aia_signature_collapse_audit",
            "priority": "P1",
            "candidate_aliases": "s262_lih;s264_aia",
            "evidence": "validation_identity_rows_show_identical_kpi_signature(검증 정체성 행에서 동일 KPI 서명 확인)",
            "decision_use": "audit_feature_order_model_identity_before_distinct_candidate_claim(독립 후보 주장 전 피처 순서/모델 정체성 감사)",
            "stop_condition": "do_not_select_duplicate_signature_candidate(중복 서명 후보 선택 금지)",
            "effect": "두 후보가 실제로 다른 표면인지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q04_validation_positive_low_pf_watch",
            "priority": "P1",
            "candidate_aliases": "s264_aih;s262_lih;s264_aia",
            "evidence": "validation_rows_positive_but_pf_about_1_21(검증 행은 양수지만 PF 약 1.21)",
            "decision_use": "keep_as_watch_not_baseline_selection(관찰로 유지하되 기준 후보 선택 아님)",
            "stop_condition": "require_curve_and_slice_review_before_any_adapter_escalation(어댑터 확대 전 곡선/구간 검토 필요)",
            "effect": "양수 숫자만 보고 ONNX(온엑스) 방향으로 건너뛰는 것을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q05_aggressive_experiment_after_handoff_fix",
            "priority": "P2_aggressive",
            "candidate_aliases": "s258_stc;s264_aih",
            "evidence": "aggressive_rows_blocked_before_performance_read(공격형 행이 성능 판독 전 차단됨)",
            "decision_use": "after_handoff_fix_run_one_aggressive_non_filter_experiment(인계 수리 뒤 필터가 아닌 공격형 실험 1회)",
            "stop_condition": "do_not_repeat_defensive_filter_stack(방어 필터 반복 금지)",
            "effect": "연구가 방어 필터만 쌓는 방향으로 굳지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def result_status(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return PARTIAL_STATUS if parser_errors else STATUS


def result_next_action(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return NEXT_ACTION_PARTIAL if parser_errors else NEXT_ACTION


def build_result_judgment(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267EM balance/time-slice/trade-quality review(267EM 잔액/시간구간/거래품질 검토)",
            "evidence_available": "trade_records(거래 기록), time_slice_kpi(시간구간 KPI), curve_diagnostics(곡선 진단), candidate_profile_review(후보 프로필 검토), init_failure_summary(초기화 실패 요약), negative_slice_summary(음수 구간 요약)",
            "evidence_missing": "visual curve inspection(시각 곡선 검토), next materialization(다음 물질화), Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성)",
            "judgment_label": "exploratory_review_completed_with_init_failures_no_selection",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": result["next_action"],
            "user_explanation_hook": "이번 검토는 후보 선택이 아니라 실행 결과와 실패를 다음 설계 재료로 바꾼 작업이다.",
        }
    ]


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267EM_producer", "producer_script", PRODUCER_PATH, "Builds run267EM balance/time-slice/trade-quality review."),
        ("stage267_run267EM_source_execution", "source_execution_result", SOURCE_EXECUTION_RESULT_PATH, "Source run267EL execution result."),
        ("stage267_run267EM_trade_records", "trade_records", TRADE_RECORDS_PATH, "Parsed trade records."),
        ("stage267_run267EM_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Time-slice KPI."),
        ("stage267_run267EM_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Curve diagnostics."),
        ("stage267_run267EM_candidate_profile_review", "candidate_profile_review", CANDIDATE_PROFILE_REVIEW_PATH, "Candidate profile review."),
        ("stage267_run267EM_attempt_outcome_review", "attempt_outcome_review", ATTEMPT_OUTCOME_REVIEW_PATH, "Attempt outcome review."),
        ("stage267_run267EM_init_failure_summary", "init_failure_summary", INIT_FAILURE_SUMMARY_PATH, "Init/runtime output gap summary."),
        ("stage267_run267EM_negative_slices", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Negative slice summary."),
        ("stage267_run267EM_attribution_summary", "performance_attribution_summary", ATTRIBUTION_SUMMARY_PATH, "Performance attribution summary."),
        ("stage267_run267EM_followup_queue", "followup_decision_queue", FOLLOWUP_DECISION_QUEUE_PATH, "Follow-up decision queue."),
        ("stage267_run267EM_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267EM_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267EM_report", "review_report", REPORT_PATH, "User-facing review report."),
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
        f"init_failure_groups={len(result['init_failure_summary'])};"
        f"negative_slices={len(result['negative_slices'])};"
        f"next_action={result['next_action']}."
    )
    stage_row = {
        "row_id": "stage267_run267EM_runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review",
        "tier_scope": "Tier A completed rows; init/runtime gaps separated; true fallback not claimed",
        "scoreboard": "trade_curve_time_slice_trade_quality_with_init_failures",
        "status": result["status"],
        "judgment": "review_completed_with_init_failures_no_candidate_selection",
        "evidence_boundary": "mt5_trade_list_curve_time_slice_review_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review",
        "status": result["status"],
        "judgment": "review_completed_with_init_failures_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "balance_timeslice_trade_quality_review",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review",
        "tier_scope": "Tier A completed rows; init/runtime gaps separated",
        "kpi_scope": "trade_curve_time_slice_trade_quality",
        "scoreboard_lane": "runtime_gap_aware_ninth_followup_or_prune_review",
        "status": result["status"],
        "judgment": "review_completed_with_init_failures_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "primary_kpi": f"candidate_profile_rows={len(result['candidate_profile_review'])};negative_slices={len(result['negative_slices'])};init_failure_groups={len(result['init_failure_summary'])}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "completed_with_init_failures",
        "notes": f"Next action: {result['next_action']}.",
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
    report_entry = f"  run267EM_runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}"
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
        "- run267EM_runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review"
        f"(267EM 런타임 공백 반영 9차 후속/가지치기 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            f"Run267EM(267EM 실행)는 run267EL(267EL 실행)의 {len(result['candidate_profile_review'])}개 KPI(핵심 성과 지표)와 {len(result['init_failure_summary'])}개 init/runtime gap(초기화/런타임 공백)을 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.",
            f"Effect(효과): candidate_profile_rows(후보-프로필 행) `{len(result['candidate_profile_review'])}`, init_failure_groups(초기화 실패 묶음) `{len(result['init_failure_summary'])}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`, followup_queue(후속 대기열) `{len(result['followup_decision_queue'])}`개를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
            text = replace_line_prefix(
                text,
                "- adapter_under_review(검토 중 어댑터):",
                "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_ninth_followup_or_prune_balance_timeslice_trade_quality_review`",
            )
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "stage267_run267EL_runtime_gap_aware_ninth_followup_or_prune_mt5_execution.md", report_line)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "stage267_run267EL_runtime_gap_aware_ninth_followup_or_prune_mt5_execution", report_line)
        else:
            text = replace_line_containing(text, "- status(", f"- status(상태): `{status}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "stage267_run267EL_runtime_gap_aware_ninth_followup_or_prune_mt5_execution.md", report_line)
        text = append_block_once(text, "Run267EM(267EM 실행)는 run267EL", block)
        review_base.write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        "  Stage267(267단계) run267EM(267EM 실행) runtime gap aware ninth follow-up/prune balance/time-slice/trade-quality review"
        f"(런타임 공백 반영 9차 후속/가지치기 잔액/시간구간/거래품질 검토) `{status}`. "
        f"Effect(효과): run267EL(267EL 실행)의 candidate_profile_rows(후보-프로필 행) `{len(result['candidate_profile_review'])}`, "
        f"init_failure_groups(초기화 실패 묶음) `{len(result['init_failure_summary'])}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`를 만들었고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(workspace, status=status, next_action=next_action)
    review_base.write_md(WORKSPACE_STATE_PATH, workspace)


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_rows = list(result["candidate_profile_review"])
    attribution = list(result["performance_attribution_summary"])
    init_rows = list(result["init_failure_summary"])
    queue_rows = list(result["followup_decision_queue"])

    def fmt(value: Any, digits: int = 2) -> str:
        if value in ("", None):
            return ""
        number = as_float(value, default=float("nan"))
        if not math.isfinite(number):
            return str(value)
        return f"{number:.{digits}f}"

    lines = [
        "# Stage267 Run267EM Balance/Time-Slice/Trade-Quality Review(267단계 267EM 잔액/시간구간/거래품질 검토)",
        "",
        f"- status(상태): `{result['status']}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- candidate_profile_rows(후보-프로필 행): `{len(candidate_rows)}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- init_failure_groups(초기화 실패 묶음): `{len(init_rows)}`",
        f"- negative_slices(음수 구간): `{len(result['negative_slices'])}`",
        f"- parser_errors(파서 오류): `{len(result['parser_errors'])}`",
        f"- next_action(다음 행동): `{result['next_action']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        f"run267EL(267EL 실행)는 {len(result.get('attempt_outcome_review', []))}개 시도 중 {len(candidate_rows)}개만 KPI(핵심 성과 지표)까지 갔다. run267EM(267EM 실행)는 그 {len(candidate_rows)}개를 곡선/구간/거래품질로 읽고, 막힌 {len(init_rows)}개는 성능 실패가 아니라 init/runtime gap(초기화/런타임 공백)으로 분리했다.",
        "효과는 후보를 성급히 뽑지 않고 다음 설계에서 무엇을 수리하고, 무엇을 압박하고, 무엇을 중복 후보로 의심해야 하는지 분리하는 것이다.",
        "",
        "## Candidate Profile(후보 프로필)",
        "",
        "| candidate(후보) | profile(프로필) | net(순손익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | weakest(최약) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for row in candidate_rows:
        lines.append(
            "| "
            f"`{row.get('candidate_alias')}` | `{row.get('profile_label')}` | "
            f"{fmt(row.get('net_profit'), 2)} | {fmt(row.get('profit_factor'), 3)} | {fmt(row.get('trade_count'), 0)} | "
            f"{fmt(row.get('report_equity_drawdown_percent'), 2)} | `{row.get('worst_month')}={fmt(row.get('worst_month_net'), 2)}` | "
            f"`{row.get('profile_read')}` |"
        )
    lines.extend(["", "## Init/Runtime Gaps(초기화/런타임 공백)", ""])
    if init_rows:
        for row in init_rows:
            lines.append(
                f"- `{row.get('candidate_alias')}` `{row.get('queue_id')}` `{row.get('attempt_role')}`: "
                f"blocked_attempts(차단 시도) `{row.get('blocked_attempts')}`. {row.get('read')}"
            )
    else:
        lines.append("- init/runtime gap(초기화/런타임 공백): `none`")
    lines.extend(["", "## Attribution(성과 귀인)", ""])
    for row in attribution:
        lines.append(f"- `{row.get('candidate_alias')}`: {row.get('observed_change')} Next(다음): {row.get('next_probe')}")
    lines.extend(["", "## Follow-Up Queue(후속 대기열)", ""])
    for row in queue_rows:
        lines.append(f"- `{row.get('queue_id')}` `{row.get('priority')}` `{row.get('candidate_aliases')}`: {row.get('decision_use')}")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 검토는 exploratory review(탐색 검토)이며 후보 선택, 연구 기준 후보 선택, ONNX(온엑스) 준비, Goal Achieve(목표 달성)를 주장하지 않는다.",
            "- 다음 run267EN(267EN 실행)는 같은 필터를 더 붙이는 작업이 아니라 handoff gap(인계 공백), 2026.04 shared fragility(공유 취약성), duplicate signature(중복 서명), 공격형 실험 재개 조건을 설계해야 한다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간구간 KPI): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            f"- candidate_profile_review(후보 프로필 검토): `{rel(CANDIDATE_PROFILE_REVIEW_PATH)}`",
            f"- init_failure_summary(초기화 실패 요약): `{rel(INIT_FAILURE_SUMMARY_PATH)}`",
            f"- negative_slice_summary(음수 구간 요약): `{rel(NEGATIVE_SLICE_PATH)}`",
            f"- followup_decision_queue(후속 판단 대기열): `{rel(FOLLOWUP_DECISION_QUEUE_PATH)}`",
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
    init_summary = build_init_failure_summary(attempt_outcomes)
    negative = negative_slices(time_rows)
    attribution = build_attribution_summary(candidate_rows, attempt_outcomes)
    followup_queue = build_followup_decision_queue(attribution, init_summary, negative)
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
        "init_failure_summary": init_summary,
        "negative_slices": negative,
        "performance_attribution_summary": attribution,
        "followup_decision_queue": followup_queue,
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
            "init_failure_summary": rel(INIT_FAILURE_SUMMARY_PATH),
            "negative_slice_summary": rel(NEGATIVE_SLICE_PATH),
            "performance_attribution_summary": rel(ATTRIBUTION_SUMMARY_PATH),
            "followup_decision_queue": rel(FOLLOWUP_DECISION_QUEUE_PATH),
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
    review_base.write_csv(INIT_FAILURE_SUMMARY_PATH, init_summary, columns(init_summary, ("candidate_alias", "queue_id", "blocked_attempts")))
    review_base.write_csv(NEGATIVE_SLICE_PATH, negative, columns(negative, ("candidate_alias", "test_id", "axis", "bucket", "net_profit")))
    review_base.write_csv(PARSER_CHECKS_PATH, parser_checks, columns(parser_checks, ("attempt_name", "parser_status")))
    review_base.write_csv(ATTRIBUTION_SUMMARY_PATH, attribution, columns(attribution, ("candidate_alias", "observed_change", "next_probe")))
    review_base.write_csv(FOLLOWUP_DECISION_QUEUE_PATH, followup_queue, columns(followup_queue, ("queue_id", "priority", "candidate_aliases")))
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
                "init_failure_groups": len(result["init_failure_summary"]),
                "negative_slices": len(result["negative_slices"]),
                "followup_queue": len(result["followup_decision_queue"]),
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
