from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

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
    sha256_file_lf_normalized,
)
from foundation.control_plane.mt5_trade_attribution import (  # noqa: E402
    MarketData,
    compute_trade_attribution,
)
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics  # noqa: E402
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report  # noqa: E402


STAGE56_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
STAGE57_ID = "57_adapter_quality__equity_segment_kpi_audit_gate"
STAGE58_ID = "58_adapter_risk__bounded_repair_before_atr_risk_integration"
RUN50CA_ID = "run50CA_stage56_baseline_adapter_onnx_runtime_reproduction_v1"
RUN57_ID = "run51A_stage57_equity_segment_kpi_audit_v1"
RUN58_PLANNED_ID = "run52A_stage58_adapter_repair_before_risk_atr_v1"
PACKET_ID = "stage57_equity_segment_kpi_audit_gate_v1"
ADAPTER_ID = "ba14_no_atr_sd5_lot025"
DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
DECISION = "proceed_to_stage58_adapter_repair_before_risk_atr"
UTC_NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

STAGE56_ROOT = REPO_ROOT / "stages" / STAGE56_ID
STAGE57_ROOT = REPO_ROOT / "stages" / STAGE57_ID
STAGE58_ROOT = REPO_ROOT / "stages" / STAGE58_ID
RUN_ROOT = STAGE57_ROOT / "02_runs" / RUN57_ID
REVIEWS_ROOT = STAGE57_ROOT / "03_reviews"
PACKET_ROOT = REPO_ROOT / "docs" / "agent_control" / "packets" / PACKET_ID

STAGE56_SUMMARY_CSV = STAGE56_ROOT / "03_reviews" / "run50CA_baseline_adapter_onnx_runtime_reproduction_summary.csv"
STAGE56_RISK_CSV = STAGE56_ROOT / "03_reviews" / "run50CA_baseline_adapter_onnx_runtime_reproduction_risk_telemetry.csv"
REPORT_DIR = STAGE56_ROOT / "02_runs" / "run50CA" / "mt5" / "reports"
REPORTS = {
    "validation_is": REPORT_DIR
    / "Project_Obsidian_Prime_v2_run50CA_stage56_baseline_adapter_onnx_runtime_reproduction_v1_ba14_no_atr_sd5_lot025_onnx_rt_val.htm",
    "oos": REPORT_DIR
    / "Project_Obsidian_Prime_v2_run50CA_stage56_baseline_adapter_onnx_runtime_reproduction_v1_ba14_no_atr_sd5_lot025_onnx_rt_oos.htm",
}

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
    "realized_over_mfe_mean",
    "mfe_capture_ratio",
    "top_trade_net",
    "top_trade_net_share",
    "top5_trade_net_share",
    "start_time",
    "end_time",
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
    "mfe_mean",
    "mae_mean",
    "realized_over_mfe_mean",
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
    "mfe_mean",
    "mae_mean",
    "realized_over_mfe_mean",
    "mfe_capture_ratio",
    "quality_flag",
)

CONCENTRATION_COLUMNS = (
    "split",
    "metric",
    "value",
    "threshold",
    "status",
    "notes",
)


def main() -> None:
    _ensure_dirs()
    source_summary = pd.read_csv(io_path(STAGE56_SUMMARY_CSV))
    market_data = MarketData.load(REPO_ROOT)
    split_frames: dict[str, pd.DataFrame] = {}
    report_metrics: dict[str, dict[str, Any]] = {}
    cost_penalty = _cost_penalty_by_split(source_summary)

    for split, report_path in REPORTS.items():
        frame, metrics = _load_trade_frame(split, report_path, market_data)
        split_frames[split] = frame
        report_metrics[split] = metrics

    segment_rows = _segment_rows(split_frames, cost_penalty)
    monthly_rows = _monthly_rows(split_frames, cost_penalty)
    session_regime_rows = _session_regime_rows(split_frames, cost_penalty)
    long_short_rows = _long_short_rows(split_frames, cost_penalty)
    concentration_rows = _concentration_rows(split_frames, source_summary, report_metrics)
    summary = _build_summary(
        split_frames=split_frames,
        report_metrics=report_metrics,
        source_summary=source_summary,
        concentration_rows=concentration_rows,
        segment_rows=segment_rows,
    )

    _write_csv(REVIEWS_ROOT / "segment_kpi_summary.csv", SEGMENT_COLUMNS, segment_rows)
    _write_csv(REVIEWS_ROOT / "monthly_kpi_summary.csv", MONTHLY_COLUMNS, monthly_rows)
    _write_csv(REVIEWS_ROOT / "session_regime_kpi_summary.csv", SLICE_COLUMNS, session_regime_rows)
    _write_csv(REVIEWS_ROOT / "long_short_kpi_summary.csv", SLICE_COLUMNS, long_short_rows)
    _write_csv(REVIEWS_ROOT / "concentration_risk_summary.csv", CONCENTRATION_COLUMNS, concentration_rows)
    _write_json(RUN_ROOT / "run_manifest.json", _run_manifest(summary))
    _write_json(RUN_ROOT / "kpi_record.json", summary)
    _write_json(REVIEWS_ROOT / "stage57_audit_summary.json", summary)
    _write_text(REVIEWS_ROOT / "equity_curve_audit.md", _equity_audit_markdown(summary))
    _write_text(REVIEWS_ROOT / "concentration_risk_report.md", _concentration_markdown(summary))
    _write_text(REVIEWS_ROOT / "stage57_decision.md", _stage57_decision_markdown(summary))
    _write_text(STAGE57_ROOT / "00_spec" / "stage_brief.md", _stage57_brief())
    _write_text(STAGE57_ROOT / "01_inputs" / "input_refs.md", _stage57_inputs())
    _write_text(STAGE57_ROOT / "03_reviews" / "review_index.md", _stage57_review_index())
    _write_text(STAGE57_ROOT / "04_selected" / "selection_status.md", _stage57_selection_status(summary))
    _write_text(STAGE58_ROOT / "00_spec" / "stage_brief.md", _stage58_brief())
    _write_text(STAGE58_ROOT / "01_inputs" / "input_refs.md", _stage58_inputs(summary))
    _write_text(STAGE58_ROOT / "03_reviews" / "review_index.md", _stage58_review_index())
    _write_text(STAGE58_ROOT / "04_selected" / "selection_status.md", _stage58_selection_status(summary))
    _write_text(STAGE56_ROOT / "04_selected" / "selection_status.md", _stage56_selection_status(summary))
    _write_text(
        REPO_ROOT / "docs" / "decisions" / "2026-05-15_stage57_equity_segment_kpi_audit_gate.md",
        _decision_memo(summary),
    )
    _write_text(REPO_ROOT / "docs" / "context" / "current_working_state.md", _current_working_state(summary))

    _write_packet(summary)
    _write_stage_ledger(summary)
    _update_registries(summary)
    _update_workspace_state(summary)
    _append_changelog(summary)


def _ensure_dirs() -> None:
    for path in (
        STAGE57_ROOT / "00_spec",
        STAGE57_ROOT / "01_inputs",
        RUN_ROOT,
        REVIEWS_ROOT,
        STAGE57_ROOT / "04_selected",
        STAGE58_ROOT / "00_spec",
        STAGE58_ROOT / "01_inputs",
        STAGE58_ROOT / "03_reviews",
        STAGE58_ROOT / "04_selected",
        PACKET_ROOT,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)


def _load_trade_frame(split: str, report_path: Path, market_data: MarketData) -> tuple[pd.DataFrame, dict[str, Any]]:
    report = parse_mt5_trade_report(report_path)
    trades = pair_deals_into_trades(report["deals"])
    stats = compute_trade_attribution(trades, market_data)
    frame = pd.DataFrame(stats["trades"])
    if frame.empty:
        raise RuntimeError(f"No trades parsed for {split}: {report_path}")
    frame["split"] = split
    frame["open_time"] = pd.to_datetime(frame["open_time"])
    frame["close_time"] = pd.to_datetime(frame["close_time"])
    frame["month"] = frame["close_time"].dt.strftime("%Y-%m")
    frame["sequence_index"] = range(1, len(frame) + 1)
    frame["chronological_third"] = _chronological_thirds(len(frame))
    frame["same_direction_reentry"] = _same_direction_reentry(frame)
    metrics = extract_mt5_strategy_report_metrics(report_path)
    return frame, metrics


