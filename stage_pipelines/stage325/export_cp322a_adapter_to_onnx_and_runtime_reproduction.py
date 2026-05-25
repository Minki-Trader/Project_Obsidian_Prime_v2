from __future__ import annotations

import argparse
import ast
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    bool_value,
    copy_to_common,
    parse_ini,
    parse_set,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage279 import execute_or_prepare_directional_runtime_mapping_mt5_probe as base  # noqa: E402


STAGE_ID = "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a"
RUN_ID = "run325A_export_cp322a_adapter_to_onnx_and_runtime_reproduction_v1"
RUN_NUMBER = "run325A"
SOURCE_RUN_ID = "run324A_execute_onnx_go_pressure_for_cp322a_adapter_package_v1"
PARENT_RUN_ID = "run323A_build_adapter_package_for_cp322a_selected_curve_v1"
UPDATED_ON = "2026-05-26"

SELECTED_CANDIDATE = "cp322A_cp321b_exact_replay_control_surface"
SELECTED_BRANCH = "run322A_cp322A_cp321b_exact_replay_control"
ADAPTER_PACKAGE_ID = "stage323_cp322a_selected_curve_adapter_package_v1"
STATUS_PREPARED = "prepared_cp322a_onnx_export_parity_runtime_reproduction_no_mt5"
STATUS_COMPLETED = "completed_cp322a_onnx_export_parity_runtime_reproduction_package_ready_for_main_push"
JUDGMENT_COMPLETED = "onnx_export_parity_and_mt5_runtime_reproduction_passed_main_push_pending"
NEXT_ACTION_WHEN_COMPLETE = "commit_and_push_main_then_mark_goal_achieved"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_final_package_for_onnx_research_handoff_only"
)
EXPLORATION_LABEL = "stage325_Model__Cp322aOnnxRuntimeReproduction"
FEATURE_ORDER = ("run322b_route_signal",)
FEATURE_ORDER_HASH = ordered_hash(FEATURE_ORDER)
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage325/run325A_cp322a_onnx"
MODEL_NAME = "cp322a_route_signal_identity.onnx"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
SELECTED_FINAL_REPORT = STAGE_ROOT / "04_selected" / "final_candidate_package_report.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
INPUTS = STAGE_ROOT / "01_inputs"
MODEL_DIR = RUN_ROOT / "models"
MT5_DIR = RUN_ROOT / "mt5"

STAGE322_ROOT = ROOT / "stages" / "322_onnx_candidate_campaign__cp321b_curve_stability_pressure"
STAGE322_RUN_A = STAGE322_ROOT / "02_runs" / "run322A"
STAGE322_RUN_B = STAGE322_ROOT / "02_runs" / "run322B"
SOURCE_QUEUE = STAGE322_RUN_A / "mt5_probe_queue.csv"
SOURCE_PAYLOAD_MANIFEST = STAGE322_RUN_A / "candidate_payload_manifest.csv"
SOURCE_EXECUTION_RESULT = STAGE322_RUN_B / "execution_result.json"
SOURCE_KPI_SUMMARY = STAGE322_RUN_B / "mt5_kpi_summary.csv"
SOURCE_FEATURE_DIR = STAGE322_RUN_B / "features"
SOURCE_MT5_DIR = STAGE322_RUN_B / "mt5"

STAGE323_PACKAGE = (
    ROOT
    / "stages"
    / "323_onnx_candidate_campaign__selected_curve_adapter_package"
    / "02_runs"
    / "run323A"
    / "adapter_package"
)
ADAPTER_MANIFEST_INPUT = INPUTS / "adapter_package_manifest.json"
ADAPTER_HASH_INPUT = INPUTS / "adapter_package_hash_receipt.json"
RUNTIME_FEATURE_ORDER = STAGE323_PACKAGE / "feature_order_runtime.csv"
RUNTIME_HANDOFF = STAGE323_PACKAGE / "runtime_handoff_manifest.json"
DECISION_SURFACE = STAGE323_PACKAGE / "decision_surface.json"
RISK_LOGIC = STAGE323_PACKAGE / "risk_logic.json"

PRODUCER = Path("stage_pipelines/stage325/export_cp322a_adapter_to_onnx_and_runtime_reproduction.py")
SELECTED_QUEUE = RUN_ROOT / "selected_mt5_probe_queue.csv"
ONNX_MODEL = MODEL_DIR / MODEL_NAME
ONNX_EXPORT_REPORT = RUN_ROOT / "onnx_export_report.json"
PYTHON_INFERENCE_CHECK = RUN_ROOT / "python_inference_check.json"
FEATURE_ORDER_PARITY = RUN_ROOT / "feature_order_parity_receipt.json"
ONNX_PARITY_RECEIPT = RUN_ROOT / "onnx_parity_receipt.json"
ATTEMPT_SUMMARY = RUN_ROOT / "attempt_summary.csv"
RUNTIME_SUPPLY = RUN_ROOT / "runtime_supply_matrix.csv"
EXECUTION_RESULT = RUN_ROOT / "execution_result.json"
MT5_KPI_SUMMARY = RUN_ROOT / "mt5_kpi_summary.csv"
RUNTIME_PARITY_RECEIPT = RUN_ROOT / "runtime_parity_receipt.json"
RUNTIME_COMPARISON = RUN_ROOT / "runtime_metric_comparison.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
FINAL_REPORT = REVIEWS / "run325A_final_candidate_package_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-26_stage325_cp322a_onnx_package_ready_main_push_pending.md"

STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
RUNTIME_COMPARE_COLUMNS = (
    "comparison_key",
    "split",
    "tier_scope",
    "route_role",
    "metric",
    "source_value",
    "onnx_value",
    "absolute_diff",
    "tolerance",
    "status",
)
SUPPLY_COLUMNS = (
    "materialized_branch_id",
    "tier_scope",
    "split",
    "rows",
    "nonflat_signal_count",
    "long_signal_count",
    "short_signal_count",
    "nonflat_signal_rate",
    "long_share_of_signals",
    "short_share_of_signals",
    "feature_matrix_path",
    "feature_matrix_hash",
)
RUNTIME_SET_COPY_KEYS = (
    "InpAllowTrading",
    "InpFixedLot",
    "InpAtrSltpEnabled",
    "InpAtrPeriod",
    "InpAtrStopMultiplier",
    "InpAtrTakeProfitMultiplier",
    "InpAtrMinStopPoints",
    "InpAtrMaxStopPoints",
    "InpAtrMinTakeProfitPoints",
    "InpAtrMaxTakeProfitPoints",
    "InpModelRiskSizingEnabled",
    "InpModelRiskMinPct",
    "InpModelRiskMaxPct",
    "InpModelRiskFallbackLot",
    "InpModelRiskConfidenceFloor",
    "InpModelRiskConfidenceCeiling",
    "InpExitRiskOverlayEnabled",
    "InpExitRiskCloseLongFeatureIndex",
    "InpExitRiskCloseShortFeatureIndex",
    "InpExitRiskCloseThreshold",
    "InpExitRiskMaxHoldFeatureIndex",
    "InpExitRiskMinHoldBars",
    "InpEntryTransitionOnly",
    "InpReentryCooldownBars",
    "InpSameDirectionReentryCooldownBars",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding=encoding,
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def upsert_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    upsert_csv_rows(path, columns, rows, key=key)


def dynamic_columns(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(str(key))
    return columns or ["status"]


def read_json(path: Path) -> dict[str, Any]:
    return dict(json.loads(io_path(path).read_text(encoding="utf-8-sig")))


def parse_metrics(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    text = str(value or "{}").strip()
    if not text:
        return {}
    for parser in (json.loads, ast.literal_eval):
        try:
            parsed = parser(text)
        except (ValueError, SyntaxError, json.JSONDecodeError):
            continue
        return dict(parsed) if isinstance(parsed, Mapping) else {}
    return {}


def metric_float(metrics: Mapping[str, Any], key: str) -> float:
    try:
        value = float(metrics.get(key, 0) or 0)
    except (TypeError, ValueError):
        return 0.0
    return value if math.isfinite(value) else 0.0


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def selected_queue_rows() -> list[dict[str, str]]:
    rows = [row for row in read_csv_rows(SOURCE_QUEUE) if row.get("materialized_branch_id") == SELECTED_BRANCH]
    if len(rows) != 1:
        raise RuntimeError(f"expected one selected queue row for {SELECTED_BRANCH}, found {len(rows)}")
    write_csv(SELECTED_QUEUE, tuple(rows[0].keys()), rows)
    return rows


def configure_base() -> None:
    base.STAGE_ID = STAGE_ID
    base.RUN_ID = RUN_ID
    base.RUN_NUMBER = RUN_NUMBER
    base.SOURCE_RUN_ID = SOURCE_RUN_ID
    base.PARENT_RUN_ID = PARENT_RUN_ID
    base.STATUS_PREPARED = STATUS_PREPARED
    base.UPDATED_ON = UPDATED_ON
    base.BOUNDARY = BOUNDARY
    base.EXPLORATION_LABEL = EXPLORATION_LABEL
    base.SIGNAL_COLUMN = FEATURE_ORDER[0]
    base.COMMON_ROOT = COMMON_ROOT
    base.STAGE_ROOT = STAGE_ROOT
    base.RUN279B = STAGE322_RUN_A
    base.RUN_ROOT = RUN_ROOT
    base.REVIEWS = REVIEWS
    base.SELECTED = SELECTED
    base.REPORT_PATH = FINAL_REPORT
    base.MODEL_DIR = MODEL_DIR
    base.MT5_DIR = MT5_DIR
    base.MT5_QUEUE = SELECTED_QUEUE
    base.RUN279B_MANIFEST = STAGE322_RUN_A / "run_manifest.json"
    base.RUN279B_PAYLOAD_MANIFEST = SOURCE_PAYLOAD_MANIFEST
    base.RUN279B_SIGNAL_RECEIPT = SOURCE_PAYLOAD_MANIFEST
    base.RUN279B_REPORT = STAGE322_ROOT / "03_reviews" / "run322A_materialization.md"
    base.RUN_REGISTRY = RUN_REGISTRY
    base.ALPHA_LEDGER = ALPHA_LEDGER
    base.ARTIFACT_REGISTRY = ARTIFACT_REGISTRY
    base.STAGE_LEDGER = STAGE_LEDGER
    base.CURRENT_STATE = CURRENT_STATE
    base.WORKSPACE_STATE = WORKSPACE_STATE
    base.CHANGELOG = CHANGELOG
    base.REVIEW_INDEX = REVIEW_INDEX
    base.PRODUCER_PATH = PRODUCER
    base.ATTEMPT_SUMMARY = ATTEMPT_SUMMARY
    base.RUNTIME_SUPPLY = RUNTIME_SUPPLY
    base.EXECUTION_RESULT = EXECUTION_RESULT
    base.MT5_KPI_SUMMARY = MT5_KPI_SUMMARY
    base.RUNTIME_PARITY_RECEIPT = RUNTIME_PARITY_RECEIPT
    base.RESULT_JUDGMENT = RESULT_JUDGMENT
    base.GATE_AUDIT = GATE_AUDIT
    base.RUN_MANIFEST = RUN_MANIFEST
    base.LINEAGE_RECEIPT = LINEAGE


def export_route_signal_onnx(path: Path) -> dict[str, Any]:
    import onnx
    from onnx import TensorProto, helper

    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    input_info = helper.make_tensor_value_info("float_input", TensorProto.FLOAT, [None, 1])
    output_info = helper.make_tensor_value_info("probabilities", TensorProto.FLOAT, [None, 3])
    half = helper.make_tensor("half_const", TensorProto.FLOAT, [1, 1], [0.5])
    one = helper.make_tensor("one_const", TensorProto.FLOAT, [1, 1], [1.0])
    nodes = [
        helper.make_node("Mul", ["float_input", "float_input"], ["x_squared"], name="square_route_signal"),
        helper.make_node("Sub", ["x_squared", "float_input"], ["short_twice"], name="short_raw"),
        helper.make_node("Mul", ["short_twice", "half_const"], ["p_short"], name="short_probability"),
        helper.make_node("Sub", ["one_const", "x_squared"], ["p_flat"], name="flat_probability"),
        helper.make_node("Add", ["x_squared", "float_input"], ["long_twice"], name="long_raw"),
        helper.make_node("Mul", ["long_twice", "half_const"], ["p_long"], name="long_probability"),
        helper.make_node("Concat", ["p_short", "p_flat", "p_long"], ["probabilities"], axis=1, name="probability_concat"),
    ]
    graph = helper.make_graph(
        nodes,
        "cp322a_route_signal_identity_probability_graph",
        [input_info],
        [output_info],
        initializer=[half, one],
    )
    model = helper.make_model(
        graph,
        producer_name="Project_Obsidian_Prime_v2_stage325",
        opset_imports=[helper.make_operatorsetid("", 13)],
    )
    model.ir_version = 7
    onnx.checker.check_model(model)
    onnx.save(model, io_path(path))
    return {
        "model_path": rel(path),
        "sha256": sha256_file_lf_normalized(path),
        "input_name": "float_input",
        "input_shape": ["N", 1],
        "output_name": "probabilities",
        "output_shape": ["N", 3],
        "class_order": ["short", "flat", "long"],
        "feature_order": list(FEATURE_ORDER),
        "feature_order_hash": FEATURE_ORDER_HASH,
        "probability_formula": {
            "p_short": "0.5 * (signal^2 - signal)",
            "p_flat": "1 - signal^2",
            "p_long": "0.5 * (signal^2 + signal)",
        },
    }


def expected_probabilities(values: np.ndarray) -> np.ndarray:
    x = values.astype("float32")
    x2 = x * x
    return np.concatenate((0.5 * (x2 - x), 1.0 - x2, 0.5 * (x2 + x)), axis=1).astype("float32")


def route_decisions(probabilities: np.ndarray) -> np.ndarray:
    decisions: list[int] = []
    for p_short, _p_flat, p_long in probabilities:
        if float(p_long) >= 0.55 and float(p_long) >= float(p_short):
            decisions.append(1)
        elif float(p_short) >= 0.55:
            decisions.append(-1)
        else:
            decisions.append(0)
    return np.asarray(decisions, dtype=np.int8)


def source_feature_path(tier_key: str, split_token: str) -> Path:
    return SOURCE_FEATURE_DIR / f"{SELECTED_BRANCH}_{tier_key}_{split_token}_route_signal.csv"


def source_ini_path(role_token: str, split_token: str) -> Path:
    return SOURCE_MT5_DIR / f"{SELECTED_BRANCH}_{role_token}_{split_token}.ini"


def source_set_path(role_token: str, split_token: str) -> Path:
    return SOURCE_MT5_DIR / f"{SELECTED_BRANCH}_{role_token}_{split_token}.set"


def source_dates(role_token: str, split_token: str) -> tuple[str, str]:
    values = parse_ini(source_ini_path(role_token, split_token))
    return values["FromDate"], values["ToDate"]


def source_rules(role_token: str, split_token: str) -> dict[str, Any]:
    values = parse_set(source_set_path(role_token, split_token))
    return {
        "short_threshold": float(values["InpShortThreshold"]),
        "long_threshold": float(values["InpLongThreshold"]),
        "min_margin": float(values["InpMinMargin"]),
        "invert_signal": bool_value(values.get("InpInvertSignal", "false")),
        "fallback_short_threshold": float(values.get("InpFallbackShortThreshold", values["InpShortThreshold"])),
        "fallback_long_threshold": float(values.get("InpFallbackLongThreshold", values["InpLongThreshold"])),
        "fallback_min_margin": float(values.get("InpFallbackMinMargin", values["InpMinMargin"])),
        "fallback_invert_signal": bool_value(values.get("InpFallbackInvertSignal", values.get("InpInvertSignal", "false"))),
        "max_hold_bars": int(float(values["InpMaxHoldBars"])),
        "close_on_flat_signal": bool_value(values.get("InpCloseOnFlatSignal", "false")),
        "reverse_on_opposite_signal": bool_value(values.get("InpReverseOnOppositeSignal", "true")),
        "close_only_on_opposite_signal": bool_value(values.get("InpCloseOnlyOnOppositeSignal", "false")),
        "extra_set_values": {key: values[key] for key in RUNTIME_SET_COPY_KEYS if key in values},
    }


def feature_exports_and_frames() -> tuple[dict[str, Any], dict[str, pd.DataFrame], list[dict[str, Any]]]:
    exports: dict[str, Any] = {}
    frames: dict[str, pd.DataFrame] = {}
    supply_rows: list[dict[str, Any]] = []
    for tier_key, tier_label in (("tier_a", mt5.TIER_A), ("tier_b", mt5.TIER_B)):
        for runtime_split, split_token in (("validation_is", "val"), ("oos", "oos")):
            path = source_feature_path(tier_key, split_token)
            frame = pd.read_csv(io_path(path), usecols=list(FEATURE_ORDER))
            values = pd.to_numeric(frame[FEATURE_ORDER[0]], errors="coerce").fillna(0).astype("int8")
            frame[FEATURE_ORDER[0]] = values
            key = f"{SELECTED_BRANCH}__{tier_key}__{runtime_split}"
            nonflat = int(values.ne(0).sum())
            long_count = int(values.eq(1).sum())
            short_count = int(values.eq(-1).sum())
            rows = int(len(frame))
            exports[key] = {"path": rel(path), "sha256": sha256_file_lf_normalized(path)}
            frames[key] = frame
            supply_rows.append(
                {
                    "materialized_branch_id": SELECTED_BRANCH,
                    "tier_scope": tier_label,
                    "split": runtime_split,
                    "rows": rows,
                    "nonflat_signal_count": nonflat,
                    "long_signal_count": long_count,
                    "short_signal_count": short_count,
                    "nonflat_signal_rate": round(float(nonflat / rows) if rows else 0.0, 8),
                    "long_share_of_signals": round(float(long_count / nonflat) if nonflat else 0.0, 8),
                    "short_share_of_signals": round(float(short_count / nonflat) if nonflat else 0.0, 8),
                    "feature_matrix_path": rel(path),
                    "feature_matrix_hash": exports[key]["sha256"],
                }
            )
    return exports, frames, supply_rows


def run_python_parity(onnx_path: Path, split_frames: Mapping[str, pd.DataFrame]) -> tuple[dict[str, Any], dict[str, Any]]:
    import onnxruntime as ort

    frames = [frame.loc[:, list(FEATURE_ORDER)].astype("float32") for frame in split_frames.values()]
    values = pd.concat(frames, axis=0, ignore_index=True).to_numpy(dtype=np.float32)
    unique_values = sorted(float(value) for value in np.unique(values[:, 0]))
    if not set(unique_values).issubset({-1.0, 0.0, 1.0}):
        raise RuntimeError(f"route signal has non-discrete values: {unique_values}")
    expected = expected_probabilities(values)
    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    actual = np.asarray(session.run(None, {input_name: values})[0], dtype=np.float32)
    expected_decisions = values[:, 0].astype(np.int8)
    actual_decisions = route_decisions(actual)
    diff = np.abs(actual - expected)
    max_diff = float(diff.max()) if diff.size else 0.0
    decision_mismatch = expected_decisions != actual_decisions
    counts = {
        "short": int((expected_decisions == -1).sum()),
        "flat": int((expected_decisions == 0).sum()),
        "long": int((expected_decisions == 1).sum()),
    }
    inference = {
        "passed": bool(max_diff <= 1e-7 and not np.any(decision_mismatch)),
        "rows": int(values.shape[0]),
        "unique_route_signal_values": unique_values,
        "max_abs_probability_diff": max_diff,
        "decision_mismatch_count": int(decision_mismatch.sum()),
        "expected_decision_counts": counts,
        "actual_decision_counts": {
            "short": int((actual_decisions == -1).sum()),
            "flat": int((actual_decisions == 0).sum()),
            "long": int((actual_decisions == 1).sum()),
        },
        "input_name": input_name,
        "output_name": output_name,
    }
    receipt = {
        "passed": bool(inference["passed"]),
        "onnx_model": rel(onnx_path),
        "onnx_model_sha256": sha256_file_lf_normalized(onnx_path),
        "probability_parity": {
            "rows": inference["rows"],
            "max_abs_probability_diff": inference["max_abs_probability_diff"],
            "tolerance": 1e-7,
        },
        "decision_parity": {
            "decision_mismatch_count": inference["decision_mismatch_count"],
            "expected_counts": inference["expected_decision_counts"],
            "actual_counts": inference["actual_decision_counts"],
        },
        "runtime_claim_boundary": "python_and_onnx_parity_only_no_runtime_authority",
    }
    return inference, receipt


def feature_order_parity_receipt() -> dict[str, Any]:
    rows = read_csv_rows(RUNTIME_FEATURE_ORDER)
    adapter_order = [row.get("feature_name", "") for row in rows]
    adapter_hash = ordered_hash(adapter_order)
    return {
        "passed": bool(adapter_order == list(FEATURE_ORDER) and adapter_hash == FEATURE_ORDER_HASH),
        "adapter_runtime_feature_order_path": rel(RUNTIME_FEATURE_ORDER),
        "adapter_runtime_feature_order": adapter_order,
        "adapter_runtime_feature_order_hash": adapter_hash,
        "onnx_input_feature_order": list(FEATURE_ORDER),
        "onnx_input_feature_order_hash": FEATURE_ORDER_HASH,
        "known_differences": [
            "logical feature route_signal_value(논리 피처 경로 신호값)는 runtime CSV(런타임 CSV)에서 run322b_route_signal(322B 실행 신호) 별칭으로 쓰인다."
        ],
    }


def copy_onnx_and_features(feature_exports: Mapping[str, Any], common_files_root: Path) -> list[dict[str, Any]]:
    copied = [copy_to_common(ONNX_MODEL, f"{COMMON_ROOT}/models/{ONNX_MODEL.name}", common_files_root)]
    seen: set[str] = set()
    for export in feature_exports.values():
        source = ROOT / str(export["path"])
        if source.name in seen:
            continue
        seen.add(source.name)
        copied.append(copy_to_common(source, f"{COMMON_ROOT}/features/{source.name}", common_files_root))
    return copied


def build_onnx_attempts(
    queue_rows: Sequence[Mapping[str, str]],
    feature_exports: Mapping[str, Any],
    *,
    include_routed: bool,
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    model_common_path = f"{COMMON_ROOT}/models/{ONNX_MODEL.name}"
    for queue_row in queue_rows:
        token = base.variant_token(queue_row, 44)
        for runtime_split, split_token in (("validation_is", "val"), ("oos", "oos")):
            for tier_key, tier_label, tier_token in (("tier_a", mt5.TIER_A, "tier_a"), ("tier_b", mt5.TIER_B, "tier_b")):
                rules = source_rules(tier_token, split_token)
                from_date, to_date = source_dates(tier_token, split_token)
                key = f"{SELECTED_BRANCH}__{tier_key}__{runtime_split}"
                feature_name = Path(str(feature_exports[key]["path"])).name
                attempt_name = f"{token}_{tier_token}_{split_token}_onnx"
                attempt = attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=325,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=attempt_name,
                    tier=tier_label,
                    split=runtime_split,
                    model_path=model_common_path,
                    model_id=f"{RUN_ID}_{token}_{tier_token}_onnx",
                    model_backend="onnx",
                    feature_path=f"{COMMON_ROOT}/features/{feature_name}",
                    feature_count=1,
                    feature_order_hash=FEATURE_ORDER_HASH,
                    short_threshold=rules["short_threshold"],
                    long_threshold=rules["long_threshold"],
                    min_margin=rules["min_margin"],
                    invert_signal=rules["invert_signal"],
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier=tier_key,
                    attempt_role="tier_only_total" if tier_key == "tier_a" else "tier_b_fallback_only_total",
                    record_view_prefix=f"mt5_{token}_{tier_token}_onnx",
                    max_hold_bars=rules["max_hold_bars"],
                    common_root=COMMON_ROOT,
                    close_on_flat_signal=rules["close_on_flat_signal"],
                    reverse_on_opposite_signal=rules["reverse_on_opposite_signal"],
                    close_only_on_opposite_signal=rules["close_only_on_opposite_signal"],
                    extra_set_values=rules["extra_set_values"],
                )
                base.attach_attempt_identity(attempt, queue_row)
                attempt["signal_policy"] = "run322b_route_signal -1/0/+1 through ONNX identity probability graph"
                attempt["source_stage322_set"] = rel(source_set_path(tier_token, split_token))
                attempt["source_stage322_feature"] = rel(ROOT / str(feature_exports[key]["path"]))
                attempts.append(attempt)
            if include_routed:
                rules = source_rules("routed", split_token)
                from_date, to_date = source_dates("routed", split_token)
                tier_a_key = f"{SELECTED_BRANCH}__tier_a__{runtime_split}"
                tier_b_key = f"{SELECTED_BRANCH}__tier_b__{runtime_split}"
                tier_a_feature = Path(str(feature_exports[tier_a_key]["path"])).name
                tier_b_feature = Path(str(feature_exports[tier_b_key]["path"])).name
                attempt_name = f"{token}_routed_{split_token}_onnx"
                attempt = attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=325,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=attempt_name,
                    tier=mt5.TIER_AB,
                    split=runtime_split,
                    model_path=model_common_path,
                    model_id=f"{RUN_ID}_{token}_tier_a_onnx",
                    model_backend="onnx",
                    feature_path=f"{COMMON_ROOT}/features/{tier_a_feature}",
                    feature_count=1,
                    feature_order_hash=FEATURE_ORDER_HASH,
                    short_threshold=rules["short_threshold"],
                    long_threshold=rules["long_threshold"],
                    min_margin=rules["min_margin"],
                    invert_signal=rules["invert_signal"],
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier="tier_a",
                    attempt_role="actual_routed_total",
                    record_view_prefix=f"mt5_{token}_actual_routed_onnx",
                    max_hold_bars=rules["max_hold_bars"],
                    common_root=COMMON_ROOT,
                    fallback_enabled=True,
                    fallback_model_path=model_common_path,
                    fallback_model_id=f"{RUN_ID}_{token}_tier_b_onnx",
                    fallback_model_backend="onnx",
                    fallback_feature_path=f"{COMMON_ROOT}/features/{tier_b_feature}",
                    fallback_feature_count=1,
                    fallback_feature_order_hash=FEATURE_ORDER_HASH,
                    fallback_short_threshold=rules["fallback_short_threshold"],
                    fallback_long_threshold=rules["fallback_long_threshold"],
                    fallback_min_margin=rules["fallback_min_margin"],
                    fallback_invert_signal=rules["fallback_invert_signal"],
                    close_on_flat_signal=rules["close_on_flat_signal"],
                    reverse_on_opposite_signal=rules["reverse_on_opposite_signal"],
                    close_only_on_opposite_signal=rules["close_only_on_opposite_signal"],
                    extra_set_values=rules["extra_set_values"],
                )
                base.attach_attempt_identity(attempt, queue_row)
                attempt["signal_policy"] = "Tier A primary + Tier B fallback run322b_route_signal through ONNX identity probability graph"
                attempt["source_stage322_set"] = rel(source_set_path("routed", split_token))
                attempt["source_stage322_feature"] = f"{rel(ROOT / str(feature_exports[tier_a_key]['path']))};{rel(ROOT / str(feature_exports[tier_b_key]['path']))}"
                attempts.append(attempt)
    return attempts


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    configure_base()
    queue_rows = selected_queue_rows()
    feature_exports, split_frames, supply_rows = feature_exports_and_frames()
    write_csv(RUNTIME_SUPPLY, SUPPLY_COLUMNS, supply_rows)
    onnx_export = export_route_signal_onnx(ONNX_MODEL)
    inference, onnx_parity = run_python_parity(ONNX_MODEL, split_frames)
    feature_parity = feature_order_parity_receipt()
    if not feature_parity["passed"]:
        raise RuntimeError("feature order parity failed")
    if not onnx_parity["passed"]:
        raise RuntimeError("ONNX probability or decision parity failed")
    common_copies = copy_onnx_and_features(feature_exports, Path(args.common_files_root))
    full_attempts = build_onnx_attempts(queue_rows, feature_exports, include_routed=not args.no_routed)
    start_index = max(0, int(args.start_index))
    end_index = start_index + int(args.limit) if args.limit is not None else None
    attempts = full_attempts[start_index:end_index]
    write_json(ONNX_EXPORT_REPORT, onnx_export)
    write_json(PYTHON_INFERENCE_CHECK, inference)
    write_json(FEATURE_ORDER_PARITY, feature_parity)
    write_json(ONNX_PARITY_RECEIPT, onnx_parity)
    return {
        "stage_id": STAGE_ID,
        "stage_number": 325,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_root": RUN_ROOT,
        "selected_candidate": SELECTED_CANDIDATE,
        "selected_branch": SELECTED_BRANCH,
        "adapter_package": ADAPTER_PACKAGE_ID,
        "attempts": attempts,
        "planned_attempt_count": len(full_attempts),
        "common_copies": common_copies,
        "feature_exports": feature_exports,
        "onnx_export": onnx_export,
        "python_inference_check": inference,
        "feature_order_parity": feature_parity,
        "onnx_parity": onnx_parity,
        "runtime_supply_matrix": supply_rows,
        "route_coverage": base.route_coverage_from_supply(supply_rows),
        "model_family": "onnx_identity_probability_graph_for_discrete_route_signal",
        "feature_set_id": "stage323_adapter_runtime_feature_order_run322b_route_signal",
        "label_id": "not_applicable_precomputed_route_signal",
        "split_contract": "Stage322 run322A payload split labels validation and oos",
        "claim_boundary": BOUNDARY,
    }


def execute_or_materialize(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": "materialized_only_no_mt5_runtime_reproduction",
        }
    return base.execute_prepared(
        prepared,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=Path(args.common_files_root),
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
        runtime_timeout_seconds=int(args.runtime_timeout_seconds),
    )


def merge_if_requested(result: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.merge_existing:
        return base.merge_existing_result(result, start_index=int(args.start_index), limit=args.limit)
    return dict(result)


def classify_status(
    result: Mapping[str, Any],
    materialize_only: bool,
    runtime_receipt: Mapping[str, Any] | None,
) -> tuple[str, str, str, str, str]:
    if materialize_only:
        return (
            STATUS_PREPARED,
            "onnx_export_and_python_parity_prepared_no_mt5",
            "partial",
            "not_claimed",
            "run325A_execute_mt5_runtime_reproduction",
        )
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    planned = int(result.get("planned_attempt_count", len(attempts)) or len(attempts))
    completed_exec = sum(1 for item in execution_results if item.get("status") == "completed")
    completed_kpi = sum(1 for item in kpis if item.get("status") == "completed")
    runtime_passed = bool(runtime_receipt and runtime_receipt.get("passed"))
    if completed_exec == planned and completed_kpi >= planned and runtime_passed:
        return (STATUS_COMPLETED, JUDGMENT_COMPLETED, "completed", "complete_pending_main_push", NEXT_ACTION_WHEN_COMPLETE)
    if kpis:
        return (
            "partial_cp322a_onnx_runtime_reproduction_requires_repair",
            "onnx_export_python_parity_passed_but_mt5_runtime_reproduction_or_metric_parity_incomplete",
            "partial_or_blocked",
            "not_claimed",
            "repair_or_rerun_run325A_mt5_runtime_reproduction",
        )
    return (
        "blocked_cp322a_onnx_runtime_reproduction_no_mt5_kpi",
        "onnx_export_python_parity_passed_but_mt5_runtime_reproduction_blocked",
        "blocked",
        "not_claimed",
        "repair_or_block_run325A_mt5_runtime_reproduction",
    )


def attempt_summary_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    by_attempt = {item.get("attempt_name"): item for item in result.get("execution_results", [])}
    rows: list[dict[str, Any]] = []
    for index, attempt in enumerate(result.get("attempts", []), start=1):
        execution = by_attempt.get(attempt.get("attempt_name"), {})
        rows.append(
            {
                "attempt_index": index,
                "attempt_name": attempt.get("attempt_name"),
                "selected_candidate": SELECTED_CANDIDATE,
                "adapter_package": ADAPTER_PACKAGE_ID,
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "status": execution.get("status", "prepared_not_executed"),
                "runtime_output_status": execution.get("runtime_outputs", {}).get("status", "not_available"),
                "model_backend": "onnx",
                "feature_order_hash": FEATURE_ORDER_HASH,
                "source_stage322_set": attempt.get("source_stage322_set"),
                "source_stage322_feature": attempt.get("source_stage322_feature"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "set_path": attempt.get("set", {}).get("path"),
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def kpi_index_from_rows(rows: Sequence[Mapping[str, Any]], *, source: bool) -> dict[tuple[str, str, str], dict[str, Any]]:
    indexed: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in rows:
        record_view = str(row.get("record_view", ""))
        report = str(row.get("report", ""))
        if source and SELECTED_BRANCH not in record_view and SELECTED_BRANCH not in report:
            continue
        if not source and "onnx" not in record_view and "onnx" not in report:
            continue
        metrics = parse_metrics(row.get("metrics", {}))
        key = (str(row.get("split", "")), str(row.get("tier_scope", "")), str(row.get("route_role", "")))
        indexed[key] = {"row": dict(row), "metrics": metrics}
    return indexed


def runtime_parity_receipt(result: Mapping[str, Any]) -> dict[str, Any]:
    source_rows = read_csv_rows(SOURCE_KPI_SUMMARY)
    source = kpi_index_from_rows(source_rows, source=True)
    actual = kpi_index_from_rows(result.get("mt5_kpi_records", []), source=False)
    tolerances = {
        "net_profit": 0.01,
        "profit_factor": 0.01,
        "max_drawdown_amount": 0.01,
        "max_drawdown_percent": 0.01,
        "recovery_factor": 0.01,
        "expectancy": 0.01,
        "trade_count": 0.0,
        "order_attempt_count": 0.0,
        "fill_count": 0.0,
        "reject_count": 0.0,
        "skip_count": 0.0,
        "model_ok_count": 0.0,
        "model_fail_count": 0.0,
    }
    required_keys = [
        ("validation_is", mt5.TIER_A, "tier_only_total"),
        ("validation_is", mt5.TIER_B, "tier_b_fallback_only_total"),
        ("validation_is", mt5.TIER_AB, "actual_routed_total"),
        ("oos", mt5.TIER_A, "tier_only_total"),
        ("oos", mt5.TIER_B, "tier_b_fallback_only_total"),
        ("oos", mt5.TIER_AB, "actual_routed_total"),
    ]
    compare_rows: list[dict[str, Any]] = []
    for key in required_keys:
        source_entry = source.get(key)
        actual_entry = actual.get(key)
        for metric, tolerance in tolerances.items():
            if source_entry is None or actual_entry is None:
                compare_rows.append(
                    {
                        "comparison_key": "|".join(key),
                        "split": key[0],
                        "tier_scope": key[1],
                        "route_role": key[2],
                        "metric": metric,
                        "source_value": "",
                        "onnx_value": "",
                        "absolute_diff": "",
                        "tolerance": tolerance,
                        "status": "missing",
                    }
                )
                continue
            source_value = metric_float(source_entry["metrics"], metric)
            actual_value = metric_float(actual_entry["metrics"], metric)
            diff = abs(source_value - actual_value)
            compare_rows.append(
                {
                    "comparison_key": "|".join(key),
                    "split": key[0],
                    "tier_scope": key[1],
                    "route_role": key[2],
                    "metric": metric,
                    "source_value": source_value,
                    "onnx_value": actual_value,
                    "absolute_diff": diff,
                    "tolerance": tolerance,
                    "status": "passed" if diff <= tolerance else "failed",
                }
            )
    write_csv(RUNTIME_COMPARISON, RUNTIME_COMPARE_COLUMNS, compare_rows)
    passed = bool(compare_rows) and all(row["status"] == "passed" for row in compare_rows)
    return {
        "passed": passed,
        "run_id": RUN_ID,
        "research_path": rel(ROOT / PRODUCER),
        "runtime_path": [row.get("ini_path") for row in attempt_summary_rows(result)],
        "shared_contract": {
            "feature_order": list(FEATURE_ORDER),
            "feature_order_hash": FEATURE_ORDER_HASH,
            "decision_thresholds": {"short": 0.55, "long": 0.55, "min_margin": 0.0},
            "risk_logic": "Stage322 set mirrored: max_hold_bars=1, close_on_flat_signal=true, ATR SL/TP and model risk sizing copied",
            "runtime_handoff": rel(RUNTIME_HANDOFF),
        },
        "known_differences": [
            "Stage322 source model backend(원천 모델 백엔드)은 ebm_table(표 기반 모델)이고 Stage325 backend(325단계 백엔드)은 onnx(온엑스)다.",
            "Both surfaces(두 표면)는 run322b_route_signal -1/0/+1을 같은 short/flat/long(매도/관망/매수) probability(확률)로 해석해야 한다.",
        ],
        "parity_check": {
            "source_kpi": rel(SOURCE_KPI_SUMMARY),
            "onnx_kpi": rel(MT5_KPI_SUMMARY),
            "comparison_csv": rel(RUNTIME_COMPARISON),
            "compared_rows": len(compare_rows),
            "failed_rows": sum(1 for row in compare_rows if row["status"] != "passed"),
        },
        "parity_identity": {
            "onnx_model": rel(ONNX_MODEL),
            "onnx_model_sha256": sha256_file_lf_normalized(ONNX_MODEL),
            "feature_order_hash": FEATURE_ORDER_HASH,
            "compile": result.get("compile", {}),
            "attempt_count": len(result.get("attempts", [])),
            "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        },
        "runtime_claim_boundary": "runtime_reproduction_receipt_only_no_runtime_authority",
    }


def compact_kpi_summary(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in result.get("mt5_kpi_records", []):
        metrics = parse_metrics(row.get("metrics", {}))
        rows.append(
            {
                "split": row.get("split"),
                "tier_scope": row.get("tier_scope"),
                "route_role": row.get("route_role"),
                "net_profit": metric_float(metrics, "net_profit"),
                "profit_factor": metric_float(metrics, "profit_factor"),
                "trade_count": int(metric_float(metrics, "trade_count")),
                "expectancy": metric_float(metrics, "expectancy"),
                "max_drawdown_percent": metric_float(metrics, "max_drawdown_percent"),
                "recovery_factor": metric_float(metrics, "recovery_factor"),
            }
        )
    return rows


def final_report_markdown(
    result: Mapping[str, Any],
    status: str,
    judgment: str,
    external_status: str,
    goal_achieve: str,
    next_action: str,
    runtime_receipt: Mapping[str, Any],
) -> str:
    attempts = list(result.get("attempts", []))
    kpis = list(result.get("mt5_kpi_records", []))
    comparison = runtime_receipt.get("parity_check", {})
    kpi_rows = compact_kpi_summary(result)
    kpi_lines = [
        (
            f"- {row['split']} / {row['tier_scope']} / {row['route_role']}: "
            f"net profit(순수익) `{row['net_profit']:.2f}`, PF(수익 팩터) `{row['profit_factor']:.2f}`, "
            f"trades(거래) `{row['trade_count']}`, DD%(손실폭 %) `{row['max_drawdown_percent']:.2f}`"
        )
        for row in kpi_rows
    ] or ["- MT5 KPI(메타트레이더5 핵심 성과 지표): `not_available`"]
    return "\n".join(
        [
            "# run325A Final Candidate Package Report(최종 후보 패키지 보고)",
            "",
            f"- stage_id(단계 ID): `{STAGE_ID}`",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`",
            f"- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`",
            f"- status(상태): `{status}`",
            f"- judgment(판정): `{judgment}`",
            f"- ONNX model(온엑스 모델): `{rel(ONNX_MODEL)}`",
            f"- feature_order_hash(피처 순서 해시): `{FEATURE_ORDER_HASH}`",
            f"- Python inference check(파이썬 추론 확인): `{rel(PYTHON_INFERENCE_CHECK)}`",
            f"- ONNX parity receipt(온엑스 동등성 영수증): `{rel(ONNX_PARITY_RECEIPT)}`",
            f"- MT5 runtime reproduction(MT5 런타임 재현): `{external_status}`",
            f"- attempts(시도): `{len(kpis)}/{len(attempts)}`",
            f"- runtime_metric_comparison(런타임 지표 비교): `{comparison.get('compared_rows', 0)}` rows(행), `{comparison.get('failed_rows', 0)}` failed(실패)",
            f"- Goal Achieve(목표 달성): `{goal_achieve}`",
            f"- next_action(다음 행동): `{next_action}`",
            "",
            "## KPI(핵심 성과 지표)",
            "",
            *kpi_lines,
            "",
            "## Package Meaning(패키지 의미)",
            "",
            "cp322A(322A 후보)는 run322b_route_signal(322B 실행 신호) 하나를 ONNX probability graph(온엑스 확률 그래프)로 넘기는 Adapter candidate package(어댑터 후보 패키지)다.",
            "Effect(효과): feature order(피처 순서), decision surface(판단 표면), risk logic(위험 로직), runtime handoff(런타임 인계)를 같은 경로에서 추적한다.",
            "",
            "## Boundary(경계)",
            "",
            f"`{BOUNDARY}`",
            "",
            "Effect(효과): 이 보고서는 ONNX package handoff(온엑스 패키지 인계) 근거이며 live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포)를 주장하지 않는다.",
        ]
    )


def decision_markdown(status: str, judgment: str, goal_achieve: str, next_action: str) -> str:
    return "\n".join(
        [
            "# Stage325 Decision(325단계 결정): ONNX Package Ready, Main Push Pending(온엑스 패키지 준비, 메인 푸시 대기)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- selected_candidate(선택 후보): `{SELECTED_CANDIDATE}`",
            f"- Adapter package(어댑터 패키지): `{ADAPTER_PACKAGE_ID}`",
            f"- status(상태): `{status}`",
            f"- judgment(판정): `{judgment}`",
            f"- Goal Achieve(목표 달성): `{goal_achieve}`",
            f"- next_action(다음 행동): `{next_action}`",
            "",
            "Effect(효과): ONNX export(온엑스 내보내기), Python inference check(파이썬 추론 확인), feature order parity(피처 순서 동등성), ONNX parity(온엑스 동등성), MT5 runtime reproduction(MT5 런타임 재현)을 하나의 패키지로 묶었다.",
            "",
            "Boundary(경계): main push(메인 푸시)가 끝나기 전까지 Goal Achieved(목표 달성 완료)는 최종 선언하지 않는다.",
        ]
    )


def write_outputs(
    result: Mapping[str, Any],
    status: str,
    judgment: str,
    external_status: str,
    goal_achieve: str,
    next_action: str,
    runtime_receipt: Mapping[str, Any],
    created_at: str,
) -> list[Path]:
    attempts = list(result.get("attempts", []))
    kpis = list(result.get("mt5_kpi_records", []))
    attempt_rows = attempt_summary_rows(result)
    write_json(EXECUTION_RESULT, result, bom=True)
    write_csv(ATTEMPT_SUMMARY, tuple(attempt_rows[0].keys()) if attempt_rows else ("status",), attempt_rows)
    write_csv(RUNTIME_SUPPLY, SUPPLY_COLUMNS, result.get("runtime_supply_matrix", []))
    write_csv(MT5_KPI_SUMMARY, dynamic_columns(kpis), kpis)
    write_json(RUNTIME_PARITY_RECEIPT, runtime_receipt)
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": (
                    f"onnx={rel(ONNX_MODEL)};python_parity={rel(ONNX_PARITY_RECEIPT)};"
                    f"feature_order={rel(FEATURE_ORDER_PARITY)};runtime_parity={rel(RUNTIME_PARITY_RECEIPT)}"
                ),
                "evidence_missing": "main_push_receipt_until_git_push_completes",
                "judgment_label": judgment,
                "judgment_class": "onnx_package_ready_for_main_push" if external_status == "completed" else "partial_or_blocked",
                "claim_boundary": BOUNDARY,
                "next_condition": next_action,
                "user_explanation_hook": "ONNX(온엑스) 패키지는 export/parity/runtime reproduction(내보내기/동등성/런타임 재현) 영수증이 있어야 의미가 있다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "onnx_export",
                "status": "passed" if path_exists(ONNX_MODEL) else "failed",
                "evidence_path": rel(ONNX_EXPORT_REPORT),
                "effect": "ONNX model(온엑스 모델)을 만들어 MT5 runtime(메타트레이더5 런타임)에 넘길 수 있게 한다.",
            },
            {
                "gate_name": "python_inference_and_onnx_parity",
                "status": "passed" if result.get("onnx_parity", {}).get("passed") else "failed",
                "evidence_path": rel(ONNX_PARITY_RECEIPT),
                "effect": "Python inference(파이썬 추론)와 ONNX output(온엑스 출력)이 같은 decision(판단)을 내는지 확인한다.",
            },
            {
                "gate_name": "feature_order_parity",
                "status": "passed" if result.get("feature_order_parity", {}).get("passed") else "failed",
                "evidence_path": rel(FEATURE_ORDER_PARITY),
                "effect": "Adapter feature order(어댑터 피처 순서)와 ONNX input(온엑스 입력)이 일치하는지 확인한다.",
            },
            {
                "gate_name": "mt5_runtime_reproduction",
                "status": external_status,
                "evidence_path": rel(RUNTIME_PARITY_RECEIPT),
                "effect": "MT5 tester(MT5 테스터) 결과가 Stage322(322단계) 원천 런타임 결과와 맞는지 확인한다.",
            },
        ],
    )
    report = final_report_markdown(result, status, judgment, external_status, goal_achieve, next_action, runtime_receipt)
    write_md(FINAL_REPORT, report)
    write_md(SELECTED_FINAL_REPORT, report)
    write_md(DECISION, decision_markdown(status, judgment, goal_achieve, next_action))
    final_paths = [
        SELECTED_QUEUE,
        ONNX_MODEL,
        ONNX_EXPORT_REPORT,
        PYTHON_INFERENCE_CHECK,
        FEATURE_ORDER_PARITY,
        ONNX_PARITY_RECEIPT,
        ATTEMPT_SUMMARY,
        RUNTIME_SUPPLY,
        EXECUTION_RESULT,
        MT5_KPI_SUMMARY,
        RUNTIME_PARITY_RECEIPT,
        RUNTIME_COMPARISON,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        FINAL_REPORT,
        SELECTED_FINAL_REPORT,
        DECISION,
    ]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "external_verification_status": external_status,
        "created_at_utc": created_at,
        "selected_candidate": SELECTED_CANDIDATE,
        "adapter_package": ADAPTER_PACKAGE_ID,
        "onnx_readiness": "export_parity_runtime_reproduction_complete" if external_status == "completed" else "partial",
        "goal_achieve": goal_achieve,
        "next_action": next_action,
        "attempt_count": len(attempts),
        "mt5_kpi_record_count": len(kpis),
        "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final_paths if path_exists(path)},
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    final_paths.append(RUN_MANIFEST)
    lineage = {
        "run_id": RUN_ID,
        "source_inputs": [
            rel(SOURCE_QUEUE),
            rel(SOURCE_PAYLOAD_MANIFEST),
            rel(SOURCE_EXECUTION_RESULT),
            rel(SOURCE_KPI_SUMMARY),
            rel(ADAPTER_MANIFEST_INPUT),
            rel(ADAPTER_HASH_INPUT),
            rel(RUNTIME_FEATURE_ORDER),
            rel(RUNTIME_HANDOFF),
            rel(DECISION_SURFACE),
            rel(RISK_LOGIC),
            rel(ROOT / PRODUCER),
        ],
        "source_hashes": {
            rel(path): sha256_file_lf_normalized(path)
            for path in [
                SOURCE_QUEUE,
                SOURCE_PAYLOAD_MANIFEST,
                SOURCE_EXECUTION_RESULT,
                SOURCE_KPI_SUMMARY,
                ADAPTER_MANIFEST_INPUT,
                ADAPTER_HASH_INPUT,
                RUNTIME_FEATURE_ORDER,
                RUNTIME_HANDOFF,
                DECISION_SURFACE,
                RISK_LOGIC,
                ROOT / PRODUCER,
            ]
            if path_exists(path)
        },
        "producer": rel(ROOT / PRODUCER),
        "consumer": "Stage325 final candidate package report and main push handoff",
        "artifact_paths": [rel(path) for path in final_paths if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final_paths if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_from_adapter_package_to_onnx_runtime_reproduction",
        "lineage_judgment": "connected_with_research_boundary_no_live_or_operating_claim",
    }
    write_json(LINEAGE, lineage)
    final_paths.append(LINEAGE)
    return final_paths


def upsert_ledgers(
    result: Mapping[str, Any],
    status: str,
    judgment: str,
    external_status: str,
    goal_achieve: str,
    next_action: str,
) -> None:
    attempt_count = len(result.get("attempts", []))
    kpi_count = len(result.get("mt5_kpi_records", []))
    upsert_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "onnx_export_parity_runtime_reproduction",
                "status": status,
                "judgment": judgment,
                "path": rel(FINAL_REPORT),
                "notes": (
                    f"selected_candidate={SELECTED_CANDIDATE};adapter_package={ADAPTER_PACKAGE_ID};"
                    f"attempts={attempt_count};mt5_kpi_records={kpi_count};goal_achieve={goal_achieve};next_action={next_action}."
                ),
            }
        ],
        key="run_id",
    )
    upsert_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__onnx_package_runtime_reproduction",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "run325A_onnx_package_runtime_reproduction",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "ONNX export/parity/MT5 runtime reproduction(온엑스 내보내기/동등성/MT5 런타임 재현)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "candidate_package_handoff",
                "scoreboard_lane": "onnx_package_ready_for_main_push" if external_status == "completed" else "partial",
                "status": status,
                "judgment": judgment,
                "path": rel(FINAL_REPORT),
                "primary_kpi": f"attempts={attempt_count};mt5_kpi_records={kpi_count};runtime_parity={external_status}",
                "guardrail_kpi": "no_live_readiness;no_runtime_authority;no_operating_promotion;no_deployment",
                "external_verification_status": external_status,
                "notes": f"selected_candidate={SELECTED_CANDIDATE};goal_achieve={goal_achieve};next_action={next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__onnx_package_runtime_reproduction",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "onnx_package_runtime_reproduction",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "onnx_export_parity_runtime_reproduction",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": BOUNDARY,
                "report_path": rel(FINAL_REPORT),
                "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count};goal_achieve={goal_achieve}.",
            }
        ],
        key="row_id",
    )


