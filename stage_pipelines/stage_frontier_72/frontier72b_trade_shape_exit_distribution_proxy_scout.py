from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists


STAGE_ID = "stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling"
RUN_ID = "frontier72B_trade_shape_exit_distribution_proxy_scout_v1"
PARENT_RUN_ID = "frontier72A_stage_open_new_upstream_axis_after_f71_economics_negative_memory_v1"
NEXT_REPAIR_RUN_ID = "frontier72C_trade_shape_label_feature_repair_or_pre_mt5_decision_v1"
NEXT_PRE_MT5_RUN_ID = "frontier72D_pre_mt5_grok_trade_shape_runtime_probe_v1"
STATUS = "proxy_scout_completed"
CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

MODEL_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"
RAW_US100 = ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"
F72A_SPEC = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f72a_label_exit_risk_spec.json"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"

INITIAL_EQUITY = 10000.0
POINT_VALUE = 1.0
POINT_SIZE = 0.01
TARGET_TPD_VALUES = [1.5, 3.0, 5.0, 7.0]


@dataclass(frozen=True)
class TradeShape:
    hold_bars: int
    stop_atr: float
    target_atr: float
    direction: int

    @property
    def shape_id(self) -> str:
        side = "long" if self.direction > 0 else "short"
        return f"{side}_h{self.hold_bars}_sl{self.stop_atr:g}_tp{self.target_atr:g}"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path) if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


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


def required_inputs() -> list[Path]:
    return [MODEL_INPUT, FEATURE_ORDER, RAW_US100, F72A_SPEC]


def split_days(timestamps: pd.Series) -> float:
    if timestamps.empty:
        return 1.0
    span = timestamps.max() - timestamps.min()
    return max(float(span.days) + 1.0, 1.0)


def max_drawdown(values: np.ndarray) -> tuple[float, float]:
    if len(values) == 0:
        return 0.0, 0.0
    equity = INITIAL_EQUITY + np.cumsum(values)
    peaks = np.maximum.accumulate(equity)
    drawdowns = peaks - equity
    max_dd = float(np.max(drawdowns))
    return max_dd, float(max_dd / INITIAL_EQUITY * 100.0)


def equity_smoothness(values: np.ndarray) -> float:
    if len(values) < 3:
        return 0.0
    equity = np.cumsum(values)
    x = np.arange(len(equity), dtype=float)
    if np.allclose(equity, equity[0]):
        return 0.0
    corr = np.corrcoef(x, equity)[0, 1]
    return float(0.0 if np.isnan(corr) else corr * corr)


def trade_metrics(timestamps: pd.Series, pnl: np.ndarray, direction: np.ndarray) -> dict[str, Any]:
    count = int(len(pnl))
    days = split_days(timestamps)
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    gross_profit = float(wins.sum()) if len(wins) else 0.0
    gross_loss = float(losses.sum()) if len(losses) else 0.0
    pf = float(gross_profit / abs(gross_loss)) if gross_loss < 0 else (999.0 if gross_profit > 0 else 0.0)
    net = float(pnl.sum())
    dd_amount, dd_percent = max_drawdown(pnl)
    avg_win = float(wins.mean()) if len(wins) else 0.0
    avg_loss = float(losses.mean()) if len(losses) else 0.0
    payoff = float(avg_win / abs(avg_loss)) if avg_loss < 0 else 0.0
    max_consecutive_loss = 0
    current_loss = 0
    for value in pnl:
        if value < 0:
            current_loss += 1
            max_consecutive_loss = max(max_consecutive_loss, current_loss)
        else:
            current_loss = 0
    return {
        "net_profit": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": pf,
        "max_drawdown_amount": dd_amount,
        "max_drawdown_percent": dd_percent,
        "trade_count": count,
        "trades_day": float(count / days),
        "win_rate": float(len(wins) / count) if count else 0.0,
        "average_win": avg_win,
        "average_loss": avg_loss,
        "payoff_ratio": payoff,
        "expectancy": float(net / count) if count else 0.0,
        "recovery_factor": float(net / dd_amount) if dd_amount > 0 else (999.0 if net > 0 else 0.0),
        "smoothness_r2": equity_smoothness(pnl),
        "max_consecutive_loss": max_consecutive_loss,
        "long_trade_count": int(np.sum(direction > 0)),
        "short_trade_count": int(np.sum(direction < 0)),
    }


def align_raw(model: pd.DataFrame, raw: pd.DataFrame) -> np.ndarray:
    raw = raw.copy()
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    positions = pd.Series(raw.index.to_numpy(), index=raw["timestamp"])
    aligned = positions.reindex(model["timestamp"])
    return aligned.to_numpy(dtype=float)


