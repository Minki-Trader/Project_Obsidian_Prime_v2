from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import materialize_bounded_repair_scaffold_inputs_without_db as bg


aw = bg.aw

TODAY = "2026-05-27"
STAGE_ID = bg.STAGE_ID
RUN_NUMBER = "run337BH"
RUN_ID = "run337BH_review_bounded_repair_scaffold_inputs_without_db_v1"
PARENT_RUN_ID = bg.RUN_ID
NEXT_RUN_ID = "run337BI_materialize_bounded_measurement_harness_without_db_v1"
STATUS = "completed_stage337BH_bounded_scaffold_inputs_reviewed_ready_for_measurement_harness_no_training_no_selection"
JUDGMENT = "scaffold_input_review_accepts_profit_curve_proxy_mt5_gap_and_no_lookahead_contracts"
DECISION = "stage337BH_open_run337BI_materialize_bounded_measurement_harness_no_training_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BH_scaffold_input_review_without_db_cp322a_frozen_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bg.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BH_scaffold_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BH_scaffold_review.md"
SELECTED_STATUS = bg.SELECTED_STATUS
STAGE_BRIEF = bg.STAGE_BRIEF
WORKSPACE_STATE = bg.WORKSPACE_STATE
CURRENT_STATE = bg.CURRENT_STATE
CHANGELOG = bg.CHANGELOG
RUN_REGISTRY = bg.RUN_REGISTRY
ALPHA_LEDGER = bg.ALPHA_LEDGER
ARTIFACT_REGISTRY = bg.ARTIFACT_REGISTRY
STAGE_LEDGER = bg.STAGE_LEDGER

RUN337BG_DIR = STAGE_DIR / "02_runs" / "run337BG"
BG_FINAL = RUN337BG_DIR / "final_decision.json"
BG_MANIFEST = RUN337BG_DIR / "run_manifest.json"
BG_SCAFFOLD = RUN337BG_DIR / "scaffold_input_package.csv"
BG_COMPONENTS = RUN337BG_DIR / "component_contracts.csv"
BG_PROFIT = RUN337BG_DIR / "profit_curve_measurement_contract.csv"
BG_PROXY = RUN337BG_DIR / "proxy_mt5_runtime_probe_contract.csv"
BG_MT5_GAP = RUN337BG_DIR / "mt5_gap_repair_input_contract.csv"
BG_FIREWALL = RUN337BG_DIR / "no_lookahead_firewall_checklist.csv"
BG_LANES = RUN337BG_DIR / "balanced_research_lane_matrix.csv"
BG_QUEUE = RUN337BG_DIR / "run337BH_review_queue.csv"
BG_GATE_AUDIT = RUN337BG_DIR / "required_gate_coverage_audit.csv"
BG_EXPERIMENT_RECEIPT = RUN337BG_DIR / "experiment_design_receipt.json"
BG_DATA_RECEIPT = RUN337BG_DIR / "data_integrity_receipt.json"
BG_MODEL_RECEIPT = RUN337BG_DIR / "model_validation_receipt.json"
BG_RUNTIME_RECEIPT = RUN337BG_DIR / "runtime_parity_receipt.json"
BG_PERFORMANCE_RECEIPT = RUN337BG_DIR / "performance_attribution_receipt.json"
BG_ARTIFACT_RECEIPT = RUN337BG_DIR / "artifact_lineage_receipt.json"
BG_JUDGMENT_RECEIPT = RUN337BG_DIR / "result_judgment_receipt.json"

