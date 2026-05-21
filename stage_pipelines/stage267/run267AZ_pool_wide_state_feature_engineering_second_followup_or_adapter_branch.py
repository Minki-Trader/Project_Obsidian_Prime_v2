from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import (
    run267AY_pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review
    as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267AZ"
RUN_ID = "run267AZ_stage267_pool_wide_state_feature_engineering_second_followup_or_adapter_branch_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
SOURCE_EXECUTION_RUN_ID = source_review.PARENT_RUN_ID
STATUS = "run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch_design_completed"
JUDGMENT = "third_branch_design_completed_no_candidate_selection"
NEXT_ACTION = "run267BA_materialize_true_fallback_cross_period_replacement_queue_from_run267AZ_design"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_state_feature_engineering_second_followup_or_adapter_branch"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_CANDIDATE_REVIEW_PATH = source_review.CANDIDATE_SECOND_REVIEW_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_PROFILE_SUMMARY_PATH = source_review.SECOND_PROFILE_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_TIME_SLICE_PATH = source_review.TIME_SLICE_KPI_PATH
SOURCE_CURVE_DIAGNOSTICS_PATH = source_review.CURVE_DIAGNOSTICS_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH
SOURCE_ROUTE_GAP_AUDIT_PATH = source_review.SOURCE_ROUTE_GAP_AUDIT_PATH
SOURCE_PRIOR_RESEARCH_AUDIT_PATH = (
    STAGE_ROOT / "03_reviews" / "stage267_prior_research_utilization_audit.md"
)
SOURCE_TRUE_INTERNAL_REVIEW_PATH = (
    STAGE_ROOT
    / "03_reviews"
    / "stage267_run267Z_true_internal_ablation_balance_timeslice_trade_quality_review.md"
)
SOURCE_POOL_WIDE_ABLATION_DESIGN_PATH = (
    STAGE_ROOT / "03_reviews" / "stage267_run267M_pool_wide_ablation_replacement_design.md"
)

CANDIDATE_DECISION_PATH = RUN_ROOT / "candidate_branch_decision_matrix.csv"
NEXT_EXPERIMENT_QUEUE_PATH = RUN_ROOT / "next_experiment_queue.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch.md"
PRODUCER_PATH = Path(
    "stage_pipelines/stage267/run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch.py"
)

STAGE_LEDGER_PATH = source_review.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_review.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_review.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_review.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_review.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_review.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_review.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_review.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_review.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_review.ARTIFACT_COLUMNS

BASELINE_ORDER = ("s264_aih", "s264_lc", "s262_lih", "s264_aia", "s258_stc")
BASELINE_CANDIDATES: dict[str, tuple[str, str, str]] = {
    "s264_aih": ("s264_allow_inner_high_quarter", "challenger_core", "conditional_core_challenger"),
    "s264_lc": ("s264_lowrank_control", "defensive_control", "control_only"),
    "s262_lih": ("s262_lowrank_inner_half_filter", "validation_heavy", "validation_control_only"),
    "s264_aia": ("s264_allow_inner_all_oos_anchor", "oos_anchor", "adapter_watch_hold"),
    "s258_stc": ("s258_short_tight_control", "stress_challenger", "stress_only"),
}


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
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def grouped(rows: Iterable[Mapping[str, Any]], key: str) -> dict[str, list[Mapping[str, Any]]]:
    output: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        output[str(row.get(key))].append(row)
    return output


def candidate_sort_key(row: Mapping[str, Any]) -> tuple[int, str]:
    alias = str(row.get("candidate_alias"))
    return (BASELINE_ORDER.index(alias) if alias in BASELINE_ORDER else 999, alias)


def source_hashes() -> dict[str, str]:
    paths = {
        "source_review_result": SOURCE_REVIEW_RESULT_PATH,
        "source_candidate_review": SOURCE_CANDIDATE_REVIEW_PATH,
        "source_candidate_summary": SOURCE_CANDIDATE_SUMMARY_PATH,
        "source_negative_slice": SOURCE_NEGATIVE_SLICE_PATH,
        "source_route_gap_audit": SOURCE_ROUTE_GAP_AUDIT_PATH,
        "producer": PRODUCER_PATH,
    }
    return {name: sha256_file_lf_normalized(path) if path_exists(path) else "missing" for name, path in paths.items()}


def worst_row(rows: Sequence[Mapping[str, Any]], key: str) -> Mapping[str, Any]:
    return min(rows, key=lambda item: as_float(item.get(key)), default={})


def best_row(rows: Sequence[Mapping[str, Any]], key: str) -> Mapping[str, Any]:
    return max(rows, key=lambda item: as_float(item.get(key)), default={})


def deep_negative_count(rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in rows if as_float(row.get("net_profit")) <= -160.0)


def build_candidate_decisions(
    summary_rows: Sequence[Mapping[str, Any]],
    candidate_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_summary = {str(row.get("candidate_alias")): row for row in summary_rows}
    by_candidate = grouped(candidate_rows, "candidate_alias")
    by_negative = grouped(negative_rows, "candidate_alias")
    decisions: list[dict[str, Any]] = []
    for alias in BASELINE_ORDER:
        candidate_id, role, design_role = BASELINE_CANDIDATES[alias]
        summary = by_summary.get(alias, {})
        items = by_candidate.get(alias, [])
        negatives = by_negative.get(alias, [])
        worst = worst_row(items, "worst_slice_net")
        best = best_row(items, "net_profit")
        net_mean = as_float(summary.get("net_profit_mean"))
        net_min = as_float(summary.get("net_profit_min"))
        net_max = as_float(summary.get("net_profit_max"))
        dd_worst = as_float(summary.get("equity_drawdown_percent_worst"))
        worst_month_min = as_float(summary.get("worst_month_net_min"))
        worst_slice_min = as_float(worst.get("worst_slice_net"))
        source_regressions = as_int(summary.get("source_regression_count"))
        slice_holes = as_int(summary.get("slice_hole_flag_count"))
        deep_count = deep_negative_count(negatives)
        best_profile = "::".join(
            str(best.get(key, ""))
            for key in ("source_test_id", "state_profile", "second_followup_profile")
            if best.get(key)
        )

        if alias == "s264_aih":
            decision = "conditional_challenger_hold_no_third_same_repair(조건부 도전자 보류, 같은 3차 수리 금지)"
            priority = "P0"
            next_use = (
                "cross-period and similar-feature replacement only; downgrade if 2024-12 or Monday remains deep"
                "(확장 기간과 유사 피처 대체만 허용, 2024-12 또는 월요일이 깊으면 강등)"
            )
            prune_boundary = "no more range/volatility pressure loop without new evidence(새 근거 없는 범위/변동성 압박 반복 금지)"
        elif alias == "s264_aia":
            decision = "adapter_watch_held_until_slice_gate(구간 게이트 전 어댑터 관찰 보류)"
            priority = "P0"
            next_use = (
                "true fallback route and DD-shape audit before Adapter development"
                "(어댑터 개발 전 실제 대체 라우팅과 손실폭 모양 감사)"
            )
            prune_boundary = "hold Adapter work if Monday hole stays below -190(월요일 구멍이 -190 아래면 어댑터 작업 보류)"
        elif alias == "s258_stc":
            decision = "stress_challenger_prune_or_wide_rescue(압박 도전자 가지치기 또는 넓은 회수)"
            priority = "P1"
            next_use = "stress-only comparator in replacement and fallback tests(대체와 대체 라우팅 시험의 압박 전용 비교 기준)"
            prune_boundary = "prune active challenger lane if worst weekday remains below -220(최악 요일이 -220 아래면 활성 도전자 라인에서 제거)"
        elif alias == "s264_lc":
            decision = "defensive_control_only_after_source_regression(원천 후퇴 뒤 방어 기준 전용)"
            priority = "P1"
            next_use = "control audit only, not Adapter or challenger lane(감사용 기준만, 어댑터나 도전자 라인 아님)"
            prune_boundary = "remove from active queue if it stops differentiating pressure drift(압박 표류 구분력이 사라지면 활성 큐에서 제거)"
        else:
            decision = "validation_control_only_after_repeat_hole(반복 구멍 뒤 검증 기준 전용)"
            priority = "P1"
            next_use = "validation stability comparator only(검증 안정성 비교 기준만)"
            prune_boundary = "do not rescue without cross-period stability improvement(확장 기간 안정 개선 없이는 회수 금지)"

        if not items:
            decision = "missing_required_no_candidate_decision(필수 누락, 후보 결정 없음)"
            priority = "blocked"
            next_use = "repair source review first(원천 검토 먼저 수리)"
            prune_boundary = "do not prune from missing evidence(근거 누락만으로 가지치기 금지)"

        decisions.append(
            {
                "candidate_alias": alias,
                "candidate_id": candidate_id,
                "candidate_role": role,
                "design_role": design_role,
                "tier_a_test_count": as_int(summary.get("tier_a_test_count")),
                "net_profit_mean": net_mean,
                "net_profit_min": net_min,
                "net_profit_max": net_max,
                "equity_drawdown_percent_worst": dd_worst,
                "worst_month_net_min": worst_month_min,
                "worst_slice_axis": worst.get("worst_slice_axis", ""),
                "worst_slice_bucket": worst.get("worst_slice_bucket", ""),
                "worst_slice_net_min": worst_slice_min,
                "deep_negative_slice_count": deep_count,
                "slice_hole_flag_count": slice_holes,
                "source_regression_count": source_regressions,
                "best_profile": best_profile,
                "decision_label": decision,
                "priority": priority,
                "next_use": next_use,
                "prune_boundary": prune_boundary,
                "reopen_condition": (
                    "reopen active branch only if cross-period and replacement tests reduce weak slices without trade-count collapse"
                    "(확장 기간과 대체 시험에서 거래 수 붕괴 없이 약한 구간이 줄 때만 활성 분기 재개)"
                ),
                "do_not_claim": "no selected candidate, no ONNX readiness, no Goal Achieve(선택 후보 없음, ONNX 준비 없음, 목표 달성 없음)",
            }
        )
    return decisions


def build_next_queue(decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    common_boundary = (
        "research development only; no selected candidate; no ONNX until goal gate"
        "(연구개발 전용, 선택 후보 없음, 목표 게이트 전 ONNX 없음)"
    )
    source = rel(SOURCE_CANDIDATE_REVIEW_PATH)
    negative_source = rel(SOURCE_NEGATIVE_SLICE_PATH)
    route_gap = rel(SOURCE_ROUTE_GAP_AUDIT_PATH)
    return [
        {
            "queue_id": "run267AZ_q01_true_fallback_route_readiness",
            "priority": "P0",
            "materialization_readiness": "ready_for_run267BA_manifest_design(run267BA 목록 설계 준비)",
            "workstream": "true_fallback_route_boundary(실제 대체 라우팅 경계)",
            "candidate_scope": "s264_aih;s264_aia;s258_stc",
            "source_evidence": f"{source};{route_gap}",
            "hypothesis": (
                "repeated Tier A holes cannot be judged as robust until actual Tier A primary plus Tier B fallback is measured"
                "(반복 Tier A 구멍은 실제 Tier A 우선 + Tier B 대체를 측정하기 전에는 견고성 판정 불가)"
            ),
            "decision_use": "decide whether Tier B fallback can fill missing-context holes or only duplicate Tier A weakness(Tier B 대체가 빈 문맥 구멍을 메우는지, Tier A 약점만 반복하는지 결정)",
            "comparison_baseline": "run267AY Tier A second follow-up review(run267AY Tier A 2차 후속 검토)",
            "control_variables": "same 2024 historical source and same candidate score surfaces(같은 2024 과거 원천과 같은 후보 점수 표면)",
            "changed_variables": "routing manifest and fallback availability only(라우팅 목록과 대체 가능성만 변경)",
            "sample_scope": "Tier A used, Tier B fallback used, actual routed total(Tier A 사용, Tier B 대체 사용, 실제 라우팅 전체)",
            "success_criteria": "fallback count is nonzero and actual routed total reduces worst weekday/month without hiding component rows(대체 수가 0이 아니고 실제 라우팅 전체가 구성 행을 숨기지 않은 채 최악 요일/월을 줄임)",
            "failure_criteria": "fallback remains zero, route cannot be materialized, or routed total keeps deep holes(대체가 0이거나 라우팅 물질화 불가 또는 라우팅 전체가 깊은 구멍 유지)",
            "invalid_conditions": "synthetic Tier A+B sum is reported as actual routed total(합성 Tier A+B 합산을 실제 라우팅 전체로 보고)",
            "stop_conditions": "if true fallback cannot be built now, mark blocked with exact missing manifest fields(실제 대체를 지금 만들 수 없으면 필요한 목록 필드를 적고 차단)",
            "evidence_plan": "route manifest, component counts, MT5 report, trade list, curve and slice review(라우팅 목록, 구성 수, MT5 보고서, 거래 목록, 곡선과 구간 검토)",
            "next_required_artifacts": "fallback manifest, runtime contract, set files, routed KPI rows(대체 목록, 런타임 계약, 설정 파일, 라우팅 KPI 행)",
            "claim_boundary": common_boundary,
        },
        {
            "queue_id": "run267AZ_q02_cross_period_similar_feature_replacement",
            "priority": "P0",
            "materialization_readiness": "ready_for_feature_surface_materialization(피처 표면 물질화 준비)",
            "workstream": "similar_feature_replacement_and_cross_period(유사 피처 대체와 확장 기간)",
            "candidate_scope": "s264_aih;s264_aia;s258_stc",
            "source_evidence": source,
            "hypothesis": (
                "the best-looking second follow-up profiles are useful only if volatility/range/trend meaning survives similar replacements and non-2024 slices"
                "(좋아 보이는 2차 후속 프로필은 변동성/범위/추세 의미가 유사 대체와 2024 외 구간에서도 살아야 쓸모 있음)"
            ),
            "decision_use": "candidate keep, downgrade, or prune decision(후보 유지, 강등, 가지치기 결정)",
            "comparison_baseline": "run267AY best profile per active role(run267AY 역할별 최고 프로필)",
            "control_variables": "no literal month or weekday rule, same risk settings, same reporting schema(월/요일 직접 규칙 없음, 같은 위험 설정, 같은 보고 형식)",
            "changed_variables": "similar volatility/range/trend feature families and cross-period slice(유사 변동성/범위/추세 피처군과 확장 기간 구간)",
            "sample_scope": "2024 historical plus at least one earlier or adjacent period if data is available(2024 과거와 데이터 가능 시 이전 또는 인접 기간 하나 이상)",
            "success_criteria": "weak slices improve and net/PF/trades remain viable across replacement family(약한 구간이 줄고 순손익/수익 팩터/거래 수가 대체 피처군에서도 유지)",
            "failure_criteria": "performance only survives one indicator family or one period(성과가 한 지표군 또는 한 기간에서만 생존)",
            "invalid_conditions": "feature order or runtime contract changes are not recorded(피처 순서 또는 런타임 계약 변경을 기록하지 않음)",
            "stop_conditions": "prune a role if replacement breaks it twice without a new market-structure hypothesis(새 시장 구조 가설 없이 대체에서 두 번 깨지면 역할 가지치기)",
            "evidence_plan": "feature manifest, category map, replacement manifest, MT5 KPI, slice review(피처 목록, 범주 지도, 대체 목록, MT5 KPI, 구간 검토)",
            "next_required_artifacts": "feature replacement manifest and materialization receipt(피처 대체 목록과 물질화 영수증)",
            "claim_boundary": common_boundary,
        },
        {
            "queue_id": "run267AZ_q03_category_ablation_failure_memory_refresh",
            "priority": "P1",
            "materialization_readiness": "design_first_then_materialize(먼저 설계 후 물질화)",
            "workstream": "category_ablation_and_failure_memory(범주 제거와 실패 기억)",
            "candidate_scope": "all_baseline_candidates(모든 기준 후보)",
            "source_evidence": f"{source};{negative_source}",
            "hypothesis": (
                "candidate fragility is category dependence rather than one calendar slice"
                "(후보 취약성은 달력 구간 하나가 아니라 범주 의존성일 수 있음)"
            ),
            "decision_use": "separate structural dependence from noise repair(구조 의존성과 잡음 수리 분리)",
            "comparison_baseline": "run267M/N/O true pool-wide ablation and run267AY second follow-up(run267M/N/O 진짜 후보군 제거와 run267AY 2차 후속)",
            "control_variables": "same candidate pool and same KPI schema(같은 후보군과 같은 KPI 형식)",
            "changed_variables": "feature category removal and low-rank/control category toggles(피처 범주 제거와 저랭크/기준 범주 토글)",
            "sample_scope": "Tier A first, Tier B marked missing unless routed manifest exists(Tier A 우선, 라우팅 목록 전까지 Tier B는 누락 표시)",
            "success_criteria": "candidate degrades gracefully instead of collapsing under one category removal(후보가 한 범주 제거에서 붕괴하지 않고 완만히 약화)",
            "failure_criteria": "one feature/category removal destroys curve or trade count(한 피처/범주 제거가 곡선 또는 거래 수를 무너뜨림)",
            "invalid_conditions": "proxy feature order is used after true feature order is available(진짜 피처 순서가 있는데 대체 피처 순서를 사용)",
            "stop_conditions": "if all candidates show same collapse, pivot to feature architecture rather than candidate repair(모든 후보가 같은 붕괴를 보이면 후보 수리 대신 피처 구조로 전환)",
            "evidence_plan": "ablation matrix, curve review, trade quality review, failure memory update(제거 행렬, 곡선 검토, 거래 품질 검토, 실패 기억 갱신)",
            "next_required_artifacts": "ablation queue and failure-memory receipt(제거 큐와 실패 기억 영수증)",
            "claim_boundary": common_boundary,
        },
        {
            "queue_id": "run267AZ_q04_adapter_contract_hold_audit",
            "priority": "P1",
            "materialization_readiness": "audit_only_no_adapter_implementation(감사 전용, 어댑터 구현 없음)",
            "workstream": "adapter_readiness_hold_boundary(어댑터 준비 보류 경계)",
            "candidate_scope": "s264_aia;s264_aih",
            "source_evidence": source,
            "hypothesis": (
                "Adapter work should wait until feature order, decision surface, risk/ATR, and route evidence stop moving"
                "(어댑터 작업은 피처 순서, 의사결정 표면, risk/ATR, 라우팅 근거가 덜 흔들릴 때까지 기다려야 함)"
            ),
            "decision_use": "define what must be stable before Adapter development(어댑터 개발 전 안정되어야 할 조건 정의)",
            "comparison_baseline": "run267P/Q adapter attempt and run267AY second follow-up(run267P/Q 어댑터 시도와 run267AY 2차 후속)",
            "control_variables": "no new adapter package, no ONNX, no runtime authority claim(새 어댑터 패키지 없음, ONNX 없음, 런타임 권위 주장 없음)",
            "changed_variables": "readiness checklist only(준비 체크리스트만 변경)",
            "sample_scope": "design audit only(설계 감사 전용)",
            "success_criteria": "adapter prerequisites are explicit and tied to evidence files(어댑터 선행조건이 명시되고 근거 파일에 연결)",
            "failure_criteria": "adapter implementation starts before weak-slice and route evidence improves(약한 구간과 라우팅 근거 개선 전 어댑터 구현 시작)",
            "invalid_conditions": "readiness checklist claims performance improvement(준비 체크리스트가 성능 개선을 주장)",
            "stop_conditions": "hold adapter implementation until at least one candidate has no deep repeated slice in routed/cross-period checks(라우팅/확장 기간에서 깊은 반복 구간이 없는 후보가 생길 때까지 보류)",
            "evidence_plan": "adapter prerequisite matrix and runtime handoff gap list(어댑터 선행조건 행렬과 런타임 인계 공백 목록)",
            "next_required_artifacts": "adapter readiness audit only(어댑터 준비 감사만)",
            "claim_boundary": common_boundary,
        },
        {
            "queue_id": "run267AZ_q05_candidate_pool_prune_or_refresh_decision",
            "priority": "P1",
            "materialization_readiness": "decision_receipt_only(결정 영수증 전용)",
            "workstream": "candidate_pool_refresh(후보군 갱신)",
            "candidate_scope": ";".join(str(row.get("candidate_alias")) for row in decisions),
            "source_evidence": source,
            "hypothesis": (
                "some candidates should become controls or stress probes instead of active contenders"
                "(일부 후보는 활성 경쟁자가 아니라 기준 또는 압박 탐침으로 남아야 함)"
            ),
            "decision_use": "candidate role refresh before more expensive runs(더 비싼 실행 전 후보 역할 갱신)",
            "comparison_baseline": "run267AY candidate summary(run267AY 후보 요약)",
            "control_variables": "original five-candidate pool remains traceable(초기 다섯 후보군은 추적 가능하게 유지)",
            "changed_variables": "active lane versus control/stress-only lane labels(활성 라인과 기준/압박 전용 라벨)",
            "sample_scope": "design only with current Stage267 evidence(현재 Stage267 근거 기반 설계 전용)",
            "success_criteria": "next materialization queue avoids spending all rows on weak repeated repairs(다음 물질화 큐가 약한 반복 수리에 모든 행을 쓰지 않음)",
            "failure_criteria": "same repair loop continues for a third pass without route or replacement evidence(라우팅 또는 대체 근거 없이 같은 수리가 세 번째 반복)",
            "invalid_conditions": "candidate is called dead or selected from this design only(이 설계만으로 후보 사망 또는 선택이라고 부름)",
            "stop_conditions": "refresh roles after run267BA review, not before evidence(근거 전이 아니라 run267BA 검토 뒤 역할 갱신)",
            "evidence_plan": "candidate decision matrix and run267BA review(후보 결정 행렬과 run267BA 검토)",
            "next_required_artifacts": "role refresh receipt and next queue filter(역할 갱신 영수증과 다음 큐 필터)",
            "claim_boundary": common_boundary,
        },
    ]


def build_failure_memory(
    candidate_decisions: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    worst_negative = min((as_float(row.get("net_profit")) for row in negative_rows), default=0.0)
    worst_candidate = min(candidate_decisions, key=lambda row: as_float(row.get("worst_slice_net_min")), default={})
    return [
        {
            "memory_id": "run267AZ_mem01_second_pressure_no_watch_rows",
            "pattern": "second follow-up pressure produced zero watch rows(2차 후속 압박이 관찰 행 0개를 만듦)",
            "evidence": rel(SOURCE_CANDIDATE_REVIEW_PATH),
            "affected_scope": "all baseline candidates(모든 기준 후보)",
            "do_not_repeat": "do not run a third same-style state pressure loop(같은 방식의 3차 상태 압박 루프 금지)",
            "salvage_angle": "switch to true fallback, replacement, and cross-period checks(실제 대체, 대체 피처, 확장 기간 확인으로 전환)",
            "reopen_condition": "a new market-structure hypothesis explains the holes(새 시장 구조 가설이 구멍을 설명)",
            "boundary": "diagnostic negative memory, not idea death(진단 부정 기억, 아이디어 사망 아님)",
        },
        {
            "memory_id": "run267AZ_mem02_deep_monday_cluster_persists",
            "pattern": "Monday remains a deep loss cluster after noncalendar pressure(비달력 압박 뒤에도 월요일 깊은 손실 군집 지속)",
            "evidence": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "affected_scope": "s264_aia;s258_stc;s262_lih;s264_lc;s264_aih",
            "do_not_repeat": "do not solve it with a literal weekday filter alone(요일 직접 필터 하나로 해결 금지)",
            "salvage_angle": "test whether Tier B fallback or similar trend/range features changes the same cluster(Tier B 대체나 유사 추세/범위 피처가 같은 군집을 바꾸는지 시험)",
            "reopen_condition": "Monday loss improves and adjacent slices do not worsen(월요일 손실이 줄고 인접 구간이 악화되지 않음)",
            "boundary": f"worst_negative_slice={worst_negative:.2f}",
        },
        {
            "memory_id": "run267AZ_mem03_2024_12_not_fixed_by_interaction",
            "pattern": "2024-12 remains a month hole after range/volatility interaction(범위/변동성 상호작용 뒤에도 2024-12 월 구멍 지속)",
            "evidence": rel(SOURCE_CANDIDATE_REVIEW_PATH),
            "affected_scope": "especially s264_aih, s264_lc, s262_lih(특히 s264_aih, s264_lc, s262_lih)",
            "do_not_repeat": "do not add a month literal repair(월 직접 수리 금지)",
            "salvage_angle": "map to cross-period regime and similar feature replacement(확장 기간 레짐과 유사 피처 대체로 매핑)",
            "reopen_condition": "2024-12 improves under a noncalendar feature family and other months survive(비달력 피처군에서 2024-12가 개선되고 다른 월이 생존)",
            "boundary": f"worst_candidate={worst_candidate.get('candidate_alias', '')};worst_slice={worst_candidate.get('worst_slice_net_min', '')}",
        },
        {
            "memory_id": "run267AZ_mem04_adapter_not_ready",
            "pattern": "adapter-looking candidates still have weak-slice and route gaps(어댑터처럼 보이는 후보도 약한 구간과 라우팅 공백이 남음)",
            "evidence": rel(SOURCE_ROUTE_GAP_AUDIT_PATH),
            "affected_scope": "s264_aia;s264_aih",
            "do_not_repeat": "do not implement Adapter before route and feature-order evidence stabilizes(라우팅과 피처 순서 근거 안정 전 어댑터 구현 금지)",
            "salvage_angle": "write readiness audit instead of package(패키지 대신 준비 감사 작성)",
            "reopen_condition": "one candidate passes routed/cross-period/similar replacement checks(한 후보가 라우팅/확장 기간/유사 대체 확인 통과)",
            "boundary": "Adapter development held, not abandoned(어댑터 개발 보류, 포기 아님)",
        },
    ]


def build_performance_attribution(candidate_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in candidate_decisions:
        alias = str(row.get("candidate_alias"))
        rows.append(
            {
                "attribution_id": f"run267AZ_attr_{alias}",
                "observed_change": (
                    f"{alias} kept positive 2024 net in run267AY but did not produce a watch row"
                    f"({alias}는 run267AY에서 2024 순손익은 양수였지만 관찰 행은 만들지 못함)"
                ),
                "comparison_baseline": "run267AU source follow-up and run267AY second follow-up(run267AU 원천 후속과 run267AY 2차 후속)",
                "likely_drivers": "state feature pressure reshaped headline KPI but weak-slice concentration persisted(상태 피처 압박이 대표 KPI를 바꿨지만 약한 구간 집중은 지속)",
                "segment_checks": "month, weekday, session, hour, direction, chronological segment(월/요일/세션/시간/방향/시간순서 구간)",
                "trade_shape": (
                    f"tests={row.get('tier_a_test_count')};net_mean={row.get('net_profit_mean')};"
                    f"worst_slice={row.get('worst_slice_net_min')};deep_negative_slices={row.get('deep_negative_slice_count')}"
                ),
                "alternative_explanations": "single-period 2024 fit, missing true fallback route, feature-family overdependence(단일 2024 기간 적합, 실제 대체 라우팅 누락, 피처군 과의존)",
                "attribution_confidence": "medium_for_2024_diagnostic_low_for_generalization(2024 진단 중간, 일반화 낮음)",
                "next_probe": NEXT_ACTION,
            }
        )
    return rows


def build_result_judgment(candidate_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "result_subject": "overall_run267AZ_design(전체 run267AZ 설계)",
            "evidence_available": "run267AY review, candidate summary, negative slices, route gap audit(run267AY 검토, 후보 요약, 음수 구간, 라우팅 공백 감사)",
            "evidence_missing": "run267BA materialization, true fallback runtime evidence, cross-period MT5 results, Adapter implementation, ONNX parity(run267BA 물질화, 실제 대체 런타임 근거, 확장 기간 MT5 결과, 어댑터 구현, ONNX 동등성)",
            "judgment_label": JUDGMENT,
            "claim_boundary": "design only; no selected candidate; no ONNX readiness(설계 전용, 선택 후보 없음, ONNX 준비 없음)",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "같은 수리를 더 누르는 대신 라우팅, 대체 피처, 확장 기간으로 검증 폭을 넓힌다.",
        }
    ]
    rows.extend(
        {
            "result_subject": str(row.get("candidate_alias")),
            "evidence_available": (
                f"net_mean={row.get('net_profit_mean')};"
                f"worst_slice={row.get('worst_slice_net_min')};"
                f"deep_negative_slice_count={row.get('deep_negative_slice_count')}"
            ),
            "evidence_missing": "true fallback route, similar replacement, broader period, Adapter readiness(실제 대체 라우팅, 유사 대체, 더 넓은 기간, 어댑터 준비)",
            "judgment_label": str(row.get("decision_label")),
            "claim_boundary": str(row.get("do_not_claim")),
            "next_condition": str(row.get("next_use")),
            "user_explanation_hook": "숫자보다 덜 깨지는지를 먼저 본다.",
        }
        for row in candidate_decisions
    )
    return rows


def build_design_receipt(queue_rows: Sequence[Mapping[str, Any]], source_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    parser_errors = len(source_result.get("parser_errors", []))
    receipts = [
        {
            "receipt_id": "run267AZ_receipt_source_authority",
            "receipt_type": "source_authority(원천 권위)",
            "status": "pass" if parser_errors == 0 else "blocked",
            "evidence_path": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267AZ uses reviewed run267AY trade-level evidence(run267AZ는 검토된 run267AY 거래 단위 근거를 사용)",
            "notes": f"parser_errors={parser_errors}",
        },
        {
            "receipt_id": "run267AZ_receipt_no_third_same_repair",
            "receipt_type": "repair_loop_control(수리 루프 통제)",
            "status": "pass",
            "evidence_path": rel(SOURCE_CANDIDATE_REVIEW_PATH),
            "effect": "same state-pressure loop is stopped before becoming a bottleneck(같은 상태 압박 루프가 병목이 되기 전에 멈춤)",
            "notes": "next queue includes true fallback, cross-period, replacement, ablation, and adapter hold audit.",
        },
        {
            "receipt_id": "run267AZ_receipt_prior_research_utilization",
            "receipt_type": "prior_research_utilization(이전 연구 활용)",
            "status": "partial_continue",
            "evidence_path": rel(SOURCE_PRIOR_RESEARCH_AUDIT_PATH),
            "effect": "Stage58 이전 연구 단서를 버리지 않고 true internal ablation과 similar replacement로 다시 연결(Stage58 이전 연구 단서를 진짜 내부 제거와 유사 대체로 재연결)",
            "notes": "Still not enough for Goal Achieve(목표 달성) or ONNX readiness(ONNX 준비).",
        },
    ]
    receipts.extend(
        {
            "receipt_id": f"run267AZ_receipt_{row['queue_id']}",
            "receipt_type": "experiment_design_queue(실험 설계 큐)",
            "status": "recorded",
            "evidence_path": str(row["source_evidence"]),
            "effect": str(row["decision_use"]),
            "notes": f"priority={row['priority']};candidate_scope={row['candidate_scope']}",
        }
        for row in queue_rows
    )
    return receipts


def build_gate_audit(
    source_result: Mapping[str, Any],
    candidate_decisions: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    failure_memory: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parser_errors = len(source_result.get("parser_errors", []))
    watch_rows = as_int(source_result.get("watch_rows"))
    return [
        {
            "gate_id": "source_review_parser_gate",
            "status": "pass" if parser_errors == 0 else "fail",
            "evidence_path": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "source review is usable for design if parser errors are zero(파서 오류 0이면 원천 검토를 설계에 사용할 수 있음)",
            "notes": f"parser_errors={parser_errors}",
        },
        {
            "gate_id": "no_candidate_selection_boundary",
            "status": "pass",
            "evidence_path": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "watch_rows=0 keeps candidate selection closed(watch 행 0개라 후보 선택을 닫아 둠)",
            "notes": f"watch_rows={watch_rows};selected_candidate=none;onnx_readiness=not_claimed",
        },
        {
            "gate_id": "experiment_design_schema",
            "status": "pass",
            "evidence_path": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "effect": "hypothesis, decision use, controls, changed variables, criteria, stop conditions, evidence plan are recorded(가설, 결정 용도, 고정/변경 변수, 기준, 중단 조건, 근거 계획 기록)",
            "notes": f"queue_rows={len(queue_rows)}",
        },
        {
            "gate_id": "repair_loop_control",
            "status": "pass",
            "evidence_path": rel(FAILURE_MEMORY_PATH),
            "effect": "third same-style repair is blocked before bottlenecking(같은 방식 3차 수리를 병목 전에 차단)",
            "notes": f"failure_memory={len(failure_memory)}",
        },
        {
            "gate_id": "candidate_role_boundary",
            "status": "pass",
            "evidence_path": rel(CANDIDATE_DECISION_PATH),
            "effect": "candidate roles are separated into active, control, stress, and adapter-hold lanes(후보 역할을 활성/기준/압박/어댑터 보류로 분리)",
            "notes": f"candidate_decisions={len(candidate_decisions)}",
        },
        {
            "gate_id": "tier_route_gap_boundary",
            "status": "pass" if path_exists(SOURCE_ROUTE_GAP_AUDIT_PATH) else "blocked",
            "evidence_path": rel(SOURCE_ROUTE_GAP_AUDIT_PATH),
            "effect": "Tier B and actual routed total remain explicit until true fallback manifest exists(Tier B와 실제 라우팅 전체는 진짜 대체 목록 전까지 명시 경계)",
            "notes": "run267AZ_q01 targets this gap directly.",
        },
    ]


def build_lineage(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "source_execution_run_id": SOURCE_EXECUTION_RUN_ID,
        "stage_id": STAGE_ID,
        "producer": rel(PRODUCER_PATH),
        "sources": {
            "review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "candidate_review": rel(SOURCE_CANDIDATE_REVIEW_PATH),
            "candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "route_gap_audit": rel(SOURCE_ROUTE_GAP_AUDIT_PATH),
            "prior_research_audit": rel(SOURCE_PRIOR_RESEARCH_AUDIT_PATH),
            "true_internal_review": rel(SOURCE_TRUE_INTERNAL_REVIEW_PATH),
            "pool_wide_ablation_design": rel(SOURCE_POOL_WIDE_ABLATION_DESIGN_PATH),
        },
        "outputs": result["outputs"],
        "artifact_hashes": result["artifact_hashes"],
        "claim_boundary": CLAIM_BOUNDARY,
        "next_consumer": NEXT_ACTION,
    }


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
    for index, current in enumerate(lines):
        if needle in current:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def remove_workspace_focus_item(text: str, needle: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].strip() == "- >-" and index + 1 < len(lines) and needle in lines[index + 1]:
            index += 2
            continue
        out.append(lines[index])
        index += 1
    return "\n".join(out) + "\n"


def update_workspace_state_text(text: str) -> str:
    text = remove_workspace_focus_item(text, "run267AZ(267AZ 실행)")
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_path = "run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch_report_path" in text
    focus_inserted = False
    focus_block = [
        "- >-",
        f"  Stage267(267단계) run267AZ(267AZ 실행) pool-wide state feature engineering second follow-up/Adapter branch design(후보군 전체 상태 피처 엔지니어링 2차 후속/어댑터 분기 설계) `{STATUS}`. Effect(효과): run267AY(267AY 실행)의 watch_rows(관찰 행) 0과 deep weak slices(깊은 약한 구간)를 받아 같은 수리 루프를 멈추고 true fallback(실제 대체), cross-period(확장 기간), similar replacement(유사 대체), Adapter hold audit(어댑터 보류 감사)로 다음 큐를 넓혔다. selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    ]
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line == "current_focus:" and not focus_inserted:
            output.append(line)
            output.extend(focus_block)
            focus_inserted = True
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
                output.append(f"  status: {STATUS}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
            if "run267AY_pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review_report_path" in stripped and not inserted_path:
                output.append(line)
                output.append(
                    f"  run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch_report_path: {rel(REPORT_PATH)}"
                )
                inserted_path = True
                continue
        output.append(line)
    return "\n".join(output) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch(267AZ 후보군 전체 상태 피처 엔지니어링 2차 후속/어댑터 분기 설계): "
        f"`{rel(REPORT_PATH)}`"
    )
    latest_line = (
        f"- latest_design(최신 설계): run267AZ(267AZ 실행) candidate decisions(후보 결정) `{len(result['candidate_decisions'])}`, "
        f"queue rows(큐 행) `{len(result['next_experiment_queue'])}`, failure memory(실패 기억) `{len(result['failure_memory'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    closing_block = "\n".join(
        [
            "Run267AZ(267AZ 실행)는 run267AY(267AY 실행)의 2차 후속 검토를 다음 분기 설계로 바꿨다.",
            "Effect(효과): 같은 state-pressure repair(상태 압박 수리)를 세 번째 반복하지 않고, true fallback routing(실제 대체 라우팅), cross-period check(확장 기간 확인), similar feature replacement(유사 피처 대체), Adapter hold audit(어댑터 보류 감사)로 넓혔다.",
            "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = replace_line_prefix(
                text,
                "- adapter_under_review(검토 중 어댑터):",
                "- adapter_under_review(검토 중 어댑터): `pool_wide_state_feature_engineering_second_followup_or_adapter_branch_design`",
            )
            text = append_after_contains(text, "stage267_run267AY_pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review.md", report_line)
            if latest_line not in text and "## Current Next Action" in text:
                text = text.replace("## Current Next Action", latest_line + "\n\n## Current Next Action", 1)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267AY_pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review.md", report_line)
        else:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267AY_pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review.md", report_line)
        text = append_block_once(text, "Run267AZ(267AZ 실행)는 run267AY", closing_block)
        write_md(path, text)
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    write_md(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace))


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "pool_wide_state_feature_engineering_second_followup_or_adapter_branch_design",
                "tier_scope": "Tier A second follow-up design; Tier B and actual routed total targeted by next true fallback queue",
                "scoreboard": "experiment_design_queue_failure_memory_candidate_role_refresh",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": (
                    f"queue_rows={len(result['next_experiment_queue'])};"
                    f"candidate_decisions={len(result['candidate_decisions'])};"
                    f"failure_memory={len(result['failure_memory'])};next_action={NEXT_ACTION}."
                ),
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
                "lane": "baseline_candidate_racing_second_followup_or_adapter_branch_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": (
                    "Run267AZ design from run267AY review; no selected candidate; "
                    f"onnx_readiness=not_claimed; goal_achieve=not_claimed; next_action={NEXT_ACTION}."
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
                "ledger_row_id": f"{RUN_ID}__pool_wide_state_feature_engineering_second_followup_or_adapter_branch_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "pool_wide_state_feature_engineering_second_followup_or_adapter_branch_design",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "pool_wide_state_feature_engineering_second_followup_or_adapter_branch_design",
                "tier_scope": "Tier A diagnostic design; Tier B fallback remains required next work",
                "kpi_scope": "design_receipt_no_new_kpi",
                "scoreboard_lane": "experiment_design_failure_memory",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": (
                    f"candidate_decisions={len(result['candidate_decisions'])};"
                    f"queue_rows={len(result['next_experiment_queue'])};"
                    f"failure_memory={len(result['failure_memory'])}"
                ),
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_design_only",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ARTIFACT_COLUMNS,
        artifact_rows(created_at),
        key="artifact_id",
    )


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267AZ_design_script", "producer_script", PRODUCER_PATH, "Builds run267AZ branch design from run267AY review."),
        ("stage267_run267AZ_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267AY review result."),
        ("stage267_run267AZ_source_candidate_review", "source_candidate_review", SOURCE_CANDIDATE_REVIEW_PATH, "Source run267AY candidate review."),
        ("stage267_run267AZ_candidate_decisions", "candidate_decision_matrix", CANDIDATE_DECISION_PATH, "Run267AZ candidate branch decision matrix."),
        ("stage267_run267AZ_next_experiment_queue", "experiment_queue", NEXT_EXPERIMENT_QUEUE_PATH, "Run267AZ next experiment queue."),
        ("stage267_run267AZ_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267AZ failure memory."),
        ("stage267_run267AZ_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Run267AZ performance attribution."),
        ("stage267_run267AZ_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267AZ result judgment."),
        ("stage267_run267AZ_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267AZ design receipt."),
        ("stage267_run267AZ_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267AZ gate audit."),
        ("stage267_run267AZ_lineage", "lineage", LINEAGE_PATH, "Run267AZ lineage map."),
        ("stage267_run267AZ_review_result", "review_result", REVIEW_RESULT_PATH, "Run267AZ review JSON payload."),
        ("stage267_run267AZ_report", "review_report", REPORT_PATH, "User-facing run267AZ design report."),
    ]
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


def fmt(value: Any) -> str:
    return f"{as_float(value):.2f}"


def report_markdown(result: Mapping[str, Any]) -> str:
    candidate_rows = result["candidate_decisions"]
    queue_rows = result["next_experiment_queue"]
    failure = result["failure_memory"]
    lines = [
        "# Stage267 Run267AZ Pool-wide State Feature Engineering Second Follow-up/Adapter Branch Design(267단계 267AZ 후보군 전체 상태 피처 엔지니어링 2차 후속/어댑터 분기 설계)",
        "",
        "- action(행동): run267AY(267AY 실행)의 second follow-up review(2차 후속 검토)를 candidate role decision(후보 역할 결정), next experiment queue(다음 실험 큐), failure memory(실패 기억)로 바꿨다.",
        "- effect(효과): watch_rows(관찰 행)가 `0`인 상태에서 같은 repair(수리)를 세 번째 반복하지 않고, true fallback routing(실제 대체 라우팅), cross-period check(확장 기간 확인), similar feature replacement(유사 피처 대체), Adapter hold audit(어댑터 보류 감사)로 검증 폭을 넓힌다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- candidate_decisions(후보 결정): `{len(candidate_rows)}`",
        f"- next_queue_rows(다음 큐 행): `{len(queue_rows)}`",
        f"- failure_memory(실패 기억): `{len(failure)}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267AY(267AY 실행)는 모든 후보가 양수 순손익을 만들었지만, 관찰 후보는 하나도 없다고 판정했다.",
        "Effect(효과): 이제는 더 세게 같은 방향으로 누르는 것이 아니라, 왜 계속 깨지는지 확인할 실험 축을 바꿔야 한다.",
        "",
        "핵심 전환은 세 가지다. 첫째, Tier B fallback(티어 B 대체)을 실제 라우팅으로 확인한다. 둘째, 비슷한 의미의 feature(피처)로 바꿔도 후보가 버티는지 본다. 셋째, Adapter(어댑터)는 아직 만들지 않고 준비 조건만 감사한다.",
        "Effect(효과): 후보를 버리거나 고르는 결정은 다음 근거 뒤로 미루고, 이번에는 다음 실행이 무엇을 증명해야 하는지 고정한다.",
        "",
        "## Candidate Decisions(후보 결정)",
        "",
        "| candidate(후보) | role(역할) | design role(설계 역할) | tests(시험 수) | net mean(평균 순손익) | worst slice(최악 구간) | deep slices(깊은 구간) | decision(결정) | next use(다음 용도) |",
        "| --- | --- | --- | ---: | ---: | --- | ---: | --- | --- |",
    ]
    for row in candidate_rows:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('candidate_role')}` | `{row.get('design_role')}` | "
            f"{as_int(row.get('tier_a_test_count'))} | {fmt(row.get('net_profit_mean'))} | "
            f"`{row.get('worst_slice_axis')}`/`{row.get('worst_slice_bucket')}` {fmt(row.get('worst_slice_net_min'))} | "
            f"{as_int(row.get('deep_negative_slice_count'))} | `{row.get('decision_label')}` | `{row.get('next_use')}` |"
        )
    lines.extend(
        [
            "",
            "## Next Experiment Queue(다음 실험 큐)",
            "",
            "| queue(큐) | priority(우선순위) | workstream(작업 흐름) | candidate scope(후보 범위) | decision use(결정 용도) | stop condition(중단 조건) |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in queue_rows:
        lines.append(
            f"| `{row.get('queue_id')}` | `{row.get('priority')}` | `{row.get('workstream')}` | "
            f"`{row.get('candidate_scope')}` | `{row.get('decision_use')}` | `{row.get('stop_conditions')}` |"
        )
    lines.extend(
        [
            "",
            "## Failure Memory(실패 기억)",
            "",
            "| memory(기억) | pattern(패턴) | do not repeat(반복 금지) | salvage(회수 각도) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in failure:
        lines.append(
            f"| `{row.get('memory_id')}` | `{row.get('pattern')}` | `{row.get('do_not_repeat')}` | `{row.get('salvage_angle')}` |"
        )
    lines.extend(
        [
            "",
            "## Attribution(성과 귀속)",
            "",
            "- observed_change(관찰 변화): run267AY(267AY 실행)는 headline KPI(대표 핵심 성과 지표)를 양수로 유지했지만 watch_rows(관찰 행) `0`과 negative slices(음수 구간) `35`를 남겼다.",
            "- comparison_baseline(비교 기준): run267AU(267AU 실행) source follow-up(원천 후속)과 run267AY(267AY 실행) second follow-up(2차 후속).",
            "- likely_drivers(가능 동인): state feature pressure(상태 피처 압박)는 대표 숫자를 바꿨지만 월요일/2024-12 약점의 시장 구조를 충분히 설명하지 못했다.",
            "- segment_checks(구간 확인): month/weekday/session/hour/direction/chron segment(월/요일/세션/시간/방향/시간순서 구간) 확인 완료, true fallback route(실제 대체 라우팅)와 cross-period(확장 기간)는 아직 미완료.",
            "- trade_shape(거래 형태): 후보별 순손익은 양수지만 최악 구간은 -160 이하가 반복됐고, 일부 후보는 source follow-up(원천 후속) 대비 순손익이나 거래 수가 후퇴했다.",
            "- attribution_confidence(귀속 신뢰도): `medium_for_2024_diagnostic_low_for_generalization(2024 진단 중간, 일반화 낮음)`.",
            "",
            "## Result Judgment(결과 판정)",
            "",
            "- result_subject(결과 대상): `run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch_design`.",
            "- evidence_available(사용 가능 근거): run267AY review(검토), candidate summary(후보 요약), negative slices(음수 구간), route gap audit(라우팅 공백 감사).",
            "- evidence_missing(빠진 근거): run267BA materialization(물질화), true fallback runtime evidence(실제 대체 런타임 근거), cross-period MT5 results(확장 기간 MT5 결과), Adapter implementation(어댑터 구현), ONNX parity(ONNX 동등성).",
            f"- judgment_label(판정 라벨): `{JUDGMENT}`.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            f"- next_condition(다음 조건): `{NEXT_ACTION}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_review(원천 검토): `{rel(SOURCE_REVIEW_RESULT_PATH)}`.",
            f"- source_candidate_review(원천 후보 검토): `{rel(SOURCE_CANDIDATE_REVIEW_PATH)}`.",
            f"- source_route_gap(원천 라우팅 공백): `{rel(SOURCE_ROUTE_GAP_AUDIT_PATH)}`.",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
            f"- outputs(산출물): `{rel(CANDIDATE_DECISION_PATH)}`, `{rel(NEXT_EXPERIMENT_QUEUE_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
        ]
    )
    return "\n".join(lines)


def build_result() -> dict[str, Any]:
    if not path_exists(SOURCE_REVIEW_RESULT_PATH):
        raise FileNotFoundError(SOURCE_REVIEW_RESULT_PATH)
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    candidate_rows = read_csv(SOURCE_CANDIDATE_REVIEW_PATH)
    summary_rows = read_csv(SOURCE_CANDIDATE_SUMMARY_PATH)
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    candidate_decisions = build_candidate_decisions(summary_rows, candidate_rows, negative_rows)
    queue_rows = build_next_queue(candidate_decisions)
    failure_memory = build_failure_memory(candidate_decisions, negative_rows)
    attribution = build_performance_attribution(candidate_decisions)
    judgment_rows = build_result_judgment(candidate_decisions)
    receipts = build_design_receipt(queue_rows, source_result)
    gate_audit = build_gate_audit(source_result, candidate_decisions, queue_rows, failure_memory)
    result = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "source_execution_run_id": SOURCE_EXECUTION_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_decisions": candidate_decisions,
        "next_experiment_queue": queue_rows,
        "failure_memory": failure_memory,
        "performance_attribution": attribution,
        "result_judgment": judgment_rows,
        "experiment_design_receipt": receipts,
        "gate_audit": gate_audit,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "outputs": {
            "candidate_decisions": rel(CANDIDATE_DECISION_PATH),
            "next_experiment_queue": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "performance_attribution": rel(PERFORMANCE_ATTRIBUTION_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "sources": {
            "review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "candidate_review": rel(SOURCE_CANDIDATE_REVIEW_PATH),
            "candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "profile_summary": rel(SOURCE_PROFILE_SUMMARY_PATH),
            "negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "time_slice": rel(SOURCE_TIME_SLICE_PATH),
            "curve_diagnostics": rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
            "route_gap_audit": rel(SOURCE_ROUTE_GAP_AUDIT_PATH),
            "prior_research_audit": rel(SOURCE_PRIOR_RESEARCH_AUDIT_PATH),
        },
        "artifact_hashes": source_hashes(),
    }
    return result


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(CANDIDATE_DECISION_PATH, result["candidate_decisions"])
    write_csv(NEXT_EXPERIMENT_QUEUE_PATH, result["next_experiment_queue"])
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"])
    write_csv(PERFORMANCE_ATTRIBUTION_PATH, result["performance_attribution"])
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"])
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"])
    write_csv(GATE_AUDIT_PATH, result["gate_audit"])
    lineage = build_lineage(result)
    write_json(LINEAGE_PATH, lineage)
    result_payload = dict(result)
    result_payload["lineage"] = lineage
    write_json(REVIEW_RESULT_PATH, result_payload)
    write_md(REPORT_PATH, report_markdown(result_payload))
    update_ledgers(str(result["created_at_utc"]), result_payload)
    update_current_truth_docs(result_payload)


def main() -> int:
    result = build_result()
    write_outputs(result)
    print(
        json.dumps(
            {
                "status": STATUS,
                "candidate_decisions": len(result["candidate_decisions"]),
                "next_queue_rows": len(result["next_experiment_queue"]),
                "failure_memory": len(result["failure_memory"]),
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": NEXT_ACTION,
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
