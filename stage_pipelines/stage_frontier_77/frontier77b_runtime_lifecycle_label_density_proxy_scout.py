from __future__ import annotations

import csv
import hashlib
import json
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
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_77__runtime_lifecycle_label_density_rebuild"
RUN_ID = "frontier77B_runtime_lifecycle_label_density_proxy_scout_v1"
PARENT_RUN_ID = "frontier77A_stage_open_runtime_lifecycle_label_density_rebuild_v1"
NEXT_RUN_IF_MEANINGFUL = "frontier77C_pre_mt5_grok_runtime_lifecycle_probe_v1"
NEXT_RUN_IF_WEAK_NONZERO = "frontier77C_pre_mt5_grok_lifecycle_negative_control_runtime_probe_v1"
NEXT_RUN_IF_ZERO = "frontier77C_lifecycle_label_zero_signal_repair_plan_v1"

STATUS_MEANINGFUL = "proxy_lifecycle_meaningful_signal_pre_mt5_grok_required_no_authority"
STATUS_WEAK_NONZERO = "proxy_lifecycle_weak_nonzero_signal_negative_control_probe_required_no_authority"
STATUS_ZERO = "proxy_lifecycle_zero_signal_logic_repair_required_no_authority"
JUDGMENT_MEANINGFUL = "lifecycle_proxy_meaningful_signal_requires_grok_and_mt5_probe_no_authority"
JUDGMENT_WEAK_NONZERO = "lifecycle_proxy_weak_signal_requires_negative_control_runtime_probe_no_authority"
JUDGMENT_ZERO = "lifecycle_proxy_zero_signal_logic_repair_required_no_authority"
CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

INITIAL_BALANCE = 10_000.0
PROXY_COST_POINTS = 1.2
SCOUT_CLUE_GATE = (
    "validation and OOS net>0 or PF>=1.15, DD<=15%, lifecycle trades/day>=1.0, "
    "trade_count>=60 per split, and fragility recorded"
)
MEANINGFUL_SIGNAL_GATE = (
    "validation+OOS net>0, PF>=1.30, DD<=10%, lifecycle trades/day>=2.0, "
    "trade_count>=80 per split, and single-position compression recorded"
)
FINAL_LIKE_REFERENCE = (
    "reference only: PF>=2.0, DD<=10%, 5<=trades/day<=10, smooth equity proxy true"
)

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
RAW_BARS_PATH = ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"
SCRIPT_PATH = "stage_pipelines/stage_frontier_77/frontier77b_runtime_lifecycle_label_density_proxy_scout.py"

SUMMARY = REVIEW_DIR / "f77b_lifecycle_proxy_summary.json"
CANDIDATES_ALL = REVIEW_DIR / "f77b_lifecycle_proxy_candidates_all.csv"
CANDIDATES_TOP = REVIEW_DIR / "f77b_lifecycle_proxy_ranked_top100.csv"
AXIS_SUMMARY = REVIEW_DIR / "f77b_lifecycle_proxy_axis_summary.csv"
MODEL_FIT_SUMMARY = REVIEW_DIR / "f77b_lifecycle_model_fit_summary.csv"
LABEL_AUDIT = REVIEW_DIR / "f77b_lifecycle_label_audit.csv"
DATA_INTEGRITY = REVIEW_DIR / "f77b_data_integrity_review.json"
MODEL_VALIDATION = REVIEW_DIR / "f77b_model_validation_review.json"
REPORT = REVIEW_DIR / "frontier77B_runtime_lifecycle_label_density_proxy_scout_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f77b.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"


@dataclass(frozen=True)
class LifecycleSpec:
    name: str
    side: str
    hold_bars: int
    tp_points: float
    sl_points: float
    utility_quantile: float


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


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
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def sha256_binary(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_hash(path: Path) -> str:
    if not path_exists(path):
        return ""
    if path.suffix.lower() in {".parquet", ".csv"}:
        return sha256_binary(path)
    return sha256_file_lf_normalized(path)


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (REVIEW_DIR, RUN_DIR, SELECTED_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def feature_order() -> list[str]:
    return [line.strip() for line in read_text(FEATURE_ORDER_PATH).splitlines() if line.strip()]


def has_columns(features: Sequence[str], names: Sequence[str]) -> list[str]:
    available = set(features)
    return [name for name in names if name in available]


def feature_sets(features: Sequence[str]) -> dict[str, list[str]]:
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
            "return_1_over_atr_14",
            "atr_14",
            "atr_50",
        ],
    )
    trend = [
        f
        for f in features
        if any(key in f for key in ["ema", "sma", "rsi", "stoch", "ppo", "roc", "trix", "adx", "di_", "supertrend", "vortex"])
    ]
    volatility_session = [
        f
        for f in features
        if any(key in f for key in ["atr", "bollinger", "bb_", "historical_vol", "squeeze", "is_us_cash", "minutes_from", "first_30m", "last_30m"])
    ]
    no_mega = [
        f
        for f in features
        if not any(key in f for key in ["nvda_", "aapl_", "msft_", "amzn_", "mega8_", "top3_", "us100_minus_mega"])
    ]
    compact_lifecycle = sorted(set(price_action + trend + volatility_session))
    return {
        "full58": list(features),
        "price_action_core": price_action,
        "trend_momentum": trend,
        "volatility_session": volatility_session,
        "mega_cap_removed": no_mega,
        "compact_lifecycle": compact_lifecycle,
    }


