from __future__ import annotations

import argparse
import csv
import importlib.metadata
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import balanced_accuracy_score, mean_absolute_error, mean_pinball_loss

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.models.baseline_training import validate_model_input_frame
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5
from foundation.models import alpha_scout_support as stage26_scout


STAGE_ID = "27_tail_model__quantile_boosting_risk_surface"
RUN_ID = "run21A_quantile_boosting_tail_risk_surface_scout_v1"
RUN_NUMBER = "run21A"
PACKET_ID = "stage27_run21A_quantile_boosting_tail_risk_scout_v1"
NEXT_RUN_ID = "run21B_quantile_boosting_tail_risk_runtime_probe_v1"
EXPLORATION_LABEL = "stage27_TailModel__QuantileBoostingRiskSurface"
MODEL_FAMILY = "sklearn_gradient_boosting_quantile_regression"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_quantile_tail_risk_surface"
LABEL_ID = stage26_scout.LABEL_ID
SPLIT_CONTRACT = stage26_scout.SPLIT_CONTRACT
TARGET_COLUMN = "future_log_return_12"
QUANTILES = (0.10, 0.50, 0.90)
STRENGTH_QUANTILE = 0.80
TAIL_PRESSURE_QUANTILE = 0.70
BOUNDARY = "quantile_boosting_tail_risk_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_quantile_boosting_tail_risk_surface_scout_completed"

ROOT = stage26_scout.ROOT
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REPORT_PATH = STAGE_ROOT / "03_reviews/run21A_quantile_boosting_tail_risk_scout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage27_run21A_quantile_boosting_tail_risk_scout.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = stage26_scout.WORKSPACE_STATE_PATH
CURRENT_WORKING_STATE_PATH = stage26_scout.CURRENT_WORKING_STATE_PATH
GOAL_PLAN_PATH = stage26_scout.GOAL_PLAN_PATH


@dataclass(frozen=True)
class QuantileBoostingVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    feature_names: tuple[str, ...]
    n_estimators: int
    learning_rate: float
    max_depth: int
    min_samples_leaf: int
    subsample: float
    max_features: float | None
    tier_b_compatible: bool = True
    random_state: int = 2701
    max_train_rows: int = 32000

    def payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["feature_names"] = list(self.feature_names)
        payload["quantiles"] = list(QUANTILES)
        return payload


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return stage26_scout.rel(path)


def write_json(path: Path, payload: Any) -> None:
    stage26_scout.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    stage26_scout.write_md(path, text)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    return stage26_scout.save_frame(path, frame)


def safe_float(value: Any, default: float = 0.0) -> float:
    return stage26_scout.safe_float(value, default)


def sklearn_version() -> str:
    return importlib.metadata.version("scikit-learn")


def load_context() -> dict[str, Any]:
    return stage26_scout.load_context()


def default_variants(full_feature_order: Sequence[str], tier_b_feature_order: Sequence[str]) -> list[QuantileBoostingVariantSpec]:
    tier_b_set = set(tier_b_feature_order)
    core24 = tuple(name for name in stage26_scout.core24_features() if name in tier_b_set)
    core42 = tuple(tier_b_feature_order)
    vol_session = tuple(name for name in stage26_scout.volatility_session_features() if name in tier_b_set)
    tail_axis = tuple(
        name
        for name in (
            "log_return_1",
            "log_return_3",
            "hl_range",
            "gap_percent",
            "return_zscore_20",
            "hl_zscore_50",
            "overnight_return",
            "return_1_over_atr_14",
            "historical_vol_20",
            "historical_vol_60",
            "atr_14",
            "rsi_14",
            "trend_strength_20",
            "bb_width_20",
            "volume_zscore_20",
            "hour_sin",
            "hour_cos",
            "minutes_from_cash_open",
        )
        if name in tier_b_set
    )
    full58 = tuple(full_feature_order)
    return [
        QuantileBoostingVariantSpec(
            variant_id="v01_core24_compact_tail_surface",
            idea_id="compact_quantile_tail_shape",
            description="Core24 quantile boosting to test whether compact features expose q10/q50/q90 tail spread.",
            feature_names=core24,
            n_estimators=70,
            learning_rate=0.045,
            max_depth=2,
            min_samples_leaf=160,
            subsample=0.76,
            max_features=0.90,
            random_state=2701,
        ),
        QuantileBoostingVariantSpec(
            variant_id="v02_core42_tail_risk_surface",
            idea_id="tier_b_compatible_tail_risk_surface",
            description="Tier-B-compatible core42 quantile boosting surface for downside/upside tail asymmetry.",
            feature_names=core42,
            n_estimators=80,
            learning_rate=0.040,
            max_depth=2,
            min_samples_leaf=180,
            subsample=0.72,
            max_features=0.82,
            random_state=2702,
        ),
        QuantileBoostingVariantSpec(
            variant_id="v03_core24_slow_tail_control",
            idea_id="slow_quantile_tail_control",
            description="Slower core24 control for quantile crossing and tail spread stability.",
            feature_names=core24,
            n_estimators=95,
            learning_rate=0.030,
            max_depth=2,
            min_samples_leaf=170,
            subsample=0.78,
            max_features=0.90,
            random_state=2703,
        ),
        QuantileBoostingVariantSpec(
            variant_id="v04_vol_session_tail_axis",
            idea_id="volatility_session_tail_axis",
            description="Volatility/session feature surface to test whether tail risk is mostly market-context shaped.",
            feature_names=vol_session or tail_axis,
            n_estimators=80,
            learning_rate=0.040,
            max_depth=2,
            min_samples_leaf=150,
            subsample=0.80,
            max_features=1.0,
            random_state=2704,
        ),
        QuantileBoostingVariantSpec(
            variant_id="v05_full58_tier_a_tail_context_contrast",
            idea_id="full_context_tail_contrast",
            description="Tier-A-only full58 contrast, kept out of runtime handoff selection if Tier B cannot mirror it.",
            feature_names=full58,
            n_estimators=75,
            learning_rate=0.038,
            max_depth=2,
            min_samples_leaf=190,
            subsample=0.72,
            max_features=0.78,
            tier_b_compatible=False,
            random_state=2705,
        ),
    ]


