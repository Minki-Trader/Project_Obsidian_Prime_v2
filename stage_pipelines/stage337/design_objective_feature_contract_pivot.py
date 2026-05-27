from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CY"
RUN_ID = "run337CY_design_objective_feature_contract_pivot_after_separability_control_failure_without_db_v1"
PARENT_RUN_ID = "run337CX_review_feature_label_separability_control_training_without_db_v1"
NEXT_RUN_ID = "run337CZ_materialize_objective_feature_contract_pivot_inputs_without_db_v1"
STATUS = "completed_stage337CY_objective_feature_contract_pivot_design_no_training_no_selection"
JUDGMENT = "objective_feature_contract_pivot_design_ready_after_separability_control_failure"
DECISION = "stage337CY_open_run337CZ_materialize_objective_feature_contract_pivot_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CY_objective_feature_contract_pivot_design_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CY_objective_pivot_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CY_objective_feature_contract_pivot_design.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CX_DIR = STAGE_DIR / "02_runs" / "run337CX"
CX_FINAL = CX_DIR / "final_decision.json"
CX_GATES = CX_DIR / "required_gate_coverage_audit.csv"
CX_FAILURE = CX_DIR / "failure_attribution_matrix.csv"
CX_RELEASE = CX_DIR / "release_lock_review.csv"
CX_TOP = CX_DIR / "top_readonly_diagnostic_pockets.csv"
CX_CONTROL_COST = CX_DIR / "control_cost_block_summary.csv"
CX_QUEUE = CX_DIR / "run337CY_repair_design_queue.csv"
CW_SCORECARD = STAGE_DIR / "02_runs" / "run337CW" / "guarded_training_scorecard.csv"
CW_TASK_DISPOSITION = STAGE_DIR / "02_runs" / "run337CW" / "task_disposition_matrix.csv"
CV_FEATURE_SETS = STAGE_DIR / "02_runs" / "run337CV" / "control_orthogonal_feature_sets.csv"
CV_LABEL_CONTRACT = STAGE_DIR / "02_runs" / "run337CV" / "label_margin_contract.csv"

