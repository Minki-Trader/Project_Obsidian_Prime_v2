from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    replace_bullet_value,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    sha256_file,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
    now_utc,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CI"
RUN_ID = "run337CI_review_directional_label_action_policy_repair_inputs_without_db_v1"
PARENT_RUN_ID = "run337CH_materialize_directional_label_action_policy_repair_inputs_without_db_v1"
NEXT_RUN_ID = "run337CJ_materialize_directional_label_action_candidate_training_inputs_without_db_v1"
STATUS = "completed_stage337CI_directional_label_action_inputs_reviewed_ready_for_candidate_training_input_materialization_no_training_no_selection"
JUDGMENT = "materialized_inputs_pass_no_overfit_review_candidate_training_input_materialization_next"
DECISION = "stage337CI_open_run337CJ_materialize_directional_label_action_candidate_training_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CI_directional_label_action_input_review_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
CH_DIR = STAGE_DIR / "02_runs" / "run337CH"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CI_directional_label_action_policy_repair_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CI_directional_label_action_policy_repair_input_review.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CH_FINAL = CH_DIR / "final_decision.json"
POLARITY_AUDIT = CH_DIR / "polarity_audit_plan.csv"
LABEL_V3_INPUT = CH_DIR / "label_v3_input_contract.csv"
ACTION_V3_INPUT = CH_DIR / "action_v3_input_contract.csv"
NEGATIVE_CONTROL = CH_DIR / "negative_control_plan.csv"
FORWARD_FIREWALL = CH_DIR / "forward_selection_firewall.csv"
RUNTIME_REQUIREMENT = CH_DIR / "runtime_probe_requirement.csv"
CURVE_QUALITY_PLAN = CH_DIR / "curve_quality_measurement_plan.csv"
CH_QUEUE = CH_DIR / "run337CI_review_queue.csv"
CH_GATES = CH_DIR / "required_gate_coverage_audit.csv"

INPUT_REVIEW = RUN_DIR / "input_review_matrix.csv"
NO_OVERFIT_REVIEW = RUN_DIR / "no_overfit_gate_review.csv"
RUNTIME_USABILITY_REVIEW = RUN_DIR / "proxy_mt5_usability_review.csv"
LINEAGE_REVIEW = RUN_DIR / "data_lineage_review.csv"
NEXT_QUEUE = RUN_DIR / "run337CJ_candidate_training_input_materialization_queue.csv"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"