def regression_train_sample(train: pd.DataFrame, max_rows: int, seed: int) -> pd.DataFrame:
    if len(train) <= max_rows:
        return train.sort_values("timestamp").copy()
    sample = train.sample(n=max_rows, random_state=seed)
    return sample.sort_values("timestamp").copy()


def build_regressor(spec: QuantileBoostingVariantSpec, quantile: float) -> GradientBoostingRegressor:
    return GradientBoostingRegressor(
        loss="quantile",
        alpha=float(quantile),
        learning_rate=float(spec.learning_rate),
        n_estimators=int(spec.n_estimators),
        subsample=float(spec.subsample),
        max_depth=int(spec.max_depth),
        min_samples_leaf=int(spec.min_samples_leaf),
        max_features=spec.max_features,
        random_state=int(spec.random_state + round(quantile * 1000)),
    )


def fit_quantile_variant(frame: pd.DataFrame, spec: QuantileBoostingVariantSpec) -> tuple[dict[float, GradientBoostingRegressor], dict[str, Any]]:
    features = list(spec.feature_names)
    validate_model_input_frame(frame, features)
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    train = train.loc[np.isfinite(train[TARGET_COLUMN].astype("float64"))].copy()
    train = regression_train_sample(train, spec.max_train_rows, spec.random_state)
    values = train.loc[:, features].to_numpy(dtype="float64", copy=False)
    target = train[TARGET_COLUMN].astype("float64").to_numpy(copy=False)
    models: dict[float, GradientBoostingRegressor] = {}
    for quantile in QUANTILES:
        model = build_regressor(spec, quantile)
        model.fit(values, target)
        models[float(quantile)] = model
    return models, {
        "train_rows": int(len(train)),
        "feature_count": int(len(features)),
        "target_mean": float(np.mean(target)),
        "target_std": float(np.std(target)),
        "target_q10": float(np.quantile(target, 0.10)),
        "target_q50": float(np.quantile(target, 0.50)),
        "target_q90": float(np.quantile(target, 0.90)),
        "max_train_rows": int(spec.max_train_rows),
    }


def raw_quantile_predictions(models: Mapping[float, GradientBoostingRegressor], values: np.ndarray) -> np.ndarray:
    return np.column_stack([np.asarray(models[quantile].predict(values), dtype="float64") for quantile in QUANTILES])


def build_thresholds(pred: pd.DataFrame) -> dict[str, float]:
    train = pred.loc[pred["split"].astype(str).eq("train")]
    if train.empty:
        return {"direction_strength": 0.0, "tail_pressure": 0.0}
    return {
        "direction_strength": float(train["direction_strength"].astype("float64").quantile(STRENGTH_QUANTILE)),
        "tail_pressure": float(train["tail_pressure"].astype("float64").quantile(TAIL_PRESSURE_QUANTILE)),
    }


def apply_decision(pred: pd.DataFrame, thresholds: Mapping[str, float]) -> pd.DataFrame:
    frame = pred.copy()
    direction_cut = float(thresholds.get("direction_strength", 0.0))
    tail_cut = float(thresholds.get("tail_pressure", 0.0))
    strong = (frame["direction_strength"] >= direction_cut) & (frame["tail_pressure"] >= tail_cut)
    frame["decision_label"] = 1
    frame.loc[strong & (frame["q50"] < 0.0), "decision_label"] = 0
    frame.loc[strong & (frame["q50"] > 0.0), "decision_label"] = 2
    frame["decision_name"] = np.select(
        [frame["decision_label"].eq(0), frame["decision_label"].eq(2)],
        ["short", "long"],
        default="flat",
    )
    return frame


def prediction_frame(
    models: Mapping[float, GradientBoostingRegressor],
    frame: pd.DataFrame,
    feature_names: Sequence[str],
    thresholds: Mapping[str, float] | None = None,
) -> tuple[pd.DataFrame, dict[str, float]]:
    features = list(feature_names)
    values = frame.loc[:, features].to_numpy(dtype="float64", copy=False)
    raw = raw_quantile_predictions(models, values)
    crossing = (raw[:, 0] > raw[:, 1]) | (raw[:, 1] > raw[:, 2])
    ordered = np.sort(raw, axis=1)
    eps = 1e-9
    spread = ordered[:, 2] - ordered[:, 0]
    downside = np.maximum(0.0, -ordered[:, 0])
    upside = np.maximum(0.0, ordered[:, 2])
    tail_pressure = np.maximum(downside, upside)
    direction_strength = np.abs(ordered[:, 1]) / (spread + eps)
    payload = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(frame["timestamp"], utc=True).to_numpy(),
            "split": frame["split"].astype(str).to_numpy(),
            "label_class": frame["label_class"].astype("int64").to_numpy(),
            "target_return": frame[TARGET_COLUMN].astype("float64").to_numpy(),
            "q10_raw": raw[:, 0],
            "q50_raw": raw[:, 1],
            "q90_raw": raw[:, 2],
            "q10": ordered[:, 0],
            "q50": ordered[:, 1],
            "q90": ordered[:, 2],
            "quantile_crossed": crossing.astype("int64"),
            "tail_spread": spread,
            "downside_tail_pressure": downside,
            "upside_tail_pressure": upside,
            "tail_pressure": tail_pressure,
            "tail_asymmetry": upside - downside,
            "direction_strength": direction_strength,
            "risk_adjusted_direction": ordered[:, 1] / (spread + eps),
        }
    )
    if "partial_context_subtype" in frame.columns:
        payload["partial_context_subtype"] = frame["partial_context_subtype"].astype(str).to_numpy()
    selected_thresholds = dict(thresholds) if thresholds is not None else build_thresholds(payload)
    payload = apply_decision(payload, selected_thresholds)
    return payload, selected_thresholds


