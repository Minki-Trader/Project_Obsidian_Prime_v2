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
from stage_pipelines.stage267 import run267CG_pool_wide_orthogonal_loss_shape_state_mt5_executor as source_executor
from stage_pipelines.stage267 import run267O_pool_wide_balance_timeslice_trade_quality_review as review_base


STAGE_ID = source_executor.STAGE_ID
SOURCE_RUN_ID = source_executor.RUN_ID
RUN_NUMBER = "run267CH"
RUN_ID = "run267CH_stage267_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review_v1"
STATUS = "run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review_completed"
PARTIAL_STATUS = "run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review_partial_parser_errors"
NEXT_ACTION = "run267CI_design_pool_wide_orthogonal_loss_shape_state_followup_or_prune"
NEXT_ACTION_PARTIAL = "run267CH_repair_pool_wide_orthogonal_loss_shape_state_trade_parser_errors"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review"
SOURCE_ROOT = source_executor.RUN_ROOT
SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
SOURCE_KPI_SUMMARY_PATH = source_executor.KPI_SUMMARY_PATH
SOURCE_FORENSICS_PATH = source_executor.FORENSICS_PATH
SOURCE_REPORT_PATH = source_executor.REPORT_PATH

TRADE_RECORDS_PATH = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = RUN_ROOT / "curve_diagnostics.csv"
CANDIDATE_TEST_REVIEW_PATH = RUN_ROOT / "candidate_profile_review.csv"
CANDIDATE_SUMMARY_PATH = RUN_ROOT / "candidate_balance_timeslice_summary.csv"
PROFILE_AXIS_SUMMARY_PATH = RUN_ROOT / "profile_axis_summary.csv"
NEGATIVE_SLICE_PATH = RUN_ROOT / "negative_slice_summary.csv"
PARSER_CHECKS_PATH = RUN_ROOT / "parser_checks.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review.py")

STAGE_LEDGER_PATH = source_executor.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_executor.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_executor.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_executor.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_executor.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_executor.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_executor.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_executor.REVIEW_INDEX_PATH


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
    review_base.CANDIDATE_TEST_REVIEW_PATH = CANDIDATE_TEST_REVIEW_PATH
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
    review_base.review_read = review_read
    review_base.candidate_read = candidate_read


def normalize_execution_result(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(dict(payload))
    attempts = []
    for attempt in normalized.get("attempts_executed", []):
        next_attempt = dict(attempt)
        profile = str(next_attempt.get("profile_label") or next_attempt.get("source_test_id") or "unknown_profile")
        next_attempt["queue_id"] = next_attempt.get("variant_id")
        next_attempt["test_id"] = profile
        next_attempt["test_type"] = "orthogonal_loss_shape_state"
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


def review_read(curve: Mapping[str, Any], base: Mapping[str, Any], weak_month: Mapping[str, Any]) -> str:
    net = as_float(curve.get("net_profit"))
    base_net = as_float(base.get("net_profit"))
    pf = as_float(curve.get("profit_factor"))
    base_pf = as_float(base.get("profit_factor"))
    equity_dd = as_float(curve.get("report_equity_drawdown_percent"))
    base_dd = as_float(base.get("max_drawdown_percent"))
    weak_month_net = as_float(weak_month.get("net_profit"))
    trade_count = as_int(curve.get("trade_count"))

    if net <= 0.0 or pf < 1.05:
        return "fragile_or_negative_failure_memory(취약 또는 음수 실패 기억)"
    if equity_dd >= 30.0 or weak_month_net <= -260.0:
        return "profit_with_uncomfortable_dd_or_weak_month(수익은 있으나 손실폭 또는 약한 월 불편)"
    if net > base_net + 250.0 and pf >= base_pf - 0.05 and equity_dd <= max(base_dd + 4.0, 24.0) and trade_count >= 150:
        return "constructive_wide_watch_no_selection(넓은 관찰 가치, 선택 아님)"
    if net > base_net and pf >= 1.20 and trade_count >= 150:
        return "constructive_but_needs_curve_pressure(건설적이나 곡선 압박 필요)"
    return "mixed_or_insufficient_curve_evidence(혼합 또는 곡선 근거 부족)"


def candidate_read(rows: Sequence[Mapping[str, Any]]) -> str:
    if not rows:
        return "missing_candidate_rows(후보 행 누락)"
    uncomfortable = [
        row
        for row in rows
        if "uncomfortable_dd" in str(row.get("review_read"))
        or as_float(row.get("report_equity_drawdown_percent")) >= 30.0
        or as_float(row.get("worst_month_net")) <= -260.0
    ]
    constructive = [row for row in rows if str(row.get("review_read")).startswith("constructive")]
    avg_dd = mean(as_float(row.get("report_equity_drawdown_percent")) for row in rows)
    worst_month_floor = min(as_float(row.get("worst_month_net")) for row in rows)
    if uncomfortable and len(constructive) < 2:
        return "risk_first_watch_or_prune(위험 우선 관찰 또는 가지치기)"
    if len(constructive) >= 2 and avg_dd <= 26.0 and worst_month_floor > -220.0:
        return "broad_constructive_watch_no_selection(넓은 건설 관찰, 선택 아님)"
    if constructive:
        return "single_or_narrow_clue_needs_more_pressure(좁은 단서, 추가 압박 필요)"
    return "mixed_or_fragile_no_selection(혼합 또는 취약, 선택 아님)"


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
                "constructive_row_count": sum(1 for row in items if str(row.get("review_read")).startswith("constructive")),
                "best_candidate_alias": best.get("candidate_alias"),
                "best_net_profit": best.get("net_profit"),
                "worst_candidate_alias": worst.get("candidate_alias"),
                "worst_net_profit": worst.get("net_profit"),
            }
        )
    return sorted(output, key=lambda row: -as_float(row.get("avg_net_profit")))


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
        output.append(next_row)
    return output


