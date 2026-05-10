from __future__ import annotations

import pandas as pd

from stage_pipelines.stage49.followup_suite import SOURCE_SIGNAL_COLUMN, apply_band_rule, evaluate_band_robustness


def test_apply_band_rule_flattens_only_short_inside_band() -> None:
    frame = pd.DataFrame(
        {
            SOURCE_SIGNAL_COLUMN: [-1, -1, -1, 1],
            "adx_14": [18.9, 20.0, 25.1, 22.0],
            "entry_decision": ["short", "short", "short", "long"],
        }
    )

    filtered, removed = apply_band_rule(frame, 20, 25)

    assert removed == 1
    assert filtered[SOURCE_SIGNAL_COLUMN].tolist() == [-1, 0, -1, 1]
    assert filtered["entry_decision"].tolist() == ["short", "flat", "short", "long"]


def test_evaluate_band_robustness_passes_when_four_variants_improve_both_splits() -> None:
    rows = []
    for index in range(4):
        for split in ("validation_is", "oos"):
            rows.append({"variant_id": f"adx_{index}", "split": split, "net_profit_delta_vs_original": 1.0 + index})
    for split in ("validation_is", "oos"):
        rows.append({"variant_id": "adx_bad", "split": split, "net_profit_delta_vs_original": -1.0})

    result = evaluate_band_robustness(rows)

    assert result["status"] == "passed"
    assert result["passed_variant_count"] == 4
