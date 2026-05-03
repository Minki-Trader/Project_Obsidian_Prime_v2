from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.models.catboost_ordered import CatBoostVariantSpec, default_stage18_catboost_variants
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage18 import catboost_mt5_characteristic_probe as base


STAGE_ID = base.STAGE_ID
STAGE_NUMBER = base.STAGE_NUMBER
MODEL_FAMILY = base.MODEL_FAMILY
FEATURE_SET_ID = base.FEATURE_SET_ID
LABEL_ID = base.LABEL_ID
SPLIT_CONTRACT = base.SPLIT_CONTRACT
STAGE_INHERITANCE = base.STAGE_INHERITANCE
ROOT = base.ROOT
STAGE_ROOT = base.STAGE_ROOT
STAGE_LEDGER_PATH = base.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = base.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = base.RUN_REGISTRY_PATH
AGGREGATE_PACKET_ID = "stage18_catboost_followup_batch_mt5_kpi_v1"
AGGREGATE_PACKET_ROOT = ROOT / "docs/agent_control/packets" / AGGREGATE_PACKET_ID
DEFAULT_VARIANT_ID = "v02_ordered_depth4_strong_l2"
PLAIN_CONTROL_VARIANT_ID = "v05_plain_depth3_control"
MIN_MARGIN = base.MIN_MARGIN
DEFAULT_MAX_HOLD_BARS = base.MAX_HOLD_BARS
DISABLED_THRESHOLD = 1.1


@dataclass(frozen=True)
class FollowupTopic:
    run_id: str
    run_number: str
    packet_id: str
    exploration_label: str
    review_filename: str
    threshold_quantile: float
    builder: str
    expected_attempts: int
    expected_kpi_records: int
    topic_read: str
    question: str
    variant_id: str = DEFAULT_VARIANT_ID
    boundary: str = "catboost_stage18_followup_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
    judgment_completed: str = "inconclusive_catboost_followup_mt5_runtime_probe_completed"
    judgment_blocked: str = "blocked_catboost_followup_mt5_runtime_probe_after_attempt"

    @property
    def run_root(self) -> Path:
        return STAGE_ROOT / "02_runs" / self.run_id

    @property
    def packet_root(self) -> Path:
        return ROOT / "docs/agent_control/packets" / self.packet_id

    @property
    def review_path(self) -> Path:
        return STAGE_ROOT / "03_reviews" / self.review_filename


@dataclass(frozen=True)
class SegmentAttempt:
    segment_id: str
    segment_label: str
    source_split: str
    runtime_split: str
    mode: str
    tier_a_matrix_key: str | None
    tier_b_matrix_key: str
    tier_a_rows: int
    tier_b_rows: int
    tier_a_threshold: float
    tier_b_threshold: float
    threshold_quantile: float
    max_hold_bars: int = DEFAULT_MAX_HOLD_BARS
    direction: str = "both"
    segment_filter: str = ""


FOLLOWUP_TOPICS: tuple[FollowupTopic, ...] = (
    FollowupTopic(
        run_id="run12D_catboost_regime_split_probe_v1",
        run_number="run12D",
        packet_id="stage18_run12D_catboost_regime_split_mt5_v1",
        exploration_label="stage18_Model__CatBoostRegimeSplit",
        review_filename="run12D_catboost_regime_split_packet.md",
        threshold_quantile=0.80,
        builder="regime_split",
        expected_attempts=4,
        expected_kpi_records=12,
        topic_read="volatility_regime_split",
        question="Does the selected CatBoost model behave differently in high-volatility and low-volatility slices?",
    ),
    FollowupTopic(
        run_id="run12E_catboost_session_timing_probe_v1",
        run_number="run12E",
        packet_id="stage18_run12E_catboost_session_timing_mt5_v1",
        exploration_label="stage18_Model__CatBoostSessionTiming",
        review_filename="run12E_catboost_session_timing_packet.md",
        threshold_quantile=0.80,
        builder="session_timing",
        expected_attempts=6,
        expected_kpi_records=18,
        topic_read="cash_session_timing_split",
        question="Does the model concentrate its runtime behavior in early, mid, or late cash-session minutes?",
    ),
    FollowupTopic(
        run_id="run12F_catboost_feature_driver_mask_probe_v1",
        run_number="run12F",
        packet_id="stage18_run12F_catboost_feature_driver_mask_mt5_v1",
        exploration_label="stage18_Model__CatBoostFeatureDriverMask",
        review_filename="run12F_catboost_feature_driver_mask_packet.md",
        threshold_quantile=0.80,
        builder="feature_mask",
        expected_attempts=6,
        expected_kpi_records=18,
        topic_read="feature_driver_masking",
        question="Which visible feature drivers keep or break the model characteristic when neutralized?",
    ),
    FollowupTopic(
        run_id="run12G_catboost_probability_calibration_probe_v1",
        run_number="run12G",
        packet_id="stage18_run12G_catboost_probability_calibration_mt5_v1",
        exploration_label="stage18_Model__CatBoostProbabilityCalibration",
        review_filename="run12G_catboost_probability_calibration_packet.md",
        threshold_quantile=0.80,
        builder="probability_calibration",
        expected_attempts=4,
        expected_kpi_records=12,
        topic_read="probability_confidence_band",
        question="Does higher non-flat confidence translate into different MT5 trade shape than mid-confidence signals?",
    ),
    FollowupTopic(
        run_id="run12H_catboost_margin_geometry_probe_v1",
        run_number="run12H",
        packet_id="stage18_run12H_catboost_margin_geometry_mt5_v1",
        exploration_label="stage18_Model__CatBoostMarginGeometry",
        review_filename="run12H_catboost_margin_geometry_packet.md",
        threshold_quantile=0.80,
        builder="margin_geometry",
        expected_attempts=4,
        expected_kpi_records=12,
        topic_read="probability_margin_geometry",
        question="Does the top-class probability margin explain the ordered CatBoost runtime behavior?",
    ),
    FollowupTopic(
        run_id="run12I_catboost_long_bias_source_probe_v1",
        run_number="run12I",
        packet_id="stage18_run12I_catboost_long_bias_source_mt5_v1",
        exploration_label="stage18_Model__CatBoostLongBiasSource",
        review_filename="run12I_catboost_long_bias_source_packet.md",
        threshold_quantile=0.80,
        builder="long_bias_source",
        expected_attempts=6,
        expected_kpi_records=18,
        topic_read="long_bias_source_split",
        question="Where does the long-side concentration come from: volatility, session timing, or residual rows?",
    ),
    FollowupTopic(
        run_id="run12J_catboost_tier_b_fallback_anatomy_probe_v1",
        run_number="run12J",
        packet_id="stage18_run12J_catboost_tier_b_fallback_anatomy_mt5_v1",
        exploration_label="stage18_Model__CatBoostTierBFallbackAnatomy",
        review_filename="run12J_catboost_tier_b_fallback_anatomy_packet.md",
        threshold_quantile=0.80,
        builder="tier_b_fallback_anatomy",
        expected_attempts=6,
        expected_kpi_records=6,
        topic_read="tier_b_fallback_subtype_anatomy",
        question="Which Tier B partial-context subtype carries the fallback behavior?",
    ),
    FollowupTopic(
        run_id="run12K_catboost_hold_stress_probe_v1",
        run_number="run12K",
        packet_id="stage18_run12K_catboost_hold_stress_mt5_v1",
        exploration_label="stage18_Model__CatBoostHoldStress",
        review_filename="run12K_catboost_hold_stress_packet.md",
        threshold_quantile=0.80,
        builder="hold_stress",
        expected_attempts=4,
        expected_kpi_records=12,
        topic_read="trade_shape_hold_time_stress",
        question="Is the CatBoost characteristic sensitive to shorter or longer maximum hold bars?",
    ),
    FollowupTopic(
        run_id="run12L_catboost_plain_variant_contrast_probe_v1",
        run_number="run12L",
        packet_id="stage18_run12L_catboost_plain_variant_contrast_mt5_v1",
        exploration_label="stage18_Model__CatBoostPlainControlContrast",
        review_filename="run12L_catboost_plain_variant_contrast_packet.md",
        threshold_quantile=0.80,
        builder="plain_variant_contrast",
        expected_attempts=2,
        expected_kpi_records=6,
        topic_read="ordered_vs_plain_boosting_contrast",
        question="Does the plain boosting control preserve or erase the ordered boosting runtime characteristic?",
        variant_id=PLAIN_CONTROL_VARIANT_ID,
    ),
    FollowupTopic(
        run_id="run12M_catboost_threshold_surface_probe_v1",
        run_number="run12M",
        packet_id="stage18_run12M_catboost_threshold_surface_mt5_v1",
        exploration_label="stage18_Model__CatBoostThresholdSurface",
        review_filename="run12M_catboost_threshold_surface_packet.md",
        threshold_quantile=0.80,
        builder="threshold_surface",
        expected_attempts=6,
        expected_kpi_records=18,
        topic_read="threshold_surface_q70_q85_q95",
        question="How does the same model behave across q70, q85, and q95 non-flat thresholds?",
    ),
)


def variant_map() -> dict[str, CatBoostVariantSpec]:
    return {spec.variant_id: spec for spec in default_stage18_catboost_variants()}