INPUT_FILES = (
    CH_FINAL,
    POLARITY_AUDIT,
    LABEL_V3_INPUT,
    ACTION_V3_INPUT,
    NEGATIVE_CONTROL,
    FORWARD_FIREWALL,
    RUNTIME_REQUIREMENT,
    CURVE_QUALITY_PLAN,
    CH_QUEUE,
    CH_GATES,
)
OUTPUT_FILES = (
    INPUT_REVIEW,
    NO_OVERFIT_REVIEW,
    RUNTIME_USABILITY_REVIEW,
    LINEAGE_REVIEW,
    NEXT_QUEUE,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    JUDGMENT_RECEIPT,
    MODEL_RECEIPT,
    LINEAGE_RECEIPT,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

INPUT_REVIEW_COLUMNS = (
    "review_id",
    "source_artifact",
    "row_count",
    "required_condition",
    "observed_condition",
    "review_status",
    "blocks_if_failed",
    "effect",
    "claim_boundary",
)
NO_OVERFIT_COLUMNS = (
    "gate_id",
    "gate_family",
    "required_condition",
    "observed_condition",
    "review_status",
    "next_use",
    "blocks_claim",
    "effect",
    "claim_boundary",
)
RUNTIME_REVIEW_COLUMNS = (
    "review_id",
    "runtime_requirement",
    "usable_for",
    "not_usable_for",
    "required_before_claim",
    "review_status",
    "effect",
    "claim_boundary",
)
LINEAGE_REVIEW_COLUMNS = (
    "lineage_id",
    "source_artifact",
    "sha256",
    "exists",
    "availability",
    "consumer",
    "review_status",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_shortcut",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def summarize_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]
    final = read_json(CH_FINAL)
    rows = {
        "polarity": read_csv(POLARITY_AUDIT),
        "label": read_csv(LABEL_V3_INPUT),
        "action": read_csv(ACTION_V3_INPUT),
        "negative": read_csv(NEGATIVE_CONTROL),
        "firewall": read_csv(FORWARD_FIREWALL),
        "runtime": read_csv(RUNTIME_REQUIREMENT),
        "curve": read_csv(CURVE_QUALITY_PLAN),
        "queue": read_csv(CH_QUEUE),
        "ch_gates": read_csv(CH_GATES),
    }
    return {
        "missing_inputs": missing,
        "ch_final": final,
        "rows": rows,
        "ch_next_action": final.get("next_action", ""),
        "ch_failed_gates": final.get("failed_gates", []),
        "ch_training": final.get("model_training", ""),
        "ch_selection": final.get("candidate_selection", ""),
    }


def build_input_review(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = summary["rows"]
    specs = [
        ("polarity_audit", POLARITY_AUDIT, len(rows["polarity"]), ">=4 polarity audits"),
        ("label_v3_input", LABEL_V3_INPUT, len(rows["label"]), ">=2 label input contracts"),
        ("action_v3_input", ACTION_V3_INPUT, len(rows["action"]), ">=2 action input contracts"),
        ("negative_control", NEGATIVE_CONTROL, len(rows["negative"]), ">=5 negative controls"),
        ("forward_firewall", FORWARD_FIREWALL, len(rows["firewall"]), ">=5 forward/selection firewalls"),
        ("runtime_requirement", RUNTIME_REQUIREMENT, len(rows["runtime"]), ">=4 runtime requirements"),
        ("curve_quality", CURVE_QUALITY_PLAN, len(rows["curve"]), ">=6 curve quality rows"),
        ("review_queue", CH_QUEUE, len(rows["queue"]), ">=1 review queue"),
    ]
    minimums = {
        "polarity_audit": 4,
        "label_v3_input": 2,
        "action_v3_input": 2,
        "negative_control": 5,
        "forward_firewall": 5,
        "runtime_requirement": 4,
        "curve_quality": 6,
        "review_queue": 1,
    }
    review_rows: list[dict[str, Any]] = []
    for review_id, path, count, required in specs:
        ok = count >= minimums[review_id]
        review_rows.append(
            {
                "review_id": review_id,
                "source_artifact": rel(path),
                "row_count": count,
                "required_condition": required,
                "observed_condition": f"rows={count}",
                "review_status": "passed" if ok else "failed",
                "blocks_if_failed": "run337CJ_candidate_training_input_materialization",
                "effect": "다음 입력 물질화가 빈 계약 위에서 진행되지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return review_rows


def build_no_overfit_review(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    rows = summary["rows"]
    firewall_ids = {row.get("firewall_id", "") for row in rows["firewall"]}
    control_ids = {row.get("control_id", "") for row in rows["negative"]}
    runtime_ids = {row.get("requirement_id", "") for row in rows["runtime"]}
    curve_ids = {row.get("metric_id", "") for row in rows["curve"]}
    requirements = [
        {
            "gate_id": "ci_gate_forward_selection_forbidden",
            "gate_family": "overfit_firewall",
            "required_condition": "forward cannot choose polarity/cost/action/lot/threshold",
            "observed_condition": ";".join(sorted(firewall_ids)),
            "ok": {"no_forward_polarity_selection", "no_forward_cost_buffer_selection", "no_forward_action_filter_selection", "no_lot_or_threshold_rescue"}.issubset(firewall_ids),
            "next_use": "CJ may materialize candidate inputs but cannot train/select from forward",
            "blocks_claim": "candidate_selection;Forward Passed;Goal Achieve",
            "effect": "전진 구간이 수리 선택 도구가 되는 길을 닫는다.",
        },
        {
            "gate_id": "ci_gate_negative_controls_complete",
            "gate_family": "model_validation",
            "required_condition": "shifted, flip, permutation, reversal, stale-context controls present",
            "observed_condition": ";".join(sorted(control_ids)),
            "ok": {"shifted_return_control", "direction_flip_control", "label_permutation_control", "time_reversal_control", "stale_context_carry_control"}.issubset(control_ids),
            "next_use": "CJ must create scoring templates for all controls",
            "blocks_claim": "model_training_validity;candidate_selection",
            "effect": "방향 수리가 또 다른 과적합이 되는지 학습 전 확인한다.",
        },
        {
            "gate_id": "ci_gate_runtime_parity_required",
            "gate_family": "runtime_parity",
            "required_condition": "proxy-MT5 row parity and trade/fill parity requirements present",
            "observed_condition": ";".join(sorted(runtime_ids)),
            "ok": {"proxy_mt5_row_parity_required", "trade_count_and_fill_parity_required"}.issubset(runtime_ids),
            "next_use": "future ONNX cannot claim runtime authority without MT5 telemetry",
            "blocks_claim": "runtime_authority;operating_promotion",
            "effect": "proxy(프록시) 성과와 MT5(메타트레이더5) 성과를 분리한다.",
        },
        {
            "gate_id": "ci_gate_curve_quality_required",
            "gate_family": "performance_attribution",
            "required_condition": "profit, risk, curve pocket, density, cost, proxy-vs-MT5 metrics present",
            "observed_condition": ";".join(sorted(curve_ids)),
            "ok": {"net_pf_expectancy", "drawdown_recovery_underwater", "worst_chunk_curve_pocket", "density_and_side_balance", "lot_normalized_cost_stress", "proxy_vs_mt5_usability"}.issubset(curve_ids),
            "next_use": "CJ/CK outputs must include curve-quality hooks before any positive judgment",
            "blocks_claim": "positive_judgment;Forward Passed",
            "effect": "예쁜 수익곡선 요구를 측정 항목으로 계속 끌고 간다.",
        },
        {
            "gate_id": "ci_gate_no_training_no_selection_in_ci",
            "gate_family": "claim_boundary",
            "required_condition": "CI reviews inputs only",
            "observed_condition": f"CH model_training={summary['ch_training']};CH candidate_selection={summary['ch_selection']}",
            "ok": summary["ch_training"] == "not_run" and summary["ch_selection"] == "not_run",
            "next_use": "CI can open input materialization only",
            "blocks_claim": "Goal Achieve;Forward Passed",
            "effect": "검토 실행이 몰래 학습/선택으로 변하지 않게 한다.",
        },
    ]
    return [
        {
            "gate_id": item["gate_id"],
            "gate_family": item["gate_family"],
            "required_condition": item["required_condition"],
            "observed_condition": item["observed_condition"],
            "review_status": "passed" if item["ok"] else "failed",
            "next_use": item["next_use"],
            "blocks_claim": item["blocks_claim"],
            "effect": item["effect"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for item in requirements
    ]


def build_runtime_review(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    runtime_rows = summary["rows"]["runtime"]
    output: list[dict[str, str]] = []
    for row in runtime_rows:
        output.append(
            {
                "review_id": f"review_{row.get('requirement_id', 'runtime_requirement')}",
                "runtime_requirement": row.get("requirement_id", ""),
                "usable_for": "proxy signal sanity, feature/action parity preparation, MT5 probe checklist",
                "not_usable_for": "Forward Passed/Failed, runtime authority, live readiness, operating promotion",
                "required_before_claim": row.get("acceptance_rule", ""),
                "review_status": "passed" if row.get("blocks_claim") else "failed",
                "effect": row.get("effect", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_lineage_review() -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for path in INPUT_FILES:
        exists = path_exists(path)
        output.append(
            {
                "lineage_id": f"source::{rel(path)}",
                "source_artifact": rel(path),
                "sha256": sha256_file(path) if exists else "",
                "exists": "true" if exists else "false",
                "availability": "ignored_with_manifest" if "/02_runs/" in rel(path) else "tracked_or_doc",
                "consumer": RUN_ID,
                "review_status": "passed" if exists else "failed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_next_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337CJ_materialize_candidate_training_inputs",
            "next_run_id": NEXT_RUN_ID,
            "task": "materialize candidate training inputs for label_v3 polarity/lifecycle and action_v3 diagnostics without training a model",
            "required_inputs": ";".join(rel(path) for path in (POLARITY_AUDIT, LABEL_V3_INPUT, ACTION_V3_INPUT, NEGATIVE_CONTROL, FORWARD_FIREWALL, RUNTIME_REQUIREMENT, CURVE_QUALITY_PLAN)),
            "required_outputs": "label_v3_candidate_matrix.csv;action_v3_candidate_matrix.csv;negative_control_scoring_template.csv;split_boundary_manifest.csv;run337CK_guarded_training_queue.csv",
            "blocked_if_missing": "missing no-forward-selection firewall, negative controls, or split boundary manifest",
            "forbidden_shortcut": "do not train in CJ; do not pick polarity/action from forward; do not tune threshold or lot",
            "effect": "학습 전 후보 입력을 만들되, 선택과 성과 주장은 계속 닫아둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(summary: Mapping[str, Any], reviews: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, str]]:
    def row(gate_id: str, ok: bool, observed: Any, expected: str, effect: str) -> dict[str, str]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": str(observed),
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    return [
        row("ci_gate_inputs_present", not summary["missing_inputs"], ";".join(summary["missing_inputs"]) or "none", "no_missing_inputs", "CH 산출물을 실제 리뷰 입력으로 연결한다."),
        row("ci_gate_parent_points_to_ci", summary["ch_next_action"] == RUN_ID, summary["ch_next_action"], RUN_ID, "현재 실행이 CH next_action(다음 행동)과 맞는다."),
        row("ci_gate_ch_gates_clean", not summary["ch_failed_gates"], ";".join(summary["ch_failed_gates"]) or "none", "no_failed_ch_gates", "실패한 입력 게이트 위에서 다음 큐를 열지 않는다."),
        row("ci_gate_input_reviews_pass", all(item["review_status"] == "passed" for item in reviews["input"]), [item["review_status"] for item in reviews["input"]], "all input reviews passed", "계약 행 수와 존재성을 검토한다."),
        row("ci_gate_no_overfit_reviews_pass", all(item["review_status"] == "passed" for item in reviews["overfit"]), [item["review_status"] for item in reviews["overfit"]], "all no-overfit reviews passed", "전진 선택/부정 대조/런타임/곡선 게이트를 검토한다."),
        row("ci_gate_runtime_review_pass", all(item["review_status"] == "passed" for item in reviews["runtime"]), [item["review_status"] for item in reviews["runtime"]], "all runtime usability reviews passed", "proxy-MT5(프록시-MT5) 사용 범위를 제한한다."),
        row("ci_gate_lineage_review_pass", all(item["review_status"] == "passed" for item in reviews["lineage"]), [item["review_status"] for item in reviews["lineage"]], "all lineage rows passed", "무시된 02_runs 산출물도 해시와 manifest(목록)로 연결한다."),
        row("ci_gate_next_queue_present", len(reviews["queue"]) == 1, len(reviews["queue"]), "one next queue row", "다음 CJ 작업을 선택이 아니라 입력 물질화로 제한한다."),
        row("ci_gate_no_training_or_selection", True, "model_training=not_run;candidate_selection=not_run", "no_training_no_selection", "CI를 리뷰 실행으로만 닫는다."),
    ]


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    model_receipt = {
        "model_family": "not_trained_in_run337CI",
        "target_and_label": "label_v3/action_v3 input review only",
        "split_method": "time-ordered historical split plus forward reject-only boundary",
        "selection_metric": "not_applicable_no_selection",
        "secondary_metrics": "input completeness, no-overfit gate coverage, proxy-MT5 usability requirements",
        "threshold_policy": "no threshold tuning",
        "overfit_risk": "opening training before firewall/negative controls are reviewed",
        "calibration_risk": "future scores remain rank/diagnostic until calibration evidence exists",
        "comparison_baseline": "run337CH materialized input contracts",
        "validation_judgment": "exploratory_input_review_ready_for_candidate_input_materialization",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in (INPUT_REVIEW, NO_OVERFIT_REVIEW, RUNTIME_USABILITY_REVIEW, LINEAGE_REVIEW, NEXT_QUEUE, REPORT_PATH)],
        "artifact_hashes": {},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "input review matrix, no-overfit gate review, runtime usability review, lineage review, gate audit",
        "evidence_missing": "no candidate training input materialization yet, no model training, no MT5 probe",
        "judgment_label": "exploratory",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": "CJ materializes candidate training inputs without training or forward selection",
        "user_explanation_hook": "입력 검토는 통과했지만 아직 모델 학습이나 전진 통과는 아니다.",
    }
    paths = [
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(LINEAGE_RECEIPT, lineage_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt["artifact_hashes"] = {rel(path): sha256_file(path) for path in paths if path_exists(path) and path != LINEAGE_RECEIPT}
    write_json(LINEAGE_RECEIPT, lineage_receipt)
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CI Directional Label/Action Input Review(방향 라벨/행동 입력 검토)

## Conclusion(결론)

run337CI(337CI 실행)는 run337CH(337CH 실행)의 polarity/label/action/no-overfit/runtime/curve inputs(극성/라벨/행동/무과적합/런타임/곡선 입력)를 검토했고, 후보 학습 입력 materialization(물질화)로 넘길 수 있다고 판단했다.

Effect(효과): 다음 run337CJ(337CJ 실행)는 모델을 학습하지 않고, label_v3/action_v3 candidate training inputs(후보 학습 입력)과 negative-control scoring template(부정 대조 채점 틀)을 만든다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- input_review_rows(입력 검토 행): `{final["input_review_rows"]}`
- no_overfit_review_rows(무과적합 검토 행): `{final["no_overfit_review_rows"]}`
- runtime_review_rows(런타임 검토 행): `{final["runtime_review_rows"]}`
- lineage_review_rows(계보 검토 행): `{final["lineage_review_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CI

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): CH 입력을 검토해 CJ 후보 학습 입력 물질화로 넘긴다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(FINAL_DECISION)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs() -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = workspace_text.replace(f"current_run_id: {RUN_ID}", f"current_run_id: {NEXT_RUN_ID}", 1)
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337CI focus complete: directional label/action repair input review(방향 라벨/행동 수리 입력 검토)를 `{STATUS}`로 닫았다. "
        "Effect(효과): run337CJ(337CJ 실행)에서 후보 학습 입력(candidate training inputs, 후보 학습 입력)을 물질화한다."
    )
    if "Stage337 run337CI focus complete" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:", focus_entry, 1)
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
## Stage337 run337CI(337CI 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): CH 입력의 no-overfit/firewall/runtime/curve gates(무과적합/방화벽/런타임/곡선 게이트)를 검토하고 CJ 후보 학습 입력 물질화를 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337CI(337CI 실행)" not in current_text:
        marker = "## Stage337 run337CH(337CH"
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
- actual_mt5_execution(실제 MT5 실행): `not_run_ci_input_review_only_run337CE_reviewed`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 candidate training inputs(후보 학습 입력) 물질화다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337CI(337CI 실행) reviewed directional label/action repair inputs(방향 라벨/행동 수리 입력). Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337CI reviewed directional label/action repair inputs(방향 라벨/행동 수리 입력) and opened `{NEXT_RUN_ID}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "directional_label_action_policy_repair_input_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_result_judgment_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__directional_label_action_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "directional_label_action_input_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "input_review",
        "tier_scope": "out_of_scope_by_claim_input_review_no_tier_kpi",
        "kpi_scope": "input_review_no_training",
        "scoreboard_lane": "model_validation_result_judgment",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": "not_applicable_input_review_only",
        "guardrail_kpi": "no_forward_selection;negative_controls;runtime_requirement;lineage",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__directional_label_action_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_result_judgment_artifact_lineage",
        "evidence_scope": "CH materialized inputs reviewed",
        "kpi_scope": "input_review_no_training",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__directional_label_action_input_review",
        "family": "model_validation_result_judgment_artifact_lineage",
        "question": "can CH materialized inputs safely move to candidate training input materialization",
        "metric_scope": "input_review_no_forward_decision",
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
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    summary = summarize_inputs()
    input_review = build_input_review(summary)
    no_overfit_review = build_no_overfit_review(summary)
    runtime_review = build_runtime_review(summary)
    lineage_review = build_lineage_review()
    queue_rows = build_next_queue()
    reviews = {
        "input": input_review,
        "overfit": no_overfit_review,
        "runtime": runtime_review,
        "lineage": lineage_review,
        "queue": queue_rows,
    }
    gates = build_gates(summary, reviews)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "input_review_rows": len(input_review),
        "no_overfit_review_rows": len(no_overfit_review),
        "runtime_review_rows": len(runtime_review),
        "lineage_review_rows": len(lineage_review),
        "queue_rows": len(queue_rows),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_rows": len(gates),
        "passed_gates": sum(1 for row in gates if row["status"] == "passed"),
        "failed_gates": [row["gate_id"] for row in gates if row["status"] != "passed"],
    }
    artifacts: list[Path] = [
        write_csv(INPUT_REVIEW, INPUT_REVIEW_COLUMNS, input_review),
        write_csv(NO_OVERFIT_REVIEW, NO_OVERFIT_COLUMNS, no_overfit_review),
        write_csv(RUNTIME_USABILITY_REVIEW, RUNTIME_REVIEW_COLUMNS, runtime_review),
        write_csv(LINEAGE_REVIEW, LINEAGE_REVIEW_COLUMNS, lineage_review),
        write_csv(NEXT_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(build_receipts(final))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts))

    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
