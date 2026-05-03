from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from foundation.control_plane.ledger import io_path
from foundation.models.baseline_training import LABEL_ORDER
from foundation.models.ebm_onnx import _validate_main_effects
from foundation.models.onnx_bridge import ordered_sklearn_probabilities, sha256_file


FIELDNAMES = ["record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long"]


def _format_float(value: Any) -> str:
    return f"{float(value):.17g}"


def export_ebm_main_effect_score_table(
    model: Any,
    output_path: Path,
    *,
    feature_count: int,
) -> dict[str, Any]:
    """Export a main-effect EBM as a compact CSV score table for MQL5 scoring."""

    _validate_main_effects(model, feature_count)
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(output_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        intercept = np.asarray(model.intercept_, dtype="float64")
        writer.writerow(
            {
                "record_type": "intercept",
                "feature_index": -1,
                "item_index": -1,
                "value": "",
                "score_short": _format_float(intercept[0]),
                "score_flat": _format_float(intercept[1]),
                "score_long": _format_float(intercept[2]),
            }
        )
        for term_index, term_features in enumerate(model.term_features_):
            feature_index = int(tuple(term_features)[0])
            cuts = np.asarray(model.bins_[feature_index][0], dtype="float64")
            scores = np.asarray(model.term_scores_[term_index], dtype="float64")
            for cut_index, cut_value in enumerate(cuts):
                writer.writerow(
                    {
                        "record_type": "cut",
                        "feature_index": feature_index,
                        "item_index": cut_index,
                        "value": _format_float(cut_value),
                        "score_short": "",
                        "score_flat": "",
                        "score_long": "",
                    }
                )
            for bin_index, row in enumerate(scores):
                writer.writerow(
                    {
                        "record_type": "score",
                        "feature_index": feature_index,
                        "item_index": bin_index,
                        "value": "",
                        "score_short": _format_float(row[0]),
                        "score_flat": _format_float(row[1]),
                        "score_long": _format_float(row[2]),
                    }
                )
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "format": "ebm_main_effect_score_table_csv_v1",
        "class_order": list(LABEL_ORDER),
        "feature_count": int(feature_count),
        "runtime_policy": "mql5_direct_bin_lookup_additive_softmax",
    }


def load_ebm_score_table(path: Path, *, feature_count: int) -> dict[str, Any]:
    cuts: list[list[float]] = [[] for _ in range(int(feature_count))]
    scores: list[list[list[float]]] = [[] for _ in range(int(feature_count))]
    intercept = np.zeros(len(LABEL_ORDER), dtype="float64")
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            record_type = str(row.get("record_type", "")).strip().lower()
            if record_type == "intercept":
                intercept = np.asarray([row["score_short"], row["score_flat"], row["score_long"]], dtype="float64")
                continue
            feature_index = int(row["feature_index"])
            if feature_index < 0 or feature_index >= int(feature_count):
                raise ValueError(f"EBM score table feature index outside width: {feature_index}")
            if record_type == "cut":
                cuts[feature_index].append(float(row["value"]))
            elif record_type == "score":
                scores[feature_index].append([float(row["score_short"]), float(row["score_flat"]), float(row["score_long"])])
            else:
                raise ValueError(f"Unknown EBM score table row type: {record_type}")
    return {
        "intercept": intercept,
        "cuts": [np.asarray(item, dtype="float64") for item in cuts],
        "scores": [np.asarray(item, dtype="float64") for item in scores],
    }


def score_ebm_table_probabilities(table: dict[str, Any], values: np.ndarray) -> np.ndarray:
    matrix = np.asarray(values, dtype="float64")
    if matrix.ndim != 2:
        raise ValueError("EBM score table values must be a 2D matrix.")
    cuts: Sequence[np.ndarray] = table["cuts"]
    scores: Sequence[np.ndarray] = table["scores"]
    if matrix.shape[1] != len(cuts):
        raise ValueError(f"Feature count mismatch: {matrix.shape[1]} != {len(cuts)}")
    logits = np.repeat(np.asarray(table["intercept"], dtype="float64").reshape(1, -1), matrix.shape[0], axis=0)
    for feature_index in range(matrix.shape[1]):
        bin_index = (matrix[:, feature_index].reshape(-1, 1) > cuts[feature_index].reshape(1, -1)).sum(axis=1) + 1
        logits += scores[feature_index][bin_index]
    logits -= logits.max(axis=1, keepdims=True)
    exp_logits = np.exp(logits)
    return exp_logits / exp_logits.sum(axis=1, keepdims=True)


def check_ebm_score_table_probability_parity(
    model: Any,
    table_path: Path,
    values: np.ndarray,
    *,
    feature_count: int,
    tolerance: float = 1.0e-10,
) -> dict[str, Any]:
    table = load_ebm_score_table(table_path, feature_count=feature_count)
    table_prob = score_ebm_table_probabilities(table, values)
    sklearn_prob = ordered_sklearn_probabilities(model, values)
    max_abs_diff = float(np.max(np.abs(sklearn_prob - table_prob))) if len(values) else 0.0
    return {
        "passed": bool(max_abs_diff <= float(tolerance)),
        "max_abs_diff": max_abs_diff,
        "tolerance": float(tolerance),
        "rows": int(len(values)),
        "table_path": table_path.as_posix(),
    }