def selected_payload(spec: CatBoostVariantSpec) -> dict[str, Any]:
    return {
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "description": spec.description,
        "spec": spec.payload(),
    }


def split_frames(
    context: Mapping[str, Any],
    tier_a_prob: pd.DataFrame,
    tier_b_prob: pd.DataFrame,
    split: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    a_frame = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq(split)].copy().reset_index(drop=True)
    b_frame = context["tier_b_fallback_frame"].loc[context["tier_b_fallback_frame"]["split"].astype(str).eq(split)].copy().reset_index(drop=True)
    a_prob = tier_a_prob.loc[tier_a_prob["split"].astype(str).eq(split)].copy().reset_index(drop=True)
    b_prob = tier_b_prob.loc[tier_b_prob["split"].astype(str).eq(split)].copy().reset_index(drop=True)
    if len(a_frame) != len(a_prob):
        raise RuntimeError(f"Tier A frame/probability length mismatch for {split}: {len(a_frame)} != {len(a_prob)}")
    if len(b_frame) != len(b_prob):
        raise RuntimeError(f"Tier B frame/probability length mismatch for {split}: {len(b_frame)} != {len(b_prob)}")
    return a_frame, b_frame, a_prob, b_prob


def nonflat_score(prob: pd.DataFrame) -> pd.Series:
    return pd.concat([prob["p_short"].astype("float64"), prob["p_long"].astype("float64")], axis=1).max(axis=1)


def bool_series(value: Any, length: int) -> pd.Series:
    if isinstance(value, pd.Series):
        return value.fillna(False).astype(bool).reset_index(drop=True)
    array = np.asarray(value, dtype=bool)
    if array.shape[0] != length:
        raise RuntimeError(f"mask length mismatch: {array.shape[0]} != {length}")
    return pd.Series(array, dtype=bool)


def subtype_counts(frame: pd.DataFrame) -> dict[str, int]:
    if frame.empty or "partial_context_subtype" not in frame.columns:
        return {}
    counts = frame["partial_context_subtype"].astype(str).value_counts().sort_index()
    return {str(key): int(value) for key, value in counts.items()}


def threshold_for(prob: pd.DataFrame, quantile: float) -> float:
    if prob.empty:
        raise RuntimeError("Cannot build a split-local threshold from an empty probability frame.")
    return float(nonflat_score(prob).quantile(quantile))


def train_medians(context: Mapping[str, Any]) -> dict[str, float]:
    train = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq("train")]
    medians: dict[str, float] = {}
    for name in ("historical_vol_20", "hl_range", "minutes_from_cash_open"):
        medians[name] = float(train[name].astype("float64").median())
    return medians


def export_segment(
    *,
    topic: FollowupTopic,
    context: Mapping[str, Any],
    feature_matrices: dict[str, dict[str, Any]],
    segments: list[SegmentAttempt],
    segment_id: str,
    segment_label: str,
    source_split: str,
    runtime_split: str,
    mode: str,
    tier_a_frame: pd.DataFrame | None,
    tier_b_frame: pd.DataFrame,
    tier_a_threshold: float,
    tier_b_threshold: float,
    threshold_quantile: float,
    max_hold_bars: int = DEFAULT_MAX_HOLD_BARS,
    direction: str = "both",
    segment_filter: str = "",
) -> None:
    root = topic.run_root / "features" / segment_id
    tier_a_key: str | None = None
    if tier_a_frame is not None:
        tier_a_key = f"{segment_id}_tier_a_{runtime_split}"
        feature_matrices[tier_a_key] = mt5.export_mt5_feature_matrix_csv(
            tier_a_frame,
            context["full_feature_order"],
            root / f"tier_a_{segment_id}_{runtime_split}_feature_matrix.csv",
            metadata_columns=("partial_context_subtype", "route_role"),
        )
    tier_b_key = f"{segment_id}_tier_b_{runtime_split}"
    feature_matrices[tier_b_key] = mt5.export_mt5_feature_matrix_csv(
        tier_b_frame,
        context["tier_b_feature_order"],
        root / f"tier_b_{segment_id}_{runtime_split}_feature_matrix.csv",
        metadata_columns=("partial_context_subtype", "route_role"),
    )
    segments.append(
        SegmentAttempt(
            segment_id=segment_id,
            segment_label=segment_label,
            source_split=source_split,
            runtime_split=runtime_split,
            mode=mode,
            tier_a_matrix_key=tier_a_key,
            tier_b_matrix_key=tier_b_key,
            tier_a_rows=0 if tier_a_frame is None else int(len(tier_a_frame)),
            tier_b_rows=int(len(tier_b_frame)),
            tier_a_threshold=tier_a_threshold,
            tier_b_threshold=tier_b_threshold,
            threshold_quantile=threshold_quantile,
            max_hold_bars=max_hold_bars,
            direction=direction,
            segment_filter=segment_filter,
        )
    )


def export_filtered_pair(
    *,
    topic: FollowupTopic,
    context: Mapping[str, Any],
    tier_a_prob: pd.DataFrame,
    tier_b_prob: pd.DataFrame,
    feature_matrices: dict[str, dict[str, Any]],
    segments: list[SegmentAttempt],
    segment_id: str,
    segment_label: str,
    source_split: str,
    a_mask: pd.Series,
    b_mask: pd.Series,
    tier_a_threshold: float,
    tier_b_threshold: float,
    threshold_quantile: float,
    mode: str = "routed",
    max_hold_bars: int = DEFAULT_MAX_HOLD_BARS,
    direction: str = "both",
    segment_filter: str = "",
    mutate_feature: str | None = None,
    mutate_value: float | None = None,
) -> None:
    runtime_split = "validation_is" if source_split == "validation" else source_split
    a_frame, b_frame, _a_prob, _b_prob = split_frames(context, tier_a_prob, tier_b_prob, source_split)
    a_mask = bool_series(a_mask, len(a_frame))
    b_mask = bool_series(b_mask, len(b_frame))
    a_selected = a_frame.loc[a_mask].copy()
    b_selected = b_frame.loc[b_mask].copy()
    if mutate_feature is not None and mutate_value is not None:
        if mutate_feature in a_selected.columns:
            a_selected.loc[:, mutate_feature] = float(mutate_value)
        if mutate_feature in b_selected.columns:
            b_selected.loc[:, mutate_feature] = float(mutate_value)
    export_segment(
        topic=topic,
        context=context,
        feature_matrices=feature_matrices,
        segments=segments,
        segment_id=segment_id,
        segment_label=segment_label,
        source_split=source_split,
        runtime_split=runtime_split,
        mode=mode,
        tier_a_frame=a_selected if mode == "routed" else None,
        tier_b_frame=b_selected,
        tier_a_threshold=tier_a_threshold,
        tier_b_threshold=tier_b_threshold,
        threshold_quantile=threshold_quantile,
        max_hold_bars=max_hold_bars,
        direction=direction,
        segment_filter=segment_filter,
    )


def build_regime_split(topic: FollowupTopic, context: Mapping[str, Any], tier_a_prob: pd.DataFrame, tier_b_prob: pd.DataFrame) -> tuple[dict[str, dict[str, Any]], list[SegmentAttempt]]:
    feature_matrices: dict[str, dict[str, Any]] = {}
    segments: list[SegmentAttempt] = []
    for split in ("validation", "oos"):
        a_frame, b_frame, a_prob, b_prob = split_frames(context, tier_a_prob, tier_b_prob, split)
        cutoff = float(a_frame["historical_vol_20"].astype("float64").median())
        thresholds = (threshold_for(a_prob, topic.threshold_quantile), threshold_for(b_prob, topic.threshold_quantile))
        for suffix, label, op in (
            ("high_vol", "high volatility(고변동성)", "ge"),
            ("low_vol", "low volatility(저변동성)", "lt"),
        ):
            a_mask = a_frame["historical_vol_20"].astype("float64").ge(cutoff) if op == "ge" else a_frame["historical_vol_20"].astype("float64").lt(cutoff)
            b_mask = b_frame["historical_vol_20"].astype("float64").ge(cutoff) if op == "ge" else b_frame["historical_vol_20"].astype("float64").lt(cutoff)
            export_filtered_pair(
                topic=topic,
                context=context,
                tier_a_prob=tier_a_prob,
                tier_b_prob=tier_b_prob,
                feature_matrices=feature_matrices,
                segments=segments,
                segment_id=suffix,
                segment_label=label,
                source_split=split,
                a_mask=a_mask,
                b_mask=b_mask,
                tier_a_threshold=thresholds[0],
                tier_b_threshold=thresholds[1],
                threshold_quantile=topic.threshold_quantile,
                segment_filter=f"historical_vol_20 {'>=' if op == 'ge' else '<'} split_median {cutoff:.10g}",
            )
    return feature_matrices, segments


