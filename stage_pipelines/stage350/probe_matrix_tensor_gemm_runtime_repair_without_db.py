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
import onnx
import pandas as pd
from onnx import TensorProto, helper, numpy_helper


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage350 import (  # noqa: E402
    probe_onnx_operator_ladder_runtime_contract_without_db as run350c,
)
from stage_pipelines.stage350 import (  # noqa: E402
    probe_softmax_output_shape_and_conversion_semantics_without_db as base,
)


TODAY = "2026-06-01"
STAGE_ID = "350_onnx_runtime_interop__softmax_output_shape_repair_probe"
RUN_NUMBER = "run350D"
RUN_ID = "run350D_build_gemm_safe_or_table_runtime_model_family_pivot_without_db_v1"
PARENT_RUN_ID = run350c.RUN_ID
NEXT_IF_REPAIRED = "run350E_rebuild_runtime_compatible_onnx_trade_surface_with_matrix_tensor_without_db_v1"
NEXT_IF_UNREPAIRED = "run350E_table_runtime_or_feature_tensor_handoff_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_matrix_tensor_gemm_runtime_repair_probe_only_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage350/run350D_matrix_tensor_gemm_probe"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage350_ONNXInterop__MatrixTensorGemmRepair"
PARITY_TOLERANCE = 1.0e-4

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run350D_matrix_tensor_gemm_runtime_repair_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage350D_matrix_tensor_gemm_runtime_repair_probe.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN350C_DIR = STAGE_DIR / "02_runs" / "run350C"
RUN350C_FINAL = RUN350C_DIR / "final_decision.json"
RUN350C_GATES = RUN350C_DIR / "required_gate_coverage_audit.csv"
RUN350C_SUMMARY = RUN350C_DIR / "operator_ladder_runtime_contract_summary.csv"
RUN350C_C03_MODEL = RUN350C_DIR / "models" / "c03_small_linear_variable.onnx"

