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
from stage_pipelines.stage337 import review_broad_validation_failure_control_residual_materialization as dv  # noqa: E402
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
STAGE_ID = dv.STAGE_ID
RUN_NUMBER = "run337DW"
RUN_ID = "run337DW_design_transfer_density_control_objective_repair_without_db_v1"
PARENT_RUN_ID = dv.RUN_ID
NEXT_RUN_ID = "run337DX_materialize_transfer_density_control_objective_repair_inputs_without_db_v1"
STATUS = "completed_stage337DW_transfer_density_control_objective_repair_design_no_training_no_selection"
JUDGMENT = "repair_design_ready_for_train_only_objective_density_control_wfo_materialization"
DECISION = "stage337DW_open_run337DX_materialize_transfer_density_control_objective_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DW_transfer_density_control_objective_repair_design_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dv.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dv.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DW_transfer_density_control_objective_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DW_transfer_density_control_objective_repair_design.md"
SELECTED_STATUS = dv.SELECTED_STATUS
STAGE_BRIEF = dv.STAGE_BRIEF
WORKSPACE_STATE = dv.WORKSPACE_STATE
CURRENT_STATE = dv.CURRENT_STATE
CHANGELOG = dv.CHANGELOG
RUN_REGISTRY = dv.RUN_REGISTRY
ALPHA_LEDGER = dv.ALPHA_LEDGER
ARTIFACT_REGISTRY = dv.ARTIFACT_REGISTRY
STAGE_LEDGER = dv.STAGE_LEDGER

DV_FINAL = dv.FINAL_DECISION
DV_GATES = dv.REQUIRED_GATE_AUDIT
DV_QUEUE = dv.DW_QUEUE
TRANSFER_BREAK_REVIEW = dv.TRANSFER_BREAK_REVIEW
DENSITY_DRAWDOWN_REVIEW = dv.DENSITY_DRAWDOWN_REVIEW
CONTROL_ISOLATION_REVIEW = dv.CONTROL_ISOLATION_REVIEW
FAMILY_MEMORY_FIREWALL_REVIEW = dv.FAMILY_MEMORY_FIREWALL_REVIEW
WFO_OBJECTIVE_PRECHECK_REVIEW = dv.WFO_OBJECTIVE_PRECHECK_REVIEW