def build_session_timing(topic: FollowupTopic, context: Mapping[str, Any], tier_a_prob: pd.DataFrame, tier_b_prob: pd.DataFrame) -> tuple[dict[str, dict[str, Any]], list[SegmentAttempt]]:
    feature_matrices: dict[str, dict[str, Any]] = {}
    segments: list[SegmentAttempt] = []
    windows = (
        ("session_early", "early cash session(초반 정규장)", 0.0, 110.0),
        ("session_mid", "mid cash session(중반 정규장)", 110.0, 220.0),
        ("session_late", "late cash session(후반 정규장)", 220.0, 390.0),
    )
    for split in ("validation", "oos"):
        a_frame, b_frame, a_prob, b_prob = split_frames(context, tier_a_prob, tier_b_prob, split)
        thresholds = (threshold_for(a_prob, topic.threshold_quantile), threshold_for(b_prob, topic.threshold_quantile))
        for segment_id, label, low, high in windows:
            a_minutes = a_frame["minutes_from_cash_open"].astype("float64")
            b_minutes = b_frame["minutes_from_cash_open"].astype("float64")
            export_filtered_pair(
                topic=topic,
                context=context,
                tier_a_prob=tier_a_prob,
                tier_b_prob=tier_b_prob,
                feature_matrices=feature_matrices,
                segments=segments,
                segment_id=segment_id,
                segment_label=label,
                source_split=split,
                a_mask=a_minutes.ge(low) & a_minutes.lt(high),
                b_mask=b_minutes.ge(low) & b_minutes.lt(high),
                tier_a_threshold=thresholds[0],
                tier_b_threshold=thresholds[1],
                threshold_quantile=topic.threshold_quantile,
                segment_filter=f"{low:g} <= minutes_from_cash_open < {high:g}",
            )
    return feature_matrices, segments


def build_feature_mask(topic: FollowupTopic, context: Mapping[str, Any], tier_a_prob: pd.DataFrame, tier_b_prob: pd.DataFrame) -> tuple[dict[str, dict[str, Any]], list[SegmentAttempt]]:
    feature_matrices: dict[str, dict[str, Any]] = {}
    segments: list[SegmentAttempt] = []
    medians = train_medians(context)
    for split in ("validation", "oos"):
        a_frame, b_frame, a_prob, b_prob = split_frames(context, tier_a_prob, tier_b_prob, split)
        thresholds = (threshold_for(a_prob, topic.threshold_quantile), threshold_for(b_prob, topic.threshold_quantile))
        all_a = pd.Series(True, index=a_frame.index)
        all_b = pd.Series(True, index=b_frame.index)
        for feature in ("historical_vol_20", "hl_range", "minutes_from_cash_open"):
            export_filtered_pair(
                topic=topic,
                context=context,
                tier_a_prob=tier_a_prob,
                tier_b_prob=tier_b_prob,
                feature_matrices=feature_matrices,
                segments=segments,
                segment_id=f"mask_{feature}",
                segment_label=f"mask {feature}({feature} 중립화)",
                source_split=split,
                a_mask=all_a,
                b_mask=all_b,
                tier_a_threshold=thresholds[0],
                tier_b_threshold=thresholds[1],
                threshold_quantile=topic.threshold_quantile,
                segment_filter=f"{feature} set to train median {medians[feature]:.10g}",
                mutate_feature=feature,
                mutate_value=medians[feature],
            )
    return feature_matrices, segments


def build_probability_calibration(topic: FollowupTopic, context: Mapping[str, Any], tier_a_prob: pd.DataFrame, tier_b_prob: pd.DataFrame) -> tuple[dict[str, dict[str, Any]], list[SegmentAttempt]]:
    feature_matrices: dict[str, dict[str, Any]] = {}
    segments: list[SegmentAttempt] = []
    for split in ("validation", "oos"):
        _a_frame, _b_frame, a_prob, b_prob = split_frames(context, tier_a_prob, tier_b_prob, split)
        a_score = nonflat_score(a_prob)
        b_score = nonflat_score(b_prob)
        a_q80, a_q90 = float(a_score.quantile(0.80)), float(a_score.quantile(0.90))
        b_q80, b_q90 = float(b_score.quantile(0.80)), float(b_score.quantile(0.90))
        for segment_id, label, a_mask, b_mask, note in (
            ("high_conf", "high confidence(고확신)", a_score.ge(a_q90), b_score.ge(b_q90), "nonflat probability >= split q90"),
            ("mid_conf", "mid confidence(중간 확신)", a_score.ge(a_q80) & a_score.lt(a_q90), b_score.ge(b_q80) & b_score.lt(b_q90), "split q80 <= nonflat probability < split q90"),
        ):
            export_filtered_pair(
                topic=topic,
                context=context,
                tier_a_prob=tier_a_prob,
                tier_b_prob=tier_b_prob,
                feature_matrices=feature_matrices,
                segments=segments,
                segment_id=segment_id,
                segment_label=label,
                source_split=split,
                a_mask=a_mask,
                b_mask=b_mask,
                tier_a_threshold=a_q80,
                tier_b_threshold=b_q80,
                threshold_quantile=topic.threshold_quantile,
                segment_filter=note,
            )
    return feature_matrices, segments


def margin_masks(prob: pd.DataFrame, threshold: float) -> tuple[pd.Series, pd.Series, float, float]:
    score = nonflat_score(prob)
    margin = prob["probability_margin"].astype("float64")
    pass_mask = score.ge(threshold)
    if int(pass_mask.sum()) == 0:
        return pd.Series(False, index=prob.index), pd.Series(False, index=prob.index), 0.0, 0.0
    pass_margin = margin.loc[pass_mask]
    low_cut = float(pass_margin.quantile(0.30))
    high_cut = float(pass_margin.quantile(0.70))
    return pass_mask & margin.ge(high_cut), pass_mask & margin.le(low_cut), high_cut, low_cut


def build_margin_geometry(topic: FollowupTopic, context: Mapping[str, Any], tier_a_prob: pd.DataFrame, tier_b_prob: pd.DataFrame) -> tuple[dict[str, dict[str, Any]], list[SegmentAttempt]]:
    feature_matrices: dict[str, dict[str, Any]] = {}
    segments: list[SegmentAttempt] = []
    for split in ("validation", "oos"):
        _a_frame, _b_frame, a_prob, b_prob = split_frames(context, tier_a_prob, tier_b_prob, split)
        a_threshold = threshold_for(a_prob, topic.threshold_quantile)
        b_threshold = threshold_for(b_prob, topic.threshold_quantile)
        a_high, a_low, a_high_cut, a_low_cut = margin_masks(a_prob, a_threshold)
        b_high, b_low, b_high_cut, b_low_cut = margin_masks(b_prob, b_threshold)
        for segment_id, label, a_mask, b_mask, note in (
            ("high_margin", "high margin(높은 확률 여백)", a_high, b_high, f"margin >= q70 among threshold-pass rows; A {a_high_cut:.10g}, B {b_high_cut:.10g}"),
            ("low_margin", "low margin(낮은 확률 여백)", a_low, b_low, f"margin <= q30 among threshold-pass rows; A {a_low_cut:.10g}, B {b_low_cut:.10g}"),
        ):
            export_filtered_pair(
                topic=topic,
                context=context,
                tier_a_prob=tier_a_prob,
                tier_b_prob=tier_b_prob,
                feature_matrices=feature_matrices,
                segments=segments,
                segment_id=segment_id,
                segment_label=label,
                source_split=split,
                a_mask=a_mask,
                b_mask=b_mask,
                tier_a_threshold=a_threshold,
                tier_b_threshold=b_threshold,
                threshold_quantile=topic.threshold_quantile,
                segment_filter=note,
            )
    return feature_matrices, segments


def build_long_bias_source(topic: FollowupTopic, context: Mapping[str, Any], tier_a_prob: pd.DataFrame, tier_b_prob: pd.DataFrame) -> tuple[dict[str, dict[str, Any]], list[SegmentAttempt]]:
    feature_matrices: dict[str, dict[str, Any]] = {}
    segments: list[SegmentAttempt] = []
    for split in ("validation", "oos"):
        a_frame, b_frame, a_prob, b_prob = split_frames(context, tier_a_prob, tier_b_prob, split)
        a_threshold = threshold_for(a_prob, topic.threshold_quantile)
        b_threshold = threshold_for(b_prob, topic.threshold_quantile)
        a_long = a_prob["p_long"].astype("float64").ge(a_threshold)
        b_long = b_prob["p_long"].astype("float64").ge(b_threshold)
        vol_cut = float(a_frame["historical_vol_20"].astype("float64").median())
        a_high_vol = a_long & a_frame["historical_vol_20"].astype("float64").ge(vol_cut)
        b_high_vol = b_long & b_frame["historical_vol_20"].astype("float64").ge(vol_cut)
        a_open = a_long & ~a_high_vol & a_frame["minutes_from_cash_open"].astype("float64").le(110.0)
        b_open = b_long & ~b_high_vol & b_frame["minutes_from_cash_open"].astype("float64").le(110.0)
        a_other = a_long & ~(a_high_vol | a_open)
        b_other = b_long & ~(b_high_vol | b_open)
        for segment_id, label, a_mask, b_mask, note in (
            ("long_high_vol", "long high volatility(매수 고변동성)", a_high_vol, b_high_vol, "long threshold pass and high volatility"),
            ("long_open_session", "long early session(매수 초반 정규장)", a_open, b_open, "long threshold pass, not high volatility, minutes <= 110"),
            ("long_other", "long residual rows(매수 잔여 행)", a_other, b_other, "long threshold pass outside prior two buckets"),
        ):
            export_filtered_pair(
                topic=topic,
                context=context,
                tier_a_prob=tier_a_prob,
                tier_b_prob=tier_b_prob,
                feature_matrices=feature_matrices,
                segments=segments,
                segment_id=segment_id,
                segment_label=label,
                source_split=split,
                a_mask=a_mask,
                b_mask=b_mask,
                tier_a_threshold=a_threshold,
                tier_b_threshold=b_threshold,
                threshold_quantile=topic.threshold_quantile,
                direction="long_only",
                segment_filter=note,
            )
    return feature_matrices, segments


