from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import onnx
import onnxruntime as ort
import pandas as pd
from onnx import TensorProto, helper, numpy_helper
from sklearn.linear_model import LogisticRegression


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage348 import (  # noqa: E402
    materialize_onnx_deployable_short_carry_probe_package_without_db as source_pkg,
)
from stage_pipelines.stage350 import (  # noqa: E402
    probe_no_scaler_table_runtime_handoff_without_db as run350e,
)


TODAY = "2026-06-01"
STAGE_ID = "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
RUN_NUMBER = "run351B"
RUN_ID = "run351B_rebuild_no_scaler_or_1d_scaler_onnx_trade_surface_without_db_v1"
PARENT_RUN_ID = "run351A_branch_stage350_to_no_scaler_or_1d_scaler_trade_surface_without_db_v1"
SOURCE_RUNTIME_REPAIR_RUN_ID = run350e.RUN_ID
NEXT_RUN_ID = "run351C_execute_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db_v1"

STATUS_READY = "completed_stage351B_no_scaler_1d_onnx_trade_surface_proxy_package_ready_no_selection"
STATUS_WEAK = "completed_stage351B_no_scaler_1d_onnx_trade_surface_proxy_weak_package_ready_no_selection"
STATUS_BLOCKED = "blocked_stage351B_no_scaler_1d_onnx_trade_surface_compile_or_package_blocked_no_selection"
CLAIM_BOUNDARY = (
    "research_development_proxy_trade_surface_and_runtime_handoff_package_only_"
    "mt5_probe_required_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

TRAINING_DATASET = (
    ROOT
    / "data"
    / "processed"
    / "training_datasets"
    / "label_v1_fwd12_split_v1_proxyw58"
    / "training_dataset.parquet"
)
TRAINING_SUMMARY = TRAINING_DATASET.parent / "training_dataset_summary.json"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
FEATURE_DIR = RUN_DIR / "features"
MODEL_DIR = RUN_DIR / "models"
EXPECTED_DIR = RUN_DIR / "expected"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

REPORT_PATH = REVIEW_DIR / "run351B_no_scaler_1d_onnx_trade_surface.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage351B_no_scaler_1d_onnx_trade_surface.md"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

FEATURE_MATRIX = FEATURE_DIR / "runtime_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "feature_matrix_manifest.csv"
FEATURE_ORDER_CONTRACT = RUN_DIR / "feature_order_contract.csv"
MODEL_TRAINING_SCORECARD = RUN_DIR / "model_training_scorecard.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
PYTHON_ONNX_SANITY = RUN_DIR / "python_onnx_sanity.csv"
PROXY_THRESHOLD_SCREEN = RUN_DIR / "proxy_threshold_screen.csv"
PROXY_SELECTION_QUEUE = RUN_DIR / "probe_priority_queue.csv"
SESSION_STABILITY = RUN_DIR / "session_regime_stability.csv"
EXPECTED_TAPE = EXPECTED_DIR / "expected_tape.csv"
EXPECTED_TAPE_INDEX = EXPECTED_DIR / "expected_tape_index.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
EA_SYNC_MANIFEST = RUN_DIR / "ea_compile_and_sync_manifest.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

COMMON_ROOT = "Project_Obsidian_Prime_v2/stage351/run351B_no_scaler_1d_trade_surface"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage351_ONNXTradeSurface__NoScalerOr1DScaler"
FEATURE_ORDER = list(source_pkg.CONTRACT_58_FEATURES)
FEATURE_ORDER_HASH = source_pkg.ordered_hash(FEATURE_ORDER)
MAGIC_BASE = 3512000
HOLD_BARS = 12
BASE_COST_LOG_RETURN = 0.00015
STRESS_COST_LOG_RETURN = 0.00030
TRADE_DENSITY_MIN = 3.0
TRADE_DENSITY_TARGET = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

INPUT_FILES = (
    TRAINING_DATASET,
    TRAINING_SUMMARY,
    STAGE_DIR / "02_runs" / "run351A" / "final_decision.json",
    STAGE_DIR / "02_runs" / "run351A" / "required_gate_coverage_audit.csv",
    STAGE_DIR / "02_runs" / "run351A" / "run351B_trade_surface_rebuild_queue.csv",
    ROOT / mt5.EA_SOURCE_PATH,
)

OUTPUT_FILES = (
    FEATURE_MATRIX,
    FEATURE_MATRIX_MANIFEST,
    FEATURE_ORDER_CONTRACT,
    MODEL_TRAINING_SCORECARD,
    MODEL_HANDOFF_MANIFEST,
    PYTHON_ONNX_SANITY,
    PROXY_THRESHOLD_SCREEN,
    PROXY_SELECTION_QUEUE,
    SESSION_STABILITY,
    EXPECTED_TAPE,
    EXPECTED_TAPE_INDEX,
    COMMON_FILES_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    EA_SYNC_MANIFEST,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    ROOT_SELECTION_STATUS,
    STAGE_LEDGER,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)

fs_path = source_pkg.fs_path
exists = source_pkg.exists
required = source_pkg.required
ensure_parent = source_pkg.ensure_parent
rel = source_pkg.rel
sha256_file = source_pkg.sha256_file
write_json = source_pkg.write_json
read_json = source_pkg.read_json
write_csv = source_pkg.write_csv
read_csv_rows = source_pkg.read_csv_rows
write_bom_text = source_pkg.write_bom_text
append_or_replace_csv = source_pkg.append_or_replace_csv
append_text_once = source_pkg.append_text_once


@dataclass(frozen=True)
class ModelVariant:
    model_variant_id: str
    graph_family: str
    runtime_contract: str
    c_value: float
    class_weight: str
    sample_weight_profile: str
    use_matrix_tensor: bool = True


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage351B no-scaler or 1D-scaler ONNX trade surface rebuild.")
    parser.add_argument("--common-files-root", default=str(source_pkg.DEFAULT_COMMON_FILES))
    parser.add_argument("--terminal-data-root", default=str(source_pkg.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--metaeditor-path", default=str(source_pkg.DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"))
    parser.add_argument("--max-surfaces", type=int, default=6)
    parser.add_argument("--skip-compile", action="store_true")
    return parser.parse_args()


def stable_softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits, axis=1, keepdims=True)
    exps = np.exp(shifted)
    return (exps / np.sum(exps, axis=1, keepdims=True)).astype(np.float32)


def load_training_frame() -> tuple[pd.DataFrame, dict[str, Any]]:
    required(TRAINING_DATASET)
    required(TRAINING_SUMMARY)
    frame = pd.read_parquet(fs_path(TRAINING_DATASET)).copy()
    summary = read_json(TRAINING_SUMMARY)
    missing = [name for name in FEATURE_ORDER if name not in frame.columns]
    if missing:
        raise RuntimeError("training_dataset missing feature columns: " + ", ".join(missing))
    if str(summary.get("feature_order_hash")) != FEATURE_ORDER_HASH:
        raise RuntimeError(
            f"feature_order_hash mismatch: summary={summary.get('feature_order_hash')} contract={FEATURE_ORDER_HASH}"
        )
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    for name in FEATURE_ORDER:
        frame[name] = pd.to_numeric(frame[name], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)
    frame["label_class"] = pd.to_numeric(frame["label_class"], errors="raise").astype(int)
    frame["future_log_return_12"] = pd.to_numeric(frame["future_log_return_12"], errors="raise").astype(float)
    frame["minutes_from_cash_open"] = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce").fillna(9999.0)
    frame["split"] = frame["split"].astype(str)
    if frame["timestamp"].duplicated().any():
        duplicate_count = int(frame["timestamp"].duplicated().sum())
        raise RuntimeError(f"duplicate timestamp rows in training frame: {duplicate_count}")
    return frame, summary


