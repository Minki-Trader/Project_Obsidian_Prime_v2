from __future__ import annotations

import copy
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage267 import run267CO_pool_wide_shared_weakness_breakout_mt5_executor as source_executor
from stage_pipelines.stage267 import run267O_pool_wide_balance_timeslice_trade_quality_review as review_base


STAGE_ID = source_executor.STAGE_ID
SOURCE_RUN_ID = source_executor.RUN_ID
RUN_NUMBER = "run267CP"
RUN_ID = "run267CP_stage267_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review_v1"
STATUS = "run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review_completed"
PARTIAL_STATUS = "run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review_partial_parser_errors"
NEXT_ACTION = "run267CQ_design_shared_weakness_breakout_followup_or_prune_from_run267CP_review"
NEXT_ACTION_PARTIAL = "run267CP_repair_shared_weakness_breakout_trade_parser_errors"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review"
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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review.py")

STAGE_LEDGER_PATH = source_executor.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_executor.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_executor.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_executor.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_executor.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_executor.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_executor.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_executor.REVIEW_INDEX_PATH

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


def cell(value: Any) -> Any:
    return review_base.cell(value)


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
    normalized = copy.deepcopy(dict(payload))
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
    if net <= 0.0 or pf <= 1.0 or trades < 100:
        return "fragile_or_thin_no_selection(취약 또는 표본 얇음, 선택 아님)"
    if equity_dd >= 30.0 or worst_month_net <= -260.0:
        return "profit_with_deep_dd_or_month_hole(수익은 있으나 손실폭 또는 월별 구멍 깊음)"
    if equity_dd >= 22.0 or worst_month_net <= -180.0:
        return "profit_with_curve_risk_watch(수익은 있으나 곡선 위험 관찰)"
    if trades >= 250 and net >= 1000.0 and pf >= 1.35 and equity_dd <= 18.5 and positive_month_ratio >= 0.58:
        return "strong_curve_clue_not_selection(강한 곡선 단서, 선택 아님)"
    if trades >= 200 and net >= 500.0 and pf >= 1.25 and equity_dd <= 24.0:
        return "constructive_curve_watch_not_selection(건설적 곡선 관찰, 선택 아님)"
    return "mixed_or_needs_more_pressure(혼합 또는 추가 압박 필요)"


def review_read(curve: Mapping[str, Any], base: Mapping[str, Any], weak_month: Mapping[str, Any]) -> str:
    net = as_float(curve.get("net_profit"))
    pf = as_float(curve.get("profit_factor"))
    equity_dd = as_float(curve.get("report_equity_drawdown_percent"))
    trade_count = as_int(curve.get("trade_count"))
    weak_month_net = as_float(weak_month.get("net_profit"))
    base_net = as_float(base.get("net_profit"))
    base_dd = as_float(base.get("max_drawdown_percent"))

    if net <= 0.0 or pf < 1.05 or trade_count < 120:
        return "failure_memory_or_supply_weak(실패 기억 또는 거래 공급 약함)"
    if equity_dd >= 30.0 or weak_month_net <= -260.0:
        return "profit_but_dd_or_month_hole_uncomfortable(수익은 있으나 손실폭 또는 월별 구멍 불편)"
    if net > base_net and equity_dd <= max(base_dd + 3.0, 18.5) and pf >= 1.45 and trade_count >= 250:
        return "constructive_stability_clue_no_selection(건설적 안정 단서, 선택 아님)"
    if net >= 1500.0 and pf >= 1.45 and trade_count >= 350 and equity_dd < 32.0:
        return "high_profit_but_needs_curve_zoom(고수익이나 곡선 확대 검토 필요)"
    if net > 500.0 and pf >= 1.25 and trade_count >= 200:
        return "mixed_constructive_needs_followup(혼합 건설적, 후속 필요)"
    return "insufficient_curve_evidence_no_selection(곡선 근거 부족, 선택 아님)"


