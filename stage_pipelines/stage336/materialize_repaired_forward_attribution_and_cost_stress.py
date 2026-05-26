from __future__ import annotations

import csv
import json
import math
import sys
from bisect import bisect_right
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics  # noqa: E402
from foundation.mt5.trade_report import Trade, pair_deals_into_trades, parse_mt5_trade_report  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run336O"
RUN_ID = "run336O_repaired_forward_attribution_and_cost_stress_v1"
PARENT_RUN_ID = "run336N_repair_gap_or_parity_review_v1"
NEXT_RUN_ID = "run336P_forward_decision_or_failure_memory_handoff_v1"
STATUS = "completed_repaired_forward_attribution_cost_stress_no_forward_decision"
JUDGMENT = "repaired_forward_subset_profitable_but_cost_direction_curve_fragile"
DECISION = "stage336O_forward_attribution_requires_failure_memory_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336O_repaired_forward_attribution_cost_stress_"
    "same_onnx_same_feature_order_same_threshold_same_risk_same_lot_no_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN336M_DIR = STAGE_DIR / "02_runs" / "run336M"
RUN336N_DIR = STAGE_DIR / "02_runs" / "run336N"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run336O_repaired_forward_attribution_and_cost_stress.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage336O_repaired_forward_attribution_cost_stress.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

