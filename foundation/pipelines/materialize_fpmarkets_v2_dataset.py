from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


DATASET_ID = "dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01"
WINDOW_START_UTC = pd.Timestamp("2022-08-01T00:00:00Z")
WINDOW_END_UTC = pd.Timestamp("2026-04-13T23:55:00Z")
PRACTICAL_MODELING_START_UTC = pd.Timestamp("2022-09-01T00:00:00Z")
WARMUP_BARS = 300
FEATURE_CONTRACT_VERSION = "docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16"
PARSER_CONTRACT_VERSION = "docs/contracts/python_feature_parser_spec_fpmarkets_v2.md@2026-04-24"
TIME_AXIS_POLICY_VERSION = "docs/contracts/time_axis_policy_fpmarkets_v2.md@2026-04-24"
RAW_TIME_AXIS_POLICY = "raw_broker_clock_bar_close_key_not_direct_utc"
SESSION_TIME_POLICY_STATUS = "unclosed_pending_timestamp_event_utc_or_broker_session_calendar"
WEIGHTS_VERSION = "foundation/config/top3_monthly_weights_fpmarkets_v2.csv@2026-04-16 (placeholder_equal_weight)"
PARSER_VERSION = "fpmarkets_v2_stage01_materializer_v1"
DEFAULT_WEIGHTS_PATH = Path("foundation/config/top3_monthly_weights_fpmarkets_v2.csv")

FEATURE_ORDER = [
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
    "close_ema20_ratio",
    "close_ema50_ratio",
    "ema9_ema20_diff",
    "ema20_ema50_diff",
    "ema50_ema200_diff",
    "ema20_ema50_spread_zscore_50",
    "sma50_sma200_ratio",
    "rsi_14",
    "rsi_50",
    "rsi_14_slope_3",
    "rsi_14_minus_50",
    "stoch_kd_diff",
    "stochrsi_kd_diff",
    "ppo_hist_12_26_9",
    "roc_12",
    "trix_15",
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "bb_position_20",
    "bb_squeeze",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "supertrend_10_3",
    "vortex_indicator",
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "us10yr_zscore_20",
    "usdx_change_1",
    "usdx_zscore_20",
    "nvda_xnas_log_return_1",
    "aapl_xnas_log_return_1",
    "msft_xnas_log_return_1",
    "amzn_xnas_log_return_1",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
]

EXPECTED_FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

INVALID_REASON_ORDER = [
    "warmup_incomplete",
    "main_symbol_missing",
    "external_alignment_missing",
    "session_semantics_missing",
    "numeric_invalid",
    "weights_unavailable",
    "contract_version_mismatch",
]


@dataclass(frozen=True)
class SymbolBinding:
    contract_symbol: str
    broker_symbol: str


