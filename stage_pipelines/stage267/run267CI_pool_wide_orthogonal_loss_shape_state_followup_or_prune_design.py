from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage267 import run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review as source_review


STAGE_ID = source_review.STAGE_ID
SOURCE_RUN_ID = source_review.RUN_ID
RUN_NUMBER = "run267CI"
RUN_ID = "run267CI_stage267_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design_v1"
STATUS = "run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design_completed"
JUDGMENT = "followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267CJ_materialize_pool_wide_orthogonal_loss_shape_state_followup_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_orthogonal_loss_shape_state_followup_or_prune_design"
SOURCE_REVIEW_ROOT = source_review.RUN_ROOT

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_REVIEW_PATH = source_review.CANDIDATE_TEST_REVIEW_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_PROFILE_AXIS_PATH = source_review.PROFILE_AXIS_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH

BRANCH_DECISION_PATH = RUN_ROOT / "branch_decisions.csv"
MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "materialization_queue.csv"
PRUNE_MATRIX_PATH = RUN_ROOT / "prune_matrix.csv"
EXPERIMENT_DESIGN_PATH = RUN_ROOT / "experiment_design_receipt.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design.py")

STAGE_LEDGER_PATH = source_review.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_review.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_review.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_review.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_review.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_review.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_review.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_review.REVIEW_INDEX_PATH

BRANCH_DECISION_COLUMNS = (
    "decision_id",
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "best_profile",
    "best_net_profit",
    "best_profit_factor",
    "best_equity_drawdown_percent",
    "worst_month",
    "worst_month_net",
    "weakest_weekday_net",
    "decision_label",
    "next_use",
    "why",
    "risk_boundary",
    "reopen_condition",
)

QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "workstream",
    "candidate_aliases",
    "source_profile",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "materialization_instruction",
)

PRUNE_COLUMNS = (
    "prune_id",
    "prune_label",
    "affected_scope",
    "why_pruned",
    "reopen_condition",
)

FAILURE_MEMORY_COLUMNS = (
    "memory_id",
    "pattern",
    "affected_scope",
    "evidence",
    "next_handling",
)

RESULT_JUDGMENT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)


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
        return int(float(value))
    except (TypeError, ValueError):
        return default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def group_by(rows: Iterable[Mapping[str, Any]], key: str) -> dict[str, list[Mapping[str, Any]]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get(key)), []).append(row)
    return grouped


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(rows, key=lambda row: as_float(row.get("net_profit")))


