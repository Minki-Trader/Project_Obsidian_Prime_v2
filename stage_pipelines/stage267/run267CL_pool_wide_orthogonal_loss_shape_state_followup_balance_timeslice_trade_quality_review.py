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
from stage_pipelines.stage267 import run267CK_pool_wide_orthogonal_loss_shape_state_followup_mt5_executor as source_executor
from stage_pipelines.stage267 import run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review as prior_review
from stage_pipelines.stage267 import run267O_pool_wide_balance_timeslice_trade_quality_review as review_base


STAGE_ID = source_executor.STAGE_ID
SOURCE_RUN_ID = source_executor.RUN_ID
RUN_NUMBER = "run267CL"
RUN_ID = "run267CL_stage267_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review_v1"
STATUS = "run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review_completed"
PARTIAL_STATUS = "run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review_partial_parser_errors"
NEXT_ACTION = "run267CM_design_pool_wide_orthogonal_loss_shape_state_followup_or_prune_from_run267CL_review"
NEXT_ACTION_PARTIAL = "run267CL_repair_pool_wide_orthogonal_loss_shape_state_followup_trade_parser_errors"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review"
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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review.py")

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
        profile = str(next_attempt.get("profile_label") or next_attempt.get("variant_id") or "unknown_profile")
        next_attempt["queue_id"] = next_attempt.get("variant_id")
        next_attempt["test_id"] = profile
        next_attempt["test_type"] = "orthogonal_loss_shape_state_followup"
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
    pf = as_float(curve.get("profit_factor"))
    equity_dd = as_float(curve.get("report_equity_drawdown_percent"))
    trade_count = as_int(curve.get("trade_count"))
    weak_month_net = as_float(weak_month.get("net_profit"))
    base_net = as_float(base.get("net_profit"))
    base_dd = as_float(base.get("max_drawdown_percent"))

    if net <= 0.0 or pf < 1.05 or trade_count < 120:
        return "fragile_or_supply_weak_failure_memory(취약 또는 거래공급 약한 실패 기억)"
    if equity_dd >= 22.0 or weak_month_net <= -220.0:
        return "profit_with_uncomfortable_curve_risk(수익은 있으나 곡선 위험 불편)"
    if net > base_net and equity_dd <= max(base_dd + 3.0, 18.5) and pf >= 1.35 and trade_count >= 250:
        return "constructive_followup_watch_no_selection(건설적 후속 관찰, 선택 아님)"
    if net > 900.0 and pf >= 1.30 and trade_count >= 250:
        return "positive_profit_shape_but_needs_slice_review(수익 형태 양호하나 구간 검토 필요)"
    return "mixed_or_insufficient_curve_evidence(혼합 또는 곡선 근거 부족)"


def candidate_read(rows: Sequence[Mapping[str, Any]]) -> str:
    if not rows:
        return "missing_candidate_rows(후보 행 누락)"
    uncomfortable = [
        row
        for row in rows
        if "uncomfortable" in str(row.get("review_read"))
        or as_float(row.get("report_equity_drawdown_percent")) >= 22.0
        or as_float(row.get("worst_month_net")) <= -220.0
    ]
    constructive = [
        row
        for row in rows
        if str(row.get("review_read")).startswith("constructive")
        or str(row.get("review_read")).startswith("positive_profit_shape")
    ]
    avg_dd = mean(as_float(row.get("report_equity_drawdown_percent")) for row in rows)
    worst_month_floor = min(as_float(row.get("worst_month_net")) for row in rows)
    if uncomfortable:
        return "profitable_but_curve_risk_watch_no_selection(수익 있으나 곡선 위험 관찰, 선택 아님)"
    if len(constructive) == len(rows) and avg_dd <= 18.5 and worst_month_floor > -180.0:
        return "broad_constructive_watch_no_selection(넓은 건설 관찰, 선택 아님)"
    if constructive:
        return "single_or_narrow_clue_needs_more_pressure(좁은 단서, 추가 압박 필요)"
    return "mixed_or_fragile_no_selection(혼합 또는 취약, 선택 아님)"


