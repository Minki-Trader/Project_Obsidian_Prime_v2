from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import onnx
import pandas as pd
from onnx import TensorProto, helper, numpy_helper

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.models.onnx_bridge import classifier_classes, sha256_file
from stage_pipelines.stage_frontier_71 import frontier71d_mt5_runtime_probe_economics_native_scout as f71d
from stage_pipelines.stage_frontier_74 import frontier74b_microburst_turnover_raw_label_and_proxy_scout as base
from stage_pipelines.stage_frontier_74 import frontier74c_microburst_label_feature_repair_proxy as repair
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
)


STAGE_ID = "stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path"
RUN_ID = "frontier74E_mt5_microburst_negative_control_runtime_probe_v1"
PARENT_RUN_ID = "frontier74D_pre_mt5_grok_microburst_negative_control_runtime_probe_v1"
NEXT_RUN_ID = "frontier74F_proxy_runtime_gap_or_closeout_decision_v1"
CLAIM_BOUNDARY = (
    "negative_control_runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
MODEL_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "features"
VETO_ROOT = RUN_ROOT / "runtime_veto_tapes"
MT5_ROOT = RUN_ROOT / "mt5"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier74E_mt5_microburst_negative_control_runtime_probe"

F74D_MANIFEST = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "run_manifest.json"
F74C_SUMMARY = STAGE_ROOT / "02_runs/frontier74C_microburst_label_feature_repair_proxy_v1/f74c_summary.json"
F74C_CANDIDATES = STAGE_ROOT / "02_runs/frontier74C_microburst_label_feature_repair_proxy_v1/f74c_candidate_results.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"

ORIGINAL_GROK_TARGET_ID = "f74c_1212"
PRIMARY_CANDIDATE_ID = "f74c_1161"
THRESHOLD_EPSILON = 1e-7


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F74E negative-control MT5 runtime probe.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--wait-timeout-seconds", type=int, default=300)
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    write_text(path, json.dumps(json_ready(payload), ensure_ascii=False, indent=2))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        rows = [{"empty": "true"}]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: json_ready(row.get(name, "")) for name in fieldnames})


def write_md(path: Path, lines: Sequence[str]) -> None:
    write_text(path, "\n".join(lines))


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.rstrip())


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise FileNotFoundError(f"ledger header missing: {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_ROOT, FEATURE_ROOT, VETO_ROOT, MT5_ROOT, MT5_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def required_inputs() -> list[Path]:
    return [F74D_MANIFEST, F74C_SUMMARY, F74C_CANDIDATES, base.FWD12_INPUT, base.FWD12_FEATURE_ORDER, base.RAW_US100, ALPHA_LEDGER, RUN_REGISTRY]


def candidate_row() -> Mapping[str, Any]:
    candidates = pd.read_csv(io_path(F74C_CANDIDATES))
    row = candidates.loc[candidates["candidate_id"].astype(str).eq(PRIMARY_CANDIDATE_ID)]
    if row.empty:
        raise RuntimeError(f"candidate_not_found:{PRIMARY_CANDIDATE_ID}")
    return row.iloc[0].to_dict()


def binary_probabilities(model: Any, values: pd.DataFrame | np.ndarray) -> np.ndarray:
    raw = np.asarray(model.predict_proba(values), dtype="float64")
    classes = classifier_classes(model)
    if 0 not in classes or 1 not in classes:
        raise RuntimeError(f"binary_model_class_coverage_failed:{classes}")
    class_to_index = {int(label): index for index, label in enumerate(classes)}
    return np.column_stack([raw[:, class_to_index[0]], raw[:, class_to_index[1]]])


def train_context() -> dict[str, Any]:
    source = candidate_row()
    frame = base.load_frame()
    raw = base.load_raw()
    positions = base.align_raw(frame, raw)
    axis = next(axis for axis in repair.repair_axes() if axis.axis_id == str(source["axis_id"]))
    path = base.compute_axis_path(frame, raw, positions, axis)
    y = repair.label_modes(frame, path, axis)[str(source["label_mode"])]
    y = y.astype(float)
    y[~np.isfinite(path["pnl"])] = np.nan
    features = base.feature_bundles(base.feature_order())[str(source["feature_bundle"])]
    gate = base.gate_mask(frame, str(source["gate_id"]), base.gate_thresholds(frame))
    finite = np.isfinite(y) & np.isfinite(path["pnl"])
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool) & gate & finite
    model = base.model_factories()[str(source["model_id"])]()
    model.fit(frame.loc[train_mask, features], y[train_mask].astype(int))
    proba = binary_probabilities(model, frame.loc[:, features])
    score = proba[:, 1]
    threshold = float(source["score_threshold"])
    raw_selected = gate & finite & (score >= threshold)
    selected = base.lifecycle_filter(frame, raw_selected, positions, axis.horizon_bars)
    proxy_kpi_by_split: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        split_selected = frame["split"].astype(str).eq(split).to_numpy(dtype=bool) & selected
        proxy_kpi_by_split[split] = base.trade_metrics(
            frame.loc[split_selected, "timestamp"],
            path["pnl"][split_selected],
            path["direction"][split_selected],
        )
    return {
        "source_candidate": dict(source),
        "frame": frame,
        "raw": raw,
        "positions": positions,
        "axis": axis,
        "path": path,
        "features": list(features),
        "model": model,
        "binary_proba": proba,
        "score": score,
        "threshold": threshold,
        "raw_selected": raw_selected,
        "selected": selected,
        "event_mask": gate & finite,
        "proxy_kpi_by_split": proxy_kpi_by_split,
    }


