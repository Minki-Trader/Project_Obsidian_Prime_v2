from __future__ import annotations

from pathlib import Path

import pandas as pd

from foundation.labels.directional_asymmetric import (
    CLASS_ID_MAP,
    SIGNAL_FEATURE_ORDER,
    DirectionalAsymmetricLabelSpec,
    build_stage41_broad_candidate_grid,
    build_stage41_micro_candidate_grid,
    label_lineage_rows,
    leakage_audit,
    materialize_directional_asymmetric_labels,
    split_label_distribution,
)
from stage_pipelines.stage41.directional_asymmetric_label_horizon_probe import (
    RUN_ID,
    STAGE_NUMBER,
    make_attempts,
)


def _base_frame() -> pd.DataFrame:
    timestamps = pd.date_range("2025-01-02T16:35:00Z", periods=40, freq="5min")
    frame = pd.DataFrame({"timestamp": timestamps})
    frame["split"] = "train"
    frame.loc[20:29, "split"] = "validation"
    frame.loc[30:, "split"] = "oos"
    frame["minutes_from_cash_open"] = range(0, 200, 5)
    frame["historical_vol_20"] = 0.002
    frame["is_first_30m_after_open"] = frame["minutes_from_cash_open"].le(30).astype(int)
    frame["is_last_30m_before_cash_close"] = 0
    frame["tier_label"] = "Tier A"
    frame["routing_source"] = "tier_a_primary"
    frame["partial_context_subtype"] = "Tier_A_full_context"
    frame["timestamp_utc"] = frame["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return frame


def _raw_close() -> pd.DataFrame:
    timestamps = pd.date_range("2025-01-02T16:35:00Z", periods=60, freq="5min")
    close = [100.0 + idx * 0.10 for idx in range(len(timestamps))]
    close[8] = 102.5
    close[18] = 98.0
    return pd.DataFrame({"timestamp": timestamps, "close": close})


def test_candidate_grid_has_required_stage41_families() -> None:
    specs = build_stage41_broad_candidate_grid()
    ids = [spec.candidate_id for spec in specs]

    assert len(ids) == 17
    assert ids[0] == "c01_current_label_reference"
    assert "c04_asymmetric_long_slow_short_fast" in ids
    assert "c09_volatility_normalized_return_label" in ids
    assert "c17_extreme_horizon_stress" in ids


def test_label_generation_uses_exact_future_closed_bar_alignment() -> None:
    spec = DirectionalAsymmetricLabelSpec(
        candidate_id="unit",
        label_id="unit_label",
        description="unit",
        label_family="unit",
        long_horizon_bars=2,
        short_horizon_bars=4,
    )

    labeled = materialize_directional_asymmetric_labels(_base_frame(), _raw_close(), spec, base_threshold=0.001)

    first = labeled.iloc[0]
    assert first["stage41_long_future_timestamp"] == first["timestamp"] + pd.Timedelta(minutes=10)
    assert first["stage41_short_future_timestamp"] == first["timestamp"] + pd.Timedelta(minutes=20)
    assert "stage41_label_class" in labeled.columns
    assert set(labeled["stage41_label_class"].unique()).issubset(set(CLASS_ID_MAP.values()))


def test_leakage_audit_rejects_no_future_feature_read() -> None:
    spec = DirectionalAsymmetricLabelSpec(
        candidate_id="unit",
        label_id="unit_label",
        description="unit",
        label_family="unit",
        long_horizon_bars=2,
        short_horizon_bars=4,
    )
    labeled = materialize_directional_asymmetric_labels(_base_frame(), _raw_close(), spec, base_threshold=0.001)
    audit = leakage_audit(labeled, spec)

    assert audit["status"] == "passed"
    assert audit["future_timestamps_after_current"] is True
    assert audit["model_feature_reads_future_columns"] is False


def test_volatility_and_session_adjustment_change_effective_thresholds() -> None:
    base = _base_frame()
    base.loc[10:, "historical_vol_20"] = 0.004
    spec = DirectionalAsymmetricLabelSpec(
        candidate_id="vol_session",
        label_id="vol_session_label",
        description="unit",
        label_family="unit",
        long_horizon_bars=2,
        short_horizon_bars=2,
        volatility_normalization=True,
        session_adjustment=True,
    )

    labeled = materialize_directional_asymmetric_labels(base, _raw_close(), spec, base_threshold=0.001)

    assert labeled["stage41_long_effective_threshold"].max() > labeled["stage41_long_effective_threshold"].min()
    assert labeled["stage41_short_effective_threshold"].max() > labeled["stage41_short_effective_threshold"].min()


def test_distribution_summary_flags_pathological_balance() -> None:
    spec = DirectionalAsymmetricLabelSpec(
        candidate_id="unit",
        label_id="unit_label",
        description="unit",
        label_family="unit",
        long_horizon_bars=2,
        short_horizon_bars=2,
        long_threshold_multiplier=100.0,
        short_threshold_multiplier=100.0,
    )
    labeled = materialize_directional_asymmetric_labels(_base_frame(), _raw_close(), spec, base_threshold=0.001)
    summary = split_label_distribution(labeled)

    assert summary["train"]["class_balance_status"] == "pathological"


def test_micro_grid_is_bounded_around_best_candidate() -> None:
    broad = build_stage41_broad_candidate_grid()
    micro = build_stage41_micro_candidate_grid("c04_asymmetric_long_slow_short_fast", broad)

    assert len(micro) == 4
    assert all(spec.candidate_id.startswith("m") for spec in micro)
    assert max(spec.max_horizon_bars for spec in micro) <= 30


def test_lineage_rows_record_closed_bar_source() -> None:
    specs = build_stage41_broad_candidate_grid()[:2]
    rows = label_lineage_rows(specs, source_data_path="data/raw/mt5_bars/m5/US100/bars.csv")

    assert rows[0]["timestamp_rule"].startswith("bar close")
    assert rows[0]["used_directly_in_mt5"] is False


def test_attempt_manifest_uses_candidate_horizon_as_hold_bars(tmp_path: Path) -> None:
    spec = build_stage41_broad_candidate_grid()[3]
    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2025-01-02T16:35:00Z", "2025-01-02T16:40:00Z"], utc=True),
            "split": ["validation", "oos"],
            "tier_label": ["Tier A", "Tier A"],
        }
    )
    feature_exports = {}
    for runtime_split in ("validation_is", "oos"):
        feature_exports[f"{spec.candidate_id}_tier_a_{runtime_split}"] = {"path": f"{spec.candidate_id}_a_{runtime_split}.csv"}
        feature_exports[f"{spec.candidate_id}_tier_b_fallback_{runtime_split}"] = {"path": f"{spec.candidate_id}_b_{runtime_split}.csv"}
    attempts = make_attempts([spec], feature_exports, {"path": "stage41_signal_table.csv"}, frame)

    assert attempts[0]["max_hold_bars"] == spec.max_horizon_bars
    assert attempts[0]["set"]["path"].endswith(".set")
    assert RUN_ID in attempts[0]["set"]["path"]
    assert STAGE_NUMBER == 41
    assert SIGNAL_FEATURE_ORDER == ("stage41_directional_label_signal",)
