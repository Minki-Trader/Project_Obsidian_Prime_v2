from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import onnx
import pandas as pd
from onnx import TensorProto, helper, numpy_helper


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage350 import (  # noqa: E402
    probe_softmax_output_shape_and_conversion_semantics_without_db as base,
)


TODAY = "2026-06-01"
STAGE_ID = "350_onnx_runtime_interop__softmax_output_shape_repair_probe"
RUN_NUMBER = "run350C"
RUN_ID = "run350C_open_runtime_output_contract_or_new_model_family_pivot_without_db_v1"
PARENT_RUN_ID = base.RUN_ID
SOURCE_RUNTIME_RUN_ID = "run350B_probe_softmax_output_shape_and_conversion_semantics_without_db_v1"
NEXT_RUN_ID = "run350D_build_gemm_safe_or_table_runtime_model_family_pivot_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_onnx_operator_ladder_runtime_contract_probe_only_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage350/run350C_operator_ladder_probe"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage350_ONNXInterop__OperatorLadder"
PARITY_TOLERANCE = 1.0e-4

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run350C_onnx_operator_ladder_runtime_contract_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage350C_onnx_operator_ladder_runtime_contract_probe.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN350B_DIR = STAGE_DIR / "02_runs" / "run350B"
RUN350B_FINAL = RUN350B_DIR / "final_decision.json"
RUN350B_GATES = RUN350B_DIR / "required_gate_coverage_audit.csv"
RUN350B_SUMMARY = RUN350B_DIR / "softmax_output_shape_conversion_probe_summary.csv"
RUN349E_E02_ONNX = base.RUN349E_E02_ONNX

VARIANT_DESIGN = RUN_DIR / "operator_ladder_variant_design.csv"
VARIANT_PACKAGE = RUN_DIR / "operator_ladder_variant_package.csv"
THRESHOLD_SCREEN = RUN_DIR / "operator_ladder_threshold_screen.csv"
PYTHON_ONNX_PROBE = RUN_DIR / "python_onnx_operator_ladder_probe.csv"
EXPECTED_TAPE = RUN_DIR / "expected_tape.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
SUMMARY_CSV = RUN_DIR / "operator_ladder_runtime_contract_summary.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_BOUNDARY_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
NEXT_ACTION_QUEUE = RUN_DIR / "next_action_queue.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

INPUT_FILES = (
    RUN350B_FINAL,
    RUN350B_GATES,
    RUN350B_SUMMARY,
    RUN349E_E02_ONNX,
    base.SOURCE_FEATURES,
    base.SOURCE_FEATURE_ORDER,
    base.SOURCE_FEATURE_LABEL,
    base.SOURCE_PREDICTIONS,
)

