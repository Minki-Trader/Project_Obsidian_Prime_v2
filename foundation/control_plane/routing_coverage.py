from __future__ import annotations

from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane.tier_context import normalize_tier_b_fallback_allowed_subtypes


SESSION_SLICE_DEFINITIONS: dict[str, tuple[float, float, str]] = {
    "early": (0.0, 110.0, "cash_session_early_0_110_minutes"),
    "mid": (110.0, 220.0, "cash_session_mid_110_220_minutes"),
    "mid_first": (110.0, 165.0, "cash_session_mid_first_110_165_minutes"),
    "mid_second": (165.0, 220.0, "cash_session_mid_second_165_220_minutes"),
    "mid_second_first": (165.0, 195.0, "cash_session_mid_second_first_165_195_minutes"),
    "mid_second_second": (195.0, 220.0, "cash_session_mid_second_second_195_220_minutes"),
    "mid_second_second_first": (195.0, 210.0, "cash_session_mid_second_second_first_195_210_minutes"),
    "mid_second_second_second": (210.0, 220.0, "cash_session_mid_second_second_second_210_220_minutes"),
    "mid_second_overlap_190_210": (190.0, 210.0, "cash_session_mid_second_overlap_190_210_minutes"),
    "mid_second_overlap_195_215": (195.0, 215.0, "cash_session_mid_second_overlap_195_215_minutes"),
    "mid_second_overlap_200_220": (200.0, 220.0, "cash_session_mid_second_overlap_200_220_minutes"),
    "mid_late_overlap_205_225": (205.0, 225.0, "cash_session_mid_late_overlap_205_225_minutes"),
    "late": (220.0, 330.0, "cash_session_late_220_330_minutes"),
}


def session_slice_payload(session_slice_id: str | None) -> dict[str, Any] | None:
    if not session_slice_id:
        return None
    start_minute, end_minute, policy_id = SESSION_SLICE_DEFINITIONS[session_slice_id]
    return {
        "slice_id": session_slice_id,
        "policy_id": policy_id,
        "minute_column": "minutes_from_cash_open",
        "start_exclusive": start_minute,
        "end_inclusive": end_minute,
        "timezone_basis": "precomputed_session_feature",
    }


def apply_session_slice(frame: pd.DataFrame, session_slice: Mapping[str, Any] | None) -> pd.DataFrame:
    if not session_slice:
        return frame.copy().reset_index(drop=True)
    minute_column = str(session_slice["minute_column"])
    if minute_column not in frame.columns:
        raise RuntimeError(f"Session slice requires missing column: {minute_column}")
    minutes = pd.to_numeric(frame[minute_column], errors="coerce")
    mask = minutes.gt(float(session_slice["start_exclusive"])) & minutes.le(float(session_slice["end_inclusive"]))
    return frame.loc[mask].copy().reset_index(drop=True)


def _split_counts(frame: pd.DataFrame) -> dict[str, int]:
    split_values = frame["split"].astype(str) if "split" in frame.columns else pd.Series([], dtype="object")
    return {split: int(split_values.eq(split).sum()) for split in ("train", "validation", "oos")}


def _subtype_counts(frame: pd.DataFrame) -> dict[str, int]:
    if frame.empty or "partial_context_subtype" not in frame.columns:
        return {}
    counts = frame["partial_context_subtype"].astype(str).value_counts().sort_index()
    return {str(index): int(value) for index, value in counts.items()}


def _subtype_counts_by_split(frame: pd.DataFrame) -> dict[str, dict[str, int]]:
    payload: dict[str, dict[str, int]] = {}
    for split in ("train", "validation", "oos"):
        split_frame = frame.loc[frame["split"].astype(str).eq(split)] if "split" in frame.columns else frame.iloc[0:0]
        payload[split] = _subtype_counts(split_frame)
    return payload


def build_eval_route_coverage_summary(
    *,
    base_summary: Mapping[str, Any],
    tier_a_eval_frame: pd.DataFrame,
    tier_b_eval_frame: pd.DataFrame,
    no_tier_eval_frame: pd.DataFrame,
    session_slice: Mapping[str, Any] | None,
    tier_b_filtered_out_frame: pd.DataFrame | None = None,
    tier_b_allowed_subtypes: Sequence[str] | None = None,
) -> dict[str, Any]:
    filtered_out = (
        tier_b_filtered_out_frame.reset_index(drop=True)
        if tier_b_filtered_out_frame is not None
        else tier_b_eval_frame.iloc[0:0].copy().reset_index(drop=True)
    )
    allowed_subtypes = normalize_tier_b_fallback_allowed_subtypes(tier_b_allowed_subtypes)
    by_split: dict[str, dict[str, int]] = {}
    for split in ("train", "validation", "oos"):
        a_count = int(tier_a_eval_frame["split"].astype(str).eq(split).sum())
        b_count = int(tier_b_eval_frame["split"].astype(str).eq(split).sum())
        no_tier_count = int(no_tier_eval_frame["split"].astype(str).eq(split).sum())
        filtered_out_count = int(filtered_out["split"].astype(str).eq(split).sum()) if "split" in filtered_out.columns else 0
        by_split[split] = {
            "tier_a_primary_rows": a_count,
            "tier_b_fallback_rows": b_count,
            "tier_b_fallback_filtered_out_rows": filtered_out_count,
            "no_tier_labelable_rows": no_tier_count,
            "routed_labelable_rows": a_count + b_count,
        }
    return {
        "policy_id": base_summary.get("policy_id"),
        "dataset_id": base_summary.get("dataset_id"),
        "feature_set_id": base_summary.get("feature_set_id"),
        "feature_count": base_summary.get("feature_count"),
        "feature_order_hash": base_summary.get("feature_order_hash"),
        "label_threshold_log_return": base_summary.get("label_threshold_log_return"),
        "source_raw_rows": base_summary.get("source_raw_rows"),
        "source_valid_rows": base_summary.get("source_valid_rows"),
        "labelable_rows": int(len(tier_a_eval_frame) + len(tier_b_eval_frame) + len(no_tier_eval_frame)),
        "tier_a_primary_rows": int(len(tier_a_eval_frame)),
        "tier_b_training_rows": base_summary.get("tier_b_training_rows"),
        "tier_b_fallback_rows": int(len(tier_b_eval_frame)),
        "tier_b_fallback_allowed_subtypes": list(allowed_subtypes) if allowed_subtypes else None,
        "tier_b_fallback_filter_policy": "allowed_subtypes" if allowed_subtypes else "none",
        "tier_b_fallback_filtered_out_rows": int(len(filtered_out)),
        "tier_b_fallback_filtered_out_by_subtype": _subtype_counts(filtered_out),
        "tier_b_fallback_filtered_out_by_split_subtype": _subtype_counts_by_split(filtered_out),
        "no_tier_labelable_rows": int(len(no_tier_eval_frame)),
        "by_split": by_split,
        "tier_b_fallback_by_subtype": _subtype_counts(tier_b_eval_frame),
        "tier_b_fallback_by_split_subtype": _subtype_counts_by_split(tier_b_eval_frame),
        "no_tier_by_split": _split_counts(no_tier_eval_frame),
        "session_slice": dict(session_slice) if session_slice else None,
        "note": (
            "Session-sliced evaluation rows derived from the base Tier A/Tier B route coverage."
            if session_slice
            else base_summary.get("note")
        ),
    }