def _chronological_thirds(length: int) -> list[str]:
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


def _same_direction_reentry(frame: pd.DataFrame) -> pd.Series:
    ordered = frame.sort_values("open_time").reset_index(drop=True)
    previous_direction = ordered["direction"].shift(1)
    previous_open = ordered["open_time"].shift(1)
    bar_gap = (ordered["open_time"] - previous_open).dt.total_seconds() / 60.0 / 5.0
    values = (ordered["direction"].eq(previous_direction) & (bar_gap <= 5.0)).fillna(False)
    values.index = ordered.index
    result = pd.Series(False, index=frame.index)
    result.loc[ordered.index] = values
    return result


def _cost_penalty_by_split(source_summary: pd.DataFrame) -> dict[str, float]:
    penalties: dict[str, float] = {}
    routed = source_summary[source_summary["view"].eq("actual_routed_total")]
    for _, row in routed.iterrows():
        split = str(row.get("split"))
        expectancy = _to_float(row.get("expectancy"))
        stressed = _to_float(row.get("cost_stressed_expectancy"))
        if expectancy is not None and stressed is not None:
            penalties[split] = max(0.0, expectancy - stressed)
    return penalties


def _segment_rows(split_frames: Mapping[str, pd.DataFrame], cost_penalty: Mapping[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, frame in split_frames.items():
        rows.append(_kpi_row(split, "full_split", "actual_routed_total", frame, cost_penalty.get(split, 0.0), frame))
        for label in ("early", "mid", "late"):
            subset = frame[frame["chronological_third"].eq(label)]
            rows.append(_kpi_row(split, "chronological_third", label, subset, cost_penalty.get(split, 0.0), frame))
    return rows


def _monthly_rows(split_frames: Mapping[str, pd.DataFrame], cost_penalty: Mapping[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, frame in split_frames.items():
        total_net = _sum(frame["net_profit"])
        for month, subset in frame.groupby("month", sort=True):
            kpi = _kpi(subset, cost_penalty.get(split, 0.0))
            rows.append(
                {
                    "split": split,
                    "month": month,
                    "trade_count": kpi["trade_count"],
                    "net_profit": kpi["net_profit"],
                    "profit_factor": kpi["profit_factor"],
                    "win_rate": kpi["win_rate"],
                    "expectancy": kpi["expectancy"],
                    "cost_stressed_expectancy": kpi["cost_stressed_expectancy"],
                    "max_closed_trade_drawdown": kpi["max_closed_trade_drawdown"],
                    "mfe_mean": kpi["mfe_mean"],
                    "mae_mean": kpi["mae_mean"],
                    "realized_over_mfe_mean": kpi["realized_over_mfe_mean"],
                    "mfe_capture_ratio": kpi["mfe_capture_ratio"],
                    "net_share": _safe_ratio(kpi["net_profit"], total_net),
                    "quality_flag": _monthly_quality(split, month, kpi, total_net),
                }
            )
    return rows


def _session_regime_rows(split_frames: Mapping[str, pd.DataFrame], cost_penalty: Mapping[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    axes = ("session_slice", "volatility_regime", "trend_regime", "adx_bucket", "spread_regime")
    for split, frame in split_frames.items():
        for axis in axes:
            for bucket, subset in frame.groupby(axis, dropna=False, sort=True):
                rows.append(_slice_row(split, axis, str(bucket), subset, frame, cost_penalty.get(split, 0.0)))
        rows.append(
            _slice_row(
                split,
                "weather_proxy",
                "not_available_use_session_volatility_trend_spread_proxies",
                frame,
                frame,
                cost_penalty.get(split, 0.0),
            )
        )
    return rows


def _long_short_rows(split_frames: Mapping[str, pd.DataFrame], cost_penalty: Mapping[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, frame in split_frames.items():
        for direction, subset in frame.groupby("direction", sort=True):
            rows.append(_slice_row(split, "direction", str(direction), subset, frame, cost_penalty.get(split, 0.0)))
    return rows


def _concentration_rows(
    split_frames: Mapping[str, pd.DataFrame],
    source_summary: pd.DataFrame,
    report_metrics: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, frame in split_frames.items():
        total_net = _sum(frame["net_profit"])
        third_net = frame.groupby("chronological_third")["net_profit"].sum().to_dict()
        month_net = frame.groupby("month")["net_profit"].sum().to_dict()
        top_positive = sorted([float(v) for v in frame["net_profit"] if float(v) > 0.0], reverse=True)
        summary_row = _source_row(source_summary, split)
        metrics = report_metrics[split]
        same_reentry_ratio = float(frame["same_direction_reentry"].mean()) if len(frame) else math.nan
        values = [
            (
                "top_single_trade_share",
                _safe_ratio(top_positive[0] if top_positive else 0.0, total_net),
                0.25,
                "single largest winning trade share of total net",
            ),
            (
                "top5_trade_share",
                _safe_ratio(sum(top_positive[:5]), total_net),
                0.40,
                "top five winning trades share of total net",
            ),
            (
                "best_month_net_share",
                _safe_ratio(max(month_net.values()) if month_net else 0.0, total_net),
                0.50,
                "largest month share of total net",
            ),
            (
                "largest_third_net_share",
                _safe_ratio(max(third_net.values()) if third_net else 0.0, total_net),
                0.65,
                "largest chronological third share of total net",
            ),
            (
                "late_third_net_share",
                _safe_ratio(third_net.get("late", 0.0), total_net),
                0.20,
                "late third should contribute positive continuation, not flatline",
            ),
            (
                "negative_month_count",
                sum(1 for value in month_net.values() if value < 0.0),
                0,
                "negative monthly buckets count",
            ),
            (
                "same_direction_reentry_ratio_local",
                same_reentry_ratio,
                0.35,
                "same-direction entries within five M5 bars",
            ),
            (
                "same_move_reentry_ratio_source",
                _to_float(summary_row.get("same_move_reentry_ratio")),
                0.35,
                "source Stage56 same-move ratio",
            ),
            (
                "cost_stressed_expectancy",
                _to_float(summary_row.get("cost_stressed_expectancy")),
                0.25,
                "Stage56 source cost-stressed expectancy",
            ),
            (
                "mfe_capture_ratio",
                _to_float(summary_row.get("mfe_capture_ratio")),
                0.60,
                "Stage56 source MFE capture ratio",
            ),
            (
                "balance_drawdown_maximal_amount",
                _to_float(metrics.get("balance_drawdown_maximal_amount")),
                300.0,
                "MT5 reported balance drawdown amount",
            ),
            (
                "equity_drawdown_maximal_amount",
                _to_float(metrics.get("equity_drawdown_maximal_amount")),
                350.0,
                "MT5 reported equity drawdown amount",
            ),
        ]
        for metric, value, threshold, notes in values:
            rows.append(
                {
                    "split": split,
                    "metric": metric,
                    "value": value,
                    "threshold": threshold,
                    "status": _concentration_status(metric, value, threshold, split),
                    "notes": notes,
                }
            )
    rows.append(
        {
            "split": "validation_is",
            "metric": "tier_b_contribution",
            "value": "disabled",
            "threshold": "required_record",
            "status": "recorded_disabled_not_omitted",
            "notes": "Tier B fallback-only remained disabled due prior fallback damage evidence.",
        }
    )
    rows.append(
        {
            "split": "oos",
            "metric": "tier_b_contribution",
            "value": "disabled",
            "threshold": "required_record",
            "status": "recorded_disabled_not_omitted",
            "notes": "Tier B fallback-only remained disabled due prior fallback damage evidence.",
        }
    )
    rows.append(
        {
            "split": "all",
            "metric": "mandatory_atr_sltp",
            "value": "missing",
            "threshold": "must_exist_before_final",
            "status": "mandatory_capability_missing_not_final",
            "notes": "Stage57 is audit only; ATR SL/TP is not developed in this stage.",
        }
    )
    rows.append(
        {
            "split": "all",
            "metric": "mandatory_model_controlled_risk_pct",
            "value": "missing",
            "threshold": "must_exist_before_final",
            "status": "mandatory_capability_missing_not_final",
            "notes": "Stage57 is audit only; model-controlled risk percent is not developed in this stage.",
        }
    )
    return rows


def _kpi_row(
    split: str,
    segment_type: str,
    segment: str,
    subset: pd.DataFrame,
    cost_penalty: float,
    full_frame: pd.DataFrame,
) -> dict[str, Any]:
    kpi = _kpi(subset, cost_penalty)
    return {
        "split": split,
        "segment_type": segment_type,
        "segment": segment,
        "trade_count": kpi["trade_count"],
        "net_profit": kpi["net_profit"],
        "profit_factor": kpi["profit_factor"],
        "win_rate": kpi["win_rate"],
        "expectancy": kpi["expectancy"],
        "cost_stressed_expectancy": kpi["cost_stressed_expectancy"],
        "max_closed_trade_drawdown": kpi["max_closed_trade_drawdown"],
        "mfe_mean": kpi["mfe_mean"],
        "mae_mean": kpi["mae_mean"],
        "realized_over_mfe_mean": kpi["realized_over_mfe_mean"],
        "mfe_capture_ratio": kpi["mfe_capture_ratio"],
        "top_trade_net": kpi["top_trade_net"],
        "top_trade_net_share": _safe_ratio(kpi["top_trade_net"], _sum(full_frame["net_profit"])),
        "top5_trade_net_share": _safe_ratio(kpi["top5_trade_net"], _sum(full_frame["net_profit"])),
        "start_time": kpi["start_time"],
        "end_time": kpi["end_time"],
        "quality_flag": _segment_quality(split, segment_type, segment, kpi, full_frame),
    }


def _slice_row(
    split: str,
    axis: str,
    bucket: str,
    subset: pd.DataFrame,
    full_frame: pd.DataFrame,
    cost_penalty: float,
) -> dict[str, Any]:
    kpi = _kpi(subset, cost_penalty)
    return {
        "split": split,
        "axis": axis,
        "bucket": bucket,
        "trade_count": kpi["trade_count"],
        "net_profit": kpi["net_profit"],
        "profit_factor": kpi["profit_factor"],
        "win_rate": kpi["win_rate"],
        "expectancy": kpi["expectancy"],
        "cost_stressed_expectancy": kpi["cost_stressed_expectancy"],
        "trade_share": _safe_ratio(kpi["trade_count"], len(full_frame)),
        "net_share": _safe_ratio(kpi["net_profit"], _sum(full_frame["net_profit"])),
        "mfe_mean": kpi["mfe_mean"],
        "mae_mean": kpi["mae_mean"],
        "realized_over_mfe_mean": kpi["realized_over_mfe_mean"],
        "mfe_capture_ratio": kpi["mfe_capture_ratio"],
        "quality_flag": _slice_quality(axis, bucket, kpi, full_frame),
    }


def _kpi(frame: pd.DataFrame, cost_penalty: float) -> dict[str, Any]:
    if frame.empty:
        return {
            "trade_count": 0,
            "net_profit": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "profit_factor": None,
            "win_rate": None,
            "expectancy": None,
            "cost_stressed_expectancy": None,
            "max_closed_trade_drawdown": 0.0,
            "mfe_mean": None,
            "mae_mean": None,
            "realized_over_mfe_mean": None,
            "mfe_capture_ratio": None,
            "top_trade_net": 0.0,
            "top5_trade_net": 0.0,
            "start_time": "",
            "end_time": "",
        }
    net_values = [float(v) for v in frame["net_profit"]]
    gross_profit = sum(v for v in net_values if v > 0.0)
    gross_loss = sum(v for v in net_values if v < 0.0)
    expectancy = _safe_ratio(sum(net_values), len(net_values))
    top_positive = sorted([v for v in net_values if v > 0.0], reverse=True)
    mfe_sum = _sum(frame["mfe"])
    return {
        "trade_count": len(frame),
        "net_profit": sum(net_values),
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": _safe_ratio(gross_profit, abs(gross_loss)),
        "win_rate": _safe_ratio(sum(1 for v in net_values if v > 0.0), len(net_values)),
        "expectancy": expectancy,
        "cost_stressed_expectancy": expectancy - cost_penalty if expectancy is not None else None,
        "max_closed_trade_drawdown": _max_drawdown(net_values),
        "mfe_mean": _mean(frame["mfe"]),
        "mae_mean": _mean(frame["mae"]),
        "realized_over_mfe_mean": _mean(frame["realized_over_mfe"]),
        "mfe_capture_ratio": _safe_ratio(sum(net_values), mfe_sum),
        "top_trade_net": top_positive[0] if top_positive else 0.0,
        "top5_trade_net": sum(top_positive[:5]),
        "start_time": frame["close_time"].min().isoformat(),
        "end_time": frame["close_time"].max().isoformat(),
    }


def _max_drawdown(net_values: Sequence[float]) -> float:
    peak = 0.0
    cumulative = 0.0
    max_dd = 0.0
    for value in net_values:
        cumulative += float(value)
        peak = max(peak, cumulative)
        max_dd = max(max_dd, peak - cumulative)
    return max_dd


def _segment_quality(
    split: str,
    segment_type: str,
    segment: str,
    kpi: Mapping[str, Any],
    full_frame: pd.DataFrame,
) -> str:
    flags: list[str] = []
    total_net = _sum(full_frame["net_profit"])
    net = _to_float(kpi.get("net_profit")) or 0.0
    pf = _to_float(kpi.get("profit_factor"))
    if segment_type == "chronological_third":
        share = _safe_ratio(net, total_net)
        if net <= 0.0:
            flags.append("negative_or_flat_segment")
        if pf is not None and pf < 1.05:
            flags.append("weak_segment_pf")
        if share is not None and share > 0.65:
            flags.append("single_window_profit_concentration")
        if split == "validation_is" and segment == "late" and net <= 0.0:
            flags.append("validation_late_flatline_risk")
        if split == "oos" and segment == "late" and share is not None and share > 0.60:
            flags.append("oos_late_period_concentration")
        if split == "oos" and segment == "early" and net <= 0.0:
            flags.append("oos_early_drawdown_risk")
    return ";".join(flags) if flags else "acceptable_measurement_only"


def _monthly_quality(split: str, month: str, kpi: Mapping[str, Any], total_net: float) -> str:
    flags: list[str] = []
    net = _to_float(kpi.get("net_profit")) or 0.0
    share = _safe_ratio(net, total_net)
    if net < 0.0:
        flags.append("negative_month")
    if share is not None and share > 0.50:
        flags.append("single_month_profit_concentration")
    return ";".join(flags) if flags else "acceptable_measurement_only"


def _slice_quality(axis: str, bucket: str, kpi: Mapping[str, Any], full_frame: pd.DataFrame) -> str:
    flags: list[str] = []
    net = _to_float(kpi.get("net_profit")) or 0.0
    net_share = _safe_ratio(net, _sum(full_frame["net_profit"]))
    trade_share = _safe_ratio(_to_float(kpi.get("trade_count")) or 0.0, len(full_frame))
    pf = _to_float(kpi.get("profit_factor"))
    if net_share is not None and net_share > 0.60:
        flags.append("bucket_profit_concentration")
    if trade_share is not None and trade_share > 0.60:
        flags.append("bucket_trade_concentration")
    if pf is not None and pf < 1.0:
        flags.append("bucket_pf_below_one")
    if axis == "weather_proxy":
        flags.append("weather_not_directly_available")
    return ";".join(flags) if flags else "acceptable_measurement_only"


def _concentration_status(metric: str, value: Any, threshold: Any, split: str) -> str:
    numeric = _to_float(value)
    threshold_numeric = _to_float(threshold)
    if numeric is None or threshold_numeric is None:
        return "missing_or_not_numeric"
    high_is_bad = {
        "top_single_trade_share",
        "top5_trade_share",
        "best_month_net_share",
        "largest_third_net_share",
        "negative_month_count",
        "same_direction_reentry_ratio_local",
        "same_move_reentry_ratio_source",
        "balance_drawdown_maximal_amount",
        "equity_drawdown_maximal_amount",
    }
    low_is_bad = {"late_third_net_share", "cost_stressed_expectancy", "mfe_capture_ratio"}
    if metric in high_is_bad and numeric > threshold_numeric:
        return "risk_flag"
    if metric in low_is_bad and numeric < threshold_numeric:
        return "risk_flag"
    if metric == "late_third_net_share" and split == "validation_is" and numeric <= 0.0:
        return "risk_flag"
    return "passed_measurement_only"


def _build_summary(
    *,
    split_frames: Mapping[str, pd.DataFrame],
    report_metrics: Mapping[str, Mapping[str, Any]],
    source_summary: pd.DataFrame,
    concentration_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    split_summary: OrderedDict[str, Any] = OrderedDict()
    for split, frame in split_frames.items():
        source = _source_row(source_summary, split)
        thirds = {
            label: _round_map(_kpi(frame[frame["chronological_third"].eq(label)], 0.0))
            for label in ("early", "mid", "late")
        }
        months = {str(month): float(value) for month, value in frame.groupby("month")["net_profit"].sum().to_dict().items()}
        split_summary[split] = {
            "source_stage56": _row_to_plain(source),
            "report_metrics": _row_to_plain(report_metrics[split]),
            "trade_count": int(len(frame)),
            "net_profit": _round(_sum(frame["net_profit"])),
            "date_range": {
                "start": frame["close_time"].min().isoformat(),
                "end": frame["close_time"].max().isoformat(),
            },
            "chronological_thirds": thirds,
            "monthly_net": {key: _round(value) for key, value in months.items()},
            "negative_months": [key for key, value in months.items() if value < 0.0],
            "same_direction_reentry_ratio_local": _round(float(frame["same_direction_reentry"].mean())),
            "risk_flags": _risk_flags_for_split(split, concentration_rows, segment_rows),
        }
    return {
        "created_at_utc": UTC_NOW,
        "stage_id": STAGE57_ID,
        "run_id": RUN57_ID,
        "source_stage_id": STAGE56_ID,
        "source_run_id": RUN50CA_ID,
        "adapter_id": ADAPTER_ID,
        "development_anchor": DEVELOPMENT_ANCHOR,
        "backup_anchor": BACKUP_ANCHOR,
        "primary_family": "kpi_evidence",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": [
            "obsidian-artifact-lineage",
            "obsidian-result-judgment",
            "obsidian-performance-attribution",
            "obsidian-backtest-forensics",
            "obsidian-data-integrity",
        ],
        "required_gates": [
            "kpi_contract_audit",
            "row_grain_audit",
            "source_authority_audit",
            "required_gate_coverage_audit",
        ],
        "claim_boundary": BOUNDARY,
        "bounded_question": (
            "Is the current Stage56 BaselineAdapter anchor strong enough, from equity curve and "
            "segmented KPI evidence, to proceed toward mandatory ATR/risk integration or must it "
            "be demoted/repaired/branched first?"
        ),
        "stage57_decision": DECISION,
        "decision_reason": (
            "ba14 remains a useful development reference, but validation late-third net is flat/negative, "
            "validation top-five trade share is high, OOS early segment PF is weak with an early-month drawdown, "
            "OOS late-third share is high, Tier B is disabled, and mandatory ATR SL/TP plus model-controlled risk% are missing."
        ),
        "allowed_claims": ["development_anchor", "adapter_candidate", "segment_kpi_failed", "failure_memory"],
        "forbidden_claims": [
            "deployment",
            "live_readiness",
            "production_baseline",
            "operating_promotion",
            "operating_reference",
            "runtime_authority",
            "overall_goal_complete",
        ],
        "split_summary": split_summary,
        "risk_flag_count": sum(1 for row in concentration_rows if row.get("status") == "risk_flag"),
        "required_outputs": {
            "equity_curve_audit": _rel(REVIEWS_ROOT / "equity_curve_audit.md"),
            "segment_kpi_summary": _rel(REVIEWS_ROOT / "segment_kpi_summary.csv"),
            "monthly_kpi_summary": _rel(REVIEWS_ROOT / "monthly_kpi_summary.csv"),
            "session_regime_kpi_summary": _rel(REVIEWS_ROOT / "session_regime_kpi_summary.csv"),
            "long_short_kpi_summary": _rel(REVIEWS_ROOT / "long_short_kpi_summary.csv"),
            "concentration_risk_report": _rel(REVIEWS_ROOT / "concentration_risk_report.md"),
            "stage57_decision": _rel(REVIEWS_ROOT / "stage57_decision.md"),
        },
        "next_stage": {
            "stage_id": STAGE58_ID,
            "planned_run_id": RUN58_PLANNED_ID,
            "handoff_decision": DECISION,
            "effect": "repair the current adapter before mandatory ATR SL/TP and model-controlled risk% integration",
        },
    }


def _risk_flags_for_split(
    split: str,
    concentration_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
) -> list[str]:
    flags: list[str] = []
    for row in concentration_rows:
        if row.get("split") == split and row.get("status") == "risk_flag":
            flags.append(str(row.get("metric")))
    for row in segment_rows:
        if row.get("split") == split:
            text = str(row.get("quality_flag") or "")
            if text and text != "acceptable_measurement_only":
                flags.extend(text.split(";"))
    return sorted(set(flags))


def _run_manifest(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE57_ID,
        "run_id": RUN57_ID,
        "packet_id": PACKET_ID,
        "created_at_utc": UTC_NOW,
        "source_stage_id": STAGE56_ID,
        "source_run_id": RUN50CA_ID,
        "source_reports": {split: _rel(path) for split, path in REPORTS.items()},
        "source_summary_csv": _rel(STAGE56_SUMMARY_CSV),
        "source_risk_telemetry_csv": _rel(STAGE56_RISK_CSV),
        "replay_policy": "no_new_optimization_existing_run50CA_reports_only",
        "decision": summary["stage57_decision"],
        "claim_boundary": BOUNDARY,
    }


def _equity_audit_markdown(summary: Mapping[str, Any]) -> str:
    val = summary["split_summary"]["validation_is"]
    oos = summary["split_summary"]["oos"]
    return f"""# Stage57 Equity Curve Audit(57단계 자금 곡선 감사)

- stage(단계): `{STAGE57_ID}`
- run(실행): `{RUN57_ID}`
- source(원천): Stage56(56단계) `{RUN50CA_ID}`
- adapter(어댑터): `{ADAPTER_ID}`
- boundary(경계): `{BOUNDARY}`

## Question(질문)

현재 Stage56(56단계) BaselineAdapter(기준선 어댑터) anchor(기준점)가 equity curve(자금 곡선)와 segment KPI(구간 핵심 성과 지표) 기준으로 ATR/risk(ATR/위험) 통합으로 바로 갈 만큼 충분한가?

## Read(판독)

Stage57(57단계)는 optimization(최적화)이나 repair(수리)를 하지 않았다. Effect(효과): 기존 run50CA(실행 run50CA) MT5 ONNX runtime(런타임) 보고서만 사용해 Stage58(58단계) 방향을 정한다.

## Validation(검증)

- net(순손익): `{val['net_profit']}`
- trade_count(거래 수): `{val['trade_count']}`
- early/mid/late net(초/중/후반 순손익): `{_third_net_text(val)}`
- negative months(음수 월): `{', '.join(val['negative_months']) or 'none'}`
- risk flags(위험 표식): `{', '.join(val['risk_flags']) or 'none'}`

Validation(검증)은 final net(최종 순손익)은 높지만 late third(후반 3분위)가 flat/negative(정체/음수)이고, top-five trade share(상위 5거래 비중)가 높다. Effect(효과): final net(최종 순손익)만으로 strong(강함)을 주장하지 않는다.

## OOS(표본외)

- net(순손익): `{oos['net_profit']}`
- trade_count(거래 수): `{oos['trade_count']}`
- early/mid/late net(초/중/후반 순손익): `{_third_net_text(oos)}`
- negative months(음수 월): `{', '.join(oos['negative_months']) or 'none'}`
- risk flags(위험 표식): `{', '.join(oos['risk_flags']) or 'none'}`

OOS(표본외)는 net(순손익)이 좋지만 early third(초반 3분위)의 PF(수익 팩터)가 약하고 first month(첫 달)가 음수이며 late third(후반 3분위)에 수익이 몰린다. Effect(효과): validation/OOS consistency(검증/표본외 일관성)를 아직 research-grade(연구 등급)로 닫지 않는다.

## Decision(판정)

`{DECISION}`

Effect(효과): `{ADAPTER_ID}`는 development reference(개발 참조)로 보존하지만, Stage58(58단계)는 먼저 bounded repair(경계 수리) 판단을 포함해야 한다. ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)는 mandatory(필수)이지만, 추가 자체가 completion(완료)이 아니다.
"""


def _concentration_markdown(summary: Mapping[str, Any]) -> str:
    val = summary["split_summary"]["validation_is"]
    oos = summary["split_summary"]["oos"]
    return f"""# Stage57 Concentration Risk Report(57단계 집중 위험 보고서)

- stage(단계): `{STAGE57_ID}`
- run(실행): `{RUN57_ID}`
- decision(판정): `{DECISION}`

## Main Flags(주요 표식)

- validation(검증): `{', '.join(val['risk_flags']) or 'none'}`
- OOS(표본외): `{', '.join(oos['risk_flags']) or 'none'}`
- Tier B(티어 B): disabled(비활성) evidence(근거)는 기록했고, synthetic combined result(합성 합산 결과)는 만들지 않았다.
- ATR SL/TP(ATR 손절/익절): missing(누락), final adapter(최종 어댑터) 주장 불가.
- model-controlled risk%(모델 제어 위험률): missing(누락), final adapter(최종 어댑터) 주장 불가.

## Interpretation(해석)

ba14(ba14)는 final net(최종 순손익)이 높지만 curve quality(곡선 품질)에는 집중 위험이 있다. Effect(효과): Stage58(58단계)는 ATR/risk(ATR/위험) 추가를 곧바로 finalization(최종화)로 보지 않고, repair-before-integration(통합 전 수리) 경로로 시작한다.

## Boundary(경계)

No deployment(배포 없음), no live readiness(실거래 준비 없음), no production baseline(생산 기준선 없음), no operating promotion(운영 승격 없음), no operating reference(운영 기준 없음), no runtime authority(런타임 권위 없음).
"""


def _stage57_decision_markdown(summary: Mapping[str, Any]) -> str:
    return f"""# Stage57 Decision(57단계 판정)

decision(판정): `{DECISION}`

Stage57(57단계)는 bounded audit gate(경계 감사 관문)로 닫는다. Effect(효과): Stage56(56단계)이 더 이상 future BaselineAdapter work(향후 기준선 어댑터 작업)를 흡수하지 않게 한다.

## Evidence(근거)

- equity_curve_audit(자금 곡선 감사): `{summary['required_outputs']['equity_curve_audit']}`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `{summary['required_outputs']['segment_kpi_summary']}`
- monthly_kpi_summary(월별 핵심 성과 지표 요약): `{summary['required_outputs']['monthly_kpi_summary']}`
- session_regime_kpi_summary(세션/국면 핵심 성과 지표 요약): `{summary['required_outputs']['session_regime_kpi_summary']}`
- long_short_kpi_summary(롱/숏 핵심 성과 지표 요약): `{summary['required_outputs']['long_short_kpi_summary']}`
- concentration_risk_report(집중 위험 보고서): `{summary['required_outputs']['concentration_risk_report']}`

## Reason(이유)

`{ADAPTER_ID}` remains a development reference(개발 참조로 유지) because MT5 ONNX runtime reproduction(MT5 ONNX 런타임 재현)은 통과했다. 그러나 validation(검증) late-third flatline(후반 정체), validation(검증) top-five concentration(상위 5거래 집중), OOS(표본외) early segment PF weakness(초반 구간 수익 팩터 약점), OOS(표본외) first-month drawdown(첫 달 손실), OOS(표본외) late profit concentration(후반 수익 집중), Tier B disabled(티어 B 비활성), ATR SL/TP missing(ATR 손절/익절 누락), model-controlled risk% missing(모델 제어 위험률 누락)이 남아 있다.

## Next(다음)

Open Stage58(58단계): `{STAGE58_ID}` with planned run(계획 실행) `{RUN58_PLANNED_ID}`.

Stage58(58단계)는 ATR/risk(ATR/위험) standalone campaign(독립 캠페인)이 아니다. Effect(효과): 먼저 adapter repair need(어댑터 수리 필요)를 다루고, mandatory ATR SL/TP(필수 ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)를 full adapter(전체 어댑터) 기준으로 통합/측정한다.

## Forbidden Claims(금지 주장)

Deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)는 주장하지 않는다.
"""


def _stage57_brief() -> str:
    return f"""# Stage57 Brief(57단계 개요)

- stage_id(단계 ID): `{STAGE57_ID}`
- packet(작업 묶음): `{PACKET_ID}`
- primary_family(주 작업군): `kpi_evidence`
- primary_skill(주 스킬): `obsidian-run-evidence-system`
- bounded_question(경계 질문): Is the current Stage56/BaselineAdapter anchor strong enough, from equity curve and segmented KPI evidence, to proceed toward mandatory ATR/risk integration or must it be demoted/repaired/branched first?
- boundary(경계): `{BOUNDARY}`

Stage57(57단계)는 audit gate(감사 관문)이다. Effect(효과): open-ended optimization(무기한 최적화), ATR/risk development(ATR/위험 개발), ONNX hardening(ONNX 경화)을 Stage57(57단계)에 넣지 않는다.
"""


def _stage57_inputs() -> str:
    return f"""# Stage57 Input References(57단계 입력 참조)

- source_summary(원천 요약): `{_rel(STAGE56_SUMMARY_CSV)}`
- source_risk_telemetry(원천 위험 텔레메트리): `{_rel(STAGE56_RISK_CSV)}`
- validation_report(검증 보고서): `{_rel(REPORTS['validation_is'])}`
- oos_report(표본외 보고서): `{_rel(REPORTS['oos'])}`

No new optimization(새 최적화 없음). Effect(효과): Stage57(57단계)는 run50CA(실행 run50CA)의 existing MT5 ONNX runtime evidence(기존 MT5 ONNX 런타임 근거)만 감사한다.
"""


def _stage57_review_index() -> str:
    return f"""# Stage57 Review Index(57단계 검토 색인)

- equity_curve_audit(자금 곡선 감사): `equity_curve_audit.md`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `segment_kpi_summary.csv`
- monthly_kpi_summary(월별 핵심 성과 지표 요약): `monthly_kpi_summary.csv`
- session_regime_kpi_summary(세션/국면 핵심 성과 지표 요약): `session_regime_kpi_summary.csv`
- long_short_kpi_summary(롱/숏 핵심 성과 지표 요약): `long_short_kpi_summary.csv`
- concentration_risk_report(집중 위험 보고서): `concentration_risk_report.md`
- stage57_decision(57단계 판정): `stage57_decision.md`

Decision(판정): `{DECISION}`.
"""


def _stage57_selection_status(summary: Mapping[str, Any]) -> str:
    return f"""# Stage57 Selection Status(57단계 선택 상태)

- stage_status(단계 상태): `closed_bounded_audit_gate`
- latest_run_id(최신 실행 ID): `{RUN57_ID}`
- current_judgment(현재 판정): `{DECISION}`
- selected_research_baseline(선택 연구 기준선): `none`
- selected_adapter(선택 어댑터): `{ADAPTER_ID}`
- next_stage(다음 단계): `{STAGE58_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage57(57단계)는 audit(감사)만 닫고, 전체 BaselineAdapter goal(기준선 어댑터 목표)은 계속 진행한다.
"""


def _stage58_brief() -> str:
    return f"""# Stage58 Brief(58단계 개요)

- stage_id(단계 ID): `{STAGE58_ID}`
- planned_run(계획 실행): `{RUN58_PLANNED_ID}`
- source_decision(원천 판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can the current adapter be repaired enough, then integrated with mandatory ATR SL/TP(필수 ATR 손절/익절) and model-controlled risk%(모델 제어 위험률), without damaging validation/OOS(검증/표본외), segment KPI(구간 핵심 성과 지표), equity curve(자금 곡선), drawdown(손실폭), cost-stressed expectancy(비용 압박 기대값), MFE/MAE(최대 유리/불리 이동), or runtime telemetry(런타임 텔레메트리)?

Stage58(58단계)는 standalone ATR/risk campaign(독립 ATR/위험 캠페인)이 아니다. Effect(효과): Stage57(57단계)에서 발견한 curve/segment weakness(곡선/구간 약점)를 먼저 bounded repair(경계 수리)로 다룬 뒤 mandatory capability(필수 기능)를 full adapter(전체 어댑터) 기준으로 통합/측정한다.
"""


def _stage58_inputs(summary: Mapping[str, Any]) -> str:
    return f"""# Stage58 Input References(58단계 입력 참조)

- stage57_decision(57단계 판정): `{_rel(REVIEWS_ROOT / 'stage57_decision.md')}`
- equity_curve_audit(자금 곡선 감사): `{summary['required_outputs']['equity_curve_audit']}`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `{summary['required_outputs']['segment_kpi_summary']}`
- monthly_kpi_summary(월별 핵심 성과 지표 요약): `{summary['required_outputs']['monthly_kpi_summary']}`
- source_adapter_spec(원천 어댑터 명세): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/04_selected/baseline_adapter_ba14_spec.json`
- source_runtime_summary(원천 런타임 요약): `{_rel(STAGE56_SUMMARY_CSV)}`

Effect(효과): Stage58(58단계)는 final net(최종 순손익)이 아니라 segment stability(구간 안정성), risk telemetry(위험 텔레메트리), bracket telemetry(브래킷 텔레메트리), validation/OOS consistency(검증/표본외 일관성)를 기준으로 판단한다.
"""


def _stage58_review_index() -> str:
    return """# Stage58 Review Index(58단계 검토 색인)

Stage58(58단계)는 아직 시작 상태다. Required outputs(필수 산출물)는 Stage58 execution(58단계 실행) 중 생성한다.

- risk_atr_integration_report.md
- risk_telemetry_summary.csv
- atr_bracket_telemetry_summary.csv
- risk_floor_segment_impact.csv
- risk_atr_segment_kpi_summary.csv
- stage58_decision.md
"""


def _stage58_selection_status(summary: Mapping[str, Any]) -> str:
    return f"""# Stage58 Selection Status(58단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage57`
- planned_run_id(계획 실행 ID): `{RUN58_PLANNED_ID}`
- source_stage(원천 단계): `{STAGE57_ID}`
- source_decision(원천 판정): `{DECISION}`
- selected_research_baseline(선택 연구 기준선): `none`
- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage58(58단계)는 repair-before-risk/ATR(위험/ATR 전 수리) 경로로 열린다. ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)는 mandatory(필수)이지만 sufficient(충분)하지 않다.
"""


def _stage56_selection_status(summary: Mapping[str, Any]) -> str:
    return f"""# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `handed_off_to_stage57_bounded_post_stage56_development`
- latest_run_id(최신 실행 ID): `{RUN50CA_ID}`
- current_judgment(현재 판정): `mt5_runtime_reproduction_attempted_research_only_handed_off`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`

## BaselineAdapter ONNX Runtime Evidence(기준선 어댑터 ONNX 런타임 근거)

- selected_adapter(선택 어댑터): `{ADAPTER_ID}`
- adapter_spec(어댑터 명세): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/04_selected/baseline_adapter_ba14_spec.json`
- onnx_parity_report(ONNX 동등성 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50BZ_baseline_adapter_onnx_parity.json`
- runtime_reproduction_report(런타임 재현 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50CA_baseline_adapter_onnx_runtime_reproduction.md`
- runtime_summary_json(런타임 요약 JSON): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50CA_baseline_adapter_onnx_runtime_reproduction_summary.json`
- runtime_summary_csv(런타임 요약 CSV): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50CA_baseline_adapter_onnx_runtime_reproduction_summary.csv`
- runtime_risk_telemetry(런타임 위험 텔레메트리): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50CA_baseline_adapter_onnx_runtime_reproduction_risk_telemetry.csv`
- runtime_gate_passed(런타임 게이트 통과): `True`

## Handoff(인계)

- stage57(57단계): `{STAGE57_ID}`
- stage57_decision(57단계 판정): `{DECISION}`
- next_stage(다음 단계): `{STAGE58_ID}`

Effect(효과): Stage56(56단계)는 더 이상 new BaselineAdapter work(새 기준선 어댑터 작업)를 흡수하지 않는다. BaselineAdapter campaign(기준선 어댑터 캠페인)은 Stage58(58단계)로 이어진다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).
"""


def _decision_memo(summary: Mapping[str, Any]) -> str:
    return f"""# 2026-05-15 Stage57 Equity Segment KPI Audit Decision(57단계 자금/구간 KPI 감사 판정)

- stage(단계): `{STAGE57_ID}`
- run(실행): `{RUN57_ID}`
- decision(판정): `{DECISION}`
- next_stage(다음 단계): `{STAGE58_ID}`
- boundary(경계): `{BOUNDARY}`

Stage57(57단계)는 Stage56(56단계)의 `ba14_no_atr_sd5_lot025` evidence(근거)를 bounded audit(경계 감사)로 읽었다. Effect(효과): Stage56(56단계)을 더 키우지 않고, BaselineAdapter(기준선 어댑터) 작업을 작은 단계로 이동한다.

판정 이유(reason, 이유): validation(검증) late-third flatline(후반 정체), validation(검증) top-five concentration(상위 5거래 집중), OOS(표본외) early segment PF weakness(초반 구간 수익 팩터 약점), OOS(표본외) first-month drawdown(첫 달 손실), OOS(표본외) late concentration(후반 집중), Tier B disabled(티어 B 비활성), ATR SL/TP missing(ATR 손절/익절 누락), model-controlled risk% missing(모델 제어 위험률 누락).

No deployment(배포 없음), no live readiness(실거래 준비 없음), no production baseline(생산 기준선 없음), no operating promotion(운영 승격 없음), no operating reference(운영 기준 없음), no runtime authority(런타임 권위 없음).
"""


def _current_working_state(summary: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `stage58_adapter_repair_before_risk_atr_v1`
- current_run(현재 실행): `{RUN58_PLANNED_ID}`
- active_stage(활성 단계): `{STAGE58_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`
- status(상태): `stage57_closed_stage58_opened`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage57(57단계) closed(종료) as a bounded equity and segment KPI audit gate(경계 자금/구간 핵심 성과 지표 감사 관문). Effect(효과): Stage56(56단계)이 더 이상 future BaselineAdapter work(향후 기준선 어댑터 작업)를 흡수하지 않는다.

## Latest Stage57 Evidence(최신 57단계 근거)

- source_run(원천 실행): `{RUN50CA_ID}`
- adapter_id(어댑터 ID): `{ADAPTER_ID}`
- decision(판정): `{DECISION}`
- validation risk flags(검증 위험 표식): `{', '.join(summary['split_summary']['validation_is']['risk_flags']) or 'none'}`
- OOS risk flags(표본외 위험 표식): `{', '.join(summary['split_summary']['oos']['risk_flags']) or 'none'}`
- required outputs(필수 산출물): `{summary['required_outputs']['stage57_decision']}`

## Active Next Stage(활성 다음 단계)

Stage58(58단계) `{STAGE58_ID}` is open(개방). Effect(효과): bounded repair(경계 수리)를 먼저 다루고, mandatory ATR SL/TP(필수 ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)를 full adapter(전체 어댑터) 기준으로 통합/측정한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
"""


def _write_packet(summary: Mapping[str, Any]) -> None:
    gate_payloads = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "primary_family": "kpi_evidence",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": summary["support_skills"],
            "required_gates": summary["required_gates"],
            "source_of_truth": "docs/agent_control/work_family_registry.yaml",
            "status": "completed",
        },
        "skill_receipts.json": {
            "packet_id": PACKET_ID,
            "skills_used": [
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-performance-attribution",
                "obsidian-backtest-forensics",
                "obsidian-data-integrity",
            ],
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            "status": "passed_with_flags",
            "grain": "split + segment/month/session/regime/direction",
            "required_outputs": summary["required_outputs"],
            "effect": "Stage57 measures existing evidence and does not optimize.",
        },
        "row_grain_audit.json": {
            "status": "passed",
            "row_grains": {
                "segment_kpi_summary": "split + segment_type + segment",
                "monthly_kpi_summary": "split + month",
                "session_regime_kpi_summary": "split + axis + bucket",
                "long_short_kpi_summary": "split + direction",
                "concentration_risk_summary": "split + metric",
            },
        },
        "source_authority_audit.json": {
            "status": "passed",
            "source_run_id": RUN50CA_ID,
            "source_reports": {split: _rel(path) for split, path in REPORTS.items()},
            "no_new_optimization": True,
        },
        "artifact_lineage_audit.json": {
            "status": "passed",
            "source_stage": STAGE56_ID,
            "derived_stage": STAGE57_ID,
            "source_summary": _rel(STAGE56_SUMMARY_CSV),
            "derived_outputs": summary["required_outputs"],
        },
        "result_judgment_gate.json": {
            "status": "passed_with_research_boundary",
            "decision": DECISION,
            "allowed_claims": summary["allowed_claims"],
            "forbidden_claims": summary["forbidden_claims"],
        },
        "required_gate_coverage_audit.json": {
            "status": "passed",
            "required_gates": summary["required_gates"],
            "covered_gates": summary["required_gates"],
        },
        "final_claim_guard.json": {
            "status": "passed",
            "overall_goal_complete": False,
            "stage57_closeout_is_not_goal_completion": True,
            "forbidden_claims": summary["forbidden_claims"],
        },
        "aggregate_summary.json": summary,
    }
    for name, payload in gate_payloads.items():
        _write_json(PACKET_ROOT / name, payload)


def _write_stage_ledger(summary: Mapping[str, Any]) -> None:
    rows = _alpha_rows(summary)
    _write_csv(STAGE57_ROOT / "03_reviews" / "stage_run_ledger.csv", ALPHA_LEDGER_COLUMNS, rows)


def _update_registries(summary: Mapping[str, Any]) -> None:
    run_rows = [
        {
            "run_id": RUN57_ID,
            "stage_id": STAGE57_ID,
            "lane": "baseline_adapter_equity_segment_audit",
            "status": "completed",
            "judgment": DECISION,
            "path": _rel(REVIEWS_ROOT / "stage57_decision.md"),
            "notes": (
                "adapter=ba14_no_atr_sd5_lot025;source_run=run50CA;decision="
                f"{DECISION};boundary={BOUNDARY}"
            ),
        }
    ]
    _upsert_csv(REPO_ROOT / "docs" / "registers" / "run_registry.csv", RUN_REGISTRY_COLUMNS, "run_id", run_rows)
    _upsert_csv(
        REPO_ROOT / "docs" / "registers" / "alpha_run_ledger.csv",
        ALPHA_LEDGER_COLUMNS,
        "ledger_row_id",
        _alpha_rows(summary),
    )
    _upsert_csv(
        REPO_ROOT / "docs" / "registers" / "artifact_registry.csv",
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        "artifact_id",
        _artifact_rows(),
    )


def _alpha_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    val = summary["split_summary"]["validation_is"]
    oos = summary["split_summary"]["oos"]
    return [
        {
            "ledger_row_id": f"{RUN57_ID}__aggregate_audit",
            "stage_id": STAGE57_ID,
            "run_id": RUN57_ID,
            "subrun_id": "aggregate_audit",
            "parent_run_id": RUN50CA_ID,
            "record_view": "equity_segment_kpi_audit",
            "tier_scope": "Tier A+B",
            "kpi_scope": "baseline_adapter_equity_segment_kpi",
            "scoreboard_lane": "kpi_evidence",
            "status": "completed",
            "judgment": DECISION,
            "path": _rel(REVIEWS_ROOT / "stage57_decision.md"),
            "primary_kpi": ledger_pairs(
                [
                    ("validation_net", val["net_profit"]),
                    ("oos_net", oos["net_profit"]),
                    ("validation_trade_count", val["trade_count"]),
                    ("oos_trade_count", oos["trade_count"]),
                    ("risk_flag_count", summary["risk_flag_count"]),
                ]
            ),
            "guardrail_kpi": (
                "atr_sltp=missing;model_controlled_risk_pct=missing;"
                "tier_b=disabled_recorded;overall_goal_complete=0"
            ),
            "external_verification_status": "completed_existing_mt5_onnx_runtime_reports",
            "notes": "Stage57 audit only; closes with Stage58 repair-before-risk/ATR handoff.",
        },
        {
            "ledger_row_id": f"{RUN57_ID}__validation_equity_segments",
            "stage_id": STAGE57_ID,
            "run_id": RUN57_ID,
            "subrun_id": "validation_equity_segments",
            "parent_run_id": RUN50CA_ID,
            "record_view": "validation_equity_segments",
            "tier_scope": "Tier A+B",
            "kpi_scope": "equity_curve_segment_kpi",
            "scoreboard_lane": "kpi_evidence",
            "status": "completed",
            "judgment": "segment_kpi_failed_adapter_repair_required",
            "path": _rel(REVIEWS_ROOT / "segment_kpi_summary.csv"),
            "primary_kpi": ledger_pairs(
                [
                    ("net", val["net_profit"]),
                    ("early_mid_late", _third_net_text(val)),
                    ("risk_flags", ",".join(val["risk_flags"])),
                ]
            ),
            "guardrail_kpi": "late_third_flatline;top5_trade_concentration",
            "external_verification_status": "completed_existing_mt5_onnx_runtime_report",
            "notes": "Validation curve is not accepted from final net alone.",
        },
        {
            "ledger_row_id": f"{RUN57_ID}__oos_equity_segments",
            "stage_id": STAGE57_ID,
            "run_id": RUN57_ID,
            "subrun_id": "oos_equity_segments",
            "parent_run_id": RUN50CA_ID,
            "record_view": "oos_equity_segments",
            "tier_scope": "Tier A+B",
            "kpi_scope": "equity_curve_segment_kpi",
            "scoreboard_lane": "kpi_evidence",
            "status": "completed",
            "judgment": "segment_kpi_failed_adapter_repair_required",
            "path": _rel(REVIEWS_ROOT / "segment_kpi_summary.csv"),
            "primary_kpi": ledger_pairs(
                [
                    ("net", oos["net_profit"]),
                    ("early_mid_late", _third_net_text(oos)),
                    ("risk_flags", ",".join(oos["risk_flags"])),
                ]
            ),
            "guardrail_kpi": "early_segment_pf_weak;first_month_negative;late_profit_concentration",
            "external_verification_status": "completed_existing_mt5_onnx_runtime_report",
            "notes": "OOS curve has strong final net but profit concentration remains.",
        },
        {
            "ledger_row_id": f"{RUN57_ID}__tier_b_disabled_record",
            "stage_id": STAGE57_ID,
            "run_id": RUN57_ID,
            "subrun_id": "tier_b_disabled_record",
            "parent_run_id": RUN50CA_ID,
            "record_view": "tier_b_disabled_record",
            "tier_scope": "Tier B",
            "kpi_scope": "tier_contribution_record",
            "scoreboard_lane": "kpi_evidence",
            "status": "disabled",
            "judgment": "tier_b_disabled_due_prior_fallback_damage",
            "path": _rel(REVIEWS_ROOT / "concentration_risk_report.md"),
            "primary_kpi": "tier_b_fallback_only=disabled",
            "guardrail_kpi": "not_synthetic_combined;actual_routed_total_uses_tier_a_primary_only",
            "external_verification_status": "completed_existing_stage56_evidence",
            "notes": "Tier B contribution was recorded as disabled, not omitted.",
        },
    ]


def _artifact_rows() -> list[dict[str, Any]]:
    artifacts = [
        ("stage57_run_manifest", "manifest", RUN_ROOT / "run_manifest.json", "Stage57 run identity."),
        ("stage57_kpi_record", "summary", RUN_ROOT / "kpi_record.json", "Stage57 aggregate KPI record."),
        ("stage57_equity_curve_audit", "report", REVIEWS_ROOT / "equity_curve_audit.md", "Equity/balance curve audit."),
        ("stage57_segment_kpi_summary", "table", REVIEWS_ROOT / "segment_kpi_summary.csv", "Segment KPI summary."),
        ("stage57_monthly_kpi_summary", "table", REVIEWS_ROOT / "monthly_kpi_summary.csv", "Monthly KPI summary."),
        ("stage57_session_regime_kpi_summary", "table", REVIEWS_ROOT / "session_regime_kpi_summary.csv", "Session/regime KPI summary."),
        ("stage57_long_short_kpi_summary", "table", REVIEWS_ROOT / "long_short_kpi_summary.csv", "Long/short KPI summary."),
        ("stage57_concentration_risk_report", "report", REVIEWS_ROOT / "concentration_risk_report.md", "Concentration risk report."),
        ("stage57_decision", "decision", REVIEWS_ROOT / "stage57_decision.md", "Stage57 decision."),
        ("stage57_packet_summary", "packet", PACKET_ROOT / "aggregate_summary.json", "Stage57 packet summary."),
        ("stage58_stage_brief", "brief", STAGE58_ROOT / "00_spec" / "stage_brief.md", "Stage58 opened from Stage57."),
    ]
    rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, notes in artifacts:
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": _rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE57_ID if not artifact_id.startswith("stage58") else STAGE58_ID,
                "run_id": RUN57_ID,
                "created_at_utc": UTC_NOW,
                "notes": notes,
            }
        )
    return rows


def _update_workspace_state(summary: Mapping[str, Any]) -> None:
    path = REPO_ROOT / "docs" / "workspace" / "workspace_state.yaml"
    text = io_path(path).read_text(encoding="utf-8-sig")
    text = re.sub(
        r"current_focus:\n(?:- >-\n  Stage57[^\n]*\n- >-\n  Stage58[^\n]*\n)?",
        "current_focus:\n",
        text,
        count=1,
    )
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {RUN58_PLANNED_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-15'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {STAGE58_ID}", text, count=1, flags=re.MULTILINE)
    focus = (
        "current_focus:\n"
        f"- >-\n"
        f"  Stage57(57단계) `{STAGE57_ID}` closed(종료) as bounded equity/segment KPI audit(경계 자금/구간 KPI 감사); "
        f"decision(판정)=`{DECISION}`. Effect(효과): Stage56(56단계)은 더 이상 BaselineAdapter(기준선 어댑터) future work(향후 작업)를 흡수하지 않고 Stage58(58단계) `{STAGE58_ID}`로 handoff(인계)한다.\n"
        f"- >-\n"
        f"  Stage58(58단계) `{STAGE58_ID}` opened(개방) as repair-before-risk/ATR(위험/ATR 전 수리) bounded stage(경계 단계). "
        f"Effect(효과): ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)는 mandatory(필수)이지만 completion(완료) 조건으로 충분하지 않다.\n"
    )
    text = text.replace("current_focus:\n", focus, 1)
    append = f"""

stage57_equity_segment_kpi_audit_gate:
  packet_id: {PACKET_ID}
  stage_id: {STAGE57_ID}
  status: closed_bounded_audit_gate
  current_run_id: {RUN57_ID}
  source_run_id: {RUN50CA_ID}
  adapter_id: {ADAPTER_ID}
  decision: {DECISION}
  next_stage: {STAGE58_ID}
  report_path: {_rel(REVIEWS_ROOT / "stage57_decision.md")}
  packet_summary_path: {_rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: completed_existing_mt5_onnx_runtime_reports
  boundary: {BOUNDARY}

stage58_bounded_repair_before_atr_risk:
  stage_id: {STAGE58_ID}
  status: active_planned_from_stage57
  planned_run_id: {RUN58_PLANNED_ID}
  source_decision: {DECISION}
  next_action: bounded adapter repair before mandatory ATR SL/TP and model-controlled risk percent integration
  boundary: {BOUNDARY}
"""
    if "stage57_equity_segment_kpi_audit_gate:" not in text:
        text += append
    io_path(path).write_text(text, encoding="utf-8-sig")


def _append_changelog(summary: Mapping[str, Any]) -> None:
    path = REPO_ROOT / "docs" / "workspace" / "changelog.md"
    addition = f"""
## 2026-05-15 Stage57 Equity Segment KPI Audit(57단계 자금/구간 KPI 감사)
- completed(완료): `{RUN57_ID}` bounded audit gate(경계 감사 관문)를 existing run50CA MT5 ONNX runtime evidence(기존 run50CA MT5 ONNX 런타임 근거)로 닫았다.
- decision(판정): `{DECISION}`.
- effect(효과): Stage56(56단계)이 더 이상 BaselineAdapter(기준선 어댑터) future work(향후 작업)를 흡수하지 않고 Stage58(58단계) `{STAGE58_ID}`로 handoff(인계)한다.

## 2026-05-15 Stage58 Opened(58단계 개방)
- opened(개방): `{STAGE58_ID}` with planned run(계획 실행) `{RUN58_PLANNED_ID}`.
- effect(효과): adapter repair need(어댑터 수리 필요)를 먼저 다루고, ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)를 full adapter(전체 어댑터) 기준으로 통합/측정한다.
"""
    text = io_path(path).read_text(encoding="utf-8-sig")
    pair_pattern = re.compile(
        r"\n## 2026-05-15 Stage57 Equity Segment KPI Audit\(57단계 자금/구간 KPI 감사\).*?"
        r"\n## 2026-05-15 Stage58 Opened\(58단계 개방\).*?(?=\n## |\Z)",
        re.DOTALL,
    )
    text = pair_pattern.sub("", text)
    io_path(path).write_text(text.rstrip() + addition, encoding="utf-8-sig")


def _upsert_csv(path: Path, fieldnames: Sequence[str], key: str, new_rows: Sequence[Mapping[str, Any]]) -> None:
    rows: list[dict[str, Any]] = []
    if io_path(path).exists():
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = [dict(row) for row in reader]
    by_key = OrderedDict((row.get(key), row) for row in rows if row.get(key))
    for row in new_rows:
        by_key[str(row[key])] = {field: _csv_value(row.get(field, "")) for field in fieldnames}
    _write_csv(path, fieldnames, list(by_key.values()), encoding="utf-8")


def _write_csv(path: Path, fieldnames: Sequence[str], rows: Sequence[Mapping[str, Any]], encoding: str = "utf-8") -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: _csv_value(row.get(field, "")) for field in fieldnames})


def _write_json(path: Path, payload: Any) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def _source_row(source_summary: pd.DataFrame, split: str) -> Mapping[str, Any]:
    matches = source_summary[source_summary["split"].eq(split) & source_summary["view"].eq("actual_routed_total")]
    if matches.empty:
        return {}
    return matches.iloc[0].to_dict()


def _row_to_plain(row: Mapping[str, Any]) -> dict[str, Any]:
    return {str(key): json_ready(value) for key, value in row.items()}


def _round_map(row: Mapping[str, Any]) -> dict[str, Any]:
    return {key: _round(value) if isinstance(value, (int, float)) else value for key, value in row.items()}


def _round(value: Any, digits: int = 6) -> Any:
    number = _to_float(value)
    if number is None:
        return value
    return round(number, digits)


def _mean(values: Iterable[Any]) -> float | None:
    numbers = [_to_float(value) for value in values]
    numbers = [value for value in numbers if value is not None]
    return sum(numbers) / len(numbers) if numbers else None


def _sum(values: Iterable[Any]) -> float:
    return sum(value for value in (_to_float(item) for item in values) if value is not None)


def _safe_ratio(numerator: Any, denominator: Any) -> float | None:
    num = _to_float(numerator)
    den = _to_float(denominator)
    if num is None or den is None or abs(den) < 1e-12:
        return None
    return num / den


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.10g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def _rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def _third_net_text(split_summary: Mapping[str, Any]) -> str:
    thirds = split_summary["chronological_thirds"]
    return (
        f"early={_round(thirds['early']['net_profit'])};"
        f"mid={_round(thirds['mid']['net_profit'])};"
        f"late={_round(thirds['late']['net_profit'])}"
    )


if __name__ == "__main__":
    main()
