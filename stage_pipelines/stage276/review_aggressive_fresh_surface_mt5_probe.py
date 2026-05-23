from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report


STAGE_ID = "276_onnx_candidate_campaign__aggressive_fresh_surface_probe"
RUN_ID = "run276D_review_aggressive_fresh_surface_mt5_probe_v1"
RUN_NUMBER = "run276D"
SOURCE_RUN_ID = "run276C_aggressive_fresh_surface_mt5_signal_replay_v1"
PARENT_RUN_ID = "run276B_materialize_aggressive_fresh_surface_probe_payloads_v1"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)
DEPOSIT = 500.0
PRODUCER_PATH = Path("stage_pipelines/stage276/review_aggressive_fresh_surface_mt5_probe.py")

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
RUN276C_ROOT = STAGE_ROOT / "02_runs" / "run276C"
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"

SOURCE_EXECUTION_RESULT = RUN276C_ROOT / "execution_result.json"
SOURCE_KPI_SUMMARY = RUN276C_ROOT / "mt5_kpi_summary.csv"
SOURCE_FORENSICS = RUN276C_ROOT / "backtest_forensics.csv"
SOURCE_RUNTIME_PARITY = RUN276C_ROOT / "runtime_parity_receipt.csv"

TRADE_RECORDS = RUN_ROOT / "trade_records.csv"
TIME_SLICE_KPI = RUN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS = RUN_ROOT / "curve_diagnostics.csv"
VARIANT_SPLIT_REVIEW = RUN_ROOT / "variant_split_review.csv"
VARIANT_SUMMARY = RUN_ROOT / "variant_summary.csv"
PACKAGE_SUMMARY = RUN_ROOT / "package_summary.csv"
STABILITY_QUEUE = RUN_ROOT / "stage277_stability_queue.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
NEGATIVE_SLICE_SUMMARY = RUN_ROOT / "negative_slice_summary.csv"
PARSER_CHECKS = RUN_ROOT / "parser_checks.csv"
FORENSICS_SUMMARY = RUN_ROOT / "forensics_summary.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATES = RUN_ROOT / "gates.csv"
ARTIFACT_LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REVIEW_RESULT = RUN_ROOT / "review_result.json"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
REPORT_PATH = REVIEWS / "run276D_report.md"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"

AXES = ("month", "weekday", "session_report", "direction", "chron_segment")
ACTIVE_SURVIVOR_READ = "pressure_survivor_for_stability_validation_not_selected_candidate"

