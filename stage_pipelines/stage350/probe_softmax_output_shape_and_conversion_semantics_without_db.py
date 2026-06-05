from __future__ import annotations

import argparse
import copy
import json
import math
import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import onnx
import onnxruntime as ort
import pandas as pd
from onnx import TensorProto, helper, numpy_helper


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337.execute_model_scout_mt5_runtime_probe_without_db import (  # noqa: E402
    terminal_processes,
)
from stage_pipelines.stage348 import (  # noqa: E402
    materialize_onnx_deployable_short_carry_probe_package_without_db as source_pkg,
)
from stage_pipelines.stage349 import (  # noqa: E402
    repair_treeensemble_onnx_operator_or_pivot_model_family_without_db as run349e,
)
from stage_pipelines.stage349 import (  # noqa: E402
    review_onnx_short_carry_mt5_probe_without_db as review349c,
)


TODAY = "2026-06-01"
STAGE_ID = "350_onnx_runtime_interop__softmax_output_shape_repair_probe"
RUN_NUMBER = "run350B"
RUN_ID = "run350B_probe_softmax_output_shape_and_conversion_semantics_without_db_v1"
PARENT_RUN_ID = "run350A_branch_stage349_to_onnx_runtime_interop_repair_without_db_v1"
SOURCE_RUNTIME_RUN_ID = run349e.RUN_ID
SOURCE_PACKAGE_RUN_ID = source_pkg.RUN_ID
NEXT_IF_REPAIR_POSITIVE = "run350C_rebuild_runtime_compatible_temperature_scaled_onnx_trade_surface_without_db_v1"
NEXT_IF_NEGATIVE = "run350C_open_runtime_output_contract_or_new_model_family_pivot_without_db_v1"
NEXT_IF_BLOCKED = "run350B_retry_softmax_output_shape_and_conversion_semantics_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_onnx_runtime_interop_probe_only_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage350/run350B_runtime_interop_probe"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage350_ONNXInterop__SoftmaxOutputShapeConversion"
PARITY_TOLERANCE = 1.0e-4
TRADE_DENSITY_MIN = 3.0
TRADE_DENSITY_TARGET = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run350B_softmax_output_shape_conversion_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage350B_softmax_output_shape_conversion_probe.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN350A_DIR = STAGE_DIR / "02_runs" / "run350A"
RUN350A_FINAL = RUN350A_DIR / "final_decision.json"
RUN350A_GATES = RUN350A_DIR / "required_gate_coverage_audit.csv"
RUN350A_QUEUE = RUN350A_DIR / "run350B_runtime_interop_repair_queue.csv"
RUN349E_DIR = ROOT / "stages" / run349e.STAGE_ID / "02_runs" / "run349E"
RUN349E_FINAL = RUN349E_DIR / "final_decision.json"
RUN349E_SUMMARY = RUN349E_DIR / "runtime_compatible_mlp_mt5_probe_summary.csv"
RUN349E_ATTEMPT_PACKAGE = RUN349E_DIR / "runtime_compatible_mlp_attempt_package.csv"
RUN349E_E01_ONNX = RUN349E_DIR / "models" / "e01_mlp_teacher_balanced.onnx"
RUN349E_E02_ONNX = RUN349E_DIR / "models" / "e02_mlp_histgbm_distill_q95.onnx"

SOURCE_FEATURES = run349e.SOURCE_FEATURES
SOURCE_FEATURE_ORDER = run349e.SOURCE_FEATURE_ORDER
SOURCE_FEATURE_LABEL = run349e.SOURCE_FEATURE_LABEL
SOURCE_PREDICTIONS = run349e.SOURCE_PREDICTIONS

VARIANT_DESIGN = RUN_DIR / "runtime_interop_variant_design.csv"
VARIANT_PACKAGE = RUN_DIR / "runtime_interop_variant_package.csv"
THRESHOLD_SCREEN = RUN_DIR / "runtime_interop_threshold_screen.csv"
PYTHON_ONNX_PROBE = RUN_DIR / "python_onnx_interop_probe.csv"
EXPECTED_TAPE = RUN_DIR / "expected_tape.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
SUMMARY_CSV = RUN_DIR / "softmax_output_shape_conversion_probe_summary.csv"
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
    RUN350A_FINAL,
    RUN350A_GATES,
    RUN350A_QUEUE,
    RUN349E_FINAL,
    RUN349E_SUMMARY,
    RUN349E_ATTEMPT_PACKAGE,
    RUN349E_E01_ONNX,
    RUN349E_E02_ONNX,
    SOURCE_FEATURES,
    SOURCE_FEATURE_ORDER,
    SOURCE_FEATURE_LABEL,
    SOURCE_PREDICTIONS,
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