def profile_row(rows: Sequence[Mapping[str, Any]], alias: str, profile: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("candidate_alias") == alias and row.get("test_id") == profile:
            return row
    return {}


def make_branch_decisions(candidate_rows: Sequence[Mapping[str, Any]], summary_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped = group_by(candidate_rows, "candidate_alias")
    summary_by_alias = {str(row.get("candidate_alias")): row for row in summary_rows}
    decisions: list[dict[str, Any]] = []
    order = ("s264_lc", "s264_aia", "s264_aih", "s262_lih", "s258_stc")
    for alias in order:
        rows = grouped.get(alias, [])
        if not rows:
            continue
        best = best_row(rows)
        impulse = profile_row(rows, alias, "similar_replacement_impulse")
        loss_shape = profile_row(rows, alias, "loss_shape_proxy_minimal")
        summary = summary_by_alias.get(alias, {})
        if alias == "s264_lc":
            label = "p0_explosive_controlled_followup(우선순위0 폭발형 통제 후속)"
            next_use = "materialize_impulse_dd_constrained_state_variant(임펄스 손실폭 통제 상태 변형 물질화)"
            why = "highest net among run267CH rows while DD stayed below 20%, but Monday and 2024-12 remain weak(267CH 최고 순수익이면서 손실폭 20% 미만, 그러나 월요일과 2024년 12월 약점 존재)"
            risk = "do not select from headline net; require non-calendar state pressure and curve review(대표 순수익 선택 금지, 비달력 상태 압박과 곡선 검토 필요)"
            reopen = "promote only after materialization plus MT5 execution plus balance/time-slice review stays less broken(물질화, MT5 실행, 잔액/시간구간 검토 뒤 덜 깨질 때만 승격)"
        elif alias == "s264_aia":
            label = "p0_oos_anchor_pressure_watch(우선순위0 표본외 앵커 압박 관찰)"
            next_use = "materialize_oos_anchor_impulse_pressure_variant(표본외 앵커 임펄스 압박 변형 물질화)"
            why = "similar replacement restored profit supply but DD is close to high-risk band(유사 대체가 수익 공급을 회복했지만 손실폭이 고위험 구간에 가까움)"
            risk = "watch as OOS anchor only, not selected candidate(표본외 앵커 관찰용이지 선택 후보 아님)"
            reopen = "continue only if cross-period pressure does not move the weak month deeper(확장 기간 압박에서 약한 월이 더 깊어지지 않을 때만 지속)"
        elif alias == "s264_aih":
            label = "p1_core_challenger_watch_after_s264_lc(우선순위1 핵심 도전자 관찰)"
            next_use = "hold_for_core_challenger_trace_and_loss_shape_lift(핵심 도전자 추적 및 손실 형태 공급 확장 대기)"
            why = "core challenger remains constructive but no longer leads this tranche(핵심 도전자는 건설적이나 이번 묶음의 선두는 아님)"
            risk = "avoid deep repair loop; use as trace against s264_lc(깊은 수리 루프 금지, s264_lc 대비 추적)"
            reopen = "reopen if s264_lc fails or loss-shape supply lift improves without Monday damage(s264_lc가 실패하거나 손실 형태 공급 확장이 월요일 손상 없이 개선될 때 재개)"
        elif alias == "s262_lih":
            label = "p1_validation_heavy_stability_lift_watch(우선순위1 검증 중심 안정 확장 관찰)"
            next_use = "hold_as_validation_heavy_control_for_loss_shape_supply_lift(손실 형태 공급 확장 검증 중심 대조로 유지)"
            why = "validation-heavy role is useful as control, but impulse DD is too close to 30%(검증 중심 역할은 대조군으로 유용하지만 임펄스 손실폭이 30%에 가까움)"
            risk = "do not force aggressive impulse as standalone(공격형 임펄스를 독립 후보로 강행하지 않음)"
            reopen = "reopen if low-DD loss-shape lift keeps validation-style stability(낮은 손실폭 손실 형태 확장이 검증형 안정성을 유지할 때 재개)"
        else:
            label = "stress_comparator_only_prune_deep_repair(압박 비교군만 유지, 깊은 수리 가지치기)"
            next_use = "stress_comparator_receipt_no_deep_repair(압박 비교 영수증, 깊은 수리 없음)"
            why = "similar impulse reached high net but DD 31.65 and Monday -313.09 are too uncomfortable(유사 임펄스 순수익은 높지만 손실폭 31.65와 월요일 -313.09가 불편)"
            risk = "keep for stress comparison only(압박 비교용으로만 유지)"
            reopen = "reopen only if a different non-calendar structure lowers DD without shrinking trades(다른 비달력 구조가 거래 수를 줄이지 않고 손실폭을 낮출 때만 재개)"
        decisions.append(
            {
                "decision_id": f"run267ci_d{len(decisions)+1:02d}_{alias}",
                "candidate_alias": alias,
                "candidate_id": best.get("candidate_id") or summary.get("candidate_id"),
                "candidate_role": best.get("candidate_role") or summary.get("candidate_role"),
                "best_profile": best.get("test_id"),
                "best_net_profit": best.get("net_profit"),
                "best_profit_factor": best.get("profit_factor"),
                "best_equity_drawdown_percent": best.get("report_equity_drawdown_percent"),
                "worst_month": best.get("worst_month"),
                "worst_month_net": best.get("worst_month_net"),
                "weakest_weekday_net": impulse.get("weakest_weekday_net") or loss_shape.get("weakest_weekday_net"),
                "decision_label": label,
                "next_use": next_use,
                "why": why,
                "risk_boundary": risk,
                "reopen_condition": reopen,
            }
        )
    return decisions


def make_materialization_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run267cj_q01_s264_lc_impulse_dd_constrained_state",
            "priority": "P0",
            "workstream": "explosive_but_controlled_impulse(폭발형이지만 통제된 임펄스)",
            "candidate_aliases": "s264_lc",
            "source_profile": "similar_replacement_impulse",
            "hypothesis": "s264_lc impulse edge can keep the high trade supply while a non-calendar state throttle reduces Monday and 2024-12 damage(s264_lc 임펄스 우위는 높은 거래 공급을 유지하면서 비달력 상태 제어로 월요일과 2024년 12월 손상을 줄일 수 있다)",
            "decision_use": "decide whether s264_lc deserves next Adapter structure work(s264_lc가 다음 어댑터 구조 작업 가치가 있는지 판단)",
            "comparison_baseline": "run267CH s264_lc similar_replacement_impulse and loss_shape_proxy_minimal(267CH s264_lc 유사 대체 임펄스 및 손실 형태 대체 최소형)",
            "control_variables": "US100 M5, historical 2024, score-table/runtime handoff, Tier A plus duplicate-boundary Tier A+B(US100 M5, 2024 과거 기간, 점수표/런타임 인계, Tier A와 중복 경계 Tier A+B)",
            "changed_variables": "add non-calendar loss-state throttle based on return/ATR shock and curve underwater state; no Monday literal filter(수익률/ATR 충격과 곡선 잠수 상태 기반 비달력 손실 상태 제어 추가, 월요일 문자 필터 금지)",
            "sample_scope": "historical_2024 first, then cross-period if curve pressure passes(2024 과거 기간 우선, 곡선 압박 통과 시 확장 기간)",
            "success_criteria": "net remains above 1200, DD below 22%, Monday loss improves by at least 30%, trades stay above 320(순수익 1200 초과, 손실폭 22% 미만, 월요일 손실 30% 이상 완화, 거래 수 320 초과)",
            "failure_criteria": "profit shrinks below 900, DD rises, or weak loss moves to another month/session(수익 900 미만, 손실폭 증가, 또는 약한 손실이 다른 월/세션으로 이동)",
            "invalid_conditions": "calendar-only deletion, changed symbol/timeframe, missing tester report, missing trade list(달력 단독 삭제, 심볼/시간프레임 변경, 테스터 보고서 누락, 거래 목록 누락)",
            "stop_conditions": "one materialization plus one MT5 execution plus one review before deeper repair(물질화 1회, MT5 실행 1회, 검토 1회 뒤 깊은 수리 여부 판단)",
            "evidence_plan": "set/ini/model artifacts, MT5 reports, trade_records, curve_diagnostics, time_slice_kpi, parser_checks(설정/초기화/모델 산출물, MT5 보고서, 거래 기록, 곡선 진단, 시간구간 KPI, 파서 점검)",
            "materialization_instruction": "build one aggressive controlled variant and one source-profile reproduction row(공격형 통제 변형 1개와 원천 프로필 재현 행 1개를 만든다)",
        },
        {
            "queue_id": "run267cj_q02_s264_aia_oos_anchor_impulse_pressure",
            "priority": "P0",
            "workstream": "oos_anchor_pressure(표본외 앵커 압박)",
            "candidate_aliases": "s264_aia",
            "source_profile": "similar_replacement_impulse",
            "hypothesis": "s264_aia can be useful as an OOS anchor only if the impulse profile survives DD pressure(s264_aia는 임펄스 프로필이 손실폭 압박을 버틸 때만 표본외 앵커로 유용하다)",
            "decision_use": "decide whether to keep or downgrade the OOS anchor role(표본외 앵커 역할 유지 또는 강등 판단)",
            "comparison_baseline": "run267CH s264_aia similar_replacement_impulse(267CH s264_aia 유사 대체 임펄스)",
            "control_variables": "same runtime handoff, same historical 2024 profile, no calendar-only repair(같은 런타임 인계, 같은 2024 과거 프로필, 달력 단독 수리 금지)",
            "changed_variables": "apply DD-shape pressure and cross-period queue after 2024 reproduction(2024 재현 뒤 손실폭 형태 압박과 확장 기간 대기열 적용)",
            "sample_scope": "historical_2024, then 2023H2/2025H1/2025H2 if P0 passes(2024 과거 기간, P0 통과 시 2023H2/2025H1/2025H2)",
            "success_criteria": "DD below 26%, worst month above -140, positive month ratio stable(손실폭 26% 미만, 최악 월 -140 초과, 양수 월 비율 안정)",
            "failure_criteria": "DD stays near 28%+ or July loss deepens(손실폭이 28% 이상 부근에 남거나 7월 손실 심화)",
            "invalid_conditions": "using OOS label as selection evidence without validation pressure(검증 압박 없이 표본외 라벨을 선택 근거로 사용)",
            "stop_conditions": "one pressure pass before keep/downgrade(압박 1회 뒤 유지/강등)",
            "evidence_plan": "MT5 KPI, curve diagnostics, weak month/session rows, failure memory(핵심 성과 지표, 곡선 진단, 약한 월/세션 행, 실패 기억)",
            "materialization_instruction": "materialize after q01 or alongside q01 if batch capacity allows(q01 이후 또는 묶음 여유가 있으면 q01과 함께 물질화)",
        },
        {
            "queue_id": "run267cj_q03_loss_shape_proxy_trade_supply_lift_pool",
            "priority": "P1",
            "workstream": "stable_axis_supply_lift(안정 축 거래 공급 확장)",
            "candidate_aliases": "s264_lc;s264_aih;s262_lih",
            "source_profile": "loss_shape_proxy_minimal",
            "hypothesis": "low-DD loss-shape proxy can gain trade supply without becoming the impulse DD problem(낮은 손실폭 손실 형태 대체가 임펄스 손실폭 문제로 변하지 않고 거래 공급을 늘릴 수 있다)",
            "decision_use": "create defensive control for Adapter candidates(어댑터 후보용 방어 대조군 생성)",
            "comparison_baseline": "run267CH loss_shape_proxy_minimal rows(267CH 손실 형태 대체 최소형 행)",
            "control_variables": "same candidate pool, same historical 2024 MT5 tester settings(같은 후보군, 같은 2024 과거 MT5 테스터 설정)",
            "changed_variables": "slightly widen state gate and risk/ATR handoff without stacking filters(필터 덧붙이기 없이 상태 게이트와 risk/ATR 인계를 약간 확장)",
            "sample_scope": "historical_2024 Tier A plus duplicate-boundary Tier A+B(2024 과거 Tier A와 중복 경계 Tier A+B)",
            "success_criteria": "net improves at least 25% while DD remains below 16% and trades stay above 210(순수익 25% 이상 개선, 손실폭 16% 미만, 거래 수 210 초과)",
            "failure_criteria": "trade supply lift worsens Monday or pushes DD above 20%(거래 공급 확장이 월요일을 악화하거나 손실폭을 20% 초과로 밀어 올림)",
            "invalid_conditions": "new feature order not traceable or runtime handoff mismatch(새 피처 순서 추적 불가 또는 런타임 인계 불일치)",
            "stop_conditions": "do not run more than one lift tranche before review(검토 전 공급 확장 묶음 1회를 넘기지 않음)",
            "evidence_plan": "feature blueprint, score table, MT5 report, curve review(피처 청사진, 점수표, MT5 보고서, 곡선 검토)",
            "materialization_instruction": "P1 only after P0 queue is materialized or explicitly batched(P0 대기열 물질화 뒤 또는 명시 묶음일 때만 P1)",
        },
        {
            "queue_id": "run267cj_q04_monday_noncalendar_state_attribution",
            "priority": "P1",
            "workstream": "weak_slice_state_attribution(약한 구간 상태 귀속)",
            "candidate_aliases": "s264_lc;s264_aih;s264_aia;s262_lih;s258_stc",
            "source_profile": "similar_replacement_impulse",
            "hypothesis": "the Monday loss cluster is a market-state cluster, not a weekday permission rule(월요일 손실 군집은 요일 허용 규칙이 아니라 시장 상태 군집이다)",
            "decision_use": "decide whether non-calendar state features deserve another adapter pass(비달력 상태 피처가 추가 어댑터 회차 가치가 있는지 판단)",
            "comparison_baseline": "run267CH negative_slice_summary Monday rows(267CH 음수 구간 요약 월요일 행)",
            "control_variables": "no MT5 selection claim, no calendar-only deletion(MT5 선택 주장 없음, 달력 단독 삭제 없음)",
            "changed_variables": "join trade records to upstream feature states and extract loss-state signature(거래 기록을 상류 피처 상태와 결합해 손실 상태 서명 추출)",
            "sample_scope": "run267CH trade records and reconstructed raw feature surface(267CH 거래 기록과 재구축 원시 피처 표면)",
            "success_criteria": "find a non-calendar signature shared across weak Monday losses(약한 월요일 손실에 공통인 비달력 서명 발견)",
            "failure_criteria": "only weekday literal explains the loss or signature is inconsistent(요일 문자만 손실을 설명하거나 서명이 불일치)",
            "invalid_conditions": "feature leakage or time-axis mismatch(피처 누수 또는 시간축 불일치)",
            "stop_conditions": "one attribution pass; if unclear, record inconclusive and pivot(귀속 1회, 불명확하면 불충분 기록 후 전환)",
            "evidence_plan": "joined feature/trade table, state contrast, leakage check(결합 피처/거래 표, 상태 대조, 누수 점검)",
            "materialization_instruction": "analysis artifact first, not MT5 attempt(먼저 분석 산출물, MT5 시도 아님)",
        },
        {
            "queue_id": "run267cj_q05_s258_stc_stress_comparator_receipt",
            "priority": "P2",
            "workstream": "stress_comparator_prune_receipt(압박 비교 가지치기 영수증)",
            "candidate_aliases": "s258_stc",
            "source_profile": "similar_replacement_impulse",
            "hypothesis": "s258_stc remains useful as a stress comparator, not as a repair target(s258_stc는 수리 대상이 아니라 압박 비교군으로 유용하다)",
            "decision_use": "prevent deep repair loop while preserving stress evidence(깊은 수리 루프를 막고 압박 근거는 보존)",
            "comparison_baseline": "run267CH s258_stc similar_replacement_impulse(267CH s258_stc 유사 대체 임펄스)",
            "control_variables": "no new MT5 attempt unless another structure reopens it(다른 구조가 재개하기 전 새 MT5 시도 없음)",
            "changed_variables": "none; receipt only(없음, 영수증만)",
            "sample_scope": "run267CH evidence only(267CH 근거만)",
            "success_criteria": "stress role is documented without spending repair stages(수리 단계를 쓰지 않고 압박 역할 기록)",
            "failure_criteria": "branch continues because headline net looked high(대표 순수익이 높다는 이유로 분기가 계속됨)",
            "invalid_conditions": "using prune receipt as negative proof of the original candidate(가지치기 영수증을 원 후보 사망 증명으로 사용)",
            "stop_conditions": "reopen only after a different non-calendar structure lowers DD(다른 비달력 구조가 손실폭을 낮춘 뒤에만 재개)",
            "evidence_plan": "failure memory and branch decision rows(실패 기억과 분기 판단 행)",
            "materialization_instruction": "do not materialize MT5 attempt(MT5 시도 물질화 금지)",
        },
    ]