def materialize_feature_matrix(frame: pd.DataFrame, common_files_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    payload = pd.DataFrame(
        {
            "bar_time_server": timestamps.dt.strftime("%Y.%m.%d %H:%M:%S"),
            "timestamp_utc": timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "split": frame["split"].astype(str).to_numpy(),
            "row_index": np.arange(len(frame), dtype="int64"),
        }
    )
    feature_payload = frame.loc[:, FEATURE_ORDER].astype("float32").reset_index(drop=True)
    payload = pd.concat([payload, feature_payload], axis=1)
    ensure_parent(FEATURE_MATRIX)
    payload.to_csv(fs_path(FEATURE_MATRIX), index=False, encoding="utf-8", float_format="%.10g")

    common_path = f"{COMMON_FEATURE_DIR}/runtime_features.csv"
    common_abs = common_files_root / Path(common_path)
    ensure_parent(common_abs)
    shutil.copy2(fs_path(FEATURE_MATRIX), fs_path(common_abs))
    split_counts = frame["split"].value_counts().to_dict()
    manifest = {
        "path": rel(FEATURE_MATRIX),
        "common_path": common_path,
        "common_absolute_path": common_abs.as_posix(),
        "sha256": sha256_file(FEATURE_MATRIX),
        "common_sha256": sha256_file(common_abs),
        "rows": int(len(frame)),
        "feature_count": len(FEATURE_ORDER),
        "feature_order_hash": FEATURE_ORDER_HASH,
        "first_timestamp": timestamps.iloc[0].isoformat(),
        "last_timestamp": timestamps.iloc[-1].isoformat(),
        "split_counts": split_counts,
        "timestamp_meaning": "broker_clock_alignment_key_written_as_bar_time_server_for_mt5_match",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(FEATURE_MATRIX_MANIFEST, [manifest])
    sync_rows = [
        {
            "sync_id": "common_feature_matrix",
            "source_path": rel(FEATURE_MATRIX),
            "target_path": common_abs.as_posix(),
            "common_path": common_path,
            "exists": exists(common_abs),
            "sha256": sha256_file(common_abs),
            "effect": "feature_matrix_copied_to_common_files_for_mt5_probe",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return manifest, sync_rows


def feature_input_hash_by_time() -> dict[str, str]:
    def fnv1a64_upper(line: str) -> str:
        value = 1469598103934665603
        for char in line:
            value = ((value ^ ord(char)) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
        return f"{value:X}"

    with open(fs_path(FEATURE_MATRIX), encoding="utf-8-sig", newline="") as handle:
        header = handle.readline().rstrip("\r\n")
        columns = header.split(",")
        time_idx = columns.index("bar_time_server")
        output: dict[str, str] = {}
        for raw in handle:
            line = raw.rstrip("\r\n")
            parts = line.split(",")
            if len(parts) <= time_idx:
                continue
            output[parts[time_idx]] = fnv1a64_upper(line)
    return output


def write_feature_order_contract(summary: Mapping[str, Any]) -> None:
    rows = []
    for index, feature in enumerate(FEATURE_ORDER):
        rows.append(
            {
                "feature_index": index,
                "feature_name": feature,
                "feature_order_hash": FEATURE_ORDER_HASH,
                "source_summary_hash": summary.get("feature_order_hash", ""),
                "runtime_feature_count": len(FEATURE_ORDER),
                "status": "active",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(FEATURE_ORDER_CONTRACT, rows)


def variant_definitions() -> list[ModelVariant]:
    return [
        ModelVariant("b00_1d_logreg_balanced_c030", "1d_scaler_softmax", "sub_div_matmul_add_softmax_1d", 0.30, "balanced", "none"),
        ModelVariant("b01_1d_logreg_balanced_c100", "1d_scaler_softmax", "sub_div_matmul_add_softmax_1d", 1.00, "balanced", "none"),
        ModelVariant("b02_1d_logreg_directional_c050", "1d_scaler_softmax", "sub_div_matmul_add_softmax_1d", 0.50, "directional", "none"),
        ModelVariant("b03_1d_logreg_cashopen_c050", "1d_scaler_softmax", "sub_div_matmul_add_softmax_1d", 0.50, "balanced", "cashopen_emphasis"),
        ModelVariant("b04_no_scaler_folded_balanced_c050", "no_scaler_folded_softmax", "matmul_add_softmax_folded_scaler", 0.50, "balanced", "none"),
        ModelVariant("b05_no_scaler_folded_directional_c030", "no_scaler_folded_softmax", "matmul_add_softmax_folded_scaler", 0.30, "directional", "none"),
    ]


def class_weight_payload(name: str) -> str | dict[int, float]:
    if name == "balanced":
        return "balanced"
    if name == "directional":
        return {0: 1.20, 1: 0.80, 2: 1.20}
    raise ValueError(f"unknown class_weight profile: {name}")


def sample_weight_array(frame: pd.DataFrame, profile: str) -> np.ndarray | None:
    if profile == "none":
        return None
    weights = np.ones(len(frame), dtype=np.float64)
    if profile == "cashopen_emphasis":
        minutes = frame["minutes_from_cash_open"].to_numpy(dtype=float)
        weights[(minutes >= 0.0) & (minutes <= 90.0)] *= 1.40
        weights[(minutes >= 300.0)] *= 1.15
        return weights
    raise ValueError(f"unknown sample_weight profile: {profile}")


def train_variants(frame: pd.DataFrame) -> tuple[list[dict[str, Any]], dict[str, np.ndarray], list[dict[str, Any]]]:
    x_all = frame.loc[:, FEATURE_ORDER].to_numpy(dtype=np.float32, copy=True)
    split = frame["split"].to_numpy(dtype=str)
    train_mask = split == "train"
    x_train = x_all[train_mask].astype(np.float64)
    y_train = frame.loc[train_mask, "label_class"].to_numpy(dtype=int)
    mean = x_train.mean(axis=0).astype(np.float32)
    scale = x_train.std(axis=0).astype(np.float32)
    scale[scale < 1.0e-6] = 1.0
    x_scaled_all = ((x_all.astype(np.float32) - mean.reshape(1, -1)) / scale.reshape(1, -1)).astype(np.float32)
    x_scaled_train = x_scaled_all[train_mask].astype(np.float64)

    model_rows: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    probability_by_variant: dict[str, np.ndarray] = {}

    for spec in variant_definitions():
        train_frame = frame.loc[train_mask].reset_index(drop=True)
        weights = sample_weight_array(train_frame, spec.sample_weight_profile)
        clf = LogisticRegression(
            C=spec.c_value,
            class_weight=class_weight_payload(spec.class_weight),
            max_iter=2000,
            solver="lbfgs",
        )
        clf.fit(x_scaled_train, y_train, sample_weight=weights)
        if list(clf.classes_) != [0, 1, 2]:
            raise RuntimeError(f"unexpected class order for {spec.model_variant_id}: {list(clf.classes_)}")
        coef = clf.coef_.astype(np.float32)
        intercept = clf.intercept_.astype(np.float32)
        if spec.graph_family == "1d_scaler_softmax":
            onnx_weights = coef.T.astype(np.float32)
            onnx_bias = intercept.astype(np.float32)
            probs = stable_softmax(x_scaled_all @ onnx_weights + onnx_bias.reshape(1, -1))
            model_path = MODEL_DIR / f"{spec.model_variant_id}.onnx"
            build_softmax_onnx(model_path, onnx_weights, onnx_bias, mean=mean, scale=scale, graph_name=spec.model_variant_id)
        elif spec.graph_family == "no_scaler_folded_softmax":
            folded_weights = (coef / scale.reshape(1, -1)).T.astype(np.float32)
            folded_bias = (
                intercept.astype(np.float64)
                - np.sum((mean.astype(np.float64) / scale.astype(np.float64)).reshape(1, -1) * coef.astype(np.float64), axis=1)
            ).astype(np.float32)
            probs = stable_softmax(x_all @ folded_weights + folded_bias.reshape(1, -1))
            model_path = MODEL_DIR / f"{spec.model_variant_id}.onnx"
            build_softmax_onnx(model_path, folded_weights, folded_bias, mean=None, scale=None, graph_name=spec.model_variant_id)
        else:
            raise ValueError(f"unsupported graph family: {spec.graph_family}")

        probability_by_variant[spec.model_variant_id] = probs
        row_sums = probs.sum(axis=1)
        sanity = onnx_sanity(model_path, x_all, probs)
        model_rows.append(
            {
                "model_variant_id": spec.model_variant_id,
                "graph_family": spec.graph_family,
                "runtime_contract": spec.runtime_contract,
                "model_path": rel(model_path),
                "model_sha256": sha256_file(model_path),
                "feature_count": len(FEATURE_ORDER),
                "feature_order_hash": FEATURE_ORDER_HASH,
                "c_value": spec.c_value,
                "class_weight": spec.class_weight,
                "sample_weight_profile": spec.sample_weight_profile,
                "output_order": "[p_short,p_flat,p_long]",
                "python_output_min": float(np.min(probs)),
                "python_output_max": float(np.max(probs)),
                "python_row_sum_min": float(np.min(row_sums)),
                "python_row_sum_max": float(np.max(row_sums)),
                "onnx_sanity_max_abs_diff": sanity["max_abs_diff"],
                "onnx_sanity_rows": sanity["rows"],
                "use_matrix_tensor": spec.use_matrix_tensor,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for split_name in ["train", "validation", "oos"]:
            mask = split == split_name
            pred = np.argmax(probs[mask], axis=1)
            actual = frame.loc[mask, "label_class"].to_numpy(dtype=int)
            score_rows.append(
                {
                    "model_variant_id": spec.model_variant_id,
                    "split": split_name,
                    "rows": int(np.sum(mask)),
                    "argmax_accuracy": float(np.mean(pred == actual)),
                    "argmax_short_rows": int(np.sum(pred == 0)),
                    "argmax_flat_rows": int(np.sum(pred == 1)),
                    "argmax_long_rows": int(np.sum(pred == 2)),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    write_csv(MODEL_HANDOFF_MANIFEST, model_rows)
    write_csv(MODEL_TRAINING_SCORECARD, score_rows)
    return model_rows, probability_by_variant, score_rows


def build_softmax_onnx(
    path: Path,
    weights: np.ndarray,
    bias: np.ndarray,
    *,
    mean: np.ndarray | None,
    scale: np.ndarray | None,
    graph_name: str,
) -> None:
    feature_count = weights.shape[0]
    nodes = []
    initializers = []
    current = "float_input"
    if mean is not None and scale is not None:
        nodes.append(helper.make_node("Sub", ["float_input", "scaler_mean"], ["centered"], name="center_features_1d"))
        nodes.append(helper.make_node("Div", ["centered", "scaler_scale"], ["scaled"], name="scale_features_1d"))
        initializers.append(numpy_helper.from_array(mean.astype(np.float32).reshape(-1), name="scaler_mean"))
        initializers.append(numpy_helper.from_array(scale.astype(np.float32).reshape(-1), name="scaler_scale"))
        current = "scaled"
    nodes.extend(
        [
            helper.make_node("MatMul", [current, "W"], ["linear_out"], name="linear_matmul"),
            helper.make_node("Add", ["linear_out", "B"], ["logits"], name="linear_bias"),
            helper.make_node("Softmax", ["logits"], ["probabilities"], name="probability_softmax", axis=1),
        ]
    )
    initializers.append(numpy_helper.from_array(weights.astype(np.float32), name="W"))
    initializers.append(numpy_helper.from_array(bias.astype(np.float32).reshape(-1), name="B"))
    input_info = helper.make_tensor_value_info("float_input", TensorProto.FLOAT, [1, feature_count])
    output_info = helper.make_tensor_value_info("probabilities", TensorProto.FLOAT, [1, 3])
    graph = helper.make_graph(nodes, graph_name, [input_info], [output_info], initializer=initializers)
    model = helper.make_model(graph)
    model.ir_version = 7
    del model.opset_import[:]
    model.opset_import.extend([helper.make_operatorsetid("", 12)])
    onnx.checker.check_model(model)
    ensure_parent(path)
    with open(fs_path(path), "wb") as handle:
        handle.write(model.SerializeToString())


def onnx_sanity(path: Path, x_all: np.ndarray, expected: np.ndarray) -> dict[str, Any]:
    if len(x_all) == 0:
        return {"rows": 0, "max_abs_diff": 0.0}
    sample_indices = np.unique(np.linspace(0, len(x_all) - 1, num=min(512, len(x_all)), dtype=int))
    session = ort.InferenceSession(fs_path(path), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = []
    for index in sample_indices:
        row = x_all[index : index + 1].astype(np.float32)
        output = session.run(None, {input_name: row})[0].reshape(1, 3)
        outputs.append(output.astype(np.float32))
    observed = np.vstack(outputs)
    wanted = expected[sample_indices].astype(np.float32)
    max_abs_diff = float(np.max(np.abs(observed - wanted))) if len(observed) else 0.0
    return {"rows": int(len(sample_indices)), "max_abs_diff": max_abs_diff}


def decision_labels(
    probs: np.ndarray,
    short_threshold: float,
    long_threshold: float,
    min_margin: float,
    minutes: np.ndarray,
    side_policy: str,
) -> np.ndarray:
    p_short = probs[:, 0]
    p_flat = probs[:, 1]
    p_long = probs[:, 2]
    short_margin = p_short - np.maximum(p_flat, p_long)
    long_margin = p_long - np.maximum(p_flat, p_short)
    short_ok = (p_short >= short_threshold) & (short_margin >= min_margin)
    long_ok = (p_long >= long_threshold) & (long_margin >= min_margin)
    labels = np.ones(len(probs), dtype=np.int8)
    long_take = long_ok & ((~short_ok) | (p_long >= p_short))
    short_take = short_ok & (~long_take)
    labels[long_take] = 2
    labels[short_take] = 0
    if side_policy == "block_early_longs_60m":
        labels[(labels == 2) & (minutes >= 0.0) & (minutes <= 60.0)] = 1
    elif side_policy != "none":
        raise ValueError(f"unsupported side policy: {side_policy}")
    return labels


def trade_returns_nonoverlap(labels: np.ndarray, future_returns: np.ndarray, dates: np.ndarray) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    next_allowed = 0
    for index, label in enumerate(labels):
        if index < next_allowed or label == 1:
            continue
        side = "short" if int(label) == 0 else "long"
        gross = -float(future_returns[index]) if side == "short" else float(future_returns[index])
        rows.append({"local_index": index, "side": side, "gross_log_return": gross, "date": str(dates[index])})
        next_allowed = index + HOLD_BARS
    return pd.DataFrame(rows)


def kpi_from_trades(trades: pd.DataFrame, day_count: int, *, cost: float) -> dict[str, Any]:
    if trades.empty:
        return {
            "trade_count": 0,
            "long_count": 0,
            "short_count": 0,
            "trade_per_day": 0.0,
            "net_log_return": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
            "win_rate": 0.0,
            "max_drawdown": 0.0,
            "recovery_factor": 0.0,
            "long_short_balance": 0.0,
            "positive_day_ratio": 0.0,
            "equity_r2": 0.0,
        }
    net = trades["gross_log_return"].to_numpy(dtype=float) - cost
    gains = net[net > 0.0].sum()
    losses = net[net < 0.0].sum()
    if losses < 0.0:
        pf = float(gains / abs(losses))
    elif gains > 0.0:
        pf = 999.0
    else:
        pf = 0.0
    equity = np.cumsum(net)
    peak = np.maximum.accumulate(np.insert(equity, 0, 0.0))[1:]
    drawdown = equity - peak
    max_dd = abs(float(np.min(drawdown))) if len(drawdown) else 0.0
    net_total = float(np.sum(net))
    recovery = net_total / max_dd if max_dd > 0.0 else (999.0 if net_total > 0.0 else 0.0)
    long_count = int((trades["side"] == "long").sum())
    short_count = int((trades["side"] == "short").sum())
    balance = min(long_count, short_count) / max(1, max(long_count, short_count))
    per_day = trades.assign(net=net).groupby("date")["net"].sum()
    positive_day_ratio = float((per_day > 0.0).mean()) if len(per_day) else 0.0
    if len(equity) >= 3:
        x = np.arange(len(equity), dtype=float)
        corr = np.corrcoef(x, equity)[0, 1]
        equity_r2 = float(corr * corr) if math.isfinite(corr) else 0.0
    else:
        equity_r2 = 0.0
    return {
        "trade_count": int(len(trades)),
        "long_count": long_count,
        "short_count": short_count,
        "trade_per_day": float(len(trades) / max(1, day_count)),
        "net_log_return": net_total,
        "profit_factor": min(pf, 999.0),
        "expectancy": float(np.mean(net)),
        "win_rate": float(np.mean(net > 0.0)),
        "max_drawdown": max_dd,
        "recovery_factor": min(recovery, 999.0),
        "long_short_balance": float(balance),
        "positive_day_ratio": positive_day_ratio,
        "equity_r2": equity_r2,
    }


def selection_score(kpi: Mapping[str, Any], stress: Mapping[str, Any]) -> float:
    trade_per_day = float(kpi["trade_per_day"])
    density_bonus = max(0.0, 8.0 - abs(trade_per_day - 5.0))
    pf = float(kpi["profit_factor"])
    return (
        float(kpi["net_log_return"]) * 10000.0
        + math.log1p(max(0.0, min(pf, 20.0))) * 35.0
        + float(kpi["recovery_factor"]) * 8.0
        + float(kpi["long_short_balance"]) * 25.0
        + float(kpi["positive_day_ratio"]) * 18.0
        + density_bonus * 3.0
        - float(kpi["max_drawdown"]) * 8500.0
        + float(stress["net_log_return"]) * 2500.0
    )


def threshold_grid(probs: np.ndarray, train_mask: np.ndarray) -> tuple[list[float], list[float], list[float]]:
    quantiles = [0.35, 0.45, 0.55, 0.65, 0.75, 0.85]
    short_thresholds = sorted({float(np.quantile(probs[train_mask, 0], q)) for q in quantiles})
    long_thresholds = sorted({float(np.quantile(probs[train_mask, 2], q)) for q in quantiles})
    margins = [0.0, 0.01, 0.02, 0.04]
    return short_thresholds, long_thresholds, margins


def screen_thresholds(frame: pd.DataFrame, probability_by_variant: Mapping[str, np.ndarray]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    stability_rows: list[dict[str, Any]] = []
    split_values = frame["split"].to_numpy(dtype=str)
    train_mask = split_values == "train"
    future_returns = frame["future_log_return_12"].to_numpy(dtype=float)
    minutes = frame["minutes_from_cash_open"].to_numpy(dtype=float)
    dates = pd.to_datetime(frame["timestamp"], utc=True).dt.date.astype(str).to_numpy()
    split_day_counts = {
        split: int(pd.Series(dates[split_values == split]).nunique())
        for split in ["train", "validation", "oos"]
    }
    side_policies = ["none", "block_early_longs_60m"]

    for model_variant_id, probs in probability_by_variant.items():
        short_thresholds, long_thresholds, margins = threshold_grid(probs, train_mask)
        for side_policy in side_policies:
            for short_threshold in short_thresholds:
                for long_threshold in long_thresholds:
                    for min_margin in margins:
                        surface_id = (
                            f"{model_variant_id}__{side_policy}__s{short_threshold:.4f}"
                            f"__l{long_threshold:.4f}__m{min_margin:.3f}"
                        )
                        labels = decision_labels(probs, short_threshold, long_threshold, min_margin, minutes, side_policy)
                        split_kpis: dict[str, dict[str, Any]] = {}
                        split_trades: dict[str, pd.DataFrame] = {}
                        for split_name in ["train", "validation", "oos"]:
                            mask = split_values == split_name
                            trades = trade_returns_nonoverlap(labels[mask], future_returns[mask], dates[mask])
                            base_kpi = kpi_from_trades(trades, split_day_counts[split_name], cost=BASE_COST_LOG_RETURN)
                            stress_kpi = kpi_from_trades(trades, split_day_counts[split_name], cost=STRESS_COST_LOG_RETURN)
                            split_kpis[split_name] = base_kpi
                            split_trades[split_name] = trades
                            rows.append(
                                {
                                    "surface_id": surface_id,
                                    "model_variant_id": model_variant_id,
                                    "side_policy": side_policy,
                                    "split": split_name,
                                    "short_threshold": short_threshold,
                                    "long_threshold": long_threshold,
                                    "min_margin": min_margin,
                                    **{f"base_{key}": value for key, value in base_kpi.items()},
                                    **{f"stress_{key}": value for key, value in stress_kpi.items()},
                                    "selection_split": "validation",
                                    "selection_score": selection_score(base_kpi, stress_kpi) if split_name == "validation" else "",
                                    "allowed_use": "proxy_scout_and_mt5_probe_prioritization_only",
                                    "forbidden_use": "mt5_kpi_substitute_or_operating_claim",
                                    "claim_boundary": CLAIM_BOUNDARY,
                                }
                            )
                        selected_like = split_kpis["validation"]["trade_count"] > 0
                        if selected_like:
                            for split_name, trades in split_trades.items():
                                if trades.empty:
                                    continue
                                split_frame = frame.loc[split_values == split_name].reset_index(drop=True)
                                bucket = pd.cut(
                                    split_frame.loc[trades["local_index"].to_numpy(dtype=int), "minutes_from_cash_open"],
                                    bins=[-1, 60, 180, 330, 99999],
                                    labels=["early_0_60", "mid_60_180", "late_180_330", "tail_330_plus"],
                                )
                                bucket_frame = trades.assign(bucket=bucket.astype(str).to_numpy())
                                for bucket_name, bucket_trades in bucket_frame.groupby("bucket"):
                                    bucket_kpi = kpi_from_trades(bucket_trades, max(1, split_day_counts[split_name]), cost=BASE_COST_LOG_RETURN)
                                    stability_rows.append(
                                        {
                                            "surface_id": surface_id,
                                            "model_variant_id": model_variant_id,
                                            "side_policy": side_policy,
                                            "split": split_name,
                                            "session_bucket": bucket_name,
                                            **bucket_kpi,
                                            "claim_boundary": CLAIM_BOUNDARY,
                                        }
                                    )

    write_csv(PROXY_THRESHOLD_SCREEN, rows)
    write_csv(SESSION_STABILITY, stability_rows)
    selected = select_surfaces(rows)
    return rows, selected, stability_rows


def select_surfaces(screen_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    validation_rows = [
        dict(row)
        for row in screen_rows
        if row.get("split") == "validation" and int(float(row.get("base_trade_count", 0) or 0)) > 0
    ]
    eligible = [
        row
        for row in validation_rows
        if float(row.get("base_trade_per_day", 0) or 0) >= TRADE_DENSITY_MIN
        and float(row.get("base_profit_factor", 0) or 0) >= 1.02
        and float(row.get("base_net_log_return", 0) or 0) > 0.0
        and float(row.get("base_long_short_balance", 0) or 0) >= 0.10
        and float(row.get("stress_net_log_return", 0) or 0) > -0.02
    ]
    if not eligible:
        eligible = [
            row
            for row in validation_rows
            if float(row.get("base_net_log_return", 0) or 0) > 0.0
            and float(row.get("base_trade_per_day", 0) or 0) >= 1.5
        ]
    if not eligible:
        eligible = validation_rows
    ranked = sorted(eligible, key=lambda row: float(row.get("selection_score", 0.0) or 0.0), reverse=True)
    fallback_ranked = sorted(
        validation_rows,
        key=lambda row: float(row.get("selection_score", 0.0) or 0.0),
        reverse=True,
    )
    selected: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for row_source in (ranked, fallback_ranked):
        for row in row_source:
            key = (str(row["model_variant_id"]), str(row["side_policy"]))
            if key in seen:
                continue
            seen.add(key)
            selected.append(row)
            if len(selected) >= 6:
                break
        if len(selected) >= 6:
            break
    for rank, row in enumerate(selected, start=1):
        row["priority_rank"] = rank
        row["next_action"] = NEXT_RUN_ID
        row["claim_boundary"] = CLAIM_BOUNDARY
    write_csv(PROXY_SELECTION_QUEUE, selected)
    return selected


def copy_models_to_common(
    model_rows: Sequence[Mapping[str, Any]],
    common_files_root: Path,
    sync_rows: list[dict[str, Any]],
) -> dict[str, str]:
    common_by_model: dict[str, str] = {}
    for row in model_rows:
        model_id = str(row["model_variant_id"])
        source = ROOT / str(row["model_path"])
        common_path = f"{COMMON_MODEL_DIR}/{model_id}.onnx"
        common_abs = common_files_root / Path(common_path)
        ensure_parent(common_abs)
        shutil.copy2(fs_path(source), fs_path(common_abs))
        common_by_model[model_id] = common_path
        sync_rows.append(
            {
                "sync_id": f"common_model::{model_id}",
                "source_path": rel(source),
                "target_path": common_abs.as_posix(),
                "common_path": common_path,
                "exists": exists(common_abs),
                "sha256": sha256_file(common_abs),
                "effect": "onnx_model_copied_to_common_files_for_mt5_probe",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(COMMON_FILES_SYNC, sync_rows)
    return common_by_model


def split_date_bounds(frame: pd.DataFrame) -> dict[str, tuple[str, str]]:
    output: dict[str, tuple[str, str]] = {}
    for split in ["validation", "oos"]:
        part = frame.loc[frame["split"].eq(split)]
        start = pd.to_datetime(part["timestamp"], utc=True).min().date()
        end = pd.to_datetime(part["timestamp"], utc=True).max().date() + timedelta(days=1)
        output[split] = (start.strftime("%Y.%m.%d"), end.strftime("%Y.%m.%d"))
    return output


def materialize_runtime_attempts(
    frame: pd.DataFrame,
    selected_surfaces: Sequence[Mapping[str, Any]],
    model_rows: Sequence[Mapping[str, Any]],
    common_by_model: Mapping[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    feature_common = f"{COMMON_FEATURE_DIR}/runtime_features.csv"
    model_by_id = {str(row["model_variant_id"]): row for row in model_rows}
    bounds = split_date_bounds(frame)
    set_rows: list[dict[str, Any]] = []
    ini_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    minutes_feature_index = FEATURE_ORDER.index("minutes_from_cash_open")
    for surface_rank, surface in enumerate(selected_surfaces, start=1):
        model_variant_id = str(surface["model_variant_id"])
        model_row = model_by_id[model_variant_id]
        side_policy = str(surface["side_policy"])
        side_filter = side_policy == "block_early_longs_60m"
        for split_offset, probe_split in enumerate(["validation", "oos"], start=0):
            from_date, to_date = bounds[probe_split]
            attempt_name = f"p{surface_rank:02d}_{model_variant_id}_{side_policy}_{probe_split}"
            model_common = common_by_model[model_variant_id]
            model_id = f"stage351B_{model_variant_id}_{side_policy}_rank{surface_rank:02d}"
            set_name = f"OPV2_{RUN_NUMBER}_{attempt_name}.set"
            ini_name = f"OPV2_{RUN_NUMBER}_{attempt_name}.ini"
            report_name = f"POPv2_{RUN_NUMBER}_{attempt_name}"
            set_path = SET_DIR / set_name
            ini_path = INI_DIR / ini_name
            telemetry_common = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv"
            summary_common = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv"
            set_values = {
                "InpRunId": f"{RUN_ID}_{attempt_name}",
                "InpExplorationLabel": EXPLORATION_LABEL,
                "InpTierLabel": "Tier A",
                "InpPrimaryActiveTier": "tier_a",
                "InpSplitLabel": f"{probe_split}_proxy_validation_selected_threshold",
                "InpMainSymbol": "US100",
                "InpTimeframe": 5,
                "InpEnforceM5": True,
                "InpFeatureCsvPath": feature_common,
                "InpFeatureCount": len(FEATURE_ORDER),
                "InpFeatureCsvUseCommonFiles": True,
                "InpFeatureRequireTimestampMatch": True,
                "InpFeatureAllowLatestFallback": False,
                "InpFeatureStrictHeader": True,
                "InpFeatureCsvDelimiter": ",",
                "InpCsvTimestampIsBarClose": True,
                "InpModelPath": model_common,
                "InpModelId": model_id,
                "InpModelBackend": "onnx",
                "InpModelUseCommonFiles": True,
                "InpModelUseCpuOnly": True,
                "InpModelNoConversion": True,
                "InpSetOutputShape": True,
                "InpModelUseMatrixTensor": bool(model_row.get("use_matrix_tensor", True)),
                "InpFeatureOrderHash": FEATURE_ORDER_HASH,
                "InpFallbackEnabled": False,
                "InpShortThreshold": float(surface["short_threshold"]),
                "InpLongThreshold": float(surface["long_threshold"]),
                "InpMinMargin": float(surface["min_margin"]),
                "InpDecisionMode": "threshold_margin",
                "InpInvertSignal": False,
                "InpSideFilterEnabled": side_filter,
                "InpSideFilterFeatureIndex": minutes_feature_index if side_filter else -1,
                "InpFallbackSideFilterFeatureIndex": minutes_feature_index if side_filter else -1,
                "InpBlockShortFeatureRange": False,
                "InpBlockShortFeatureMin": 0.0,
                "InpBlockShortFeatureMax": 0.0,
                "InpBlockLongFeatureRange": side_filter,
                "InpBlockLongFeatureMin": 0.0,
                "InpBlockLongFeatureMax": 60.0 if side_filter else 0.0,
                "InpAllowTrading": True,
                "InpFixedLot": 0.10,
                "InpMagic": MAGIC_BASE + (surface_rank * 10) + split_offset,
                "InpDeviationPoints": 20,
                "InpCloseOnFlatSignal": False,
                "InpReverseOnOppositeSignal": True,
                "InpCloseOnlyOnOppositeSignal": False,
                "InpMaxHoldBars": HOLD_BARS,
                "InpMaxConcurrentPositions": 1,
                "InpReentryCooldownBars": 0,
                "InpSameDirectionReentryCooldownBars": 0,
                "InpEntryTransitionOnly": False,
                "InpExitRiskOverlayEnabled": False,
                "InpAtrSltpEnabled": False,
                "InpModelRiskSizingEnabled": False,
                "InpTelemetryEnabled": True,
                "InpTelemetryUseCommonFiles": True,
                "InpTelemetryCsvPath": telemetry_common,
                "InpSummaryCsvPath": summary_common,
            }
            set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
            ini_payload = mt5.materialize_tester_ini_file(
                mt5.TesterMaterializationConfig(
                    shutdown_terminal=1,
                    from_date=from_date,
                    to_date=to_date,
                    report=report_name,
                ),
                ini_path,
                set_file_path=Path(set_name),
            )
            set_rows.append(
                {
                    "attempt_name": attempt_name,
                    "surface_id": surface["surface_id"],
                    "model_variant_id": model_variant_id,
                    "probe_split": probe_split,
                    "set_path": rel(set_path),
                    "set_sha256": set_payload["sha256"],
                    "parameter_count": set_payload["parameter_count"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            ini_rows.append(
                {
                    "attempt_name": attempt_name,
                    "surface_id": surface["surface_id"],
                    "model_variant_id": model_variant_id,
                    "probe_split": probe_split,
                    "ini_path": rel(ini_path),
                    "ini_sha256": ini_payload["sha256"],
                    "set_file": set_name,
                    "from_date": from_date,
                    "to_date": to_date,
                    "report_name": report_name,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            attempt_rows.append(
                {
                    "attempt_name": attempt_name,
                    "surface_id": surface["surface_id"],
                    "priority_rank": surface_rank,
                    "probe_split": probe_split,
                    "tier": "Tier A",
                    "split": probe_split,
                    "model_variant_id": model_variant_id,
                    "model_id": model_id,
                    "model_backend": "onnx",
                    "runtime_contract": model_row["runtime_contract"],
                    "graph_family": model_row["graph_family"],
                    "model_common_path": model_common,
                    "feature_csv_path": feature_common,
                    "feature_count": len(FEATURE_ORDER),
                    "feature_order_hash": FEATURE_ORDER_HASH,
                    "short_threshold": surface["short_threshold"],
                    "long_threshold": surface["long_threshold"],
                    "min_margin": surface["min_margin"],
                    "side_policy": side_policy,
                    "use_matrix_tensor": model_row.get("use_matrix_tensor", True),
                    "set_name": set_name,
                    "ini_name": ini_name,
                    "set_path": rel(set_path),
                    "ini_path": rel(ini_path),
                    "common_telemetry_path": telemetry_common,
                    "common_summary_path": summary_common,
                    "report_name": report_name,
                    "from_date": from_date,
                    "to_date": to_date,
                    "proxy_validation_trade_per_day": surface["base_trade_per_day"],
                    "proxy_validation_profit_factor": surface["base_profit_factor"],
                    "proxy_validation_net_log_return": surface["base_net_log_return"],
                    "allowed_use": "mt5_runtime_probe_execution",
                    "forbidden_use": "operating_claim_or_runtime_authority",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(TESTER_SET_MANIFEST, set_rows)
    write_csv(TESTER_INI_MANIFEST, ini_rows)
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, attempt_rows)
    return attempt_rows, set_rows, ini_rows


def label_name(label_id: int) -> str:
    return {0: "short", 1: "flat", 2: "long"}.get(int(label_id), "flat")


def write_expected_tape(
    frame: pd.DataFrame,
    selected_surfaces: Sequence[Mapping[str, Any]],
    probability_by_variant: Mapping[str, np.ndarray],
) -> None:
    feature_hashes = feature_input_hash_by_time()
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    bar_times = timestamps.dt.strftime("%Y.%m.%d %H:%M:%S").to_numpy()
    timestamp_utc = timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ").to_numpy()
    minutes = frame["minutes_from_cash_open"].to_numpy(dtype=float)
    future_returns = frame["future_log_return_12"].to_numpy(dtype=float)
    rows: list[dict[str, Any]] = []
    index_rows: list[dict[str, Any]] = []
    for surface in selected_surfaces:
        surface_id = str(surface["surface_id"])
        model_variant_id = str(surface["model_variant_id"])
        probs = probability_by_variant[model_variant_id]
        labels = decision_labels(
            probs,
            float(surface["short_threshold"]),
            float(surface["long_threshold"]),
            float(surface["min_margin"]),
            minutes,
            str(surface["side_policy"]),
        )
        for idx in range(len(frame)):
            label = label_name(int(labels[idx]))
            gross = 0.0
            if label == "short":
                gross = -float(future_returns[idx])
            elif label == "long":
                gross = float(future_returns[idx])
            rows.append(
                {
                    "surface_id": surface_id,
                    "model_variant_id": model_variant_id,
                    "bar_time_server": bar_times[idx],
                    "timestamp_utc": timestamp_utc[idx],
                    "split": frame.at[idx, "split"],
                    "row_index": idx,
                    "mt5_input_hash": feature_hashes.get(bar_times[idx], ""),
                    "p_short": float(probs[idx, 0]),
                    "p_flat": float(probs[idx, 1]),
                    "p_long": float(probs[idx, 2]),
                    "ea_mapped_expected_label": label,
                    "expected_class_id": int(labels[idx]),
                    "proxy_fixed_horizon_gross_log_return": gross,
                    "short_threshold": surface["short_threshold"],
                    "long_threshold": surface["long_threshold"],
                    "min_margin": surface["min_margin"],
                    "side_policy": surface["side_policy"],
                    "allowed_use": "proxy_vs_mt5_runtime_probe_comparison_only",
                    "forbidden_use": "mt5_kpi_substitute_or_operating_selection",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        surface_rows = pd.DataFrame([row for row in rows if row["surface_id"] == surface_id])
        for split_name in ["train", "validation", "oos", "all"]:
            part = surface_rows if split_name == "all" else surface_rows.loc[surface_rows["split"].eq(split_name)]
            counts = part["ea_mapped_expected_label"].value_counts().to_dict() if not part.empty else {}
            index_rows.append(
                {
                    "surface_id": surface_id,
                    "model_variant_id": model_variant_id,
                    "split": split_name,
                    "row_count": int(len(part)),
                    "expected_short_count": int(counts.get("short", 0)),
                    "expected_long_count": int(counts.get("long", 0)),
                    "expected_flat_count": int(counts.get("flat", 0)),
                    "path": rel(EXPECTED_TAPE),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(EXPECTED_TAPE, rows)
    for row in index_rows:
        row["expected_tape_sha256"] = sha256_file(EXPECTED_TAPE)
    write_csv(EXPECTED_TAPE_INDEX, index_rows)


def compile_and_sync_ea(metaeditor_path: Path, terminal_data_root: Path, *, skip_compile: bool) -> dict[str, Any]:
    source_dir = ROOT / "foundation" / "mt5"
    source_ea = ROOT / mt5.EA_SOURCE_PATH
    source_ex5 = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
    include_src = source_dir / "include"
    target_dir = terminal_data_root / "MQL5" / "Experts" / "Project_Obsidian_Prime_v2" / "foundation" / "mt5"
    compile_log = MT5_DIR / "run351B_metaeditor_compile.log"
    if skip_compile:
        compile_payload = {"status": "skipped", "reason": "skip_compile_argument"}
    else:
        compile_payload = mt5.compile_mql5_ea(metaeditor_path, source_ea, compile_log)
    sync_rows: list[dict[str, Any]] = []
    os.makedirs(fs_path(target_dir), exist_ok=True)
    for src, name in ((source_ea, "ea_source"), (source_ex5, "ea_binary")):
        dst = target_dir / src.name
        if exists(src):
            shutil.copy2(fs_path(src), fs_path(dst))
            sync_rows.append({"artifact": name, "source": rel(src), "target": dst.as_posix(), "status": "copied", "sha256": sha256_file(dst)})
        else:
            sync_rows.append({"artifact": name, "source": rel(src), "target": dst.as_posix(), "status": "missing_source"})
    include_dst = target_dir / "include"
    if exists(include_src):
        shutil.copytree(fs_path(include_src), fs_path(include_dst), dirs_exist_ok=True)
        sync_rows.append({"artifact": "ea_include_tree", "source": rel(include_src), "target": include_dst.as_posix(), "status": "copied"})
    payload = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": now_utc(),
        "compile": compile_payload,
        "sync_rows": sync_rows,
        "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(EA_SYNC_MANIFEST, payload)
    return payload


def build_final(
    *,
    selected_surfaces: Sequence[Mapping[str, Any]],
    attempt_rows: Sequence[Mapping[str, Any]],
    compile_payload: Mapping[str, Any],
    model_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    compile_status = str(compile_payload.get("compile", {}).get("status", "missing"))
    best = selected_surfaces[0] if selected_surfaces else {}
    best_trade_per_day = float(best.get("base_trade_per_day", 0.0) or 0.0)
    best_pf = float(best.get("base_profit_factor", 0.0) or 0.0)
    best_net = float(best.get("base_net_log_return", 0.0) or 0.0)
    positive_proxy = bool(best_net > 0.0 and best_pf >= 1.02 and best_trade_per_day >= TRADE_DENSITY_MIN)
    if compile_status not in {"completed", "skipped"} or not attempt_rows:
        status = STATUS_BLOCKED
        judgment = "blocked_package_or_compile_issue_runtime_probe_not_ready"
        result_judgment = "blocked"
        decision = "stage351B_repair_package_or_compile_then_retry"
        next_run = RUN_ID
    elif positive_proxy:
        status = STATUS_READY
        judgment = "exploratory_proxy_positive_runtime_handoff_ready_mt5_probe_required_no_selection"
        result_judgment = "exploratory_positive_proxy"
        decision = "stage351B_open_run351C_execute_mt5_probe"
        next_run = NEXT_RUN_ID
    else:
        status = STATUS_WEAK
        judgment = "exploratory_proxy_weak_runtime_handoff_ready_mt5_probe_required_before_interpretation"
        result_judgment = "inconclusive_proxy_weak"
        decision = "stage351B_open_run351C_execute_or_repair_mt5_probe"
        next_run = NEXT_RUN_ID
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_repair_run_id": SOURCE_RUNTIME_REPAIR_RUN_ID,
        "status": status,
        "judgment": judgment,
        "result_judgment": result_judgment,
        "decision": decision,
        "next_run_id": next_run,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "model_variants": len(model_rows),
        "selected_surfaces": len(selected_surfaces),
        "runtime_attempt_rows": len(attempt_rows),
        "best_surface_id": best.get("surface_id", ""),
        "best_model_variant_id": best.get("model_variant_id", ""),
        "best_validation_trade_per_day": best_trade_per_day,
        "best_validation_profit_factor": best_pf,
        "best_validation_net_log_return": best_net,
        "best_validation_recovery_factor": float(best.get("base_recovery_factor", 0.0) or 0.0),
        "best_validation_max_drawdown": float(best.get("base_max_drawdown", 0.0) or 0.0),
        "best_validation_long_short_balance": float(best.get("base_long_short_balance", 0.0) or 0.0),
        "best_stress_net_log_return": float(best.get("stress_net_log_return", 0.0) or 0.0),
        "compile_status": compile_status,
        "trade_density_requirement": TRADE_DENSITY_TARGET,
        "proxy_expected_value": "created_for_scout_only_mt5_runtime_probe_required",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "forward_passed": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def write_receipts(final: Mapping[str, Any], summary: Mapping[str, Any], model_rows: Sequence[Mapping[str, Any]]) -> None:
    base_payload = {"stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": now_utc(), "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base_payload,
            "idea_id": "stage351_no_scaler_or_1d_scaler_softmax_trade_surface",
            "hypothesis": "A no-scaler folded logistic or 1D-scaler logistic Softmax ONNX can create a tradable US100 M5 surface after Stage350E runtime contract repair.",
            "decision_use": "Prioritize MT5 runtime probe attempts; not candidate selection.",
            "comparison_baseline": "Stage350E passed no-scaler and 1D-scaler linear runtime parity but did not build a profitable trade surface.",
            "control_variables": "US100 M5 fwd12 label, 58-feature order, train/validation/oos split, output [p_short,p_flat,p_long], threshold_margin runtime decision.",
            "changed_variables": "logistic regularization, class weighting, sample weighting, no-scaler folded graph, 1D-scaler graph, side filter policy, threshold and margin.",
            "sample_scope": "FPMarkets US100 M5 2022-09-01 to 2026-04-13, train/validation/oos.",
            "success_criteria": "Validation proxy has positive EV, PF above 1, 3+ trades/day, tolerable drawdown, and package is ready for MT5 probe.",
            "failure_criteria": "No surface reaches density and positive EV, or runtime package cannot be produced.",
            "invalid_conditions": "feature hash mismatch, duplicate timestamps, non-finite features, ONNX sanity mismatch, missing handoff artifacts.",
            "stop_conditions": "Queue a bounded MT5 probe package or mark package/compile blocked.",
            "evidence_plan": [rel(PROXY_THRESHOLD_SCREEN), rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), rel(EA_SYNC_MANIFEST)],
            "evidence_boundary": "scout_and_handoff_only",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base_payload,
            "data_source": rel(TRAINING_DATASET),
            "time_axis": "timestamp is broker-clock alignment key materialized as bar_time_server for MT5 matching; timestamp_utc is written for audit.",
            "sample_scope": {"rows": int(summary.get("rows", 0)), "splits": summary.get("split_summary", {})},
            "missing_or_duplicate_check": "duplicate timestamp rows rejected; feature NaN/inf coerced only after feature-column audit.",
            "feature_label_boundary": "features are current-bar inputs; label uses future_log_return_12 and is not used in feature construction.",
            "split_boundary": summary.get("split_boundaries", {}),
            "leakage_risk": "validation threshold ranking creates research selection risk; OOS is read-only and MT5 probe remains required.",
            "data_hash_or_identity": {"training_dataset_sha256": sha256_file(TRAINING_DATASET), "summary_sha256": sha256_file(TRAINING_SUMMARY), "feature_order_hash": FEATURE_ORDER_HASH},
            "integrity_judgment": "usable_with_boundary",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base_payload,
            "model_family": "multiclass logistic regression exported as manual ONNX MatMul/Add/Softmax graphs",
            "target_and_label": "label_class 0=short, 1=flat, 2=long from fwd12 log-return threshold",
            "split_method": "fixed train/validation/oos holdout",
            "selection_metric": "validation proxy EV score with trade/day, PF, recovery, drawdown, balance, and cost stress terms",
            "secondary_metrics": ["oos_read_only", "trade_count", "long_short_balance", "session_bucket_stability", "onnx_sanity_diff"],
            "threshold_policy": "searched on train-derived probability quantiles and ranked on validation only",
            "overfit_risk": "multiple threshold/model/surface testing; MT5 and later WFO evidence required before promotion language",
            "calibration_risk": "Logistic Softmax outputs are treated as runtime probabilities but not live-calibrated probabilities.",
            "comparison_baseline": "Stage350E runtime-repaired diagnostic ONNX paths",
            "validation_judgment": final["result_judgment"],
            "model_rows": [dict(row) for row in model_rows],
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base_payload,
            "research_path": rel(Path(__file__)),
            "runtime_path": [rel(ROOT / mt5.EA_SOURCE_PATH), rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)],
            "shared_contract": "58 features, [p_short,p_flat,p_long], threshold_margin, matrixf tensor input, ONNX_NO_CONVERSION, output shape [1,3].",
            "known_differences": "Stage351B does not execute MT5 Strategy Tester; proxy EV is not MT5 KPI.",
            "parity_check": "Python ONNXRuntime sample sanity only; Stage351C must compare MT5 telemetry with expected_tape.",
            "parity_identity": [rel(EA_SYNC_MANIFEST), rel(MODEL_HANDOFF_MANIFEST), rel(FEATURE_MATRIX_MANIFEST)],
            "runtime_claim_boundary": "runtime_handoff_package_only",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [rel(PROXY_THRESHOLD_SCREEN), rel(PROXY_SELECTION_QUEUE), rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), rel(EA_SYNC_MANIFEST)],
            "evidence_missing": ["MT5 runtime telemetry", "strategy tester KPI", "proxy-vs-MT5 difference attribution", "WFO/forward authority"],
            "judgment_label": final["result_judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "run351C MT5 runtime probe must execute selected validation/oos attempts and compare expected_tape.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base_payload,
            "allowed_claims": ["proxy_scout", "runtime_handoff_package_ready" if final["status"] != STATUS_BLOCKED else "blocked_package"],
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

    sanity_rows = pd.read_csv(fs_path(PYTHON_ONNX_SANITY), encoding="utf-8-sig").to_dict("records") if exists(PYTHON_ONNX_SANITY) else []
    compile_status = str(final.get("compile_status", "missing"))
    return [
        row("input_data_gate", exists(TRAINING_DATASET) and exists(TRAINING_SUMMARY), rel(TRAINING_DATASET), "training input exists and is auditable"),
        row("feature_order_contract_gate", exists(FEATURE_ORDER_CONTRACT) and FEATURE_ORDER_HASH == mt5.FEATURE_ORDER_HASH, rel(FEATURE_ORDER_CONTRACT), "58-feature order matches MT5 contract hash"),
        row("model_training_gate", exists(MODEL_TRAINING_SCORECARD) and int(final.get("model_variants", 0)) > 0, rel(MODEL_TRAINING_SCORECARD), "model variants were trained and scored"),
        row("onnx_export_gate", exists(MODEL_HANDOFF_MANIFEST) and int(final.get("model_variants", 0)) > 0, rel(MODEL_HANDOFF_MANIFEST), "manual ONNX models were exported"),
        row("python_onnx_sanity_gate", bool(sanity_rows) and all(float(r.get("max_abs_diff", 1.0) or 1.0) <= 1.0e-5 for r in sanity_rows), rel(PYTHON_ONNX_SANITY), "ONNXRuntime sample output matches Python logits"),
        row("proxy_kpi_contract_audit", exists(PROXY_THRESHOLD_SCREEN) and int(final.get("selected_surfaces", 0)) > 0, rel(PROXY_THRESHOLD_SCREEN), "proxy EV screen and queue were written"),
        row("runtime_handoff_package_gate", exists(RUNTIME_PROBE_ATTEMPT_PACKAGE) and int(final.get("runtime_attempt_rows", 0)) > 0, rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), "MT5 probe handoff rows exist"),
        row("metaeditor_compile_gate", compile_status in {"completed", "skipped"}, rel(EA_SYNC_MANIFEST), "EA compile/sync was attempted or explicitly skipped"),
        row("artifact_lineage_recorded", exists(LINEAGE_RECEIPT) and exists(RUN_MANIFEST), f"{rel(LINEAGE_RECEIPT)};{rel(RUN_MANIFEST)}", "artifact lineage connects inputs, models, package, and reports"),
        row("tier_pair_rows_written", exists(STAGE_LEDGER) and exists(PROJECT_LEDGER), f"{rel(STAGE_LEDGER)};{rel(PROJECT_LEDGER)}", "Tier A/Tier B/Tier A+B records are present"),
        row("final_claim_guard", all(final.get(key) == "not_claimed" for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]), rel(FINAL_DECISION), "operating claims remain closed"),
    ]


def write_lineage(final: Mapping[str, Any]) -> None:
    artifact_hashes = {
        rel(path): sha256_file(path)
        for path in OUTPUT_FILES
        if exists(path) and Path(path).is_file()
    }
    write_json(
        LINEAGE_RECEIPT,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": final["next_run_id"],
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": artifact_hashes,
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


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
            "parent_run_id": PARENT_RUN_ID,
            "created_at_utc": now_utc(),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "attempts": list(attempts),
            "gate_audit": rel(GATE_AUDIT),
            "final_decision": rel(FINAL_DECISION),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run351B No-Scaler/1D-Scaler ONNX Trade Surface(351B 실행 스케일러 없음/1차원 스케일러 온엑스 거래 표면)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- model_variants(모델 변형): `{final['model_variants']}`
- selected_surfaces(선택 표면): `{final['selected_surfaces']}`
- runtime_attempt_rows(런타임 시도 행): `{final['runtime_attempt_rows']}`
- best_surface_id(최상위 표면 ID): `{final['best_surface_id']}`
- validation_trade_per_day(검증 거래/일): `{final['best_validation_trade_per_day']:.4f}`
- validation_profit_factor(검증 수익 팩터): `{final['best_validation_profit_factor']:.4f}`
- validation_net_log_return(검증 순 로그수익): `{final['best_validation_net_log_return']:.8f}`
- validation_recovery_factor(검증 회복 계수): `{final['best_validation_recovery_factor']:.4f}`
- validation_max_drawdown(검증 최대 낙폭): `{final['best_validation_max_drawdown']:.8f}`
- stress_net_log_return(비용 압박 순 로그수익): `{final['best_stress_net_log_return']:.8f}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`

Action(행동): Stage350E(350E 실행)에서 통과한 no-scaler/1D-scaler ONNX(스케일러 없음/1차원 스케일러 온엑스) 계약으로 logistic Softmax(로지스틱 소프트맥스) 거래 표면을 재구축했다.

Effect(효과): 무거운 Stage350(350단계) runtime interop repair(런타임 상호운용 수리) 흐름을 닫고, Stage351C(351C 실행) MT5 runtime probe(MT5 런타임 탐침)가 바로 실행할 모델/설정/예상 테이프를 갖게 했다.

Boundary(경계): proxy expected value(프록시 예상값)는 scout(스카우트) 전용이다. MT5 KPI(MT5 핵심 성과 지표), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), goal achieve(목표 달성)는 주장하지 않는다.
"""
    decision = f"""# Stage351B Decision(351B 결정)

- decision(결정): `{final['decision']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`
- judgment(판정): `{final['judgment']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): validation proxy(검증 프록시) 기준으로 MT5 probe(MT5 탐침) 우선순위를 만들었다.

Effect(효과): 다음 작업은 proxy(프록시)를 믿는 것이 아니라, Strategy Tester(전략 테스터)에서 expected_tape(예상 테이프)와 runtime telemetry(런타임 기록)를 비교한다.
"""
    current = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{final['status']}`
- current_judgment(현재 판정): `{final['judgment']}`
- current_decision(현재 결정): `{final['decision']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage351B(351B 실행)에서 no-scaler/1D-scaler ONNX trade surface(스케일러 없음/1차원 스케일러 온엑스 거래 표면)와 MT5 handoff(인계)를 만들었다.

Effect(효과): Stage351C(351C 실행)는 새 표면을 MT5 runtime probe(MT5 런타임 탐침)로 검증하면 된다.
"""
    selection = f"""# Stage351 Selection Status(351단계 선택 상태)

- selection_status(선택 상태): `no_selection(선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- latest_judgment(최근 판정): `{final['judgment']}`
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
        "## run351B No-Scaler/1D-Scaler ONNX Trade Surface",
        f"""## run351B No-Scaler/1D-Scaler ONNX Trade Surface(351B 실행 스케일러 없음/1차원 스케일러 온엑스 거래 표면)

- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- judgment(판정): `{final['judgment']}`
- selected_surfaces(선택 표면): `{final['selected_surfaces']}`
- runtime_attempt_rows(런타임 시도 행): `{final['runtime_attempt_rows']}`
""",
    )
    changelog = f"""## {TODAY} run351B No-Scaler/1D-Scaler ONNX Trade Surface

- action(행동): no-scaler/1D-scaler ONNX(스케일러 없음/1차원 스케일러 온엑스) logistic Softmax(로지스틱 소프트맥스) 표면 `{final['model_variants']}`개를 학습하고 MT5 probe(MT5 탐침) 시도 `{final['runtime_attempt_rows']}`행을 만들었다.
- effect(효과): Stage351C(351C 실행)가 proxy expected value(프록시 예상값)와 MT5 runtime telemetry(MT5 런타임 기록)를 비교할 수 있게 했다.
"""
    append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run351B No-Scaler/1D-Scaler ONNX Trade Surface", changelog)
    append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run351B No-Scaler/1D-Scaler ONNX Trade Surface", changelog)
    append_text_once(
        IDEA_REGISTRY,
        "stage351_no_scaler_or_1d_scaler_softmax_trade_surface",
        """## stage351_no_scaler_or_1d_scaler_softmax_trade_surface

- hypothesis(가설): Stage350E(350E 실행)에서 통과한 단순 ONNX(온엑스) 계약이면 거래 표면을 다시 만들 수 있다.
- evidence_boundary(근거 경계): scout_and_handoff_only(스카우트 및 인계 전용)
""",
    )
    if final["status"] == STATUS_WEAK:
        append_text_once(
            NEGATIVE_RESULT_REGISTER,
            "stage351B_proxy_weak_trade_surface",
            """## stage351B_proxy_weak_trade_surface

- result(결과): proxy(프록시)는 약하지만 MT5 probe(MT5 탐침) 인계는 가능하다.
- reopen_condition(재개 조건): MT5 runtime probe(MT5 런타임 탐침)가 proxy(프록시)와 다른 수익 구조를 보이거나 새 threshold/rule stack(임계값/규칙 묶음)이 생길 때 재개한다.
""",
        )


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
        "model_variants": final["model_variants"],
        "selected_surfaces": final["selected_surfaces"],
        "runtime_attempt_rows": final["runtime_attempt_rows"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    ledger_base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "result_judgment": final["result_judgment"],
        "decision": final["decision"],
        "next_run_id": final["next_run_id"],
        "primary_artifact": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "structural_scout_and_runtime_handoff",
        "primary_kpi": f"validation_pf={final['best_validation_profit_factor']:.4f};validation_tpd={final['best_validation_trade_per_day']:.4f};validation_net={final['best_validation_net_log_return']:.8f}",
        "guardrail_kpi": f"stress_net={final['best_stress_net_log_return']:.8f};runtime_probe_required",
        "external_verification_status": "mt5_probe_required",
        "trade_count": "",
        "net_profit": "",
        "profit_factor": "",
        "expectancy": "",
        "drawdown": "",
        "recovery_factor": "",
    }
    rows = [
        {
            **ledger_base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "proxy_trade_surface_and_runtime_handoff",
            "kpi_scope": "proxy_scout_only",
        },
        {
            **ledger_base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **ledger_base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "tier_b_missing_same_as_tier_a_boundary",
            "kpi_scope": "proxy_scout_only",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)


def update_artifact_registry() -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": Path(path).suffix.lstrip(".") or "artifact",
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha256_file(path) if Path(path).is_file() else "",
                    "created_at": TODAY,
                    "created_at_utc": now_utc(),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def validate(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    missing = [
        rel(path)
        for path in [
            FINAL_DECISION,
            RUN_MANIFEST,
            GATE_AUDIT,
            REPORT_PATH,
            MODEL_HANDOFF_MANIFEST,
            PROXY_THRESHOLD_SCREEN,
            PROXY_SELECTION_QUEUE,
            RUNTIME_PROBE_ATTEMPT_PACKAGE,
            EXPECTED_TAPE,
            EA_SYNC_MANIFEST,
        ]
        if not exists(path)
    ]
    if missing:
        raise FileNotFoundError("missing generated output: " + ", ".join(missing))
    failed = [gate["gate_id"] for gate in gates if gate.get("status") != "passed"]
    if failed and not str(final.get("status", "")).startswith("blocked_"):
        raise RuntimeError("required gate audit failed: " + ", ".join(failed))
    if final.get("goal_achieve") != "not_claimed":
        raise RuntimeError("forbidden goal claim")


def write_python_onnx_sanity_from_models(model_rows: Sequence[Mapping[str, Any]]) -> None:
    rows = [
        {
            "model_variant_id": row["model_variant_id"],
            "model_path": row["model_path"],
            "model_sha256": row["model_sha256"],
            "sample_rows": row["onnx_sanity_rows"],
            "max_abs_diff": row["onnx_sanity_max_abs_diff"],
            "status": "passed" if float(row["onnx_sanity_max_abs_diff"]) <= 1.0e-5 else "failed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in model_rows
    ]
    write_csv(PYTHON_ONNX_SANITY, rows)


def main() -> None:
    args = parse_args()
    for directory in [RUN_DIR, FEATURE_DIR, MODEL_DIR, EXPECTED_DIR, MT5_DIR, SET_DIR, INI_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    for path in INPUT_FILES:
        required(path)

    common_files_root = Path(args.common_files_root)
    frame, summary = load_training_frame()
    write_feature_order_contract(summary)
    feature_manifest, sync_rows = materialize_feature_matrix(frame, common_files_root)
    model_rows, probability_by_variant, _score_rows = train_variants(frame)
    write_python_onnx_sanity_from_models(model_rows)
    screen_rows, selected_surfaces, _stability_rows = screen_thresholds(frame, probability_by_variant)
    if args.max_surfaces > 0:
        selected_surfaces = selected_surfaces[: args.max_surfaces]
        write_csv(PROXY_SELECTION_QUEUE, selected_surfaces)
    common_by_model = copy_models_to_common(model_rows, common_files_root, sync_rows)
    write_expected_tape(frame, selected_surfaces, probability_by_variant)
    attempt_rows, _set_rows, _ini_rows = materialize_runtime_attempts(frame, selected_surfaces, model_rows, common_by_model)
    compile_payload = compile_and_sync_ea(Path(args.metaeditor_path), Path(args.terminal_data_root), skip_compile=bool(args.skip_compile))
    final_seed = build_final(
        selected_surfaces=selected_surfaces,
        attempt_rows=attempt_rows,
        compile_payload=compile_payload,
        model_rows=model_rows,
    )
    write_receipts(final_seed, summary, model_rows)
    write_lineage(final_seed)
    gates = make_gates(final_seed)
    write_csv(GATE_AUDIT, gates)
    write_final_manifest(final_seed, gates, attempt_rows)
    final = read_json(FINAL_DECISION)
    write_docs(final)
    write_registers(final)
    update_artifact_registry()
    write_lineage(final)
    gates = make_gates(final)
    write_csv(GATE_AUDIT, gates)
    write_final_manifest(final, gates, attempt_rows)
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
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "model_variants": final["model_variants"],
                "selected_surfaces": final["selected_surfaces"],
                "runtime_attempt_rows": final["runtime_attempt_rows"],
                "best_validation_trade_per_day": final["best_validation_trade_per_day"],
                "best_validation_profit_factor": final["best_validation_profit_factor"],
                "best_validation_net_log_return": final["best_validation_net_log_return"],
                "compile_status": final["compile_status"],
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