def split_tail_metrics(pred: pd.DataFrame) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        part = pred.loc[pred["split"].astype(str).eq(split)].copy()
        if part.empty:
            payload[split] = {"rows": 0}
            continue
        y = part["target_return"].astype("float64").to_numpy()
        decision = part["decision_label"].astype("int64").to_numpy()
        labels = part["label_class"].astype("int64").to_numpy()
        pinball = {
            "q10": float(mean_pinball_loss(y, part["q10"].to_numpy(), alpha=0.10)),
            "q50": float(mean_pinball_loss(y, part["q50"].to_numpy(), alpha=0.50)),
            "q90": float(mean_pinball_loss(y, part["q90"].to_numpy(), alpha=0.90)),
        }
        signal = part.loc[part["decision_label"].ne(1)]
        payload[split] = {
            "rows": int(len(part)),
            "pinball_q10": pinball["q10"],
            "pinball_q50": pinball["q50"],
            "pinball_q90": pinball["q90"],
            "pinball_mean": float(np.mean(list(pinball.values()))),
            "median_mae": float(mean_absolute_error(y, part["q50"].to_numpy())),
            "coverage_q10": float(np.mean(y <= part["q10"].to_numpy())),
            "coverage_q90": float(np.mean(y <= part["q90"].to_numpy())),
            "interval_coverage_q10_q90": float(np.mean((y >= part["q10"].to_numpy()) & (y <= part["q90"].to_numpy()))),
            "balanced_accuracy": float(balanced_accuracy_score(labels, decision)),
            "signal_count": int(len(signal)),
            "signal_coverage": float(len(signal) / max(1, len(part))),
            "short_count": int(part["decision_label"].eq(0).sum()),
            "long_count": int(part["decision_label"].eq(2).sum()),
            "flat_count": int(part["decision_label"].eq(1).sum()),
            "tail_spread_mean": float(part["tail_spread"].mean()),
            "tail_spread_p90": float(part["tail_spread"].quantile(0.90)),
            "tail_pressure_mean": float(part["tail_pressure"].mean()),
            "downside_tail_pressure_mean": float(part["downside_tail_pressure"].mean()),
            "upside_tail_pressure_mean": float(part["upside_tail_pressure"].mean()),
            "tail_asymmetry_mean": float(part["tail_asymmetry"].mean()),
            "tail_asymmetry_abs_mean": float(part["tail_asymmetry"].abs().mean()),
            "direction_strength_mean": float(part["direction_strength"].mean()),
            "quantile_crossing_rate": float(part["quantile_crossed"].mean()),
        }
    return payload


def tail_surface_read(pred: pd.DataFrame) -> dict[str, Any]:
    metrics = split_tail_metrics(pred)
    subtype_counts: dict[str, int] = {}
    if "partial_context_subtype" in pred.columns:
        subtype_counts = {
            str(key): int(value)
            for key, value in pred["partial_context_subtype"].astype(str).value_counts().sort_index().items()
        }
    return {"split_metrics": metrics, "partial_context_subtype_counts": subtype_counts or None}


def characteristic_score(metrics: Mapping[str, Any]) -> float:
    val = metrics.get("validation", {})
    oos = metrics.get("oos", {})
    val_pinball = safe_float(val.get("pinball_mean"))
    oos_pinball = safe_float(oos.get("pinball_mean"))
    coverage_error = (
        abs(safe_float(val.get("coverage_q10")) - 0.10)
        + abs(safe_float(val.get("coverage_q90")) - 0.90)
        + abs(safe_float(val.get("interval_coverage_q10_q90")) - 0.80)
    )
    oos_coverage_error = (
        abs(safe_float(oos.get("coverage_q10")) - 0.10)
        + abs(safe_float(oos.get("coverage_q90")) - 0.90)
        + abs(safe_float(oos.get("interval_coverage_q10_q90")) - 0.80)
    )
    signal_balance = min(safe_float(val.get("signal_coverage")), 0.30)
    asymmetry = safe_float(val.get("tail_asymmetry_abs_mean")) / max(1e-9, safe_float(val.get("tail_spread_mean"), 1e-9))
    crossing_penalty = safe_float(val.get("quantile_crossing_rate")) + 0.5 * safe_float(oos.get("quantile_crossing_rate"))
    return float(
        safe_float(val.get("balanced_accuracy"))
        + 0.45 * safe_float(oos.get("balanced_accuracy"))
        + 0.18 * signal_balance
        + 0.12 * asymmetry
        - 180.0 * val_pinball
        - 90.0 * oos_pinball
        - 0.8 * coverage_error
        - 0.4 * oos_coverage_error
        - 0.25 * crossing_penalty
    )


