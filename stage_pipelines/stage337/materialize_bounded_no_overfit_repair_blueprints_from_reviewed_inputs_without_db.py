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

from stage_pipelines.stage337 import review_no_overfit_repair_inputs_from_shifted_attribution_without_db as bb


aw = bb.aw

TODAY = "2026-05-27"
STAGE_ID = bb.STAGE_ID
RUN_NUMBER = "run337BC"
RUN_ID = "run337BC_materialize_bounded_no_overfit_repair_blueprints_from_reviewed_inputs_without_db_v1"
PARENT_RUN_ID = bb.RUN_ID
NEXT_RUN_ID = "run337BD_review_bounded_no_overfit_repair_blueprints_without_db_v1"
STATUS = "completed_stage337BC_bounded_no_overfit_repair_blueprints_materialized_no_training_no_selection"
JUDGMENT = "bounded_repair_blueprints_materialized_with_cp322a_freeze_and_proxy_mt5_boundary"
DECISION = "stage337BC_open_run337BD_review_bounded_blueprints_no_training_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BC_bounded_no_overfit_repair_blueprints_without_db_"
    "cp322a_frozen_no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bb.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bb.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BC_bounded_no_overfit_repair_blueprints.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BC_bounded_no_overfit_repair_blueprints.md"
SELECTED_STATUS = bb.SELECTED_STATUS
STAGE_BRIEF = bb.STAGE_BRIEF
WORKSPACE_STATE = bb.WORKSPACE_STATE
CURRENT_STATE = bb.CURRENT_STATE
CHANGELOG = bb.CHANGELOG
RUN_REGISTRY = bb.RUN_REGISTRY
ALPHA_LEDGER = bb.ALPHA_LEDGER
ARTIFACT_REGISTRY = bb.ARTIFACT_REGISTRY
STAGE_LEDGER = bb.STAGE_LEDGER

RUN337BB_DIR = STAGE_DIR / "02_runs" / "run337BB"
RUN337BA_DIR = STAGE_DIR / "02_runs" / "run337BA"
RUN337AY_DIR = STAGE_DIR / "02_runs" / "run337AY"

BB_FINAL = RUN337BB_DIR / "final_decision.json"
BB_MANIFEST = RUN337BB_DIR / "run_manifest.json"
BB_FEATURE_REVIEW = RUN337BB_DIR / "feature_contract_review.csv"
BB_GATE_REVIEW = RUN337BB_DIR / "gate_contract_review.csv"
BB_PROXY_REVIEW = RUN337BB_DIR / "proxy_mt5_pairing_review.csv"
BB_NEGATIVE_REVIEW = RUN337BB_DIR / "negative_control_review.csv"
BB_FIREWALL = RUN337BB_DIR / "no_overfit_firewall_review.csv"
BB_USABILITY = RUN337BB_DIR / "bounded_repair_usability_matrix.csv"
BB_QUEUE = RUN337BB_DIR / "run337BC_blueprint_queue.csv"
BB_LINEAGE = RUN337BB_DIR / "input_lineage_review.csv"
BB_GATE_AUDIT = RUN337BB_DIR / "required_gate_coverage_audit.csv"
BA_FEATURE = RUN337BA_DIR / "feature_contract.csv"
BA_GATE = RUN337BA_DIR / "gate_contract.csv"
BA_PROXY = RUN337BA_DIR / "proxy_mt5_pairing_contract.csv"
BA_NEGATIVE = RUN337BA_DIR / "negative_control_plan.csv"
AY_FINAL = RUN337AY_DIR / "final_decision.json"
AY_PROTOCOL = RUN337AY_DIR / "protocol_attribution_matrix.csv"
AY_COST = RUN337AY_DIR / "cost_stress_report.csv"
AY_CURVE = RUN337AY_DIR / "curve_pocket_report.csv"
AY_PROXY = RUN337AY_DIR / "proxy_mt5_attribution_usability.csv"
AY_REGIME = RUN337AY_DIR / "shifted_custom_regime_attribution.csv"
CP322_PACKAGE_MANIFEST = ROOT / "stages" / "324_onnx_candidate_campaign__onnx_go_pressure_for_cp322a_adapter" / "01_inputs" / "adapter_package_manifest.json"
CP322_HASH_RECEIPT = ROOT / "stages" / "324_onnx_candidate_campaign__onnx_go_pressure_for_cp322a_adapter" / "01_inputs" / "adapter_package_hash_receipt.json"