def model_builders(random_state: int = 7702) -> dict[str, Callable[[], Any]]:
    return {
        "logistic_l2_balanced": lambda: make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=300, class_weight="balanced", C=0.5, solver="lbfgs"),
        ),
        "extra_trees_d7_l80": lambda: ExtraTreesClassifier(
            n_estimators=70,
            max_depth=7,
            min_samples_leaf=80,
            class_weight="balanced_subsample",
            random_state=random_state,
            n_jobs=-1,
        ),
        "hist_gbm_d4_l2": lambda: HistGradientBoostingClassifier(
            max_iter=100,
            max_leaf_nodes=31,
            max_depth=4,
            l2_regularization=0.1,
            learning_rate=0.05,
            random_state=random_state,
        ),
    }


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    for path in (DATASET_PATH, FEATURE_ORDER_PATH, RAW_BARS_PATH):
        if not path_exists(path):
            raise FileNotFoundError(f"missing required input: {rel(path)}")
    df = pd.read_parquet(io_path(DATASET_PATH)).copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    raw = pd.read_csv(
        io_path(RAW_BARS_PATH),
        usecols=["time_open_unix", "time_close_unix", "open", "high", "low", "close", "spread_points"],
    )
    raw["open_ts"] = pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
    raw["close_ts"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.sort_values("open_ts").reset_index(drop=True)
    for col in ["open", "high", "low", "close", "spread_points"]:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    return df, raw, feature_order()


def entry_indices(df: pd.DataFrame, raw: pd.DataFrame) -> np.ndarray:
    mapping = {ts: idx for idx, ts in enumerate(raw["open_ts"])}
    return df["timestamp"].map(mapping).fillna(-1).astype(int).to_numpy()


def lifecycle_specs() -> list[LifecycleSpec]:
    base = [
        (6, 10.0, 8.0),
        (12, 18.0, 12.0),
        (18, 26.0, 16.0),
    ]
    specs: list[LifecycleSpec] = []
    for side in ["long", "short"]:
        for hold, tp, sl in base:
            for q in [0.60, 0.70]:
                specs.append(LifecycleSpec(f"{side}_h{hold}_tp{int(tp)}_sl{int(sl)}_uq{int(q * 100)}", side, hold, tp, sl, q))
    return specs


def compute_path_outcome(raw: pd.DataFrame, indices: np.ndarray, spec: LifecycleSpec) -> dict[str, np.ndarray]:
    open_arr = raw["open"].to_numpy(float)
    high_arr = raw["high"].to_numpy(float)
    low_arr = raw["low"].to_numpy(float)
    close_arr = raw["close"].to_numpy(float)
    n = len(indices)
    pnl = np.full(n, np.nan, dtype=float)
    mfe = np.full(n, np.nan, dtype=float)
    mae = np.full(n, np.nan, dtype=float)
    exit_offset = np.zeros(n, dtype=int)
    valid = np.zeros(n, dtype=bool)
    side_mult = 1.0 if spec.side == "long" else -1.0
    max_idx = len(raw) - spec.hold_bars
    for row_idx, raw_idx in enumerate(indices):
        if raw_idx < 0 or raw_idx > max_idx:
            continue
        entry = open_arr[raw_idx]
        if not np.isfinite(entry) or entry <= 0:
            continue
        path_high = high_arr[raw_idx : raw_idx + spec.hold_bars]
        path_low = low_arr[raw_idx : raw_idx + spec.hold_bars]
        path_close = close_arr[raw_idx : raw_idx + spec.hold_bars]
        if not (np.isfinite(path_high).all() and np.isfinite(path_low).all() and np.isfinite(path_close).all()):
            continue
        if spec.side == "long":
            mfe[row_idx] = float(np.max(path_high - entry))
            mae[row_idx] = float(np.max(entry - path_low))
            terminal = float(path_close[-1] - entry)
            realized = terminal
            offset = spec.hold_bars
            for local_idx in range(spec.hold_bars):
                sl_hit = path_low[local_idx] <= entry - spec.sl_points
                tp_hit = path_high[local_idx] >= entry + spec.tp_points
                if sl_hit or tp_hit:
                    realized = -spec.sl_points if sl_hit else spec.tp_points
                    offset = local_idx + 1
                    break
        else:
            mfe[row_idx] = float(np.max(entry - path_low))
            mae[row_idx] = float(np.max(path_high - entry))
            terminal = float(entry - path_close[-1])
            realized = terminal
            offset = spec.hold_bars
            for local_idx in range(spec.hold_bars):
                sl_hit = path_high[local_idx] >= entry + spec.sl_points
                tp_hit = path_low[local_idx] <= entry - spec.tp_points
                if sl_hit or tp_hit:
                    realized = -spec.sl_points if sl_hit else spec.tp_points
                    offset = local_idx + 1
                    break
        pnl[row_idx] = realized - PROXY_COST_POINTS
        exit_offset[row_idx] = max(1, int(offset))
        valid[row_idx] = True
        _ = side_mult
    utility = pnl - 0.15 * np.nan_to_num(mae, nan=0.0) - 0.02 * exit_offset
    return {"pnl": pnl, "mfe": mfe, "mae": mae, "exit_offset": exit_offset, "valid": valid, "utility": utility}


def make_label(df: pd.DataFrame, outcome: Mapping[str, np.ndarray], spec: LifecycleSpec) -> np.ndarray:
    train_mask = (df["split"] == "train").to_numpy() & outcome["valid"]
    utility = outcome["utility"]
    threshold = float(np.nanquantile(utility[train_mask], spec.utility_quantile))
    return ((utility >= threshold) & (outcome["pnl"] > 0.0) & outcome["valid"]).astype(int)


def clean_matrices(df: pd.DataFrame, train_mask: np.ndarray, columns: Sequence[str]) -> dict[str, pd.DataFrame]:
    train = df.loc[train_mask, columns].replace([np.inf, -np.inf], np.nan)
    med = train.median(numeric_only=True).fillna(0.0)
    cleaned: dict[str, pd.DataFrame] = {}
    for split in ["train", "validation", "oos"]:
        part = df.loc[df["split"] == split, columns].replace([np.inf, -np.inf], np.nan).fillna(med)
        cleaned[split] = part.astype(float)
    return cleaned


def probability(model: Any, matrix: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(matrix))[:, 1]
    return np.asarray(model.predict(matrix), dtype=float)


def session_mask(df: pd.DataFrame, name: str) -> np.ndarray:
    if name == "all":
        return np.ones(len(df), dtype=bool)
    if name == "cash_open":
        return df.get("is_first_30m_after_open", pd.Series(0, index=df.index)).fillna(0).astype(int).to_numpy() == 1
    if name == "cash_mid":
        cash = df.get("is_us_cash_open", pd.Series(0, index=df.index)).fillna(0).astype(int).to_numpy() == 1
        first = df.get("is_first_30m_after_open", pd.Series(0, index=df.index)).fillna(0).astype(int).to_numpy() == 1
        last = df.get("is_last_30m_before_cash_close", pd.Series(0, index=df.index)).fillna(0).astype(int).to_numpy() == 1
        return cash & ~first & ~last
    if name == "cash_late":
        return df.get("is_last_30m_before_cash_close", pd.Series(0, index=df.index)).fillna(0).astype(int).to_numpy() == 1
    raise ValueError(name)


def risk_thresholds(df: pd.DataFrame) -> dict[str, float]:
    train = df.loc[df["split"] == "train"]

    def med(name: str, fallback: float) -> float:
        if name not in train:
            return fallback
        return float(pd.to_numeric(train[name], errors="coerce").median())

    return {
        "atr_ratio_median": med("atr_14_over_atr_50", 1.0),
        "boll_width_median": med("bollinger_width_20", 0.0),
        "adx_median": med("adx_14", 20.0),
    }


def risk_mask(df: pd.DataFrame, name: str, side: str, thresholds: Mapping[str, float]) -> np.ndarray:
    if name == "none":
        return np.ones(len(df), dtype=bool)
    if name == "low_volatility":
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


def lifecycle_select(raw_signal: np.ndarray, exit_offsets: np.ndarray) -> np.ndarray:
    selected = np.zeros_like(raw_signal, dtype=bool)
    remaining = 0
    for idx, flag in enumerate(raw_signal):
        if remaining > 0:
            remaining -= 1
            continue
        if bool(flag):
            selected[idx] = True
            remaining = max(int(exit_offsets[idx]) - 1, 0)
    return selected


def max_consecutive_losses(pnl: np.ndarray) -> int:
    best = 0
    current = 0
    for value in pnl:
        if value < 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def max_time_under_water_trades(pnl: np.ndarray) -> int:
    if len(pnl) == 0:
        return 0
    equity = INITIAL_BALANCE + np.cumsum(pnl)
    peak = -np.inf
    current = 0
    best = 0
    for value in equity:
        if value >= peak:
            peak = value
            current = 0
        else:
            current += 1
            best = max(best, current)
    return best


def max_drawdown_percent(pnl: np.ndarray) -> float:
    if len(pnl) == 0:
        return 0.0
    equity = INITIAL_BALANCE + np.cumsum(pnl)
    peaks = np.maximum.accumulate(equity)
    dd = (peaks - equity) / INITIAL_BALANCE * 100.0
    return float(np.max(dd)) if len(dd) else 0.0


def lifecycle_kpi(split_df: pd.DataFrame, selected: np.ndarray, outcome: Mapping[str, np.ndarray]) -> dict[str, Any]:
    pnl = np.asarray(outcome["pnl"])[selected]
    exit_offsets = np.asarray(outcome["exit_offset"])[selected]
    mae = np.asarray(outcome["mae"])[selected]
    if len(pnl) == 0:
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
            "avg_hold_bars": 0.0,
            "avg_mae": 0.0,
            "max_consecutive_loss": 0,
            "time_under_water_trades": 0,
            "smooth_equity_proxy": 0,
        }
    gross_profit = float(pnl[pnl > 0].sum())
    gross_loss = float(pnl[pnl < 0].sum())
    net = float(pnl.sum())
    pf = gross_profit / abs(gross_loss) if gross_loss < 0 else (999.0 if gross_profit > 0 else 0.0)
    dd_pct = max_drawdown_percent(pnl)
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    trades = int(len(pnl))
    dates = pd.to_datetime(split_df.loc[selected, "timestamp"], errors="coerce").dt.date.nunique()
    avg_win = float(wins.mean()) if len(wins) else 0.0
    avg_loss = float(losses.mean()) if len(losses) else 0.0
    recovery = net / (dd_pct / 100.0 * INITIAL_BALANCE) if dd_pct > 0 else (999.0 if net > 0 else 0.0)
    max_loss = max_consecutive_losses(pnl)
    tuw = max_time_under_water_trades(pnl)
    smooth = int(net > 0 and dd_pct <= 10.0 and max_loss <= 6 and tuw <= max(10, trades // 3))
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
        "recovery": recovery,
        "avg_hold_bars": float(np.mean(exit_offsets)) if len(exit_offsets) else 0.0,
        "avg_mae": float(np.nanmean(mae)) if len(mae) else 0.0,
        "max_consecutive_loss": max_loss,
        "time_under_water_trades": tuw,
        "smooth_equity_proxy": smooth,
    }


def scout_gate(metrics: Mapping[str, Any]) -> bool:
    return (
        int(metrics["trade_count"]) >= 60
        and float(metrics["trades_day"]) >= 1.0
        and float(metrics["dd_pct"]) <= 15.0
        and (float(metrics["net"]) > 0.0 or float(metrics["pf"]) >= 1.15)
    )


def meaningful_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 1.30
            and float(metrics["dd_pct"]) <= 10.0
            and float(metrics["trades_day"]) >= 2.0
            and int(metrics["trade_count"]) >= 80
        )

    return ok(val) and ok(oos)