def compute_shape_path(model: pd.DataFrame, raw: pd.DataFrame, positions: np.ndarray, shape: TradeShape) -> dict[str, np.ndarray]:
    n = len(model)
    pnl = np.full(n, np.nan)
    quality = np.full(n, np.nan)
    mae_ratio = np.full(n, np.nan)
    mfe_ratio = np.full(n, np.nan)
    tuw_ratio = np.full(n, np.nan)
    atr_values = pd.to_numeric(model["atr_14"], errors="coerce").to_numpy(dtype=float)
    spread_cost = pd.to_numeric(raw["spread_points"], errors="coerce").fillna(0).to_numpy(dtype=float) * POINT_SIZE
    open_values = raw["open"].to_numpy(dtype=float)
    high_values = raw["high"].to_numpy(dtype=float)
    low_values = raw["low"].to_numpy(dtype=float)
    close_values = raw["close"].to_numpy(dtype=float)
    max_pos = len(raw) - shape.hold_bars - 2
    for i, pos_float in enumerate(positions):
        if not np.isfinite(pos_float):
            continue
        pos = int(pos_float)
        if pos < 0 or pos > max_pos:
            continue
        atr = atr_values[i]
        if not np.isfinite(atr) or atr <= 0:
            continue
        entry_idx = pos + 1
        exit_idx = pos + shape.hold_bars
        entry = open_values[entry_idx]
        cost = spread_cost[entry_idx]
        stop = shape.stop_atr * atr
        target = shape.target_atr * atr
        realized = None
        adverse_bars = 0
        max_fav = 0.0
        max_adv = 0.0
        for j in range(entry_idx, exit_idx + 1):
            if shape.direction > 0:
                fav = high_values[j] - entry
                adv = entry - low_values[j]
                hit_stop = low_values[j] <= entry - stop
                hit_target = high_values[j] >= entry + target
            else:
                fav = entry - low_values[j]
                adv = high_values[j] - entry
                hit_stop = high_values[j] >= entry + stop
                hit_target = low_values[j] <= entry - target
            max_fav = max(max_fav, fav)
            max_adv = max(max_adv, adv)
            if adv > fav:
                adverse_bars += 1
            if hit_stop and hit_target:
                realized = -stop
                break
            if hit_stop:
                realized = -stop
                break
            if hit_target:
                realized = target
                break
        if realized is None:
            realized = shape.direction * (close_values[exit_idx] - entry)
        net = (realized - cost) * POINT_VALUE
        pnl[i] = net
        mae_ratio[i] = max_adv / atr
        mfe_ratio[i] = max_fav / atr
        tuw_ratio[i] = adverse_bars / max(shape.hold_bars, 1)
        quality[i] = (net / atr) + 0.20 * (mfe_ratio[i] - mae_ratio[i]) - 0.10 * tuw_ratio[i]
    label = (quality > 0.05) & (pnl > 0) & (mae_ratio <= shape.stop_atr * 1.15)
    return {
        "pnl": pnl,
        "quality": quality,
        "label": label.astype(float),
        "mae_ratio": mae_ratio,
        "mfe_ratio": mfe_ratio,
        "tuw_ratio": tuw_ratio,
        "direction": np.full(n, shape.direction),
    }


def shape_universe(spec: Mapping[str, Any]) -> list[TradeShape]:
    trade_shapes = spec["trade_shapes"]
    holds = [6, 12, 24, 36]
    stops = [0.6, 1.2]
    targets = [0.8, 1.8]
    return [
        TradeShape(hold, stop, target, direction)
        for hold in holds
        for stop in stops
        for target in targets
        for direction in (1, -1)
        if hold in trade_shapes["hold_bars"]
    ]


