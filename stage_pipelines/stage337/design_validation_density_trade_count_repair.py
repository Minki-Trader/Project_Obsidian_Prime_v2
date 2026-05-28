from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import review_guarded_transfer_density_control_training as ea  # noqa: E402
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
STAGE_ID = ea.STAGE_ID
RUN_NUMBER = "run337EB"
RUN_ID = "run337EB_design_validation_density_trade_count_repair_without_db_v1"
PARENT_RUN_ID = ea.RUN_ID
NEXT_RUN_ID = "run337EC_materialize_validation_density_trade_count_repair_inputs_without_db_v1"
STATUS = "completed_stage337EB_validation_density_trade_count_repair_design_no_training_no_selection"
JUDGMENT = "repair_design_ready_for_train_only_validation_density_trade_count_materialization"
DECISION = "stage337EB_open_run337EC_materialize_validation_density_trade_count_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EB_validation_density_trade_count_repair_design_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ea.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ea.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EB_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EB_repair_design.md"
SELECTED_STATUS = ea.SELECTED_STATUS
STAGE_BRIEF = ea.STAGE_BRIEF
WORKSPACE_STATE = ea.WORKSPACE_STATE
CURRENT_STATE = ea.CURRENT_STATE
CHANGELOG = ea.CHANGELOG
RUN_REGISTRY = ea.RUN_REGISTRY
ALPHA_LEDGER = ea.ALPHA_LEDGER
ARTIFACT_REGISTRY = ea.ARTIFACT_REGISTRY
STAGE_LEDGER = ea.STAGE_LEDGER

EA_FINAL = ea.FINAL_DECISION
EA_GATES = ea.REQUIRED_GATE_AUDIT
EA_QUEUE = ea.EB_QUEUE
CANDIDATE_REVIEW = ea.CANDIDATE_TRAINING_REVIEW
CONTROL_DENSITY_REVIEW = ea.CONTROL_DENSITY_SPLIT_REVIEW
FAILURE_MEMORY = ea.FAILURE_MEMORY_UPDATE
DZ_MODEL_MANIFEST = ea.MODEL_MANIFEST
DZ_TRADE_SCORECARD = ea.PROXY_TRADE_SCORECARD
DZ_DENSITY_AUDIT = ea.DENSITY_GUARD_AUDIT
DZ_AUXILIARY_TAG_SUMMARY = STAGE_DIR / "02_runs" / "run337DZ" / "auxiliary_tag_summary.csv"