SYMBOL_BINDINGS: tuple[SymbolBinding, ...] = (
    SymbolBinding("US100", "US100"),
    SymbolBinding("VIX", "VIX"),
    SymbolBinding("US10YR", "US10YR"),
    SymbolBinding("USDX", "USDX"),
    SymbolBinding("NVDA", "NVDA.xnas"),
    SymbolBinding("AAPL", "AAPL.xnas"),
    SymbolBinding("MSFT", "MSFT.xnas"),
    SymbolBinding("AMZN", "AMZN.xnas"),
    SymbolBinding("AMD", "AMD.xnas"),
    SymbolBinding("GOOGL.xnas", "GOOGL.xnas"),
    SymbolBinding("META", "META.xnas"),
    SymbolBinding("TSLA", "TSLA.xnas"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize the first FPMarkets v2 Stage 01 dataset.")
    parser.add_argument(
        "--raw-root",
        default="data/raw/mt5_bars/m5",
        help="Repo-relative root containing raw M5 MT5 bar exports.",
    )
    parser.add_argument(
        "--output-root",
        default=f"data/processed/datasets/{DATASET_ID}",
        help="Repo-relative output root for the processed dataset.",
    )
    return parser.parse_args()


def feature_order_hash() -> str:
    payload = "\n".join(FEATURE_ORDER).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_raw_symbol(raw_root: Path, binding: SymbolBinding) -> pd.DataFrame:
    symbol_dir = raw_root / binding.contract_symbol
    csv_candidates = sorted(symbol_dir.glob("*.csv"))
    if len(csv_candidates) != 1:
        raise RuntimeError(f"Expected exactly one raw CSV under {symbol_dir}, found {len(csv_candidates)}")
    csv_path = csv_candidates[0]
    frame = pd.read_csv(csv_path)
    required_columns = {"time_open_unix", "time_close_unix", "open", "high", "low", "close"}
    missing = required_columns.difference(frame.columns)
    if missing:
        raise RuntimeError(f"Raw CSV {csv_path} is missing columns: {sorted(missing)}")
    frame["timestamp"] = pd.to_datetime(frame["time_close_unix"], unit="s", utc=True)
    frame["timestamp_policy"] = RAW_TIME_AXIS_POLICY
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    frame = frame.loc[(frame["timestamp"] >= WINDOW_START_UTC) & (frame["timestamp"] <= WINDOW_END_UTC)].copy()
    if frame["timestamp"].duplicated().any():
        raise RuntimeError(f"Duplicate timestamps detected in {csv_path}")
    if not frame["timestamp"].is_monotonic_increasing:
        raise RuntimeError(f"Timestamps are not monotonic in {csv_path}")
    frame["contract_symbol"] = binding.contract_symbol
    frame["broker_symbol"] = binding.broker_symbol
    frame["source_csv_path"] = str(csv_path.as_posix())
    return frame


def load_source_identity(raw_root: Path, binding: SymbolBinding) -> dict[str, object]:
    symbol_dir = raw_root / binding.contract_symbol
    csv_path = next(symbol_dir.glob("*.csv"))
    manifest_path = next(symbol_dir.glob("*.manifest.json"))
    csv_stat = csv_path.stat()
    manifest_stat = manifest_path.stat()
    return {
        "contract_symbol": binding.contract_symbol,
        "broker_symbol": binding.broker_symbol,
        "csv_path": str(csv_path.as_posix()),
        "csv_size": csv_stat.st_size,
        "csv_modified_utc": pd.Timestamp(csv_stat.st_mtime, unit="s", tz="UTC").isoformat(),
        "csv_sha256": sha256_file(csv_path),
        "manifest_path": str(manifest_path.as_posix()),
        "manifest_size": manifest_stat.st_size,
        "manifest_modified_utc": pd.Timestamp(manifest_stat.st_mtime, unit="s", tz="UTC").isoformat(),
        "manifest_sha256": sha256_file(manifest_path),
    }


def sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=window).mean()


def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False, min_periods=span).mean()


