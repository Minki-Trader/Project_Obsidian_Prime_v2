from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import median
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AE"
RUN_ID = "run337AE_completed_day_forward_attribution_cost_stress_v1"
PARENT_RUN_ID = "run337AD_completed_day_forward_slice_or_next_day_rollover_confirm_v1"
NEXT_RUN_ID = "run337AF_failure_memory_and_no_overfit_rebuild_queue_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AE_completed_day_forward_attribution_cost_stress_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS = "completed_stage337AE_completed_day_attribution_cost_stress_fragile_no_forward_decision"
JUDGMENT = "completed_day_slice_runtime_parity_holds_but_cost_buffer_recovery_and_curve_pockets_are_fragile"
DECISION = "stage337AE_open_run337AF_failure_memory_and_no_overfit_rebuild_queue_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337AD_DIR = STAGE_DIR / "02_runs" / "run337AD"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AE_completed_day_forward_attribution_cost_stress.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AE_completed_day_forward_attribution_cost_stress.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SOURCE_EXECUTION = RUN337AD_DIR / "execution_result.json"
SOURCE_RUNTIME_SUMMARY = RUN337AD_DIR / "runtime_summary.csv"
SOURCE_KPI_SUMMARY = RUN337AD_DIR / "completed_day_forward_kpi_summary.csv"
SOURCE_GAP = RUN337AD_DIR / "tester_feature_last_gap_completed_day_slice.csv"
SOURCE_PARITY = RUN337AD_DIR / "timestamp_aligned_proxy_mt5_difference.csv"
SOURCE_USABILITY = RUN337AD_DIR / "proxy_usability_judgment.csv"
SOURCE_RUN_MANIFEST = RUN337AD_DIR / "run_manifest.json"

TRADE_RECORDS = RUN_DIR / "trade_records.csv"
PARSER_CHECKS = RUN_DIR / "report_parser_checks.csv"
PARSER_ERRORS = RUN_DIR / "report_parser_errors.csv"
SIGNAL_ATTRIBUTION = RUN_DIR / "signal_attribution_report.csv"
REGIME_ATTRIBUTION = RUN_DIR / "regime_attribution_report.csv"
DB_ATTRIBUTION = RUN_DIR / "db_attribution_report.csv"
LOT_NORMALIZED = RUN_DIR / "lot_normalized_report.csv"
COST_STRESS = RUN_DIR / "cost_stress_report.csv"
CURVE_POCKET = RUN_DIR / "curve_pocket_report.csv"
ECONOMIC_REGIME_AUDIT = RUN_DIR / "economic_regime_source_audit.csv"
FINAL_DECISION = RUN_DIR / "final_forward_decision_report.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
INPUT_IDENTITY = RUN_DIR / "input_identity.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"

COMPLETED_ATTEMPT = "u42_plain_rf_ad_completed_day_broker_slice"
FULL_CONTROL_ATTEMPT = "u42_plain_rf_ad_full_current_day_broker_control"
ATTEMPT_FEATURES = {
    COMPLETED_ATTEMPT: RUN337AD_DIR / "feature_matrices" / "u42_plain_ad_completed_day_broker_slice_features.csv",
    FULL_CONTROL_ATTEMPT: RUN337AD_DIR / "feature_matrices" / "u42_plain_ad_full_current_day_broker_control_features.csv",
}
ATTEMPT_TELEMETRY = {
    COMPLETED_ATTEMPT: RUN337AD_DIR / "runtime_telemetry" / "u42_plain_rf_ad_completed_day_broker_slice_telemetry.csv",
    FULL_CONTROL_ATTEMPT: RUN337AD_DIR / "runtime_telemetry" / "u42_plain_rf_ad_full_current_day_broker_control_telemetry.csv",
}

DEPOSIT = 500.0
STRESS_POINTS = (0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0)
ROLLING_WINDOWS = (20, 50)


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return str(value)


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(normalized)
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if bom else "utf-8"), bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt", ".yaml"} else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(normalized)
    return path


