from __future__ import annotations

from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from foundation.models.baseline_training import validate_model_input_frame


SCALAR_METRICS = (
    "unit_count",
    "rows",
    "zero_rate_mean",
    "zero_rate_max",
    "dead_unit_count",
    "near_dead_unit_count",
    "active_units_row_mean",
    "activation_l2_row_mean",
    "high_activation_rate_mean",
    "pre_activation_abs_p95",
)


def _hidden_activation(name: str, values: np.ndarray) -> np.ndarray:
    if name == "relu":
        return np.maximum(values, 0.0)
    if name == "tanh":
        return np.tanh(values)
    if name == "logistic":
        return 1.0 / (1.0 + np.exp(-values))
    if name == "identity":
        return values
    raise ValueError(f"Unsupported MLP activation: {name}")


def hidden_layer_values(model: Pipeline, values: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
    scaler = model.named_steps["scaler"]
    classifier = model.named_steps["classifier"]
    layer_input = scaler.transform(values)
    activation_name = str(classifier.activation)
    layers: list[tuple[np.ndarray, np.ndarray]] = []
    for weights, bias in zip(classifier.coefs_[:-1], classifier.intercepts_[:-1], strict=True):
        pre_activation = layer_input @ weights + bias
        activation = _hidden_activation(activation_name, pre_activation)
        layers.append((pre_activation, activation))
        layer_input = activation
    return layers


def _split_arrays(
    model: Pipeline,
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    split_name: str,
) -> list[tuple[np.ndarray, np.ndarray]]:
    split = frame.loc[frame["split"].astype(str).eq(split_name)]
    values = split.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
    return hidden_layer_values(model, values)


def _train_high_thresholds(
    model: Pipeline,
    frame: pd.DataFrame,
    feature_order: Sequence[str],
) -> list[np.ndarray]:
    train_layers = _split_arrays(model, frame, feature_order, "train")
    thresholds: list[np.ndarray] = []
    for _pre, activation in train_layers:
        if len(activation):
            thresholds.append(np.quantile(activation, 0.95, axis=0))
        else:
            thresholds.append(np.asarray([], dtype="float64"))
    return thresholds


def _safe_mean(values: np.ndarray) -> float | None:
    return float(values.mean()) if values.size else None


def _safe_max(values: np.ndarray) -> float | None:
    return float(values.max()) if values.size else None


def _summarize_layer(
    *,
    scope: str,
    split_name: str,
    layer_index: int,
    pre_activation: np.ndarray,
    activation: np.ndarray,
    high_threshold: np.ndarray,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows = int(activation.shape[0])
    unit_count = int(activation.shape[1]) if activation.ndim == 2 else 0
    if rows == 0 or unit_count == 0:
        return (
            {
                "scope": scope,
                "split": split_name,
                "layer_index": layer_index,
                "rows": rows,
                "unit_count": unit_count,
                "finite": True,
            },
            [],
        )
    zero = np.isclose(activation, 0.0, atol=1e-12)
    zero_rate = zero.mean(axis=0)
    high_rate = (activation >= high_threshold.reshape(1, -1)).mean(axis=0) if high_threshold.size else np.zeros(unit_count)
    active_units = (~zero).sum(axis=1)
    l2 = np.linalg.norm(activation, axis=1) / max(unit_count**0.5, 1.0)
    pre_abs = np.abs(pre_activation)
    unit_rows = []
    for index in range(unit_count):
        unit_rows.append(
            {
                "scope": scope,
                "split": split_name,
                "layer_index": layer_index,
                "unit_index": index,
                "activation_mean": float(activation[:, index].mean()),
                "activation_std": float(activation[:, index].std()),
                "zero_rate": float(zero_rate[index]),
                "high_activation_rate": float(high_rate[index]),
                "pre_activation_mean": float(pre_activation[:, index].mean()),
                "pre_activation_std": float(pre_activation[:, index].std()),
            }
        )
    summary = {
        "scope": scope,
        "split": split_name,
        "layer_index": layer_index,
        "rows": rows,
        "unit_count": unit_count,
        "finite": bool(np.isfinite(activation).all() and np.isfinite(pre_activation).all()),
        "zero_rate_mean": float(zero_rate.mean()),
        "zero_rate_max": float(zero_rate.max()),
        "dead_unit_count": int((zero_rate >= 0.99).sum()),
        "near_dead_unit_count": int((zero_rate >= 0.95).sum()),
        "active_units_row_mean": float(active_units.mean()),
        "activation_l2_row_mean": float(l2.mean()),
        "high_activation_rate_mean": float(high_rate.mean()),
        "pre_activation_abs_p95": float(np.quantile(pre_abs, 0.95)),
    }
    return summary, unit_rows


def activation_summary(
    *,
    model: Pipeline,
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    scope: str,
) -> dict[str, Any]:
    feature_names = list(feature_order)
    validate_model_input_frame(frame, feature_names)
    high_thresholds = _train_high_thresholds(model, frame, feature_names)
    summaries: list[dict[str, Any]] = []
    unit_rows: list[dict[str, Any]] = []
    for split_name in ("train", "validation", "oos"):
        layers = _split_arrays(model, frame, feature_names, split_name)
        for layer_offset, (pre_activation, activation) in enumerate(layers, start=1):
            summary, rows = _summarize_layer(
                scope=scope,
                split_name=split_name,
                layer_index=layer_offset,
                pre_activation=pre_activation,
                activation=activation,
                high_threshold=high_thresholds[layer_offset - 1],
            )
            summaries.append(summary)
            unit_rows.extend(rows)
    summary_frame = pd.DataFrame(summaries)
    unit_frame = pd.DataFrame(unit_rows)
    return {
        "summary": summary_frame,
        "unit_stats": unit_frame,
        "payload": {
            "scope": scope,
            "layers": summary_frame.to_dict(orient="records"),
            "dead_unit_threshold_zero_rate": 0.99,
            "near_dead_unit_threshold_zero_rate": 0.95,
            "high_activation_reference": "train_split_unit_p95",
        },
    }


def activation_drift(summary_frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    keys = ["scope", "layer_index"]
    train_lookup = {
        (str(row["scope"]), int(row["layer_index"])): row
        for row in summary_frame.loc[summary_frame["split"].astype(str).eq("train")].to_dict(orient="records")
    }
    for row in summary_frame.loc[~summary_frame["split"].astype(str).eq("train")].to_dict(orient="records"):
        key = (str(row["scope"]), int(row["layer_index"]))
        train = train_lookup.get(key)
        if not train:
            continue
        payload = {field: row[field] for field in (*keys, "split") if field in row}
        for metric in SCALAR_METRICS:
            if metric in row and metric in train and row[metric] is not None and train[metric] is not None:
                payload[f"{metric}_delta_vs_train"] = float(row[metric]) - float(train[metric])
        rows.append(payload)
    return pd.DataFrame(rows)


def activation_scope_gap(tier_a_summary: pd.DataFrame, tier_b_summary: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    a_rows = {
        (str(row["split"]), int(row["layer_index"])): row
        for row in tier_a_summary.to_dict(orient="records")
    }
    for b_row in tier_b_summary.to_dict(orient="records"):
        key = (str(b_row["split"]), int(b_row["layer_index"]))
        a_row = a_rows.get(key)
        if not a_row:
            continue
        payload: dict[str, Any] = {"split": key[0], "layer_index": key[1]}
        for metric in SCALAR_METRICS:
            if metric in a_row and metric in b_row and a_row[metric] is not None and b_row[metric] is not None:
                payload[f"{metric}_tier_b_minus_tier_a"] = float(b_row[metric]) - float(a_row[metric])
        rows.append(payload)
    return pd.DataFrame(rows)