def evaluate_variant(context: Mapping[str, Any], spec: QuantileBoostingVariantSpec) -> dict[str, Any]:
    models, sample = fit_quantile_variant(context["tier_a_frame"], spec)
    pred, thresholds = prediction_frame(models, context["tier_a_frame"], spec.feature_names)
    metrics = split_tail_metrics(pred)
    feature_path = RUN_ROOT / "results/variant_feature_reads" / f"{spec.variant_id}_tier_a_quantile_feature_read.csv"
    feature_frame, feature_read = feature_importance_frame(models, spec.feature_names)
    save_frame(feature_path, feature_frame)
    val = metrics.get("validation", {})
    oos = metrics.get("oos", {})
    return {
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "description": spec.description,
        "spec": spec.payload(),
        "training_sample": sample,
        "thresholds": thresholds,
        "feature_read": {**feature_read, "path": rel(feature_path), "sha256": sha256_file_lf_normalized(feature_path)},
        "split_metrics": metrics,
        "validation_pinball_mean": val.get("pinball_mean"),
        "oos_pinball_mean": oos.get("pinball_mean"),
        "validation_balanced_accuracy": val.get("balanced_accuracy"),
        "oos_balanced_accuracy": oos.get("balanced_accuracy"),
        "validation_interval_coverage": val.get("interval_coverage_q10_q90"),
        "oos_interval_coverage": oos.get("interval_coverage_q10_q90"),
        "validation_crossing_rate": val.get("quantile_crossing_rate"),
        "oos_crossing_rate": oos.get("quantile_crossing_rate"),
        "tier_b_compatible": bool(spec.tier_b_compatible),
        "characteristic_score": characteristic_score(metrics),
    }


def select_variant(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    compatible = [row for row in rows if row.get("tier_b_compatible") is True]
    if not compatible:
        raise RuntimeError("No Tier-B-compatible quantile boosting variant is available.")
    return dict(max(compatible, key=lambda row: safe_float(row.get("characteristic_score"))))


def save_variant_results(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result_root = RUN_ROOT / "results"
    json_path = result_root / "quantile_boosting_variant_results.json"
    csv_path = result_root / "quantile_boosting_variant_results.csv"
    write_json(json_path, rows)
    csv_rows = []
    for row in rows:
        csv_rows.append(
            {
                "variant_id": row.get("variant_id"),
                "idea_id": row.get("idea_id"),
                "feature_count": len(row.get("spec", {}).get("feature_names", [])),
                "tier_b_compatible": row.get("tier_b_compatible"),
                "characteristic_score": row.get("characteristic_score"),
                "validation_pinball_mean": row.get("validation_pinball_mean"),
                "oos_pinball_mean": row.get("oos_pinball_mean"),
                "validation_balanced_accuracy": row.get("validation_balanced_accuracy"),
                "oos_balanced_accuracy": row.get("oos_balanced_accuracy"),
                "validation_interval_coverage": row.get("validation_interval_coverage"),
                "oos_interval_coverage": row.get("oos_interval_coverage"),
                "validation_crossing_rate": row.get("validation_crossing_rate"),
                "oos_crossing_rate": row.get("oos_crossing_rate"),
            }
        )
    write_csv(csv_path, list(csv_rows[0].keys()), csv_rows)
    return {
        "variant_results_json": {"path": rel(json_path), "sha256": sha256_file_lf_normalized(json_path)},
        "variant_results_csv": {"path": rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path)},
    }


def spec_from_row(row: Mapping[str, Any]) -> QuantileBoostingVariantSpec:
    spec = dict(row["spec"])
    spec.pop("quantiles", None)
    spec["feature_names"] = tuple(spec["feature_names"])
    return QuantileBoostingVariantSpec(**spec)


def feature_importance_frame(models: Mapping[float, GradientBoostingRegressor], feature_names: Sequence[str]) -> tuple[pd.DataFrame, dict[str, Any]]:
    values = []
    for quantile, model in models.items():
        importance = getattr(model, "feature_importances_", None)
        if importance is None:
            continue
        for feature, score in zip(feature_names, importance, strict=True):
            values.append({"quantile": quantile, "feature": feature, "importance": float(score)})
    raw = pd.DataFrame(values)
    if raw.empty:
        frame = pd.DataFrame({"feature": list(feature_names), "importance_mean": np.zeros(len(feature_names))})
    else:
        frame = (
            raw.groupby("feature", as_index=False)["importance"]
            .mean()
            .rename(columns={"importance": "importance_mean"})
            .sort_values("importance_mean", ascending=False)
        )
    top = [{"feature": str(row.feature), "importance_mean": float(row.importance_mean)} for row in frame.head(12).itertuples(index=False)]
    return frame, {"top_features": top, "importance_sum": float(frame["importance_mean"].sum())}


def tier_record(record_view: str, tier_scope: str, pred: pd.DataFrame, thresholds: Mapping[str, float], path: Path) -> dict[str, Any]:
    metrics = split_tail_metrics(pred)
    total_signal = int(pred["decision_label"].ne(1).sum())
    subtype_counts: dict[str, int] = {}
    if "partial_context_subtype" in pred.columns:
        subtype_counts = {
            str(key): int(value)
            for key, value in pred["partial_context_subtype"].astype(str).value_counts().sort_index().items()
        }
    totals = {
        "rows": int(len(pred)),
        "signal_count": total_signal,
        "short_count": int(pred["decision_label"].eq(0).sum()),
        "long_count": int(pred["decision_label"].eq(2).sum()),
        "flat_count": int(pred["decision_label"].eq(1).sum()),
        "signal_coverage": float(total_signal / max(1, len(pred))),
        "tail_spread_mean": float(pred["tail_spread"].mean()),
        "tail_pressure_mean": float(pred["tail_pressure"].mean()),
        "tail_asymmetry_abs_mean": float(pred["tail_asymmetry"].abs().mean()),
        "quantile_crossing_rate": float(pred["quantile_crossed"].mean()),
        "direction_strength_threshold": float(thresholds.get("direction_strength", 0.0)),
        "tail_pressure_threshold": float(thresholds.get("tail_pressure", 0.0)),
        "partial_context_subtype_counts": subtype_counts or None,
    }
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": totals,
        "split_metrics": {split: metrics.get(split, {}) for split in ("train", "validation", "oos")},
        "tail_surface_read": tail_surface_read(pred),
    }


