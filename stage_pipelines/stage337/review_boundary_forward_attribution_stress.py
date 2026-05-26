from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean, median
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
RUN_NUMBER = "run337R"
RUN_ID = "run337R_fresh_boundary_repaired_forward_attribution_and_asof_policy_review_v1"
PARENT_RUN_ID = "run337Q_review_runtime_data_and_feature_source_repair_probe_v1"
NEXT_RUN_ID = "run337S_tester_visible_source_policy_repair_or_next_data_boundary_probe_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337R_boundary_forward_attribution_stress_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS = "completed_stage337R_boundary_attribution_stress_forward_blocked_no_goal_achieve"
JUDGMENT = "forward_blocked_by_tester_current_day_gap_and_asof_source_policy_after_attribution_review"
DECISION = "stage337R_open_run337S_tester_visible_source_policy_repair_or_next_data_boundary_probe_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337Q_DIR = STAGE_DIR / "02_runs" / "run337Q"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337R_boundary_forward_attribution_stress_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337R_boundary_forward_attribution_stress_review.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SOURCE_EXECUTION = RUN337Q_DIR / "runtime_execution_result.json"
SOURCE_ATTEMPTS = RUN337Q_DIR / "boundary_repair_handoff_attempts.json"
SOURCE_RUNTIME = RUN337Q_DIR / "fresh_mt5_runtime_probe_result.csv"
SOURCE_GAP = RUN337Q_DIR / "tester_feature_last_gap_reprobe.csv"
SOURCE_ASOF = RUN337Q_DIR / "asof_source_policy_review.csv"
SOURCE_BOUNDARY = RUN337Q_DIR / "tester_date_boundary_log_audit.csv"
SOURCE_PARITY = RUN337Q_DIR / "timestamp_aligned_proxy_mt5_difference.csv"

TRADE_RECORDS = RUN_DIR / "trade_records.csv"
PARSER_CHECKS = RUN_DIR / "report_parser_checks.csv"
PARSER_ERRORS = RUN_DIR / "report_parser_errors.csv"
REGIME_ATTRIBUTION = RUN_DIR / "regime_attribution_report.csv"
DB_ATTRIBUTION = RUN_DIR / "db_attribution_report.csv"
LOT_NORMALIZED = RUN_DIR / "lot_normalized_report.csv"
COST_STRESS = RUN_DIR / "cost_stress_report.csv"
CURVE_POCKET = RUN_DIR / "curve_pocket_report.csv"
FORWARD_DECISION = RUN_DIR / "final_forward_decision_report.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"

