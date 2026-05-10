from __future__ import annotations

import pandas as pd

from stage_pipelines.stage50 import adx_reference_wfo_stress as stage50


def test_window_mask_uses_half_open_dates() -> None:
    frame = pd.DataFrame(
        {
            "_timestamp_dt": pd.to_datetime(
                ["2025-03-31T22:00:00Z", "2025-04-01T16:35:00Z", "2025-06-30T22:00:00Z", "2025-07-01T16:35:00Z"],
                utc=True,
            )
        }
    )
    mask = stage50.window_mask(frame, stage50.WFO_WINDOWS[0])
    assert mask.tolist() == [False, True, True, False]


def test_summarize_rolling_robustness_passes_three_positive_windows() -> None:
    rows = [
        {"variant_id": "adx_20_25", "window_id": "w01_2025q2", "net_profit": 10.0, "profit_factor": 1.2, "trade_count": 4},
        {"variant_id": "adx_20_25", "window_id": "w02_2025q3", "net_profit": 12.0, "profit_factor": 1.3, "trade_count": 5},
        {"variant_id": "adx_20_25", "window_id": "w03_2025q4", "net_profit": -2.0, "profit_factor": 0.9, "trade_count": 3},
        {"variant_id": "adx_20_25", "window_id": "w04_2026q1", "net_profit": 8.0, "profit_factor": 1.1, "trade_count": 2},
    ]
    summary = stage50.summarize_rolling_robustness(rows)
    assert summary[0]["variant_id"] == "adx_20_25"
    assert summary[0]["positive_windows"] == 3
    assert summary[0]["negative_windows"] == 1
    assert summary[0]["total_net_profit"] == 28.0
    assert summary[0]["robustness_status"] == "passed"


def test_decide_judgment_keeps_reference_variant_boundary() -> None:
    mt5_result = {"external_verification_status": "completed"}
    robustness_rows = [
        {"variant_id": "adx_19_24", "robustness_status": "passed"},
        {"variant_id": stage50.REFERENCE_VARIANT, "robustness_status": "weak"},
    ]
    judgment, reason = stage50.decide_judgment(mt5_result, robustness_rows)
    assert judgment == stage50.INCONCLUSIVE_JUDGMENT
    assert reason == "comparison_variant_passed_but_stage49_reference_variant_did_not"


def test_route_coverage_for_windows_uses_window_ids() -> None:
    audit_rows = [
        {"window_id": "w01_2025q2", "window_rows": 100},
        {"window_id": "w01_2025q2", "window_rows": 100},
        {"window_id": "w02_2025q3", "window_rows": 80},
    ]
    coverage = stage50.route_coverage_for_windows(audit_rows)
    assert coverage["by_split"]["w01_2025q2"]["tier_a_primary_rows"] == 100
    assert coverage["by_split"]["w02_2025q3"]["routed_labelable_rows"] == 80

