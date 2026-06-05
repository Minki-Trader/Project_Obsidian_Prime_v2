from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from onnx import helper, numpy_helper


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage350 import (  # noqa: E402
    probe_matrix_tensor_gemm_runtime_repair_without_db as run350d,
)
from stage_pipelines.stage350 import (  # noqa: E402
    probe_softmax_output_shape_and_conversion_semantics_without_db as base,
)


TODAY = "2026-06-01"
STAGE_ID = "350_onnx_runtime_interop__softmax_output_shape_repair_probe"
RUN_NUMBER = "run350E"
RUN_ID = "run350E_table_runtime_or_feature_tensor_handoff_probe_without_db_v1"
PARENT_RUN_ID = run350d.RUN_ID
NEXT_IF_ONNX_REPAIR = "run350F_rebuild_no_scaler_or_1d_scaler_onnx_trade_surface_without_db_v1"
NEXT_IF_TABLE_ONLY = "run350F_build_runtime_table_trade_surface_from_proxy_clues_without_db_v1"
NEXT_IF_UNREPAIRED = "run350F_runtime_feature_tensor_snapshot_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_no_scaler_table_runtime_handoff_probe_only_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage350/run350E_no_scaler_table_probe"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage350_ONNXInterop__NoScalerTableRuntimeHandoff"
PARITY_TOLERANCE = 1.0e-4

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run350E_no_scaler_table_runtime_handoff_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage350E_no_scaler_table_runtime_handoff_probe.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN350D_DIR = STAGE_DIR / "02_runs" / "run350D"
RUN350D_FINAL = RUN350D_DIR / "final_decision.json"
RUN350D_GATES = RUN350D_DIR / "required_gate_coverage_audit.csv"
RUN350D_SYNC = RUN350D_DIR / "ea_compile_and_sync_manifest.json"

VARIANT_DESIGN = RUN_DIR / "no_scaler_table_variant_design.csv"
VARIANT_PACKAGE = RUN_DIR / "no_scaler_table_variant_package.csv"
THRESHOLD_SCREEN = RUN_DIR / "no_scaler_table_threshold_screen.csv"
PYTHON_PROBE = RUN_DIR / "python_no_scaler_table_probe.csv"
EXPECTED_TAPE = RUN_DIR / "expected_tape.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
SUMMARY_CSV = RUN_DIR / "no_scaler_table_runtime_summary.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
EA_SYNC_MANIFEST = RUN_DIR / "ea_compile_and_sync_manifest.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
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
    RUN350D_FINAL,
    RUN350D_GATES,
    RUN350D_SYNC,
    base.SOURCE_FEATURES,
    base.SOURCE_FEATURE_ORDER,
    ROOT / mt5.EA_SOURCE_PATH,
)

OUTPUT_FILES = (
    VARIANT_DESIGN,
    VARIANT_PACKAGE,
    THRESHOLD_SCREEN,
    PYTHON_PROBE,
    EXPECTED_TAPE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    STRATEGY_TESTER_REPORTS,
    RUNTIME_OUTPUT_COPY,
    PROXY_MT5_DIFF,
    SUMMARY_CSV,
    RUNTIME_IDENTITY,
    EA_SYNC_MANIFEST,
    EXPERIMENT_RECEIPT,
    DATA_INTEGRITY_RECEIPT,
    RUNTIME_PARITY_RECEIPT,
    ARTIFACT_LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_BOUNDARY_RECEIPT,
    NEXT_ACTION_QUEUE,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
)

