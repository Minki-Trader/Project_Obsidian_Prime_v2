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
from sklearn.base import clone

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage_frontier_67.frontier67c_runtime_native_order_intent_economics import (
    as_float,
    as_int,
    extract_deal_metrics,
    ratio,
)
from stage_pipelines.stage_frontier_68.frontier68d_mt5_runtime_probe_candidate_axis_materialization import (
    clear_runtime_outputs,
    empty_deal_metrics,
    gap_cause_summary,
    reconciliation_error,
)
from stage_pipelines.stage_frontier_69 import frontier69b_event_first_first_hit_proxy_sweep as f69b
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
)


STAGE_ID = f69b.STAGE_ID
RUN_ID = "frontier69D_event_first_onnx_runtime_probe_v1"
PARENT_RUN_ID = "frontier69C_repair_event_first_label_or_feature_surface_v1"
NEXT_RUN_ID = "frontier69E_proxy_runtime_gap_analysis_and_repair_decision_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
MT5_ROOT = RUN_ROOT / "mt5"
MODEL_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "features"
VETO_ROOT = RUN_ROOT / "runtime_veto_tapes"
REPORT_ROOT = RUN_ROOT / "reports"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier69D_event_first_onnx_runtime_probe"

GROK_PACKET_ROOT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f69d_pre_mt5_event_first_runtime_probe"
GROK_PROMPT = GROK_PACKET_ROOT / "prompts/f69d_pre_mt5_event_first_runtime_probe_prompt.md"
GROK_CLEAN = GROK_PACKET_ROOT / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET_ROOT / "outputs/metadata.json"

F69B_SUMMARY = REVIEWS_ROOT / "f69b_proxy_candidate_summary_review.csv"
F69B_KPI = REVIEWS_ROOT / "f69b_proxy_kpi_by_split_review.csv"
F69C_SUMMARY = REVIEWS_ROOT / "f69c_proxy_candidate_summary_review.csv"

CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STATUS_COMPLETED = "completed_mt5_runtime_probe_observation_no_authority(MT5 런타임 탐침 관찰 완료, 권위 없음)"
STATUS_BLOCKED = "blocked_mt5_runtime_probe_attempted_repair_required_no_authority(MT5 런타임 탐침 시도 차단, 수리 필요, 권위 없음)"
STATUS_MATERIALIZED = "materialized_pending_mt5_runtime_probe_execution_no_authority(물질화 완료, MT5 런타임 탐침 실행 대기, 권위 없음)"


@dataclass(frozen=True)
class AxisSpec:
    axis_id: str
    candidate_id: str
    role: str
    target_id: str
    feature_set_id: str
    model_id: str
    event_id: str
    side_policy: str
    threshold_quantile: float
    priority: int


AXES: tuple[AxisSpec, ...] = (
    AxisSpec(
        axis_id="pf_sparse_export_axis",
        candidate_id="f69b_9dd9ed423f5f",
        role="runtime_probe_axis_only_high_pf_sparse_exportable_not_completion_candidate",
        target_id="fh_h3_sl09_tp135_edge10",
        feature_set_id="price_path_core_v1",
        model_id="shallow_extra_trees_v1",
        event_id="event_session_edges",
        side_policy="long_only",
        threshold_quantile=0.95,
        priority=1,
    ),
    AxisSpec(
        axis_id="density_weak_export_axis",
        candidate_id="f69b_968cfd55b728",
        role="runtime_probe_axis_only_dense_weak_pf_exportable_not_completion_candidate",
        target_id="fh_h3_sl09_tp135_edge10",
        feature_set_id="morph_session_core_v1",
        model_id="shallow_extra_trees_v1",
        event_id="event_bb_squeeze_release",
        side_policy="long_only",
        threshold_quantile=0.65,
        priority=2,
    ),
)

SPLITS = ("validation", "oos")

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
    "deal_count",
    "deal_in_count",
    "deal_out_count",
    "deal_minus_order_fill",
    "deal_count_equals_2x_trade",
    "order_fill_equals_deal_count",
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
    "deal_profit_sum",
    "deal_commission_sum",
    "deal_swap_sum",
    "deal_cost_sum",
    "net_reconciliation_error",
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
    parser = argparse.ArgumentParser(description="F69D event-first ONNX runtime probe.")
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


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig")


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


def sha256_file(path: Path) -> str:
    return f69b.sha256_file(path)


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


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_ROOT, FEATURE_ROOT, VETO_ROOT, MT5_ROOT, MT5_ROOT / "reports", REPORT_ROOT, REVIEWS_ROOT, STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def match_one(items: Sequence[Any], attr: str, value: str) -> Any:
    matches = [item for item in items if str(getattr(item, attr)) == value]
    if len(matches) != 1:
        raise RuntimeError(f"match failed for {attr}={value}: {len(matches)}")
    return matches[0]


def candidate_summary_rows() -> dict[str, Mapping[str, Any]]:
    rows: dict[str, Mapping[str, Any]] = {}
    for path in (F69B_SUMMARY, F69C_SUMMARY):
        if not path_exists(path):
            continue
        frame = read_csv(path)
        for row in frame.to_dict("records"):
            candidate_id = str(row.get("candidate_id", ""))
            if candidate_id:
                rows[candidate_id] = row
    return rows


def proxy_kpi_by_candidate() -> dict[tuple[str, str], Mapping[str, Any]]:
    frame = read_csv(F69B_KPI)
    return {(str(row["candidate_id"]), str(row["split"])): row for row in frame.to_dict("records")}


