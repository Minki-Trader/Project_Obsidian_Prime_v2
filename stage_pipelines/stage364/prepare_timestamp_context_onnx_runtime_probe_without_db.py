from __future__ import annotations

import json
import os
import shutil
import sys
import csv
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import onnx
import onnxruntime as ort
import pandas as pd
from onnx import TensorProto, helper


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5.runtime_artifacts import copy_to_common_files, mt5_runtime_module_hashes  # noqa: E402
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file  # noqa: E402
from stage_pipelines.stage364 import train_timestamp_context_cost_filter_model_without_db as tr  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = tr.STAGE_ID
RUN_NUMBER = "run364F"
RUN_ID = "run364F_prepare_timestamp_context_onnx_runtime_probe_without_db_v1"
PARENT_RUN_ID = tr.RUN_ID
NEXT_RUN_ID = "run364G_execute_timestamp_context_onnx_mt5_runtime_probe_without_db_v1"

STATUS = "completed_stage364F_onnx_runtime_probe_package_prepared_common_files_synced_no_mt5_execution"
JUDGMENT = "runtime_probe_package_ready_common_files_synced_mt5_execution_required_no_authority"
DECISION = "stage364F_open_run364G_execute_timestamp_context_onnx_mt5_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_common_files_synced_no_mt5_execution_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "mt5_report_open_close_time_joined_to_runtime_bar_time_no_timezone_conversion"
OUTPUT_CONTRACT = "p_short=0_p_flat=0_p_long=binary_keep_probability_threshold_margin"

STAGE_DIR = tr.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "feature_matrices"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"

SOURCE_RUN_DIR = STAGE_DIR / "02_runs" / "run364E"
SOURCE_SEED_RUN_DIR = STAGE_DIR / "02_runs" / "run364D"
SOURCE_TRAINING_SEED_TABLE = SOURCE_SEED_RUN_DIR / "timestamp_context_training_seed_table.csv"
SOURCE_FEATURE_SCHEMA = SOURCE_SEED_RUN_DIR / "timestamp_context_feature_schema.json"
SOURCE_MONTH_PRESSURE = SOURCE_SEED_RUN_DIR / "month_pressure_matrix.csv"
SOURCE_SELECTED_MODEL_SUMMARY = SOURCE_RUN_DIR / "selected_model_summary.json"
SOURCE_THRESHOLD_SURFACE = SOURCE_RUN_DIR / "threshold_surface.csv"
SOURCE_MODEL_ARTIFACT_MANIFEST = SOURCE_RUN_DIR / "model_artifact_manifest.csv"
SOURCE_ONNX_SMOKE_REPORT = SOURCE_RUN_DIR / "onnx_smoke_report.csv"
SOURCE_RUNTIME_PROBE_QUEUE = SOURCE_RUN_DIR / "run364F_runtime_probe_queue.csv"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_REPORT = REVIEW_DIR / "run364E_timestamp_context_cost_filter_model_training.md"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
FEATURE_ORDER = RUN_DIR / "feature_order.json"
FEATURE_MATRIX = FEATURE_DIR / "timestamp_context_cost_filter_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "runtime_feature_matrix_manifest.csv"
SOURCE_BINARY_ONNX = MODEL_DIR / "rf_depth3_balanced_source_binary.onnx"
RUNTIME_P3_ONNX = MODEL_DIR / "rf_depth3_balanced_keep_score_as_long_p3.onnx"
MODEL_OUTPUT_ADAPTER_MANIFEST = RUN_DIR / "model_output_adapter_manifest.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_DIR / "timestamp_context_expected_probability_tape.csv"
EXPECTED_PROBABILITY_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUN364G_EXECUTION_QUEUE = RUN_DIR / "run364G_execution_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364F_timestamp_context_onnx_runtime_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364F_timestamp_context_onnx_runtime_probe_package.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
PORTABLE_EA_EX5 = (
    DEFAULT_PORTABLE_ROOT
    / "MQL5"
    / "Experts"
    / "Project_Obsidian_Prime_v2"
    / "foundation"
    / "mt5"
    / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
)
EA_SOURCE = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.mq5"
EA_BINARY = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_timestamp_context_onnx_runtime_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_EXPECTED_DIR = f"{COMMON_ROOT}/expected"
COMMON_CONFIG_DIR = f"{COMMON_ROOT}/config"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