def export_binary_sklearn_to_onnx(model: Any, output_path: Path, feature_count: int) -> dict[str, Any]:
    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import FloatTensorType

    options = {id(model): {"zipmap": False}}
    if hasattr(model, "named_steps"):
        for step in model.named_steps.values():
            if hasattr(step, "predict_proba"):
                options[id(step)] = {"zipmap": False}
    onnx_model = convert_sklearn(
        model,
        initial_types=[("float_input", FloatTensorType([None, int(feature_count)]))],
        options=options,
        target_opset=12,
    )
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    onnx.save(onnx_model, str(io_path(output_path)))
    return {"path": rel(output_path), "sha256": sha256_file(output_path)}


def output_shape(output: Any) -> list[Any]:
    dims: list[Any] = []
    for dim in output.type.tensor_type.shape.dim:
        if dim.dim_value:
            dims.append(int(dim.dim_value))
        elif dim.dim_param:
            dims.append(str(dim.dim_param))
        else:
            dims.append(None)
    return dims


def find_binary_probability_output(model: Any) -> str:
    candidates = [
        output.name
        for output in model.graph.output
        if output.type.WhichOneof("value") == "tensor_type" and len(output_shape(output)) == 2 and output_shape(output)[-1] == 2
    ]
    if len(candidates) != 1:
        raise RuntimeError(f"binary_probability_output_not_unique:{candidates}")
    return candidates[0]


def patch_binary_onnx_to_short_three_columns(binary_path: Path, patched_path: Path) -> dict[str, Any]:
    model = onnx.load(str(io_path(binary_path)))
    prob_name = find_binary_probability_output(model)
    axes = numpy_helper.from_array(np.asarray([1], dtype=np.int64), name="slice_axes_col")
    steps = numpy_helper.from_array(np.asarray([1], dtype=np.int64), name="slice_steps_col")
    start0 = numpy_helper.from_array(np.asarray([0], dtype=np.int64), name="slice_start_col0")
    end1 = numpy_helper.from_array(np.asarray([1], dtype=np.int64), name="slice_end_col1")
    start1 = numpy_helper.from_array(np.asarray([1], dtype=np.int64), name="slice_start_col1")
    end2 = numpy_helper.from_array(np.asarray([2], dtype=np.int64), name="slice_end_col2")
    zero_scalar = numpy_helper.from_array(np.asarray([0.0], dtype=np.float32), name="zero_scalar")
    model.graph.initializer.extend([axes, steps, start0, end1, start1, end2, zero_scalar])
    model.graph.node.extend(
        [
            helper.make_node("Slice", [prob_name, "slice_start_col0", "slice_end_col1", "slice_axes_col", "slice_steps_col"], ["flat_col"], name="SliceFlatProbability"),
            helper.make_node("Slice", [prob_name, "slice_start_col1", "slice_end_col2", "slice_axes_col", "slice_steps_col"], ["short_col"], name="SliceShortProbability"),
            helper.make_node("Mul", ["flat_col", "zero_scalar"], ["long_zero_col"], name="BuildZeroLongProbability"),
            helper.make_node("Concat", ["short_col", "flat_col", "long_zero_col"], ["probabilities_3"], name="BuildThreeColumnProbability", axis=1),
        ]
    )
    del model.graph.output[:]
    model.graph.output.extend([helper.make_tensor_value_info("probabilities_3", TensorProto.FLOAT, [None, 3])])
    onnx.checker.check_model(model)
    io_path(patched_path.parent).mkdir(parents=True, exist_ok=True)
    onnx.save(model, str(io_path(patched_path)))
    return {
        "binary_probability_output": prob_name,
        "patched_probability_output": "probabilities_3",
        "path": rel(patched_path),
        "sha256": sha256_file(patched_path),
        "schema": "[p_short,p_flat,p_long=0]",
    }


