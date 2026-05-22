from __future__ import annotations

import json
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
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import (
    run267DE_shared_weakness_breakout_second_followup_or_prune_mt5_executor as source_executor,
)
from stage_pipelines.stage267 import run267O_pool_wide_balance_timeslice_trade_quality_review as review_base


STAGE_ID = source_executor.STAGE_ID
SOURCE_RUN_ID = source_executor.RUN_ID
RUN_NUMBER = "run267DF"
RUN_ID = "run267DF_stage267_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review_v1"
STATUS = "run267DF_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review_completed"
PARTIAL_STATUS = "run267DF_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review_partial_parser_errors"
NEXT_ACTION = "run267DG_design_shared_weakness_breakout_second_followup_or_prune_from_run267DF_review"
NEXT_ACTION_PARTIAL = "run267DF_repair_shared_weakness_breakout_second_followup_or_prune_trade_parser_errors"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review"
SOURCE_ROOT = source_executor.RUN_ROOT
SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
SOURCE_KPI_SUMMARY_PATH = source_executor.KPI_SUMMARY_PATH
SOURCE_FORENSICS_PATH = source_executor.FORENSICS_PATH
SOURCE_REPORT_PATH = source_executor.REPORT_PATH

TRADE_RECORDS_PATH = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = RUN_ROOT / "curve_diagnostics.csv"
CANDIDATE_PROFILE_REVIEW_PATH = RUN_ROOT / "candidate_profile_review.csv"
CANDIDATE_SUMMARY_PATH = RUN_ROOT / "candidate_balance_timeslice_summary.csv"
PROFILE_AXIS_SUMMARY_PATH = RUN_ROOT / "profile_axis_summary.csv"
NEGATIVE_SLICE_PATH = RUN_ROOT / "negative_slice_summary.csv"
PARSER_CHECKS_PATH = RUN_ROOT / "parser_checks.csv"
ATTRIBUTION_SUMMARY_PATH = RUN_ROOT / "performance_attribution_summary.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DF_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DF_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review.py")

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
    return review_base.as_float(value, default)


def as_int(value: Any, default: int = 0) -> int:
    return review_base.as_int(value, default)


def columns(rows: Sequence[Mapping[str, Any]], fallback: Sequence[str]) -> tuple[str, ...]:
    if rows:
        return tuple(str(key) for key in rows[0].keys())
    return tuple(fallback)


def configure_review_base() -> None:
    review_base.RUN_ID = RUN_ID
    review_base.SOURCE_RUN_ID = SOURCE_RUN_ID
    review_base.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    review_base.SOURCE_EXECUTION_RESULT_PATH = SOURCE_EXECUTION_RESULT_PATH
    review_base.SOURCE_KPI_SUMMARY_PATH = SOURCE_KPI_SUMMARY_PATH
    review_base.SOURCE_FORENSICS_PATH = SOURCE_FORENSICS_PATH
    review_base.SOURCE_ROOT = SOURCE_ROOT
    review_base.SOURCE_KPI_DELTA_PATH = RUN_ROOT / "not_applicable_kpi_delta_review.csv"
    review_base.TRADE_RECORDS_PATH = TRADE_RECORDS_PATH
    review_base.TIME_SLICE_KPI_PATH = TIME_SLICE_KPI_PATH
    review_base.CURVE_DIAGNOSTICS_PATH = CURVE_DIAGNOSTICS_PATH
    review_base.CANDIDATE_TEST_REVIEW_PATH = CANDIDATE_PROFILE_REVIEW_PATH
    review_base.CANDIDATE_SUMMARY_PATH = CANDIDATE_SUMMARY_PATH
    review_base.TEST_AXIS_SUMMARY_PATH = PROFILE_AXIS_SUMMARY_PATH
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
    review_base.review_read = review_read
    review_base.candidate_read = candidate_read


