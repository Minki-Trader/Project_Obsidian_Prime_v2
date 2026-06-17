from __future__ import annotations

import argparse
import csv
import json
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
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage_frontier_71 import frontier71b_economics_native_proxy_scout as f71b
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
)


STAGE_ID = f71b.STAGE_ID
RUN_ID = "frontier71D_mt5_runtime_probe_economics_native_scout_v1"
PARENT_RUN_ID = "frontier71D_pre_mt5_grok_runtime_probe_economics_native_scout_v1"
SOURCE_PROXY_RUN_ID = f71b.RUN_ID
NEXT_RUN_ID = "frontier71E_proxy_runtime_gap_analysis_and_repair_decision_v1"
CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = f71b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f71b.REVIEWS_ROOT
MODEL_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "features"
VETO_ROOT = RUN_ROOT / "runtime_veto_tapes"
MT5_ROOT = RUN_ROOT / "mt5"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier71D_mt5_runtime_probe_economics_native_scout"

F71B_CANDIDATES = STAGE_ROOT / "02_runs" / SOURCE_PROXY_RUN_ID / "f71b_candidate_summary.csv"
GROK_PACKET_ROOT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f71_pre_mt5_runtime_probe_economics_native_scout"
GROK_PROMPT = GROK_PACKET_ROOT / "prompts/f71_pre_mt5_runtime_probe_economics_native_scout_prompt.md"
GROK_CLEAN = GROK_PACKET_ROOT / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET_ROOT / "outputs/metadata.json"

PRIMARY_CANDIDATE_ID = "f71b_1e511d3db9c3"

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
    threshold: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F71D economics-native scout MT5 runtime probe.")
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
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: json_ready(row.get(name, "")) for name in fieldnames})


def as_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if np.isfinite(number) else None


def as_int(value: Any) -> int | None:
    number = as_float(value)
    return int(round(number)) if number is not None else None


def ratio(numerator: Any, denominator: Any) -> float | None:
    num = as_float(numerator)
    den = as_float(denominator)
    if num is None or den in (None, 0):
        return None
    return num / den


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_ROOT, FEATURE_ROOT, VETO_ROOT, MT5_ROOT, MT5_ROOT / "reports", REVIEWS_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def candidate_axis() -> AxisSpec:
    rows = pd.read_csv(io_path(F71B_CANDIDATES))
    source = rows.loc[rows["candidate_id"].astype(str).eq(PRIMARY_CANDIDATE_ID)]
    if source.empty:
        raise RuntimeError(f"missing primary candidate: {PRIMARY_CANDIDATE_ID}")
    row = source.iloc[0].to_dict()
    return AxisSpec(
        axis_id="f71b_fracture_pf_dd_primary",
        candidate_id=PRIMARY_CANDIDATE_ID,
        role="primary_grok_accepted_fracture_pf_dd_scout",
        label_id=str(row["label_id"]),
        feature_set_id=str(row["feature_set_id"]),
        model_id=str(row["model_id"]),
        selection_id=str(row["selection_id"]),
        mask_name=str(row["mask_name"]),
        threshold_quantile=float(row["threshold_quantile"]),
        threshold=float(row["threshold"]),
    )


def onnx_probabilities(onnx_path: Path, values: np.ndarray) -> np.ndarray:
    import onnxruntime as ort

    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: values.astype("float32")})
    for output in outputs:
        arr = np.asarray(output)
        if arr.ndim == 2 and arr.shape[1] == 3:
            return arr.astype("float64")
    raise RuntimeError("ONNX probability output not found(ONNX 확률 출력 없음)")


