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

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import review_guarded_prediction_surface_validation_edge_training as dp  # noqa: E402
from stage_pipelines.stage337 import train_guarded_prediction_surface_validation_edge_repair_candidates as do  # noqa: E402
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
STAGE_ID = dp.STAGE_ID
RUN_NUMBER = "run337DQ"
RUN_ID = "run337DQ_design_validation_support_and_control_residual_repair_without_db_v1"
PARENT_RUN_ID = dp.RUN_ID
NEXT_RUN_ID = "run337DR_materialize_validation_support_control_residual_repair_inputs_without_db_v1"
STATUS = "completed_stage337DQ_validation_support_control_residual_repair_design_no_training_no_selection"
JUDGMENT = "repair_design_ready_for_row_level_tape_materialization_no_selection"
DECISION = "stage337DQ_open_run337DR_materialize_validation_support_control_residual_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DQ_validation_support_control_residual_repair_design_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dp.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dp.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DQ_validation_support_control_residual_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DQ_validation_support_control_residual_repair_design.md"
SELECTED_STATUS = dp.SELECTED_STATUS
STAGE_BRIEF = dp.STAGE_BRIEF
WORKSPACE_STATE = dp.WORKSPACE_STATE
CURRENT_STATE = dp.CURRENT_STATE
CHANGELOG = dp.CHANGELOG
RUN_REGISTRY = dp.RUN_REGISTRY
ALPHA_LEDGER = dp.ALPHA_LEDGER
ARTIFACT_REGISTRY = dp.ARTIFACT_REGISTRY
STAGE_LEDGER = dp.STAGE_LEDGER

DP_FINAL = dp.FINAL_DECISION
DP_GATES = dp.REQUIRED_GATE_AUDIT
DP_QUEUE = dp.DQ_QUEUE
DP_CANDIDATE_REVIEW = dp.CANDIDATE_TRAINING_REVIEW
DP_CONTROL_SURFACE_REVIEW = dp.CONTROL_SURFACE_REVIEW
DP_GAP_REVIEW = dp.VALIDATION_OOS_GAP_REVIEW
DP_RUNTIME_REVIEW = dp.RUNTIME_DISPOSITION_REVIEW
DO_MODEL_MANIFEST = do.TRAINED_MODEL_MANIFEST
DO_ONNX_PARITY = do.ONNX_PARITY
DO_CLASS_SCORECARD = do.CANDIDATE_SCORECARD
DO_PROXY_TRADE_SCORECARD = do.PROXY_TRADE_SCORECARD
SOURCE_MODEL_INPUT = do.SOURCE_MODEL_INPUT
VALIDATION_EDGE_FRAME = do.VALIDATION_EDGE_FRAME

