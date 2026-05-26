from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5.trade_report import Trade, pair_deals_into_trades, parse_mt5_trade_report  # noqa: E402


STAGE_ID = "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN_ID = "run330F_raw_forward_mt5_kpi_regime_cost_curve_review_v1"
RUN_NUMBER = "run330F"
PARENT_RUN_ID = "run330E_mt5_runtime_probe_or_block_v1"
EXPLORATION_LABEL = "stage330_Review__RawForwardMt5RegimeCostCurve"
CLAIM_BOUNDARY = (
    "research_development_only_forward_mt5_review_no_threshold_retuning_no_candidate_selection_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
STATUS = "completed_raw_forward_mt5_kpi_regime_cost_curve_review_no_final_forward_decision"
JUDGMENT = "raw_forward_mt5_review_completed_research_only_no_goal_achieve"
DECISION = "stage330F_raw_forward_mt5_evidence_mixed_overfit_fragility_review_required_no_selection"
NEXT_ACTION = "run330G_raw_forward_failure_fragility_memory_and_overfit_followup"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN330E_DIR = STAGE_DIR / "02_runs" / "run330E"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage330F_raw_forward_mt5_review.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RAW_FORWARD_BARS = ROOT / "stages" / "326_forward__cp322a_frozen_forward_gate" / "01_inputs" / "raw_m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
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
    body = text.strip() + "\n"
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(body)
    return path


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
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8"))


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
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def load_attempts() -> list[dict[str, Any]]:
    return read_json(RUN330E_DIR / "mt5_probe_attempts.json")


def load_bars() -> pd.DataFrame:
    bars = pd.read_csv(
        io_path(RAW_FORWARD_BARS),
        usecols=["time_open_unix", "open", "high", "low", "close", "spread_points"],
    )
    bars["timestamp_key"] = pd.to_datetime(bars["time_open_unix"], unit="s")
    for column in ("open", "high", "low", "close", "spread_points"):
        bars[column] = pd.to_numeric(bars[column], errors="coerce")
    return bars.sort_values("timestamp_key").reset_index(drop=True)


def load_features(attempt: Mapping[str, Any]) -> pd.DataFrame:
    feature_path = ROOT / str(attempt["feature_export"]["path"])
    features = pd.read_csv(io_path(feature_path))
    features["timestamp_key"] = pd.to_datetime(features["bar_time_server"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    for column in features.columns:
        if column not in {"bar_time_server", "timestamp_utc", "timestamp_key"}:
            features[column] = pd.to_numeric(features[column], errors="coerce")
    return features.sort_values("timestamp_key").drop_duplicates("timestamp_key", keep="last").reset_index(drop=True)


def load_telemetry(attempt: Mapping[str, Any]) -> pd.DataFrame:
    telemetry_path = RUN330E_DIR / "runtime_telemetry" / f"{attempt['attempt_name']}_telemetry.csv"
    telemetry = pd.read_csv(io_path(telemetry_path))
    telemetry["timestamp_key"] = pd.to_datetime(telemetry["bar_time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    return telemetry


def feature_at(features: pd.DataFrame, timestamp: pd.Timestamp) -> Mapping[str, Any]:
    exact = features.loc[features["timestamp_key"].eq(timestamp)]
    if not exact.empty:
        return exact.iloc[-1].to_dict()
    prior = features.loc[features["timestamp_key"].le(timestamp)].tail(1)
    if not prior.empty:
        delta = timestamp - pd.Timestamp(prior.iloc[-1]["timestamp_key"])
        if pd.Timedelta(0) <= delta <= pd.Timedelta(minutes=5):
            return prior.iloc[-1].to_dict()
    return {}


def bars_window(bars: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    window = bars.loc[(bars["timestamp_key"] >= start) & (bars["timestamp_key"] < end)]
    if window.empty:
        window = bars.loc[bars["timestamp_key"].eq(start)]
    return window


def parse_attempt_trades(report: Mapping[str, Any]) -> list[Trade]:
    report_path = Path(str(report.get("html_report", {}).get("path", "")))
    parsed = parse_mt5_trade_report(report_path)
    return pair_deals_into_trades(parsed["deals"])


def classify_session(minutes: Any) -> str:
    value = to_float(minutes)
    if value is None:
        return "feature_missing"
    if 0 < value <= 110:
        return "early"
    if value <= 220:
        return "mid"
    if value <= 330:
        return "late"
    return "outside_cash_session"


def quantile_bucket(value: Any, low: float | None, high: float | None, prefix: str) -> str:
    number = to_float(value)
    if number is None or low is None or high is None:
        return f"{prefix}_missing"
    if number <= low:
        return f"{prefix}_low"
    if number <= high:
        return f"{prefix}_mid"
    return f"{prefix}_high"


def z_bucket(value: Any, prefix: str) -> str:
    number = to_float(value)
    if number is None:
        return f"{prefix}_missing"
    if number < -0.5:
        return f"{prefix}_low"
    if number <= 0.5:
        return f"{prefix}_mid"
    return f"{prefix}_high"


def adx_bucket(value: Any) -> str:
    number = to_float(value)
    if number is None:
        return "adx_missing"
    if number < 20:
        return "adx_lt20"
    if number <= 25:
        return "adx_20_25"
    return "adx_gt25"


def trend_bucket(feature: Mapping[str, Any]) -> str:
    adx = to_float(feature.get("adx_14"))
    state = to_float(feature.get("supertrend_10_3"))
    if adx is None or state is None:
        return "trend_missing"
    if adx < 20:
        return "range_or_weak_trend"
    return "uptrend" if state > 0 else "downtrend"


def signed_bucket(value: Any, prefix: str) -> str:
    number = to_float(value)
    if number is None:
        return f"{prefix}_missing"
    if number > 0:
        return f"{prefix}_up"
    if number < 0:
        return f"{prefix}_down"
    return f"{prefix}_flat"


def to_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def metric_summary(values: Sequence[float]) -> dict[str, Any]:
    vals = [float(value) for value in values]
    gross_profit = sum(value for value in vals if value > 0.0)
    gross_loss = sum(value for value in vals if value < 0.0)
    trade_count = len(vals)
    wins = sum(1 for value in vals if value > 0.0)
    return {
        "trade_count": trade_count,
        "net_profit": round(sum(vals), 6),
        "gross_profit": round(gross_profit, 6),
        "gross_loss": round(gross_loss, 6),
        "profit_factor": round(gross_profit / abs(gross_loss), 6) if gross_loss < 0 else None,
        "expectancy": round(sum(vals) / trade_count, 6) if trade_count else None,
        "win_rate": round(wins / trade_count, 6) if trade_count else None,
        "max_drawdown": round(max_drawdown(vals), 6),
    }


def max_drawdown(values: Sequence[float]) -> float:
    equity = 0.0
    peak = 0.0
    worst = 0.0
    for value in values:
        equity += float(value)
        peak = max(peak, equity)
        worst = min(worst, equity - peak)
    return abs(worst)


def underwater_stats(values: Sequence[float], times: Sequence[pd.Timestamp]) -> dict[str, Any]:
    equity = 0.0
    peak = 0.0
    current_len = 0
    current_start: pd.Timestamp | None = None
    worst_len = 0
    worst_start: pd.Timestamp | None = None
    worst_end: pd.Timestamp | None = None
    for value, timestamp in zip(values, times, strict=False):
        equity += float(value)
        if equity >= peak:
            peak = equity
            current_len = 0
            current_start = None
            continue
        if current_len == 0:
            current_start = timestamp
        current_len += 1
        if current_len > worst_len:
            worst_len = current_len
            worst_start = current_start
            worst_end = timestamp
    return {
        "max_underwater_trade_count": worst_len,
        "max_underwater_start": worst_start,
        "max_underwater_end": worst_end,
    }


def aggregate(rows: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, ...], list[float]] = {}
    for row in rows:
        key = tuple(str(row.get(column, "missing")) for column in keys)
        grouped.setdefault(key, []).append(float(row.get("net_profit") or 0.0))
    result: list[dict[str, Any]] = []
    for key, values in sorted(grouped.items()):
        payload = {column: value for column, value in zip(keys, key, strict=False)}
        payload.update(metric_summary(values))
        result.append(payload)
    return result


def attempt_report_by_name(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row["attempt_name"]): row for row in execution_result.get("strategy_tester_reports", [])}


def build_trade_rows(
    attempts: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
    bars: pd.DataFrame,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    reports = attempt_report_by_name(execution_result)
    trade_rows: list[dict[str, Any]] = []
    long_short_rows: list[dict[str, Any]] = []
    kpi_rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        report = reports[attempt_name]
        metrics = dict(report.get("metrics", {}))
        trades = parse_attempt_trades(report)
        features = load_features(attempt)
        telemetry = load_telemetry(attempt)
        cycle = telemetry.loc[telemetry["record_type"].eq("cycle")].copy()
        cycle_days = int(cycle["timestamp_key"].dt.date.nunique())
        vol_low, vol_high = quantile_edges(features.get("historical_vol_20"))
        spread_low, spread_high = quantile_edges(bars.get("spread_points"))
        enriched: list[dict[str, Any]] = []
        for trade in trades:
            feature = feature_at(features, trade.open_time)
            window = bars_window(bars, trade.open_time, trade.close_time)
            high = to_float(window["high"].max() if not window.empty else None) or trade.open_price
            low = to_float(window["low"].min() if not window.empty else None) or trade.open_price
            if trade.direction == "buy":
                mfe_points = max(0.0, high - trade.open_price)
                mae_points = max(0.0, trade.open_price - low)
            else:
                mfe_points = max(0.0, trade.open_price - low)
                mae_points = max(0.0, high - trade.open_price)
            spread = to_float(window["spread_points"].median() if not window.empty else None)
            row = {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "attempt_name": attempt_name,
                "candidate_id": attempt["candidate_id"],
                "artifact_slug": attempt["artifact_slug"],
                "feature_set_id": attempt["feature_set_id"],
                "model_id": attempt["model_id"],
                "trade_index": trade.index,
                "direction": trade.direction,
                "open_time": trade.open_time,
                "close_time": trade.close_time,
                "hold_bars": round((trade.close_time - trade.open_time).total_seconds() / 60.0 / 5.0, 6),
                "volume": trade.volume,
                "open_price": trade.open_price,
                "close_price": trade.close_price,
                "net_profit": trade.net_profit,
                "gross_profit": trade.gross_profit,
                "commission": trade.commission,
                "swap": trade.swap,
                "mfe_points": round(mfe_points, 6),
                "mae_points": round(mae_points, 6),
                "realized_over_mfe_points": round(trade.net_profit / mfe_points, 6) if mfe_points else None,
                "session_slice": classify_session(feature.get("minutes_from_cash_open")),
                "hour": trade.open_time.hour,
                "month": trade.close_time.strftime("%Y-%m"),
                "volatility_regime": quantile_bucket(feature.get("historical_vol_20"), vol_low, vol_high, "vol"),
                "adx_bucket": adx_bucket(feature.get("adx_14")),
                "trend_regime": trend_bucket(feature),
                "vix_regime": z_bucket(feature.get("vix_zscore_20"), "vix"),
                "vix_change_regime": signed_bucket(feature.get("vix_change_1"), "vix_change"),
                "usd_regime": z_bucket(feature.get("usdx_zscore_20"), "usdx"),
                "usd_change_regime": signed_bucket(feature.get("usdx_change_1"), "usdx_change"),
                "rate_regime": z_bucket(feature.get("us10yr_zscore_20"), "us10yr"),
                "rate_change_regime": signed_bucket(feature.get("us10yr_change_1"), "us10yr_change"),
                "spread_regime": quantile_bucket(spread, spread_low, spread_high, "spread"),
                "spread_points_median_in_trade": spread,
                "db_source": "not_applicable_no_db_decision_surface",
            }
            enriched.append(row)
            trade_rows.append(row)
        values = [float(row["net_profit"]) for row in enriched]
        times = [pd.Timestamp(row["close_time"]) for row in enriched]
        recomputed = metric_summary(values)
        underwater = underwater_stats(values, times)
        kpi_rows.append(
            {
                "attempt_name": attempt_name,
                "candidate_id": attempt["candidate_id"],
                "artifact_slug": attempt["artifact_slug"],
                "feature_set_id": attempt["feature_set_id"],
                "model_id": attempt["model_id"],
                "session_days": cycle_days,
                "rows_evaluated": int(cycle.shape[0]),
                "signal_count": int(cycle["decision"].isin(["long", "short"]).sum()),
                "order_attempt_count": int(cycle["order_attempted"].astype(str).str.lower().eq("true").sum()),
                "order_fill_count": int(cycle["order_filled"].astype(str).str.lower().eq("true").sum()),
                "trade_count": metrics.get("trade_count"),
                "trades_per_day": round(float(metrics.get("trade_count") or 0) / cycle_days, 6) if cycle_days else None,
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "expectancy": metrics.get("expectancy"),
                "recovery_factor": metrics.get("recovery_factor"),
                "equity_dd_amount": metrics.get("equity_drawdown_maximal_amount"),
                "equity_dd_percent": metrics.get("equity_drawdown_maximal_percent"),
                "long_trade_count": metrics.get("long_trade_count"),
                "short_trade_count": metrics.get("short_trade_count"),
                "long_win_rate_percent": metrics.get("long_win_rate_percent"),
                "short_win_rate_percent": metrics.get("short_win_rate_percent"),
                "recomputed_net_profit": recomputed["net_profit"],
                "recomputed_profit_factor": recomputed["profit_factor"],
                "recomputed_max_drawdown": recomputed["max_drawdown"],
                "net_recompute_delta": round(float(metrics.get("net_profit") or 0.0) - float(recomputed["net_profit"]), 6),
                **underwater,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        long_short_rows.extend(aggregate(enriched, ["attempt_name", "artifact_slug", "direction"]))
    return trade_rows, long_short_rows, kpi_rows


def quantile_edges(series: Any) -> tuple[float | None, float | None]:
    if series is None:
        return None, None
    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if numeric.empty:
        return None, None
    return float(numeric.quantile(0.33)), float(numeric.quantile(0.66))


def build_regime_rows(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    axes = [
        "session_slice",
        "hour",
        "month",
        "volatility_regime",
        "adx_bucket",
        "trend_regime",
        "vix_regime",
        "vix_change_regime",
        "usd_regime",
        "usd_change_regime",
        "rate_regime",
        "rate_change_regime",
        "spread_regime",
    ]
    rows: list[dict[str, Any]] = []
    for axis in axes:
        for row in aggregate(trade_rows, ["attempt_name", "artifact_slug", axis]):
            bucket = row.pop(axis)
            row.update({"axis": axis, "bucket": bucket})
            rows.append(row)
    return rows


def build_db_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "attempt_name": attempt["attempt_name"],
            "artifact_slug": attempt["artifact_slug"],
            "candidate_id": attempt["candidate_id"],
            "db_source": "not_applicable",
            "status": "out_of_scope_by_claim",
            "reason": "run330B forward-safe non-identity control surfaces use a single ONNX probability surface; no D/B decision-source field exists in run330E telemetry.",
            "effect": "D/B attribution is not invented; a future cp322A exact D/B handoff repair must carry source tags before D/B attribution can be claimed.",
        }
        for attempt in attempts
    ]


def build_lot_rows(kpi_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in kpi_rows:
        lot = 0.10
        rows.append(
            {
                "attempt_name": row["attempt_name"],
                "artifact_slug": row["artifact_slug"],
                "fixed_lot": lot,
                "net_profit_at_fixed_lot": row["net_profit"],
                "equity_dd_amount_at_fixed_lot": row["equity_dd_amount"],
                "net_profit_per_1lot_linear": safe_div(row["net_profit"], lot),
                "equity_dd_amount_per_1lot_linear": safe_div(row["equity_dd_amount"], lot),
                "expectancy_per_1lot_linear": safe_div(row["expectancy"], lot),
                "normalization_boundary": "linear_lot_normalization_only_not_new_lot_optimization",
            }
        )
    return rows


def safe_div(value: Any, denom: float) -> float | None:
    number = to_float(value)
    if number is None or denom == 0:
        return None
    return round(number / denom, 6)


def build_cost_rows(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    costs = [0.0, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0]
    rows: list[dict[str, Any]] = []
    by_attempt: dict[str, list[Mapping[str, Any]]] = {}
    for row in trade_rows:
        by_attempt.setdefault(str(row["attempt_name"]), []).append(row)
    for attempt_name, trades in sorted(by_attempt.items()):
        artifact = str(trades[0]["artifact_slug"])
        base_values = [float(row["net_profit"]) for row in trades]
        for cost in costs:
            stressed = [value - cost for value in base_values]
            metrics = metric_summary(stressed)
            rows.append(
                {
                    "attempt_name": attempt_name,
                    "artifact_slug": artifact,
                    "extra_cost_per_round_trip_account_ccy": cost,
                    "net_profit_after_cost": metrics["net_profit"],
                    "profit_factor_after_cost": metrics["profit_factor"],
                    "expectancy_after_cost": metrics["expectancy"],
                    "max_drawdown_after_cost": metrics["max_drawdown"],
                    "survives_pf_gt_1": bool((metrics["profit_factor"] or 0.0) > 1.0),
                    "stress_boundary": "synthetic account-currency round-trip cost; no threshold, lot, or rule retuning",
                }
            )
    return rows


def build_curve_rows(trade_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_attempt: dict[str, list[Mapping[str, Any]]] = {}
    for row in trade_rows:
        by_attempt.setdefault(str(row["attempt_name"]), []).append(row)
    chunk_rows: list[dict[str, Any]] = []
    underwater_rows: list[dict[str, Any]] = []
    for attempt_name, rows in sorted(by_attempt.items()):
        ordered = sorted(rows, key=lambda row: (pd.Timestamp(row["close_time"]), int(row["trade_index"])))
        values = [float(row["net_profit"]) for row in ordered]
        times = [pd.Timestamp(row["close_time"]) for row in ordered]
        artifact = str(ordered[0]["artifact_slug"])
        underwater = underwater_stats(values, times)
        underwater.update(
            {
                "attempt_name": attempt_name,
                "artifact_slug": artifact,
                "total_trade_count": len(ordered),
                "max_drawdown": max_drawdown(values),
            }
        )
        underwater_rows.append(underwater)
        thirds = split_chunks(ordered, 3)
        for idx, chunk in enumerate(thirds, start=1):
            chunk_values = [float(row["net_profit"]) for row in chunk]
            metrics = metric_summary(chunk_values)
            chunk_rows.append(
                {
                    "attempt_name": attempt_name,
                    "artifact_slug": artifact,
                    "chunk_type": "thirds",
                    "chunk_id": f"third_{idx}",
                    "start_time": chunk[0]["close_time"] if chunk else None,
                    "end_time": chunk[-1]["close_time"] if chunk else None,
                    **metrics,
                }
            )
        window = min(20, len(ordered))
        if window:
            windows = []
            for start in range(0, len(ordered) - window + 1):
                chunk = ordered[start : start + window]
                chunk_values = [float(row["net_profit"]) for row in chunk]
                metrics = metric_summary(chunk_values)
                windows.append((metrics["net_profit"], start, chunk, metrics))
            worst_net, start, chunk, metrics = min(windows, key=lambda item: item[0])
            chunk_rows.append(
                {
                    "attempt_name": attempt_name,
                    "artifact_slug": artifact,
                    "chunk_type": "rolling_worst_net",
                    "chunk_id": f"rolling_{window}_start_{start + 1}",
                    "start_time": chunk[0]["close_time"],
                    "end_time": chunk[-1]["close_time"],
                    **metrics,
                }
            )
    return chunk_rows, underwater_rows


def split_chunks(rows: Sequence[Mapping[str, Any]], count: int) -> list[list[Mapping[str, Any]]]:
    if not rows:
        return [[] for _ in range(count)]
    size = math.ceil(len(rows) / count)
    chunks = [list(rows[index : index + size]) for index in range(0, len(rows), size)]
    while len(chunks) < count:
        chunks.append([])
    return chunks[:count]


def build_decision_payload(kpi_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]], curve_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    stress_1 = {
        str(row["attempt_name"]): row
        for row in cost_rows
        if float(row["extra_cost_per_round_trip_account_ccy"]) == 1.0
    }
    watchlist: list[str] = []
    fragile: list[str] = []
    for row in kpi_rows:
        attempt = str(row["attempt_name"])
        pf = to_float(row.get("profit_factor")) or 0.0
        net = to_float(row.get("net_profit")) or 0.0
        dd_pct = to_float(row.get("equity_dd_percent")) or 999.0
        survives_cost = bool(stress_1.get(attempt, {}).get("survives_pf_gt_1"))
        if net > 0 and pf > 1.2 and dd_pct <= 15 and survives_cost:
            watchlist.append(attempt)
        elif net <= 25 or pf <= 1.05 or not survives_cost:
            fragile.append(attempt)
    return {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "watchlist_not_selection": watchlist,
        "fragility_flags": fragile,
        "reason": (
            "run330F has complete raw-forward MT5 report and telemetry evidence, but it is still a research review. "
            "Curve pockets, cost fragility, and cp322A D/B source handoff remain unresolved."
        ),
        "next_action": NEXT_ACTION,
    }


def write_outputs(generated_at_utc: str) -> list[Path]:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    SELECTED_DIR.mkdir(parents=True, exist_ok=True)
    attempts = load_attempts()
    execution_result = read_json(RUN330E_DIR / "execution_result.json")
    bars = load_bars()
    trade_rows, long_short_rows, kpi_rows = build_trade_rows(attempts, execution_result, bars)
    regime_rows = build_regime_rows(trade_rows)
    db_rows = build_db_rows(attempts)
    lot_rows = build_lot_rows(kpi_rows)
    cost_rows = build_cost_rows(trade_rows)
    curve_rows, underwater_rows = build_curve_rows(trade_rows)
    decision_payload = build_decision_payload(kpi_rows, cost_rows, curve_rows)

    artifacts: list[Path] = []
    artifacts.append(
        write_csv(
            RUN_DIR / "forward_mt5_kpi_report.csv",
            [
                "attempt_name",
                "candidate_id",
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "session_days",
                "rows_evaluated",
                "signal_count",
                "order_attempt_count",
                "order_fill_count",
                "trade_count",
                "trades_per_day",
                "net_profit",
                "profit_factor",
                "expectancy",
                "recovery_factor",
                "equity_dd_amount",
                "equity_dd_percent",
                "long_trade_count",
                "short_trade_count",
                "long_win_rate_percent",
                "short_win_rate_percent",
                "recomputed_net_profit",
                "recomputed_profit_factor",
                "recomputed_max_drawdown",
                "net_recompute_delta",
                "max_underwater_trade_count",
                "max_underwater_start",
                "max_underwater_end",
                "claim_boundary",
            ],
            kpi_rows,
        )
    )
    artifacts.append(write_csv(RUN_DIR / "trade_level_records.csv", list(trade_rows[0].keys()) if trade_rows else [], trade_rows))
    artifacts.append(write_csv(RUN_DIR / "long_short_attribution_report.csv", ["attempt_name", "artifact_slug", "direction", "trade_count", "net_profit", "gross_profit", "gross_loss", "profit_factor", "expectancy", "win_rate", "max_drawdown"], long_short_rows))
    artifacts.append(write_csv(RUN_DIR / "regime_attribution_report.csv", ["attempt_name", "artifact_slug", "axis", "bucket", "trade_count", "net_profit", "gross_profit", "gross_loss", "profit_factor", "expectancy", "win_rate", "max_drawdown"], regime_rows))
    artifacts.append(write_csv(RUN_DIR / "session_hour_month_volatility_adx_vix_usd_rate_slices.csv", ["attempt_name", "artifact_slug", "axis", "bucket", "trade_count", "net_profit", "gross_profit", "gross_loss", "profit_factor", "expectancy", "win_rate", "max_drawdown"], regime_rows))
    artifacts.append(write_csv(RUN_DIR / "db_attribution_report.csv", ["attempt_name", "artifact_slug", "candidate_id", "db_source", "status", "reason", "effect"], db_rows))
    artifacts.append(write_csv(RUN_DIR / "lot_normalized_report.csv", ["attempt_name", "artifact_slug", "fixed_lot", "net_profit_at_fixed_lot", "equity_dd_amount_at_fixed_lot", "net_profit_per_1lot_linear", "equity_dd_amount_per_1lot_linear", "expectancy_per_1lot_linear", "normalization_boundary"], lot_rows))
    artifacts.append(write_csv(RUN_DIR / "cost_stress_report.csv", ["attempt_name", "artifact_slug", "extra_cost_per_round_trip_account_ccy", "net_profit_after_cost", "profit_factor_after_cost", "expectancy_after_cost", "max_drawdown_after_cost", "survives_pf_gt_1", "stress_boundary"], cost_rows))
    artifacts.append(write_csv(RUN_DIR / "curve_pocket_report.csv", ["attempt_name", "artifact_slug", "chunk_type", "chunk_id", "start_time", "end_time", "trade_count", "net_profit", "gross_profit", "gross_loss", "profit_factor", "expectancy", "win_rate", "max_drawdown"], curve_rows))
    artifacts.append(write_csv(RUN_DIR / "underwater_stretch_report.csv", ["attempt_name", "artifact_slug", "total_trade_count", "max_underwater_trade_count", "max_underwater_start", "max_underwater_end", "max_drawdown"], underwater_rows))
    artifacts.append(write_json(RUN_DIR / "final_forward_decision.json", decision_payload))
    artifacts.append(write_json(RUN_DIR / "performance_attribution_receipt.json", {"status": "completed", "kpi_report": rel(artifacts[0]), "regime_report": rel(artifacts[3]), "cost_stress_report": rel(artifacts[7]), "curve_pocket_report": rel(artifacts[8]), "claim_boundary": CLAIM_BOUNDARY}))
    artifacts.append(write_csv(RUN_DIR / "result_judgment.csv", ["run_id", "status", "judgment", "decision", "forward_passed", "forward_failed", "goal_achieve", "next_action", "claim_boundary"], [{**decision_payload, "run_id": RUN_ID, "claim_boundary": CLAIM_BOUNDARY}]))
    artifacts.append(write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate_name", "status", "evidence_path", "effect"], gate_rows()))
    artifacts.append(write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage_payload(generated_at_utc, artifacts)))
    artifacts.append(write_json(RUN_DIR / "run_manifest.json", {"stage_id": STAGE_ID, "run_id": RUN_ID, "run_number": RUN_NUMBER, "parent_run_id": PARENT_RUN_ID, "generated_at_utc": generated_at_utc, **decision_payload, "claim_boundary": CLAIM_BOUNDARY}))

    artifacts.extend(write_reports(kpi_rows, decision_payload))
    artifacts.append(update_selection_status(decision_payload))
    artifacts.extend(update_current_truth(decision_payload))
    update_registers(generated_at_utc, decision_payload, artifacts)
    return artifacts


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_name": "runtime_parity(런타임 동등성)",
            "status": "completed_with_research_boundary",
            "evidence_path": rel(RUN330E_DIR / "runtime_parity_receipt.json"),
            "effect": "run330E의 MT5 report/telemetry(보고서/실행 기록)를 분석 입력으로 쓰되 runtime authority(런타임 권위)는 주장하지 않는다.",
        },
        {
            "gate_name": "backtest_forensics(백테스트 포렌식)",
            "status": "usable_with_boundary",
            "evidence_path": rel(RUN330E_DIR / "backtest_forensics_receipt.json"),
            "effect": "Strategy Tester(전략 테스터) 출력의 경로와 거래 근거를 연결하되 profit(수익)만으로 선택하지 않는다.",
        },
        {
            "gate_name": "data_integrity(데이터 무결성)",
            "status": "passed_with_forward_scope",
            "evidence_path": rel(RAW_FORWARD_BARS),
            "effect": "2026-04-14 이후 raw-forward(원본 전진) M5 bars(5분봉)와 runtime telemetry(런타임 실행 기록)를 같은 시간축으로 읽는다.",
        },
        {
            "gate_name": "performance_attribution(성과 귀속)",
            "status": "completed",
            "evidence_path": rel(RUN_DIR / "performance_attribution_receipt.json"),
            "effect": "MT5 KPI(핵심 성과 지표)를 방향, 국면, 비용, 곡선 포켓으로 분해한다.",
        },
        {
            "gate_name": "result_judgment(결과 판정)",
            "status": "passed_no_goal_achieve",
            "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
            "effect": "Forward Passed(전진 통과), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
        {
            "gate_name": "artifact_lineage(산출물 계보)",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "artifact_lineage_receipt.json"),
            "effect": "run330E MT5 보고서와 run330F 분석 산출물을 연결한다.",
        },
    ]


def lineage_payload(generated_at_utc: str, artifacts: Sequence[Path]) -> dict[str, Any]:
    inputs = [
        RUN330E_DIR / "execution_result.json",
        RUN330E_DIR / "mt5_runtime_probe_summary.csv",
        RUN330E_DIR / "mt5" / "reports",
        RUN330E_DIR / "runtime_telemetry",
        RAW_FORWARD_BARS,
    ]
    all_paths = list(dict.fromkeys([*artifacts, Path(__file__)]))
    return {
        "generated_at_utc": generated_at_utc,
        "source_inputs": [rel(path) for path in inputs],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in all_paths if path.exists()],
        "artifact_hashes": {rel(path): sha256_file(path) for path in all_paths if path.exists() and path.is_file()},
        "lineage_judgment": "connected_with_raw_forward_review_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_reports(kpi_rows: Sequence[Mapping[str, Any]], decision_payload: Mapping[str, Any]) -> list[Path]:
    sorted_rows = sorted(kpi_rows, key=lambda row: float(row.get("net_profit") or 0.0), reverse=True)
    table = "\n".join(
        [
            "| attempt(시도) | net(순손익) | PF(수익 팩터) | trades/day(일 거래) | DD%(드로다운 퍼센트) | recovery(회복 계수) |",
            "|---|---:|---:|---:|---:|---:|",
            *[
                f"| {row['artifact_slug']} | {row['net_profit']} | {row['profit_factor']} | {row['trades_per_day']} | {row['equity_dd_percent']} | {row['recovery_factor']} |"
                for row in sorted_rows
            ],
        ]
    )
    watchlist = ", ".join(str(item) for item in decision_payload["watchlist_not_selection"]) or "none"
    fragile = ", ".join(str(item) for item in decision_payload["fragility_flags"]) or "none"
    report = write_md(
        REVIEWS_DIR / "run330F_raw_forward_mt5_kpi_regime_cost_curve_review.md",
        f"""
# run330F Raw Forward MT5 KPI Regime Cost Curve Review(330F 원본 전진 MT5 핵심 지표/국면/비용/곡선 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{decision_payload['status']}`
- judgment(판정): `{decision_payload['judgment']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## MT5 KPI(핵심 성과 지표)

{table}

## Read(판독)

- watchlist_not_selection(선택 아닌 관찰 목록): `{watchlist}`
- fragility_flags(취약성 표시): `{fragile}`
- D/B attribution(D/B 귀속): `out_of_scope_by_claim`
- effect(효과): raw-forward MT5 evidence(원본 전진 MT5 근거)는 생겼지만 cost fragility(비용 취약성), curve pocket(곡선 포켓), D/B source handoff(D/B 원천 인계)가 남아 Forward Passed(전진 통과)를 닫지 않는다.

## Next(다음)

`{NEXT_ACTION}`
""",
    )
    decision_doc = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage330F Raw Forward MT5 Review Decision(330F 원본 전진 MT5 검토 결정)

- decision(결정): `{decision_payload['decision']}`
- status(상태): `{decision_payload['status']}`
- judgment(판정): `{decision_payload['judgment']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): 일부 후보가 양수라도 overfit pressure(과적합 압력), cost fragility(비용 취약성), curve pocket(곡선 포켓) 검토가 남아 research handoff(연구 인계)로만 남긴다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    return [report, decision_doc]


def update_selection_status(decision_payload: Mapping[str, Any]) -> Path:
    watchlist = ", ".join(str(item) for item in decision_payload["watchlist_not_selection"]) or "none"
    fragile = ", ".join(str(item) for item in decision_payload["fragility_flags"]) or "none"
    return write_md(
        SELECTED_DIR / "selection_status.md",
        f"""
# Stage330 Selection Status(330단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_not_forward_authority`
- research_onnx_status(연구 온엑스 상태): `raw_forward_mt5_kpi_regime_cost_curve_review_completed_no_selection`
- latest_runtime_probe(최신 런타임 탐침): `{PARENT_RUN_ID}`
- latest_forward_review(최신 전진 검토): `{RUN_ID}`
- watchlist_not_selection(선택 아닌 관찰 목록): `{watchlist}`
- fragility_flags(취약성 표시): `{fragile}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): MT5 KPI(핵심 성과 지표)를 확인했지만 후보 선택이나 운영 주장은 아직 없다.
""",
    )


def update_current_truth(decision_payload: Mapping[str, Any]) -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage330(330단계) run330F(330F 실행) raw-forward MT5 review(원본 전진 MT5 검토)를 `{decision_payload['status']}`로 닫았다. "
        "Effect(효과): KPI(핵심 성과 지표), regime(국면), cost stress(비용 압박), curve pocket(곡선 포켓)을 기록했지만 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 없다.\n"
    )
    if "Stage330(330단계) run330F(330F 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)
    updated.append(WORKSPACE_STATE)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v6`",
        "- current_run(": f"- current_run(현재 실행): `{RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- selected_research_baseline(": "- selected_research_baseline(선택 연구 기준선): `none`",
        "- target_surface(": "- target_surface(목표 표면): `raw_forward_mt5_kpi_regime_cost_curve_review`",
        "- status(": f"- status(상태): `{decision_payload['status']}`",
        "- decision(": f"- decision(판정): `{decision_payload['judgment']}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement_line in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement_line)
    lines = current_text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("- run330E_summary("):
            lines[index] = (
                "- run330E_summary(330E 요약): raw-forward MT5 runtime probe(원본 전진 MT5 런타임 탐침)를 "
                "`completed_raw_forward_mt5_runtime_probe_no_forward_decision`로 다시 닫았다. Effect(효과): portable MT5(포터블 메타트레이더5)로 6/6 report/telemetry(보고서/실행 기록)를 확보했지만 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 없다."
            )
            break
    current_text = "\n".join(lines) + "\n"
    summary = (
        f"- run330F_summary(330F 요약): raw-forward MT5 KPI/regime/cost/curve review(원본 전진 MT5 핵심 지표/국면/비용/곡선 검토)를 `{decision_payload['status']}`로 닫았다. "
        "Effect(효과): watchlist(관찰 목록)는 만들었지만 selected candidate(선택 후보), Forward Passed(전진 통과), Goal Achieve(목표 달성)는 없다."
    )
    if "run330F_summary(330F 요약)" not in current_text:
        current_text = current_text.replace(f"- decision(판정): `{decision_payload['judgment']}`\n", f"- decision(판정): `{decision_payload['judgment']}`\n{summary}\n", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)
    updated.append(CURRENT_STATE)

    append_if_missing(
        CHANGELOG,
        "Stage330F Raw Forward MT5 KPI Regime Cost Curve Review",
        f"""
## 2026-05-26 - Stage330F Raw Forward MT5 KPI Regime Cost Curve Review(330F 원본 전진 MT5 핵심 지표/국면/비용/곡선 검토)

- run330F(330F 실행): run330E(330E 실행)의 MT5 report/telemetry(보고서/실행 기록)를 KPI(핵심 성과 지표), regime(국면), cost stress(비용 압박), curve pocket(곡선 포켓)으로 분해했다.
- status(상태): `{decision_payload['status']}`
- judgment(판정): `{decision_payload['judgment']}`
- effect(효과): watchlist(관찰 목록)는 만들었지만 선택 후보, Forward Passed(전진 통과), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    updated.append(CHANGELOG)
    return updated


def update_registers(generated_at_utc: str, decision_payload: Mapping[str, Any], artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run330F_raw_forward_mt5_kpi_regime_cost_curve_review.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "performance_attribution",
                "status": decision_payload["status"],
                "judgment": decision_payload["judgment"],
                "path": rel(report_path),
                "notes": "raw_forward_mt5_kpi_regime_cost_curve_review;no_selection;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__raw_forward_mt5_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "raw_forward_mt5_review",
                "tier_scope": "raw_forward_runtime_probe",
                "kpi_scope": "kpi_regime_cost_curve",
                "scoreboard_lane": "performance_attribution",
                "status": decision_payload["status"],
                "judgment": decision_payload["judgment"],
                "path": rel(report_path),
                "primary_kpi": "forward_mt5_kpi_report",
                "guardrail_kpi": "cost_stress;curve_pocket;db_attribution_out_of_scope",
                "external_verification_status": "uses_completed_run330E_mt5_reports_and_runtime_telemetry",
                "notes": f"decision={decision_payload['decision']};next_action={NEXT_ACTION}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__raw_forward_mt5_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "raw_forward_mt5_review(원본 전진 MT5 검토)",
                "tier_scope": "raw_forward_runtime_probe(원본 전진 런타임 탐침)",
                "scoreboard": "kpi_regime_cost_curve(KPI/국면/비용/곡선)",
                "status": decision_payload["status"],
                "judgment": decision_payload["judgment"],
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": decision_payload["decision"],
            }
        ],
    )
    artifact_rows = []
    for artifact_path in artifacts:
        if artifact_path.exists() and artifact_path.is_file():
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(artifact_path)}",
                    "artifact_type": "stage330F_raw_forward_review_artifact",
                    "path": rel(artifact_path),
                    "sha256": sha256_file(artifact_path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "raw-forward MT5 KPI/regime/cost/curve review artifact; no operating claim.",
                }
            )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage330F raw-forward MT5 KPI/regime/cost/curve review.")
    return parser.parse_args()


def main() -> None:
    _ = parse_args()
    generated_at_utc = utc_now()
    artifacts = write_outputs(generated_at_utc)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "artifact_count": len(artifacts),
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