def candidate_read(rows: Sequence[Mapping[str, Any]]) -> str:
    if not rows:
        return "missing_candidate_rows(후보 행 누락)"
    uncomfortable = [
        row
        for row in rows
        if "uncomfortable" in str(row.get("review_read"))
        or as_float(row.get("report_equity_drawdown_percent")) >= 30.0
        or as_float(row.get("worst_month_net")) <= -260.0
    ]
    constructive = [
        row
        for row in rows
        if str(row.get("review_read")).startswith("constructive")
        or str(row.get("review_read")).startswith("high_profit")
        or str(row.get("review_read")).startswith("mixed_constructive")
    ]
    avg_dd = mean(as_float(row.get("report_equity_drawdown_percent")) for row in rows)
    worst_month_floor = min(as_float(row.get("worst_month_net")) for row in rows)
    if uncomfortable:
        return "profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)"
    if len(constructive) == len(rows) and avg_dd <= 22.0 and worst_month_floor > -180.0:
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
            or as_float(item.get("report_equity_drawdown_percent")) >= 30.0
            or as_float(item.get("worst_month_net")) <= -260.0
        )
        next_row["constructive_row_count"] = sum(
            1
            for item in items
            if str(item.get("review_read")).startswith(("constructive", "high_profit", "mixed_constructive"))
        )
        output.append(next_row)
    return output


def build_profile_axis_summary(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("test_id")), []).append(row)
    output: list[dict[str, Any]] = []
    for test_id, items in sorted(grouped.items()):
        best = max(items, key=lambda row: as_float(row.get("net_profit")))
        worst = min(items, key=lambda row: as_float(row.get("net_profit")))
        output.append(
            {
                "test_id": test_id,
                "test_type": best.get("test_type"),
                "row_count": len(items),
                "avg_net_profit": mean(as_float(row.get("net_profit")) for row in items),
                "avg_profit_factor": mean(as_float(row.get("profit_factor")) for row in items),
                "avg_equity_drawdown_percent": mean(as_float(row.get("report_equity_drawdown_percent")) for row in items),
                "avg_trade_count": mean(as_float(row.get("trade_count")) for row in items),
                "worst_month_floor": min(as_float(row.get("worst_month_net")) for row in items),
                "risk_row_count": sum(
                    1
                    for row in items
                    if "uncomfortable" in str(row.get("review_read"))
                    or as_float(row.get("report_equity_drawdown_percent")) >= 30.0
                    or as_float(row.get("worst_month_net")) <= -260.0
                ),
                "constructive_row_count": sum(
                    1
                    for row in items
                    if str(row.get("review_read")).startswith(("constructive", "high_profit", "mixed_constructive"))
                ),
                "best_candidate_alias": best.get("candidate_alias"),
                "best_net_profit": best.get("net_profit"),
                "worst_candidate_alias": worst.get("candidate_alias"),
                "worst_net_profit": worst.get("net_profit"),
            }
        )
    return sorted(output, key=lambda row: -as_float(row.get("avg_net_profit")))