def build_profile_axis_summary(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return prior_review.build_profile_axis_summary(rows)


def add_candidate_risk_counts(
    summary_rows: Sequence[Mapping[str, Any]],
    candidate_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    return prior_review.add_candidate_risk_counts(summary_rows, candidate_rows)


def result_status(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return PARTIAL_STATUS if parser_errors else STATUS


def result_next_action(parser_errors: Sequence[Mapping[str, Any]]) -> str:
    return NEXT_ACTION_PARTIAL if parser_errors else NEXT_ACTION


def short_profile(label: str) -> str:
    if label == "controlled_impulse_dd_state_throttle":
        return "controlled impulse DD state throttle(통제형 임펄스 손실폭 상태 조절)"
    if label == "oos_anchor_impulse_pressure":
        return "OOS anchor impulse pressure(표본외 앵커 임펄스 압박)"
    return label


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_summary = list(result["candidate_summary"])
    candidate_tests = list(result["candidate_profile_review"])
    top_tests = sorted(candidate_tests, key=lambda row: as_float(row.get("net_profit")), reverse=True)
    weak_slices = list(result["negative_slices"])[:15]
    parser_errors = list(result["parser_errors"])
    profile_rows = list(result["profile_axis_summary"])

    lines = [
        "# Stage267 Run267CL Follow-up Balance/Time-Slice/Trade-Quality Review(267단계 267CL 후속 잔액/시간구간/거래품질 검토)",
        "",
        f"- status(상태): `{result['status']}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- curve_rows(곡선 행): `{result['curve_row_count']}`",
        f"- time_slice_rows(시간 구간 행): `{result['time_slice_row_count']}`",
        f"- parser_errors(파서 오류): `{len(parser_errors)}`",
        f"- next_action(다음 행동): `{result['next_action']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "run267CK(267CK 실행)의 숫자는 둘 다 좋아 보였지만, run267CL(267CL 실행)은 그 숫자를 바로 고르지 않고 거래 목록과 곡선으로 다시 열어본 검토다.",
        "효과(effect, 효과)는 `s264_lc`와 `s264_aia`가 실제로 덜 깨지는지, 특정 월/시간/방향에 손실이 몰리는지, DD(drawdown, 손실폭)가 편한지 분리해서 보는 것이다.",
        "현재 결론은 둘 다 연구 단서로는 살아 있지만, 아직 선택 후보(selected candidate, 선택 후보)나 연구 기준 후보(selected research baseline, 선택 연구 기준 후보)는 아니다.",
        "",
        "## Candidate Summary(후보 요약)",
        "",
        "| candidate(후보) | profile rows(프로필 행) | strong clue rows(강한 단서 행) | risk rows(위험 행) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭 %) | avg trades(평균 거래 수) | worst month floor(최악 월 바닥) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in candidate_summary:
        lines.append(
            f"| `{row['candidate_alias']}` | {cell(row.get('test_count', row.get('row_count')))} | "
            f"{cell(row.get('strong_curve_clue_count', ''))} | {cell(row.get('risk_row_count', ''))} | "
            f"{cell(row['avg_net_profit'])} | {cell(row['avg_profit_factor'])} | "
            f"{cell(row['avg_equity_drawdown_percent'])} | {cell(row['avg_trade_count'])} | "
            f"{cell(row['worst_month_floor'])} | {row['candidate_read']} |"
        )
    lines.extend(
        [
            "",
            "## Profile Axis(프로필 축)",
            "",
            "| profile(프로필) | candidates(후보 수) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭 %) | avg trades(평균 거래 수) | worst month floor(최악 월 바닥) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in profile_rows:
        lines.append(
            f"| `{short_profile(str(row['test_id']))}` | {cell(row.get('row_count', row.get('candidate_count')))} | "
            f"{cell(row['avg_net_profit'])} | {cell(row['avg_profit_factor'])} | "
            f"{cell(row['avg_equity_drawdown_percent'])} | {cell(row['avg_trade_count'])} | "
            f"{cell(row['worst_month_floor'])} |"
        )
    lines.extend(
        [
            "",
            "## Candidate-Profile Rows(후보-프로필 행)",
            "",
            "| candidate(후보) | profile(프로필) | net(순수익) | PF(수익 팩터) | DD%(손실폭 %) | trades(거래 수) | worst month(최악 월) | weak session(약한 세션) | weak chron(약한 순서) | read(판독) |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |",
        ]
    )
    for row in top_tests:
        lines.append(
            f"| `{row['candidate_alias']}` | `{short_profile(str(row['test_id']))}` | {cell(row['net_profit'])} | "
            f"{cell(row['profit_factor'])} | {cell(row['report_equity_drawdown_percent'])} | {cell(row['trade_count'])} | "
            f"`{row['worst_month']}` {cell(row['worst_month_net'])} | `{row['weakest_session_report']}` {cell(row['weakest_session_net'])} | "
            f"`{row['weakest_chron_segment']}` {cell(row['weakest_chron_net'])} | {row['review_read']} |"
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
            f"| `{row['candidate_alias']}` | `{short_profile(str(row['test_id']))}` | `{row['axis']}` | `{row['bucket']}` | "
            f"{cell(row['trade_count'])} | {cell(row['net_profit'])} | {cell(row['profit_factor'])} | "
            f"{cell(row['closed_balance_max_drawdown_percent'])} |"
        )
    lines.extend(
        [
            "",
            "## Performance Attribution(성과 귀속)",
            "",
            "- observed_change(관찰 변화): run267CK(267CK 실행)의 두 follow-up(후속) 후보는 2024 구간에서 순수익과 PF(수익 팩터)를 모두 양수로 유지했다.",
            "- comparison_baseline(비교 기준): Stage267(267단계)의 2024 baseline(2024 기준), run267CG(267CG 실행), run267CH(267CH 실행)의 약한 구간 검토다.",
            "- likely_drivers(가능 원인): `s264_lc`는 controlled impulse DD state throttle(통제형 임펄스 손실폭 상태 조절)로 거래 공급을 유지했고, `s264_aia`는 OOS anchor impulse pressure(표본외 앵커 임펄스 압박)로 PF(수익 팩터)를 조금 더 높였다.",
            "- segment_checks(구간 점검): month(월), weekday(요일), close_hour_report(청산 시간), session_report(세션), direction(방향), chron_segment(시간 순서 구간)를 분리했다.",
            "- attribution_confidence(귀속 신뢰도): `medium(중간)`. trade list(거래 목록)는 있지만, 아직 다음 설계에서 보류된 후보와 실패 기억을 함께 비교해야 한다.",
            "",
            "## Backtest Forensics(백테스트 포렌식)",
            "",
            f"- source_execution_result(원천 실행 결과): `{rel(SOURCE_EXECUTION_RESULT_PATH)}`",
            f"- source_kpi_summary(원천 KPI 요약): `{rel(SOURCE_KPI_SUMMARY_PATH)}`",
            f"- source_forensics(원천 포렌식): `{rel(SOURCE_FORENSICS_PATH)}`",
            f"- source_report(원천 보고서): `{rel(SOURCE_REPORT_PATH)}`",
            f"- source_reports(원천 보고서 폴더): `{rel(SOURCE_ROOT / 'mt5' / 'reports')}`",
            "- tester_identity(테스터 정체성): historical 2024(2024 과거 구간), `US100`, `M5`, deposit(예치금) `500`, Strategy Tester(전략 테스터) 산출물.",
            "- trade_evidence(거래 근거): MT5 report(보고서)의 deal list(체결 목록)를 trade list(거래 목록)로 다시 짝지어 확인했다.",
            "- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)는 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건에 따른다. 별도 비용 우위는 주장하지 않는다.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- trade_records(거래 기록): `{rel(TRADE_RECORDS_PATH)}`",
            f"- time_slice_kpi(시간 구간 KPI): `{rel(TIME_SLICE_KPI_PATH)}`",
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
            "- result_subject(결과 대상): `run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review`.",
            "- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- selected_research_baseline(선택 연구 기준 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
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
            "row_id": "stage267_run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review",
            "tier_scope": "Tier A and duplicate-boundary Tier A+B historical 2024 run267CK MT5 review",
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
            "lane": "baseline_candidate_racing_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "notes": f"Run267CL reviews run267CK curve/time-slice/trade-quality; selected_candidate=none; selected_research_baseline=none; onnx_readiness=not_claimed; next_action={next_action}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    review_base.upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review",
            "tier_scope": "Tier A and duplicate-boundary Tier A+B historical 2024 run267CK MT5 review",
            "kpi_scope": "curve_time_slice_trade_quality_review",
            "scoreboard_lane": "trade_shape_curve_time_slice_review",
            "status": status,
            "judgment": judgment,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"candidate_profile_rows={len(result['candidate_profile_review'])};negative_slices={len(result['negative_slices'])}",
            "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "completed_for_run267CK_mt5_report_review",
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
        ("stage267_run267CL_review_script", "producer_script", PRODUCER_PATH, "Builds run267CL curve/time-slice/trade-quality review."),
        ("stage267_run267CL_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267CL paired trade records from run267CK reports."),
        ("stage267_run267CL_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267CL month/weekday/hour/session/direction/chron-segment KPI."),
        ("stage267_run267CL_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267CL closed-balance curve diagnostics."),
        ("stage267_run267CL_candidate_profile_review", "candidate_profile_review", CANDIDATE_TEST_REVIEW_PATH, "Run267CL candidate-profile curve and weak-slice review."),
        ("stage267_run267CL_candidate_summary", "candidate_summary", CANDIDATE_SUMMARY_PATH, "Run267CL candidate balance/time-slice summary."),
        ("stage267_run267CL_profile_axis_summary", "profile_axis_summary", PROFILE_AXIS_SUMMARY_PATH, "Run267CL profile axis summary."),
        ("stage267_run267CL_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267CL worst negative slices."),
        ("stage267_run267CL_parser_checks", "parser_checks", PARSER_CHECKS_PATH, "Run267CL parser reconciliation checks."),
        ("stage267_run267CL_review_result", "review_result", REVIEW_RESULT_PATH, "Run267CL review JSON payload."),
        ("stage267_run267CL_review_report", "review_report", REPORT_PATH, "User-facing run267CL balance/time-slice/trade-quality review."),
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


def update_workspace_state(status: str, next_action: str) -> None:
    report_entry = f"  run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review_report_path: {rel(REPORT_PATH)}"
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = replace_line_prefix(text, "current_run_id:", f"current_run_id: {RUN_ID}")
    text = text.replace(f"  status: {source_executor.COMPLETED_STATUS}", f"  status: {status}", 1)
    text = text.replace(f"  current_run_id: {SOURCE_RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    text = text.replace(f"  last_completed_run_id: {SOURCE_RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    text = text.replace(f"  next_action: {source_executor.NEXT_COMPLETED}", f"  next_action: {next_action}", 1)
    text = append_after_contains(text, "run267CK_pool_wide_orthogonal_loss_shape_state_followup_mt5_execution_report_path", report_entry)
    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267CL(267CL 실행) pool-wide orthogonal loss-shape/state follow-up balance/time-slice/trade-quality review"
        f"(후보군 전체 직교 손실 형태/상태 후속 잔액/시간구간/거래품질 검토) `{status}`. Effect(효과): run267CK(267CK 실행)의 "
        "4개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 거래 목록, 곡선, 약한 구간으로 다시 읽었고 selected candidate(선택 후보), "
        "selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if f"`{status}`" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus_line, 1)
    review_base.write_md(WORKSPACE_STATE_PATH, text)


def update_current_docs(result: Mapping[str, Any]) -> None:
    status = str(result["status"])
    next_action = str(result["next_action"])
    report_line = f"- run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review(267CL 후보군 전체 직교 손실 형태/상태 후속 잔액/시간구간/거래품질 검토): `{rel(REPORT_PATH)}`"
    latest_line = (
        f"- latest_review(최신 검토): run267CL(267CL 실행) candidate_profile_rows(후보-프로필 행) "
        f"`{len(result['candidate_profile_review'])}`, negative_slices(음수 구간) `{len(result['negative_slices'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    summary_line = (
        "Run267CL(267CL 실행)는 run267CK(267CK 실행)의 4개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 "
        "trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), "
        "trade quality(거래 품질)로 다시 읽었다. Effect(효과): 수익 단서는 보존하되 후보 선택은 보류하고 run267CM(267CM 실행) "
        "후속/가지치기 설계로 넘긴다."
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "stage267_run267CK_pool_wide_orthogonal_loss_shape_state_followup_mt5_execution.md", report_line)
            text = append_after_contains(text, "Run267CL(267CL 실행)", summary_line)
            if "- latest_review(최신 검토):" in text:
                lines = text.splitlines()
                for index, line in enumerate(lines):
                    if line.startswith("- latest_review(최신 검토):"):
                        lines[index] = latest_line
                        break
                text = "\n".join(lines) + "\n"
            else:
                text = append_after_contains(text, "## Current Next Action", latest_line)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
            text = append_after_contains(text, "run267CK_pool_wide_orthogonal_loss_shape_state_followup_mt5_execution", report_line)
        else:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "stage267_run267CK_pool_wide_orthogonal_loss_shape_state_followup_mt5_execution.md", report_line)
        review_base.write_md(path, text)
    update_workspace_state(status, next_action)


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
