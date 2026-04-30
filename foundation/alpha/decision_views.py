from __future__ import annotations

import itertools
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.control_plane.ledger import io_path
from foundation.control_plane.tier_context import subtype_counts as _subtype_counts
from foundation.models.baseline_training import LABEL_ORDER
from foundation.models.decision_surface import (
    DECISION_CLASS_NO_TRADE,
    DECISION_LABEL_NO_TRADE,
    PROBABILITY_COLUMNS,
    ThresholdRule,
    apply_threshold_rule,
    probability_matrix,
    threshold_rule_from_values,
    threshold_rule_payload,
    validate_threshold_rule,
)
from foundation.models.onnx_bridge import ordered_sklearn_probabilities, sha256_file


TIER_COLUMN = "tier_label"
TIER_A = "Tier A"
TIER_B = "Tier B"
TIER_AB = "Tier A+B"
REQUIRED_TIER_VIEWS = (
    ("tier_a_separate", TIER_A),
    ("tier_b_separate", TIER_B),
    ("tier_ab_combined", TIER_AB),
)


def threshold_id(short_threshold: float, long_threshold: float, min_margin: float) -> str:
    return f"short{short_threshold:.3f}_long{long_threshold:.3f}_margin{min_margin:.3f}"


def sweep_threshold_rules(
    probabilities: pd.DataFrame | np.ndarray,
    y_true: Sequence[int] | np.ndarray | pd.Series | None = None,
    *,
    short_thresholds: Sequence[float] = (0.40, 0.45, 0.50, 0.55, 0.60),
    long_thresholds: Sequence[float] | None = None,
    min_margins: Sequence[float] = (0.00, 0.025, 0.05, 0.075, 0.10),
) -> pd.DataFrame:
    if long_thresholds is None:
        long_thresholds = short_thresholds
    matrix = probability_matrix(probabilities)
    true_values = None if y_true is None else np.asarray(y_true, dtype="int64")
    if true_values is not None and true_values.shape[0] != matrix.shape[0]:
        raise ValueError("y_true length must match probability row count.")

    rows: list[dict[str, Any]] = []
    for short_threshold, long_threshold, min_margin in itertools.product(
        short_thresholds, long_thresholds, min_margins
    ):
        rule = ThresholdRule(
            threshold_id=threshold_id(short_threshold, long_threshold, min_margin),
            short_threshold=float(short_threshold),
            long_threshold=float(long_threshold),
            min_margin=float(min_margin),
        )
        decisions = apply_threshold_rule(matrix, rule)
        decision_classes = decisions["decision_label_class"].to_numpy(dtype="int64", copy=False)
        signal_mask = decision_classes != DECISION_CLASS_NO_TRADE
        signal_count = int(signal_mask.sum())
        short_count = int((decision_classes == 0).sum())
        long_count = int((decision_classes == 2).sum())
        row: dict[str, Any] = {
            "threshold_id": rule.threshold_id,
            "short_threshold": rule.short_threshold,
            "long_threshold": rule.long_threshold,
            "min_margin": rule.min_margin,
            "rows": int(len(decisions)),
            "signal_count": signal_count,
            "short_count": short_count,
            "long_count": long_count,
            "coverage": float(signal_count / len(decisions)) if len(decisions) else 0.0,
            "no_trade_rate": float(1.0 - signal_count / len(decisions)) if len(decisions) else 1.0,
            "long_share_of_signals": float(long_count / signal_count) if signal_count else np.nan,
        }
        if true_values is not None:
            correct = decision_classes[signal_mask] == true_values[signal_mask]
            row["directional_hit_rate"] = float(correct.mean()) if signal_count else np.nan
            row["directional_correct_count"] = int(correct.sum()) if signal_count else 0
        rows.append(row)
    return pd.DataFrame(rows)


def select_threshold_from_sweep(
    sweep: pd.DataFrame,
    *,
    primary_metric: str = "directional_hit_rate",
    min_coverage: float = 0.01,
) -> dict[str, Any]:
    if sweep.empty:
        raise ValueError("Threshold sweep is empty.")
    if primary_metric not in sweep.columns:
        primary_metric = "coverage"
    candidates = sweep.loc[sweep["coverage"].fillna(0.0) >= min_coverage].copy()
    if candidates.empty:
        candidates = sweep.copy()
    candidates[primary_metric] = candidates[primary_metric].fillna(-np.inf)
    candidates = candidates.sort_values(
        [primary_metric, "coverage", "signal_count", "threshold_id"],
        ascending=[False, False, False, True],
    )
    return candidates.iloc[0].to_dict()


def build_prediction_frame(
    model: Any,
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    rule: ThresholdRule,
    *,
    tier_column: str = TIER_COLUMN,
) -> pd.DataFrame:
    values = frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
    probabilities = ordered_sklearn_probabilities(model, values, class_order=LABEL_ORDER)
    decisions = apply_threshold_rule(probabilities, rule)
    identity_columns = [
        name
        for name in (
            "timestamp",
            "symbol",
            "split",
            "label",
            "label_class",
            "route_role",
            "partial_context_subtype",
            "missing_feature_group_mask",
            "available_feature_group_mask",
            "tier_a_primary_available",
            "tier_a_full_feature_ready",
            "tier_b_core_ready",
            "context_reject_reason",
        )
        if name in frame.columns
    ]
    result = frame.loc[:, identity_columns].reset_index(drop=True).copy()
    if tier_column in frame.columns:
        result[tier_column] = frame[tier_column].to_numpy()
    return pd.concat([result, decisions], axis=1)


