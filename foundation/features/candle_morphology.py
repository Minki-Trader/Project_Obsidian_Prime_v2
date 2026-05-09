from __future__ import annotations

import json
import math
from dataclasses import dataclass, replace
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.mt5 import runtime_support as mt5


SIGNAL_FEATURE_ORDER = ("stage40_candle_morphology_signal",)
RAW_OHLC_COLUMNS = ("open", "high", "low", "close")
MORPHOLOGY_COLUMNS = (
    "candle_body_size",
    "candle_full_range",
    "candle_upper_wick",
    "candle_lower_wick",
    "candle_body_range_ratio",
    "candle_wick_asymmetry",
    "candle_close_location_in_range",
    "candle_outside_bar_flag",
    "candle_inside_bar_flag",
    "candle_adverse_outside_long",
    "candle_adverse_outside_short",
    "candle_rejection_tail_up",
    "candle_rejection_tail_down",
    "candle_wide_range_doji_like",
    "candle_impulse_body_flag",
    "candle_narrow_range_compression",
    "candle_expansion_after_compression",
    "candle_prior_range_ratio",
    "candle_directional_morphology_score",
)
REQUIRED_BASE_FEATURES = ("return_zscore_20", "adx_14")
REQUIRED_FEATURES = (*REQUIRED_BASE_FEATURES, *MORPHOLOGY_COLUMNS)


@dataclass(frozen=True)
class CandleMorphologyCandidateSpec:
    candidate_id: str
    label: str
    mechanism_family: str
    rule_code: str
    changes_entry_eligibility: bool
    scoring_only: bool = False
    direction_specific: bool = False
    long_short_scope: str = "both"
    expected_trade_count_effect: str = "moderate"
    over_thinning_risk: str = "medium"
    threshold_family: str = "broad_train_quantile_v1"
    threshold_overrides: Mapping[str, float] | None = None
    notes: str = ""


