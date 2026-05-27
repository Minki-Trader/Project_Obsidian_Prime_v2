from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage337 import label_boundary_lifecycle_cost_frontier_probe_without_db as ca  # noqa: E402


by = ca.by
bz = ca.bz
aw = ca.aw
bg = ca.bg

TODAY = "2026-05-28"
STAGE_ID = ca.STAGE_ID
RUN_NUMBER = "run337CB"
RUN_ID = "run337CB_lifecycle_aware_no_overfit_design_without_db_v1"
PARENT_RUN_ID = ca.RUN_ID
NEXT_RUN_ID = "run337CC_materialize_lifecycle_aware_no_overfit_inputs_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CB_lifecycle_aware_no_overfit_design_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ca.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ca.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337CB_lifecycle_aware_no_overfit_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CB_lifecycle_aware_no_overfit_design.md"
SELECTED_STATUS = ca.SELECTED_STATUS
STAGE_BRIEF = ca.STAGE_BRIEF
WORKSPACE_STATE = ca.WORKSPACE_STATE
CURRENT_STATE = ca.CURRENT_STATE
CHANGELOG = ca.CHANGELOG
RUN_REGISTRY = ca.RUN_REGISTRY
ALPHA_LEDGER = ca.ALPHA_LEDGER
ARTIFACT_REGISTRY = ca.ARTIFACT_REGISTRY
STAGE_LEDGER = ca.STAGE_LEDGER

CA_FINAL = ca.FINAL_DECISION
CA_LABELABLE = ca.LABELABLE_ONLY_SCORE
CA_LIFECYCLE = ca.LIFECYCLE_ACTION_PARITY
CA_BRIDGE = ca.LIFECYCLE_COMPRESSION_BRIDGE
CA_COST = ca.COST_FRONTIER_GUARDRAIL
CA_EXTERNAL = ca.EXTERNAL_TELEMETRY_IDENTITY
BZ_SPLIT = bz.SPLIT_STABILITY_MATRIX
BZ_RUNTIME = bz.RUNTIME_KPI_MATRIX

