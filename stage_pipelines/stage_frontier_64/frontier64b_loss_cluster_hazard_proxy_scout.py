from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import balanced_accuracy_score, f1_score, log_loss, roc_auc_score

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import (  # noqa: E402
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b  # noqa: E402
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b  # noqa: E402
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b  # noqa: E402
from stage_pipelines.stage_frontier_59 import run_frontier59_runtime_probe as f59  # noqa: E402


STAGE_NUM = 64
STAGE_ID = "stage_frontier_64__independent_pf_source_after_inverse_signal_memory"
RUN_ID = "frontier64B_loss_cluster_hazard_proxy_scout_v1"
RUN_NUMBER = "frontier64B"
PARENT_RUN_ID = "frontier64A_stage_open_independent_pf_source_after_inverse_signal_memory_v1"
NEXT_RUN_ID = "frontier64C_grok_pre_mt5_loss_cluster_hazard_review_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / "runB_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_64/frontier64b_loss_cluster_hazard_proxy_scout.py")

F64A_REPORT = STAGE_ROOT / "03_reviews" / "runA_report.md"
GROK_STAGE_OPEN = Path("docs/agent_control/grok_reviews/2026-06-16_frontier64_stage_open/small_review/clean_output.md")
SELECTION_STATUS_JSON = STAGE_ROOT / "04_selected" / "selection_status.json"

DIRECTION_COLUMNS = (
    "ema20_ema50_diff",
    "ppo_hist_12_26_9",
    "roc_12",
    "di_spread_14",
    "top3_weighted_return_1",
)
LOSS_PRESSURE_COLUMNS = (
    "log_return_1_against_direction",
    "log_return_3_against_direction",
    "hl_range",
    "abs_gap_percent",
    "atr_14_over_atr_50",
)
CLASS_ORDER = (0, 1)
MODEL_ID_PREFIX = "frontier64_loss_cluster_hazard_extratrees"

ENTRY_QUANTILES = (0.35, 0.45, 0.55, 0.65)
HAZARD_PROB_CEILINGS = (0.35, 0.45, 0.55, 0.65)
MAX_HOLD_OPTIONS = (2, 4, 6)
SAME_DIRECTION_COOLDOWN_OPTIONS = (0, 1)
TARGET_DENSITY_LOW = 5.0
TARGET_DENSITY_HIGH = 10.0

F63_VALIDATION_PF = 0.8140498112595147
F63_OOS_PF = 0.8526944472672842
F63_VALIDATION_DD = 12.32617605252273
F63_OOS_DD = 6.675334620797035
F63_VALIDATION_DENSITY = 4.14207650273224
F63_OOS_DENSITY = 4.755725190839694


@dataclass(frozen=True)
class HazardProfile:
    profile_id: str
    label_window_bars: int
    label_hold_bars: int
    cluster_quantile: float
    min_samples_leaf: int
    max_depth: int


PROFILES: tuple[HazardProfile, ...] = (
    HazardProfile("f64b_hz_w12_h2_q65", 12, 2, 0.65, 140, 6),
    HazardProfile("f64b_hz_w24_h4_q70", 24, 4, 0.70, 160, 7),
    HazardProfile("f64b_hz_w36_h6_q75", 36, 6, 0.75, 180, 7),
)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_context = validate_stage_context()
    base = build_base()
    models = train_hazard_models(base)
    rows = evaluate_candidates(base, models)
    final = build_final(created_at, base, models, rows, stage_context)
    artifacts = write_artifacts(final, base, models, rows)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(json.dumps(json_ready({"status": final["status"], "judgment": final["judgment"], "best_candidate": final["best_candidate_id"], "next_run_id": final["next_run_id"]}), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_DIR, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_stage_context() -> dict[str, Any]:
    required = [F64A_REPORT, GROK_STAGE_OPEN, SELECTION_STATUS_JSON]
    missing = [path.as_posix() for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing F64 stage-open context(단계 개방 문맥 누락): {missing}")
    workspace = read_text(f03b.WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_matches": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_matches": f"next_run_id: {RUN_ID}" in workspace,
        "stage_open_report_present": path_exists(F64A_REPORT),
        "grok_stage_open_accepted": "accepted" in read_text(GROK_STAGE_OPEN).lower(),
    }
    if not all(checks.values()):
        raise RuntimeError(f"F64 stage context check failed(단계 문맥 확인 실패): {json.dumps(checks, ensure_ascii=False)}")
    return {
        "checks": checks,
        "stage_open_report": artifact_identity(F64A_REPORT),
        "grok_stage_open": artifact_identity(GROK_STAGE_OPEN),
        "selection_status_json": artifact_identity(SELECTION_STATUS_JSON),
        "boundary": "stage_open_only_no_authority(단계 개방 전용, 권위 없음)",
    }


def build_base() -> dict[str, Any]:
    frame = f23b.load_frame().copy()
    feature_order = f23b.read_feature_order()
    raw_path = f33b.load_raw_path(frame)
    x_raw = frame[feature_order].astype("float64").to_numpy()
    valid_features = np.isfinite(x_raw).all(axis=1)
    runtime = build_runtime_arrays(raw_path)
    finite = (
        valid_features
        & runtime["long_valid"]
        & runtime["short_valid"]
        & np.isfinite(runtime["long_pnl_h2"])
        & np.isfinite(runtime["short_pnl_h2"])
    )
    train_mask = f33b.split_mask(frame, "train") & finite
    if not train_mask.any():
        raise RuntimeError("F64B has no finite train rows(유효 학습 행 없음)")
    direction_score = simple_direction_score(frame, train_mask)
    direction = np.where(direction_score >= 0.0, 1, -1).astype("int8")
    entry_strength = np.abs(direction_score)
    loss_pressure = loss_pressure_score(frame, direction, train_mask)
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
        "direction_score": direction_score,
        "direction": direction,
        "entry_strength": entry_strength,
        "loss_pressure": loss_pressure,
        "data_integrity": {
            "feature_count": len(feature_order),
            "feature_order_hash": ordered_hash(feature_order),
            "expected_feature_hash": f23b.EXPECTED_FEATURE_HASH,
            "feature_contract_match": len(feature_order) == 58 and ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
            "raw_rows": int(raw_path["raw_rows"]),
            "missing_entry_positions": int(raw_path["missing_entry_positions"]),
            "missing_future_positions": int(raw_path["missing_future_positions"]),
            "direction_columns": list(DIRECTION_COLUMNS),
            "loss_pressure_columns": list(LOSS_PRESSURE_COLUMNS),
        },
    }


def build_runtime_arrays(raw_path: Mapping[str, Any]) -> dict[str, np.ndarray]:
    raw = raw_path["raw"]
    entry_pos = np.asarray(raw_path["entry_pos"], dtype="int64")
    open_prices = raw["open"].to_numpy(dtype="float64")
    high_prices = raw["high"].to_numpy(dtype="float64")
    low_prices = raw["low"].to_numpy(dtype="float64")
    close_prices = raw["close"].to_numpy(dtype="float64")
    prev_close = np.r_[np.nan, close_prices[:-1]]
    tr = np.nanmax(
        np.vstack([high_prices - low_prices, np.abs(high_prices - prev_close), np.abs(low_prices - prev_close)]),
        axis=0,
    )
    atr = pd.Series(tr).rolling(f59.ATR_PERIOD, min_periods=f59.ATR_PERIOD).mean().to_numpy(dtype="float64")
    out: dict[str, np.ndarray] = {"atr": atr}
    for side_name, side in (("long", 1), ("short", -1)):
        any_valid = np.zeros(len(entry_pos), dtype=bool)
        for hold in MAX_HOLD_OPTIONS:
            pnl = np.full(len(entry_pos), np.nan, dtype="float64")
            valid = np.zeros(len(entry_pos), dtype=bool)
            exit_pos = np.full(len(entry_pos), -1, dtype="int64")
            exit_reason = np.full(len(entry_pos), "", dtype=object)
            for idx in range(len(entry_pos)):
                result = simulate_isolated_side(idx, side, entry_pos, open_prices, high_prices, low_prices, atr, max_hold=hold)
                if result["valid"]:
                    pnl[idx] = float(result["pnl"])
                    valid[idx] = True
                    exit_pos[idx] = int(result["exit_pos"])
                    exit_reason[idx] = str(result["exit_reason"])
            out[f"{side_name}_pnl_h{hold}"] = pnl
            out[f"{side_name}_valid_h{hold}"] = valid
            out[f"{side_name}_exit_pos_h{hold}"] = exit_pos
            out[f"{side_name}_exit_reason_h{hold}"] = exit_reason
            any_valid |= valid
        out[f"{side_name}_valid"] = any_valid
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


def simple_direction_score(frame: pd.DataFrame, train_mask: np.ndarray) -> np.ndarray:
    parts = []
    for column in DIRECTION_COLUMNS:
        parts.append(train_z(frame[column].astype("float64").to_numpy(), train_mask))
    return np.nanmean(np.vstack(parts), axis=0)


def loss_pressure_score(frame: pd.DataFrame, direction: np.ndarray, train_mask: np.ndarray) -> np.ndarray:
    raw_parts = {
        "log_return_1_against_direction": -direction.astype("float64") * frame["log_return_1"].astype("float64").to_numpy(),
        "log_return_3_against_direction": -direction.astype("float64") * frame["log_return_3"].astype("float64").to_numpy(),
        "hl_range": frame["hl_range"].astype("float64").to_numpy(),
        "abs_gap_percent": np.abs(frame["gap_percent"].astype("float64").to_numpy()),
        "atr_14_over_atr_50": frame["atr_14_over_atr_50"].astype("float64").to_numpy(),
    }
    return np.nanmean(np.vstack([train_z(raw_parts[column], train_mask) for column in LOSS_PRESSURE_COLUMNS]), axis=0)


def train_z(values: np.ndarray, train_mask: np.ndarray) -> np.ndarray:
    train_values = values[train_mask]
    mean = float(np.nanmean(train_values))
    std = float(np.nanstd(train_values))
    if not math.isfinite(std) or std <= 1e-12:
        return np.zeros(len(values), dtype="float64")
    return (values - mean) / std


def train_hazard_models(base: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    x_raw = np.asarray(base["x_raw"], dtype="float64")
    finite = np.asarray(base["finite"], dtype=bool)
    train_mask = np.asarray(base["train_mask"], dtype=bool)
    models: dict[str, dict[str, Any]] = {}
    for ordinal, profile in enumerate(PROFILES, start=1):
        labels, target_meta = hazard_labels(base, profile)
        train_values = labels[train_mask]
        if len(set(int(v) for v in train_values)) < 2:
            models[profile.profile_id] = {"profile": profile, "skipped": True, "skip_reason": "single_class_train_hazard_label(단일 클래스 위험 라벨)"}
            continue
        model = ExtraTreesClassifier(
            n_estimators=500,
            max_depth=profile.max_depth,
            min_samples_leaf=profile.min_samples_leaf,
            random_state=6400 + ordinal,
            n_jobs=-1,
            class_weight="balanced_subsample",
        )
        model.fit(x_raw[train_mask], train_values)
        probabilities = np.zeros((len(labels), 2), dtype="float64")
        probabilities[finite] = ordered_sklearn_probabilities(model, x_raw[finite], class_order=CLASS_ORDER)
        class_rows = classification_rows(base, labels, probabilities)
        models[profile.profile_id] = {
            "profile": profile,
            "model": model,
            "labels": labels,
            "hazard_probability": probabilities[:, 1],
            "class_rows": class_rows,
            "target_meta": target_meta,
            "skipped": False,
        }
    return models


def hazard_labels(base: Mapping[str, Any], profile: HazardProfile) -> tuple[np.ndarray, dict[str, Any]]:
    direction = np.asarray(base["direction"], dtype="int8")
    runtime = base["runtime"]
    train_mask = np.asarray(base["train_mask"], dtype=bool)
    long_pnl = np.asarray(runtime[f"long_pnl_h{profile.label_hold_bars}"], dtype="float64")
    short_pnl = np.asarray(runtime[f"short_pnl_h{profile.label_hold_bars}"], dtype="float64")
    chosen_pnl = np.where(direction > 0, long_pnl, short_pnl)
    loss_event = np.isfinite(chosen_pnl) & (chosen_pnl < 0.0)
    future_loss_cluster = forward_rolling_mean(loss_event.astype("float64"), profile.label_window_bars)
    loss_pressure = np.asarray(base["loss_pressure"], dtype="float64")
    blended = 0.65 * future_loss_cluster + 0.35 * train_rank(loss_pressure, train_mask)
    threshold = float(np.nanquantile(blended[train_mask], profile.cluster_quantile))
    labels = (blended >= threshold).astype("int64")
    labels[~np.isfinite(blended)] = 0
    target_meta = {
        "profile": asdict(profile),
        "label_boundary": "future_loss_cluster_label_used_only_for_training_target(미래 손실 군집 라벨은 학습 목표에만 사용)",
        "hazard_threshold": threshold,
        "train_hazard_rate": float(labels[train_mask].mean()),
        "all_hazard_rate": float(labels.mean()),
        "future_loss_cluster_train_mean": float(np.nanmean(future_loss_cluster[train_mask])),
        "loss_pressure_train_mean": float(np.nanmean(loss_pressure[train_mask])),
    }
    return labels, target_meta


def forward_rolling_mean(values: np.ndarray, window: int) -> np.ndarray:
    series = pd.Series(values.astype("float64"))
    min_periods = max(3, int(window) // 3)
    return series.iloc[::-1].rolling(int(window), min_periods=min_periods).mean().iloc[::-1].to_numpy(dtype="float64")


def train_rank(values: np.ndarray, train_mask: np.ndarray) -> np.ndarray:
    train_values = values[train_mask]
    finite_train = train_values[np.isfinite(train_values)]
    if len(finite_train) == 0:
        return np.zeros(len(values), dtype="float64")
    order = np.sort(finite_train)
    ranks = np.searchsorted(order, values, side="right").astype("float64") / max(1, len(order))
    ranks[~np.isfinite(values)] = 0.0
    return ranks


def classification_rows(base: Mapping[str, Any], labels: np.ndarray, probabilities: np.ndarray) -> list[dict[str, Any]]:
    frame = base["frame"]
    finite = np.asarray(base["finite"], dtype=bool)
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = f33b.split_mask(frame, split) & finite
        y_true = labels[mask]
        probs = probabilities[mask]
        pred = (probs[:, 1] >= 0.5).astype("int64")
        row = {
            "split": split,
            "rows": int(mask.sum()),
            "hazard_rate": float(y_true.mean()) if len(y_true) else 0.0,
            "balanced_accuracy": safe_float(balanced_accuracy_score(y_true, pred)) if len(set(y_true)) > 1 else 0.0,
            "macro_f1": safe_float(f1_score(y_true, pred, labels=list(CLASS_ORDER), average="macro", zero_division=0)),
            "log_loss": safe_float(log_loss(y_true, probs, labels=list(CLASS_ORDER))) if len(set(y_true)) > 1 else 0.0,
            "roc_auc": safe_float(roc_auc_score(y_true, probs[:, 1])) if len(set(y_true)) > 1 else 0.0,
            "pred_hazard_count": int(pred.sum()),
            "true_hazard_count": int(y_true.sum()),
        }
        rows.append(row)
    return rows


def evaluate_candidates(base: Mapping[str, Any], models: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    train_mask = np.asarray(base["train_mask"], dtype=bool)
    strength = np.asarray(base["entry_strength"], dtype="float64")
    direction = np.asarray(base["direction"], dtype="int8")
    for profile_id, payload in models.items():
        if payload.get("skipped"):
            continue
        hazard_probability = np.asarray(payload["hazard_probability"], dtype="float64")
        profile = payload["profile"]
        for entry_quantile in ENTRY_QUANTILES:
            entry_cut = float(np.nanquantile(strength[train_mask], entry_quantile))
            base_signal = np.where(strength >= entry_cut, direction, 0).astype("int8")
            for hazard_ceiling in HAZARD_PROB_CEILINGS:
                gated_signal = np.where((base_signal != 0) & (hazard_probability <= hazard_ceiling), base_signal, 0).astype("int8")
                for max_hold in MAX_HOLD_OPTIONS:
                    for cooldown in SAME_DIRECTION_COOLDOWN_OPTIONS:
                        row = {
                            "candidate_id": candidate_id(profile_id, entry_quantile, hazard_ceiling, max_hold, cooldown),
                            "profile_id": profile_id,
                            "model_id": model_id(profile),
                            "decision_mode": "simple_symmetric_entry_with_loss_cluster_hazard_gate(단순 대칭 진입과 손실 군집 위험 게이트)",
                            "entry_quantile": float(entry_quantile),
                            "entry_cut": entry_cut,
                            "hazard_probability_ceiling": float(hazard_ceiling),
                            "max_hold_bars": int(max_hold),
                            "same_direction_cooldown_bars": int(cooldown),
                            "entry_transition_only": True,
                            "close_on_flat_signal": False,
                        }
                        for split in ("train", "validation", "oos"):
                            metrics = proxy_metrics(base, gated_signal, split, max_hold, cooldown)
                            prefix = "validation" if split == "validation" else split
                            row.update(prefixed_metrics(prefix, metrics))
                        row["forward_min_pf"] = min(safe_float(row["validation_profit_factor"]), safe_float(row["oos_profit_factor"]))
                        row["forward_max_dd"] = max(safe_float(row["validation_dd_risk"]), safe_float(row["oos_dd_risk"]))
                        row["forward_min_density"] = min(safe_float(row["validation_trades_per_day"]), safe_float(row["oos_trades_per_day"]))
                        row["forward_density_target_flag"] = density_in_band(row["validation_trades_per_day"]) and density_in_band(row["oos_trades_per_day"])
                        row["forward_dual_positive_flag"] = safe_float(row["validation_profit_factor"]) >= 1.0 and safe_float(row["oos_profit_factor"]) >= 1.0
                        row["forward_dd_under10_flag"] = safe_float(row["validation_dd_risk"]) < 10.0 and safe_float(row["oos_dd_risk"]) < 10.0
                        row["f63_four_axis_proxy_beat_flag"] = f63_four_axis_beat(row)
                        row["hazard_vs_thinning_read"] = hazard_vs_thinning(row)
                        row["selection_score"] = selection_score(row)
                        rows.append(row)
    rows.sort(key=lambda item: safe_float(item.get("selection_score")), reverse=True)
    return rows


def proxy_metrics(base: Mapping[str, Any], signal: np.ndarray, split: str, max_hold: int, cooldown_bars: int) -> dict[str, Any]:
    frame = base["frame"]
    raw_path = base["raw_path"]
    runtime = base["runtime"]
    finite = np.asarray(base["finite"], dtype=bool)
    split_mask = f33b.split_mask(frame, split) & finite
    indices = np.flatnonzero(split_mask)
    entry_pos = np.asarray(raw_path["entry_pos"], dtype="int64")
    pnl: list[float] = []
    times: list[Any] = []
    side_counts = {1: 0, -1: 0}
    exit_reasons: dict[str, int] = {}
    next_allowed_pos = -1
    same_direction_next_allowed_pos = {1: -1, -1: -1}
    last_signal_seen = False
    last_signal = 0
    transition_block_count = 0
    cooldown_block_count = 0
    overlap_block_count = 0
    invalid_count = 0
    raw_signal_count = int((signal[split_mask] != 0).sum())
    for idx in indices:
        side = int(signal[idx])
        if side == 0:
            last_signal = 0
            last_signal_seen = True
            continue
        pos = int(entry_pos[idx])
        if pos < next_allowed_pos:
            overlap_block_count += 1
            last_signal = side
            last_signal_seen = True
            continue
        if last_signal_seen and last_signal == side:
            transition_block_count += 1
            last_signal = side
            last_signal_seen = True
            continue
        if pos < same_direction_next_allowed_pos[side]:
            cooldown_block_count += 1
            last_signal = side
            last_signal_seen = True
            continue
        result = isolated_result(runtime, idx, side, max_hold)
        if not result["valid"]:
            invalid_count += 1
            last_signal = side
            last_signal_seen = True
            continue
        pnl.append(float(result["pnl"]))
        times.append(frame["timestamp"].iloc[idx])
        side_counts[side] += 1
        reason = str(result["exit_reason"])
        exit_reasons[reason] = exit_reasons.get(reason, 0) + 1
        next_allowed_pos = int(result["exit_pos"]) + 1
        if cooldown_bars > 0:
            same_direction_next_allowed_pos[side] = int(result["exit_pos"]) + int(cooldown_bars) + 1
        last_signal = side
        last_signal_seen = True
    arr = np.asarray(pnl, dtype="float64")
    metric_payload = f23b.scout.trade_metrics(arr, pd.Series(times))
    days = f23b.scout.count_scope_days(frame.loc[split_mask, "timestamp"])
    return {
        "profit_factor": safe_float(metric_payload.get("profit_factor")),
        "dd_risk": safe_float(max(float(metric_payload["max_drawdown_percent"]), float(metric_payload["max_monthly_drawdown_percent"]))),
        "trade_count": int(len(arr)),
        "signal_count": int(raw_signal_count),
        "trades_per_day": float(len(arr) / days) if days else 0.0,
        "signals_per_day": float(raw_signal_count / days) if days else 0.0,
        "net_profit": safe_float(metric_payload.get("net_profit")),
        "win_rate": float((arr > 0.0).mean()) if len(arr) else 0.0,
        "equity_trend_r2": equity_trend_r2(arr),
        "long_trade_count": int(side_counts[1]),
        "short_trade_count": int(side_counts[-1]),
        "stop_exit_count": int(exit_reasons.get("stop", 0)),
        "take_exit_count": int(exit_reasons.get("take", 0)),
        "maxhold_exit_count": int(exit_reasons.get("maxhold", 0)),
        "entry_suppression_count": max(0, raw_signal_count - int(len(arr))),
        "transition_block_count": int(transition_block_count),
        "same_direction_cooldown_block_count": int(cooldown_block_count),
        "overlap_block_count": int(overlap_block_count),
        "invalid_event_count": int(invalid_count),
    }


def isolated_result(runtime: Mapping[str, np.ndarray], idx: int, side: int, hold: int) -> dict[str, Any]:
    prefix = "long" if side > 0 else "short"
    valid = bool(runtime[f"{prefix}_valid_h{hold}"][idx])
    if not valid:
        return {"valid": False}
    return {
        "valid": True,
        "pnl": float(runtime[f"{prefix}_pnl_h{hold}"][idx]),
        "exit_pos": int(runtime[f"{prefix}_exit_pos_h{hold}"][idx]),
        "exit_reason": str(runtime[f"{prefix}_exit_reason_h{hold}"][idx]),
    }


def prefixed_metrics(prefix: str, metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {f"{prefix}_{key}": value for key, value in metrics.items()}


def equity_trend_r2(pnl: np.ndarray) -> float:
    if len(pnl) < 3:
        return 0.0
    y = np.cumsum(pnl)
    x = np.arange(len(y), dtype="float64")
    if float(np.nanvar(y)) <= 1e-12:
        return 0.0
    coef = np.polyfit(x, y, 1)
    y_hat = coef[0] * x + coef[1]
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - float(np.mean(y))) ** 2))
    return max(0.0, 1.0 - ss_res / ss_tot) if ss_tot > 0 else 0.0


def f63_four_axis_beat(row: Mapping[str, Any]) -> bool:
    return bool(
        safe_float(row.get("validation_profit_factor")) > F63_VALIDATION_PF
        and safe_float(row.get("oos_profit_factor")) > F63_OOS_PF
        and safe_float(row.get("validation_dd_risk")) <= F63_VALIDATION_DD
        and safe_float(row.get("oos_dd_risk")) <= F63_OOS_DD
        and density_in_band(row.get("validation_trades_per_day"))
        and density_in_band(row.get("oos_trades_per_day"))
        and safe_float(row.get("validation_equity_trend_r2")) > 0.05
        and safe_float(row.get("oos_equity_trend_r2")) > 0.05
    )


def hazard_vs_thinning(row: Mapping[str, Any]) -> str:
    if safe_float(row.get("forward_min_density")) < TARGET_DENSITY_LOW:
        return "likely_thinning_density_below_target(거래 축소 가능성, 빈도 목표 미달)"
    if safe_float(row.get("forward_min_pf")) <= 1.0:
        return "hazard_gate_did_not_lift_pf(위험 게이트가 PF를 올리지 못함)"
    if bool(row.get("f63_four_axis_proxy_beat_flag")):
        return "hazard_gate_proxy_clue_not_only_thinning(위험 게이트 프록시 단서, 단순 축소만은 아님)"
    return "mixed_proxy_read_requires_pre_mt5_review(혼합 프록시 판독, MT5 전 검토 필요)"


def selection_score(row: Mapping[str, Any]) -> float:
    density_penalty = density_distance(row.get("validation_trades_per_day")) + density_distance(row.get("oos_trades_per_day"))
    dd_penalty = max(0.0, safe_float(row.get("forward_max_dd")) - 10.0) / 10.0
    pf_axis = min(safe_float(row.get("validation_profit_factor")), 4.0) + min(safe_float(row.get("oos_profit_factor")), 4.0)
    smooth_axis = safe_float(row.get("validation_equity_trend_r2")) + safe_float(row.get("oos_equity_trend_r2"))
    f63_bonus = 2.0 if bool(row.get("f63_four_axis_proxy_beat_flag")) else 0.0
    positive_bonus = 0.75 if bool(row.get("forward_dual_positive_flag")) else 0.0
    dd_bonus = 0.5 if bool(row.get("forward_dd_under10_flag")) else 0.0
    return f63_bonus + positive_bonus + dd_bonus + pf_axis + smooth_axis - density_penalty - dd_penalty


def build_final(
    created_at: str,
    base: Mapping[str, Any],
    models: Mapping[str, Mapping[str, Any]],
    rows: list[dict[str, Any]],
    stage_context: Mapping[str, Any],
) -> dict[str, Any]:
    best = rows[0] if rows else {}
    f63_beats = [row for row in rows if row.get("f63_four_axis_proxy_beat_flag")]
    seed_rows = [
        row
        for row in rows
        if safe_float(row.get("validation_profit_factor")) >= 1.2
        and safe_float(row.get("oos_profit_factor")) >= 1.2
        and density_in_band(row.get("validation_trades_per_day"))
        and density_in_band(row.get("oos_trades_per_day"))
        and safe_float(row.get("forward_max_dd")) <= 15.0
    ]
    preserved_rows = [
        row
        for row in rows
        if safe_float(row.get("validation_profit_factor")) >= 1.0
        and safe_float(row.get("oos_profit_factor")) >= 1.0
        and safe_float(row.get("forward_min_density")) >= 3.0
        and safe_float(row.get("forward_max_dd")) <= 20.0
    ]
    if f63_beats:
        status = "loss_cluster_hazard_proxy_scout_clue_no_authority(손실 군집 위험 프록시 탐색 단서, 권위 없음)"
        judgment = "scout_clue(탐색 단서)"
    elif seed_rows:
        status = "loss_cluster_hazard_seed_surface_no_authority(손실 군집 위험 씨앗 표면, 권위 없음)"
        judgment = "seed_surface(씨앗 표면)"
    elif preserved_rows:
        status = "loss_cluster_hazard_preserved_clue_no_authority(손실 군집 위험 보존 단서, 권위 없음)"
        judgment = "preserved_clue_candidate(보존 단서 후보)"
    elif rows:
        status = "loss_cluster_hazard_proxy_failed_forward_axes_no_authority(손실 군집 위험 프록시 전진축 실패, 권위 없음)"
        judgment = "negative_memory_candidate_requires_runtime_probe(부정 기억 후보, 런타임 탐침 필요)"
    else:
        status = "loss_cluster_hazard_invalid_no_trainable_candidate_no_authority(손실 군집 위험 학습 후보 없음, 권위 없음)"
        judgment = "invalid_setup_candidate(무효 설정 후보)"
    skipped = [payload for payload in models.values() if payload.get("skipped")]
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID if rows else "frontier64D_repair_or_closeout_after_invalid_proxy_v1",
        "status": status,
        "judgment": judgment,
        "candidate_row_count": len(rows),
        "f63_four_axis_beat_rows": len(f63_beats),
        "seed_surface_rows": len(seed_rows),
        "preserved_clue_rows": len(preserved_rows),
        "best_candidate_id": best.get("candidate_id", "none"),
        "best_candidate_row": best,
        "profile_count": len(PROFILES),
        "trained_model_count": len([p for p in models.values() if not p.get("skipped")]),
        "skipped_model_count": len(skipped),
        "data_integrity": base["data_integrity"],
        "stage_context": stage_context,
        "model_validation": {
            "model_role": "binary admission hazard gate only(이진 진입 위험 게이트 전용)",
            "direction_boundary": "simple symmetric entry surface supplies direction(단순 대칭 진입 표면이 방향 제공)",
            "target_boundary": "future loss cluster is training label only(미래 손실 군집은 학습 라벨 전용)",
            "split_method": "fixed train/validation/OOS split, no WFO yet(고정 학습/검증/표본외 분할, WFO 아직 없음)",
            "selection_policy": "capped proxy grid, no post-MT5 threshold repair(상한 프록시 격자, 런타임 후 임계값 수리 없음)",
            "best_candidate": best.get("candidate_id", "none"),
        },
        "mt5_status": "pending_pre_mt5_grok_review_and_runtime_probe(비싼 MT5 전 그록 검토와 런타임 탐침 대기)",
        "wfo_status": "not_run_proxy_only(WFO 미실행, 프록시 전용)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(
    final: Mapping[str, Any],
    base: Mapping[str, Any],
    models: Mapping[str, Mapping[str, Any]],
    rows: list[dict[str, Any]],
) -> dict[str, Path]:
    model_artifacts = export_selected_model(final, base, models)
    candidate_rows = json_ready(rows)
    if candidate_rows and model_artifacts:
        candidate_rows[0].update(
            {
                "joblib_path": model_artifacts["model_path"],
                "joblib_sha256": model_artifacts["model_sha256"],
                "onnx_path": model_artifacts["onnx_path"],
                "onnx_sha256": model_artifacts["onnx_sha256"],
                "onnx_parity_passed": model_artifacts["onnx_parity"]["passed"],
                "onnx_parity_max_abs_diff": model_artifacts["onnx_parity"]["max_abs_diff"],
            }
        )
        final["best_candidate_row"].update(candidate_rows[0])
    model_rows: list[dict[str, Any]] = []
    target_rows: list[dict[str, Any]] = []
    for profile_id, payload in models.items():
        profile = payload.get("profile")
        target_rows.append({"profile_id": profile_id, **(payload.get("target_meta") or {}), "skipped": bool(payload.get("skipped")), "skip_reason": payload.get("skip_reason", "")})
        for row in payload.get("class_rows", []):
            model_rows.append({"profile_id": profile_id, "model_id": model_id(profile), **row})
    artifacts = {
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "model_diagnostics": RUN_ROOT / "model_diagnostics.csv",
        "target_diagnostics": RUN_ROOT / "target_diagnostics.csv",
        "final_decision": RUN_ROOT / "final_decision.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_csv(artifacts["candidate_summary"], candidate_rows)
    write_csv(artifacts["model_diagnostics"], model_rows)
    write_csv(artifacts["target_diagnostics"], target_rows)
    final_payload = {**final, "model_artifacts": model_artifacts, "script_path": SCRIPT_PATH.as_posix(), "script_sha256": sha256_file(SCRIPT_PATH)}
    write_json(artifacts["final_decision"], final_payload)
    write_json(artifacts["run_manifest"], {**final_payload, "artifacts": {key: path.as_posix() for key, path in artifacts.items()}})
    return artifacts


def export_selected_model(final: Mapping[str, Any], base: Mapping[str, Any], models: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    best = final.get("best_candidate_row") or {}
    profile_id = str(best.get("profile_id", ""))
    payload = models.get(profile_id)
    if not payload or payload.get("skipped"):
        return {}
    model = payload["model"]
    model_name = model_id(payload["profile"])
    model_path = MODEL_DIR / f"{model_name}.joblib"
    onnx_path = MODEL_DIR / f"{model_name}.onnx"
    io_path(model_path.parent).mkdir(parents=True, exist_ok=True)
    joblib.dump(model, io_path(model_path))
    export_meta = export_sklearn_to_onnx_zipmap_disabled(model, onnx_path, feature_count=58, target_opset=12, drop_label_output=False)
    sample = np.asarray(base["x_raw"], dtype="float64")[np.asarray(base["finite"], dtype=bool)][:1024]
    expected = ordered_sklearn_probabilities(model, sample, class_order=CLASS_ORDER)
    parity = onnx_probability_parity(onnx_path, sample, expected)
    return {
        "model_id": model_name,
        "model_path": model_path.as_posix(),
        "model_sha256": sha256_file(model_path),
        "onnx_path": onnx_path.as_posix(),
        "onnx_sha256": sha256_file(onnx_path),
        "onnx_export": export_meta,
        "onnx_parity": parity,
        "feature_order_hash": base["feature_order_hash"],
        "feature_count": 58,
        "class_order": list(CLASS_ORDER),
    }


def onnx_probability_parity(onnx_path: Path, values: np.ndarray, expected: np.ndarray) -> dict[str, Any]:
    try:
        import onnxruntime as ort

        session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: values.astype(np.float32)})
        probabilities = None
        for output in outputs:
            arr = np.asarray(output)
            if arr.ndim == 2 and arr.shape[1] == expected.shape[1]:
                probabilities = arr.astype("float64")
                break
        if probabilities is None:
            return {"passed": False, "reason": "probability_output_not_found(확률 출력 없음)", "output_count": len(outputs)}
        diff = np.abs(probabilities - expected)
        return {
            "passed": bool(float(diff.max()) <= 1e-5),
            "max_abs_diff": safe_float(diff.max()),
            "mean_abs_diff": safe_float(diff.mean()),
            "rows": int(len(values)),
            "output_count": len(outputs),
            "input_name": input_name,
        }
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {"passed": False, "reason": f"onnxruntime_failed(온엑스런타임 실패): {exc}"}


def write_report(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> None:
    best = final.get("best_candidate_row") or {}
    lines = [
        "# Frontier64B Loss-Cluster Hazard Proxy Scout(F64B 손실 군집 위험 프록시 탐색)",
        "",
        f"Updated(갱신): {final['created_at_utc']}",
        "",
        f"Status(상태): `{final['status']}`",
        "",
        f"Judgment(판정): `{final['judgment']}`",
        "",
        "## Action And Effect(행동과 효과)",
        "",
        "Action(행동): binary hazard model(이진 위험 모델)로 local loss-cluster hazard(국소 손실 군집 위험)를 예측하고, simple symmetric entry surface(단순 대칭 진입 표면)의 진입만 gate(게이트)했다.",
        "",
        "Effect(효과): model(모델)이 direction(방향)을 고르지 않게 해 F61~F63 side allocation(방향 배분) repair loop(수리 반복)과 분리했다.",
        "",
        "## Result Summary(결과 요약)",
        "",
        f"- candidate rows(후보 행): `{final['candidate_row_count']}`",
        f"- f63 four-axis beat rows(F63 네 축 동시 개선 행): `{final['f63_four_axis_beat_rows']}`",
        f"- seed surface rows(씨앗 표면 행): `{final['seed_surface_rows']}`",
        f"- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`",
        f"- best candidate(최선 후보): `{best.get('candidate_id', 'none')}`",
        f"- validation PF/density/DD/smoothness(검증 수익 팩터/빈도/손실폭/매끄러움): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk'))}%` / `{fmt(best.get('validation_equity_trend_r2'))}`",
        f"- OOS PF/density/DD/smoothness(표본외 수익 팩터/빈도/손실폭/매끄러움): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk'))}%` / `{fmt(best.get('oos_equity_trend_r2'))}`",
        f"- hazard_vs_thinning(위험 대 단순 축소): `{best.get('hazard_vs_thinning_read', 'none')}`",
        "",
        "## Artifacts(산출물)",
        "",
        f"- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`",
        f"- model diagnostics(모델 진단): `{artifacts['model_diagnostics'].as_posix()}`",
        f"- target diagnostics(목표 진단): `{artifacts['target_diagnostics'].as_posix()}`",
        f"- final decision(최종 판단): `{artifacts['final_decision'].as_posix()}`",
        "",
        "## Boundaries(경계)",
        "",
        "Evidence boundary(근거 경계): proxy-only(프록시 전용), ONNX parity(온엑스 동등성)는 selected model(선택 모델)에만 확인했다.",
        "",
        "Missing evidence(부족 근거): WFO(워크포워드), stress(스트레스), MT5 runtime probe(MT5 런타임 탐침)는 아직 실행하지 않았다.",
        "",
        "Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.",
        "",
        f"Next action(다음 행동): `{final['next_run_id']}`. Effect(효과): expensive MT5/WFO(비싼 MT5/WFO) 전에 Grok second opinion(그록 2차 의견)과 local verification(로컬 검증)을 거친다.",
        "",
    ]
    f03b.write_text_sig(REPORT_PATH, "\n".join(lines))


def update_registries(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(final))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final, artifacts))
    f03b.write_json(STAGE_ROOT / "04_selected" / "selection_status.json", selection_status_json(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(final))
    upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    for row in ledger_rows(final, artifacts):
        upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv(stage_ledger, "ledger_row_id", row)
    append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(final))
    append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_entry(final))


def workspace_state(final: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            f"current_stage_id: {STAGE_ID}",
            f"current_run_id: {RUN_ID}",
            f"latest_completed_run_id: {RUN_ID}",
            f"current_status: {final['status']}",
            f"current_judgment: {final['judgment']}",
            "next_stage_id: null",
            f"next_run_id: {final['next_run_id']}",
            "runtime_probe_status: pending_pre_mt5_grok_review",
            "runtime_authority: not_claimed",
            "operating_promotion: not_claimed",
            "live_readiness: not_claimed",
            "goal_achieve: not_claimed",
            f"updated_at_utc: '{final['created_at_utc']}'",
            "notes:",
            f"  - \"F64B proxy(프록시) completed(완료): best={final['best_candidate_id']}; f63_four_axis_beat_rows={final['f63_four_axis_beat_rows']}; seed_rows={final['seed_surface_rows']}; preserved_rows={final['preserved_clue_rows']}.\"",
            "  - \"MT5 runtime probe(MT5 런타임 탐침) still pending(대기); next step(다음 단계) is pre-MT5 Grok review(비싼 MT5 전 그록 검토).\"",
            "  - \"No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed(주장 없음).\"",
        ]
    )


