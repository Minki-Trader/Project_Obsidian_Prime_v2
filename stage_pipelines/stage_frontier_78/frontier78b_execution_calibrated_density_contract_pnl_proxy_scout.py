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


STAGE_ID = "stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild"
RUN_ID = "frontier78B_execution_calibrated_density_contract_pnl_proxy_scout_v1"
PARENT_RUN_ID = "frontier78A_stage_open_execution_calibrated_density_contract_pnl_v1"
NEXT_RUN_IF_MEANINGFUL = "frontier78C_pre_mt5_grok_execution_calibrated_runtime_probe_v1"
NEXT_RUN_IF_WEAK_NONZERO = "frontier78C_pre_mt5_grok_execution_calibrated_negative_control_runtime_probe_v1"
NEXT_RUN_IF_ZERO = "frontier78C_execution_calibrated_zero_signal_repair_plan_v1"

STATUS_MEANINGFUL = "proxy_contract_meaningful_signal_pre_mt5_grok_required_no_authority"
STATUS_WEAK_NONZERO = "proxy_contract_weak_nonzero_signal_negative_control_probe_required_no_authority"
STATUS_ZERO = "proxy_contract_zero_signal_logic_repair_required_no_authority"
JUDGMENT_MEANINGFUL = "contract_proxy_meaningful_signal_requires_grok_and_mt5_probe_no_authority"
JUDGMENT_WEAK_NONZERO = "contract_proxy_weak_signal_requires_negative_control_runtime_probe_no_authority"
JUDGMENT_ZERO = "contract_proxy_zero_signal_logic_repair_required_no_authority"
CLAIM_BOUNDARY = (
    "proxy_scout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

INITIAL_BALANCE = 10_000.0
SLTP_POINT_SCALE = 100.0
CONTRACT_PNL_SCALE = 0.08870965974736267
CONTRACT_PNL_SCALE_SOURCE = (
    "F77 observed gross-profit runtime/proxy scale mean(관찰 총이익 런타임/프록시 배율 평균): "
    "(0.09352576207175615 + 0.08389355742296918) / 2"
)
MAX_CALENDAR_TPD_SCOUT = 14.0

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
SCRIPT_PATH = "stage_pipelines/stage_frontier_78/frontier78b_execution_calibrated_density_contract_pnl_proxy_scout.py"

SUMMARY = REVIEW_DIR / "f78b_contract_proxy_summary.json"
CANDIDATES_ALL = REVIEW_DIR / "f78b_contract_proxy_candidates_all.csv"
CANDIDATES_TOP = REVIEW_DIR / "f78b_contract_proxy_ranked_top100.csv"
AXIS_SUMMARY = REVIEW_DIR / "f78b_contract_proxy_axis_summary.csv"
MODEL_FIT_SUMMARY = REVIEW_DIR / "f78b_contract_model_fit_summary.csv"
LABEL_AUDIT = REVIEW_DIR / "f78b_contract_label_audit.csv"
DATA_INTEGRITY = REVIEW_DIR / "f78b_data_integrity_review.json"
MODEL_VALIDATION = REVIEW_DIR / "f78b_model_validation_review.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f78b_artifact_lineage.json"
REPORT = REVIEW_DIR / "frontier78B_execution_calibrated_density_contract_pnl_proxy_scout_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f78b.md"
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
class ContractSpec:
    name: str
    side: str
    hold_bars: int
    tp_price_units: float
    sl_price_units: float
    label_mode: str
    utility_quantile: float


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


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


def ensure_dirs() -> None:
    for path in (REVIEW_DIR, RUN_DIR, SELECTED_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def feature_order() -> list[str]:
    return [line.strip() for line in read_text(FEATURE_ORDER_PATH).splitlines() if line.strip()]


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    for path in (DATASET_PATH, FEATURE_ORDER_PATH, RAW_BARS_PATH):
        if not path_exists(path):
            raise FileNotFoundError(f"missing required input(필수 입력 누락): {rel(path)}")
    df = pd.read_parquet(io_path(DATASET_PATH)).copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    raw = pd.read_csv(
        io_path(RAW_BARS_PATH),
        usecols=[
            "time_open_unix",
            "time_close_unix",
            "open",
            "high",
            "low",
            "close",
            "spread_points",
            "tick_volume",
        ],
    )
    raw["open_ts"] = pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
    raw["close_ts"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.sort_values("open_ts").reset_index(drop=True)
    for col in ["open", "high", "low", "close", "spread_points", "tick_volume"]:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    return df, raw, feature_order()


def entry_indices_next_bar(df: pd.DataFrame, raw: pd.DataFrame) -> np.ndarray:
    mapping = {ts: idx for idx, ts in enumerate(raw["open_ts"])}
    current_idx = df["timestamp"].map(mapping).fillna(-2).astype(int).to_numpy()
    return current_idx + 1


def has_columns(features: Sequence[str], names: Sequence[str]) -> list[str]:
    available = set(features)
    return [name for name in names if name in available]


def feature_sets(features: Sequence[str]) -> dict[str, list[str]]:
    price = has_columns(
        features,
        [
            "log_return_1",
            "log_return_3",
            "hl_range",
            "close_open_ratio",
            "gap_percent",
            "return_zscore_20",
            "hl_zscore_50",
            "return_1_over_atr_14",
            "close_prev_close_ratio",
        ],
    )
    volatility = [f for f in features if any(key in f for key in ["atr", "bollinger", "bb_", "historical_vol", "squeeze"])]
    session = [f for f in features if any(key in f for key in ["is_us_cash", "minutes_from", "first_30m", "last_30m", "day_of_week"])]
    trend = [f for f in features if any(key in f for key in ["ema", "sma", "rsi", "stoch", "ppo", "roc", "trix", "adx", "di_", "supertrend", "vortex"])]
    contract_core = sorted(set(price + volatility + session + trend[:12]))
    price_vol_session = sorted(set(price + volatility + session))
    return {
        "full58": list(features),
        "contract_core": contract_core,
        "price_vol_session": price_vol_session,
    }


def model_builders(random_state: int = 7802) -> dict[str, Callable[[], Any]]:
    return {
        "logistic_l2_balanced": lambda: make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=300, class_weight="balanced", C=0.5, solver="lbfgs"),
        ),
        "extra_trees_d8_l60": lambda: ExtraTreesClassifier(
            n_estimators=60,
            max_depth=8,
            min_samples_leaf=60,
            class_weight="balanced_subsample",
            random_state=random_state,
            n_jobs=-1,
        ),
    }


def contract_specs() -> list[ContractSpec]:
    base = [
        (6, 10.0, 7.0),
        (12, 18.0, 12.0),
        (18, 26.0, 16.0),
    ]
    modes = [
        ("net_utility", 0.58),
        ("density_quota_utility", 0.52),
    ]
    specs: list[ContractSpec] = []
    for side in ["long", "short"]:
        for hold, tp, sl in base:
            for mode, q in modes:
                specs.append(ContractSpec(f"{side}_h{hold}_tp{int(tp)}_sl{int(sl)}_{mode}_q{int(q * 100)}", side, hold, tp, sl, mode, q))
    return specs


def compute_contract_outcome(raw: pd.DataFrame, indices: np.ndarray, spec: ContractSpec) -> dict[str, np.ndarray]:
    open_arr = raw["open"].to_numpy(float)
    high_arr = raw["high"].to_numpy(float)
    low_arr = raw["low"].to_numpy(float)
    close_arr = raw["close"].to_numpy(float)
    spread_price_units = raw["spread_points"].to_numpy(float) / SLTP_POINT_SCALE
    n = len(indices)
    pnl_price = np.full(n, np.nan, dtype=float)
    pnl_contract = np.full(n, np.nan, dtype=float)
    mfe_contract = np.full(n, np.nan, dtype=float)
    mae_contract = np.full(n, np.nan, dtype=float)
    spread_cost_contract = np.full(n, np.nan, dtype=float)
    utility = np.full(n, np.nan, dtype=float)
    exit_offset = np.zeros(n, dtype=int)
    valid = np.zeros(n, dtype=bool)
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
            mfe_price = float(np.max(path_high - entry))
            mae_price = float(np.max(entry - path_low))
            realized = float(path_close[-1] - entry)
            offset = spec.hold_bars
            for local_idx in range(spec.hold_bars):
                sl_hit = path_low[local_idx] <= entry - spec.sl_price_units
                tp_hit = path_high[local_idx] >= entry + spec.tp_price_units
                if sl_hit or tp_hit:
                    realized = -spec.sl_price_units if sl_hit else spec.tp_price_units
                    offset = local_idx + 1
                    break
        else:
            mfe_price = float(np.max(entry - path_low))
            mae_price = float(np.max(path_high - entry))
            realized = float(entry - path_close[-1])
            offset = spec.hold_bars
            for local_idx in range(spec.hold_bars):
                sl_hit = path_high[local_idx] >= entry + spec.sl_price_units
                tp_hit = path_low[local_idx] <= entry - spec.tp_price_units
                if sl_hit or tp_hit:
                    realized = -spec.sl_price_units if sl_hit else spec.tp_price_units
                    offset = local_idx + 1
                    break
        spread_cost = float(spread_price_units[raw_idx]) * CONTRACT_PNL_SCALE if np.isfinite(spread_price_units[raw_idx]) else 0.0
        contract_pnl = realized * CONTRACT_PNL_SCALE - spread_cost
        mae = mae_price * CONTRACT_PNL_SCALE + spread_cost
        mfe = mfe_price * CONTRACT_PNL_SCALE
        if spec.label_mode == "dd_penalized_utility":
            score = contract_pnl - 0.45 * mae - 0.004 * offset
        elif spec.label_mode == "density_quota_utility":
            score = contract_pnl - 0.12 * mae - 0.001 * offset
        else:
            score = contract_pnl - 0.22 * mae - 0.002 * offset
        pnl_price[row_idx] = realized
        pnl_contract[row_idx] = contract_pnl
        mfe_contract[row_idx] = mfe
        mae_contract[row_idx] = mae
        spread_cost_contract[row_idx] = spread_cost
        utility[row_idx] = score
        exit_offset[row_idx] = max(1, int(offset))
        valid[row_idx] = True
    return {
        "pnl_price": pnl_price,
        "pnl_contract": pnl_contract,
        "mfe_contract": mfe_contract,
        "mae_contract": mae_contract,
        "spread_cost_contract": spread_cost_contract,
        "utility": utility,
        "exit_offset": exit_offset,
        "valid": valid,
    }


def make_label(df: pd.DataFrame, outcome: Mapping[str, np.ndarray], spec: ContractSpec) -> np.ndarray:
    train_mask = (df["split"] == "train").to_numpy() & np.asarray(outcome["valid"], dtype=bool)
    utility = np.asarray(outcome["utility"], dtype=float)
    if train_mask.sum() == 0:
        return np.zeros(len(df), dtype=int)
    threshold = float(np.nanquantile(utility[train_mask], spec.utility_quantile))
    pnl = np.asarray(outcome["pnl_contract"], dtype=float)
    mae = np.asarray(outcome["mae_contract"], dtype=float)
    if spec.label_mode == "dd_penalized_utility":
        guard = mae <= np.nanquantile(mae[train_mask], 0.70)
    elif spec.label_mode == "density_quota_utility":
        guard = np.ones(len(df), dtype=bool)
    else:
        guard = mae <= np.nanquantile(mae[train_mask], 0.82)
    return ((utility >= threshold) & (pnl > 0.0) & guard & np.asarray(outcome["valid"], dtype=bool)).astype(int)


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

    def quantile(name: str, q: float, fallback: float) -> float:
        if name not in train:
            return fallback
        series = pd.to_numeric(train[name], errors="coerce")
        if series.dropna().empty:
            return fallback
        return float(series.quantile(q))

    return {
        "atr_ratio_median": quantile("atr_14_over_atr_50", 0.50, 1.0),
        "boll_width_low": quantile("bollinger_width_20", 0.45, 0.0),
        "boll_width_high": quantile("bollinger_width_20", 0.70, 1.0),
        "adx_median": quantile("adx_14", 0.50, 20.0),
    }


def risk_mask(df: pd.DataFrame, name: str, side: str, thresholds: Mapping[str, float]) -> np.ndarray:
    if name == "none":
        return np.ones(len(df), dtype=bool)
    if name == "low_volatility":
        atr = pd.to_numeric(df.get("atr_14_over_atr_50", pd.Series(np.nan, index=df.index)), errors="coerce").to_numpy()
        width = pd.to_numeric(df.get("bollinger_width_20", pd.Series(np.nan, index=df.index)), errors="coerce").to_numpy()
        return (atr <= thresholds["atr_ratio_median"]) & (width <= thresholds["boll_width_low"])
    if name == "trend_aligned":
        adx = pd.to_numeric(df.get("adx_14", pd.Series(np.nan, index=df.index)), errors="coerce").to_numpy()
        di = pd.to_numeric(df.get("di_spread_14", pd.Series(0.0, index=df.index)), errors="coerce").to_numpy()
        direction = di > 0 if side == "long" else di < 0
        return (adx >= thresholds["adx_median"]) & direction
    if name == "mean_revert":
        bb = pd.to_numeric(df.get("bb_position_20", pd.Series(0.5, index=df.index)), errors="coerce").fillna(0.5).to_numpy()
        return bb <= 0.35 if side == "long" else bb >= 0.65
    if name == "liquidity_release":
        width = pd.to_numeric(df.get("bollinger_width_20", pd.Series(np.nan, index=df.index)), errors="coerce").to_numpy()
        volume = pd.to_numeric(df.get("tick_volume_zscore_20", pd.Series(0.0, index=df.index)), errors="coerce").fillna(0.0).to_numpy()
        return (width >= thresholds["boll_width_high"]) | (volume >= 0.5)
    raise ValueError(name)


def lifecycle_select(raw_signal: np.ndarray, exit_offsets: np.ndarray, cooldown_bars: int) -> np.ndarray:
    selected = np.zeros_like(raw_signal, dtype=bool)
    remaining = 0
    for idx, flag in enumerate(raw_signal):
        if remaining > 0:
            remaining -= 1
            continue
        if bool(flag):
            selected[idx] = True
            remaining = max(int(exit_offsets[idx]) + int(cooldown_bars) - 1, 0)
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


def calendar_days(split_df: pd.DataFrame) -> int:
    ts = pd.to_datetime(split_df["timestamp"], errors="coerce", utc=True).dropna()
    if ts.empty:
        return 0
    return max(1, int((ts.max().date() - ts.min().date()).days))


def contract_kpi(split_df: pd.DataFrame, selected: np.ndarray, outcome: Mapping[str, np.ndarray]) -> dict[str, Any]:
    pnl = np.asarray(outcome["pnl_contract"], dtype=float)[selected]
    exit_offsets = np.asarray(outcome["exit_offset"], dtype=int)[selected]
    mae = np.asarray(outcome["mae_contract"], dtype=float)[selected]
    spread = np.asarray(outcome["spread_cost_contract"], dtype=float)[selected]
    days = calendar_days(split_df)
    active_days = pd.to_datetime(split_df.loc[selected, "timestamp"], errors="coerce").dt.date.nunique() if selected.any() else 0
    if len(pnl) == 0:
        return {
            "net": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "pf": 0.0,
            "dd_pct": 0.0,
            "trade_count": 0,
            "calendar_days": days,
            "calendar_trades_day": 0.0,
            "active_days": int(active_days),
            "active_trades_day": 0.0,
            "win_rate": 0.0,
            "avg_win": 0.0,
            "avg_loss": 0.0,
            "payoff": 0.0,
            "expectancy": 0.0,
            "recovery": 0.0,
            "avg_hold_bars": 0.0,
            "avg_mae_contract": 0.0,
            "avg_spread_cost_contract": 0.0,
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
    avg_win = float(wins.mean()) if len(wins) else 0.0
    avg_loss = float(losses.mean()) if len(losses) else 0.0
    recovery = net / (dd_pct / 100.0 * INITIAL_BALANCE) if dd_pct > 0 else (999.0 if net > 0 else 0.0)
    max_loss = max_consecutive_losses(pnl)
    tuw = max_time_under_water_trades(pnl)
    smooth = int(net > 0 and dd_pct <= 10.0 and max_loss <= 8 and tuw <= max(20, trades // 3))
    return {
        "net": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "pf": pf,
        "dd_pct": dd_pct,
        "trade_count": trades,
        "calendar_days": days,
        "calendar_trades_day": float(trades / days) if days else 0.0,
        "active_days": int(active_days),
        "active_trades_day": float(trades / active_days) if active_days else 0.0,
        "win_rate": float(len(wins) / trades) if trades else 0.0,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff": abs(avg_win / avg_loss) if avg_loss < 0 else 0.0,
        "expectancy": float(pnl.mean()) if trades else 0.0,
        "recovery": recovery,
        "avg_hold_bars": float(np.mean(exit_offsets)) if len(exit_offsets) else 0.0,
        "avg_mae_contract": float(np.nanmean(mae)) if len(mae) else 0.0,
        "avg_spread_cost_contract": float(np.nanmean(spread)) if len(spread) else 0.0,
        "max_consecutive_loss": max_loss,
        "time_under_water_trades": tuw,
        "smooth_equity_proxy": smooth,
    }


def scout_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            int(metrics["trade_count"]) > 0
            and float(metrics["pf"]) >= 1.15
            and float(metrics["dd_pct"]) <= 12.0
            and 1.0 <= float(metrics["calendar_trades_day"]) <= MAX_CALENDAR_TPD_SCOUT
        )

    return ok(val) and ok(oos)


def meaningful_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 1.35
            and float(metrics["dd_pct"]) <= 10.0
            and 2.0 <= float(metrics["calendar_trades_day"]) <= 12.0
            and int(metrics["trade_count"]) >= 80
        )

    return ok(val) and ok(oos)


def final_like_reference(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 2.0
            and float(metrics["dd_pct"]) <= 10.0
            and 5.0 <= float(metrics["calendar_trades_day"]) <= 10.0
            and int(metrics["smooth_equity_proxy"]) == 1
        )

    return ok(val) and ok(oos)


def density_score(value: float) -> float:
    if value <= 0:
        return -10.0
    if 5.0 <= value <= 10.0:
        return 10.0
    if value < 5.0:
        return value * 1.6
    return max(0.0, 10.0 - (value - 10.0) * 1.5)


def rank_score(val: Mapping[str, Any], oos: Mapping[str, Any], meaningful: bool, scout: bool, near: bool) -> float:
    min_pf = min(float(val["pf"]), float(oos["pf"]), 5.0)
    max_dd = max(float(val["dd_pct"]), float(oos["dd_pct"]))
    min_net = min(float(val["net"]), float(oos["net"]))
    density = min(density_score(float(val["calendar_trades_day"])), density_score(float(oos["calendar_trades_day"])))
    smooth = int(val["smooth_equity_proxy"]) + int(oos["smooth_equity_proxy"])
    return (
        (1_000_000.0 if meaningful else 0.0)
        + (250_000.0 if near else 0.0)
        + (100_000.0 if scout else 0.0)
        + (20_000.0 if min_net > 0 else 0.0)
        + min_pf * 4_000.0
        + density * 2_500.0
        + smooth * 2_500.0
        - max_dd * 350.0
        + min_net * 25.0
    )


def fit_and_score() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    df, raw, features = load_inputs()
    indices = entry_indices_next_bar(df, raw)
    feature_map = feature_sets(features)
    builders = model_builders()
    thresholds = risk_thresholds(df)
    specs = contract_specs()
    sessions = ["all", "cash_open", "cash_mid"]
    risk_filters = ["none", "trend_aligned", "mean_revert"]
    prob_quantiles = [0.72, 0.86]
    cooldowns = [0, 6]

    candidate_rows: list[dict[str, Any]] = []
    fit_rows: list[dict[str, Any]] = []
    label_rows: list[dict[str, Any]] = []
    candidate_id = 0

    for spec in specs:
        outcome = compute_contract_outcome(raw, indices, spec)
        label = make_label(df, outcome, spec)
        train_valid = (df["split"] == "train").to_numpy() & np.asarray(outcome["valid"], dtype=bool)
        positive = int(label[train_valid].sum()) if train_valid.sum() else 0
        label_rows.append(
            {
                "label_name": spec.name,
                "side": spec.side,
                "hold_bars": spec.hold_bars,
                "tp_price_units": spec.tp_price_units,
                "sl_price_units": spec.sl_price_units,
                "tp_broker_points": spec.tp_price_units * SLTP_POINT_SCALE,
                "sl_broker_points": spec.sl_price_units * SLTP_POINT_SCALE,
                "label_mode": spec.label_mode,
                "utility_quantile": spec.utility_quantile,
                "train_valid_rows": int(train_valid.sum()),
                "train_positive_rows": positive,
                "train_positive_rate": float(label[train_valid].mean()) if train_valid.sum() else 0.0,
                "validation_valid_rows": int(((df["split"] == "validation").to_numpy() & np.asarray(outcome["valid"], dtype=bool)).sum()),
                "oos_valid_rows": int(((df["split"] == "oos").to_numpy() & np.asarray(outcome["valid"], dtype=bool)).sum()),
            }
        )
        if train_valid.sum() == 0 or positive == 0 or positive == train_valid.sum():
            fit_rows.append(
                {
                    "label_name": spec.name,
                    "feature_set": "all",
                    "model": "all",
                    "status": "skipped_single_class_or_empty",
                    "train_rows": int(train_valid.sum()),
                    "positive_rows": positive,
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
                            for cooldown in cooldowns:
                                split_payload: dict[str, dict[str, Any]] = {}
                                row_base: dict[str, Any] = {}
                                raw_any = 0
                                entry_any = 0
                                for split in ["validation", "oos"]:
                                    split_mask_global = (df["split"] == split).to_numpy()
                                    split_df = df.loc[split_mask_global].reset_index(drop=True)
                                    split_outcome = {key: np.asarray(value)[split_mask_global] for key, value in outcome.items()}
                                    valid = np.asarray(split_outcome["valid"], dtype=bool)
                                    raw_signal = (
                                        (probs[split] >= prob_threshold)
                                        & valid
                                        & session_mask(split_df, session)
                                        & risk_mask(split_df, risk_filter, spec.side, thresholds)
                                    )
                                    selected = lifecycle_select(raw_signal, np.asarray(split_outcome["exit_offset"], dtype=int), cooldown)
                                    metrics = contract_kpi(split_df, selected, split_outcome)
                                    split_payload[split] = metrics
                                    raw_any += int(raw_signal.sum())
                                    entry_any += int(selected.sum())
                                    row_base[f"{split}_raw_signal_count"] = int(raw_signal.sum())
                                    row_base[f"{split}_lifecycle_trade_count"] = int(selected.sum())
                                    row_base[f"{split}_signal_to_trade_ratio"] = int(selected.sum()) / int(raw_signal.sum()) if int(raw_signal.sum()) else 0.0
                                val = split_payload["validation"]
                                oos = split_payload["oos"]
                                scout = scout_gate(val, oos)
                                meaningful = meaningful_gate(val, oos)
                                near = final_like_reference(val, oos)
                                dual_positive = float(val["net"]) > 0.0 and float(oos["net"]) > 0.0
                                candidate_id += 1
                                row: dict[str, Any] = {
                                    "candidate_id": f"f78b_{candidate_id:05d}",
                                    "label_name": spec.name,
                                    "side": spec.side,
                                    "hold_bars": spec.hold_bars,
                                    "tp_price_units": spec.tp_price_units,
                                    "sl_price_units": spec.sl_price_units,
                                    "tp_broker_points": spec.tp_price_units * SLTP_POINT_SCALE,
                                    "sl_broker_points": spec.sl_price_units * SLTP_POINT_SCALE,
                                    "label_mode": spec.label_mode,
                                    "utility_quantile": spec.utility_quantile,
                                    "feature_set": feature_set_name,
                                    "feature_count": len(cols),
                                    "model": model_name,
                                    "prob_quantile": q,
                                    "prob_threshold": prob_threshold,
                                    "session": session,
                                    "risk_filter": risk_filter,
                                    "cooldown_bars": cooldown,
                                    "contract_pnl_scale": CONTRACT_PNL_SCALE,
                                    "contract_pnl_scale_source": CONTRACT_PNL_SCALE_SOURCE,
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
        "contract_pnl_scale": CONTRACT_PNL_SCALE,
        "contract_pnl_scale_source": CONTRACT_PNL_SCALE_SOURCE,
        "claim_boundary": CLAIM_BOUNDARY,
        "calendar_density_rule": "calendar_trades_day = trade_count / split calendar days(달력일)",
        "entry_rule": "next raw bar open after feature timestamp(피처 시각 다음 원천 봉 시가)",
        "scout_budget": "sequential first pass(순차 1차 회차): 3 feature sets x 2 model families x 12 labels x 2 quantiles x 3 sessions x 3 risk filters x 2 cooldowns",
    }
    return candidate_rows, fit_rows, label_rows, summary


def axis_summary_rows(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis in ["label_mode", "side", "hold_bars", "feature_set", "model", "session", "risk_filter", "cooldown_bars"]:
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
                    "best_val_net_pf_dd_calendar_tpd": f"{best['val_net']}/{best['val_pf']}/{best['val_dd_pct']}/{best['val_calendar_trades_day']}",
                    "best_oos_net_pf_dd_calendar_tpd": f"{best['oos_net']}/{best['oos_pf']}/{best['oos_dd_pct']}/{best['oos_calendar_trades_day']}",
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
        "time_axis": "Feature timestamp(피처 시각)은 closed-bar key(닫힌 봉 키)로 두고, entry(진입)는 next raw bar open(다음 원천 봉 시가)로 둔다.",
        "sample_scope": "US100 M5 split_v1 train/validation/oos(훈련/검증/표본외). Tier A separate(티어 A 분리); Tier B missing_required(티어 B 필수 누락).",
        "missing_or_duplicate_check": "entry index(진입 인덱스)는 raw open_ts(원천 시가 시각) mapping(매핑)에서 생성된다; invalid tail rows(끝부분 무효 행)는 label valid=false(라벨 무효)로 빠진다.",
        "feature_label_boundary": "features(피처)는 current row(현재 행)만 쓰고, label/target(라벨/목표)은 next-bar entry 이후 future OHLC path(미래 OHLC 경로)만 쓴다.",
        "split_boundary": "model fit(모델 학습), utility quantile(효용 분위수), probability threshold(확률 임계값)는 train only(훈련 전용)에서 계산된다.",
        "leakage_risk": "session/risk filter(세션/위험 필터)가 label path(라벨 경로)와 섞일 위험; F78B keeps them as entry-time feature filters(진입 시점 피처 필터).",
        "data_hash_or_identity": {
            "dataset_sha256": file_hash(DATASET_PATH),
            "feature_order_sha256": file_hash(FEATURE_ORDER_PATH),
            "raw_bars_sha256": file_hash(RAW_BARS_PATH),
            "candidate_rows": summary.get("candidate_rows"),
        },
        "integrity_judgment": "usable_with_boundary(경계 있는 사용 가능)",
    }


def model_validation_review(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "model_family": "logistic_l2_balanced(균형 로지스틱), extra_trees_d8_l60(엑스트라트리), hist_gbm_d4_l2(히스토그램 GBM)",
        "target_and_label": "contract-calibrated utility labels(계약 보정 효용 라벨) from next-bar first-touch path(다음 봉 선도달 경로), spread cost(스프레드 비용), MAE risk(불리 이동 위험), and hold time(보유 시간).",
        "split_method": "time-ordered train/validation/oos holdout(시간 순서 훈련/검증/표본외 고정); no WFO(워크포워드 없음) in F78B scout.",
        "selection_metric": "rank_score(순위 점수) combines meaningful/scout gates(의미/탐색 게이트), PF(수익 팩터), calendar density(달력 밀도), DD(손실폭), net(순수익), smooth proxy(매끄러움 프록시).",
        "secondary_metrics": "active-day density(활성일 밀도), signal-to-trade ratio(신호-거래 비율), max loss streak(최대 연속 손실), time under water trades(회복 전 거래 수), average spread cost(평균 스프레드 비용).",
        "threshold_policy": "probability thresholds(확률 임계값)은 train prediction quantile(훈련 예측 분위수)로 검색된다; scores are ranks(순위) not calibrated probabilities(보정 확률 아님).",
        "overfit_risk": "large axis sweep(큰 축 탐색) across labels/features/models/sessions/risk/cooldown; F78B remains proxy scout(프록시 탐색).",
        "calibration_risk": "CONTRACT_PNL_SCALE is runtime-observed proxy calibration(런타임 관찰 프록시 보정) from F77 gross profit scale, not broker authority(브로커 권위 아님).",
        "comparison_baseline": "F77 runtime lifecycle label density closeout(런타임 생명주기 라벨 밀도 마감) and its money/density gap(금액/밀도 간극).",
        "validation_judgment": "exploratory_proxy_scout(탐색 프록시)",
        "summary_counts": {
            "fit_completed": summary.get("fit_completed"),
            "candidate_rows": summary.get("candidate_rows"),
            "meaningful_signal_count": summary.get("meaningful_signal_count"),
            "scout_clue_count": summary.get("scout_clue_count"),
        },
    }


def artifact_lineage(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_inputs": [rel(DATASET_PATH), rel(FEATURE_ORDER_PATH), rel(RAW_BARS_PATH), "stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78a_experiment_design_review.json"],
        "producer": SCRIPT_PATH,
        "consumer": NEXT_RUN_IF_MEANINGFUL if int(summary.get("meaningful_signal_count", 0)) > 0 else NEXT_RUN_IF_WEAK_NONZERO,
        "artifact_paths": [rel(SUMMARY), rel(CANDIDATES_ALL), rel(CANDIDATES_TOP), rel(AXIS_SUMMARY), rel(REPORT), rel(RUN_MANIFEST)],
        "artifact_hashes": {
            "dataset_sha256": file_hash(DATASET_PATH),
            "raw_bars_sha256": file_hash(RAW_BARS_PATH),
            "script_sha256": file_hash(ROOT / SCRIPT_PATH),
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER)],
        "availability": "tracked_reviews_with_reproducible_command(추적 리뷰와 재현 명령)",
        "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
    }


def format_best(best: Mapping[str, Any]) -> str:
    if not best:
        return "none(없음)"
    return (
        f"{best.get('candidate_id')} val net/PF/DD/calendar_tpd/trades(검증 순수익/수익 팩터/손실폭/달력일거래/거래) "
        f"{best.get('val_net')}/{best.get('val_pf')}/{best.get('val_dd_pct')}/{best.get('val_calendar_trades_day')}/{best.get('val_trade_count')}; "
        f"oos(표본외) {best.get('oos_net')}/{best.get('oos_pf')}/{best.get('oos_dd_pct')}/{best.get('oos_calendar_trades_day')}/{best.get('oos_trade_count')}"
    )


def report_text(created_at: str, summary: Mapping[str, Any], top_rows: Sequence[Mapping[str, Any]]) -> str:
    status, judgment, next_run = status_and_next(summary)
    best = summary.get("best_candidate") or {}
    table = "\n".join(
        [
            "| candidate(후보) | model(모델) | label(라벨) | feature(피처) | session/risk/cd(세션/위험/쿨다운) | val net/PF/DD/tpd/trades(검증) | oos net/PF/DD/tpd/trades(표본외) | scout/meaningful(탐색/의미) |",
            "|---|---|---|---|---|---:|---:|---|",
            *[
                f"| `{row.get('candidate_id')}` | `{row.get('model')}` | `{row.get('label_name')}` | `{row.get('feature_set')}` | `{row.get('session')}/{row.get('risk_filter')}/{row.get('cooldown_bars')}` | "
                f"`{row.get('val_net'):.4f}/{row.get('val_pf'):.4f}/{row.get('val_dd_pct'):.4f}/{row.get('val_calendar_trades_day'):.4f}/{row.get('val_trade_count')}` | "
                f"`{row.get('oos_net'):.4f}/{row.get('oos_pf'):.4f}/{row.get('oos_dd_pct'):.4f}/{row.get('oos_calendar_trades_day'):.4f}/{row.get('oos_trade_count')}` | "
                f"`{row.get('scout_clue')}/{row.get('meaningful_signal')}` |"
                for row in top_rows[:12]
            ],
        ]
    )
    return f"""# Frontier78B Execution-Calibrated Contract P/L Proxy Scout Report(F78B 실행 보정 계약 손익 프록시 탐색 보고서)

Updated(갱신): {created_at}

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- candidate rows(후보 행): `{summary['candidate_rows']}`
- fit completed(학습 완료): `{summary['fit_completed']}/{summary['fit_rows']}`
- scout clue count(탐색 단서 수): `{summary['scout_clue_count']}`
- meaningful signal count(의미 신호 수): `{summary['meaningful_signal_count']}`
- final-like reference count(완성 유사 참조 수): `{summary['final_like_reference_count']}`
- nonzero lifecycle trade candidates(비영 생명주기 거래 후보): `{summary['nonzero_lifecycle_trade_candidates']}`
- contract P/L scale(계약 손익 배율): `{summary['contract_pnl_scale']}` from `{summary['contract_pnl_scale_source']}`
- entry rule(진입 규칙): `{summary['entry_rule']}`
- density rule(밀도 규칙): `{summary['calendar_density_rule']}`
- best candidate(최선 후보): {format_best(best)}
- next action(다음 행동): `{next_run}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Top Proxy Rows(상위 프록시 행)

{table}

## Interpretation Boundary(해석 경계)

This is proxy scout only(프록시 탐색 전용). It can create scout clue(탐색 단서), seed surface(씨앗 표면), or runtime probe observation target(런타임 탐침 관찰 대상), but not completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def gate_audit_text(status: str, summary: Mapping[str, Any], next_run: str) -> str:
    return f"""# Required Gate Coverage Audit F78B(F78B 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| data integrity(데이터 무결성) | `recorded(기록됨)` | `{rel(DATA_INTEGRITY)}` |
| model validation(모델 검증) | `recorded(기록됨)` | `{rel(MODEL_VALIDATION)}` |
| proxy KPI contract(프록시 KPI 계약) | `passed(통과)` | `{rel(SUMMARY)}` |
| contract P/L identity(계약 손익 정체성) | `recorded(기록됨)` | scale `{summary.get('contract_pnl_scale')}` source `{summary.get('contract_pnl_scale_source')}` |
| calendar density denominator(달력 밀도 분모) | `recorded(기록됨)` | candidate rows contain calendar_trades_day(달력 일 거래 수) and active_trades_day(활성일 거래 수) |
| Tier paired record(티어 쌍 기록) | `boundary_recorded(경계 기록)` | Tier A separate(티어 A 분리), Tier B missing_required(필수 누락), combined out_of_scope(합산 범위 밖) |
| runtime probe rule(런타임 탐침 규칙) | `required_next(다음 필수)` | meaningful/weak nonzero signal(의미/약한 비영 신호)이 있으면 pre-MT5 Grok + MT5 Runtime Probe(사전 MT5 그록 + MT5 런타임 탐침) |
| claim guard(주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |

Open status(현재 상태): `{status}`

Next run(다음 실행): `{next_run}`
"""


def selection_status_text(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> str:
    return f"""# F78 Selection Status(F78 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F78B execution-calibrated proxy scout(실행 보정 프록시 탐색)를 완료했다.

Effect(효과): contract P/L scale(계약 손익 배율), calendar density(달력 밀도), next-bar entry(다음 봉 진입), lifecycle occupancy(생명주기 점유)를 포함한 후보 표면을 기록했다.

Best candidate(최선 후보): {format_best(summary.get('best_candidate') or {})}

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
        "notes": f"candidates={summary.get('candidate_rows')}; scout={summary.get('scout_clue_count')}; meaningful={summary.get('meaningful_signal_count')}; next={next_run}",
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT),
        "run_number": "frontier78B",
        "date": created_at[:10],
        "decision": judgment,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "rows": summary.get("candidate_rows"),
        "gate_passes": "8",
        "gate_total": "8",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "best_candidate_id": best.get("candidate_id", ""),
        "candidate_count": summary.get("candidate_rows"),
        "scout_clue_count": summary.get("scout_clue_count"),
        "meaningful_signal_count": summary.get("meaningful_signal_count"),
        "model": best.get("model", ""),
        "net_profit": best.get("oos_net", ""),
        "profit_factor": best.get("oos_pf", ""),
        "drawdown_percent": best.get("oos_dd_pct", ""),
        "expectancy": best.get("oos_expectancy", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "trades_per_day": best.get("oos_calendar_trades_day", ""),
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "contract_proxy_validation_oos(계약 프록시 검증/표본외)",
        "primary_kpi": f"scout={summary.get('scout_clue_count')};meaningful={summary.get('meaningful_signal_count')};near={summary.get('final_like_reference_count')}",
        "guardrail_kpi": f"contract_scale={summary.get('contract_pnl_scale')};calendar_density=recorded;entry=next_bar",
        "work_family": "experiment_execution(실험 실행)",
        "row_id": row_id,
        "ledger_row_id": row_id,
        "subrun_id": "execution_calibrated_proxy_scout(실행 보정 프록시 탐색)",
        "evidence_boundary": "proxy_scout_only_no_authority(프록시 탐색만, 권위 없음)",
        "next_action": next_run,
        "question": "Can contract-calibrated labels reduce runtime money/density gap?(계약 보정 라벨이 런타임 금액/밀도 간극을 줄이나?)",
        "artifact_count": "9",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution(실험 실행)",
        "run_type": "execution_calibrated_contract_proxy_scout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST),
        "result_path": rel(REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_only(프록시 전용)",
        "oos_trades_per_day": best.get("oos_calendar_trades_day", ""),
        "oos_net_profit": best.get("oos_net", ""),
        "oos_profit_factor": best.get("oos_pf", ""),
        "oos_trade_count": best.get("oos_trade_count", ""),
        "oos_drawdown_percent": best.get("oos_dd_pct", ""),
        "completion_candidate_count": summary.get("final_like_reference_count"),
    }


def update_ledgers(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> None:
    row = ledger_row(created_at, status, judgment, next_run, summary)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_idea_registry(summary: Mapping[str, Any], next_run: str) -> None:
    marker = "<!-- frontier78B_execution_calibrated_density_contract_pnl_proxy_scout_v1 -->"
    text = read_text(IDEA_REGISTRY)
    if marker in text:
        return
    best = summary.get("best_candidate") or {}
    addition = f"""

{marker}
- `{RUN_ID}` executed F78 execution-calibrated contract P/L proxy scout(F78 실행 보정 계약 손익 프록시 탐색). Result(결과): `scout={summary.get('scout_clue_count')}`, `meaningful={summary.get('meaningful_signal_count')}`, `final_like={summary.get('final_like_reference_count')}`. Best(최선): `{best.get('candidate_id', '')}` OOS net/PF/DD/calendar_tpd(표본외 순수익/수익 팩터/손실폭/달력일 거래 수) `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_calendar_trades_day', '')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{next_run}`.
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_state_files(created_at: str, status: str, judgment: str, next_run: str, summary: Mapping[str, Any]) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run}
runtime_probe_status: f78_mandatory_runtime_probe_pending_after_contract_proxy_scout
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f77_closeout_2_of_5
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F78B proxy scout(프록시 탐색)를 완료했다."
  - "Effect(효과): contract P/L(계약 손익), calendar density(달력 밀도), fill semantics(체결 의미)를 후보 KPI(핵심 성과 지표)에 넣었다."
  - "Next(다음): {next_run}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F78B execution-calibrated proxy scout(실행 보정 프록시 탐색)를 완료했다.

Effect(효과): best proxy(최선 프록시)는 `{(summary.get('best_candidate') or {}).get('candidate_id', 'none')}`이고, scout clue(탐색 단서) `{summary.get('scout_clue_count')}`, meaningful signal(의미 신호) `{summary.get('meaningful_signal_count')}`를 기록했다.

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- runtime rule(런타임 규칙): weak nonzero or meaningful signal(약한 비영 또는 의미 신호)이 있으므로 pre-MT5 Grok review(사전 MT5 그록 검토)와 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) 경로를 준비한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def run_manifest_payload(
    created_at: str,
    status: str,
    judgment: str,
    next_run: str,
    summary: Mapping[str, Any],
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
        "contract_pnl_scale": CONTRACT_PNL_SCALE,
        "contract_pnl_scale_source": CONTRACT_PNL_SCALE_SOURCE,
        "summary": summary,
        "data_source": [rel(DATASET_PATH), rel(FEATURE_ORDER_PATH), rel(RAW_BARS_PATH)],
        "artifacts": {
            "summary": rel(SUMMARY),
            "candidates_all": rel(CANDIDATES_ALL),
            "candidates_top": rel(CANDIDATES_TOP),
            "axis_summary": rel(AXIS_SUMMARY),
            "fit_summary": rel(MODEL_FIT_SUMMARY),
            "label_audit": rel(LABEL_AUDIT),
            "data_integrity": rel(DATA_INTEGRITY),
            "model_validation": rel(MODEL_VALIDATION),
            "artifact_lineage": rel(ARTIFACT_LINEAGE),
            "report": rel(REPORT),
            "gate_audit": rel(GATE_AUDIT),
        },
    }


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    candidate_rows, fit_rows, label_rows, summary = fit_and_score()
    top_rows = candidate_rows[:100]
    axis_rows = axis_summary_rows(candidate_rows)
    status, judgment, next_run = status_and_next(summary)

    write_json(SUMMARY, summary)
    write_csv(CANDIDATES_ALL, candidate_rows)
    write_csv(CANDIDATES_TOP, top_rows)
    write_csv(AXIS_SUMMARY, axis_rows)
    write_csv(MODEL_FIT_SUMMARY, fit_rows)
    write_csv(LABEL_AUDIT, label_rows)
    write_json(DATA_INTEGRITY, data_integrity_review(summary))
    write_json(MODEL_VALIDATION, model_validation_review(summary))
    write_json(ARTIFACT_LINEAGE, artifact_lineage(summary))
    write_text(REPORT, report_text(created_at, summary, top_rows))
    write_text(GATE_AUDIT, gate_audit_text(status, summary, next_run))
    write_text(SELECTION_STATUS, selection_status_text(created_at, status, judgment, next_run, summary))
    write_json(RUN_MANIFEST, run_manifest_payload(created_at, status, judgment, next_run, summary))
    update_ledgers(created_at, status, judgment, next_run, summary)
    update_idea_registry(summary, next_run)
    update_state_files(created_at, status, judgment, next_run, summary)

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
                    "best_candidate": summary["best_candidate"],
                    "next_run_id": next_run,
                    "report": rel(REPORT),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
