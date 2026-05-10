from __future__ import annotations

import pandas as pd

from stage_pipelines.stage49.reversal_selection_rule_mt5 import (
    SOURCE_SIGNAL_COLUMN,
    apply_rule_to_feature_frame,
    decide_judgment,
    route_coverage_from_audit,
)


def test_apply_rule_only_flattens_short_adx_20_25() -> None:
    frame = pd.DataFrame(
        {
            SOURCE_SIGNAL_COLUMN: [-1, -1, 1, 0, -1],
            "adx_14": [19.9, 20.0, 23.0, 24.0, 25.1],
            "entry_decision": ["short", "short", "long", "flat", "short"],
        }
    )

    filtered, removed = apply_rule_to_feature_frame(frame)

    assert removed == 1
    assert filtered[SOURCE_SIGNAL_COLUMN].tolist() == [-1, 0, 1, 0, -1]
    assert filtered["entry_decision"].tolist() == ["short", "flat", "long", "flat", "short"]


def test_decision_positive_only_when_both_mt5_deltas_positive() -> None:
    rows = [
        {"split": "validation_is", "net_profit_delta": 1.0},
        {"split": "oos", "net_profit_delta": 2.0},
    ]

    judgment, reason = decide_judgment(rows, "completed")

    assert "positive_runtime_linkage" in judgment
    assert "both_split_mt5_net_profit_delta_positive" in reason


def test_decision_blocked_when_mt5_not_completed() -> None:
    rows = [
        {"split": "validation_is", "net_profit_delta": 1.0},
        {"split": "oos", "net_profit_delta": 2.0},
    ]

    judgment, reason = decide_judgment(rows, "blocked")

    assert judgment.startswith("blocked_runtime_probe")
    assert reason == "mt5_strategy_tester_output_missing_or_partial"


def test_route_coverage_keeps_validation_alias_for_kpi_enrichment() -> None:
    audit = [
        {"split": "validation_is", "tier_scope": "Tier A", "input_rows": 10},
        {"split": "validation_is", "tier_scope": "Tier B", "input_rows": 3},
        {"split": "oos", "tier_scope": "Tier A", "input_rows": 8},
        {"split": "oos", "tier_scope": "Tier B", "input_rows": 2},
    ]

    coverage = route_coverage_from_audit(audit)

    assert coverage["by_split"]["validation"]["tier_a_primary_rows"] == 10
    assert coverage["by_split"]["validation"]["tier_b_fallback_rows"] == 3
    assert coverage["by_split"]["oos"]["routed_labelable_rows"] == 10
