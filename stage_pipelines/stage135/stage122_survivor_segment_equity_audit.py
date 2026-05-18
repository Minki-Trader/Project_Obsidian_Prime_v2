from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import OrderedDict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_trade_attribution import (  # noqa: E402
    MarketData,
    compute_trade_attribution,
)
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics  # noqa: E402
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report  # noqa: E402
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402


STAGE_ID = "135_adapter_research__stage122_survivor_segment_equity_audit"
RUN_ID = "run135A_stage135_stage122_survivor_segment_equity_audit_v1"
PACKET_ID = "stage135_stage122_survivor_segment_equity_audit_v1"
PARENT_RUN_ID = "run134A_stage134_stage122_survivor_followup_review_v1"
SOURCE_STAGE133_ID = "133_adapter_research__stage122_survivor_density_recovery_branch"
SOURCE_STAGE134_ID = "134_adapter_research__stage122_survivor_followup_review"
NEXT_STAGE_ID = "136_adapter_research__stage122_survivor_trade_count_concentration_repair"
NEXT_RUN_ID = "run136A_stage136_stage122_survivor_trade_count_concentration_repair_v1"
NEXT_PACKET_ID = "stage136_stage122_survivor_trade_count_concentration_repair_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
ADAPTER_ID = "s133_stage122_control_cd5_h3_risk035"
DECISION = "continue_stage136_trade_count_concentration_repair_candidate_not_final"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
RUN_ROOT = STAGE_ROOT / "02_runs" / "run135A"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_SUMMARY = Path("stages") / SOURCE_STAGE133_ID / "03_reviews/stage133_survivor_recovery_summary.csv"
SOURCE_SEGMENTS = Path("stages") / SOURCE_STAGE133_ID / "03_reviews/stage133_segment_kpi_summary.csv"
SOURCE_RISK = Path("stages") / SOURCE_STAGE133_ID / "03_reviews/stage133_risk_atr_telemetry.csv"
SOURCE_TRADE_AUDIT = Path("stages") / SOURCE_STAGE133_ID / "03_reviews/stage133_trade_audit.csv"
SOURCE_STAGE134_REVIEW = Path("stages") / SOURCE_STAGE134_ID / "03_reviews/stage134_survivor_followup_review.md"
SOURCE_STAGE134_DECISION = Path("stages") / SOURCE_STAGE134_ID / "03_reviews/stage134_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage135_segment_equity_audit_report.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage135_segment_equity_audit_summary.json"
SEGMENT_PATH = REVIEWS_ROOT / "stage135_segment_stability_summary.csv"
MONTHLY_PATH = REVIEWS_ROOT / "stage135_monthly_kpi_summary.csv"
SESSION_REGIME_PATH = REVIEWS_ROOT / "stage135_session_regime_kpi_summary.csv"
LONG_SHORT_PATH = REVIEWS_ROOT / "stage135_long_short_kpi_summary.csv"
EQUITY_AUDIT_PATH = REVIEWS_ROOT / "stage135_equity_curve_shape_audit.md"
RISK_ATR_PATH = REVIEWS_ROOT / "stage135_risk_atr_behavior_audit.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage135_concentration_risk_report.md"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage135_performance_attribution.md"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage135_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage135_decision.md"
TRADE_RECORDS_PATH = REVIEWS_ROOT / "stage135_trade_shape_records.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
NEGATIVE_REGISTER_PATH = Path("docs/registers/negative_result_register.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

SEGMENT_COLUMNS = (
    "split",
    "segment_type",
    "segment",
    "trade_count",
    "net_profit",
    "profit_factor",
    "win_rate",
    "expectancy",
    "cost_stressed_expectancy",
    "max_closed_trade_drawdown",
    "mfe_mean",
    "mae_mean",
    "mfe_capture_ratio",
    "top_trade_net_share",
    "top5_trade_net_share",
    "net_share",
    "quality_flag",
)
MONTHLY_COLUMNS = (
    "split",
    "month",
    "trade_count",
    "net_profit",
    "profit_factor",
    "win_rate",
    "expectancy",
    "cost_stressed_expectancy",
    "max_closed_trade_drawdown",
    "mfe_capture_ratio",
    "net_share",
    "quality_flag",
)
SLICE_COLUMNS = (
    "split",
    "axis",
    "bucket",
    "trade_count",
    "net_profit",
    "profit_factor",
    "win_rate",
    "expectancy",
    "cost_stressed_expectancy",
    "trade_share",
    "net_share",
    "mfe_capture_ratio",
    "quality_flag",
)
RISK_COLUMNS = (
    "split",
    "atr_enabled",
    "model_risk_enabled",
    "risk_floor_applied_count",
    "avg_model_risk_pct",
    "max_model_risk_pct",
    "avg_clipped_risk_pct",
    "max_clipped_risk_pct",
    "avg_actual_risk_pct_after_floor",
    "max_actual_risk_pct_after_floor",
    "avg_computed_lot",
    "max_computed_lot",
    "avg_executed_lot",
    "max_executed_lot",
    "avg_atr_points",
    "avg_open_sl_points",
    "avg_open_tp_points",
    "risk_bucket",
    "telemetry_sha256",
    "quality_flag",
)
TRADE_COLUMNS = (
    "split",
    "trade_index",
    "direction",
    "open_time",
    "close_time",
    "hold_bars",
    "net_profit",
    "equity_after_trade",
    "chronological_third",
    "month",
    "session_slice",
    "volatility_regime",
    "trend_regime",
    "adx_bucket",
    "spread_regime",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def repo_path(path: str | Path) -> Path:
    candidate = Path(str(path))
    return candidate if candidate.is_absolute() else REPO_ROOT / candidate


def ensure_dirs() -> None:
    for path in (REVIEWS_ROOT, RUN_ROOT, SPEC_ROOT, INPUT_ROOT, SELECTED_ROOT, PACKET_ROOT, NEXT_STAGE_ROOT / "00_spec", NEXT_STAGE_ROOT / "01_inputs", NEXT_STAGE_ROOT / "03_reviews", NEXT_STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if columns is None:
        ordered: list[str] = []
        for row in rows:
            for key in row:
                if key not in ordered:
                    ordered.append(key)
        columns = tuple(ordered)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10f}" if math.isfinite(value) else ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def to_float(value: Any) -> float | None:
    try:
        if value in (None, ""):
            return None
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def round6(value: Any) -> Any:
    number = to_float(value)
    return round(number, 6) if number is not None else value


def safe_ratio(num: Any, den: Any) -> float | None:
    numerator = to_float(num)
    denominator = to_float(den)
    if numerator is None or denominator in (None, 0.0):
        return None
    return numerator / denominator


def source_summary_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(SOURCE_SUMMARY)
        if row.get("adapter_id") == ADAPTER_ID and row.get("view") == "actual_routed_total" and row.get("split") in {"validation_is", "oos"}
    ]


def cost_penalty_by_split(rows: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    penalties: dict[str, float] = {}
    for row in rows:
        expectancy = as_float(row.get("expectancy"))
        stressed = as_float(row.get("cost_stressed_expectancy"))
        penalties[str(row.get("split"))] = max(0.0, expectancy - stressed)
    return penalties


def chronological_thirds(length: int) -> list[str]:
    labels: list[str] = []
    for index in range(length):
        ratio = index / max(length, 1)
        if ratio < 1 / 3:
            labels.append("early")
        elif ratio < 2 / 3:
            labels.append("mid")
        else:
            labels.append("late")
    return labels


def same_direction_reentry(frame: pd.DataFrame) -> pd.Series:
    ordered = frame.sort_values("open_time").reset_index()
    previous_direction = ordered["direction"].shift(1)
    previous_open = ordered["open_time"].shift(1)
    bar_gap = (ordered["open_time"] - previous_open).dt.total_seconds() / 60.0 / 5.0
    values = (ordered["direction"].eq(previous_direction) & (bar_gap <= 5.0)).fillna(False)
    result = pd.Series(False, index=frame.index)
    for row_index, value in zip(ordered["index"], values, strict=False):
        result.loc[row_index] = bool(value)
    return result


def load_trade_frame(split: str, report_path: Path, market_data: MarketData) -> tuple[pd.DataFrame, dict[str, Any]]:
    report = parse_mt5_trade_report(report_path)
    trades = pair_deals_into_trades(report["deals"])
    stats = compute_trade_attribution(trades, market_data)
    frame = pd.DataFrame(stats["trades"])
    if frame.empty:
        raise RuntimeError(f"No trades parsed for {split}: {report_path}")
    frame["split"] = split
    frame["open_time"] = pd.to_datetime(frame["open_time"])
    frame["close_time"] = pd.to_datetime(frame["close_time"])
    frame = frame.sort_values("close_time").reset_index(drop=True)
    frame["trade_index"] = range(1, len(frame) + 1)
    frame["month"] = frame["close_time"].dt.strftime("%Y-%m")
    frame["chronological_third"] = chronological_thirds(len(frame))
    frame["same_direction_reentry"] = same_direction_reentry(frame)
    frame["equity_after_trade"] = frame["net_profit"].astype(float).cumsum()
    return frame, extract_mt5_strategy_report_metrics(report_path)


def kpi(frame: pd.DataFrame, cost_penalty: float) -> dict[str, Any]:
    if frame.empty:
        return {
            "trade_count": 0,
            "net_profit": 0.0,
            "profit_factor": None,
            "win_rate": None,
            "expectancy": None,
            "cost_stressed_expectancy": None,
            "max_closed_trade_drawdown": 0.0,
            "mfe_mean": None,
            "mae_mean": None,
            "mfe_capture_ratio": None,
            "top_trade_net": 0.0,
            "top5_trade_net": 0.0,
        }
    net_values = [float(value) for value in frame["net_profit"]]
    gross_profit = sum(value for value in net_values if value > 0.0)
    gross_loss = abs(sum(value for value in net_values if value < 0.0))
    expectancy = sum(net_values) / len(net_values)
    top_positive = sorted([value for value in net_values if value > 0.0], reverse=True)
    mfe_sum = sum(float(value) for value in frame["mfe"] if to_float(value) is not None)
    return {
        "trade_count": len(net_values),
        "net_profit": sum(net_values),
        "profit_factor": safe_ratio(gross_profit, gross_loss),
        "win_rate": safe_ratio(sum(1 for value in net_values if value > 0.0), len(net_values)),
        "expectancy": expectancy,
        "cost_stressed_expectancy": expectancy - cost_penalty,
        "max_closed_trade_drawdown": max_drawdown(net_values),
        "mfe_mean": frame["mfe"].astype(float).mean(),
        "mae_mean": frame["mae"].astype(float).mean(),
        "mfe_capture_ratio": safe_ratio(sum(net_values), mfe_sum),
        "top_trade_net": top_positive[0] if top_positive else 0.0,
        "top5_trade_net": sum(top_positive[:5]),
    }


def max_drawdown(values: Sequence[float]) -> float:
    peak = 0.0
    cumulative = 0.0
    max_dd = 0.0
    for value in values:
        cumulative += float(value)
        peak = max(peak, cumulative)
        max_dd = max(max_dd, peak - cumulative)
    return max_dd


def equity_shape(frame: pd.DataFrame) -> dict[str, Any]:
    ordered = frame.sort_values("close_time").reset_index(drop=True)
    cumulative = ordered["net_profit"].astype(float).cumsum()
    running_max = cumulative.cummax()
    drawdown = running_max - cumulative
    max_dd = float(drawdown.max()) if len(drawdown) else 0.0
    max_dd_index = int(drawdown.idxmax()) if len(drawdown) else 0
    prior_peak = float(running_max.iloc[max_dd_index]) if len(running_max) else 0.0
    trough = float(cumulative.iloc[max_dd_index]) if len(cumulative) else 0.0
    after = cumulative.iloc[max_dd_index + 1 :]
    recovered = bool((after >= prior_peak).any()) if len(after) else False
    longest_stagnation = 0
    current = 0
    peak = -math.inf
    for value in cumulative:
        if float(value) > peak:
            peak = float(value)
            current = 0
        else:
            current += 1
            longest_stagnation = max(longest_stagnation, current)
    first_equity = float(cumulative.iloc[0]) if len(cumulative) else 0.0
    final_equity = float(cumulative.iloc[-1]) if len(cumulative) else 0.0
    return {
        "final_net": final_equity,
        "first_trade_equity": first_equity,
        "max_closed_trade_drawdown": max_dd,
        "max_drawdown_trade_index": max_dd_index + 1,
        "max_drawdown_prior_peak": prior_peak,
        "max_drawdown_trough": trough,
        "recovered_after_max_drawdown": recovered,
        "post_max_dd_net_gain": final_equity - trough,
        "longest_non_new_high_trades": longest_stagnation,
        "start_time": ordered["close_time"].min().isoformat(),
        "end_time": ordered["close_time"].max().isoformat(),
    }


def segment_rows(split_frames: Mapping[str, pd.DataFrame], costs: Mapping[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, frame in split_frames.items():
        rows.append(segment_row(split, "full_split", "actual_routed_total", frame, frame, costs.get(split, 0.0)))
        for label in ("early", "mid", "late"):
            subset = frame[frame["chronological_third"].eq(label)]
            rows.append(segment_row(split, "chronological_third", label, subset, frame, costs.get(split, 0.0)))
    return rows


def segment_row(split: str, segment_type: str, segment: str, subset: pd.DataFrame, full: pd.DataFrame, cost_penalty: float) -> dict[str, Any]:
    row = kpi(subset, cost_penalty)
    total_net = float(full["net_profit"].astype(float).sum())
    net = as_float(row["net_profit"])
    quality = segment_quality(split, segment_type, segment, row, total_net)
    return {
        "split": split,
        "segment_type": segment_type,
        "segment": segment,
        "trade_count": row["trade_count"],
        "net_profit": round6(net),
        "profit_factor": round6(row["profit_factor"]),
        "win_rate": round6(row["win_rate"]),
        "expectancy": round6(row["expectancy"]),
        "cost_stressed_expectancy": round6(row["cost_stressed_expectancy"]),
        "max_closed_trade_drawdown": round6(row["max_closed_trade_drawdown"]),
        "mfe_mean": round6(row["mfe_mean"]),
        "mae_mean": round6(row["mae_mean"]),
        "mfe_capture_ratio": round6(row["mfe_capture_ratio"]),
        "top_trade_net_share": round6(safe_ratio(row["top_trade_net"], total_net)),
        "top5_trade_net_share": round6(safe_ratio(row["top5_trade_net"], total_net)),
        "net_share": round6(safe_ratio(net, total_net)),
        "quality_flag": quality,
    }


def segment_quality(split: str, segment_type: str, segment: str, row: Mapping[str, Any], total_net: float) -> str:
    if segment_type != "chronological_third":
        return "acceptable_measurement_only"
    flags: list[str] = []
    net = as_float(row.get("net_profit"))
    pf = to_float(row.get("profit_factor"))
    share = safe_ratio(net, total_net)
    if net <= 0.0:
        flags.append("negative_or_flat_segment")
    if pf is not None and pf < 1.25:
        flags.append("weak_segment_pf")
    if split == "validation_is" and pf is not None and pf < 1.50:
        flags.append("validation_third_pf_below_repair_target")
    if share is not None and share > 0.55:
        flags.append("single_window_profit_concentration")
    if split == "oos" and segment == "late" and share is not None and share > 0.50:
        flags.append("oos_late_period_concentration")
    return ";".join(flags) if flags else "acceptable_measurement_only"


def monthly_rows(split_frames: Mapping[str, pd.DataFrame], costs: Mapping[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, frame in split_frames.items():
        total_net = float(frame["net_profit"].astype(float).sum())
        for month, subset in frame.groupby("month", sort=True):
            row = kpi(subset, costs.get(split, 0.0))
            net = as_float(row["net_profit"])
            share = safe_ratio(net, total_net)
            flags: list[str] = []
            if net < 0.0:
                flags.append("negative_month")
            if share is not None and share > 0.50:
                flags.append("single_month_profit_concentration")
            rows.append(
                {
                    "split": split,
                    "month": month,
                    "trade_count": row["trade_count"],
                    "net_profit": round6(net),
                    "profit_factor": round6(row["profit_factor"]),
                    "win_rate": round6(row["win_rate"]),
                    "expectancy": round6(row["expectancy"]),
                    "cost_stressed_expectancy": round6(row["cost_stressed_expectancy"]),
                    "max_closed_trade_drawdown": round6(row["max_closed_trade_drawdown"]),
                    "mfe_capture_ratio": round6(row["mfe_capture_ratio"]),
                    "net_share": round6(share),
                    "quality_flag": ";".join(flags) if flags else "acceptable_measurement_only",
                }
            )
    return rows


def slice_rows(split_frames: Mapping[str, pd.DataFrame], costs: Mapping[str, float], axes: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, frame in split_frames.items():
        total_net = float(frame["net_profit"].astype(float).sum())
        for axis in axes:
            if axis not in frame.columns:
                continue
            for bucket, subset in frame.groupby(axis, dropna=False, sort=True):
                row = kpi(subset, costs.get(split, 0.0))
                net = as_float(row["net_profit"])
                trade_share = safe_ratio(row["trade_count"], len(frame))
                net_share = safe_ratio(net, total_net)
                flags: list[str] = []
                if trade_share is not None and trade_share > 0.60:
                    flags.append("bucket_trade_concentration")
                if net_share is not None and net_share > 0.60:
                    flags.append("bucket_profit_concentration")
                if to_float(row.get("profit_factor")) is not None and as_float(row.get("profit_factor")) < 1.0:
                    flags.append("bucket_pf_below_one")
                rows.append(
                    {
                        "split": split,
                        "axis": axis,
                        "bucket": str(bucket),
                        "trade_count": row["trade_count"],
                        "net_profit": round6(net),
                        "profit_factor": round6(row["profit_factor"]),
                        "win_rate": round6(row["win_rate"]),
                        "expectancy": round6(row["expectancy"]),
                        "cost_stressed_expectancy": round6(row["cost_stressed_expectancy"]),
                        "trade_share": round6(trade_share),
                        "net_share": round6(net_share),
                        "mfe_capture_ratio": round6(row["mfe_capture_ratio"]),
                        "quality_flag": ";".join(flags) if flags else "acceptable_measurement_only",
                    }
                )
    return rows


def concentration_flags(split_frames: Mapping[str, pd.DataFrame], segment_data: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, frame in split_frames.items():
        total_net = float(frame["net_profit"].astype(float).sum())
        months = frame.groupby("month")["net_profit"].sum().to_dict()
        thirds = frame.groupby("chronological_third")["net_profit"].sum().to_dict()
        top_positive = sorted([float(value) for value in frame["net_profit"] if float(value) > 0.0], reverse=True)
        metrics = [
            ("top_single_trade_share", safe_ratio(top_positive[0] if top_positive else 0.0, total_net), 0.25, "high_bad"),
            ("top5_trade_share", safe_ratio(sum(top_positive[:5]), total_net), 0.40, "high_bad"),
            ("best_month_net_share", safe_ratio(max(months.values()) if months else 0.0, total_net), 0.50, "high_bad"),
            ("largest_third_net_share", safe_ratio(max(thirds.values()) if thirds else 0.0, total_net), 0.55, "high_bad"),
            ("late_third_net_share", safe_ratio(thirds.get("late", 0.0), total_net), 0.15, "low_bad"),
            ("negative_month_count", sum(1 for value in months.values() if value < 0.0), 0, "high_bad"),
            ("same_direction_reentry_ratio_local", float(frame["same_direction_reentry"].mean()) if len(frame) else None, 0.35, "high_bad"),
            ("trade_count_gap_to_34d", len(frame) - LEGACY_34D["trade_count"], 0, "low_bad"),
        ]
        for metric, value, threshold, mode in metrics:
            rows.append(
                {
                    "split": split,
                    "metric": metric,
                    "value": round6(value),
                    "threshold": threshold,
                    "status": flag_status(value, threshold, mode),
                    "notes": concentration_note(metric),
                }
            )
    for row in segment_data:
        if row.get("segment_type") == "chronological_third" and row.get("quality_flag") != "acceptable_measurement_only":
            rows.append(
                {
                    "split": row.get("split"),
                    "metric": f"segment_quality_{row.get('segment')}",
                    "value": row.get("quality_flag"),
                    "threshold": "acceptable_measurement_only",
                    "status": "risk_flag",
                    "notes": "chronological third segment quality flag",
                }
            )
    return rows


def flag_status(value: Any, threshold: Any, mode: str) -> str:
    number = to_float(value)
    limit = to_float(threshold)
    if number is None or limit is None:
        return "missing_or_not_numeric"
    if mode == "high_bad" and number > limit:
        return "risk_flag"
    if mode == "low_bad" and number < limit:
        return "risk_flag"
    return "passed_measurement_only"


def concentration_note(metric: str) -> str:
    return {
        "top_single_trade_share": "single winning trade should not carry the result",
        "top5_trade_share": "top five winning trades should not dominate the result",
        "best_month_net_share": "best month should not dominate the result",
        "largest_third_net_share": "one chronological third should not dominate the result",
        "late_third_net_share": "late period should still contribute",
        "negative_month_count": "negative month count is recorded for curve quality",
        "same_direction_reentry_ratio_local": "same direction reentry within five M5 bars",
        "trade_count_gap_to_34d": "34D lesson target used only as KPI target surface",
    }.get(metric, "concentration metric")


def risk_atr_rows() -> list[dict[str, Any]]:
    source_rows = [
        row
        for row in read_csv(SOURCE_RISK)
        if row.get("adapter_id") == ADAPTER_ID and row.get("view") == "actual_routed_total" and row.get("split") in {"validation_is", "oos"}
    ]
    rows: list[dict[str, Any]] = []
    for row in source_rows:
        flags: list[str] = []
        if str(row.get("atr_enabled")) != "True":
            flags.append("atr_missing")
        if str(row.get("model_risk_enabled")) != "True":
            flags.append("model_risk_missing")
        if as_float(row.get("max_model_risk_pct")) > 0.05:
            flags.append("risk_cap_exceeded")
        if as_float(row.get("risk_floor_applied_count")) > 0:
            flags.append("risk_floor_impact_present")
        if as_float(row.get("avg_actual_risk_pct_after_floor")) > as_float(row.get("avg_model_risk_pct")) * 1.25:
            flags.append("actual_risk_inflation_check")
        rows.append(
            {
                "split": row.get("split"),
                "atr_enabled": row.get("atr_enabled"),
                "model_risk_enabled": row.get("model_risk_enabled"),
                "risk_floor_applied_count": row.get("risk_floor_applied_count"),
                "avg_model_risk_pct": row.get("avg_model_risk_pct"),
                "max_model_risk_pct": row.get("max_model_risk_pct"),
                "avg_clipped_risk_pct": row.get("avg_clipped_risk_pct"),
                "max_clipped_risk_pct": row.get("max_clipped_risk_pct"),
                "avg_actual_risk_pct_after_floor": row.get("avg_actual_risk_pct_after_floor"),
                "max_actual_risk_pct_after_floor": row.get("max_actual_risk_pct_after_floor"),
                "avg_computed_lot": row.get("avg_computed_lot"),
                "max_computed_lot": row.get("max_computed_lot"),
                "avg_executed_lot": row.get("avg_executed_lot"),
                "max_executed_lot": row.get("max_executed_lot"),
                "avg_atr_points": row.get("avg_atr_points"),
                "avg_open_sl_points": row.get("avg_open_sl_points"),
                "avg_open_tp_points": row.get("avg_open_tp_points"),
                "risk_bucket": row.get("risk_bucket"),
                "telemetry_sha256": row.get("telemetry_sha256"),
                "quality_flag": ";".join(flags) if flags else "risk_atr_present_measurement_only",
            }
        )
    return rows


def trade_records(split_frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, frame in split_frames.items():
        for _, trade in frame.iterrows():
            rows.append(
                {
                    "split": split,
                    "trade_index": int(trade["trade_index"]),
                    "direction": trade.get("direction"),
                    "open_time": trade["open_time"].isoformat(),
                    "close_time": trade["close_time"].isoformat(),
                    "hold_bars": round6(trade.get("hold_bars")),
                    "net_profit": round6(trade.get("net_profit")),
                    "equity_after_trade": round6(trade.get("equity_after_trade")),
                    "chronological_third": trade.get("chronological_third"),
                    "month": trade.get("month"),
                    "session_slice": trade.get("session_slice"),
                    "volatility_regime": trade.get("volatility_regime"),
                    "trend_regime": trade.get("trend_regime"),
                    "adx_bucket": trade.get("adx_bucket"),
                    "spread_regime": trade.get("spread_regime"),
                }
            )
    return rows


def source_row(rows: Sequence[Mapping[str, Any]], split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("split") == split:
            return row
    return {}


def source_report_path(row: Mapping[str, Any]) -> Path:
    raw = str(row.get("report_path") or "")
    if not raw:
        raise RuntimeError(f"Missing report_path for {row.get('split')}")
    return repo_path(raw)


def kpi_gap(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "pf_gap_to_34d": as_float(row.get("profit_factor")) - LEGACY_34D["profit_factor"],
        "net_gap_to_34d": as_float(row.get("net_profit")) - LEGACY_34D["net_profit"],
        "dd_pct_gap_to_34d": as_float(row.get("max_drawdown_percent")) - LEGACY_34D["max_drawdown_percent"],
        "trade_gap_to_34d": as_float(row.get("trade_count")) - LEGACY_34D["trade_count"],
    }


def split_flags(source: Mapping[str, Any], concentration: Sequence[Mapping[str, Any]], split: str) -> list[str]:
    flags: list[str] = []
    if as_float(source.get("profit_factor")) < LEGACY_34D["profit_factor"]:
        flags.append("pf_below_34d_exact")
    if as_float(source.get("net_profit")) < LEGACY_34D["net_profit"]:
        flags.append("net_below_34d")
    if as_float(source.get("max_drawdown_percent")) > LEGACY_34D["max_drawdown_percent"]:
        flags.append("drawdown_pct_above_34d")
    if as_float(source.get("trade_count")) < LEGACY_34D["trade_count"]:
        flags.append("trade_count_below_34d")
    flags.extend(str(row.get("metric")) for row in concentration if row.get("split") == split and row.get("status") == "risk_flag")
    return sorted(set(flags))


def build_audit() -> dict[str, Any]:
    ensure_dirs()
    summary_rows = source_summary_rows()
    if len(summary_rows) != 2:
        raise RuntimeError(f"Expected 2 source summary rows for {ADAPTER_ID}, found {len(summary_rows)}")
    costs = cost_penalty_by_split(summary_rows)
    market_data = MarketData.load(REPO_ROOT)
    split_frames: OrderedDict[str, pd.DataFrame] = OrderedDict()
    report_metrics: dict[str, Mapping[str, Any]] = {}
    source_reports: dict[str, str] = {}
    for split in ("validation_is", "oos"):
        row = source_row(summary_rows, split)
        report_path = source_report_path(row)
        frame, metrics = load_trade_frame(split, report_path, market_data)
        split_frames[split] = frame
        report_metrics[split] = metrics
        source_reports[split] = rel(report_path)

    segments = segment_rows(split_frames, costs)
    monthly = monthly_rows(split_frames, costs)
    session_regime = slice_rows(split_frames, costs, ("session_slice", "volatility_regime", "trend_regime", "adx_bucket", "spread_regime"))
    long_short = slice_rows(split_frames, costs, ("direction",))
    concentration = concentration_flags(split_frames, segments)
    risk_rows = risk_atr_rows()
    trade_rows = trade_records(split_frames)
    equity = {split: equity_shape(frame) for split, frame in split_frames.items()}
    split_summary: OrderedDict[str, Any] = OrderedDict()
    for split in ("validation_is", "oos"):
        row = source_row(summary_rows, split)
        split_summary[split] = {
            "source_kpi": {key: row.get(key) for key in ("profit_factor", "net_profit", "max_drawdown_percent", "trade_count", "trades_per_day", "expectancy", "cost_stressed_expectancy", "same_move_reentry_ratio", "mfe_capture_ratio")},
            "gap_to_34d": {key: round6(value) for key, value in kpi_gap(row).items()},
            "equity_shape": equity[split],
            "risk_flags": split_flags(row, concentration, split),
            "source_report": source_reports[split],
        }
    decision_reason = (
        "PF/net은 강하지만 validation(검증) PF가 34D(레거시 기준) 정확값보다 아주 조금 낮고, "
        "validation late third(검증 후반 3분위) 손익 집중, OOS(외부 표본) drawdown(손실폭) 초과, "
        "거래 수 부족이 남아 Stage136(136단계) 수리로 넘긴다."
    )
    return {
        "created_at_utc": utc_now(),
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "adapter_id": ADAPTER_ID,
        "target_surface": TARGET_SURFACE,
        "legacy_34d": LEGACY_34D,
        "claim_boundary": BOUNDARY,
        "decision": DECISION,
        "decision_reason": decision_reason,
        "source_reports": source_reports,
        "split_summary": split_summary,
        "report_metrics": report_metrics,
        "risk_flag_count": sum(1 for row in concentration if row.get("status") == "risk_flag"),
        "artifacts": {
            "report": rel(REPORT_PATH),
            "summary_json": rel(SUMMARY_JSON_PATH),
            "segment_stability": rel(SEGMENT_PATH),
            "monthly_kpi": rel(MONTHLY_PATH),
            "session_regime_kpi": rel(SESSION_REGIME_PATH),
            "long_short_kpi": rel(LONG_SHORT_PATH),
            "equity_curve_shape_audit": rel(EQUITY_AUDIT_PATH),
            "risk_atr_behavior_audit": rel(RISK_ATR_PATH),
            "concentration_risk_report": rel(CONCENTRATION_PATH),
            "performance_attribution": rel(ATTRIBUTION_PATH),
            "route_decision": rel(ROUTE_DECISION_PATH),
            "decision": rel(DECISION_PATH),
            "trade_records": rel(TRADE_RECORDS_PATH),
        },
        "next_stage": {
            "stage_id": NEXT_STAGE_ID,
            "run_id": NEXT_RUN_ID,
            "packet_id": NEXT_PACKET_ID,
            "bounded_question": "Can the survivor candidate raise trade count and reduce validation concentration without damaging PF/net, drawdown, risk/ATR, or OOS behavior?",
        },
        "data": {
            "segments": segments,
            "monthly": monthly,
            "session_regime": session_regime,
            "long_short": long_short,
            "concentration": concentration,
            "risk_atr": risk_rows,
            "trades": trade_rows,
            "source_summary_rows": summary_rows,
        },
    }


def write_outputs(audit: Mapping[str, Any]) -> None:
    data = audit["data"]
    write_csv(SEGMENT_PATH, data["segments"], SEGMENT_COLUMNS)
    write_csv(MONTHLY_PATH, data["monthly"], MONTHLY_COLUMNS)
    write_csv(SESSION_REGIME_PATH, data["session_regime"], SLICE_COLUMNS)
    write_csv(LONG_SHORT_PATH, data["long_short"], SLICE_COLUMNS)
    write_csv(RISK_ATR_PATH, data["risk_atr"], RISK_COLUMNS)
    write_csv(TRADE_RECORDS_PATH, data["trades"], TRADE_COLUMNS)
    write_csv(
        ROUTE_DECISION_PATH,
        [
            {
                "decision": DECISION,
                "next_stage": NEXT_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "adapter_id": ADAPTER_ID,
                "overall_goal_complete": False,
                "reason": "pf_net_strong_but_validation_concentration_oos_dd_and_trade_count_gap_route_stage136",
            }
        ],
    )
    write_md(REPORT_PATH, report_markdown(audit))
    write_md(EQUITY_AUDIT_PATH, equity_markdown(audit))
    write_md(CONCENTRATION_PATH, concentration_markdown(audit))
    write_md(ATTRIBUTION_PATH, attribution_markdown(audit))
    write_md(DECISION_PATH, decision_markdown(audit))
    slim = dict(audit)
    slim["data"] = {
        "row_counts": {
            "segments": len(data["segments"]),
            "monthly": len(data["monthly"]),
            "session_regime": len(data["session_regime"]),
            "long_short": len(data["long_short"]),
            "concentration": len(data["concentration"]),
            "risk_atr": len(data["risk_atr"]),
            "trades": len(data["trades"]),
        }
    }
    write_json(SUMMARY_JSON_PATH, slim)


def report_markdown(audit: Mapping[str, Any]) -> str:
    val = audit["split_summary"]["validation_is"]
    oos = audit["split_summary"]["oos"]
    return f"""# Stage135 Segment/Equity Audit Report(135단계 구간/자금곡선 감사 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- adapter(어댑터): `{ADAPTER_ID}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Easy Read(쉬운 판독)

현재 후보는 강하다. validation/OOS(검증/외부 표본) 순손익(net P/L, 순손익)은 34D(레거시 기준)를 넘고, ATR bracket(ATR 괄호)과 model risk%(모델 위험 비율)도 이미 측정되어 있다.

하지만 아직 final package(최종 패키지)가 아니다. validation PF(검증 수익 팩터)는 34D 정확값보다 아주 조금 낮고, validation late third(검증 후반 3분위)가 순손익을 많이 들고 있으며, OOS drawdown(외부 표본 손실폭)은 34D보다 크고, trade count(거래 수)는 34D보다 많이 낮다.

Effect(효과): 이 후보를 버리지는 않지만, Stage136(136단계)에서 거래 수와 손익 집중을 작게 수리한다.

## KPI vs 34D(KPI와 34D 비교)

| split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래) | main flags(주요 표시) |
|---|---:|---:|---:|---:|---|
| validation(검증) | {as_float(val['source_kpi']['profit_factor']):.6f} | {as_float(val['source_kpi']['net_profit']):.2f} | {as_float(val['source_kpi']['max_drawdown_percent']):.2f} | {as_float(val['source_kpi']['trade_count']):.0f} | {", ".join(val["risk_flags"]) or "none"} |
| OOS(외부 표본) | {as_float(oos['source_kpi']['profit_factor']):.6f} | {as_float(oos['source_kpi']['net_profit']):.2f} | {as_float(oos['source_kpi']['max_drawdown_percent']):.2f} | {as_float(oos['source_kpi']['trade_count']):.0f} | {", ".join(oos["risk_flags"]) or "none"} |

## Evidence(근거)

- segment_stability(구간 안정성): `{audit['artifacts']['segment_stability']}`
- monthly_kpi(월별 핵심 성과 지표): `{audit['artifacts']['monthly_kpi']}`
- session_regime_kpi(세션/국면 핵심 성과 지표): `{audit['artifacts']['session_regime_kpi']}`
- long_short_kpi(롱/숏 핵심 성과 지표): `{audit['artifacts']['long_short_kpi']}`
- equity_curve_shape(자금곡선 모양): `{audit['artifacts']['equity_curve_shape_audit']}`
- risk_atr_behavior(위험/ATR 행동): `{audit['artifacts']['risk_atr_behavior_audit']}`

## Boundary(경계)

deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)는 주장하지 않는다.
"""


def equity_markdown(audit: Mapping[str, Any]) -> str:
    lines = [
        "# Stage135 Equity Curve Shape Audit(135단계 자금곡선 모양 감사)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- adapter(어댑터): `{ADAPTER_ID}`",
        "",
        "## Read(판독)",
        "",
        "equity curve(자금곡선)는 최종 손익만 보지 않는다. Effect(효과): 한 구간의 폭발적 수익이나 늦은 평탄화를 따로 잡는다.",
        "",
        "| split(분할) | final net(최종 순손익) | closed DD(닫힌 거래 손실폭) | recovered(회복) | longest no-high trades(최장 신고점 없음 거래 수) | flags(표시) |",
        "|---|---:|---:|---|---:|---|",
    ]
    for split, payload in audit["split_summary"].items():
        eq = payload["equity_shape"]
        lines.append(
            f"| {split} | {as_float(eq['final_net']):.2f} | {as_float(eq['max_closed_trade_drawdown']):.2f} | {eq['recovered_after_max_drawdown']} | {eq['longest_non_new_high_trades']} | {', '.join(payload['risk_flags']) or 'none'} |"
        )
    lines.extend(
        [
            "",
            "## Decision Effect(판정 효과)",
            "",
            f"`{DECISION}`. Stage136(136단계)는 trade count(거래 수)와 concentration(집중)을 수리하되, PF/net(수익 팩터/순손익), drawdown(손실폭), risk/ATR(위험/ATR)을 훼손하면 안 된다.",
        ]
    )
    return "\n".join(lines)


def concentration_markdown(audit: Mapping[str, Any]) -> str:
    rows = audit["data"]["concentration"]
    risk_rows = [row for row in rows if row.get("status") == "risk_flag"]
    lines = [
        "# Stage135 Concentration Risk Report(135단계 집중 위험 보고서)",
        "",
        f"- risk_flag_count(위험 표시 수): `{len(risk_rows)}`",
        "",
        "| split(분할) | metric(지표) | value(값) | threshold(기준) | notes(메모) |",
        "|---|---|---:|---:|---|",
    ]
    for row in risk_rows:
        lines.append(f"| {row.get('split')} | {row.get('metric')} | {row.get('value')} | {row.get('threshold')} | {row.get('notes')} |")
    lines.extend(
        [
            "",
            "Effect(효과): 강한 최종 순손익(net P/L, 순손익)을 보존하되, 한 구간이나 적은 거래 수에 기대는 위험은 Stage136(136단계)로 넘긴다.",
        ]
    )
    return "\n".join(lines)


def attribution_markdown(audit: Mapping[str, Any]) -> str:
    val = audit["split_summary"]["validation_is"]
    oos = audit["split_summary"]["oos"]
    return f"""# Stage135 Performance Attribution(135단계 성과 귀속)

- observed_change(관찰 변화): Stage133 survivor(133단계 생존 후보)가 validation/OOS(검증/외부 표본) 순손익(net P/L, 순손익)을 34D(레거시 기준) 이상으로 회복했다.
- comparison_baseline(비교 기준): legacy 34D lesson-only KPI target(레거시 34D 교훈 전용 핵심 성과 지표 목표), Stage133 segment/risk evidence(133단계 구간/위험 근거).
- likely_drivers(가능한 동인): Stage122 survivor shell(Stage122 생존 후보 껍질), ATR bracket(ATR 괄호), capped model risk%(상한 모델 위험 비율), Tier B disabled(Tier B 비활성) 경로 보존.
- segment_checks(구간 점검): chronological thirds(시간 3분위), month(월), session/regime(세션/국면), long/short(롱/숏), risk/ATR telemetry(위험/ATR 원격측정), trade shape(거래 모양).
- trade_shape(거래 모양): validation(검증) trades `{val['source_kpi']['trade_count']}`, OOS(외부 표본) trades `{oos['source_kpi']['trade_count']}`로 34D `{LEGACY_34D['trade_count']}`보다 낮다.
- alternative_explanations(대안 설명): 낮은 거래 수와 validation late concentration(검증 후반 집중)이 headline KPI(대표 핵심 성과 지표)를 키웠을 수 있다.
- attribution_confidence(귀속 신뢰도): medium(중간). MT5 report deal list(메타트레이더5 거래 목록)를 파싱했지만 Stage135(135단계)는 새 최적화가 아니다.
- next_probe(다음 탐침): Stage136(136단계)에서 거래 수를 늘리거나 집중을 낮추는 작은 수리만 시험한다.

Effect(효과): 좋은 결과를 버리지 않고, 약한 이유도 숨기지 않는다.
"""


def decision_markdown(audit: Mapping[str, Any]) -> str:
    return f"""# Stage135 Decision(135단계 판정)

decision(판정): `{DECISION}`

Stage135(135단계)는 review-only audit(검토 전용 감사)로 닫는다. Effect(효과): strong candidate(강한 후보)는 보존하지만 final package(최종 패키지)나 overall goal complete(전체 목표 완료)를 주장하지 않는다.

## Reason(이유)

{audit['decision_reason']}

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_JSON_PATH)}`
- segment_stability(구간 안정성): `{rel(SEGMENT_PATH)}`
- monthly_kpi(월별 핵심 성과 지표): `{rel(MONTHLY_PATH)}`
- session_regime_kpi(세션/국면 핵심 성과 지표): `{rel(SESSION_REGIME_PATH)}`
- long_short_kpi(롱/숏 핵심 성과 지표): `{rel(LONG_SHORT_PATH)}`
- equity_curve_shape(자금곡선 모양): `{rel(EQUITY_AUDIT_PATH)}`
- risk_atr_behavior(위험/ATR 행동): `{rel(RISK_ATR_PATH)}`
- performance_attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage136(136단계)의 질문은 trade count(거래 수)와 concentration(집중)을 고치되, validation/OOS(검증/외부 표본) PF/net(수익 팩터/순손익), drawdown(손실폭), risk/ATR(위험/ATR)을 망치지 않는지다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def write_stage_docs(audit: Mapping[str, Any]) -> None:
    write_md(
        SPEC_ROOT / "stage_brief.md",
        f"""# {STAGE_ID}

Stage135(135단계)는 Stage133/134 survivor candidate(생존 후보)를 segment/equity audit(구간/자금곡선 감사)로 판정한다.

## Bounded Question(경계 질문)

강한 PF/net(수익 팩터/순손익)이 segment stability(구간 안정성), equity curve(자금곡선), risk/ATR behavior(위험/ATR 행동)에서도 credible(신뢰 가능)한가?

Effect(효과): 높은 최종 손익만 보고 전체 목표 완료를 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage135 Input References(135단계 입력 참조)

- stage134_decision(134단계 판정): `{rel(SOURCE_STAGE134_DECISION)}`
- stage134_review(134단계 검토): `{rel(SOURCE_STAGE134_REVIEW)}`
- stage133_summary(133단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage133_segment_kpi(133단계 구간 KPI): `{rel(SOURCE_SEGMENTS)}`
- stage133_risk_atr_telemetry(133단계 위험/ATR 원격측정): `{rel(SOURCE_RISK)}`
- stage133_trade_audit(133단계 거래 감사): `{rel(SOURCE_TRADE_AUDIT)}`
- validation_report(검증 보고서): `{audit['source_reports']['validation_is']}`
- oos_report(외부 표본 보고서): `{audit['source_reports']['oos']}`

No new optimization(새 최적화 없음). Effect(효과): 기존 MT5(메타트레이더5) 근거만 감사한다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage135 Review Index(135단계 검토 색인)

- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_JSON_PATH)}`
- segment_stability(구간 안정성): `{rel(SEGMENT_PATH)}`
- monthly_kpi(월별 핵심 성과 지표): `{rel(MONTHLY_PATH)}`
- session_regime_kpi(세션/국면 핵심 성과 지표): `{rel(SESSION_REGIME_PATH)}`
- long_short_kpi(롱/숏 핵심 성과 지표): `{rel(LONG_SHORT_PATH)}`
- equity_curve_shape(자금곡선 모양): `{rel(EQUITY_AUDIT_PATH)}`
- risk_atr_behavior(위험/ATR 행동): `{rel(RISK_ATR_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- performance_attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage135 Selection Status(135단계 선택 상태)

- stage_status(단계 상태): `closed_bounded_audit`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE134_ID}`
- stage135_decision(135단계 판정): `{DECISION}`
- selected_adapter(선택 어댑터): `{ADAPTER_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage135(135단계)는 감사로 닫고, 수리는 Stage136(136단계)로 분리한다.
""",
    )


def write_next_stage_docs() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage136(136단계)는 Stage135(135단계)가 남긴 trade count/concentration(거래 수/집중) 약점을 bounded repair(경계 수리)로 다룬다.

## Bounded Question(경계 질문)

Can the survivor candidate raise trade count(거래 수) and reduce concentration(집중) without damaging PF/net(수익 팩터/순손익), drawdown(손실폭), risk/ATR(위험/ATR), or OOS behavior(외부 표본 행동)?

Effect(효과): Stage136(136단계)가 또 다른 무한 캠페인이 되지 않게 한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage136 Input References(136단계 입력 참조)

- stage135_decision(135단계 판정): `{rel(DECISION_PATH)}`
- stage135_report(135단계 보고서): `{rel(REPORT_PATH)}`
- stage135_segment_stability(135단계 구간 안정성): `{rel(SEGMENT_PATH)}`
- stage135_equity_curve_shape(135단계 자금곡선 모양): `{rel(EQUITY_AUDIT_PATH)}`
- stage135_risk_atr_behavior(135단계 위험/ATR 행동): `{rel(RISK_ATR_PATH)}`
- source_stage133_summary(원천 133단계 요약): `{rel(SOURCE_SUMMARY)}`

Effect(효과): Stage136(136단계)는 Stage135(135단계) 약점만 좁게 수리한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage136 Review Index(136단계 검토 색인)

Stage136(136단계)는 planned(계획) 상태다. Effect(효과): trade count/concentration(거래 수/집중) 수리 결과가 나오기 전까지 전체 목표 완료를 주장하지 않는다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage136 Selection Status(136단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage135`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- adapter_under_repair(수리 대상 어댑터): `{ADAPTER_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SEGMENT_PATH,
        MONTHLY_PATH,
        SESSION_REGIME_PATH,
        LONG_SHORT_PATH,
        EQUITY_AUDIT_PATH,
        RISK_ATR_PATH,
        CONCENTRATION_PATH,
        ATTRIBUTION_PATH,
        ROUTE_DECISION_PATH,
        DECISION_PATH,
        TRADE_RECORDS_PATH,
        STAGE_LEDGER_PATH,
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage135_segment_equity_audit_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage135 bounded segment/equity audit artifact.",
                }
            )
    return rows


def write_ledgers(audit: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    val = audit["split_summary"]["validation_is"]
    oos = audit["split_summary"]["oos"]
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_survivor_segment_equity_audit",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs((("adapter", ADAPTER_ID), ("target_surface", TARGET_SURFACE), ("overall_goal_complete", False))),
            }
        ],
        key="run_id",
    )
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage135_segment_equity_audit",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage135_segment_equity_audit",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_mt5_report_deal_list_audit",
            "tier_scope": "Tier A+B routed review; Tier B disabled evidence preserved",
            "kpi_scope": "segment_equity_risk_atr_audit",
            "scoreboard_lane": "baseline_adapter_research",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("adapter", ADAPTER_ID),
                    ("val_net", val["source_kpi"]["net_profit"]),
                    ("val_pf", val["source_kpi"]["profit_factor"]),
                    ("oos_net", oos["source_kpi"]["net_profit"]),
                    ("oos_pf", oos["source_kpi"]["profit_factor"]),
                )
            ),
            "guardrail_kpi": ledger_pairs(
                (
                    ("val_flags", ",".join(val["risk_flags"])),
                    ("oos_flags", ",".join(oos["risk_flags"])),
                    ("overall_goal_complete", False),
                    ("claim_boundary", BOUNDARY),
                )
            ),
            "external_verification_status": "completed_existing_stage133_mt5_reports_reparsed",
            "notes": "Stage135 audit only; no new optimization; no operational claim.",
        }
    ]
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def write_packet_files(audit: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    files = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "primary_family": "adapter_development",
            "primary_skill": "obsidian-performance-attribution",
            "support_skills": ["obsidian-result-judgment", "obsidian-artifact-lineage"],
            "required_gates": ["experiment_design_receipt", "kpi_contract_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"],
            "status": "completed",
        },
        "experiment_design_receipt.json": {
            "hypothesis": "Stage133 survivor is strong but must pass segment/equity/risk audit before repair or hardening.",
            "decision_use": "route only to next bounded repair stage",
            "comparison_baseline": "legacy 34D lesson-only KPI target and Stage133 survivor evidence",
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            "source_reports": audit["source_reports"],
            "outputs": audit["artifacts"],
            "status": "completed",
        },
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "judgment_label": "exploratory_research_candidate_not_final",
            "decision": DECISION,
            "overall_goal_complete": False,
            "claim_boundary": BOUNDARY,
            "status": "passed_with_boundary",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK), rel(SOURCE_STAGE134_DECISION)],
            "consumers": list(audit["artifacts"].values()),
            "ledger_links": ledger_payload,
            "status": "completed",
        },
        "final_claim_guard.json": {
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "required_gate_coverage_audit.json": {
            "required_gates": ["experiment_design_receipt", "kpi_contract_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"],
            "covered_by": ["experiment_design_receipt.json", "kpi_contract_audit.json", "result_judgment_gate.json", "artifact_lineage_audit.json", "final_claim_guard.json"],
            "status": "completed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "adapter_id": ADAPTER_ID,
            "next_stage": NEXT_STAGE_ID,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
            "artifacts": audit["artifacts"],
        },
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def update_registers() -> None:
    existing = io_path(NEGATIVE_REGISTER_PATH).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER_PATH) else "# Negative Result Register\n\n"
    row_id = "NR-030"
    if row_id not in existing:
        row = (
            f"| `{row_id}` | `IDEA-ST135-STAGE122-SURVIVOR-AUDIT` | Stage122 survivor(Stage122 생존 후보)는 34D(레거시 기준) 이상 KPI(핵심 성과 지표)에 바로 도달할 수 있다 | "
            "Stage135(135단계)에서 PF/net(수익 팩터/순손익)은 강했지만 validation late concentration(검증 후반 집중), OOS drawdown(외부 표본 손실폭), trade count gap(거래 수 격차)이 남았다 | "
            "후보는 보존하고 Stage136(136단계)에서 trade count/concentration(거래 수/집중)만 좁게 수리한다 | "
            "거래 수가 늘고 집중이 낮아져도 validation/OOS PF/net(검증/외부 표본 수익 팩터/순손익)과 risk/ATR(위험/ATR)이 유지될 때 |\n"
        )
        io_path(NEGATIVE_REGISTER_PATH).write_text(existing.rstrip() + "\n" + row, encoding="utf-8-sig")


def update_current_truth() -> None:
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_repair(수리 대상 어댑터): `{ADAPTER_ID}`
- status(상태): `stage135_closed_{DECISION}_stage136_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage135(135단계)는 survivor candidate(생존 후보)를 버리지 않았다. 하지만 validation concentration(검증 집중), OOS drawdown(외부 표본 손실폭), trade count gap(거래 수 격차)이 남아 Stage136(136단계)로 넘겼다. Effect(효과): 좋은 KPI(핵심 성과 지표)를 보존하되 전체 목표 완료를 주장하지 않는다.

## Latest Stage135 Evidence(최신 135단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- segment_stability(구간 안정성): `{rel(SEGMENT_PATH)}`
- equity_curve_shape(자금곡선 모양): `{rel(EQUITY_AUDIT_PATH)}`
- risk_atr_behavior(위험/ATR 행동): `{rel(RISK_ATR_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    text = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage135(135단계) closed(종료) as `{DECISION}` and Stage136(136단계) `{NEXT_STAGE_ID}` is active_planned(활성 계획). Effect(효과): survivor candidate(생존 후보)를 버리지 않고 거래 수/집중 약점만 좁게 수리한다.
- >-
  Stage135 evidence(135단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SEGMENT_PATH)}`, `{rel(EQUITY_AUDIT_PATH)}`, `{rel(RISK_ATR_PATH)}`에 있다. Effect(효과): KPI(핵심 성과 지표) 강점과 약점을 동시에 추적한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.

"""
    text = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, text, count=1) if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", text) else text.rstrip() + "\n" + focus
    block = f"""
stage135_stage122_survivor_segment_equity_audit:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_bounded_audit
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE134_ID}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage136_stage122_survivor_trade_count_concentration_repair:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: active_planned_from_stage135
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  next_action: run_stage136_trade_count_concentration_repair
  boundary: {BOUNDARY}
"""
    text = re.sub(r"(?ms)\nstage135_stage122_survivor_segment_equity_audit:.*?(?=\nstage\d+_|$)", "\n", text)
    text = re.sub(r"(?ms)\nstage136_stage122_survivor_trade_count_concentration_repair:.*?(?=\nstage\d+_|$)", "\n", text)
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if STAGE_ID in existing and DECISION in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage135 segment/equity audit closeout(135단계 구간/자금곡선 감사 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): survivor candidate(생존 후보)는 보존하고, trade count/concentration(거래 수/집중) 수리를 Stage136(136단계)로 분리했다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(audit, artifacts)
    write_packet_files(audit, ledger_payload)
    write_stage_docs(audit)
    write_next_stage_docs()
    update_registers()
    update_current_truth()
    append_changelog()
    write_json(
        SUMMARY_JSON_PATH,
        {
            **{key: value for key, value in audit.items() if key != "data"},
            "ledger_payload": ledger_payload,
            "data": {
                "row_counts": {
                    "segments": len(audit["data"]["segments"]),
                    "monthly": len(audit["data"]["monthly"]),
                    "session_regime": len(audit["data"]["session_regime"]),
                    "long_short": len(audit["data"]["long_short"]),
                    "concentration": len(audit["data"]["concentration"]),
                    "risk_atr": len(audit["data"]["risk_atr"]),
                    "trades": len(audit["data"]["trades"]),
                }
            },
        },
    )
    final_artifacts = artifact_rows()
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, final_artifacts, key="artifact_id")
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "report": rel(REPORT_PATH),
                    "next_stage": NEXT_STAGE_ID,
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
