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
RUN_NUMBER = "run337CU"
RUN_ID = "run337CU_design_feature_label_separability_control_repair_without_db_v1"
PARENT_RUN_ID = "run337CT_review_weak_density_control_repaired_candidates_without_db_v1"
NEXT_RUN_ID = "run337CV_materialize_feature_label_separability_control_repair_inputs_without_db_v1"
STATUS = "completed_stage337CU_feature_label_separability_control_repair_design_no_training_no_selection"
JUDGMENT = "feature_label_separability_and_control_orthogonalization_repair_design_ready"
DECISION = "stage337CU_open_run337CV_materialize_feature_label_separability_control_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CU_feature_label_separability_control_repair_design_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CU_separability_control_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CU_feature_label_separability_control_repair_design.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CT_DIR = STAGE_DIR / "02_runs" / "run337CT"
CT_FINAL = CT_DIR / "final_decision.json"
CT_GATES = CT_DIR / "required_gate_coverage_audit.csv"
CT_FAILURE = CT_DIR / "failure_attribution_matrix.csv"
CT_POLICY = CT_DIR / "policy_diagnostic_summary.csv"
CT_LOCK = CT_DIR / "release_lock_review.csv"
CT_QUEUE = CT_DIR / "run337CU_repair_design_queue.csv"
CS_SCORECARD = STAGE_DIR / "02_runs" / "run337CS" / "repaired_model_scorecard.csv"
CS_CONTROLS = STAGE_DIR / "02_runs" / "run337CS" / "extended_control_scorecard.csv"