TRAIN_ONLY_OBJECTIVE_CONTRACTS = RUN_DIR / "train_only_objective_contracts.csv"
DENSITY_DECONCENTRATION_CONTRACTS = RUN_DIR / "density_deconcentration_contracts.csv"
CONTROL_RESIDUAL_ISOLATION_CONTRACTS = RUN_DIR / "control_residual_isolation_contracts.csv"
WFO_EMBARGO_PRECHECK_DESIGN = RUN_DIR / "wfo_embargo_precheck_design.csv"
NO_RELEASE_FIREWALL_DESIGN = RUN_DIR / "no_release_firewall_design.csv"
DX_QUEUE = RUN_DIR / "run337DX_materialization_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DV_FINAL,
    DV_GATES,
    DV_QUEUE,
    TRANSFER_BREAK_REVIEW,
    DENSITY_DRAWDOWN_REVIEW,
    CONTROL_ISOLATION_REVIEW,
    FAMILY_MEMORY_FIREWALL_REVIEW,
    WFO_OBJECTIVE_PRECHECK_REVIEW,
)
OUTPUT_FILES = (
    TRAIN_ONLY_OBJECTIVE_CONTRACTS,
    DENSITY_DECONCENTRATION_CONTRACTS,
    CONTROL_RESIDUAL_ISOLATION_CONTRACTS,
    WFO_EMBARGO_PRECHECK_DESIGN,
    NO_RELEASE_FIREWALL_DESIGN,
    DX_QUEUE,
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

OBJECTIVE_COLUMNS = (
    "contract_id",
    "repair_axis",
    "source_blocker",
    "materialization_instruction",
    "success_condition",
    "failure_condition",
    "invalid_condition",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
DESIGN_COLUMNS = (
    "contract_id",
    "repair_axis",
    "source_blocker",
    "materialization_instruction",
    "success_condition",
    "failure_condition",
    "invalid_condition",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "blocked_action_or_claim",
    "blocked_reason",
    "carry_status",
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


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def count_contains(rows: Sequence[Mapping[str, Any]], column: str, pattern: str) -> int:
    return sum(pattern in str(row.get(column, "")) for row in rows)


def build_objective_contracts(final: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "contract_id": "train_only_abstention_cost_margin_label",
            "repair_axis": "objective(목표)",
            "source_blocker": f"validation_floor_blocks={final['validation_floor_block_rows']};high_density={final['high_density_validation_rows']}",
            "materialization_instruction": "DX builds train-split abstention-aware cost margin tags without validation/OOS labels(DX가 검증/OOS 라벨 없이 학습 분할 보류 인식 비용 여백 태그 생성)",
            "success_condition": "tags exist for train rows and are audit-only before review(태그가 학습 행에 존재하고 리뷰 전 감사 전용)",
            "failure_condition": "tags cannot separate flat/low-margin overtrading(태그가 flat/저여백 과매매를 분리하지 못함)",
            "invalid_condition": "validation/OOS outcomes enter label definition(검증/OOS 결과가 라벨 정의에 들어감)",
            "forbidden_action": "no training, no threshold tuning(학습/임계값 튜닝 금지)",
            "effect": "opens objective repair without selecting a model(모델 선택 없이 목표 수리 열기)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "train_only_drawdown_pressure_tag",
            "repair_axis": "risk_shape(위험 형태)",
            "source_blocker": f"density_review_rows={final['density_review_rows']}",
            "materialization_instruction": "DX tags train rows by local underwater/drawdown pressure from existing action tape(DX가 기존 행동 테이프의 국소 침수/드로다운 압력으로 학습 행 태그)",
            "success_condition": "drawdown pressure tag is available for later objective review(드로다운 압력 태그가 이후 목표 검토에 사용 가능)",
            "failure_condition": "drawdown pressure is uniform and not informative(드로다운 압력이 균일해 정보가 없음)",
            "invalid_condition": "validation drawdown is used as a training penalty(검증 드로다운을 학습 페널티로 사용)",
            "forbidden_action": "no validation risk retune(검증 위험 재튜닝 금지)",
            "effect": "makes curve pocket pressure observable before training(학습 전 곡선 포켓 압력 관찰 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "train_only_direction_residual_tag",
            "repair_axis": "direction(방향)",
            "source_blocker": f"transfer_breaks={final['transfer_break_rows']}",
            "materialization_instruction": "DX creates train-only residual tags for long/short imbalance and post-cost direction mismatch(DX가 롱/숏 불균형과 비용 후 방향 불일치 학습 전용 잔차 태그 생성)",
            "success_condition": "direction residual can be reviewed against validation without being chosen(방향 잔차를 선택 없이 검증과 비교 가능)",
            "failure_condition": "residual is indistinguishable from random direction noise(잔차가 무작위 방향 잡음과 구분 안 됨)",
            "invalid_condition": "validation direction outcome defines the residual(검증 방향 결과가 잔차를 정의)",
            "forbidden_action": "no validation direction filter(검증 방향 필터 금지)",
            "effect": "separates direction weakness from cost weakness(방향 약점과 비용 약점 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "oos_lift_quarantine_binding",
            "repair_axis": "selection_firewall(선택 방화벽)",
            "source_blocker": f"oos_lift_rows={final['oos_lift_rows']}",
            "materialization_instruction": "DX carries OOS-only lift rows as quarantine metadata, not positive labels(DX가 OOS 단독 개선 행을 긍정 라벨이 아닌 격리 메타데이터로 전달)",
            "success_condition": "quarantine rows are visible and cannot enter scoring objective(격리 행이 보이며 점수 목표에 들어가지 못함)",
            "failure_condition": "OOS-only lift remains unexplained but isolated(OOS 단독 개선은 설명 안 되지만 격리됨)",
            "invalid_condition": "OOS lift is treated as winner evidence(OOS 개선을 승자 근거로 취급)",
            "forbidden_action": "no OOS-based shortlist(OOS 기반 후보 목록 금지)",
            "effect": "keeps overfit pressure from OOS-only pockets(OOS 단독 포켓 과적합 압력 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "objective_review_firewall",
            "repair_axis": "review_boundary(검토 경계)",
            "source_blocker": "DV review release blocked(DV 검토 해제 차단)",
            "materialization_instruction": "DX emits objective inputs only; training opens only after separate review(DX는 목표 입력만 생성하고 별도 검토 후 학습 가능)",
            "success_condition": "DX output can be reviewed without any trained model(DX 출력이 학습 모델 없이 검토 가능)",
            "failure_condition": "inputs are too weak to justify guarded training(입력이 방어 학습을 정당화하기에 약함)",
            "invalid_condition": "DX starts model fitting(DX가 모델 적합 시작)",
            "forbidden_action": "no model training in DW/DX(DW/DX 모델 학습 금지)",
            "effect": "keeps design and execution stages separate(설계와 실행 단계 분리 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_density_contracts(final: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "contract_id": "train_only_density_profile",
            "repair_axis": "density(밀도)",
            "source_blocker": f"high_density_validation_rows={final['high_density_validation_rows']}",
            "materialization_instruction": "DX profiles action density using train rows and existing predictions only(DX가 학습 행과 기존 예측만으로 행동 밀도 프로필 생성)",
            "success_condition": "density profile is available by model/split without tuning(모델/분할별 밀도 프로필을 튜닝 없이 사용 가능)",
            "failure_condition": "density pressure is not separable from model family(밀도 압력이 모델 계열과 분리 안 됨)",
            "invalid_condition": "validation density threshold is selected(검증 밀도 임계값 선택)",
            "forbidden_action": "no density threshold search(밀도 임계값 탐색 금지)",
            "effect": "makes overbroad action surface measurable(과넓은 행동 표면 측정 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "drawdown_pocket_profile",
            "repair_axis": "curve_pocket(곡선 포켓)",
            "source_blocker": "DV density/drawdown review(DV 밀도/드로다운 검토)",
            "materialization_instruction": "DX tags contiguous underwater pockets from frozen prediction tape(DX가 고정 예측 테이프의 연속 침수 포켓 태그 생성)",
            "success_condition": "underwater pocket tags exist without changing trades(거래 변경 없이 침수 포켓 태그 존재)",
            "failure_condition": "underwater pockets are diffuse and not actionable(침수 포켓이 넓게 퍼져 조치 어려움)",
            "invalid_condition": "pocket tags are used as filters before review(포켓 태그를 검토 전 필터로 사용)",
            "forbidden_action": "no curve-pocket filter(곡선 포켓 필터 금지)",
            "effect": "turns curve shape into evidence, not selection(곡선 형태를 선택이 아닌 근거로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "action_entropy_profile",
            "repair_axis": "action_mix(행동 혼합)",
            "source_blocker": "validation argmax overbreadth(검증 argmax 과다)",
            "materialization_instruction": "DX profiles flat/long/short entropy by split and model family(DX가 분할/모델 계열별 flat/long/short 엔트로피 프로필 생성)",
            "success_condition": "action mix imbalance is named before future objective(미래 목표 전 행동 혼합 불균형 명명)",
            "failure_condition": "action mix is balanced but still weak(행동 혼합은 균형이나 여전히 약함)",
            "invalid_condition": "entropy becomes a validation-tuned selector(엔트로피가 검증 튜닝 선택자가 됨)",
            "forbidden_action": "no action-mix shortlist(행동 혼합 기반 후보 목록 금지)",
            "effect": "distinguishes action overbreadth from directional signal(행동 과다와 방향 신호 구분)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "density_release_firewall",
            "repair_axis": "release_boundary(해제 경계)",
            "source_blocker": "density pressure blocks release(밀도 압력이 해제 차단)",
            "materialization_instruction": "DX writes density metrics as review-only columns(DX가 밀도 지표를 검토 전용 열로 기록)",
            "success_condition": "density metrics cannot alter score threshold(밀도 지표가 점수 임계값을 바꾸지 못함)",
            "failure_condition": "density remains high after future repair(미래 수리 후에도 밀도 높음)",
            "invalid_condition": "density metric changes trade decision in DX(DX에서 밀도 지표가 거래 결정을 바꿈)",
            "forbidden_action": "no lot or threshold optimization(랏 또는 임계값 최적화 금지)",
            "effect": "keeps density work diagnostic(밀도 작업을 진단으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_control_contracts(final: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "contract_id": "technical_extratrees_shifted_residual_isolation",
            "repair_axis": "control_residual(대조 잔차)",
            "source_blocker": f"control_block_rows={final['control_block_rows']}",
            "materialization_instruction": "DX isolates technical ExtraTrees shifted-control blocks by source order, hour, month, and cost ladder(DX가 technical ExtraTrees 이동 대조 차단을 원천 순서/시간/월/비용 사다리로 격리)",
            "success_condition": "blocked lineage signature is localized or confirmed broad(차단 계열 서명이 국소화되거나 넓음으로 확인)",
            "failure_condition": "control residual cannot be separated from candidate signal(대조 잔차와 후보 신호 분리 실패)",
            "invalid_condition": "control rule is relaxed to pass(통과시키려고 대조 규칙 완화)",
            "forbidden_action": "no control threshold relaxation(대조 임계값 완화 금지)",
            "effect": "keeps serial residual blocker explicit(연속 잔차 차단 명시 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "fixed_control_rule_carry",
            "repair_axis": "control_policy(대조 정책)",
            "source_blocker": "DV control review(DV 대조 검토)",
            "materialization_instruction": "DX carries alignment>=max(0.45,candidate-0.02) unchanged(DX가 alignment>=max(0.45,candidate-0.02)를 그대로 전달)",
            "success_condition": "control policy hash/description remains unchanged(대조 정책 해시/설명 불변)",
            "failure_condition": "future candidate is blocked by same rule(미래 후보가 같은 규칙에 차단)",
            "invalid_condition": "policy changes inside materialization(물질화 안에서 정책 변경)",
            "forbidden_action": "no control retuning(대조 재튜닝 금지)",
            "effect": "keeps overfit guard stable(과적합 방어 안정 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "nonblocking_controls_keepalive",
            "repair_axis": "audit_breadth(감사 폭)",
            "source_blocker": "noise/block-shuffle controls are non-blocking but required(잡음/블록 셔플 대조는 비차단이나 필수)",
            "materialization_instruction": "DX keeps noise and block-shuffle controls in every review table(DX가 모든 리뷰 표에 잡음 및 블록 셔플 대조 유지)",
            "success_condition": "all controls appear even when not blocking(차단하지 않아도 모든 대조 등장)",
            "failure_condition": "nonblocking controls add no insight(비차단 대조가 통찰 없음)",
            "invalid_condition": "passing controls are dropped(통과 대조 삭제)",
            "forbidden_action": "no control deletion(대조 삭제 금지)",
            "effect": "prevents narrow control review(좁은 대조 검토 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "control_runtime_firewall",
            "repair_axis": "runtime_boundary(런타임 경계)",
            "source_blocker": "shifted-control block prevents runtime probe(이동 대조 차단은 런타임 탐침 차단)",
            "materialization_instruction": "DX emits runtime-blocking disposition for any control-blocked lineage(DX가 대조 차단 계열에 런타임 차단 처분 기록)",
            "success_condition": "runtime queue remains empty while controls block(대조가 차단하는 동안 런타임 대기열 비어 있음)",
            "failure_condition": "all future variants remain control-blocked(미래 변형 전체가 대조 차단 유지)",
            "invalid_condition": "blocked lineage enters MT5 queue(차단 계열이 MT5 대기열 진입)",
            "forbidden_action": "no MT5 probe from blocked controls(대조 차단 상태 MT5 탐침 금지)",
            "effect": "keeps runtime claims closed(런타임 주장 닫힘 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_wfo_design(final: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "contract_id": "rolling_origin_precheck",
            "repair_axis": "WFO(WFO)",
            "source_blocker": "single split evidence insufficient(단일 분할 근거 부족)",
            "materialization_instruction": "DX writes rolling-origin split feasibility from existing timestamp range(DX가 기존 시점 범위로 rolling-origin 분할 가능성 기록)",
            "success_condition": "future training knows feasible windows before fitting(미래 학습이 적합 전 가능 창을 앎)",
            "failure_condition": "timestamp range cannot support enough folds(시점 범위가 충분한 fold를 지원 못함)",
            "invalid_condition": "folds are chosen after model result(모델 결과 후 fold 선택)",
            "forbidden_action": "no post-selection WFO backfill(선택 후 WFO 사후 보강 금지)",
            "effect": "keeps forward robustness standard ahead of training(학습 전 전진 강건성 기준 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "purge_embargo_precheck",
            "repair_axis": "serial_dependence(연속 의존)",
            "source_blocker": "shifted-control residual(이동 대조 잔차)",
            "materialization_instruction": "DX computes purge/embargo feasibility around horizon and source order(DX가 horizon/source order 기준 purge/embargo 가능성 계산)",
            "success_condition": "embargo gap can be named without training(학습 없이 embargo 간격 명명 가능)",
            "failure_condition": "purge removes too much training data(purge가 학습 데이터를 너무 많이 제거)",
            "invalid_condition": "embargo is skipped to preserve KPI(성과 보존 위해 embargo 생략)",
            "forbidden_action": "no skip of serial-dependence guard(연속 의존 방어 생략 금지)",
            "effect": "links control residual to split design(대조 잔차를 분할 설계와 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "completed_day_boundary_policy",
            "repair_axis": "tester_boundary(테스터 경계)",
            "source_blocker": "current-day tester gap history(현재일 테스터 공백 이력)",
            "materialization_instruction": "DX carries completed-day-only evidence boundary into future MT5 planning(DX가 완성일 전용 근거 경계를 미래 MT5 계획으로 전달)",
            "success_condition": "future runtime probe queue states completed-day requirement(미래 런타임 탐침 대기열이 완성일 필요조건 명시)",
            "failure_condition": "broker boundary remains unavailable(브로커 경계 여전히 불가)",
            "invalid_condition": "current-day gap is treated as pass(현재일 공백을 통과로 취급)",
            "forbidden_action": "no forward decision from incomplete tester day(불완성 테스터 일자로 전진 판정 금지)",
            "effect": "keeps external verification boundary honest(외부 검증 경계 정직하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "wfo_release_firewall",
            "repair_axis": "claim_boundary(주장 경계)",
            "source_blocker": f"validation_floor_blocks={final['validation_floor_block_rows']}",
            "materialization_instruction": "DX marks WFO precheck as prerequisite, not proof(DX가 WFO 사전검사를 증명이 아닌 전제로 표시)",
            "success_condition": "future report cannot claim readiness from precheck alone(미래 보고서가 사전검사만으로 준비성 주장 불가)",
            "failure_condition": "WFO precheck exposes infeasible data geometry(WFO 사전검사가 불가능한 데이터 구조 노출)",
            "invalid_condition": "precheck is reported as Forward Passed(사전검사를 Forward Passed로 보고)",
            "forbidden_action": "no Forward/Goal claim(전진/목표 주장 금지)",
            "effect": "prevents readiness language from design artifacts(설계 산출물이 준비성 언어가 되는 것 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_firewall_rows() -> list[dict[str, str]]:
    return [
        {
            "firewall_id": "no_model_training_in_dw_dx",
            "blocked_action_or_claim": "model_training(모델 학습)",
            "blocked_reason": "DW/DX are design/materialization only(DW/DX는 설계/물질화 전용)",
            "carry_status": "active",
            "effect": "prevents repair design from becoming hidden training(수리 설계가 숨은 학습이 되는 것 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_threshold_or_density_tuning",
            "blocked_action_or_claim": "threshold_or_density_tuning(임계값 또는 밀도 튜닝)",
            "blocked_reason": "validation weakness cannot become selector(검증 약점이 선택자가 되면 안 됨)",
            "carry_status": "active",
            "effect": "prevents repair-overfit(수리 과적합 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_control_relaxation",
            "blocked_action_or_claim": "control_relaxation(대조 완화)",
            "blocked_reason": "shifted-control block is evidence, not nuisance(이동 대조 차단은 잡음이 아니라 근거)",
            "carry_status": "active",
            "effect": "keeps overfit guard stable(과적합 방어 안정 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_oos_lift_selection",
            "blocked_action_or_claim": "OOS-only shortlist(OOS 단독 후보 목록)",
            "blocked_reason": "OOS lift is quarantined until validation repair(OOS 개선은 검증 수리 전 격리)",
            "carry_status": "active",
            "effect": "blocks OOS-pocket overfit(OOS 포켓 과적합 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_mt5_forward_goal_claim",
            "blocked_action_or_claim": "MT5/Forward/Goal claim(MT5/전진/목표 주장)",
            "blocked_reason": "design has no runtime or forward evidence(설계에는 런타임/전진 근거 없음)",
            "carry_status": "active",
            "effect": "keeps claim boundary honest(주장 경계 정직하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_dx_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DX_materialize_train_only_objective_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize train-only objective inputs(학습 전용 목표 입력 물질화)",
            "required_inputs": rel(TRAIN_ONLY_OBJECTIVE_CONTRACTS),
            "required_outputs": "train_only_objective_input_frame.parquet;objective_contract_audit.csv",
            "blocked_if_missing": "objective contracts(목표 계약)",
            "forbidden_action": "no model training(모델 학습 금지)",
            "effect": "turns design into auditable labels/tags(설계를 감사 가능한 라벨/태그로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DX_materialize_density_deconcentration_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize density deconcentration inputs(밀도 탈집중 입력 물질화)",
            "required_inputs": rel(DENSITY_DECONCENTRATION_CONTRACTS),
            "required_outputs": "density_deconcentration_matrix.csv",
            "blocked_if_missing": "density contracts(밀도 계약)",
            "forbidden_action": "no density threshold tuning(밀도 임계값 튜닝 금지)",
            "effect": "makes action overbreadth testable(행동 과다를 시험 가능하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DX_materialize_control_isolation_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize control residual isolation inputs(대조 잔차 격리 입력 물질화)",
            "required_inputs": rel(CONTROL_RESIDUAL_ISOLATION_CONTRACTS),
            "required_outputs": "control_residual_isolation_matrix.csv",
            "blocked_if_missing": "control contracts(대조 계약)",
            "forbidden_action": "no control relaxation(대조 완화 금지)",
            "effect": "isolates serial residual before any training(학습 전 연속 잔차 격리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DX_materialize_wfo_embargo_precheck",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "materialize WFO/embargo precheck(WFO/격리 사전검사 물질화)",
            "required_inputs": rel(WFO_EMBARGO_PRECHECK_DESIGN),
            "required_outputs": "wfo_embargo_feasibility.csv",
            "blocked_if_missing": "WFO design(WFO 설계)",
            "forbidden_action": "no post-selection WFO(선택 후 WFO 금지)",
            "effect": "checks data geometry before future training(미래 학습 전 데이터 구조 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DX_carry_no_release_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "carry no-release firewall(무해제 방화벽 전달)",
            "required_inputs": rel(NO_RELEASE_FIREWALL_DESIGN),
            "required_outputs": "no_release_firewall_carry.csv",
            "blocked_if_missing": "firewall design(방화벽 설계)",
            "forbidden_action": "no candidate selection/MT5/Forward/Goal(후보 선택/MT5/전진/목표 금지)",
            "effect": "keeps materialization from becoming promotion(물질화가 승격으로 변하는 것 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DV inputs exist(필수 DV 입력 존재)"),
        ("parent_dv_gates_passed", final["dv_failed_gate_rows"] == 0, str(final["dv_failed_gate_rows"]), "0", "DV review usable(DV 검토 사용 가능)"),
        ("parent_next_action_matches", final["dv_next_action"] == RUN_ID, str(final["dv_next_action"]), RUN_ID, "continues DV queue(DV 대기열을 이어감)"),
        ("objective_contracts_materialized", final["objective_contract_rows"] >= 5, str(final["objective_contract_rows"]), ">=5", "objective contracts created(목표 계약 생성)"),
        ("density_contracts_materialized", final["density_contract_rows"] >= 4, str(final["density_contract_rows"]), ">=4", "density contracts created(밀도 계약 생성)"),
        ("control_contracts_materialized", final["control_contract_rows"] >= 4, str(final["control_contract_rows"]), ">=4", "control contracts created(대조 계약 생성)"),
        ("wfo_design_materialized", final["wfo_design_rows"] >= 4, str(final["wfo_design_rows"]), ">=4", "WFO design created(WFO 설계 생성)"),
        ("firewall_materialized", final["firewall_rows"] >= 5, str(final["firewall_rows"]), ">=5", "firewall rows created(방화벽 행 생성)"),
        ("dx_queue_materialized", final["dx_queue_rows"] == 5, str(final["dx_queue_rows"]), "5", "DX queue opened(DX 대기열 열림)"),
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
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "DV review artifacts only; no new market rows(DV 검토 산출물 전용, 새 시장 행 없음)",
        "sample_scope": f"validation_floor_blocks={final['validation_floor_block_rows']};transfer_breaks={final['transfer_break_rows']};control_blocks={final['control_block_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']}",
        "feature_label_boundary": "design contracts only; no labels materialized in DW(DW는 설계 계약만, 라벨 물질화 없음)",
        "split_boundary": "WFO/embargo designed as precheck, not executed(WFO/격리는 실행이 아니라 사전검사 설계)",
        "leakage_risk": "using validation blockers as tuned filters(검증 차단 요소를 튜닝 필터로 쓰는 위험)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_design_no_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "no model training; design for future repair inputs(모델 학습 없음, 미래 수리 입력 설계)",
        "target_and_label": "future train-only tags specified but not materialized(미래 학습 전용 태그 명세만 있고 물질화 전)",
        "split_method": "WFO/embargo precheck design(WFO/격리 사전검사 설계)",
        "selection_metric": "none(없음)",
        "secondary_metrics": "transfer, density, control, WFO blockers carried(전이/밀도/대조/WFO 차단 전달)",
        "threshold_policy": "no threshold tuning(임계값 튜닝 없음)",
        "overfit_risk": "repair-overfit through validation filters(검증 필터를 통한 수리 과적합)",
        "calibration_risk": "not applicable; no score calibration(해당 없음, 점수 보정 없음)",
        "comparison_baseline": rel(DV_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": "design generated from DV blockers(DV 차단 요소에서 설계 생성)",
        "comparison_baseline": rel(DV_FINAL),
        "likely_drivers": "broad validation floor, density pressure, shifted-control residual, WFO gap(넓은 검증 하한/밀도 압력/이동 대조 잔차/WFO 공백)",
        "segment_checks": f"objective={final['objective_contract_rows']};density={final['density_contract_rows']};control={final['control_contract_rows']};wfo={final['wfo_design_rows']}",
        "trade_shape": "not measured in design-only run(설계 전용 실행이라 측정 안 함)",
        "alternative_explanations": "label mismatch or market regime drift remains possible(라벨 불일치 또는 시장 레짐 변화 가능)",
        "attribution_confidence": "design_ready_not_result(결과가 아니라 설계 준비)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "design contracts, DX queue, gates, receipts(설계 계약/DX 대기열/게이트/영수증)",
        "evidence_missing": "DX materialization, review, training, MT5, forward evidence(DX 물질화/검토/학습/MT5/전진 근거)",
        "judgment_label": "design_completed_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "이번 단계는 무엇을 고칠지 계약으로 고정했고, 아직 고친 결과를 주장하지 않는다.",
    }
    paths = [
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
        "availability": "ignored_design_outputs_with_tracked_report(무시된 설계 출력과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DW Transfer Density Control Objective Repair Design(전이/밀도/대조/목표 수리 설계)

## Conclusion(결론)

run337DW(337DW 실행)는 DV 차단 근거를 DX 물질화 계약으로 바꿨다.

설계 축은 train-only objective(학습 전용 목표), density deconcentration(밀도 탈집중), shifted-control isolation(이동 대조 격리), WFO/embargo precheck(WFO/격리 사전검사), no-release firewall(무해제 방화벽)이다.

이 작업은 design-only(설계 전용)이다. 새 학습, 후보 선택, 임계값 튜닝, MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 하지 않는다.

Effect(효과): run337DX(337DX 실행)는 설계를 실제 입력 테이블로 물질화하고, 그 뒤 별도 리뷰 없이는 학습으로 넘어가지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- objective_contract_rows(목표 계약 행): `{final["objective_contract_rows"]}`
- density_contract_rows(밀도 계약 행): `{final["density_contract_rows"]}`
- control_contract_rows(대조 계약 행): `{final["control_contract_rows"]}`
- wfo_design_rows(WFO 설계 행): `{final["wfo_design_rows"]}`
- firewall_rows(방화벽 행): `{final["firewall_rows"]}`
- dx_queue_rows(DX 대기열 행): `{final["dx_queue_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DW

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 수리 방향을 DX 물질화 계약으로 고정했지만 선택/학습/MT5/Forward(전진)는 닫는다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(TRAIN_ONLY_OBJECTIVE_CONTRACTS)}`, `{rel(DX_QUEUE)}`
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
        f"  Stage337 run337DW focus complete: transfer/density/control/objective repair design(전이/밀도/대조/목표 수리 설계)을 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DX(337DX 실행)에서 train-only objective/density/control/WFO contracts(학습 전용 목표/밀도/대조/WFO 계약)를 물질화한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DW focus complete")
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
    section = f"""## Stage337 run337DW(337DW 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 수리 설계를 물질화 대기열로 만들었지만 학습/선택/MT5/Forward(전진)는 주장하지 않는다. Goal(목표)은 주장하지 않는다."""
    current_text = append_once(current_text, section, "Stage337 run337DW(337DW 실행)")
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection_text, _ = read_text_lossless(SELECTED_STATUS)
    selection = selection_text
    for field_name, value in {
        "latest_run": f"`{RUN_ID}`",
        "latest_decision": f"`{DECISION}`",
        "current_run": f"`{NEXT_RUN_ID}`",
        "rebuild_status": f"`{STATUS}`",
        "actual_mt5_execution": "`not_run_dw_design_only`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "effect": "`다음은 transfer/density/control/objective input materialization(전이/밀도/대조/목표 입력 물질화)이다.`",
    }.items():
        selection = replace_bullet_value(selection, field_name, value)
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337DW(337DW 실행) designed transfer/density/control/objective repair contracts and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DW(337DW 실행) designed transfer"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337DW designed transfer/density/control/objective repair contracts and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DW designed transfer"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "transfer_density_control_objective_repair_design_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"objective={final['objective_contract_rows']};density={final['density_contract_rows']};control={final['control_contract_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design_model_validation_result_judgment",
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
        "kpi_scope": "design_contracts_no_kpi",
        "scoreboard_lane": "experiment_design_model_validation_result_judgment",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"objective={final['objective_contract_rows']};density={final['density_contract_rows']};control={final['control_contract_rows']};wfo={final['wfo_design_rows']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_model_validation_result_judgment",
        "evidence_scope": "repair contracts designed",
        "kpi_scope": "design_contracts",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_design",
        "family": "experiment_design_model_validation_result_judgment",
        "question": "how to repair transfer density and control blockers without overfit tuning",
        "metric_scope": "objective_density_control_wfo_design",
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

    dv_final = read_json(DV_FINAL)
    dv_failed_gate_rows = sum(1 for row in read_csv(DV_GATES) if row.get("status") != "passed")
    transfer_review = read_csv(TRANSFER_BREAK_REVIEW)
    density_review = read_csv(DENSITY_DRAWDOWN_REVIEW)
    control_review = read_csv(CONTROL_ISOLATION_REVIEW)
    wfo_review = read_csv(WFO_OBJECTIVE_PRECHECK_REVIEW)
    final_seed = {
        **dv_final,
        "dv_failed_gate_rows": dv_failed_gate_rows,
        "transfer_review_rows": len(transfer_review),
        "density_review_rows": len(density_review),
        "control_review_rows": len(control_review),
        "wfo_review_rows": len(wfo_review),
    }
    objective_rows = build_objective_contracts(final_seed)
    density_rows = build_density_contracts(final_seed)
    control_rows = build_control_contracts(final_seed)
    wfo_rows = build_wfo_design(final_seed)
    firewall_rows = build_firewall_rows()
    queue_rows = build_dx_queue()
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dv_next_action": dv_final.get("next_action", ""),
        "dv_failed_gate_rows": dv_failed_gate_rows,
        "missing_inputs": len(missing),
        "validation_floor_block_rows": int(dv_final.get("validation_floor_block_rows", 0)),
        "transfer_break_rows": int(dv_final.get("transfer_break_rows", 0)),
        "oos_lift_rows": int(dv_final.get("oos_lift_rows", 0)),
        "high_density_validation_rows": int(dv_final.get("high_density_validation_rows", 0)),
        "control_block_rows": int(dv_final.get("control_block_rows", 0)),
        "objective_contract_rows": len(objective_rows),
        "density_contract_rows": len(density_rows),
        "control_contract_rows": len(control_rows),
        "wfo_design_rows": len(wfo_rows),
        "firewall_rows": len(firewall_rows),
        "dx_queue_rows": len(queue_rows),
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
        write_csv(TRAIN_ONLY_OBJECTIVE_CONTRACTS, OBJECTIVE_COLUMNS, objective_rows),
        write_csv(DENSITY_DECONCENTRATION_CONTRACTS, DESIGN_COLUMNS, density_rows),
        write_csv(CONTROL_RESIDUAL_ISOLATION_CONTRACTS, DESIGN_COLUMNS, control_rows),
        write_csv(WFO_EMBARGO_PRECHECK_DESIGN, DESIGN_COLUMNS, wfo_rows),
        write_csv(NO_RELEASE_FIREWALL_DESIGN, FIREWALL_COLUMNS, firewall_rows),
        write_csv(DX_QUEUE, QUEUE_COLUMNS, queue_rows),
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
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