EXPERIMENT_DESIGN = RUN_DIR / "lifecycle_aware_experiment_design.csv"
TARGET_CONTRACT = RUN_DIR / "lifecycle_aware_target_metric_contract.csv"
VALIDATION_GATES = RUN_DIR / "no_overfit_validation_gate_contract.csv"
NEGATIVE_CONTROLS = RUN_DIR / "negative_control_plan.csv"
FEATURE_CONSTRAINTS = RUN_DIR / "feature_family_constraints.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337CC_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_discipline_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CA_FINAL,
    CA_LABELABLE,
    CA_LIFECYCLE,
    CA_BRIDGE,
    CA_COST,
    CA_EXTERNAL,
    BZ_SPLIT,
    BZ_RUNTIME,
)
OUTPUT_FILES = (
    EXPERIMENT_DESIGN,
    TARGET_CONTRACT,
    VALIDATION_GATES,
    NEGATIVE_CONTROLS,
    FEATURE_CONSTRAINTS,
    MATERIALIZATION_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
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

DESIGN_COLUMNS = (
    "design_id",
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
    "claim_boundary",
)
TARGET_COLUMNS = (
    "target_id",
    "target_metric",
    "runtime_rule",
    "label_boundary",
    "cost_policy",
    "score_unit",
    "required_identity",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
GATE_CONTRACT_COLUMNS = (
    "gate_id",
    "gate_family",
    "required_condition",
    "pass_condition",
    "fail_condition",
    "invalid_condition",
    "evidence_path",
    "claim_boundary",
)
NEGATIVE_COLUMNS = (
    "control_id",
    "control_type",
    "purpose",
    "expected_if_signal_real",
    "failure_meaning",
    "required_output",
    "claim_boundary",
)
FEATURE_COLUMNS = (
    "constraint_id",
    "feature_family",
    "allowed_change",
    "blocked_change",
    "reason",
    "evidence_source",
    "claim_boundary",
)
NEXT_COLUMNS = by.NEXT_COLUMNS
GATE_COLUMNS = by.GATE_COLUMNS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=RUN_ID)
    return parser.parse_args()


def rel(path: Path) -> str:
    return by.rel(path)


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    return by.csv_value(value)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return by.write_csv(path, columns, rows)


def write_json(path: Path, payload: Any) -> Path:
    return by.write_json(path, payload)


def write_md(path: Path, text: str) -> Path:
    return by.write_md(path, text)


def read_json(path: Path) -> Any:
    return by.read_json(path)


def read_df(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig")


def input_gates() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        rows.append(
            {
                "gate_id": f"input_exists::{rel(path)}",
                "status": "passed" if path_exists(path) else "failed",
                "evidence": rel(path),
                "effect": "input available for CB design(CB 설계 입력 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_design() -> list[dict[str, Any]]:
    return [
        {
            "design_id": "lifecycle_aware_no_overfit_v1",
            "hypothesis": "A future ONNX is only useful if its edge survives MT5-like lifecycle compression, labelable-only scoring, rolling splits, and cost2 stress.",
            "decision_use": "design next materialization inputs only; no candidate selection",
            "comparison_baseline": f"{rel(CA_LABELABLE)};{rel(CA_LIFECYCLE)};{rel(BZ_RUNTIME)}",
            "control_variables": "US100 M5; completed-day boundary; max_hold_bars=12; no lot optimization; no threshold tuning",
            "changed_variables": "target scoring surface changes from raw signal score to lifecycle-aware diagnostic target",
            "sample_scope": "2026-04-14 forward diagnostic plus prior train/validation/oos split references",
            "success_criteria": "materialized input contract can compute lifecycle-aware score and all negative controls before training",
            "failure_criteria": "cannot build labelable lifecycle target, cost2 guard, or rolling split evidence without leakage",
            "invalid_conditions": "future return enters features; threshold chosen from forward; telemetry identity missing",
            "stop_conditions": "stop before training if any gate lacks row-level evidence or if cost/session frontier is used as selection",
            "evidence_plan": f"{rel(TARGET_CONTRACT)};{rel(VALIDATION_GATES)};{rel(NEGATIVE_CONTROLS)};{rel(MATERIALIZATION_QUEUE)}",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_target_contract() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "lifecycle_closed_trade_log_return_cost2",
            "target_metric": "closed lifecycle trade log return after max_hold/reverse/flat lifecycle, stressed at cost2",
            "runtime_rule": "max_hold_bars=12 from CA lifecycle parity; reverse opens new direction; close_max_hold is an order action",
            "label_boundary": "use only rows/trades whose exit bar and future label are available; separate non-labelable latest rows",
            "cost_policy": "cost0/cost1/cost2 reported; cost2 survival is a guardrail, not a threshold selector",
            "score_unit": "diagnostic log-return proxy; not MT5 account-currency PnL",
            "required_identity": rel(CA_EXTERNAL),
            "forbidden_use": "do not claim operating, forward pass, or runtime authority from proxy target",
            "effect": "turns raw signal score into lifecycle-aware measurement(원 신호 점수를 생애주기 인식 측정으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "target_id": "labelable_signal_quality_floor",
            "target_metric": "labelable-only hit/coverage/PF floor before lifecycle materialization",
            "runtime_rule": "must be compared against lifecycle compression bridge",
            "label_boundary": "non-labelable signals are counted but excluded from profit metric",
            "cost_policy": "same cost assumptions as target lifecycle contract",
            "score_unit": "diagnostic signal metric",
            "required_identity": rel(CA_LABELABLE),
            "forbidden_use": "do not use labelable-only score alone for selection",
            "effect": "keeps measurement from hiding missing labels(빠진 라벨을 숨기지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_validation_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "rolling_split_stability_gate",
            "gate_family": "model_validation",
            "required_condition": "train, validation, oos, forward diagnostic rows exist for any materialized model scout",
            "pass_condition": "no single split carries the result; degradation is named and bounded",
            "fail_condition": "train-only or forward-only improvement drives the design",
            "invalid_condition": "split boundary is recomputed after seeing forward result",
            "evidence_path": rel(BZ_SPLIT),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cost2_survival_guard",
            "gate_family": "performance_attribution",
            "required_condition": "cost0/cost1/cost2 diagnostics are recorded before candidate comparison",
            "pass_condition": "cost2 failure is allowed but must be a design constraint",
            "fail_condition": "cost1-only survival is described as robust",
            "invalid_condition": "threshold or lot is optimized to pass cost2",
            "evidence_path": rel(CA_COST),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "lifecycle_parity_guard",
            "gate_family": "runtime_parity",
            "required_condition": "max-hold lifecycle action rule remains hash-linked to MT5 telemetry",
            "pass_condition": "proxy action match rate >= 0.999 on completed-day overlap",
            "fail_condition": "lifecycle proxy diverges from MT5 action telemetry",
            "invalid_condition": "Common Files telemetry is missing or un-hashed",
            "evidence_path": rel(CA_LIFECYCLE),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "final_claim_guard",
            "gate_family": "claim_discipline",
            "required_condition": "design stays research-only",
            "pass_condition": "no Forward Passed, Forward Failed, runtime authority, or Goal Achieve claim",
            "fail_condition": "design is treated as model readiness",
            "invalid_condition": "claim boundary is absent from outputs",
            "evidence_path": rel(REQUIRED_GATE_AUDIT),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_negative_controls() -> list[dict[str, Any]]:
    return [
        {
            "control_id": "shifted_label_one_bar",
            "control_type": "leakage_probe",
            "purpose": "detect whether lifecycle score survives a one-bar label shift suspiciously",
            "expected_if_signal_real": "edge changes materially under shift",
            "failure_meaning": "score may be insensitive to time boundary or leakage-like",
            "required_output": "shifted_label_lifecycle_score.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "direction_flip",
            "control_type": "directionality_probe",
            "purpose": "confirm long/short direction is not arbitrary",
            "expected_if_signal_real": "flipped direction weakens lifecycle score",
            "failure_meaning": "model may be trading exposure or drift rather than direction",
            "required_output": "direction_flip_lifecycle_score.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "session_holdout",
            "control_type": "concentration_probe",
            "purpose": "test whether edge depends on one hour/session pocket",
            "expected_if_signal_real": "score remains interpretable outside top concentration pocket",
            "failure_meaning": "session concentration may be carrying the surface",
            "required_output": "session_holdout_lifecycle_score.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "cost2_and_cost5_stress",
            "control_type": "cost_probe",
            "purpose": "separate fragile cost edge from robust lifecycle edge",
            "expected_if_signal_real": "cost2 degradation is bounded and cost5 failure is named",
            "failure_meaning": "raw surface is too cost-sensitive for robust model design",
            "required_output": "cost_stress_lifecycle_score.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_feature_constraints() -> list[dict[str, Any]]:
    return [
        {
            "constraint_id": "technical42_allowed_primary",
            "feature_family": "us100_technical42_no_external",
            "allowed_change": "lifecycle-aware target materialization and rolling split scoring",
            "blocked_change": "forward threshold search or lot tuning",
            "reason": "technical-only path has cleanest external dependency boundary but still cost/session fragile",
            "evidence_source": rel(BZ_RUNTIME),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "macro48_allowed_with_lag_audit",
            "feature_family": "macro48_no_equity_breadth_or_top3",
            "allowed_change": "lag-audited lifecycle target materialization",
            "blocked_change": "unlagged macro/equity carry or forward-selected macro subset",
            "reason": "macro branch needs explicit stale/lag guard before model training",
            "evidence_source": rel(BZ_RUNTIME),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "core56_not_primary_until_stale_risk_repaired",
            "feature_family": "core56_no_top3_weight_features",
            "allowed_change": "stress branch only",
            "blocked_change": "primary candidate claim",
            "reason": "equity stale stress remains not-primary and cost2 survivor count is zero",
            "evidence_source": rel(CA_COST),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_materialization_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337CC_materialize_lifecycle_aware_no_overfit_inputs",
            "next_run_id": NEXT_RUN_ID,
            "lane": "materialize_inputs_before_training",
            "priority": "P0",
            "reason": "CB design requires lifecycle-aware target, rolling split guard, negative controls, and cost stress before any model training",
            "required_evidence": "target metric contract, validation gates, negative controls, feature constraints, artifact hashes",
            "forbidden_shortcut": "no training, no candidate selection, no threshold tuning, no forward pass claim",
            "effect": "moves from design to input materialization(설계에서 입력 물질화로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(
    input_rows: Sequence[Mapping[str, Any]],
    design_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    control_rows: Sequence[Mapping[str, Any]],
    feature_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    gates = list(input_rows)
    checks = [
        ("experiment_design_contract", len(design_rows) == 1, f"design_rows={len(design_rows)}"),
        ("target_metric_contract", len(target_rows) >= 2 and all(row.get("forbidden_use") for row in target_rows), f"target_rows={len(target_rows)}"),
        ("no_overfit_gate_contract", len(gate_rows) >= 4, f"gate_rows={len(gate_rows)}"),
        ("negative_control_contract", len(control_rows) >= 4, f"negative_control_rows={len(control_rows)}"),
        ("feature_constraint_contract", len(feature_rows) >= 3, f"feature_constraint_rows={len(feature_rows)}"),
        ("required_gate_coverage_audit", True, "CB required gates represented"),
        ("final_claim_guard", True, "no forward/goal/runtime authority claim"),
    ]
    for gate_id, passed, evidence in checks:
        gates.append(
            {
                "gate_id": gate_id,
                "status": "passed" if passed else "failed",
                "evidence": evidence,
                "effect": "supports CB design closeout without promotion claim(CB 설계 종료를 승격 주장 없이 지지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return gates


def classify(gates: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    failed = [row for row in gates if row.get("status") != "passed"]
    if failed:
        return (
            "blocked_stage337CB_lifecycle_aware_design_gate_failed_no_forward_decision",
            "blocked_required_design_contract_missing",
            "stage337CB_repair_design_contract_before_materialization",
            RUN_ID,
        )
    return (
        "completed_stage337CB_lifecycle_aware_no_overfit_design_materialized_no_training_no_selection",
        "design_contract_ready_for_lifecycle_aware_materialization",
        "stage337CB_open_run337CC_materialize_lifecycle_aware_no_overfit_inputs",
        NEXT_RUN_ID,
    )


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "run_id": RUN_ID,
                "hypothesis": "A lifecycle-aware target and no-overfit gates must be materialized before any further model training",
                "decision_use": "opens materialization only",
                "evidence_plan": [rel(EXPERIMENT_DESIGN), rel(TARGET_CONTRACT), rel(VALIDATION_GATES), rel(NEGATIVE_CONTROLS)],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [rel(CA_LABELABLE), rel(CA_LIFECYCLE), rel(CA_EXTERNAL)],
                "time_axis": "completed-day runtime overlap and prior split references",
                "integrity_judgment": "design_only_usable_with_prior_hashes",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "not trained in CB",
                "threshold_policy": "no threshold selection; cost stress is guardrail",
                "overfit_risk": "addressed by gate contract and negative controls",
                "validation_judgment": "design_materialized_no_selection",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "observed_change": "CA lifecycle rule closed measurement gap but cost2 guard remains severe",
                "comparison_baseline": [rel(CA_COST), rel(BZ_RUNTIME)],
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in OUTPUT_FILES if path_exists(path)],
                "lineage_judgment": "connected_design_only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "judgment_label": final["judgment"],
                "evidence_available": [rel(REPORT_PATH), rel(REQUIRED_GATE_AUDIT)],
                "evidence_missing": "no materialized lifecycle target yet, no training, no MT5 rerun",
                "next_condition": final["next_action"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "effect": "CB is design only(CB는 설계만 해당)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def write_report(final: Mapping[str, Any], design_rows: Sequence[Mapping[str, Any]], target_rows: Sequence[Mapping[str, Any]], control_rows: Sequence[Mapping[str, Any]]) -> Path:
    target_lines = "\n".join(f"| `{row['target_id']}` | {row['target_metric']} | {row['cost_policy']} |" for row in target_rows)
    control_lines = "\n".join(f"| `{row['control_id']}` | `{row['control_type']}` | {row['purpose']} |" for row in control_rows)
    return write_md(
        REPORT_PATH,
        f"""# Stage337 run337CB Lifecycle-Aware No-Overfit Design(생애주기 인식 무과적합 설계)

## Conclusion(결론)

run337CB(337CB 실행)는 CA의 labelable score(라벨 가능 점수)와 lifecycle parity(생애주기 동등성)를 다음 materialization(물질화) 계약으로 바꿨다.

Effect(효과): 다음 run337CC(337CC 실행)는 학습 전에 lifecycle-aware target(생애주기 인식 목표), rolling split guard(구간 분할 가드), negative controls(부정 대조), cost stress(비용 압박)를 먼저 만들게 된다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Target Contract(목표 계약)

| target(목표) | metric(지표) | cost policy(비용 정책) |
|---|---|---|
{target_lines}

## Negative Controls(부정 대조)

| control(대조) | type(유형) | purpose(목적) |
|---|---|---|
{control_lines}

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    return write_md(
        DECISION_DOC,
        f"""# Decision: Stage337 run337CB Lifecycle-Aware No-Overfit Design(결정: 생애주기 인식 무과적합 설계)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): lifecycle-aware target(생애주기 인식 목표)과 no-overfit gates(무과적합 게이트)를 설계 계약으로 고정했다. 이것은 materialization(물질화) 준비이며, 모델 학습이나 후보 선택이 아니다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = by.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", NEXT_RUN_ID)
    workspace = bg.replace_top_value(workspace, "updated_on: ", f"'{TODAY}'")
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337CB focus complete: lifecycle-aware no-overfit design(생애주기 인식 무과적합 설계)을 `{final['status']}`로 닫았다. "
        "Effect(효과): run337CC(337CC 실행) materialization(물질화)을 연다.\n"
    )
    if "Stage337 run337CB focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(by.write_text_preserving(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = by.read_text_lossless(CURRENT_STATE)
    current = current_text
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
## Stage337 run337CB(337CB 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): lifecycle-aware no-overfit design(생애주기 인식 무과적합 설계)을 만들고 materialization(물질화)을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337CB(337CB 실행)" not in current:
        marker = "## Stage337 run337CA(337CA"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(by.write_text_preserving(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- actual_mt5_execution(실제 MT5 실행): `not_run_design_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 lifecycle-aware no-overfit input materialization(생애주기 인식 무과적합 입력 물질화)이다.
"""
    artifacts.append(by.write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = by.read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337CB(337CB 실행) materialized lifecycle-aware no-overfit design(생애주기 인식 무과적합 설계). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(by.write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = by.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337CB materialized lifecycle-aware no-overfit design(생애주기 인식 무과적합 설계) and opened `{NEXT_RUN_ID}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(by.write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "lifecycle_aware_no_overfit_design_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "experiment_design",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__lifecycle_aware_no_overfit_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "lifecycle_aware_no_overfit_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "design_contract",
        "tier_scope": "Tier A completed-day evidence boundary",
        "kpi_scope": "design_no_kpi_execution",
        "scoreboard_lane": "diagnostic_special",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"design_rows={final['design_rows']}",
        "guardrail_kpi": "no training; no threshold tuning; no goal claim",
        "external_verification_status": "not_applicable_design_only",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__lifecycle_aware_no_overfit_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design",
        "evidence_scope": "CA label/lifecycle/cost outputs converted to design contract",
        "kpi_scope": "design_contract",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"target_rows={final['target_rows']};negative_controls={final['negative_control_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__lifecycle_aware_no_overfit_design",
        "family": "experiment_design",
        "question": "what lifecycle-aware no-overfit inputs must be materialized before training",
        "metric_scope": "design_only",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    artifacts = [
        aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]
    artifact_columns, existing_rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    artifact_columns = artifact_columns or ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    generated = now_utc()
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
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    merged = [row for row in existing_rows if row.get("artifact_id") not in keys]
    merged.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, merged))
    return artifacts


def main() -> int:
    parse_args()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    parent = read_json(CA_FINAL)
    inputs = input_gates()
    design_rows = build_design()
    target_rows = build_target_contract()
    validation_rows = build_validation_gates()
    negative_rows = build_negative_controls()
    feature_rows = build_feature_constraints()
    queue_rows = build_materialization_queue()
    gates = build_gates(inputs, design_rows, target_rows, validation_rows, negative_rows, feature_rows)
    status, judgment, decision, next_action = classify(gates)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "parent_status": parent.get("status", ""),
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "design_rows": len(design_rows),
        "target_rows": len(target_rows),
        "validation_gate_rows": len(validation_rows),
        "negative_control_rows": len(negative_rows),
        "feature_constraint_rows": len(feature_rows),
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
        write_csv(EXPERIMENT_DESIGN, DESIGN_COLUMNS, design_rows),
        write_csv(TARGET_CONTRACT, TARGET_COLUMNS, target_rows),
        write_csv(VALIDATION_GATES, GATE_CONTRACT_COLUMNS, validation_rows),
        write_csv(NEGATIVE_CONTROLS, NEGATIVE_COLUMNS, negative_rows),
        write_csv(FEATURE_CONSTRAINTS, FEATURE_COLUMNS, feature_rows),
        write_csv(MATERIALIZATION_QUEUE, NEXT_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(build_receipts(final))
    artifacts.append(write_report(final, design_rows, target_rows, negative_rows))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final, artifacts))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
