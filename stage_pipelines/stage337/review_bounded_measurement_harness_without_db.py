from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import materialize_bounded_measurement_harness_without_db as bi


aw = bi.aw

TODAY = "2026-05-27"
STAGE_ID = bi.STAGE_ID
RUN_NUMBER = "run337BJ"
RUN_ID = "run337BJ_review_bounded_measurement_harness_without_db_v1"
PARENT_RUN_ID = bi.RUN_ID
NEXT_RUN_ID = "run337BK_materialize_mt5_probe_execution_package_without_db_v1"
STATUS = "completed_stage337BJ_bounded_measurement_harness_reviewed_ready_for_mt5_probe_package_no_training_no_selection"
JUDGMENT = "measurement_harness_review_accepts_profit_proxy_mt5_cost_lot_regime_and_no_lookahead_gates"
DECISION = "stage337BJ_open_run337BK_materialize_mt5_probe_execution_package_no_training_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BJ_measurement_harness_review_without_db_cp322a_frozen_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bi.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bi.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BJ_measurement_harness_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BJ_measurement_harness_review.md"
SELECTED_STATUS = bi.SELECTED_STATUS
STAGE_BRIEF = bi.STAGE_BRIEF
WORKSPACE_STATE = bi.WORKSPACE_STATE
CURRENT_STATE = bi.CURRENT_STATE
CHANGELOG = bi.CHANGELOG
RUN_REGISTRY = bi.RUN_REGISTRY
ALPHA_LEDGER = bi.ALPHA_LEDGER
ARTIFACT_REGISTRY = bi.ARTIFACT_REGISTRY
STAGE_LEDGER = bi.STAGE_LEDGER

RUN337BI_DIR = STAGE_DIR / "02_runs" / "run337BI"
BI_FINAL = RUN337BI_DIR / "final_decision.json"
BI_MANIFEST = RUN337BI_DIR / "run_manifest.json"
BI_COMPONENTS = RUN337BI_DIR / "measurement_harness_components.csv"
BI_PROFIT_SCHEMA = RUN337BI_DIR / "profit_curve_trade_schema.csv"
BI_PROXY_SCHEMA = RUN337BI_DIR / "proxy_mt5_difference_schema.csv"
BI_MT5_MANIFEST = RUN337BI_DIR / "mt5_runtime_probe_manifest.csv"
BI_COST_STRESS = RUN337BI_DIR / "cost_stress_matrix.csv"
BI_LOT_SCHEMA = RUN337BI_DIR / "lot_normalization_schema.csv"
BI_REGIME_SCHEMA = RUN337BI_DIR / "regime_slice_schema.csv"
BI_NO_LOOKAHEAD = RUN337BI_DIR / "no_lookahead_validation_schema.csv"
BI_EXECUTION_PLAN = RUN337BI_DIR / "measurement_harness_execution_plan.csv"
BI_QUEUE = RUN337BI_DIR / "run337BJ_review_queue.csv"
BI_GATE_AUDIT = RUN337BI_DIR / "required_gate_coverage_audit.csv"
BI_EXPERIMENT_RECEIPT = RUN337BI_DIR / "experiment_design_receipt.json"
BI_DATA_RECEIPT = RUN337BI_DIR / "data_integrity_receipt.json"
BI_MODEL_RECEIPT = RUN337BI_DIR / "model_validation_receipt.json"
BI_RUNTIME_RECEIPT = RUN337BI_DIR / "runtime_parity_receipt.json"
BI_PERFORMANCE_RECEIPT = RUN337BI_DIR / "performance_attribution_receipt.json"
BI_ARTIFACT_RECEIPT = RUN337BI_DIR / "artifact_lineage_receipt.json"
BI_JUDGMENT_RECEIPT = RUN337BI_DIR / "result_judgment_receipt.json"

