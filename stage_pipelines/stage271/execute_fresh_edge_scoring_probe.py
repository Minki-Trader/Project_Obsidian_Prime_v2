from __future__ import annotations

import hashlib
import json
import sys
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE_ID = "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure"
RUN_ID = "run271D_execute_fresh_edge_scoring_probe_v1"
SOURCE_RUN_ID = "run271C_materialize_fresh_edge_scoring_handoff_inputs_v1"
NEXT_ACTION = "run271E_screen_fresh_edge_score_surfaces"
STATUS = "completed_fresh_edge_scoring_probe_no_candidate_selection"
JUDGMENT = "exploratory_score_table_materialized_no_candidate_selection"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)
FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_ROOT / "02_runs" / "run271D"
SCORES_DIR = RUN_DIR / "scores"
HANDOFF_DIR = RUN_DIR / "handoff"
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected"
RUN271C_DIR = STAGE_ROOT / "02_runs" / "run271C"

TIER_A_DATASET = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
    / "model_input_dataset.parquet"
)
TIER_A_FEATURE_ORDER = TIER_A_DATASET.with_name("model_input_feature_order.txt")
TIER_A_SUMMARY = TIER_A_DATASET.with_name("model_input_summary.json")
TIER_A_MANIFEST = TIER_A_DATASET.with_name("feature_set_manifest.json")
TIER_B_DATASET = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v1"
    / "model_input_dataset.parquet"
)
TIER_B_FEATURE_ORDER = TIER_B_DATASET.with_name("model_input_feature_order.txt")
TIER_B_SUMMARY = TIER_B_DATASET.with_name("model_input_summary.json")
TIER_B_MANIFEST = TIER_B_DATASET.with_name("feature_set_manifest.json")

SOURCE_SPECS = RUN271C_DIR / "scoring_input_specs.json"
SOURCE_HANDOFF_PLAN = RUN271C_DIR / "handoff_input_plan.csv"
SOURCE_IDENTITY = RUN271C_DIR / "package_identity_receipts.csv"
SOURCE_DATASET_PROFILE = RUN271C_DIR / "dataset_profile.json"
SOURCE_RUN_MANIFEST = RUN271C_DIR / "run_manifest.json"
SOURCE_REPORT = REVIEWS / "run271C_report.md"
BASE_ADAPTER = ROOT / "foundation" / "adapters" / "baseline_adapter.py"

SCORE_SUMMARY = RUN_DIR / "score_materialization_summary.csv"
SIGNAL_READ_SUMMARY = RUN_DIR / "signal_read_summary.csv"
WEAK_SLICE_SUMMARY = RUN_DIR / "weak_slice_score_summary.csv"
TIER_SCOPE_RECEIPTS = RUN_DIR / "tier_scope_receipts.csv"
THRESHOLD_RECEIPT = RUN_DIR / "threshold_receipt.csv"
HANDOFF_RESOLUTION = RUN_DIR / "handoff_path_resolution.csv"
SCORE_SAMPLES = RUN_DIR / "score_samples.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
RUN_REPORT = REVIEWS / "run271D_report.md"
SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = Path("stage_pipelines/stage271/execute_fresh_edge_scoring_probe.py")

STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)

