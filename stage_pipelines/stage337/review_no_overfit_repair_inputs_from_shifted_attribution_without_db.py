from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import materialize_no_overfit_repair_inputs_from_shifted_attribution_without_db as ba


aw = ba.aw

TODAY = "2026-05-27"
STAGE_ID = ba.STAGE_ID
RUN_NUMBER = "run337BB"
RUN_ID = "run337BB_review_no_overfit_repair_inputs_from_shifted_attribution_without_db_v1"
PARENT_RUN_ID = ba.RUN_ID
NEXT_RUN_ID = "run337BC_materialize_bounded_no_overfit_repair_blueprints_from_reviewed_inputs_without_db_v1"
STATUS = "completed_stage337BB_no_overfit_repair_inputs_reviewed_ready_for_bounded_blueprint_no_training_no_selection"
JUDGMENT = "reviewed_inputs_can_open_bounded_repair_blueprint_but_forward_and_runtime_authority_unproven"
DECISION = "stage337BB_open_run337BC_materialize_bounded_no_overfit_repair_blueprints_without_db_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BB_no_overfit_repair_input_review_without_db_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ba.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ba.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BB_no_overfit_repair_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BB_no_overfit_repair_input_review.md"
SELECTED_STATUS = ba.SELECTED_STATUS
STAGE_BRIEF = ba.STAGE_BRIEF
WORKSPACE_STATE = ba.WORKSPACE_STATE
CURRENT_STATE = ba.CURRENT_STATE
CHANGELOG = ba.CHANGELOG
RUN_REGISTRY = ba.RUN_REGISTRY
ALPHA_LEDGER = ba.ALPHA_LEDGER
ARTIFACT_REGISTRY = ba.ARTIFACT_REGISTRY
STAGE_LEDGER = ba.STAGE_LEDGER

RUN337BA_DIR = STAGE_DIR / "02_runs" / "run337BA"
RUN337AY_DIR = STAGE_DIR / "02_runs" / "run337AY"

BA_FINAL = RUN337BA_DIR / "final_decision.json"
BA_MANIFEST = RUN337BA_DIR / "run_manifest.json"
BA_FEATURE = RUN337BA_DIR / "feature_contract.csv"
BA_GATE = RUN337BA_DIR / "gate_contract.csv"
BA_PROXY = RUN337BA_DIR / "proxy_mt5_pairing_contract.csv"
BA_NEGATIVE = RUN337BA_DIR / "negative_control_plan.csv"
BA_COST = RUN337BA_DIR / "cost_margin_feature_contract.csv"
BA_SIDE = RUN337BA_DIR / "side_balance_input_contract.csv"
BA_DENSITY = RUN337BA_DIR / "density_retention_contract.csv"
BA_CURVE = RUN337BA_DIR / "curve_state_veto_feature_map.csv"
BA_SOURCE_HASH = RUN337BA_DIR / "input_source_hash_matrix.csv"
BA_PACKAGE = RUN337BA_DIR / "materialized_input_package_manifest.csv"
BA_NO_LOOKAHEAD = RUN337BA_DIR / "no_lookahead_materialization_audit.csv"
BA_REVIEW_QUEUE = RUN337BA_DIR / "run337BB_review_queue.csv"
BA_GATE_AUDIT = RUN337BA_DIR / "required_gate_coverage_audit.csv"

AY_FINAL = RUN337AY_DIR / "final_decision.json"
AY_PROTOCOL = RUN337AY_DIR / "protocol_attribution_matrix.csv"
AY_PROXY = RUN337AY_DIR / "proxy_mt5_attribution_usability.csv"
AY_COST = RUN337AY_DIR / "cost_stress_report.csv"
AY_CURVE = RUN337AY_DIR / "curve_pocket_report.csv"
AY_REGIME = RUN337AY_DIR / "shifted_custom_regime_attribution.csv"
AY_SHIFTED_TRADES = RUN337AY_DIR / "shifted_custom_trade_records.csv"
AY_COMPLETED_TRADES = RUN337AY_DIR / "completed_day_anchor_trade_records.csv"