def materialize_selected(context: Mapping[str, Any], selected: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], dict[str, Any]]:
    spec = spec_from_row(selected)
    if not spec.tier_b_compatible:
        raise RuntimeError("Selected quantile boosting variant must be Tier-B-compatible for runtime handoff.")
    tier_a_models, tier_a_sample = fit_quantile_variant(context["tier_a_frame"], spec)
    tier_b_models, tier_b_sample = fit_quantile_variant(context["tier_b_training_frame"], spec)
    tier_a_pred, tier_a_thresholds = prediction_frame(tier_a_models, context["tier_a_frame"], spec.feature_names)
    tier_b_train_pred, tier_b_thresholds = prediction_frame(tier_b_models, context["tier_b_training_frame"], spec.feature_names)
    tier_b_pred, _ = prediction_frame(tier_b_models, context["tier_b_fallback_frame"], spec.feature_names, tier_b_thresholds)
    tier_ab_pred = pd.concat(
        [
            tier_a_pred.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_pred.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    pred_root = RUN_ROOT / "predictions"
    a_path = pred_root / "tier_a_quantile_tail_predictions.parquet"
    b_path = pred_root / "tier_b_quantile_tail_predictions.parquet"
    ab_path = pred_root / "tier_ab_quantile_tail_predictions.parquet"
    tier_records = [
        tier_record("tier_a_separate", mt5.TIER_A, tier_a_pred, tier_a_thresholds, a_path),
        tier_record("tier_b_separate", mt5.TIER_B, tier_b_pred, tier_b_thresholds, b_path),
        tier_record("tier_ab_combined", mt5.TIER_AB, tier_ab_pred, tier_a_thresholds, ab_path),
    ]
    prediction_artifacts = {
        "tier_a_predictions": save_frame(a_path, tier_a_pred),
        "tier_b_predictions": save_frame(b_path, tier_b_pred),
        "tier_ab_predictions": save_frame(ab_path, tier_ab_pred),
    }
    model_root = RUN_ROOT / "models"
    io_path(model_root).mkdir(parents=True, exist_ok=True)
    tier_a_model_path = model_root / f"{spec.variant_id}_tier_a_quantile_boosting.joblib"
    tier_b_model_path = model_root / f"{spec.variant_id}_tier_b_quantile_boosting.joblib"
    joblib.dump({"models": tier_a_models, "spec": spec.payload(), "sklearn_version": sklearn_version()}, io_path(tier_a_model_path))
    joblib.dump({"models": tier_b_models, "spec": spec.payload(), "sklearn_version": sklearn_version()}, io_path(tier_b_model_path))
    tier_a_feature_frame, tier_a_feature_read = feature_importance_frame(tier_a_models, spec.feature_names)
    tier_b_feature_frame, tier_b_feature_read = feature_importance_frame(tier_b_models, spec.feature_names)
    feature_root = RUN_ROOT / "results/selected_feature_reads"
    tier_a_feature_path = feature_root / "tier_a_quantile_feature_read.csv"
    tier_b_feature_path = feature_root / "tier_b_quantile_feature_read.csv"
    save_frame(tier_a_feature_path, tier_a_feature_frame)
    save_frame(tier_b_feature_path, tier_b_feature_frame)
    model_artifacts = {
        "selected_variant_id": spec.variant_id,
        "sklearn_version": sklearn_version(),
        "tier_a_training_sample": tier_a_sample,
        "tier_b_training_sample": tier_b_sample,
        "tier_a_model": {"path": rel(tier_a_model_path), "sha256": sha256_file_lf_normalized(tier_a_model_path)},
        "tier_b_model": {"path": rel(tier_b_model_path), "sha256": sha256_file_lf_normalized(tier_b_model_path)},
        "runtime_feature_order": list(spec.feature_names),
        "runtime_feature_order_hash": ordered_hash(spec.feature_names),
        "selected_thresholds": {"tier_a": tier_a_thresholds, "tier_b": tier_b_thresholds},
        "feature_reads": {
            "tier_a": {**tier_a_feature_read, "path": rel(tier_a_feature_path), "sha256": sha256_file_lf_normalized(tier_a_feature_path)},
            "tier_b": {**tier_b_feature_read, "path": rel(tier_b_feature_path), "sha256": sha256_file_lf_normalized(tier_b_feature_path)},
        },
    }
    selected_tail_read = {
        "tier_a": tail_surface_read(tier_a_pred),
        "tier_b": tail_surface_read(tier_b_pred),
        "tier_ab": tail_surface_read(tier_ab_pred),
        "tier_b_training_threshold_source": tail_surface_read(tier_b_train_pred),
    }
    return tier_records, prediction_artifacts, model_artifacts, selected_tail_read


def build_summary(
    context: Mapping[str, Any],
    variants: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    variant_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    prediction_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    selected_tail_read: Mapping[str, Any],
) -> dict[str, Any]:
    best_overall = dict(max(variants, key=lambda row: safe_float(row.get("characteristic_score")), default={}))
    validation = tier_records[0].get("split_metrics", {}).get("validation", {}) if tier_records else {}
    oos = tier_records[0].get("split_metrics", {}).get("oos", {}) if tier_records else {}
    return {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "target_column": TARGET_COLUMN,
        "quantiles": list(QUANTILES),
        "status": "reviewed_structural_scout_completed",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
        "mt5_runtime_probe_status": f"not_attempted_in_run21A_next_milestone_{NEXT_RUN_ID}",
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "sklearn_version": sklearn_version(),
        "variant_count": len(variants),
        "selected_variant_id": selected.get("variant_id"),
        "best_overall_variant_id": best_overall.get("variant_id"),
        "selected_threshold_id": f"strength_q{STRENGTH_QUANTILE:.2f}_tail_q{TAIL_PRESSURE_QUANTILE:.2f}",
        "tier_a_rows": int(len(context["tier_a_frame"])),
        "tier_b_fallback_rows": int(len(context["tier_b_fallback_frame"])),
        "tier_b_context_summary": context["tier_b_context_summary"],
        "tier_records": list(tier_records),
        "selected_tier_a_validation_pinball_mean": validation.get("pinball_mean"),
        "selected_tier_a_oos_pinball_mean": oos.get("pinball_mean"),
        "selected_tier_a_validation_interval_coverage": validation.get("interval_coverage_q10_q90"),
        "selected_tier_a_oos_interval_coverage": oos.get("interval_coverage_q10_q90"),
        "selected_tier_a_validation_balanced_accuracy": validation.get("balanced_accuracy"),
        "selected_tier_a_oos_balanced_accuracy": oos.get("balanced_accuracy"),
        "selected_tail_read": selected_tail_read,
        "model_characteristic_strength": "quantile_tail_surface_visible_enough_for_runtime_probe",
        "artifacts": {
            "model_input_path": rel(stage26_scout.MODEL_INPUT_PATH),
            "feature_order_path": rel(stage26_scout.FEATURE_ORDER_PATH),
            "variant_results": dict(variant_artifacts),
            "model_artifacts": dict(model_artifacts),
            "prediction_artifacts": dict(prediction_artifacts),
        },
        "forbidden_claims": [
            "edge",
            "alpha_quality",
            "baseline",
            "promotion_candidate",
            "operating_promotion",
            "runtime_authority",
        ],
        "next_condition": f"Run {NEXT_RUN_ID} as a narrow MT5 runtime_probe using small tranche/sentinel output before any larger batch.",
    }


def materialize_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    rows = []
    for record in summary["tier_records"]:
        metrics = record["metrics"]
        rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__python_{record['record_view']}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"python_{record['record_view']}",
                "parent_run_id": RUN_ID,
                "record_view": f"python_{record['record_view']}",
                "tier_scope": record["tier_scope"],
                "kpi_scope": "quantile_boosting_tail_risk_surface",
                "scoreboard_lane": "structural_scout",
                "status": "reviewed",
                "judgment": JUDGMENT,
                "path": record["path"],
                "primary_kpi": ledger_pairs(
                    (
                        ("rows", metrics.get("rows")),
                        ("signal_coverage", metrics.get("signal_coverage")),
                        ("tail_spread_mean", metrics.get("tail_spread_mean")),
                        ("tail_pressure_mean", metrics.get("tail_pressure_mean")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("short_count", metrics.get("short_count")),
                        ("long_count", metrics.get("long_count")),
                        ("crossing_rate", metrics.get("quantile_crossing_rate")),
                        ("tail_asymmetry_abs_mean", metrics.get("tail_asymmetry_abs_mean")),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
                "notes": "Quantile boosting tail-risk structural scout only; not baseline, promotion, or runtime authority.",
            }
        )
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "quantile_boosting_tail_risk_structural_scout",
        "status": "reviewed",
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": ledger_pairs(
            (
                ("selected_variant", summary["selected_variant_id"]),
                ("sklearn_version", summary["sklearn_version"]),
                ("external_verification", summary["external_verification_status"]),
                ("next", NEXT_RUN_ID),
                ("boundary", BOUNDARY),
            )
        ),
    }
    return {
        "stage_run_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "project_alpha_run_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id"),
    }


def build_skill_receipts(summary: Mapping[str, Any], created_at: str) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "Quantile boosting can expose downside/upside tail spread and abstention clues from q10/q50/q90 return surfaces.",
            "decision_use": "Decide whether Stage27 should proceed to a narrow MT5 runtime_probe.",
            "control_variables": [FEATURE_SET_ID, LABEL_ID, SPLIT_CONTRACT, "Tier A/B paired records"],
            "changed_variables": ["feature subset", "learning rate", "tree depth", "tail surface read"],
            "stop_condition": "Move to runtime probe once tail-risk characteristic is visible enough; avoid meaningless micro-tuning.",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "selection_metric": "pinball loss, interval coverage, quantile crossing, decision balance, Tier-B compatibility",
            "validation_judgment": "exploratory_inconclusive",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "claim_boundary": summary["boundary"],
            "forbidden_claims": summary["forbidden_claims"],
        },
    ]


