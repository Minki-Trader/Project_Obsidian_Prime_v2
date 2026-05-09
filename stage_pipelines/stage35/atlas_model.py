from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from foundation.control_plane.ledger import io_path
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage35 import atlas_config as cfg
from stage_pipelines.stage35 import common


LABEL_COLUMNS = {
    "timestamp",
    "symbol",
    "future_timestamp",
    "future_log_return_12",
    "label",
    "label_class",
    "label_id",
    "split",
    "split_id",
    "horizon_bars",
    "horizon_minutes",
}


def load_dataset() -> pd.DataFrame:
    cfg.validate_topic_layout()
    frame = pd.read_parquet(io_path(cfg.MODEL_INPUT_PATH)).sort_values("timestamp").reset_index(drop=True)
    missing = [name for name in cfg.FEATURE_ORDER if name not in frame.columns]
    if missing:
        raise RuntimeError(f"model input is missing feature columns: {missing}")
    if frame["timestamp"].duplicated().any():
        raise RuntimeError("model input contains duplicate timestamps")
    if ordered_hash(cfg.FEATURE_ORDER) != cfg.FEATURE_ORDER_HASH:
        raise RuntimeError("58-feature order hash mismatch")
    return frame


def _proxy_metrics(values: Sequence[float]) -> dict[str, Any]:
    values = [float(value) for value in values if np.isfinite(value)]
    return {
        "count": int(len(values)),
        "net_return_proxy": round(float(sum(values)), 10) if values else 0.0,
        "mean_return_proxy": round(float(np.mean(values)), 10) if values else 0.0,
        "profit_factor_proxy": None if not values else common.profit_factor(values),
    }


def _direction_for_train(state_frame: pd.DataFrame) -> str:
    returns = state_frame["future_log_return_12"].astype(float).to_numpy()
    long_net = float(np.nansum(returns))
    short_net = float(np.nansum(-returns))
    return "long" if long_net >= short_net else "short"