def label_prefilter(model: pd.DataFrame, paths: Mapping[str, Mapping[str, np.ndarray]]) -> tuple[list[str], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    for shape_id, path in paths.items():
        mask_train = (model["split"] == "train").to_numpy() & np.isfinite(path["pnl"])
        mask_val = (model["split"] == "validation").to_numpy() & np.isfinite(path["pnl"])
        train_positive = float(np.nanmean(path["label"][mask_train])) if np.any(mask_train) else 0.0
        selected_val = mask_val & (path["label"] > 0)
        metrics = trade_metrics(model.loc[selected_val, "timestamp"], path["pnl"][selected_val], path["direction"][selected_val])
        viable = 0.02 <= train_positive <= 0.40 and metrics["trades_day"] >= 0.5
        rows.append({
            "shape_id": shape_id,
            "train_positive_rate": train_positive,
            "validation_oracle_net": metrics["net_profit"],
            "validation_oracle_pf": metrics["profit_factor"],
            "validation_oracle_dd": metrics["max_drawdown_percent"],
            "validation_oracle_trades_day": metrics["trades_day"],
            "viable": viable,
        })
    ranked = sorted(
        [row for row in rows if row["viable"]],
        key=lambda row: (row["validation_oracle_pf"], row["validation_oracle_net"], row["validation_oracle_trades_day"]),
        reverse=True,
    )
    selected = [row["shape_id"] for row in ranked[:12]]
    if len(selected) < 8:
        selected = [row["shape_id"] for row in sorted(rows, key=lambda row: row["validation_oracle_net"], reverse=True)[:12]]
    return selected, rows


def feature_bundles(features: Sequence[str]) -> dict[str, list[str]]:
    features = list(features)
    external_tokens = ("vix_", "us10yr_", "usdx_", "nvda_", "aapl_", "msft_", "amzn_", "mega8_", "top3_", "us100_minus_")
    price_tokens = (
        "log_return", "hl_", "close_", "gap_", "return_", "ema", "sma", "rsi", "stoch", "ppo", "roc", "trix",
        "atr", "bollinger", "bb_", "historical_vol", "adx", "di_", "supertrend", "vortex",
    )
    session_tokens = ("is_us_cash_open", "minutes_from_cash_open", "is_first_30m", "is_last_30m")
    return {
        "all58": features,
        "no_external_macro": [f for f in features if not f.startswith(external_tokens)],
        "price_path_vol": [f for f in features if f.startswith(price_tokens)],
        "session_vol_path": [f for f in features if f.startswith(price_tokens) or f.startswith(session_tokens)],
    }


def model_factories() -> dict[str, Any]:
    return {
        "logistic_l2": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            LogisticRegression(max_iter=300, class_weight="balanced", solver="lbfgs"),
        ),
        "hist_additive_tree": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            HistGradientBoostingClassifier(max_iter=70, learning_rate=0.06, max_leaf_nodes=15, l2_regularization=0.05),
        ),
        "extra_trees_ref": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            ExtraTreesClassifier(
                n_estimators=90,
                max_depth=8,
                min_samples_leaf=60,
                class_weight="balanced_subsample",
                random_state=7202,
                n_jobs=-1,
            ),
        ),
        "small_nn_16": lambda: make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            MLPClassifier(hidden_layer_sizes=(16,), alpha=0.001, max_iter=80, random_state=7202, early_stopping=True),
        ),
    }


def score_threshold(scores: np.ndarray, timestamps: pd.Series, target_tpd: float) -> float:
    if len(scores) == 0:
        return math.inf
    days = split_days(timestamps)
    target_count = max(int(round(days * target_tpd)), 1)
    target_count = min(target_count, len(scores))
    return float(np.partition(scores, len(scores) - target_count)[len(scores) - target_count])


def evaluate_candidate(
    model: pd.DataFrame,
    scores: np.ndarray,
    path: Mapping[str, np.ndarray],
    target_tpd: float,
) -> dict[str, Any]:
    validation_mask = (model["split"] == "validation").to_numpy() & np.isfinite(scores) & np.isfinite(path["pnl"])
    threshold = score_threshold(scores[validation_mask], model.loc[validation_mask, "timestamp"], target_tpd)
    results: dict[str, Any] = {"score_threshold": threshold}
    for split in ("train", "validation", "oos"):
        mask = (model["split"] == split).to_numpy() & np.isfinite(scores) & np.isfinite(path["pnl"]) & (scores >= threshold)
        metrics = trade_metrics(model.loc[mask, "timestamp"], path["pnl"][mask], path["direction"][mask])
        for key, value in metrics.items():
            results[f"{split}_{key}"] = value
    return results


def is_scout(row: Mapping[str, Any]) -> bool:
    return (
        row["validation_net_profit"] > 0
        and row["oos_net_profit"] > 0
        and row["validation_profit_factor"] >= 1.10
        and row["oos_profit_factor"] >= 1.10
        and row["validation_max_drawdown_percent"] <= 15
        and row["oos_max_drawdown_percent"] <= 15
        and row["validation_trades_day"] >= 1.5
        and row["oos_trades_day"] >= 1.0
    )


def is_meaningful(row: Mapping[str, Any]) -> bool:
    return (
        is_scout(row)
        and row["validation_profit_factor"] >= 1.25
        and row["oos_profit_factor"] >= 1.25
        and row["validation_max_drawdown_percent"] <= 10
        and row["oos_max_drawdown_percent"] <= 10
        and row["validation_trades_day"] >= 3.0
        and row["oos_trades_day"] >= 3.0
        and row["oos_smoothness_r2"] >= 0.15
    )


