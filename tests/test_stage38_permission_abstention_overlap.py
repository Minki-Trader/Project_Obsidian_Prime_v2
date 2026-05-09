from __future__ import annotations

import numpy as np
import pandas as pd

from foundation.models.ebm_score_table import load_ebm_score_table, score_ebm_table_probabilities
from stage_pipelines.stage38 import permission_abstention_overlap as st38


def sample_common() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "stage38_row_id": range(6),
            "timestamp": pd.date_range("2025-01-01", periods=6, freq="5min", tz="UTC"),
            "timestamp_utc": pd.date_range("2025-01-01", periods=6, freq="5min", tz="UTC").strftime("%Y-%m-%dT%H:%M:%SZ"),
            "split": ["train", "validation", "validation", "oos", "oos", "train"],
            "validation_oos_split_label": ["train", "validation_is", "validation_is", "oos", "oos", "train"],
            "label_class": [0, 2, 1, 2, 0, 1],
            "tier_label": [st38.mt5.TIER_A, st38.mt5.TIER_A, st38.mt5.TIER_B, st38.mt5.TIER_A, st38.mt5.TIER_B, st38.mt5.TIER_B],
            "routing_source": ["tier_a_primary", "tier_a_primary", "tier_b_fallback", "tier_a_primary", "tier_b_fallback", "tier_b_fallback"],
            "partial_context_subtype": ["Tier_A_full_context"] * 6,
            "tier_a_available": [True, True, False, True, False, False],
            "tier_b_fallback_available": [False, False, True, False, True, True],
            "p_flat": [0.3, 0.2, 0.4, 0.3, 0.6, 0.2],
            "calibrated_margin": [0.2, 0.4, 0.2, 0.3, -0.1, 0.4],
            "entropy": [0.4, 0.3, 0.7, 0.5, 0.9, 0.4],
            "tail_pressure": [0.2, 0.1, 0.5, 0.3, 0.8, 0.2],
            "ebm_direction": [0.2, 0.3, -0.2, 0.4, -0.1, 0.2],
            "ebm_abs_direction": [0.2, 0.3, 0.2, 0.4, 0.1, 0.2],
            "permission_score": [0.2, 0.3, 0.2, 0.4, 0.1, 0.2],
            "permission_filter_signal": [True, True, True, True, False, True],
            "permission_direction": [1, 1, -1, 1, -1, 1],
            "calibrated_direction": [1, 1, -1, 1, 0, 1],
            "ebm_direction_signal": [1, 1, -1, 1, -1, 1],
            "target_direction": [1, 1, -1, 1, -1, 1],
            "surface_missing": [False, False, False, False, False, True],
        }
    )


def test_candidate_grid_has_required_broad_branches() -> None:
    grid = st38.build_candidate_grid()
    assert len(grid) == 17
    assert grid[0].candidate_id == "c01_no_overlap_reference"
    assert grid[-1].enabled_surfaces == ("permission", "abstention", "entropy", "tail", "ebm")


def test_candidate_signal_respects_missingness_and_tier_routing() -> None:
    common = sample_common()
    thresholds = {
        "permission_score_min": 0.15,
        "p_flat_max": 0.5,
        "calibrated_margin_min": 0.0,
        "entropy_max": 0.8,
        "tail_pressure_max": 0.6,
        "ebm_abs_min": 0.15,
    }
    spec = st38.CandidateSpec(
        candidate_id="c17_permission_abstention_entropy_tail_ebm",
        label="all surfaces",
        enabled_surfaces=("permission", "abstention", "entropy", "tail", "ebm"),
        entry_permission_rule="permission",
        abstention_rule="abstention",
    )
    frame = st38.apply_candidate_to_table(common, spec, thresholds)
    assert frame.loc[frame["split"].eq("validation"), st38.SIGNAL_FEATURE_ORDER[0]].tolist() == [1, -1]
    assert frame.loc[frame["surface_missing"], st38.SIGNAL_FEATURE_ORDER[0]].eq(0).all()


def test_thinning_metrics_and_rejection_reason() -> None:
    common = sample_common()
    thresholds = {
        "permission_score_min": 0.15,
        "p_flat_max": 0.5,
        "calibrated_margin_min": 0.0,
        "entropy_max": 0.8,
        "tail_pressure_max": 0.6,
        "ebm_abs_min": 0.15,
    }
    frames = {spec.candidate_id: st38.apply_candidate_to_table(common, spec, thresholds) for spec in st38.build_candidate_grid()[:2]}
    rows = st38.compute_candidate_summary(frames)
    assert {row["candidate_id"] for row in rows} == {"c01_no_overlap_reference", "c02_permission_only"}
    assert all("thinning_ratio_vs_reference" in row for row in rows)
    assert any(row["candidate_rejection_reason"].startswith("thin_trade_stream") for row in rows)


def test_signal_score_table_maps_short_flat_long(tmp_path) -> None:
    path = tmp_path / "signal_table.csv"
    st38.export_signal_score_table(path)
    table = load_ebm_score_table(path, feature_count=1)
    probs = score_ebm_table_probabilities(table, np.asarray([[-1.0], [0.0], [1.0]]))
    assert probs[0, 0] > 0.99
    assert probs[1, 1] > 0.99
    assert probs[2, 2] > 0.99


def test_micro_gate_rejects_fragile_or_negative_candidate() -> None:
    rows = [
        {"candidate_id": "c01", "split": "validation_is", "net_profit": 10, "profit_factor": 1.2, "trade_count": 2, "actual_routed_total_count_mt5": 2, "tier_b_fallback_used_count_mt5": 0},
        {"candidate_id": "c01", "split": "oos", "net_profit": -1, "profit_factor": 0.9, "trade_count": 2, "actual_routed_total_count_mt5": 2, "tier_b_fallback_used_count_mt5": 0},
    ]
    gate = st38.evaluate_micro_search_gate(rows)
    assert gate["status"] == "failed"
    assert "oos_net_not_positive" in gate["rejected_candidates"][0]["reason"]

