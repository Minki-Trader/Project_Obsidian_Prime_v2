from __future__ import annotations

import csv
import json
import math
import sys
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
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import run267BL_aggressive_pressure_first_tranche_balance_timeslice_trade_quality_review as source_review


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267BM"
RUN_ID = "run267BM_stage267_aggressive_pressure_second_tranche_or_cross_period_validation_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
SOURCE_EXECUTION_RUN_ID = source_review.PARENT_RUN_ID
STATUS = "run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design_completed"
JUDGMENT = "experiment_design_completed_no_candidate_selection"
NEXT_ACTION = "run267BN_materialize_aggressive_second_tranche_cross_period_validation"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "aggressive_pressure_second_tranche_or_cross_period_validation_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_VARIANT_REVIEW_PATH = source_review.AGGRESSIVE_VARIANT_REVIEW_PATH
SOURCE_VARIANT_SUMMARY_PATH = source_review.AGGRESSIVE_VARIANT_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_TIME_SLICE_PATH = source_review.TIME_SLICE_KPI_PATH
SOURCE_CURVE_DIAGNOSTICS_PATH = source_review.CURVE_DIAGNOSTICS_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH
SOURCE_EXECUTION_RESULT_PATH = source_review.SOURCE_EXECUTION_RESULT_PATH
SOURCE_TRANCHE_QUEUE_PATH = source_review.SOURCE_TRANCHE_QUEUE_PATH
SOURCE_RUNTIME_CONTRACT_PATH = source_review.SOURCE_RUNTIME_CONTRACT_PATH
SOURCE_PROFILE_ENCODING_PATH = source_review.SOURCE_PROFILE_ENCODING_PATH
SOURCE_RUNTIME_PARITY_PATH = source_review.SOURCE_RUNTIME_PARITY_PATH

SECOND_TRANCHE_QUEUE_PATH = RUN_ROOT / "second_tranche_queue.csv"
CROSS_PERIOD_PLAN_PATH = RUN_ROOT / "cross_period_validation_plan.csv"
VARIANT_DECISION_PATH = RUN_ROOT / "variant_decision_matrix.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design.py")

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

QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "materialization_scope",
    "candidate_id",
    "candidate_alias",
    "candidate_role",
    "source_variant_id",
    "source_queue_id",
    "design_lane",
    "target_period",
    "target_split",
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
    "claim_boundary",
    "materialization_instruction",
)

DECISION_COLUMNS = (
    "variant_id",
    "priority",
    "net_profit",
    "profit_factor",
    "trade_count",
    "drawdown_percent",
    "worst_month",
    "worst_month_net",
    "worst_slice",
    "worst_slice_net",
    "decision_label",
    "next_use",
    "do_not_claim",
)

PLAN_COLUMNS = (
    "plan_id",
    "period",
    "split",
    "purpose",
    "must_keep_fixed",
    "must_change",
    "success_floor",
    "failure_floor",
    "evidence_required",
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


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return value


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
    fieldnames = list(columns or ordered or ("status", "notes"))
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


def source_hashes() -> dict[str, str]:
    paths = {
        "source_review_result": SOURCE_REVIEW_RESULT_PATH,
        "source_variant_review": SOURCE_VARIANT_REVIEW_PATH,
        "source_variant_summary": SOURCE_VARIANT_SUMMARY_PATH,
        "source_negative_slice": SOURCE_NEGATIVE_SLICE_PATH,
        "source_execution_result": SOURCE_EXECUTION_RESULT_PATH,
        "source_tranche_queue": SOURCE_TRANCHE_QUEUE_PATH,
        "source_runtime_contract": SOURCE_RUNTIME_CONTRACT_PATH,
        "producer": PRODUCER_PATH,
    }
    return {name: sha256_file_lf_normalized(path) if path_exists(path) else "missing" for name, path in paths.items()}


def row_by_variant(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("variant_id")): row for row in rows}


def variant_decision_rows(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in variant_rows:
        variant = str(row.get("variant_id"))
        flags = str(row.get("fragility_flags"))
        if variant == "anti_overconstraint_prune":
            decision = "p0_cross_period_validate_no_selection(P0 확장 기간 검증, 선택 아님)"
            priority = "P0"
            next_use = "materialize 2023H2/2025H1/2025H2 and similar replacement stress(2023H2/2025H1/2025H2 및 유사 대체 압박 물질화)"
        elif variant == "state_acceleration_interaction":
            decision = "p1_interaction_replacement_watch_no_selection(P1 상호작용 대체 관찰, 선택 아님)"
            priority = "P1"
            next_use = "use as interaction-control branch if P0 survives(1순위가 버티면 상호작용 대조 분기로 사용)"
        elif variant == "explode_opportunity_recall":
            decision = "p2_salvage_only_due_deep_slice_hole(P2 회수 전용, 깊은 구간 구멍 때문)"
            priority = "P2"
            next_use = "do not expand until session and Monday holes are isolated(세션/월요일 구멍이 분리되기 전 확장 금지)"
        elif variant == "payoff_convexity_push":
            decision = "p3_prune_for_now_due_dd_and_month_hole(P3 일단 가지치기, 손실폭과 월 구멍 때문)"
            priority = "P3"
            next_use = "record as failure memory unless new risk-shape idea appears(새 위험 모양 아이디어 전까지 실패 기억)"
        else:
            decision = "diagnostic_only(진단 전용)"
            priority = "PX"
            next_use = "hold(보류)"
        output.append(
            {
                "variant_id": variant,
                "priority": priority,
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "drawdown_percent": row.get("report_equity_drawdown_percent"),
                "worst_month": row.get("worst_month"),
                "worst_month_net": row.get("worst_month_net"),
                "worst_slice": f"{row.get('worst_slice_axis')}/{row.get('worst_slice_bucket')}",
                "worst_slice_net": row.get("worst_slice_net"),
                "decision_label": decision,
                "next_use": next_use,
                "do_not_claim": "selected_candidate;selected_research_baseline;ONNX readiness;Goal Achieve",
                "fragility_flags": flags,
            }
        )
    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "PX": 9}
    return sorted(output, key=lambda item: (order.get(str(item.get("priority")), 9), -as_float(item.get("net_profit"))))


