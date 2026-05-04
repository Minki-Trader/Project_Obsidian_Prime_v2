from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from pygam import LogisticGAM

from foundation.control_plane.ledger import io_path
from foundation.models.baseline_training import LABEL_ORDER
from foundation.models.ebm_score_table import load_ebm_score_table, score_ebm_table_probabilities
from foundation.models.onnx_bridge import sha256_file


FIELDNAMES = ["record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long"]


def _format_float(value: Any) -> str:
    return f"{float(value):.17g}"


def _intercept(model: LogisticGAM) -> float:
    index = len(model.terms) - 1
    coef_indices = model.terms.get_coef_indices(index)
    if len(coef_indices) != 1:
        raise ValueError("GAM intercept term must have exactly one coefficient.")
    return float(model.coef_[coef_indices[0]])


def _finite_feature_values(frame: pd.DataFrame, feature: str) -> np.ndarray:
    values = frame[feature].to_numpy(dtype="float64", copy=False)
    return values[np.isfinite(values)]


def _feature_cuts(values: np.ndarray, *, bin_count: int) -> np.ndarray:
    if len(values) == 0:
        return np.asarray([], dtype="float64")
    requested = max(1, int(bin_count))
    raw = np.quantile(values, np.linspace(0.0, 1.0, requested + 1)[1:-1])
    return np.unique(np.asarray(raw, dtype="float64"))


def _feature_representatives(values: np.ndarray, *, cut_count: int) -> np.ndarray:
    bin_count = int(cut_count) + 1
    if len(values) == 0:
        return np.zeros(bin_count, dtype="float64")
    quantiles = (np.arange(bin_count, dtype="float64") + 0.5) / float(bin_count)
    return np.asarray(np.quantile(values, quantiles), dtype="float64")


def _term_partial(model: LogisticGAM, term_index: int, base_row: np.ndarray, reps: np.ndarray) -> np.ndarray:
    matrix = np.repeat(np.asarray(base_row, dtype="float64").reshape(1, -1), len(reps), axis=0)
    matrix[:, int(term_index)] = reps
    return np.asarray(model.partial_dependence(term=int(term_index), X=matrix), dtype="float64").reshape(-1)


def original_gam_probabilities(models: Mapping[str, LogisticGAM], values: np.ndarray) -> np.ndarray:
    matrix = np.asarray(values, dtype="float64")
    if matrix.ndim != 2:
        raise ValueError("GAM probability input must be a 2D matrix.")
    short_logit = np.asarray(models["short"]._linear_predictor(matrix), dtype="float64").reshape(-1)
    long_logit = np.asarray(models["long"]._linear_predictor(matrix), dtype="float64").reshape(-1)
    logits = np.stack([short_logit, np.zeros(len(matrix), dtype="float64"), long_logit], axis=1)
    logits -= logits.max(axis=1, keepdims=True)
    exp_logits = np.exp(logits)
    return exp_logits / exp_logits.sum(axis=1, keepdims=True)


def export_gam_piecewise_score_table(
    models: Mapping[str, LogisticGAM],
    output_path: Path,
    *,
    feature_names: Sequence[str],
    reference_frame: pd.DataFrame,
    bin_count: int = 128,
) -> dict[str, Any]:
    """Export a one-vs-rest GAM as an MQL5-compatible additive score table.

    The table is a piecewise approximation of each smooth term. It is a runtime
    probe handoff format, not a full GAM runtime-authority representation.
    """

    features = list(feature_names)
    missing = sorted(set(features).difference(reference_frame.columns))
    if missing:
        raise ValueError(f"Reference frame is missing GAM features: {missing}")
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    base_row = reference_frame.loc[:, features].median().to_numpy(dtype="float64")
    with io_path(output_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerow(
            {
                "record_type": "intercept",
                "feature_index": -1,
                "item_index": -1,
                "value": "",
                "score_short": _format_float(_intercept(models["short"])),
                "score_flat": _format_float(0.0),
                "score_long": _format_float(_intercept(models["long"])),
            }
        )
        for feature_index, feature in enumerate(features):
            values = _finite_feature_values(reference_frame, feature)
            cuts = _feature_cuts(values, bin_count=int(bin_count))
            reps = _feature_representatives(values, cut_count=len(cuts))
            short_scores = _term_partial(models["short"], feature_index, base_row, reps)
            long_scores = _term_partial(models["long"], feature_index, base_row, reps)
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
            for score_index in range(len(cuts) + 2):
                rep_index = max(0, score_index - 1)
                if rep_index >= len(reps):
                    rep_index = len(reps) - 1
                writer.writerow(
                    {
                        "record_type": "score",
                        "feature_index": feature_index,
                        "item_index": score_index,
                        "value": "",
                        "score_short": _format_float(short_scores[rep_index]),
                        "score_flat": _format_float(0.0),
                        "score_long": _format_float(long_scores[rep_index]),
                    }
                )
    return {
        "path": output_path.as_posix(),
        "sha256": sha256_file(output_path),
        "format": "gam_piecewise_score_table_csv_v1",
        "class_order": list(LABEL_ORDER),
        "feature_count": len(features),
        "feature_names": features,
        "bin_count_requested": int(bin_count),
        "runtime_policy": "mql5_direct_bin_lookup_additive_softmax_piecewise_gam_probe",
        "claim_boundary": "piecewise_runtime_probe_not_full_gam_runtime_authority",
    }


def check_gam_piecewise_score_table_parity(
    models: Mapping[str, LogisticGAM],
    table_path: Path,
    values: np.ndarray,
    *,
    feature_count: int,
    max_tolerance: float = 0.30,
    p95_tolerance: float = 0.04,
    mean_tolerance: float = 0.02,
) -> dict[str, Any]:
    table = load_ebm_score_table(table_path, feature_count=int(feature_count))
    table_prob = score_ebm_table_probabilities(table, values)
    expected_prob = original_gam_probabilities(models, values)
    abs_diff = np.abs(expected_prob - table_prob)
    max_abs_diff = float(np.max(abs_diff)) if len(values) else 0.0
    p95_abs_diff = float(np.quantile(abs_diff, 0.95)) if len(values) else 0.0
    mean_abs_diff = float(np.mean(abs_diff)) if len(values) else 0.0
    passed = (
        max_abs_diff <= float(max_tolerance)
        and p95_abs_diff <= float(p95_tolerance)
        and mean_abs_diff <= float(mean_tolerance)
    )
    return {
        "passed": bool(passed),
        "approximation_policy": "piecewise_gam_score_table_probe",
        "max_abs_diff": max_abs_diff,
        "p95_abs_diff": p95_abs_diff,
        "mean_abs_diff": mean_abs_diff,
        "max_tolerance": float(max_tolerance),
        "p95_tolerance": float(p95_tolerance),
        "mean_tolerance": float(mean_tolerance),
        "rows": int(len(values)),
        "table_path": table_path.as_posix(),
        "claim_boundary": "approximation_check_not_full_runtime_parity",
    }
