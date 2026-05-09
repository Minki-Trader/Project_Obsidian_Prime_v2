from __future__ import annotations

import json
import math
from dataclasses import dataclass, replace
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.mt5 import runtime_support as mt5


SIGNAL_FEATURE_ORDER = ("stage40_volatility_squeeze_signal",)
REQUIRED_BASE_FEATURES = (
    "return_zscore_20",
    "bollinger_width_20",
    "bb_position_20",
    "bb_squeeze",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "ema20_ema50_diff",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
)


@dataclass(frozen=True)
class VolatilitySqueezeCandidateSpec:
    candidate_id: str
    label: str
    mechanism_family: str
    rule_code: str
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


def _quantile(series: pd.Series, q: float, fallback: float) -> float:
    values = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty:
        return float(fallback)
    value = float(values.quantile(float(q)))
    return value if math.isfinite(value) else float(fallback)


def _abs_quantile(series: pd.Series, q: float, fallback: float) -> float:
    return _quantile(pd.to_numeric(series, errors="coerce").abs(), q, fallback)


def build_thresholds(common: pd.DataFrame) -> dict[str, float]:
    train = common.loc[common["split"].astype(str).eq("train") & _finite_mask(common, REQUIRED_BASE_FEATURES)].copy()
    return {
        "return_abs_q60": _abs_quantile(train["return_zscore_20"], 0.60, 0.35),
        "return_abs_q67": _abs_quantile(train["return_zscore_20"], 0.67, 0.50),
        "return_abs_q75": _abs_quantile(train["return_zscore_20"], 0.75, 0.75),
        "vol_expand_q60": _quantile(train["historical_vol_5_over_20"], 0.60, 1.0),
        "vol_expand_q67": _quantile(train["historical_vol_5_over_20"], 0.67, 1.10),
        "vol_expand_q75": _quantile(train["historical_vol_5_over_20"], 0.75, 1.25),
        "width_low_q33": _quantile(train["bollinger_width_20"], 0.33, 0.01),
        "width_low_q25": _quantile(train["bollinger_width_20"], 0.25, 0.008),
        "adx_q33": _quantile(train["adx_14"], 0.33, 15.0),
        "adx_q50": _quantile(train["adx_14"], 0.50, 20.0),
        "adx_q67": _quantile(train["adx_14"], 0.67, 25.0),
        "di_abs_q60": _abs_quantile(train["di_spread_14"], 0.60, 5.0),
        "di_abs_q67": _abs_quantile(train["di_spread_14"], 0.67, 7.5),
        "bb_upper": 0.75,
        "bb_lower": 0.25,
        "bb_pullback_upper": 0.65,
        "bb_pullback_lower": 0.35,
        "open_minutes_max": 30.0,
    }


def candidate_thresholds(base: Mapping[str, float], spec: VolatilitySqueezeCandidateSpec) -> dict[str, float]:
    out = {str(key): float(value) for key, value in base.items()}
    for key, value in (spec.threshold_overrides or {}).items():
        out[str(key)] = float(value)
    return out


def build_broad_candidate_grid(threshold_family: str = "broad_train_quantile_v1") -> list[VolatilitySqueezeCandidateSpec]:
    items = [
        ("c01_reference_return_z_momentum", "reference return-z momentum", "reference/carry comparison", "reference_return_z_momentum"),
        ("c02_squeeze_breakout_bb_position", "squeeze breakout by Bollinger position", "squeeze breakout", "squeeze_breakout_bb_position"),
        ("c03_squeeze_release_return_expansion", "squeeze release with return and vol expansion", "squeeze release", "squeeze_release_return_expansion"),
        ("c04_low_width_expansion_di_confirmation", "low-width expansion with DI confirmation", "width expansion", "low_width_expansion_di"),
        ("c05_trend_expansion_ema_alignment", "trend expansion with EMA alignment", "trend expansion", "trend_expansion_ema"),
        ("c06_chop_squeeze_reversal_extreme", "chop squeeze reversal at band extremes", "squeeze reversal", "chop_squeeze_reversal"),
        ("c07_high_vol_breakout_return_z", "high-volatility return-z breakout", "volatility breakout", "high_vol_breakout_return"),
        ("c08_pullback_in_trend_continuation", "pullback in trend continuation", "trend pullback", "pullback_trend_continuation"),
        ("c09_first_30m_squeeze_breakout", "first-30m squeeze breakout", "session conditioned squeeze", "first_30m_squeeze_breakout"),
        ("c10_di_spread_squeeze_release", "DI-spread squeeze release", "DI pressure release", "di_spread_squeeze_release"),
        ("c11_expansion_without_squeeze_reference", "expansion without squeeze reference", "expansion reference", "expansion_without_squeeze_reference"),
        ("c12_squeeze_plus_adx_di_alignment", "squeeze plus ADX and DI alignment", "multi-confirmed squeeze", "squeeze_adx_di_alignment"),
    ]
    return [
        VolatilitySqueezeCandidateSpec(
            candidate_id=candidate_id,
            label=label,
            mechanism_family=family,
            rule_code=rule_code,
            threshold_family=threshold_family,
        )
        for candidate_id, label, family, rule_code in items
    ]


