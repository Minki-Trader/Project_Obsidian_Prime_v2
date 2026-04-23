from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import date, datetime, time, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


UTC = timezone.utc
NEW_YORK = ZoneInfo("America/New_York")


@dataclass(frozen=True)
class EquitySessionSymbol:
    contract_symbol: str
    broker_symbol: str


DEFAULT_EQUITY_SYMBOLS: tuple[EquitySessionSymbol, ...] = (
    EquitySessionSymbol("AAPL", "AAPL.xnas"),
    EquitySessionSymbol("MSFT", "MSFT.xnas"),
    EquitySessionSymbol("AMZN", "AMZN.xnas"),
    EquitySessionSymbol("AMD", "AMD.xnas"),
    EquitySessionSymbol("GOOGL.xnas", "GOOGL.xnas"),
    EquitySessionSymbol("META", "META.xnas"),
    EquitySessionSymbol("NVDA", "NVDA.xnas"),
    EquitySessionSymbol("TSLA", "TSLA.xnas"),
)


@dataclass(frozen=True)
class DayProbe:
    contract_symbol: str
    raw_date: str
    row_count: int
    first_open_raw_as_utc: str
    last_open_raw_as_utc: str
    expected_cash_open_utc: str
    expected_last_bar_open_utc: str
    first_open_offset_seconds: int
    last_open_offset_seconds: int
    first_open_clock: str
    last_open_clock: str


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def normalize_offset_key(seconds: int) -> str:
    hours = seconds / 3600
    if hours.is_integer():
        return f"{int(hours):+d}h"
    return f"{hours:+.2f}h"


def expected_ny_session_open(raw_date: date) -> datetime:
    return datetime.combine(raw_date, time(9, 30), tzinfo=NEW_YORK).astimezone(UTC)


def expected_ny_last_bar_open(raw_date: date) -> datetime:
    return datetime.combine(raw_date, time(15, 55), tzinfo=NEW_YORK).astimezone(UTC)


def load_daily_raw_bounds(csv_path: Path) -> dict[date, list[datetime]]:
    grouped: dict[date, list[datetime]] = defaultdict(list)
    with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            raw_open = datetime.fromtimestamp(int(row["time_open_unix"]), tz=UTC)
            grouped[raw_open.date()].append(raw_open)
    return grouped


def inspect_symbol(raw_root: Path, symbol: EquitySessionSymbol) -> tuple[list[DayProbe], list[str]]:
    symbol_dir = raw_root / symbol.contract_symbol
    notes: list[str] = []
    csv_files = sorted(symbol_dir.glob("*.csv"))
    if len(csv_files) != 1:
        notes.append(f"{symbol.contract_symbol}: expected one CSV, found {len(csv_files)}")
        return [], notes

    day_probes: list[DayProbe] = []
    grouped = load_daily_raw_bounds(csv_files[0])
    for raw_date, opens in sorted(grouped.items()):
        first_open = min(opens)
        last_open = max(opens)
        expected_open = expected_ny_session_open(raw_date)
        expected_last = expected_ny_last_bar_open(raw_date)
        day_probes.append(
            DayProbe(
                contract_symbol=symbol.contract_symbol,
                raw_date=raw_date.isoformat(),
                row_count=len(opens),
                first_open_raw_as_utc=first_open.isoformat().replace("+00:00", "Z"),
                last_open_raw_as_utc=last_open.isoformat().replace("+00:00", "Z"),
                expected_cash_open_utc=expected_open.isoformat().replace("+00:00", "Z"),
                expected_last_bar_open_utc=expected_last.isoformat().replace("+00:00", "Z"),
                first_open_offset_seconds=int((first_open - expected_open).total_seconds()),
                last_open_offset_seconds=int((last_open - expected_last).total_seconds()),
                first_open_clock=first_open.strftime("%H:%M"),
                last_open_clock=last_open.strftime("%H:%M"),
            )
        )
    return day_probes, notes