def final_like_reference(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 2.0
            and float(metrics["dd_pct"]) <= 10.0
            and 5.0 <= float(metrics["trades_day"]) <= 10.0
            and int(metrics["smooth_equity_proxy"]) == 1
        )

    return ok(val) and ok(oos)


def rank_score(val: Mapping[str, Any], oos: Mapping[str, Any], meaningful: bool, scout: bool, near: bool) -> float:
    min_pf = min(float(val["pf"]), float(oos["pf"]), 5.0)
    min_tpd = min(float(val["trades_day"]), float(oos["trades_day"]), 10.0)
    max_dd = max(float(val["dd_pct"]), float(oos["dd_pct"]))
    min_net = min(float(val["net"]), float(oos["net"]))
    smooth = int(val["smooth_equity_proxy"]) + int(oos["smooth_equity_proxy"])
    return (
        (1_000_000.0 if meaningful else 0.0)
        + (250_000.0 if near else 0.0)
        + (100_000.0 if scout else 0.0)
        + (20_000.0 if min_net > 0 else 0.0)
        + min_pf * 3_000.0
        + min_tpd * 1_200.0
        + smooth * 2_000.0
        - max_dd * 250.0
        + min_net * 0.05
    )


def fit_and_score() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    df, raw, features = load_inputs()
    indices = entry_indices(df, raw)
    feature_map = feature_sets(features)
    builders = model_builders()
    thresholds = risk_thresholds(df)
    specs = lifecycle_specs()
    sessions = ["all", "cash_open", "cash_mid", "cash_late"]
    risk_filters = ["none", "low_volatility", "trend_aligned", "mean_revert"]
    prob_quantiles = [0.80, 0.87, 0.93]

    candidate_rows: list[dict[str, Any]] = []
    fit_rows: list[dict[str, Any]] = []
    label_rows: list[dict[str, Any]] = []
    candidate_id = 0

    for spec in specs:
        outcome = compute_path_outcome(raw, indices, spec)
        label = make_label(df, outcome, spec)
        train_valid = (df["split"] == "train").to_numpy() & outcome["valid"]
        label_rows.append(
            {
                "label_name": spec.name,
                "side": spec.side,
                "hold_bars": spec.hold_bars,
                "tp_points": spec.tp_points,
                "sl_points": spec.sl_points,
                "utility_quantile": spec.utility_quantile,
                "train_valid_rows": int(train_valid.sum()),
                "train_positive_rows": int(label[train_valid].sum()),
                "train_positive_rate": float(label[train_valid].mean()) if train_valid.sum() else 0.0,
                "validation_valid_rows": int(((df["split"] == "validation").to_numpy() & outcome["valid"]).sum()),
                "oos_valid_rows": int(((df["split"] == "oos").to_numpy() & outcome["valid"]).sum()),
            }
        )
        if train_valid.sum() == 0 or label[train_valid].sum() == 0 or label[train_valid].sum() == train_valid.sum():
            fit_rows.append(
                {
                    "label_name": spec.name,
                    "feature_set": "all",
                    "model": "all",
                    "status": "skipped_single_class_or_empty",
                    "train_rows": int(train_valid.sum()),
                    "positive_rows": int(label[train_valid].sum()) if train_valid.sum() else 0,
                }
            )
            continue
        for feature_set_name, cols in feature_map.items():
            if not cols:
                continue
            matrices = clean_matrices(df, train_valid, cols)
            train_matrix = df.loc[train_valid, cols].replace([np.inf, -np.inf], np.nan)
            med = train_matrix.median(numeric_only=True).fillna(0.0)
            train_matrix = train_matrix.fillna(med).astype(float)
            y_train = label[train_valid]
            for model_name, builder in builders.items():
                model = builder()
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        model.fit(train_matrix, y_train)
                    train_probs = probability(model, train_matrix)
                    probs = {split: probability(model, matrices[split]) for split in ["validation", "oos"]}
                    fit_rows.append(
                        {
                            "label_name": spec.name,
                            "feature_set": feature_set_name,
                            "feature_count": len(cols),
                            "model": model_name,
                            "status": "fit_completed",
                            "train_rows": int(len(y_train)),
                            "positive_rows": int(y_train.sum()),
                            "positive_rate": float(y_train.mean()),
                        }
                    )
                except Exception as exc:  # noqa: BLE001
                    fit_rows.append(
                        {
                            "label_name": spec.name,
                            "feature_set": feature_set_name,
                            "feature_count": len(cols),
                            "model": model_name,
                            "status": "fit_failed",
                            "error": str(exc)[:200],
                            "train_rows": int(len(y_train)),
                            "positive_rows": int(y_train.sum()),
                        }
                    )
                    continue

                for q in prob_quantiles:
                    prob_threshold = float(np.quantile(train_probs, q))
                    for session in sessions:
                        for risk_filter in risk_filters:
                            split_payload: dict[str, dict[str, Any]] = {}
                            row_base: dict[str, Any] = {}
                            scout = False
                            raw_any = 0
                            entry_any = 0
                            for split in ["validation", "oos"]:
                                split_mask_global = (df["split"] == split).to_numpy()
                                split_df = df.loc[split_mask_global].reset_index(drop=True)
                                split_outcome = {
                                    key: np.asarray(value)[split_mask_global]
                                    for key, value in outcome.items()
                                }
                                valid = np.asarray(split_outcome["valid"], dtype=bool)
                                raw_signal = (
                                    (probs[split] >= prob_threshold)
                                    & valid
                                    & session_mask(split_df, session)
                                    & risk_mask(split_df, risk_filter, spec.side, thresholds)
                                )
                                selected = lifecycle_select(raw_signal, np.asarray(split_outcome["exit_offset"], dtype=int))
                                metrics = lifecycle_kpi(split_df, selected, split_outcome)
                                split_payload[split] = metrics
                                raw_any += int(raw_signal.sum())
                                entry_any += int(selected.sum())
                                scout = scout or scout_gate(metrics)
                                row_base[f"{split}_raw_signal_count"] = int(raw_signal.sum())
                                row_base[f"{split}_lifecycle_trade_count"] = int(selected.sum())
                                row_base[f"{split}_signal_to_trade_ratio"] = int(selected.sum()) / int(raw_signal.sum()) if int(raw_signal.sum()) else 0.0
                            val = split_payload["validation"]
                            oos = split_payload["oos"]
                            meaningful = meaningful_gate(val, oos)
                            near = final_like_reference(val, oos)
                            dual_positive = float(val["net"]) > 0.0 and float(oos["net"]) > 0.0
                            candidate_id += 1
                            row: dict[str, Any] = {
                                "candidate_id": f"f77b_{candidate_id:05d}",
                                "label_name": spec.name,
                                "side": spec.side,
                                "hold_bars": spec.hold_bars,
                                "tp_points": spec.tp_points,
                                "sl_points": spec.sl_points,
                                "utility_quantile": spec.utility_quantile,
                                "feature_set": feature_set_name,
                                "feature_count": len(cols),
                                "model": model_name,
                                "prob_quantile": q,
                                "prob_threshold": prob_threshold,
                                "session": session,
                                "risk_filter": risk_filter,
                                "raw_signal_total": raw_any,
                                "lifecycle_trade_total": entry_any,
                                "overall_signal_to_trade_ratio": entry_any / raw_any if raw_any else 0.0,
                                "scout_clue": int(scout),
                                "meaningful_signal": int(meaningful),
                                "final_like_reference": int(near),
                                "dual_positive": int(dual_positive),
                                "rank_score": rank_score(val, oos, meaningful, scout, near),
                            }
                            row.update(row_base)
                            for prefix, metrics in [("val", val), ("oos", oos)]:
                                for key, value in metrics.items():
                                    row[f"{prefix}_{key}"] = value
                            candidate_rows.append(row)

    candidate_rows.sort(key=lambda row: float(row["rank_score"]), reverse=True)
    best = candidate_rows[0] if candidate_rows else {}
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "candidate_rows": len(candidate_rows),
        "fit_rows": len(fit_rows),
        "fit_completed": sum(1 for row in fit_rows if row.get("status") == "fit_completed"),
        "label_rows": len(label_rows),
        "scout_clue_count": sum(int(row["scout_clue"]) for row in candidate_rows),
        "meaningful_signal_count": sum(int(row["meaningful_signal"]) for row in candidate_rows),
        "final_like_reference_count": sum(int(row["final_like_reference"]) for row in candidate_rows),
        "dual_positive_count": sum(int(row["dual_positive"]) for row in candidate_rows),
        "nonzero_lifecycle_trade_candidates": sum(1 for row in candidate_rows if int(row["lifecycle_trade_total"]) > 0),
        "best_candidate": best,
        "claim_boundary": CLAIM_BOUNDARY,
        "scout_clue_gate": SCOUT_CLUE_GATE,
        "meaningful_signal_gate": MEANINGFUL_SIGNAL_GATE,
        "final_like_reference": FINAL_LIKE_REFERENCE,
    }
    return candidate_rows, fit_rows, label_rows, summary