OUTPUT_FILES = (
    VARIANT_DESIGN,
    VARIANT_PACKAGE,
    THRESHOLD_SCREEN,
    PYTHON_ONNX_PROBE,
    EXPECTED_TAPE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    STRATEGY_TESTER_REPORTS,
    RUNTIME_OUTPUT_COPY,
    PROXY_MT5_DIFF,
    SUMMARY_CSV,
    RUNTIME_IDENTITY,
    RUNTIME_PARITY_RECEIPT,
    BACKTEST_FORENSICS_RECEIPT,
    PERFORMANCE_ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    ARTIFACT_LINEAGE_RECEIPT,
    CLAIM_BOUNDARY_RECEIPT,
    EXPERIMENT_RECEIPT,
    NEXT_ACTION_QUEUE,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
)


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def patch_base_globals() -> None:
    replacements: dict[str, Any] = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_RUNTIME_RUN_ID": SOURCE_RUNTIME_RUN_ID,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "COMMON_ROOT": COMMON_ROOT,
        "COMMON_MODEL_DIR": COMMON_MODEL_DIR,
        "COMMON_TELEMETRY_DIR": COMMON_TELEMETRY_DIR,
        "EXPLORATION_LABEL": EXPLORATION_LABEL,
        "PARITY_TOLERANCE": PARITY_TOLERANCE,
        "RUN_DIR": RUN_DIR,
        "MODEL_DIR": MODEL_DIR,
        "MT5_DIR": MT5_DIR,
        "SET_DIR": SET_DIR,
        "INI_DIR": INI_DIR,
        "TELEMETRY_COPY_DIR": TELEMETRY_COPY_DIR,
        "REVIEW_DIR": REVIEW_DIR,
        "REPORT_PATH": REPORT_PATH,
        "DECISION_DOC": DECISION_DOC,
        "STAGE_BRIEF": STAGE_BRIEF,
        "SELECTION_STATUS": SELECTION_STATUS,
        "STAGE_LEDGER": STAGE_LEDGER,
        "VARIANT_DESIGN": VARIANT_DESIGN,
        "VARIANT_PACKAGE": VARIANT_PACKAGE,
        "THRESHOLD_SCREEN": THRESHOLD_SCREEN,
        "PYTHON_ONNX_PROBE": PYTHON_ONNX_PROBE,
        "EXPECTED_TAPE": EXPECTED_TAPE,
        "TERMINAL_PROCESS_AUDIT": TERMINAL_PROCESS_AUDIT,
        "MT5_EXECUTION_RESULT": MT5_EXECUTION_RESULT,
        "STRATEGY_TESTER_REPORTS": STRATEGY_TESTER_REPORTS,
        "RUNTIME_OUTPUT_COPY": RUNTIME_OUTPUT_COPY,
        "PROXY_MT5_DIFF": PROXY_MT5_DIFF,
        "SUMMARY_CSV": SUMMARY_CSV,
        "RUNTIME_IDENTITY": RUNTIME_IDENTITY,
        "RUNTIME_PARITY_RECEIPT": RUNTIME_PARITY_RECEIPT,
        "BACKTEST_FORENSICS_RECEIPT": BACKTEST_FORENSICS_RECEIPT,
        "PERFORMANCE_ATTRIBUTION_RECEIPT": PERFORMANCE_ATTRIBUTION_RECEIPT,
        "JUDGMENT_RECEIPT": JUDGMENT_RECEIPT,
        "ARTIFACT_LINEAGE_RECEIPT": ARTIFACT_LINEAGE_RECEIPT,
        "CLAIM_BOUNDARY_RECEIPT": CLAIM_BOUNDARY_RECEIPT,
        "EXPERIMENT_RECEIPT": EXPERIMENT_RECEIPT,
        "NEXT_ACTION_QUEUE": NEXT_ACTION_QUEUE,
        "GATE_AUDIT": GATE_AUDIT,
        "FINAL_DECISION": FINAL_DECISION,
        "RUN_MANIFEST": RUN_MANIFEST,
        "WORKSPACE_STATE": WORKSPACE_STATE,
        "CURRENT_WORKING_STATE": CURRENT_WORKING_STATE,
        "RUN_REGISTRY": RUN_REGISTRY,
        "PROJECT_LEDGER": PROJECT_LEDGER,
        "ARTIFACT_REGISTRY": ARTIFACT_REGISTRY,
        "ROOT_SELECTION_STATUS": ROOT_SELECTION_STATUS,
        "ROOT_CHANGELOG": ROOT_CHANGELOG,
        "WORKSPACE_CHANGELOG": WORKSPACE_CHANGELOG,
    }
    for key, value in replacements.items():
        setattr(base, key, value)


def parse_args() -> argparse.Namespace:
    return base.parse_args()


def build_matmul_bias_model(path: Path, feature_count: int, *, include_scaler: bool) -> None:
    nodes = []
    initializers = []
    current = "float_input"
    if include_scaler:
        initializers.extend(
            [
                numpy_helper.from_array(np.zeros((1, feature_count), dtype=np.float32), name="scaler_mean"),
                numpy_helper.from_array(np.ones((1, feature_count), dtype=np.float32), name="scaler_scale"),
            ]
        )
        nodes.append(helper.make_node("Sub", [current, "scaler_mean"], ["centered"], name="center_features"))
        nodes.append(helper.make_node("Div", ["centered", "scaler_scale"], ["scaled"], name="scale_features"))
        current = "scaled"
    weights = np.zeros((feature_count, 3), dtype=np.float32)
    bias = np.asarray([0.20, 0.55, 0.25], dtype=np.float32)
    initializers.extend(
        [
            numpy_helper.from_array(weights, name="W"),
            numpy_helper.from_array(bias, name="B"),
        ]
    )
    nodes.append(helper.make_node("MatMul", [current, "W"], ["matmul_out"], name="matmul_zero"))
    nodes.append(helper.make_node("Add", ["matmul_out", "B"], ["probabilities"], name="bias_probability"))
    input_info, output_info = base.model_io([1, feature_count], [1, 3])
    graph = helper.make_graph(nodes, "stage350C_matmul_bias_contract", [input_info], [output_info], initializer=initializers)
    model = base.set_model_versions(helper.make_model(graph))
    base.ensure_parent(path)
    path.write_bytes(model.SerializeToString())


