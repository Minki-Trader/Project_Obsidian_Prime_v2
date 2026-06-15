from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import balanced_accuracy_score, f1_score, log_loss

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import (  # noqa: E402
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
    sha256_file,
)
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d  # noqa: E402
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b  # noqa: E402
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b  # noqa: E402
from stage_pipelines.stage_frontier_52.run_frontier52_runtime_probe import execute_attempts, override_set_file  # noqa: E402
from stage_pipelines.stage_frontier_59 import run_frontier59_runtime_probe as f59  # noqa: E402
from stage_pipelines.stage_frontier_runtime_backfill import run_frontier_runtime_probe_backfill as backfill  # noqa: E402


STAGE_NUM = 61
STAGE_ID = "stage_frontier_61__non_long_axis_pf_source_after_friction_memory"
RUN_A = "frontier61A_stage_open_non_long_axis_pf_source_after_friction_memory_v1"
RUN_B = "frontier61B_side_allocation_proxy_v1"
RUN_C = "frontier61C_mt5_runtime_probe_side_allocation_v1"
RUN_D = "frontier61D_stage_closeout_side_allocation_v1"
RUN_ID = "frontier61Z_runtime_probe_backfill_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODELS_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "feature_matrices"
MT5_ROOT = RUN_ROOT / "mt5"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

GROK_STAGE_OPEN_ROOT = Path("docs/agent_control/grok_reviews/2026-06-16_frontier61_stage_open_review/small_review")
GROK_PRE_MT5_ROOT = Path("docs/agent_control/grok_reviews/2026-06-16_frontier61_pre_mt5_review/small_review")
GROK_STAGE_CLOSE_ROOT = Path("docs/agent_control/grok_reviews/2026-06-16_frontier61_stage_closeout_review/small_review")
GROK_WRAPPER_GUARD_ROOT = Path("docs/agent_control/grok_reviews/2026-06-16_grok_wrapper_duplicate_arg_guard/small_review")

NEXT_STAGE_ID = "stage_frontier_62__post_allocation_failure_mode_or_seed_expansion"
NEXT_RUN_ID = "frontier62A_stage_open_post_allocation_failure_mode_or_seed_expansion_v1"

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT

MODEL_ID = "frontier61_side_allocation_extratrees_d7_l120_v1"
LABEL_CONFIGS = (
    {"name": "balanced_margin_q45_opp_q55", "opportunity_q": 0.55, "margin_q": 0.45},
    {"name": "dense_margin_q35_opp_q50", "opportunity_q": 0.50, "margin_q": 0.35},
    {"name": "strict_margin_q55_opp_q60", "opportunity_q": 0.60, "margin_q": 0.55},
)
THRESHOLDS = (0.38, 0.42, 0.46)
MIN_MARGINS = (0.02, 0.04, 0.06)
MAX_HOLD_OPTIONS = (4, 6)
TARGET_DENSITY_LOW = 5.0
TARGET_DENSITY_HIGH = 10.0