def build_tier_b_fallback_anatomy(topic: FollowupTopic, context: Mapping[str, Any], tier_a_prob: pd.DataFrame, tier_b_prob: pd.DataFrame) -> tuple[dict[str, dict[str, Any]], list[SegmentAttempt]]:
    feature_matrices: dict[str, dict[str, Any]] = {}
    segments: list[SegmentAttempt] = []
    groups = (
        ("b_macro_missing", "B macro missing(B 매크로 결측)", {"B_macro_missing"}),
        ("b_mixed_partial_context", "B mixed partial context(B 혼합 부분 문맥)", {"B_mixed_partial_context"}),
        (
            "b_core_or_outside",
            "B core or outside(B 핵심/범위 밖)",
            {"B_core_only", "B_full_context_outside_tier_a_scope", "B_constituent_missing"},
        ),
    )
    for split in ("validation", "oos"):
        _a_frame, b_frame, _a_prob, b_prob = split_frames(context, tier_a_prob, tier_b_prob, split)
        b_threshold = threshold_for(b_prob, topic.threshold_quantile)
        for segment_id, label, values in groups:
            mask = b_frame["partial_context_subtype"].astype(str).isin(values)
            export_filtered_pair(
                topic=topic,
                context=context,
                tier_a_prob=tier_a_prob,
                tier_b_prob=tier_b_prob,
                feature_matrices=feature_matrices,
                segments=segments,
                segment_id=segment_id,
                segment_label=label,
                source_split=split,
                a_mask=pd.Series(False, index=range(len(_a_frame))),
                b_mask=mask,
                tier_a_threshold=DISABLED_THRESHOLD,
                tier_b_threshold=b_threshold,
                threshold_quantile=topic.threshold_quantile,
                mode="tier_b_only",
                segment_filter=f"partial_context_subtype in {sorted(values)}",
            )
    return feature_matrices, segments


def build_hold_stress(topic: FollowupTopic, context: Mapping[str, Any], tier_a_prob: pd.DataFrame, tier_b_prob: pd.DataFrame) -> tuple[dict[str, dict[str, Any]], list[SegmentAttempt]]:
    feature_matrices: dict[str, dict[str, Any]] = {}
    segments: list[SegmentAttempt] = []
    for split in ("validation", "oos"):
        a_frame, b_frame, a_prob, b_prob = split_frames(context, tier_a_prob, tier_b_prob, split)
        thresholds = (threshold_for(a_prob, topic.threshold_quantile), threshold_for(b_prob, topic.threshold_quantile))
        all_a = pd.Series(True, index=a_frame.index)
        all_b = pd.Series(True, index=b_frame.index)
        for bars in (6, 18):
            export_filtered_pair(
                topic=topic,
                context=context,
                tier_a_prob=tier_a_prob,
                tier_b_prob=tier_b_prob,
                feature_matrices=feature_matrices,
                segments=segments,
                segment_id=f"hold_{bars}",
                segment_label=f"max hold {bars}(최대 보유 {bars}봉)",
                source_split=split,
                a_mask=all_a,
                b_mask=all_b,
                tier_a_threshold=thresholds[0],
                tier_b_threshold=thresholds[1],
                threshold_quantile=topic.threshold_quantile,
                max_hold_bars=bars,
                segment_filter=f"InpMaxHoldBars={bars}",
            )
    return feature_matrices, segments


def build_full_routed(topic: FollowupTopic, context: Mapping[str, Any], tier_a_prob: pd.DataFrame, tier_b_prob: pd.DataFrame) -> tuple[dict[str, dict[str, Any]], list[SegmentAttempt]]:
    feature_matrices: dict[str, dict[str, Any]] = {}
    segments: list[SegmentAttempt] = []
    for split in ("validation", "oos"):
        a_frame, b_frame, a_prob, b_prob = split_frames(context, tier_a_prob, tier_b_prob, split)
        all_a = pd.Series(True, index=a_frame.index)
        all_b = pd.Series(True, index=b_frame.index)
        export_filtered_pair(
            topic=topic,
            context=context,
            tier_a_prob=tier_a_prob,
            tier_b_prob=tier_b_prob,
            feature_matrices=feature_matrices,
            segments=segments,
            segment_id="plain_control",
            segment_label="plain boosting control(Plain 부스팅 대조군)",
            source_split=split,
            a_mask=all_a,
            b_mask=all_b,
            tier_a_threshold=threshold_for(a_prob, topic.threshold_quantile),
            tier_b_threshold=threshold_for(b_prob, topic.threshold_quantile),
            threshold_quantile=topic.threshold_quantile,
            segment_filter="full split with plain boosting control variant",
        )
    return feature_matrices, segments


def build_threshold_surface(topic: FollowupTopic, context: Mapping[str, Any], tier_a_prob: pd.DataFrame, tier_b_prob: pd.DataFrame) -> tuple[dict[str, dict[str, Any]], list[SegmentAttempt]]:
    feature_matrices: dict[str, dict[str, Any]] = {}
    segments: list[SegmentAttempt] = []
    for split in ("validation", "oos"):
        a_frame, b_frame, a_prob, b_prob = split_frames(context, tier_a_prob, tier_b_prob, split)
        all_a = pd.Series(True, index=a_frame.index)
        all_b = pd.Series(True, index=b_frame.index)
        for quantile in (0.70, 0.85, 0.95):
            export_filtered_pair(
                topic=topic,
                context=context,
                tier_a_prob=tier_a_prob,
                tier_b_prob=tier_b_prob,
                feature_matrices=feature_matrices,
                segments=segments,
                segment_id=f"q{int(quantile * 100)}",
                segment_label=f"threshold q{int(quantile * 100)}(임계값 q{int(quantile * 100)})",
                source_split=split,
                a_mask=all_a,
                b_mask=all_b,
                tier_a_threshold=threshold_for(a_prob, quantile),
                tier_b_threshold=threshold_for(b_prob, quantile),
                threshold_quantile=quantile,
                segment_filter=f"full split with nonflat quantile {quantile:.2f}",
            )
    return feature_matrices, segments


BUILDERS = {
    "regime_split": build_regime_split,
    "session_timing": build_session_timing,
    "feature_mask": build_feature_mask,
    "probability_calibration": build_probability_calibration,
    "margin_geometry": build_margin_geometry,
    "long_bias_source": build_long_bias_source,
    "tier_b_fallback_anatomy": build_tier_b_fallback_anatomy,
    "hold_stress": build_hold_stress,
    "plain_variant_contrast": build_full_routed,
    "threshold_surface": build_threshold_surface,
}


