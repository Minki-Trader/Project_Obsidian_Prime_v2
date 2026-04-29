from __future__ import annotations

import argparse
import csv
import json
import math
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd
import yaml

from foundation.control_plane.ledger import io_path, json_ready, ledger_value, sha256_file_lf_normalized


PACKET_ID_DEFAULT = "kpi_trade_attribution_v1"
SOURCE_PACKET_ID_DEFAULT = "kpi_rebuild_mt5_recording_v1"
SOURCE_RECORDS_PATH = Path("docs/agent_control/packets/kpi_rebuild_mt5_recording_v1/normalized_kpi_records.jsonl")
RAW_US100_BARS_PATH = Path("data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv")
FEATURE_FRAME_PATH = Path("data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58/features.parquet")
M5_MINUTES = 5.0

ACTUAL_ROUTE_ROLES = {"routed_total", "tier_only_total", "tier_b_fallback_only_total", "not_applicable"}
SESSION_SLICE_DEFINITIONS = {
    "early": (0.0, 110.0),
    "mid": (110.0, 220.0),
    "late": (220.0, 330.0),
    "mid_second_overlap_200_220": (200.0, 220.0),
}

TRADE_COLUMNS = (
    "run_id",
    "record_view",
    "split",
    "tier_scope",
    "route_role",
    "trade_index",
    "direction",
    "open_time",
    "close_time",
    "hold_bars",
    "volume",
    "open_price",
    "close_price",
    "gross_profit",
    "net_profit",
    "swap",
    "commission",
    "mfe",
    "mae",
    "realized_over_mfe",
    "session_slice",
    "volatility_regime",
    "trend_regime",
    "adx_bucket",
    "spread_regime",
)

SUMMARY_COLUMNS = (
    "run_id",
    "record_view",
    "split",
    "tier_scope",
    "route_role",
    "trade_count",
    "avg_hold_bars",
    "mfe_mean",
    "mae_mean",
    "long_net_profit",
    "short_net_profit",
    "positive_month_ratio",
    "status",
)


@dataclass(frozen=True)
class Deal:
    time: pd.Timestamp
    ticket: str
    symbol: str
    order_type: str
    direction: str
    volume: float
    price: float | None
    order: str
    commission: float
    swap: float
    profit: float
    balance: float | None
    comment: str


@dataclass(frozen=True)
class Trade:
    index: int
    direction: str
    open_time: pd.Timestamp
    close_time: pd.Timestamp
    volume: float
    open_price: float
    close_price: float
    gross_profit: float
    net_profit: float
    swap: float
    commission: float


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell_active = False
        self._cell_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self._row = []
        if tag in {"td", "th"} and self._row is not None:
            self._cell_active = True
            self._cell_parts = []

    def handle_data(self, data: str) -> None:
        if self._cell_active:
            self._cell_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._row is not None:
            self._row.append(" ".join("".join(self._cell_parts).split()))
            self._cell_active = False
        if tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None


def write_mt5_trade_attribution_packet(
    root: Path | str = Path("."),
    *,
    packet_id: str = PACKET_ID_DEFAULT,
    source_packet_id: str = SOURCE_PACKET_ID_DEFAULT,
    output_dir: Path | str | None = None,
    created_at_utc: str | None = None,
) -> dict[str, Any]:
    root_path = Path(root).resolve()
    created_at = created_at_utc or _utc_now()
    source_records = _read_jsonl(root_path / SOURCE_RECORDS_PATH)
    market_data = MarketData.load(root_path)
    enriched_records, trade_rows, summary_rows, parser_errors = enrich_records(source_records, root_path, market_data)
    summary = _build_summary(
        packet_id=packet_id,
        source_packet_id=source_packet_id,
        created_at_utc=created_at,
        source_records=source_records,
        enriched_records=enriched_records,
        trade_rows=trade_rows,
        summary_rows=summary_rows,
        parser_errors=parser_errors,
    )
    packet = {
        "summary": summary,
        "enriched_records": enriched_records,
        "trade_rows": trade_rows,
        "summary_rows": summary_rows,
        "parser_errors": parser_errors,
        "work_packet": _build_work_packet(packet_id, source_packet_id, created_at, summary),
        "receipts": _build_receipts(packet_id, source_packet_id, created_at, summary),
    }
    out_dir = Path(output_dir) if output_dir is not None else root_path / "docs/agent_control/packets" / packet_id
    if not out_dir.is_absolute():
        out_dir = root_path / out_dir
    io_path(out_dir / "skill_receipts").mkdir(parents=True, exist_ok=True)
    _write_jsonl(out_dir / "enriched_kpi_records.jsonl", enriched_records)
    _write_csv(out_dir / "trade_level_records.csv", TRADE_COLUMNS, trade_rows)
    _write_csv(out_dir / "trade_attribution_summary.csv", SUMMARY_COLUMNS, summary_rows)
    _write_json(out_dir / "attribution_summary.json", summary)
    _write_json(out_dir / "parser_errors.json", parser_errors)
    _write_yaml(out_dir / "work_packet.yaml", packet["work_packet"])
    for name, receipt in packet["receipts"].items():
        _write_yaml(out_dir / "skill_receipts" / f"{name}.yaml", receipt)
    return packet


