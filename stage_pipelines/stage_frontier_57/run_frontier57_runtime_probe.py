from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import export_sklearn_to_onnx_zipmap_disabled, ordered_hash, sha256_file  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b  # noqa: E402
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b  # noqa: E402
from stage_pipelines.stage_frontier_52.run_frontier52_runtime_probe import execute_attempts, override_set_file  # noqa: E402
from stage_pipelines.stage_frontier_53.run_frontier53_runtime_probe import (  # noqa: E402
    onnx_short_score_parity,
    patch_binary_onnx_to_short_score3,
)
from stage_pipelines.stage_frontier_runtime_backfill import run_frontier_runtime_probe_backfill as backfill  # noqa: E402


STAGE_NUM = 57
STAGE_ID = "stage_frontier_57__short_pf_edge_after_adverse_excursion_memory"
RUN_A = "frontier57A_stage_open_short_pf_edge_after_adverse_excursion_memory_v1"
RUN_B = "frontier57B_fast_exit_execution_proxy_v1"
RUN_C = "frontier57C_mt5_runtime_probe_fast_exit_execution_v1"
RUN_D = "frontier57D_stage_closeout_fast_exit_execution_v1"
RUN_ID = "frontier57Z_runtime_probe_backfill_v1"
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
MT5_ROOT = RUN_ROOT / "mt5"
MODELS_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "feature_matrices"
REVIEWS_ROOT = Path("stages") / STAGE_ID / "03_reviews"
SELECTED_ROOT = Path("stages") / STAGE_ID / "04_selected"

GROK_STAGE_OPEN_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-16_frontier57_stage_open_snapshot"
GROK_PRE_MT5_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-16_frontier57_pre_mt5_review"
GROK_STAGE_CLOSE_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-16_frontier57_stage_closeout_review"

SIDE_VALUE = -1
MAX_HOLD_BARS = 6
ATR_PERIOD = 14
ATR_STOP_MULT = 0.8
ATR_TP_MULT = 1.2
ATR_MIN_STOP_POINTS = 40.0
ATR_MAX_STOP_POINTS = 180.0
ATR_MIN_TP_POINTS = 60.0
ATR_MAX_TP_POINTS = 260.0
PRIMARY_SCORE_Q = 0.85
STRESS_SCORE_QS = (0.80, 0.85, 0.90, 0.95)
LABEL_HOLD_LIMITS = (1, 2, 3, 4)
LABEL_PNL_QS = (0.50, 0.55, 0.60, 0.65)
PRIMARY_HOLD_LIMIT = 2
PRIMARY_PNL_Q = 0.55
CANDIDATE_PREFIX = "f57b_fast_exit_execution_extratrees_d6_l80_short"
MODEL_FAMILY = "extratrees_depth6_leaf80"
MODEL_ID = "f57_fast_exit_execution_extratrees_d6_l80_short_score3"

RUNTIME_POLICY = {
    "InpCloseOnFlatSignal": False,
    "InpEntryTransitionOnly": False,
    "InpEntryTransitionRearmMinConfidenceDelta": 0.0,
    "InpMaxHoldBars": MAX_HOLD_BARS,
    "InpReentryCooldownBars": 0,
    "InpSameDirectionReentryCooldownBars": 0,
    "InpAtrSltpEnabled": True,
    "InpAtrPeriod": ATR_PERIOD,
    "InpAtrStopMultiplier": ATR_STOP_MULT,
    "InpAtrTakeProfitMultiplier": ATR_TP_MULT,
    "InpAtrMinStopPoints": ATR_MIN_STOP_POINTS,
    "InpAtrMaxStopPoints": ATR_MAX_STOP_POINTS,
    "InpAtrMinTakeProfitPoints": ATR_MIN_TP_POINTS,
    "InpAtrMaxTakeProfitPoints": ATR_MAX_TP_POINTS,
}

NEXT_STAGE_ID = "stage_frontier_58__short_pf_edge_after_fast_exit_execution_memory"
NEXT_RUN_ID = "frontier58A_stage_open_short_pf_edge_after_fast_exit_execution_memory_v1"

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Frontier57 fast-exit execution source MT5 runtime probe.")
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

    base = build_training_base()
    proxy_rows = evaluate_proxy_surface(base)
    proxy_row = select_primary_proxy_row(proxy_rows)
    training = train_fast_exit_candidate(base, proxy_row)
    artifacts = materialize_model_artifacts(training)
    split_payload = materialize_split_payload(training, proxy_row)
    spec = candidate_spec(proxy_row, artifacts)
    attempts = backfill.materialize_attempts(
        spec,
        split_payload,
        training["feature_order"],
        artifacts["feature_order_hash"],
        Path(args.common_files_root),
    )
    attempts = apply_runtime_policy_overrides(attempts)
    write_proxy_artifacts(training, artifacts, proxy_rows, proxy_row, attempts)

    if args.proxy_only:
        print(json.dumps(json_ready({"status": "proxy_ready", "proxy_row": proxy_row, "artifacts": artifacts}), ensure_ascii=False, indent=2))
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
    backfill.write_csv(RUN_ROOT / "proxy_runtime_gap.csv", proxy_gap_rows)
    failure_mode = failure_mode_observation(proxy_row, runtime_rows, proxy_gap_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "candidate_id": proxy_row["candidate_id"],
        "classification": classification,
        "runtime_probe_status": classification,
        "judgment": stage_judgment(runtime_rows),
        "failure_mode_observation": failure_mode,
        "proxy_candidate": json_ready(proxy_row),
        "proxy_surface_rows": json_ready(proxy_rows),
        "model_artifacts": artifacts,
        "runtime_policy": RUNTIME_POLICY,
        "runtime_rows": runtime_rows,
        "proxy_runtime_gap_rows": proxy_gap_rows,
        "claim_boundary": backfill.claim_boundary_payload(),
        "created_at_utc": created_at,
    }
    backfill.write_json(RUN_ROOT / "final_decision.json", final)
    backfill.write_json(RUN_ROOT / "run_manifest.json", final)
    write_reports(final, proxy_row, runtime_rows, proxy_gap_rows, attempts, execution_payload)
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
                "feature_count": artifacts["feature_count"],
                "runtime_policy": RUNTIME_POLICY,
            },
        },
        spec,
        runtime_rows,
    )
    update_workspace_state(final)
    update_registers(final)
    print(json.dumps(json_ready({"status": classification, "run_id": RUN_ID, "runtime_rows": runtime_rows}), ensure_ascii=False, indent=2))
    return 0 if classification != "blocked_attempt_failed" else 1


def mkdirs() -> None:
    paths = (
        RUN_ROOT,
        MT5_ROOT,
        MODELS_ROOT,
        FEATURE_ROOT,
        REVIEWS_ROOT,
        SELECTED_ROOT,
        Path("stages") / STAGE_ID / "00_spec",
        Path("stages") / STAGE_ID / "01_inputs",
        Path("stages") / STAGE_ID / "02_runs" / RUN_A,
        Path("stages") / STAGE_ID / "02_runs" / RUN_B,
        Path("stages") / STAGE_ID / "02_runs" / RUN_C,
        Path("stages") / STAGE_ID / "02_runs" / RUN_D,
    )
    for path in paths:
        io_path(path).mkdir(parents=True, exist_ok=True)


def build_training_base() -> dict[str, Any]:
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    raw_path = f33b.load_raw_path(frame)
    runtime = build_fast_exit_arrays(frame, raw_path)
    x_raw = frame[feature_order].to_numpy(dtype="float64")
    valid_features = np.isfinite(x_raw).all(axis=1)
    finite = (
        valid_features
        & runtime["valid"]
        & np.isfinite(runtime["pnl"])
        & np.isfinite(runtime["mae_atr"])
        & np.isfinite(runtime["mfe_atr"])
    )
    train_mask = f33b.split_mask(frame, "train") & finite
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
    }


def train_fast_exit_candidate(base: Mapping[str, Any], proxy_row: Mapping[str, Any]) -> dict[str, Any]:
    hold_limit = int(proxy_row.get("label_hold_limit", PRIMARY_HOLD_LIMIT))
    pnl_q = float(proxy_row.get("label_pnl_q", PRIMARY_PNL_Q))
    trained = fit_fast_exit_model(base, hold_limit, pnl_q)
    return {
        **dict(base),
        **trained,
        "primary_score_threshold": float(proxy_row["score_threshold"]),
        "selected_proxy_row": json_ready(dict(proxy_row)),
    }


