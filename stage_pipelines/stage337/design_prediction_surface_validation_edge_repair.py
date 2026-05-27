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
from stage_pipelines.stage337 import review_pair_prediction_tape_surface_attribution as dk  # noqa: E402
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
STAGE_ID = dk.STAGE_ID
RUN_NUMBER = "run337DL"
RUN_ID = "run337DL_design_prediction_surface_validation_edge_repair_without_db_v1"
PARENT_RUN_ID = dk.RUN_ID
NEXT_RUN_ID = "run337DM_materialize_prediction_surface_validation_edge_repair_inputs_without_db_v1"
STATUS = "completed_stage337DL_prediction_surface_validation_edge_repair_design_no_training_no_selection"
JUDGMENT = "repair_design_ready_for_validation_edge_surface_deconcentration_materialization"
DECISION = "stage337DL_open_run337DM_materialize_prediction_surface_validation_edge_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DL_prediction_surface_validation_edge_repair_design_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dk.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dk.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DL_prediction_surface_validation_edge_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DL_prediction_surface_validation_edge_repair_design.md"
SELECTED_STATUS = dk.SELECTED_STATUS
STAGE_BRIEF = dk.STAGE_BRIEF
WORKSPACE_STATE = dk.WORKSPACE_STATE
CURRENT_STATE = dk.CURRENT_STATE
CHANGELOG = dk.CHANGELOG
RUN_REGISTRY = dk.RUN_REGISTRY
ALPHA_LEDGER = dk.ALPHA_LEDGER
ARTIFACT_REGISTRY = dk.ARTIFACT_REGISTRY
STAGE_LEDGER = dk.STAGE_LEDGER

DK_FINAL = dk.FINAL_DECISION
DK_GATES = dk.REQUIRED_GATE_AUDIT
DK_QUEUE = dk.DL_QUEUE
DK_FAILURE_MEMORY = dk.FAILURE_MEMORY
DK_SLICE_BLOCKERS = dk.SLICE_BLOCKERS
DK_CURVE_REVIEW = dk.CURVE_REVIEW
DK_SURFACE_REVIEW = dk.SURFACE_REVIEW
DK_REPLAY_REVIEW = dk.REPLAY_REVIEW
DJ_SURFACE_AUDIT = dk.DJ_SURFACE_AUDIT
DJ_RELEASE_BLOCKERS = dk.DJ_RELEASE_BLOCKERS