def enrich_records(
    records: Sequence[Mapping[str, Any]],
    root: Path,
    market_data: "MarketData",
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    enriched: list[dict[str, Any]] = []
    trade_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    parser_errors: list[dict[str, Any]] = []

    for record in records:
        current = deepcopy(dict(record))
        if not _is_trade_attribution_allowed(current):
            enriched.append(current)
            continue
        report_path = _record_report_path(root, current)
        if report_path is None:
            _mark_trade_missing(current, "mt5_report_path_missing")
            enriched.append(current)
            continue
        try:
            report = parse_mt5_trade_report(report_path)
            trades = pair_deals_into_trades(report["deals"])
            stats = compute_trade_attribution(trades, market_data)
        except Exception as exc:  # pragma: no cover - real malformed reports stay auditable
            parser_errors.append(
                {
                    "run_id": _value(current, "row_grain", "run_id"),
                    "record_view": _value(current, "row_grain", "record_view"),
                    "report_path": report_path.as_posix(),
                    "error": str(exc),
                }
            )
            _mark_trade_missing(current, "trade_attribution_parse_error")
            enriched.append(current)
            continue
        if stats["trade_count"] == 0:
            _mark_trade_missing(current, "mt5_deal_list_empty")
            enriched.append(current)
            continue
        _apply_trade_stats(current, stats)
        summary_rows.append(_summary_row(current, stats))
        trade_rows.extend(_trade_rows(current, stats["trades"]))
        enriched.append(current)

    _fill_validation_oos_gaps(enriched)
    return enriched, trade_rows, summary_rows, parser_errors


class MarketData:
    def __init__(self, bars: pd.DataFrame, features: pd.DataFrame) -> None:
        self.bars = bars
        self.features = features
        self.volatility_edges = _quantile_edges(features["historical_vol_20"])
        self.spread_edges = _quantile_edges(bars["spread_points"])

    @classmethod
    def load(cls, root: Path) -> "MarketData":
        bars = load_us100_bars(root / RAW_US100_BARS_PATH)
        features = load_feature_frame(root / FEATURE_FRAME_PATH)
        return cls(bars, features)

    @classmethod
    def from_frames(cls, bars: pd.DataFrame, features: pd.DataFrame) -> "MarketData":
        prepared_bars = prepare_bars(bars)
        prepared_features = prepare_features(features)
        return cls(prepared_bars, prepared_features)


def load_us100_bars(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(
        io_path(path),
        usecols=["time_open_unix", "time_close_unix", "open", "high", "low", "close", "spread_points"],
    )
    return prepare_bars(frame)


def prepare_bars(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    if "time_open" not in result.columns:
        result["time_open"] = pd.to_datetime(result["time_open_unix"], unit="s")
    if "time_close" not in result.columns:
        result["time_close"] = pd.to_datetime(result["time_close_unix"], unit="s")
    for column in ("open", "high", "low", "close", "spread_points"):
        result[column] = pd.to_numeric(result[column], errors="coerce")
    return result.sort_values("time_open").reset_index(drop=True)


def load_feature_frame(path: Path) -> pd.DataFrame:
    columns = [
        "timestamp",
        "minutes_from_cash_open",
        "historical_vol_20",
        "adx_14",
        "di_spread_14",
        "supertrend_10_3",
    ]
    frame = pd.read_parquet(io_path(path), columns=columns)
    return prepare_features(frame)


def prepare_features(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["timestamp_key"] = pd.to_datetime(result["timestamp"], utc=True).dt.tz_localize(None)
    for column in ("minutes_from_cash_open", "historical_vol_20", "adx_14", "di_spread_14", "supertrend_10_3"):
        if column not in result.columns:
            result[column] = math.nan
        result[column] = pd.to_numeric(result[column], errors="coerce")
    return result.sort_values("timestamp_key").drop_duplicates("timestamp_key", keep="last").reset_index(drop=True)


def parse_mt5_trade_report(report_path: Path) -> dict[str, Any]:
    text = _read_report_text(report_path)
    parser = _TableParser()
    parser.feed(text)
    return {
        "deals": _extract_deals(parser.rows),
        "summary": _extract_report_summary(parser.rows),
    }


def pair_deals_into_trades(deals: Sequence[Deal]) -> list[Trade]:
    trades: list[Trade] = []
    open_deal: Deal | None = None
    for deal in deals:
        if deal.direction == "in" and deal.price is not None:
            open_deal = deal
            continue
        if deal.direction != "out" or open_deal is None or deal.price is None:
            continue
        trades.append(
            Trade(
                index=len(trades) + 1,
                direction=open_deal.order_type.lower(),
                open_time=open_deal.time,
                close_time=deal.time,
                volume=min(open_deal.volume, deal.volume),
                open_price=float(open_deal.price),
                close_price=float(deal.price),
                gross_profit=deal.profit,
                net_profit=deal.profit + deal.swap + deal.commission,
                swap=deal.swap,
                commission=deal.commission,
            )
        )
        open_deal = None
    return trades


def compute_trade_attribution(trades: Sequence[Trade], market_data: MarketData) -> dict[str, Any]:
    trade_payloads = []
    for trade in trades:
        payload = _trade_payload(trade, market_data)
        trade_payloads.append(payload)
    return {
        "trade_count": len(trade_payloads),
        "trades": trade_payloads,
        "trade_diagnostics": _trade_diagnostics(trade_payloads),
        "risk": _risk_from_trades(trade_payloads),
        "regime_slice_attribution": _regime_from_trades(trade_payloads),
    }


def _trade_payload(trade: Trade, market_data: MarketData) -> dict[str, Any]:
    bars = market_data.bars
    window = bars.loc[(bars["time_open"] >= trade.open_time) & (bars["time_open"] < trade.close_time)].copy()
    if window.empty:
        window = bars.loc[bars["time_open"].eq(trade.open_time)].copy()
    high = _finite_or_none(window["high"].max() if not window.empty else None)
    low = _finite_or_none(window["low"].min() if not window.empty else None)
    high = max(high if high is not None else trade.open_price, trade.open_price, trade.close_price)
    low = min(low if low is not None else trade.open_price, trade.open_price, trade.close_price)
    if trade.direction == "buy":
        mfe = max(0.0, (high - trade.open_price) * trade.volume)
        mae = max(0.0, (trade.open_price - low) * trade.volume)
    else:
        mfe = max(0.0, (trade.open_price - low) * trade.volume)
        mae = max(0.0, (high - trade.open_price) * trade.volume)
    hold_bars = max(0.0, (trade.close_time - trade.open_time).total_seconds() / 60.0 / M5_MINUTES)
    feature = _feature_at(market_data.features, trade.open_time)
    bar = _bar_at(market_data.bars, trade.open_time)
    realized_over_mfe = trade.net_profit / mfe if mfe else None
    return {
        "trade_index": trade.index,
        "direction": trade.direction,
        "open_time": trade.open_time,
        "close_time": trade.close_time,
        "hold_bars": hold_bars,
        "volume": trade.volume,
        "open_price": trade.open_price,
        "close_price": trade.close_price,
        "gross_profit": trade.gross_profit,
        "net_profit": trade.net_profit,
        "swap": trade.swap,
        "commission": trade.commission,
        "mfe": mfe,
        "mae": mae,
        "realized_over_mfe": realized_over_mfe,
        "session_slice": _session_slice(feature.get("minutes_from_cash_open"), trade.open_time),
        "volatility_regime": _bucket(feature.get("historical_vol_20"), market_data.volatility_edges, "vol"),
        "trend_regime": _trend_regime(feature),
        "adx_bucket": _adx_bucket(feature.get("adx_14")),
        "spread_regime": _bucket(bar.get("spread_points"), market_data.spread_edges, "spread"),
        "month": trade.close_time.strftime("%Y-%m"),
        "quarter": f"{trade.close_time.year}-Q{((trade.close_time.month - 1) // 3) + 1}",
    }


def _trade_diagnostics(trades: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    long_trades = [row for row in trades if row["direction"] == "buy"]
    short_trades = [row for row in trades if row["direction"] == "sell"]
    loss_trades = [row for row in trades if float(row["net_profit"]) < 0.0]
    win_trades = [row for row in trades if float(row["net_profit"]) > 0.0]
    return {
        "long_trade_count": len(long_trades),
        "short_trade_count": len(short_trades),
        "long_net_profit": _sum(long_trades, "net_profit"),
        "short_net_profit": _sum(short_trades, "net_profit"),
        "long_expectancy": _mean([row["net_profit"] for row in long_trades]),
        "short_expectancy": _mean([row["net_profit"] for row in short_trades]),
        "avg_hold_bars": _mean([row["hold_bars"] for row in trades]),
        "hold_distribution": {
            "min": _min([row["hold_bars"] for row in trades]),
            "median": _median([row["hold_bars"] for row in trades]),
            "max": _max([row["hold_bars"] for row in trades]),
        },
        "mfe_mean": _mean([row["mfe"] for row in trades]),
        "mae_mean": _mean([row["mae"] for row in trades]),
        "realized_over_mfe": _mean([row["realized_over_mfe"] for row in trades if row["realized_over_mfe"] is not None]),
        "loss_trade_mfe": {
            "loss_trades": len(loss_trades),
            "loss_with_positive_mfe": sum(1 for row in loss_trades if float(row["mfe"]) > 0.0),
            "ratio": _ratio(sum(1 for row in loss_trades if float(row["mfe"]) > 0.0), len(loss_trades)),
            "mfe_mean": _mean([row["mfe"] for row in loss_trades]),
        },
        "win_trade_mae": {
            "win_trades": len(win_trades),
            "win_with_positive_mae": sum(1 for row in win_trades if float(row["mae"]) > 0.0),
            "ratio": _ratio(sum(1 for row in win_trades if float(row["mae"]) > 0.0), len(win_trades)),
            "mae_mean": _mean([row["mae"] for row in win_trades]),
        },
    }


def _risk_from_trades(trades: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_day = _group_sum(trades, lambda row: str(row["close_time"])[:10])
    by_week = _group_sum(trades, lambda row: pd.Timestamp(row["close_time"]).strftime("%G-W%V"))
    consecutive_losses = 0
    current = 0
    for row in sorted(trades, key=lambda item: item["close_time"]):
        if float(row["net_profit"]) < 0.0:
            current += 1
            consecutive_losses = max(consecutive_losses, current)
        else:
            current = 0
    return {
        "worst_day": min(by_day.values()) if by_day else None,
        "worst_week": min(by_week.values()) if by_week else None,
        "consecutive_losses": consecutive_losses,
    }


def _regime_from_trades(trades: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    month_pnl = _group_sum(trades, lambda row: str(row["month"]))
    quarter_pnl = _group_sum(trades, lambda row: str(row["quarter"]))
    return {
        "session_slice": _group_summary(trades, "session_slice"),
        "volatility_regime": _group_summary(trades, "volatility_regime"),
        "trend_regime": _group_summary(trades, "trend_regime"),
        "adx_bucket": _group_summary(trades, "adx_bucket"),
        "spread_regime": _group_summary(trades, "spread_regime"),
        "month_pnl": month_pnl,
        "quarter_pnl": quarter_pnl,
        "subperiod_consistency": _subperiod_consistency(month_pnl),
    }


def _apply_trade_stats(record: dict[str, Any], stats: Mapping[str, Any]) -> None:
    diagnostics = stats["trade_diagnostics"]
    for field, value in diagnostics.items():
        n_a_reason = None
        if field == "long_expectancy" and value is None and diagnostics.get("long_trade_count") == 0:
            n_a_reason = "no_long_trades"
        elif field == "short_expectancy" and value is None and diagnostics.get("short_trade_count") == 0:
            n_a_reason = "no_short_trades"
        record["trade_diagnostics"][field] = _cell(
            value,
            n_a_reason,
            authority="python_recomputed_from_mt5_deals",
        )
    for field, value in stats["risk"].items():
        record["risk"][field] = _cell(value, authority="python_recomputed_from_mt5_deals")
    for field, value in stats["regime_slice_attribution"].items():
        record["regime_slice_attribution"][field] = _cell(value, authority="python_attribution_from_signal_and_trade_join")
    record["source_evidence"]["trade_attribution"] = {
        "parser": "foundation.control_plane.mt5_trade_attribution",
        "price_source": RAW_US100_BARS_PATH.as_posix(),
        "feature_source": FEATURE_FRAME_PATH.as_posix(),
        "mfe_mae_convention": "money_units_positive_favorable_and_positive_adverse",
    }


def _fill_validation_oos_gaps(records: Sequence[dict[str, Any]]) -> None:
    by_key: dict[tuple[str, str, str], dict[str, float]] = {}
    for record in records:
        key = (
            str(_value(record, "row_grain", "run_id")),
            str(_value(record, "row_grain", "tier_scope")),
            str(_value(record, "row_grain", "route_role")),
        )
        split = str(_value(record, "row_grain", "split"))
        net = _value(record, "mt5_trading_headline", "net_profit")
        if isinstance(net, (int, float)):
            by_key.setdefault(key, {})[split] = float(net)
    for record in records:
        key = (
            str(_value(record, "row_grain", "run_id")),
            str(_value(record, "row_grain", "tier_scope")),
            str(_value(record, "row_grain", "route_role")),
        )
        pair = by_key.get(key, {})
        if "validation" in pair and "oos" in pair:
            record["regime_slice_attribution"]["validation_oos_gap"] = _cell(
                {
                    "oos_minus_validation_net_profit": pair["oos"] - pair["validation"],
                    "validation_net_profit": pair["validation"],
                    "oos_net_profit": pair["oos"],
                },
                authority="python_attribution_from_signal_and_trade_join",
            )


def _extract_deals(rows: Sequence[Sequence[str]]) -> list[Deal]:
    header_index = None
    for index, row in enumerate(rows):
        if _is_deal_header(row):
            header_index = index
            break
    if header_index is None:
        return []
    deals: list[Deal] = []
    for row in rows[header_index + 1 :]:
        if len(row) < 13:
            continue
        if row[4].lower() not in {"in", "out"}:
            continue
        deals.append(
            Deal(
                time=_parse_time(row[0]),
                ticket=row[1],
                symbol=row[2],
                order_type=row[3].lower(),
                direction=row[4].lower(),
                volume=_num(row[5]) or 0.0,
                price=_num(row[6]),
                order=row[7],
                commission=_num(row[8]) or 0.0,
                swap=_num(row[9]) or 0.0,
                profit=_num(row[10]) or 0.0,
                balance=_num(row[11]),
                comment=row[12],
            )
        )
    return deals


def _extract_report_summary(rows: Sequence[Sequence[str]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for row in rows:
        for index, cell in enumerate(row):
            if cell in {"\ud3c9\uade0 \ud3ec\uc9c0\uc158 \ud640\ub529\uc2dc\uac04:", "Average position holding time:"} and index + 1 < len(row):
                summary["average_position_holding_time"] = row[index + 1]
                summary["average_position_holding_bars"] = _duration_to_bars(row[index + 1])
            if cell == "Correlation (Profits,MFE):" and index + 1 < len(row):
                summary["correlation_profit_mfe"] = _num(row[index + 1])
            if cell == "Correlation (Profits,MAE):" and index + 1 < len(row):
                summary["correlation_profit_mae"] = _num(row[index + 1])
            if cell == "Correlation (MFE,MAE):" and index + 1 < len(row):
                summary["correlation_mfe_mae"] = _num(row[index + 1])
    return summary


def _is_deal_header(row: Sequence[str]) -> bool:
    lowered = [cell.lower() for cell in row]
    return (
        len(row) >= 13
        and (row[0] in {"\uc2dc\uac04", "Time"})
        and (row[4] in {"\ubc29\ud5a5", "Direction"})
        and ("profit" in lowered or "\uc218\uc775" in row)
    )


def _is_trade_attribution_allowed(record: Mapping[str, Any]) -> bool:
    role = str(_value(record, "row_grain", "route_role") or "")
    if role not in ACTUAL_ROUTE_ROLES:
        return False
    net_cell = record.get("mt5_trading_headline", {}).get("net_profit", {})
    return isinstance(net_cell, Mapping) and net_cell.get("n/a_reason") in {None, ""}


def _mark_trade_missing(record: dict[str, Any], reason: str) -> None:
    for field in (
        "long_net_profit",
        "short_net_profit",
        "long_expectancy",
        "short_expectancy",
        "avg_hold_bars",
        "hold_distribution",
        "mfe_mean",
        "mae_mean",
        "realized_over_mfe",
        "loss_trade_mfe",
        "win_trade_mae",
    ):
        record["trade_diagnostics"][field] = _cell(None, reason, "python_recomputed_from_mt5_deals")
    for field in ("session_slice", "volatility_regime", "trend_regime", "adx_bucket", "spread_regime", "month_pnl", "quarter_pnl", "subperiod_consistency"):
        record["regime_slice_attribution"][field] = _cell(None, reason, "python_attribution_from_signal_and_trade_join")


def _record_report_path(root: Path, record: Mapping[str, Any]) -> Path | None:
    source = record.get("source_evidence", {})
    if not isinstance(source, Mapping):
        return None
    raw = source.get("mt5_report_path")
    if not raw:
        return None
    path = Path(str(raw))
    if not path.is_absolute():
        path = root / path
    return path


def _read_report_text(path: Path) -> str:
    raw = io_path(path).read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16", errors="replace")
    return raw.decode("utf-8-sig", errors="replace")


def _feature_at(features: pd.DataFrame, timestamp: pd.Timestamp) -> dict[str, Any]:
    matched = features.loc[features["timestamp_key"].eq(timestamp)]
    if matched.empty:
        return {}
    return matched.iloc[-1].to_dict()


def _bar_at(bars: pd.DataFrame, timestamp: pd.Timestamp) -> dict[str, Any]:
    matched = bars.loc[bars["time_open"].eq(timestamp)]
    if matched.empty:
        return {}
    return matched.iloc[-1].to_dict()


def _session_slice(minutes: Any, timestamp: pd.Timestamp | None = None) -> str:
    value = _float_or_none(minutes)
    if value is None and timestamp is not None:
        value = _minutes_from_cash_open_fallback(timestamp)
    if value is None:
        return "feature_missing"
    for name in ("early", "mid", "late"):
        start, end = SESSION_SLICE_DEFINITIONS[name]
        if value > start and value <= end:
            return name
    return "outside_cash_session"


def _minutes_from_cash_open_fallback(timestamp: pd.Timestamp) -> float | None:
    try:
        broker_time = pd.Timestamp(timestamp).tz_localize("Europe/Athens", ambiguous="raise", nonexistent="raise")
        ny_time = broker_time.tz_convert("America/New_York")
    except Exception:
        return None
    session_open = ny_time.normalize() + pd.Timedelta(hours=9, minutes=30)
    return (ny_time - session_open).total_seconds() / 60.0


def _trend_regime(feature: Mapping[str, Any]) -> str:
    adx = _float_or_none(feature.get("adx_14"))
    state = _float_or_none(feature.get("supertrend_10_3"))
    if adx is None or state is None:
        return "feature_missing"
    if adx < 20:
        return "range_or_weak_trend"
    return "uptrend" if state > 0 else "downtrend"


def _adx_bucket(value: Any) -> str:
    number = _float_or_none(value)
    if number is None:
        return "feature_missing"
    if number < 20:
        return "adx_lt20"
    if number <= 25:
        return "adx_20_25"
    return "adx_gt25"


def _bucket(value: Any, edges: tuple[float, float] | None, prefix: str) -> str:
    number = _float_or_none(value)
    if number is None or edges is None:
        return "feature_missing"
    low, high = edges
    if number <= low:
        return f"{prefix}_low"
    if number <= high:
        return f"{prefix}_mid"
    return f"{prefix}_high"


def _group_summary(trades: Sequence[Mapping[str, Any]], key: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for row in trades:
        bucket = str(row.get(key) or "missing")
        slot = result.setdefault(bucket, {"trade_count": 0, "net_profit": 0.0})
        slot["trade_count"] += 1
        slot["net_profit"] += float(row.get("net_profit") or 0.0)
    return {key: {"trade_count": value["trade_count"], "net_profit": round(value["net_profit"], 6)} for key, value in sorted(result.items())}


def _group_sum(trades: Sequence[Mapping[str, Any]], key_fn: Any) -> dict[str, float]:
    result: dict[str, float] = {}
    for row in trades:
        key = key_fn(row)
        result[key] = result.get(key, 0.0) + float(row.get("net_profit") or 0.0)
    return {key: round(value, 6) for key, value in sorted(result.items())}


def _subperiod_consistency(month_pnl: Mapping[str, float]) -> dict[str, Any]:
    values = list(month_pnl.values())
    positive = sum(1 for value in values if value > 0.0)
    negative = sum(1 for value in values if value < 0.0)
    return {
        "months": len(values),
        "positive_months": positive,
        "negative_months": negative,
        "positive_month_ratio": _ratio(positive, len(values)),
        "best_month_pnl": max(values) if values else None,
        "worst_month_pnl": min(values) if values else None,
    }


def _summary_row(record: Mapping[str, Any], stats: Mapping[str, Any]) -> dict[str, Any]:
    diagnostics = stats["trade_diagnostics"]
    consistency = stats["regime_slice_attribution"]["subperiod_consistency"]
    return {
        "run_id": _value(record, "row_grain", "run_id"),
        "record_view": _value(record, "row_grain", "record_view"),
        "split": _value(record, "row_grain", "split"),
        "tier_scope": _value(record, "row_grain", "tier_scope"),
        "route_role": _value(record, "row_grain", "route_role"),
        "trade_count": stats["trade_count"],
        "avg_hold_bars": diagnostics["avg_hold_bars"],
        "mfe_mean": diagnostics["mfe_mean"],
        "mae_mean": diagnostics["mae_mean"],
        "long_net_profit": diagnostics["long_net_profit"],
        "short_net_profit": diagnostics["short_net_profit"],
        "positive_month_ratio": consistency["positive_month_ratio"],
        "status": "trade_attribution_recorded",
    }


def _trade_rows(record: Mapping[str, Any], trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for trade in trades:
        row = {column: trade.get(column) for column in TRADE_COLUMNS}
        row.update(
            {
                "run_id": _value(record, "row_grain", "run_id"),
                "record_view": _value(record, "row_grain", "record_view"),
                "split": _value(record, "row_grain", "split"),
                "tier_scope": _value(record, "row_grain", "tier_scope"),
                "route_role": _value(record, "row_grain", "route_role"),
                "open_time": trade["open_time"].strftime("%Y-%m-%d %H:%M:%S"),
                "close_time": trade["close_time"].strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        rows.append(row)
    return rows


def _build_summary(
    *,
    packet_id: str,
    source_packet_id: str,
    created_at_utc: str,
    source_records: Sequence[Mapping[str, Any]],
    enriched_records: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    summary_rows: Sequence[Mapping[str, Any]],
    parser_errors: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    source_actual = [record for record in source_records if _is_trade_attribution_allowed(record)]
    enriched_actual = len(summary_rows)
    status = "trade_attribution_complete" if source_actual and enriched_actual == len(source_actual) and not parser_errors else "partial_trade_attribution"
    return {
        "packet_id": packet_id,
        "source_packet_id": source_packet_id,
        "created_at_utc": created_at_utc,
        "status": status,
        "source_records": len(source_records),
        "actual_records_requiring_trade_attribution": len(source_actual),
        "records_with_trade_attribution": enriched_actual,
        "trade_level_rows": len(trade_rows),
        "parser_error_count": len(parser_errors),
        "outputs": {
            "enriched_kpi_records": f"docs/agent_control/packets/{packet_id}/enriched_kpi_records.jsonl",
            "trade_level_records": f"docs/agent_control/packets/{packet_id}/trade_level_records.csv",
            "trade_attribution_summary": f"docs/agent_control/packets/{packet_id}/trade_attribution_summary.csv",
        },
        "claim_boundary": "fills trade diagnostics and regime attribution only where MT5 deal list and price/feature joins exist",
    }


def _build_work_packet(packet_id: str, source_packet_id: str, created_at: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": packet_id,
        "created_at_utc": created_at,
        "source_packet_id": source_packet_id,
        "requested_action": "fill_trade_diagnostics_and_regime_slice_attribution",
        "scope": {
            "avg_hold_bars": "from paired MT5 in/out deals",
            "mfe_mae": "from MT5 deals joined to US100 M5 OHLC bars",
            "regime_slice": "from trade open time joined to feature frame",
        },
        "status": summary["status"],
        "completion_forbidden_if": ["parser_error_count > 0", "records_with_trade_attribution < actual_records_requiring_trade_attribution"],
    }


def _build_receipts(packet_id: str, source_packet_id: str, created_at: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "backtest_forensics": {
            "packet_id": packet_id,
            "source_packet_id": source_packet_id,
            "created_at_utc": created_at,
            "trade_evidence": "MT5 deal list parsed from strategy tester HTML reports",
            "backtest_judgment": "usable_with_boundary" if summary["records_with_trade_attribution"] else "blocked",
            "blocking_findings": [] if not summary["parser_error_count"] else ["Some reports could not be parsed."],
        },
        "performance_attribution": {
            "packet_id": packet_id,
            "observed_change": "trade diagnostics and regime/slice fields populated from deal-level evidence",
            "segment_checks": ["session_slice", "volatility_regime", "trend_regime", "adx_bucket", "spread_regime", "month_pnl", "quarter_pnl"],
            "attribution_confidence": "medium",
            "next_probe": "compare enriched validation/OOS gaps against selected candidates before new experiment choice",
        },
        "runtime_parity": {
            "packet_id": packet_id,
            "runtime_path": "MT5 strategy tester reports and Common/Files telemetry",
            "research_path": "foundation.control_plane.mt5_trade_attribution",
            "runtime_claim_boundary": "runtime_probe",
            "known_differences": ["MFE/MAE are recomputed from exported OHLC bars, not read as scalar fields from MT5 report."],
        },
    }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not io_path(path).exists():
        return []
    return [json.loads(line) for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def _write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(json_ready(row), ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def _write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def _write_yaml(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False), encoding="utf-8")


def _write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: ledger_value(row.get(column, "")) for column in columns})


def _cell(value: Any, n_a_reason: str | None = None, authority: str = "") -> dict[str, Any]:
    return {"value": json_ready(value), "n/a_reason": n_a_reason, "authority": authority}


def _value(record: Mapping[str, Any], section: str, field: str) -> Any:
    cell = record.get(section, {}).get(field, {})
    return cell.get("value") if isinstance(cell, Mapping) else None


def _parse_time(value: str) -> pd.Timestamp:
    return pd.Timestamp(datetime.strptime(value, "%Y.%m.%d %H:%M:%S"))


def _duration_to_bars(value: str) -> float | None:
    parts = value.split(":")
    if len(parts) != 3:
        return None
    hours, minutes, seconds = (int(part) for part in parts)
    duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return duration.total_seconds() / 60.0 / M5_MINUTES


def _num(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip().replace(",", "")
    if not text:
        return None
    if " " in text:
        text = text.split(" ")[0]
    try:
        return float(text)
    except ValueError:
        return None


def _float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _finite_or_none(value: Any) -> float | None:
    return _float_or_none(value)


def _quantile_edges(series: pd.Series) -> tuple[float, float] | None:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return None
    low = float(clean.quantile(1.0 / 3.0))
    high = float(clean.quantile(2.0 / 3.0))
    return (low, high)


def _sum(rows: Sequence[Mapping[str, Any]], field: str) -> float:
    return round(sum(float(row.get(field) or 0.0) for row in rows), 6)


def _mean(values: Sequence[Any]) -> float | None:
    clean = [_float_or_none(value) for value in values]
    clean = [value for value in clean if value is not None]
    return round(sum(clean) / len(clean), 6) if clean else None


def _median(values: Sequence[Any]) -> float | None:
    clean = sorted(value for value in (_float_or_none(item) for item in values) if value is not None)
    if not clean:
        return None
    mid = len(clean) // 2
    if len(clean) % 2:
        return round(clean[mid], 6)
    return round((clean[mid - 1] + clean[mid]) / 2.0, 6)


def _min(values: Sequence[Any]) -> float | None:
    clean = [value for value in (_float_or_none(item) for item in values) if value is not None]
    return round(min(clean), 6) if clean else None


def _max(values: Sequence[Any]) -> float | None:
    clean = [value for value in (_float_or_none(item) for item in values) if value is not None]
    return round(max(clean), 6) if clean else None


def _ratio(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 6) if denominator else None


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build deal-level MT5 trade attribution KPI packet.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--packet-id", default=PACKET_ID_DEFAULT)
    parser.add_argument("--created-at-utc", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    packet = write_mt5_trade_attribution_packet(
        Path(args.root),
        packet_id=args.packet_id,
        created_at_utc=args.created_at_utc,
    )
    print(json.dumps(packet["summary"], ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