def axis_summary_rows(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis in ["label_name", "side", "hold_bars", "feature_set", "model", "session", "risk_filter"]:
        values = sorted({str(row[axis]) for row in candidate_rows})
        for value in values:
            subset = [row for row in candidate_rows if str(row[axis]) == value]
            best = max(subset, key=lambda row: float(row["rank_score"]))
            rows.append(
                {
                    "axis": axis,
                    "value": value,
                    "candidate_rows": len(subset),
                    "scout_clue_count": sum(int(row["scout_clue"]) for row in subset),
                    "meaningful_signal_count": sum(int(row["meaningful_signal"]) for row in subset),
                    "final_like_reference_count": sum(int(row["final_like_reference"]) for row in subset),
                    "dual_positive_count": sum(int(row["dual_positive"]) for row in subset),
                    "best_candidate": best["candidate_id"],
                    "best_rank_score": best["rank_score"],
                    "best_val_net_pf_dd_tpd": f"{best['val_net']}/{best['val_pf']}/{best['val_dd_pct']}/{best['val_trades_day']}",
                    "best_oos_net_pf_dd_tpd": f"{best['oos_net']}/{best['oos_pf']}/{best['oos_dd_pct']}/{best['oos_trades_day']}",
                    "best_signal_to_trade_ratio": best["overall_signal_to_trade_ratio"],
                }
            )
    return rows


def status_and_next(summary: Mapping[str, Any]) -> tuple[str, str, str]:
    if int(summary["meaningful_signal_count"]) > 0:
        return STATUS_MEANINGFUL, JUDGMENT_MEANINGFUL, NEXT_RUN_IF_MEANINGFUL
    if int(summary["nonzero_lifecycle_trade_candidates"]) > 0:
        return STATUS_WEAK_NONZERO, JUDGMENT_WEAK_NONZERO, NEXT_RUN_IF_WEAK_NONZERO
    return STATUS_ZERO, JUDGMENT_ZERO, NEXT_RUN_IF_ZERO


def data_integrity_review(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "data_source": [rel(DATASET_PATH), rel(FEATURE_ORDER_PATH), rel(RAW_BARS_PATH)],
        "time_axis": (
            "feature timestamp(피처 시간표시)은 closed-bar key(닫힌 봉 키)로 다루고, "
            "raw open_ts == feature timestamp를 next-bar entry open(다음 봉 시가 진입)으로 사용한다."
        ),
        "sample_scope": "US100 M5 train/validation/oos split_v1; raw bars cover feature range plus forward path.",
        "missing_or_duplicate_check": "entry open mapping is required for every feature row; missing rows would be invalid for label materialization.",
        "feature_label_boundary": "features use current closed bar; lifecycle labels use next bar open and future high/low/close path only after entry.",
        "split_boundary": "time-ordered train/validation/oos; thresholds and probability cutoffs learned from train only.",
        "leakage_risk": "highest risk is accidentally using the current feature bar high/low as future path; script starts path at next bar open_ts.",
        "data_hash_or_identity": {
            "dataset_sha256": file_hash(DATASET_PATH),
            "feature_order_sha256": file_hash(FEATURE_ORDER_PATH),
            "raw_bars_sha256": file_hash(RAW_BARS_PATH),
            "candidate_rows": summary.get("candidate_rows"),
        },
        "integrity_judgment": "usable_with_boundary",
    }


def model_validation_review(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "model_family": "logistic_l2_balanced, extra_trees_d7_l80, hist_gbm_d4_l2",
        "target_and_label": "runtime lifecycle utility labels(런타임 생명주기 효용 라벨) from TP/SL first-touch, hold, MAE, and PnL.",
        "split_method": "time-ordered holdout train/validation/oos; no WFO in F77B scout.",
        "selection_metric": "rank_score combining meaningful gate, scout gate, PF, DD, lifecycle trades/day, net, and smooth proxy.",
        "secondary_metrics": "signal_to_trade_ratio, avg_hold_bars, MAE, max consecutive loss, time under water trades.",
        "threshold_policy": "probability/rank quantiles searched on train predictions; scores are ranking scores, not calibrated probabilities.",
        "overfit_risk": "multiple-testing across label/feature/model/session/risk arms; F77B remains exploratory until MT5 probe.",
        "calibration_risk": "classifier outputs are selection ranks; no probability calibration claim.",
        "comparison_baseline": "F76 independent-signal proxy and lifecycle-aware repair negative memory.",
        "validation_judgment": "exploratory_proxy_scout",
        "summary_counts": {
            "fit_completed": summary.get("fit_completed"),
            "candidate_rows": summary.get("candidate_rows"),
            "meaningful_signal_count": summary.get("meaningful_signal_count"),
            "scout_clue_count": summary.get("scout_clue_count"),
        },
    }


def report_text(created_at: str, summary: Mapping[str, Any], top_rows: Sequence[Mapping[str, Any]]) -> str:
    status, judgment, next_run = status_and_next(summary)
    best = summary.get("best_candidate") or {}
    lines = [
        "# Frontier77B Runtime Lifecycle Label Density Proxy Scout Report(F77B 런타임 생명주기 라벨/밀도 프록시 탐색 보고서)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- candidate rows(후보 행): `{summary['candidate_rows']}`",
        f"- fit completed(학습 완료): `{summary['fit_completed']}/{summary['fit_rows']}`",
        f"- scout clue count(탐색 단서 수): `{summary['scout_clue_count']}`",
        f"- meaningful signal count(의미 신호 수): `{summary['meaningful_signal_count']}`",
        f"- final-like reference count(최종 유사 참조 수): `{summary['final_like_reference_count']}`",
        f"- nonzero lifecycle trade candidates(비영 생명주기 거래 후보): `{summary['nonzero_lifecycle_trade_candidates']}`",
        f"- next action(다음 행동): `{next_run}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Best Candidate(최선 후보)",
        "",
        f"- candidate(후보): `{best.get('candidate_id', '')}`",
        f"- axes(축): `{best.get('label_name', '')}/{best.get('feature_set', '')}/{best.get('model', '')}/{best.get('session', '')}/{best.get('risk_filter', '')}/q{best.get('prob_quantile', '')}`",
        f"- validation net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래): `{best.get('val_net', '')}/{best.get('val_pf', '')}/{best.get('val_dd_pct', '')}/{best.get('val_trades_day', '')}/{best.get('val_trade_count', '')}`",
        f"- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일거래/거래): `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_trades_day', '')}/{best.get('oos_trade_count', '')}`",
        f"- signal_to_trade_ratio(신호-거래 비율): `{best.get('overall_signal_to_trade_ratio', '')}`",
        f"- avg hold val/oos(평균 보유 검증/표본외): `{best.get('val_avg_hold_bars', '')}/{best.get('oos_avg_hold_bars', '')}`",
        "",
        "## Top Rows(상위 행)",
        "",
        "| rank(순위) | candidate(후보) | axes(축) | val net/PF/DD/tpd(검증) | oos net/PF/DD/tpd(표본외) | raw->trade val/oos(원신호->거래) | flags(표식) |",
        "|---:|---|---|---|---|---|---|",
    ]
    for idx, row in enumerate(top_rows[:12], start=1):
        lines.append(
            "| {idx} | `{candidate}` | `{axes}` | `{val}` | `{oos}` | `{ratio}` | `{flags}` |".format(
                idx=idx,
                candidate=row.get("candidate_id", ""),
                axes="/".join(
                    str(row.get(key, ""))
                    for key in ["label_name", "feature_set", "model", "session", "risk_filter", "prob_quantile"]
                ),
                val=f"{row.get('val_net', '')}/{row.get('val_pf', '')}/{row.get('val_dd_pct', '')}/{row.get('val_trades_day', '')}",
                oos=f"{row.get('oos_net', '')}/{row.get('oos_pf', '')}/{row.get('oos_dd_pct', '')}/{row.get('oos_trades_day', '')}",
                ratio=f"{row.get('validation_raw_signal_count', '')}->{row.get('validation_lifecycle_trade_count', '')}/{row.get('oos_raw_signal_count', '')}->{row.get('oos_lifecycle_trade_count', '')}",
                flags=f"scout={row.get('scout_clue', '')};meaningful={row.get('meaningful_signal', '')};near={row.get('final_like_reference', '')}",
            )
        )
    lines.extend(
        [
            "",
            "## Data Integrity(데이터 무결성)",
            "",
            "- data_source(데이터 원천): model input parquet(모델 입력 파케이), feature order(피처 순서), raw OHLC bars(원천 OHLC 봉).",
            "- time_axis(시간축): feature timestamp(피처 시간표시)는 closed-bar key(닫힌 봉 키), entry(진입)는 raw open_ts == feature timestamp인 next bar open(다음 봉 시가).",
            "- feature_label_boundary(피처/라벨 경계): feature(피처)는 현재 닫힌 봉까지만 쓰고, label(라벨)은 그 다음 봉부터의 high/low/close path(고가/저가/종가 경로)로 만든다.",
            "- integrity_judgment(무결성 판정): `usable_with_boundary(경계 포함 사용 가능)`.",
            "",
            "## Model Validation(모델 검증)",
            "",
            "- validation_judgment(검증 판정): `exploratory_proxy_scout(탐색 프록시)`.",
            "- threshold_policy(임계값 정책): train prediction quantile(학습 예측 분위수)을 사용하며 calibrated probability(보정 확률)는 주장하지 않는다.",
            "- overfit_risk(과적합 위험): label/feature/model/session/risk arms(라벨/피처/모델/세션/위험 팔) 다중 탐색이 있으므로 MT5 probe(MT5 탐침) 전에는 scout clue(탐색 단서)까지만 말한다.",
            "",
            "## Runtime Rule(런타임 규칙)",
            "",
            f"Action(행동): next run(다음 실행)은 `{next_run}`.",
            "",
            "Effect(효과): meaningful signal(의미 신호)이면 pre-MT5 Grok review(MT5 전 Grok 검토) 뒤 MT5 Runtime Probe(MT5 런타임 탐침)를 실행하고, weak nonzero signal(약한 비영 신호)이면 negative-control MT5 Runtime Probe(부정 대조 MT5 탐침)를 준비한다.",
        ]
    )
    return "\n".join(lines)


def gate_audit_text(created_at: str, summary: Mapping[str, Any]) -> str:
    status, _judgment, next_run = status_and_next(summary)
    return f"""# Required Gate Coverage Audit F77B(F77B 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F77A stage open(F77A 단계 개방) | `passed(통과)` | parent `{PARENT_RUN_ID}` |
| data integrity(데이터 무결성) | `usable_with_boundary(경계 포함 사용 가능)` | `{rel(DATA_INTEGRITY)}` |
| lifecycle label materialization(생명주기 라벨 물질화) | `passed(통과)` | `{summary['label_rows']}` label rows |
| model rotation(모델 회전) | `passed(통과)` | `{summary['fit_completed']}/{summary['fit_rows']}` fits |
| proxy KPI contract(프록시 KPI 계약) | `passed(통과)` | `{rel(SUMMARY)}` |
| meaningful signal gate(의미 신호 게이트) | `{summary['meaningful_signal_count']}` | `{MEANINGFUL_SIGNAL_GATE}` |
| runtime next action(런타임 다음 행동) | `{next_run}` | status `{status}` |
| final claim guard(최종 주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def selection_status_text(created_at: str, status: str, judgment: str, next_run: str) -> str:
    return f"""# F77 Selection Status(F77 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F77B runtime lifecycle proxy scout(런타임 생명주기 프록시 탐색)를 실행했다.

Effect(효과): 다음 행동은 Grok review(Grok 검토)를 거친 MT5 Runtime Probe(MT5 런타임 탐침) 준비다.

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def ledger_row(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    best = summary.get("best_candidate") or {}
    row_id = f"{RUN_ID}__proxy_scout"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_scout(프록시 탐색)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT),
        "notes": f"candidates={summary['candidate_rows']}; scout={summary['scout_clue_count']}; meaningful={summary['meaningful_signal_count']}; next={next_run}",
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT),
        "run_number": "frontier77B",
        "date": created_at[:10],
        "decision": judgment,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "rows": summary["candidate_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_proxy": best.get("candidate_id", ""),
        "candidate_rows": summary["candidate_rows"],
        "positive_proxy_rows": summary["scout_clue_count"],
        "strict_joint_pass_count": summary["meaningful_signal_count"],
        "best_model_id": best.get("model", ""),
        "best_proxy_net": best.get("oos_net", ""),
        "net_profit": best.get("oos_net", ""),
        "profit_factor": best.get("oos_pf", ""),
        "drawdown": best.get("oos_dd_pct", ""),
        "max_drawdown_percent": best.get("oos_dd_pct", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "trade_density": best.get("oos_trades_day", ""),
        "expectancy": best.get("oos_expectancy", ""),
        "recovery_factor": best.get("oos_recovery", ""),
        "view": "proxy_validation_oos_lifecycle",
        "tier": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "metric_scope": "lifecycle_proxy_validation_oos(생명주기 프록시 검증/표본외)",
        "scoreboard_lane": "runtime_lifecycle_label_density_proxy(런타임 생명주기 라벨/밀도 프록시)",
        "external_verification_status": "mt5_runtime_probe_required_next(MT5 런타임 탐침 다음 필수)",
        "result_judgment": judgment,
        "final_decision_path": rel(SELECTION_STATUS),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": created_at,
        "ledger_row_id": row_id,
        "subrun_id": "runtime_lifecycle_proxy_scout(런타임 생명주기 프록시 탐색)",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "proxy_validation_oos_lifecycle(생명주기 프록시 검증/표본외)",
        "primary_kpi": f"scout={summary['scout_clue_count']};meaningful={summary['meaningful_signal_count']};near={summary['final_like_reference_count']}",
        "guardrail_kpi": "runtime_probe_required_next;no authority",
        "work_family": "experiment_execution(실험 실행)",
        "row_id": row_id,
        "evidence_boundary": "proxy_scout_only_no_authority(프록시 탐색만, 권위 없음)",
        "next_action": next_run,
        "question": "Can lifecycle labels reduce proxy/runtime gap?(생명주기 라벨이 프록시/런타임 간극을 줄이나?)",
        "artifact_count": "10",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution(실험 실행)",
        "run_type": "runtime_lifecycle_label_density_proxy_scout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST),
        "result_path": rel(REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_only(프록시 전용)",
        "expected_net_profit": best.get("oos_net", ""),
        "expected_profit_factor": best.get("oos_pf", ""),
        "expected_trade_count": best.get("oos_trade_count", ""),
        "expected_trade_density": best.get("oos_trades_day", ""),
    }


def update_ledgers(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> None:
    row = ledger_row(created_at, status, judgment, next_run, summary)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_idea_registry(status: str, judgment: str, summary: Mapping[str, Any], next_run: str) -> None:
    marker = "<!-- frontier77B_runtime_lifecycle_label_density_proxy_scout_v1 -->"
    text = read_text(IDEA_REGISTRY)
    if marker in text:
        return
    best = summary.get("best_candidate") or {}
    addition = f"""

{marker}
- `{RUN_ID}` executed runtime lifecycle label density proxy scout(런타임 생명주기 라벨/밀도 프록시 탐색). Status(상태): `{status}`. Judgment(판정): `{judgment}`. Candidate rows(후보 행) `{summary['candidate_rows']}`, scout clue(탐색 단서) `{summary['scout_clue_count']}`, meaningful signal(의미 신호) `{summary['meaningful_signal_count']}`, best OOS net/PF/DD/tpd(최선 표본외 순수익/수익 팩터/손실폭/일거래) `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_trades_day', '')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{next_run}`.
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_state_files(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> None:
    best = summary.get("best_candidate") or {}
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run}
runtime_probe_status: f77_pre_mt5_grok_required_before_runtime_probe
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f76_closeout_1_of_5
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F77B runtime lifecycle proxy scout(런타임 생명주기 프록시 탐색)를 완료했다."
  - "Effect(효과): raw OHLC path(원천 OHLC 경로) 기반 label/trade_shape(라벨/거래 형태) 후보를 MT5 전 검토 대상으로 만들었다."
  - "Best proxy(최선 프록시): {best.get('candidate_id', '')} OOS net/PF/DD/tpd {best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_trades_day', '')}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)

    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F77B runtime lifecycle label density proxy scout(런타임 생명주기 라벨/밀도 프록시 탐색)를 실행했다.

Effect(효과): F77은 이제 raw OHLC path(원천 OHLC 경로), first-touch exit(최초접촉 청산), single-position occupancy(단일 포지션 점유)를 포함한 proxy evidence(프록시 근거)를 가진다.

## Proxy Result(프록시 결과)

- candidate rows(후보 행): `{summary['candidate_rows']}`
- scout clue count(탐색 단서 수): `{summary['scout_clue_count']}`
- meaningful signal count(의미 신호 수): `{summary['meaningful_signal_count']}`
- final-like reference count(최종 유사 참조 수): `{summary['final_like_reference_count']}`
- best OOS net/PF/DD/tpd(최선 표본외 순수익/수익 팩터/손실폭/일거래): `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_trades_day', '')}`

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- runtime status(런타임 상태): `f77_pre_mt5_grok_required_before_runtime_probe`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    write_text(SELECTION_STATUS, selection_status_text(created_at, status, judgment, next_run))


def manifest_payload(
    created_at: str,
    status: str,
    judgment: str,
    next_run: str,
    summary: Mapping[str, Any],
    top_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "dataset_path": rel(DATASET_PATH),
        "dataset_sha256": file_hash(DATASET_PATH),
        "feature_order_path": rel(FEATURE_ORDER_PATH),
        "feature_order_sha256": file_hash(FEATURE_ORDER_PATH),
        "raw_bars_path": rel(RAW_BARS_PATH),
        "raw_bars_sha256": file_hash(RAW_BARS_PATH),
        "script": SCRIPT_PATH,
        "summary": summary,
        "top_candidates_preview": list(top_rows[:5]),
        "outputs": {
            "summary": rel(SUMMARY),
            "candidates_all": rel(CANDIDATES_ALL),
            "candidates_top": rel(CANDIDATES_TOP),
            "axis_summary": rel(AXIS_SUMMARY),
            "model_fit_summary": rel(MODEL_FIT_SUMMARY),
            "label_audit": rel(LABEL_AUDIT),
            "data_integrity": rel(DATA_INTEGRITY),
            "model_validation": rel(MODEL_VALIDATION),
            "report": rel(REPORT),
            "gate_audit": rel(GATE_AUDIT),
        },
    }


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    candidate_rows, fit_rows, label_rows, summary = fit_and_score()
    summary = dict(summary)
    summary["created_at_utc"] = created_at
    status, judgment, next_run = status_and_next(summary)
    top_rows = candidate_rows[:100]
    axis_rows = axis_summary_rows(candidate_rows)
    data_review = data_integrity_review(summary)
    model_review = model_validation_review(summary)

    write_json(SUMMARY, summary)
    write_csv(CANDIDATES_ALL, candidate_rows)
    write_csv(CANDIDATES_TOP, top_rows)
    write_csv(AXIS_SUMMARY, axis_rows)
    write_csv(MODEL_FIT_SUMMARY, fit_rows)
    write_csv(LABEL_AUDIT, label_rows)
    write_json(DATA_INTEGRITY, data_review)
    write_json(MODEL_VALIDATION, model_review)
    write_text(REPORT, report_text(created_at, summary, top_rows))
    write_text(GATE_AUDIT, gate_audit_text(created_at, summary))
    write_json(RUN_MANIFEST, manifest_payload(created_at, status, judgment, next_run, summary, top_rows))
    update_state_files(created_at, status, judgment, next_run, summary)
    update_ledgers(created_at, status, judgment, next_run, summary)
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
                    "final_like_reference_count": summary["final_like_reference_count"],
                    "nonzero_lifecycle_trade_candidates": summary["nonzero_lifecycle_trade_candidates"],
                    "next_run_id": next_run,
                    "best_candidate": summary["best_candidate"].get("candidate_id") if summary.get("best_candidate") else "",
                    "best_oos_net_pf_dd_tpd": [
                        summary["best_candidate"].get("oos_net") if summary.get("best_candidate") else "",
                        summary["best_candidate"].get("oos_pf") if summary.get("best_candidate") else "",
                        summary["best_candidate"].get("oos_dd_pct") if summary.get("best_candidate") else "",
                        summary["best_candidate"].get("oos_trades_day") if summary.get("best_candidate") else "",
                    ],
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