FEATURE_REVIEW = RUN_DIR / "feature_contract_review.csv"
GATE_REVIEW = RUN_DIR / "gate_contract_review.csv"
PROXY_REVIEW = RUN_DIR / "proxy_mt5_pairing_review.csv"
NEGATIVE_REVIEW = RUN_DIR / "negative_control_review.csv"
FIREWALL_REVIEW = RUN_DIR / "no_overfit_firewall_review.csv"
USABILITY_MATRIX = RUN_DIR / "bounded_repair_usability_matrix.csv"
RUN337BC_QUEUE = RUN_DIR / "run337BC_blueprint_queue.csv"
INPUT_LINEAGE_REVIEW = RUN_DIR / "input_lineage_review.csv"
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
    BA_FINAL,
    BA_MANIFEST,
    BA_FEATURE,
    BA_GATE,
    BA_PROXY,
    BA_NEGATIVE,
    BA_COST,
    BA_SIDE,
    BA_DENSITY,
    BA_CURVE,
    BA_SOURCE_HASH,
    BA_PACKAGE,
    BA_NO_LOOKAHEAD,
    BA_REVIEW_QUEUE,
    BA_GATE_AUDIT,
    AY_FINAL,
    AY_PROTOCOL,
    AY_PROXY,
    AY_COST,
    AY_CURVE,
    AY_REGIME,
    AY_SHIFTED_TRADES,
    AY_COMPLETED_TRADES,
)
OUTPUT_FILES = (
    FEATURE_REVIEW,
    GATE_REVIEW,
    PROXY_REVIEW,
    NEGATIVE_REVIEW,
    FIREWALL_REVIEW,
    USABILITY_MATRIX,
    RUN337BC_QUEUE,
    INPUT_LINEAGE_REVIEW,
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

REQUIRED_DESIGNS = {
    "az_defensive_cost_margin_objective",
    "az_repair_direction_balance_surface",
    "az_aggressive_density_preservation",
    "az_repair_curve_pocket_state_veto",
    "az_control_proxy_mt5_dual_read",
}
REQUIRED_GATES = {
    "az_gate_no_forward_threshold_search",
    "az_gate_proxy_mt5_dual_evidence",
    "az_gate_density_retention",
    "az_gate_cost_ladder",
    "az_gate_curve_pocket_out_of_sample",
    "az_gate_asof_data_integrity",
}

FEATURE_REVIEW_COLUMNS = (
    "contract_id",
    "design_id",
    "input_family",
    "allowed_source_count",
    "missing_allowed_sources",
    "timestamp_rule_status",
    "forbidden_source_status",
    "proxy_mt5_role_status",
    "review_gate_status",
    "review_status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
GATE_REVIEW_COLUMNS = (
    "contract_id",
    "source_gate_id",
    "gate_family",
    "artifact_to_check",
    "artifact_exists",
    "pass_condition_present",
    "fail_condition_present",
    "overfit_path_named",
    "review_status",
    "effect",
    "claim_boundary",
)
PROXY_REVIEW_COLUMNS = (
    "pairing_id",
    "subject",
    "proxy_artifact_exists",
    "mt5_runtime_artifact_exists",
    "proxy_rows",
    "proxy_matched_rows",
    "proxy_forward_usable_rows",
    "pairing_boundary_status",
    "review_status",
    "usable_for",
    "not_usable_for",
    "effect",
    "claim_boundary",
)
NEGATIVE_REVIEW_COLUMNS = (
    "control_id",
    "control_family",
    "active_guard_fields",
    "invalid_condition_present",
    "expected_failure_present",
    "forbidden_path_covered",
    "review_status",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "status",
    "evidence_path",
    "observed",
    "risk_checked",
    "effect",
    "claim_boundary",
)
USABILITY_COLUMNS = (
    "design_id",
    "review_contract",
    "input_usability",
    "required_next_blueprint",
    "must_keep_fixed",
    "must_reject_if",
    "evidence_basis",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "blueprint_family",
    "source_design_id",
    "required_inputs",
    "predeclared_success_evidence",
    "predeclared_failure_evidence",
    "negative_controls",
    "forbidden_actions",
    "priority",
    "effect",
    "claim_boundary",
)
LINEAGE_COLUMNS = (
    "source_id",
    "path",
    "exists",
    "row_count",
    "sha256",
    "hash_matches_parent_record",
    "review_status",
    "effect",
    "claim_boundary",
)
GATE_AUDIT_COLUMNS = aw.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def path_from_repo(raw: str) -> Path:
    text = str(raw or "").strip().replace("/", "\\")
    return ROOT / text


def split_paths(raw: str) -> list[Path]:
    return [path_from_repo(item.strip()) for item in str(raw or "").split(";") if item.strip()]


def row_count(path: Path) -> int:
    if not aw.path_exists(path):
        return 0
    if path.suffix.lower() == ".json":
        return len(aw.read_json(path))
    return len(aw.read_csv(path))


def csv_number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def yes_no(value: bool) -> str:
    return "true" if value else "false"


def status_text(ok: bool) -> str:
    return "passed" if ok else "failed"


def require_inputs() -> None:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError("missing run337BB inputs: " + "; ".join(missing))


def load_inputs() -> dict[str, Any]:
    require_inputs()
    return {
        "ba_final": aw.read_json(BA_FINAL),
        "ba_manifest": aw.read_json(BA_MANIFEST),
        "features": aw.read_csv(BA_FEATURE),
        "gates": aw.read_csv(BA_GATE),
        "proxy_pairs": aw.read_csv(BA_PROXY),
        "negative_controls": aw.read_csv(BA_NEGATIVE),
        "cost_contract": aw.read_csv(BA_COST),
        "side_contract": aw.read_csv(BA_SIDE),
        "density_contract": aw.read_csv(BA_DENSITY),
        "curve_contract": aw.read_csv(BA_CURVE),
        "source_hashes": aw.read_csv(BA_SOURCE_HASH),
        "package": aw.read_csv(BA_PACKAGE),
        "no_lookahead": aw.read_csv(BA_NO_LOOKAHEAD),
        "review_queue": aw.read_csv(BA_REVIEW_QUEUE),
        "ba_gate_audit": aw.read_csv(BA_GATE_AUDIT),
        "ay_final": aw.read_json(AY_FINAL),
        "ay_protocol": aw.read_csv(AY_PROTOCOL),
        "ay_proxy": aw.read_csv(AY_PROXY),
        "ay_cost": aw.read_csv(AY_COST),
        "ay_curve": aw.read_csv(AY_CURVE),
        "ay_regime": aw.read_csv(AY_REGIME),
        "ay_shifted_trades": aw.read_csv(AY_SHIFTED_TRADES),
        "ay_completed_trades": aw.read_csv(AY_COMPLETED_TRADES),
    }


def build_feature_review(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    gate_ids = {str(row.get("source_gate_id", "")) for row in src["gates"]}
    rows: list[dict[str, Any]] = []
    for feature in src["features"]:
        allowed_paths = split_paths(feature.get("allowed_sources", ""))
        missing = [aw.rel(path) for path in allowed_paths if not aw.path_exists(path)]
        timestamp_text = " ".join(
            str(feature.get(key, ""))
            for key in ("timestamp_rule", "split_rule", "materialized_input")
        ).lower()
        forbidden_text = str(feature.get("forbidden_sources", "")).lower()
        proxy_text = str(feature.get("proxy_mt5_role", "")).lower()
        gate_id = str(feature.get("review_gate", ""))
        timestamp_ok = any(
            token in timestamp_text
            for token in ("decision", "결정", "pre-trade", "진입 전", "prior", "as-of", "시점")
        )
        forbidden_ok = any(
            token in forbidden_text
            for token in (
                "threshold",
                "임계",
                "lot",
                "로트",
                "post-trade",
                "사후",
                "date",
                "trade index",
                "forward",
                "전진",
                "kpi",
                "proxy",
                "프록시",
            )
        )
        proxy_ok = "mt5" in proxy_text and any(
            token in proxy_text
            for token in (
                "proxy",
                "프록시",
                "cannot",
                "owns",
                "확인",
                "detect",
                "mismatch",
                "kpi",
                "런타임",
                "runtime",
            )
        )
        gate_ok = gate_id in gate_ids
        ok = not missing and timestamp_ok and forbidden_ok and proxy_ok and gate_ok
        rows.append(
            {
                "contract_id": feature.get("contract_id", ""),
                "design_id": feature.get("design_id", ""),
                "input_family": feature.get("input_family", ""),
                "allowed_source_count": len(allowed_paths),
                "missing_allowed_sources": ";".join(missing),
                "timestamp_rule_status": status_text(timestamp_ok),
                "forbidden_source_status": status_text(forbidden_ok),
                "proxy_mt5_role_status": status_text(proxy_ok),
                "review_gate_status": status_text(gate_ok),
                "review_status": "accepted_for_bounded_repair_blueprint(제한 수리 청사진에 사용 가능)" if ok else "rejected_until_contract_repaired(계약 수리 전 거부)",
                "allowed_use": "repair blueprint input only(수리 청사진 입력 전용)",
                "forbidden_use": "training, threshold search, lot change, D/B rewrite, forward decision(학습/임계값 탐색/로트 변경/D-B 재작성/전진 판정)",
                "effect": "keeps feature input predeclared before any new repair test(새 수리 시험 전 피처 입력을 사전 선언 상태로 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gate_review(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for gate in src["gates"]:
        artifact = path_from_repo(str(gate.get("artifact_to_check", "")))
        pass_present = bool(str(gate.get("pass_condition", "")).strip())
        fail_present = bool(str(gate.get("fail_condition", "")).strip())
        overfit_present = bool(str(gate.get("prevents_overfit_path", "")).strip())
        exists = aw.path_exists(artifact)
        ok = exists and pass_present and fail_present and overfit_present
        rows.append(
            {
                "contract_id": gate.get("contract_id", ""),
                "source_gate_id": gate.get("source_gate_id", ""),
                "gate_family": gate.get("gate_family", ""),
                "artifact_to_check": gate.get("artifact_to_check", ""),
                "artifact_exists": yes_no(exists),
                "pass_condition_present": yes_no(pass_present),
                "fail_condition_present": yes_no(fail_present),
                "overfit_path_named": yes_no(overfit_present),
                "review_status": "gate_contract_review_passed(게이트 계약 검토 통과)" if ok else "gate_contract_review_failed(게이트 계약 검토 실패)",
                "effect": "turns repair into falsifiable test instead of open-ended tuning(수리를 열린 튜닝이 아니라 반증 가능한 시험으로 바꿈)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_review(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    proxy_rows = src["ay_proxy"]
    proxy_count = sum(csv_number(row.get("proxy_rows")) for row in proxy_rows)
    matched_count = sum(csv_number(row.get("proxy_matched")) for row in proxy_rows)
    forward_usable = sum(1 for row in proxy_rows if str(row.get("usable_for_forward_decision", "")).lower() == "true")
    rows: list[dict[str, Any]] = []
    for pair in src["proxy_pairs"]:
        proxy_path = path_from_repo(str(pair.get("proxy_artifact", "")))
        mt5_path = path_from_repo(str(pair.get("mt5_runtime_artifact", "")))
        not_usable = str(pair.get("not_usable_for", ""))
        usable = str(pair.get("usable_for", ""))
        boundary_ok = (
            aw.path_exists(proxy_path)
            and aw.path_exists(mt5_path)
            and forward_usable == 0
            and matched_count == proxy_count
            and ("forward" in not_usable.lower() or "전진" in not_usable)
            and ("kpi" not in usable.lower() or "not" in not_usable.lower() or "전진" in not_usable)
        )
        rows.append(
            {
                "pairing_id": pair.get("pairing_id", ""),
                "subject": pair.get("subject", ""),
                "proxy_artifact_exists": yes_no(aw.path_exists(proxy_path)),
                "mt5_runtime_artifact_exists": yes_no(aw.path_exists(mt5_path)),
                "proxy_rows": int(proxy_count),
                "proxy_matched_rows": int(matched_count),
                "proxy_forward_usable_rows": int(forward_usable),
                "pairing_boundary_status": status_text(boundary_ok),
                "review_status": "proxy_usable_for_signal_and_attribution_only(프록시는 신호와 귀속 점검 전용)" if boundary_ok else "proxy_boundary_failed(프록시 경계 실패)",
                "usable_for": "schema/signal/parity sanity and mismatch detection(스키마/신호/동등성 점검과 불일치 탐지)",
                "not_usable_for": "Forward Passed/Failed or profitability KPI(전진 통과/실패 또는 수익성 KPI)",
                "effect": "keeps proxy from becoming a hidden forward result(프록시가 숨은 전진 결과가 되는 길을 막음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_negative_review(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    coverage_tokens = {
        "threshold": ("threshold", "임계"),
        "lot": ("lot", "로트"),
        "db": ("d/b", "d-b", "D/B", "D-B"),
        "date": ("date", "날짜"),
        "trade_index": ("trade index", "거래 번호"),
        "proxy": ("proxy", "프록시"),
    }
    for control in src["negative_controls"]:
        text = " ".join(str(control.get(key, "")) for key in control).lower()
        active_fields = sum(1 for key in ("materialized_check", "expected_failure_or_guard", "invalid_if") if str(control.get(key, "")).strip())
        invalid_present = bool(str(control.get("invalid_if", "")).strip())
        expected_present = bool(str(control.get("expected_failure_or_guard", "")).strip())
        covered = [
            name
            for name, tokens in coverage_tokens.items()
            if any(token.lower() in text for token in tokens)
        ]
        ok = active_fields == 3 and invalid_present and expected_present and bool(covered)
        rows.append(
            {
                "control_id": control.get("control_id", ""),
                "control_family": control.get("control_family", ""),
                "active_guard_fields": active_fields,
                "invalid_condition_present": yes_no(invalid_present),
                "expected_failure_present": yes_no(expected_present),
                "forbidden_path_covered": ",".join(covered),
                "review_status": "negative_control_active(부정 대조 활성)" if ok else "negative_control_incomplete(부정 대조 불완전)",
                "effect": "defines what must fail before a repair is trusted(수리를 믿기 전에 반드시 실패해야 할 길을 정의)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_firewall_review(
    src: Mapping[str, Any],
    feature_review: Sequence[Mapping[str, Any]],
    gate_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    negative_review: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    design_ids = {str(row.get("design_id", "")) for row in src["features"]}
    gate_ids = {str(row.get("source_gate_id", "")) for row in src["gates"]}
    ba_gates_passed = sum(1 for row in src["ba_gate_audit"] if row.get("status") == "passed")
    no_lookahead_passed = sum(1 for row in src["no_lookahead"] if row.get("status") == "passed")
    source_rows_exist = all(str(row.get("exists", "")).lower() == "true" for row in src["source_hashes"])
    feature_passed = sum(1 for row in feature_review if str(row.get("review_status", "")).startswith("accepted_"))
    gate_passed = sum(1 for row in gate_review if str(row.get("review_status", "")).startswith("gate_contract_review_passed"))
    proxy_passed = sum(1 for row in proxy_review if str(row.get("review_status", "")).startswith("proxy_usable"))
    negative_passed = sum(1 for row in negative_review if str(row.get("review_status", "")).startswith("negative_control_active"))
    final_text = json.dumps(src["ba_final"], ensure_ascii=False).lower()
    no_claim = all(
        token in final_text
        for token in ("not_claimed", "no_model_training", "no_threshold_retuning", "no_lot_optimization")
    )
    rows = [
        {
            "firewall_id": "bb_firewall_design_coverage",
            "status": status_text(design_ids == REQUIRED_DESIGNS),
            "evidence_path": aw.rel(BA_FEATURE),
            "observed": f"designs={len(design_ids)}/5",
            "risk_checked": "missing design silently drops a repair axis(누락 설계가 수리 축을 조용히 제거하는 위험)",
            "effect": "all cost/side/density/curve/proxy axes remain visible(비용/방향/밀도/곡선/프록시 축을 모두 보이게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "bb_firewall_gate_coverage",
            "status": status_text(gate_ids == REQUIRED_GATES and ba_gates_passed == len(src["ba_gate_audit"])),
            "evidence_path": aw.rel(BA_GATE_AUDIT),
            "observed": f"source_gates={len(gate_ids)}/6;parent_gates={ba_gates_passed}/{len(src['ba_gate_audit'])}",
            "risk_checked": "repair proceeds without falsification gate(반증 게이트 없이 수리 진행)",
            "effect": "next blueprint must keep pass/fail evidence explicit(다음 청사진이 통과/실패 근거를 명시하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "bb_firewall_no_lookahead_audit",
            "status": status_text(no_lookahead_passed == len(src["no_lookahead"]) and no_lookahead_passed > 0),
            "evidence_path": aw.rel(BA_NO_LOOKAHEAD),
            "observed": f"no_lookahead={no_lookahead_passed}/{len(src['no_lookahead'])}",
            "risk_checked": "future bar or shifted-result parameter enters features(미래 봉이나 이동 결과 파라미터가 피처에 들어가는 위험)",
            "effect": "keeps review on pre-trade/as-of inputs(검토를 진입 전/시점 기준 입력으로 제한)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "bb_firewall_proxy_boundary",
            "status": status_text(proxy_passed == len(proxy_review) and proxy_passed > 0),
            "evidence_path": aw.rel(PROXY_REVIEW),
            "observed": f"proxy_reviews={proxy_passed}/{len(proxy_review)}",
            "risk_checked": "proxy result becomes forward KPI(프록시 결과가 전진 KPI가 되는 위험)",
            "effect": "proxy remains sanity check and mismatch detector only(프록시는 점검과 불일치 탐지만 맡음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "bb_firewall_negative_controls",
            "status": status_text(negative_passed == len(negative_review) and negative_passed > 0),
            "evidence_path": aw.rel(NEGATIVE_REVIEW),
            "observed": f"negative_controls={negative_passed}/{len(negative_review)}",
            "risk_checked": "repair hides forbidden date/threshold/lot/D-B paths(수리가 금지된 날짜/임계값/로트/D-B 경로를 숨기는 위험)",
            "effect": "forbidden paths are named before blueprint generation(청사진 생성 전에 금지 경로를 이름 붙임)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "bb_firewall_source_lineage",
            "status": status_text(source_rows_exist and len(src["source_hashes"]) >= 17),
            "evidence_path": aw.rel(BA_SOURCE_HASH),
            "observed": f"sources={len(src['source_hashes'])};all_exist={source_rows_exist}",
            "risk_checked": "ledger points to missing ignored artifacts(장부가 누락된 무시 산출물을 가리키는 위험)",
            "effect": "ignored 02_runs artifacts remain reproducibly identified(무시된 02_runs 산출물을 재현 가능하게 식별)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "bb_firewall_claim_guard",
            "status": status_text(no_claim),
            "evidence_path": aw.rel(BA_FINAL),
            "observed": "Forward/Goal/runtime claims remain not_claimed(전진/목표/런타임 주장이 계속 미주장)",
            "risk_checked": "input review is overstated as model readiness(입력 검토를 모델 준비로 과장하는 위험)",
            "effect": "keeps this run below Forward Passed/Failed and runtime authority(이번 실행을 전진 통과/실패와 런타임 권위 아래에 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "bb_firewall_review_completeness",
            "status": status_text(feature_passed == len(feature_review) and gate_passed == len(gate_review)),
            "evidence_path": aw.rel(FEATURE_REVIEW) + ";" + aw.rel(GATE_REVIEW),
            "observed": f"feature={feature_passed}/{len(feature_review)};gate={gate_passed}/{len(gate_review)}",
            "risk_checked": "partial review opens blueprint too early(부분 검토가 청사진을 너무 일찍 여는 위험)",
            "effect": "opens run337BC only after all contract reviews pass(모든 계약 검토가 통과한 뒤에만 run337BC를 엶)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def build_usability_matrix(src: Mapping[str, Any], feature_review: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    review_by_design = {str(row.get("design_id", "")): row for row in feature_review}
    shifted_trades = len(src["ay_shifted_trades"])
    completed_trades = len(src["ay_completed_trades"])
    cost_fragile = any("fragile" in str(row.get("stress_status", "")).lower() for row in src["ay_cost"])
    curve_rows = len(src["ay_curve"])
    return [
        {
            "design_id": "az_defensive_cost_margin_objective",
            "review_contract": review_by_design.get("az_defensive_cost_margin_objective", {}).get("contract_id", ""),
            "input_usability": "usable_as_objective_constraint(목표 제약으로 사용 가능)",
            "required_next_blueprint": "cost margin feature and cost-stress fail ladder(비용 마진 피처와 비용 압박 실패 사다리)",
            "must_keep_fixed": "existing ONNX/threshold/lot/risk; no shifted KPI parameter search(기존 ONNX/임계값/로트/위험 고정, 이동 KPI 파라미터 탐색 금지)",
            "must_reject_if": "0.5pt cost stress is optimized by threshold or lot(0.5포인트 비용 압박을 임계값이나 로트로 최적화)",
            "evidence_basis": f"cost_fragile={cost_fragile};shifted_trades={shifted_trades};completed_trades={completed_trades}",
            "effect": "forces cost robustness to be tested as margin, not tuned profit(비용 강건성을 튜닝 수익이 아니라 마진으로 시험)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "az_repair_direction_balance_surface",
            "review_contract": review_by_design.get("az_repair_direction_balance_surface", {}).get("contract_id", ""),
            "input_usability": "usable_as_side_balance_guard(방향 균형 가드로 사용 가능)",
            "required_next_blueprint": "long/short attribution floor without side-specific threshold(방향별 임계값 없는 롱/숏 귀속 하한)",
            "must_keep_fixed": "single frozen score surface; no side-specific retune(단일 고정 점수 표면, 방향별 재조정 금지)",
            "must_reject_if": "short density is forced by forward-targeted threshold(숏 밀도를 전진 목표 임계값으로 강제)",
            "evidence_basis": f"protocol_rows={len(src['ay_protocol'])};regime_rows={len(src['ay_regime'])}",
            "effect": "separates true side robustness from side overfit(진짜 방향 강건성과 방향 과적합을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "az_aggressive_density_preservation",
            "review_contract": review_by_design.get("az_aggressive_density_preservation", {}).get("contract_id", ""),
            "input_usability": "usable_as_trade_density_guard(거래 밀도 가드로 사용 가능)",
            "required_next_blueprint": "minimum trade retention and no no-trade victory rule(최소 거래 보존과 무거래 승리 금지 규칙)",
            "must_keep_fixed": "lot and risk unchanged(로트와 위험 고정)",
            "must_reject_if": "net improves only because exposure collapses(노출이 무너져서만 순익 개선)",
            "evidence_basis": f"shifted_trades={shifted_trades};completed_trades={completed_trades}",
            "effect": "keeps aggressive repair from becoming a hidden filter(공격적 수리가 숨은 필터가 되는 것을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "az_repair_curve_pocket_state_veto",
            "review_contract": review_by_design.get("az_repair_curve_pocket_state_veto", {}).get("contract_id", ""),
            "input_usability": "usable_as_state_veto_hypothesis_only(상태 거부 가설 전용으로 사용 가능)",
            "required_next_blueprint": "pre-trade ATR/ADX/session/regime state map, not date pocket(진입 전 ATR/ADX/세션/국면 상태 맵, 날짜 포켓 아님)",
            "must_keep_fixed": "no trade index, calendar date, realized drawdown feature(거래 번호/날짜/실현 손실 피처 금지)",
            "must_reject_if": "worst pocket row number or date appears in feature(최악 포켓 행 번호나 날짜가 피처에 등장)",
            "evidence_basis": f"curve_rows={curve_rows};regime_rows={len(src['ay_regime'])}",
            "effect": "tests curve-shape thesis without memorizing bad pockets(나쁜 구간을 외우지 않고 곡선 형태 가설을 시험)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "az_control_proxy_mt5_dual_read",
            "review_contract": review_by_design.get("az_control_proxy_mt5_dual_read", {}).get("contract_id", ""),
            "input_usability": "usable_as_runtime_mismatch_detector_only(런타임 불일치 탐지 전용으로 사용 가능)",
            "required_next_blueprint": "proxy expected vs MT5 runtime read side-by-side(프록시 예상값과 MT5 런타임 값을 나란히 읽기)",
            "must_keep_fixed": "MT5 owns KPI; proxy owns sanity check(MT5는 KPI 담당, 프록시는 점검 담당)",
            "must_reject_if": "proxy net/PF/DD is used as forward result(프록시 순익/PF/DD를 전진 결과로 사용)",
            "evidence_basis": f"proxy_rows={len(src['ay_proxy'])};proxy_forward_usable=false",
            "effect": "keeps parity work useful without promoting proxy to authority(프록시를 권위로 올리지 않고 동등성 작업을 유용하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_blueprint_queue(usability_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    priorities = {
        "az_defensive_cost_margin_objective": "P0",
        "az_repair_direction_balance_surface": "P1",
        "az_aggressive_density_preservation": "P1",
        "az_repair_curve_pocket_state_veto": "P2",
        "az_control_proxy_mt5_dual_read": "P0",
    }
    for idx, item in enumerate(usability_rows, start=1):
        design_id = str(item.get("design_id", ""))
        rows.append(
            {
                "queue_id": f"run337BC_blueprint_{idx:02d}",
                "next_run_id": NEXT_RUN_ID,
                "blueprint_family": item.get("required_next_blueprint", ""),
                "source_design_id": design_id,
                "required_inputs": item.get("review_contract", "") + ";" + aw.rel(USABILITY_MATRIX),
                "predeclared_success_evidence": "MT5 KPI plus proxy mismatch check plus no-lookahead gate(MT5 KPI와 프록시 불일치 점검 및 미래참조 방지 게이트)",
                "predeclared_failure_evidence": item.get("must_reject_if", ""),
                "negative_controls": aw.rel(NEGATIVE_REVIEW),
                "forbidden_actions": "training;threshold retune;D/B rewrite;lot optimization;date pocket;trade index(학습/임계값 재조정/D-B 재작성/로트 최적화/날짜 포켓/거래 번호)",
                "priority": priorities.get(design_id, "P2"),
                "effect": "opens bounded blueprint generation without selecting a candidate(후보 선택 없이 제한된 청사진 생성을 엶)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_lineage_review(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in src["source_hashes"]:
        path = path_from_repo(str(source.get("path", "")))
        expected = str(source.get("sha256", ""))
        actual = aw.sha256_file(path) if aw.path_exists(path) else ""
        matches = bool(expected) and expected == actual
        rows.append(
            {
                "source_id": source.get("source_id", ""),
                "path": source.get("path", ""),
                "exists": yes_no(aw.path_exists(path)),
                "row_count": row_count(path),
                "sha256": actual,
                "hash_matches_parent_record": yes_no(matches),
                "review_status": "lineage_connected(계보 연결)" if matches else "lineage_mismatch_or_missing(계보 불일치 또는 누락)",
                "effect": "checks that reviewed inputs still point to the exact parent evidence(검토 입력이 정확한 부모 근거를 계속 가리키는지 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gates(
    src: Mapping[str, Any],
    feature_review: Sequence[Mapping[str, Any]],
    gate_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    negative_review: Sequence[Mapping[str, Any]],
    firewall_review: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    lineage_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    gates = [
        {
            "gate_id": "bb_gate_source_run337BA_loaded",
            "status": status_text(bool(src["ba_final"]) and len(src["features"]) == 5 and len(src["gates"]) == 6),
            "observed": f"feature={len(src['features'])};gate={len(src['gates'])};final={bool(src['ba_final'])}",
            "expected": "run337BA materialized package loaded(337BA 물질화 패키지 로드)",
        },
        {
            "gate_id": "bb_gate_parent_gate_inherited",
            "status": status_text(all(row.get("status") == "passed" for row in src["ba_gate_audit"])),
            "observed": f"run337BA_gates={sum(1 for row in src['ba_gate_audit'] if row.get('status') == 'passed')}/{len(src['ba_gate_audit'])}",
            "expected": "all run337BA gates passed(337BA 게이트 전부 통과)",
        },
        {
            "gate_id": "bb_gate_feature_review_complete",
            "status": status_text(all(str(row.get("review_status", "")).startswith("accepted_") for row in feature_review)),
            "observed": f"accepted={sum(1 for row in feature_review if str(row.get('review_status', '')).startswith('accepted_'))}/{len(feature_review)}",
            "expected": "all feature contracts accepted(피처 계약 전부 수락)",
        },
        {
            "gate_id": "bb_gate_gate_contract_review_complete",
            "status": status_text(all(str(row.get("review_status", "")).startswith("gate_contract_review_passed") for row in gate_review)),
            "observed": f"gate_contracts={sum(1 for row in gate_review if str(row.get('review_status', '')).startswith('gate_contract_review_passed'))}/{len(gate_review)}",
            "expected": "all falsification gate contracts reviewed(반증 게이트 계약 전부 검토)",
        },
        {
            "gate_id": "bb_gate_proxy_mt5_boundary_preserved",
            "status": status_text(all(str(row.get("review_status", "")).startswith("proxy_usable") for row in proxy_review)),
            "observed": f"proxy_pairings={len(proxy_review)};forward_usable={sum(csv_number(row.get('proxy_forward_usable_rows')) for row in proxy_review)}",
            "expected": "proxy signal only, MT5 owns KPI(프록시는 신호 전용, MT5가 KPI 담당)",
        },
        {
            "gate_id": "bb_gate_negative_controls_active",
            "status": status_text(all(str(row.get("review_status", "")).startswith("negative_control_active") for row in negative_review)),
            "observed": f"negative_controls={len(negative_review)}",
            "expected": "negative controls active(부정 대조 활성)",
        },
        {
            "gate_id": "bb_gate_no_overfit_firewall_passed",
            "status": status_text(all(row.get("status") == "passed" for row in firewall_review)),
            "observed": f"firewalls={sum(1 for row in firewall_review if row.get('status') == 'passed')}/{len(firewall_review)}",
            "expected": "no look-ahead/retune/claim firewall passes(미래참조/재조정/주장 방화벽 통과)",
        },
        {
            "gate_id": "bb_gate_lineage_connected",
            "status": status_text(all(str(row.get("review_status", "")).startswith("lineage_connected") for row in lineage_rows)),
            "observed": f"lineage={sum(1 for row in lineage_rows if str(row.get('review_status', '')).startswith('lineage_connected'))}/{len(lineage_rows)}",
            "expected": "input hashes still match(입력 해시 일치 유지)",
        },
        {
            "gate_id": "bb_gate_blueprint_queue_ready",
            "status": status_text(len(queue_rows) == len(usability_rows) == 5),
            "observed": f"queue={len(queue_rows)};usability={len(usability_rows)}",
            "expected": "run337BC queue opens five bounded blueprint rows(337BC 대기열 5개 제한 청사진 행 생성)",
        },
        {
            "gate_id": "bb_gate_no_training_selection_claim_guard",
            "status": status_text(
                src["ba_final"].get("forward_passed") == "not_claimed"
                and src["ba_final"].get("runtime_authority") == "not_claimed"
                and src["ba_final"].get("goal_achieve") == "not_claimed"
            ),
            "observed": "no model training, no threshold retune, no candidate, no Forward/Goal claim(학습/임계값 재조정/후보/전진/목표 주장 없음)",
            "expected": "research boundary only(연구 경계만 허용)",
        },
    ]
    return [
        {
            "gate_id": row["gate_id"],
            "status": row["status"],
            "observed": row["observed"],
            "expected": row["expected"],
            "effect": "blocks run337BC from opening unless review evidence is complete(검토 근거가 완성되지 않으면 run337BC 개방 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in gates
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    receipts = [
        (
            EXPERIMENT_RECEIPT,
            {
                "hypothesis": "run337BA contracts can be reviewed into bounded repair blueprints without forward retune(337BA 계약을 전진 재조정 없이 제한 수리 청사진으로 검토할 수 있다)",
                "decision_use": "open run337BC blueprint materialization only(337BC 청사진 물질화만 개방)",
                "comparison_baseline": "run337BA materialized contracts and run337AY attribution evidence(337BA 물질화 계약과 337AY 귀속 근거)",
                "control_variables": "existing ONNX, feature order, threshold, lot, D/B boundary, risk logic fixed(기존 ONNX/피처 순서/임계값/로트/D-B 경계/위험 로직 고정)",
                "changed_variables": "review artifacts and blueprint queue only(검토 산출물과 청사진 대기열만 변경)",
                "success_criteria": "all review gates pass and no Forward/Goal claim is made(모든 검토 게이트 통과 및 전진/목표 주장 없음)",
                "failure_criteria": "any contract enables threshold, lot, D/B, date pocket, proxy-only KPI, or look-ahead(계약이 임계값/로트/D-B/날짜 포켓/프록시 단독 KPI/미래참조를 허용)",
                "evidence_plan": [aw.rel(path) for path in OUTPUT_FILES],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [aw.rel(path) for path in INPUT_FILES],
                "time_axis": "decision-time/pre-trade/as-of only; no future bar allowed(결정 시점/진입 전/시점 기준만 허용, 미래 봉 금지)",
                "sample_scope": "run337AY shifted custom and completed-day anchor evidence(337AY 이동 커스텀 및 완성일 앵커 근거)",
                "feature_label_boundary": "review forbids post-trade profit, realized drawdown, trade index, and calendar date as repair feature(검토는 사후 수익/실현 손실/거래 번호/날짜를 수리 피처로 금지)",
                "split_boundary": "review only; no training or forward selection(검토 전용, 학습이나 전진 선택 없음)",
                "leakage_risk": "forward-tuned threshold or date-pocket veto(전진 맞춤 임계값 또는 날짜 포켓 거부)",
                "integrity_judgment": "usable_with_boundary_for_blueprint_review_only(청사진 검토 경계 안에서 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "existing cp322A frozen ONNX research artifact(기존 cp322A 고정 ONNX 연구 산출물)",
                "threshold_policy": "fixed; no search or calibration in run337BB(고정, 337BB에서 탐색/보정 없음)",
                "overfit_risk": "repair blueprint could memorize shifted fragile pockets if not gated(게이트가 없으면 수리 청사진이 이동 취약 구간을 외울 수 있음)",
                "calibration_risk": "proxy score is sanity/rank signal, not profitability proof(프록시 점수는 점검/순위 신호이지 수익성 증명이 아님)",
                "validation_judgment": "exploratory_input_review_only(탐색 입력 검토 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": aw.rel(__file__),
                "runtime_path": "not_modified_in_run337BB(337BB에서 수정 없음)",
                "shared_contract": "proxy can detect mismatch; MT5 owns KPI(프록시는 불일치 탐지, MT5는 KPI 담당)",
                "known_differences": "proxy expected values are not forward profitability results(프록시 예상값은 전진 수익성 결과가 아님)",
                "parity_check": aw.rel(PROXY_REVIEW),
                "runtime_claim_boundary": "research-only; no runtime authority(연구 전용, 런타임 권위 없음)",
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
                "availability": "tracked reports plus ignored 02_runs artifacts represented by hash registry(추적 보고서와 해시 장부로 표시된 무시 02_runs 산출물)",
                "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [aw.rel(FEATURE_REVIEW), aw.rel(GATE_REVIEW), aw.rel(PROXY_REVIEW), aw.rel(REQUIRED_GATE_AUDIT)],
                "evidence_missing": "no new MT5 forward, no new ONNX, no live-like runtime authority(신규 MT5 전진/신규 ONNX/실거래형 런타임 권위 없음)",
                "judgment_label": "exploratory_review_passed_for_next_blueprint(다음 청사진을 위한 탐색 검토 통과)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
            },
        ),
    ]
    paths: list[Path] = []
    for path, payload in receipts:
        paths.append(aw.write_json(path, payload))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BB No-Overfit Repair Input Review(337단계 337BB 무과적합 수리 입력 검토)

## Conclusion(결론)

run337BB(337BB 실행)는 run337BA(337BA 실행)의 input contracts(입력 계약)를 검토했고, bounded repair blueprint(제한 수리 청사진) 생성으로 넘길 수 있다고 판정했다.

Effect(효과): 다음 run337BC(337BC 실행)는 비용(cost, 비용), 방향(side, 방향), 밀도(density, 밀도), 곡선 상태(curve state, 곡선 상태), proxy-MT5(프록시-MT5) 경계를 고정한 청사진만 만들 수 있다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- feature_reviews(피처 검토): `{final['feature_review_passed']}/{final['feature_review_rows']}`
- gate_reviews(게이트 검토): `{final['gate_review_passed']}/{final['gate_review_rows']}`
- proxy_reviews(프록시 검토): `{final['proxy_review_passed']}/{final['proxy_review_rows']}`
- negative_controls(부정 대조): `{final['negative_review_passed']}/{final['negative_review_rows']}`
- firewalls(방화벽): `{final['firewall_passed']}/{final['firewall_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Plain Meaning(쉬운 의미)

이번 실행은 새 ONNX(온엑스)를 만든 것이 아니다. 수리 실험에 들어가기 전에 어떤 입력은 써도 되고, 어떤 입력은 쓰면 과적합이 되는지를 먼저 잠갔다.

Effect(효과): 좋은 결과가 나온 뒤에 임계값(threshold, 임계값), 로트(lot, 로트), D/B rule(D/B 규칙), 날짜 포켓(date pocket, 날짜 포켓)을 맞추는 길을 막는다.

## Proxy-MT5 Boundary(프록시-MT5 경계)

proxy expected value(프록시 예상값)는 schema/signal sanity(스키마/신호 점검)와 mismatch detection(불일치 탐지)에만 쓴다. MT5(MetaTrader 5, 메타트레이더5) 결과만 KPI(핵심 성과 지표) 근거가 될 수 있다.

Effect(효과): 프록시가 편리하다는 이유로 forward result(전진 결과)처럼 쓰이는 것을 막는다.

## Next Action(다음 행동)

- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337BB

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

run337BB(337BB 실행)는 review(검토)만 했다. model training(모델 학습), threshold retune(임계값 재조정), D/B rewrite(D/B 재작성), lot optimization(로트 최적화), candidate selection(후보 선택)은 없다.

Effect(효과): run337BC(337BC 실행)는 bounded blueprint(제한 청사진)만 만들 수 있고, Forward/Goal(전진/목표)은 계속 주장하지 않는다.
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
        f"  Stage337 run337BB focus complete: run337BB(337BB 실행)은 `{final['status']}`로 no-overfit repair inputs(무과적합 수리 입력)를 검토했다. Effect(효과): feature reviews(피처 검토) `{final['feature_review_passed']}/{final['feature_review_rows']}`, gate reviews(게이트 검토) `{final['gate_review_passed']}/{final['gate_review_rows']}`, firewalls(방화벽) `{final['firewall_passed']}/{final['firewall_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
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
## Stage337 run337BB(337BB 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BB(337BB 실행)는 run337BA(337BA 실행)의 피처/게이트/proxy-MT5/부정 대조 계약을 검토하고 run337BC(337BC 실행) 제한 청사진 대기열을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337BB" not in current:
        current = current.replace("## Stage337 run337BA", section + "\n## Stage337 run337BA", 1)
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
- reviewed_feature_contract_rows(검토 피처 계약 행): `{final['feature_review_rows']}`
- reviewed_gate_contract_rows(검토 게이트 계약 행): `{final['gate_review_rows']}`
- negative_control_rows(부정 대조 행): `{final['negative_review_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_blueprint_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337BB(337BB 실행)는 제한 청사진으로 갈 수 있는 입력만 검토했고, 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = aw.replace_prefix_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337BB_summary(337BB 요약): `{final['status']}`. "
        f"Effect(효과): run337BA 입력 계약을 feature review(피처 검토) `{final['feature_review_passed']}/{final['feature_review_rows']}`, gate review(게이트 검토) `{final['gate_review_passed']}/{final['gate_review_rows']}`, firewall(방화벽) `{final['firewall_passed']}/{final['firewall_rows']}`로 검토하고 run337BC(337BC 실행) 제한 청사진을 연다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337BB_summary" not in brief:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337BB(337BB 실행) `{final['status']}`. "
        f"Effect(효과): no-overfit repair inputs(무과적합 수리 입력)을 검토하고 bounded repair blueprint(제한 수리 청사진) 대기열을 열었으며 Forward/Goal(전진/목표)은 주장하지 않음."
    )
    if "Stage337 run337BB" not in changelog:
        changelog = changelog.rstrip() + "\n" + line + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "no_overfit_repair_input_review_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "family": "experiment_execution",
        "primary_report": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "no_overfit_repair_input_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "no_overfit_repair_input_review_without_db(D/B 없는 무과적합 수리 입력 검토)",
        "tier_scope": "Tier A shifted/completed diagnostic evidence with strict proxy boundary(Tier A 이동/완성 진단 근거와 엄격한 프록시 경계)",
        "kpi_scope": "contract_review_no_new_trading_kpi(계약 검토, 신규 거래 KPI 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"feature_review={final['feature_review_passed']}/{final['feature_review_rows']};firewalls={final['firewall_passed']}/{final['firewall_rows']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim_input_review_only(주장 범위 밖, 입력 검토 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "run337BA materialized repair input contracts",
        "kpi_scope": "input_review_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__input_review",
        "family": "no_overfit_repair_input_review_without_db",
        "question": "can materialized no-overfit repair inputs open bounded blueprints without retune",
        "metric_scope": "contract_review_firewall_proxy_boundary",
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

    feature_review = build_feature_review(src)
    feature_path = aw.write_csv(FEATURE_REVIEW, FEATURE_REVIEW_COLUMNS, feature_review)
    gate_review = build_gate_review(src)
    gate_path = aw.write_csv(GATE_REVIEW, GATE_REVIEW_COLUMNS, gate_review)
    proxy_review = build_proxy_review(src)
    proxy_path = aw.write_csv(PROXY_REVIEW, PROXY_REVIEW_COLUMNS, proxy_review)
    negative_review = build_negative_review(src)
    negative_path = aw.write_csv(NEGATIVE_REVIEW, NEGATIVE_REVIEW_COLUMNS, negative_review)
    firewall_review = build_firewall_review(src, feature_review, gate_review, proxy_review, negative_review)
    firewall_path = aw.write_csv(FIREWALL_REVIEW, FIREWALL_COLUMNS, firewall_review)
    usability_rows = build_usability_matrix(src, feature_review)
    usability_path = aw.write_csv(USABILITY_MATRIX, USABILITY_COLUMNS, usability_rows)
    queue_rows = build_blueprint_queue(usability_rows)
    queue_path = aw.write_csv(RUN337BC_QUEUE, QUEUE_COLUMNS, queue_rows)
    lineage_rows = build_lineage_review(src)
    lineage_path = aw.write_csv(INPUT_LINEAGE_REVIEW, LINEAGE_COLUMNS, lineage_rows)
    gate_audit = build_gates(src, feature_review, gate_review, proxy_review, negative_review, firewall_review, usability_rows, queue_rows, lineage_rows)
    gate_audit_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_AUDIT_COLUMNS, gate_audit)

    all_gates_pass = all(row.get("status") == "passed" for row in gate_audit)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BB_no_overfit_input_review_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all_gates_pass else "repair_input_review_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BB_input_review_before_blueprint",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BB_input_review_gate_failure_v1",
        "feature_review_rows": len(feature_review),
        "feature_review_passed": sum(1 for row in feature_review if str(row.get("review_status", "")).startswith("accepted_")),
        "gate_review_rows": len(gate_review),
        "gate_review_passed": sum(1 for row in gate_review if str(row.get("review_status", "")).startswith("gate_contract_review_passed")),
        "proxy_review_rows": len(proxy_review),
        "proxy_review_passed": sum(1 for row in proxy_review if str(row.get("review_status", "")).startswith("proxy_usable")),
        "negative_review_rows": len(negative_review),
        "negative_review_passed": sum(1 for row in negative_review if str(row.get("review_status", "")).startswith("negative_control_active")),
        "firewall_rows": len(firewall_review),
        "firewall_passed": sum(1 for row in firewall_review if row.get("status") == "passed"),
        "usability_rows": len(usability_rows),
        "blueprint_queue_rows": len(queue_rows),
        "lineage_rows": len(lineage_rows),
        "lineage_passed": sum(1 for row in lineage_rows if str(row.get("review_status", "")).startswith("lineage_connected")),
        "gate_rows": len(gate_audit),
        "passed_gates": sum(1 for row in gate_audit if row.get("status") == "passed"),
        "failed_gates": [row.get("gate_id") for row in gate_audit if row.get("status") != "passed"],
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
        feature_path,
        gate_path,
        proxy_path,
        negative_path,
        firewall_path,
        usability_path,
        queue_path,
        lineage_path,
        gate_audit_path,
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
                "feature_review": f"{final['feature_review_passed']}/{final['feature_review_rows']}",
                "gate_review": f"{final['gate_review_passed']}/{final['gate_review_rows']}",
                "proxy_review": f"{final['proxy_review_passed']}/{final['proxy_review_rows']}",
                "negative_review": f"{final['negative_review_passed']}/{final['negative_review_rows']}",
                "firewalls": f"{final['firewall_passed']}/{final['firewall_rows']}",
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