VARIANT_DESIGN = RUN_DIR / "matrix_tensor_gemm_variant_design.csv"
VARIANT_PACKAGE = RUN_DIR / "matrix_tensor_gemm_variant_package.csv"
THRESHOLD_SCREEN = RUN_DIR / "matrix_tensor_gemm_threshold_screen.csv"
PYTHON_ONNX_PROBE = RUN_DIR / "python_onnx_matrix_tensor_gemm_probe.csv"
EXPECTED_TAPE = RUN_DIR / "expected_tape.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
SUMMARY_CSV = RUN_DIR / "matrix_tensor_gemm_runtime_summary.csv"
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
    RUN350C_FINAL,
    RUN350C_GATES,
    RUN350C_SUMMARY,
    RUN350C_C03_MODEL,
    base.RUN349E_E02_ONNX,
    base.SOURCE_FEATURES,
    base.SOURCE_FEATURE_ORDER,
    ROOT / mt5.EA_SOURCE_PATH,
    ROOT / "foundation" / "mt5" / "include" / "ObsidianPrime" / "ModelRuntime.mqh",
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
to_int = base.to_int


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage350D matrix tensor and Gemm runtime repair probe.")
    parser.add_argument("--terminal-path", default=str(base.source_pkg.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(base.source_pkg.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(base.source_pkg.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(base.source_pkg.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--reuse-existing-outputs", action="store_true")
    parser.add_argument("--metaeditor-path", default=str(base.source_pkg.DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"))
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
        "PYTHON_ONNX_PROBE": PYTHON_ONNX_PROBE,
        "EXPECTED_TAPE": EXPECTED_TAPE,
        "TERMINAL_PROCESS_AUDIT": TERMINAL_PROCESS_AUDIT,
        "MT5_EXECUTION_RESULT": MT5_EXECUTION_RESULT,
        "STRATEGY_TESTER_REPORTS": STRATEGY_TESTER_REPORTS,
        "RUNTIME_OUTPUT_COPY": RUNTIME_OUTPUT_COPY,
        "PROXY_MT5_DIFF": PROXY_MT5_DIFF,
        "SUMMARY_CSV": SUMMARY_CSV,
        "RUNTIME_IDENTITY": RUNTIME_IDENTITY,
        "GATE_AUDIT": GATE_AUDIT,
        "FINAL_DECISION": FINAL_DECISION,
        "RUN_MANIFEST": RUN_MANIFEST,
    }
    for key, value in replacements.items():
        setattr(base, key, value)


def gate_passed(path: Path) -> bool:
    _fields, rows = read_csv_rows(required(path))
    return bool(rows) and all(str(row.get("status", "")).lower() == "passed" for row in rows)


def compile_and_sync_ea(metaeditor_path: Path, terminal_data_root: Path) -> dict[str, Any]:
    compile_log = MT5_DIR / "matrix_tensor_compile.log"
    source_dir = ROOT / "foundation" / "mt5"
    source_ea = ROOT / mt5.EA_SOURCE_PATH
    source_ex5 = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
    include_src = source_dir / "include"
    target_dir = terminal_data_root / "MQL5" / "Experts" / "Project_Obsidian_Prime_v2" / "foundation" / "mt5"
    terminal_root = terminal_data_root.resolve()
    resolved_target = target_dir.resolve()
    if not str(resolved_target).lower().startswith(str(terminal_root).lower()):
        raise RuntimeError(f"portable_target_outside_terminal_root:{resolved_target}")

    compile_payload = mt5.compile_mql5_ea(metaeditor_path, source_ea, compile_log)
    sync_rows: list[dict[str, Any]] = []
    os.makedirs(fs_path(target_dir), exist_ok=True)
    for src, name in ((source_ea, "ea_source"), (source_ex5, "ea_binary")):
        dst = target_dir / src.name
        if not exists(src):
            sync_rows.append({"artifact": name, "source": rel(src), "target": dst.as_posix(), "status": "missing_source"})
            continue
        shutil.copy2(fs_path(src), fs_path(dst))
        sync_rows.append(
            {
                "artifact": name,
                "source": rel(src),
                "target": dst.as_posix(),
                "status": "copied",
                "sha256": sha256_file(dst),
            }
        )
    include_dst = target_dir / "include"
    shutil.copytree(fs_path(include_src), fs_path(include_dst), dirs_exist_ok=True)
    sync_rows.append(
        {
            "artifact": "ea_include_tree",
            "source": rel(include_src),
            "target": include_dst.as_posix(),
            "status": "copied",
            "sha256": "tree_copied_hashes_recorded_in_runtime_identity",
        }
    )
    payload = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": now_utc(),
        "compile": compile_payload,
        "sync_rows": sync_rows,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(EA_SYNC_MANIFEST, payload)
    return payload


def load_research_inputs() -> tuple[pd.DataFrame, list[str], np.ndarray]:
    feature_order = list(base.run349e.load_feature_order())
    frame = base.load_research_frame(feature_order)
    x_all = frame.loc[:, feature_order].to_numpy(dtype=np.float32, copy=True)
    return frame, feature_order, x_all


def small_linear_params(frame: pd.DataFrame, feature_order: Sequence[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x = frame.loc[:, list(feature_order)].to_numpy(dtype=np.float32, copy=True)
    mean = np.mean(x, axis=0, keepdims=True).astype(np.float32)
    scale = np.std(x, axis=0, keepdims=True).astype(np.float32)
    scale[scale < 1.0e-6] = 1.0
    weights = np.zeros((len(feature_order), 3), dtype=np.float32)
    weights[0, 0] = 0.005
    weights[1, 1] = 0.005
    weights[2, 2] = 0.005
    weights[3, 0] = -0.003
    weights[4, 2] = 0.003
    bias = np.asarray([0.25, 0.50, 0.25], dtype=np.float32)
    return mean, scale, weights, bias


def build_gemm_small_linear_model(path: Path, frame: pd.DataFrame, feature_order: Sequence[str]) -> None:
    mean, scale, weights, bias = small_linear_params(frame, feature_order)
    nodes = [
        helper.make_node("Sub", ["float_input", "scaler_mean"], ["centered"], name="center_features"),
        helper.make_node("Div", ["centered", "scaler_scale"], ["scaled"], name="scale_features"),
        helper.make_node("Gemm", ["scaled", "W", "B"], ["probabilities"], name="small_linear_gemm", alpha=1.0, beta=1.0, transB=0),
    ]
    initializers = [
        numpy_helper.from_array(mean, name="scaler_mean"),
        numpy_helper.from_array(scale, name="scaler_scale"),
        numpy_helper.from_array(weights, name="W"),
        numpy_helper.from_array(bias, name="B"),
    ]
    input_info, output_info = base.model_io([1, len(feature_order)], [1, 3])
    graph = helper.make_graph(nodes, "stage350D_gemm_small_linear_contract", [input_info], [output_info], initializer=initializers)
    model = base.set_model_versions(helper.make_model(graph))
    ensure_parent(path)
    path.write_bytes(model.SerializeToString())


def variant_definitions() -> list[dict[str, Any]]:
    return [
        {
            "attempt_name": "d00_array_matmul_small_linear",
            "source_model": "c03_small_linear_variable",
            "builder": "small_linear_matmul",
            "graph_mode": "sub_div_matmul_add_variable_output",
            "input_container": "float_array",
            "use_matrix_tensor": False,
            "allow_trading": False,
            "purpose": "current_array_contract_recheck",
        },
        {
            "attempt_name": "d01_matrix_matmul_small_linear",
            "source_model": "c03_small_linear_variable",
            "builder": "small_linear_matmul",
            "graph_mode": "sub_div_matmul_add_variable_output",
            "input_container": "matrixf",
            "use_matrix_tensor": True,
            "allow_trading": False,
            "purpose": "matrix_tensor_repair_probe",
        },
        {
            "attempt_name": "d02_array_gemm_small_linear",
            "source_model": "diagnostic_gemm_small_linear",
            "builder": "small_linear_gemm",
            "graph_mode": "sub_div_gemm_variable_output",
            "input_container": "float_array",
            "use_matrix_tensor": False,
            "allow_trading": False,
            "purpose": "gemm_operator_probe_array",
        },
        {
            "attempt_name": "d03_matrix_gemm_small_linear",
            "source_model": "diagnostic_gemm_small_linear",
            "builder": "small_linear_gemm",
            "graph_mode": "sub_div_gemm_variable_output",
            "input_container": "matrixf",
            "use_matrix_tensor": True,
            "allow_trading": False,
            "purpose": "gemm_operator_probe_matrix",
        },
        {
            "attempt_name": "d04_array_e02_softmax_temp64",
            "source_model": "e02_mlp_histgbm_distill_q95",
            "builder": "e02_softmax_temp64",
            "graph_mode": "full_mlp_softmax_temp64",
            "input_container": "float_array",
            "use_matrix_tensor": False,
            "allow_trading": False,
            "purpose": "full_mlp_array_recheck",
        },
        {
            "attempt_name": "d05_matrix_e02_softmax_temp64",
            "source_model": "e02_mlp_histgbm_distill_q95",
            "builder": "e02_softmax_temp64",
            "graph_mode": "full_mlp_softmax_temp64",
            "input_container": "matrixf",
            "use_matrix_tensor": True,
            "allow_trading": False,
            "purpose": "full_mlp_matrix_repair_probe",
        },
    ]


def materialize_variants(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    x_all: np.ndarray,
) -> tuple[list[dict[str, Any]], dict[str, np.ndarray]]:
    variants: list[dict[str, Any]] = []
    probabilities: dict[str, np.ndarray] = {}
    probe_rows: list[dict[str, Any]] = []
    shared_paths: dict[str, Path] = {}
    for definition in variant_definitions():
        attempt_name = str(definition["attempt_name"])
        builder = str(definition["builder"])
        path = MODEL_DIR / f"{attempt_name}.onnx"
        if builder == "small_linear_matmul":
            if builder not in shared_paths:
                shared_paths[builder] = MODEL_DIR / "shared_small_linear_matmul.onnx"
                run350c.build_small_linear_model(shared_paths[builder], frame, feature_order)
            shutil.copy2(fs_path(shared_paths[builder]), fs_path(path))
        elif builder == "small_linear_gemm":
            if builder not in shared_paths:
                shared_paths[builder] = MODEL_DIR / "shared_small_linear_gemm.onnx"
                build_gemm_small_linear_model(shared_paths[builder], frame, feature_order)
            shutil.copy2(fs_path(shared_paths[builder]), fs_path(path))
        elif builder == "e02_softmax_temp64":
            if builder not in shared_paths:
                shared_paths[builder] = MODEL_DIR / "shared_e02_softmax_temp64.onnx"
                run350c.build_e02_logits_model(shared_paths[builder], temperature=64.0, softmax=True, feature_count=len(feature_order))
            shutil.copy2(fs_path(shared_paths[builder]), fs_path(path))
        else:
            raise ValueError(f"unsupported builder: {builder}")
        output = base.run_onnx_probabilities(path, x_all)
        row_sums = output.sum(axis=1)
        probabilities[attempt_name] = output
        variant = {
            **definition,
            "model_path": path,
            "model_sha256": sha256_file(path),
            "temperature": 64.0 if builder == "e02_softmax_temp64" else 1.0,
            "no_conversion": True,
            "set_output_shape": True,
        }
        variants.append(variant)
        probe_rows.append(
            {
                "attempt_name": attempt_name,
                "builder": builder,
                "graph_mode": definition["graph_mode"],
                "input_container": definition["input_container"],
                "use_matrix_tensor": definition["use_matrix_tensor"],
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
    write_csv(PYTHON_ONNX_PROBE, probe_rows)
    return variants, probabilities


def select_attempts(
    variants: Sequence[Mapping[str, Any]],
    screen_rows: Sequence[Mapping[str, Any]],
    common_files_root: Path,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for idx, variant in enumerate(variants, start=1):
        attempt_name = str(variant["attempt_name"])
        rows = [row for row in screen_rows if row["attempt_name"] == attempt_name and row["split"] == "all"]
        best = rows[0] if rows else {"long_threshold": 0.99, "short_threshold": 0.99, "q_long": "diagnostic", "q_short": "diagnostic", "signal_rows": 0}
        model_common_path = f"{COMMON_MODEL_DIR}/{attempt_name}.onnx"
        common_model_abs = common_files_root / Path(model_common_path)
        ensure_parent(common_model_abs)
        shutil.copy2(fs_path(Path(variant["model_path"])), fs_path(common_model_abs))
        selected.append(
            {
                **variant,
                "model_id": f"stage350D_{attempt_name}",
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
                "magic": 3509000 + idx,
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
        set_name = f"OPV2_run350D_{attempt_name}.set"
        ini_name = f"OPV2_run350D_{attempt_name}.ini"
        report_name = f"POPv2_run350D_{attempt_name}"
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
        set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
        cfg = mt5.TesterMaterializationConfig(shutdown_terminal=1, from_date=str(attempt["from_date"]), to_date=str(attempt["to_date"]), report=report_name)
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
                "forbidden_use": "candidate_selection_or_operating_claim(후보 선택 또는 운영 주장)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(VARIANT_PACKAGE, rows)
    return rows


def enrich_summary(summary_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_attempt = {str(row["attempt_name"]): row for row in attempts}
    enriched: list[dict[str, Any]] = []
    for row in summary_rows:
        attempt = by_attempt.get(str(row.get("attempt_name", "")), {})
        enriched.append(
            {
                **dict(row),
                "input_container": attempt.get("input_container", ""),
                "use_matrix_tensor": attempt.get("use_matrix_tensor", ""),
                "builder": attempt.get("builder", ""),
                "purpose": attempt.get("purpose", ""),
            }
        )
    write_csv(SUMMARY_CSV, enriched)
    return enriched


def build_final(
    args: argparse.Namespace,
    compile_sync: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
    summary_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    completed = [row for row in summary_rows if str(row.get("runtime_status", "")) == "completed"]
    passed = [row for row in summary_rows if str(row.get("probability_parity", "")).lower() == "true"]
    by_name = {row.get("attempt_name"): row for row in summary_rows}
    d00_pass = str(by_name.get("d00_array_matmul_small_linear", {}).get("probability_parity", "")).lower() == "true"
    d01_pass = str(by_name.get("d01_matrix_matmul_small_linear", {}).get("probability_parity", "")).lower() == "true"
    d03_pass = str(by_name.get("d03_matrix_gemm_small_linear", {}).get("probability_parity", "")).lower() == "true"
    d05_pass = str(by_name.get("d05_matrix_e02_softmax_temp64", {}).get("probability_parity", "")).lower() == "true"
    compile_status = str(compile_sync.get("compile", {}).get("status", "missing"))
    if compile_status != "completed":
        status = "blocked_stage350D_metaeditor_compile_failed_no_selection"
        judgment = "blocked_matrix_tensor_runtime_repair_compile_failed"
        result_judgment = "blocked(차단)"
        decision = "stage350D_retry_after_compile_repair"
        next_run_id = RUN_ID
    elif len(completed) < len(attempts):
        status = "blocked_stage350D_runtime_outputs_missing_no_selection"
        judgment = "blocked_matrix_tensor_gemm_probe_mt5_outputs_missing_or_terminal_unavailable"
        result_judgment = "blocked(차단)"
        decision = "stage350D_retry_matrix_tensor_gemm_probe"
        next_run_id = RUN_ID
    elif d01_pass and not d00_pass:
        status = "completed_stage350D_matrix_tensor_repair_verified_no_selection"
        judgment = "positive_runtime_repair_matrixf_tensor_restores_variable_matmul_probability_parity_no_selection"
        result_judgment = "positive_runtime_repair_clue(긍정 런타임 수리 단서)"
        decision = "stage350D_open_run350E_rebuild_runtime_compatible_onnx_trade_surface_with_matrix_tensor"
        next_run_id = NEXT_IF_REPAIRED
    elif d01_pass:
        status = "completed_stage350D_variable_matmul_parity_passed_after_module_repair_no_selection"
        judgment = "positive_runtime_repair_variable_matmul_probability_parity_passed_requires_full_trade_surface_probe"
        result_judgment = "positive_runtime_repair_clue(긍정 런타임 수리 단서)"
        decision = "stage350D_open_run350E_rebuild_runtime_compatible_onnx_trade_surface_with_matrix_tensor"
        next_run_id = NEXT_IF_REPAIRED
    elif d03_pass:
        status = "completed_stage350D_gemm_matrix_path_parity_passed_matmul_unrepaired_no_selection"
        judgment = "positive_runtime_repair_gemm_matrix_path_passed_matmul_path_still_failed"
        result_judgment = "positive_runtime_repair_clue(긍정 런타임 수리 단서)"
        decision = "stage350D_open_run350E_build_gemm_safe_onnx_trade_surface"
        next_run_id = NEXT_IF_REPAIRED
    else:
        status = "completed_stage350D_matrix_tensor_and_gemm_paths_failed_no_selection"
        judgment = "negative_runtime_contract_matrix_tensor_and_gemm_repair_failed_table_runtime_or_handoff_probe_required"
        result_judgment = "negative_runtime_contract(부정 런타임 계약)"
        decision = "stage350D_open_run350E_table_runtime_or_feature_tensor_handoff_probe"
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
        "probability_parity_pass_rows": len(passed),
        "array_matmul_passed": d00_pass,
        "matrix_matmul_passed": d01_pass,
        "matrix_gemm_passed": d03_pass,
        "matrix_full_mlp_passed": d05_pass,
        "diff_rows": len(diff_rows),
        "runtime_output_copy_ready_rows": sum(1 for row in copy_rows if str(row.get("exists", "")).lower() == "true"),
        "compile_status": compile_status,
        "compile_log_path": compile_sync.get("compile", {}).get("log_path", ""),
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

    summary_rows = pd.read_csv(fs_path(SUMMARY_CSV), encoding="utf-8-sig").to_dict("records") if exists(SUMMARY_CSV) else []
    completed_all = bool(summary_rows) and all(str(r.get("runtime_status", "")) == "completed" for r in summary_rows)
    input_hash_all = bool(summary_rows) and all(str(r.get("input_hash_parity", "")).lower() == "true" for r in summary_rows if int(float(r.get("rows_compared", 0) or 0)) > 0)
    return [
        row("parent_run350C_gate", gate_passed(RUN350C_GATES), rel(RUN350C_GATES), "Stage350C gate(게이트)가 닫혔다."),
        row("metaeditor_compile_gate", final.get("compile_status") == "completed" and exists(EA_SYNC_MANIFEST), rel(EA_SYNC_MANIFEST), "EA module change(EA 모듈 변경)가 컴파일되고 동기화됐다."),
        row("runtime_evidence_gate", completed_all, rel(MT5_EXECUTION_RESULT), "MT5 runtime telemetry(MT5 런타임 기록)가 모든 변형에서 관찰됐다."),
        row("scope_completion_gate", bool(summary_rows) and len(summary_rows) == int(final.get("attempt_rows", 0)), rel(SUMMARY_CSV), "계획된 변형 범위가 요약됐다."),
        row("kpi_contract_audit", input_hash_all and exists(PROXY_MT5_DIFF), f"{rel(SUMMARY_CSV)};{rel(PROXY_MT5_DIFF)}", "입력 해시와 확률 차이를 행 단위로 비교했다."),
        row("required_gate_coverage_audit", exists(GATE_AUDIT), rel(GATE_AUDIT), "필수 게이트 커버리지(coverage, 범위)를 기록했다."),
        row("artifact_lineage_recorded", exists(ARTIFACT_LINEAGE_RECEIPT) and exists(RUN_MANIFEST), f"{rel(ARTIFACT_LINEAGE_RECEIPT)};{rel(RUN_MANIFEST)}", "산출물 계보가 연결됐다."),
        row("tier_pair_rows_written", exists(STAGE_LEDGER) and exists(PROJECT_LEDGER), f"{rel(STAGE_LEDGER)};{rel(PROJECT_LEDGER)}", "Tier A/B/A+B 장부 행을 기록했다."),
        row("final_claim_guard", all(final.get(key) == "not_claimed" for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]), rel(FINAL_DECISION), "운영 주장을 닫아 두었다."),
    ]


def write_receipts(final: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]]) -> None:
    base_payload = {"stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": now_utc(), "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base_payload,
            "hypothesis": "MT5 ONNX mismatch begins when variable input tensors are passed as flat float arrays; matrixf input may restore probability parity.",
            "decision_use": "Choose matrixf ONNX rebuild, GEMM-safe graph, or table runtime pivot.",
            "comparison_baseline": "run350C variable_matmul_add failed while constant and zero-weight variants passed.",
            "control_variables": "Stage348 runtime_features, feature order, date range, tester profile, thresholds, trading disabled.",
            "changed_variables": "input container float_array vs matrixf, MatMul vs Gemm, small linear vs full MLP softmax temp64.",
            "sample_scope": "FPMarkets US100 M5 Tier A Strategy Tester replay 2024.07.30 to 2025.01.01.",
            "success_criteria": "matrixf small-linear or GEMM path reaches row-level probability parity with input hash parity.",
            "failure_criteria": "matrixf and GEMM variants still mismatch or runtime telemetry is missing.",
            "invalid_conditions": "timestamp drift, input hash mismatch, missing compile, missing tester reports, or stale EA binary.",
            "stop_conditions": "repair path identified, all repair paths fail, or MT5 execution blocks.",
            "evidence_plan": [rel(SUMMARY_CSV), rel(PROXY_MT5_DIFF), rel(EA_SYNC_MANIFEST), rel(RUNTIME_IDENTITY)],
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            **base_payload,
            "data_source": rel(base.SOURCE_FEATURES),
            "time_axis": "bar_time_server is broker-clock close key(브로커 시계 닫힘 키); timestamp_utc is comparison metadata(비교 메타데이터).",
            "sample_scope": "US100 M5, 2024.07.30 to 2025.01.01, Tier A runtime feature rows.",
            "missing_or_duplicate_check": "Inherited from run350C source feature handoff; this run checks timestamp-matched runtime rows.",
            "feature_label_boundary": "No labels are used for this diagnostic; features are closed-bar runtime_features only.",
            "split_boundary": "all_rows_train_selected_thresholds is diagnostic replay scope, not promotion split.",
            "leakage_risk": "Low for this probe because outputs are deterministic operator checks, not training selection.",
            "data_hash_or_identity": {"feature_csv": sha256_file(base.SOURCE_FEATURES), "feature_order": sha256_file(base.SOURCE_FEATURE_ORDER)},
            "integrity_judgment": "usable_with_boundary",
        },
    )
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            **base_payload,
            "research_path": rel(PYTHON_ONNX_PROBE),
            "runtime_path": rel(VARIANT_PACKAGE),
            "shared_contract": "feature order 53, output [p_short,p_flat,p_long], ONNX input shape [1,feature_count], trading disabled.",
            "known_differences": "d00/d02/d04 use flat float array; d01/d03/d05 use matrixf input/output path.",
            "parity_check": rel(SUMMARY_CSV),
            "parity_identity": rel(RUNTIME_IDENTITY),
            "primary_source_note": "MQL5 OnnxRun reference examples use matrixf input and vectorf output for shaped tensors.",
            "runtime_claim_boundary": "runtime_probe(런타임 탐침)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base_payload,
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
            **base_payload,
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
            **base_payload,
            "allowed_claims": ["runtime_probe", "runtime_repair_clue", "operator_container_attribution"],
            "forbidden_claims": ["candidate_selection", "forward_passed", "live_readiness", "operating_promotion", "runtime_authority", "goal_achieve"],
            "goal_achieve": "not_claimed",
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
    report = f"""# run350D Matrix Tensor Gemm Runtime Repair Probe(350D 행렬 텐서 Gemm 런타임 수리 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- result_judgment(결과 판정): `{final['result_judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- probability_parity_pass_rows(확률 동등성 통과 행): `{final['probability_parity_pass_rows']}`
- array_matmul_passed(배열 MatMul 통과): `{final['array_matmul_passed']}`
- matrix_matmul_passed(행렬 MatMul 통과): `{final['matrix_matmul_passed']}`
- matrix_gemm_passed(행렬 Gemm 통과): `{final['matrix_gemm_passed']}`
- matrix_full_mlp_passed(행렬 전체 MLP 통과): `{final['matrix_full_mlp_passed']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`

Action(행동): run350D(350D 실행)는 float array(부동소수 배열)와 matrixf(부동소수 행렬) 입력 컨테이너를 MatMul(행렬곱), Gemm(일반 행렬곱), full MLP(전체 다층 퍼셉트론) 변형에서 MT5 Strategy Tester(MT5 전략 테스터)로 비교했다.

Effect(효과): run350C(350C 실행)의 variable_matmul_add(가변 행렬곱+더하기) 실패가 입력 컨테이너 문제인지, ONNX operator(온엑스 연산자) 문제인지 분리했다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    decision = f"""# Stage350D Decision(350D 결정)

- decision(결정): `{final['decision']}`
- next_run_id(다음 실행 ID): `{final['next_run_id']}`
- judgment(판정): `{final['judgment']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): matrix tensor/Gemm(행렬 텐서/Gemm) 수리 경로를 MT5 runtime evidence(MT5 런타임 근거)로 판정했다.

Effect(효과): 다음 실행은 수리된 ONNX trade surface(온엑스 거래 표면) 재구축 또는 table runtime(테이블 런타임) 분기로 간다.
"""
    current = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{final['status']}`
- current_judgment(현재 판정): `{final['judgment']}`
- current_decision(현재 결정): `{final['decision']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): run350D(350D 실행)는 matrixf input/output(행렬 입력/출력)과 Gemm(일반 행렬곱) 경로를 MT5에서 검증했다.

Effect(효과): 다음 작업은 runtime parity(런타임 동등성)가 확인된 경로만 수익 모델 탐색으로 넘긴다.
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
        "## run350D Matrix Tensor Gemm Runtime Repair Probe",
        f"""## run350D Matrix Tensor Gemm Runtime Repair Probe(350D 행렬 텐서 Gemm 런타임 수리 탐침)

- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{final['next_run_id']}`
- judgment(판정): `{final['judgment']}`
- matrix_matmul_passed(행렬 MatMul 통과): `{final['matrix_matmul_passed']}`
- matrix_gemm_passed(행렬 Gemm 통과): `{final['matrix_gemm_passed']}`
""",
    )
    changelog = f"""## {TODAY} run350D Matrix Tensor Gemm Runtime Repair Probe

- action(행동): matrixf input/output(행렬 입력/출력), float array(부동소수 배열), Gemm(일반 행렬곱) ONNX 변형 `{final['attempt_rows']}`개를 MT5 Strategy Tester(MT5 전략 테스터)로 실행했다.
- effect(효과): matrix_matmul_passed(행렬 MatMul 통과) `{final['matrix_matmul_passed']}`, matrix_gemm_passed(행렬 Gemm 통과) `{final['matrix_gemm_passed']}`, next(다음) `{final['next_run_id']}`를 기록했다.
"""
    append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run350D Matrix Tensor Gemm Runtime Repair Probe", changelog)
    append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run350D Matrix Tensor Gemm Runtime Repair Probe", changelog)


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
        "probability_parity_pass_rows": final["probability_parity_pass_rows"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    ledger_base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "status": final["status"],
        "judgment": final["judgment"],
        "result_judgment": final["result_judgment"],
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at": TODAY,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "next_run_id": final["next_run_id"],
        "primary_kpi": f"matrix_matmul_passed={final['matrix_matmul_passed']};matrix_gemm_passed={final['matrix_gemm_passed']}",
        "guardrail_kpi": "no_trading_diagnostic_run(거래 없음 진단 실행)",
    }
    rows = [
        {**ledger_base, "ledger_row_id": f"{RUN_ID}__Tier A", "subrun_id": "Tier A", "view": "Tier A used(Tier A 사용)", "record_view": "Tier A used(Tier A 사용)", "tier": "Tier A", "tier_scope": "Tier A", "metric_scope": "matrix_tensor_gemm_runtime_probe", "kpi_scope": "MT5 runtime telemetry(MT5 런타임 텔레메트리)"},
        {**ledger_base, "ledger_row_id": f"{RUN_ID}__Tier B", "subrun_id": "Tier B", "view": "Tier B fallback used(Tier B 대체 사용)", "record_view": "Tier B fallback used(Tier B 대체 사용)", "tier": "Tier B", "tier_scope": "Tier B", "metric_scope": "missing_required", "kpi_scope": "missing_required", "result_status": "missing_required(필수 누락)"},
        {**ledger_base, "ledger_row_id": f"{RUN_ID}__Tier A+B", "subrun_id": "Tier A+B", "view": "Tier A+B combined(Tier A+B 합산)", "record_view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "tier_scope": "Tier A+B", "metric_scope": "same_as_tier_a_until_tier_b_available", "kpi_scope": "same_as_tier_a_until_tier_b_available"},
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
    compile_sync = compile_and_sync_ea(Path(args.metaeditor_path), Path(args.terminal_data_root))
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
    write_csv(NEXT_ACTION_QUEUE, [{"queue_id": final_seed["next_run_id"], "stage_id": STAGE_ID, "source_run_id": RUN_ID, "priority": 1, "action": "continue_from_matrix_tensor_gemm_repair_probe", "effect": "Use matrix tensor or GEMM repair result to choose next runtime-safe ONNX path.", "claim_boundary": CLAIM_BOUNDARY}])
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
                "array_matmul_passed": final["array_matmul_passed"],
                "matrix_matmul_passed": final["matrix_matmul_passed"],
                "matrix_gemm_passed": final["matrix_gemm_passed"],
                "matrix_full_mlp_passed": final["matrix_full_mlp_passed"],
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
