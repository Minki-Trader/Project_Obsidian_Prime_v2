from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


STAGE_ID = "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN_ID = "run330C_forward_mt5_or_score_curve_review_v1"
RUN_NUMBER = "run330C"
PARENT_RUN_ID = "run330B_materialize_forward_safe_non_identity_control_surfaces_v1"
SOURCE_MT5_RUN_ID = "run329F_forward_mt5_kpi_regime_cost_curve_review_v1"
NEXT_ACTION = "run330D_regime_attribution_v1"

STATUS = "completed_score_curve_cost_pressure_review_no_forward_decision"
JUDGMENT = "score_curve_cost_pressure_completed_research_only_no_forward_decision"
DECISION = "stage330C_score_curve_pressure_fragile_runtime_and_regime_review_next"
CLAIM_BOUNDARY = (
    "research_development_only_score_curve_proxy_and_session_mt5_reference_no_forward_threshold_tuning_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

FIXED_LOT = 0.1
HOLD_BARS = 12
COST_STEPS = [0.0, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0]

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN330B_DIR = STAGE_DIR / "02_runs" / "run330B"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SOURCE_STAGE_DIR = ROOT / "stages" / "329_onnx_rebuild__live_feature_control"
SOURCE_RUN329F_DIR = SOURCE_STAGE_DIR / "02_runs" / "run329F"
RAW_FORWARD_BARS = ROOT / "stages" / "326_forward__cp322a_frozen_forward_gate" / "01_inputs" / "raw_m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage330C_score_curve_cost_pressure_review.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, pd.Timestamp):
        if value.tzinfo is not None:
            value = value.tz_convert("UTC").tz_localize(None)
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig"), had_bom


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    if path.exists():
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    else:
        fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    index = {tuple(str(row.get(column, "")) for column in key_columns): pos for pos, row in enumerate(existing)}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {field: csv_value(row.get(field, "")) for field in fieldnames}
        if key in index:
            existing[index[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(existing)
    return path


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def safe_div(value: float | None, denom: float | None) -> float | None:
    if value is None or denom in (None, 0):
        return None
    return value / denom


def profit_factor(values: Sequence[float]) -> float | None:
    gross_profit = sum(value for value in values if value > 0)
    gross_loss = -sum(value for value in values if value < 0)
    if gross_loss == 0:
        return None if gross_profit == 0 else math.inf
    return gross_profit / gross_loss


def max_drawdown(values: Sequence[float]) -> float:
    equity = 0.0
    peak = 0.0
    worst = 0.0
    for value in values:
        equity += value
        peak = max(peak, equity)
        worst = max(worst, peak - equity)
    return worst


def underwater_stats(values: Sequence[float], times: Sequence[pd.Timestamp]) -> dict[str, Any]:
    equity = 0.0
    peak = 0.0
    current_start: pd.Timestamp | None = None
    current_len = 0
    worst_len = 0
    worst_start: pd.Timestamp | None = None
    worst_end: pd.Timestamp | None = None
    worst_dd = 0.0
    for value, timestamp in zip(values, times):
        equity += value
        if equity >= peak:
            peak = equity
            current_start = None
            current_len = 0
            continue
        if current_start is None:
            current_start = timestamp
            current_len = 0
        current_len += 1
        drawdown = peak - equity
        if current_len > worst_len or drawdown > worst_dd:
            worst_len = current_len
            worst_start = current_start
            worst_end = timestamp
            worst_dd = max(worst_dd, drawdown)
    return {
        "total_trade_count": len(values),
        "max_underwater_trade_count": worst_len,
        "max_underwater_start": worst_start,
        "max_underwater_end": worst_end,
        "max_drawdown": worst_dd,
    }


def aggregate(rows: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(tuple(row.get(key, "") for key in keys), []).append(row)
    output: list[dict[str, Any]] = []
    for key, group_rows in grouped.items():
        values = [float(row.get("proxy_net_profit", 0.0)) for row in group_rows]
        closes = [pd.Timestamp(row.get("close_time")) for row in group_rows]
        gross_profit = sum(value for value in values if value > 0)
        gross_loss = -sum(value for value in values if value < 0)
        output.append(
            {
                **dict(zip(keys, key)),
                "trade_count": len(group_rows),
                "net_profit": sum(values),
                "gross_profit": gross_profit,
                "gross_loss": gross_loss,
                "profit_factor": profit_factor(values),
                "expectancy": safe_div(sum(values), len(values)),
                "win_rate": safe_div(sum(1 for value in values if value > 0), len(values)),
                "max_drawdown": max_drawdown(values),
                **underwater_stats(values, closes),
            }
        )
    return output


def load_bars() -> pd.DataFrame:
    bars = pd.read_csv(
        io_path(RAW_FORWARD_BARS),
        usecols=["time_open_unix", "open", "high", "low", "close", "spread_points"],
    )
    bars["timestamp"] = pd.to_datetime(bars["time_open_unix"], unit="s", utc=True)
    for column in ("open", "high", "low", "close", "spread_points"):
        bars[column] = pd.to_numeric(bars[column], errors="coerce")
    return bars.sort_values("timestamp").drop_duplicates("timestamp", keep="last").reset_index(drop=True)


def load_manifest() -> list[dict[str, str]]:
    rows = read_csv_rows(RUN330B_DIR / "signal_payload_manifest.csv")
    if not rows:
        raise RuntimeError("run330B signal_payload_manifest.csv is missing or empty")
    return rows


def build_proxy_trades(bars: pd.DataFrame, manifest_rows: Sequence[Mapping[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    bar_index = {pd.Timestamp(row.timestamp): index for index, row in bars.iterrows()}
    all_trades: list[dict[str, Any]] = []
    coverage_rows: list[dict[str, Any]] = []
    for manifest in manifest_rows:
        payload_path = ROOT / str(manifest["signal_payload_path"])
        signals = pd.read_csv(io_path(payload_path))
        if signals.empty:
            coverage_rows.append(
                {
                    "artifact_slug": manifest["artifact_slug"],
                    "view_id": manifest["view_id"],
                    "signal_rows": 0,
                    "proxy_trade_count": 0,
                    "missing_bar_rows": 0,
                    "skipped_during_hold_rows": 0,
                    "coverage_judgment": "empty_signal_payload",
                }
            )
            continue
        signals["timestamp"] = pd.to_datetime(signals["timestamp"], utc=True, errors="coerce")
        signals = signals.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
        next_allowed: pd.Timestamp | None = None
        missing_bar_rows = 0
        skipped_during_hold_rows = 0
        trade_index = 0
        for signal in signals.to_dict("records"):
            timestamp = pd.Timestamp(signal["timestamp"])
            if next_allowed is not None and timestamp <= next_allowed:
                skipped_during_hold_rows += 1
                continue
            open_index = bar_index.get(timestamp)
            if open_index is None:
                missing_bar_rows += 1
                continue
            close_index = min(open_index + HOLD_BARS, len(bars) - 1)
            if close_index <= open_index:
                missing_bar_rows += 1
                continue
            open_bar = bars.iloc[open_index]
            close_bar = bars.iloc[close_index]
            direction = int(to_float(signal.get("signal_direction")) or 0)
            if direction == 0:
                continue
            entry_price = float(open_bar["close"])
            exit_price = float(close_bar["close"])
            point_return = direction * (exit_price - entry_price)
            net_profit = point_return * FIXED_LOT
            window = bars.iloc[open_index : close_index + 1]
            trade_index += 1
            next_allowed = pd.Timestamp(close_bar["timestamp"])
            all_trades.append(
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "source_type": "score_signal_proxy_nonoverlap_hold12_not_mt5",
                    "candidate_id": signal.get("candidate_id", manifest["candidate_id"]),
                    "artifact_slug": manifest["artifact_slug"],
                    "feature_set_id": signal.get("feature_set_id", ""),
                    "model_id": signal.get("model_id", ""),
                    "view_id": manifest["view_id"],
                    "trade_index": trade_index,
                    "direction": "long" if direction > 0 else "short",
                    "signal_timestamp": timestamp,
                    "open_time": pd.Timestamp(open_bar["timestamp"]),
                    "close_time": pd.Timestamp(close_bar["timestamp"]),
                    "hold_bars": close_index - open_index,
                    "fixed_lot": FIXED_LOT,
                    "entry_close": entry_price,
                    "exit_close": exit_price,
                    "point_return": point_return,
                    "proxy_net_profit": net_profit,
                    "max_probability": to_float(signal.get("max_probability")),
                    "probability_margin": to_float(signal.get("probability_margin")),
                    "decision_threshold": to_float(signal.get("decision_threshold")),
                    "hour": signal.get("hour_utc", ""),
                    "month": signal.get("month", ""),
                    "session_slice": signal.get("us_cash_session", ""),
                    "volatility_regime": signal.get("volatility_regime", ""),
                    "adx_regime": signal.get("adx_regime", ""),
                    "vix_regime": signal.get("vix_zscore_regime", ""),
                    "usd_regime": signal.get("usdx_zscore_regime", ""),
                    "rate_regime": signal.get("us10yr_zscore_regime", ""),
                    "spread_points_median_in_trade": float(window["spread_points"].median()),
                    "proxy_boundary": "score_signal_curve_proxy_not_mt5_not_forward_decision",
                }
            )
        proxy_trade_count = sum(
            1
            for trade in all_trades
            if trade["artifact_slug"] == manifest["artifact_slug"] and trade["view_id"] == manifest["view_id"]
        )
        coverage_rows.append(
            {
                "artifact_slug": manifest["artifact_slug"],
                "candidate_id": manifest["candidate_id"],
                "view_id": manifest["view_id"],
                "signal_rows": len(signals),
                "proxy_trade_count": proxy_trade_count,
                "missing_bar_rows": missing_bar_rows,
                "skipped_during_hold_rows": skipped_during_hold_rows,
                "signal_to_proxy_trade_compression": safe_div(len(signals), proxy_trade_count),
                "coverage_judgment": "usable_proxy_coverage" if proxy_trade_count else "blocked_no_proxy_trades",
            }
        )
    return all_trades, coverage_rows


def build_kpi_rows(trades: Sequence[Mapping[str, Any]], summary_rows: Sequence[Mapping[str, str]], coverage_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    coverage_by_key = {(row["artifact_slug"], row["view_id"]): row for row in coverage_rows}
    summary_by_key = {(row["artifact_slug"], row["view_id"]): row for row in summary_rows}
    rows: list[dict[str, Any]] = []
    for group in aggregate(trades, ["artifact_slug", "candidate_id", "feature_set_id", "model_id", "view_id"]):
        values = [float(trade["proxy_net_profit"]) for trade in trades if trade["artifact_slug"] == group["artifact_slug"] and trade["view_id"] == group["view_id"]]
        coverage = coverage_by_key.get((group["artifact_slug"], group["view_id"]), {})
        summary = summary_by_key.get((group["artifact_slug"], group["view_id"]), {})
        days = to_float(summary.get("days")) or 0.0
        dd = to_float(group.get("max_drawdown")) or 0.0
        net = to_float(group.get("net_profit")) or 0.0
        rows.append(
            {
                **group,
                "days": days,
                "signals_per_day": to_float(summary.get("signals_per_day")),
                "proxy_trades_per_day": safe_div(group["trade_count"], days),
                "signal_rows": coverage.get("signal_rows", ""),
                "signal_to_proxy_trade_compression": coverage.get("signal_to_proxy_trade_compression", ""),
                "recovery_factor": safe_div(net, dd),
                "fixed_lot": FIXED_LOT,
                "hold_bars_policy": HOLD_BARS,
                "profit_factor_is_finite": math.isfinite(profit_factor(values) or math.inf),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def split_chunks(rows: Sequence[Mapping[str, Any]], count: int) -> list[list[Mapping[str, Any]]]:
    if not rows:
        return []
    size = math.ceil(len(rows) / count)
    return [list(rows[index : index + size]) for index in range(0, len(rows), size)]


def build_curve_rows(trades: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    curve_rows: list[dict[str, Any]] = []
    underwater_rows: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for trade in sorted(trades, key=lambda item: (item["artifact_slug"], item["view_id"], item["close_time"])):
        grouped.setdefault((str(trade["artifact_slug"]), str(trade["view_id"])), []).append(trade)
    for (artifact_slug, view_id), group in grouped.items():
        for idx, chunk in enumerate(split_chunks(group, 3), start=1):
            stats = aggregate(chunk, ["artifact_slug", "candidate_id", "feature_set_id", "model_id", "view_id"])[0]
            curve_rows.append(
                {
                    **stats,
                    "chunk_type": "thirds",
                    "chunk_id": f"third_{idx}",
                    "start_time": chunk[0]["open_time"],
                    "end_time": chunk[-1]["close_time"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        if len(group) >= 20:
            windows: list[tuple[int, list[Mapping[str, Any]], float]] = []
            for start in range(0, len(group) - 19):
                window = group[start : start + 20]
                windows.append((start, list(window), sum(float(row["proxy_net_profit"]) for row in window)))
            start, window, _ = min(windows, key=lambda item: item[2])
            stats = aggregate(window, ["artifact_slug", "candidate_id", "feature_set_id", "model_id", "view_id"])[0]
            curve_rows.append(
                {
                    **stats,
                    "chunk_type": "rolling_worst_net",
                    "chunk_id": f"rolling_20_start_{start + 1}",
                    "start_time": window[0]["open_time"],
                    "end_time": window[-1]["close_time"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        values = [float(row["proxy_net_profit"]) for row in group]
        times = [pd.Timestamp(row["close_time"]) for row in group]
        underwater_rows.append(
            {
                "artifact_slug": artifact_slug,
                "view_id": view_id,
                **underwater_stats(values, times),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return curve_rows, underwater_rows


def build_cost_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for trade in trades:
        grouped.setdefault((str(trade["artifact_slug"]), str(trade["view_id"])), []).append(trade)
    for (artifact_slug, view_id), group in grouped.items():
        base = group[0]
        for cost in COST_STEPS:
            values = [float(trade["proxy_net_profit"]) - cost for trade in group]
            rows.append(
                {
                    "artifact_slug": artifact_slug,
                    "candidate_id": base["candidate_id"],
                    "view_id": view_id,
                    "extra_cost_per_round_trip_account_ccy": cost,
                    "net_profit_after_cost": sum(values),
                    "profit_factor_after_cost": profit_factor(values),
                    "expectancy_after_cost": safe_div(sum(values), len(values)),
                    "max_drawdown_after_cost": max_drawdown(values),
                    "survives_pf_gt_1": (profit_factor(values) or 0.0) > 1.0,
                    "stress_boundary": "score_proxy_synthetic_round_trip_cost_not_mt5_no_threshold_or_lot_repair",
                }
            )
    return rows


def build_lot_rows(kpi_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in kpi_rows:
        rows.append(
            {
                "artifact_slug": row["artifact_slug"],
                "candidate_id": row["candidate_id"],
                "view_id": row["view_id"],
                "fixed_lot": FIXED_LOT,
                "net_profit_at_fixed_lot": row["net_profit"],
                "equity_dd_amount_at_fixed_lot": row["max_drawdown"],
                "net_profit_per_1lot_linear": safe_div(to_float(row.get("net_profit")), FIXED_LOT),
                "equity_dd_amount_per_1lot_linear": safe_div(to_float(row.get("max_drawdown")), FIXED_LOT),
                "expectancy_per_1lot_linear": safe_div(to_float(row.get("expectancy")), FIXED_LOT),
                "normalization_boundary": "linear_lot_normalization_only_not_new_lot_optimization_score_proxy",
            }
        )
    return rows


def build_source_direction_rows(trades: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    long_short = aggregate(trades, ["artifact_slug", "candidate_id", "view_id", "direction"])
    regime_rows: list[dict[str, Any]] = []
    axes = [
        ("session", "session_slice"),
        ("hour", "hour"),
        ("month", "month"),
        ("volatility", "volatility_regime"),
        ("adx", "adx_regime"),
        ("vix", "vix_regime"),
        ("usd", "usd_regime"),
        ("rate", "rate_regime"),
    ]
    for axis, key in axes:
        rows = aggregate(trades, ["artifact_slug", "candidate_id", "view_id", key])
        for row in rows:
            row["axis"] = axis
            row["bucket"] = row.pop(key)
            row["claim_boundary"] = CLAIM_BOUNDARY
            regime_rows.append(row)
    db_rows = []
    for slug in sorted({str(trade["artifact_slug"]) for trade in trades}):
        db_rows.append(
            {
                "artifact_slug": slug,
                "db_source": "not_applicable_no_db_decision_surface",
                "status": "out_of_scope_by_claim",
                "reason": "Stage330 non-identity controls do not contain the original cp322A D/B source surface.",
                "effect": "D/B attribution is recorded as unavailable so it cannot support Forward Passed.",
            }
        )
    return long_short, regime_rows, db_rows


def read_source_mt5_reference() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    kpi = read_csv_rows(SOURCE_RUN329F_DIR / "forward_mt5_kpi_report.csv")
    cost = read_csv_rows(SOURCE_RUN329F_DIR / "cost_stress_report.csv")
    curve = read_csv_rows(SOURCE_RUN329F_DIR / "curve_pocket_report.csv")
    trade = read_csv_rows(SOURCE_RUN329F_DIR / "trade_level_records.csv")
    for rows in (kpi, cost, curve, trade):
        for row in rows:
            row["source_run_id"] = SOURCE_MT5_RUN_ID
            row["stage330_reference_boundary"] = "session_parity_mt5_reference_only_raw_forward_mt5_not_claimed"
            if "view_id" not in row:
                row["view_id"] = "old_session_parity"
    return kpi, cost, curve, trade


def build_bridge_rows(kpi_rows: Sequence[Mapping[str, Any]], mt5_kpi_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    proxy_by_slug = {
        str(row["artifact_slug"]): row
        for row in kpi_rows
        if str(row.get("view_id")) == "old_session_parity"
    }
    output: list[dict[str, Any]] = []
    for mt5_row in mt5_kpi_rows:
        slug = str(mt5_row.get("artifact_slug", ""))
        proxy = proxy_by_slug.get(slug, {})
        mt5_net = to_float(mt5_row.get("net_profit"))
        proxy_net = to_float(proxy.get("net_profit"))
        mt5_pf = to_float(mt5_row.get("profit_factor"))
        proxy_pf = to_float(proxy.get("profit_factor"))
        same_sign = (
            proxy_net is not None
            and mt5_net is not None
            and ((proxy_net >= 0 and mt5_net >= 0) or (proxy_net < 0 and mt5_net < 0))
        )
        output.append(
            {
                "artifact_slug": slug,
                "view_id": "old_session_parity",
                "score_proxy_trade_count": proxy.get("trade_count", ""),
                "mt5_trade_count": mt5_row.get("trade_count", ""),
                "score_proxy_net_profit": proxy_net,
                "mt5_net_profit": mt5_net,
                "net_delta_proxy_minus_mt5": None if proxy_net is None or mt5_net is None else proxy_net - mt5_net,
                "score_proxy_profit_factor": proxy_pf,
                "mt5_profit_factor": mt5_pf,
                "same_net_sign": same_sign,
                "bridge_judgment": "directional_proxy_only_not_mt5_replacement" if same_sign else "proxy_mt5_shape_disagreement_pressure",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_raw_session_gap_rows(
    kpi_rows: Sequence[Mapping[str, Any]],
    raw_session_rows: Sequence[Mapping[str, str]],
    mt5_kpi_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_key = {(row["artifact_slug"], row["view_id"]): row for row in kpi_rows}
    mt5_by_slug = {str(row.get("artifact_slug")): row for row in mt5_kpi_rows}
    output: list[dict[str, Any]] = []
    for guard in raw_session_rows:
        slug = guard["artifact_slug"]
        raw = by_key.get((slug, "raw_forward"), {})
        session = by_key.get((slug, "old_session_parity"), {})
        mt5 = mt5_by_slug.get(slug, {})
        raw_net = to_float(raw.get("net_profit"))
        session_net = to_float(session.get("net_profit"))
        mt5_net = to_float(mt5.get("net_profit"))
        raw_pf = to_float(raw.get("profit_factor"))
        session_pf = to_float(session.get("profit_factor"))
        output.append(
            {
                "artifact_slug": slug,
                "candidate_id": guard.get("candidate_id"),
                "gap_judgment": guard.get("gap_judgment"),
                "raw_session_row_ratio": to_float(guard.get("raw_session_row_ratio")),
                "raw_session_signal_per_day_ratio": to_float(guard.get("raw_session_signal_per_day_ratio")),
                "exclusive_raw_signal_rate": to_float(guard.get("exclusive_raw_signal_rate")),
                "raw_proxy_trade_count": raw.get("trade_count", ""),
                "session_proxy_trade_count": session.get("trade_count", ""),
                "session_mt5_trade_count": mt5.get("trade_count", ""),
                "raw_proxy_net_profit": raw_net,
                "session_proxy_net_profit": session_net,
                "session_mt5_net_profit": mt5_net,
                "raw_minus_session_proxy_net": None if raw_net is None or session_net is None else raw_net - session_net,
                "raw_proxy_profit_factor": raw_pf,
                "session_proxy_profit_factor": session_pf,
                "pressure_judgment": pressure_judgment(guard, raw, session),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def pressure_judgment(guard: Mapping[str, Any], raw: Mapping[str, Any], session: Mapping[str, Any]) -> str:
    if guard.get("gap_judgment") == "raw_session_gap_high_pressure":
        return "high_pressure_raw_density_blocks_forward_pass_claim"
    raw_pf = to_float(raw.get("profit_factor")) or 0.0
    session_pf = to_float(session.get("profit_factor")) or 0.0
    if raw_pf < 1.0 and session_pf >= 1.0:
        return "raw_proxy_curve_degrades_versus_session"
    return "review_band_no_selection"


def build_decision_payload(
    kpi_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    high_pressure = sum(1 for row in gap_rows if "high_pressure" in str(row.get("pressure_judgment", "")))
    cost_failures = sum(
        1
        for row in cost_rows
        if float(row.get("extra_cost_per_round_trip_account_ccy") or 0.0) <= 1.0 and not row.get("survives_pf_gt_1")
    )
    worst_curve = min((to_float(row.get("net_profit")) or 0.0 for row in curve_rows), default=0.0)
    best_raw_net = max(
        (to_float(row.get("net_profit")) or -math.inf for row in kpi_rows if row.get("view_id") == "raw_forward"),
        default=-math.inf,
    )
    if high_pressure or cost_failures or worst_curve < 0:
        decision_reason = "curve_cost_or_raw_session_pressure_requires_more_runtime_and_regime_attribution"
    else:
        decision_reason = "score_proxy_did_not_find_immediate_pressure_but_mt5_and_regime_evidence_missing"
    return {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "selected_candidate": "none",
        "best_raw_proxy_net_profit": None if best_raw_net == -math.inf else best_raw_net,
        "high_pressure_raw_session_count": high_pressure,
        "cost_failures_at_or_below_1": cost_failures,
        "worst_curve_pocket_net": worst_curve,
        "reason": decision_reason,
        "next_action": NEXT_ACTION,
    }


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_name": "T04_curve_pocket_and_underwater",
            "status": "completed_score_proxy_and_session_mt5_reference",
            "evidence_path": rel(RUN_DIR / "score_curve_pocket_report.csv"),
            "effect": "곡선 포켓과 수중 구간을 MT5 주장 없이 먼저 드러낸다.",
        },
        {
            "gate_name": "T05_cost_stress",
            "status": "completed_score_proxy_cost_pressure",
            "evidence_path": rel(RUN_DIR / "score_cost_stress_report.csv"),
            "effect": "비용을 붙였을 때 신호가 얼마나 빨리 무너지는지 본다.",
        },
        {
            "gate_name": "T09_lot_normalized_review_partial",
            "status": "completed_proxy_only",
            "evidence_path": rel(RUN_DIR / "score_lot_normalized_report.csv"),
            "effect": "로트 최적화 없이 1 lot 선형 환산만 남긴다.",
        },
        {
            "gate_name": "runtime_mt5_raw_forward",
            "status": "not_completed_out_of_scope_by_claim_in_run330C",
            "evidence_path": rel(RUN_DIR / "runtime_parity_receipt.json"),
            "effect": "raw-forward MT5 결과가 없음을 명시해 Forward Passed로 오독하지 않게 한다.",
        },
    ]


def lineage_payload(generated_at_utc: str, artifacts: Sequence[Path]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runs": [PARENT_RUN_ID, SOURCE_MT5_RUN_ID],
        "generated_at_utc": generated_at_utc,
        "inputs": [
            {"path": rel(RUN330B_DIR / "signal_payload_manifest.csv"), "sha256": sha256_file(RUN330B_DIR / "signal_payload_manifest.csv")},
            {"path": rel(RUN330B_DIR / "raw_session_gap_guard.csv"), "sha256": sha256_file(RUN330B_DIR / "raw_session_gap_guard.csv")},
            {"path": rel(SOURCE_RUN329F_DIR / "forward_mt5_kpi_report.csv"), "sha256": sha256_file(SOURCE_RUN329F_DIR / "forward_mt5_kpi_report.csv")},
            {"path": rel(RAW_FORWARD_BARS), "sha256": sha256_file(RAW_FORWARD_BARS)},
        ],
        "artifacts": [
            {"path": rel(path), "sha256": sha256_file(path), "artifact_type": infer_artifact_type(path)}
            for path in artifacts
            if path.exists()
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def infer_artifact_type(path: Path) -> str:
    if path.suffix.lower() == ".json":
        return "json_receipt"
    if path.suffix.lower() == ".md":
        return "review_report"
    if path.suffix.lower() == ".py":
        return "pipeline_script"
    return "csv_report"


def write_outputs(generated_at_utc: str) -> tuple[list[Path], dict[str, Any]]:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows = load_manifest()
    summary_rows = read_csv_rows(RUN330B_DIR / "fixed_threshold_replay_summary.csv")
    raw_session_guard = read_csv_rows(RUN330B_DIR / "raw_session_gap_guard.csv")
    bars = load_bars()
    proxy_trades, coverage_rows = build_proxy_trades(bars, manifest_rows)
    if not proxy_trades:
        raise RuntimeError("run330C cannot proceed because no score proxy trades were generated")

    kpi_rows = build_kpi_rows(proxy_trades, summary_rows, coverage_rows)
    curve_rows, underwater_rows = build_curve_rows(proxy_trades)
    cost_rows = build_cost_rows(proxy_trades)
    lot_rows = build_lot_rows(kpi_rows)
    long_short_rows, regime_rows, db_rows = build_source_direction_rows(proxy_trades)
    mt5_kpi, mt5_cost, mt5_curve, mt5_trades = read_source_mt5_reference()
    bridge_rows = build_bridge_rows(kpi_rows, mt5_kpi)
    gap_rows = build_raw_session_gap_rows(kpi_rows, raw_session_guard, mt5_kpi)
    decision_payload = build_decision_payload(kpi_rows, cost_rows, curve_rows, gap_rows)

    artifacts: list[Path] = []
    artifacts.append(write_csv(RUN_DIR / "score_proxy_trade_records.csv", list(proxy_trades[0].keys()), proxy_trades))
    artifacts.append(write_csv(RUN_DIR / "score_curve_proxy_kpi_report.csv", list(kpi_rows[0].keys()), kpi_rows))
    artifacts.append(write_csv(RUN_DIR / "score_proxy_coverage_audit.csv", list(coverage_rows[0].keys()), coverage_rows))
    artifacts.append(write_csv(RUN_DIR / "score_curve_pocket_report.csv", list(curve_rows[0].keys()), curve_rows))
    artifacts.append(write_csv(RUN_DIR / "score_underwater_stretch_report.csv", list(underwater_rows[0].keys()), underwater_rows))
    artifacts.append(write_csv(RUN_DIR / "score_cost_stress_report.csv", list(cost_rows[0].keys()), cost_rows))
    artifacts.append(write_csv(RUN_DIR / "score_lot_normalized_report.csv", list(lot_rows[0].keys()), lot_rows))
    artifacts.append(write_csv(RUN_DIR / "score_long_short_attribution_report.csv", list(long_short_rows[0].keys()), long_short_rows))
    artifacts.append(write_csv(RUN_DIR / "score_regime_attribution_proxy_report.csv", list(regime_rows[0].keys()), regime_rows))
    artifacts.append(write_csv(RUN_DIR / "session_hour_month_volatility_adx_vix_usd_rate_slices.csv", list(regime_rows[0].keys()), regime_rows))
    artifacts.append(write_csv(RUN_DIR / "db_attribution_report.csv", list(db_rows[0].keys()), db_rows))
    artifacts.append(write_csv(RUN_DIR / "score_mt5_bridge_comparison.csv", list(bridge_rows[0].keys()), bridge_rows))
    artifacts.append(write_csv(RUN_DIR / "raw_session_curve_gap_report.csv", list(gap_rows[0].keys()), gap_rows))
    artifacts.append(write_csv(RUN_DIR / "session_mt5_reference_kpi_report.csv", list(mt5_kpi[0].keys()) if mt5_kpi else [], mt5_kpi))
    artifacts.append(write_csv(RUN_DIR / "session_mt5_reference_cost_stress_report.csv", list(mt5_cost[0].keys()) if mt5_cost else [], mt5_cost))
    artifacts.append(write_csv(RUN_DIR / "session_mt5_reference_curve_pocket_report.csv", list(mt5_curve[0].keys()) if mt5_curve else [], mt5_curve))
    artifacts.append(write_csv(RUN_DIR / "session_mt5_reference_trade_records.csv", list(mt5_trades[0].keys()) if mt5_trades else [], mt5_trades))
    artifacts.append(write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate_name", "status", "evidence_path", "effect"], gate_rows()))

    artifacts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [
                    rel(RUN330B_DIR / "signal_payload_manifest.csv"),
                    rel(RAW_FORWARD_BARS),
                    rel(SOURCE_RUN329F_DIR / "forward_mt5_kpi_report.csv"),
                ],
                "time_axis": "US100 M5 broker bars use MT5 API Unix seconds converted to UTC; signal timestamps are UTC bar opens.",
                "sample_scope": "2026-04-14+ latest forward raw and old-session parity views from run330B.",
                "missing_or_duplicate_check": "Exact timestamp coverage checked through score_proxy_coverage_audit.csv.",
                "feature_label_boundary": "No labels or future outcome columns are used for signal generation; forward outcome is read only for proxy scoring.",
                "split_boundary": "Latest forward holdout only; no threshold, feature, or lot tuning.",
                "leakage_risk": "Score proxy outcome is not a training input and cannot select or tune thresholds in this run.",
                "data_hash_or_identity": sha256_file(RUN330B_DIR / "signal_payload_manifest.csv"),
                "integrity_judgment": "usable_with_boundary_score_proxy_not_mt5",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "Stage329 research ONNX controls reused frozen in run330B payloads",
                "target_and_label": "No new label is built in run330C; score proxy reads forward price movement after fixed signals.",
                "split_method": "latest forward read-only pressure review",
                "selection_metric": "none_no_selection",
                "secondary_metrics": "curve pocket, underwater stretch, cost stress, direction and regime attribution",
                "threshold_policy": "fixed_train_only_threshold_from_run329C_run330B",
                "overfit_risk": "raw/session density explosion and old-session MT5 positivity may not generalize to raw forward supply",
                "calibration_risk": "probabilities are treated as ranking/signal scores, not calibrated probabilities",
                "comparison_baseline": "run329F session-parity MT5 evidence and run330B raw/session signal density guard",
                "validation_judgment": JUDGMENT,
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": "No new raw-forward MT5 tester run in run330C; Stage329F session-parity MT5 reports are reference only.",
                "shared_contract": "run330B fixed signal payloads preserve timestamp, side, score, threshold, and view identity.",
                "known_differences": [
                    "score proxy uses non-overlap hold12 close-to-close movement and is not the MT5 EA fill/risk engine",
                    "raw_forward MT5 report is missing",
                    "Stage329F MT5 evidence covers old_session_parity only",
                ],
                "parity_check": "score_mt5_bridge_comparison.csv compares old_session score proxy with Stage329F MT5; raw MT5 remains missing",
                "parity_identity": {
                    "run330B_signal_manifest_sha256": sha256_file(RUN330B_DIR / "signal_payload_manifest.csv"),
                    "run329F_mt5_kpi_sha256": sha256_file(SOURCE_RUN329F_DIR / "forward_mt5_kpi_report.csv"),
                },
                "runtime_claim_boundary": "research_only_no_runtime_authority",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "backtest_forensics_receipt.json",
            {
                "tester_identity": "Stage329F session-parity tester identity is referenced; run330C does not create a new tester identity.",
                "ea_identity": "No new EA/set/package generated in run330C.",
                "report_identity": rel(SOURCE_RUN329F_DIR / "forward_mt5_kpi_report.csv"),
                "trade_evidence": "Stage329F trade list is copied as reference; score proxy trade list is separate and not tester output.",
                "cost_assumptions": "score proxy cost stress applies synthetic account-currency round-trip costs.",
                "forensic_checks": "MT5 reference and score proxy outputs are kept in separate files and bridge comparison.",
                "backtest_judgment": "usable_with_boundary_session_mt5_reference_only_raw_mt5_missing",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "performance_attribution_receipt.json",
            {
                "observed_change": "run330B signals are converted into score-curve proxy trades and compared with old-session MT5 reference.",
                "comparison_baseline": SOURCE_MT5_RUN_ID,
                "likely_drivers": "raw/session density, long/short skew, high-pressure controls, cost sensitivity, curve pocket concentration",
                "segment_checks": "view, direction, month, hour, session, volatility, ADX, VIX, USD, rate, curve thirds, rolling worst 20",
                "trade_shape": "score_curve_proxy_kpi_report.csv plus score_curve_pocket_report.csv",
                "alternative_explanations": "proxy fill model is not MT5; latest broker bars have documented tail gap in run330B",
                "attribution_confidence": "medium_for_score_proxy_low_for_runtime",
                "next_probe": NEXT_ACTION,
            },
        )
    )
    artifacts.append(write_json(RUN_DIR / "final_forward_decision.json", decision_payload))
    artifacts.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            [
                "run_id",
                "status",
                "judgment",
                "decision",
                "forward_passed",
                "forward_failed",
                "goal_achieve",
                "selected_candidate",
                "next_action",
                "claim_boundary",
            ],
            [{**decision_payload, "run_id": RUN_ID, "claim_boundary": CLAIM_BOUNDARY}],
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "source_mt5_run_id": SOURCE_MT5_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_action": NEXT_ACTION,
                "external_verification_status": "out_of_scope_by_claim_score_proxy_only_new_raw_mt5_not_run",
                "claim_boundary": CLAIM_BOUNDARY,
                "fixed_lot": FIXED_LOT,
                "hold_bars": HOLD_BARS,
                "score_proxy_trade_count": len(proxy_trades),
                "selected_candidate": "none",
                "goal_achieve": "not_claimed",
            },
        )
    )
    artifacts.append(Path(__file__))
    report_paths = write_reports(kpi_rows, gap_rows, bridge_rows, decision_payload)
    artifacts.extend(report_paths)
    artifacts.append(write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage_payload(generated_at_utc, artifacts)))
    return artifacts, decision_payload


def write_reports(
    kpi_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    bridge_rows: Sequence[Mapping[str, Any]],
    decision_payload: Mapping[str, Any],
) -> list[Path]:
    report_path = REVIEWS_DIR / "run330C_forward_score_curve_cost_pressure_review.md"
    decision_path = DECISION_DOC
    top_raw = sorted(
        [row for row in kpi_rows if row.get("view_id") == "raw_forward"],
        key=lambda row: to_float(row.get("net_profit")) or -math.inf,
        reverse=True,
    )[:6]
    top_lines = "\n".join(
        f"| {row['artifact_slug']} | {row['view_id']} | {csv_value(row['net_profit'])} | {csv_value(row['profit_factor'])} | {csv_value(row['trade_count'])} | {csv_value(row['max_drawdown'])} |"
        for row in top_raw
    )
    high_pressure = [row for row in gap_rows if "high_pressure" in str(row.get("pressure_judgment", ""))]
    bridge_bad = [row for row in bridge_rows if row.get("bridge_judgment") == "proxy_mt5_shape_disagreement_pressure"]
    report = f"""
# Run330C Forward Score-Curve Cost Pressure Review(330C 전진 점수 곡선 비용 압박 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Method(방법)

run330B(330B 실행)의 fixed threshold signal payload(고정 임계값 신호 인계물)를 그대로 읽고, `hold12 non-overlap score proxy(12봉 비중복 점수 대리검증)`를 만들었다. Effect(효과): MT5(`MetaTrader 5`, 메타트레이더5) fill(체결)과 risk logic(위험 로직)을 흉내 낸 성공 주장이 아니라, raw-forward(원본 전진) 공급이 곡선과 비용에서 먼저 깨지는지 보는 압박 판독이다.

Stage329F(329F 실행)의 old-session MT5(기존 세션 MT5)는 reference(참고)로만 복사했다. Effect(효과): 세션 동등 양수 결과를 raw-forward MT5 결과처럼 쓰지 못하게 한다.

## Raw Proxy Top Read(원본 대리검증 상위 판독)

| artifact(산출물) | view(보기) | net(순손익) | PF(수익 팩터) | trades(거래) | DD(손실폭) |
|---|---|---:|---:|---:|---:|
{top_lines}

## Pressure Read(압박 판독)

- raw/session high pressure count(원본/세션 고압 개수): `{decision_payload.get('high_pressure_raw_session_count')}`
- cost failures at or below +1(비용 +1 이하 실패): `{decision_payload.get('cost_failures_at_or_below_1')}`
- worst curve pocket net(최악 곡선 포켓 순손익): `{csv_value(decision_payload.get('worst_curve_pocket_net'))}`
- score/MT5 bridge disagreement(점수/MT5 연결 불일치): `{len(bridge_bad)}`

Effect(효과): 이 결과는 Forward Passed(전진 통과)가 아니라 run330D(330D 실행)의 regime/source attribution(국면/원천 귀속)과 이후 raw-forward MT5(원본 전진 MT5) 여부를 결정하는 압박 증거다.

## Key Files(주요 파일)

- score kpi(점수 핵심 지표): `{rel(RUN_DIR / 'score_curve_proxy_kpi_report.csv')}`
- curve pocket(곡선 포켓): `{rel(RUN_DIR / 'score_curve_pocket_report.csv')}`
- cost stress(비용 압박): `{rel(RUN_DIR / 'score_cost_stress_report.csv')}`
- lot normalized(로트 정규화): `{rel(RUN_DIR / 'score_lot_normalized_report.csv')}`
- raw/session gap(원본/세션 간극): `{rel(RUN_DIR / 'raw_session_curve_gap_report.csv')}`
- MT5 reference(메타트레이더5 참고): `{rel(RUN_DIR / 'session_mt5_reference_kpi_report.csv')}`

## Next(다음)

`{NEXT_ACTION}`
"""
    decision_doc = f"""
# Stage330C Score-Curve Cost Pressure Decision(330C 점수 곡선 비용 압박 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Reason(이유)

run330C(330C 실행)는 score proxy(점수 대리검증)와 Stage329F(329F 실행) session-parity MT5 reference(세션 동등 MT5 참고)를 분리했다. Effect(효과): raw-forward MT5(원본 전진 MT5)가 없는 상태에서 성공이나 실패를 최종 판정하지 않는다.

- high pressure raw/session rows(고압 원본/세션 행): `{len(high_pressure)}`
- bridge disagreement(연결 불일치): `{len(bridge_bad)}`
- next_action(다음 행동): `{NEXT_ACTION}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return [write_md(report_path, report), write_md(decision_path, decision_doc)]


def update_selection_status(decision_payload: Mapping[str, Any]) -> Path:
    text, had_bom = read_text_lossless(SELECTION_STATUS)
    replacements = {
        "- stage_status(": "- stage_status(단계 상태): `open_score_curve_pressure_completed`",
        "- latest_completed_run(": f"- latest_completed_run(최신 완료 실행): `{RUN_ID}`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_ACTION}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- effect(": "- effect(효과): run330C(330C 실행)는 점수 곡선/비용/로트/세션 MT5 참고를 만들었지만, raw-forward MT5가 없어 선택 후보와 Forward Passed(전진 통과)는 없다.",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    return write_text_lossless(SELECTION_STATUS, text, had_bom)


def update_current_truth(decision_payload: Mapping[str, Any]) -> list[Path]:
    updated: list[Path] = []
    state_text, state_bom = read_text_lossless(WORKSPACE_STATE)
    state_text = replace_prefix_line(state_text, "current_run_id:", f"current_run_id: {NEXT_ACTION}")
    focus_marker = "current_focus:\n"
    focus_entry = (
        "current_focus:\n"
        "- >-\n"
        "  Stage330(330단계) run330C(330C 실행)는 `completed_score_curve_cost_pressure_review_no_forward_decision`로 score-curve proxy(점수 곡선 대리검증)와 session MT5 reference(세션 MT5 참고)를 분리했다. Effect(효과): Forward Passed/Failed(전진 통과/실패) 없이 run330D(330D 실행)의 regime/source attribution(국면/원천 귀속)으로 넘긴다.\n"
    )
    if focus_marker in state_text and "run330C(330C 실행)는 `completed_score_curve_cost_pressure_review_no_forward_decision`" not in state_text:
        state_text = state_text.replace(focus_marker, focus_entry, 1)
    block_marker = "stage330C_score_curve_cost_pressure_review:"
    if block_marker not in state_text:
        state_text = state_text.rstrip() + f"""

stage330C_score_curve_cost_pressure_review:
  run_id: {RUN_ID}
  status: {STATUS}
  decision: {DECISION}
  next_action: {NEXT_ACTION}
  selected_candidate: none
  forward_passed: not_claimed
  forward_failed: not_claimed
  goal_achieve: not_claimed
  effect: score_curve_proxy_and_session_mt5_reference_created_without_raw_forward_mt5_or_selection
"""
    updated.append(write_text_lossless(WORKSPACE_STATE, state_text, state_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_run(", f"- current_run(현재 실행): `{NEXT_ACTION}`")
    current_text = replace_prefix_line(current_text, "- status(", "- status(상태): `stage330_run330C_score_curve_pressure_completed_regime_attribution_next`")
    current_text = replace_prefix_line(current_text, "- decision(", f"- decision(판정): `{DECISION}`")
    current_text = replace_prefix_line(current_text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    summary = (
        "- run330C_summary(330C 요약): score-curve/cost/lot/regime proxy(점수 곡선/비용/로트/국면 대리검증)와 Stage329F session MT5 reference(세션 MT5 참고)를 `completed_score_curve_cost_pressure_review_no_forward_decision`로 닫았다. "
        "Effect(효과): raw-forward MT5(원본 전진 MT5)가 없어 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 없다."
    )
    if "run330C_summary(330C 요약)" not in current_text:
        current_text = current_text.replace("- run330B_summary", summary + "\n- run330B_summary", 1)
    updated.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    stage_block = f"""
## run330C_score_curve_cost_pressure_summary(330C 점수 곡선 비용 압박 요약)

- run(실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): score proxy(점수 대리검증)와 session MT5 reference(세션 MT5 참고)를 분리했고, raw-forward MT5(원본 전진 MT5)가 없어서 선택 후보와 Forward Passed(전진 통과)는 없다.
"""
    updated.append(append_if_missing(STAGE_BRIEF, "run330C_score_curve_cost_pressure_summary", stage_block))
    changelog_entry = f"- 2026-05-26: Stage330(330단계) `{RUN_ID}` score-curve/cost pressure review(점수 곡선/비용 압박 검토)를 완료했다. 효과(effect, 효과): raw-forward MT5 없이 점수 대리검증과 세션 MT5 참고를 분리하고 Goal Achieve(목표 달성)는 주장하지 않는다."
    updated.append(append_if_missing(CHANGELOG, RUN_ID, changelog_entry))
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run330C_forward_score_curve_cost_pressure_review.md"
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "forward_score_curve_review",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "notes": "score_proxy_curve_cost_lot_pressure;session_mt5_reference_only;raw_mt5_not_claimed;goal_achieve_not_claimed.",
    }
    upsert_csv(RUN_REGISTRY, ["run_id"], [run_row])
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__score_curve_cost_pressure",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "score_curve_cost_pressure",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "score_curve_proxy_and_session_mt5_reference",
        "tier_scope": "latest_forward_raw_and_old_session_parity",
        "kpi_scope": "score_proxy_curve_cost_lot_and_mt5_reference",
        "scoreboard_lane": "performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "primary_kpi": "score_proxy_net_pf_curve_pocket",
        "guardrail_kpi": "raw_session_gap;cost_stress;score_mt5_bridge",
        "external_verification_status": "out_of_scope_by_claim_score_proxy_only_new_raw_mt5_not_run",
        "notes": "No candidate selection, no Forward Passed/Failed, no runtime authority.",
    }
    upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [ledger_row])
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__score_curve_cost_pressure",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "score_curve_cost_pressure_review(점수 곡선 비용 압박 검토)",
                "tier_scope": "latest forward raw/session views(최신 전진 원본/세션 보기)",
                "scoreboard": "performance_attribution_runtime_boundary(성과 귀속 런타임 경계)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selection;no_forward_decision;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows = []
    for path in artifacts:
        if not path.exists():
            continue
        artifact_rows.append(
            {
                "artifact_id": f"run330C_{path.stem}",
                "artifact_type": infer_artifact_type(path),
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": "Run330C score-curve/cost pressure artifact; no Forward Passed/Failed claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage330C score-curve/cost pressure review.")
    parser.add_argument("--generated-at-utc", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generated_at_utc = args.generated_at_utc or utc_now()
    artifacts, decision_payload = write_outputs(generated_at_utc)
    artifacts.extend([update_selection_status(decision_payload), *update_current_truth(decision_payload)])
    update_registers(generated_at_utc, artifacts)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "artifact_count": len([path for path in artifacts if path.exists()]),
                "selected_candidate": "none",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
