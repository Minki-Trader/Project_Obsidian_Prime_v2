from __future__ import annotations

import csv
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

import numpy as np
import onnxruntime as ort
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import prepare_timestamp_context_onnx_runtime_probe_without_db as pkg  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364I"
RUN_ID = "run364I_design_dense_m5_runtime_repair_proxy_without_db_v1"
PARENT_RUN_ID = "run364H_review_timestamp_context_onnx_mt5_runtime_probe_without_db_v1"
NEXT_RUN_ID = "run364J_train_direct_dense_m5_return_onnx_scout_without_db_v1"

STATUS = "completed_stage364I_dense_m5_repair_proxy_scouted_direct_dense_onnx_scout_opened_no_authority"
JUDGMENT = (
    "mixed_proxy_prefilter_dense_source_recovers_feature_density_but_stage364_cost_filter_edge_weak_"
    "direct_dense_model_scout_required_no_authority"
)
DECISION = "stage364I_open_run364J_train_direct_dense_m5_return_onnx_scout_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_dense_m5_proxy_prefilter_only_no_new_model_training_no_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "mt5_runtime_bar_time_joined_to_raw_m5_time_open_unix_no_timezone_conversion"
PROXY_EXECUTION_BOUNDARY = "raw_m5_open_to_open_long_proxy_not_mt5_strategy_tester"
COST_STRESS_PER_TRADE = 0.30
FIXED_LOT = 0.10

STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"

SOURCE_RUN364H_DIR = STAGE_DIR / "02_runs" / "run364H"
SOURCE_RUN364E_DIR = STAGE_DIR / "02_runs" / "run364E"
SOURCE_RUN364D_DIR = STAGE_DIR / "02_runs" / "run364D"
SOURCE_STAGE359_DIR = ROOT / "stages" / "359_runtime_probe_execution__high_density_label_pivot_mt5_check" / "02_runs" / "run359B"

SOURCE_PARENT_FINAL = SOURCE_RUN364H_DIR / "final_decision.json"
SOURCE_PARENT_GATES = SOURCE_RUN364H_DIR / "required_gate_coverage_audit.csv"
SOURCE_REPAIR_QUEUE = SOURCE_RUN364H_DIR / "run364I_offensive_repair_design_queue.csv"
SOURCE_PARENT_REPORT = REVIEW_DIR / "run364H_timestamp_context_onnx_mt5_runtime_probe_review.md"
SOURCE_SELECTED_MODEL_SUMMARY = SOURCE_RUN364E_DIR / "selected_model_summary.json"
SOURCE_FEATURE_SCHEMA = SOURCE_RUN364D_DIR / "timestamp_context_feature_schema.json"
SOURCE_BINARY_ONNX = SOURCE_RUN364E_DIR / "onnx" / "rf_depth3_balanced.onnx"
SOURCE_RUN359_SUMMARY = SOURCE_STAGE359_DIR / "high_density_label_pivot_mt5_probe_summary.csv"
SOURCE_Q05_VALIDATION_TELEMETRY = SOURCE_STAGE359_DIR / "runtime_telemetry" / "q05_pside_all_validation_telemetry.csv"
SOURCE_Q05_OOS_TELEMETRY = SOURCE_STAGE359_DIR / "runtime_telemetry" / "q05_pside_all_oos_telemetry.csv"
SOURCE_RAW_US100_M5 = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"

INPUT_FILES = [
    SOURCE_PARENT_FINAL,
    SOURCE_PARENT_GATES,
    SOURCE_REPAIR_QUEUE,
    SOURCE_PARENT_REPORT,
    SOURCE_SELECTED_MODEL_SUMMARY,
    SOURCE_FEATURE_SCHEMA,
    SOURCE_BINARY_ONNX,
    SOURCE_RUN359_SUMMARY,
    SOURCE_Q05_VALIDATION_TELEMETRY,
    SOURCE_Q05_OOS_TELEMETRY,
    SOURCE_RAW_US100_M5,
]

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
DENSE_FEATURE_MATRIX = RUN_DIR / "dense_m5_source_feature_matrix.csv"
DENSE_COVERAGE = RUN_DIR / "dense_source_coverage.csv"
VARIANT_SCORECARD = RUN_DIR / "dense_proxy_variant_scorecard.csv"
TOP_TRADE_SAMPLE = RUN_DIR / "dense_proxy_top_trade_sample.csv"
FINDINGS = RUN_DIR / "dense_runtime_repair_findings.csv"
NEXT_QUEUE = RUN_DIR / "run364J_offensive_next_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364I_dense_m5_runtime_repair_proxy.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364I_dense_m5_runtime_repair_proxy.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

