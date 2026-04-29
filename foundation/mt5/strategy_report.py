from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Sequence

from foundation.control_plane.ledger import io_path


class _Mt5ReportTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[str]] = []
        self._current_row: list[str] | None = None
        self._current_cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "tr":
            self._current_row = []
        elif tag in {"td", "th"} and self._current_row is not None:
            self._current_cell = []

    def handle_data(self, data: str) -> None:
        if self._current_cell is not None:
            self._current_cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"td", "th"} and self._current_cell is not None and self._current_row is not None:
            text = " ".join("".join(self._current_cell).split())
            self._current_row.append(text)
            self._current_cell = None
        elif tag == "tr" and self._current_row is not None:
            if any(cell for cell in self._current_row):
                self.rows.append(self._current_row)
            self._current_row = None


_REPORT_NUMBER_RE = re.compile(r"([-+]?\d[\d\s,]*(?:\.\d+)?)(\s*%)?")


def read_text_best_effort(path: Path) -> tuple[str, str]:
    raw = io_path(path).read_bytes()
    for encoding in ("utf-16", "utf-8-sig", "utf-8", "cp949"):
        try:
            text = raw.decode(encoding)
        except UnicodeDecodeError:
            continue
        if encoding == "utf-16" and not raw.startswith((b"\xff\xfe", b"\xfe\xff")) and "<" not in text[:200]:
            continue
        return text, encoding
    return raw.decode("utf-8", errors="ignore"), "utf-8-ignore"


def _report_numbers(value: Any) -> list[tuple[float, bool]]:
    text = str(value or "").replace("\xa0", " ")
    numbers: list[tuple[float, bool]] = []
    for match in _REPORT_NUMBER_RE.finditer(text):
        number_text = match.group(1).replace(" ", "").replace(",", "")
        try:
            numbers.append((float(number_text), bool(match.group(2))))
        except ValueError:
            continue
    return numbers


def parse_report_number(value: Any) -> float | None:
    numbers = _report_numbers(value)
    return numbers[0][0] if numbers else None


def parse_report_count(value: Any) -> int | None:
    number = parse_report_number(value)
    return None if number is None else int(round(number))


def parse_count_percent(value: Any) -> dict[str, Any]:
    numbers = _report_numbers(value)
    count = int(round(numbers[0][0])) if numbers else None
    percent = next((number for number, is_percent in numbers if is_percent), None)
    if percent is None and len(numbers) > 1:
        percent = numbers[1][0]
    return {"count": count, "percent": percent}


def parse_amount_percent(value: Any) -> dict[str, Any]:
    numbers = _report_numbers(value)
    amount = next((number for number, is_percent in numbers if not is_percent), None)
    percent = next((number for number, is_percent in numbers if is_percent), None)
    if amount is None and numbers:
        amount = numbers[0][0]
    if percent is None and len(numbers) > 1:
        percent = numbers[1][0]
    return {"amount": amount, "percent": percent}


def _normalize_report_label(value: Any) -> str:
    return str(value or "").strip().rstrip(":").casefold()


def _cell_after(row: Sequence[str], aliases: Sequence[str]) -> str | None:
    normalized_aliases = {_normalize_report_label(alias) for alias in aliases}
    for index, cell in enumerate(row[:-1]):
        if _normalize_report_label(cell) in normalized_aliases:
            for next_cell in row[index + 1 :]:
                if str(next_cell).strip():
                    return next_cell
    return None


def _first_cell_after(rows: Sequence[Sequence[str]], aliases: Sequence[str]) -> str | None:
    for row in rows:
        value = _cell_after(row, aliases)
        if value is not None:
            return value
    return None


def _first_row_containing(rows: Sequence[Sequence[str]], aliases: Sequence[str]) -> Sequence[str] | None:
    normalized_aliases = {_normalize_report_label(alias) for alias in aliases}
    for row in rows:
        row_labels = {_normalize_report_label(cell) for cell in row}
        if row_labels & normalized_aliases:
            return row
    return None


