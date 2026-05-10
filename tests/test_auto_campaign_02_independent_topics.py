from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from foundation.features.independent_alpha_campaign import (
    CORE_FEATURES,
    STAGE_TOPICS,
    apply_candidate_to_table,
    build_broad_candidate_grid,
    build_micro_candidate_grid,
    build_stage_model_context,
    lineage_rows,
    summarize_candidate_frames,
    topic_schema,
)
from stage_pipelines.auto_campaign_02.independent_runtime_probe import (
    build_mt5_candidate_summary,
    make_attempts,
    model_context_manifest,
)


def _base_frame(rows: int = 96) -> pd.DataFrame:
    timestamps = pd.date_range("2025-01-02T16:35:00Z", periods=rows, freq="5min")
    frame = pd.DataFrame(
        {
            "timestamp": timestamps,
            "timestamp_utc": timestamps.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "split": ["train"] * 56 + ["validation"] * 20 + ["oos"] * (rows - 76),
            "validation_oos_split_label": ["train"] * 56 + ["validation_is"] * 20 + ["oos"] * (rows - 76),
            "symbol": "US100",
            "label_class": ([2, 0, 1, 2, 0, 1] * ((rows // 6) + 1))[:rows],
            "tier_label": (["Tier A", "Tier B"] * ((rows // 2) + 1))[:rows],
            "routing_source": (["tier_a_primary", "tier_b_fallback"] * ((rows // 2) + 1))[:rows],
            "partial_context_subtype": (["Tier_A_full_context", "missing_secondary_context"] * ((rows // 2) + 1))[:rows],
            "tier_a_available": ([True, False] * ((rows // 2) + 1))[:rows],
            "tier_b_fallback_available": ([False, True] * ((rows // 2) + 1))[:rows],
        }
    )
    x = np.linspace(-2.0, 2.0, rows)
    for idx, feature in enumerate(CORE_FEATURES):
        frame[feature] = np.sin(x + idx * 0.17) + (idx % 5) * 0.05
    frame["hl_range"] = np.linspace(0.001, 0.006, rows)
    frame["bb_squeeze"] = (np.arange(rows) % 4 == 0).astype(int)
    frame["adx_14"] = 18.0 + (np.arange(rows) % 12)
    frame["di_spread_14"] = np.where(np.arange(rows) % 2 == 0, 1.0, -1.0)
    frame["return_zscore_20"] = np.tile([1.4, -1.3, 0.2, 0.9, -0.8, 0.1], rows // 6 + 1)[:rows]
    frame["bollinger_width_20"] = np.linspace(0.004, 0.020, rows)
    frame["historical_vol_5_over_20"] = np.tile([0.8, 1.1, 1.4, 0.9, 1.6, 1.2], rows // 6 + 1)[:rows]
    frame["atr_14_over_atr_50"] = np.tile([0.75, 0.95, 1.15, 0.85, 1.25, 1.05], rows // 6 + 1)[:rows]
    return frame


def test_all_campaign02_topics_have_broad_grids_and_schema() -> None:
    for topic in STAGE_TOPICS.values():
        specs = build_broad_candidate_grid(topic)
        schema = topic_schema(topic)

        assert len(specs) == 8
        assert specs[0].candidate_id.startswith("c01")
        assert schema[0]["column"] == topic.signal_column


def test_candidate_application_records_signal_missingness_and_tier_counts() -> None:
    common = _base_frame()
    for topic in STAGE_TOPICS.values():
        context = build_stage_model_context(common, topic)
        specs = build_broad_candidate_grid(topic)[:2]
        frames = {spec.candidate_id: apply_candidate_to_table(common, topic, spec, context) for spec in specs}
        summary = summarize_candidate_frames(topic, frames, specs)

        assert all(topic.signal_column in frame.columns for frame in frames.values())
        assert all(set(frame[topic.signal_column].unique()).issubset({-1, 0, 1}) for frame in frames.values())
        assert any(row["tier_a_used_count"] >= 0 and row["tier_b_fallback_used_count"] >= 0 for row in summary)
        assert any(row["split"] == "validation_is" for row in summary)


def test_stage47_source_signals_do_not_force_missing_flat_signal() -> None:
    common = _base_frame()
    topic = STAGE_TOPICS[47]
    context = build_stage_model_context(common, topic)
    spec = build_broad_candidate_grid(topic)[2]

    scored = apply_candidate_to_table(common, topic, spec, context)

    assert scored[f"{topic.short_stage()}_missing"].sum() == 0
    assert scored[topic.signal_column].abs().sum() > 0


def test_model_context_manifest_summarizes_source_signal_series() -> None:
    common = _base_frame()
    topic = STAGE_TOPICS[47]
    manifest = model_context_manifest(build_stage_model_context(common, topic))

    assert "source_signals" in manifest
    assert manifest["source_signals"]["reference"]["rows"] == len(common)
    assert "ranked_features" in manifest


def test_micro_grid_is_bounded_around_broad_candidate() -> None:
    topic = STAGE_TOPICS[45]
    broad = build_broad_candidate_grid(topic)
    micro = build_micro_candidate_grid(topic, broad[1].candidate_id, broad)

    assert len(micro) == 4
    assert all(spec.candidate_id.startswith("m") for spec in micro)


def test_lineage_rows_record_closed_bar_mt5_direct_signal() -> None:
    topic = STAGE_TOPICS[43]
    specs = build_broad_candidate_grid(topic)[:2]
    rows = lineage_rows(topic, specs, "data/processed/model_inputs/unit.parquet")

    assert rows[0]["timestamp_rule"] == "closed M5 bar close"
    assert rows[0]["used_directly_in_mt5"] == topic.signal_column
    assert rows[0]["missingness_behavior"].startswith("flat signal")


def test_attempt_manifest_carries_candidate_identity() -> None:
    topic = STAGE_TOPICS[43]
    spec = build_broad_candidate_grid(topic)[0]
    common = _base_frame().loc[lambda frame: frame["tier_label"].eq("Tier A")].copy()
    feature_exports = {}
    for runtime_split in ("validation_is", "oos"):
        feature_exports[f"{spec.candidate_id}_tier_a_{runtime_split}"] = {"path": f"{spec.candidate_id}_a_{runtime_split}.csv"}
        feature_exports[f"{spec.candidate_id}_tier_b_fallback_{runtime_split}"] = {"path": f"{spec.candidate_id}_b_{runtime_split}.csv"}

    attempts = make_attempts(topic, [spec], feature_exports, {"path": "stage43_signal_table.csv"}, common)

    assert attempts[0]["candidate_id"] == spec.candidate_id
    assert attempts[0]["candidate_token"] == "c01"
    assert Path(attempts[0]["set"]["path"]).suffix == ".set"


def test_mt5_candidate_summary_maps_attempt_back_to_full_candidate_id() -> None:
    topic = STAGE_TOPICS[43]
    candidate_id = build_broad_candidate_grid(topic)[0].candidate_id
    row = build_mt5_candidate_summary(
        topic,
        [
            {
                "record_view": "mt5_routed_c01",
                "record_split": "validation_is",
                "tier_scope": "actual routed total",
                "subrun_id": "routed_c01_validation_is",
                "status": "completed",
                "metrics": {"net_profit": 12.0, "profit_factor": 1.2, "trade_count": 30},
                "path": "report.xml",
            }
        ],
        [
            {
                "candidate_id": candidate_id,
                "split": "validation_is",
                "tier_a_used_count": 10,
                "tier_b_fallback_used_count": 2,
                "actual_routed_total_count": 12,
            }
        ],
        [{"attempt_name": "routed_c01_validation_is", "candidate_id": candidate_id, "status": "completed"}],
    )[0]

    assert row["candidate_id"] == candidate_id
    assert row["actual_routed_total_count_mt5"] == 12