def make_prune_matrix() -> list[dict[str, Any]]:
    return [
        {
            "prune_id": "run267ci_p01_no_headline_candidate_selection",
            "prune_label": "no_headline_selection(대표 숫자 선택 금지)",
            "affected_scope": "all run267CH positive rows(267CH 양수 행 전체)",
            "why_pruned": "positive net does not prove curve quality, Adapter structure, runtime reproduction, or ONNX parity(양수 순수익은 곡선 품질, 어댑터 구조, 런타임 재현, ONNX 동등성을 증명하지 않음)",
            "reopen_condition": "only after materialization, MT5 execution, trade review, Adapter trace, and parity-worthy package(물질화, MT5 실행, 거래 검토, 어댑터 추적, 동등성 가치 패키지 이후)",
        },
        {
            "prune_id": "run267ci_p02_no_calendar_only_monday_filter",
            "prune_label": "no_calendar_only_filter(달력 단독 필터 금지)",
            "affected_scope": "Monday loss cluster(월요일 손실 군집)",
            "why_pruned": "Monday is a symptom; deleting weekdays would not prove market structure(월요일은 증상이며 요일 삭제는 시장 구조를 증명하지 않음)",
            "reopen_condition": "only as state attribution target, not as literal permission rule(문자 허용 규칙이 아니라 상태 귀속 대상으로만 재개)",
        },
        {
            "prune_id": "run267ci_p03_prune_s258_stc_deep_repair_here",
            "prune_label": "stress_only_no_deep_repair(압박 전용, 깊은 수리 없음)",
            "affected_scope": "s258_stc similar_replacement_impulse(s258_stc 유사 대체 임펄스)",
            "why_pruned": "DD 31.65 and Monday -313.09 make it a stress comparator, not a near-term Adapter candidate(손실폭 31.65와 월요일 -313.09로 단기 어댑터 후보가 아니라 압박 비교군)",
            "reopen_condition": "different structure lowers DD without trade-count collapse(다른 구조가 거래 수 붕괴 없이 손실폭을 낮출 때)",
        },
        {
            "prune_id": "run267ci_p04_no_filter_stacking_repair_loop",
            "prune_label": "no_filter_stacking_loop(필터 덧붙이기 루프 금지)",
            "affected_scope": "all follow-up queues(모든 후속 대기열)",
            "why_pruned": "the user goal requires aggressive experiments and feature structure, not defensive stacking only(사용자 목표는 방어적 필터 덧붙이기만이 아니라 공격 실험과 피처 구조를 요구)",
            "reopen_condition": "new feature/state structure is named and traceable(새 피처/상태 구조가 이름 붙고 추적 가능할 때)",
        },
        {
            "prune_id": "run267ci_p05_no_onnx_adapter_claim",
            "prune_label": "no_onnx_or_adapter_claim(ONNX/어댑터 주장 금지)",
            "affected_scope": "run267CI design outputs(267CI 설계 산출물)",
            "why_pruned": "this run designs next experiments only; no model package or parity evidence exists yet(이번 실행은 다음 실험 설계일 뿐 모델 패키지나 동등성 근거 없음)",
            "reopen_condition": "after R&D racing winner, Adapter package, runtime reproduction, and ONNX parity evidence(연구개발 경주 생존자, 어댑터 패키지, 런타임 재현, ONNX 동등성 근거 이후)",
        },
    ]