def _numeric(frame: pd.DataFrame, column: str, fallback: float = 0.0) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(fallback, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce")


def _finite_mask(frame: pd.DataFrame, columns: Sequence[str]) -> pd.Series:
    if not columns:
        return pd.Series(True, index=frame.index)
    mask = pd.Series(True, index=frame.index)
    for column in columns:
        if column not in frame.columns:
            return pd.Series(False, index=frame.index)
        mask &= np.isfinite(pd.to_numeric(frame[column], errors="coerce"))
    return mask


def _safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    denom = pd.to_numeric(denominator, errors="coerce").replace(0.0, np.nan)
    return (pd.to_numeric(numerator, errors="coerce") / denom).replace([np.inf, -np.inf], np.nan)


def _quantile(series: pd.Series, q: float, fallback: float) -> float:
    values = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty:
        return float(fallback)
    value = float(values.quantile(float(q)))
    return value if math.isfinite(value) else float(fallback)


def candle_morphology_schema() -> list[dict[str, Any]]:
    return [
        {"column": "candle_body_size", "formula": "abs(close - open)", "warmup": 0, "missingness": "NaN if OHLC missing"},
        {"column": "candle_full_range", "formula": "high - low", "warmup": 0, "missingness": "NaN if OHLC missing or range negative"},
        {"column": "candle_upper_wick", "formula": "high - max(open, close)", "warmup": 0, "missingness": "NaN if OHLC missing"},
        {"column": "candle_lower_wick", "formula": "min(open, close) - low", "warmup": 0, "missingness": "NaN if OHLC missing"},
        {"column": "candle_body_range_ratio", "formula": "body_size / full_range", "warmup": 0, "missingness": "NaN when full_range is zero"},
        {"column": "candle_wick_asymmetry", "formula": "(upper_wick - lower_wick) / full_range", "warmup": 0, "missingness": "NaN when full_range is zero"},
        {"column": "candle_close_location_in_range", "formula": "(close - low) / full_range", "warmup": 0, "missingness": "NaN when full_range is zero"},
        {"column": "candle_outside_bar_flag", "formula": "high > prior_high and low < prior_low", "warmup": 1, "missingness": "False on first aligned row"},
        {"column": "candle_inside_bar_flag", "formula": "high < prior_high and low > prior_low", "warmup": 1, "missingness": "False on first aligned row"},
        {"column": "candle_adverse_outside_long", "formula": "outside_bar and bearish body", "warmup": 1, "missingness": "False when outside flag unavailable"},
        {"column": "candle_adverse_outside_short", "formula": "outside_bar and bullish body", "warmup": 1, "missingness": "False when outside flag unavailable"},
        {"column": "candle_rejection_tail_up", "formula": "upper_wick/full_range >= train q75 and close_location <= 0.55", "warmup": 0, "missingness": "False when ratios unavailable"},
        {"column": "candle_rejection_tail_down", "formula": "lower_wick/full_range >= train q75 and close_location >= 0.45", "warmup": 0, "missingness": "False when ratios unavailable"},
        {"column": "candle_wide_range_doji_like", "formula": "full_range >= train q75 and body_range_ratio <= train q25", "warmup": 0, "missingness": "False when ratios unavailable"},
        {"column": "candle_impulse_body_flag", "formula": "body_range_ratio >= train q75 and full_range >= train q60", "warmup": 0, "missingness": "False when ratios unavailable"},
        {"column": "candle_narrow_range_compression", "formula": "full_range <= train q25 or range/prior20_median <= train q25", "warmup": 20, "missingness": "False until prior20 median exists"},
        {"column": "candle_expansion_after_compression", "formula": "prior bar compression and current range >= train q67", "warmup": 21, "missingness": "False until prior compression exists"},
        {"column": "candle_prior_range_ratio", "formula": "current full_range / prior full_range", "warmup": 1, "missingness": "NaN when prior range unavailable"},
        {"column": "candle_directional_morphology_score", "formula": "bullish impulse/lower-tail/close-high minus bearish impulse/upper-tail/close-low/adverse outside", "warmup": 1, "missingness": "0 when component flags unavailable"},
    ]


def materialize_candle_morphology(raw_bars: pd.DataFrame) -> pd.DataFrame:
    required = {"time_close_unix", *RAW_OHLC_COLUMNS}
    missing = required.difference(raw_bars.columns)
    if missing:
        raise ValueError(f"missing raw OHLC columns: {sorted(missing)}")
    bars = raw_bars.copy()
    bars["timestamp"] = pd.to_datetime(bars["time_close_unix"], unit="s", utc=True)
    bars = bars.sort_values("timestamp").drop_duplicates("timestamp", keep="last").reset_index(drop=True)
    open_ = _numeric(bars, "open")
    high = _numeric(bars, "high")
    low = _numeric(bars, "low")
    close = _numeric(bars, "close")
    body = (close - open_).abs()
    full_range = high - low
    upper = high - pd.concat([open_, close], axis=1).max(axis=1)
    lower = pd.concat([open_, close], axis=1).min(axis=1) - low
    close_location = _safe_divide(close - low, full_range)
    body_ratio = _safe_divide(body, full_range)
    upper_ratio = _safe_divide(upper, full_range)
    lower_ratio = _safe_divide(lower, full_range)
    prior_high = high.shift(1)
    prior_low = low.shift(1)
    prior_range = full_range.shift(1)
    outside = (high > prior_high) & (low < prior_low)
    inside = (high < prior_high) & (low > prior_low)
    prior20_median = full_range.shift(1).rolling(20, min_periods=20).median()
    range_to_prior20 = _safe_divide(full_range, prior20_median)
    train_like = bars
    range_q25 = _quantile(train_like.assign(_r=full_range)["_r"], 0.25, 10.0)
    range_q60 = _quantile(train_like.assign(_r=full_range)["_r"], 0.60, 20.0)
    range_q67 = _quantile(train_like.assign(_r=full_range)["_r"], 0.67, 25.0)
    range_q75 = _quantile(train_like.assign(_r=full_range)["_r"], 0.75, 30.0)
    body_q25 = _quantile(body_ratio, 0.25, 0.20)
    body_q75 = _quantile(body_ratio, 0.75, 0.65)
    upper_wick_q75 = _quantile(upper_ratio, 0.75, 0.45)
    lower_wick_q75 = _quantile(lower_ratio, 0.75, 0.45)
    range_ratio_q25 = _quantile(range_to_prior20, 0.25, 0.70)
    narrow = full_range.le(range_q25) | range_to_prior20.le(range_ratio_q25)
    expansion = narrow.shift(1, fill_value=False) & full_range.ge(range_q67)
    impulse = body_ratio.ge(body_q75) & full_range.ge(range_q60)
    upper_rejection = upper_ratio.ge(upper_wick_q75) & close_location.le(0.55)
    lower_rejection = lower_ratio.ge(lower_wick_q75) & close_location.ge(0.45)
    wide_doji = full_range.ge(range_q75) & body_ratio.le(body_q25)
    bullish_body = close.gt(open_)
    bearish_body = close.lt(open_)
    score = (
        (impulse & bullish_body).astype(int)
        + lower_rejection.astype(int)
        + close_location.ge(0.70).astype(int)
        - (impulse & bearish_body).astype(int)
        - upper_rejection.astype(int)
        - close_location.le(0.30).astype(int)
        - (outside & bearish_body).astype(int)
        + (outside & bullish_body).astype(int)
    )
    out = bars[["timestamp", "contract_symbol", "broker_symbol", "timeframe", *RAW_OHLC_COLUMNS]].copy()
    out["candle_body_size"] = body
    out["candle_full_range"] = full_range
    out["candle_upper_wick"] = upper
    out["candle_lower_wick"] = lower
    out["candle_body_range_ratio"] = body_ratio
    out["candle_wick_asymmetry"] = _safe_divide(upper - lower, full_range)
    out["candle_close_location_in_range"] = close_location
    out["candle_outside_bar_flag"] = outside.fillna(False).astype("int8")
    out["candle_inside_bar_flag"] = inside.fillna(False).astype("int8")
    out["candle_adverse_outside_long"] = (outside & bearish_body).fillna(False).astype("int8")
    out["candle_adverse_outside_short"] = (outside & bullish_body).fillna(False).astype("int8")
    out["candle_rejection_tail_up"] = upper_rejection.fillna(False).astype("int8")
    out["candle_rejection_tail_down"] = lower_rejection.fillna(False).astype("int8")
    out["candle_wide_range_doji_like"] = wide_doji.fillna(False).astype("int8")
    out["candle_impulse_body_flag"] = impulse.fillna(False).astype("int8")
    out["candle_narrow_range_compression"] = narrow.fillna(False).astype("int8")
    out["candle_expansion_after_compression"] = expansion.fillna(False).astype("int8")
    out["candle_prior_range_ratio"] = _safe_divide(full_range, prior_range)
    out["candle_directional_morphology_score"] = score.astype("int16")
    out["candle_morphology_warmup_ready"] = prior20_median.notna().astype("int8")
    out["candle_morphology_missing"] = ~_finite_mask(out, ("candle_body_size", "candle_full_range", "candle_body_range_ratio"))
    return out


def build_thresholds(common: pd.DataFrame) -> dict[str, float]:
    train = common.loc[common["split"].astype(str).eq("train") & _finite_mask(common, REQUIRED_FEATURES)].copy()
    return {
        "return_abs_q60": _quantile(_numeric(train, "return_zscore_20").abs(), 0.60, 0.35),
        "return_abs_q67": _quantile(_numeric(train, "return_zscore_20").abs(), 0.67, 0.50),
        "adx_q50": _quantile(_numeric(train, "adx_14"), 0.50, 20.0),
        "morph_score_abs_q50": _quantile(_numeric(train, "candle_directional_morphology_score").abs(), 0.50, 1.0),
        "morph_score_abs_q75": _quantile(_numeric(train, "candle_directional_morphology_score").abs(), 0.75, 2.0),
    }


def candidate_thresholds(base: Mapping[str, float], spec: CandleMorphologyCandidateSpec) -> dict[str, float]:
    out = {str(key): float(value) for key, value in base.items()}
    for key, value in (spec.threshold_overrides or {}).items():
        out[str(key)] = float(value)
    return out


def build_broad_candidate_grid(threshold_family: str = "broad_train_quantile_v1") -> list[CandleMorphologyCandidateSpec]:
    items = [
        ("c01_reference_no_candle_morphology", "reference without candle morphology", "reference/carry comparison", "reference_no_candle", True, False, False, "both", "reference", "low"),
        ("c02_outside_bar_context", "outside bar as context only", "outside bar context", "outside_context", True, False, False, "both", "lower", "medium"),
        ("c03_adverse_outside_bar_filter", "adverse outside bar filter", "adverse outside filter", "adverse_outside_filter", True, False, True, "both", "slightly lower", "medium"),
        ("c04_adverse_outside_bar_directional_long", "long-side adverse outside bar only", "directional adverse outside", "adverse_outside_long_only", True, False, True, "long_only", "slightly lower", "medium"),
        ("c05_adverse_outside_bar_directional_short", "short-side adverse outside bar only", "directional adverse outside", "adverse_outside_short_only", True, False, True, "short_only", "slightly lower", "medium"),
        ("c06_rejection_tail_context", "rejection tail as context only", "rejection tail context", "rejection_tail_context", True, False, False, "both", "lower", "high"),
        ("c07_rejection_tail_directional", "direction-aware rejection tail", "directional rejection tail", "rejection_tail_directional", True, False, True, "both", "lower", "high"),
        ("c08_wide_range_doji_negative_control", "wide-range doji-like negative control", "negative control", "wide_range_doji_negative_control", True, False, False, "both", "lower", "high"),
        ("c09_impulse_body_context", "impulse body context", "impulse body context", "impulse_body_context", True, False, False, "both", "lower", "medium"),
        ("c10_impulse_body_directional", "direction-aware impulse body", "directional impulse body", "impulse_body_directional", True, False, True, "both", "lower", "medium"),
        ("c11_narrow_range_compression_context", "narrow-range compression context", "compression context", "narrow_compression_context", True, False, False, "both", "lower", "high"),
        ("c12_expansion_after_compression_context", "expansion after compression context", "expansion after compression", "expansion_after_compression", True, False, False, "both", "lower", "medium"),
        ("c13_outside_bar_plus_rejection_tail", "outside bar plus rejection tail", "combined outside/rejection", "outside_plus_rejection", True, False, True, "both", "much lower", "high"),
        ("c14_outside_bar_plus_impulse_body", "outside bar plus impulse body", "combined outside/impulse", "outside_plus_impulse", True, False, True, "both", "much lower", "high"),
        ("c15_morphology_score_low_complexity", "low-complexity morphology score", "low-complexity score", "morphology_score_low_complexity", True, True, True, "both", "moderate", "medium"),
        ("c16_directional_morphology_score", "long/short separate morphology score", "directional score", "directional_morphology_score", True, True, True, "both", "moderate", "medium"),
        ("c17_morphology_contrast_extreme_sweep", "extreme threshold stress test", "extreme score stress", "morphology_score_extreme", True, True, True, "both", "much lower", "high"),
    ]
    return [
        CandleMorphologyCandidateSpec(
            candidate_id=candidate_id,
            label=label,
            mechanism_family=family,
            rule_code=rule_code,
            changes_entry_eligibility=entry,
            scoring_only=scoring,
            direction_specific=directional,
            long_short_scope=scope,
            expected_trade_count_effect=effect,
            over_thinning_risk=risk,
            threshold_family=threshold_family,
        )
        for candidate_id, label, family, rule_code, entry, scoring, directional, scope, effect, risk in items
    ]


def _reference_masks(frame: pd.DataFrame, thresholds: Mapping[str, float]) -> tuple[pd.Series, pd.Series]:
    rz = _numeric(frame, "return_zscore_20")
    adx = _numeric(frame, "adx_14")
    ret = float(thresholds["return_abs_q67"])
    adx_min = float(thresholds["adx_q50"])
    return rz.ge(ret) & adx.ge(adx_min), rz.le(-ret) & adx.ge(adx_min)


def _rule_masks(frame: pd.DataFrame, thresholds: Mapping[str, float], rule_code: str) -> tuple[pd.Series, pd.Series, Sequence[str], pd.Series]:
    ref_long, ref_short = _reference_masks(frame, thresholds)
    outside = _numeric(frame, "candle_outside_bar_flag").ge(0.5)
    adverse_long = _numeric(frame, "candle_adverse_outside_long").ge(0.5)
    adverse_short = _numeric(frame, "candle_adverse_outside_short").ge(0.5)
    rej_up = _numeric(frame, "candle_rejection_tail_up").ge(0.5)
    rej_down = _numeric(frame, "candle_rejection_tail_down").ge(0.5)
    doji = _numeric(frame, "candle_wide_range_doji_like").ge(0.5)
    impulse = _numeric(frame, "candle_impulse_body_flag").ge(0.5)
    narrow = _numeric(frame, "candle_narrow_range_compression").ge(0.5)
    expansion = _numeric(frame, "candle_expansion_after_compression").ge(0.5)
    score = _numeric(frame, "candle_directional_morphology_score")
    body_ratio = _numeric(frame, "candle_body_range_ratio")
    close_loc = _numeric(frame, "candle_close_location_in_range")
    scope = pd.Series(True, index=frame.index)
    score_mid = max(float(thresholds["morph_score_abs_q50"]), 1.0)
    score_extreme = max(float(thresholds["morph_score_abs_q75"]), 2.0)
    if rule_code == "reference_no_candle":
        long = ref_long
        short = ref_short
        activation = scope
    elif rule_code == "outside_context":
        long = ref_long & outside
        short = ref_short & outside
        activation = outside
    elif rule_code == "adverse_outside_filter":
        long = ref_long & ~adverse_long
        short = ref_short & ~adverse_short
        activation = adverse_long | adverse_short
    elif rule_code == "adverse_outside_long_only":
        long = ref_long & ~adverse_long
        short = ref_short
        activation = adverse_long
    elif rule_code == "adverse_outside_short_only":
        long = ref_long
        short = ref_short & ~adverse_short
        activation = adverse_short
    elif rule_code == "rejection_tail_context":
        activation = rej_up | rej_down
        long = ref_long & activation
        short = ref_short & activation
    elif rule_code == "rejection_tail_directional":
        activation = rej_up | rej_down
        long = ref_long & rej_down
        short = ref_short & rej_up
    elif rule_code == "wide_range_doji_negative_control":
        long = ref_long & doji
        short = ref_short & doji
        activation = doji
    elif rule_code == "impulse_body_context":
        long = ref_long & impulse
        short = ref_short & impulse
        activation = impulse
    elif rule_code == "impulse_body_directional":
        bullish = impulse & close_loc.ge(0.55) & body_ratio.ge(0.5)
        bearish = impulse & close_loc.le(0.45) & body_ratio.ge(0.5)
        long = ref_long & bullish
        short = ref_short & bearish
        activation = bullish | bearish
    elif rule_code == "narrow_compression_context":
        long = ref_long & narrow
        short = ref_short & narrow
        activation = narrow
    elif rule_code == "expansion_after_compression":
        long = ref_long & expansion
        short = ref_short & expansion
        activation = expansion
    elif rule_code == "outside_plus_rejection":
        long = ref_long & outside & rej_down
        short = ref_short & outside & rej_up
        activation = outside & (rej_up | rej_down)
    elif rule_code == "outside_plus_impulse":
        long = ref_long & outside & impulse & close_loc.ge(0.55)
        short = ref_short & outside & impulse & close_loc.le(0.45)
        activation = outside & impulse
    elif rule_code == "morphology_score_low_complexity":
        long = ref_long & score.ge(score_mid)
        short = ref_short & score.le(-score_mid)
        activation = score.abs().ge(score_mid)
    elif rule_code == "directional_morphology_score":
        long = score.ge(score_mid)
        short = score.le(-score_mid)
        activation = score.abs().ge(score_mid)
    elif rule_code == "morphology_score_extreme":
        long = score.ge(score_extreme)
        short = score.le(-score_extreme)
        activation = score.abs().ge(score_extreme)
    else:
        raise ValueError(f"unknown candle morphology rule: {rule_code}")
    return long.fillna(False), short.fillna(False), REQUIRED_FEATURES, activation.fillna(False)


def apply_candidate_to_table(
    common: pd.DataFrame,
    spec: CandleMorphologyCandidateSpec,
    base_thresholds: Mapping[str, float],
) -> pd.DataFrame:
    thresholds = candidate_thresholds(base_thresholds, spec)
    long_mask, short_mask, required, activation = _rule_masks(common, thresholds, spec.rule_code)
    missing = ~_finite_mask(common, required) | _numeric(common, "candle_morphology_missing").ge(0.5)
    long_mask &= ~missing
    short_mask &= ~missing
    signal = np.select([long_mask.to_numpy(), short_mask.to_numpy()], [1, -1], default=0).astype("int32")
    out_columns = [
        "stage40_row_id",
        "timestamp",
        "timestamp_utc",
        "split",
        "validation_oos_split_label",
        "label_class",
        "tier_label",
        "routing_source",
        "partial_context_subtype",
        "tier_a_available",
        "tier_b_fallback_available",
        *REQUIRED_FEATURES,
        "candle_morphology_warmup_ready",
        "candle_morphology_missing",
    ]
    out = common[[column for column in out_columns if column in common.columns]].copy()
    out["candidate_id"] = spec.candidate_id
    out["candidate_label"] = spec.label
    out["mechanism_family"] = spec.mechanism_family
    out["rule_code"] = spec.rule_code
    out["threshold_family"] = spec.threshold_family
    out["thresholds_json"] = json.dumps(thresholds, sort_keys=True, separators=(",", ":"))
    out["changes_entry_eligibility"] = spec.changes_entry_eligibility
    out["scoring_only"] = spec.scoring_only
    out["direction_specific"] = spec.direction_specific
    out["long_short_scope"] = spec.long_short_scope
    out["expected_trade_count_effect"] = spec.expected_trade_count_effect
    out["over_thinning_risk"] = spec.over_thinning_risk
    out["stage40_surface_missing"] = missing.to_numpy()
    out["morphology_activation"] = activation.to_numpy() & ~missing.to_numpy()
    out["candidate_long_pass"] = long_mask.to_numpy()
    out["candidate_short_pass"] = short_mask.to_numpy()
    out["candidate_pass"] = long_mask.to_numpy() | short_mask.to_numpy()
    out[SIGNAL_FEATURE_ORDER[0]] = signal
    out["entry_decision"] = np.where(signal > 0, "long", np.where(signal < 0, "short", "flat"))
    return out


def split_alias(split: str) -> str:
    return "validation_is" if str(split) == "validation" else str(split)


def summarize_candidate_frames(candidate_frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    reference_counts: dict[str, int] = {}
    reference = candidate_frames.get("c01_reference_no_candle_morphology")
    for split in ("validation", "oos"):
        reference_counts[split] = 0 if reference is None else int(reference.loc[reference["split"].astype(str).eq(split), SIGNAL_FEATURE_ORDER[0]].ne(0).sum())
    rows: list[dict[str, Any]] = []
    for candidate_id, frame in candidate_frames.items():
        for split in ("validation", "oos"):
            view = frame.loc[frame["split"].astype(str).eq(split)]
            if view.empty:
                rows.append({"candidate_id": candidate_id, "split": split_alias(split), "candidate_rejection_reason": "missing_split_rows"})
                continue
            signal = view[SIGNAL_FEATURE_ORDER[0]].astype(int)
            signal_count = int(signal.ne(0).sum())
            tier_a = view.loc[view["tier_label"].astype(str).eq(mt5.TIER_A)]
            tier_b = view.loc[view["tier_label"].astype(str).eq(mt5.TIER_B)]
            tier_b_signal = int(tier_b[SIGNAL_FEATURE_ORDER[0]].ne(0).sum())
            ref_count = max(reference_counts.get(split, 0), 1)
            activation_count = int(view["morphology_activation"].astype(bool).sum())
            rejection = "mt5_pending"
            if signal_count < 20:
                rejection = "thin_trade_stream_python_signal_count_lt_20"
            elif candidate_id != "c01_reference_no_candle_morphology" and signal_count / ref_count < 0.10:
                rejection = "thin_trade_stream_vs_reference_python"
            elif signal_count and tier_b_signal / signal_count > 0.60:
                rejection = "tier_b_fallback_signal_share_gt_60pct_python"
            elif candidate_id != "c01_reference_no_candle_morphology" and activation_count / max(len(view), 1) < 0.005:
                rejection = "morphology_activation_trivial_python"
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "candidate_label": str(view["candidate_label"].iloc[0]),
                    "split": split_alias(split),
                    "mechanism_family": str(view["mechanism_family"].iloc[0]),
                    "rule_code": str(view["rule_code"].iloc[0]),
                    "threshold_family": str(view["threshold_family"].iloc[0]),
                    "thresholds": str(view["thresholds_json"].iloc[0]),
                    "enabled_morphology_features": enabled_features_for_rule(str(view["rule_code"].iloc[0])),
                    "long_short_behavior": str(view["long_short_scope"].iloc[0]),
                    "changes_entry_eligibility": bool(view["changes_entry_eligibility"].iloc[0]),
                    "scoring_only": bool(view["scoring_only"].iloc[0]),
                    "direction_specific": bool(view["direction_specific"].iloc[0]),
                    "expected_trade_count_effect": str(view["expected_trade_count_effect"].iloc[0]),
                    "over_thinning_risk": str(view["over_thinning_risk"].iloc[0]),
                    "tier_a_signal_count": int(tier_a[SIGNAL_FEATURE_ORDER[0]].ne(0).sum()),
                    "tier_b_fallback_signal_count": tier_b_signal,
                    "actual_routed_total_count": signal_count,
                    "trade_count_delta_vs_reference": int(signal_count - ref_count),
                    "long_count": int(signal.gt(0).sum()),
                    "short_count": int(signal.lt(0).sum()),
                    "flat_count": int(signal.eq(0).sum()),
                    "no_trade_rate": float(1.0 - signal_count / len(view)) if len(view) else 1.0,
                    "morphology_activation_count": activation_count,
                    "morphology_activation_rate": float(activation_count / len(view)) if len(view) else 0.0,
                    "thinning_ratio_vs_reference": float(signal_count / ref_count),
                    "tier_b_signal_share_python": float(tier_b_signal / signal_count) if signal_count else None,
                    "missing_surface_rows": int(view["stage40_surface_missing"].sum()),
                    "candidate_rejection_reason": rejection,
                }
            )
    return rows