def threshold_values(side_policy: str, edge_threshold: float) -> dict[str, float | str]:
    if side_policy == "long_only":
        return {"short_threshold": 1.1, "long_threshold": 0.0, "min_margin": float(edge_threshold), "decision_mode": "threshold_margin"}
    if side_policy == "short_only":
        return {"short_threshold": 0.0, "long_threshold": 1.1, "min_margin": float(edge_threshold), "decision_mode": "threshold_margin"}
    return {"short_threshold": 0.0, "long_threshold": 0.0, "min_margin": float(edge_threshold), "decision_mode": "threshold_margin"}


def build_axis_contexts() -> list[dict[str, Any]]:
    base, raw = f69b.load_frames()
    summary_lookup = candidate_summary_rows()
    proxy_lookup = proxy_kpi_by_candidate()
    feature_lookup = {feature.feature_set_id: feature for feature in f69b.feature_sets(base)}
    model_lookup = {model.model_id: model for model in f69b.model_specs()}
    target_lookup = {target.target_id: target for target in f69b.target_specs()}
    contexts: list[dict[str, Any]] = []

    for axis in AXES:
        target = target_lookup[axis.target_id]
        feature_set = feature_lookup[axis.feature_set_id]
        model_spec = model_lookup[axis.model_id]
        frame = f69b.build_target_frame(base, raw, target)
        event = match_one(f69b.event_specs(frame), "event_id", axis.event_id)
        train_mask = frame["split"].astype(str).eq("train").to_numpy()
        estimator = clone(model_spec.build())
        estimator.fit(frame.loc[train_mask, list(feature_set.columns)], frame.loc[train_mask, "target_class"])
        classes = list(getattr(estimator, "classes_", getattr(estimator[-1], "classes_", [])))
        train_proba = estimator.predict_proba(frame.loc[train_mask, list(feature_set.columns)])
        train_side, train_edge = f69b.side_and_edge(train_proba, classes)
        train_side = f69b.apply_side_policy(train_side, axis.side_policy)
        train_pool_mask = event.mask[train_mask] & (train_side != 1) & np.isfinite(train_edge)
        train_pool = train_edge[train_pool_mask]
        if len(train_pool) == 0:
            raise RuntimeError(f"empty threshold pool for {axis.axis_id}")
        edge_threshold = float(np.quantile(train_pool, axis.threshold_quantile))
        candidate_id_check = "f69b_" + f69b.stable_id(
            [
                target.target_id,
                feature_set.feature_set_id,
                model_spec.model_id,
                event.event_id,
                axis.threshold_quantile,
                axis.side_policy,
            ]
        )
        split_payload: dict[str, Any] = {}
        for split_name in ("train", *SPLITS):
            split_mask = frame["split"].astype(str).eq(split_name).to_numpy()
            proba = estimator.predict_proba(frame.loc[split_mask, list(feature_set.columns)])
            side, edge = f69b.side_and_edge(proba, classes)
            adjusted_side = f69b.apply_side_policy(side.copy(), axis.side_policy)
            local_event = event.mask[split_mask]
            raw_signal = local_event & (adjusted_side != 1) & (edge >= edge_threshold)
            selected = f69b.non_overlap_indices(raw_signal, target.horizon_bars, target.horizon_bars)
            split_payload[split_name] = {
                "split_mask": split_mask,
                "frame": frame.loc[split_mask].copy().reset_index(drop=True),
                "proba": proba,
                "side": side,
                "adjusted_side": adjusted_side,
                "edge": edge,
                "event_mask": local_event,
                "raw_signal": raw_signal,
                "selected_indices": selected,
                "expected_rows": int(split_mask.sum()),
                "expected_signal_count": int(raw_signal.sum()),
                "expected_selected_trade_count": int(len(selected)),
            }
        kpi_rows = [
            f69b.evaluate_candidate(frame, split_name, split_payload[split_name]["split_mask"], split_payload[split_name]["side"], split_payload[split_name]["edge"], event.mask, f69b.CandidateSpec(
                candidate_id=axis.candidate_id,
                target=target,
                feature_set=feature_set,
                model=model_spec,
                event_id=event.event_id,
                threshold_quantile=axis.threshold_quantile,
                edge_threshold=edge_threshold,
                side_policy=axis.side_policy,
                cooldown_bars=target.horizon_bars,
            ))
            for split_name in SPLITS
        ]
        contexts.append(
            {
                "axis": axis,
                "target": target,
                "feature_set": feature_set,
                "model_spec": model_spec,
                "event": event,
                "frame": frame,
                "estimator": estimator,
                "classes": classes,
                "feature_columns": list(feature_set.columns),
                "feature_order_hash": ordered_hash(feature_set.columns),
                "edge_threshold": edge_threshold,
                "candidate_id_check": candidate_id_check,
                "candidate_id_match": candidate_id_check == axis.candidate_id,
                "summary_reference": summary_lookup.get(axis.candidate_id, {}),
                "proxy_kpi": {split: dict(proxy_lookup.get((axis.candidate_id, split), {})) for split in SPLITS},
                "recomputed_kpi": {row["split"]: row for row in kpi_rows},
                "split_payload": split_payload,
                "threshold_values": threshold_values(axis.side_policy, edge_threshold),
            }
        )
    return contexts


def onnx_probabilities(onnx_path: Path, values: np.ndarray) -> np.ndarray:
    import onnxruntime as ort

    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: np.asarray(values, dtype="float32")})
    candidates = [output for output in outputs if isinstance(output, np.ndarray) and output.ndim == 2 and output.shape[1] == 3]
    if len(candidates) != 1:
        raise RuntimeError(f"expected one probability output, got {[getattr(output, 'shape', None) for output in outputs]}")
    return np.asarray(candidates[0], dtype="float64")


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
        metadata_columns=("target_class",),
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


def write_veto_tape(context: Mapping[str, Any], output_path: Path) -> dict[str, Any]:
    frame: pd.DataFrame = context["frame"]
    event_mask = np.asarray(context["event"].mask, dtype=bool)
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
        "format": "runtime_veto_tape_entry_veto_outside_event",
    }


