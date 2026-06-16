from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.models.onnx_bridge import check_onnxruntime_probability_parity, export_sklearn_to_onnx_zipmap_disabled, ordered_hash
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage_frontier_70 import frontier70b_label_regime_asymmetric_value_proxy_scout as f70b
from stage_pipelines.stage_frontier_70 import frontier70c_label_regime_stability_repair_proxy_scout as f70c
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
)


STAGE_ID = f70b.STAGE_ID
RUN_ID = "frontier70D_label_regime_stability_runtime_probe_v1"
PARENT_RUN_ID = f70c.RUN_ID
NEXT_RUN_ID = "frontier70E_proxy_runtime_gap_analysis_and_repair_decision_v1"
IDEA_ID = f70b.IDEA_ID

STAGE_ROOT = f70b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f70b.REVIEWS_ROOT
MODEL_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "features"
VETO_ROOT = RUN_ROOT / "runtime_veto_tapes"
MT5_ROOT = RUN_ROOT / "mt5"
REPORT_ROOT = RUN_ROOT / "reports"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier70D_label_regime_stability_runtime_probe"

F70C_SUMMARY = REVIEWS_ROOT / "f70c_proxy_candidate_summary_review.csv"
GROK_PACKET_ROOT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f70d_pre_mt5_label_regime_stability_runtime_probe"
GROK_PROMPT = GROK_PACKET_ROOT / "prompts/f70d_pre_mt5_label_regime_stability_runtime_probe_prompt.md"
GROK_CLEAN = GROK_PACKET_ROOT / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET_ROOT / "outputs/metadata.json"

CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
STATUS_MATERIALIZED = "materialized_pending_mt5_runtime_probe_execution_no_authority"
STATUS_COMPLETED = "completed_mt5_runtime_probe_observation_no_authority"
STATUS_BLOCKED = "blocked_mt5_runtime_probe_attempted_repair_required_no_authority"

SPLITS = ("validation", "oos")
ALL_SPLITS = ("train", "validation", "oos")


@dataclass(frozen=True)
class AxisSpec:
    axis_id: str
    candidate_id: str
    role: str
    label_id: str
    feature_set_id: str
    model_id: str
    selection_id: str
    mask_name: str
    threshold_quantile: float
    priority: int


AXES: tuple[AxisSpec, ...] = (
    AxisSpec(
        axis_id="reference_low_dd_axis",
        candidate_id="f70c_f9a2939acd19",
        role="near_miss_reference_axis_joint_soft_zero_observation_only",
        label_id="repair_trend_quality_h18_tp85_edge08_pen40",
        feature_set_id="regime_value_macro_v1",
        model_id="extratrees_light_reference_v1",
        selection_id="vol_expansion_q50",
        mask_name="vol_expansion",
        threshold_quantile=0.50,
        priority=1,
    ),
    AxisSpec(
        axis_id="small_nn_density_axis",
        candidate_id="f70c_5c8a3021f38f",
        role="hypothesis_carrier_small_nn_joint_soft_zero_observation_only",
        label_id="repair_vol_expansion_h18_tp85_edge08_pen40",
        feature_set_id="regime_value_macro_v1",
        model_id="small_mlp_l2_v1",
        selection_id="vol_expansion_q50",
        mask_name="vol_expansion",
        threshold_quantile=0.50,
        priority=2,
    ),
)

RUNTIME_RECEIPT_COLUMNS = (
    "run_id",
    "attempt_name",
    "candidate_id",
    "axis_id",
    "split",
    "test_period_start",
    "test_period_end",
    "calendar_days_exclusive",
    "tester_status",
    "runtime_status",
    "report_status",
    "expected_rows",
    "feature_ready_count",
    "feature_ready_diff",
    "expected_signal_count",
    "signal_count",
    "signal_count_diff",
    "expected_selected_trade_count",
    "order_attempt_count",
    "order_fill_count",
    "order_fill_rate",
    "trade_count",
    "trades_per_day",
    "long_trade_count",
    "short_trade_count",
    "winning_trade_count",
    "losing_trade_count",
    "net_profit",
    "gross_profit",
    "gross_loss",
    "profit_factor",
    "expectancy",
    "win_rate_percent",
    "average_win",
    "average_loss",
    "payoff_ratio",
    "recovery_factor",
    "max_drawdown_amount",
    "max_drawdown_percent",
    "proxy_net_profit",
    "proxy_profit_factor",
    "proxy_trades_per_day",
    "proxy_dd_percent",
    "dd_delta_runtime_minus_proxy",
    "gap_cause_summary",
    "report_path",
    "telemetry_path",
    "summary_path",
    "claim_boundary",
)

GAP_COLUMNS = (
    "run_id",
    "attempt_name",
    "candidate_id",
    "axis_id",
    "split",
    "gap_type",
    "metric",
    "proxy_value",
    "runtime_value",
    "delta",
    "classification",
    "evidence",
    "claim_boundary",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F70D label-regime stability MT5 runtime probe.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=420)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
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


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (list(rows[0].keys()) if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in fieldnames})


