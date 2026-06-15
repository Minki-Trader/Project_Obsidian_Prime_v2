from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash, sha256_file  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b  # noqa: E402
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b  # noqa: E402
from stage_pipelines.stage_frontier_52.run_frontier52_runtime_probe import execute_attempts, override_set_file  # noqa: E402
from stage_pipelines.stage_frontier_59 import run_frontier59_runtime_probe as f59  # noqa: E402
from stage_pipelines.stage_frontier_runtime_backfill import run_frontier_runtime_probe_backfill as backfill  # noqa: E402


STAGE_NUM = 60
STAGE_ID = "stage_frontier_60__long_axis_friction_escape_or_negative_memory"
RUN_A = "frontier60A_stage_open_long_axis_friction_escape_or_negative_memory_v1"
RUN_B = "frontier60B_fixed_f59_score_admission_cadence_proxy_v1"
RUN_C = "frontier60C_mt5_runtime_probe_long_axis_friction_escape_v1"
RUN_D = "frontier60D_stage_closeout_long_axis_friction_escape_v1"
RUN_ID = "frontier60Z_runtime_probe_backfill_v1"
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
MT5_ROOT = RUN_ROOT / "mt5"
FEATURE_ROOT = RUN_ROOT / "feature_matrices"
REVIEWS_ROOT = Path("stages") / STAGE_ID / "03_reviews"
SELECTED_ROOT = Path("stages") / STAGE_ID / "04_selected"

F59_STAGE_ID = "stage_frontier_59__long_quality_edge_after_short_economics_memory"
F59_RUN_ID = "frontier59Z_runtime_probe_backfill_v1"
F59_RUN_ROOT = Path("stages") / F59_STAGE_ID / "02_runs" / F59_RUN_ID
F59_FINAL_DECISION = F59_RUN_ROOT / "final_decision.json"
F59_MODEL_MANIFEST = F59_RUN_ROOT / "models" / "model_artifact_manifest.json"

GROK_STAGE_OPEN_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-16_frontier60_stage_open_snapshot"
GROK_PRE_MT5_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-16_frontier60_pre_mt5_review"
GROK_STAGE_CLOSE_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-16_frontier60_stage_closeout_review"

SCORE_QS = (0.80, 0.85, 0.90)
REENTRY_COOLDOWNS = (1, 2)
SAME_DIRECTION_COOLDOWNS = (3, 4)
MAX_HOLD_OPTIONS = (4, 6)
TARGET_DENSITY_LOW = 5.0
TARGET_DENSITY_HIGH = 10.0

BASE_RUNTIME_POLICY = {
    "InpCloseOnFlatSignal": True,
    "InpEntryTransitionOnly": True,
    "InpEntryTransitionRearmMinConfidenceDelta": 0.0,
    "InpAtrSltpEnabled": True,
    "InpAtrPeriod": f59.ATR_PERIOD,
    "InpAtrStopMultiplier": f59.ATR_STOP_MULT,
    "InpAtrTakeProfitMultiplier": f59.ATR_TP_MULT,
    "InpAtrMinStopPoints": f59.ATR_MIN_STOP_POINTS,
    "InpAtrMaxStopPoints": f59.ATR_MAX_STOP_POINTS,
    "InpAtrMinTakeProfitPoints": f59.ATR_MIN_TP_POINTS,
    "InpAtrMaxTakeProfitPoints": f59.ATR_MAX_TP_POINTS,
    "InpRuntimeVetoTapeEnabled": False,
}

NEXT_STAGE_ID = "stage_frontier_61__non_long_axis_pf_source_after_friction_memory"
NEXT_RUN_ID = "frontier61A_stage_open_non_long_axis_pf_source_after_friction_memory_v1"

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Frontier60 fixed F59 long-score admission cadence MT5 runtime probe.")
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

    base = load_fixed_f59_score_base()
    artifacts = fixed_f59_artifacts()
    proxy_rows = evaluate_proxy_surface(base)
    proxy_row = select_primary_proxy_row(proxy_rows)
    split_payload = materialize_split_payload(base, proxy_row)
    spec = candidate_spec(proxy_row, artifacts)
    attempts = backfill.materialize_attempts(
        spec,
        split_payload,
        base["feature_order"],
        base["feature_order_hash"],
        Path(args.common_files_root),
    )
    attempts = apply_runtime_policy_overrides(attempts, proxy_row)
    write_proxy_artifacts(base, artifacts, proxy_rows, proxy_row, attempts)

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
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "candidate_id": proxy_row["candidate_id"],
        "classification": classification,
        "runtime_probe_status": classification,
        "judgment": stage_judgment(runtime_rows, proxy_row),
        "failure_mode_observation": failure_mode_observation(proxy_row, runtime_rows, proxy_gap_rows),
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
                "source_f59_run_id": F59_RUN_ID,
                "onnx_path": artifacts["onnx_path"],
                "runtime_policy": runtime_policy_for(proxy_row),
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


def load_fixed_f59_score_base() -> dict[str, Any]:
    if not path_exists(F59_FINAL_DECISION):
        raise FileNotFoundError(f"missing F59 final decision: {F59_FINAL_DECISION.as_posix()}")
    base = dict(f59.build_training_base())
    artifacts = fixed_f59_artifacts()
    model_path = Path(str(artifacts["model_path"]))
    model = joblib.load(io_path(model_path))
    x_raw = np.asarray(base["x_raw"], dtype="float64")
    finite = np.asarray(base["finite"], dtype=bool)
    score = np.full(len(base["frame"]), np.nan, dtype="float64")
    raw_prob = model.predict_proba(x_raw[finite])
    class_to_index = {int(label): index for index, label in enumerate(model.classes_)}
    if 1 not in class_to_index:
        raise RuntimeError("F59 fixed model has no positive long-quality class")
    score[finite] = raw_prob[:, class_to_index[1]]
    base["score"] = score
    base["probabilities"] = f59.long_score_three_class(score)
    base["feature_order_hash"] = ordered_hash(base["feature_order"])
    base["source_f59_final_decision"] = backfill.read_json(F59_FINAL_DECISION)
    base["source_f59_artifacts"] = artifacts
    base["raw_pos_to_frame_idx"] = {int(pos): idx for idx, pos in enumerate(np.asarray(base["raw_path"]["entry_pos"], dtype="int64"))}
    return base