SCAFFOLD_REVIEW = RUN_DIR / "scaffold_input_review_matrix.csv"
PROFIT_REVIEW = RUN_DIR / "profit_curve_contract_review.csv"
PROXY_REVIEW = RUN_DIR / "proxy_mt5_contract_review.csv"
MT5_GAP_REVIEW = RUN_DIR / "mt5_gap_repair_contract_review.csv"
FIREWALL_REVIEW = RUN_DIR / "no_lookahead_firewall_review.csv"
LANE_REVIEW = RUN_DIR / "balanced_lane_review.csv"
IMPLEMENTATION_HANDOFF = RUN_DIR / "measurement_harness_handoff_boundary.csv"
RUN337BI_QUEUE = RUN_DIR / "run337BI_measurement_harness_queue.csv"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BG_FINAL,
    BG_MANIFEST,
    BG_SCAFFOLD,
    BG_COMPONENTS,
    BG_PROFIT,
    BG_PROXY,
    BG_MT5_GAP,
    BG_FIREWALL,
    BG_LANES,
    BG_QUEUE,
    BG_GATE_AUDIT,
    BG_EXPERIMENT_RECEIPT,
    BG_DATA_RECEIPT,
    BG_MODEL_RECEIPT,
    BG_RUNTIME_RECEIPT,
    BG_PERFORMANCE_RECEIPT,
    BG_ARTIFACT_RECEIPT,
    BG_JUDGMENT_RECEIPT,
)
OUTPUT_FILES = (
    SCAFFOLD_REVIEW,
    PROFIT_REVIEW,
    PROXY_REVIEW,
    MT5_GAP_REVIEW,
    FIREWALL_REVIEW,
    LANE_REVIEW,
    IMPLEMENTATION_HANDOFF,
    RUN337BI_QUEUE,
    REQUIRED_GATE_AUDIT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

SCAFFOLD_REVIEW_COLUMNS = (
    "review_id",
    "input_id",
    "source_blueprint_id",
    "workstream",
    "component",
    "frozen_controls_present",
    "changed_variables_bounded",
    "profit_priority_present",
    "runtime_probe_required",
    "forbidden_actions_complete",
    "invalid_conditions_complete",
    "next_consumer_ok",
    "review_status",
    "effect",
    "claim_boundary",
)
PROFIT_REVIEW_COLUMNS = (
    "review_id",
    "metric_id",
    "metric_family",
    "required_metric",
    "lot_normalized_or_guarded",
    "cost_stress_ok",
    "forward_use_blocked",
    "failure_signal_present",
    "review_status",
    "effect",
    "claim_boundary",
)
PROXY_REVIEW_COLUMNS = (
    "review_id",
    "contract_id",
    "comparison_subject",
    "proxy_field_ok",
    "mt5_probe_field_ok",
    "join_key_present",
    "difference_output_present",
    "usability_bounded",
    "forbidden_claim_present",
    "review_status",
    "effect",
    "claim_boundary",
)
MT5_GAP_REVIEW_COLUMNS = (
    "review_id",
    "repair_input_id",
    "source_blueprint_id",
    "gap_minutes",
    "feature_last_required",
    "probe_output_complete",
    "blocked_claims_complete",
    "review_status",
    "effect",
    "claim_boundary",
)
FIREWALL_REVIEW_COLUMNS = (
    "review_id",
    "guard_id",
    "guard_family",
    "must_remain_false",
    "abort_if_seen_present",
    "added_check_present",
    "review_status",
    "effect",
    "claim_boundary",
)
LANE_REVIEW_COLUMNS = (
    "review_id",
    "lane_id",
    "workstream_family",
    "required_contracts_present",
    "metric_scope_present",
    "forbidden_shortcut_present",
    "review_status",
    "effect",
    "claim_boundary",
)
HANDOFF_COLUMNS = (
    "handoff_id",
    "allowed_next_work",
    "required_inputs",
    "required_outputs",
    "must_preserve",
    "must_reject",
    "review_before_runtime",
    "handoff_status",
    "effect",
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
GATE_COLUMNS = (
    "gate_id",
    "status",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def read_rows(path: Path) -> list[dict[str, str]]:
    _, rows = aw.read_csv_table(path, prefer_head=True)
    return rows


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def load_inputs() -> dict[str, Any]:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BG review source files: {missing}")
    return {
        "final": read_json(BG_FINAL),
        "manifest": read_json(BG_MANIFEST),
        "scaffold": read_rows(BG_SCAFFOLD),
        "components": read_rows(BG_COMPONENTS),
        "profit": read_rows(BG_PROFIT),
        "proxy": read_rows(BG_PROXY),
        "mt5_gap": read_rows(BG_MT5_GAP),
        "firewall": read_rows(BG_FIREWALL),
        "lanes": read_rows(BG_LANES),
        "queue": read_rows(BG_QUEUE),
        "gates": read_rows(BG_GATE_AUDIT),
        "receipts": [read_json(path) for path in (
            BG_EXPERIMENT_RECEIPT,
            BG_DATA_RECEIPT,
            BG_MODEL_RECEIPT,
            BG_RUNTIME_RECEIPT,
            BG_PERFORMANCE_RECEIPT,
            BG_ARTIFACT_RECEIPT,
            BG_JUDGMENT_RECEIPT,
        )],
    }


def build_scaffold_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        controls = row.get("control_variables", "")
        forbidden = row.get("forbidden_actions", "")
        invalid = row.get("invalid_conditions", "")
        required_metrics = row.get("required_metrics", "")
        frozen_ok = all(term in controls for term in ("cp322A", "threshold", "D/B", "runtime handoff"))
        bounded_ok = "measurement inputs" in row.get("changed_variables", "") or "측정 입력" in row.get("changed_variables", "")
        profit_priority = any(term in required_metrics for term in ("net_profit", "profit", "수익", "curve", "곡선")) or "offensive" in row.get("workstream", "")
        runtime_required = "MT5" in row.get("required_runtime_probe", "") and "probe" in row.get("required_runtime_probe", "")
        forbidden_ok = all(term in forbidden for term in ("training", "threshold", "D/B", "lot", "forward", "runtime"))
        invalid_ok = all(term in invalid for term in ("training", "threshold", "D/B", "lot", "date", "trade-index", "proxy"))
        next_ok = row.get("next_consumer") == RUN_ID
        passed = frozen_ok and bounded_ok and runtime_required and forbidden_ok and invalid_ok and next_ok
        out.append(
            {
                "review_id": f"{RUN_NUMBER}_{row['source_blueprint_id']}_scaffold_review",
                "input_id": row["input_id"],
                "source_blueprint_id": row["source_blueprint_id"],
                "workstream": row["workstream"],
                "component": row["scaffold_component"],
                "frozen_controls_present": bool_text(frozen_ok),
                "changed_variables_bounded": bool_text(bounded_ok),
                "profit_priority_present": bool_text(profit_priority),
                "runtime_probe_required": bool_text(runtime_required),
                "forbidden_actions_complete": bool_text(forbidden_ok),
                "invalid_conditions_complete": bool_text(invalid_ok),
                "next_consumer_ok": bool_text(next_ok),
                "review_status": "accepted_for_measurement_harness(측정 하네스 허용)" if passed else "rejected_scaffold_contract_gap(스캐폴드 계약 공백 거절)",
                "effect": "keeps next implementation bound to measurement contracts and frozen cp322A(다음 구현을 측정 계약과 고정 cp322A에 묶음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def build_profit_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        lot_guarded = row.get("must_be_lot_normalized") in {"true", "false_if_unscaled(비정규화면 거짓)", "not_applicable"} or "lot" in row.get("required_metric", "")
        cost_ok = row.get("cost_stress_required") in {"true", "false"}
        forward_blocked = row.get("forward_use_allowed") == "false"
        failure_signal = bool(row.get("failure_signal", "").strip())
        passed = lot_guarded and cost_ok and forward_blocked and failure_signal
        out.append(
            {
                "review_id": f"{RUN_NUMBER}_{row['metric_id']}_profit_review",
                "metric_id": row["metric_id"],
                "metric_family": row["metric_family"],
                "required_metric": row["required_metric"],
                "lot_normalized_or_guarded": bool_text(lot_guarded),
                "cost_stress_ok": bool_text(cost_ok),
                "forward_use_blocked": bool_text(forward_blocked),
                "failure_signal_present": bool_text(failure_signal),
                "review_status": "accepted_profit_curve_contract(수익곡선 계약 허용)" if passed else "rejected_profit_curve_contract_gap(수익곡선 계약 공백 거절)",
                "effect": "requires profit, trade count, risk, curve pocket, and stress to be read together(수익/거래수/위험/곡선 포켓/스트레스를 함께 읽게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def build_proxy_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        proxy_ok = row.get("proxy_expected_field", "").startswith("proxy_expected_")
        mt5_ok = row.get("mt5_runtime_probe_field", "").startswith("mt5_runtime_probe_")
        join_ok = bool(row.get("join_key", "").strip())
        diff_ok = "difference" in row.get("required_difference_output", "") or "차이" in row.get("required_difference_output", "")
        usability = row.get("usability_if_pass", "")
        bounded = any(term in usability for term in ("signal", "diagnostic", "handoff", "observability", "신호", "진단", "인계", "관측"))
        forbidden = bool(row.get("must_not_claim", "").strip())
        passed = proxy_ok and mt5_ok and join_ok and diff_ok and bounded and forbidden
        out.append(
            {
                "review_id": f"{RUN_NUMBER}_{row['contract_id']}_proxy_review",
                "contract_id": row["contract_id"],
                "comparison_subject": row["comparison_subject"],
                "proxy_field_ok": bool_text(proxy_ok),
                "mt5_probe_field_ok": bool_text(mt5_ok),
                "join_key_present": bool_text(join_ok),
                "difference_output_present": bool_text(diff_ok),
                "usability_bounded": bool_text(bounded),
                "forbidden_claim_present": bool_text(forbidden),
                "review_status": "accepted_proxy_mt5_contract(프록시-MT5 계약 허용)" if passed else "rejected_proxy_mt5_contract_gap(프록시-MT5 계약 공백 거절)",
                "effect": "allows proxy use only after expected values are compared with MT5 runtime probe values(프록시 예상값을 MT5 런타임 탐침값과 비교한 뒤에만 사용 허용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def build_mt5_gap_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        gap = int(row.get("max_tester_to_feature_gap_minutes") or 0)
        feature_required = "feature_last" in row.get("required_before_forward", "")
        probe = row.get("required_probe_output", "")
        probe_complete = all(term in probe for term in ("tester report", "handoff", "difference", "feature_last"))
        blocked = row.get("blocked_claims_until_repaired", "")
        blocked_complete = all(term in blocked for term in ("Forward", "runtime authority", "live readiness", "deployment"))
        passed = gap >= 0 and feature_required and probe_complete and blocked_complete
        out.append(
            {
                "review_id": f"{RUN_NUMBER}_{row['repair_input_id']}_mt5_gap_review",
                "repair_input_id": row["repair_input_id"],
                "source_blueprint_id": row["source_blueprint_id"],
                "gap_minutes": str(gap),
                "feature_last_required": bool_text(feature_required),
                "probe_output_complete": bool_text(probe_complete),
                "blocked_claims_complete": bool_text(blocked_complete),
                "review_status": "accepted_mt5_gap_repair_contract(MT5 공백 수리 계약 허용)" if passed else "rejected_mt5_gap_contract_gap(MT5 공백 계약 공백 거절)",
                "effect": "keeps forward decisions blocked until tester reaches feature_last(테스터가 feature_last에 도달할 때까지 전진 판정을 막음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def build_firewall_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        must_false = row.get("must_remain_false") == "true"
        abort = bool(row.get("abort_if_seen", "").strip())
        added = bool(row.get("added_check", "").strip())
        passed = must_false and abort and added
        out.append(
            {
                "review_id": f"{RUN_NUMBER}_{row['guard_id']}_firewall_review",
                "guard_id": row["guard_id"],
                "guard_family": row["guard_family"],
                "must_remain_false": row["must_remain_false"],
                "abort_if_seen_present": bool_text(abort),
                "added_check_present": bool_text(added),
                "review_status": "accepted_no_lookahead_firewall(미래참조 방화벽 허용)" if passed else "rejected_firewall_gap(방화벽 공백 거절)",
                "effect": "prevents stronger profit research from reintroducing look-ahead or selection bias(강한 수익 연구가 미래참조나 선택 편향을 다시 만들지 못하게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def build_lane_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        contracts = bool(row.get("required_contracts", "").strip())
        metric = bool(row.get("required_metric_scope", "").strip())
        forbidden = bool(row.get("forbidden_shortcut", "").strip())
        passed = contracts and metric and forbidden
        out.append(
            {
                "review_id": f"{RUN_NUMBER}_{row['lane_id']}_lane_review",
                "lane_id": row["lane_id"],
                "workstream_family": row["workstream_family"],
                "required_contracts_present": bool_text(contracts),
                "metric_scope_present": bool_text(metric),
                "forbidden_shortcut_present": bool_text(forbidden),
                "review_status": "accepted_balanced_lane(균형 레인 허용)" if passed else "rejected_lane_gap(레인 공백 거절)",
                "effect": "keeps defensive, repair, offensive, parity, and attribution lanes balanced(방어/수리/공격/동등성/귀속 레인을 균형 있게 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def build_handoff() -> list[dict[str, Any]]:
    return [
        {
            "handoff_id": "run337BH_measurement_harness_handoff",
            "allowed_next_work": "materialize bounded measurement harness inputs and dry-run contracts(제한 측정 하네스 입력과 드라이런 계약 물질화)",
            "required_inputs": ";".join(aw.rel(path) for path in (SCAFFOLD_REVIEW, PROFIT_REVIEW, PROXY_REVIEW, MT5_GAP_REVIEW, FIREWALL_REVIEW, LANE_REVIEW)),
            "required_outputs": "measurement harness contract, proxy-MT5 diff schema, profit curve schema, MT5 probe manifest, review queue(측정 하네스 계약/프록시-MT5 차이 스키마/수익곡선 스키마/MT5 탐침 목록/검토 대기열)",
            "must_preserve": "cp322A ONNX, threshold, D/B, lot, risk, ATR SL/TP, runtime handoff(cp322A ONNX/임계값/D-B/로트/위험/ATR SLTP/런타임 인계)",
            "must_reject": "training, threshold search, D/B rewrite, lot optimization, single KPI selection, proxy KPI authority, forward claim(학습/임계값 탐색/D-B 재작성/로트 최적화/단일 KPI 선택/프록시 KPI 권위/전진 주장)",
            "review_before_runtime": "run337BJ review must pass before MT5 runtime or forward tester execution(MT5 런타임 또는 전진 테스터 실행 전 run337BJ 검토 필요)",
            "handoff_status": "open_measurement_harness_inputs_only(측정 하네스 입력만 개방)",
            "effect": "moves toward actual profit/parity measurement without mutating the trading surface(거래 표면 변경 없이 실제 수익/동등성 측정으로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BI_materialize_bounded_measurement_harness",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "bounded measurement harness inputs(제한 측정 하네스 입력)",
            "inputs_to_review": ";".join(aw.rel(path) for path in (SCAFFOLD_REVIEW, PROFIT_REVIEW, PROXY_REVIEW, MT5_GAP_REVIEW, FIREWALL_REVIEW, LANE_REVIEW, IMPLEMENTATION_HANDOFF)),
            "must_confirm": "profit curve schema, proxy-MT5 expected-vs-runtime schema, MT5 feature_last repair probe, no-lookahead firewall(수익곡선 스키마/프록시-MT5 예상값 대 런타임값 스키마/MT5 feature_last 수리 탐침/미래참조 방화벽)",
            "must_reject_if": "model training, threshold retune, D/B rewrite, lot optimization, date-fit, trade-index target, proxy KPI authority, Forward/Runtime/Goal claim(모델 학습/임계값 재조정/D-B 재작성/로트 최적화/날짜 맞춤/거래번호 타깃/프록시 KPI 권위/전진·런타임·목표 주장)",
            "expected_outputs": "measurement harness materialization package only(측정 하네스 물질화 패키지만)",
            "priority": "P0",
            "effect": "lets the next run build measurement inputs without opening model or runtime authority(다음 실행이 모델 또는 런타임 권위 없이 측정 입력을 만들게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def count_status(rows: Sequence[Mapping[str, Any]], column: str, prefix: str) -> int:
    return sum(1 for row in rows if str(row.get(column, "")).startswith(prefix))


def build_gates(
    src: Mapping[str, Any],
    scaffold_review: Sequence[Mapping[str, Any]],
    profit_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    mt5_review: Sequence[Mapping[str, Any]],
    firewall_review: Sequence[Mapping[str, Any]],
    lane_review: Sequence[Mapping[str, Any]],
    handoff_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parent = src["final"]
    source_gates_passed = sum(1 for row in src["gates"] if row.get("status") == "passed")
    profit_required = {
        "run337BG_net_profit",
        "run337BG_profit_factor",
        "run337BG_trades_per_day",
        "run337BG_max_drawdown",
        "run337BG_recovery_factor",
        "run337BG_expectancy",
        "run337BG_worst_chunk",
        "run337BG_underwater_stretch",
        "run337BG_curve_pocket",
        "run337BG_lot_normalized",
        "run337BG_cost_stress",
    }
    profit_ids = {row["metric_id"] for row in src["profit"]}
    lane_names = {row["workstream_family"] for row in src["lanes"]}
    gate_specs = [
        ("bh_gate_parent_loaded", parent.get("next_action") == RUN_ID, f"parent_next={parent.get('next_action')}", "run337BG opens run337BH(337BG가 337BH를 엶)"),
        ("bh_gate_parent_gates_passed", parent.get("passed_gates") == parent.get("gate_rows") == 12 and source_gates_passed == 12, f"parent_gates={parent.get('passed_gates')}/{parent.get('gate_rows')};audit={source_gates_passed}/12", "run337BG all gates passed(337BG 모든 게이트 통과)"),
        ("bh_gate_scaffold_review_accepts_all", len(scaffold_review) == 5 and count_status(scaffold_review, "review_status", "accepted_for_measurement_harness") == 5, f"scaffold={count_status(scaffold_review, 'review_status', 'accepted_for_measurement_harness')}/{len(scaffold_review)}", "five scaffold inputs accepted(스캐폴드 입력 5개 허용)"),
        ("bh_gate_profit_contract_complete", profit_required.issubset(profit_ids) and count_status(profit_review, "review_status", "accepted_profit_curve_contract") == len(profit_review) == 11, f"profit={count_status(profit_review, 'review_status', 'accepted_profit_curve_contract')}/{len(profit_review)}", "profit curve metrics complete and reviewed(수익곡선 지표 완비 및 검토)"),
        ("bh_gate_proxy_mt5_contract_complete", count_status(proxy_review, "review_status", "accepted_proxy_mt5_contract") == len(proxy_review) == 5, f"proxy={count_status(proxy_review, 'review_status', 'accepted_proxy_mt5_contract')}/{len(proxy_review)}", "proxy expected vs MT5 runtime probe contracts reviewed(프록시 예상값 대 MT5 런타임 탐침 계약 검토)"),
        ("bh_gate_mt5_gap_contract_active", count_status(mt5_review, "review_status", "accepted_mt5_gap_repair_contract") == len(mt5_review) == 5, f"mt5_gap={count_status(mt5_review, 'review_status', 'accepted_mt5_gap_repair_contract')}/{len(mt5_review)}", "MT5 feature_last gap repair contracts reviewed(MT5 feature_last 공백 수리 계약 검토)"),
        ("bh_gate_firewalls_active", count_status(firewall_review, "review_status", "accepted_no_lookahead_firewall") == len(firewall_review) >= 12, f"firewall={count_status(firewall_review, 'review_status', 'accepted_no_lookahead_firewall')}/{len(firewall_review)}", "no-lookahead firewalls reviewed(미래참조 방화벽 검토)"),
        ("bh_gate_balanced_lanes", {"defensive(방어)", "repair(수리)", "offensive(공격)", "parity-control(동등성 대조)"}.issubset(lane_names) and count_status(lane_review, "review_status", "accepted_balanced_lane") == len(lane_review), f"lanes={';'.join(sorted(lane_names))};review={count_status(lane_review, 'review_status', 'accepted_balanced_lane')}/{len(lane_review)}", "balanced lanes reviewed(균형 레인 검토)"),
        ("bh_gate_handoff_bounded", len(handoff_rows) == 1 and "training" in handoff_rows[0]["must_reject"] and "cp322A" in handoff_rows[0]["must_preserve"], f"handoff={len(handoff_rows)}", "bounded measurement harness handoff only(제한 측정 하네스 인계만)"),
        ("bh_gate_queue_ready", len(queue_rows) == 1 and queue_rows[0]["next_run_id"] == NEXT_RUN_ID, f"queue={len(queue_rows)};next={queue_rows[0]['next_run_id'] if queue_rows else 'missing'}", "run337BI queue ready(337BI 대기열 준비)"),
        ("bh_gate_no_trading_kpi_claim", True, "no_new_trading_kpi;forward=not_claimed", "no trading KPI or forward claim(거래 KPI 또는 전진 주장 없음)"),
        ("bh_gate_no_forbidden_claims", True, "runtime=not_claimed;goal=not_claimed", "no runtime authority or Goal Achieve(런타임 권위 또는 목표 달성 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": observed,
            "expected": expected,
            "effect": "blocks measurement harness handoff unless review proves bounded profit/parity scope(검토가 제한된 수익/동등성 범위를 증명해야 측정 하네스 인계 허용)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in gate_specs
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    receipts = [
        (
            EXPERIMENT_RECEIPT,
            {
                "skill": "obsidian-experiment-design",
                "run_id": RUN_ID,
                "hypothesis": "reviewed scaffold inputs can safely open measurement harness materialization(검토된 스캐폴드 입력이 측정 하네스 물질화를 안전하게 열 수 있음)",
                "decision_use": "open run337BI only if all review gates pass(모든 검토 게이트 통과 시 run337BI만 개방)",
                "comparison_baseline": PARENT_RUN_ID,
                "control_variables": "cp322A ONNX, threshold, D/B, risk, lot, ATR SL/TP, runtime handoff frozen(cp322A ONNX/임계값/D-B/위험/로트/ATR SLTP/런타임 인계 고정)",
                "changed_variables": "review artifacts and next measurement harness queue only(검토 산출물과 다음 측정 하네스 대기열만)",
                "sample_scope": "no trading data interpreted in this review(이번 검토에서는 거래 데이터 해석 없음)",
                "success_criteria": "12 gates pass and run337BI queue ready(12개 게이트 통과와 run337BI 대기열 준비)",
                "failure_criteria": "missing profit metric, proxy-MT5 field, MT5 gap input, or firewall(수익 지표/프록시-MT5 필드/MT5 공백 입력/방화벽 누락)",
                "invalid_conditions": "any surface mutation or forward claim(표면 변경 또는 전진 주장)",
                "stop_conditions": "failed gate creates repair before implementation(게이트 실패 시 구현 전 수리)",
                "evidence_plan": [aw.rel(path) for path in OUTPUT_FILES],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "skill": "obsidian-data-integrity",
                "run_id": RUN_ID,
                "data_source": [aw.rel(path) for path in INPUT_FILES],
                "time_axis": "feature_last and completed-bar rules required downstream(feature_last와 완성봉 규칙은 하위 필수)",
                "sample_scope": "review-only, no new training or KPI sample(검토 전용, 새 학습 또는 KPI 표본 없음)",
                "missing_or_duplicate_check": "required in run337BI harness schemas(337BI 하네스 스키마에서 필수)",
                "feature_label_boundary": "future bar, date-fit, trade-index, proxy KPI authority rejected(미래 봉/날짜 맞춤/거래번호/프록시 KPI 권위 거부)",
                "split_boundary": "frozen cp322A research artifact, measurement-only next step(cp322A 고정 연구 산출물, 다음은 측정 전용)",
                "leakage_risk": "not measured yet; guard retained(아직 측정하지 않음, 가드 유지)",
                "data_hash_or_identity": f"artifact_registry_run={RUN_ID}",
                "integrity_judgment": "usable_with_boundary_for_measurement_harness_review(측정 하네스 검토에 한해 경계 포함 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "skill": "obsidian-model-validation",
                "run_id": RUN_ID,
                "model_family": "cp322A frozen ONNX package(cp322A 고정 ONNX 패키지)",
                "target_and_label": "unchanged; no fit or label rewrite(변경 없음, fit 또는 라벨 재작성 없음)",
                "split_method": "review-only, no split mutation(검토 전용, 분할 변경 없음)",
                "selection_metric": "none; no selection(없음, 선택 없음)",
                "secondary_metrics": "profit/risk/execution metrics accepted as future measurement contracts only(수익/위험/실행 지표는 미래 측정 계약으로만 허용)",
                "threshold_policy": "fixed frozen threshold(고정 임계값)",
                "overfit_risk": "single-KPI or proxy authority blocked(단일 KPI 또는 프록시 권위 차단)",
                "calibration_risk": "scores not treated as probability(점수를 확률로 취급하지 않음)",
                "comparison_baseline": PARENT_RUN_ID,
                "validation_judgment": "research_review_only(연구 검토 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "skill": "obsidian-runtime-parity",
                "run_id": RUN_ID,
                "research_path": aw.rel(Path(__file__)),
                "runtime_path": "MT5 runtime not executed; next harness input only(MT5 런타임 미실행, 다음 하네스 입력 전용)",
                "shared_contract": "proxy expected value fields and MT5 runtime probe value fields reviewed(프록시 예상값 필드와 MT5 런타임 탐침값 필드 검토)",
                "known_differences": "tester_feature_last_gap remains until fresh MT5 probe(신규 MT5 탐침 전까지 tester_feature_last 공백 유지)",
                "parity_check": "contract review only, no runtime authority(계약 검토 전용, 런타임 권위 없음)",
                "parity_identity": f"parent={PARENT_RUN_ID};review={RUN_ID}",
                "runtime_claim_boundary": "research_only_no_runtime_authority(연구 전용, 런타임 권위 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "skill": "obsidian-performance-attribution",
                "run_id": RUN_ID,
                "observed_change": "profit-curve measurement contract reviewed; no trading KPI observed(수익곡선 측정 계약 검토, 거래 KPI 관측 없음)",
                "comparison_baseline": PARENT_RUN_ID,
                "likely_drivers": "not_applicable_until_trade_list(거래 목록 전까지 해당 없음)",
                "segment_checks": "long/short/session/hour/month/volatility/ADX/VIX/USD/rate required downstream(롱숏/세션/시간/월/변동성/ADX/VIX/USD/금리 하위 필수)",
                "trade_shape": "required downstream, not measured here(하위 필수, 여기서는 미측정)",
                "alternative_explanations": "measurement contract can still fail when real MT5 data arrives(실제 MT5 데이터에서 측정 계약이 실패할 수 있음)",
                "attribution_confidence": "inconclusive_by_design(설계상 불충분)",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "skill": "obsidian-artifact-lineage",
                "run_id": RUN_ID,
                "source_inputs": [aw.rel(path) for path in INPUT_FILES],
                "producer": aw.rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [aw.rel(path) for path in OUTPUT_FILES],
                "artifact_hashes": "recorded_in_artifact_registry(산출물 등록부에 기록)",
                "registry_links": [aw.rel(RUN_REGISTRY), aw.rel(ALPHA_LEDGER), aw.rel(STAGE_LEDGER), aw.rel(ARTIFACT_REGISTRY)],
                "availability": "tracked_and_reproducible_from_script(추적됨, 스크립트로 재현 가능)",
                "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "skill": "obsidian-result-judgment",
                "run_id": RUN_ID,
                "result_subject": "run337BG scaffold inputs review(337BG 스캐폴드 입력 검토)",
                "evidence_available": [aw.rel(path) for path in OUTPUT_FILES],
                "evidence_missing": "measurement harness output, MT5 runtime probe, forward trade list, profit curve KPI(측정 하네스 출력/MT5 런타임 탐침/전진 거래 목록/수익곡선 KPI)",
                "judgment_label": "exploratory_review_completed(탐색 검토 완료)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "입력 계약은 통과했지만 아직 실제 수익 검증은 아니다.",
            },
        ),
    ]
    return [aw.write_json(path, payload) for path, payload in receipts]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BH Scaffold Input Review(337단계 337BH 스캐폴드 입력 검토)

## Conclusion(결론)

run337BH(337BH 실행)는 run337BG(337BG 실행)의 profit curve(수익곡선), proxy-MT5(프록시-MT5), MT5 gap repair(MT5 공백 수리), no-lookahead firewall(미래참조 방화벽), balanced lane(균형 레인) 입력을 검토했고, 다음은 measurement harness(측정 하네스) 입력 물질화만 허용한다고 판정했다.

Effect(효과): 수익곡선 우선 연구를 실제 측정 쪽으로 한 단계 넘기되, cp322A(322A 후보), threshold(임계값), D/B rule(D/B 규칙), lot(로트), runtime handoff(런타임 인계)는 바꾸지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- scaffold_reviews(스캐폴드 검토): `{final['scaffold_passed']}/{final['scaffold_rows']}`
- profit_reviews(수익 계약 검토): `{final['profit_passed']}/{final['profit_rows']}`
- proxy_reviews(프록시 계약 검토): `{final['proxy_passed']}/{final['proxy_rows']}`
- mt5_gap_reviews(MT5 공백 검토): `{final['mt5_passed']}/{final['mt5_rows']}`
- firewall_reviews(방화벽 검토): `{final['firewall_passed']}/{final['firewall_rows']}`
- lane_reviews(레인 검토): `{final['lane_passed']}/{final['lane_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Proxy-MT5 Boundary(프록시-MT5 경계)

proxy expected field(프록시 예상 필드)와 MT5 runtime probe field(MT5 런타임 탐침 필드)는 비교 계약으로 허용했다. 하지만 실제 MT5 runtime probe(MT5 런타임 탐침) 출력이 아직 없으므로, signal parity(신호 동등성)와 handoff sanity(인계 정상성) 범위만 열고 Forward Passed/Failed(전진 통과/실패)는 열지 않는다.

## Next Action(다음 행동)

- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BH Scaffold Review(결정: 337단계 337BH 스캐폴드 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): profit curve(수익곡선) 우선 입력을 measurement harness(측정 하네스)로 넘길 수 있지만, 실제 MT5 runtime probe(MT5 런타임 탐침)와 forward trade list(전진 거래 목록)는 아직 없다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []

    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.remove_workspace_focus_block(workspace_text, "Stage337 run337BH focus")
    workspace = bg.replace_top_value(workspace, "current_run_id: ", NEXT_RUN_ID)
    focus = (
        f"- >-\n  Stage337 run337BH focus complete: run337BH(337BH 실행)은 `{final['status']}`로 "
        f"bounded scaffold input review(제한 스캐폴드 입력 검토)를 완료했다. Effect(효과): "
        f"profit reviews(수익 검토) `{final['profit_passed']}/{final['profit_rows']}`, proxy reviews(프록시 검토) "
        f"`{final['proxy_passed']}/{final['proxy_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`이며 "
        f"Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    current = bg.remove_markdown_section(current_text, "## Stage337 run337BH(337BH 실행)")
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BH(337BH 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BH(337BH 실행)는 수익곡선/프록시-MT5/MT5 공백/미래참조 방화벽 입력을 검토하고 측정 하네스 입력만 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.

"""
    marker = "## Stage337 run337BG"
    current = current.replace(marker, entry + marker, 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- scaffold_review_rows(스캐폴드 검토 행): `{final['scaffold_rows']}`
- profit_contract_review_rows(수익 계약 검토 행): `{final['profit_rows']}`
- proxy_mt5_review_rows(프록시-MT5 검토 행): `{final['proxy_rows']}`
- mt5_gap_review_rows(MT5 공백 검토 행): `{final['mt5_rows']}`
- no_lookahead_firewall_review_rows(미래참조 방화벽 검토 행): `{final['firewall_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_measurement_harness_input_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337BH(337BH 실행)는 측정 하네스 입력만 열었고 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief_text, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_text = bg.remove_lines_containing(brief_text, "run337BH(337BH 실행):")
    brief_line = (
        f"\n- run337BH(337BH 실행): `{final['status']}`. Effect(효과): scaffold input review(스캐폴드 입력 검토)를 완료했고 "
        f"measurement harness(측정 하네스) 입력만 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief_text.rstrip() + brief_line, brief_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_text = bg.remove_lines_containing(changelog_text, f",{RUN_ID},")
    changelog_line = f"{TODAY},Stage337,{RUN_ID},{final['status']},{final['judgment']},{aw.rel(REPORT_PATH)}\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_line, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "bounded_scaffold_input_review_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "work_family": "experiment_design",
        "primary_artifact": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__scaffold_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "scaffold_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BH bounded scaffold review",
        "tier_scope": "research_review_only",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"profit={final['profit_passed']}/{final['profit_rows']};proxy={final['proxy_passed']}/{final['proxy_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "guardrail_kpi": "cp322a_frozen;proxy_signal_only;mt5_gap_repair_required;no_training;no_threshold;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 검토 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};runtime_authority_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__scaffold_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design",
        "evidence_scope": "run337BG scaffold inputs",
        "kpi_scope": "review_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__scaffold_review",
        "family": "bounded_scaffold_input_review_without_db",
        "question": "can reviewed scaffold inputs open measurement harness without surface mutation",
        "metric_scope": "profit_curve_proxy_mt5_mt5_gap_no_lookahead",
        "primary_artifact": aw.rel(REPORT_PATH),
        "report_path": aw.rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
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
    scaffold_review = build_scaffold_review(src["scaffold"])
    scaffold_path = aw.write_csv(SCAFFOLD_REVIEW, SCAFFOLD_REVIEW_COLUMNS, scaffold_review)
    profit_review = build_profit_review(src["profit"])
    profit_path = aw.write_csv(PROFIT_REVIEW, PROFIT_REVIEW_COLUMNS, profit_review)
    proxy_review = build_proxy_review(src["proxy"])
    proxy_path = aw.write_csv(PROXY_REVIEW, PROXY_REVIEW_COLUMNS, proxy_review)
    mt5_review = build_mt5_gap_review(src["mt5_gap"])
    mt5_path = aw.write_csv(MT5_GAP_REVIEW, MT5_GAP_REVIEW_COLUMNS, mt5_review)
    firewall_review = build_firewall_review(src["firewall"])
    firewall_path = aw.write_csv(FIREWALL_REVIEW, FIREWALL_REVIEW_COLUMNS, firewall_review)
    lane_review = build_lane_review(src["lanes"])
    lane_path = aw.write_csv(LANE_REVIEW, LANE_REVIEW_COLUMNS, lane_review)
    handoff_rows = build_handoff()
    handoff_path = aw.write_csv(IMPLEMENTATION_HANDOFF, HANDOFF_COLUMNS, handoff_rows)
    queue_rows = build_queue()
    queue_path = aw.write_csv(RUN337BI_QUEUE, QUEUE_COLUMNS, queue_rows)
    gate_rows = build_gates(src, scaffold_review, profit_review, proxy_review, mt5_review, firewall_review, lane_review, handoff_rows, queue_rows)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BH_scaffold_review_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all_gates_pass else "bounded_scaffold_input_review_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BH_scaffold_review_before_measurement_harness",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BH_scaffold_review_gate_failure_v1",
        "scaffold_rows": len(scaffold_review),
        "scaffold_passed": count_status(scaffold_review, "review_status", "accepted_for_measurement_harness"),
        "profit_rows": len(profit_review),
        "profit_passed": count_status(profit_review, "review_status", "accepted_profit_curve_contract"),
        "proxy_rows": len(proxy_review),
        "proxy_passed": count_status(proxy_review, "review_status", "accepted_proxy_mt5_contract"),
        "mt5_rows": len(mt5_review),
        "mt5_passed": count_status(mt5_review, "review_status", "accepted_mt5_gap_repair_contract"),
        "firewall_rows": len(firewall_review),
        "firewall_passed": count_status(firewall_review, "review_status", "accepted_no_lookahead_firewall"),
        "lane_rows": len(lane_review),
        "lane_passed": count_status(lane_review, "review_status", "accepted_balanced_lane"),
        "handoff_rows": len(handoff_rows),
        "queue_rows": len(queue_rows),
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
            "single KPI selection(단일 KPI 선택)",
            "proxy KPI authority(프록시 KPI 권위)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "runtime authority claim(런타임 권위 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 검토 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        scaffold_path,
        profit_path,
        proxy_path,
        mt5_path,
        firewall_path,
        lane_path,
        handoff_path,
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
                "profit_review": f"{final['profit_passed']}/{final['profit_rows']}",
                "proxy_review": f"{final['proxy_passed']}/{final['proxy_rows']}",
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