def normalize_tier_label(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    text = str(value).strip().lower().replace("_", " ")
    if text in {"tier a", "a"}:
        return TIER_A
    if text in {"tier b", "b"}:
        return TIER_B
    if text in {"tier a+b", "tier ab", "a+b", "ab", "combined"}:
        return TIER_AB
    return None


def build_tier_prediction_views(
    predictions: pd.DataFrame,
    *,
    tier_column: str = TIER_COLUMN,
) -> dict[str, pd.DataFrame]:
    empty = predictions.iloc[0:0].copy()
    if tier_column not in predictions.columns:
        return {view: empty.copy() for view, _scope in REQUIRED_TIER_VIEWS}

    normalized = predictions[tier_column].map(normalize_tier_label)
    tier_a = predictions.loc[normalized.eq(TIER_A)].copy()
    tier_b = predictions.loc[normalized.eq(TIER_B)].copy()
    combined = pd.concat([tier_a, tier_b], ignore_index=True)
    return {
        "tier_a_separate": tier_a.reset_index(drop=True),
        "tier_b_separate": tier_b.reset_index(drop=True),
        "tier_ab_combined": combined.reset_index(drop=True),
    }


def prediction_view_metrics(view: pd.DataFrame) -> dict[str, Any]:
    rows = int(len(view))
    payload: dict[str, Any] = {
        "rows": rows,
        "signal_count": 0,
        "short_count": 0,
        "long_count": 0,
        "no_trade_count": 0,
        "signal_coverage": 0.0,
        "probability_row_sum_max_abs_error": None,
    }
    if rows == 0:
        return payload

    if "decision_label" in view.columns:
        decision_labels = view["decision_label"].astype(str)
        payload["short_count"] = int(decision_labels.eq("short").sum())
        payload["long_count"] = int(decision_labels.eq("long").sum())
        payload["no_trade_count"] = int(decision_labels.eq(DECISION_LABEL_NO_TRADE).sum())
        payload["signal_count"] = int(payload["short_count"] + payload["long_count"])
        payload["signal_coverage"] = float(payload["signal_count"] / rows)
    if "threshold_id" in view.columns:
        payload["threshold_ids"] = sorted(str(value) for value in view["threshold_id"].dropna().unique())

    if all(name in view.columns for name in PROBABILITY_COLUMNS):
        matrix = probability_matrix(view.loc[:, PROBABILITY_COLUMNS])
        payload["probability_row_sum_max_abs_error"] = float(np.abs(matrix.sum(axis=1) - 1.0).max())
        payload["mean_probability"] = {
            name: float(matrix[:, index].mean()) for index, name in enumerate(PROBABILITY_COLUMNS)
        }
    if "partial_context_subtype" in view.columns:
        payload["partial_context_subtype_counts"] = _subtype_counts(view)
        if "decision_label" in view.columns:
            signal_view = view.loc[view["decision_label"].astype(str).ne(DECISION_LABEL_NO_TRADE)]
            payload["partial_context_subtype_signal_counts"] = _subtype_counts(signal_view)
    return payload


def build_paired_tier_records(
    tier_views: Mapping[str, pd.DataFrame],
    *,
    run_id: str,
    stage_id: str,
    base_path: str | Path | None = None,
    kpi_scope: str = "signal_probability_threshold",
    scoreboard_lane: str = "structural_scout",
    external_verification_status: str = "out_of_scope_by_claim",
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    base = None if base_path is None else Path(base_path)
    for record_view, tier_scope in REQUIRED_TIER_VIEWS:
        view = tier_views.get(record_view)
        metrics = prediction_view_metrics(view if view is not None else pd.DataFrame())
        status = "completed_payload" if metrics["rows"] > 0 else "missing_required"
        judgment = "inconclusive_payload_only" if metrics["rows"] > 0 else "inconclusive_tier_pair_incomplete"
        record_path = "" if base is None else (base / f"{record_view}_predictions.parquet").as_posix()
        records.append(
            {
                "ledger_row_id": f"{run_id}__{record_view}",
                "stage_id": stage_id,
                "run_id": run_id,
                "subrun_id": record_view,
                "parent_run_id": run_id,
                "record_view": record_view,
                "tier_scope": tier_scope,
                "kpi_scope": kpi_scope,
                "scoreboard_lane": scoreboard_lane,
                "status": status,
                "judgment": judgment,
                "path": record_path,
                "primary_kpi": {"signal_coverage": metrics["signal_coverage"]},
                "guardrail_kpi": {
                    "probability_row_sum_max_abs_error": metrics["probability_row_sum_max_abs_error"],
                },
                "external_verification_status": external_verification_status,
                "notes": "Tier labels are sample labels, not exploration gates.",
                "metrics": metrics,
            }
        )
    return records


def materialize_tier_prediction_views(
    tier_views: Mapping[str, pd.DataFrame],
    output_root: Path,
) -> dict[str, dict[str, Any]]:
    io_path(output_root).mkdir(parents=True, exist_ok=True)
    payload: dict[str, dict[str, Any]] = {}
    for record_view, view in tier_views.items():
        if view.empty:
            payload[record_view] = {"status": "missing_required", "rows": 0, "path": None, "sha256": None}
            continue
        path = output_root / f"{record_view}_predictions.parquet"
        view.to_parquet(io_path(path), index=False)
        payload[record_view] = {
            "status": "completed_payload",
            "rows": int(len(view)),
            "path": path.as_posix(),
            "sha256": sha256_file(path),
        }
    return payload

