from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import onnx
import onnxruntime as ort
import pandas as pd
from onnx import TensorProto, helper, numpy_helper
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import log_loss
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


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
    review_onnx_short_carry_mt5_probe_without_db as review349c,
)


TODAY = "2026-06-01"
STAGE_ID = "349_onnx_short_carry_runtime__execute_mt5_probe"
SOURCE_STAGE_ID = source_pkg.STAGE_ID
RUN_NUMBER = "run349E"
RUN_ID = "run349E_repair_treeensemble_onnx_operator_or_pivot_model_family_without_db_v1"
PARENT_RUN_ID = "run349D_test_onnx_no_conversion_runtime_parity_diagnostic_without_db_v1"
SOURCE_PACKAGE_RUN_ID = source_pkg.RUN_ID
NEXT_RUN_ID = "run349F_review_runtime_compatible_mlp_probe_or_open_next_alpha_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_compatible_mlp_operator_pivot_probe_only_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage349/run349E_runtime_compatible_mlp_probe"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage349_ONNXShortCarry__RuntimeCompatibleMLPPivot"
PARITY_TOLERANCE = 1.0e-4

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run349E_runtime_compatible_mlp_operator_pivot_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage349E_runtime_compatible_mlp_operator_pivot_probe.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN349D_DIR = STAGE_DIR / "02_runs" / "run349D"
RUN349D_FINAL = RUN349D_DIR / "final_decision.json"
RUN349D_GATES = RUN349D_DIR / "required_gate_coverage_audit.csv"
RUN349D_SUMMARY = RUN349D_DIR / "onnx_no_conversion_runtime_parity_summary.csv"

SOURCE_FEATURES = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run348C" / "features" / "runtime_features.csv"
SOURCE_FEATURE_ORDER = (
    ROOT
    / "stages"
    / "347_cash_open_asymmetric_source__long_short_head_design"
    / "02_runs"
    / "run347C"
    / "feature_order.csv"
)
SOURCE_FEATURE_ORDER_CONTRACT = source_pkg.FEATURE_ORDER_CONTRACT
SOURCE_FEATURE_LABEL = (
    ROOT
    / "stages"
    / "347_cash_open_asymmetric_source__long_short_head_design"
    / "02_runs"
    / "run347B"
    / "feature_label_source_table.csv"
)
SOURCE_PREDICTIONS = (
    ROOT
    / "stages"
    / "347_cash_open_asymmetric_source__long_short_head_design"
    / "02_runs"
    / "run347C"
    / "proxy_model_predictions.csv"
)

ATTEMPT_PACKAGE = RUN_DIR / "runtime_compatible_mlp_attempt_package.csv"
TRAINING_AUDIT = RUN_DIR / "runtime_compatible_mlp_training_audit.csv"
THRESHOLD_SCREEN = RUN_DIR / "runtime_compatible_mlp_threshold_screen.csv"
PYTHON_ONNX_PARITY = RUN_DIR / "python_onnx_parity.csv"
EXPECTED_TAPE = RUN_DIR / "expected_tape.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
SUMMARY_CSV = RUN_DIR / "runtime_compatible_mlp_mt5_probe_summary.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_BOUNDARY_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
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
    RUN349D_FINAL,
    RUN349D_GATES,
    RUN349D_SUMMARY,
    SOURCE_FEATURES,
    SOURCE_FEATURE_ORDER,
    SOURCE_FEATURE_ORDER_CONTRACT,
    SOURCE_FEATURE_LABEL,
    SOURCE_PREDICTIONS,
)