def profit_factor(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> float | None:
    gross_profit = sum(number(row.get(key)) for row in rows if number(row.get(key)) > 0.0)
    gross_loss = -sum(number(row.get(key)) for row in rows if number(row.get(key)) < 0.0)
    if gross_loss == 0.0:
        return math.inf if gross_profit > 0.0 else None
    return gross_profit / gross_loss


def max_closed_drawdown(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> tuple[float, int, float, str, str]:
    balance = DEPOSIT
    peak = DEPOSIT
    max_dd = 0.0
    longest_underwater = 0
    current_underwater = 0
    underwater_count = 0
    dd_start = ""
    dd_end = ""
    current_peak_time = ""
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        balance += number(row.get(key))
        close_time = str(row.get("close_time", ""))
        if balance >= peak:
            peak = balance
            current_underwater = 0
            current_peak_time = close_time
        else:
            current_underwater += 1
            underwater_count += 1
            longest_underwater = max(longest_underwater, current_underwater)
        drawdown = peak - balance
        if drawdown > max_dd:
            max_dd = drawdown
            dd_start = current_peak_time
            dd_end = close_time
    share = underwater_count / len(rows) if rows else 0.0
    return max_dd, longest_underwater, share, dd_start, dd_end


def metrics(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> dict[str, Any]:
    count = len(rows)
    net = sum(number(row.get(key)) for row in rows)
    gross_profit = sum(number(row.get(key)) for row in rows if number(row.get(key)) > 0.0)
    gross_loss = sum(number(row.get(key)) for row in rows if number(row.get(key)) < 0.0)
    wins = sum(1 for row in rows if number(row.get(key)) > 0.0)
    losses = sum(1 for row in rows if number(row.get(key)) < 0.0)
    dd, underwater, underwater_share, dd_start, dd_end = max_closed_drawdown(rows, key)
    return {
        "trade_count": count,
        "net_profit": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor(rows, key),
        "expectancy": net / count if count else None,
        "win_count": wins,
        "loss_count": losses,
        "win_rate": wins / count if count else None,
        "average_win": gross_profit / wins if wins else None,
        "average_loss": gross_loss / losses if losses else None,
        "max_closed_drawdown": dd,
        "recovery_factor": net / dd if dd else None,
        "longest_underwater_trades": underwater,
        "underwater_trade_share": underwater_share,
        "drawdown_start": dd_start,
        "drawdown_end": dd_end,
    }


def grouped(rows: Iterable[Mapping[str, Any]], keys: Sequence[str]) -> dict[tuple[Any, ...], list[Mapping[str, Any]]]:
    output: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        output[tuple(row.get(key, "") for key in keys)].append(row)
    return output


def session_bucket(ts: pd.Timestamp) -> str:
    hour = int(ts.hour)
    if 0 <= hour <= 6:
        return "session_00_06_utc"
    if 7 <= hour <= 12:
        return "session_07_12_utc"
    if 13 <= hour <= 20:
        return "session_13_20_utc"
    return "session_21_23_utc"


def chronological_segment(index: int, total: int) -> str:
    if total <= 0:
        return "none"
    third = (total + 2) // 3
    if index < third:
        return "chron_early"
    if index < third * 2:
        return "chron_mid"
    return "chron_late"


def numeric_bucket(value: Any, label: str, cuts: Sequence[float]) -> str:
    parsed = number(value, math.nan)
    if not math.isfinite(parsed):
        return f"{label}_missing"
    low = -math.inf
    for cut in cuts:
        if parsed < cut:
            return f"{label}_{low:g}_to_{cut:g}"
        low = cut
    return f"{label}_{low:g}_plus"


def feature_frame(path: Path) -> pd.DataFrame:
    if not path_exists(path):
        return pd.DataFrame()
    frame = pd.read_csv(io_path(path))
    timestamp_column = next((col for col in ("timestamp_utc", "bar_time_server", "timestamp") if col in frame.columns), None)
    if timestamp_column is None:
        frame["feature_ts"] = pd.NaT
    else:
        values = frame[timestamp_column].astype(str)
        parsed = pd.to_datetime(values.str.replace(".", "-", regex=False), errors="coerce", utc=True)
        frame["feature_ts"] = parsed.dt.tz_convert(None)
    return frame.dropna(subset=["feature_ts"]).sort_values("feature_ts").reset_index(drop=True)


def feature_at(features: pd.DataFrame, ts: pd.Timestamp) -> Mapping[str, Any]:
    if features.empty:
        return {}
    key = pd.Timestamp(ts)
    if key.tzinfo is not None:
        key = key.tz_convert(None)
    index = features["feature_ts"].searchsorted(key, side="right") - 1
    if index < 0:
        return {}
    return features.iloc[int(index)].to_dict()


def source_execution_rows() -> list[Mapping[str, Any]]:
    data = read_json(SOURCE_EXECUTION)
    rows = [row for row in data.get("execution_results", []) if row.get("attempt_name") in ATTEMPT_FEATURES]
    rows.sort(key=lambda row: 0 if row.get("attempt_name") == COMPLETED_ATTEMPT else 1)
    return rows


def kpi_by_attempt() -> dict[str, Mapping[str, str]]:
    return {str(row.get("attempt_name", "")): row for row in read_csv(SOURCE_KPI_SUMMARY)}


def report_path(record: Mapping[str, Any]) -> Path:
    report = record.get("strategy_tester_report", {})
    html = report.get("html_report", {}) if isinstance(report, Mapping) else {}
    return Path(str(html.get("path") or ""))


def point_value_estimate(rows: Sequence[Mapping[str, Any]]) -> float:
    values: list[float] = []
    for row in rows:
        volume = number(row.get("volume"))
        delta = abs(number(row.get("close_price")) - number(row.get("open_price")))
        gross = abs(number(row.get("gross_profit")))
        if volume > 0.0 and delta > 0.0 and gross > 0.0:
            values.append(gross / (delta * volume))
    return median(values) if values else 1.0


def slice_type(attempt_name: str) -> str:
    if attempt_name == COMPLETED_ATTEMPT:
        return "completed_day_broker_slice"
    if attempt_name == FULL_CONTROL_ATTEMPT:
        return "full_current_day_control_observed_until_tester_cutoff"
    return "unknown"


def forward_usability(attempt_name: str) -> str:
    if attempt_name == COMPLETED_ATTEMPT:
        return "usable_for_completed_day_runtime_attribution_not_forward_pass_fail"
    if attempt_name == FULL_CONTROL_ATTEMPT:
        return "not_usable_as_full_current_day_forward_decision"
    return "unknown"


def build_trade_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    feature_cache: dict[str, pd.DataFrame] = {}
    rows: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for exec_row in source_execution_rows():
        attempt_name = str(exec_row.get("attempt_name", ""))
        path = report_path(exec_row)
        try:
            parsed = parse_mt5_trade_report(path)
            trades = pair_deals_into_trades(parsed["deals"])
        except Exception as exc:  # persisted as evidence.
            errors.append({"attempt_name": attempt_name, "report_path": rel(path), "error": str(exc), "claim_boundary": CLAIM_BOUNDARY})
            continue
        metrics_payload = exec_row.get("strategy_tester_report", {}).get("metrics", {})
        expected_count = int(number(metrics_payload.get("trade_count")))
        checks.append(
            {
                "attempt_name": attempt_name,
                "slice_type": slice_type(attempt_name),
                "report_path": rel(path),
                "expected_trade_count": expected_count,
                "parsed_trade_count": len(trades),
                "trade_count_delta": len(trades) - expected_count,
                "parser_status": "matched" if len(trades) == expected_count else "count_mismatch",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        feature_path = ATTEMPT_FEATURES.get(attempt_name, Path(""))
        feature_key = feature_path.as_posix()
        if feature_key not in feature_cache:
            feature_cache[feature_key] = feature_frame(feature_path)
        features = feature_cache[feature_key]
        ordered = sorted(trades, key=lambda trade: trade.close_time)
        point_value = point_value_estimate(
            [
                {
                    "volume": trade.volume,
                    "open_price": trade.open_price,
                    "close_price": trade.close_price,
                    "gross_profit": trade.gross_profit,
                }
                for trade in ordered
            ]
        )
        for index, trade in enumerate(ordered):
            open_time = pd.Timestamp(trade.open_time)
            close_time = pd.Timestamp(trade.close_time)
            feat = feature_at(features, open_time)
            row = {
                "run_id": RUN_ID,
                "source_run_id": PARENT_RUN_ID,
                "attempt_name": attempt_name,
                "slice_type": slice_type(attempt_name),
                "forward_usability": forward_usability(attempt_name),
                "artifact_slug": exec_row.get("artifact_slug", ""),
                "feature_set_id": exec_row.get("feature_set_id", ""),
                "model_id": exec_row.get("model_id", ""),
                "tier": exec_row.get("tier", ""),
                "split": exec_row.get("split", ""),
                "db_source_status": "not_available_in_run337AD_u42_artifacts",
                "db_source": "not_available",
                "decision_surface_mapping": "technical42_long_short_surface_only_no_D_B_source_columns",
                "trade_index": trade.index,
                "direction": trade.direction,
                "open_time": open_time.strftime("%Y-%m-%d %H:%M:%S"),
                "close_time": close_time.strftime("%Y-%m-%d %H:%M:%S"),
                "holding_minutes": (close_time - open_time).total_seconds() / 60.0,
                "holding_bars_m5": (close_time - open_time).total_seconds() / 300.0,
                "month": close_time.strftime("%Y-%m"),
                "weekday": close_time.strftime("%A"),
                "open_hour_utc": open_time.strftime("%H"),
                "close_hour_utc": close_time.strftime("%H"),
                "session_utc": session_bucket(open_time),
                "chron_segment": chronological_segment(index, len(ordered)),
                "volume": trade.volume,
                "open_price": trade.open_price,
                "close_price": trade.close_price,
                "gross_profit": trade.gross_profit,
                "net_profit": trade.net_profit,
                "swap": trade.swap,
                "commission": trade.commission,
                "lot_normalized_net_per_1lot": trade.net_profit / trade.volume if trade.volume else None,
                "point_value_per_lot_estimate": point_value,
                "feature_timestamp": pd.Timestamp(feat.get("feature_ts")).strftime("%Y-%m-%d %H:%M:%S") if feat else "",
                "atr_14": feat.get("atr_14", ""),
                "atr_50": feat.get("atr_50", ""),
                "atr_14_over_atr_50": feat.get("atr_14_over_atr_50", ""),
                "historical_vol_20": feat.get("historical_vol_20", ""),
                "historical_vol_5_over_20": feat.get("historical_vol_5_over_20", ""),
                "adx_14": feat.get("adx_14", ""),
                "di_spread_14": feat.get("di_spread_14", ""),
                "rsi_14": feat.get("rsi_14", ""),
                "minutes_from_cash_open": feat.get("minutes_from_cash_open", ""),
                "is_us_cash_open": feat.get("is_us_cash_open", ""),
                "vix_zscore_20": feat.get("vix_zscore_20", ""),
                "us10yr_zscore_20": feat.get("us10yr_zscore_20", ""),
                "usdx_zscore_20": feat.get("usdx_zscore_20", ""),
                "vol_regime": numeric_bucket(feat.get("historical_vol_20"), "vol", (0.08, 0.14, 0.22)),
                "atr_ratio_regime": numeric_bucket(feat.get("atr_14_over_atr_50"), "atr_ratio", (0.8, 1.0, 1.2)),
                "adx_regime": numeric_bucket(feat.get("adx_14"), "adx", (20.0, 25.0, 40.0)),
                "di_regime": numeric_bucket(feat.get("di_spread_14"), "di_spread", (-20.0, 0.0, 20.0)),
                "vix_regime": numeric_bucket(feat.get("vix_zscore_20"), "vix_z", (-1.0, 0.0, 1.0)),
                "rate_regime": numeric_bucket(feat.get("us10yr_zscore_20"), "us10yr_z", (-1.0, 0.0, 1.0)),
                "usd_regime": numeric_bucket(feat.get("usdx_zscore_20"), "usdx_z", (-1.0, 0.0, 1.0)),
                "source_report_path": rel(path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            rows.append(row)
    return rows, checks, errors


def parse_runtime_ts(value: Any) -> pd.Timestamp | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return pd.Timestamp(datetime.strptime(text, "%Y.%m.%d %H:%M:%S"))
    except ValueError:
        parsed = pd.to_datetime(text, errors="coerce")
        return None if pd.isna(parsed) else pd.Timestamp(parsed)


def build_signal_rows() -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for attempt_name, telemetry_path in ATTEMPT_TELEMETRY.items():
        cycles = [row for row in read_csv(telemetry_path) if row.get("record_type") == "cycle"]
        enriched: list[dict[str, Any]] = []
        total = len(cycles)
        for index, row in enumerate(cycles):
            ts = parse_runtime_ts(row.get("bar_time"))
            item = dict(row)
            item["attempt_name"] = attempt_name
            item["slice_type"] = slice_type(attempt_name)
            item["decision"] = row.get("decision", "")
            item["exec_action"] = row.get("exec_action", "")
            item["order_filled_bool"] = str(row.get("order_filled", "")).lower() == "true"
            item["month"] = ts.strftime("%Y-%m") if ts is not None else ""
            item["weekday"] = ts.strftime("%A") if ts is not None else ""
            item["hour_utc"] = ts.strftime("%H") if ts is not None else ""
            item["session_utc"] = session_bucket(ts) if ts is not None else "session_missing"
            item["chron_segment"] = chronological_segment(index, total)
            enriched.append(item)
        axes = ("decision", "exec_action", "month", "weekday", "hour_utc", "session_utc", "chron_segment")
        for axis in axes:
            for key, rows in grouped(enriched, (axis,)).items():
                bucket = key[0]
                long_count = sum(1 for row in rows if row.get("decision") == "long")
                short_count = sum(1 for row in rows if row.get("decision") == "short")
                flat_count = sum(1 for row in rows if row.get("decision") == "flat")
                fills = sum(1 for row in rows if row.get("order_filled_bool"))
                output.append(
                    {
                        "attempt_name": attempt_name,
                        "slice_type": slice_type(attempt_name),
                        "axis": axis,
                        "bucket": bucket,
                        "cycle_count": len(rows),
                        "long_signal_count": long_count,
                        "short_signal_count": short_count,
                        "flat_signal_count": flat_count,
                        "order_fill_count": fills,
                        "long_signal_share": long_count / len(rows) if rows else None,
                        "short_signal_share": short_count / len(rows) if rows else None,
                        "flat_signal_share": flat_count / len(rows) if rows else None,
                        "fill_per_cycle": fills / len(rows) if rows else None,
                        "signal_read": signal_read(long_count, short_count, flat_count, fills, len(rows)),
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return output


def signal_read(long_count: int, short_count: int, flat_count: int, fills: int, total: int) -> str:
    if total <= 0:
        return "missing_signal_rows"
    if long_count > short_count * 10 and short_count < max(20, long_count * 0.1):
        return "long_heavy_signal_mix"
    if fills == 0 and (long_count or short_count):
        return "signal_without_fill"
    if flat_count / total > 0.8:
        return "mostly_flat"
    return "mixed_signal_distribution"


def slice_read(item: Mapping[str, Any]) -> str:
    trades = int(number(item.get("trade_count")))
    net = number(item.get("net_profit"))
    pf = number(item.get("profit_factor"), math.nan)
    dd = number(item.get("max_closed_drawdown"))
    recovery = number(item.get("recovery_factor"), math.nan)
    if trades < 3:
        return "too_thin_to_read"
    if net <= 0.0:
        return "negative_slice"
    if math.isfinite(pf) and pf < 1.1:
        return "pf_thin_slice"
    if math.isfinite(recovery) and recovery < 1.0:
        return "recovery_below_one_slice"
    if dd > abs(net) * 1.5 and dd > 20.0:
        return "drawdown_heavy_slice"
    return "constructive_slice"


def build_slice_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    axes = (
        "direction",
        "month",
        "weekday",
        "open_hour_utc",
        "close_hour_utc",
        "session_utc",
        "chron_segment",
        "vol_regime",
        "atr_ratio_regime",
        "adx_regime",
        "di_regime",
        "vix_regime",
        "rate_regime",
        "usd_regime",
        "is_us_cash_open",
    )
    rows: list[dict[str, Any]] = []
    for axis in axes:
        for key, items in grouped(trades, ("attempt_name", "slice_type", "feature_set_id", axis)).items():
            attempt, slice_name, feature_set, bucket = key
            item = metrics(items)
            rows.append(
                {
                    "attempt_name": attempt,
                    "slice_type": slice_name,
                    "feature_set_id": feature_set,
                    "axis": axis,
                    "bucket": bucket,
                    **item,
                    "slice_read": slice_read(item),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_db_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, items in grouped(trades, ("attempt_name", "slice_type", "feature_set_id", "db_source_status", "db_source", "decision_surface_mapping")).items():
        attempt, slice_name, feature_set, status, source, mapping = key
        rows.append(
            {
                "attempt_name": attempt,
                "slice_type": slice_name,
                "feature_set_id": feature_set,
                "db_source_status": status,
                "db_source": source,
                "decision_surface_mapping": mapping,
                **metrics(items),
                "interpretation": "D/B source columns are not present in run337AD u42 artifacts; only long/short direction attribution is supported.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for key, items in grouped(trades, ("attempt_name", "slice_type", "feature_set_id", "direction")).items():
        attempt, slice_name, feature_set, direction = key
        rows.append(
            {
                "attempt_name": attempt,
                "slice_type": slice_name,
                "feature_set_id": feature_set,
                "db_source_status": "direction_proxy_only",
                "db_source": f"direction_{direction}",
                "decision_surface_mapping": "long_short_attribution_not_D_B_source",
                **metrics(items),
                "interpretation": "Direction attribution exists, but it must not be read as D source or B source attribution.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_lot_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, items in grouped(trades, ("attempt_name", "slice_type", "feature_set_id")).items():
        attempt, slice_name, feature_set = key
        item = metrics(items)
        total_lots = sum(number(row.get("volume")) for row in items)
        lots = [number(row.get("volume")) for row in items if number(row.get("volume")) > 0.0]
        rows.append(
            {
                "attempt_name": attempt,
                "slice_type": slice_name,
                "feature_set_id": feature_set,
                **item,
                "total_lots": total_lots,
                "fixed_lot_observed": median(lots) if lots else None,
                "net_per_1lot": item["net_profit"] / total_lots if total_lots else None,
                "net_per_0_1lot_trade": item["net_profit"] / len(items) if items else None,
                "lot_policy_read": "fixed_0_1_lot_observed_no_lot_optimization",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def stress_read(item: Mapping[str, Any]) -> str:
    net = number(item.get("net_profit"))
    pf = number(item.get("profit_factor"), math.nan)
    if net <= 0.0:
        return "cost_breaks_net"
    if not math.isfinite(pf) or pf < 1.0:
        return "cost_breaks_pf"
    if pf < 1.1:
        return "cost_leaves_pf_below_1_1"
    if pf < 1.2:
        return "cost_thin_pf_1_1_to_1_2"
    return "cost_survives_this_scenario"


def build_cost_stress_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, items in grouped(trades, ("attempt_name", "slice_type", "feature_set_id")).items():
        attempt, slice_name, feature_set = key
        point_value = point_value_estimate(items)
        base_metric = metrics(items)
        breakeven_points = base_metric["net_profit"] / (len(items) * median([number(row.get("volume")) for row in items]) * point_value) if items else None
        for stress in STRESS_POINTS:
            stressed: list[dict[str, Any]] = []
            for row in items:
                extra_cost = stress * number(row.get("volume")) * point_value
                copy = dict(row)
                copy["stressed_net_profit"] = number(row.get("net_profit")) - extra_cost
                stressed.append(copy)
            item = metrics(stressed, "stressed_net_profit")
            rows.append(
                {
                    "attempt_name": attempt,
                    "slice_type": slice_name,
                    "feature_set_id": feature_set,
                    "extra_round_trip_points": stress,
                    "point_value_per_1lot_estimate": point_value,
                    "breakeven_extra_round_trip_points_estimate": breakeven_points,
                    **item,
                    "stress_read": stress_read(item),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def rolling_pockets(items: Sequence[Mapping[str, Any]], window: int) -> dict[str, Any]:
    ordered = sorted(items, key=lambda row: str(row.get("close_time")))
    if len(ordered) < window:
        return {
            "window_trades": window,
            "pocket_status": "not_enough_trades",
            "pocket_net_profit": None,
            "pocket_start": "",
            "pocket_end": "",
        }
    best: dict[str, Any] = {"pocket_net_profit": math.inf}
    for start in range(0, len(ordered) - window + 1):
        chunk = ordered[start : start + window]
        net = sum(number(row.get("net_profit")) for row in chunk)
        if net < number(best.get("pocket_net_profit"), math.inf):
            best = {
                "window_trades": window,
                "pocket_status": "computed",
                "pocket_net_profit": net,
                "pocket_start": chunk[0].get("close_time", ""),
                "pocket_end": chunk[-1].get("close_time", ""),
            }
    return best


def build_curve_rows(trades: Sequence[Mapping[str, Any]], slice_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    cost_by_attempt = {(row.get("attempt_name"), number(row.get("extra_round_trip_points"))): row for row in cost_rows}
    report_kpis = kpi_by_attempt()
    for key, items in grouped(trades, ("attempt_name", "slice_type", "feature_set_id")).items():
        attempt, slice_name, feature_set = key
        item = metrics(items)
        report = report_kpis.get(str(attempt), {})
        relevant_slices = [row for row in slice_rows if row.get("attempt_name") == attempt]
        month_slices = [row for row in relevant_slices if row.get("axis") == "month" and int(number(row.get("trade_count"))) >= 3]
        chron_slices = [row for row in relevant_slices if row.get("axis") == "chron_segment"]
        worst = min(month_slices + chron_slices, key=lambda row: number(row.get("net_profit")), default={})
        negative_months = [row for row in month_slices if number(row.get("net_profit")) < 0.0]
        one_point = cost_by_attempt.get((attempt, 1.0), {})
        five_point = cost_by_attempt.get((attempt, 5.0), {})
        output.append(
            {
                "attempt_name": attempt,
                "slice_type": slice_name,
                "feature_set_id": feature_set,
                "pocket_type": "attempt_summary",
                **item,
                "mt5_report_net_profit": report.get("net_profit", ""),
                "mt5_report_profit_factor": report.get("profit_factor", ""),
                "mt5_report_trade_count": report.get("trade_count", ""),
                "mt5_report_max_drawdown_amount": report.get("max_drawdown_amount", ""),
                "mt5_report_recovery_factor": report.get("recovery_factor", ""),
                "mt5_report_expectancy": report.get("expectancy", ""),
                "positive_month_ratio": (len(month_slices) - len(negative_months)) / len(month_slices) if month_slices else None,
                "negative_month_count": len(negative_months),
                "worst_slice_axis": worst.get("axis", ""),
                "worst_slice_bucket": worst.get("bucket", ""),
                "worst_slice_net_profit": worst.get("net_profit", ""),
                "one_point_pf": one_point.get("profit_factor", ""),
                "five_point_net_profit": five_point.get("net_profit", ""),
                "curve_read": curve_read(item, report, worst, one_point, five_point, attempt),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for axis_name, rows_for_axis in (("worst_month", month_slices), ("worst_chron_segment", chron_slices)):
            pocket = min(rows_for_axis, key=lambda row: number(row.get("net_profit")), default={})
            if pocket:
                output.append(
                    {
                        "attempt_name": attempt,
                        "slice_type": slice_name,
                        "feature_set_id": feature_set,
                        "pocket_type": axis_name,
                        "axis": pocket.get("axis", ""),
                        "bucket": pocket.get("bucket", ""),
                        "trade_count": pocket.get("trade_count", ""),
                        "net_profit": pocket.get("net_profit", ""),
                        "profit_factor": pocket.get("profit_factor", ""),
                        "max_closed_drawdown": pocket.get("max_closed_drawdown", ""),
                        "recovery_factor": pocket.get("recovery_factor", ""),
                        "curve_read": pocket.get("slice_read", ""),
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
        for window in ROLLING_WINDOWS:
            pocket = rolling_pockets(items, window)
            output.append(
                {
                    "attempt_name": attempt,
                    "slice_type": slice_name,
                    "feature_set_id": feature_set,
                    "pocket_type": f"worst_rolling_{window}_trades",
                    "trade_count": window,
                    "net_profit": pocket.get("pocket_net_profit"),
                    "pocket_start": pocket.get("pocket_start", ""),
                    "pocket_end": pocket.get("pocket_end", ""),
                    "curve_read": "negative_rolling_pocket" if number(pocket.get("pocket_net_profit")) < 0.0 else pocket.get("pocket_status", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return output


def curve_read(item: Mapping[str, Any], report: Mapping[str, Any], worst: Mapping[str, Any], one_point: Mapping[str, Any], five_point: Mapping[str, Any], attempt: str) -> str:
    net = number(item.get("net_profit"))
    pf = number(item.get("profit_factor"), math.nan)
    report_recovery = number(report.get("recovery_factor"), math.nan)
    worst_net = number(worst.get("net_profit"))
    one_pf = number(one_point.get("profit_factor"), math.nan)
    five_net = number(five_point.get("net_profit"), math.nan)
    if attempt == FULL_CONTROL_ATTEMPT:
        return "boundary_control_not_full_current_day_forward"
    if net <= 0.0 or not math.isfinite(pf) or pf <= 1.0:
        return "negative_or_unprofitable_completed_day_slice"
    if math.isfinite(one_pf) and one_pf < 1.1:
        return "cost_fragile_completed_day_slice"
    if math.isfinite(five_net) and five_net <= 0.0:
        return "wide_cost_stress_breaks_net"
    if math.isfinite(report_recovery) and report_recovery < 1.0:
        return "recovery_below_one_completed_day_slice"
    if worst_net < 0.0:
        return "has_negative_curve_pocket"
    return "constructive_but_completed_day_only"


def build_economic_regime_audit(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    feature_columns = set()
    for path in ATTEMPT_FEATURES.values():
        if path_exists(path):
            frame = pd.read_csv(io_path(path), nrows=1)
            feature_columns.update(str(col) for col in frame.columns)
    rows = []
    for field, meaning in (
        ("vix_zscore_20", "VIX regime"),
        ("usdx_zscore_20", "USD regime"),
        ("us10yr_zscore_20", "rate regime"),
    ):
        rows.append(
            {
                "field": field,
                "meaning": meaning,
                "available_in_feature_matrix": field in feature_columns,
                "trade_rows_with_value": sum(1 for row in trades if str(row.get(field, "")).strip()),
                "audit_read": "missing_in_u42_no_external_feature_set" if field not in feature_columns else "available",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def gate_rows(
    trades: Sequence[Mapping[str, Any]],
    parser_checks: Sequence[Mapping[str, Any]],
    parser_errors: Sequence[Mapping[str, Any]],
    signal_rows: Sequence[Mapping[str, Any]],
    regime_rows: Sequence[Mapping[str, Any]],
    db_rows: Sequence[Mapping[str, Any]],
    lot_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    curve_rows: Sequence[Mapping[str, Any]],
    economic_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parser_ok = bool(parser_checks) and not parser_errors and all(row.get("parser_status") == "matched" for row in parser_checks)
    one_point_fragile = [
        row for row in cost_rows
        if number(row.get("extra_round_trip_points")) == 1.0 and row.get("stress_read") in {"cost_leaves_pf_below_1_1", "cost_breaks_pf", "cost_breaks_net"}
    ]
    return [
        {
            "gate_name": "frozen_candidate_identity",
            "status": "covered",
            "evidence_path": rel(INPUT_IDENTITY),
            "effect": "cp322A/u42 ONNX, feature order, threshold, risk and lot logic are read-only inputs; no retuning is performed.",
        },
        {
            "gate_name": "trade_report_parse",
            "status": "covered" if parser_ok else "covered_partial",
            "evidence_path": rel(PARSER_CHECKS),
            "effect": f"MT5 HTML reports were parsed into trade records; parser_errors={len(parser_errors)}.",
        },
        {
            "gate_name": "signal_attribution",
            "status": "covered" if signal_rows else "blocked",
            "evidence_path": rel(SIGNAL_ATTRIBUTION),
            "effect": "Runtime telemetry is decomposed by signal, execution action, hour, session and chronology.",
        },
        {
            "gate_name": "regime_attribution",
            "status": "covered" if regime_rows else "blocked",
            "evidence_path": rel(REGIME_ATTRIBUTION),
            "effect": "Trades are decomposed by direction, time, volatility, ADX, DI and cash-session slices.",
        },
        {
            "gate_name": "db_source_attribution_boundary",
            "status": "covered_boundary",
            "evidence_path": rel(DB_ATTRIBUTION),
            "effect": "D/B source attribution is marked unavailable in run337AD u42 artifacts, preventing a fake D/B read.",
        },
        {
            "gate_name": "lot_normalized_result",
            "status": "covered" if lot_rows else "blocked",
            "evidence_path": rel(LOT_NORMALIZED),
            "effect": "Fixed lot and per-lot result are reported without optimizing lot size.",
        },
        {
            "gate_name": "cost_stress",
            "status": "failed_for_robustness_review" if one_point_fragile else "covered",
            "evidence_path": rel(COST_STRESS),
            "effect": f"Spread/slippage stress is applied after the fact; one_point_fragile_rows={len(one_point_fragile)}.",
        },
        {
            "gate_name": "curve_pocket",
            "status": "covered" if curve_rows else "blocked",
            "evidence_path": rel(CURVE_POCKET),
            "effect": "Worst month, chronology and rolling trade pockets are recorded.",
        },
        {
            "gate_name": "economic_regime_availability",
            "status": "covered_boundary",
            "evidence_path": rel(ECONOMIC_REGIME_AUDIT),
            "effect": f"External VIX/USD/rate fields available={sum(1 for row in economic_rows if row.get('available_in_feature_matrix'))}/{len(economic_rows)}.",
        },
        {
            "gate_name": "no_forward_pass_fail_or_goal_claim",
            "status": "covered",
            "evidence_path": rel(FINAL_DECISION),
            "effect": "Forward Passed, Forward Failed, runtime authority and Goal Achieve are not claimed.",
        },
    ]


def build_final_decision(curve_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]], db_rows: Sequence[Mapping[str, Any]], economic_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed_curve = next((row for row in curve_rows if row.get("attempt_name") == COMPLETED_ATTEMPT and row.get("pocket_type") == "attempt_summary"), {})
    full_curve = next((row for row in curve_rows if row.get("attempt_name") == FULL_CONTROL_ATTEMPT and row.get("pocket_type") == "attempt_summary"), {})
    completed_one = next((row for row in cost_rows if row.get("attempt_name") == COMPLETED_ATTEMPT and number(row.get("extra_round_trip_points")) == 1.0), {})
    completed_five = next((row for row in cost_rows if row.get("attempt_name") == COMPLETED_ATTEMPT and number(row.get("extra_round_trip_points")) == 5.0), {})
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "completed_day_slice": completed_curve,
        "full_current_day_control": full_curve,
        "completed_day_one_point_stress": completed_one,
        "completed_day_five_point_stress": completed_five,
        "db_source_attribution": "not_available_in_run337AD_u42_artifacts",
        "economic_regime_boundary": economic_rows,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "forward_blocked": "full_current_day_control_gap_remains_latest_current_day_not_forward_decidable",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_text(final_decision: Mapping[str, Any], curve_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]], db_rows: Sequence[Mapping[str, Any]], economic_rows: Sequence[Mapping[str, Any]], parser_errors: Sequence[Mapping[str, Any]]) -> str:
    completed = final_decision.get("completed_day_slice", {})
    one_point = final_decision.get("completed_day_one_point_stress", {})
    five_point = final_decision.get("completed_day_five_point_stress", {})
    weak_pockets = [
        row for row in curve_rows
        if row.get("attempt_name") == COMPLETED_ATTEMPT and row.get("pocket_type") != "attempt_summary" and number(row.get("net_profit")) < 0.0
    ]
    weak_pockets.sort(key=lambda row: number(row.get("net_profit")))
    lines = [
        "# Stage337AE Completed-Day Forward Attribution Cost Stress(337AE 완성일 전진 귀속/비용 압박)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- decision(결정): `{DECISION}`",
        f"- completed_day_net(완성일 순수익): `{csv_value(completed.get('net_profit'))}`",
        f"- completed_day_pf(완성일 수익 팩터): `{csv_value(completed.get('profit_factor'))}`",
        f"- completed_day_closed_trade_dd(완성일 마감 거래 손실폭): `{csv_value(completed.get('max_closed_drawdown'))}`",
        f"- completed_day_mt5_equity_dd(완성일 MT5 평가금 손실폭): `{csv_value(completed.get('mt5_report_max_drawdown_amount'))}`",
        f"- completed_day_mt5_recovery(완성일 MT5 회복 계수): `{csv_value(completed.get('mt5_report_recovery_factor'))}`",
        f"- one_point_stress_pf(1포인트 압박 수익 팩터): `{csv_value(one_point.get('profit_factor'))}`",
        f"- five_point_stress_net(5포인트 압박 순수익): `{csv_value(five_point.get('net_profit'))}`",
        f"- parser_errors(파서 오류): `{len(parser_errors)}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- runtime_authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Read(판독)",
        "",
        "run337AD(337AD 실행)의 completed-day broker slice(완성일 브로커 구간)는 MT5(메타트레이더5) 거래 보고서 기준으로 순수익은 양수지만 PF(수익 팩터)와 recovery(회복)가 얇다. 1포인트 추가 비용에서 PF가 약해지고 5포인트 압박에서는 순수익이 깨진다.",
        "",
        "효과: 이 결과는 후보를 수정하지 않고도 cost buffer(비용 버퍼), curve pocket(곡선 포켓), direction mix(방향 혼합)의 약점을 다음 실패 기억/재구성 큐로 넘긴다. 최신 현재일 전체 forward(전진) 판정은 full current-day control(현재일 전체 대조군) 공백 때문에 아직 닫지 않는다.",
        "",
        "## Curve Pockets(곡선 포켓)",
        "",
        "| pocket(포켓) | bucket(구간) | net(순수익) | PF(수익 팩터) | trades(거래 수) | read(판독) |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in weak_pockets[:12]:
        lines.append(
            f"| `{row.get('pocket_type', '')}` | `{row.get('bucket', row.get('pocket_start', ''))}` | `{csv_value(row.get('net_profit'))}` | `{csv_value(row.get('profit_factor'))}` | `{csv_value(row.get('trade_count'))}` | `{row.get('curve_read', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Artifacts(산출물)",
            "",
            f"- frozen forward MT5 report(고정 전진 MT5 보고): `{rel(REPORT_PATH)}`",
            f"- regime attribution report(국면 귀속 보고): `{rel(REGIME_ATTRIBUTION)}`",
            f"- D/B attribution report(D/B 귀속 보고): `{rel(DB_ATTRIBUTION)}`",
            f"- lot-normalized report(랏 정규화 보고): `{rel(LOT_NORMALIZED)}`",
            f"- cost stress report(비용 압박 보고): `{rel(COST_STRESS)}`",
            f"- curve pocket report(곡선 포켓 보고): `{rel(CURVE_POCKET)}`",
            f"- final forward decision report(최종 전진 결정 보고): `{rel(FINAL_DECISION)}`",
            "",
            "## Attribution Boundary(귀속 경계)",
            "",
            f"- D/B attribution(D/B 귀속): `{db_rows[0].get('db_source_status', 'not_available') if db_rows else 'not_available'}`",
            f"- economic external fields(경제 외부 필드): `{sum(1 for row in economic_rows if row.get('available_in_feature_matrix'))}/{len(economic_rows)}` available(사용 가능)",
            "- no retune(재튜닝 없음): `true`",
            "- no threshold change(임계값 변경 없음): `true`",
            "- no lot optimization(랏 최적화 없음): `true`",
        ]
    )
    return "\n".join(lines)


def decision_doc_text(final_decision: Mapping[str, Any]) -> str:
    completed = final_decision.get("completed_day_slice", {})
    return f"""# 2026-05-27 Stage337AE Decision(337AE 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- completed_day_net(완성일 순수익): `{csv_value(completed.get('net_profit'))}`
- completed_day_pf(완성일 수익 팩터): `{csv_value(completed.get('profit_factor'))}`
- completed_day_mt5_equity_dd(완성일 MT5 평가금 손실폭): `{csv_value(completed.get('mt5_report_max_drawdown_amount'))}`
- completed_day_mt5_recovery(완성일 MT5 회복 계수): `{csv_value(completed.get('mt5_report_recovery_factor'))}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): completed-day attribution/cost stress(완성일 귀속/비용 압박)는 cp322A/u42 고정 산출물을 수정하지 않고 비용 버퍼와 곡선 취약성을 확인했다. 이 결과는 forward decision(전진 판정)이 아니라 no-overfit rebuild queue(무과적합 재구성 대기열)의 실패 기억이다.
"""


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows = read_csv(path)
    columns = list(rows[0].keys()) if rows else list(row.keys())
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    return write_csv(path, columns, rows)


def append_artifacts(paths: Sequence[Path]) -> Path:
    rows = read_csv(ARTIFACT_REGISTRY)
    columns = list(rows[0].keys()) if rows else [
        "artifact_id",
        "artifact_type",
        "path",
        "artifact_path",
        "sha256",
        "stage_id",
        "run_id",
        "created_at_utc",
        "notes",
        "claim_boundary",
    ]
    for column in ("artifact_id", "artifact_type", "path", "artifact_path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "claim_boundary"):
        if column not in columns:
            columns.append(column)
    rows = [row for row in rows if row.get("run_id") != RUN_ID]
    generated = now_utc()
    for path in paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        suffix = path.suffix.lower()
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "artifact_type": suffix.lstrip(".") or "file",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if suffix in {".csv", ".json", ".md", ".txt", ".py", ".yaml"} else sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        pattern = re.escape(marker) + r".*?(?=\n## |\Z)"
        return re.sub(pattern, block.strip(), text, count=1, flags=re.S)
    return text.rstrip() + "\n\n" + block.strip() + "\n"


def update_status_docs(final_decision: Mapping[str, Any]) -> list[Path]:
    completed = final_decision.get("completed_day_slice", {})
    one_point = final_decision.get("completed_day_one_point_stress", {})
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- completed_day_slice_gap(완성일 구간 공백): `tester_reached_feature_last`
- full_current_day_control_gap(현재일 전체 대조 공백): `tester_feature_last_gap_remains`
- completed_day_net(완성일 순수익): `{csv_value(completed.get('net_profit'))}`
- completed_day_pf(완성일 수익 팩터): `{csv_value(completed.get('profit_factor'))}`
- completed_day_mt5_equity_dd(완성일 MT5 평가금 손실폭): `{csv_value(completed.get('mt5_report_max_drawdown_amount'))}`
- completed_day_mt5_recovery(완성일 MT5 회복 계수): `{csv_value(completed.get('mt5_report_recovery_factor'))}`
- one_point_stress_pf(1포인트 압박 수익 팩터): `{csv_value(one_point.get('profit_factor'))}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `latest_current_day_visibility_boundary_not_operating_resolved`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AE(337AE 실행)는 completed-day broker slice(완성일 브로커 구간)의 귀속/비용 압박을 만들었고, 비용 버퍼와 회복 곡선이 얇아 Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    write_md(SELECTED_STATUS, selection_text)
    changed = [SELECTED_STATUS]
    if path_exists(WORKSPACE_STATE):
        text, bom = read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
        focus = (
            "- >-\n"
            f"  Stage337 run337AE focus complete: run337AE(337AE 실행)는 `{STATUS}`로 completed-day attribution/cost stress(완성일 귀속/비용 압박)를 완료했다. "
            f"Effect(효과): completed-day net(완성일 순수익) `{csv_value(completed.get('net_profit'))}`, PF(수익 팩터) `{csv_value(completed.get('profit_factor'))}`, "
            f"MT5 equity DD(MT5 평가금 손실폭) `{csv_value(completed.get('mt5_report_max_drawdown_amount'))}`, one-point stress PF(1포인트 압박 수익 팩터) `{csv_value(one_point.get('profit_factor'))}`를 기록했고 Forward/Goal(전진/목표)은 주장하지 않는다."
        )
        if "Stage337 run337AE focus complete" not in text:
            text = text.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
        else:
            text = re.sub(r"- >-\n  Stage337 run337AE focus complete:.*?(?=\n- >-|\Z)", focus, text, count=1, flags=re.S)
        write_text(WORKSPACE_STATE, text, bom)
        changed.append(WORKSPACE_STATE)
    if path_exists(CURRENT_STATE):
        text, bom = read_text(CURRENT_STATE)
        header = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `337_onnx_research_packet__cost_buffer_direction_curve_rebuild_v1`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `cost_buffer_direction_curve_rebuild`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
        text = re.sub(r"\A# Current Working State\(현재 작업 상태\).*?(?=\n## )", header.rstrip() + "\n", text, count=1, flags=re.S)
        block = f"""## Stage337 run337AE(337AE 실행) - {TODAY}

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): completed-day attribution/cost stress(완성일 귀속/비용 압박)로 비용 1포인트 압박과 곡선 포켓을 기록했다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
        text = append_once(text, "## Stage337 run337AE(337AE 실행)", block)
        write_text(CURRENT_STATE, text, bom)
        changed.append(CURRENT_STATE)
    if path_exists(CHANGELOG):
        text, bom = read_text(CHANGELOG)
        line = f"- {TODAY}: Stage337 run337AE(337AE 실행) `{STATUS}`. Effect(효과): completed-day attribution/cost stress(완성일 귀속/비용 압박)를 완료했고 Forward/Goal(전진/목표)은 주장하지 않음."
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
        write_text(CHANGELOG, text, bom)
        changed.append(CHANGELOG)
    if path_exists(STAGE_BRIEF):
        text, bom = read_text(STAGE_BRIEF)
        text = replace_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        summary = f"- run337AE_summary(337AE 요약): `{STATUS}`. Effect(효과): completed-day net(완성일 순수익) `{csv_value(completed.get('net_profit'))}`, PF(수익 팩터) `{csv_value(completed.get('profit_factor'))}`, MT5 equity DD(MT5 평가금 손실폭) `{csv_value(completed.get('mt5_report_max_drawdown_amount'))}`, 비용 압박 취약성을 기록했다.\n"
        if "run337AE_summary(337AE 요약)" in text:
            text = re.sub(r"- run337AE_summary\(337AE 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
        else:
            text = text.replace("- selected_candidate(선택 후보):", summary + "- selected_candidate(선택 후보):")
        write_text(STAGE_BRIEF, text, bom)
        changed.append(STAGE_BRIEF)
    return changed


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    trades, parser_checks, parser_errors = build_trade_records()
    signal_rows = build_signal_rows()
    regime_rows = build_slice_rows(trades)
    db_rows = build_db_rows(trades)
    lot_rows = build_lot_rows(trades)
    cost_rows = build_cost_stress_rows(trades)
    curve_rows = build_curve_rows(trades, regime_rows, cost_rows)
    economic_rows = build_economic_regime_audit(trades)
    gates = gate_rows(trades, parser_checks, parser_errors, signal_rows, regime_rows, db_rows, lot_rows, cost_rows, curve_rows, economic_rows)
    final_decision = build_final_decision(curve_rows, cost_rows, db_rows, economic_rows)

    artifacts = [
        write_csv(TRADE_RECORDS, list(trades[0].keys()) if trades else ["run_id"], trades),
        write_csv(PARSER_CHECKS, list(parser_checks[0].keys()) if parser_checks else ["attempt_name", "parser_status"], parser_checks),
        write_csv(PARSER_ERRORS, list(parser_errors[0].keys()) if parser_errors else ["attempt_name", "error"], parser_errors),
        write_csv(SIGNAL_ATTRIBUTION, list(signal_rows[0].keys()) if signal_rows else ["attempt_name"], signal_rows),
        write_csv(REGIME_ATTRIBUTION, list(regime_rows[0].keys()) if regime_rows else ["attempt_name"], regime_rows),
        write_csv(DB_ATTRIBUTION, list(db_rows[0].keys()) if db_rows else ["attempt_name"], db_rows),
        write_csv(LOT_NORMALIZED, list(lot_rows[0].keys()) if lot_rows else ["attempt_name"], lot_rows),
        write_csv(COST_STRESS, list(cost_rows[0].keys()) if cost_rows else ["attempt_name"], cost_rows),
        write_csv(CURVE_POCKET, list(curve_rows[0].keys()) if curve_rows else ["attempt_name"], curve_rows),
        write_csv(ECONOMIC_REGIME_AUDIT, list(economic_rows[0].keys()) if economic_rows else ["field"], economic_rows),
        write_csv(GATE_AUDIT, ["gate_name", "status", "evidence_path", "effect"], gates),
        write_json(FINAL_DECISION, final_decision),
        write_json(
            INPUT_IDENTITY,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "source_execution": rel(SOURCE_EXECUTION),
                "source_runtime_summary": rel(SOURCE_RUNTIME_SUMMARY),
                "source_kpi_summary": rel(SOURCE_KPI_SUMMARY),
                "source_gap": rel(SOURCE_GAP),
                "source_parity": rel(SOURCE_PARITY),
                "source_usability": rel(SOURCE_USABILITY),
                "source_run_manifest": rel(SOURCE_RUN_MANIFEST),
                "attempts": list(ATTEMPT_FEATURES),
                "frozen_rules": [
                    "no model change",
                    "no adapter change",
                    "no feature order change",
                    "no threshold change",
                    "no risk logic change",
                    "no lot optimization",
                    "no ATR SL/TP change",
                    "no runtime handoff change",
                ],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_RECEIPT,
            {
                "data_source": [rel(SOURCE_EXECUTION), rel(SOURCE_KPI_SUMMARY), rel(SOURCE_GAP), rel(SOURCE_PARITY)],
                "time_axis": "MT5 Strategy Tester server timestamps are treated as UTC-like project timestamps matching run337AD telemetry and feature rows.",
                "sample_scope": "US100 M5 completed-day broker slice from 2026-04-14T01:05:00Z through 2026-05-26T23:55:00Z; full current-day control remains boundary-only.",
                "missing_or_duplicate_check": "parser trade count is matched against MT5 report metrics; feature lookup uses nearest feature row at or before trade open.",
                "feature_label_boundary": "no label rebuild, no training, no threshold search; realized trades only.",
                "split_boundary": "forward completed-day runtime probe only, not full latest forward pass/fail.",
                "leakage_risk": "economic regime external fields are unavailable in u42 no-external feature matrix and are not backfilled.",
                "data_hash_or_identity": rel(INPUT_IDENTITY),
                "integrity_judgment": "usable_for_completed_day_attribution_with_forward_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            PERFORMANCE_RECEIPT,
            {
                "observed_change": "completed-day runtime slice is profitable but cost and recovery robustness are thin",
                "comparison_baseline": PARENT_RUN_ID,
                "likely_drivers": ["long-heavy signal mix", "thin PF", "fixed 0.1 lot", "completed-day tester boundary"],
                "segment_checks": [rel(SIGNAL_ATTRIBUTION), rel(REGIME_ATTRIBUTION), rel(DB_ATTRIBUTION), rel(CURVE_POCKET), rel(COST_STRESS)],
                "trade_shape": final_decision.get("completed_day_slice", {}),
                "alternative_explanations": ["Strategy Tester current-day cutoff", "u42 no-external source missing VIX/USD/rate regimes"],
                "attribution_confidence": "medium_for_completed_day_only",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_RECEIPT,
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(SOURCE_EXECUTION),
                "shared_contract": "run337AD frozen ONNX, feature order, threshold, risk, lot, ATR SL/TP and runtime handoff are unchanged.",
                "known_differences": "full current-day control still stops at completed-day tester cutoff",
                "parity_check": rel(SOURCE_PARITY),
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            BACKTEST_RECEIPT,
            {
                "tester_identity": "run337AD portable MT5 FPMarkets US100 M5 Strategy Tester reports",
                "ea_identity": "ObsidianPrimeV2_RuntimeProbeEA with run337AD set/ini copies",
                "report_identity": [rel(report_path(row)) for row in source_execution_rows()],
                "trade_evidence": {"trade_rows": len(trades), "parser_checks": len(parser_checks), "parser_errors": len(parser_errors)},
                "cost_assumptions": "base MT5 report costs retained; cost stress adds post-hoc point-based round-trip stress without changing EA or lot",
                "forensic_checks": [rel(PARSER_CHECKS), rel(COST_STRESS), rel(CURVE_POCKET)],
                "backtest_judgment": "usable_with_boundary_for_completed_day_attribution_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            MODEL_VALIDATION_RECEIPT,
            {
                "model_family": "frozen run337AD u42 ONNX package",
                "target_and_label": "unchanged from parent package; no label rebuild in run337AE",
                "split_method": "completed-day forward runtime probe attribution",
                "selection_metric": "not_applicable_no_selection",
                "secondary_metrics": ["cost stress", "direction attribution", "curve pocket", "lot-normalized result"],
                "threshold_policy": "fixed_unchanged",
                "overfit_risk": "completed-day positive net may be too thin under cost and curve pocket stress",
                "calibration_risk": "scores are used only through frozen runtime decision surface",
                "comparison_baseline": PARENT_RUN_ID,
                "validation_judgment": "negative_with_boundary_no_forward_pass_fail",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(TRADE_RECORDS), rel(SIGNAL_ATTRIBUTION), rel(REGIME_ATTRIBUTION), rel(COST_STRESS), rel(CURVE_POCKET), rel(FINAL_DECISION)],
                "evidence_missing": ["full latest current-day Strategy Tester visibility", "D/B source columns", "VIX/USD/rate feature columns"],
                "judgment_label": "negative",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "완성일 구간에서는 돈을 벌었지만 비용과 곡선이 얇아 강건하다고 말할 수 없다.",
            },
        ),
    ]
    artifacts.extend(
        [
            write_md(REPORT_PATH, report_text(final_decision, curve_rows, cost_rows, db_rows, economic_rows, parser_errors)),
            write_md(DECISION_DOC, decision_doc_text(final_decision)),
        ]
    )
    artifacts.extend(update_status_docs(final_decision))
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "completed_day_forward_attribution_cost_stress",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        },
    )
    upsert_csv(
        STAGE_LEDGER,
        ["run_key"],
        {
            "run_key": f"{RUN_ID}__completed_day_forward_attribution_cost_stress",
            "ledger_row_id": f"{RUN_ID}__completed_day_forward_attribution_cost_stress",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "family": "completed_day_forward_attribution_cost_stress",
            "work_family": "kpi_evidence_runtime_backtest_attribution",
            "question": "does the completed-day forward slice survive cost, curve, direction and regime attribution without retuning",
            "metric_scope": "completed_day_runtime_probe_trade_level_attribution_cost_stress_no_forward_decision",
            "evidence_scope": "run337AD MT5 reports telemetry features and parity receipts",
            "kpi_scope": "diagnostic_negative_with_forward_boundary",
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "primary_artifact": rel(REPORT_PATH),
            "path": rel(REPORT_PATH),
            "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            "decision": DECISION,
        },
    )
    artifacts.extend([RUN_REGISTRY, STAGE_LEDGER])
    artifacts.append(
        write_json(
            RUN_MANIFEST,
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "parent_run_id": PARENT_RUN_ID,
                "primary_family": "kpi_evidence",
                "primary_skill": "obsidian-performance-attribution",
                "support_skills": [
                    "obsidian-data-integrity",
                    "obsidian-backtest-forensics",
                    "obsidian-runtime-parity",
                    "obsidian-model-validation",
                    "obsidian-result-judgment",
                ],
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_action": NEXT_RUN_ID,
                "artifacts": [rel(path) for path in artifacts],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifacts.append(append_artifacts([*artifacts, Path(__file__)]))
    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "trade_rows": len(trades),
                    "parser_errors": len(parser_errors),
                    "completed_day_curve_read": final_decision.get("completed_day_slice", {}).get("curve_read"),
                    "one_point_stress_read": final_decision.get("completed_day_one_point_stress", {}).get("stress_read"),
                    "next_action": NEXT_RUN_ID,
                    "goal_achieve": "not_claimed",
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