def enabled_features_for_rule(rule_code: str) -> str:
    mapping = {
        "reference_no_candle": "none",
        "outside_context": "candle_outside_bar_flag",
        "adverse_outside_filter": "candle_adverse_outside_long,candle_adverse_outside_short",
        "adverse_outside_long_only": "candle_adverse_outside_long",
        "adverse_outside_short_only": "candle_adverse_outside_short",
        "rejection_tail_context": "candle_rejection_tail_up,candle_rejection_tail_down",
        "rejection_tail_directional": "candle_rejection_tail_up,candle_rejection_tail_down",
        "wide_range_doji_negative_control": "candle_wide_range_doji_like",
        "impulse_body_context": "candle_impulse_body_flag",
        "impulse_body_directional": "candle_impulse_body_flag,candle_close_location_in_range",
        "narrow_compression_context": "candle_narrow_range_compression",
        "expansion_after_compression": "candle_expansion_after_compression",
        "outside_plus_rejection": "candle_outside_bar_flag,candle_rejection_tail_up,candle_rejection_tail_down",
        "outside_plus_impulse": "candle_outside_bar_flag,candle_impulse_body_flag",
        "morphology_score_low_complexity": "candle_directional_morphology_score",
        "directional_morphology_score": "candle_directional_morphology_score",
        "morphology_score_extreme": "candle_directional_morphology_score",
    }
    return mapping.get(rule_code, "")


