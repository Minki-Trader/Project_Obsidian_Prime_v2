from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from foundation.control_plane.ledger import io_path
from foundation.models.baseline_training import LABEL_ORDER
from foundation.models.ebm_score_table import FIELDNAMES, load_ebm_score_table, score_ebm_table_probabilities
from foundation.models.onnx_bridge import sha256_file


STATE_FEATURE_NAME = "hmm_state_code"


def _format_float(value: Any) -> str:
    return f"{float(value):.17g}"


def state_policy_frame(
    sequence: pd.DataFrame,
    *,
    split: str = "train",
    state_column: str = "hidden_state",
    label_column: str = "label_class",
    smoothing: float = 1.0,
) -> pd.DataFrame:
    required = {state_column, label_column, "split"}
    missing = sorted(required.difference(sequence.columns))
    if missing:
        raise ValueError(f"HMM state policy sequence missing columns: {missing}")
    source = sequence.loc[sequence["split"].astype(str).eq(str(split))].copy()
    if source.empty:
        raise ValueError(f"HMM state policy split is empty: {split}")
    states = sorted(int(value) for value in source[state_column].dropna().unique())
    if states != list(range(max(states) + 1)):
        raise ValueError(f"HMM states must be contiguous from zero: {states}")

    rows: list[dict[str, Any]] = []
    alpha = float(smoothing)
    for state in states:
        part = source.loc[source[state_column].astype("int64").eq(state)]
        counts = part[label_column].astype("int64").value_counts().to_dict()
        smoothed = np.asarray([counts.get(index, 0) + alpha for index in range(len(LABEL_ORDER))], dtype="float64")
        probabilities = smoothed / smoothed.sum()
        logits = np.log(probabilities)
        rows.append(
            {
                "hidden_state": state,
                "rows": int(len(part)),
                "short_count": int(counts.get(0, 0)),
                "flat_count": int(counts.get(1, 0)),
                "long_count": int(counts.get(2, 0)),
                "p_short": float(probabilities[0]),
                "p_flat": float(probabilities[1]),
                "p_long": float(probabilities[2]),
                "score_short": float(logits[0]),
                "score_flat": float(logits[1]),
                "score_long": float(logits[2]),
            }
        )
    return pd.DataFrame(rows).sort_values("hidden_state").reset_index(drop=True)


def export_hmm_state_policy_score_table(
    policy: pd.DataFrame,
    output_path: Path,
    *,
    feature_name: str = STATE_FEATURE_NAME,
) -> dict[str, Any]:
    required = {"hidden_state", "score_short", "score_flat", "score_long"}
    missing = sorted(required.difference(policy.columns))
    if missing:
        raise ValueError(f"HMM state policy table missing columns: {missing}")
    states = sorted(int(value) for value in policy["hidden_state"].dropna().unique())
    if states != list(range(max(states) + 1)):
        raise ValueError(f"HMM states must be contiguous from zero: {states}")
    by_state = {int(row.hidden_state): row for row in policy.itertuples(index=False)}

    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(output_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerow(
            {
                "record_type": "intercept",
                "feature_index": -1,
                "item_index": -1,
                "value": "",
                "score_short": _format_float(0.0),
                "score_flat": _format_float(0.0),
                "score_long": _format_float(0.0),
            }
        )
        for cut_index in range(max(states)):
            writer.writerow(
                {
                    "record_type": "cut",
                    "feature_index": 0,
                    "item_index": cut_index,
                    "value": _format_float(cut_index + 0.5),
                    "score_short": "",
                    "score_flat": "",
                    "score_long": "",
                }
            )
        for score_index in range(len(states) + 1):
            state = max(0, score_index - 1)
            row = by_state[state]
            writer.writerow(
                {
                    "record_type": "score",
                    "feature_index": 0,
                    "item_index": score_index,
                    "value": "",
                    "score_short": _format_float(row.score_short),
                    "score_flat": _format_float(row.score_flat),
                    "score_long": _format_float(row.score_long),
                }
            )
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "format": "hmm_state_policy_ebm_score_table_csv_v1",
        "class_order": list(LABEL_ORDER),
        "feature_count": 1,
        "feature_names": [feature_name],
        "state_count": len(states),
        "runtime_policy": "mql5_ebm_table_backend_state_code_lookup_softmax",
        "claim_boundary": "hmm_state_policy_runtime_probe_not_live_hmm_runtime_authority",
    }


def attach_state_policy_probabilities(
    sequence: pd.DataFrame,
    policy: pd.DataFrame,
    *,
    state_column: str = "hidden_state",
) -> pd.DataFrame:
    state_policy = policy.loc[:, ["hidden_state", "p_short", "p_flat", "p_long"]].copy()
    out = sequence.merge(state_policy, how="left", left_on=state_column, right_on="hidden_state", suffixes=("", "_policy"))
    if out[["p_short", "p_flat", "p_long"]].isna().any().any():
        raise ValueError("HMM state policy did not cover all sequence states.")
    out["probability_margin"] = np.maximum(out["p_short"], out["p_long"]) - out["p_flat"]
    return out


def check_hmm_state_policy_table_parity(
    policy: pd.DataFrame,
    table_path: Path,
    state_values: np.ndarray,
    *,
    tolerance: float = 1.0e-10,
) -> dict[str, Any]:
    values = np.asarray(state_values, dtype="float64").reshape(-1, 1)
    table = load_ebm_score_table(table_path, feature_count=1)
    table_prob = score_ebm_table_probabilities(table, values)
    state_policy = policy.set_index("hidden_state")[["p_short", "p_flat", "p_long"]]
    expected = np.asarray([state_policy.loc[int(value), :].to_numpy(dtype="float64") for value in values.reshape(-1)])
    max_abs_diff = float(np.max(np.abs(expected - table_prob))) if len(values) else 0.0
    return {
        "passed": bool(max_abs_diff <= float(tolerance)),
        "max_abs_diff": max_abs_diff,
        "tolerance": float(tolerance),
        "rows": int(len(values)),
        "table_path": table_path.as_posix(),
        "claim_boundary": "state_table_lookup_parity_not_mt5_runtime_authority",
    }