def _state_rows(topic_id: str, frame: pd.DataFrame, state_col: str, directions: Mapping[int, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split_name, split_frame in frame.groupby("split", dropna=False):
        total = len(split_frame)
        for state_id, state_frame in split_frame.groupby(state_col, dropna=False):
            state = int(state_id)
            direction = directions[state]
            sign = 1.0 if direction == "long" else -1.0
            proxy_returns = (state_frame["future_log_return_12"].astype(float) * sign).to_numpy()
            labels = state_frame["label"].astype(str).value_counts().to_dict()
            metrics = _proxy_metrics(proxy_returns)
            rows.append(
                {
                    "topic_id": topic_id,
                    "split": str(split_name),
                    "state_id": state,
                    "state_direction": direction,
                    "row_count": int(len(state_frame)),
                    "coverage": round(float(len(state_frame) / total), 6) if total else 0.0,
                    "label_short_count": int(labels.get("short", 0)),
                    "label_flat_count": int(labels.get("flat", 0)),
                    "label_long_count": int(labels.get("long", 0)),
                    **metrics,
                }
            )
    return rows


def fit_topic(frame: pd.DataFrame, topic: cfg.AtlasTopic) -> tuple[pd.Series, list[dict[str, Any]], dict[str, Any]]:
    state_col = f"state_{topic.topic_id}"
    train = frame.loc[frame["split"].eq("train"), list(topic.features)]
    scaler = StandardScaler()
    train_matrix = scaler.fit_transform(train.to_numpy(dtype="float64"))
    model = KMeans(n_clusters=cfg.KMEANS_CLUSTERS, n_init=20, random_state=cfg.RANDOM_STATE)
    model.fit(train_matrix)
    all_matrix = scaler.transform(frame.loc[:, list(topic.features)].to_numpy(dtype="float64"))
    states = pd.Series(model.predict(all_matrix), index=frame.index, name=state_col)
    work = frame.loc[:, ["timestamp", "split", "label", "future_log_return_12"]].copy()
    work[state_col] = states
    directions = {
        int(state): _direction_for_train(group)
        for state, group in work.loc[work["split"].eq("train")].groupby(state_col, dropna=False)
    }
    rows = _state_rows(topic.topic_id, work, state_col, directions)
    payload = {
        "topic": asdict(topic),
        "state_column": state_col,
        "cluster_count": cfg.KMEANS_CLUSTERS,
        "scaler_mean": [float(value) for value in scaler.mean_],
        "scaler_scale": [float(value) for value in scaler.scale_],
        "cluster_centers": model.cluster_centers_.tolist(),
        "train_directions": {str(key): value for key, value in directions.items()},
    }
    return states, rows, payload


def _pf_sort(value: Any) -> float:
    number = common.numeric(value, -999.0)
    return 999.0 if number >= 999.0 else number


def select_state(topic: cfg.AtlasTopic, rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    validation_rows = [row for row in rows if row["topic_id"] == topic.topic_id and row["split"] == "validation"]
    eligible = [row for row in validation_rows if int(row["row_count"]) >= cfg.MIN_VALIDATION_ROWS]
    pool = eligible or validation_rows
    selected = max(
        pool,
        key=lambda row: (
            _pf_sort(row.get("profit_factor_proxy")),
            common.numeric(row.get("net_return_proxy")),
            int(row.get("row_count") or 0),
        ),
    )
    return {
        "topic_id": topic.topic_id,
        "idea_id": topic.idea_id,
        "selected_state_id": int(selected["state_id"]),
        "state_direction": str(selected["state_direction"]),
        "validation_row_count": int(selected["row_count"]),
        "validation_net_return_proxy": selected.get("net_return_proxy"),
        "validation_profit_factor_proxy": selected.get("profit_factor_proxy"),
        "selection_rule": "highest_validation_proxy_pf_with_train_direction_and_min_rows",
        "tier_b_scope": topic.tier_b_scope,
    }


def build_atlas() -> dict[str, Any]:
    frame = load_dataset()
    assignment_frame = frame.loc[:, ["timestamp", "split", *cfg.FEATURE_ORDER, "label", "future_log_return_12"]].copy()
    all_rows: list[dict[str, Any]] = []
    model_payloads: list[dict[str, Any]] = []
    selections: list[dict[str, Any]] = []
    for topic in cfg.TOPICS:
        states, rows, payload = fit_topic(frame, topic)
        assignment_frame[f"state_{topic.topic_id}"] = states
        all_rows.extend(rows)
        model_payloads.append(payload)
        selections.append(select_state(topic, rows))
    data_identity = {
        "path": common.rel(cfg.MODEL_INPUT_PATH),
        "sha256": common.sha256_file(cfg.MODEL_INPUT_PATH),
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "feature_order_hash": ordered_hash(cfg.FEATURE_ORDER),
        "split_counts": frame["split"].value_counts().sort_index().to_dict(),
        "timestamp_min": frame["timestamp"].min().isoformat(),
        "timestamp_max": frame["timestamp"].max().isoformat(),
    }
    return {
        "frame": assignment_frame,
        "state_rows": all_rows,
        "model_payloads": model_payloads,
        "selections": selections,
        "data_identity": data_identity,
    }


def selected_frame(assignments: pd.DataFrame, selection: Mapping[str, Any], split_name: str) -> pd.DataFrame:
    topic_id = str(selection["topic_id"])
    state_col = f"state_{topic_id}"
    state_id = int(selection["selected_state_id"])
    return assignments.loc[
        assignments["split"].astype(str).eq(split_name) & assignments[state_col].astype(int).eq(state_id),
        ["timestamp", "split", *cfg.FEATURE_ORDER, state_col],
    ].copy()


def write_constant_score_table(path: Path, direction: str) -> dict[str, Any]:
    if direction not in {"long", "short"}:
        raise ValueError(f"unsupported direction: {direction}")
    intercept = {"short": (2.2, 0.0, 0.0), "long": (0.0, 0.0, 2.2)}[direction]
    rows = [{"record_type": "intercept", "feature_index": -1, "item_index": -1, "value": "", "score_short": intercept[0], "score_flat": intercept[1], "score_long": intercept[2]}]
    for feature_index in range(len(cfg.FEATURE_ORDER)):
        rows.append({"record_type": "score", "feature_index": feature_index, "item_index": 0, "value": "", "score_short": 0.0, "score_flat": 0.0, "score_long": 0.0})
        rows.append({"record_type": "score", "feature_index": feature_index, "item_index": 1, "value": "", "score_short": 0.0, "score_flat": 0.0, "score_long": 0.0})
    common.write_csv(path, rows, ("record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long"))
    return {"path": common.rel(path), "sha256": common.sha256_file(path), "direction": direction, "feature_count": len(cfg.FEATURE_ORDER), "backend": "ebm_table_constant"}