def make_failure_memory(candidate_rows: Sequence[Mapping[str, Any]], negative_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    monday_rows = [row for row in negative_rows if row.get("axis") == "weekday" and row.get("bucket") == "Monday"]
    impulse_rows = [row for row in candidate_rows if row.get("test_id") == "similar_replacement_impulse"]
    s258 = profile_row(candidate_rows, "s258_stc", "similar_replacement_impulse")
    return [
        {
            "memory_id": "run267ci_m01_impulse_monday_loss_cluster",
            "pattern": "similar impulse raises profit but clusters Monday loss(유사 임펄스는 수익을 올리지만 월요일 손실을 군집시킴)",
            "affected_scope": ";".join(str(row.get("candidate_alias")) for row in monday_rows[:6]),
            "evidence": ";".join(f"{row.get('candidate_alias')}={row.get('net_profit')}" for row in monday_rows[:6]),
            "next_handling": "state attribution before any weekday rule(요일 규칙 전에 상태 귀속)",
        },
        {
            "memory_id": "run267ci_m02_impulse_dd_expansion",
            "pattern": "similar replacement expands trade supply and DD together(유사 대체는 거래 공급과 손실폭을 함께 키움)",
            "affected_scope": "similar_replacement_impulse across pool(후보군 전체 유사 대체 임펄스)",
            "evidence": f"avg_dd={mean(as_float(row.get('report_equity_drawdown_percent')) for row in impulse_rows):.3f};avg_net={mean(as_float(row.get('net_profit')) for row in impulse_rows):.3f}",
            "next_handling": "use DD-shape pressure, not blind expansion(맹목 확장이 아니라 손실폭 형태 압박 사용)",
        },
        {
            "memory_id": "run267ci_m03_s258_stc_stress_only",
            "pattern": "s258_stc headline net hides uncomfortable DD(s258_stc 대표 순수익은 불편한 손실폭을 숨김)",
            "affected_scope": "s258_stc",
            "evidence": f"net={s258.get('net_profit')};dd={s258.get('report_equity_drawdown_percent')};monday={s258.get('weakest_weekday_net')}",
            "next_handling": "stress comparator only until structure changes(구조가 바뀔 때까지 압박 비교군만)",
        },
        {
            "memory_id": "run267ci_m04_duplicate_boundary_not_true_fallback",
            "pattern": "Tier A+B row is duplicate boundary, not true fallback(Tier A+B 행은 실제 대체가 아니라 중복 경계)",
            "affected_scope": "run267CG/run267CH routed_total rows(267CG/267CH 라우팅 전체 행)",
            "evidence": "run267CG tier_pair_boundary says true Tier B fallback remains future work(267CG 티어 경계가 실제 Tier B 대체는 향후 작업이라고 명시)",
            "next_handling": "do not use duplicate rows as route robustness proof(중복 행을 라우트 견고성 증거로 쓰지 않음)",
        },
    ]


def make_experiment_receipts(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [dict(row) for row in queue_rows]


def make_result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267CI follow-up/prune design(267CI 후속/가지치기 설계)",
            "evidence_available": "run267CH candidate_profile_review, candidate_summary, profile_axis_summary, negative_slice_summary(267CH 후보-프로필 검토, 후보 요약, 프로필 축 요약, 음수 구간 요약)",
            "evidence_missing": "new materialized variants, MT5 execution, balance/time-slice review, Adapter package, runtime reproduction, ONNX parity(새 물질화 변형, MT5 실행, 잔액/시간구간 검토, 어댑터 패키지, 런타임 재현, ONNX 동등성)",
            "judgment_label": "exploratory_design_only(탐색 설계 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "This run decides what to try next; it does not pick a candidate(이번 실행은 다음에 무엇을 시험할지 정하며 후보를 고르지 않는다)",
        }
    ]


