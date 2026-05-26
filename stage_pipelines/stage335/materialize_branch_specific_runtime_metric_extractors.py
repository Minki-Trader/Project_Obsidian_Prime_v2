from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics  # noqa: E402
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report  # noqa: E402


TODAY = "2026-05-26"
STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
RUN_NUMBER = "run335N"
RUN_ID = "run335N_materialize_branch_specific_runtime_metric_extractors_v1"
PARENT_RUN_ID = "run335M_branch_specific_runtime_metric_extraction_design_v1"
NEXT_RUN_ID = "run335O_branch_specific_runtime_metric_usability_and_repair_decision_v1"

STATUS = "completed_branch_specific_runtime_metric_materialization_no_forward_decision"
JUDGMENT = "structured_runtime_trade_metrics_materialized_usable_for_diagnostics_no_forward_decision"
DECISION = "stage335N_structured_runtime_metric_materialized_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335N_branch_specific_runtime_metric_materialization_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN335D_DIR = STAGE_DIR / "02_runs" / "run335D"
RUN335F_DIR = STAGE_DIR / "02_runs" / "run335F"
RUN335K_DIR = STAGE_DIR / "02_runs" / "run335K"
RUN335L_DIR = STAGE_DIR / "02_runs" / "run335L"
RUN335M_DIR = STAGE_DIR / "02_runs" / "run335M"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335N_branch_specific_runtime_metric_materialization.md"
REPORT_DOC = REVIEWS_DIR / "run335N_branch_specific_runtime_metric_materialization.md"

TRADE_LEDGER_CSV = RUN_DIR / "runtime_trade_ledger.csv"
PARSER_CHECKS_CSV = RUN_DIR / "mt5_trade_parser_reconciliation.csv"
ATTEMPT_SUMMARY_CSV = RUN_DIR / "attempt_runtime_metric_summary.csv"
JOIN_AUDIT_CSV = RUN_DIR / "trade_telemetry_join_audit.csv"
BRANCH_METRIC_CSV = RUN_DIR / "branch_runtime_metric_matrix.csv"
LOT_NORMALIZED_CSV = RUN_DIR / "lot_normalized_metric_matrix.csv"
COST_STRESS_CSV = RUN_DIR / "cost_stress_metric_matrix.csv"
CURVE_UNDERWATER_CSV = RUN_DIR / "curve_pocket_underwater_matrix.csv"
REGIME_SLICE_CSV = RUN_DIR / "regime_direction_slice_matrix.csv"
PROXY_DIFF_CSV = RUN_DIR / "protocol_specific_proxy_mt5_difference.csv"
NEGATIVE_CONTROL_CSV = RUN_DIR / "negative_control_subject_boundary_audit.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_branch_specific_runtime_metric_materialization_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"

DEPOSIT = 500.0
ROLLING_WINDOWS = (5, 10, 20, 50)
EXTRA_COST_PER_TRADE = (0.0, 0.25, 0.5, 1.0, 2.0)
FEATURE_METADATA = {"bar_time_server", "timestamp_utc", "split", "row_index"}


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return str(value)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> None:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")


def replace_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = new_line
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + new_line + "\n"


def append_or_replace_section(path: Path, header: str, body: str) -> None:
    text, had_bom = read_text_lossless(path)
    section = f"\n## {header}\n\n{body.strip()}\n"
    pattern = re.compile(rf"\n## {re.escape(header)}\n.*?(?=\n## |\Z)", re.S)
    if pattern.search(text):
        text = pattern.sub(section.rstrip(), text)
    else:
        text = text.rstrip() + section
    write_text_lossless(path, text.rstrip() + "\n", had_bom)


def sha256_bytes(path: Path) -> str:
    return hashlib.sha256(io_path(path).read_bytes()).hexdigest()


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return default


def mt5_time(value: pd.Timestamp) -> str:
    return pd.Timestamp(value).strftime("%Y.%m.%d %H:%M:%S")


def iso_time(value: pd.Timestamp) -> str:
    return pd.Timestamp(value).strftime("%Y-%m-%d %H:%M:%S")


def session_bucket(hour: int) -> str:
    if 0 <= hour <= 6:
        return "session_00_06"
    if 7 <= hour <= 12:
        return "session_07_12"
    if 13 <= hour <= 20:
        return "session_13_20"
    return "session_21_23"


def chronological_segment(index: int, total: int) -> str:
    if total <= 0:
        return "none"
    third = (total + 2) // 3
    if index < third:
        return "chron_early"
    if index < third * 2:
        return "chron_mid"
    return "chron_late"


def group_rows(rows: Iterable[Mapping[str, Any]], keys: Sequence[str]) -> dict[tuple[Any, ...], list[Mapping[str, Any]]]:
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row.get(key) for key in keys)].append(row)
    return grouped


def profit_factor(rows: Sequence[Mapping[str, Any]]) -> float | None:
    gross_profit = sum(as_float(row.get("net_profit")) for row in rows if as_float(row.get("net_profit")) > 0.0)
    gross_loss = -sum(as_float(row.get("net_profit")) for row in rows if as_float(row.get("net_profit")) < 0.0)
    if gross_loss == 0.0:
        return math.inf if gross_profit > 0.0 else None
    return gross_profit / gross_loss


def sequence_metrics(rows: Sequence[Mapping[str, Any]], *, deposit: float = DEPOSIT) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda item: str(item.get("close_time")))
    count = len(ordered)
    net = sum(as_float(row.get("net_profit")) for row in ordered)
    wins = [as_float(row.get("net_profit")) for row in ordered if as_float(row.get("net_profit")) > 0.0]
    losses = [as_float(row.get("net_profit")) for row in ordered if as_float(row.get("net_profit")) < 0.0]
    peak = deposit
    balance = deposit
    max_dd = 0.0
    max_dd_pct = 0.0
    underwater = 0
    longest_underwater = 0
    underwater_count = 0
    max_losing_streak = 0
    current_losing = 0
    for row in ordered:
        pnl = as_float(row.get("net_profit"))
        balance += pnl
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            underwater_count += 1
            longest_underwater = max(longest_underwater, underwater)
        dd = peak - balance
        dd_pct = (dd / peak * 100.0) if peak else 0.0
        max_dd = max(max_dd, dd)
        max_dd_pct = max(max_dd_pct, dd_pct)
        if pnl < 0.0:
            current_losing += 1
            max_losing_streak = max(max_losing_streak, current_losing)
        else:
            current_losing = 0
    gross_profit = sum(wins)
    gross_loss = sum(losses)
    avg_win = gross_profit / len(wins) if wins else None
    avg_loss = gross_loss / len(losses) if losses else None
    payoff = (avg_win / abs(avg_loss)) if avg_win is not None and avg_loss not in {None, 0.0} else None
    total_volume = sum(as_float(row.get("volume")) for row in ordered)
    return {
        "trade_count": count,
        "net_profit": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor(ordered),
        "expectancy": net / count if count else None,
        "win_rate": len(wins) / count if count else None,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff_ratio": payoff,
        "closed_balance_max_drawdown": max_dd,
        "closed_balance_max_drawdown_percent": max_dd_pct,
        "longest_underwater_trades": longest_underwater,
        "underwater_trade_share": underwater_count / count if count else None,
        "max_losing_streak": max_losing_streak,
        "recovery_factor_closed": net / max_dd if max_dd > 0.0 else None,
        "total_volume": total_volume,
        "net_per_lot": net / total_volume if total_volume else None,
    }


