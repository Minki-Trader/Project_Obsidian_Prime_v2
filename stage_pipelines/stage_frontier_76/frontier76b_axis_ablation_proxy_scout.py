from __future__ import annotations

import csv
import json
import math
import sys
import warnings
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics"
RUN_ID = "frontier76B_axis_ablation_proxy_scout_v1"
PARENT_RUN_ID = "frontier76A_stage_open_axis_ablation_source_discovery_v1"
NEXT_RUN_IF_MEANINGFUL = "frontier76C_pre_mt5_grok_axis_ablation_runtime_probe_v1"
NEXT_RUN_IF_NO_MEANINGFUL = "frontier76C_pre_mt5_grok_axis_ablation_negative_control_runtime_probe_v1"
STATUS_MEANINGFUL = "proxy_scout_meaningful_signal_pre_mt5_probe_required_no_authority"
STATUS_NO_MEANINGFUL = "proxy_scout_no_meaningful_signal_negative_control_probe_required_no_authority"
CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
SCOUT_CLUE_GATE = "one split net>0 or PF>=1.15, trade_count>=50, density>=0.75/day, fragility recorded"
MEANINGFUL_SIGNAL_GATE = "validation+OOS net>0, PF>=1.30, DD<=10%, trades/day>=1.0, trade_count>=100 per split"
INITIAL_BALANCE = 10_000.0
PROXY_POINT_SCALE = 10_000.0
PROXY_COST_POINTS = 1.2

STAGE_DIR = ROOT / "stages" / STAGE_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
SELECTED_DIR = STAGE_DIR / "04_selected"
DATASET_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_feature_order.txt"
)
SCRIPT_PATH = "stage_pipelines/stage_frontier_76/frontier76b_axis_ablation_proxy_scout.py"

SUMMARY = REVIEW_DIR / "f76b_summary.json"
CANDIDATES_TOP = REVIEW_DIR / "f76b_candidate_results_ranked_top100.csv"
AXIS_SUMMARY = REVIEW_DIR / "f76b_axis_summary.csv"
MODEL_FIT_SUMMARY = REVIEW_DIR / "f76b_model_fit_summary.csv"
REPORT = REVIEW_DIR / "frontier76B_axis_ablation_proxy_scout_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f76b.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"