def artifact_entry(artifact_id: str, artifact_type: str, path: Path, created_at: str, notes: str) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "notes": notes,
    }


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "pool_wide_orthogonal_loss_shape_state_followup_or_prune_design",
            "tier_scope": "Tier A and duplicate-boundary Tier A+B evidence from run267CH(267CH Tier A와 중복 경계 Tier A+B 근거)",
            "scoreboard": "experiment_design_followup_or_prune",
            "status": STATUS,
            "judgment": JUDGMENT,
            "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"branch_decisions={result['branch_decision_count']};queue_rows={result['materialization_queue_count']};prune_rows={result['prune_count']};next_action={NEXT_ACTION};selected_candidate=none.",
        },
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_orthogonal_loss_shape_state_followup_or_prune_design",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "notes": f"Run267CI converts run267CH curve/time-slice evidence to follow-up/prune queue; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__pool_wide_orthogonal_loss_shape_state_followup_or_prune_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "pool_wide_orthogonal_loss_shape_state_followup_or_prune_design",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "followup_or_prune_design",
            "tier_scope": "Tier A and duplicate-boundary Tier A+B run267CH review(267CH Tier A와 중복 경계 Tier A+B 검토)",
            "kpi_scope": "experiment_design_failure_memory_prune",
            "scoreboard_lane": "orthogonal_loss_shape_state_followup_or_prune",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"queue_rows={result['materialization_queue_count']};prune_rows={result['prune_count']}",
            "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": f"Next action: {NEXT_ACTION}.",
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
        artifact_entry("stage267_run267CI_producer", "producer_script", PRODUCER_PATH, created_at, "Builds run267CI follow-up/prune design."),
        artifact_entry("stage267_run267CI_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, created_at, "Source run267CH review result."),
        artifact_entry("stage267_run267CI_branch_decisions", "branch_decisions", BRANCH_DECISION_PATH, created_at, "Run267CI branch decisions."),
        artifact_entry("stage267_run267CI_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, created_at, "Run267CI next materialization queue."),
        artifact_entry("stage267_run267CI_prune_matrix", "prune_matrix", PRUNE_MATRIX_PATH, created_at, "Run267CI prune matrix."),
        artifact_entry("stage267_run267CI_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_PATH, created_at, "Run267CI experiment design receipt."),
        artifact_entry("stage267_run267CI_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, created_at, "Run267CI failure memory."),
        artifact_entry("stage267_run267CI_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, created_at, "Run267CI result judgment."),
        artifact_entry("stage267_run267CI_review_result", "review_result", REVIEW_RESULT_PATH, created_at, "Run267CI review JSON payload."),
        artifact_entry("stage267_run267CI_report", "review_report", REPORT_PATH, created_at, "User-facing run267CI report."),
    )
    rows = read_csv(ARTIFACT_REGISTRY_PATH)
    replace = {row["artifact_id"]: row for row in entries}
    merged = [row for row in rows if row.get("artifact_id") not in replace]
    merged.extend(replace.values())
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"))


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = f"- run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design(267CI 후보군 전체 직교 손실 형태/상태 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    summary_line = (
        "Run267CI(267CI 실행)는 run267CH(267CH 실행)의 curve/time-slice/trade-quality(곡선/시간구간/거래품질) 근거를 "
        f"branch decisions(분기 판단) `{result['branch_decision_count']}`개, materialization queue(물질화 대기열) `{result['materialization_queue_count']}`개, "
        f"prune rows(가지치기 행) `{result['prune_count']}`개로 바꿨다. Effect(효과): headline net(대표 순수익)으로 후보를 고르지 않고, "
        "s264_lc 공격형 통제 후속과 s258_stc 압박 비교 전용 경계를 분리한다."
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_orthogonal_loss_shape_state_followup_or_prune_design`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review.md", report_line)
            text = append_after_contains(text, "Run267CI(267CI 실행)는", summary_line)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review", report_line)
        else:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "stage267_run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review.md", report_line)
        write_md(path, text)

    focus_line = (
        "- >-\n"
        f"  Stage267(267단계) run267CI(267CI 실행) pool-wide orthogonal loss-shape/state follow-up or prune design"
        f"(후보군 전체 직교 손실 형태/상태 후속 또는 가지치기 설계) `{STATUS}`. Effect(효과): run267CH(267CH 실행)의 곡선/시간구간/거래품질 근거를 "
        f"branch decisions(분기 판단) `{result['branch_decision_count']}`개, materialization queue(물질화 대기열) `{result['materialization_queue_count']}`개, "
        f"prune rows(가지치기 행) `{result['prune_count']}`개로 바꿨으며 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), "
        "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace("  status: run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review_completed", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {SOURCE_RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {SOURCE_RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace("  next_action: run267CI_design_pool_wide_orthogonal_loss_shape_state_followup_or_prune", f"  next_action: {NEXT_ACTION}", 1)
    workspace = append_after_contains(
        workspace,
        "run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review_report_path",
        f"  run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design_report_path: {rel(REPORT_PATH)}",
    )
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_line + "\n", 1)
    write_md(WORKSPACE_STATE_PATH, workspace)


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267CI Orthogonal Follow-Up/Prune Design(267단계 267CI 직교 후속/가지치기 설계)",
        "",
        "- action(행동): run267CH(267CH 실행)의 balance/time-slice/trade-quality(잔액/시간구간/거래품질) 검토를 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.",
        "- effect(효과): 수익이 강한 impulse(임펄스) 축을 버리지 않되, DD(drawdown, 손실폭)와 Monday(월요일) 약점을 숨기지 않고 다음 물질화 대기열로 분리한다.",
        f"- status(상태): `{STATUS}`",
        f"- branch_decisions(분기 판단): `{result['branch_decision_count']}`",
        f"- materialization_queue_rows(물질화 대기열 행): `{result['materialization_queue_count']}`",
        f"- prune_rows(가지치기 행): `{result['prune_count']}`",
        f"- failure_memory_rows(실패 기억 행): `{result['failure_memory_count']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "`s264_lc`는 이번 묶음에서 가장 밀어볼 만한 공격형 통제 후속이다. 하지만 그 이유는 selected candidate(선택 후보)라서가 아니라, 높은 순수익과 낮은 전체 DD(drawdown, 손실폭)가 동시에 보였기 때문이다. 월요일과 2024년 12월 약점은 그대로 남아 있으므로 다음 run267CJ(267CJ 실행)에서 비달력 상태 제어로 압박해야 한다.",
        "",
        "`s258_stc`는 숫자는 강해도 손실폭과 월요일 손실이 불편해서 깊은 수리 대상으로 두지 않는다. 이 후보는 stress comparator(압박 비교군)로 남긴다.",
        "",
        "## Branch Decisions(분기 판단)",
        "",
        "| candidate(후보) | best profile(최고 프로필) | net(순수익) | DD%(손실폭) | decision(판단) | next use(다음 용도) |",
        "| --- | --- | ---: | ---: | --- | --- |",
    ]
    for row in result["branch_decisions"]:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['best_profile']}` | {cell(row['best_net_profit'])} | "
            f"{cell(row['best_equity_drawdown_percent'])} | {row['decision_label']} | {row['next_use']} |"
        )
    lines.extend(
        [
            "",
            "## Materialization Queue(물질화 대기열)",
            "",
            "| queue(대기열) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) | success(성공 기준) |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in result["materialization_queue"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['priority']}` | `{row['candidate_aliases']}` | {row['workstream']} | {row['success_criteria']} |"
        )
    lines.extend(
        [
            "",
            "## Prune Matrix(가지치기 행렬)",
            "",
            "| prune(가지치기) | label(라벨) | affected(대상) | reopen(재개 조건) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in result["prune_matrix"]:
        lines.append(f"| `{row['prune_id']}` | {row['prune_label']} | {row['affected_scope']} | {row['reopen_condition']} |")
    lines.extend(
        [
            "",
            "## Result Judgment(결과 판정)",
            "",
            "- result_subject(결과 대상): `run267CI_followup_or_prune_design`.",
            "- judgment_label(판정 라벨): `exploratory_design_only(탐색 설계 전용)`.",
            "- evidence_available(사용 가능 근거): run267CH(267CH 실행) candidate/profile/time-slice(후보/프로필/시간구간) 검토.",
            "- evidence_missing(누락 근거): run267CJ(267CJ 실행) 물질화, MT5(MetaTrader 5, 메타트레이더5) 실행, 새 곡선 검토, Adapter(어댑터) 패키지, runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성).",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- source_review_result(원천 검토 결과): `{rel(SOURCE_REVIEW_RESULT_PATH)}`",
            f"- branch_decisions(분기 판단): `{rel(BRANCH_DECISION_PATH)}`",
            f"- materialization_queue(물질화 대기열): `{rel(MATERIALIZATION_QUEUE_PATH)}`",
            f"- prune_matrix(가지치기 행렬): `{rel(PRUNE_MATRIX_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_PATH)}`",
            f"- review_result(검토 결과): `{rel(REVIEW_RESULT_PATH)}`",
        ]
    )
    return "\n".join(lines)


def build() -> dict[str, Any]:
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    candidate_rows = read_csv(SOURCE_CANDIDATE_REVIEW_PATH)
    summary_rows = read_csv(SOURCE_CANDIDATE_SUMMARY_PATH)
    profile_rows = read_csv(SOURCE_PROFILE_AXIS_PATH)
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    decisions = make_branch_decisions(candidate_rows, summary_rows)
    queue_rows = make_materialization_queue()
    prune_rows = make_prune_matrix()
    failure_rows = make_failure_memory(candidate_rows, negative_rows)
    design_rows = make_experiment_receipts(queue_rows)
    judgment_rows = make_result_judgment()
    result = {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "branch_decision_count": len(decisions),
        "materialization_queue_count": len(queue_rows),
        "prune_count": len(prune_rows),
        "failure_memory_count": len(failure_rows),
        "source_run267CH_trade_records": source_result.get("trade_record_count"),
        "source_run267CH_negative_slices": len(source_result.get("negative_slices", [])),
        "source_profile_axis": profile_rows,
        "branch_decisions": decisions,
        "materialization_queue": queue_rows,
        "prune_matrix": prune_rows,
        "failure_memory": failure_rows,
        "experiment_design_receipt": design_rows,
        "result_judgment": judgment_rows,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "outputs": {
            "branch_decisions": rel(BRANCH_DECISION_PATH),
            "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
            "prune_matrix": rel(PRUNE_MATRIX_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(BRANCH_DECISION_PATH, decisions, BRANCH_DECISION_COLUMNS)
    write_csv(MATERIALIZATION_QUEUE_PATH, queue_rows, QUEUE_COLUMNS)
    write_csv(PRUNE_MATRIX_PATH, prune_rows, PRUNE_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_PATH, design_rows, QUEUE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, failure_rows, FAILURE_MEMORY_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, judgment_rows, RESULT_JUDGMENT_COLUMNS)
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_docs(result)
    return result


def main() -> int:
    result = build()
    print(
        json.dumps(
            {
                "status": result["status"],
                "branch_decisions": result["branch_decision_count"],
                "materialization_queue": result["materialization_queue_count"],
                "prune_rows": result["prune_count"],
                "failure_memory": result["failure_memory_count"],
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