def build_queue(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_variant = row_by_variant(variant_rows)
    p0 = by_variant.get("anti_overconstraint_prune", {})
    p1 = by_variant.get("state_acceleration_interaction", {})
    base_control = (
        "symbol=US100;timeframe=M5;broker=FPMarkets;MT5 profile utf-8-no-bom(MT5 프로필 UTF-8 BOM 없음);"
        "risk/reporting fixed(위험/보고 고정);no ONNX(ONNX 없음)"
    )
    rows = [
        {
            "queue_id": "run267BM_01_s264_aih_anti_overconstraint_2023h2",
            "priority": "P0",
            "materialization_scope": "direct_mt5_attempt_ready(직접 MT5 시도 준비)",
            "candidate_id": p0.get("candidate_id", "s264_allow_inner_high_quarter"),
            "candidate_alias": p0.get("candidate_alias", "s264_aih"),
            "candidate_role": p0.get("candidate_role", "core_challenger"),
            "source_variant_id": "anti_overconstraint_prune",
            "source_queue_id": p0.get("source_queue_id", ""),
            "design_lane": "cross_period_validation(확장 기간 검증)",
            "target_period": "2023H2",
            "target_split": "adjacent_period_pre_2024_stress(2024 이전 인접 기간 압박)",
            "hypothesis": "If anti-overconstraint is structural, it should not need 2024-only timing to survive(과제약 제거가 구조적이면 2024 전용 타이밍 없이도 버텨야 한다).",
            "decision_use": "decide whether the P0 aggressive branch deserves broader materialization(P0 공격형 분기가 더 넓은 물질화 가치가 있는지 결정)",
            "comparison_baseline": "run267BL anti_overconstraint_prune 2024 result and run267B historical 2024 baseline(run267BL 과제약 제거 2024 결과와 run267B 2024 기준)",
            "control_variables": base_control,
            "changed_variables": "period only; keep anti-overconstraint surface and risk handoff fixed(기간만 변경, 과제약 제거 표면과 위험 인계 고정)",
            "sample_scope": "Tier A first; Tier B fallback remains blocked until true fallback manifest exists(Tier A 우선, Tier B 대체는 목록 전까지 차단)",
            "success_criteria": "PF>=1.45; DD<=20%; no month below -350; trade_count>=250; late segment net>=0",
            "failure_criteria": "PF<1.20 or DD>25% or one month/session dominates loss(PF 1.20 미만 또는 DD 25% 초과 또는 한 월/세션 손실 지배)",
            "invalid_conditions": "feature frame mismatch, stale report, tester profile BOM, runtime CSV missing(피처 프레임 불일치, 낡은 보고서, BOM 프로필, 런타임 CSV 누락)",
            "stop_conditions": "if 2023H2 fails hard, do not expand P0 to third repair loop(2023H2가 크게 깨지면 P0 3차 수리 확장 금지)",
            "evidence_plan": "MT5 report, KPI summary, trade records, curve diagnostics, time-slice KPI(MT5 보고서, KPI 요약, 거래 기록, 곡선 진단, 시간구간 KPI)",
            "claim_boundary": "research_materialization_queue_only_no_selection_no_onnx",
            "materialization_instruction": "clone source model/set shape and bind to 2023H2 feature frame(원천 모델/설정 형태를 복제하고 2023H2 피처 프레임에 연결)",
        },
        {
            "queue_id": "run267BM_02_s264_aih_anti_overconstraint_2025h1",
            "priority": "P0",
            "materialization_scope": "direct_mt5_attempt_ready(직접 MT5 시도 준비)",
            "candidate_id": p0.get("candidate_id", "s264_allow_inner_high_quarter"),
            "candidate_alias": p0.get("candidate_alias", "s264_aih"),
            "candidate_role": p0.get("candidate_role", "core_challenger"),
            "source_variant_id": "anti_overconstraint_prune",
            "source_queue_id": p0.get("source_queue_id", ""),
            "design_lane": "cross_period_validation(확장 기간 검증)",
            "target_period": "2025H1",
            "target_split": "adjacent_oos_recovery_stress(인접 표본외 회복 압박)",
            "hypothesis": "The branch should keep a usable curve after 2024 without relying on one late-2024 run-up(이 분기는 2024 후에도 특정 후반 상승에만 기대지 않아야 한다).",
            "decision_use": "test OOS carry-forward value without claiming readiness(준비 주장 없이 OOS 이월 가치 검정)",
            "comparison_baseline": "run267BL anti_overconstraint_prune 2024 result and adjacent-period replacement lessons(run267BL 2024 결과와 인접 기간 대체 교훈)",
            "control_variables": base_control,
            "changed_variables": "period only; keep anti-overconstraint surface and risk handoff fixed(기간만 변경, 표면/위험 인계 고정)",
            "sample_scope": "Tier A first; true fallback blocked(Tier A 우선, 실제 대체 차단)",
            "success_criteria": "PF>=1.35; DD<=22%; no deep month below -350; trade_count>=160",
            "failure_criteria": "OOS collapse, low trade count luck, or DD spike(OOS 붕괴, 적은 거래 운, DD 급등)",
            "invalid_conditions": "feature/report/runtime handoff mismatch(피처/보고/런타임 인계 불일치)",
            "stop_conditions": "if 2025H1 and 2025H2 both fail, demote P0 to failure memory(2025H1/2025H2 모두 실패하면 P0 실패 기억으로 강등)",
            "evidence_plan": "MT5 report plus curve/time-slice/trade quality review(MT5 보고서와 곡선/시간구간/거래품질 검토)",
            "claim_boundary": "research_materialization_queue_only_no_selection_no_onnx",
            "materialization_instruction": "clone source model/set shape and bind to 2025H1 feature frame(원천 모델/설정 형태를 복제하고 2025H1 피처 프레임에 연결)",
        },
        {
            "queue_id": "run267BM_03_s264_aih_anti_overconstraint_2025h2",
            "priority": "P0",
            "materialization_scope": "direct_mt5_attempt_ready(직접 MT5 시도 준비)",
            "candidate_id": p0.get("candidate_id", "s264_allow_inner_high_quarter"),
            "candidate_alias": p0.get("candidate_alias", "s264_aih"),
            "candidate_role": p0.get("candidate_role", "core_challenger"),
            "source_variant_id": "anti_overconstraint_prune",
            "source_queue_id": p0.get("source_queue_id", ""),
            "design_lane": "cross_period_validation(확장 기간 검증)",
            "target_period": "2025H2",
            "target_split": "adjacent_oos_late_stress(인접 표본외 후반 압박)",
            "hypothesis": "The branch should survive late adjacent OOS instead of being a 2024-only pocket(2024 전용 주머니가 아니라 인접 OOS 후반도 버텨야 한다).",
            "decision_use": "test late-OOS fragility before adapter work(어댑터 작업 전 후반 OOS 취약성 검정)",
            "comparison_baseline": "run267BL anti_overconstraint_prune 2024 result(run267BL 과제약 제거 2024 결과)",
            "control_variables": base_control,
            "changed_variables": "period only; keep anti-overconstraint surface and risk handoff fixed(기간만 변경, 표면/위험 인계 고정)",
            "sample_scope": "Tier A first; true fallback blocked(Tier A 우선, 실제 대체 차단)",
            "success_criteria": "PF>=1.30; DD<=22%; trade_count>=100; no single slice loss below -300",
            "failure_criteria": "late OOS breaks or relies on one session only(후반 OOS 붕괴 또는 한 세션 의존)",
            "invalid_conditions": "feature/report/runtime handoff mismatch(피처/보고/런타임 인계 불일치)",
            "stop_conditions": "if late OOS fails and 2025H1 fails, stop P0 branch repair loop(후반 OOS와 2025H1이 실패하면 P0 수리 루프 중단)",
            "evidence_plan": "MT5 report plus curve/time-slice/trade quality review(MT5 보고서와 곡선/시간구간/거래품질 검토)",
            "claim_boundary": "research_materialization_queue_only_no_selection_no_onnx",
            "materialization_instruction": "clone source model/set shape and bind to 2025H2 feature frame(원천 모델/설정 형태를 복제하고 2025H2 피처 프레임에 연결)",
        },
        {
            "queue_id": "run267BM_04_s264_aih_anti_overconstraint_similar_replacement",
            "priority": "P1",
            "materialization_scope": "source_surface_needed_before_mt5(MT5 전 원천 표면 필요)",
            "candidate_id": p0.get("candidate_id", "s264_allow_inner_high_quarter"),
            "candidate_alias": p0.get("candidate_alias", "s264_aih"),
            "candidate_role": p0.get("candidate_role", "core_challenger"),
            "source_variant_id": "anti_overconstraint_prune",
            "source_queue_id": p0.get("source_queue_id", ""),
            "design_lane": "similar_feature_replacement(유사 피처 대체)",
            "target_period": "2024",
            "target_split": "historical_2024_tier_a_train_era_stress",
            "hypothesis": "The anti-overconstraint branch should not depend on one ADX-style trend column(과제약 제거 분기는 하나의 ADX류 추세 컬럼에만 의존하면 안 된다).",
            "decision_use": "decide whether Adapter feature structure is worth designing(어댑터 피처 구조 설계 가치 판단)",
            "comparison_baseline": "run267BL anti_overconstraint_prune and run267W rep_trend_strength_adx(run267BL 과제약 제거와 run267W ADX 대체)",
            "control_variables": base_control,
            "changed_variables": "replace trend-strength meaning with acceleration/rank-volatility proxy(추세 강도 의미를 가속/순위 변동성 대체축으로 교체)",
            "sample_scope": "2024 Tier A diagnostic first(2024 Tier A 진단 우선)",
            "success_criteria": "PF remains >=1.55, DD<=18%, trade count>=350, no deeper Monday/session hole",
            "failure_criteria": "performance vanishes after replacement or holes deepen(대체 후 성과 소멸 또는 구멍 심화)",
            "invalid_conditions": "feature order not proven or replacement leaks time(피처 순서 미입증 또는 시간 누수)",
            "stop_conditions": "if replacement fails, keep P0 as non-Adapter watch only(대체 실패 시 P0는 비어댑터 관찰로만 유지)",
            "evidence_plan": "feature map, model mutation audit, MT5 run, trade-quality review(피처 지도, 모델 변형 감사, MT5 실행, 거래품질 검토)",
            "claim_boundary": "research_design_only_no_selection_no_onnx",
            "materialization_instruction": "build replacement score table before MT5( MT5 전 대체 점수표 작성)",
        },
        {
            "queue_id": "run267BM_05_s264_aih_state_acceleration_cross_period_control",
            "priority": "P1",
            "materialization_scope": "control_mt5_attempt_ready(대조 MT5 시도 준비)",
            "candidate_id": p1.get("candidate_id", "s264_allow_inner_high_quarter"),
            "candidate_alias": p1.get("candidate_alias", "s264_aih"),
            "candidate_role": p1.get("candidate_role", "core_challenger"),
            "source_variant_id": "state_acceleration_interaction",
            "source_queue_id": p1.get("source_queue_id", ""),
            "design_lane": "interaction_control_cross_period(상호작용 대조 확장 기간)",
            "target_period": "2025H1",
            "target_split": "adjacent_oos_recovery_stress",
            "hypothesis": "A smaller but cleaner interaction branch may be more stable than raw opportunity expansion(작지만 깨끗한 상호작용 분기가 원시 기회 확장보다 안정적일 수 있다).",
            "decision_use": "control against P0 so the next step does not overfit one aggressive branch(P0 대조로 한 공격형 분기에 과적합하지 않게 함)",
            "comparison_baseline": "run267BL state_acceleration_interaction and anti_overconstraint_prune(run267BL 상태 가속 상호작용과 과제약 제거)",
            "control_variables": base_control,
            "changed_variables": "period only for interaction branch(상호작용 분기의 기간만 변경)",
            "sample_scope": "Tier A first; true fallback blocked(Tier A 우선, 실제 대체 차단)",
            "success_criteria": "PF>=1.35; DD<=17.5%; trade_count>=160; no late segment net below zero",
            "failure_criteria": "small edge collapses outside 2024(작은 edge가 2024 밖에서 붕괴)",
            "invalid_conditions": "feature/report/runtime handoff mismatch(피처/보고/런타임 인계 불일치)",
            "stop_conditions": "if both P0 and P1 fail 2025H1, pivot away from s264_aih aggressive branch(P0/P1 둘 다 2025H1 실패 시 s264_aih 공격 분기 전환)",
            "evidence_plan": "MT5 report plus curve/time-slice/trade quality review(MT5 보고서와 곡선/시간구간/거래품질 검토)",
            "claim_boundary": "research_materialization_queue_only_no_selection_no_onnx",
            "materialization_instruction": "clone interaction score table and bind to 2025H1 feature frame(상호작용 점수표 복제 후 2025H1 피처 프레임 연결)",
        },
        {
            "queue_id": "run267BM_06_s264_aih_explode_opportunity_hole_audit",
            "priority": "P2",
            "materialization_scope": "audit_before_more_mt5(추가 MT5 전 감사)",
            "candidate_id": "s264_allow_inner_high_quarter",
            "candidate_alias": "s264_aih",
            "candidate_role": "core_challenger",
            "source_variant_id": "explode_opportunity_recall",
            "source_queue_id": by_variant_value(by_variant=by_variant, variant="explode_opportunity_recall", key="source_queue_id"),
            "design_lane": "weak_slice_hole_audit(약한 구간 구멍 감사)",
            "target_period": "2024",
            "target_split": "historical_2024_tier_a_train_era_stress",
            "hypothesis": "The highest net branch may be unusable if its session/Monday holes are structural(순수익 최고 분기도 세션/월요일 구멍이 구조적이면 쓰기 어렵다).",
            "decision_use": "decide whether to salvage or prune explode_opportunity_recall(기회 회수 확장을 회수할지 가지칠지 결정)",
            "comparison_baseline": "run267BL explode_opportunity_recall negative slices(run267BL 기회 회수 확장 음수 구간)",
            "control_variables": base_control,
            "changed_variables": "no new filter; audit only until hole source is explained(새 필터 없음, 구멍 원인 설명 전 감사만)",
            "sample_scope": "2024 Tier A trade list and time-slice only(2024 Tier A 거래 목록과 시간구간만)",
            "success_criteria": "hole traced to narrow low-count slice and not recurring across months(구멍이 적은 거래의 좁은 구간으로 설명되고 월별 반복 아님)",
            "failure_criteria": "Monday/session hole repeats across months or high trade count(월요일/세션 구멍이 월별 반복 또는 거래 수 큼)",
            "invalid_conditions": "trade parser mismatch or report missing(거래 파서 불일치 또는 보고서 누락)",
            "stop_conditions": "do not materialize until audit passes(감사 통과 전 물질화 금지)",
            "evidence_plan": "negative slice drilldown and chart review(음수 구간 세부 검토와 차트 검토)",
            "claim_boundary": "research_audit_only_no_selection_no_onnx",
            "materialization_instruction": "no MT5 materialization in run267BN unless converted to explicit audit artifact(run267BN에서는 명시 감사 산출물 전까지 MT5 물질화 없음)",
        },
    ]
    return rows


def by_variant_value(*, by_variant: Mapping[str, Mapping[str, Any]], variant: str, key: str) -> Any:
    return by_variant.get(variant, {}).get(key, "")


def build_cross_period_plan() -> list[dict[str, Any]]:
    return [
        {
            "plan_id": "cross_2023h2",
            "period": "2023H2",
            "split": "adjacent_period_pre_2024_stress(2024 이전 인접 기간 압박)",
            "purpose": "check whether 2024 result is a time pocket(2024 결과가 시간 주머니인지 확인)",
            "must_keep_fixed": "risk handoff, lot sizing, report identity, no-BOM profile(위험 인계, 랏 크기, 보고서 정체성, BOM 없는 프로필)",
            "must_change": "feature frame and tester date only(피처 프레임과 테스터 날짜만 변경)",
            "success_floor": "PF>=1.45;DD<=20%;month_net_min>-350;trade_count>=250",
            "failure_floor": "PF<1.20 or DD>25 or month/session deep loss(PF 1.20 미만 또는 DD 25 초과 또는 월/세션 깊은 손실)",
            "evidence_required": "MT5 report;KPI;trade records;curve;time-slice;profile encoding receipt",
        },
        {
            "plan_id": "cross_2025h1",
            "period": "2025H1",
            "split": "adjacent_oos_recovery_stress(인접 표본외 회복 압박)",
            "purpose": "check OOS carry-forward(OOS 이월 확인)",
            "must_keep_fixed": "risk handoff, lot sizing, report identity, no-BOM profile(위험 인계, 랏 크기, 보고서 정체성, BOM 없는 프로필)",
            "must_change": "feature frame and tester date only(피처 프레임과 테스터 날짜만 변경)",
            "success_floor": "PF>=1.35;DD<=22%;trade_count>=160",
            "failure_floor": "PF<1.10 or DD>27 or low-trade lucky spike(PF 1.10 미만 또는 DD 27 초과 또는 적은 거래 운)",
            "evidence_required": "MT5 report;KPI;trade records;curve;time-slice;profile encoding receipt",
        },
        {
            "plan_id": "cross_2025h2",
            "period": "2025H2",
            "split": "adjacent_oos_late_stress(인접 표본외 후반 압박)",
            "purpose": "check late OOS fragility(후반 OOS 취약성 확인)",
            "must_keep_fixed": "risk handoff, lot sizing, report identity, no-BOM profile(위험 인계, 랏 크기, 보고서 정체성, BOM 없는 프로필)",
            "must_change": "feature frame and tester date only(피처 프레임과 테스터 날짜만 변경)",
            "success_floor": "PF>=1.30;DD<=22%;trade_count>=100",
            "failure_floor": "late segment net negative with deep slice(후반 순수익 음수와 깊은 구간 손실)",
            "evidence_required": "MT5 report;KPI;trade records;curve;time-slice;profile encoding receipt",
        },
    ]


def failure_memory_rows() -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "run267BM_payoff_convexity_push_prune",
            "pattern": "payoff_convexity_push had headline net but DD/month/Monday holes(페이오프 볼록성 확장은 겉 순수익은 있으나 DD/월/월요일 구멍이 있음)",
            "evidence": f"{rel(SOURCE_VARIANT_REVIEW_PATH)}",
            "affected_scope": "s264_aih aggressive pressure first tranche(s264_aih 공격형 압박 첫 묶음)",
            "do_not_repeat": "do not keep stretching payoff without a new risk-shape idea(새 위험 모양 아이디어 없이 페이오프만 늘리지 않기)",
            "salvage_angle": "only revisit with explicit DD compression or exit-shape redesign(명시적 DD 압축 또는 청산 구조 재설계 때만 재방문)",
            "boundary": "failure_memory_not_candidate_selection(실패 기억, 후보 선택 아님)",
        },
        {
            "memory_id": "run267BM_explode_opportunity_session_hole",
            "pattern": "explode_opportunity_recall had strongest net but deep session/Monday holes(기회 회수 확장은 순수익 최고이나 깊은 세션/월요일 구멍 있음)",
            "evidence": f"{rel(SOURCE_NEGATIVE_SLICE_PATH)}",
            "affected_scope": "s264_aih opportunity expansion(s264_aih 기회 확장)",
            "do_not_repeat": "do not promote high net without slice hole audit(구간 구멍 감사 없이 높은 순수익만 승격하지 않기)",
            "salvage_angle": "audit whether the hole is low-count noise before more MT5(추가 MT5 전 구멍이 적은 거래 노이즈인지 감사)",
            "boundary": "failure_memory_not_candidate_selection(실패 기억, 후보 선택 아님)",
        },
    ]