BLUEPRINT_MATRIX = RUN_DIR / "bounded_repair_blueprint_matrix.csv"
FREEZE_CONTRACT = RUN_DIR / "cp322a_freeze_contract.csv"
EXECUTION_PROTOCOL = RUN_DIR / "bounded_execution_protocol_matrix.csv"
FALSIFICATION_MATRIX = RUN_DIR / "blueprint_falsification_gate_matrix.csv"
PROXY_MT5_PLAN = RUN_DIR / "proxy_mt5_blueprint_measurement_plan.csv"
SOURCE_IDENTITY = RUN_DIR / "blueprint_source_identity.csv"
RUN337BD_QUEUE = RUN_DIR / "run337BD_review_queue.csv"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BB_FINAL,
    BB_MANIFEST,
    BB_FEATURE_REVIEW,
    BB_GATE_REVIEW,
    BB_PROXY_REVIEW,
    BB_NEGATIVE_REVIEW,
    BB_FIREWALL,
    BB_USABILITY,
    BB_QUEUE,
    BB_LINEAGE,
    BB_GATE_AUDIT,
    BA_FEATURE,
    BA_GATE,
    BA_PROXY,
    BA_NEGATIVE,
    AY_FINAL,
    AY_PROTOCOL,
    AY_COST,
    AY_CURVE,
    AY_PROXY,
    AY_REGIME,
    CP322_PACKAGE_MANIFEST,
    CP322_HASH_RECEIPT,
)
OUTPUT_FILES = (
    BLUEPRINT_MATRIX,
    FREEZE_CONTRACT,
    EXECUTION_PROTOCOL,
    FALSIFICATION_MATRIX,
    PROXY_MT5_PLAN,
    SOURCE_IDENTITY,
    RUN337BD_QUEUE,
    REQUIRED_GATE_AUDIT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    FINAL_DECISION,
    RUN_MANIFEST,
)
REQUIRED_DESIGN_ORDER = (
    "az_defensive_cost_margin_objective",
    "az_repair_direction_balance_surface",
    "az_aggressive_density_preservation",
    "az_repair_curve_pocket_state_veto",
    "az_control_proxy_mt5_dual_read",
)