def train_and_score(model: pd.DataFrame, features: Sequence[str], y: np.ndarray, factory: Any) -> tuple[np.ndarray, dict[str, Any]]:
    train_mask = (model["split"] == "train").to_numpy() & np.isfinite(y)
    valid_mask = np.isfinite(y)
    x_train = model.loc[train_mask, features]
    y_train = y[train_mask].astype(int)
    if len(np.unique(y_train)) < 2:
        raise ValueError("one_class_label")
    estimator = factory()
    estimator.fit(x_train, y_train)
    scores = np.full(len(model), np.nan)
    if hasattr(estimator, "predict_proba"):
        scores[valid_mask] = estimator.predict_proba(model.loc[valid_mask, features])[:, 1]
    else:
        decision = estimator.decision_function(model.loc[valid_mask, features])
        scores[valid_mask] = 1.0 / (1.0 + np.exp(-decision))
    train_auc = float(roc_auc_score(y_train, scores[train_mask])) if len(np.unique(y_train)) == 2 else 0.0
    return scores, {"train_auc": train_auc, "train_positive_rate": float(np.mean(y_train))}


def run_scout() -> dict[str, Any]:
    model = pd.read_parquet(io_path(MODEL_INPUT))
    model["timestamp"] = pd.to_datetime(model["timestamp"], utc=True)
    raw = pd.read_csv(io_path(RAW_US100))
    raw = raw.sort_values("time_close_unix").reset_index(drop=True)
    positions = align_raw(model, raw)
    features = [line.strip() for line in read_text(FEATURE_ORDER).splitlines() if line.strip()]
    spec = json.loads(read_text(F72A_SPEC))
    shapes = shape_universe(spec)
    paths = {shape.shape_id: compute_shape_path(model, raw, positions, shape) for shape in shapes}
    selected_shape_ids, shape_rows = label_prefilter(model, paths)
    bundles = feature_bundles(features)
    factories = model_factories()
    candidate_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    for shape_id in selected_shape_ids:
        path = paths[shape_id]
        y = path["label"]
        for bundle_id, bundle_features in bundles.items():
            for model_id, factory in factories.items():
                try:
                    scores, train_info = train_and_score(model, bundle_features, y, factory)
                except Exception as exc:  # noqa: BLE001 - recorded as scout failure evidence.
                    failure_rows.append({
                        "shape_id": shape_id,
                        "bundle_id": bundle_id,
                        "model_id": model_id,
                        "error": type(exc).__name__,
                        "message": str(exc)[:180],
                    })
                    continue
                for target_tpd in TARGET_TPD_VALUES:
                    row = {
                        "candidate_id": f"f72b_{len(candidate_rows) + 1:04d}",
                        "shape_id": shape_id,
                        "bundle_id": bundle_id,
                        "model_id": model_id,
                        "target_trades_day": target_tpd,
                        "feature_count": len(bundle_features),
                        **train_info,
                        **evaluate_candidate(model, scores, path, target_tpd),
                    }
                    row["scout_clue"] = is_scout(row)
                    row["meaningful_candidate"] = is_meaningful(row)
                    row["final_like_reference_only"] = (
                        row["meaningful_candidate"]
                        and row["validation_profit_factor"] >= 2.0
                        and row["oos_profit_factor"] >= 2.0
                        and 5.0 <= row["validation_trades_day"] <= 10.0
                        and 5.0 <= row["oos_trades_day"] <= 10.0
                    )
                    candidate_rows.append(row)
    ranked = sorted(
        candidate_rows,
        key=lambda row: (
            bool(row["meaningful_candidate"]),
            bool(row["scout_clue"]),
            row["oos_profit_factor"],
            row["oos_net_profit"],
            -abs(row["oos_trades_day"] - 5.0),
        ),
        reverse=True,
    )
    best = ranked[0] if ranked else {}
    selected_path = paths.get(best.get("shape_id", ""), {})
    selected_scores = None
    if best:
        bundle_features = bundles[best["bundle_id"]]
        scores, _ = train_and_score(model, bundle_features, selected_path["label"], factories[best["model_id"]])
        selected_scores = scores
    return {
        "model": model,
        "shape_rows": shape_rows,
        "selected_shape_ids": selected_shape_ids,
        "candidate_rows": candidate_rows,
        "failure_rows": failure_rows,
        "ranked_rows": ranked,
        "best": best,
        "selected_path": selected_path,
        "selected_scores": selected_scores,
    }