def performance_attribution_rows() -> list[dict[str, Any]]:
    return [
        {
            "attribution_id": "run267BM_anti_overconstraint_signal",
            "observed_change": "anti_overconstraint_prune produced PF 1.81, 495 trades, DD 16.53, all months positive in 2024(과제약 제거가 2024에서 PF 1.81, 495거래, DD 16.53, 전월 양수)",
            "comparison_baseline": "run267BL first tranche and prior defensive repair branches(run267BL 첫 묶음과 이전 방어 수리 분기)",
            "likely_drivers": "removing overconstraints increased opportunity while preserving risk shape(과제약 제거가 기회를 늘리면서 위험 모양을 보존)",
            "segment_checks": "session_07_12 and Monday still need watch(07-12 세션과 월요일은 관찰 필요)",
            "trade_shape": "trade count large enough for next pressure but not enough for selection(다음 압박에는 충분한 거래 수이나 선택에는 부족)",
            "alternative_explanations": "2024-specific market pocket or source ADX replacement artifact(2024 전용 시장 주머니 또는 원천 ADX 대체 산물)",
            "attribution_confidence": "medium_for_design_only(설계 한정 중간)",
            "next_probe": "cross-period validation plus similar replacement(확장 기간 검증과 유사 대체)",
        },
        {
            "attribution_id": "run267BM_state_acceleration_control",
            "observed_change": "state_acceleration_interaction had lower net but clean DD and reasonable PF(상태 가속 상호작용은 낮은 순수익이나 깨끗한 DD와 괜찮은 PF)",
            "comparison_baseline": "anti_overconstraint_prune and explode_opportunity_recall(과제약 제거와 기회 회수 확장)",
            "likely_drivers": "interaction surface may be more stable but less explosive(상호작용 표면은 더 안정적이나 덜 폭발적일 수 있음)",
            "segment_checks": "Monday and 2024-06 remain weak(월요일과 2024-06은 여전히 약함)",
            "trade_shape": "409 trades with PF 1.61 gives control value(409거래 PF 1.61은 대조 가치 있음)",
            "alternative_explanations": "smaller edge could vanish outside 2024(작은 edge는 2024 밖에서 사라질 수 있음)",
            "attribution_confidence": "medium_low_until_cross_period(확장 기간 전 중하)",
            "next_probe": "2025H1 control run if P0 materialization proceeds(P0 물질화 시 2025H1 대조 실행)",
        },
    ]


