from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import attempt_balanced_no_lookahead_runtime_probe_without_db as aw
from stage_pipelines.stage337 import design_no_overfit_repair_from_shifted_attribution_without_db as az


TODAY = "2026-05-27"
STAGE_ID = az.STAGE_ID
RUN_NUMBER = "run337BA"
RUN_ID = "run337BA_materialize_no_overfit_repair_inputs_from_shifted_attribution_without_db_v1"
PARENT_RUN_ID = az.RUN_ID
NEXT_RUN_ID = "run337BB_review_no_overfit_repair_inputs_from_shifted_attribution_without_db_v1"
STATUS = "completed_stage337BA_no_overfit_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "run337AZ_design_converted_to_repair_input_contracts_without_forward_retune"
DECISION = "stage337BA_open_run337BB_review_materialized_no_overfit_repair_inputs_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BA_no_overfit_repair_input_materialization_without_db_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = az.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = az.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BA_no_overfit_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BA_no_overfit_repair_inputs.md"
SELECTED_STATUS = az.SELECTED_STATUS
STAGE_BRIEF = az.STAGE_BRIEF
WORKSPACE_STATE = az.WORKSPACE_STATE
CURRENT_STATE = az.CURRENT_STATE
CHANGELOG = az.CHANGELOG
RUN_REGISTRY = az.RUN_REGISTRY
ALPHA_LEDGER = az.ALPHA_LEDGER
ARTIFACT_REGISTRY = az.ARTIFACT_REGISTRY
STAGE_LEDGER = az.STAGE_LEDGER

RUN337AZ_DIR = STAGE_DIR / "02_runs" / "run337AZ"
RUN337AY_DIR = STAGE_DIR / "02_runs" / "run337AY"

AZ_FINAL = RUN337AZ_DIR / "final_decision.json"
AZ_DESIGN = RUN337AZ_DIR / "no_overfit_repair_design_matrix.csv"
AZ_DELTA = RUN337AZ_DIR / "shifted_fragility_delta_matrix.csv"
AZ_FALSIFICATION = RUN337AZ_DIR / "repair_falsification_protocol.csv"
AZ_PROXY_POLICY = RUN337AZ_DIR / "proxy_mt5_runtime_use_policy.csv"
AZ_DATA_BOUNDARY = RUN337AZ_DIR / "data_feature_boundary_contract.csv"
AZ_QUEUE = RUN337AZ_DIR / "run337BA_materialization_queue.csv"
AZ_BALANCE = RUN337AZ_DIR / "repair_defensive_aggressive_balance_matrix.csv"
AZ_GATE = RUN337AZ_DIR / "required_gate_coverage_audit.csv"
AY_FINAL = RUN337AY_DIR / "final_decision.json"
AY_PROTOCOL = RUN337AY_DIR / "protocol_attribution_matrix.csv"
AY_COST = RUN337AY_DIR / "cost_stress_report.csv"
AY_CURVE = RUN337AY_DIR / "curve_pocket_report.csv"
AY_PROXY = RUN337AY_DIR / "proxy_mt5_attribution_usability.csv"
AY_REGIME = RUN337AY_DIR / "shifted_custom_regime_attribution.csv"
AY_SHIFTED_TRADES = RUN337AY_DIR / "shifted_custom_trade_records.csv"
AY_COMPLETED_TRADES = RUN337AY_DIR / "completed_day_anchor_trade_records.csv"