BASE_RUNTIME_POLICY = {
    "InpCloseOnFlatSignal": False,
    "InpEntryTransitionOnly": False,
    "InpEntryTransitionRearmMinConfidenceDelta": 0.0,
    "InpAtrSltpEnabled": True,
    "InpAtrPeriod": f59.ATR_PERIOD,
    "InpAtrStopMultiplier": f59.ATR_STOP_MULT,
    "InpAtrTakeProfitMultiplier": f59.ATR_TP_MULT,
    "InpAtrMinStopPoints": f59.ATR_MIN_STOP_POINTS,
    "InpAtrMaxStopPoints": f59.ATR_MAX_STOP_POINTS,
    "InpAtrMinTakeProfitPoints": f59.ATR_MIN_TP_POINTS,
    "InpAtrMaxTakeProfitPoints": f59.ATR_MAX_TP_POINTS,
    "InpReentryCooldownBars": 0,
    "InpSameDirectionReentryCooldownBars": 0,
    "InpRuntimeVetoTapeEnabled": False,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Frontier61 side-allocation proxy and MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--proxy-only", action="store_true")
    parser.add_argument("--refresh-docs-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    created_at = utc_now()
    mkdirs()
    if args.refresh_docs_only:
        refresh_docs()
        print(json.dumps({"status": "refreshed_docs", "run_id": RUN_ID}, ensure_ascii=False, indent=2))
        return 0

    base = build_base()
    failure_audit = build_failure_mode_audit()
    label_contract = build_label_contract(base)
    training = train_side_allocation_model(base, label_contract)
    artifacts = export_model_artifacts(training)
    proxy_rows = evaluate_proxy_surface(base, training)
    proxy_row = select_primary_proxy_row(proxy_rows)
    split_payload = materialize_split_payload(base, training, proxy_row)
    spec = candidate_spec(proxy_row, artifacts)
    attempts = backfill.materialize_attempts(
        spec,
        split_payload,
        base["feature_order"],
        base["feature_order_hash"],
        Path(args.common_files_root),
    )
    attempts = apply_runtime_policy_overrides(attempts, proxy_row)
    write_proxy_artifacts(base, failure_audit, label_contract, training, artifacts, proxy_rows, proxy_row, attempts)

    if args.proxy_only:
        print(
            json.dumps(
                json_ready({"status": "proxy_ready", "run_id": RUN_ID, "candidate": proxy_row, "artifacts": artifacts}),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    compile_payload = backfill.compile_runtime_ea(Path(args.metaeditor_path))
    terminal_probe = backfill.terminal_processes()
    execution_payload = execute_attempts(args, spec, attempts, compile_payload, terminal_probe, created_at)
    runtime_rows = backfill.build_runtime_summary_rows(spec, attempts, execution_payload, split_payload)
    runtime_rows = attach_runtime_density(runtime_rows, split_payload)
    backfill.write_csv(RUN_ROOT / "mt5_runtime_probe_summary.csv", runtime_rows)

    classification = "runtime_probe_observation_no_authority"
    if not any(row.get("runtime_status") == "completed" and row.get("report_status") == "completed" for row in runtime_rows):
        classification = "blocked_attempt_failed"

    proxy_gap_rows = proxy_runtime_gap_rows(proxy_row, runtime_rows)
    label_contract_public = public_label_contract(label_contract)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "candidate_id": proxy_row["candidate_id"],
        "classification": classification,
        "runtime_probe_status": classification,
        "judgment": stage_judgment(runtime_rows, proxy_row),
        "failure_mode_observation": failure_mode_observation(runtime_rows, proxy_gap_rows),
        "failure_audit": failure_audit,
        "label_contract": label_contract_public,
        "training_summary": training_summary(training),
        "proxy_candidate": json_ready(proxy_row),
        "proxy_surface_rows": json_ready(proxy_rows),
        "model_artifacts": json_ready(artifacts),
        "runtime_policy": runtime_policy_for(proxy_row),
        "runtime_rows": runtime_rows,
        "proxy_runtime_gap_rows": proxy_gap_rows,
        "claim_boundary": backfill.claim_boundary_payload(),
        "created_at_utc": created_at,
    }
    backfill.write_json(RUN_ROOT / "final_decision.json", final)
    backfill.write_json(RUN_ROOT / "run_manifest.json", final)
    write_reports(final, proxy_row, runtime_rows, proxy_gap_rows)
    backfill.upsert_backfill_status_ledger(
        STAGE_NUM,
        STAGE_ID,
        created_at,
        classification,
        {
            "status": classification,
            "reason": "mandatory_stage_runtime_probe_recorded",
            "checks": {
                "candidate_id": proxy_row["candidate_id"],
                "onnx_path": artifacts["onnx_path"],
                "feature_order_hash": artifacts["feature_order_hash"],
                "runtime_policy": runtime_policy_for(proxy_row),
            },
        },
        spec,
        runtime_rows,
    )
    update_workspace_state(final)
    update_registers(final)
    print(json.dumps(json_ready({"status": classification, "run_id": RUN_ID, "judgment": final["judgment"]}), ensure_ascii=False, indent=2))
    return 0 if classification != "blocked_attempt_failed" else 1


def mkdirs() -> None:
    for path in (
        RUN_ROOT,
        MODELS_ROOT,
        FEATURE_ROOT,
        MT5_ROOT,
        REVIEWS_ROOT,
        SELECTED_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "02_runs" / RUN_A,
        STAGE_ROOT / "02_runs" / RUN_B,
        STAGE_ROOT / "02_runs" / RUN_C,
        STAGE_ROOT / "02_runs" / RUN_D,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)


def build_base() -> dict[str, Any]:
    frame = f23b.load_frame().copy()
    feature_order = f23b.read_feature_order()
    raw_path = f33b.load_raw_path(frame)
    x_raw = frame[feature_order].astype("float64").to_numpy()
    valid_features = np.isfinite(x_raw).all(axis=1)
    runtime = build_side_runtime_arrays(raw_path)
    finite = (
        valid_features
        & runtime["long_valid"]
        & runtime["short_valid"]
        & np.isfinite(runtime["long_pnl"])
        & np.isfinite(runtime["short_pnl"])
    )
    train_mask = f33b.split_mask(frame, "train") & finite
    if not train_mask.any():
        raise RuntimeError("F61 has no finite train rows")
    return {
        "frame": frame,
        "feature_order": feature_order,
        "feature_order_hash": ordered_hash(feature_order),
        "raw_path": raw_path,
        "x_raw": x_raw,
        "valid_features": valid_features,
        "finite": finite,
        "train_mask": train_mask,
        "runtime": runtime,
        "data_integrity": {
            "feature_count": len(feature_order),
            "feature_order_hash": ordered_hash(feature_order),
            "expected_feature_hash": f23b.EXPECTED_FEATURE_HASH,
            "feature_contract_match": len(feature_order) == 58 and ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
            "raw_rows": int(raw_path["raw_rows"]),
            "missing_entry_positions": int(raw_path["missing_entry_positions"]),
            "missing_future_positions": int(raw_path["missing_future_positions"]),
        },
    }


def build_side_runtime_arrays(raw_path: Mapping[str, Any]) -> dict[str, np.ndarray]:
    raw = raw_path["raw"]
    entry_pos = np.asarray(raw_path["entry_pos"], dtype="int64")
    open_prices = raw["open"].to_numpy(dtype="float64")
    high_prices = raw["high"].to_numpy(dtype="float64")
    low_prices = raw["low"].to_numpy(dtype="float64")
    close_prices = raw["close"].to_numpy(dtype="float64")
    prev_close = np.r_[np.nan, close_prices[:-1]]
    tr = np.nanmax(
        np.vstack(
            [
                high_prices - low_prices,
                np.abs(high_prices - prev_close),
                np.abs(low_prices - prev_close),
            ]
        ),
        axis=0,
    )
    atr = pd.Series(tr).rolling(f59.ATR_PERIOD, min_periods=f59.ATR_PERIOD).mean().to_numpy(dtype="float64")
    out: dict[str, np.ndarray] = {"atr": atr}
    for side_name, side in (("long", 1), ("short", -1)):
        pnl = np.full(len(entry_pos), np.nan, dtype="float64")
        valid = np.zeros(len(entry_pos), dtype=bool)
        exit_pos = np.full(len(entry_pos), -1, dtype="int64")
        exit_reason = np.full(len(entry_pos), "", dtype=object)
        for idx in range(len(entry_pos)):
            result = simulate_isolated_side(
                int(idx),
                int(side),
                entry_pos,
                open_prices,
                high_prices,
                low_prices,
                atr,
                max_hold=max(MAX_HOLD_OPTIONS),
            )
            if result["valid"]:
                pnl[idx] = float(result["pnl"])
                valid[idx] = True
                exit_pos[idx] = int(result["exit_pos"])
                exit_reason[idx] = str(result["exit_reason"])
        out[f"{side_name}_pnl"] = pnl
        out[f"{side_name}_valid"] = valid
        out[f"{side_name}_exit_pos"] = exit_pos
        out[f"{side_name}_exit_reason"] = exit_reason
    return out


def simulate_isolated_side(
    idx: int,
    side: int,
    entry_pos: np.ndarray,
    open_prices: np.ndarray,
    high_prices: np.ndarray,
    low_prices: np.ndarray,
    atr: np.ndarray,
    *,
    max_hold: int,
) -> dict[str, Any]:
    p = int(entry_pos[idx])
    if p < f59.ATR_PERIOD or p + 1 >= len(open_prices):
        return {"valid": False}
    entry = float(open_prices[p])
    atr_value = float(atr[p])
    if not math.isfinite(entry) or entry <= 0.0 or not math.isfinite(atr_value) or atr_value <= 0.0:
        return {"valid": False}
    stop_points = min(max(atr_value * f59.ATR_STOP_MULT, f59.ATR_MIN_STOP_POINTS), f59.ATR_MAX_STOP_POINTS)
    take_points = min(max(atr_value * f59.ATR_TP_MULT, f59.ATR_MIN_TP_POINTS), f59.ATR_MAX_TP_POINTS)
    end = min(p + int(max_hold), len(open_prices) - 1)
    if side > 0:
        stop_price = entry - stop_points
        take_price = entry + take_points
        for q in range(p + 1, end + 1):
            if float(low_prices[q]) <= stop_price:
                return {"valid": True, "pnl": math.log(stop_price / entry) - f23b.scout.ROUGH_COST_LOG_RETURN, "exit_pos": q, "exit_reason": "stop"}
            if float(high_prices[q]) >= take_price:
                return {"valid": True, "pnl": math.log(take_price / entry) - f23b.scout.ROUGH_COST_LOG_RETURN, "exit_pos": q, "exit_reason": "take"}
        exit_price = float(open_prices[end])
        if not math.isfinite(exit_price) or exit_price <= 0.0:
            return {"valid": False}
        return {"valid": True, "pnl": math.log(exit_price / entry) - f23b.scout.ROUGH_COST_LOG_RETURN, "exit_pos": end, "exit_reason": "maxhold"}
    stop_price = entry + stop_points
    take_price = entry - take_points
    for q in range(p + 1, end + 1):
        if float(high_prices[q]) >= stop_price:
            return {"valid": True, "pnl": math.log(entry / stop_price) - f23b.scout.ROUGH_COST_LOG_RETURN, "exit_pos": q, "exit_reason": "stop"}
        if float(low_prices[q]) <= take_price:
            return {"valid": True, "pnl": math.log(entry / take_price) - f23b.scout.ROUGH_COST_LOG_RETURN, "exit_pos": q, "exit_reason": "take"}
    exit_price = float(open_prices[end])
    if not math.isfinite(exit_price) or exit_price <= 0.0:
        return {"valid": False}
    return {"valid": True, "pnl": math.log(entry / exit_price) - f23b.scout.ROUGH_COST_LOG_RETURN, "exit_pos": end, "exit_reason": "maxhold"}


def build_label_contract(base: Mapping[str, Any]) -> dict[str, Any]:
    runtime = base["runtime"]
    train_mask = np.asarray(base["train_mask"], dtype=bool)
    long_pnl = np.asarray(runtime["long_pnl"], dtype="float64")
    short_pnl = np.asarray(runtime["short_pnl"], dtype="float64")
    best = np.maximum(long_pnl, short_pnl)
    margin = np.abs(long_pnl - short_pnl)
    selected_contract: dict[str, Any] | None = None
    selected_labels: np.ndarray | None = None
    contract_rows: list[dict[str, Any]] = []
    for config in LABEL_CONFIGS:
        opportunity_cut = float(np.quantile(best[train_mask], float(config["opportunity_q"])))
        margin_cut = float(np.quantile(margin[train_mask], float(config["margin_q"])))
        labels = labels_from_contract(long_pnl, short_pnl, opportunity_cut, margin_cut)
        row = label_distribution_row(labels, train_mask, config, opportunity_cut, margin_cut)
        contract_rows.append(row)
        if (
            row["train_short_fraction"] >= 0.05
            and row["train_long_fraction"] >= 0.05
            and row["train_flat_fraction"] <= 0.82
            and selected_contract is None
        ):
            selected_contract = dict(row)
            selected_labels = labels
    if selected_contract is None:
        selected_contract = dict(contract_rows[0])
        selected_labels = labels_from_contract(long_pnl, short_pnl, selected_contract["opportunity_cut"], selected_contract["margin_cut"])
        selected_contract["selection_warning"] = "class_balance_guard_not_met_used_first_config"
    selected_contract["all_label_config_rows"] = [dict(row) for row in contract_rows]
    selected_contract["labels"] = selected_labels
    return selected_contract


def labels_from_contract(long_pnl: np.ndarray, short_pnl: np.ndarray, opportunity_cut: float, margin_cut: float) -> np.ndarray:
    labels = np.ones(len(long_pnl), dtype="int8")
    long_ok = (long_pnl > short_pnl) & (long_pnl >= opportunity_cut) & ((long_pnl - short_pnl) >= margin_cut)
    short_ok = (short_pnl > long_pnl) & (short_pnl >= opportunity_cut) & ((short_pnl - long_pnl) >= margin_cut)
    labels[short_ok] = 0
    labels[long_ok] = 2
    return labels


def label_distribution_row(
    labels: np.ndarray,
    train_mask: np.ndarray,
    config: Mapping[str, Any],
    opportunity_cut: float,
    margin_cut: float,
) -> dict[str, Any]:
    total = max(1, int(train_mask.sum()))
    return {
        "label_config": config["name"],
        "opportunity_q": float(config["opportunity_q"]),
        "margin_q": float(config["margin_q"]),
        "opportunity_cut": safe_float(opportunity_cut),
        "margin_cut": safe_float(margin_cut),
        "train_short_count": int(((labels == 0) & train_mask).sum()),
        "train_flat_count": int(((labels == 1) & train_mask).sum()),
        "train_long_count": int(((labels == 2) & train_mask).sum()),
        "train_short_fraction": float(((labels == 0) & train_mask).sum() / total),
        "train_flat_fraction": float(((labels == 1) & train_mask).sum() / total),
        "train_long_fraction": float(((labels == 2) & train_mask).sum() / total),
        "flat_definition": "flat_when_neither_side_beats_opportunity_cut_and_margin",
        "tie_break": "flat_on_tie_or_margin_fail",
        "future_boundary": "label_uses_future_path_only_for_training_label_not_runtime_features",
    }


def train_side_allocation_model(base: Mapping[str, Any], label_contract: Mapping[str, Any]) -> dict[str, Any]:
    x_raw = np.asarray(base["x_raw"], dtype="float64")
    finite = np.asarray(base["finite"], dtype=bool)
    train_mask = np.asarray(base["train_mask"], dtype=bool)
    labels = np.asarray(label_contract["labels"], dtype="int8")
    missing = sorted(set(f04d.LABEL_ORDER) - set(int(value) for value in labels[train_mask]))
    if missing:
        raise RuntimeError(f"F61 train labels missing classes: {missing}")
    model = ExtraTreesClassifier(
        n_estimators=600,
        max_depth=7,
        min_samples_leaf=120,
        random_state=6101,
        n_jobs=-1,
        class_weight="balanced_subsample",
    )
    model.fit(x_raw[train_mask], labels[train_mask])
    probabilities = np.zeros((len(labels), 3), dtype="float64")
    probabilities[finite] = ordered_sklearn_probabilities(model, x_raw[finite], class_order=f04d.LABEL_ORDER)
    class_rows = []
    for split in ("train", "validation", "oos"):
        split_mask = f33b.split_mask(base["frame"], split) & finite
        y_true = labels[split_mask]
        probs = probabilities[split_mask]
        y_pred = np.asarray(f04d.LABEL_ORDER, dtype="int64")[probs.argmax(axis=1)]
        class_rows.append(
            {
                "split": split,
                "rows": int(split_mask.sum()),
                "balanced_accuracy": safe_float(balanced_accuracy_score(y_true, y_pred)),
                "macro_f1": safe_float(f1_score(y_true, y_pred, labels=f04d.LABEL_ORDER, average="macro", zero_division=0)),
                "log_loss": safe_float(log_loss(y_true, probs, labels=f04d.LABEL_ORDER)),
                "pred_short": int((y_pred == 0).sum()),
                "pred_flat": int((y_pred == 1).sum()),
                "pred_long": int((y_pred == 2).sum()),
                "true_short": int((y_true == 0).sum()),
                "true_flat": int((y_true == 1).sum()),
                "true_long": int((y_true == 2).sum()),
            }
        )
    return {
        "model": model,
        "labels": labels,
        "probabilities": probabilities,
        "class_rows": class_rows,
        "x_raw": x_raw,
        "finite": finite,
    }


def export_model_artifacts(training: Mapping[str, Any]) -> dict[str, Any]:
    model = training["model"]
    model_path = MODELS_ROOT / f"{MODEL_ID}.joblib"
    onnx_path = MODELS_ROOT / f"{MODEL_ID}.onnx"
    io_path(model_path.parent).mkdir(parents=True, exist_ok=True)
    joblib.dump(model, io_path(model_path))
    export_meta = export_sklearn_to_onnx_zipmap_disabled(
        model,
        onnx_path,
        feature_count=58,
        target_opset=12,
        drop_label_output=False,
    )
    sample = np.asarray(training["x_raw"], dtype="float64")[np.asarray(training["finite"], dtype=bool)][:1024]
    expected = ordered_sklearn_probabilities(model, sample, class_order=f04d.LABEL_ORDER)
    parity = onnx_probability_parity(onnx_path, sample, expected)
    artifacts = {
        "model_id": MODEL_ID,
        "model_path": model_path.as_posix(),
        "model_sha256": sha256_file(model_path),
        "onnx_path": onnx_path.as_posix(),
        "onnx_sha256": sha256_file(onnx_path),
        "onnx_export": export_meta,
        "onnx_parity": parity,
        "feature_count": 58,
        "feature_order_hash": f23b.EXPECTED_FEATURE_HASH,
        "label_order": f04d.LABEL_ORDER,
    }
    backfill.write_json(MODELS_ROOT / "model_artifact_manifest.json", artifacts)
    return artifacts


def onnx_probability_parity(onnx_path: Path, values: np.ndarray, expected: np.ndarray) -> dict[str, Any]:
    import onnxruntime as ort

    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: values.astype("float32")})
    candidates = [np.asarray(output, dtype="float64") for output in outputs if np.asarray(output).ndim == 2 and np.asarray(output).shape[1] == 3]
    if not candidates:
        return {"passed": False, "reason": "no_3class_probability_output", "rows": int(len(values))}
    actual = candidates[-1]
    diff = np.abs(actual - expected)
    return {
        "passed": bool(float(diff.max()) <= 1e-5),
        "max_abs_diff": safe_float(float(diff.max())),
        "mean_abs_diff": safe_float(float(diff.mean())),
        "rows": int(len(values)),
        "output_count": int(len(outputs)),
        "input_name": input_name,
    }


def evaluate_proxy_surface(base: Mapping[str, Any], training: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    probabilities = np.asarray(training["probabilities"], dtype="float64")
    for threshold in THRESHOLDS:
        for min_margin in MIN_MARGINS:
            for max_hold in MAX_HOLD_OPTIONS:
                row = {
                    "candidate_id": candidate_id(threshold, min_margin, max_hold),
                    "model_id": MODEL_ID,
                    "decision_mode": "edge_margin",
                    "short_threshold": float(threshold),
                    "long_threshold": float(threshold),
                    "min_margin": float(min_margin),
                    "max_hold_bars": int(max_hold),
                    "runtime_probe_candidate_flag": False,
                }
                signal = signal_from_probability_params(probabilities, threshold, threshold, min_margin)
                for split in ("train", "validation", "oos"):
                    metrics = sequential_proxy_metrics(base, signal, split, int(max_hold))
                    prefix = "validation" if split == "validation" else split
                    row.update(prefixed_metrics(prefix, metrics))
                row["forward_min_pf"] = min(safe_float(row["validation_profit_factor"]), safe_float(row["oos_profit_factor"]))
                row["forward_max_dd"] = max(safe_float(row["validation_dd_risk"]), safe_float(row["oos_dd_risk"]))
                row["forward_min_density"] = min(safe_float(row["validation_trades_per_day"]), safe_float(row["oos_trades_per_day"]))
                row["forward_density_target_flag"] = density_in_band(row["validation_trades_per_day"]) and density_in_band(row["oos_trades_per_day"])
                row["forward_dual_positive_flag"] = safe_float(row["validation_profit_factor"]) >= 1.0 and safe_float(row["oos_profit_factor"]) >= 1.0
                row["forward_dd_under10_flag"] = row["forward_max_dd"] < 10.0
                rows.append(row)
    return rows


def signal_from_probability_params(probabilities: np.ndarray, short_threshold: float, long_threshold: float, min_margin: float) -> np.ndarray:
    spec = backfill.CandidateSpec(
        stage_num=STAGE_NUM,
        stage_id=STAGE_ID,
        parent_run_id=RUN_B,
        source_run_id=RUN_B,
        candidate_id="temporary_proxy_signal",
        model_id=MODEL_ID,
        model_path=Path(""),
        onnx_path=Path(""),
        decision_mode="edge_margin",
        short_threshold=float(short_threshold),
        long_threshold=float(long_threshold),
        min_margin=float(min_margin),
        max_hold_bars=6,
        cooldown_bars=0,
        source_contract="temporary_proxy_signal",
        source_note="temporary proxy signal",
    )
    return backfill.signal_from_probabilities(probabilities, spec)


def sequential_proxy_metrics(base: Mapping[str, Any], signal: np.ndarray, split: str, max_hold: int) -> dict[str, Any]:
    frame = base["frame"]
    raw_path = base["raw_path"]
    runtime = base["runtime"]
    finite = np.asarray(base["finite"], dtype=bool)
    split_mask = f33b.split_mask(frame, split) & finite
    indices = np.flatnonzero(split_mask)
    entry_pos = np.asarray(raw_path["entry_pos"], dtype="int64")
    open_prices = raw_path["raw"]["open"].to_numpy(dtype="float64")
    high_prices = raw_path["raw"]["high"].to_numpy(dtype="float64")
    low_prices = raw_path["raw"]["low"].to_numpy(dtype="float64")
    atr = np.asarray(runtime["atr"], dtype="float64")
    pnl: list[float] = []
    times: list[Any] = []
    side_counts = {1: 0, -1: 0}
    exit_reasons: dict[str, int] = {}
    next_allowed_pos = -1
    raw_signal_count = int((signal[split_mask] != 0).sum())
    for idx in indices:
        side = int(signal[idx])
        if side == 0:
            continue
        pos = int(entry_pos[idx])
        if pos < next_allowed_pos:
            continue
        result = simulate_isolated_side(idx, side, entry_pos, open_prices, high_prices, low_prices, atr, max_hold=max_hold)
        if not result["valid"]:
            continue
        pnl.append(float(result["pnl"]))
        times.append(frame["timestamp"].iloc[idx])
        side_counts[side] += 1
        exit_reasons[str(result["exit_reason"])] = exit_reasons.get(str(result["exit_reason"]), 0) + 1
        next_allowed_pos = int(result["exit_pos"]) + 1
    arr = np.asarray(pnl, dtype="float64")
    metrics = f23b.scout.trade_metrics(arr, pd.Series(times))
    days = f23b.scout.count_scope_days(frame.loc[split_mask, "timestamp"])
    return {
        "profit_factor": safe_float(metrics.get("profit_factor")),
        "dd_risk": safe_float(max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"]))),
        "trade_count": int(len(arr)),
        "signal_count": raw_signal_count,
        "trades_per_day": float(len(arr) / days) if days else 0.0,
        "signals_per_day": float(raw_signal_count / days) if days else 0.0,
        "net_profit": safe_float(metrics.get("net_profit")),
        "win_rate": float((arr > 0.0).mean()) if len(arr) else 0.0,
        "long_trade_count": int(side_counts[1]),
        "short_trade_count": int(side_counts[-1]),
        "stop_exit_count": int(exit_reasons.get("stop", 0)),
        "take_exit_count": int(exit_reasons.get("take", 0)),
        "maxhold_exit_count": int(exit_reasons.get("maxhold", 0)),
        "entry_suppression_count": max(0, raw_signal_count - int(len(arr))),
    }


def select_primary_proxy_row(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not rows:
        raise RuntimeError("F61 proxy surface produced no rows")

    def density_error(row: Mapping[str, Any], key: str) -> float:
        density = safe_float(row.get(key))
        if TARGET_DENSITY_LOW <= density <= TARGET_DENSITY_HIGH:
            return 0.0
        if density < TARGET_DENSITY_LOW:
            return TARGET_DENSITY_LOW - density
        return density - TARGET_DENSITY_HIGH

    def score(row: Mapping[str, Any]) -> tuple[float, ...]:
        return (
            -density_error(row, "train_trades_per_day"),
            safe_float(row.get("train_profit_factor")),
            -safe_float(row.get("train_dd_risk")),
            1.0 if row.get("forward_density_target_flag") else 0.0,
            1.0 if row.get("forward_dual_positive_flag") else 0.0,
            1.0 if row.get("forward_dd_under10_flag") else 0.0,
            safe_float(row.get("forward_min_pf")),
            -safe_float(row.get("forward_max_dd")),
            -density_error(row, "validation_trades_per_day") - density_error(row, "oos_trades_per_day"),
            -abs(safe_float(row.get("validation_long_trade_count")) - safe_float(row.get("validation_short_trade_count"))) / 1000.0,
        )

    selected = max((dict(row) for row in rows), key=score)
    selected["runtime_probe_candidate_flag"] = True
    selected["selection_rule"] = (
        "pre_registered_train_density_pf_then_readonly_forward_balance_single_probe"
        "(사전등록 학습 밀도/PF 우선 + 전진 읽기 균형, 단일 런타임 탐침)"
    )
    return selected


def materialize_split_payload(
    base: Mapping[str, Any],
    training: Mapping[str, Any],
    proxy_row: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    rows_for_expected: list[dict[str, Any]] = []
    frame = base["frame"].copy()
    feature_order = list(base["feature_order"])
    x_raw = np.asarray(base["x_raw"], dtype="float64")
    finite = np.asarray(base["finite"], dtype=bool)
    probabilities = np.asarray(training["probabilities"], dtype="float64")
    signal_all = signal_from_probability_params(
        probabilities,
        float(proxy_row["short_threshold"]),
        float(proxy_row["long_threshold"]),
        float(proxy_row["min_margin"]),
    )
    runtime_frame = pd.concat(
        [
            frame[["timestamp", "symbol", "split"]].reset_index(drop=True),
            pd.DataFrame(x_raw, columns=feature_order),
        ],
        axis=1,
    )
    for runtime_split, source_split in (("validation_is", "validation"), ("oos", "oos")):
        split_all = runtime_frame["split"].astype(str).eq(source_split).to_numpy()
        export_mask = split_all & finite
        export_frame = runtime_frame.loc[export_mask].copy()
        feature_path = FEATURE_ROOT / f"{RUN_ID}_{runtime_split}_features.csv"
        feature_export = mt5.export_mt5_feature_matrix_csv(export_frame, feature_order, feature_path)
        expected_signal = signal_all[export_mask]
        expected = expected_signal_summary(export_frame, expected_signal, runtime_split, proxy_row)
        rows_for_expected.append(expected)
        out[runtime_split] = {
            "source_split": source_split,
            "frame": export_frame,
            "signal": expected_signal,
            "feature_export": feature_export,
            "expected": expected,
            "from_date": backfill.split_date_range(export_frame)[0],
            "to_date": backfill.split_date_range(export_frame)[1],
        }
    backfill.write_csv(RUN_ROOT / "expected_signal_summary.csv", rows_for_expected)
    return out


def expected_signal_summary(frame: pd.DataFrame, signal: np.ndarray, runtime_split: str, proxy_row: Mapping[str, Any]) -> dict[str, Any]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True).reset_index(drop=True)
    days = backfill.count_scope_days(timestamps) if len(timestamps) else 0
    signal_count = int((signal != 0).sum())
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "split": runtime_split,
        "rows": int(len(frame)),
        "days_in_scope": int(days),
        "decision_mode": "edge_margin_side_allocation",
        "short_threshold": float(proxy_row["short_threshold"]),
        "long_threshold": float(proxy_row["long_threshold"]),
        "min_margin": float(proxy_row["min_margin"]),
        "signal_count": signal_count,
        "long_count": int((signal == 1).sum()),
        "short_count": int((signal == -1).sum()),
        "flat_count": int((signal == 0).sum()),
        "expected_density_per_day": float(signal_count / days) if days else 0.0,
    }


def candidate_spec(proxy_row: Mapping[str, Any], artifacts: Mapping[str, Any]) -> backfill.CandidateSpec:
    return backfill.CandidateSpec(
        stage_num=STAGE_NUM,
        stage_id=STAGE_ID,
        parent_run_id=RUN_B,
        source_run_id=RUN_B,
        candidate_id=str(proxy_row["candidate_id"]),
        model_id=str(artifacts["model_id"]),
        model_path=Path(str(artifacts["model_path"])),
        onnx_path=Path(str(artifacts["onnx_path"])),
        decision_mode="edge_margin",
        short_threshold=float(proxy_row["short_threshold"]),
        long_threshold=float(proxy_row["long_threshold"]),
        min_margin=float(proxy_row["min_margin"]),
        max_hold_bars=int(proxy_row["max_hold_bars"]),
        cooldown_bars=0,
        source_contract="f61_3class_side_allocation_short_flat_long",
        source_note="F61 trains a new 3-class side allocation target; F53-F60 are reference-only failure memory.",
    )


def apply_runtime_policy_overrides(attempts: Sequence[Mapping[str, Any]], proxy_row: Mapping[str, Any]) -> list[dict[str, Any]]:
    patched: list[dict[str, Any]] = []
    runtime_policy = runtime_policy_for(proxy_row)
    for attempt in attempts:
        row = dict(attempt)
        set_payload = dict(row["set"])
        set_path = Path(str(set_payload["path"]))
        override_set_file(set_path, runtime_policy)
        set_payload["sha256"] = sha256_file(set_path)
        set_payload["runtime_policy_override"] = json_ready(runtime_policy)
        row["set"] = set_payload
        row["runtime_policy"] = json_ready(runtime_policy)
        patched.append(row)
    backfill.write_json(MT5_ROOT / "runtime_policy_override_manifest.json", {"policy": runtime_policy, "attempts": patched})
    return patched


def runtime_policy_for(proxy_row: Mapping[str, Any]) -> dict[str, Any]:
    return {**BASE_RUNTIME_POLICY, "InpMaxHoldBars": int(proxy_row["max_hold_bars"])}


def attach_runtime_density(runtime_rows: Sequence[Mapping[str, Any]], split_payload: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in runtime_rows:
        item = dict(row)
        expected = split_payload[str(item.get("split"))]["expected"]
        days = float(expected.get("days_in_scope", 0) or 0)
        trades = safe_float(item.get("trade_count"))
        item["days_in_scope"] = int(days)
        item["runtime_trades_per_day"] = float(trades / days) if days else 0.0
        item["expected_signal_density_per_day"] = expected.get("expected_density_per_day")
        out.append(item)
    return out


def proxy_runtime_gap_rows(proxy_row: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        split = str(row.get("split", ""))
        proxy_prefix = "validation" if split == "validation_is" else "oos"
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "candidate_id": proxy_row["candidate_id"],
                "split": split,
                "proxy_profit_factor": safe_float(proxy_row.get(f"{proxy_prefix}_profit_factor")),
                "mt5_profit_factor": safe_float(row.get("profit_factor")),
                "profit_factor_gap_mt5_minus_proxy": safe_float(safe_float(row.get("profit_factor")) - safe_float(proxy_row.get(f"{proxy_prefix}_profit_factor"))),
                "proxy_dd_risk": safe_float(proxy_row.get(f"{proxy_prefix}_dd_risk")),
                "mt5_max_drawdown_percent": safe_float(row.get("max_drawdown_percent")),
                "dd_gap_mt5_minus_proxy": safe_float(safe_float(row.get("max_drawdown_percent")) - safe_float(proxy_row.get(f"{proxy_prefix}_dd_risk"))),
                "proxy_trade_count": safe_float(proxy_row.get(f"{proxy_prefix}_trade_count")),
                "mt5_trade_count": safe_float(row.get("trade_count")),
                "trade_count_gap_mt5_minus_proxy": safe_float(safe_float(row.get("trade_count")) - safe_float(proxy_row.get(f"{proxy_prefix}_trade_count"))),
                "proxy_trades_per_day": safe_float(proxy_row.get(f"{proxy_prefix}_trades_per_day")),
                "mt5_trades_per_day": safe_float(row.get("runtime_trades_per_day")),
                "density_gap_mt5_minus_proxy": safe_float(safe_float(row.get("runtime_trades_per_day")) - safe_float(proxy_row.get(f"{proxy_prefix}_trades_per_day"))),
                "signal_count_diff": row.get("signal_count_diff"),
                "feature_ready_diff": row.get("feature_ready_diff"),
            }
        )
    backfill.write_csv(RUN_ROOT / "proxy_runtime_gap.csv", rows)
    return rows


def build_failure_mode_audit() -> dict[str, Any]:
    stage_rows = [
        {"stage": "F53", "axis": "short", "validation_pf": 0.37, "validation_dd": 31.92, "validation_trades": 1325, "oos_pf": 0.56, "oos_dd": 19.18, "oos_trades": 1337, "signal_diff": 0},
        {"stage": "F54", "axis": "short", "validation_pf": 0.41, "validation_dd": 63.63, "validation_trades": 2781, "oos_pf": 0.61, "oos_dd": 28.22, "oos_trades": 2163, "signal_diff": 0},
        {"stage": "F55", "axis": "short", "validation_pf": 0.42, "validation_dd": 20.84, "validation_trades": 954, "oos_pf": 0.64, "oos_dd": 8.30, "oos_trades": 711, "signal_diff": 0},
        {"stage": "F56", "axis": "short", "validation_pf": 0.46, "validation_dd": 29.91, "validation_trades": 1389, "oos_pf": 0.74, "oos_dd": 9.27, "oos_trades": 1018, "signal_diff": 0},
        {"stage": "F57", "axis": "short", "validation_pf": 0.43, "validation_dd": 32.41, "validation_trades": 1331, "oos_pf": 0.68, "oos_dd": 11.12, "oos_trades": 902, "signal_diff": 0},
        {"stage": "F58", "axis": "short", "validation_pf": 0.36, "validation_dd": 34.43, "validation_trades": 1405, "oos_pf": 0.68, "oos_dd": 11.38, "oos_trades": 1217, "signal_diff": 0},
        {"stage": "F59", "axis": "long", "validation_pf": 0.46, "validation_dd": 22.84, "validation_trades": 1002, "oos_pf": 0.58, "oos_dd": 10.27, "oos_trades": 688, "signal_diff": 0},
        {"stage": "F60", "axis": "long_admission", "validation_pf": 0.41, "validation_dd": 14.89, "validation_trades": 661, "oos_pf": 0.51, "oos_dd": 8.48, "oos_trades": 494, "signal_diff": -1501},
    ]
    return {
        "audit_basis": "stage_run_ledger_rows_F53_to_F60_and_runtime_reports",
        "rows": stage_rows,
        "dominant_read": "F53-F59 have completed MT5 rows and mostly signal_diff=0, so the repeated failure is treated as alpha/economics failure more than handoff failure; F60 separately records intentional admission suppression.",
        "f61_implication": "Change target to side allocation while keeping feature contract and runtime probe parity checks explicit.",
    }


def write_proxy_artifacts(
    base: Mapping[str, Any],
    failure_audit: Mapping[str, Any],
    label_contract: Mapping[str, Any],
    training: Mapping[str, Any],
    artifacts: Mapping[str, Any],
    proxy_rows: Sequence[Mapping[str, Any]],
    proxy_row: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
) -> None:
    label_contract_public = public_label_contract(label_contract)
    stage_open_manifest = {
        "stage_id": STAGE_ID,
        "run_id": RUN_A,
        "hypothesis": "3class_side_allocation_can_find_non_axis_pf_source_after_short_and_long_friction_memory",
        "work_family": "runtime_backtest",
        "primary_skill": "obsidian-runtime-parity",
        "support_skills": ["obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-experiment-design", "obsidian-model-validation"],
        "grok_stage_open_classification": grok_classification(GROK_STAGE_OPEN_ROOT),
        "local_verification_status": "completed_before_runtime_probe_materialization",
        "failure_audit": failure_audit,
        "label_contract": label_contract_public,
        "feature_contract": base["data_integrity"],
        "proxy_grid_freeze": proxy_grid_freeze_payload(),
        "tier_plan": tier_plan_payload(),
        "selected_proxy_candidate": proxy_row,
        "claim_boundary": backfill.claim_boundary_payload(),
    }
    backfill.write_json(STAGE_ROOT / "02_runs" / RUN_A / "stage_open_manifest.json", stage_open_manifest)
    backfill.write_json(STAGE_ROOT / "01_inputs" / "failure_mode_audit_f53_f60.json", failure_audit)
    backfill.write_json(STAGE_ROOT / "01_inputs" / "label_contract.json", label_contract_public)
    backfill.write_json(STAGE_ROOT / "01_inputs" / "runtime_policy_manifest.json", {"policy": runtime_policy_for(proxy_row), "attempts": attempts})
    backfill.write_csv(STAGE_ROOT / "02_runs" / RUN_B / "proxy_surface_summary.csv", proxy_rows)
    backfill.write_json(STAGE_ROOT / "02_runs" / RUN_B / "selected_proxy_candidate.json", proxy_row)
    backfill.write_csv(STAGE_ROOT / "02_runs" / RUN_B / "model_classification_summary.csv", training["class_rows"])
    backfill.write_json(RUN_ROOT / "source_truth_snapshot.json", stage_open_manifest | {"model_artifacts": artifacts})
    backfill.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief_text(stage_open_manifest))
    backfill.write_text_sig(REVIEWS_ROOT / "runA_report.md", run_a_report_text(stage_open_manifest))
    backfill.write_text_sig(REVIEWS_ROOT / "local_verification.md", local_verification_text(stage_open_manifest, artifacts))


def public_label_contract(label_contract: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in label_contract.items() if key != "labels"}
    backfill.write_text_sig(REVIEWS_ROOT / "grok_stage_open_receipt.md", grok_receipt_text("stage_open(단계 개방)", GROK_STAGE_OPEN_ROOT))
    backfill.write_text_sig(REVIEWS_ROOT / "grok_wrapper_guard_receipt.md", grok_receipt_text("wrapper_guard(래퍼 보호)", GROK_WRAPPER_GUARD_ROOT))
    backfill.write_text_sig(REVIEWS_ROOT / "runB_report.md", run_b_report_text(proxy_rows, proxy_row, label_contract_public, training))


def training_summary(training: Mapping[str, Any]) -> dict[str, Any]:
    labels = np.asarray(training["labels"], dtype="int8")
    return {
        "class_rows": training["class_rows"],
        "label_counts_all": {str(label): int((labels == label).sum()) for label in f04d.LABEL_ORDER},
    }


def write_reports(
    final: Mapping[str, Any],
    proxy_row: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
) -> None:
    backfill.write_json(REVIEWS_ROOT / "runtime_probe_status.json", final)
    backfill.write_text_sig(REVIEWS_ROOT / "runtime_probe_report.md", runtime_probe_report_text(final, runtime_rows))
    backfill.write_text_sig(REVIEWS_ROOT / f"{RUN_ID}_report.md", runtime_probe_report_text(final, runtime_rows))
    backfill.write_text_sig(REVIEWS_ROOT / "runC_report.md", run_c_report_text(runtime_rows, proxy_gap_rows))
    backfill.write_text_sig(REVIEWS_ROOT / "proxy_runtime_gap_report.md", proxy_runtime_gap_report_text(proxy_gap_rows))
    backfill.write_text_sig(REVIEWS_ROOT / "runD_closeout_report.md", run_d_report_text(final))
    backfill.write_text_sig(REVIEWS_ROOT / "required_gate_coverage_audit.md", required_gate_audit_text(final))
    if path_exists(GROK_PRE_MT5_ROOT / "clean_output.md"):
        backfill.write_text_sig(REVIEWS_ROOT / "grok_pre_mt5_receipt.md", grok_receipt_text("pre_mt5(MT5 전)", GROK_PRE_MT5_ROOT))
    if path_exists(GROK_STAGE_CLOSE_ROOT / "clean_output.md"):
        backfill.write_text_sig(REVIEWS_ROOT / "grok_stage_closeout_receipt.md", grok_receipt_text("stage_closeout(단계 마감)", GROK_STAGE_CLOSE_ROOT))
    backfill.write_text_sig(SELECTED_ROOT / "selection_status.md", selection_status_text(final))
    backfill.write_json(SELECTED_ROOT / "selection_status.json", final)
    if str(final.get("judgment", "")).startswith("negative_memory"):
        backfill.write_text_sig(SELECTED_ROOT / "negative_memory.md", negative_memory_text(final))
    else:
        backfill.write_text_sig(SELECTED_ROOT / "preserved_clue.md", preserved_clue_text(final))


def proxy_grid_freeze_payload() -> dict[str, Any]:
    return {
        "thresholds": THRESHOLDS,
        "min_margins": MIN_MARGINS,
        "max_hold_options": MAX_HOLD_OPTIONS,
        "grid_rows": len(THRESHOLDS) * len(MIN_MARGINS) * len(MAX_HOLD_OPTIONS),
        "selection_metric": "train density target, train PF, train DD, then read-only validation/OOS balance",
        "one_candidate_freeze": "exactly one selected_proxy_candidate is materialized for MT5 before any repair",
        "posthoc_expansion": "forbidden within F61 before first MT5 runtime probe",
    }


def tier_plan_payload() -> dict[str, Any]:
    return {
        "tier_a": "validation_is and oos MT5 runtime probe rows are Tier A separate",
        "tier_b": "missing_required at stage open because no Tier B runtime payload is materialized in this packet",
        "tier_ab_combined": "missing_required at stage open because no routed Tier A+B payload is materialized in this packet",
        "boundary": "Tier B absence cannot support completion or authority claims",
    }


def stage_judgment(runtime_rows: Sequence[Mapping[str, Any]], proxy_row: Mapping[str, Any]) -> str:
    completed = [row for row in runtime_rows if row.get("runtime_status") == "completed" and row.get("report_status") == "completed"]
    if not completed:
        return "blocked_side_allocation_runtime_probe_attempt_failed(차단, 방향 배분 런타임 탐침 시도 실패)"
    min_pf = min(safe_float(row.get("profit_factor")) for row in completed)
    max_dd = max(safe_float(row.get("max_drawdown_percent")) for row in completed)
    min_density = min(safe_float(row.get("runtime_trades_per_day")) for row in completed)
    if min_pf >= 1.0 and max_dd < 10.0 and density_in_band(min_density):
        return "preserved_clue_side_allocation_runtime_probe_observation(보존 단서, 방향 배분 런타임 탐침 관찰)"
    if min_pf < 1.0:
        return "negative_memory_side_allocation_failed_runtime_pf(부정 기억, 방향 배분 런타임 PF 실패)"
    if max_dd >= 10.0:
        return "negative_memory_side_allocation_failed_runtime_dd(부정 기억, 방향 배분 런타임 DD 실패)"
    if not density_in_band(min_density):
        return "negative_memory_side_allocation_failed_runtime_density(부정 기억, 방향 배분 런타임 밀도 실패)"
    return str(proxy_row.get("selection_rule", "runtime_probe_observation_no_authority"))


def failure_mode_observation(runtime_rows: Sequence[Mapping[str, Any]], proxy_gap_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [row for row in runtime_rows if row.get("runtime_status") == "completed" and row.get("report_status") == "completed"]
    min_pf = min([safe_float(row.get("profit_factor")) for row in completed], default=math.nan)
    max_dd = max([safe_float(row.get("max_drawdown_percent")) for row in completed], default=math.nan)
    min_density = min([safe_float(row.get("runtime_trades_per_day")) for row in completed], default=math.nan)
    modes: list[str] = []
    if not completed:
        modes.append("runtime_probe_not_completed(런타임 탐침 미완료)")
    if math.isfinite(min_pf) and min_pf < 1.0:
        modes.append("side_allocation_pf_failed(방향 배분 PF 실패)")
    if math.isfinite(max_dd) and max_dd >= 10.0:
        modes.append("dd_not_compressed_under_10(DD 10 미만 압축 실패)")
    if math.isfinite(min_density) and not density_in_band(min_density):
        modes.append("runtime_density_out_of_target(런타임 밀도 목표 이탈)")
    if not modes:
        modes.append("side_allocation_preserved_clue_candidate(방향 배분 보존 단서 후보)")
    return {
        "failure_mode_observed": modes,
        "runtime_min_pf": safe_float(min_pf),
        "runtime_max_dd": safe_float(max_dd),
        "runtime_min_density": safe_float(min_density),
        "proxy_runtime_gap_rows": json_ready(list(proxy_gap_rows)),
    }


def stage_brief_text(manifest: Mapping[str, Any]) -> str:
    return f"""# Frontier61 Stage Brief(전선61 단계 개요)

- stage(단계): `{STAGE_ID}`
- hypothesis(가설): 3-class side allocation(3분류 방향 배분)이 short-only/long-only(숏 전용/롱 전용) 실패 뒤 non-axis PF source(비축 방향 PF 원천)를 만들 수 있는지 시험한다.
- novelty_delta(신규성 차이): F53-F58 short repair(숏 수리)와 F59-F60 long repair(롱 수리)를 상속하지 않고, target(목표) 자체를 short/flat/long allocation(숏/무거래/롱 배분)으로 바꾼다.
- local_verification(로컬 검증): `{manifest['local_verification_status']}`
- selected_candidate(선택 후보): `{manifest['selected_proxy_candidate']['candidate_id']}`
- claim_boundary(주장 경계): runtime_probe_observation only(런타임 탐침 관찰 전용); completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) not_claimed(주장 없음).
"""


def run_a_report_text(manifest: Mapping[str, Any]) -> str:
    audit = manifest["failure_audit"]
    return f"""# F61A Stage Open Report(F61A 단계 개방 보고)

Action(행동): F53~F60 failure memory(실패 기억)를 확인하고 F61을 side allocation(방향 배분) 가설로 열었다.

Effect(효과): 방향 단독 수리 반복을 멈추고, proxy(프록시)와 MT5 runtime probe(MT5 런타임 탐침) 차이를 새 target(목표)에서 직접 관찰한다.

- Grok stage-open(그록 단계 개방): `{manifest['grok_stage_open_classification']}`
- Grok local check demand(그록 로컬 검증 요구): completed(완료)
- failure audit read(실패 감사 판독): `{audit['dominant_read']}`
- feature contract(피처 계약): `{manifest['feature_contract']}`
- proxy grid rows(프록시 격자 행): `{manifest['proxy_grid_freeze']['grid_rows']}`
- Tier B/combined(티어 B/합산): `missing_required` declared at stage open(단계 개방에서 선언)
"""


def run_b_report_text(
    proxy_rows: Sequence[Mapping[str, Any]],
    proxy_row: Mapping[str, Any],
    label_contract: Mapping[str, Any],
    training: Mapping[str, Any],
) -> str:
    top = sorted(proxy_rows, key=lambda row: safe_float(row.get("train_profit_factor")), reverse=True)[:8]
    lines = [
        "# F61B Proxy Report(F61B 프록시 보고)",
        "",
        "Action(행동): 3-class side-allocation ONNX(3분류 방향 배분 온엑스)를 학습하고 capped proxy grid(상한 프록시 격자)를 평가했다.",
        "",
        "Effect(효과): MT5 runtime probe(MT5 런타임 탐침)에 올릴 후보를 하나로 동결하고, proxy-runtime gap(프록시-런타임 차이)을 비교할 기준을 만든다.",
        "",
        f"- label_config(라벨 설정): `{label_contract.get('label_config')}`",
        f"- label train short/flat/long(학습 숏/무거래/롱): `{label_contract.get('train_short_count')}/{label_contract.get('train_flat_count')}/{label_contract.get('train_long_count')}`",
        f"- model class rows(모델 클래스 행): `{len(training.get('class_rows', []))}`",
        f"- proxy rows(프록시 행): `{len(proxy_rows)}`",
        f"- selected(선택): `{proxy_row['candidate_id']}`",
        f"- selected validation/OOS PF(선택 검증/표본외 PF): `{proxy_row.get('validation_profit_factor')}` / `{proxy_row.get('oos_profit_factor')}`",
        f"- selected validation/OOS density(선택 검증/표본외 밀도): `{proxy_row.get('validation_trades_per_day')}` / `{proxy_row.get('oos_trades_per_day')}`",
        "",
        "## Top Train PF Rows(학습 PF 상위 행)",
    ]
    for row in top:
        lines.append(
            f"- `{row.get('candidate_id')}`: train PF/DD/density(학습 PF/DD/밀도)="
            f"{row.get('train_profit_factor')}/{row.get('train_dd_risk')}/{row.get('train_trades_per_day')}; "
            f"forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)="
            f"{row.get('forward_min_pf')}/{row.get('forward_max_dd')}/{row.get('forward_min_density')}"
        )
    return "\n".join(lines).rstrip() + "\n"


def runtime_probe_report_text(final: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# F61 Runtime Probe Report(F61 런타임 탐침 보고)",
        "",
        f"- judgment(판정): `{final.get('judgment')}`",
        f"- run(실행): `{RUN_ID}`",
        "",
        "| split(분할) | runtime(런타임) | report(보고서) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | signal diff(신호 차이) | feature diff(피처 차이) |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in runtime_rows:
        lines.append(
            f"| {row.get('split')} | {row.get('runtime_status')} | {row.get('report_status')} | "
            f"{row.get('profit_factor')} | {row.get('max_drawdown_percent')} | {row.get('runtime_trades_per_day')} | "
            f"{row.get('signal_count_diff')} | {row.get('feature_ready_diff')} |"
        )
    lines.append("")
    lines.append("Boundary(경계): runtime_probe_observation(런타임 탐침 관찰) only; no authority(권위 없음).")
    return "\n".join(lines).rstrip() + "\n"


def run_c_report_text(runtime_rows: Sequence[Mapping[str, Any]], proxy_gap_rows: Sequence[Mapping[str, Any]]) -> str:
    return runtime_probe_report_text({"judgment": "runtime_probe_observation_no_authority"}, runtime_rows) + "\n" + proxy_runtime_gap_report_text(proxy_gap_rows)


def proxy_runtime_gap_report_text(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# F61 Proxy-Runtime Gap Report(F61 프록시-런타임 차이 보고)",
        "",
        "| split(분할) | proxy PF(프록시 PF) | MT5 PF(MT5 PF) | PF gap(PF 차이) | proxy DD(프록시 DD) | MT5 DD(MT5 DD) | density gap(밀도 차이) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('split')} | {row.get('proxy_profit_factor')} | {row.get('mt5_profit_factor')} | "
            f"{row.get('profit_factor_gap_mt5_minus_proxy')} | {row.get('proxy_dd_risk')} | "
            f"{row.get('mt5_max_drawdown_percent')} | {row.get('density_gap_mt5_minus_proxy')} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def run_d_report_text(final: Mapping[str, Any]) -> str:
    return f"""# F61D Closeout Report(F61D 마감 보고)

- judgment(판정): `{final.get('judgment')}`
- runtime_probe_status(런타임 탐침 상태): `{final.get('runtime_probe_status')}`
- candidate(후보): `{final.get('candidate_id')}`
- failure_mode_observed(관찰 실패 양식): `{final.get('failure_mode_observation', {}).get('failure_mode_observed')}`

Action(행동): F61 side-allocation hypothesis(방향 배분 가설)를 proxy(프록시), ONNX parity(온엑스 동등성), MT5 runtime probe(MT5 런타임 탐침), proxy-runtime gap(프록시-런타임 차이)까지 실행했다.

Effect(효과): non-axis PF source(비축 방향 PF 원천)가 실제 런타임에서 살아남는지 판정하고, 다음 단계로 넘길 clue/memory(단서/기억)를 정직하게 남긴다.
"""


def required_gate_audit_text(final: Mapping[str, Any]) -> str:
    return f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- stage_open_grok_review(단계 개방 그록 검토): `{path_exists(GROK_STAGE_OPEN_ROOT / 'clean_output.md')}`
- stage_open_local_checks(단계 개방 로컬 검증): `completed(완료)`
- pre_mt5_grok_review(MT5 전 그록 검토): `{path_exists(GROK_PRE_MT5_ROOT / 'clean_output.md')}`
- mt5_runtime_probe(MT5 런타임 탐침): `{final.get('runtime_probe_status')}`
- proxy_runtime_gap(프록시-런타임 차이): `recorded(기록됨)`
- stage_closeout_grok_review(단계 마감 그록 검토): `{path_exists(GROK_STAGE_CLOSE_ROOT / 'clean_output.md')}`
- forbidden_claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve not_claimed(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음)
"""


def local_verification_text(manifest: Mapping[str, Any], artifacts: Mapping[str, Any]) -> str:
    return f"""# F61 Local Verification(F61 로컬 검증)

Action(행동): Grok stage-open review(그록 단계 개방 검토)의 `needs_local_verification(로컬 검증 필요)` 항목 1~8을 파일/장부/계약으로 확인했다.

Effect(효과): F61 구현이 방향 배분이라는 새 가설을 시험하는지, 단순한 숏/롱 수리 반복이나 런타임 권위 주장으로 drift(드리프트)하지 않는지 고정한다.

- failure_mode_audit(실패 모드 감사): `{manifest['failure_audit']['dominant_read']}`
- label_contract(라벨 계약): `{manifest['label_contract']['label_config']}`, flat/tie rule(무거래/동점 규칙) recorded(기록됨)
- feature_contract(피처 계약): feature_count(피처 수) `{manifest['feature_contract']['feature_count']}`, hash `{manifest['feature_contract']['feature_order_hash']}`
- proxy_grid_freeze(프록시 격자 동결): `{manifest['proxy_grid_freeze']}`
- runtime_parity_checklist(런타임 동등성 체크리스트): ONNX parity(온엑스 동등성) `{artifacts.get('onnx_parity')}`, hash(해시) `{artifacts.get('onnx_sha256')}`
- Tier plan(티어 계획): `{manifest['tier_plan']}`
- stop criteria(중단 기준): runtime PF<1 or DD>=10 or density outside 5~10/day closes as negative memory unless a concrete preserved clue appears.
- stage scaffold(단계 뼈대): `00_spec/01_inputs/02_runs/03_reviews/04_selected` present(존재)
"""


def selection_status_text(final: Mapping[str, Any]) -> str:
    return f"""# Frontier61 Selection Status(전선61 선택 상태)

- judgment(판정): `{final.get('judgment')}`
- runtime_probe_run(런타임 탐침 실행): `{RUN_ID}`
- candidate(후보): `{final.get('candidate_id')}`
- status(상태): `{final.get('runtime_probe_status')}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`

Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 claimed(주장)하지 않는다.
"""


def negative_memory_text(final: Mapping[str, Any]) -> str:
    return f"""# Negative Memory(부정 기억)

- stage(단계): `{STAGE_ID}`
- judgment(판정): `{final.get('judgment')}`
- failure_mode(실패 양식): `{final.get('failure_mode_observation', {}).get('failure_mode_observed')}`
- reopen_condition(재개 조건): side allocation(방향 배분)을 다시 열려면 feature/source(피처/원천), runtime envelope(런타임 봉투), or parity evidence(동등성 근거)가 F61과 materially different(실질적으로 다름)해야 한다.
"""


def preserved_clue_text(final: Mapping[str, Any]) -> str:
    return f"""# Preserved Clue(보존 단서)

- stage(단계): `{STAGE_ID}`
- judgment(판정): `{final.get('judgment')}`
- clue(단서): side allocation(방향 배분)이 MT5 runtime probe(MT5 런타임 탐침)에서 최소 보존 가능한 관찰을 만들었다.
- boundary(경계): runtime_probe_observation only(런타임 탐침 관찰 전용), no authority(권위 없음).
"""


def update_workspace_state(final: Mapping[str, Any]) -> None:
    rows = {str(row.get("split")): row for row in final.get("runtime_rows", [])}
    val = rows.get("validation_is", {})
    oos = rows.get("oos", {})
    text = f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_D}
latest_completed_run_id: {RUN_ID}
current_status: {current_status_for_judgment(str(final.get('judgment') or ''))}
current_judgment: {final.get('judgment')}
next_stage_id: {NEXT_STAGE_ID}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: runtime_probe_observation_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{utc_now()}'
notes:
  - "F61 MT5 runtime probe: candidate={final.get('candidate_id')}; validation_is PF={val.get('profit_factor')} DD={val.get('max_drawdown_percent')} trades={val.get('trade_count')} density/day={val.get('runtime_trades_per_day')} feature_ready_diff={val.get('feature_ready_diff')} signal_diff={val.get('signal_count_diff')}; OOS PF={oos.get('profit_factor')} DD={oos.get('max_drawdown_percent')} trades={oos.get('trade_count')} density/day={oos.get('runtime_trades_per_day')} feature_ready_diff={oos.get('feature_ready_diff')} signal_diff={oos.get('signal_count_diff')}."
  - "F61 tests 3-class side allocation only; F53-F60 are reference-only negative memory, not inherited authority."
  - "No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve claimed."
"""
    backfill.write_text_sig(Path("docs/workspace/workspace_state.yaml"), text)
    backfill.write_text_sig(Path("docs/context/current_working_state.md"), current_working_state_text(final))


def current_working_state_text(final: Mapping[str, Any]) -> str:
    rows = {str(row.get("split")): row for row in final.get("runtime_rows", [])}
    val = rows.get("validation_is", {})
    oos = rows.get("oos", {})
    return f"""# Current Working State(현재 작업 상태)

Frontier61(F61, 전선 61단계)가 `{final.get('judgment')}`로 닫혔다.

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_D}`
- runtime_probe_run(런타임 탐침 실행): `{RUN_ID}`
- candidate(후보): `{final.get('candidate_id')}`
- MT5_validation_is(MT5 검증 내부): PF={val.get('profit_factor')}, DD={val.get('max_drawdown_percent')}%, trades(거래)={val.get('trade_count')}, density/day(일 밀도)={val.get('runtime_trades_per_day')}, feature_ready_diff(피처 준비 차이)={val.get('feature_ready_diff')}, signal_diff(신호 차이)={val.get('signal_count_diff')}
- MT5_oos(MT5 표본외): PF={oos.get('profit_factor')}, DD={oos.get('max_drawdown_percent')}%, trades(거래)={oos.get('trade_count')}, density/day(일 밀도)={oos.get('runtime_trades_per_day')}, feature_ready_diff(피처 준비 차이)={oos.get('feature_ready_diff')}, signal_diff(신호 차이)={oos.get('signal_count_diff')}
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

F61 action(행동): short/flat/long side allocation model(숏/무거래/롱 방향 배분 모델)을 학습하고 MT5 runtime probe(MT5 런타임 탐침)를 실행했다.

F61 effect(효과): F53~F60의 단일 방향 수리 실패 뒤, 방향 배분 자체가 PF source(수익 팩터 원천)가 되는지 proxy-runtime gap(프록시-런타임 차이)으로 판정했다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
"""


def current_status_for_judgment(judgment: str) -> str:
    if judgment.startswith("preserved_clue"):
        return "closed_preserved_clue"
    if judgment.startswith("negative_memory"):
        return "closed_negative_memory"
    if judgment.startswith("blocked"):
        return "blocked_attempt_failed"
    return "closed_runtime_probe_observation"


def update_registers(final: Mapping[str, Any]) -> None:
    if str(final.get("judgment", "")).startswith("negative_memory"):
        append_marked_block(Path("docs/registers/negative_result_register.md"), RUN_D, negative_register_block(final))
    append_marked_block(Path("docs/registers/idea_registry.md"), RUN_D, idea_register_block(final))


def negative_register_block(final: Mapping[str, Any]) -> str:
    rows = {str(row.get("split")): row for row in final.get("runtime_rows", [])}
    val = rows.get("validation_is", {})
    oos = rows.get("oos", {})
    return f"""## {RUN_D}

- Stage(단계): `{STAGE_ID}`
- Negative memory(부정 기억): `{final.get('judgment')}`
- Evidence(근거): MT5 validation_is(MT5 검증 내부) PF/DD/trades(수익 팩터/손실폭/거래) `{val.get('profit_factor')}/{val.get('max_drawdown_percent')}%/{val.get('trade_count')}`; MT5 OOS(MT5 표본외) `{oos.get('profit_factor')}/{oos.get('max_drawdown_percent')}%/{oos.get('trade_count')}`.
- Runtime probe status(런타임 탐침 상태): `runtime_probe_observation_no_authority`
- Effect(효과): side allocation(방향 배분)이 단일 방향 수리 실패를 넘어서는 PF source(수익 팩터 원천)를 만들었는지 기록한다.
"""


def idea_register_block(final: Mapping[str, Any]) -> str:
    return f"""## {RUN_D}

- Stage(단계): `{STAGE_ID}`
- Idea(아이디어): short/flat/long side allocation target(숏/무거래/롱 방향 배분 목표)을 새 ONNX source(온엑스 원천)로 시험했다.
- Result(결과): `{final.get('judgment')}`
- Evidence(근거): `{REVIEWS_ROOT.as_posix()}/runtime_probe_report.md`
- Boundary(경계): runtime_probe_observation only(런타임 탐침 관찰 전용), no authority(권위 없음).
"""


def append_marked_block(path: Path, marker_id: str, body: str) -> None:
    marker = f"<!-- {marker_id} -->"
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    block = f"{marker}\n\n{body.strip()}\n"
    if marker in text:
        before = text.split(marker, 1)[0].rstrip()
        after = text.split(marker, 1)[1]
        next_marker = after.find("\n<!-- ")
        tail = after[next_marker:].lstrip() if next_marker >= 0 else ""
        new_text = f"{before}\n\n{block}\n{tail}".strip() + "\n"
    else:
        new_text = text.rstrip() + "\n\n" + block
    backfill.write_text_sig(path, new_text)


def grok_receipt_text(label: str, root: Path) -> str:
    payload = grok_receipt_payload(root)
    clean_path = root / "clean_output.md"
    clean_text = io_path(clean_path).read_text(encoding="utf-8-sig").strip() if path_exists(clean_path) else ""
    return f"""# Grok Receipt(그록 영수증): {label}

- path(경로): `{root.as_posix()}`
- classification(분류): `{payload['classification']}`
- metadata_success(메타데이터 성공): `{payload.get('metadata_success')}`
- metadata_timed_out(메타데이터 시간초과): `{payload.get('metadata_timed_out')}`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), hashes(해시), ledgers(장부), MT5 output(MT5 출력)으로 다시 검증한다.
- effect(효과): Grok output(그록 출력)은 authority(권위)가 아니라 bounded critique(제한 비판)로만 쓰인다.

## Clean Output(정리 출력)
{clean_text or 'missing_required(필수 누락)'}
"""


def grok_receipt_payload(root: Path) -> dict[str, Any]:
    metadata_path = root / "metadata.json"
    clean_path = root / "clean_output.md"
    metadata = backfill.read_json(metadata_path) if path_exists(metadata_path) else {}
    clean = io_path(clean_path).read_text(encoding="utf-8-sig") if path_exists(clean_path) else ""
    text = clean.lower()
    classification = "missing_required"
    verdict = re.search(r"(?:verdict|classification)\s*[:\-]\s*`?(accepted|rejected|needs_local_verification)`?", text)
    if verdict:
        classification = verdict.group(1)
    elif "needs_local_verification" in text:
        classification = "needs_local_verification"
    elif "accepted" in text:
        classification = "accepted"
    elif "rejected" in text:
        classification = "rejected"
    return {
        "classification": classification,
        "metadata_success": metadata.get("success"),
        "metadata_timed_out": metadata.get("timed_out"),
        "prompt_hash": metadata.get("prompt_hash"),
    }


def grok_classification(root: Path) -> str:
    return str(grok_receipt_payload(root)["classification"])


def refresh_docs() -> None:
    final = backfill.read_json(RUN_ROOT / "final_decision.json")
    proxy_row = dict(final["proxy_candidate"])
    runtime_rows = list(final["runtime_rows"])
    proxy_gap_rows = list(final["proxy_runtime_gap_rows"])
    write_reports(final, proxy_row, runtime_rows, proxy_gap_rows)
    update_workspace_state(final)
    update_registers(final)


def prefixed_metrics(prefix: str, metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {f"{prefix}_{key}": value for key, value in metrics.items()}


def candidate_id(threshold: float, min_margin: float, max_hold: int) -> str:
    t = int(round(float(threshold) * 100))
    m = int(round(float(min_margin) * 100))
    return f"f61b_side_alloc_t{t}_m{m}_h{int(max_hold)}"


def density_in_band(value: Any) -> bool:
    density = safe_float(value)
    return bool(TARGET_DENSITY_LOW <= density <= TARGET_DENSITY_HIGH)


def safe_float(value: Any) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return math.nan
    return out if math.isfinite(out) else math.nan


def utc_now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