def experiment_design_receipt_rows(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "field": "hypothesis",
            "value": "anti_overconstraint_prune may be a stronger aggressive branch if it survives adjacent periods and similar replacement(과제약 제거가 인접 기간과 유사 대체에서 버티면 더 강한 공격형 분기일 수 있음)",
            "effect": "2024 숫자 하나로 고르지 않고 구조 여부를 확인한다.",
        },
        {
            "field": "decision_use",
            "value": "materialization priority and prune/continue boundary only(물질화 우선순위와 가지치기/계속 경계만)",
            "effect": "selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비)를 주장하지 않는다.",
        },
        {
            "field": "comparison_baseline",
            "value": "run267BL first tranche plus historical 2024 baseline and prior ablation/replacement lessons(run267BL 첫 묶음, 2024 기준, 이전 제거/대체 교훈)",
            "effect": "headline KPI(겉 KPI)를 기존 연구 흐름과 연결한다.",
        },
        {
            "field": "control_variables",
            "value": "US100 M5 FPMarkets, risk handoff, report identity, no-BOM tester profile(US100 M5 FPMarkets, 위험 인계, 보고서 정체성, BOM 없는 테스터 프로필)",
            "effect": "기간 차이를 후보 차이로 오해하지 않게 한다.",
        },
        {
            "field": "queue_rows",
            "value": str(len(queue_rows)),
            "effect": "다음 run267BN(267BN 실행)에 넘길 물질화 후보 수를 고정한다.",
        },
    ]