def upsert_ledger(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None:
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise RuntimeError(f"ledger header missing: {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def fmt(value: Any, digits: int = 6) -> str:
    if value is None:
        return ""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(number):
        return ""
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def as_int(value: Any) -> int | None:
    number = as_float(value)
    return None if number is None else int(round(number))


def ratio(numerator: float | int | None, denominator: float | int | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return float(numerator) / float(denominator)


def sha256_file(path: Path) -> str:
    return f70b.sha256_file(path)


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_ROOT, FEATURE_ROOT, VETO_ROOT, MT5_ROOT, MT5_ROOT / "reports", REPORT_ROOT, REVIEWS_ROOT, STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def read_csv_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig")


def match_one(items: Sequence[Any], attr: str, value: str) -> Any:
    matches = [item for item in items if str(getattr(item, attr)) == value]
    if len(matches) != 1:
        raise RuntimeError(f"match failed for {attr}={value}: {len(matches)}")
    return matches[0]


def candidate_summary_lookup() -> dict[str, Mapping[str, Any]]:
    frame = read_csv_frame(F70C_SUMMARY)
    return {str(row["candidate_id"]): row for row in frame.to_dict("records")}


def onnx_probabilities(onnx_path: Path, values: np.ndarray) -> np.ndarray:
    import onnxruntime as ort

    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: np.asarray(values, dtype="float32")})
    candidates = [output for output in outputs if isinstance(output, np.ndarray) and output.ndim == 2 and output.shape[1] == 3]
    if len(candidates) != 1:
        raise RuntimeError(f"expected one probability output, got {[getattr(output, 'shape', None) for output in outputs]}")
    return np.asarray(candidates[0], dtype="float64")


def side_score_from_probabilities(proba: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    p_short = proba[:, 0]
    p_flat = proba[:, 1]
    p_long = proba[:, 2]
    side = np.where(p_long >= p_short, 1, -1)
    score = np.maximum(p_long, p_short) - p_flat
    return side.astype(int), score.astype(float)


def split_dates(frame: pd.DataFrame, split_name: str) -> tuple[str, str]:
    split = frame.loc[frame["split"].astype(str).eq(split_name)]
    if split.empty:
        raise RuntimeError(f"empty split: {split_name}")
    timestamps = pd.to_datetime(split["timestamp"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def build_axis_contexts() -> list[dict[str, Any]]:
    frame = f70b.load_frames()
    features = {item.feature_set_id: item for item in f70b.feature_sets(frame)}
    labels = {item.label_id: item for item in f70c.repair_label_specs()}
    models = {item.model_id: item for item in f70c.repair_model_specs()}
    selections = {item.selection_id: item for item in f70c.repair_selection_specs()}
    summary_lookup = candidate_summary_lookup()
    contexts: list[dict[str, Any]] = []
    train_mask = frame["split"].astype(str).eq("train").to_numpy()
    for axis in AXES:
        label_spec = labels[axis.label_id]
        feature_set = features[axis.feature_set_id]
        model_spec = models[axis.model_id]
        selection = selections[axis.selection_id]
        local_frame = f70b.add_future_path(frame.copy(), label_spec.horizon_bars)
        label = f70b.build_labels(local_frame, label_spec)
        if label.loc[train_mask].nunique() < 2:
            raise RuntimeError(f"label has fewer than two train classes: {axis.label_id}")
        estimator = model_spec.build()
        estimator.fit(local_frame.loc[train_mask, feature_set.columns], label.loc[train_mask])
        sklearn_side, sklearn_score = f70b.side_scores(estimator, local_frame.loc[:, feature_set.columns])
        event_mask = f70b.mask_for(local_frame, selection.mask_name)
        train_scores = sklearn_score[train_mask & event_mask & np.isfinite(sklearn_score)]
        if len(train_scores) < 20:
            raise RuntimeError(f"too few train scores for threshold: {axis.candidate_id}")
        threshold = float(np.quantile(train_scores, selection.threshold_quantile))
        active = (sklearn_score >= threshold) & event_mask
        selected_indices = f70b.non_overlap_indices(active, label_spec.horizon_bars)
        selected_set = set(selected_indices)
        selected_mask = np.array([idx in selected_set for idx in range(len(local_frame))], dtype=bool)
        profits = f70b.first_hit_profit(
            local_frame,
            sklearn_side,
            label_spec.horizon_bars,
            tp_atr=label_spec.base_tp_atr * 1.25,
            sl_atr=label_spec.base_tp_atr * 0.85,
        )
        candidate_id_check = "f70c_" + f70b.stable_id([axis.label_id, axis.feature_set_id, axis.model_id, axis.selection_id])
        split_payload: dict[str, dict[str, Any]] = {}
        for split_name in ALL_SPLITS:
            split_frame = local_frame.loc[local_frame["split"].astype(str).eq(split_name)]
            idx = split_frame.index.to_numpy()
            split_selected = selected_mask[idx]
            split_active = active[idx]
            split_payload[split_name] = {
                "frame": split_frame,
                "indices": idx,
                "event_mask": event_mask[idx],
                "active": split_active,
                "selected_mask": split_selected,
                "side": sklearn_side[idx],
                "score": sklearn_score[idx],
                "expected_rows": int(len(split_frame)),
                "expected_signal_count": int(split_active.sum()),
                "expected_selected_trade_count": int(split_selected.sum()),
                "proxy_kpi": f70b.proxy_kpi(
                    profits[idx][split_selected],
                    split_frame["timestamp"].loc[split_selected],
                    split_frame["timestamp"],
                ),
            }
        contexts.append(
            {
                "axis": axis,
                "frame": local_frame,
                "label_spec": label_spec,
                "feature_set": feature_set,
                "model_spec": model_spec,
                "selection": selection,
                "estimator": estimator,
                "feature_columns": list(feature_set.columns),
                "feature_order_hash": ordered_hash(feature_set.columns),
                "threshold": threshold,
                "candidate_id_check": candidate_id_check,
                "candidate_id_match": candidate_id_check == axis.candidate_id,
                "summary_reference": summary_lookup.get(axis.candidate_id, {}),
                "split_payload": split_payload,
                "classes": [int(value) for value in estimator.classes_],
            }
        )
    return contexts


def write_veto_tape(context: Mapping[str, Any], output_path: Path) -> dict[str, Any]:
    frame: pd.DataFrame = context["frame"]
    event_mask = f70b.mask_for(frame, context["selection"].mask_name)
    payload = pd.DataFrame()
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    payload["bar_time_server"] = timestamps.dt.strftime("%Y.%m.%d %H:%M:%S")
    payload["timestamp_utc"] = timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    payload["entry_veto"] = np.where(event_mask, 0, 1).astype(int)
    payload["event_active"] = event_mask.astype(int)
    payload["split"] = frame["split"].astype(str).to_numpy()
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    payload.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "rows": int(len(payload)),
        "event_active_rows": int(event_mask.sum()),
        "veto_rows": int((~event_mask).sum()),
        "format": "runtime_veto_tape_entry_veto_outside_selection_mask",
    }


def export_context_artifacts(context: Mapping[str, Any]) -> dict[str, Any]:
    axis: AxisSpec = context["axis"]
    feature_columns = list(context["feature_columns"])
    estimator = context["estimator"]
    model_path = MODEL_ROOT / f"{axis.candidate_id}.joblib"
    onnx_path = MODEL_ROOT / f"{axis.candidate_id}.onnx"
    feature_order_path = MODEL_ROOT / f"{axis.candidate_id}_feature_order.txt"
    feature_csv_path = FEATURE_ROOT / f"{axis.candidate_id}_features.csv"
    veto_path = VETO_ROOT / f"{axis.candidate_id}_runtime_veto_tape.csv"
    io_path(feature_order_path).write_text("\n".join(feature_columns) + "\n", encoding="utf-8")
    joblib.dump(estimator, io_path(model_path))
    export_meta = export_sklearn_to_onnx_zipmap_disabled(
        estimator,
        onnx_path,
        feature_count=len(feature_columns),
        target_opset=12,
        drop_label_output=True,
    )
    feature_meta = mt5.export_mt5_feature_matrix_csv(
        context["frame"],
        feature_columns,
        feature_csv_path,
        metadata_columns=("split",),
    )
    veto_meta = write_veto_tape(context, veto_path)
    return {
        "candidate_id": axis.candidate_id,
        "axis_id": axis.axis_id,
        "model_path": rel(model_path),
        "model_sha256": sha256_file(model_path),
        "onnx_path": rel(onnx_path),
        "onnx_sha256": sha256_file(onnx_path),
        "feature_order_path": rel(feature_order_path),
        "feature_order_sha256": sha256_file(feature_order_path),
        "feature_csv_path": rel(feature_csv_path),
        "feature_csv_sha256": sha256_file(feature_csv_path),
        "runtime_veto_tape_path": rel(veto_path),
        "runtime_veto_tape_sha256": sha256_file(veto_path),
        "onnx_export": export_meta,
        "feature_csv": feature_meta,
        "runtime_veto_tape": veto_meta,
    }


def parity_rows(context: Mapping[str, Any], artifact: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    axis: AxisSpec = context["axis"]
    onnx_path = ROOT / str(artifact["onnx_path"])
    estimator = context["estimator"]
    feature_columns = list(context["feature_columns"])
    probability_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    for split_name in ALL_SPLITS:
        split_payload = context["split_payload"][split_name]
        split_frame: pd.DataFrame = split_payload["frame"]
        values = split_frame.loc[:, feature_columns].to_numpy(dtype="float64")
        sample = values[: min(len(values), 2048)]
        probability = check_onnxruntime_probability_parity(
            estimator,
            onnx_path,
            sample,
            class_order=(-1, 0, 1),
            tolerance=1e-5,
        )
        probability_rows.append({"candidate_id": axis.candidate_id, "axis_id": axis.axis_id, "split": split_name, **probability})
        onnx_proba = onnx_probabilities(onnx_path, values)
        onnx_side, onnx_score = side_score_from_probabilities(onnx_proba)
        sklearn_side = np.asarray(split_payload["side"], dtype=int)
        sklearn_score = np.asarray(split_payload["score"], dtype=float)
        event_mask = np.asarray(split_payload["event_mask"], dtype=bool)
        threshold = float(context["threshold"])
        sklearn_signal = event_mask & (sklearn_score >= threshold)
        onnx_signal = event_mask & (onnx_score >= threshold)
        signal_rows.append(
            {
                "candidate_id": axis.candidate_id,
                "axis_id": axis.axis_id,
                "split": split_name,
                "rows": int(len(split_frame)),
                "sklearn_signal_count": int(sklearn_signal.sum()),
                "onnx_signal_count": int(onnx_signal.sum()),
                "signal_count_diff": int(onnx_signal.sum() - sklearn_signal.sum()),
                "signal_mismatch_count": int((onnx_signal != sklearn_signal).sum()),
                "side_mismatch_on_signal_count": int(((onnx_side != sklearn_side) & (onnx_signal | sklearn_signal)).sum()),
                "max_score_abs_diff": float(np.abs(onnx_score - sklearn_score).max()) if len(onnx_score) else 0.0,
                "event_active_rows": int(event_mask.sum()),
                "threshold": threshold,
                "passed": bool(
                    int((onnx_signal != sklearn_signal).sum()) == 0
                    and int(((onnx_side != sklearn_side) & (onnx_signal | sklearn_signal)).sum()) == 0
                ),
            }
        )
    return probability_rows, signal_rows


def materialize_candidates(common_files_root: Path, contexts: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    artifact_rows: list[dict[str, Any]] = []
    probability_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    local_verification: list[dict[str, Any]] = []

    def add_check(name: str, ok: bool, detail: str, effect: str) -> None:
        local_verification.append({"check_name": name, "status": "passed" if ok else "failed", "detail": detail, "effect": effect})

    add_check("grok_clean_output_exists", path_exists(GROK_CLEAN), rel(GROK_CLEAN), "pre-MT5 Grok review evidence is present")
    add_check("grok_metadata_exists", path_exists(GROK_METADATA), rel(GROK_METADATA), "Grok wrapper metadata is present")
    for context in contexts:
        axis: AxisSpec = context["axis"]
        try:
            artifact = export_context_artifacts(context)
            probability, signal = parity_rows(context, artifact)
            all_probability_pass = all(row.get("passed") for row in probability)
            all_signal_pass = all(row.get("passed") for row in signal)
            artifact["export_status"] = "exported_onnx_parity_passed" if all_probability_pass and all_signal_pass else "exported_onnx_parity_failed"
            artifact["export_error"] = ""
            artifact["probability_parity_passed"] = all_probability_pass
            artifact["signal_parity_passed"] = all_signal_pass
            artifact["candidate_id_match"] = context["candidate_id_match"]
            artifact["candidate_id_check"] = context["candidate_id_check"]
            artifact["feature_order_hash"] = context["feature_order_hash"]
            artifact["threshold"] = context["threshold"]
            artifact["role"] = axis.role
            if all_probability_pass and all_signal_pass:
                model_common = f"{COMMON_RUN_ROOT}/models/{Path(str(artifact['onnx_path'])).name}"
                feature_common = f"{COMMON_RUN_ROOT}/features/{Path(str(artifact['feature_csv_path'])).name}"
                veto_common = f"{COMMON_RUN_ROOT}/runtime_veto_tapes/{Path(str(artifact['runtime_veto_tape_path'])).name}"
                artifact["model_common_path"] = model_common
                artifact["feature_common_path"] = feature_common
                artifact["runtime_veto_tape_common_path"] = veto_common
                artifact["model_common_copy"] = mt5.copy_to_common_files(common_files_root, ROOT / str(artifact["onnx_path"]), model_common)
                artifact["feature_common_copy"] = mt5.copy_to_common_files(common_files_root, ROOT / str(artifact["feature_csv_path"]), feature_common)
                artifact["runtime_veto_tape_common_copy"] = mt5.copy_to_common_files(common_files_root, ROOT / str(artifact["runtime_veto_tape_path"]), veto_common)
            probability_rows.extend(probability)
            signal_rows.extend(signal)
            add_check(
                f"{axis.candidate_id}_candidate_id_reconstructed",
                bool(context["candidate_id_match"]),
                f"expected={axis.candidate_id};actual={context['candidate_id_check']}",
                "candidate identity is reconstructed from label/features/model/selection",
            )
            add_check(f"{axis.candidate_id}_onnx_probability_parity", all_probability_pass, f"rows={len(probability)}", "ONNX probability matches sklearn")
            add_check(f"{axis.candidate_id}_onnx_signal_parity", all_signal_pass, f"rows={len(signal)}", "ONNX signal count and side match sklearn")
        except Exception as exc:  # noqa: BLE001
            artifact = {
                "candidate_id": axis.candidate_id,
                "axis_id": axis.axis_id,
                "role": axis.role,
                "export_status": "export_or_parity_failed_repair_required",
                "export_error": f"{type(exc).__name__}: {exc}",
                "probability_parity_passed": False,
                "signal_parity_passed": False,
                "candidate_id_match": context.get("candidate_id_match"),
                "candidate_id_check": context.get("candidate_id_check"),
            }
            add_check(f"{axis.candidate_id}_export_or_parity", False, artifact["export_error"], "export or parity blocker recorded")
        artifact_rows.append(artifact)
    return artifact_rows, probability_rows, signal_rows, local_verification


def build_attempts(contexts: Sequence[Mapping[str, Any]], artifacts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    context_by_candidate = {context["axis"].candidate_id: context for context in contexts}
    attempts: list[dict[str, Any]] = []
    for artifact in artifacts:
        if artifact.get("export_status") != "exported_onnx_parity_passed":
            continue
        context = context_by_candidate[str(artifact["candidate_id"])]
        axis: AxisSpec = context["axis"]
        label_spec = context["label_spec"]
        threshold = float(context["threshold"])
        for split_name in SPLITS:
            split_payload = context["split_payload"][split_name]
            start, end = split_dates(context["frame"], split_name)
            attempt_name = f"f70d_{safe_name(axis.axis_id, 24)}_{axis.candidate_id[-6:]}_{split_name}"
            extra = {
                "InpSameDirectionReentryCooldownBars": int(label_spec.horizon_bars),
                "InpReentryCooldownBars": 0,
                "InpAtrSltpEnabled": True,
                "InpAtrStopMultiplier": float(label_spec.base_tp_atr * 0.85),
                "InpAtrTakeProfitMultiplier": float(label_spec.base_tp_atr * 1.25),
                "InpAtrMinStopPoints": 1.0,
                "InpAtrMinTakeProfitPoints": 1.0,
                "InpDecisionMode": "edge_margin",
                "InpFallbackDecisionMode": "edge_margin",
                "InpRuntimeVetoTapeEnabled": True,
                "InpRuntimeVetoTapePath": str(artifact["runtime_veto_tape_common_path"]),
                "InpRuntimeVetoTapeUseCommonFiles": True,
                "InpRuntimeVetoTapeDelimiter": ",",
            }
            attempt = attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=70,
                exploration_label=f"frontier70D_{axis.axis_id}_runtime_probe",
                attempt_name=attempt_name,
                tier=mt5.TIER_A,
                split=split_name,
                model_path=str(artifact["model_common_path"]),
                model_id=f"F70D_{axis.candidate_id}_{axis.axis_id}",
                model_backend="onnx",
                feature_path=str(artifact["feature_common_path"]),
                feature_count=int(len(context["feature_columns"])),
                feature_order_hash=str(context["feature_order_hash"]),
                short_threshold=0.0,
                long_threshold=0.0,
                min_margin=threshold,
                invert_signal=False,
                from_date=start,
                to_date=end,
                primary_active_tier=mt5.TIER_A,
                attempt_role=f"f70d_{axis.role}",
                record_view_prefix=f"mt5_f70d_{safe_name(axis.axis_id, 24)}_{axis.candidate_id[-6:]}",
                max_hold_bars=int(label_spec.horizon_bars),
                common_root=COMMON_RUN_ROOT,
                close_on_flat_signal=False,
                reverse_on_opposite_signal=True,
                close_only_on_opposite_signal=False,
                extra_set_values=extra,
            )
            attempt.update(
                {
                    "candidate_id": axis.candidate_id,
                    "axis_id": axis.axis_id,
                    "axis_role": axis.role,
                    "expected_rows": split_payload["expected_rows"],
                    "expected_signal_count": split_payload["expected_signal_count"],
                    "expected_selected_trade_count": split_payload["expected_selected_trade_count"],
                    "proxy_kpi": split_payload["proxy_kpi"],
                    "summary_reference": context["summary_reference"],
                    "label_id": axis.label_id,
                    "feature_set_id": axis.feature_set_id,
                    "model_id": axis.model_id,
                    "selection_id": axis.selection_id,
                    "mask_name": axis.mask_name,
                    "threshold": threshold,
                    "threshold_quantile": axis.threshold_quantile,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            attempts.append(attempt)
    return attempts


def safe_name(value: str, limit: int = 72) -> str:
    text = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in value).strip("_")
    return (text or "item")[:limit]


def compile_runtime_ea(metaeditor_path: Path) -> dict[str, Any]:
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, MT5_ROOT / "mt5_compile.log")
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
                "portable_ea_sha256": mt5.sha256_file(PORTABLE_EA_BINARY),
            }
        )
    return {"compile": compile_payload, "portable_ea": portable_payload}


def can_run_terminal(compile_payload: Mapping[str, Any]) -> bool:
    compile_status = ((compile_payload.get("compile") or {}).get("status"))
    return compile_status == "completed" or path_exists(PORTABLE_EA_BINARY)


def clear_runtime_outputs(common_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def execute_attempts(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]], compile_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for attempt in attempts:
        if not can_run_terminal(compile_payload):
            result = {"status": "blocked", "blocker": "compile_failed_and_portable_ea_missing"}
        else:
            clear_runtime_outputs(Path(args.common_files_root), attempt)
            mt5.remove_existing_mt5_report_artifacts(Path(args.terminal_data_root), attempt, run_id=RUN_ID)
            try:
                result = mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini"]["path"]),
                    set_path=ROOT / str(attempt["set"]["path"]),
                    tester_profile_set_path=Path(args.tester_profile_root) / mt5.EA_TESTER_SET_NAME,
                    tester_profile_ini_path=Path(args.tester_profile_root) / f"opv2_{attempt['attempt_name']}.ini",
                    timeout_seconds=int(args.timeout_seconds),
                    terminal_extra_args=["/portable"],
                )
            except subprocess.TimeoutExpired as exc:
                result = {
                    "status": "blocked",
                    "command": exc.cmd,
                    "returncode": None,
                    "stdout": (exc.stdout or "")[-2000:],
                    "stderr": (exc.stderr or "")[-2000:],
                    "blocker": "terminal_timeout",
                }
            runtime_outputs = mt5.wait_for_mt5_runtime_outputs(
                Path(args.common_files_root),
                attempt,
                timeout_seconds=int(args.wait_timeout_seconds),
                poll_seconds=2.0,
            )
            if runtime_outputs.get("status") != "completed":
                result["status"] = "blocked"
                result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            result["runtime_outputs"] = runtime_outputs
        result.update(
            {
                "attempt_name": attempt["attempt_name"],
                "tier": attempt["tier"],
                "split": attempt["split"],
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "candidate_id": attempt.get("candidate_id"),
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


def tester_period(attempt: Mapping[str, Any]) -> dict[str, Any]:
    tester = ((attempt.get("ini") or {}).get("tester") or {})
    start = str(tester.get("FromDate") or "").replace(".", "-")
    end = str(tester.get("ToDate") or "").replace(".", "-")
    days = None
    if start and end:
        try:
            days = max((datetime.strptime(end, "%Y-%m-%d") - datetime.strptime(start, "%Y-%m-%d")).days, 1)
        except ValueError:
            days = None
    return {"start": start, "end": end, "calendar_days_exclusive": days}


def gap_cause_summary(attempt: Mapping[str, Any], metrics: Mapping[str, Any], last: Mapping[str, Any]) -> str:
    feature_diff = (as_int(last.get("feature_ready_count")) or 0) - int(attempt.get("expected_rows") or 0)
    signal_count = (as_int(last.get("long_count")) or 0) + (as_int(last.get("short_count")) or 0)
    signal_diff = signal_count - int(attempt.get("expected_signal_count") or 0)
    trade_count = as_int(metrics.get("trade_count")) or 0
    expected_trades = int(attempt.get("expected_selected_trade_count") or 0)
    order_attempt_count = as_int(last.get("order_attempt_count")) or 0
    order_fill_count = as_int(last.get("order_fill_count")) or 0
    if feature_diff != 0:
        return "feature_readiness_gap"
    if signal_diff != 0:
        return "signal_count_gap"
    if order_attempt_count and order_fill_count < order_attempt_count:
        return "order_fill_gap_after_signal_parity"
    if abs(trade_count - expected_trades) > max(2, int(expected_trades * 0.20)):
        return "trade_lifecycle_gap_after_signal_parity"
    return "runtime_economics_gap_after_signal_and_feature_parity"


def build_runtime_receipt(execution_results: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    attempts_by_name = {str(attempt["attempt_name"]): attempt for attempt in attempts}
    rows: list[dict[str, Any]] = []
    for result in execution_results:
        attempt = attempts_by_name[str(result["attempt_name"])]
        runtime = result.get("runtime_outputs", {}) if isinstance(result.get("runtime_outputs"), Mapping) else {}
        last = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
        report = result.get("strategy_tester_report", {}) if isinstance(result.get("strategy_tester_report"), Mapping) else {}
        metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
        test_period = tester_period(attempt)
        proxy = attempt.get("proxy_kpi") if isinstance(attempt.get("proxy_kpi"), Mapping) else {}
        long_count = as_int(last.get("long_count")) or 0
        short_count = as_int(last.get("short_count")) or 0
        signal_count = long_count + short_count
        order_attempt_count = as_int(last.get("order_attempt_count")) or 0
        order_fill_count = as_int(last.get("order_fill_count")) or 0
        trade_count = as_int(metrics.get("trade_count")) or 0
        winning_trade_count = as_int(metrics.get("winning_trade_count")) or 0
        losing_trade_count = as_int(metrics.get("losing_trade_count")) or 0
        gross_profit = as_float(metrics.get("gross_profit"))
        gross_loss = as_float(metrics.get("gross_loss"))
        average_win = gross_profit / winning_trade_count if gross_profit is not None and winning_trade_count else None
        average_loss = gross_loss / losing_trade_count if gross_loss is not None and losing_trade_count else None
        payoff_ratio = abs(average_win / average_loss) if average_win is not None and average_loss not in (None, 0) else None
        runtime_dd = as_float(metrics.get("max_drawdown_percent"))
        proxy_dd = as_float(proxy.get("dd_pct"))
        report_rel = (report.get("html_report") or {}).get("path", "") if isinstance(report.get("html_report"), Mapping) else ""
        rows.append(
            {
                "run_id": RUN_ID,
                "attempt_name": attempt.get("attempt_name"),
                "candidate_id": attempt.get("candidate_id"),
                "axis_id": attempt.get("axis_id"),
                "split": attempt.get("split"),
                "test_period_start": test_period.get("start"),
                "test_period_end": test_period.get("end"),
                "calendar_days_exclusive": test_period.get("calendar_days_exclusive"),
                "tester_status": result.get("status"),
                "runtime_status": runtime.get("status", "missing"),
                "report_status": report.get("status", "missing"),
                "expected_rows": attempt.get("expected_rows"),
                "feature_ready_count": as_int(last.get("feature_ready_count")) or 0,
                "feature_ready_diff": (as_int(last.get("feature_ready_count")) or 0) - int(attempt.get("expected_rows") or 0),
                "expected_signal_count": attempt.get("expected_signal_count"),
                "signal_count": signal_count,
                "signal_count_diff": signal_count - int(attempt.get("expected_signal_count") or 0),
                "expected_selected_trade_count": attempt.get("expected_selected_trade_count"),
                "order_attempt_count": order_attempt_count,
                "order_fill_count": order_fill_count,
                "order_fill_rate": ratio(order_fill_count, order_attempt_count),
                "trade_count": trade_count,
                "trades_per_day": ratio(trade_count, test_period.get("calendar_days_exclusive")),
                "long_trade_count": metrics.get("long_trade_count"),
                "short_trade_count": metrics.get("short_trade_count"),
                "winning_trade_count": winning_trade_count,
                "losing_trade_count": losing_trade_count,
                "net_profit": metrics.get("net_profit"),
                "gross_profit": metrics.get("gross_profit"),
                "gross_loss": metrics.get("gross_loss"),
                "profit_factor": metrics.get("profit_factor"),
                "expectancy": metrics.get("expectancy"),
                "win_rate_percent": metrics.get("win_rate_percent"),
                "average_win": average_win,
                "average_loss": average_loss,
                "payoff_ratio": payoff_ratio,
                "recovery_factor": metrics.get("recovery_factor"),
                "max_drawdown_amount": metrics.get("max_drawdown_amount"),
                "max_drawdown_percent": runtime_dd,
                "proxy_net_profit": as_float(proxy.get("net")),
                "proxy_profit_factor": as_float(proxy.get("pf")),
                "proxy_trades_per_day": as_float(proxy.get("trades_per_day")),
                "proxy_dd_percent": proxy_dd,
                "dd_delta_runtime_minus_proxy": (runtime_dd - proxy_dd) if runtime_dd is not None and proxy_dd is not None else None,
                "gap_cause_summary": gap_cause_summary(attempt, metrics, last),
                "report_path": report_rel,
                "telemetry_path": runtime.get("telemetry_path", ""),
                "summary_path": runtime.get("summary_path", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def numeric_delta(runtime: Any, proxy: Any) -> float | None:
    runtime_value = as_float(runtime)
    proxy_value = as_float(proxy)
    if runtime_value is None or proxy_value is None:
        return None
    return runtime_value - proxy_value


def gap_class(metric: str, delta: Any) -> str:
    value = as_float(delta)
    if value is None:
        return f"{metric}_missing_comparison"
    if abs(value) <= 1e-9:
        return f"{metric}_exact"
    if abs(value) <= 0.05:
        return f"{metric}_small_gap"
    return f"{metric}_gap"


def gap_row(receipt: Mapping[str, Any], gap_type: str, metric: str, proxy_value: Any, runtime_value: Any, delta: Any, classification: str, evidence: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "attempt_name": receipt.get("attempt_name"),
        "candidate_id": receipt.get("candidate_id"),
        "axis_id": receipt.get("axis_id"),
        "split": receipt.get("split"),
        "gap_type": gap_type,
        "metric": metric,
        "proxy_value": proxy_value,
        "runtime_value": runtime_value,
        "delta": delta,
        "classification": classification,
        "evidence": evidence,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gap_classification(receipt: Mapping[str, Any]) -> list[dict[str, Any]]:
    signal_delta = receipt.get("signal_count_diff")
    feature_delta = receipt.get("feature_ready_diff")
    density_delta = numeric_delta(receipt.get("trades_per_day"), receipt.get("proxy_trades_per_day"))
    pf_delta = numeric_delta(receipt.get("profit_factor"), receipt.get("proxy_profit_factor"))
    dd_delta = numeric_delta(receipt.get("max_drawdown_percent"), receipt.get("proxy_dd_percent"))
    return [
        gap_row(receipt, "signal_count_parity", "signal_count", receipt.get("expected_signal_count"), receipt.get("signal_count"), signal_delta, "signal_count_exact" if signal_delta == 0 else "signal_count_gap", "runtime_summary_vs_onnx_signal_parity"),
        gap_row(receipt, "feature_readiness", "feature_ready_count", receipt.get("expected_rows"), receipt.get("feature_ready_count"), feature_delta, "feature_ready_exact" if feature_delta == 0 else "feature_ready_gap", "runtime_summary_feature_ready_count"),
        gap_row(receipt, "trade_density", "trades_per_day", receipt.get("proxy_trades_per_day"), receipt.get("trades_per_day"), density_delta, gap_class("trade_density", density_delta), "proxy_kpi_vs_strategy_tester_trade_count"),
        gap_row(receipt, "profit_factor", "profit_factor", receipt.get("proxy_profit_factor"), receipt.get("profit_factor"), pf_delta, gap_class("profit_factor", pf_delta), "proxy_kpi_vs_strategy_tester_report"),
        gap_row(receipt, "drawdown_percent", "drawdown_percent", receipt.get("proxy_dd_percent"), receipt.get("max_drawdown_percent"), dd_delta, gap_class("drawdown_percent", dd_delta), "proxy_dd_percent_vs_strategy_tester_dd"),
    ]


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipts = list(payload.get("runtime_receipt") or [])
    completed_receipts = [row for row in receipts if row.get("tester_status") == "completed"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "axis_count": len(payload.get("axis_contexts", [])),
        "attempt_count": len(payload.get("attempts", [])),
        "completed_attempt_count": len(completed_receipts),
        "exported_count": sum(1 for row in payload.get("artifact_rows", []) if row.get("export_status") == "exported_onnx_parity_passed"),
        "runtime_receipt_rows": len(receipts),
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
    }


def grok_identity() -> dict[str, Any]:
    return {
        "packet_root": rel(GROK_PACKET_ROOT),
        "prompt_path": rel(GROK_PROMPT),
        "clean_output_path": rel(GROK_CLEAN),
        "metadata_path": rel(GROK_METADATA),
        "prompt_sha256": sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else "",
        "clean_output_sha256": sha256_file(GROK_CLEAN) if path_exists(GROK_CLEAN) else "",
        "metadata_exists": path_exists(GROK_METADATA),
        "advice_classification": "accepted_with_guardrails_needs_local_verification_on_packaging",
    }


def experiment_design_payload() -> dict[str, Any]:
    return {
        "hypothesis": "F70 label/regime stability near-miss axes can reveal whether density-aware label selection transfers through ONNX and RuntimeVetoTape into MT5 runtime.",
        "decision_use": "runtime_probe_observation and proxy/runtime repair planning only",
        "comparison_baseline": "F70C proxy KPI by split; F69 exact-parity bridge is reference-only infrastructure memory",
        "control_variables": ["US100 M5", "RuntimeProbeEA", "validation/OOS split", "fixed two diagnostic axes", "edge_margin decision mode", "ATR SL/TP from label parameters"],
        "changed_variables": ["model family axis: ExtraTrees reference vs small NN hypothesis carrier", "label target: trend quality vs volatility expansion", "runtime materialization"],
        "sample_scope": "Tier A validation/OOS windows from F70 model input frame",
        "success_criteria": "ONNX probability/signal parity and at least one MT5 tester/runtime telemetry record or exact blocker",
        "failure_criteria": "export/parity/veto tape/compile/tester output blocked, or runtime economics collapse after parity",
        "invalid_conditions": "candidate id mismatch, missing Grok pre-review, missing feature order, wrong decision-mode mapping, timestamp handoff mismatch",
        "stop_conditions": "after fixed two-axis runtime probe attempt; no threshold sweep or post-hoc tuning inside F70D",
        "evidence_plan": "run_manifest, ONNX/export rows, probability/signal parity CSV, runtime receipt CSV, gap classification CSV, MT5 reports, ledgers",
    }


def run_manifest(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "claim_boundary": CLAIM_BOUNDARY,
        "producer": "stage_pipelines/stage_frontier_70/frontier70d_label_regime_stability_runtime_probe.py",
        "experiment_design": experiment_design_payload(),
        "grok_packet": grok_identity(),
        "source_inputs": [rel(F70C_SUMMARY), rel(f70b.MODEL_INPUT), rel(f70b.RAW_US100)],
        "axis_specs": [axis.__dict__ for axis in AXES],
        "artifact_rows": payload.get("artifact_rows", []),
        "probability_parity_path": rel(RUN_ROOT / "f70d_onnx_probability_parity.csv"),
        "signal_parity_path": rel(RUN_ROOT / "f70d_onnx_signal_parity.csv"),
        "runtime_receipt_path": rel(RUN_ROOT / "f70d_runtime_probe_receipt.csv"),
        "gap_classification_path": rel(RUN_ROOT / "f70d_gap_classification.csv"),
        "attempts": payload.get("attempts", []),
        "compile_payload": payload.get("compile_payload"),
        "execution_results": payload.get("execution_results", []),
        "strategy_tester_reports": payload.get("strategy_tester_reports", []),
        "mt5_kpi_records": payload.get("mt5_kpi_records", []),
        "summary": build_summary(payload),
        "next_action": NEXT_RUN_ID,
    }


def report_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    lines = [
        "# F70D Label-Regime Stability MT5 Runtime Probe(F70D 라벨-장세 안정성 MT5 런타임 탐침)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "## Action And Effect(행동과 효과)",
        "",
        "Action(행동): F70C near-miss axes(F70C 근접 실패 축) 2개를 ONNX(온엑스), RuntimeVetoTape(런타임 차단 테이프), MT5 Strategy Tester(MT5 전략 테스터)로 물질화했다.",
        "",
        "Effect(효과): proxy-only clue(프록시 전용 단서)가 runtime execution(런타임 실행)에서 신호, 피처, 거래 경제성으로 어떻게 달라지는지 관찰한다.",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- attempts(시도): `{len(payload.get('attempts', []))}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## ONNX And Signal Parity(ONNX와 신호 동등성)",
        "",
        "| axis(축) | candidate(후보) | role(역할) | export(내보내기) | probability parity(확률 동등성) | signal parity(신호 동등성) |",
        "|---|---|---|---|---|---|",
    ]
    for row in payload.get("artifact_rows", []):
        lines.append(
            f"| `{row.get('axis_id')}` | `{row.get('candidate_id')}` | `{row.get('role')}` | `{row.get('export_status')}` | `{row.get('probability_parity_passed')}` | `{row.get('signal_parity_passed')}` |"
        )
    lines.extend(
        [
            "",
            "## Runtime KPI(런타임 핵심 성과 지표)",
            "",
            "| axis(축) | split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for row in payload.get("runtime_receipt", []):
        lines.append(
            "| `{axis}` | `{split}` | `{start}..{end}` | `{net}` | `{gp}` | `{gl}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{sig}` | `{feat}` | `{gap}` |".format(
                axis=row.get("axis_id"),
                split=row.get("split"),
                start=row.get("test_period_start"),
                end=row.get("test_period_end"),
                net=fmt(row.get("net_profit")),
                gp=fmt(row.get("gross_profit")),
                gl=fmt(row.get("gross_loss")),
                pf=fmt(row.get("profit_factor")),
                dd=fmt(row.get("max_drawdown_percent")),
                trades=fmt(row.get("trade_count")),
                tpd=fmt(row.get("trades_per_day")),
                sig=fmt(row.get("signal_count_diff")),
                feat=fmt(row.get("feature_ready_diff")),
                gap=row.get("gap_cause_summary", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Runtime Parity Boundary(런타임 동등성 경계)",
            "",
            "- research_path(연구 경로): `stage_pipelines/stage_frontier_70/frontier70d_label_regime_stability_runtime_probe.py`.",
            "- runtime_path(런타임 경로): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5` and include modules(포함 모듈).",
            "- shared_contract(공유 계약): feature order hash(피처 순서 해시), ONNX probability output(온엑스 확률 출력), edge_margin decision mode(엣지 마진 의사결정), RuntimeVetoTape selection mask(런타임 차단 테이프 선택 마스크), ATR SL/TP(평균진폭 손절/익절), max hold bars(최대 보유 봉수).",
            "- known_differences(알려진 차이): proxy non-overlap(프록시 비중첩)은 EA max hold/cooldown(EA 최대 보유/쿨다운)과 같지 않을 수 있어 trade count gap(거래 수 간극)을 별도로 기록한다.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return lines


def gate_audit_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    return [
        "# F70D Required Gate Coverage Audit(F70D 필수 게이트 커버리지 감사)",
        "",
        f"- updated_at_utc(갱신): `{created_at}`",
        f"- Grok pre-MT5 review(그록 MT5 전 검토): `{rel(GROK_CLEAN)}`.",
        f"- candidate axes(후보 축): `{summary['axis_count']}`.",
        f"- exported/parity passed(내보내기/동등성 통과): `{summary['exported_count']}`.",
        f"- MT5 attempts(MT5 시도): `{summary['attempt_count']}`.",
        f"- completed attempts(완료 시도): `{summary['completed_attempt_count']}`.",
        f"- runtime receipt rows(런타임 영수증 행): `{summary['runtime_receipt_rows']}`.",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`.",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`.",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`.",
    ]


def grok_receipt_lines(created_at: str) -> list[str]:
    return [
        "# F70D Pre-MT5 Grok Receipt(F70D MT5 전 그록 영수증)",
        "",
        f"- created_at_utc(생성): `{created_at}`",
        "- trigger_reason(트리거 이유): major validation before MT5 Runtime Probe(MT5 런타임 탐침 전 주요 검증).",
        "- review_size(검토 크기): `medium(중간)`.",
        "- direction_before_grok(그록 전 방향): F70C two near-miss axes(F70C 근접 실패 축 2개)를 diagnostic runtime probe(진단 런타임 탐침)로 물질화.",
        f"- bounded_evidence(제한 근거): `{rel(GROK_PROMPT)}`.",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else ''}`.",
        f"- grok_output_identity(그록 출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{sha256_file(GROK_CLEAN) if path_exists(GROK_CLEAN) else ''}`.",
        "- advice_classification(조언 분류): `accepted_with_guardrails_needs_local_verification(보호 조건 포함 수용, 로컬 검증 필요)`.",
        "- accepted(수용): fixed two-axis runtime probe(고정 2축 런타임 탐침), no threshold sweep(임계값 탐색 없음), role separation(역할 분리).",
        "- needs_local_verification(로컬 검증 필요): ONNX export(온엑스 내보내기), probability/signal parity(확률/신호 동등성), veto tape alignment(차단 테이프 정렬), tester output(테스터 출력).",
        "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        "- final_codex_direction(최종 Codex 방향): proceed with fixed diagnostic MT5 runtime probe observation(고정 진단 MT5 런타임 탐침 관찰 진행).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def write_outputs(payload: Mapping[str, Any], created_at: str) -> None:
    write_json(RUN_ROOT / "frontier70D_runtime_probe_execution_result.json", payload)
    write_json(RUN_ROOT / "frontier70D_runtime_probe_summary.json", build_summary(payload))
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(payload, created_at))
    write_json(RUN_ROOT / "f70d_experiment_design.json", experiment_design_payload())
    write_json(RUN_ROOT / "f70d_grok_review_classification.json", grok_identity())
    write_csv(RUN_ROOT / "f70d_candidate_axis_materialization.csv", payload.get("artifact_rows", []))
    write_csv(RUN_ROOT / "f70d_onnx_probability_parity.csv", payload.get("probability_parity", []))
    write_csv(RUN_ROOT / "f70d_onnx_signal_parity.csv", payload.get("signal_parity", []))
    write_csv(RUN_ROOT / "f70d_local_verification.csv", payload.get("local_verification", []))
    write_csv(RUN_ROOT / "f70d_runtime_probe_receipt.csv", payload.get("runtime_receipt", []), RUNTIME_RECEIPT_COLUMNS)
    write_csv(RUN_ROOT / "f70d_gap_classification.csv", payload.get("gap_classification", []), GAP_COLUMNS)
    write_csv(REVIEWS_ROOT / "f70d_candidate_axis_materialization_review.csv", payload.get("artifact_rows", []))
    write_csv(REVIEWS_ROOT / "f70d_onnx_signal_parity_review.csv", payload.get("signal_parity", []))
    write_csv(REVIEWS_ROOT / "f70d_runtime_probe_receipt_review.csv", payload.get("runtime_receipt", []), RUNTIME_RECEIPT_COLUMNS)
    write_csv(REVIEWS_ROOT / "f70d_gap_classification_review.csv", payload.get("gap_classification", []), GAP_COLUMNS)
    write_md(REVIEWS_ROOT / "frontier70D_label_regime_stability_runtime_probe_report.md", report_lines(payload, created_at))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f70d.md", gate_audit_lines(payload, created_at))
    write_md(REVIEWS_ROOT / "f70d_pre_mt5_grok_receipt.md", grok_receipt_lines(created_at))


def best_receipt(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    receipts = [row for row in payload.get("runtime_receipt", []) if row.get("split") == "oos"]
    if not receipts:
        receipts = list(payload.get("runtime_receipt", []))
    if not receipts:
        return {}
    return max(receipts, key=lambda row: as_float(row.get("profit_factor")) or -999.0)


def update_state_and_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = best_receipt(payload)
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "label_regime_stability_mt5_runtime_probe(라벨-장세 안정성 MT5 런타임 탐침)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "mt5_runtime_probe_observation(MT5 런타임 탐침 관찰)",
        "tier_scope": "Tier A separate(Tier A 분리)",
        "kpi_scope": "runtime_probe_kpi_and_proxy_gap(런타임 탐침 KPI와 프록시 간극)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REVIEWS_ROOT / "frontier70D_label_regime_stability_runtime_probe_report.md"),
        "primary_kpi": f"attempts={summary['attempt_count']};completed_attempts={summary['completed_attempt_count']};exported={summary['exported_count']}",
        "guardrail_kpi": "joint_soft=0;final_like=0 upfront;no authority claims",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked(차단)",
        "notes": "F70D materialized fixed diagnostic axes after Grok pre-MT5 review.",
        "run_number": "frontier70D",
        "date": created_at[:10],
        "decision": "proceed_to_f70e_proxy_runtime_gap_analysis",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEWS_ROOT / "frontier70D_label_regime_stability_runtime_probe_report.md"),
        "trained_models": summary["axis_count"],
        "onnx_parity": summary["exported_count"],
        "best_proxy": best.get("candidate_id", ""),
        "candidate_rows": summary["axis_count"],
        "best_model_id": best.get("axis_id", ""),
        "best_proxy_net": fmt(best.get("proxy_net_profit")),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_ROOT / "frontier70D_runtime_probe_execution_result.json"),
        "view": "mt5_runtime_probe(MT5 런타임 탐침)",
        "tier": "Tier A separate(Tier A 분리)",
        "metric_scope": "runtime_probe_observation(런타임 탐침 관찰)",
        "net_profit": fmt(best.get("net_profit")),
        "profit_factor": fmt(best.get("profit_factor")),
        "drawdown": fmt(best.get("max_drawdown_percent")),
        "trade_count": fmt(best.get("trade_count")),
        "result_status": payload.get("status"),
        "feature_count": "",
        "lane": "runtime_probe(런타임 탐침)",
        "family": "runtime_validation(런타임 검증)",
        "primary_report": rel(REVIEWS_ROOT / "frontier70D_label_regime_stability_runtime_probe_report.md"),
        "attempt_count": summary["attempt_count"],
        "source_package_run_id": PARENT_RUN_ID,
        "row_id": f"{RUN_ID}__runtime_probe",
        "scoreboard": "runtime_probe(런타임 탐침)",
        "evidence_boundary": "runtime_probe_observation_only(런타임 탐침 관찰 전용)",
        "work_family": "runtime_validation(런타임 검증)",
        "evidence_scope": "mt5_runtime_probe(MT5 런타임 탐침)",
        "run_key": RUN_ID,
        "question": "Do F70 label-regime stability near-miss axes transfer into MT5 runtime?(F70 라벨-장세 안정성 근접 실패 축이 MT5 런타임으로 전이되는가)",
        "next_action": NEXT_RUN_ID,
        "result_judgment": payload.get("judgment"),
        "final_decision_path": rel(REVIEWS_ROOT / "frontier70D_label_regime_stability_runtime_probe_report.md"),
        "created_at": created_at,
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f70d.md"),
        "artifact_count": len(payload.get("artifact_rows", [])),
        "created_at_utc": created_at,
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f70d.md"),
        "kpi_summary": f"attempts={summary['attempt_count']};completed={summary['completed_attempt_count']};runtime_rows={summary['runtime_receipt_rows']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "trade_density": fmt(best.get("trades_per_day")),
        "source_authority": "runtime_probe_observation_no_authority(런타임 탐침 관찰, 권위 없음)",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_runtime_probe(전선 런타임 탐침)",
        "run_type": "label_regime_stability_runtime_probe(라벨-장세 안정성 런타임 탐침)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "frontier70D_runtime_probe_execution_result.json"),
        "result_path": rel(REVIEWS_ROOT / "frontier70D_label_regime_stability_runtime_probe_report.md"),
        "selected_net_profit": fmt(best.get("net_profit")),
        "selected_profit_factor": fmt(best.get("profit_factor")),
        "selected_trade_density": fmt(best.get("trades_per_day")),
        "max_drawdown_percent": fmt(best.get("max_drawdown_percent")),
        "strict_joint_pass_count": 0,
    }
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", ledger_row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")
    upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", ledger_row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", ledger_row)
    update_text_state(payload, created_at, summary, best)


def update_text_state(payload: Mapping[str, Any], created_at: str, summary: Mapping[str, Any], best: Mapping[str, Any]) -> None:
    workspace_lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f70_runtime_probe_attempted_observation_recorded_no_authority(F70 런타임 탐침 시도/관찰 기록, 권위 없음)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: due_at_f70_closeout_not_before_gap_analysis",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        f'  - "F70D action(행동): diagnostic axes(진단 축) `{summary["axis_count"]}`개를 ONNX/RuntimeVetoTape/MT5(온엑스/런타임 차단 테이프/MT5)로 물질화했다."',
        f'  - "Effect(효과): attempts(시도) `{summary["attempt_count"]}`, completed_attempts(완료 시도) `{summary["completed_attempt_count"]}`, runtime_receipt_rows(런타임 영수증 행) `{summary["runtime_receipt_rows"]}`를 기록했다."',
        f'  - "Representative runtime OOS net/PF/DD/trades_day(대표 런타임 표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get("net_profit"))}/{fmt(best.get("profit_factor"))}/{fmt(best.get("max_drawdown_percent"))}/{fmt(best.get("trades_per_day"))}`."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}`에서 proxy/runtime gap(프록시/런타임 간극)을 분석하고 repair(수리) 또는 closeout(마감)을 결정한다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(workspace_lines) + "\n", encoding="utf-8-sig")
    current_lines = [
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
        "Action(행동): F70D label-regime stability MT5 runtime probe(F70D 라벨-장세 안정성 MT5 런타임 탐침)를 실행했다.",
        "",
        "Effect(효과): F70C 근접 실패 proxy(프록시) 축을 실제 MT5 Strategy Tester(MT5 전략 테스터)와 runtime telemetry(런타임 기록)로 관찰할 근거를 만들었다.",
        "",
        f"- status(상태): `{payload.get('status')}`.",
        f"- judgment(판정): `{payload.get('judgment')}`.",
        f"- attempts/completed(시도/완료): `{summary['attempt_count']}` / `{summary['completed_attempt_count']}`.",
        f"- runtime receipt rows(런타임 영수증 행): `{summary['runtime_receipt_rows']}`.",
        f"- representative OOS net/PF/DD/trades_day(대표 표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('net_profit'))}` / `{fmt(best.get('profit_factor'))}` / `{fmt(best.get('max_drawdown_percent'))}` / `{fmt(best.get('trades_per_day'))}`.",
        "",
        "## Key Artifacts(핵심 산출물)",
        "",
        f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier70D_label_regime_stability_runtime_probe_report.md`",
        f"- runtime receipt(런타임 영수증): `stages/{STAGE_ID}/03_reviews/f70d_runtime_probe_receipt_review.csv`",
        f"- gap classification(간극 분류): `stages/{STAGE_ID}/03_reviews/f70d_gap_classification_review.csv`",
        f"- Grok receipt(그록 영수증): `stages/{STAGE_ID}/03_reviews/f70d_pre_mt5_grok_receipt.md`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", current_lines)
    selection_lines = [
        "# F70 Selection Status(F70 선택 상태)",
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
        f"- completed_action(완료 행동): `{RUN_ID}` label-regime stability runtime probe(라벨-장세 안정성 런타임 탐침).",
        f"- attempts/completed(시도/완료): `{summary['attempt_count']}` / `{summary['completed_attempt_count']}`.",
        f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier70D_label_regime_stability_runtime_probe_report.md`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}`.",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(STAGE_ROOT / "04_selected" / "selection_status.md", selection_lines)
    append_once(
        ROOT / "docs/registers/idea_registry.md",
        f"{RUN_ID} executed",
        f"""### {RUN_ID}

- {RUN_ID} executed(실행): F70C near-miss label-regime axes(F70C 근접 실패 라벨-장세 축)를 ONNX/RuntimeVetoTape/MT5(온엑스/런타임 차단 테이프/MT5)로 물질화했다. Status(상태): `{payload.get('status')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
""",
    )


def main() -> int:
    args = parse_args()
    ensure_dirs()
    created_at = utc_now()
    contexts = build_axis_contexts()
    artifact_rows, probability_rows, signal_rows, local_verification = materialize_candidates(Path(args.common_files_root), contexts)
    attempts = build_attempts(contexts, artifact_rows)
    payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS_MATERIALIZED,
        "judgment": "mt5_runtime_probe_materialized_pending_execution_no_authority",
        "claim_boundary": CLAIM_BOUNDARY,
        "grok_packet": grok_identity(),
        "axis_contexts": [
            {
                "axis": context["axis"].__dict__,
                "feature_order_hash": context["feature_order_hash"],
                "threshold": context["threshold"],
                "candidate_id_match": context["candidate_id_match"],
                "candidate_id_check": context["candidate_id_check"],
                "summary_reference": context["summary_reference"],
            }
            for context in contexts
        ],
        "artifact_rows": artifact_rows,
        "probability_parity": probability_rows,
        "signal_parity": signal_rows,
        "local_verification": local_verification,
        "attempts": attempts,
        "execution_results": [],
        "strategy_tester_reports": [],
        "mt5_kpi_records": [],
        "runtime_receipt": [],
        "gap_classification": [],
    }
    if args.materialize_only or not args.execute:
        write_outputs(payload, created_at)
        print(json.dumps(json_ready({"status": payload["status"], "attempt_count": len(attempts)}), ensure_ascii=False, indent=2))
        return 0

    compile_payload = compile_runtime_ea(Path(args.metaeditor_path))
    payload["compile_payload"] = compile_payload
    execution_results = execute_attempts(args, attempts, compile_payload)
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=Path(args.terminal_data_root),
        run_output_root=RUN_ROOT,
        attempts=attempts,
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    receipt_rows = build_runtime_receipt(execution_results, attempts)
    gap_rows = [row for receipt in receipt_rows for row in build_gap_classification(receipt)]
    execution_completed = bool(execution_results) and any(row.get("status") == "completed" for row in execution_results)
    report_completed = bool(kpi_records)
    payload.update(
        {
            "status": STATUS_COMPLETED if execution_completed and report_completed else STATUS_BLOCKED,
            "judgment": (
                "runtime_probe_observation_recorded_no_authority"
                if execution_completed and report_completed
                else "runtime_probe_attempt_blocked_repair_required_no_authority"
            ),
            "execution_results": execution_results,
            "strategy_tester_reports": report_records,
            "mt5_kpi_records": kpi_records,
            "runtime_receipt": receipt_rows,
            "gap_classification": gap_rows,
        }
    )
    write_outputs(payload, created_at)
    update_state_and_ledgers(payload, created_at)
    print(
        json.dumps(
            json_ready(
                {
                    "status": payload["status"],
                    "judgment": payload["judgment"],
                    "attempt_count": len(attempts),
                    "completed_attempt_count": build_summary(payload)["completed_attempt_count"],
                    "exported_count": build_summary(payload)["exported_count"],
                    "runtime_receipt_rows": len(receipt_rows),
                    "next_action": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