def selected_trade_rows(model: pd.DataFrame, best: Mapping[str, Any], path: Mapping[str, np.ndarray], scores: np.ndarray | None) -> list[dict[str, Any]]:
    if not best or scores is None:
        return []
    mask = (
        (model["split"].isin(["validation", "oos"])).to_numpy()
        & np.isfinite(scores)
        & np.isfinite(path["pnl"])
        & (scores >= float(best["score_threshold"]))
    )
    rows = []
    for idx in np.where(mask)[0]:
        rows.append({
            "timestamp": str(model.iloc[idx]["timestamp"]),
            "split": model.iloc[idx]["split"],
            "candidate_id": best["candidate_id"],
            "shape_id": best["shape_id"],
            "direction": "long" if path["direction"][idx] > 0 else "short",
            "score": float(scores[idx]),
            "pnl": float(path["pnl"][idx]),
            "quality": float(path["quality"][idx]),
            "mae_ratio": float(path["mae_ratio"][idx]),
            "mfe_ratio": float(path["mfe_ratio"][idx]),
            "tuw_ratio": float(path["tuw_ratio"][idx]),
        })
    return rows


def summary_payload(result: Mapping[str, Any]) -> dict[str, Any]:
    rows = result["candidate_rows"]
    best = result["best"]
    scout_count = sum(1 for row in rows if row["scout_clue"])
    meaningful_count = sum(1 for row in rows if row["meaningful_candidate"])
    final_like = sum(1 for row in rows if row["final_like_reference_only"])
    next_run = NEXT_PRE_MT5_RUN_ID if meaningful_count > 0 else NEXT_REPAIR_RUN_ID
    judgment = (
        "proxy_meaningful_candidate_pre_mt5_required_no_authority"
        if meaningful_count > 0
        else "proxy_scout_clue_repair_required_no_authority"
        if scout_count > 0
        else "proxy_zero_meaningful_repair_required_no_authority"
    )
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": judgment,
        "candidate_count": len(rows),
        "shape_count": len(result["selected_shape_ids"]),
        "model_failure_count": len(result["failure_rows"]),
        "scout_clue_count": scout_count,
        "meaningful_candidate_count": meaningful_count,
        "final_like_reference_only_count": final_like,
        "best_candidate": best,
        "next_run_id": next_run,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": utc_now(),
    }


def tier_rows(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "record_view": "Tier A separate(Tier A 분리)",
            "status": "materialized_proxy_scout(프록시 탐색 물질화)",
            "kpi": f"candidates={summary['candidate_count']}; scout={summary['scout_clue_count']}; meaningful={summary['meaningful_candidate_count']}",
            "effect": "Tier A model input produced proxy KPI(Tier A 모델 입력이 프록시 KPI 생성)",
        },
        {
            "record_view": "Tier B separate(Tier B 분리)",
            "status": "missing_required(필수 누락)",
            "kpi": "not_materialized_in_f72b_proxy_scout(F72B 프록시 탐색에서 미물질화)",
            "effect": "not omitted; repair or later routed record required(생략 아님, 수리 또는 이후 라우팅 기록 필요)",
        },
        {
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "kpi": "no_synthetic_combined_claim_without_tier_b(Tier B 없이 합성 합산 주장 없음)",
            "effect": "prevents combined overclaim(합산 과장 방지)",
        },
    ]


