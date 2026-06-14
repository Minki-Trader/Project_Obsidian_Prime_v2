from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b


STAGE_ID = "stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout"
RUN_ID = "frontier18B_asymmetric_exit_lifecycle_proxy_scout_v1"
RUN_NUMBER = "frontier18B"
PARENT_RUN_ID = "frontier18A_stage_open_asymmetric_exit_lifecycle_profit_lock_onnx_scout_v1"
NEXT_GROK_RUN_ID = "frontier18C_grok_pre_expensive_asymmetric_exit_lifecycle_review_v1"
NEXT_REPAIR_RUN_ID = "frontier18C_asymmetric_exit_lifecycle_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_18/frontier18b_asymmetric_exit_lifecycle_proxy_scout.py")

STAGE_BRIEF = STAGE_ROOT / "00_spec" / "stage_brief.md"
PROFILE_SPEC = STAGE_ROOT / "00_spec" / "lifecycle_profile_spec.md"
DO_NOT_REPEAT = STAGE_ROOT / "00_spec" / "do_not_repeat.md"
F18A_REPORT = STAGE_ROOT / "03_reviews" / f"{PARENT_RUN_ID}_report.md"
F18A_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "stage_open_summary.json"
GROK_STAGE_OPEN_OUTPUT = Path(
    "docs/agent_control/grok_reviews/2026-06-14_frontier18_stage_open/small_review/clean_output.md"
)

LABEL_ORDER = f04d.LABEL_ORDER
LABEL_NAMES = f04d.LABEL_NAMES

MODEL_ID_SHORT = {
    "logreg_l2_c0p5_plain_argmax": "lr_plain",
    "logreg_l2_c0p5_balanced_argmax": "lr_bal",
    "rf_depth5_leaf80_balanced_argmax": "rf_bal",
}

SCOUT_DENSITY_LOW = 5.0
SCOUT_DENSITY_HIGH = 10.0
SCOUT_PF_FLOOR = 1.2
SCOUT_DD_CEILING = 15.0
SCOUT_WORST_SUBPERIOD_DD_CEILING = 25.0
SEED_DENSITY_LOW = 3.0
SEED_DENSITY_HIGH = 10.0

F17B_BEST_VALIDATION_PF = 1.30338
F17B_BEST_OOS_PF = 1.13674
F17B_BEST_VALIDATION_DD = 13.4384
F17B_BEST_OOS_DD = 12.7647
F17C_RUNTIME_VALIDATION_PF = 1.13
F17C_RUNTIME_OOS_PF = 0.92
F17C_RUNTIME_VALIDATION_DD = 35.45
F17C_RUNTIME_OOS_DD = 47.50


@dataclass(frozen=True)
class LifecycleProfile:
    variant_id: str
    family_id: str
    max_hold_bars: int
    close_on_flat: bool
    reverse_on_opposite: bool
    atr_stop_multiplier: float
    atr_take_profit_multiplier: float
    exit_risk_overlay_enabled: bool = False