def wilder_smooth(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()


def rolling_zscore(series: pd.Series, window: int) -> pd.Series:
    rolling_mean = series.rolling(window=window, min_periods=window).mean()
    rolling_std = series.rolling(window=window, min_periods=window).std(ddof=0)
    zscore = (series - rolling_mean) / rolling_std
    zero_std_mask = rolling_std.eq(0) & rolling_mean.notna()
    zscore = zscore.mask(zero_std_mask, 0.0)
    return zscore


def compute_rsi(close: pd.Series, period: int) -> pd.Series:
    delta = close.diff()
    gains = delta.clip(lower=0.0)
    losses = (-delta).clip(lower=0.0)
    avg_gain = wilder_smooth(gains, period)
    avg_loss = wilder_smooth(losses, period)
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    rsi = rsi.mask(avg_loss.eq(0) & avg_gain.eq(0), 50.0)
    return rsi


def compute_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return wilder_smooth(tr, period)


def compute_stochastic(high: pd.Series, low: pd.Series, close: pd.Series) -> tuple[pd.Series, pd.Series]:
    lowest_low = low.rolling(window=14, min_periods=14).min()
    highest_high = high.rolling(window=14, min_periods=14).max()
    denom = highest_high - lowest_low
    raw_k = 100.0 * (close - lowest_low) / denom
    raw_k = raw_k.mask(denom.eq(0))
    k = sma(raw_k, 3)
    d = sma(k, 3)
    return k, d


def compute_stochrsi(close: pd.Series) -> tuple[pd.Series, pd.Series]:
    rsi14 = compute_rsi(close, 14)
    rolling_min = rsi14.rolling(window=14, min_periods=14).min()
    rolling_max = rsi14.rolling(window=14, min_periods=14).max()
    denom = rolling_max - rolling_min
    raw = 100.0 * (rsi14 - rolling_min) / denom
    raw = raw.mask(denom.eq(0))
    k = sma(raw, 3)
    d = sma(k, 3)
    return k, d


def compute_ppo_hist(close: pd.Series) -> pd.Series:
    ema12 = ema(close, 12)
    ema26 = ema(close, 26)
    ppo = 100.0 * (ema12 - ema26) / ema26
    signal = ema(ppo, 9)
    return ppo - signal


def compute_trix(close: pd.Series) -> pd.Series:
    ema1 = ema(close, 15)
    ema2 = ema(ema1, 15)
    ema3 = ema(ema2, 15)
    return ema3 / ema3.shift(1) - 1.0


def compute_adx(high: pd.Series, low: pd.Series, close: pd.Series, period: int) -> tuple[pd.Series, pd.Series, pd.Series]:
    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = pd.Series(np.where((up_move > down_move) & (up_move > 0), up_move, 0.0), index=high.index)
    minus_dm = pd.Series(np.where((down_move > up_move) & (down_move > 0), down_move, 0.0), index=high.index)
    atr = compute_atr(high, low, close, period)
    plus_di = 100.0 * wilder_smooth(plus_dm, period) / atr
    minus_di = 100.0 * wilder_smooth(minus_dm, period) / atr
    dx = 100.0 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    adx = wilder_smooth(dx, period)
    return adx, plus_di, minus_di


def compute_supertrend_state(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 10, multiplier: float = 3.0) -> pd.Series:
    atr = compute_atr(high, low, close, period)
    hl2 = (high + low) / 2.0
    basic_upper = hl2 + multiplier * atr
    basic_lower = hl2 - multiplier * atr
    final_upper = basic_upper.copy()
    final_lower = basic_lower.copy()
    state = pd.Series(np.nan, index=close.index, dtype="float64")
    for idx in range(1, len(close)):
        if np.isnan(atr.iloc[idx]):
            continue
        prev_idx = close.index[idx - 1]
        cur_idx = close.index[idx]
        if (
            basic_upper.iloc[idx] < final_upper.iloc[idx - 1]
            or close.iloc[idx - 1] > final_upper.iloc[idx - 1]
        ):
            final_upper.iloc[idx] = basic_upper.iloc[idx]
        else:
            final_upper.iloc[idx] = final_upper.iloc[idx - 1]

        if (
            basic_lower.iloc[idx] > final_lower.iloc[idx - 1]
            or close.iloc[idx - 1] < final_lower.iloc[idx - 1]
        ):
            final_lower.iloc[idx] = basic_lower.iloc[idx]
        else:
            final_lower.iloc[idx] = final_lower.iloc[idx - 1]

        prev_state = state.loc[prev_idx]
        if np.isnan(prev_state):
            prev_state = 1.0 if close.iloc[idx] >= final_lower.iloc[idx] else -1.0
        if prev_state == 1.0:
            state.loc[cur_idx] = -1.0 if close.iloc[idx] < final_lower.iloc[idx] else 1.0
        else:
            state.loc[cur_idx] = 1.0 if close.iloc[idx] > final_upper.iloc[idx] else -1.0
    return state


def compute_vortex(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    prev_low = low.shift(1)
    prev_high = high.shift(1)
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    vm_plus = (high - prev_low).abs()
    vm_minus = (low - prev_high).abs()
    tr_sum = tr.rolling(window=period, min_periods=period).sum()
    vi_plus = vm_plus.rolling(window=period, min_periods=period).sum() / tr_sum
    vi_minus = vm_minus.rolling(window=period, min_periods=period).sum() / tr_sum
    return vi_plus - vi_minus


def compute_session_features(frame: pd.DataFrame) -> dict[str, pd.Series]:
    session_timestamp = frame["timestamp_event_utc"] if "timestamp_event_utc" in frame.columns else frame["timestamp"]
    timestamp_ny = session_timestamp.dt.tz_convert("America/New_York")
    close_time = timestamp_ny.dt.time
    ny_date = timestamp_ny.dt.date
    session_midnight = timestamp_ny.dt.normalize()
    is_us_cash_open = (
        ((timestamp_ny.dt.hour > 9) | ((timestamp_ny.dt.hour == 9) & (timestamp_ny.dt.minute >= 35)))
        & ((timestamp_ny.dt.hour < 16) | ((timestamp_ny.dt.hour == 16) & (timestamp_ny.dt.minute == 0)))
    ).astype(float)

    session_open_ts = session_midnight + pd.Timedelta(hours=9, minutes=30)
    minutes_from_cash_open = (timestamp_ny - session_open_ts).dt.total_seconds() / 60.0
    is_first_30m_after_open = ((minutes_from_cash_open > 0) & (minutes_from_cash_open <= 30)).astype(float)

    session_close_ts = session_midnight + pd.Timedelta(hours=16)
    minutes_to_cash_close = (session_close_ts - timestamp_ny).dt.total_seconds() / 60.0
    is_last_30m_before_cash_close = (
        (minutes_to_cash_close >= 0) & (minutes_to_cash_close <= 25)
    ).astype(float)

    cash_open_mask = (timestamp_ny.dt.hour == 9) & (timestamp_ny.dt.minute == 35)
    cash_close_mask = (timestamp_ny.dt.hour == 16) & (timestamp_ny.dt.minute == 0)

    cash_open_today = frame["open"].where(cash_open_mask).groupby(ny_date).transform("first")
    cash_close_by_date = frame.loc[cash_close_mask, ["close"]].copy()
    cash_close_by_date["ny_date"] = ny_date.loc[cash_close_mask].values
    cash_close_prev_lookup = cash_close_by_date.groupby("ny_date")["close"].last().shift(1)
    cash_close_prev_session = pd.Series(ny_date).map(cash_close_prev_lookup)
    overnight_return = cash_open_today / cash_close_prev_session - 1.0
    overnight_return = overnight_return.groupby(ny_date).ffill()

    return {
        "timestamp_ny": timestamp_ny,
        "is_us_cash_open": is_us_cash_open,
        "minutes_from_cash_open": minutes_from_cash_open,
        "is_first_30m_after_open": is_first_30m_after_open,
        "is_last_30m_before_cash_close": is_last_30m_before_cash_close,
        "overnight_return": overnight_return,
    }


def load_weights(weights_path: Path | None = None) -> pd.DataFrame:
    source_path = DEFAULT_WEIGHTS_PATH if weights_path is None else Path(weights_path)
    weights = pd.read_csv(source_path)
    weights["month"] = weights["month"].astype(str)
    return weights


def merge_exact_timestamp_presence(
    base: pd.DataFrame,
    source: pd.DataFrame,
    *,
    match_column: str,
) -> pd.DataFrame:
    presence = source[["timestamp"]].copy()
    presence[match_column] = True
    merged = base.merge(presence, on="timestamp", how="left")
    merged[match_column] = merged[match_column].eq(True)
    return merged


def build_proxy_feature_source(source: pd.DataFrame, prefix: str) -> pd.DataFrame:
    prepared = source[["timestamp", "close"]].copy()
    prepared[f"{prefix}_change_1"] = prepared["close"] / prepared["close"].shift(1) - 1.0
    prepared[f"{prefix}_zscore_20"] = rolling_zscore(prepared["close"], 20)
    return prepared.rename(columns={"close": f"{prefix}_close"})


def attach_external_series(
    base: pd.DataFrame,
    external_frames: dict[str, pd.DataFrame],
    *,
    weights_path: Path | None = None,
) -> tuple[pd.DataFrame, dict[str, int], list[str]]:
    merged = base.copy()
    alignment_missing_counts: dict[str, int] = {}
    exact_match_columns: list[str] = []

    proxy_configs = {
        "VIX": ("vix", external_frames["VIX"]),
        "US10YR": ("us10yr", external_frames["US10YR"]),
        "USDX": ("usdx", external_frames["USDX"]),
    }
    for contract_symbol, (prefix, source) in proxy_configs.items():
        match_column = f"__exact_match__{prefix}"
        exact_match_columns.append(match_column)
        merged = merge_exact_timestamp_presence(merged, source, match_column=match_column)
        source_view = build_proxy_feature_source(source, prefix)
        merged = merged.merge(source_view, on="timestamp", how="left")
        alignment_missing_counts[contract_symbol] = int((~merged[match_column]).sum())

    stock_return_symbols = {
        "NVDA": "nvda_xnas_log_return_1",
        "AAPL": "aapl_xnas_log_return_1",
        "MSFT": "msft_xnas_log_return_1",
        "AMZN": "amzn_xnas_log_return_1",
    }
    for contract_symbol, feature_name in stock_return_symbols.items():
        source = external_frames[contract_symbol].copy()
        token = contract_symbol.lower().replace(".", "_")
        match_column = f"__exact_match__{token}"
        exact_match_columns.append(match_column)
        merged = merge_exact_timestamp_presence(merged, source, match_column=match_column)
        source[feature_name] = np.log(source["close"] / source["close"].shift(1))
        source_view = source[["timestamp", feature_name]]
        merged = merged.merge(source_view, on="timestamp", how="left")
        alignment_missing_counts[contract_symbol] = int((~merged[match_column]).sum())

    basket_symbols = ["AAPL", "AMZN", "AMD", "GOOGL.xnas", "META", "MSFT", "NVDA", "TSLA"]
    basket_return_1_cols: list[str] = []
    basket_return_5_cols: list[str] = []
    for contract_symbol in basket_symbols:
        source = external_frames[contract_symbol].copy()
        token = contract_symbol.lower().replace(".", "_")
        match_column = f"__exact_match__{token}"
        if match_column not in exact_match_columns:
            exact_match_columns.append(match_column)
            merged = merge_exact_timestamp_presence(merged, source, match_column=match_column)
        return_1_col = f"{token}_simple_return_1"
        return_5_col = f"{token}_simple_return_5"
        source[return_1_col] = source["close"] / source["close"].shift(1) - 1.0
        source[return_5_col] = source["close"] / source["close"].shift(5) - 1.0
        source_view = source[["timestamp", return_1_col, return_5_col]]
        merged = merged.merge(source_view, on="timestamp", how="left")
        basket_return_1_cols.append(return_1_col)
        basket_return_5_cols.append(return_5_col)
        alignment_missing_counts.setdefault(contract_symbol, int((~merged[match_column]).sum()))

    merged["mega8_equal_return_1"] = merged[basket_return_1_cols].mean(axis=1)
    merged["mega8_pos_breadth_1"] = (merged[basket_return_1_cols] > 0).mean(axis=1)
    merged["mega8_dispersion_5"] = merged[basket_return_5_cols].std(axis=1, ddof=0)

    weights = load_weights(weights_path)
    merged["month"] = merged["timestamp"].dt.strftime("%Y-%m")
    merged = merged.merge(weights, on="month", how="left")
    merged["top3_weighted_return_1"] = (
        merged["msft_xnas_weight"] * merged["msft_simple_return_1"]
        + merged["nvda_xnas_weight"] * merged["nvda_simple_return_1"]
        + merged["aapl_xnas_weight"] * merged["aapl_simple_return_1"]
    )

    merged["us100_simple_return_1"] = merged["close"] / merged["close"].shift(1) - 1.0
    merged["us100_minus_mega8_equal_return_1"] = merged["us100_simple_return_1"] - merged["mega8_equal_return_1"]
    merged["us100_minus_top3_weighted_return_1"] = merged["us100_simple_return_1"] - merged["top3_weighted_return_1"]

    return merged, alignment_missing_counts, exact_match_columns


def compute_main_features(base: pd.DataFrame) -> pd.DataFrame:
    frame = base.copy()
    close = frame["close"]
    high = frame["high"]
    low = frame["low"]
    open_ = frame["open"]

    frame["log_return_1"] = np.log(close / close.shift(1))
    frame["log_return_3"] = np.log(close / close.shift(3))
    frame["hl_range"] = (high - low) / close
    frame["close_open_ratio"] = close / open_
    frame["gap_percent"] = open_ / close.shift(1) - 1.0
    frame["close_prev_close_ratio"] = close / close.shift(1)
    frame["return_zscore_20"] = rolling_zscore(frame["log_return_1"], 20)
    frame["hl_zscore_50"] = rolling_zscore(frame["hl_range"], 50)

    atr_14 = compute_atr(high, low, close, 14)
    atr_20 = compute_atr(high, low, close, 20)
    atr_50 = compute_atr(high, low, close, 50)
    frame["atr_14"] = atr_14
    frame["atr_50"] = atr_50
    frame["return_1_over_atr_14"] = (close / close.shift(1) - 1.0) / (atr_14 / close)

    ema9 = ema(close, 9)
    ema20 = ema(close, 20)
    ema50 = ema(close, 50)
    ema200 = ema(close, 200)
    sma50 = sma(close, 50)
    sma200 = sma(close, 200)
    frame["close_ema20_ratio"] = close / ema20
    frame["close_ema50_ratio"] = close / ema50
    frame["ema9_ema20_diff"] = ema9 - ema20
    frame["ema20_ema50_diff"] = ema20 - ema50
    frame["ema50_ema200_diff"] = ema50 - ema200
    frame["ema20_ema50_spread_zscore_50"] = rolling_zscore(frame["ema20_ema50_diff"], 50)
    frame["sma50_sma200_ratio"] = sma50 / sma200

    rsi14 = compute_rsi(close, 14)
    rsi50 = compute_rsi(close, 50)
    frame["rsi_14"] = rsi14
    frame["rsi_50"] = rsi50
    frame["rsi_14_slope_3"] = (rsi14 - rsi14.shift(3)) / 3.0
    frame["rsi_14_minus_50"] = rsi14 - 50.0

    stoch_k, stoch_d = compute_stochastic(high, low, close)
    stochrsi_k, stochrsi_d = compute_stochrsi(close)
    frame["stoch_kd_diff"] = stoch_k - stoch_d
    frame["stochrsi_kd_diff"] = stochrsi_k - stochrsi_d
    frame["ppo_hist_12_26_9"] = compute_ppo_hist(close)
    frame["roc_12"] = close / close.shift(12) - 1.0
    frame["trix_15"] = compute_trix(close)
    frame["atr_14_over_atr_50"] = atr_14 / atr_50

    bb_mid_20 = sma(close, 20)
    bb_std_20 = close.rolling(window=20, min_periods=20).std(ddof=0)
    bb_upper = bb_mid_20 + 2.0 * bb_std_20
    bb_lower = bb_mid_20 - 2.0 * bb_std_20
    kc_mid = ema20
    kc_upper = kc_mid + 1.5 * atr_20
    kc_lower = kc_mid - 1.5 * atr_20
    frame["bollinger_width_20"] = (bb_upper - bb_lower) / bb_mid_20
    frame["bb_position_20"] = (close - bb_lower) / (bb_upper - bb_lower)
    frame["bb_squeeze"] = ((bb_upper <= kc_upper) & (bb_lower >= kc_lower)).astype(float)

    hv20 = frame["log_return_1"].rolling(window=20, min_periods=20).std(ddof=0) * np.sqrt(252 * 288)
    hv5 = frame["log_return_1"].rolling(window=5, min_periods=5).std(ddof=0) * np.sqrt(252 * 288)
    frame["historical_vol_20"] = hv20
    frame["historical_vol_5_over_20"] = hv5 / hv20

    adx14, plus_di_14, minus_di_14 = compute_adx(high, low, close, 14)
    frame["adx_14"] = adx14
    frame["di_spread_14"] = plus_di_14 - minus_di_14
    frame["supertrend_10_3"] = compute_supertrend_state(high, low, close, 10, 3.0)
    frame["vortex_indicator"] = compute_vortex(high, low, close, 14)

    session_features = compute_session_features(frame)
    for name, series in session_features.items():
        frame[name] = series

    return frame


def build_feature_frame(
    raw_root: Path,
    *,
    weights_path: Path | None = None,
    weights_version_label: str | None = None,
) -> tuple[pd.DataFrame, dict[str, object]]:
    weights_version = (
        WEIGHTS_VERSION
        if weights_path is None and weights_version_label is None
        else weights_version_label
        if weights_version_label is not None
        else f"{Path(weights_path).as_posix()} (custom_weight_source)"
    )
    frames = {binding.contract_symbol: load_raw_symbol(raw_root, binding) for binding in SYMBOL_BINDINGS}
    base = frames["US100"].copy()
    base = compute_main_features(base)
    base, alignment_missing_counts, exact_match_columns = attach_external_series(
        base,
        frames,
        weights_path=weights_path,
    )

    base["vix_change_1"] = base["vix_change_1"]
    base["vix_zscore_20"] = base["vix_zscore_20"]
    base["us10yr_change_1"] = base["us10yr_change_1"]
    base["us10yr_zscore_20"] = base["us10yr_zscore_20"]
    base["usdx_change_1"] = base["usdx_change_1"]
    base["usdx_zscore_20"] = base["usdx_zscore_20"]

    warmup_mask = pd.Series(False, index=base.index)
    warmup_mask.iloc[:WARMUP_BARS] = True

    main_symbol_missing_mask = base[["open", "high", "low", "close"]].isna().any(axis=1)
    main_symbol_missing_mask |= (base["high"] < base["low"])

    external_alignment_missing_mask = ~base[exact_match_columns].all(axis=1)
    session_semantics_missing_mask = base["overnight_return"].isna()
    weights_unavailable_mask = base[["msft_xnas_weight", "nvda_xnas_weight", "aapl_xnas_weight"]].isna().any(axis=1)
    numeric_invalid_mask = base[FEATURE_ORDER].replace([np.inf, -np.inf], np.nan).isna().any(axis=1)
    numeric_invalid_mask &= ~(warmup_mask | external_alignment_missing_mask | session_semantics_missing_mask | weights_unavailable_mask)

    invalid_reason_flags = {
        "warmup_incomplete": warmup_mask,
        "main_symbol_missing": main_symbol_missing_mask,
        "external_alignment_missing": external_alignment_missing_mask,
        "session_semantics_missing": session_semantics_missing_mask,
        "numeric_invalid": numeric_invalid_mask,
        "weights_unavailable": weights_unavailable_mask,
        "contract_version_mismatch": pd.Series(False, index=base.index),
    }

    for reason_code, mask in invalid_reason_flags.items():
        base[f"invalid__{reason_code}"] = mask.astype(bool)

    invalid_mask = pd.Series(False, index=base.index)
    for mask in invalid_reason_flags.values():
        invalid_mask |= mask
    base["valid_row"] = ~invalid_mask
    base = base.drop(columns=exact_match_columns)

    source_identities = [load_source_identity(raw_root, binding) for binding in SYMBOL_BINDINGS]
    counts = {
        "raw_rows": int(len(base)),
        "valid_rows": int(base["valid_row"].sum()),
        "invalid_rows": int((~base["valid_row"]).sum()),
        "weights_version": weights_version,
        "time_axis_policy_version": TIME_AXIS_POLICY_VERSION,
        "raw_time_axis_policy": RAW_TIME_AXIS_POLICY,
        "session_time_policy_status": SESSION_TIME_POLICY_STATUS,
        "invalid_reason_breakdown": {
            reason_code: int(mask.sum()) for reason_code, mask in invalid_reason_flags.items()
        },
        "alignment_missing_counts": alignment_missing_counts,
        "source_identities": source_identities,
    }
    return base, counts


def write_outputs(output_root: Path, frame: pd.DataFrame, counts: dict[str, object]) -> dict[str, str]:
    output_root.mkdir(parents=True, exist_ok=True)
    feature_hash = feature_order_hash()
    if feature_hash != EXPECTED_FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {feature_hash} != {EXPECTED_FEATURE_ORDER_HASH}")

    features_path = output_root / "features.parquet"
    validity_path = output_root / "row_validity_report.json"
    summary_path = output_root / "dataset_summary.json"
    feature_order_path = output_root / "feature_order.txt"
    parser_manifest_path = output_root / "parser_manifest.json"
    merge_report_path = output_root / "external_merge_report.json"
    debug_rows_path = output_root / "sample_debug_rows.csv"

    valid_frame = frame.loc[frame["valid_row"], ["timestamp"] + FEATURE_ORDER].copy()
    valid_frame["symbol"] = "US100"
    ordered_columns = ["timestamp", "symbol"] + FEATURE_ORDER
    valid_frame = valid_frame[ordered_columns]
    valid_frame[FEATURE_ORDER] = valid_frame[FEATURE_ORDER].astype("float32")
    valid_frame.to_parquet(features_path, index=False)

    invalid_reason_breakdown = counts["invalid_reason_breakdown"]
    row_validity_payload = {
        "dataset_id": DATASET_ID,
        "raw_rows": counts["raw_rows"],
        "valid_rows": counts["valid_rows"],
        "invalid_rows": counts["invalid_rows"],
        "invalid_reason_breakdown": invalid_reason_breakdown,
        "alignment_missing_counts": counts["alignment_missing_counts"],
        "weights_version": counts["weights_version"],
        "time_axis_policy_version": counts["time_axis_policy_version"],
        "raw_time_axis_policy": counts["raw_time_axis_policy"],
        "session_time_policy_status": counts["session_time_policy_status"],
        "raw_source_time_binding_assumption": "time_close_unix and time_open_unix are broker-clock bar-close/open keys, not direct UTC epoch seconds",
    }
    validity_path.write_text(json.dumps(row_validity_payload, indent=2), encoding="utf-8")

    source_identities = counts["source_identities"]
    summary_payload = {
        "dataset_id": DATASET_ID,
        "parser_version": PARSER_VERSION,
        "feature_count": len(FEATURE_ORDER),
        "feature_order_sha256": feature_hash,
        "window_start": WINDOW_START_UTC.isoformat(),
        "window_end_inclusive": WINDOW_END_UTC.isoformat(),
        "practical_modeling_start": PRACTICAL_MODELING_START_UTC.isoformat(),
        "warmup_bars": WARMUP_BARS,
        "preload_policy": "300 bars minimum; practical modeling start remains 2022-09-01",
        "weights_version": counts["weights_version"],
        "feature_contract_version": FEATURE_CONTRACT_VERSION,
        "parser_contract_version": PARSER_CONTRACT_VERSION,
        "time_axis_policy_version": TIME_AXIS_POLICY_VERSION,
        "raw_rows": counts["raw_rows"],
        "valid_rows": counts["valid_rows"],
        "invalid_rows": counts["invalid_rows"],
        "invalid_reason_breakdown": invalid_reason_breakdown,
        "source_identities": source_identities,
        "raw_time_axis_policy": counts["raw_time_axis_policy"],
        "session_time_policy_status": counts["session_time_policy_status"],
        "raw_source_time_binding_assumption": "time_close_unix and time_open_unix are broker-clock bar-close/open keys, not direct UTC epoch seconds",
    }
    summary_path.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    feature_order_path.write_text("\n".join(FEATURE_ORDER), encoding="utf-8")
    parser_manifest_path.write_text(
        json.dumps(
            {
                "dataset_id": DATASET_ID,
                "parser_version": PARSER_VERSION,
                "feature_contract_version": FEATURE_CONTRACT_VERSION,
                "parser_contract_version": PARSER_CONTRACT_VERSION,
                "time_axis_policy_version": TIME_AXIS_POLICY_VERSION,
                "feature_order_sha256": feature_hash,
                "raw_root": "data/raw/mt5_bars/m5",
                "output_root": str(output_root.as_posix()),
                "raw_time_axis_policy": RAW_TIME_AXIS_POLICY,
                "session_time_policy_status": SESSION_TIME_POLICY_STATUS,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    merge_report_path.write_text(
        json.dumps(
            {
                "dataset_id": DATASET_ID,
                "alignment_missing_counts": counts["alignment_missing_counts"],
                "weights_version": counts["weights_version"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    debug_columns = ["timestamp", "valid_row"] + [f"invalid__{reason}" for reason in INVALID_REASON_ORDER]
    debug_frame = frame[debug_columns].copy()
    debug_frame["timestamp"] = debug_frame["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    debug_frame.head(200).to_csv(debug_rows_path, index=False)

    return {
        "features_parquet_sha256": sha256_file(features_path),
        "row_validity_report_sha256": sha256_file(validity_path),
        "dataset_summary_sha256": sha256_file(summary_path),
    }


def main() -> int:
    args = parse_args()
    raw_root = Path(args.raw_root)
    output_root = Path(args.output_root)
    frame, counts = build_feature_frame(raw_root)
    hashes = write_outputs(output_root, frame, counts)
    payload = {
        "status": "ok",
        "dataset_id": DATASET_ID,
        "raw_rows": counts["raw_rows"],
        "valid_rows": counts["valid_rows"],
        "invalid_rows": counts["invalid_rows"],
        "invalid_reason_breakdown": counts["invalid_reason_breakdown"],
        "output_root": str(output_root.resolve()),
        "hashes": hashes,
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
