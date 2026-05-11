from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, ledger_pairs, sha256_file_lf_normalized
from foundation.control_plane.mt5_trade_attribution import MarketData, compute_trade_attribution
from foundation.mt5.runtime_artifacts import write_json
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN_ID = "run50C_d38h10_logreg_dense_v1"
VARIANT_ID = "d38h10"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / "run50C" / VARIANT_ID
REPORT_ROOT = RUN_ROOT / "mt5" / "reports"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
ATTRIBUTION_CSV_PATH = REVIEWS_ROOT / "stage56_market_weather_attribution.csv"
TRADE_RECORDS_CSV_PATH = REVIEWS_ROOT / "stage56_d38h10_trade_weather_records.csv"
REPORT_PATH = REVIEWS_ROOT / "stage56_market_weather_attribution.md"
SUMMARY_PATH = REVIEWS_ROOT / "stage56_market_weather_attribution_summary.json"

AXES = ("session_slice", "volatility_regime", "trend_regime", "adx_bucket", "spread_regime")
SPLIT_REPORTS = {
    "validation": REPORT_ROOT / f"Project_Obsidian_Prime_v2_{RUN_ID}_routed_validation_is.htm",
    "oos": REPORT_ROOT / f"Project_Obsidian_Prime_v2_{RUN_ID}_routed_oos.htm",
}

ATTRIBUTION_COLUMNS = (
    "run_id",
    "variant_id",
    "split",
    "axis",
    "bucket",
    "trade_count",
    "net_profit",
    "trade_share",
    "profit_per_trade",
)

TRADE_COLUMNS = (
    "run_id",
    "variant_id",
    "split",
    "trade_index",
    "direction",
    "open_time",
    "close_time",
    "hold_bars",
    "net_profit",
    "session_slice",
    "volatility_regime",
    "trend_regime",
    "adx_bucket",
    "spread_regime",
)


def _write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def _round(value: Any, digits: int = 6) -> Any:
    if isinstance(value, (int, float)):
        return round(float(value), digits)
    return value