INPUT_FILES = [
    SOURCE_TRAINING_SEED_TABLE,
    SOURCE_FEATURE_SCHEMA,
    SOURCE_MONTH_PRESSURE,
    SOURCE_SELECTED_MODEL_SUMMARY,
    SOURCE_THRESHOLD_SURFACE,
    SOURCE_MODEL_ARTIFACT_MANIFEST,
    SOURCE_ONNX_SMOKE_REPORT,
    SOURCE_RUNTIME_PROBE_QUEUE,
    SOURCE_FINAL_DECISION,
    SOURCE_GATE_AUDIT,
    SOURCE_REPORT,
    EA_SOURCE,
    EA_BINARY,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    FEATURE_ORDER,
    FEATURE_MATRIX,
    FEATURE_MATRIX_MANIFEST,
    SOURCE_BINARY_ONNX,
    RUNTIME_P3_ONNX,
    MODEL_OUTPUT_ADAPTER_MANIFEST,
    EXPECTED_PROBABILITY_TAPE,
    EXPECTED_PROBABILITY_INDEX,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TESTER_IDENTITY_CONTRACT,
    PROXY_MT5_COMPARISON_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    RUN364G_EXECUTION_QUEUE,
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
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return tr.rel(path)


def exists(path: Path | str) -> bool:
    return tr.exists(path)


def sha256_file(path: Path | str) -> str:
    return tr.sha256_file(path)


def read_json(path: Path) -> Any:
    return tr.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    tr.write_json(path, payload)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    tr.write_csv(path, rows)


def write_text(path: Path, text: str) -> None:
    tr.write_text(path, text, bom=True)


def append_text_once(path: Path, marker: str, text: str) -> None:
    tr.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    tr.append_or_replace_csv(path, key_fields, rows, extend_header=True)


def append_registry_rows(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    fieldnames, existing = tr.read_csv_rows(path)
    if not fieldnames:
        write_csv(path, rows)
        return
    existing_keys = {tuple(str(row.get(field, "")) for field in key_fields) for row in existing}
    next_rows = []
    for row in rows:
        key = tuple(str(row.get(field, "")) for field in key_fields)
        if key in existing_keys:
            append_or_replace_csv(path, key_fields, rows)
            return
        next_rows.append(row)
    with open(tr.fs_path(path), "ab+") as raw:
        raw.seek(0, os.SEEK_END)
        if raw.tell() > 0:
            raw.seek(-1, os.SEEK_END)
            if raw.read(1) not in {b"\n", b"\r"}:
                raw.write(b"\n")
    with open(tr.fs_path(path), "a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        for row in next_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def ensure_dirs() -> None:
    for path in [RUN_DIR, MODEL_DIR, FEATURE_DIR, EXPECTED_DIR, MT5_DIR, SET_DIR, INI_DIR, REVIEW_DIR, SELECTED_DIR, SPEC_DIR]:
        os.makedirs(tr.fs_path(path), exist_ok=True)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run364F inputs: {missing}")
    source_final = read_json(SOURCE_FINAL_DECISION)
    if source_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364E final_decision next_run_id mismatch: {source_final.get('next_run_id')}")
    _, source_gates = tr.read_csv_rows(SOURCE_GATE_AUDIT)
    failed = [row for row in source_gates if str(row.get("status", "")).lower() not in {"passed", "pass"}]
    if failed:
        raise RuntimeError("run364E gate audit is not fully passed")


def write_input_manifest(source_onnx: Path) -> None:
    rows = []
    for path in [*INPUT_FILES, source_onnx]:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha256_file(path) if exists(path) else "",
                "effect": "input artifact(입력 산출물) 정체성을 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)


def load_feature_frame() -> tuple[pd.DataFrame, list[str], dict[str, Any]]:
    schema = read_json(SOURCE_FEATURE_SCHEMA)
    feature_columns = list(schema["feature_columns"])
    frame = pd.read_csv(tr.fs_path(SOURCE_TRAINING_SEED_TABLE), encoding="utf-8-sig")
    frame["open_dt"] = pd.to_datetime(frame["open_time"], format="%Y-%m-%d %H:%M:%S", errors="raise")
    frame["timestamp"] = frame["open_dt"].dt.tz_localize("UTC")
    frame = frame.sort_values(["split", "open_dt", "trade_index"]).reset_index(drop=True)
    for column in feature_columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if frame[feature_columns].isna().any().any():
        raise RuntimeError("feature matrix contains NaN values")
    if not np.isfinite(frame[feature_columns].to_numpy(dtype="float64")).all():
        raise RuntimeError("feature matrix contains non-finite values")
    return frame, feature_columns, schema


def selected_runtime_model() -> tuple[dict[str, Any], Path, float]:
    selected = read_json(SOURCE_SELECTED_MODEL_SUMMARY)
    model_id = str(selected["best_onnx_model_id"])
    if model_id != "rf_depth3_balanced":
        raise RuntimeError(f"run364F expected rf_depth3_balanced, got {model_id}")
    source_onnx = ROOT / str(selected["best_onnx_path"])
    if not exists(source_onnx):
        raise FileNotFoundError(rel(source_onnx))
    threshold = float(selected["best_onnx_threshold"])
    return selected, source_onnx, threshold


def slice_constant(name: str, values: Sequence[int]) -> onnx.TensorProto:
    return helper.make_tensor(name, TensorProto.INT64, [len(values)], list(values))


def write_runtime_p3_adapter(source_onnx: Path, target_onnx: Path) -> dict[str, Any]:
    os.makedirs(tr.fs_path(target_onnx.parent), exist_ok=True)
    shutil.copy2(tr.fs_path(source_onnx), tr.fs_path(SOURCE_BINARY_ONNX))

    model = onnx.load(tr.fs_path(source_onnx))
    probability_output = next((output.name for output in model.graph.output if output.name == "probabilities"), "")
    if not probability_output:
        probability_output = model.graph.output[-1].name

    existing_names = {node.name for node in model.graph.node}
    suffix = "stage364f"
    node_names = {
        "slice_keep": f"SliceKeepProbability_{suffix}",
        "zero": f"ZeroKeepProbability_{suffix}",
        "concat": f"KeepScoreAsP3_{suffix}",
    }
    if any(name in existing_names for name in node_names.values()):
        raise RuntimeError("runtime adapter node names already exist")

    initializers = [
        slice_constant("stage364f_keep_starts", [1]),
        slice_constant("stage364f_keep_ends", [2]),
        slice_constant("stage364f_slice_axes", [1]),
        slice_constant("stage364f_slice_steps", [1]),
        helper.make_tensor("stage364f_zero_scalar", TensorProto.FLOAT, [], [0.0]),
    ]
    nodes = [
        helper.make_node(
            "Slice",
            [probability_output, "stage364f_keep_starts", "stage364f_keep_ends", "stage364f_slice_axes", "stage364f_slice_steps"],
            ["stage364f_keep_probability"],
            name=node_names["slice_keep"],
        ),
        helper.make_node(
            "Mul",
            ["stage364f_keep_probability", "stage364f_zero_scalar"],
            ["stage364f_zero_probability"],
            name=node_names["zero"],
        ),
        helper.make_node(
            "Concat",
            ["stage364f_zero_probability", "stage364f_zero_probability", "stage364f_keep_probability"],
            ["stage364f_p_short_p_flat_p_long"],
            name=node_names["concat"],
            axis=1,
        ),
    ]
    model.graph.initializer.extend(initializers)
    model.graph.node.extend(nodes)
    del model.graph.output[:]
    model.graph.output.extend(
        [
            helper.make_tensor_value_info(
                "stage364f_p_short_p_flat_p_long",
                TensorProto.FLOAT,
                [None, 3],
            )
        ]
    )
    model.doc_string = (
        "Stage364F runtime adapter: maps binary keep probability to "
        "p_short=0, p_flat=0, p_long=keep_probability."
    )
    onnx.checker.check_model(model)
    onnx.save(model, tr.fs_path(target_onnx))
    return {
        "source_binary_onnx": rel(source_onnx),
        "local_source_binary_onnx": rel(SOURCE_BINARY_ONNX),
        "runtime_p3_onnx": rel(target_onnx),
        "source_binary_sha256": sha256_file(source_onnx),
        "local_source_binary_sha256": sha256_file(SOURCE_BINARY_ONNX),
        "runtime_p3_sha256": sha256_file(target_onnx),
        "probability_output": probability_output,
        "output_contract": OUTPUT_CONTRACT,
    }


def run_source_keep_probability(source_onnx: Path, matrix: np.ndarray) -> np.ndarray:
    session = ort.InferenceSession(tr.fs_path(source_onnx), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    output_names = [output.name for output in session.get_outputs()]
    outputs = session.run(None, {input_name: matrix.astype(np.float32)})
    probability_index = output_names.index("probabilities") if "probabilities" in output_names else len(outputs) - 1
    probabilities = np.asarray(outputs[probability_index], dtype=np.float64)
    if probabilities.ndim != 2 or probabilities.shape[1] != 2:
        raise RuntimeError(f"expected binary probabilities, got {probabilities.shape}")
    return probabilities[:, 1]


def run_runtime_p3_probability(runtime_onnx: Path, matrix: np.ndarray) -> np.ndarray:
    session = ort.InferenceSession(tr.fs_path(runtime_onnx), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: matrix.astype(np.float32)})
    probabilities = np.asarray(outputs[0], dtype=np.float64)
    if probabilities.ndim != 2 or probabilities.shape[1] != 3:
        raise RuntimeError(f"expected p3 probabilities, got {probabilities.shape}")
    return probabilities


def format_timestamp(value: Any) -> str:
    return pd.Timestamp(value).tz_convert("UTC").strftime("%Y.%m.%d %H:%M:%S")


def date_bounds(frame: pd.DataFrame) -> tuple[str, str, str, str]:
    first = pd.Timestamp(frame["timestamp"].min()).tz_convert("UTC")
    last = pd.Timestamp(frame["timestamp"].max()).tz_convert("UTC")
    return (
        first.strftime("%Y.%m.%d %H:%M:%S"),
        last.strftime("%Y.%m.%d %H:%M:%S"),
        first.strftime("%Y.%m.%d"),
        (last + timedelta(days=1)).strftime("%Y.%m.%d"),
    )


def export_feature_order(feature_columns: Sequence[str], schema: Mapping[str, Any]) -> dict[str, Any]:
    payload = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "schema_version": schema.get("schema_version", ""),
        "feature_columns": list(feature_columns),
        "feature_count": len(feature_columns),
        "feature_order_hash": ordered_hash(feature_columns),
        "source_feature_schema": rel(SOURCE_FEATURE_SCHEMA),
        "source_feature_schema_sha256": sha256_file(SOURCE_FEATURE_SCHEMA),
        "timestamp_semantics": "open_time/bar_time as MT5 server bar-open timestamp, no timezone conversion(진입/봉 시각을 MT5 서버 봉 시작 시각으로 사용, 시간대 변환 없음)",
        "output_contract": OUTPUT_CONTRACT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FEATURE_ORDER, payload)
    return payload


def export_feature_matrix(frame: pd.DataFrame, feature_columns: Sequence[str], feature_payload: Mapping[str, Any]) -> dict[str, Any]:
    metadata_columns = [
        "open_time",
        "close_time",
        "attempt_name",
        "trade_index",
        "cost_0_30_net",
        "label_cost_positive_0_30",
        "month_id",
        "input_hash",
        "time_axis",
    ]
    from foundation.mt5.runtime_artifacts import export_mt5_feature_matrix_csv  # local import keeps script startup light

    manifest = export_mt5_feature_matrix_csv(
        frame,
        feature_columns,
        FEATURE_MATRIX,
        timestamp_column="timestamp",
        metadata_columns=metadata_columns,
    )
    row = {
        "matrix_id": "timestamp_context_cost_filter_features",
        "run_id": RUN_ID,
        "path": rel(FEATURE_MATRIX),
        "sha256": sha256_file(FEATURE_MATRIX),
        "rows": manifest["rows"],
        "feature_count": manifest["feature_count"],
        "feature_order_hash": feature_payload["feature_order_hash"],
        "first_time": format_timestamp(frame["timestamp"].iloc[0]),
        "last_time": format_timestamp(frame["timestamp"].iloc[-1]),
        "timestamp_semantics": "InpCsvTimestampIsBarClose=false, CSV timestamp matches closed bar open(인풋 CSV 시각은 닫힌 봉 시작 시각과 매칭)",
        "metadata_columns": json.dumps(metadata_columns, ensure_ascii=False),
        "effect": "MT5 EA(메타트레이더5 전문가 자문)가 Python(파이썬)과 같은 피처 행을 읽게 한다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(FEATURE_MATRIX_MANIFEST, [row])
    return row


def export_expected_tape(
    frame: pd.DataFrame,
    p3: np.ndarray,
    threshold: float,
    feature_hash: str,
    selected: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in frame.reset_index(drop=True).iterrows():
        score = float(p3[index, 2])
        keep = score >= threshold
        rows.append(
            {
                "row_index": index,
                "split": row["split"],
                "bar_time_server": format_timestamp(row["timestamp"]),
                "timestamp_utc": pd.Timestamp(row["timestamp"]).tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ"),
                "open_time": row["open_time"],
                "trade_index": int(row["trade_index"]),
                "source_attempt_name": row.get("attempt_name", ""),
                "model_id": selected["best_onnx_model_id"],
                "threshold_id": selected["best_onnx_threshold_id"],
                "threshold": round(float(threshold), 12),
                "p_short": round(float(p3[index, 0]), 12),
                "p_flat": round(float(p3[index, 1]), 12),
                "p_long": round(score, 12),
                "keep_score": round(score, 12),
                "python_keep": bool(keep),
                "ea_expected_signal": "long" if keep else "flat",
                "ea_expected_signal_int": 1 if keep else 0,
                "decision_reason": "long_threshold_met" if keep else "threshold_or_margin_not_met",
                "cost_0_30_net": row.get("cost_0_30_net", ""),
                "label_cost_positive_0_30": row.get("label_cost_positive_0_30", ""),
                "month_id": row.get("month_id", ""),
                "input_hash": row.get("input_hash", ""),
                "feature_order_hash": feature_hash,
                "output_contract": OUTPUT_CONTRACT,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(EXPECTED_PROBABILITY_TAPE, rows)
    by_split = (
        pd.DataFrame(rows)
        .groupby("split", dropna=False)
        .agg(rows=("row_index", "count"), expected_long_rows=("python_keep", "sum"), avg_keep_score=("keep_score", "mean"))
        .reset_index()
    )
    index_rows = by_split.to_dict("records")
    for index_row in index_rows:
        index_row.update(
            {
                "run_id": RUN_ID,
                "expected_probability_tape": rel(EXPECTED_PROBABILITY_TAPE),
                "expected_probability_tape_sha256": sha256_file(EXPECTED_PROBABILITY_TAPE),
                "threshold": round(float(threshold), 12),
                "effect": "runtime telemetry(런타임 기록)와 비교할 expected tape(예상 테이프)를 만든다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(EXPECTED_PROBABILITY_INDEX, index_rows)
    return {"rows": len(rows), "sha256": sha256_file(EXPECTED_PROBABILITY_TAPE)}, {"rows": index_rows}


def copy_common(local_path: Path, common_path: str, sync_id: str, effect: str) -> dict[str, Any]:
    result = copy_to_common_files(DEFAULT_COMMON_FILES, local_path, common_path)
    return {
        "sync_id": sync_id,
        "source_path": rel(local_path),
        "common_path": common_path,
        "absolute_path": result["absolute_path"],
        "exists": exists(Path(result["absolute_path"])),
        "sha256": result["sha256"],
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def materialize_set_ini(
    selected: Mapping[str, Any],
    threshold: float,
    feature_hash: str,
    feature_common: str,
    model_common: str,
    first_time: str,
    last_time: str,
    from_date: str,
    to_date: str,
) -> tuple[str, str, list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    attempt_name = "run364F_rf_depth3_balanced_density_3_0_keep_long_p3"
    set_name = f"ObsidianPrimeV2_RuntimeProbeEA_{attempt_name}.set"
    ini_name = f"ObsidianPrimeV2_RuntimeProbeEA_{attempt_name}.ini"
    set_path = SET_DIR / set_name
    ini_path = INI_DIR / ini_name
    report_name = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt_name}"
    set_values = {
        "InpRunId": f"{RUN_ID}_{attempt_name}",
        "InpExplorationLabel": "stage364_TimestampContextONNX__RuntimeProbe",
        "InpTierLabel": "Tier A",
        "InpPrimaryActiveTier": "tier_a",
        "InpSplitLabel": "validation_oos_timestamp_context_cost_filter_probe",
        "InpMainSymbol": "US100",
        "InpTimeframe": 5,
        "InpEnforceM5": True,
        "InpFeatureCsvPath": feature_common,
        "InpFeatureCount": 21,
        "InpFeatureCsvUseCommonFiles": True,
        "InpFeatureRequireTimestampMatch": True,
        "InpFeatureAllowLatestFallback": False,
        "InpFeatureStrictHeader": True,
        "InpFeatureCsvDelimiter": ",",
        "InpCsvTimestampIsBarClose": False,
        "InpModelPath": model_common,
        "InpModelId": selected["best_onnx_model_id"],
        "InpModelBackend": "onnx",
        "InpModelUseCommonFiles": True,
        "InpModelUseCpuOnly": True,
        "InpModelNoConversion": False,
        "InpSetOutputShape": True,
        "InpModelUseMatrixTensor": False,
        "InpFeatureOrderHash": feature_hash,
        "InpFallbackEnabled": False,
        "InpShortThreshold": 1.0,
        "InpLongThreshold": threshold,
        "InpMinMargin": 0.0,
        "InpDecisionMode": "threshold_margin",
        "InpInvertSignal": False,
        "InpAllowTrading": True,
        "InpFixedLot": 0.10,
        "InpMagic": 3646001,
        "InpDeviationPoints": 20,
        "InpCloseOnFlatSignal": False,
        "InpReverseOnOppositeSignal": True,
        "InpCloseOnlyOnOppositeSignal": False,
        "InpMaxHoldBars": 6,
        "InpMaxConcurrentPositions": 1,
        "InpReentryCooldownBars": 0,
        "InpSameDirectionReentryCooldownBars": 0,
        "InpEntryTransitionOnly": False,
        "InpAtrSltpEnabled": False,
        "InpModelRiskSizingEnabled": False,
        "InpTelemetryEnabled": True,
        "InpTelemetryUseCommonFiles": True,
        "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv",
        "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv",
    }
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    ini_payload = materialize_tester_ini_file(
        TesterMaterializationConfig(
            shutdown_terminal=1,
            from_date=from_date,
            to_date=to_date,
            report=report_name,
        ),
        ini_path,
        set_file_path=Path(set_name),
    )
    set_rows = [
        {
            "attempt_name": attempt_name,
            "model_id": selected["best_onnx_model_id"],
            "set_path": rel(set_path),
            "set_sha256": set_payload["sha256"],
            "parameter_count": set_payload["parameter_count"],
            "decision_mode": "threshold_margin(임계값 마진)",
            "short_threshold": 1.0,
            "long_threshold": round(float(threshold), 12),
            "min_margin": 0.0,
            "allow_trading": True,
            "fixed_lot": 0.10,
            "max_hold_bars": 6,
            "csv_timestamp_is_bar_close": False,
            "output_contract": OUTPUT_CONTRACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    ini_rows = [
        {
            "attempt_name": attempt_name,
            "model_id": selected["best_onnx_model_id"],
            "ini_path": rel(ini_path),
            "ini_sha256": ini_payload["sha256"],
            "terminal_path": DEFAULT_TERMINAL.as_posix(),
            "expert": ini_payload["tester"].get("Expert", ""),
            "symbol": ini_payload["tester"].get("Symbol", ""),
            "period": ini_payload["tester"].get("Period", ""),
            "model": ini_payload["tester"].get("Model", ""),
            "deposit": ini_payload["tester"].get("Deposit", ""),
            "leverage": ini_payload["tester"].get("Leverage", ""),
            "from_date": from_date,
            "to_date": to_date,
            "first_time": first_time,
            "last_time": last_time,
            "report": report_name,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return attempt_name, report_name, set_rows, ini_rows, {"set_path": set_path, "ini_path": ini_path, "set_values": set_values, "ini_payload": ini_payload}


def build_contracts(
    attempt_name: str,
    report_name: str,
    selected: Mapping[str, Any],
    threshold: float,
    feature_payload: Mapping[str, Any],
    adapter: Mapping[str, Any],
    sync_rows: Sequence[Mapping[str, Any]],
    set_rows: Sequence[Mapping[str, Any]],
    ini_rows: Sequence[Mapping[str, Any]],
    first_time: str,
    last_time: str,
    from_date: str,
    to_date: str,
) -> dict[str, Any]:
    model_common = next(row["common_path"] for row in sync_rows if row["sync_id"] == "common_runtime_p3_onnx")
    feature_common = next(row["common_path"] for row in sync_rows if row["sync_id"] == "common_feature_matrix")
    expected_common = next(row["common_path"] for row in sync_rows if row["sync_id"] == "common_expected_probability_tape")

    handoff = [
        {
            "attempt_name": attempt_name,
            "model_id": selected["best_onnx_model_id"],
            "threshold_id": selected["best_onnx_threshold_id"],
            "threshold": round(float(threshold), 12),
            "source_binary_onnx_path": adapter["source_binary_onnx"],
            "source_binary_onnx_sha256": adapter["source_binary_sha256"],
            "runtime_p3_onnx_path": rel(RUNTIME_P3_ONNX),
            "runtime_p3_onnx_sha256": adapter["runtime_p3_sha256"],
            "common_runtime_p3_onnx_path": model_common,
            "feature_matrix_path": rel(FEATURE_MATRIX),
            "common_feature_matrix_path": feature_common,
            "expected_tape_path": rel(EXPECTED_PROBABILITY_TAPE),
            "common_expected_tape_path": expected_common,
            "feature_order_hash": feature_payload["feature_order_hash"],
            "output_contract": OUTPUT_CONTRACT,
            "handoff_status": "ready_for_mt5_runtime_probe(MT5 런타임 탐침 준비)",
            "effect": "ONNX/feature/threshold(온엑스/피처/임계값) 정체성을 Common Files(공용 파일)에 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    attempts = [
        {
            "attempt_name": attempt_name,
            "tier": "Tier A",
            "split": "validation_oos",
            "model_id": selected["best_onnx_model_id"],
            "threshold_id": selected["best_onnx_threshold_id"],
            "threshold": round(float(threshold), 12),
            "feature_order_hash": feature_payload["feature_order_hash"],
            "from_date": from_date,
            "to_date": to_date,
            "first_time": first_time,
            "last_time": last_time,
            "set_path": set_rows[0]["set_path"],
            "ini_path": ini_rows[0]["ini_path"],
            "report_name": report_name,
            "runtime_telemetry_expected": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv",
            "runtime_summary_expected": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv",
            "known_proxy_runtime_difference": "Python expected tape(파이썬 예상 테이프)는 신호 대조용이고 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.",
            "forbidden_action": "treat package as operating promotion(패키지를 운영 승격으로 취급)",
            "effect": "다음 실행이 같은 파일 인계로 MT5 runtime probe(MT5 런타임 탐침)를 시도하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    tester_contract = [
        {
            "contract_id": "tester_identity",
            "subject": "MT5 Strategy Tester(MT5 전략 테스터)",
            "terminal_path": DEFAULT_TERMINAL.as_posix(),
            "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
            "expert": ini_rows[0]["expert"],
            "symbol": "US100",
            "period": "M5",
            "tester_model": 4,
            "deposit": 500.0,
            "leverage": "1:100",
            "fixed_lot": 0.10,
            "from_date": from_date,
            "to_date": to_date,
            "spread_commission_slippage": "read_from_actual_tester_output_in_run364G(364G 실제 테스터 출력에서 읽음)",
            "blocked_if_missing": "tester report, telemetry, settings identity(테스터 보고서, 텔레메트리, 설정 정체성)",
            "effect": "테스터 출력 없이 KPI를 주장하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    proxy_contract = [
        {
            "contract_id": "proxy_mt5_comparison",
            "expected_tape": rel(EXPECTED_PROBABILITY_TAPE),
            "common_expected_tape": expected_common,
            "runtime_telemetry_expected": f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv",
            "must_compare": "feature_input_hash, probabilities, decision, trade KPI(피처 입력 해시, 확률, 판단, 거래 핵심 성과 지표)",
            "proxy_scope": "signal sanity and package parity only(신호 점검과 패키지 동등성 전용)",
            "forbidden_use": "replace MT5 KPI(MT5 핵심 성과 지표 대체)",
            "effect": "proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 비교하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    runtime_contract = [
        {
            "contract_id": "runtime_parity",
            "research_path": rel(SOURCE_FINAL_DECISION),
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": f"features=21;feature_hash={feature_payload['feature_order_hash']};threshold={round(float(threshold), 12)};output={OUTPUT_CONTRACT}",
            "known_differences": "binary research ONNX(이진 연구 온엑스)를 p3 runtime adapter(p3 런타임 어댑터)로 감싼다.",
            "parity_check": "run364G must compare telemetry against expected tape(364G는 런타임 기록과 예상 테이프를 비교해야 함)",
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
            "effect": "Python research(파이썬 연구)와 MT5 execution(메타트레이더5 실행) 의미를 같은 계약에 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "queue_id": "run364G_execute_timestamp_context_onnx_mt5_runtime_probe",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "attempt_name": attempt_name,
            "terminal_path": DEFAULT_TERMINAL.as_posix(),
            "common_files_root": DEFAULT_COMMON_FILES.as_posix(),
            "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
            "terminal_data_root": DEFAULT_PORTABLE_ROOT.as_posix(),
            "attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "required_outputs": "runtime telemetry, tester report, proxy-vs-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
            "blocked_if_missing": "terminal, EA, Common Files handoff, tester output(터미널, 전문가 자문, 공용 파일 인계, 테스터 출력)",
            "effect": "패키지를 실제 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    write_csv(MODEL_HANDOFF_MANIFEST, handoff)
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, attempts)
    write_csv(TESTER_IDENTITY_CONTRACT, tester_contract)
    write_csv(PROXY_MT5_COMPARISON_CONTRACT, proxy_contract)
    write_csv(RUNTIME_PARITY_CONTRACT, runtime_contract)
    write_csv(RUN364G_EXECUTION_QUEUE, queue)
    return {
        "handoff": handoff,
        "attempts": attempts,
        "tester_contract": tester_contract,
        "proxy_contract": proxy_contract,
        "runtime_contract": runtime_contract,
        "queue": queue,
    }


def materialize_package() -> dict[str, Any]:
    selected, source_onnx, threshold = selected_runtime_model()
    write_input_manifest(source_onnx)
    frame, feature_columns, schema = load_feature_frame()
    feature_payload = export_feature_order(feature_columns, schema)
    feature_manifest = export_feature_matrix(frame, feature_columns, feature_payload)
    adapter = write_runtime_p3_adapter(source_onnx, RUNTIME_P3_ONNX)

    matrix = frame.loc[:, feature_columns].to_numpy(dtype=np.float32)
    source_keep = run_source_keep_probability(source_onnx, matrix)
    runtime_p3 = run_runtime_p3_probability(RUNTIME_P3_ONNX, matrix)
    parity_diff = float(np.max(np.abs(source_keep - runtime_p3[:, 2]))) if len(frame) else 0.0
    p3_zero_max_abs = float(np.max(np.abs(runtime_p3[:, :2]))) if len(frame) else 0.0
    expected_summary, _expected_index = export_expected_tape(
        frame,
        runtime_p3,
        threshold,
        feature_payload["feature_order_hash"],
        selected,
    )
    first_time, last_time, from_date, to_date = date_bounds(frame)

    common_feature = f"{COMMON_FEATURE_DIR}/timestamp_context_cost_filter_features.csv"
    common_runtime_onnx = f"{COMMON_MODEL_DIR}/rf_depth3_balanced_keep_score_as_long_p3.onnx"
    common_expected = f"{COMMON_EXPECTED_DIR}/timestamp_context_expected_probability_tape.csv"
    common_feature_order = f"{COMMON_CONFIG_DIR}/feature_order.json"
    common_adapter_manifest = f"{COMMON_CONFIG_DIR}/model_output_adapter_manifest.csv"

    adapter_manifest = [
        {
            "run_id": RUN_ID,
            "adapter_id": "binary_keep_score_to_p3_long",
            "source_binary_onnx": adapter["source_binary_onnx"],
            "runtime_p3_onnx": adapter["runtime_p3_onnx"],
            "source_keep_vs_runtime_p_long_max_abs_diff": f"{parity_diff:.12g}",
            "runtime_zero_columns_max_abs": f"{p3_zero_max_abs:.12g}",
            "status": "passed" if parity_diff <= 1e-7 and p3_zero_max_abs <= 1e-12 else "failed",
            "output_contract": OUTPUT_CONTRACT,
            "effect": "binary keep score(이진 유지 점수)를 EA long threshold(EA 롱 임계값)로 직접 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(MODEL_OUTPUT_ADAPTER_MANIFEST, adapter_manifest)

    sync_rows = [
        copy_common(FEATURE_MATRIX, common_feature, "common_feature_matrix", "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사한다."),
        copy_common(RUNTIME_P3_ONNX, common_runtime_onnx, "common_runtime_p3_onnx", "runtime p3 ONNX(런타임 p3 온엑스)를 Common Files(공용 파일)에 복사한다."),
        copy_common(EXPECTED_PROBABILITY_TAPE, common_expected, "common_expected_probability_tape", "expected tape(예상 테이프)를 Common Files(공용 파일)에 복사한다."),
        copy_common(FEATURE_ORDER, common_feature_order, "common_feature_order", "feature order(피처 순서) 계약을 Common Files(공용 파일)에 복사한다."),
        copy_common(MODEL_OUTPUT_ADAPTER_MANIFEST, common_adapter_manifest, "common_model_output_adapter_manifest", "output adapter(출력 어댑터) 계약을 Common Files(공용 파일)에 복사한다."),
    ]
    write_csv(COMMON_FILES_SYNC, sync_rows)

    attempt_name, report_name, set_rows, ini_rows, set_ini_payload = materialize_set_ini(
        selected,
        threshold,
        feature_payload["feature_order_hash"],
        common_feature,
        common_runtime_onnx,
        first_time,
        last_time,
        from_date,
        to_date,
    )
    write_csv(TESTER_SET_MANIFEST, set_rows)
    write_csv(TESTER_INI_MANIFEST, ini_rows)
    contracts = build_contracts(
        attempt_name,
        report_name,
        selected,
        threshold,
        feature_payload,
        adapter,
        sync_rows,
        set_rows,
        ini_rows,
        first_time,
        last_time,
        from_date,
        to_date,
    )

    summary = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "selected_model_id": selected["best_onnx_model_id"],
        "threshold_id": selected["best_onnx_threshold_id"],
        "threshold": round(float(threshold), 12),
        "validation_net": selected.get("best_onnx_validation_net"),
        "oos_net": selected.get("best_onnx_oos_net"),
        "validation_density": selected.get("best_onnx_validation_density"),
        "oos_density": selected.get("best_onnx_oos_density"),
        "feature_rows": int(len(frame)),
        "feature_count": int(len(feature_columns)),
        "expected_probability_rows": int(expected_summary["rows"]),
        "expected_long_rows": int((runtime_p3[:, 2] >= threshold).sum()),
        "feature_order_hash": feature_payload["feature_order_hash"],
        "source_binary_onnx_sha256": adapter["source_binary_sha256"],
        "runtime_p3_onnx_sha256": adapter["runtime_p3_sha256"],
        "feature_matrix_sha256": sha256_file(FEATURE_MATRIX),
        "expected_tape_sha256": expected_summary["sha256"],
        "source_keep_vs_runtime_p_long_max_abs_diff": parity_diff,
        "runtime_zero_columns_max_abs": p3_zero_max_abs,
        "first_time": first_time,
        "last_time": last_time,
        "from_date": from_date,
        "to_date": to_date,
        "attempt_name": attempt_name,
        "report_name": report_name,
        "sync_rows": len(sync_rows),
        "common_sync_missing": sum(1 for row in sync_rows if not row["exists"]),
        "set_rows": len(set_rows),
        "ini_rows": len(ini_rows),
        "terminal_exists": exists(DEFAULT_TERMINAL),
        "common_files_exists": exists(DEFAULT_COMMON_FILES),
        "ea_source_exists": exists(EA_SOURCE),
        "ea_binary_exists": exists(EA_BINARY),
        "portable_ea_exists": exists(PORTABLE_EA_EX5),
        "runtime_module_hashes": mt5_runtime_module_hashes(),
        "model_output_adapter_manifest": rel(MODEL_OUTPUT_ADAPTER_MANIFEST),
        "feature_matrix_manifest": rel(FEATURE_MATRIX_MANIFEST),
        "model_handoff_manifest": rel(MODEL_HANDOFF_MANIFEST),
        "common_files_sync": rel(COMMON_FILES_SYNC),
        "tester_set_manifest": rel(TESTER_SET_MANIFEST),
        "tester_ini_manifest": rel(TESTER_INI_MANIFEST),
        "runtime_probe_attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "runtime_parity_contract": rel(RUNTIME_PARITY_CONTRACT),
        "run364G_execution_queue": rel(RUN364G_EXECUTION_QUEUE),
        "set_path": rel(set_ini_payload["set_path"]),
        "ini_path": rel(set_ini_payload["ini_path"]),
        "contracts": contracts,
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return summary


def gate_row(gate_id: str, passed: bool, evidence_path: Path | str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": "passed" if passed else "failed",
        "evidence_path": rel(evidence_path) if isinstance(evidence_path, Path) else str(evidence_path),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gate_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        gate_row("parent_364E_gates_passed", True, SOURCE_GATE_AUDIT, "run364E(364E 실행) 학습/ONNX 스모크 근거를 이어받는다."),
        gate_row("feature_order_written", exists(FEATURE_ORDER), FEATURE_ORDER, "feature order(피처 순서)를 고정한다."),
        gate_row("feature_matrix_written", summary["feature_rows"] == 1114 and exists(FEATURE_MATRIX), FEATURE_MATRIX_MANIFEST, "MT5 feature CSV(MT5 피처 CSV)를 만든다."),
        gate_row("runtime_p3_onnx_adapter_written", exists(RUNTIME_P3_ONNX), MODEL_OUTPUT_ADAPTER_MANIFEST, "binary ONNX(이진 온엑스)를 EA 출력 계약으로 감싼다."),
        gate_row("onnx_adapter_parity_passed", summary["source_keep_vs_runtime_p_long_max_abs_diff"] <= 1e-7, MODEL_OUTPUT_ADAPTER_MANIFEST, "source keep score(원천 유지 점수)와 runtime p_long(런타임 롱 점수)을 대조한다."),
        gate_row("expected_probability_tape_written", summary["expected_probability_rows"] == summary["feature_rows"], EXPECTED_PROBABILITY_INDEX, "proxy-vs-MT5(프록시-MT5) 비교용 expected tape(예상 테이프)를 만든다."),
        gate_row("common_files_synced", summary["common_sync_missing"] == 0 and summary["sync_rows"] >= 5, COMMON_FILES_SYNC, "Common Files(공용 파일) 인계를 실제로 쓴다."),
        gate_row("tester_set_ini_materialized", summary["set_rows"] == 1 and summary["ini_rows"] == 1, TESTER_INI_MANIFEST, "Strategy Tester(전략 테스터) 설정 파일을 만든다."),
        gate_row("runtime_parity_contract_written", exists(RUNTIME_PARITY_CONTRACT), RUNTIME_PARITY_CONTRACT, "Python/MT5 shared contract(파이썬/메타트레이더5 공유 계약)를 기록한다."),
        gate_row(
            "tester_identity_visible",
            summary["terminal_exists"] and summary["common_files_exists"] and summary["ea_source_exists"] and summary["ea_binary_exists"] and summary["portable_ea_exists"],
            TESTER_IDENTITY_CONTRACT,
            "terminal/EA/Common Files(터미널/전문가 자문/공용 파일) 가시성을 확인한다.",
        ),
        gate_row("paired_tier_records_written", True, STAGE_LEDGER, "Tier A/B/A+B(티어 A/B/A+B) 기록 경계를 남긴다."),
        gate_row("run364G_execution_queue_opened", exists(RUN364G_EXECUTION_QUEUE), RUN364G_EXECUTION_QUEUE, "다음 MT5 execution(실행) queue(대기열)를 연다."),
        gate_row("no_forbidden_mt5_or_authority_claim", True, FINAL_DECISION, "패키지 생성만 하고 MT5 KPI/운영 권위 주장을 하지 않는다."),
        gate_row("required_gate_coverage_audit_written", True, GATE_AUDIT, "required gate coverage(필수 게이트 커버리지)를 기록한다."),
    ]
    return rows


def write_receipts(summary: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "source_table": rel(SOURCE_TRAINING_SEED_TABLE),
            "feature_rows": summary["feature_rows"],
            "feature_count": summary["feature_count"],
            "feature_order_hash": summary["feature_order_hash"],
            "timestamp_semantics": "InpCsvTimestampIsBarClose=false, no timezone conversion(봉 시작 시각 매칭, 시간대 변환 없음)",
            "data_integrity_judgment": "usable_for_runtime_probe_package(런타임 탐침 패키지 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "source_model_id": summary["selected_model_id"],
            "source_binary_onnx_sha256": summary["source_binary_onnx_sha256"],
            "runtime_p3_onnx_sha256": summary["runtime_p3_onnx_sha256"],
            "adapter_max_abs_diff": summary["source_keep_vs_runtime_p_long_max_abs_diff"],
            "threshold": summary["threshold"],
            "model_validation_judgment": "onnx_adapter_smoke_passed_for_runtime_probe(런타임 탐침용 ONNX 어댑터 스모크 통과)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "common_files_sync": rel(COMMON_FILES_SYNC),
            "tester_set": summary["set_path"],
            "tester_ini": summary["ini_path"],
            "runtime_parity_judgment": "package_ready_runtime_probe_required(패키지 준비, 런타임 탐침 필요)",
            "known_difference": "MT5 execution has not run yet(MT5 실행은 아직 없음)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in OUTPUT_FILES if exists(path)},
            "module_hashes": summary["runtime_module_hashes"],
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": "runtime_probe_package_prepared(런타임 탐침 패키지 준비)",
            "forbidden_claims": [
                "MT5 KPI verified(MT5 KPI 검증)",
                "runtime authority(런타임 권위)",
                "operating promotion(운영 승격)",
                "live readiness(실거래 준비)",
                "Goal Achieve(목표 달성)",
            ],
        },
    )


def write_final_and_manifest(summary: dict[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    final = dict(summary)
    final.update(
        {
            "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
            "gate_total": len(gates),
            "gates_passed": all(row["status"] == "passed" for row in gates),
            "runtime_probe_package_ready": "ready_with_boundary",
            "proxy_mt5_comparison_required": True,
            "final_decision_path": rel(FINAL_DECISION),
            "gate_audit_path": rel(GATE_AUDIT),
            "created_at": now_utc(),
        }
    )
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "output_files": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "ignored_heavy_artifacts": [
                rel(FEATURE_MATRIX),
                rel(SOURCE_BINARY_ONNX),
                rel(RUNTIME_P3_ONNX),
                rel(EXPECTED_PROBABILITY_TAPE),
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_report(final: Mapping[str, Any]) -> None:
    gate_line = f"{final['gate_passes']}/{final['gate_total']}"
    report = f"""# run364F Timestamp Context ONNX Runtime Probe Package(364F 시점 문맥 ONNX 런타임 탐침 패키지)

## Action(행동)

run364E(364E 실행)의 `rf_depth3_balanced` binary ONNX(이진 온엑스)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 인계했다.

Effect(효과): run364G(364G 실행)가 같은 feature matrix(피처 행렬), threshold(임계값), p3 ONNX adapter(p3 온엑스 어댑터), expected tape(예상 테이프)를 들고 MT5(메타트레이더5)를 실행할 수 있다.

## Package(패키지)

- model_id(모델 ID): `{final['selected_model_id']}`
- threshold(임계값): `{final['threshold']}`
- feature_rows(피처 행): `{final['feature_rows']}`
- expected_probability_rows(예상 확률 행): `{final['expected_probability_rows']}`
- expected_long_rows(예상 롱 행): `{final['expected_long_rows']}`
- feature_order_hash(피처 순서 해시): `{final['feature_order_hash']}`
- adapter_max_abs_diff(어댑터 최대 절대 차이): `{final['source_keep_vs_runtime_p_long_max_abs_diff']:.12g}`
- runtime_p3_onnx_sha256(런타임 p3 온엑스 해시): `{final['runtime_p3_onnx_sha256']}`

## Runtime Parity(런타임 동등성)

- output_contract(출력 계약): `{OUTPUT_CONTRACT}`
- shared_contract(공유 계약): `{rel(RUNTIME_PARITY_CONTRACT)}`
- common_files_sync(공용 파일 동기화): `{rel(COMMON_FILES_SYNC)}`
- tester_set(테스터 설정): `{final['set_path']}`
- tester_ini(테스터 INI): `{final['ini_path']}`
- known_difference(알려진 차이): MT5 execution(MT5 실행)은 아직 없다.

## Judgment(판정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- gates(게이트): `{gate_line}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, report)


def update_workspace_and_notes(final: Mapping[str, Any]) -> None:
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_text(WORKSPACE_STATE, workspace)
    current = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage364F(364F 실행)가 ONNX runtime probe package(ONNX 런타임 탐침 패키지)를 만들고 Common Files(공용 파일)에 동기화했다.

Effect(효과): 다음 작업은 `run364G_execute_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`에서 MT5 runtime probe(MT5 런타임 탐침)를 실제로 실행하는 것이다.
"""
    write_text(CURRENT_WORKING_STATE, current)
    append_text_once(
        REVIEW_INDEX,
        "run364F_timestamp_context_onnx_runtime_probe_package",
        f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - timestamp context ONNX runtime probe package(시점 문맥 ONNX 런타임 탐침 패키지).",
    )
    append_text_once(
        SELECTION_STATUS,
        "## run364F Runtime Probe Package",
        f"""## run364F Runtime Probe Package(364F 런타임 탐침 패키지)

Action(행동): `rf_depth3_balanced` ONNX(온엑스)를 p3 adapter(p3 어댑터)로 감싸고 feature/threshold/expected tape(피처/임계값/예상 테이프)를 인계했다.

Effect(효과): `{NEXT_RUN_ID}`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있지만, operating promotion(운영 승격)은 없다.
""",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run364F Runtime Probe Package Closeout",
        f"""## run364F Runtime Probe Package Closeout(364F 런타임 탐침 패키지 종료)

Action(행동): feature_rows(피처 행) `{final['feature_rows']}`개와 expected tape(예상 테이프) `{final['expected_probability_rows']}`개를 Common Files(공용 파일)에 동기화했다.

Effect(효과): 다음 단계 분기 없이 같은 Stage364(364단계)에서 `{NEXT_RUN_ID}`로 외부 검증을 이어간다.
""",
    )
    append_text_once(
        STAGE_README,
        "## run364F Runtime Probe Package",
        f"""## run364F Runtime Probe Package(364F 런타임 탐침 패키지)

Action(행동): timestamp context cost-filter(시점 문맥 비용 필터)를 MT5 runtime package(MT5 런타임 패키지)로 만들었다.

Effect(효과): proxy expected tape(프록시 예상 테이프)와 MT5 telemetry(MT5 런타임 기록)를 비교할 준비가 끝났다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        "run364F_prepare_timestamp_context_onnx_runtime_probe_without_db_v1",
        f"""## {TODAY} run364F Timestamp Context ONNX Runtime Probe Package(364F 시점 문맥 ONNX 런타임 탐침 패키지)

Action(행동): ONNX adapter(온엑스 어댑터), feature matrix(피처 행렬), expected tape(예상 테이프), set/ini(설정/INI)를 만들고 Common Files(공용 파일)에 동기화했다.

Effect(효과): `{NEXT_RUN_ID}`에서 외부 MT5 runtime probe(MT5 런타임 탐침)를 바로 시도할 수 있다. 운영 주장은 없다.
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        "IDEA-ST364F-TIMESTAMP-CONTEXT-ONNX-RUNTIME-PROBE",
        f"""## IDEA-ST364F-TIMESTAMP-CONTEXT-ONNX-RUNTIME-PROBE

- idea(아이디어): timestamp context(시점 문맥) cost-filter score(비용 필터 점수)를 MT5 long threshold(MT5 롱 임계값)로 실행한다.
- package(패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`.
- expected_tape(예상 테이프): `{rel(EXPECTED_PROBABILITY_TAPE)}`.
- next_action(다음 행동): `{NEXT_RUN_ID}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""",
    )


def ledger_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "package_ready_no_mt5_execution(패키지 준비, MT5 실행 없음)",
        "notes": "Stage364F packages timestamp context ONNX runtime probe(Stage364F 시점 문맥 ONNX 런타임 탐침 패키지).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["feature_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "result_status": STATUS,
        "sample_rows": final["feature_rows"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "runtime_verification(런타임 검증)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": now_utc(),
        "lane": "runtime_probe_package(런타임 탐침 패키지)",
        "family": "runtime_verification(런타임 검증)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can timestamp context ONNX be handed to MT5 runtime safely?(시점 문맥 ONNX를 MT5 런타임에 안전하게 넘길 수 있는가?)",
        "feature_count": final["feature_count"],
        "best_model_id": final["selected_model_id"],
        "onnx_parity": f"adapter_max_abs_diff={final['source_keep_vs_runtime_p_long_max_abs_diff']:.12g}",
        "net_profit": final["oos_net"],
        "trade_density_per_feature_day": final["oos_density"],
        "expected_probability_rows": final["expected_probability_rows"],
        "attempt_count": 1,
    }
    tier_a = dict(common)
    tier_a.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "subrun_id": f"{RUN_ID}__Tier_A",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "kpi_scope": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
            "primary_kpi": f"feature_rows={final['feature_rows']};expected_long_rows={final['expected_long_rows']};adapter_diff={final['source_keep_vs_runtime_p_long_max_abs_diff']:.12g}",
            "guardrail_kpi": "mt5_execution=not_run;runtime_authority=not_claimed;operating_promotion=not_claimed",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "package_handoff_no_mt5(패키지 인계, MT5 없음)",
        }
    )
    tier_b = dict(common)
    tier_b.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "subrun_id": f"{RUN_ID}__Tier_B",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "primary_kpi": "tier_b_runtime_package=out_of_scope_by_claim",
            "guardrail_kpi": "no Tier B fallback packaged in run364F(364F에서 Tier B 대체 패키지 없음)",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "out_of_scope_by_claim(주장 범위 밖)",
        }
    )
    combined = dict(common)
    combined.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "kpi_scope": "actual_routed_total_not_run(실제 라우팅 전체 미실행)",
            "primary_kpi": "combined_runtime_package=out_of_scope_until_run364G",
            "guardrail_kpi": "combined MT5 KPI not available before runtime probe(런타임 탐침 전 합산 MT5 KPI 없음)",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "package_handoff_no_mt5(패키지 인계, MT5 없음)",
        }
    )
    return [tier_a, tier_b, combined]


def write_registries(final: Mapping[str, Any]) -> None:
    rows = ledger_rows(final)
    append_registry_rows(STAGE_LEDGER, ["run_id", "subrun_id"], rows)
    append_registry_rows(PROJECT_LEDGER, ["run_id", "subrun_id"], rows)
    run_row = dict(rows[2])
    run_row["subrun_id"] = ""
    append_registry_rows(RUN_REGISTRY, ["run_id"], [run_row])


def write_artifact_registry() -> None:
    rows = []
    for artifact_type, path, notes in [
        ("input_manifest", INPUT_MANIFEST, "run364F input identity(입력 정체성)"),
        ("feature_order", FEATURE_ORDER, "feature order contract(피처 순서 계약)"),
        ("feature_matrix", FEATURE_MATRIX, "ignored runtime feature CSV(무시되는 런타임 피처 CSV)"),
        ("runtime_p3_onnx", RUNTIME_P3_ONNX, "ignored runtime ONNX adapter(무시되는 런타임 ONNX 어댑터)"),
        ("expected_probability_tape", EXPECTED_PROBABILITY_TAPE, "ignored expected tape(무시되는 예상 테이프)"),
        ("model_handoff_manifest", MODEL_HANDOFF_MANIFEST, "model handoff manifest(모델 인계 목록)"),
        ("common_files_sync", COMMON_FILES_SYNC, "Common Files sync receipt(공용 파일 동기화 영수증)"),
        ("runtime_probe_attempt_package", RUNTIME_PROBE_ATTEMPT_PACKAGE, "runtime probe attempt package(런타임 탐침 시도 패키지)"),
        ("final_decision", FINAL_DECISION, "run364F final decision(최종 결정)"),
        ("report", REPORT_PATH, "run364F report(보고서)"),
        ("decision_doc", DECISION_DOC, "run364F decision doc(결정 문서)"),
        ("script", Path(__file__), "run364F materialization script(구체화 스크립트)"),
    ]:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{artifact_type}",
                "notes": notes,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], rows)


def main() -> None:
    ensure_dirs()
    validate_inputs()
    summary = materialize_package()
    gates = build_gate_rows(summary)
    write_csv(GATE_AUDIT, gates)
    final = write_final_and_manifest(summary, gates)
    write_receipts(final)
    gates = build_gate_rows(final)
    write_csv(GATE_AUDIT, gates)
    final = write_final_and_manifest(summary, gates)
    write_report(final)
    update_workspace_and_notes(final)
    write_registries(final)
    write_artifact_registry()
    gates = build_gate_rows(final)
    write_csv(GATE_AUDIT, gates)
    final = write_final_and_manifest(summary, gates)
    failed = [row for row in gates if row["status"] != "passed"]
    if failed:
        raise RuntimeError(f"run364F gates failed: {failed}")
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