def current_working_state(final: Mapping[str, Any]) -> str:
    best = final.get("best_candidate_row") or {}
    return f"""# Current Working State(현재 작업 상태)

Frontier64(F64, 전선 64단계)는 F64B proxy scout(프록시 탐색)를 완료했고, MT5 runtime probe(MT5 런타임 탐침)는 아직 실행 전이다.

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- judgment(판정): `{final['judgment']}`
- best_candidate(최선 후보): `{final['best_candidate_id']}`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk'))}%`
- OOS PF/density/DD(표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk'))}%`
- f63_four_axis_beat_rows(F63 네 축 동시 개선 행): `{final['f63_four_axis_beat_rows']}`
- next_run(다음 실행): `{final['next_run_id']}`

Action(행동): binary hazard model(이진 위험 모델)이 simple symmetric entry surface(단순 대칭 진입 표면)의 진입을 허용/차단하도록 proxy(프록시)를 실행했다.

Effect(효과): F64 가설이 단순 thinning(거래 축소)인지 independent PF source(독립 수익 팩터 원천)인지 MT5 전 단계에서 먼저 판별할 수 있게 했다.

Claim boundary(주장 경계): scout clue(탐색 단서), seed surface(씨앗 표면), preserved clue(보존 단서), negative memory candidate(부정 기억 후보)까지만 말한다. completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
"""