def extract_mt5_strategy_report_metrics(report_path: Path) -> dict[str, Any]:
    text, encoding = read_text_best_effort(report_path)
    parser = _Mt5ReportTableParser()
    parser.feed(text)
    rows = parser.rows

    metrics: dict[str, Any] = {
        "status": "partial",
        "report_path": report_path.as_posix(),
        "source_encoding": encoding,
        "parsed_row_count": len(rows),
    }

    scalar_fields = {
        "net_profit": ("총수입", "Total Net Profit"),
        "gross_profit": ("누적 수익", "Gross Profit"),
        "gross_loss": ("누적 손실", "Gross Loss"),
        "profit_factor": ("Profit Factor",),
        "expectancy": ("예상 비용", "Expected Payoff"),
        "recovery_factor": ("Recovery Factor",),
        "sharpe_ratio": ("Sharpe Ratio",),
    }
    scalar_fields.update(
        {
            "net_profit": (*scalar_fields["net_profit"], "총 순수익", "총 순 이익", "총손익"),
            "gross_profit": (*scalar_fields["gross_profit"], "총 수익", "총 이익"),
            "gross_loss": (*scalar_fields["gross_loss"], "총 손실"),
            "profit_factor": (*scalar_fields["profit_factor"], "수익 팩터"),
            "expectancy": (*scalar_fields["expectancy"], "기대 수익", "예상 보상"),
            "recovery_factor": (*scalar_fields["recovery_factor"], "회복 계수"),
            "sharpe_ratio": (*scalar_fields["sharpe_ratio"], "샤프 비율"),
        }
    )
    for field, aliases in scalar_fields.items():
        metrics[field] = parse_report_number(_first_cell_after(rows, aliases))

    for field, aliases in {
        "balance_drawdown_maximal": ("Balance Drawdown Maximal",),
        "equity_drawdown_maximal": ("Equity Drawdown Maximal",),
    }.items():
        parsed = parse_amount_percent(_first_cell_after(rows, aliases))
        metrics[f"{field}_amount"] = parsed["amount"]
        metrics[f"{field}_percent"] = parsed["percent"]

    trade_row = _first_row_containing(rows, ("매도거래수 (won %)", "Short Trades (won %)"))
    trade_count_value = _cell_after(trade_row, ("총 거래횟수", "Total Trades")) if trade_row else None
    if metrics.get("balance_drawdown_maximal_amount") is None:
        parsed = parse_amount_percent(
            _first_cell_after(rows, ("잔고 하락폭 최대", "잔고 최대 하락폭", "잔고 드로다운 최대"))
        )
        metrics["balance_drawdown_maximal_amount"] = parsed["amount"]
        metrics["balance_drawdown_maximal_percent"] = parsed["percent"]
    if metrics.get("equity_drawdown_maximal_amount") is None:
        parsed = parse_amount_percent(
            _first_cell_after(
                rows,
                (
                    "평가금 하락폭 최대",
                    "평가금 최대 하락폭",
                    "자본 하락폭 최대",
                    "자본 최대 하락폭",
                    "자본 드로다운 최대",
                ),
            )
        )
        metrics["equity_drawdown_maximal_amount"] = parsed["amount"]
        metrics["equity_drawdown_maximal_percent"] = parsed["percent"]
    if trade_count_value is None and trade_row:
        trade_count_value = _cell_after(trade_row, ("총 거래", "총 거래수"))
    metrics["trade_count"] = parse_report_count(trade_count_value)
    if trade_row is None:
        trade_row = _first_row_containing(rows, ("매도 거래 (승률 %)", "매도 거래 (won %)"))
        trade_count_value = _cell_after(trade_row, ("총 거래", "총 거래수")) if trade_row else None
        metrics["trade_count"] = parse_report_count(trade_count_value)
    if trade_row is not None:
        short = parse_count_percent(_cell_after(trade_row, ("매도거래수 (won %)", "Short Trades (won %)")))
        long = parse_count_percent(_cell_after(trade_row, ("매수거래수 (won %)", "Long Trades (won %)")))
        if short["count"] is None:
            short = parse_count_percent(_cell_after(trade_row, ("매도 거래 (승률 %)", "매도 거래 (won %)")))
        if long["count"] is None:
            long = parse_count_percent(_cell_after(trade_row, ("매수 거래 (승률 %)", "매수 거래 (won %)")))
        metrics["short_trade_count"] = short["count"]
        metrics["short_win_rate_percent"] = short["percent"]
        metrics["long_trade_count"] = long["count"]
        metrics["long_win_rate_percent"] = long["percent"]

    profit_row = _first_row_containing(rows, ("수익거래수 (% of total)", "Profit Trades (% of total)"))
    if profit_row is None:
        profit_row = _first_row_containing(rows, ("수익 거래 (% 총계 중)", "수익 거래 (% of total)"))
    if profit_row is not None:
        deal_count_value = _cell_after(profit_row, ("총 거래횟수", "Total Deals"))
        if deal_count_value is None:
            deal_count_value = _cell_after(profit_row, ("총 딜", "총 거래"))
        metrics["deal_count"] = parse_report_count(deal_count_value)
        winners = parse_count_percent(_cell_after(profit_row, ("수익거래수 (% of total)", "Profit Trades (% of total)")))
        losers = parse_count_percent(_cell_after(profit_row, ("손실거래수 (% of total)", "Loss Trades (% of total)")))
        if winners["count"] is None:
            winners = parse_count_percent(_cell_after(profit_row, ("수익 거래 (% 총계 중)", "수익 거래 (% of total)")))
        if losers["count"] is None:
            losers = parse_count_percent(_cell_after(profit_row, ("손실 거래 (% 총계 중)", "손실 거래 (% of total)")))
        metrics["winning_trade_count"] = winners["count"]
        metrics["win_rate_percent"] = winners["percent"]
        metrics["losing_trade_count"] = losers["count"]
        metrics["loss_rate_percent"] = losers["percent"]

    metrics["max_drawdown_amount"] = (
        metrics.get("equity_drawdown_maximal_amount") or metrics.get("balance_drawdown_maximal_amount")
    )
    metrics["max_drawdown_percent"] = (
        metrics.get("equity_drawdown_maximal_percent") or metrics.get("balance_drawdown_maximal_percent")
    )
    if metrics.get("expectancy") is None and metrics.get("trade_count"):
        metrics["expectancy"] = float(metrics["net_profit"] / metrics["trade_count"]) if metrics.get("net_profit") is not None else None
    if metrics.get("profit_factor") is None and metrics.get("gross_profit") is not None and metrics.get("gross_loss"):
        metrics["profit_factor"] = float(metrics["gross_profit"] / abs(metrics["gross_loss"]))
    if metrics.get("recovery_factor") is None and metrics.get("net_profit") is not None and metrics.get("max_drawdown_amount"):
        metrics["recovery_factor"] = float(metrics["net_profit"] / metrics["max_drawdown_amount"])

    required = [
        "net_profit",
        "profit_factor",
        "expectancy",
        "trade_count",
        "win_rate_percent",
        "max_drawdown_amount",
        "recovery_factor",
    ]
    missing = [field for field in required if metrics.get(field) is None]
    metrics["missing_required_metrics"] = missing
    metrics["status"] = "completed" if not missing else "partial"
    return metrics