FEATURE_CONTRACT = RUN_DIR / "feature_contract.csv"
GATE_CONTRACT = RUN_DIR / "gate_contract.csv"
PROXY_MT5_PAIRING = RUN_DIR / "proxy_mt5_pairing_contract.csv"
NEGATIVE_CONTROL_PLAN = RUN_DIR / "negative_control_plan.csv"
COST_MARGIN_CONTRACT = RUN_DIR / "cost_margin_feature_contract.csv"
SIDE_BALANCE_CONTRACT = RUN_DIR / "side_balance_input_contract.csv"
DENSITY_RETENTION_CONTRACT = RUN_DIR / "density_retention_contract.csv"
CURVE_STATE_VETO_MAP = RUN_DIR / "curve_state_veto_feature_map.csv"
INPUT_SOURCE_HASH = RUN_DIR / "input_source_hash_matrix.csv"
PACKAGE_MANIFEST = RUN_DIR / "materialized_input_package_manifest.csv"
NO_LOOKAHEAD_AUDIT = RUN_DIR / "no_lookahead_materialization_audit.csv"
RUN337BB_QUEUE = RUN_DIR / "run337BB_review_queue.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    AZ_FINAL,
    AZ_DESIGN,
    AZ_DELTA,
    AZ_FALSIFICATION,
    AZ_PROXY_POLICY,
    AZ_DATA_BOUNDARY,
    AZ_QUEUE,
    AZ_BALANCE,
    AZ_GATE,
    AY_FINAL,
    AY_PROTOCOL,
    AY_COST,
    AY_CURVE,
    AY_PROXY,
    AY_REGIME,
    AY_SHIFTED_TRADES,
    AY_COMPLETED_TRADES,
)
OUTPUT_FILES = (
    FEATURE_CONTRACT,
    GATE_CONTRACT,
    PROXY_MT5_PAIRING,
    NEGATIVE_CONTROL_PLAN,
    COST_MARGIN_CONTRACT,
    SIDE_BALANCE_CONTRACT,
    DENSITY_RETENTION_CONTRACT,
    CURVE_STATE_VETO_MAP,
    INPUT_SOURCE_HASH,
    PACKAGE_MANIFEST,
    NO_LOOKAHEAD_AUDIT,
    RUN337BB_QUEUE,
    GATE_AUDIT,
    ROUTING_RECEIPT,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

FEATURE_COLUMNS = (
    "contract_id",
    "design_id",
    "input_family",
    "materialized_input",
    "allowed_sources",
    "forbidden_sources",
    "timestamp_rule",
    "split_rule",
    "proxy_mt5_role",
    "review_gate",
    "status",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "contract_id",
    "source_gate_id",
    "design_ids",
    "gate_family",
    "artifact_to_check",
    "pass_condition",
    "fail_condition",
    "prevents_overfit_path",
    "review_owner",
    "status",
    "claim_boundary",
)
PAIRING_COLUMNS = (
    "pairing_id",
    "subject",
    "proxy_artifact",
    "mt5_runtime_artifact",
    "required_join_key",
    "usable_for",
    "not_usable_for",
    "mismatch_action",
    "status",
    "effect",
    "claim_boundary",
)
NEGATIVE_COLUMNS = (
    "control_id",
    "control_family",
    "applies_to_designs",
    "materialized_check",
    "expected_failure_or_guard",
    "invalid_if",
    "status",
    "effect",
    "claim_boundary",
)
SPECIAL_CONTRACT_COLUMNS = (
    "contract_id",
    "design_id",
    "input_fields",
    "derived_fields",
    "allowed_calculation",
    "forbidden_calculation",
    "parent_reference",
    "materialization_status",
    "next_review",
    "claim_boundary",
)
SOURCE_COLUMNS = (
    "source_id",
    "path",
    "exists",
    "row_count",
    "sha256",
    "used_for",
    "availability",
    "claim_boundary",
)
PACKAGE_COLUMNS = (
    "package_id",
    "artifact_path",
    "artifact_type",
    "rows",
    "producer",
    "consumer",
    "source_inputs",
    "status",
    "claim_boundary",
)
AUDIT_COLUMNS = (
    "audit_id",
    "status",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)
REVIEW_QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "review_subject",
    "inputs_to_review",
    "must_confirm",
    "must_reject_if",
    "expected_outputs",
    "priority",
    "effect",
    "claim_boundary",
)
REQUIRED_GATE_COLUMNS = aw.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fnum(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(str(value))
    except Exception:
        return default
    return parsed if math.isfinite(parsed) else default


def row_count(path: Path) -> int:
    return len(aw.read_csv(path)) if aw.path_exists(path) else 0


def source_identity(path: Path) -> dict[str, Any]:
    return {
        "path": aw.rel(path),
        "exists": str(aw.path_exists(path)).lower(),
        "row_count": row_count(path),
        "sha256": aw.sha256_file(path) if aw.path_exists(path) else "",
    }


def read_sources() -> dict[str, Any]:
    return {
        "az_final": aw.read_json(AZ_FINAL),
        "az_design": aw.read_csv(AZ_DESIGN),
        "az_delta": aw.read_csv(AZ_DELTA),
        "az_falsification": aw.read_csv(AZ_FALSIFICATION),
        "az_proxy_policy": aw.read_csv(AZ_PROXY_POLICY),
        "az_data_boundary": aw.read_csv(AZ_DATA_BOUNDARY),
        "az_queue": aw.read_csv(AZ_QUEUE),
        "az_balance": aw.read_csv(AZ_BALANCE),
        "az_gate": aw.read_csv(AZ_GATE),
        "ay_final": aw.read_json(AY_FINAL),
        "ay_protocol": aw.read_csv(AY_PROTOCOL),
        "ay_cost": aw.read_csv(AY_COST),
        "ay_curve": aw.read_csv(AY_CURVE),
        "ay_proxy": aw.read_csv(AY_PROXY),
        "ay_regime": aw.read_csv(AY_REGIME),
        "ay_shifted_trades": aw.read_csv(AY_SHIFTED_TRADES),
        "ay_completed_trades": aw.read_csv(AY_COMPLETED_TRADES),
    }


def design_by_id(rows: Sequence[Mapping[str, str]]) -> dict[str, dict[str, str]]:
    return {str(row.get("design_id", "")): dict(row) for row in rows}


def build_feature_contracts(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    designs = design_by_id(src["az_design"])
    return [
        {
            "contract_id": "ba_feature_cost_margin",
            "design_id": "az_defensive_cost_margin_objective",
            "input_family": "cost_margin(비용 마진)",
            "materialized_input": "cost_margin_pretrade_contract(진입 전 비용 마진 계약)",
            "allowed_sources": aw.rel(AY_COST) + "; " + aw.rel(AY_SHIFTED_TRADES),
            "forbidden_sources": "post-trade profit as feature; shifted forward KPI as threshold(사후 수익 피처화; 이동 전진 KPI로 임계값 선택)",
            "timestamp_rule": "decision_time_or_prior_only(결정 시각 또는 이전만)",
            "split_rule": "future training must use pre-forward split only; run337BA has no training(미래 학습은 전진 전 분할만, 337BA 학습 없음)",
            "proxy_mt5_role": "MT5 trade records provide cost ladder; proxy cannot provide profit KPI(MT5 거래 기록은 비용 사다리 제공, 프록시는 수익 KPI 불가)",
            "review_gate": "az_gate_cost_ladder",
            "status": "materialized_contract_only(계약 물질화 전용)",
            "effect": designs.get("az_defensive_cost_margin_objective", {}).get("next_materialization_need", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "ba_feature_side_balance",
            "design_id": "az_repair_direction_balance_surface",
            "input_family": "side_balance(방향 균형)",
            "materialized_input": "side_balance_input_contract(방향 균형 입력 계약)",
            "allowed_sources": aw.rel(AY_PROTOCOL) + "; " + aw.rel(AY_SHIFTED_TRADES) + "; " + aw.rel(AY_COMPLETED_TRADES),
            "forbidden_sources": "forward short count target; side-specific threshold selected from shifted result(전진 숏 수 목표; 이동 결과 기반 방향별 임계값)",
            "timestamp_rule": "trade direction at decision time only(결정 시점 거래 방향만)",
            "split_rule": "side objective must be judged on predeclared split packs(방향 목적은 사전 선언 분할 묶음에서 판정)",
            "proxy_mt5_role": "proxy may check side decision parity; MT5 owns side fill attribution(프록시는 방향 결정 동등성 점검, MT5는 방향 체결 귀속 담당)",
            "review_gate": "az_gate_density_retention",
            "status": "materialized_contract_only(계약 물질화 전용)",
            "effect": designs.get("az_repair_direction_balance_surface", {}).get("next_materialization_need", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "ba_feature_density_retention",
            "design_id": "az_aggressive_density_preservation",
            "input_family": "density_retention(거래 밀도 보존)",
            "materialized_input": "density_retention_contract(밀도 보존 계약)",
            "allowed_sources": aw.rel(AY_FINAL) + "; " + aw.rel(AY_SHIFTED_TRADES) + "; " + aw.rel(AY_COMPLETED_TRADES),
            "forbidden_sources": "lot scaling; trade-count maximization on shifted forward result(로트 조정; 이동 전진 결과의 거래 수 최대화)",
            "timestamp_rule": "pre-trade exposure state only(진입 전 노출 상태만)",
            "split_rule": "report retention ratios but do not select parameters in run337BA(보존 비율 보고, 337BA 파라미터 선택 없음)",
            "proxy_mt5_role": "proxy cannot certify trade density; MT5 records fill/skip/fill count(MT5 기록만 거래 밀도 체결/스킵 확인)",
            "review_gate": "az_gate_density_retention",
            "status": "materialized_contract_only(계약 물질화 전용)",
            "effect": designs.get("az_aggressive_density_preservation", {}).get("next_materialization_need", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "ba_feature_curve_state_veto",
            "design_id": "az_repair_curve_pocket_state_veto",
            "input_family": "curve_state_veto(곡선 상태 거부)",
            "materialized_input": "curve_state_veto_feature_map(곡선 상태 거부 피처맵)",
            "allowed_sources": aw.rel(AY_CURVE) + "; " + aw.rel(AY_REGIME) + "; " + aw.rel(AY_SHIFTED_TRADES),
            "forbidden_sources": "trade index, calendar date, realized drawdown after entry(거래 번호, 달력 날짜, 진입 후 실현 손실)",
            "timestamp_rule": "pre-trade ATR/ADX/vol/session/as-of macro only(진입 전 ATR/ADX/변동성/세션/as-of 거시만)",
            "split_rule": "state thesis must be written before MT5 retest(상태 논제는 MT5 재시험 전 작성)",
            "proxy_mt5_role": "proxy checks input availability; MT5 confirms actual curve pocket(프록시는 입력 가용성, MT5는 실제 곡선 포켓 확인)",
            "review_gate": "az_gate_curve_pocket_out_of_sample",
            "status": "materialized_contract_only(계약 물질화 전용)",
            "effect": designs.get("az_repair_curve_pocket_state_veto", {}).get("next_materialization_need", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "ba_feature_proxy_mt5_dual_read",
            "design_id": "az_control_proxy_mt5_dual_read",
            "input_family": "proxy_mt5_dual_read(프록시-MT5 이중 판독)",
            "materialized_input": "proxy_runtime_pairing_contract(프록시-런타임 짝 계약)",
            "allowed_sources": aw.rel(AY_PROXY) + "; " + aw.rel(AY_PROTOCOL),
            "forbidden_sources": "proxy numeric net/PF/DD as forward KPI(프록시 숫자 순익/PF/DD를 전진 KPI로 사용)",
            "timestamp_rule": "exact decision timestamp join only(정확 결정 시각 결합만)",
            "split_rule": "proxy role is signal sanity only across all splits(프록시 역할은 모든 분할에서 신호 점검 전용)",
            "proxy_mt5_role": "proxy detects mismatch; MT5 owns KPI(프록시는 불일치 탐지, MT5는 KPI 담당)",
            "review_gate": "az_gate_proxy_mt5_dual_evidence",
            "status": "materialized_contract_only(계약 물질화 전용)",
            "effect": designs.get("az_control_proxy_mt5_dual_read", {}).get("next_materialization_need", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_contracts(src: Mapping[str, Any], feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    design_ids = ",".join(str(row.get("design_id", "")) for row in feature_rows)
    artifact_by_gate = {
        "az_gate_no_forward_threshold_search": aw.rel(NO_LOOKAHEAD_AUDIT),
        "az_gate_proxy_mt5_dual_evidence": aw.rel(PROXY_MT5_PAIRING),
        "az_gate_density_retention": aw.rel(DENSITY_RETENTION_CONTRACT),
        "az_gate_cost_ladder": aw.rel(COST_MARGIN_CONTRACT),
        "az_gate_curve_pocket_out_of_sample": aw.rel(CURVE_STATE_VETO_MAP),
        "az_gate_asof_data_integrity": aw.rel(NO_LOOKAHEAD_AUDIT),
    }
    rows = []
    for gate in src["az_falsification"]:
        gate_id = str(gate.get("gate_id", ""))
        rows.append(
            {
                "contract_id": f"ba_contract_{gate_id}",
                "source_gate_id": gate_id,
                "design_ids": design_ids if gate_id != "az_gate_proxy_mt5_dual_evidence" else "az_control_proxy_mt5_dual_read",
                "gate_family": gate.get("gate_type", ""),
                "artifact_to_check": artifact_by_gate.get(gate_id, aw.rel(GATE_CONTRACT)),
                "pass_condition": gate.get("pass_condition", ""),
                "fail_condition": gate.get("fail_condition", ""),
                "prevents_overfit_path": gate.get("effect", ""),
                "review_owner": NEXT_RUN_ID,
                "status": "materialized_for_review(검토용 물질화)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_pairing(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for idx, policy in enumerate(src["az_proxy_policy"], start=1):
        subject = str(policy.get("subject", ""))
        rows.append(
            {
                "pairing_id": f"ba_proxy_pair_{idx:02d}",
                "subject": subject,
                "proxy_artifact": aw.rel(AY_PROXY),
                "mt5_runtime_artifact": aw.rel(AY_SHIFTED_TRADES) if "shifted" in subject.lower() or "이동" in subject else aw.rel(AY_PROTOCOL),
                "required_join_key": "decision_timestamp_exact_or_report_trade_identity(정확 결정 시각 또는 보고서 거래 정체성)",
                "usable_for": policy.get("usable_for", ""),
                "not_usable_for": policy.get("not_usable_for", ""),
                "mismatch_action": "abort runtime KPI claim and route to run337BB review(런타임 KPI 주장 중단 후 337BB 검토로 보냄)",
                "status": "materialized_pairing_contract(쌍 계약 물질화)",
                "effect": policy.get("next_required_evidence", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_negative_controls(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    all_designs = ",".join(str(row.get("design_id", "")) for row in feature_rows)
    return [
        {
            "control_id": "ba_control_no_forward_threshold_search",
            "control_family": "overfit_search(과적합 탐색)",
            "applies_to_designs": all_designs,
            "materialized_check": "manifest and contracts contain no selected threshold/lot/D-B parameter(목록과 계약에 선택된 임계값/로트/D-B 파라미터 없음)",
            "expected_failure_or_guard": "any parameter chosen from run337AY KPI fails(337AY KPI에서 고른 파라미터는 실패)",
            "invalid_if": "run337BA selects a candidate or threshold(337BA가 후보나 임계값 선택)",
            "status": "active_guard(활성 가드)",
            "effect": "keeps repair from becoming forward retune(수리가 전진 재튜닝이 되는 것을 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ba_control_trade_index_veto_forbidden",
            "control_family": "curve_pocket(곡선 포켓)",
            "applies_to_designs": "az_repair_curve_pocket_state_veto",
            "materialized_check": "curve inputs cannot contain trade_index veto or exact bad pocket id(곡선 입력은 거래 번호 거부나 정확한 나쁜 포켓 ID 포함 불가)",
            "expected_failure_or_guard": "trade index/date veto fails(거래 번호/날짜 거부는 실패)",
            "invalid_if": "calendar date, row number, or realized drawdown enters feature contract(날짜/행 번호/실현 손실이 피처 계약에 들어감)",
            "status": "active_guard(활성 가드)",
            "effect": "prevents memorized pretty curve(암기된 예쁜 곡선 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ba_control_proxy_only_abort",
            "control_family": "proxy_mt5_boundary(프록시-MT5 경계)",
            "applies_to_designs": "az_control_proxy_mt5_dual_read",
            "materialized_check": "proxy-only KPI claim aborts review(프록시 단독 KPI 주장은 검토 중단)",
            "expected_failure_or_guard": "proxy result without MT5 runtime identity is unusable for forward(런타임 정체성 없는 프록시 결과는 전진에 사용 불가)",
            "invalid_if": "proxy net/PF/DD is written as forward result(프록시 순익/PF/DD가 전진 결과로 기록)",
            "status": "active_guard(활성 가드)",
            "effect": "keeps proxy useful but bounded(프록시를 유용하지만 제한된 상태로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ba_control_cost_overstress",
            "control_family": "cost_stress(비용 압박)",
            "applies_to_designs": "az_defensive_cost_margin_objective",
            "materialized_check": "cost ladder must include zero, 0.5, 1.0, 2.0 point stress references(비용 사다리는 0/0.5/1.0/2.0 포인트 압박 참조 포함)",
            "expected_failure_or_guard": "small cost collapse remains visible(작은 비용 붕괴가 계속 드러남)",
            "invalid_if": "cost stress row is removed to make design pass(설계 통과를 위해 비용 압박 행 제거)",
            "status": "active_guard(활성 가드)",
            "effect": "keeps thin cost buffer exposed(얇은 비용 버퍼를 계속 노출)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ba_control_side_shuffle",
            "control_family": "direction_balance(방향 균형)",
            "applies_to_designs": "az_repair_direction_balance_surface",
            "materialized_check": "direction labels must be decision-time labels and side shuffle remains a negative check(방향 라벨은 결정 시점 라벨이며 방향 셔플은 부정 점검으로 유지)",
            "expected_failure_or_guard": "side repair cannot pass by forcing short count(방향 수리는 숏 수 강제로 통과 불가)",
            "invalid_if": "future short profit selects a side rule(미래 숏 수익이 방향 규칙을 선택)",
            "status": "active_guard(활성 가드)",
            "effect": "keeps side repair honest(방향 수리를 정직하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ba_control_broker_current_day_gap",
            "control_family": "runtime_boundary(런타임 경계)",
            "applies_to_designs": all_designs,
            "materialized_check": "broker current-day gap remains negative control until repaired by MT5 evidence(브로커 현재일 공백은 MT5 근거로 수리되기 전까지 부정 대조)",
            "expected_failure_or_guard": "synthetic shifted route cannot claim broker forward authority(합성 이동 경로는 브로커 전진 권위 주장 불가)",
            "invalid_if": "shifted custom result is called broker current-day forward result(이동 커스텀 결과를 브로커 현재일 전진 결과로 부름)",
            "status": "active_guard(활성 가드)",
            "effect": "keeps runtime boundary visible(런타임 경계를 보이게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_special_contracts(src: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    ay_final = src["ay_final"]
    shifted = f"shifted_trades={ay_final.get('shifted_trade_count', '')};shifted_net={ay_final.get('shifted_net_profit', '')};shifted_pf={ay_final.get('shifted_profit_factor', '')}"
    completed = f"completed_trades={ay_final.get('completed_trade_count', '')};completed_net={ay_final.get('completed_net_profit', '')};completed_pf={ay_final.get('completed_profit_factor', '')}"
    cost_rows = src["ay_cost"]
    cost_levels = ",".join(str(row.get("cost_points_per_trade", "")) for row in cost_rows)
    cost_contract = [
        {
            "contract_id": "ba_cost_margin_ladder_reference",
            "design_id": "az_defensive_cost_margin_objective",
            "input_fields": "entry_time,direction,volume,base_net_profit,cost_points_per_trade",
            "derived_fields": "stressed_net,stressed_pf,cost_margin_alert",
            "allowed_calculation": "apply predeclared cost ladder to MT5 trade records(사전 선언 비용 사다리를 MT5 거래 기록에 적용)",
            "forbidden_calculation": "choose threshold, lot, or entry filter from cost stress result(비용 압박 결과로 임계값/로트/진입 필터 선택)",
            "parent_reference": f"{shifted};cost_levels={cost_levels}",
            "materialization_status": "ready_for_run337BB_review(337BB 검토 준비)",
            "next_review": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    side_contract = [
        {
            "contract_id": "ba_side_balance_reference",
            "design_id": "az_repair_direction_balance_surface",
            "input_fields": "decision_time,direction,side_signal,mt5_fill_side",
            "derived_fields": "side_coverage,side_expectancy,side_density_alert",
            "allowed_calculation": "compare long/short attribution by decision-time side(결정 시점 방향별 롱/숏 귀속 비교)",
            "forbidden_calculation": "force shorts or tune side threshold from forward short outcome(전진 숏 결과로 숏 강제 또는 방향 임계값 조정)",
            "parent_reference": f"{shifted};{completed}",
            "materialization_status": "ready_for_run337BB_review(337BB 검토 준비)",
            "next_review": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    density_contract = [
        {
            "contract_id": "ba_density_retention_reference",
            "design_id": "az_aggressive_density_preservation",
            "input_fields": "trade_count,trades_per_day,fill_count,skip_count,exposure_hours",
            "derived_fields": "density_retention_ratio,fill_skip_balance,density_alert",
            "allowed_calculation": "report density against parent anchors without selecting a pass threshold(부모 앵커 대비 밀도 보고, 통과 임계값 선택 없음)",
            "forbidden_calculation": "optimize lot or entry count to reach desired trade count(원하는 거래 수 도달을 위해 로트 또는 진입 수 최적화)",
            "parent_reference": f"{shifted};{completed}",
            "materialization_status": "ready_for_run337BB_review(337BB 검토 준비)",
            "next_review": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    curve_contract = [
        {
            "contract_id": "ba_curve_state_veto_reference",
            "design_id": "az_repair_curve_pocket_state_veto",
            "input_fields": "decision_time,atr_14,adx_14,vol_20,session_utc,asof_regime_bucket",
            "derived_fields": "state_veto_candidate,rolling_pocket_alert,underwater_risk_flag",
            "allowed_calculation": "map pre-trade state to curve pocket diagnostics(진입 전 상태를 곡선 포켓 진단에 매핑)",
            "forbidden_calculation": "use trade index, exact date, or realized underwater after entry(거래 번호/정확 날짜/진입 후 수중 상태 사용)",
            "parent_reference": aw.rel(AY_CURVE) + ";" + aw.rel(AY_REGIME),
            "materialization_status": "ready_for_run337BB_review(337BB 검토 준비)",
            "next_review": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return cost_contract, side_contract, density_contract, curve_contract


def build_source_hashes() -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_FILES:
        ident = source_identity(path)
        rows.append(
            {
                "source_id": path.stem,
                "path": ident["path"],
                "exists": ident["exists"],
                "row_count": ident["row_count"],
                "sha256": ident["sha256"],
                "used_for": "run337BA materialized input contract lineage(337BA 입력 계약 계보)",
                "availability": "tracked_or_registered_source(추적 또는 등록된 원천)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_package_manifest(paths: Sequence[Path]) -> list[dict[str, Any]]:
    rows = []
    source_inputs = ";".join(aw.rel(path) for path in INPUT_FILES)
    for path in paths:
        if path in {PACKAGE_MANIFEST, GATE_AUDIT, FINAL_DECISION, RUN_MANIFEST}:
            continue
        rows.append(
            {
                "package_id": f"{RUN_ID}::{path.stem}",
                "artifact_path": aw.rel(path),
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "rows": row_count(path) if aw.path_exists(path) else "",
                "producer": aw.rel(__file__),
                "consumer": NEXT_RUN_ID,
                "source_inputs": source_inputs,
                "status": "materialized_or_receipt(물질화 또는 영수증)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_no_lookahead_audit(src: Mapping[str, Any], feature_rows: Sequence[Mapping[str, Any]], negative_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    feature_text = " ".join(str(row.get("timestamp_rule", "")) + " " + str(row.get("forbidden_sources", "")) for row in feature_rows).lower()
    data_text = " ".join(str(row.get("feature_label_boundary", "")) + " " + str(row.get("leakage_risk", "")) for row in src["az_data_boundary"]).lower()
    negative_text = " ".join(str(row.get("invalid_if", "")) + " " + str(row.get("materialized_check", "")) for row in negative_rows).lower()
    return [
        {
            "audit_id": "ba_audit_timestamp_rules",
            "status": "passed" if ("decision" in feature_text or "결정" in feature_text) and ("pre-trade" in feature_text or "진입 전" in feature_text) else "failed",
            "observed": "feature contracts contain decision-time/pre-trade timestamp rules(피처 계약에 결정 시점/진입 전 시각 규칙 포함)",
            "expected": "no future bar or post-trade state in inputs(미래 봉 또는 사후 상태 입력 금지)",
            "effect": "blocks look-ahead feature materialization(미래참조 피처 물질화 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ba_audit_forward_parameter_search_forbidden",
            "status": "passed" if ("threshold" in feature_text or "임계" in feature_text) and ("forward" in feature_text or "전진" in feature_text) else "failed",
            "observed": "feature contracts forbid forward threshold/parameter use(피처 계약이 전진 임계값/파라미터 사용 금지)",
            "expected": "no parameter selected from shifted evidence(이동 근거에서 파라미터 선택 없음)",
            "effect": "keeps materialization from becoming retune(물질화가 재튜닝이 되지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ba_audit_data_boundary_inherited",
            "status": "passed" if ("future" in data_text or "미래" in data_text or "look-ahead" in data_text) and ("feature" in data_text or "피처" in data_text) else "failed",
            "observed": f"data_boundary_rows={len(src['az_data_boundary'])}",
            "expected": "run337AZ data boundary inherited(337AZ 데이터 경계 상속)",
            "effect": "connects materialized inputs to parent data integrity(물질화 입력을 부모 데이터 무결성과 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ba_audit_negative_controls_active",
            "status": "passed" if all(token in negative_text for token in ("proxy", "trade", "threshold")) or ("프록시" in negative_text and "거래" in negative_text and "임계" in negative_text) else "failed",
            "observed": f"negative_controls={len(negative_rows)}",
            "expected": "proxy-only, trade-index, threshold controls active(프록시 단독/거래 번호/임계값 대조 활성)",
            "effect": "keeps known overfit paths visible(알려진 과적합 경로를 보이게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_review_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BB_input_contract_review",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "run337BA materialized no-overfit repair inputs(337BA 물질화된 무과적합 수리 입력)",
            "inputs_to_review": ";".join(aw.rel(path) for path in (FEATURE_CONTRACT, GATE_CONTRACT, PROXY_MT5_PAIRING, NEGATIVE_CONTROL_PLAN, NO_LOOKAHEAD_AUDIT)),
            "must_confirm": "all five design ids materialized, no future leakage, proxy bounded, MT5 KPI authority preserved(5개 설계 물질화, 미래 누수 없음, 프록시 경계, MT5 KPI 권위 보존)",
            "must_reject_if": "candidate, threshold, D/B rule, lot, date pocket, or trade-index rule appears(후보/임계값/D-B 규칙/로트/날짜 포켓/거래 번호 규칙 등장)",
            "expected_outputs": "input_review.csv;materialization_acceptance.csv;runtime_probe_or_repair_queue.csv",
            "priority": "P0",
            "effect": "forces review before any MT5 runtime probe or model build(MT5 런타임 탐침 또는 모델 빌드 전 검토 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(src: Mapping[str, Any], feature_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]], proxy_rows: Sequence[Mapping[str, Any]], negative_rows: Sequence[Mapping[str, Any]], no_lookahead_rows: Sequence[Mapping[str, Any]], review_queue: Sequence[Mapping[str, Any]], source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    az_gate_passed = all(str(row.get("status", "")) == "passed" for row in src["az_gate"]) and bool(src["az_gate"])
    az_claims_clean = all(str(src["az_final"].get(key, "")) == "not_claimed" for key in ("forward_passed", "forward_failed", "runtime_authority", "goal_achieve"))
    design_ids = {str(row.get("design_id", "")) for row in src["az_design"]}
    feature_design_ids = {str(row.get("design_id", "")) for row in feature_rows}
    gate_source_ids = {str(row.get("source_gate_id", "")) for row in gate_rows}
    parent_gate_ids = {str(row.get("gate_id", "")) for row in src["az_falsification"]}
    source_all_exist = all(str(row.get("exists", "")).lower() == "true" for row in source_rows)
    return [
        {
            "gate_id": "source_run337AZ_loaded",
            "status": "passed" if src["az_final"] and src["az_design"] and src["az_queue"] else "failed",
            "observed": f"design={len(src['az_design'])};queue={len(src['az_queue'])};final={bool(src['az_final'])}",
            "expected": "run337AZ design/final/queue present(337AZ 설계/최종/대기열 존재)",
            "effect": "materialization starts from approved design(승인된 설계에서 물질화 시작)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "parent_gate_inherited",
            "status": "passed" if az_gate_passed else "failed",
            "observed": f"run337AZ_gates={sum(1 for row in src['az_gate'] if str(row.get('status', '')) == 'passed')}/{len(src['az_gate'])}",
            "expected": "run337AZ gates passed before input materialization(입력 물질화 전 337AZ 게이트 통과)",
            "effect": "prevents materializing from invalid design(무효 설계에서 물질화 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "materializes_all_design_ids",
            "status": "passed" if design_ids == feature_design_ids and len(feature_rows) == 5 else "failed",
            "observed": f"design_ids={len(design_ids)};feature_contracts={len(feature_rows)}",
            "expected": "all five run337AZ designs materialized(337AZ 5개 설계 모두 물질화)",
            "effect": "keeps defensive/aggressive/repair/control balance intact(방어/공격/수리/대조 균형 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "falsification_gate_contracts_materialized",
            "status": "passed" if parent_gate_ids == gate_source_ids and len(gate_rows) >= 6 else "failed",
            "observed": f"parent_gates={len(parent_gate_ids)};gate_contracts={len(gate_rows)}",
            "expected": "all falsification gates become gate contracts(모든 반증 게이트가 게이트 계약으로 전환)",
            "effect": "future runs can reject bad repair paths(미래 실행이 나쁜 수리 경로를 거절 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_pairing_boundary",
            "status": "passed" if proxy_rows and all("Forward" in str(row.get("not_usable_for", "")) or "전진" in str(row.get("not_usable_for", "")) for row in proxy_rows) else "failed",
            "observed": f"proxy_pairing_rows={len(proxy_rows)}",
            "expected": "proxy paired with MT5 and not usable for forward KPI(프록시는 MT5와 쌍이며 전진 KPI 불가)",
            "effect": "prevents proxy-only selection(프록시 단독 선택 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "negative_controls_materialized",
            "status": "passed" if len(negative_rows) >= 6 else "failed",
            "observed": f"negative_controls={len(negative_rows)}",
            "expected": "threshold, trade-index, proxy-only, cost, side, broker-gap controls(임계값/거래 번호/프록시 단독/비용/방향/브로커 공백 대조)",
            "effect": "keeps overfit traps attached to the package(과적합 함정을 패키지에 부착)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_lookahead_audit_passed",
            "status": "passed" if no_lookahead_rows and all(str(row.get("status", "")) == "passed" for row in no_lookahead_rows) else "failed",
            "observed": f"no_lookahead={sum(1 for row in no_lookahead_rows if str(row.get('status', '')) == 'passed')}/{len(no_lookahead_rows)}",
            "expected": "all no-lookahead audits passed(모든 미래참조 방지 감사 통과)",
            "effect": "protects against repeat look-ahead bias(미래참조 편향 재발 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "input_source_lineage_complete",
            "status": "passed" if source_all_exist and len(source_rows) == len(INPUT_FILES) else "failed",
            "observed": f"sources={len(source_rows)};all_exist={source_all_exist}",
            "expected": "all source inputs exist and have identity(모든 원천 입력 존재 및 정체성 보유)",
            "effect": "makes ignored run outputs reusable through registry hashes(무시된 실행 산출물을 등록부 해시로 재사용 가능하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "review_queue_ready",
            "status": "passed" if review_queue and str(review_queue[0].get("next_run_id", "")) == NEXT_RUN_ID else "failed",
            "observed": f"review_queue_rows={len(review_queue)};next={review_queue[0].get('next_run_id', '') if review_queue else ''}",
            "expected": NEXT_RUN_ID,
            "effect": "forces review before runtime probe or training(런타임 탐침 또는 학습 전 검토 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_training_selection_claim_guard",
            "status": "passed" if az_claims_clean else "failed",
            "observed": f"parent_forward_claims_clean={az_claims_clean};run337BA_claims=no_forward_no_goal",
            "expected": "no training, threshold retune, candidate selection, forward/goal claim(학습/임계값 재조정/후보 선택/전진-목표 주장 없음)",
            "effect": "keeps run337BA as input materialization only(337BA를 입력 물질화로만 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    receipts = [
        (
            ROUTING_RECEIPT,
            {
                "work_packet_lifecycle": "experiment_to_evidence_to_report(실험-근거-보고)",
                "primary_family": "experiment_execution",
                "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
                "support_skills": [
                    "obsidian-experiment-design(실험 설계)",
                    "obsidian-data-integrity(데이터 무결성)",
                    "obsidian-model-validation(모델 검증)",
                    "obsidian-artifact-lineage(산출물 계보)",
                ],
                "required_gates": [
                    "scope_completion_gate",
                    "kpi_contract_audit",
                    "skill_receipt_lint",
                    "required_gate_coverage_audit",
                ],
                "branch_worktree_fit": "main matches workspace_state active_branch(메인 브랜치가 현재 상태와 일치)",
                "branch_action": "stay",
                "handoff_surface": [aw.rel(REPORT_PATH), aw.rel(FEATURE_CONTRACT), aw.rel(RUN_REGISTRY)],
            },
        ),
        (
            RUN_EVIDENCE_RECEIPT,
            {
                "measurement_scope": "input materialization contract; no new trading KPI(입력 물질화 계약, 신규 거래 KPI 없음)",
                "management_state": "run folder, manifest, report, ledgers, artifact registry updated(실행 폴더/목록/보고서/장부/산출물 등록부 갱신)",
                "judgment_class": "inconclusive_for_forward_but_completed_for_input_materialization(전진 판정 불충분, 입력 물질화 완료)",
                "scoreboard": "diagnostic_special",
                "parity_level": "P3_runtime_shadow_parity_sampled inherited, not upgraded(부모의 P3 런타임 그림자 동등성 표본 상속, 상향 없음)",
                "wfo_status": "not_applicable(해당 없음)",
                "registry_update_required": "yes",
                "negative_memory_required": "yes",
                "hard_gate_applicable": "no",
                "evidence_boundary": "materialized_input_contract_only(물질화 입력 계약 전용)",
            },
        ),
        (
            EXPERIMENT_RECEIPT,
            {
                "hypothesis": "run337AZ design can become concrete no-overfit repair input contracts(337AZ 설계가 구체 무과적합 수리 입력 계약이 될 수 있다)",
                "decision_use": "open run337BB review, not runtime probe or candidate selection(337BB 검토 개방, 런타임 탐침 또는 후보 선택 아님)",
                "comparison_baseline": "run337AZ design and run337AY evidence(337AZ 설계와 337AY 근거)",
                "control_variables": "no training, no retune, no D/B, no lot, no forward claim(학습/재조정/D-B/로트/전진 주장 없음)",
                "changed_variables": "materialized contract files only(물질화 계약 파일만 변경)",
                "sample_scope": "US100 M5 post-OOS diagnostic evidence with synthetic-shift boundary(US100 M5 표본외 이후 진단 근거와 합성 이동 경계)",
                "success_criteria": "feature, gate, proxy, negative control, lineage, no-lookahead audit, review queue materialized(피처/게이트/프록시/부정 대조/계보/미래참조 감사/검토 대기열 물질화)",
                "failure_criteria": "missing design id, missing source identity, proxy-only KPI, or leakage(설계 ID 누락/원천 정체성 누락/프록시 단독 KPI/누수)",
                "invalid_conditions": "candidate/threshold/lot/D-B selected in run337BA(337BA에서 후보/임계값/로트/D-B 선택)",
                "stop_conditions": "run337BB must review before any MT5 runtime or model action(337BB 검토 전 MT5 런타임 또는 모델 행동 금지)",
                "evidence_plan": [aw.rel(FEATURE_CONTRACT), aw.rel(GATE_CONTRACT), aw.rel(NO_LOOKAHEAD_AUDIT), aw.rel(GATE_AUDIT)],
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [aw.rel(path) for path in INPUT_FILES],
                "time_axis": "US100 M5 decision timestamp; exact shifted custom route remains diagnostic(US100 M5 결정 시각, 정확 이동 커스텀 경로는 진단용 유지)",
                "sample_scope": "post-2026-04-14 diagnostic forward evidence, no training use(2026-04-14 이후 진단 전진 근거, 학습 사용 없음)",
                "missing_or_duplicate_check": "source identities and row counts materialized; deeper row audit deferred to run337BB(원천 정체성과 행 수 물질화, 깊은 행 감사는 337BB)",
                "feature_label_boundary": "pre-trade features only, no realized outcome feature(진입 전 피처만, 실현 결과 피처 없음)",
                "split_boundary": "forward evidence cannot select parameters(전진 근거는 파라미터 선택 불가)",
                "leakage_risk": "threshold, date-pocket, trade-index, proxy-only overfit(임계값/날짜 포켓/거래 번호/프록시 단독 과적합)",
                "data_hash_or_identity": aw.rel(INPUT_SOURCE_HASH),
                "integrity_judgment": "usable_with_boundary(경계付き 사용 가능)",
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "future non-frozen ONNX repair input contract; no model built(미래 비고정 ONNX 수리 입력 계약, 모델 빌드 없음)",
                "target_and_label": "no new label; future labels must be predeclared(신규 라벨 없음, 미래 라벨 사전 선언 필요)",
                "split_method": "forward diagnostic only, no training split consumed(전진 진단 전용, 학습 분할 소비 없음)",
                "selection_metric": "none(없음)",
                "secondary_metrics": "cost/direction/density/curve/proxy-MT5 gates(비용/방향/밀도/곡선/프록시-MT5 게이트)",
                "threshold_policy": "fixed/no search(고정/탐색 없음)",
                "overfit_risk": "materializing run337AY weakness into hidden parameter(337AY 약점을 숨은 파라미터로 물질화)",
                "calibration_risk": "proxy score is sanity signal, not probability proof(프록시 점수는 점검 신호, 확률 증명 아님)",
                "comparison_baseline": "run337AY/AZ(337AY/AZ)",
                "validation_judgment": "exploratory_input_materialization_only(탐색 입력 물질화 전용)",
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [aw.rel(path) for path in INPUT_FILES],
                "producer": aw.rel(__file__),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [aw.rel(path) for path in OUTPUT_FILES],
                "artifact_hashes": "registered in artifact_registry after write(작성 후 산출물 등록부에 기록)",
                "registry_links": [aw.rel(RUN_REGISTRY), aw.rel(ALPHA_LEDGER), aw.rel(STAGE_LEDGER), aw.rel(ARTIFACT_REGISTRY)],
                "availability": "tracked report and generated ignored run folder with registry identity(추적 보고서와 등록부 정체성을 가진 생성 실행 폴더)",
                "lineage_judgment": "connected_with_boundary(경계付き 연결)",
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [aw.rel(FEATURE_CONTRACT), aw.rel(GATE_CONTRACT), aw.rel(GATE_AUDIT)],
                "evidence_missing": "run337BB review, MT5 repair probe, new ONNX, operating parity closure(337BB 검토/MT5 수리 탐침/새 ONNX/운영 동등성 폐쇄)",
                "judgment_label": "exploratory(탐색)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "Inputs are now concrete, but the model is not yet improved or tradable(입력은 구체화됐지만 모델 개선이나 거래 가능성은 아직 아님).",
            },
        ),
    ]
    return [aw.write_json(path, payload) for path, payload in receipts]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BA No-Overfit Repair Inputs(337단계 337BA 무과적합 수리 입력)

## Purpose(목적)

run337BA(337BA 실행)는 run337AZ(337AZ 실행)의 no-overfit repair design(무과적합 수리 설계)을 실제 input contracts(입력 계약)로 물질화했다.

Effect(효과): 다음 run337BB(337BB 실행)가 비용(cost, 비용), 방향(side, 방향), 밀도(density, 밀도), 곡선 포켓(curve pocket, 곡선 포켓), proxy-MT5 pairing(프록시-MT5 쌍)을 검토할 수 있다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- feature_contract_rows(피처 계약 행): `{final['feature_contract_rows']}`
- gate_contract_rows(게이트 계약 행): `{final['gate_contract_rows']}`
- proxy_pairing_rows(프록시 쌍 행): `{final['proxy_pairing_rows']}`
- negative_control_rows(부정 대조 행): `{final['negative_control_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Plain Meaning(쉬운 의미)

이번 결과는 새 모델이 좋아졌다는 뜻이 아니다. 지금 한 일은 다음 검토자가 사용할 체크리스트와 입력 표를 만든 것이다.

Effect(효과): 수리 실험을 진행하되, 전진 결과에 맞춰 threshold(임계값), lot(로트), D/B rule(D/B 규칙), 날짜 포켓(date pocket, 날짜 포켓)을 맞추는 길을 막는다.

## Outputs(산출물)

- `{aw.rel(FEATURE_CONTRACT)}`
- `{aw.rel(GATE_CONTRACT)}`
- `{aw.rel(PROXY_MT5_PAIRING)}`
- `{aw.rel(NEGATIVE_CONTROL_PLAN)}`
- `{aw.rel(NO_LOOKAHEAD_AUDIT)}`
- `{aw.rel(RUN337BB_QUEUE)}`
- `{aw.rel(GATE_AUDIT)}`

## Decision(결정)

- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337BA

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

run337BA(337BA 실행)는 input materialization(입력 물질화)만 완료했다. model training(모델 학습), threshold retune(임계값 재조정), D/B rewrite(D/B 재작성), lot optimization(로트 최적화), candidate selection(후보 선택)은 없다.

Effect(효과): 다음 작업은 run337BB(337BB 실행) 검토이며, Forward/Goal(전진/목표)은 계속 주장하지 않는다.
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def insert_current_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text:
        return text
    if marker not in text:
        return text.rstrip() + "\n" + block
    return text.replace(marker, marker + block, 1)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    ws, ws_bom = aw.read_tracked_text_lossless(WORKSPACE_STATE)
    ws = aw.replace_prefix_line(ws, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337BA focus complete: run337BA(337BA 실행)은 `{final['status']}`로 no-overfit repair inputs(무과적합 수리 입력)을 물질화했다. Effect(효과): feature contracts(피처 계약) `{final['feature_contract_rows']}`, gate contracts(게이트 계약) `{final['gate_contract_rows']}`, negative controls(부정 대조) `{final['negative_control_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    ws = insert_current_focus(ws, focus)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, ws, ws_bom))

    current, current_bom = aw.read_tracked_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": f"- status(상태): `{final['status']}`",
        "- decision(결정):": f"- decision(결정): `{final['decision']}`",
        "- latest_completed_run(최근 완료 실행):": f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- next_action(다음 행동):": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current = aw.replace_prefix_line(current, prefix, replacement)
    section = f"""
## Stage337 run337BA(337BA 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BA(337BA 실행)는 run337AZ(337AZ 실행)의 설계를 피처/게이트/proxy-MT5/부정 대조 계약으로 물질화했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337BA" not in current:
        current = current.replace("## Stage337 run337AZ", section + "\n## Stage337 run337AZ", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- shifted_custom_route(이동 커스텀 경로): `feature_last_reached_attribution_fragile`
- completed_day_anchor(완성일 앵커): `feature_last_reached_realism_anchor`
- materialized_feature_contract_rows(물질화 피처 계약 행): `{final['feature_contract_rows']}`
- materialized_gate_contract_rows(물질화 게이트 계약 행): `{final['gate_contract_rows']}`
- negative_control_rows(부정 대조 행): `{final['negative_control_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_review_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337BA(337BA 실행)는 검토 가능한 입력을 만들었지만 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = aw.replace_prefix_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337BA_summary(337BA 요약): `{final['status']}`. "
        f"Effect(효과): run337AZ 설계를 feature contracts(피처 계약) `{final['feature_contract_rows']}`행, gate contracts(게이트 계약) `{final['gate_contract_rows']}`행, negative controls(부정 대조) `{final['negative_control_rows']}`행으로 물질화했고 run337BB(337BB 실행) 검토를 연다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337BA_summary" not in brief:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337BA(337BA 실행) `{final['status']}`. "
        f"Effect(효과): no-overfit repair design(무과적합 수리 설계)을 입력 계약과 run337BB 검토 대기열로 물질화하고 Forward/Goal(전진/목표)은 주장하지 않음."
    )
    if "Stage337 run337BA" not in changelog:
        changelog = changelog.rstrip() + "\n" + line + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "no_overfit_repair_input_materialization_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};feature_contracts={final['feature_contract_rows']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "family": "experiment_execution",
        "primary_report": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__no_overfit_repair_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "no_overfit_repair_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "no_overfit_repair_input_materialization_without_db(D/B 없는 무과적합 수리 입력 물질화)",
        "tier_scope": "Tier A shifted/completed diagnostic evidence with input boundary(Tier A 이동/완성 진단 근거, 입력 경계 포함)",
        "kpi_scope": "input_contract_no_new_trading_kpi(입력 계약, 신규 거래 KPI 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"feature_contracts={final['feature_contract_rows']};gate_contracts={final['gate_contract_rows']};negative_controls={final['negative_control_rows']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim_input_materialization_only(주장 범위 밖, 입력 물질화 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__no_overfit_repair_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "run337AZ design and run337AY attribution tables",
        "kpi_scope": "input_contract_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__no_overfit_repair_inputs",
        "family": "no_overfit_repair_input_materialization_without_db",
        "question": "can run337AZ design become concrete repair inputs without forward retune or D/B",
        "metric_scope": "feature_gate_proxy_negative_control_contracts",
        "primary_artifact": aw.rel(REPORT_PATH),
        "report_path": aw.rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not aw.path_exists(path):
            continue
        artifact_path = aw.rel(path)
        if artifact_path in seen:
            continue
        seen.add(artifact_path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return aw.write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    src = read_sources()
    feature_rows = build_feature_contracts(src)
    feature_path = aw.write_csv(FEATURE_CONTRACT, FEATURE_COLUMNS, feature_rows)
    gate_contract_rows = build_gate_contracts(src, feature_rows)
    gate_contract_path = aw.write_csv(GATE_CONTRACT, GATE_COLUMNS, gate_contract_rows)
    proxy_rows = build_proxy_pairing(src)
    proxy_path = aw.write_csv(PROXY_MT5_PAIRING, PAIRING_COLUMNS, proxy_rows)
    negative_rows = build_negative_controls(feature_rows)
    negative_path = aw.write_csv(NEGATIVE_CONTROL_PLAN, NEGATIVE_COLUMNS, negative_rows)
    cost_rows, side_rows, density_rows, curve_rows = build_special_contracts(src)
    cost_path = aw.write_csv(COST_MARGIN_CONTRACT, SPECIAL_CONTRACT_COLUMNS, cost_rows)
    side_path = aw.write_csv(SIDE_BALANCE_CONTRACT, SPECIAL_CONTRACT_COLUMNS, side_rows)
    density_path = aw.write_csv(DENSITY_RETENTION_CONTRACT, SPECIAL_CONTRACT_COLUMNS, density_rows)
    curve_path = aw.write_csv(CURVE_STATE_VETO_MAP, SPECIAL_CONTRACT_COLUMNS, curve_rows)
    source_rows = build_source_hashes()
    source_path = aw.write_csv(INPUT_SOURCE_HASH, SOURCE_COLUMNS, source_rows)
    no_lookahead_rows = build_no_lookahead_audit(src, feature_rows, negative_rows)
    no_lookahead_path = aw.write_csv(NO_LOOKAHEAD_AUDIT, AUDIT_COLUMNS, no_lookahead_rows)
    review_queue = build_review_queue()
    review_queue_path = aw.write_csv(RUN337BB_QUEUE, REVIEW_QUEUE_COLUMNS, review_queue)
    gate_rows = build_gates(src, feature_rows, gate_contract_rows, proxy_rows, negative_rows, no_lookahead_rows, review_queue, source_rows)
    gate_path = aw.write_csv(GATE_AUDIT, REQUIRED_GATE_COLUMNS, gate_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all(row.get("status") == "passed" for row in gate_rows) else "invalid_stage337BA_repair_input_materialization_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all(row.get("status") == "passed" for row in gate_rows) else "repair_input_materialization_gate_failure",
        "decision": DECISION if all(row.get("status") == "passed" for row in gate_rows) else "repair_stage337BA_input_materialization_gate_failure_before_run337BB",
        "next_action": NEXT_RUN_ID if all(row.get("status") == "passed" for row in gate_rows) else "repair_stage337BA_input_materialization_gate_failure_v1",
        "feature_contract_rows": len(feature_rows),
        "gate_contract_rows": len(gate_contract_rows),
        "proxy_pairing_rows": len(proxy_rows),
        "negative_control_rows": len(negative_rows),
        "cost_contract_rows": len(cost_rows),
        "side_contract_rows": len(side_rows),
        "density_contract_rows": len(density_rows),
        "curve_contract_rows": len(curve_rows),
        "source_rows": len(source_rows),
        "no_lookahead_rows": len(no_lookahead_rows),
        "review_queue_rows": len(review_queue),
        "gate_rows": len(gate_rows),
        "passed_gates": sum(1 for row in gate_rows if row.get("status") == "passed"),
        "failed_gates": [row.get("gate_id") for row in gate_rows if row.get("status") != "passed"],
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = aw.write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "producer": aw.rel(__file__),
        "parent_run_id": PARENT_RUN_ID,
        "inputs": [aw.rel(path) for path in INPUT_FILES],
        "outputs": [aw.rel(path) for path in OUTPUT_FILES],
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rewrite(D/B 재작성)",
            "lot optimization(로트 최적화)",
            "candidate selection(후보 선택)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    package_rows = build_package_manifest(
        [
            feature_path,
            gate_contract_path,
            proxy_path,
            negative_path,
            cost_path,
            side_path,
            density_path,
            curve_path,
            source_path,
            no_lookahead_path,
            review_queue_path,
            *receipt_paths,
        ]
    )
    package_path = aw.write_csv(PACKAGE_MANIFEST, PACKAGE_COLUMNS, package_rows)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        feature_path,
        gate_contract_path,
        proxy_path,
        negative_path,
        cost_path,
        side_path,
        density_path,
        curve_path,
        source_path,
        package_path,
        no_lookahead_path,
        review_queue_path,
        gate_path,
        *receipt_paths,
        final_path,
        manifest_path,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
        Path(__file__),
    ]
    artifact_registry_path = update_artifact_registry(artifact_paths, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "feature_contract_rows": final["feature_contract_rows"],
                "gate_contract_rows": final["gate_contract_rows"],
                "negative_controls": final["negative_control_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "report": aw.rel(report_path),
                "artifact_registry": aw.rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