def selection_status(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> str:
    best = final.get("best_candidate_row") or {}
    return f"""# F64 Selection Status(F64 선택 상태)

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- selected_proxy_candidate(선택 프록시 후보): `{final['best_candidate_id']}`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk'))}%`
- OOS PF/density/DD(표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk'))}%`
- f63_four_axis_beat_rows(F63 네 축 동시 개선 행): `{final['f63_four_axis_beat_rows']}`
- next_run(다음 실행): `{final['next_run_id']}`
- report(보고서): `{REPORT_PATH.as_posix()}`
- candidate_summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
"""


def selection_status_json(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "selected_proxy_candidate": final["best_candidate_id"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
        "candidate_summary": artifacts["candidate_summary"].as_posix(),
        "claim_boundary": final["claim_boundary"],
    }


def review_index(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> str:
    return "\n".join(
        [
            "# F64 Review Index(F64 검토 색인)",
            "",
            "- `runA_report.md`: stage-open report(단계 개방 보고)",
            "- `runB_report.md`: proxy scout report(프록시 탐색 보고)",
            "- `grok_stage_open_receipt.md`: Grok stage-open receipt(그록 단계 개방 영수증)",
            "- `local_verification.md`: local verification(로컬 검증)",
            "- `required_gate_coverage_audit.md`: required gate coverage audit(필수 게이트 커버리지 감사)",
            "- `stage_run_ledger.csv`: stage-local run ledger(단계 로컬 실행 장부)",
            f"- `{artifacts['candidate_summary'].as_posix()}`: candidate summary(후보 요약)",
            "",
        ]
    )


def gate_audit(final: Mapping[str, Any]) -> str:
    return f"""# F64 Required Gate Coverage Audit(F64 필수 게이트 커버리지 감사)

- reentry_read(재진입 읽기): `completed(완료)`
- work_family_selected(작업군 선택): `alpha_experiment(알파 실험)` / `experiment_design(실험 설계)`
- primary_skill_receipt(주 스킬 영수증): `obsidian-experiment-design(실험 설계)`
- support_skill_receipts(보조 스킬 영수증): `obsidian-data-integrity(데이터 무결성)`, `obsidian-model-validation(모델 검증)`, `obsidian-grok-collaboration(그록 협업)`, `obsidian-runtime-parity(런타임 동등성)`, `obsidian-claim-discipline(주장 규율)`
- stage_open_grok_review(단계 개방 그록 검토): `accepted(수용)`
- proxy_completed(프록시 완료): `{RUN_ID}`
- proxy_judgment(프록시 판정): `{final['judgment']}`
- runtime_probe_gate(런타임 탐침 게이트): `pending_pre_mt5_grok_review(비싼 MT5 전 그록 검토 대기)`
- final_claim_guard(최종 주장 보호): forbidden claims(금지 주장) 모두 not_claimed(주장 없음).
"""


def run_registry_row(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> dict[str, Any]:
    best = final.get("best_candidate_row") or {}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "loss_cluster_hazard_proxy_scout(손실 군집 위험 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"best={final['best_candidate_id']};f63_beat={final['f63_four_axis_beat_rows']};seed={final['seed_surface_rows']};preserved={final['preserved_clue_rows']};next={final['next_run_id']}",
        "family": "alpha_experiment(알파 실험)",
        "primary_report": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": final["created_at_utc"][:10],
        "decision": final["judgment"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_rows": final["candidate_row_count"],
        "claim_boundary": "proxy_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve(프록시 전용, 완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)",
        "report_path": REPORT_PATH.as_posix(),
        "trained_models": final["trained_model_count"],
        "onnx_parity": best.get("onnx_parity_passed", ""),
        "best_proxy": final["best_candidate_id"],
        "candidate_model_id": best.get("model_id", ""),
        "profit_factor": best.get("oos_profit_factor", ""),
        "drawdown": best.get("oos_dd_risk", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "view": "proxy_scout(프록시 탐색)",
        "tier": "Tier A(티어 A)",
        "metric_scope": "proxy_not_runtime(프록시, 런타임 아님)",
        "scoreboard_lane": "loss_cluster_hazard_proxy(손실 군집 위험 프록시)",
        "external_verification_status": "pending_mt5_runtime_probe(MT5 런타임 탐침 대기)",
        "trade_density_per_feature_day": best.get("oos_trades_per_day", ""),
        "trade_density_requirement_status": "proxy_read_only(프록시 판독 전용)",
        "result_judgment": final["judgment"],
        "gate_audit_path": (STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md").as_posix(),
        "created_at": final["created_at_utc"],
        "record_view": "proxy_scout(프록시 탐색)",
        "tier_scope": "Tier A separate(티어 A 분리)",
        "kpi_scope": "loss_cluster_hazard_proxy_not_runtime(손실 군집 위험 프록시, 런타임 아님)",
        "work_family": "alpha_experiment(알파 실험)",
        "evidence_boundary": "proxy_only_runtime_pending(프록시 전용, 런타임 대기)",
        "next_action": final["next_run_id"],
        "question": "Can loss-cluster hazard admission source(손실 군집 위험 진입 허용 원천) create independent PF source(독립 수익 팩터 원천)?",
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": (STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md").as_posix(),
        "runtime_authority": "not_claimed(주장 없음)",
        "operating_promotion": "not_claimed(주장 없음)",
        "run_family": "frontier_proxy_scout(전선 프록시 탐색)",
        "run_type": "proxy_scout(프록시 탐색)",
        "output_path": artifacts["candidate_summary"].as_posix(),
        "result_path": artifacts["final_decision"].as_posix(),
        "selected_profit_factor": best.get("oos_profit_factor", ""),
        "selected_trade_density": best.get("oos_trades_per_day", ""),
        "goal_achieve": "not_claimed(주장 없음)",
        "source_authority": "reference_not_inheritance(참조이지 상속 아님)",
        "trade_density": best.get("oos_trades_per_day", ""),
        "max_drawdown_percent": best.get("oos_dd_risk", ""),
        "strict_joint_pass_count": final["f63_four_axis_beat_rows"],
    }


def ledger_rows(final: Mapping[str, Any], artifacts: Mapping[str, Path]) -> list[dict[str, Any]]:
    best = final.get("best_candidate_row") or {}
    base = run_registry_row(final, artifacts)
    base.update(
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_proxy",
            "subrun_id": f"{RUN_ID}__tier_a_proxy",
            "record_view": "Tier A separate(티어 A 분리)",
            "primary_kpi": f"best={final['best_candidate_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
            "guardrail_kpi": f"val_pf={fmt(best.get('validation_profit_factor'))};val_density={fmt(best.get('validation_trades_per_day'))};val_dd={fmt(best.get('validation_dd_risk'))};f63_beat={final['f63_four_axis_beat_rows']}",
            "status": final["status"],
            "judgment": final["judgment"],
            "path": REPORT_PATH.as_posix(),
            "external_verification_status": "pending_mt5_runtime_probe(MT5 런타임 탐침 대기)",
            "notes": f"hazard_vs_thinning={best.get('hazard_vs_thinning_read', '')}; next={final['next_run_id']}",
        }
    )
    return [base]


def changelog_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {final['created_at_utc'][:10]} Frontier64B Proxy Scout(F64B 프록시 탐색)\n\n- action(행동): `{RUN_ID}`로 loss-cluster hazard admission source(손실 군집 위험 진입 허용 원천) proxy(프록시)를 실행했다.\n- effect(효과): best `{final['best_candidate_id']}`, f63_four_axis_beat_rows(F63 네 축 동시 개선 행) `{final['f63_four_axis_beat_rows']}`를 기록하고 pre-MT5 Grok review(비싼 MT5 전 그록 검토)로 넘겼다.\n- boundary(경계): MT5 runtime probe(MT5 런타임 탐침)는 아직 pending(대기)이며 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.\n"


def idea_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {RUN_ID}\n\n- Stage(단계): `{STAGE_ID}`\n- Idea(아이디어): binary hazard model(이진 위험 모델)이 simple symmetric entry surface(단순 대칭 진입 표면)의 손실 군집 위험을 gate(게이트)한다.\n- Result(결과): `{final['judgment']}`\n- Evidence(근거): `{REPORT_PATH.as_posix()}`\n- Next(다음): `{final['next_run_id']}`\n- Boundary(경계): proxy-only(프록시 전용), runtime pending(런타임 대기), no authority(권위 없음).\n"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    pd.DataFrame(json_ready(rows)).to_csv(io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = read_csv_header(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, lineterminator="\n")
        writer.writeheader()


def read_csv_header(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv(path: Path, key: str, row: Mapping[str, Any]) -> None:
    header = read_csv_header(path)
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for existing in csv.DictReader(handle):
            rows.append(dict(existing))
    normalized = {column: f03b.stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: f03b.stringify(item.get(column, "")) for column in header})


def append_once(path: Path, marker: str, line: str) -> None:
    text = read_text(path) if path_exists(path) else ""
    marker_text = f"<!-- {marker} -->"
    if marker_text in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    f03b.write_text_sig(path, text + f"\n{marker_text}\n{line}")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def candidate_id(profile_id: str, entry_quantile: float, hazard_ceiling: float, max_hold: int, cooldown: int) -> str:
    return f"f64b_{profile_id}_eq{int(entry_quantile * 100)}_hz{int(hazard_ceiling * 100)}_h{max_hold}_cd{cooldown}"


def model_id(profile: HazardProfile) -> str:
    return f"{MODEL_ID_PREFIX}_{profile.profile_id}"


def density_in_band(value: Any) -> bool:
    number = safe_float(value)
    return TARGET_DENSITY_LOW <= number <= TARGET_DENSITY_HIGH


def density_distance(value: Any) -> float:
    number = safe_float(value)
    if number < TARGET_DENSITY_LOW:
        return TARGET_DENSITY_LOW - number
    if number > TARGET_DENSITY_HIGH:
        return number - TARGET_DENSITY_HIGH
    return 0.0


def safe_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def fmt(value: Any) -> str:
    return f"{safe_float(value):.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