VALIDATION_EDGE_CONTRACT = RUN_DIR / "validation_edge_repair_contract.csv"
SURFACE_DECONTRACT = RUN_DIR / "surface_deconcentration_repair_contract.csv"
BALANCED_QUEUE = RUN_DIR / "balanced_repair_attack_design_queue.csv"
RUNTIME_FIREWALL = RUN_DIR / "runtime_firewall_contract.csv"
NO_OVERFIT_GUARDRAILS = RUN_DIR / "no_overfit_guardrail_matrix.csv"
DM_QUEUE = RUN_DIR / "run337DM_materialization_queue.csv"
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
    DK_FINAL,
    DK_GATES,
    DK_QUEUE,
    DK_FAILURE_MEMORY,
    DK_SLICE_BLOCKERS,
    DK_CURVE_REVIEW,
    DK_SURFACE_REVIEW,
    DK_REPLAY_REVIEW,
    DJ_SURFACE_AUDIT,
    DJ_RELEASE_BLOCKERS,
)
OUTPUT_FILES = (
    VALIDATION_EDGE_CONTRACT,
    SURFACE_DECONTRACT,
    BALANCED_QUEUE,
    RUNTIME_FIREWALL,
    NO_OVERFIT_GUARDRAILS,
    DM_QUEUE,
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

VALIDATION_COLUMNS = (
    "contract_id",
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
    "forbidden_use",
    "effect",
    "claim_boundary",
)
SURFACE_COLUMNS = (
    "contract_id",
    "surface_axis",
    "observed_blocker",
    "design_response",
    "required_stability_check",
    "success_criteria",
    "failure_criteria",
    "forbidden_use",
    "evidence_output",
    "effect",
    "claim_boundary",
)
BALANCED_COLUMNS = (
    "design_id",
    "lane",
    "priority",
    "task",
    "changed_variables",
    "fixed_variables",
    "required_inputs",
    "required_outputs",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "held_action",
    "held_until",
    "required_evidence",
    "forbidden_claim",
    "effect",
    "claim_boundary",
)
GUARDRAIL_COLUMNS = (
    "guardrail_id",
    "risk",
    "required_control",
    "blocks_if",
    "evidence_output",
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


def count_by(rows: Sequence[Mapping[str, Any]], column: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        key = str(row.get(column, ""))
        counts[key] = counts.get(key, 0) + 1
    return counts


def summarize_inputs() -> dict[str, Any]:
    final = read_json(DK_FINAL)
    gates = read_csv(DK_GATES)
    queue = read_csv(DK_QUEUE)
    memory = read_csv(DK_FAILURE_MEMORY)
    slices = read_csv(DK_SLICE_BLOCKERS)
    curve = read_csv(DK_CURVE_REVIEW)
    surface = read_csv(DK_SURFACE_REVIEW)
    blockers = read_csv(DJ_RELEASE_BLOCKERS)
    return {
        "final": final,
        "gates": gates,
        "queue": queue,
        "memory": memory,
        "slices": slices,
        "curve": curve,
        "surface": surface,
        "blockers": blockers,
        "failed_gates": [row for row in gates if row.get("status") != "passed"],
        "p0_queue_rows": sum(1 for row in queue if row.get("priority") == "P0"),
        "slice_status_counts": count_by(slices, "slice_review_status"),
        "release_blocker_count": len(blockers),
    }


def build_validation_edge_contract(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    final = summary["final"]
    baseline = rel(DK_CURVE_REVIEW)
    return [
        {
            "contract_id": "dl_validation_edge_train_only_minimax",
            "hypothesis": "train-block minimax objective can reduce broad validation weakness(학습 블록 미니맥스 목표가 넓은 검증 약점을 줄일 수 있음)",
            "decision_use": "choose what DM materializes, not choose a candidate(DM 물질화 대상을 고르되 후보를 선택하지 않음)",
            "comparison_baseline": baseline,
            "control_variables": "feature order, split boundary, no OOS winner use(피처 순서/분할 경계/OOS 승자 미사용)",
            "changed_variables": "objective contract only; penalize train sub-block collapse(목표 계약만 변경; 학습 하위 블록 붕괴 벌점)",
            "sample_scope": "US100 M5 Stage337 inherited split, review-only design(US100 M5 Stage337 상속 분할, 설계 검토 전용)",
            "success_criteria": "DM creates train-only validation-edge input frame and audit(DM이 학습 전용 검증 우위 입력 프레임과 감사를 생성)",
            "failure_criteria": f"repeats DK validation block rows={final.get('validation_pf_below_1p05_rows')}(DK 검증 차단 행 반복)",
            "invalid_conditions": "uses validation/OOS to tune threshold or pick pair(검증/OOS로 임계값 조정 또는 쌍 선택)",
            "stop_conditions": "if label boundary or split audit fails, stop before training(라벨 경계나 분할 감사 실패 시 학습 전 중단)",
            "evidence_plan": "validation_edge_input_frame.parquet; split_boundary_audit.csv; objective_contract_receipt.json",
            "forbidden_use": "no release, no MT5, no Forward claim(해제/MT5/전진 주장 금지)",
            "effect": "turns broad weak validation into a repair target(넓은 검증 약점을 수리 목표로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "dl_costed_label_margin_repair",
            "hypothesis": "costed label margin can separate tradable signal from raw direction(비용 반영 라벨 여백이 거래 가능 신호와 단순 방향을 분리)",
            "decision_use": "define label candidates for later guarded training(이후 방어 학습용 라벨 후보 정의)",
            "comparison_baseline": baseline,
            "control_variables": "bar-close feature boundary, fixed split, fixed no-lot policy(봉 마감 피처 경계/고정 분할/고정 무로트 정책)",
            "changed_variables": "label margin family and cost buffer diagnostics(라벨 여백 계열과 비용 버퍼 진단)",
            "sample_scope": "train materialization first; validation/OOS read-only audits(학습 물질화 우선, 검증/OOS 읽기 전용 감사)",
            "success_criteria": "DM produces label margin matrix with leakage audit(DM이 라벨 여백 행렬과 누수 감사를 생성)",
            "failure_criteria": "costed labels collapse trade density below usable review floor(비용 반영 라벨이 거래 밀도를 검토 불가 수준으로 붕괴)",
            "invalid_conditions": "feature uses future return or OOS pocket identity(피처가 미래 수익 또는 OOS 포켓 정체성을 사용)",
            "stop_conditions": "stop if shifted-return control wins(이동 수익률 대조가 이기면 중단)",
            "evidence_plan": "costed_label_margin_contract.csv; label_boundary_audit.csv; shifted_control_plan.csv",
            "forbidden_use": "no threshold fitting from validation/OOS(검증/OOS 임계값 맞춤 금지)",
            "effect": "keeps repair about signal tradeability, not OOS matching(수리를 OOS 맞춤이 아니라 신호 거래가능성으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "dl_validation_pocket_quarantine_reuse",
            "hypothesis": "known OOS-positive/validation-thin pockets should become quarantine labels(알려진 OOS 양호/검증 얇음 포켓은 격리 라벨이 되어야 함)",
            "decision_use": "prevent repeated surface mining in DM/next training(DM/다음 학습에서 표면 채굴 반복 방지)",
            "comparison_baseline": rel(DK_FAILURE_MEMORY),
            "control_variables": "OOS not used as reward; only as forbidden-memory tag(OOS는 보상이 아니라 금지 기억 태그로만 사용)",
            "changed_variables": "quarantine metadata and exclusion diagnostics(격리 메타데이터와 제외 진단)",
            "sample_scope": "DK failure memory plus DJ surface audit(DK 실패 기억과 DJ 표면 감사)",
            "success_criteria": "DM writes pocket_quarantine_matrix.csv with all 13 thin pockets(DM이 얇은 포켓 13개를 격리 행렬로 기록)",
            "failure_criteria": "any quarantined pocket becomes a preferred training target(격리 포켓이 선호 학습 목표가 됨)",
            "invalid_conditions": "uses OOS pocket as positive selector(OOS 포켓을 양의 선택자로 사용)",
            "stop_conditions": "stop if quarantine coverage is below DK count(격리 커버리지가 DK 집계보다 작으면 중단)",
            "evidence_plan": "pocket_quarantine_matrix.csv; forbidden_selection_audit.csv",
            "forbidden_use": "no cherry-pick after quarantine(격리 후 골라잡기 금지)",
            "effect": "converts tempting OOS pockets into failure memory(유혹적인 OOS 포켓을 실패 기억으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "dl_trade_density_floor_without_lot_tuning",
            "hypothesis": "trade density can be raised by objective design without lot optimization(로트 최적화 없이 목표 설계로 거래 밀도를 높일 수 있음)",
            "decision_use": "prepare aggressive branch inputs without selecting candidate(후보 선택 없이 공격 가지 입력 준비)",
            "comparison_baseline": rel(DK_SLICE_BLOCKERS),
            "control_variables": "fixed lot assumption, no lot search, no threshold search(고정 로트 가정/로트 탐색 없음/임계값 탐색 없음)",
            "changed_variables": "density regularizer and sample-floor diagnostics(밀도 정규화와 표본 하한 진단)",
            "sample_scope": "slice status matrix from DK(DK 슬라이스 상태 행렬)",
            "success_criteria": "DM creates density_floor_contract.csv and thin-slice exclusion audit(DM이 밀도 하한 계약과 얇은 슬라이스 제외 감사를 생성)",
            "failure_criteria": "density gain comes only from thin or concentrated slices(밀도 증가가 얇거나 집중된 슬라이스에서만 발생)",
            "invalid_conditions": "lot or threshold is optimized(로트 또는 임계값이 최적화됨)",
            "stop_conditions": "stop if density conflicts with no-overfit controls(밀도가 무과적합 대조와 충돌하면 중단)",
            "evidence_plan": "density_floor_contract.csv; thin_slice_exclusion_audit.csv",
            "forbidden_use": "do not claim profit from density design(밀도 설계로 수익 주장 금지)",
            "effect": "keeps offensive work controlled(공격 작업을 통제된 상태로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_surface_contract(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    final = summary["final"]
    return [
        {
            "contract_id": "dl_surface_axis_cost_policy",
            "surface_axis": "cost_policy_id(비용 정책 ID)",
            "observed_blocker": f"surface_watch_rows={final.get('surface_watch_rows')};max_gap={final.get('max_surface_gap')}",
            "design_response": "require cost ladder stability before candidate review(후보 검토 전 비용 사다리 안정성 요구)",
            "required_stability_check": "extra0/extra2/extra5 rank agreement and PF gap audit(extra0/extra2/extra5 순위 일치와 PF 차이 감사)",
            "success_criteria": "DM writes cost_ladder_deconcentration_matrix.csv",
            "failure_criteria": "only one cost rung carries OOS edge(한 비용 단계만 OOS 우위를 가짐)",
            "forbidden_use": "do not select cheapest/strongest cost rung alone(가장 싸거나 강한 비용 단계만 선택 금지)",
            "evidence_output": "cost_ladder_deconcentration_matrix.csv",
            "effect": "turns cost surface into a stability gate(비용 표면을 안정성 게이트로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "dl_surface_axis_model_family",
            "surface_axis": "model_config_id(모델 설정 ID)",
            "observed_blocker": "OOS edge concentrated by model family(모델 계열별 OOS 우위 집중)",
            "design_response": "require model-family breadth and negative-control gap(모델 계열 폭과 부정대조 격차 요구)",
            "required_stability_check": "logreg/extratrees/lgbm-style family comparison where available(가능한 모델 계열 비교)",
            "success_criteria": "DM writes model_family_surface_matrix.csv",
            "failure_criteria": "one model family explains all positive OOS pockets(한 모델 계열이 모든 양의 OOS 포켓을 설명)",
            "forbidden_use": "do not promote model family from isolated OOS(고립 OOS로 모델 계열 승격 금지)",
            "evidence_output": "model_family_surface_matrix.csv",
            "effect": "reduces model-family overfit path(모델 계열 과적합 경로 감소)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "dl_surface_axis_feature_set",
            "surface_axis": "feature_set_id(피처 묶음 ID)",
            "observed_blocker": "surface watch tied to feature context(표면 감시가 피처 문맥에 묶임)",
            "design_response": "require feature ablation and lag-safe membership audit(피처 제거와 지연 안전 구성 감사 요구)",
            "required_stability_check": "feature family leave-one-group-out surface(피처 계열 그룹 단위 제거 표면)",
            "success_criteria": "DM writes feature_family_deconcentration_matrix.csv",
            "failure_criteria": "one feature group creates most OOS-only edge(한 피처 그룹이 대부분의 OOS 전용 우위 생성)",
            "forbidden_use": "do not use post-hoc feature winner as candidate(사후 피처 승자를 후보로 사용 금지)",
            "evidence_output": "feature_family_deconcentration_matrix.csv",
            "effect": "tests whether feature context is robust or pocketed(피처 문맥이 강건한지 포켓인지 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "dl_surface_axis_slice_concentration",
            "surface_axis": "slice_axis/slice_value(슬라이스 축/값)",
            "observed_blocker": f"thin_slices={final.get('thin_slice_rows')};slice_blocks={final.get('slice_block_rows')}",
            "design_response": "exclude thin slices from release evidence; keep as diagnostics(얇은 슬라이스를 해제 근거에서 제외하고 진단으로 유지)",
            "required_stability_check": "session/hour/month/volatility/ADX/VIX/USD/rate slice breadth(세션/시간/월/변동성/ADX/VIX/USD/금리 슬라이스 폭)",
            "success_criteria": "DM writes slice_breadth_guard_matrix.csv",
            "failure_criteria": "positive edge lives in thin slice only(양의 우위가 얇은 슬라이스에만 존재)",
            "forbidden_use": "do not pick slice winners(슬라이스 승자 선택 금지)",
            "evidence_output": "slice_breadth_guard_matrix.csv",
            "effect": "separates diagnostics from selection(진단과 선택을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_balanced_queue() -> list[dict[str, str]]:
    return [
        {
            "design_id": "dl_defensive_validation_edge_floor",
            "lane": "defensive(방어)",
            "priority": "P0",
            "task": "build train-only validation-edge floor inputs(학습 전용 검증 우위 하한 입력 생성)",
            "changed_variables": "objective and label contract(목표와 라벨 계약)",
            "fixed_variables": "no OOS selection, no threshold tuning, no lot optimization(OOS 선택/임계값 튜닝/로트 최적화 없음)",
            "required_inputs": f"{rel(VALIDATION_EDGE_CONTRACT)};{rel(DK_FAILURE_MEMORY)}",
            "required_outputs": "validation_edge_input_frame.parquet;label_boundary_audit.csv",
            "success_criteria": "inputs are complete and leakage audit passes(입력이 완전하고 누수 감사 통과)",
            "failure_criteria": "cannot create train-only target without leakage(누수 없이 학습 전용 목표 생성 불가)",
            "invalid_conditions": "uses validation/OOS target to tune(검증/OOS 목표로 튜닝)",
            "effect": "repairs broad validation weakness first(넓은 검증 약점을 먼저 수리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "dl_aggressive_trade_density_shape",
            "lane": "aggressive(공격)",
            "priority": "P0",
            "task": "prepare trade-density and payoff-shape expansion inputs(거래 밀도와 보상 형태 확장 입력 준비)",
            "changed_variables": "density regularizer, payoff rank diagnostics(밀도 정규화/보상 순위 진단)",
            "fixed_variables": "fixed lot, no validation threshold search(고정 로트/검증 임계값 탐색 없음)",
            "required_inputs": f"{rel(DK_SLICE_BLOCKERS)};{rel(DK_CURVE_REVIEW)}",
            "required_outputs": "density_floor_contract.csv;payoff_shape_expansion_matrix.csv",
            "success_criteria": "aggressive branch has enough non-thin rows for later training(공격 가지가 이후 학습에 충분한 비얇은 행 확보)",
            "failure_criteria": "trade growth depends on thin slices only(거래 증가가 얇은 슬라이스에만 의존)",
            "invalid_conditions": "post-hoc OOS pocket becomes target(사후 OOS 포켓이 목표가 됨)",
            "effect": "keeps profit ambition alive without overfit shortcut(과적합 지름길 없이 수익 야심 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "dl_repair_surface_deconcentration",
            "lane": "repair(수리)",
            "priority": "P0",
            "task": "materialize surface deconcentration matrices(표면 탈집중 행렬 물질화)",
            "changed_variables": "surface audit granularity(표면 감사 세분도)",
            "fixed_variables": "cost/model/feature surfaces not selected as winners(비용/모델/피처 표면을 승자로 선택하지 않음)",
            "required_inputs": f"{rel(SURFACE_DECONTRACT)};{rel(DJ_SURFACE_AUDIT)}",
            "required_outputs": "surface_deconcentration_input_bundle.json",
            "success_criteria": "all cost/model/feature axes have stability matrices(모든 비용/모델/피처 축 안정성 행렬 존재)",
            "failure_criteria": "surface axis missing or isolated(표면 축 누락 또는 고립)",
            "invalid_conditions": "deconcentration is used to pick OOS winner(탈집중을 OOS 승자 선택에 사용)",
            "effect": "blocks repeated surface mining(반복 표면 채굴 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "dl_control_negative_and_purged",
            "lane": "control(대조)",
            "priority": "P0",
            "task": "define shifted/noise/purged controls before any training(학습 전 이동/잡음/제거 대조 정의)",
            "changed_variables": "control audit coverage(대조 감사 범위)",
            "fixed_variables": "chronological split and no-lookahead rule(시간순 분할과 미래참조 금지)",
            "required_inputs": rel(NO_OVERFIT_GUARDRAILS),
            "required_outputs": "negative_control_contract.csv;purged_split_contract.csv",
            "success_criteria": "DM writes controls that block training release if controls win(DM이 대조 승리 시 학습 해제를 막는 대조 생성)",
            "failure_criteria": "controls cannot be aligned to input frame(대조를 입력 프레임에 정렬할 수 없음)",
            "invalid_conditions": "control labels leak future state(대조 라벨이 미래 상태 누수)",
            "effect": "prevents lookahead recurrence(미래참조 재발 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "dl_runtime_proxy_firewall",
            "lane": "firewall(방화벽)",
            "priority": "P1",
            "task": "preserve proxy/MT5 comparison as future evidence, not current claim(proxy/MT5 비교를 미래 근거로 보존하고 현재 주장으로 쓰지 않음)",
            "changed_variables": "future evidence checklist only(미래 근거 체크리스트만 변경)",
            "fixed_variables": "no MT5 probe in DL/DM(DL/DM에서 MT5 탐침 없음)",
            "required_inputs": rel(RUNTIME_FIREWALL),
            "required_outputs": "future_proxy_mt5_evidence_checklist.csv",
            "success_criteria": "future runtime gate has explicit required proxy and MT5 fields(미래 런타임 게이트에 명시적 proxy/MT5 필드 존재)",
            "failure_criteria": "runtime claim appears without tester output(테스터 출력 없이 런타임 주장 등장)",
            "invalid_conditions": "Forward or operating language is written(전진 또는 운영 표현 작성)",
            "effect": "keeps runtime authority closed while preserving path forward(런타임 권위를 닫고 다음 경로 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_runtime_firewall() -> list[dict[str, str]]:
    return [
        {
            "firewall_id": "dl_no_candidate_selection",
            "held_action": "candidate_selection(후보 선택)",
            "held_until": "post-DM materialized inputs and later guarded training review(DM 입력 물질화와 이후 방어 학습 검토 후)",
            "required_evidence": "validation-edge input, surface deconcentration, negative controls(검증 우위 입력/표면 탈집중/부정대조)",
            "forbidden_claim": "promotion candidate, release, selected ONNX(승격 후보/해제/선택 ONNX)",
            "effect": "prevents design from becoming selection(설계가 선택으로 변하는 것을 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "dl_no_mt5_probe",
            "held_action": "MT5 probe(MT5 탐침)",
            "held_until": "a later candidate passes validation, control, cost, surface gates(이후 후보가 검증/대조/비용/표면 게이트 통과)",
            "required_evidence": "ONNX parity and proxy scorecard after training(학습 후 ONNX 동등성과 프록시 점수표)",
            "forbidden_claim": "runtime probe or runtime authority(런타임 탐침 또는 런타임 권위)",
            "effect": "keeps external verification staged correctly(외부 검증 순서를 맞게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "dl_no_forward_decision",
            "held_action": "Forward Passed/Forward Failed(전진 통과/전진 실패)",
            "held_until": "actual forward/MT5 evidence exists(실제 전진/MT5 근거 존재)",
            "required_evidence": "broker data, tester report, attribution reports(브로커 데이터/테스터 보고서/귀속 보고서)",
            "forbidden_claim": "Goal Achieve, live readiness, deployment(목표 달성/실거래 준비/배포)",
            "effect": "keeps research boundary honest(연구 경계를 정직하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_guardrails() -> list[dict[str, str]]:
    return [
        {
            "guardrail_id": "dl_no_lookahead_feature_boundary",
            "risk": "lookahead leakage(미래참조 누수)",
            "required_control": "bar-close feature/label boundary audit(봉 마감 피처/라벨 경계 감사)",
            "blocks_if": "future return appears in feature columns(미래 수익이 피처 열에 등장)",
            "evidence_output": "label_boundary_audit.csv",
            "effect": "prevents previous lookahead issue from recurring(이전 미래참조 문제 재발 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "dl_no_validation_oos_retune",
            "risk": "overfit through validation/OOS retune(검증/OOS 재튜닝 과적합)",
            "required_control": "train-only materialization and read-only validation/OOS audit(학습 전용 물질화와 검증/OOS 읽기 전용 감사)",
            "blocks_if": "threshold, pair, lot, or surface chosen from validation/OOS(임계값/쌍/로트/표면이 검증/OOS에서 선택)",
            "evidence_output": "forbidden_selection_audit.csv",
            "effect": "keeps repair from becoming another overfit(수리가 또 다른 과적합이 되는 것을 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "dl_negative_control_floor",
            "risk": "spurious separability(가짜 분리력)",
            "required_control": "shifted return, noise label, and block-shuffle controls(이동 수익률/잡음 라벨/블록 셔플 대조)",
            "blocks_if": "control beats or matches candidate signal(대조가 후보 신호를 이기거나 맞먹음)",
            "evidence_output": "negative_control_contract.csv",
            "effect": "requires signal to beat easy fake baselines(신호가 쉬운 가짜 기준선을 이기도록 요구)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "dl_surface_deconcentration_floor",
            "risk": "surface mining(표면 채굴)",
            "required_control": "cost/model/feature/slice breadth matrices(비용/모델/피처/슬라이스 폭 행렬)",
            "blocks_if": "edge is isolated to one surface pocket(우위가 한 표면 포켓에 고립)",
            "evidence_output": "surface_deconcentration_input_bundle.json",
            "effect": "forces broadness evidence before selection(선택 전 폭 근거를 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_dm_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DM_materialize_validation_edge_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize validation-edge repair input frame(검증 우위 수리 입력 프레임 물질화)",
            "required_inputs": rel(VALIDATION_EDGE_CONTRACT),
            "required_outputs": "validation_edge_input_frame.parquet;validation_edge_audit.csv",
            "blocked_if_missing": "validation-edge contract(검증 우위 계약)",
            "forbidden_action": "no training, no threshold tuning(학습/임계값 튜닝 금지)",
            "effect": "turns design into measurable inputs(설계를 측정 가능한 입력으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DM_materialize_surface_deconcentration",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize cost/model/feature/slice surface matrices(비용/모델/피처/슬라이스 표면 행렬 물질화)",
            "required_inputs": rel(SURFACE_DECONTRACT),
            "required_outputs": "surface_deconcentration_input_bundle.json",
            "blocked_if_missing": "surface deconcentration contract(표면 탈집중 계약)",
            "forbidden_action": "no cherry-pick selection(골라잡기 선택 금지)",
            "effect": "makes surface blocker testable(표면 차단을 시험 가능하게 만듦)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DM_materialize_balanced_attack_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize defensive/aggressive/repair/control branches(방어/공격/수리/대조 가지 물질화)",
            "required_inputs": rel(BALANCED_QUEUE),
            "required_outputs": "balanced_repair_attack_input_manifest.json",
            "blocked_if_missing": "balanced queue(균형 대기열)",
            "forbidden_action": "no candidate ranking by OOS(OOS 후보 순위화 금지)",
            "effect": "keeps strong-profit ambition and no-overfit discipline together(강한 수익 목표와 무과적합 규율을 함께 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DM_materialize_no_overfit_controls",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize negative-control and leakage guard inputs(부정대조와 누수 방지 입력 물질화)",
            "required_inputs": rel(NO_OVERFIT_GUARDRAILS),
            "required_outputs": "negative_control_contract.csv;label_boundary_audit.csv",
            "blocked_if_missing": "guardrail matrix(가드레일 행렬)",
            "forbidden_action": "no skip of controls(대조 생략 금지)",
            "effect": "prevents lookahead and fake signal from re-entering(미래참조와 가짜 신호 재진입 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DM_preserve_runtime_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "carry no-MT5/no-release firewall into DM(DM으로 무MT5/무해제 방화벽 전달)",
            "required_inputs": rel(RUNTIME_FIREWALL),
            "required_outputs": "runtime_firewall_carryforward.csv",
            "blocked_if_missing": "runtime firewall contract(런타임 방화벽 계약)",
            "forbidden_action": "no MT5 probe, no Forward claim(MT5 탐침/전진 주장 금지)",
            "effect": "keeps runtime authority closed(런타임 권위 닫힘 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DK inputs exist(필수 DK 입력 존재)"),
        ("parent_dk_gates_passed", final["dk_failed_gate_rows"] == 0, str(final["dk_failed_gate_rows"]), "0", "DK review usable(DK 검토 사용 가능)"),
        ("parent_next_action_matches", final["dk_next_action"] == RUN_ID, str(final["dk_next_action"]), RUN_ID, "continues DK queue(DK 대기열을 이어감)"),
        ("validation_contract_materialized", final["validation_contract_rows"] >= 4, str(final["validation_contract_rows"]), ">=4", "validation repair contracts exist(검증 수리 계약 존재)"),
        ("surface_contract_materialized", final["surface_contract_rows"] >= 4, str(final["surface_contract_rows"]), ">=4", "surface contracts exist(표면 계약 존재)"),
        ("balanced_lanes_present", final["balanced_lane_count"] >= 5, str(final["balanced_lane_count"]), ">=5", "defensive/aggressive/repair/control/firewall lanes exist(방어/공격/수리/대조/방화벽 존재)"),
        ("runtime_firewall_materialized", final["runtime_firewall_rows"] >= 3, str(final["runtime_firewall_rows"]), ">=3", "runtime firewall exists(런타임 방화벽 존재)"),
        ("guardrails_materialized", final["guardrail_rows"] >= 4, str(final["guardrail_rows"]), ">=4", "no-overfit guardrails exist(무과적합 가드레일 존재)"),
        ("dm_queue_materialized", final["dm_queue_rows"] >= 5, str(final["dm_queue_rows"]), ">=5", "DM materialization queue exists(DM 물질화 대기열 존재)"),
        (
            "no_forbidden_execution",
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
        "hypothesis": "validation-edge and surface-deconcentration repair can reduce overfit risk before any new training(새 학습 전 검증 우위와 표면 탈집중 수리가 과적합 위험을 낮출 수 있음)",
        "decision_use": "open DM materialization, not select model(DM 물질화를 열며 모델 선택은 아님)",
        "comparison_baseline": rel(DK_FINAL),
        "control_variables": "no threshold tuning, no lot optimization, no OOS selection, no MT5(임계값 튜닝/로트 최적화/OOS 선택/MT5 없음)",
        "changed_variables": "design contracts for objective, label, surface, controls(목표/라벨/표면/대조 설계 계약)",
        "sample_scope": "Stage337 US100 M5 inherited artifacts, design-only(Stage337 US100 M5 상속 산출물, 설계 전용)",
        "success_criteria": "DM can materialize complete repair inputs with gates(DM이 완전한 수리 입력과 게이트를 물질화)",
        "failure_criteria": "inputs require OOS retune or leak future state(입력이 OOS 재튜닝 또는 미래 상태 누수를 요구)",
        "invalid_conditions": "design claims release or candidate selection(설계가 해제 또는 후보 선택을 주장)",
        "stop_conditions": "stop before training if any guardrail fails(가드레일 실패 시 학습 전 중단)",
        "evidence_plan": [rel(path) for path in [VALIDATION_EDGE_CONTRACT, SURFACE_DECONTRACT, NO_OVERFIT_GUARDRAILS, DM_QUEUE]],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherits DK/DJ replay artifacts; no new bars read(DK/DJ 리플레이 산출물 상속, 새 봉 읽지 않음)",
        "sample_scope": "design-only on frozen review outputs(고정 검토 산출물 설계 전용)",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']}",
        "feature_label_boundary": "future DM must audit bar-close feature/label boundary(미래 DM은 봉 마감 피처/라벨 경계 감사 필요)",
        "split_boundary": "chronological split inherited, validation/OOS read-only(시간순 분할 상속, 검증/OOS 읽기 전용)",
        "leakage_risk": "turning OOS pocket into design target(OOS 포켓을 설계 목표로 바꿈)",
        "data_hash_or_identity": {"dk_final": sha256_file(DK_FINAL), "dk_failure_memory": sha256_file(DK_FAILURE_MEMORY)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "no model trained; design for later guarded ONNX research(모델 학습 없음; 이후 방어 ONNX 연구 설계)",
        "target_and_label": "costed validation-edge label and objective contracts only(비용 반영 검증 우위 라벨/목표 계약만)",
        "split_method": "inherited chronological split with future train-only materialization(상속 시간순 분할과 미래 학습 전용 물질화)",
        "selection_metric": "none(없음)",
        "secondary_metrics": "surface breadth, negative controls, density floor(표면 폭/부정대조/밀도 하한)",
        "threshold_policy": "unchanged; no threshold tuning(변경 없음; 임계값 튜닝 없음)",
        "overfit_risk": "validation/OOS retune and surface mining(검증/OOS 재튜닝과 표면 채굴)",
        "calibration_risk": "not applicable until training(학습 전 해당 없음)",
        "comparison_baseline": rel(DK_CURVE_REVIEW),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"design contracts={final['validation_contract_rows'] + final['surface_contract_rows']};dm_queue={final['dm_queue_rows']}",
        "comparison_baseline": rel(DK_FINAL),
        "likely_drivers": "broad validation weakness and surface isolation(넓은 검증 약점과 표면 고립)",
        "segment_checks": "planned, not executed: session/hour/month/vol/ADX/VIX/USD/rate(계획됨, 미실행: 세션/시간/월/변동성/ADX/VIX/USD/금리)",
        "trade_shape": "not measured in DL design(DL 설계에서는 측정하지 않음)",
        "alternative_explanations": "label mismatch, target underfit, cost model mismatch(라벨 불일치/목표 과소적합/비용 모델 불일치)",
        "attribution_confidence": "high_for_design_coverage_low_for_future_profit(설계 커버리지는 높음, 미래 수익은 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "DK gates, failure memory, design contracts(DK 게이트/실패 기억/설계 계약)",
        "evidence_missing": "DM materialized inputs, training, ONNX parity, MT5(미래 DM 입력/학습/ONNX 동등성/MT5)",
        "judgment_label": "design_ready",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "이번 단계는 고르는 단계가 아니라, 다음 입력을 안전하게 만들기 위한 설계 고정입니다.",
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
    text = f"""# Stage337 run337DL Prediction Surface Validation-Edge Repair Design(예측 표면 검증 우위 수리 설계)

## Conclusion(결론)

run337DL(337DL 실행)은 DK review(DK 검토)의 차단 원인을 repair design(수리 설계)으로 바꿨다. 이 단계는 training(학습), selection(선택), MT5 probe(MT5 탐침)가 아니다.

핵심 설계는 네 가지다. validation-edge repair(검증 우위 수리), surface deconcentration(표면 탈집중), defensive/aggressive/repair/control balance(방어/공격/수리/대조 균형), runtime firewall(런타임 방화벽)이다.

Effect(효과): 다음 run337DM(337DM 실행)은 이 설계를 실제 입력 프레임과 감사 파일로 물질화한다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- validation_contract_rows(검증 계약 행): `{final["validation_contract_rows"]}`
- surface_contract_rows(표면 계약 행): `{final["surface_contract_rows"]}`
- balanced_design_rows(균형 설계 행): `{final["balanced_design_rows"]}`
- guardrail_rows(가드레일 행): `{final["guardrail_rows"]}`
- dm_queue_rows(DM 대기열 행): `{final["dm_queue_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DL

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): DK 차단 원인을 DM 물질화용 계약으로 바꾸고, runtime/Forward(런타임/전진) 주장은 닫아둔다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(VALIDATION_EDGE_CONTRACT)}`, `{rel(SURFACE_DECONTRACT)}`
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
        f"  Stage337 run337DL focus complete: prediction surface validation-edge repair design(예측 표면 검증 우위 수리 설계)을 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DM(337DM 실행)에서 validation-edge/surface/control inputs(검증 우위/표면/대조 입력)을 물질화한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DL focus complete")
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
## Stage337 run337DL(337DL 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): validation-edge/surface/control repair(검증 우위/표면/대조 수리)를 DM 물질화로 넘긴다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DK(337DK"
    if "## Stage337 run337DL(337DL 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_dl_design_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 prediction surface validation-edge repair input materialization(예측 표면 검증 우위 수리 입력 물질화)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DL(337DL 실행) designed prediction surface validation-edge repair(예측 표면 검증 우위 수리 설계). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DL(337DL 실행) designed prediction surface"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DL designed prediction surface validation-edge repair(예측 표면 검증 우위 수리 설계) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DL designed prediction surface"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "prediction_surface_validation_edge_repair_design_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"validation_contracts={final['validation_contract_rows']};surface_contracts={final['surface_contract_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design_model_validation_performance_attribution_result_judgment",
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
        "kpi_scope": "validation_edge_surface_deconcentration_design",
        "scoreboard_lane": "experiment_design_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"dm_queue={final['dm_queue_rows']};guardrails={final['guardrail_rows']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_model_validation_performance_attribution_result_judgment",
        "evidence_scope": "DK blockers converted to DM contracts",
        "kpi_scope": "design_coverage_no_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_design",
        "family": "experiment_design_model_validation_performance_attribution_result_judgment",
        "question": "how should validation-edge and surface-isolation blockers be repaired without OOS retune",
        "metric_scope": "contract_coverage_guardrails_runtime_firewall",
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
    summary = summarize_inputs()
    validation_rows = build_validation_edge_contract(summary)
    surface_rows = build_surface_contract(summary)
    balanced_rows = build_balanced_queue()
    firewall_rows = build_runtime_firewall()
    guardrail_rows = build_guardrails()
    dm_queue_rows = build_dm_queue()
    artifacts: list[Path] = [
        write_csv(VALIDATION_EDGE_CONTRACT, VALIDATION_COLUMNS, validation_rows),
        write_csv(SURFACE_DECONTRACT, SURFACE_COLUMNS, surface_rows),
        write_csv(BALANCED_QUEUE, BALANCED_COLUMNS, balanced_rows),
        write_csv(RUNTIME_FIREWALL, FIREWALL_COLUMNS, firewall_rows),
        write_csv(NO_OVERFIT_GUARDRAILS, GUARDRAIL_COLUMNS, guardrail_rows),
        write_csv(DM_QUEUE, QUEUE_COLUMNS, dm_queue_rows),
    ]
    lane_count = len({row["lane"].split("(")[0] for row in balanced_rows})
    dk_final: Mapping[str, Any] = summary["final"]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dk_next_action": dk_final.get("next_action", ""),
        "dk_failed_gate_rows": len(summary["failed_gates"]),
        "missing_inputs": len(missing),
        "dk_validation_pf_below_1p05_rows": dk_final.get("validation_pf_below_1p05_rows", 0),
        "dk_surface_watch_rows": dk_final.get("surface_watch_rows", 0),
        "dk_slice_block_rows": dk_final.get("slice_block_rows", 0),
        "dk_thin_slice_rows": dk_final.get("thin_slice_rows", 0),
        "validation_contract_rows": len(validation_rows),
        "surface_contract_rows": len(surface_rows),
        "balanced_design_rows": len(balanced_rows),
        "balanced_lane_count": lane_count,
        "runtime_firewall_rows": len(firewall_rows),
        "guardrail_rows": len(guardrail_rows),
        "dm_queue_rows": len(dm_queue_rows),
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