def onnx_probability(onnx_path: Path, values: np.ndarray, expected_cols: int) -> np.ndarray:
    import onnxruntime as ort

    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: values.astype("float32")})
    candidates = [np.asarray(output, dtype="float64") for output in outputs if isinstance(output, np.ndarray) and output.ndim == 2 and output.shape[1] == expected_cols]
    if len(candidates) != 1:
        raise RuntimeError(f"onnx_probability_output_not_unique:{[getattr(output, 'shape', None) for output in outputs]}")
    return candidates[0]


def reproduction_rows(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    frame = context["frame"]
    for split in ("validation", "oos"):
        split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
        proxy = context["proxy_kpi_by_split"][split]
        source = context["source_candidate"]
        source_count = int(float(source.get(f"{split}_trade_count", 0) or 0))
        reproduced_count = int((split_mask & context["selected"]).sum())
        count_ratio = float(min(source_count, reproduced_count) / max(source_count, reproduced_count, 1))
        rows.append(
            {
                "split": split,
                "source_selected_count": source_count,
                "reproduced_selected_count": reproduced_count,
                "overlap_count": reproduced_count if source_count == reproduced_count else "",
                "overlap_ratio_vs_source": count_ratio,
                "count_diff": reproduced_count - source_count,
                "source_net_profit": source.get(f"{split}_net_profit"),
                "source_profit_factor": source.get(f"{split}_profit_factor"),
                "source_max_drawdown_percent": source.get(f"{split}_max_drawdown_percent"),
                "source_trades_day": source.get(f"{split}_trades_day"),
                "reproduced_net_profit": proxy.get("net_profit"),
                "reproduced_profit_factor": proxy.get("profit_factor"),
                "reproduced_max_drawdown_percent": proxy.get("max_drawdown_percent"),
                "reproduced_trades_day": proxy.get("trades_day"),
                "metric_reproduction_boundary": "same deterministic replay; timestamp source file unavailable for repaired candidate(결정적 재현, 수리 후보별 시각 원천 파일 없음)",
            }
        )
    return rows


def parity_rows(context: Mapping[str, Any], raw_onnx_path: Path, patched_onnx_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    frame = context["frame"]
    features = context["features"]
    threshold = float(context["threshold"])
    runtime_threshold = threshold - THRESHOLD_EPSILON
    probability_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        subset = frame.loc[frame["split"].astype(str).eq(split)]
        idx = subset.index.to_numpy()
        values = subset.loc[:, features].to_numpy(dtype="float64")
        binary_expected = context["binary_proba"][idx]
        patched_expected = np.column_stack([binary_expected[:, 1], binary_expected[:, 0], np.zeros(len(binary_expected))])
        sample_values = values[: min(len(values), 4096)]
        sample_binary = binary_expected[: len(sample_values)]
        sample_patched = patched_expected[: len(sample_values)]
        raw_actual = onnx_probability(raw_onnx_path, sample_values, 2)
        patched_actual = onnx_probability(patched_onnx_path, sample_values, 3)
        raw_diff = np.abs(raw_actual - sample_binary)
        patched_diff = np.abs(patched_actual - sample_patched)
        probability_rows.append(
            {
                "split": split,
                "sample_rows": len(sample_values),
                "raw_binary_max_abs_diff": float(raw_diff.max()) if raw_diff.size else 0.0,
                "patched_three_col_max_abs_diff": float(patched_diff.max()) if patched_diff.size else 0.0,
                "patched_long_col_max_abs": float(np.abs(patched_actual[:, 2]).max()) if len(patched_actual) else 0.0,
                "passed": bool((float(raw_diff.max()) if raw_diff.size else 0.0) <= 1e-5 and (float(patched_diff.max()) if patched_diff.size else 0.0) <= 1e-5),
            }
        )
        all_patched = onnx_probability(patched_onnx_path, values, 3)
        onnx_raw_signal = context["event_mask"][idx] & (all_patched[:, 0] >= runtime_threshold)
        onnx_vetoed_signal = onnx_raw_signal & context["selected"][idx]
        selected_expected = context["selected"][idx]
        signal_rows.append(
            {
                "split": split,
                "rows": len(subset),
                "expected_selected_count": int(selected_expected.sum()),
                "onnx_raw_signal_count": int(onnx_raw_signal.sum()),
                "onnx_vetoed_signal_count": int(onnx_vetoed_signal.sum()),
                "signal_count_diff_after_veto": int(onnx_vetoed_signal.sum() - selected_expected.sum()),
                "signal_mismatch_count_after_veto": int((onnx_vetoed_signal != selected_expected).sum()),
                "source_threshold": threshold,
                "runtime_threshold": runtime_threshold,
                "threshold_epsilon": THRESHOLD_EPSILON,
                "passed": bool(int((onnx_vetoed_signal != selected_expected).sum()) == 0),
            }
        )
    return probability_rows, signal_rows


def materialize(context: Mapping[str, Any], common_files_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    candidate_id = f"f74e_negative_control_{PRIMARY_CANDIDATE_ID}"
    model_path = MODEL_ROOT / f"{candidate_id}.joblib"
    raw_onnx_path = MODEL_ROOT / f"{candidate_id}.binary_raw.onnx"
    patched_onnx_path = MODEL_ROOT / f"{candidate_id}.onnx"
    feature_order_path = MODEL_ROOT / f"{candidate_id}_feature_order.txt"
    feature_csv_path = FEATURE_ROOT / f"{candidate_id}_features.csv"
    veto_path = VETO_ROOT / f"{candidate_id}_selected_entry_runtime_veto_tape.csv"
    io_path(MODEL_ROOT).mkdir(parents=True, exist_ok=True)
    joblib.dump(context["model"], io_path(model_path))
    io_path(feature_order_path).write_text("\n".join(context["features"]) + "\n", encoding="utf-8")
    raw_export = export_binary_sklearn_to_onnx(context["model"], raw_onnx_path, len(context["features"]))
    patch_meta = patch_binary_onnx_to_short_three_columns(raw_onnx_path, patched_onnx_path)
    feature_meta = f71d.mt5.export_mt5_feature_matrix_csv(context["frame"], context["features"], feature_csv_path, metadata_columns=("split",))
    veto_meta = f71d.selected_entry_tape(context["frame"], context["selected"], context["event_mask"], veto_path)
    probability, signal = parity_rows(context, raw_onnx_path, patched_onnx_path)
    reproduction = reproduction_rows(context)
    probability_ok = all(row.get("passed") for row in probability)
    signal_ok = all(row.get("passed") for row in signal)
    overlap_ok = all(float(row.get("overlap_ratio_vs_source", 0.0)) >= 0.98 for row in reproduction)
    artifact = {
        "candidate_id": candidate_id,
        "source_candidate_id": PRIMARY_CANDIDATE_ID,
        "original_grok_target_id": ORIGINAL_GROK_TARGET_ID,
        "materialization_repair_reason": "original_hist_gbm_target_blocked_by_skl2onnx_tree_attribute_type; logistic_l2_same_axis_label_session_used",
        "materialization_mode": "short_binary_onnx_three_column_negative_control",
        "model_path": rel(model_path),
        "model_sha256": sha256_file(model_path),
        "raw_binary_onnx_path": rel(raw_onnx_path),
        "raw_binary_onnx_sha256": sha256_file(raw_onnx_path),
        "patched_onnx_path": rel(patched_onnx_path),
        "patched_onnx_sha256": sha256_file(patched_onnx_path),
        "feature_order_path": rel(feature_order_path),
        "feature_order_sha256": sha256_file(feature_order_path),
        "feature_csv_path": rel(feature_csv_path),
        "feature_csv_sha256": sha256_file(feature_csv_path),
        "runtime_veto_tape_path": rel(veto_path),
        "runtime_veto_tape_sha256": sha256_file(veto_path),
        "raw_binary_export": raw_export,
        "patch_meta": patch_meta,
        "feature_csv": feature_meta,
        "runtime_veto_tape": veto_meta,
        "probability_parity_passed": probability_ok,
        "signal_parity_passed": signal_ok,
        "source_reproduction_overlap_passed": overlap_ok,
        "threshold": float(context["threshold"]),
        "threshold_epsilon": THRESHOLD_EPSILON,
        "short_threshold": float(context["threshold"]) - THRESHOLD_EPSILON,
        "long_threshold": 1.1,
        "min_margin": -1.0,
        "decision_mode": "threshold_margin",
        "runtime_claim_ceiling": "negative_control_runtime_probe_observation_only",
    }
    if probability_ok and signal_ok and overlap_ok:
        for local_path, common_key, copy_key in (
            (patched_onnx_path, "model_common_path", "model_common_copy"),
            (feature_csv_path, "feature_common_path", "feature_common_copy"),
            (veto_path, "runtime_veto_tape_common_path", "runtime_veto_tape_common_copy"),
        ):
            common_path = f"{COMMON_RUN_ROOT}/{local_path.parent.name}/{local_path.name}"
            artifact[common_key] = common_path
            artifact[copy_key] = f71d.mt5.copy_to_common_files(common_files_root, local_path, common_path)
    artifact["export_status"] = "negative_control_parity_passed" if probability_ok and signal_ok and overlap_ok else "negative_control_parity_failed"
    return artifact, probability, signal, reproduction


def build_attempts(context: Mapping[str, Any], artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    axis = context["axis"]
    for split in ("validation", "oos"):
        from_date, to_date = f71d.split_dates(context["frame"], split)
        split_mask = context["frame"]["split"].astype(str).eq(split).to_numpy(dtype=bool)
        expected_selected = int((context["selected"] & split_mask).sum())
        attempt_name = f"f74e_negative_control_{split}"
        extra = {
            "InpSameDirectionReentryCooldownBars": int(axis.horizon_bars),
            "InpReentryCooldownBars": 0,
            "InpAtrSltpEnabled": True,
            "InpAtrStopMultiplier": float(axis.stop_atr),
            "InpAtrTakeProfitMultiplier": float(axis.target_atr),
            "InpAtrMinStopPoints": 1.0,
            "InpAtrMinTakeProfitPoints": 1.0,
            "InpDecisionMode": "threshold_margin",
            "InpFallbackDecisionMode": "threshold_margin",
            "InpRuntimeVetoTapeEnabled": True,
            "InpRuntimeVetoTapePath": str(artifact["runtime_veto_tape_common_path"]),
            "InpRuntimeVetoTapeUseCommonFiles": True,
            "InpRuntimeVetoTapeDelimiter": ",",
        }
        attempt = attempt_payload(
            run_root=RUN_ROOT,
            run_id=RUN_ID,
            stage_number=74,
            exploration_label="frontier74E_negative_control_runtime_probe",
            attempt_name=attempt_name,
            tier=f71d.mt5.TIER_A,
            split=split,
            model_path=str(artifact["model_common_path"]),
            model_id=f"F74E_{artifact['candidate_id']}",
            model_backend="onnx",
            feature_path=str(artifact["feature_common_path"]),
            feature_count=len(context["features"]),
            feature_order_hash=str(artifact.get("feature_order_sha256", "f74e_feature_order")),
            short_threshold=float(context["threshold"]) - THRESHOLD_EPSILON,
            long_threshold=1.1,
            min_margin=-1.0,
            invert_signal=False,
            from_date=from_date,
            to_date=to_date,
            primary_active_tier=f71d.mt5.TIER_A,
            attempt_role="negative_control_runtime_probe",
            record_view_prefix="mt5_f74e_negative_control",
            max_hold_bars=int(axis.horizon_bars),
            common_root=COMMON_RUN_ROOT,
            close_on_flat_signal=False,
            reverse_on_opposite_signal=True,
            close_only_on_opposite_signal=False,
            extra_set_values=extra,
        )
        attempt.update(
            {
                "candidate_id": artifact["candidate_id"],
                "source_candidate_id": PRIMARY_CANDIDATE_ID,
                "axis_id": context["source_candidate"].get("axis_id"),
                "expected_rows": int(split_mask.sum()),
                "expected_signal_count": expected_selected,
                "expected_selected_trade_count": expected_selected,
                "proxy_kpi": context["proxy_kpi_by_split"].get(split, {}),
                "runtime_threshold": float(context["threshold"]) - THRESHOLD_EPSILON,
                "threshold_epsilon": THRESHOLD_EPSILON,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempts.append(attempt)
    return attempts


def compile_runtime_ea(metaeditor_path: Path) -> dict[str, Any]:
    compile_payload = f71d.mt5.compile_mql5_ea(metaeditor_path, f71d.mt5.EA_SOURCE_PATH, MT5_ROOT / "mt5_compile.log")
    portable_payload = {
        "repo_ea_ex5": rel(EA_BINARY),
        "portable_ea_ex5": PORTABLE_EA_BINARY.as_posix(),
        "portable_ea_ex5_exists_before": path_exists(PORTABLE_EA_BINARY),
        "copied": False,
    }
    if path_exists(EA_BINARY):
        io_path(PORTABLE_EA_BINARY.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(EA_BINARY), io_path(PORTABLE_EA_BINARY))
        portable_payload.update(
            {
                "copied": True,
                "portable_ea_ex5_exists_after": path_exists(PORTABLE_EA_BINARY),
                "portable_ea_sha256": f71d.mt5.sha256_file(PORTABLE_EA_BINARY),
            }
        )
    return {"compile": compile_payload, "portable_ea": portable_payload}


def can_run_terminal(payload: Mapping[str, Any]) -> bool:
    return ((payload.get("compile") or {}).get("status") == "completed") or path_exists(PORTABLE_EA_BINARY)


def execute_attempts(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]], compile_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for attempt in attempts:
        if not can_run_terminal(compile_payload):
            result = {"status": "blocked", "blocker": "compile_failed_and_portable_ea_missing"}
        else:
            f71d.clear_runtime_outputs(Path(args.common_files_root), attempt)
            f71d.mt5.remove_existing_mt5_report_artifacts(Path(args.terminal_data_root), attempt, run_id=RUN_ID)
            try:
                result = f71d.mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini"]["path"]),
                    set_path=ROOT / str(attempt["set"]["path"]),
                    tester_profile_set_path=Path(args.tester_profile_root) / f71d.mt5.EA_TESTER_SET_NAME,
                    tester_profile_ini_path=Path(args.tester_profile_root) / f"opv2_{attempt['attempt_name']}.ini",
                    timeout_seconds=int(args.timeout_seconds),
                    terminal_extra_args=["/portable"],
                )
            except subprocess.TimeoutExpired as exc:
                result = {
                    "status": "blocked",
                    "command": exc.cmd,
                    "stdout": (exc.stdout or "")[-2000:],
                    "stderr": (exc.stderr or "")[-2000:],
                    "blocker": "terminal_timeout",
                }
            runtime_outputs = f71d.mt5.wait_for_mt5_runtime_outputs(Path(args.common_files_root), attempt, timeout_seconds=int(args.wait_timeout_seconds), poll_seconds=2.0)
            if runtime_outputs.get("status") != "completed":
                result["status"] = "blocked"
                result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            result["runtime_outputs"] = runtime_outputs
        result.update(
            {
                "attempt_name": attempt["attempt_name"],
                "tier": attempt["tier"],
                "split": attempt["split"],
                "candidate_id": attempt.get("candidate_id"),
                "source_candidate_id": attempt.get("source_candidate_id"),
                "axis_id": attempt.get("axis_id"),
                "expected_rows": attempt.get("expected_rows"),
                "expected_signal_count": attempt.get("expected_signal_count"),
                "expected_selected_trade_count": attempt.get("expected_selected_trade_count"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "set_path": attempt.get("set", {}).get("path"),
            }
        )
        results.append(result)
    return results


def best_receipt(receipts: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return next((row for row in receipts if row.get("split") == "oos"), receipts[0] if receipts else {})


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipts = list(payload.get("runtime_receipt", []))
    completed = sum(1 for row in receipts if row.get("tester_status") == "completed")
    best = best_receipt(receipts)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "attempt_count": len(payload.get("attempts", [])),
        "completed_attempt_count": completed,
        "probability_parity_pass_rows": sum(1 for row in payload.get("probability_parity", []) if row.get("passed")),
        "signal_parity_pass_rows": sum(1 for row in payload.get("signal_parity", []) if row.get("passed")),
        "source_reproduction_min_overlap": min((float(row.get("overlap_ratio_vs_source", 0.0)) for row in payload.get("source_reproduction", [])), default=0.0),
        "best_runtime": best,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    artifact = payload.get("artifact_rows", [{}])[0]
    return [
        "# Frontier74E MT5 Negative-Control Runtime Probe(F74E MT5 부정 대조 런타임 탐침)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- attempts(시도): `{summary['attempt_count']}`; completed(완료): `{summary['completed_attempt_count']}`",
        f"- probability parity pass rows(확률 동등성 통과 행): `{summary['probability_parity_pass_rows']}`",
        f"- signal parity pass rows(신호 동등성 통과 행): `{summary['signal_parity_pass_rows']}`",
        f"- source reproduction min overlap(원천 재현 최소 중복): `{summary['source_reproduction_min_overlap']}`",
        f"- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`",
        f"- artifact export(산출물 내보내기): `{artifact.get('export_status')}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Boundary(경계)",
        "",
        "This is negative-control runtime_probe observation only(부정 대조 런타임 탐침 관찰 전용). It cannot create completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).",
    ]


def gate_audit_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    return [
        "# F74E Required Gate Coverage Audit(F74E 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "| gate(게이트) | status(상태) | evidence/effect(근거/효과) |",
        "|---|---|---|",
        f"| ONNX/materialization parity(ONNX/물질화 동등성) | `{'pass(통과)' if summary['probability_parity_pass_rows'] == 3 and summary['signal_parity_pass_rows'] == 3 else 'fail_or_blocked(실패 또는 차단)'}` | probability/signal rows(확률/신호 행) `{summary['probability_parity_pass_rows']}/{summary['signal_parity_pass_rows']}` |",
        f"| MT5 runtime probe(MT5 런타임 탐침) | `{'completed(완료)' if summary['completed_attempt_count'] else 'blocked_or_materialized_pending(차단 또는 물질화 후 대기)'}` | attempts/completed(시도/완료) `{summary['attempt_count']}/{summary['completed_attempt_count']}` |",
        "| negative-control boundary(부정 대조 경계) | `pass(통과)` | F74C no-scout context preserved(F74C 탐색 단서 없음 맥락 보존). |",
        "| final claim guard(최종 주장 보호) | `pass(통과)` | no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). |",
    ]


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    report = REVIEWS_ROOT / "frontier74E_mt5_negative_control_runtime_probe_report.md"
    manifest = RUN_ROOT / "run_manifest.json"
    audit = REVIEWS_ROOT / "required_gate_coverage_audit_f74e.md"
    row = {
        "ledger_row_id": f"{RUN_ID}__runtime_probe",
        "row_id": f"{RUN_ID}__runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "negative_control_runtime_probe(부정 대조 런타임 탐침)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "MT5 negative-control runtime probe(MT5 부정 대조 런타임 탐침)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope_by_claim",
        "kpi_scope": "runtime_probe_kpi(런타임 탐침 KPI)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "result_status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "result_judgment": payload.get("judgment"),
        "path": rel(report),
        "report_path": rel(report),
        "primary_report": rel(report),
        "primary_artifact": rel(manifest),
        "output_path": rel(manifest),
        "result_path": rel(report),
        "primary_kpi": f"attempts={summary['attempt_count']};completed={summary['completed_attempt_count']}",
        "guardrail_kpi": f"prob_parity={summary['probability_parity_pass_rows']};signal_parity={summary['signal_parity_pass_rows']}",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked_or_materialized_pending(차단 또는 물질화 후 대기)",
        "notes": "F74E negative-control MT5 Runtime Probe; no authority(F74E 부정 대조 MT5 런타임 탐침, 권위 없음).",
        "run_number": "frontier74E",
        "date": created_at[:10],
        "run_date": created_at[:10],
        "decision": payload.get("judgment"),
        "next_run_id": NEXT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "rows": summary["attempt_count"],
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": summary["attempt_count"],
        "runtime_completed_rows": summary["completed_attempt_count"],
        "probability_parity_pass_rows": summary["probability_parity_pass_rows"],
        "net_profit": best.get("net_profit", ""),
        "profit_factor": best.get("profit_factor", ""),
        "drawdown": best.get("max_drawdown_percent", ""),
        "max_drawdown_percent": best.get("max_drawdown_percent", ""),
        "trade_count": best.get("trade_count", ""),
        "trade_density": best.get("trades_per_day", ""),
        "expectancy": best.get("expectancy", ""),
        "recovery_factor": best.get("recovery_factor", ""),
        "created_at_utc": created_at,
        "required_gate_audit": rel(audit),
        "gate_audit_path": rel(audit),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "runtime_backtest(MT5 런타임/백테스트)",
        "run_type": "negative_control_runtime_probe(부정 대조 런타임 탐침)",
        "input_run_id": PARENT_RUN_ID,
        "question": "How does F74C weak proxy materialize in MT5 runtime?(F74C 약한 프록시는 MT5 런타임에서 어떻게 물질화되는가?)",
        "evidence_boundary": "runtime_probe_observation_no_authority(런타임 탐침 관찰, 권위 없음)",
    }
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_registers(payload: Mapping[str, Any]) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    marker = "<!-- frontier74E_mt5_negative_control_runtime_probe_v1 -->"
    block = f"""<!-- frontier74E_mt5_negative_control_runtime_probe_v1 -->
- `{RUN_ID}` executed/attempted(실행/시도) F74 negative-control MT5 Runtime Probe(F74 부정 대조 MT5 런타임 탐침). Result(결과): `{payload.get('judgment')}`. Attempts(시도) `{summary['attempt_count']}`, completed(완료) `{summary['completed_attempt_count']}`. Best runtime(최선 런타임) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier74E_mt5_negative_control_runtime_probe_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(IDEA_REGISTRY, marker, block)


def update_state(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f74_negative_control_runtime_probe_attempted",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f73_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        '  - "Action(행동): F74E negative-control MT5 Runtime Probe(부정 대조 MT5 런타임 탐침)를 실행/시도했다."',
        f'  - "Effect(효과): runtime receipt rows(런타임 영수증 행) {len(payload.get("runtime_receipt", []))}개를 만들고 다음 행동을 {NEXT_RUN_ID}로 설정했다."',
        f'  - "Best runtime(최선 런타임): net/PF/DD/tpd {best.get("net_profit", "")}/{best.get("profit_factor", "")}/{best.get("max_drawdown_percent", "")}/{best.get("trades_per_day", "")}."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    write_text(WORKSPACE_STATE, "\n".join(lines))
    write_md(
        SELECTED_ROOT / "selection_status.md",
        [
            "# F74 Selection Status(F74 선택 상태)",
            "",
            f"- stage(단계): `{STAGE_ID}`",
            f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
            f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
            f"- status(상태): `{payload.get('status')}`",
            f"- judgment(판정): `{payload.get('judgment')}`",
            "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
            "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
            "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
            "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
            "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
            f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
            f"- boundary(경계): `{CLAIM_BOUNDARY}`",
        ],
    )
    write_md(
        CURRENT_WORKING_STATE,
        [
            "# Current Working State(현재 작업 상태)",
            "",
            f"Updated(갱신): {created_at}",
            "",
            f"Active stage(활성 단계): `{STAGE_ID}`",
            f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "",
            "## Current Truth(현재 진실)",
            "",
            "Action(행동): F74E negative-control MT5 Runtime Probe(부정 대조 MT5 런타임 탐침)를 실행/시도했다.",
            "",
            f"Effect(효과): 다음 실행을 `{NEXT_RUN_ID}`로 설정했다.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ],
    )


def main() -> int:
    args = parse_args()
    ensure_dirs()
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F74E required material missing: {missing}")
    created_at = utc_now()
    context = train_context()
    artifact, probability_rows, signal_rows, reproduction_rows_out = materialize(context, Path(args.common_files_root))
    attempts = build_attempts(context, artifact) if artifact.get("export_status") == "negative_control_parity_passed" else []
    compile_payload = compile_runtime_ea(Path(args.metaeditor_path))
    execution_results: list[dict[str, Any]] = []
    if args.execute and not args.materialize_only and attempts:
        execution_results = execute_attempts(args, attempts, compile_payload)
        reports = f71d.mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=Path(args.terminal_data_root),
            run_output_root=RUN_ROOT,
            attempts=attempts,
            run_id=RUN_ID,
        )
        f71d.mt5.attach_mt5_report_metrics(execution_results, reports)
    runtime_receipt = f71d.build_runtime_receipt(execution_results, attempts) if execution_results else []
    completed = sum(1 for row in runtime_receipt if row.get("tester_status") == "completed")
    if args.execute and completed:
        status = "completed_negative_control_runtime_probe_observation_no_authority"
        judgment = "negative_control_runtime_probe_completed_gap_analysis_required_no_authority"
    elif args.execute:
        status = "blocked_negative_control_runtime_probe_attempted_no_authority"
        judgment = "negative_control_runtime_probe_blocked_no_authority"
    else:
        status = "materialized_pending_negative_control_runtime_probe_no_authority"
        judgment = "negative_control_runtime_probe_materialized_pending_execution_no_authority"
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": created_at,
        "artifact_rows": [artifact],
        "probability_parity": probability_rows,
        "signal_parity": signal_rows,
        "source_reproduction": reproduction_rows_out,
        "attempts": attempts,
        "compile_payload": compile_payload,
        "execution_results": execution_results,
        "runtime_receipt": runtime_receipt,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_ROOT / "run_manifest.json", payload)
    write_json(RUN_ROOT / "f74e_summary.json", build_summary(payload))
    write_csv(RUN_ROOT / "f74e_probability_parity.csv", probability_rows)
    write_csv(RUN_ROOT / "f74e_signal_parity.csv", signal_rows)
    write_csv(RUN_ROOT / "f74e_source_reproduction.csv", reproduction_rows_out)
    write_csv(RUN_ROOT / "f74e_runtime_receipt.csv", runtime_receipt)
    write_json(RUN_ROOT / "f74e_execution_results.json", execution_results)
    write_json(REVIEWS_ROOT / "f74e_summary.json", build_summary(payload))
    write_csv(REVIEWS_ROOT / "f74e_runtime_receipt.csv", runtime_receipt)
    write_csv(REVIEWS_ROOT / "f74e_probability_parity.csv", probability_rows)
    write_csv(REVIEWS_ROOT / "f74e_signal_parity.csv", signal_rows)
    write_md(REVIEWS_ROOT / "frontier74E_mt5_negative_control_runtime_probe_report.md", report_lines(payload, created_at))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f74e.md", gate_audit_lines(payload, created_at))
    update_ledgers(payload, created_at)
    update_registers(payload)
    update_state(payload, created_at)
    print(json.dumps(json_ready(build_summary(payload)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