def result_status(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return PARTIAL_STATUS if parser_errors else STATUS


def result_next_action(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return NEXT_ACTION_PARTIAL if parser_errors else NEXT_ACTION


def build_attribution_summary(
    candidate_rows: Sequence[Mapping[str, Any]],
    candidate_summary: Sequence[Mapping[str, Any]],
    negative_slices: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_alias: dict[str, list[Mapping[str, Any]]] = {}
    for row in candidate_rows:
        by_alias.setdefault(str(row.get("candidate_alias")), []).append(row)
    for summary in candidate_summary:
        alias = str(summary.get("candidate_alias"))
        items = by_alias.get(alias, [])
        weak = [row for row in negative_slices if row.get("candidate_alias") == alias][:3]
        best = max(items, key=lambda row: as_float(row.get("net_profit"))) if items else {}
        rows.append(
            {
                "candidate_alias": alias,
                "observed_change": f"avg_net={cell(summary.get('avg_net_profit'))};avg_pf={cell(summary.get('avg_profit_factor'))};avg_dd={cell(summary.get('avg_equity_drawdown_percent'))}",
                "comparison_baseline": "run267CO headline KPI and Stage267 2024 baseline evidence",
                "likely_drivers": f"profile={best.get('test_id', '')};risk_rows={summary.get('risk_row_count', '')};constructive_rows={summary.get('constructive_row_count', '')}",
                "segment_checks": ";".join(f"{row.get('axis')}={row.get('bucket')}:{cell(row.get('net_profit'))}" for row in weak) or "no_top_negative_slice_for_alias",
                "trade_shape": f"avg_trades={cell(summary.get('avg_trade_count'))};worst_month_floor={cell(summary.get('worst_month_floor'))}",
                "alternative_explanations": "duplicate-boundary Tier A+B, 2024-only pressure, MT5 broker-history costs, profile-specific overfit",
                "attribution_confidence": "medium_low(중간-낮음)",
                "next_probe": NEXT_ACTION,
            }
        )
    return rows


def build_result_judgment(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267CP pool-wide shared weakness breakout balance/time-slice/trade-quality review(267CP 후보군 전체 공유 약점 돌파 잔액/시간구간/거래품질 검토)",
            "evidence_available": "MT5 reports(보고서), trade records(거래 기록), curve diagnostics(곡선 진단), time-slice KPI(시간구간 핵심 성과 지표), parser checks(파서 점검)",
            "evidence_missing": "post-review follow-up design(후속 설계), cross-period repeat(확장 기간 반복), Adapter package(어댑터 패키지), ONNX parity(ONNX 동등성)",
            "judgment_label": "exploratory(탐색)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": result["next_action"],
            "user_explanation_hook": "이번 리뷰는 수익 후보를 고르는 단계가 아니라, 어디서 덜 깨지고 어디서 불편한지 분해하는 단계다.",
        }
    ]


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_summary = list(result["candidate_summary"])
    candidate_rows = list(result["candidate_profile_review"])
    top_rows = sorted(candidate_rows, key=lambda row: as_float(row.get("net_profit")), reverse=True)[:12]
    weak_slices = list(result["negative_slices"])[:15]
    profile_rows = list(result["profile_axis_summary"])[:8]
    parser_errors = list(result["parser_errors"])

    lines = [
        "# Stage267 Run267CP Shared Weakness Breakout Balance/Time-Slice/Trade-Quality Review(267단계 267CP 공유 약점 돌파 잔액/시간구간/거래품질 검토)",
        "",
        "- action(행동): run267CO(267CO 실행)의 12개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록)로 다시 읽고 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)를 계산했다.",
        "- effect(효과): headline KPI(대표 핵심 성과 지표)가 좋아 보여도 월별/요일별/시간별/세션별/방향별/기간 구간 약점이 후보 선택을 막는지 확인한다.",
        f"- status(상태): `{result['status']}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- curve_rows(곡선 행): `{result['curve_row_count']}`",
        f"- time_slice_rows(시간구간 행): `{result['time_slice_row_count']}`",
        f"- candidate_profile_rows(후보-프로필 행): `{len(candidate_rows)}`",
        f"- negative_slices(음수 구간): `{len(result['negative_slices'])}`",
        f"- parser_errors(파서 오류): `{len(parser_errors)}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{result['next_action']}`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "이번 실행은 후보를 고르는 단계가 아니다. `s264_lc`는 상대적으로 손실폭이 편하지만 더 넓은 follow-up(후속)이 필요하고, `s264_aia`와 `s258_stc`는 수익은 보이나 DD(drawdown, 손실폭)와 약한 구간이 불편하다. `s264_aih`의 aggressive shock release(공격형 충격 해소)는 PF(profit factor, 수익 팩터)는 좋지만 거래 수와 총수익이 작아 단독 선택 근거가 아니다.",
        "",
        "따라서 다음 run267CQ(267CQ 실행)는 숫자 1등을 고르는 것이 아니라 shared weakness breakout(공유 약점 돌파)을 후속/가지치기 설계로 바꾸어야 한다.",
        "",
        "## Candidate Summary(후보 요약)",
        "",
        "| candidate(후보) | profile rows(프로필 행) | constructive rows(건설 행) | risk rows(위험 행) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭 %) | avg trades(평균 거래 수) | worst month floor(최악 월 바닥) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in candidate_summary:
        lines.append(
            f"| `{row['candidate_alias']}` | {cell(row.get('test_count'))} | {cell(row.get('constructive_row_count'))} | {cell(row.get('risk_row_count'))} | "
            f"{cell(row.get('avg_net_profit'))} | {cell(row.get('avg_profit_factor'))} | {cell(row.get('avg_equity_drawdown_percent'))} | "
            f"{cell(row.get('avg_trade_count'))} | {cell(row.get('worst_month_floor'))} | {row.get('candidate_read')} |"
        )
    lines.extend(
        [
            "",
            "## Profile Axis(프로필 축)",
            "",
            "| profile(프로필) | rows(행) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭 %) | avg trades(평균 거래 수) | risk rows(위험 행) | best candidate(최고 후보) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in profile_rows:
        lines.append(
            f"| `{row.get('test_id')}` | {cell(row.get('row_count'))} | {cell(row.get('avg_net_profit'))} | "
            f"{cell(row.get('avg_profit_factor'))} | {cell(row.get('avg_equity_drawdown_percent'))} | "
            f"{cell(row.get('avg_trade_count'))} | {cell(row.get('risk_row_count'))} | `{row.get('best_candidate_alias')}` |"
        )
    lines.extend(
        [
            "",
            "## Top Candidate-Profile Rows(상위 후보-프로필 행)",
            "",
            "| candidate(후보) | profile(프로필) | net(순수익) | PF(수익 팩터) | DD%(손실폭 %) | trades(거래 수) | weakest month(최약 월) | read(판독) |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in top_rows:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('test_id')}` | {cell(row.get('net_profit'))} | "
            f"{cell(row.get('profit_factor'))} | {cell(row.get('report_equity_drawdown_percent'))} | "
            f"{cell(row.get('trade_count'))} | `{row.get('worst_month')}` {cell(row.get('worst_month_net'))} | {row.get('review_read')} |"
        )
    lines.extend(
        [
            "",
            "## Weak Slices(약한 구간)",
            "",
            "| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | PF(수익 팩터) | DD%(손실폭 %) |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in weak_slices:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('test_id')}` | `{row.get('axis')}` | `{row.get('bucket')}` | "
            f"{cell(row.get('trade_count'))} | {cell(row.get('net_profit'))} | {cell(row.get('profit_factor'))} | "
            f"{cell(row.get('closed_balance_max_drawdown_percent'))} |"
        )
    lines.extend(
        [
            "",
            "## Performance Attribution(성과 귀속)",
            "",
            "- observed_change(관찰 변화): shared weakness breakout(공유 약점 돌파)은 전 후보에서 PF(profit factor, 수익 팩터)와 net profit(순수익)을 만들었지만, DD(drawdown, 손실폭)와 약한 월/세션이 후보별로 다르게 남았다.",
            "- likely_drivers(가능 원인): shared weakness state interaction(공유 약점 상태 상호작용)은 거래 수를 충분히 유지하지만, 특정 후보는 손실폭이 같이 커진다. aggressive shock release(공격형 충격 해소)는 PF는 높지만 거래 수가 줄어 안정 후보로 보기 어렵다.",
            "- alternative_explanations(대안 설명): Tier A+B(티어 A+B)는 duplicate-boundary(중복 경계)이므로 true fallback(실제 대체) 효과로 해석하면 안 된다. 또한 2024 기간 압박만으로 전체 기간 안정성을 말할 수 없다.",
            "- attribution_confidence(귀속 신뢰도): `medium_low(중간-낮음)`. 거래 목록과 구간 근거는 생겼지만, 후속 설계와 반복 검증 전에는 선택 근거가 아니다.",
            "",
            "## Backtest Forensics(백테스트 포렌식)",
            "",
            f"- source_execution_result(원천 실행 결과): `{rel(SOURCE_EXECUTION_RESULT_PATH)}`",
            f"- source_kpi_summary(원천 KPI 요약): `{rel(SOURCE_KPI_SUMMARY_PATH)}`",
            f"- source_forensics(원천 포렌식): `{rel(SOURCE_FORENSICS_PATH)}`",
            f"- source_reports(원천 보고서): `{rel(SOURCE_ROOT / 'mt5' / 'reports')}`",
            "- tester_identity(테스터 정체성): historical 2024(2024 과거 기간) `US100` `M5`, deposit(예치금) 500, Strategy Tester(전략 테스터) 산출물.",
            "- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)은 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건을 따른다. 별도 비용 우위는 주장하지 않는다.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간구간 핵심 성과 지표): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            f"- candidate_profile_review(후보-프로필 검토): `{rel(CANDIDATE_PROFILE_REVIEW_PATH)}`",
            f"- candidate_summary(후보 요약): `{rel(CANDIDATE_SUMMARY_PATH)}`",
            f"- profile_axis_summary(프로필 축 요약): `{rel(PROFILE_AXIS_SUMMARY_PATH)}`",
            f"- negative_slice_summary(음수 구간 요약): `{rel(NEGATIVE_SLICE_PATH)}`",
            f"- performance_attribution_summary(성과 귀속 요약): `{rel(ATTRIBUTION_SUMMARY_PATH)}`",
            f"- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_PATH)}`",
            f"- parser_checks(파서 점검): `{rel(PARSER_CHECKS_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review`.",
            "- judgment_label(판정 라벨): `exploratory(탐색)`.",
            "- selected_candidate(선택 후보): `none`.",
            "- selected_research_baseline(선택 연구 기준 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- next_action(다음 행동): `{result['next_action']}`.",
        ]
    )
    return "\n".join(lines)


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    judgment = "exploratory_review_completed_no_candidate_selection"
    review_base.upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review",
            "tier_scope": "Tier A and duplicate-boundary Tier A+B historical 2024 run267CO MT5 review",
            "scoreboard": "trade_shape_curve_time_slice_review",
            "status": status,
            "judgment": judgment,
            "evidence_boundary": "curve_time_slice_trade_quality_review_not_candidate_selection_not_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"candidate_profile_rows={len(result['candidate_profile_review'])};negative_slices={len(result['negative_slices'])};next_action={next_action};selected_candidate=none.",
        },
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    review_base.upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "notes": f"Run267CP reviews run267CO curve/time-slice/trade-quality; selected_candidate=none; selected_research_baseline=none; onnx_readiness=not_claimed; next_action={next_action}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    review_base.upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review",
            "tier_scope": "Tier A and duplicate-boundary Tier A+B historical 2024 run267CO MT5 review",
            "kpi_scope": "curve_time_slice_trade_quality_review",
            "scoreboard_lane": "trade_shape_curve_time_slice_review",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"candidate_profile_rows={len(result['candidate_profile_review'])};negative_slices={len(result['negative_slices'])}",
            "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "completed_for_run267CO_mt5_report_review",
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
    entries = (
        ("stage267_run267CP_review_script", "producer_script", PRODUCER_PATH, "Builds run267CP curve/time-slice/trade-quality review."),
        ("stage267_run267CP_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267CP paired trade records from run267CO reports."),
        ("stage267_run267CP_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267CP month/weekday/hour/session/direction/chron-segment KPI."),
        ("stage267_run267CP_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267CP closed-balance curve diagnostics."),
        ("stage267_run267CP_candidate_profile_review", "candidate_profile_review", CANDIDATE_PROFILE_REVIEW_PATH, "Run267CP candidate-profile curve and weak-slice review."),
        ("stage267_run267CP_candidate_summary", "candidate_summary", CANDIDATE_SUMMARY_PATH, "Run267CP candidate balance/time-slice summary."),
        ("stage267_run267CP_profile_axis_summary", "profile_axis_summary", PROFILE_AXIS_SUMMARY_PATH, "Run267CP profile axis summary."),
        ("stage267_run267CP_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267CP worst negative slices."),
        ("stage267_run267CP_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Run267CP parser reconciliation checks."),
        ("stage267_run267CP_performance_attribution", "performance_attribution_summary", ATTRIBUTION_SUMMARY_PATH, "Run267CP performance attribution summary."),
        ("stage267_run267CP_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267CP result judgment."),
        ("stage267_run267CP_review_result", "review_result", REVIEW_RESULT_PATH, "Run267CP review JSON payload."),
        ("stage267_run267CP_review_report", "review_report", REPORT_PATH, "User-facing run267CP balance/time-slice/trade-quality review."),
    )
    registry_rows = review_base.read_csv(ARTIFACT_REGISTRY_PATH)
    replacement = {
        artifact_id: {
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
    }
    merged = [row for row in registry_rows if row.get("artifact_id") not in replacement]
    merged.extend(replacement.values())
    review_base.write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    return review_base.replace_line_prefix(text, prefix, replacement)


def append_after_contains(text: str, needle: str, line: str) -> str:
    return review_base.append_after_contains(text, needle, line)


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def update_current_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    report_line = (
        "- run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review"
        f"(267CP 후보군 전체 공유 약점 돌파 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    )
    latest_line = (
        f"- latest_review(최신 검토): run267CP(267CP 실행) candidate_profile_rows(후보-프로필 행) "
        f"`{len(result['candidate_profile_review'])}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    block = "\n".join(
        [
            "Run267CP(267CP 실행)는 run267CO(267CO 실행)의 12개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.",
            f"Effect(효과): candidate_profile_rows(후보-프로필 행) `{len(result['candidate_profile_review'])}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`를 만들었고, 다음은 follow-up/prune design(후속/가지치기 설계)이다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    current = append_after_contains(current, "stage267_run267CO_pool_wide_shared_weakness_breakout_mt5_execution.md", report_line)
    if "- latest_review(최신 검토):" in current:
        lines = current.splitlines()
        for index, line in enumerate(lines):
            if line.startswith("- latest_review(최신 검토):"):
                lines[index] = latest_line
                break
        current = "\n".join(lines) + "\n"
    else:
        current = append_after_contains(current, "## Current Next Action", latest_line)
    current = append_block_once(current, "Run267CP(267CP 실행)는 run267CO", block)
    review_base.write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selection = append_after_contains(selection, "run267CO_pool_wide_shared_weakness_breakout_mt5_execution", report_line)
    selection = append_block_once(selection, "Run267CP(267CP 실행)는 run267CO", block)
    review_base.write_md(SELECTION_STATUS_PATH, selection)

    review_index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_index = replace_line_prefix(review_index, "- status(상태):", f"- status(상태): `{status}`")
    review_index = replace_line_prefix(review_index, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review_index = replace_line_prefix(review_index, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review_index = append_after_contains(review_index, "run267CO_pool_wide_shared_weakness_breakout_mt5_execution", report_line)
    review_index = append_block_once(review_index, "Run267CP(267CP 실행)는 run267CO", block)
    review_base.write_md(REVIEW_INDEX_PATH, review_index)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_executor.COMPLETED_STATUS}", f"  status: {status}", 1)
    workspace = workspace.replace(f"  current_run_id: {SOURCE_RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {SOURCE_RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  next_action: {source_executor.NEXT_COMPLETED}", f"  next_action: {next_action}", 1)
    workspace = append_after_contains(
        workspace,
        "run267CO_pool_wide_shared_weakness_breakout_mt5_execution_report_path",
        f"  run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}",
    )
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267CP(267CP 실행) pool-wide shared weakness breakout balance/time-slice/trade-quality review"
        f"(후보군 전체 공유 약점 돌파 잔액/시간구간/거래품질 검토) `{status}`. "
        f"Effect(효과): run267CO(267CO 실행)의 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 거래 목록과 약한 구간으로 다시 읽었고, "
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