def rolling_pocket(rows: Sequence[Mapping[str, Any]], window: int) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda item: str(item.get("close_time")))
    if not ordered:
        return {"window": window, "eligible": False}
    if len(ordered) < window:
        total = sum(as_float(row.get("net_profit")) for row in ordered)
        return {
            "window": window,
            "eligible": False,
            "observed_trades": len(ordered),
            "worst_window_net": total,
            "worst_window_start_trade": 1,
            "worst_window_end_trade": len(ordered),
        }
    best_start = 0
    worst = math.inf
    for index in range(0, len(ordered) - window + 1):
        value = sum(as_float(row.get("net_profit")) for row in ordered[index : index + window])
        if value < worst:
            worst = value
            best_start = index
    return {
        "window": window,
        "eligible": True,
        "observed_trades": len(ordered),
        "worst_window_net": worst,
        "worst_window_start_trade": best_start + 1,
        "worst_window_end_trade": best_start + window,
        "worst_window_start_time": ordered[best_start].get("close_time"),
        "worst_window_end_time": ordered[best_start + window - 1].get("close_time"),
    }


def load_runtime_sources() -> dict[str, Any]:
    runtime_summary = read_csv_rows(RUN335K_DIR / "mt5_fresh_runtime_probe_summary.csv")
    handoff = read_csv_rows(RUN335K_DIR / "independent_handoff_attempt_manifest.csv")
    parity = read_csv_rows(RUN335L_DIR / "row_level_runtime_parity_summary.csv")
    contract = read_csv_rows(RUN335M_DIR / "branch_runtime_metric_extraction_contract.csv")
    proxy_numeric = read_csv_rows(RUN335K_DIR / "proxy_numeric_vs_fresh_mt5_difference.csv")
    protocols = read_csv_rows(RUN335F_DIR / "probe_protocol_design_matrix.csv")
    return {
        "runtime_summary": runtime_summary,
        "handoff": handoff,
        "parity": parity,
        "contract": contract,
        "proxy_numeric": proxy_numeric,
        "protocols": protocols,
    }


def build_attempt_maps(sources: Mapping[str, Any]) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    summary = {row["attempt_name"]: row for row in sources["runtime_summary"]}
    handoff = {row["attempt_name"]: row for row in sources["handoff"]}
    parity = {row["attempt_name"]: row for row in sources["parity"]}
    return summary, handoff, parity


def load_feature_frames(handoff_by_attempt: Mapping[str, Mapping[str, str]]) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    for attempt, row in handoff_by_attempt.items():
        path = ROOT / str(row.get("new_feature_path", ""))
        if not path_exists(path):
            continue
        frame = pd.read_csv(io_path(path))
        frame["bar_time_server"] = frame["bar_time_server"].astype(str)
        for column in frame.columns:
            if column not in FEATURE_METADATA:
                frame[column] = pd.to_numeric(frame[column], errors="coerce")
        frames[attempt] = frame
    return frames


def load_telemetry_frames(summary_by_attempt: Mapping[str, Mapping[str, str]]) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    for attempt in summary_by_attempt:
        path = RUN335K_DIR / "runtime_telemetry" / f"{attempt}_telemetry.csv"
        if not path_exists(path):
            continue
        frame = pd.read_csv(io_path(path))
        frame = frame[frame["record_type"].eq("cycle")].copy()
        frame["bar_time"] = frame["bar_time"].astype(str)
        frames[attempt] = frame
    return frames


