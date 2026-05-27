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
    now_utc,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CL"
RUN_ID = "run337CL_review_guarded_directional_label_action_candidate_training_without_db_v1"
PARENT_RUN_ID = "run337CK_guarded_directional_label_action_candidate_training_without_db_v1"
NEXT_RUN_ID = "run337CM_design_serial_dependence_label_boundary_repair_without_db_v1"
STATUS = "completed_stage337CL_guarded_training_review_shifted_control_risk_blocks_runtime_probe_no_selection"
JUDGMENT = "negative_control_risk_requires_serial_dependence_label_boundary_repair_before_mt5_probe"
DECISION = "stage337CL_open_run337CM_serial_dependence_label_boundary_repair_design"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CL_guarded_training_review_without_db_"
    "negative_control_risk_blocks_runtime_probe_no_new_training_no_threshold_tuning_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CL_guarded_training_negative_control_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CL_guarded_training_negative_control_review.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CK_DIR = STAGE_DIR / "02_runs" / "run337CK"
CK_FINAL = CK_DIR / "final_decision.json"
CK_GATES = CK_DIR / "required_gate_coverage_audit.csv"
CK_SCORECARD = CK_DIR / "guarded_model_scorecard.csv"
CK_NEGATIVE = CK_DIR / "negative_control_scorecard.csv"
CK_PARITY = CK_DIR / "onnxruntime_parity_matrix.csv"
CK_MODEL_MANIFEST = CK_DIR / "trained_model_manifest.csv"
CK_RUNTIME_QUEUE = CK_DIR / "runtime_probe_package_queue.csv"
CK_THRESHOLD_POLICY = CK_DIR / "decision_threshold_policy.csv"