def parity_rows(context: Mapping[str, Any], artifact: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    onnx_path = ROOT / str(artifact["onnx_path"])
    estimator = context["estimator"]
    feature_columns = list(context["feature_columns"])
    classes = list(context["classes"])
    axis: AxisSpec = context["axis"]
    probability_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    for split in ("train", *SPLITS):
        split_frame: pd.DataFrame = context["split_payload"][split]["frame"]
        values = split_frame.loc[:, feature_columns].to_numpy(dtype="float64")
        sample = values[: min(len(values), 2048)]
        probability = check_onnxruntime_probability_parity(estimator, onnx_path, sample, tolerance=1e-5)
        probability_rows.append({"candidate_id": axis.candidate_id, "axis_id": axis.axis_id, "split": split, **probability})
        onnx_proba = onnx_probabilities(onnx_path, values)
        onnx_side, onnx_edge = f69b.side_and_edge(onnx_proba, classes)
        onnx_side = f69b.apply_side_policy(onnx_side, axis.side_policy)
        sklearn_side = np.asarray(context["split_payload"][split]["adjusted_side"], dtype=int)
        sklearn_edge = np.asarray(context["split_payload"][split]["edge"], dtype=float)
        event_mask = np.asarray(context["split_payload"][split]["event_mask"], dtype=bool)
        threshold = float(context["edge_threshold"])
        sklearn_signal = event_mask & (sklearn_side != 1) & (sklearn_edge >= threshold)
        onnx_signal = event_mask & (onnx_side != 1) & (onnx_edge >= threshold)
        signal_rows.append(
            {
                "candidate_id": axis.candidate_id,
                "axis_id": axis.axis_id,
                "split": split,
                "rows": int(len(split_frame)),
                "sklearn_signal_count": int(sklearn_signal.sum()),
                "onnx_signal_count": int(onnx_signal.sum()),
                "signal_count_diff": int(onnx_signal.sum() - sklearn_signal.sum()),
                "signal_mismatch_count": int((onnx_signal != sklearn_signal).sum()),
                "side_mismatch_on_signal_count": int(((onnx_side != sklearn_side) & (onnx_signal | sklearn_signal)).sum()),
                "max_edge_abs_diff": float(np.abs(onnx_edge - sklearn_edge).max()) if len(onnx_edge) else 0.0,
                "event_active_rows": int(event_mask.sum()),
                "passed": bool(int((onnx_signal != sklearn_signal).sum()) == 0 and int(((onnx_side != sklearn_side) & (onnx_signal | sklearn_signal)).sum()) == 0),
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

    add_check("grok_clean_output_exists", path_exists(GROK_CLEAN), rel(GROK_CLEAN), "Grok pre-MT5 review(그록 MT5 전 검토)가 기록되어 있다.")
    add_check("grok_metadata_exists", path_exists(GROK_METADATA), rel(GROK_METADATA), "Grok wrapper metadata(그록 래퍼 메타데이터)가 기록되어 있다.")
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
                "Proxy candidate identity(프록시 후보 정체성)를 같은 해시 규칙으로 재구성했다.",
            )
            add_check(
                f"{axis.candidate_id}_onnx_probability_parity",
                all_probability_pass,
                f"rows={len(probability)}",
                "ONNX probability output(ONNX 확률 출력)이 sklearn(사이킷런)과 맞는다.",
            )
            add_check(
                f"{axis.candidate_id}_onnx_signal_parity",
                all_signal_pass,
                f"rows={len(signal)}",
                "ONNX event-first signal(ONNX 이벤트 우선 신호)이 프록시 신호와 맞는다.",
            )
        except Exception as exc:  # noqa: BLE001 - export or parity failure is evidence.
            artifact = {
                "candidate_id": axis.candidate_id,
                "axis_id": axis.axis_id,
                "export_status": "export_or_parity_failed_repair_required",
                "export_error": f"{type(exc).__name__}: {exc}",
                "probability_parity_passed": False,
                "signal_parity_passed": False,
            }
            add_check(f"{axis.candidate_id}_export_or_parity", False, artifact["export_error"], "Export/parity blocker(내보내기/동등성 차단)를 기록한다.")
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
        target = context["target"]
        threshold = context["threshold_values"]
        for split in SPLITS:
            split_payload = context["split_payload"][split]
            start, end = split_dates(context["frame"], split)
            attempt_name = f"f69d_{safe_name(axis.axis_id, 24)}_{axis.candidate_id[-6:]}_{split}"
            extra = {
                "InpSameDirectionReentryCooldownBars": int(target.horizon_bars),
                "InpReentryCooldownBars": 0,
                "InpAtrSltpEnabled": True,
                "InpAtrStopMultiplier": float(target.sl_atr),
                "InpAtrTakeProfitMultiplier": float(target.tp_atr),
                "InpAtrMinStopPoints": float(target.min_edge_points),
                "InpAtrMinTakeProfitPoints": float(target.min_edge_points),
                "InpDecisionMode": str(threshold["decision_mode"]),
                "InpFallbackDecisionMode": str(threshold["decision_mode"]),
                "InpRuntimeVetoTapeEnabled": True,
                "InpRuntimeVetoTapePath": str(artifact["runtime_veto_tape_common_path"]),
                "InpRuntimeVetoTapeUseCommonFiles": True,
                "InpRuntimeVetoTapeDelimiter": ",",
            }
            attempt = attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=69,
                exploration_label=f"frontier69D_{axis.axis_id}_runtime_probe(F69D {axis.axis_id} 런타임 탐침)",
                attempt_name=attempt_name,
                tier=mt5.TIER_A,
                split=split,
                model_path=str(artifact["model_common_path"]),
                model_id=f"F69D_{axis.candidate_id}_{axis.axis_id}",
                model_backend="onnx",
                feature_path=str(artifact["feature_common_path"]),
                feature_count=int(context["feature_set"].columns.__len__()),
                feature_order_hash=str(context["feature_order_hash"]),
                short_threshold=float(threshold["short_threshold"]),
                long_threshold=float(threshold["long_threshold"]),
                min_margin=float(threshold["min_margin"]),
                invert_signal=False,
                from_date=start,
                to_date=end,
                primary_active_tier=mt5.TIER_A,
                attempt_role=f"f69d_{axis.role}",
                record_view_prefix=f"mt5_f69d_{safe_name(axis.axis_id, 24)}_{axis.candidate_id[-6:]}",
                max_hold_bars=int(target.horizon_bars),
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
                    "proxy_kpi": context["proxy_kpi"].get(split, context["recomputed_kpi"].get(split, {})),
                    "recomputed_proxy_kpi": context["recomputed_kpi"].get(split, {}),
                    "event_id": axis.event_id,
                    "side_policy": axis.side_policy,
                    "edge_threshold": context["edge_threshold"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            attempts.append(attempt)
    return attempts


def split_dates(frame: pd.DataFrame, split_name: str) -> tuple[str, str]:
    split = frame.loc[frame["split"].astype(str).eq(split_name)]
    if split.empty:
        raise RuntimeError(f"empty split: {split_name}")
    timestamps = pd.to_datetime(split["timestamp"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


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


def build_runtime_receipt(execution_results: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    attempts_by_name = {str(attempt["attempt_name"]): attempt for attempt in attempts}
    rows: list[dict[str, Any]] = []
    for result in execution_results:
        attempt = attempts_by_name[str(result["attempt_name"])]
        runtime = result.get("runtime_outputs", {}) if isinstance(result.get("runtime_outputs"), Mapping) else {}
        last = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
        report = result.get("strategy_tester_report", {}) if isinstance(result.get("strategy_tester_report"), Mapping) else {}
        metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
        report_rel = (report.get("html_report") or {}).get("path", "") if isinstance(report.get("html_report"), Mapping) else ""
        report_path = ROOT / str(report_rel) if report_rel else Path("")
        deal_metrics = extract_deal_metrics(report_path) if report_rel and path_exists(report_path) else empty_deal_metrics()
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
        average_win = as_float(metrics.get("average_win"))
        if average_win is None and winning_trade_count and gross_profit is not None:
            average_win = gross_profit / winning_trade_count
        average_loss = as_float(metrics.get("average_loss"))
        if average_loss is None and losing_trade_count and gross_loss is not None:
            average_loss = gross_loss / losing_trade_count
        payoff_ratio = as_float(metrics.get("payoff_ratio"))
        if payoff_ratio is None and average_win is not None and average_loss not in (None, 0):
            payoff_ratio = abs(average_win / average_loss)
        test_period = tester_period(attempt)
        proxy = attempt.get("proxy_kpi") if isinstance(attempt.get("proxy_kpi"), Mapping) else {}
        runtime_dd = as_float(metrics.get("max_drawdown_percent"))
        proxy_dd = as_float(proxy.get("drawdown_percent_on_10000"))
        row = {
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
            "deal_count": as_int(metrics.get("deal_count")) or int(deal_metrics["deal_row_count"]),
            "deal_in_count": deal_metrics["deal_in_count"],
            "deal_out_count": deal_metrics["deal_out_count"],
            "deal_minus_order_fill": (as_int(metrics.get("deal_count")) or int(deal_metrics["deal_row_count"])) - order_fill_count,
            "deal_count_equals_2x_trade": (as_int(metrics.get("deal_count")) or int(deal_metrics["deal_row_count"])) == 2 * trade_count if trade_count else False,
            "order_fill_equals_deal_count": order_fill_count == (as_int(metrics.get("deal_count")) or int(deal_metrics["deal_row_count"])),
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
            "proxy_net_profit": as_float(proxy.get("net_profit")),
            "proxy_profit_factor": as_float(proxy.get("profit_factor")),
            "proxy_trades_per_day": as_float(proxy.get("trades_per_day")),
            "proxy_dd_percent": proxy_dd,
            "dd_delta_runtime_minus_proxy": (runtime_dd - proxy_dd) if runtime_dd is not None and proxy_dd is not None else None,
            "deal_profit_sum": deal_metrics["deal_profit_sum"],
            "deal_commission_sum": deal_metrics["deal_commission_sum"],
            "deal_swap_sum": deal_metrics["deal_swap_sum"],
            "deal_cost_sum": deal_metrics["deal_cost_sum"],
            "net_reconciliation_error": reconciliation_error(metrics.get("net_profit"), deal_metrics),
            "gap_cause_summary": gap_cause_summary(attempt, metrics, last),
            "report_path": report_rel,
            "telemetry_path": runtime.get("telemetry_path", ""),
            "summary_path": runtime.get("summary_path", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append(row)
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
        return "missing_comparison(비교값 누락)"
    if abs(value) <= 1e-9:
        return f"{metric}_exact({metric} 정확)"
    if abs(value) <= 0.05:
        return f"{metric}_small_gap({metric} 작은 간극)"
    return f"{metric}_gap({metric} 간극)"


def f69_gap_row(
    receipt: Mapping[str, Any],
    gap_type: str,
    metric: str,
    proxy_value: Any,
    runtime_value: Any,
    delta: Any,
    classification: str,
    evidence: str,
) -> dict[str, Any]:
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


def build_f69_gap_classification(receipt: Mapping[str, Any]) -> list[dict[str, Any]]:
    signal_delta = receipt.get("signal_count_diff")
    feature_delta = receipt.get("feature_ready_diff")
    density_delta = numeric_delta(receipt.get("trades_per_day"), receipt.get("proxy_trades_per_day"))
    pf_delta = numeric_delta(receipt.get("profit_factor"), receipt.get("proxy_profit_factor"))
    dd_delta = numeric_delta(receipt.get("max_drawdown_percent"), receipt.get("proxy_dd_percent"))
    order_fill = as_int(receipt.get("order_fill_count")) or 0
    deal_count = as_int(receipt.get("deal_count")) or 0
    return [
        f69_gap_row(
            receipt,
            "signal_count_parity(신호 수 동등성)",
            "signal_count",
            receipt.get("expected_signal_count"),
            receipt.get("signal_count"),
            signal_delta,
            "signal_count_exact(신호 수 정확)" if signal_delta == 0 else "signal_count_gap(신호 수 간극)",
            "runtime_summary_vs_onnx_signal_parity",
        ),
        f69_gap_row(
            receipt,
            "feature_readiness(피처 준비)",
            "feature_ready_count",
            receipt.get("expected_rows"),
            receipt.get("feature_ready_count"),
            feature_delta,
            "feature_ready_exact(피처 준비 정확)" if feature_delta == 0 else "feature_ready_gap(피처 준비 간극)",
            "runtime_summary_feature_ready_count",
        ),
        f69_gap_row(
            receipt,
            "trade_density(거래 밀도)",
            "trades_per_day",
            receipt.get("proxy_trades_per_day"),
            receipt.get("trades_per_day"),
            density_delta,
            gap_class("trade_density", density_delta),
            "proxy_kpi_vs_strategy_tester_trade_count",
        ),
        f69_gap_row(
            receipt,
            "profit_factor(수익 팩터)",
            "profit_factor",
            receipt.get("proxy_profit_factor"),
            receipt.get("profit_factor"),
            pf_delta,
            gap_class("profit_factor", pf_delta),
            "proxy_kpi_vs_strategy_tester_report",
        ),
        f69_gap_row(
            receipt,
            "drawdown_percent(손실폭 퍼센트)",
            "drawdown_percent",
            receipt.get("proxy_dd_percent"),
            receipt.get("max_drawdown_percent"),
            dd_delta,
            gap_class("drawdown_percent", dd_delta),
            "proxy_dd_percent_vs_strategy_tester_dd",
        ),
        f69_gap_row(
            receipt,
            "order_fill_vs_deal_count(주문 체결 대 거래내역 수)",
            "order_fill_vs_deal_count",
            order_fill,
            deal_count,
            deal_count - order_fill,
            "deal_count_expected_round_turn(왕복 거래 내역 수 예상)" if deal_count == order_fill * 2 else "deal_count_shape_gap(거래내역 형태 간극)",
            "runtime_order_fill_count_vs_strategy_report_deal_count",
        ),
        f69_gap_row(
            receipt,
            "commission_swap(수수료/스왑)",
            "commission_swap",
            "proxy_cost_terms",
            f"commission={receipt.get('deal_commission_sum')};swap={receipt.get('deal_swap_sum')}",
            receipt.get("deal_cost_sum"),
            "cost_terms_recorded(비용 항목 기록)",
            "strategy_report_deal_table",
        ),
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
        "advice_classification": "accepted_with_guardrails(보호 장치와 함께 수용)",
    }


def experiment_design_payload() -> dict[str, Any]:
    return {
        "hypothesis": "F69 event-first proxy clues can be materialized through ONNX plus RuntimeVetoTape to reveal proxy/runtime gap causes.",
        "decision_use": "runtime_probe_observation and repair planning only",
        "comparison_baseline": "F69B/F69C proxy KPI by split and candidate; F68 runtime memories are reference only",
        "control_variables": ["US100 M5", "RuntimeProbeEA", "fixed two ExtraTrees axes", "validation/OOS split", "same deposit/leverage/modeling mode"],
        "changed_variables": ["axis role: sparse high-PF vs dense weak-PF", "feature set", "event mask"],
        "sample_scope": "Tier A validation/OOS windows from F69 target frame",
        "success_criteria": "ONNX parity and at least one MT5 tester/runtime telemetry record or exact blocker",
        "failure_criteria": "export/parity/event tape/tester/compile output blocked",
        "invalid_conditions": "candidate id mismatch, event tape timestamp mismatch, threshold mapping mismatch, missing Grok pre-review",
        "stop_conditions": "after fixed two-axis runtime probe attempt or first non-recoverable bridge blocker",
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
        "producer": "stage_pipelines/stage_frontier_69/frontier69d_event_first_onnx_runtime_probe.py",
        "experiment_design": experiment_design_payload(),
        "grok_packet": grok_identity(),
        "source_inputs": [rel(F69B_SUMMARY), rel(F69B_KPI), rel(F69C_SUMMARY), rel(f69b.MODEL_INPUT), rel(f69b.RAW_US100)],
        "axis_specs": [axis.__dict__ for axis in AXES],
        "artifact_rows": payload.get("artifact_rows", []),
        "probability_parity_path": rel(RUN_ROOT / "f69d_onnx_probability_parity.csv"),
        "signal_parity_path": rel(RUN_ROOT / "f69d_onnx_signal_parity.csv"),
        "runtime_receipt_path": rel(RUN_ROOT / "f69d_runtime_probe_receipt.csv"),
        "gap_classification_path": rel(RUN_ROOT / "f69d_gap_classification.csv"),
        "attempts": payload.get("attempts", []),
        "compile_payload": payload.get("compile_payload"),
        "execution_results": payload.get("execution_results", []),
        "strategy_tester_reports": payload.get("strategy_tester_reports", []),
        "mt5_kpi_records": payload.get("mt5_kpi_records", []),
        "summary": build_summary(payload),
        "next_action": NEXT_RUN_ID,
    }


def write_outputs(payload: Mapping[str, Any], created_at: str) -> None:
    write_json(RUN_ROOT / "frontier69D_runtime_probe_execution_result.json", payload)
    write_json(RUN_ROOT / "frontier69D_runtime_probe_summary.json", build_summary(payload))
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(payload, created_at))
    write_json(RUN_ROOT / "f69d_experiment_design.json", experiment_design_payload())
    write_json(RUN_ROOT / "f69d_grok_review_classification.json", grok_identity())
    write_csv(RUN_ROOT / "f69d_candidate_axis_materialization.csv", payload.get("artifact_rows", []))
    write_csv(RUN_ROOT / "f69d_onnx_probability_parity.csv", payload.get("probability_parity", []))
    write_csv(RUN_ROOT / "f69d_onnx_signal_parity.csv", payload.get("signal_parity", []))
    write_csv(RUN_ROOT / "f69d_local_verification.csv", payload.get("local_verification", []))
    write_csv(RUN_ROOT / "f69d_runtime_probe_receipt.csv", payload.get("runtime_receipt", []), RUNTIME_RECEIPT_COLUMNS)
    write_csv(RUN_ROOT / "f69d_gap_classification.csv", payload.get("gap_classification", []), GAP_COLUMNS)
    write_csv(REVIEWS_ROOT / "f69d_candidate_axis_materialization_review.csv", payload.get("artifact_rows", []))
    write_csv(REVIEWS_ROOT / "f69d_onnx_signal_parity_review.csv", payload.get("signal_parity", []))
    write_csv(REVIEWS_ROOT / "f69d_runtime_probe_receipt_review.csv", payload.get("runtime_receipt", []), RUNTIME_RECEIPT_COLUMNS)
    write_csv(REVIEWS_ROOT / "f69d_gap_classification_review.csv", payload.get("gap_classification", []), GAP_COLUMNS)
    write_md(REVIEWS_ROOT / "frontier69D_event_first_onnx_runtime_probe_report.md", report_lines(payload, created_at))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f69d.md", gate_audit_lines(payload, created_at))
    write_md(REVIEWS_ROOT / "f69d_pre_mt5_grok_receipt.md", grok_receipt_lines(payload, created_at))


def report_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    lines = [
        "# F69D Event-First ONNX Runtime Probe(F69D 이벤트 우선 ONNX 런타임 탐침)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "## Action And Effect(행동과 효과)",
        "",
        "Action(행동): F69B/F69C proxy(프록시)에서 exportable ExtraTrees axes(내보내기 가능한 ExtraTrees 축) 2개를 ONNX(온엑스), RuntimeVetoTape(런타임 차단 테이프), MT5 Strategy Tester(MT5 전략 테스터)로 물질화했다.",
        "",
        "Effect(효과): high-PF sparse clue(고PF 희박 단서)와 dense weak-PF clue(촘촘하지만 약한 PF 단서)를 구분해 proxy/runtime KPI gap(프록시/런타임 KPI 간극)을 관찰한다.",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- Grok advice(그록 조언): `accepted_with_guardrails(보호 장치와 함께 수용)`.",
        f"- attempts(시도 수): `{len(payload.get('attempts', []))}`.",
        "",
        "## ONNX And Signal Parity(ONNX와 신호 동등성)",
        "",
        "| axis(축) | candidate(후보) | export(내보내기) | probability parity(확률 동등성) | signal parity(신호 동등성) |",
        "|---|---|---|---|---|",
    ]
    for row in payload.get("artifact_rows", []):
        lines.append(
            f"| `{row.get('axis_id')}` | `{row.get('candidate_id')}` | `{row.get('export_status')}` | `{row.get('probability_parity_passed')}` | `{row.get('signal_parity_passed')}` |"
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
            "- research_path(연구 경로): `stage_pipelines/stage_frontier_69/frontier69d_event_first_onnx_runtime_probe.py`.",
            "- runtime_path(런타임 경로): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5` and include modules(포함 모듈).",
            "- shared_contract(공유 계약): feature order hash(피처 순서 해시), ONNX probability output(ONNX 확률 출력), event veto tape(이벤트 차단 테이프), threshold_margin(임계값 마진), ATR SL/TP(ATR 손절/익절), max hold bars(최대 보유 봉).",
            "- known_differences(알려진 차이): proxy first-hit points(프록시 선도달 포인트)와 MT5 account execution(계좌 실행)은 비용/체결/포지션 생명주기가 다르다.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return lines


def gate_audit_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    return [
        "# F69D Required Gate Coverage Audit(F69D 필수 게이트 커버리지 감사)",
        "",
        f"- updated_at_utc(갱신): `{created_at}`",
        f"- Grok pre-MT5 review(그록 MT5 전 검토): `{rel(GROK_CLEAN)}`.",
        f"- candidate axes(후보 축): `{len(payload.get('axis_contexts', []))}`.",
        f"- exported/parity passed(내보내기/동등성 통과): `{sum(1 for row in payload.get('artifact_rows', []) if row.get('export_status') == 'exported_onnx_parity_passed')}`.",
        f"- MT5 attempts(시도): `{len(payload.get('attempts', []))}`.",
        f"- runtime receipt rows(런타임 영수증 행): `{len(payload.get('runtime_receipt', []))}`.",
        f"- Strategy Tester reports(전략 테스터 보고서): `{len(payload.get('strategy_tester_reports', []))}`.",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`.",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`.",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`.",
    ]


def grok_receipt_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    return [
        "# F69D Pre-MT5 Grok Receipt(F69D MT5 전 그록 영수증)",
        "",
        f"- created_at_utc(생성): `{created_at}`",
        "- trigger_reason(트리거 이유): major validation before MT5 Runtime Probe(MT5 런타임 탐침 전 주요 검증).",
        "- review_size(검토 크기): `medium(중간)`.",
        "- direction_before_grok(그록 전 방향): two exportable ExtraTrees axes(내보내기 가능 ExtraTrees 두 축)를 ONNX/RuntimeVetoTape/MT5로 물질화.",
        f"- bounded_evidence(제한 근거): `{rel(GROK_PROMPT)}`.",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else ''}`.",
        f"- grok_output_identity(그록 출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{sha256_file(GROK_CLEAN) if path_exists(GROK_CLEAN) else ''}`.",
        "- advice_classification(조언 분류): `accepted_with_guardrails(보호 장치와 함께 수용)`.",
        "- accepted(수용): probe-not-promotion framing(탐침이지 승격 아님), HGB exclusion(HGB 제외), dual-axis gap design(이중 축 간극 설계), existing bridge reuse(기존 연결 재사용).",
        "- rejected_or_guarded(거절/보호): HGB fallback temptation(HGB 대체 유혹), shadow shortlist(숨은 후보 목록), sparse axis over-interpretation(희박 축 과해석).",
        "- needs_local_verification(로컬 검증 필요): ONNX export(내보내기), signal parity(신호 동등성), event tape alignment(이벤트 테이프 정렬), RuntimeProbeEA tester outputs(런타임 탐침 EA 테스터 출력).",
        "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        "- final_codex_direction(최종 Codex 방향): proceed with fixed two-axis runtime probe observation(고정 두 축 런타임 탐침 관찰 진행).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def update_state_and_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best_receipt = next((row for row in payload.get("runtime_receipt", []) if row.get("split") == "oos"), {})
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "event_first_onnx_runtime_probe(이벤트 우선 ONNX 런타임 탐침)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "mt5_runtime_probe_observation(MT5 런타임 탐침 관찰)",
        "tier_scope": "Tier A separate(Tier A 분리)",
        "kpi_scope": "runtime_probe_kpi_and_proxy_gap(런타임 탐침 KPI와 프록시 간극)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REVIEWS_ROOT / "frontier69D_event_first_onnx_runtime_probe_report.md"),
        "primary_kpi": f"attempts={summary['attempt_count']};completed_attempts={summary['completed_attempt_count']};exported={summary['exported_count']}",
        "guardrail_kpi": "no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve claimed",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked(차단)",
        "notes": "F69D materialized fixed exportable event-first axes; observation only.",
        "run_number": "frontier69D",
        "date": created_at[:10],
        "decision": "proceed_to_f69e_proxy_runtime_gap_analysis",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEWS_ROOT / "frontier69D_event_first_onnx_runtime_probe_report.md"),
        "trained_models": summary["axis_count"],
        "onnx_parity": summary["exported_count"],
        "best_proxy": best_receipt.get("candidate_id", ""),
        "candidate_rows": summary["axis_count"],
        "best_model_id": "shallow_extra_trees_v1",
        "best_proxy_net": fmt(best_receipt.get("proxy_net_profit")),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_ROOT / "frontier69D_runtime_probe_execution_result.json"),
        "view": "mt5_runtime_probe(MT5 런타임 탐침)",
        "tier": "Tier A separate(Tier A 분리)",
        "metric_scope": "runtime_probe_observation(런타임 탐침 관찰)",
        "net_profit": fmt(best_receipt.get("net_profit")),
        "profit_factor": fmt(best_receipt.get("profit_factor")),
        "drawdown": fmt(best_receipt.get("max_drawdown_percent")),
        "trade_count": fmt(best_receipt.get("trade_count")),
        "result_status": payload.get("status"),
        "feature_count": "",
        "lane": "runtime_probe(런타임 탐침)",
        "family": "runtime_validation(런타임 검증)",
        "primary_report": rel(REVIEWS_ROOT / "frontier69D_event_first_onnx_runtime_probe_report.md"),
        "attempt_count": summary["attempt_count"],
        "source_package_run_id": PARENT_RUN_ID,
        "row_id": f"{RUN_ID}__runtime_probe",
        "scoreboard": "runtime_probe(런타임 탐침)",
        "evidence_boundary": "runtime_probe_observation_only(런타임 탐침 관찰 전용)",
        "work_family": "runtime_validation(런타임 검증)",
        "evidence_scope": "mt5_runtime_probe(MT5 런타임 탐침)",
        "run_key": RUN_ID,
        "question": "Can F69 event-first proxy axes transfer through ONNX and RuntimeVetoTape into MT5 runtime?(F69 이벤트 우선 프록시 축이 ONNX와 런타임 차단 테이프로 MT5에 넘어가는가)",
        "next_action": NEXT_RUN_ID,
        "result_judgment": payload.get("judgment"),
        "final_decision_path": rel(REVIEWS_ROOT / "frontier69D_event_first_onnx_runtime_probe_report.md"),
        "created_at": created_at,
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f69d.md"),
        "artifact_count": len(payload.get("artifact_rows", [])),
        "created_at_utc": created_at,
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f69d.md"),
        "kpi_summary": f"attempts={summary['attempt_count']};completed={summary['completed_attempt_count']};runtime_rows={summary['runtime_receipt_rows']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "trade_density": fmt(best_receipt.get("trades_per_day")),
        "source_authority": "runtime_probe_observation_no_authority(런타임 탐침 관찰, 권위 없음)",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_runtime_probe(전선 런타임 탐침)",
        "run_type": "event_first_onnx_runtime_probe(이벤트 우선 ONNX 런타임 탐침)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "frontier69D_runtime_probe_execution_result.json"),
        "result_path": rel(REVIEWS_ROOT / "frontier69D_event_first_onnx_runtime_probe_report.md"),
        "selected_net_profit": fmt(best_receipt.get("net_profit")),
        "selected_profit_factor": fmt(best_receipt.get("profit_factor")),
        "selected_trade_density": fmt(best_receipt.get("trades_per_day")),
        "max_drawdown_percent": fmt(best_receipt.get("max_drawdown_percent")),
        "strict_joint_pass_count": 0,
    }
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", ledger_row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")
    upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", ledger_row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", ledger_row)
    update_text_state(payload, created_at, summary, best_receipt)


def update_text_state(payload: Mapping[str, Any], created_at: str, summary: Mapping[str, Any], best_receipt: Mapping[str, Any]) -> None:
    status_lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f69_runtime_probe_attempted_observation_recorded_no_authority(F69 런타임 탐침 시도/관찰 기록, 권위 없음)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        f'  - "F69D action(행동): exportable event-first axes(내보내기 가능 이벤트 우선 축) `{summary["axis_count"]}`개를 ONNX/RuntimeVetoTape/MT5(ONNX/런타임 차단 테이프/MT5)로 물질화했다."',
        f'  - "Effect(효과): attempts(시도) `{summary["attempt_count"]}`, completed_attempts(완료 시도) `{summary["completed_attempt_count"]}`, runtime_receipt_rows(런타임 영수증 행) `{summary["runtime_receipt_rows"]}`."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}`에서 proxy/runtime gap(프록시/런타임 간극)을 분석하고 repair(수리) 또는 closeout(마감)을 결정한다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(status_lines) + "\n", encoding="utf-8")
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
        "Action(행동): F69D event-first ONNX runtime probe(F69D 이벤트 우선 ONNX 런타임 탐침)를 실행했다.",
        "",
        "Effect(효과): F69B/F69C의 high-PF sparse clue(고PF 희박 단서)와 dense weak-PF clue(촘촘하지만 약한 PF 단서)를 RuntimeProbeEA(런타임 탐침 EA)에 태워 proxy/runtime gap(프록시/런타임 간극)을 관찰할 근거를 만들었다.",
        "",
        f"- status(상태): `{payload.get('status')}`.",
        f"- judgment(판정): `{payload.get('judgment')}`.",
        f"- attempts/completed(시도/완료): `{summary['attempt_count']}` / `{summary['completed_attempt_count']}`.",
        f"- runtime receipt rows(런타임 영수증 행): `{summary['runtime_receipt_rows']}`.",
        f"- representative OOS net/PF/DD/trades_day(대표 표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(best_receipt.get('net_profit'))}` / `{fmt(best_receipt.get('profit_factor'))}` / `{fmt(best_receipt.get('max_drawdown_percent'))}` / `{fmt(best_receipt.get('trades_per_day'))}`.",
        "",
        "## Key Artifacts(핵심 산출물)",
        "",
        f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier69D_event_first_onnx_runtime_probe_report.md`",
        f"- runtime receipt(런타임 영수증): `stages/{STAGE_ID}/03_reviews/f69d_runtime_probe_receipt_review.csv`",
        f"- gap classification(간극 분류): `stages/{STAGE_ID}/03_reviews/f69d_gap_classification_review.csv`",
        f"- Grok receipt(그록 영수증): `stages/{STAGE_ID}/03_reviews/f69d_pre_mt5_grok_receipt.md`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", current_lines)
    selection_lines = [
        "# F69 Selection Status(F69 선택 상태)",
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
        f"- completed_action(완료 행동): `{RUN_ID}` event-first ONNX runtime probe(이벤트 우선 ONNX 런타임 탐침).",
        f"- attempts/completed(시도/완료): `{summary['attempt_count']}` / `{summary['completed_attempt_count']}`.",
        f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier69D_event_first_onnx_runtime_probe_report.md`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}`.",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(STAGE_ROOT / "04_selected" / "selection_status.md", selection_lines)
    append_once(
        ROOT / "docs/registers/idea_registry.md",
        f"{RUN_ID} executed",
        f"""### {RUN_ID}

- {RUN_ID} executed(실행): F69 exportable event-first axes(F69 내보내기 가능 이벤트 우선 축)를 ONNX/RuntimeVetoTape/MT5(ONNX/런타임 차단 테이프/MT5)로 물질화했다. Status(상태): `{payload.get('status')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
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
        "judgment": "mt5_runtime_probe_materialized_pending_execution_no_authority(MT5 런타임 탐침 물질화, 실행 대기, 권위 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
        "grok_packet": grok_identity(),
        "axis_contexts": [
            {
                "axis": context["axis"].__dict__,
                "feature_order_hash": context["feature_order_hash"],
                "edge_threshold": context["edge_threshold"],
                "candidate_id_match": context["candidate_id_match"],
                "summary_reference": context["summary_reference"],
                "threshold_values": context["threshold_values"],
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
    gap_rows = [row for receipt in receipt_rows for row in build_f69_gap_classification(receipt)]
    execution_completed = bool(execution_results) and any(row.get("status") == "completed" for row in execution_results)
    report_completed = bool(kpi_records)
    payload.update(
        {
            "status": STATUS_COMPLETED if execution_completed and report_completed else STATUS_BLOCKED,
            "judgment": (
                "runtime_probe_observation_recorded_no_authority(MT5 런타임 탐침 관찰 기록, 권위 없음)"
                if execution_completed and report_completed
                else "runtime_probe_attempt_blocked_repair_required_no_authority(MT5 런타임 탐침 시도 차단, 수리 필요, 권위 없음)"
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
                    "completed_attempt_count": sum(1 for row in execution_results if row.get("status") == "completed"),
                    "report_count": len(kpi_records),
                    "runtime_receipt_rows": len(receipt_rows),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