def _attribution_rows(stats_by_split: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, stats in stats_by_split.items():
        trade_count = int(stats.get("trade_count") or 0)
        regimes = stats.get("regime_slice_attribution", {})
        for axis in AXES:
            axis_payload = regimes.get(axis, {}) if isinstance(regimes, Mapping) else {}
            if not isinstance(axis_payload, Mapping):
                continue
            for bucket, payload in axis_payload.items():
                if not isinstance(payload, Mapping):
                    continue
                bucket_trades = int(payload.get("trade_count") or 0)
                net_profit = float(payload.get("net_profit") or 0.0)
                rows.append(
                    {
                        "run_id": RUN_ID,
                        "variant_id": VARIANT_ID,
                        "split": split,
                        "axis": axis,
                        "bucket": bucket,
                        "trade_count": bucket_trades,
                        "net_profit": _round(net_profit, 6),
                        "trade_share": _round(bucket_trades / trade_count if trade_count else 0.0, 6),
                        "profit_per_trade": _round(net_profit / bucket_trades if bucket_trades else 0.0, 6),
                    }
                )
    return rows


def _trade_rows(stats_by_split: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, stats in stats_by_split.items():
        for trade in stats.get("trades", []):
            rows.append(
                {
                    "run_id": RUN_ID,
                    "variant_id": VARIANT_ID,
                    "split": split,
                    "trade_index": trade.get("trade_index"),
                    "direction": trade.get("direction"),
                    "open_time": trade.get("open_time").strftime("%Y-%m-%d %H:%M:%S") if trade.get("open_time") is not None else "",
                    "close_time": trade.get("close_time").strftime("%Y-%m-%d %H:%M:%S") if trade.get("close_time") is not None else "",
                    "hold_bars": _round(trade.get("hold_bars"), 6),
                    "net_profit": _round(trade.get("net_profit"), 6),
                    "session_slice": trade.get("session_slice"),
                    "volatility_regime": trade.get("volatility_regime"),
                    "trend_regime": trade.get("trend_regime"),
                    "adx_bucket": trade.get("adx_bucket"),
                    "spread_regime": trade.get("spread_regime"),
                }
            )
    return rows


def _top_rows(rows: Sequence[Mapping[str, Any]], *, split: str, axis: str, reverse: bool) -> list[Mapping[str, Any]]:
    filtered = [row for row in rows if row.get("split") == split and row.get("axis") == axis]
    return sorted(filtered, key=lambda row: float(row.get("net_profit") or 0.0), reverse=reverse)[:3]


def _write_report(rows: Sequence[Mapping[str, Any]], stats_by_split: Mapping[str, Mapping[str, Any]]) -> None:
    lines = [
        "# Stage56 Market-Weather Attribution(56단계 시장 상태 귀속)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- variant_id(변형 ID): `{VARIANT_ID}`",
        "- source(원천): MT5 strategy tester(전략 테스터) routed report(라우팅 보고서) deal list(거래 목록)",
        "- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`",
        "",
        "## Split Summary(분할 요약)",
        "",
        "| split(분할) | trades(거래) | net(순손익) | positive_month_ratio(양수 월 비율) | avg_hold_bars(평균 보유 봉) |",
        "|---|---:|---:|---:|---:|",
    ]
    for split, stats in stats_by_split.items():
        diagnostics = stats.get("trade_diagnostics", {})
        regimes = stats.get("regime_slice_attribution", {})
        consistency = regimes.get("subperiod_consistency", {}) if isinstance(regimes, Mapping) else {}
        net = sum(float(trade.get("net_profit") or 0.0) for trade in stats.get("trades", []))
        lines.append(
            "| {split} | {trades} | {net:.2f} | {pmr} | {avg} |".format(
                split=split,
                trades=stats.get("trade_count"),
                net=net,
                pmr=consistency.get("positive_month_ratio"),
                avg=diagnostics.get("avg_hold_bars"),
            )
        )
    lines.extend(
        [
            "",
            "## Key Attribution(핵심 귀속)",
            "",
        ]
    )
    for split in ("validation", "oos"):
        lines.append(f"### {split}")
        for axis in AXES:
            top = _top_rows(rows, split=split, axis=axis, reverse=True)
            bottom = _top_rows(rows, split=split, axis=axis, reverse=False)
            top_text = ", ".join(f"{row.get('bucket')} {row.get('net_profit')}" for row in top) or "none"
            bottom_text = ", ".join(f"{row.get('bucket')} {row.get('net_profit')}" for row in bottom) or "none"
            lines.append(f"- {axis}: best(최상) `{top_text}` / worst(최악) `{bottom_text}`")
        lines.append("")
    lines.extend(
        [
            "## Read(판독)",
            "",
            "- 이 귀속은 hard filter(강제 필터)가 아니라 explanation table(설명 표)이다.",
            "- 효과(effect, 효과): d38h10 후보가 어느 시장 상태에서 손익을 만들거나 잃는지 설명하지만, Stage56(56단계) 안에서 새 운영 필터를 만들지는 않는다.",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8-sig")


def build_attribution() -> dict[str, Any]:
    market_data = MarketData.load(REPO_ROOT)
    stats_by_split: dict[str, dict[str, Any]] = {}
    parser_errors: list[dict[str, Any]] = []
    for split, report_path in SPLIT_REPORTS.items():
        try:
            report = parse_mt5_trade_report(report_path)
            trades = pair_deals_into_trades(report["deals"])
            stats_by_split[split] = compute_trade_attribution(trades, market_data)
        except Exception as exc:
            parser_errors.append({"split": split, "report_path": report_path.as_posix(), "error": str(exc)})
    rows = _attribution_rows(stats_by_split)
    trades = _trade_rows(stats_by_split)
    _write_csv(ATTRIBUTION_CSV_PATH, ATTRIBUTION_COLUMNS, rows)
    _write_csv(TRADE_RECORDS_CSV_PATH, TRADE_COLUMNS, trades)
    _write_report(rows, stats_by_split)
    summary = {
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "variant_id": VARIANT_ID,
        "status": "completed" if not parser_errors and stats_by_split else "partial_or_blocked",
        "parser_errors": parser_errors,
        "split_trade_counts": {split: stats.get("trade_count") for split, stats in stats_by_split.items()},
        "artifacts": {
            "attribution_csv": ATTRIBUTION_CSV_PATH.as_posix(),
            "trade_records_csv": TRADE_RECORDS_CSV_PATH.as_posix(),
            "report_path": REPORT_PATH.as_posix(),
        },
        "hashes": {
            "attribution_csv_sha256": sha256_file_lf_normalized(ATTRIBUTION_CSV_PATH),
            "trade_records_csv_sha256": sha256_file_lf_normalized(TRADE_RECORDS_CSV_PATH),
            "report_sha256": sha256_file_lf_normalized(REPORT_PATH),
        },
        "boundary": "research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference",
        "notes": ledger_pairs(
            (
                ("source", "mt5_strategy_tester_deal_list"),
                ("market_weather_role", "attribution_only"),
                ("hard_filter_created", False),
            )
        ),
    }
    write_json(SUMMARY_PATH, summary)
    return summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage56 market-weather attribution for d38h10.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    parse_args(argv)
    print(json.dumps(build_attribution(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