SEPARABILITY_DESIGN = RUN_DIR / "feature_label_separability_repair_design.csv"
CONTROL_ORTHOGONAL_PLAN = RUN_DIR / "control_orthogonalization_plan.csv"
MODEL_FAMILY_LOSS_PLAN = RUN_DIR / "model_family_loss_probe_plan.csv"
FIREWALLS = RUN_DIR / "density_only_and_oos_selection_firewall.csv"
CV_QUEUE = RUN_DIR / "run337CV_materialization_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (CT_FINAL, CT_GATES, CT_FAILURE, CT_POLICY, CT_LOCK, CT_QUEUE, CS_SCORECARD, CS_CONTROLS)
OUTPUT_FILES = (
    SEPARABILITY_DESIGN,
    CONTROL_ORTHOGONAL_PLAN,
    MODEL_FAMILY_LOSS_PLAN,
    FIREWALLS,
    CV_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
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

SEPARABILITY_COLUMNS = ("design_id", "repair_axis", "hypothesis", "materialized_input", "train_only_rule", "validation_oos_role", "blocks_if", "effect", "claim_boundary")
CONTROL_COLUMNS = ("control_plan_id", "blocked_control", "repair_action", "required_input", "pass_condition", "forbidden_action", "effect", "claim_boundary")
MODEL_PLAN_COLUMNS = ("probe_id", "model_family_or_loss", "scope", "why_now", "allowed_size", "forbidden_action", "effect", "claim_boundary")
FIREWALL_COLUMNS = ("firewall_id", "forbidden_pattern", "reason", "blocks_if_seen", "effect", "claim_boundary")
QUEUE_COLUMNS = ("queue_id", "next_run_id", "priority", "task", "required_inputs", "required_outputs", "blocked_if_missing", "forbidden_action", "effect", "claim_boundary")
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def build_separability_design() -> list[dict[str, str]]:
    return [
        {
            "design_id": "label_margin_widen_train_only_q60_q70",
            "repair_axis": "label_boundary(라벨 경계)",
            "hypothesis": "current q50 deadzone is too noisy for direction separation(현재 q50 사각지대가 방향 분리에 너무 시끄러움)",
            "materialized_input": "train-only q60/q70 vol-normalized margin labels(학습 전용 q60/q70 변동성 정규화 마진 라벨)",
            "train_only_rule": "derive margins from train split only(마진은 학습 분할에서만 산출)",
            "validation_oos_role": "read-only separability and controls(읽기 전용 분리력/대조)",
            "blocks_if": "validation balanced <= CT max or density collapses below declared floor(검증 균형 정확도가 CT 최대 이하 또는 밀도 붕괴)",
            "effect": "밀도보다 라벨 품질을 먼저 고친다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "two_stage_nonflat_then_direction",
            "repair_axis": "target_decomposition(목표 분해)",
            "hypothesis": "flat-vs-trade and direction are mixed too early(무거래/거래와 방향이 너무 일찍 섞임)",
            "materialized_input": "stage1 non-flat gate plus stage2 direction label(1단계 비플랫 게이트와 2단계 방향 라벨)",
            "train_only_rule": "stage1 density floor fixed from train only(1단계 밀도 하한은 학습 전용 고정)",
            "validation_oos_role": "read-only joint gate(읽기 전용 결합 게이트)",
            "blocks_if": "stage1 passes but stage2 direction remains below 0.40 balanced(1단계 통과 후 2단계 방향 0.40 미만)",
            "effect": "거래 여부와 방향 실패를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "feature_state_carry_pruned_set",
            "repair_axis": "feature_state(피처 상태)",
            "hypothesis": "high state-carry features may support shifted controls(높은 상태 이월 피처가 이동 대조를 돕는다)",
            "materialized_input": "feature subsets excluding high autocorrelation groups(높은 자기상관 그룹 제외 피처 부분집합)",
            "train_only_rule": "feature exclusion rule fixed before validation/OOS scoring(검증/OOS 채점 전 제외 규칙 고정)",
            "validation_oos_role": "read-only control clearance(읽기 전용 대조 통과)",
            "blocks_if": "gap72/gap96/horizon controls remain aligned(72/96갭/기간 대조가 계속 정렬)",
            "effect": "대조가 먹는 낡은 상태를 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "calendar_session_concentration_guard",
            "repair_axis": "calendar_concentration(달력 집중)",
            "hypothesis": "day/session pockets may dominate weak signal(일/세션 포켓이 약한 신호를 지배할 수 있음)",
            "materialized_input": "day/session concentration gates from CR/CS diagnostics(CR/CS 진단 기반 일/세션 집중 게이트)",
            "train_only_rule": "predeclare max day/session share before scoring(채점 전 최대 일/세션 비중 선언)",
            "validation_oos_role": "read-only concentration check(읽기 전용 집중 확인)",
            "blocks_if": "one day/session pocket carries trades or proxy return(단일 일/세션 포켓이 거래/프록시 수익 지배)",
            "effect": "곡선 포켓을 분리력으로 착각하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_control_plan() -> list[dict[str, str]]:
    return [
        {
            "control_plan_id": "gap72_gap96_predeclared_degradation",
            "blocked_control": "label_shift_gap72_control;label_shift_gap96_control",
            "repair_action": "score every candidate against both controls before any runtime queue(런타임 대기열 전 모든 후보를 두 대조에 채점)",
            "required_input": rel(CS_CONTROLS),
            "pass_condition": "control trade balanced < actual and <0.45 on validation/OOS(대조 거래 균형 정확도 실제보다 낮고 0.45 미만)",
            "forbidden_action": "do not drop controls after failure(실패 후 대조 삭제 금지)",
            "effect": "이동 의존을 수익 신호로 보내지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_plan_id": "horizon_modulo_fold_guard",
            "blocked_control": "horizon_modulo_fold_control",
            "repair_action": "add modulo-fold control as hard release gate(모듈로 폴드 대조를 강한 해제 게이트로 추가)",
            "required_input": rel(CS_CONTROLS),
            "pass_condition": "modulo control degraded on validation and OOS(모듈로 대조가 검증/OOS에서 약화)",
            "forbidden_action": "do not claim release if modulo control blocks(모듈로 대조 차단 시 해제 주장 금지)",
            "effect": "기간 구조 누수를 더 빨리 잡는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_plan_id": "density_quality_joint_gate",
            "blocked_control": "signal_floor_lock plus model_discrimination",
            "repair_action": "require balanced accuracy and density together(균형 정확도와 밀도를 함께 요구)",
            "required_input": rel(CT_POLICY),
            "pass_condition": "validation balanced >0.40 and density floor met before OOS read(검증 균형 정확도 0.40 초과와 밀도 하한 충족)",
            "forbidden_action": "do not use density-only pass(밀도 단독 통과 금지)",
            "effect": "거래수만 늘린 모델을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_model_plan() -> list[dict[str, str]]:
    return [
        {
            "probe_id": "balanced_extratrees_leaf_grid_tiny",
            "model_family_or_loss": "extra_trees_leaf_grid(엑스트라트리 잎 격자)",
            "scope": "tiny predeclared grid only(작은 사전 선언 격자만)",
            "why_now": "current extratrees leaf160 underfits separation(현재 leaf160이 분리력을 과소적합)",
            "allowed_size": "3 leaf settings x designed labels(잎 설정 3개와 설계 라벨)",
            "forbidden_action": "no broad search and no OOS ranking(광범위 탐색/OOS 순위 금지)",
            "effect": "용량 부족인지 라벨 문제인지 나눈다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "probe_id": "cost_sensitive_direction_loss_scout",
            "model_family_or_loss": "class_weight_direction_loss(방향 손실 가중)",
            "scope": "train-only class weights(학습 전용 클래스 가중)",
            "why_now": "flat majority may suppress direction signal(플랫 다수가 방향 신호를 누를 수 있음)",
            "allowed_size": "2 weight profiles only(가중 프로필 2개만)",
            "forbidden_action": "no validation/OOS weight tuning(검증/OOS 가중 조정 금지)",
            "effect": "방향 분리 실패를 손실함수에서 탐침한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "probe_id": "two_stage_calibrated_rank_only",
            "model_family_or_loss": "two_stage_rank_model(2단계 순위 모델)",
            "scope": "diagnostic only, probabilities are ranks(진단 전용, 확률은 순위)",
            "why_now": "single multiclass surface stayed weak(단일 다중분류 표면이 약함)",
            "allowed_size": "stage1/stage2 scout only(1/2단계 스카우트만)",
            "forbidden_action": "no calibrated probability claim(보정 확률 주장 금지)",
            "effect": "거래 가능성과 방향성을 분리해서 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_firewalls() -> list[dict[str, str]]:
    return [
        {
            "firewall_id": "no_density_only_repair",
            "forbidden_pattern": "increase signal density without improving validation balanced accuracy(검증 균형 정확도 개선 없는 신호 밀도 증가)",
            "reason": "CT showed density rose but release stayed blocked(CT에서 밀도는 올랐지만 해제는 계속 차단)",
            "blocks_if_seen": "density gate used without quality/control gate(품질/대조 게이트 없는 밀도 게이트)",
            "effect": "밀도 임계값만 만지는 과적합을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_oos_rank_selection",
            "forbidden_pattern": "choose best policy/model by OOS diagnostic rank(OOS 진단 순위로 최고 정책/모델 선택)",
            "reason": "CT diagnostic ranks are not selection(CT 진단 순위는 선택이 아님)",
            "blocks_if_seen": "OOS rank appears in selection field(OOS 순위가 선택 필드에 등장)",
            "effect": "또 다른 과적합 선택을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_mt5_before_control_clearance",
            "forbidden_pattern": "run MT5 from model with any extended control block(확장 대조 차단 모델의 MT5 실행)",
            "reason": "96/96 extended controls blocked release(확장 대조 96/96이 해제 차단)",
            "blocks_if_seen": "runtime queue ignores control blocks(런타임 대기열이 대조 차단 무시)",
            "effect": "대조 실패를 MT5로 우회하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_cv_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337CV_materialize_label_margin_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize train-only q60/q70 label margins(학습 전용 q60/q70 라벨 마진 물질화)",
            "required_inputs": rel(SEPARABILITY_DESIGN),
            "required_outputs": "label_margin_candidate_frame.parquet;label_margin_contract.csv",
            "blocked_if_missing": "separability design missing(분리력 설계 누락)",
            "forbidden_action": "do not derive thresholds from validation/OOS(검증/OOS에서 임계값 산출 금지)",
            "effect": "라벨 잡음을 줄이는 입력을 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CV_materialize_two_stage_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize non-flat then direction labels(비플랫 후 방향 라벨 물질화)",
            "required_inputs": rel(SEPARABILITY_DESIGN),
            "required_outputs": "two_stage_label_contract.csv;two_stage_training_task_matrix.csv",
            "blocked_if_missing": "two-stage design missing(2단계 설계 누락)",
            "forbidden_action": "do not select stage from OOS(단계를 OOS로 선택 금지)",
            "effect": "거래 가능성과 방향을 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CV_materialize_control_orthogonal_features",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize feature dropout/control matrix(피처 드롭아웃/대조 행렬 물질화)",
            "required_inputs": rel(CONTROL_ORTHOGONAL_PLAN),
            "required_outputs": "control_orthogonal_feature_sets.csv;extended_control_contract.csv",
            "blocked_if_missing": "control plan missing(대조 계획 누락)",
            "forbidden_action": "do not drop controls after they block(차단 뒤 대조 삭제 금지)",
            "effect": "대조 직교화를 학습 전 입력으로 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CV_materialize_tiny_model_probe_matrix",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "materialize tiny model/loss probe matrix(작은 모델/손실 탐침 행렬 물질화)",
            "required_inputs": rel(MODEL_FAMILY_LOSS_PLAN),
            "required_outputs": "tiny_model_probe_task_matrix.csv",
            "blocked_if_missing": "model plan missing(모델 계획 누락)",
            "forbidden_action": "do not broaden search from OOS rank(OOS 순위로 탐색 확대 금지)",
            "effect": "모델 용량과 라벨 실패를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]
    ct_final = read_json(CT_FINAL)

    def row(gate_id: str, ok: bool, observed: Any, expected: str, effect: str) -> dict[str, str]:
        return {"gate_id": gate_id, "status": "passed" if ok else "failed", "observed": str(observed), "expected": expected, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}

    return [
        row("cu_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CT evidence(근거)를 연결했다."),
        row("cu_gate_parent_points_to_cu", ct_final.get("next_action", "") == RUN_ID, ct_final.get("next_action", ""), RUN_ID, "CT next_action(다음 행동)과 CU run(실행)이 맞는다."),
        row("cu_gate_separability_design", final["separability_design_rows"] >= 4, final["separability_design_rows"], ">=4", "피처/라벨 분리력 설계를 만들었다."),
        row("cu_gate_control_plan", final["control_plan_rows"] >= 3, final["control_plan_rows"], ">=3", "대조 직교화 계획을 만들었다."),
        row("cu_gate_firewalls", final["firewall_rows"] >= 3, final["firewall_rows"], ">=3", "금지 패턴을 명시했다."),
        row("cu_gate_cv_queue", final["cv_queue_rows"] >= 4, final["cv_queue_rows"], ">=4", "CV 물질화 대기열을 열었다."),
        row("cu_gate_no_training_selection_mt5", True, "training=not_run;selection=not_run;mt5=not_run", "no training/selection/MT5", "CU는 설계만 수행한다."),
    ]


def write_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "design only, inherits CT/CS time axis(설계 전용, CT/CS 시간축 상속)",
        "sample_scope": "no new rows or labels materialized yet(아직 새 행/라벨 물질화 없음)",
        "feature_label_boundary": "future CV must use train-only thresholds(CV는 학습 전용 임계값만 사용)",
        "split_boundary": "validation/OOS read-only role declared(검증/OOS 읽기 전용 역할 선언)",
        "leakage_risk": "turning design alternatives into selected winner(설계 대안을 선택 승자로 바꾸는 위험)",
        "integrity_judgment": "usable_design_only",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "design only for tiny probes(작은 탐침 설계 전용)",
        "target_and_label": "feature/label separability repair targets(피처/라벨 분리력 수리 목표)",
        "split_method": "predeclared train-only rules with read-only validation/OOS(사전 선언 학습 전용 규칙과 읽기 전용 검증/OOS)",
        "selection_metric": "none_no_selection(없음, 선택 아님)",
        "threshold_policy": "threshold changes forbidden except train-only materialized contracts(학습 전용 계약 물질화 외 임계값 변경 금지)",
        "overfit_risk": "density-only repair and OOS rank selection(밀도 단독 수리와 OOS 순위 선택)",
        "validation_judgment": "design_ready_for_input_materialization(입력 물질화 설계 준비)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "CT failure attribution and CU design artifacts(CT 실패 귀속과 CU 설계 산출물)",
        "evidence_missing": "CV materialized inputs and future training(CV 물질화 입력과 향후 학습)",
        "judgment_label": "exploratory_design_ready(탐색 설계 준비)",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "밀도 수리를 접고 분리력/대조 직교화 수리로 넘어간다.",
    }
    receipt_paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifact_paths] + [rel(path) for path in receipt_paths],
        "artifact_hashes": {rel(path): sha256_file(path) for path in list(artifact_paths) + receipt_paths if path_exists(path) and io_path(path).is_file()},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers(02_runs는 목록/해시로 추적, 보고서와 장부는 저장소 추적)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipt_paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return receipt_paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CU Feature/Label Separability Control Repair Design(피처/라벨 분리력 대조 수리 설계)

## Conclusion(결론)

run337CU(337CU 실행)는 CT review(CT 검토)의 release blocked(해제 차단)를 density-only repair(밀도 단독 수리) 금지와 feature/label separability repair(피처/라벨 분리력 수리) 설계로 바꿨다.

Effect(효과): 다음 run337CV(337CV 실행)는 학습이 아니라 q60/q70 label margin(라벨 마진), two-stage labels(2단계 라벨), control-orthogonal features(대조 직교 피처), tiny model probe matrix(작은 모델 탐침 행렬)를 물질화한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- separability_design_rows(분리력 설계 행): `{final["separability_design_rows"]}`
- control_plan_rows(대조 계획 행): `{final["control_plan_rows"]}`
- model_plan_rows(모델 계획 행): `{final["model_plan_rows"]}`
- firewall_rows(방화벽 행): `{final["firewall_rows"]}`
- cv_queue_rows(CV 대기열 행): `{final["cv_queue_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CU

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): density-only repair(밀도 단독 수리)를 막고 CV input materialization(CV 입력 물질화)을 연다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(SEPARABILITY_DESIGN)}`, `{rel(CONTROL_ORTHOGONAL_PLAN)}`, `{rel(CV_QUEUE)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
- MT5 probe(MT5 탐침): `not_run`
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
        "current_focus:\n- >-\n"
        f"  Stage337 run337CU focus complete: feature/label separability control repair design(피처/라벨 분리력 대조 수리 설계)을 `{STATUS}`로 닫았다. "
        "Effect(효과): run337CV(337CV 실행)에서 수리 입력을 물질화한다."
    )
    workspace_text = workspace_text.replace("current_focus:", focus_entry, 1) if "Stage337 run337CU focus complete" not in workspace_text else re.sub(
        r"current_focus:\n- >-\n  Stage337 run337CU focus complete:.*?(?=\n- >-\n  Stage337 run337CT|\n[A-Za-z0-9_]+:)",
        focus_entry,
        workspace_text,
        count=1,
        flags=re.DOTALL,
    )
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
## Stage337 run337CU(337CU 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): density-only repair(밀도 단독 수리)를 금지하고 feature/label/control repair(피처/라벨/대조 수리) 입력 물질화를 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current_text = re.sub(r"\n## Stage337 run337CU\(337CU 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CT|\Z)", "\n", current_text, count=1, flags=re.DOTALL)
    marker = "## Stage337 run337CT(337CT"
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
- actual_mt5_execution(실제 MT5 실행): `held_by_cu_design_no_mt5`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 feature/label separability control repair input materialization(피처/라벨 분리력 대조 수리 입력 물질화)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CU(337CU 실행)" not in line)
    stage_entry = f"- {TODAY}: run337CU(337CU 실행) designed feature/label separability control repair(피처/라벨 분리력 대조 수리). Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337CU designed feature/label separability control repair" not in line)
    changelog_entry = f"- {TODAY}: Stage337 run337CU designed feature/label separability control repair(피처/라벨 분리력 대조 수리) and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "feature_label_separability_control_repair_design_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"separability_design={final['separability_design_rows']};cv_queue={final['cv_queue_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design_model_validation_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__separability_control_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "separability_control_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_design",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "design_no_training_no_selection",
        "scoreboard_lane": "experiment_design_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"design_rows={final['separability_design_rows']};firewalls={final['firewall_rows']}",
        "guardrail_kpi": "no_density_only;no_oos_selection;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__separability_control_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_model_validation_result_judgment",
        "evidence_scope": "CT failure attribution converted to repair design",
        "kpi_scope": "design_no_training_no_selection",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__separability_control_design",
        "family": "experiment_design_model_validation_result_judgment",
        "question": "what should repair after weak density/control release block target",
        "metric_scope": "separability_design_control_plan_firewalls_queue",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    artifacts = [upsert_csv(RUN_REGISTRY, "run_id", run_row), upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row), upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row)]

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
        new_rows.append({"artifact_id": f"{RUN_ID}::{artifact_path}", "artifact_type": path.suffix.lstrip(".") or "file", "path": artifact_path, "sha256": sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": generated, "notes": STATUS, "artifact_path": artifact_path, "claim_boundary": CLAIM_BOUNDARY})
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    separability_rows = build_separability_design()
    control_rows = build_control_plan()
    model_rows = build_model_plan()
    firewall_rows = build_firewalls()
    queue_rows = build_cv_queue()
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "separability_design_rows": len(separability_rows),
        "control_plan_rows": len(control_rows),
        "model_plan_rows": len(model_rows),
        "firewall_rows": len(firewall_rows),
        "cv_queue_rows": len(queue_rows),
        "model_training": "not_run",
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
    artifacts: list[Path] = [
        write_csv(SEPARABILITY_DESIGN, SEPARABILITY_COLUMNS, separability_rows),
        write_csv(CONTROL_ORTHOGONAL_PLAN, CONTROL_COLUMNS, control_rows),
        write_csv(MODEL_FAMILY_LOSS_PLAN, MODEL_PLAN_COLUMNS, model_rows),
        write_csv(FIREWALLS, FIREWALL_COLUMNS, firewall_rows),
        write_csv(CV_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(write_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