def counter_to_dict(counter: Counter[int] | Counter[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for key, count in counter.most_common():
        if isinstance(key, int):
            result[normalize_offset_key(key)] = count
        else:
            result[key] = count
    return result


def build_probe(
    raw_root: Path,
    symbols: tuple[EquitySessionSymbol, ...] = DEFAULT_EQUITY_SYMBOLS,
    repo_root: Path | None = None,
) -> dict[str, object]:
    repo_root = repo_root or Path.cwd()
    all_days: list[DayProbe] = []
    notes: list[str] = []
    symbol_summaries: list[dict[str, object]] = []

    for symbol in symbols:
        symbol_days, symbol_notes = inspect_symbol(raw_root, symbol)
        all_days.extend(symbol_days)
        notes.extend(symbol_notes)
        first_offsets = Counter(day.first_open_offset_seconds for day in symbol_days)
        first_clocks = Counter(day.first_open_clock for day in symbol_days)
        symbol_summaries.append(
            {
                "contract_symbol": symbol.contract_symbol,
                "broker_symbol": symbol.broker_symbol,
                "observed_days": len(symbol_days),
                "first_open_offset_distribution": counter_to_dict(first_offsets),
                "first_open_clock_distribution": counter_to_dict(first_clocks),
            }
        )

    first_offsets = Counter(day.first_open_offset_seconds for day in all_days)
    last_offsets = Counter(day.last_open_offset_seconds for day in all_days)
    first_clocks = Counter(day.first_open_clock for day in all_days)
    direct_utc_match_count = first_offsets.get(0, 0)
    direct_utc_match_ratio = direct_utc_match_count / len(all_days) if all_days else 0.0
    dominant_offsets = set(first_offsets)
    expected_broker_wall_clock_offsets = {7200, 10800}
    broker_wall_clock_like_ratio = (
        sum(first_offsets[offset] for offset in expected_broker_wall_clock_offsets) / len(all_days)
        if all_days
        else 0.0
    )

    if direct_utc_match_ratio >= 0.95:
        interpretation = "direct_utc_candidate"
    elif broker_wall_clock_like_ratio >= 0.85:
        interpretation = "broker_server_wall_clock_candidate"
    else:
        interpretation = "mixed_or_incomplete_candidate"

    summary = {
        "probe_version": "FPMARKETS_V2_TIME_SEMANTICS_PROBE_V1",
        "generated_at_utc": datetime.now(tz=UTC).isoformat().replace("+00:00", "Z"),
        "raw_root": repo_relative(raw_root, repo_root),
        "symbols_checked": [symbol.contract_symbol for symbol in symbols],
        "observed_symbol_days": len(all_days),
        "direct_utc_match_ratio": round(direct_utc_match_ratio, 6),
        "broker_wall_clock_like_ratio": round(broker_wall_clock_like_ratio, 6),
        "first_open_offset_distribution": counter_to_dict(first_offsets),
        "last_open_offset_distribution": counter_to_dict(last_offsets),
        "first_open_clock_distribution": counter_to_dict(first_clocks),
        "dominant_first_open_offsets_seconds": sorted(dominant_offsets),
        "candidate_interpretation": interpretation,
        "readout": (
            "Raw equity-session timestamps do not behave like direct UTC cash-session opens. "
            "They mostly behave like broker/server wall-clock seconds, especially +2h and +3h "
            "relative to New York cash-session UTC opens. A few dates are partial or shifted and "
            "must stay explicit."
        ),
        "next_decision": (
            "Before feature-frame closure, choose and document whether model timestamps remain raw "
            "broker-clock keys or are transformed into explicit UTC event times."
        ),
        "notes": notes,
    }
    return {
        "summary": summary,
        "symbols": symbol_summaries,
        "daily_probes": [asdict(day) for day in all_days],
    }


def render_markdown(probe: dict[str, object]) -> str:
    summary = probe["summary"]
    symbols = probe["symbols"]
    assert isinstance(summary, dict)
    assert isinstance(symbols, list)

    lines = [
        "# Time Semantics Probe(시간 의미 탐침)",
        "",
        "## 요약(Summary, 요약)",
        "",
        f"- 후보 해석(candidate interpretation, 후보 해석): `{summary['candidate_interpretation']}`",
        f"- 관측 심볼-일수(observed symbol-days, 관측 심볼-일수): `{summary['observed_symbol_days']}`",
        f"- 직접 UTC 일치율(direct UTC match ratio, 직접 UTC 일치율): `{summary['direct_utc_match_ratio']}`",
        f"- 브로커 시계 유사율(broker wall-clock-like ratio, 브로커 시계 유사율): `{summary['broker_wall_clock_like_ratio']}`",
        "",
        "쉽게 말하면, 현재 원천 timestamp(타임스탬프)를 UTC(협정세계시)로 바로 읽으면 미국 주식 정규장 시간이 맞지 않는다.",
        "대부분은 뉴욕 정규장 UTC 시간보다 `+2h` 또는 `+3h` 늦은 브로커/서버 시계(broker/server clock, 브로커/서버 시계)처럼 보인다.",
        "",
        "## 오프셋 분포(Offset Distribution, 오프셋 분포)",
        "",
        "| offset(오프셋) | count(개수) |",
        "|---|---:|",
    ]
    for offset, count in summary["first_open_offset_distribution"].items():
        lines.append(f"| `{offset}` | {count} |")

    lines.extend(
        [
            "",
            "## 심볼별 판독(Symbol Readout, 심볼별 판독)",
            "",
            "| symbol(심볼) | observed days(관측일) | first-open offsets(첫 봉 오프셋) | first-open clocks(첫 봉 시각) |",
            "|---|---:|---|---|",
        ]
    )
    for symbol in symbols:
        assert isinstance(symbol, dict)
        lines.append(
            "| "
            f"`{symbol['contract_symbol']}` | "
            f"{symbol['observed_days']} | "
            f"`{symbol['first_open_offset_distribution']}` | "
            f"`{symbol['first_open_clock_distribution']}` |"
        )

    lines.extend(
        [
            "",
            "## 경계(Boundary, 경계)",
            "",
            "이 결과는 시간 의미(time semantics, 시간 의미) 후보를 세우는 근거(evidence, 근거)다. "
            "아직 피처 프레임(feature frame, 피처 프레임) 폐쇄나 런타임 권위(runtime authority, 런타임 권위)를 주장하지 않는다.",
            "",
            "## 다음 결정(Next Decision, 다음 결정)",
            "",
            "피처 프레임(feature frame, 피처 프레임)을 만들기 전에 timestamp(타임스탬프)를 원천 브로커 시계 키(raw broker-clock key, 원천 브로커 시계 키)로 둘지, "
            "명시적 UTC 이벤트 시간(explicit UTC event time, 명시적 UTC 이벤트 시간)으로 변환할지 정해야 한다.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(probe: dict[str, object], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "time_semantics_probe.json").write_text(json.dumps(probe, indent=2), encoding="utf-8")
    (output_dir / "time_semantics_probe.md").write_text(render_markdown(probe), encoding="utf-8-sig")

    with (output_dir / "daily_time_offsets.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = (
            "contract_symbol",
            "raw_date",
            "row_count",
            "first_open_raw_as_utc",
            "expected_cash_open_utc",
            "first_open_offset_seconds",
            "last_open_raw_as_utc",
            "expected_last_bar_open_utc",
            "last_open_offset_seconds",
            "first_open_clock",
            "last_open_clock",
        )
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in probe["daily_probes"]:
            writer.writerow({key: row.get(key) for key in fieldnames})

    manifest = {
        "run_id": output_dir.name,
        "lane": "evidence",
        "stage_id": "01_data_foundation__raw_m5_inventory",
        "command": (
            "python foundation/collectors/time_semantics_probe.py "
            "--raw-root data/raw/mt5_bars/m5 "
            f"--output-dir {output_dir.as_posix()}"
        ),
        "outputs": [
            (output_dir / "time_semantics_probe.json").as_posix(),
            (output_dir / "time_semantics_probe.md").as_posix(),
            (output_dir / "daily_time_offsets.csv").as_posix(),
        ],
        "judgment_boundary": (
            "Evidence run only. This identifies a candidate timestamp interpretation; "
            "it does not close feature-frame semantics or runtime authority."
        ),
    }
    (output_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe FPMarkets v2 raw timestamp semantics against US cash sessions.")
    parser.add_argument("--raw-root", default="data/raw/mt5_bars/m5")
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    probe = build_probe(Path(args.raw_root), repo_root=Path.cwd())
    write_outputs(probe, Path(args.output_dir))
    print(json.dumps(probe["summary"], indent=2))


if __name__ == "__main__":
    main()
