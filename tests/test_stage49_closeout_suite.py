from __future__ import annotations

from stage_pipelines.stage49.closeout_suite import hold_bucket, leave_one_month_stability, subtype_allowed


def test_subtype_allowed_variants_are_exclusive() -> None:
    assert subtype_allowed("subtype_macro_only", "B_macro_missing")
    assert not subtype_allowed("subtype_macro_only", "B_core_only")
    assert subtype_allowed("subtype_non_macro_only", "B_core_only")
    assert not subtype_allowed("subtype_non_macro_only", "B_macro_missing")


def test_hold_bucket_boundaries() -> None:
    assert hold_bucket(None) == "hold_missing"
    assert hold_bucket(6) == "hold_0_6"
    assert hold_bucket(12) == "hold_7_12"
    assert hold_bucket(24) == "hold_13_24"
    assert hold_bucket(25) == "hold_gt24"


def test_leave_one_month_stability_detects_fragility() -> None:
    rows = [
        {"month": "2025-10", "net_profit": 10.0},
        {"month": "2025-11", "net_profit": 20.0},
        {"month": "2025-12", "net_profit": -5.0},
    ]

    result = leave_one_month_stability(rows)

    assert result["total_net_profit"] == 25.0
    assert result["worst_month"] == "2025-12"
    assert result["leave_one_month_min_net_profit"] == 5.0
    assert result["stability_status"] == "passed"