VALIDATION_SUPPORT_DESIGN = RUN_DIR / "validation_support_repair_design.csv"
CONTROL_RESIDUAL_DESIGN = RUN_DIR / "control_residual_repair_design.csv"
OOS_ONLY_QUARANTINE = RUN_DIR / "oos_only_lift_quarantine.csv"
RUNTIME_FIREWALL_DESIGN = RUN_DIR / "runtime_firewall_repair_design.csv"
ROW_LEVEL_TAPE_CONTRACT = RUN_DIR / "row_level_tape_materialization_contract.csv"
DR_QUEUE = RUN_DIR / "run337DR_materialization_queue.csv"
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
    DP_FINAL,
    DP_GATES,
    DP_QUEUE,
    DP_CANDIDATE_REVIEW,
    DP_CONTROL_SURFACE_REVIEW,
    DP_GAP_REVIEW,
    DP_RUNTIME_REVIEW,
    DO_MODEL_MANIFEST,
    DO_ONNX_PARITY,
    DO_CLASS_SCORECARD,
    DO_PROXY_TRADE_SCORECARD,
    SOURCE_MODEL_INPUT,
    VALIDATION_EDGE_FRAME,
)
OUTPUT_FILES = (
    VALIDATION_SUPPORT_DESIGN,
    CONTROL_RESIDUAL_DESIGN,
    OOS_ONLY_QUARANTINE,
    RUNTIME_FIREWALL_DESIGN,
    ROW_LEVEL_TAPE_CONTRACT,
    DR_QUEUE,
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

VALIDATION_DESIGN_COLUMNS = (
    "design_id",
    "observed_failure",
    "evidence_source",
    "repair_hypothesis",
    "materialization_plan",
    "success_condition",
    "failure_condition",
    "invalid_condition",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
CONTROL_DESIGN_COLUMNS = (
    "design_id",
    "control_subject",
    "observed_blocker",
    "repair_hypothesis",
    "materialization_plan",
    "success_condition",
    "failure_condition",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
QUARANTINE_COLUMNS = (
    "model_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "validation_pf",
    "oos_pf",
    "pf_gap_oos_minus_validation",
    "quarantine_reason",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "blocked_action_or_claim",
    "blocked_reason",
    "allowed_next_action",
    "required_evidence_to_release",
    "effect",
    "claim_boundary",
)
TAPE_CONTRACT_COLUMNS = (
    "contract_id",
    "scope",
    "required_inputs",
    "required_outputs",
    "row_scope",
    "model_scope",
    "split_scope",
    "success_condition",
    "failure_condition",
    "forbidden_use",
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


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def load_frames() -> dict[str, pd.DataFrame]:
    return {
        "candidate": pd.read_csv(io_path(DP_CANDIDATE_REVIEW)),
        "control": pd.read_csv(io_path(DP_CONTROL_SURFACE_REVIEW)),
        "gap": pd.read_csv(io_path(DP_GAP_REVIEW)),
        "runtime": pd.read_csv(io_path(DP_RUNTIME_REVIEW)),
        "models": pd.read_csv(io_path(DO_MODEL_MANIFEST)),
        "parity": pd.read_csv(io_path(DO_ONNX_PARITY)),
        "class_score": pd.read_csv(io_path(DO_CLASS_SCORECARD)),
        "trade_score": pd.read_csv(io_path(DO_PROXY_TRADE_SCORECARD)),
    }


def build_validation_design(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, str]]:
    candidate = frames["candidate"]
    validation_failures = int((pd.to_numeric(candidate["validation_pf"], errors="coerce") < 1.05).sum())
    oos_lift_rows = int(frames["gap"]["gap_status"].astype(str).eq("oos_only_lift_quarantined").sum())
    return [
        {
            "design_id": "validation_pf_floor_all_model_block",
            "observed_failure": f"{validation_failures}/18 models below validation PF 1.05(검증 PF 1.05 미만)",
            "evidence_source": rel(DP_CANDIDATE_REVIEW),
            "repair_hypothesis": "aggregate scorecards hide row-level validation drawdown pockets(집계 점수표가 행 단위 검증 침수 포켓을 숨김)",
            "materialization_plan": "DR creates all-model prediction tape and validation curve-pocket slices(DR이 전체 모델 예측 테이프와 검증 곡선 포켓 슬라이스 생성)",
            "success_condition": "validation weak pockets are named without selecting a winner(승자 선택 없이 검증 약한 포켓을 이름 붙임)",
            "failure_condition": "no stable validation support surface appears(안정적 검증 지지 표면이 없음)",
            "invalid_condition": "DR tunes thresholds or filters on validation/OOS(DR이 검증/OOS로 임계값이나 필터 조정)",
            "forbidden_action": "no candidate selection, no threshold tuning(후보 선택/임계값 튜닝 금지)",
            "effect": "turns floor failure into diagnostic evidence(하한 실패를 진단 근거로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "cost_ladder_transfer_support",
            "observed_failure": "extra0/extra2/extra5 cost ladders do not produce validation release(비용 사다리 전반이 검증 해제를 만들지 못함)",
            "evidence_source": rel(DP_CANDIDATE_REVIEW),
            "repair_hypothesis": "cost ladder is changing trade density more than signal quality(비용 사다리가 신호 품질보다 거래 밀도를 더 바꿈)",
            "materialization_plan": "DR builds cost-ladder transfer matrix from identical rows(DR이 동일 행 기반 비용 사다리 전이 행렬 생성)",
            "success_condition": "cost effect is separable from feature/model effect(비용 효과와 피처/모델 효과 분리)",
            "failure_condition": "all cost ladders share same validation weakness(모든 비용 사다리가 같은 검증 약점 공유)",
            "invalid_condition": "cost policy is optimized after seeing OOS(OOS 확인 뒤 비용 정책 최적화)",
            "forbidden_action": "no cost policy selection(비용 정책 선택 금지)",
            "effect": "prevents cost ladder overfit(비용 사다리 과적합 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "feature_family_transfer_mismatch",
            "observed_failure": "state_carry leads OOS while macro_extra_trees leads validation(상태 캐리는 OOS, 매크로 엑스트라트리는 검증에서 상대 우위)",
            "evidence_source": rel(DP_GAP_REVIEW),
            "repair_hypothesis": "feature family edge is split-regime dependent(피처 계열 엣지가 분할/레짐 의존)",
            "materialization_plan": "DR computes feature-family split transfer and month/hour slices(DR이 피처 계열 분할 전이와 월/시간 슬라이스 계산)",
            "success_condition": "transfer mismatch is localized to time/regime slices(전이 불일치가 시간/레짐 슬라이스로 국소화)",
            "failure_condition": "mismatch remains broad and unexplained(불일치가 넓고 설명 안 됨)",
            "invalid_condition": "feature family is selected by best OOS row(최고 OOS 행으로 피처 계열 선택)",
            "forbidden_action": "no feature family winner selection(피처 계열 승자 선택 금지)",
            "effect": "keeps attractive OOS family from becoming selection pressure(매력적 OOS 계열이 선택 압력이 되는 것을 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "oos_only_lift_quarantine_design",
            "observed_failure": f"{oos_lift_rows} models show OOS-only lift(표본외 단독 개선)",
            "evidence_source": rel(DP_GAP_REVIEW),
            "repair_hypothesis": "OOS lift can be real regime signal or sample accident(OOS 개선은 실제 레짐 신호 또는 표본 사고일 수 있음)",
            "materialization_plan": "DR tags OOS-only rows and excludes them from release queues(DR이 OOS 단독 행을 태그하고 해제 대기열에서 제외)",
            "success_condition": "quarantine ledger fully covers OOS-only lift rows(격리 장부가 OOS 단독 행 전체를 덮음)",
            "failure_condition": "OOS-only rows leak into release queue(OOS 단독 행이 해제 대기열로 유입)",
            "invalid_condition": "quarantine is used as reverse selection(격리를 역선택 도구로 사용)",
            "forbidden_action": "no OOS-only winner selection(OOS 단독 승자 선택 금지)",
            "effect": "protects against overfit pressure(과적합 압력 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_control_design(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, str]]:
    candidate_blocks = frames["candidate"].loc[pd.to_numeric(frames["candidate"]["validation_control_block_rows"], errors="coerce").fillna(0) > 0]
    return [
        {
            "design_id": "shifted_return_residual_tape",
            "control_subject": "shifted_return_control(이동 수익률 대조)",
            "observed_blocker": f"{len(candidate_blocks)} models have validation shifted-control block(검증 이동 대조 차단)",
            "repair_hypothesis": "some predictions still align with serially shifted labels(일부 예측이 이동 라벨과 정렬)",
            "materialization_plan": "DR materializes model-row shifted control tape(DR이 모델-행 이동 대조 테이프 생성)",
            "success_condition": "blocked rows are localized by model/feature/hour/month(차단 행이 모델/피처/시간/월로 국소화)",
            "failure_condition": "shifted alignment is broad across surfaces(이동 정렬이 표면 전반에 넓음)",
            "forbidden_action": "no runtime probe while shifted control blocks(이동 대조 차단 중 런타임 탐침 금지)",
            "effect": "keeps serial dependence ahead of release(연속 의존을 해제보다 앞에 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "control_floor_fixed_policy",
            "control_subject": "negative control threshold(부정대조 기준)",
            "observed_blocker": "control block rule is fixed from DP, not tuned(대조 차단 규칙은 DP 고정, 튜닝 아님)",
            "repair_hypothesis": "fixed control floor is needed to avoid repair-overfit(수리 과적합 방지를 위해 고정 대조 하한 필요)",
            "materialization_plan": "DR carries fixed block condition alignment>=max(0.45,candidate-0.02)(DR이 고정 차단 조건 유지)",
            "success_condition": "all future reviews use same control blocker(미래 검토가 같은 대조 차단 조건 사용)",
            "failure_condition": "control rule is weakened to pass a model(모델 통과를 위해 대조 규칙 완화)",
            "forbidden_action": "no control threshold retuning(대조 임계값 재튜닝 금지)",
            "effect": "prevents overfit via control relaxation(대조 완화 과적합 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "non_blocking_controls_preserved",
            "control_subject": "noise/block_shuffle controls(잡음/블록 셔플 대조)",
            "observed_blocker": "noise and block-shuffle did not drive release block(잡음/블록 셔플은 해제 차단 주원인 아님)",
            "repair_hypothesis": "non-blocking controls still define the minimum audit surface(비차단 대조도 최소 감사 표면)",
            "materialization_plan": "DR keeps all controls in row-level output(DR이 모든 대조를 행 단위 출력에 보존)",
            "success_condition": "control coverage remains complete(대조 커버리지 완전 유지)",
            "failure_condition": "controls are dropped because they passed(통과했다는 이유로 대조 삭제)",
            "forbidden_action": "no control deletion(대조 삭제 금지)",
            "effect": "keeps audit breadth(감사 폭 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_quarantine(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    gap = frames["gap"]
    quarantine = gap.loc[gap["gap_status"].astype(str).eq("oos_only_lift_quarantined")].copy()
    rows: list[dict[str, Any]] = []
    for row in quarantine.to_dict("records"):
        rows.append(
            {
                "model_id": row["model_id"],
                "cost_policy_id": row.get("cost_policy_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "model_config_id": row.get("model_config_id", ""),
                "validation_pf": as_float(row.get("validation_pf")),
                "oos_pf": as_float(row.get("oos_pf")),
                "pf_gap_oos_minus_validation": as_float(row.get("pf_gap_oos_minus_validation")),
                "quarantine_reason": "oos_pf_ge_1p10_and_validation_pf_lt_1p05",
                "allowed_use": "failure memory and row-level attribution(실패 기억과 행 단위 귀인)",
                "forbidden_use": "candidate selection, threshold tuning, MT5 queue(후보 선택/임계값 튜닝/MT5 대기열)",
                "effect": "names attractive but unsafe pockets(매력적이나 안전하지 않은 포켓 명명)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_firewall() -> list[dict[str, str]]:
    return [
        {
            "firewall_id": "no_candidate_selection",
            "blocked_action_or_claim": "candidate selection(후보 선택)",
            "blocked_reason": "validation PF floor failed on all 18 models(18개 전부 검증 PF 하한 실패)",
            "allowed_next_action": NEXT_RUN_ID,
            "required_evidence_to_release": "future reviewed validation/control pass, not DQ design(미래 검토된 검증/대조 통과)",
            "effect": "keeps design from becoming selection(설계가 선택으로 변하는 것을 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_mt5_probe",
            "blocked_action_or_claim": "MT5 runtime probe(MT5 런타임 탐침)",
            "blocked_reason": "shifted control and validation support unresolved(이동 대조와 검증 지지 미해결)",
            "allowed_next_action": NEXT_RUN_ID,
            "required_evidence_to_release": "row-level tape review and repaired training review(행 단위 테이프 검토와 수리 학습 검토)",
            "effect": "keeps runtime authority closed(런타임 권위 닫힘 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_forward_claim",
            "blocked_action_or_claim": "Forward Passed/Failed(전진 통과/실패)",
            "blocked_reason": "DQ is design-only and no MT5/forward data used(DQ는 설계 전용이며 MT5/전진 데이터 없음)",
            "allowed_next_action": NEXT_RUN_ID,
            "required_evidence_to_release": "actual forward or runtime evidence(실제 전진 또는 런타임 근거)",
            "effect": "prevents premature forward judgment(조기 전진 판정 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_tape_contract() -> list[dict[str, str]]:
    common_inputs = ";".join([rel(DO_MODEL_MANIFEST), rel(SOURCE_MODEL_INPUT), rel(VALIDATION_EDGE_FRAME)])
    return [
        {
            "contract_id": "all_model_prediction_tape",
            "scope": "all 18 DO models, no selection(DO 모델 18개 전체, 선택 없음)",
            "required_inputs": common_inputs,
            "required_outputs": "all_model_prediction_tape.parquet",
            "row_scope": "source_row_id aligned validation and OOS(source_row_id 정렬 검증/OOS)",
            "model_scope": "all trained joblib and ONNX references(모든 학습 joblib/ONNX 참조)",
            "split_scope": "validation;oos",
            "success_condition": "predictions exist for every model-row-cost split(모든 모델-행-비용 분할 예측 존재)",
            "failure_condition": "any model cannot be scored or feature order is missing(모델 점수화 불가 또는 피처 순서 누락)",
            "forbidden_use": "model selection or threshold search(모델 선택 또는 임계값 탐색)",
            "effect": "creates evidence needed before repair training(수리 학습 전 필요한 근거 생성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "validation_curve_pocket_slices",
            "scope": "validation weak pockets(검증 약한 포켓)",
            "required_inputs": "all_model_prediction_tape.parquet",
            "required_outputs": "validation_curve_pocket_slices.csv",
            "row_scope": "time, hour, month, cost, feature family(시간/시/월/비용/피처 계열)",
            "model_scope": "all models(모든 모델)",
            "split_scope": "validation",
            "success_condition": "weak pockets are attributed by slice(약한 포켓이 슬라이스별 귀인)",
            "failure_condition": "weakness cannot be localized(약점 국소화 실패)",
            "forbidden_use": "filter mining for release(해제용 필터 채굴)",
            "effect": "turns weak PF into concrete failure memory(약한 PF를 구체 실패 기억으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "shifted_control_residual_tape",
            "scope": "negative control residuals(부정대조 잔차)",
            "required_inputs": "all_model_prediction_tape.parquet",
            "required_outputs": "shifted_control_residual_tape.csv",
            "row_scope": "validation and OOS rows(검증 및 OOS 행)",
            "model_scope": "all models with blocked rows highlighted(차단 행 강조 전체 모델)",
            "split_scope": "validation;oos",
            "success_condition": "shifted-control alignment is localized or cleared(이동 대조 정렬 국소화 또는 해소)",
            "failure_condition": "shifted alignment remains broad(이동 정렬이 넓게 남음)",
            "forbidden_use": "weakening control rule(대조 규칙 완화)",
            "effect": "tests serial dependence suspicion(연속 의존 의심 검정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "oos_quarantine_ledger",
            "scope": "10 OOS-only lift models(표본외 단독 개선 10개 모델)",
            "required_inputs": rel(OOS_ONLY_QUARANTINE),
            "required_outputs": "oos_only_lift_quarantine_ledger.csv",
            "row_scope": "quarantined models only for attribution(귀인 전용 격리 모델)",
            "model_scope": "quarantined rows, not shortlist(격리 행, 후보 목록 아님)",
            "split_scope": "oos with validation reference(OOS와 검증 참조)",
            "success_condition": "all OOS-only rows excluded from release queues(모든 OOS 단독 행 해제 대기열 제외)",
            "failure_condition": "quarantine row appears in release queue(격리 행이 해제 대기열 등장)",
            "forbidden_use": "reverse selection from quarantine(격리에서 역선택)",
            "effect": "keeps OOS lift as evidence not decision(OOS 개선을 결정이 아닌 근거로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_dr_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DR_materialize_all_model_prediction_tape",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize all-model prediction tape(전체 모델 예측 테이프 물질화)",
            "required_inputs": rel(ROW_LEVEL_TAPE_CONTRACT),
            "required_outputs": "all_model_prediction_tape.parquet",
            "blocked_if_missing": "row-level tape contract(행 단위 테이프 계약)",
            "forbidden_action": "no model selection or threshold search(모델 선택 또는 임계값 탐색 금지)",
            "effect": "creates row evidence before repair training(수리 학습 전 행 근거 생성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DR_materialize_validation_curve_pockets",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize validation curve pocket attribution(검증 곡선 포켓 귀인 물질화)",
            "required_inputs": rel(VALIDATION_SUPPORT_DESIGN),
            "required_outputs": "validation_curve_pocket_slices.csv",
            "blocked_if_missing": "validation support repair design(검증 지지 수리 설계)",
            "forbidden_action": "no filter mining for release(해제용 필터 채굴 금지)",
            "effect": "explains validation weakness(검증 약점 설명)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DR_materialize_control_residual_tape",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize shifted-control residual tape(이동 대조 잔차 테이프 물질화)",
            "required_inputs": rel(CONTROL_RESIDUAL_DESIGN),
            "required_outputs": "shifted_control_residual_tape.csv",
            "blocked_if_missing": "control residual repair design(대조 잔차 수리 설계)",
            "forbidden_action": "no control threshold relaxation(대조 임계값 완화 금지)",
            "effect": "tests overfit/serial residual(과적합/연속 잔차 검정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DR_materialize_oos_quarantine",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "materialize OOS-only lift quarantine ledger(OOS 단독 개선 격리 장부 물질화)",
            "required_inputs": rel(OOS_ONLY_QUARANTINE),
            "required_outputs": "oos_only_lift_quarantine_ledger.csv",
            "blocked_if_missing": "OOS quarantine rows(OOS 격리 행)",
            "forbidden_action": "no OOS-only selection(OOS 단독 선택 금지)",
            "effect": "preserves OOS lift as failure memory(OOS 개선을 실패 기억으로 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DR_preserve_runtime_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "carry runtime firewall forward(런타임 방화벽 전방 전달)",
            "required_inputs": rel(RUNTIME_FIREWALL_DESIGN),
            "required_outputs": "runtime_firewall_carry.csv",
            "blocked_if_missing": "runtime firewall repair design(런타임 방화벽 수리 설계)",
            "forbidden_action": "no MT5/Forward claim(MT5/전진 주장 금지)",
            "effect": "keeps operating boundary closed(운영 경계 닫힘 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DP/DO inputs exist(필수 DP/DO 입력 존재)"),
        ("parent_dp_gates_passed", final["dp_failed_gate_rows"] == 0, str(final["dp_failed_gate_rows"]), "0", "DP review evidence usable(DP 검토 근거 사용 가능)"),
        ("parent_next_action_matches", final["dp_next_action"] == RUN_ID, str(final["dp_next_action"]), RUN_ID, "continues DP queue(DP 대기열을 이어감)"),
        ("validation_design_materialized", final["validation_design_rows"] >= 4, str(final["validation_design_rows"]), ">=4", "validation repair design exists(검증 수리 설계 존재)"),
        ("control_design_materialized", final["control_design_rows"] >= 3, str(final["control_design_rows"]), ">=3", "control residual design exists(대조 잔차 설계 존재)"),
        ("quarantine_coverage", final["quarantine_rows"] == final["dp_oos_only_lift_rows"], f"{final['quarantine_rows']}/{final['dp_oos_only_lift_rows']}", "all", "OOS-only lift rows quarantined(OOS 단독 개선 행 격리)"),
        ("tape_contract_materialized", final["tape_contract_rows"] >= 4, str(final["tape_contract_rows"]), ">=4", "row-level contract exists(행 단위 계약 존재)"),
        ("runtime_firewall_materialized", final["runtime_firewall_rows"] >= 3, str(final["runtime_firewall_rows"]), ">=3", "runtime firewall preserved(런타임 방화벽 보존)"),
        ("dr_queue_materialized", final["dr_queue_rows"] == 5, str(final["dr_queue_rows"]), "5", "DR materialization queue opened(DR 물질화 대기열 열림)"),
        (
            "no_forbidden_claim",
            final["model_training"] == "not_run"
            and final["candidate_selection"] == "not_run"
            and final["mt5_runtime_probe"] == "not_run"
            and final["goal_achieve"] == "not_claimed",
            f"training={final['model_training']};selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            "claim boundary preserved(주장 경계 보존)",
        ),
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
    experiment_receipt = {
        "hypothesis": "validation weakness needs row-level attribution before further training(추가 학습 전 검증 약점의 행 단위 귀인이 필요)",
        "comparison_baseline": rel(DP_FINAL),
        "controls": "fixed negative-control blockers and OOS quarantine(고정 부정대조 차단과 OOS 격리)",
        "stop_conditions": "any selection, threshold tuning, MT5, or Forward claim(선택/임계값 튜닝/MT5/전진 주장 발생)",
        "success_criteria": "DR can materialize prediction/control/quarantine tapes(DR이 예측/대조/격리 테이프 물질화)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherits DO source_row_id UTC bar alignment(DO source_row_id UTC 봉 정렬 상속)",
        "sample_scope": f"quarantine_rows={final['quarantine_rows']};validation_design_rows={final['validation_design_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']}",
        "feature_label_boundary": "design-only, no feature/label recomputation(설계 전용, 피처/라벨 재계산 없음)",
        "split_boundary": "validation/OOS diagnostics only(검증/OOS 진단 전용)",
        "leakage_risk": "DR prediction tape could be misused for filter mining(DR 예측 테이프가 필터 채굴에 오용될 위험)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_design_no_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "design from DO trained ONNX candidates(DO 학습 ONNX 후보 기반 설계)",
        "target_and_label": "unchanged costed action label(비용 반영 행동 라벨 유지)",
        "split_method": "DP validation/OOS review drives design(DP 검증/OOS 검토가 설계 입력)",
        "selection_metric": "none; all models remain review-only(없음, 모든 모델 검토 전용)",
        "secondary_metrics": "validation PF floor, OOS-only lift, shifted controls(검증 PF 하한/OOS 단독 개선/이동 대조)",
        "threshold_policy": "no threshold tuning(임계값 튜닝 없음)",
        "overfit_risk": "repairing by selecting OOS-only pockets(OOS 단독 포켓 선택으로 수리하는 위험)",
        "calibration_risk": "scores remain diagnostic(점수는 진단 전용)",
        "comparison_baseline": rel(DP_CANDIDATE_REVIEW),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"validation_pf_below={final['dp_validation_pf_below_rows']};oos_only_lift={final['dp_oos_only_lift_rows']};control_blocks={final['dp_control_block_rows']}",
        "comparison_baseline": rel(DP_FINAL),
        "likely_drivers": "row-level validation pocket, cost ladder, feature transfer, shifted control(행 단위 검증 포켓/비용 사다리/피처 전이/이동 대조)",
        "segment_checks": "designed, not executed yet(설계됨, 아직 실행 전)",
        "trade_shape": "DP aggregate only; DR will materialize row tape(DP 집계만, DR이 행 테이프 물질화)",
        "alternative_explanations": "sample accident, residual serial dependence, proxy cost mismatch(표본 사고/잔여 연속 의존/프록시 비용 불일치)",
        "attribution_confidence": "low_until_DR_materialization(DR 물질화 전까지 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "DP review outputs and DQ design artifacts(DP 검토 출력과 DQ 설계 산출물)",
        "evidence_missing": "DR row-level materialization and later review(DR 행 단위 물질화와 이후 검토)",
        "judgment_label": "design_completed_materialization_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "지금은 새 모델을 고르는 단계가 아니라, 왜 검증이 약한지 더 촘촘히 볼 입력을 만든 단계다.",
    }
    paths = [
        write_json(EXPERIMENT_RECEIPT, experiment_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in list(artifact_paths) + paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_design_outputs_with_tracked_report(무시된 설계 산출물과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DQ Validation Support Control Residual Repair Design(검증 지지 대조 잔차 수리 설계)

## Conclusion(결론)

run337DQ(337DQ 실행)는 run337DP(337DP 실행)의 validation PF floor(검증 PF 하한), OOS-only lift(표본외 단독 개선), shifted control residual(이동 대조 잔차)을 다음 materialization(물질화) 계약으로 바꿨다.

이 작업은 design-only(설계 전용)이다. 새 학습, 후보 선택, 임계값 튜닝, MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 하지 않는다.

Effect(효과): run337DR(337DR 실행)은 전체 18개 모델의 row-level prediction/control/quarantine tape(행 단위 예측/대조/격리 테이프)를 만들어 수리 전 근거를 확보한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- validation_design_rows(검증 설계 행): `{final["validation_design_rows"]}`
- control_design_rows(대조 설계 행): `{final["control_design_rows"]}`
- quarantine_rows(격리 행): `{final["quarantine_rows"]}`
- tape_contract_rows(테이프 계약 행): `{final["tape_contract_rows"]}`
- dr_queue_rows(DR 대기열 행): `{final["dr_queue_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DQ

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): validation/control(검증/대조) 차단을 DR row-level materialization(행 단위 물질화)로 넘기고 선택/MT5/Forward(전진)는 계속 닫는다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(VALIDATION_SUPPORT_DESIGN)}`, `{rel(CONTROL_RESIDUAL_DESIGN)}`
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
        f"  Stage337 run337DQ focus complete: validation support/control residual repair design(검증 지지/대조 잔차 수리 설계)을 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DR(337DR 실행)에서 row-level prediction/control/quarantine tape(행 단위 예측/대조/격리 테이프)를 물질화한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DQ focus complete")
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
    section = f"""## Stage337 run337DQ(337DQ 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 검증/대조 차단을 행 단위 물질화 계약으로 바꿨지만 선택/MT5/Forward(전진)는 주장하지 않는다. Goal(목표)은 주장하지 않는다."""
    current_text = append_once(current_text, section, "Stage337 run337DQ(337DQ 실행)")
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection_text, _ = read_text_lossless(SELECTED_STATUS)
    selection = selection_text
    for field_name, value in {
        "latest_run": f"`{RUN_ID}`",
        "latest_decision": f"`{DECISION}`",
        "current_run": f"`{NEXT_RUN_ID}`",
        "rebuild_status": f"`{STATUS}`",
        "actual_mt5_execution": "`not_run_dq_design_only`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "effect": "`다음은 row-level prediction/control/quarantine tape materialization(행 단위 예측/대조/격리 테이프 물질화)이다.`",
    }.items():
        selection = replace_bullet_value(selection, field_name, value)
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337DQ(337DQ 실행) designed validation/control residual repair and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DQ(337DQ 실행) designed validation/control residual repair"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337DQ designed validation/control residual repair and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DQ designed validation/control residual repair"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "validation_support_control_residual_repair_design_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"validation_design={final['validation_design_rows']};control_design={final['control_design_rows']};quarantine={final['quarantine_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design_data_integrity_model_validation_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "design_no_training_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "design_from_proxy_review",
        "scoreboard_lane": "experiment_design_model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"quarantine_rows={final['quarantine_rows']};tape_contracts={final['tape_contract_rows']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_model_validation_performance_attribution_result_judgment",
        "evidence_scope": "validation/control repair design materialized",
        "kpi_scope": "design_contracts_from_DP_review",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_design",
        "family": "experiment_design_model_validation_performance_attribution_result_judgment",
        "question": "how to inspect validation weakness and shifted control residual without selecting winners",
        "metric_scope": "design_rows_quarantine_rows_tape_contracts",
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
    frames = load_frames()
    validation_rows = build_validation_design(frames)
    control_rows = build_control_design(frames)
    quarantine_rows = build_quarantine(frames)
    firewall_rows = build_firewall()
    tape_rows = build_tape_contract()
    queue_rows = build_dr_queue()
    artifacts: list[Path] = [
        write_csv(VALIDATION_SUPPORT_DESIGN, VALIDATION_DESIGN_COLUMNS, validation_rows),
        write_csv(CONTROL_RESIDUAL_DESIGN, CONTROL_DESIGN_COLUMNS, control_rows),
        write_csv(OOS_ONLY_QUARANTINE, QUARANTINE_COLUMNS, quarantine_rows),
        write_csv(RUNTIME_FIREWALL_DESIGN, FIREWALL_COLUMNS, firewall_rows),
        write_csv(ROW_LEVEL_TAPE_CONTRACT, TAPE_CONTRACT_COLUMNS, tape_rows),
        write_csv(DR_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    dp_final = read_json(DP_FINAL)
    dp_failed_gate_rows = sum(1 for row in read_csv(DP_GATES) if row.get("status") != "passed")
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dp_next_action": dp_final.get("next_action", ""),
        "dp_failed_gate_rows": dp_failed_gate_rows,
        "missing_inputs": len(missing),
        "dp_validation_pf_below_rows": int(dp_final.get("validation_pf_below_1p05_rows", 0)),
        "dp_oos_only_lift_rows": int(dp_final.get("oos_only_lift_rows", 0)),
        "dp_control_block_rows": int(dp_final.get("control_block_rows", 0)),
        "validation_design_rows": len(validation_rows),
        "control_design_rows": len(control_rows),
        "quarantine_rows": len(quarantine_rows),
        "runtime_firewall_rows": len(firewall_rows),
        "tape_contract_rows": len(tape_rows),
        "dr_queue_rows": len(queue_rows),
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
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
