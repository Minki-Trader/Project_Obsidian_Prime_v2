from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from foundation.control_plane.ledger import io_path, sha256_file_lf_normalized
from foundation.models.ebm_score_table import FIELDNAMES, load_ebm_score_table, score_ebm_table_probabilities
from foundation.models.onnx_bridge import ordered_hash


DISCRETE_SIGNAL_SAMPLE_VALUES = np.asarray([[-1.0], [0.0], [1.0]], dtype="float64")


def _format_score(value: Any) -> str:
    return f"{float(value):.17g}"


def export_single_discrete_signal_score_table(
    path: Path,
    *,
    feature_order: Sequence[str],
    logit_strength: float = 4.0,
    format_name: str = "single_discrete_signal_ebm_score_table_csv_v1",
) -> dict[str, Any]:
    """Write a one-feature EBM-compatible table mapping -1/0/+1 to short/flat/long."""

    if len(feature_order) != 1:
        raise ValueError("single discrete signal table requires exactly one feature")
    strength = float(logit_strength)
    rows = [
        {
            "record_type": "intercept",
            "feature_index": -1,
            "item_index": -1,
            "value": "",
            "score_short": "0",
            "score_flat": "0",
            "score_long": "0",
        },
        {
            "record_type": "cut",
            "feature_index": 0,
            "item_index": 0,
            "value": "-0.5",
            "score_short": "",
            "score_flat": "",
            "score_long": "",
        },
        {
            "record_type": "cut",
            "feature_index": 0,
            "item_index": 1,
            "value": "0.5",
            "score_short": "",
            "score_flat": "",
            "score_long": "",
        },
        {
            "record_type": "score",
            "feature_index": 0,
            "item_index": 0,
            "value": "",
            "score_short": _format_score(strength),
            "score_flat": _format_score(-strength),
            "score_long": _format_score(-strength),
        },
        {
            "record_type": "score",
            "feature_index": 0,
            "item_index": 1,
            "value": "",
            "score_short": _format_score(strength),
            "score_flat": _format_score(-strength),
            "score_long": _format_score(-strength),
        },
        {
            "record_type": "score",
            "feature_index": 0,
            "item_index": 2,
            "value": "",
            "score_short": _format_score(-strength),
            "score_flat": _format_score(strength),
            "score_long": _format_score(-strength),
        },
        {
            "record_type": "score",
            "feature_index": 0,
            "item_index": 3,
            "value": "",
            "score_short": _format_score(-strength),
            "score_flat": _format_score(-strength),
            "score_long": _format_score(strength),
        },
    ]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    table = load_ebm_score_table(path, feature_count=1)
    probabilities = score_ebm_table_probabilities(table, DISCRETE_SIGNAL_SAMPLE_VALUES)
    return {
        "path": path.as_posix(),
        "sha256": sha256_file_lf_normalized(path),
        "format": format_name,
        "feature_order": list(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "parity_sample_values": DISCRETE_SIGNAL_SAMPLE_VALUES.reshape(-1).tolist(),
        "parity_sample_probabilities": probabilities.tolist(),
        "runtime_policy": "-1 short, 0 flat, +1 long through EBM-table softmax and EA probability thresholds",
    }