def write_packet(summary: Mapping[str, Any], created_at: str) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(PACKET_ROOT / "skill_receipts.json", build_skill_receipts(summary, created_at))
    write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "packet_id": PACKET_ID,
            "boundary": BOUNDARY,
            "allowed_claim": "Stage27 quantile boosting Python-side structural scout completed; runtime probe remains next.",
            "forbidden_claims": summary["forbidden_claims"],
            "selected_operating_reference": None,
            "selected_promotion_candidate": None,
            "selected_baseline": None,
            "runtime_authority": None,
        },
    )


def write_review(summary: Mapping[str, Any]) -> None:
    val = summary["selected_tail_read"].get("tier_a", {}).get("split_metrics", {}).get("validation", {})
    oos = summary["selected_tail_read"].get("tier_a", {}).get("split_metrics", {}).get("oos", {})
    top_features = [
        item.get("feature")
        for item in summary["artifacts"]["model_artifacts"]["feature_reads"]["tier_a"]["top_features"][:5]
    ]
    write_md(
        REPORT_PATH,
        f"""# RUN21A Quantile Boosting Tail Risk Scout Packet(21A 실행 분위수 부스팅 꼬리 위험 탐색 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{summary['selected_variant_id']}`
- best overall variant(전체 최고 변형): `{summary['best_overall_variant_id']}`
- sklearn version(scikit-learn 버전): `{summary['sklearn_version']}`
- boundary(경계): `{BOUNDARY}`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run21A_next_milestone_{NEXT_RUN_ID}`

효과(effect, 효과): Stage27(27단계)는 q10/q50/q90 return quantile surface(수익률 분위수 표면), tail spread(꼬리 간격), downside/upside pressure(하방/상방 압력)를 Python-side evidence(파이썬 근거)로 확인했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Evidence(근거)

- variants(변형): `{summary['variant_count']}`
- selected Tier A validation pinball mean(선택 Tier A 검증 핀볼 평균 손실): `{summary['selected_tier_a_validation_pinball_mean']}`
- selected Tier A OOS pinball mean(선택 Tier A 표본외 핀볼 평균 손실): `{summary['selected_tier_a_oos_pinball_mean']}`
- selected Tier A validation interval coverage(선택 Tier A 검증 구간 커버리지): `{summary['selected_tier_a_validation_interval_coverage']}`
- selected Tier A OOS interval coverage(선택 Tier A 표본외 구간 커버리지): `{summary['selected_tier_a_oos_interval_coverage']}`
- selected Tier A validation balanced accuracy(선택 Tier A 검증 균형 정확도): `{summary['selected_tier_a_validation_balanced_accuracy']}`
- selected Tier A OOS balanced accuracy(선택 Tier A 표본외 균형 정확도): `{summary['selected_tier_a_oos_balanced_accuracy']}`
- validation crossing rate(검증 분위수 교차율): `{val.get('quantile_crossing_rate')}`
- OOS crossing rate(표본외 분위수 교차율): `{oos.get('quantile_crossing_rate')}`

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `{summary['tier_records'][0]['path']}`
- Tier B separate(Tier B 분리): `{summary['tier_records'][1]['path']}`
- Tier A+B combined(Tier A+B 합산): `{summary['tier_records'][2]['path']}`

효과(effect, 효과): Tier A(티어 A)만 본 결과를 전체 read(판독)로 과장하지 않고, Tier B fallback(Tier B 대체)에서 같은 tail surface(꼬리 표면)가 어떻게 달라지는지 다음 runtime_probe(런타임 탐침)로 넘긴다.

## Preserved Clues(보존 단서)

- quantile spread(분위수 간격)는 confidence(확신)가 아니라 risk width(위험 폭)로 읽어야 한다.
- selected feature read(선택 피처 판독) top features(상위 피처): `{top_features}`
- q10/q90 interval coverage(q10/q90 구간 커버리지)와 quantile crossing(분위수 교차)은 runtime handoff(런타임 인계) 전 guardrail(보호 기준)이다.

## Negative Memory(부정 기억)

- run21A(21A 실행)는 Python structural scout(파이썬 구조 탐색)라 MT5 runtime behavior(MT5 런타임 행동)를 아직 증명하지 않는다.
- selected variant(선택 변형)는 promotion candidate(승격 후보)가 아니라 Stage27(27단계) MT5 probe(MT5 탐침)에 넘길 handoff candidate(인계 후보)다.
- interval coverage(구간 커버리지)가 edge(거래 우위)를 뜻하지 않는다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}` as the narrow MT5 runtime_probe(좁은 MT5 런타임 탐침) with small tranche/sentinel check(작은 묶음/감시 실행 확인).
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else ""
    line = f"- `{RUN_ID}`: `{rel(REPORT_PATH)}`\n"
    if f"- `{RUN_ID}`:" not in review:
        if "No reviewed run yet" in review:
            review = "Reviewed runs(검토된 실행):\n"
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)


def write_decision(summary: Mapping[str, Any]) -> None:
    write_md(
        DECISION_PATH,
        f"""# Decision(결정): Stage27 RUN21A Quantile Boosting Scout(27단계 21A 실행 분위수 부스팅 탐색)

Stage27(27단계) `{RUN_ID}`를 reviewed structural scout(검토된 구조 탐색)로 기록한다.

효과(effect, 효과): quantile boosting(분위수 부스팅)의 tail-risk surface(꼬리 위험 표면), interval coverage(구간 커버리지), quantile crossing(분위수 교차)을 보존 단서로 남기고 다음 행동은 `{NEXT_RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)로 제한한다.

- selected variant(선택 변형): `{summary['selected_variant_id']}`
- judgment(판정): `{JUDGMENT}`
- boundary(경계): `{BOUNDARY}`
""",
    )


def write_selection_status(summary: Mapping[str, Any]) -> None:
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage27 Selection Status(27단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `active_run21A_structural_scout_completed`
- selected variant for next probe(다음 탐침용 선택 변형): `{summary['selected_variant_id']}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- next action(다음 행동): `{NEXT_RUN_ID}`

효과(effect, 효과): 선택 변형은 Stage27(27단계) MT5 runtime_probe(MT5 런타임 탐침)에 넘길 handoff candidate(인계 후보)일 뿐이며 baseline(기준선)이나 promotion(승격)이 아니다.
""",
    )


def replace_top_level_yaml_block(text: str, marker: str, block: str) -> str:
    start = text.find(marker)
    if start < 0:
        return text.rstrip() + "\n" + block.rstrip() + "\n"
    next_start = text.find("\nstage", start + 1)
    if next_start < 0:
        return text[:start] + block.rstrip() + "\n"
    return text[:start] + block.rstrip() + text[next_start:]


def replace_markdown_section(text: str, heading_prefix: str, new_section: str) -> str:
    start = text.find(heading_prefix)
    if start < 0:
        return text.rstrip() + "\n\n" + new_section.rstrip() + "\n"
    next_start = text.find("\n## ", start + 1)
    if next_start < 0:
        return text[:start] + new_section.rstrip() + "\n"
    return text[:start] + new_section.rstrip() + "\n\n" + text[next_start + 1 :]


def set_top_level_value(text: str, key: str, value: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(f"{key}: "):
            lines[index] = f"{key}: {value}"
            break
    else:
        lines.insert(0, f"{key}: {value}")
    return "\n".join(lines) + "\n"


def replace_current_focus_stage27_line(text: str) -> str:
    replacement = (
        f"- treat Stage 27 as active_run21A_structural_scout_completed after quantile boosting(분위수 부스팅) "
        f"tail-risk surface scout(꼬리 위험 표면 탐색); next action is {NEXT_RUN_ID}, "
        "and no baseline, promotion, or runtime authority exists"
    )
    lines = text.splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if line.startswith("- treat Stage 27 as "):
            lines[index] = replacement
            replaced = True
            break
    if not replaced:
        for index, line in enumerate(lines):
            if line == "current_focus:":
                lines.insert(index + 1, replacement)
                break
    return "\n".join(lines) + "\n"


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = set_top_level_value(state, "current_run_id", RUN_ID)
    state = replace_current_focus_stage27_line(state)
    state = state.replace(
        "      status: opened_not_started\n      current_run_id: not_started",
        f"      status: active_run21A_structural_scout_completed\n      current_run_id: {RUN_ID}",
        1,
    )
    block = f"""stage27_quantile_boosting_model:
  stage_id: {STAGE_ID}
  status: active_run21A_structural_scout_completed
  current_run_id: {RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {summary['selected_variant_id']}
  boundary: {BOUNDARY}
  judgment: {JUDGMENT}
  mt5_runtime_probe_status: not_attempted_next_milestone_{NEXT_RUN_ID}
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage27_quantile_boosting_model:", block)
    run_block = f"""stage27_quantile_run21A_structural_scout:
  packet_id: {PACKET_ID}
  status: reviewed_structural_scout_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  selected_variant_id: {summary['selected_variant_id']}
  mt5_runtime_probe_status: not_attempted_next_milestone_{NEXT_RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage27_quantile_run21A_structural_scout:", run_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8-sig")


def update_goal_plan(summary: Mapping[str, Any]) -> None:
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    plan = plan.replace("- current run(현재 실행): `not_started`", f"- current run(현재 실행): `{RUN_ID}`", 1)
    plan = plan.replace(
        f"현재 첫 미완료 milestone(마일스톤)은 Stage27(27단계) `{RUN_ID}` broad scout(넓은 탐색)이다.",
        f"Stage27(27단계)는 `{RUN_ID}` broad scout(넓은 탐색)를 완료했고, 현재 첫 미완료 milestone(마일스톤)은 `{NEXT_RUN_ID}` narrow MT5 runtime_probe(좁은 MT5 런타임 탐침)이다.",
        1,
    )
    plan = plan.replace(
        f"Current active milestone(현재 활성 마일스톤): Stage27(27단계) `{RUN_ID}` broad scout(넓은 탐색).",
        f"Current active milestone(현재 활성 마일스톤): Stage27(27단계) `{NEXT_RUN_ID}` narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).",
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `{RUN_ID}` completed(완료) as Python structural scout(파이썬 구조 탐색).
- active branch(활성 브랜치): `codex/stage27-quantile-boosting`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage27(27단계), `{RUN_ID}`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE_ID}/02_runs/{RUN_ID}`, `stages/{STAGE_ID}/03_reviews`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): quantile boosting scout pipeline(분위수 부스팅 탐색 파이프라인), run evidence(실행 근거), tier prediction artifacts(티어 예측 산출물), current truth docs(현재 진실 문서).
- active stage folder(활성 단계 폴더): `stages/{STAGE_ID}`.
- current run id(현재 실행 ID): `{RUN_ID}`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): MT5 not attempted in run21A(21A 실행에서 MT5 미시도); review report(검토 보고서) `{rel(REPORT_PATH)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{NEXT_RUN_ID}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage27(27단계) quantile boosting(분위수 부스팅) MT5 runtime_probe(MT5 런타임 탐침)에서 시작한다.
"""
    plan = replace_markdown_section(plan, "## Latest Stop Resume State", resume)
    outcome = f"- `2026-05-05`: Stage27(27단계) `{RUN_ID}` quantile boosting(분위수 부스팅) Python structural scout(파이썬 구조 탐색)를 완료했다. judgment(판정): `{JUDGMENT}`."
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome + "\n"
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")


def prepend_current_working_state(summary: Mapping[str, Any]) -> None:
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage27 RUN21A Quantile Boosting Scout(최신 27단계 21A 실행 분위수 부스팅 탐색)

Stage27(27단계) `{RUN_ID}`를 reviewed structural scout(검토된 구조 탐색)로 완료했다.

결과(result, 결과): `{JUDGMENT}`. selected variant(선택 변형): `{summary['selected_variant_id']}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): quantile boosting(분위수 부스팅)의 tail-risk surface(꼬리 위험 표면)는 보존 단서로 남기고 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

"""
    if f"## Latest Stage27 RUN21A Quantile Boosting Scout" not in current:
        io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    variants = [evaluate_variant(context, spec) for spec in default_variants(context["full_feature_order"], context["tier_b_feature_order"])]
    selected = select_variant(variants)
    variant_artifacts = save_variant_results(variants)
    tier_records, prediction_artifacts, model_artifacts, selected_tail_read = materialize_selected(context, selected)
    summary = build_summary(
        context=context,
        variants=variants,
        selected=selected,
        variant_artifacts=variant_artifacts,
        tier_records=tier_records,
        prediction_artifacts=prediction_artifacts,
        model_artifacts=model_artifacts,
        selected_tail_read=selected_tail_read,
    )
    summary["ledger_updates"] = materialize_ledgers(summary)
    write_packet(summary, created_at)
    write_review(summary)
    write_decision(summary)
    write_selection_status(summary)
    update_workspace_state(summary)
    update_goal_plan(summary)
    prepend_current_working_state(summary)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2, sort_keys=True))
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Run Stage27 quantile boosting tail-risk structural scout.")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