PROFILES: tuple[LifecycleProfile, ...] = (
    LifecycleProfile(
        variant_id="f18b_hold4_flat_close_atr1p2_tp2p4",
        family_id="short_profit_lock_flat_close",
        max_hold_bars=4,
        close_on_flat=True,
        reverse_on_opposite=False,
        atr_stop_multiplier=1.2,
        atr_take_profit_multiplier=2.4,
    ),
    LifecycleProfile(
        variant_id="f18b_hold6_reverse_atr1p5_tp3p0",
        family_id="balanced_reverse_on_opposite",
        max_hold_bars=6,
        close_on_flat=False,
        reverse_on_opposite=True,
        atr_stop_multiplier=1.5,
        atr_take_profit_multiplier=3.0,
    ),
    LifecycleProfile(
        variant_id="f18b_hold8_exit_risk_overlay_atr1p0_tp2p0",
        family_id="exit_risk_overlay_early_damage_control",
        max_hold_bars=8,
        close_on_flat=True,
        reverse_on_opposite=False,
        atr_stop_multiplier=1.0,
        atr_take_profit_multiplier=2.0,
        exit_risk_overlay_enabled=True,
    ),
)


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    stage_context = validate_stage_context()
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    result = train_and_evaluate(full, raw, feature_order)
    final = build_final(created_at, result, source_integrity, feature_order, stage_context)
    artifacts = write_artifacts(result, final)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "run_id": RUN_ID,
                    "strict_scout_clue_rows": final["strict_scout_clue_rows"],
                    "seed_surface_rows": final["seed_surface_rows"],
                    "preserved_clue_rows": final["preserved_clue_rows"],
                    "best_candidate": final["best_candidate_row"].get("candidate_id"),
                    "next_run_id": final["next_run_id"],
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def validate_stage_context() -> dict[str, Any]:
    required = [STAGE_BRIEF, PROFILE_SPEC, DO_NOT_REPEAT, F18A_REPORT, GROK_STAGE_OPEN_OUTPUT]
    missing = [path.as_posix() for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing Frontier18 stage-open context: {missing}")
    workspace = read_text(f03b.WORKSPACE_STATE)
    profile_text = read_text(PROFILE_SPEC)
    guard_text = read_text(DO_NOT_REPEAT)
    grok_text = read_text(GROK_STAGE_OPEN_OUTPUT).lower()
    profile_ids = [profile.variant_id for profile in PROFILES]
    checks = {
        "workspace_current_stage_matches": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_matches": f"next_run_id: {RUN_ID}" in workspace,
        "profile_count_locked_to_three": len(PROFILES) == 3,
        "profile_ids_in_spec": all(profile_id in profile_text for profile_id in profile_ids),
        "stage344_negative_memory_disclosed": "stage344" in guard_text.lower(),
        "stage337_negative_memory_disclosed": "stage337" in guard_text.lower(),
        "runtime_probe_guard_present": "runtime_probe" in guard_text.lower() or "runtime probe" in guard_text.lower(),
        "stage_open_grok_available": "classification" in grok_text and "accepted" in grok_text,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier18 tracked stage context failed checks: {json.dumps(checks, ensure_ascii=False)}")
    return {
        "stage_brief": artifact_identity(STAGE_BRIEF),
        "profile_spec": artifact_identity(PROFILE_SPEC),
        "do_not_repeat": artifact_identity(DO_NOT_REPEAT),
        "frontier18a_report": artifact_identity(F18A_REPORT),
        "frontier18a_summary": artifact_identity(F18A_SUMMARY),
        "grok_stage_open_output": artifact_identity(GROK_STAGE_OPEN_OUTPUT),
        "checks": checks,
        "stage_open_artifact_boundary": (
            "tracked_stage_docs_plus_stage_open_summary_if_available"
            "(추적 단계 문서와 가능하면 단계 개방 요약 사용)"
        ),
    }


def train_and_evaluate(full: pd.DataFrame, raw: pd.DataFrame, feature_order: list[str]) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values.")
    labels = full["label_class"].astype("int64").to_numpy()
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    missing_classes = sorted(set(LABEL_ORDER) - set(int(value) for value in labels[train_mask]))
    if missing_classes:
        raise RuntimeError(f"Train labels missing classes: {missing_classes}")

    sample_indices = np.concatenate(
        [np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256] for split in ("train", "validation", "oos")]
    )

    model_metrics: list[dict[str, Any]] = []
    subperiod_metrics: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    profile_audit_rows: list[dict[str, Any]] = []
    trade_rows: list[dict[str, Any]] = []
    model_artifacts: list[dict[str, Any]] = []

    for profile in PROFILES:
        profile_audit_rows.extend(profile_feasibility_rows(full, profile))

    for spec in f04d.MODEL_SPECS:
        model_short = MODEL_ID_SHORT.get(spec.model_id, spec.model_id[:12])
        model_instance_id = f"f18b_entry_{model_short}"
        model = clone(spec.estimator)
        model.fit(x_all[train_mask], labels[train_mask])
        probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
        pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
        signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")

        target_dir = MODEL_DIR / model_instance_id
        io_path(target_dir).mkdir(parents=True, exist_ok=True)
        model_path = target_dir / f"{model_instance_id}.joblib"
        onnx_path = target_dir / f"{model_instance_id}.onnx"
        joblib.dump(model, io_path(model_path))
        export_meta = export_sklearn_to_onnx_zipmap_disabled(
            model,
            onnx_path,
            feature_count=x_all.shape[1],
            target_opset=12,
            drop_label_output=False,
        )
        parity = check_onnxruntime_probability_parity(
            model,
            onnx_path,
            x_all[sample_indices],
            class_order=LABEL_ORDER,
            tolerance=1e-5,
        )
        parity_rows.append(
            {
                "model_id": spec.model_id,
                "model_instance_id": model_instance_id,
                "onnx_path": onnx_path.as_posix(),
                "onnx_sha256": export_meta["sha256"],
                "joblib_path": model_path.as_posix(),
                "joblib_sha256": sha256_file(model_path),
                "parity_passed": bool(parity["passed"]),
                "parity_max_abs_diff": parity["max_abs_diff"],
                "parity_mean_abs_diff": parity["mean_abs_diff"],
                "rows_checked": parity["rows"],
                "input_name": parity["input_name"],
                "output_names": "|".join(parity["output_names"]),
            }
        )
        model_artifacts.append(
            {
                "model_id": spec.model_id,
                "model_instance_id": model_instance_id,
                "joblib_path": model_path.as_posix(),
                "joblib_sha256": sha256_file(model_path),
                "onnx_path": onnx_path.as_posix(),
                "onnx_sha256": export_meta["sha256"],
                "availability": "generated_ignored_with_manifest(생성됨, 목록으로 추적)",
            }
        )
        classification_rows.extend(classification_metrics(full, labels, pred_label, spec.model_id, model_instance_id))

        for profile in PROFILES:
            candidate_id = f"{profile.variant_id}__{model_short}__lifecycle"
            simulated = simulate_profile(full, raw, signal, profile, candidate_id, spec.model_id, model_instance_id)
            model_metrics.extend(simulated["metrics"])
            subperiod_metrics.extend(simulated["subperiod_metrics"])
            trade_rows.extend(simulated["trades"])

    candidate_summary = build_candidate_summary(model_metrics, subperiod_metrics, parity_rows, classification_rows)
    return {
        "model_metrics": model_metrics,
        "subperiod_metrics": subperiod_metrics,
        "classification_metrics": classification_rows,
        "onnx_parity": parity_rows,
        "profile_audit": profile_audit_rows,
        "trade_log": trade_rows,
        "candidate_summary": candidate_summary,
        "model_artifacts": model_artifacts,
    }


def simulate_profile(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    signal: np.ndarray,
    profile: LifecycleProfile,
    candidate_id: str,
    model_id: str,
    model_instance_id: str,
) -> dict[str, list[dict[str, Any]]]:
    trades: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        split_mask = full["split"].astype(str).eq(split).to_numpy()
        split_indexes = np.flatnonzero(split_mask)
        split_trades = simulate_split(full, raw, signal, profile, candidate_id, model_id, model_instance_id, split_indexes, split)
        trades.extend(split_trades)
    metrics = [evaluate_trade_rows(trades, profile, candidate_id, model_id, model_instance_id, split, "aggregate", split) for split in ("train", "validation", "oos")]
    subperiod_metrics = evaluate_subperiods(trades, profile, candidate_id, model_id, model_instance_id)
    return {"trades": trades, "metrics": metrics, "subperiod_metrics": subperiod_metrics}


def simulate_split(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    signal: np.ndarray,
    profile: LifecycleProfile,
    candidate_id: str,
    model_id: str,
    model_instance_id: str,
    split_indexes: np.ndarray,
    split: str,
) -> list[dict[str, Any]]:
    if len(split_indexes) == 0:
        return []
    raw_open = raw["open"].astype("float64").to_numpy()
    raw_high = raw["high"].astype("float64").to_numpy()
    raw_low = raw["low"].astype("float64").to_numpy()
    raw_close = raw["close"].astype("float64").to_numpy()
    max_raw_index = int(full.iloc[split_indexes]["raw_index"].max())
    trades: list[dict[str, Any]] = []
    position: dict[str, Any] | None = None

    for row_index in split_indexes:
        row = full.iloc[int(row_index)]
        raw_index = int(row["raw_index"])
        row_signal = int(signal[int(row_index)])
        if position is not None and raw_index >= int(position["entry_raw_index"]):
            exit_event = maybe_exit_position(position, raw_index, raw_high, raw_low, raw_close, row_signal, profile)
            if exit_event is not None:
                trades.append(close_trade(position, exit_event, row, profile, candidate_id, model_id, model_instance_id, split))
                reverse_side = -int(position["side"]) if exit_event["reason"] == "reverse_on_opposite" else 0
                position = None
                if reverse_side and can_open(raw_index, max_raw_index, profile, raw_open):
                    position = open_position(reverse_side, raw_index, row_index, row, raw_open, profile)
                    continue

        if position is None and row_signal != 0 and can_open(raw_index, max_raw_index, profile, raw_open):
            position = open_position(row_signal, raw_index, row_index, row, raw_open, profile)

    if position is not None:
        last_row = full.iloc[int(split_indexes[-1])]
        last_raw = min(max_raw_index, len(raw_close) - 1)
        event = {"exit_raw_index": last_raw, "exit_price": float(raw_close[last_raw]), "reason": "split_end_forced_close"}
        trades.append(close_trade(position, event, last_row, profile, candidate_id, model_id, model_instance_id, split))
    return trades


def can_open(raw_index: int, max_raw_index: int, profile: LifecycleProfile, raw_open: np.ndarray) -> bool:
    entry_raw = raw_index + 1
    if entry_raw >= len(raw_open):
        return False
    return entry_raw + profile.max_hold_bars <= max_raw_index


def open_position(
    side: int,
    raw_index: int,
    row_index: int,
    row: pd.Series,
    raw_open: np.ndarray,
    profile: LifecycleProfile,
) -> dict[str, Any]:
    entry_raw = raw_index + 1
    entry_price = float(raw_open[entry_raw])
    atr_value = float(row["atr_14"])
    if not math.isfinite(atr_value) or atr_value <= 0.0:
        atr_value = max(abs(entry_price) * 0.001, 1.0)
    return {
        "side": int(side),
        "entry_raw_index": int(entry_raw),
        "entry_signal_row_index": int(row_index),
        "entry_signal_timestamp": str(row["timestamp"]),
        "entry_price": entry_price,
        "entry_atr": atr_value,
        "stop_distance": atr_value * profile.atr_stop_multiplier,
        "take_profit_distance": atr_value * profile.atr_take_profit_multiplier,
    }


def maybe_exit_position(
    position: dict[str, Any],
    raw_index: int,
    raw_high: np.ndarray,
    raw_low: np.ndarray,
    raw_close: np.ndarray,
    row_signal: int,
    profile: LifecycleProfile,
) -> dict[str, Any] | None:
    side = int(position["side"])
    entry_raw = int(position["entry_raw_index"])
    age_bars = raw_index - entry_raw + 1
    entry_price = float(position["entry_price"])
    stop = float(position["stop_distance"])
    take_profit = float(position["take_profit_distance"])

    if side > 0:
        stop_price = entry_price - stop
        take_profit_price = entry_price + take_profit
        stop_hit = float(raw_low[raw_index]) <= stop_price
        take_hit = float(raw_high[raw_index]) >= take_profit_price
    else:
        stop_price = entry_price + stop
        take_profit_price = entry_price - take_profit
        stop_hit = float(raw_high[raw_index]) >= stop_price
        take_hit = float(raw_low[raw_index]) <= take_profit_price

    if stop_hit:
        return {"exit_raw_index": raw_index, "exit_price": stop_price, "reason": "atr_stop"}
    if take_hit:
        return {"exit_raw_index": raw_index, "exit_price": take_profit_price, "reason": "atr_take_profit"}
    if profile.close_on_flat and row_signal == 0:
        return {"exit_raw_index": raw_index, "exit_price": float(raw_close[raw_index]), "reason": "close_on_flat"}
    if profile.reverse_on_opposite and row_signal == -side:
        return {"exit_raw_index": raw_index, "exit_price": float(raw_close[raw_index]), "reason": "reverse_on_opposite"}
    if profile.exit_risk_overlay_enabled and age_bars >= 2:
        unrealized = side * (math.log(float(raw_close[raw_index])) - math.log(entry_price))
        risk_floor = -0.55 * math.log1p(stop / max(entry_price, 1e-12))
        if unrealized <= risk_floor:
            return {"exit_raw_index": raw_index, "exit_price": float(raw_close[raw_index]), "reason": "exit_risk_overlay"}
    if age_bars >= profile.max_hold_bars:
        return {"exit_raw_index": raw_index, "exit_price": float(raw_close[raw_index]), "reason": "max_hold"}
    return None


def close_trade(
    position: dict[str, Any],
    event: dict[str, Any],
    row: pd.Series,
    profile: LifecycleProfile,
    candidate_id: str,
    model_id: str,
    model_instance_id: str,
    split: str,
) -> dict[str, Any]:
    side = int(position["side"])
    entry_price = float(position["entry_price"])
    exit_price = float(event["exit_price"])
    gross_log_return = side * (math.log(exit_price) - math.log(entry_price))
    net_log_return = gross_log_return - scout.ROUGH_COST_LOG_RETURN
    return {
        "candidate_id": candidate_id,
        "target_id": profile.variant_id,
        "model_id": model_id,
        "model_instance_id": model_instance_id,
        "split": split,
        "entry_signal_timestamp": position["entry_signal_timestamp"],
        "exit_signal_timestamp": str(row["timestamp"]),
        "entry_raw_index": int(position["entry_raw_index"]),
        "exit_raw_index": int(event["exit_raw_index"]),
        "side": side,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "entry_atr": float(position["entry_atr"]),
        "hold_bars": int(event["exit_raw_index"]) - int(position["entry_raw_index"]) + 1,
        "exit_reason": event["reason"],
        "gross_log_return": gross_log_return,
        "net_log_return": net_log_return,
        "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
        "execution_boundary": (
            "closed_bar_signal_next_bar_open_proxy_stop_first_when_same_bar_ambiguous"
            "(종료봉 신호 다음 봉 시가 프록시, 같은 봉 동시 충돌은 손절 우선)"
        ),
    }


def evaluate_trade_rows(
    trades: list[dict[str, Any]],
    profile: LifecycleProfile,
    candidate_id: str,
    model_id: str,
    model_instance_id: str,
    split: str,
    granularity: str,
    period: str,
) -> dict[str, Any]:
    selected = [
        row
        for row in trades
        if row["candidate_id"] == candidate_id and row["split"] == split and (granularity == "aggregate" or row["period"] == period)
    ]
    pnl = np.asarray([float(row["net_log_return"]) for row in selected], dtype="float64")
    times = pd.Series([row["entry_signal_timestamp"] for row in selected], dtype="object")
    metrics = scout.trade_metrics(pnl, pd.to_datetime(times, utc=True)) if len(selected) else scout.trade_metrics(pnl, pd.Series([], dtype="datetime64[ns, UTC]"))
    days = count_days_for_trade_set(selected)
    trade_count = int(len(selected))
    trades_per_day = float(trade_count / days) if days else 0.0
    sparse_floor = max(5, int(math.ceil(days / 2))) if days else 5
    sparse_flag = trade_count < sparse_floor
    pf999_sparse_flag = bool(float(metrics["profit_factor"]) >= 999.0 and sparse_flag)
    dd_risk = max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"]))
    density_distance = scout.density_axis_distance(trades_per_day)
    pf_distance = scout.profit_factor_axis_distance(float(metrics["profit_factor"]), trade_count, sparse_flag, pf999_sparse_flag)
    dd_distance = max(0.0, (dd_risk - scout.DD_TARGET_PERCENT) / scout.DD_TARGET_PERCENT)
    smoothness_distance = scout.smoothness_axis_distance(metrics)
    return {
        "candidate_id": candidate_id,
        "target_id": profile.variant_id,
        "model_id": model_id,
        "model_instance_id": model_instance_id,
        "comparison_kind": "asymmetric_exit_lifecycle_simulation_proxy(비대칭 청산 생명주기 시뮬레이션 프록시)",
        "split": split,
        "granularity": granularity,
        "period": period,
        "tier_scope": "Tier A(티어 A)",
        "record_view": "Tier A separate(티어 A 분리)",
        "max_hold_bars": profile.max_hold_bars,
        "close_on_flat": profile.close_on_flat,
        "reverse_on_opposite": profile.reverse_on_opposite,
        "atr_stop_multiplier": profile.atr_stop_multiplier,
        "atr_take_profit_multiplier": profile.atr_take_profit_multiplier,
        "exit_risk_overlay_enabled": profile.exit_risk_overlay_enabled,
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": trades_per_day,
        "long_trade_count": int(sum(1 for row in selected if int(row["side"]) > 0)),
        "short_trade_count": int(sum(1 for row in selected if int(row["side"]) < 0)),
        "net_profit": metrics["net_profit"],
        "profit_factor": metrics["profit_factor"],
        "expectancy": metrics["expectancy"],
        "win_rate": metrics["win_rate"],
        "max_drawdown_percent": metrics["max_drawdown_percent"],
        "max_monthly_drawdown_percent": metrics["max_monthly_drawdown_percent"],
        "dd_risk_percent": dd_risk,
        "underwater_ratio": metrics["underwater_ratio"],
        "max_loss_streak": metrics["max_loss_streak"],
        "equity_trend_r2": metrics["equity_trend_r2"],
        "sparse_flag": bool(sparse_flag),
        "pf999_sparse_flag": bool(pf999_sparse_flag),
        "density_axis_distance": density_distance,
        "pf_axis_distance": pf_distance,
        "dd_axis_distance": dd_distance,
        "smoothness_axis_distance": smoothness_distance,
        "aspiration_distance_score": density_distance + pf_distance + dd_distance + smoothness_distance,
        "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
    }


def evaluate_subperiods(
    trades: list[dict[str, Any]],
    profile: LifecycleProfile,
    candidate_id: str,
    model_id: str,
    model_instance_id: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    candidate_trades = [row for row in trades if row["candidate_id"] == candidate_id]
    if not candidate_trades:
        return rows
    frame = pd.DataFrame(candidate_trades)
    times = pd.to_datetime(frame["entry_signal_timestamp"], utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    frame["month_period"] = times.dt.to_period("M").astype(str)
    frame["quarter_period"] = times.dt.to_period("Q").astype(str)
    for split in ("train", "validation", "oos"):
        split_frame = frame.loc[frame["split"].astype(str).eq(split)].copy()
        for column, granularity in (("month_period", "month"), ("quarter_period", "quarter")):
            for period in sorted(split_frame[column].dropna().unique()):
                marked = [dict(row) for row in split_frame.loc[split_frame[column].eq(period)].to_dict(orient="records")]
                for item in marked:
                    item["period"] = str(period)
                rows.append(
                    evaluate_trade_rows(marked, profile, candidate_id, model_id, model_instance_id, split, granularity, str(period))
                )
    return rows


def count_days_for_trade_set(trades: list[dict[str, Any]]) -> int:
    if not trades:
        return 0
    times = pd.Series([row["entry_signal_timestamp"] for row in trades])
    return scout.count_scope_days(pd.to_datetime(times, utc=True))


def profile_feasibility_rows(full: pd.DataFrame, profile: LifecycleProfile) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    raw_index = full["raw_index"].astype("int64")
    for split in ("train", "validation", "oos"):
        frame = full.loc[full["split"].astype(str).eq(split)].copy()
        days = scout.count_scope_days(frame["timestamp"].reset_index(drop=True)) if len(frame) else 0
        enough_path = int((raw_index.loc[frame.index] + profile.max_hold_bars + 1 <= raw_index.loc[frame.index].max()).sum()) if len(frame) else 0
        rows.append(
            {
                "target_id": profile.variant_id,
                "split": split,
                "rows": int(len(frame)),
                "days_in_scope": days,
                "max_hold_bars": profile.max_hold_bars,
                "rows_with_full_lifecycle_path": enough_path,
                "full_lifecycle_path_fraction": float(enough_path / len(frame)) if len(frame) else 0.0,
                "profile_boundary": "pre_registered_stage_open_profile(단계 개방 때 사전 등록한 프로필)",
            }
        )
    return rows


def classification_metrics(
    full: pd.DataFrame,
    labels: np.ndarray,
    pred_label: np.ndarray,
    model_id: str,
    model_instance_id: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = full["split"].astype(str).eq(split).to_numpy()
        y_true = labels[mask]
        y_pred = pred_label[mask]
        rows.append(
            {
                "model_id": model_id,
                "model_instance_id": model_instance_id,
                "split": split,
                "rows": int(mask.sum()),
                "accuracy": float(accuracy_score(y_true, y_pred)),
                "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
                "macro_f1": float(f1_score(y_true, y_pred, labels=LABEL_ORDER, average="macro", zero_division=0)),
                "pred_short": int((y_pred == 0).sum()),
                "pred_flat": int((y_pred == 1).sum()),
                "pred_long": int((y_pred == 2).sum()),
                "true_short": int((y_true == 0).sum()),
                "true_flat": int((y_true == 1).sum()),
                "true_long": int((y_true == 2).sum()),
            }
        )
    return rows


def build_candidate_summary(
    model_metrics: list[dict[str, Any]],
    subperiod_metrics: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
    classification_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    metrics_by_candidate: dict[str, list[dict[str, Any]]] = {}
    for row in model_metrics:
        metrics_by_candidate.setdefault(str(row["candidate_id"]), []).append(row)
    sub_by_candidate: dict[str, list[dict[str, Any]]] = {}
    for row in subperiod_metrics:
        sub_by_candidate.setdefault(str(row["candidate_id"]), []).append(row)
    parity_by_model = {str(row["model_instance_id"]): row for row in parity_rows}
    class_by_model_split = {(str(row["model_instance_id"]), str(row["split"])): row for row in classification_rows}

    summaries: list[dict[str, Any]] = []
    for candidate_id, rows in metrics_by_candidate.items():
        split_rows = {str(row["split"]): row for row in rows if row["granularity"] == "aggregate"}
        if "validation" not in split_rows or "oos" not in split_rows:
            continue
        val = split_rows["validation"]
        oos = split_rows["oos"]
        subs = [row for row in sub_by_candidate.get(candidate_id, []) if row["split"] in {"validation", "oos"}]
        worst_sub_dd = max([float(row["dd_risk_percent"]) for row in subs], default=999.0)
        negative_subperiod_fraction = float(np.mean([float(row["net_profit"]) <= 0.0 for row in subs])) if subs else 1.0
        subperiod_density_min = min([float(row["trades_per_day"]) for row in subs], default=0.0)
        model_instance_id = str(val["model_instance_id"])
        parity = parity_by_model.get(model_instance_id, {})
        validation_class = class_by_model_split.get((model_instance_id, "validation"), {})
        oos_class = class_by_model_split.get((model_instance_id, "oos"), {})
        parity_passed = bool(parity.get("parity_passed"))
        strict = all(
            [
                parity_passed,
                metric_pass(val, density_low=SCOUT_DENSITY_LOW, density_high=SCOUT_DENSITY_HIGH),
                metric_pass(oos, density_low=SCOUT_DENSITY_LOW, density_high=SCOUT_DENSITY_HIGH),
                worst_sub_dd <= SCOUT_WORST_SUBPERIOD_DD_CEILING,
                negative_subperiod_fraction <= 0.25,
            ]
        )
        density_seed = (
            SEED_DENSITY_LOW <= float(val["trades_per_day"]) <= SEED_DENSITY_HIGH
            and SEED_DENSITY_LOW <= float(oos["trades_per_day"]) <= SEED_DENSITY_HIGH
        )
        pf_not_below_reference = float(val["profit_factor"]) >= F17C_RUNTIME_VALIDATION_PF and float(oos["profit_factor"]) >= F17C_RUNTIME_OOS_PF
        dd_better_than_reference = float(val["dd_risk_percent"]) < F17C_RUNTIME_VALIDATION_DD and float(oos["dd_risk_percent"]) < F17C_RUNTIME_OOS_DD
        seed = all(
            [
                parity_passed,
                float(val["net_profit"]) > 0.0,
                float(oos["net_profit"]) > 0.0,
                density_seed,
                pf_not_below_reference,
                dd_better_than_reference,
                float(val["dd_risk_percent"]) <= 18.0,
                float(oos["dd_risk_percent"]) <= 18.0,
                worst_sub_dd <= 30.0,
                negative_subperiod_fraction <= 0.35,
            ]
        )
        preserved = all(
            [
                parity_passed,
                float(val["net_profit"]) > 0.0,
                float(oos["net_profit"]) > 0.0,
                min(float(val["trades_per_day"]), float(oos["trades_per_day"])) >= 2.0,
                max(float(val["trades_per_day"]), float(oos["trades_per_day"])) <= 12.0,
                dd_better_than_reference,
                (float(oos["profit_factor"]) >= F17B_BEST_OOS_PF or float(oos["dd_risk_percent"]) < F17B_BEST_OOS_DD),
                worst_sub_dd <= 35.0,
            ]
        )
        score = (
            float(val["aspiration_distance_score"])
            + float(oos["aspiration_distance_score"])
            + (worst_sub_dd / 10.0)
            + negative_subperiod_fraction
            + (0.0 if seed else 1.0)
            + (0.0 if preserved else 2.0)
        )
        summaries.append(
            {
                "candidate_id": candidate_id,
                "target_id": val["target_id"],
                "model_id": val["model_id"],
                "model_instance_id": model_instance_id,
                "strict_scout_clue_pass": bool(strict),
                "seed_surface_pass": bool(seed),
                "preserved_clue_pass": bool(preserved),
                "lifecycle_score": score,
                "validation_profit_factor": val["profit_factor"],
                "validation_trades_per_day": val["trades_per_day"],
                "validation_dd_risk_percent": val["dd_risk_percent"],
                "validation_net_profit": val["net_profit"],
                "validation_equity_trend_r2": val["equity_trend_r2"],
                "oos_profit_factor": oos["profit_factor"],
                "oos_trades_per_day": oos["trades_per_day"],
                "oos_dd_risk_percent": oos["dd_risk_percent"],
                "oos_net_profit": oos["net_profit"],
                "oos_equity_trend_r2": oos["equity_trend_r2"],
                "validation_oos_subperiod_worst_dd_risk_percent": worst_sub_dd,
                "validation_oos_negative_subperiod_fraction": negative_subperiod_fraction,
                "validation_oos_subperiod_min_trades_per_day": subperiod_density_min,
                "parity_passed": parity_passed,
                "onnx_path": parity.get("onnx_path", ""),
                "onnx_sha256": parity.get("onnx_sha256", ""),
                "joblib_path": parity.get("joblib_path", ""),
                "joblib_sha256": parity.get("joblib_sha256", ""),
                "validation_macro_f1": validation_class.get("macro_f1", ""),
                "oos_macro_f1": oos_class.get("macro_f1", ""),
                "pf_not_below_f17c_runtime_reference": bool(pf_not_below_reference),
                "dd_better_than_f17c_runtime_reference": bool(dd_better_than_reference),
                "signal_contract": (
                    "fixed_fwd12_argmax_entry_plus_pre_registered_lifecycle_exit"
                    "(고정 fwd12 최대확률 진입과 사전 등록 생명주기 청산)"
                ),
            }
        )
    summaries.sort(
        key=lambda row: (
            not bool(row["strict_scout_clue_pass"]),
            not bool(row["seed_surface_pass"]),
            not bool(row["preserved_clue_pass"]),
            float(row["lifecycle_score"]),
        )
    )
    return json_ready(summaries)


def metric_pass(row: dict[str, Any], *, density_low: float, density_high: float) -> bool:
    return all(
        [
            float(row["net_profit"]) > 0.0,
            float(row["profit_factor"]) >= SCOUT_PF_FLOOR,
            density_low <= float(row["trades_per_day"]) <= density_high,
            float(row["dd_risk_percent"]) <= SCOUT_DD_CEILING,
        ]
    )


def build_final(
    created_at: str,
    result: dict[str, Any],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    stage_context: dict[str, Any],
) -> dict[str, Any]:
    candidate_summary = result["candidate_summary"]
    best = candidate_summary[0] if candidate_summary else {}
    strict_rows = [row for row in candidate_summary if row.get("strict_scout_clue_pass")]
    seed_rows = [row for row in candidate_summary if row.get("seed_surface_pass")]
    preserved_rows = [row for row in candidate_summary if row.get("preserved_clue_pass")]
    if strict_rows:
        status = "asymmetric_exit_lifecycle_strict_scout_clue_no_authority"
        judgment = "scout_clue(탐색 단서)"
        next_run_id = NEXT_GROK_RUN_ID
    elif seed_rows:
        status = "asymmetric_exit_lifecycle_seed_surface_no_authority"
        judgment = "seed_surface_candidate(씨앗 표면 후보)"
        next_run_id = NEXT_GROK_RUN_ID
    elif preserved_rows:
        status = "asymmetric_exit_lifecycle_preserved_clue_no_authority"
        judgment = "preserved_clue_candidate(보존 단서 후보)"
        next_run_id = NEXT_GROK_RUN_ID
    elif candidate_summary:
        status = "asymmetric_exit_lifecycle_no_forward_clue_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run_id = NEXT_REPAIR_RUN_ID
    else:
        status = "asymmetric_exit_lifecycle_invalid_no_candidate_no_authority"
        judgment = "invalid_setup_candidate(무효 설정 후보)"
        next_run_id = NEXT_REPAIR_RUN_ID
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "strict_scout_clue_rows": len(strict_rows),
        "seed_surface_rows": len(seed_rows),
        "preserved_clue_rows": len(preserved_rows),
        "candidate_row_count": len(candidate_summary),
        "best_candidate_row": best,
        "profile_count": len(PROFILES),
        "model_count": len(f04d.MODEL_SPECS),
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "source_integrity": source_integrity,
        "stage_context": stage_context,
        "data_integrity": data_integrity_record(source_integrity, feature_order),
        "model_validation": model_validation_record(best),
        "artifact_lineage": artifact_lineage_record(),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "wfo_status": "not_run_requires_grok_pre_expensive_before_wfo_or_mt5(WFO/MT5 전 Grok 검토 필요)",
        "mt5_status": "not_run_proxy_only_runtime_probe_required_before_closeout(프록시 전용, 마감 전 런타임 탐침 필요)",
    }


def data_integrity_record(source_integrity: dict[str, Any], feature_order: list[str]) -> dict[str, Any]:
    return {
        "data_source": f03b.DATASET_PATH.as_posix(),
        "time_axis": "US100 M5 closed-bar timestamps, UTC storage, New York calendar for grouping(US100 M5 종료봉 타임스탬프, UTC 저장, 뉴욕 달력 그룹)",
        "sample_scope": "Tier A full-context fixed train/validation/OOS split(티어 A 전체 문맥 고정 학습/검증/표본외 분할)",
        "missing_or_duplicate_check": source_integrity.get("integrity_judgment", "source_integrity_carried_with_boundary"),
        "feature_label_boundary": "features closed at signal bar; lifecycle proxy uses future raw OHLC only for evaluation(피처는 신호봉 종료 기준, 생명주기 프록시는 평가용 미래 OHLC 사용)",
        "split_boundary": "models fit train only; lifecycle profiles pre-registered before proxy result(모델은 학습 구간만 적합, 생명주기 프로필은 결과 전 사전 등록)",
        "leakage_risk": "proxy exit path is evaluation path, not model input(프록시 청산 경로는 평가 경로이지 모델 입력 아님)",
        "data_hash_or_identity": {
            "dataset_sha256": sha256_file(f03b.DATASET_PATH),
            "feature_order_sha256": sha256_file(f03b.FEATURE_ORDER_PATH),
            "feature_order_hash": ordered_hash(feature_order),
        },
        "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 포함 사용 가능)",
    }


def model_validation_record(best: dict[str, Any]) -> dict[str, Any]:
    return {
        "model_family": "fixed sklearn-to-ONNX class probability models(고정 sklearn-to-ONNX 분류 확률 모델)",
        "target_and_label": "existing fwd12 label_class used only for entry seed(기존 fwd12 label_class를 진입 씨앗에만 사용)",
        "split_method": "fixed train/validation/OOS split, no WFO yet(고정 학습/검증/표본외 분할, WFO 아직 없음)",
        "selection_metric": "strict clue, seed surface, preserved clue, then lifecycle score(엄격 단서, 씨앗 표면, 보존 단서, 생명주기 점수 순)",
        "secondary_metrics": "PF, density, DD, subperiod DD, negative subperiod fraction, ONNX parity(PF, 빈도, 손실폭, 하위기간 손실폭, 부정 하위기간 비율, ONNX 동등성)",
        "threshold_policy": "argmax entry only; no score-rank density calibration(최대확률 진입만 사용, 점수 순위 빈도 보정 없음)",
        "overfit_risk": "single proxy pass without WFO; next expensive check requires Grok review(WFO 없는 단일 프록시 회차, 비싼 검증 전 Grok 검토 필요)",
        "runtime_risk": "Python lifecycle simulation is not MT5 runtime parity(파이썬 생명주기 시뮬레이션은 MT5 런타임 동등성 아님)",
        "comparison_baseline": "F17 proxy/runtime observations are reference-only(F17 프록시/런타임 관찰은 참조 전용)",
        "validation_judgment": "exploratory_scout_only(탐색 전용)",
        "best_candidate": best.get("candidate_id", "none"),
    }


def artifact_lineage_record() -> dict[str, Any]:
    return {
        "source_inputs": [
            f03b.DATASET_PATH.as_posix(),
            f03b.FEATURE_ORDER_PATH.as_posix(),
            STAGE_BRIEF.as_posix(),
            PROFILE_SPEC.as_posix(),
            DO_NOT_REPEAT.as_posix(),
            GROK_STAGE_OPEN_OUTPUT.as_posix(),
        ],
        "producer": SCRIPT_PATH.as_posix(),
        "consumer": REPORT_PATH.as_posix(),
        "artifact_paths": [RUN_ROOT.as_posix(), REPORT_PATH.as_posix()],
        "artifact_hashes": "run_manifest records evidence and generated model hashes(실행 목록이 근거와 생성 모델 해시를 기록)",
        "registry_links": [
            f03b.RUN_REGISTRY.as_posix(),
            f03b.ALPHA_LEDGER.as_posix(),
            (STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv").as_posix(),
        ],
        "availability": "small_evidence_force_trackable_models_ignored_with_manifest(작은 근거는 강제 추적 가능, 모델은 목록으로 추적)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
    }


def write_artifacts(result: dict[str, Any], final: dict[str, Any]) -> dict[str, Path]:
    artifacts = {
        "profile_manifest": RUN_ROOT / "profile_manifest.csv",
        "profile_audit": RUN_ROOT / "profile_audit.csv",
        "model_metrics": RUN_ROOT / "model_metrics.csv",
        "subperiod_metrics": RUN_ROOT / "subperiod_metrics.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "trade_log": RUN_ROOT / "trade_log.csv",
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "final_decision": RUN_ROOT / "final_decision.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_csv(artifacts["profile_manifest"], [asdict(profile) for profile in PROFILES])
    write_csv(artifacts["profile_audit"], result["profile_audit"])
    write_csv(artifacts["model_metrics"], result["model_metrics"])
    write_csv(artifacts["subperiod_metrics"], result["subperiod_metrics"])
    write_csv(artifacts["classification_metrics"], result["classification_metrics"])
    write_csv(artifacts["onnx_parity"], result["onnx_parity"])
    write_csv(artifacts["trade_log"], result["trade_log"])
    write_csv(artifacts["candidate_summary"], result["candidate_summary"])
    write_json(artifacts["final_decision"], final)
    manifest = {
        **final,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "dataset": artifact_identity(f03b.DATASET_PATH),
        "feature_order": artifact_identity(f03b.FEATURE_ORDER_PATH),
        "artifacts": {key: path.as_posix() for key, path in artifacts.items()},
        "artifact_identities": {key: artifact_identity(path) for key, path in artifacts.items() if key != "run_manifest"},
        "model_artifacts": result["model_artifacts"],
        "regeneration_command": f"python {SCRIPT_PATH.as_posix()}",
    }
    write_json(artifacts["run_manifest"], manifest)
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    text = f"""# Frontier18B Asymmetric Exit Lifecycle Proxy Scout(전선18B 비대칭 청산 생명주기 프록시 탐색)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): fixed fwd12 entry ONNX models(고정 fwd12 진입 ONNX 모델)에 3 pre-registered lifecycle profiles(사전 등록 생명주기 프로필)를 붙여 validation/OOS(검증/표본외) proxy path(프록시 경로)를 시뮬레이션했습니다.

Effect(효과): F17 loss-cluster firewall(손실 군집 방화벽)을 상속하지 않고, 이번 가설의 exit lifecycle(청산 생명주기) 축이 PF/density/DD/smoothness(PF/빈도/손실폭/매끄러움)에 주는 영향을 분리해서 봅니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `{final['candidate_row_count']}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- seed surface rows(씨앗 표면 행): `{final['seed_surface_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- best candidate(최선 후보): `{best.get('candidate_id', 'none')}`
- validation PF/density/DD(검증 PF/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본외 PF/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- worst subperiod DD(최악 하위기간 손실폭): `{fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}%`
- negative subperiod fraction(부정 하위기간 비율): `{fmt(best.get('validation_oos_negative_subperiod_fraction'))}`
- ONNX parity(ONNX 동등성): `{best.get('parity_passed', 'n/a')}`

## Artifacts(산출물)

- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- model metrics(모델 지표): `{artifacts['model_metrics'].as_posix()}`
- subperiod metrics(하위기간 지표): `{artifacts['subperiod_metrics'].as_posix()}`
- trade log(거래 기록): `{artifacts['trade_log'].as_posix()}`
- ONNX parity(ONNX 동등성): `{artifacts['onnx_parity'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Boundaries(경계)

Evidence boundary(근거 경계): proxy-only(프록시 전용)이며, Python OHLC lifecycle simulation(파이썬 OHLC 생명주기 시뮬레이션)은 MT5 runtime parity(MT5 런타임 동등성)가 아닙니다.

Missing evidence(부족 근거): WFO(워크포워드 최적화), stress(스트레스), MT5 runtime probe(MT5 런타임 탐침)는 아직 실행하지 않았습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.

Next action(다음 행동): `{final['next_run_id']}`. Effect(효과): 비싼 WFO/MT5(워크포워드/MT5) 또는 repair/closeout(수리/마감) 전 단계에서 claim boundary(주장 경계)를 유지합니다.
"""
    f03b.write_text_sig(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(final))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(final))
    upsert_csv_io(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    for row in ledger_rows(final):
        upsert_csv_io(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv_io(stage_ledger, "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): strict={final['strict_scout_clue_rows']}, seed={final['seed_surface_rows']}, preserved={final['preserved_clue_rows']}, next `{final['next_run_id']}`.\n",
    )


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"current_stage_id: {STAGE_ID}",
            f"current_run_id: {RUN_ID}",
            f"latest_completed_run_id: {RUN_ID}",
            f"current_status: {final['status']}",
            f"current_judgment: {final['judgment']}",
            f"next_run_id: {final['next_run_id']}",
            "runtime_authority: not_claimed",
            "operating_promotion: not_claimed",
            "goal_achieve: not_claimed",
            f"updated_at_utc: '{final['created_at_utc']}'",
            "",
        ]
    )


def current_working_state(final: dict[str, Any]) -> str:
    best = final["best_candidate_row"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier18B(전선18B)가 asymmetric exit lifecycle proxy scout(비대칭 청산 생명주기 프록시 탐색)를 실행했습니다.

Effect(효과): best candidate(최선 후보) `{best.get('candidate_id', 'none')}`의 PF-density-DD(PF-빈도-손실폭)를 기록했고, MT5 runtime probe(MT5 런타임 탐침) 전에는 권위 주장을 하지 않습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_candidate_row"]
    return f"""# Frontier18 Selection Status(전선18 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Best candidate(최선 후보): `{best.get('candidate_id', 'none')}`

Strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`

Seed surface rows(씨앗 표면 행): `{final['seed_surface_rows']}`

Preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{final['next_run_id']}`

Key artifacts(핵심 산출물): `{artifacts['candidate_summary'].as_posix()}`, `{artifacts['trade_log'].as_posix()}`
"""


def review_index(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier18 Review Index(전선18 검토 색인)

Updated(갱신): {final['created_at_utc']}

- `{PARENT_RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용), lifecycle profile locks(생명주기 프로필 고정), runtime probe obligation(런타임 탐침 의무) recorded(기록).
- `{RUN_ID}`: proxy scout(프록시 탐색), strict rows(엄격 행) `{final['strict_scout_clue_rows']}`, seed rows(씨앗 행) `{final['seed_surface_rows']}`, preserved rows(보존 행) `{final['preserved_clue_rows']}`.
- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- trade log(거래 기록): `{artifacts['trade_log'].as_posix()}`
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier18B Required Gate Coverage Audit(전선18B 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- scope_completion_gate(범위 완료 게이트): 3 profiles(프로필) x 3 model specs(모델 규격)을 실행했습니다.
- kpi_contract_audit(KPI 계약 감사): validation/OOS PF-density-DD(검증/표본외 PF-빈도-손실폭), subperiod DD(하위기간 손실폭), negative subperiod fraction(부정 하위기간 비율)을 기록했습니다.
- data_integrity_gate(데이터 무결성 게이트): `{final['data_integrity']['integrity_judgment']}`
- model_validation_gate(모델 검증 게이트): `{final['model_validation']['validation_judgment']}`
- artifact_lineage_gate(산출물 계보 게이트): `{final['artifact_lineage']['lineage_judgment']}`
- tier_pair_gate(티어 쌍 게이트): Tier A separate(티어 A 분리)는 기록했고, Tier B/combined(티어 B/합산)는 missing_required(필수 누락)로 기록했습니다.
- onnx_parity_gate(ONNX 동등성 게이트): 후보 모델별 ONNX parity(ONNX 동등성)를 기록했습니다. 통과 없는 후보는 clue(단서)로 판정하지 않습니다.
- runtime_probe_obligation_gate(런타임 탐침 의무 게이트): closeout(마감) 전 MT5 runtime probe(MT5 런타임 탐침) 또는 exact blocked reason(정확한 차단 사유)이 필요합니다.
- final_claim_guard(최종 주장 보호): completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장) 없음.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "asymmetric_exit_lifecycle_proxy_scout(비대칭 청산 생명주기 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": (
            f"strict={final['strict_scout_clue_rows']};seed={final['seed_surface_rows']};"
            f"preserved={final['preserved_clue_rows']};no_wfo_no_mt5_no_authority"
        ),
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["candidate_row_count"]),
        "claim_boundary": "proxy_scout_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_kpi": primary_kpi_text(best),
        "guardrail_kpi": "pre_registered_lifecycle_profiles_no_density_calibration(사전 등록 생명주기 프로필, 빈도 보정 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5_yet(주장 범위 밖, MT5 아직 없음)",
        "result_path": REPORT_PATH.as_posix(),
        "final_decision_path": artifacts["final_decision"].as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_candidate_row"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "asymmetric_exit_lifecycle_proxy_scout(비대칭 청산 생명주기 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "fixed_entry_pre_registered_lifecycle_no_wfo_no_mt5_no_authority(고정 진입, 사전 등록 생명주기, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5_yet(주장 범위 밖, MT5 아직 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_asymmetric_exit_lifecycle_proxy",
            "subrun_id": f"{RUN_ID}__tier_a_asymmetric_exit_lifecycle_proxy",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "asymmetric_exit_lifecycle_proxy_not_runtime(비대칭 청산 생명주기 프록시, 런타임 아님)",
            "primary_kpi": primary_kpi_text(best),
            "notes": f"strict={final['strict_scout_clue_rows']};seed={final['seed_surface_rows']};preserved={final['preserved_clue_rows']};no_authority",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_paired_source(필수 누락, 쌍 원천 없음)",
            "notes": "Tier B paired materialization not available(티어 B 쌍 물질화 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_combined_claim(필수 누락, 합산 주장 없음)",
            "notes": "combined record blocked by missing Tier B(티어 B 부재로 합산 기록 차단)",
        },
    ]


def primary_kpi_text(best: dict[str, Any]) -> str:
    return (
        f"best={best.get('candidate_id', 'none')};"
        f"strict={best.get('strict_scout_clue_pass', False)};"
        f"seed={best.get('seed_surface_pass', False)};"
        f"preserved={best.get('preserved_clue_pass', False)};"
        f"val_pf={fmt(best.get('validation_profit_factor'))};"
        f"val_density={fmt(best.get('validation_trades_per_day'))};"
        f"val_dd={fmt(best.get('validation_dd_risk_percent'))};"
        f"oos_pf={fmt(best.get('oos_profit_factor'))};"
        f"oos_density={fmt(best.get('oos_trades_per_day'))};"
        f"oos_dd={fmt(best.get('oos_dd_risk_percent'))};"
        f"worst_sub_dd={fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}"
    )


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = read_csv_header_io(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_csv_header_io(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv_io(path: Path, key: str, row: dict[str, Any]) -> None:
    header = read_csv_header_io(path)
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
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: f03b.stringify(item.get(column, "")) for column in header})


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    pd.DataFrame(json_ready(rows)).to_csv(io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if not math.isfinite(number):
        return "inf"
    return f"{number:.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