STRESS_POINTS = (0.0, 0.5, 1.0, 2.0, 5.0, 10.0)
DEPOSIT = 500.0


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
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8"), had_bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt", ".yaml"} else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(normalized)
    return path


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def profit_factor(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> float | None:
    wins = sum(number(row.get(key)) for row in rows if number(row.get(key)) > 0.0)
    losses = -sum(number(row.get(key)) for row in rows if number(row.get(key)) < 0.0)
    if losses == 0.0:
        return math.inf if wins > 0.0 else None
    return wins / losses


def max_closed_drawdown(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> tuple[float, int, float]:
    balance = DEPOSIT
    peak = DEPOSIT
    max_dd = 0.0
    longest_underwater = 0
    current_underwater = 0
    underwater_count = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        balance += number(row.get(key))
        if balance >= peak:
            peak = balance
            current_underwater = 0
        else:
            current_underwater += 1
            underwater_count += 1
            longest_underwater = max(longest_underwater, current_underwater)
        max_dd = max(max_dd, peak - balance)
    share = underwater_count / len(rows) if rows else 0.0
    return max_dd, longest_underwater, share


def metrics(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> dict[str, Any]:
    count = len(rows)
    net = sum(number(row.get(key)) for row in rows)
    gross_profit = sum(number(row.get(key)) for row in rows if number(row.get(key)) > 0.0)
    gross_loss = sum(number(row.get(key)) for row in rows if number(row.get(key)) < 0.0)
    dd, underwater, underwater_share = max_closed_drawdown(rows, key)
    return {
        "trade_count": count,
        "net_profit": net,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor(rows, key),
        "expectancy": net / count if count else None,
        "max_closed_drawdown": dd,
        "recovery_factor": net / dd if dd else None,
        "longest_underwater_trades": underwater,
        "underwater_trade_share": underwater_share,
    }


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
    val = number(value, math.nan)
    if not math.isfinite(val):
        return f"{label}_missing"
    low = -math.inf
    for cut in cuts:
        if val < cut:
            return f"{label}_{low:g}_to_{cut:g}"
        low = cut
    return f"{label}_{low:g}_plus"


def feature_frame(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(io_path(path))
    timestamp_column = next((col for col in ("timestamp_utc", "bar_time_server", "timestamp") if col in frame.columns), None)
    if timestamp_column is None:
        frame["feature_ts"] = pd.NaT
    else:
        frame["feature_ts"] = (
            pd.to_datetime(frame[timestamp_column].astype(str).str.replace(".", "-", regex=False), errors="coerce", utc=True)
            .dt.tz_convert(None)
        )
    return frame.dropna(subset=["feature_ts"]).sort_values("feature_ts").reset_index(drop=True)


def feature_at(features: pd.DataFrame, ts: pd.Timestamp) -> Mapping[str, Any]:
    if features.empty:
        return {}
    key_ts = pd.Timestamp(ts)
    key = key_ts.tz_convert(None) if key_ts.tzinfo else key_ts
    index = features["feature_ts"].searchsorted(key, side="right") - 1
    if index < 0:
        return {}
    return features.iloc[int(index)].to_dict()


def attempts_by_name() -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in read_json(SOURCE_ATTEMPTS)}


def execution_reports() -> list[Mapping[str, Any]]:
    result = read_json(SOURCE_EXECUTION)
    return list(result.get("execution_results", []))


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
        if volume > 0 and delta > 0 and gross > 0:
            values.append(gross / (delta * volume))
    return median(values) if values else 1.0


def build_trade_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    attempts = attempts_by_name()
    feature_cache: dict[str, pd.DataFrame] = {}
    rows: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for exec_row in execution_reports():
        attempt_name = str(exec_row.get("attempt_name", ""))
        attempt = attempts.get(attempt_name, {})
        path = report_path(exec_row)
        try:
            parsed = parse_mt5_trade_report(path)
            trades = pair_deals_into_trades(parsed["deals"])
        except Exception as exc:  # pragma: no cover - persisted as evidence.
            errors.append({"attempt_name": attempt_name, "report_path": rel(path), "error": str(exc), "claim_boundary": CLAIM_BOUNDARY})
            continue
        metrics_payload = exec_row.get("strategy_tester_report", {}).get("metrics", {})
        expected_count = int(number(metrics_payload.get("trade_count")))
        checks.append(
            {
                "attempt_name": attempt_name,
                "report_path": rel(path),
                "expected_trade_count": expected_count,
                "parsed_trade_count": len(trades),
                "trade_count_delta": len(trades) - expected_count,
                "parser_status": "matched" if len(trades) == expected_count else "count_mismatch",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        feature_path = ROOT / str(attempt.get("feature_local_path", ""))
        feature_key = feature_path.as_posix()
        if feature_key not in feature_cache:
            feature_cache[feature_key] = feature_frame(feature_path) if path_exists(feature_path) else pd.DataFrame()
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
        for idx, trade in enumerate(ordered):
            open_time = pd.Timestamp(trade.open_time)
            close_time = pd.Timestamp(trade.close_time)
            feat = feature_at(features, open_time)
            row = {
                "run_id": RUN_ID,
                "source_run_id": PARENT_RUN_ID,
                "attempt_name": attempt_name,
                "artifact_slug": exec_row.get("artifact_slug", ""),
                "feature_set_id": exec_row.get("feature_set_id", ""),
                "model_id": exec_row.get("model_id", ""),
                "candidate_id": attempt.get("candidate_id", ""),
                "decision_surface_mapping": attempt.get("decision_surface_mapping", ""),
                "db_source_status": "not_available_in_stage337Q_repaired_onnx_attempts",
                "db_source": "not_available",
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
                "chron_segment": chronological_segment(idx, len(ordered)),
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
                "adx_14": feat.get("adx_14", ""),
                "historical_vol_20": feat.get("historical_vol_20", ""),
                "vix_zscore_20": feat.get("vix_zscore_20", ""),
                "us10yr_zscore_20": feat.get("us10yr_zscore_20", ""),
                "usdx_zscore_20": feat.get("usdx_zscore_20", ""),
                "minutes_from_cash_open": feat.get("minutes_from_cash_open", ""),
                "is_us_cash_open": feat.get("is_us_cash_open", ""),
                "vol_regime": numeric_bucket(feat.get("historical_vol_20"), "vol", (0.08, 0.14, 0.22)),
                "adx_regime": numeric_bucket(feat.get("adx_14"), "adx", (20, 25, 40)),
                "vix_regime": numeric_bucket(feat.get("vix_zscore_20"), "vix_z", (-1, 0, 1)),
                "rate_regime": numeric_bucket(feat.get("us10yr_zscore_20"), "us10yr_z", (-1, 0, 1)),
                "usd_regime": numeric_bucket(feat.get("usdx_zscore_20"), "usdx_z", (-1, 0, 1)),
                "source_report_path": rel(path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            rows.append(row)
    return rows, checks, errors


def grouped(rows: Iterable[Mapping[str, Any]], keys: Sequence[str]) -> dict[tuple[Any, ...], list[Mapping[str, Any]]]:
    out: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        out[tuple(row.get(key, "") for key in keys)].append(row)
    return out


def build_slice_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    axes = (
        "direction",
        "month",
        "weekday",
        "open_hour_utc",
        "session_utc",
        "chron_segment",
        "vol_regime",
        "adx_regime",
        "vix_regime",
        "rate_regime",
        "usd_regime",
        "is_us_cash_open",
    )
    rows: list[dict[str, Any]] = []
    for axis in axes:
        for key, items in grouped(trades, ("attempt_name", "feature_set_id", axis)).items():
            attempt, feature_set, bucket = key
            item = metrics(items)
            rows.append(
                {
                    "attempt_name": attempt,
                    "feature_set_id": feature_set,
                    "axis": axis,
                    "bucket": bucket,
                    **item,
                    "slice_read": slice_read(item),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def slice_read(item: Mapping[str, Any]) -> str:
    trades = int(number(item.get("trade_count")))
    net = number(item.get("net_profit"))
    pf = number(item.get("profit_factor"), math.nan)
    dd = number(item.get("max_closed_drawdown"))
    if trades < 3:
        return "too_thin_to_read"
    if net < 0 and dd >= 80:
        return "negative_deep_drawdown_slice"
    if net < 0:
        return "negative_slice"
    if math.isfinite(pf) and pf >= 1.4:
        return "constructive_slice"
    return "mixed_slice"


def build_db_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, items in grouped(trades, ("attempt_name", "feature_set_id", "db_source_status", "db_source", "decision_surface_mapping")).items():
        attempt, feature_set, status, source, mapping = key
        rows.append(
            {
                "attempt_name": attempt,
                "feature_set_id": feature_set,
                "db_source_status": status,
                "db_source": source,
                "decision_surface_mapping": mapping,
                **metrics(items),
                "interpretation": "D/B attribution unavailable in run337Q artifacts; source-family attribution retained instead",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for key, items in grouped(trades, ("attempt_name", "feature_set_id", "direction")).items():
        attempt, feature_set, direction = key
        rows.append(
            {
                "attempt_name": attempt,
                "feature_set_id": feature_set,
                "db_source_status": "direction_proxy_only",
                "db_source": f"direction_{direction}",
                "decision_surface_mapping": "long_short_attribution_not_D_B_source",
                **metrics(items),
                "interpretation": "Long/short attribution is present; D/B source is not present in this repaired ONNX handoff.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_lot_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, items in grouped(trades, ("attempt_name", "feature_set_id")).items():
        attempt, feature_set = key
        item = metrics(items)
        total_lots = sum(number(row.get("volume")) for row in items)
        rows.append(
            {
                "attempt_name": attempt,
                "feature_set_id": feature_set,
                **item,
                "total_lots": total_lots,
                "net_per_1lot": item["net_profit"] / total_lots if total_lots else None,
                "net_per_trade": item["net_profit"] / len(items) if items else None,
                "median_trade_lot": median([number(row.get("volume")) for row in items]) if items else None,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_cost_stress_rows(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, items in grouped(trades, ("attempt_name", "feature_set_id")).items():
        attempt, feature_set = key
        point_value = point_value_estimate(items)
        for stress in STRESS_POINTS:
            stressed: list[dict[str, Any]] = []
            for row in items:
                cost = stress * number(row.get("volume")) * point_value
                copy = dict(row)
                copy["stressed_net_profit"] = number(row.get("net_profit")) - cost
                stressed.append(copy)
            item = metrics(stressed, "stressed_net_profit")
            rows.append(
                {
                    "attempt_name": attempt,
                    "feature_set_id": feature_set,
                    "extra_round_trip_points": stress,
                    "point_value_per_1lot_estimate": point_value,
                    **item,
                    "stress_read": stress_read(item),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def stress_read(item: Mapping[str, Any]) -> str:
    net = number(item.get("net_profit"))
    pf = number(item.get("profit_factor"), math.nan)
    if net <= 0:
        return "cost_breaks_net"
    if math.isfinite(pf) and pf < 1.1:
        return "cost_leaves_thin_pf"
    return "cost_survives_this_scenario"


def build_curve_rows(trades: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, str]], gap_rows: Sequence[Mapping[str, str]], asof_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    runtime_by = {row["attempt_name"]: row for row in runtime_rows}
    gap_by = {row["attempt_name"]: row for row in gap_rows}
    asof_blocked = {row["feature_set_id"] for row in asof_rows if str(row.get("usable_for_forward_pass_fail", "")).lower() == "false"}
    rows: list[dict[str, Any]] = []
    slice_rows = build_slice_rows(trades)
    for key, items in grouped(trades, ("attempt_name", "feature_set_id")).items():
        attempt, feature_set = key
        item = metrics(items)
        month_items = [row for row in slice_rows if row["attempt_name"] == attempt and row["axis"] == "month" and int(number(row["trade_count"])) >= 3]
        chron_items = [row for row in slice_rows if row["attempt_name"] == attempt and row["axis"] == "chron_segment"]
        worst = min(month_items + chron_items, key=lambda row: number(row.get("net_profit")), default={})
        negative_months = [row for row in month_items if number(row.get("net_profit")) < 0.0]
        positive_month_ratio = (len(month_items) - len(negative_months)) / len(month_items) if month_items else None
        tester_gap = number(gap_by.get(attempt, {}).get("tester_to_feature_last_gap_minutes"))
        row = {
            "attempt_name": attempt,
            "feature_set_id": feature_set,
            **item,
            "runtime_report_net_profit": runtime_by.get(attempt, {}).get("net_profit", ""),
            "runtime_report_profit_factor": runtime_by.get(attempt, {}).get("profit_factor", ""),
            "runtime_report_max_drawdown_amount": runtime_by.get(attempt, {}).get("max_drawdown_amount", ""),
            "positive_month_ratio": positive_month_ratio,
            "negative_month_count": len(negative_months),
            "worst_slice_axis": worst.get("axis", ""),
            "worst_slice_bucket": worst.get("bucket", ""),
            "worst_slice_net_profit": worst.get("net_profit", ""),
            "worst_slice_trade_count": worst.get("trade_count", ""),
            "tester_to_feature_last_gap_minutes": tester_gap,
            "asof_forward_policy_blocked": feature_set in asof_blocked,
            "curve_read": curve_read(item, worst, tester_gap, feature_set in asof_blocked),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append(row)
    rows.sort(key=lambda row: (-number(row.get("net_profit")), number(row.get("max_closed_drawdown"))))
    return rows


def curve_read(item: Mapping[str, Any], worst: Mapping[str, Any], tester_gap: float, asof_blocked: bool) -> str:
    net = number(item.get("net_profit"))
    pf = number(item.get("profit_factor"), math.nan)
    dd = number(item.get("max_closed_drawdown"))
    worst_net = number(worst.get("net_profit"))
    if tester_gap > 0 or asof_blocked:
        return "blocked_for_forward_decision_even_if_runtime_probe_positive"
    if net <= 0 or not math.isfinite(pf) or pf <= 1:
        return "fragile_or_negative"
    if dd >= 120 or worst_net <= -80:
        return "curve_pocket_risk"
    return "constructive_runtime_probe_only"


def gate_rows(trades: Sequence[Mapping[str, Any]], parser_checks: Sequence[Mapping[str, Any]], parser_errors: Sequence[Mapping[str, Any]], curve_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, str]], asof_rows: Sequence[Mapping[str, str]], parity_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    parser_ok = parser_checks and not parser_errors and all(row.get("parser_status") == "matched" for row in parser_checks)
    tester_gap_count = sum(1 for row in gap_rows if str(row.get("gap_status")) != "tester_reached_feature_last")
    asof_blocks = sum(1 for row in asof_rows if str(row.get("usable_for_forward_pass_fail", "")).lower() == "false")
    parity_matches = sum(1 for row in parity_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    positive_runtime = sum(1 for row in curve_rows if number(row.get("net_profit")) > 0 and number(row.get("profit_factor"), math.nan) > 1)
    return [
        {
            "gate_name": "trade_report_parse",
            "status": "covered" if parser_ok else "covered_partial",
            "evidence_path": rel(PARSER_CHECKS),
            "effect": "MT5 report(보고서)의 deal list(거래 목록)를 trade records(거래 기록)로 변환했다.",
        },
        {
            "gate_name": "timestamp_aligned_runtime_parity",
            "status": "covered" if parity_matches == len(parity_rows) and parity_rows else "covered_partial",
            "evidence_path": rel(SOURCE_PARITY),
            "effect": f"timestamp-aligned proxy/MT5 parity(시점 맞춤 프록시/MT5 동등성)를 확인했다; matched={parity_matches}/{len(parity_rows)}.",
        },
        {
            "gate_name": "regime_attribution",
            "status": "covered" if trades else "blocked",
            "evidence_path": rel(REGIME_ATTRIBUTION),
            "effect": "direction/session/hour/month/volatility/ADX/VIX/USD/rate slices(방향/세션/시간/월/변동성/ADX/VIX/USD/금리 구간)를 만들었다.",
        },
        {
            "gate_name": "cost_stress_and_lot_normalized",
            "status": "covered" if trades else "blocked",
            "evidence_path": rel(COST_STRESS),
            "effect": "lot-normalized(랏 정규화)와 spread/slippage stress(스프레드/슬리피지 압박)를 만들었다.",
        },
        {
            "gate_name": "forward_decision_boundary",
            "status": "covered_blocked",
            "evidence_path": rel(FORWARD_DECISION),
            "effect": f"positive_runtime_rows={positive_runtime}; tester_gap_attempts={tester_gap_count}; asof_forward_blocks={asof_blocks}라서 Forward Passed/Failed(전진 통과/실패)는 주장하지 않는다.",
        },
        {
            "gate_name": "no_goal_achieve_claim",
            "status": "covered",
            "evidence_path": rel(DECISION_DOC),
            "effect": "Goal Achieve(목표 달성), runtime authority(런타임 권위), deployment(배포)를 모두 닫아뒀다.",
        },
    ]


def build_report(curve_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, str]], asof_rows: Sequence[Mapping[str, str]], parser_errors: Sequence[Mapping[str, Any]]) -> str:
    best = curve_rows[0] if curve_rows else {}
    tester_gap_count = sum(1 for row in gap_rows if str(row.get("gap_status")) != "tester_reached_feature_last")
    asof_blocks = sum(1 for row in asof_rows if str(row.get("usable_for_forward_pass_fail", "")).lower() == "false")
    cost_breaks = sum(1 for row in cost_rows if row.get("stress_read") == "cost_breaks_net" and number(row.get("extra_round_trip_points")) <= 2.0)
    lines = [
        "# Stage337R Boundary Forward Attribution Stress Review(337R 경계 전진 귀속 압박 리뷰)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- decision(결정): `{DECISION}`",
        f"- best_runtime_probe(최선 런타임 탐침): `{best.get('attempt_name', 'none')}` net(순익) `{csv_value(best.get('net_profit', ''))}`, PF(손익비) `{csv_value(best.get('profit_factor', ''))}`",
        f"- tester_gap_attempts(테스터 공백 시도): `{tester_gap_count}`",
        f"- asof_forward_blocks(시점 기준 전진 차단): `{asof_blocks}`",
        f"- low_cost_break_rows(낮은 비용 압박 붕괴 행): `{cost_breaks}`",
        f"- parser_errors(파서 오류): `{len(parser_errors)}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- Forward Blocked(전진 차단): `current_run_boundary`",
        "- runtime authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Runtime Curve(런타임 곡선)",
        "",
        "| attempt(시도) | feature(피처) | net(순익) | PF(손익비) | trades(거래수) | DD(손실폭) | worst pocket(최악 포켓) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for row in curve_rows:
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{row.get('feature_set_id', '')}` | `{csv_value(row.get('net_profit'))}` | `{csv_value(row.get('profit_factor'))}` | `{csv_value(row.get('trade_count'))}` | `{csv_value(row.get('max_closed_drawdown'))}` | `{row.get('worst_slice_axis', '')}:{row.get('worst_slice_bucket', '')}` | `{row.get('curve_read', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "run337R(337R 실행)는 새 후보 개발이 아니라 run337Q(337Q 실행)의 실제 Strategy Tester(전략 테스터) 산출물을 거래 목록 단위로 분해한 리뷰다. ONNX(온엑스), feature order(피처 순서), threshold(임계값), risk/lot(위험/랏)은 수정하지 않았다.",
            "",
            "효과: 일부 runtime probe(런타임 탐침) 지표는 양수지만, tester current-day gap(테스터 현재일 공백)과 as-of source policy(시점 기준 원천 정책) 때문에 Forward Passed/Failed(전진 통과/실패)는 닫지 않는다.",
        ]
    )
    return "\n".join(lines)


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
    columns = list(rows[0].keys()) if rows else ["artifact_id", "artifact_type", "path", "artifact_path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "claim_boundary"]
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
                "sha256": sha256_file_lf_normalized(path) if suffix in {".csv", ".json", ".md", ".txt", ".py"} else sha256_file(path),
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
        return text
    return text.rstrip() + "\n\n" + block.strip() + "\n"


def update_status_docs(curve_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    best = curve_rows[0] if curve_rows else {}
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- best_runtime_probe(최선 런타임 탐침): `{best.get('attempt_name', 'none')}`
- tester_reached_feature_last(테스터 피처 끝 도달): `0/5 from run337Q`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337R(337R 실행)는 거래 목록 기반 attribution/stress(귀속/압박)를 만들었고, tester current-day gap(테스터 현재일 공백)과 as-of source policy(시점 기준 원천 정책) 때문에 Forward decision(전진 판정)은 차단으로 남긴다.
"""
    write_md(SELECTED_STATUS, selection_text)

    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
        focus = (
            "- >-\n"
            f"  Stage337 run337R focus complete: Stage337(337단계) run337R(337R 실행)는 `{STATUS}`로 boundary forward attribution/stress review(경계 전진 귀속/압박 리뷰)를 완료했다. "
            "Effect(효과): MT5(메타트레이더5) 거래 목록을 방향/세션/월/변동성/ADX/VIX/USD/금리/비용/곡선 포켓으로 분해했지만 Forward/Goal(전진/목표)은 주장하지 않는다."
        )
        text = text.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1) if "Stage337 run337R focus complete" not in text else text
        write_text(WORKSPACE_STATE, text, had_bom)

    if path_exists(CURRENT_STATE):
        text, had_bom = read_text(CURRENT_STATE)
        block = f"""## Stage337 run337R(337R 실행) - {TODAY}

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): trade-level attribution/stress(거래 단위 귀속/압박)를 만들고 tester/as-of blockers(테스터/시점 기준 차단 요소)를 분리했다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
        write_text(CURRENT_STATE, append_once(text, "## Stage337 run337R(337R 실행)", block), had_bom)

    if path_exists(CHANGELOG):
        text, had_bom = read_text(CHANGELOG)
        line = f"- {TODAY}: Stage337 run337R(337R 실행) `{STATUS}`. Effect(효과): boundary forward attribution/stress review(경계 전진 귀속/압박 리뷰)를 완료했고 Forward/Goal(전진/목표) 주장은 없음."
        write_text(CHANGELOG, text.rstrip() + ("\n" + line + "\n" if line not in text else "\n"), had_bom)
    return [SELECTED_STATUS, WORKSPACE_STATE, CURRENT_STATE, CHANGELOG]


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    trades, parser_checks, parser_errors = build_trade_records()
    runtime_rows = read_csv(SOURCE_RUNTIME)
    gap_rows = read_csv(SOURCE_GAP)
    asof_rows = read_csv(SOURCE_ASOF)
    parity_rows = read_csv(SOURCE_PARITY)
    boundary_rows = read_csv(SOURCE_BOUNDARY)

    regime_rows = build_slice_rows(trades)
    db_rows = build_db_rows(trades)
    lot_rows = build_lot_rows(trades)
    cost_rows = build_cost_stress_rows(trades)
    curve_rows = build_curve_rows(trades, runtime_rows, gap_rows, asof_rows)
    gates = gate_rows(trades, parser_checks, parser_errors, curve_rows, gap_rows, asof_rows, parity_rows)

    artifacts = [
        write_csv(TRADE_RECORDS, list(trades[0].keys()) if trades else ["run_id"], trades),
        write_csv(PARSER_CHECKS, list(parser_checks[0].keys()) if parser_checks else ["attempt_name", "parser_status"], parser_checks),
        write_csv(PARSER_ERRORS, list(parser_errors[0].keys()) if parser_errors else ["attempt_name", "error"], parser_errors),
        write_csv(REGIME_ATTRIBUTION, list(regime_rows[0].keys()) if regime_rows else ["attempt_name"], regime_rows),
        write_csv(DB_ATTRIBUTION, list(db_rows[0].keys()) if db_rows else ["attempt_name"], db_rows),
        write_csv(LOT_NORMALIZED, list(lot_rows[0].keys()) if lot_rows else ["attempt_name"], lot_rows),
        write_csv(COST_STRESS, list(cost_rows[0].keys()) if cost_rows else ["attempt_name"], cost_rows),
        write_csv(CURVE_POCKET, list(curve_rows[0].keys()) if curve_rows else ["attempt_name"], curve_rows),
        write_csv(GATE_AUDIT, ["gate_name", "status", "evidence_path", "effect"], gates),
        write_json(
            FORWARD_DECISION,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "best_runtime_probe": curve_rows[0] if curve_rows else {},
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "forward_blocked": "current_run_boundary",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_RECEIPT,
            {
                "data_source": [rel(SOURCE_EXECUTION), rel(SOURCE_ATTEMPTS), rel(SOURCE_ASOF), rel(SOURCE_GAP)],
                "time_axis": "MT5 report trade times are tester server timestamps; feature context uses nearest feature timestamp at or before trade open time",
                "sample_scope": "US100 M5 2026-04-14 through tester-observed 2026-05-26 23:55 from run337Q",
                "feature_label_boundary": "no labels, no retraining, no threshold retune; only realized tester trade report parsing",
                "integrity_judgment": "usable_for_runtime_attribution_not_forward_pass_fail",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_RECEIPT,
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(SOURCE_EXECUTION),
                "shared_contract": "same run337Q frozen ONNX, feature order, threshold, risk, lot, ATR SL/TP and Strategy Tester reports",
                "parity_check": rel(SOURCE_PARITY),
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            BACKTEST_RECEIPT,
            {
                "tester_identity": "run337Q portable MT5 FPMarkets US100 M5 Strategy Tester reports",
                "trade_evidence": {"trade_rows": len(trades), "parser_checks": len(parser_checks), "parser_errors": len(parser_errors)},
                "cost_assumptions": "base report cost retained; stress report adds point-based round-trip cost proxy without changing EA",
                "backtest_judgment": "usable_with_boundary_for_attribution_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(TRADE_RECORDS), rel(REGIME_ATTRIBUTION), rel(COST_STRESS), rel(CURVE_POCKET), rel(FORWARD_DECISION)],
                "evidence_missing": ["tester inclusion of current-day feature tail", "forward-usable as-of policy for external source families"],
                "judgment_label": "blocked",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
            },
        ),
    ]
    artifacts.extend(
        [
            write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "artifacts": [rel(path) for path in artifacts], "claim_boundary": CLAIM_BOUNDARY}),
            write_md(REPORT_PATH, build_report(curve_rows, cost_rows, gap_rows, asof_rows, parser_errors)),
            write_md(
                DECISION_DOC,
                f"""# Stage337R Decision(337R 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): run337Q(337Q 실행)의 MT5 report(보고서)를 거래 단위로 파싱해 regime/cost/curve(국면/비용/곡선)를 확인했지만, tester current-day gap(테스터 현재일 공백)과 as-of source policy(시점 기준 원천 정책)가 남아 전진 통과/실패 판정은 차단으로 둔다.
""",
            ),
        ]
    )
    artifacts.extend(update_status_docs(curve_rows))
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "boundary_forward_attribution_stress",
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
            "run_key": f"{RUN_ID}__boundary_forward_attribution_stress",
            "ledger_row_id": f"{RUN_ID}__boundary_forward_attribution_stress",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "family": "boundary_forward_attribution_stress",
            "work_family": "runtime_backtest_attribution",
            "question": "where does tester-visible forward robustness hold or break under frozen handoff",
            "metric_scope": "trade_level_attribution_cost_stress_curve_pocket_no_forward_decision",
            "evidence_scope": "run337Q MT5 reports and telemetry",
            "kpi_scope": "diagnostic_forward_blocked",
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
    artifacts.append(append_artifacts(artifacts))
    print(json.dumps(json_ready({"status": STATUS, "judgment": JUDGMENT, "decision": DECISION, "trade_rows": len(trades), "parser_errors": len(parser_errors), "next_action": NEXT_RUN_ID, "goal_achieve": "not_claimed"}), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