def build_small_linear_model(path: Path, frame: pd.DataFrame, feature_order: Sequence[str]) -> None:
    x = frame.loc[:, list(feature_order)].to_numpy(dtype=np.float32, copy=True)
    mean = np.mean(x, axis=0, keepdims=True).astype(np.float32)
    scale = np.std(x, axis=0, keepdims=True).astype(np.float32)
    scale[scale < 1.0e-6] = 1.0
    weights = np.zeros((len(feature_order), 3), dtype=np.float32)
    # Tiny weights create a probability-like but row-varying output.
    weights[0, 0] = 0.005
    weights[1, 1] = 0.005
    weights[2, 2] = 0.005
    weights[3, 0] = -0.003
    weights[4, 2] = 0.003
    bias = np.asarray([0.25, 0.50, 0.25], dtype=np.float32)
    nodes = [
        helper.make_node("Sub", ["float_input", "scaler_mean"], ["centered"], name="center_features"),
        helper.make_node("Div", ["centered", "scaler_scale"], ["scaled"], name="scale_features"),
        helper.make_node("MatMul", ["scaled", "W"], ["linear_out"], name="small_linear_matmul"),
        helper.make_node("Add", ["linear_out", "B"], ["probabilities"], name="small_linear_bias"),
    ]
    initializers = [
        numpy_helper.from_array(mean, name="scaler_mean"),
        numpy_helper.from_array(scale, name="scaler_scale"),
        numpy_helper.from_array(weights, name="W"),
        numpy_helper.from_array(bias, name="B"),
    ]
    input_info, output_info = base.model_io([1, len(feature_order)], [1, 3])
    graph = helper.make_graph(nodes, "stage350C_small_linear_contract", [input_info], [output_info], initializer=initializers)
    model = base.set_model_versions(helper.make_model(graph))
    base.ensure_parent(path)
    path.write_bytes(model.SerializeToString())


def build_e02_logits_model(path: Path, *, temperature: float, softmax: bool, feature_count: int) -> None:
    source = onnx.load(base.fs_path(base.required(RUN349E_E02_ONNX)))
    nodes, initializers, logits_name = base.split_pre_softmax(source)
    current = logits_name
    if temperature != 1.0:
        initializers.append(numpy_helper.from_array(np.asarray([temperature], dtype=np.float32), name="temperature"))
        nodes.append(helper.make_node("Div", [current, "temperature"], ["temperature_logits"], name="temperature_scale_logits"))
        current = "temperature_logits"
    if softmax:
        nodes.append(helper.make_node("Softmax", [current], ["probabilities"], name="probability_softmax", axis=1))
    else:
        nodes.append(helper.make_node("Identity", [current], ["probabilities"], name="logits_as_output"))
    input_info, output_info = base.model_io([1, feature_count], [1, 3])
    graph = helper.make_graph(nodes, "stage350C_e02_logits_contract", [input_info], [output_info], initializer=initializers)
    model = base.set_model_versions(helper.make_model(graph))
    base.ensure_parent(path)
    path.write_bytes(model.SerializeToString())


def operator_variants() -> list[dict[str, Any]]:
    return [
        {
            "attempt_name": "c00_constant_vector",
            "operator_step": "constant_only",
            "builder": "constant",
            "allow_trading": False,
            "no_conversion": True,
            "set_output_shape": True,
        },
        {
            "attempt_name": "c01_matmul_zero_bias",
            "operator_step": "matmul_add_constant_bias",
            "builder": "matmul_bias",
            "include_scaler": False,
            "allow_trading": False,
            "no_conversion": True,
            "set_output_shape": True,
        },
        {
            "attempt_name": "c02_scaler_matmul_zero_bias",
            "operator_step": "sub_div_matmul_add_constant_bias",
            "builder": "matmul_bias",
            "include_scaler": True,
            "allow_trading": False,
            "no_conversion": True,
            "set_output_shape": True,
        },
        {
            "attempt_name": "c03_small_linear_variable",
            "operator_step": "sub_div_matmul_add_variable_output",
            "builder": "small_linear",
            "allow_trading": False,
            "no_conversion": True,
            "set_output_shape": True,
        },
        {
            "attempt_name": "c04_e02_logits_temp64_no_softmax",
            "operator_step": "full_mlp_logits_without_softmax",
            "builder": "e02_logits",
            "temperature": 64.0,
            "softmax": False,
            "allow_trading": False,
            "no_conversion": True,
            "set_output_shape": True,
        },
        {
            "attempt_name": "c05_e02_softmax_temp64",
            "operator_step": "full_mlp_softmax_temp64",
            "builder": "e02_logits",
            "temperature": 64.0,
            "softmax": True,
            "allow_trading": False,
            "no_conversion": True,
            "set_output_shape": True,
        },
    ]