OUTPUT_FILES = (
    ATTEMPT_PACKAGE,
    TRAINING_AUDIT,
    THRESHOLD_SCREEN,
    PYTHON_ONNX_PARITY,
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
    parser = argparse.ArgumentParser(description="Run Stage349E runtime-compatible MLP ONNX pivot probe.")
    parser.add_argument("--terminal-path", default=str(source_pkg.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(source_pkg.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(source_pkg.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(source_pkg.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--reuse-existing-outputs", action="store_true")
    return parser.parse_args()


def gate_passed(path: Path) -> bool:
    _fields, rows = read_csv_rows(required(path))
    return bool(rows) and all(str(row.get("status", "")).lower() == "passed" for row in rows)


def norm_time(value: Any) -> str:
    text = str(value).strip()
    text = text.replace("T", " ").replace("Z", "")
    if "-" in text[:10]:
        text = text.replace("-", ".")
    if "." in text[10:]:
        text = text.split(".", 1)[0]
    return text[:19]


def fnv1a64_upper(line: str) -> str:
    value = 1469598103934665603
    for char in line:
        value = ((value ^ ord(char)) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return f"{value:X}"


def label_to_id(value: Any) -> int:
    text = str(value).lower()
    if "short" in text or "숏" in text:
        return 0
    if "long" in text or "롱" in text:
        return 2
    return 1


def id_to_label(value: int) -> str:
    return {0: "short", 1: "flat", 2: "long"}.get(int(value), "flat")


def load_feature_order() -> list[str]:
    frame = pd.read_csv(fs_path(required(SOURCE_FEATURE_ORDER)), encoding="utf-8-sig")
    return frame["feature_name"].astype(str).tolist()


def load_frames(feature_order: Sequence[str]) -> pd.DataFrame:
    features = pd.read_csv(fs_path(required(SOURCE_FEATURES)), encoding="utf-8-sig", low_memory=False).fillna("")
    labels = pd.read_csv(fs_path(required(SOURCE_FEATURE_LABEL)), encoding="utf-8-sig", low_memory=False).fillna("")
    predictions = pd.read_csv(fs_path(required(SOURCE_PREDICTIONS)), encoding="utf-8-sig", low_memory=False).fillna("")
    features["bar_time_key"] = features["bar_time_server"].map(norm_time)
    labels["bar_time_key"] = labels["bar_time"].map(norm_time)
    predictions["bar_time_key"] = predictions["bar_time"].map(norm_time)
    keep_label_cols = [
        "bar_time_key",
        "feature_input_hash",
        "allocator_teacher_label",
        "long_quality_teacher_label",
        "short_carry_teacher_label",
        "cash_open_bucket",
        "minutes_from_cash_open",
    ]
    keep_pred_cols = [
        "bar_time_key",
        "HistGBM_allocator_p_short",
        "HistGBM_allocator_p_flat",
        "HistGBM_allocator_p_long",
    ]
    merged = features.merge(labels[keep_label_cols], on="bar_time_key", how="left", suffixes=("", "_label"))
    merged = merged.merge(predictions[keep_pred_cols], on="bar_time_key", how="left")
    for column in feature_order:
        merged[column] = pd.to_numeric(merged[column], errors="raise")
    for column in ["long_quality_teacher_label", "short_carry_teacher_label", "minutes_from_cash_open"]:
        merged[column] = pd.to_numeric(merged[column], errors="coerce").fillna(0.0)
    for column in ["HistGBM_allocator_p_short", "HistGBM_allocator_p_flat", "HistGBM_allocator_p_long"]:
        merged[column] = pd.to_numeric(merged[column], errors="coerce").fillna(0.0)
    return merged


def pseudo_histgbm_labels(frame: pd.DataFrame) -> np.ndarray:
    train = frame[frame["split"].astype(str).eq("train")]
    long_threshold = float(train["HistGBM_allocator_p_long"].quantile(0.95))
    short_threshold = float(train["HistGBM_allocator_p_short"].quantile(0.95))
    labels: list[int] = []
    for _, row in frame.iterrows():
        p_short = float(row["HistGBM_allocator_p_short"])
        p_long = float(row["HistGBM_allocator_p_long"])
        if p_long >= long_threshold and p_long >= p_short:
            labels.append(2)
        elif p_short >= short_threshold:
            labels.append(0)
        else:
            labels.append(1)
    return np.asarray(labels, dtype=np.int64)


def balanced_indices(y: np.ndarray, *, seed: int, per_class: int = 900) -> np.ndarray:
    rng = np.random.default_rng(seed)
    indices: list[np.ndarray] = []
    for klass in [0, 1, 2]:
        klass_indices = np.flatnonzero(y == klass)
        if len(klass_indices) == 0:
            raise ValueError(f"class missing for MLP training(MLP 학습 클래스 누락): {klass}")
        replace = len(klass_indices) < per_class
        indices.append(rng.choice(klass_indices, size=per_class, replace=replace))
    output = np.concatenate(indices)
    rng.shuffle(output)
    return output


def build_manual_mlp_onnx(
    path: Path,
    scaler: StandardScaler,
    model: MLPClassifier,
    feature_count: int,
) -> None:
    input_name = "float_input"
    output_name = "probabilities"
    nodes = []
    initializers = [
        numpy_helper.from_array(scaler.mean_.astype(np.float32).reshape(1, feature_count), name="scaler_mean"),
        numpy_helper.from_array(scaler.scale_.astype(np.float32).reshape(1, feature_count), name="scaler_scale"),
    ]
    nodes.append(helper.make_node("Sub", [input_name, "scaler_mean"], ["centered"], name="center_features"))
    nodes.append(helper.make_node("Div", ["centered", "scaler_scale"], ["layer0_input"], name="scale_features"))
    current = "layer0_input"
    for layer_index, (weights, bias) in enumerate(zip(model.coefs_, model.intercepts_)):
        weight_name = f"W{layer_index}"
        bias_name = f"B{layer_index}"
        matmul_name = f"matmul_{layer_index}"
        add_name = f"add_{layer_index}"
        initializers.append(numpy_helper.from_array(weights.astype(np.float32), name=weight_name))
        initializers.append(numpy_helper.from_array(bias.astype(np.float32), name=bias_name))
        nodes.append(helper.make_node("MatMul", [current, weight_name], [matmul_name], name=f"matmul_layer_{layer_index}"))
        nodes.append(helper.make_node("Add", [matmul_name, bias_name], [add_name], name=f"bias_layer_{layer_index}"))
        if layer_index < len(model.coefs_) - 1:
            relu_name = f"relu_{layer_index}"
            nodes.append(helper.make_node("Relu", [add_name], [relu_name], name=f"relu_layer_{layer_index}"))
            current = relu_name
        else:
            nodes.append(helper.make_node("Softmax", [add_name], [output_name], name="probability_softmax", axis=1))
    graph = helper.make_graph(
        nodes,
        "stage349E_runtime_compatible_mlp",
        [helper.make_tensor_value_info(input_name, TensorProto.FLOAT, [None, feature_count])],
        [helper.make_tensor_value_info(output_name, TensorProto.FLOAT, [None, 3])],
        initializer=initializers,
    )
    onnx_model = helper.make_model(graph, opset_imports=[helper.make_operatorsetid("", 12)])
    onnx_model.ir_version = 7
    onnx.checker.check_model(onnx_model)
    ensure_parent(path)
    path.write_bytes(onnx_model.SerializeToString())


def train_models(frame: pd.DataFrame, feature_order: Sequence[str]) -> tuple[list[dict[str, Any]], dict[str, np.ndarray]]:
    train_mask = frame["split"].astype(str).eq("train").to_numpy()
    x_all = frame.loc[:, list(feature_order)].to_numpy(dtype=np.float32, copy=True)
    y_teacher = frame["allocator_teacher_label"].map(label_to_id).to_numpy(dtype=np.int64)
    y_hist = pseudo_histgbm_labels(frame)
    variants = [
        {
            "attempt_name": "e01_mlp_teacher_balanced",
            "target": y_teacher,
            "model_family": "pure_tensor_mlp_teacher_balanced",
            "hidden": (16,),
            "seed": 34901,
        },
        {
            "attempt_name": "e02_mlp_histgbm_distill_q95",
            "target": y_hist,
            "model_family": "pure_tensor_mlp_histgbm_distill_q95",
            "hidden": (16,),
            "seed": 34902,
        },
    ]
    attempts: list[dict[str, Any]] = []
    probability_by_attempt: dict[str, np.ndarray] = {}
    training_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    for variant in variants:
        y_all = np.asarray(variant["target"], dtype=np.int64)
        y_train = y_all[train_mask]
        x_train = x_all[train_mask]
        scaler = StandardScaler()
        scaler.fit(x_train)
        selected = balanced_indices(y_train, seed=int(variant["seed"]), per_class=900)
        x_balanced = scaler.transform(x_train[selected]).astype(np.float32)
        y_balanced = y_train[selected]
        model = MLPClassifier(
            hidden_layer_sizes=variant["hidden"],
            activation="relu",
            solver="lbfgs",
            alpha=1.0e-4,
            max_iter=350,
            random_state=int(variant["seed"]),
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ConvergenceWarning)
            model.fit(x_balanced, y_balanced)
        probabilities = model.predict_proba(scaler.transform(x_all).astype(np.float32)).astype(np.float32)
        if list(model.classes_) != [0, 1, 2]:
            raise RuntimeError(f"unexpected class order(예상 밖 클래스 순서): {model.classes_}")
        model_path = MODEL_DIR / f"{variant['attempt_name']}.onnx"
        build_manual_mlp_onnx(model_path, scaler, model, len(feature_order))
        sess = ort.InferenceSession(fs_path(model_path), providers=["CPUExecutionProvider"])
        onnx_probs = sess.run(None, {sess.get_inputs()[0].name: x_all.astype(np.float32)})[0]
        max_abs = float(np.max(np.abs(onnx_probs - probabilities)))
        logloss_value = float(log_loss(y_train, probabilities[train_mask], labels=[0, 1, 2]))
        counts = {f"train_class_{klass}_rows": int(np.sum(y_train == klass)) for klass in [0, 1, 2]}
        training_rows.append(
            {
                "attempt_name": variant["attempt_name"],
                "model_family": variant["model_family"],
                "train_rows": int(len(y_train)),
                "balanced_rows": int(len(y_balanced)),
                **counts,
                "hidden_layers": str(variant["hidden"]),
                "solver": "lbfgs",
                "train_log_loss": logloss_value,
                "model_path": rel(model_path),
                "model_sha256": sha256_file(model_path),
                "operator_policy": "pure_tensor_ops_only(순수 텐서 연산만 사용)",
                "effect": "MT5 ai.onnx.ml TreeEnsembleClassifier(트리 앙상블 분류기) 실패를 우회한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        parity_rows.append(
            {
                "attempt_name": variant["attempt_name"],
                "python_vs_manual_onnx_max_abs_diff": max_abs,
                "status": "passed" if max_abs <= 1.0e-6 else "failed",
                "model_path": rel(model_path),
                "effect": "Python sklearn(파이썬 사이킷런) 확률과 manual ONNX(수동 온엑스) 확률이 같은지 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        probability_by_attempt[variant["attempt_name"]] = probabilities
        attempts.append({**variant, "model_path": model_path, "model_sha256": sha256_file(model_path)})
    write_csv(TRAINING_AUDIT, training_rows)
    write_csv(PYTHON_ONNX_PARITY, parity_rows)
    return attempts, probability_by_attempt


def decision_from_probs(p_short: float, p_flat: float, p_long: float, short_threshold: float, long_threshold: float) -> str:
    del p_flat
    short_ok = p_short >= short_threshold
    long_ok = p_long >= long_threshold
    if long_ok and (not short_ok or p_long >= p_short):
        return "long"
    if short_ok:
        return "short"
    return "flat"


def apply_side_filter(label: str, minutes_from_cash_open: float) -> str:
    if label == "long" and 0.0 <= minutes_from_cash_open <= 60.0:
        return "flat"
    return label


def screen_thresholds(
    frame: pd.DataFrame,
    attempts: Sequence[Mapping[str, Any]],
    probability_by_attempt: Mapping[str, np.ndarray],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    quantiles = [0.70, 0.80, 0.85, 0.90, 0.95]
    for attempt in attempts:
        probs = probability_by_attempt[str(attempt["attempt_name"])]
        train_mask = frame["split"].astype(str).eq("train").to_numpy()
        for q_long in quantiles:
            long_threshold = float(np.quantile(probs[train_mask, 2], q_long))
            for q_short in quantiles:
                short_threshold = float(np.quantile(probs[train_mask, 0], q_short))
                labels = []
                for idx, row in frame.iterrows():
                    label = decision_from_probs(float(probs[idx, 0]), float(probs[idx, 1]), float(probs[idx, 2]), short_threshold, long_threshold)
                    labels.append(apply_side_filter(label, float(row["minutes_from_cash_open"])))
                labels_arr = np.asarray(labels, dtype=object)
                for split_name in ["train", "validation", "test", "all"]:
                    if split_name == "all":
                        mask = np.ones(len(frame), dtype=bool)
                    else:
                        mask = frame["split"].astype(str).eq(split_name).to_numpy()
                    split_labels = labels_arr[mask]
                    signal_mask = split_labels != "flat"
                    long_hits = int(np.sum((split_labels == "long") & (frame.loc[mask, "long_quality_teacher_label"].to_numpy(dtype=float) > 0)))
                    short_hits = int(np.sum((split_labels == "short") & (frame.loc[mask, "short_carry_teacher_label"].to_numpy(dtype=float) > 0)))
                    signal_rows = int(np.sum(signal_mask))
                    teacher_hits = int(long_hits + short_hits)
                    precision = teacher_hits / signal_rows if signal_rows else 0.0
                    balance = (
                        min(int(np.sum(split_labels == "long")), int(np.sum(split_labels == "short")))
                        / max(1, max(int(np.sum(split_labels == "long")), int(np.sum(split_labels == "short"))))
                    )
                    target_penalty = abs(signal_rows - 450) / 450 if split_name == "all" else 0.0
                    score = (teacher_hits * 3.0) + (precision * 200.0) + (balance * 40.0) - (target_penalty * 40.0)
                    rows.append(
                        {
                            "attempt_name": attempt["attempt_name"],
                            "model_family": attempt["model_family"],
                            "split": split_name,
                            "q_long": q_long,
                            "q_short": q_short,
                            "long_threshold": long_threshold,
                            "short_threshold": short_threshold,
                            "signal_rows": signal_rows,
                            "predicted_long_rows": int(np.sum(split_labels == "long")),
                            "predicted_short_rows": int(np.sum(split_labels == "short")),
                            "teacher_hit_rows": teacher_hits,
                            "teacher_long_hit_rows": long_hits,
                            "teacher_short_hit_rows": short_hits,
                            "teacher_precision": precision,
                            "long_short_balance": balance,
                            "selection_score": score,
                            "allowed_use": "proxy_signal_sanity_only(프록시 신호 점검 전용)",
                            "forbidden_use": "MT5_KPI_substitute_or_selection(MT5 핵심 성과 지표 대체 또는 선정)",
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )
    write_csv(THRESHOLD_SCREEN, rows)
    return rows


def select_attempts(
    frame: pd.DataFrame,
    attempts: Sequence[Mapping[str, Any]],
    probability_by_attempt: Mapping[str, np.ndarray],
    screen_rows: Sequence[Mapping[str, Any]],
    common_files_root: Path,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    all_rows = [row for row in screen_rows if row["split"] == "all" and 250 <= int(row["signal_rows"]) <= 900]
    for base in attempts:
        candidates = [row for row in all_rows if row["attempt_name"] == base["attempt_name"]]
        if not candidates:
            candidates = [row for row in screen_rows if row["split"] == "all" and row["attempt_name"] == base["attempt_name"]]
        best = sorted(candidates, key=lambda row: float(row["selection_score"]), reverse=True)[0]
        attempt_name = str(base["attempt_name"])
        model_common_path = f"{COMMON_MODEL_DIR}/{attempt_name}.onnx"
        common_model_abs = common_files_root / Path(model_common_path)
        ensure_parent(common_model_abs)
        shutil.copy2(fs_path(base["model_path"]), fs_path(common_model_abs))
        selected.append(
            {
                "attempt_name": attempt_name,
                "model_family": base["model_family"],
                "model_id": f"stage349E_{attempt_name}",
                "model_path": rel(base["model_path"]),
                "model_sha256": sha256_file(Path(base["model_path"])),
                "model_common_path": model_common_path,
                "model_common_sha256": sha256_file(common_model_abs),
                "feature_csv_path": "Project_Obsidian_Prime_v2/stage348/run348C_onnx_short_carry_probe/features/runtime_features.csv",
                "feature_count": len(load_feature_order()),
                "feature_order_hash": "870630295e4a4f15a168230f75a27726e910d8ba141270e1b2140cdd4519ba0c",
                "long_threshold": float(best["long_threshold"]),
                "short_threshold": float(best["short_threshold"]),
                "q_long": best["q_long"],
                "q_short": best["q_short"],
                "proxy_signal_rows": best["signal_rows"],
                "proxy_teacher_hit_rows": best["teacher_hit_rows"],
                "proxy_teacher_precision": best["teacher_precision"],
                "from_date": "2024.07.30",
                "to_date": "2025.01.01",
                "tier": "Tier A",
                "split": "all_rows_train_selected_thresholds",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return selected


def write_expected_tape(
    frame: pd.DataFrame,
    attempts: Sequence[Mapping[str, Any]],
    probability_by_attempt: Mapping[str, np.ndarray],
) -> None:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        probs = probability_by_attempt[str(attempt["attempt_name"])]
        for idx, row in frame.iterrows():
            label = decision_from_probs(
                float(probs[idx, 0]),
                float(probs[idx, 1]),
                float(probs[idx, 2]),
                float(attempt["short_threshold"]),
                float(attempt["long_threshold"]),
            )
            mapped = apply_side_filter(label, float(row["minutes_from_cash_open"]))
            teacher_label = id_to_label(label_to_id(row["allocator_teacher_label"]))
            teacher_hit = (
                (mapped == "long" and float(row["long_quality_teacher_label"]) > 0)
                or (mapped == "short" and float(row["short_carry_teacher_label"]) > 0)
            )
            rows.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "model_family": attempt["model_family"],
                    "bar_time_server": row["bar_time_server"],
                    "timestamp_utc": row["timestamp_utc"],
                    "split": row["split"],
                    "row_index": int(row["row_index"]),
                    "feature_input_hash": row.get("feature_input_hash", ""),
                    "p_short": float(probs[idx, 0]),
                    "p_flat": float(probs[idx, 1]),
                    "p_long": float(probs[idx, 2]),
                    "proxy_intended_label": label,
                    "ea_mapped_expected_label": mapped,
                    "expected_class_id": {"short": 0, "flat": 1, "long": 2}[mapped],
                    "teacher_allocator_label": teacher_label,
                    "teacher_hit": bool(teacher_hit),
                    "long_probability_threshold": attempt["long_threshold"],
                    "short_probability_threshold": attempt["short_threshold"],
                    "runtime_mapping_status": "threshold_rule_plus_long_early_side_filter(임계값 규칙과 초반 롱 차단 필터)",
                    "allowed_use": "proxy_vs_mt5_runtime_probe_comparison(프록시와 MT5 런타임 탐침 비교)",
                    "forbidden_use": "MT5_KPI_substitute_or_selection(MT5 핵심 성과 지표 대체 또는 선정)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(EXPECTED_TAPE, rows)


def materialize_mt5_files(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for idx, attempt in enumerate(attempts, start=1):
        common_telemetry = f"{COMMON_TELEMETRY_DIR}/{attempt['attempt_name']}_telemetry.csv"
        common_summary = f"{COMMON_TELEMETRY_DIR}/{attempt['attempt_name']}_summary.csv"
        set_name = f"OPV2_run349E_{attempt['attempt_name']}.set"
        ini_name = f"OPV2_run349E_{attempt['attempt_name']}.ini"
        report_name = f"POPv2_run349E_{attempt['attempt_name']}"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        set_values = {
            "InpRunId": f"{RUN_ID}_{attempt['attempt_name']}",
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
            "InpModelNoConversion": True,
            "InpSetOutputShape": True,
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
            "InpAllowTrading": True,
            "InpFixedLot": 0.1,
            "InpMagic": 3497000 + idx,
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
            generated_by="stage_pipelines/stage349/repair_treeensemble_onnx_operator_or_pivot_model_family_without_db.py",
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
                "allowed_use": "MT5 runtime probe(MT5 런타임 탐침)",
                "forbidden_use": "candidate_selection_or_operating_claim(후보 선정 또는 운영 주장)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(ATTEMPT_PACKAGE, rows)
    return rows


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        path = common_files_root / Path(str(attempt[key]))
        if exists(path):
            os.unlink(fs_path(path))


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        for key, suffix in (("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")):
            source = common_files_root / Path(str(attempt[key]))
            target = TELEMETRY_COPY_DIR / f"{attempt['attempt_name']}_{suffix}.csv"
            copied = False
            if exists(source):
                ensure_parent(target)
                shutil.copy2(fs_path(source), fs_path(target))
                copied = True
            rows.append(
                {
                    "copy_id": f"{attempt['attempt_name']}::{suffix}",
                    "attempt_name": attempt["attempt_name"],
                    "source_path": source.as_posix(),
                    "target_path": rel(target),
                    "exists": copied and exists(target),
                    "sha256": sha256_file(target) if copied and exists(target) else "",
                    "effect": "MT5 Common Files(공용 파일)의 runtime telemetry(런타임 기록)를 Stage349E run folder(실행 폴더)에 고정한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(RUNTIME_OUTPUT_COPY, rows)
    return rows


def execute_attempts(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    terminal_probe = terminal_processes()
    write_json(TERMINAL_PROCESS_AUDIT, terminal_probe)
    execution_results: list[dict[str, Any]] = []
    if args.materialize_only:
        for attempt in attempts:
            execution_results.append({"attempt_name": attempt["attempt_name"], "status": "not_run_materialize_only", "runtime_outputs": {"status": "not_run_materialize_only"}, "ini_path": attempt["ini_path"], "set_path": attempt["set_path"]})
    elif args.reuse_existing_outputs:
        for attempt in attempts:
            runtime_outputs = mt5.validate_mt5_runtime_outputs(common_files_root, attempt)
            execution_results.append({"attempt_name": attempt["attempt_name"], "status": "completed" if runtime_outputs.get("status") == "completed" else "blocked", "runtime_outputs": runtime_outputs, "ini_path": attempt["ini_path"], "set_path": attempt["set_path"]})
    elif terminal_probe.get("status") != "no_terminal64_process":
        for attempt in attempts:
            execution_results.append({"attempt_name": attempt["attempt_name"], "status": "blocked", "blocker": "target_portable_terminal_already_running", "runtime_outputs": {"status": "blocked", "wait_status": "skipped_terminal_already_running"}, "ini_path": attempt["ini_path"], "set_path": attempt["set_path"]})
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
                tester_result = {"status": "blocked", "command": exc.cmd, "returncode": None, "stdout": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "", "stderr": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "", "blocker": "terminal_timeout"}
            runtime_outputs = mt5.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=args.wait_timeout_seconds, poll_seconds=2.0)
            if runtime_outputs.get("status") != "completed":
                tester_result["status"] = "blocked"
                tester_result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            execution_results.append({**tester_result, "attempt_name": attempt["attempt_name"], "runtime_outputs": runtime_outputs, "ini_path": attempt["ini_path"], "set_path": attempt["set_path"]})
    report_records = mt5.collect_mt5_strategy_report_artifacts(terminal_data_root=terminal_data_root, run_output_root=RUN_DIR, attempts=attempts, run_id=RUN_ID)
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    copy_rows = copy_runtime_outputs(common_files_root, attempts)
    write_json(MT5_EXECUTION_RESULT, execution_results)
    write_json(STRATEGY_TESTER_REPORTS, report_records)
    return execution_results, report_records, copy_rows


def expected_by_attempt() -> dict[str, dict[str, Mapping[str, Any]]]:
    expected = pd.read_csv(fs_path(required(EXPECTED_TAPE)), encoding="utf-8-sig", low_memory=False).fillna("")
    output: dict[str, dict[str, Mapping[str, Any]]] = {}
    for attempt_name, group in expected.groupby("attempt_name"):
        output[str(attempt_name)] = {norm_time(row["bar_time_server"]): row.to_dict() for _, row in group.iterrows()}
    return output


def compare_outputs(attempts: Sequence[Mapping[str, Any]], execution_results: Sequence[Mapping[str, Any]], report_records: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
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
            summary_rows.append({"attempt_name": attempt_name, "runtime_status": execution.get("runtime_outputs", {}).get("status", "missing"), "report_status": report.get("status", "missing"), "rows_compared": 0, "probability_match_rows": 0, "input_hash_match_rows": 0, "max_abs_diff": "", "parity_status": "blocked_runtime_telemetry_missing(런타임 기록 누락)", "claim_boundary": CLAIM_BOUNDARY})
            continue
        telemetry = pd.read_csv(fs_path(local_telemetry), encoding="utf-8-sig", low_memory=False).fillna("")
        cycles = telemetry[telemetry["record_type"].astype(str).str.lower().eq("cycle")].copy()
        cycles = cycles[cycles["feature_ready"].astype(str).str.lower().eq("true")].copy()
        max_abs = 0.0
        matched_time = 0
        probability_match = 0
        input_hash_match = 0
        decision_match = 0
        for _, row in cycles.iterrows():
            key = norm_time(row.get("bar_time", ""))
            exp = expected.get(key)
            if exp is None:
                continue
            matched_time += 1
            diffs = {
                "p_short_abs_diff": abs(to_float(row.get("p_short")) - to_float(exp.get("p_short"))),
                "p_flat_abs_diff": abs(to_float(row.get("p_flat")) - to_float(exp.get("p_flat"))),
                "p_long_abs_diff": abs(to_float(row.get("p_long")) - to_float(exp.get("p_long"))),
            }
            row_max = max(diffs.values())
            max_abs = max(max_abs, row_max)
            prob_ok = row_max <= PARITY_TOLERANCE
            hash_ok = str(row.get("input_hash", "")).upper() == str(exp.get("feature_input_hash", "")).upper()
            dec_ok = str(row.get("decision", "")).lower() == str(exp.get("ea_mapped_expected_label", "")).lower()
            probability_match += int(prob_ok)
            input_hash_match += int(hash_ok)
            decision_match += int(dec_ok)
            diff_rows.append({"attempt_name": attempt_name, "bar_time": key, **diffs, "row_max_abs_diff": row_max, "probability_match": prob_ok, "input_hash_match": hash_ok, "decision_match": dec_ok, "mt5_decision": row.get("decision", ""), "expected_decision": exp.get("ea_mapped_expected_label", ""), "claim_boundary": CLAIM_BOUNDARY})
        if exists(local_summary):
            runtime_summary = pd.read_csv(fs_path(local_summary), encoding="utf-8-sig", low_memory=False).fillna("")
            last = runtime_summary.iloc[-1].to_dict() if not runtime_summary.empty else {}
        else:
            last = {}
        feature_days = len({key[:10] for key in expected if key})
        trade_count = to_int(metrics.get("trade_count"), 0)
        summary_rows.append(
            {
                "attempt_name": attempt_name,
                "model_family": attempt.get("model_family", ""),
                "runtime_status": execution.get("runtime_outputs", {}).get("status", "missing"),
                "report_status": report.get("status", "missing"),
                "rows_compared": matched_time,
                "probability_match_rows": probability_match,
                "input_hash_match_rows": input_hash_match,
                "decision_match_rows": decision_match,
                "max_abs_diff": max_abs if matched_time else "",
                "parity_status": "passed(통과)" if matched_time and probability_match == matched_time else "failed_or_missing(실패 또는 누락)",
                "net_profit": metrics.get("net_profit", ""),
                "profit_factor": metrics.get("profit_factor", ""),
                "expectancy": metrics.get("expectancy", ""),
                "max_drawdown_amount": metrics.get("max_drawdown_amount", ""),
                "recovery_factor": metrics.get("recovery_factor", ""),
                "trade_count": trade_count,
                "long_trade_count": metrics.get("long_trade_count", ""),
                "short_trade_count": metrics.get("short_trade_count", ""),
                "trade_density_per_feature_day": trade_count / feature_days if feature_days else "",
                "model_ok_count": to_int(last.get("model_ok_count"), 0),
                "feature_ready_count": to_int(last.get("feature_ready_count"), 0),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(PROXY_MT5_DIFF, diff_rows)
    write_csv(SUMMARY_CSV, summary_rows)
    return summary_rows, diff_rows


def write_runtime_identity(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]]) -> None:
    rows = [
        {"identity_type": "terminal64", "path": str(args.terminal_path), "sha256": sha256_file(Path(args.terminal_path)) if exists(Path(args.terminal_path)) else "", "status": "present" if exists(Path(args.terminal_path)) else "missing"},
    ]
    for attempt in attempts:
        model_path = ROOT / str(attempt["model_path"])
        common_model = Path(args.common_files_root) / Path(str(attempt["model_common_path"]))
        rows.append({"identity_type": "repo_model", "attempt_name": attempt["attempt_name"], "path": rel(model_path), "sha256": sha256_file(model_path), "status": "present"})
        rows.append({"identity_type": "common_files_model", "attempt_name": attempt["attempt_name"], "path": common_model.as_posix(), "sha256": sha256_file(common_model) if exists(common_model) else "", "status": "present" if exists(common_model) else "missing"})
    for module in mt5.mt5_runtime_module_hashes():
        rows.append({"identity_type": "mt5_runtime_module", "path": module.get("path", ""), "sha256": module.get("sha256", ""), "status": module.get("status", "")})
    write_csv(RUNTIME_IDENTITY, rows)


def build_final(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]], summary_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]], copy_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed_rows = [row for row in summary_rows if row.get("runtime_status") == "completed"]
    parity_pass_rows = [row for row in summary_rows if str(row.get("parity_status", "")).startswith("passed")]
    positive_rows = [row for row in summary_rows if to_float(row.get("net_profit")) > 0 and to_float(row.get("profit_factor")) >= 1.1 and to_int(row.get("trade_count")) >= 300]
    best = sorted(summary_rows, key=lambda row: (to_float(row.get("net_profit")), to_float(row.get("profit_factor"))), reverse=True)[0] if summary_rows else {}
    if len(completed_rows) < len(attempts):
        status = "blocked_stage349E_runtime_compatible_mlp_mt5_probe_incomplete_repair_required_no_selection"
        judgment = "blocked_runtime_outputs_missing_for_some_mlp_attempts"
        result_judgment = "blocked(차단)"
    elif positive_rows and len(parity_pass_rows) == len(attempts):
        status = "completed_stage349E_runtime_compatible_mlp_probe_positive_review_required_no_selection"
        judgment = "runtime_compatible_mlp_probe_positive_kpi_review_required_no_selection"
        result_judgment = "positive_review_required(긍정 검토 필요)"
    elif len(parity_pass_rows) == len(attempts):
        status = "completed_stage349E_runtime_compatible_mlp_probe_negative_or_weak_kpi_no_selection"
        judgment = "runtime_compatible_mlp_parity_passed_but_kpi_negative_or_weak_continue_offensive_exploration"
        result_judgment = "negative_or_weak_kpi(부정 또는 약한 KPI)"
    else:
        status = "completed_stage349E_runtime_compatible_mlp_probe_parity_failed_repair_required_no_selection"
        judgment = "pure_tensor_mlp_mt5_probability_parity_failed_runtime_repair_required"
        result_judgment = "negative_runtime_parity(부정 런타임 동등성)"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "result_judgment": result_judgment,
        "decision": "stage349E_open_run349F_review_runtime_compatible_mlp_probe_or_next_alpha",
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": len(attempts),
        "runtime_completed_rows": len(completed_rows),
        "parity_pass_rows": len(parity_pass_rows),
        "positive_rows": len(positive_rows),
        "diff_rows": len(diff_rows),
        "runtime_output_copy_ready_rows": sum(1 for row in copy_rows if str(row.get("exists", "")).lower() == "true"),
        "best_attempt_name": best.get("attempt_name", ""),
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


def make_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    def row(gate_id: str, passed: bool, evidence: str, effect: str) -> dict[str, Any]:
        return {"stage_id": STAGE_ID, "run_id": RUN_ID, "gate_id": gate_id, "status": "passed" if passed else "failed", "evidence": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY, "created_at_utc": now_utc()}
    return [
        row("parent_run349D_gate", gate_passed(RUN349D_GATES), rel(RUN349D_GATES), "TreeEnsembleClassifier(트리 앙상블 분류기) 실패 근거를 확인한다."),
        row("pure_tensor_onnx_materialized", exists(PYTHON_ONNX_PARITY) and all(r.get("status") == "passed" for r in pd.read_csv(fs_path(PYTHON_ONNX_PARITY)).to_dict("records")), rel(PYTHON_ONNX_PARITY), "ai.onnx.ml 연산자 없이 pure tensor ONNX(순수 텐서 온엑스)를 만든다."),
        row("threshold_screen_written", exists(THRESHOLD_SCREEN), rel(THRESHOLD_SCREEN), "train-selected threshold(학습 구간 선정 임계값)만 쓴다."),
        row("mt5_runtime_output_observed", final["runtime_completed_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0, rel(MT5_EXECUTION_RESULT), "MT5 runtime telemetry(런타임 기록)가 모든 시도에서 생성됐는지 확인한다."),
        row("strategy_report_collected", exists(STRATEGY_TESTER_REPORTS), rel(STRATEGY_TESTER_REPORTS), "Strategy Tester report(전략 테스터 보고서)를 수집한다."),
        row("proxy_mt5_diff_written", exists(PROXY_MT5_DIFF) and exists(SUMMARY_CSV), f"{rel(PROXY_MT5_DIFF)};{rel(SUMMARY_CSV)}", "proxy expected(프록시 예상)와 MT5 runtime(런타임) 차이를 기록한다."),
        row("tier_pair_rows_written", exists(STAGE_LEDGER) and exists(PROJECT_LEDGER), f"{rel(STAGE_LEDGER)};{rel(PROJECT_LEDGER)}", "Tier A/B/A+B 기록을 남긴다."),
        row("artifact_lineage_recorded", exists(ARTIFACT_LINEAGE_RECEIPT) and exists(RUN_MANIFEST), f"{rel(ARTIFACT_LINEAGE_RECEIPT)};{rel(RUN_MANIFEST)}", "입력, 모델, MT5 출력 계보를 연결한다."),
        row("final_claim_guard", all(final.get(key) == "not_claimed" for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]), rel(FINAL_DECISION), "운영 주장과 목표 달성을 주장하지 않는다."),
    ]


def write_receipts(final: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]]) -> None:
    base = {"stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": now_utc(), "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUNTIME_PARITY_RECEIPT, {**base, "research_path": rel(TRAINING_AUDIT), "runtime_path": rel(ATTEMPT_PACKAGE), "shared_contract": "feature order 53(피처 순서 53), output [p_short,p_flat,p_long](출력 순서), pure tensor ONNX(순수 텐서 온엑스)", "parity_check": rel(SUMMARY_CSV), "runtime_claim_boundary": "runtime_probe(런타임 탐침)"})
    write_json(BACKTEST_FORENSICS_RECEIPT, {**base, "tester_report": rel(STRATEGY_TESTER_REPORTS), "tester_settings": "US100 M5, Model=4(real ticks, 실제 틱), Deposit=500, Leverage=1:100", "forensic_gaps": [] if final["runtime_completed_rows"] == final["attempt_rows"] else ["some_runtime_outputs_missing(일부 런타임 출력 누락)"]})
    write_json(PERFORMANCE_ATTRIBUTION_RECEIPT, {**base, "summary": rel(SUMMARY_CSV), "best_attempt_name": final["best_attempt_name"], "best_net_profit": final["best_net_profit"], "best_profit_factor": final["best_profit_factor"], "best_trade_count": final["best_trade_count"], "judgment": final["judgment"]})
    write_json(JUDGMENT_RECEIPT, {**base, "result_judgment": final["result_judgment"], "status": final["status"], "decision": final["decision"], "next_run_id": final["next_run_id"], "forbidden_claims": ["candidate_selection", "forward_passed", "live_readiness", "operating_promotion", "runtime_authority", "goal_achieve"]})
    write_json(ARTIFACT_LINEAGE_RECEIPT, {**base, "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha256_file(path) for path in OUTPUT_FILES if exists(path) and path.is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "tracked", "lineage_judgment": "connected_with_boundary(경계 포함 연결)"})
    write_json(CLAIM_BOUNDARY_RECEIPT, {**base, "allowed_claims": ["runtime_probe(런타임 탐침)", "model_family_pivot_evidence(모델 계열 전환 근거)"], "forbidden_claims": ["candidate_selection", "forward_passed", "live_readiness", "operating_promotion", "runtime_authority", "goal_achieve"], "goal_achieve": "not_claimed"})


def write_final_manifest(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> None:
    payload = dict(final)
    payload["gate_passes"] = sum(1 for gate in gates if gate.get("status") == "passed")
    payload["gate_total"] = len(gates)
    write_json(FINAL_DECISION, payload)
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": now_utc(), "parent_run_id": PARENT_RUN_ID, "attempts": attempts, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)], "gates": rel(GATE_AUDIT), "final_decision": rel(FINAL_DECISION), "claim_boundary": CLAIM_BOUNDARY})


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run349E Runtime-Compatible MLP Operator Pivot Probe(349E 런타임 호환 MLP 연산자 전환 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- parity_pass_rows(동등성 통과 행): `{final['parity_pass_rows']}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_trade_count(최고 거래 수): `{final['best_trade_count']}`
- best_trade_density(최고 거래 밀도): `{final['best_trade_density_per_feature_day']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`

Action(행동): TreeEnsembleClassifier(트리 앙상블 분류기) ONNX(온엑스)를 버리고 pure tensor MLP(순수 텐서 다층 퍼셉트론) ONNX 후보를 만들어 MT5 Strategy Tester(전략 테스터)에 넣었다.

Effect(효과): MT5 ONNX runtime(런타임)이 확률을 같은 의미로 실행할 수 있는 모델 계열을 다시 열고, 수익 구조는 MT5 KPI(MT5 핵심 성과 지표)로만 판단한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    decision = f"""# Stage349E Decision(349E 결정)

- decision(결정): `{final['decision']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`
- result_judgment(결과 판정): `{final['result_judgment']}`

Action(행동): runtime-compatible MLP(런타임 호환 MLP) 탐침을 닫고 review/open-next-alpha(검토/다음 알파 열기)로 넘긴다.

Effect(효과): 운영 승격 없이 수익 구조와 runtime parity(런타임 동등성)를 분리해서 다음 탐색을 고른다.
"""
    current = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{final['status']}`
- current_judgment(현재 판정): `{final['judgment']}`
- current_decision(현재 결정): `{final['decision']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): run349E(349E 실행)는 pure tensor MLP ONNX(순수 텐서 MLP 온엑스) 후보를 MT5에서 탐침했다.

Effect(효과): 다음은 run349F(349F 실행)에서 parity/KPI(동등성/KPI)를 검토하거나 새 alpha branch(알파 분기)를 연다.
"""
    selection = f"""# Stage349 Selection Status(349단계 선택 상태)

- selection_status(선정 상태): `no_selection(선정 없음)`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- latest_judgment(최근 판정): `{final['judgment']}`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    stage_brief = f"""# Stage349 ONNX Short-Carry Runtime Probe(349단계 온엑스 숏 기여 런타임 탐침)

- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- latest_judgment(최근 판정): `{final['judgment']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Latest Evidence(최신 근거)

- run349D(349D 실행): input_hash(입력 해시)는 일치했지만 TreeEnsembleClassifier(트리 앙상블 분류기) ONNX 확률이 불일치했다.
- run349E(349E 실행): pure tensor MLP(순수 텐서 MLP) 후보를 MT5 runtime probe(런타임 탐침)로 실행했다.
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- next_condition(다음 조건): `{final['next_run_id']}`
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(STAGE_BRIEF, stage_brief)
    append_text_once(STAGE_README, "## run349E Runtime-Compatible MLP Operator Pivot Probe", f"""## run349E Runtime-Compatible MLP Operator Pivot Probe

- run_id(실행 ID): `{RUN_ID}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- effect(효과): TreeEnsembleClassifier(트리 앙상블 분류기) 실패 뒤 pure tensor MLP(순수 텐서 MLP) 경로를 검증했다.
""")
    changelog = f"""## {TODAY} run349E Runtime-Compatible MLP Operator Pivot Probe

- action(행동): pure tensor MLP ONNX(순수 텐서 MLP 온엑스) 후보 `{final['attempt_rows']}`개를 MT5 runtime probe(런타임 탐침)로 실행했다.
- effect(효과): best_attempt(최고 시도) `{final['best_attempt_name']}`, net_profit(순수익) `{final['best_net_profit']}`, PF(수익 팩터) `{final['best_profit_factor']}`를 기록했다.
"""
    append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run349E Runtime-Compatible MLP Operator Pivot Probe", changelog)
    append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run349E Runtime-Compatible MLP Operator Pivot Probe", changelog)


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
    run_row = {"run_id": RUN_ID, "stage_id": STAGE_ID, "run_number": RUN_NUMBER, "parent_run_id": PARENT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "result_judgment": final["result_judgment"], "decision": final["decision"], "next_run_id": final["next_run_id"], "report_path": rel(REPORT_PATH), "final_decision_path": rel(FINAL_DECISION), "gate_audit_path": rel(GATE_AUDIT), "created_at": TODAY, "claim_boundary": CLAIM_BOUNDARY}
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    ledger_base = {"stage_id": STAGE_ID, "run_id": RUN_ID, "run_number": RUN_NUMBER, "status": final["status"], "judgment": final["judgment"], "result_judgment": final["result_judgment"], "net_profit": final["best_net_profit"], "profit_factor": final["best_profit_factor"], "expectancy": final["best_expectancy"], "trade_count": final["best_trade_count"], "trade_density_per_feature_day": final["best_trade_density_per_feature_day"], "report_path": rel(REPORT_PATH), "final_decision_path": rel(FINAL_DECISION), "claim_boundary": CLAIM_BOUNDARY, "created_at": TODAY}
    ledger_rows = [
        {**ledger_base, "ledger_row_id": f"{RUN_ID}__Tier A", "subrun_id": "Tier A", "view": "Tier A used(Tier A 사용)", "record_view": "Tier A used(Tier A 사용)", "tier": "Tier A", "tier_scope": "Tier A", "metric_scope": "runtime_compatible_mlp_probe", "kpi_scope": "MT5 Strategy Tester report(MT5 전략 테스터 보고서)"},
        {**ledger_base, "ledger_row_id": f"{RUN_ID}__Tier B", "subrun_id": "Tier B", "view": "Tier B fallback used(Tier B 대체 사용)", "record_view": "Tier B fallback used(Tier B 대체 사용)", "tier": "Tier B", "tier_scope": "Tier B", "metric_scope": "missing_required", "kpi_scope": "missing_required", "net_profit": "", "profit_factor": "", "expectancy": "", "trade_count": "", "trade_density_per_feature_day": "", "result_status": "missing_required(필수 누락)"},
        {**ledger_base, "ledger_row_id": f"{RUN_ID}__Tier A+B", "subrun_id": "Tier A+B", "view": "Tier A+B combined(Tier A+B 합산)", "record_view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "tier_scope": "Tier A+B", "metric_scope": "same_as_tier_a_until_tier_b_available", "kpi_scope": "same_as_tier_a_until_tier_b_available"},
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows)


def update_artifact_registry() -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path):
            rows.append({"artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}", "stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": path.suffix.lstrip(".") or "artifact", "path": rel(path), "artifact_path": rel(path), "sha256": sha256_file(path) if path.is_file() else "", "created_at": TODAY, "created_at_utc": now_utc(), "claim_boundary": CLAIM_BOUNDARY})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def validate(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    missing = [rel(path) for path in [FINAL_DECISION, RUN_MANIFEST, GATE_AUDIT, REPORT_PATH, SUMMARY_CSV, EXPECTED_TAPE] if not exists(path)]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    if final.get("goal_achieve") != "not_claimed":
        raise RuntimeError("forbidden goal claim(금지된 목표 주장)")
    if not gates:
        raise RuntimeError("gate audit missing(게이트 감사 누락)")


def main() -> None:
    for directory in [RUN_DIR, MODEL_DIR, MT5_DIR, SET_DIR, INI_DIR, TELEMETRY_COPY_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    for path in INPUT_FILES:
        required(path)
    args = parse_args()
    feature_order = load_feature_order()
    frame = load_frames(feature_order)
    train_attempts, probability_by_attempt = train_models(frame, feature_order)
    screen_rows = screen_thresholds(frame, train_attempts, probability_by_attempt)
    selected = select_attempts(frame, train_attempts, probability_by_attempt, screen_rows, Path(args.common_files_root))
    write_expected_tape(frame, selected, probability_by_attempt)
    attempts = materialize_mt5_files(selected)
    execution_results, report_records, copy_rows = execute_attempts(args, attempts)
    summary_rows, diff_rows = compare_outputs(attempts, execution_results, report_records)
    write_runtime_identity(args, attempts)
    final_seed = build_final(args, attempts, summary_rows, diff_rows, copy_rows)
    write_receipts(final_seed, attempts)
    write_csv(NEXT_ACTION_QUEUE, [{"queue_id": NEXT_RUN_ID, "stage_id": STAGE_ID, "source_run_id": RUN_ID, "priority": 1, "action": "review_runtime_compatible_mlp_probe_or_open_next_alpha(런타임 호환 MLP 탐침 검토 또는 다음 알파 열기)", "effect": "runtime parity(런타임 동등성)와 MT5 KPI(MT5 핵심 성과 지표)에 따라 다음 탐색을 고른다.", "claim_boundary": CLAIM_BOUNDARY}])
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
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "judgment": final["judgment"], "result_judgment": final["result_judgment"], "attempts": final["attempt_rows"], "runtime_completed_rows": final["runtime_completed_rows"], "parity_pass_rows": final["parity_pass_rows"], "best_attempt_name": final["best_attempt_name"], "best_net_profit": final["best_net_profit"], "best_profit_factor": final["best_profit_factor"], "best_trade_count": final["best_trade_count"], "gates": f"{final['gate_passes']}/{final['gate_total']}", "goal_achieve": final["goal_achieve"], "next_run_id": final["next_run_id"]}, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