def result_judgment_rows() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "run267BL variant review, negative slices, curve diagnostics, MT5 profile/runtime receipts(run267BL 변형 검토, 음수 구간, 곡선 진단, MT5 프로필/런타임 영수증)",
            "evidence_missing": "cross-period MT5 execution, similar replacement execution, Adapter structure, ONNX parity(확장 기간 MT5 실행, 유사 대체 실행, 어댑터 구조, ONNX 동등성)",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "좋아 보이는 2024 결과를 바로 고르지 않고, 다음에는 기간을 바꿔서 깨지는지 본다.",
        }
    ]


def gate_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_authority_audit",
            "status": "passed",
            "evidence": rel(SOURCE_VARIANT_REVIEW_PATH),
            "effect": "run267BM(267BM 실행)이 run267BL(267BL 실행)의 실제 리뷰 결과에서 출발한다.",
        },
        {
            "gate": "no_selection_claim_guard",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_PATH),
            "effect": "선택 후보/ONNX/목표 달성을 주장하지 않는다.",
        },
        {
            "gate": "materialization_boundary",
            "status": "passed",
            "evidence": rel(SECOND_TRANCHE_QUEUE_PATH),
            "effect": "다음 작업은 설계 큐이며 실행 결과가 아니다.",
        },
    ]


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


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + focus_block, 1)


