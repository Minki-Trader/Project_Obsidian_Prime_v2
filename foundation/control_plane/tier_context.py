from __future__ import annotations

import re
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


TIER_B_PARTIAL_CONTEXT_SUBTYPES = (
    "B_full_context_outside_tier_a_scope",
    "B_macro_missing",
    "B_constituent_missing",
    "B_basket_missing",
    "B_core_only",
    "B_mixed_partial_context",
)

TIER_B_CONTEXT_GROUPS = {
    "macro": ("vix_change_1", "vix_zscore_20", "us10yr_change_1", "us10yr_zscore_20", "usdx_change_1", "usdx_zscore_20"),
    "constituent": ("nvda_xnas_log_return_1", "aapl_xnas_log_return_1", "msft_xnas_log_return_1", "amzn_xnas_log_return_1"),
    "basket": (
        "mega8_equal_return_1",
        "mega8_pos_breadth_1",
        "mega8_dispersion_5",
        "us100_minus_mega8_equal_return_1",
        "top3_weighted_return_1",
        "us100_minus_top3_weighted_return_1",
    ),
}


def finite_feature_mask(frame: pd.DataFrame, feature_order: Sequence[str]) -> pd.Series:
    missing = [name for name in feature_order if name not in frame.columns]
    if missing:
        raise RuntimeError(f"Frame is missing required feature columns: {missing}")
    matrix = frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
    return pd.Series(np.isfinite(matrix).all(axis=1), index=frame.index)


def classify_tier_b_partial_context(
    frame: pd.DataFrame,
    *,
    context_groups: Mapping[str, Sequence[str]] = TIER_B_CONTEXT_GROUPS,
) -> pd.DataFrame:
    result = frame.copy()
    group_ready = {
        group_name: finite_feature_mask(result, feature_names)
        for group_name, feature_names in context_groups.items()
    }

    subtypes: list[str] = []
    missing_masks: list[str] = []
    available_masks: list[str] = []
    group_names = list(context_groups)
    for row_index in result.index:
        missing_groups = [name for name in group_names if not bool(group_ready[name].loc[row_index])]
        available_groups = [name for name in group_names if name not in missing_groups]
        missing_set = set(missing_groups)
        if not missing_groups:
            subtype = "B_full_context_outside_tier_a_scope"
        elif missing_set == {"macro"}:
            subtype = "B_macro_missing"
        elif missing_set == {"constituent"}:
            subtype = "B_constituent_missing"
        elif missing_set == {"basket"}:
            subtype = "B_basket_missing"
        elif missing_set == set(group_names):
            subtype = "B_core_only"
        else:
            subtype = "B_mixed_partial_context"
        subtypes.append(subtype)
        missing_masks.append("|".join(missing_groups) if missing_groups else "none")
        available_masks.append("|".join(available_groups) if available_groups else "core_only")

    result["partial_context_subtype"] = subtypes
    result["missing_feature_group_mask"] = missing_masks
    result["available_feature_group_mask"] = available_masks
    return result


def parse_tier_b_fallback_allowed_subtypes(raw_value: str | None) -> tuple[str, ...] | None:
    if not raw_value:
        return None
    values = tuple(part.strip() for part in re.split(r"[,;]", raw_value) if part.strip())
    return normalize_tier_b_fallback_allowed_subtypes(values)


def normalize_tier_b_fallback_allowed_subtypes(
    allowed_subtypes: Sequence[str] | None,
) -> tuple[str, ...] | None:
    if not allowed_subtypes:
        return None
    values = tuple(str(value).strip() for value in allowed_subtypes if str(value).strip())
    unknown = sorted(set(values).difference(TIER_B_PARTIAL_CONTEXT_SUBTYPES))
    if unknown:
        raise RuntimeError(f"Unknown Tier B fallback subtypes: {unknown}")
    return values


def apply_tier_b_fallback_subtype_filter(
    frame: pd.DataFrame,
    allowed_subtypes: Sequence[str] | None,
    *,
    no_tier_route_role: str = "no_tier",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    normalized = normalize_tier_b_fallback_allowed_subtypes(allowed_subtypes)
    if not normalized:
        return frame.copy().reset_index(drop=True), frame.iloc[0:0].copy().reset_index(drop=True)
    if "partial_context_subtype" not in frame.columns:
        raise RuntimeError("Tier B fallback subtype filter requires partial_context_subtype")
    mask = frame["partial_context_subtype"].astype(str).isin(normalized)
    filtered = frame.loc[mask].copy().reset_index(drop=True)
    filtered_out = frame.loc[~mask].copy().reset_index(drop=True)
    if not filtered_out.empty:
        filtered_out["route_role"] = no_tier_route_role
        filtered_out["context_reject_reason"] = "tier_b_fallback_subtype_filtered_out"
    return filtered, filtered_out


def subtype_counts(frame: pd.DataFrame) -> dict[str, int]:
    if frame.empty or "partial_context_subtype" not in frame.columns:
        return {}
    counts = frame["partial_context_subtype"].astype(str).value_counts().sort_index()
    return {str(index): int(value) for index, value in counts.items()}
