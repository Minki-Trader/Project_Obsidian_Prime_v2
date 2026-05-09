from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, replace
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.features.session_calendar import (
    BROKER_CLOCK_TIMEZONE,
    SESSION_TIMEZONE,
    broker_clock_key_to_event_utc,
)
from foundation.mt5 import runtime_support as mt5


SIGNAL_FEATURE_ORDER = ("stage42_session_reliability_signal",)
BAR_MINUTES = 5
MAX_CASH_SESSION_MINUTES = 390
REQUIRED_REFERENCE_FEATURES = ("return_zscore_20", "adx_14")
SESSION_FEATURE_COLUMNS = (
    "stage42_timestamp_utc",
    "stage42_broker_server_timestamp",
    "stage42_day_of_week",
    "stage42_hour_of_day",
    "stage42_minute_bucket",
    "stage42_cash_open_proximity_minutes",
    "stage42_cash_close_proximity_minutes",
    "stage42_early_cash_session_flag",
    "stage42_mid_session_flag",
    "stage42_late_cash_session_flag",
    "stage42_overnight_futures_like_flag",
    "stage42_session_transition_flag",
    "stage42_first_30_minutes_flag",
    "stage42_first_60_minutes_flag",
    "stage42_last_30_minutes_flag",
    "stage42_last_60_minutes_flag",
    "stage42_lunch_midday_lull_flag",
    "stage42_session_bucket_id",
    "stage42_session_bucket_label",
)


@dataclass(frozen=True)
class SessionStructureCandidateSpec:
    candidate_id: str
    label: str
    mechanism_family: str
    rule_code: str
    model_family: str = "score_table_rule"
    thresholds: Mapping[str, float] | None = None
    changes_entry_eligibility: bool = True
    scoring_only: bool = False
    direction_specific: bool = False
    long_short_scope: str = "both"
    expected_trade_count_effect: str = "moderate"
    overfit_risk: str = "medium"
    notes: str = ""

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["thresholds"] = dict(self.thresholds or {})
        return payload