BLUEPRINT_COLUMNS = (
    "blueprint_id",
    "source_design_id",
    "blueprint_family",
    "repair_axis",
    "allowed_inputs",
    "frozen_items",
    "mutable_items",
    "success_evidence",
    "failure_evidence",
    "negative_controls",
    "proxy_mt5_rule",
    "overfit_rejection_rule",
    "next_review_gate",
    "status",
    "effect",
    "claim_boundary",
)
FREEZE_COLUMNS = (
    "freeze_id",
    "subject",
    "source_identity",
    "hash_or_value",
    "freeze_status",
    "forbidden_change",
    "effect",
    "claim_boundary",
)
EXECUTION_COLUMNS = (
    "protocol_id",
    "source_blueprint_id",
    "execution_family",
    "required_artifacts",
    "preflight_checks",
    "measurement_scope",
    "allowed_decision_use",
    "invalid_if",
    "next_run_owner",
    "status",
    "effect",
    "claim_boundary",
)
FALSIFICATION_COLUMNS = (
    "gate_id",
    "source_blueprint_id",
    "gate_family",
    "must_pass",
    "must_fail_or_abort_if",
    "evidence_artifact",
    "blocks_overfit_path",
    "status",
    "effect",
    "claim_boundary",
)
PROXY_PLAN_COLUMNS = (
    "plan_id",
    "source_blueprint_id",
    "proxy_artifact",
    "mt5_artifact",
    "join_key",
    "proxy_allowed_use",
    "mt5_required_use",
    "mismatch_action",
    "not_allowed_use",
    "status",
    "effect",
    "claim_boundary",
)
SOURCE_COLUMNS = (
    "source_id",
    "path",
    "exists",
    "row_count",
    "sha256",
    "used_for",
    "status",
    "claim_boundary",
)
QUEUE_COLUMNS = (
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
GATE_COLUMNS = aw.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def row_count(path: Path) -> int:
    if not aw.path_exists(path):
        return 0
    if path.suffix.lower() == ".json":
        return len(aw.read_json(path))
    return len(aw.read_csv(path))


def path_from_repo(raw: str) -> Path:
    return ROOT / str(raw or "").strip().replace("/", "\\")


def status_text(ok: bool) -> str:
    return "passed" if ok else "failed"


def require_inputs() -> None:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError("missing run337BC inputs: " + "; ".join(missing))


def load_inputs() -> dict[str, Any]:
    require_inputs()
    return {
        "bb_final": aw.read_json(BB_FINAL),
        "bb_manifest": aw.read_json(BB_MANIFEST),
        "feature_review": aw.read_csv(BB_FEATURE_REVIEW),
        "gate_review": aw.read_csv(BB_GATE_REVIEW),
        "proxy_review": aw.read_csv(BB_PROXY_REVIEW),
        "negative_review": aw.read_csv(BB_NEGATIVE_REVIEW),
        "firewall": aw.read_csv(BB_FIREWALL),
        "usability": aw.read_csv(BB_USABILITY),
        "queue": aw.read_csv(BB_QUEUE),
        "lineage": aw.read_csv(BB_LINEAGE),
        "bb_gate_audit": aw.read_csv(BB_GATE_AUDIT),
        "ba_feature": aw.read_csv(BA_FEATURE),
        "ba_gate": aw.read_csv(BA_GATE),
        "ba_proxy": aw.read_csv(BA_PROXY),
        "ba_negative": aw.read_csv(BA_NEGATIVE),
        "ay_final": aw.read_json(AY_FINAL),
        "ay_protocol": aw.read_csv(AY_PROTOCOL),
        "ay_cost": aw.read_csv(AY_COST),
        "ay_curve": aw.read_csv(AY_CURVE),
        "ay_proxy": aw.read_csv(AY_PROXY),
        "ay_regime": aw.read_csv(AY_REGIME),
        "cp322_manifest": aw.read_json(CP322_PACKAGE_MANIFEST),
        "cp322_hash": aw.read_json(CP322_HASH_RECEIPT),
    }


def by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {str(row.get(key, "")): dict(row) for row in rows}


def package_identity(src: Mapping[str, Any]) -> dict[str, str]:
    manifest = src["cp322_manifest"]
    receipt = src["cp322_hash"]
    snapshot = manifest.get("source_handoff_snapshot", {})
    risk = snapshot.get("risk_logic", {}) if isinstance(snapshot, Mapping) else {}
    return {
        "selected_candidate": str(manifest.get("selected_candidate", "cp322A_cp321b_exact_replay_control_surface")),
        "adapter_package": str(manifest.get("adapter_package_id", "")),
        "package_hash": str(receipt.get("package_hash", "")),
        "model_feature_order_hash": str(snapshot.get("model_feature_order_hash", "")),
        "runtime_feature_order_hash": str(snapshot.get("runtime_feature_order_hash", "")),
        "direction_surface_hash": str(snapshot.get("direction_surface_hash", "")),
        "handoff_hash": str(risk.get("handoff_hash", "")),
        "fixed_lot": str(risk.get("fixed_lot", "")),
        "atr_stop_multiplier": str(risk.get("atr_stop_multiplier", "")),
        "atr_take_profit_multiplier": str(risk.get("atr_take_profit_multiplier", "")),
    }


def build_blueprints(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    queue_by_design = by_key(src["queue"], "source_design_id")
    feature_by_design = by_key(src["ba_feature"], "design_id")
    usability_by_design = by_key(src["usability"], "design_id")
    rows: list[dict[str, Any]] = []
    axis_by_design = {
        "az_defensive_cost_margin_objective": "cost_margin(비용 마진)",
        "az_repair_direction_balance_surface": "side_balance(방향 균형)",
        "az_aggressive_density_preservation": "trade_density(거래 밀도)",
        "az_repair_curve_pocket_state_veto": "curve_state(곡선 상태)",
        "az_control_proxy_mt5_dual_read": "proxy_mt5_boundary(프록시-MT5 경계)",
    }
    for index, design_id in enumerate(REQUIRED_DESIGN_ORDER, start=1):
        queue = queue_by_design.get(design_id, {})
        feature = feature_by_design.get(design_id, {})
        usability = usability_by_design.get(design_id, {})
        rows.append(
            {
                "blueprint_id": f"bc_blueprint_{index:02d}",
                "source_design_id": design_id,
                "blueprint_family": queue.get("blueprint_family", usability.get("required_next_blueprint", "")),
                "repair_axis": axis_by_design.get(design_id, "unknown(미상)"),
                "allowed_inputs": feature.get("allowed_sources", "") + ";" + aw.rel(BB_USABILITY),
                "frozen_items": "cp322A ONNX, feature order, D/B surface, score threshold, risk logic, lot, ATR SL/TP, runtime handoff(322A 온엑스/피처 순서/D-B 표면/점수 임계값/위험 로직/로트/ATR 손절익절/런타임 인계)",
                "mutable_items": "blueprint text and future review queue only(청사진 문서와 미래 검토 대기열만)",
                "success_evidence": queue.get("predeclared_success_evidence", ""),
                "failure_evidence": queue.get("predeclared_failure_evidence", ""),
                "negative_controls": queue.get("negative_controls", aw.rel(BB_NEGATIVE_REVIEW)),
                "proxy_mt5_rule": "proxy checks signal/mismatch only; MT5 owns KPI(프록시는 신호/불일치 점검만, MT5가 KPI 담당)",
                "overfit_rejection_rule": usability.get("must_reject_if", queue.get("predeclared_failure_evidence", "")),
                "next_review_gate": NEXT_RUN_ID,
                "status": "materialized_blueprint_for_review(검토용 청사진 물질화)",
                "effect": "turns reviewed inputs into bounded repair work without selecting parameters(검토 입력을 파라미터 선택 없는 제한 수리 작업으로 바꿈)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_freeze_contract(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    identity = package_identity(src)
    rows = [
        ("cp322_candidate", "selected_candidate(선택 후보)", identity["selected_candidate"], identity["package_hash"], "candidate replacement(후보 교체)"),
        ("adapter_package", "adapter_package(어댑터 패키지)", identity["adapter_package"], identity["package_hash"], "adapter/package rewrite(어댑터/패키지 재작성)"),
        ("feature_order", "feature_order(피처 순서)", "model/runtime feature order hash(모델/런타임 피처 순서 해시)", identity["model_feature_order_hash"] + ";" + identity["runtime_feature_order_hash"], "feature order change(피처 순서 변경)"),
        ("decision_surface", "D/B decision surface(D/B 결정 표면)", "direction surface hash(방향 표면 해시)", identity["direction_surface_hash"], "D/B rule rewrite(D/B 규칙 재작성)"),
        ("score_threshold", "score threshold(점수 임계값)", "frozen adapter decision surface(고정 어댑터 결정 표면)", "no threshold retune in run337BC(337BC 임계값 재조정 없음)", "threshold search(임계값 탐색)"),
        ("risk_logic", "risk logic(위험 로직)", "runtime handoff risk logic(런타임 인계 위험 로직)", identity["handoff_hash"], "risk logic change(위험 로직 변경)"),
        ("lot_logic", "lot logic(로트 로직)", "fixed_lot(고정 로트)", identity["fixed_lot"], "lot optimization(로트 최적화)"),
        ("atr_sltp", "ATR SL/TP(ATR 손절/익절)", "ATR multipliers(ATR 배수)", identity["atr_stop_multiplier"] + "/" + identity["atr_take_profit_multiplier"], "ATR SL/TP retune(ATR 손절/익절 재조정)"),
        ("runtime_handoff", "runtime handoff(런타임 인계)", "handoff hash(인계 해시)", identity["handoff_hash"], "runtime handoff rewrite(런타임 인계 재작성)"),
    ]
    return [
        {
            "freeze_id": freeze_id,
            "subject": subject,
            "source_identity": source_identity,
            "hash_or_value": hash_or_value,
            "freeze_status": "frozen_not_modified(고정, 수정 없음)",
            "forbidden_change": forbidden_change,
            "effect": "keeps repair blueprint from becoming a new candidate or retune(수리 청사진이 새 후보나 재튜닝이 되는 것을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for freeze_id, subject, source_identity, hash_or_value, forbidden_change in rows
    ]


def build_execution_protocols(blueprints: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in blueprints:
        blueprint_id = str(item.get("blueprint_id", ""))
        rows.append(
            {
                "protocol_id": f"{blueprint_id}_protocol",
                "source_blueprint_id": blueprint_id,
                "execution_family": "bounded_repair_probe_design_only(제한 수리 탐침 설계 전용)",
                "required_artifacts": aw.rel(BLUEPRINT_MATRIX) + ";" + aw.rel(FREEZE_CONTRACT) + ";" + aw.rel(PROXY_MT5_PLAN),
                "preflight_checks": "freeze contract, no-lookahead gate, proxy-MT5 boundary, negative controls(고정 계약/미래참조 방지 게이트/프록시-MT5 경계/부정 대조)",
                "measurement_scope": "future MT5 KPI, proxy mismatch, cost stress, curve pocket, trade density(미래 MT5 KPI/프록시 불일치/비용 압박/곡선 포켓/거래 밀도)",
                "allowed_decision_use": "open review and later implementation design only(검토와 이후 구현 설계만 허용)",
                "invalid_if": "training or threshold/lot/D-B/date/trade-index selection appears(학습 또는 임계값/로트/D-B/날짜/거래번호 선택 등장)",
                "next_run_owner": NEXT_RUN_ID,
                "status": "protocol_materialized_for_review(검토용 절차 물질화)",
                "effect": "makes next repair measurable before implementation(다음 수리를 구현 전에 측정 가능하게 만듦)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_falsification_matrix(blueprints: Sequence[Mapping[str, Any]], src: Mapping[str, Any]) -> list[dict[str, Any]]:
    gate_rows = src["gate_review"]
    rows: list[dict[str, Any]] = []
    for item in blueprints:
        blueprint_id = str(item.get("blueprint_id", ""))
        for gate in gate_rows:
            gate_id = str(gate.get("source_gate_id", ""))
            rows.append(
                {
                    "gate_id": f"{blueprint_id}_{gate_id}",
                    "source_blueprint_id": blueprint_id,
                    "gate_family": gate.get("gate_family", ""),
                    "must_pass": gate.get("artifact_to_check", "") + " remains available and gate condition is predeclared(산출물 가용성과 사전 선언 게이트 유지)",
                    "must_fail_or_abort_if": gate.get("fail_condition_present", "") + "; any forbidden change appears(금지 변경 등장 시 중단)",
                    "evidence_artifact": aw.rel(REQUIRED_GATE_AUDIT),
                    "blocks_overfit_path": "threshold/lot/D-B/date/trade-index/proxy-KPI shortcut(임계값/로트/D-B/날짜/거래번호/프록시-KPI 지름길)",
                    "status": "materialized_falsification_gate(반증 게이트 물질화)",
                    "effect": "requires each blueprint to survive the same anti-overfit gate set(각 청사진이 같은 과적합 방지 게이트를 통과하게 함)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_proxy_plan(blueprints: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "plan_id": f"{item.get('blueprint_id')}_proxy_mt5_plan",
            "source_blueprint_id": item.get("blueprint_id", ""),
            "proxy_artifact": aw.rel(AY_PROXY),
            "mt5_artifact": aw.rel(AY_PROTOCOL),
            "join_key": "decision_timestamp_exact_or_trade_identity(정확 결정 시각 또는 거래 정체성)",
            "proxy_allowed_use": "schema, signal sanity, mismatch detection(스키마/신호 점검/불일치 탐지)",
            "mt5_required_use": "profit, PF, drawdown, expectancy, trade count KPI(수익/PF/손실폭/기대값/거래수 KPI)",
            "mismatch_action": "abort forward claim and open parity repair(전진 주장 중단 후 동등성 수리 개방)",
            "not_allowed_use": "proxy net/PF/DD as Forward Passed or Forward Failed(프록시 순익/PF/DD를 전진 통과 또는 실패로 사용)",
            "status": "proxy_mt5_measurement_plan_materialized(프록시-MT5 측정 계획 물질화)",
            "effect": "keeps proxy useful while preventing proxy authority(프록시는 유용하게 쓰되 권위가 되지 못하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for item in blueprints
    ]


def build_source_identity() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        exists = aw.path_exists(path)
        rows.append(
            {
                "source_id": path.stem,
                "path": aw.rel(path),
                "exists": str(exists).lower(),
                "row_count": row_count(path),
                "sha256": aw.sha256_file(path) if exists else "",
                "used_for": "run337BC bounded blueprint materialization(337BC 제한 청사진 물질화)",
                "status": "connected(연결)" if exists else "missing(누락)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_review_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BD_review_bounded_blueprints",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "run337BC bounded no-overfit repair blueprints(337BC 제한 무과적합 수리 청사진)",
            "inputs_to_review": ";".join(
                [
                    aw.rel(BLUEPRINT_MATRIX),
                    aw.rel(FREEZE_CONTRACT),
                    aw.rel(EXECUTION_PROTOCOL),
                    aw.rel(FALSIFICATION_MATRIX),
                    aw.rel(PROXY_MT5_PLAN),
                ]
            ),
            "must_confirm": "cp322A freeze, no retune, no proxy KPI authority, falsification gates complete(322A 고정/재조정 없음/프록시 KPI 권위 없음/반증 게이트 완성)",
            "must_reject_if": "candidate selection, training, threshold/lot/D-B/date/trade-index rule appears(후보 선택/학습/임계값/로트/D-B/날짜/거래번호 규칙 등장)",
            "expected_outputs": "review matrix, implementation boundary, next execution queue(검토 행렬/구현 경계/다음 실행 대기열)",
            "priority": "P0",
            "effect": "prevents blueprint materialization from silently becoming implementation(청사진 물질화가 몰래 구현이 되는 것을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(
    src: Mapping[str, Any],
    blueprints: Sequence[Mapping[str, Any]],
    freezes: Sequence[Mapping[str, Any]],
    protocols: Sequence[Mapping[str, Any]],
    falsification: Sequence[Mapping[str, Any]],
    proxy_plan: Sequence[Mapping[str, Any]],
    sources: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parent_gates_passed = sum(1 for row in src["bb_gate_audit"] if row.get("status") == "passed")
    freeze_ok = all(row.get("freeze_status", "").startswith("frozen") for row in freezes)
    forbidden_text = " ".join(str(row) for row in blueprints + protocols + falsification + proxy_plan).lower()
    no_forbidden = all(
        token not in forbidden_text
        for token in ("selected_candidate:", "threshold_search_enabled", "lot_optimization_enabled", "forward_passed: true")
    )
    proxy_ok = all("proxy net" in str(row.get("not_allowed_use", "")).lower() or "프록시" in str(row.get("not_allowed_use", "")) for row in proxy_plan)
    gates = [
        ("bc_gate_parent_review_loaded", bool(src["bb_final"]) and len(src["queue"]) == 5, f"queue={len(src['queue'])};final={bool(src['bb_final'])}", "run337BB review inputs loaded(337BB 검토 입력 로드)"),
        ("bc_gate_parent_gates_inherited", parent_gates_passed == len(src["bb_gate_audit"]) and parent_gates_passed > 0, f"parent_gates={parent_gates_passed}/{len(src['bb_gate_audit'])}", "run337BB gates passed(337BB 게이트 통과)"),
        ("bc_gate_blueprints_materialized", len(blueprints) == 5, f"blueprints={len(blueprints)}", "five blueprints materialized(청사진 5개 물질화)"),
        ("bc_gate_cp322a_freeze_contract", len(freezes) >= 9 and freeze_ok, f"freeze_rows={len(freezes)};freeze_ok={freeze_ok}", "cp322A fixed surface contract present(322A 고정 표면 계약 존재)"),
        ("bc_gate_protocols_materialized", len(protocols) == len(blueprints), f"protocols={len(protocols)}", "each blueprint has protocol(각 청사진 절차 존재)"),
        ("bc_gate_falsification_complete", len(falsification) >= len(blueprints) * 6, f"falsification={len(falsification)}", "all blueprint gates materialized(청사진 게이트 모두 물질화)"),
        ("bc_gate_proxy_mt5_plan_bounded", len(proxy_plan) == len(blueprints) and proxy_ok, f"proxy_plan={len(proxy_plan)};proxy_ok={proxy_ok}", "proxy remains non-KPI authority(프록시는 KPI 권위 아님)"),
        ("bc_gate_source_identity_connected", all(row.get("status") == "connected(연결)" for row in sources), f"sources={len(sources)}", "all source inputs connected(모든 원천 입력 연결)"),
        ("bc_gate_review_queue_ready", len(queue) == 1 and queue[0].get("next_run_id") == NEXT_RUN_ID, f"queue={len(queue)};next={NEXT_RUN_ID}", "run337BD review queue ready(337BD 검토 대기열 준비)"),
        ("bc_gate_no_training_selection_claim_guard", no_forbidden and src["bb_final"].get("goal_achieve") == "not_claimed", "no training, no retune, no selection, no Forward/Goal claim(학습/재조정/선택/전진/목표 주장 없음)", "claim boundary preserved(주장 경계 보존)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": status_text(ok),
            "observed": observed,
            "expected": expected,
            "effect": "blocks run337BD unless blueprint package is bounded and reviewable(청사진 패키지가 제한되고 검토 가능할 때만 337BD를 엶)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in gates
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    receipts = [
        (
            EXPERIMENT_RECEIPT,
            {
                "hypothesis": "reviewed repair inputs can become bounded blueprints without retuning cp322A(검토된 수리 입력을 322A 재조정 없이 제한 청사진으로 바꿀 수 있다)",
                "decision_use": "open run337BD review only(337BD 검토만 개방)",
                "control_variables": "cp322A package, ONNX, feature order, threshold, D/B surface, risk, lot, ATR SL/TP, runtime handoff fixed(322A 패키지/온엑스/피처 순서/임계값/D-B 표면/위험/로트/ATR 손절익절/런타임 인계 고정)",
                "changed_variables": "blueprint documents and review queue only(청사진 문서와 검토 대기열만 변경)",
                "success_criteria": "blueprints cover five axes and all gates pass(청사진 5개 축 포함 및 모든 게이트 통과)",
                "failure_criteria": "any blueprint permits training, retune, proxy KPI, or date-pocket memorization(청사진이 학습/재조정/프록시 KPI/날짜 포켓 암기를 허용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [aw.rel(path) for path in INPUT_FILES],
                "time_axis": "decision-time/pre-trade/as-of evidence only(결정 시점/진입 전/시점 기준 근거만)",
                "sample_scope": "run337BB reviewed inputs and run337AY diagnostic attribution(337BB 검토 입력과 337AY 진단 귀속)",
                "feature_label_boundary": "blueprints forbid post-trade realized profit, drawdown, date pocket, and trade index as features(청사진은 사후 실현 수익/손실/날짜 포켓/거래번호 피처 금지)",
                "integrity_judgment": "usable_with_boundary_for_blueprint_only(청사진 경계 안에서만 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "cp322A frozen ONNX and adapter package(322A 고정 온엑스와 어댑터 패키지)",
                "threshold_policy": "fixed, searched nowhere in run337BC(고정, 337BC에서 탐색 없음)",
                "overfit_risk": "repair could memorize shifted fragility if date/trade-index enters(날짜/거래번호가 들어가면 수리가 이동 취약성을 외울 위험)",
                "validation_judgment": "blueprint_only_not_candidate(청사진 전용, 후보 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": aw.rel(__file__),
                "runtime_path": "not modified in run337BC(337BC에서 수정 없음)",
                "shared_contract": "proxy mismatch check plus MT5 KPI authority(프록시 불일치 점검과 MT5 KPI 권위)",
                "parity_check": aw.rel(PROXY_MT5_PLAN),
                "runtime_claim_boundary": "research-only, no runtime authority(연구 전용, 런타임 권위 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [aw.rel(path) for path in INPUT_FILES],
                "producer": aw.rel(__file__),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [aw.rel(path) for path in OUTPUT_FILES],
                "registry_links": [aw.rel(RUN_REGISTRY), aw.rel(ALPHA_LEDGER), aw.rel(STAGE_LEDGER), aw.rel(ARTIFACT_REGISTRY)],
                "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [aw.rel(BLUEPRINT_MATRIX), aw.rel(FREEZE_CONTRACT), aw.rel(REQUIRED_GATE_AUDIT)],
                "evidence_missing": "no implementation, no MT5 forward retest, no new ONNX, no runtime authority(구현 없음/MT5 전진 재시험 없음/신규 온엑스 없음/런타임 권위 없음)",
                "judgment_label": "blueprint_materialized_for_review(검토용 청사진 물질화)",
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    paths: list[Path] = []
    for path, payload in receipts:
        paths.append(aw.write_json(path, payload))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BC Bounded No-Overfit Repair Blueprints(337단계 337BC 제한 무과적합 수리 청사진)

## Conclusion(결론)

run337BC(337BC 실행)는 run337BB(337BB 실행)가 승인한 5개 repair axis(수리 축)를 bounded blueprint(제한 청사진)로 물질화했다.

Effect(효과): 다음 run337BD(337BD 실행)는 이 청사진이 실제 구현으로 넘어가도 과적합, proxy authority(프록시 권위), threshold retune(임계값 재조정), lot optimization(로트 최적화)을 만들지 않는지 검토한다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- blueprints(청사진): `{final['blueprint_rows']}`
- freeze_contract_rows(고정 계약 행): `{final['freeze_rows']}`
- execution_protocols(실행 절차): `{final['protocol_rows']}`
- falsification_gates(반증 게이트): `{final['falsification_rows']}`
- proxy_mt5_plans(프록시-MT5 계획): `{final['proxy_plan_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Plain Meaning(쉬운 의미)

이번 실행은 모델을 고친 것이 아니다. 고치기 전에 “어디까지는 허용, 어디부터는 과적합”인지 청사진으로 박아 둔 것이다.

Effect(효과): 수리 실험이 좋은 숫자에 맞춰 임계값(threshold, 임계값), 로트(lot, 로트), D/B rule(D/B 규칙), 날짜 포켓(date pocket, 날짜 포켓)을 바꾸는 길을 막는다.

## Boundary(경계)

cp322A(322A 후보)의 ONNX(온엑스), feature order(피처 순서), D/B surface(D/B 표면), score threshold(점수 임계값), risk logic(위험 로직), lot logic(로트 로직), ATR SL/TP(ATR 손절/익절), runtime handoff(런타임 인계)는 고정이다.

## Next Action(다음 행동)

- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337BC

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

run337BC(337BC 실행)는 bounded blueprint materialization(제한 청사진 물질화)만 수행했다. cp322A(322A 후보)는 고정이고, model training(모델 학습), threshold retune(임계값 재조정), D/B rewrite(D/B 재작성), lot optimization(로트 최적화), candidate selection(후보 선택)은 없다.

Effect(효과): 다음 작업은 run337BD(337BD 실행) 청사진 검토이며, Forward/Goal(전진/목표)은 계속 주장하지 않는다.
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
    workspace, workspace_bom = aw.read_tracked_text_lossless(WORKSPACE_STATE)
    workspace = aw.replace_prefix_line(workspace, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337BC focus complete: run337BC(337BC 실행)은 `{final['status']}`로 bounded no-overfit repair blueprints(제한 무과적합 수리 청사진)를 물질화했다. Effect(효과): blueprints(청사진) `{final['blueprint_rows']}`, freeze rows(고정 행) `{final['freeze_rows']}`, falsification gates(반증 게이트) `{final['falsification_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    workspace = insert_current_focus(workspace, focus)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

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
## Stage337 run337BC(337BC 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BC(337BC 실행)는 run337BB(337BB 실행)의 5개 제한 수리 축을 청사진/고정 계약/반증 게이트/proxy-MT5(프록시-MT5) 계획으로 물질화했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337BC" not in current:
        current = current.replace("## Stage337 run337BB", section + "\n## Stage337 run337BB", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- blueprint_rows(청사진 행): `{final['blueprint_rows']}`
- freeze_contract_rows(고정 계약 행): `{final['freeze_rows']}`
- falsification_gate_rows(반증 게이트 행): `{final['falsification_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_review_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337BC(337BC 실행)는 청사진만 만들었고 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = aw.replace_prefix_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337BC_summary(337BC 요약): `{final['status']}`. "
        f"Effect(효과): bounded blueprints(제한 청사진) `{final['blueprint_rows']}`, cp322A freeze contracts(322A 고정 계약) `{final['freeze_rows']}`, falsification gates(반증 게이트) `{final['falsification_rows']}`를 만들고 run337BD(337BD 실행) 검토를 연다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337BC_summary" not in brief:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337BC(337BC 실행) `{final['status']}`. "
        f"Effect(효과): cp322A(322A 후보)를 고정한 bounded no-overfit repair blueprint(제한 무과적합 수리 청사진)을 물질화하고 Forward/Goal(전진/목표)은 주장하지 않음."
    )
    if "Stage337 run337BC" not in changelog:
        changelog = changelog.rstrip() + "\n" + line + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "bounded_no_overfit_repair_blueprint_materialization_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "family": "experiment_execution",
        "primary_report": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__bounded_blueprints",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "bounded_no_overfit_repair_blueprints",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "bounded_no_overfit_repair_blueprints_without_db(D/B 없는 제한 무과적합 수리 청사진)",
        "tier_scope": "Tier A shifted/completed diagnostic evidence with cp322A frozen subject(Tier A 이동/완성 진단 근거와 322A 고정 대상)",
        "kpi_scope": "blueprint_no_new_trading_kpi(청사진, 신규 거래 KPI 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"blueprints={final['blueprint_rows']};freeze={final['freeze_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "guardrail_kpi": "cp322a_frozen;no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim_blueprint_only(주장 범위 밖, 청사진 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__bounded_blueprints",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "run337BB reviewed input contracts and cp322A package identity",
        "kpi_scope": "blueprint_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__bounded_blueprints",
        "family": "bounded_no_overfit_repair_blueprint_materialization_without_db",
        "question": "can reviewed repair inputs become cp322A-frozen bounded repair blueprints",
        "metric_scope": "blueprint_freeze_falsification_proxy_boundary",
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
    src = load_inputs()
    blueprints = build_blueprints(src)
    blueprint_path = aw.write_csv(BLUEPRINT_MATRIX, BLUEPRINT_COLUMNS, blueprints)
    freezes = build_freeze_contract(src)
    freeze_path = aw.write_csv(FREEZE_CONTRACT, FREEZE_COLUMNS, freezes)
    protocols = build_execution_protocols(blueprints)
    protocol_path = aw.write_csv(EXECUTION_PROTOCOL, EXECUTION_COLUMNS, protocols)
    falsification = build_falsification_matrix(blueprints, src)
    falsification_path = aw.write_csv(FALSIFICATION_MATRIX, FALSIFICATION_COLUMNS, falsification)
    proxy_plan = build_proxy_plan(blueprints)
    proxy_path = aw.write_csv(PROXY_MT5_PLAN, PROXY_PLAN_COLUMNS, proxy_plan)
    source_rows = build_source_identity()
    source_path = aw.write_csv(SOURCE_IDENTITY, SOURCE_COLUMNS, source_rows)
    review_queue = build_review_queue()
    queue_path = aw.write_csv(RUN337BD_QUEUE, QUEUE_COLUMNS, review_queue)
    gate_rows = build_gates(src, blueprints, freezes, protocols, falsification, proxy_plan, source_rows, review_queue)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BC_bounded_blueprint_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all_gates_pass else "bounded_blueprint_materialization_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BC_blueprint_materialization_before_review",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BC_blueprint_materialization_gate_failure_v1",
        "blueprint_rows": len(blueprints),
        "freeze_rows": len(freezes),
        "protocol_rows": len(protocols),
        "falsification_rows": len(falsification),
        "proxy_plan_rows": len(proxy_plan),
        "source_rows": len(source_rows),
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
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        blueprint_path,
        freeze_path,
        protocol_path,
        falsification_path,
        proxy_path,
        source_path,
        queue_path,
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
                "blueprints": final["blueprint_rows"],
                "freeze_contracts": final["freeze_rows"],
                "falsification_gates": final["falsification_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "report": aw.rel(report_path),
                "artifact_registry": aw.rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
