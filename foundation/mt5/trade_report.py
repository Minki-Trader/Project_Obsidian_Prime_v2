from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path
import sys
from typing import Any, Sequence

import pandas as pd


M5_MINUTES = 5.0


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


def _read_report_text(path: Path) -> str:
    raw = _io_path(path).read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16", errors="replace")
    return raw.decode("utf-8-sig", errors="replace")


def _io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


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