def _numeric(frame: pd.DataFrame, column: str, fallback: float = np.nan) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(fallback, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce")


def _finite(series: pd.Series) -> pd.Series:
    return np.isfinite(pd.to_numeric(series, errors="coerce"))


def _safe_divide(numerator: Any, denominator: Any) -> Any:
    with np.errstate(divide="ignore", invalid="ignore"):
        result = np.asarray(numerator, dtype="float64") / np.asarray(denominator, dtype="float64")
    if np.ndim(result) == 0:
        number = float(result)
        return number if math.isfinite(number) else np.nan
    result = pd.Series(result).replace([np.inf, -np.inf], np.nan)
    return result


def _quantile(series: pd.Series, q: float, fallback: float) -> float:
    values = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty:
        return float(fallback)
    value = float(values.quantile(float(q)))
    return value if math.isfinite(value) else float(fallback)


def session_structure_schema() -> list[dict[str, Any]]:
    return [
        {
            "column": "stage42_timestamp_utc",
            "formula": "broker-clock timestamp key converted through Europe/Athens broker clock to UTC event time",
            "timestamp_rule": "closed M5 bar close; no partial current bar",
            "warmup": 0,
            "missingness": "NaT if timestamp missing or timezone conversion fails",
            "used_directly_in_mt5": False,
        },
        {
            "column": "stage42_broker_server_timestamp",
            "formula": "source timestamp retained as broker/server timestamp key used by MT5 feature CSV matching",
            "timestamp_rule": "closed M5 bar close key",
            "warmup": 0,
            "missingness": "NaT if source timestamp missing",
            "used_directly_in_mt5": False,
        },
        {
            "column": "stage42_day_of_week",
            "formula": "UTC event timestamp dayofweek",
            "timestamp_rule": "derived from stage42_timestamp_utc",
            "warmup": 0,
            "missingness": "NaN if UTC timestamp missing",
            "used_directly_in_mt5": False,
        },
        {
            "column": "stage42_hour_of_day",
            "formula": "UTC event timestamp hour",
            "timestamp_rule": "derived from stage42_timestamp_utc",
            "warmup": 0,
            "missingness": "NaN if UTC timestamp missing",
            "used_directly_in_mt5": False,
        },
        {
            "column": "stage42_minute_bucket",
            "formula": "floor(minutes_from_cash_open / 30) * 30",
            "timestamp_rule": "closed-bar cash-session minute",
            "warmup": 0,
            "missingness": "NA when minutes_from_cash_open missing",
            "used_directly_in_mt5": False,
        },
        {
            "column": "stage42_cash_open_proximity_minutes",
            "formula": "abs(minutes_from_cash_open)",
            "timestamp_rule": "closed-bar cash-session minute",
            "warmup": 0,
            "missingness": "NaN when minutes_from_cash_open missing",
            "used_directly_in_mt5": False,
        },
        {
            "column": "stage42_cash_close_proximity_minutes",
            "formula": "abs(390 - minutes_from_cash_open)",
            "timestamp_rule": "closed-bar cash-session minute",
            "warmup": 0,
            "missingness": "NaN when minutes_from_cash_open missing",
            "used_directly_in_mt5": False,
        },
        {
            "column": "stage42_session_bucket_label",
            "formula": "cash_open_0_30, early_cash_30_60, morning_60_120, midday_lull_120_240, late_cash_240_330, cash_close_330_390, overnight_or_unmapped",
            "timestamp_rule": "bucket from closed-bar minutes_from_cash_open",
            "warmup": 0,
            "missingness": "overnight_or_unmapped when minute is missing or outside cash bounds",
            "used_directly_in_mt5": False,
        },
        {
            "column": "stage42_session_reliability_signal",
            "formula": "candidate-specific -1/0/+1 discrete signal exported to MT5 score-table runtime",
            "timestamp_rule": "same closed-bar timestamp as feature CSV",
            "warmup": 0,
            "missingness": "0 when required session/reference feature is missing",
            "used_directly_in_mt5": True,
        },
    ]


def materialize_session_structure(frame: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" not in frame.columns:
        raise ValueError("missing timestamp column")
    out = frame.copy()
    timestamp_key = pd.to_datetime(out["timestamp"], utc=True, errors="coerce")
    out["timestamp"] = timestamp_key
    out["stage42_broker_server_timestamp"] = timestamp_key
    try:
        event_utc = broker_clock_key_to_event_utc(timestamp_key)
    except Exception:
        event_utc = timestamp_key
    out["stage42_timestamp_utc"] = event_utc
    out["stage42_timestamp_timezone_rule"] = "broker_clock_key_to_event_utc"
    out["stage42_broker_clock_timezone"] = BROKER_CLOCK_TIMEZONE
    out["stage42_session_timezone"] = SESSION_TIMEZONE
    out["stage42_timezone_ambiguity_note"] = "raw MT5 timestamps are broker-clock keys; timestamp is retained for MT5 matching and converted UTC is diagnostic"
    out["stage42_day_of_week"] = event_utc.dt.dayofweek.astype("float64")
    out["stage42_hour_of_day"] = event_utc.dt.hour.astype("float64")
    out["stage42_utc_minute_of_day"] = (event_utc.dt.hour * 60 + event_utc.dt.minute).astype("float64")

    minutes = _numeric(out, "minutes_from_cash_open")
    if minutes.isna().all():
        timestamp_ny = event_utc.dt.tz_convert(SESSION_TIMEZONE)
        session_open = timestamp_ny.dt.normalize() + pd.Timedelta(hours=9, minutes=30)
        minutes = (timestamp_ny - session_open).dt.total_seconds() / 60.0
    out["stage42_minutes_from_cash_open"] = minutes
    out["stage42_minute_bucket"] = (np.floor(minutes / 30.0) * 30.0).where(_finite(minutes))
    out["stage42_cash_open_proximity_minutes"] = minutes.abs()
    out["stage42_cash_close_proximity_minutes"] = (MAX_CASH_SESSION_MINUTES - minutes).abs()
    out["stage42_first_30_minutes_flag"] = ((minutes > 0) & (minutes <= 30)).astype("int8")
    out["stage42_first_60_minutes_flag"] = ((minutes > 0) & (minutes <= 60)).astype("int8")
    out["stage42_last_30_minutes_flag"] = ((minutes >= 360) & (minutes <= 390)).astype("int8")
    out["stage42_last_60_minutes_flag"] = ((minutes >= 330) & (minutes <= 390)).astype("int8")
    out["stage42_early_cash_session_flag"] = ((minutes > 0) & (minutes <= 60)).astype("int8")
    out["stage42_mid_session_flag"] = ((minutes > 120) & (minutes < 270)).astype("int8")
    out["stage42_late_cash_session_flag"] = ((minutes >= 270) & (minutes <= 390)).astype("int8")
    out["stage42_lunch_midday_lull_flag"] = ((minutes >= 120) & (minutes <= 240)).astype("int8")
    cash_like = (minutes > 0) & (minutes <= MAX_CASH_SESSION_MINUTES)
    out["stage42_overnight_futures_like_flag"] = (~cash_like.fillna(False)).astype("int8")
    out["stage42_session_transition_flag"] = (
        out["stage42_first_30_minutes_flag"].eq(1) | out["stage42_last_30_minutes_flag"].eq(1)
    ).astype("int8")

    labels = np.select(
        [
            (minutes > 0) & (minutes <= 30),
            (minutes > 30) & (minutes <= 60),
            (minutes > 60) & (minutes <= 120),
            (minutes > 120) & (minutes <= 240),
            (minutes > 240) & (minutes <= 330),
            (minutes > 330) & (minutes <= 390),
        ],
        [
            "cash_open_0_30",
            "early_cash_30_60",
            "morning_60_120",
            "midday_lull_120_240",
            "late_cash_240_330",
            "cash_close_330_390",
        ],
        default="overnight_or_unmapped",
    )
    out["stage42_session_bucket_label"] = pd.Series(labels, index=out.index).astype("string")
    bucket_map = {
        "overnight_or_unmapped": 0,
        "cash_open_0_30": 1,
        "early_cash_30_60": 2,
        "morning_60_120": 3,
        "midday_lull_120_240": 4,
        "late_cash_240_330": 5,
        "cash_close_330_390": 6,
    }
    out["stage42_session_bucket_id"] = out["stage42_session_bucket_label"].map(bucket_map).fillna(0).astype("int16")
    return out


def session_distribution(frame: pd.DataFrame) -> dict[str, dict[str, int]]:
    if "stage42_session_bucket_label" not in frame.columns:
        raise ValueError("session features are not materialized")
    distribution: dict[str, dict[str, int]] = {}
    for split, split_frame in frame.groupby(frame["split"].astype(str), dropna=False):
        distribution[str(split)] = {
            str(key): int(value)
            for key, value in split_frame["stage42_session_bucket_label"].astype(str).value_counts(dropna=False).items()
        }
    return distribution


def session_lineage_rows(source_data_path: str) -> list[dict[str, Any]]:
    rows = []
    for item in session_structure_schema():
        rows.append(
            {
                "column": item["column"],
                "source_data_path": source_data_path,
                "source_symbol": "US100",
                "timeframe": "M5",
                "timestamp_rule": item["timestamp_rule"],
                "ohlc_column_mapping": "not_used_timestamp_only" if "signal" not in item["column"] else "candidate_signal_from_closed_bar_features",
                "calculation_formula": item["formula"],
                "warmup_requirement": item["warmup"],
                "missingness_behavior": item["missingness"],
                "used_directly_in_mt5": item["used_directly_in_mt5"],
                "python_candidate_design_only": not bool(item["used_directly_in_mt5"]),
            }
        )
    return rows


def build_stage42_broad_candidate_grid() -> list[SessionStructureCandidateSpec]:
    items = [
        ("c01_reference_no_session_structure", "reference runtime signal without session structure", "reference", "reference_no_session", "score_table_rule", False, False, "both", "reference", "low"),
        ("c02_session_feature_low_complexity", "low-complexity model with session features included", "session feature model", "session_feature_low_complexity", "session_reliability_score_table", True, True, "both", "moderate", "medium"),
        ("c03_cash_open_only_reliability", "cash-open reliability candidate", "cash open reliability", "cash_open_only", "score_table_rule", True, False, "both", "lower", "medium_high"),
        ("c04_early_cash_session_reliability", "first 60 minutes / early session candidate", "early cash reliability", "early_cash_only", "score_table_rule", True, False, "both", "lower", "medium"),
        ("c05_mid_session_reliability", "mid-session candidate", "mid-session reliability", "mid_session_only", "score_table_rule", True, False, "both", "lower", "medium"),
        ("c06_cash_close_reliability", "late / close session candidate", "cash close reliability", "cash_close_only", "score_table_rule", True, False, "both", "lower", "medium_high"),
        ("c07_overnight_reliability", "overnight/futures-like candidate", "overnight reliability", "overnight_only", "score_table_rule", True, False, "both", "much lower", "high"),
        ("c08_exclude_weak_session_bucket", "remove weakest session bucket from reference signal", "weak session exclusion", "exclude_weakest_bucket", "session_reliability_score_table", True, False, "both", "slightly lower", "medium"),
        ("c09_session_specific_thresholds", "session-specific confidence thresholds", "session thresholds", "session_specific_thresholds", "session_reliability_score_table", True, True, "both", "moderate", "medium"),
        ("c10_session_specific_long_short_thresholds", "session-specific long/short thresholds", "directional session thresholds", "session_specific_long_short_thresholds", "session_directional_score_table", True, True, "both", "moderate", "medium_high"),
        ("c11_session_adjusted_label_recheck", "broad session-adjusted label recheck", "broad session label read", "session_adjusted_label_recheck", "session_label_balance_score", True, True, "both", "moderate", "medium_high"),
        ("c12_session_calibration_layer", "calibration by session bucket", "session calibration", "session_calibration_layer", "session_reliability_score_table", True, True, "both", "lower", "medium"),
        ("c13_session_reliability_score", "compact session reliability score", "session reliability score", "session_reliability_score", "session_reliability_score_table", True, True, "both", "moderate", "medium"),
        ("c14_session_and_volatility_interaction", "session x volatility interaction", "session volatility interaction", "session_volatility_interaction", "score_table_rule", True, True, "both", "lower", "medium_high"),
        ("c15_session_and_spread_proxy_interaction", "session x execution/spread proxy", "session spread interaction", "session_spread_proxy_interaction", "score_table_rule", True, True, "both", "lower", "medium_high"),
        ("c16_direction_specific_session_model", "long/short separate session model", "direction-specific session model", "direction_specific_session_model", "session_directional_score_table", True, True, "both", "moderate", "high"),
        ("c17_session_extreme_stress", "extreme stress for session-only read", "extreme stress", "session_extreme_stress", "session_reliability_score_table", True, True, "both", "much lower", "high"),
    ]
    return [
        SessionStructureCandidateSpec(
            candidate_id=candidate_id,
            label=label,
            mechanism_family=family,
            rule_code=rule,
            model_family=model_family,
            changes_entry_eligibility=changes_entry,
            scoring_only=scoring_only,
            direction_specific="long_short" in rule or "direction" in rule,
            long_short_scope=scope,
            expected_trade_count_effect=effect,
            overfit_risk=risk,
        )
        for candidate_id, label, family, rule, model_family, changes_entry, scoring_only, scope, effect, risk in items
    ]


def build_stage42_micro_candidate_grid(
    best_candidate_id: str,
    broad_specs: Sequence[SessionStructureCandidateSpec],
) -> list[SessionStructureCandidateSpec]:
    base = next(spec for spec in broad_specs if spec.candidate_id == best_candidate_id)
    variants = [
        ("m01_session_threshold_relaxed", {"session_strength_min": -0.02, "return_multiplier": 0.90}),
        ("m02_session_threshold_firm", {"session_strength_min": 0.03, "return_multiplier": 1.05}),
        ("m03_less_concentrated_bucket_mix", {"max_bucket_share": 0.60, "return_multiplier": 0.95}),
        ("m04_directional_session_balance", {"directional_strength_min": 0.02, "return_multiplier": 1.00}),
    ]
    return [
        replace(
            base,
            candidate_id=f"{suffix}_{base.candidate_id}",
            label=f"{base.label} micro {suffix}",
            thresholds=thresholds,
            notes="bounded Stage42 micro-search around a broad session/time-structure candidate",
        )
        for suffix, thresholds in variants
    ]


def build_reference_thresholds(frame: pd.DataFrame) -> dict[str, float]:
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    return {
        "return_abs_q62": _quantile(_numeric(train, "return_zscore_20").abs(), 0.62, 0.60),
        "return_abs_q70": _quantile(_numeric(train, "return_zscore_20").abs(), 0.70, 0.80),
        "adx_q45": _quantile(_numeric(train, "adx_14"), 0.45, 20.0),
        "adx_q60": _quantile(_numeric(train, "adx_14"), 0.60, 25.0),
        "vol_q50": _quantile(_numeric(train, "historical_vol_20"), 0.50, 0.001),
        "spread_q70": _quantile(_numeric(train, "stage42_spread_points"), 0.70, 200.0),
    }


def reference_signal(frame: pd.DataFrame, thresholds: Mapping[str, float], multiplier: float = 1.0) -> pd.Series:
    rz = _numeric(frame, "return_zscore_20")
    adx = _numeric(frame, "adx_14")
    ret = float(thresholds.get("return_abs_q62", 0.60)) * float(multiplier)
    adx_min = float(thresholds.get("adx_q45", 20.0))
    signal = pd.Series(0, index=frame.index, dtype="int8")
    signal.loc[rz.ge(ret) & adx.ge(adx_min)] = 1
    signal.loc[rz.le(-ret) & adx.ge(adx_min)] = -1
    signal.loc[~(_finite(rz) & _finite(adx))] = 0
    return signal


def build_session_reliability_model(frame: pd.DataFrame, thresholds: Mapping[str, float]) -> dict[str, Any]:
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    train_signal = reference_signal(train, thresholds)
    labels = pd.to_numeric(train.get("label_class"), errors="coerce")
    target_direction = pd.Series(0, index=train.index, dtype="int8")
    target_direction.loc[labels.eq(2)] = 1
    target_direction.loc[labels.eq(0)] = -1
    active = train_signal.ne(0)
    rows = []
    global_hit = float((train_signal.loc[active] == target_direction.loc[active]).mean()) if active.any() else 0.50
    global_hit = global_hit if math.isfinite(global_hit) else 0.50
    bucket_labels = sorted(frame["stage42_session_bucket_label"].astype(str).unique())
    for bucket in bucket_labels:
        bucket_mask = train["stage42_session_bucket_label"].astype(str).eq(bucket)
        bucket_active = active & bucket_mask
        count = int(bucket_active.sum())
        hit_rate = float((train_signal.loc[bucket_active] == target_direction.loc[bucket_active]).mean()) if count else global_hit
        if not math.isfinite(hit_rate):
            hit_rate = global_hit
        long_mask = bucket_active & train_signal.eq(1)
        short_mask = bucket_active & train_signal.eq(-1)
        long_hit = float((target_direction.loc[long_mask] == 1).mean()) if int(long_mask.sum()) else hit_rate
        short_hit = float((target_direction.loc[short_mask] == -1).mean()) if int(short_mask.sum()) else hit_rate
        rows.append(
            {
                "bucket": bucket,
                "train_signal_count": count,
                "hit_rate": hit_rate,
                "score": hit_rate - 0.50,
                "long_signal_count": int(long_mask.sum()),
                "long_hit_rate": long_hit if math.isfinite(long_hit) else hit_rate,
                "long_score": (long_hit if math.isfinite(long_hit) else hit_rate) - 0.50,
                "short_signal_count": int(short_mask.sum()),
                "short_hit_rate": short_hit if math.isfinite(short_hit) else hit_rate,
                "short_score": (short_hit if math.isfinite(short_hit) else hit_rate) - 0.50,
            }
        )
    if not rows:
        rows.append({"bucket": "missing", "train_signal_count": 0, "hit_rate": global_hit, "score": 0.0, "long_signal_count": 0, "long_hit_rate": global_hit, "long_score": 0.0, "short_signal_count": 0, "short_hit_rate": global_hit, "short_score": 0.0})
    weakest = min(rows, key=lambda row: (row["hit_rate"], -row["train_signal_count"]))
    strongest = max(rows, key=lambda row: (row["hit_rate"], row["train_signal_count"]))
    return {
        "model_family": "session_reliability_score_table",
        "global_hit_rate": global_hit,
        "rows": rows,
        "weakest_bucket": weakest["bucket"],
        "strongest_bucket": strongest["bucket"],
        "score_by_bucket": {row["bucket"]: row["score"] for row in rows},
        "long_score_by_bucket": {row["bucket"]: row["long_score"] for row in rows},
        "short_score_by_bucket": {row["bucket"]: row["short_score"] for row in rows},
    }


def _bucket_score(frame: pd.DataFrame, model: Mapping[str, Any], key: str = "score_by_bucket") -> pd.Series:
    mapping = model.get(key, {})
    if not isinstance(mapping, Mapping):
        mapping = {}
    return frame["stage42_session_bucket_label"].astype(str).map(mapping).fillna(0.0).astype("float64")


def apply_candidate_to_table(
    frame: pd.DataFrame,
    spec: SessionStructureCandidateSpec,
    thresholds: Mapping[str, float],
    reliability_model: Mapping[str, Any],
) -> pd.DataFrame:
    if "stage42_session_bucket_label" not in frame.columns:
        raise ValueError("session features are not materialized")
    out = frame.copy()
    overrides = dict(spec.thresholds or {})
    multiplier = float(overrides.get("return_multiplier", 1.0))
    base = reference_signal(out, thresholds, multiplier=multiplier)
    minutes = _numeric(out, "stage42_minutes_from_cash_open")
    bucket = out["stage42_session_bucket_label"].astype(str)
    score = _bucket_score(out, reliability_model)
    long_score = _bucket_score(out, reliability_model, "long_score_by_bucket")
    short_score = _bucket_score(out, reliability_model, "short_score_by_bucket")
    weak = str(reliability_model.get("weakest_bucket", ""))
    strong = str(reliability_model.get("strongest_bucket", ""))
    vol = _numeric(out, "historical_vol_20")
    spread = _numeric(out, "stage42_spread_points")
    signal = base.copy()
    activation = pd.Series(False, index=out.index)
    rule = spec.rule_code
    if rule == "reference_no_session":
        activation = base.ne(0)
    elif rule == "session_feature_low_complexity":
        keep = score.ge(float(overrides.get("session_strength_min", -0.01)))
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    elif rule == "cash_open_only":
        keep = minutes.gt(0) & minutes.le(30)
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    elif rule == "early_cash_only":
        keep = minutes.gt(0) & minutes.le(60)
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    elif rule == "mid_session_only":
        keep = minutes.gt(120) & minutes.lt(270)
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    elif rule == "cash_close_only":
        keep = minutes.ge(330) & minutes.le(390)
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    elif rule == "overnight_only":
        keep = out["stage42_overnight_futures_like_flag"].eq(1)
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    elif rule == "exclude_weakest_bucket":
        keep = ~bucket.eq(weak)
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    elif rule == "session_specific_thresholds":
        adaptive = np.where(score.ge(0.04), 0.90, np.where(score.lt(-0.02), 1.15, 1.0))
        signal = reference_signal(out, thresholds, multiplier=1.0).where(base.ne(0), 0)
        signal = reference_signal(out.assign(return_zscore_20=_numeric(out, "return_zscore_20") / adaptive), thresholds).astype("int8")
        activation = score.ne(0)
    elif rule == "session_specific_long_short_thresholds":
        long_ok = base.eq(1) & long_score.ge(float(overrides.get("directional_strength_min", -0.02)))
        short_ok = base.eq(-1) & short_score.ge(float(overrides.get("directional_strength_min", -0.02)))
        signal = pd.Series(0, index=out.index, dtype="int8")
        signal.loc[long_ok] = 1
        signal.loc[short_ok] = -1
        activation = long_ok | short_ok
    elif rule == "session_adjusted_label_recheck":
        keep = score.ge(0.0) | bucket.eq(strong)
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    elif rule == "session_calibration_layer":
        strong_abs = _numeric(out, "return_zscore_20").abs().ge(float(thresholds.get("return_abs_q70", 0.8)))
        keep = score.ge(0.02) & strong_abs
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    elif rule == "session_reliability_score":
        keep = score.ge(float(overrides.get("session_strength_min", 0.0)))
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    elif rule == "session_volatility_interaction":
        keep = score.ge(-0.01) & vol.ge(float(thresholds.get("vol_q50", 0.001)))
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    elif rule == "session_spread_proxy_interaction":
        spread_ok = spread.le(float(thresholds.get("spread_q70", 200.0))) | spread.isna()
        keep = score.ge(-0.01) & spread_ok
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    elif rule == "direction_specific_session_model":
        long_ok = base.eq(1) & long_score.ge(0.0)
        short_ok = base.eq(-1) & short_score.ge(0.0)
        signal = pd.Series(0, index=out.index, dtype="int8")
        signal.loc[long_ok] = 1
        signal.loc[short_ok] = -1
        activation = long_ok | short_ok
    elif rule == "session_extreme_stress":
        keep = bucket.eq(strong) & _numeric(out, "return_zscore_20").abs().ge(float(thresholds.get("return_abs_q70", 0.8)))
        signal = base.where(keep, 0).astype("int8")
        activation = keep
    else:
        raise ValueError(f"unknown Stage42 rule_code: {rule}")
    out["stage42_reference_signal"] = base.astype("int8")
    out["stage42_session_reliability_score"] = score
    out["stage42_session_long_score"] = long_score
    out["stage42_session_short_score"] = short_score
    out["stage42_session_activation"] = activation.astype("int8")
    out["stage42_session_reliability_signal"] = signal.fillna(0).astype("int8")
    out["entry_decision"] = out["stage42_session_reliability_signal"]
    out["candidate_id"] = spec.candidate_id
    out["candidate_label"] = spec.label
    out["rule_code"] = spec.rule_code
    return out


def summarize_candidate_frames(
    frames: Mapping[str, pd.DataFrame],
    specs: Sequence[SessionStructureCandidateSpec],
    reliability_model: Mapping[str, Any],
) -> list[dict[str, Any]]:
    specs_by_id = {spec.candidate_id: spec for spec in specs}
    rows: list[dict[str, Any]] = []
    reference_counts: dict[str, int] = {}
    if "c01_reference_no_session_structure" in frames:
        ref = frames["c01_reference_no_session_structure"]
        for split, split_frame in ref.groupby(ref["split"].astype(str)):
            reference_counts[str(split)] = int(split_frame["stage42_session_reliability_signal"].ne(0).sum())
    for candidate_id, frame in frames.items():
        spec = specs_by_id[candidate_id]
        for split, split_frame in frame.groupby(frame["split"].astype(str)):
            if split not in {"validation", "oos"}:
                continue
            runtime_split = "validation_is" if split == "validation" else "oos"
            signal = pd.to_numeric(split_frame["stage42_session_reliability_signal"], errors="coerce").fillna(0)
            active = signal.ne(0)
            tier_a = split_frame["tier_label"].astype(str).eq(mt5.TIER_A) if "tier_label" in split_frame else pd.Series(False, index=split_frame.index)
            tier_b = split_frame["tier_label"].astype(str).eq(mt5.TIER_B) if "tier_label" in split_frame else pd.Series(False, index=split_frame.index)
            by_bucket = split_frame.loc[active, "stage42_session_bucket_label"].astype(str).value_counts()
            dominant_share = float(by_bucket.max() / max(int(active.sum()), 1)) if int(active.sum()) else 0.0
            best_bucket = str(by_bucket.index[0]) if len(by_bucket) else "none"
            worst_bucket = str(by_bucket.index[-1]) if len(by_bucket) else "none"
            ref_count = reference_counts.get(str(split), int(active.sum()))
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "candidate_label": spec.label,
                    "split": runtime_split,
                    "session_feature_set": spec.mechanism_family,
                    "session_bucket_definitions": "0-30 open, 30-60 early, 60-120 morning, 120-240 midday, 240-330 late, 330-390 close, outside unmapped",
                    "model_family_or_rule_family": spec.model_family,
                    "thresholds": json.dumps(spec.thresholds or {}, ensure_ascii=False, sort_keys=True),
                    "train_session_counts": json.dumps(session_distribution(frame).get("train", {}), ensure_ascii=False, sort_keys=True),
                    "validation_session_counts": json.dumps(session_distribution(frame).get("validation", {}), ensure_ascii=False, sort_keys=True),
                    "oos_session_counts": json.dumps(session_distribution(frame).get("oos", {}), ensure_ascii=False, sort_keys=True),
                    "tier_a_used_count": int((active & tier_a).sum()),
                    "tier_b_fallback_used_count": int((active & tier_b).sum()),
                    "actual_routed_total_count": int(active.sum()),
                    "validation_trade_count": int(active.sum()) if runtime_split == "validation_is" else "",
                    "oos_trade_count": int(active.sum()) if runtime_split == "oos" else "",
                    "long_count": int(signal.gt(0).sum()),
                    "short_count": int(signal.lt(0).sum()),
                    "no_trade_rate": float(1.0 - active.mean()) if len(split_frame) else 0.0,
                    "trade_count_thinning_vs_reference": int(active.sum()) - int(ref_count),
                    "session_activation_rate": float(pd.to_numeric(split_frame["stage42_session_activation"], errors="coerce").fillna(0).gt(0).mean()) if len(split_frame) else 0.0,
                    "per_session_trade_count": json.dumps({str(key): int(value) for key, value in by_bucket.items()}, ensure_ascii=False, sort_keys=True),
                    "session_concentration_share": dominant_share,
                    "worst_session_bucket": worst_bucket,
                    "best_session_bucket": best_bucket,
                    "weakest_train_session_bucket": reliability_model.get("weakest_bucket"),
                    "strongest_train_session_bucket": reliability_model.get("strongest_bucket"),
                    "candidate_rejection_reason": "mt5_pending",
                }
            )
    return rows