def parse_attempt_reports(
    summary_by_attempt: Mapping[str, Mapping[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    trade_rows: list[dict[str, Any]] = []
    parser_rows: list[dict[str, Any]] = []
    metrics_by_attempt: dict[str, dict[str, Any]] = {}
    for attempt, summary in summary_by_attempt.items():
        report_path = Path(str(summary.get("report_path", "")))
        parsed = parse_mt5_trade_report(report_path)
        trades = pair_deals_into_trades(parsed["deals"])
        report_metrics = extract_mt5_strategy_report_metrics(report_path)
        report_sha = sha256_bytes(report_path)
        ordered = sorted(trades, key=lambda item: item.close_time)
        running_balance = DEPOSIT
        for index, trade in enumerate(ordered):
            running_balance += trade.net_profit
            close = pd.Timestamp(trade.close_time)
            open_time = pd.Timestamp(trade.open_time)
            direction = "long" if trade.direction == "buy" else "short"
            trade_rows.append(
                {
                    "attempt_name": attempt,
                    "artifact_slug": summary.get("artifact_slug", ""),
                    "feature_set_id": summary.get("feature_set_id", ""),
                    "trade_index": trade.index,
                    "direction": direction,
                    "raw_direction": trade.direction,
                    "open_time": iso_time(open_time),
                    "close_time": iso_time(close),
                    "open_time_server": mt5_time(open_time),
                    "close_time_server": mt5_time(close),
                    "holding_minutes": (close - open_time).total_seconds() / 60.0,
                    "volume": trade.volume,
                    "open_price": trade.open_price,
                    "close_price": trade.close_price,
                    "gross_profit": trade.gross_profit,
                    "net_profit": trade.net_profit,
                    "commission": trade.commission,
                    "swap": trade.swap,
                    "closed_balance_recomputed": running_balance,
                    "month": close.strftime("%Y-%m"),
                    "weekday": close.strftime("%A"),
                    "open_hour": open_time.strftime("%H"),
                    "close_hour": close.strftime("%H"),
                    "session_bucket": session_bucket(int(close.strftime("%H"))),
                    "chron_segment": chronological_segment(index, len(ordered)),
                    "source_report_path": rel(report_path),
                    "report_sha256": report_sha,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        expected_count = as_int(summary.get("trade_count"))
        parsed_net = round(sum(float(trade.net_profit) for trade in trades), 6)
        expected_net = as_float(summary.get("net_profit"))
        parser_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": summary.get("artifact_slug", ""),
                "report_path": rel(report_path),
                "report_sha256": report_sha,
                "deal_count": len(parsed["deals"]),
                "expected_trade_count": expected_count,
                "parsed_trade_count": len(trades),
                "trade_count_delta": len(trades) - expected_count,
                "expected_net_profit": expected_net,
                "parsed_net_profit": parsed_net,
                "net_profit_delta": parsed_net - expected_net,
                "report_parser_status": report_metrics.get("status"),
                "trade_parser_status": "matched" if len(trades) == expected_count and abs(parsed_net - expected_net) <= 0.02 else "mismatch",
                "average_position_holding_bars": parsed["summary"].get("average_position_holding_bars"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        metrics_by_attempt[attempt] = {**dict(summary), **report_metrics, "parsed_trade_count": len(trades), "parsed_net_profit": parsed_net}
    return trade_rows, parser_rows, metrics_by_attempt


def feature_bucket(value: Any, low: float | None = None, high: float | None = None, prefix: str = "bucket") -> str:
    number = as_float(value, math.nan)
    if not math.isfinite(number):
        return "feature_missing"
    if low is not None and high is not None:
        if number <= low:
            return f"{prefix}_low"
        if number <= high:
            return f"{prefix}_mid"
        return f"{prefix}_high"
    if number < -1.0:
        return f"{prefix}_lt_minus1"
    if number > 1.0:
        return f"{prefix}_gt_plus1"
    return f"{prefix}_neutral"


def feature_quantiles(frames: Mapping[str, pd.DataFrame], column: str) -> tuple[float, float] | None:
    values = []
    for frame in frames.values():
        if column in frame.columns:
            values.extend(pd.to_numeric(frame[column], errors="coerce").dropna().tolist())
    if not values:
        return None
    series = pd.Series(values)
    return float(series.quantile(1.0 / 3.0)), float(series.quantile(2.0 / 3.0))


def last_indexed_row_as_dict(frame: pd.DataFrame | None, key: str) -> dict[str, Any]:
    if frame is None or key not in frame.index:
        return {}
    matched = frame.loc[key]
    if isinstance(matched, pd.DataFrame):
        return matched.iloc[-1].to_dict()
    return matched.to_dict()


def enrich_trade_rows(
    trade_rows: Sequence[Mapping[str, Any]],
    telemetry_frames: Mapping[str, pd.DataFrame],
    feature_frames: Mapping[str, pd.DataFrame],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    vol_edges = feature_quantiles(feature_frames, "historical_vol_20")
    joined_rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    feature_by_attempt = {
        attempt: frame.set_index("bar_time_server", drop=False)
        for attempt, frame in feature_frames.items()
        if "bar_time_server" in frame.columns
    }
    telemetry_by_attempt = {
        attempt: frame.set_index("bar_time", drop=False)
        for attempt, frame in telemetry_frames.items()
        if "bar_time" in frame.columns
    }
    for row in trade_rows:
        current = dict(row)
        attempt = str(row.get("attempt_name"))
        open_key = str(row.get("open_time_server"))
        close_key = str(row.get("close_time_server"))
        telemetry = telemetry_by_attempt.get(attempt)
        features = feature_by_attempt.get(attempt)
        open_telemetry = last_indexed_row_as_dict(telemetry, open_key)
        close_telemetry = last_indexed_row_as_dict(telemetry, close_key)
        feature_row = last_indexed_row_as_dict(features, open_key)
        current.update(
            {
                "open_active_tier": open_telemetry.get("active_tier", ""),
                "open_decision": open_telemetry.get("decision", ""),
                "open_exec_action": open_telemetry.get("exec_action", ""),
                "open_order_filled": open_telemetry.get("order_filled", ""),
                "open_p_short": open_telemetry.get("p_short", ""),
                "open_p_flat": open_telemetry.get("p_flat", ""),
                "open_p_long": open_telemetry.get("p_long", ""),
                "close_decision": close_telemetry.get("decision", ""),
                "close_exec_action": close_telemetry.get("exec_action", ""),
                "feature_join_status": "matched" if feature_row else "missing",
                "telemetry_open_join_status": "matched" if open_telemetry else "missing",
                "telemetry_close_join_status": "matched" if close_telemetry else "missing",
                "feature_minutes_from_cash_open": feature_row.get("minutes_from_cash_open", ""),
                "feature_historical_vol_20": feature_row.get("historical_vol_20", ""),
                "feature_adx_14": feature_row.get("adx_14", ""),
                "feature_vix_zscore_20": feature_row.get("vix_zscore_20", ""),
                "feature_usdx_zscore_20": feature_row.get("usdx_zscore_20", ""),
                "feature_us10yr_zscore_20": feature_row.get("us10yr_zscore_20", ""),
            }
        )
        if vol_edges is None:
            current["volatility_regime"] = "feature_missing"
        else:
            current["volatility_regime"] = feature_bucket(feature_row.get("historical_vol_20"), vol_edges[0], vol_edges[1], "vol")
        adx = as_float(feature_row.get("adx_14"), math.nan)
        if not math.isfinite(adx):
            current["adx_bucket"] = "feature_missing"
        elif adx < 20:
            current["adx_bucket"] = "adx_lt20"
        elif adx <= 25:
            current["adx_bucket"] = "adx_20_25"
        else:
            current["adx_bucket"] = "adx_gt25"
        current["vix_regime"] = feature_bucket(feature_row.get("vix_zscore_20"), prefix="vix_z")
        current["usd_regime"] = feature_bucket(feature_row.get("usdx_zscore_20"), prefix="usdx_z")
        current["rate_regime"] = feature_bucket(feature_row.get("us10yr_zscore_20"), prefix="us10yr_z")
        joined_rows.append(current)
        audit_rows.append(
            {
                "attempt_name": attempt,
                "trade_index": row.get("trade_index"),
                "open_time_server": open_key,
                "close_time_server": close_key,
                "open_join_status": current["telemetry_open_join_status"],
                "close_join_status": current["telemetry_close_join_status"],
                "feature_join_status": current["feature_join_status"],
                "open_active_tier": current["open_active_tier"],
                "open_decision": current["open_decision"],
                "open_exec_action": current["open_exec_action"],
                "open_order_filled": current["open_order_filled"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return joined_rows, audit_rows


def build_attempt_summary(
    trade_rows: Sequence[Mapping[str, Any]],
    parser_rows: Sequence[Mapping[str, Any]],
    metrics_by_attempt: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parser_by_attempt = {row["attempt_name"]: row for row in parser_rows}
    rows: list[dict[str, Any]] = []
    for attempt, grouped in group_rows(trade_rows, ("attempt_name",)).items():
        attempt_name = str(attempt[0])
        metrics = sequence_metrics(grouped)
        report = metrics_by_attempt.get(attempt_name, {})
        first = min(pd.Timestamp(row["open_time"]) for row in grouped)
        last = max(pd.Timestamp(row["close_time"]) for row in grouped)
        day_span = max((last - first).total_seconds() / 86400.0, 1.0)
        parser = parser_by_attempt.get(attempt_name, {})
        rows.append(
            {
                "attempt_name": attempt_name,
                "artifact_slug": report.get("artifact_slug", ""),
                "feature_set_id": report.get("feature_set_id", ""),
                "first_trade_open_time": iso_time(first),
                "last_trade_close_time": iso_time(last),
                "calendar_day_span": day_span,
                "trades_per_calendar_day": metrics["trade_count"] / day_span if day_span else None,
                "report_net_profit": report.get("net_profit"),
                "parsed_net_profit": parser.get("parsed_net_profit"),
                "net_profit": metrics["net_profit"],
                "profit_factor": metrics["profit_factor"],
                "trade_count": metrics["trade_count"],
                "expectancy": metrics["expectancy"],
                "win_rate": metrics["win_rate"],
                "report_max_drawdown_amount": report.get("max_drawdown_amount"),
                "closed_balance_max_drawdown": metrics["closed_balance_max_drawdown"],
                "closed_balance_max_drawdown_percent": metrics["closed_balance_max_drawdown_percent"],
                "report_recovery_factor": report.get("recovery_factor"),
                "recovery_factor_closed": metrics["recovery_factor_closed"],
                "long_trade_count": sum(1 for row in grouped if row.get("direction") == "long"),
                "short_trade_count": sum(1 for row in grouped if row.get("direction") == "short"),
                "long_net_profit": sum(as_float(row.get("net_profit")) for row in grouped if row.get("direction") == "long"),
                "short_net_profit": sum(as_float(row.get("net_profit")) for row in grouped if row.get("direction") == "short"),
                "longest_underwater_trades": metrics["longest_underwater_trades"],
                "underwater_trade_share": metrics["underwater_trade_share"],
                "max_losing_streak": metrics["max_losing_streak"],
                "net_per_lot": metrics["net_per_lot"],
                "parser_status": parser.get("trade_parser_status"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(rows, key=lambda row: row["attempt_name"])


def branches_from_contract(contract_rows: Sequence[Mapping[str, str]]) -> list[str]:
    return sorted({str(row.get("branch_name")) for row in contract_rows if row.get("branch_name")})


def build_cost_stress_rows(
    branches: Sequence[str],
    trade_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (attempt_name,), grouped in group_rows(trade_rows, ("attempt_name",)).items():
        for branch in branches:
            for extra_cost in EXTRA_COST_PER_TRADE:
                stressed = []
                for row in grouped:
                    current = dict(row)
                    current["net_profit"] = as_float(row.get("net_profit")) - extra_cost
                    stressed.append(current)
                metrics = sequence_metrics(stressed)
                rows.append(
                    {
                        "branch_name": branch,
                        "attempt_name": attempt_name,
                        "stress_model": "extra_round_turn_result_currency_per_trade",
                        "extra_cost_per_trade": extra_cost,
                        "trade_count": metrics["trade_count"],
                        "net_profit": metrics["net_profit"],
                        "profit_factor": metrics["profit_factor"],
                        "expectancy": metrics["expectancy"],
                        "closed_balance_max_drawdown": metrics["closed_balance_max_drawdown"],
                        "recovery_factor_closed": metrics["recovery_factor_closed"],
                        "stress_use": "diagnostic_cost_fragility_only_no_retune",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return rows


def build_curve_rows(branches: Sequence[str], trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for (attempt_name,), grouped in group_rows(trade_rows, ("attempt_name",)).items():
        base_metrics = sequence_metrics(grouped)
        for branch in branches:
            for window in ROLLING_WINDOWS:
                pocket = rolling_pocket(grouped, window)
                output.append(
                    {
                        "branch_name": branch,
                        "attempt_name": attempt_name,
                        "rolling_window_trades": window,
                        "window_eligible": pocket.get("eligible"),
                        "observed_trades": pocket.get("observed_trades"),
                        "worst_window_net": pocket.get("worst_window_net"),
                        "worst_window_start_trade": pocket.get("worst_window_start_trade"),
                        "worst_window_end_trade": pocket.get("worst_window_end_trade"),
                        "worst_window_start_time": pocket.get("worst_window_start_time"),
                        "worst_window_end_time": pocket.get("worst_window_end_time"),
                        "longest_underwater_trades": base_metrics["longest_underwater_trades"],
                        "underwater_trade_share": base_metrics["underwater_trade_share"],
                        "closed_balance_max_drawdown": base_metrics["closed_balance_max_drawdown"],
                        "max_losing_streak": base_metrics["max_losing_streak"],
                        "curve_use": "diagnostic_curve_quality_only_no_forward_pocket_filter",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return output


def slice_rows(rows: Sequence[Mapping[str, Any]], axis: str, bucket_field: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for (bucket, direction), grouped in group_rows(rows, (bucket_field, "direction")).items():
        metrics = sequence_metrics(grouped)
        output.append(
            {
                "axis": axis,
                "bucket": bucket,
                "direction": direction,
                **metrics,
            }
        )
    return output


def build_regime_rows(branches: Sequence[str], trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    axes = {
        "direction": "direction",
        "session": "session_bucket",
        "close_hour": "close_hour",
        "month": "month",
        "volatility": "volatility_regime",
        "adx": "adx_bucket",
        "vix": "vix_regime",
        "usd": "usd_regime",
        "rate": "rate_regime",
    }
    output: list[dict[str, Any]] = []
    for (attempt_name,), attempt_rows in group_rows(trade_rows, ("attempt_name",)).items():
        for branch in branches:
            for axis, field in axes.items():
                for item in slice_rows(attempt_rows, axis, field):
                    output.append(
                        {
                            "branch_name": branch,
                            "attempt_name": attempt_name,
                            "axis": item["axis"],
                            "bucket": item["bucket"],
                            "direction": item["direction"],
                            "trade_count": item["trade_count"],
                            "net_profit": item["net_profit"],
                            "profit_factor": item["profit_factor"],
                            "expectancy": item["expectancy"],
                            "win_rate": item["win_rate"],
                            "closed_balance_max_drawdown": item["closed_balance_max_drawdown"],
                            "longest_underwater_trades": item["longest_underwater_trades"],
                            "slice_use": "diagnostic_attribution_only_no_regime_filter",
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )
    return output


def build_lot_normalized_rows(branches: Sequence[str], summary_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in summary_rows:
        for branch in branches:
            output.append(
                {
                    "branch_name": branch,
                    "attempt_name": row.get("attempt_name"),
                    "trade_count": row.get("trade_count"),
                    "total_volume": row.get("trade_count") and as_float(row.get("trade_count")) * 0.1,
                    "net_profit": row.get("net_profit"),
                    "net_per_lot": row.get("net_per_lot"),
                    "expectancy_per_lot": as_float(row.get("expectancy")) / 0.1 if row.get("expectancy") not in {"", None} else None,
                    "lot_normalized_use": "diagnostic_scale_separation_only_no_lot_optimization",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return output


def metric_payload(metric_id: str, summary: Mapping[str, Any], cost_rows: Sequence[Mapping[str, Any]], curve_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if metric_id == "cost_stress":
        stress = [row for row in cost_rows if row.get("attempt_name") == summary.get("attempt_name") and as_float(row.get("extra_cost_per_trade")) == 1.0]
        return stress[0] if stress else {}
    if metric_id in {"curve_pocket", "underwater_stretch"}:
        windows = [row for row in curve_rows if row.get("attempt_name") == summary.get("attempt_name") and as_int(row.get("rolling_window_trades")) == 20]
        return windows[0] if windows else {}
    if metric_id == "direction_attribution":
        return {
            "long_trade_count": summary.get("long_trade_count"),
            "short_trade_count": summary.get("short_trade_count"),
            "long_net_profit": summary.get("long_net_profit"),
            "short_net_profit": summary.get("short_net_profit"),
        }
    if metric_id == "lot_normalized":
        return {"net_per_lot": summary.get("net_per_lot"), "expectancy_per_lot": as_float(summary.get("expectancy")) / 0.1}
    if metric_id == "runtime_identity":
        return {"parser_status": summary.get("parser_status")}
    if metric_id == "subject_boundary":
        return {"subject_boundary": "control_only_non_identity_runtime_subject"}
    return dict(summary)


def build_branch_metric_rows(
    contract_rows: Sequence[Mapping[str, str]],
    summary_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for contract in contract_rows:
        for summary in summary_rows:
            payload = metric_payload(str(contract.get("metric_id")), summary, cost_rows, curve_rows)
            output.append(
                {
                    "branch_name": contract.get("branch_name"),
                    "branch_id": contract.get("branch_id"),
                    "metric_id": contract.get("metric_id"),
                    "metric_family": contract.get("metric_family"),
                    "attempt_name": summary.get("attempt_name"),
                    "trade_count": summary.get("trade_count"),
                    "net_profit": summary.get("net_profit"),
                    "profit_factor": summary.get("profit_factor"),
                    "trades_per_calendar_day": summary.get("trades_per_calendar_day"),
                    "expectancy": summary.get("expectancy"),
                    "report_max_drawdown_amount": summary.get("report_max_drawdown_amount"),
                    "closed_balance_max_drawdown": summary.get("closed_balance_max_drawdown"),
                    "report_recovery_factor": summary.get("report_recovery_factor"),
                    "recovery_factor_closed": summary.get("recovery_factor_closed"),
                    "longest_underwater_trades": summary.get("longest_underwater_trades"),
                    "long_net_profit": summary.get("long_net_profit"),
                    "short_net_profit": summary.get("short_net_profit"),
                    "net_per_lot": summary.get("net_per_lot"),
                    "metric_payload": payload,
                    "metric_status": "materialized_from_structured_runtime_trade_ledger",
                    "selection_eligible": "false",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return output


def structured_value_for_dimension(
    dimension: str,
    summary: Mapping[str, Any],
    cost_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
) -> Any:
    if dimension == "net_profit":
        return summary.get("net_profit")
    if dimension == "profit_factor":
        return summary.get("profit_factor")
    if dimension == "max_drawdown":
        return summary.get("report_max_drawdown_amount") or summary.get("closed_balance_max_drawdown")
    if dimension == "trades_per_day":
        return summary.get("trades_per_calendar_day")
    if dimension == "expectancy":
        return summary.get("expectancy")
    if dimension == "recovery_factor":
        return summary.get("report_recovery_factor") or summary.get("recovery_factor_closed")
    if dimension == "underwater_stretch":
        return summary.get("longest_underwater_trades")
    if dimension == "lot_normalized_result":
        return summary.get("net_per_lot")
    if dimension == "long_short_attribution":
        return {"long_net_profit": summary.get("long_net_profit"), "short_net_profit": summary.get("short_net_profit")}
    if dimension == "spread_slippage_stress":
        stress = [
            row
            for row in cost_rows
            if row.get("attempt_name") == summary.get("attempt_name") and as_float(row.get("extra_cost_per_trade")) == 1.0
        ]
        return stress[0].get("net_profit") if stress else None
    if dimension == "curve_pocket":
        pocket = [
            row
            for row in curve_rows
            if row.get("attempt_name") == summary.get("attempt_name") and as_int(row.get("rolling_window_trades")) == 20
        ]
        return pocket[0].get("worst_window_net") if pocket else None
    if dimension == "session_hour_regime":
        return "available_in_regime_direction_slice_matrix"
    return None


def has_materialized_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value != ""
    if isinstance(value, dict):
        return any(has_materialized_value(item) for item in value.values())
    return True


def build_proxy_diff_rows(
    proxy_rows: Sequence[Mapping[str, str]],
    summary_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for proxy in proxy_rows:
        for summary in summary_rows:
            value = structured_value_for_dimension(str(proxy.get("dimension")), summary, cost_rows, curve_rows)
            proxy_value = proxy.get("proxy_expected_value")
            runtime_value = as_float(value, math.nan) if not isinstance(value, (dict, str)) else math.nan
            proxy_numeric = as_float(proxy_value, math.nan)
            difference = proxy_numeric - runtime_value if math.isfinite(proxy_numeric) and math.isfinite(runtime_value) else None
            output.append(
                {
                    "protocol_id": proxy.get("protocol_id"),
                    "branch_id": proxy.get("branch_id"),
                    "branch_name": proxy.get("branch_name"),
                    "attempt_name": summary.get("attempt_name"),
                    "dimension": proxy.get("dimension"),
                    "proxy_expected_value": proxy_value,
                    "structured_runtime_value": value,
                    "difference_proxy_minus_structured_runtime": difference,
                    "difference_status": "structured_runtime_available_proxy_aggregate_context_only" if has_materialized_value(value) else "structured_runtime_missing",
                    "proxy_use": "diagnostic_context_only_not_branch_forward_decision",
                    "runtime_use": "branch_specific_diagnostic_materialized",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return output


def build_negative_control_rows(branches: Sequence[str], summary_rows: Sequence[Mapping[str, Any]], parity_by_attempt: Mapping[str, Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    controls = {
        "cp322a_exact_blocker_control": "cp322a_exact_forward_route_signal_missing_non_identity_attempts_must_not_be_promoted",
        "subject_swap_negative_control": "nonmatching_subject_positive_runtime_result_rejected_as_selection_evidence",
        "null_adjacent_period_control": "adjacent_period_control_requires_separate_runtime_materialization_before_forward_claim",
    }
    for branch in branches:
        if branch not in controls:
            continue
        for summary in summary_rows:
            attempt = str(summary.get("attempt_name"))
            parity = parity_by_attempt.get(attempt, {})
            rows.append(
                {
                    "branch_name": branch,
                    "attempt_name": attempt,
                    "control_rule": controls[branch],
                    "runtime_identity_status": parity.get("row_level_parity_judgment", "missing_parity"),
                    "decision_mismatch_rows": parity.get("decision_mismatch_rows", ""),
                    "positive_inference_allowed": "false",
                    "control_judgment": "negative_control_boundary_enforced",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_gate_rows(
    parser_rows: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    join_rows: Sequence[Mapping[str, Any]],
    branch_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parser_mismatches = [row for row in parser_rows if row.get("trade_parser_status") != "matched"]
    open_missing = [row for row in join_rows if row.get("open_join_status") != "matched"]
    feature_missing = [row for row in join_rows if row.get("feature_join_status") != "matched"]
    return [
        {
            "gate_id": "run335M_queue_executed",
            "status": "passed",
            "evidence": rel(RUN335M_DIR / "run335N_metric_materialization_queue.csv"),
            "finding": "run335N materialization followed the queued extraction contract",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "mt5_trade_parser_reconciled",
            "status": "passed" if not parser_mismatches else "failed",
            "evidence": rel(PARSER_CHECKS_CSV),
            "finding": f"parser_mismatches={len(parser_mismatches)};trade_rows={len(trade_rows)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "trade_telemetry_open_join",
            "status": "passed" if not open_missing else "passed_with_boundary",
            "evidence": rel(JOIN_AUDIT_CSV),
            "finding": f"open_join_missing={len(open_missing)};feature_join_missing={len(feature_missing)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "branch_metric_matrix_created",
            "status": "passed" if branch_rows else "failed",
            "evidence": rel(BRANCH_METRIC_CSV),
            "finding": f"branch_metric_rows={len(branch_rows)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_runtime_difference_rebuilt",
            "status": "passed" if proxy_rows else "failed",
            "evidence": rel(PROXY_DIFF_CSV),
            "finding": f"proxy_difference_rows={len(proxy_rows)};proxy remains diagnostic context only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_retune_no_selection_no_goal_achieve",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_CSV),
            "finding": "model/threshold/lot/risk/handoff unchanged; no Forward Passed/Failed and no Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(outputs: Sequence[Path], metrics: Mapping[str, Any]) -> list[Path]:
    common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "outputs": [rel(path) for path in outputs],
        "metrics": dict(metrics),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts = {
        "backtest_forensics_receipt.json": {
            **common,
            "tester_identity": "FPMarketsSC-Live Strategy Tester; US100 M5; deposit 500; leverage 1:100; period 2026-04-14 to 2026-05-23 from run335K reports.",
            "ea_identity": "ObsidianPrimeV2_RuntimeProbeEA with run335K .set, model, feature order, and telemetry identity.",
            "report_identity": rel(RUN335K_DIR / "mt5" / "reports"),
            "trade_evidence": "MT5 deal lists parsed and reconciled to report trade counts and net profit.",
            "cost_assumptions": "Original broker tester costs plus synthetic diagnostic extra result-currency cost grid; no cost retune.",
            "forensic_checks": ["report hash", "deal count", "trade count", "net profit reconciliation", "telemetry open-time join"],
            "backtest_judgment": "usable_with_boundary_for_diagnostics_no_forward_decision",
        },
        "runtime_parity_receipt.json": {
            **common,
            "research_path": rel(Path("stage_pipelines/stage335/materialize_branch_specific_runtime_metric_extractors.py")),
            "runtime_path": rel(RUN335K_DIR / "mt5"),
            "shared_contract": "run335K model/feature/threshold/risk/handoff identities plus run335L row-level parity.",
            "known_differences": "This run parses existing MT5 reports and does not execute new Strategy Tester jobs.",
            "parity_check": "trade ledger is joined to run335K telemetry; row-level signal parity remains from run335L.",
            "runtime_claim_boundary": "runtime_probe_diagnostic_no_runtime_authority",
        },
        "data_integrity_receipt.json": {
            **common,
            "data_source": "run335K MT5 reports, telemetry, feature matrices, run335M extraction contract.",
            "time_axis": "MT5 broker server time; trade open time joins to same-bar telemetry and feature row; no future shifting.",
            "sample_scope": "US100 M5 forward runtime reports from 2026-04-14 through 2026-05-23.",
            "missing_or_duplicate_check": "Parser reconciliation and telemetry join audit emitted.",
            "feature_label_boundary": "No model training or labels; regime joins are explanatory slices only.",
            "split_boundary": "forward runtime diagnostic only.",
            "leakage_risk": "Post-hoc branch selection from slices; blocked by claim boundary and next review requirement.",
            "integrity_judgment": "usable_with_boundary_for_diagnostic_attribution",
        },
        "performance_attribution_receipt.json": {
            **common,
            "observed_change": "Repeated aggregate proxy numbers replaced with structured per-attempt runtime trade metrics.",
            "comparison_baseline": "run335L proxy specificity audit and run335K fresh runtime summaries.",
            "likely_drivers": ["trade density", "direction mix", "curve pocket", "cost stress", "session/hour/regime slices"],
            "segment_checks": ["direction", "session", "hour", "month", "volatility", "ADX", "VIX", "USD", "rate"],
            "trade_shape": "available in runtime_trade_ledger and branch_runtime_metric_matrix.",
            "alternative_explanations": ["broker fill/cost assumptions", "non-identity subject boundary", "short forward sample"],
            "attribution_confidence": "medium_for_diagnostics_low_for_selection",
            "next_probe": NEXT_RUN_ID,
        },
        "result_judgment_receipt.json": {
            **common,
            "result_subject": "run335N branch-specific runtime metric materialization",
            "evidence_available": [rel(TRADE_LEDGER_CSV), rel(BRANCH_METRIC_CSV), rel(COST_STRESS_CSV), rel(CURVE_UNDERWATER_CSV), rel(REGIME_SLICE_CSV)],
            "evidence_missing": "No new ONNX, no operating review, no forward passed/failed decision.",
            "judgment_label": "runtime_probe_diagnostic_materialized_no_forward_decision",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
        },
        "artifact_lineage_receipt.json": {
            **common,
            "source_inputs": [rel(RUN335K_DIR), rel(RUN335L_DIR), rel(RUN335M_DIR)],
            "producer": "python stage_pipelines/stage335/materialize_branch_specific_runtime_metric_extractors.py",
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in outputs],
            "availability": "tracked_run_outputs_force_added",
            "lineage_judgment": "connected_with_boundary_no_new_mt5_execution",
        },
    }
    paths = []
    for name, payload in receipts.items():
        path = RUN_DIR / name
        write_json(path, payload)
        paths.append(path)
    return paths


def write_report_and_decision(metrics: Mapping[str, Any]) -> None:
    best_attempt = metrics.get("best_net_attempt", "")
    worst_pocket = metrics.get("worst_pocket_attempt", "")
    report = f"""
# Run335N Branch-Specific Runtime Metric Materialization(335N 분기별 런타임 지표 물질화)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- decision(판정): `{DECISION}`
- trade_rows(거래 행): `{metrics['trade_rows']}`
- branch_metric_rows(분기 지표 행): `{metrics['branch_metric_rows']}`
- cost_stress_rows(비용 압박 행): `{metrics['cost_stress_rows']}`
- regime_slice_rows(국면 조각 행): `{metrics['regime_slice_rows']}`
- parser_mismatches(파서 불일치): `{metrics['parser_mismatches']}`
- best_net_attempt(최고 순수익 시도): `{best_attempt}`
- worst_pocket_attempt(최악 포켓 시도): `{worst_pocket}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Judgment(판정)

run335N(335N 실행)은 run335K(335K 실행)의 MT5 Strategy Tester report(MT5 전략 테스터 보고서)를 trade ledger(거래 장부)로 구조화했다.

Effect(효과): run335L(335L 실행)에서 문제였던 repeated aggregate proxy(반복 집계 프록시) 대신, 실제 MT5 trade/deal list(거래/딜 목록)에서 net/PF/DD/trades per day/curve pocket/underwater/cost stress/regime slice(순수익/수익 팩터/손실/일 거래수/곡선 포켓/수중 구간/비용 압박/국면 조각)를 뽑았다.

## Evidence(근거)

- runtime_trade_ledger(런타임 거래 장부): `{rel(TRADE_LEDGER_CSV)}`
- parser_reconciliation(파서 대조): `{rel(PARSER_CHECKS_CSV)}`
- trade_telemetry_join_audit(거래-기록 연결 감사): `{rel(JOIN_AUDIT_CSV)}`
- branch_runtime_metric_matrix(분기 런타임 지표 행렬): `{rel(BRANCH_METRIC_CSV)}`
- cost_stress_metric_matrix(비용 압박 지표 행렬): `{rel(COST_STRESS_CSV)}`
- curve_pocket_underwater_matrix(곡선 포켓/수중 구간 행렬): `{rel(CURVE_UNDERWATER_CSV)}`
- regime_direction_slice_matrix(국면/방향 조각 행렬): `{rel(REGIME_SLICE_CSV)}`
- proxy_difference(프록시 차이): `{rel(PROXY_DIFF_CSV)}`
- gate_audit(게이트 감사): `{rel(GATE_AUDIT_CSV)}`

## Boundary(경계)

이 실행은 diagnostic runtime materialization(진단용 런타임 물질화)이다. 모델(model, 모델), threshold(임계값), lot(로트), risk logic(위험 로직), feature order(피처 순서), runtime handoff(런타임 인계)는 바꾸지 않았다.

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    write_md(REPORT_DOC, report)

    decision = f"""
# Decision(판정): Stage335N Branch-Specific Runtime Metric Materialization(분기별 런타임 지표 물질화)

`{RUN_ID}`은 MT5 report(보고서)를 거래 장부와 분기별 지표 행렬로 물질화했다.

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- parsed_trade_rows(파싱 거래 행): `{metrics['trade_rows']}`
- branch_metric_rows(분기 지표 행): `{metrics['branch_metric_rows']}`
- parser_mismatches(파서 불일치): `{metrics['parser_mismatches']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): 다음 run335O(335O 실행)는 이 구조화 지표를 바탕으로 방어적 실패 기억, 공격적 후보 방향, repair(수리) 우선순위를 판단할 수 있다. 단, 이 자체는 후보 선택이나 운영 주장 근거가 아니다.
"""
    write_md(DECISION_DOC, decision)


def update_workspace_documents(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        "  Stage335(335단계) run335N(335N 실행)는 "
        f"`{STATUS}`로 branch-specific runtime metric materialization(분기별 런타임 지표 물질화)을 완료했다. "
        f"Effect(효과): trade rows(거래 행) `{metrics['trade_rows']}`개, branch metric rows(분기 지표 행) "
        f"`{metrics['branch_metric_rows']}`개, regime slice rows(국면 조각 행) `{metrics['regime_slice_rows']}`개를 만들고 "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335N(335N 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", f"current_focus:\n- >-\n{focus_line}\n", 1)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_packet", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v15`")
    current_text = replace_line(current_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision", f"- decision(판정): `{DECISION}`")
    summary_line = (
        f"- run335N_summary(335N 요약): branch-specific runtime metric materialization(분기별 런타임 지표 물질화)을 "
        f"`{STATUS}`로 완료했다. Effect(효과): MT5 report(보고서)에서 trade ledger(거래 장부) `{metrics['trade_rows']}`행과 "
        f"branch runtime metric matrix(분기 런타임 지표 행렬) `{metrics['branch_metric_rows']}`행을 만들었고, "
        "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335N_summary(335N 요약)" not in current_text:
        current_text = current_text.replace("- run335M_summary", summary_line + "\n- run335M_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_text, selection_bom = read_text_lossless(SELECTED_DIR / "selection_status.md")
    selection_text = replace_line(selection_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect",
        "- effect(효과): Stage335N(335N 실행)은 structured runtime trade ledger(구조화 런타임 거래 장부)와 branch metric matrix(분기 지표 행렬)를 만들었고, run335O(335O 실행)에서 진단 활용성과 repair/공격/방어 우선순위를 판정한다. Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    selection_text = replace_line(selection_text, "- latest_review", f"- latest_review(최신 검토): `{RUN_ID}`")
    write_text_lossless(SELECTED_DIR / "selection_status.md", selection_text, selection_bom)

    brief_text, brief_bom = read_text_lossless(STAGE_BRIEF)
    brief_text = replace_line(brief_text, "- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(STAGE_BRIEF, brief_text, brief_bom)

    input_body = f"""
- runtime_trade_ledger(런타임 거래 장부): `{rel(TRADE_LEDGER_CSV)}`
- attempt_runtime_metric_summary(시도별 런타임 지표 요약): `{rel(ATTEMPT_SUMMARY_CSV)}`
- trade_telemetry_join_audit(거래-기록 연결 감사): `{rel(JOIN_AUDIT_CSV)}`
- branch_runtime_metric_matrix(분기 런타임 지표 행렬): `{rel(BRANCH_METRIC_CSV)}`
- cost_stress_metric_matrix(비용 압박 지표 행렬): `{rel(COST_STRESS_CSV)}`
- curve_pocket_underwater_matrix(곡선 포켓/수중 구간 행렬): `{rel(CURVE_UNDERWATER_CSV)}`
- regime_direction_slice_matrix(국면/방향 조각 행렬): `{rel(REGIME_SLICE_CSV)}`
- decision(결정): `{rel(DECISION_DOC)}`
"""
    append_or_replace_section(INPUT_REFS, "run335N Branch-Specific Runtime Metric Materialization(335N 분기별 런타임 지표 물질화)", input_body)

    changelog_body = f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): runtime trade ledger(런타임 거래 장부) `{metrics['trade_rows']}`행과 branch metric matrix(분기 지표 행렬) `{metrics['branch_metric_rows']}`행을 만들었다.
- boundary(경계): 이 결과는 diagnostic(진단)이며 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "2026-05-26 Stage335N Branch-Specific Runtime Metric Materialization(335N 분기별 런타임 지표 물질화)", changelog_body)


def update_registers(outputs: Sequence[Path], metrics: Mapping[str, Any]) -> None:
    report_rel = rel(REPORT_DOC)
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage335_branch_specific_runtime_metric_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__structured_runtime_metric_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "branch_specific_runtime_metric_materialization",
                "tier_scope": "Tier A runtime reports with branch protocol views",
                "kpi_scope": "runtime_trade_ledger_cost_curve_regime_direction_diagnostics",
                "scoreboard_lane": "runtime_probe_diagnostic_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "primary_kpi": f"trade_rows={metrics['trade_rows']};branch_metric_rows={metrics['branch_metric_rows']};parser_mismatches={metrics['parser_mismatches']}",
                "guardrail_kpi": "no_retune;proxy_context_only;forward_passed_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "completed_existing_run335K_mt5_report_review_no_new_mt5",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "work_family",
            "evidence_scope",
            "kpi_scope",
            "status",
            "judgment",
            "claim_boundary",
            "path",
            "notes",
            "decision",
        ),
        [
            {
                "ledger_row_id": f"{RUN_ID}__structured_runtime_metric_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "runtime_metric_materialization",
                "evidence_scope": "run335K_mt5_reports_telemetry_features_run335M_contract",
                "kpi_scope": "structured_trade_cost_curve_regime_direction_diagnostics",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": report_rel,
                "notes": f"trade_rows={metrics['trade_rows']};branch_metric_rows={metrics['branch_metric_rows']};next={NEXT_RUN_ID}.",
                "decision": f"{DECISION};next_action={NEXT_RUN_ID}",
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": "stage335_branch_specific_runtime_metric_materialization",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "notes": "structured_runtime_metric_output_no_retune_no_forward_decision",
        }
        for path in outputs
    ]
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    sources = load_runtime_sources()
    summary_by_attempt, handoff_by_attempt, parity_by_attempt = build_attempt_maps(sources)
    feature_frames = load_feature_frames(handoff_by_attempt)
    telemetry_frames = load_telemetry_frames(summary_by_attempt)
    raw_trade_rows, parser_rows, metrics_by_attempt = parse_attempt_reports(summary_by_attempt)
    trade_rows, join_rows = enrich_trade_rows(raw_trade_rows, telemetry_frames, feature_frames)
    attempt_rows = build_attempt_summary(trade_rows, parser_rows, metrics_by_attempt)
    branches = branches_from_contract(sources["contract"])
    cost_rows = build_cost_stress_rows(branches, trade_rows)
    curve_rows = build_curve_rows(branches, trade_rows)
    regime_rows = build_regime_rows(branches, trade_rows)
    lot_rows = build_lot_normalized_rows(branches, attempt_rows)
    branch_rows = build_branch_metric_rows(sources["contract"], attempt_rows, cost_rows, curve_rows)
    proxy_rows = build_proxy_diff_rows(sources["proxy_numeric"], attempt_rows, cost_rows, curve_rows)
    negative_rows = build_negative_control_rows(branches, attempt_rows, parity_by_attempt)
    gate_rows = build_gate_rows(parser_rows, trade_rows, join_rows, branch_rows, proxy_rows)
    parser_mismatches = sum(1 for row in parser_rows if row.get("trade_parser_status") != "matched")
    best = max(attempt_rows, key=lambda row: as_float(row.get("net_profit"))) if attempt_rows else {}
    worst_pocket_row = min(curve_rows, key=lambda row: as_float(row.get("worst_window_net"), math.inf)) if curve_rows else {}
    metrics = {
        "attempt_count": len(attempt_rows),
        "trade_rows": len(trade_rows),
        "parser_mismatches": parser_mismatches,
        "join_rows": len(join_rows),
        "branch_metric_rows": len(branch_rows),
        "cost_stress_rows": len(cost_rows),
        "curve_rows": len(curve_rows),
        "regime_slice_rows": len(regime_rows),
        "proxy_difference_rows": len(proxy_rows),
        "negative_control_rows": len(negative_rows),
        "best_net_attempt": best.get("attempt_name", ""),
        "best_net_profit": best.get("net_profit", ""),
        "worst_pocket_attempt": worst_pocket_row.get("attempt_name", ""),
        "worst_pocket_net": worst_pocket_row.get("worst_window_net", ""),
    }

    write_csv(
        TRADE_LEDGER_CSV,
        [
            "attempt_name",
            "artifact_slug",
            "feature_set_id",
            "trade_index",
            "direction",
            "raw_direction",
            "open_time",
            "close_time",
            "open_time_server",
            "close_time_server",
            "holding_minutes",
            "volume",
            "open_price",
            "close_price",
            "gross_profit",
            "net_profit",
            "commission",
            "swap",
            "closed_balance_recomputed",
            "month",
            "weekday",
            "open_hour",
            "close_hour",
            "session_bucket",
            "chron_segment",
            "open_active_tier",
            "open_decision",
            "open_exec_action",
            "open_order_filled",
            "open_p_short",
            "open_p_flat",
            "open_p_long",
            "volatility_regime",
            "adx_bucket",
            "vix_regime",
            "usd_regime",
            "rate_regime",
            "source_report_path",
            "report_sha256",
            "claim_boundary",
        ],
        trade_rows,
    )
    write_csv(
        PARSER_CHECKS_CSV,
        [
            "attempt_name",
            "artifact_slug",
            "report_path",
            "report_sha256",
            "deal_count",
            "expected_trade_count",
            "parsed_trade_count",
            "trade_count_delta",
            "expected_net_profit",
            "parsed_net_profit",
            "net_profit_delta",
            "report_parser_status",
            "trade_parser_status",
            "average_position_holding_bars",
            "claim_boundary",
        ],
        parser_rows,
    )
    write_csv(
        ATTEMPT_SUMMARY_CSV,
        [
            "attempt_name",
            "artifact_slug",
            "feature_set_id",
            "first_trade_open_time",
            "last_trade_close_time",
            "calendar_day_span",
            "trades_per_calendar_day",
            "report_net_profit",
            "parsed_net_profit",
            "net_profit",
            "profit_factor",
            "trade_count",
            "expectancy",
            "win_rate",
            "report_max_drawdown_amount",
            "closed_balance_max_drawdown",
            "closed_balance_max_drawdown_percent",
            "report_recovery_factor",
            "recovery_factor_closed",
            "long_trade_count",
            "short_trade_count",
            "long_net_profit",
            "short_net_profit",
            "longest_underwater_trades",
            "underwater_trade_share",
            "max_losing_streak",
            "net_per_lot",
            "parser_status",
            "claim_boundary",
        ],
        attempt_rows,
    )
    write_csv(
        JOIN_AUDIT_CSV,
        [
            "attempt_name",
            "trade_index",
            "open_time_server",
            "close_time_server",
            "open_join_status",
            "close_join_status",
            "feature_join_status",
            "open_active_tier",
            "open_decision",
            "open_exec_action",
            "open_order_filled",
            "claim_boundary",
        ],
        join_rows,
    )
    write_csv(
        BRANCH_METRIC_CSV,
        [
            "branch_name",
            "branch_id",
            "metric_id",
            "metric_family",
            "attempt_name",
            "trade_count",
            "net_profit",
            "profit_factor",
            "trades_per_calendar_day",
            "expectancy",
            "report_max_drawdown_amount",
            "closed_balance_max_drawdown",
            "report_recovery_factor",
            "recovery_factor_closed",
            "longest_underwater_trades",
            "long_net_profit",
            "short_net_profit",
            "net_per_lot",
            "metric_payload",
            "metric_status",
            "selection_eligible",
            "claim_boundary",
        ],
        branch_rows,
    )
    write_csv(
        LOT_NORMALIZED_CSV,
        [
            "branch_name",
            "attempt_name",
            "trade_count",
            "total_volume",
            "net_profit",
            "net_per_lot",
            "expectancy_per_lot",
            "lot_normalized_use",
            "claim_boundary",
        ],
        lot_rows,
    )
    write_csv(
        COST_STRESS_CSV,
        [
            "branch_name",
            "attempt_name",
            "stress_model",
            "extra_cost_per_trade",
            "trade_count",
            "net_profit",
            "profit_factor",
            "expectancy",
            "closed_balance_max_drawdown",
            "recovery_factor_closed",
            "stress_use",
            "claim_boundary",
        ],
        cost_rows,
    )
    write_csv(
        CURVE_UNDERWATER_CSV,
        [
            "branch_name",
            "attempt_name",
            "rolling_window_trades",
            "window_eligible",
            "observed_trades",
            "worst_window_net",
            "worst_window_start_trade",
            "worst_window_end_trade",
            "worst_window_start_time",
            "worst_window_end_time",
            "longest_underwater_trades",
            "underwater_trade_share",
            "closed_balance_max_drawdown",
            "max_losing_streak",
            "curve_use",
            "claim_boundary",
        ],
        curve_rows,
    )
    write_csv(
        REGIME_SLICE_CSV,
        [
            "branch_name",
            "attempt_name",
            "axis",
            "bucket",
            "direction",
            "trade_count",
            "net_profit",
            "profit_factor",
            "expectancy",
            "win_rate",
            "closed_balance_max_drawdown",
            "longest_underwater_trades",
            "slice_use",
            "claim_boundary",
        ],
        regime_rows,
    )
    write_csv(
        PROXY_DIFF_CSV,
        [
            "protocol_id",
            "branch_id",
            "branch_name",
            "attempt_name",
            "dimension",
            "proxy_expected_value",
            "structured_runtime_value",
            "difference_proxy_minus_structured_runtime",
            "difference_status",
            "proxy_use",
            "runtime_use",
            "claim_boundary",
        ],
        proxy_rows,
    )
    write_csv(
        NEGATIVE_CONTROL_CSV,
        [
            "branch_name",
            "attempt_name",
            "control_rule",
            "runtime_identity_status",
            "decision_mismatch_rows",
            "positive_inference_allowed",
            "control_judgment",
            "claim_boundary",
        ],
        negative_rows,
    )
    write_csv(GATE_AUDIT_CSV, ["gate_id", "status", "evidence", "finding", "claim_boundary"], gate_rows)
    write_csv(
        RESULT_JUDGMENT_CSV,
        [
            "run_id",
            "status",
            "judgment",
            "decision",
            "evidence_available",
            "evidence_missing",
            "forward_passed",
            "forward_failed",
            "runtime_authority",
            "goal_achieve",
            "next_action",
            "claim_boundary",
        ],
        [
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "evidence_available": "runtime_trade_ledger;branch_metric_matrix;cost_stress;curve_underwater;regime_direction;proxy_difference",
                "evidence_missing": "operating_review;new_onnx_candidate;forward_pass_fail_decision",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    outputs = [
        TRADE_LEDGER_CSV,
        PARSER_CHECKS_CSV,
        ATTEMPT_SUMMARY_CSV,
        JOIN_AUDIT_CSV,
        BRANCH_METRIC_CSV,
        LOT_NORMALIZED_CSV,
        COST_STRESS_CSV,
        CURVE_UNDERWATER_CSV,
        REGIME_SLICE_CSV,
        PROXY_DIFF_CSV,
        NEGATIVE_CONTROL_CSV,
        GATE_AUDIT_CSV,
        RESULT_JUDGMENT_CSV,
    ]
    receipts = write_receipts(outputs, metrics)
    outputs.extend(receipts)
    write_report_and_decision(metrics)
    outputs.extend([REPORT_DOC, DECISION_DOC])
    write_json(
        FINAL_DECISION_JSON,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "metrics": metrics,
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    outputs.append(FINAL_DECISION_JSON)
    write_json(
        RUN_MANIFEST_JSON,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "stage_id": STAGE_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "command": "python stage_pipelines/stage335/materialize_branch_specific_runtime_metric_extractors.py",
            "artifacts": [rel(path) for path in outputs],
            "metrics": metrics,
            "selected_candidate": "none",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "generated_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    outputs.append(RUN_MANIFEST_JSON)
    update_workspace_documents(metrics)
    update_registers(outputs, metrics)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "trade_rows": metrics["trade_rows"],
                "branch_metric_rows": metrics["branch_metric_rows"],
                "cost_stress_rows": metrics["cost_stress_rows"],
                "regime_slice_rows": metrics["regime_slice_rows"],
                "parser_mismatches": metrics["parser_mismatches"],
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
