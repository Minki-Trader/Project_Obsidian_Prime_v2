from __future__ import annotations

import pandas as pd

from foundation.features.independent_alpha_campaign import STAGE_TOPICS
from stage_pipelines.stage48.survivor_cluster_concentration import (
    _parse_metrics,
    _top_bucket,
    _specs_for_stage,
    build_decision_rows,
)


def test_top_bucket_returns_label_count_and_share() -> None:
    label, count, share = _top_bucket(pd.Series(["a", "a", "b", "c"]), 4)

    assert label == "a"
    assert count == 2
    assert share == 0.5


def test_decision_row_marks_signal_concentration_risk() -> None:
    roster = [
        type(
            "Source",
            (),
            {
                "stage_number": 43,
                "stage_id": "43_model_rebuild__low_complexity_feature_subset_regularized_signal",
                "run_id": "run37A_low_complexity_feature_subset_rebuild_broad_mt5_probe_v1",
                "candidate_id": "c02_top8_stability_ranked_elasticnet",
                "source_reason": "unit",
            },
        )()
    ]
    concentration = [
        {
            "stage_number": 43,
            "source_candidate_id": "c02_top8_stability_ranked_elasticnet",
            "split": "validation_is",
            "concentration_reasons": "top_month_share_gt_45pct",
        },
        {
            "stage_number": 43,
            "source_candidate_id": "c02_top8_stability_ranked_elasticnet",
            "split": "oos",
            "concentration_reasons": "none",
        },
    ]
    mt5 = [
        {
            "stage_number": 43,
            "candidate_id": "c02_top8_stability_ranked_elasticnet",
            "split": "validation_is",
            "net_profit": 10,
            "profit_factor": 1.2,
            "trade_count": 40,
        },
        {
            "stage_number": 43,
            "candidate_id": "c02_top8_stability_ranked_elasticnet",
            "split": "oos",
            "net_profit": 5,
            "profit_factor": 1.1,
            "trade_count": 40,
        },
    ]

    rows = build_decision_rows(roster, concentration, mt5)

    assert rows[0]["stage_number"] == 43
    assert rows[0]["decision_status"] == "concentration_risk_or_thin_signal_level"


def test_specs_for_stage_recovers_micro_candidate_from_parent() -> None:
    specs = _specs_for_stage(
        STAGE_TOPICS[43],
        {"micro_search_gate": {"best_candidate": "m01_relaxed_c02_top8_stability_ranked_elasticnet"}},
    )

    assert "m01_relaxed_c02_top8_stability_ranked_elasticnet" in specs
    assert "m04_extreme_stress_c02_top8_stability_ranked_elasticnet" in specs


def test_parse_metrics_salvages_truncated_stage_ledger_json() -> None:
    metrics = _parse_metrics(
        '{"net_profit":564.49,"profit_factor":1.23,"fill_count":708,'
        '"max_drawdown_amount":284.47,"report_path":"C:/truncated'
    )

    assert metrics["parse_status"] == "truncated_json_salvaged"
    assert metrics["net_profit"] == 564.49
    assert metrics["profit_factor"] == 1.23
    assert metrics["fill_count"] == 708