fs_path = base.fs_path
exists = base.exists
required = base.required
ensure_parent = base.ensure_parent
rel = base.rel
sha256_file = base.sha256_file
write_json = base.write_json
write_csv = base.write_csv
read_csv_rows = base.read_csv_rows
read_json = base.read_json
append_or_replace_csv = base.append_or_replace_csv
write_bom_text = base.write_bom_text
append_text_once = base.append_text_once
to_float = base.to_float


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage350E no-scaler and table runtime handoff probe.")
    parser.add_argument("--terminal-path", default=str(base.source_pkg.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(base.source_pkg.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(base.source_pkg.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(base.source_pkg.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--metaeditor-path", default=str(base.source_pkg.DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--reuse-existing-outputs", action="store_true")
    return parser.parse_args()


def patch_base_globals() -> None:
    replacements: dict[str, Any] = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
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
        "VARIANT_DESIGN": VARIANT_DESIGN,
        "VARIANT_PACKAGE": VARIANT_PACKAGE,
        "THRESHOLD_SCREEN": THRESHOLD_SCREEN,
        "PYTHON_ONNX_PROBE": PYTHON_PROBE,
        "EXPECTED_TAPE": EXPECTED_TAPE,
        "TERMINAL_PROCESS_AUDIT": TERMINAL_PROCESS_AUDIT,
        "MT5_EXECUTION_RESULT": MT5_EXECUTION_RESULT,
        "STRATEGY_TESTER_REPORTS": STRATEGY_TESTER_REPORTS,
        "RUNTIME_OUTPUT_COPY": RUNTIME_OUTPUT_COPY,
        "PROXY_MT5_DIFF": PROXY_MT5_DIFF,
        "SUMMARY_CSV": SUMMARY_CSV,
        "RUNTIME_IDENTITY": RUNTIME_IDENTITY,
    }
    for key, value in replacements.items():
        setattr(base, key, value)


def gate_passed(path: Path) -> bool:
    _fields, rows = read_csv_rows(required(path))
    return bool(rows) and all(str(row.get("status", "")).lower() == "passed" for row in rows)


def compile_and_sync(args: argparse.Namespace) -> dict[str, Any]:
    payload = run350d.compile_and_sync_ea(Path(args.metaeditor_path), Path(args.terminal_data_root))
    payload["stage_id"] = STAGE_ID
    payload["run_id"] = RUN_ID
    payload["claim_boundary"] = CLAIM_BOUNDARY
    write_json(EA_SYNC_MANIFEST, payload)
    return payload


def load_research_inputs() -> tuple[pd.DataFrame, list[str], np.ndarray]:
    feature_order = list(base.run349e.load_feature_order())
    frame = base.load_research_frame(feature_order)
    x_all = frame.loc[:, feature_order].to_numpy(dtype=np.float32, copy=True)
    return frame, feature_order, x_all


def small_linear_params(frame: pd.DataFrame, feature_order: Sequence[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    mean, scale, weights, bias = run350d.small_linear_params(frame, feature_order)
    return mean.reshape(-1).astype(np.float32), scale.reshape(-1).astype(np.float32), weights, bias


def set_versions(model: Any) -> Any:
    return base.set_model_versions(model)


def build_no_scaler_model(path: Path, feature_count: int) -> None:
    weights = np.zeros((feature_count, 3), dtype=np.float32)
    weights[0, 0] = 0.100
    weights[1, 1] = 0.100
    weights[2, 2] = 0.100
    weights[3, 0] = -0.050
    weights[4, 2] = 0.050
    bias = np.asarray([0.25, 0.50, 0.25], dtype=np.float32)
    nodes = [
        helper.make_node("MatMul", ["float_input", "W"], ["linear_out"], name="no_scaler_matmul"),
        helper.make_node("Add", ["linear_out", "B"], ["probabilities"], name="no_scaler_bias"),
    ]
    initializers = [numpy_helper.from_array(weights, name="W"), numpy_helper.from_array(bias, name="B")]
    input_info, output_info = base.model_io([1, feature_count], [1, 3])
    graph = helper.make_graph(nodes, "stage350E_no_scaler_linear", [input_info], [output_info], initializer=initializers)
    ensure_parent(path)
    path.write_bytes(set_versions(helper.make_model(graph)).SerializeToString())


def build_sub_only_model(path: Path, frame: pd.DataFrame, feature_order: Sequence[str]) -> None:
    mean, _scale, weights, bias = small_linear_params(frame, feature_order)
    nodes = [
        helper.make_node("Sub", ["float_input", "scaler_mean"], ["centered"], name="center_features_1d"),
        helper.make_node("MatMul", ["centered", "W"], ["linear_out"], name="sub_only_matmul"),
        helper.make_node("Add", ["linear_out", "B"], ["probabilities"], name="sub_only_bias"),
    ]
    initializers = [
        numpy_helper.from_array(mean, name="scaler_mean"),
        numpy_helper.from_array(weights, name="W"),
        numpy_helper.from_array(bias, name="B"),
    ]
    input_info, output_info = base.model_io([1, len(feature_order)], [1, 3])
    graph = helper.make_graph(nodes, "stage350E_sub_only_linear", [input_info], [output_info], initializer=initializers)
    ensure_parent(path)
    path.write_bytes(set_versions(helper.make_model(graph)).SerializeToString())


def build_1d_scaler_model(path: Path, frame: pd.DataFrame, feature_order: Sequence[str]) -> None:
    mean, scale, weights, bias = small_linear_params(frame, feature_order)
    nodes = [
        helper.make_node("Sub", ["float_input", "scaler_mean"], ["centered"], name="center_features_1d"),
        helper.make_node("Div", ["centered", "scaler_scale"], ["scaled"], name="scale_features_1d"),
        helper.make_node("MatMul", ["scaled", "W"], ["linear_out"], name="one_d_scaler_matmul"),
        helper.make_node("Add", ["linear_out", "B"], ["probabilities"], name="one_d_scaler_bias"),
    ]
    initializers = [
        numpy_helper.from_array(mean, name="scaler_mean"),
        numpy_helper.from_array(scale, name="scaler_scale"),
        numpy_helper.from_array(weights, name="W"),
        numpy_helper.from_array(bias, name="B"),
    ]
    input_info, output_info = base.model_io([1, len(feature_order)], [1, 3])
    graph = helper.make_graph(nodes, "stage350E_1d_scaler_linear", [input_info], [output_info], initializer=initializers)
    ensure_parent(path)
    path.write_bytes(set_versions(helper.make_model(graph)).SerializeToString())


def write_feature_score_table(path: Path, feature_count: int) -> None:
    rows: list[dict[str, Any]] = []
    intercept = np.log(np.asarray([0.30, 0.40, 0.30], dtype=float))
    rows.append({"record_type": "intercept", "feature_index": -1, "item_index": 0, "value": 0.0, "score_short": intercept[0], "score_flat": intercept[1], "score_long": intercept[2]})
    for feature_index in range(feature_count):
        cut = 0.0 if feature_index == 0 else 1.0e9
        rows.append({"record_type": "cut", "feature_index": feature_index, "item_index": 0, "value": cut, "score_short": 0.0, "score_flat": 0.0, "score_long": 0.0})
        for item_index in range(3):
            if feature_index == 0 and item_index == 1:
                score = (0.25, -0.10, -0.15)
            elif feature_index == 0 and item_index == 2:
                score = (-0.25, -0.10, 0.25)
            else:
                score = (0.0, 0.0, 0.0)
            rows.append({"record_type": "score", "feature_index": feature_index, "item_index": item_index, "value": 0.0, "score_short": score[0], "score_flat": score[1], "score_long": score[2]})
    write_csv(path, rows)


def score_table_probabilities(x_all: np.ndarray) -> np.ndarray:
    intercept = np.log(np.asarray([0.30, 0.40, 0.30], dtype=float))
    logits = np.repeat(intercept.reshape(1, 3), x_all.shape[0], axis=0)
    negative_or_zero = x_all[:, 0] <= 0.0
    logits[negative_or_zero] += np.asarray([0.25, -0.10, -0.15])
    logits[~negative_or_zero] += np.asarray([-0.25, -0.10, 0.25])
    shifted = logits - logits.max(axis=1, keepdims=True)
    probs = np.exp(shifted)
    probs /= probs.sum(axis=1, keepdims=True)
    return probs.astype(np.float32)


def variant_definitions() -> list[dict[str, Any]]:
    return [
        {"attempt_name": "e00_array_no_scaler_linear", "builder": "no_scaler", "model_backend": "onnx", "input_container": "float_array", "use_matrix_tensor": False, "graph_mode": "matmul_add_no_scaler", "allow_trading": False, "purpose": "no_scaler_matmul_probe"},
        {"attempt_name": "e01_matrix_no_scaler_linear", "builder": "no_scaler", "model_backend": "onnx", "input_container": "matrixf", "use_matrix_tensor": True, "graph_mode": "matmul_add_no_scaler", "allow_trading": False, "purpose": "no_scaler_matrix_probe"},
        {"attempt_name": "e02_matrix_sub_only_linear", "builder": "sub_only", "model_backend": "onnx", "input_container": "matrixf", "use_matrix_tensor": True, "graph_mode": "sub_matmul_add_1d_mean", "allow_trading": False, "purpose": "sub_broadcast_probe"},
        {"attempt_name": "e03_matrix_1d_scaler_linear", "builder": "one_d_scaler", "model_backend": "onnx", "input_container": "matrixf", "use_matrix_tensor": True, "graph_mode": "sub_div_matmul_add_1d_scaler", "allow_trading": False, "purpose": "one_d_scaler_probe"},
        {"attempt_name": "e04_table_feature0_sign_surface", "builder": "feature0_score_table", "model_backend": "ebm_table", "input_container": "mql_feature_array", "use_matrix_tensor": False, "graph_mode": "mql_score_table_feature0_sign", "allow_trading": False, "purpose": "table_runtime_handoff_probe"},
    ]


def materialize_variants(frame: pd.DataFrame, feature_order: Sequence[str], x_all: np.ndarray) -> tuple[list[dict[str, Any]], dict[str, np.ndarray]]:
    variants: list[dict[str, Any]] = []
    probabilities: dict[str, np.ndarray] = {}
    probe_rows: list[dict[str, Any]] = []
    shared_paths: dict[str, Path] = {}
    for definition in variant_definitions():
        attempt_name = definition["attempt_name"]
        builder = definition["builder"]
        suffix = ".csv" if definition["model_backend"] == "ebm_table" else ".onnx"
        path = MODEL_DIR / f"{attempt_name}{suffix}"
        if builder == "no_scaler":
            if builder not in shared_paths:
                shared_paths[builder] = MODEL_DIR / "shared_no_scaler_linear.onnx"
                build_no_scaler_model(shared_paths[builder], len(feature_order))
            shutil.copy2(fs_path(shared_paths[builder]), fs_path(path))
            output = base.run_onnx_probabilities(path, x_all)
        elif builder == "sub_only":
            build_sub_only_model(path, frame, feature_order)
            output = base.run_onnx_probabilities(path, x_all)
        elif builder == "one_d_scaler":
            build_1d_scaler_model(path, frame, feature_order)
            output = base.run_onnx_probabilities(path, x_all)
        elif builder == "feature0_score_table":
            write_feature_score_table(path, len(feature_order))
            output = score_table_probabilities(x_all)
        else:
            raise ValueError(f"unsupported builder: {builder}")
        probabilities[attempt_name] = output
        row_sums = output.sum(axis=1)
        variant = {**definition, "model_path": path, "model_sha256": sha256_file(path), "source_model": "stage350E_diagnostic", "temperature": 1.0, "no_conversion": True, "set_output_shape": True}
        variants.append(variant)
        probe_rows.append(
            {
                "attempt_name": attempt_name,
                "builder": builder,
                "model_backend": definition["model_backend"],
                "input_container": definition["input_container"],
                "graph_mode": definition["graph_mode"],
                "model_path": rel(path),
                "model_sha256": sha256_file(path),
                "python_output_min": float(np.min(output)),
                "python_output_max": float(np.max(output)),
                "python_row_sum_min": float(np.min(row_sums)),
                "python_row_sum_max": float(np.max(row_sums)),
                "status": "passed" if np.all(np.isfinite(output)) else "failed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(VARIANT_DESIGN, variants)
    write_csv(PYTHON_PROBE, probe_rows)
    return variants, probabilities


def select_attempts(variants: Sequence[Mapping[str, Any]], screen_rows: Sequence[Mapping[str, Any]], common_files_root: Path) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for idx, variant in enumerate(variants, start=1):
        attempt_name = str(variant["attempt_name"])
        rows = [row for row in screen_rows if row["attempt_name"] == attempt_name and row["split"] == "all"]
        best = rows[0] if rows else {"long_threshold": 0.99, "short_threshold": 0.99, "q_long": "diagnostic", "q_short": "diagnostic", "signal_rows": 0}
        suffix = ".csv" if variant["model_backend"] == "ebm_table" else ".onnx"
        model_common_path = f"{COMMON_MODEL_DIR}/{attempt_name}{suffix}"
        common_model_abs = common_files_root / Path(model_common_path)
        ensure_parent(common_model_abs)
        shutil.copy2(fs_path(Path(variant["model_path"])), fs_path(common_model_abs))
        selected.append(
            {
                **variant,
                "model_id": f"stage350E_{attempt_name}",
                "model_path": rel(Path(variant["model_path"])),
                "model_common_path": model_common_path,
                "model_common_sha256": sha256_file(common_model_abs),
                "feature_csv_path": "Project_Obsidian_Prime_v2/stage348/run348C_onnx_short_carry_probe/features/runtime_features.csv",
                "feature_count": len(base.run349e.load_feature_order()),
                "feature_order_hash": "870630295e4a4f15a168230f75a27726e910d8ba141270e1b2140cdd4519ba0c",
                "long_threshold": float(best["long_threshold"]),
                "short_threshold": float(best["short_threshold"]),
                "q_long": best.get("q_long", "diagnostic"),
                "q_short": best.get("q_short", "diagnostic"),
                "proxy_signal_rows": best.get("signal_rows", 0),
                "from_date": "2024.07.30",
                "to_date": "2025.01.01",
                "tier": "Tier A",
                "split": "all_rows_train_selected_thresholds",
                "magic": 3510000 + idx,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return selected


def materialize_mt5_files(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        common_telemetry = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv"
        common_summary = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv"
        set_name = f"OPV2_run350E_{attempt_name}.set"
        ini_name = f"OPV2_run350E_{attempt_name}.ini"
        report_name = f"POPv2_run350E_{attempt_name}"
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
            "InpModelBackend": attempt["model_backend"],
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": bool(attempt["no_conversion"]),
            "InpSetOutputShape": bool(attempt["set_output_shape"]),
            "InpModelUseMatrixTensor": bool(attempt["use_matrix_tensor"]),
            "InpFeatureOrderHash": attempt["feature_order_hash"],
            "InpFallbackEnabled": False,
            "InpShortThreshold": float(attempt["short_threshold"]),
            "InpLongThreshold": float(attempt["long_threshold"]),
            "InpMinMargin": -1.0,
            "InpDecisionMode": "threshold_margin",
            "InpInvertSignal": False,
            "InpSideFilterEnabled": False,
            "InpAllowTrading": False,
            "InpFixedLot": 0.1,
            "InpMagic": int(attempt["magic"]),
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": common_telemetry,
            "InpSummaryCsvPath": common_summary,
        }
        set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
        cfg = mt5.TesterMaterializationConfig(shutdown_terminal=1, from_date=str(attempt["from_date"]), to_date=str(attempt["to_date"]), report=report_name)
        ini_payload = mt5.materialize_tester_ini_file(cfg, ini_path, set_file_path=Path(set_name))
        rows.append({**attempt, "set_name": set_name, "ini_name": ini_name, "set_path": rel(set_path), "ini_path": rel(ini_path), "set_sha256": set_payload["sha256"], "ini_sha256": ini_payload["sha256"], "common_telemetry_path": common_telemetry, "common_summary_path": common_summary, "report_name": report_name, "ini": {"tester": {"Report": report_name}}, "allowed_use": "MT5 runtime probe(MT5 런타임 탐침)", "forbidden_use": "candidate_selection_or_operating_claim(후보 선택 또는 운영 주장)", "claim_boundary": CLAIM_BOUNDARY})
    write_csv(VARIANT_PACKAGE, rows)
    return rows


def enrich_summary(summary_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_attempt = {str(row["attempt_name"]): row for row in attempts}
    enriched: list[dict[str, Any]] = []
    for row in summary_rows:
        attempt = by_attempt.get(str(row.get("attempt_name", "")), {})
        enriched.append({**dict(row), "model_backend": attempt.get("model_backend", ""), "input_container": attempt.get("input_container", ""), "builder": attempt.get("builder", ""), "purpose": attempt.get("purpose", "")})
    write_csv(SUMMARY_CSV, enriched)
    return enriched


def build_final(args: argparse.Namespace, compile_sync: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]], summary_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]], copy_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [row for row in summary_rows if str(row.get("runtime_status", "")) == "completed"]
    by_name = {row.get("attempt_name"): row for row in summary_rows}
    def passed(name: str) -> bool:
        return str(by_name.get(name, {}).get("probability_parity", "")).lower() == "true"
    no_scaler_pass = passed("e00_array_no_scaler_linear") or passed("e01_matrix_no_scaler_linear")
    sub_only_pass = passed("e02_matrix_sub_only_linear")
    one_d_scaler_pass = passed("e03_matrix_1d_scaler_linear")
    table_pass = passed("e04_table_feature0_sign_surface")
    compile_status = str(compile_sync.get("compile", {}).get("status", "missing"))
    if compile_status != "completed":
        status = "blocked_stage350E_metaeditor_compile_failed_no_selection"
        judgment = "blocked_no_scaler_table_probe_compile_failed"
        result_judgment = "blocked(차단)"
        decision = "stage350E_retry_after_compile_repair"
        next_run_id = RUN_ID
    elif len(completed) < len(attempts):
        status = "blocked_stage350E_runtime_outputs_missing_no_selection"
        judgment = "blocked_no_scaler_table_probe_mt5_outputs_missing_or_terminal_unavailable"
        result_judgment = "blocked(차단)"
        decision = "stage350E_retry_no_scaler_table_probe"
        next_run_id = RUN_ID
    elif one_d_scaler_pass or sub_only_pass or no_scaler_pass:
        status = "completed_stage350E_onnx_simplified_path_parity_passed_no_selection"
        judgment = "positive_runtime_repair_simplified_onnx_path_passed_scaler_broadcast_contract_is_suspect"
        result_judgment = "positive_runtime_repair_clue(긍정 런타임 수리 단서)"
        decision = "stage350E_open_run350F_rebuild_no_scaler_or_1d_scaler_onnx_trade_surface"
        next_run_id = NEXT_IF_ONNX_REPAIR
    elif table_pass:
        status = "completed_stage350E_table_runtime_parity_passed_onnx_paths_failed_no_selection"
        judgment = "positive_runtime_escape_hatch_table_runtime_passed_onnx_variable_paths_failed"
        result_judgment = "positive_runtime_escape_hatch(긍정 런타임 우회 단서)"
        decision = "stage350E_open_run350F_build_runtime_table_trade_surface_from_proxy_clues"
        next_run_id = NEXT_IF_TABLE_ONLY
    else:
        status = "completed_stage350E_no_scaler_and_table_paths_failed_no_selection"
        judgment = "negative_runtime_contract_no_scaler_table_and_1d_scaler_paths_failed_feature_tensor_snapshot_probe_required"
        result_judgment = "negative_runtime_contract(부정 런타임 계약)"
        decision = "stage350E_open_run350F_runtime_feature_tensor_snapshot_probe"
        next_run_id = NEXT_IF_UNREPAIRED
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "result_judgment": result_judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": len(attempts),
        "runtime_completed_rows": len(completed),
        "probability_parity_pass_rows": sum(1 for row in summary_rows if str(row.get("probability_parity", "")).lower() == "true"),
        "no_scaler_passed": no_scaler_pass,
        "sub_only_passed": sub_only_pass,
        "one_d_scaler_passed": one_d_scaler_pass,
        "table_runtime_passed": table_pass,
        "diff_rows": len(diff_rows),
        "runtime_output_copy_ready_rows": sum(1 for row in copy_rows if str(row.get("exists", "")).lower() == "true"),
        "compile_status": compile_status,
        "materialize_only": bool(args.materialize_only),
        "reuse_existing_outputs": bool(args.reuse_existing_outputs),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "forward_passed": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def make_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    def row(gate_id: str, passed: bool, evidence: str, effect: str) -> dict[str, Any]:
        return {"stage_id": STAGE_ID, "run_id": RUN_ID, "gate_id": gate_id, "status": "passed" if passed else "failed", "evidence": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY, "created_at_utc": now_utc()}
    summary_rows = pd.read_csv(fs_path(SUMMARY_CSV), encoding="utf-8-sig").to_dict("records") if exists(SUMMARY_CSV) else []
    completed_all = bool(summary_rows) and all(str(r.get("runtime_status", "")) == "completed" for r in summary_rows)
    input_hash_all = bool(summary_rows) and all(str(r.get("input_hash_parity", "")).lower() == "true" for r in summary_rows if int(float(r.get("rows_compared", 0) or 0)) > 0)
    return [
        row("parent_run350D_gate", gate_passed(RUN350D_GATES), rel(RUN350D_GATES), "Stage350D gate(게이트)가 닫혔다."),
        row("metaeditor_compile_gate", final.get("compile_status") == "completed" and exists(EA_SYNC_MANIFEST), rel(EA_SYNC_MANIFEST), "EA(전문가 자문)가 컴파일되고 동기화됐다."),
        row("runtime_evidence_gate", completed_all, rel(MT5_EXECUTION_RESULT), "MT5 runtime telemetry(MT5 런타임 기록)가 관찰됐다."),
        row("scope_completion_gate", bool(summary_rows) and len(summary_rows) == int(final.get("attempt_rows", 0)), rel(SUMMARY_CSV), "계획된 변형 범위가 완료됐다."),
        row("kpi_contract_audit", input_hash_all and exists(PROXY_MT5_DIFF), f"{rel(SUMMARY_CSV)};{rel(PROXY_MT5_DIFF)}", "입력 해시와 확률 차이를 행 단위로 비교했다."),
        row("artifact_lineage_recorded", exists(ARTIFACT_LINEAGE_RECEIPT) and exists(RUN_MANIFEST), f"{rel(ARTIFACT_LINEAGE_RECEIPT)};{rel(RUN_MANIFEST)}", "산출물 계보가 연결됐다."),
        row("tier_pair_rows_written", exists(STAGE_LEDGER) and exists(PROJECT_LEDGER), f"{rel(STAGE_LEDGER)};{rel(PROJECT_LEDGER)}", "Tier A/B/A+B 장부 행을 기록했다."),
        row("final_claim_guard", all(final.get(key) == "not_claimed" for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]), rel(FINAL_DECISION), "운영 주장을 닫아 두었다."),
    ]


def write_receipts(final: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]]) -> None:
    payload = {"stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": now_utc(), "claim_boundary": CLAIM_BOUNDARY}
    write_json(EXPERIMENT_RECEIPT, {**payload, "hypothesis": "If no-scaler or 1D-scaler ONNX passes, the run350C failure is scaler/broadcast related; if table runtime passes, MQL table handoff is a viable escape hatch.", "decision_use": "Choose simplified ONNX rebuild, table runtime trade surface, or deeper feature tensor snapshot.", "comparison_baseline": "run350D matrixf and Gemm paths both failed.", "control_variables": "Stage348 runtime_features, feature order, tester identity, date range, trading disabled.", "changed_variables": "no scaler, sub only, 1D scaler, table runtime.", "sample_scope": "FPMarkets US100 M5 Tier A Strategy Tester replay 2024.07.30 to 2025.01.01.", "success_criteria": "Any simplified ONNX or table runtime variant reaches row-level probability parity.", "failure_criteria": "All variants mismatch despite input hash parity.", "invalid_conditions": "compile failure, timestamp drift, input hash mismatch, missing runtime output.", "stop_conditions": "parity path found or all paths fail.", "evidence_plan": [rel(SUMMARY_CSV), rel(PROXY_MT5_DIFF), rel(EA_SYNC_MANIFEST)]})
    write_json(DATA_INTEGRITY_RECEIPT, {**payload, "data_source": rel(base.SOURCE_FEATURES), "time_axis": "bar_time_server is broker-clock close key(브로커 시계 닫힘 키).", "sample_scope": "US100 M5 Tier A runtime feature rows.", "missing_or_duplicate_check": "Timestamp-matched feature-ready rows are compared.", "feature_label_boundary": "No labels are used; this is deterministic runtime interop.", "split_boundary": "Diagnostic replay only, not promotion split.", "leakage_risk": "Low for runtime interop; no training selection occurs.", "data_hash_or_identity": {"feature_csv": sha256_file(base.SOURCE_FEATURES), "feature_order": sha256_file(base.SOURCE_FEATURE_ORDER)}, "integrity_judgment": "usable_with_boundary"})
    write_json(RUNTIME_PARITY_RECEIPT, {**payload, "research_path": rel(PYTHON_PROBE), "runtime_path": rel(VARIANT_PACKAGE), "shared_contract": "feature order 53, output [p_short,p_flat,p_long], trading disabled.", "known_differences": "ONNX variants use COpModelRuntime; table variant uses COpEbmTableRuntime.", "parity_check": rel(SUMMARY_CSV), "parity_identity": rel(RUNTIME_IDENTITY), "runtime_claim_boundary": "runtime_probe(런타임 탐침)"})
    write_json(JUDGMENT_RECEIPT, {**payload, "result_judgment": final["result_judgment"], "status": final["status"], "decision": final["decision"], "next_run_id": final["next_run_id"], "forbidden_claims": ["candidate_selection", "forward_passed", "live_readiness", "operating_promotion", "runtime_authority", "goal_achieve"]})
    write_json(ARTIFACT_LINEAGE_RECEIPT, {**payload, "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": final["next_run_id"], "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha256_file(path) for path in OUTPUT_FILES if exists(path) and path.is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "tracked", "lineage_judgment": "connected_with_boundary"})
    write_json(CLAIM_BOUNDARY_RECEIPT, {**payload, "allowed_claims": ["runtime_probe", "interop_attribution"], "forbidden_claims": ["candidate_selection", "forward_passed", "live_readiness", "operating_promotion", "runtime_authority", "goal_achieve"], "goal_achieve": "not_claimed"})


def write_final_manifest(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> None:
    payload = dict(final)
    payload["gate_passes"] = sum(1 for gate in gates if gate.get("status") == "passed")
    payload["gate_total"] = len(gates)
    write_json(FINAL_DECISION, payload)
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": now_utc(), "parent_run_id": PARENT_RUN_ID, "attempts": attempts, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)], "gates": rel(GATE_AUDIT), "final_decision": rel(FINAL_DECISION), "claim_boundary": CLAIM_BOUNDARY})


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run350E No Scaler Table Runtime Handoff Probe(350E 스케일러 없음 테이블 런타임 인계 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- result_judgment(결과 판정): `{final['result_judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- probability_parity_pass_rows(확률 동등성 통과 행): `{final['probability_parity_pass_rows']}`
- no_scaler_passed(스케일러 없음 통과): `{final['no_scaler_passed']}`
- sub_only_passed(Sub 전용 통과): `{final['sub_only_passed']}`
- one_d_scaler_passed(1D 스케일러 통과): `{final['one_d_scaler_passed']}`
- table_runtime_passed(테이블 런타임 통과): `{final['table_runtime_passed']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`

Action(행동): run350E(350E 실행)는 no-scaler ONNX(스케일러 없음 온엑스), 1D scaler ONNX(1차원 스케일러 온엑스), table runtime(테이블 런타임)을 MT5에서 비교했다.

Effect(효과): scaler/broadcast(스케일러/브로드캐스트) 문제와 ONNX 우회(table runtime, 테이블 런타임) 가능성을 분리했다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    decision = f"""# Stage350E Decision(350E 결정)

- decision(결정): `{final['decision']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`
- judgment(판정): `{final['judgment']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): no-scaler/table runtime(스케일러 없음/테이블 런타임) 분리 판정을 기록했다.

Effect(효과): 다음 실행은 수리된 경로만 모델 표면(model surface, 모델 표면) 탐색으로 넘긴다.
"""
    current = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{final['status']}`
- current_judgment(현재 판정): `{final['judgment']}`
- current_decision(현재 결정): `{final['decision']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): run350E(350E 실행)는 no-scaler/table runtime(스케일러 없음/테이블 런타임) 경로를 MT5에서 검증했다.

Effect(효과): 다음 작업은 수리 가능 경로 또는 더 좁은 feature tensor snapshot(피처 텐서 스냅샷)으로 이동한다.
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
    append_text_once(STAGE_BRIEF, "## run350E No Scaler Table Runtime Handoff Probe", f"""## run350E No Scaler Table Runtime Handoff Probe(350E 스케일러 없음 테이블 런타임 인계 탐침)

- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- judgment(판정): `{final['judgment']}`
- no_scaler_passed(스케일러 없음 통과): `{final['no_scaler_passed']}`
- table_runtime_passed(테이블 런타임 통과): `{final['table_runtime_passed']}`
""")
    changelog = f"""## {TODAY} run350E No Scaler Table Runtime Handoff Probe

- action(행동): no-scaler ONNX(스케일러 없음 온엑스), 1D scaler ONNX(1차원 스케일러 온엑스), table runtime(테이블 런타임) 변형 `{final['attempt_rows']}`개를 MT5 Strategy Tester(MT5 전략 테스터)로 실행했다.
- effect(효과): no_scaler_passed(스케일러 없음 통과) `{final['no_scaler_passed']}`, table_runtime_passed(테이블 런타임 통과) `{final['table_runtime_passed']}`, next(다음) `{final['next_run_id']}`를 기록했다.
"""
    append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run350E No Scaler Table Runtime Handoff Probe", changelog)
    append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run350E No Scaler Table Runtime Handoff Probe", changelog)


def write_registers(final: Mapping[str, Any]) -> None:
    write_bom_text(WORKSPACE_STATE, "\n".join([f"current_stage_id: {STAGE_ID}", f"current_run_id: {final['next_run_id']}", f"latest_completed_run_id: {RUN_ID}", f"current_status: {final['status']}", f"current_judgment: {final['judgment']}", f"current_decision: {final['decision']}", f"next_run_id: {final['next_run_id']}", f"claim_boundary: {CLAIM_BOUNDARY}", f"updated_at: {TODAY}", ""]))
    run_row = {"run_id": RUN_ID, "stage_id": STAGE_ID, "run_number": RUN_NUMBER, "parent_run_id": PARENT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "result_judgment": final["result_judgment"], "decision": final["decision"], "next_run_id": final["next_run_id"], "report_path": rel(REPORT_PATH), "final_decision_path": rel(FINAL_DECISION), "gate_audit_path": rel(GATE_AUDIT), "created_at": TODAY, "claim_boundary": CLAIM_BOUNDARY, "attempt_count": final["attempt_rows"], "runtime_completed_rows": final["runtime_completed_rows"], "probability_parity_pass_rows": final["probability_parity_pass_rows"]}
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    ledger_base = {"stage_id": STAGE_ID, "run_id": RUN_ID, "run_number": RUN_NUMBER, "status": final["status"], "judgment": final["judgment"], "result_judgment": final["result_judgment"], "report_path": rel(REPORT_PATH), "final_decision_path": rel(FINAL_DECISION), "claim_boundary": CLAIM_BOUNDARY, "created_at": TODAY, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "next_run_id": final["next_run_id"], "primary_kpi": f"no_scaler_passed={final['no_scaler_passed']};table_runtime_passed={final['table_runtime_passed']}", "guardrail_kpi": "no_trading_diagnostic_run(거래 없음 진단 실행)"}
    rows = [
        {**ledger_base, "ledger_row_id": f"{RUN_ID}__Tier A", "subrun_id": "Tier A", "view": "Tier A used(Tier A 사용)", "record_view": "Tier A used(Tier A 사용)", "tier": "Tier A", "tier_scope": "Tier A", "metric_scope": "no_scaler_table_runtime_probe", "kpi_scope": "MT5 runtime telemetry(MT5 런타임 텔레메트리)"},
        {**ledger_base, "ledger_row_id": f"{RUN_ID}__Tier B", "subrun_id": "Tier B", "view": "Tier B fallback used(Tier B 대체 사용)", "record_view": "Tier B fallback used(Tier B 대체 사용)", "tier": "Tier B", "tier_scope": "Tier B", "metric_scope": "missing_required", "kpi_scope": "missing_required", "result_status": "missing_required(필수 누락)"},
        {**ledger_base, "ledger_row_id": f"{RUN_ID}__Tier A+B", "subrun_id": "Tier A+B", "view": "Tier A+B combined(Tier A+B 합산)", "record_view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "tier_scope": "Tier A+B", "metric_scope": "same_as_tier_a_until_tier_b_available", "kpi_scope": "same_as_tier_a_until_tier_b_available"},
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)


def update_artifact_registry() -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path):
            rows.append({"artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}", "stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": path.suffix.lstrip(".") or "artifact", "path": rel(path), "artifact_path": rel(path), "sha256": sha256_file(path) if path.is_file() else "", "created_at": TODAY, "created_at_utc": now_utc(), "claim_boundary": CLAIM_BOUNDARY})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def validate(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    missing = [rel(path) for path in [FINAL_DECISION, RUN_MANIFEST, GATE_AUDIT, REPORT_PATH, SUMMARY_CSV, EXPECTED_TAPE, VARIANT_PACKAGE, EA_SYNC_MANIFEST] if not exists(path)]
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
        os.makedirs(fs_path(directory), exist_ok=True)
    for path in INPUT_FILES:
        required(path)
    args = parse_args()
    compile_sync = compile_and_sync(args)
    frame, feature_order, x_all = load_research_inputs()
    variants, probability_by_attempt = materialize_variants(frame, feature_order, x_all)
    screen_rows = base.screen_thresholds(frame, variants, probability_by_attempt)
    attempts = select_attempts(variants, screen_rows, Path(args.common_files_root))
    base.write_expected_tape(frame, attempts, probability_by_attempt)
    attempts = materialize_mt5_files(attempts)
    execution_results, report_records, copy_rows = base.execute_attempts(args, attempts)
    summary_rows, diff_rows = base.compare_outputs(attempts, execution_results, report_records)
    summary_rows = enrich_summary(summary_rows, attempts)
    base.write_runtime_identity(args, attempts)
    final_seed = build_final(args, compile_sync, attempts, summary_rows, diff_rows, copy_rows)
    write_receipts(final_seed, attempts)
    write_csv(NEXT_ACTION_QUEUE, [{"queue_id": final_seed["next_run_id"], "stage_id": STAGE_ID, "source_run_id": RUN_ID, "priority": 1, "action": "continue_from_no_scaler_table_probe", "effect": "Use simplified ONNX or table runtime result to choose next runtime-safe path.", "claim_boundary": CLAIM_BOUNDARY}])
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
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "judgment": final["judgment"], "result_judgment": final["result_judgment"], "attempts": final["attempt_rows"], "runtime_completed_rows": final["runtime_completed_rows"], "probability_parity_pass_rows": final["probability_parity_pass_rows"], "no_scaler_passed": final["no_scaler_passed"], "sub_only_passed": final["sub_only_passed"], "one_d_scaler_passed": final["one_d_scaler_passed"], "table_runtime_passed": final["table_runtime_passed"], "gates": f"{final['gate_passes']}/{final['gate_total']}", "goal_achieve": final["goal_achieve"], "next_run_id": final["next_run_id"]}, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