def update_stage267_workspace_block(text: str, *, status: str, run_id: str, next_action: str, report_entry: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_report = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {run_id}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not inserted_report:
                output.append(report_entry)
                inserted_report = True
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {status}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {run_id}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {run_id}")
                continue
            if stripped.startswith("next_action:"):
                if not inserted_report:
                    output.append(report_entry)
                    inserted_report = True
                output.append(f"  next_action: {next_action}")
                continue
        output.append(line)
    if in_stage267 and not inserted_report:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def update_current_truth_docs() -> None:
    report_line = f"- run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design(267BM 공격형 압박 2차 묶음/확장 기간 검증 설계): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            "Run267BM(267BM 실행)은 run267BL(267BL 실행)의 aggressive pressure first tranche(공격형 압박 첫 묶음) 검토를 받아 2차 묶음과 cross-period validation(확장 기간 검증) 큐를 설계했다.",
            "Effect(효과): anti_overconstraint_prune(과제약 제거)을 바로 선택하지 않고 2023H2/2025H1/2025H2 및 similar replacement(유사 대체)에서 다시 깨뜨려 본다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = replace_line_prefix(
            text,
            "- adapter_under_review(검토 중 어댑터):",
            "- adapter_under_review(검토 중 어댑터): `aggressive_pressure_second_tranche_or_cross_period_validation_design`",
        )
        text = append_after_contains(text, "stage267_run267BL_aggressive_pressure_first_tranche_balance_timeslice_trade_quality_review.md", report_line)
        text = append_block_once(text, "Run267BM(267BM 실행)은 run267BL", block)
        write_md(path, text)
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BM(267BM 실행) aggressive pressure second tranche/cross-period validation design(공격형 압박 2차 묶음/확장 기간 검증 설계) `{STATUS}`. "
        "Effect(효과): anti_overconstraint_prune(과제약 제거)을 바로 고르지 않고 2023H2/2025H1/2025H2와 similar replacement(유사 대체)로 다시 검증하도록 큐를 만들었고 selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        status=STATUS,
        run_id=RUN_ID,
        next_action=NEXT_ACTION,
        report_entry=f"  run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def update_ledgers(created_at: str, queue_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "aggressive_pressure_second_tranche_or_cross_period_validation_design",
                "tier_scope": "Tier A design first; true fallback blocked",
                "scoreboard": "experiment_design_queue",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"queue_rows={len(queue_rows)};next_action={NEXT_ACTION};selected_candidate=none.",
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
                "lane": "baseline_candidate_racing_aggressive_pressure_second_tranche_cross_period_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": f"queue_rows={len(queue_rows)};selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__aggressive_pressure_second_tranche_or_cross_period_validation_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "aggressive_pressure_second_tranche_or_cross_period_validation_design",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "aggressive_pressure_second_tranche_or_cross_period_validation_design",
                "tier_scope": "Tier A design first; true fallback blocked",
                "kpi_scope": "design_queue_no_kpi",
                "scoreboard_lane": "experiment_design_queue",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": f"queue_rows={len(queue_rows)};p0_rows=3;p1_rows=2;p2_rows=1",
                "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "out_of_scope_by_claim",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    entries = (
        ("stage267_run267BM_design_script", "producer_script", PRODUCER_PATH, "Builds run267BM second tranche/cross-period validation design."),
        ("stage267_run267BM_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267BL review result."),
        ("stage267_run267BM_source_variant_review", "source_variant_review", SOURCE_VARIANT_REVIEW_PATH, "Source run267BL variant review."),
        ("stage267_run267BM_source_variant_summary", "source_variant_summary", SOURCE_VARIANT_SUMMARY_PATH, "Source run267BL variant summary."),
        ("stage267_run267BM_second_tranche_queue", "second_tranche_queue", SECOND_TRANCHE_QUEUE_PATH, "Run267BM materialization queue."),
        ("stage267_run267BM_cross_period_plan", "cross_period_plan", CROSS_PERIOD_PLAN_PATH, "Run267BM cross-period validation plan."),
        ("stage267_run267BM_variant_decision", "variant_decision_matrix", VARIANT_DECISION_PATH, "Run267BM variant decision matrix."),
        ("stage267_run267BM_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267BM failure memory."),
        ("stage267_run267BM_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Run267BM performance attribution."),
        ("stage267_run267BM_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267BM experiment design receipt."),
        ("stage267_run267BM_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267BM result judgment."),
        ("stage267_run267BM_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267BM gate audit."),
        ("stage267_run267BM_lineage", "lineage", LINEAGE_PATH, "Run267BM lineage map."),
        ("stage267_run267BM_review_result", "review_result", REVIEW_RESULT_PATH, "Run267BM review JSON payload."),
        ("stage267_run267BM_review_report", "review_report", REPORT_PATH, "User-facing run267BM design report."),
    )
    rows = [
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
    existing = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    replacement_ids = {row["artifact_id"] for row in rows}
    merged = [row for row in existing if row.get("artifact_id") not in replacement_ids]
    merged.extend(rows)
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ARTIFACT_COLUMNS)