fs_path = review349c.fs_path
exists = review349c.exists
required = review349c.required
ensure_parent = review349c.ensure_parent
rel = review349c.rel
sha256_file = review349c.sha256_file
read_json = review349c.read_json
write_json = review349c.write_json
write_csv = review349c.write_csv
read_csv_rows = review349c.read_csv_rows
append_or_replace_csv = review349c.append_or_replace_csv
write_bom_text = review349c.write_bom_text
append_text_once = review349c.append_text_once
to_float = review349c.to_float
to_int = review349c.to_int


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage350B ONNX runtime interop probe.")
    parser.add_argument("--terminal-path", default=str(source_pkg.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(source_pkg.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(source_pkg.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(source_pkg.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--reuse-existing-outputs", action="store_true")
    return parser.parse_args()


def norm_time(value: Any) -> str:
    return run349e.norm_time(value)


def fnv1a64_upper(line: str) -> str:
    value = 1469598103934665603
    for char in line:
        value = ((value ^ ord(char)) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return f"{value:X}"


def feature_input_hash_by_time() -> dict[str, str]:
    with open(fs_path(required(SOURCE_FEATURES)), encoding="utf-8-sig", newline="") as handle:
        header = handle.readline().rstrip("\r\n")
        columns = header.split(",")
        try:
            time_idx = columns.index("bar_time_server")
        except ValueError as exc:
            raise RuntimeError("runtime_features.csv missing bar_time_server") from exc
        output: dict[str, str] = {}
        for raw in handle:
            line = raw.rstrip("\r\n")
            parts = line.split(",")
            if len(parts) <= time_idx:
                continue
            output[norm_time(parts[time_idx])] = fnv1a64_upper(line)
    return output


def gate_passed(path: Path) -> bool:
    _fields, rows = read_csv_rows(required(path))
    return bool(rows) and all(str(row.get("status", "")).lower() == "passed" for row in rows)


def class_id(label: str) -> int:
    return {"short": 0, "flat": 1, "long": 2}.get(label, 1)


def load_research_frame(feature_order: Sequence[str]) -> pd.DataFrame:
    frame = run349e.load_frames(feature_order).copy()
    for feature in feature_order:
        frame[feature] = pd.to_numeric(frame[feature], errors="coerce").fillna(0.0).astype(np.float32)
    frame["minutes_from_cash_open"] = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce").fillna(999.0)
    frame["long_quality_teacher_label"] = pd.to_numeric(frame["long_quality_teacher_label"], errors="coerce").fillna(0.0)
    frame["short_carry_teacher_label"] = pd.to_numeric(frame["short_carry_teacher_label"], errors="coerce").fillna(0.0)
    return frame


def model_io(input_shape: Sequence[int | str], output_shape: Sequence[int | str]) -> tuple[Any, Any]:
    return (
        helper.make_tensor_value_info("float_input", TensorProto.FLOAT, list(input_shape)),
        helper.make_tensor_value_info("probabilities", TensorProto.FLOAT, list(output_shape)),
    )


def split_pre_softmax(source: onnx.ModelProto) -> tuple[list[Any], list[Any], str]:
    nodes: list[Any] = []
    logits_name = ""
    for node in source.graph.node:
        if node.op_type == "Softmax":
            logits_name = str(node.input[0])
            break
        nodes.append(copy.deepcopy(node))
    if not logits_name:
        raise RuntimeError("source ONNX missing Softmax node")
    initializers = [copy.deepcopy(init) for init in source.graph.initializer]
    return nodes, initializers, logits_name


def set_model_versions(model: onnx.ModelProto) -> onnx.ModelProto:
    model.ir_version = 7
    del model.opset_import[:]
    model.opset_import.extend([helper.make_operatorsetid("", 12)])
    onnx.checker.check_model(model)
    return model


def build_constant_model(path: Path, feature_count: int) -> None:
    value = np.asarray([[0.20, 0.55, 0.25]], dtype=np.float32)
    node = helper.make_node(
        "Constant",
        inputs=[],
        outputs=["probabilities"],
        name="constant_probability_output",
        value=numpy_helper.from_array(value, name="constant_probability_value"),
    )
    input_info, output_info = model_io([1, feature_count], [1, 3])
    graph = helper.make_graph([node], "stage350B_constant_probability_canary", [input_info], [output_info])
    model = set_model_versions(helper.make_model(graph))
    ensure_parent(path)
    path.write_bytes(model.SerializeToString())


def build_softmax_variant(
    source_path: Path,
    target_path: Path,
    *,
    graph_mode: str,
    temperature: float,
    feature_count: int,
) -> None:
    source = onnx.load(fs_path(required(source_path)))
    nodes, initializers, logits_name = split_pre_softmax(source)
    current = logits_name
    if temperature != 1.0:
        temp_name = "temperature_scale"
        initializers.append(numpy_helper.from_array(np.asarray([temperature], dtype=np.float32), name=temp_name))
        nodes.append(helper.make_node("Div", [current, temp_name], ["temperature_logits"], name="temperature_scale_logits"))
        current = "temperature_logits"
    if graph_mode == "softmax_op":
        nodes.append(helper.make_node("Softmax", [current], ["probabilities"], name="probability_softmax", axis=1))
    elif graph_mode == "explicit_stable_softmax":
        nodes.extend(
            [
                helper.make_node("ReduceMax", [current], ["max_logits"], name="softmax_reduce_max", axes=[1], keepdims=1),
                helper.make_node("Sub", [current, "max_logits"], ["shifted_logits"], name="softmax_shift_logits"),
                helper.make_node("Exp", ["shifted_logits"], ["exp_logits"], name="softmax_exp"),
                helper.make_node("ReduceSum", ["exp_logits"], ["sum_exp_logits"], name="softmax_reduce_sum", axes=[1], keepdims=1),
                helper.make_node("Div", ["exp_logits", "sum_exp_logits"], ["probabilities"], name="softmax_divide"),
            ]
        )
    else:
        raise ValueError(f"unsupported graph mode: {graph_mode}")
    input_info, output_info = model_io([1, feature_count], [1, 3])
    graph = helper.make_graph(
        nodes,
        f"stage350B_{graph_mode}_temperature_{temperature:g}",
        [input_info],
        [output_info],
        initializer=initializers,
    )
    model = set_model_versions(helper.make_model(graph))
    ensure_parent(target_path)
    target_path.write_bytes(model.SerializeToString())


def run_onnx_probabilities(path: Path, matrix: np.ndarray) -> np.ndarray:
    session = ort.InferenceSession(fs_path(path), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    rows: list[np.ndarray] = []
    for index in range(matrix.shape[0]):
        output = session.run(None, {input_name: matrix[index : index + 1].astype(np.float32)})[0]
        rows.append(np.asarray(output, dtype=np.float32).reshape(1, 3))
    return np.vstack(rows)


def variant_definitions() -> list[dict[str, Any]]:
    return [
        {
            "attempt_name": "b00_constant_vector_fixed_noconv",
            "source_model": "constant",
            "source_path": "",
            "graph_mode": "constant",
            "temperature": 1.0,
            "no_conversion": True,
            "set_output_shape": True,
            "allow_trading": False,
            "purpose": "output_buffer_canary",
        },
        {
            "attempt_name": "b01_e02_softmax_fixed_noconv",
            "source_model": "e02_mlp_histgbm_distill_q95",
            "source_path": RUN349E_E02_ONNX,
            "graph_mode": "softmax_op",
            "temperature": 1.0,
            "no_conversion": True,
            "set_output_shape": True,
            "allow_trading": True,
            "purpose": "fixed_shape_baseline",
        },
        {
            "attempt_name": "b02_e02_explicit_softmax_fixed_noconv",
            "source_model": "e02_mlp_histgbm_distill_q95",
            "source_path": RUN349E_E02_ONNX,
            "graph_mode": "explicit_stable_softmax",
            "temperature": 1.0,
            "no_conversion": True,
            "set_output_shape": True,
            "allow_trading": True,
            "purpose": "softmax_operator_replacement",
        },
        {
            "attempt_name": "b03_e02_temp16_softmax_fixed_noconv",
            "source_model": "e02_mlp_histgbm_distill_q95",
            "source_path": RUN349E_E02_ONNX,
            "graph_mode": "softmax_op",
            "temperature": 16.0,
            "no_conversion": True,
            "set_output_shape": True,
            "allow_trading": True,
            "purpose": "numeric_saturation_temperature_probe",
        },
        {
            "attempt_name": "b04_e02_temp16_softmax_fixed_conversion",
            "source_model": "e02_mlp_histgbm_distill_q95",
            "source_path": RUN349E_E02_ONNX,
            "graph_mode": "softmax_op",
            "temperature": 16.0,
            "no_conversion": False,
            "set_output_shape": True,
            "allow_trading": True,
            "purpose": "conversion_flag_probe",
        },
        {
            "attempt_name": "b05_e02_temp64_softmax_fixed_noconv",
            "source_model": "e02_mlp_histgbm_distill_q95",
            "source_path": RUN349E_E02_ONNX,
            "graph_mode": "softmax_op",
            "temperature": 64.0,
            "no_conversion": True,
            "set_output_shape": True,
            "allow_trading": True,
            "purpose": "wide_temperature_saturation_probe",
        },
    ]


def materialize_onnx_variants(feature_count: int, x_all: np.ndarray) -> tuple[list[dict[str, Any]], dict[str, np.ndarray]]:
    variants: list[dict[str, Any]] = []
    probability_by_attempt: dict[str, np.ndarray] = {}
    probe_rows: list[dict[str, Any]] = []
    for definition in variant_definitions():
        attempt_name = str(definition["attempt_name"])
        model_path = MODEL_DIR / f"{attempt_name}.onnx"
        if definition["graph_mode"] == "constant":
            build_constant_model(model_path, feature_count)
        else:
            build_softmax_variant(
                Path(definition["source_path"]),
                model_path,
                graph_mode=str(definition["graph_mode"]),
                temperature=float(definition["temperature"]),
                feature_count=feature_count,
            )
        probabilities = run_onnx_probabilities(model_path, x_all)
        row_sums = probabilities.sum(axis=1)
        max_prob = probabilities.max(axis=1)
        min_prob = probabilities.min(axis=1)
        probe_rows.append(
            {
                "attempt_name": attempt_name,
                "source_model": definition["source_model"],
                "graph_mode": definition["graph_mode"],
                "temperature": definition["temperature"],
                "no_conversion": definition["no_conversion"],
                "set_output_shape": definition["set_output_shape"],
                "allow_trading": definition["allow_trading"],
                "model_path": rel(model_path),
                "model_sha256": sha256_file(model_path),
                "probability_row_sum_min": float(np.min(row_sums)),
                "probability_row_sum_max": float(np.max(row_sums)),
                "probability_min": float(np.min(min_prob)),
                "probability_max": float(np.max(max_prob)),
                "expected_saturation_rows": int(np.sum(max_prob >= 0.999999)),
                "status": "passed" if np.all(np.isfinite(probabilities)) and np.max(np.abs(row_sums - 1.0)) <= 1.0e-4 else "failed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        variant = {**definition, "model_path": model_path, "model_sha256": sha256_file(model_path)}
        variants.append(variant)
        probability_by_attempt[attempt_name] = probabilities
    write_csv(VARIANT_DESIGN, variants)
    write_csv(PYTHON_ONNX_PROBE, probe_rows)
    return variants, probability_by_attempt


def decide_label(p_short: float, p_flat: float, p_long: float, short_threshold: float, long_threshold: float) -> str:
    return run349e.decision_from_probs(p_short, p_flat, p_long, short_threshold, long_threshold)


def apply_side_filter(label: str, minutes_from_cash_open: float) -> str:
    return run349e.apply_side_filter(label, minutes_from_cash_open)


def screen_thresholds(
    frame: pd.DataFrame,
    variants: Sequence[Mapping[str, Any]],
    probability_by_attempt: Mapping[str, np.ndarray],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    quantiles = [0.70, 0.80, 0.85, 0.90, 0.95, 0.98]
    split_values = frame["split"].astype(str).to_numpy()
    minutes = frame["minutes_from_cash_open"].to_numpy(dtype=float)
    long_teacher = frame["long_quality_teacher_label"].to_numpy(dtype=float)
    short_teacher = frame["short_carry_teacher_label"].to_numpy(dtype=float)
    train_mask = split_values == "train"
    for variant in variants:
        attempt_name = str(variant["attempt_name"])
        probs = probability_by_attempt[attempt_name]
        if not bool(variant["allow_trading"]):
            rows.append(
                {
                    "attempt_name": attempt_name,
                    "split": "all",
                    "q_long": "canary",
                    "q_short": "canary",
                    "long_threshold": 0.99,
                    "short_threshold": 0.99,
                    "signal_rows": 0,
                    "predicted_long_rows": 0,
                    "predicted_short_rows": 0,
                    "teacher_hit_rows": 0,
                    "teacher_precision": 0.0,
                    "long_short_balance": 0.0,
                    "selection_score": 0.0,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        for q_long in quantiles:
            long_threshold = float(np.quantile(probs[train_mask, 2], q_long))
            for q_short in quantiles:
                short_threshold = float(np.quantile(probs[train_mask, 0], q_short))
                labels = np.empty(len(frame), dtype=object)
                for idx in range(len(frame)):
                    raw_label = decide_label(
                        float(probs[idx, 0]),
                        float(probs[idx, 1]),
                        float(probs[idx, 2]),
                        short_threshold,
                        long_threshold,
                    )
                    labels[idx] = apply_side_filter(raw_label, float(minutes[idx]))
                for split_name in ["train", "validation", "test", "all"]:
                    mask = np.ones(len(frame), dtype=bool) if split_name == "all" else split_values == split_name
                    split_labels = labels[mask]
                    long_rows = int(np.sum(split_labels == "long"))
                    short_rows = int(np.sum(split_labels == "short"))
                    signal_rows = int(long_rows + short_rows)
                    hits = int(np.sum((split_labels == "long") & (long_teacher[mask] > 0))) + int(
                        np.sum((split_labels == "short") & (short_teacher[mask] > 0))
                    )
                    precision = hits / signal_rows if signal_rows else 0.0
                    balance = min(long_rows, short_rows) / max(1, max(long_rows, short_rows))
                    target_penalty = abs(signal_rows - 450) / 450 if split_name == "all" else 0.0
                    saturation_penalty = float(np.mean(probs[mask].max(axis=1) >= 0.999999))
                    score = (hits * 3.0) + (precision * 200.0) + (balance * 40.0) - (target_penalty * 40.0) - (
                        saturation_penalty * 15.0
                    )
                    rows.append(
                        {
                            "attempt_name": attempt_name,
                            "split": split_name,
                            "q_long": q_long,
                            "q_short": q_short,
                            "long_threshold": long_threshold,
                            "short_threshold": short_threshold,
                            "signal_rows": signal_rows,
                            "predicted_long_rows": long_rows,
                            "predicted_short_rows": short_rows,
                            "teacher_hit_rows": hits,
                            "teacher_precision": precision,
                            "long_short_balance": balance,
                            "expected_saturation_rate": saturation_penalty,
                            "selection_score": score,
                            "allowed_use": "proxy_signal_sanity_only",
                            "forbidden_use": "MT5_KPI_substitute_or_operating_selection",
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )
    write_csv(THRESHOLD_SCREEN, rows)
    return rows


def select_thresholds(
    variants: Sequence[Mapping[str, Any]],
    screen_rows: Sequence[Mapping[str, Any]],
    common_files_root: Path,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for idx, variant in enumerate(variants, start=1):
        attempt_name = str(variant["attempt_name"])
        all_rows = [row for row in screen_rows if row["attempt_name"] == attempt_name and row["split"] == "all"]
        eligible = [row for row in all_rows if 250 <= int(float(row["signal_rows"])) <= 900]
        if not eligible:
            eligible = all_rows
        best = sorted(eligible, key=lambda row: float(row["selection_score"]), reverse=True)[0]
        model_common_path = f"{COMMON_MODEL_DIR}/{attempt_name}.onnx"
        common_model_abs = common_files_root / Path(model_common_path)
        ensure_parent(common_model_abs)
        shutil.copy2(fs_path(Path(variant["model_path"])), fs_path(common_model_abs))
        selected.append(
            {
                **variant,
                "model_id": f"stage350B_{attempt_name}",
                "model_path": rel(Path(variant["model_path"])),
                "model_common_path": model_common_path,
                "model_common_sha256": sha256_file(common_model_abs),
                "feature_csv_path": "Project_Obsidian_Prime_v2/stage348/run348C_onnx_short_carry_probe/features/runtime_features.csv",
                "feature_count": len(run349e.load_feature_order()),
                "feature_order_hash": "870630295e4a4f15a168230f75a27726e910d8ba141270e1b2140cdd4519ba0c",
                "long_threshold": float(best["long_threshold"]),
                "short_threshold": float(best["short_threshold"]),
                "q_long": best["q_long"],
                "q_short": best["q_short"],
                "proxy_signal_rows": best["signal_rows"],
                "proxy_teacher_precision": best.get("teacher_precision", ""),
                "from_date": "2024.07.30",
                "to_date": "2025.01.01",
                "tier": "Tier A",
                "split": "all_rows_train_selected_thresholds",
                "magic": 3508000 + idx,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return selected


def write_expected_tape(
    frame: pd.DataFrame,
    attempts: Sequence[Mapping[str, Any]],
    probability_by_attempt: Mapping[str, np.ndarray],
) -> None:
    feature_hashes = feature_input_hash_by_time()
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        probs = probability_by_attempt[attempt_name]
        for idx, row in frame.iterrows():
            raw_label = decide_label(
                float(probs[idx, 0]),
                float(probs[idx, 1]),
                float(probs[idx, 2]),
                float(attempt["short_threshold"]),
                float(attempt["long_threshold"]),
            )
            mapped = apply_side_filter(raw_label, float(row["minutes_from_cash_open"]))
            bar_time = norm_time(row["bar_time_server"])
            rows.append(
                {
                    "attempt_name": attempt_name,
                    "bar_time_server": row["bar_time_server"],
                    "timestamp_utc": row["timestamp_utc"],
                    "split": row["split"],
                    "row_index": int(row["row_index"]),
                    "mt5_input_hash": feature_hashes.get(bar_time, ""),
                    "p_short": float(probs[idx, 0]),
                    "p_flat": float(probs[idx, 1]),
                    "p_long": float(probs[idx, 2]),
                    "proxy_intended_label": raw_label,
                    "ea_mapped_expected_label": mapped,
                    "expected_class_id": class_id(mapped),
                    "long_probability_threshold": attempt["long_threshold"],
                    "short_probability_threshold": attempt["short_threshold"],
                    "allowed_use": "proxy_vs_mt5_runtime_probe_comparison",
                    "forbidden_use": "MT5_KPI_substitute_or_operating_selection",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(EXPECTED_TAPE, rows)


def materialize_mt5_files(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        common_telemetry = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv"
        common_summary = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv"
        set_name = f"OPV2_run350B_{attempt_name}.set"
        ini_name = f"OPV2_run350B_{attempt_name}.ini"
        report_name = f"POPv2_run350B_{attempt_name}"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        set_values = {
            "InpRunId": f"{RUN_ID}_{attempt_name}",
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "all_rows_train_selected_thresholds",
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpEnforceM5": True,
            "InpFeatureCsvPath": attempt["feature_csv_path"],
            "InpFeatureCount": int(attempt["feature_count"]),
            "InpFeatureCsvUseCommonFiles": True,
            "InpFeatureRequireTimestampMatch": True,
            "InpFeatureAllowLatestFallback": False,
            "InpFeatureStrictHeader": True,
            "InpFeatureCsvDelimiter": ",",
            "InpCsvTimestampIsBarClose": True,
            "InpModelPath": attempt["model_common_path"],
            "InpModelId": attempt["model_id"],
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": bool(attempt["no_conversion"]),
            "InpSetOutputShape": bool(attempt["set_output_shape"]),
            "InpFeatureOrderHash": attempt["feature_order_hash"],
            "InpFallbackEnabled": False,
            "InpShortThreshold": float(attempt["short_threshold"]),
            "InpLongThreshold": float(attempt["long_threshold"]),
            "InpMinMargin": -1.0,
            "InpDecisionMode": "threshold_margin",
            "InpInvertSignal": False,
            "InpSideFilterEnabled": True,
            "InpSideFilterFeatureIndex": 37,
            "InpFallbackSideFilterFeatureIndex": 37,
            "InpBlockShortFeatureRange": False,
            "InpBlockShortFeatureMin": 0,
            "InpBlockShortFeatureMax": 0,
            "InpBlockLongFeatureRange": True,
            "InpBlockLongFeatureMin": 0,
            "InpBlockLongFeatureMax": 60,
            "InpAllowTrading": bool(attempt["allow_trading"]),
            "InpFixedLot": 0.1,
            "InpMagic": int(attempt["magic"]),
            "InpDeviationPoints": 20,
            "InpCloseOnFlatSignal": False,
            "InpReverseOnOppositeSignal": True,
            "InpCloseOnlyOnOppositeSignal": False,
            "InpMaxHoldBars": 12,
            "InpMaxConcurrentPositions": 1,
            "InpReentryCooldownBars": 0,
            "InpSameDirectionReentryCooldownBars": 0,
            "InpEntryTransitionOnly": False,
            "InpExitRiskOverlayEnabled": False,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": common_telemetry,
            "InpSummaryCsvPath": common_summary,
        }
        set_payload = mt5.materialize_tester_set_file(
            set_values,
            set_path,
            generated_by="stage_pipelines/stage350/probe_softmax_output_shape_and_conversion_semantics_without_db.py",
        )
        cfg = mt5.TesterMaterializationConfig(
            shutdown_terminal=1,
            from_date=str(attempt["from_date"]),
            to_date=str(attempt["to_date"]),
            report=report_name,
        )
        ini_payload = mt5.materialize_tester_ini_file(cfg, ini_path, set_file_path=Path(set_name))
        rows.append(
            {
                **attempt,
                "set_name": set_name,
                "ini_name": ini_name,
                "set_path": rel(set_path),
                "ini_path": rel(ini_path),
                "set_sha256": set_payload["sha256"],
                "ini_sha256": ini_payload["sha256"],
                "common_telemetry_path": common_telemetry,
                "common_summary_path": common_summary,
                "report_name": report_name,
                "ini": {"tester": {"Report": report_name}},
                "allowed_use": "MT5 runtime probe",
                "forbidden_use": "candidate_selection_or_operating_claim",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(VARIANT_PACKAGE, rows)
    return rows


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        path = common_files_root / Path(str(attempt[key]))
        if exists(path):
            os.unlink(fs_path(path))


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        for key, suffix in (("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")):
            source = common_files_root / Path(str(attempt[key]))
            target = TELEMETRY_COPY_DIR / f"{attempt_name}_{suffix}.csv"
            copied = False
            if exists(source):
                ensure_parent(target)
                shutil.copy2(fs_path(source), fs_path(target))
                copied = True
            rows.append(
                {
                    "copy_id": f"{attempt_name}::{suffix}",
                    "attempt_name": attempt_name,
                    "source_path": source.as_posix(),
                    "target_path": rel(target),
                    "exists": copied and exists(target),
                    "sha256": sha256_file(target) if copied and exists(target) else "",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(RUNTIME_OUTPUT_COPY, rows)
    return rows


def execute_attempts(
    args: argparse.Namespace,
    attempts: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    terminal_probe = terminal_processes()
    write_json(TERMINAL_PROCESS_AUDIT, terminal_probe)
    execution_results: list[dict[str, Any]] = []
    if args.materialize_only:
        for attempt in attempts:
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "status": "not_run_materialize_only",
                    "runtime_outputs": {"status": "not_run_materialize_only"},
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
    elif args.reuse_existing_outputs:
        for attempt in attempts:
            runtime_outputs = mt5.validate_mt5_runtime_outputs(common_files_root, attempt)
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "status": "completed" if runtime_outputs.get("status") == "completed" else "blocked",
                    "runtime_outputs": runtime_outputs,
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
    elif terminal_probe.get("status") != "no_terminal64_process":
        for attempt in attempts:
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "status": "blocked",
                    "blocker": "target_portable_terminal_already_running",
                    "runtime_outputs": {"status": "blocked", "wait_status": "skipped_terminal_already_running"},
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
    else:
        for attempt in attempts:
            remove_runtime_outputs(common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
            try:
                tester_result = mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini_path"]),
                    set_path=ROOT / str(attempt["set_path"]),
                    tester_profile_set_path=tester_profile_root / str(attempt["set_name"]),
                    tester_profile_ini_path=tester_profile_root / str(attempt["ini_name"]),
                    timeout_seconds=args.timeout_seconds,
                    terminal_extra_args=["/portable"],
                )
            except subprocess.TimeoutExpired as exc:
                tester_result = {
                    "status": "blocked",
                    "command": exc.cmd,
                    "returncode": None,
                    "stdout": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
                    "stderr": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
                    "blocker": "terminal_timeout",
                }
            runtime_outputs = mt5.wait_for_mt5_runtime_outputs(
                common_files_root,
                attempt,
                timeout_seconds=args.wait_timeout_seconds,
                poll_seconds=2.0,
            )
            if runtime_outputs.get("status") != "completed":
                tester_result["status"] = "blocked"
                tester_result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            execution_results.append(
                {
                    **tester_result,
                    "attempt_name": attempt["attempt_name"],
                    "runtime_outputs": runtime_outputs,
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=RUN_DIR,
        attempts=attempts,
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    copy_rows = copy_runtime_outputs(common_files_root, attempts)
    write_json(MT5_EXECUTION_RESULT, execution_results)
    write_json(STRATEGY_TESTER_REPORTS, report_records)
    return execution_results, report_records, copy_rows


def expected_by_attempt() -> dict[str, dict[str, Mapping[str, Any]]]:
    expected = pd.read_csv(fs_path(required(EXPECTED_TAPE)), encoding="utf-8-sig", low_memory=False).fillna("")
    return {
        str(attempt_name): {norm_time(row["bar_time_server"]): row.to_dict() for _, row in group.iterrows()}
        for attempt_name, group in expected.groupby("attempt_name")
    }


def compare_outputs(
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    expected_lookup = expected_by_attempt()
    execution_by_attempt = {row.get("attempt_name"): row for row in execution_results}
    report_by_attempt = {row.get("attempt_name"): row for row in report_records}
    summary_rows: list[dict[str, Any]] = []
    diff_rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        local_telemetry = TELEMETRY_COPY_DIR / f"{attempt_name}_telemetry.csv"
        local_summary = TELEMETRY_COPY_DIR / f"{attempt_name}_summary.csv"
        expected = expected_lookup.get(attempt_name, {})
        execution = execution_by_attempt.get(attempt_name, {})
        report = report_by_attempt.get(attempt_name, {})
        metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
        if not exists(local_telemetry):
            summary_rows.append(
                {
                    "attempt_name": attempt_name,
                    "runtime_status": execution.get("runtime_outputs", {}).get("status", "missing"),
                    "report_status": report.get("status", "missing"),
                    "rows_compared": 0,
                    "probability_match_rows": 0,
                    "input_hash_match_rows": 0,
                    "max_abs_diff": "",
                    "attribution": "runtime_telemetry_missing",
                    "parity_status": "blocked_runtime_telemetry_missing",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        telemetry = pd.read_csv(fs_path(local_telemetry), encoding="utf-8-sig", low_memory=False).fillna("")
        cycles = telemetry[telemetry["record_type"].astype(str).str.lower().eq("cycle")].copy()
        cycles = cycles[cycles["feature_ready"].astype(str).str.lower().eq("true")].copy()
        max_abs = 0.0
        matched_time = 0
        probability_match = 0
        input_hash_match = 0
        decision_match = 0
        runtime_saturated = 0
        expected_saturated = 0
        first_mismatch: dict[str, Any] | None = None
        for _, row in cycles.iterrows():
            key = norm_time(row.get("bar_time", ""))
            exp = expected.get(key)
            if exp is None:
                continue
            matched_time += 1
            runtime_probs = np.asarray(
                [to_float(row.get("p_short")), to_float(row.get("p_flat")), to_float(row.get("p_long"))],
                dtype=float,
            )
            expected_probs = np.asarray(
                [to_float(exp.get("p_short")), to_float(exp.get("p_flat")), to_float(exp.get("p_long"))],
                dtype=float,
            )
            diffs = np.abs(runtime_probs - expected_probs)
            row_max = float(np.max(diffs))
            max_abs = max(max_abs, row_max)
            prob_ok = row_max <= PARITY_TOLERANCE
            hash_ok = str(row.get("input_hash", "")).strip().upper() == str(exp.get("mt5_input_hash", "")).strip().upper()
            dec_ok = str(row.get("decision", "")).strip().lower() == str(exp.get("ea_mapped_expected_label", "")).strip().lower()
            probability_match += int(prob_ok)
            input_hash_match += int(hash_ok)
            decision_match += int(dec_ok)
            runtime_saturated += int(float(np.max(runtime_probs)) >= 0.999999)
            expected_saturated += int(float(np.max(expected_probs)) >= 0.999999)
            if not prob_ok and first_mismatch is None:
                first_mismatch = {
                    "bar_time": key,
                    "runtime_p_short": float(runtime_probs[0]),
                    "runtime_p_flat": float(runtime_probs[1]),
                    "runtime_p_long": float(runtime_probs[2]),
                    "expected_p_short": float(expected_probs[0]),
                    "expected_p_flat": float(expected_probs[1]),
                    "expected_p_long": float(expected_probs[2]),
                    "mt5_input_hash": str(row.get("input_hash", "")).strip().upper(),
                    "expected_input_hash": str(exp.get("mt5_input_hash", "")).strip().upper(),
                }
            diff_rows.append(
                {
                    "attempt_name": attempt_name,
                    "bar_time": key,
                    "p_short_abs_diff": float(diffs[0]),
                    "p_flat_abs_diff": float(diffs[1]),
                    "p_long_abs_diff": float(diffs[2]),
                    "row_max_abs_diff": row_max,
                    "probability_match": prob_ok,
                    "input_hash_match": hash_ok,
                    "decision_match": dec_ok,
                    "mt5_decision": row.get("decision", ""),
                    "expected_decision": exp.get("ea_mapped_expected_label", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        if exists(local_summary):
            runtime_summary = pd.read_csv(fs_path(local_summary), encoding="utf-8-sig", low_memory=False).fillna("")
            last_summary = runtime_summary.iloc[-1].to_dict() if not runtime_summary.empty else {}
        else:
            last_summary = {}
        feature_days = len({key[:10] for key in expected if key})
        trade_count = to_int(metrics.get("trade_count"), 0)
        density = trade_count / feature_days if feature_days else 0.0
        probability_parity = matched_time > 0 and probability_match == matched_time and max_abs <= PARITY_TOLERANCE
        input_hash_parity = matched_time > 0 and input_hash_match == matched_time
        attribution = "parity_passed"
        if not input_hash_parity:
            attribution = "feature_handoff_or_hash_mismatch"
        elif not probability_parity and attempt.get("purpose") == "output_buffer_canary":
            attribution = "ea_output_buffer_or_shape_contract_problem"
        elif not probability_parity and expected_saturated > matched_time * 0.8:
            attribution = "model_numeric_saturation_or_softmax_semantics"
        elif not probability_parity:
            attribution = "onnx_runtime_output_semantics_mismatch"
        summary_rows.append(
            {
                "attempt_name": attempt_name,
                "source_model": attempt.get("source_model", ""),
                "graph_mode": attempt.get("graph_mode", ""),
                "temperature": attempt.get("temperature", ""),
                "no_conversion": attempt.get("no_conversion", ""),
                "set_output_shape": attempt.get("set_output_shape", ""),
                "allow_trading": attempt.get("allow_trading", ""),
                "runtime_status": execution.get("runtime_outputs", {}).get("status", "missing"),
                "report_status": report.get("status", "missing"),
                "rows_compared": matched_time,
                "probability_match_rows": probability_match,
                "input_hash_match_rows": input_hash_match,
                "decision_match_rows": decision_match,
                "max_abs_diff": max_abs if matched_time else "",
                "probability_parity": probability_parity,
                "input_hash_parity": input_hash_parity,
                "runtime_saturated_rows": runtime_saturated,
                "expected_saturated_rows": expected_saturated,
                "attribution": attribution,
                "first_mismatch": first_mismatch or {},
                "parity_status": "passed" if probability_parity else "failed_or_missing",
                "net_profit": metrics.get("net_profit", ""),
                "profit_factor": metrics.get("profit_factor", ""),
                "expectancy": metrics.get("expectancy", ""),
                "max_drawdown_amount": metrics.get("max_drawdown_amount", ""),
                "recovery_factor": metrics.get("recovery_factor", ""),
                "trade_count": trade_count,
                "long_trade_count": metrics.get("long_trade_count", ""),
                "short_trade_count": metrics.get("short_trade_count", ""),
                "trade_density_per_feature_day": density,
                "trade_density_status": "meets_min_3_to_10_band" if density >= TRADE_DENSITY_MIN else "below_min_3_per_day",
                "model_ok_count": to_int(last_summary.get("model_ok_count"), 0),
                "feature_ready_count": to_int(last_summary.get("feature_ready_count"), 0),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(PROXY_MT5_DIFF, diff_rows)
    write_csv(SUMMARY_CSV, summary_rows)
    return summary_rows, diff_rows


def write_runtime_identity(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]]) -> None:
    rows = []
    module_hashes = mt5.mt5_runtime_module_hashes()
    for attempt in attempts:
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "terminal_path": args.terminal_path,
                "common_files_root": args.common_files_root,
                "tester_profile_root": args.tester_profile_root,
                "terminal_data_root": args.terminal_data_root,
                "ea_source": rel(mt5.EA_SOURCE_PATH),
                "module_hashes": module_hashes,
                "model_sha256": attempt.get("model_sha256", ""),
                "model_common_sha256": attempt.get("model_common_sha256", ""),
                "set_sha256": attempt.get("set_sha256", ""),
                "ini_sha256": attempt.get("ini_sha256", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(RUNTIME_IDENTITY, rows)


def best_runtime_row(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    tradable = [row for row in summary_rows if str(row.get("allow_trading", "")).lower() == "true"]
    if not tradable:
        return dict(summary_rows[0]) if summary_rows else {}
    return sorted(
        tradable,
        key=lambda row: (
            str(row.get("probability_parity", "")).lower() == "true",
            to_float(row.get("net_profit"), -1e9),
            to_float(row.get("profit_factor"), 0.0),
            to_int(row.get("trade_count"), 0),
        ),
        reverse=True,
    )[0]


def build_final(
    args: argparse.Namespace,
    attempts: Sequence[Mapping[str, Any]],
    summary_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    completed = [row for row in summary_rows if str(row.get("runtime_status", "")) == "completed"]
    canary_rows = [row for row in summary_rows if row.get("attempt_name") == "b00_constant_vector_fixed_noconv"]
    canary_pass = bool(canary_rows and str(canary_rows[0].get("probability_parity", "")).lower() == "true")
    parity_pass_rows = [row for row in summary_rows if str(row.get("probability_parity", "")).lower() == "true"]
    tradable_parity_rows = [
        row for row in parity_pass_rows if str(row.get("allow_trading", "")).lower() == "true"
    ]
    best = best_runtime_row(summary_rows)
    positive_kpi = (
        str(best.get("allow_trading", "")).lower() == "true"
        and str(best.get("probability_parity", "")).lower() == "true"
        and to_float(best.get("net_profit"), 0.0) > 0.0
        and to_float(best.get("profit_factor"), 0.0) > 1.0
        and to_float(best.get("trade_density_per_feature_day"), 0.0) >= TRADE_DENSITY_MIN
    )
    if len(completed) < len(attempts):
        status = "blocked_stage350B_runtime_interop_probe_outputs_missing_no_selection"
        judgment = "blocked_runtime_interop_probe_mt5_outputs_missing_or_terminal_unavailable"
        result_judgment = "blocked(차단)"
        decision = "stage350B_retry_runtime_interop_probe"
        next_run_id = NEXT_IF_BLOCKED
    elif positive_kpi:
        status = "completed_stage350B_runtime_interop_repair_positive_kpi_review_required_no_selection"
        judgment = "repair_positive_runtime_probability_parity_and_positive_mt5_kpi_review_required"
        result_judgment = "repair_positive_review_required(수리 긍정 검토 필요)"
        decision = "stage350B_open_run350C_rebuild_runtime_compatible_temperature_scaled_onnx_trade_surface"
        next_run_id = NEXT_IF_REPAIR_POSITIVE
    elif tradable_parity_rows:
        status = "completed_stage350B_runtime_interop_repair_parity_passed_kpi_weak_no_selection"
        judgment = "runtime_interop_repair_parity_passed_but_mt5_kpi_weak_continue_model_surface_rebuild"
        result_judgment = "negative_or_weak_kpi(부정 또는 약한 KPI)"
        decision = "stage350B_open_run350C_rebuild_or_expand_runtime_compatible_model_surface"
        next_run_id = NEXT_IF_REPAIR_POSITIVE
    elif canary_pass:
        status = "completed_stage350B_output_buffer_canary_passed_model_variants_failed_no_selection"
        judgment = "negative_canary_passed_model_graph_or_numeric_saturation_still_blocks_runtime_parity"
        result_judgment = "negative_runtime_parity(부정 런타임 동등성)"
        decision = "stage350B_open_run350C_output_contract_or_new_model_family_pivot"
        next_run_id = NEXT_IF_NEGATIVE
    else:
        status = "completed_stage350B_output_buffer_canary_failed_ea_output_contract_repair_required_no_selection"
        judgment = "negative_canary_failed_ea_output_buffer_or_shape_contract_repair_required"
        result_judgment = "negative_runtime_contract(부정 런타임 계약)"
        decision = "stage350B_open_run350C_runtime_output_contract_repair"
        next_run_id = NEXT_IF_NEGATIVE
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "result_judgment": result_judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": len(attempts),
        "runtime_completed_rows": len(completed),
        "probability_parity_pass_rows": len(parity_pass_rows),
        "tradable_probability_parity_pass_rows": len(tradable_parity_rows),
        "canary_passed": canary_pass,
        "diff_rows": len(diff_rows),
        "runtime_output_copy_ready_rows": sum(1 for row in copy_rows if str(row.get("exists", "")).lower() == "true"),
        "best_attempt_name": best.get("attempt_name", ""),
        "best_attribution": best.get("attribution", ""),
        "best_net_profit": best.get("net_profit", ""),
        "best_profit_factor": best.get("profit_factor", ""),
        "best_expectancy": best.get("expectancy", ""),
        "best_trade_count": best.get("trade_count", ""),
        "best_trade_density_per_feature_day": best.get("trade_density_per_feature_day", ""),
        "best_max_abs_diff": best.get("max_abs_diff", ""),
        "materialize_only": bool(args.materialize_only),
        "reuse_existing_outputs": bool(args.reuse_existing_outputs),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def write_receipts(final: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]]) -> None:
    base = {"stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": now_utc(), "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "MT5 ONNX runtime mismatch may be output shape, Softmax operator, conversion flag, or numeric saturation.",
            "decision_use": "Choose whether Stage350C should repair EA output contract, rebuild a temperature-scaled ONNX surface, or pivot model family.",
            "comparison_baseline": "run349D TreeEnsemble no-conversion mismatch and run349E pure tensor MLP mismatch.",
            "control_variables": "Stage348 runtime_features, Stage349 tester identity, US100 M5 date range, EA decision surface.",
            "changed_variables": "constant canary, fixed output shape, explicit stable softmax, temperature scaling, conversion flag.",
            "sample_scope": "FPMarkets US100 M5 Tier A Strategy Tester replay 2024.07.30 to 2025.01.01.",
            "success_criteria": "input hash parity plus probability parity, and if tradable, MT5 KPI not breaking trade density.",
            "failure_criteria": "canary or model variants produce probability mismatch or saturated one-hot output.",
            "invalid_conditions": "timestamp drift, feature hash mismatch, missing tester report, or runtime outputs missing.",
            "stop_conditions": "parity repair found, output contract repair needed, or pivot to new model family required.",
            "evidence_plan": [rel(SUMMARY_CSV), rel(PROXY_MT5_DIFF), rel(STRATEGY_TESTER_REPORTS), rel(RUNTIME_IDENTITY)],
        },
    )
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            **base,
            "research_path": rel(PYTHON_ONNX_PROBE),
            "runtime_path": rel(VARIANT_PACKAGE),
            "shared_contract": "feature order 53, output [p_short,p_flat,p_long], thresholds from train-selected proxy screen",
            "known_differences": "constant canary is diagnostic only and not a trading model.",
            "parity_check": rel(SUMMARY_CSV),
            "parity_identity": rel(RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe(런타임 탐침)",
        },
    )
    write_json(
        BACKTEST_FORENSICS_RECEIPT,
        {
            **base,
            "tester_report": rel(STRATEGY_TESTER_REPORTS),
            "tester_settings": "US100 M5, real ticks model, Deposit 500, Leverage 1:100",
            "forensic_gaps": [] if final["runtime_completed_rows"] == final["attempt_rows"] else ["runtime_outputs_missing"],
        },
    )
    write_json(
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        {
            **base,
            "summary": rel(SUMMARY_CSV),
            "best_attempt_name": final["best_attempt_name"],
            "best_attribution": final["best_attribution"],
            "best_net_profit": final["best_net_profit"],
            "best_profit_factor": final["best_profit_factor"],
            "best_trade_count": final["best_trade_count"],
            "judgment": final["judgment"],
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_judgment": final["result_judgment"],
            "status": final["status"],
            "decision": final["decision"],
            "next_run_id": final["next_run_id"],
            "forbidden_claims": ["candidate_selection", "forward_passed", "live_readiness", "operating_promotion", "runtime_authority", "goal_achieve"],
        },
    )
    write_json(
        ARTIFACT_LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": final["next_run_id"],
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in OUTPUT_FILES if exists(path) and path.is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(
        CLAIM_BOUNDARY_RECEIPT,
        {
            **base,
            "allowed_claims": ["runtime_probe", "runtime_interop_repair_evidence"],
            "forbidden_claims": ["candidate_selection", "forward_passed", "live_readiness", "operating_promotion", "runtime_authority", "goal_achieve"],
            "goal_achieve": "not_claimed",
        },
    )


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

    summary_rows = pd.read_csv(fs_path(SUMMARY_CSV), encoding="utf-8-sig").to_dict("records") if exists(SUMMARY_CSV) else []
    completed_all = bool(summary_rows) and all(str(r.get("runtime_status", "")) == "completed" for r in summary_rows)
    input_hash_all = bool(summary_rows) and all(str(r.get("input_hash_parity", "")).lower() == "true" for r in summary_rows if int(float(r.get("rows_compared", 0) or 0)) > 0)
    return [
        row("parent_stage350A_gate", gate_passed(RUN350A_GATES), rel(RUN350A_GATES), "Stage350A branch gate is closed."),
        row("source_run349E_visible", all(exists(path) for path in [RUN349E_FINAL, RUN349E_E01_ONNX, RUN349E_E02_ONNX]), rel(RUN349E_FINAL), "Source ONNX artifacts are visible."),
        row("onnx_variants_materialized", exists(VARIANT_DESIGN) and exists(PYTHON_ONNX_PROBE), rel(PYTHON_ONNX_PROBE), "Interop ONNX variants were materialized and checked in Python."),
        row("expected_tape_written", exists(EXPECTED_TAPE), rel(EXPECTED_TAPE), "Expected tape includes timestamp-safe probabilities and MT5 input hashes."),
        row("mt5_runtime_output_observed", completed_all, rel(MT5_EXECUTION_RESULT), "MT5 runtime telemetry exists for all variants."),
        row("strategy_report_collected", exists(STRATEGY_TESTER_REPORTS), rel(STRATEGY_TESTER_REPORTS), "Strategy Tester reports were collected."),
        row("input_hash_parity_checked", input_hash_all, rel(SUMMARY_CSV), "Feature handoff identity was checked with MT5 line hashes."),
        row("probability_diff_attributed", exists(PROXY_MT5_DIFF) and exists(SUMMARY_CSV), f"{rel(PROXY_MT5_DIFF)};{rel(SUMMARY_CSV)}", "Probability differences were attributed."),
        row("tier_pair_rows_written", exists(STAGE_LEDGER) and exists(PROJECT_LEDGER), f"{rel(STAGE_LEDGER)};{rel(PROJECT_LEDGER)}", "Tier A/B/A+B records were written."),
        row("artifact_lineage_recorded", exists(ARTIFACT_LINEAGE_RECEIPT) and exists(RUN_MANIFEST), f"{rel(ARTIFACT_LINEAGE_RECEIPT)};{rel(RUN_MANIFEST)}", "Artifact lineage was connected."),
        row("final_claim_guard", all(final.get(key) == "not_claimed" for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]), rel(FINAL_DECISION), "Operating claims remain blocked."),
    ]


def write_final_manifest(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> None:
    payload = dict(final)
    payload["gate_passes"] = sum(1 for gate in gates if gate.get("status") == "passed")
    payload["gate_total"] = len(gates)
    write_json(FINAL_DECISION, payload)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": now_utc(),
            "parent_run_id": PARENT_RUN_ID,
            "attempts": attempts,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "gates": rel(GATE_AUDIT),
            "final_decision": rel(FINAL_DECISION),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run350B Softmax Output Shape Conversion Probe(350B 소프트맥스 출력 모양 변환 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- result_judgment(결과 판정): `{final['result_judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- probability_parity_pass_rows(확률 동등성 통과 행): `{final['probability_parity_pass_rows']}`
- canary_passed(카나리 통과): `{final['canary_passed']}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_attribution(최고 시도 귀속): `{final['best_attribution']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_trade_count(최고 거래 수): `{final['best_trade_count']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`

Action(행동): fixed output shape(고정 출력 모양), explicit softmax(명시 소프트맥스), temperature scaling(온도 스케일링), conversion flag(변환 플래그)를 MT5 Strategy Tester(전략 테스터)에서 비교했다.

Effect(효과): ONNX probability mismatch(온엑스 확률 불일치)를 output buffer(출력 버퍼), graph semantics(그래프 의미), numeric saturation(숫자 포화), model KPI(모델 핵심 성과) 중 어디에 붙일지 좁혔다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    decision = f"""# Stage350B Decision(350B 결정)

- decision(결정): `{final['decision']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`
- result_judgment(결과 판정): `{final['result_judgment']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): runtime interop probe(런타임 상호운용 탐침)를 닫고 다음 수리 방향을 고정했다.

Effect(효과): 다음 실행은 MT5 evidence(MT5 근거)를 기준으로 output contract repair(출력 계약 수리) 또는 runtime-compatible model rebuild(런타임 호환 모델 재구축)로 간다.
"""
    current = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{final['status']}`
- current_judgment(현재 판정): `{final['judgment']}`
- current_decision(현재 결정): `{final['decision']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): run350B(350B 실행)는 ONNX output semantics(온엑스 출력 의미)를 MT5에서 탐침했다.

Effect(효과): 다음 작업은 확률 동등성(parity, 동등성) 결과에 맞춰 모델 재구축 또는 런타임 출력 계약 수리를 진행한다.
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
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    append_text_once(
        STAGE_BRIEF,
        "## run350B Softmax Output Shape Conversion Probe",
        f"""## run350B Softmax Output Shape Conversion Probe(350B 소프트맥스 출력 모양 변환 탐침)

- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- judgment(판정): `{final['judgment']}`

Action(행동): Stage350B(350B 실행)는 softmax/output shape/conversion(소프트맥스/출력 모양/변환) 조합을 MT5에서 비교했다.

Effect(효과): Stage350(350단계)의 다음 질문은 `{final['next_run_id']}`로 좁혀졌다.
""",
    )
    changelog = f"""## {TODAY} run350B Softmax Output Shape Conversion Probe

- action(행동): ONNX runtime interop(온엑스 런타임 상호운용) 변형 `{final['attempt_rows']}`개를 MT5 Strategy Tester(전략 테스터)로 실행했다.
- effect(효과): best_attempt(최고 시도) `{final['best_attempt_name']}`, net_profit(순수익) `{final['best_net_profit']}`, PF(수익 팩터) `{final['best_profit_factor']}`, next(다음) `{final['next_run_id']}`를 기록했다.
"""
    append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run350B Softmax Output Shape Conversion Probe", changelog)
    append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run350B Softmax Output Shape Conversion Probe", changelog)


def write_registers(final: Mapping[str, Any]) -> None:
    write_bom_text(
        WORKSPACE_STATE,
        "\n".join(
            [
                f"current_stage_id: {STAGE_ID}",
                f"current_run_id: {final['next_run_id']}",
                f"latest_completed_run_id: {RUN_ID}",
                f"current_status: {final['status']}",
                f"current_judgment: {final['judgment']}",
                f"current_decision: {final['decision']}",
                f"next_run_id: {final['next_run_id']}",
                f"claim_boundary: {CLAIM_BOUNDARY}",
                f"updated_at: {TODAY}",
                "",
            ]
        ),
    )
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "result_judgment": final["result_judgment"],
        "decision": final["decision"],
        "next_run_id": final["next_run_id"],
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_count": final["attempt_rows"],
        "runtime_completed_rows": final["runtime_completed_rows"],
        "best_net_profit": final["best_net_profit"],
        "best_profit_factor": final["best_profit_factor"],
        "trade_count": final["best_trade_count"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    ledger_base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "status": final["status"],
        "judgment": final["judgment"],
        "result_judgment": final["result_judgment"],
        "net_profit": final["best_net_profit"],
        "profit_factor": final["best_profit_factor"],
        "expectancy": final["best_expectancy"],
        "trade_count": final["best_trade_count"],
        "trade_density_per_feature_day": final["best_trade_density_per_feature_day"],
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at": TODAY,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "next_run_id": final["next_run_id"],
    }
    ledger_rows = [
        {
            **ledger_base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A used(Tier A 사용)",
            "record_view": "Tier A used(Tier A 사용)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "runtime_interop_probe",
            "kpi_scope": "MT5 Strategy Tester report(MT5 전략 테스터 보고서)",
            "primary_kpi": f"net_profit={final['best_net_profit']};pf={final['best_profit_factor']};trades={final['best_trade_count']}",
            "guardrail_kpi": TRADE_DENSITY_TARGET,
        },
        {
            **ledger_base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B fallback used(Tier B 대체 사용)",
            "record_view": "Tier B fallback used(Tier B 대체 사용)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "net_profit": "",
            "profit_factor": "",
            "expectancy": "",
            "trade_count": "",
            "trade_density_per_feature_day": "",
            "result_status": "missing_required(필수 누락)",
        },
        {
            **ledger_base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows)


def update_artifact_registry() -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": path.suffix.lstrip(".") or "artifact",
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha256_file(path) if path.is_file() else "",
                    "created_at": TODAY,
                    "created_at_utc": now_utc(),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def validate(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    missing = [
        rel(path)
        for path in [FINAL_DECISION, RUN_MANIFEST, GATE_AUDIT, REPORT_PATH, SUMMARY_CSV, EXPECTED_TAPE, VARIANT_PACKAGE]
        if not exists(path)
    ]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    failed = [gate["gate_id"] for gate in gates if gate.get("status") != "passed"]
    if failed and not str(final.get("status", "")).startswith("blocked_"):
        raise RuntimeError("required gate audit failed(필수 게이트 감사 실패): " + ", ".join(failed))
    if final.get("goal_achieve") != "not_claimed":
        raise RuntimeError("forbidden goal claim(금지된 목표 주장)")


def main() -> None:
    for directory in [RUN_DIR, MODEL_DIR, MT5_DIR, SET_DIR, INI_DIR, TELEMETRY_COPY_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    for path in INPUT_FILES:
        required(path)
    args = parse_args()
    feature_order = run349e.load_feature_order()
    frame = load_research_frame(feature_order)
    x_all = frame.loc[:, list(feature_order)].to_numpy(dtype=np.float32, copy=True)
    variants, probability_by_attempt = materialize_onnx_variants(len(feature_order), x_all)
    screen_rows = screen_thresholds(frame, variants, probability_by_attempt)
    selected = select_thresholds(variants, screen_rows, Path(args.common_files_root))
    write_expected_tape(frame, selected, probability_by_attempt)
    attempts = materialize_mt5_files(selected)
    execution_results, report_records, copy_rows = execute_attempts(args, attempts)
    summary_rows, diff_rows = compare_outputs(attempts, execution_results, report_records)
    write_runtime_identity(args, attempts)
    final_seed = build_final(args, attempts, summary_rows, diff_rows, copy_rows)
    write_receipts(final_seed, attempts)
    write_csv(NEXT_ACTION_QUEUE, [{"queue_id": final_seed["next_run_id"], "stage_id": STAGE_ID, "source_run_id": RUN_ID, "priority": 1, "action": "continue_stage350_runtime_repair", "effect": "Use Stage350B attribution to repair ONNX runtime path.", "claim_boundary": CLAIM_BOUNDARY}])
    gates = make_gates(final_seed)
    write_csv(GATE_AUDIT, gates)
    write_final_manifest(final_seed, gates, attempts)
    final = read_json(FINAL_DECISION)
    write_docs(final)
    write_registers(final)
    update_artifact_registry()
    gates = make_gates(final)
    write_csv(GATE_AUDIT, gates)
    write_final_manifest(final, gates, attempts)
    final = read_json(FINAL_DECISION)
    write_docs(final)
    write_registers(final)
    update_artifact_registry()
    validate(final, gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "result_judgment": final["result_judgment"],
                "attempts": final["attempt_rows"],
                "runtime_completed_rows": final["runtime_completed_rows"],
                "probability_parity_pass_rows": final["probability_parity_pass_rows"],
                "canary_passed": final["canary_passed"],
                "best_attempt_name": final["best_attempt_name"],
                "best_attribution": final["best_attribution"],
                "best_net_profit": final["best_net_profit"],
                "best_profit_factor": final["best_profit_factor"],
                "best_trade_count": final["best_trade_count"],
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "goal_achieve": final["goal_achieve"],
                "next_run_id": final["next_run_id"],
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
