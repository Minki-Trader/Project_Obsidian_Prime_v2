from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


TOP3_SYMBOLS: tuple[str, ...] = ("MSFT", "NVDA", "AAPL")
WEIGHT_COLUMNS: dict[str, str] = {
    "MSFT": "msft_xnas_weight",
    "NVDA": "nvda_xnas_weight",
    "AAPL": "aapl_xnas_weight",
}
CLOSE_COLUMNS: dict[str, str] = {
    "MSFT": "msft_xnas_close",
    "NVDA": "nvda_xnas_close",
    "AAPL": "aapl_xnas_close",
}


@dataclass(frozen=True)
class PriceProxyWeightSpec:
    start_month: str = "2022-08"
    end_month: str = "2026-04"
    sum_tolerance: float = 1e-9


def month_labels(start_month: str, end_month: str) -> list[str]:
    start = pd.Period(start_month, freq="M")
    end = pd.Period(end_month, freq="M")
    if end < start:
        raise ValueError(f"end_month must be >= start_month: {start_month} > {end_month}")
    return pd.period_range(start, end, freq="M").astype(str).tolist()


def load_close_frame(raw_root: Path, symbol: str) -> pd.DataFrame:
    symbol_dir = raw_root / symbol
    csv_candidates = sorted(symbol_dir.glob("*.csv"))
    if len(csv_candidates) != 1:
        raise RuntimeError(f"Expected exactly one raw CSV under {symbol_dir}, found {len(csv_candidates)}")
    frame = pd.read_csv(csv_candidates[0], usecols=["time_close_unix", "close"])
    frame["timestamp"] = pd.to_datetime(frame["time_close_unix"], unit="s", utc=True)
    frame = frame[["timestamp", "close"]].drop_duplicates("timestamp").sort_values("timestamp")
    if frame["timestamp"].duplicated().any():
        raise RuntimeError(f"Duplicate timestamps detected for {symbol}.")
    if not frame["timestamp"].is_monotonic_increasing:
        raise RuntimeError(f"Timestamps are not monotonic for {symbol}.")
    frame["close"] = pd.to_numeric(frame["close"], errors="coerce")
    if frame["close"].isna().any():
        raise RuntimeError(f"Close values contain NaN for {symbol}.")
    return frame.rename(columns={"close": CLOSE_COLUMNS[symbol]})


def build_common_close_frame(symbol_frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    missing_symbols = sorted(set(TOP3_SYMBOLS).difference(symbol_frames))
    if missing_symbols:
        raise RuntimeError(f"Missing close frames for symbols: {missing_symbols}")

    merged: pd.DataFrame | None = None
    for symbol in TOP3_SYMBOLS:
        source = symbol_frames[symbol][["timestamp", CLOSE_COLUMNS[symbol]]].copy()
        merged = source if merged is None else merged.merge(source, on="timestamp", how="inner")

    if merged is None or merged.empty:
        raise RuntimeError("No common MT5 timestamp exists for top3 price-proxy weights.")
    merged = merged.sort_values("timestamp").reset_index(drop=True)
    if not merged["timestamp"].is_monotonic_increasing:
        raise RuntimeError("Common top3 close frame timestamps are not monotonic.")
    return merged


def load_common_close_frame(raw_root: Path) -> pd.DataFrame:
    frames = {symbol: load_close_frame(raw_root, symbol) for symbol in TOP3_SYMBOLS}
    return build_common_close_frame(frames)


def _month_start(month: str) -> pd.Timestamp:
    return pd.Period(month, freq="M").start_time.tz_localize("UTC")


def _select_month_source_row(common: pd.DataFrame, month: str) -> tuple[pd.Series, str, bool]:
    month_start = _month_start(month)
    prior = common.loc[common["timestamp"] < month_start]
    if not prior.empty:
        return prior.iloc[-1], "last_common_closed_bar_before_month_start", False

    bootstrap = common.loc[common["timestamp"] >= month_start]
    if bootstrap.empty:
        raise RuntimeError(f"No common top3 closed bar is available for bootstrap month {month}.")
    return bootstrap.iloc[0], "first_common_closed_bar_in_month_bootstrap", True


def compute_monthly_price_proxy_weights(
    common_close_frame: pd.DataFrame,
    spec: PriceProxyWeightSpec = PriceProxyWeightSpec(),
) -> pd.DataFrame:
    required_columns = {"timestamp", *CLOSE_COLUMNS.values()}
    missing = required_columns.difference(common_close_frame.columns)
    if missing:
        raise RuntimeError(f"Common close frame is missing columns: {sorted(missing)}")

    rows: list[dict[str, object]] = []
    for month in month_labels(spec.start_month, spec.end_month):
        source_row, source_rule, bootstrap_month = _select_month_source_row(common_close_frame, month)
        closes = np.array([float(source_row[CLOSE_COLUMNS[symbol]]) for symbol in TOP3_SYMBOLS], dtype="float64")
        if not np.isfinite(closes).all() or (closes <= 0).any():
            raise RuntimeError(f"Invalid top3 close values for month {month}: {closes.tolist()}")
        close_sum = float(closes.sum())
        weights = closes / close_sum
        weight_sum = float(weights.sum())
        if abs(weight_sum - 1.0) > spec.sum_tolerance:
            raise RuntimeError(f"Weight sum out of tolerance for month {month}: {weight_sum}")

        row: dict[str, object] = {
            "month": month,
            "source_timestamp": pd.Timestamp(source_row["timestamp"]).isoformat(),
            "source_rule": source_rule,
            "bootstrap_month": bool(bootstrap_month),
            "weight_method": "mt5_price_proxy_close_share",
        }
        for symbol, close_value, weight_value in zip(TOP3_SYMBOLS, closes, weights, strict=True):
            row[CLOSE_COLUMNS[symbol]] = float(close_value)
            row[WEIGHT_COLUMNS[symbol]] = float(weight_value)
        row["weight_sum"] = weight_sum
        rows.append(row)

    result = pd.DataFrame(rows)
    validate_price_proxy_weights(result, spec)
    return result


def validate_price_proxy_weights(
    weights: pd.DataFrame,
    spec: PriceProxyWeightSpec = PriceProxyWeightSpec(),
) -> None:
    expected_months = month_labels(spec.start_month, spec.end_month)
    actual_months = weights["month"].astype(str).tolist() if "month" in weights.columns else []
    if actual_months != expected_months:
        raise RuntimeError(f"Monthly weight coverage mismatch: {actual_months} != {expected_months}")

    required_columns = {
        "month",
        "source_timestamp",
        "source_rule",
        "bootstrap_month",
        "weight_method",
        "weight_sum",
        *CLOSE_COLUMNS.values(),
        *WEIGHT_COLUMNS.values(),
    }
    missing = required_columns.difference(weights.columns)
    if missing:
        raise RuntimeError(f"Weight table is missing columns: {sorted(missing)}")

    weight_values = weights.loc[:, list(WEIGHT_COLUMNS.values())].to_numpy(dtype="float64")
    if not np.isfinite(weight_values).all():
        raise RuntimeError("Weight table contains NaN or infinite weights.")
    if (weight_values <= 0).any():
        raise RuntimeError("Weight table contains non-positive weights.")

    sums = weight_values.sum(axis=1)
    if not np.allclose(sums, 1.0, atol=spec.sum_tolerance, rtol=0.0):
        raise RuntimeError("Weight table rows do not sum to 1.0 within tolerance.")