STAGE_LEDGER_COLUMNS = (
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
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def safe_name(value: str, limit: int = 96) -> str:
    return "".join(char if char.isalnum() else "_" for char in value).strip("_")[:limit]


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding=encoding,
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def read_json(path: Path) -> dict[str, Any]:
    return dict(json.loads(io_path(path).read_text(encoding="utf-8-sig")))


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_section(text: str, heading: str, block: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return text.rstrip() + "\n\n" + heading + "\n\n" + block.rstrip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    replacement = [heading, "", *block.rstrip().splitlines(), ""]
    return "\n".join([*lines[:start], *replacement, *lines[end:]]).rstrip() + "\n"


def remove_focus_items(text: str, marker: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index("current_focus:")
    except ValueError:
        return text
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith((" ", "-")):
            end = index
            break
    focus_lines = lines[start + 1 : end]
    kept: list[str] = []
    index = 0
    while index < len(focus_lines):
        line = focus_lines[index]
        if not line.startswith("- >-"):
            kept.append(line)
            index += 1
            continue
        block_end = index + 1
        while block_end < len(focus_lines) and not focus_lines[block_end].startswith("- >-"):
            block_end += 1
        block = focus_lines[index:block_end]
        if not any(marker in block_line for block_line in block):
            kept.extend(block)
        index = block_end
    return "\n".join([*lines[: start + 1], *kept, *lines[end:]]).rstrip() + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(str(value).replace(",", ""))
        return number if math.isfinite(number) else default
    except Exception:
        return default


def as_int(value: Any) -> int:
    try:
        return int(float(str(value).replace(",", "")))
    except Exception:
        return 0


def session_bucket(hour: int) -> str:
    if 0 <= hour <= 6:
        return "session_00_06_report_time"
    if 7 <= hour <= 12:
        return "session_07_12_report_time"
    if 13 <= hour <= 20:
        return "session_13_20_report_time"
    return "session_21_23_report_time"


def chronological_segment(index: int, total: int) -> str:
    if total <= 0:
        return "none"
    third = (total + 2) // 3
    if index < third:
        return "chron_early"
    if index < third * 2:
        return "chron_mid"
    return "chron_late"


def variant_token(value: str) -> str:
    text = value.replace("run276A_", "")
    for prefix in ("cp275A_", "cp275B_", "cp275D_"):
        text = text.replace(prefix, "")
    return text


def package_id_from_variant(value: str) -> str:
    for package_id in (
        "cp275A_volatility_pullback_breakout_surface",
        "cp275B_cross_asset_divergence_reversal_surface",
        "cp275D_macro_volatility_squeeze_release_surface",
    ):
        if value.startswith(package_id[:6].replace("_", "")):
            return package_id
    if "cp275A" in value:
        return "cp275A_volatility_pullback_breakout_surface"
    if "cp275B" in value:
        return "cp275B_cross_asset_divergence_reversal_surface"
    if "cp275D" in value:
        return "cp275D_macro_volatility_squeeze_release_surface"
    return ""


def attempt_by_name(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in execution_result.get("attempts", [])}


def records_by_view(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("record_view")): row for row in execution_result.get("mt5_kpi_records", [])}


def group_rows(rows: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> dict[tuple[Any, ...], list[Mapping[str, Any]]]:
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row.get(key, "") for key in keys)].append(row)
    return grouped


def profit_factor(rows: Sequence[Mapping[str, Any]]) -> float | None:
    gross_profit = sum(as_float(row.get("net_profit")) for row in rows if as_float(row.get("net_profit")) > 0.0)
    gross_loss = -sum(as_float(row.get("net_profit")) for row in rows if as_float(row.get("net_profit")) < 0.0)
    if gross_loss == 0.0:
        return math.inf if gross_profit > 0.0 else None
    return gross_profit / gross_loss


def max_closed_balance_drawdown(rows: Sequence[Mapping[str, Any]]) -> tuple[float, float, int, float]:
    balance = DEPOSIT
    peak = DEPOSIT
    max_dd = 0.0
    max_dd_pct = 0.0
    longest_underwater = 0
    current_underwater = 0
    underwater_count = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        balance += as_float(row.get("net_profit"))
        if balance >= peak:
            peak = balance
            current_underwater = 0
        else:
            current_underwater += 1
            underwater_count += 1
            longest_underwater = max(longest_underwater, current_underwater)
        dd = peak - balance
        dd_pct = dd / peak * 100.0 if peak else 0.0
        max_dd = max(max_dd, dd)
        max_dd_pct = max(max_dd_pct, dd_pct)
    return max_dd, max_dd_pct, longest_underwater, underwater_count / len(rows) if rows else 0.0


def max_losing_streak(rows: Sequence[Mapping[str, Any]]) -> int:
    current = 0
    worst = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        if as_float(row.get("net_profit")) < 0.0:
            current += 1
            worst = max(worst, current)
        else:
            current = 0
    return worst


def metrics(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda item: str(item.get("close_time")))
    count = len(ordered)
    net = round(sum(as_float(row.get("net_profit")) for row in ordered), 2)
    wins = [as_float(row.get("net_profit")) for row in ordered if as_float(row.get("net_profit")) > 0.0]
    losses = [as_float(row.get("net_profit")) for row in ordered if as_float(row.get("net_profit")) < 0.0]
    dd, dd_pct, underwater, underwater_share = max_closed_balance_drawdown(ordered)
    avg_win = sum(wins) / len(wins) if wins else None
    avg_loss = sum(losses) / len(losses) if losses else None
    return {
        "trade_count": count,
        "net_profit": net,
        "gross_profit": round(sum(wins), 2),
        "gross_loss": round(sum(losses), 2),
        "profit_factor": profit_factor(ordered),
        "expectancy": net / count if count else None,
        "win_rate": len(wins) / count if count else None,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff_ratio": (avg_win / abs(avg_loss)) if avg_win is not None and avg_loss not in {None, 0.0} else None,
        "closed_balance_max_drawdown": dd,
        "closed_balance_max_drawdown_percent": dd_pct,
        "longest_underwater_trades": underwater,
        "underwater_trade_share": underwater_share,
        "max_losing_streak": max_losing_streak(ordered),
        "recovery_factor_closed": net / dd if dd > 0 else None,
    }


def slice_read(row: Mapping[str, Any]) -> str:
    count = as_int(row.get("trade_count"))
    net = as_float(row.get("net_profit"))
    dd_pct = as_float(row.get("closed_balance_max_drawdown_percent"))
    if count < 3:
        return "thin_slice"
    if net <= -150.0 or dd_pct >= 30.0:
        return "deep_negative_or_dd_slice"
    if net < -50.0:
        return "negative_fragile_slice"
    if net < 0.0:
        return "minor_negative_slice"
    return "measured_slice"


def build_trade_records(execution_result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    attempts = attempt_by_name(execution_result)
    rows: list[dict[str, Any]] = []
    parser_checks: list[dict[str, Any]] = []
    for record in execution_result.get("mt5_kpi_records", []):
        if record.get("status") != "completed":
            continue
        report = dict(record.get("report", {}))
        metric_payload = dict(record.get("metrics", {}))
        attempt_name = str(report.get("attempt_name") or "")
        attempt = dict(attempts.get(attempt_name, {}))
        variant_id = str(attempt.get("variant_id") or "")
        package_id = str(attempt.get("package_id") or package_id_from_variant(variant_id))
        html_path = Path(str(metric_payload.get("report_path") or dict(report.get("html_report", {})).get("path") or ""))
        if not html_path.is_absolute():
            html_path = ROOT / html_path
        try:
            parsed = parse_mt5_trade_report(html_path)
            trades = pair_deals_into_trades(parsed["deals"])
            error = ""
        except Exception as exc:
            trades = []
            error = str(exc)
        expected = as_int(metric_payload.get("trade_count"))
        parser_checks.append(
            {
                "attempt_name": attempt_name,
                "record_view": record.get("record_view"),
                "variant_id": variant_id,
                "package_id": package_id,
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "report_path": rel(html_path),
                "expected_trade_count": expected,
                "parsed_trade_count": len(trades),
                "trade_count_delta": len(trades) - expected,
                "parser_status": "matched" if not error and len(trades) == expected else "parse_error" if error else "count_mismatch",
                "error": error,
            }
        )
        if error:
            continue
        ordered = sorted(trades, key=lambda item: item.close_time)
        total = len(ordered)
        for index, trade in enumerate(ordered):
            close_hour = int(trade.close_time.strftime("%H"))
            rows.append(
                {
                    "run_id": RUN_ID,
                    "source_run_id": SOURCE_RUN_ID,
                    "record_view": record.get("record_view"),
                    "attempt_name": attempt_name,
                    "variant_id": variant_id,
                    "variant_token": variant_token(variant_id),
                    "package_id": package_id,
                    "queue_role": attempt.get("queue_role", ""),
                    "tier_scope": record.get("tier_scope"),
                    "split": record.get("split"),
                    "route_role": record.get("route_role"),
                    "trade_index": trade.index,
                    "direction": trade.direction,
                    "open_time": trade.open_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "close_time": trade.close_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "holding_minutes": (trade.close_time - trade.open_time).total_seconds() / 60.0,
                    "month": trade.close_time.strftime("%Y-%m"),
                    "weekday": trade.close_time.strftime("%A"),
                    "session_report": session_bucket(close_hour),
                    "chron_segment": chronological_segment(index, total),
                    "volume": trade.volume,
                    "open_price": trade.open_price,
                    "close_price": trade.close_price,
                    "gross_profit": trade.gross_profit,
                    "net_profit": trade.net_profit,
                    "commission": trade.commission,
                    "swap": trade.swap,
                    "source_report_path": rel(html_path),
                }
            )
    return rows, parser_checks


def build_time_slice_rows(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for axis in AXES:
        keys = ("variant_id", "variant_token", "package_id", "record_view", "tier_scope", "split", axis)
        for key, rows in group_rows(trade_rows, keys).items():
            variant_id, token, package_id, record_view, tier_scope, split, bucket = key
            item = metrics(rows)
            output.append(
                {
                    "variant_id": variant_id,
                    "variant_token": token,
                    "package_id": package_id,
                    "record_view": record_view,
                    "tier_scope": tier_scope,
                    "split": split,
                    "axis": axis,
                    "bucket": bucket,
                    **item,
                    "slice_read": slice_read(item),
                }
            )
    return output


def chart_by_view(execution_result: Mapping[str, Any]) -> dict[str, str]:
    return {
        str(record.get("record_view")): str(dict(dict(record.get("report", {})).get("chart", {})).get("path") or "")
        for record in execution_result.get("mt5_kpi_records", [])
    }


def metric_by_view(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(record.get("record_view")): dict(record.get("metrics", {})) for record in execution_result.get("mt5_kpi_records", [])}


def curve_read(item: Mapping[str, Any], report_metrics: Mapping[str, Any], month_rows: Sequence[Mapping[str, Any]]) -> str:
    report_dd = as_float(report_metrics.get("equity_drawdown_maximal_percent"))
    closed_dd = as_float(item.get("closed_balance_max_drawdown_percent"))
    risk_dd = max(report_dd, closed_dd)
    pf = as_float(item.get("profit_factor"))
    net = as_float(item.get("net_profit"))
    negative_month_count = sum(1 for row in month_rows if as_float(row.get("net_profit")) < 0.0)
    if net <= 0.0:
        return "negative_curve"
    if risk_dd >= 45.0:
        return "drawdown_too_high_for_candidate_gate"
    if pf < 1.05:
        return "thin_pf_curve"
    if negative_month_count >= 3:
        return "many_negative_months_curve"
    return "constructive_watch_not_selection"


def build_curve_rows(
    trade_rows: Sequence[Mapping[str, Any]],
    time_rows: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
) -> list[dict[str, Any]]:
    metrics_by_view = metric_by_view(execution_result)
    charts = chart_by_view(execution_result)
    output: list[dict[str, Any]] = []
    keys = ("variant_id", "variant_token", "package_id", "record_view", "tier_scope", "split", "route_role")
    for key, rows in group_rows(trade_rows, keys).items():
        variant_id, token, package_id, record_view, tier_scope, split, route_role = key
        item = metrics(rows)
        report_metrics = dict(metrics_by_view.get(str(record_view), {}))
        month_rows = [
            row
            for row in time_rows
            if row.get("record_view") == record_view and row.get("axis") == "month" and as_int(row.get("trade_count")) >= 3
        ]
        chron_rows = [
            row
            for row in time_rows
            if row.get("record_view") == record_view and row.get("axis") == "chron_segment" and as_int(row.get("trade_count")) >= 3
        ]
        worst_month = min(month_rows, key=lambda row: as_float(row.get("net_profit"))) if month_rows else {}
        best_month = max(month_rows, key=lambda row: as_float(row.get("net_profit"))) if month_rows else {}
        chron = {str(row.get("bucket")): row for row in chron_rows}
        negative_months = [row for row in month_rows if as_float(row.get("net_profit")) < 0.0]
        output.append(
            {
                "variant_id": variant_id,
                "variant_token": token,
                "package_id": package_id,
                "record_view": record_view,
                "tier_scope": tier_scope,
                "split": split,
                "route_role": route_role,
                **item,
                "report_equity_drawdown_percent": report_metrics.get("equity_drawdown_maximal_percent"),
                "report_balance_drawdown_percent": report_metrics.get("balance_drawdown_maximal_percent"),
                "report_recovery_factor": report_metrics.get("recovery_factor"),
                "positive_month_ratio": (len(month_rows) - len(negative_months)) / len(month_rows) if month_rows else None,
                "negative_month_count": len(negative_months),
                "worst_month": worst_month.get("bucket", ""),
                "worst_month_net": worst_month.get("net_profit", ""),
                "best_month": best_month.get("bucket", ""),
                "best_month_net": best_month.get("net_profit", ""),
                "chron_early_net": chron.get("chron_early", {}).get("net_profit", ""),
                "chron_mid_net": chron.get("chron_mid", {}).get("net_profit", ""),
                "chron_late_net": chron.get("chron_late", {}).get("net_profit", ""),
                "source_chart_path": charts.get(str(record_view), ""),
                "curve_read": curve_read(item, report_metrics, month_rows),
            }
        )
    return output


def worst_slice_for(record_view: str, time_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    rows = [
        row
        for row in time_rows
        if row.get("record_view") == record_view
        and row.get("axis") in {"month", "session_report", "chron_segment"}
        and as_int(row.get("trade_count")) >= 3
    ]
    return min(rows, key=lambda row: as_float(row.get("net_profit"))) if rows else {}


def fragility_flags(row: Mapping[str, Any], worst: Mapping[str, Any]) -> list[str]:
    flags: list[str] = []
    if as_float(row.get("net_profit")) <= 0.0:
        flags.append("nonpositive_net")
    if as_float(row.get("profit_factor")) < 1.05:
        flags.append("pf_too_thin")
    if as_float(row.get("report_equity_drawdown_percent")) >= 45.0:
        flags.append("report_dd_too_high")
    if as_float(row.get("closed_balance_max_drawdown_percent")) >= 30.0:
        flags.append("closed_balance_dd_watch")
    if as_float(row.get("worst_month_net")) <= -120.0:
        flags.append("month_hole")
    if as_float(worst.get("net_profit")) <= -150.0:
        flags.append("deep_slice_hole")
    return flags or ["no_major_flag_in_this_split"]


def split_read(flags: Sequence[str]) -> str:
    if "nonpositive_net" in flags:
        return "fails_net_gate"
    if "pf_too_thin" in flags:
        return "thin_pf_watch_only"
    if "report_dd_too_high" in flags or "month_hole" in flags or "deep_slice_hole" in flags:
        return "risk_or_slice_fragile"
    return "split_survives_pressure_watch"


def build_variant_split_review(curve_rows: Sequence[Mapping[str, Any]], time_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in sorted(curve_rows, key=lambda item: (str(item.get("variant_id")), str(item.get("tier_scope")), str(item.get("split")))):
        worst = worst_slice_for(str(row.get("record_view")), time_rows)
        flags = fragility_flags(row, worst)
        output.append(
            {
                "variant_id": row.get("variant_id"),
                "variant_token": row.get("variant_token"),
                "package_id": row.get("package_id"),
                "tier_scope": row.get("tier_scope"),
                "split": row.get("split"),
                "record_view": row.get("record_view"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "expectancy": row.get("expectancy"),
                "win_rate": row.get("win_rate"),
                "report_equity_drawdown_percent": row.get("report_equity_drawdown_percent"),
                "closed_balance_max_drawdown_percent": row.get("closed_balance_max_drawdown_percent"),
                "recovery_factor_closed": row.get("recovery_factor_closed"),
                "negative_month_count": row.get("negative_month_count"),
                "worst_month": row.get("worst_month"),
                "worst_month_net": row.get("worst_month_net"),
                "worst_slice_axis": worst.get("axis", ""),
                "worst_slice_bucket": worst.get("bucket", ""),
                "worst_slice_net": worst.get("net_profit", ""),
                "fragility_flags": ";".join(flags),
                "curve_read": row.get("curve_read"),
                "split_review_read": split_read(flags),
                "selection_boundary": "not_candidate_selection",
            }
        )
    return output


def split_map(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("split")): row for row in rows}


def tier_survival(rows: Sequence[Mapping[str, Any]]) -> tuple[str, str]:
    splits = split_map(rows)
    val = splits.get("validation_is", {})
    oos = splits.get("oos", {})
    flags = {flag for row in rows for flag in str(row.get("fragility_flags", "")).split(";") if flag}
    if not val or not oos:
        return "missing_required_split_not_survivor", "repair_missing_split"
    if as_float(oos.get("net_profit")) <= 0.0:
        return "oos_negative_not_survivor", "failure_memory"
    if as_float(val.get("net_profit")) <= 0.0:
        return "validation_negative_not_survivor", "failure_memory"
    if as_float(val.get("profit_factor")) < 1.05 or as_float(oos.get("profit_factor")) < 1.05:
        return "pf_too_thin_not_survivor", "watch_only"
    if {"report_dd_too_high", "month_hole", "deep_slice_hole"} & flags:
        return "risk_or_slice_fragility_not_survivor", "failure_memory"
    return ACTIVE_SURVIVOR_READ, "stability_queue_seed"


def build_variant_summary(split_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for key, rows in group_rows(split_rows, ("variant_id", "variant_token", "package_id", "tier_scope")).items():
        variant_id, token, package_id, tier_scope = key
        survival, next_use = tier_survival(rows)
        splits = split_map(rows)
        val = splits.get("validation_is", {})
        oos = splits.get("oos", {})
        flags = sorted({flag for row in rows for flag in str(row.get("fragility_flags", "")).split(";") if flag})
        output.append(
            {
                "variant_id": variant_id,
                "variant_token": token,
                "package_id": package_id,
                "tier_scope": tier_scope,
                "validation_net_profit": val.get("net_profit", ""),
                "oos_net_profit": oos.get("net_profit", ""),
                "validation_profit_factor": val.get("profit_factor", ""),
                "oos_profit_factor": oos.get("profit_factor", ""),
                "validation_trade_count": val.get("trade_count", ""),
                "oos_trade_count": oos.get("trade_count", ""),
                "validation_equity_dd_percent": val.get("report_equity_drawdown_percent", ""),
                "oos_equity_dd_percent": oos.get("report_equity_drawdown_percent", ""),
                "fragility_flags": ";".join(flags),
                "survival_read": survival,
                "next_use": next_use,
            }
        )
    output.sort(key=lambda row: (0 if row["survival_read"] == ACTIVE_SURVIVOR_READ else 1, str(row["variant_id"]), str(row["tier_scope"])))
    return output


def build_package_summary(variant_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    package_rows: list[dict[str, Any]] = []
    stability_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    for key, rows in group_rows(variant_rows, ("variant_id", "variant_token", "package_id")).items():
        variant_id, token, package_id = key
        tier_a = next((row for row in rows if row.get("tier_scope") == "Tier A"), {})
        tier_b = next((row for row in rows if row.get("tier_scope") == "Tier B"), {})
        tier_a_survived = tier_a.get("survival_read") == ACTIVE_SURVIVOR_READ
        tier_b_survived = tier_b.get("survival_read") == ACTIVE_SURVIVOR_READ
        if tier_a_survived and tier_b_survived:
            package_read = "paired_pressure_survivor_for_stability_validation"
            next_use = "stage277_stability_validation_seed"
        elif tier_a_survived or tier_b_survived:
            package_read = "unpaired_survivor_watch_not_candidate"
            next_use = "failure_memory_or_repair_only"
        else:
            package_read = "paired_failure_memory_not_survivor"
            next_use = "failure_memory"
        row = {
            "variant_id": variant_id,
            "variant_token": token,
            "package_id": package_id,
            "tier_a_survival_read": tier_a.get("survival_read", "missing"),
            "tier_b_survival_read": tier_b.get("survival_read", "missing"),
            "tier_a_oos_net_profit": tier_a.get("oos_net_profit", ""),
            "tier_b_oos_net_profit": tier_b.get("oos_net_profit", ""),
            "tier_a_oos_pf": tier_a.get("oos_profit_factor", ""),
            "tier_b_oos_pf": tier_b.get("oos_profit_factor", ""),
            "package_read": package_read,
            "next_use": next_use,
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
        }
        package_rows.append(row)
        if package_read == "paired_pressure_survivor_for_stability_validation":
            stability_rows.append(
                {
                    **row,
                    "queue_id": f"run276D_{safe_name(str(token), 48)}_stage277_stability_seed",
                    "required_next_evidence": "balance/equity_curve_zoom;month_session_slice;trade_quality_stability;Adapter identity precheck",
                    "survivor_boundary": "pressure_survivor_not_selected_candidate",
                }
            )
        else:
            failure_rows.append(
                {
                    **row,
                    "failure_memory_label": package_read,
                    "reuse_rule": "do_not_call_candidate_without_new_thesis_or_repair_gate",
                }
            )
    package_rows.sort(key=lambda row: (0 if row["package_read"] == "paired_pressure_survivor_for_stability_validation" else 1, str(row["variant_id"])))
    return package_rows, stability_rows, failure_rows


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 200) -> list[dict[str, Any]]:
    rows = [
        row
        for row in time_rows
        if as_int(row.get("trade_count")) >= 3
        and as_float(row.get("net_profit")) < 0.0
        and row.get("axis") in {"month", "session_report", "chron_segment"}
    ]
    rows.sort(key=lambda row: as_float(row.get("net_profit")))
    return [dict(row) for row in rows[:limit]]


def build_forensics_summary(forensics_rows: Sequence[Mapping[str, str]], parser_checks: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    mismatches = [row for row in parser_checks if row.get("parser_status") != "matched"]
    return {
        "tester_identity": {
            "symbol": sorted({row.get("symbol", "") for row in forensics_rows if row.get("symbol")}),
            "timeframe": sorted({row.get("timeframe", "") for row in forensics_rows if row.get("timeframe")}),
            "deposit": sorted({row.get("deposit", "") for row in forensics_rows if row.get("deposit")}),
            "leverage": sorted({row.get("leverage", "") for row in forensics_rows if row.get("leverage")}),
            "model": sorted({row.get("model", "") for row in forensics_rows if row.get("model")}),
        },
        "report_identity": {
            "forensics_rows": len(forensics_rows),
            "completed_reports": sum(1 for row in forensics_rows if row.get("report_status") == "completed"),
        },
        "trade_evidence": {
            "parser_checks": len(parser_checks),
            "parser_mismatches": len(mismatches),
        },
        "cost_assumptions": "strategy_tester_report_costs_only_no_cost_edge_claim",
        "forensic_checks": "tester identity, parser match, report path, trade count, chart path where available",
        "backtest_judgment": "usable_with_boundary" if forensics_rows and not mismatches else "inconclusive_parser_mismatch",
    }


def classify_result(package_rows: Sequence[Mapping[str, Any]], parser_checks: Sequence[Mapping[str, Any]]) -> tuple[str, str, str]:
    mismatches = [row for row in parser_checks if row.get("parser_status") != "matched"]
    if mismatches:
        return (
            "partial_aggressive_fresh_surface_mt5_review_parser_mismatch",
            "inconclusive_parser_mismatch_no_candidate_selection",
            "repair_run276D_parser_or_report_identity_before_candidate_judgment",
        )
    survivors = [row for row in package_rows if row.get("package_read") == "paired_pressure_survivor_for_stability_validation"]
    if survivors:
        return (
            "completed_aggressive_fresh_surface_mt5_review_survivor_watch_no_selection",
            "exploratory_survivor_watch_no_candidate_selection",
            "run276E_close_stage276_open_stage277_stability_validation",
        )
    return (
        "completed_aggressive_fresh_surface_mt5_review_no_survivor_selection",
        "valid_negative_aggressive_fresh_surface_probe_no_candidate_selection",
        "run276E_close_stage276_open_stage277_fresh_thesis_rebuild",
    )


def _legacy_result_judgment_rows(status: str, judgment: str, next_action: str, package_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    survivors = sum(1 for row in package_rows if row.get("package_read") == "paired_pressure_survivor_for_stability_validation")
    return [
        {
            "result_subject": "run276D aggressive fresh surface balance/time-slice/trade-quality review(276D 공격형 새 표면 잔액/시간구간/거래품질 검토)",
            "evidence_available": "run276C MT5 KPI summary;48 tester reports;trade records;time-slice KPI;curve diagnostics;forensics summary",
            "evidence_missing": "Adapter package;ONNX export/parity;runtime authority;selected candidate",
            "judgment_label": judgment,
            "judgment_class": "exploratory_survivor_watch" if survivors else "valid_negative_or_failure_memory",
            "claim_boundary": BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": f"survivor_watch_rows={survivors}; selected candidate(선택 후보)는 아직 없다.",
        }
    ]


def _legacy_gate_rows(status: str, package_rows: Sequence[Mapping[str, Any]], parser_checks: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    survivors = sum(1 for row in package_rows if row.get("package_read") == "paired_pressure_survivor_for_stability_validation")
    parser_mismatches = sum(1 for row in parser_checks if row.get("parser_status") != "matched")
    return [
        {
            "gate_name": "backtest_forensics_gate",
            "status": "passed" if parser_mismatches == 0 else "blocked_or_inconclusive",
            "evidence_path": rel(PARSER_CHECKS),
            "effect": "tester report(테스터 보고서)와 trade count(거래 수)가 맞는지 확인한다.",
        },
        {
            "gate_name": "paired_tier_review_gate",
            "status": "passed" if package_rows else "blocked",
            "evidence_path": rel(PACKAGE_SUMMARY),
            "effect": "Tier A/Tier B(티어 A/티어 B)를 같은 variant(변형) 단위로 비교한다.",
        },
        {
            "gate_name": "claim_guard",
            "status": "passed_no_selected_candidate_no_onnx_no_goal",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "survivor watch(생존 관찰)를 selected candidate(선택 후보)로 올리지 않는다.",
        },
        {
            "gate_name": "next_stage_gate",
            "status": "stability_queue" if survivors else "fresh_rebuild_queue",
            "evidence_path": rel(STABILITY_QUEUE if survivors else FAILURE_MEMORY),
            "effect": "다음 stage(단계)의 질문을 좁게 유지한다.",
        },
    ]


def _legacy_write_report(result: Mapping[str, Any]) -> None:
    package_rows = list(result["package_summary"])
    survivor_rows = list(result["stability_queue"])
    failure_rows = list(result["failure_memory"])
    top_lines = []
    for row in package_rows[:12]:
        top_lines.append(
            f"- `{row['variant_token']}` `{row['package_id']}`: tier_a_oos(티어 A 표본외) `{row['tier_a_oos_net_profit']}` PF `{row['tier_a_oos_pf']}`, "
            f"tier_b_oos(티어 B 표본외) `{row['tier_b_oos_net_profit']}` PF `{row['tier_b_oos_pf']}`, read(판독) `{row['package_read']}`"
        )
    survivor_lines = "\n".join(
        f"- `{row['variant_token']}` `{row['package_id']}`: `{row['survivor_boundary']}`, next(다음) `{row['next_use']}`"
        for row in survivor_rows
    ) or "- none(없음)"
    failure_lines = "\n".join(
        f"- `{row['variant_token']}` `{row['package_id']}`: `{row['failure_memory_label']}`"
        for row in failure_rows[:16]
    ) or "- none(없음)"
    write_md(
        REPORT_PATH,
        f"""# run276D Aggressive Fresh Surface MT5 Review(276D 공격형 새 표면 MT5 검토)

- status(상태): `{result['status']}`
- judgment(판정): `{result['judgment']}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- trade_records(거래 기록): `{result['trade_record_count']}`
- package_rows(패키지 행): `{len(package_rows)}`
- survivor_watch_rows(생존 관찰 행): `{len(survivor_rows)}`
- failure_memory_rows(실패 기억 행): `{len(failure_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{result['next_action']}`

## Plain Result(쉬운 결과)

run276D(276D 실행)는 run276C(276C 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.
효과(effect, 효과): headline KPI(대표 KPI, 대표 핵심 성과 지표)가 좋은 분기라도 약한 month/session/chron slice(월/세션/순서 구간)와 drawdown(손실폭)을 숨기지 못하게 한다.

## Package Read(패키지 판독)

{chr(10).join(top_lines)}

## Survivor Watch(생존 관찰)

{survivor_lines}

## Failure Memory(실패 기억)

{failure_lines}

## Claim Boundary(주장 경계)

survivor watch(생존 관찰)는 selected candidate(선택 후보)가 아니다.
효과(effect, 효과): Stage277(277단계)로 넘기더라도 stability validation(안정성 검증) 씨앗일 뿐 ONNX readiness(ONNX 준비)나 Goal Achieve(목표 달성)를 주장하지 않는다.

`{BOUNDARY}`
""",
    )


def artifact_rows(paths: Sequence[Path], created_at: str) -> list[dict[str, Any]]:
    rows = []
    for path in paths:
        if path_exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{safe_name(rel(path), 96)}",
                    "artifact_type": "run276D_review_artifact",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created_at,
                    "notes": "run276D aggressive fresh surface MT5 review artifact.",
                }
            )
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    report = rel(REPORT_PATH)
    survivor_count = len(result["stability_queue"])
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "aggressive_fresh_surface_balance_timeslice_trade_quality_review",
                "status": result["status"],
                "judgment": result["judgment"],
                "path": report,
                "notes": f"trade_records={result['trade_record_count']};survivor_watch_rows={survivor_count};selected_candidate=none;onnx_readiness=not_claimed;next_action={result['next_action']}.",
            }
        ],
        key="run_id",
    )
    project_row = {
        "ledger_row_id": f"{RUN_ID}__balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "balance_timeslice_trade_quality_review",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "balance_timeslice_trade_quality_review",
        "tier_scope": "Tier A separate/Tier B separate/Tier A+B paired review",
        "kpi_scope": "mt5_runtime_review",
        "scoreboard_lane": "runtime_probe_review",
        "status": result["status"],
        "judgment": result["judgment"],
        "path": report,
        "primary_kpi": f"trade_records={result['trade_record_count']};survivor_watch_rows={survivor_count};package_rows={len(result['package_summary'])}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "completed_for_run276C_report_review",
        "notes": f"next_action={result['next_action']}.",
    }
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    stage_row = {
        "row_id": f"{RUN_ID}__balance_timeslice_trade_quality_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "balance_timeslice_trade_quality_review",
        "tier_scope": "Tier A separate/Tier B separate/Tier A+B paired review",
        "scoreboard": "runtime_probe_review",
        "status": result["status"],
        "judgment": result["judgment"],
        "evidence_boundary": "diagnostic_review_no_candidate_selection_no_onnx",
        "report_path": report,
        "notes": f"trade_records={result['trade_record_count']};survivor_watch_rows={survivor_count};next_action={result['next_action']}.",
    }
    upsert_csv_rows(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")


def _legacy_update_docs(result: Mapping[str, Any]) -> None:
    survivor_count = len(result["stability_queue"])
    failure_count = len(result["failure_memory"])
    selection = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{result['status']}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{result['next_action']}`")
    selection = replace_section(
        selection,
        "## Current Meaning(현재 의미)",
        f"run276D(276D 실행)는 run276C(276C 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) runtime probe(런타임 탐침)를 balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토)로 다시 읽었다.\n효과(effect, 효과): survivor watch(생존 관찰) `{survivor_count}`개와 failure memory(실패 기억) `{failure_count}`개를 남겼지만 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    selection = append_once(selection, "run276D_report", f"- run276D_report(276D 보고서): `{rel(REPORT_PATH)}`")
    selection = append_once(selection, "run276D_package_summary", f"- run276D_package_summary(276D 패키지 요약): `{rel(PACKAGE_SUMMARY)}`")
    write_md(SELECTED, selection)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{result['status']}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{result['next_action']}`")
    summary = (
        f"- run276D_summary(276D 요약): run276D(276D 실행)는 run276C(276C 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 "
        f"trade list(거래 목록), curve(곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)로 검토했다. "
        f"Effect(효과): survivor watch(생존 관찰) `{survivor_count}`개와 failure memory(실패 기억) `{failure_count}`개를 남겼고 "
        "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current = replace_line_prefix(current, "- run276D_summary(", summary)
    current = append_once(current, "run276D_summary", summary)
    write_md(CURRENT_STATE, current)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run276D_report",
        f"- run276D_report(276D 보고서): `{rel(REPORT_PATH)}`\n- run276D_trade_records(276D 거래 기록): `{rel(TRADE_RECORDS)}`\n- run276D_package_summary(276D 패키지 요약): `{rel(PACKAGE_SUMMARY)}`\n- run276D_stability_queue(276D 안정성 대기열): `{rel(STABILITY_QUEUE)}`",
    )
    write_md(REVIEW_INDEX, review)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage276(276단계) run276D(276D 실행) aggressive fresh surface MT5 review(공격형 새 표면 MT5 검토) `{RUN_ID}`. "
        f"Effect(효과): survivor watch(생존 관찰) `{survivor_count}`개와 failure memory(실패 기억) `{failure_count}`개를 기록했고 "
        f"selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = remove_focus_items(workspace, RUN_ID)
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run276D aggressive fresh surface MT5 review(276D 공격형 새 표면 MT5 검토)\n\n- status(상태): `{result['status']}`\n- judgment(판정): `{result['judgment']}`\n- effect(효과): 48개 MT5 report(보고서)를 trade/curve/slice(거래/곡선/구간)로 검토하고 survivor watch(생존 관찰) `{survivor_count}`개를 남겼다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def result_judgment_rows(status: str, judgment: str, next_action: str, package_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    survivors = sum(1 for row in package_rows if row.get("package_read") == "paired_pressure_survivor_for_stability_validation")
    return [
        {
            "result_subject": "run276D aggressive fresh surface balance/time-slice/trade-quality review(276D 공격형 새 표면 잔액/시간 구간/거래 품질 검토)",
            "evidence_available": "run276C MT5 KPI summary(run276C MT5 핵심 성과 지표 요약);48 tester reports(테스터 보고서 48개);trade records(거래 기록);time-slice KPI(시간 구간 핵심 성과 지표);curve diagnostics(곡선 진단);forensics summary(포렌식 요약)",
            "evidence_missing": "Adapter package(어댑터 패키지);ONNX export/parity(ONNX 내보내기/동등성);runtime authority(런타임 권위);selected candidate(선택 후보)",
            "judgment_label": judgment,
            "judgment_class": "exploratory_survivor_watch(탐색 생존 관찰)" if survivors else "valid_negative_or_failure_memory(유효 부정 또는 실패 기억)",
            "claim_boundary": BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": f"survivor_watch_rows(생존 관찰 행)={survivors}; selected candidate(선택 후보)는 아직 없다.",
            "status": status,
        }
    ]


def gate_rows(status: str, package_rows: Sequence[Mapping[str, Any]], parser_checks: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    survivors = sum(1 for row in package_rows if row.get("package_read") == "paired_pressure_survivor_for_stability_validation")
    parser_mismatches = sum(1 for row in parser_checks if row.get("parser_status") != "matched")
    return [
        {
            "gate_name": "backtest_forensics_gate(백테스트 포렌식 게이트)",
            "status": "passed(통과)" if parser_mismatches == 0 else "blocked_or_inconclusive(차단 또는 불충분)",
            "evidence_path": rel(PARSER_CHECKS),
            "effect": "tester report(테스터 보고서)와 trade count(거래 수)가 맞는지 확인한다.",
            "run_status": status,
        },
        {
            "gate_name": "paired_tier_review_gate(티어 쌍 검토 게이트)",
            "status": "passed(통과)" if package_rows else "blocked(차단)",
            "evidence_path": rel(PACKAGE_SUMMARY),
            "effect": "Tier A/Tier B(티어 A/티어 B)를 같은 variant(변형) 단위로 비교한다.",
            "run_status": status,
        },
        {
            "gate_name": "claim_guard(주장 보호 게이트)",
            "status": "passed_no_selected_candidate_no_onnx_no_goal(선택 후보 없음/ONNX 없음/목표 달성 없음으로 통과)",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "survivor watch(생존 관찰)를 selected candidate(선택 후보)로 올려 말하지 않는다.",
            "run_status": status,
        },
        {
            "gate_name": "next_stage_gate(다음 단계 게이트)",
            "status": "stability_queue(안정성 대기열)" if survivors else "fresh_rebuild_queue(새 재구성 대기열)",
            "evidence_path": rel(STABILITY_QUEUE if survivors else FAILURE_MEMORY),
            "effect": "다음 stage(단계)의 질문을 좁게 정한다.",
            "run_status": status,
        },
    ]


def write_report(result: Mapping[str, Any]) -> None:
    package_rows = list(result["package_summary"])
    survivor_rows = list(result["stability_queue"])
    failure_rows = list(result["failure_memory"])
    top_lines = []
    for row in package_rows[:12]:
        top_lines.append(
            f"- `{row['variant_token']}` `{row['package_id']}`: "
            f"Tier A OOS(티어 A 표본외) net(순손익) `{row['tier_a_oos_net_profit']}` PF(수익 팩터) `{row['tier_a_oos_pf']}`, "
            f"Tier B OOS(티어 B 표본외) net(순손익) `{row['tier_b_oos_net_profit']}` PF(수익 팩터) `{row['tier_b_oos_pf']}`, "
            f"read(판독) `{row['package_read']}`"
        )
    survivor_lines = "\n".join(
        f"- `{row['variant_token']}` `{row['package_id']}`: `{row['survivor_boundary']}`, next(다음) `{row['next_use']}`"
        for row in survivor_rows
    ) or "- none(없음)"
    failure_lines = "\n".join(
        f"- `{row['variant_token']}` `{row['package_id']}`: `{row['failure_memory_label']}`"
        for row in failure_rows[:16]
    ) or "- none(없음)"
    write_md(
        REPORT_PATH,
        f"""# run276D Aggressive Fresh Surface MT5 Review(276D 공격형 새 표면 MT5 검토)

- status(상태): `{result['status']}`
- judgment(판정): `{result['judgment']}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- trade_records(거래 기록): `{result['trade_record_count']}`
- package_rows(패키지 행): `{len(package_rows)}`
- survivor_watch_rows(생존 관찰 행): `{len(survivor_rows)}`
- failure_memory_rows(실패 기억 행): `{len(failure_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{result['next_action']}`

## Plain Result(쉬운 결과)

run276D(276D 실행)는 run276C(276C 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)로 다시 읽었다.
효과(effect, 효과): headline KPI(대표 핵심 성과 지표)가 좋아 보여도 약한 month/session/chron slice(월/세션/순서 구간)와 drawdown(손실폭)을 숨기지 못하게 한다.

## Package Read(패키지 판독)

{chr(10).join(top_lines)}

## Survivor Watch(생존 관찰)

{survivor_lines}

## Failure Memory(실패 기억)

{failure_lines}

## Claim Boundary(주장 경계)

survivor watch(생존 관찰)는 selected candidate(선택 후보)가 아니다.
효과(effect, 효과): Stage277(277단계)로 넘기더라도 stability validation(안정성 검증) 씨앗일 뿐, ONNX readiness(ONNX 준비)나 Goal Achieve(목표 달성)를 주장하지 않는다.

`{BOUNDARY}`
""",
    )


def update_docs(result: Mapping[str, Any]) -> None:
    survivor_count = len(result["stability_queue"])
    failure_count = len(result["failure_memory"])
    selection = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{result['status']}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{result['next_action']}`")
    selection = replace_section(
        selection,
        "## Current Meaning(현재 의미)",
        (
            f"run276D(276D 실행)는 run276C(276C 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) runtime probe(런타임 탐침)를 "
            "balance/time-slice/trade-quality review(잔액/시간 구간/거래 품질 검토)로 다시 읽었다.\n"
            f"효과(effect, 효과): survivor watch(생존 관찰) `{survivor_count}`개와 failure memory(실패 기억) `{failure_count}`개를 남겼지만 "
            "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
        ),
    )
    selection = append_once(selection, "run276D_report", f"- run276D_report(276D 보고서): `{rel(REPORT_PATH)}`")
    selection = append_once(selection, "run276D_package_summary", f"- run276D_package_summary(276D 패키지 요약): `{rel(PACKAGE_SUMMARY)}`")
    write_md(SELECTED, selection)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{result['status']}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{result['next_action']}`")
    summary = (
        f"- run276D_summary(276D 요약): run276D(276D 실행)는 run276C(276C 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 "
        "trade list(거래 목록), curve(곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)로 검토했다. "
        f"Effect(효과): survivor watch(생존 관찰) `{survivor_count}`개와 failure memory(실패 기억) `{failure_count}`개를 남겼고 "
        "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current = replace_line_prefix(current, "- run276D_summary(", summary)
    current = append_once(current, "run276D_summary", summary)
    write_md(CURRENT_STATE, current)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run276D_report",
        (
            f"- run276D_report(276D 보고서): `{rel(REPORT_PATH)}`\n"
            f"- run276D_trade_records(276D 거래 기록): `{rel(TRADE_RECORDS)}`\n"
            f"- run276D_package_summary(276D 패키지 요약): `{rel(PACKAGE_SUMMARY)}`\n"
            f"- run276D_stability_queue(276D 안정성 대기열): `{rel(STABILITY_QUEUE)}`"
        ),
    )
    write_md(REVIEW_INDEX, review)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage276(276단계) run276D(276D 실행) aggressive fresh surface MT5 review(공격형 새 표면 MT5 검토) `{RUN_ID}`. "
        f"Effect(효과): survivor watch(생존 관찰) `{survivor_count}`개와 failure memory(실패 기억) `{failure_count}`개를 기록했고 "
        "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = remove_focus_items(workspace, RUN_ID)
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        (
            "## 2026-05-23 run276D aggressive fresh surface MT5 review(276D 공격형 새 표면 MT5 검토)\n\n"
            f"- status(상태): `{result['status']}`\n"
            f"- judgment(판정): `{result['judgment']}`\n"
            f"- effect(효과): 48개 MT5 report(보고서)를 trade/curve/slice(거래/곡선/구간)로 검토하고 survivor watch(생존 관찰) `{survivor_count}`개를 남겼다.\n"
            "- boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, change)


def run() -> dict[str, Any]:
    created_at = utc_now()
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    execution_result = read_json(SOURCE_EXECUTION_RESULT)
    trade_rows, parser_checks = build_trade_records(execution_result)
    time_rows = build_time_slice_rows(trade_rows)
    curve_rows = build_curve_rows(trade_rows, time_rows, execution_result)
    split_rows = build_variant_split_review(curve_rows, time_rows)
    variant_rows = build_variant_summary(split_rows)
    package_rows, stability_rows, failure_rows = build_package_summary(variant_rows)
    negative_rows = negative_slices(time_rows)
    forensic = build_forensics_summary(read_csv_rows(SOURCE_FORENSICS), parser_checks)
    status, judgment, next_action = classify_result(package_rows, parser_checks)
    result_rows = result_judgment_rows(status, judgment, next_action, package_rows)
    gates = gate_rows(status, package_rows, parser_checks)

    trade_columns = list(trade_rows[0].keys()) if trade_rows else ["status"]
    time_columns = list(time_rows[0].keys()) if time_rows else ["status"]
    curve_columns = list(curve_rows[0].keys()) if curve_rows else ["status"]
    split_columns = list(split_rows[0].keys()) if split_rows else ["status"]
    variant_columns = list(variant_rows[0].keys()) if variant_rows else ["status"]
    package_columns = list(package_rows[0].keys()) if package_rows else ["status"]
    parser_columns = list(parser_checks[0].keys()) if parser_checks else ["status"]
    result_columns = list(result_rows[0].keys())
    gate_columns = list(gates[0].keys())

    write_csv(TRADE_RECORDS, trade_columns, trade_rows)
    write_csv(TIME_SLICE_KPI, time_columns, time_rows)
    write_csv(CURVE_DIAGNOSTICS, curve_columns, curve_rows)
    write_csv(VARIANT_SPLIT_REVIEW, split_columns, split_rows)
    write_csv(VARIANT_SUMMARY, variant_columns, variant_rows)
    write_csv(PACKAGE_SUMMARY, package_columns, package_rows)
    write_csv(STABILITY_QUEUE, package_columns + ["queue_id", "required_next_evidence", "survivor_boundary"], stability_rows)
    write_csv(FAILURE_MEMORY, package_columns + ["failure_memory_label", "reuse_rule"], failure_rows)
    write_csv(NEGATIVE_SLICE_SUMMARY, time_columns, negative_rows)
    write_csv(PARSER_CHECKS, parser_columns, parser_checks)
    write_json(FORENSICS_SUMMARY, forensic, bom=True)
    write_csv(RESULT_JUDGMENT, result_columns, result_rows)
    write_csv(GATES, gate_columns, gates)

    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "next_action": next_action,
        "trade_record_count": len(trade_rows),
        "time_slice_rows": len(time_rows),
        "curve_rows": len(curve_rows),
        "parser_checks": parser_checks,
        "forensics_summary": forensic,
        "variant_summary": variant_rows,
        "package_summary": package_rows,
        "stability_queue": stability_rows,
        "failure_memory": failure_rows,
        "result_judgment": result_rows,
        "gates": gates,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
        "created_at_utc": created_at,
    }
    write_report(result)
    output_paths = [
        TRADE_RECORDS,
        TIME_SLICE_KPI,
        CURVE_DIAGNOSTICS,
        VARIANT_SPLIT_REVIEW,
        VARIANT_SUMMARY,
        PACKAGE_SUMMARY,
        STABILITY_QUEUE,
        FAILURE_MEMORY,
        NEGATIVE_SLICE_SUMMARY,
        PARSER_CHECKS,
        FORENSICS_SUMMARY,
        RESULT_JUDGMENT,
        GATES,
        REVIEW_RESULT,
        RUN_MANIFEST,
        ARTIFACT_LINEAGE,
        REPORT_PATH,
    ]
    write_json(REVIEW_RESULT, result, bom=True)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "producer": rel(PRODUCER_PATH),
        "source_inputs": [rel(SOURCE_EXECUTION_RESULT), rel(SOURCE_KPI_SUMMARY), rel(SOURCE_FORENSICS), rel(SOURCE_RUNTIME_PARITY)],
        "outputs": [rel(path) for path in output_paths if path_exists(path)],
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
        "next_action": next_action,
    }
    write_json(RUN_MANIFEST, manifest, bom=True)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": rel(PRODUCER_PATH),
        "consumer": [next_action, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["outputs"],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in output_paths if path_exists(path) and io_path(path).is_file()},
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(ARTIFACT_LINEAGE, lineage, bom=True)
    final_paths = [path for path in output_paths if path_exists(path) and io_path(path).is_file()]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows(final_paths, created_at), key="artifact_id")
    update_ledgers(result)
    update_docs(result)
    return result


def main() -> int:
    result = run()
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": result["status"],
                "judgment": result["judgment"],
                "trade_record_count": result["trade_record_count"],
                "package_rows": len(result["package_summary"]),
                "survivor_watch_rows": len(result["stability_queue"]),
                "failure_memory_rows": len(result["failure_memory"]),
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