def report_markdown(
    queue_rows: Sequence[Mapping[str, Any]],
    decision_rows: Sequence[Mapping[str, Any]],
    plan_rows: Sequence[Mapping[str, Any]],
) -> str:
    lines = [
        "# Stage267 run267BM Aggressive Pressure Second Tranche / Cross-Period Validation Design(267단계 267BM 공격형 압박 2차 묶음 / 확장 기간 검증 설계)",
        "",
        f"- action(행동): run267BL(267BL 실행)의 first tranche review(첫 묶음 검토)를 바탕으로 `{len(queue_rows)}`개 second tranche queue(2차 묶음 큐)를 만들었다.",
        "- effect(효과): anti_overconstraint_prune(과제약 제거)을 바로 고르지 않고 2023H2/2025H1/2025H2, similar replacement(유사 대체), interaction control(상호작용 대조)로 다시 부순다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "`anti_overconstraint_prune`은 지금 가장 볼 만하다. 하지만 이건 2024 한 구간에서 나온 관찰이다.",
        "Effect(효과): 바로 선택하지 않고 기간을 바꿔도 덜 깨지는지 확인한다. 깨지면 실패 기억으로 남기고, 버티면 다음 Adapter(어댑터) 설계 가치가 생긴다.",
        "",
        "## Variant Decisions(변형 판단)",
        "",
        "| priority(우선순위) | variant(변형) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst slice(최악 구간) | decision(판단) |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in decision_rows:
        lines.append(
            f"| `{row.get('priority')}` | `{row.get('variant_id')}` | {as_float(row.get('net_profit')):.2f} | "
            f"{as_float(row.get('profit_factor')):.2f} | {as_int(row.get('trade_count'))} | "
            f"{as_float(row.get('drawdown_percent')):.2f} | `{row.get('worst_slice')}` {as_float(row.get('worst_slice_net')):.2f} | `{row.get('decision_label')}` |"
        )
    lines.extend(
        [
            "",
            "## Second Tranche Queue(2차 묶음 큐)",
            "",
            "| queue(큐) | priority(우선순위) | lane(경로) | period(기간) | source(원천) | purpose(목적) |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in queue_rows:
        lines.append(
            f"| `{row.get('queue_id')}` | `{row.get('priority')}` | `{row.get('design_lane')}` | `{row.get('target_period')}` | "
            f"`{row.get('source_variant_id')}` | {row.get('decision_use')} |"
        )
    lines.extend(
        [
            "",
            "## Cross-Period Plan(확장 기간 계획)",
            "",
            "| plan(계획) | period(기간) | success floor(성공 바닥) | failure floor(실패 바닥) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in plan_rows:
        lines.append(
            f"| `{row.get('plan_id')}` | `{row.get('period')}` | {row.get('success_floor')} | {row.get('failure_floor')} |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- result_subject(결과 대상): `run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design`.",
            "- evidence_available(사용 가능 근거): run267BL(267BL 실행) variant review(변형 검토), negative slice(음수 구간), curve diagnostics(곡선 진단), profile/runtime receipts(프로필/런타임 영수증).",
            "- evidence_missing(빠진 근거): cross-period MT5 execution(확장 기간 MT5 실행), similar replacement execution(유사 대체 실행), Adapter structure(어댑터 구조), ONNX parity(ONNX 동등성).",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- second_tranche_queue(2차 묶음 큐): `{rel(SECOND_TRANCHE_QUEUE_PATH)}`",
            f"- cross_period_plan(확장 기간 계획): `{rel(CROSS_PERIOD_PLAN_PATH)}`",
            f"- variant_decision_matrix(변형 판단 행렬): `{rel(VARIANT_DECISION_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- performance_attribution(성과 귀속): `{rel(PERFORMANCE_ATTRIBUTION_PATH)}`",
            f"- lineage(계보): `{rel(LINEAGE_PATH)}`",
        ]
    )
    return "\n".join(lines)


def run() -> dict[str, Any]:
    created_at = utc_now()
    variant_rows = read_csv(SOURCE_VARIANT_REVIEW_PATH)
    if not variant_rows:
        raise RuntimeError(f"missing source variant review: {SOURCE_VARIANT_REVIEW_PATH}")
    queue_rows = build_queue(variant_rows)
    decision_rows = variant_decision_rows(variant_rows)
    plan_rows = build_cross_period_plan()
    failure_rows = failure_memory_rows()
    attribution_rows = performance_attribution_rows()
    design_rows = experiment_design_receipt_rows(queue_rows)
    judgment_rows = result_judgment_rows()
    gate_rows = gate_audit_rows()
    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_execution_run_id": SOURCE_EXECUTION_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "queue_row_count": len(queue_rows),
        "variant_decision_count": len(decision_rows),
        "cross_period_plan_count": len(plan_rows),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "source_hashes": source_hashes(),
        "outputs": {
            "second_tranche_queue": rel(SECOND_TRANCHE_QUEUE_PATH),
            "cross_period_validation_plan": rel(CROSS_PERIOD_PLAN_PATH),
            "variant_decision_matrix": rel(VARIANT_DECISION_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "performance_attribution": rel(PERFORMANCE_ATTRIBUTION_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(SECOND_TRANCHE_QUEUE_PATH, queue_rows, QUEUE_COLUMNS)
    write_csv(CROSS_PERIOD_PLAN_PATH, plan_rows, PLAN_COLUMNS)
    write_csv(VARIANT_DECISION_PATH, decision_rows, DECISION_COLUMNS + ("fragility_flags",))
    write_csv(FAILURE_MEMORY_PATH, failure_rows)
    write_csv(PERFORMANCE_ATTRIBUTION_PATH, attribution_rows)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, design_rows)
    write_csv(RESULT_JUDGMENT_PATH, judgment_rows, RESULT_JUDGMENT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, gate_rows)
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "sources": {
                "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
                "source_variant_review": rel(SOURCE_VARIANT_REVIEW_PATH),
                "source_variant_summary": rel(SOURCE_VARIANT_SUMMARY_PATH),
                "source_negative_slice": rel(SOURCE_NEGATIVE_SLICE_PATH),
                "source_time_slice": rel(SOURCE_TIME_SLICE_PATH),
                "source_curve_diagnostics": rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
                "source_profile_encoding": rel(SOURCE_PROFILE_ENCODING_PATH),
                "source_runtime_parity": rel(SOURCE_RUNTIME_PARITY_PATH),
            },
            "outputs": result["outputs"],
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
        },
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(queue_rows, decision_rows, plan_rows))
    update_ledgers(created_at, queue_rows)
    update_current_truth_docs()
    return result


def main() -> int:
    result = run()
    print(
        json.dumps(
            {
                "status": result["status"],
                "queue_rows": result["queue_row_count"],
                "variant_decisions": result["variant_decision_count"],
                "cross_period_plans": result["cross_period_plan_count"],
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