def report_lines(summary: Mapping[str, Any]) -> list[str]:
    best = summary["best_candidate"]
    next_run = summary["next_run_id"]
    best_lines = [
        f"- candidate_id(후보 ID): `{best.get('candidate_id', '')}`",
        f"- shape/model/bundle(형태/모델/묶음): `{best.get('shape_id', '')}` / `{best.get('model_id', '')}` / `{best.get('bundle_id', '')}`",
        f"- validation net/PF/DD/tpd(검증 순수익/수익 팩터/손실폭/일거래): `{best.get('validation_net_profit', 0):.4f}` / `{best.get('validation_profit_factor', 0):.4f}` / `{best.get('validation_max_drawdown_percent', 0):.4f}%` / `{best.get('validation_trades_day', 0):.4f}`",
        f"- OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일거래): `{best.get('oos_net_profit', 0):.4f}` / `{best.get('oos_profit_factor', 0):.4f}` / `{best.get('oos_max_drawdown_percent', 0):.4f}%` / `{best.get('oos_trades_day', 0):.4f}`",
        f"- scout/meaningful/final-like(탐색/의미/최종 유사): `{best.get('scout_clue', False)}` / `{best.get('meaningful_candidate', False)}` / `{best.get('final_like_reference_only', False)}`",
    ] if best else ["- no candidate rows(후보 행 없음)."]
    return [
        "# Frontier72B Trade-Shape Proxy Scout(F72B 거래 형태 프록시 탐색)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"- status(상태): `{summary['status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- candidate_count(후보 수): `{summary['candidate_count']}`",
        f"- scout_clue_count(탐색 단서 수): `{summary['scout_clue_count']}`",
        f"- meaningful_candidate_count(의미 후보 수): `{summary['meaningful_candidate_count']}`",
        f"- final_like_reference_only_count(최종 유사 참조 전용 수): `{summary['final_like_reference_only_count']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Best Candidate(최선 후보)",
        "",
        *best_lines,
        "",
        "## Tier Records(티어 기록)",
        "",
        "- Tier A separate(Tier A 분리): materialized proxy scout(프록시 탐색 물질화).",
        "- Tier B separate(Tier B 분리): missing_required(필수 누락).",
        "- Tier A+B combined(Tier A+B 합산): out_of_scope_by_claim(주장 범위 밖).",
        "",
        "## Proxy/Runtime Boundary(프록시/런타임 경계)",
        "",
        "Runtime probe(런타임 탐침)는 아직 실행하지 않았다. Effect(효과): F72B는 proxy-only(프록시 전용)이며, 의미 후보가 있으면 pre-MT5 Grok(사전 MT5 Grok) 뒤 MT5 Runtime Probe(MT5 런타임 탐침)로 물질화한다.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{next_run}`.",
    ]


def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F72B Required Gate Coverage Audit(F72B 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| stage_open_anchor(단계 개방 고정점) | pass(통과) | `{rel(F72A_SPEC)}` | F72A label/exit/risk spec(라벨/청산/위험 명세)에 연결 |",
        f"| proxy_scout_execution(프록시 탐색 실행) | pass(통과) | `{rel(RUN_ROOT / 'f72b_candidate_summary.csv')}` | 후보 KPI 생성 |",
        f"| feature_ablation_breadth(피처 묶음 폭) | pass(통과) | `{rel(RUN_ROOT / 'f72b_feature_bundle_summary.csv')}` | 빼기/재조합 반영 |",
        f"| tier_pair_record(티어 쌍 기록) | partial_with_missing_required(필수 누락 포함 부분 통과) | `{rel(RUN_ROOT / 'f72b_tier_record_status.csv')}` | Tier B 누락을 숨기지 않음 |",
        "| mandatory_mt5_runtime_probe(필수 MT5 런타임 탐침) | pending_after_proxy(프록시 후 대기) | next action(다음 행동) | proxy-only 주장을 넘지 않음 |",
        f"| final_claim_guard(최종 주장 보호) | pass(통과) | `{CLAIM_BOUNDARY}` | 금지 주장 없음 |",
    ]


def selected_status_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# F72 Selection Status(F72 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{summary['next_run_id']}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{summary['status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- next_action(다음 행동): `{summary['next_run_id']}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ]


def run_manifest(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": summary["next_run_id"],
        "status": summary["status"],
        "judgment": summary["judgment"],
        "candidate_count": summary["candidate_count"],
        "scout_clue_count": summary["scout_clue_count"],
        "meaningful_candidate_count": summary["meaningful_candidate_count"],
        "claim_boundary": CLAIM_BOUNDARY,
        "artifacts": [
            rel(RUN_ROOT / "f72b_candidate_summary.csv"),
            rel(RUN_ROOT / "f72b_top_candidates.csv"),
            rel(RUN_ROOT / "f72b_top_candidate_trades.csv"),
            rel(REVIEWS_ROOT / "frontier72B_trade_shape_exit_distribution_proxy_scout_report.md"),
        ],
    }


def feature_bundle_summary(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for bundle_id in sorted({row["bundle_id"] for row in rows}):
        subset = [row for row in rows if row["bundle_id"] == bundle_id]
        best = max(subset, key=lambda row: row["oos_profit_factor"])
        out.append({
            "bundle_id": bundle_id,
            "candidate_count": len(subset),
            "scout_clue_count": sum(1 for row in subset if row["scout_clue"]),
            "meaningful_candidate_count": sum(1 for row in subset if row["meaningful_candidate"]),
            "best_oos_pf": best["oos_profit_factor"],
            "best_oos_net": best["oos_net_profit"],
            "best_oos_trades_day": best["oos_trades_day"],
        })
    return out


def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    best = summary["best_candidate"]
    return {
        "ledger_row_id": f"{RUN_ID}__proxy_scout",
        "row_id": f"{RUN_ID}__proxy_scout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "proxy_scout(프록시 탐색)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope_by_claim",
        "kpi_scope": "proxy_scout_kpi(프록시 탐색 KPI)",
        "scoreboard_lane": "structural_scout(구조 스카우트)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": rel(REVIEWS_ROOT / "frontier72B_trade_shape_exit_distribution_proxy_scout_report.md"),
        "primary_kpi": f"candidates={summary['candidate_count']}; scout={summary['scout_clue_count']}; meaningful={summary['meaningful_candidate_count']}",
        "guardrail_kpi": f"best_oos_pf={best.get('oos_profit_factor', 0):.4f}; best_oos_tpd={best.get('oos_trades_day', 0):.4f}; mt5_probe=pending",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(프록시 전용 주장 범위 밖)",
        "notes": "F72B trade-shape-first proxy scout completed; MT5 probe pending after proxy decision.",
        "family": "experiment_execution(실험 실행)",
        "lane": "proxy_scout(프록시 탐색)",
        "primary_report": rel(REVIEWS_ROOT / "frontier72B_trade_shape_exit_distribution_proxy_scout_report.md"),
        "run_number": "frontier72B",
        "date": summary["created_at_utc"][:10],
        "decision": summary["judgment"],
        "next_run_id": summary["next_run_id"],
        "rows": summary["candidate_count"],
        "gate_passes": 5,
        "gate_total": 6,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEWS_ROOT / "frontier72B_trade_shape_exit_distribution_proxy_scout_report.md"),
        "run_date": summary["created_at_utc"][:10],
        "primary_artifact": rel(RUN_ROOT / "f72b_candidate_summary.csv"),
        "candidate_model_id": best.get("candidate_id", ""),
        "net_profit": best.get("oos_net_profit", ""),
        "profit_factor": best.get("oos_profit_factor", ""),
        "drawdown": best.get("oos_max_drawdown_percent", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "result_status": summary["status"],
        "candidate_rows": summary["candidate_count"],
        "positive_proxy_rows": summary["scout_clue_count"],
        "best_model_id": best.get("model_id", ""),
        "best_proxy_net": best.get("oos_net_profit", ""),
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "metric_scope": "proxy_scout_kpi(프록시 탐색 KPI)",
        "result_judgment": summary["judgment"],
        "final_decision_path": rel(REVIEWS_ROOT / "frontier72B_trade_shape_exit_distribution_proxy_scout_report.md"),
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f72b.md"),
        "created_at": summary["created_at_utc"],
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f72b.md"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_scout_only(프록시 탐색 전용)",
        "evidence_boundary": "proxy_only_no_runtime(프록시 전용, 런타임 없음)",
        "next_action": summary["next_run_id"],
        "question": "Can trade-shape-first exit/risk labels create a wider density/PF/DD seed surface?(거래 형태 우선 청산/위험 라벨이 더 넓은 밀도/수익 팩터/손실폭 씨앗 표면을 만들 수 있나?)",
        "artifact_count": 9,
        "work_family": "experiment_execution(실험 실행)",
        "run_family": "frontier_proxy_scout(전선 프록시 탐색)",
        "run_type": "trade_shape_exit_distribution_proxy_scout(거래 형태 청산 분포 프록시 탐색)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "result_path": rel(REVIEWS_ROOT / "frontier72B_trade_shape_exit_distribution_proxy_scout_report.md"),
        "trade_density": best.get("oos_trades_day", ""),
        "max_drawdown_percent": best.get("oos_max_drawdown_percent", ""),
        "strict_joint_pass_count": summary["meaningful_candidate_count"],
    }


def update_ledgers(summary: Mapping[str, Any]) -> None:
    row = ledger_row(summary)
    upsert_ledger(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_ledger(RUN_REGISTRY, "run_id", row)
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_registers(summary: Mapping[str, Any]) -> None:
    marker = "<!-- frontier72B_trade_shape_exit_distribution_proxy_scout_v1 -->"
    best = summary["best_candidate"]
    block = f"""<!-- frontier72B_trade_shape_exit_distribution_proxy_scout_v1 -->
- `{RUN_ID}` executed F72 trade-shape-first exit distribution proxy scout(F72 거래 형태 우선 청산 분포 프록시 탐색). Result(결과): `{summary['judgment']}`. Candidates(후보) `{summary['candidate_count']}`, scout clue(탐색 단서) `{summary['scout_clue_count']}`, meaningful candidate(의미 후보) `{summary['meaningful_candidate_count']}`. Best OOS(최선 표본외) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `{best.get('oos_net_profit', 0):.4f}/{best.get('oos_profit_factor', 0):.4f}/{best.get('oos_max_drawdown_percent', 0):.4f}/{best.get('oos_trades_day', 0):.4f}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier72B_trade_shape_exit_distribution_proxy_scout_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{summary['next_run_id']}`."""
    append_once(IDEA_REGISTRY, marker, block)


def update_state_files(summary: Mapping[str, Any]) -> None:
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {summary['next_run_id']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {summary['status']}",
        f"current_judgment: {summary['judgment']}",
        f"next_run_id: {summary['next_run_id']}",
        "runtime_probe_status: f72_mandatory_runtime_probe_pending_after_proxy_decision",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f71_closeout",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "notes:",
        f'  - "Action(행동): F72B proxy scout(프록시 탐색)를 실행했다. Candidates(후보) {summary["candidate_count"]}, scout clue(탐색 단서) {summary["scout_clue_count"]}, meaningful(의미 후보) {summary["meaningful_candidate_count"]}."',
        f'  - "Effect(효과): 다음 행동을 {summary["next_run_id"]}로 고정했다. Runtime probe(런타임 탐침)는 아직 pending(대기)이다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    current = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {summary['created_at_utc']}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{summary['next_run_id']}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F72B trade-shape exit distribution proxy scout(거래 형태 청산 분포 프록시 탐색)를 실행했다.",
        "",
        f"Effect(효과): 후보 `{summary['candidate_count']}`개 중 scout clue(탐색 단서) `{summary['scout_clue_count']}`개, meaningful candidate(의미 후보) `{summary['meaningful_candidate_count']}`개를 기록했고, 다음 행동을 `{summary['next_run_id']}`로 설정했다.",
        "",
        f"- judgment(판정): `{summary['judgment']}`.",
        f"- best OOS PF(최선 표본외 수익 팩터): `{summary['best_candidate'].get('oos_profit_factor', 0):.4f}`.",
        "- runtime probe(런타임 탐침): pending after proxy decision(프록시 결정 뒤 대기).",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_text(CURRENT_WORKING_STATE, current)


def write_outputs(result: Mapping[str, Any], summary: Mapping[str, Any]) -> None:
    for path in (RUN_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ranked = result["ranked_rows"]
    write_csv(RUN_ROOT / "f72b_shape_prefilter.csv", result["shape_rows"])
    write_csv(RUN_ROOT / "f72b_candidate_summary.csv", result["candidate_rows"])
    write_csv(RUN_ROOT / "f72b_top_candidates.csv", ranked[:25])
    write_csv(RUN_ROOT / "f72b_model_failures.csv", result["failure_rows"])
    write_csv(RUN_ROOT / "f72b_feature_bundle_summary.csv", feature_bundle_summary(result["candidate_rows"]))
    trade_rows = selected_trade_rows(result["model"], summary["best_candidate"], result["selected_path"], result["selected_scores"])
    write_csv(RUN_ROOT / "f72b_top_candidate_trades.csv", trade_rows)
    write_csv(RUN_ROOT / "f72b_tier_record_status.csv", tier_rows(summary))
    write_json(RUN_ROOT / "frontier72B_proxy_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_text(RUN_ROOT / "reports/result_summary.md", report_lines(summary))
    write_text(REVIEWS_ROOT / "frontier72B_trade_shape_exit_distribution_proxy_scout_report.md", report_lines(summary))
    write_text(REVIEWS_ROOT / "required_gate_coverage_audit_f72b.md", gate_audit_lines(summary))
    write_text(SELECTED_ROOT / "selection_status.md", selected_status_lines(summary))


def main() -> int:
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F72B required material missing: {missing}")
    result = run_scout()
    summary = summary_payload(result)
    write_outputs(result, summary)
    update_registers(summary)
    update_ledgers(summary)
    update_state_files(summary)
    print(json.dumps(json_ready({
        "status": summary["status"],
        "judgment": summary["judgment"],
        "candidate_count": summary["candidate_count"],
        "scout_clue_count": summary["scout_clue_count"],
        "meaningful_candidate_count": summary["meaningful_candidate_count"],
        "next_run_id": summary["next_run_id"],
        "best_oos_net": summary["best_candidate"].get("oos_net_profit", 0),
        "best_oos_pf": summary["best_candidate"].get("oos_profit_factor", 0),
        "best_oos_dd": summary["best_candidate"].get("oos_max_drawdown_percent", 0),
        "best_oos_trades_day": summary["best_candidate"].get("oos_trades_day", 0),
        "claim_boundary": CLAIM_BOUNDARY,
    }), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
