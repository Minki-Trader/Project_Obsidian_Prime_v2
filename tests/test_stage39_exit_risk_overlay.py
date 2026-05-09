from __future__ import annotations

import numpy as np
import pandas as pd

from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.models.ebm_score_table import load_ebm_score_table, score_ebm_table_probabilities
from foundation.risk import exit_overlay as overlay
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage39 import exit_risk_non_entry_overlay as st39


def sample_common() -> pd.DataFrame:
    timestamps = pd.date_range("2025-01-01", periods=8, freq="5min", tz="UTC")
    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "split": ["train", "train", "validation", "validation", "oos", "oos", "validation", "oos"],
            "label_class": [0, 1, 2, 0, 1, 2, 0, 1],
            "tier_label": [mt5.TIER_A, mt5.TIER_B, mt5.TIER_A, mt5.TIER_B, mt5.TIER_A, mt5.TIER_B, mt5.TIER_A, mt5.TIER_B],
            "routing_source": ["tier_a_primary", "tier_b_fallback"] * 4,
            "partial_context_subtype": ["Tier_A_full_context", "B_mixed_partial_context"] * 4,
            "tier_a_available": [True, False] * 4,
            "tier_b_fallback_available": [False, True] * 4,
            "stage39_base_entry_signal": [1, -1, 1, -1, 1, -1, 0, 1],
            "stage24_survival_risk_z": [0.1, 0.2, 1.2, 1.3, 0.9, 1.5, np.nan, 1.1],
            "stage25_hazard_risk_z": [0.1, 0.2, 1.1, 1.4, 1.2, 0.1, 1.0, 1.4],
            "stage27_tail_pressure": [0.001, 0.002, 0.010, 0.011, 0.012, 0.001, 0.013, 0.014],
            "stage39_surface_missing": [False, False, False, False, False, False, True, False],
        }
    )


def test_broad_candidate_grid_matches_required_stage39_ids() -> None:
    grid = overlay.build_broad_candidate_grid()
    assert len(grid) == 17
    assert grid[0].candidate_id == "c01_no_overlay_reference"
    assert grid[-1].candidate_id == "c17_direction_specific_lifecycle_tail_exit"


def test_exit_overlay_does_not_change_base_entry_signal_and_respects_missingness() -> None:
    common = sample_common()
    thresholds = overlay.build_loose_thresholds(common)
    spec = next(item for item in overlay.build_broad_candidate_grid() if item.candidate_id == "c08_survival_hazard_tail_exit")
    frame = overlay.apply_exit_overlay_candidate(common, spec, thresholds)
    assert frame[overlay.STAGE39_FEATURE_ORDER[0]].tolist() == common["stage39_base_entry_signal"].tolist()
    assert frame.loc[common["stage39_surface_missing"], "overlay_risk_active"].eq(False).all()
    assert frame[overlay.STAGE39_FEATURE_ORDER[1]].isin([0, 1]).all()
    assert frame[overlay.STAGE39_FEATURE_ORDER[2]].isin([0, 1]).all()


def test_reduce_max_hold_candidate_exports_hold_override_not_entry_filter() -> None:
    common = sample_common()
    thresholds = overlay.build_loose_thresholds(common)
    spec = next(item for item in overlay.build_broad_candidate_grid() if item.candidate_id == "c13_reduce_max_hold_on_hazard")
    frame = overlay.apply_exit_overlay_candidate(common, spec, thresholds)
    assert frame[overlay.STAGE39_FEATURE_ORDER[0]].tolist() == common["stage39_base_entry_signal"].tolist()
    assert frame[overlay.STAGE39_FEATURE_ORDER[1]].eq(0).all()
    assert frame[overlay.STAGE39_FEATURE_ORDER[2]].eq(0).all()
    assert set(frame[overlay.STAGE39_FEATURE_ORDER[3]].unique()).issubset({0, 6})


def test_entry_count_stability_guard_and_candidate_summary() -> None:
    common = sample_common()
    thresholds = overlay.build_loose_thresholds(common)
    frames = {spec.candidate_id: overlay.apply_exit_overlay_candidate(common, spec, thresholds) for spec in overlay.build_broad_candidate_grid()[:2]}
    summary = overlay.summarize_candidate_frames(frames)
    assert {row["candidate_id"] for row in summary} == {"c01_no_overlay_reference", "c02_survival_clock_exit"}
    assert all(row["base_entry_count_stable"] for row in summary)
    assert all(row["entry_count_delta_vs_reference"] == 0 for row in summary)


def test_hold_metrics_from_telemetry_actions() -> None:
    actions = [
        {"exec_action": "open_long", "position_before": "none"},
        {"exec_action": "hold_same_direction", "position_before": "long"},
        {"exec_action": "close_exit_overlay", "position_before": "long"},
        {"exec_action": "open_short", "position_before": "none"},
        {"exec_action": "close_exit_overlay_max_hold", "position_before": "short"},
    ]
    metrics = overlay.hold_metrics_from_actions(actions)
    assert metrics["entry_count_runtime"] == 2
    assert metrics["early_exit_count_runtime"] == 2
    assert metrics["max_hold_bars"] == 2


def test_stage39_score_table_keeps_overlay_features_neutral(tmp_path) -> None:
    path = tmp_path / "stage39_score_table.csv"
    st39.export_signal_score_table(path)
    table = load_ebm_score_table(path, feature_count=4)
    probs = score_ebm_table_probabilities(table, np.asarray([[-1.0, 1.0, 1.0, 6.0], [0.0, 1.0, 1.0, 6.0], [1.0, 1.0, 1.0, 6.0]]))
    assert probs[0, 0] > 0.99
    assert probs[1, 1] > 0.99
    assert probs[2, 2] > 0.99


def test_attempt_payload_accepts_stage39_exit_overlay_set_values(tmp_path) -> None:
    payload = attempt_payload(
        run_root=tmp_path,
        run_id="run33A",
        stage_number=39,
        exploration_label="stage39",
        attempt_name="routed_c02_validation_is",
        tier=mt5.TIER_AB,
        split="validation_is",
        model_path="common/model.csv",
        model_id="model",
        model_backend="ebm_table",
        feature_path="common/features.csv",
        feature_count=4,
        feature_order_hash="hash",
        short_threshold=0.55,
        long_threshold=0.55,
        min_margin=0.0,
        invert_signal=False,
        from_date="2025.01.01",
        to_date="2025.01.02",
        primary_active_tier="tier_a",
        attempt_role="routed_total",
        record_view_prefix="mt5_routed_c02",
        max_hold_bars=12,
        common_root="Project_Obsidian_Prime_v2/stage39/run33A",
        fallback_enabled=True,
        extra_set_values={"InpExitRiskOverlayEnabled": True, "InpExitRiskCloseLongFeatureIndex": 1},
    )
    text = (tmp_path / "mt5/routed_c02_validation_is.set").read_text(encoding="utf-8")
    assert "InpExitRiskOverlayEnabled=true" in text
    assert "InpExitRiskCloseLongFeatureIndex=1" in text
    assert payload["extra_set_values"]["InpExitRiskCloseLongFeatureIndex"] == 1