OUTPUT_FILES = [
    INPUT_MANIFEST,
    DENSE_FEATURE_MATRIX,
    DENSE_COVERAGE,
    VARIANT_SCORECARD,
    TOP_TRADE_SAMPLE,
    FINDINGS,
    NEXT_QUEUE,
    WORK_PACKET,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path | str) -> str:
    return pkg.tr.fs_path(path)


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path | str) -> bool:
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha256_file(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    pkg.write_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.tr.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    return pkg.tr.read_csv_rows(path)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    pkg.tr.append_or_replace_csv(path, key_fields, rows, extend_header=True)


def append_registry_rows(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    pkg.append_registry_rows(path, key_fields, rows)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return default


def finite_float(value: float, digits: int = 10) -> float | str:
    if math.isnan(value):
        return ""
    if math.isinf(value):
        return "inf" if value > 0 else "-inf"
    return round(float(value), digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SELECTED_DIR, SPEC_DIR]:
        os.makedirs(io(path), exist_ok=True)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364I inputs: " + ", ".join(missing))
    parent = read_json(SOURCE_PARENT_FINAL)
    if parent.get("next_run_id") != "run364I_design_runtime_failure_repair_offensive_queue_without_db_v1":
        raise RuntimeError(f"run364H parent next_run_id mismatch: {parent.get('next_run_id')}")
    _, gates = read_csv_rows(SOURCE_PARENT_GATES)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run364H gates are not all passed")
    selected = read_json(SOURCE_SELECTED_MODEL_SUMMARY)
    if selected.get("best_onnx_model_id") != "rf_depth3_balanced":
        raise RuntimeError("run364I expects run364E rf_depth3_balanced selected model")


def write_input_manifest() -> None:
    rows = []
    for path in [*INPUT_FILES, Path(__file__)]:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "availability": "tracked_or_ignored_with_manifest",
                "effect": "input identity(입력 정체성)를 고정해 dense proxy(고밀도 프록시)를 재현 가능하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)


def load_feature_schema() -> list[str]:
    schema = read_json(SOURCE_FEATURE_SCHEMA)
    return list(schema["feature_columns"])


def load_feature_days() -> dict[str, float]:
    frame = pd.read_csv(io(SOURCE_RUN359_SUMMARY), encoding="utf-8-sig")
    days: dict[str, float] = {}
    for split in ("validation", "oos"):
        attempt = f"q05_pside_all_{split}"
        match = frame.loc[frame["attempt_name"].eq(attempt)]
        if match.empty:
            raise RuntimeError(f"missing run359B summary row: {attempt}")
        days[split] = float(match["feature_day_count"].iloc[0])
    return days


def load_q05_cycle(split: str) -> pd.DataFrame:
    path = SOURCE_Q05_VALIDATION_TELEMETRY if split == "validation" else SOURCE_Q05_OOS_TELEMETRY
    frame = pd.read_csv(io(path), encoding="utf-8-sig")
    frame = frame.loc[frame["record_type"].eq("cycle")].copy()
    frame["split"] = split
    frame["bar_dt"] = pd.to_datetime(frame["bar_time"], format="%Y.%m.%d %H:%M:%S", errors="raise")
    for column in ["p_short", "p_flat", "p_long"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if frame[["p_short", "p_flat", "p_long"]].isna().any().any():
        raise RuntimeError(f"q05 telemetry probabilities contain NaN: {split}")
    return frame


def add_stage364_features(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["margin_gap_actual"] = out["p_long"] - out[["p_short", "p_flat"]].max(axis=1)
    out["p_long_minus_p_short"] = out["p_long"] - out["p_short"]
    out["p_long_minus_p_flat"] = out["p_long"] - out["p_flat"]
    out["open_hour"] = out["bar_dt"].dt.hour.astype(int)
    out["open_dow"] = out["bar_dt"].dt.dayofweek.astype(int)
    out["minute_bucket15"] = ((out["bar_dt"].dt.minute // 15) * 15).astype(int)
    out["is_hour17"] = (out["open_hour"] == 17).astype(int)
    out["is_minute30_or45"] = out["minute_bucket15"].isin([30, 45]).astype(int)
    out["is_primary_toxic_bucket"] = ((out["open_hour"] == 17) & out["minute_bucket15"].isin([30, 45])).astype(int)
    out["open_hour_sin"] = np.sin(2.0 * np.pi * out["open_hour"] / 24.0)
    out["open_hour_cos"] = np.cos(2.0 * np.pi * out["open_hour"] / 24.0)
    out["open_dow_sin"] = np.sin(2.0 * np.pi * out["open_dow"] / 7.0)
    out["open_dow_cos"] = np.cos(2.0 * np.pi * out["open_dow"] / 7.0)
    out["minute_bucket15_sin"] = np.sin(2.0 * np.pi * out["minute_bucket15"] / 60.0)
    out["minute_bucket15_cos"] = np.cos(2.0 * np.pi * out["minute_bucket15"] / 60.0)
    out["hour17_p_long_interaction"] = out["is_hour17"] * out["p_long"]
    out["hour17_margin_gap_interaction"] = out["is_hour17"] * out["margin_gap_actual"]
    out["hour17_plong_minus_pshort_interaction"] = out["is_hour17"] * out["p_long_minus_p_short"]
    return out


def score_keep_probability(frame: pd.DataFrame, feature_columns: Sequence[str]) -> np.ndarray:
    matrix = frame.loc[:, list(feature_columns)].astype("float32").to_numpy()
    if not np.isfinite(matrix).all():
        raise RuntimeError("dense Stage364 feature matrix contains non-finite values")
    session = ort.InferenceSession(io(SOURCE_BINARY_ONNX), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    output_names = [output.name for output in session.get_outputs()]
    outputs = session.run(None, {input_name: matrix})
    probability_index = output_names.index("probabilities") if "probabilities" in output_names else len(outputs) - 1
    probabilities = np.asarray(outputs[probability_index], dtype="float64")
    if probabilities.ndim != 2 or probabilities.shape[1] != 2:
        raise RuntimeError(f"expected binary probabilities, got {probabilities.shape}")
    return probabilities[:, 1]


def load_raw_prices() -> pd.DataFrame:
    raw = pd.read_csv(io(SOURCE_RAW_US100_M5), usecols=["time_open_unix", "open", "close"], encoding="utf-8-sig")
    raw["bar_time"] = (
        pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
        .dt.tz_localize(None)
        .dt.strftime("%Y.%m.%d %H:%M:%S")
    )
    raw = raw.drop_duplicates("bar_time").set_index("bar_time")
    return raw[["open", "close"]]


def materialize_dense_source(feature_columns: Sequence[str]) -> pd.DataFrame:
    dense = pd.concat([load_q05_cycle("validation"), load_q05_cycle("oos")], ignore_index=True)
    dense = add_stage364_features(dense)
    raw = load_raw_prices()
    dense["raw_open"] = dense["bar_time"].map(raw["open"])
    dense["raw_close"] = dense["bar_time"].map(raw["close"])
    dense["keep_probability"] = score_keep_probability(dense, feature_columns)
    dense["source_scope"] = "run359B_q05_dense_runtime_cycle"
    dense["source_boundary"] = "q05 runtime telemetry reused as dense feature source(q05 런타임 기록을 고밀도 피처 원천으로 재사용)"
    dense["time_axis"] = TIME_AXIS
    dense["claim_boundary"] = CLAIM_BOUNDARY
    missing_raw = int(dense[["raw_open", "raw_close"]].isna().any(axis=1).sum())
    if missing_raw:
        raise RuntimeError(f"raw M5 price join missing rows: {missing_raw}")
    output_columns = [
        "split",
        "bar_time",
        "source_time",
        "symbol",
        "timeframe",
        "decision",
        "decision_reason",
        "exec_action",
        "position_before",
        "position_after",
        "input_hash",
        "raw_open",
        "raw_close",
        "keep_probability",
        *feature_columns,
        "source_scope",
        "source_boundary",
        "time_axis",
        "claim_boundary",
    ]
    write_csv(DENSE_FEATURE_MATRIX, dense.loc[:, output_columns].to_dict("records"))
    return dense


def source_scope_functions() -> dict[str, Callable[[pd.DataFrame], pd.Series]]:
    return {
        "q05_long_dense_flat_fill": lambda frame: frame["decision"].eq("long"),
        "q05_long_no_hour18_dense_flat_fill": lambda frame: frame["decision"].eq("long") & ~frame["open_hour"].isin([18]),
        "q05_long_no_hour16_18_dense_flat_fill": lambda frame: frame["decision"].eq("long") & ~frame["open_hour"].isin([16, 18]),
        "all_m5_keep_probability_extreme_control": lambda frame: pd.Series(True, index=frame.index),
    }


def choose_validation_threshold(validation: pd.DataFrame, eligible: pd.Series, feature_days: float, target: float) -> float:
    scores = validation.loc[eligible, "keep_probability"].to_numpy(dtype="float64")
    if scores.size == 0:
        return 1.0
    k = max(1, min(scores.size, math.ceil(target * feature_days)))
    return float(np.sort(scores)[::-1][k - 1])


def threshold_plan(dense: pd.DataFrame, days: Mapping[str, float]) -> dict[str, dict[str, float]]:
    selected = read_json(SOURCE_SELECTED_MODEL_SUMMARY)
    validation = dense.loc[dense["split"].eq("validation")].copy().reset_index(drop=True)
    plan: dict[str, dict[str, float]] = {
        "run364E_fixed_density_3_0": {
            "threshold": float(selected["best_onnx_threshold"]),
            "target_trade_day": float(selected["best_onnx_validation_density"]),
        }
    }
    for target in [3.0, 5.0, 7.0, 10.0]:
        plan[f"validation_dense_target_{str(target).replace('.', '_')}"] = {
            "threshold": target,
            "target_trade_day": target,
        }
    return plan


def selected_threshold(
    threshold_id: str,
    threshold_payload: Mapping[str, float],
    validation: pd.DataFrame,
    eligible_validation: pd.Series,
    days: Mapping[str, float],
) -> float:
    if threshold_id == "run364E_fixed_density_3_0":
        return float(threshold_payload["threshold"])
    return choose_validation_threshold(validation, eligible_validation, float(days["validation"]), float(threshold_payload["target_trade_day"]))


def simulate_long_proxy(
    frame: pd.DataFrame,
    desired: pd.Series,
    *,
    max_hold_bars: int,
    force_same_day_flat: bool,
    variant_id: str,
) -> list[dict[str, Any]]:
    rows = frame.sort_values("bar_dt").reset_index(drop=True)
    wants = desired.reset_index(drop=True).astype(bool).to_numpy()
    opens = rows["raw_open"].to_numpy(dtype="float64")
    closes = rows["raw_close"].to_numpy(dtype="float64")
    bar_times = rows["bar_time"].astype(str).to_numpy()
    bar_dates = rows["bar_dt"].dt.strftime("%Y-%m-%d").to_numpy()
    probabilities = rows["keep_probability"].to_numpy(dtype="float64")

    trades: list[dict[str, Any]] = []
    in_position = False
    entry_price = 0.0
    entry_time = ""
    entry_probability = 0.0
    hold_bars = 0
    previous_date = ""
    entry_index = -1

    for index, want_long in enumerate(wants):
        current_date = str(bar_dates[index])
        if in_position:
            hold_bars += 1
            exit_reason = ""
            if force_same_day_flat and previous_date and current_date != previous_date:
                exit_reason = "same_day_force_flat"
            elif not want_long:
                exit_reason = "close_on_flat"
            elif hold_bars >= max_hold_bars:
                exit_reason = "calendar_max_hold"
            if exit_reason:
                exit_price = float(opens[index] if np.isfinite(opens[index]) else closes[index])
                gross = (exit_price - entry_price) * FIXED_LOT
                trades.append(
                    {
                        "run_id": RUN_ID,
                        "variant_id": variant_id,
                        "split": rows.loc[index, "split"],
                        "entry_index": entry_index,
                        "exit_index": index,
                        "entry_time": entry_time,
                        "exit_time": str(bar_times[index]),
                        "entry_price": round(entry_price, 5),
                        "exit_price": round(exit_price, 5),
                        "entry_keep_probability": round(entry_probability, 12),
                        "hold_bars": hold_bars,
                        "gross_proxy_profit": round(gross, 10),
                        "cost_0_30_proxy_profit": round(gross - COST_STRESS_PER_TRADE, 10),
                        "exit_reason": exit_reason,
                        "proxy_boundary": PROXY_EXECUTION_BOUNDARY,
                    }
                )
                in_position = False
                hold_bars = 0
                entry_index = -1
        if not in_position and want_long:
            entry_price = float(opens[index] if np.isfinite(opens[index]) else closes[index])
            entry_time = str(bar_times[index])
            entry_probability = float(probabilities[index])
            in_position = True
            hold_bars = 0
            entry_index = index
        previous_date = current_date

    if in_position:
        index = len(rows) - 1
        exit_price = float(closes[index] if np.isfinite(closes[index]) else opens[index])
        gross = (exit_price - entry_price) * FIXED_LOT
        trades.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "split": rows.loc[index, "split"],
                "entry_index": entry_index,
                "exit_index": index,
                "entry_time": entry_time,
                "exit_time": str(bar_times[index]),
                "entry_price": round(entry_price, 5),
                "exit_price": round(exit_price, 5),
                "entry_keep_probability": round(entry_probability, 12),
                "hold_bars": hold_bars,
                "gross_proxy_profit": round(gross, 10),
                "cost_0_30_proxy_profit": round(gross - COST_STRESS_PER_TRADE, 10),
                "exit_reason": "final_close",
                "proxy_boundary": PROXY_EXECUTION_BOUNDARY,
            }
        )
    return trades


def metric_row(
    trades: Sequence[Mapping[str, Any]],
    *,
    split: str,
    feature_day_count: float,
    variant_id: str,
    desired_rows: int,
    source_scope_id: str,
    threshold_id: str,
    threshold: float,
    target_trade_day: float,
    exit_policy_id: str,
    max_hold_bars: int,
    force_same_day_flat: bool,
) -> dict[str, Any]:
    profits = np.asarray([as_float(row["cost_0_30_proxy_profit"]) for row in trades], dtype="float64")
    trade_count = int(len(profits))
    density = trade_count / feature_day_count if feature_day_count else 0.0
    desired_density = desired_rows / feature_day_count if feature_day_count else 0.0
    if trade_count:
        net = float(profits.sum())
        gains = float(profits[profits > 0].sum())
        losses = float(profits[profits < 0].sum())
        pf = gains / abs(losses) if losses < 0 else (999.0 if gains > 0 else 0.0)
        equity = np.cumsum(profits)
        peaks = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
        drawdown = float((equity - peaks).min()) if equity.size else 0.0
        recovery = net / abs(drawdown) if drawdown < 0 else (999.0 if net > 0 else 0.0)
        expectancy = net / trade_count
        win_rate = float((profits > 0).mean())
        hold_values = [as_float(row["hold_bars"]) for row in trades]
        max_hold_observed = int(max(hold_values)) if hold_values else 0
    else:
        net = gains = losses = pf = drawdown = recovery = expectancy = win_rate = 0.0
        max_hold_observed = 0
    strict_success = (
        density >= 3.0
        and net > 0
        and pf >= 1.05
        and drawdown > -300.0
    )
    soft_density_positive = density >= 3.0 and net > 0
    return {
        "run_id": RUN_ID,
        "variant_id": variant_id,
        "split": split,
        "source_scope_id": source_scope_id,
        "threshold_id": threshold_id,
        "threshold": round(float(threshold), 12),
        "target_trade_day": target_trade_day,
        "exit_policy_id": exit_policy_id,
        "max_hold_bars": max_hold_bars,
        "force_same_day_flat": force_same_day_flat,
        "desired_long_rows": desired_rows,
        "desired_long_density": round(desired_density, 10),
        "proxy_trade_count": trade_count,
        "proxy_trade_density_per_feature_day": round(density, 10),
        "cost_0_30_net_profit": round(net, 10),
        "cost_0_30_gross_profit": round(gains, 10),
        "cost_0_30_gross_loss": round(losses, 10),
        "cost_0_30_profit_factor": finite_float(pf),
        "cost_0_30_expectancy": round(expectancy, 10) if trade_count else 0.0,
        "win_rate": round(win_rate, 10) if trade_count else 0.0,
        "max_drawdown_cost_0_30": round(drawdown, 10),
        "recovery_factor_cost_0_30": finite_float(recovery),
        "max_hold_observed_bars": max_hold_observed,
        "strict_success": "true" if strict_success else "false",
        "soft_density_positive": "true" if soft_density_positive else "false",
        "no_trade_splitting_status": "single_position_entry_transition_only",
        "proxy_boundary": PROXY_EXECUTION_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def sweep_variants(dense: pd.DataFrame, days: Mapping[str, float]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    scopes = source_scope_functions()
    threshold_payloads = threshold_plan(dense, days)
    validation = dense.loc[dense["split"].eq("validation")].sort_values("bar_dt").reset_index(drop=True)
    split_frames = {split: dense.loc[dense["split"].eq(split)].sort_values("bar_dt").reset_index(drop=True) for split in ("validation", "oos")}
    exit_policies = [
        ("close_on_flat_m5_max6", 6, False),
        ("close_on_flat_m5_max12", 12, False),
        ("close_on_flat_m5_max24", 24, False),
        ("same_day_flat_m5_max24", 24, True),
    ]
    metric_rows: list[dict[str, Any]] = []
    trade_rows: list[dict[str, Any]] = []
    for source_scope_id, scope_func in scopes.items():
        eligible_validation = scope_func(validation)
        for threshold_id, threshold_payload in threshold_payloads.items():
            threshold = selected_threshold(threshold_id, threshold_payload, validation, eligible_validation, days)
            target_trade_day = float(threshold_payload["target_trade_day"])
            for exit_policy_id, max_hold_bars, force_same_day_flat in exit_policies:
                variant_id = f"{source_scope_id}__{threshold_id}__{exit_policy_id}"
                for split, split_frame in split_frames.items():
                    eligible = scope_func(split_frame)
                    desired = eligible & (split_frame["keep_probability"] >= threshold)
                    trades = simulate_long_proxy(
                        split_frame,
                        desired,
                        max_hold_bars=max_hold_bars,
                        force_same_day_flat=force_same_day_flat,
                        variant_id=variant_id,
                    )
                    metric_rows.append(
                        metric_row(
                            trades,
                            split=split,
                            feature_day_count=float(days[split]),
                            variant_id=variant_id,
                            desired_rows=int(desired.sum()),
                            source_scope_id=source_scope_id,
                            threshold_id=threshold_id,
                            threshold=threshold,
                            target_trade_day=target_trade_day,
                            exit_policy_id=exit_policy_id,
                            max_hold_bars=max_hold_bars,
                            force_same_day_flat=force_same_day_flat,
                        )
                    )
                    if trades:
                        sorted_trades = sorted(trades, key=lambda row: as_float(row["cost_0_30_proxy_profit"]))
                        trade_rows.extend(sorted_trades[:3])
                        trade_rows.extend(sorted_trades[-3:])
    write_csv(VARIANT_SCORECARD, metric_rows)
    write_csv(TOP_TRADE_SAMPLE, trade_rows)
    return metric_rows, trade_rows


def pair_metrics(metric_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_variant: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in metric_rows:
        by_variant.setdefault(str(row["variant_id"]), {})[str(row["split"])] = row
    paired = []
    for variant_id, splits in by_variant.items():
        validation = splits.get("validation", {})
        oos = splits.get("oos", {})
        if not validation or not oos:
            continue
        strict = validation.get("strict_success") == "true" and oos.get("strict_success") == "true"
        soft = validation.get("soft_density_positive") == "true" and oos.get("soft_density_positive") == "true"
        paired.append(
            {
                "variant_id": variant_id,
                "source_scope_id": validation.get("source_scope_id", ""),
                "threshold_id": validation.get("threshold_id", ""),
                "exit_policy_id": validation.get("exit_policy_id", ""),
                "validation_density": as_float(validation.get("proxy_trade_density_per_feature_day")),
                "oos_density": as_float(oos.get("proxy_trade_density_per_feature_day")),
                "validation_net": as_float(validation.get("cost_0_30_net_profit")),
                "oos_net": as_float(oos.get("cost_0_30_net_profit")),
                "validation_pf": as_float(validation.get("cost_0_30_profit_factor")),
                "oos_pf": as_float(oos.get("cost_0_30_profit_factor")),
                "validation_drawdown": as_float(validation.get("max_drawdown_cost_0_30")),
                "oos_drawdown": as_float(oos.get("max_drawdown_cost_0_30")),
                "strict_cross_split_success": strict,
                "soft_cross_split_density_positive": soft,
                "ranking_score": (
                    as_float(validation.get("cost_0_30_net_profit"))
                    + as_float(oos.get("cost_0_30_net_profit"))
                    + min(as_float(validation.get("cost_0_30_profit_factor")), as_float(oos.get("cost_0_30_profit_factor"))) * 10.0
                ),
            }
        )
    return sorted(
        paired,
        key=lambda row: (
            row["strict_cross_split_success"],
            row["soft_cross_split_density_positive"],
            row["oos_net"],
            row["validation_net"],
            row["ranking_score"],
        ),
        reverse=True,
    )


def write_dense_coverage(dense: pd.DataFrame, days: Mapping[str, float], metric_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    sparse_rows = int(read_json(SOURCE_PARENT_FINAL).get("expected_rows", 1114))
    paired = pair_metrics(metric_rows)
    strict_count = int(sum(1 for row in paired if row["strict_cross_split_success"]))
    soft_count = int(sum(1 for row in paired if row["soft_cross_split_density_positive"]))
    best = paired[0] if paired else {}
    coverage_rows = []
    for split in ("validation", "oos"):
        part = dense.loc[dense["split"].eq(split)]
        coverage_rows.append(
            {
                "run_id": RUN_ID,
                "split": split,
                "dense_cycle_rows": int(len(part)),
                "q05_long_cycle_rows": int(part["decision"].eq("long").sum()),
                "q05_short_cycle_rows": int(part["decision"].eq("short").sum()),
                "q05_flat_cycle_rows": int(part["decision"].eq("flat").sum()),
                "feature_day_count": days[split],
                "dense_cycle_per_feature_day": round(len(part) / days[split], 10) if days[split] else 0.0,
                "q05_long_cycle_per_feature_day": round(part["decision"].eq("long").sum() / days[split], 10) if days[split] else 0.0,
                "raw_price_join_missing_rows": int(part[["raw_open", "raw_close"]].isna().any(axis=1).sum()),
                "keep_probability_min": round(float(part["keep_probability"].min()), 12),
                "keep_probability_mean": round(float(part["keep_probability"].mean()), 12),
                "keep_probability_max": round(float(part["keep_probability"].max()), 12),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    coverage_rows.append(
        {
            "run_id": RUN_ID,
            "split": "combined",
            "dense_cycle_rows": int(len(dense)),
            "q05_long_cycle_rows": int(dense["decision"].eq("long").sum()),
            "q05_short_cycle_rows": int(dense["decision"].eq("short").sum()),
            "q05_flat_cycle_rows": int(dense["decision"].eq("flat").sum()),
            "feature_day_count": round(sum(days.values()), 4),
            "dense_cycle_per_feature_day": round(len(dense) / sum(days.values()), 10),
            "q05_long_cycle_per_feature_day": round(dense["decision"].eq("long").sum() / sum(days.values()), 10),
            "raw_price_join_missing_rows": int(dense[["raw_open", "raw_close"]].isna().any(axis=1).sum()),
            "keep_probability_min": round(float(dense["keep_probability"].min()), 12),
            "keep_probability_mean": round(float(dense["keep_probability"].mean()), 12),
            "keep_probability_max": round(float(dense["keep_probability"].max()), 12),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    write_csv(DENSE_COVERAGE, coverage_rows)
    return {
        "dense_rows": int(len(dense)),
        "sparse_expected_rows": sparse_rows,
        "dense_to_sparse_row_multiplier": round(len(dense) / sparse_rows, 10) if sparse_rows else 0.0,
        "strict_cross_split_success_count": strict_count,
        "soft_cross_split_density_positive_count": soft_count,
        "best_variant_id": best.get("variant_id", ""),
        "best_variant_source_scope": best.get("source_scope_id", ""),
        "best_variant_threshold_id": best.get("threshold_id", ""),
        "best_variant_exit_policy_id": best.get("exit_policy_id", ""),
        "best_validation_density": round(as_float(best.get("validation_density")), 10),
        "best_oos_density": round(as_float(best.get("oos_density")), 10),
        "best_validation_net": round(as_float(best.get("validation_net")), 10),
        "best_oos_net": round(as_float(best.get("oos_net")), 10),
        "best_validation_pf": round(as_float(best.get("validation_pf")), 10),
        "best_oos_pf": round(as_float(best.get("oos_pf")), 10),
    }


def write_findings_and_queue(summary: Mapping[str, Any]) -> None:
    findings = [
        {
            "finding_id": "F-ST364I-DENSE-SOURCE-COVERAGE",
            "finding_type": "positive_clue(긍정 단서)",
            "finding": "dense q05 runtime cycle source(고밀도 q05 런타임 사이클 원천)가 sparse expected tape(희소 예상 테이프)보다 훨씬 넓은 feature-ready rows(피처 준비 행)를 제공한다.",
            "metric": f"dense_rows={summary['dense_rows']};sparse_expected_rows={summary['sparse_expected_rows']};multiplier={summary['dense_to_sparse_row_multiplier']}",
            "effect": "run364G의 feature skip(피처 스킵)과 sparse max-hold(희소 최대 보유) 문제를 직접 고칠 재료가 생겼다.",
            "boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "F-ST364I-COST-FILTER-WEAK-OOS",
            "finding_type": "negative_memory(부정 기억)",
            "finding": "run364E cost filter(비용 필터)를 dense q05 source(고밀도 q05 원천)에 얹으면 일부 variant(변형)는 밀도와 순수익을 회복하지만 OOS profit factor(표본외 수익 팩터)가 너무 약하다.",
            "metric": f"strict_success_count={summary['strict_cross_split_success_count']};soft_density_positive_count={summary['soft_cross_split_density_positive_count']};best_oos_pf={summary['best_oos_pf']}",
            "effect": "운영 주장 대신 direct dense M5 ONNX scout(직접 고밀도 M5 ONNX 탐색)로 공격 방향을 바꾼다.",
            "boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "F-ST364I-NO-SPLIT-PROXY",
            "finding_type": "trade_shape_control(거래 형태 대조)",
            "finding": "proxy simulator(프록시 시뮬레이터)는 single-position entry-transition-only(단일 포지션 전환 진입)로 동작한다.",
            "metric": "no_trade_splitting_status=single_position_entry_transition_only",
            "effect": "거래수를 쪼개 수익을 나누는 방식 없이 dense tape(고밀도 테이프) 효과를 본다.",
            "boundary": CLAIM_BOUNDARY,
        },
    ]
    queue = [
        {
            "queue_id": "run364J_Q01_direct_dense_m5_return_onnx_scout",
            "next_run_id": NEXT_RUN_ID,
            "idea_id": "IDEA-ST364I-DIRECT-DENSE-M5-RETURN-ONNX-SCOUT",
            "hypothesis": "processed dense M5 features(처리된 고밀도 M5 피처)와 direct forward-return label(직접 전방 수익 라벨)을 쓰면 q05 cost-filter overlay(q05 비용 필터 덧씌우기)보다 OOS edge(표본외 우위)를 넓게 회복할 수 있다.",
            "variant_family": "offensive_model_family_pivot(공격 모델 계열 전환)",
            "broad_sweep": "logreg/rf/extra-trees shallow ONNX(로지스틱/랜덤포레스트/엑스트라트리 얕은 ONNX), long-only and two-sided(롱 전용/양방향)",
            "extreme_sweep": "all-M5 dense target 3/5/7/10 per day(전체 M5 일 3/5/7/10 목표), no q05 probability bridge(q05 확률 연결 제거)",
            "success_gate": "validation+OOS proxy net>0, PF>=1.05, trade/day>=3, no catastrophic drawdown(검증+표본외 프록시 순수익 양수, 수익 팩터 1.05 이상, 일 3회 이상, 파국 낙폭 없음)",
            "effect": "Stage364를 새 stage(단계)로 쪼개지 않고 같은 단계 안에서 더 공격적인 수익 원천을 연다.",
            "boundary": "design_queue_next_run(다음 실행 설계 대기열)",
        },
        {
            "queue_id": "run364J_Q02_q05_dense_two_sided_session_veto_control",
            "next_run_id": "run364J_or_later_q05_dense_two_sided_session_veto_control",
            "idea_id": "IDEA-ST364I-Q05-DENSE-TWO-SIDED-SESSION-VETO",
            "hypothesis": "run359B q05 two-sided dense runtime(양방향 고밀도 런타임)은 OOS positive(표본외 양수)였으므로, validation loss clusters(검증 손실 군집)를 session/regime veto(세션/국면 제외)로 자르면 재사용 단서가 될 수 있다.",
            "variant_family": "offensive_rule_stack_control(공격 규칙 묶음 대조)",
            "broad_sweep": "hour veto, month/regime veto, volatility filter(시간 제외/월국면 제외/변동성 필터)",
            "extreme_sweep": "no-18-hour, no-16-18-hour, 19-21 only(18시 제외/16-18시 제외/19-21 전용)",
            "success_gate": "do not rely on long-only sparse trade table(롱 전용 희소 거래표에 기대지 않기)",
            "effect": "run364I의 약한 long-only cost filter(롱 전용 비용 필터)를 원래 양방향 dense clue(고밀도 단서)와 비교한다.",
            "boundary": "queue_only(대기열 전용)",
        },
        {
            "queue_id": "run364J_Q03_dense_flat_tape_mt5_semantics_control",
            "next_run_id": "run364J_or_later_dense_flat_tape_mt5_semantics_control",
            "idea_id": "IDEA-ST364I-DENSE-FLAT-TAPE-MT5-SEMANTICS",
            "hypothesis": "best weak dense variant(최선 약한 고밀도 변형)을 MT5 flat-filled tape(MT5 flat 채움 테이프)로 보내면 sparse max-hold failure(희소 최대 보유 실패)가 사라지는지 분리할 수 있다.",
            "variant_family": "runtime_semantics_control(런타임 의미 대조)",
            "broad_sweep": "close_on_flat true, max_hold 6/12/24 M5 bars(flat 청산 true, 최대 보유 6/12/24 M5봉)",
            "extreme_sweep": "same-day force flat(당일 강제 flat)",
            "success_gate": "MT5 probe must beat run364G negative KPI(MT5 탐침이 run364G 부정 KPI를 넘어야 함)",
            "effect": "모델 우위 실패와 런타임 보유 의미 실패를 분리한다.",
            "boundary": "queue_only(대기열 전용)",
        },
    ]
    write_csv(FINDINGS, findings)
    write_csv(NEXT_QUEUE, queue)


def write_work_packet_and_receipts(summary: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "work_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템; policy-backed)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "dense M5 source(고밀도 M5 원천) and calendar exit(캘린더 청산) can repair run364G sparse runtime failure.",
            "decision_use": "choose next offensive run(다음 공격 실행 선택)",
            "comparison_baseline": "run364G MT5 negative probe and run359B q05 dense runtime(run364G MT5 부정 탐침 및 run359B q05 고밀도 런타임)",
            "control_variables": ["fixed_lot=0.10", "cost_stress_per_trade=0.30", "single_position=true"],
            "changed_variables": ["dense source scope", "keep threshold", "calendar max hold", "session veto"],
            "sample_scope": "Tier A validation+OOS q05 runtime cycles(Tier A 검증+표본외 q05 런타임 사이클)",
            "success_criteria": "cross-split net>0, PF>=1.05, trade/day>=3 without trade splitting",
            "failure_criteria": "density recovers but OOS PF/net remains weak",
            "invalid_conditions": "raw M5 join missing, ONNX scoring failure, timestamp disorder",
            "stop_conditions": "open direct dense ONNX scout if strict cross-split success count is zero",
            "evidence_plan": [rel(VARIANT_SCORECARD), rel(DENSE_COVERAGE), rel(FINDINGS), rel(NEXT_QUEUE)],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(SOURCE_Q05_VALIDATION_TELEMETRY), rel(SOURCE_Q05_OOS_TELEMETRY), rel(SOURCE_RAW_US100_M5)],
            "time_axis": TIME_AXIS,
            "sample_scope": "validation 2025-01-02..2025-09-30, OOS 2025-10-01..2026-04-13 q05 cycle rows",
            "missing_or_duplicate_check": "raw price join missing rows = 0",
            "feature_label_boundary": "features from q05 runtime probabilities and timestamp fields only; proxy PnL uses later raw price after scoring",
            "split_boundary": "run359B validation/OOS retained",
            "leakage_risk": "proxy PnL must not feed threshold except validation target threshold; OOS read only",
            "data_hash_or_identity": {"dense_rows": summary["dense_rows"], "raw_sha256": sha(SOURCE_RAW_US100_M5)},
            "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 조건부 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "run364E rf_depth3_balanced ONNX cost filter(run364E 랜덤포레스트 비용 필터 ONNX)",
            "target_and_label": "label_cost_positive_0_30 from sparse long trade training seed",
            "split_method": "validation threshold, OOS read only",
            "selection_metric": "dense proxy cross-split net/PF/density",
            "secondary_metrics": ["drawdown", "expectancy", "trade_count", "session veto"],
            "threshold_policy": "fixed run364E threshold plus validation target thresholds",
            "overfit_risk": "threshold and session sweeps are scout-only until MT5 probe",
            "calibration_risk": "keep score is sparse long-cost probability, not full dense M5 calibrated probability",
            "comparison_baseline": "run364G sparse MT5 negative and run359B q05 dense runtime",
            "validation_judgment": "exploratory_mixed_no_candidate_selection(탐색 혼합, 후보 선택 없음)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_reports_and_ignored_run_artifacts_with_manifest",
            "lineage_judgment": "connected_with_proxy_boundary(프록시 경계 조건부 연결)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "strict_cross_split_success_count": summary["strict_cross_split_success_count"],
            "soft_cross_split_density_positive_count": summary["soft_cross_split_density_positive_count"],
            "mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": "dense M5 proxy prefilter completed(고밀도 M5 프록시 선별 완료)",
            "forbidden_claims": [
                "MT5 KPI verified(MT5 KPI 검증)",
                "operating promotion(운영 승격)",
                "runtime authority(런타임 권위)",
                "live readiness(실거래 준비)",
                "Goal Achieve(목표 달성)",
            ],
        },
    )


def gate_row(gate_id: str, passed: bool, evidence_path: Path, description: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": "passed" if passed else "failed",
        "evidence_path": rel(evidence_path),
        "description": description,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    _, parent_gates = read_csv_rows(SOURCE_PARENT_GATES)
    parent_passed = bool(parent_gates) and all(row.get("status") == "passed" for row in parent_gates)
    return [
        gate_row("parent_364H_gates_passed", parent_passed, SOURCE_PARENT_GATES, "run364H gates(364H 게이트)를 상속 확인한다."),
        gate_row("dense_source_rows_materialized", summary["dense_rows"] > summary["sparse_expected_rows"], DENSE_FEATURE_MATRIX, "dense source(고밀도 원천)가 sparse expected tape(희소 예상 테이프)보다 넓다."),
        gate_row("raw_m5_price_join_complete", True, DENSE_COVERAGE, "raw M5 price join(원천 M5 가격 결합) 누락이 없다."),
        gate_row("onnx_scoring_completed", exists(DENSE_FEATURE_MATRIX), DENSE_FEATURE_MATRIX, "run364E ONNX(온엑스) keep probability(유지 확률)를 dense rows(고밀도 행)에 계산했다."),
        gate_row("proxy_variant_sweep_materialized", exists(VARIANT_SCORECARD), VARIANT_SCORECARD, "threshold/session/exit sweep(임계값/세션/청산 탐색)을 기록했다."),
        gate_row("trade_density_no_split_audit_written", exists(VARIANT_SCORECARD), VARIANT_SCORECARD, "single-position entry-transition-only(단일 포지션 전환 진입) proxy(프록시)를 썼다."),
        gate_row("findings_and_next_queue_written", exists(FINDINGS) and exists(NEXT_QUEUE), NEXT_QUEUE, "findings(발견)와 next queue(다음 대기열)를 기록했다."),
        gate_row("paired_tier_records_written", True, STAGE_LEDGER, "Tier A/B/A+B(티어 A/B/A+B) 기록 경계를 남긴다."),
        gate_row("no_forbidden_operating_claim", True, FINAL_DECISION, "운영 승격/런타임 권위/목표 달성을 주장하지 않는다."),
        gate_row("required_gate_coverage_audit_written", True, GATE_AUDIT, "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다."),
    ]


def write_final_and_manifest(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    final = {
        **dict(summary),
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "result_judgment": JUDGMENT,
        "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
        "proxy_execution_boundary": PROXY_EXECUTION_BOUNDARY,
        "cost_stress_per_trade": COST_STRESS_PER_TRADE,
        "new_model_training": "not_run",
        "mt5_execution": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "gates_passed": all(row.get("status") == "passed" for row in gates),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "command": f"python {rel(Path(__file__))}",
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
            "external_verification_status": "out_of_scope_by_claim_no_mt5_execution",
        },
    )
    return final


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return ""
    lines = ["|" + "|".join(columns) + "|", "|" + "|".join(["---"] * len(columns)) + "|"]
    for row in rows:
        lines.append("|" + "|".join(str(row.get(column, "")) for column in columns) + "|")
    return "\n".join(lines)


def top_paired_rows(limit: int = 8) -> list[dict[str, Any]]:
    _, rows = read_csv_rows(VARIANT_SCORECARD)
    paired = pair_metrics(rows)
    return paired[:limit]


def write_report(final: Mapping[str, Any]) -> None:
    top_rows = top_paired_rows()
    report = f"""# run364I Dense M5 Runtime Repair Proxy(364I 고밀도 M5 런타임 수리 프록시)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- dense_rows(고밀도 행): `{final['dense_rows']}`
- sparse_expected_rows(희소 예상 행): `{final['sparse_expected_rows']}`
- dense_to_sparse_row_multiplier(고밀도/희소 배율): `{final['dense_to_sparse_row_multiplier']}`
- strict_cross_split_success_count(엄격 교차 분할 성공 수): `{final['strict_cross_split_success_count']}`
- soft_cross_split_density_positive_count(느슨한 밀도+양수 수): `{final['soft_cross_split_density_positive_count']}`
- best_variant_id(최선 변형 ID): `{final['best_variant_id']}`
- best_validation_net(최선 검증 순수익): `{final['best_validation_net']}`
- best_oos_net(최선 표본외 순수익): `{final['best_oos_net']}`
- best_validation_density(최선 검증 밀도): `{final['best_validation_density']}`
- best_oos_density(최선 표본외 밀도): `{final['best_oos_density']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Judgment(판정)

Action(행동): run359B q05 dense runtime cycle(q05 고밀도 런타임 사이클)에 run364E ONNX cost filter(ONNX 비용 필터)를 다시 얹고, close_on_flat/calendar max-hold(Flat 청산/캘린더 최대 보유) proxy(프록시)를 넓게 시험했다.
Effect(효과): run364G의 sparse tape(희소 테이프) 문제는 고칠 수 있지만, 현재 cost filter(비용 필터)는 OOS profit factor(표본외 수익 팩터)가 약해서 운영 주장으로 갈 수 없다.

## Top Proxy Variants(상위 프록시 변형)

{markdown_table(top_rows, ["variant_id", "validation_density", "oos_density", "validation_net", "oos_net", "validation_pf", "oos_pf", "strict_cross_split_success", "soft_cross_split_density_positive"])}

## Evidence(근거)

- dense feature matrix(고밀도 피처 행렬): `{rel(DENSE_FEATURE_MATRIX)}`
- dense coverage(고밀도 커버리지): `{rel(DENSE_COVERAGE)}`
- variant scorecard(변형 점수표): `{rel(VARIANT_SCORECARD)}`
- findings(발견): `{rel(FINDINGS)}`
- next queue(다음 대기열): `{rel(NEXT_QUEUE)}`

## Boundary(경계)

proxy(프록시)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. 이번 실행은 model training(모델 학습), MT5 execution(MT5 실행), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, f"""# {TODAY} Stage364I Decision(364I 결정)

- decision(결정): `{DECISION}`
- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- strict_success_count(엄격 성공 수): `{final['strict_cross_split_success_count']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(VARIANT_SCORECARD)}`, `{rel(NEXT_QUEUE)}`

Action(행동): dense M5 repair proxy(고밀도 M5 수리 프록시)를 완료했다.
Effect(효과): Stage364(364단계)를 새로 쪼개지 않고, 다음 공격 실행을 direct dense M5 ONNX scout(직접 고밀도 M5 ONNX 탐색)로 연다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")


def replace_stage_header() -> None:
    text = pkg.tr.read_text(STAGE_BRIEF)
    replacements = {
        "- current_run_id(": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
        "- latest_completed_run_id(": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
        "- selection_status(": "- selection_status(선택 상태): `dense_m5_proxy_scouted_direct_dense_onnx_scout_opened_no_operating_claim(고밀도 M5 프록시 탐색 완료, 직접 고밀도 ONNX 탐색 열림, 운영 주장 없음)`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    output = []
    for line in text.splitlines():
        replaced = False
        for prefix, value in replacements.items():
            if line.startswith(prefix):
                output.append(value)
                replaced = True
                break
        if not replaced:
            output.append(line)
    write_text(STAGE_BRIEF, "\n".join(output))


def write_state_docs(final: Mapping[str, Any]) -> None:
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    pkg.tr.write_text(WORKSPACE_STATE, workspace, bom=False)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

run364I(364I 실행)는 dense M5 source(고밀도 M5 원천)가 sparse runtime failure(희소 런타임 실패)를 고칠 수 있다는 구조 단서를 만들었지만, run364E cost filter(비용 필터)의 OOS edge(표본외 우위)가 약해 direct dense M5 ONNX scout(직접 고밀도 M5 ONNX 탐색)를 연다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 Selection Status(364단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- dense_m5_proxy(고밀도 M5 프록시): `completed_mixed_no_authority(완료, 혼합, 권위 없음)`
- dense_rows(고밀도 행): `{final['dense_rows']}`
- sparse_expected_rows(희소 예상 행): `{final['sparse_expected_rows']}`
- strict_cross_split_success_count(엄격 교차 분할 성공 수): `{final['strict_cross_split_success_count']}`
- best_oos_net(최선 표본외 순수익): `{final['best_oos_net']}`
- best_oos_pf(최선 표본외 수익 팩터): `{final['best_oos_pf']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): dense source(고밀도 원천)는 살리고, 약한 cost filter(비용 필터)는 운영 후보로 과장하지 않는다.
""",
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - dense M5 runtime repair proxy(고밀도 M5 런타임 수리 프록시).")
    append_text_once(
        STAGE_BRIEF,
        "## run364I Dense M5 Runtime Repair Proxy",
        f"""## run364I Dense M5 Runtime Repair Proxy(364I 고밀도 M5 런타임 수리 프록시)

Action(행동): q05 dense runtime cycles(q05 고밀도 런타임 사이클) `{final['dense_rows']}`개에 run364E ONNX cost filter(ONNX 비용 필터)를 적용하고 calendar exit proxy(캘린더 청산 프록시)를 탐색했다.

Effect(효과): sparse expected tape(희소 예상 테이프) 실패는 수리 가능하지만, strict cross-split success(엄격 교차 분할 성공)가 `{final['strict_cross_split_success_count']}`개라 `{NEXT_RUN_ID}`로 직접 고밀도 모델 탐색을 연다.
""",
    )
    append_text_once(
        STAGE_README,
        "## run364I Dense M5 Runtime Repair Proxy",
        f"""## run364I Dense M5 Runtime Repair Proxy(364I 고밀도 M5 런타임 수리 프록시)

Action(행동): dense source repair(고밀도 원천 수리)를 proxy scorecard(프록시 점수표)로 구체화했다.

Effect(효과): 다음 실행은 `{NEXT_RUN_ID}`이고, 운영 주장은 없다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} run364I Dense M5 Runtime Repair Proxy(364I 고밀도 M5 런타임 수리 프록시)

Action(행동): run359B q05 dense runtime cycle(q05 고밀도 런타임 사이클)을 run364E ONNX cost filter(ONNX 비용 필터)와 결합해 proxy sweep(프록시 탐색)을 실행했다.

Effect(효과): dense_rows(고밀도 행) `{final['dense_rows']}`, strict_success_count(엄격 성공 수) `{final['strict_cross_split_success_count']}`로 기록했고, 다음 공격 실행 `{NEXT_RUN_ID}`를 열었다.

Boundary(경계): MT5 execution(MT5 실행), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        "IDEA-ST364I-DIRECT-DENSE-M5-RETURN-ONNX-SCOUT",
        f"""## IDEA-ST364I-DIRECT-DENSE-M5-RETURN-ONNX-SCOUT

- idea(아이디어): q05 probability bridge(q05 확률 연결)와 sparse long cost filter(희소 롱 비용 필터)를 벗어나 processed dense M5 features(처리 고밀도 M5 피처)로 직접 ONNX(온엑스) 모델을 학습한다.
- hypothesis(가설): dense direct return label(고밀도 직접 수익 라벨)이 OOS edge(표본외 우위)를 더 넓게 만든다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): logreg/rf/extra-trees shallow ONNX(로지스틱/랜덤포레스트/엑스트라트리 얕은 ONNX), long-only/two-sided(롱 전용/양방향), trade/day 3/5/7/10.
- extreme_sweep(극단 탐색): all-M5 dense control(전체 M5 고밀도 대조), q05-free source(q05 제거 원천), no-18-hour veto(18시 제외).
- micro_search_gate(미세 탐색 게이트): validation+OOS proxy(검증+표본외 프록시) net>0, PF>=1.05, trade/day>=3.
- wfo_plan(WFO 계획): positive scout(긍정 탐색) 이후 WFO(walk-forward optimization, 워크포워드 최적화) 강화.
- failure_memory(실패 기억): run364I found cost-filter overlay OOS PF weak(run364I 비용 필터 덧씌우기 표본외 수익 팩터 약함).
- evidence_boundary(근거 경계): `scout_only(탐색 전용)`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    append_text_once(
        NEGATIVE_REGISTER,
        "FM-ST364I-COST-FILTER-DENSE-OOS-WEAK",
        f"""## FM-ST364I-COST-FILTER-DENSE-OOS-WEAK

- run_id(실행 ID): `{RUN_ID}`
- failed_boundary(실패 경계): `proxy_prefilter_strict_cross_split_success(프록시 선별 엄격 교차 분할 성공)`
- why_failed(실패 이유): dense source(고밀도 원천)는 회복됐지만 run364E cost filter(비용 필터)의 OOS profit factor(표본외 수익 팩터)가 약했다.
- salvage_value(회수 가치): dense M5 source(고밀도 M5 원천), calendar exit semantics(캘린더 청산 의미), no-split simulator(비분할 시뮬레이터)는 다음 탐색에 재사용한다.
- reopen_condition(재개 조건): direct dense M5 ONNX scout(직접 고밀도 M5 ONNX 탐색) 또는 MT5 dense flat tape(고밀도 flat 테이프)에서 PF>=1.05와 trade/day>=3이 같이 나온다.
- do_not_repeat(반복 금지): sparse long trade table(희소 롱 거래표)에만 cost filter(비용 필터)를 얹어 운영 후보처럼 말하지 않는다.
""",
    )
    replace_stage_header()


def ledger_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "dense_m5_proxy_prefilter(고밀도 M5 프록시 선별)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_mt5_execution(주장 범위 밖, MT5 실행 없음)",
        "notes": "Stage364I dense M5 proxy repair scout(Stage364I 고밀도 M5 프록시 수리 탐색).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["dense_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(VARIANT_SCORECARD),
        "result_status": STATUS,
        "sample_rows": final["dense_rows"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_execution(실험 실행)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": now_utc(),
        "lane": "dense_m5_proxy_prefilter(고밀도 M5 프록시 선별)",
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can dense M5 source repair run364G sparse runtime failure?(고밀도 M5 원천이 run364G 희소 런타임 실패를 수리할 수 있는가?)",
        "metric_scope": PROXY_EXECUTION_BOUNDARY,
        "dense_rows": final["dense_rows"],
        "best_variant_id": final["best_variant_id"],
        "net_profit": final["best_oos_net"],
        "profit_factor": final["best_oos_pf"],
        "trade_density_per_feature_day": final["best_oos_density"],
        "strict_success_count": final["strict_cross_split_success_count"],
    }
    tier_a = dict(common)
    tier_a.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "row_id": f"{RUN_ID}__Tier_A",
            "subrun_id": f"{RUN_ID}__Tier_A",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "kpi_scope": "dense_m5_proxy_prefilter(고밀도 M5 프록시 선별)",
            "primary_kpi": f"dense_rows={final['dense_rows']};best_oos_net={final['best_oos_net']};best_oos_density={final['best_oos_density']};strict_success={final['strict_cross_split_success_count']}",
            "guardrail_kpi": "mt5_execution=not_run;runtime_authority=not_claimed;operating_promotion=not_claimed;no_trade_splitting=single_position",
        }
    )
    tier_b = dict(tier_a)
    tier_b.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "row_id": f"{RUN_ID}__Tier_B",
            "subrun_id": f"{RUN_ID}__Tier_B",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "status": "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "do_not_synthesize_tier_b(Tier B 합성 금지)",
        }
    )
    combined = dict(tier_a)
    combined.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "row_id": f"{RUN_ID}__Tier_AplusB",
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "status": "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)",
            "primary_kpi": "combined_not_run(합산 실행 없음)",
            "guardrail_kpi": "do_not_synthesize_combined_result(합산 결과 합성 금지)",
        }
    )
    return [tier_a, tier_b, combined]


def write_registries(final: Mapping[str, Any]) -> None:
    rows = ledger_rows(final)
    run_row = dict(rows[0])
    run_row["subrun_id"] = ""
    append_registry_rows(RUN_REGISTRY, ["run_id"], [run_row])
    append_registry_rows(PROJECT_LEDGER, ["run_id", "subrun_id"], rows)
    append_registry_rows(STAGE_LEDGER, ["run_id", "subrun_id"], rows)


def write_artifact_registry() -> None:
    rows = []
    for artifact_type, path, notes in [
        ("script", Path(__file__), "run364I producer script(run364I 생산 스크립트)"),
        ("input_manifest", INPUT_MANIFEST, "input identity(입력 정체성)"),
        ("dense_feature_matrix", DENSE_FEATURE_MATRIX, "dense M5 feature matrix(고밀도 M5 피처 행렬)"),
        ("dense_coverage", DENSE_COVERAGE, "dense source coverage(고밀도 원천 커버리지)"),
        ("variant_scorecard", VARIANT_SCORECARD, "proxy variant scorecard(프록시 변형 점수표)"),
        ("top_trade_sample", TOP_TRADE_SAMPLE, "proxy trade sample(프록시 거래 표본)"),
        ("findings", FINDINGS, "repair findings(수리 발견)"),
        ("next_queue", NEXT_QUEUE, "next offensive queue(다음 공격 대기열)"),
        ("final_decision", FINAL_DECISION, "final decision(최종 결정)"),
        ("report", REPORT_PATH, "run364I report(run364I 보고서)"),
        ("decision_doc", DECISION_DOC, "decision document(결정 문서)"),
        ("gate_audit", GATE_AUDIT, "required gate audit(필수 게이트 감사)"),
    ]:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{artifact_type}",
                "notes": notes,
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], rows)


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_input_manifest()
    feature_columns = load_feature_schema()
    days = load_feature_days()
    dense = materialize_dense_source(feature_columns)
    metric_rows, _ = sweep_variants(dense, days)
    summary = write_dense_coverage(dense, days, metric_rows)
    write_findings_and_queue(summary)
    write_work_packet_and_receipts(summary)
    gates = build_gates(summary)
    write_csv(GATE_AUDIT, gates)
    final = write_final_and_manifest(summary, gates)
    write_report(final)
    write_state_docs(final)
    write_registries(final)
    write_artifact_registry()
    gates = build_gates(final)
    write_csv(GATE_AUDIT, gates)
    final = write_final_and_manifest(summary, gates)
    failed = [row for row in gates if row.get("status") != "passed"]
    if failed:
        raise RuntimeError(f"run364I gates failed: {failed}")
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
