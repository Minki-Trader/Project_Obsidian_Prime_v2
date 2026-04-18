from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

import MetaTrader5 as mt5


UTC = timezone.utc
M5_SECONDS = 5 * 60


@dataclass(frozen=True)
class SymbolBinding:
    contract_symbol: str
    broker_symbol: str


DEFAULT_SYMBOL_BINDINGS: tuple[SymbolBinding, ...] = (
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
    parser = argparse.ArgumentParser(
        description="Export FPMarkets v2 raw M5 bars from the connected MetaTrader 5 terminal."
    )
    parser.add_argument(
        "--output-root",
        default="data/raw/mt5_bars/m5",
        help="Repo-relative output root for raw M5 bar exports.",
    )
    parser.add_argument(
        "--start-utc",
        default="2022-08-01T00:00:00Z",
        help="Inclusive UTC start for M5 bar opens.",
    )
    parser.add_argument(
        "--end-utc",
        default="2026-04-13T23:55:00Z",
        help="Inclusive UTC end for M5 bar opens.",
    )
    parser.add_argument(
        "--price-basis",
        default="Bid",
        help="Price basis label to write into the CSV manifest fields.",
    )
    return parser.parse_args()


def parse_utc_timestamp(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(f"UTC timestamp must be timezone-aware: {value}")
    return parsed.astimezone(UTC)


def normalize_file_token(value: str) -> str:
    return value.lower().replace(".", "_")


def ensure_symbol_selected(symbol: str) -> None:
    info = mt5.symbol_info(symbol)
    if info is None:
        raise RuntimeError(f"Symbol not found in terminal: {symbol}")
    if not info.visible and not mt5.symbol_select(symbol, True):
        raise RuntimeError(f"Failed to select symbol in Market Watch: {symbol}")


def write_csv(csv_path: Path, binding: SymbolBinding, rates, price_basis: str) -> None:
    fieldnames = [
        "time_open_unix",
        "time_close_unix",
        "contract_symbol",
        "broker_symbol",
        "timeframe",
        "price_basis",
        "open",
        "high",
        "low",
        "close",
        "tick_volume",
        "spread_points",
        "real_volume",
        "time_basis",
        "timezone_status",
    ]
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rates:
            time_open_unix = int(row["time"])
            writer.writerow(
                {
                    "time_open_unix": time_open_unix,
                    "time_close_unix": time_open_unix + M5_SECONDS,
                    "contract_symbol": binding.contract_symbol,
                    "broker_symbol": binding.broker_symbol,
                    "timeframe": "M5",
                    "price_basis": price_basis,
                    "open": row["open"],
                    "high": row["high"],
                    "low": row["low"],
                    "close": row["close"],
                    "tick_volume": int(row["tick_volume"]),
                    "spread_points": int(row["spread"]),
                    "real_volume": int(row["real_volume"]),
                    "time_basis": "MT5_PY_API_UNIX_SECONDS",
                    "timezone_status": "UNRESOLVED_REQUIRES_MANUAL_BINDING",
                }
            )


def write_manifest(
    manifest_path: Path,
    binding: SymbolBinding,
    csv_path: Path,
    rates,
    requested_from_utc: datetime,
    requested_to_utc: datetime,
    price_basis: str,
) -> None:
    first_open_unix = int(rates[0]["time"])
    last_open_unix = int(rates[-1]["time"])
    last_close_unix = last_open_unix + M5_SECONDS
    terminal = mt5.terminal_info()
    payload = {
        "manifest_version": "FPMARKETS_V2_STAGE01_RAW_BAR_EXPORT_V1",
        "export_status": "COMPLETE",
        "terminal_path": terminal.path if terminal else None,
        "terminal_data_path": terminal.data_path if terminal else None,
        "contract_symbol": binding.contract_symbol,
        "broker_symbol": binding.broker_symbol,
        "timeframe": "M5",
        "requested_from_utc": requested_from_utc.isoformat().replace("+00:00", "Z"),
        "requested_to_utc": requested_to_utc.isoformat().replace("+00:00", "Z"),
        "resolved_first_open_unix": first_open_unix,
        "resolved_last_open_unix": last_open_unix,
        "resolved_last_close_unix": last_close_unix,
        "row_count": len(rates),
        "csv_file": str(csv_path.resolve()),
        "time_basis": "MT5_PY_API_UNIX_SECONDS",
        "source_timezone": "OPEN",
        "calendar_id": "OPEN",
        "timezone_status": "UNRESOLVED_REQUIRES_MANUAL_BINDING",
        "bar_open_column": "time_open_unix",
        "bar_close_column": "time_close_unix",
        "price_basis": price_basis,
        "generated_at_utc": datetime.now(tz=UTC).isoformat().replace("+00:00", "Z"),
        "note": (
            "Raw export produced directly from MetaTrader5.copy_rates_range for "
            "Project Obsidian Prime v2 Stage 01. Timezone/calendar stay OPEN until "
            "manually bound in the dataset-contract pipeline."
        ),
    }
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_summary(
    summary_path: Path,
    rows: list[dict[str, object]],
    requested_from_utc: datetime,
    requested_to_utc: datetime,
) -> None:
    payload = {
        "summary_version": "FPMARKETS_V2_STAGE01_RAW_BAR_EXPORT_SUMMARY_V1",
        "requested_from_utc": requested_from_utc.isoformat().replace("+00:00", "Z"),
        "requested_to_utc": requested_to_utc.isoformat().replace("+00:00", "Z"),
        "exported_symbols": rows,
        "generated_at_utc": datetime.now(tz=UTC).isoformat().replace("+00:00", "Z"),
    }
    summary_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def export_symbol(
    output_root: Path,
    binding: SymbolBinding,
    requested_from_utc: datetime,
    requested_to_utc: datetime,
    price_basis: str,
) -> dict[str, object]:
    ensure_symbol_selected(binding.broker_symbol)
    rates = mt5.copy_rates_range(
        binding.broker_symbol,
        mt5.TIMEFRAME_M5,
        requested_from_utc,
        requested_to_utc,
    )
    if rates is None:
        raise RuntimeError(f"MT5 copy_rates_range failed for {binding.broker_symbol}: {mt5.last_error()}")
    if len(rates) == 0:
        raise RuntimeError(f"No M5 bars returned for {binding.broker_symbol} in the requested window.")

    symbol_root = output_root / binding.contract_symbol
    file_token = normalize_file_token(binding.broker_symbol)
    csv_path = symbol_root / f"bars_{file_token}_m5_mt5api_raw.csv"
    manifest_path = symbol_root / f"bars_{file_token}_m5_mt5api_raw.manifest.json"

    write_csv(csv_path, binding, rates, price_basis)
    write_manifest(manifest_path, binding, csv_path, rates, requested_from_utc, requested_to_utc, price_basis)

    first_open_unix = int(rates[0]["time"])
    last_open_unix = int(rates[-1]["time"])
    return {
        "contract_symbol": binding.contract_symbol,
        "broker_symbol": binding.broker_symbol,
        "row_count": len(rates),
        "csv_path": str(csv_path.resolve()),
        "manifest_path": str(manifest_path.resolve()),
        "first_open_unix": first_open_unix,
        "last_open_unix": last_open_unix,
    }


def export_all(
    output_root: Path,
    symbol_bindings: Iterable[SymbolBinding],
    requested_from_utc: datetime,
    requested_to_utc: datetime,
    price_basis: str,
) -> list[dict[str, object]]:
    exported: list[dict[str, object]] = []
    for binding in symbol_bindings:
        exported.append(
            export_symbol(
                output_root=output_root,
                binding=binding,
                requested_from_utc=requested_from_utc,
                requested_to_utc=requested_to_utc,
                price_basis=price_basis,
            )
        )
    return exported


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    requested_from_utc = parse_utc_timestamp(args.start_utc)
    requested_to_utc = parse_utc_timestamp(args.end_utc)
    if requested_to_utc <= requested_from_utc:
        raise ValueError("end-utc must be later than start-utc")

    if not mt5.initialize():
        raise RuntimeError(f"Failed to initialize MetaTrader5: {mt5.last_error()}")

    try:
        exported = export_all(
            output_root=output_root,
            symbol_bindings=DEFAULT_SYMBOL_BINDINGS,
            requested_from_utc=requested_from_utc,
            requested_to_utc=requested_to_utc,
            price_basis=args.price_basis,
        )
        summary_path = output_root / "stage01_raw_export_summary.json"
        write_summary(summary_path, exported, requested_from_utc, requested_to_utc)
        print(json.dumps({"status": "ok", "exported_symbols": exported, "summary_path": str(summary_path.resolve())}, indent=2))
        return 0
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