def copy_runtime_inputs(topic: FollowupTopic, model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, topic.run_id)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_onnx", "tier_b_onnx"):
        local_path = ROOT / model_artifacts[key]["path"]
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = Path(str(matrix["path"]))
        if not local_path.is_absolute():
            local_path = ROOT / local_path
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_attempts(
    topic: FollowupTopic,
    context: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Mapping[str, Any]],
    segments: Sequence[SegmentAttempt],
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, topic.run_id)
    tier_a_model = Path(model_artifacts["tier_a_onnx"]["path"]).name
    tier_b_model = Path(model_artifacts["tier_b_onnx"]["path"]).name
    for segment in segments:
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], segment.source_split)
        tier_b_matrix = Path(str(feature_matrices[segment.tier_b_matrix_key]["path"])).name
        a_short = segment.tier_a_threshold
        a_long = segment.tier_a_threshold
        b_short = segment.tier_b_threshold
        b_long = segment.tier_b_threshold
        if segment.direction == "long_only":
            a_short = DISABLED_THRESHOLD
            b_short = DISABLED_THRESHOLD
        elif segment.direction == "short_only":
            a_long = DISABLED_THRESHOLD
            b_long = DISABLED_THRESHOLD
        common_kwargs = {
            "run_root": topic.run_root,
            "run_id": topic.run_id,
            "stage_number": STAGE_NUMBER,
            "exploration_label": topic.exploration_label,
            "split": segment.runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": segment.max_hold_bars,
            "common_root": common,
        }
        if segment.mode == "tier_b_only":
            attempt = attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_b_{segment.segment_id}_{segment.runtime_split}",
                tier=mt5.TIER_B,
                model_path=f"{common}/models/{tier_b_model}",
                model_id=f"{topic.run_id}_tier_b",
                feature_path=f"{common}/features/{tier_b_matrix}",
                feature_count=len(context["tier_b_feature_order"]),
                feature_order_hash=context["tier_b_feature_order_hash"],
                short_threshold=b_short,
                long_threshold=b_long,
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_b_fallback",
                attempt_role="tier_b_fallback_only_total",
                record_view_prefix=f"mt5_tier_b_{segment.segment_id}",
            )
        else:
            if segment.tier_a_matrix_key is None:
                raise RuntimeError(f"routed segment missing Tier A matrix: {segment.segment_id}")
            tier_a_matrix = Path(str(feature_matrices[segment.tier_a_matrix_key]["path"])).name
            attempt = attempt_payload(
                **common_kwargs,
                attempt_name=f"routed_{segment.segment_id}_{segment.runtime_split}",
                tier=mt5.TIER_AB,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{topic.run_id}_tier_a",
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=len(context["full_feature_order"]),
                feature_order_hash=context["full_feature_order_hash"],
                short_threshold=a_short,
                long_threshold=a_long,
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix=f"mt5_routed_{segment.segment_id}",
                fallback_enabled=True,
                fallback_model_path=f"{common}/models/{tier_b_model}",
                fallback_model_id=f"{topic.run_id}_tier_b",
                fallback_feature_path=f"{common}/features/{tier_b_matrix}",
                fallback_feature_count=len(context["tier_b_feature_order"]),
                fallback_feature_order_hash=context["tier_b_feature_order_hash"],
                fallback_short_threshold=b_short,
                fallback_long_threshold=b_long,
                fallback_min_margin=MIN_MARGIN,
                fallback_invert_signal=False,
            )
        attempt["segment_id"] = segment.segment_id
        attempt["segment_label"] = segment.segment_label
        attempt["segment_filter"] = segment.segment_filter
        attempt["source_split"] = segment.source_split
        attempt["threshold_quantile"] = segment.threshold_quantile
        attempt["tier_a_threshold"] = segment.tier_a_threshold
        attempt["tier_b_threshold"] = segment.tier_b_threshold
        attempt["segment_coverage"] = {
            "tier_a_primary_labelable_rows": segment.tier_a_rows,
            "tier_b_fallback_labelable_rows": segment.tier_b_rows,
            "routed_labelable_rows": segment.tier_a_rows + segment.tier_b_rows,
            "no_tier_labelable_rows": 0,
            "partial_context_subtype_counts": subtype_counts(
                pd.read_csv(
                    io_path(ROOT / feature_matrices[segment.tier_b_matrix_key]["path"])
                    if not Path(str(feature_matrices[segment.tier_b_matrix_key]["path"])).is_absolute()
                    else io_path(Path(str(feature_matrices[segment.tier_b_matrix_key]["path"])))
                )
            ),
        }
        attempts.append(attempt)
    return attempts


def record_views_for_attempt(attempt: Mapping[str, Any]) -> set[str]:
    prefix = str(attempt.get("record_view_prefix"))
    split = str(attempt.get("split"))
    if attempt.get("routing_mode"):
        return {
            f"{prefix}_{split}",
            f"{prefix}_tier_a_used_{split}",
            f"{prefix}_tier_b_fallback_used_{split}",
        }
    return {f"{prefix}_{split}"}


