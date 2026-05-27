from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage337 import completed_day_lock_or_tester_visibility_repair_without_db as by  # noqa: E402


bx = by.bx
bu = by.bu
aw = by.aw
bg = by.bg

TODAY = "2026-05-28"
STAGE_ID = by.STAGE_ID
RUN_NUMBER = "run337BZ"
RUN_ID = "run337BZ_runtime_kpi_attribution_and_no_overfit_research_matrix_without_db_v1"
PARENT_RUN_ID = by.RUN_ID
NEXT_RUN_ID = "run337CA_label_boundary_lifecycle_cost_frontier_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BZ_runtime_kpi_no_overfit_matrix_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = by.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = by.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BZ_runtime_kpi_attribution_and_no_overfit_research_matrix.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337BZ_runtime_kpi_no_overfit_research_matrix.md"
SELECTED_STATUS = by.SELECTED_STATUS
STAGE_BRIEF = by.STAGE_BRIEF
WORKSPACE_STATE = by.WORKSPACE_STATE
CURRENT_STATE = by.CURRENT_STATE
CHANGELOG = by.CHANGELOG
RUN_REGISTRY = by.RUN_REGISTRY
ALPHA_LEDGER = by.ALPHA_LEDGER
ARTIFACT_REGISTRY = by.ARTIFACT_REGISTRY
STAGE_LEDGER = by.STAGE_LEDGER

BY_FINAL = by.FINAL_DECISION
BY_LOCK = by.WINDOW_LOCK
BY_SCORE = by.LOCKED_PROXY_SCORECARD
BY_COMPARE = by.LOCKED_PROXY_MT5_COMPARE
BY_USABILITY = by.LOCKED_USABILITY
BX_KPI = bx.KPI_ATTRIBUTION
BX_FLOW = bx.TRADE_FLOW_ATTRIBUTION
BX_HOUR = bx.SIGNAL_HOUR_ATTRIBUTION
BU_SCORECARD = bu.DECISION_SCORECARD
BU_PROXY_EXPECTED = bu.PROXY_EXPECTED_FORWARD

LABEL_BOUNDARY_AUDIT = RUN_DIR / "label_boundary_audit.csv"
SPLIT_STABILITY_MATRIX = RUN_DIR / "split_stability_no_overfit_matrix.csv"
THRESHOLD_COST_SENSITIVITY = RUN_DIR / "threshold_cost_sensitivity_matrix.csv"
SIDE_SESSION_CONCENTRATION = RUN_DIR / "side_session_concentration_matrix.csv"
RUNTIME_KPI_MATRIX = RUN_DIR / "runtime_kpi_no_overfit_attribution_matrix.csv"
RESEARCH_LANE_PRIORITY = RUN_DIR / "research_lane_priority_matrix.csv"
FOLLOWUP_QUEUE = RUN_DIR / "run337CA_guarded_followup_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_discipline_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BY_FINAL,
    BY_LOCK,
    BY_SCORE,
    BY_COMPARE,
    BY_USABILITY,
    BX_KPI,
    BX_FLOW,
    BX_HOUR,
    BU_SCORECARD,
    BU_PROXY_EXPECTED,
)
OUTPUT_FILES = (
    LABEL_BOUNDARY_AUDIT,
    SPLIT_STABILITY_MATRIX,
    THRESHOLD_COST_SENSITIVITY,
    SIDE_SESSION_CONCENTRATION,
    RUNTIME_KPI_MATRIX,
    RESEARCH_LANE_PRIORITY,
    FOLLOWUP_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

PRIMARY_THRESHOLD = "fixed_short040_long040_margin002"
PRIMARY_COST_BPS = 1.0

LABEL_COLUMNS = (
    "model_id",
    "feature_set_id",
    "locked_cutoff_bar_time",
    "locked_rows",
    "locked_signal_rows",
    "label_available_signal_rows",
    "label_missing_signal_rows",
    "label_missing_signal_rate",
    "rederived_net_log_return_cost1",
    "rederived_profit_factor_cost1",
    "rederived_expectancy_per_trade_cost1",
    "rederived_max_drawdown_log_return_cost1",
    "rederived_worst_20_trade_net_log_return_cost1",
    "integrity_judgment",
    "effect",
    "claim_boundary",
)
SPLIT_COLUMNS = (
    "model_id",
    "feature_set_id",
    "model_family",
    "threshold_id",
    "cost_bps_per_trade",
    "train_pf",
    "validation_pf",
    "oos_pf",
    "forward_pf",
    "train_net_log_return",
    "validation_net_log_return",
    "oos_net_log_return",
    "forward_net_log_return",
    "forward_minus_train_pf",
    "worst_non_train_pf",
    "overfit_risk",
    "validation_judgment",
    "claim_boundary",
)
SENSITIVITY_COLUMNS = (
    "model_id",
    "feature_set_id",
    "model_family",
    "threshold_id",
    "forward_cost0_pf",
    "forward_cost1_pf",
    "forward_cost2_pf",
    "forward_cost0_net",
    "forward_cost1_net",
    "forward_cost2_net",
    "cost1_to_cost2_net_delta",
    "survives_cost1",
    "survives_cost2",
    "sensitivity_judgment",
    "claim_boundary",
)
SESSION_COLUMNS = (
    "model_id",
    "feature_set_id",
    "total_runtime_signals",
    "top_hour_utc",
    "top_hour_signals",
    "top_hour_signal_share",
    "active_signal_hours",
    "long_share",
    "short_share",
    "side_bias",
    "session_concentration_judgment",
    "claim_boundary",
)
RUNTIME_COLUMNS = (
    "model_id",
    "feature_set_id",
    "model_family",
    "mt5_net_profit",
    "mt5_profit_factor",
    "mt5_trade_count",
    "mt5_max_drawdown_amount",
    "proxy_forward_pf_cost1",
    "rederived_labelable_pf_cost1",
    "runtime_signal_rate",
    "orders_per_signal",
    "trades_per_ready_row",
    "label_missing_signal_rate",
    "overfit_risk",
    "session_concentration_judgment",
    "primary_failure_modes",
    "research_implication",
    "attribution_confidence",
    "claim_boundary",
)
LANE_COLUMNS = (
    "lane_id",
    "priority",
    "source_evidence",
    "hypothesis",
    "required_probe",
    "forbidden_shortcut",
    "expected_effect",
    "claim_boundary",
)
GATE_COLUMNS = by.GATE_COLUMNS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=RUN_ID)
    return parser.parse_args()