COST_STRESS = (0.25, 0.5, 1.0, 2.0, 5.0)
ROLLING_WINDOWS = (20, 50, 100)


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8"), had_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> None:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding)


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def append_after_header(text: str, marker: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for idx, existing in enumerate(lines):
        if existing.startswith(marker):
            lines.insert(idx + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_if_missing(path: Path, marker: str, entry: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        write_text_preserving(path, text, had_bom)
    return path


def append_register_row(path: Path, columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    existing_rows: list[dict[str, str]] = []
    key_column = columns[0]
    key_value = csv_value(row.get(key_column, ""))
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for existing in reader:
                if existing.get(key_column) != key_value:
                    existing_rows.append(existing)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for existing in existing_rows:
            writer.writerow({column: csv_value(existing.get(column, "")) for column in columns})
        writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def safe_float(value: Any, default: float = math.nan) -> float:
    if value in {None, ""}:
        return default
    try:
        number = float(value)
        return number if math.isfinite(number) else default
    except Exception:
        return default


def safe_int(value: Any, default: int = 0) -> int:
    number = safe_float(value, math.nan)
    return default if math.isnan(number) else int(round(number))


def parse_set(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        if not line.strip() or line.lstrip().startswith(";") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def report_path_for_attempt(attempt_name: str) -> Path:
    candidates = sorted((RUN336M_DIR / "mt5" / "reports").glob(f"*_{attempt_name}.htm"))
    if not candidates:
        raise RuntimeError(f"missing MT5 report for {attempt_name}")
    return candidates[0]


def load_feature_frame(attempt: Mapping[str, Any]) -> pd.DataFrame:
    frame = pd.read_csv(io_path(ROOT / str(attempt["feature_local_path"])))
    frame["bar_key"] = frame["bar_time_server"].astype(str)
    frame["timestamp"] = pd.to_datetime(frame["bar_time_server"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    return frame


def infer_server_utc_offset_minutes(attempts: Sequence[Mapping[str, Any]]) -> int:
    feature = load_feature_frame(attempts[0])
    first_feature_time = feature["timestamp"].dropna().iloc[0]
    raw_path = RUN336M_DIR / "raw_refresh_probe" / "US100" / "bars_us100_m5_mt5api_raw.csv"
    raw = pd.read_csv(io_path(raw_path), nrows=1)
    first_raw_utc = pd.to_datetime(raw.loc[0, "time_close_unix"], unit="s", utc=True).tz_localize(None)
    offset = int(round((first_feature_time - first_raw_utc).total_seconds() / 60.0))
    if abs(offset) > 720:
        raise RuntimeError(f"unreasonable MT5 server offset minutes: {offset}")
    return offset


def write_time_axis_offset_audit(server_utc_offset_minutes: int, attempts: Sequence[Mapping[str, Any]]) -> Path:
    feature = load_feature_frame(attempts[0])
    first_feature_time = feature["timestamp"].dropna().iloc[0]
    rows: list[dict[str, Any]] = []
    for symbol in ("US100", "VIX", "USDX", "US10YR"):
        path = RUN336M_DIR / "raw_refresh_probe" / symbol / f"bars_{symbol.lower()}_m5_mt5api_raw.csv"
        raw = pd.read_csv(io_path(path))
        first_raw_utc = pd.to_datetime(raw["time_close_unix"].iloc[0], unit="s", utc=True).tz_localize(None)
        last_raw_utc = pd.to_datetime(raw["time_close_unix"].iloc[-1], unit="s", utc=True).tz_localize(None)
        rows.append(
            {
                "symbol": symbol,
                "rows": len(raw),
                "raw_time_basis": raw.get("time_basis", pd.Series([""])).iloc[0],
                "first_raw_utc": first_raw_utc,
                "first_raw_server": first_raw_utc + timedelta(minutes=server_utc_offset_minutes),
                "last_raw_utc": last_raw_utc,
                "last_raw_server": last_raw_utc + timedelta(minutes=server_utc_offset_minutes),
                "reference_first_feature_server": first_feature_time,
                "server_utc_offset_minutes": server_utc_offset_minutes,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(
        RUN_DIR / "macro_time_axis_offset_audit.csv",
        [
            "symbol",
            "rows",
            "raw_time_basis",
            "first_raw_utc",
            "first_raw_server",
            "last_raw_utc",
            "last_raw_server",
            "reference_first_feature_server",
            "server_utc_offset_minutes",
            "claim_boundary",
        ],
        rows,
    )


def load_macro_frame(symbol: str, server_utc_offset_minutes: int) -> pd.DataFrame:
    path = RUN336M_DIR / "raw_refresh_probe" / symbol / f"bars_{symbol.lower()}_m5_mt5api_raw.csv"
    frame = pd.read_csv(io_path(path))
    timestamp_utc = pd.to_datetime(frame["time_close_unix"], unit="s", utc=True).dt.tz_localize(None)
    frame["timestamp"] = timestamp_utc + pd.to_timedelta(server_utc_offset_minutes, unit="m")
    frame["close"] = pd.to_numeric(frame["close"], errors="coerce")
    frame[f"{symbol.lower()}_change_1"] = frame["close"].diff()
    frame[f"{symbol.lower()}_level_bucket"] = quantile_bucket(frame["close"], f"{symbol.lower()}_level")
    frame[f"{symbol.lower()}_change_bucket"] = change_bucket(frame[f"{symbol.lower()}_change_1"], f"{symbol.lower()}_change")
    return frame[["timestamp", "close", f"{symbol.lower()}_change_1", f"{symbol.lower()}_level_bucket", f"{symbol.lower()}_change_bucket"]].rename(columns={"close": f"{symbol.lower()}_close"})


def load_telemetry_by_key(attempt_name: str) -> dict[str, Mapping[str, Any]]:
    path = RUN336M_DIR / "runtime_telemetry" / f"{attempt_name}_telemetry.csv"
    frame = pd.read_csv(io_path(path))
    frame = frame[frame["bar_time"].notna()].copy()
    frame["bar_key"] = frame["bar_time"].astype(str)
    return {str(row["bar_key"]): row for row in frame.to_dict("records")}


def macro_lookup_payload(macros: Mapping[str, pd.DataFrame]) -> dict[str, tuple[list[datetime], list[Mapping[str, Any]]]]:
    payload: dict[str, tuple[list[datetime], list[Mapping[str, Any]]]] = {}
    for symbol, frame in macros.items():
        ordered = frame.sort_values("timestamp").copy()
        times = [pd.Timestamp(item).to_pydatetime() for item in ordered["timestamp"].tolist()]
        payload[symbol] = (times, ordered.to_dict("records"))
    return payload


def lookup_macro_asof(payload: Mapping[str, tuple[list[datetime], list[Mapping[str, Any]]]], timestamp: datetime) -> tuple[dict[str, Any], int, float | None]:
    values: dict[str, Any] = {}
    hit_count = 0
    ages: list[float] = []
    for symbol, (times, records) in payload.items():
        idx = bisect_right(times, timestamp) - 1
        symbol_key = symbol.lower()
        if idx < 0:
            values[f"{symbol_key}_join_mode"] = "missing_before_first_bar"
            values[f"{symbol_key}_age_minutes"] = None
            continue
        item = records[idx]
        age_minutes = (timestamp - pd.Timestamp(item["timestamp"]).to_pydatetime()).total_seconds() / 60.0
        hit_count += 1
        ages.append(age_minutes)
        values[f"{symbol_key}_join_mode"] = "exact" if abs(age_minutes) < 1e-9 else "asof_backward_no_future"
        values[f"{symbol_key}_age_minutes"] = age_minutes
        for key, value in item.items():
            if key != "timestamp":
                values[key] = value
    return values, hit_count, (max(ages) if ages else None)


def quantile_bucket(series: pd.Series, prefix: str) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    finite = values.dropna()
    if finite.empty or finite.nunique() < 3:
        return pd.Series([f"{prefix}_unknown"] * len(series), index=series.index)
    q1, q2 = finite.quantile([0.33, 0.67]).tolist()
    return values.apply(lambda x: f"{prefix}_low" if pd.notna(x) and x <= q1 else (f"{prefix}_high" if pd.notna(x) and x >= q2 else (f"{prefix}_mid" if pd.notna(x) else f"{prefix}_unknown")))


def change_bucket(series: pd.Series, prefix: str) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").fillna(0.0)
    return values.apply(lambda x: f"{prefix}_up" if x > 0 else (f"{prefix}_down" if x < 0 else f"{prefix}_flat"))


def adx_bucket(value: Any) -> str:
    number = safe_float(value)
    if math.isnan(number):
        return "adx_unknown"
    if number < 15:
        return "adx_lt15"
    if number < 20:
        return "adx_15_20"
    if number < 25:
        return "adx_20_25"
    if number < 30:
        return "adx_25_30"
    return "adx_ge30"


def session_bucket(minutes: Any, hour: int) -> str:
    value = safe_float(minutes)
    if not math.isnan(value):
        if 0 <= value <= 30:
            return "cash_open_0_30"
        if 30 < value <= 180:
            return "cash_mid"
        if 180 < value <= 360:
            return "cash_late"
        if 360 < value <= 390:
            return "cash_close_30"
    if 13 <= hour <= 20:
        return "cash_or_overlap_unknown"
    return "outside_cash_session"


def group_bucket(metric: Any, edges: tuple[float, float], prefix: str) -> str:
    value = safe_float(metric)
    if math.isnan(value):
        return f"{prefix}_unknown"
    if value <= edges[0]:
        return f"{prefix}_low"
    if value >= edges[1]:
        return f"{prefix}_high"
    return f"{prefix}_mid"


def trade_curve_stats(trades: Sequence[Mapping[str, Any]], net_key: str = "net_profit") -> dict[str, Any]:
    ordered = sorted(trades, key=lambda row: row["close_time"])
    equity = []
    total = 0.0
    for row in ordered:
        total += safe_float(row.get(net_key), 0.0)
        equity.append(total)
    peak = 0.0
    max_dd = 0.0
    underwater_count = 0
    longest = 0
    current = 0
    for value in equity:
        peak = max(peak, value)
        dd = peak - value
        max_dd = max(max_dd, dd)
        if dd > 1e-12:
            underwater_count += 1
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return {
        "closed_equity_final": total,
        "closed_balance_max_drawdown": max_dd,
        "underwater_trade_count": underwater_count,
        "underwater_trade_share": underwater_count / len(equity) if equity else None,
        "longest_underwater_trades": longest,
    }


def profit_factor(values: Sequence[float]) -> float | None:
    gross_profit = sum(value for value in values if value > 0)
    gross_loss = sum(value for value in values if value < 0)
    if gross_loss == 0:
        return None
    return gross_profit / abs(gross_loss)


def group_summary(rows: Sequence[Mapping[str, Any]], group_key: str, value_key: str = "net_profit") -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    groups: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        groups.setdefault(str(row.get(group_key, "unknown")), []).append(row)
    for bucket, group in groups.items():
        values = [safe_float(row.get(value_key), 0.0) for row in group]
        results.append(
            {
                "bucket": bucket,
                "trade_count": len(group),
                "net_profit": sum(values),
                "profit_factor": profit_factor(values),
                "expectancy": sum(values) / len(values) if values else None,
                "win_rate": sum(1 for value in values if value > 0) / len(values) if values else None,
            }
        )
    return sorted(results, key=lambda row: (safe_float(row["net_profit"], -1e18), -safe_int(row["trade_count"])))


def rolling_pockets(rows: Sequence[Mapping[str, Any]], attempt_name: str) -> list[dict[str, Any]]:
    ordered = sorted(rows, key=lambda row: row["close_time"])
    values = [safe_float(row.get("net_profit"), 0.0) for row in ordered]
    result: list[dict[str, Any]] = []
    for window in ROLLING_WINDOWS:
        if len(values) < window:
            continue
        nets = [sum(values[idx : idx + window]) for idx in range(0, len(values) - window + 1)]
        worst_idx = int(np.argmin(nets))
        best_idx = int(np.argmax(nets))
        result.append(
            {
                "attempt_name": attempt_name,
                "rolling_window_trades": window,
                "worst_window_start_trade": worst_idx + 1,
                "worst_window_end_trade": worst_idx + window,
                "worst_window_net": nets[worst_idx],
                "best_window_start_trade": best_idx + 1,
                "best_window_end_trade": best_idx + window,
                "best_window_net": nets[best_idx],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return result


def build_attempt_payload(attempt: Mapping[str, Any], runtime_row: Mapping[str, Any], macros: Mapping[str, pd.DataFrame]) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    attempt_name = str(attempt["attempt_name"])
    report_path = report_path_for_attempt(attempt_name)
    report_metrics = extract_mt5_strategy_report_metrics(report_path)
    parsed = parse_mt5_trade_report(report_path)
    trades = pair_deals_into_trades(parsed["deals"])
    feature = load_feature_frame(attempt)
    feature_by_key = {str(row["bar_key"]): row for row in feature.to_dict("records")}
    telemetry_by_key = load_telemetry_by_key(attempt_name)
    set_values = parse_set(ROOT / str(attempt["set"]["path"]))
    fixed_lot = safe_float(set_values.get("InpFixedLot"), 0.1)
    macro_payload = macro_lookup_payload(macros)
    trade_rows: list[dict[str, Any]] = []
    for trade in trades:
        open_key = trade.open_time.strftime("%Y.%m.%d %H:%M:%S")
        feature_row = feature_by_key.get(open_key, {})
        telemetry_row = telemetry_by_key.get(open_key, {})
        macro_values, macro_hit_count, macro_max_age_minutes = lookup_macro_asof(macro_payload, trade.open_time)
        hour = int(trade.open_time.hour)
        net = float(trade.net_profit)
        row = {
            "attempt_name": attempt_name,
            "artifact_slug": attempt.get("artifact_slug", ""),
            "feature_set_id": attempt.get("feature_set_id", ""),
            "trade_index": trade.index,
            "direction": trade.direction,
            "open_time": trade.open_time,
            "close_time": trade.close_time,
            "open_hour": hour,
            "close_month": trade.close_time.strftime("%Y-%m"),
            "weekday": trade.open_time.strftime("%a"),
            "hold_bars": max(0.0, (trade.close_time - trade.open_time).total_seconds() / 60.0 / 5.0),
            "volume": trade.volume,
            "open_price": trade.open_price,
            "close_price": trade.close_price,
            "gross_profit": float(trade.gross_profit),
            "net_profit": net,
            "net_per_lot": net / fixed_lot if fixed_lot else None,
            "swap": float(trade.swap),
            "commission": float(trade.commission),
            "feature_join_status": "matched" if feature_row else "missing",
            "telemetry_join_status": "matched" if telemetry_row else "missing",
            "macro_join_status": "all_matched" if macro_hit_count == len(macro_payload) else ("partial_matched" if macro_hit_count else "missing"),
            "macro_max_age_minutes": macro_max_age_minutes,
            "runtime_decision": telemetry_row.get("decision", ""),
            "p_short": safe_float(telemetry_row.get("p_short")),
            "p_flat": safe_float(telemetry_row.get("p_flat")),
            "p_long": safe_float(telemetry_row.get("p_long")),
            "executed_lot": safe_float(telemetry_row.get("executed_lot")),
            "atr_points": safe_float(telemetry_row.get("atr_points")),
            "open_sl_points": safe_float(telemetry_row.get("open_sl_points")),
            "open_tp_points": safe_float(telemetry_row.get("open_tp_points")),
            "session_bucket": session_bucket(feature_row.get("minutes_from_cash_open"), hour),
            "volatility_bucket": group_bucket(feature_row.get("historical_vol_20"), (0.0006, 0.0012), "histvol20"),
            "adx_bucket": adx_bucket(feature_row.get("adx_14")),
            "di_spread_sign": "di_positive" if safe_float(feature_row.get("di_spread_14"), 0.0) > 0 else ("di_negative" if safe_float(feature_row.get("di_spread_14"), 0.0) < 0 else "di_flat_or_missing"),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        row.update(macro_values)
        trade_rows.append(row)
    curve = trade_curve_stats(trade_rows)
    values = [safe_float(row["net_profit"], 0.0) for row in trade_rows]
    long_values = [safe_float(row["net_profit"], 0.0) for row in trade_rows if row["direction"] == "buy"]
    short_values = [safe_float(row["net_profit"], 0.0) for row in trade_rows if row["direction"] == "sell"]
    first = min((row["open_time"] for row in trade_rows), default=None)
    last = max((row["close_time"] for row in trade_rows), default=None)
    day_span = (last - first).total_seconds() / 86400.0 if first is not None and last is not None else math.nan
    summary = {
        "attempt_name": attempt_name,
        "artifact_slug": attempt.get("artifact_slug", ""),
        "feature_set_id": attempt.get("feature_set_id", ""),
        "model_id": attempt.get("model_id", ""),
        "report_path": rel(report_path),
        "trade_count": len(trade_rows),
        "net_profit": sum(values),
        "profit_factor": profit_factor(values),
        "expectancy": sum(values) / len(values) if values else None,
        "win_rate": sum(1 for value in values if value > 0) / len(values) if values else None,
        "gross_profit": sum(value for value in values if value > 0),
        "gross_loss": sum(value for value in values if value < 0),
        "calendar_days": day_span,
        "trades_per_calendar_day": len(trade_rows) / day_span if day_span and day_span > 0 else None,
        "closed_balance_max_drawdown": curve["closed_balance_max_drawdown"],
        "recovery_factor_closed": sum(values) / curve["closed_balance_max_drawdown"] if curve["closed_balance_max_drawdown"] else None,
        "underwater_trade_share": curve["underwater_trade_share"],
        "longest_underwater_trades": curve["longest_underwater_trades"],
        "long_trade_count": len(long_values),
        "short_trade_count": len(short_values),
        "long_net_profit": sum(long_values),
        "short_net_profit": sum(short_values),
        "net_per_lot": sum(values) / fixed_lot if fixed_lot else None,
        "fixed_lot": fixed_lot,
        "report_net_profit": report_metrics.get("net_profit"),
        "report_profit_factor": report_metrics.get("profit_factor"),
        "runtime_net_profit": runtime_row.get("net_profit", ""),
        "runtime_profit_factor": runtime_row.get("profit_factor", ""),
        "runtime_trade_count": runtime_row.get("trade_count", ""),
        "feature_join_match_count": sum(1 for row in trade_rows if row["feature_join_status"] == "matched"),
        "telemetry_join_match_count": sum(1 for row in trade_rows if row["telemetry_join_status"] == "matched"),
        "macro_join_all_match_count": sum(1 for row in trade_rows if row["macro_join_status"] == "all_matched"),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    cost_rows = []
    for cost in COST_STRESS:
        stressed = [safe_float(row["net_profit"], 0.0) - cost for row in trade_rows]
        stressed_rows = [{**row, "stressed_net_profit": stressed[idx]} for idx, row in enumerate(trade_rows)]
        stressed_curve = trade_curve_stats(stressed_rows, "stressed_net_profit")
        cost_rows.append(
            {
                "attempt_name": attempt_name,
                "extra_cost_per_trade": cost,
                "trade_count": len(stressed),
                "net_profit": sum(stressed),
                "profit_factor": profit_factor(stressed),
                "expectancy": sum(stressed) / len(stressed) if stressed else None,
                "closed_balance_max_drawdown": stressed_curve["closed_balance_max_drawdown"],
                "recovery_factor_closed": sum(stressed) / stressed_curve["closed_balance_max_drawdown"] if stressed_curve["closed_balance_max_drawdown"] else None,
                "survives_positive_net": sum(stressed) > 0,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    slice_rows: list[dict[str, Any]] = []
    axes = [
        "direction",
        "session_bucket",
        "open_hour",
        "close_month",
        "weekday",
        "volatility_bucket",
        "adx_bucket",
        "di_spread_sign",
        "vix_level_bucket",
        "vix_change_bucket",
        "usdx_level_bucket",
        "usdx_change_bucket",
        "us10yr_level_bucket",
        "us10yr_change_bucket",
    ]
    for axis in axes:
        for item in group_summary(trade_rows, axis):
            slice_rows.append({"attempt_name": attempt_name, "axis": axis, **item, "claim_boundary": CLAIM_BOUNDARY})
    return trade_rows, summary, cost_rows, rolling_pockets(trade_rows, attempt_name), slice_rows


def classify_attempt(row: Mapping[str, Any], cost_rows: Sequence[Mapping[str, Any]], pocket_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    attempt = str(row["attempt_name"])
    attempt_cost = [item for item in cost_rows if item["attempt_name"] == attempt]
    attempt_pockets = [item for item in pocket_rows if item["attempt_name"] == attempt]
    cost05 = next((safe_float(item["net_profit"]) for item in attempt_cost if safe_float(item["extra_cost_per_trade"]) == 0.5), math.nan)
    cost10 = next((safe_float(item["net_profit"]) for item in attempt_cost if safe_float(item["extra_cost_per_trade"]) == 1.0), math.nan)
    worst20 = next((safe_float(item["worst_window_net"]) for item in attempt_pockets if safe_int(item["rolling_window_trades"]) == 20), math.nan)
    score = 0
    reasons: list[str] = []
    if safe_float(row["net_profit"]) > 0:
        score += 2
    else:
        reasons.append("net_non_positive")
    if safe_float(row["profit_factor"]) >= 1.2:
        score += 2
    else:
        reasons.append("pf_below_1_2")
    if safe_float(row["trades_per_calendar_day"]) >= 4:
        score += 2
    else:
        reasons.append("density_below_4_per_day")
    if safe_float(row["recovery_factor_closed"]) >= 1:
        score += 2
    else:
        reasons.append("recovery_below_1")
    if safe_float(row["long_net_profit"]) > 0 and safe_float(row["short_net_profit"]) > 0:
        score += 2
    else:
        reasons.append("direction_asymmetry")
    if safe_float(cost05) > 0:
        score += 2
    else:
        reasons.append("fails_cost_0_5")
    if safe_float(cost10) > 0:
        score += 1
    else:
        reasons.append("fails_cost_1_0")
    if safe_float(worst20) > -50:
        score += 1
    else:
        reasons.append("rolling20_pocket_deep")
    if safe_float(row["underwater_trade_share"]) <= 0.7:
        score += 1
    else:
        reasons.append("underwater_share_high")
    if score >= 12:
        label = "strong_research_clue_not_forward_pass"
    elif score >= 8:
        label = "usable_but_fragile_research_clue"
    elif score >= 5:
        label = "fragile_failure_memory"
    else:
        label = "failure_memory_only"
    return {
        "attempt_name": attempt,
        "artifact_slug": row.get("artifact_slug", ""),
        "feature_set_id": row.get("feature_set_id", ""),
        "net_profit": row.get("net_profit"),
        "profit_factor": row.get("profit_factor"),
        "trade_count": row.get("trade_count"),
        "trades_per_calendar_day": row.get("trades_per_calendar_day"),
        "closed_balance_max_drawdown": row.get("closed_balance_max_drawdown"),
        "recovery_factor_closed": row.get("recovery_factor_closed"),
        "underwater_trade_share": row.get("underwater_trade_share"),
        "long_net_profit": row.get("long_net_profit"),
        "short_net_profit": row.get("short_net_profit"),
        "cost_plus_0_5_net": cost05,
        "cost_plus_1_0_net": cost10,
        "rolling20_worst_net": worst20,
        "forward_robustness_score": score,
        "forward_subset_judgment": label,
        "failure_axes": ";".join(reasons) if reasons else "none_in_scored_subset",
        "selection_eligible": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_reports(scorecard: Sequence[Mapping[str, Any]], findings: Sequence[Mapping[str, Any]]) -> list[Path]:
    top_rows = "\n".join(
        "| {attempt} | {score} | {net} | {pf} | {tpd} | {c05} | {c10} | {fail} |".format(
            attempt=row["attempt_name"],
            score=row["forward_robustness_score"],
            net=csv_value(row["net_profit"]),
            pf=csv_value(row["profit_factor"]),
            tpd=csv_value(row["trades_per_calendar_day"]),
            c05=csv_value(row["cost_plus_0_5_net"]),
            c10=csv_value(row["cost_plus_1_0_net"]),
            fail=row["failure_axes"],
        )
        for row in scorecard
    )
    finding_lines = "\n".join(f"- {row['finding_id']}: {row['finding']}" for row in findings)
    report = f"""# run336O Repaired Forward Attribution and Cost Stress(336O 수리 전진 귀속 및 비용 압박)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Scorecard(점수표)

| attempt(시도) | score(점수) | net(순익) | PF(수익 팩터) | trades/day(일 거래) | cost+0.5 net | cost+1.0 net | failure axes(실패 축) |
|---|---:|---:|---:|---:|---:|---:|---|
{top_rows}

## Findings(발견)

{finding_lines}

## Boundary(경계)

Action(행동): run336M MT5 report(보고서)와 trade deal list(딜 목록)를 거래 단위로 분해해 cost stress(비용 압박), curve pocket(곡선 포켓), direction/session/month/regime slice(방향/세션/월/국면 조각)를 계산했다.

Effect(효과): repaired handoff(수리 인계)는 동작하지만, 비용과 방향/곡선 취약성이 남아 Forward Passed(전진 통과)나 Goal Achieve(목표 달성)를 주장할 수 없다. 이 결과는 next research handoff(다음 연구 인계)와 failure memory(실패 기억)에만 쓴다.
"""
    decision_doc = f"""# Stage336O Decision(336O 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): run336O(336O 실행)는 수리된 forward subset(전진 부분집합)의 취약 축을 비용/방향/곡선/국면으로 고정했다. 다음은 failure memory handoff(실패 기억 인계) 또는 명시적 forward decision review(전진 판정 검토)다.
"""
    return [write_md(REPORT_PATH, report), write_md(DECISION_DOC, decision_doc)]


def build_findings(scorecard: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]], pocket_rows: Sequence[Mapping[str, Any]], slice_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    cost10_fail = sum(1 for row in scorecard if safe_float(row["cost_plus_1_0_net"]) <= 0)
    short_drag = sum(1 for row in scorecard if safe_float(row["short_net_profit"]) <= 0)
    weak_recovery = sum(1 for row in scorecard if safe_float(row["recovery_factor_closed"]) < 1)
    deep20 = sum(1 for row in scorecard if safe_float(row["rolling20_worst_net"]) <= -50)
    low_density = sum(1 for row in scorecard if safe_float(row["trades_per_calendar_day"]) < 4)
    worst_slice = min(slice_rows, key=lambda row: safe_float(row.get("net_profit"), 0.0)) if slice_rows else {}
    return [
        {
            "finding_id": "cost_buffer_fragility",
            "severity": "high",
            "finding": f"{cost10_fail}/4 attempts lose positive net under extra_cost_per_trade=1.0.",
            "next_probe": "new R&D should improve expectancy before raising trade count; do not retune forward threshold.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "direction_asymmetry",
            "severity": "high",
            "finding": f"{short_drag}/4 attempts have non-positive short-side net profit.",
            "next_probe": "carry side-separated failure memory; avoid cosmetic short repair on forward data.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "curve_recovery_fragility",
            "severity": "high",
            "finding": f"{weak_recovery}/4 attempts have recovery_factor_closed < 1 and {deep20}/4 have rolling20 worst net <= -50.",
            "next_probe": "require curve-pocket constraints in next research stage before any operating claim.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "density_quality_tradeoff",
            "severity": "medium",
            "finding": f"{low_density}/4 attempts remain below 4 trades/day after repaired handoff.",
            "next_probe": "search for quality-preserving density, not lot or threshold optimization.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "worst_regime_slice",
            "severity": "medium",
            "finding": f"worst slice: attempt={worst_slice.get('attempt_name','')}, axis={worst_slice.get('axis','')}, bucket={worst_slice.get('bucket','')}, net={csv_value(worst_slice.get('net_profit',''))}.",
            "next_probe": "use as failure memory; no post-forward filter is selected here.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def update_status_docs(scorecard: Sequence[Mapping[str, Any]]) -> list[Path]:
    best = max(scorecard, key=lambda row: safe_float(row["forward_robustness_score"], -1)) if scorecard else {}
    summary = (
        f"- run336O_summary(336O 요약): repaired forward attribution/cost stress(수리 전진 귀속/비용 압박)를 `{STATUS}`로 완료했다. "
        f"Effect(효과): best repaired clue(최선 수리 단서)는 `{best.get('attempt_name','')}` score(점수) `{best.get('forward_robustness_score','')}`지만, cost/direction/curve fragility(비용/방향/곡선 취약성)가 남아 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    artifacts: list[Path] = []
    text, had_bom = read_text_lossless(CURRENT_STATE)
    text = replace_prefix_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(text, "- status(상태):", f"- status(상태): `{STATUS}`")
    text = replace_prefix_line(text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
    text = append_after_header(text, "- decision(결정):", summary)
    write_text_preserving(CURRENT_STATE, text, had_bom)
    artifacts.append(CURRENT_STATE)

    text, had_bom = read_text_lossless(WORKSPACE_STATE)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage336(336단계) run336O(336O 실행)는 `{STATUS}`로 cost/direction/curve/regime attribution(비용/방향/곡선/국면 귀속)을 완료했다. "
        "Effect(효과): repaired subset(수리 부분집합)은 동작하지만 cost buffer/direction symmetry/curve recovery(비용 버퍼/방향 대칭/곡선 회복)가 부족해 Forward Passed(전진 통과)는 주장하지 않는다."
    )
    if "Stage336(336단계) run336O(336O 실행)" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
    write_text_preserving(WORKSPACE_STATE, text, had_bom)
    artifacts.append(WORKSPACE_STATE)

    selection = f"""# Stage336 Selection Status(336단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `335_overfit_guard__failure_memory_constrained_research_handoff`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_materialization(최신 물질화): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run336O(336O 실행)는 repaired subset(수리 부분집합)의 비용/방향/곡선 취약성을 failure memory(실패 기억)로 고정했다. 후보 선택이나 운영 주장은 없다.
"""
    artifacts.append(write_md(SELECTED_STATUS, selection))

    changelog = f"""## Stage336O Repaired Forward Attribution and Cost Stress(336O 수리 전진 귀속 및 비용 압박)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run336M(336M 실행)의 MT5 report/deal list(보고서/딜 목록)를 trade-level(거래 수준)로 분해해 cost stress(비용 압박), curve pocket(곡선 포켓), direction/session/month/regime slice(방향/세션/월/국면 조각)를 계산했다.
- effect(효과): repaired handoff(수리 인계)는 동작하지만 cost/direction/curve fragility(비용/방향/곡선 취약성)가 남아 Forward Passed(전진 통과)와 Goal Achieve(목표 달성)는 주장하지 않는다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    artifacts.append(append_if_missing(CHANGELOG, "Stage336O Repaired Forward Attribution", changelog))
    return artifacts


def write_receipts(scorecard: Sequence[Mapping[str, Any]], trade_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    return [
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "run_id": RUN_ID,
                "data_source": "run336M MT5 reports, telemetry, repaired feature CSV, and raw macro M5 probes",
                "time_axis": "MT5 report trade open/close server timestamps joined exactly to feature bar_time_server; raw macro time_close_unix is converted to inferred MT5 server time and joined with backward as-of no-future fill audited by age columns",
                "sample_scope": "four run336M repaired attempts, 2026-04-14 through latest tester output",
                "missing_or_duplicate_check": "trade-feature and trade-telemetry exact joins retained as missing buckets when absent; macro joins use backward as-of no-future fill and record age/missing state",
                "feature_label_boundary": "no labels or outcomes used to alter model, threshold, lot, or risk",
                "split_boundary": "forward-only repaired runtime probe",
                "leakage_risk": "regime slices use open-time features/macros only; no post-forward filter selected",
                "data_hash_or_identity": rel(RUN_DIR / "trade_level_records.csv"),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(RUN336M_DIR / "runtime_execution_result.json"),
                "shared_contract": "same repaired run336M MT5 outputs; no new runtime logic",
                "known_differences": "analysis-only attribution over existing reports",
                "parity_check": rel(RUN336N_DIR / "timestamp_aligned_proxy_mt5_difference.csv"),
                "runtime_claim_boundary": "runtime_probe",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "backtest_forensics_receipt.json",
            {
                "run_id": RUN_ID,
                "tester_identity": rel(RUN336M_DIR / "tester_settings_identity.json"),
                "ea_identity": rel(RUN336M_DIR / "runtime_execution_result.json"),
                "report_identity": rel(RUN_DIR / "report_metric_reparse_audit.csv"),
                "trade_evidence": f"trade rows parsed={len(trade_rows)} from MT5 deal lists",
                "cost_assumptions": "synthetic extra cost per closed trade applied after original MT5 result; original spread/slippage unchanged",
                "forensic_checks": "report metrics reparsed, trade count compared, cost stress computed",
                "backtest_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "performance_attribution_receipt.json",
            {
                "run_id": RUN_ID,
                "observed_change": "repaired feature handoff made latest-forward MT5 runnable; attribution shows uneven quality",
                "comparison_baseline": "run336M headline MT5 results and run336N parity pass",
                "likely_drivers": "thin expectancy, direction asymmetry, and rolling curve pockets",
                "segment_checks": "direction, session, hour, month, volatility, ADX, VIX, USDX, US10YR, cost, rolling windows",
                "trade_shape": f"attempts={len(scorecard)}; total_trades={len(trade_rows)}",
                "alternative_explanations": "tester cycle coverage and current partial-session rows remain analysis boundary, not model mismatch",
                "attribution_confidence": "medium",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "run_id": RUN_ID,
                "result_subject": "repaired forward subset attribution and cost stress",
                "evidence_available": "trade-level report parse, cost stress, curve pocket, regime slices, scorecard",
                "evidence_missing": "core56 equity refresh, full final forward passed/failed decision review",
                "judgment_label": "runtime_probe",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "수리된 인계는 돌아가지만 비용/방향/곡선이 아직 깨끗하지 않아 성공 선언은 금지된다.",
            },
        ),
    ]


def update_registers(artifact_paths: Sequence[Path]) -> list[Path]:
    artifacts = [
        append_register_row(
            RUN_REGISTRY,
            ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "forward_attribution_cost_stress",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            },
        ),
        append_register_row(
            STAGE_LEDGER,
            ["ledger_row_id", "stage_id", "run_id", "work_family", "evidence_scope", "kpi_scope", "status", "judgment", "claim_boundary", "path", "notes", "decision"],
            {
                "ledger_row_id": f"{RUN_ID}__forward_attribution_cost_stress",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "forward_attribution_cost_stress",
                "evidence_scope": "run336M_repaired_mt5_trade_reports",
                "kpi_scope": "cost_direction_curve_regime_no_forward_decision",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_PATH),
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "decision": DECISION,
            },
        ),
        append_register_row(
            ALPHA_LEDGER,
            [
                "ledger_row_id",
                "stage_id",
                "run_id",
                "subrun_id",
                "parent_run_id",
                "record_view",
                "tier_scope",
                "kpi_scope",
                "scoreboard_lane",
                "status",
                "judgment",
                "path",
                "primary_kpi",
                "guardrail_kpi",
                "external_verification_status",
                "notes",
            ],
            {
                "ledger_row_id": f"{RUN_ID}__actual_repaired_runtime_total",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "actual_repaired_runtime_total",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "actual_runtime_probe_review",
                "tier_scope": "not_applicable_repaired_forward_subset",
                "kpi_scope": "cost_direction_curve_regime_no_forward_decision",
                "scoreboard_lane": "runtime_probe_trade_shape",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": "forward_robustness_scorecard",
                "guardrail_kpi": "cost_stress;curve_pocket;direction_asymmetry;runtime_join_status",
                "external_verification_status": "completed",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            },
        ),
    ]
    existing_artifact_rows: list[list[str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader, None)
            for existing in reader:
                if len(existing) > 5 and existing[5] == RUN_ID:
                    continue
                existing_artifact_rows.append(existing)
    with io_path(ARTIFACT_REGISTRY).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"])
        writer.writerows(existing_artifact_rows)
        for path in artifact_paths:
            if not path_exists(path) or io_path(path).is_dir():
                continue
            digest = sha256_file_lf_normalized(path) if path.suffix.lower() in {".csv", ".json", ".md", ".txt", ".py"} else ""
            writer.writerow([f"{RUN_ID}::{rel(path)}", path.suffix.lstrip(".") or "file", rel(path), digest, STAGE_ID, RUN_ID, TODAY + "T00:00:00Z", "run336O_forward_attribution_artifact"])
    artifacts.append(ARTIFACT_REGISTRY)
    return artifacts


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    generated_at_utc = now_utc()
    attempts = read_json(RUN336M_DIR / "independent_handoff_attempts.json")
    runtime_rows = {row["attempt_name"]: row for row in read_csv(RUN336M_DIR / "fresh_mt5_runtime_probe_result.csv")}
    server_utc_offset_minutes = infer_server_utc_offset_minutes(attempts)
    macros = {symbol: load_macro_frame(symbol, server_utc_offset_minutes) for symbol in ("VIX", "USDX", "US10YR")}
    all_trades: list[dict[str, Any]] = []
    attempt_summaries: list[dict[str, Any]] = []
    all_cost: list[dict[str, Any]] = []
    all_pockets: list[dict[str, Any]] = []
    all_slices: list[dict[str, Any]] = []
    report_audit: list[dict[str, Any]] = []
    for attempt in attempts:
        trade_rows, summary, cost_rows, pocket_rows, slice_rows = build_attempt_payload(attempt, runtime_rows[str(attempt["attempt_name"])], macros)
        all_trades.extend(trade_rows)
        attempt_summaries.append(summary)
        all_cost.extend(cost_rows)
        all_pockets.extend(pocket_rows)
        all_slices.extend(slice_rows)
        report_audit.append(
            {
                "attempt_name": attempt["attempt_name"],
                "runtime_trade_count": runtime_rows[str(attempt["attempt_name"])].get("trade_count", ""),
                "parsed_trade_count": summary["trade_count"],
                "runtime_net_profit": runtime_rows[str(attempt["attempt_name"])].get("net_profit", ""),
                "parsed_net_profit": summary["net_profit"],
                "runtime_profit_factor": runtime_rows[str(attempt["attempt_name"])].get("profit_factor", ""),
                "parsed_profit_factor": summary["profit_factor"],
                "report_path": summary["report_path"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    scorecard = sorted([classify_attempt(row, all_cost, all_pockets) for row in attempt_summaries], key=lambda row: (-safe_float(row["forward_robustness_score"]), -safe_float(row["net_profit"])))
    findings = build_findings(scorecard, all_cost, all_pockets, all_slices)
    artifact_paths: list[Path] = [
        write_time_axis_offset_audit(server_utc_offset_minutes, attempts),
        write_csv(
            RUN_DIR / "trade_level_records.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "trade_index",
                "direction",
                "open_time",
                "close_time",
                "open_hour",
                "close_month",
                "weekday",
                "hold_bars",
                "volume",
                "open_price",
                "close_price",
                "gross_profit",
                "net_profit",
                "net_per_lot",
                "swap",
                "commission",
                "feature_join_status",
                "telemetry_join_status",
                "macro_join_status",
                "macro_max_age_minutes",
                "runtime_decision",
                "p_short",
                "p_flat",
                "p_long",
                "executed_lot",
                "atr_points",
                "open_sl_points",
                "open_tp_points",
                "session_bucket",
                "volatility_bucket",
                "adx_bucket",
                "di_spread_sign",
                "vix_close",
                "vix_change_1",
                "vix_level_bucket",
                "vix_change_bucket",
                "vix_join_mode",
                "vix_age_minutes",
                "usdx_close",
                "usdx_change_1",
                "usdx_level_bucket",
                "usdx_change_bucket",
                "usdx_join_mode",
                "usdx_age_minutes",
                "us10yr_close",
                "us10yr_change_1",
                "us10yr_level_bucket",
                "us10yr_change_bucket",
                "us10yr_join_mode",
                "us10yr_age_minutes",
                "claim_boundary",
            ],
            all_trades,
        ),
        write_csv(
            RUN_DIR / "attempt_forward_attribution_summary.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "report_path",
                "trade_count",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "gross_profit",
                "gross_loss",
                "calendar_days",
                "trades_per_calendar_day",
                "closed_balance_max_drawdown",
                "recovery_factor_closed",
                "underwater_trade_share",
                "longest_underwater_trades",
                "long_trade_count",
                "short_trade_count",
                "long_net_profit",
                "short_net_profit",
                "net_per_lot",
                "fixed_lot",
                "report_net_profit",
                "report_profit_factor",
                "runtime_net_profit",
                "runtime_profit_factor",
                "runtime_trade_count",
                "feature_join_match_count",
                "telemetry_join_match_count",
                "macro_join_all_match_count",
                "claim_boundary",
            ],
            attempt_summaries,
        ),
        write_csv(
            RUN_DIR / "cost_stress_report.csv",
            ["attempt_name", "extra_cost_per_trade", "trade_count", "net_profit", "profit_factor", "expectancy", "closed_balance_max_drawdown", "recovery_factor_closed", "survives_positive_net", "claim_boundary"],
            all_cost,
        ),
        write_csv(
            RUN_DIR / "curve_pocket_report.csv",
            ["attempt_name", "rolling_window_trades", "worst_window_start_trade", "worst_window_end_trade", "worst_window_net", "best_window_start_trade", "best_window_end_trade", "best_window_net", "claim_boundary"],
            all_pockets,
        ),
        write_csv(
            RUN_DIR / "regime_direction_slice_report.csv",
            ["attempt_name", "axis", "bucket", "trade_count", "net_profit", "profit_factor", "expectancy", "win_rate", "claim_boundary"],
            all_slices,
        ),
        write_csv(
            RUN_DIR / "forward_robustness_scorecard.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "net_profit",
                "profit_factor",
                "trade_count",
                "trades_per_calendar_day",
                "closed_balance_max_drawdown",
                "recovery_factor_closed",
                "underwater_trade_share",
                "long_net_profit",
                "short_net_profit",
                "cost_plus_0_5_net",
                "cost_plus_1_0_net",
                "rolling20_worst_net",
                "forward_robustness_score",
                "forward_subset_judgment",
                "failure_axes",
                "selection_eligible",
                "claim_boundary",
            ],
            scorecard,
        ),
        write_csv(
            RUN_DIR / "forward_fragility_findings.csv",
            ["finding_id", "severity", "finding", "next_probe", "claim_boundary"],
            findings,
        ),
        write_csv(
            RUN_DIR / "report_metric_reparse_audit.csv",
            ["attempt_name", "runtime_trade_count", "parsed_trade_count", "runtime_net_profit", "parsed_net_profit", "runtime_profit_factor", "parsed_profit_factor", "report_path", "claim_boundary"],
            report_audit,
        ),
        write_csv(
            RUN_DIR / "run336P_failure_memory_queue.csv",
            ["queue_id", "source_finding", "required_action", "forbidden", "claim_boundary"],
            [
                {
                    "queue_id": "cost_direction_curve_failure_memory",
                    "source_finding": "cost_buffer_fragility;direction_asymmetry;curve_recovery_fragility",
                    "required_action": "carry failure axes into new no-retune R&D stage or explicit forward decision review",
                    "forbidden": "threshold retune; lot optimization; post-forward regime filter selection",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        ),
    ]
    artifact_paths.extend(write_reports(scorecard, findings))
    artifact_paths.extend(write_receipts(scorecard, all_trades))
    artifact_paths.extend(update_status_docs(scorecard))
    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "attempts": len(scorecard),
        "trade_rows": len(all_trades),
        "best_attempt": scorecard[0]["attempt_name"] if scorecard else "",
        "best_score": scorecard[0]["forward_robustness_score"] if scorecard else "",
        "server_utc_offset_minutes": server_utc_offset_minutes,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_paths.append(write_json(RUN_DIR / "final_repaired_forward_attribution_decision.json", final_decision))
    artifact_paths.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                **final_decision,
                "generated_at_utc": generated_at_utc,
                "parent_run_id": PARENT_RUN_ID,
                "artifacts": [rel(path) for path in [*artifact_paths, RUN_DIR / "run_manifest.json"]],
            },
        )
    )
    artifact_paths.extend(update_registers(artifact_paths))
    print(json.dumps(final_decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