def enrich_records_with_segment_metadata(records: Sequence[dict[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    lookup: dict[str, Mapping[str, Any]] = {}
    for attempt in attempts:
        for view in record_views_for_attempt(attempt):
            lookup[view] = attempt
    enriched: list[dict[str, Any]] = []
    for record in records:
        item = dict(record)
        attempt = lookup.get(str(item.get("record_view")))
        if attempt:
            metrics = dict(item.get("metrics", {}))
            coverage = attempt.get("segment_coverage", {})
            metrics.update(
                {
                    "segment_id": attempt.get("segment_id"),
                    "segment_label": attempt.get("segment_label"),
                    "segment_filter": attempt.get("segment_filter"),
                    "source_split": attempt.get("source_split"),
                    "threshold_quantile": attempt.get("threshold_quantile"),
                    "tier_a_threshold": attempt.get("tier_a_threshold"),
                    "tier_b_threshold": attempt.get("tier_b_threshold"),
                    "max_hold_bars": attempt.get("max_hold_bars"),
                    "route_coverage_split": attempt.get("source_split"),
                    "tier_a_primary_labelable_rows": coverage.get("tier_a_primary_labelable_rows"),
                    "tier_b_fallback_labelable_rows": coverage.get("tier_b_fallback_labelable_rows"),
                    "routed_labelable_rows": coverage.get("routed_labelable_rows"),
                    "no_tier_labelable_rows": coverage.get("no_tier_labelable_rows"),
                }
            )
            if item.get("route_role") in {"fallback_used", "routed_total", "tier_b_fallback_only_total"}:
                metrics["partial_context_subtype_counts"] = coverage.get("partial_context_subtype_counts", {})
            item["metrics"] = metrics
            item["segment_id"] = attempt.get("segment_id")
        enriched.append(item)
    return enriched


def execute_or_block(topic: FollowupTopic, prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.materialize_only):
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": topic.judgment_blocked,
            "failure": {"type": "materialize_only", "message": "MT5 execution was skipped by CLI flag."},
        }
    try:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
            common_files_root=COMMON_FILES_ROOT_DEFAULT,
            tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
            timeout_seconds=int(args.timeout_seconds),
        )
    except Exception as exc:
        return {
            **dict(prepared),
            "compile": {"status": "exception_or_not_completed"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": topic.judgment_blocked,
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    result["mt5_kpi_records"] = enrich_records_with_segment_metadata(result.get("mt5_kpi_records", []), prepared.get("attempts", []))
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = topic.judgment_completed if completed else topic.judgment_blocked
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = prepared["selected_variant_id"]
        record["topic_read"] = topic.topic_read
    return result


def parity_passed(model_artifacts: Mapping[str, Any]) -> bool:
    return base.parity_passed(model_artifacts)


def actual_trading_records(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        dict(record)
        for record in result.get("mt5_kpi_records", [])
        if record.get("route_role") not in {"primary_used", "fallback_used"}
    ]


def slim_record(record: Mapping[str, Any]) -> dict[str, Any]:
    metrics = record.get("metrics", {})
    metrics = metrics if isinstance(metrics, Mapping) else {}
    report = record.get("report", {})
    report_path = ""
    if isinstance(report, Mapping):
        html_report = report.get("html_report", {})
        if isinstance(html_report, Mapping):
            report_path = str(html_report.get("path") or "")
    return {
        "record_view": record.get("record_view"),
        "split": record.get("split"),
        "tier_scope": record.get("tier_scope"),
        "route_role": record.get("route_role"),
        "segment_id": metrics.get("segment_id"),
        "segment_label": metrics.get("segment_label"),
        "net_profit": metrics.get("net_profit"),
        "profit_factor": metrics.get("profit_factor"),
        "trade_count": metrics.get("trade_count"),
        "max_drawdown_amount": metrics.get("max_drawdown_amount"),
        "max_drawdown_percent": metrics.get("max_drawdown_percent"),
        "recovery_factor": metrics.get("recovery_factor"),
        "tier_a_used_count": metrics.get("tier_a_used_count"),
        "tier_b_fallback_used_count": metrics.get("tier_b_fallback_used_count"),
        "tier_a_primary_labelable_rows": metrics.get("tier_a_primary_labelable_rows"),
        "tier_b_fallback_labelable_rows": metrics.get("tier_b_fallback_labelable_rows"),
        "threshold_quantile": metrics.get("threshold_quantile"),
        "max_hold_bars": metrics.get("max_hold_bars"),
        "report_path": report_path,
    }


def build_runtime_read(topic: FollowupTopic, result: Mapping[str, Any], model_artifacts: Mapping[str, Any]) -> dict[str, Any]:
    actual = actual_trading_records(result)
    actual_slim = [slim_record(record) for record in actual]
    oos_rows = [row for row in actual_slim if row.get("split") == "oos"]
    best_oos = max(oos_rows, key=lambda row: base.safe_float(row.get("net_profit")), default={})
    worst_oos = min(oos_rows, key=lambda row: base.safe_float(row.get("net_profit")), default={})
    trade_counts = [base.safe_float(row.get("trade_count")) for row in actual_slim]
    net_values = [base.safe_float(row.get("net_profit")) for row in actual_slim]
    risk_warning = any(base.safe_float(row.get("max_drawdown_percent")) >= 25.0 for row in actual_slim)
    completed = result.get("external_verification_status") == "completed"
    parity_ok = parity_passed(model_artifacts)
    visible = completed and parity_ok and bool(actual_slim) and (max(trade_counts or [0.0]) > 0 or (max(net_values or [0.0]) - min(net_values or [0.0])) != 0)
    return {
        "model_characteristic_strength": f"{topic.topic_read}_visible" if visible else f"{topic.topic_read}_weak_or_incomplete",
        "closure_judgment": topic.judgment_completed if completed else topic.judgment_blocked,
        "runtime_read": {
            "new_characteristic_visible": visible,
            "actual_trading_record_count": len(actual_slim),
            "component_record_count": max(0, len(result.get("mt5_kpi_records", [])) - len(actual_slim)),
            "best_oos_record": best_oos,
            "worst_oos_record": worst_oos,
            "oos_net_profit_range": base.safe_float(best_oos.get("net_profit")) - base.safe_float(worst_oos.get("net_profit")) if best_oos and worst_oos else 0.0,
            "max_trade_count": max(trade_counts or [0.0]),
            "risk_warning": risk_warning,
            "diagnostic_note": "Segmented MT5 records are diagnostic runtime probes only, not synthetic combined performance.",
        },
        "segment_records": actual_slim,
    }


def build_summary(
    topic: FollowupTopic,
    result: Mapping[str, Any],
    selected: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    feature_matrices: Mapping[str, Any],
    segments: Sequence[SegmentAttempt],
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "run_number": topic.run_number,
        "run_id": topic.run_id,
        "packet_id": topic.packet_id,
        "stage_id": STAGE_ID,
        "model_family": MODEL_FAMILY,
        "topic_read": topic.topic_read,
        "question": topic.question,
        "boundary": topic.boundary,
        "judgment": result["judgment"],
        "external_verification_status": result["external_verification_status"],
        "selected_variant": selected,
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
        "python_tier_records": list(tier_records),
        "feature_matrix_count": len(feature_matrices),
        "segment_plan": [segment.__dict__ for segment in segments],
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "attempt_count": len(result.get("attempts", [])),
        "expected_attempts": topic.expected_attempts,
        "expected_kpi_records": topic.expected_kpi_records,
    }
    summary.update(build_runtime_read(topic, result, model_artifacts))
    return summary


def upsert_run_registry(topic: FollowupTopic, result: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    runtime_read = summary.get("runtime_read", {})
    best = runtime_read.get("best_oos_record", {}) if isinstance(runtime_read, Mapping) else {}
    worst = runtime_read.get("worst_oos_record", {}) if isinstance(runtime_read, Mapping) else {}
    row = {
        "run_id": topic.run_id,
        "stage_id": STAGE_ID,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
        "judgment": summary["closure_judgment"],
        "path": base.rel(topic.run_root),
        "notes": ledger_pairs(
            (
                ("model_family", MODEL_FAMILY),
                ("topic_read", topic.topic_read),
                ("selected_variant", result.get("selected_variant_id")),
                ("attempts", summary.get("attempt_count")),
                ("mt5_kpi_records", summary.get("mt5_kpi_record_count")),
                ("best_oos_view", best.get("record_view") if isinstance(best, Mapping) else None),
                ("best_oos_net_profit", best.get("net_profit") if isinstance(best, Mapping) else None),
                ("worst_oos_view", worst.get("record_view") if isinstance(worst, Mapping) else None),
                ("worst_oos_net_profit", worst.get("net_profit") if isinstance(worst, Mapping) else None),
                ("characteristic_strength", summary.get("model_characteristic_strength")),
                ("external_verification", result["external_verification_status"]),
                ("boundary", "runtime_probe_only"),
            )
        ),
    }
    return upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [row], key="run_id")


def write_run_outputs(
    topic: FollowupTopic,
    context: Mapping[str, Any],
    result: Mapping[str, Any],
    selected: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    feature_matrices: Mapping[str, Any],
    segments: Sequence[SegmentAttempt],
    kpi: Mapping[str, Any],
    created_at: str,
) -> dict[str, Any]:
    summary = build_summary(topic, result, selected, model_artifacts, prediction_artifacts, tier_records, feature_matrices, segments)
    registry_output = upsert_run_registry(topic, result, summary)
    ledger_rows = build_alpha_scout_ledger_rows(
        run_id=topic.run_id,
        stage_id=STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        selected_threshold_id=f"stage18_followup_q{topic.threshold_quantile:.2f}_or_segment_specific",
        run_output_root=topic.run_root,
        external_verification_status=result["external_verification_status"],
    )
    ledger_outputs = materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=ledger_rows,
    )
    manifest = {
        "run_id": topic.run_id,
        "packet_id": topic.packet_id,
        "stage_id": STAGE_ID,
        "run_number": topic.run_number,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": STAGE_INHERITANCE,
        "topic_read": topic.topic_read,
        "question": topic.question,
        "boundary": topic.boundary,
        "selected_variant_id": selected.get("variant_id"),
        "tier_a_feature_order_hash": context["full_feature_order_hash"],
        "tier_b_feature_order_hash": context["tier_b_feature_order_hash"],
        "threshold_policy": "validation/oos split-local non-flat quantile; no profit search; run12M uses explicit q70/q85/q95 surface",
        "segment_plan": [segment.__dict__ for segment in segments],
        "runtime_probe": {
            key: result.get(key)
            for key in (
                "attempts",
                "common_copies",
                "compile",
                "execution_results",
                "strategy_tester_reports",
                "external_verification_status",
                "judgment",
                "failure",
            )
            if key in result
        },
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
    }
    kpi_record = {
        "run_id": topic.run_id,
        "packet_id": topic.packet_id,
        "stage_id": STAGE_ID,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": False,
        "kpi_scope": f"catboost_stage18_followup_{topic.topic_read}_mt5_runtime_probe",
        "selected_variant": selected,
        "python_tier_records": list(tier_records),
        "tier_b_context_summary": context["tier_b_context_summary"],
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": result["external_verification_status"],
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "kpi_records": result.get("mt5_kpi_records", []),
        },
        "kpi_management": dict(kpi),
        "external_verification_status": result["external_verification_status"],
        "judgment": summary["closure_judgment"],
        "boundary": topic.boundary,
        "ledger_outputs": ledger_outputs,
        "registry_output": registry_output,
    }
    summary["ledger_outputs"] = ledger_outputs
    summary["registry_output"] = registry_output
    summary["kpi_management"] = dict(kpi)
    base.write_json(topic.run_root / "run_manifest.json", manifest)
    base.write_json(topic.run_root / "kpi_record.json", kpi_record)
    base.write_json(topic.run_root / "summary.json", summary)
    base.write_json(topic.packet_root / "run_summaries" / f"{topic.run_id}.json", summary)
    base.write_md(topic.run_root / "reports/result_summary.md", run_result_markdown(topic, summary, kpi))
    return summary


def gate_payloads(topic: FollowupTopic, summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> dict[str, Any]:
    runtime_ok = (
        summary["external_verification_status"] == "completed"
        and summary["attempt_count"] == topic.expected_attempts
        and summary["mt5_kpi_record_count"] == topic.expected_kpi_records
    )
    kpi_ok = kpi["normalized_records"] == topic.expected_kpi_records and kpi["parser_errors"] == 0 and kpi["missing_runs"] == 0
    parity_ok = parity_passed(summary.get("model_artifacts", {}))
    source_ok = runtime_ok and kpi_ok and parity_ok
    required = {
        "runtime_evidence_gate": "pass" if runtime_ok else "blocked",
        "scope_completion_gate": "pass" if summary.get("segment_plan") else "blocked",
        "kpi_contract_audit": "pass" if kpi_ok else "blocked",
        "source_authority_audit": "pass" if source_ok else "blocked",
        "required_gate_coverage_audit": "pass" if source_ok else "blocked",
        "final_claim_guard": "pass" if source_ok else "blocked",
    }
    return {
        "runtime_evidence_gate": {
            "audit_name": "runtime_evidence_gate",
            "status": required["runtime_evidence_gate"],
            "passed": runtime_ok,
            "expected_attempts": topic.expected_attempts,
            "expected_kpi_records": topic.expected_kpi_records,
            "counts": {"attempt_count": summary["attempt_count"], "mt5_kpi_record_count": summary["mt5_kpi_record_count"]},
        },
        "scope_completion_gate": {
            "audit_name": "scope_completion_gate",
            "status": required["scope_completion_gate"],
            "passed": bool(summary.get("segment_plan")),
            "scope": f"{topic.run_number} {topic.topic_read} segmented MT5 runtime probe",
        },
        "kpi_contract_audit": {"audit_name": "kpi_contract_audit", "status": required["kpi_contract_audit"], "passed": kpi_ok, **dict(kpi)},
        "source_authority_audit": {
            "audit_name": "source_authority_audit",
            "status": required["source_authority_audit"],
            "passed": source_ok,
            "source": "run kpi_record.json, MT5 Strategy Tester reports, normalized KPI files",
            "onnx_parity_passed": parity_ok,
        },
        "final_claim_guard": {
            "audit_name": "final_claim_guard",
            "status": required["final_claim_guard"],
            "passed": source_ok,
            "allowed_claims": [summary.get("closure_judgment"), "runtime_probe", "model_characteristic_read"],
            "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        "required_gate_coverage_audit": {
            "audit_name": "required_gate_coverage_audit",
            "status": required["required_gate_coverage_audit"],
            "passed": source_ok,
            "required_gates": required,
        },
    }


def run_result_markdown(topic: FollowupTopic, summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    lines = [
        f"# {topic.run_number} CatBoost Follow-up MT5 KPI Result({topic.run_number} 캣부스트 후속 MT5 KPI 결과)",
        "",
        f"- run(실행): `{topic.run_id}`",
        f"- topic read(주제 판독): `{topic.topic_read}`",
        f"- question(질문): {topic.question}",
        f"- selected variant(선택 변형): `{summary.get('selected_variant', {}).get('variant_id')}`",
        f"- judgment(판정): `{summary.get('closure_judgment')}`",
        f"- external verification(외부 검증): `{summary.get('external_verification_status')}`",
        f"- characteristic strength(특성 강도): `{summary.get('model_characteristic_strength')}`",
        f"- attempts(시도 수): `{summary.get('attempt_count')}`",
        f"- MT5 KPI records(MT5 KPI 기록): `{summary.get('mt5_kpi_record_count')}`",
        f"- normalized KPI records(정규화 KPI 기록): `{kpi.get('normalized_records')}`",
        "",
        "| segment(구간) | split(분할) | net profit(순손익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실폭) |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in summary.get("segment_records", []):
        lines.append(
            f"| `{row.get('record_view')}` | `{row.get('split')}` | `{row.get('net_profit')}` | `{row.get('profit_factor')}` | `{row.get('trade_count')}` | `{row.get('max_drawdown_amount')}` |"
        )
    lines.extend(
        [
            "",
            "효과(effect, 효과): 이 실행은 CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) 모델 특성을 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)로 연결했다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)


def packet_markdown(topic: FollowupTopic, summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            f"# Stage18 {topic.run_number} Follow-up Packet({topic.run_number} 후속 묶음)",
            "",
            f"- run(실행): `{topic.run_id}`",
            f"- topic read(주제 판독): `{topic.topic_read}`",
            f"- question(질문): {topic.question}",
            f"- judgment(판정): `{summary.get('closure_judgment')}`",
            f"- characteristic strength(특성 강도): `{summary.get('model_characteristic_strength')}`",
            f"- attempts(시도 수): `{summary.get('attempt_count')}`",
            f"- MT5 KPI records(MT5 KPI 기록): `{summary.get('mt5_kpi_record_count')}`",
            f"- normalized KPI records(정규화 KPI 기록): `{kpi.get('normalized_records')}`",
            f"- trade attribution records(거래 귀속 기록): `{kpi.get('trade_attribution_records')}`",
            f"- boundary(경계): `{topic.boundary}`",
            "",
            "효과(effect, 효과): Stage18(18단계) CatBoost(캣부스트) 후속 주제를 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심 성과 지표) 증거까지 묶었다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )


def write_packet_files(topic: FollowupTopic, summary: Mapping[str, Any], kpi: Mapping[str, Any], created_at: str) -> None:
    base.write_json(topic.packet_root / "aggregate_summary.json", {**dict(summary), "kpi_management": dict(kpi)})
    base.write_json(
        topic.packet_root / "artifact_index.json",
        {"run_summary": base.rel(topic.run_root / "summary.json"), "report_path": base.rel(topic.review_path), "created_at_utc": created_at},
    )
    base.write_json(
        topic.packet_root / "routing_receipt.json",
        {
            "packet_id": topic.packet_id,
            "created_at_utc": created_at,
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": [
                "obsidian-backtest-forensics",
                "obsidian-artifact-lineage",
                "obsidian-performance-attribution",
                "obsidian-result-judgment",
            ],
            "required_gates": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "source_authority_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
        },
    )
    base.write_json(
        topic.packet_root / "skill_receipts.json",
        {
            "packet_id": topic.packet_id,
            "created_at_utc": created_at,
            "receipts": [
                {"skill": "obsidian-experiment-design", "status": "completed", "question": topic.question},
                {"skill": "obsidian-runtime-parity", "status": "completed", "runtime_claim_boundary": "runtime_probe"},
                {"skill": "obsidian-backtest-forensics", "status": "completed", "backtest_judgment": "usable_with_boundary" if summary["external_verification_status"] == "completed" else "blocked"},
                {"skill": "obsidian-artifact-lineage", "status": "completed", "artifact_paths": [base.rel(topic.run_root / "run_manifest.json"), base.rel(topic.run_root / "kpi_record.json")]},
                {"skill": "obsidian-performance-attribution", "status": "completed", "attribution_confidence": "diagnostic_runtime_probe"},
                {"skill": "obsidian-result-judgment", "status": "completed", "judgment_label": summary.get("closure_judgment"), "claim_boundary": topic.boundary},
            ],
        },
    )
    for name, payload in gate_payloads(topic, summary, kpi).items():
        base.write_json(topic.packet_root / f"{name}.json", payload)
    base.write_md(topic.review_path, packet_markdown(topic, summary, kpi))


def build_topic_run(
    topic: FollowupTopic,
    args: argparse.Namespace,
    context: Mapping[str, Any],
    spec: CatBoostVariantSpec,
    created_at: str,
) -> dict[str, Any]:
    selected = selected_payload(spec)
    selected_model_artifacts, tier_a_model, tier_b_model, tier_a_prob, tier_b_prob, a_threshold, b_threshold = base.materialize_selected_models(topic, context, spec)
    tier_records, prediction_artifacts = base.python_tier_records(topic, tier_a_prob, tier_b_prob, a_threshold, b_threshold)
    onnx_artifacts = base.export_models(topic, context, selected_model_artifacts, tier_a_model, tier_b_model)
    model_artifacts = {
        **selected_model_artifacts,
        **onnx_artifacts,
        "thresholds": {"tier_a": a_threshold, "tier_b": b_threshold, "default_quantile": topic.threshold_quantile},
    }
    feature_matrices, segments = BUILDERS[topic.builder](topic, context, tier_a_prob, tier_b_prob)
    model_artifacts["segment_thresholds"] = [segment.__dict__ for segment in segments]
    copies = copy_runtime_inputs(topic, model_artifacts, feature_matrices)
    attempts = make_attempts(topic, context, model_artifacts, feature_matrices, segments)
    prepared = {
        "stage_id": STAGE_ID,
        "stage_number": STAGE_NUMBER,
        "run_id": topic.run_id,
        "run_number": topic.run_number,
        "run_root": topic.run_root,
        "selected_variant_id": selected.get("variant_id"),
        "attempts": attempts,
        "common_copies": copies,
        "route_coverage": context["tier_b_context_summary"],
        "model_artifacts": model_artifacts,
        "feature_matrices": list(feature_matrices.values()),
    }
    result = execute_or_block(topic, prepared, args)
    result["selected_variant_id"] = selected.get("variant_id")
    result["model_artifacts"] = model_artifacts
    result["feature_matrices"] = list(feature_matrices.values())
    provisional_kpi = {
        "normalized_records": 0,
        "normalized_summary_rows": 0,
        "missing_runs": 0,
        "parser_errors": 0,
        "trade_attribution_records": 0,
        "trade_level_rows": 0,
        "trade_parser_errors": 0,
    }
    write_run_outputs(topic, context, result, selected, model_artifacts, prediction_artifacts, tier_records, feature_matrices, segments, provisional_kpi, created_at)
    kpi = base.write_normalized_kpi(topic)
    summary = write_run_outputs(topic, context, result, selected, model_artifacts, prediction_artifacts, tier_records, feature_matrices, segments, kpi, created_at)
    write_packet_files(topic, summary, kpi, created_at)
    return {**summary, "kpi_management": kpi}


def aggregate_read(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [summary for summary in summaries if summary.get("external_verification_status") == "completed"]
    blocked = [summary.get("run_number") for summary in summaries if summary.get("external_verification_status") != "completed"]
    visible = [summary for summary in summaries if "visible" in str(summary.get("model_characteristic_strength"))]
    return {
        "judgment": "inconclusive_catboost_followup_batch_mt5_kpi_completed" if len(completed) == len(summaries) else "blocked_catboost_followup_batch_mt5_kpi_after_attempt",
        "claim_boundary": "runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        "completed_run_count": len(completed),
        "blocked_runs": blocked,
        "visible_topic_count": len(visible),
        "total_attempt_count": sum(int(summary.get("attempt_count") or 0) for summary in summaries),
        "total_mt5_kpi_records": sum(int(summary.get("mt5_kpi_record_count") or 0) for summary in summaries),
        "total_normalized_kpi_records": sum(int(summary.get("kpi_management", {}).get("normalized_records") or 0) for summary in summaries),
        "total_trade_attribution_records": sum(int(summary.get("kpi_management", {}).get("trade_attribution_records") or 0) for summary in summaries),
        "recommendation": "use_followup_segments_for_catboost_characteristic_attribution_only",
    }


def aggregate_markdown(summaries: Sequence[Mapping[str, Any]], read: Mapping[str, Any]) -> str:
    lines = [
        "# Stage18 CatBoost Follow-up MT5 KPI Batch(18단계 캣부스트 후속 MT5 KPI 배치)",
        "",
        f"- judgment(판정): `{read.get('judgment')}`",
        f"- boundary(경계): `{read.get('claim_boundary')}`",
        f"- completed runs(완료 실행): `{read.get('completed_run_count')}` / `{len(summaries)}`",
        f"- total attempts(전체 시도): `{read.get('total_attempt_count')}`",
        f"- total MT5 KPI records(전체 MT5 KPI 기록): `{read.get('total_mt5_kpi_records')}`",
        f"- total normalized KPI records(전체 정규화 KPI 기록): `{read.get('total_normalized_kpi_records')}`",
        "",
        "| run(실행) | topic(주제) | strength(강도) | attempts/KPI(시도/KPI) | best OOS(최고 OOS) | worst OOS(최저 OOS) |",
        "|---|---|---|---:|---:|---:|",
    ]
    for summary in summaries:
        runtime_read = summary.get("runtime_read", {})
        best = runtime_read.get("best_oos_record", {}) if isinstance(runtime_read, Mapping) else {}
        worst = runtime_read.get("worst_oos_record", {}) if isinstance(runtime_read, Mapping) else {}
        lines.append(
            f"| `{summary.get('run_number')}` | `{summary.get('topic_read')}` | `{summary.get('model_characteristic_strength')}` | `{summary.get('attempt_count')}/{summary.get('mt5_kpi_record_count')}` | `{best.get('record_view') if isinstance(best, Mapping) else None}: {best.get('net_profit') if isinstance(best, Mapping) else None}` | `{worst.get('record_view') if isinstance(worst, Mapping) else None}: {worst.get('net_profit') if isinstance(worst, Mapping) else None}` |"
        )
    lines.extend(
        [
            "",
            "효과(effect, 효과): 10개 후속 주제를 각각 다른 질문으로 나눠 CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) 모델 특성을 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)까지 연결했다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)


def write_aggregate_packet(summaries: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    read = aggregate_read(summaries)
    io_path(AGGREGATE_PACKET_ROOT).mkdir(parents=True, exist_ok=True)
    base.write_json(
        AGGREGATE_PACKET_ROOT / "aggregate_summary.json",
        {"packet_id": AGGREGATE_PACKET_ID, "created_at_utc": created_at, "run_summaries": list(summaries), "aggregate_read": read},
    )
    base.write_json(
        AGGREGATE_PACKET_ROOT / "artifact_index.json",
        {
            "run_summary_paths": [base.rel(STAGE_ROOT / "02_runs" / str(summary["run_id"]) / "summary.json") for summary in summaries],
            "report_path": base.rel(STAGE_ROOT / "03_reviews/stage18_catboost_followup_batch_mt5_kpi_packet.md"),
            "created_at_utc": created_at,
        },
    )
    all_completed = len(read.get("blocked_runs") or []) == 0
    for name, payload in {
        "performance_attribution_audit": {
            "audit_name": "performance_attribution_audit",
            "status": "pass" if all_completed else "blocked",
            "passed": all_completed,
            "attribution_confidence": "diagnostic_runtime_probe",
            "aggregate_read": read,
        },
        "result_judgment_audit": {
            "audit_name": "result_judgment_audit",
            "status": "pass" if all_completed else "blocked",
            "passed": all_completed,
            "judgment_label": read["judgment"],
            "claim_boundary": read["claim_boundary"],
        },
        "final_claim_guard": {
            "audit_name": "final_claim_guard",
            "status": "pass" if all_completed else "blocked",
            "passed": all_completed,
            "allowed_claims": [read["judgment"], "runtime_probe", "model_characteristic_read"],
            "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        "required_gate_coverage_audit": {
            "audit_name": "required_gate_coverage_audit",
            "status": "pass" if all_completed else "blocked",
            "passed": all_completed,
            "required_gates": {
                "runtime_evidence_gate": "pass" if all_completed else "blocked",
                "scope_completion_gate": "pass" if len(summaries) == len(FOLLOWUP_TOPICS) else "blocked",
                "kpi_contract_audit": "pass" if all_completed else "blocked",
                "performance_attribution_audit": "pass" if all_completed else "blocked",
                "result_judgment_audit": "pass" if all_completed else "blocked",
                "final_claim_guard": "pass" if all_completed else "blocked",
            },
        },
    }.items():
        base.write_json(AGGREGATE_PACKET_ROOT / f"{name}.json", payload)
    base.write_md(STAGE_ROOT / "03_reviews/stage18_catboost_followup_batch_mt5_kpi_packet.md", aggregate_markdown(summaries, read))
    return read


def sync_stage18_docs(summaries: Sequence[Mapping[str, Any]], aggregate: Mapping[str, Any]) -> None:
    latest = summaries[-1]
    status = "reviewed_run12D_run12M_catboost_followup_mt5_kpi"
    base.write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        "\n".join(
            [
                "# Stage18 Selection Status(18단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                f"- status(상태): `{status}`",
                f"- current run(현재 실행): `{latest.get('run_id')}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{aggregate.get('judgment')}`",
                f"- recommendation(권고): `{aggregate.get('recommendation')}`",
                f"- boundary(경계): `{aggregate.get('claim_boundary')}`",
                "",
                "효과(effect, 효과): Stage18(18단계)은 run12A-run12C(실행12A-실행12C) 기본 판독 뒤 run12D-run12M(실행12D-실행12M) 후속 MT5(`MetaTrader 5`, 메타트레이더5) KPI(`Key Performance Indicator`, 핵심 성과 지표) 배치를 완료했지만, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            ]
        ),
    )
    base.write_md(
        STAGE_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage18 Review Index(18단계 검토 색인)",
                "",
                "- base packet(기본 묶음): `stages/18_model_family_challenge__catboost_ordered_boosting_scout/03_reviews/stage18_catboost_characteristic_mt5_kpi_packet.md`",
                "- follow-up aggregate packet(후속 종합 묶음): `stages/18_model_family_challenge__catboost_ordered_boosting_scout/03_reviews/stage18_catboost_followup_batch_mt5_kpi_packet.md`",
                *[
                    f"- `{summary.get('run_id')}`: `{summary.get('closure_judgment')}`, report(보고서): `stages/18_model_family_challenge__catboost_ordered_boosting_scout/03_reviews/{FOLLOWUP_TOPICS[index].review_filename}`"
                    for index, summary in enumerate(summaries)
                ],
                "",
                "효과(effect, 효과): Stage18(18단계) CatBoost(캣부스트) 후속 10개 주제 기록을 한 곳에서 찾을 수 있다.",
            ]
        ),
    )
    state_path = ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    state = state.replace("current_run_id: run12C_catboost_q80_direction_balance_probe_v1", f"current_run_id: {latest.get('run_id')}", 1)
    stage_block = f"""stage18_catboost_followup_batch_mt5_kpi:
  stage_id: {STAGE_ID}
  status: {status}
  lane: independent_model_family_topic_pivot_no_promotion
  model_family: {MODEL_FAMILY}
  current_run_id: {latest.get('run_id')}
  run_range: run12D-run12M
  completed_run_count: {aggregate.get('completed_run_count')}
  blocked_runs: {','.join(aggregate.get('blocked_runs') or []) or 'none'}
  mt5_attempt_count: {aggregate.get('total_attempt_count')}
  mt5_kpi_record_count: {aggregate.get('total_mt5_kpi_records')}
  normalized_kpi_record_count: {aggregate.get('total_normalized_kpi_records')}
  trade_attribution_records: {aggregate.get('total_trade_attribution_records')}
  visible_topic_count: {aggregate.get('visible_topic_count')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {aggregate.get('claim_boundary')}
  aggregate_packet_path: {base.rel(STAGE_ROOT / '03_reviews/stage18_catboost_followup_batch_mt5_kpi_packet.md')}
  packet_summary_path: docs/agent_control/packets/{AGGREGATE_PACKET_ID}/aggregate_summary.json
  next_action: {aggregate.get('recommendation')}
"""
    state = base.replace_top_level_yaml_block(state, "stage18_catboost_followup_batch_mt5_kpi:", stage_block)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")

    current_path = ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    insert = "\n".join(
        [
            "## Latest Stage18 RUN12D-RUN12M Update(최신 18단계 실행12D-실행12M 업데이트)",
            "",
            "Stage18(18단계) CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) 후속 10개 주제를 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)까지 연결했다.",
            "",
            f"효과(effect, 효과): `{aggregate.get('judgment')}`로 기록했다. 이 판독은 runtime_probe(런타임 탐침)와 model characteristic read(모델 특성 판독)만 허용하며 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
        ]
    )
    if "## Latest Stage18 RUN12D-RUN12M Update" not in current:
        current = insert + current
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")

    changelog_path = ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = f"- 2026-05-03: Stage18(18단계) `run12D-run12M` CatBoost(캣부스트) 후속 MT5 KPI 배치를 완료했다. 효과(effect, 효과): 10개 주제를 runtime_probe(런타임 탐침)와 KPI(`Key Performance Indicator`, 핵심 성과 지표)로 기록하고 `{aggregate.get('judgment')}`로 판정했다.\n"
    if line not in changelog:
        io_path(changelog_path).write_text(changelog.rstrip() + "\n" + line, encoding="utf-8-sig")


def build_all(args: argparse.Namespace) -> dict[str, Any]:
    created_at = base.utc_now()
    context = base.load_context()
    specs = variant_map()
    summaries = [
        build_topic_run(topic, args, context, specs[topic.variant_id], created_at)
        for topic in FOLLOWUP_TOPICS
    ]
    aggregate = write_aggregate_packet(summaries, created_at)
    sync_stage18_docs(summaries, aggregate)
    payload = {"aggregate": aggregate, "summaries": summaries}
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2))
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage18 CatBoost follow-up MT5 KPI batch.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--materialize-only", action="store_true")
    args = parser.parse_args(argv)
    build_all(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