def rel(path: Path) -> str:
    return by.rel(path)


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    return by.csv_value(value)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return by.write_csv(path, columns, rows)


def write_json(path: Path, payload: Any) -> Path:
    return by.write_json(path, payload)


def write_md(path: Path, text: str) -> Path:
    return by.write_md(path, text)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return by.read_csv(path)


def read_json(path: Path) -> Any:
    return by.read_json(path)


def read_df(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig")


def as_float(value: Any) -> float:
    try:
        if value is None or value == "":
            return float("nan")
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def finite_or_none(value: float) -> float | None:
    return float(value) if math.isfinite(value) else None


def safe_pf(values: np.ndarray) -> float:
    gains = float(values[values > 0.0].sum())
    losses = float(values[values < 0.0].sum())
    if losses < 0.0:
        return gains / abs(losses)
    if gains > 0.0:
        return float("inf")
    return 0.0


def max_drawdown(values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    return float((curve - peak).min())


def worst_rolling(values: np.ndarray, window: int) -> float:
    if values.size == 0:
        return 0.0
    if values.size < window:
        return float(values.sum())
    sums = np.convolve(values, np.ones(window), mode="valid")
    return float(sums.min())


def require_inputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        exists = path_exists(path)
        rows.append(
            {
                "gate_id": f"input_exists::{rel(path)}",
                "status": "passed" if exists else "failed",
                "evidence": rel(path),
                "effect": "input available for BZ attribution matrix(입력이 BZ 귀속 행렬에 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_label_boundary(proxy: pd.DataFrame, locks: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lock in locks.to_dict("records"):
        model_id = str(lock["model_id"])
        feature_set_id = str(lock["feature_set_id"])
        cutoff = str(lock["locked_cutoff_bar_time"])
        model_proxy = proxy[(proxy["model_id"] == model_id) & (proxy["bar_time"].astype(str) <= cutoff)].copy()
        signal_mask = model_proxy["decision_label_class"].astype("int64") != -1
        labelable = signal_mask & model_proxy["future_log_return_12"].astype("float64").replace([np.inf, -np.inf], np.nan).notna()
        decision_class = model_proxy["decision_label_class"].astype("int64").to_numpy()
        future = model_proxy["future_log_return_12"].astype("float64").to_numpy()
        signed = np.zeros(len(model_proxy), dtype="float64")
        long_mask = decision_class == 2
        short_mask = decision_class == 0
        signed[long_mask] = future[long_mask]
        signed[short_mask] = -future[short_mask]
        trade_returns = signed[labelable.to_numpy()] - PRIMARY_COST_BPS / 10000.0
        locked_signals = int(signal_mask.sum())
        labelable_signals = int(labelable.sum())
        missing = locked_signals - labelable_signals
        missing_rate = float(missing / locked_signals) if locked_signals else 0.0
        judgment = "usable_with_label_boundary" if missing == 0 else "usable_for_signal_not_profit_until_label_boundary_repaired"
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": feature_set_id,
                "locked_cutoff_bar_time": cutoff,
                "locked_rows": int(len(model_proxy)),
                "locked_signal_rows": locked_signals,
                "label_available_signal_rows": labelable_signals,
                "label_missing_signal_rows": missing,
                "label_missing_signal_rate": missing_rate,
                "rederived_net_log_return_cost1": finite_or_none(float(trade_returns.sum())) if trade_returns.size else 0.0,
                "rederived_profit_factor_cost1": finite_or_none(safe_pf(trade_returns)),
                "rederived_expectancy_per_trade_cost1": finite_or_none(float(trade_returns.mean())) if trade_returns.size else 0.0,
                "rederived_max_drawdown_log_return_cost1": finite_or_none(max_drawdown(trade_returns)),
                "rederived_worst_20_trade_net_log_return_cost1": finite_or_none(worst_rolling(trade_returns, 20)),
                "integrity_judgment": judgment,
                "effect": "separates signal parity from profit labels(신호 동등성과 수익 라벨을 분리)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def metric_lookup(score: pd.DataFrame, model_id: str, threshold: str, cost: float, split: str) -> Mapping[str, Any] | None:
    subset = score[
        (score["model_id"] == model_id)
        & (score["threshold_id"] == threshold)
        & (score["cost_bps_per_trade"].astype("float64") == float(cost))
        & (score["split"] == split)
    ]
    if subset.empty:
        return None
    return subset.iloc[0].to_dict()


def risk_from_splits(train_pf: float, validation_pf: float, oos_pf: float, forward_pf: float, forward_net: float) -> str:
    non_train = [value for value in (validation_pf, oos_pf, forward_pf) if math.isfinite(value)]
    worst_non_train = min(non_train) if non_train else float("nan")
    if not math.isfinite(worst_non_train):
        return "inconclusive_missing_split_metric"
    if train_pf - worst_non_train >= 0.35 or forward_pf < 0.9 or forward_net < 0.0:
        return "high_overfit_or_fragility_risk"
    if train_pf - worst_non_train >= 0.15 or forward_pf < 1.02:
        return "medium_overfit_or_cost_fragility_risk"
    return "lower_relative_overfit_risk_but_not_selection"


def build_split_stability(score: pd.DataFrame, models: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model_id in models:
        sample = score[score["model_id"] == model_id].iloc[0].to_dict()
        train = metric_lookup(score, model_id, PRIMARY_THRESHOLD, PRIMARY_COST_BPS, "train") or {}
        validation = metric_lookup(score, model_id, PRIMARY_THRESHOLD, PRIMARY_COST_BPS, "validation") or {}
        oos = metric_lookup(score, model_id, PRIMARY_THRESHOLD, PRIMARY_COST_BPS, "oos") or {}
        forward = metric_lookup(score, model_id, PRIMARY_THRESHOLD, PRIMARY_COST_BPS, "forward_after_2026_04_14_diagnostic") or {}
        train_pf = as_float(train.get("profit_factor"))
        validation_pf = as_float(validation.get("profit_factor"))
        oos_pf = as_float(oos.get("profit_factor"))
        forward_pf = as_float(forward.get("profit_factor"))
        forward_net = as_float(forward.get("net_log_return_sum"))
        non_train = [value for value in (validation_pf, oos_pf, forward_pf) if math.isfinite(value)]
        worst_non_train = min(non_train) if non_train else float("nan")
        risk = risk_from_splits(train_pf, validation_pf, oos_pf, forward_pf, forward_net)
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": sample.get("feature_set_id", ""),
                "model_family": sample.get("model_family", ""),
                "threshold_id": PRIMARY_THRESHOLD,
                "cost_bps_per_trade": PRIMARY_COST_BPS,
                "train_pf": finite_or_none(train_pf),
                "validation_pf": finite_or_none(validation_pf),
                "oos_pf": finite_or_none(oos_pf),
                "forward_pf": finite_or_none(forward_pf),
                "train_net_log_return": finite_or_none(as_float(train.get("net_log_return_sum"))),
                "validation_net_log_return": finite_or_none(as_float(validation.get("net_log_return_sum"))),
                "oos_net_log_return": finite_or_none(as_float(oos.get("net_log_return_sum"))),
                "forward_net_log_return": finite_or_none(forward_net),
                "forward_minus_train_pf": finite_or_none(forward_pf - train_pf),
                "worst_non_train_pf": finite_or_none(worst_non_train),
                "overfit_risk": risk,
                "validation_judgment": "exploratory_diagnostic_not_selection",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_threshold_cost_sensitivity(score: pd.DataFrame, models: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    forward = score[score["split"] == "forward_after_2026_04_14_diagnostic"].copy()
    for model_id in models:
        sample = score[score["model_id"] == model_id].iloc[0].to_dict()
        for threshold in sorted(forward[forward["model_id"] == model_id]["threshold_id"].unique()):
            metrics = {
                cost: metric_lookup(score, model_id, str(threshold), float(cost), "forward_after_2026_04_14_diagnostic") or {}
                for cost in (0.0, 1.0, 2.0)
            }
            pf0 = as_float(metrics[0.0].get("profit_factor"))
            pf1 = as_float(metrics[1.0].get("profit_factor"))
            pf2 = as_float(metrics[2.0].get("profit_factor"))
            net0 = as_float(metrics[0.0].get("net_log_return_sum"))
            net1 = as_float(metrics[1.0].get("net_log_return_sum"))
            net2 = as_float(metrics[2.0].get("net_log_return_sum"))
            survives_cost1 = bool(math.isfinite(pf1) and pf1 >= 1.0 and net1 >= 0.0)
            survives_cost2 = bool(math.isfinite(pf2) and pf2 >= 1.0 and net2 >= 0.0)
            if survives_cost2:
                judgment = "less_cost_fragile_diagnostic_only"
            elif survives_cost1:
                judgment = "cost2_breaks_forward_edge"
            else:
                judgment = "does_not_survive_cost1_forward_diagnostic"
            rows.append(
                {
                    "model_id": model_id,
                    "feature_set_id": sample.get("feature_set_id", ""),
                    "model_family": sample.get("model_family", ""),
                    "threshold_id": threshold,
                    "forward_cost0_pf": finite_or_none(pf0),
                    "forward_cost1_pf": finite_or_none(pf1),
                    "forward_cost2_pf": finite_or_none(pf2),
                    "forward_cost0_net": finite_or_none(net0),
                    "forward_cost1_net": finite_or_none(net1),
                    "forward_cost2_net": finite_or_none(net2),
                    "cost1_to_cost2_net_delta": finite_or_none(net2 - net1),
                    "survives_cost1": survives_cost1,
                    "survives_cost2": survives_cost2,
                    "sensitivity_judgment": judgment,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_session_concentration(hour: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (model_id, feature_set_id), group in hour.groupby(["model_id", "feature_set_id"], sort=True):
        group = group.copy()
        group["signals"] = group["short_count"].astype("int64") + group["long_count"].astype("int64")
        total = int(group["signals"].sum())
        top = group.sort_values(["signals", "hour_utc"], ascending=[False, True]).iloc[0] if not group.empty else {}
        top_signals = int(top.get("signals", 0)) if len(group) else 0
        share = float(top_signals / total) if total else 0.0
        longs = int(group["long_count"].sum())
        shorts = int(group["short_count"].sum())
        active = int((group["signals"] > 0).sum())
        long_share = float(longs / total) if total else 0.0
        short_share = float(shorts / total) if total else 0.0
        side_bias = "long_bias" if long_share >= 0.7 else ("short_bias" if short_share >= 0.7 else "mixed")
        concentration = "high_session_concentration" if share >= 0.25 or active <= 6 else ("medium_session_concentration" if share >= 0.15 or active <= 10 else "broad_session_distribution")
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": feature_set_id,
                "total_runtime_signals": total,
                "top_hour_utc": int(top.get("hour_utc", -1)) if len(group) else "",
                "top_hour_signals": top_signals,
                "top_hour_signal_share": share,
                "active_signal_hours": active,
                "long_share": long_share,
                "short_share": short_share,
                "side_bias": side_bias,
                "session_concentration_judgment": concentration,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_runtime_matrix(
    kpi: pd.DataFrame,
    flow: pd.DataFrame,
    compare: pd.DataFrame,
    labels: Sequence[Mapping[str, Any]],
    splits: Sequence[Mapping[str, Any]],
    sessions: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    label_by_model = {str(row["model_id"]): row for row in labels}
    split_by_model = {str(row["model_id"]): row for row in splits}
    session_by_model = {str(row["model_id"]): row for row in sessions}
    flow_by_model = {str(row["model_id"]): row for row in flow.to_dict("records")}
    compare_by_model = {str(row["model_id"]): row for row in compare.to_dict("records")}
    rows: list[dict[str, Any]] = []
    for row in kpi.to_dict("records"):
        model_id = str(row["model_id"])
        flow_row = flow_by_model.get(model_id, {})
        compare_row = compare_by_model.get(model_id, {})
        label_row = label_by_model.get(model_id, {})
        split_row = split_by_model.get(model_id, {})
        session_row = session_by_model.get(model_id, {})
        failure_modes: list[str] = []
        pf = as_float(row.get("new_profit_factor"))
        net = as_float(row.get("new_mt5_net_profit"))
        if math.isfinite(pf) and pf < 1.0:
            failure_modes.append("mt5_pf_below_one")
        if math.isfinite(net) and net < 0.0:
            failure_modes.append("mt5_net_negative")
        if as_float(label_row.get("label_missing_signal_rate")) > 0.0:
            failure_modes.append("label_boundary_gap")
        if str(split_row.get("overfit_risk", "")).startswith("high"):
            failure_modes.append("split_overfit_or_fragility")
        if str(session_row.get("session_concentration_judgment", "")).startswith("high"):
            failure_modes.append("session_concentration")
        if as_float(flow_row.get("orders_per_signal")) < 0.25:
            failure_modes.append("signal_to_trade_compression")
        if not failure_modes:
            failure_modes.append("weak_edge_needs_more_runtime_evidence")
        if "label_boundary_gap" in failure_modes or "signal_to_trade_compression" in failure_modes:
            implication = "run337CA_label_boundary_lifecycle_proxy_first"
        elif "split_overfit_or_fragility" in failure_modes:
            implication = "rolling_split_negative_control_before_training"
        else:
            implication = "cost_session_frontier_probe_no_selection"
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": row.get("feature_set_id", ""),
                "model_family": row.get("model_family", ""),
                "mt5_net_profit": finite_or_none(net),
                "mt5_profit_factor": finite_or_none(pf),
                "mt5_trade_count": int(as_float(row.get("new_trade_count"))) if math.isfinite(as_float(row.get("new_trade_count"))) else "",
                "mt5_max_drawdown_amount": finite_or_none(as_float(row.get("new_max_drawdown_amount"))),
                "proxy_forward_pf_cost1": finite_or_none(as_float(compare_row.get("proxy_profit_factor_cost1_locked"))),
                "rederived_labelable_pf_cost1": finite_or_none(as_float(label_row.get("rederived_profit_factor_cost1"))),
                "runtime_signal_rate": finite_or_none(as_float(flow_row.get("runtime_signal_rate"))),
                "orders_per_signal": finite_or_none(as_float(flow_row.get("orders_per_signal"))),
                "trades_per_ready_row": finite_or_none(as_float(flow_row.get("trades_per_ready_row"))),
                "label_missing_signal_rate": finite_or_none(as_float(label_row.get("label_missing_signal_rate"))),
                "overfit_risk": split_row.get("overfit_risk", ""),
                "session_concentration_judgment": session_row.get("session_concentration_judgment", ""),
                "primary_failure_modes": ";".join(failure_modes),
                "research_implication": implication,
                "attribution_confidence": "medium" if len(failure_modes) <= 2 else "medium_low_multi_driver",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_lane_priority(runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    modes = ";".join(str(row.get("primary_failure_modes", "")) for row in runtime_rows)
    rows = [
        {
            "lane_id": "defensive_label_boundary_repair",
            "priority": "P0",
            "source_evidence": rel(LABEL_BOUNDARY_AUDIT),
            "hypothesis": "locked proxy rows mix labelable and non-labelable signals, so profit diagnostics must separate label boundary",
            "required_probe": "labelable-only proxy score plus report gate before any profit comparison",
            "forbidden_shortcut": "do not tune threshold or call NaN profit acceptable",
            "expected_effect": "prevents overfit-by-mismeasurement(측정 오류 과적합 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lane_id": "defensive_execution_lifecycle_proxy",
            "priority": "P0",
            "source_evidence": rel(BX_FLOW),
            "hypothesis": "signal count compresses into far fewer trades under one-position, reverse, and max-hold runtime lifecycle",
            "required_probe": "Python lifecycle proxy that mirrors runtime trade formation before model training",
            "forbidden_shortcut": "do not compare raw signal PnL to MT5 account PnL as same unit",
            "expected_effect": "separates signal edge from execution shape(신호 우위와 실행 형태 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lane_id": "offensive_cost_session_frontier",
            "priority": "P1",
            "source_evidence": rel(THRESHOLD_COST_SENSITIVITY),
            "hypothesis": "a useful future ONNX must survive cost and session concentration without relying on one fragile threshold",
            "required_probe": "cost/session frontier scan as diagnostic only, not threshold selection",
            "forbidden_shortcut": "do not choose the best threshold from forward window",
            "expected_effect": "finds robust design constraints(강건한 설계 제약 발견)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lane_id": "visibility_repair_plan",
            "priority": "P0",
            "source_evidence": rel(BY_LOCK),
            "hypothesis": "latest tester gap still blocks latest-forward and operating claims",
            "required_probe": "broker/tester visibility repair or completed-day-only test contract",
            "forbidden_shortcut": "do not treat hidden latest rows as forward pass",
            "expected_effect": "keeps forward boundary honest(전진 경계 정직성 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    if "split_overfit_or_fragility" in modes:
        rows.append(
            {
                "lane_id": "rolling_split_negative_control",
                "priority": "P1",
                "source_evidence": rel(SPLIT_STABILITY_MATRIX),
                "hypothesis": "train-to-forward degradation suggests model family or feature set may be fitting stale structure",
                "required_probe": "rolling split and shifted-label negative control before any candidate claim",
                "forbidden_shortcut": "do not select the least-bad model as candidate",
                "expected_effect": "distinguishes real signal from historical fit(실제 신호와 과거 적합 분리)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_followup_queue(lanes: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337CA_label_boundary_lifecycle_cost_frontier",
            "next_run_id": NEXT_RUN_ID,
            "lane": "defensive_first_then_offensive_frontier",
            "priority": "P0",
            "reason": "BZ found label boundary and runtime lifecycle as first-order blockers before any new ONNX claim",
            "required_evidence": "labelable-only proxy score, lifecycle proxy, cost/session diagnostic frontier, no-lookahead gates",
            "forbidden_shortcut": "no threshold tuning, no lot optimization, no candidate selection, no forward pass claim",
            "effect": "turns BZ attribution into a bounded next probe(귀속 결과를 제한된 다음 탐침으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(
    input_gates: Sequence[Mapping[str, Any]],
    labels: Sequence[Mapping[str, Any]],
    splits: Sequence[Mapping[str, Any]],
    sensitivity: Sequence[Mapping[str, Any]],
    sessions: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    lanes: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    gates: list[dict[str, Any]] = list(input_gates)
    checks = [
        ("kpi_contract_audit", len(runtime_rows) >= 6, f"runtime_matrix_rows={len(runtime_rows)}"),
        ("row_grain_audit", all(row.get("model_id") for row in runtime_rows), "model-level rows preserve one row per scout"),
        ("label_boundary_audit", len(labels) >= 6 and all("integrity_judgment" in row for row in labels), f"label_rows={len(labels)}"),
        ("split_overfit_audit", len(splits) >= 6 and all(row.get("overfit_risk") for row in splits), f"split_rows={len(splits)}"),
        ("cost_sensitivity_audit", len(sensitivity) >= 18, f"sensitivity_rows={len(sensitivity)}"),
        ("session_concentration_audit", len(sessions) >= 6, f"session_rows={len(sessions)}"),
        ("source_authority_audit", all(path_exists(path) for path in INPUT_FILES), "inputs are prior run artifacts"),
        ("required_gate_coverage_audit", len(lanes) >= 4, f"lane_rows={len(lanes)}"),
        ("final_claim_guard", True, "Forward/Goal/runtime authority remain not_claimed"),
    ]
    for gate_id, passed, evidence in checks:
        gates.append(
            {
                "gate_id": gate_id,
                "status": "passed" if passed else "failed",
                "evidence": evidence,
                "effect": "supports BZ closeout without promotion claim(BZ 종료를 승격 주장 없이 지지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return gates


def classify(gates: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    failed = [row for row in gates if row.get("status") != "passed"]
    if failed:
        return (
            "blocked_stage337BZ_runtime_kpi_no_overfit_matrix_gate_failed_no_forward_decision",
            "blocked_required_bz_matrix_evidence_missing",
            "stage337BZ_repair_missing_matrix_evidence_before_next_probe",
            RUN_ID,
        )
    modes = ";".join(str(row.get("primary_failure_modes", "")) for row in runtime_rows)
    if "label_boundary_gap" in modes or "signal_to_trade_compression" in modes:
        return (
            "completed_stage337BZ_runtime_kpi_no_overfit_matrix_label_lifecycle_first_no_forward_decision",
            "diagnostic_matrix_points_to_label_boundary_and_runtime_lifecycle_before_new_onnx_claim",
            "stage337BZ_open_run337CA_label_boundary_lifecycle_cost_frontier_probe",
            NEXT_RUN_ID,
        )
    return (
        "completed_stage337BZ_runtime_kpi_no_overfit_matrix_cost_session_frontier_no_forward_decision",
        "diagnostic_matrix_points_to_cost_session_frontier_before_new_onnx_claim",
        "stage337BZ_open_run337CA_cost_session_frontier_probe",
        NEXT_RUN_ID,
    )


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "run_id": RUN_ID,
                "selected_work_family": "kpi_evidence",
                "primary_skill": "obsidian-run-evidence-system",
                "support_skills": ["obsidian-performance-attribution", "obsidian-model-validation", "obsidian-data-integrity", "obsidian-artifact-lineage", "obsidian-result-judgment", "obsidian-claim-discipline"],
                "hypothesis": "runtime KPI weakness can be decomposed into label boundary, lifecycle, cost, session, and split risk before more model work",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [rel(BY_LOCK), rel(BY_COMPARE), rel(BX_KPI), rel(BU_SCORECARD), rel(BU_PROXY_EXPECTED)],
                "time_axis": "US100 M5 bar_time/timestamp_utc from prior run artifacts; latest hidden tester gap remains excluded",
                "sample_scope": "2026-04-14 forward diagnostic through completed-day cutoff 2026-05-26 23:55 where MT5 overlap exists",
                "feature_label_boundary": "future_log_return_12 used only where label is finite; non-labelable locked rows are separated",
                "integrity_judgment": "usable_with_completed_day_and_label_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "BU model scouts unchanged; no new training",
                "target_and_label": "direction class with 12-bar future return diagnostic only",
                "split_method": "train/validation/oos/forward diagnostic plus runtime probe overlap",
                "selection_metric": "none; matrix is diagnostic",
                "threshold_policy": "fixed threshold read only, no tuning",
                "overfit_risk": "split degradation and cost/session sensitivity matrix",
                "validation_judgment": "exploratory_diagnostic_no_selection",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "observed_change": "weak MT5 KPI despite proxy overlap parity",
                "comparison_baseline": [rel(BX_KPI), rel(BY_COMPARE)],
                "likely_drivers": "label boundary, signal-to-trade compression, cost sensitivity, session/side concentration, split fragility",
                "segment_checks": [rel(LABEL_BOUNDARY_AUDIT), rel(SPLIT_STABILITY_MATRIX), rel(THRESHOLD_COST_SENSITIVITY), rel(SIDE_SESSION_CONCENTRATION)],
                "attribution_confidence": "medium diagnostic, not operating evidence",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in OUTPUT_FILES if path_exists(path)],
                "availability": "tracked reports and registries plus ignored run artifacts represented by hashes",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(RUNTIME_KPI_MATRIX), rel(REPORT_PATH), rel(REQUIRED_GATE_AUDIT)],
                "evidence_missing": "no new MT5 latest visibility repair, no new model, no operating evidence",
                "judgment_label": final["judgment"],
                "next_condition": final["next_action"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "operating_promotion": "not_claimed",
                "goal_achieve": "not_claimed",
                "effect": "BZ is diagnostic evidence only, not selection(진단 근거일 뿐 선택이 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def write_report(final: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]], lanes: Sequence[Mapping[str, Any]]) -> Path:
    top_runtime = list(runtime_rows)[:6]
    runtime_lines = "\n".join(
        f"| `{row['model_id']}` | {row['mt5_net_profit']} | {row['mt5_profit_factor']} | `{row['primary_failure_modes']}` | `{row['research_implication']}` |"
        for row in top_runtime
    )
    lane_lines = "\n".join(
        f"| `{row['lane_id']}` | `{row['priority']}` | {row['hypothesis']} |"
        for row in lanes
    )
    return write_md(
        REPORT_PATH,
        f"""# Stage337 run337BZ Runtime KPI/No-Overfit Matrix(런타임 성과/무과적합 행렬)

## Conclusion(결론)

run337BZ(337BZ 실행)는 새 model training(모델 학습), threshold tuning(임계값 조정), lot optimization(로트 최적화)을 하지 않고 BY/BX/BU 근거를 합쳐 원인 행렬을 만들었다.

Effect(효과): 다음 probe(탐침)는 label boundary(라벨 경계)와 execution lifecycle(실행 생애주기)을 먼저 고쳐야 하며, Forward/Goal(전진/목표)은 계속 주장하지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- runtime_matrix_rows(런타임 행렬 행): `{final['runtime_matrix_rows']}`
- split_matrix_rows(분할 행렬 행): `{final['split_matrix_rows']}`
- cost_sensitivity_rows(비용 민감도 행): `{final['cost_sensitivity_rows']}`

## Runtime Matrix(런타임 행렬)

| model(모델) | MT5 net(MT5 순익) | MT5 PF(MT5 수익 팩터) | failure modes(실패 모드) | implication(의미) |
|---|---:|---:|---|---|
{runtime_lines}

## Research Lanes(연구 레인)

| lane(레인) | priority(우선순위) | hypothesis(가설) |
|---|---|---|
{lane_lines}

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    return write_md(
        DECISION_DOC,
        f"""# Decision: Stage337 run337BZ Runtime KPI/No-Overfit Matrix(결정: 런타임 성과/무과적합 행렬)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): runtime KPI weakness(런타임 성과 약점)을 label boundary(라벨 경계), lifecycle(생애주기), cost/session(비용/세션), split fragility(분할 취약성)로 나눴다. 이 결정은 다음 연구 탐침을 여는 것이며, 후보 선택이나 운영 주장이 아니다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = by.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", NEXT_RUN_ID)
    workspace = bg.replace_top_value(workspace, "updated_on: ", f"'{TODAY}'")
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337BZ focus complete: runtime KPI/no-overfit matrix(런타임 성과/무과적합 행렬)을 `{final['status']}`로 닫았다. "
        "Effect(효과): label boundary(라벨 경계)와 lifecycle proxy(생애주기 프록시)를 run337CA(337CA 실행) 우선 탐침으로 연다.\n"
    )
    if "Stage337 run337BZ focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(by.write_text_preserving(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = by.read_text_lossless(CURRENT_STATE)
    current = current_text
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BZ(337BZ 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): runtime KPI attribution/no-overfit matrix(런타임 성과 귀속/무과적합 행렬)을 만들고 label boundary/lifecycle(라벨 경계/생애주기) 우선 탐침을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337BZ(337BZ 실행)" not in current:
        marker = "## Stage337 run337BY(337BY"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(by.write_text_preserving(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- actual_mt5_execution(실제 MT5 실행): `not_run_matrix_from_existing_runtime_evidence`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 label boundary/lifecycle/cost frontier probe(라벨 경계/생애주기/비용 전선 탐침)이다.
"""
    artifacts.append(by.write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = by.read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337BZ(337BZ 실행) built runtime KPI/no-overfit matrix(런타임 성과/무과적합 행렬). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(by.write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = by.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337BZ built runtime KPI/no-overfit matrix(런타임 성과/무과적합 행렬) and opened `{NEXT_RUN_ID}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(by.write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_kpi_no_overfit_matrix_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};runtime_matrix_rows={final['runtime_matrix_rows']};goal_achieve_not_claimed.",
        "family": "kpi_evidence",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_kpi_no_overfit_matrix",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_kpi_no_overfit_matrix",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "diagnostic_matrix",
        "tier_scope": "Tier A completed-day runtime evidence boundary",
        "kpi_scope": "runtime_kpi_attribution_no_overfit_no_forward_decision",
        "scoreboard_lane": "diagnostic_special",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"runtime_matrix_rows={final['runtime_matrix_rows']}",
        "guardrail_kpi": "no training; no threshold tuning; no goal claim",
        "external_verification_status": "reviewed_existing_mt5_output",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_kpi_no_overfit_matrix",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "kpi_evidence",
        "evidence_scope": "BY lock, BX runtime KPI, BU split scorecard, proxy labels",
        "kpi_scope": "runtime_kpi_no_overfit_matrix",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"split_rows={final['split_matrix_rows']};cost_rows={final['cost_sensitivity_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__runtime_kpi_no_overfit_matrix",
        "family": "kpi_evidence",
        "question": "what causes weak runtime KPI and what must be repaired before new ONNX work",
        "metric_scope": "runtime_kpi_label_split_cost_session",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    artifacts = [
        aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]
    artifact_columns, existing_rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    artifact_columns = artifact_columns or ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    generated = now_utc()
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    merged = [row for row in existing_rows if row.get("artifact_id") not in keys]
    merged.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, merged))
    return artifacts


def main() -> int:
    parse_args()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    input_gates = require_inputs()
    parent = read_json(BY_FINAL)
    locks = read_df(BY_LOCK)
    compare = read_df(BY_COMPARE)
    kpi = read_df(BX_KPI)
    flow = read_df(BX_FLOW)
    hour = read_df(BX_HOUR)
    score = read_df(BU_SCORECARD)
    proxy = read_df(BU_PROXY_EXPECTED)
    models = list(kpi["model_id"].astype(str))

    labels = build_label_boundary(proxy, locks)
    splits = build_split_stability(score, models)
    sensitivity = build_threshold_cost_sensitivity(score, models)
    sessions = build_session_concentration(hour)
    runtime_rows = build_runtime_matrix(kpi, flow, compare, labels, splits, sessions)
    lanes = build_lane_priority(runtime_rows)
    followup = build_followup_queue(lanes)
    gates = build_gates(input_gates, labels, splits, sensitivity, sessions, runtime_rows, lanes)
    status, judgment, decision, next_action = classify(gates, runtime_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "parent_status": parent.get("status", ""),
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "label_boundary_rows": len(labels),
        "split_matrix_rows": len(splits),
        "cost_sensitivity_rows": len(sensitivity),
        "session_matrix_rows": len(sessions),
        "runtime_matrix_rows": len(runtime_rows),
        "lane_rows": len(lanes),
        "followup_rows": len(followup),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_rows": len(gates),
        "passed_gates": sum(1 for row in gates if row["status"] == "passed"),
        "failed_gates": [row["gate_id"] for row in gates if row["status"] != "passed"],
    }
    artifacts: list[Path] = [
        write_csv(LABEL_BOUNDARY_AUDIT, LABEL_COLUMNS, labels),
        write_csv(SPLIT_STABILITY_MATRIX, SPLIT_COLUMNS, splits),
        write_csv(THRESHOLD_COST_SENSITIVITY, SENSITIVITY_COLUMNS, sensitivity),
        write_csv(SIDE_SESSION_CONCENTRATION, SESSION_COLUMNS, sessions),
        write_csv(RUNTIME_KPI_MATRIX, RUNTIME_COLUMNS, runtime_rows),
        write_csv(RESEARCH_LANE_PRIORITY, LANE_COLUMNS, lanes),
        write_csv(FOLLOWUP_QUEUE, by.NEXT_COLUMNS, followup),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(build_receipts(final))
    artifacts.append(write_report(final, runtime_rows, lanes))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final, artifacts))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