def per_session_attribution(frame: pd.DataFrame, candidate_id: str) -> list[dict[str, Any]]:
    if "future_log_return_12" in frame.columns:
        forward_return = _numeric(frame, "future_log_return_12").fillna(0.0)
    elif "label" in frame.columns:
        forward_return = _numeric(frame, "label").fillna(0.0)
    else:
        forward_return = pd.Series(0.0, index=frame.index)
    signal = pd.to_numeric(frame["stage42_session_reliability_signal"], errors="coerce").fillna(0.0)
    proxy_pnl = signal * forward_return
    work = frame.assign(stage42_proxy_pnl=proxy_pnl, stage42_signal_abs=signal.abs())
    rows = []
    for split, split_frame in work.groupby(work["split"].astype(str), dropna=False):
        if split not in {"validation", "oos"}:
            continue
        for bucket, bucket_frame in split_frame.groupby(split_frame["stage42_session_bucket_label"].astype(str), dropna=False):
            active = bucket_frame.loc[bucket_frame["stage42_signal_abs"].gt(0)]
            wins = active.loc[active["stage42_proxy_pnl"].gt(0), "stage42_proxy_pnl"].sum()
            losses = abs(active.loc[active["stage42_proxy_pnl"].lt(0), "stage42_proxy_pnl"].sum())
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "split": "validation_is" if split == "validation" else "oos",
                    "session_bucket": str(bucket),
                    "per_session_net_profit_proxy": float(active["stage42_proxy_pnl"].sum()) if len(active) else 0.0,
                    "per_session_pf_proxy": float(wins / losses) if losses > 0 else (float("inf") if wins > 0 else 0.0),
                    "per_session_trade_count_proxy": int(len(active)),
                    "per_session_drawdown_proxy": float(active["stage42_proxy_pnl"].cumsum().sub(active["stage42_proxy_pnl"].cumsum().cummax()).min()) if len(active) else 0.0,
                }
            )
    return rows


def session_concentration_rejection(row: Mapping[str, Any], *, max_share: float = 0.70, min_trades: int = 20) -> str | None:
    trade_count = int(float(row.get("actual_routed_total_count") or 0))
    share = float(row.get("session_concentration_share") or 0.0)
    if trade_count < min_trades:
        return "session_bucket_trade_count_too_thin"
    if share > max_share:
        return "one_session_concentration_too_high"
    return None