def fixed_f59_artifacts() -> dict[str, Any]:
    final = backfill.read_json(F59_FINAL_DECISION)
    artifacts = dict(final["model_artifacts"])
    model_path = Path(str(artifacts["model_path"]))
    onnx_path = Path(str(artifacts["onnx_path"]))
    if not path_exists(model_path):
        raise FileNotFoundError(f"missing F59 fixed model path: {model_path.as_posix()}")
    if not path_exists(onnx_path):
        raise FileNotFoundError(f"missing F59 fixed ONNX path: {onnx_path.as_posix()}")
    artifacts["model_sha256_recheck"] = sha256_file(model_path)
    artifacts["onnx_sha256_recheck"] = sha256_file(onnx_path)
    artifacts["source_stage_id"] = F59_STAGE_ID
    artifacts["source_run_id"] = F59_RUN_ID
    artifacts["reuse_boundary"] = "fixed_input_only_no_winner_no_baseline_no_authority(고정 입력 전용, 승자/기준선/권위 없음)"
    if path_exists(F59_MODEL_MANIFEST):
        artifacts["source_model_manifest"] = backfill.read_json(F59_MODEL_MANIFEST)
    return artifacts


def evaluate_proxy_surface(base: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    score = np.asarray(base["score"], dtype="float64")
    finite = np.asarray(base["finite"], dtype=bool)
    train_mask = np.asarray(base["train_mask"], dtype=bool)
    train_scores = score[train_mask & finite & np.isfinite(score)]
    if len(train_scores) == 0:
        raise RuntimeError("F60 fixed F59 score stream has no finite train scores")
    for score_q in SCORE_QS:
        threshold = float(np.quantile(train_scores, score_q))
        signal_mask = finite & np.isfinite(score) & (score >= threshold)
        for reentry_cd in REENTRY_COOLDOWNS:
            for same_cd in SAME_DIRECTION_COOLDOWNS:
                for max_hold in MAX_HOLD_OPTIONS:
                    candidate = {
                        "candidate_id": candidate_id(score_q, reentry_cd, same_cd, max_hold),
                        "source_candidate_id": base["source_f59_final_decision"]["candidate_id"],
                        "model_family": "fixed_f59_directional_long_quality_score",
                        "score_q": float(score_q),
                        "score_threshold": threshold,
                        "side": "long(롱)",
                        "side_value": 1,
                        "label_family": "fixed_f59_long_quality_no_relabel(고정 F59 롱 품질, 재라벨 없음)",
                        "admission_family": "entry_transition_close_on_flat_cooldown(전환 진입/무신호 청산/쿨다운)",
                        "max_hold_bars": int(max_hold),
                        "reentry_cooldown_bars": int(reentry_cd),
                        "same_direction_reentry_cooldown_bars": int(same_cd),
                        "runtime_probe_candidate_flag": False,
                    }
                    for split in ("train", "validation", "oos"):
                        metrics = lifecycle_proxy_metrics(base, signal_mask, split, int(max_hold), int(reentry_cd), int(same_cd))
                        prefix = "validation" if split == "validation" else split
                        candidate.update(prefixed_metrics(prefix, metrics))
                    candidate["forward_min_pf"] = min(
                        safe_float(candidate.get("validation_profit_factor")),
                        safe_float(candidate.get("oos_profit_factor")),
                    )
                    candidate["forward_max_dd"] = max(
                        safe_float(candidate.get("validation_dd_risk")),
                        safe_float(candidate.get("oos_dd_risk")),
                    )
                    candidate["forward_min_density"] = min(
                        safe_float(candidate.get("validation_trades_per_day")),
                        safe_float(candidate.get("oos_trades_per_day")),
                    )
                    candidate["forward_max_density"] = max(
                        safe_float(candidate.get("validation_trades_per_day")),
                        safe_float(candidate.get("oos_trades_per_day")),
                    )
                    candidate["train_density_target_flag"] = density_in_band(candidate.get("train_trades_per_day"))
                    candidate["forward_density_target_flag"] = (
                        density_in_band(candidate.get("validation_trades_per_day"))
                        and density_in_band(candidate.get("oos_trades_per_day"))
                    )
                    candidate["forward_dual_positive_flag"] = bool(
                        safe_float(candidate.get("validation_profit_factor")) >= 1.0
                        and safe_float(candidate.get("oos_profit_factor")) >= 1.0
                    )
                    candidate["forward_dd_under10_flag"] = bool(candidate["forward_max_dd"] < 10.0)
                    candidate["selection_note"] = (
                        "train_only_density_rescue_readonly_forward_no_promotion"
                        "(학습 전용 밀도 구제, 전방 읽기 전용, 승격 없음)"
                    )
                    rows.append(candidate)
    return rows


def lifecycle_proxy_metrics(
    base: Mapping[str, Any],
    signal_mask: np.ndarray,
    split: str,
    max_hold: int,
    reentry_cd: int,
    same_cd: int,
) -> dict[str, Any]:
    frame = base["frame"]
    finite = np.asarray(base["finite"], dtype=bool)
    split_mask = f33b.split_mask(frame, split) & finite
    indices = np.flatnonzero(split_mask)
    entry_pos = np.asarray(base["raw_path"]["entry_pos"], dtype="int64")
    trade_pnl: list[float] = []
    trade_times: list[Any] = []
    exit_reasons: list[str] = []
    next_allowed_pos = -1
    previous_signal = False
    raw_signal_count = int((split_mask & signal_mask).sum())
    for idx in indices:
        pos = int(entry_pos[idx])
        current_signal = bool(signal_mask[idx])
        if pos < next_allowed_pos:
            previous_signal = current_signal
            continue
        if current_signal and not previous_signal:
            result = simulate_lifecycle_long(base, int(idx), signal_mask, int(max_hold))
            if result["valid"]:
                trade_pnl.append(float(result["pnl"]))
                trade_times.append(frame["timestamp"].iloc[idx])
                exit_reasons.append(str(result["exit_reason"]))
                next_allowed_pos = int(result["exit_pos"]) + max(int(reentry_cd), int(same_cd)) + 1
        previous_signal = current_signal
    arr = np.asarray(trade_pnl, dtype="float64")
    metrics = f23b.scout.trade_metrics(arr, pd.Series(trade_times))
    days = f23b.scout.count_scope_days(frame.loc[split_mask, "timestamp"])
    stop_count = sum(1 for reason in exit_reasons if reason == "stop")
    take_count = sum(1 for reason in exit_reasons if reason == "take")
    flat_count = sum(1 for reason in exit_reasons if reason == "flat")
    return {
        "profit_factor": safe_float(metrics.get("profit_factor")),
        "dd_risk": safe_float(max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"]))),
        "trade_count": int(len(arr)),
        "signal_count": raw_signal_count,
        "trades_per_day": float(len(arr) / days) if days else 0.0,
        "signals_per_day": float(raw_signal_count / days) if days else 0.0,
        "net_profit": safe_float(metrics.get("net_profit")),
        "win_rate": float((arr > 0.0).mean()) if len(arr) else 0.0,
        "stop_exit_count": int(stop_count),
        "take_exit_count": int(take_count),
        "flat_exit_count": int(flat_count),
        "entry_suppression_count": max(0, raw_signal_count - int(len(arr))),
    }


def simulate_lifecycle_long(base: Mapping[str, Any], idx: int, signal_mask: np.ndarray, max_hold: int) -> dict[str, Any]:
    raw = base["raw_path"]["raw"]
    entry_pos = np.asarray(base["raw_path"]["entry_pos"], dtype="int64")
    pos_to_idx = dict(base["raw_pos_to_frame_idx"])
    open_prices = raw["open"].to_numpy(dtype="float64")
    high_prices = raw["high"].to_numpy(dtype="float64")
    low_prices = raw["low"].to_numpy(dtype="float64")
    atr = np.asarray(base["runtime"]["atr"], dtype="float64")
    p = int(entry_pos[idx])
    if p < f59.ATR_PERIOD or p + 1 >= len(open_prices):
        return {"valid": False}
    entry = float(open_prices[p])
    atr_value = float(atr[p])
    if not math.isfinite(entry) or entry <= 0.0 or not math.isfinite(atr_value) or atr_value <= 0.0:
        return {"valid": False}
    stop_points = min(max(atr_value * f59.ATR_STOP_MULT, f59.ATR_MIN_STOP_POINTS), f59.ATR_MAX_STOP_POINTS)
    take_points = min(max(atr_value * f59.ATR_TP_MULT, f59.ATR_MIN_TP_POINTS), f59.ATR_MAX_TP_POINTS)
    stop_price = entry - stop_points
    take_price = entry + take_points
    end = min(p + int(max_hold), len(open_prices) - 1)
    for q in range(p + 1, end + 1):
        frame_idx = pos_to_idx.get(int(q))
        if frame_idx is not None and not bool(signal_mask[int(frame_idx)]):
            exit_price = float(open_prices[q])
            if math.isfinite(exit_price) and exit_price > 0.0:
                return {
                    "valid": True,
                    "pnl": math.log(exit_price / entry) - f23b.scout.ROUGH_COST_LOG_RETURN,
                    "hold_bars": q - p,
                    "exit_reason": "flat",
                    "exit_pos": q,
                }
        if float(low_prices[q]) <= stop_price:
            return {
                "valid": True,
                "pnl": math.log(stop_price / entry) - f23b.scout.ROUGH_COST_LOG_RETURN,
                "hold_bars": q - p,
                "exit_reason": "stop",
                "exit_pos": q,
            }
        if float(high_prices[q]) >= take_price:
            return {
                "valid": True,
                "pnl": math.log(take_price / entry) - f23b.scout.ROUGH_COST_LOG_RETURN,
                "hold_bars": q - p,
                "exit_reason": "take",
                "exit_pos": q,
            }
    exit_price = float(open_prices[end])
    if not math.isfinite(exit_price) or exit_price <= 0.0:
        return {"valid": False}
    return {
        "valid": True,
        "pnl": math.log(exit_price / entry) - f23b.scout.ROUGH_COST_LOG_RETURN,
        "hold_bars": end - p,
        "exit_reason": "maxhold",
        "exit_pos": end,
    }


def prefixed_metrics(prefix: str, metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {f"{prefix}_{key}": value for key, value in metrics.items()}


def select_primary_proxy_row(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not rows:
        raise RuntimeError("F60 fixed-score admission cadence proxy surface produced no rows")

    def train_density_error(row: Mapping[str, Any]) -> float:
        density = safe_float(row.get("train_trades_per_day"))
        if TARGET_DENSITY_LOW <= density <= TARGET_DENSITY_HIGH:
            return 0.0
        if density < TARGET_DENSITY_LOW:
            return TARGET_DENSITY_LOW - density
        return density - TARGET_DENSITY_HIGH

    def forward_density_error(row: Mapping[str, Any]) -> float:
        return abs(safe_float(row.get("validation_trades_per_day")) - 7.5) + abs(safe_float(row.get("oos_trades_per_day")) - 7.5)

    def score(row: Mapping[str, Any]) -> tuple[float, ...]:
        return (
            -train_density_error(row),
            safe_float(row.get("train_profit_factor")),
            -safe_float(row.get("train_dd_risk")),
            1.0 if row.get("forward_dual_positive_flag") else 0.0,
            1.0 if row.get("forward_dd_under10_flag") else 0.0,
            1.0 if row.get("forward_density_target_flag") else 0.0,
            safe_float(row.get("forward_min_pf")),
            -safe_float(row.get("forward_max_dd")),
            -forward_density_error(row),
            safe_float(row.get("score_q")),
            float(row.get("reentry_cooldown_bars") == 2),
            float(row.get("same_direction_reentry_cooldown_bars") == 4),
            float(row.get("max_hold_bars") == 6),
        )

    selected = max((dict(row) for row in rows), key=score)
    selected["runtime_probe_candidate_flag"] = True
    selected["selection_rule"] = (
        "train_only_density_rescue_then_readonly_forward_balance_single_probe"
        "(학습 전용 밀도 구제 뒤 전방 읽기 전용 균형 단일 탐침)"
    )
    return selected


def materialize_split_payload(base: Mapping[str, Any], proxy_row: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    rows_for_expected: list[dict[str, Any]] = []
    frame = base["frame"].copy()
    feature_order = list(base["feature_order"])
    x_raw = np.asarray(base["x_raw"], dtype="float64")
    finite = np.asarray(base["finite"], dtype=bool)
    score = np.asarray(base["score"], dtype="float64")
    signal_mask = finite & np.isfinite(score) & (score >= float(proxy_row["score_threshold"]))
    signal_all = np.where(signal_mask, 1, 0).astype("int8")
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


def expected_signal_summary(frame: pd.DataFrame, signal: np.ndarray, runtime_split: str) -> dict[str, Any]:
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
        "decision_mode": "threshold_margin_fixed_f59_long_score_entry_transition",
        "signal_count": signal_count,
        "raw_signal_count": signal_count,
        "admitted_signal_count": "runtime_entry_transition_measured_by_mt5(런타임 전환 진입으로 MT5에서 측정)",
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
        source_run_id=F59_RUN_ID,
        candidate_id=str(proxy_row["candidate_id"]),
        model_id=str(artifacts["model_id"]),
        model_path=Path(str(artifacts["model_path"])),
        onnx_path=Path(str(artifacts["onnx_path"])),
        decision_mode="threshold_margin",
        short_threshold=1.0,
        long_threshold=float(proxy_row["score_threshold"]),
        min_margin=0.0,
        max_hold_bars=int(proxy_row["max_hold_bars"]),
        cooldown_bars=int(proxy_row["reentry_cooldown_bars"]),
        source_contract="fixed_f59_long_score_entry_transition_cadence",
        source_note=(
            "F60 uses the F59 long-quality score artifact as fixed input only; changed variable is "
            "entry-transition/close-on-flat/cooldown admission cadence with no relabel, retrain, or authority import."
        ),
    )


def apply_runtime_policy_overrides(
    attempts: Sequence[Mapping[str, Any]],
    proxy_row: Mapping[str, Any],
) -> list[dict[str, Any]]:
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
    return {
        **BASE_RUNTIME_POLICY,
        "InpMaxHoldBars": int(proxy_row["max_hold_bars"]),
        "InpReentryCooldownBars": int(proxy_row["reentry_cooldown_bars"]),
        "InpSameDirectionReentryCooldownBars": int(proxy_row["same_direction_reentry_cooldown_bars"]),
    }


def attach_runtime_density(
    runtime_rows: Sequence[Mapping[str, Any]],
    split_payload: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in runtime_rows:
        item = dict(row)
        expected = split_payload[str(item.get("split"))]["expected"]
        days = float(expected.get("days_in_scope", 0) or 0)
        trades = safe_float(item.get("trade_count"))
        attempts = safe_float(item.get("mt5_order_attempt_count"))
        item["days_in_scope"] = int(days)
        item["runtime_trades_per_day"] = float(trades / days) if days else 0.0
        item["runtime_order_attempts_per_day"] = float(attempts / days) if days else 0.0
        item["expected_signal_density_per_day"] = expected.get("expected_signal_density_per_day")
        item["entry_policy_suppression_count"] = int(expected.get("signal_count", 0) or 0) - int(item.get("mt5_order_attempt_count", 0) or 0)
        out.append(item)
    return out


def proxy_runtime_gap_rows(proxy_row: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        split = str(row.get("split", ""))
        proxy_prefix = "validation" if split == "validation_is" else "oos"
        proxy_pf = safe_float(proxy_row.get(f"{proxy_prefix}_profit_factor"))
        proxy_dd = safe_float(proxy_row.get(f"{proxy_prefix}_dd_risk"))
        proxy_trades = safe_float(proxy_row.get(f"{proxy_prefix}_trade_count"))
        proxy_density = safe_float(proxy_row.get(f"{proxy_prefix}_trades_per_day"))
        mt5_pf = safe_float(row.get("profit_factor"))
        mt5_dd = safe_float(row.get("max_drawdown_percent"))
        mt5_trades = safe_float(row.get("trade_count"))
        mt5_density = safe_float(row.get("runtime_trades_per_day"))
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "candidate_id": proxy_row["candidate_id"],
                "split": split,
                "proxy_profit_factor": proxy_pf,
                "mt5_profit_factor": mt5_pf,
                "profit_factor_gap_mt5_minus_proxy": safe_float(mt5_pf - proxy_pf),
                "proxy_dd_risk": proxy_dd,
                "mt5_max_drawdown_percent": mt5_dd,
                "dd_gap_mt5_minus_proxy": safe_float(mt5_dd - proxy_dd),
                "proxy_trade_count": proxy_trades,
                "mt5_trade_count": mt5_trades,
                "trade_count_gap_mt5_minus_proxy": safe_float(mt5_trades - proxy_trades),
                "proxy_trades_per_day": proxy_density,
                "mt5_trades_per_day": mt5_density,
                "density_gap_mt5_minus_proxy": safe_float(mt5_density - proxy_density),
                "raw_signal_count_diff": row.get("signal_count_diff"),
                "feature_ready_diff": row.get("feature_ready_diff"),
                "entry_policy_suppression_count": row.get("entry_policy_suppression_count"),
            }
        )
    return rows


def failure_mode_observation(
    proxy_row: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    completed = [row for row in runtime_rows if row.get("runtime_status") == "completed" and row.get("report_status") == "completed"]
    modes: list[str] = []
    min_pf = min([safe_float(row.get("profit_factor")) for row in completed], default=math.nan)
    max_dd = max([safe_float(row.get("max_drawdown_percent")) for row in completed], default=math.nan)
    min_density = min([safe_float(row.get("runtime_trades_per_day")) for row in completed], default=math.nan)
    suppression = sum(int(row.get("entry_policy_suppression_count") or 0) for row in completed)
    if not completed:
        modes.append("runtime_probe_not_completed(런타임 탐침 미완료)")
    if math.isfinite(min_pf) and min_pf < 1.0:
        modes.append("friction_escape_pf_failed(마찰 탈출 수익 팩터 실패)")
    if math.isfinite(max_dd) and max_dd >= 10.0:
        modes.append("dd_not_compressed_under_10(손실폭 10 미만 압축 실패)")
    if math.isfinite(min_density) and not density_in_band(min_density):
        modes.append("runtime_density_out_of_target(런타임 밀도 목표 이탈)")
    if suppression <= 0:
        modes.append("entry_cadence_no_measured_suppression(진입 리듬 억제 미측정)")
    if not modes:
        modes.append("friction_escape_preserved_clue_candidate(마찰 탈출 보존 단서 후보)")
    return {
        "failure_mode_observed": modes,
        "proxy_forward_min_pf": proxy_row.get("forward_min_pf"),
        "proxy_forward_max_dd": proxy_row.get("forward_max_dd"),
        "proxy_forward_min_density": proxy_row.get("forward_min_density"),
        "runtime_min_pf": safe_float(min_pf),
        "runtime_max_dd": safe_float(max_dd),
        "runtime_min_density": safe_float(min_density),
        "entry_policy_suppression_count": int(suppression),
        "proxy_runtime_gap_rows": json_ready(list(proxy_gap_rows)),
        "comparison_note": "F60 compares MT5 tester KPI against lifecycle proxy, while raw signal_count_diff may include intentional entry-transition suppression.",
    }


def stage_judgment(runtime_rows: Sequence[Mapping[str, Any]], proxy_row: Mapping[str, Any]) -> str:
    completed = [row for row in runtime_rows if row.get("runtime_status") == "completed" and row.get("report_status") == "completed"]
    if not completed:
        return "blocked_runtime_probe_attempt_failed(차단, 런타임 탐침 시도 실패)"
    min_pf = min(safe_float(row.get("profit_factor")) for row in completed)
    max_dd = max(safe_float(row.get("max_drawdown_percent")) for row in completed)
    min_density = min(safe_float(row.get("runtime_trades_per_day")) for row in completed)
    if min_pf >= 1.0 and max_dd < 10.0 and density_in_band(min_density):
        return "preserved_clue_long_axis_friction_escape_probe_only(보존 단서, 롱 축 마찰 탈출 런타임 탐침 전용)"
    if min_pf < 1.0:
        return "negative_memory_long_axis_friction_escape_failed_pf(부정 기억, 롱 축 마찰 탈출 수익 팩터 실패)"
    if not density_in_band(min_density):
        return "negative_memory_long_axis_friction_escape_lost_density(부정 기억, 롱 축 마찰 탈출 밀도 상실)"
    if max_dd >= 10.0:
        return "negative_memory_long_axis_friction_escape_failed_dd(부정 기억, 롱 축 마찰 탈출 손실폭 실패)"
    return str(proxy_row.get("selection_rule", "runtime_probe_observation_no_authority"))


def write_proxy_artifacts(
    base: Mapping[str, Any],
    artifacts: Mapping[str, Any],
    proxy_rows: Sequence[Mapping[str, Any]],
    proxy_row: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
) -> None:
    backfill.write_json(RUN_ROOT / "source_truth_snapshot.json", source_truth_snapshot(base, artifacts, proxy_row))
    backfill.write_csv(Path("stages") / STAGE_ID / "02_runs" / RUN_B / "proxy_surface_summary.csv", proxy_rows)
    backfill.write_json(Path("stages") / STAGE_ID / "02_runs" / RUN_B / "selected_proxy_candidate.json", proxy_row)
    backfill.write_json(Path("stages") / STAGE_ID / "01_inputs" / "runtime_policy_manifest.json", {"policy": runtime_policy_for(proxy_row), "attempts": attempts})
    backfill.write_json(Path("stages") / STAGE_ID / "02_runs" / RUN_A / "stage_open_manifest.json", stage_open_manifest(proxy_row))
    backfill.write_json(Path("stages") / STAGE_ID / "02_runs" / RUN_C / "runtime_probe_manifest.json", {"candidate": proxy_row, "artifacts": artifacts, "attempts": attempts})
    backfill.write_text_sig(Path("stages") / STAGE_ID / "00_spec" / "stage_brief.md", stage_brief_text(proxy_row))
    backfill.write_text_sig(REVIEWS_ROOT / "runA_report.md", run_a_report_text(proxy_row))
    backfill.write_text_sig(REVIEWS_ROOT / "runB_report.md", run_b_report_text(proxy_rows, proxy_row))


def source_truth_snapshot(base: Mapping[str, Any], artifacts: Mapping[str, Any], proxy_row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "candidate_id": proxy_row["candidate_id"],
        "feature_count": len(base["feature_order"]),
        "feature_order_hash": base["feature_order_hash"],
        "source_f59_stage_id": F59_STAGE_ID,
        "source_f59_run_id": F59_RUN_ID,
        "source_f59_candidate_id": base["source_f59_final_decision"]["candidate_id"],
        "source_boundary": "fixed_artifact_input_only_no_relabel_no_retrain_no_authority(고정 산출물 입력 전용, 재라벨/재학습/권위 없음)",
        "grid_lock": {
            "score_qs": SCORE_QS,
            "reentry_cooldowns": REENTRY_COOLDOWNS,
            "same_direction_reentry_cooldowns": SAME_DIRECTION_COOLDOWNS,
            "max_hold_options": MAX_HOLD_OPTIONS,
            "posthoc_expansion": "forbidden(금지)",
        },
        "selected_proxy_candidate": proxy_row,
        "runtime_policy": runtime_policy_for(proxy_row),
        "model_artifacts": artifacts,
        "claim_boundary": backfill.claim_boundary_payload(),
    }


def stage_open_manifest(proxy_row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_A,
        "hypothesis": "fixed_f59_long_score_entry_cadence_can_escape_repeated_entry_friction_or_close_negative_memory",
        "novelty_delta": "runtime_representation_admission_cadence_only_no_relabel_no_retrain",
        "do_not_repeat": [
            "do_not_expand_grid_after_forward_read",
            "do_not_treat_f52_lifecycle_clue_as_baseline",
            "do_not_claim_long_axis_escape_without_MT5_PF_density_DD",
        ],
        "selected_probe_candidate": proxy_row["candidate_id"],
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
    del attempts, execution_payload
    backfill.write_json(REVIEWS_ROOT / "runtime_probe_status.json", final)
    backfill.write_csv(RUN_ROOT / "proxy_runtime_gap.csv", proxy_gap_rows)
    backfill.write_text_sig(REVIEWS_ROOT / "grok_stage_open_receipt.md", grok_receipt_text("stage_open(단계 개방)", GROK_STAGE_OPEN_ROOT))
    if path_exists(GROK_PRE_MT5_ROOT):
        backfill.write_text_sig(REVIEWS_ROOT / "grok_pre_mt5_receipt.md", grok_receipt_text("pre_mt5(메타트레이더 전)", GROK_PRE_MT5_ROOT))
    if path_exists(GROK_STAGE_CLOSE_ROOT):
        backfill.write_text_sig(REVIEWS_ROOT / "grok_stage_closeout_receipt.md", grok_receipt_text("stage_closeout(단계 마감)", GROK_STAGE_CLOSE_ROOT))
    backfill.write_text_sig(REVIEWS_ROOT / "runtime_probe_report.md", runtime_probe_report_text(final, runtime_rows))
    backfill.write_text_sig(REVIEWS_ROOT / f"{RUN_ID}_report.md", runtime_probe_report_text(final, runtime_rows))
    backfill.write_text_sig(REVIEWS_ROOT / "proxy_runtime_gap_report.md", proxy_runtime_gap_report_text(proxy_gap_rows))
    backfill.write_text_sig(REVIEWS_ROOT / "runC_report.md", run_c_report_text(runtime_rows, proxy_gap_rows))
    backfill.write_text_sig(REVIEWS_ROOT / "runD_closeout_report.md", run_d_report_text(final))
    backfill.write_text_sig(REVIEWS_ROOT / "required_gate_coverage_audit.md", required_gate_audit_text(final))
    backfill.write_text_sig(REVIEWS_ROOT / "local_verification.md", local_verification_text(final))
    backfill.write_text_sig(SELECTED_ROOT / "selection_status.md", selection_status_text(final))
    backfill.write_json(SELECTED_ROOT / "selection_status.json", final)
    if str(final.get("judgment", "")).startswith("negative_memory"):
        backfill.write_text_sig(SELECTED_ROOT / "negative_memory.md", negative_memory_text(final))
    else:
        backfill.write_text_sig(SELECTED_ROOT / "preserved_clue.md", preserved_clue_text(final))


def stage_brief_text(proxy_row: Mapping[str, Any]) -> str:
    return f"""# Frontier60 Stage Brief(전선60 단계 개요)

- stage(단계): `{STAGE_ID}`
- hypothesis(가설): fixed F59 long-quality score(고정 F59 롱 품질 점수)에 entry-transition/close-on-flat/cooldown admission cadence(전환 진입/무신호 청산/쿨다운 진입 리듬)를 붙이면 repeated-entry friction(반복 진입 마찰)을 벗어나는지 확인한다.
- selected_candidate(선택 후보): `{proxy_row['candidate_id']}`
- changed_variable(변경 변수): runtime representation/admission cadence(런타임 표현/진입 리듬)만.
- locked_source(고정 원천): F59 model/ONNX artifact(F59 모델/온엑스 산출물), no relabel/retrain(재라벨/재학습 없음).
- claim_boundary(주장 경계): runtime_probe_observation only(런타임 탐침 관찰 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def run_a_report_text(proxy_row: Mapping[str, Any]) -> str:
    return f"""# F60A Stage Open Report(F60A 단계 개방 보고)

Action(행동): F59 negative memory(F59 부정 기억)를 읽고 fixed-score admission cadence(고정 점수 진입 리듬) 가설로 F60을 열었다.

Effect(효과): source/model/label(원천/모델/라벨)을 바꾸지 않고 runtime representation(런타임 표현)만 시험한다.

- Grok verdict(그록 판정): `{grok_receipt_payload(GROK_STAGE_OPEN_ROOT)['classification']}`
- selected candidate(선택 후보): `{proxy_row['candidate_id']}`
- stop rule(중지 규칙): proxy 1-select(프록시 1개 선택) + MT5 runtime probe 1회(런타임 탐침 1회) 뒤 closeout(마감).
"""


def run_b_report_text(proxy_rows: Sequence[Mapping[str, Any]], proxy_row: Mapping[str, Any]) -> str:
    top = sorted(proxy_rows, key=lambda row: safe_float(row.get("train_profit_factor")), reverse=True)[:8]
    lines = [
        "# F60B Proxy Report(F60B 프록시 보고)",
        "",
        "Action(행동): fixed F59 score(고정 F59 점수) 위에서 사전등록 admission grid(진입 허용 격자)를 평가했다.",
        "",
        "Effect(효과): validation/OOS(검증/표본외)는 read-only(읽기 전용)로 기록하고, 선택은 train density rescue(학습 밀도 구제)를 우선했다.",
        "",
        f"- rows(행): `{len(proxy_rows)}`",
        f"- selected(선택): `{proxy_row['candidate_id']}`",
        f"- selected proxy validation/OOS(선택 프록시 검증/표본외): PF `{proxy_row.get('validation_profit_factor')}` / `{proxy_row.get('oos_profit_factor')}`, DD `{proxy_row.get('validation_dd_risk')}` / `{proxy_row.get('oos_dd_risk')}`, density `{proxy_row.get('validation_trades_per_day')}` / `{proxy_row.get('oos_trades_per_day')}`",
        "",
        "## Top Train PF Rows(학습 PF 상위 행)",
    ]
    for row in top:
        lines.append(
            f"- `{row.get('candidate_id')}`: train PF/DD/density(학습 수익 팩터/손실폭/밀도)="
            f"{row.get('train_profit_factor')}/{row.get('train_dd_risk')}/{row.get('train_trades_per_day')}; "
            f"forward min PF/max DD/min density(전방 최소 수익 팩터/최대 손실폭/최소 밀도)="
            f"{row.get('forward_min_pf')}/{row.get('forward_max_dd')}/{row.get('forward_min_density')}"
        )
    return "\n".join(lines).rstrip() + "\n"


def run_c_report_text(runtime_rows: Sequence[Mapping[str, Any]], proxy_gap_rows: Sequence[Mapping[str, Any]]) -> str:
    return runtime_probe_report_text({"judgment": "runtime_probe_observation_no_authority", "proxy_runtime_gap_rows": proxy_gap_rows}, runtime_rows)


def run_d_report_text(final: Mapping[str, Any]) -> str:
    return f"""# F60D Closeout Report(F60D 마감 보고)

- judgment(판정): `{final.get('judgment')}`
- runtime_probe_status(런타임 탐침 상태): `{final.get('runtime_probe_status')}`
- failure_mode_observed(관찰 실패 양식): `{final.get('failure_mode_observation', {}).get('failure_mode_observed')}`

Action(행동): F60 fixed-score admission cadence(고정 점수 진입 리듬) lifecycle(생명주기)를 MT5 runtime probe(MT5 런타임 탐침)까지 실행하고 proxy-runtime gap(프록시-런타임 차이)을 기록했다.

Effect(효과): long axis friction escape(롱 축 마찰 탈출)를 보존 단서로 둘지, 부정 기억으로 닫을지 판정했다. Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
"""


def runtime_probe_report_text(final: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# F60 Runtime Probe Report(F60 런타임 탐침 보고)",
        "",
        f"- judgment(판정): `{final.get('judgment')}`",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        "",
        "| split(분할) | runtime(런타임) | report(보고서) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | raw signal diff(원천 신호 차이) | entry suppression(진입 억제) |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in runtime_rows:
        lines.append(
            f"| {row.get('split')} | {row.get('runtime_status')} | {row.get('report_status')} | "
            f"{row.get('profit_factor')} | {row.get('max_drawdown_percent')} | {row.get('runtime_trades_per_day')} | "
            f"{row.get('signal_count_diff')} | {row.get('entry_policy_suppression_count')} |"
        )
    lines.extend(
        [
            "",
            "Boundary(경계): this is runtime_probe_observation(런타임 탐침 관찰) only; it does not create runtime authority(런타임 권위) or live readiness(실거래 준비).",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def proxy_runtime_gap_report_text(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# F60 Proxy-Runtime Gap Report(F60 프록시-런타임 차이 보고)",
        "",
        "| split(분할) | proxy PF(프록시 수익 팩터) | MT5 PF(MT5 수익 팩터) | PF gap(PF 차이) | proxy DD(프록시 손실폭) | MT5 DD(MT5 손실폭) | density gap(밀도 차이) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('split')} | {row.get('proxy_profit_factor')} | {row.get('mt5_profit_factor')} | "
            f"{row.get('profit_factor_gap_mt5_minus_proxy')} | {row.get('proxy_dd_risk')} | "
            f"{row.get('mt5_max_drawdown_percent')} | {row.get('density_gap_mt5_minus_proxy')} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def required_gate_audit_text(final: Mapping[str, Any]) -> str:
    return f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- stage_open_grok_review(단계 개방 그록 검토): `{path_exists(GROK_STAGE_OPEN_ROOT / 'clean_output.md')}`
- pre_mt5_grok_review(MT5 전 그록 검토): `{path_exists(GROK_PRE_MT5_ROOT / 'clean_output.md')}`
- mt5_runtime_probe(MT5 런타임 탐침): `{final.get('runtime_probe_status')}`
- proxy_runtime_gap(프록시-런타임 차이): `recorded(기록됨)`
- stage_closeout_grok_review(단계 마감 그록 검토): `{path_exists(GROK_STAGE_CLOSE_ROOT / 'clean_output.md')}`
- forbidden_claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve not_claimed(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음)
"""


def local_verification_text(final: Mapping[str, Any]) -> str:
    return f"""# Local Verification(로컬 검증)

- F59 fixed artifacts rechecked(F59 고정 산출물 재확인): `model_sha256_recheck`, `onnx_sha256_recheck`
- proxy rows(프록시 행): `{len(final.get('proxy_surface_rows', []))}`
- MT5 runtime rows(MT5 런타임 행): `{len(final.get('runtime_rows', []))}`
- judgment(판정): `{final.get('judgment')}`
- claim_boundary(주장 경계): `{final.get('claim_boundary')}`
"""


def selection_status_text(final: Mapping[str, Any]) -> str:
    return f"""# Frontier60 Selection Status(전선60 선택 상태)

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
- reopen_condition(재개 조건): new non-long PF source(새 비롱 수익 팩터 원천) or materially different runtime representation(실질적으로 다른 런타임 표현)이 있을 때만 롱 축을 재개한다.
"""


def preserved_clue_text(final: Mapping[str, Any]) -> str:
    return f"""# Preserved Clue(보존 단서)

- stage(단계): `{STAGE_ID}`
- judgment(판정): `{final.get('judgment')}`
- clue(단서): fixed F59 long score with admission cadence(고정 F59 롱 점수 + 진입 리듬)가 MT5에서 최소 관찰 단서를 만들었다.
- boundary(경계): runtime_probe_observation only(런타임 탐침 관찰 전용), no authority(권위 없음).
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
  - "F60 MT5 runtime probe: candidate={final.get('candidate_id')}; validation_is PF={val.get('profit_factor')} DD={val.get('max_drawdown_percent')} trades={val.get('trade_count')} density/day={val.get('runtime_trades_per_day')} feature_ready_diff={val.get('feature_ready_diff')} signal_diff={val.get('signal_count_diff')}; OOS PF={oos.get('profit_factor')} DD={oos.get('max_drawdown_percent')} trades={oos.get('trade_count')} density/day={oos.get('runtime_trades_per_day')} feature_ready_diff={oos.get('feature_ready_diff')} signal_diff={oos.get('signal_count_diff')}."
  - "F60 tests fixed F59 long score with admission cadence only; F52/F59 are reference-only, not inherited authority."
  - "No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve claimed."
"""
    backfill.write_text_sig(Path("docs") / "workspace" / "workspace_state.yaml", text)
    backfill.write_text_sig(Path("docs") / "context" / "current_working_state.md", current_working_state_text(final))


def current_status_for_judgment(judgment: str) -> str:
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

Frontier60(F60, 전선 60단계)가 `{final.get('judgment')}`로 닫혔다.

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_D}`
- runtime_probe_run(런타임 탐침 실행): `{RUN_ID}`
- candidate(후보): `{final.get('candidate_id')}`
- MT5_validation_is(MT5 검증 내부): PF={val.get('profit_factor')}, DD={val.get('max_drawdown_percent')}%, trades(거래)={val.get('trade_count')}, density/day(일 밀도)={val.get('runtime_trades_per_day')}, feature_ready_diff(피처 준비 차이)={val.get('feature_ready_diff')}, signal_diff(신호 차이)={val.get('signal_count_diff')}
- MT5_oos(MT5 표본외): PF={oos.get('profit_factor')}, DD={oos.get('max_drawdown_percent')}%, trades(거래)={oos.get('trade_count')}, density/day(일 밀도)={oos.get('runtime_trades_per_day')}, feature_ready_diff(피처 준비 차이)={oos.get('feature_ready_diff')}, signal_diff(신호 차이)={oos.get('signal_count_diff')}
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

F60 action(행동): fixed F59 long-quality score(고정 F59 롱 품질 점수)에 entry-transition/close-on-flat/cooldown runtime envelope(전환 진입/무신호 청산/쿨다운 런타임 봉투)를 붙여 MT5 runtime probe(MT5 런타임 탐침)를 실행했다.

F60 effect(효과): long-axis friction escape(롱 축 마찰 탈출) 여부를 PF(수익 팩터), DD(손실폭), density(밀도), entry suppression(진입 억제), proxy-runtime gap(프록시-런타임 차이)으로 분리했다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
"""


def update_registers(final: Mapping[str, Any]) -> None:
    if str(final.get("judgment", "")).startswith("negative_memory"):
        append_marked_block(Path("docs") / "registers" / "negative_result_register.md", RUN_D, negative_register_block(final))
    else:
        append_marked_block(Path("docs") / "registers" / "idea_registry.md", RUN_D, idea_register_block(final))
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
- Effect(효과): fixed F59 long score(고정 F59 롱 점수)에 admission cadence(진입 리듬)를 붙이는 방식이 long-axis friction escape(롱 축 마찰 탈출)를 만들었는지 기억한다.
"""


def idea_register_block(final: Mapping[str, Any]) -> str:
    return f"""## {RUN_D}

- Stage(단계): `{STAGE_ID}`
- Idea(아이디어): fixed F59 long quality score(고정 F59 롱 품질 점수)에 admission cadence runtime envelope(진입 리듬 런타임 봉투)를 붙여 friction escape(마찰 탈출)를 시험했다.
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


def grok_receipt_payload(root: Path) -> dict[str, Any]:
    metadata_path = root / "metadata.json"
    clean_path = root / "clean_output.md"
    metadata = backfill.read_json(metadata_path) if path_exists(metadata_path) else {}
    clean = io_path(clean_path).read_text(encoding="utf-8-sig") if path_exists(clean_path) else ""
    classification = "missing_required"
    text = clean.lower()
    if "accepted" in text:
        classification = "accepted"
    elif "rejected" in text:
        classification = "rejected"
    elif "needs_local_verification" in text:
        classification = "needs_local_verification"
    return {
        "classification": classification,
        "metadata_success": metadata.get("success"),
        "metadata_timed_out": metadata.get("timed_out"),
        "prompt_hash": metadata.get("prompt_hash"),
    }


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


def density_in_band(value: Any) -> bool:
    density = safe_float(value)
    return bool(TARGET_DENSITY_LOW <= density <= TARGET_DENSITY_HIGH)


def candidate_id(score_q: float, reentry_cd: int, same_cd: int, max_hold: int) -> str:
    q = int(round(score_q * 100))
    return f"f60b_fixed_f59_long_entry_cadence_q{q}_cd{reentry_cd}_same{same_cd}_h{max_hold}"


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