def result_status(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return PARTIAL_STATUS if parser_errors else STATUS


def result_next_action(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return NEXT_ACTION_PARTIAL if parser_errors else NEXT_ACTION


def short_profile(label: str) -> str:
    if label == "loss_shape_proxy_minimal":
        return "loss shape proxy(손실 형태 대체)"
    if label == "similar_replacement_impulse":
        return "similar replacement impulse(유사 대체 임펄스)"
    return label


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_summary = list(result["candidate_summary"])
    candidate_tests = list(result["candidate_profile_review"])
    top_tests = sorted(candidate_tests, key=lambda row: as_float(row.get("net_profit")), reverse=True)[:12]
    weak_slices = list(result["negative_slices"])[:15]
    parser_errors = list(result["parser_errors"])
    profile_rows = list(result["profile_axis_summary"])
    top_profile_rows = sorted(profile_rows, key=lambda row: as_float(row.get("avg_net_profit")), reverse=True)[:8]

    lines = [
        "# Stage267 Run267CH Orthogonal Loss-Shape/State Balance Review(267단계 267CH 직교 손실 형태/상태 잔액 검토)",
        "",
        "- action(행동): run267CG(267CG 실행)의 20개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록)로 다시 파싱하고, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)를 만들었다.",
        "- effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 후보별 약한 월, 요일, 시간, 세션, 방향, 기간 구간을 분리해 다음 follow-up/prune(후속/가지치기) 판단에 쓸 수 있다.",
        f"- status(상태): `{result['status']}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- curve_rows(곡선 행): `{result['curve_row_count']}`",
        f"- time_slice_rows(시간구간 행): `{result['time_slice_row_count']}`",
        f"- parser_errors(파서 오류): `{len(parser_errors)}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "run267CG(267CG 실행)는 숫자를 만들었고, run267CH(267CH 실행)는 그 숫자가 덜 깨지는지 봤다. loss shape proxy(손실 형태 대체)는 상대적으로 얌전하지만 수익 확장이 작고, similar replacement impulse(유사 대체 임펄스)는 수익을 키우는 대신 DD(drawdown, 손실폭)와 약한 구간 부담이 같이 커진다.",
        "",
        "그래서 아직 selected candidate(선택 후보)는 없다. 다음 run267CI(267CI 실행)에서는 넓게 산 후보를 바로 고르지 말고, 수익을 키운 축과 손실폭을 키운 축을 분리해 follow-up/prune(후속/가지치기)해야 한다.",
        "",
        "## Candidate Summary(후보 요약)",
        "",
        "| candidate(후보) | strong clues(강한 단서) | risk rows(위험 행) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭) | avg trades(평균 거래 수) | worst month floor(최악 월 바닥) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in candidate_summary:
        lines.append(
            f"| `{row['candidate_alias']}` | {cell(row['strong_curve_clue_count'])} | {cell(row['risk_row_count'])} | "
            f"{cell(row['avg_net_profit'])} | {cell(row['avg_profit_factor'])} | {cell(row['avg_equity_drawdown_percent'])} | "
            f"{cell(row['avg_trade_count'])} | {cell(row['worst_month_floor'])} | {row['candidate_read']} |"
        )
    lines.extend(
        [
            "",
            "## Profile Axis(프로필 축)",
            "",
            "| profile(프로필) | candidates(후보 수) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭) | avg trades(평균 거래 수) | worst month floor(최악 월 바닥) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in top_profile_rows:
        lines.append(
            f"| `{short_profile(str(row['test_id']))}` | {cell(row['row_count'])} | {cell(row['avg_net_profit'])} | "
            f"{cell(row['avg_profit_factor'])} | {cell(row['avg_equity_drawdown_percent'])} | {cell(row['avg_trade_count'])} | {cell(row['worst_month_floor'])} |"
        )
    lines.extend(
        [
            "",
            "## Top Candidate-Profile Rows(상위 후보-프로필 행)",
            "",
            "| candidate(후보) | profile(프로필) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | worst month(최악 월) | read(판독) |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in top_tests:
        lines.append(
            f"| `{row['candidate_alias']}` | `{short_profile(str(row['test_id']))}` | {cell(row['net_profit'])} | "
            f"{cell(row['profit_factor'])} | {cell(row['report_equity_drawdown_percent'])} | {cell(row['trade_count'])} | "
            f"`{row['worst_month']}` {cell(row['worst_month_net'])} | {row['review_read']} |"
        )
    lines.extend(
        [
            "",
            "## Weak Slices(약한 구간)",
            "",
            "| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | PF(수익 팩터) | DD%(손실폭) |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in weak_slices:
        lines.append(
            f"| `{row['candidate_alias']}` | `{short_profile(str(row['test_id']))}` | `{row['axis']}` | `{row['bucket']}` | "
            f"{cell(row['trade_count'])} | {cell(row['net_profit'])} | {cell(row['profit_factor'])} | {cell(row['closed_balance_max_drawdown_percent'])} |"
        )
    lines.extend(
        [
            "",
            "## Performance Attribution(성과 귀속)",
            "",
            "- observed_change(관찰 변화): similar replacement impulse(유사 대체 임펄스)는 대부분 후보에서 net profit(순수익)과 trade count(거래 수)를 늘렸지만 DD(drawdown, 손실폭)도 같이 커졌다.",
            "- likely_drivers(가능 원인): trend strength proxy(추세 강도 대체)와 impulse(임펄스) 축이 진입 공급을 늘리면서 수익 기회와 손실 노출을 동시에 키운 것으로 보인다.",
            "- alternative_explanations(대체 설명): Tier A+B(티어 A+B)는 실제 fallback(대체) 합산이 아니라 duplicate boundary(중복 경계)이므로, 넓은 라우팅 안정성으로 해석하면 안 된다.",
            "- attribution_confidence(귀속 신뢰도): `medium(중간)`. MT5 trade list(거래 목록) 근거는 생겼지만, 아직 후속 설계와 추가 기간 압박이 필요하다.",
            "",
            "## Backtest Forensics(백테스트 포렌식)",
            "",
            f"- source_execution_result(원천 실행 결과): `{rel(SOURCE_EXECUTION_RESULT_PATH)}`",
            f"- source_kpi_summary(원천 KPI 요약): `{rel(SOURCE_KPI_SUMMARY_PATH)}`",
            f"- source_forensics(원천 포렌식): `{rel(SOURCE_FORENSICS_PATH)}`",
            f"- source_reports(원천 보고서): `{rel(SOURCE_ROOT / 'mt5' / 'reports')}`",
            "- tester_scope(테스터 범위): historical 2024(2024 과거 기간) `US100` `M5`, deposit(예치금) 500, Strategy Tester(전략 테스터) 산출물.",
            "- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)은 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건을 따른다. 별도 비용 우위는 주장하지 않는다.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간구간 KPI): `{rel(TIME_SLICE_KPI_PATH)}`",
            f"- curve_diagnostics(곡선 진단): `{rel(CURVE_DIAGNOSTICS_PATH)}`",
            f"- candidate_profile_review(후보-프로필 검토): `{rel(CANDIDATE_TEST_REVIEW_PATH)}`",
            f"- candidate_summary(후보 요약): `{rel(CANDIDATE_SUMMARY_PATH)}`",
            f"- profile_axis_summary(프로필 축 요약): `{rel(PROFILE_AXIS_SUMMARY_PATH)}`",
            f"- negative_slice_summary(음수 구간 요약): `{rel(NEGATIVE_SLICE_PATH)}`",
            f"- parser_checks(파서 점검): `{rel(PARSER_CHECKS_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review`.",
            "- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- selected_research_baseline(선택 연구 기준 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- next_action(다음 행동): `{result['next_action']}`.",
        ]
    )
    return "\n".join(lines)


def upsert_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    judgment = "diagnostic_review_completed_no_candidate_selection"
    review_base.upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review",
            "tier_scope": "Tier A and duplicate-boundary Tier A+B historical 2024 run267CG MT5 review",
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
            "lane": "baseline_candidate_racing_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "notes": f"Run267CH reviews run267CG curve/time-slice/trade-quality; selected_candidate=none; onnx_readiness=not_claimed; next_action={next_action}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    review_base.upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review",
            "tier_scope": "Tier A and duplicate-boundary Tier A+B historical 2024 run267CG MT5 review",
            "kpi_scope": "curve_time_slice_trade_quality_review",
            "scoreboard_lane": "trade_shape_curve_time_slice_review",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"candidate_profile_rows={len(result['candidate_profile_review'])};negative_slices={len(result['negative_slices'])}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "completed_for_run267CG_mt5_report_review",
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
        ("stage267_run267CH_review_script", "producer_script", PRODUCER_PATH, "Builds run267CH curve/time-slice/trade-quality review."),
        ("stage267_run267CH_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267CH paired trade records from run267CG reports."),
        ("stage267_run267CH_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267CH month/weekday/hour/session/direction/chron-segment KPI."),
        ("stage267_run267CH_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267CH closed-balance curve diagnostics."),
        ("stage267_run267CH_candidate_profile_review", "candidate_profile_review", CANDIDATE_TEST_REVIEW_PATH, "Run267CH candidate-profile curve and weak-slice review."),
        ("stage267_run267CH_candidate_summary", "candidate_summary", CANDIDATE_SUMMARY_PATH, "Run267CH candidate balance/time-slice summary."),
        ("stage267_run267CH_profile_axis_summary", "profile_axis_summary", PROFILE_AXIS_SUMMARY_PATH, "Run267CH profile axis summary."),
        ("stage267_run267CH_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267CH worst negative slices."),
        ("stage267_run267CH_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Run267CH parser reconciliation checks."),
        ("stage267_run267CH_review_result", "review_result", REVIEW_RESULT_PATH, "Run267CH review JSON payload."),
        ("stage267_run267CH_review_report", "review_report", REPORT_PATH, "User-facing run267CH balance/time-slice/trade-quality review."),
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


def replace_existing_line_prefix(text: str, prefix: str, replacement: str) -> str:
    return review_base.replace_existing_line_prefix(text, prefix, replacement)


def append_after_contains(text: str, needle: str, line: str) -> str:
    return review_base.append_after_contains(text, needle, line)


def update_current_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    report_line = f"- run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review(267CH 후보군 전체 직교 손실 형태/상태 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    summary_line = (
        "Run267CH(267CH 실행)는 run267CG(267CG 실행)의 20개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 trade list(거래 목록), "
        "balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다. "
        "Effect(효과): selected candidate(선택 후보)는 없고, 수익 확장 축과 DD(drawdown, 손실폭) 위험 축을 run267CI(267CI 실행) 후속/가지치기로 넘긴다."
    )
    current_focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267CH(267CH 실행) pool-wide orthogonal loss-shape/state balance/time-slice/trade-quality review"
        f"(후보군 전체 직교 손실 형태/상태 잔액/시간구간/거래품질 검토) `{status}`. Effect(효과): run267CG(267CG 실행)의 20개 MT5(MetaTrader 5, 메타트레이더5) "
        "보고서를 거래 목록, 곡선, 약한 구간으로 다시 읽었고 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), "
        "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )

    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "stage267_run267CG_pool_wide_orthogonal_loss_shape_state_mt5_execution.md", report_line)
            text = append_after_contains(text, "Run267CH(267CH 실행)는", summary_line)
            text = append_after_contains(
                text,
                "## Current Next Action",
                f"- latest_review(최신 검토): run267CH(267CH 실행) candidate_profile_rows(후보-프로필 행) `{len(result['candidate_profile_review'])}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`, report(보고서) `{rel(REPORT_PATH)}`.",
            )
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "run267CG_pool_wide_orthogonal_loss_shape_state_mt5_execution", report_line)
        else:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "stage267_run267CG_pool_wide_orthogonal_loss_shape_state_mt5_execution.md", report_line)
        review_base.write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace("  status: run267CG_pool_wide_orthogonal_loss_shape_state_mt5_batch_completed", f"  status: {status}", 1)
    workspace = workspace.replace(f"  current_run_id: {SOURCE_RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {SOURCE_RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace("  next_action: run267CH_review_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality", f"  next_action: {next_action}", 1)
    workspace = append_after_contains(
        workspace,
        "run267CG_pool_wide_orthogonal_loss_shape_state_mt5_execution_report_path",
        f"  run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}",
    )
    if f"`{status}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + current_focus_line + "\n", 1)
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
            "candidate_profile_review": rel(CANDIDATE_TEST_REVIEW_PATH),
            "candidate_summary": rel(CANDIDATE_SUMMARY_PATH),
            "profile_axis_summary": rel(PROFILE_AXIS_SUMMARY_PATH),
            "negative_slice_summary": rel(NEGATIVE_SLICE_PATH),
            "parser_checks": rel(PARSER_CHECKS_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    review_base.write_csv(TRADE_RECORDS_PATH, trade_rows, columns(trade_rows, ("run_id", "record_view", "net_profit")))
    review_base.write_csv(TIME_SLICE_KPI_PATH, time_rows, columns(time_rows, ("record_view", "axis", "bucket", "net_profit")))
    review_base.write_csv(CURVE_DIAGNOSTICS_PATH, curve_rows, columns(curve_rows, ("record_view", "net_profit", "curve_read")))
    review_base.write_csv(CANDIDATE_TEST_REVIEW_PATH, candidate_rows, columns(candidate_rows, ("candidate_alias", "test_id", "net_profit")))
    review_base.write_csv(CANDIDATE_SUMMARY_PATH, candidate_summary, columns(candidate_summary, ("candidate_alias", "avg_net_profit", "candidate_read")))
    review_base.write_csv(PROFILE_AXIS_SUMMARY_PATH, profile_axis_summary, columns(profile_axis_summary, ("test_id", "avg_net_profit")))
    review_base.write_csv(NEGATIVE_SLICE_PATH, negative, columns(negative, ("candidate_alias", "test_id", "axis", "bucket", "net_profit")))
    review_base.write_csv(PARSER_CHECKS_PATH, parser_checks, columns(parser_checks, ("attempt_name", "parser_status")))
    review_base.write_json(REVIEW_RESULT_PATH, result)
    review_base.write_md(REPORT_PATH, report_markdown(result))
    upsert_ledgers(created_at, result)
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
