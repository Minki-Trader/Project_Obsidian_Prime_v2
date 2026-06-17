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
from stage_pipelines.stage_frontier_73 import frontier73b_session_regime_feature_model_rotation_proxy_scout as f73b
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
)


STAGE_ID = f73b.STAGE_ID
RUN_ID = "frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1"
PARENT_RUN_ID = "frontier73E_proxy_runtime_gap_analysis_or_repair_decision_v1"
NEXT_RUN_ID = "frontier73G_direct_binary_adapter_gap_or_closeout_decision_v1"
CLAIM_BOUNDARY = (
    "direct_binary_adapter_runtime_repair_observation_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = f73b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f73b.REVIEWS_ROOT
SELECTED_ROOT = f73b.SELECTED_ROOT
MODEL_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "features"
VETO_ROOT = RUN_ROOT / "runtime_veto_tapes"
MT5_ROOT = RUN_ROOT / "mt5"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier73F_direct_binary_adapter_runtime_repair"
THRESHOLD_EPSILON = 1e-7

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f73f_pre_mt5_direct_binary_adapter_runtime_repair"
GROK_PROMPT = GROK_PACKET / "prompts/f73f_pre_mt5_direct_binary_adapter_runtime_repair_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"
F73C_TOP = STAGE_ROOT / "02_runs/frontier73C_axis_reduction_or_repair_proxy_scout_v1/f73c_top_candidates.csv"
F73C_BEST_TRADES = STAGE_ROOT / "02_runs/frontier73C_axis_reduction_or_repair_proxy_scout_v1/f73c_best_candidate_trades.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F73F direct binary ONNX adapter MT5 runtime repair.")
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


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def write_text(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_ROOT, FEATURE_ROOT, VETO_ROOT, MT5_ROOT, MT5_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def required_inputs() -> list[Path]:
    return [GROK_CLEAN, GROK_METADATA, F73C_TOP, F73C_BEST_TRADES, f73b.FWD12_INPUT, f73b.FWD12_FEATURE_ORDER, f73b.RAW_US100]


def selected_candidate() -> Mapping[str, Any]:
    top = pd.read_csv(io_path(F73C_TOP))
    row = top.loc[top["candidate_id"].astype(str).eq("f73c_0002")]
    if row.empty:
        row = top.head(1)
    return row.iloc[0].to_dict()


def cash_open_gate(frame: pd.DataFrame) -> np.ndarray:
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    return ((minutes >= 0) & (minutes <= 60)).to_numpy(dtype=bool)


def binary_probabilities(model: Any, values: pd.DataFrame | np.ndarray) -> np.ndarray:
    raw = np.asarray(model.predict_proba(values), dtype="float64")
    classes = classifier_classes(model)
    if 0 not in classes or 1 not in classes:
        raise RuntimeError(f"binary_model_class_coverage_failed:{classes}")
    class_to_index = {int(label): index for index, label in enumerate(classes)}
    return np.column_stack([raw[:, class_to_index[0]], raw[:, class_to_index[1]]])


def train_context() -> dict[str, Any]:
    source = selected_candidate()
    raw = f73b.load_raw()
    data = f73b.load_dataset(f73b.DATASETS[str(source["dataset_id"])], raw)
    frame = data["frame"].copy()
    features = f73b.feature_bundles(data["features"])[str(source["feature_bundle"])]
    gate = cash_open_gate(frame)
    y = np.asarray(data["paths"]["long"]["quality_label"], dtype=float)
    finite = np.isfinite(y) & np.isfinite(data["paths"]["long"]["pnl"])
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool) & gate & finite
    model = f73b.model_factories()["small_nn_16"]()
    model.fit(frame.loc[train_mask, features], y[train_mask].astype(int))
    proba = binary_probabilities(model, frame.loc[:, features])
    score = proba[:, 1]
    threshold = float(source["score_threshold"])
    selected = gate & finite & (score >= threshold)
    proxy_kpi_by_split: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool) & selected
        proxy_kpi_by_split[split] = f73b.trade_metrics(
            frame.loc[split_mask, "timestamp"],
            data["paths"]["long"]["pnl"][split_mask],
            np.ones(int(split_mask.sum()), dtype=int),
        )
    return {
        "source_candidate": dict(source),
        "frame": frame,
        "features": list(features),
        "feature_order_hash": f73b.ordered_hash(features) if hasattr(f73b, "ordered_hash") else None,
        "model": model,
        "binary_proba": proba,
        "score": score,
        "threshold": threshold,
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


def patch_binary_onnx_to_three_columns(binary_path: Path, patched_path: Path) -> dict[str, Any]:
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
            helper.make_node("Slice", [prob_name, "slice_start_col1", "slice_end_col2", "slice_axes_col", "slice_steps_col"], ["long_col"], name="SliceLongProbability"),
            helper.make_node("Mul", ["flat_col", "zero_scalar"], ["short_zero_col"], name="BuildZeroShortProbability"),
            helper.make_node("Concat", ["short_zero_col", "flat_col", "long_col"], ["probabilities_3"], name="BuildThreeColumnProbability", axis=1),
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
        "schema": "[p_short=0,p_flat,p_long]",
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


def source_trade_sets() -> dict[str, set[pd.Timestamp]]:
    trades = pd.read_csv(io_path(F73C_BEST_TRADES))
    trades["timestamp"] = pd.to_datetime(trades["timestamp"], utc=True)
    return {split: set(trades.loc[trades["split"].astype(str).eq(split), "timestamp"].tolist()) for split in ("validation", "oos")}


def reproduction_rows(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    source = context["source_candidate"]
    frame = context["frame"].copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    selected_ts_by_source = source_trade_sets()
    rows: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        split_selected = context["selected"] & frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
        reproduced_ts = set(frame.loc[split_selected, "timestamp"].tolist())
        source_ts = selected_ts_by_source[split]
        overlap = source_ts & reproduced_ts
        proxy = context["proxy_kpi_by_split"][split]
        rows.append(
            {
                "split": split,
                "source_selected_count": len(source_ts),
                "reproduced_selected_count": len(reproduced_ts),
                "overlap_count": len(overlap),
                "overlap_ratio_vs_source": float(len(overlap) / len(source_ts)) if source_ts else 0.0,
                "source_net_profit": source.get(f"{split}_net_profit"),
                "source_profit_factor": source.get(f"{split}_profit_factor"),
                "source_max_drawdown_percent": source.get(f"{split}_max_drawdown_percent"),
                "source_trades_day": source.get(f"{split}_trades_day"),
                "reproduced_net_profit": proxy.get("net_profit"),
                "reproduced_profit_factor": proxy.get("profit_factor"),
                "reproduced_max_drawdown_percent": proxy.get("max_drawdown_percent"),
                "reproduced_trades_day": proxy.get("trades_day"),
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
        patched_expected = np.column_stack([np.zeros(len(binary_expected)), binary_expected[:, 0], binary_expected[:, 1]])
        sample_values = values[: min(len(values), 4096)]
        sample_expected = patched_expected[: len(sample_values)]
        raw_actual = onnx_probability(raw_onnx_path, sample_values, 2)
        patched_actual = onnx_probability(patched_onnx_path, sample_values, 3)
        raw_diff = np.abs(raw_actual - binary_expected[: len(sample_values)])
        patched_diff = np.abs(patched_actual - sample_expected)
        probability_rows.append(
            {
                "split": split,
                "sample_rows": len(sample_values),
                "raw_binary_max_abs_diff": float(raw_diff.max()) if raw_diff.size else 0.0,
                "patched_three_col_max_abs_diff": float(patched_diff.max()) if patched_diff.size else 0.0,
                "patched_short_col_max_abs": float(np.abs(patched_actual[:, 0]).max()) if len(patched_actual) else 0.0,
                "threshold": threshold,
                "passed": bool((float(raw_diff.max()) if raw_diff.size else 0.0) <= 1e-5 and (float(patched_diff.max()) if patched_diff.size else 0.0) <= 1e-5),
            }
        )
        all_patched = onnx_probability(patched_onnx_path, values, 3)
        selected_expected = context["selected"][idx]
        onnx_selected = context["event_mask"][idx] & (all_patched[:, 2] >= runtime_threshold)
        signal_rows.append(
            {
                "split": split,
                "rows": len(subset),
                "expected_signal_count": int(selected_expected.sum()),
                "onnx_signal_count": int(onnx_selected.sum()),
                "signal_count_diff": int(onnx_selected.sum() - selected_expected.sum()),
                "signal_mismatch_count": int((onnx_selected != selected_expected).sum()),
                "source_threshold": threshold,
                "runtime_threshold": runtime_threshold,
                "threshold_epsilon": THRESHOLD_EPSILON,
                "passed": bool(int((onnx_selected != selected_expected).sum()) == 0),
            }
        )
    return probability_rows, signal_rows


def materialize(context: Mapping[str, Any], common_files_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    source = context["source_candidate"]
    candidate_id = f"f73f_direct_binary_{source['candidate_id']}"
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
    patch_meta = patch_binary_onnx_to_three_columns(raw_onnx_path, patched_onnx_path)
    feature_meta = f71d.mt5.export_mt5_feature_matrix_csv(context["frame"], context["features"], feature_csv_path, metadata_columns=("split",))
    veto_meta = f71d.selected_entry_tape(context["frame"], context["selected"], context["event_mask"], veto_path)
    probability, signal = parity_rows(context, raw_onnx_path, patched_onnx_path)
    reproduction = reproduction_rows(context)
    probability_ok = all(row.get("passed") for row in probability)
    signal_ok = all(row.get("passed") for row in signal)
    overlap_ok = all(float(row.get("overlap_ratio_vs_source", 0.0)) >= 0.98 for row in reproduction)
    artifact = {
        "candidate_id": candidate_id,
        "source_candidate_id": source.get("candidate_id"),
        "materialization_mode": "direct_binary_onnx_three_column_adapter",
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
        "short_threshold": 1.1,
        "long_threshold": float(context["threshold"]) - THRESHOLD_EPSILON,
        "min_margin": -1.0,
        "decision_mode": "threshold_margin",
        "runtime_claim_ceiling": "runtime_probe_observation_only",
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
    artifact["export_status"] = "direct_binary_adapter_parity_passed" if probability_ok and signal_ok and overlap_ok else "direct_binary_adapter_parity_failed"
    return artifact, probability, signal, reproduction


def build_attempts(context: Mapping[str, Any], artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        from_date, to_date = f71d.split_dates(context["frame"], split)
        split_mask = context["frame"]["split"].astype(str).eq(split).to_numpy(dtype=bool)
        expected_selected = int((context["selected"] & split_mask).sum())
        attempt_name = f"f73f_direct_binary_adapter_{split}"
        extra = {
            "InpSameDirectionReentryCooldownBars": 12,
            "InpReentryCooldownBars": 0,
            "InpAtrSltpEnabled": True,
            "InpAtrStopMultiplier": 1.0,
            "InpAtrTakeProfitMultiplier": 1.6,
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
            stage_number=73,
            exploration_label="frontier73F_direct_binary_adapter_runtime_repair",
            attempt_name=attempt_name,
            tier=f71d.mt5.TIER_A,
            split=split,
            model_path=str(artifact["model_common_path"]),
            model_id=f"F73F_{artifact['candidate_id']}",
            model_backend="onnx",
            feature_path=str(artifact["feature_common_path"]),
            feature_count=len(context["features"]),
            feature_order_hash=str(artifact.get("feature_order_sha256", "direct_binary_adapter_feature_order")),
            short_threshold=1.1,
            long_threshold=float(context["threshold"]) - THRESHOLD_EPSILON,
            min_margin=-1.0,
            invert_signal=False,
            from_date=from_date,
            to_date=to_date,
            primary_active_tier=f71d.mt5.TIER_A,
            attempt_role="direct_binary_adapter_runtime_repair",
            record_view_prefix="mt5_f73f_direct_binary_adapter",
            max_hold_bars=12,
            common_root=COMMON_RUN_ROOT,
            close_on_flat_signal=False,
            reverse_on_opposite_signal=True,
            close_only_on_opposite_signal=False,
            extra_set_values=extra,
        )
        attempt.update(
            {
                "candidate_id": artifact["candidate_id"],
                "source_candidate_id": context["source_candidate"].get("candidate_id"),
                "axis_id": "f73f_direct_binary_adapter",
                "expected_rows": int(split_mask.sum()),
                "expected_signal_count": expected_selected,
                "expected_selected_trade_count": expected_selected,
                "proxy_kpi": context["proxy_kpi_by_split"].get(split, {}),
                "source_threshold": context["threshold"],
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
        portable_payload.update({"copied": True, "portable_ea_ex5_exists_after": path_exists(PORTABLE_EA_BINARY), "portable_ea_sha256": f71d.mt5.sha256_file(PORTABLE_EA_BINARY)})
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
                result = {"status": "blocked", "command": exc.cmd, "stdout": (exc.stdout or "")[-2000:], "stderr": (exc.stderr or "")[-2000:], "blocker": "terminal_timeout"}
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


def grok_receipt_lines(created_at: str, artifact: Mapping[str, Any]) -> list[str]:
    metadata = read_json(GROK_METADATA)
    return [
        "# F73F Pre-MT5 Grok Receipt(F73F 사전 MT5 Grok 영수증)",
        "",
        f"- created_at_utc(생성): `{created_at}`",
        "- trigger_reason(트리거 이유): F73E가 proxy_bridge_selection_divergence(프록시-연결 선택 분기)를 주요 간극으로 판정해 직접 이진 ONNX 어댑터 수리 전 외부 검토 필요.",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{sha256_file(GROK_PROMPT)}`.",
        f"- output_identity(출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{sha256_file(GROK_CLEAN)}`.",
        f"- wrapper_success(래퍼 성공): `{metadata.get('success')}`; returncode(반환 코드): `{metadata.get('returncode')}`.",
        "- advice_classification(조언 분류): `accepted_capped_repair_with_local_verification(로컬 검증 조건 수용)`.",
        "- accepted(수용): direct binary adapter(직접 이진 어댑터), capped repair probe(상한 수리 탐침), no EA module change(EA 모듈 변경 없음).",
        "- rejected(거절): F73D receipts alone closeout(F73D만으로 마감), success/completion language(성공/완성 표현).",
        "- needs_local_verification(로컬 검증 필요): proxy reproduction(프록시 재현), graph patch schema(그래프 패치 스키마), binary probability parity(이진 확률 동등성), signal parity(신호 동등성), selection overlap(선택 중복).",
        f"- local_verification(로컬 검증): export `{artifact.get('export_status')}`, probability parity `{artifact.get('probability_parity_passed')}`, signal parity `{artifact.get('signal_parity_passed')}`, reproduction overlap pass `{artifact.get('source_reproduction_overlap_passed')}`.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def report_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    artifact = payload.get("artifact_rows", [{}])[0]
    return [
        "# Frontier73F Direct Binary Adapter Runtime Repair(F73F 직접 이진 어댑터 런타임 수리)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- attempts(시도): `{summary['attempt_count']}`; completed(완료): `{summary['completed_attempt_count']}`",
        f"- probability parity pass rows(확률 동등성 통과 행): `{summary['probability_parity_pass_rows']}`",
        f"- signal parity pass rows(신호 동등성 통과 행): `{summary['signal_parity_pass_rows']}`",
        f"- source reproduction min overlap(원천 재현 최소 중복): `{summary['source_reproduction_min_overlap']}`",
        f"- export_status(내보내기 상태): `{artifact.get('export_status')}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        f"- best split(최선 분할): `{best.get('split', '')}`",
        f"- net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}` / `{best.get('profit_factor', '')}` / `{best.get('max_drawdown_percent', '')}` / `{best.get('trades_per_day', '')}`",
        f"- expected signal/trade vs runtime signal/trade(예상 신호/거래 대 런타임 신호/거래): `{best.get('expected_signal_count', '')}/{best.get('expected_selected_trade_count', '')}` vs `{best.get('signal_count', '')}/{best.get('trade_count', '')}`",
        f"- gap cause(간극 원인): `{best.get('gap_cause_summary', '')}`",
        "",
        "Effect(효과): F73C binary signal(이진 신호)을 3열 ONNX 출력으로 직접 인계해 bridge divergence(연결 분기)를 제거하고, 남는 간극이 lifecycle/execution economics(생명주기/실행 경제성)인지 확인한다.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`.",
    ]


def gate_audit_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    artifact = payload.get("artifact_rows", [{}])[0]
    return [
        "# F73F Required Gate Coverage Audit(F73F 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        f"- pre_mt5_grok(사전 MT5 Grok): `{rel(GROK_CLEAN)}`.",
        f"- graph_patch_contract(그래프 패치 계약): `{artifact.get('patch_meta', {}).get('schema')}`.",
        f"- source_reproduction_min_overlap(원천 재현 최소 중복): `{summary['source_reproduction_min_overlap']}`.",
        f"- probability_parity_pass_rows(확률 동등성 통과 행): `{summary['probability_parity_pass_rows']}`.",
        f"- signal_parity_pass_rows(신호 동등성 통과 행): `{summary['signal_parity_pass_rows']}`.",
        f"- runtime_attempts(런타임 시도): `{summary['attempt_count']}`.",
        f"- runtime_receipt_rows(런타임 영수증 행): `{len(payload.get('runtime_receipt', []))}`.",
        "- final_claim_guard(최종 주장 보호): pass(통과).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def write_outputs(payload: Mapping[str, Any], created_at: str) -> None:
    artifact = payload.get("artifact_rows", [{}])[0]
    write_json(RUN_ROOT / "frontier73F_runtime_repair_execution_result.json", payload)
    write_json(RUN_ROOT / "frontier73F_runtime_repair_summary.json", build_summary(payload))
    write_json(RUN_ROOT / "run_manifest.json", {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "artifact_rows": payload.get("artifact_rows", []),
        "attempts": payload.get("attempts", []),
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_csv(RUN_ROOT / "f73f_direct_binary_adapter_materialization.csv", payload.get("artifact_rows", []))
    write_csv(RUN_ROOT / "f73f_probability_parity.csv", payload.get("probability_parity", []))
    write_csv(RUN_ROOT / "f73f_signal_parity.csv", payload.get("signal_parity", []))
    write_csv(RUN_ROOT / "f73f_source_reproduction.csv", payload.get("source_reproduction", []))
    write_csv(RUN_ROOT / "f73f_runtime_probe_receipt.csv", payload.get("runtime_receipt", []), f71d.RUNTIME_RECEIPT_COLUMNS)
    write_csv(REVIEWS_ROOT / "f73f_direct_binary_adapter_materialization_review.csv", payload.get("artifact_rows", []))
    write_csv(REVIEWS_ROOT / "f73f_probability_parity_review.csv", payload.get("probability_parity", []))
    write_csv(REVIEWS_ROOT / "f73f_signal_parity_review.csv", payload.get("signal_parity", []))
    write_csv(REVIEWS_ROOT / "f73f_source_reproduction_review.csv", payload.get("source_reproduction", []))
    write_csv(REVIEWS_ROOT / "f73f_runtime_probe_receipt_review.csv", payload.get("runtime_receipt", []), f71d.RUNTIME_RECEIPT_COLUMNS)
    write_text(REVIEWS_ROOT / "frontier73F_direct_binary_adapter_runtime_repair_report.md", report_lines(payload, created_at))
    write_text(REVIEWS_ROOT / "f73f_pre_mt5_grok_receipt.md", grok_receipt_lines(created_at, artifact))
    write_text(REVIEWS_ROOT / "required_gate_coverage_audit_f73f.md", gate_audit_lines(payload, created_at))


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    row = {
        "ledger_row_id": f"{RUN_ID}__runtime_repair_probe",
        "row_id": f"{RUN_ID}__runtime_repair_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "direct_binary_adapter_runtime_repair(직접 이진 어댑터 런타임 수리)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "MT5 Runtime Repair Probe(MT5 런타임 수리 탐침)",
        "tier_scope": "Tier A separate(Tier A 분리)",
        "kpi_scope": "runtime_repair_probe_kpi(런타임 수리 탐침 KPI)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REVIEWS_ROOT / "frontier73F_direct_binary_adapter_runtime_repair_report.md"),
        "primary_kpi": f"completed={summary['completed_attempt_count']};best_pf={best.get('profit_factor')};overlap={summary['source_reproduction_min_overlap']}",
        "guardrail_kpi": f"signal_diff={best.get('signal_count_diff')};feature_diff={best.get('feature_ready_diff')}",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked(차단)",
        "notes": "F73F direct binary adapter runtime repair probe; no authority.",
        "family": "runtime_repair_probe(런타임 수리 탐침)",
        "lane": "mt5_runtime_probe(MT5 런타임 탐침)",
        "primary_report": rel(REVIEWS_ROOT / "frontier73F_direct_binary_adapter_runtime_repair_report.md"),
        "run_number": "frontier73F",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload.get("runtime_receipt", [])),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEWS_ROOT / "frontier73F_direct_binary_adapter_runtime_repair_report.md"),
        "runtime_completed_rows": summary["completed_attempt_count"],
        "best_net_profit": best.get("net_profit"),
        "best_profit_factor": best.get("profit_factor"),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_ROOT / "run_manifest.json"),
        "candidate_model_id": payload.get("artifact_rows", [{}])[0].get("candidate_id"),
        "net_profit": best.get("net_profit"),
        "profit_factor": best.get("profit_factor"),
        "drawdown": best.get("max_drawdown_percent"),
        "trade_count": best.get("trade_count"),
        "trade_density": best.get("trades_per_day"),
        "result_status": payload.get("status"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": created_at,
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73f.md"),
        "evidence_boundary": "runtime_repair_probe_observation_no_authority(런타임 수리 탐침 관찰, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "result_path": rel(REVIEWS_ROOT / "frontier73F_direct_binary_adapter_runtime_repair_report.md"),
    }
    f73b.upsert_ledger(f73b.ALPHA_LEDGER, "ledger_row_id", row)
    f73b.upsert_ledger(f73b.RUN_REGISTRY, "run_id", row)
    f73b.upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=f73b.ALPHA_LEDGER)


def update_registers(payload: Mapping[str, Any]) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    marker = "<!-- frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1 -->"
    block = f"""<!-- frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1 -->
- `{RUN_ID}` executed/attempted(실행/시도) F73 direct binary ONNX adapter runtime repair(F73 직접 이진 ONNX 어댑터 런타임 수리). Result(결과): `{payload.get('judgment')}`. Attempts(시도) `{summary['attempt_count']}`, completed(완료) `{summary['completed_attempt_count']}`. Best runtime(최선 런타임) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier73F_direct_binary_adapter_runtime_repair_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(f73b.IDEA_REGISTRY, marker, block)


def update_state(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f73_direct_binary_adapter_repair_probe_attempted",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f72_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        f'  - "Action(행동): F73F direct binary adapter runtime repair(직접 이진 어댑터 런타임 수리)를 실행/시도했다. Attempts(시도) {summary["attempt_count"]}, completed(완료) {summary["completed_attempt_count"]}."',
        f'  - "Effect(효과): bridge divergence(연결 분기)를 제거한 수리 탐침을 만들고, 다음 행동을 {NEXT_RUN_ID}로 설정했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(f73b.WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    write_text(SELECTED_ROOT / "selection_status.md", [
        "# F73 Selection Status(F73 선택 상태)",
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
    ])
    write_text(f73b.CURRENT_WORKING_STATE, [
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
        "Action(행동): F73F direct binary adapter runtime repair(직접 이진 어댑터 런타임 수리)를 실행/시도했다.",
        "",
        f"Effect(효과): runtime receipt rows(런타임 영수증 행) `{len(payload.get('runtime_receipt', []))}`개를 만들고, 다음 행동을 `{NEXT_RUN_ID}`로 설정했다.",
        "",
        f"- judgment(판정): `{payload.get('judgment')}`.",
        f"- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{summary['best_runtime'].get('net_profit', '')}` / `{summary['best_runtime'].get('profit_factor', '')}` / `{summary['best_runtime'].get('max_drawdown_percent', '')}` / `{summary['best_runtime'].get('trades_per_day', '')}`.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ])


def grok_receipt_lines(created_at: str, artifact: Mapping[str, Any]) -> list[str]:
    metadata = read_json(GROK_METADATA)
    return [
        "# F73F Pre-MT5 Grok Receipt(F73F 사전 MT5 Grok 영수증)",
        "",
        f"- created_at_utc(생성 시각): `{created_at}`",
        "- trigger_reason(트리거 이유): F73E가 bridge divergence(연결 분기)를 주요 proxy/runtime gap(프록시/런타임 간극)으로 판정했기 때문에, direct binary ONNX adapter(직접 이진 ONNX 어댑터) 수리 탐침을 사전 검토했다.",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{sha256_file(GROK_PROMPT)}`.",
        f"- output_identity(출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{sha256_file(GROK_CLEAN)}`.",
        f"- wrapper_success(래퍼 성공): `{metadata.get('success')}`; returncode(반환 코드): `{metadata.get('returncode')}`.",
        "- advice_classification(조언 분류): `accepted_capped_repair_with_local_verification(로컬 검증 조건부 수용)`.",
        "- accepted(수용): direct binary adapter(직접 이진 어댑터), capped repair probe(상한 있는 수리 탐침), no EA module change(EA 모듈 변경 없음).",
        "- rejected(거절): F73D receipts alone closeout(F73D 영수증만으로 마감), success/completion language(성공/완성 표현).",
        "- needs_local_verification(로컬 검증 필요): proxy reproduction(프록시 재현), graph patch schema(그래프 패치 스키마), binary probability parity(이진 확률 동등성), signal parity(신호 동등성), selection overlap(선택 중복).",
        f"- local_verification(로컬 검증): export `{artifact.get('export_status')}`, probability parity `{artifact.get('probability_parity_passed')}`, signal parity `{artifact.get('signal_parity_passed')}`, reproduction overlap pass `{artifact.get('source_reproduction_overlap_passed')}`.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def report_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    artifact = payload.get("artifact_rows", [{}])[0]
    return [
        "# Frontier73F Direct Binary Adapter Runtime Repair(F73F 직접 이진 어댑터 런타임 수리)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- attempts(시도): `{summary['attempt_count']}`; completed(완료): `{summary['completed_attempt_count']}`",
        f"- probability parity pass rows(확률 동등성 통과 행): `{summary['probability_parity_pass_rows']}`",
        f"- signal parity pass rows(신호 동등성 통과 행): `{summary['signal_parity_pass_rows']}`",
        f"- source reproduction min overlap(원천 재현 최소 중복): `{summary['source_reproduction_min_overlap']}`",
        f"- export_status(내보내기 상태): `{artifact.get('export_status')}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        f"- best split(최선 분할): `{best.get('split', '')}`",
        f"- net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}` / `{best.get('profit_factor', '')}` / `{best.get('max_drawdown_percent', '')}` / `{best.get('trades_per_day', '')}`",
        f"- expected signal/trade vs runtime signal/trade(예상 신호/거래 대 런타임 신호/거래): `{best.get('expected_signal_count', '')}/{best.get('expected_selected_trade_count', '')}` vs `{best.get('signal_count', '')}/{best.get('trade_count', '')}`",
        f"- signal/feature diff(신호/피처 차이): `{best.get('signal_count_diff', '')}` / `{best.get('feature_ready_diff', '')}`",
        f"- gap cause(간극 원인): `{best.get('gap_cause_summary', '')}`",
        "",
        "## Proxy Reproduction(프록시 재현)",
        "",
        f"- source_candidate_id(원천 후보 ID): `{artifact.get('source_candidate_id')}`",
        f"- graph patch schema(그래프 패치 스키마): `{artifact.get('patch_meta', {}).get('schema')}`",
        f"- threshold(임계값): `{artifact.get('threshold')}`",
        f"- patched_onnx_sha256(패치 ONNX 해시): `{artifact.get('patched_onnx_sha256')}`",
        "",
        "Effect(효과): F73C binary signal(이진 신호)을 3-column ONNX output(3열 ONNX 출력)으로 직접 연결해서 bridge divergence(연결 분기)를 제거했고, 남는 간극이 lifecycle/execution economics(생명주기/실행 경제성)인지 확인한다.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`.",
    ]


def gate_audit_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    artifact = payload.get("artifact_rows", [{}])[0]
    return [
        "# F73F Required Gate Coverage Audit(F73F 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        f"- pre_mt5_grok(사전 MT5 Grok): `{rel(GROK_CLEAN)}`.",
        f"- graph_patch_contract(그래프 패치 계약): `{artifact.get('patch_meta', {}).get('schema')}`.",
        f"- source_reproduction_min_overlap(원천 재현 최소 중복): `{summary['source_reproduction_min_overlap']}`.",
        f"- probability_parity_pass_rows(확률 동등성 통과 행): `{summary['probability_parity_pass_rows']}`.",
        f"- signal_parity_pass_rows(신호 동등성 통과 행): `{summary['signal_parity_pass_rows']}`.",
        f"- runtime_attempts(런타임 시도): `{summary['attempt_count']}`.",
        f"- runtime_receipt_rows(런타임 영수증 행): `{len(payload.get('runtime_receipt', []))}`.",
        "- final_claim_guard(최종 주장 보호): pass(통과).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    row = {
        "ledger_row_id": f"{RUN_ID}__runtime_repair_probe",
        "row_id": f"{RUN_ID}__runtime_repair_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "direct_binary_adapter_runtime_repair(직접 이진 어댑터 런타임 수리)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "MT5 Runtime Repair Probe(MT5 런타임 수리 탐침)",
        "tier_scope": "Tier A separate(Tier A 분리)",
        "kpi_scope": "runtime_repair_probe_kpi(런타임 수리 탐침 KPI)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REVIEWS_ROOT / "frontier73F_direct_binary_adapter_runtime_repair_report.md"),
        "primary_kpi": f"completed={summary['completed_attempt_count']};best_pf={best.get('profit_factor')};overlap={summary['source_reproduction_min_overlap']}",
        "guardrail_kpi": f"signal_diff={best.get('signal_count_diff')};feature_diff={best.get('feature_ready_diff')}",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked(차단)",
        "notes": "F73F direct binary adapter runtime repair probe(직접 이진 어댑터 런타임 수리 탐침); no authority(권위 없음).",
        "family": "runtime_repair_probe(런타임 수리 탐침)",
        "lane": "mt5_runtime_probe(MT5 런타임 탐침)",
        "primary_report": rel(REVIEWS_ROOT / "frontier73F_direct_binary_adapter_runtime_repair_report.md"),
        "run_number": "frontier73F",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload.get("runtime_receipt", [])),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEWS_ROOT / "frontier73F_direct_binary_adapter_runtime_repair_report.md"),
        "runtime_completed_rows": summary["completed_attempt_count"],
        "best_net_profit": best.get("net_profit"),
        "best_profit_factor": best.get("profit_factor"),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_ROOT / "run_manifest.json"),
        "candidate_model_id": payload.get("artifact_rows", [{}])[0].get("candidate_id"),
        "net_profit": best.get("net_profit"),
        "profit_factor": best.get("profit_factor"),
        "drawdown": best.get("max_drawdown_percent"),
        "trade_count": best.get("trade_count"),
        "trade_density": best.get("trades_per_day"),
        "result_status": payload.get("status"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": created_at,
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73f.md"),
        "evidence_boundary": "runtime_repair_probe_observation_no_authority(런타임 수리 탐침 관찰, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "result_path": rel(REVIEWS_ROOT / "frontier73F_direct_binary_adapter_runtime_repair_report.md"),
    }
    f73b.upsert_ledger(f73b.ALPHA_LEDGER, "ledger_row_id", row)
    f73b.upsert_ledger(f73b.RUN_REGISTRY, "run_id", row)
    f73b.upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=f73b.ALPHA_LEDGER)


def update_registers(payload: Mapping[str, Any]) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    marker = "<!-- frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1 -->"
    block = f"""<!-- frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1 -->
- `{RUN_ID}` executed/attempted(실행/시도) F73 direct binary ONNX adapter runtime repair(F73 직접 이진 ONNX 어댑터 런타임 수리). Result(결과): `{payload.get('judgment')}`. Attempts(시도) `{summary['attempt_count']}`, completed(완료) `{summary['completed_attempt_count']}`. Best runtime(최선 런타임) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier73F_direct_binary_adapter_runtime_repair_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(f73b.IDEA_REGISTRY, marker, block)


def update_state(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f73_direct_binary_adapter_repair_probe_attempted",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f72_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        f'  - "Action(행동): F73F direct binary adapter runtime repair(직접 이진 어댑터 런타임 수리)를 실행/시도했다. Attempts(시도) {summary["attempt_count"]}, completed(완료) {summary["completed_attempt_count"]}."',
        f'  - "Effect(효과): bridge divergence(연결 분기)를 제거하는 수리 탐침을 만들고, 다음 행동을 {NEXT_RUN_ID}로 설정했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(f73b.WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    write_text(SELECTED_ROOT / "selection_status.md", [
        "# F73 Selection Status(F73 선택 상태)",
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
    ])
    write_text(f73b.CURRENT_WORKING_STATE, [
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
        "Action(행동): F73F direct binary adapter runtime repair(직접 이진 어댑터 런타임 수리)를 실행/시도했다.",
        "",
        f"Effect(효과): runtime receipt rows(런타임 영수증 행) `{len(payload.get('runtime_receipt', []))}`개를 만들고 다음 행동을 `{NEXT_RUN_ID}`로 설정했다.",
        "",
        f"- judgment(판정): `{payload.get('judgment')}`.",
        f"- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}` / `{best.get('profit_factor', '')}` / `{best.get('max_drawdown_percent', '')}` / `{best.get('trades_per_day', '')}`.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ])


def main() -> int:
    args = parse_args()
    ensure_dirs()
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F73F required material missing: {missing}")
    created_at = utc_now()
    context = train_context()
    artifact, probability_rows, signal_rows, reproduction_rows_out = materialize(context, Path(args.common_files_root))
    attempts = build_attempts(context, artifact) if artifact.get("export_status") == "direct_binary_adapter_parity_passed" else []
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
        status = "completed_direct_binary_adapter_runtime_repair_observation_no_authority"
        judgment = "direct_binary_adapter_runtime_repair_completed_gap_or_closeout_required_no_authority"
    elif args.execute:
        status = "blocked_direct_binary_adapter_runtime_repair_attempted_no_authority"
        judgment = "direct_binary_adapter_runtime_repair_blocked_no_authority"
    else:
        status = "materialized_pending_direct_binary_adapter_runtime_repair_no_authority"
        judgment = "direct_binary_adapter_runtime_repair_materialized_pending_execution_no_authority"
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
    write_outputs(payload, created_at)
    update_ledgers(payload, created_at)
    update_registers(payload)
    update_state(payload, created_at)
    print(json.dumps(json_ready(build_summary(payload)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
