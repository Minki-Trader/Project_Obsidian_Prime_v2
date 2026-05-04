from __future__ import annotations

import numpy as np
import pandas as pd

from foundation.control_plane.ledger import io_path
from foundation.models.ebm_score_table import load_ebm_score_table, score_ebm_table_probabilities
from foundation.models.hmm_state_policy import (
    check_hmm_state_policy_table_parity,
    export_hmm_state_policy_score_table,
    state_policy_frame,
)


def test_hmm_state_policy_exports_ebm_compatible_state_table(tmp_path) -> None:
    sequence = pd.DataFrame(
        {
            "split": ["train"] * 8,
            "hidden_state": [0, 0, 0, 0, 1, 1, 1, 1],
            "label_class": [0, 0, 0, 1, 2, 2, 2, 1],
        }
    )
    policy = state_policy_frame(sequence, smoothing=0.5)
    output = tmp_path / "hmm_state_policy_score_table.csv"

    export = export_hmm_state_policy_score_table(policy, output)
    table = load_ebm_score_table(output, feature_count=1)
    probabilities = score_ebm_table_probabilities(table, np.asarray([[0.0], [1.0]], dtype="float64"))
    parity = check_hmm_state_policy_table_parity(policy, output, np.asarray([0.0, 1.0]))

    assert export["format"] == "hmm_state_policy_ebm_score_table_csv_v1"
    assert export["feature_count"] == 1
    assert export["state_count"] == 2
    assert probabilities[0, 0] > probabilities[0, 2]
    assert probabilities[1, 2] > probabilities[1, 0]
    assert parity["passed"] is True
    assert io_path(output).read_text(encoding="utf-8").startswith("record_type,feature_index")