def side_score_from_probability(proba: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    short_p = proba[:, 0]
    flat_p = proba[:, 1]
    long_p = proba[:, 2]
    side = np.where(long_p >= short_p, 1, -1)
    score = np.maximum(long_p, short_p) - 0.55 * flat_p + 0.35 * np.abs(long_p - short_p)
    return side.astype(int), score.astype(float)


def split_dates(frame: pd.DataFrame, split_name: str) -> tuple[str, str]:
    subset = frame.loc[frame["split"].astype(str).eq(split_name)]
    timestamps = pd.to_datetime(subset["timestamp"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def selected_entry_tape(frame: pd.DataFrame, selected: np.ndarray, event_mask: np.ndarray, path: Path) -> dict[str, Any]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    payload = pd.DataFrame(
        {
            "bar_time_server": timestamps.dt.strftime("%Y.%m.%d %H:%M:%S"),
            "timestamp_utc": timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "entry_veto": np.where(selected, 0, 1).astype(int),
            "selected_entry": selected.astype(int),
            "event_active": event_mask.astype(int),
            "split": frame["split"].astype(str).to_numpy(),
        }
    )
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    payload.to_csv(io_path(path), index=False, encoding="utf-8", lineterminator="\n")
    return {
        "path": rel(path),
        "sha256": mt5.sha256_file(path),
        "rows": int(len(payload)),
        "selected_entry_rows": int(selected.sum()),
        "event_active_rows": int(event_mask.sum()),
    }


def build_context() -> dict[str, Any]:
    axis = candidate_axis()
    frame = f71b.load_frame()
    label_spec = next(item for item in f71b.label_specs() if item.label_id == axis.label_id)
    feature_set = next(item for item in f71b.feature_sets(frame) if item.feature_set_id == axis.feature_set_id)
    model_spec = next(item for item in f71b.model_specs() if item.model_id == axis.model_id)
    label, long_profit, short_profit, best_utility = f71b.build_label(frame, label_spec)
    train_mask = f71b.split_mask(frame, "train")
    weights = f71b.sample_weight(frame, label, best_utility)[train_mask]
    model = model_spec.build()
    f71b.fit_model(model, frame.loc[train_mask, feature_set.columns], label.loc[train_mask], weights)
    side, score = f71b.side_scores(model, frame.loc[:, feature_set.columns])
    selection = f71b.SelectionSpec(axis.selection_id, axis.mask_name, axis.threshold_quantile)
    selected = f71b.selected_mask_from_threshold(frame, score, selection, label_spec.horizon_bars, axis.threshold)
    split_rows = f71b.evaluate_splits(frame, selected, side, long_profit, short_profit)
    by_split = {row["split"]: row for row in split_rows}
    return {
        "axis": axis,
        "frame": frame,
        "label_spec": label_spec,
        "feature_set": feature_set,
        "feature_columns": list(feature_set.columns),
        "feature_order_hash": ordered_hash(feature_set.columns),
        "model_spec": model_spec,
        "model": model,
        "side": side,
        "score": score,
        "selected": selected,
        "event_mask": f71b.mask_for(frame, axis.mask_name),
        "long_profit": long_profit,
        "short_profit": short_profit,
        "proxy_kpi_by_split": by_split,
    }


def materialize_context(context: Mapping[str, Any], common_files_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    axis: AxisSpec = context["axis"]
    feature_columns = list(context["feature_columns"])
    model = context["model"]
    model_path = MODEL_ROOT / f"{axis.candidate_id}.joblib"
    onnx_path = MODEL_ROOT / f"{axis.candidate_id}.onnx"
    feature_order_path = MODEL_ROOT / f"{axis.candidate_id}_feature_order.txt"
    feature_csv_path = FEATURE_ROOT / f"{axis.candidate_id}_features.csv"
    veto_path = VETO_ROOT / f"{axis.candidate_id}_selected_entry_runtime_veto_tape.csv"
    io_path(feature_order_path).write_text("\n".join(feature_columns) + "\n", encoding="utf-8")
    joblib.dump(model, io_path(model_path))
    onnx_export = export_sklearn_to_onnx_zipmap_disabled(model, onnx_path, feature_count=len(feature_columns), target_opset=12, drop_label_output=True)
    feature_meta = mt5.export_mt5_feature_matrix_csv(context["frame"], feature_columns, feature_csv_path, metadata_columns=("split",))
    veto_meta = selected_entry_tape(context["frame"], context["selected"], context["event_mask"], veto_path)
    probability_rows, signal_rows = parity_rows(context, onnx_path)
    probability_ok = all(row.get("passed") for row in probability_rows)
    signal_ok = all(row.get("passed") for row in signal_rows)
    artifact = {
        "candidate_id": axis.candidate_id,
        "axis_id": axis.axis_id,
        "role": axis.role,
        "model_path": rel(model_path),
        "model_sha256": mt5.sha256_file(model_path),
        "onnx_path": rel(onnx_path),
        "onnx_sha256": mt5.sha256_file(onnx_path),
        "feature_order_path": rel(feature_order_path),
        "feature_order_sha256": mt5.sha256_file(feature_order_path),
        "feature_csv_path": rel(feature_csv_path),
        "feature_csv_sha256": mt5.sha256_file(feature_csv_path),
        "runtime_veto_tape_path": rel(veto_path),
        "runtime_veto_tape_sha256": mt5.sha256_file(veto_path),
        "onnx_export": onnx_export,
        "feature_csv": feature_meta,
        "runtime_veto_tape": veto_meta,
        "probability_parity_passed": probability_ok,
        "signal_parity_passed": signal_ok,
        "feature_order_hash": context["feature_order_hash"],
        "threshold": axis.threshold,
    }
    if probability_ok and signal_ok:
        for local_path, common_path_key, copy_key in (
            (onnx_path, "model_common_path", "model_common_copy"),
            (feature_csv_path, "feature_common_path", "feature_common_copy"),
            (veto_path, "runtime_veto_tape_common_path", "runtime_veto_tape_common_copy"),
        ):
            common_path = f"{COMMON_RUN_ROOT}/{local_path.parent.name}/{local_path.name}"
            artifact[common_path_key] = common_path
            artifact[copy_key] = mt5.copy_to_common_files(common_files_root, local_path, common_path)
    artifact["export_status"] = "exported_selected_entry_tape_parity_passed" if probability_ok and signal_ok else "exported_selected_entry_tape_parity_failed"
    return artifact, probability_rows, signal_rows


def parity_rows(context: Mapping[str, Any], onnx_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    axis: AxisSpec = context["axis"]
    model = context["model"]
    feature_columns = list(context["feature_columns"])
    probability_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        subset = context["frame"].loc[context["frame"]["split"].astype(str).eq(split)]
        idx = subset.index.to_numpy()
        values = subset.loc[:, feature_columns].to_numpy(dtype="float64")
        sample = values[: min(len(values), 2048)]
        probability = check_onnxruntime_probability_parity(model, onnx_path, sample, class_order=(-1, 0, 1), tolerance=1e-5)
        probability_rows.append({"candidate_id": axis.candidate_id, "axis_id": axis.axis_id, "split": split, **probability})
        sklearn_proba = ordered_sklearn_probabilities(model, values, class_order=(-1, 0, 1))
        onnx_proba = onnx_probabilities(onnx_path, values)
        sk_side, sk_score = side_score_from_probability(sklearn_proba)
        onnx_side, onnx_score = side_score_from_probability(onnx_proba)
        selected = context["selected"][idx]
        sk_signal = selected & (sk_score >= axis.threshold)
        onnx_signal = selected & (onnx_score >= axis.threshold)
        signal_rows.append(
            {
                "candidate_id": axis.candidate_id,
                "axis_id": axis.axis_id,
                "split": split,
                "rows": int(len(subset)),
                "selected_entry_rows": int(selected.sum()),
                "sklearn_signal_count": int(sk_signal.sum()),
                "onnx_signal_count": int(onnx_signal.sum()),
                "signal_count_diff": int(onnx_signal.sum() - sk_signal.sum()),
                "signal_mismatch_count": int((onnx_signal != sk_signal).sum()),
                "side_mismatch_on_signal_count": int(((onnx_side != sk_side) & (onnx_signal | sk_signal)).sum()),
                "max_score_abs_diff": float(np.max(np.abs(onnx_score - sk_score))) if len(onnx_score) else 0.0,
                "threshold": axis.threshold,
                "passed": bool(int((onnx_signal != sk_signal).sum()) == 0 and int(((onnx_side != sk_side) & (onnx_signal | sk_signal)).sum()) == 0),
            }
        )
    return probability_rows, signal_rows


def build_attempts(context: Mapping[str, Any], artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    axis: AxisSpec = context["axis"]
    label_spec = context["label_spec"]
    attempts: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        from_date, to_date = split_dates(context["frame"], split)
        split_mask = context["frame"]["split"].astype(str).eq(split).to_numpy(dtype=bool)
        expected_rows = int(split_mask.sum())
        expected_selected = int((context["selected"] & split_mask).sum())
        attempt_name = f"f71d_{axis.axis_id}_{split}"
        extra = {
            "InpSameDirectionReentryCooldownBars": int(label_spec.horizon_bars),
            "InpReentryCooldownBars": 0,
            "InpAtrSltpEnabled": True,
            "InpAtrStopMultiplier": float(label_spec.sl_atr),
            "InpAtrTakeProfitMultiplier": float(label_spec.tp_atr),
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
            stage_number=71,
            exploration_label=f"frontier71D_{axis.axis_id}_runtime_probe",
            attempt_name=attempt_name,
            tier=mt5.TIER_A,
            split=split,
            model_path=str(artifact["model_common_path"]),
            model_id=f"F71D_{axis.candidate_id}_{axis.axis_id}",
            model_backend="onnx",
            feature_path=str(artifact["feature_common_path"]),
            feature_count=len(context["feature_columns"]),
            feature_order_hash=str(context["feature_order_hash"]),
            short_threshold=0.0,
            long_threshold=0.0,
            min_margin=float(axis.threshold),
            invert_signal=False,
            from_date=from_date,
            to_date=to_date,
            primary_active_tier=mt5.TIER_A,
            attempt_role=f"f71d_{axis.role}",
            record_view_prefix=f"mt5_f71d_{axis.axis_id}",
            max_hold_bars=int(label_spec.horizon_bars),
            common_root=COMMON_RUN_ROOT,
            close_on_flat_signal=False,
            reverse_on_opposite_signal=True,
            close_only_on_opposite_signal=False,
            extra_set_values=extra,
        )
        proxy = context["proxy_kpi_by_split"].get(split, {})
        attempt.update(
            {
                "candidate_id": axis.candidate_id,
                "axis_id": axis.axis_id,
                "axis_role": axis.role,
                "expected_rows": expected_rows,
                "expected_signal_count": expected_selected,
                "expected_selected_trade_count": expected_selected,
                "proxy_kpi": proxy,
                "label_id": axis.label_id,
                "feature_set_id": axis.feature_set_id,
                "model_id": axis.model_id,
                "selection_id": axis.selection_id,
                "mask_name": "selected_entry_only",
                "threshold": axis.threshold,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempts.append(attempt)
    return attempts


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
        portable_payload.update({"copied": True, "portable_ea_ex5_exists_after": path_exists(PORTABLE_EA_BINARY), "portable_ea_sha256": mt5.sha256_file(PORTABLE_EA_BINARY)})
    return {"compile": compile_payload, "portable_ea": portable_payload}


def can_run_terminal(compile_payload: Mapping[str, Any]) -> bool:
    return ((compile_payload.get("compile") or {}).get("status") == "completed") or path_exists(PORTABLE_EA_BINARY)


def clear_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        target = common_files_root / Path(str(attempt.get(key, "")))
        if path_exists(target):
            io_path(target).unlink()


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
            runtime_outputs = mt5.wait_for_mt5_runtime_outputs(Path(args.common_files_root), attempt, timeout_seconds=int(args.wait_timeout_seconds), poll_seconds=2.0)
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
        proxy_dd = as_float(proxy.get("max_drawdown_percent"))
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
                "proxy_net_profit": as_float(proxy.get("net_profit")),
                "proxy_profit_factor": as_float(proxy.get("profit_factor")),
                "proxy_trades_per_day": as_float(proxy.get("trades_day")),
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


def gap_rows(receipts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for receipt in receipts:
        for metric, proxy_key, runtime_key in (
            ("net_profit", "proxy_net_profit", "net_profit"),
            ("profit_factor", "proxy_profit_factor", "profit_factor"),
            ("trades_per_day", "proxy_trades_per_day", "trades_per_day"),
            ("drawdown_percent", "proxy_dd_percent", "max_drawdown_percent"),
        ):
            proxy_value = receipt.get(proxy_key)
            runtime_value = receipt.get(runtime_key)
            proxy_float = as_float(proxy_value)
            runtime_float = as_float(runtime_value)
            delta = runtime_float - proxy_float if proxy_float is not None and runtime_float is not None else None
            classification = f"{metric}_missing" if delta is None else (f"{metric}_small_gap" if abs(delta) <= 0.05 else f"{metric}_gap")
            rows.append(
                {
                    "run_id": RUN_ID,
                    "attempt_name": receipt.get("attempt_name"),
                    "candidate_id": receipt.get("candidate_id"),
                    "axis_id": receipt.get("axis_id"),
                    "split": receipt.get("split"),
                    "gap_type": receipt.get("gap_cause_summary"),
                    "metric": metric,
                    "proxy_value": proxy_value,
                    "runtime_value": runtime_value,
                    "delta": delta,
                    "classification": classification,
                    "evidence": receipt.get("report_path") or receipt.get("summary_path"),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipts = list(payload.get("runtime_receipt") or [])
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "candidate_id": PRIMARY_CANDIDATE_ID,
        "attempt_count": len(payload.get("attempts", [])),
        "completed_attempt_count": sum(1 for row in receipts if row.get("tester_status") == "completed"),
        "runtime_receipt_rows": len(receipts),
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    lines = [
        "# Frontier71D MT5 Runtime Probe(F71D MT5 런타임 탐침)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- candidate(후보): `{PRIMARY_CANDIDATE_ID}`",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Grok Review(그록 검토)",
        "",
        f"- prompt(프롬프트): `{rel(GROK_PROMPT)}`",
        f"- output(출력): `{rel(GROK_CLEAN)}`",
        "- classification(분류): `accepted_primary_f71b_probe_rejected_default_repair_again_needs_local_verification_for_materialization(1차 F71B 탐침 수용, 기본 추가수리 거절, 물질화 로컬 검증 필요)`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        "| split(분할) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | expected signals(예상 신호) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload.get("runtime_receipt", []):
        lines.append(
            "| `{split}` | `{net}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{expected}` | `{sig}` | `{feat}` | `{gap}` |".format(
                split=row.get("split"),
                net=f71b.fmt(row.get("net_profit")),
                pf=f71b.fmt(row.get("profit_factor")),
                dd=f71b.fmt(row.get("max_drawdown_percent")),
                trades=f71b.fmt(row.get("trade_count")),
                tpd=f71b.fmt(row.get("trades_per_day")),
                expected=f71b.fmt(row.get("expected_signal_count")),
                sig=f71b.fmt(row.get("signal_count_diff")),
                feat=f71b.fmt(row.get("feature_ready_diff")),
                gap=row.get("gap_cause_summary"),
            )
        )
    lines.extend(
        [
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{NEXT_RUN_ID}`",
        ]
    )
    return lines


def grok_receipt_lines(created_at: str) -> list[str]:
    return [
        "# F71D Pre-MT5 Grok Receipt(F71D MT5 전 그록 영수증)",
        "",
        f"- created_at_utc(생성): `{created_at}`",
        "- trigger_reason(트리거 이유): MT5 Runtime Probe(MT5 런타임 탐침) 전 target selection(대상 선택).",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{mt5.sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else ''}`.",
        f"- grok_output_identity(그록 출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{mt5.sha256_file(GROK_CLEAN) if path_exists(GROK_CLEAN) else ''}`.",
        "- advice_classification(조언 분류): `accepted_primary_f71b_probe; rejected_default_repair_again; needs_local_verification_materialization(1차 F71B 탐침 수용; 기본 추가수리 거절; 물질화 로컬 검증 필요)`.",
        f"- final_codex_direction(최종 Codex 방향): `{PRIMARY_CANDIDATE_ID}` MT5 Runtime Probe(MT5 런타임 탐침).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def gate_audit_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    return [
        "# Required Gate Coverage Audit F71D(필수 게이트 커버리지 감사 F71D)",
        "",
        f"- updated_at_utc(갱신): `{created_at}`",
        f"- Grok pre-MT5 review(그록 MT5 전 검토): `{rel(GROK_CLEAN)}`.",
        f"- ONNX/signal parity rows(온엑스/신호 동등성 행): `{len(payload.get('signal_parity', []))}`.",
        f"- MT5 attempts(MT5 시도): `{summary['attempt_count']}`.",
        f"- completed attempts(완료 시도): `{summary['completed_attempt_count']}`.",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`.",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`.",
    ]


def write_outputs(payload: Mapping[str, Any], created_at: str) -> None:
    write_json(RUN_ROOT / "frontier71D_runtime_probe_execution_result.json", payload)
    write_json(RUN_ROOT / "frontier71D_runtime_probe_summary.json", build_summary(payload))
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(payload, created_at))
    write_csv(RUN_ROOT / "f71d_candidate_axis_materialization.csv", payload.get("artifact_rows", []))
    write_csv(RUN_ROOT / "f71d_onnx_probability_parity.csv", payload.get("probability_parity", []))
    write_csv(RUN_ROOT / "f71d_onnx_signal_parity.csv", payload.get("signal_parity", []))
    write_csv(RUN_ROOT / "f71d_runtime_probe_receipt.csv", payload.get("runtime_receipt", []), RUNTIME_RECEIPT_COLUMNS)
    write_csv(RUN_ROOT / "f71d_gap_classification.csv", payload.get("gap_classification", []), GAP_COLUMNS)
    write_csv(REVIEWS_ROOT / "f71d_candidate_axis_materialization_review.csv", payload.get("artifact_rows", []))
    write_csv(REVIEWS_ROOT / "f71d_onnx_probability_parity_review.csv", payload.get("probability_parity", []))
    write_csv(REVIEWS_ROOT / "f71d_onnx_signal_parity_review.csv", payload.get("signal_parity", []))
    write_csv(REVIEWS_ROOT / "f71d_runtime_probe_receipt_review.csv", payload.get("runtime_receipt", []), RUNTIME_RECEIPT_COLUMNS)
    write_csv(REVIEWS_ROOT / "f71d_gap_classification_review.csv", payload.get("gap_classification", []), GAP_COLUMNS)
    write_md(REVIEWS_ROOT / "frontier71D_mt5_runtime_probe_report.md", report_lines(payload, created_at))
    write_md(REVIEWS_ROOT / "f71d_pre_mt5_grok_receipt.md", grok_receipt_lines(created_at))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f71d.md", gate_audit_lines(payload, created_at))


def run_manifest(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "created_at_utc": created_at,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "producer": "stage_pipelines/stage_frontier_71/frontier71d_mt5_runtime_probe_economics_native_scout.py",
        "grok_packet": {"prompt": rel(GROK_PROMPT), "clean_output": rel(GROK_CLEAN), "metadata": rel(GROK_METADATA)},
        "candidate_id": PRIMARY_CANDIDATE_ID,
        "artifact_rows": payload.get("artifact_rows", []),
        "attempts": payload.get("attempts", []),
        "summary": build_summary(payload),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def best_receipt(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    receipts = [row for row in payload.get("runtime_receipt", []) if row.get("split") == "oos"]
    if not receipts:
        receipts = list(payload.get("runtime_receipt", []))
    return receipts[0] if receipts else {}


def registry_row(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    summary = build_summary(payload)
    best = best_receipt(payload)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_runtime_probe(MT5 런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REVIEWS_ROOT / "frontier71D_mt5_runtime_probe_report.md"),
        "notes": f"candidate={PRIMARY_CANDIDATE_ID};attempts={summary['attempt_count']};completed={summary['completed_attempt_count']}",
        "family": "runtime_probe(런타임 탐침)",
        "primary_report": rel(REVIEWS_ROOT / "frontier71D_mt5_runtime_probe_report.md"),
        "run_number": "frontier71D",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload.get("runtime_receipt", [])),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEWS_ROOT / "frontier71D_mt5_runtime_probe_report.md"),
        "runtime_completed_rows": summary["completed_attempt_count"],
        "matched_rows": "",
        "mismatch_rows": "",
        "best_net_profit": best.get("net_profit"),
        "best_profit_factor": best.get("profit_factor"),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_ROOT / "run_manifest.json"),
        "candidate_model_id": PRIMARY_CANDIDATE_ID,
        "net_profit": best.get("net_profit"),
        "profit_factor": best.get("profit_factor"),
        "drawdown": best.get("max_drawdown_percent"),
        "trade_count": best.get("trade_count"),
        "result_status": payload.get("status"),
        "view": "MT5 Runtime Probe(MT5 런타임 탐침)",
        "tier": "Tier A",
        "metric_scope": "runtime_probe_kpi(런타임 탐침 KPI)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked(차단)",
        "result_judgment": payload.get("judgment"),
        "final_decision_path": rel(REVIEWS_ROOT / "frontier71D_mt5_runtime_probe_report.md"),
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f71d.md"),
        "created_at": created_at,
        "ledger_row_id": f"{RUN_ID}__runtime_probe",
        "subrun_id": "mt5_runtime_probe(MT5 런타임 탐침)",
        "record_view": "MT5 Runtime Probe(MT5 런타임 탐침)",
        "tier_scope": "Tier A separate(Tier A 분리)",
        "kpi_scope": "runtime_probe_kpi(런타임 탐침 KPI)",
        "primary_kpi": f"completed={summary['completed_attempt_count']};best_pf={f71b.fmt(best.get('profit_factor'))};best_dd={f71b.fmt(best.get('max_drawdown_percent'))}",
        "guardrail_kpi": f"signal_diff={f71b.fmt(best.get('signal_count_diff'))};feature_diff={f71b.fmt(best.get('feature_ready_diff'))}",
        "row_id": f"{RUN_ID}__runtime_probe",
        "evidence_boundary": "runtime_probe_observation_no_authority(런타임 탐침 관찰, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Does F71B economics-native scout transfer to MT5 runtime?(F71B 경제성 탐색 단서가 MT5 런타임으로 전이되나?)",
        "artifact_count": 12,
        "created_at_utc": created_at,
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f71d.md"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_runtime_probe(전선 런타임 탐침)",
        "run_type": "mt5_runtime_probe(MT5 런타임 탐침)",
        "input_run_id": SOURCE_PROXY_RUN_ID,
        "output_path": rel(RUN_ROOT),
        "result_path": rel(REVIEWS_ROOT / "frontier71D_mt5_runtime_probe_report.md"),
        "goal_achieve": "not_claimed",
        "source_authority": "F71B proxy scout + F71D Grok review(F71B 프록시 탐색 + F71D 그록 검토)",
        "trade_density": best.get("trades_per_day"),
        "max_drawdown_percent": best.get("max_drawdown_percent"),
    }


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    row = registry_row(payload, created_at)
    f71b.upsert_ledger(f71b.RUN_REGISTRY, "run_id", row)
    f71b.upsert_ledger(f71b.ALPHA_LEDGER, "ledger_row_id", row)
    f71b.upsert_ledger(f71b.STAGE_LEDGER, "ledger_row_id", row, source_header=f71b.ALPHA_LEDGER)


def append_idea(payload: Mapping[str, Any]) -> None:
    marker = "<!-- frontier71D_mt5_runtime_probe_economics_native_scout_v1 -->"
    best = best_receipt(payload)
    block = f"""
{marker}
- `{RUN_ID}` executed MT5 Runtime Probe(MT5 런타임 탐침) for `{PRIMARY_CANDIDATE_ID}` after Grok review(그록 검토 후). Result(결과): `{payload.get('judgment')}`. Best runtime(최선 런타임) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{f71b.fmt(best.get('net_profit'))}/{f71b.fmt(best.get('profit_factor'))}/{f71b.fmt(best.get('max_drawdown_percent'))}/{f71b.fmt(best.get('trades_per_day'))}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier71D_mt5_runtime_probe_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    f71b.append_once(f71b.IDEA_REGISTRY, marker, block)


def write_state(payload: Mapping[str, Any], created_at: str) -> None:
    best = best_receipt(payload)
    state_lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_retrospective_completed",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        '  - "Action(행동): F71D MT5 Runtime Probe(MT5 런타임 탐침)를 실행했다."',
        f'  - "Effect(효과): runtime best PF={f71b.fmt(best.get("profit_factor"))}, DD={f71b.fmt(best.get("max_drawdown_percent"))}, trades/day={f71b.fmt(best.get("trades_per_day"))}로 F71E gap analysis(간극 분석)를 진행한다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(f71b.WORKSPACE_STATE).write_text("\n".join(state_lines) + "\n", encoding="utf-8-sig")
    lines = [
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
        "Action(행동): F71D MT5 Runtime Probe(MT5 런타임 탐침)를 실행했다.",
        "",
        f"Effect(효과): proxy/runtime gap analysis(프록시/런타임 간극 분석)를 `{NEXT_RUN_ID}`에서 진행할 수 있다.",
        "",
        f"- candidate(후보): `{PRIMARY_CANDIDATE_ID}`.",
        f"- best runtime net/PF/DD/trades_day(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{f71b.fmt(best.get('net_profit'))}` / `{f71b.fmt(best.get('profit_factor'))}` / `{f71b.fmt(best.get('max_drawdown_percent'))}` / `{f71b.fmt(best.get('trades_per_day'))}`.",
        f"- next action(다음 행동): `{NEXT_RUN_ID}`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(f71b.CURRENT_WORKING_STATE, lines)


def main() -> int:
    args = parse_args()
    ensure_dirs()
    created_at = utc_now()
    if not path_exists(GROK_CLEAN) or not path_exists(GROK_METADATA):
        raise RuntimeError("missing pre-MT5 Grok review(F71D MT5 전 그록 검토 누락)")
    context = build_context()
    artifact, probability_rows, signal_rows = materialize_context(context, Path(args.common_files_root))
    attempts = build_attempts(context, artifact) if artifact.get("export_status") == "exported_selected_entry_tape_parity_passed" else []
    compile_payload = compile_runtime_ea(Path(args.metaeditor_path))
    execution_results: list[dict[str, Any]] = []
    if args.execute and not args.materialize_only and attempts:
        execution_results = execute_attempts(args, attempts, compile_payload)
        reports = mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=Path(args.terminal_data_root),
            run_output_root=RUN_ROOT,
            attempts=attempts,
            run_id=RUN_ID,
        )
        mt5.attach_mt5_report_metrics(execution_results, reports)
    runtime_receipt = build_runtime_receipt(execution_results, attempts) if execution_results else []
    gaps = gap_rows(runtime_receipt)
    completed = sum(1 for row in runtime_receipt if row.get("tester_status") == "completed")
    if args.execute and completed:
        status = "completed_mt5_runtime_probe_observation_no_authority"
        judgment = "runtime_probe_completed_gap_analysis_required_no_authority"
    elif args.execute:
        status = "blocked_mt5_runtime_probe_attempted_no_authority"
        judgment = "runtime_probe_blocked_repair_required_no_authority"
    else:
        status = "materialized_pending_mt5_runtime_probe_execution_no_authority"
        judgment = "runtime_probe_materialized_pending_execution_no_authority"
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": created_at,
        "artifact_rows": [artifact],
        "probability_parity": probability_rows,
        "signal_parity": signal_rows,
        "attempts": attempts,
        "compile_payload": compile_payload,
        "execution_results": execution_results,
        "runtime_receipt": runtime_receipt,
        "gap_classification": gaps,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_outputs(payload, created_at)
    update_ledgers(payload, created_at)
    append_idea(payload)
    write_state(payload, created_at)
    print(json.dumps(json_ready(build_summary(payload)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
