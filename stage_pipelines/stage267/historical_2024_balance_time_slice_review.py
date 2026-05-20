from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_trade_attribution import MarketData, compute_trade_attribution
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe


STAGE_ID = input_probe.STAGE_ID
RUN_ID = input_probe.RUN_ID
HIST_ROOT = input_probe.HIST_ROOT
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY
STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH

EXECUTION_RESULT_PATH = HIST_ROOT / "execution_result.json"
TRADE_RECORDS_PATH = HIST_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = HIST_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = HIST_ROOT / "balance_curve_diagnostics.csv"
CANDIDATE_WEAKNESS_PATH = HIST_ROOT / "candidate_weakness_summary.csv"
REVIEW_RESULT_PATH = HIST_ROOT / "balance_time_slice_review.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_historical_2024_balance_time_slice_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/historical_2024_balance_time_slice_review.py")

DEPOSIT = 500.0
AXES = (
    "month",
    "weekday",
    "close_hour_utc",
    "direction",
    "session_slice",
    "chron_segment",
    "trend_regime",
    "adx_bucket",
    "volatility_regime",
    "spread_regime",
)
CANDIDATE_ROLES = {
    "s264_allow_inner_high_quarter": "core_challenger",
    "s264_lowrank_control": "defensive_control",
    "s262_lowrank_inner_half_filter": "validation_heavy",
    "s264_allow_inner_all_oos_anchor": "oos_anchor",
    "s258_short_tight_control": "stress_challenger",
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    return value


def fnum(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def profit_factor(rows: Sequence[Mapping[str, Any]]) -> float | None:
    wins = sum(float(row.get("net_profit") or 0.0) for row in rows if float(row.get("net_profit") or 0.0) > 0.0)
    losses = -sum(float(row.get("net_profit") or 0.0) for row in rows if float(row.get("net_profit") or 0.0) < 0.0)
    if losses == 0.0:
        return math.inf if wins > 0.0 else None
    return wins / losses


def max_closed_balance_drawdown(rows: Sequence[Mapping[str, Any]]) -> tuple[float, float, int, int]:
    balance = DEPOSIT
    peak = DEPOSIT
    max_dd = 0.0
    max_dd_pct = 0.0
    underwater = 0
    longest_underwater = 0
    underwater_trade_count = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        balance += float(row.get("net_profit") or 0.0)
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            underwater_trade_count += 1
            longest_underwater = max(longest_underwater, underwater)
        dd = peak - balance
        dd_pct = dd / peak * 100.0 if peak else 0.0
        max_dd = max(max_dd, dd)
        max_dd_pct = max(max_dd_pct, dd_pct)
    return max_dd, max_dd_pct, longest_underwater, underwater_trade_count


def max_losing_streak(rows: Sequence[Mapping[str, Any]]) -> int:
    current = 0
    worst = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        if float(row.get("net_profit") or 0.0) < 0.0:
            current += 1
            worst = max(worst, current)
        else:
            current = 0
    return worst


def chronological_segment(index: int, total: int) -> str:
    if total <= 0:
        return "none"
    third = (total + 2) // 3
    if index < third:
        return "chron_early"
    if index < third * 2:
        return "chron_mid"
    return "chron_late"


def metrics(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda item: str(item.get("close_time")))
    trade_count = len(ordered)
    net = sum(float(row.get("net_profit") or 0.0) for row in ordered)
    wins = sum(1 for row in ordered if float(row.get("net_profit") or 0.0) > 0.0)
    gross_profit = sum(float(row.get("net_profit") or 0.0) for row in ordered if float(row.get("net_profit") or 0.0) > 0.0)
    gross_loss = sum(float(row.get("net_profit") or 0.0) for row in ordered if float(row.get("net_profit") or 0.0) < 0.0)
    max_dd, max_dd_pct, longest_underwater, underwater_trade_count = max_closed_balance_drawdown(ordered)
    return {
        "trade_count": trade_count,
        "net_profit": net,
        "profit_factor": profit_factor(ordered),
        "expectancy": net / trade_count if trade_count else None,
        "win_rate": wins / trade_count if trade_count else None,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "closed_balance_max_drawdown": max_dd,
        "closed_balance_max_drawdown_percent": max_dd_pct,
        "longest_underwater_trades": longest_underwater,
        "underwater_trade_share": underwater_trade_count / trade_count if trade_count else None,
        "max_losing_streak": max_losing_streak(ordered),
    }


def metric_row(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    item = metrics(rows)
    return {
        "trade_count": item["trade_count"],
        "net_profit": item["net_profit"],
        "profit_factor": item["profit_factor"],
        "expectancy": item["expectancy"],
        "win_rate": item["win_rate"],
        "closed_balance_max_drawdown": item["closed_balance_max_drawdown"],
        "closed_balance_max_drawdown_percent": item["closed_balance_max_drawdown_percent"],
        "max_losing_streak": item["max_losing_streak"],
    }


def read_attempts(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(item.get("attempt_name")): item for item in execution_result.get("attempts_executed", [])}


def report_records(execution_result: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [item for item in execution_result.get("mt5_kpi_records", []) if item.get("status") == "completed"]


def build_trade_records(execution_result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    market_data = MarketData.load(REPO_ROOT)
    attempts = read_attempts(execution_result)
    trade_rows: list[dict[str, Any]] = []
    parser_errors: list[dict[str, Any]] = []
    for record in report_records(execution_result):
        report = record.get("report", {})
        attempt_name = str(report.get("attempt_name") or "")
        attempt = attempts.get(attempt_name, {})
        html_path = Path(str(record.get("metrics", {}).get("report_path") or report.get("html_report", {}).get("path") or ""))
        if not html_path.is_absolute():
            html_path = REPO_ROOT / html_path
        try:
            parsed = parse_mt5_trade_report(html_path)
            trades = pair_deals_into_trades(parsed["deals"])
            attribution = compute_trade_attribution(trades, market_data)
        except Exception as exc:
            parser_errors.append({"attempt_name": attempt_name, "report_path": rel(html_path), "error": str(exc)})
            continue
        enriched = sorted(attribution["trades"], key=lambda row: row["close_time"])
        total = len(enriched)
        for index, trade in enumerate(enriched):
            close_time = trade.get("close_time")
            open_time = trade.get("open_time")
            row = {
                "run_id": RUN_ID,
                "record_view": record.get("record_view"),
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": CANDIDATE_ROLES.get(str(attempt.get("candidate_id")), ""),
                "attempt_name": attempt_name,
                "tier_scope": record.get("tier_scope"),
                "route_role": record.get("route_role"),
                "split": record.get("split"),
                "trade_index": trade.get("trade_index"),
                "direction": trade.get("direction"),
                "open_time": open_time.strftime("%Y-%m-%d %H:%M:%S") if open_time is not None else "",
                "close_time": close_time.strftime("%Y-%m-%d %H:%M:%S") if close_time is not None else "",
                "month": close_time.strftime("%Y-%m") if close_time is not None else "",
                "weekday": close_time.strftime("%A") if close_time is not None else "",
                "close_hour_utc": close_time.strftime("%H") if close_time is not None else "",
                "chron_segment": chronological_segment(index, total),
                "hold_bars": trade.get("hold_bars"),
                "volume": trade.get("volume"),
                "open_price": trade.get("open_price"),
                "close_price": trade.get("close_price"),
                "gross_profit": trade.get("gross_profit"),
                "net_profit": trade.get("net_profit"),
                "swap": trade.get("swap"),
                "commission": trade.get("commission"),
                "mfe": trade.get("mfe"),
                "mae": trade.get("mae"),
                "realized_over_mfe": trade.get("realized_over_mfe"),
                "session_slice": trade.get("session_slice"),
                "volatility_regime": trade.get("volatility_regime"),
                "trend_regime": trade.get("trend_regime"),
                "adx_bucket": trade.get("adx_bucket"),
                "spread_regime": trade.get("spread_regime"),
                "source_report_path": rel(html_path),
                "source_chart_path": report.get("chart", {}).get("path", ""),
            }
            trade_rows.append(row)
    return trade_rows, parser_errors


def grouped_rows(rows: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(str(row.get(key) or "") for key in keys)].append(row)
    output = []
    for key_values, group in sorted(grouped.items()):
        result = {key: key_values[index] for index, key in enumerate(keys)}
        result.update(metric_row(group))
        output.append(result)
    return output


def build_time_slice_rows(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base_keys = ("candidate_id", "candidate_alias", "candidate_role", "record_view", "tier_scope", "route_role")
    for axis in AXES:
        for row in grouped_rows(trade_rows, (*base_keys, axis)):
            row["axis"] = axis
            row["bucket"] = row.pop(axis)
            row["slice_read"] = slice_read(row)
            rows.append(row)
    return rows


def slice_read(row: Mapping[str, Any]) -> str:
    trades = int(float(row.get("trade_count") or 0))
    net = float(row.get("net_profit") or 0.0)
    pf = fnum(row.get("profit_factor"))
    if trades < 10:
        return "thin_slice"
    if net < -30.0:
        return "negative_slice"
    if pf is not None and pf < 0.9:
        return "weak_pf_slice"
    if net < 0.0:
        return "minor_negative_slice"
    return "measured_slice"


def curve_grade(row: Mapping[str, Any]) -> str:
    net = float(row.get("net_profit") or 0.0)
    pf = fnum(row.get("profit_factor")) or 0.0
    equity_dd = fnum(row.get("report_equity_drawdown_percent")) or 0.0
    positive_month_ratio = fnum(row.get("positive_month_ratio")) or 0.0
    late_net = float(row.get("chron_late_net") or 0.0)
    if net <= 0.0:
        return "D_broken"
    if equity_dd >= 38.0 or pf <= 1.03 or positive_month_ratio < 0.5:
        return "D_fragile"
    if equity_dd >= 30.0 or positive_month_ratio < 0.67 or late_net <= 0.0:
        return "C_watch"
    return "B_survives"


def curve_read(row: Mapping[str, Any]) -> str:
    grade = str(row.get("curve_grade") or "")
    if grade.startswith("D"):
        return "rough_curve_high_dd_or_low_pf"
    if grade.startswith("C"):
        return "survives_but_curve_not_pretty"
    return "curve_survives_first_pass"


def build_curve_diagnostics(
    trade_rows: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
) -> list[dict[str, Any]]:
    kpi_by_view = {str(item.get("record_view")): item for item in report_records(execution_result)}
    rows: list[dict[str, Any]] = []
    for grouped in grouped_rows(
        trade_rows,
        ("candidate_id", "candidate_alias", "candidate_role", "record_view", "tier_scope", "route_role"),
    ):
        record_view = str(grouped["record_view"])
        view_trades = [row for row in trade_rows if str(row.get("record_view")) == record_view]
        months = grouped_rows(view_trades, ("month",))
        chron = {row["bucket"]: row for row in build_time_slice_rows(view_trades) if row.get("axis") == "chron_segment"}
        worst_month = min(months, key=lambda item: float(item.get("net_profit") or 0.0)) if months else {}
        best_month = max(months, key=lambda item: float(item.get("net_profit") or 0.0)) if months else {}
        positive_months = sum(1 for row in months if float(row.get("net_profit") or 0.0) > 0.0)
        kpi = kpi_by_view.get(record_view, {})
        kpi_metrics = kpi.get("metrics", {}) if isinstance(kpi, Mapping) else {}
        grouped.update(
            {
                "report_balance_drawdown_percent": kpi_metrics.get("balance_drawdown_maximal_percent"),
                "report_equity_drawdown_percent": kpi_metrics.get("equity_drawdown_maximal_percent"),
                "report_recovery_factor": kpi_metrics.get("recovery_factor"),
                "positive_month_ratio": positive_months / len(months) if months else None,
                "negative_month_count": sum(1 for row in months if float(row.get("net_profit") or 0.0) < 0.0),
                "worst_month": worst_month.get("month", ""),
                "worst_month_net": worst_month.get("net_profit", ""),
                "best_month": best_month.get("month", ""),
                "best_month_net": best_month.get("net_profit", ""),
                "chron_early_net": chron.get("chron_early", {}).get("net_profit", ""),
                "chron_mid_net": chron.get("chron_mid", {}).get("net_profit", ""),
                "chron_late_net": chron.get("chron_late", {}).get("net_profit", ""),
                "source_chart_path": view_trades[0].get("source_chart_path", "") if view_trades else "",
            }
        )
        grouped["curve_grade"] = curve_grade(grouped)
        grouped["curve_read"] = curve_read(grouped)
        rows.append(grouped)
    return rows


def weakest_bucket(
    time_slice_rows: Sequence[Mapping[str, Any]],
    candidate_id: str,
    route_role: str,
    axis: str,
) -> Mapping[str, Any]:
    rows = [
        row
        for row in time_slice_rows
        if row.get("candidate_id") == candidate_id
        and row.get("route_role") == route_role
        and row.get("axis") == axis
        and int(float(row.get("trade_count") or 0)) >= 10
    ]
    return min(rows, key=lambda item: float(item.get("net_profit") or 0.0)) if rows else {}


def build_candidate_summary(
    curve_rows: Sequence[Mapping[str, Any]],
    time_slice_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    routed = [row for row in curve_rows if row.get("route_role") == "routed_total"]
    summary: list[dict[str, Any]] = []
    for row in sorted(routed, key=lambda item: str(item.get("candidate_id"))):
        candidate_id = str(row.get("candidate_id"))
        weak_month = weakest_bucket(time_slice_rows, candidate_id, "routed_total", "month")
        weak_session = weakest_bucket(time_slice_rows, candidate_id, "routed_total", "session_slice")
        weak_hour = weakest_bucket(time_slice_rows, candidate_id, "routed_total", "close_hour_utc")
        weak_direction = weakest_bucket(time_slice_rows, candidate_id, "routed_total", "direction")
        weak_adx = weakest_bucket(time_slice_rows, candidate_id, "routed_total", "adx_bucket")
        weak_chron = weakest_bucket(time_slice_rows, candidate_id, "routed_total", "chron_segment")
        summary.append(
            {
                "candidate_id": candidate_id,
                "candidate_alias": row.get("candidate_alias"),
                "candidate_role": row.get("candidate_role"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "expectancy": row.get("expectancy"),
                "report_equity_drawdown_percent": row.get("report_equity_drawdown_percent"),
                "closed_balance_max_drawdown_percent": row.get("closed_balance_max_drawdown_percent"),
                "positive_month_ratio": row.get("positive_month_ratio"),
                "worst_month": weak_month.get("bucket", ""),
                "worst_month_net": weak_month.get("net_profit", ""),
                "weakest_session": weak_session.get("bucket", ""),
                "weakest_session_net": weak_session.get("net_profit", ""),
                "weakest_hour_utc": weak_hour.get("bucket", ""),
                "weakest_hour_net": weak_hour.get("net_profit", ""),
                "weakest_direction": weak_direction.get("bucket", ""),
                "weakest_direction_net": weak_direction.get("net_profit", ""),
                "weakest_adx_bucket": weak_adx.get("bucket", ""),
                "weakest_adx_net": weak_adx.get("net_profit", ""),
                "weakest_chron_segment": weak_chron.get("bucket", ""),
                "weakest_chron_net": weak_chron.get("net_profit", ""),
                "curve_grade": row.get("curve_grade"),
                "candidate_read": row.get("curve_read"),
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return summary


def top_negative_slices(time_slice_rows: Sequence[Mapping[str, Any]], limit: int = 12) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in time_slice_rows
        if row.get("route_role") == "routed_total"
        and row.get("slice_read") in {"negative_slice", "weak_pf_slice", "minor_negative_slice"}
        and int(float(row.get("trade_count") or 0)) >= 10
    ]
    rows.sort(key=lambda item: float(item.get("net_profit") or 0.0))
    return rows[:limit]


def report_markdown(result: Mapping[str, Any]) -> str:
    summary = result["candidate_summary"]
    weak_slices = result.get("top_negative_slices", [])
    lines = [
        "# Stage267 Historical 2024 Balance/Time-Slice Review(267단계 2024 잔액/시간 구간 검토)",
        "",
        "- action(행동): MT5 Strategy Tester(전략 테스터) HTML report(보고서)의 deal list(거래 목록)를 파싱하고, closed balance curve(청산 기준 잔액 곡선), monthly/session/time-slice KPI(월별/세션별/시간대별 핵심 성과 지표)를 계산했다.",
        "- effect(효과): 2024 historical stress(2024 과거 압박)에서 누가 단순히 순수익이 높은지가 아니라, 어디서 거칠게 깨지는지 후보별로 볼 수 있게 했다.",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- parser_errors(파서 오류): `{len(result['parser_errors'])}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Candidate Curve Read(후보 곡선 판독)",
        "",
        "| candidate(후보) | role(역할) | net(순수익) | PF(수익 팩터) | trades(거래 수) | equity DD%(평가금 손실폭%) | month+(양수 월 비율) | worst month(최악 월) | weakest session(최약 세션) | grade(등급) | read(판독) |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |",
    ]
    for row in summary:
        lines.append(
            "| `{candidate_id}` | `{candidate_role}` | {net_profit:.2f} | {profit_factor:.2f} | {trade_count} | {dd:.2f} | {pmr:.2f} | `{worst_month}` {worst_month_net:.2f} | `{weakest_session}` {weakest_session_net:.2f} | `{curve_grade}` | `{candidate_read}` |".format(
                candidate_id=row.get("candidate_id"),
                candidate_role=row.get("candidate_role"),
                net_profit=float(row.get("net_profit") or 0.0),
                profit_factor=float(row.get("profit_factor") or 0.0),
                trade_count=int(float(row.get("trade_count") or 0)),
                dd=float(row.get("report_equity_drawdown_percent") or 0.0),
                pmr=float(row.get("positive_month_ratio") or 0.0),
                worst_month=row.get("worst_month"),
                worst_month_net=float(row.get("worst_month_net") or 0.0),
                weakest_session=row.get("weakest_session"),
                weakest_session_net=float(row.get("weakest_session_net") or 0.0),
                curve_grade=row.get("curve_grade"),
                candidate_read=row.get("candidate_read"),
            )
        )
    lines.extend(
        [
            "",
            "## Common Weak Slices(공통 약점 구간)",
            "",
            "| candidate(후보) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | PF(수익 팩터) | read(판독) |",
            "| --- | --- | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in weak_slices:
        lines.append(
            "| `{candidate_alias}` | `{axis}` | `{bucket}` | {trade_count} | {net_profit:.2f} | {profit_factor:.2f} | `{slice_read}` |".format(
                candidate_alias=row.get("candidate_alias"),
                axis=row.get("axis"),
                bucket=row.get("bucket"),
                trade_count=int(float(row.get("trade_count") or 0)),
                net_profit=float(row.get("net_profit") or 0.0),
                profit_factor=float(row.get("profit_factor") or 0.0),
                slice_read=row.get("slice_read"),
            )
        )
    lines.extend(
        [
            "",
            "## Read(판독)",
            "",
            "- `s258_short_tight_control`은 net profit(순수익)이 가장 높지만 equity DD%(평가금 손실폭%)가 가장 크다. Effect(효과): stress challenger(압박 도전자)로 남기되, 강한 후보로 올리면 안 된다.",
            "- `s262_lowrank_inner_half_filter`는 validation-heavy(검증 중심) 역할과 다르게 2024 stress(2024 압박)에서 PF(수익 팩터)와 DD(drawdown, 손실폭)가 가장 불편하다. Effect(효과): validation 안정성 후보라는 역할은 유지하되, 2024 회복력은 약점으로 기록한다.",
            "- `s264_allow_inner_high_quarter`, `s264_lowrank_control`, `s264_allow_inner_all_oos_anchor`는 버티기는 하지만 curve(곡선)가 예쁘다고 말할 수 없다. Effect(효과): 다음 R&D racing(연구개발 경주)은 더 좋은 숫자 찾기가 아니라 약한 구간을 줄이는 방향이어야 한다.",
            "",
            "## Judgment(판정)",
            "",
            "- result_subject(판정 대상): Stage267 run267B 2024 historical stress(2024 과거 압박) balance/time-slice review(잔액/시간 구간 검토).",
            "- evidence_available(사용 가능 근거): MT5 report(보고서) 10개, deal list(거래 목록), closed balance diagnostics(잔액 곡선 진단), time-slice KPI(시간 구간 핵심 성과 지표).",
            "- evidence_missing(부족 근거): visual zoom review(시각 확대 검토), feature ablation(피처 제거), similar replacement(유사 대체), Adapter(어댑터) 구조 검증.",
            "- judgment_label(판정 라벨): `inconclusive_research_evidence`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- next_condition(다음 조건): 약한 월/세션/시간대가 ablation/replacement(제거/대체)와 Adapter(어댑터) 구조에서 줄어드는지 확인한다.",
        ]
    )
    return "\n".join(lines)


def upsert_stage_ledger() -> None:
    row = {
        "row_id": "stage267_run267B_historical_2024_balance_time_slice_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "historical_2024_balance_time_slice_review",
        "tier_scope": "Tier A and Tier A+B historical stress attempts",
        "scoreboard": "trade_shape",
        "status": "completed_quantitative_review_visual_zoom_pending",
        "judgment": "inconclusive_rough_curve_no_candidate_selection",
        "evidence_boundary": "closed_balance_curve_and_time_slice_from_mt5_deals_no_candidate_selection_no_onnx_readiness",
        "report_path": rel(REPORT_PATH),
        "notes": "2024 historical stress balance/time-slice review recorded; selected candidate none.",
    }
    rows = input_probe.read_csv_rows(STAGE_LEDGER_PATH)
    merged = [item for item in rows if item.get("row_id") != row["row_id"]]
    merged.append(row)
    input_probe.write_csv(
        STAGE_LEDGER_PATH,
        merged,
        (
            "row_id",
            "stage_id",
            "run_id",
            "view",
            "tier_scope",
            "scoreboard",
            "status",
            "judgment",
            "evidence_boundary",
            "report_path",
            "notes",
        ),
    )


def upsert_artifacts(created_at: str) -> None:
    entries = (
        ("stage267_run267B_historical_2024_balance_time_slice_script", "producer_script", PRODUCER_PATH, "Builds 2024 balance/time-slice review from MT5 deal lists."),
        ("stage267_run267B_historical_2024_trade_records", "trade_records", TRADE_RECORDS_PATH, "Deal-paired trade records enriched with time/session/regime buckets."),
        ("stage267_run267B_historical_2024_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Monthly/session/hour/direction/regime slice KPI for 2024 stress."),
        ("stage267_run267B_historical_2024_curve_diagnostics", "balance_curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Closed-balance curve diagnostics for 2024 stress."),
        ("stage267_run267B_historical_2024_candidate_weakness", "candidate_weakness_summary", CANDIDATE_WEAKNESS_PATH, "Candidate-level 2024 weakness summary."),
        ("stage267_run267B_historical_2024_balance_time_slice_result", "review_result", REVIEW_RESULT_PATH, "JSON payload for 2024 balance/time-slice review."),
        ("stage267_run267B_historical_2024_balance_time_slice_report", "review_report", REPORT_PATH, "User-facing 2024 balance/time-slice review."),
    )
    rows = input_probe.read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows = []
    for artifact_id, artifact_type, path, notes in entries:
        new_rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    replacement = {row["artifact_id"]: row for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement]
    merged.extend(new_rows)
    input_probe.write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def execute() -> dict[str, Any]:
    created_at = utc_now()
    execution_result = read_json(EXECUTION_RESULT_PATH)
    trade_rows, parser_errors = build_trade_records(execution_result)
    time_slice_rows = build_time_slice_rows(trade_rows)
    curve_rows = build_curve_diagnostics(trade_rows, execution_result)
    candidate_summary = build_candidate_summary(curve_rows, time_slice_rows)
    negative_slices = top_negative_slices(time_slice_rows)
    result = {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": "completed_quantitative_review_visual_zoom_pending" if not parser_errors else "partial_parser_errors",
        "claim_boundary": CLAIM_BOUNDARY,
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_slice_rows),
        "curve_diagnostic_count": len(curve_rows),
        "candidate_summary_count": len(candidate_summary),
        "parser_errors": parser_errors,
        "candidate_summary": candidate_summary,
        "top_negative_slices": negative_slices,
        "outputs": {
            "trade_records": rel(TRADE_RECORDS_PATH),
            "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
            "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
            "candidate_weakness_summary": rel(CANDIDATE_WEAKNESS_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(
        TRADE_RECORDS_PATH,
        trade_rows,
        (
            "run_id",
            "record_view",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "attempt_name",
            "tier_scope",
            "route_role",
            "split",
            "trade_index",
            "direction",
            "open_time",
            "close_time",
            "month",
            "weekday",
            "close_hour_utc",
            "chron_segment",
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
            "source_report_path",
            "source_chart_path",
        ),
    )
    write_csv(
        TIME_SLICE_KPI_PATH,
        time_slice_rows,
        (
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "record_view",
            "tier_scope",
            "route_role",
            "axis",
            "bucket",
            "trade_count",
            "net_profit",
            "profit_factor",
            "expectancy",
            "win_rate",
            "closed_balance_max_drawdown",
            "closed_balance_max_drawdown_percent",
            "max_losing_streak",
            "slice_read",
        ),
    )
    write_csv(
        CURVE_DIAGNOSTICS_PATH,
        curve_rows,
        (
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "record_view",
            "tier_scope",
            "route_role",
            "trade_count",
            "net_profit",
            "profit_factor",
            "expectancy",
            "win_rate",
            "closed_balance_max_drawdown",
            "closed_balance_max_drawdown_percent",
            "longest_underwater_trades",
            "underwater_trade_share",
            "max_losing_streak",
            "report_balance_drawdown_percent",
            "report_equity_drawdown_percent",
            "report_recovery_factor",
            "positive_month_ratio",
            "negative_month_count",
            "worst_month",
            "worst_month_net",
            "best_month",
            "best_month_net",
            "chron_early_net",
            "chron_mid_net",
            "chron_late_net",
            "source_chart_path",
            "curve_grade",
            "curve_read",
        ),
    )
    write_csv(
        CANDIDATE_WEAKNESS_PATH,
        candidate_summary,
        (
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "net_profit",
            "profit_factor",
            "trade_count",
            "expectancy",
            "report_equity_drawdown_percent",
            "closed_balance_max_drawdown_percent",
            "positive_month_ratio",
            "worst_month",
            "worst_month_net",
            "weakest_session",
            "weakest_session_net",
            "weakest_hour_utc",
            "weakest_hour_net",
            "weakest_direction",
            "weakest_direction_net",
            "weakest_adx_bucket",
            "weakest_adx_net",
            "weakest_chron_segment",
            "weakest_chron_net",
            "curve_grade",
            "candidate_read",
            "selected_candidate",
            "onnx_readiness",
        ),
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    upsert_stage_ledger()
    upsert_artifacts(created_at)
    return result


def main() -> int:
    result = execute()
    print(
        json.dumps(
            {
                "status": result["status"],
                "trade_record_count": result["trade_record_count"],
                "time_slice_rows": result["time_slice_row_count"],
                "candidate_summary_count": result["candidate_summary_count"],
                "parser_errors": len(result["parser_errors"]),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
