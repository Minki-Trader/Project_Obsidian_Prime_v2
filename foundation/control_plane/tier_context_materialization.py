from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import numpy as np
import pandas as pd

from foundation.control_plane.tier_context import (
    classify_tier_b_partial_context,
    finite_feature_mask,
    subtype_counts as _subtype_counts,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.pipelines.materialize_fpmarkets_v2_dataset import build_feature_frame
from foundation.pipelines.materialize_training_label_split_dataset import (
    TrainingLabelSplitSpec,
    assign_label_classes,
    assign_split,
    build_label_candidates,
    load_us100_close_series,
)


TIER_COLUMN = "tier_label"
TIER_B = "Tier B"
ROUTE_ROLE_A_PRIMARY = "tier_a_primary"
ROUTE_ROLE_B_FALLBACK = "tier_b_fallback"
ROUTE_ROLE_NO_TIER = "no_tier"
TIER_B_PARTIAL_CONTEXT_DATASET_ID = "stage10_tier_b_partial_context_core42_v1"
TIER_B_PARTIAL_CONTEXT_FEATURE_SET_ID = "feature_set_stage10_tier_b_core42_us100_session_v1"
TIER_B_PARTIAL_CONTEXT_POLICY_ID = "tier_b_partial_context_core42_fallback_v1"
TIER_B_CORE_FEATURE_ORDER = (
    "log_return_1",
    "log_return_3",
    "hl_range",
    "close_open_ratio",
    "gap_percent",
    "close_prev_close_ratio",
    "return_zscore_20",
    "hl_zscore_50",
    "overnight_return",
    "return_1_over_atr_14",
    "close_ema20_ratio",
    "close_ema50_ratio",
    "ema9_ema20_diff",
    "ema20_ema50_diff",
    "ema50_ema200_diff",
    "ema20_ema50_spread_zscore_50",
    "sma50_sma200_ratio",
    "rsi_14",
    "rsi_50",
    "rsi_14_slope_3",
    "rsi_14_minus_50",
    "stoch_kd_diff",
    "stochrsi_kd_diff",
    "ppo_hist_12_26_9",
    "roc_12",
    "trix_15",
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "bb_position_20",
    "bb_squeeze",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "supertrend_10_3",
    "vortex_indicator",
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
)


def _timestamp_key(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, utc=True).astype("int64")


def _split_counts(frame: pd.DataFrame) -> dict[str, int]:
    if frame.empty or "split" not in frame.columns:
        return {}
    counts = frame["split"].astype(str).value_counts().sort_index()
    return {str(index): int(value) for index, value in counts.items()}


def _subtype_counts_by_split(frame: pd.DataFrame) -> dict[str, dict[str, int]]:
    if frame.empty or "split" not in frame.columns or "partial_context_subtype" not in frame.columns:
        return {}
    payload: dict[str, dict[str, int]] = {}
    for split, split_frame in frame.groupby(frame["split"].astype(str), dropna=False):
        payload[str(split)] = _subtype_counts(split_frame)
    return payload


def build_tier_b_partial_context_frames(
    *,
    raw_root: Path,
    tier_a_frame: pd.DataFrame,
    tier_a_feature_order: Sequence[str],
    tier_b_feature_order: Sequence[str],
    label_threshold: float,
    label_spec: TrainingLabelSplitSpec | None = None,
) -> dict[str, Any]:
    spec = label_spec or TrainingLabelSplitSpec()
    feature_frame, source_counts = build_feature_frame(raw_root)
    feature_frame = feature_frame.copy()
    feature_frame["timestamp"] = pd.to_datetime(feature_frame["timestamp"], utc=True)
    if "symbol" not in feature_frame.columns:
        feature_frame["symbol"] = "US100"

    cash_open = feature_frame["is_us_cash_open"].fillna(0).astype(bool)
    practical = feature_frame["timestamp"] >= spec.train_start_utc
    feature_frame = feature_frame.loc[practical & cash_open].sort_values("timestamp").reset_index(drop=True)

    raw_close_frame = load_us100_close_series(raw_root)
    labelable = build_label_candidates(feature_frame, raw_close_frame, spec)
    labelable = assign_label_classes(labelable, label_threshold)
    labelable["split"] = assign_split(labelable, spec)
    labelable["label_id"] = spec.label_id
    labelable["split_id"] = spec.split_id
    labelable["horizon_bars"] = spec.horizon_bars
    labelable["horizon_minutes"] = spec.horizon_minutes
    labelable["symbol"] = "US100"
    labelable = labelable.sort_values("timestamp").reset_index(drop=True)

    tier_a_keys = set(_timestamp_key(tier_a_frame["timestamp"]).tolist())
    labelable_keys = _timestamp_key(labelable["timestamp"])
    tier_a_available = labelable_keys.isin(tier_a_keys)
    tier_b_ready = finite_feature_mask(labelable, tier_b_feature_order)
    tier_a_full_feature_ready = finite_feature_mask(labelable, tier_a_feature_order)

    labelable["tier_a_primary_available"] = tier_a_available.to_numpy()
    labelable["tier_a_full_feature_ready"] = tier_a_full_feature_ready.to_numpy()
    labelable["tier_b_core_ready"] = tier_b_ready.to_numpy()
    labelable["route_role"] = np.select(
        [tier_a_available.to_numpy(), tier_b_ready.to_numpy()],
        [ROUTE_ROLE_A_PRIMARY, ROUTE_ROLE_B_FALLBACK],
        default=ROUTE_ROLE_NO_TIER,
    )

    labeled_with_context = classify_tier_b_partial_context(labelable)
    b_training = labeled_with_context.loc[tier_b_ready].copy().reset_index(drop=True)
    b_fallback = labeled_with_context.loc[~tier_a_available & tier_b_ready].copy().reset_index(drop=True)
    no_tier = labeled_with_context.loc[~tier_a_available & ~tier_b_ready].copy().reset_index(drop=True)

    b_training[TIER_COLUMN] = TIER_B
    b_fallback[TIER_COLUMN] = TIER_B
    no_tier["context_reject_reason"] = "core42_nonfinite_or_missing"
    no_tier["partial_context_subtype"] = "no_tier_core42_missing"
    no_tier["missing_feature_group_mask"] = "core42"
    no_tier["available_feature_group_mask"] = "insufficient_for_tier_b"

    by_split: dict[str, dict[str, int]] = {}
    for split in ("train", "validation", "oos"):
        by_split[split] = {
            "tier_a_primary_rows": int(tier_a_frame["split"].astype(str).eq(split).sum()),
            "tier_b_fallback_rows": int(b_fallback["split"].astype(str).eq(split).sum()),
            "no_tier_labelable_rows": int(no_tier["split"].astype(str).eq(split).sum()),
        }
        by_split[split]["routed_labelable_rows"] = (
            by_split[split]["tier_a_primary_rows"] + by_split[split]["tier_b_fallback_rows"]
        )

    summary = {
        "policy_id": TIER_B_PARTIAL_CONTEXT_POLICY_ID,
        "dataset_id": TIER_B_PARTIAL_CONTEXT_DATASET_ID,
        "feature_set_id": TIER_B_PARTIAL_CONTEXT_FEATURE_SET_ID,
        "feature_count": int(len(tier_b_feature_order)),
        "feature_order_hash": ordered_hash(tier_b_feature_order),
        "label_threshold_log_return": float(label_threshold),
        "source_raw_rows": int(source_counts.get("raw_rows", 0)),
        "source_valid_rows": int(source_counts.get("valid_rows", 0)),
        "labelable_rows": int(len(labelable)),
        "tier_a_primary_rows": int(len(tier_a_frame)),
        "tier_b_training_rows": int(len(b_training)),
        "tier_b_fallback_rows": int(len(b_fallback)),
        "no_tier_labelable_rows": int(len(no_tier)),
        "by_split": by_split,
        "tier_b_fallback_by_subtype": _subtype_counts(b_fallback),
        "tier_b_fallback_by_split_subtype": _subtype_counts_by_split(b_fallback),
        "no_tier_by_split": _split_counts(no_tier),
        "note": (
            "Tier B fallback is built from partial-context rows outside the strict Tier A clean sample "
            "that still have finite US100/session core42 features."
        ),
    }
    return {
        "route_frame": labeled_with_context,
        "tier_b_training_frame": b_training,
        "tier_b_fallback_frame": b_fallback,
        "no_tier_frame": no_tier,
        "summary": summary,
    }