def _rule_masks(frame: pd.DataFrame, thresholds: Mapping[str, float], rule_code: str) -> tuple[pd.Series, pd.Series, Sequence[str]]:
    rz = _numeric(frame, "return_zscore_20")
    width = _numeric(frame, "bollinger_width_20")
    bb = _numeric(frame, "bb_position_20")
    squeeze = _numeric(frame, "bb_squeeze").ge(0.5)
    vol = _numeric(frame, "historical_vol_5_over_20")
    adx = _numeric(frame, "adx_14")
    di = _numeric(frame, "di_spread_14")
    ema = _numeric(frame, "ema20_ema50_diff")
    minutes = _numeric(frame, "minutes_from_cash_open")
    first30 = _numeric(frame, "is_first_30m_after_open").ge(0.5) | minutes.between(0, float(thresholds["open_minutes_max"]), inclusive="both")

    req = REQUIRED_BASE_FEATURES
    ret60 = float(thresholds["return_abs_q60"])
    ret67 = float(thresholds["return_abs_q67"])
    ret75 = float(thresholds["return_abs_q75"])
    vol60 = float(thresholds["vol_expand_q60"])
    vol67 = float(thresholds["vol_expand_q67"])
    vol75 = float(thresholds["vol_expand_q75"])
    width33 = float(thresholds["width_low_q33"])
    width25 = float(thresholds["width_low_q25"])
    adx33 = float(thresholds["adx_q33"])
    adx50 = float(thresholds["adx_q50"])
    adx67 = float(thresholds["adx_q67"])
    di60 = float(thresholds["di_abs_q60"])
    di67 = float(thresholds["di_abs_q67"])
    upper = float(thresholds["bb_upper"])
    lower = float(thresholds["bb_lower"])
    pull_upper = float(thresholds["bb_pullback_upper"])
    pull_lower = float(thresholds["bb_pullback_lower"])

    if rule_code == "reference_return_z_momentum":
        long = rz.ge(ret67) & adx.ge(adx50)
        short = rz.le(-ret67) & adx.ge(adx50)
    elif rule_code == "squeeze_breakout_bb_position":
        long = squeeze & bb.ge(upper) & rz.ge(0)
        short = squeeze & bb.le(lower) & rz.le(0)
    elif rule_code == "squeeze_release_return_expansion":
        long = squeeze & vol.ge(vol67) & rz.ge(ret60)
        short = squeeze & vol.ge(vol67) & rz.le(-ret60)
    elif rule_code == "low_width_expansion_di":
        long = width.le(width33) & vol.ge(vol67) & di.ge(di60)
        short = width.le(width33) & vol.ge(vol67) & di.le(-di60)
    elif rule_code == "trend_expansion_ema":
        long = vol.ge(vol67) & adx.ge(adx67) & ema.gt(0) & rz.ge(0)
        short = vol.ge(vol67) & adx.ge(adx67) & ema.lt(0) & rz.le(0)
    elif rule_code == "chop_squeeze_reversal":
        long = squeeze & adx.le(adx33) & bb.le(lower) & rz.le(-ret60)
        short = squeeze & adx.le(adx33) & bb.ge(upper) & rz.ge(ret60)
    elif rule_code == "high_vol_breakout_return":
        long = vol.ge(vol75) & rz.ge(ret75)
        short = vol.ge(vol75) & rz.le(-ret75)
    elif rule_code == "pullback_trend_continuation":
        long = adx.ge(adx67) & ema.gt(0) & bb.le(pull_lower) & rz.le(0)
        short = adx.ge(adx67) & ema.lt(0) & bb.ge(pull_upper) & rz.ge(0)
    elif rule_code == "first_30m_squeeze_breakout":
        long = first30 & squeeze & bb.ge(upper) & rz.ge(ret60)
        short = first30 & squeeze & bb.le(lower) & rz.le(-ret60)
    elif rule_code == "di_spread_squeeze_release":
        long = squeeze & vol.ge(vol60) & di.ge(di67)
        short = squeeze & vol.ge(vol60) & di.le(-di67)
    elif rule_code == "expansion_without_squeeze_reference":
        long = ~squeeze & vol.ge(vol67) & rz.ge(ret67)
        short = ~squeeze & vol.ge(vol67) & rz.le(-ret67)
    elif rule_code == "squeeze_adx_di_alignment":
        long = squeeze & adx.ge(adx50) & di.ge(di60) & rz.ge(0)
        short = squeeze & adx.ge(adx50) & di.le(-di60) & rz.le(0)
    else:
        raise ValueError(f"unknown volatility squeeze rule: {rule_code}")
    return long.fillna(False), short.fillna(False), req