SCORE_REVIEW = RUN_DIR / "scorecard_review_matrix.csv"
NEGATIVE_ATTRIBUTION = RUN_DIR / "negative_control_attribution_matrix.csv"
RUNTIME_DISPOSITION = RUN_DIR / "runtime_probe_disposition.csv"
REPAIR_QUEUE = RUN_DIR / "run337CM_repair_design_queue.csv"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CK_FINAL,
    CK_GATES,
    CK_SCORECARD,
    CK_NEGATIVE,
    CK_PARITY,
    CK_MODEL_MANIFEST,
    CK_RUNTIME_QUEUE,
    CK_THRESHOLD_POLICY,
)
OUTPUT_FILES = (
    SCORE_REVIEW,
    NEGATIVE_ATTRIBUTION,
    RUNTIME_DISPOSITION,
    REPAIR_QUEUE,
    REQUIRED_GATE_AUDIT,
    MODEL_RECEIPT,
    DATA_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
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

SCORE_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "model_family",
    "oos_balanced_accuracy",
    "validation_balanced_accuracy",
    "oos_macro_f1",
    "oos_signal_density",
    "oos_decision_short",
    "oos_decision_long",
    "oos_decision_no_trade",
    "risk_read",
    "claim_boundary",
)
NEGATIVE_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "control_id",
    "validation_control_balanced_accuracy",
    "oos_control_balanced_accuracy",
    "validation_actual_balanced_accuracy",
    "oos_actual_balanced_accuracy",
    "oos_control_minus_actual",
    "severity",
    "interpretation",
    "claim_boundary",
)
RUNTIME_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "onnx_path",
    "mt5_probe_disposition",
    "blocking_reason",
    "next_condition",
    "claim_boundary",
)
REPAIR_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "repair_topic",
    "hypothesis",
    "required_output",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def fnum(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    return float(value)


def by_key(rows: Sequence[Mapping[str, str]], *fields: str) -> dict[tuple[str, ...], Mapping[str, str]]:
    return {tuple(str(row.get(field, "")) for field in fields): row for row in rows}


def build_score_review(score_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    keyed = by_key(score_rows, "model_id", "split")
    models = sorted({row["model_id"] for row in score_rows})
    rows: list[dict[str, Any]] = []
    for model_id in models:
        oos = keyed[(model_id, "oos")]
        validation = keyed[(model_id, "validation")]
        oos_bal = fnum(oos["balanced_accuracy"])
        risk_read = "weak_predictive_edge_review_only"
        if oos_bal >= 0.45:
            risk_read = "modest_proxy_edge_but_requires_negative_control_clearance"
        rows.append(
            {
                "model_id": model_id,
                "label_candidate_id": oos["label_candidate_id"],
                "model_family": oos["model_family"],
                "oos_balanced_accuracy": oos_bal,
                "validation_balanced_accuracy": fnum(validation["balanced_accuracy"]),
                "oos_macro_f1": fnum(oos["macro_f1"]),
                "oos_signal_density": fnum(oos["signal_density"]),
                "oos_decision_short": int(fnum(oos["decision_short"])),
                "oos_decision_long": int(fnum(oos["decision_long"])),
                "oos_decision_no_trade": int(fnum(oos["decision_no_trade"])),
                "risk_read": risk_read,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_negative_attribution(
    negative_rows: Sequence[Mapping[str, str]], score_rows: Sequence[Mapping[str, str]]
) -> list[dict[str, Any]]:
    keyed = by_key(score_rows, "model_id", "split")
    high_rows = [row for row in negative_rows if row["control_status"] == "review_required_high_control_alignment"]
    rows: list[dict[str, Any]] = []
    for row in high_rows:
        model_id = row["model_id"]
        validation_actual = fnum(keyed[(model_id, "validation")]["balanced_accuracy"])
        oos_actual = fnum(keyed[(model_id, "oos")]["balanced_accuracy"])
        validation_control = fnum(row["validation_balanced_accuracy"])
        oos_control = fnum(row["oos_balanced_accuracy"])
        delta = oos_control - oos_actual
        control_id = row["control_id"]
        if control_id == "shifted_return_control":
            severity = "block_runtime_probe"
            interpretation = (
                "shifted_return_control(이동 수익률 대조)이 실제 OOS(표본외) 점수와 같거나 더 강하다. "
                "serial dependence(연속 의존) 또는 label boundary(라벨 경계) 취약성을 먼저 수리해야 한다."
            )
        else:
            severity = "review_before_reuse"
            interpretation = (
                "direction_flip_control(방향 반전 대조)이 validation(검증)에서 높게 보인다. "
                "방향 극성 해석을 다음 설계에서 확인해야 한다."
            )
        rows.append(
            {
                "model_id": model_id,
                "label_candidate_id": row["label_candidate_id"],
                "control_id": control_id,
                "validation_control_balanced_accuracy": validation_control,
                "oos_control_balanced_accuracy": oos_control,
                "validation_actual_balanced_accuracy": validation_actual,
                "oos_actual_balanced_accuracy": oos_actual,
                "oos_control_minus_actual": delta,
                "severity": severity,
                "interpretation": interpretation,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_runtime_disposition(
    runtime_rows: Sequence[Mapping[str, str]], negative_review: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    blocked_models = {
        row["model_id"]
        for row in negative_review
        if row["severity"] == "block_runtime_probe"
    }
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        model_id = row["model_id"]
        if model_id in blocked_models:
            disposition = "hold_before_mt5_probe"
            reason = "shifted_return_control(이동 수익률 대조) high alignment(높은 정렬)"
            next_condition = "serial-dependence label-boundary repair(연속 의존 라벨 경계 수리) must clear"
        else:
            disposition = "review_only_not_selected"
            reason = "no immediate blocker, but no candidate selection allowed in CL"
            next_condition = "may be reconsidered after CM repair design"
        rows.append(
            {
                "model_id": model_id,
                "label_candidate_id": row["label_candidate_id"],
                "onnx_path": row["onnx_path"],
                "mt5_probe_disposition": disposition,
                "blocking_reason": reason,
                "next_condition": next_condition,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_repair_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "cm_p0_serial_dependence_label_boundary_audit",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "repair_topic": "serial-dependence label-boundary audit(연속 의존 라벨 경계 감사)",
            "hypothesis": "shifted controls stay strong because labels and features carry slow state across the 12-bar horizon(12봉 지평선 밖으로 느린 상태가 이어진다).",
            "required_output": "label_autocorrelation_and_shift_gap_matrix.csv",
            "forbidden_action": "do not tune threshold or choose a candidate from CK OOS(임계값 조정/후보 선택 금지)",
            "effect": "separates true edge(진짜 우위) from serial carry(연속 이월).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cm_p0_purged_embargo_split_design",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "repair_topic": "purged/embargo split design(제거/격리 분할 설계)",
            "hypothesis": "train-validation-OOS adjacency(인접성)가 target carry(타깃 이월)를 남긴다.",
            "required_output": "purged_split_contract_candidate.csv",
            "forbidden_action": "do not backfit split to profit(수익에 맞춰 분할 재조정 금지)",
            "effect": "reduces leakage-like continuity(누수형 연속성)를 압박한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cm_p1_nonoverlap_horizon_stress",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "repair_topic": "non-overlap horizon stress(비중첩 지평선 압박)",
            "hypothesis": "return horizon overlap or near-overlap(수익 지평선 중첩/근접 중첩)이 signal(신호)을 부풀린다.",
            "required_output": "nonoverlap_horizon_negative_control_plan.csv",
            "forbidden_action": "do not select best horizon from OOS(표본외 최고 지평선 선택 금지)",
            "effect": "tests whether edge survives horizon decorrelation(지평선 탈상관).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "cm_p1_direction_polarity_review",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "repair_topic": "direction polarity review(방향 극성 검토)",
            "hypothesis": "one q50 linear surface shows direction-flip validation alignment(방향 반전 검증 정렬).",
            "required_output": "direction_flip_attribution_matrix.csv",
            "forbidden_action": "do not flip polarity because one control looks good(대조 하나로 극성 반전 금지)",
            "effect": "prevents another polarity overfit(극성 과적합)를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    model_receipt = {
        "model_family": "no_new_training_review_of_ck_sklearn_onnx_candidates",
        "target_and_label": "directional label/action candidates from CK",
        "split_method": "train/validation/OOS scorecard review only",
        "selection_metric": "not_applicable_no_candidate_selection",
        "secondary_metrics": "negative controls, ONNX parity, signal density, OOS balanced accuracy",
        "threshold_policy": "fixed CK threshold reviewed only; not tuned",
        "overfit_risk": "shifted_return_control high alignment blocks runtime probe",
        "calibration_risk": "scores are exploratory ranking/proxy probabilities only",
        "comparison_baseline": "CK original, flipped, cost margin, volnorm candidates",
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "CK model input split is inherited; no new broker data used",
        "sample_scope": "CK scorecards and OOS proxy rows only",
        "missing_or_duplicate_check": "all required CK artifacts present",
        "feature_label_boundary": "review finds shifted-control risk; no new labels generated",
        "split_boundary": "review only, no fit",
        "leakage_risk": "serial target carry and adjacent split continuity",
        "data_hash_or_identity": {"ck_final_sha256": sha256_file(CK_FINAL)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in OUTPUT_FILES],
        "artifact_hashes": {},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "CK scorecards, negative controls, parity matrix, runtime queue",
        "evidence_missing": "MT5 runtime probe, forward execution, repaired label-boundary rerun",
        "judgment_label": "exploratory",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "ONNX 후보는 만들어졌지만 부정 대조가 너무 강해 바로 MT5 탐침으로 넘기지 않는다.",
    }
    paths = [
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(LINEAGE_RECEIPT, lineage_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt["artifact_hashes"] = {rel(path): sha256_file(path) for path in paths if path != LINEAGE_RECEIPT and path_exists(path)}
    write_json(LINEAGE_RECEIPT, lineage_receipt)
    return paths


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]

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
        row("cl_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CK 산출물을 모두 읽는다."),
        row("cl_gate_ck_gates_clean", final["ck_failed_gates"] == 0, final["ck_failed_gates"], "0 failed CK gates", "부모 실행의 산출물 게이트를 확인한다."),
        row("cl_gate_parity_clean", final["onnx_parity_passed"] == final["onnx_parity_rows"], f"{final['onnx_parity_passed']}/{final['onnx_parity_rows']}", "all parity passed", "ONNX(온엑스) 동등성은 문제 원인이 아님을 분리한다."),
        row("cl_gate_negative_controls_reviewed", final["negative_review_required_rows"] > 0, final["negative_review_required_rows"], ">0 reviewed risk rows", "부정 대조 위험을 검토 대상으로 올린다."),
        row("cl_gate_runtime_probe_blocked_by_risk", final["runtime_hold_rows"] == final["runtime_queue_rows"], f"{final['runtime_hold_rows']}/{final['runtime_queue_rows']}", "all runtime queue rows held", "강한 부정 대조가 있으면 MT5 탐침을 바로 열지 않는다."),
        row("cl_gate_repair_queue_created", final["repair_queue_rows"] >= 4, final["repair_queue_rows"], ">=4 repair rows", "다음 CM 수리 설계를 연다."),
        row("cl_gate_no_selection_or_forward_claim", True, "selection=not_run;forward=not_claimed", "no selection/forward claim", "리뷰 결과를 승자나 전진 판정으로 바꾸지 않는다."),
    ]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CL Guarded Training Review(방어 학습 검토)

## Conclusion(결론)

run337CL(337CL 실행)은 CK candidate ONNX(후보 온엑스)를 선택하지 않는다. CK는 ONNX parity(온엑스 동등성) `10/10`을 통과했지만, shifted_return_control(이동 수익률 대조) `10`행과 direction_flip_control(방향 반전 대조) `1`행이 `review_required(검토 필요)`로 남았다.

Effect(효과): MT5 runtime probe(MT5 런타임 탐침)는 지금 열지 않고, run337CM(337CM 실행)에서 serial-dependence label-boundary repair design(연속 의존 라벨 경계 수리 설계)을 먼저 연다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- reviewed_models(검토 모델): `{final["reviewed_models"]}`
- onnx_parity(ONNX 동등성): `{final["onnx_parity_passed"]}/{final["onnx_parity_rows"]}`
- negative_review_required_rows(부정 대조 검토 필요 행): `{final["negative_review_required_rows"]}`
- runtime_hold_rows(런타임 보류 행): `{final["runtime_hold_rows"]}/{final["runtime_queue_rows"]}`
- repair_queue_rows(수리 대기열 행): `{final["repair_queue_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- new_training(새 학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `held`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CL

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): shifted_return_control(이동 수익률 대조)이 모든 runtime queue(런타임 대기열) 모델을 보류시켰으므로 MT5 probe(탐침)를 열지 않고 CM repair design(수리 설계)을 연다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(NEGATIVE_ATTRIBUTION)}`, `{rel(RUNTIME_DISPOSITION)}`
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
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337CL focus complete: guarded training review(방어 학습 검토)를 `{STATUS}`로 닫았다. "
        "Effect(효과): shifted_return_control(이동 수익률 대조)이 모든 runtime queue(런타임 대기열)를 막아 run337CM(337CM 실행) serial-dependence label-boundary repair design(연속 의존 라벨 경계 수리 설계)을 연다."
    )
    if "Stage337 run337CL focus complete" in workspace_text:
        workspace_text = re.sub(
            r"current_focus:\n- >-\n  Stage337 run337CL focus complete:.*?(?=\n- >-\n  Stage337 run337CK|\n[A-Za-z0-9_]+:)",
            focus_entry,
            workspace_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
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
## Stage337 run337CL(337CL 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): CK ONNX parity(온엑스 동등성)는 통과했지만 shifted_return_control(이동 수익률 대조)이 강해 MT5 runtime probe(MT5 런타임 탐침)를 보류하고 CM repair design(수리 설계)을 연다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current_text = re.sub(
        r"\n## Stage337 run337CL\(337CL 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CK|\Z)",
        "\n",
        current_text,
        count=1,
        flags=re.DOTALL,
    )
    marker = "## Stage337 run337CK(337CK"
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
- actual_mt5_execution(실제 MT5 실행): `held_by_cl_negative_control_review`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 serial-dependence label-boundary repair design(연속 의존 라벨 경계 수리 설계)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CL(337CL 실행)" not in line)
    stage_entry = f"- {TODAY}: run337CL(337CL 실행) reviewed guarded training(방어 학습 검토). Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337CL reviewed guarded training" not in line)
    changelog_entry = f"- {TODAY}: Stage337 run337CL reviewed guarded training(방어 학습 검토) and opened `{NEXT_RUN_ID}`."
    changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "guarded_training_negative_control_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"neg_review={final['negative_review_required_rows']};runtime_hold={final['runtime_hold_rows']}/{final['runtime_queue_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "kpi_evidence_model_validation_result_judgment_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__negative_control_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "negative_control_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "scorecard_negative_control_review",
        "tier_scope": "out_of_scope_by_claim_training_proxy_no_mt5",
        "kpi_scope": "proxy_scorecard_no_mt5",
        "scoreboard_lane": "model_validation_result_judgment",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"negative_review_required_rows={final['negative_review_required_rows']};runtime_hold_rows={final['runtime_hold_rows']}",
        "guardrail_kpi": "no_selection;no_mt5_probe;repair_queue_created",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__negative_control_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "kpi_evidence_model_validation_result_judgment_artifact_lineage",
        "evidence_scope": "CK scorecards and negative controls reviewed",
        "kpi_scope": "proxy_scorecard_no_mt5",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__negative_control_review",
        "family": "kpi_evidence_model_validation_result_judgment_artifact_lineage",
        "question": "do CK candidates clear negative-control review before MT5 probe",
        "metric_scope": "negative_control_review_no_forward_decision",
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
    ck_final = read_json(CK_FINAL)
    ck_gates = read_csv(CK_GATES)
    score_rows = read_csv(CK_SCORECARD)
    negative_rows = read_csv(CK_NEGATIVE)
    parity_rows = read_csv(CK_PARITY)
    model_rows = read_csv(CK_MODEL_MANIFEST)
    runtime_rows = read_csv(CK_RUNTIME_QUEUE)

    score_review = build_score_review(score_rows)
    negative_review = build_negative_attribution(negative_rows, score_rows)
    runtime_disposition = build_runtime_disposition(runtime_rows, negative_review)
    repair_queue = build_repair_queue()
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "reviewed_models": len(model_rows),
        "score_review_rows": len(score_review),
        "negative_review_required_rows": len(negative_review),
        "negative_review_block_runtime_rows": sum(1 for row in negative_review if row["severity"] == "block_runtime_probe"),
        "runtime_queue_rows": len(runtime_disposition),
        "runtime_hold_rows": sum(1 for row in runtime_disposition if row["mt5_probe_disposition"] == "hold_before_mt5_probe"),
        "repair_queue_rows": len(repair_queue),
        "onnx_parity_rows": len(parity_rows),
        "onnx_parity_passed": sum(1 for row in parity_rows if row["passed"] == "true"),
        "ck_failed_gates": len([row for row in ck_gates if row["status"] != "passed"]) + len(ck_final.get("failed_gates", [])),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "held_by_negative_control_review",
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
        write_csv(SCORE_REVIEW, SCORE_COLUMNS, score_review),
        write_csv(NEGATIVE_ATTRIBUTION, NEGATIVE_COLUMNS, negative_review),
        write_csv(RUNTIME_DISPOSITION, RUNTIME_COLUMNS, runtime_disposition),
        write_csv(REPAIR_QUEUE, REPAIR_COLUMNS, repair_queue),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(build_receipts(final))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