def materialize_operator_variants(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    x_all: np.ndarray,
) -> tuple[list[dict[str, Any]], dict[str, np.ndarray]]:
    variants = []
    probabilities: dict[str, np.ndarray] = {}
    probe_rows = []
    for definition in operator_variants():
        attempt_name = str(definition["attempt_name"])
        path = MODEL_DIR / f"{attempt_name}.onnx"
        builder = str(definition["builder"])
        if builder == "constant":
            base.build_constant_model(path, len(feature_order))
        elif builder == "matmul_bias":
            build_matmul_bias_model(path, len(feature_order), include_scaler=bool(definition.get("include_scaler", False)))
        elif builder == "small_linear":
            build_small_linear_model(path, frame, feature_order)
        elif builder == "e02_logits":
            build_e02_logits_model(
                path,
                temperature=float(definition.get("temperature", 1.0)),
                softmax=bool(definition.get("softmax", False)),
                feature_count=len(feature_order),
            )
        else:
            raise ValueError(f"unsupported builder: {builder}")
        output = base.run_onnx_probabilities(path, x_all)
        row_sums = output.sum(axis=1)
        max_values = output.max(axis=1)
        variants.append({**definition, "model_path": path, "model_sha256": base.sha256_file(path), "graph_mode": definition["operator_step"], "temperature": definition.get("temperature", 1.0), "source_model": "diagnostic_operator_ladder"})
        probabilities[attempt_name] = output
        probe_rows.append(
            {
                "attempt_name": attempt_name,
                "operator_step": definition["operator_step"],
                "model_path": base.rel(path),
                "model_sha256": base.sha256_file(path),
                "python_output_min": float(np.min(output)),
                "python_output_max": float(np.max(output)),
                "python_row_sum_min": float(np.min(row_sums)),
                "python_row_sum_max": float(np.max(row_sums)),
                "python_saturated_rows": int(np.sum(max_values >= 0.999999)),
                "status": "passed" if np.all(np.isfinite(output)) else "failed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    base.write_csv(VARIANT_DESIGN, variants)
    base.write_csv(PYTHON_ONNX_PROBE, probe_rows)
    return variants, probabilities


def first_failing_operator(summary_rows: Sequence[Mapping[str, Any]]) -> str:
    order = [
        ("c00_constant_vector", "constant_only"),
        ("c01_matmul_zero_bias", "matmul_add_constant_bias"),
        ("c02_scaler_matmul_zero_bias", "sub_div_scaler"),
        ("c03_small_linear_variable", "variable_matmul_add"),
        ("c04_e02_logits_temp64_no_softmax", "full_mlp_logits_or_relu_path"),
        ("c05_e02_softmax_temp64", "softmax_path"),
    ]
    by_name = {row.get("attempt_name"): row for row in summary_rows}
    for name, label in order:
        row = by_name.get(name)
        if not row or str(row.get("probability_parity", "")).lower() != "true":
            return label
    return "none_all_operator_ladder_passed"


def build_final(
    args: argparse.Namespace,
    attempts: Sequence[Mapping[str, Any]],
    summary_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    completed = [row for row in summary_rows if str(row.get("runtime_status", "")) == "completed"]
    parity_rows = [row for row in summary_rows if str(row.get("probability_parity", "")).lower() == "true"]
    failing = first_failing_operator(summary_rows)
    blocked = len(completed) < len(attempts)
    if blocked:
        status = "blocked_stage350C_operator_ladder_runtime_outputs_missing_no_selection"
        judgment = "blocked_operator_ladder_mt5_outputs_missing_or_terminal_unavailable"
        result_judgment = "blocked(차단)"
        decision = "stage350C_retry_operator_ladder_runtime_contract_probe"
        next_run_id = RUN_ID
    elif failing == "none_all_operator_ladder_passed":
        status = "completed_stage350C_operator_ladder_passed_softmax_model_family_pivot_required_no_selection"
        judgment = "operator_ladder_passed_prior_failure_likely_model_training_numeric_surface_pivot_required"
        result_judgment = "negative_model_surface(부정 모델 표면)"
        decision = "stage350C_open_run350D_build_gemm_safe_or_table_runtime_model_family_pivot"
        next_run_id = NEXT_RUN_ID
    else:
        status = "completed_stage350C_operator_ladder_found_runtime_contract_break_no_selection"
        judgment = f"negative_runtime_contract_first_failing_operator_{failing}_repair_required"
        result_judgment = "negative_runtime_contract(부정 런타임 계약)"
        decision = "stage350C_open_run350D_build_gemm_safe_or_table_runtime_model_family_pivot"
        next_run_id = NEXT_RUN_ID
    best = summary_rows[0] if summary_rows else {}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "status": status,
        "judgment": judgment,
        "result_judgment": result_judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "first_failing_operator": failing,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": len(attempts),
        "runtime_completed_rows": len(completed),
        "probability_parity_pass_rows": len(parity_rows),
        "diff_rows": len(diff_rows),
        "runtime_output_copy_ready_rows": sum(1 for row in copy_rows if str(row.get("exists", "")).lower() == "true"),
        "best_attempt_name": best.get("attempt_name", ""),
        "best_net_profit": best.get("net_profit", ""),
        "best_profit_factor": best.get("profit_factor", ""),
        "best_expectancy": best.get("expectancy", ""),
        "best_trade_count": best.get("trade_count", ""),
        "materialize_only": bool(args.materialize_only),
        "reuse_existing_outputs": bool(args.reuse_existing_outputs),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def make_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    def row(gate_id: str, passed: bool, evidence: str, effect: str) -> dict[str, Any]:
        return {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence": evidence,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        }

    summary_rows = pd.read_csv(base.fs_path(SUMMARY_CSV), encoding="utf-8-sig").to_dict("records") if base.exists(SUMMARY_CSV) else []
    completed_all = bool(summary_rows) and all(str(r.get("runtime_status", "")) == "completed" for r in summary_rows)
    input_hash_all = bool(summary_rows) and all(str(r.get("input_hash_parity", "")).lower() == "true" for r in summary_rows if int(float(r.get("rows_compared", 0) or 0)) > 0)
    return [
        row("parent_run350B_gate", base.gate_passed(RUN350B_GATES), base.rel(RUN350B_GATES), "Stage350B gate is closed."),
        row("operator_variants_materialized", base.exists(PYTHON_ONNX_PROBE) and base.exists(VARIANT_PACKAGE), f"{base.rel(PYTHON_ONNX_PROBE)};{base.rel(VARIANT_PACKAGE)}", "ONNX operator ladder variants were materialized."),
        row("expected_tape_written", base.exists(EXPECTED_TAPE), base.rel(EXPECTED_TAPE), "Expected tape includes MT5 input hashes."),
        row("mt5_runtime_output_observed", completed_all, base.rel(MT5_EXECUTION_RESULT), "MT5 runtime telemetry exists for all variants."),
        row("strategy_report_collected", base.exists(STRATEGY_TESTER_REPORTS), base.rel(STRATEGY_TESTER_REPORTS), "Strategy Tester reports were collected."),
        row("input_hash_parity_checked", input_hash_all, base.rel(SUMMARY_CSV), "Feature handoff identity was checked."),
        row("operator_break_attributed", base.exists(SUMMARY_CSV) and final.get("first_failing_operator", "") != "", base.rel(SUMMARY_CSV), "First failing operator was attributed."),
        row("tier_pair_rows_written", base.exists(STAGE_LEDGER) and base.exists(PROJECT_LEDGER), f"{base.rel(STAGE_LEDGER)};{base.rel(PROJECT_LEDGER)}", "Tier A/B/A+B records were written."),
        row("artifact_lineage_recorded", base.exists(ARTIFACT_LINEAGE_RECEIPT) and base.exists(RUN_MANIFEST), f"{base.rel(ARTIFACT_LINEAGE_RECEIPT)};{base.rel(RUN_MANIFEST)}", "Artifact lineage was connected."),
        row("final_claim_guard", all(final.get(key) == "not_claimed" for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]), base.rel(FINAL_DECISION), "Operating claims remain blocked."),
    ]


def write_receipts(final: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]]) -> None:
    base_payload = {"stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": now_utc(), "claim_boundary": CLAIM_BOUNDARY}
    base.write_json(EXPERIMENT_RECEIPT, {**base_payload, "hypothesis": "The Stage350B model mismatch starts at a specific ONNX operator boundary.", "decision_use": "Choose GEMM-safe ONNX rebuild, table runtime fallback, or model family pivot.", "comparison_baseline": "run350B constant canary passed while MLP variants failed.", "control_variables": "Stage348 features, MT5 tester identity, feature hash contract.", "changed_variables": "Constant, MatMul/Add, Sub/Div scaler, variable linear output, full MLP logits, full MLP softmax.", "sample_scope": "FPMarkets US100 M5 Tier A tester replay.", "success_criteria": "Find the earliest operator with MT5 probability mismatch.", "failure_criteria": "Runtime outputs missing or input hash mismatch.", "invalid_conditions": "timestamp drift, missing report, or feature handoff mismatch.", "stop_conditions": "operator boundary found or all ladder steps pass.", "evidence_plan": [base.rel(SUMMARY_CSV), base.rel(PROXY_MT5_DIFF)]})
    base.write_json(RUNTIME_PARITY_RECEIPT, {**base_payload, "research_path": base.rel(PYTHON_ONNX_PROBE), "runtime_path": base.rel(VARIANT_PACKAGE), "shared_contract": "feature order 53, output buffer [0..2], row-level MT5 input hash", "known_differences": "all variants are diagnostic; trading disabled.", "parity_check": base.rel(SUMMARY_CSV), "parity_identity": base.rel(RUNTIME_IDENTITY), "runtime_claim_boundary": "runtime_probe(런타임 탐침)"})
    base.write_json(BACKTEST_FORENSICS_RECEIPT, {**base_payload, "tester_report": base.rel(STRATEGY_TESTER_REPORTS), "tester_settings": "US100 M5, real ticks model, Deposit 500, Leverage 1:100", "forensic_gaps": [] if final["runtime_completed_rows"] == final["attempt_rows"] else ["runtime_outputs_missing"]})
    base.write_json(PERFORMANCE_ATTRIBUTION_RECEIPT, {**base_payload, "summary": base.rel(SUMMARY_CSV), "first_failing_operator": final["first_failing_operator"], "judgment": final["judgment"]})
    base.write_json(JUDGMENT_RECEIPT, {**base_payload, "result_judgment": final["result_judgment"], "status": final["status"], "decision": final["decision"], "next_run_id": final["next_run_id"], "forbidden_claims": ["candidate_selection", "forward_passed", "live_readiness", "operating_promotion", "runtime_authority", "goal_achieve"]})
    base.write_json(ARTIFACT_LINEAGE_RECEIPT, {**base_payload, "source_inputs": [base.rel(path) for path in INPUT_FILES], "producer": base.rel(Path(__file__)), "consumer": final["next_run_id"], "artifact_paths": [base.rel(path) for path in OUTPUT_FILES if base.exists(path)], "artifact_hashes": {base.rel(path): base.sha256_file(path) for path in OUTPUT_FILES if base.exists(path) and path.is_file()}, "registry_links": [base.rel(RUN_REGISTRY), base.rel(PROJECT_LEDGER), base.rel(STAGE_LEDGER), base.rel(ARTIFACT_REGISTRY)], "availability": "tracked", "lineage_judgment": "connected_with_boundary"})
    base.write_json(CLAIM_BOUNDARY_RECEIPT, {**base_payload, "allowed_claims": ["runtime_probe", "operator_ladder_attribution"], "forbidden_claims": ["candidate_selection", "forward_passed", "live_readiness", "operating_promotion", "runtime_authority", "goal_achieve"], "goal_achieve": "not_claimed"})


def write_final_manifest(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> None:
    payload = dict(final)
    payload["gate_passes"] = sum(1 for gate in gates if gate.get("status") == "passed")
    payload["gate_total"] = len(gates)
    base.write_json(FINAL_DECISION, payload)
    base.write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": now_utc(), "parent_run_id": PARENT_RUN_ID, "attempts": attempts, "inputs": [base.rel(path) for path in INPUT_FILES], "outputs": [base.rel(path) for path in OUTPUT_FILES if base.exists(path)], "gates": base.rel(GATE_AUDIT), "final_decision": base.rel(FINAL_DECISION), "claim_boundary": CLAIM_BOUNDARY})


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run350C ONNX Operator Ladder Runtime Contract Probe(350C 온엑스 연산자 사다리 런타임 계약 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- result_judgment(결과 판정): `{final['result_judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- probability_parity_pass_rows(확률 동등성 통과 행): `{final['probability_parity_pass_rows']}`
- first_failing_operator(첫 실패 연산자): `{final['first_failing_operator']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`

Action(행동): Constant(상수), MatMul/Add(행렬곱/더하기), Sub/Div scaler(스케일러), variable linear output(가변 선형 출력), full MLP logits(전체 MLP 로짓), Softmax(소프트맥스)를 순서대로 MT5에서 실행했다.

Effect(효과): Stage350B(350B 실행)의 ONNX mismatch(온엑스 불일치)가 어느 연산자 경계에서 시작되는지 분리한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    decision = f"""# Stage350C Decision(350C 결정)

- decision(결정): `{final['decision']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`
- first_failing_operator(첫 실패 연산자): `{final['first_failing_operator']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): ONNX operator ladder(온엑스 연산자 사다리) 판정을 다음 실행 조건으로 고정했다.

Effect(효과): 다음 실행은 GEMM-safe ONNX(젬 안전 온엑스), table runtime(테이블 런타임), 또는 새 model family(모델 계열)로 분기할 수 있다.
"""
    current = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{final['status']}`
- current_judgment(현재 판정): `{final['judgment']}`
- current_decision(현재 결정): `{final['decision']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): run350C(350C 실행)는 ONNX operator ladder(온엑스 연산자 사다리)를 MT5에서 탐침했다.

Effect(효과): 다음 작업은 첫 실패 연산자(`{final['first_failing_operator']}`) 기준으로 런타임 안전 모델 경로를 고른다.
"""
    selection = f"""# Stage350 Selection Status(350단계 선택 상태)

- selection_status(선정 상태): `no_selection(선정 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- latest_judgment(최근 판정): `{final['judgment']}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    base.write_bom_text(REPORT_PATH, report)
    base.write_bom_text(DECISION_DOC, decision)
    base.write_bom_text(CURRENT_WORKING_STATE, current)
    base.write_bom_text(SELECTION_STATUS, selection)
    base.write_bom_text(ROOT_SELECTION_STATUS, selection)
    base.append_text_once(STAGE_BRIEF, "## run350C ONNX Operator Ladder Runtime Contract Probe", f"""## run350C ONNX Operator Ladder Runtime Contract Probe(350C 온엑스 연산자 사다리 런타임 계약 탐침)

- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- first_failing_operator(첫 실패 연산자): `{final['first_failing_operator']}`
""")
    changelog = f"""## {TODAY} run350C ONNX Operator Ladder Runtime Contract Probe

- action(행동): ONNX operator ladder(온엑스 연산자 사다리) 변형 `{final['attempt_rows']}`개를 MT5 Strategy Tester(전략 테스터)로 실행했다.
- effect(효과): first_failing_operator(첫 실패 연산자) `{final['first_failing_operator']}`와 next(다음) `{final['next_run_id']}`를 기록했다.
"""
    base.append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run350C ONNX Operator Ladder Runtime Contract Probe", changelog)
    base.append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run350C ONNX Operator Ladder Runtime Contract Probe", changelog)


def write_registers(final: Mapping[str, Any]) -> None:
    base.write_bom_text(WORKSPACE_STATE, "\n".join([f"current_stage_id: {STAGE_ID}", f"current_run_id: {final['next_run_id']}", f"latest_completed_run_id: {RUN_ID}", f"current_status: {final['status']}", f"current_judgment: {final['judgment']}", f"current_decision: {final['decision']}", f"next_run_id: {final['next_run_id']}", f"claim_boundary: {CLAIM_BOUNDARY}", f"updated_at: {TODAY}", ""]))
    run_row = {"run_id": RUN_ID, "stage_id": STAGE_ID, "run_number": RUN_NUMBER, "parent_run_id": PARENT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "result_judgment": final["result_judgment"], "decision": final["decision"], "next_run_id": final["next_run_id"], "report_path": base.rel(REPORT_PATH), "final_decision_path": base.rel(FINAL_DECISION), "gate_audit_path": base.rel(GATE_AUDIT), "created_at": TODAY, "claim_boundary": CLAIM_BOUNDARY, "attempt_count": final["attempt_rows"], "runtime_completed_rows": final["runtime_completed_rows"]}
    base.append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    ledger_base = {"stage_id": STAGE_ID, "run_id": RUN_ID, "run_number": RUN_NUMBER, "status": final["status"], "judgment": final["judgment"], "result_judgment": final["result_judgment"], "report_path": base.rel(REPORT_PATH), "final_decision_path": base.rel(FINAL_DECISION), "claim_boundary": CLAIM_BOUNDARY, "created_at": TODAY, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "next_run_id": final["next_run_id"], "primary_kpi": f"first_failing_operator={final['first_failing_operator']}", "guardrail_kpi": "no_trading_diagnostic_run(거래 없음 진단 실행)"}
    rows = [
        {**ledger_base, "ledger_row_id": f"{RUN_ID}__Tier A", "subrun_id": "Tier A", "view": "Tier A used(Tier A 사용)", "record_view": "Tier A used(Tier A 사용)", "tier": "Tier A", "tier_scope": "Tier A", "metric_scope": "operator_ladder_runtime_probe", "kpi_scope": "MT5 runtime telemetry(MT5 런타임 텔레메트리)"},
        {**ledger_base, "ledger_row_id": f"{RUN_ID}__Tier B", "subrun_id": "Tier B", "view": "Tier B fallback used(Tier B 대체 사용)", "record_view": "Tier B fallback used(Tier B 대체 사용)", "tier": "Tier B", "tier_scope": "Tier B", "metric_scope": "missing_required", "kpi_scope": "missing_required", "result_status": "missing_required(필수 누락)"},
        {**ledger_base, "ledger_row_id": f"{RUN_ID}__Tier A+B", "subrun_id": "Tier A+B", "view": "Tier A+B combined(Tier A+B 합산)", "record_view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "tier_scope": "Tier A+B", "metric_scope": "same_as_tier_a_until_tier_b_available", "kpi_scope": "same_as_tier_a_until_tier_b_available"},
    ]
    base.append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    base.append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)


def update_artifact_registry() -> None:
    rows = []
    for path in OUTPUT_FILES:
        if base.exists(path):
            rows.append({"artifact_id": f"{RUN_ID}__{base.rel(path).replace('/', '__').replace('.', '_')}", "stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": path.suffix.lstrip(".") or "artifact", "path": base.rel(path), "artifact_path": base.rel(path), "sha256": base.sha256_file(path) if path.is_file() else "", "created_at": TODAY, "created_at_utc": now_utc(), "claim_boundary": CLAIM_BOUNDARY})
    base.append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def validate(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    missing = [base.rel(path) for path in [FINAL_DECISION, RUN_MANIFEST, GATE_AUDIT, REPORT_PATH, SUMMARY_CSV, EXPECTED_TAPE, VARIANT_PACKAGE] if not base.exists(path)]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    failed = [gate["gate_id"] for gate in gates if gate.get("status") != "passed"]
    if failed and not str(final.get("status", "")).startswith("blocked_"):
        raise RuntimeError("required gate audit failed(필수 게이트 감사 실패): " + ", ".join(failed))
    if final.get("goal_achieve") != "not_claimed":
        raise RuntimeError("forbidden goal claim(금지된 목표 주장)")


def main() -> None:
    patch_base_globals()
    for directory in [RUN_DIR, MODEL_DIR, MT5_DIR, SET_DIR, INI_DIR, TELEMETRY_COPY_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        os.makedirs(base.fs_path(directory), exist_ok=True)
    for path in INPUT_FILES:
        base.required(path)
    args = parse_args()
    feature_order = base.run349e.load_feature_order()
    frame = base.load_research_frame(feature_order)
    x_all = frame.loc[:, list(feature_order)].to_numpy(dtype=np.float32, copy=True)
    variants, probability_by_attempt = materialize_operator_variants(frame, feature_order, x_all)
    screen_rows = base.screen_thresholds(frame, variants, probability_by_attempt)
    selected = base.select_thresholds(variants, screen_rows, Path(args.common_files_root))
    base.write_expected_tape(frame, selected, probability_by_attempt)
    attempts = base.materialize_mt5_files(selected)
    execution_results, report_records, copy_rows = base.execute_attempts(args, attempts)
    summary_rows, diff_rows = base.compare_outputs(attempts, execution_results, report_records)
    base.write_runtime_identity(args, attempts)
    final_seed = build_final(args, attempts, summary_rows, diff_rows, copy_rows)
    write_receipts(final_seed, attempts)
    base.write_csv(NEXT_ACTION_QUEUE, [{"queue_id": final_seed["next_run_id"], "stage_id": STAGE_ID, "source_run_id": RUN_ID, "priority": 1, "action": "continue_from_operator_ladder_attribution", "effect": "Use first failing ONNX operator to choose runtime-safe model path.", "claim_boundary": CLAIM_BOUNDARY}])
    gates = make_gates(final_seed)
    base.write_csv(GATE_AUDIT, gates)
    write_final_manifest(final_seed, gates, attempts)
    final = base.read_json(FINAL_DECISION)
    write_docs(final)
    write_registers(final)
    update_artifact_registry()
    gates = make_gates(final)
    base.write_csv(GATE_AUDIT, gates)
    write_final_manifest(final, gates, attempts)
    final = base.read_json(FINAL_DECISION)
    write_docs(final)
    write_registers(final)
    update_artifact_registry()
    validate(final, gates)
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "judgment": final["judgment"], "result_judgment": final["result_judgment"], "attempts": final["attempt_rows"], "runtime_completed_rows": final["runtime_completed_rows"], "probability_parity_pass_rows": final["probability_parity_pass_rows"], "first_failing_operator": final["first_failing_operator"], "gates": f"{final['gate_passes']}/{final['gate_total']}", "goal_achieve": final["goal_achieve"], "next_run_id": final["next_run_id"]}, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