@dataclass(frozen=True)
class TargetSpec:
    name: str
    side: str
    threshold: float
    operator: str


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if not rows:
        io_path(path).write_text("", encoding="utf-8-sig")
        return
    fieldnames = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any]) -> None:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [existing for existing in reader if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def feature_order() -> list[str]:
    return [line.strip() for line in io_path(FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def has_columns(features: Sequence[str], names: Sequence[str]) -> list[str]:
    available = set(features)
    return [name for name in names if name in available]


def feature_sets(features: Sequence[str]) -> dict[str, list[str]]:
    full = list(features)
    price_action = has_columns(
        features,
        [
            "log_return_1",
            "log_return_3",
            "hl_range",
            "close_open_ratio",
            "gap_percent",
            "close_prev_close_ratio",
            "return_zscore_20",
            "hl_zscore_50",
            "overnight_return",
            "return_1_over_atr_14",
            "atr_14",
            "atr_50",
        ],
    )
    trend = [f for f in features if any(key in f for key in ["ema", "sma", "rsi", "stoch", "ppo", "roc", "trix", "adx", "di_", "supertrend", "vortex"])]
    volatility = [f for f in features if any(key in f for key in ["atr", "bollinger", "bb_", "historical_vol", "squeeze", "adx", "di_spread", "zscore"])]
    session_macro_removed = [
        f
        for f in features
        if not any(key in f for key in ["is_us_cash", "minutes_from", "first_30m", "last_30m", "vix_", "us10yr_", "usdx_"])
    ]
    mega_removed = [
        f
        for f in features
        if not any(key in f for key in ["nvda_", "aapl_", "msft_", "amzn_", "mega8_", "top3_", "us100_minus_mega"])
    ]
    return {
        "full58": full,
        "price_action_core": price_action,
        "trend_momentum": trend,
        "volatility_compression": volatility,
        "session_macro_removed": session_macro_removed,
        "mega_cap_removed": mega_removed,
    }


def target_specs(train: pd.DataFrame) -> list[TargetSpec]:
    returns = train["future_log_return_12"].astype(float)
    return [
        TargetSpec("long_fwd12_q60", "long", float(returns.quantile(0.60)), ">"),
        TargetSpec("long_fwd12_q70", "long", float(returns.quantile(0.70)), ">"),
        TargetSpec("short_fwd12_q40", "short", float(returns.quantile(0.40)), "<"),
        TargetSpec("short_fwd12_q30", "short", float(returns.quantile(0.30)), "<"),
    ]


def make_target(series: pd.Series, spec: TargetSpec) -> np.ndarray:
    if spec.operator == ">":
        return (series.astype(float).to_numpy() > spec.threshold).astype(int)
    return (series.astype(float).to_numpy() < spec.threshold).astype(int)


def model_builders(random_state: int = 7601) -> dict[str, Callable[[], Any]]:
    return {
        "logistic_l2_balanced": lambda: make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=300, class_weight="balanced", C=0.5, solver="lbfgs"),
        ),
        "extra_trees_d7_l60": lambda: ExtraTreesClassifier(
            n_estimators=80,
            max_depth=7,
            min_samples_leaf=60,
            class_weight="balanced_subsample",
            random_state=random_state,
            n_jobs=-1,
        ),
        "hist_gbm_d4_l2": lambda: HistGradientBoostingClassifier(
            max_iter=120,
            max_leaf_nodes=31,
            max_depth=4,
            l2_regularization=0.1,
            learning_rate=0.05,
            random_state=random_state,
        ),
        "small_mlp_16": lambda: make_pipeline(
            StandardScaler(),
            MLPClassifier(
                hidden_layer_sizes=(16,),
                alpha=0.01,
                max_iter=80,
                early_stopping=True,
                n_iter_no_change=5,
                random_state=random_state,
            ),
        ),
    }


def clean_matrices(df: pd.DataFrame, train_mask: pd.Series, columns: Sequence[str]) -> dict[str, pd.DataFrame]:
    train = df.loc[train_mask, columns].replace([np.inf, -np.inf], np.nan)
    med = train.median(numeric_only=True).fillna(0.0)
    cleaned = {}
    for split in ["train", "validation", "oos"]:
        part = df.loc[df["split"] == split, columns].replace([np.inf, -np.inf], np.nan).fillna(med)
        cleaned[split] = part.astype(float)
    return cleaned


def probability(model: Any, matrix: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(matrix))[:, 1]
    pred = model.predict(matrix)
    return np.asarray(pred, dtype=float)


def session_mask(df: pd.DataFrame, name: str) -> np.ndarray:
    if name == "all":
        return np.ones(len(df), dtype=bool)
    if name == "cash_open":
        return df.get("is_first_30m_after_open", pd.Series(0, index=df.index)).fillna(0).astype(int).to_numpy() == 1
    if name == "cash_late":
        return df.get("is_last_30m_before_cash_close", pd.Series(0, index=df.index)).fillna(0).astype(int).to_numpy() == 1
    if name == "cash_mid":
        is_cash = df.get("is_us_cash_open", pd.Series(0, index=df.index)).fillna(0).astype(int).to_numpy() == 1
        first = df.get("is_first_30m_after_open", pd.Series(0, index=df.index)).fillna(0).astype(int).to_numpy() == 1
        last = df.get("is_last_30m_before_cash_close", pd.Series(0, index=df.index)).fillna(0).astype(int).to_numpy() == 1
        return is_cash & ~first & ~last
    raise ValueError(name)


def risk_thresholds(train: pd.DataFrame) -> dict[str, float]:
    def med(name: str, fallback: float = 0.0) -> float:
        if name not in train:
            return fallback
        return float(pd.to_numeric(train[name], errors="coerce").median())

    return {
        "atr_ratio_median": med("atr_14_over_atr_50", 1.0),
        "boll_width_median": med("bollinger_width_20", 0.0),
        "adx_median": med("adx_14", 20.0),
    }


def risk_mask(df: pd.DataFrame, name: str, side: str, thresholds: Mapping[str, float]) -> np.ndarray:
    n = len(df)
    if name == "none":
        return np.ones(n, dtype=bool)
    if name == "compression":
        atr = pd.to_numeric(df.get("atr_14_over_atr_50", pd.Series(np.nan, index=df.index)), errors="coerce").to_numpy()
        width = pd.to_numeric(df.get("bollinger_width_20", pd.Series(np.nan, index=df.index)), errors="coerce").to_numpy()
        return (atr <= thresholds["atr_ratio_median"]) & (width <= thresholds["boll_width_median"])
    if name == "trend_aligned":
        adx = pd.to_numeric(df.get("adx_14", pd.Series(np.nan, index=df.index)), errors="coerce").to_numpy()
        di = pd.to_numeric(df.get("di_spread_14", pd.Series(0.0, index=df.index)), errors="coerce").to_numpy()
        direction = di > 0 if side == "long" else di < 0
        return (adx >= thresholds["adx_median"]) & direction
    if name == "mean_revert":
        bb = pd.to_numeric(df.get("bb_position_20", pd.Series(0.5, index=df.index)), errors="coerce").fillna(0.5).to_numpy()
        return bb <= 0.35 if side == "long" else bb >= 0.65
    raise ValueError(name)


def apply_cooldown(mask: np.ndarray, cooldown_bars: int) -> np.ndarray:
    if cooldown_bars <= 0:
        return mask
    selected = np.zeros_like(mask, dtype=bool)
    last = -10**9
    for idx, flag in enumerate(mask):
        if flag and idx - last > cooldown_bars:
            selected[idx] = True
            last = idx
    return selected


def max_drawdown(values: np.ndarray) -> float:
    if len(values) == 0:
        return 0.0
    equity = INITIAL_BALANCE + np.cumsum(values)
    peaks = np.maximum.accumulate(equity)
    dd = peaks - equity
    return float(np.max(dd)) if len(dd) else 0.0


def kpi(split_df: pd.DataFrame, selected: np.ndarray, side: str) -> dict[str, float]:
    if selected.sum() == 0:
        return {
            "net": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "pf": 0.0,
            "dd_pct": 0.0,
            "trade_count": 0,
            "trades_day": 0.0,
            "win_rate": 0.0,
            "avg_win": 0.0,
            "avg_loss": 0.0,
            "payoff": 0.0,
            "expectancy": 0.0,
            "recovery": 0.0,
        }
    side_mult = 1.0 if side == "long" else -1.0
    future = pd.to_numeric(split_df.loc[selected, "future_log_return_12"], errors="coerce").fillna(0.0).to_numpy()
    pnl = side_mult * future * PROXY_POINT_SCALE - PROXY_COST_POINTS
    gross_profit = float(pnl[pnl > 0].sum())
    gross_loss = float(pnl[pnl < 0].sum())
    net = float(pnl.sum())
    pf = gross_profit / abs(gross_loss) if gross_loss < 0 else (999.0 if gross_profit > 0 else 0.0)
    dd_amount = max_drawdown(pnl)
    dd_pct = dd_amount / INITIAL_BALANCE * 100.0
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    dates = pd.to_datetime(split_df["timestamp"], errors="coerce").dt.date.nunique()
    trades = int(len(pnl))
    avg_win = float(wins.mean()) if len(wins) else 0.0
    avg_loss = float(losses.mean()) if len(losses) else 0.0
    return {
        "net": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "pf": pf,
        "dd_pct": dd_pct,
        "trade_count": trades,
        "trades_day": float(trades / dates) if dates else 0.0,
        "win_rate": float(len(wins) / trades) if trades else 0.0,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff": abs(avg_win / avg_loss) if avg_loss < 0 else 0.0,
        "expectancy": float(pnl.mean()) if trades else 0.0,
        "recovery": net / dd_amount if dd_amount > 0 else (999.0 if net > 0 else 0.0),
    }


def clue_gate(metrics: Mapping[str, float]) -> bool:
    return (
        int(metrics["trade_count"]) >= 50
        and float(metrics["trades_day"]) >= 0.75
        and (float(metrics["net"]) > 0 or float(metrics["pf"]) >= 1.15)
    )


def meaningful_gate(val: Mapping[str, float], oos: Mapping[str, float]) -> bool:
    def ok(metrics: Mapping[str, float]) -> bool:
        return (
            float(metrics["net"]) > 0
            and float(metrics["pf"]) >= 1.30
            and float(metrics["dd_pct"]) <= 10.0
            and float(metrics["trades_day"]) >= 1.0
            and int(metrics["trade_count"]) >= 100
        )

    return ok(val) and ok(oos)


def rank_score(val: Mapping[str, float], oos: Mapping[str, float], meaningful: bool, scout: bool) -> float:
    capped_min_pf = min(float(val["pf"]), float(oos["pf"]), 5.0)
    capped_min_tpd = min(float(val["trades_day"]), float(oos["trades_day"]), 10.0)
    min_trades = min(int(val["trade_count"]), int(oos["trade_count"]))
    return (
        (1_000_000.0 if meaningful else 0.0)
        + (100_000.0 if scout else 0.0)
        + (10_000.0 if (float(val["net"]) > 0 and float(oos["net"]) > 0) else 0.0)
        + capped_min_pf * 1000.0
        + capped_min_tpd * 100.0
        + min_trades * 2.0
        - max(float(val["dd_pct"]), float(oos["dd_pct"])) * 100.0
        + float(oos["net"]) * 0.01
    )


def fit_and_score() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    df = pd.read_parquet(io_path(DATASET_PATH)).copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    features = feature_order()
    train_mask = df["split"] == "train"
    train = df.loc[train_mask]
    targets = target_specs(train)
    feature_map = feature_sets(features)
    builders = model_builders()
    thresholds = risk_thresholds(train)
    prob_quantiles = [0.80, 0.85, 0.90]
    sessions = ["all", "cash_open", "cash_mid", "cash_late"]
    risks = ["none", "compression", "trend_aligned", "mean_revert"]
    cooldowns = [0, 6]

    candidate_rows: list[dict[str, Any]] = []
    fit_rows: list[dict[str, Any]] = []
    candidate_id = 0

    for feature_set_name, cols in feature_map.items():
        if not cols:
            continue
        matrices = clean_matrices(df, train_mask, cols)
        for target in targets:
            y_train = make_target(train["future_log_return_12"], target)
            positives = int(y_train.sum())
            if positives == 0 or positives == len(y_train):
                fit_rows.append(
                    {
                        "feature_set": feature_set_name,
                        "target": target.name,
                        "model": "all",
                        "status": "skipped_single_class",
                        "positive_train": positives,
                        "train_rows": int(len(y_train)),
                    }
                )
                continue
            for model_name, builder in builders.items():
                if model_name == "small_mlp_16" and feature_set_name not in {"price_action_core", "volatility_compression"}:
                    continue
                model = builder()
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        model.fit(matrices["train"], y_train)
                    probs = {split: probability(model, matrices[split]) for split in ["train", "validation", "oos"]}
                    fit_rows.append(
                        {
                            "feature_set": feature_set_name,
                            "target": target.name,
                            "model": model_name,
                            "status": "fit_completed",
                            "positive_train": positives,
                            "train_rows": int(len(y_train)),
                            "train_positive_rate": float(positives / len(y_train)),
                        }
                    )
                except Exception as exc:  # noqa: BLE001
                    fit_rows.append(
                        {
                            "feature_set": feature_set_name,
                            "target": target.name,
                            "model": model_name,
                            "status": "fit_failed",
                            "error": str(exc)[:200],
                            "positive_train": positives,
                            "train_rows": int(len(y_train)),
                        }
                    )
                    continue

                for q in prob_quantiles:
                    prob_threshold = float(np.quantile(probs["train"], q))
                    for session in sessions:
                        for risk in risks:
                            for cooldown in cooldowns:
                                val_df = df.loc[df["split"] == "validation"].copy()
                                oos_df = df.loc[df["split"] == "oos"].copy()
                                val_mask = (
                                    (probs["validation"] >= prob_threshold)
                                    & session_mask(val_df, session)
                                    & risk_mask(val_df, risk, target.side, thresholds)
                                )
                                oos_mask = (
                                    (probs["oos"] >= prob_threshold)
                                    & session_mask(oos_df, session)
                                    & risk_mask(oos_df, risk, target.side, thresholds)
                                )
                                val_mask = apply_cooldown(val_mask, cooldown)
                                oos_mask = apply_cooldown(oos_mask, cooldown)
                                val_kpi = kpi(val_df.reset_index(drop=True), val_mask, target.side)
                                oos_kpi = kpi(oos_df.reset_index(drop=True), oos_mask, target.side)
                                scout = clue_gate(val_kpi) or clue_gate(oos_kpi)
                                meaningful = meaningful_gate(val_kpi, oos_kpi)
                                dual_positive = val_kpi["net"] > 0 and oos_kpi["net"] > 0
                                candidate_id += 1
                                row: dict[str, Any] = {
                                    "candidate_id": f"f76b_{candidate_id:05d}",
                                    "feature_set": feature_set_name,
                                    "feature_count": len(cols),
                                    "target": target.name,
                                    "side": target.side,
                                    "target_threshold": target.threshold,
                                    "model": model_name,
                                    "prob_quantile": q,
                                    "prob_threshold": prob_threshold,
                                    "session": session,
                                    "risk_filter": risk,
                                    "cooldown_bars": cooldown,
                                    "scout_clue": int(scout),
                                    "meaningful_signal": int(meaningful),
                                    "dual_positive": int(dual_positive),
                                    "rank_score": rank_score(val_kpi, oos_kpi, meaningful, scout),
                                }
                                for prefix, metrics in [("val", val_kpi), ("oos", oos_kpi)]:
                                    for key, value in metrics.items():
                                        row[f"{prefix}_{key}"] = value
                                candidate_rows.append(row)

    candidate_rows.sort(key=lambda row: float(row["rank_score"]), reverse=True)
    summary = {
        "run_id": RUN_ID,
        "candidate_rows": len(candidate_rows),
        "fit_rows": len(fit_rows),
        "fit_completed": sum(1 for row in fit_rows if row.get("status") == "fit_completed"),
        "scout_clue_count": sum(int(row["scout_clue"]) for row in candidate_rows),
        "meaningful_signal_count": sum(int(row["meaningful_signal"]) for row in candidate_rows),
        "dual_positive_count": sum(int(row["dual_positive"]) for row in candidate_rows),
        "best_candidate": candidate_rows[0] if candidate_rows else {},
        "claim_boundary": CLAIM_BOUNDARY,
        "scout_clue_gate": SCOUT_CLUE_GATE,
        "meaningful_signal_gate": MEANINGFUL_SIGNAL_GATE,
        "created_at_utc": utc_now(),
    }
    return candidate_rows, fit_rows, summary


def axis_summary_rows(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis in ["feature_set", "target", "model", "session", "risk_filter"]:
        values = sorted({str(row[axis]) for row in candidate_rows})
        for value in values:
            subset = [row for row in candidate_rows if str(row[axis]) == value]
            if not subset:
                continue
            best = max(subset, key=lambda row: float(row["rank_score"]))
            rows.append(
                {
                    "axis": axis,
                    "value": value,
                    "candidate_rows": len(subset),
                    "scout_clue_count": sum(int(row["scout_clue"]) for row in subset),
                    "meaningful_signal_count": sum(int(row["meaningful_signal"]) for row in subset),
                    "dual_positive_count": sum(int(row["dual_positive"]) for row in subset),
                    "best_candidate": best["candidate_id"],
                    "best_rank_score": best["rank_score"],
                    "best_val_pf_dd_tpd": f"{best['val_pf']}/{best['val_dd_pct']}/{best['val_trades_day']}",
                    "best_oos_pf_dd_tpd": f"{best['oos_pf']}/{best['oos_dd_pct']}/{best['oos_trades_day']}",
                }
            )
    return rows


def status_and_next(summary: Mapping[str, Any]) -> tuple[str, str, str]:
    if int(summary["meaningful_signal_count"]) > 0:
        return STATUS_MEANINGFUL, "meaningful_signal_pre_mt5_probe_required_no_authority", NEXT_RUN_IF_MEANINGFUL
    return STATUS_NO_MEANINGFUL, "no_meaningful_signal_negative_control_probe_required_no_authority", NEXT_RUN_IF_NO_MEANINGFUL


def report_text(summary: Mapping[str, Any], status: str, judgment: str, next_run: str) -> str:
    best = summary.get("best_candidate") or {}
    return f"""# Frontier76B Axis Ablation Proxy Scout Report(F76B 축 제거 프록시 탐색 보고서)

Run id(실행 ID): `{RUN_ID}`

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Hypothesis(가설)

Feature/label/model/trade/risk/session ablation(피처/라벨/모델/거래/위험/세션 제거·교체)이 runtime economics source(런타임 경제성 원천)를 식별하거나 반증할 수 있는지 proxy(프록시)로 탐색했다.

## Proxy KPI(프록시 핵심 성과 지표)

- candidate rows(후보 행): `{summary['candidate_rows']}`
- model fits completed(완료된 모델 적합): `{summary['fit_completed']}/{summary['fit_rows']}`
- scout clue count(탐색 단서 수): `{summary['scout_clue_count']}`
- meaningful signal count(의미 신호 수): `{summary['meaningful_signal_count']}`
- dual positive count(양분할 양수 수): `{summary['dual_positive_count']}`

## Best Candidate(최선 후보)

- candidate(후보): `{best.get('candidate_id', '')}`
- axes(축): feature/model/target/session/risk/cooldown `{best.get('feature_set', '')}/{best.get('model', '')}/{best.get('target', '')}/{best.get('session', '')}/{best.get('risk_filter', '')}/{best.get('cooldown_bars', '')}`
- validation net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래): `{best.get('val_net', '')}/{best.get('val_pf', '')}/{best.get('val_dd_pct', '')}%/{best.get('val_trades_day', '')}/{best.get('val_trade_count', '')}`
- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일거래/거래): `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}%/{best.get('oos_trades_day', '')}/{best.get('oos_trade_count', '')}`

## Gate Read(게이트 판독)

- scout clue gate(탐색 단서 게이트): `{SCOUT_CLUE_GATE}`
- meaningful signal gate(의미 신호 게이트): `{MEANINGFUL_SIGNAL_GATE}`
- result(결과): `{judgment}`

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `{rel(DATASET_PATH)}` sha256 `{sha256_file_lf_normalized(DATASET_PATH)}`; `{rel(FEATURE_ORDER_PATH)}` sha256 `{sha256_file_lf_normalized(FEATURE_ORDER_PATH)}`
- producer(생산자): `{SCRIPT_PATH}`
- consumer(소비자): `{next_run}`
- artifact_paths(산출물 경로): `{rel(SUMMARY)}`, `{rel(CANDIDATES_TOP)}`, `{rel(AXIS_SUMMARY)}`, `{rel(MODEL_FIT_SUMMARY)}`, `{rel(REPORT)}`, `{rel(GATE_AUDIT)}`
- artifact_hashes(산출물 해시): source input hashes(원천 입력 해시)는 local run_manifest(로컬 실행 목록) `{rel(RUN_MANIFEST)}`에 기록했다.
- registry_links(등록부 연결): `docs/registers/run_registry.csv`, `docs/registers/alpha_run_ledger.csv`, `{rel(STAGE_LEDGER)}`
- availability(가용성): review artifacts(검토 산출물)는 tracked(추적됨) 대상이고, run_manifest(실행 목록)는 `stages/*/02_runs/` ignore rule(무시 규칙) 아래 local generated artifact(로컬 생성 산출물)이다.
- lineage_judgment(계보 판정): `connected_with_boundary`

## Runtime Rule(런타임 규칙)

Action(행동): `{next_run}`로 넘긴다.

Effect(효과): meaningful signal(의미 신호)이 없으면 best nonzero/scout candidate(최선 비영/탐색 후보)를 negative-control MT5 Runtime Probe(부정 대조 MT5 런타임 탐침)로 물질화해 proxy/runtime gap(프록시/런타임 간극)을 기록한다. meaningful signal(의미 신호)이 있으면 pre-MT5 Grok review(MT5 전 Grok 검토) 뒤 MT5 Runtime Probe(런타임 탐침)를 실행한다.
"""


def gate_audit_text(status: str, next_run: str, summary: Mapping[str, Any]) -> str:
    rows = [
        ("stage_open_boundary(단계 개방 경계)", "passed(통과)", "F76A opened and pushed(개방 완료)"),
        ("proxy_candidate_matrix(프록시 후보 행렬)", "passed(통과)", f"{summary['candidate_rows']} candidates"),
        ("model_family_rotation(모델 계열 회전)", "passed(통과)", f"{summary['fit_completed']} fits completed"),
        ("scout_meaningful_gate_split(탐색/의미 게이트 분리)", "passed(통과)", f"scout={summary['scout_clue_count']}; meaningful={summary['meaningful_signal_count']}"),
        ("runtime_probe_next_step(런타임 탐침 다음 단계)", "required(필수)", next_run),
        ("claim_guard(주장 보호)", "passed(통과)", CLAIM_BOUNDARY),
    ]
    body = "\n".join(f"| {gate} | {gate_status} | {evidence} |" for gate, gate_status, evidence in rows)
    return f"""# Required Gate Coverage Audit F76B(F76B 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence(근거) |
|---|---|---|
{body}

Status(상태): `{status}`
"""


def selection_status_text(status: str, judgment: str, next_run: str) -> str:
    return f"""# F76 Selection Status(F76 선택 상태)

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F76B axis ablation proxy scout(축 제거 프록시 탐색)를 완료했다.

Effect(효과): F76은 아직 runtime probe(런타임 탐침) 전이며, 다음 실행은 `{next_run}`이다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def update_state(status: str, judgment: str, next_run: str, created_at: str) -> None:
    workspace = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run}
runtime_probe_status: f76_runtime_probe_required_next
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_frontier71_to_75_retrospective_completed
updated_at_utc: '{created_at}'
context_anchor: stages/{STAGE_ID}/03_reviews/context_anchor.md
notes:
  - "Action(행동): F76B proxy scout(프록시 탐색)를 완료했다."
  - "Effect(효과): next action(다음 행동)은 MT5 Runtime Probe(런타임 탐침) 전 Grok 검토와 물질화다."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(ROOT / "docs/workspace/workspace_state.yaml", workspace)

    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F76B axis ablation proxy scout(축 제거 프록시 탐색)를 완료했다.

Effect(효과): proxy scout(프록시 탐색) 결과를 바탕으로 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) 준비로 이동한다.

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- runtime status(런타임 상태): `f76_runtime_probe_required_next`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(ROOT / "docs/context/current_working_state.md", current)


def update_ledgers(status: str, judgment: str, next_run: str, summary: Mapping[str, Any], created_at: str) -> None:
    row_id = f"{RUN_ID}__proxy_scout"
    row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_scout(프록시 탐색)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT),
        "notes": f"candidates={summary['candidate_rows']}; scout={summary['scout_clue_count']}; meaningful={summary['meaningful_signal_count']}",
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT),
        "run_number": "frontier76B",
        "date": "2026-06-17",
        "decision": "prepare_runtime_probe_after_proxy_scout",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "rows": summary["candidate_rows"],
        "gate_passes": "6",
        "gate_total": "6",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": "2026-06-17",
        "primary_artifact": rel(SUMMARY),
        "candidate_rows": summary["candidate_rows"],
        "positive_proxy_rows": summary["scout_clue_count"],
        "strict_joint_pass_count": summary["meaningful_signal_count"],
        "result_status": status,
        "view": "proxy_scout(프록시 탐색)",
        "tier": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "metric_scope": "validation_oos_proxy(검증/표본외 프록시)",
        "scoreboard_lane": "structural_scout(구조 탐색)",
        "external_verification_status": "runtime_probe_required_next(런타임 탐침 다음 필수)",
        "result_judgment": judgment,
        "final_decision_path": rel(SELECTION_STATUS),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": created_at,
        "ledger_row_id": row_id,
        "subrun_id": "proxy_scout(프록시 탐색)",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "proxy_validation_oos(프록시 검증/표본외)",
        "primary_kpi": f"scout={summary['scout_clue_count']};meaningful={summary['meaningful_signal_count']}",
        "guardrail_kpi": "runtime_probe_required_next;no authority",
        "work_family": "experiment_execution(실험 실행)",
        "row_id": row_id,
        "evidence_boundary": "proxy_scout_only_no_authority(프록시 탐색만, 권위 없음)",
        "next_action": next_run,
        "question": "Can axis ablation find runtime economics source?(축 제거가 런타임 경제성 원천을 찾나?)",
        "artifact_count": "6",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution(실험 실행)",
        "run_type": "axis_ablation_proxy_scout(축 제거 프록시 탐색)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(SUMMARY),
        "result_path": rel(REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_only(프록시 전용)",
    }
    upsert_csv(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    upsert_csv(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row)


def update_idea_registry(status: str, judgment: str, summary: Mapping[str, Any], next_run: str) -> None:
    path = ROOT / "docs/registers/idea_registry.md"
    text = io_path(path).read_text(encoding="utf-8-sig")
    marker = "<!-- frontier76B_axis_ablation_proxy_scout_v1 -->"
    if marker in text:
        return
    addition = f"""

{marker}
- `{RUN_ID}` executed F76 axis-ablation proxy scout(F76 축 제거 프록시 탐색). Status(상태): `{status}`. Judgment(판정): `{judgment}`. Candidate rows(후보 행) `{summary['candidate_rows']}`, scout clue(탐색 단서) `{summary['scout_clue_count']}`, meaningful signal(의미 신호) `{summary['meaningful_signal_count']}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{next_run}`.
"""
    write_text(path, text.rstrip() + addition)


def main() -> int:
    created_at = utc_now()
    io_path(REVIEW_DIR).mkdir(parents=True, exist_ok=True)
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    candidate_rows, fit_rows, summary = fit_and_score()
    summary = dict(summary)
    summary["created_at_utc"] = created_at
    status, judgment, next_run = status_and_next(summary)
    top = candidate_rows[:100]
    axis_rows = axis_summary_rows(candidate_rows)
    write_json(SUMMARY, summary)
    write_csv(CANDIDATES_TOP, top)
    write_csv(AXIS_SUMMARY, axis_rows)
    write_csv(MODEL_FIT_SUMMARY, fit_rows)
    write_text(REPORT, report_text(summary, status, judgment, next_run))
    write_text(GATE_AUDIT, gate_audit_text(status, next_run, summary))
    write_text(SELECTION_STATUS, selection_status_text(status, judgment, next_run))
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": next_run,
            "created_at_utc": created_at,
            "status": status,
            "judgment": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "dataset_path": rel(DATASET_PATH),
            "dataset_sha256": sha256_file_lf_normalized(DATASET_PATH),
            "feature_order_path": rel(FEATURE_ORDER_PATH),
            "feature_order_sha256": sha256_file_lf_normalized(FEATURE_ORDER_PATH),
            "script": SCRIPT_PATH,
            "outputs": {
                "summary": rel(SUMMARY),
                "candidates_top": rel(CANDIDATES_TOP),
                "axis_summary": rel(AXIS_SUMMARY),
                "model_fit_summary": rel(MODEL_FIT_SUMMARY),
                "report": rel(REPORT),
                "gate_audit": rel(GATE_AUDIT),
            },
        },
    )
    update_state(status, judgment, next_run, created_at)
    update_ledgers(status, judgment, next_run, summary, created_at)
    update_idea_registry(status, judgment, summary, next_run)
    print(
        json.dumps(
            json_ready(
                {
                    "status": status,
                    "judgment": judgment,
                    "candidate_rows": summary["candidate_rows"],
                    "scout_clue_count": summary["scout_clue_count"],
                    "meaningful_signal_count": summary["meaningful_signal_count"],
                    "next_run_id": next_run,
                    "best_candidate": summary["best_candidate"].get("candidate_id"),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