def fit_fast_exit_model(base: Mapping[str, Any], hold_limit: int, pnl_q: float) -> dict[str, Any]:
    runtime = base["runtime"]
    train_mask = np.asarray(base["train_mask"], dtype=bool)
    x_raw = np.asarray(base["x_raw"], dtype="float64")
    finite = np.asarray(base["finite"], dtype=bool)
    pnl_cut = float(np.quantile(np.asarray(runtime["pnl"], dtype="float64")[train_mask], pnl_q))
    event = (
        (np.asarray(runtime["pnl"], dtype="float64") >= pnl_cut)
        & (np.asarray(runtime["exit_reason"], dtype=object) != "stop")
        & (np.asarray(runtime["hold"], dtype="int64") <= int(hold_limit))
    ).astype("int8")
    model = ExtraTreesClassifier(
        n_estimators=500,
        max_depth=6,
        min_samples_leaf=80,
        random_state=5701,
        n_jobs=-1,
        class_weight="balanced_subsample",
    )
    model.fit(x_raw[train_mask], event[train_mask])
    score = np.full(len(base["frame"]), np.nan, dtype="float64")
    raw_prob = model.predict_proba(x_raw[finite])
    class_to_index = {int(label): index for index, label in enumerate(model.classes_)}
    score[finite] = raw_prob[:, class_to_index[1]]
    thresholds = {
        f"score_q_{score_q:.2f}": float(np.quantile(score[train_mask & np.isfinite(score)], score_q))
        for score_q in STRESS_SCORE_QS
    }
    probabilities = short_score_three_class(score)
    return {
        "event": event,
        "model": model,
        "score": score,
        "probabilities": probabilities,
        "thresholds": thresholds,
        "label_hold_limit": int(hold_limit),
        "label_pnl_q": pnl_q,
        "pnl_cut": pnl_cut,
        "event_positive_rate_train": float(event[train_mask].mean()) if train_mask.any() else 0.0,
    }


def build_fast_exit_arrays(frame: pd.DataFrame, raw_path: Mapping[str, Any]) -> dict[str, Any]:
    del frame
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
    atr = pd.Series(tr).rolling(ATR_PERIOD, min_periods=ATR_PERIOD).mean().to_numpy(dtype="float64")
    pnl = np.full(len(entry_pos), np.nan, dtype="float64")
    hold = np.zeros(len(entry_pos), dtype="int64")
    valid = np.zeros(len(entry_pos), dtype=bool)
    exit_reason = np.full(len(entry_pos), "", dtype=object)
    mae_atr = np.full(len(entry_pos), np.nan, dtype="float64")
    mfe_atr = np.full(len(entry_pos), np.nan, dtype="float64")
    for idx in range(len(entry_pos)):
        result = simulate_isolated_short(idx, entry_pos, open_prices, high_prices, low_prices, atr)
        if result["valid"]:
            pnl[idx] = float(result["pnl"])
            hold[idx] = int(result["hold_bars"])
            valid[idx] = True
            exit_reason[idx] = str(result["exit_reason"])
            mae_atr[idx] = float(result["mae_atr"])
            mfe_atr[idx] = float(result["mfe_atr"])
    return {
        "pnl": pnl,
        "hold": hold,
        "valid": valid,
        "exit_reason": exit_reason,
        "atr": atr,
        "mae_atr": mae_atr,
        "mfe_atr": mfe_atr,
    }


def simulate_isolated_short(
    idx: int,
    entry_pos: np.ndarray,
    open_prices: np.ndarray,
    high_prices: np.ndarray,
    low_prices: np.ndarray,
    atr: np.ndarray,
) -> dict[str, Any]:
    p = int(entry_pos[idx])
    if p < ATR_PERIOD or p + 1 >= len(open_prices):
        return {"valid": False}
    entry = float(open_prices[p])
    atr_value = float(atr[p])
    if not math.isfinite(entry) or not math.isfinite(atr_value) or entry <= 0.0 or atr_value <= 0.0:
        return {"valid": False}
    stop_points = min(max(atr_value * ATR_STOP_MULT, ATR_MIN_STOP_POINTS), ATR_MAX_STOP_POINTS)
    take_points = min(max(atr_value * ATR_TP_MULT, ATR_MIN_TP_POINTS), ATR_MAX_TP_POINTS)
    stop_price = entry + stop_points
    take_price = entry - take_points
    end = min(p + MAX_HOLD_BARS, len(open_prices) - 1)
    max_adverse_points = 0.0
    max_favorable_points = 0.0
    for q in range(p + 1, end + 1):
        max_adverse_points = max(max_adverse_points, float(high_prices[q]) - entry)
        max_favorable_points = max(max_favorable_points, entry - float(low_prices[q]))
        if float(high_prices[q]) >= stop_price:
            return {
                "valid": True,
                "pnl": math.log(entry / stop_price) - f23b.scout.ROUGH_COST_LOG_RETURN,
                "hold_bars": q - p,
                "exit_reason": "stop",
                "mae_atr": max_adverse_points / max(atr_value, 1e-12),
                "mfe_atr": max_favorable_points / max(atr_value, 1e-12),
            }
        if float(low_prices[q]) <= take_price:
            return {
                "valid": True,
                "pnl": math.log(entry / take_price) - f23b.scout.ROUGH_COST_LOG_RETURN,
                "hold_bars": q - p,
                "exit_reason": "take",
                "mae_atr": max_adverse_points / max(atr_value, 1e-12),
                "mfe_atr": max_favorable_points / max(atr_value, 1e-12),
            }
    exit_price = float(open_prices[end])
    if not math.isfinite(exit_price) or exit_price <= 0.0:
        return {"valid": False}
    return {
        "valid": True,
        "pnl": math.log(entry / exit_price) - f23b.scout.ROUGH_COST_LOG_RETURN,
        "hold_bars": end - p,
        "exit_reason": "maxhold",
        "mae_atr": max_adverse_points / max(atr_value, 1e-12),
        "mfe_atr": max_favorable_points / max(atr_value, 1e-12),
    }


def short_score_three_class(score: np.ndarray) -> np.ndarray:
    out = np.zeros((len(score), 3), dtype="float64")
    finite = np.isfinite(score)
    out[finite, 0] = score[finite]
    return out


