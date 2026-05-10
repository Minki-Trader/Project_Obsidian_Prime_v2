from __future__ import annotations

from stage_pipelines.stage50 import followup_suite as suite


def test_summarize_route_robustness_passes_three_windows() -> None:
    rows = [
        {"route_view": "tier_a_primary_tier_b_fallback_routed_total", "window_id": "w01_2025q2", "net_profit": -5.0, "profit_factor": 0.9, "trade_count": 10},
        {"route_view": "tier_a_primary_tier_b_fallback_routed_total", "window_id": "w02_2025q3", "net_profit": 50.0, "profit_factor": 1.4, "trade_count": 20},
        {"route_view": "tier_a_primary_tier_b_fallback_routed_total", "window_id": "w03_2025q4", "net_profit": 40.0, "profit_factor": 1.3, "trade_count": 15},
        {"route_view": "tier_a_primary_tier_b_fallback_routed_total", "window_id": "w04_2026q1", "net_profit": 30.0, "profit_factor": 1.2, "trade_count": 12},
    ]
    summary = suite.summarize_route_robustness(rows)
    assert summary[0]["positive_windows"] == 3
    assert summary[0]["total_net_profit"] == 115.0
    assert summary[0]["robustness_status"] == "passed"


def test_cost_rows_apply_extra_cost_per_trade() -> None:
    trades = [
        {"window_id": "w01_2025q2", "net_profit": 10.0},
        {"window_id": "w01_2025q2", "net_profit": -2.0},
    ]
    rows = suite.build_cost_rows("source", "run", "route", trades)
    cost_one = next(row for row in rows if row["extra_cost_per_trade"] == 1.0 and row["window_id"] == "w01_2025q2")
    assert cost_one["trade_count"] == 2
    assert cost_one["base_net_profit"] == 8.0
    assert cost_one["adjusted_net_profit"] == 6.0
    assert cost_one["positive_after_cost"] is True


def test_overlap_summary_flags_high_concentration() -> None:
    rows = []
    for variant in ("a", "b", "c", "d"):
        rows.append({"window_id": "w01_2025q2", "trade_key": "buy|2025-04-01 16:40:00", "variant_id": variant, "net_profit": 10.0})
    rows.append({"window_id": "w01_2025q2", "trade_key": "sell|2025-04-02 16:40:00", "variant_id": "a", "net_profit": -1.0})
    clusters = suite.overlap_clusters(rows)
    summary = suite.overlap_summary(rows, clusters)
    q2 = next(row for row in summary if row["window_id"] == "w01_2025q2")
    assert q2["keys_seen_in_4plus_variants"] == 1
    assert q2["concentration_status"] == "high_concentration"


def test_route_coverage_for_run44c_uses_tier_counts() -> None:
    audit_rows = [
        {"window_id": "w01_2025q2", "tier_scope": "Tier A", "window_rows": 100},
        {"window_id": "w01_2025q2", "tier_scope": "Tier B", "window_rows": 25},
    ]
    coverage = suite.route_coverage_for_run44c(audit_rows)
    assert coverage["by_split"]["w01_2025q2"]["tier_a_primary_rows"] == 100
    assert coverage["by_split"]["w01_2025q2"]["tier_b_fallback_rows"] == 25
    assert coverage["by_split"]["w01_2025q2"]["routed_labelable_rows"] == 125