PACKAGE_SHORT_IDS = {
    "cp271A_damage_first_loss_asymmetry_surface": "cp271A",
    "cp271B_time_risk_phase_router_surface": "cp271B",
    "cp271C_recovery_tail_payoff_rebalance_surface": "cp271C",
    "cp271D_stage270_reference_control_boundary": "cp271D",
}
LABEL_OR_FUTURE_COLUMNS = {
    "future_timestamp",
    "future_log_return_12",
    "label",
    "label_class",
    "label_id",
    "horizon_bars",
    "horizon_minutes",
}


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def read_json(path: Path) -> Any:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def load_feature_order(path: Path) -> list[str]:
    return [line.strip() for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def robust_z(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce").astype("float64")
    median = numeric.median(skipna=True)
    mad = (numeric - median).abs().median(skipna=True)
    scale = mad * 1.4826 if mad and np.isfinite(mad) else numeric.std(skipna=True)
    if not scale or not np.isfinite(scale):
        return pd.Series(0.0, index=series.index, dtype="float64")
    return ((numeric - median) / scale).replace([np.inf, -np.inf], np.nan).fillna(0.0).clip(-6.0, 6.0)


def sigmoid(value: pd.Series | np.ndarray) -> pd.Series:
    array = np.asarray(value, dtype="float64")
    clipped = np.clip(array, -20.0, 20.0)
    return pd.Series(1.0 / (1.0 + np.exp(-clipped)))


def col(frame: pd.DataFrame, name: str, default: float = 0.0) -> pd.Series:
    if name not in frame.columns:
        return pd.Series(default, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[name], errors="coerce").astype("float64").fillna(default)


def percentile_rank(values: pd.Series, train_mask: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce").astype("float64").replace([np.inf, -np.inf], np.nan)
    train_values = numeric[train_mask & numeric.notna()].sort_values().to_numpy()
    if len(train_values) == 0:
        return pd.Series(0.5, index=values.index, dtype="float64")
    ranks = np.searchsorted(train_values, numeric.fillna(np.nanmedian(train_values)).to_numpy(), side="right")
    return pd.Series(ranks / len(train_values), index=values.index, dtype="float64").clip(0.0, 1.0)


def train_quantile(values: pd.Series, train_mask: pd.Series, quantile: float) -> float:
    numeric = pd.to_numeric(values, errors="coerce").astype("float64")
    train_values = numeric[train_mask & numeric.notna()]
    if train_values.empty:
        return float("nan")
    return float(train_values.quantile(quantile))


def missing_features(frame: pd.DataFrame, expected_feature_order: Sequence[str]) -> list[str]:
    return [name for name in expected_feature_order if name not in frame.columns]


def prepare_view(path: Path, tier_view: str, feature_order_path: Path, expected_feature_order: Sequence[str]) -> pd.DataFrame:
    frame = pd.read_parquet(io_path(path)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    observed_feature_order = load_feature_order(feature_order_path)
    input_hash = sha256_text("\n".join(observed_feature_order))
    missing = missing_features(frame, expected_feature_order)
    for name in missing:
        frame[name] = np.nan
    frame["tier_view"] = tier_view
    frame["input_feature_order_hash"] = input_hash
    frame["expected_feature_order_hash"] = FEATURE_ORDER_HASH
    frame["missing_required_feature_count"] = len(missing)
    frame["missing_required_features"] = ";".join(missing) if missing else "none"
    frame["row_seq"] = np.arange(len(frame), dtype="int64")
    frame["chron_segment"] = chron_segment(frame)
    return frame


def chron_segment(frame: pd.DataFrame) -> pd.Series:
    if "timestamp" not in frame.columns:
        return pd.Series("unknown", index=frame.index)
    ts = pd.to_datetime(frame["timestamp"], utc=True)
    quantiles = ts.rank(method="first", pct=True)
    return pd.Series(
        np.select(
            [quantiles <= 0.25, quantiles <= 0.50, quantiles <= 0.75],
            ["chron_q1", "chron_q2", "chron_q3"],
            default="chron_q4",
        ),
        index=frame.index,
    )


def base_output(frame: pd.DataFrame, spec: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": frame["timestamp"],
            "symbol": frame.get("symbol", pd.Series("US100", index=frame.index)),
            "split": frame["split"].astype(str),
            "tier_view": frame["tier_view"],
            "package_id": spec["package_id"],
            "input_feature_order_hash": frame["input_feature_order_hash"],
            "expected_feature_order_hash": frame["expected_feature_order_hash"],
            "missing_required_feature_count": frame["missing_required_feature_count"],
            "missing_required_features": frame["missing_required_features"],
            "decision_rule_hash": spec["decision_rule_hash"],
            "risk_rule_hash": spec["risk_rule_hash"],
            "adapter_schema_hash": spec["adapter_schema_hash"],
            "score_columns_hash": spec["score_columns_hash"],
            "claim_boundary": BOUNDARY,
        }
    )


def add_evaluation_columns(output: pd.DataFrame, frame: pd.DataFrame) -> pd.DataFrame:
    route_long = col(frame, "di_spread_14") >= 0
    label = frame["label"].astype(str) if "label" in frame.columns else pd.Series("", index=frame.index)
    route_code = pd.Series(np.where(route_long, "long", "short"), index=frame.index)
    output["route_code"] = route_code
    output["label"] = label
    output["label_alignment_flag"] = ((output["materialized_decision_flag"] == 1) & route_code.eq(label)).astype("int8")
    output["evaluation_label_available"] = label.isin(["long", "short", "flat"]).astype("int8")
    return output


def weak_slice_flags(frame: pd.DataFrame) -> pd.DataFrame:
    ts = pd.to_datetime(frame["timestamp"], utc=True)
    minutes = col(frame, "minutes_from_cash_open", default=np.nan)
    hour = ts.dt.hour
    return pd.DataFrame(
        {
            "weekday": ts.dt.day_name(),
            "month": ts.dt.month.astype("int16"),
            "utc_hour": hour.astype("int16"),
            "chron_segment": frame["chron_segment"],
            "is_thursday": (ts.dt.dayofweek == 3).astype("int8"),
            "is_stage270_bad_month": ts.dt.month.isin([11]).astype("int8"),
            "is_session_risk_window": (
                ((minutes >= 0) & (minutes <= 35))
                | ((minutes >= 330) & (minutes <= 390))
                | hour.between(13, 20)
            ).astype("int8"),
            "is_chron_early": frame["chron_segment"].isin(["chron_q1", "chron_q2"]).astype("int8"),
        },
        index=frame.index,
    )


def score_cp271a(frame: pd.DataFrame, spec: Mapping[str, Any]) -> pd.DataFrame:
    train_mask = frame["split"].astype(str).eq("train")
    weak = weak_slice_flags(frame)
    recent_negative_expectancy_raw = (
        (-col(frame, "log_return_1")).clip(lower=0.0).rolling(12, min_periods=3).mean().fillna(0.0)
        + 0.55 * (-col(frame, "log_return_3")).clip(lower=0.0).rolling(24, min_periods=3).mean().fillna(0.0)
    )
    side_specific_damage_raw = (
        (col(frame, "di_spread_14") < 0).astype("float64") * (-col(frame, "log_return_3")).clip(lower=0.0)
        + (col(frame, "di_spread_14") >= 0).astype("float64") * col(frame, "log_return_3").clip(lower=0.0)
        + 0.20 * col(frame, "vix_zscore_20").abs()
    )
    weak_slice_overlap = weak[["is_thursday", "is_stage270_bad_month", "is_session_risk_window", "is_chron_early"]].sum(axis=1)
    damage_risk_raw = (
        0.40 * robust_z(recent_negative_expectancy_raw)
        + 0.25 * robust_z(side_specific_damage_raw)
        + 0.20 * robust_z(col(frame, "atr_14_over_atr_50"))
        + 0.15 * weak_slice_overlap
    )
    opportunity_raw = (
        0.25 * robust_z(col(frame, "adx_14"))
        + 0.25 * robust_z(col(frame, "di_spread_14").abs())
        + 0.18 * robust_z(col(frame, "ppo_hist_12_26_9").abs())
        + 0.17 * robust_z(col(frame, "ema20_ema50_diff").abs())
        - 0.15 * robust_z(recent_negative_expectancy_raw)
    )
    damage_risk_score = percentile_rank(damage_risk_raw, train_mask)
    opportunity_score = percentile_rank(opportunity_raw, train_mask)
    candidate_decision_score = (opportunity_score * (1.0 - 0.55 * damage_risk_score)).clip(0.0, 1.0)
    decision_threshold = train_quantile(candidate_decision_score, train_mask, 0.68)
    risk_action_code = np.select(
        [damage_risk_score >= 0.72, weak_slice_overlap >= 3, candidate_decision_score >= decision_threshold],
        ["risk_cut", "weak_slice_hold", "route_allowed"],
        default="scout_only",
    )

    output = base_output(frame, spec)
    output["loss_pressure_state"] = pd.cut(
        damage_risk_score,
        bins=[-0.01, 0.35, 0.72, 1.01],
        labels=["low_loss_pressure", "medium_loss_pressure", "high_loss_pressure"],
    ).astype(str)
    output["recent_negative_expectancy"] = recent_negative_expectancy_raw.round(10)
    output["side_specific_damage"] = side_specific_damage_raw.round(10)
    output["weak_slice_overlap"] = weak_slice_overlap.astype("int8")
    output["damage_risk_score"] = damage_risk_score.round(8)
    output["opportunity_score"] = opportunity_score.round(8)
    output["candidate_decision_score"] = candidate_decision_score.round(8)
    output["risk_action_code"] = risk_action_code
    output["materialized_decision_flag"] = (
        (candidate_decision_score >= decision_threshold) & (damage_risk_score <= 0.55) & (weak_slice_overlap <= 2)
    ).astype("int8")
    return add_evaluation_columns(output, frame)


def score_cp271b(frame: pd.DataFrame, spec: Mapping[str, Any]) -> pd.DataFrame:
    train_mask = frame["split"].astype(str).eq("train")
    weak = weak_slice_flags(frame)
    ts = pd.to_datetime(frame["timestamp"], utc=True)
    minutes = col(frame, "minutes_from_cash_open", default=np.nan).fillna(999.0)
    weekday_phase = pd.Series(
        np.select(
            [ts.dt.dayofweek == 0, ts.dt.dayofweek == 3, ts.dt.dayofweek == 4],
            ["monday_reset", "thursday_fragility", "friday_tail"],
            default="midweek_neutral",
        ),
        index=frame.index,
    )
    month_regime_pressure = percentile_rank(
        0.45 * robust_z(col(frame, "vix_zscore_20").abs())
        + 0.30 * weak["is_stage270_bad_month"]
        + 0.25 * robust_z(col(frame, "usdx_zscore_20").abs()),
        train_mask,
    )
    session_clock_risk = percentile_rank(
        0.45 * weak["is_session_risk_window"]
        + 0.25 * col(frame, "is_first_30m_after_open")
        + 0.20 * col(frame, "is_last_30m_before_cash_close")
        + 0.10 * robust_z((minutes - 195.0).abs()),
        train_mask,
    )
    chron_phase_age = percentile_rank(frame["row_seq"], train_mask)
    phase_risk_score = (
        0.32 * month_regime_pressure
        + 0.30 * session_clock_risk
        + 0.20 * weak["is_thursday"]
        + 0.18 * (1.0 - chron_phase_age)
    ).clip(0.0, 1.0)
    phase_opportunity_score = percentile_rank(
        0.30 * robust_z(col(frame, "adx_14"))
        + 0.25 * robust_z(col(frame, "ema20_ema50_diff").abs())
        + 0.20 * robust_z(col(frame, "bb_squeeze").abs())
        + 0.15 * robust_z(col(frame, "mega8_pos_breadth_1"))
        - 0.10 * robust_z(col(frame, "historical_vol_5_over_20").abs()),
        train_mask,
    )
    candidate_decision_score = (phase_opportunity_score * (1.0 - 0.45 * phase_risk_score)).clip(0.0, 1.0)
    decision_threshold = train_quantile(candidate_decision_score, train_mask, 0.66)
    risk_action_code = np.select(
        [phase_risk_score >= 0.70, session_clock_risk >= 0.72, candidate_decision_score >= decision_threshold],
        ["phase_cut", "clock_hold", "route_allowed"],
        default="scout_only",
    )

    output = base_output(frame, spec)
    output["weekday_phase"] = weekday_phase
    output["month_regime_pressure"] = month_regime_pressure.round(8)
    output["session_clock_risk"] = session_clock_risk.round(8)
    output["chron_phase_age"] = chron_phase_age.round(8)
    output["phase_risk_score"] = phase_risk_score.round(8)
    output["phase_opportunity_score"] = phase_opportunity_score.round(8)
    output["candidate_decision_score"] = candidate_decision_score.round(8)
    output["risk_action_code"] = risk_action_code
    output["materialized_decision_flag"] = (
        (candidate_decision_score >= decision_threshold) & (phase_risk_score <= 0.58)
    ).astype("int8")
    return add_evaluation_columns(output, frame)


def score_cp271c(frame: pd.DataFrame, spec: Mapping[str, Any]) -> pd.DataFrame:
    train_mask = frame["split"].astype(str).eq("train")
    weak = weak_slice_flags(frame)
    recovery_pressure_raw = (
        0.30 * (-robust_z(col(frame, "return_zscore_20")))
        + 0.22 * (50.0 - col(frame, "rsi_14")).clip(lower=0.0) / 50.0
        + 0.20 * robust_z(col(frame, "mega8_pos_breadth_1"))
        + 0.16 * robust_z(col(frame, "top3_weighted_return_1"))
        + 0.12 * robust_z(col(frame, "us100_minus_top3_weighted_return_1").abs())
    )
    fragility_raw = (
        0.30 * robust_z(col(frame, "atr_14_over_atr_50").abs())
        + 0.25 * robust_z(col(frame, "historical_vol_5_over_20").abs())
        + 0.20 * robust_z(col(frame, "hl_zscore_50").abs())
        + 0.15 * weak["is_stage270_bad_month"]
        + 0.10 * weak["is_session_risk_window"]
    )
    payoff_balance_raw = recovery_pressure_raw - 0.65 * fragility_raw
    drawdown_slope_raw = (
        (-col(frame, "log_return_1")).clip(lower=0.0).rolling(48, min_periods=6).sum().fillna(0.0)
        + (-col(frame, "log_return_3")).clip(lower=0.0).rolling(16, min_periods=4).sum().fillna(0.0)
    )
    recovery_quality_score = percentile_rank(payoff_balance_raw, train_mask)
    payoff_fragility_score = percentile_rank(fragility_raw + 0.15 * robust_z(drawdown_slope_raw), train_mask)
    thin_tail_warning = (
        (payoff_fragility_score >= 0.70)
        | ((col(frame, "bb_squeeze") >= train_quantile(col(frame, "bb_squeeze"), train_mask, 0.70)) & (recovery_quality_score <= 0.55))
    ).astype("int8")
    candidate_decision_score = (recovery_quality_score * (1.0 - 0.50 * payoff_fragility_score)).clip(0.0, 1.0)
    decision_threshold = train_quantile(candidate_decision_score, train_mask, 0.67)
    risk_action_code = np.select(
        [thin_tail_warning == 1, payoff_fragility_score >= 0.68, candidate_decision_score >= decision_threshold],
        ["thin_tail_hold", "fragility_cut", "route_allowed"],
        default="scout_only",
    )

    output = base_output(frame, spec)
    output["payoff_balance_state"] = pd.cut(
        recovery_quality_score - payoff_fragility_score,
        bins=[-1.01, -0.15, 0.15, 1.01],
        labels=["fragile_payoff", "balanced_payoff", "recovery_payoff"],
    ).astype(str)
    output["expected_recovery_pressure"] = recovery_pressure_raw.round(10)
    output["drawdown_slope_state"] = percentile_rank(drawdown_slope_raw, train_mask).round(8)
    output["thin_tail_warning"] = thin_tail_warning
    output["recovery_quality_score"] = recovery_quality_score.round(8)
    output["payoff_fragility_score"] = payoff_fragility_score.round(8)
    output["candidate_decision_score"] = candidate_decision_score.round(8)
    output["risk_action_code"] = risk_action_code
    output["materialized_decision_flag"] = (
        (candidate_decision_score >= decision_threshold)
        & (payoff_fragility_score <= 0.60)
        & (thin_tail_warning == 0)
    ).astype("int8")
    return add_evaluation_columns(output, frame)


def score_cp271d(frame: pd.DataFrame, spec: Mapping[str, Any], *, adapter_hash: str, handoff_hash: str) -> pd.DataFrame:
    input_hash = frame["input_feature_order_hash"].astype(str)
    expected_hash = frame["expected_feature_order_hash"].astype(str)
    identity_match = input_hash.eq(expected_hash).astype("int8")

    output = base_output(frame, spec)
    output["q01_reference_identity"] = "stage270_reference_only"
    output["q03_preserved_clue_identity"] = "nonfilter_failure_memory_only"
    output["decision_rule_diff_hash"] = spec["decision_rule_hash"]
    output["risk_rule_diff_hash"] = spec["risk_rule_hash"]
    output["candidate_decision_score"] = identity_match.astype("float64")
    output["risk_action_code"] = np.where(identity_match == 1, "identity_match_control", "feature_order_boundary")
    output["adapter_hash"] = adapter_hash
    output["handoff_hash"] = handoff_hash
    output["materialized_decision_flag"] = 0
    return add_evaluation_columns(output, frame)


def score_package(frame: pd.DataFrame, spec: Mapping[str, Any], *, adapter_hash: str) -> pd.DataFrame:
    package_id = str(spec["package_id"])
    handoff_hash = sha256_text(
        "|".join(
            [
                package_id,
                str(spec["feature_order_hash"]),
                str(spec["decision_rule_hash"]),
                str(spec["risk_rule_hash"]),
                str(spec["adapter_schema_hash"]),
                str(spec["score_columns_hash"]),
                adapter_hash,
                BOUNDARY,
            ]
        )
    )
    if package_id == "cp271A_damage_first_loss_asymmetry_surface":
        return score_cp271a(frame, spec)
    if package_id == "cp271B_time_risk_phase_router_surface":
        return score_cp271b(frame, spec)
    if package_id == "cp271C_recovery_tail_payoff_rebalance_surface":
        return score_cp271c(frame, spec)
    if package_id == "cp271D_stage270_reference_control_boundary":
        return score_cp271d(frame, spec, adapter_hash=adapter_hash, handoff_hash=handoff_hash)
    raise ValueError(f"Unknown package_id: {package_id}")


def summarize_scores(package_id: str, table: pd.DataFrame, score_columns: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (tier_view, split), split_frame in table.groupby(["tier_view", "split"], dropna=False):
        numeric_columns = [
            column
            for column in score_columns
            if column in split_frame.columns and pd.api.types.is_numeric_dtype(split_frame[column])
        ]
        score_min = float(split_frame[numeric_columns].min(numeric_only=True).min()) if numeric_columns else float("nan")
        score_max = float(split_frame[numeric_columns].max(numeric_only=True).max()) if numeric_columns else float("nan")
        decision_count = int(split_frame["materialized_decision_flag"].sum())
        rows.append(
            {
                "package_id": package_id,
                "tier_view": tier_view,
                "split": split,
                "rows": int(len(split_frame)),
                "score_columns": ";".join(score_columns),
                "null_score_cells": int(split_frame[list(score_columns)].isna().sum().sum()) if score_columns else 0,
                "numeric_score_min": round(score_min, 8) if np.isfinite(score_min) else "",
                "numeric_score_max": round(score_max, 8) if np.isfinite(score_max) else "",
                "materialized_decision_count": decision_count,
                "materialized_decision_rate": round(decision_count / len(split_frame), 8) if len(split_frame) else 0.0,
                "performance_claim": "none",
            }
        )
    return rows


def summarize_signal(package_id: str, table: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (tier_view, split), split_frame in table.groupby(["tier_view", "split"], dropna=False):
        decisions = split_frame[split_frame["materialized_decision_flag"] == 1]
        directional = decisions[decisions["label"].isin(["long", "short"])]
        decision_count = int(len(decisions))
        hit_rate = float(directional["label_alignment_flag"].mean()) if len(directional) else float("nan")
        long_share = float(decisions["route_code"].eq("long").mean()) if decision_count else float("nan")
        rows.append(
            {
                "package_id": package_id,
                "tier_view": tier_view,
                "split": split,
                "rows": int(len(split_frame)),
                "decision_count": decision_count,
                "decision_rate": round(decision_count / len(split_frame), 8) if len(split_frame) else 0.0,
                "directional_label_rows": int(len(directional)),
                "label_alignment_rate": round(hit_rate, 8) if np.isfinite(hit_rate) else "",
                "long_route_share": round(long_share, 8) if np.isfinite(long_share) else "",
                "short_route_share": round(1.0 - long_share, 8) if np.isfinite(long_share) else "",
                "avg_candidate_decision_score": round(float(decisions["candidate_decision_score"].mean()), 8) if decision_count else "",
                "signal_claim": "structural_alignment_only_not_trading_kpi",
            }
        )
    return rows


def summarize_weak_slices(package_id: str, table: pd.DataFrame) -> list[dict[str, Any]]:
    enriched = table.copy()
    ts = pd.to_datetime(enriched["timestamp"], utc=True)
    enriched["slice_weekday"] = ts.dt.day_name()
    enriched["slice_month"] = ts.dt.month.astype(str)
    enriched["slice_utc_hour"] = ts.dt.hour.astype(str)
    enriched["slice_chron_segment"] = pd.Series(
        np.select(
            [ts.rank(method="first", pct=True) <= 0.25, ts.rank(method="first", pct=True) <= 0.50, ts.rank(method="first", pct=True) <= 0.75],
            ["chron_q1", "chron_q2", "chron_q3"],
            default="chron_q4",
        ),
        index=enriched.index,
    )
    rows: list[dict[str, Any]] = []
    slice_specs = [
        ("weekday", "slice_weekday"),
        ("month", "slice_month"),
        ("utc_hour", "slice_utc_hour"),
        ("chron_segment", "slice_chron_segment"),
    ]
    for slice_type, column in slice_specs:
        for (tier_view, split, slice_value), group in enriched.groupby(["tier_view", "split", column], dropna=False):
            decision_count = int(group["materialized_decision_flag"].sum())
            rows.append(
                {
                    "package_id": package_id,
                    "tier_view": tier_view,
                    "split": split,
                    "slice_type": slice_type,
                    "slice_value": slice_value,
                    "rows": int(len(group)),
                    "decision_count": decision_count,
                    "decision_rate": round(decision_count / len(group), 8) if len(group) else 0.0,
                    "avg_candidate_decision_score": round(float(group["candidate_decision_score"].mean()), 8),
                    "weak_slice_claim": "screening_input_only",
                }
            )
    return rows


def threshold_rows(package_id: str, table: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for tier_view, tier_frame in table.groupby("tier_view", dropna=False):
        train_mask = tier_frame["split"].astype(str).eq("train")
        rows.append(
            {
                "package_id": package_id,
                "tier_view": tier_view,
                "score_column": "candidate_decision_score",
                "train_q50": round(train_quantile(tier_frame["candidate_decision_score"], train_mask, 0.50), 8),
                "train_q60": round(train_quantile(tier_frame["candidate_decision_score"], train_mask, 0.60), 8),
                "train_q66": round(train_quantile(tier_frame["candidate_decision_score"], train_mask, 0.66), 8),
                "train_q67": round(train_quantile(tier_frame["candidate_decision_score"], train_mask, 0.67), 8),
                "train_q68": round(train_quantile(tier_frame["candidate_decision_score"], train_mask, 0.68), 8),
                "threshold_policy": "train_split_quantile_only_no_selection",
                "selection_claim": "none",
            }
        )
    return rows


def build_handoff_payload(spec: Mapping[str, Any], table_path: Path, table_hash: str, table: pd.DataFrame, model_hash: str) -> dict[str, Any]:
    return {
        "package_id": spec["package_id"],
        "package_role": spec["package_role"],
        "feature_order_hash": spec["feature_order_hash"],
        "blueprint_hash": spec.get("blueprint_hash", ""),
        "decision_rule_hash": spec["decision_rule_hash"],
        "risk_rule_hash": spec["risk_rule_hash"],
        "adapter_schema_hash": spec["adapter_schema_hash"],
        "score_columns_hash": spec["score_columns_hash"],
        "model_hash": model_hash,
        "score_table_path": rel(table_path),
        "score_table_hash": table_hash,
        "tier_view_rows": {str(k): int(v) for k, v in table["tier_view"].value_counts().sort_index().items()},
        "input_view_feature_order_hashes": {
            str(k): str(v) for k, v in table.groupby("tier_view")["input_feature_order_hash"].first().sort_index().items()
        },
        "claim_boundary": BOUNDARY,
        "materialization_judgment": "score_table_materialized_no_candidate_selection",
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
    }


def source_hashes(paths: Sequence[Path]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in paths:
        hashes[rel(path)] = sha256_file(path) if path.suffix == ".parquet" else sha256_file_lf_normalized(path)
    return hashes


def data_integrity_payload(
    *,
    tier_a: pd.DataFrame,
    tier_b: pd.DataFrame,
    expected_feature_order: Sequence[str],
    tier_a_hash: str,
    tier_b_hash: str,
    hashes: Mapping[str, str],
) -> dict[str, Any]:
    return {
        "data_source": {
            "tier_a": rel(TIER_A_DATASET),
            "tier_b": rel(TIER_B_DATASET),
        },
        "time_axis": "timestamp(타임스탬프)는 UTC closed M5 bar(UTC 종가 5분봉) 기준이며 입력 순서를 보존했다.",
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5(5분봉)",
            "tier_a_rows": int(len(tier_a)),
            "tier_b_rows": int(len(tier_b)),
            "combined_rows": int(len(tier_a) + len(tier_b)),
            "tier_a_split_counts": {str(k): int(v) for k, v in tier_a["split"].value_counts().to_dict().items()},
            "tier_b_split_counts": {str(k): int(v) for k, v in tier_b["split"].value_counts().to_dict().items()},
        },
        "missing_or_duplicate_check": {
            "tier_a_duplicate_timestamps": int(tier_a["timestamp"].duplicated().sum()),
            "tier_b_duplicate_timestamps": int(tier_b["timestamp"].duplicated().sum()),
            "tier_a_missing_required_features": missing_features(tier_a, expected_feature_order),
            "tier_b_missing_required_features": missing_features(tier_b, expected_feature_order),
        },
        "feature_label_boundary": "label/future columns(라벨/미래 열)은 score formula(점수 공식)에 쓰지 않고 signal read(신호 판독)에만 썼다.",
        "split_boundary": "train split(학습 분할)만 percentile/quantile(백분위/분위수) 기준을 만들고 validation/oos(검증/표본외)는 읽기 전용이다.",
        "leakage_risk": "score output(점수 출력)에 label(라벨)이 포함되지만 decision flag(판단 플래그) 생성 뒤 구조 신호 판독에만 사용된다.",
        "data_hash_or_identity": {
            **dict(hashes),
            "tier_a_feature_order_hash": tier_a_hash,
            "tier_b_feature_order_hash": tier_b_hash,
            "expected_feature_order_hash": FEATURE_ORDER_HASH,
        },
        "integrity_judgment": "usable_with_boundary",
    }


def model_validation_payload() -> dict[str, Any]:
    return {
        "model_family": "deterministic rank scoring surfaces(결정적 순위 점수 표면), no trained model(학습 모델 없음)",
        "target_and_label": "label_v1_fwd12 3-class(12봉 전방 3분류 라벨)는 signal read(신호 판독)에만 사용했다.",
        "split_method": "train/validation/oos(학습/검증/표본외) fixed split(고정 분할)",
        "selection_metric": "none selected(선택 없음); run271D(271D 실행)는 materialization probe(물질화 탐침)다.",
        "secondary_metrics": "decision_rate(판단 비율), label_alignment_rate(라벨 정렬률), weak_slice_score_summary(약한 구간 점수 요약), score hashes(점수 해시)",
        "threshold_policy": "train quantile only(학습 분위수만 사용), no tuned threshold(조율 임계값 없음)",
        "overfit_risk": "fresh thesis(새 논제)가 Stage270(270단계) failure memory(실패 기억)를 보므로 run271E(271E 실행)에서 neutral slices(중립 구간)를 함께 봐야 한다.",
        "calibration_risk": "scores(점수)는 probability(확률)가 아니라 rank/ordering(순위/정렬)이다.",
        "comparison_baseline": "cp271D support control(보조 대조)과 Stage270(270단계) reference boundary(참고 경계)",
        "validation_judgment": JUDGMENT,
    }


def result_rows() -> list[dict[str, str]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "score tables;handoff json;tier receipts;threshold receipt;signal read summary;weak slice summary;data/model/lineage receipts;ledgers",
            "evidence_missing": "screened candidate package;Adapter package;MT5 runtime output;ONNX export;ONNX parity;MT5 runtime reproduction",
            "judgment_label": "exploratory_score_materialization",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "점수표(score table, 점수표)는 생겼지만 후보 선택(selected candidate, 선택 후보)은 아직 없다.",
        }
    ]


def manifest_payload(
    *,
    hashes: Mapping[str, str],
    output_hashes: Mapping[str, str],
    package_count: int,
    tier_a_rows: int,
    tier_b_rows: int,
    combined_rows: int,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "producer": rel(ROOT / PRODUCER_PATH),
        "entry_command": f"python {PRODUCER_PATH.as_posix()}",
        "created_at_utc": utc_now(),
        "source_inputs": list(hashes.keys()),
        "source_hashes": dict(hashes),
        "output_artifacts": list(output_hashes.keys()),
        "output_hashes": dict(output_hashes),
        "package_count": package_count,
        "tier_a_rows": tier_a_rows,
        "tier_b_rows": tier_b_rows,
        "combined_rows": combined_rows,
        "tier_scope_records": ["Tier A separate", "Tier B separate", "Tier A+B combined"],
        "scoreboard": "structural_scout",
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_score_materialization_only",
        "claim_boundary": BOUNDARY,
        "next_action": NEXT_ACTION,
    }


def lineage_payload(paths: Sequence[Path], hashes: Mapping[str, str]) -> dict[str, Any]:
    artifact_hashes = {rel(path): sha256_file(path) for path in paths if path_exists(path)}
    return {
        "source_inputs": dict(hashes),
        "producer": rel(ROOT / PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in paths],
        "artifact_hashes": artifact_hashes,
        "registry_links": {
            "run_registry": rel(RUN_REGISTRY),
            "alpha_ledger": rel(ALPHA_LEDGER),
            "stage_ledger": rel(STAGE_LEDGER),
            "artifact_registry": rel(ARTIFACT_REGISTRY),
        },
        "availability": "tracked_or_reproducible_from_command",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], signal_rows: Sequence[Mapping[str, Any]], tier_rows: Sequence[Mapping[str, Any]]) -> str:
    package_rows = sorted({str(row["package_id"]) for row in summary_rows})
    package_lines = "\n".join(f"- `{package_id}`" for package_id in package_rows)
    signal_preview = "\n".join(
        f"- `{row['package_id']}` / `{row['tier_view']}` / `{row['split']}`: decisions(판단) `{row['decision_count']}`, alignment(정렬률) `{row['label_alignment_rate']}`"
        for row in signal_rows
        if row["split"] in {"validation", "oos"} and row["tier_view"] == "Tier A separate"
    )
    tier_lines = "\n".join(
        f"- `{row['tier_scope']}`: rows(행) `{row['rows']}`, status(상태) `{row['materialization_status']}`"
        for row in tier_rows
    )
    return f"""# run271D Fresh Edge Scoring Probe(271D 새 거래 우위 점수 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- scoreboard(점수판): `structural_scout(구조 스카우트)`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Meaning(의미)

run271D(271D 실행)는 run271C(271C 실행)의 scoring input specs(점수 입력 규격)를 Tier A/Tier B/Tier A+B(티어 A/티어 B/티어 A+B) score table(점수표)로 물질화했다.
효과(effect, 효과): fresh edge package(새 거래 우위 패키지)를 아직 선택하지 않고, run271E(271E 실행)에서 선별할 구조 점수 근거를 만든다.

## Packages(패키지)

{package_lines}

## Tier Records(티어 기록)

{tier_lines}

## Signal Read Preview(신호 판독 미리보기)

{signal_preview}

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): score table(점수표), handoff JSON(인계 JSON), tier receipt(티어 영수증), signal read summary(신호 판독 요약)를 생성했다.
- kpi_contract_audit(KPI 계약 감사): scoreboard(점수판)는 `structural_scout(구조 스카우트)`이고 trading KPI(거래 핵심 성과 지표)는 주장하지 않는다.
- skill_receipt_lint(스킬 영수증 점검): data integrity(데이터 무결성), model validation(모델 검증), artifact lineage(산출물 계보), result judgment(결과 판정) receipt(영수증)를 남겼다.
- required_gate_coverage_audit(필수 게이트 커버리지 감사): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)을 모두 기록했다.
- final_claim_guard(최종 주장 방어): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
"""


def write_selection_status() -> None:
    text = f"""# Stage271 Selection Status(271단계 선택 상태)

- stage_status(단계 상태): `{STATUS}`
- current_packet(현재 작업 묶음): `stage271_fresh_edge_rebuild_after_nonfilter_failure_v1`
- current_run(현재 실행): `{RUN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- score_materialization_summary(점수 물질화 요약): `{rel(SCORE_SUMMARY)}`
- signal_read_summary(신호 판독 요약): `{rel(SIGNAL_READ_SUMMARY)}`
- next_action(다음 행동): `{NEXT_ACTION}`

## Current Meaning(현재 의미)

run271D(271D 실행)는 score table(점수표)을 만들었다.
효과(effect, 효과): 이제 run271E(271E 실행)에서 score surface(점수 표면)를 선별할 수 있지만, 아직 candidate package(후보 패키지) 선택이나 ONNX readiness(온엑스 준비)는 없다.

## Boundary(경계)

`{BOUNDARY}`
"""
    write_md(SELECTION_STATUS, text)


def write_review_index() -> None:
    text = f"""# Stage271 Review Index(271단계 검토 색인)

## Current State(현재 상태)

Stage271(271단계)은 run271D(271D 실행) fresh edge scoring probe(새 거래 우위 점수 탐침)까지 완료됐다.
효과(effect, 효과): score table(점수표)와 구조 신호 요약을 만들었고, 다음은 run271E(271E 실행) score surface screen(점수 표면 선별)이다.

## Reports(보고서)

- run271A report(271A 보고서): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/03_reviews/run271A_report.md`
- run271B report(271B 보고서): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/03_reviews/run271B_report.md`
- run271C report(271C 보고서): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/03_reviews/run271C_report.md`
- run271D report(271D 보고서): `{rel(RUN_REPORT)}`
- run271D score summary(271D 점수 요약): `{rel(SCORE_SUMMARY)}`
- run271D signal read summary(271D 신호 판독 요약): `{rel(SIGNAL_READ_SUMMARY)}`
"""
    write_md(REVIEW_INDEX, text)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def update_state_docs(package_count: int, tier_a_rows: int, tier_b_rows: int, combined_rows: int) -> None:
    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `fresh_edge_score_surfaces`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run271D_summary(271D 요약)",
        f"- run271D_summary(271D 요약): run271D(271D 실행)는 package(패키지) `{package_count}`개에 Tier A separate(Tier A 분리) `{tier_a_rows}`행, Tier B separate(Tier B 분리) `{tier_b_rows}`행, Tier A+B combined(Tier A+B 합산) `{combined_rows}`행의 score table(점수표)을 만들었다. Effect(효과): run271E(271E 실행)가 score surface(점수 표면)를 선별할 수 있지만 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage271(271단계) run271D(271D 실행) fresh edge scoring probe(새 거래 우위 점수 탐침) `{RUN_ID}`. "
        f"Effect(효과): package(패키지) `{package_count}`개에 Tier A/Tier B/Tier A+B(티어 A/티어 B/티어 A+B) score table(점수표)을 만들었고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage271(271단계) run271D(271D 실행)")
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run271D fresh edge scoring probe(271D 새 거래 우위 점수 탐침)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): Tier A/Tier B/Tier A+B(티어 A/티어 B/티어 A+B) score table(점수표)과 handoff(인계) receipt(영수증)를 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def update_registers(created_at: str, artifacts: Sequence[Path], package_count: int, tier_a_rows: int, tier_b_rows: int, combined_rows: int) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"package_rows={package_count};tier_a_rows={tier_a_rows};tier_b_rows={tier_b_rows};combined_rows={combined_rows};selected_candidate=none;onnx_readiness=not_claimed.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_score_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_a_score_materialization",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier A score table(티어 A 점수표)",
            "tier_scope": "Tier A separate",
            "kpi_scope": "structural_signal_score_materialization",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(SCORE_SUMMARY),
            "primary_kpi": f"rows={tier_a_rows};packages={package_count}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;trading_kpi=none",
            "external_verification_status": "out_of_scope_by_claim_score_materialization_only",
            "notes": "Tier A full-context score table materialized.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_score_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_score_materialization",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier B score table(티어 B 점수표)",
            "tier_scope": "Tier B separate",
            "kpi_scope": "structural_signal_score_materialization",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": "materialized_partial_context_score_table_with_boundary",
            "path": rel(TIER_SCOPE_RECEIPTS),
            "primary_kpi": f"rows={tier_b_rows};packages={package_count}",
            "guardrail_kpi": "partial_context_missing_features_recorded;no_fallback_authority_claimed",
            "external_verification_status": "out_of_scope_by_claim_score_materialization_only",
            "notes": "Tier B partial-context score table materialized with missing-feature receipt.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_ab_score_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_ab_score_materialization",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier A+B score table(티어 A+B 점수표)",
            "tier_scope": "Tier A+B combined",
            "kpi_scope": "structural_signal_score_materialization",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": "materialized_combined_view_no_routed_pnl_claim",
            "path": rel(TIER_SCOPE_RECEIPTS),
            "primary_kpi": f"rows={combined_rows};packages={package_count}",
            "guardrail_kpi": "performance_claim=none;synthetic_materialization_view_only",
            "external_verification_status": "out_of_scope_by_claim_score_materialization_only",
            "notes": "Combined row is score materialization view, not routed account performance.",
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__score_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_edge_scoring_probe",
                "tier_scope": "Tier A+B paired score materialization",
                "scoreboard": "structural_scout",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "score_table_only_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"package_rows={package_count};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    if path_exists(ARTIFACT_REGISTRY):
        existing = [row for row in read_csv_rows(ARTIFACT_REGISTRY) if str(row.get("run_id", "")).strip() != RUN_ID]
        write_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, existing)
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run271D_score_materialization_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run271D fresh edge scoring probe artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def execute() -> dict[str, Any]:
    sources = [
        SOURCE_SPECS,
        SOURCE_HANDOFF_PLAN,
        SOURCE_IDENTITY,
        SOURCE_DATASET_PROFILE,
        SOURCE_RUN_MANIFEST,
        SOURCE_REPORT,
        TIER_A_DATASET,
        TIER_A_FEATURE_ORDER,
        TIER_A_SUMMARY,
        TIER_A_MANIFEST,
        TIER_B_DATASET,
        TIER_B_FEATURE_ORDER,
        TIER_B_SUMMARY,
        TIER_B_MANIFEST,
        BASE_ADAPTER,
    ]
    must_exist(sources)
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(SCORES_DIR).mkdir(parents=True, exist_ok=True)
    io_path(HANDOFF_DIR).mkdir(parents=True, exist_ok=True)

    specs = read_json(SOURCE_SPECS)
    identity_rows = read_csv_rows(SOURCE_IDENTITY)
    identity_by_package = {row["package_id"]: row for row in identity_rows}
    expected_feature_order = load_feature_order(TIER_A_FEATURE_ORDER)
    tier_a_hash = sha256_text("\n".join(expected_feature_order))
    if tier_a_hash != FEATURE_ORDER_HASH:
        raise ValueError(f"Tier A feature hash mismatch: {tier_a_hash} != {FEATURE_ORDER_HASH}")
    tier_b_feature_order = load_feature_order(TIER_B_FEATURE_ORDER)
    tier_b_hash = sha256_text("\n".join(tier_b_feature_order))

    tier_a = prepare_view(TIER_A_DATASET, "Tier A separate", TIER_A_FEATURE_ORDER, expected_feature_order)
    tier_b = prepare_view(TIER_B_DATASET, "Tier B separate", TIER_B_FEATURE_ORDER, expected_feature_order)
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.*",
            category=FutureWarning,
        )
        combined = pd.concat([tier_a, tier_b], ignore_index=True, sort=False)
    combined["combined_view_label"] = "Tier A+B combined score materialization view; no routed PnL"

    hashes = source_hashes(sources)
    adapter_hash = sha256_file(BASE_ADAPTER)
    score_summary_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    weak_rows: list[dict[str, Any]] = []
    threshold_receipt_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    score_sample_rows: list[dict[str, Any]] = []
    score_paths: list[Path] = []
    handoff_paths: list[Path] = []

    for raw_spec in specs["packages"]:
        package_id = str(raw_spec["package_id"])
        spec = {**raw_spec, **identity_by_package.get(package_id, {})}
        short_id = PACKAGE_SHORT_IDS[package_id]
        model_hash = sha256_text(json.dumps(json_ready(spec), ensure_ascii=False, sort_keys=True))
        table = score_package(combined, spec, adapter_hash=adapter_hash)
        score_columns = list(spec["score_columns"])
        table_path = SCORES_DIR / f"{short_id}_fresh_edge_scores.parquet"
        table.to_parquet(io_path(table_path), index=False)
        table_hash = sha256_file(table_path)
        score_paths.append(table_path)
        score_summary_rows.extend(summarize_scores(package_id, table, score_columns))
        signal_rows.extend(summarize_signal(package_id, table))
        weak_rows.extend(summarize_weak_slices(package_id, table))
        threshold_receipt_rows.extend(threshold_rows(package_id, table))

        sample = table.groupby(["tier_view", "split"], dropna=False).head(1)
        for _, row in sample.iterrows():
            payload = {
                "package_id": package_id,
                "tier_view": row["tier_view"],
                "split": row["split"],
                "timestamp": row["timestamp"].isoformat(),
                "materialized_decision_flag": int(row["materialized_decision_flag"]),
                "candidate_decision_score": float(row["candidate_decision_score"]),
                "risk_action_code": row["risk_action_code"],
                "route_code": row["route_code"],
            }
            score_sample_rows.append(payload)

        handoff_payload = build_handoff_payload(spec, table_path, table_hash, table, model_hash)
        handoff_path = HANDOFF_DIR / f"{short_id}.json"
        write_json(handoff_path, handoff_payload)
        handoff_paths.append(handoff_path)
        handoff_rows.append(
            {
                "package_id": package_id,
                "score_table_path": rel(table_path),
                "score_table_hash": table_hash,
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file(handoff_path),
                "path_resolution_reason": "compact_stage271_run271D_handoff_path",
            }
        )

    tier_receipt_rows = [
        {
            "tier_scope": "Tier A separate",
            "source_path": rel(TIER_A_DATASET),
            "feature_order_hash": tier_a_hash,
            "rows": int(len(tier_a)),
            "missing_required_features": "none",
            "materialization_status": "materialized_full_context_score_inputs",
            "performance_claim": "none",
        },
        {
            "tier_scope": "Tier B separate",
            "source_path": rel(TIER_B_DATASET),
            "feature_order_hash": tier_b_hash,
            "rows": int(len(tier_b)),
            "missing_required_features": tier_b["missing_required_features"].iloc[0],
            "materialization_status": "materialized_partial_context_score_inputs",
            "performance_claim": "none",
        },
        {
            "tier_scope": "Tier A+B combined",
            "source_path": "synthetic_score_materialization_view_from_tier_a_and_tier_b_score_tables",
            "feature_order_hash": f"TierA={tier_a_hash};TierB={tier_b_hash}",
            "rows": int(len(combined)),
            "missing_required_features": "see_component_rows",
            "materialization_status": "materialized_combined_score_input_view_no_routed_pnl",
            "performance_claim": "none",
        },
    ]
    write_csv(
        SCORE_SUMMARY,
        (
            "package_id",
            "tier_view",
            "split",
            "rows",
            "score_columns",
            "null_score_cells",
            "numeric_score_min",
            "numeric_score_max",
            "materialized_decision_count",
            "materialized_decision_rate",
            "performance_claim",
        ),
        score_summary_rows,
    )
    write_csv(
        SIGNAL_READ_SUMMARY,
        (
            "package_id",
            "tier_view",
            "split",
            "rows",
            "decision_count",
            "decision_rate",
            "directional_label_rows",
            "label_alignment_rate",
            "long_route_share",
            "short_route_share",
            "avg_candidate_decision_score",
            "signal_claim",
        ),
        signal_rows,
    )
    write_csv(
        WEAK_SLICE_SUMMARY,
        (
            "package_id",
            "tier_view",
            "split",
            "slice_type",
            "slice_value",
            "rows",
            "decision_count",
            "decision_rate",
            "avg_candidate_decision_score",
            "weak_slice_claim",
        ),
        weak_rows,
    )
    write_csv(
        TIER_SCOPE_RECEIPTS,
        (
            "tier_scope",
            "source_path",
            "feature_order_hash",
            "rows",
            "missing_required_features",
            "materialization_status",
            "performance_claim",
        ),
        tier_receipt_rows,
    )
    write_csv(
        THRESHOLD_RECEIPT,
        (
            "package_id",
            "tier_view",
            "score_column",
            "train_q50",
            "train_q60",
            "train_q66",
            "train_q67",
            "train_q68",
            "threshold_policy",
            "selection_claim",
        ),
        threshold_receipt_rows,
    )
    write_csv(
        HANDOFF_RESOLUTION,
        (
            "package_id",
            "score_table_path",
            "score_table_hash",
            "handoff_path",
            "handoff_hash",
            "path_resolution_reason",
        ),
        handoff_rows,
    )
    write_json(SCORE_SAMPLES, score_sample_rows)
    write_json(
        DATA_INTEGRITY_RECEIPT,
        data_integrity_payload(
            tier_a=tier_a,
            tier_b=tier_b,
            expected_feature_order=expected_feature_order,
            tier_a_hash=tier_a_hash,
            tier_b_hash=tier_b_hash,
            hashes=hashes,
        ),
    )
    write_json(MODEL_VALIDATION_RECEIPT, model_validation_payload())
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows())

    provisional_artifacts = [
        *score_paths,
        *handoff_paths,
        SCORE_SUMMARY,
        SIGNAL_READ_SUMMARY,
        WEAK_SLICE_SUMMARY,
        TIER_SCOPE_RECEIPTS,
        THRESHOLD_RECEIPT,
        HANDOFF_RESOLUTION,
        SCORE_SAMPLES,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
    ]
    output_hashes = {rel(path): sha256_file(path) for path in provisional_artifacts if path_exists(path)}
    write_json(
        RUN_MANIFEST,
        manifest_payload(
            hashes=hashes,
            output_hashes=output_hashes,
            package_count=len(specs["packages"]),
            tier_a_rows=int(len(tier_a)),
            tier_b_rows=int(len(tier_b)),
            combined_rows=int(len(combined)),
        ),
    )
    write_md(RUN_REPORT, report_markdown(score_summary_rows, signal_rows, tier_receipt_rows))
    write_selection_status()
    write_review_index()

    artifacts = [
        RUN_MANIFEST,
        *provisional_artifacts,
        RUN_REPORT,
        SELECTION_STATUS,
        REVIEW_INDEX,
    ]
    write_json(ARTIFACT_LINEAGE_RECEIPT, lineage_payload([*artifacts, ARTIFACT_LINEAGE_RECEIPT], hashes))
    artifacts.append(ARTIFACT_LINEAGE_RECEIPT)
    created_at = utc_now()
    update_registers(created_at, artifacts, len(specs["packages"]), int(len(tier_a)), int(len(tier_b)), int(len(combined)))
    update_state_docs(len(specs["packages"]), int(len(tier_a)), int(len(tier_b)), int(len(combined)))
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "package_rows": len(specs["packages"]),
        "tier_a_rows": int(len(tier_a)),
        "tier_b_rows": int(len(tier_b)),
        "combined_rows": int(len(combined)),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


def main() -> int:
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