def apply_candidate_to_table(
    common: pd.DataFrame,
    spec: VolatilitySqueezeCandidateSpec,
    base_thresholds: Mapping[str, float],
) -> pd.DataFrame:
    thresholds = candidate_thresholds(base_thresholds, spec)
    long_mask, short_mask, required = _rule_masks(common, thresholds, spec.rule_code)
    missing = ~_finite_mask(common, required)
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
        *REQUIRED_BASE_FEATURES,
    ]
    out = common[[column for column in out_columns if column in common.columns]].copy()
    out["candidate_id"] = spec.candidate_id
    out["candidate_label"] = spec.label
    out["mechanism_family"] = spec.mechanism_family
    out["rule_code"] = spec.rule_code
    out["threshold_family"] = spec.threshold_family
    out["thresholds_json"] = json.dumps(thresholds, sort_keys=True, separators=(",", ":"))
    out["stage40_surface_missing"] = missing.to_numpy()
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
    reference = candidate_frames.get("c01_reference_return_z_momentum")
    for split in ("validation", "oos"):
        if reference is None:
            reference_counts[split] = 0
        else:
            reference_counts[split] = int(reference.loc[reference["split"].astype(str).eq(split), SIGNAL_FEATURE_ORDER[0]].ne(0).sum())
    rows: list[dict[str, Any]] = []
    for candidate_id, frame in candidate_frames.items():
        for split in ("validation", "oos"):
            view = frame.loc[frame["split"].astype(str).eq(split)]
            if view.empty:
                rows.append(
                    {
                        "candidate_id": candidate_id,
                        "split": split_alias(split),
                        "candidate_rejection_reason": "missing_split_rows",
                    }
                )
                continue
            signal = view[SIGNAL_FEATURE_ORDER[0]].astype(int)
            signal_count = int(signal.ne(0).sum())
            tier_a = view.loc[view["tier_label"].astype(str).eq(mt5.TIER_A)]
            tier_b = view.loc[view["tier_label"].astype(str).eq(mt5.TIER_B)]
            tier_b_signal = int(tier_b[SIGNAL_FEATURE_ORDER[0]].ne(0).sum())
            ref_count = max(reference_counts.get(split, 0), 1)
            rejection = "mt5_pending"
            if signal_count < 20:
                rejection = "thin_trade_stream_python_signal_count_lt_20"
            elif candidate_id != "c01_reference_return_z_momentum" and signal_count / ref_count < 0.10:
                rejection = "thin_trade_stream_vs_reference_python"
            elif signal_count and tier_b_signal / signal_count > 0.60:
                rejection = "tier_b_fallback_signal_share_gt_60pct_python"
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "candidate_label": str(view["candidate_label"].iloc[0]),
                    "split": split_alias(split),
                    "mechanism_family": str(view["mechanism_family"].iloc[0]),
                    "rule_code": str(view["rule_code"].iloc[0]),
                    "threshold_family": str(view["threshold_family"].iloc[0]),
                    "thresholds": str(view["thresholds_json"].iloc[0]),
                    "tier_a_signal_count": int(tier_a[SIGNAL_FEATURE_ORDER[0]].ne(0).sum()),
                    "tier_b_fallback_signal_count": tier_b_signal,
                    "actual_routed_total_count": signal_count,
                    "long_count": int(signal.gt(0).sum()),
                    "short_count": int(signal.lt(0).sum()),
                    "flat_count": int(signal.eq(0).sum()),
                    "no_trade_rate": float(1.0 - signal_count / len(view)) if len(view) else 1.0,
                    "thinning_ratio_vs_reference": float(signal_count / ref_count),
                    "tier_b_signal_share_python": float(tier_b_signal / signal_count) if signal_count else None,
                    "missing_surface_rows": int(view["stage40_surface_missing"].sum()),
                    "candidate_rejection_reason": rejection,
                }
            )
    return rows


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
    broad_specs: Sequence[VolatilitySqueezeCandidateSpec],
    thresholds: Mapping[str, float],
) -> list[VolatilitySqueezeCandidateSpec]:
    base = next(spec for spec in broad_specs if spec.candidate_id == best_candidate_id)
    override_sets = [
        ("m01_relaxed_return", {"return_abs_q67": float(thresholds["return_abs_q60"])}),
        ("m02_firmer_return", {"return_abs_q67": float(thresholds["return_abs_q75"])}),
        ("m03_relaxed_vol", {"vol_expand_q67": float(thresholds["vol_expand_q60"])}),
        ("m04_firmer_vol", {"vol_expand_q67": float(thresholds["vol_expand_q75"])}),
        ("m05_relaxed_trend", {"adx_q67": float(thresholds["adx_q50"])}),
        ("m06_firmer_width", {"width_low_q33": float(thresholds["width_low_q25"])}),
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