def normalize_execution_result(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    attempts = []
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

    records = []
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


def curve_read(item: Mapping[str, Any], report_metrics: Mapping[str, Any], month_rows: Sequence[Mapping[str, Any]]) -> str:
    equity_dd = as_float(report_metrics.get("equity_drawdown_maximal_percent") or item.get("closed_balance_max_drawdown_percent"))
    pf = as_float(item.get("profit_factor"))
    net = as_float(item.get("net_profit"))
    trades = as_int(item.get("trade_count"))
    negative_months = [row for row in month_rows if as_float(row.get("net_profit")) < 0.0]
    worst_month_net = min((as_float(row.get("net_profit")) for row in month_rows), default=0.0)
    positive_month_ratio = (len(month_rows) - len(negative_months)) / len(month_rows) if month_rows else 0.0
    if net <= 0.0 or pf <= 1.0 or trades < 180:
        return "fragile_or_thin_no_selection(취약 또는 표본 얇음, 선택 아님)"
    if equity_dd >= 26.0 or worst_month_net <= -240.0:
        return "profit_with_deep_dd_or_month_hole(수익은 있으나 손실폭 또는 월별 구멍 깊음)"
    if equity_dd >= 20.0 or worst_month_net <= -170.0:
        return "profit_with_curve_risk_watch(수익은 있으나 곡선 위험 관찰)"
    if trades >= 350 and net >= 1600.0 and pf >= 1.45 and equity_dd <= 16.0 and positive_month_ratio >= 0.65:
        return "strong_curve_clue_not_selection(강한 곡선 단서, 선택 아님)"
    if trades >= 300 and net >= 1200.0 and pf >= 1.35 and equity_dd <= 19.0:
        return "constructive_curve_watch_not_selection(건설적 곡선 관찰, 선택 아님)"
    if trades < 300 and pf >= 1.45:
        return "high_pf_but_supply_thin_no_selection(높은 수익 팩터지만 공급 얇음, 선택 아님)"
    return "mixed_or_needs_more_pressure(혼합 또는 추가 압박 필요)"


def review_read(curve: Mapping[str, Any], base: Mapping[str, Any], weak_month: Mapping[str, Any]) -> str:
    net = as_float(curve.get("net_profit"))
    pf = as_float(curve.get("profit_factor"))
    equity_dd = as_float(curve.get("report_equity_drawdown_percent"))
    trade_count = as_int(curve.get("trade_count"))
    weak_month_net = as_float(weak_month.get("net_profit"))
    base_net = as_float(base.get("net_profit"))
    base_dd = as_float(base.get("max_drawdown_percent"))

    if net <= 0.0 or pf < 1.05 or trade_count < 180:
        return "failure_memory_or_supply_weak(실패 기억 또는 거래 공급 약함)"
    if equity_dd >= 26.0 or weak_month_net <= -240.0:
        return "profit_but_dd_or_month_hole_uncomfortable(수익은 있으나 손실폭 또는 월별 구멍 불편)"
    if net > base_net and equity_dd <= max(base_dd + 3.0, 18.0) and pf >= 1.45 and trade_count >= 350:
        return "constructive_stability_clue_no_selection(건설적 안정 단서, 선택 아님)"
    if net >= 1700.0 and pf >= 1.40 and trade_count >= 350 and equity_dd < 18.0:
        return "high_profit_needs_curve_zoom_no_selection(고수익, 곡선 확대 검토 필요, 선택 아님)"
    if net > 1000.0 and pf >= 1.30 and trade_count >= 300:
        return "mixed_constructive_needs_followup(혼합 건설적, 후속 필요)"
    return "insufficient_curve_evidence_no_selection(곡선 근거 부족, 선택 아님)"


def candidate_read(rows: Sequence[Mapping[str, Any]]) -> str:
    if not rows:
        return "missing_candidate_rows(후보 행 누락)"
    failures = [
        row
        for row in rows
        if str(row.get("review_read")).startswith("failure")
        or as_float(row.get("net_profit")) <= 0.0
        or as_float(row.get("profit_factor")) <= 1.0
    ]
    uncomfortable = [
        row
        for row in rows
        if "uncomfortable" in str(row.get("review_read"))
        or as_float(row.get("report_equity_drawdown_percent")) >= 26.0
        or as_float(row.get("worst_month_net")) <= -240.0
    ]
    thin = [row for row in rows if "supply_thin" in str(row.get("curve_read")) or as_int(row.get("trade_count")) < 300]
    constructive = [
        row
        for row in rows
        if str(row.get("review_read")).startswith("constructive")
        or str(row.get("review_read")).startswith("high_profit")
        or str(row.get("review_read")).startswith("mixed_constructive")
    ]
    avg_dd = mean(as_float(row.get("report_equity_drawdown_percent")) for row in rows)
    worst_month_floor = min(as_float(row.get("worst_month_net")) for row in rows)
    if failures:
        return "failure_memory_or_prune_no_selection(실패 기억 또는 가지치기, 선택 아님)"
    if uncomfortable:
        return "profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)"
    if thin and not uncomfortable:
        return "constructive_but_supply_thin_no_selection(건설적이나 거래 공급 얇음, 선택 아님)"
    if len(constructive) == len(rows) and avg_dd <= 19.0 and worst_month_floor > -170.0:
        return "broad_constructive_watch_no_selection(넓은 건설적 관찰, 선택 아님)"
    if constructive:
        return "narrow_or_mixed_clue_needs_more_pressure(좁거나 혼합 단서, 추가 압박 필요)"
    return "mixed_or_fragile_no_selection(혼합 또는 취약, 선택 아님)"


def add_candidate_risk_counts(
    summary_rows: Sequence[Mapping[str, Any]],
    candidate_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in candidate_rows:
        grouped.setdefault(str(row.get("candidate_alias")), []).append(row)
    output: list[dict[str, Any]] = []
    for row in summary_rows:
        next_row = dict(row)
        items = grouped.get(str(row.get("candidate_alias")), [])
        next_row["risk_row_count"] = sum(
            1
            for item in items
            if "uncomfortable" in str(item.get("review_read"))
            or str(item.get("review_read")).startswith("failure")
            or as_float(item.get("net_profit")) <= 0.0
            or as_float(item.get("profit_factor")) <= 1.0
            or as_float(item.get("report_equity_drawdown_percent")) >= 26.0
            or as_float(item.get("worst_month_net")) <= -240.0
        )
        next_row["thin_supply_row_count"] = sum(1 for item in items if as_int(item.get("trade_count")) < 300)
        next_row["constructive_row_count"] = sum(
            1
            for item in items
            if str(item.get("review_read")).startswith("constructive")
            or str(item.get("review_read")).startswith("high_profit")
            or str(item.get("review_read")).startswith("mixed_constructive")
        )
        output.append(next_row)
    return output


def build_profile_axis_summary(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("test_id")), []).append(row)
    output: list[dict[str, Any]] = []
    for profile, items in sorted(grouped.items()):
        output.append(
            {
                "test_id": profile,
                "row_count": len(items),
                "candidate_aliases": ";".join(sorted({str(row.get("candidate_alias")) for row in items})),
                "avg_net_profit": mean(as_float(row.get("net_profit")) for row in items),
                "avg_profit_factor": mean(as_float(row.get("profit_factor")) for row in items),
                "avg_trade_count": mean(as_float(row.get("trade_count")) for row in items),
                "avg_equity_dd_percent": mean(as_float(row.get("report_equity_drawdown_percent")) for row in items),
                "worst_month_floor": min(as_float(row.get("worst_month_net")) for row in items),
                "thin_supply_rows": sum(1 for row in items if as_int(row.get("trade_count")) < 300),
                "risk_rows": sum(
                    1
                    for row in items
                    if "uncomfortable" in str(row.get("review_read"))
                    or str(row.get("review_read")).startswith("failure")
                    or as_float(row.get("net_profit")) <= 0.0
                    or as_float(row.get("profit_factor")) <= 1.0
                    or as_float(row.get("report_equity_drawdown_percent")) >= 26.0
                    or as_float(row.get("worst_month_net")) <= -240.0
                ),
                "profile_read": profile_read(items),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def profile_read(items: Sequence[Mapping[str, Any]]) -> str:
    if not items:
        return "missing_profile_rows(프로필 행 누락)"
    failure_rows = sum(
        1
        for row in items
        if str(row.get("review_read")).startswith("failure")
        or as_float(row.get("net_profit")) <= 0.0
        or as_float(row.get("profit_factor")) <= 1.0
    )
    risk_rows = sum(
        1
        for row in items
        if "uncomfortable" in str(row.get("review_read"))
        or str(row.get("review_read")).startswith("failure")
        or as_float(row.get("net_profit")) <= 0.0
        or as_float(row.get("profit_factor")) <= 1.0
        or as_float(row.get("report_equity_drawdown_percent")) >= 26.0
        or as_float(row.get("worst_month_net")) <= -240.0
    )
    thin_rows = sum(1 for row in items if as_int(row.get("trade_count")) < 300)
    if failure_rows:
        return "profile_failure_memory_or_prune(프로필 실패 기억 또는 가지치기)"
    if risk_rows:
        return "profile_profitable_but_risk_rows_present(프로필 수익성은 있으나 위험 행 있음)"
    if thin_rows:
        return "profile_constructive_but_supply_thin(프로필 건설적이나 거래 공급 얇음)"
    return "profile_constructive_watch_no_selection(프로필 건설적 관찰, 선택 아님)"


def result_status(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return PARTIAL_STATUS if parser_errors else STATUS


def result_next_action(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return NEXT_ACTION_PARTIAL if parser_errors else NEXT_ACTION


def build_attribution_summary(
    candidate_rows: Sequence[Mapping[str, Any]],
    candidate_summary: Sequence[Mapping[str, Any]],
    negative_slices: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    negative_by_candidate: dict[str, list[Mapping[str, Any]]] = {}
    for row in negative_slices:
        negative_by_candidate.setdefault(str(row.get("candidate_alias")), []).append(row)
    summary_by_candidate = {str(row.get("candidate_alias")): row for row in candidate_summary}
    output: list[dict[str, Any]] = []
    for row in candidate_rows:
        alias = str(row.get("candidate_alias"))
        negatives = negative_by_candidate.get(alias, [])
        weakest = min(negatives, key=lambda item: as_float(item.get("net_profit")), default={})
        summary = summary_by_candidate.get(alias, {})
        output.append(
            {
                "candidate_alias": alias,
                "test_id": row.get("test_id"),
                "observed_change": f"net={row.get('net_profit')};pf={row.get('profit_factor')};trades={row.get('trade_count')};dd={row.get('report_equity_drawdown_percent')}",
                "likely_drivers": "run267DE(267DE 실행)는 run267DD(267DD 실행)의 cross-period stress(기간 교차 압박), similar replacement(유사 대체), feature neutralization ablation(피처 중립화 제거), weekday DD control(요일 손실폭 대조), destructive prune(파괴적 가지치기) 축을 MT5(MetaTrader 5, 메타트레이더5) report(보고서)와 KPI(핵심 성과 지표)로 연결했다.",
                "weakest_slice": f"{weakest.get('axis', '')}:{weakest.get('bucket', '')}:{weakest.get('net_profit', '')}",
                "candidate_read": summary.get("candidate_read", ""),
                "next_probe": next_probe_for_row(row, weakest),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def next_probe_for_row(row: Mapping[str, Any], weakest: Mapping[str, Any]) -> str:
    profile = str(row.get("test_id"))
    net = as_float(row.get("net_profit"))
    pf = as_float(row.get("profit_factor"))
    trades = as_int(row.get("trade_count"))
    dd = as_float(row.get("report_equity_drawdown_percent"))
    weakest_net = as_float(weakest.get("net_profit"))
    if "december_destructive_prune" in profile and (net <= 0.0 or pf <= 1.0 or trades < 80):
        return "s264_aih_destructive_prune_failed_prune_or_rebuild_supply(s264_aih 파괴적 가지치기 실패, 가지치기 또는 공급 구조 재작성)"
    if "s258_session_cross_period_stress" in profile and (dd >= 14.0 or weakest_net <= -170.0):
        return "s258_cross_period_stress_needs_curve_zoom_or_short_repair(s258 기간 교차 압박 곡선 확대 또는 짧은 수리 필요)"
    if "similar_replacement_watch" in profile and net > 0.0 and pf >= 1.30:
        return "s264_aia_replacement_survived_enter_survivor_gate_no_selection(s264_aia 유사 대체 생존, 생존 게이트 진입 가능, 선택 아님)"
    if "ablation_neutralized_watch" in profile and net > 0.0 and pf >= 1.35:
        return "s264_aia_ablation_survived_check_feature_dependency_no_selection(s264_aia 제거 생존, 피처 의존성 점검, 선택 아님)"
    if "weekday_dd_control" in profile and dd >= 20.0:
        return "control_weekday_dd_uncomfortable_needs_weekday_month_zoom(대조 후보 요일 손실폭 불편, 요일/월 확대 검토 필요)"
    if dd >= 20.0 or weakest_net <= -170.0:
        return "inspect_balance_curve_and_weak_slice_before_followup(후속 전 곡선과 약점 구간 확대 검토)"
    return "candidate_profile_can_enter_followup_design_no_selection(후속 설계 진입 가능, 선택 아님)"


def build_result_judgment(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267DF shared weakness second follow-up/prune balance/time-slice/trade-quality review(267DF 공유 약점 2차 후속/가지치기 잔액/시간구간/거래품질 검토)",
            "evidence_available": "trade records(거래 기록), time-slice KPI(시간구간 핵심 성과 지표), curve diagnostics(곡선 진단), negative slices(음수 구간)",
            "evidence_missing": "survivor ablation/replacement gate(생존 후보 제거/대체 게이트), full Adapter package(전체 어댑터 패키지), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성)",
            "judgment_label": "review_completed_no_candidate_selection",
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
    profile_rows = list(result["profile_axis_summary"])
    negative = list(result["negative_slices"])
    lines = [
        "# Stage267 Run267DF Shared Weakness Second Follow-up/Prune Review(267단계 267DF 공유 약점 후속/가지치기 검토)",
        "",
        f"- status(상태): `{result['status']}`",
        f"- trade records(거래 기록): `{result['trade_record_count']}`",
        f"- time-slice rows(시간구간 행): `{result['time_slice_row_count']}`",
        f"- candidate-profile rows(후보-프로필 행): `{len(candidate_rows)}`",
        f"- negative slices(음수 구간): `{len(negative)}`",
        f"- next_action(다음 행동): `{result['next_action']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Candidate/Profile Read(후보/프로필 판독)",
        "",
        "| candidate(후보) | profile(프로필) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | worst_month(최악 월) | worst_month_net(최악 월 순익) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---|---:|---|",
    ]
    for row in candidate_rows:
        lines.append(
            "| "
            f"`{row.get('candidate_alias', '')}` | `{row.get('test_id', '')}` | "
            f"{round(as_float(row.get('net_profit')), 2)} | {round(as_float(row.get('profit_factor')), 4)} | "
            f"{as_int(row.get('trade_count'))} | {round(as_float(row.get('report_equity_drawdown_percent')), 2)} | "
            f"`{row.get('worst_month', '')}` | {round(as_float(row.get('worst_month_net')), 2)} | "
            f"`{row.get('review_read', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Profile Axis Read(프로필 축 판독)",
            "",
            "| profile(프로필) | rows(행) | avg_net(평균 순익) | avg_PF(평균 수익 팩터) | avg_trades(평균 거래 수) | avg_DD%(평균 손실폭 %) | profile_read(프로필 판독) |",
            "|---|---:|---:|---:|---:|---:|---|",
        ]
    )
    for row in profile_rows:
        lines.append(
            "| "
            f"`{row.get('test_id', '')}` | {row.get('row_count', '')} | "
            f"{round(as_float(row.get('avg_net_profit')), 2)} | {round(as_float(row.get('avg_profit_factor')), 4)} | "
            f"{round(as_float(row.get('avg_trade_count')), 1)} | {round(as_float(row.get('avg_equity_dd_percent')), 2)} | "
            f"`{row.get('profile_read', '')}` |"
        )
    worst_negative = sorted(negative, key=lambda row: as_float(row.get("net_profit")))[:8]
    lines.extend(
        [
            "",
            "## Weak Slice Watch(약점 구간 관찰)",
            "",
            "| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | net_profit(순익) | trades(거래 수) |",
            "|---|---|---|---|---:|---:|",
        ]
    )
    for row in worst_negative:
        lines.append(
            "| "
            f"`{row.get('candidate_alias', '')}` | `{row.get('test_id', '')}` | `{row.get('axis', '')}` | "
            f"`{row.get('bucket', '')}` | {round(as_float(row.get('net_profit')), 2)} | {as_int(row.get('trade_count'))} |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "Run267DF(267DF 실행)는 후보 선택이나 ONNX readiness(ONNX 준비) 선언이 아니다. 이 검토는 다음 run267DG(267DG 실행)의 second follow-up/prune design(2차 후속/가지치기 설계)을 만들기 위한 근거다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간구간 핵심 성과 지표): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            f"- candidate_profile_review(후보 프로필 검토): `{rel(CANDIDATE_PROFILE_REVIEW_PATH)}`",
            f"- negative_slice_summary(음수 구간 요약): `{rel(NEGATIVE_SLICE_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267DF_producer", "producer_script", PRODUCER_PATH, "Builds run267DF balance/time-slice/trade-quality review."),
        ("stage267_run267DF_trade_records", "trade_records", TRADE_RECORDS_PATH, "Parsed trade records."),
        ("stage267_run267DF_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Time-slice KPI."),
        ("stage267_run267DF_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Curve diagnostics."),
        ("stage267_run267DF_candidate_profile_review", "candidate_profile_review", CANDIDATE_PROFILE_REVIEW_PATH, "Candidate-profile review."),
        ("stage267_run267DF_candidate_summary", "candidate_summary", CANDIDATE_SUMMARY_PATH, "Candidate summary."),
        ("stage267_run267DF_profile_axis_summary", "profile_axis_summary", PROFILE_AXIS_SUMMARY_PATH, "Profile axis summary."),
        ("stage267_run267DF_negative_slice", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Negative slice summary."),
        ("stage267_run267DF_attribution", "performance_attribution_summary", ATTRIBUTION_SUMMARY_PATH, "Performance attribution."),
        ("stage267_run267DF_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DF_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Parser checks."),
        ("stage267_run267DF_review_result", "review_result", REVIEW_RESULT_PATH, "Review result payload."),
        ("stage267_run267DF_report", "review_report", REPORT_PATH, "User-facing review report."),
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
        f"negative_slices={len(result['negative_slices'])};"
        f"trade_records={result['trade_record_count']};next_action={result['next_action']}."
    )
    stage_row = {
        "row_id": "stage267_run267DF_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review",
        "tier_scope": "Tier A and duplicate Tier A+B boundary review; true fallback not claimed",
        "scoreboard": "trade_curve_time_slice_trade_quality",
        "status": status,
        "judgment": "review_completed_no_candidate_selection",
        "evidence_boundary": "mt5_trade_list_curve_time_slice_review_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review",
        "status": status,
        "judgment": "review_completed_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review",
        "tier_scope": "Tier A and duplicate Tier A+B boundary",
        "kpi_scope": "trade_curve_time_slice_trade_quality",
        "scoreboard_lane": "shared_weakness_followup_review",
        "status": status,
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


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def update_current_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    report_line = (
        "- run267DF_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review"
        f"(267DF 공유 약점 후속/가지치기 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    )
    latest_line = (
        f"- latest_review(최신 검토): run267DF(267DF 실행) candidate_profile_rows(후보-프로필 행) "
        f"`{len(result['candidate_profile_review'])}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    block = "\n".join(
        [
            "Run267DF(267DF 실행)는 run267DE(267DE 실행)의 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.",
            f"Effect(효과): candidate_profile_rows(후보-프로필 행) `{len(result['candidate_profile_review'])}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`를 만들었고, 다음은 second follow-up/prune design(2차 후속/가지치기 설계)이다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(
        current,
        "- adapter_under_review(검토 중 어댑터):",
        "- adapter_under_review(검토 중 어댑터): `shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review`",
    )
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    current = append_after_contains(current, "stage267_run267DE_shared_weakness_breakout_second_followup_or_prune_mt5_execution.md", report_line)
    current = append_after_contains(current, "## Current Next Action", latest_line)
    current = append_block_once(current, "Run267DF(267DF 실행)는 run267DE", block)
    review_base.write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selection = append_after_contains(selection, "run267DE_shared_weakness_breakout_second_followup_or_prune_mt5_execution", report_line)
    selection = append_block_once(selection, "Run267DF(267DF 실행)는 run267DE", block)
    review_base.write_md(SELECTION_STATUS_PATH, selection)

    review_index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_index = replace_line_prefix(review_index, "- status(상태):", f"- status(상태): `{status}`")
    review_index = replace_line_prefix(review_index, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(
        review_index,
        "- last_completed_run(마지막 완료 실행):",
        f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`",
    )
    review_index = append_after_contains(review_index, "run267DE_shared_weakness_breakout_second_followup_or_prune_mt5_execution", report_line)
    review_index = append_block_once(review_index, "Run267DF(267DF 실행)는 run267DE", block)
    review_base.write_md(REVIEW_INDEX_PATH, review_index)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_executor.COMPLETED_STATUS}", f"  status: {status}", 1)
    workspace = workspace.replace(f"  current_run_id: {SOURCE_RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {SOURCE_RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  next_action: {source_executor.NEXT_COMPLETED}", f"  next_action: {next_action}", 1)
    workspace = append_after_contains(
        workspace,
        "run267DE_shared_weakness_breakout_second_followup_or_prune_mt5_execution_report_path",
        f"  run267DF_shared_weakness_breakout_second_followup_or_prune_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}",
    )
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267DF(267DF 실행) shared weakness breakout second follow-up/prune balance/time-slice/trade-quality review"
        f"(공유 약점 돌파 후속/가지치기 잔액/시간구간/거래품질 검토) `{status}`. "
        f"Effect(효과): run267DE(267DE 실행)의 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 거래 목록과 약한 구간으로 다시 읽었고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if f"`{status}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_line, 1)
    review_base.write_md(WORKSPACE_STATE_PATH, workspace)


def build_review() -> dict[str, Any]:
    configure_review_base()
    if not path_exists(SOURCE_EXECUTION_RESULT_PATH):
        raise FileNotFoundError(SOURCE_EXECUTION_RESULT_PATH)
    created_at = utc_now()
    execution_result = normalize_execution_result(review_base.read_json(SOURCE_EXECUTION_RESULT_PATH))
    trade_rows, parser_errors, parser_checks = review_base.build_trade_records(execution_result)
    time_rows = review_base.build_time_slice_rows(trade_rows)
    curve_rows = review_base.build_curve_rows(trade_rows, time_rows, execution_result)
    candidate_rows = review_base.build_candidate_test_review(curve_rows, time_rows)
    candidate_summary = add_candidate_risk_counts(review_base.build_candidate_summary(candidate_rows), candidate_rows)
    profile_axis_summary = build_profile_axis_summary(candidate_rows)
    negative = review_base.negative_slices(time_rows)
    attribution = build_attribution_summary(candidate_rows, candidate_summary, negative)
    result = {
        "status": result_status(parser_errors),
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "candidate_profile_review": candidate_rows,
        "candidate_summary": candidate_summary,
        "profile_axis_summary": profile_axis_summary,
        "negative_slices": negative,
        "performance_attribution_summary": attribution,
        "parser_errors": parser_errors,
        "parser_checks": parser_checks,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": result_next_action(parser_errors),
        "outputs": {
            "trade_records": rel(TRADE_RECORDS_PATH),
            "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
            "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
            "candidate_profile_review": rel(CANDIDATE_PROFILE_REVIEW_PATH),
            "candidate_summary": rel(CANDIDATE_SUMMARY_PATH),
            "profile_axis_summary": rel(PROFILE_AXIS_SUMMARY_PATH),
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
    review_base.write_csv(CANDIDATE_PROFILE_REVIEW_PATH, candidate_rows, columns(candidate_rows, ("candidate_alias", "test_id", "net_profit")))
    review_base.write_csv(CANDIDATE_SUMMARY_PATH, candidate_summary, columns(candidate_summary, ("candidate_alias", "avg_net_profit", "candidate_read")))
    review_base.write_csv(PROFILE_AXIS_SUMMARY_PATH, profile_axis_summary, columns(profile_axis_summary, ("test_id", "avg_net_profit")))
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
                "trade_records": result["trade_record_count"],
                "time_slice_rows": result["time_slice_row_count"],
                "curve_rows": result["curve_row_count"],
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
