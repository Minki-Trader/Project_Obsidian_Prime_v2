from __future__ import annotations

import numpy as np
import pandas as pd

from foundation.alpha.discrete_signal_table import export_single_discrete_signal_score_table
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.features import volatility_squeeze_expansion as vse
from foundation.models.ebm_score_table import load_ebm_score_table, score_ebm_table_probabilities
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage40 import volatility_squeeze_expansion_scout as st40


def sample_common() -> pd.DataFrame:
    timestamps = pd.date_range("2025-01-01", periods=10, freq="5min", tz="UTC")
    return pd.DataFrame(
        {
            "stage40_row_id": range(10),
            "timestamp": timestamps,
            "timestamp_utc": timestamps.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "split": ["train", "train", "validation", "validation", "oos", "oos", "validation", "oos", "train", "oos"],
            "validation_oos_split_label": ["train", "train", "validation_is", "validation_is", "oos", "oos", "validation_is", "oos", "train", "oos"],
            "label_class": [0, 1, 2, 0, 2, 0, 1, 2, 0, 1],
            "tier_label": [mt5.TIER_A, mt5.TIER_B, mt5.TIER_A, mt5.TIER_B, mt5.TIER_A, mt5.TIER_B, mt5.TIER_A, mt5.TIER_B, mt5.TIER_A, mt5.TIER_B],
            "routing_source": ["tier_a_primary", "tier_b_fallback"] * 5,
            "partial_context_subtype": ["Tier_A_full_context", "B_mixed_partial_context"] * 5,
            "tier_a_available": [True, False] * 5,
            "tier_b_fallback_available": [False, True] * 5,
            "return_zscore_20": [1.2, -1.1, 1.4, -1.5, 1.3, -1.2, np.nan, 0.9, 1.0, -0.8],
            "bollinger_width_20": [0.01, 0.01, 0.008, 0.009, 0.011, 0.012, 0.01, 0.01, 0.011, 0.012],
            "bb_position_20": [0.82, 0.18, 0.86, 0.16, 0.80, 0.20, 0.90, 0.10, 0.60, 0.40],
            "bb_squeeze": [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            "historical_vol_5_over_20": [1.3, 1.2, 1.4, 1.5, 1.3, 1.2, 1.1, 1.4, 1.5, 1.6],
            "adx_14": [24, 25, 26, 27, 28, 29, 12, 11, 30, 31],
            "di_spread_14": [9, -9, 10, -10, 8, -8, 2, -2, 11, -11],
            "ema20_ema50_diff": [0.2, -0.2, 0.3, -0.3, 0.2, -0.2, 0.1, -0.1, 0.2, -0.2],
            "minutes_from_cash_open": [5, 5, 10, 10, 15, 15, 20, 20, 35, 35],
            "is_first_30m_after_open": [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        }
    )


def test_discrete_signal_score_table_maps_short_flat_long(tmp_path) -> None:
    path = tmp_path / "signal_table.csv"
    payload = export_single_discrete_signal_score_table(path, feature_order=vse.SIGNAL_FEATURE_ORDER)
    table = load_ebm_score_table(path, feature_count=1)
    probs = score_ebm_table_probabilities(table, np.asarray([[-1.0], [0.0], [1.0]]))
    assert payload["feature_order_hash"]
    assert probs[0, 0] > 0.99
    assert probs[1, 1] > 0.99
    assert probs[2, 2] > 0.99


def test_broad_candidate_grid_has_independent_volatility_squeeze_branches() -> None:
    grid = vse.build_broad_candidate_grid()
    assert len(grid) == 12
    assert grid[0].candidate_id == "c01_reference_return_z_momentum"
    assert grid[-1].rule_code == "squeeze_adx_di_alignment"
    assert len({spec.mechanism_family for spec in grid}) >= 6


def test_candidate_signal_respects_missingness_and_tier_routing() -> None:
    common = sample_common()
    thresholds = vse.build_thresholds(common)
    spec = next(item for item in vse.build_broad_candidate_grid() if item.candidate_id == "c02_squeeze_breakout_bb_position")
    frame = vse.apply_candidate_to_table(common, spec, thresholds)
    validation_signals = frame.loc[frame["split"].eq("validation"), vse.SIGNAL_FEATURE_ORDER[0]].tolist()
    assert validation_signals[:2] == [1, -1]
    assert frame.loc[frame["stage40_surface_missing"], vse.SIGNAL_FEATURE_ORDER[0]].eq(0).all()
    assert {"tier_a_primary", "tier_b_fallback"} <= set(frame["routing_source"])


def test_candidate_summary_tracks_tier_b_and_rejection_reasons() -> None:
    common = sample_common()
    thresholds = vse.build_thresholds(common)
    frames = {spec.candidate_id: vse.apply_candidate_to_table(common, spec, thresholds) for spec in vse.build_broad_candidate_grid()[:2]}
    rows = vse.summarize_candidate_frames(frames)
    assert {row["candidate_id"] for row in rows} == {"c01_reference_return_z_momentum", "c02_squeeze_breakout_bb_position"}
    assert all("tier_b_fallback_signal_count" in row for row in rows)
    assert any(str(row["candidate_rejection_reason"]).startswith("thin_trade_stream") for row in rows)


def test_route_coverage_records_tier_a_b_and_no_tier_counts() -> None:
    common = sample_common()
    coverage = vse.route_coverage_from_common(common, {"validation": 3, "oos": 2})
    assert coverage["by_split"]["validation"]["tier_a_primary_rows"] == 2
    assert coverage["by_split"]["validation"]["tier_b_fallback_rows"] == 1
    assert coverage["no_tier_by_split"]["validation"] == 3


def test_micro_gate_rejects_oos_negative_or_thin_mt5_candidate() -> None:
    rows = [
        {"candidate_id": "c02", "split": "validation_is", "net_profit": 50, "profit_factor": 1.2, "trade_count": 30, "actual_routed_total_count_mt5": 30, "tier_b_fallback_used_count_mt5": 5},
        {"candidate_id": "c02", "split": "oos", "net_profit": -5, "profit_factor": 0.9, "trade_count": 18, "actual_routed_total_count_mt5": 18, "tier_b_fallback_used_count_mt5": 2},
    ]
    gate = st40.evaluate_micro_search_gate(rows)
    assert gate["status"] == "failed"
    assert "oos_net_not_positive" in gate["rejected_candidates"][0]["reason"]
    assert "trade_count_too_thin_for_micro_search" in gate["rejected_candidates"][0]["reason"]


def test_promotion_gate_blocks_positive_rows_without_cluster_check() -> None:
    rows = [
        {"candidate_id": "c02", "split": "validation_is", "net_profit": 100, "profit_factor": 1.2, "trade_count": 30, "max_drawdown": 40, "actual_routed_total_count_mt5": 30, "tier_b_fallback_used_count_mt5": 5},
        {"candidate_id": "c02", "split": "oos", "net_profit": 80, "profit_factor": 1.15, "trade_count": 28, "max_drawdown": 35, "actual_routed_total_count_mt5": 28, "tier_b_fallback_used_count_mt5": 4},
    ]
    gate = st40.evaluate_promotion_candidate_gate(rows)
    assert gate["status"] == "failed"
    assert "cluster_concentration_check_not_available_for_positive_gate" in gate["rejected_candidates"][0]["reason"]


def test_attempt_payload_accepts_stage40_discrete_signal_handoff(tmp_path) -> None:
    payload = attempt_payload(
        run_root=tmp_path,
        run_id=st40.RUN_ID,
        stage_number=40,
        exploration_label=st40.EXPLORATION_LABEL,
        attempt_name="routed_c02_validation_is",
        tier=mt5.TIER_AB,
        split="validation_is",
        model_path="Project_Obsidian_Prime_v2/stage40/models/signal.csv",
        model_id="stage40_signal_table",
        model_backend="ebm_table",
        feature_path="Project_Obsidian_Prime_v2/stage40/features/tier_a.csv",
        feature_count=1,
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
        common_root="Project_Obsidian_Prime_v2/stage40/run34A",
        fallback_enabled=True,
        fallback_model_path="Project_Obsidian_Prime_v2/stage40/models/signal.csv",
        fallback_model_backend="ebm_table",
        fallback_feature_path="Project_Obsidian_Prime_v2/stage40/features/tier_b.csv",
        fallback_feature_count=1,
        fallback_feature_order_hash="hash",
    )
    text = (tmp_path / "mt5/routed_c02_validation_is.set").read_text(encoding="utf-8")
    assert "InpModelBackend=ebm_table" in text
    assert "InpFallbackEnabled=true" in text
    assert payload["routing_mode"] == mt5.ROUTING_MODE_A_B_FALLBACK


def test_merge_execution_results_marks_blocked_micro_as_partial() -> None:
    broad = {"external_verification_status": "completed", "attempts": [1], "candidate_specs": [1], "common_copies": [], "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "python_candidate_summary": [], "feature_matrices": {}}
    micro = {"external_verification_status": "blocked", "attempts": [2], "candidate_specs": [2], "common_copies": [], "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "python_candidate_summary": [], "feature_matrices": {}}
    merged = st40.merge_execution_results(broad, micro)
    assert merged["external_verification_status"] == "partial_completed_with_blocked_micro_attempt"
    assert merged["attempts"] == [1, 2]