REPAIR_DESIGN = RUN_DIR / "validation_density_trade_count_repair_design.csv"
OBJECTIVE_CONTRACTS = RUN_DIR / "objective_repair_contracts.csv"
MODEL_VARIANT_CONTRACTS = RUN_DIR / "model_variant_contracts.csv"
GUARDRAIL_CONTRACTS = RUN_DIR / "density_trade_count_guardrails.csv"
OOS_QUARANTINE = RUN_DIR / "oos_pocket_quarantine_contract.csv"
ARTIFACT_PRESERVATION = RUN_DIR / "artifact_preservation_review.csv"
EC_QUEUE = RUN_DIR / "run337EC_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EA_FINAL,
    EA_GATES,
    EA_QUEUE,
    CANDIDATE_REVIEW,
    CONTROL_DENSITY_REVIEW,
    FAILURE_MEMORY,
    DZ_MODEL_MANIFEST,
    DZ_TRADE_SCORECARD,
    DZ_DENSITY_AUDIT,
    DZ_AUXILIARY_TAG_SUMMARY,
)
OUTPUT_FILES = (
    REPAIR_DESIGN,
    OBJECTIVE_CONTRACTS,
    MODEL_VARIANT_CONTRACTS,
    GUARDRAIL_CONTRACTS,
    OOS_QUARANTINE,
    ARTIFACT_PRESERVATION,
    EC_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
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

DESIGN_COLUMNS = (
    "design_id",
    "problem_signal",
    "hypothesis",
    "decision_use",
    "changed_variables",
    "control_variables",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "effect",
    "claim_boundary",
)
OBJECTIVE_COLUMNS = (
    "contract_id",
    "contract_family",
    "train_only_source",
    "materialization_rule",
    "forbidden_use",
    "expected_effect",
    "claim_boundary",
)
MODEL_VARIANT_COLUMNS = (
    "variant_id",
    "model_family",
    "parameter_contract",
    "why_included",
    "forbidden_use",
    "claim_boundary",
)
GUARDRAIL_COLUMNS = (
    "guardrail_id",
    "guard_type",
    "review_rule",
    "blocks_release_if",
    "effect",
    "claim_boundary",
)
QUARANTINE_COLUMNS = (
    "quarantine_id",
    "trigger",
    "quarantine_rule",
    "allowed_use",
    "forbidden_use",
    "claim_boundary",
)
PRESERVE_COLUMNS = (
    "artifact_id",
    "source_path",
    "preservation_status",
    "allowed_use",
    "forbidden_use",
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


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def load_context() -> dict[str, Any]:
    final = read_json(EA_FINAL)
    candidates = pd.read_csv(io_path(CANDIDATE_REVIEW))
    density = pd.read_csv(io_path(DZ_DENSITY_AUDIT))
    trade = pd.read_csv(io_path(DZ_TRADE_SCORECARD))
    best_validation_id = str(final.get("best_validation_model_id", ""))
    best_rows = candidates.loc[candidates["model_id"].astype(str).eq(best_validation_id)]
    validation_pf = candidates["validation_pf"].astype(float)
    validation_trades = candidates["validation_trade_count"].astype(int)
    density_pressure_models = int(
        candidates.loc[candidates["validation_density_pressure_rows"].astype(int) > 0, "model_id"].nunique()
    )
    return {
        "final": final,
        "candidates": candidates,
        "density": density,
        "trade": trade,
        "best_candidate": best_rows.iloc[0].to_dict() if len(best_rows) else {},
        "validation_pf_pass_rows": int((validation_pf >= 1.05).sum()),
        "validation_trade_pass_rows": int((validation_trades >= 500).sum()),
        "validation_both_pass_rows": int(((validation_pf >= 1.05) & (validation_trades >= 500)).sum()),
        "density_pressure_models": density_pressure_models,
    }


def build_design_rows(context: Mapping[str, Any]) -> list[dict[str, str]]:
    final = context["final"]
    core_signal = (
        f"best_validation_pf={final.get('best_validation_pf')};"
        f"best_validation_trade_count={final.get('best_validation_trade_count')};"
        f"density_pressure_rows={final.get('density_validation_pressure_rows')}"
    )
    return [
        {
            "design_id": "validation_trade_count_lift_without_threshold",
            "problem_signal": core_signal,
            "hypothesis": "near-margin trade support(근접 마진 거래 지지)를 학습 전용(train-only, 학습 전용)으로 넣으면 threshold tuning(임계값 조정) 없이 482 trades(482 거래)를 500 이상으로 올릴 수 있다.",
            "decision_use": "EC materialization(EC 물질화) 설계만 열고 selection(선택)은 금지한다.",
            "changed_variables": "ExtraTrees leaf/depth(리프/깊이)와 train-only sample weight(학습 전용 표본 가중치).",
            "control_variables": "feature order(피처 순서), split(분할), score threshold(점수 임계값), lot logic(랏 로직), OOS selector(OOS 선택기)를 고정한다.",
            "success_criteria": "validation PF(검증 PF) >= 1.05, validation trades(검증 거래수) >= 500, density pressure(밀도 압력) 없음.",
            "failure_criteria": "PF가 1.05 미만이거나 거래수가 500 미만이거나 밀도 압력이 남는다.",
            "invalid_conditions": "validation/OOS(검증/OOS) 행을 가중치, 목표, 임계값 산정에 쓰면 무효다.",
            "stop_conditions": "학습 전용 가중치나 피처 순서가 감사되지 않으면 다음 학습으로 넘기지 않는다.",
            "evidence_plan": "EC input frame(입력 프레임), ED training scorecard(학습 점수표), ONNX parity(ONNX 동등성), density audit(밀도 감사).",
            "effect": "post-hoc filter(사후 필터) 없이 거래수 부족을 공격한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "density_pressure_deconcentration",
            "problem_signal": f"validation_density_pressure_rows={final.get('density_validation_pressure_rows')};density_pressure_models={context['density_pressure_models']}",
            "hypothesis": "고밀도 후보는 action density transfer(행동 밀도 전이)가 과격해서 무너졌으므로, train-only density-tempered weighting(학습 전용 밀도 완화 가중치)이 압력을 줄일 수 있다.",
            "decision_use": "density guard(밀도 가드)를 EC/ED review(EC/ED 검토)의 hard blocker(강한 차단 조건)로 둔다.",
            "changed_variables": "학습 전용 class/sample weight(클래스/표본 가중치)와 모델 용량(capacity, 용량).",
            "control_variables": "scoring after training(학습 후 점수화)에서 density threshold search(밀도 임계값 탐색)를 하지 않는다.",
            "success_criteria": "validation density pressure rows(검증 밀도 압력 행)가 0이고 거래수 하한이 유지된다.",
            "failure_criteria": "밀도 압력이 지속되거나 PF가 붕괴한다.",
            "invalid_conditions": "검증 밀도 결과로 학습 가중치를 다시 고르면 무효다.",
            "stop_conditions": "수리가 사후 밀도 필터를 요구하면 중지한다.",
            "evidence_plan": "density_trade_count_guardrails.csv와 ED density_guard_audit.csv.",
            "effect": "밀도 수리를 학습 설계 안에 묶어 과적합 루프를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "thin_oos_pocket_quarantine",
            "problem_signal": f"best_oos_pf={final.get('best_oos_pf')};best_oos_trade_count={final.get('best_oos_trade_count')}",
            "hypothesis": "높은 OOS PF(OOS 수익계수)는 표본이 38 trades(38 거래)뿐이면 warning signal(경고 신호)이지 selector(선택기)가 아니다.",
            "decision_use": "thin OOS pocket(얇은 OOS 포켓)을 격리하고 validation support(검증 지지)가 생기기 전 선택을 막는다.",
            "changed_variables": "모델 변수는 바꾸지 않고 release rule(해제 규칙)만 문서화한다.",
            "control_variables": "OOS는 read-only evidence(읽기 전용 근거)로만 둔다.",
            "success_criteria": "OOS PF만 높은 후보가 선택되지 않는다.",
            "failure_criteria": "향후 검토가 얇은 OOS 포켓을 선택 근거로 쓰면 실패다.",
            "invalid_conditions": "OOS 포켓이 EC 학습 목표나 가중치에 들어가면 무효다.",
            "stop_conditions": "OOS 기반 선택 흔적이 보이면 branch(분기)를 무효 처리한다.",
            "evidence_plan": "oos_pocket_quarantine_contract.csv와 release disposition(해제 처분).",
            "effect": "좋아 보이는 얇은 구간에 다시 과적합되는 길을 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "offensive_payoff_tail_support",
            "problem_signal": "user goal(사용자 목표)은 높은 profit(수익)을 원하지만 현재 검증 edge(우위)는 얇다.",
            "hypothesis": "train-only payoff-tail support(학습 전용 보상 꼬리 지지)를 넣으면 validation/OOS retune(검증/OOS 재조정) 없이 공격성을 키울 수 있다.",
            "decision_use": "EC 입력에 offensive branch(공격적 분기)를 추가하되 검증 게이트를 유지한다.",
            "changed_variables": "train-only payoff-tail weights(학습 전용 보상 꼬리 가중치).",
            "control_variables": "split(분할), feature set(피처 묶음), threshold(임계값), lot(랏)을 고정한다.",
            "success_criteria": "control/density failure(대조/밀도 실패) 없이 validation PF/trades(검증 PF/거래수)가 좋아진다.",
            "failure_criteria": "OOS만 좋아지고 검증이 약하면 실패다.",
            "invalid_conditions": "payoff tail(보상 꼬리)을 검증/OOS에서 학습하면 무효다.",
            "stop_conditions": "가중치 생성 근거를 해시와 표로 감사할 수 없으면 중지한다.",
            "evidence_plan": "objective_repair_contracts.csv와 다음 ED scorecard(ED 점수표).",
            "effect": "수익 공격성을 넣되 no-lookahead boundary(미래참조 방지 경계)를 유지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "control_gate_preservation",
            "problem_signal": f"control_block_rows={final.get('control_block_rows')};release_candidate_rows={final.get('release_candidate_rows')}",
            "hypothesis": "negative controls(부정 대조)는 통과했지만 그 자체가 release evidence(해제 근거)는 아니다.",
            "decision_use": "controls(대조)를 다음 학습의 hard gate(강한 게이트)로 보존한다.",
            "changed_variables": "없음. 감사 게이트만 이월한다.",
            "control_variables": "shifted/noise/block controls(이동/소음/차단 대조)를 완화하지 않는다.",
            "success_criteria": "수리 후에도 control block(대조 차단)이 0이다.",
            "failure_criteria": "수리 후보가 대조에서만 좋아지거나 대조 실패를 낸다.",
            "invalid_conditions": "control relaxation(대조 완화)이 들어가면 무효다.",
            "stop_conditions": "대조 산출물이 빠지면 학습 검토를 닫지 않는다.",
            "evidence_plan": "guardrail contracts(가드레일 계약)와 control scorecard(대조 점수표).",
            "effect": "수리 실험이 또 다른 과적합 실험이 되지 않게 붙잡는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_objective_contracts() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "train_only_near_margin_trade_support",
            "contract_family": "trade_count_lift(거래수 증가)",
            "train_only_source": "train split(학습 분할)의 costed action label(비용 반영 행동 라벨)과 return margin(수익 여백).",
            "materialization_rule": "거래 라벨이 있고 비용 초과 여백이 학습 q45 이하인 행만 사전 선언 가중치로 보강한다.",
            "forbidden_use": "validation trade threshold tuning(검증 거래 임계값 조정).",
            "expected_effect": "score threshold(점수 임계값)을 바꾸지 않고 근접 포켓 거래수를 높인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "train_only_density_tempered_class_prior",
            "contract_family": "density_deconcentration(밀도 분산)",
            "train_only_source": "train class prior(학습 클래스 비율)와 feature family audit(피처 계열 감사).",
            "materialization_rule": "모든 후보를 고정 class/sample weights(클래스/표본 가중치)로 학습하고 밀도는 점수화 후 감사만 한다.",
            "forbidden_use": "post-hoc density filter(사후 밀도 필터) 또는 validation density search(검증 밀도 탐색).",
            "expected_effect": "고밀도 collapse(붕괴)를 줄이고 낮은 밀도 tree branch(트리 분기)를 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "train_only_payoff_tail_offense",
            "contract_family": "offensive_profit_shape(공격적 수익 형태)",
            "train_only_source": "train-only positive payoff quantiles(학습 전용 양수 보상 분위).",
            "materialization_rule": "수익 꼬리 행을 사전 최대값 이하 가중치로 보강한다.",
            "forbidden_use": "OOS pocket selection(OOS 포켓 선택) 또는 validation-tail retune(검증 꼬리 재조정).",
            "expected_effect": "얇은 OOS 선택기를 만들지 않고 보상 크기를 키운다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "control_gate_carry_forward",
            "contract_family": "overfit_control(과적합 대조)",
            "train_only_source": "EA control clearance(EA 대조 통과)와 DZ control scorecards(DZ 대조 점수표).",
            "materialization_rule": "shifted/noise/block controls(이동/소음/차단 대조)를 ED release blocker(ED 해제 차단 조건)로 이월한다.",
            "forbidden_use": "control relaxation(대조 완화).",
            "expected_effect": "repair branch(수리 분기)가 과적합 분기로 바뀌는 일을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_model_variants() -> list[dict[str, str]]:
    return [
        {
            "variant_id": "extratrees_depth7_leaf80_trade_lift",
            "model_family": "ExtraTreesClassifier(엑스트라 트리 분류기)",
            "parameter_contract": "n_estimators=144;max_depth=7;min_samples_leaf=80;class_weight=balanced.",
            "why_included": "DZ leaf120보다 덜 보수적이어서 근접 거래수 부족을 밀어볼 수 있다.",
            "forbidden_use": "validation result(검증 결과)를 보고 leaf/depth(리프/깊이)를 다시 고르지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "variant_id": "extratrees_depth6_leaf90_density_guard",
            "model_family": "ExtraTreesClassifier(엑스트라 트리 분류기)",
            "parameter_contract": "n_estimators=144;max_depth=6;min_samples_leaf=90;class_weight=balanced.",
            "why_included": "leaf120보다 거래수는 넓히되 depth(깊이)를 제한해 밀도 폭주를 막는다.",
            "forbidden_use": "density threshold(밀도 임계값) 사후 탐색.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "variant_id": "extratrees_depth8_leaf100_payoff_tail",
            "model_family": "ExtraTreesClassifier(엑스트라 트리 분류기)",
            "parameter_contract": "n_estimators=180;max_depth=8;min_samples_leaf=100;payoff_tail_weight=predeclared.",
            "why_included": "공격적 payoff tail(보상 꼬리)을 담되 leaf floor(리프 하한)로 과도한 세분화를 막는다.",
            "forbidden_use": "OOS PF(OOS 수익계수)를 보고 선택.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "variant_id": "hist_gradient_depth4_l2_trade_support",
            "model_family": "HistGradientBoostingClassifier(히스토그램 그래디언트 부스팅 분류기)",
            "parameter_contract": "max_leaf_nodes=31;max_iter=160;l2_regularization=0.20;learning_rate=0.035.",
            "why_included": "tree ensemble(트리 앙상블)과 다른 bias(편향)를 주되 regularization(정규화)을 강하게 둔다.",
            "forbidden_use": "unsupported ONNX path(미지원 ONNX 경로)이면 EC에서 제외한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_guardrails() -> list[dict[str, str]]:
    return [
        {
            "guardrail_id": "no_validation_threshold_tuning",
            "guard_type": "anti_overfit(과적합 방지)",
            "review_rule": "score threshold(점수 임계값)은 EB/EC/ED 전체에서 고정한다.",
            "blocks_release_if": "threshold search(임계값 탐색) 흔적이 발견된다.",
            "effect": "수익 개선이 재튜닝 착시인지 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "validation_pf_trade_floor_joint_gate",
            "guard_type": "validation_floor(검증 하한)",
            "review_rule": "validation PF(검증 PF) >= 1.05와 validation trades(검증 거래수) >= 500을 동시에 본다.",
            "blocks_release_if": "둘 중 하나라도 미달한다.",
            "effect": "얇은 고PF 또는 낮은 우위 고거래수 후보를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "density_transfer_guard",
            "guard_type": "density_stability(밀도 안정성)",
            "review_rule": "train 대비 validation/OOS action density(행동 밀도) 점프를 감사한다.",
            "blocks_release_if": "validation density pressure(검증 밀도 압력)가 남는다.",
            "effect": "브로커 실전형 과밀 거래 위험을 조기에 차단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "thin_oos_quarantine",
            "guard_type": "oos_quarantine(OOS 격리)",
            "review_rule": "OOS trade count(OOS 거래수)가 100 미만인 고PF 후보는 선택 근거로 쓰지 않는다.",
            "blocks_release_if": "thin OOS pocket(얇은 OOS 포켓)이 release argument(해제 주장)에 쓰인다.",
            "effect": "작은 표본 우연성을 다음 분기 선택기로 만들지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "control_gate_hard_carry",
            "guard_type": "negative_control(부정 대조)",
            "review_rule": "shifted/noise/block controls(이동/소음/차단 대조)는 계속 hard gate(강한 게이트)다.",
            "blocks_release_if": "control block rows(대조 차단 행)가 0보다 크다.",
            "effect": "수리된 후보가 데이터 착시를 먹고 좋아지는지 잡는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "runtime_firewall_no_mt5",
            "guard_type": "claim_boundary(주장 경계)",
            "review_rule": "EB는 design only(설계 전용)라 MT5/runtime/forward(메타트레이더5/런타임/전진)를 주장하지 않는다.",
            "blocks_release_if": "selection, MT5, forward, live readiness(선택/MT5/전진/라이브 준비) 표현이 긍정 주장으로 등장한다.",
            "effect": "연구 설계와 운영 주장을 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_quarantine(final: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "quarantine_id": "best_oos_pf_thin_sample",
            "trigger": f"best_oos_pf={final.get('best_oos_pf')};best_oos_trade_count={final.get('best_oos_trade_count')}",
            "quarantine_rule": "OOS trade count(OOS 거래수) < 100인 고PF 포켓은 warning(경고)으로만 둔다.",
            "allowed_use": "failure memory(실패 기억), diagnostic attribution(진단 분해), future stress target(미래 압박 대상).",
            "forbidden_use": "selection(선택), threshold tuning(임계값 조정), lot optimization(랏 최적화), release claim(해제 주장).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "quarantine_id": "validation_support_required_before_oos_use",
            "trigger": "validation_both_floor_pass_rows=0",
            "quarantine_rule": "validation PF/trades(검증 PF/거래수) 공동 하한이 통과되기 전 OOS 포켓을 우승 근거로 쓰지 않는다.",
            "allowed_use": "regime slice question(레짐 조각 질문)과 curve pocket audit(곡선 포켓 감사).",
            "forbidden_use": "winner selection(승자 선택).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_preservation_rows() -> list[dict[str, str]]:
    sources = [
        ("ea_final_decision", EA_FINAL),
        ("ea_failure_memory", FAILURE_MEMORY),
        ("dz_model_manifest", DZ_MODEL_MANIFEST),
        ("dz_trade_scorecard", DZ_TRADE_SCORECARD),
        ("dz_density_audit", DZ_DENSITY_AUDIT),
    ]
    rows = []
    for artifact_id, path in sources:
        rows.append(
            {
                "artifact_id": artifact_id,
                "source_path": rel(path),
                "preservation_status": "preserved_as_research_evidence(연구 근거로 보존)",
                "allowed_use": "design input(설계 입력) and failure memory(실패 기억).",
                "forbidden_use": "runtime authority(런타임 권위), operating promotion(운영 승격), goal achieve(목표 달성).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_ec_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "materialize_train_only_repair_frame",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train-only repair frame(학습 전용 수리 프레임) 생성.",
            "required_inputs": f"{rel(REPAIR_DESIGN)};{rel(OBJECTIVE_CONTRACTS)}",
            "required_outputs": "train_only_validation_density_trade_count_frame.parquet;objective_contract_audit.csv",
            "blocked_if_missing": "source train rows(원천 학습 행), feature order(피처 순서), objective contracts(목표 계약).",
            "forbidden_action": "validation/OOS retune(검증/OOS 재조정).",
            "effect": "수리 가중치를 실제 학습 입력으로 물질화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "materialize_model_task_matrix",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "model variant task matrix(모델 변형 작업 행렬) 생성.",
            "required_inputs": f"{rel(MODEL_VARIANT_CONTRACTS)};{rel(GUARDRAIL_CONTRACTS)}",
            "required_outputs": "ec_training_task_matrix.csv",
            "blocked_if_missing": "ONNX-capable model path(ONNX 가능 모델 경로).",
            "forbidden_action": "result-driven parameter search(결과 기반 파라미터 탐색).",
            "effect": "다음 학습 범위를 사전 선언된 변형으로 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "carry_controls_density_wfo",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "control/density/WFO guard matrix(대조/밀도/WFO 가드 행렬) 이월.",
            "required_inputs": f"{rel(CONTROL_DENSITY_REVIEW)};{rel(DZ_DENSITY_AUDIT)}",
            "required_outputs": "control_density_wfo_guard_matrix.csv",
            "blocked_if_missing": "EA control review(EA 대조 검토).",
            "forbidden_action": "control gate relaxation(대조 게이트 완화).",
            "effect": "수리 후보가 같은 실패를 반복하는지 즉시 보이게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "preserve_no_release_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "no-release firewall(해제 금지 방화벽) 보존.",
            "required_inputs": f"{rel(OOS_QUARANTINE)};{rel(ARTIFACT_PRESERVATION)}",
            "required_outputs": "no_release_firewall_carry.csv",
            "blocked_if_missing": "quarantine contract(격리 계약).",
            "forbidden_action": "selection, MT5, forward, live readiness(선택/MT5/전진/라이브 준비).",
            "effect": "좋은 일부 지표가 운영 주장으로 번지는 것을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    no_forbidden_claim = all(
        final.get(key) in {"not_run", "not_run_design_only", "not_claimed"}
        for key in (
            "model_training",
            "threshold_tuning",
            "lot_optimization",
            "candidate_selection",
            "mt5_runtime_probe",
            "forward_passed",
            "forward_failed",
            "runtime_authority",
            "goal_achieve",
        )
    )
    release_blockers = final.get("release_blockers", [])
    if not isinstance(release_blockers, list):
        release_blockers = [str(release_blockers)]
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "모든 EA/DZ 입력이 있어야 설계 근거가 닫힌다."),
        ("parent_ea_gates_passed", final["ea_failed_gate_rows"] == 0, str(final["ea_failed_gate_rows"]), "0", "부모 검토가 깨끗해야 실패 기억을 신뢰한다."),
        ("parent_next_action_matches", final["ea_next_action"] == RUN_ID, str(final["ea_next_action"]), RUN_ID, "라우팅이 EB로 정확히 이어졌는지 확인한다."),
        ("parent_release_blocked", final["parent_release_candidate_rows"] == 0 and len(release_blockers) > 0, f"release={final['parent_release_candidate_rows']};blockers={len(release_blockers)}", "release=0;blockers>0", "해제 실패를 수리 설계 입력으로 묶는다."),
        ("design_rows_min", final["design_rows"] >= 5, str(final["design_rows"]), ">=5", "수리 주제가 단일 처방으로 좁아지지 않게 한다."),
        ("objective_contract_rows_min", final["objective_contract_rows"] >= 4, str(final["objective_contract_rows"]), ">=4", "학습 목표 계약이 충분히 분해됐는지 본다."),
        ("model_variant_rows_min", final["model_variant_rows"] >= 4, str(final["model_variant_rows"]), ">=4", "모델 변형이 사전 선언됐는지 본다."),
        ("guardrail_rows_min", final["guardrail_rows"] >= 6, str(final["guardrail_rows"]), ">=6", "과적합 방지 게이트를 유지한다."),
        ("queue_rows_min", final["queue_rows"] >= 4, str(final["queue_rows"]), ">=4", "다음 EC 작업이 실행 가능한 큐로 남았는지 본다."),
        ("oos_quarantine_present", final["quarantine_rows"] >= 2, str(final["quarantine_rows"]), ">=2", "얇은 OOS 포켓을 선택기에서 분리한다."),
        ("artifact_preservation_present", final["preservation_rows"] >= 5, str(final["preservation_rows"]), ">=5", "부모 산출물 계보를 보존한다."),
        ("no_forbidden_claim", no_forbidden_claim, str(no_forbidden_claim).lower(), "true", "EB는 설계 전용이며 운영/목표 주장을 하지 않는다."),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    experiment = {
        "run_id": RUN_ID,
        "hypothesis": "validation PF/trade count/density blockers(검증 PF/거래수/밀도 차단)을 threshold tuning(임계값 조정) 없이 학습 전용 설계로 고친다.",
        "comparison_baseline": rel(EA_FINAL),
        "changed_variables": "train-only objectives/model capacity/predeclared weights(학습 전용 목표/모델 용량/사전 선언 가중치).",
        "fixed_variables": "feature order/split/threshold/lot/ATR/MT5 handoff(피처 순서/분할/임계값/랏/ATR/MT5 인계).",
        "success_criteria": "future ED must jointly pass validation PF/trades/density/control(향후 ED가 검증 PF/거래수/밀도/대조를 공동 통과).",
        "stop_conditions": "any validation/OOS retune or threshold search(검증/OOS 재조정 또는 임계값 탐색).",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data = {
        "input_files": [rel(path) for path in INPUT_FILES],
        "missing_inputs": final["missing_inputs"],
        "hashes": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "split_boundary": "read parent review outputs only; no new training data used(부모 검토 산출물만 읽고 새 학습 데이터는 쓰지 않음).",
        "integrity_judgment": "usable_for_design_only(설계 전용으로 사용 가능).",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_training": "not_run_design_only(미실행, 설계 전용)",
        "selection_metric": "none(없음)",
        "threshold_policy": "fixed_no_tuning(고정, 조정 없음)",
        "variant_contract_rows": final["model_variant_rows"],
        "overfit_risk": "repairing too directly to parent failure(부모 실패에 너무 직접 맞출 위험).",
        "mitigation": "predeclared contracts and no OOS selector(사전 선언 계약과 OOS 선택기 금지).",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "observed_parent_blockers": final["release_blockers"],
        "best_validation_pf": final["best_validation_pf"],
        "best_validation_trade_count": final["best_validation_trade_count"],
        "best_oos_pf": final["best_oos_pf"],
        "best_oos_trade_count": final["best_oos_trade_count"],
        "attribution": "validation edge thin, trade count near floor, density transfer unstable, OOS pocket thin(검증 우위 얇음, 거래수 하한 근접, 밀도 전이 불안정, OOS 포켓 얇음).",
        "confidence": "medium for design, low for runtime(설계에는 중간, 런타임에는 낮음).",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": JUDGMENT,
        "evidence_available": "EA failure memory and EB contracts(EA 실패 기억과 EB 계약).",
        "evidence_missing": "EC materialization, ED training, MT5, forward(EC 물질화, ED 학습, MT5, 전진).",
        "next_condition": NEXT_RUN_ID,
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(EXPERIMENT_RECEIPT, experiment),
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_with_boundary(경계 안에서 연결됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EB Repair Design(337EB 수리 설계)

## Conclusion(결론)

run337EB(337EB 실행)는 EA review(EA 검토)에서 막힌 validation PF/trade count/density(검증 PF/거래수/밀도)를 다음 EC materialization(EC 물질화) 계약으로 바꿨다.

Action(행동): threshold tuning(임계값 조정), lot optimization(랏 최적화), candidate selection(후보 선택), MT5 probe(MT5 탐침)는 실행하지 않았다.

Effect(효과): 실패를 고쳐 보이게 만드는 것이 아니라, 과적합을 막는 사전 선언 수리 설계로 고정했다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- design_rows(설계 행): `{final["design_rows"]}`
- objective_contract_rows(목표 계약 행): `{final["objective_contract_rows"]}`
- model_variant_rows(모델 변형 행): `{final["model_variant_rows"]}`
- guardrail_rows(가드레일 행): `{final["guardrail_rows"]}`
- best_validation_pf(이전 최고 검증 PF): `{final["best_validation_pf"]}`
- best_validation_trade_count(이전 최고 검증 거래수): `{final["best_validation_trade_count"]}`
- best_oos_pf(이전 최고 OOS PF): `{final["best_oos_pf"]}`
- best_oos_trade_count(이전 최고 OOS 거래수): `{final["best_oos_trade_count"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EB

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): EA의 validation/density/trade blockers(검증/밀도/거래 차단)를 EC의 train-only repair inputs(학습 전용 수리 입력)로 넘긴다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(REPAIR_DESIGN)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337EB focus complete: validation-density/trade-count repair design(검증-밀도/거래수 수리 설계)을 `{STATUS}`로 닫았다. "
        "Effect(효과): 다음 run337EC에서 train-only objective/model/guardrail inputs(학습 전용 목표/모델/가드레일 입력)를 물질화한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EB focus complete")
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
## Stage337 run337EB(337EB 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): validation PF/trade count/density(검증 PF/거래수/밀도) 실패를 train-only repair design(학습 전용 수리 설계)로 고정했다. 선택/MT5/Forward/Goal(선택/MT5/전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337EA("
    if "## Stage337 run337EB(337EB 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_eb_design_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): validation-density/trade-count repair input materialization(검증-밀도/거래수 수리 입력 물질화)로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EB(337EB 실행) designed validation-density/trade-count repair(검증-밀도/거래수 수리 설계). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EB(337EB 실행) designed validation-density"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337EB designed validation-density/trade-count repair(검증-밀도/거래수 수리 설계) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EB designed validation-density"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "validation_density_trade_count_repair_design_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"design_rows={final['design_rows']};guardrails={final['guardrail_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design_data_integrity_model_validation_performance_attribution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "design_no_training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "design_contract_no_kpi",
        "scoreboard_lane": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_validation_pf={final['best_validation_pf']};best_validation_trades={final['best_validation_trade_count']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;no_oos_selector",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_data_integrity_model_validation_performance_attribution",
        "evidence_scope": "EA blockers converted to EC materialization design",
        "kpi_scope": "validation_density_trade_count_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_design",
        "family": "experiment_design_data_integrity_model_validation_performance_attribution",
        "question": "how to repair validation PF trade count and density without overfit tuning",
        "metric_scope": "design_rows_objective_model_guardrails",
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
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    context = load_context()
    design_rows = build_design_rows(context)
    objective_rows = build_objective_contracts()
    model_rows = build_model_variants()
    guardrail_rows = build_guardrails()
    quarantine_rows = build_quarantine(context["final"])
    preservation_rows = build_preservation_rows()
    queue_rows = build_ec_queue()
    artifacts: list[Path] = [
        write_csv(REPAIR_DESIGN, DESIGN_COLUMNS, design_rows),
        write_csv(OBJECTIVE_CONTRACTS, OBJECTIVE_COLUMNS, objective_rows),
        write_csv(MODEL_VARIANT_CONTRACTS, MODEL_VARIANT_COLUMNS, model_rows),
        write_csv(GUARDRAIL_CONTRACTS, GUARDRAIL_COLUMNS, guardrail_rows),
        write_csv(OOS_QUARANTINE, QUARANTINE_COLUMNS, quarantine_rows),
        write_csv(ARTIFACT_PRESERVATION, PRESERVE_COLUMNS, preservation_rows),
        write_csv(EC_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]

    ea_final = context["final"]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "ea_next_action": ea_final.get("next_action", ""),
        "ea_failed_gate_rows": sum(1 for row in read_csv(EA_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "candidate_rows": int(len(context["candidates"])),
        "best_validation_model_id": ea_final.get("best_validation_model_id", ""),
        "best_validation_pf": ea_final.get("best_validation_pf", 0),
        "best_validation_trade_count": ea_final.get("best_validation_trade_count", 0),
        "best_oos_pf": ea_final.get("best_oos_pf", 0),
        "best_oos_trade_count": ea_final.get("best_oos_trade_count", 0),
        "density_validation_pressure_rows": ea_final.get("density_validation_pressure_rows", 0),
        "parent_release_candidate_rows": ea_final.get("release_candidate_rows", 0),
        "release_blockers": ea_final.get("release_blockers", []),
        "validation_pf_pass_rows": context["validation_pf_pass_rows"],
        "validation_trade_pass_rows": context["validation_trade_pass_rows"],
        "validation_both_pass_rows": context["validation_both_pass_rows"],
        "density_pressure_models": context["density_pressure_models"],
        "design_rows": len(design_rows),
        "objective_contract_rows": len(objective_rows),
        "model_variant_rows": len(model_rows),
        "guardrail_rows": len(guardrail_rows),
        "quarantine_rows": len(quarantine_rows),
        "preservation_rows": len(preservation_rows),
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
    artifacts.extend([write_report(final), write_decision_doc(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))

    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": "gate_failed", "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "design_rows": final["design_rows"],
                "objective_contract_rows": final["objective_contract_rows"],
                "model_variant_rows": final["model_variant_rows"],
                "guardrail_rows": final["guardrail_rows"],
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