def update_artifact_registry(paths: Sequence[Path], created_at: str) -> None:
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": "stage325_onnx_candidate_package_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run325A ONNX export/parity/MT5 runtime reproduction(온엑스 내보내기/동등성/MT5 런타임 재현)",
        }
        for path in paths
        if path_exists(path)
    ]
    upsert_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def update_docs(
    status: str,
    judgment: str,
    external_status: str,
    goal_achieve: str,
    next_action: str,
    kpi_count: int,
    attempt_count: int,
) -> None:
    onnx_readiness = (
        "export_parity_runtime_reproduction_complete"
        if external_status == "completed"
        else "partial_export_and_python_parity_no_mt5_reproduction"
    )
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig") if path_exists(SELECTED) else ""
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- ONNX readiness(온엑스 준비):", f"- ONNX readiness(온엑스 준비): `{onnx_readiness}`")
    selected = replace_line_prefix(selected, "- Goal Achieve(목표 달성):", f"- Goal Achieve(목표 달성): `{goal_achieve}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selected = append_once(selected, "run325A_final_candidate_package_report", f"- run325A_final_candidate_package_report(325A 최종 후보 패키지 보고): `{rel(FINAL_REPORT)}`")
    selected = append_once(selected, "run325A_runtime_parity_receipt", f"- run325A_runtime_parity_receipt(325A 런타임 동등성 영수증): `{rel(RUNTIME_PARITY_RECEIPT)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Review Index(검토 색인)\n"
    review_index = append_once(
        review_index,
        "run325A_final_candidate_package_report",
        "\n".join(
            [
                f"- run325A_final_candidate_package_report(325A 최종 후보 패키지 보고): `{rel(FINAL_REPORT)}`",
                f"- run325A_onnx_parity_receipt(325A 온엑스 동등성 영수증): `{rel(ONNX_PARITY_RECEIPT)}`",
                f"- run325A_runtime_parity_receipt(325A 런타임 동등성 영수증): `{rel(RUNTIME_PARITY_RECEIPT)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    current = replace_line_prefix(current, "- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{BOUNDARY}`")
    summary_line = (
        "- run325A_summary(325A 요약): ONNX export(온엑스 내보내기), Python parity(파이썬 동등성), "
        f"feature order parity(피처 순서 동등성), MT5 runtime reproduction(MT5 런타임 재현)을 `{external_status}`로 기록했다. "
        f"Effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 핵심 성과 지표 기록) `{kpi_count}`개를 "
        f"cp322A 후보 패키지 근거로 묶고, main push(메인 푸시) 전까지 Goal Achieve(목표 달성)는 `{goal_achieve}`로 둔다."
    )
    if "- run325A_summary(325A 요약):" in current:
        current = replace_line_prefix(current, "- run325A_summary(325A 요약):", summary_line)
    else:
        current = append_once(current, "run325A_summary", summary_line)
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        f"- >-\n"
        f"  Stage325(325단계) run325A(325A 실행) ONNX export/parity/runtime reproduction(온엑스 내보내기/동등성/런타임 재현) `{RUN_ID}`. "
        f"Effect(효과): selected candidate(선택 후보) `{SELECTED_CANDIDATE}`와 Adapter package(어댑터 패키지) `{ADAPTER_PACKAGE_ID}`의 "
        f"ONNX package(온엑스 패키지)를 만들고 main push(메인 푸시) 후 Goal Achieve(목표 달성)를 닫을 수 있는 상태로 둔다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage325(325단계) run325A")
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog_line = (
        "- run325A(325A 실행): cp322A(322A 후보) Adapter package(어댑터 패키지)를 ONNX model(온엑스 모델), "
        f"parity receipts(동등성 영수증), MT5 runtime reproduction(MT5 런타임 재현) `{external_status}`로 기록했다. "
        f"Effect(효과): Goal Achieve(목표 달성)는 `{goal_achieve}`이고 next_action(다음 행동)은 `{next_action}`이다."
    )
    if "run325A_export_cp322a_adapter_to_onnx" in changelog:
        changelog = replace_line_prefix(changelog, "- run325A(325A 실행):", changelog_line)
    else:
        changelog = append_once(
            changelog,
            "run325A_export_cp322a_adapter_to_onnx",
            f"## {UPDATED_ON} - Stage325 ONNX Package(325단계 온엑스 패키지)\n\n{changelog_line}",
        )
    write_md(CHANGELOG, changelog)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=300)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--merge-existing", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--no-routed", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    created_at = utc_now()
    prepared = prepare(args)
    result = execute_or_materialize(prepared, args)
    result = merge_if_requested(result, args)
    runtime_receipt: dict[str, Any] = {
        "passed": False,
        "run_id": RUN_ID,
        "parity_check": {"compared_rows": 0, "failed_rows": 0},
        "runtime_claim_boundary": "not_attempted_materialize_only",
    }
    if not args.materialize_only and result.get("mt5_kpi_records"):
        runtime_receipt = runtime_parity_receipt(result)
    status, judgment, external_status, goal_achieve, next_action = classify_status(result, args.materialize_only, runtime_receipt)
    output_paths = write_outputs(result, status, judgment, external_status, goal_achieve, next_action, runtime_receipt, created_at)
    upsert_ledgers(result, status, judgment, external_status, goal_achieve, next_action)
    update_artifact_registry(output_paths, created_at)
    update_docs(status, judgment, external_status, goal_achieve, next_action, len(result.get("mt5_kpi_records", [])), len(result.get("attempts", [])))
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "status": status,
                    "judgment": judgment,
                    "external_verification_status": external_status,
                    "selected_candidate": SELECTED_CANDIDATE,
                    "adapter_package": ADAPTER_PACKAGE_ID,
                    "onnx_readiness": "export_parity_runtime_reproduction_complete" if external_status == "completed" else "partial",
                    "goal_achieve": goal_achieve,
                    "planned_attempt_count": result.get("planned_attempt_count"),
                    "attempt_count": len(result.get("attempts", [])),
                    "mt5_kpi_records": len(result.get("mt5_kpi_records", [])),
                    "runtime_parity_passed": runtime_receipt.get("passed"),
                    "next_action": next_action,
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