OBJECTIVE_PIVOT = RUN_DIR / "objective_family_pivot_design.csv"
FEATURE_CONTRACT = RUN_DIR / "feature_contract_pivot_matrix.csv"
TWO_STAGE_CONTRACT = RUN_DIR / "two_stage_runtime_contract_design.csv"
CONTROL_OBJECTIVE = RUN_DIR / "control_orthogonal_objective_contract.csv"
COST_ABSTENTION = RUN_DIR / "cost_aware_abstention_contract.csv"
ATTACK_DEFENSE_BALANCE = RUN_DIR / "attack_defense_repair_balance_matrix.csv"
NO_OVERFIT_FIREWALL = RUN_DIR / "no_overfit_firewall_contract.csv"
CZ_QUEUE = RUN_DIR / "run337CZ_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CX_FINAL,
    CX_GATES,
    CX_FAILURE,
    CX_RELEASE,
    CX_TOP,
    CX_CONTROL_COST,
    CX_QUEUE,
    CW_SCORECARD,
    CW_TASK_DISPOSITION,
    CV_FEATURE_SETS,
    CV_LABEL_CONTRACT,
)
OUTPUT_FILES = (
    OBJECTIVE_PIVOT,
    FEATURE_CONTRACT,
    TWO_STAGE_CONTRACT,
    CONTROL_OBJECTIVE,
    COST_ABSTENTION,
    ATTACK_DEFENSE_BALANCE,
    NO_OVERFIT_FIREWALL,
    CZ_QUEUE,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    DATA_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

OBJECTIVE_COLUMNS = (
    "objective_id",
    "objective_family",
    "hypothesis",
    "target_definition",
    "profit_curve_intent",
    "control_requirement",
    "train_only_rule",
    "validation_gate",
    "oos_role",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "forbidden_action",
    "next_materialization",
    "claim_boundary",
)
FEATURE_COLUMNS = (
    "feature_contract_id",
    "feature_family",
    "include_rule",
    "exclude_rule",
    "economic_regime_handling",
    "control_reason",
    "expected_effect",
    "invalid_if",
    "forbidden_action",
    "next_materialization",
    "claim_boundary",
)
TWO_STAGE_COLUMNS = (
    "contract_id",
    "stage1_model",
    "stage2_model",
    "handoff_field",
    "runtime_surface",
    "onnx_packaging_rule",
    "proxy_mt5_compare_requirement",
    "blocked_if",
    "effect",
    "claim_boundary",
)
CONTROL_OBJECTIVE_COLUMNS = (
    "contract_id",
    "control_id",
    "objective_rule",
    "residualization_rule",
    "pass_condition",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
COST_COLUMNS = (
    "contract_id",
    "cost_level_points",
    "target_rule",
    "abstention_rule",
    "curve_quality_gate",
    "profit_curve_intent",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
BALANCE_COLUMNS = (
    "lane_id",
    "lane_type",
    "purpose",
    "risk",
    "required_evidence",
    "stop_condition",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "forbidden_pattern",
    "reason",
    "blocks_if_seen",
    "allowed_alternative",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def summarize_inputs() -> dict[str, Any]:
    final = read_json(CX_FINAL)
    failures = read_csv(CX_FAILURE)
    release = read_csv(CX_RELEASE)
    controls = read_csv(CX_CONTROL_COST)
    tasks = read_csv(CW_TASK_DISPOSITION)
    return {
        "final": final,
        "failures": failures,
        "release": release,
        "controls": controls,
        "tasks": tasks,
        "hard_blockers": sum(1 for row in failures if row.get("is_blocker") == "true"),
        "held_two_stage": sum(1 for row in tasks if row.get("training_disposition") == "held_requires_composite_runtime_contract"),
        "best_validation_balanced": float(final.get("best_validation_balanced") or 0.0),
        "best_oos_balanced": float(final.get("best_oos_balanced") or 0.0),
        "control_blocks": int(final.get("control_blocks") or 0),
        "cost_blocks": int(final.get("cost_blocks") or 0),
    }


def build_objectives() -> list[dict[str, str]]:
    return [
        {
            "objective_id": "cost_positive_tradeability_first",
            "objective_family": "tradeability_gate_then_direction(거래가능성 게이트 후 방향)",
            "hypothesis": "Direction labels are too noisy unless tradeability after cost is learned first(비용 후 거래가능성을 먼저 배우지 않으면 방향 라벨이 너무 시끄럽다).",
            "target_definition": "stage1: net_after_cost_positive_or_abstain; stage2: direction only inside stage1 pass(1단계 비용 후 양수/회피, 2단계 통과 구간 방향)",
            "profit_curve_intent": "reduce ugly low-edge trades before chasing high return(고수익을 좇기 전 낮은 엣지 거래를 줄임)",
            "control_requirement": "must weaken label_shift_gap72/gap96 and horizon_modulo controls(라벨 이동 72/96과 기간 모듈로 대조 약화 필수)",
            "train_only_rule": "cost and abstention cutoffs derived from train only(비용과 회피 컷오프는 학습 전용)",
            "validation_gate": "validation PF proxy >1.05, balanced >0.40, control blocks=0 before OOS read(검증 프록시 PF 1.05 초과, 균형 0.40 초과, 대조 차단 0)",
            "oos_role": "read-only stress and not ranking(OOS는 읽기 전용 압박, 순위 아님)",
            "success_criteria": "nonzero review eligible rows and cost curve does not break(리뷰 가능 행 존재와 비용 곡선 유지)",
            "failure_criteria": "validation still below 0.40 or controls aligned(검증 0.40 미만 지속 또는 대조 정렬)",
            "invalid_conditions": "any validation/OOS threshold selection(검증/OOS 임계값 선택 발생)",
            "forbidden_action": "no threshold lowering and no lot optimization(임계값 낮추기와 로트 최적화 금지)",
            "next_materialization": "cost_tradeability_label_frame.parquet",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "asymmetric_payoff_rank",
            "objective_family": "payoff_rank_not_probability(확률이 아닌 보상 순위)",
            "hypothesis": "US100 edge may sit in payoff asymmetry rather than class accuracy(US100 엣지는 클래스 정확도보다 보상 비대칭에 있을 수 있다).",
            "target_definition": "rank forward bars by reward_to_drawdown_after_cost(비용 후 보상/손실비로 전진 구간 순위화)",
            "profit_curve_intent": "prefer fewer but cleaner high convexity trades(적지만 더 깨끗한 볼록성 거래 선호)",
            "control_requirement": "rank must beat shifted controls on validation before OOS read(순위가 OOS 전 검증에서 이동 대조를 이겨야 함)",
            "train_only_rule": "rank bins and tail thresholds from train split only(순위 구간과 꼬리 임계값은 학습 전용)",
            "validation_gate": "top rank bucket validation net positive at cost 2 and 5(상위 순위 버킷이 비용 2/5에서 검증 순양수)",
            "oos_role": "read-only convexity stress(읽기 전용 볼록성 압박)",
            "success_criteria": "monotonic rank buckets and no single day/session pocket dominance(순위 버킷 단조성과 단일 일/세션 지배 없음)",
            "failure_criteria": "rank monotonicity breaks or pocket concentration high(순위 단조성 붕괴 또는 포켓 집중 높음)",
            "invalid_conditions": "rank bucket chosen by OOS best bucket(OOS 최고 버킷으로 순위 선택)",
            "forbidden_action": "no OOS rank selection(OOS 순위 선택 금지)",
            "next_materialization": "payoff_rank_label_frame.parquet",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "control_residual_direction",
            "objective_family": "control_residual_signal(대조 잔차 신호)",
            "hypothesis": "Signal that remains after control proxies may be more robust(대조 프록시 이후 남는 신호가 더 강건할 수 있다).",
            "target_definition": "direction only when label differs from gap72/gap96/modulo controls(라벨이 gap72/gap96/modulo 대조와 다를 때만 방향)",
            "profit_curve_intent": "remove serial-control-like trades before profit evaluation(수익 평가 전 연속 대조형 거래 제거)",
            "control_requirement": "control labels are mandatory inputs and cannot be dropped(대조 라벨은 필수 입력이며 제거 금지)",
            "train_only_rule": "residual eligibility rule fixed from train only(잔차 가능 규칙은 학습 전용 고정)",
            "validation_gate": "control block rows must be zero on validation(검증 대조 차단 행 0)",
            "oos_role": "read-only residual check(읽기 전용 잔차 확인)",
            "success_criteria": "actual beats every control with trade count floor(실제가 모든 대조를 이기고 거래수 하한 충족)",
            "failure_criteria": "controls stay equal or better(대조가 같거나 더 좋음)",
            "invalid_conditions": "control set weakened after seeing result(결과를 본 뒤 대조 약화)",
            "forbidden_action": "no dropping failed controls(실패 대조 제거 금지)",
            "next_materialization": "control_residual_label_frame.parquet",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "two_stage_explicit_handoff",
            "objective_family": "two_model_runtime_surface(2모델 런타임 표면)",
            "hypothesis": "Held two-stage tasks may be useful only with explicit runtime handoff(보류된 2단계 작업은 명시 런타임 인계에서만 쓸 수 있다).",
            "target_definition": "model A gates tradeability, model B ranks direction if A passes(A모델 거래가능성, A 통과 시 B모델 방향 순위)",
            "profit_curve_intent": "keep curve beautiful by separating skip logic from direction logic(스킵 로직과 방향 로직을 분리해 곡선 품질 유지)",
            "control_requirement": "proxy and MT5 must compare both stage decisions(프록시와 MT5가 두 단계 결정을 모두 비교)",
            "train_only_rule": "stage A/B cutoffs from train only(A/B 컷오프 학습 전용)",
            "validation_gate": "both stage parity and validation control clearance required(두 단계 동등성과 검증 대조 통과 필요)",
            "oos_role": "read-only handoff stress(읽기 전용 인계 압박)",
            "success_criteria": "stage handoff has zero schema ambiguity and trade floor(단계 인계 스키마 모호성 0 및 거래 하한)",
            "failure_criteria": "handoff ambiguity or no validation edge(인계 모호성 또는 검증 엣지 없음)",
            "invalid_conditions": "packaged as fake single ONNX(가짜 단일 ONNX로 패키징)",
            "forbidden_action": "no fake single-surface claim(가짜 단일 표면 주장 금지)",
            "next_materialization": "two_stage_handoff_manifest.json",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_feature_contracts() -> list[dict[str, str]]:
    return [
        {
            "feature_contract_id": "technical_session_vol_lag_safe",
            "feature_family": "technical_session_volatility(기술/세션/변동성)",
            "include_rule": "price/return/ATR/volatility/session fields only(가격/수익률/ATR/변동성/세션 필드만)",
            "exclude_rule": "exclude stale macro/equity side sources unless lag-safe audit passes(지연 안전 감사 전 낡은 거시/주식 원천 제외)",
            "economic_regime_handling": "regime used as slice, not direct selection(국면은 슬라이스로만 사용, 직접 선택 아님)",
            "control_reason": "reduce stale-source and control alignment risk(낡은 원천과 대조 정렬 위험 감소)",
            "expected_effect": "cleaner but possibly fewer trades(더 깨끗하나 거래수 감소 가능)",
            "invalid_if": "feature set chosen by OOS result(OOS 결과로 피처 묶음 선택)",
            "forbidden_action": "no OOS feature selection(OOS 피처 선택 금지)",
            "next_materialization": "feature_set_technical_session_vol.json",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_contract_id": "drop_high_state_carry_ge70_plus_cost_context",
            "feature_family": "state_carry_pruned_cost_context(상태 이월 제거 + 비용 문맥)",
            "include_rule": "include low carry features plus ATR/spread cost proxies(낮은 이월 피처와 ATR/스프레드 비용 프록시 포함)",
            "exclude_rule": "drop features with prior max autocorrelation >=0.70(이전 최대 자기상관 0.70 이상 제거)",
            "economic_regime_handling": "cost stress by volatility bucket(변동성 버킷별 비용 압박)",
            "control_reason": "attack serial-dependence-like controls(연속 의존형 대조 공격)",
            "expected_effect": "weaken controls before any profit claim(수익 주장 전 대조 약화)",
            "invalid_if": "high carry features reintroduced without audit(감사 없이 높은 이월 피처 재도입)",
            "forbidden_action": "no hidden feature re-add(숨은 피처 재추가 금지)",
            "next_materialization": "feature_set_state_pruned_cost.json",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_contract_id": "macro_equity_lag_safe_rescue",
            "feature_family": "economic_regime_rescue(경제 국면 구조 구제)",
            "include_rule": "include macro/equity only with explicit lag and stale-age sidecar(명시 지연과 낡음 나이 보조표가 있을 때만 거시/주식 포함)",
            "exclude_rule": "exclude same-bar macro/equity joins(동일봉 거시/주식 결합 제외)",
            "economic_regime_handling": "VIX/USD/rate slices are attribution gates(VIX/USD/금리 슬라이스는 귀속 게이트)",
            "control_reason": "test whether economics helps without leakage(누수 없이 경제 정보가 돕는지 시험)",
            "expected_effect": "possibly improve regime pockets without lookahead(미래참조 없이 국면 포켓 개선 가능)",
            "invalid_if": "any stale-age or timestamp sidecar missing(낡음 나이 또는 시각 보조표 누락)",
            "forbidden_action": "no unlagged external source(지연 없는 외부 원천 금지)",
            "next_materialization": "feature_set_macro_lag_safe.json",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_two_stage_contract() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "two_stage_tradeability_then_direction_v1",
            "stage1_model": "tradeability_after_cost_gate(비용 후 거래가능성 게이트)",
            "stage2_model": "direction_rank_inside_stage1_pass(1단계 통과 구간 방향 순위)",
            "handoff_field": "stage1_pass;stage1_score;stage2_direction;stage2_score;final_action(1단계 통과/점수, 2단계 방향/점수, 최종 행동)",
            "runtime_surface": "two ONNX files plus deterministic adapter(ONNX 두 개 + 결정적 어댑터)",
            "onnx_packaging_rule": "do not merge into fake single ONNX unless converter proves exact composition(정확 합성이 증명되기 전 가짜 단일 ONNX 병합 금지)",
            "proxy_mt5_compare_requirement": "compare both stage scores and final action row-by-row(두 단계 점수와 최종 행동을 행 단위 비교)",
            "blocked_if": "any stage schema field missing or proxy/MT5 mismatch(단계 스키마 필드 누락 또는 프록시/MT5 불일치)",
            "effect": "2단계 아이디어를 런타임 동등성 안에서만 검증한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_control_objectives() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "control_residual_gap72",
            "control_id": "label_shift_gap72_control",
            "objective_rule": "train only when actual label differs from gap72 control(실제 라벨이 gap72 대조와 다를 때만 학습)",
            "residualization_rule": "control label stored as sidecar, never dropped(대조 라벨은 보조표로 저장, 제거 금지)",
            "pass_condition": "validation actual trade balanced > control balanced and control <0.45(검증 실제 거래 균형이 대조보다 높고 대조 0.45 미만)",
            "forbidden_action": "no removing gap72 after failure(실패 후 gap72 제거 금지)",
            "effect": "가장 강한 이동 대조 차단을 정면으로 다룬다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "control_residual_gap96",
            "control_id": "label_shift_gap96_control",
            "objective_rule": "train residual eligibility against gap96( gap96 대비 잔차 가능성 학습)",
            "residualization_rule": "gap96 sidecar joined by source_row_id(source_row_id로 gap96 보조표 결합)",
            "pass_condition": "validation and OOS readonly both show weakened control(검증과 OOS 읽기 전용 모두 대조 약화)",
            "forbidden_action": "no post-hoc control weakening(사후 대조 약화 금지)",
            "effect": "긴 지연 구조와의 동조를 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "control_residual_modulo",
            "control_id": "horizon_modulo_fold_control",
            "objective_rule": "penalize horizon modulo fold mimicry(기간 모듈로 폴드 모방 벌점)",
            "residualization_rule": "fold id can be diagnostic only, not feature(폴드 ID는 진단 전용, 피처 금지)",
            "pass_condition": "modulo control degraded before runtime queue(런타임 대기 전 모듈로 대조 약화)",
            "forbidden_action": "no using fold id as predictive feature(폴드 ID 예측 피처 사용 금지)",
            "effect": "기간 구조 착시를 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_cost_contract() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "cost2_primary_abstention",
            "cost_level_points": "2",
            "target_rule": "positive only if reward exceeds cost2 plus drawdown buffer(보상이 비용2와 손실 버퍼를 넘을 때만 양성)",
            "abstention_rule": "skip if expected edge below train-only cost buffer(기대 엣지가 학습 전용 비용 버퍼 미만이면 스킵)",
            "curve_quality_gate": "validation net positive, PF>1.05, drawdown pocket bounded(검증 순양수, PF 1.05 초과, 손실 포켓 제한)",
            "profit_curve_intent": "protect curve beauty before increasing trade count(거래수 증가 전 곡선 품질 보호)",
            "forbidden_action": "no lot scaling to hide cost failure(비용 실패 은폐용 로트 확대 금지)",
            "effect": "비용에 약한 거래를 먼저 걸러낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "cost5_stress_survivor",
            "cost_level_points": "5",
            "target_rule": "stress survivor label for high conviction only(고확신만 비용5 생존 라벨)",
            "abstention_rule": "skip all medium confidence trades under stress(압박에서 중간 확신 거래 모두 스킵)",
            "curve_quality_gate": "cost5 validation loss pockets do not dominate(비용5 검증 손실 포켓 지배 금지)",
            "profit_curve_intent": "seek explosive return only after stress survival(압박 생존 뒤 폭발 수익 추구)",
            "forbidden_action": "no choosing cost level by OOS(OOS로 비용 수준 선택 금지)",
            "effect": "강한 비용 압박에서도 깨지지 않는 신호만 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_balance() -> list[dict[str, str]]:
    return [
        {
            "lane_id": "defensive_control_first",
            "lane_type": "defensive(방어)",
            "purpose": "kill control-aligned false edges(대조 정렬 가짜 엣지 제거)",
            "risk": "may reduce trade count(거래수 감소 가능)",
            "required_evidence": "control scorecard and residual sidecar(대조 점수표와 잔차 보조표)",
            "stop_condition": "controls still block after residual objective(잔차 목표 뒤에도 대조 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lane_id": "offensive_payoff_rank",
            "lane_type": "offensive(공격)",
            "purpose": "find explosive payoff pockets without OOS selection(OOS 선택 없이 폭발 보상 포켓 탐색)",
            "risk": "tail overfit(꼬리 과적합)",
            "required_evidence": "train/validation monotonic rank buckets and OOS readonly stress(학습/검증 단조 순위 버킷과 OOS 읽기 전용 압박)",
            "stop_condition": "rank monotonicity breaks(순위 단조성 붕괴)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lane_id": "repair_two_stage_handoff",
            "lane_type": "repair(수리)",
            "purpose": "make held two-stage idea runtime-testable(보류 2단계 아이디어를 런타임 시험 가능하게 함)",
            "risk": "handoff complexity(인계 복잡성)",
            "required_evidence": "proxy and MT5 compare fields for both stages(두 단계 프록시/MT5 비교 필드)",
            "stop_condition": "handoff schema ambiguity remains(인계 스키마 모호성 지속)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_firewalls() -> list[dict[str, str]]:
    return [
        {
            "firewall_id": "no_validation_gate_lowering",
            "forbidden_pattern": "lower 0.40 validation balanced gate after failure(실패 후 검증 균형 0.40 게이트 낮추기)",
            "reason": "CX failure was validation quality(검증 품질 실패였음)",
            "blocks_if_seen": "new run uses lower validation balanced gate(새 실행이 낮은 검증 게이트 사용)",
            "allowed_alternative": "change objective before scoring(채점 전 목표 변경)",
            "effect": "실패를 기준 완화로 숨기지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_oos_best_pocket_selection",
            "forbidden_pattern": "choose OOS pocket/model/policy by best rank(OOS 최고 순위로 포켓/모델/정책 선택)",
            "reason": "CX named OOS readonly pocket(읽기 전용 OOS 포켓으로 명명됨)",
            "blocks_if_seen": "OOS rank appears in selection field(OOS 순위가 선택 필드에 등장)",
            "allowed_alternative": "predeclare validation gate then read OOS(검증 게이트 사전 선언 후 OOS 판독)",
            "effect": "또 다른 과적합을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_lot_or_cost_masking",
            "forbidden_pattern": "lot optimization or ignoring cost stress(로트 최적화 또는 비용 압박 무시)",
            "reason": "CX cost blocks were large(CX 비용 차단이 큼)",
            "blocks_if_seen": "profit improves only by lot/cost removal(수익 개선이 로트/비용 제거만으로 발생)",
            "allowed_alternative": "cost-aware abstention target(비용 인식 회피 타깃)",
            "effect": "곡선 품질을 비용 현실 위에 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_fake_single_onnx_two_stage",
            "forbidden_pattern": "claim two-stage as one ONNX without exact adapter proof(정확 어댑터 증명 없이 2단계를 단일 ONNX로 주장)",
            "reason": "two-stage tasks were held for contract gap(2단계 작업은 계약 공백으로 보류됨)",
            "blocks_if_seen": "runtime package hides second-stage decision(런타임 패키지가 2단계 결정을 숨김)",
            "allowed_alternative": "two ONNX plus deterministic adapter(ONNX 두 개와 결정적 어댑터)",
            "effect": "proxy/MT5 parity(프록시/MT5 동등성)를 지킨다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_cz_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337CZ_materialize_cost_tradeability_labels",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize cost tradeability and payoff rank labels(비용 거래가능성 및 보상 순위 라벨 물질화)",
            "required_inputs": f"{rel(OBJECTIVE_PIVOT)};{rel(COST_ABSTENTION)}",
            "required_outputs": "cost_tradeability_label_frame.parquet;payoff_rank_label_frame.parquet",
            "blocked_if_missing": "objective/cost contracts missing(목표/비용 계약 누락)",
            "forbidden_action": "no validation/OOS threshold tuning(검증/OOS 임계값 조정 금지)",
            "effect": "수익곡선 품질을 라벨부터 다룬다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CZ_materialize_control_residual_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize control residual sidecars(대조 잔차 보조표 물질화)",
            "required_inputs": rel(CONTROL_OBJECTIVE),
            "required_outputs": "control_residual_label_frame.parquet;control_sidecar_matrix.csv",
            "blocked_if_missing": "control objective contract missing(대조 목표 계약 누락)",
            "forbidden_action": "no dropping failed controls(실패 대조 제거 금지)",
            "effect": "대조 정렬을 학습 입력에서 직접 다룬다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CZ_materialize_feature_contracts",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize feature contract sets(피처 계약 묶음 물질화)",
            "required_inputs": rel(FEATURE_CONTRACT),
            "required_outputs": "feature_contract_manifest.json;feature_set_matrix.csv",
            "blocked_if_missing": "feature contract missing(피처 계약 누락)",
            "forbidden_action": "no hidden feature re-add(숨은 피처 재추가 금지)",
            "effect": "피처 원천과 대조 위험을 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CZ_materialize_two_stage_handoff",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "materialize two-stage handoff manifest(2단계 인계 목록 물질화)",
            "required_inputs": rel(TWO_STAGE_CONTRACT),
            "required_outputs": "two_stage_handoff_manifest.json;proxy_mt5_two_stage_compare_contract.csv",
            "blocked_if_missing": "two-stage contract missing(2단계 계약 누락)",
            "forbidden_action": "no fake single ONNX claim(가짜 단일 ONNX 주장 금지)",
            "effect": "2단계 모델을 런타임 동등성 안에서만 다음으로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]

    def row(gate_id: str, ok: bool, observed: Any, expected: str, effect: str) -> dict[str, str]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": str(observed),
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    return [
        row("cy_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CX 실패 귀속과 CW/CV 산출물에 연결한다."),
        row("cy_gate_parent_points_to_cy", final["cx_next_action"] == RUN_ID, final["cx_next_action"], RUN_ID, "CX next_action(다음 행동)과 CY 실행을 맞춘다."),
        row("cy_gate_objective_rows", final["objective_rows"] >= 4, final["objective_rows"], ">=4", "목표 계열 전환을 충분히 설계한다."),
        row("cy_gate_feature_contract_rows", final["feature_contract_rows"] >= 3, final["feature_contract_rows"], ">=3", "피처 계약 전환을 만든다."),
        row("cy_gate_firewalls", final["firewall_rows"] >= 4, final["firewall_rows"], ">=4", "과적합 방화벽을 명시한다."),
        row("cy_gate_two_stage_contract", final["two_stage_contract_rows"] == 1, final["two_stage_contract_rows"], "1", "2단계 인계 계약을 별도 명시한다."),
        row("cy_gate_cz_queue", final["queue_rows"] >= 4, final["queue_rows"], ">=4", "CZ 입력 물질화 대기열을 연다."),
        row("cy_gate_no_training_selection_mt5", True, "training=not_run;selection=not_run;mt5=not_run", "no training/selection/MT5", "설계를 후보 선택으로 바꾸지 않는다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    experiment_receipt = {
        "hypothesis": "CW failed because objective and feature contracts still model noisy direction/control-aligned edges(CW 실패는 목표/피처 계약이 여전히 시끄러운 방향/대조 정렬 엣지를 모델링했기 때문일 수 있다).",
        "decision_use": "open CZ materialization only(CZ 물질화만 열기)",
        "comparison_baseline": "run337CX failure attribution(CX 실패 귀속)",
        "control_variables": "no validation/OOS threshold tuning, no lot optimization, no MT5 probe(검증/OOS 임계값 조정, 로트 최적화, MT5 탐침 없음)",
        "changed_variables": "objective families, feature contracts, two-stage handoff, cost-aware abstention(목표 계열, 피처 계약, 2단계 인계, 비용 인식 회피)",
        "sample_scope": "design only from existing Stage337 artifacts(기존 337단계 산출물 기반 설계 전용)",
        "success_criteria": "CZ can materialize leakage-safe inputs(CZ가 누수 없는 입력을 만들 수 있음)",
        "failure_criteria": "contracts missing firewall or repeat OOS selection(계약이 방화벽을 빠뜨리거나 OOS 선택 반복)",
        "invalid_conditions": "any training or selection in CY(CY에서 학습 또는 선택 발생)",
        "stop_conditions": "gate failure or missing CX evidence(게이트 실패 또는 CX 근거 누락)",
        "evidence_plan": [rel(path) for path in artifact_paths],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "design only, no model training(설계 전용, 모델 학습 없음)",
        "target_and_label": "cost tradeability, payoff rank, control residual, two-stage handoff contracts(비용 거래가능성, 보상 순위, 대조 잔차, 2단계 인계 계약)",
        "split_method": "train-only future materialization; validation/OOS read-only(향후 학습 전용 물질화, 검증/OOS 읽기 전용)",
        "selection_metric": "not_applicable_no_selection(해당 없음, 선택 없음)",
        "secondary_metrics": "controls, cost, curve pockets, proxy-MT5 compare readiness(대조, 비용, 곡선 포켓, 프록시-MT5 비교 준비)",
        "threshold_policy": "predeclare train-only(사전 선언 학습 전용)",
        "overfit_risk": "OOS pocket selection and threshold lowering(OOS 포켓 선택과 임계값 낮추기)",
        "calibration_risk": "future rank scores are not probabilities(향후 순위 점수는 확률이 아님)",
        "comparison_baseline": PARENT_RUN_ID,
        "validation_judgment": "design_ready_for_materialization",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherited from prior artifacts, no new rows joined(기존 산출물 상속, 새 행 결합 없음)",
        "sample_scope": "design only using existing shared-window evidence(기존 공유 구간 근거 기반 설계 전용)",
        "missing_or_duplicate_check": "input presence gate(입력 존재 게이트)",
        "feature_label_boundary": "future labels are only specified for CZ, not created in CY(미래 라벨은 CZ용 명세만 있고 CY에서 만들지 않음)",
        "split_boundary": "train-only rules specified; validation/OOS read-only(학습 전용 규칙 명세, 검증/OOS 읽기 전용)",
        "leakage_risk": "macro/equity lag source and OOS selection(거시/주식 지연 원천 및 OOS 선택)",
        "data_hash_or_identity": {"cx_final_sha256": sha256_file(CX_FINAL)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "attribution_subject": RUN_ID,
        "from_failure": "validation/control/cost block(CX 검증/대조/비용 차단)",
        "performance_intent": "beautiful curve, trade count floor, explosive payoff only after cost/control survival(아름다운 곡선, 거래수 하한, 비용/대조 생존 후 폭발 보상)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "design contracts, firewalls, CZ queue(설계 계약, 방화벽, CZ 대기열)",
        "evidence_missing": "materialized inputs, training, ONNX, proxy/MT5(물질화 입력, 학습, ONNX, 프록시/MT5)",
        "judgment_label": "exploratory_design_ready",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "이번 실행은 방향을 바꾼 설계이지 아직 새 모델 성과가 아니다.",
    }
    receipt_paths = [
        write_json(EXPERIMENT_RECEIPT, experiment_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifact_paths] + [rel(path) for path in receipt_paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + receipt_paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_design_and_ignored_run_outputs(추적 설계와 무시된 실행 산출물)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipt_paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return receipt_paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CY Objective/Feature Pivot Design(목표/피처 전환 설계)

## Conclusion(결론)

run337CY(337CY 실행)는 CX 실패를 threshold lowering(임계값 낮추기)으로 덮지 않고 objective family pivot(목표 계열 전환)으로 바꿨다. 설계는 cost tradeability(비용 거래가능성), payoff rank(보상 순위), control residual(대조 잔차), two-stage handoff(2단계 인계)를 다음 물질화 대상으로 연다.

Effect(효과): 다음 run337CZ(337CZ 실행)는 수익곡선 품질(profit curve quality, 수익곡선 품질)을 라벨과 피처 계약부터 다시 만든다. 모델 학습, 후보 선택, MT5 probe(MT5 탐침), Forward/Goal(전진/목표)은 아직 주장하지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- objective_rows(목표 행): `{final["objective_rows"]}`
- feature_contract_rows(피처 계약 행): `{final["feature_contract_rows"]}`
- two_stage_contract_rows(2단계 계약 행): `{final["two_stage_contract_rows"]}`
- cost_contract_rows(비용 계약 행): `{final["cost_contract_rows"]}`
- firewall_rows(방화벽 행): `{final["firewall_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- new_training(새 학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CY

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): validation/control/cost(검증/대조/비용) 실패를 목표/피처 계약 전환으로 바꾸고 CZ 물질화를 열었다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(OBJECTIVE_PIVOT)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs() -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337CY focus complete: objective/feature contract pivot design(목표/피처 계약 전환 설계)을 "
        f"`{STATUS}`로 닫았다. Effect(효과): run337CZ(337CZ 실행)에서 cost tradeability/payoff rank/control residual/two-stage handoff(비용 거래가능성/보상 순위/대조 잔차/2단계 인계) 입력을 물질화한다."
    )
    workspace_text = workspace_text.replace("current_focus:", focus_entry, 1)
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{STATUS}`",
        "decision": f"`{DECISION}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""
## Stage337 run337CY(337CY 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): cost tradeability/payoff rank/control residual/two-stage handoff(비용 거래가능성/보상 순위/대조 잔차/2단계 인계) 설계를 만들었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337CX(337CX"
    current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{STATUS}`
- actual_mt5_execution(실제 MT5 실행): `not_run_cy_design_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 objective/feature contract pivot input materialization(목표/피처 계약 전환 입력 물질화)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337CY(337CY 실행) designed objective/feature contract pivot(목표/피처 계약 전환 설계). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337CY designed objective/feature contract pivot(목표/피처 계약 전환 설계) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "objective_feature_contract_pivot_design_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"objectives={final['objective_rows']};feature_contracts={final['feature_contract_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design_data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__objective_pivot_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "objective_pivot_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "design_no_training",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "design_contract_no_kpi",
        "scoreboard_lane": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"objective_rows={final['objective_rows']};firewalls={final['firewall_rows']}",
        "guardrail_kpi": "no_threshold_lowering;no_oos_selection;no_fake_two_stage_onnx",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__objective_pivot_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "CX failure converted into objective feature contract design",
        "kpi_scope": "design_contract_no_training",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__objective_pivot_design",
        "family": "experiment_design_data_integrity_model_validation_artifact_lineage",
        "question": "what objective and feature contracts should follow separability/control failure",
        "metric_scope": "design_contract_firewall_queue",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    artifacts = [
        upsert_csv(RUN_REGISTRY, "run_id", run_row),
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row),
        upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row),
    ]
    artifact_columns: list[str] = []
    artifact_rows: list[dict[str, str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            artifact_columns = list(reader.fieldnames or [])
            artifact_rows = [dict(row) for row in reader]
    if not artifact_columns:
        artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    summary = summarize_inputs()
    objectives = build_objectives()
    feature_contracts = build_feature_contracts()
    two_stage = build_two_stage_contract()
    control_objectives = build_control_objectives()
    cost_contracts = build_cost_contract()
    balance = build_balance()
    firewalls = build_firewalls()
    queue_rows = build_cz_queue()
    artifacts: list[Path] = [
        write_csv(OBJECTIVE_PIVOT, OBJECTIVE_COLUMNS, objectives),
        write_csv(FEATURE_CONTRACT, FEATURE_COLUMNS, feature_contracts),
        write_csv(TWO_STAGE_CONTRACT, TWO_STAGE_COLUMNS, two_stage),
        write_csv(CONTROL_OBJECTIVE, CONTROL_OBJECTIVE_COLUMNS, control_objectives),
        write_csv(COST_ABSTENTION, COST_COLUMNS, cost_contracts),
        write_csv(ATTACK_DEFENSE_BALANCE, BALANCE_COLUMNS, balance),
        write_csv(NO_OVERFIT_FIREWALL, FIREWALL_COLUMNS, firewalls),
        write_csv(CZ_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "cx_next_action": summary["final"].get("next_action", ""),
        "cx_best_validation_balanced": summary["best_validation_balanced"],
        "cx_best_oos_balanced": summary["best_oos_balanced"],
        "cx_control_blocks": summary["control_blocks"],
        "cx_cost_blocks": summary["cost_blocks"],
        "hard_blockers": summary["hard_blockers"],
        "held_two_stage_rows": summary["held_two_stage"],
        "objective_rows": len(objectives),
        "feature_contract_rows": len(feature_contracts),
        "two_stage_contract_rows": len(two_stage),
        "control_objective_rows": len(control_objectives),
        "cost_contract_rows": len(cost_contracts),
        "balance_rows": len(balance),
        "firewall_rows": len(firewalls),
        "queue_rows": len(queue_rows),
        "model_training": "not_run_design_only",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