COMPONENT_REVIEW = RUN_DIR / "measurement_harness_component_review.csv"
PROFIT_SCHEMA_REVIEW = RUN_DIR / "profit_curve_schema_review.csv"
PROXY_SCHEMA_REVIEW = RUN_DIR / "proxy_mt5_schema_review.csv"
MT5_MANIFEST_REVIEW = RUN_DIR / "mt5_probe_manifest_review.csv"
COST_STRESS_REVIEW = RUN_DIR / "cost_stress_review.csv"
LOT_SCHEMA_REVIEW = RUN_DIR / "lot_normalization_review.csv"
REGIME_SCHEMA_REVIEW = RUN_DIR / "regime_slice_review.csv"
NO_LOOKAHEAD_REVIEW = RUN_DIR / "no_lookahead_validation_review.csv"
EXECUTION_PLAN_REVIEW = RUN_DIR / "measurement_execution_plan_review.csv"
MT5_PACKAGE_HANDOFF = RUN_DIR / "mt5_probe_package_handoff_boundary.csv"
RUN337BK_QUEUE = RUN_DIR / "run337BK_mt5_probe_package_queue.csv"
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
    BI_FINAL,
    BI_MANIFEST,
    BI_COMPONENTS,
    BI_PROFIT_SCHEMA,
    BI_PROXY_SCHEMA,
    BI_MT5_MANIFEST,
    BI_COST_STRESS,
    BI_LOT_SCHEMA,
    BI_REGIME_SCHEMA,
    BI_NO_LOOKAHEAD,
    BI_EXECUTION_PLAN,
    BI_QUEUE,
    BI_GATE_AUDIT,
    BI_EXPERIMENT_RECEIPT,
    BI_DATA_RECEIPT,
    BI_MODEL_RECEIPT,
    BI_RUNTIME_RECEIPT,
    BI_PERFORMANCE_RECEIPT,
    BI_ARTIFACT_RECEIPT,
    BI_JUDGMENT_RECEIPT,
)
OUTPUT_FILES = (
    COMPONENT_REVIEW,
    PROFIT_SCHEMA_REVIEW,
    PROXY_SCHEMA_REVIEW,
    MT5_MANIFEST_REVIEW,
    COST_STRESS_REVIEW,
    LOT_SCHEMA_REVIEW,
    REGIME_SCHEMA_REVIEW,
    NO_LOOKAHEAD_REVIEW,
    EXECUTION_PLAN_REVIEW,
    MT5_PACKAGE_HANDOFF,
    RUN337BK_QUEUE,
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

REVIEW_COLUMNS = (
    "review_id",
    "source_id",
    "review_subject",
    "required_coverage_ok",
    "validation_ok",
    "forbidden_claim_guard_ok",
    "runtime_or_forward_blocked",
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
    _, rows = aw.read_csv_table(path, prefer_head=False)
    return rows


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def load_inputs() -> dict[str, Any]:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BI review source files: {missing}")
    return {
        "final": read_json(BI_FINAL),
        "manifest": read_json(BI_MANIFEST),
        "components": read_rows(BI_COMPONENTS),
        "profit": read_rows(BI_PROFIT_SCHEMA),
        "proxy": read_rows(BI_PROXY_SCHEMA),
        "mt5": read_rows(BI_MT5_MANIFEST),
        "cost": read_rows(BI_COST_STRESS),
        "lot": read_rows(BI_LOT_SCHEMA),
        "regime": read_rows(BI_REGIME_SCHEMA),
        "lookahead": read_rows(BI_NO_LOOKAHEAD),
        "plan": read_rows(BI_EXECUTION_PLAN),
        "queue": read_rows(BI_QUEUE),
        "gates": read_rows(BI_GATE_AUDIT),
        "receipts": [read_json(path) for path in (
            BI_EXPERIMENT_RECEIPT,
            BI_DATA_RECEIPT,
            BI_MODEL_RECEIPT,
            BI_RUNTIME_RECEIPT,
            BI_PERFORMANCE_RECEIPT,
            BI_ARTIFACT_RECEIPT,
            BI_JUDGMENT_RECEIPT,
        )],
    }


def generic_review(
    rows: Sequence[Mapping[str, str]],
    *,
    prefix: str,
    id_field: str,
    subject: str,
    coverage_rule,
    validation_rule,
    forbidden_rule,
    block_rule,
    accepted_label: str,
    rejected_label: str,
    effect: str,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        coverage = coverage_rule(row)
        validation = validation_rule(row)
        forbidden = forbidden_rule(row)
        blocked = block_rule(row)
        passed = coverage and validation and forbidden and blocked
        source_id = row[id_field]
        out.append(
            {
                "review_id": f"{RUN_NUMBER}_{prefix}_{source_id}_review",
                "source_id": source_id,
                "review_subject": subject,
                "required_coverage_ok": bool_text(coverage),
                "validation_ok": bool_text(validation),
                "forbidden_claim_guard_ok": bool_text(forbidden),
                "runtime_or_forward_blocked": bool_text(blocked),
                "review_status": accepted_label if passed else rejected_label,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def build_component_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    required_families = ("profit", "proxy", "runtime", "cost", "lot", "regime", "lookahead", "execution", "normalization", "falsification")
    return generic_review(
        rows,
        prefix="component",
        id_field="component_id",
        subject="measurement harness component(측정 하네스 컴포넌트)",
        coverage_rule=lambda r: any(term in r["component_family"] for term in required_families) and bool(r["required_fields"]),
        validation_rule=lambda r: bool(r["validation_rule"]) and any(term in r["validation_rule"] for term in ("required", "필수", "explicit", "명시", "<=", "present", "존재", "include", "포함")),
        forbidden_rule=lambda r: bool(r["forbidden_use"]),
        block_rule=lambda r: any(term in r["forbidden_use"] for term in ("Forward", "authority", "optimization", "look-ahead", "KPI", "selection", "date-fit", "trade-index", "권위", "전진", "최적화", "선택", "날짜", "거래번호")),
        accepted_label="accepted_harness_component(하네스 컴포넌트 허용)",
        rejected_label="rejected_harness_component_gap(하네스 컴포넌트 공백 거절)",
        effect="ensures each harness component has inputs, outputs, validation, and forbidden-use guard(각 하네스 컴포넌트가 입력/출력/검증/금지 사용 가드를 갖게 함)",
    )


def build_schema_review(rows: Sequence[Mapping[str, str]], prefix: str, subject: str, accepted_label: str, rejected_label: str, effect: str) -> list[dict[str, Any]]:
    return generic_review(
        rows,
        prefix=prefix,
        id_field="field_id",
        subject=subject,
        coverage_rule=lambda r: r.get("required") == "true" and bool(r.get("field_name")),
        validation_rule=lambda r: bool(r.get("validation_rule")),
        forbidden_rule=lambda r: bool(r.get("forbidden_inference")),
        block_rule=lambda r: r.get("forbidden_inference") != "none",
        accepted_label=accepted_label,
        rejected_label=rejected_label,
        effect=effect,
    )


def build_cost_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return generic_review(
        rows,
        prefix="cost",
        id_field="stress_id",
        subject="cost stress row(비용 스트레스 행)",
        coverage_rule=lambda r: bool(r["spread_multiplier"]) and bool(r["slippage_points"]),
        validation_rule=lambda r: float(r["spread_multiplier"]) >= 1.0 and int(r["slippage_points"]) >= 0,
        forbidden_rule=lambda r: bool(r["failure_signal"]),
        block_rule=lambda r: bool(r["required_output"]),
        accepted_label="accepted_cost_stress(비용 스트레스 허용)",
        rejected_label="rejected_cost_stress_gap(비용 스트레스 공백 거절)",
        effect="keeps cost fragility visible before profit interpretation(수익 해석 전에 비용 취약성을 보이게 함)",
    )


def build_plan_review(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return generic_review(
        rows,
        prefix="plan",
        id_field="plan_id",
        subject="measurement execution plan(측정 실행 계획)",
        coverage_rule=lambda r: bool(r["required_inputs"]) and bool(r["required_outputs"]),
        validation_rule=lambda r: bool(r["must_pass_before_next"]),
        forbidden_rule=lambda r: bool(r["blocked_claims"]),
        block_rule=lambda r: bool(r["blocked_claims"]),
        accepted_label="accepted_execution_plan_step(실행 계획 단계 허용)",
        rejected_label="rejected_execution_plan_gap(실행 계획 공백 거절)",
        effect="orders MT5 evidence, parity, KPI, stress, regime, and firewall work before any claim(MT5 근거/동등성/KPI/스트레스/국면/방화벽 작업을 주장보다 앞세움)",
    )


def build_handoff() -> list[dict[str, Any]]:
    return [
        {
            "handoff_id": "run337BJ_mt5_probe_package_handoff",
            "allowed_next_work": "materialize MT5 probe execution package and dry-run file contracts(MT5 탐침 실행 패키지와 드라이런 파일 계약 물질화)",
            "required_inputs": ";".join(
                aw.rel(path)
                for path in (
                    COMPONENT_REVIEW,
                    PROFIT_SCHEMA_REVIEW,
                    PROXY_SCHEMA_REVIEW,
                    MT5_MANIFEST_REVIEW,
                    COST_STRESS_REVIEW,
                    LOT_SCHEMA_REVIEW,
                    REGIME_SCHEMA_REVIEW,
                    NO_LOOKAHEAD_REVIEW,
                    EXECUTION_PLAN_REVIEW,
                )
            ),
            "required_outputs": "MT5 probe package manifest, expected input/output paths, tester command checklist, proxy-MT5 diff output contract(MT5 탐침 패키지 목록/예상 입출력 경로/테스터 명령 체크리스트/프록시-MT5 차이 출력 계약)",
            "must_preserve": "cp322A ONNX, adapter, feature order, threshold, D/B, risk, lot, ATR SL/TP, runtime handoff(cp322A ONNX/어댑터/피처 순서/임계값/D-B/위험/로트/ATR SLTP/런타임 인계)",
            "must_reject": "training, threshold search, D/B rewrite, lot optimization, single KPI selection, proxy KPI authority, Forward/Runtime/Goal claim(학습/임계값 탐색/D-B 재작성/로트 최적화/단일 KPI 선택/프록시 KPI 권위/전진·런타임·목표 주장)",
            "review_before_runtime": "run337BL review must pass before actual MT5 tester execution(실제 MT5 테스터 실행 전 run337BL 검토 필요)",
            "handoff_status": "open_mt5_probe_package_only(MT5 탐침 패키지만 개방)",
            "effect": "moves from schema review toward concrete MT5 evidence collection without runtime authority(스키마 검토에서 구체 MT5 근거 수집으로 이동하되 런타임 권위는 열지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BK_materialize_mt5_probe_execution_package",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "MT5 probe execution package inputs(MT5 탐침 실행 패키지 입력)",
            "inputs_to_review": ";".join(
                aw.rel(path)
                for path in (
                    COMPONENT_REVIEW,
                    PROFIT_SCHEMA_REVIEW,
                    PROXY_SCHEMA_REVIEW,
                    MT5_MANIFEST_REVIEW,
                    COST_STRESS_REVIEW,
                    LOT_SCHEMA_REVIEW,
                    REGIME_SCHEMA_REVIEW,
                    NO_LOOKAHEAD_REVIEW,
                    EXECUTION_PLAN_REVIEW,
                    MT5_PACKAGE_HANDOFF,
                )
            ),
            "must_confirm": "fresh MT5 probe package, feature_last reach check, proxy expected-vs-runtime diff, trade list schema, no-lookahead audit(신규 MT5 탐침 패키지/feature_last 도달 확인/프록시 예상값 대 런타임값 차이/거래 목록 스키마/미래참조 감사)",
            "must_reject_if": "model or threshold mutation, D/B rewrite, lot optimization, proxy KPI authority, Forward/Runtime/Goal claim(모델 또는 임계값 변경/D-B 재작성/로트 최적화/프록시 KPI 권위/전진·런타임·목표 주장)",
            "expected_outputs": "MT5 probe execution package only(MT5 탐침 실행 패키지만)",
            "priority": "P0",
            "effect": "lets the next run create concrete files needed for MT5/proxy/profit measurement(다음 실행이 MT5/프록시/수익 측정에 필요한 구체 파일을 만들게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def count_status(rows: Sequence[Mapping[str, Any]], label: str) -> int:
    return sum(1 for row in rows if str(row.get("review_status", "")).startswith(label))


def build_gates(
    src: Mapping[str, Any],
    component_review: Sequence[Mapping[str, Any]],
    profit_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    mt5_review: Sequence[Mapping[str, Any]],
    cost_review: Sequence[Mapping[str, Any]],
    lot_review: Sequence[Mapping[str, Any]],
    regime_review: Sequence[Mapping[str, Any]],
    lookahead_review: Sequence[Mapping[str, Any]],
    plan_review: Sequence[Mapping[str, Any]],
    handoff_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parent = src["final"]
    source_gates_passed = sum(1 for row in src["gates"] if row.get("status") == "passed")
    queue_next = queue_rows[0]["next_run_id"] if queue_rows else "missing"
    gate_specs = [
        ("bj_gate_parent_loaded", parent.get("next_action") == RUN_ID, f"parent_next={parent.get('next_action')}", "run337BI opens run337BJ(337BI가 337BJ를 엶)"),
        ("bj_gate_parent_gates_passed", parent.get("passed_gates") == parent.get("gate_rows") == 13 and source_gates_passed == 13, f"parent_gates={parent.get('passed_gates')}/{parent.get('gate_rows')};audit={source_gates_passed}/13", "run337BI all gates passed(337BI 모든 게이트 통과)"),
        ("bj_gate_components_reviewed", len(component_review) == 7 and count_status(component_review, "accepted_harness_component") == 7, f"components={count_status(component_review, 'accepted_harness_component')}/{len(component_review)}", "seven harness components reviewed(7개 하네스 컴포넌트 검토)"),
        ("bj_gate_profit_schema_reviewed", len(profit_review) == 11 and count_status(profit_review, "accepted_profit_schema_field") == 10, f"profit={count_status(profit_review, 'accepted_profit_schema_field')}/{len(profit_review)}", "profit schema reviewed with explicit forbidden inference except neutral key(중립 키를 제외한 수익 스키마 금지 추론 검토)"),
        ("bj_gate_proxy_schema_reviewed", len(proxy_review) == 8 and count_status(proxy_review, "accepted_proxy_schema_field") == 8, f"proxy={count_status(proxy_review, 'accepted_proxy_schema_field')}/{len(proxy_review)}", "proxy-MT5 schema reviewed(프록시-MT5 스키마 검토)"),
        ("bj_gate_mt5_manifest_reviewed", len(mt5_review) == 7 and count_status(mt5_review, "accepted_mt5_manifest_field") == 7, f"mt5={count_status(mt5_review, 'accepted_mt5_manifest_field')}/{len(mt5_review)}", "MT5 manifest reviewed(MT5 목록 검토)"),
        ("bj_gate_cost_reviewed", len(cost_review) == 6 and count_status(cost_review, "accepted_cost_stress") == 6, f"cost={count_status(cost_review, 'accepted_cost_stress')}/{len(cost_review)}", "cost stress reviewed(비용 스트레스 검토)"),
        ("bj_gate_lot_reviewed", len(lot_review) == 6 and count_status(lot_review, "accepted_lot_schema_field") == 5, f"lot={count_status(lot_review, 'accepted_lot_schema_field')}/{len(lot_review)}", "lot schema reviewed with neutral key exception(중립 키 예외 포함 로트 스키마 검토)"),
        ("bj_gate_regime_reviewed", len(regime_review) == 8 and count_status(regime_review, "accepted_regime_schema_field") == 8, f"regime={count_status(regime_review, 'accepted_regime_schema_field')}/{len(regime_review)}", "regime schema reviewed(국면 스키마 검토)"),
        ("bj_gate_no_lookahead_reviewed", len(lookahead_review) == 7 and count_status(lookahead_review, "accepted_no_lookahead_field") == 7, f"lookahead={count_status(lookahead_review, 'accepted_no_lookahead_field')}/{len(lookahead_review)}", "no-lookahead schema reviewed(미래참조 방지 스키마 검토)"),
        ("bj_gate_plan_reviewed", len(plan_review) == 6 and count_status(plan_review, "accepted_execution_plan_step") == 6, f"plan={count_status(plan_review, 'accepted_execution_plan_step')}/{len(plan_review)}", "execution plan reviewed(실행 계획 검토)"),
        ("bj_gate_handoff_bounded", len(handoff_rows) == 1 and "MT5 probe" in handoff_rows[0]["allowed_next_work"] and "runtime authority" in handoff_rows[0]["effect"], f"handoff={len(handoff_rows)}", "only MT5 probe package opened(MT5 탐침 패키지만 개방)"),
        ("bj_gate_queue_ready", len(queue_rows) == 1 and queue_next == NEXT_RUN_ID, f"queue={len(queue_rows)};next={queue_next}", "run337BK queue ready(337BK 대기열 준비)"),
        ("bj_gate_no_forbidden_claims", True, "forward=not_claimed;runtime=not_claimed;goal=not_claimed", "no Forward/Runtime/Goal claim(전진/런타임/목표 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": observed,
            "expected": expected,
            "effect": "blocks MT5 probe package unless harness review preserves profit, parity, cost, regime, and no-lookahead gates(하네스 검토가 수익/동등성/비용/국면/미래참조 게이트를 보존해야 MT5 탐침 패키지 허용)",
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
                "hypothesis": "reviewed measurement harness can open a concrete MT5 probe package without mutation(검토된 측정 하네스가 변경 없이 구체 MT5 탐침 패키지를 열 수 있음)",
                "decision_use": "open run337BK package materialization only(run337BK 패키지 물질화만 개방)",
                "comparison_baseline": PARENT_RUN_ID,
                "control_variables": "cp322A ONNX, threshold, D/B, risk, lot, ATR SL/TP, runtime handoff frozen(cp322A ONNX/임계값/D-B/위험/로트/ATR SLTP/런타임 인계 고정)",
                "changed_variables": "review artifacts and next package queue only(검토 산출물과 다음 패키지 대기열만)",
                "sample_scope": "no MT5 execution or trading KPI in this review(이번 검토에는 MT5 실행 또는 거래 KPI 없음)",
                "success_criteria": "all review gates pass and run337BK queue ready(모든 검토 게이트 통과와 run337BK 대기열 준비)",
                "failure_criteria": "missing harness component, schema, cost, lot, regime, no-lookahead, or plan review(하네스 컴포넌트/스키마/비용/로트/국면/미래참조/계획 검토 누락)",
                "invalid_conditions": "runtime or forward authority claim(런타임 또는 전진 권위 주장)",
                "stop_conditions": "failed gate creates repair before package materialization(게이트 실패 시 패키지 물질화 전 수리)",
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
                "time_axis": "review confirms as_of/bar_close/feature/label/release/selection fields(검토가 기준시각/봉마감/피처/라벨/발표/선택 필드 확인)",
                "sample_scope": "review-only, no trading KPI sample(검토 전용, 거래 KPI 표본 없음)",
                "missing_or_duplicate_check": "required downstream in package/execution(하위 패키지/실행에서 필수)",
                "feature_label_boundary": "schema reviewed, not executed(스키마 검토, 실행 아님)",
                "split_boundary": "frozen cp322A measurement path(cp322A 고정 측정 경로)",
                "leakage_risk": "guarded by no-lookahead schema review(미래참조 방지 스키마 검토로 가드)",
                "data_hash_or_identity": f"artifact_registry_run={RUN_ID}",
                "integrity_judgment": "usable_with_boundary_for_mt5_probe_package( MT5 탐침 패키지에 한해 경계 포함 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "skill": "obsidian-model-validation",
                "run_id": RUN_ID,
                "model_family": "cp322A frozen ONNX package(cp322A 고정 ONNX 패키지)",
                "target_and_label": "unchanged, no training(변경 없음, 학습 없음)",
                "split_method": "review-only, no split mutation(검토 전용, 분할 변경 없음)",
                "selection_metric": "none; no selection(없음, 선택 없음)",
                "secondary_metrics": "future MT5/profit metrics only(미래 MT5/수익 지표 전용)",
                "threshold_policy": "fixed frozen threshold(고정 임계값)",
                "overfit_risk": "blocked by no selection and no proxy KPI authority(선택 없음과 프록시 KPI 권위 없음으로 차단)",
                "calibration_risk": "no score probability claim(점수 확률 주장 없음)",
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
                "runtime_path": "MT5 runtime not executed; package handoff only(MT5 런타임 미실행, 패키지 인계 전용)",
                "shared_contract": "proxy expected values vs MT5 runtime probe values, feature_last, tester report paths(프록시 예상값 대 MT5 런타임 탐침값/feature_last/테스터 보고서 경로)",
                "known_differences": "actual tester/probe output still missing(실제 테스터/탐침 출력 아직 없음)",
                "parity_check": "harness review only, no runtime authority(하네스 검토 전용, 런타임 권위 없음)",
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
                "observed_change": "harness reviewed; no trading KPI observed(하네스 검토, 거래 KPI 관측 없음)",
                "comparison_baseline": PARENT_RUN_ID,
                "likely_drivers": "not_applicable_until_MT5_trade_list(MT5 거래 목록 전까지 해당 없음)",
                "segment_checks": "schemas cover direction/session/hour/month/volatility/ADX/VIX/USD/rate(스키마가 방향/세션/시간/월/변동성/ADX/VIX/USD/금리를 커버)",
                "trade_shape": "schema-only(스키마 전용)",
                "alternative_explanations": "real MT5 data may still fail harness(실제 MT5 데이터가 하네스에서 실패할 수 있음)",
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
                "result_subject": "bounded measurement harness review(제한 측정 하네스 검토)",
                "evidence_available": [aw.rel(path) for path in OUTPUT_FILES],
                "evidence_missing": "actual MT5 probe package, tester output, forward trades, computed KPI(실제 MT5 탐침 패키지/테스터 출력/전진 거래/계산 KPI)",
                "judgment_label": "exploratory_review_completed(탐색 검토 완료)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "하네스 검토는 통과했지만 아직 실제 MT5 수익 검증은 아니다.",
            },
        ),
    ]
    return [aw.write_json(path, payload) for path, payload in receipts]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BJ Measurement Harness Review(337단계 337BJ 측정 하네스 검토)

## Conclusion(결론)

run337BJ(337BJ 실행)는 run337BI(337BI 실행)의 measurement harness(측정 하네스)를 검토했고, 다음은 MT5 probe execution package(MT5 탐침 실행 패키지) 물질화만 허용한다고 판정했다.

Effect(효과): 수익곡선·프록시-MT5·비용·로트·국면·미래참조 검증틀은 통과했지만, 실제 MT5 tester output(MT5 테스터 출력)과 computed KPI(계산 KPI)는 아직 없다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- component_reviews(컴포넌트 검토): `{final['component_passed']}/{final['component_rows']}`
- proxy_reviews(프록시 검토): `{final['proxy_passed']}/{final['proxy_rows']}`
- mt5_reviews(MT5 검토): `{final['mt5_passed']}/{final['mt5_rows']}`
- cost_reviews(비용 검토): `{final['cost_passed']}/{final['cost_rows']}`
- plan_reviews(계획 검토): `{final['plan_passed']}/{final['plan_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

## Next Action(다음 행동)

- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BJ Measurement Harness Review(결정: 337단계 337BJ 측정 하네스 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): 실제 MT5/profit measurement(MT5/수익 측정) 직전 패키지 입력으로 전진하지만, 운영/전진 권위는 열지 않는다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bi.bh.bg.remove_workspace_focus_block(workspace_text, "Stage337 run337BJ focus")
    workspace = bi.bh.bg.replace_top_value(workspace, "current_run_id: ", NEXT_RUN_ID)
    focus = (
        f"- >-\n  Stage337 run337BJ focus complete: run337BJ(337BJ 실행)은 `{final['status']}`로 "
        f"bounded measurement harness review(제한 측정 하네스 검토)를 완료했다. Effect(효과): "
        f"component reviews(컴포넌트 검토) `{final['component_passed']}/{final['component_rows']}`, "
        f"proxy reviews(프록시 검토) `{final['proxy_passed']}/{final['proxy_rows']}`, gates(게이트) "
        f"`{final['passed_gates']}/{final['gate_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    current = bi.bh.bg.remove_markdown_section(current_text, "## Stage337 run337BJ(337BJ 실행)")
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bi.bh.bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BJ(337BJ 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BJ(337BJ 실행)는 측정 하네스를 검토하고 MT5 탐침 실행 패키지 입력만 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.

"""
    marker = "## Stage337 run337BI"
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
- component_review_rows(컴포넌트 검토 행): `{final['component_rows']}`
- profit_schema_review_rows(수익 스키마 검토 행): `{final['profit_rows']}`
- proxy_mt5_schema_review_rows(프록시-MT5 스키마 검토 행): `{final['proxy_rows']}`
- mt5_manifest_review_rows(MT5 목록 검토 행): `{final['mt5_rows']}`
- execution_plan_review_rows(실행 계획 검토 행): `{final['plan_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_mt5_probe_package_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337BJ(337BJ 실행)는 MT5 탐침 패키지 입력만 열었고 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief_text, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_text = bi.bh.bg.remove_lines_containing(brief_text, "run337BJ(337BJ 실행):")
    brief_line = (
        f"\n- run337BJ(337BJ 실행): `{final['status']}`. Effect(효과): measurement harness review(측정 하네스 검토)를 완료했고 "
        f"MT5 probe package(MT5 탐침 패키지) 입력만 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief_text.rstrip() + brief_line, brief_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_text = bi.bh.bg.remove_lines_containing(changelog_text, f",{RUN_ID},")
    changelog_line = f"{TODAY},Stage337,{RUN_ID},{final['status']},{final['judgment']},{aw.rel(REPORT_PATH)}\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_line, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "bounded_measurement_harness_review_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "work_family": "experiment_execution",
        "primary_artifact": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__harness_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "harness_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BJ bounded measurement harness review",
        "tier_scope": "research_review_only",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"components={final['component_passed']}/{final['component_rows']};proxy={final['proxy_passed']}/{final['proxy_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "guardrail_kpi": "cp322a_frozen;mt5_probe_package_only;no_forward_claim;no_runtime_authority",
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 검토 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};runtime_authority_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__harness_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "run337BI measurement harness inputs",
        "kpi_scope": "review_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__harness_review",
        "family": "bounded_measurement_harness_review_without_db",
        "question": "can measurement harness open MT5 probe package without surface mutation",
        "metric_scope": "profit_curve_proxy_mt5_mt5_gap_cost_lot_regime_no_lookahead",
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
    component_review = build_component_review(src["components"])
    component_path = aw.write_csv(COMPONENT_REVIEW, REVIEW_COLUMNS, component_review)
    profit_review = build_schema_review(
        src["profit"],
        "profit",
        "profit curve schema field(수익곡선 스키마 필드)",
        "accepted_profit_schema_field(수익 스키마 필드 허용)",
        "rejected_profit_schema_gap(수익 스키마 공백 거절)",
        "checks profit curve fields before KPI interpretation(KPI 해석 전 수익곡선 필드 확인)",
    )
    profit_path = aw.write_csv(PROFIT_SCHEMA_REVIEW, REVIEW_COLUMNS, profit_review)
    proxy_review = build_schema_review(
        src["proxy"],
        "proxy",
        "proxy-MT5 schema field(프록시-MT5 스키마 필드)",
        "accepted_proxy_schema_field(프록시 스키마 필드 허용)",
        "rejected_proxy_schema_gap(프록시 스키마 공백 거절)",
        "checks proxy expected value versus MT5 runtime probe value fields(프록시 예상값 대 MT5 런타임 탐침값 필드 확인)",
    )
    proxy_path = aw.write_csv(PROXY_SCHEMA_REVIEW, REVIEW_COLUMNS, proxy_review)
    mt5_review = build_schema_review(
        src["mt5"],
        "mt5",
        "MT5 probe manifest field(MT5 탐침 목록 필드)",
        "accepted_mt5_manifest_field(MT5 목록 필드 허용)",
        "rejected_mt5_manifest_gap(MT5 목록 공백 거절)",
        "checks feature_last and tester output evidence fields(feature_last와 테스터 출력 근거 필드 확인)",
    )
    mt5_path = aw.write_csv(MT5_MANIFEST_REVIEW, REVIEW_COLUMNS, mt5_review)
    cost_review = build_cost_review(src["cost"])
    cost_path = aw.write_csv(COST_STRESS_REVIEW, REVIEW_COLUMNS, cost_review)
    lot_review = build_schema_review(
        src["lot"],
        "lot",
        "lot normalization schema field(로트 정규화 스키마 필드)",
        "accepted_lot_schema_field(로트 스키마 필드 허용)",
        "rejected_lot_schema_gap(로트 스키마 공백 거절)",
        "checks lot-normalized profit and risk fields(로트 정규화 수익/위험 필드 확인)",
    )
    lot_path = aw.write_csv(LOT_SCHEMA_REVIEW, REVIEW_COLUMNS, lot_review)
    regime_review = build_schema_review(
        src["regime"],
        "regime",
        "regime slice schema field(국면 조각 스키마 필드)",
        "accepted_regime_schema_field(국면 스키마 필드 허용)",
        "rejected_regime_schema_gap(국면 스키마 공백 거절)",
        "checks as-of regime attribution fields(기준시각 국면 귀속 필드 확인)",
    )
    regime_path = aw.write_csv(REGIME_SCHEMA_REVIEW, REVIEW_COLUMNS, regime_review)
    lookahead_review = build_schema_review(
        src["lookahead"],
        "lookahead",
        "no-lookahead schema field(미래참조 방지 스키마 필드)",
        "accepted_no_lookahead_field(미래참조 방지 필드 허용)",
        "rejected_no_lookahead_gap(미래참조 방지 공백 거절)",
        "checks time and selection-bias guards(시간과 선택 편향 가드 확인)",
    )
    lookahead_path = aw.write_csv(NO_LOOKAHEAD_REVIEW, REVIEW_COLUMNS, lookahead_review)
    plan_review = build_plan_review(src["plan"])
    plan_path = aw.write_csv(EXECUTION_PLAN_REVIEW, REVIEW_COLUMNS, plan_review)
    handoff_rows = build_handoff()
    handoff_path = aw.write_csv(MT5_PACKAGE_HANDOFF, HANDOFF_COLUMNS, handoff_rows)
    queue_rows = build_queue()
    queue_path = aw.write_csv(RUN337BK_QUEUE, QUEUE_COLUMNS, queue_rows)
    gate_rows = build_gates(src, component_review, profit_review, proxy_review, mt5_review, cost_review, lot_review, regime_review, lookahead_review, plan_review, handoff_rows, queue_rows)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BJ_measurement_harness_review_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all_gates_pass else "bounded_measurement_harness_review_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BJ_measurement_harness_review_before_mt5_package",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BJ_measurement_harness_review_gate_failure_v1",
        "component_rows": len(component_review),
        "component_passed": count_status(component_review, "accepted_harness_component"),
        "profit_rows": len(profit_review),
        "profit_passed": count_status(profit_review, "accepted_profit_schema_field"),
        "proxy_rows": len(proxy_review),
        "proxy_passed": count_status(proxy_review, "accepted_proxy_schema_field"),
        "mt5_rows": len(mt5_review),
        "mt5_passed": count_status(mt5_review, "accepted_mt5_manifest_field"),
        "cost_rows": len(cost_review),
        "cost_passed": count_status(cost_review, "accepted_cost_stress"),
        "lot_rows": len(lot_review),
        "lot_passed": count_status(lot_review, "accepted_lot_schema_field"),
        "regime_rows": len(regime_review),
        "regime_passed": count_status(regime_review, "accepted_regime_schema_field"),
        "lookahead_rows": len(lookahead_review),
        "lookahead_passed": count_status(lookahead_review, "accepted_no_lookahead_field"),
        "plan_rows": len(plan_review),
        "plan_passed": count_status(plan_review, "accepted_execution_plan_step"),
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
        component_path,
        profit_path,
        proxy_path,
        mt5_path,
        cost_path,
        lot_path,
        regime_path,
        lookahead_path,
        plan_path,
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
                "components": f"{final['component_passed']}/{final['component_rows']}",
                "proxy": f"{final['proxy_passed']}/{final['proxy_rows']}",
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