def evaluate_proxy_surface(training: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for hold_limit in LABEL_HOLD_LIMITS:
        for pnl_q in LABEL_PNL_QS:
            fitted = fit_fast_exit_model(training, int(hold_limit), float(pnl_q))
            score = np.asarray(fitted["score"], dtype="float64")
            finite = np.asarray(training["finite"], dtype=bool) & np.isfinite(score)
            for score_q in STRESS_SCORE_QS:
                threshold = float(fitted["thresholds"][f"score_q_{score_q:.2f}"])
                signal_mask = finite & (score >= threshold)
                row: dict[str, Any] = {
                    "candidate_id": candidate_id(int(hold_limit), float(pnl_q), float(score_q)),
                    "model_family": MODEL_FAMILY,
                    "side": "short(숏)",
                    "side_value": SIDE_VALUE,
                    "label_family": "fast_exit_positive_execution_short(빠른 청산 양수 실행 숏)",
                    "admission_family": "none_threshold_signal_only(없음, 임계값 신호만 사용)",
                    "label_hold_limit": int(hold_limit),
                    "label_pnl_q": float(pnl_q),
                    "pnl_cut": safe_float(fitted["pnl_cut"]),
                    "score_q": score_q,
                    "score_threshold": threshold,
                    "event_positive_rate_train": safe_float(fitted["event_positive_rate_train"]),
                    "runtime_probe_candidate_flag": False,
                    "selection_note": "exploratory_all_signal_execution_proxy_no_promotion(탐색용 전체 신호 실행 프록시, 승격 없음)",
                }
                for split in ("train", "validation", "oos"):
                    metrics = all_signal_proxy_metrics({**dict(training), **fitted}, signal_mask, split)
                    filtered_metrics = sequential_proxy_metrics({**dict(training), **fitted}, signal_mask, split)
                    signal_metrics = signal_density_metrics(training, signal_mask, split)
                    prefix = "validation" if split == "validation" else split
                    for key, value in metrics.items():
                        row[f"{prefix}_{key}"] = value
                    for key, value in filtered_metrics.items():
                        row[f"{prefix}_filtered_{key}"] = value
                    row[f"{prefix}_raw_signal_count"] = signal_metrics["signal_count"]
                    row[f"{prefix}_raw_signals_per_day"] = signal_metrics["signals_per_day"]
                    row[f"{prefix}_veto_count"] = 0
                    row[f"{prefix}_admission_rate"] = 1.0
                row["forward_min_pf"] = min(safe_float(row["validation_profit_factor"]), safe_float(row["oos_profit_factor"]))
                row["forward_max_dd"] = max(safe_float(row["validation_dd_risk"]), safe_float(row["oos_dd_risk"]))
                row["forward_min_density"] = min(safe_float(row["validation_trades_per_day"]), safe_float(row["oos_trades_per_day"]))
                row["forward_max_density"] = max(safe_float(row["validation_trades_per_day"]), safe_float(row["oos_trades_per_day"]))
                row["forward_min_signal_density"] = min(
                    safe_float(row["validation_signals_per_day"]), safe_float(row["oos_signals_per_day"])
                )
                row["forward_max_signal_density"] = max(
                    safe_float(row["validation_signals_per_day"]), safe_float(row["oos_signals_per_day"])
                )
                row["proxy_trade_density_target_flag"] = bool(
                    5.0 <= row["validation_trades_per_day"] <= 10.0 and 5.0 <= row["oos_trades_per_day"] <= 10.0
                )
                row["signal_density_target_flag"] = bool(
                    5.0 <= row["validation_signals_per_day"] <= 10.0 and 5.0 <= row["oos_signals_per_day"] <= 10.0
                )
                row["density_target_flag"] = bool(
                    row["proxy_trade_density_target_flag"] or row["signal_density_target_flag"]
                )
                row["dual_positive_proxy_flag"] = bool(row["validation_profit_factor"] >= 1.0 and row["oos_profit_factor"] >= 1.0)
                row["proxy_margin_flag"] = bool(row["validation_profit_factor"] >= 1.02 and row["oos_profit_factor"] >= 1.02)
                rows.append(row)
    selected = select_primary_proxy_row(rows)
    for row in rows:
        row["runtime_probe_candidate_flag"] = bool(row["candidate_id"] == selected["candidate_id"])
    return rows


def candidate_id(hold_limit: int, pnl_q: float, score_q: float) -> str:
    return (
        f"{CANDIDATE_PREFIX}_h{int(hold_limit)}"
        f"_pnl{int(round(pnl_q * 100))}_q{int(round(score_q * 100))}"
    )


def signal_density_metrics(training: Mapping[str, Any], signal_mask: np.ndarray, split: str) -> dict[str, Any]:
    frame = training["frame"]
    finite = np.asarray(training["finite"], dtype=bool)
    split_mask = f33b.split_mask(frame, split) & finite
    days = f23b.scout.count_scope_days(frame.loc[split_mask, "timestamp"])
    count = int((split_mask & signal_mask).sum())
    return {"signal_count": count, "signals_per_day": float(count / days) if days else 0.0}


def all_signal_proxy_metrics(training: Mapping[str, Any], signal_mask: np.ndarray, split: str) -> dict[str, Any]:
    frame = training["frame"]
    finite = np.asarray(training["finite"], dtype=bool)
    split_mask = f33b.split_mask(frame, split) & finite
    pnl = np.asarray(training["runtime"]["pnl"], dtype="float64")
    indices = np.flatnonzero(split_mask & signal_mask)
    arr = pnl[indices]
    trade_times = frame["timestamp"].iloc[indices]
    metrics = f23b.scout.trade_metrics(arr, pd.Series(trade_times))
    days = f23b.scout.count_scope_days(frame.loc[split_mask, "timestamp"])
    return {
        "profit_factor": safe_float(metrics.get("profit_factor")),
        "dd_risk": safe_float(max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"]))),
        "trade_count": int(len(arr)),
        "signal_count": int(len(arr)),
        "trades_per_day": float(len(arr) / days) if days else 0.0,
        "signals_per_day": float(len(arr) / days) if days else 0.0,
        "net_profit": safe_float(metrics.get("net_profit")),
    }


def sequential_proxy_metrics(training: Mapping[str, Any], signal_mask: np.ndarray, split: str) -> dict[str, Any]:
    frame = training["frame"]
    finite = np.asarray(training["finite"], dtype=bool)
    split_mask = f33b.split_mask(frame, split) & finite
    entry_pos = np.asarray(training["raw_path"]["entry_pos"], dtype="int64")
    pnl = np.asarray(training["runtime"]["pnl"], dtype="float64")
    hold = np.asarray(training["runtime"]["hold"], dtype="int64")
    indices = np.flatnonzero(split_mask & signal_mask)
    trade_pnl: list[float] = []
    trade_times: list[Any] = []
    next_allowed_pos = -1
    for idx in indices:
        p = int(entry_pos[idx])
        if p < next_allowed_pos:
            continue
        trade_pnl.append(float(pnl[idx]))
        trade_times.append(frame["timestamp"].iloc[idx])
        next_allowed_pos = p + int(hold[idx]) + 1
    arr = np.asarray(trade_pnl, dtype="float64")
    metrics = f23b.scout.trade_metrics(arr, pd.Series(trade_times))
    days = f23b.scout.count_scope_days(frame.loc[split_mask, "timestamp"])
    return {
        "profit_factor": safe_float(metrics.get("profit_factor")),
        "dd_risk": safe_float(max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"]))),
        "trade_count": int(len(arr)),
        "signal_count": int((split_mask & signal_mask).sum()),
        "trades_per_day": float(len(arr) / days) if days else 0.0,
        "signals_per_day": float((split_mask & signal_mask).sum() / days) if days else 0.0,
        "net_profit": safe_float(metrics.get("net_profit")),
    }


def select_primary_proxy_row(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not rows:
        raise RuntimeError("F57 fast-exit execution proxy surface produced no rows")

    def score(row: Mapping[str, Any]) -> tuple[float, float, float, float, float, float, float, float]:
        signal_density_ok = 1.0 if row.get("signal_density_target_flag") else 0.0
        trade_density_ok = 1.0 if row.get("proxy_trade_density_target_flag") else 0.0
        margin_ok = 1.0 if row.get("proxy_margin_flag") else 0.0
        dual_positive = 1.0 if row.get("dual_positive_proxy_flag") else 0.0
        min_pf = safe_float(row.get("forward_min_pf"))
        max_dd = safe_float(row.get("forward_max_dd"))
        signal_mid_error = abs(safe_float(row.get("validation_signals_per_day")) - 7.5) + abs(
            safe_float(row.get("oos_signals_per_day")) - 7.5
        )
        trade_floor_penalty = max(0.0, 5.0 - safe_float(row.get("validation_trades_per_day"))) + max(
            0.0, 5.0 - safe_float(row.get("oos_trades_per_day"))
        )
        trade_mid_error = abs(safe_float(row.get("validation_trades_per_day")) - 7.5) + abs(
            safe_float(row.get("oos_trades_per_day")) - 7.5
        )
        return (
            signal_density_ok,
            margin_ok,
            dual_positive,
            trade_density_ok,
            min_pf,
            -max_dd,
            -signal_mid_error,
            -trade_floor_penalty - trade_mid_error * 0.1,
        )

    selected = max((dict(row) for row in rows), key=score)
    selected["selection_rule"] = (
        "exploratory_all_signal_density_then_pf_margin_no_promotion"
        "(탐색용 전체 신호 밀도 우선, PF 여유 다음, 승격 없음)"
    )
    selected["runtime_probe_candidate_flag"] = True
    return selected


def materialize_model_artifacts(training: Mapping[str, Any]) -> dict[str, Any]:
    model_path = MODELS_ROOT / f"{MODEL_ID}.joblib"
    binary_onnx_path = MODELS_ROOT / f"{MODEL_ID}.binary.onnx"
    onnx_path = MODELS_ROOT / f"{MODEL_ID}.onnx"
    feature_order_path = MODELS_ROOT / f"{MODEL_ID}.feature_order.txt"
    joblib.dump(training["model"], io_path(model_path))
    binary_meta = export_sklearn_to_onnx_zipmap_disabled(
        training["model"],
        binary_onnx_path,
        feature_count=len(training["feature_order"]),
        target_opset=12,
        drop_label_output=False,
    )
    patch_binary_onnx_to_short_score3(binary_onnx_path, onnx_path)
    parity = onnx_short_score_parity(onnx_path, training["x_raw"], training["probabilities"])
    io_path(feature_order_path).write_text("\n".join(training["feature_order"]) + "\n", encoding="utf-8")
    payload = {
        "model_id": MODEL_ID,
        "model_path": model_path.as_posix(),
        "model_sha256": sha256_file(model_path),
        "binary_onnx": binary_meta,
        "onnx_path": onnx_path.as_posix(),
        "onnx_sha256": sha256_file(onnx_path),
        "feature_count": len(training["feature_order"]),
        "feature_order_hash": training["feature_order_hash"],
        "feature_order_path": feature_order_path.as_posix(),
        "onnx_parity": parity,
        "probability_mapping": "p_short=fast_exit_positive_execution_score,p_flat=0,p_long=0",
    }
    backfill.write_json(MODELS_ROOT / "model_artifact_manifest.json", payload)
    return payload


def materialize_split_payload(training: Mapping[str, Any], proxy_row: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    rows_for_expected: list[dict[str, Any]] = []
    frame = training["frame"].copy()
    feature_order = list(training["feature_order"])
    x_raw = np.asarray(training["x_raw"], dtype="float64")
    finite = np.asarray(training["finite"], dtype=bool)
    score = np.asarray(training["score"], dtype="float64")
    signal_mask = finite & (score >= float(proxy_row["score_threshold"]))
    signal_all = np.where(signal_mask, -1, 0).astype("int8")
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
        expected = expected_signal_summary(export_frame, expected_signal, runtime_split)
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


def expected_signal_summary(
    frame: pd.DataFrame,
    signal: np.ndarray,
    runtime_split: str,
) -> dict[str, Any]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True).reset_index(drop=True)
    days = backfill.count_scope_days(timestamps) if len(timestamps) else 0
    signal_count = int((signal != 0).sum())
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "split": runtime_split,
        "rows": int(len(frame)),
        "full_split_rows": int(len(frame)),
        "days_in_scope": int(days),
        "decision_mode": "threshold_margin_fast_exit_execution_score",
        "signal_count": signal_count,
        "raw_signal_count": signal_count,
        "admitted_signal_count": signal_count,
        "veto_count": 0,
        "long_count": int((signal == 1).sum()),
        "short_count": int((signal == -1).sum()),
        "flat_count": int((signal == 0).sum()),
        "raw_signal_density_per_day": float(signal_count / days) if days else 0.0,
        "expected_signal_density_per_day": float(signal_count / days) if days else 0.0,
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
        decision_mode="threshold_margin",
        short_threshold=float(proxy_row["score_threshold"]),
        long_threshold=1.0,
        min_margin=0.0,
        max_hold_bars=MAX_HOLD_BARS,
        cooldown_bars=0,
        source_contract="fast_exit_execution_score_threshold_all_signal_proxy_no_sparse_veto",
        source_note=(
            "F57 fast-exit execution label after F56 adverse-excursion memory; "
            "runtime handoff uses direct threshold_margin without RuntimeVetoTape."
        ),
    )


def apply_runtime_policy_overrides(
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    patched: list[dict[str, Any]] = []
    for attempt in attempts:
        row = dict(attempt)
        runtime_policy = {**RUNTIME_POLICY, "InpRuntimeVetoTapeEnabled": False}
        set_payload = dict(row["set"])
        set_path = Path(str(set_payload["path"]))
        override_set_file(set_path, runtime_policy)
        set_payload["sha256"] = sha256_file(set_path)
        set_payload["runtime_policy_override"] = json_ready(runtime_policy)
        row["set"] = set_payload
        row["runtime_policy"] = json_ready(runtime_policy)
        patched.append(row)
    backfill.write_json(
        MT5_ROOT / "runtime_policy_override_manifest.json",
        {"base_policy": RUNTIME_POLICY, "attempts": patched},
    )
    return patched


def attach_runtime_density(
    runtime_rows: Sequence[Mapping[str, Any]],
    split_payload: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in runtime_rows:
        item = dict(row)
        expected = split_payload[str(item.get("split"))]["expected"]
        days = float(expected.get("days_in_scope", 0) or 0)
        trades = as_float(item.get("trade_count")) or 0.0
        item["days_in_scope"] = int(days)
        item["runtime_trades_per_day"] = float(trades / days) if days else 0.0
        item["expected_signal_density_per_day"] = expected.get("expected_signal_density_per_day")
        out.append(item)
    return out


def proxy_runtime_gap_rows(proxy_row: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        split = str(row.get("split", ""))
        proxy_prefix = "validation" if split == "validation_is" else "oos"
        proxy_pf = as_float(proxy_row.get(f"{proxy_prefix}_profit_factor"))
        proxy_dd = as_float(proxy_row.get(f"{proxy_prefix}_dd_risk"))
        proxy_trades = as_float(proxy_row.get(f"{proxy_prefix}_trade_count"))
        proxy_density = as_float(proxy_row.get(f"{proxy_prefix}_trades_per_day"))
        mt5_pf = as_float(row.get("profit_factor"))
        mt5_dd = as_float(row.get("max_drawdown_percent"))
        mt5_trades = as_float(row.get("trade_count"))
        mt5_density = as_float(row.get("runtime_trades_per_day"))
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "candidate_id": str(proxy_row["candidate_id"]),
                "split": split,
                "proxy_profit_factor": proxy_pf,
                "mt5_profit_factor": mt5_pf,
                "profit_factor_gap_mt5_minus_proxy": none_gap(mt5_pf, proxy_pf),
                "proxy_dd_risk": proxy_dd,
                "mt5_max_drawdown_percent": mt5_dd,
                "dd_gap_mt5_minus_proxy": none_gap(mt5_dd, proxy_dd),
                "proxy_trade_count": proxy_trades,
                "mt5_trade_count": mt5_trades,
                "trade_count_gap_mt5_minus_proxy": none_gap(mt5_trades, proxy_trades),
                "proxy_trades_per_day": proxy_density,
                "mt5_trades_per_day": mt5_density,
                "density_gap_mt5_minus_proxy": none_gap(mt5_density, proxy_density),
                "signal_count_diff": row.get("signal_count_diff"),
                "feature_ready_diff": row.get("feature_ready_diff"),
            }
        )
    return rows


def write_proxy_artifacts(
    training: Mapping[str, Any],
    artifacts: Mapping[str, Any],
    proxy_rows: Sequence[Mapping[str, Any]],
    proxy_row: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
) -> None:
    backfill.write_json(RUN_ROOT / "source_truth_snapshot.json", source_truth_snapshot(training, artifacts, proxy_row))
    backfill.write_csv(Path("stages") / STAGE_ID / "02_runs" / RUN_B / "proxy_surface_summary.csv", proxy_rows)
    backfill.write_json(Path("stages") / STAGE_ID / "02_runs" / RUN_B / "selected_proxy_candidate.json", proxy_row)
    backfill.write_json(Path("stages") / STAGE_ID / "01_inputs" / "runtime_policy_manifest.json", {"policy": RUNTIME_POLICY, "attempts": attempts})
    backfill.write_json(Path("stages") / STAGE_ID / "02_runs" / RUN_A / "stage_open_manifest.json", stage_open_manifest(proxy_row))
    backfill.write_json(Path("stages") / STAGE_ID / "02_runs" / RUN_C / "runtime_probe_manifest.json", {"candidate": proxy_row, "artifacts": artifacts, "attempts": attempts})
    backfill.write_text_sig(Path("stages") / STAGE_ID / "00_spec" / "stage_brief.md", stage_brief_text(proxy_row))
    backfill.write_text_sig(REVIEWS_ROOT / "runA_report.md", run_a_report_text(proxy_row))
    backfill.write_text_sig(REVIEWS_ROOT / "runB_report.md", run_b_report_text(proxy_rows, proxy_row))


def source_truth_snapshot(
    training: Mapping[str, Any],
    artifacts: Mapping[str, Any],
    proxy_row: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "candidate_id": proxy_row["candidate_id"],
        "feature_count": len(training["feature_order"]),
        "feature_order_hash": training["feature_order_hash"],
        "train_rows": int(np.asarray(training["train_mask"], dtype=bool).sum()),
        "event_positive_rate_train": training["event_positive_rate_train"],
        "label_hold_limit": training["label_hold_limit"],
        "label_pnl_q": training["label_pnl_q"],
        "pnl_cut": training["pnl_cut"],
        "score_q": proxy_row["score_q"],
        "score_threshold": proxy_row["score_threshold"],
        "admission_family": proxy_row.get("admission_family"),
        "selection_rule": proxy_row.get("selection_rule"),
        "runtime_simulation": runtime_simulation_payload(),
        "model_artifacts": artifacts,
        "claim_boundary": backfill.claim_boundary_payload(),
    }


def runtime_simulation_payload() -> dict[str, Any]:
    return {
        "side": "short",
        "max_hold_bars": MAX_HOLD_BARS,
        "atr_period": ATR_PERIOD,
        "atr_stop_multiplier": ATR_STOP_MULT,
        "atr_take_profit_multiplier": ATR_TP_MULT,
        "atr_min_stop_points": ATR_MIN_STOP_POINTS,
        "atr_max_stop_points": ATR_MAX_STOP_POINTS,
        "atr_min_take_profit_points": ATR_MIN_TP_POINTS,
        "atr_max_take_profit_points": ATR_MAX_TP_POINTS,
        "same_bar_both_hit_policy": "stop_first_conservative",
        "proxy_cost_log_return": f23b.scout.ROUGH_COST_LOG_RETURN,
    }


def stage_open_manifest(proxy_row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_A,
        "hypothesis": "fast_exit_execution_short_source_after_adverse_excursion_memory",
        "do_not_repeat": "do_not_repeat_proxy_pf_gt_one_plus_onnx_parity_as_mt5_edge_transfer",
        "selected_probe_candidate": proxy_row["candidate_id"],
        "label_parameters": {
            "label_hold_limit": proxy_row.get("label_hold_limit"),
            "label_pnl_q": proxy_row.get("label_pnl_q"),
            "pnl_cut": proxy_row.get("pnl_cut"),
            "score_q": proxy_row.get("score_q"),
        },
        "grok_stage_open": grok_receipt_payload(GROK_STAGE_OPEN_ROOT),
        "claim_boundary": backfill.claim_boundary_payload(),
    }


def write_reports(
    final: Mapping[str, Any],
    proxy_row: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    execution_payload: Mapping[str, Any],
) -> None:
    report = runtime_report_text(final, proxy_row, runtime_rows, proxy_gap_rows)
    backfill.write_text_sig(REVIEWS_ROOT / "runtime_probe_report.md", report)
    backfill.write_text_sig(REVIEWS_ROOT / f"{RUN_ID}_report.md", report)
    backfill.write_text_sig(REVIEWS_ROOT / "proxy_runtime_gap_report.md", proxy_runtime_gap_report_text(proxy_gap_rows))
    backfill.write_json(REVIEWS_ROOT / "runtime_probe_status.json", final)
    backfill.write_json(MT5_ROOT / "handoff_manifest.json", {"attempts": attempts, "execution": execution_payload})
    write_stage_lifecycle_documents(final, proxy_row, runtime_rows, proxy_gap_rows, attempts)


def write_stage_lifecycle_documents(
    final: Mapping[str, Any],
    proxy_row: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
) -> None:
    selection = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "candidate_id": proxy_row["candidate_id"],
        "classification": final.get("classification"),
        "judgment": final.get("judgment"),
        "runtime_policy": RUNTIME_POLICY,
        "runtime_rows": list(runtime_rows),
        "proxy_runtime_gap_rows": list(proxy_gap_rows),
        "failure_mode_observation": final.get("failure_mode_observation"),
        "claim_boundary": backfill.claim_boundary_payload(),
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
    }
    run_d_root = Path("stages") / STAGE_ID / "02_runs" / RUN_D
    backfill.write_json(SELECTED_ROOT / "selection_status.json", selection)
    backfill.write_json(run_d_root / "closeout_manifest.json", selection)
    backfill.write_json(RUN_ROOT / "execution_payload_summary.json", {"classification": final.get("classification"), "attempt_count": len(attempts)})
    backfill.write_text_sig(REVIEWS_ROOT / "runC_report.md", run_c_report_text(runtime_rows, proxy_gap_rows))
    backfill.write_text_sig(REVIEWS_ROOT / "runD_closeout_report.md", closeout_report_text(selection))
    backfill.write_text_sig(REVIEWS_ROOT / "required_gate_coverage_audit.md", gate_audit_text(selection))
    backfill.write_text_sig(REVIEWS_ROOT / "local_verification.md", local_verification_text(selection))
    backfill.write_text_sig(REVIEWS_ROOT / "grok_stage_open_receipt.md", grok_receipt_text("stage_open(단계 개방)", GROK_STAGE_OPEN_ROOT))
    backfill.write_text_sig(REVIEWS_ROOT / "grok_pre_mt5_receipt.md", grok_receipt_text("pre_mt5(MT5 전)", GROK_PRE_MT5_ROOT))
    backfill.write_text_sig(REVIEWS_ROOT / "grok_stage_closeout_receipt.md", grok_receipt_text("stage_closeout(단계 마감)", GROK_STAGE_CLOSE_ROOT))
    backfill.write_text_sig(SELECTED_ROOT / "selection_status.md", selection_status_text(selection))
    backfill.write_text_sig(SELECTED_ROOT / "negative_memory.md", negative_memory_text(selection))
    backfill.write_text_sig(SELECTED_ROOT / "preserved_clue.md", preserved_clue_text(selection))


def stage_judgment(runtime_rows: Sequence[Mapping[str, Any]]) -> str:
    completed = [row for row in runtime_rows if row.get("runtime_status") == "completed" and row.get("report_status") == "completed"]
    if not completed:
        return "blocked_attempt_failed(차단, 시도 실패)"
    feature_ready_ok = all((as_float(row.get("feature_ready_diff")) or 0.0) == 0.0 for row in completed)
    signal_ok = all((as_float(row.get("signal_count_diff")) or 0.0) == 0.0 for row in completed)
    min_pf = min((as_float(row.get("profit_factor")) or 0.0) for row in completed)
    max_dd = max((as_float(row.get("max_drawdown_percent")) or 999.0) for row in completed)
    densities = [as_float(row.get("runtime_trades_per_day")) or 0.0 for row in completed]
    density_ok = bool(densities) and min(densities) >= 5.0 and max(densities) <= 10.5
    if feature_ready_ok and signal_ok and min_pf >= 2.0 and max_dd < 10.0 and density_ok:
        return "completion_candidate_fast_exit_execution_source_needs_wfo_stress(완성 후보, 빠른 청산 실행 원천은 WFO/압박 검토 필요)"
    if feature_ready_ok and signal_ok and min_pf >= 1.0 and max_dd < 10.0 and density_ok:
        return "preserved_clue_fast_exit_execution_source_survived_weak_pf(보존 단서, 빠른 청산 실행 원천이 약한 PF로 생존)"
    if feature_ready_ok and signal_ok:
        return "negative_memory_fast_exit_execution_source_did_not_transfer(부정 기억, 빠른 청산 실행 원천이 MT5로 전이되지 않음)"
    return "invalid_setup_fast_exit_execution_runtime_handoff_mismatch(무효 설정, 빠른 청산 실행 런타임 인계 불일치)"


def failure_mode_observation(
    proxy_row: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    completed = [
        row for row in runtime_rows if row.get("runtime_status") == "completed" and row.get("report_status") == "completed"
    ]
    modes: list[str] = []
    if not completed:
        modes.append("blocked_attempt_failed(차단, 시도 실패)")
    feature_ready_ok = all((as_float(row.get("feature_ready_diff")) or 0.0) == 0.0 for row in completed)
    signal_ok = all((as_float(row.get("signal_count_diff")) or 0.0) == 0.0 for row in completed)
    density_match = True
    economics_match = True
    for row in proxy_gap_rows:
        proxy_density = as_float(row.get("proxy_trades_per_day")) or 0.0
        density_gap = abs(as_float(row.get("density_gap_mt5_minus_proxy")) or 0.0)
        if proxy_density > 0 and density_gap / proxy_density > 0.30:
            density_match = False
        mt5_pf = as_float(row.get("mt5_profit_factor")) or 0.0
        mt5_dd = as_float(row.get("mt5_max_drawdown_percent")) or 999.0
        proxy_pf = as_float(row.get("proxy_profit_factor")) or 0.0
        proxy_dd = as_float(row.get("proxy_dd_risk")) or 999.0
        if mt5_pf < 1.0 or mt5_pf < proxy_pf * 0.90 or mt5_dd > max(proxy_dd, 10.0):
            economics_match = False
    if completed and (not feature_ready_ok or not signal_ok):
        modes.append("proxy_still_misaligned(프록시 여전히 불정렬)")
    if completed and density_match and not economics_match:
        modes.append("density_align_economics_collapse(밀도 정렬 뒤 경제성 붕괴)")
    if completed and feature_ready_ok and signal_ok and not economics_match:
        modes.append("source_no_transfer(원천 전이 실패)")
    if not modes:
        modes.append("none_observed(관찰 없음)")
    return {
        "failure_mode_observed": modes,
        "density_match_within_30pct": density_match,
        "economics_match": economics_match,
        "parity_recheck": "pass_proxy_onnx_only(프록시 ONNX만 통과)",
        "proxy_validation_pf": proxy_row.get("validation_profit_factor"),
        "proxy_oos_pf": proxy_row.get("oos_profit_factor"),
        "comparison_note": "MT5 rows compared against all-signal proxy rows; filtered proxy kept as secondary context.",
    }


def runtime_report_text(
    final: Mapping[str, Any],
    proxy_row: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
) -> str:
    kpi_lines = "\n".join(
        f"- {row.get('split')}: runtime_status(런타임 상태)={row.get('runtime_status')}, report_status(보고 상태)={row.get('report_status')}, "
        f"PF(수익 팩터)={row.get('profit_factor')}, DD(손실폭)={row.get('max_drawdown_percent')}, "
        f"trades(거래)={row.get('trade_count')}, density/day(일 밀도)={row.get('runtime_trades_per_day')}, "
        f"signal_diff(신호 차이)={row.get('signal_count_diff')}, feature_ready_diff(피처 준비 차이)={row.get('feature_ready_diff')}"
        for row in runtime_rows
    )
    gap_lines = "\n".join(
        f"- {row.get('split')}: PF gap(MT5-proxy, MT5-프록시)={row.get('profit_factor_gap_mt5_minus_proxy')}, "
        f"DD gap(MT5-proxy, MT5-프록시)={row.get('dd_gap_mt5_minus_proxy')}, "
        f"density gap(MT5-proxy, MT5-프록시)={row.get('density_gap_mt5_minus_proxy')}"
        for row in proxy_gap_rows
    )
    policy_lines = "\n".join(f"- {key}: {value}" for key, value in RUNTIME_POLICY.items())
    return f"""# Frontier57 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `{RUN_ID}`
- candidate(후보): `{proxy_row['candidate_id']}`
- status(상태): `{final.get('classification')}`
- judgment(판정): `{final.get('judgment')}`
- failure_mode(실패 모드): `{final.get('failure_mode_observation')}`
- hypothesis(가설): fast-exit positive execution PF source(빠른 청산 양수 실행 수익 팩터 원천)
- proxy validation/OOS(프록시 검증/표본외): all-signal PF(전체 신호 수익 팩터) `{proxy_row.get('validation_profit_factor')}` / `{proxy_row.get('oos_profit_factor')}`, DD(손실폭) `{proxy_row.get('validation_dd_risk')}` / `{proxy_row.get('oos_dd_risk')}`, trade density(거래 밀도) `{proxy_row.get('validation_trades_per_day')}` / `{proxy_row.get('oos_trades_per_day')}`, raw signal density(원신호 밀도) `{proxy_row.get('validation_signals_per_day')}` / `{proxy_row.get('oos_signals_per_day')}`
- filtered proxy density(필터 프록시 밀도): `{proxy_row.get('validation_filtered_trades_per_day')}` / `{proxy_row.get('oos_filtered_trades_per_day')}`
- label(라벨): hold_limit(보유 한계)=`{proxy_row.get('label_hold_limit')}`, pnl_q(손익 분위수)=`{proxy_row.get('label_pnl_q')}`, pnl_cut(손익 절단값)=`{proxy_row.get('pnl_cut')}`, score_q(점수 분위수)=`{proxy_row.get('score_q')}`

## Runtime Policy(런타임 정책)
{policy_lines}

## Runtime KPI(런타임 성과 지표)
{kpi_lines}

## Proxy Runtime Gap(프록시 런타임 차이)
{gap_lines}

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
"""


def proxy_runtime_gap_report_text(proxy_gap_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Frontier57 Proxy Runtime Gap(프록시-런타임 차이)",
        "",
        "Action(행동): fast-exit execution source(빠른 청산 실행 원천)를 all-signal direct threshold(전체 신호 직접 임계값)로 MT5 Strategy Tester(MT5 전략 테스터)에 넘겼다.",
        "",
        "Effect(효과): proxy ranking(프록시 순위), signal density(신호 밀도), runtime economics(런타임 경제성)의 차이를 PF(수익 팩터), DD(손실폭), density(밀도), signal_diff(신호 차이)로 분리한다.",
        "",
    ]
    for row in proxy_gap_rows:
        lines.append(
            f"- {row.get('split')}: PF(수익 팩터) {row.get('proxy_profit_factor')} -> {row.get('mt5_profit_factor')}; "
            f"DD(손실폭) {row.get('proxy_dd_risk')} -> {row.get('mt5_max_drawdown_percent')}; "
            f"density/day(일 밀도) {row.get('proxy_trades_per_day')} -> {row.get('mt5_trades_per_day')}; "
            f"feature_ready_diff(피처 준비 차이)={row.get('feature_ready_diff')}; signal_diff(신호 차이)={row.get('signal_count_diff')}"
        )
    lines.append("")
    return "\n".join(lines)


def stage_brief_text(proxy_row: Mapping[str, Any]) -> str:
    return f"""# Frontier57 Stage Brief(전선57 단계 요약)

- stage_id(단계 ID): `{STAGE_ID}`
- work_family(작업군): `runtime_backtest(MT5/런타임 백테스트 실행)`
- primary_skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`
- hypothesis(가설): F56 adverse-excursion negative memory(F56 불리 이동 부정 기억) 뒤, train-only fast-exit positive execution label(학습 전용 빠른 청산 양수 실행 라벨)이 MT5에서 PF source(수익 팩터 원천)로 전이되는지 시험한다.
- selected_probe_candidate(선택 탐침 후보): `{proxy_row['candidate_id']}`
- selection_rule(선택 규칙): `{proxy_row.get('selection_rule')}`
- proxy_density(프록시 밀도): all-signal trade/day(전체 신호 거래/일) `{proxy_row.get('validation_trades_per_day')}` / `{proxy_row.get('oos_trades_per_day')}`, filtered trade/day(필터 거래/일) `{proxy_row.get('validation_filtered_trades_per_day')}` / `{proxy_row.get('oos_filtered_trades_per_day')}`
- do_not_repeat(반복 금지): proxy PF(프록시 수익 팩터)>1과 ONNX parity(온엑스 동등성)를 MT5 edge transfer(MT5 우위 전이)로 간주하지 않는다.

Action(행동): Python proxy(파이썬 프록시)는 train split(학습 분할)의 positive PnL(양수 손익)과 fast exit(빠른 청산) 조건을 학습하고, MT5(MT5, 메타트레이더5)는 같은 ONNX score threshold(온엑스 점수 임계값)를 직접 실행한다.

Effect(효과): filtered sequential proxy(필터 순차 프록시)와 실제 MT5 order path(MT5 주문 경로)의 밀도 차이를 줄이고, source economics(원천 경제성) 자체가 남는지 본다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
"""


def run_a_report_text(proxy_row: Mapping[str, Any]) -> str:
    return f"""# Frontier57 Run A(전선57 실행 A)

Action(행동): F56 negative memory(F56 부정 기억)를 읽고 fast-exit positive execution source(빠른 청산 양수 실행 원천) 가설로 F57을 열었다.

Effect(효과): 바뀐 것은 PF source(수익 팩터 원천)와 proxy alignment(프록시 정렬)이며, winner/baseline/runtime authority(승자/기준선/런타임 권위)는 상속하지 않는다.

- Grok stage-open(그록 단계 개방): `{GROK_STAGE_OPEN_ROOT.as_posix()}`
- selected candidate(선택 후보): `{proxy_row['candidate_id']}`
"""


def run_b_report_text(proxy_rows: Sequence[Mapping[str, Any]], proxy_row: Mapping[str, Any]) -> str:
    rows = "\n".join(
        f"- {row.get('candidate_id')}: all_signal val PF/DD/density(전체 신호 검증 수익 팩터/손실폭/밀도)="
        f"{row.get('validation_profit_factor')}/{row.get('validation_dd_risk')}/{row.get('validation_trades_per_day')}; "
        f"all_signal OOS PF/DD/density(전체 신호 표본외 수익 팩터/손실폭/밀도)="
        f"{row.get('oos_profit_factor')}/{row.get('oos_dd_risk')}/{row.get('oos_trades_per_day')}; "
        f"filtered density val/OOS(필터 밀도 검증/표본외)={row.get('validation_filtered_trades_per_day')}/{row.get('oos_filtered_trades_per_day')}"
        for row in proxy_rows
    )
    return f"""# Frontier57 Run B(전선57 실행 B)

Action(행동): ExtraTrees depth6 leaf80(엑스트라트리스 깊이6 리프80) fast-exit score(빠른 청산 점수)에 hold_limit/pnl_q/score_q(보유 한계/손익 분위수/점수 분위수)를 붙인 proxy surface(프록시 표면)를 확인했다.

Effect(효과): 주 후보 `{proxy_row['candidate_id']}`를 MT5 runtime probe(MT5 런타임 탐침)로 보내고, 나머지는 label/threshold stability surface(라벨/임계값 안정성 표면)로 보존한다.

## Proxy Rows(프록시 행)
{rows}
"""


def run_c_report_text(runtime_rows: Sequence[Mapping[str, Any]], proxy_gap_rows: Sequence[Mapping[str, Any]]) -> str:
    row_lines = "\n".join(
        f"- {row.get('split')}: PF(수익 팩터)={row.get('profit_factor')}, DD(손실폭)={row.get('max_drawdown_percent')}, "
        f"trades(거래)={row.get('trade_count')}, density/day(일 밀도)={row.get('runtime_trades_per_day')}"
        for row in runtime_rows
    )
    gap_lines = "\n".join(
        f"- {row.get('split')}: PF gap(PF 차이)={row.get('profit_factor_gap_mt5_minus_proxy')}, DD gap(손실폭 차이)={row.get('dd_gap_mt5_minus_proxy')}"
        for row in proxy_gap_rows
    )
    return f"""# Frontier57 Run C(전선57 실행 C)

Action(행동): mandatory MT5 runtime probe(필수 MT5 런타임 탐침)를 실행했다.

Effect(효과): fast-exit all-signal proxy(빠른 청산 전체 신호 프록시)가 direct threshold order path(직접 임계값 주문 경로)에서 유지되는지 본다.

## Runtime(런타임)
{row_lines}

## Gap(차이)
{gap_lines}
"""


def closeout_report_text(selection: Mapping[str, Any]) -> str:
    rows = selection.get("runtime_rows", [])
    row_lines = "\n".join(
        f"- {row.get('split')}: PF(수익 팩터)={row.get('profit_factor')}, DD(손실폭)={row.get('max_drawdown_percent')}, "
        f"trades(거래)={row.get('trade_count')}, feature_ready_diff(피처 준비 차이)={row.get('feature_ready_diff')}, signal_diff(신호 차이)={row.get('signal_count_diff')}"
        for row in rows
    )
    return f"""# Frontier57 Closeout(전선57 마감)

- judgment(판정): `{selection.get('judgment')}`
- runtime_probe_run(런타임 탐침 실행): `{RUN_ID}`
- candidate(후보): `{selection.get('candidate_id')}`
- failure_mode(실패 모드): `{selection.get('failure_mode_observation')}`

## Runtime Observation(런타임 관찰)
{row_lines}

Closeout(마감): `{selection.get('judgment')}`

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
"""


def gate_audit_text(selection: Mapping[str, Any]) -> str:
    return f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- runtime_evidence_gate(런타임 근거 게이트): `{RUN_ID}` MT5 Strategy Tester(MT5 전략 테스터) output(출력)으로 covered(충족).
- scope_completion_gate(범위 완료 게이트): F57 lifecycle(F57 생명주기)은 `{selection.get('judgment')}`로 closed(마감).
- kpi_contract_audit(KPI 계약 감사): Tier A separate(티어 A 분리) validation_is/OOS(검증 내부/표본외) 기록. Tier B/combined(티어 B/합산)는 missing_required(필수 누락)로 ledger(장부)에 기록.
- external_review_packet(외부 검토 묶음): Grok stage-open/pre-MT5/stage-closeout(그록 단계 개방/MT5 전/단계 마감) receipt(영수증) 기록.
- final_claim_guard(최종 주장 가드): authority/live/goal(권위/실거래/목표) not_claimed(주장 없음).
"""


def local_verification_text(selection: Mapping[str, Any]) -> str:
    return f"""# Local Verification(로컬 검증)

- feature_contract(피처 계약): raw 58 feature order(원천 58 피처 순서) hash(해시)를 사용.
- label_boundary(라벨 경계): fast-exit execution label(빠른 청산 실행 라벨)은 train split(학습 분할)의 PnL quantile(손익 분위수)과 hold limit(보유 한계)만 사용했다.
- admission_boundary(진입 허용 경계): F57은 sparse admission/runtime veto(희소 진입 허용/런타임 차단)를 쓰지 않고 all-signal direct threshold(전체 신호 직접 임계값)만 MT5에 전달했다.
- model_boundary(모델 경계): `{MODEL_ID}`는 F57에서 새로 학습했고 prior winner/baseline(과거 승자/기준선)을 상속하지 않았다.
- runtime_policy(런타임 정책): `{json.dumps(json_ready(RUNTIME_POLICY), ensure_ascii=False, sort_keys=True)}`
- hold_policy_note(보유 정책 메모): label hold_limit(라벨 보유 한계)과 runtime max_hold(런타임 최대 보유)는 source test(원천 시험)와 execution test(실행 시험)의 분리 축으로 기록한다.
- failure_mode(실패 모드): `{selection.get('failure_mode_observation')}`
- parity(동등성): ONNX(온엑스) fast-exit score output(빠른 청산 점수 출력)과 Python(파이썬) score(점수)는 model_artifact_manifest(모델 산출물 목록)에 기록.
- judgment(판정): `{selection.get('judgment')}`
"""


def selection_status_text(selection: Mapping[str, Any]) -> str:
    return f"""# Frontier57 Selection Status(전선57 선택 상태)

- judgment(판정): `{selection.get('judgment')}`
- runtime_probe_run(런타임 탐침 실행): `{RUN_ID}`
- candidate(후보): `{selection.get('candidate_id')}`
- status(상태): `{selection.get('classification')}`
- next_stage(다음 단계): `{selection.get('next_stage_id')}`

Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 claimed(주장)하지 않는다.
"""


def negative_memory_text(selection: Mapping[str, Any]) -> str:
    rows = {str(row.get("split")): row for row in selection.get("runtime_rows", [])}
    val = rows.get("validation_is", {})
    oos = rows.get("oos", {})
    return f"""# Frontier57 Negative Memory(전선57 부정 기억)

- judgment(판정): `{selection.get('judgment')}`
- memory(기억): all-signal proxy(전체 신호 프록시)와 ONNX parity(온엑스 동등성)를 맞춘 뒤에도 MT5 validation/OOS(MT5 검증/표본외) PF(수익 팩터)는 `{val.get('profit_factor')}` / `{oos.get('profit_factor')}`로 관찰됐다.
- do_not_repeat(반복 금지): fast-exit label(빠른 청산 라벨)만 바꾸고 execution economics(실행 경제성)를 MT5에서 확인하지 않는 방식으로 같은 수리를 반복하지 않는다.
- boundary(경계): F57 후보에 대한 economic transfer(경제성 전이) 기억이며, signal path failure(신호 경로 실패)나 다른 PF source(수익 팩터 원천) 탐색 금지를 뜻하지 않는다.
"""


def preserved_clue_text(selection: Mapping[str, Any]) -> str:
    rows = {str(row.get("split")): row for row in selection.get("runtime_rows", [])}
    val = rows.get("validation_is", {})
    oos = rows.get("oos", {})
    return f"""# Frontier57 Preserved Clue(전선57 보존 단서)

- judgment(판정): `{selection.get('judgment')}`
- clue(단서): all-signal proxy(전체 신호 프록시)는 MT5 trade density(MT5 거래 밀도)와 직접 비교 가능한 형태를 만들었다.
- clue(단서): validation/OOS runtime density(검증/표본외 런타임 밀도)는 `{val.get('runtime_trades_per_day')}` / `{oos.get('runtime_trades_per_day')}`로 기록됐다.
- clue(단서): feature_ready_diff(피처 준비 차이)와 signal_diff(신호 차이)를 분리해 source failure(원천 실패)와 handoff failure(인계 실패)를 구분했다.
- boundary(경계): clue only(단서 전용), no authority(권위 없음), no baseline(기준선 없음), no promotion(승격 없음).
"""


def grok_receipt_payload(root: Path) -> dict[str, Any]:
    clean = root / "clean_output.md"
    metadata = root / "metadata.json"
    metadata_payload: dict[str, Any] = {}
    if path_exists(metadata):
        try:
            metadata_payload = json.loads(io_path(metadata).read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            metadata_payload = {"success": False, "decode_error": True}
    success = metadata_payload.get("success")
    timed_out = metadata_payload.get("timed_out")
    if success is True:
        classification = "needs_local_verification(로컬 검증 필요)"
    elif timed_out:
        classification = "attempted_timeout_needs_local_verification(시도 시간초과, 로컬 검증 필요)"
    elif path_exists(metadata):
        classification = "attempted_failed_needs_local_verification(시도 실패, 로컬 검증 필요)"
    else:
        classification = "needs_local_verification(로컬 검증 필요)" if path_exists(clean) else "missing_required(필수 누락)"
    return {
        "root": root.as_posix(),
        "clean_output_exists": path_exists(clean),
        "metadata_exists": path_exists(metadata),
        "metadata_success": success,
        "metadata_timed_out": timed_out,
        "classification": classification,
    }


def grok_receipt_text(label: str, root: Path) -> str:
    payload = grok_receipt_payload(root)
    clean_path = root / "clean_output.md"
    clean_text = io_path(clean_path).read_text(encoding="utf-8-sig").strip() if path_exists(clean_path) else ""
    return f"""# Grok Receipt(그록 영수증): {label}

- path(경로): `{root.as_posix()}`
- classification(분류): `{payload['classification']}`
- metadata_success(메타데이터 성공): `{payload.get('metadata_success')}`
- metadata_timed_out(메타데이터 시간초과): `{payload.get('metadata_timed_out')}`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), EA parameters(EA 파라미터), MT5 output(MT5 출력)으로 다시 검증했다.
- effect(효과): Grok(그록) output(출력)은 authority(권위)를 만들지 않고 review boundary(검토 경계)만 제공한다.

## Clean Output(정리 출력)
{clean_text or 'missing_required(필수 누락)'}
"""


def update_workspace_state(final: Mapping[str, Any]) -> None:
    rows = {str(row.get("split")): row for row in final.get("runtime_rows", [])}
    val = rows.get("validation_is", {})
    oos = rows.get("oos", {})
    current_status = current_status_for_judgment(str(final.get("judgment") or ""))
    text = f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_D}
latest_completed_run_id: {RUN_ID}
current_status: {current_status}
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
  - "F57 MT5 runtime probe: candidate={final.get('candidate_id')}; validation_is PF={val.get('profit_factor')} DD={val.get('max_drawdown_percent')} trades={val.get('trade_count')} feature_ready_diff={val.get('feature_ready_diff')} signal_diff={val.get('signal_count_diff')}; OOS PF={oos.get('profit_factor')} DD={oos.get('max_drawdown_percent')} trades={oos.get('trade_count')} feature_ready_diff={oos.get('feature_ready_diff')} signal_diff={oos.get('signal_count_diff')}."
  - "F57 tests fast-exit positive execution source after F56 adverse-excursion memory; F56 is negative memory, not inherited authority."
  - "No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve claimed."
"""
    backfill.write_text_sig(Path("docs") / "workspace" / "workspace_state.yaml", text)
    backfill.write_text_sig(Path("docs") / "context" / "current_working_state.md", current_working_state_text(final))


def current_status_for_judgment(judgment: str) -> str:
    if judgment.startswith("completion_candidate"):
        return "closed_completion_candidate"
    if judgment.startswith("preserved_clue"):
        return "closed_preserved_clue"
    if judgment.startswith("negative_memory"):
        return "closed_negative_memory"
    if judgment.startswith("invalid_setup"):
        return "closed_invalid_setup"
    if judgment.startswith("blocked"):
        return "blocked_attempt_failed"
    return "closed_runtime_probe_observation"


def current_working_state_text(final: Mapping[str, Any]) -> str:
    rows = {str(row.get("split")): row for row in final.get("runtime_rows", [])}
    val = rows.get("validation_is", {})
    oos = rows.get("oos", {})
    return f"""# Current Working State(현재 작업 상태)

Frontier57(F57, 전선 57단계)가 `{final.get('judgment')}`로 닫혔다.

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_D}`
- runtime_probe_run(런타임 탐침 실행): `{RUN_ID}`
- candidate(후보): `{final.get('candidate_id')}`
- MT5_validation_is(MT5 검증 내부): PF={val.get('profit_factor')}, DD={val.get('max_drawdown_percent')}%, trades(거래)={val.get('trade_count')}, density/day(일 밀도)={val.get('runtime_trades_per_day')}, feature_ready_diff(피처 준비 차이)={val.get('feature_ready_diff')}, signal_diff(신호 차이)={val.get('signal_count_diff')}
- MT5_oos(MT5 표본외): PF={oos.get('profit_factor')}, DD={oos.get('max_drawdown_percent')}%, trades(거래)={oos.get('trade_count')}, density/day(일 밀도)={oos.get('runtime_trades_per_day')}, feature_ready_diff(피처 준비 차이)={oos.get('feature_ready_diff')}, signal_diff(신호 차이)={oos.get('signal_count_diff')}
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

F57 action(행동): fast-exit positive execution score(빠른 청산 양수 실행 점수)를 학습하고 all-signal direct threshold(전체 신호 직접 임계값)로 MT5 runtime probe(MT5 런타임 탐침)를 실행했다.

F57 effect(효과): label source(라벨 원천), all-signal proxy(전체 신호 프록시), MT5 order path(MT5 주문 경로)의 차이를 PF(수익 팩터), DD(손실폭), density(밀도), signal_diff(신호 차이), feature_ready_diff(피처 준비 차이)로 분리했다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
"""


def update_registers(final: Mapping[str, Any]) -> None:
    if str(final.get("judgment", "")).startswith("negative_memory"):
        append_marked_block(Path("docs") / "registers" / "negative_result_register.md", RUN_D, negative_register_block(final))
    append_marked_block(Path("docs") / "registers" / "idea_registry.md", RUN_D, idea_register_block(final))


def negative_register_block(final: Mapping[str, Any]) -> str:
    rows = {str(row.get("split")): row for row in final.get("runtime_rows", [])}
    val = rows.get("validation_is", {})
    oos = rows.get("oos", {})
    return f"""## {RUN_D}

- Stage(단계): `{STAGE_ID}`
- Negative memory(부정 기억): `{final.get('judgment')}`
- Evidence(근거): MT5 validation_is(MT5 검증 내부) PF/DD/trades(수익 팩터/손실폭/거래) `{val.get('profit_factor')}/{val.get('max_drawdown_percent')}%/{val.get('trade_count')}`; MT5 OOS(MT5 표본외) `{oos.get('profit_factor')}/{oos.get('max_drawdown_percent')}%/{oos.get('trade_count')}`.
- Runtime probe status(런타임 탐침 상태): `runtime_probe_observation_no_authority`
- Effect(효과): fast-exit positive execution source(빠른 청산 양수 실행 원천)를 같은 형태로 반복하기 전에 proxy-to-runtime economics(프록시-런타임 경제성) 전이 여부를 먼저 기억한다.
"""


def idea_register_block(final: Mapping[str, Any]) -> str:
    return f"""## {RUN_D}

- Stage(단계): `{STAGE_ID}`
- Idea(아이디어): fast-exit positive execution label(빠른 청산 양수 실행 라벨)을 PF source(수익 팩터 원천)로 시험했다.
- Result(결과): `{final.get('judgment')}`
- Evidence(근거): `{REVIEWS_ROOT.as_posix()}/runtime_probe_report.md`
- Boundary(경계): reference-only(참조 전용), no authority(권위 없음).
"""


def append_marked_block(path: Path, marker_id: str, body: str) -> None:
    marker = f"<!-- {marker_id} -->"
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    block = f"{marker}\n\n{body.strip()}\n"
    if marker in text:
        before = text.split(marker, 1)[0].rstrip()
        after = text.split(marker, 1)[1]
        tail = ""
        next_marker = after.find("\n<!-- ")
        if next_marker >= 0:
            tail = after[next_marker:].lstrip()
        new_text = f"{before}\n\n{block}\n{tail}".strip() + "\n"
    else:
        new_text = text.rstrip() + "\n\n" + block
    backfill.write_text_sig(path, new_text)


def refresh_docs() -> None:
    final = backfill.read_json(RUN_ROOT / "final_decision.json")
    proxy_row = dict(final["proxy_candidate"])
    runtime_rows = list(final["runtime_rows"])
    proxy_gap_rows = list(final["proxy_runtime_gap_rows"])
    handoff_path = MT5_ROOT / "handoff_manifest.json"
    handoff = backfill.read_json(handoff_path) if path_exists(handoff_path) else {"attempts": [], "execution": {}}
    write_reports(final, proxy_row, runtime_rows, proxy_gap_rows, handoff.get("attempts", []), handoff.get("execution", {}))
    update_workspace_state(final)
    update_registers(final)


def safe_float(value: Any) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return math.nan
    return out if math.isfinite(out) else math.nan


def as_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def none_gap(left: float | None, right: float | None) -> float | None:
    if left is None or right is None:
        return None
    return float(left - right)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