def route_coverage_from_common(common: pd.DataFrame, no_tier_by_split: Mapping[str, Any] | None = None) -> dict[str, Any]:
    by_split: dict[str, dict[str, int]] = {}
    subtype: dict[str, dict[str, int]] = {}
    no_tier_by_split = no_tier_by_split or {}
    for split in ("validation", "oos"):
        view = common.loc[common["split"].astype(str).eq(split)]
        tier_a_rows = int(view["tier_label"].astype(str).eq(mt5.TIER_A).sum())
        tier_b_rows = int(view["tier_label"].astype(str).eq(mt5.TIER_B).sum())
        by_split[split] = {
            "tier_a_primary_rows": tier_a_rows,
            "tier_b_fallback_rows": tier_b_rows,
            "routed_labelable_rows": tier_a_rows + tier_b_rows,
            "morphology_missing_rows": int(_numeric(view, "candle_morphology_missing").ge(0.5).sum()),
            "morphology_warmup_not_ready_rows": int(_numeric(view, "candle_morphology_warmup_ready").lt(0.5).sum()),
        }
        subtype[split] = (
            view.loc[view["tier_label"].astype(str).eq(mt5.TIER_B), "partial_context_subtype"]
            .astype(str)
            .value_counts()
            .to_dict()
        )
    return {
        "by_split": by_split,
        "tier_b_fallback_by_split_subtype": subtype,
        "no_tier_by_split": {str(key): int(value) for key, value in no_tier_by_split.items()},
    }


def build_micro_candidate_grid(
    best_candidate_id: str,
    broad_specs: Sequence[CandleMorphologyCandidateSpec],
    thresholds: Mapping[str, float],
) -> list[CandleMorphologyCandidateSpec]:
    base = next(spec for spec in broad_specs if spec.candidate_id == best_candidate_id)
    override_sets = [
        ("m01_relaxed_return", {"return_abs_q67": float(thresholds["return_abs_q60"])}),
        ("m02_firmer_score", {"morph_score_abs_q50": float(thresholds["morph_score_abs_q75"])}),
        ("m03_relaxed_score", {"morph_score_abs_q75": float(thresholds["morph_score_abs_q50"])}),
        ("m04_firmer_adx", {"adx_q50": float(thresholds["adx_q50"]) * 1.10}),
    ]
    return [
        replace(
            base,
            candidate_id=f"{micro_id}_{base.candidate_id}",
            label=f"bounded micro-search {micro_id} around {base.label}",
            threshold_family="micro_search_bounded_v1",
            threshold_overrides=overrides,
            notes="created only after broad-sweep micro-search gate passes",
        )
        for micro_id, overrides in override_sets
    ]
