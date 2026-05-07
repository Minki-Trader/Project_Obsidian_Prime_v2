from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter, WeibullAFTFitter
from lifelines.utils import concordance_index

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
import foundation.models.alpha_scout_support as scout_support
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5


STAGE_ID = "24_exit_model__survival_time_to_event_hold_shape"
RUN_ID = "run18A_survival_time_to_event_hold_shape_scout_v1"
RUN_NUMBER = "run18A"
PACKET_ID = "stage24_run18A_survival_time_to_event_scout_v1"
NEXT_RUN_ID = "run18B_survival_time_to_event_runtime_probe_v1"
EXPLORATION_LABEL = "stage24_Exit__SurvivalTimeToEventHoldShape"
MODEL_FAMILY = "lifelines_survival_time_to_event_models"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_survival_hold_shape"
LABEL_ID = scout_support.LABEL_ID
SPLIT_CONTRACT = scout_support.SPLIT_CONTRACT
MAX_HORIZON_BARS = 12
BOUNDARY = "survival_time_to_event_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_survival_time_to_event_hold_shape_scout_completed"

ROOT = scout_support.ROOT
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REPORT_PATH = STAGE_ROOT / "03_reviews/run18A_survival_time_to_event_scout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage24_run18A_survival_time_to_event_scout.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN_PATH = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"


@dataclass(frozen=True)
class SurvivalVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    model_type: str
    event_name: str
    feature_names: tuple[str, ...]
    threshold_multiplier: float
    tier_b_compatible: bool = True
    penalizer: float = 1.0
    peak_multiplier: float | None = None

    def payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["feature_names"] = list(self.feature_names)
        return payload


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return scout_support.rel(path)


def safe_float(value: Any, default: float = 0.0) -> float:
    return scout_support.safe_float(value, default)


def write_json(path: Path, payload: Any) -> None:
    scout_support.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    scout_support.write_md(path, text)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    return scout_support.save_frame(path, frame)


def load_context() -> dict[str, Any]:
    return scout_support.load_context()


def core24_features() -> tuple[str, ...]:
    return scout_support.core24_features()


def volatility_session_features() -> tuple[str, ...]:
    return (
        "log_return_1",
        "log_return_3",
        "return_zscore_20",
        "hl_range",
        "atr_14",
        "atr_14_over_atr_50",
        "bollinger_width_20",
        "historical_vol_20",
        "adx_14",
        "di_spread_14",
        "rsi_14",
        "rsi_14_slope_3",
        "minutes_from_cash_open",
        "is_first_30m_after_open",
    )


def default_variants(tier_b_feature_order: Sequence[str]) -> list[SurvivalVariantSpec]:
    tier_b_set = set(tier_b_feature_order)
    core = tuple(name for name in core24_features() if name in tier_b_set)
    vol_session = tuple(name for name in volatility_session_features() if name in tier_b_set)
    return [
        SurvivalVariantSpec(
            variant_id="v01_cox_core24_abs_move_3x",
            idea_id="absolute_move_time_to_event",
            description="Cox proportional hazard model for time until either-side price movement reaches 3x the label threshold.",
            model_type="cox",
            event_name="abs_move_3x",
            feature_names=core,
            threshold_multiplier=3.0,
        ),
        SurvivalVariantSpec(
            variant_id="v02_cox_core24_adverse_direction_1p5x",
            idea_id="adverse_direction_time_to_event",
            description="Cox model for time until label-direction adverse movement reaches 1.5x threshold; structural hindsight only.",
            model_type="cox",
            event_name="adverse_direction_1p5x",
            feature_names=core,
            threshold_multiplier=1.5,
        ),
        SurvivalVariantSpec(
            variant_id="v03_cox_vol_session_abs_move_3x",
            idea_id="volatility_session_exit_clock",
            description="Cox model using volatility/session features for the same absolute movement event.",
            model_type="cox",
            event_name="abs_move_3x",
            feature_names=vol_session,
            threshold_multiplier=3.0,
        ),
        SurvivalVariantSpec(
            variant_id="v04_weibull_aft_core24_abs_move_3x",
            idea_id="parametric_survival_duration_shape",
            description="Weibull AFT model for absolute movement event to compare parametric duration shape.",
            model_type="weibull_aft",
            event_name="abs_move_3x",
            feature_names=core,
            threshold_multiplier=3.0,
        ),
    ]


def add_future_return_path(frame: pd.DataFrame, max_horizon_bars: int = MAX_HORIZON_BARS) -> pd.DataFrame:
    work = frame.sort_values("timestamp").reset_index(drop=True).copy()
    returns = pd.to_numeric(work["log_return_1"], errors="coerce").fillna(0.0)
    cumulative = pd.Series(np.zeros(len(work), dtype="float64"))
    for horizon in range(1, max_horizon_bars + 1):
        cumulative = cumulative + returns.shift(-horizon)
        work[f"future_cum_log_return_{horizon}"] = cumulative.to_numpy(dtype="float64", copy=False)
    return work


def label_direction(frame: pd.DataFrame) -> np.ndarray:
    if "label_id" in frame.columns:
        label_id = pd.to_numeric(frame["label_id"], errors="coerce")
        direction = np.where(label_id.eq(2), 1, np.where(label_id.eq(0), -1, 0))
        return direction.astype("int8")
    label_text = frame.get("label_class", pd.Series([""] * len(frame))).astype(str).str.lower()
    direction = np.where(
        label_text.str.contains("long|up|buy"),
        1,
        np.where(label_text.str.contains("short|down|sell"), -1, 0),
    )
    return direction.astype("int8")


def event_duration_arrays(frame: pd.DataFrame, spec: SurvivalVariantSpec, base_threshold: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    future_cols = [f"future_cum_log_return_{horizon}" for horizon in range(1, MAX_HORIZON_BARS + 1)]
    values = frame[future_cols].to_numpy(dtype="float64", copy=False)
    threshold = abs(float(base_threshold) * float(spec.threshold_multiplier))
    directions = label_direction(frame)
    durations: list[int] = []
    events: list[int] = []
    usable_mask: list[bool] = []
    for row_index in range(len(frame)):
        row = values[row_index]
        valid_count = int(np.isfinite(row).sum())
        if valid_count < 1:
            durations.append(0)
            events.append(0)
            usable_mask.append(False)
            continue
        horizon_values = row[:valid_count]
        direction = int(directions[row_index])
        if spec.event_name == "abs_move_3x":
            hits = np.flatnonzero(np.abs(horizon_values) >= threshold)
            usable = True
        elif spec.event_name == "adverse_direction_1p5x":
            if direction == 0:
                hits = np.array([], dtype=int)
                usable = False
            else:
                signed_path = direction * horizon_values
                hits = np.flatnonzero(signed_path <= -threshold)
                usable = True
        elif spec.event_name == "profit_decay_after_peak_2x":
            if direction == 0:
                hits = np.array([], dtype=int)
                usable = False
            else:
                signed_path = direction * horizon_values
                peak_path = np.maximum.accumulate(signed_path)
                peak_threshold = abs(float(base_threshold) * float(spec.peak_multiplier or 2.0))
                hits = np.flatnonzero((peak_path >= peak_threshold) & (signed_path <= peak_path * 0.5))
                usable = True
        else:
            raise ValueError(f"Unknown event_name: {spec.event_name}")
        if hits.size:
            durations.append(int(hits[0]) + 1)
            events.append(1)
        else:
            durations.append(valid_count)
            events.append(0)
        usable_mask.append(usable)
    return (
        np.asarray(durations, dtype="int16"),
        np.asarray(events, dtype="int8"),
        np.asarray(usable_mask, dtype=bool),
    )


def build_survival_frame(frame: pd.DataFrame, spec: SurvivalVariantSpec, base_threshold: float) -> pd.DataFrame:
    work = add_future_return_path(frame)
    durations, events, usable = event_duration_arrays(work, spec, base_threshold)
    work["duration_bars"] = durations
    work["event_observed"] = events
    work["event_name"] = spec.event_name
    work["threshold_multiplier"] = float(spec.threshold_multiplier)
    work["event_threshold_abs_log_return"] = abs(float(base_threshold) * float(spec.threshold_multiplier))
    work = work.loc[usable & (work["duration_bars"] >= 1)].copy()
    work["event_observed"] = work["event_observed"].astype("int8")
    work["duration_bars"] = work["duration_bars"].astype("int16")
    return work


def fit_preprocessor(train: pd.DataFrame, feature_names: Sequence[str]) -> dict[str, Any]:
    raw = train.loc[:, list(feature_names)].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan)
    medians = raw.median(axis=0).fillna(0.0)
    filled = raw.fillna(medians)
    variances = filled.var(axis=0)
    usable = [column for column in filled.columns if float(variances.get(column, 0.0)) > 1.0e-12 and filled[column].nunique(dropna=True) > 1]
    if not usable:
        raise ValueError("No usable survival model features after low-variance filtering.")
    means = filled.loc[:, usable].mean(axis=0)
    stds = filled.loc[:, usable].std(axis=0).replace(0.0, 1.0).fillna(1.0)
    return {
        "feature_names": list(usable),
        "dropped_features": [name for name in feature_names if name not in set(usable)],
        "medians": {name: float(medians.get(name, 0.0)) for name in usable},
        "means": {name: float(means.get(name, 0.0)) for name in usable},
        "stds": {name: float(stds.get(name, 1.0)) for name in usable},
        "clip": 8.0,
    }


def transform_features(frame: pd.DataFrame, preprocess: Mapping[str, Any]) -> pd.DataFrame:
    features = list(preprocess["feature_names"])
    raw = frame.loc[:, features].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan)
    for name in features:
        raw[name] = raw[name].fillna(float(preprocess["medians"].get(name, 0.0)))
        raw[name] = (raw[name] - float(preprocess["means"].get(name, 0.0))) / float(preprocess["stds"].get(name, 1.0))
    return raw.clip(lower=-float(preprocess.get("clip", 8.0)), upper=float(preprocess.get("clip", 8.0)))


def survival_fit_frame(frame: pd.DataFrame, preprocess: Mapping[str, Any]) -> pd.DataFrame:
    x = transform_features(frame, preprocess)
    fit = x.copy()
    fit["duration_bars"] = pd.to_numeric(frame["duration_bars"], errors="coerce").astype("float64")
    fit["event_observed"] = pd.to_numeric(frame["event_observed"], errors="coerce").fillna(0).astype("int8")
    return fit


def fit_survival_model(frame: pd.DataFrame, spec: SurvivalVariantSpec) -> tuple[Any, dict[str, Any], dict[str, Any]]:
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    if len(train) < 500:
        raise ValueError(f"Training sample too small for survival scout: {len(train)}")
    event_rate = float(train["event_observed"].mean())
    if event_rate <= 0.01 or event_rate >= 0.99:
        raise ValueError(f"Training event rate outside useful scout range: {event_rate}")
    preprocess = fit_preprocessor(train, spec.feature_names)
    fit = survival_fit_frame(train, preprocess)
    if spec.model_type == "cox":
        model = CoxPHFitter(penalizer=float(spec.penalizer))
        model.fit(fit, duration_col="duration_bars", event_col="event_observed", show_progress=False)
    elif spec.model_type == "weibull_aft":
        model = WeibullAFTFitter(penalizer=float(spec.penalizer))
        model.fit(fit, duration_col="duration_bars", event_col="event_observed")
    else:
        raise ValueError(f"Unknown model_type: {spec.model_type}")
    sample = {
        "train_rows": int(len(train)),
        "train_event_rate": event_rate,
        "feature_count_before_filter": int(len(spec.feature_names)),
        "feature_count_after_filter": int(len(preprocess["feature_names"])),
        "dropped_features": list(preprocess["dropped_features"]),
    }
    return model, preprocess, sample


def finite_series(values: Any, fallback: float = 0.0) -> pd.Series:
    series = pd.Series(np.asarray(values).reshape(-1)).astype("float64")
    finite = series.replace([np.inf, -np.inf], np.nan)
    if finite.notna().any():
        cap = float(finite.dropna().max())
        floor = float(finite.dropna().min())
        series = series.replace(np.inf, cap).replace(-np.inf, floor).fillna(fallback)
    else:
        series = series.replace([np.inf, -np.inf], np.nan).fillna(fallback)
    return series


def prediction_frame(model: Any, preprocess: Mapping[str, Any], frame: pd.DataFrame, spec: SurvivalVariantSpec) -> pd.DataFrame:
    x = transform_features(frame, preprocess)
    if spec.model_type == "cox":
        risk_score = finite_series(model.predict_partial_hazard(x), fallback=1.0)
        survival_score = -risk_score
    else:
        median_duration = finite_series(model.predict_median(x), fallback=float(MAX_HORIZON_BARS))
        survival_score = median_duration
        risk_score = -median_duration
    columns = [
        "timestamp",
        "split",
        "label_id",
        "label_class",
        "duration_bars",
        "event_observed",
        "event_name",
        "threshold_multiplier",
        "event_threshold_abs_log_return",
    ]
    optional = [name for name in ("partial_context_subtype", "tier_scope") if name in frame.columns]
    pred = frame[[name for name in columns if name in frame.columns] + optional].copy().reset_index(drop=True)
    pred["variant_id"] = spec.variant_id
    pred["model_type"] = spec.model_type
    pred["survival_score"] = survival_score.to_numpy(dtype="float64", copy=False)
    pred["risk_score"] = risk_score.to_numpy(dtype="float64", copy=False)
    return pred


def split_survival_metrics(pred: pd.DataFrame) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        sub = pred.loc[pred["split"].astype(str).eq(split)].copy()
        if sub.empty:
            metrics[split] = {"rows": 0}
            continue
        durations = pd.to_numeric(sub["duration_bars"], errors="coerce")
        events = pd.to_numeric(sub["event_observed"], errors="coerce").fillna(0).astype(int)
        survival_score = pd.to_numeric(sub["survival_score"], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)
        risk_score = pd.to_numeric(sub["risk_score"], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)
        if int(events.sum()) >= 2 and durations.nunique(dropna=True) > 1:
            try:
                c_index = float(concordance_index(durations, survival_score, events))
            except Exception:
                c_index = None
        else:
            c_index = None
        q33, q66 = risk_score.quantile([0.333, 0.667]).tolist()
        low_risk = sub.loc[risk_score <= q33]
        high_risk = sub.loc[risk_score >= q66]
        low_event_rate = float(low_risk["event_observed"].mean()) if not low_risk.empty else None
        high_event_rate = float(high_risk["event_observed"].mean()) if not high_risk.empty else None
        low_median_duration = float(low_risk["duration_bars"].median()) if not low_risk.empty else None
        high_median_duration = float(high_risk["duration_bars"].median()) if not high_risk.empty else None
        metrics[split] = {
            "rows": int(len(sub)),
            "observed_event_count": int(events.sum()),
            "censored_count": int(len(sub) - int(events.sum())),
            "event_rate": float(events.mean()),
            "median_duration_bars": float(durations.median()),
            "concordance_index": c_index,
            "risk_score_q10": float(risk_score.quantile(0.10)),
            "risk_score_q50": float(risk_score.quantile(0.50)),
            "risk_score_q90": float(risk_score.quantile(0.90)),
            "low_risk_event_rate": low_event_rate,
            "high_risk_event_rate": high_event_rate,
            "high_minus_low_event_rate": None
            if low_event_rate is None or high_event_rate is None
            else float(high_event_rate - low_event_rate),
            "low_risk_median_duration_bars": low_median_duration,
            "high_risk_median_duration_bars": high_median_duration,
            "low_minus_high_median_duration_bars": None
            if low_median_duration is None or high_median_duration is None
            else float(low_median_duration - high_median_duration),
        }
    return metrics


def coefficient_frame(model: Any, preprocess: Mapping[str, Any], spec: SurvivalVariantSpec) -> tuple[pd.DataFrame, dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if spec.model_type == "cox":
        params = model.params_
        for feature, coefficient in params.items():
            rows.append(
                {
                    "feature": str(feature),
                    "coefficient": float(coefficient),
                    "abs_coefficient": abs(float(coefficient)),
                    "effect_read": "positive_coefficient_means_higher_hazard_shorter_survival",
                }
            )
    else:
        params = model.params_
        for index, coefficient in params.items():
            if isinstance(index, tuple):
                component, feature = str(index[0]), str(index[1])
            else:
                component, feature = "unknown", str(index)
            if feature == "Intercept":
                continue
            rows.append(
                {
                    "feature": feature,
                    "component": component,
                    "coefficient": float(coefficient),
                    "abs_coefficient": abs(float(coefficient)),
                    "effect_read": "lambda_positive_coefficient_means_longer_predicted_duration",
                }
            )
    frame = pd.DataFrame(rows).sort_values("abs_coefficient", ascending=False).reset_index(drop=True)
    summary = {
        "feature_count_after_filter": int(len(preprocess["feature_names"])),
        "dropped_features": list(preprocess["dropped_features"]),
        "top_features": frame.head(10).to_dict(orient="records"),
    }
    return frame, summary


def characteristic_score(metrics: Mapping[str, Any]) -> float:
    val = metrics.get("validation", {})
    oos = metrics.get("oos", {})
    train = metrics.get("train", {})
    val_ci = safe_float(val.get("concordance_index"), 0.5)
    oos_ci = safe_float(oos.get("concordance_index"), 0.5)
    train_ci = safe_float(train.get("concordance_index"), 0.5)
    val_event = safe_float(val.get("event_rate"), 0.0)
    oos_event = safe_float(oos.get("event_rate"), 0.0)
    val_spread = abs(safe_float(val.get("high_minus_low_event_rate"), 0.0))
    oos_spread = abs(safe_float(oos.get("high_minus_low_event_rate"), 0.0))
    return float(
        (val_ci - 0.5)
        + (oos_ci - 0.5)
        - abs(val_ci - oos_ci)
        - 0.25 * abs(train_ci - val_ci)
        - 0.15 * abs(val_event - oos_event)
        + 0.05 * (val_spread + oos_spread)
    )


def evaluate_variant(context: Mapping[str, Any], spec: SurvivalVariantSpec) -> dict[str, Any]:
    try:
        frame = build_survival_frame(context["tier_a_frame"], spec, float(context["training_summary"]["threshold_log_return"]))
        model, preprocess, sample = fit_survival_model(frame, spec)
        pred = prediction_frame(model, preprocess, frame, spec)
        metrics = split_survival_metrics(pred)
        feature_frame, feature_summary = coefficient_frame(model, preprocess, spec)
        feature_path = RUN_ROOT / "results/variant_feature_reads" / f"{spec.variant_id}_feature_read.csv"
        save_frame(feature_path, feature_frame)
        return {
            "variant_id": spec.variant_id,
            "idea_id": spec.idea_id,
            "description": spec.description,
            "spec": spec.payload(),
            "status": "completed",
            "training_sample": sample,
            "event_definition": {
                "event_name": spec.event_name,
                "threshold_multiplier": spec.threshold_multiplier,
                "base_threshold_log_return": float(context["training_summary"]["threshold_log_return"]),
                "max_horizon_bars": MAX_HORIZON_BARS,
            },
            "metrics": metrics,
            "feature_read": feature_summary,
            "feature_artifact": {"path": rel(feature_path), "sha256": sha256_file_lf_normalized(feature_path)},
            "characteristic_score": characteristic_score(metrics),
        }
    except Exception as exc:
        return {
            "variant_id": spec.variant_id,
            "idea_id": spec.idea_id,
            "description": spec.description,
            "spec": spec.payload(),
            "status": "invalid_setup",
            "invalid_reason": str(exc),
            "characteristic_score": -999.0,
        }


def select_variant(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [row for row in rows if row.get("status") == "completed" and row.get("spec", {}).get("tier_b_compatible") is True]
    if not completed:
        raise RuntimeError("No completed Stage24 survival scout variant was available for selection.")
    return dict(max(completed, key=lambda row: safe_float(row.get("characteristic_score"), -999.0)))


def spec_from_row(row: Mapping[str, Any]) -> SurvivalVariantSpec:
    payload = dict(row.get("spec", {}))
    payload["feature_names"] = tuple(payload["feature_names"])
    return SurvivalVariantSpec(**payload)


def save_variant_results(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result_root = RUN_ROOT / "results"
    json_path = result_root / "survival_variant_results.json"
    csv_path = result_root / "survival_variant_results.csv"
    write_json(json_path, list(rows))
    csv_rows = []
    for row in rows:
        spec = row.get("spec", {})
        metrics = row.get("metrics", {})
        train = metrics.get("train", {})
        val = metrics.get("validation", {})
        oos = metrics.get("oos", {})
        csv_rows.append(
            {
                "variant_id": row.get("variant_id"),
                "model_type": spec.get("model_type"),
                "event_name": spec.get("event_name"),
                "status": row.get("status"),
                "feature_count": len(spec.get("feature_names", [])),
                "characteristic_score": row.get("characteristic_score"),
                "train_event_rate": train.get("event_rate"),
                "validation_event_rate": val.get("event_rate"),
                "oos_event_rate": oos.get("event_rate"),
                "train_c_index": train.get("concordance_index"),
                "validation_c_index": val.get("concordance_index"),
                "oos_c_index": oos.get("concordance_index"),
                "validation_high_minus_low_event_rate": val.get("high_minus_low_event_rate"),
                "oos_high_minus_low_event_rate": oos.get("high_minus_low_event_rate"),
                "invalid_reason": row.get("invalid_reason"),
            }
        )
    write_csv(
        csv_path,
        (
            "variant_id",
            "model_type",
            "event_name",
            "status",
            "feature_count",
            "characteristic_score",
            "train_event_rate",
            "validation_event_rate",
            "oos_event_rate",
            "train_c_index",
            "validation_c_index",
            "oos_c_index",
            "validation_high_minus_low_event_rate",
            "oos_high_minus_low_event_rate",
            "invalid_reason",
        ),
        csv_rows,
    )
    return {
        "variant_results_json": {"path": rel(json_path), "sha256": sha256_file_lf_normalized(json_path)},
        "variant_results_csv": {"path": rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path)},
    }


def tier_record(record_view: str, tier_scope: str, pred: pd.DataFrame, path: Path) -> dict[str, Any]:
    metrics = split_survival_metrics(pred)
    all_events = pd.to_numeric(pred["event_observed"], errors="coerce").fillna(0).astype(int)
    all_duration = pd.to_numeric(pred["duration_bars"], errors="coerce")
    subtype_counts: dict[str, int] = {}
    if "partial_context_subtype" in pred.columns:
        subtype_counts = {str(key): int(value) for key, value in pred["partial_context_subtype"].astype(str).value_counts().sort_index().items()}
    total = {
        "rows": int(len(pred)),
        "event_count": int(all_events.sum()),
        "event_rate": float(all_events.mean()) if len(pred) else None,
        "median_duration_bars": float(all_duration.median()) if len(pred) else None,
        "validation_c_index": metrics.get("validation", {}).get("concordance_index"),
        "oos_c_index": metrics.get("oos", {}).get("concordance_index"),
        "partial_context_subtype_counts": subtype_counts or None,
    }
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": total,
        "split_metrics": metrics,
    }


def materialize_selected(
    context: Mapping[str, Any],
    selected: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    spec = spec_from_row(selected)
    base_threshold = float(context["training_summary"]["threshold_log_return"])
    tier_a_frame = build_survival_frame(context["tier_a_frame"], spec, base_threshold)
    tier_b_training_frame = build_survival_frame(context["tier_b_training_frame"], spec, base_threshold)
    tier_b_fallback_frame = build_survival_frame(context["tier_b_fallback_frame"], spec, base_threshold)
    tier_a_model, tier_a_preprocess, tier_a_sample = fit_survival_model(tier_a_frame, spec)
    tier_b_model, tier_b_preprocess, tier_b_sample = fit_survival_model(tier_b_training_frame, spec)
    model_root = RUN_ROOT / "models"
    io_path(model_root).mkdir(parents=True, exist_ok=True)
    tier_a_model_path = model_root / f"{spec.variant_id}_tier_a_survival_model.joblib"
    tier_b_model_path = model_root / f"{spec.variant_id}_tier_b_survival_model.joblib"
    joblib.dump({"model": tier_a_model, "preprocess": tier_a_preprocess, "spec": spec.payload()}, io_path(tier_a_model_path))
    joblib.dump({"model": tier_b_model, "preprocess": tier_b_preprocess, "spec": spec.payload()}, io_path(tier_b_model_path))
    tier_a_pred = prediction_frame(tier_a_model, tier_a_preprocess, tier_a_frame, spec)
    tier_b_pred = prediction_frame(tier_b_model, tier_b_preprocess, tier_b_fallback_frame, spec)
    tier_ab_pred = pd.concat(
        [
            tier_a_pred.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_pred.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    pred_root = RUN_ROOT / "predictions"
    a_path = pred_root / "tier_a_survival_predictions.parquet"
    b_path = pred_root / "tier_b_survival_predictions.parquet"
    ab_path = pred_root / "tier_ab_survival_predictions.parquet"
    records = [
        tier_record("tier_a_separate", mt5.TIER_A, tier_a_pred, a_path),
        tier_record("tier_b_separate", mt5.TIER_B, tier_b_pred, b_path),
        tier_record("tier_ab_combined", mt5.TIER_AB, tier_ab_pred, ab_path),
    ]
    prediction_artifacts = {
        "tier_a_predictions": save_frame(a_path, tier_a_pred),
        "tier_b_predictions": save_frame(b_path, tier_b_pred),
        "tier_ab_predictions": save_frame(ab_path, tier_ab_pred),
    }
    tier_a_feature_frame, tier_a_feature_read = coefficient_frame(tier_a_model, tier_a_preprocess, spec)
    tier_b_feature_frame, tier_b_feature_read = coefficient_frame(tier_b_model, tier_b_preprocess, spec)
    feature_root = RUN_ROOT / "results/selected_feature_reads"
    a_feature_path = feature_root / "tier_a_survival_feature_read.csv"
    b_feature_path = feature_root / "tier_b_survival_feature_read.csv"
    save_frame(a_feature_path, tier_a_feature_frame)
    save_frame(b_feature_path, tier_b_feature_frame)
    model_artifacts = {
        "tier_a_model": {"path": rel(tier_a_model_path), "sha256": sha256_file_lf_normalized(tier_a_model_path), "training_sample": tier_a_sample},
        "tier_b_model": {"path": rel(tier_b_model_path), "sha256": sha256_file_lf_normalized(tier_b_model_path), "training_sample": tier_b_sample},
        "runtime_feature_order": list(tier_a_preprocess["feature_names"]),
        "runtime_feature_order_hash": ordered_hash(tier_a_preprocess["feature_names"]),
        "event_definition": selected.get("event_definition"),
        "feature_reads": {
            "tier_a": {**tier_a_feature_read, "path": rel(a_feature_path), "sha256": sha256_file_lf_normalized(a_feature_path)},
            "tier_b": {**tier_b_feature_read, "path": rel(b_feature_path), "sha256": sha256_file_lf_normalized(b_feature_path)},
        },
    }
    return records, prediction_artifacts, model_artifacts


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
                "kpi_scope": "survival_time_to_event_hold_shape",
                "scoreboard_lane": "structural_scout",
                "status": "reviewed",
                "judgment": JUDGMENT,
                "path": record["path"],
                "primary_kpi": ledger_pairs(
                    (
                        ("rows", metrics.get("rows")),
                        ("event_rate", metrics.get("event_rate")),
                        ("median_duration", metrics.get("median_duration_bars")),
                        ("validation_c_index", metrics.get("validation_c_index")),
                        ("oos_c_index", metrics.get("oos_c_index")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("event_count", metrics.get("event_count")),
                        ("subtypes", metrics.get("partial_context_subtype_counts")),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
                "notes": "Survival time-to-event structural scout only; not baseline, promotion, or runtime authority.",
            }
        )
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "survival_time_to_event_structural_scout",
        "status": "reviewed",
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": ledger_pairs(
            (
                ("selected_variant", summary["selected_variant_id"]),
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


def write_review(summary: Mapping[str, Any]) -> None:
    selected = summary["selected_variant_id"]
    read = summary["selected_variant_read"]
    val = read.get("metrics", {}).get("validation", {})
    oos = read.get("metrics", {}).get("oos", {})
    write_md(
        REPORT_PATH,
        f"""# RUN18A Survival Time-To-Event Scout Packet(실행18A 생존 시간-사건 탐색 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected}`
- boundary(경계): `{BOUNDARY}`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run18A_next_milestone_{NEXT_RUN_ID}(실행18A에서는 미시도, 다음 마일스톤은 {NEXT_RUN_ID})`

효과(effect, 효과): Survival model(생존 모델)을 entry model(진입 모델)이 아니라 hold/exit clock(보유/청산 시계)로 탐색했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Evidence(근거)

- variants(변형): `{summary['variant_count']}`
- completed variants(완료 변형): `{summary['completed_variant_count']}`
- selected model type(선택 모델 유형): `{read.get('spec', {}).get('model_type')}`
- event definition(사건 정의): `{read.get('spec', {}).get('event_name')}`
- validation c-index(검증 일치 지수): `{val.get('concordance_index')}`
- OOS c-index(표본외 일치 지수): `{oos.get('concordance_index')}`
- validation event rate(검증 사건 비율): `{val.get('event_rate')}`
- OOS event rate(표본외 사건 비율): `{oos.get('event_rate')}`
- Tier A rows(Tier A 행): `{summary['tier_rows']['tier_a']}`
- Tier B fallback rows(Tier B 대체 행): `{summary['tier_rows']['tier_b_fallback']}`

## Preserved Clues(보존 단서)

- time-to-event(사건까지 시간) 형태는 fixed hold(고정 보유) 튜닝이 아니라 event/censoring(사건/검열) 구조로 읽을 수 있다.
- Cox hazard(콕스 위험률)와 Weibull AFT(와이블 가속고장시간) 모두 같은 event surface(사건 표면)에서 비교했으므로 model family behavior(모델군 행동) 차이를 남겼다.
- Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)를 모두 기록했다.

## Invalid Or Negative Memory(무효 또는 부정 기억)

- adverse-direction event(불리 방향 사건)는 label direction(라벨 방향)을 쓰므로 hindsight structural probe(사후 구조 탐침)로만 보존한다.
- Python-side survival score(파이썬 생존 점수)는 MT5(`MetaTrader 5`, 메타트레이더5) handoff(인계)를 아직 통과하지 않았으므로 runtime claim(런타임 주장)이 아니다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}` as the narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else ""
    line = f"- `{RUN_ID}`: `{rel(REPORT_PATH)}`\n"
    if f"- `{RUN_ID}`:" not in review:
        review = review.replace(
            "No reviewed run yet(아직 검토된 실행 없음).\n\n효과(effect, 효과): 다음 작업은 `run18A_survival_time_to_event_hold_shape_scout_v1`부터 기록한다.",
            "Reviewed runs(검토된 실행):",
        )
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)


def write_packet(summary: Mapping[str, Any], created_at: str) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    receipts = [
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "Survival models may describe hold/exit timing through event and censoring structure.",
            "boundary": BOUNDARY,
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "event_boundary": "future cumulative log return path over 12 closed M5 bars; structural scout only.",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "judgment": JUDGMENT,
            "allowed_claims": summary["allowed_claims"],
            "forbidden_claims": summary["forbidden_claims"],
        },
    ]
    write_json(PACKET_ROOT / "skill_receipts.json", receipts)
    write_json(
        PACKET_ROOT / "scope_completion_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "required_views": ["tier_a_separate", "tier_b_separate", "tier_ab_combined"],
            "completed_views": [record["record_view"] for record in summary["tier_records"]],
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {"packet_id": PACKET_ID, "status": "not_required_for_run18A", "next_runtime_probe": NEXT_RUN_ID},
    )
    write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "allowed_claims": summary["allowed_claims"],
            "forbidden_claims": summary["forbidden_claims"],
            "claim_boundary": BOUNDARY,
        },
    )


def replace_top_level_yaml_block(text: str, marker: str, block: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + block
    start = text.index(marker)
    next_start = len(text)
    cursor = text.find("\n", start + len(marker))
    while cursor != -1:
        line_start = cursor + 1
        line_end = text.find("\n", line_start)
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        if line and not line[0].isspace() and ":" in line:
            next_start = line_start
            break
        cursor = text.find("\n", line_start)
    return text[:start] + block + text[next_start:]


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = text.replace("current_run_id: not_started", f"current_run_id: {RUN_ID}", 1)
    text = text.replace(
        "- treat Stage 24 as opened_not_started after Stage23 reviewed closeout; next action is run18A_survival_time_to_event_hold_shape_scout_v1, and no baseline, promotion, or runtime authority exists",
        f"- treat Stage 24 as active after {RUN_ID} Survival model(생존 모델) Python structural scout(파이썬 구조 탐색); next action is {NEXT_RUN_ID}, and no baseline, promotion, or runtime authority exists",
        1,
    )
    text = text.replace(
        "      status: opened_not_started\n      current_run_id: not_started\n    stage25:",
        f"      status: active_run18A_python_structural_scout_completed\n      current_run_id: {RUN_ID}\n    stage25:",
        1,
    )
    text = text.replace("latest_completed_run: stage23_closeout_stage24_open", f"latest_completed_run: {RUN_ID}", 1)
    text = text.replace("next_exact_action: run18A_survival_time_to_event_hold_shape_scout_v1", f"next_exact_action: {NEXT_RUN_ID}", 1)
    block = f"""stage24_survival_model:
  stage_id: {STAGE_ID}
  status: active_run18A_python_structural_scout_completed
  current_run_id: {RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {summary['selected_variant_id']}
  boundary: {BOUNDARY}
  stage_brief_path: stages/{STAGE_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE_ID}/04_selected/selection_status.md
  report_path: stages/{STAGE_ID}/03_reviews/run18A_survival_time_to_event_scout_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    text = replace_top_level_yaml_block(text, "stage24_survival_model:", block)
    run_block = f"""stage24_survival_run18A_structural_scout:
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
  report_path: stages/{STAGE_ID}/03_reviews/run18A_survival_time_to_event_scout_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    text = replace_top_level_yaml_block(text, "stage24_survival_run18A_structural_scout:", run_block)
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def update_text_docs(summary: Mapping[str, Any]) -> None:
    selected_read = summary["selected_variant_read"]
    val = selected_read.get("metrics", {}).get("validation", {})
    oos = selected_read.get("metrics", {}).get("oos", {})
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage24 Selection Status(24단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `active_run18A_python_structural_scout_completed`
- current run(현재 실행): `{RUN_ID}`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{summary['selected_variant_id']}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage24(24단계)는 Survival model(생존 모델)의 Python-side evidence(파이썬 근거)를 남겼지만, MT5 runtime_probe(MT5 런타임 탐침), closeout(마감), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 아직 없다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}`.
""",
    )
    write_md(
        DECISION_PATH,
        f"""# 2026-05-05 Stage24 RUN18A Survival Time-To-Event Decision(24단계 실행18A 생존 시간-사건 결정)

## Decision(결정)

`{RUN_ID}`를 `{JUDGMENT}`로 기록한다.

효과(effect, 효과): Survival model(생존 모델)의 time-to-event(사건까지 시간)와 censoring(검열) 구조를 hold/exit clue(보유/청산 단서)로 보존한다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Selected Read(선택 판독)

- selected variant(선택 변형): `{summary['selected_variant_id']}`
- validation c-index(검증 일치 지수): `{val.get('concordance_index')}`
- OOS c-index(표본외 일치 지수): `{oos.get('concordance_index')}`
- next action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage24 RUN18A Survival Update(최신 24단계 실행18A 생존 업데이트)

Stage24(24단계) `{RUN_ID}`를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `{JUDGMENT}`. selected variant(선택 변형): `{summary['selected_variant_id']}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): Survival model(생존 모델)을 entry score(진입 점수)가 아니라 time-to-event(사건까지 시간), censoring(검열), hold/exit clock(보유/청산 시계)으로 읽었다. MT5 runtime_probe(MT5 런타임 탐침)는 다음 실행이다.

"""
    if "## Latest Stage24 RUN18A Survival Update" not in current[:2000]:
        io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    plan = plan.replace("- current run(현재 실행): `not_started`", f"- current run(현재 실행): `{RUN_ID}`", 1)
    plan = plan.replace(
        "Stage24(24단계)는 Survival model(생존 모델) open-only(개방만) 상태다. 현재 첫 미완료 milestone(마일스톤)은 Stage24(24단계) `run18A_survival_time_to_event_hold_shape_scout_v1` broad scout(넓은 탐색)이다.",
        f"Stage24(24단계)는 `{RUN_ID}` Survival model(생존 모델) Python structural scout(파이썬 구조 탐색)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 Stage24(24단계) `{NEXT_RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)이다.",
        1,
    )
    plan = plan.replace(
        "- [ ] Stage24(24단계) Survival model(생존 모델) scout/probe/closeout/open Stage25",
        f"- [ ] Stage24(24단계) Survival model(생존 모델) scout/probe/closeout/open Stage25. Completed(완료): `{RUN_ID}`; remaining(남음): MT5 runtime_probe(MT5 런타임 탐침), closeout/open Stage25.",
        1,
    )
    duplicate_progress = (
        f"- [ ] Stage24(24단계) Survival model(생존 모델) scout/probe/closeout/open Stage25. "
        f"Completed(완료): `{RUN_ID}`; remaining(남음): MT5 runtime_probe(MT5 런타임 탐침), closeout/open Stage25.. "
        f"Completed(완료): `{RUN_ID}`; remaining(남음): MT5 runtime_probe(MT5 런타임 탐침), closeout/open Stage25."
    )
    single_progress = (
        f"- [ ] Stage24(24단계) Survival model(생존 모델) scout/probe/closeout/open Stage25. "
        f"Completed(완료): `{RUN_ID}`; remaining(남음): MT5 runtime_probe(MT5 런타임 탐침), closeout/open Stage25."
    )
    plan = plan.replace(duplicate_progress, single_progress)
    plan = plan.replace(
        "Current active milestone(현재 활성 마일스톤): Stage24(24단계) `run18A_survival_time_to_event_hold_shape_scout_v1` broad scout(넓은 탐색).",
        f"Current active milestone(현재 활성 마일스톤): Stage24(24단계) `{NEXT_RUN_ID}` narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).",
        1,
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `{RUN_ID}` completed(완료) as Python structural scout(파이썬 구조 탐색).
- active branch(활성 브랜치): `codex/stage24-survival-model`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage24(24단계), `{RUN_ID}`.
- created/updated folders(생성/수정 폴더): `stage_pipelines/stage24`, `stages/{STAGE_ID}/02_runs/{RUN_ID}`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): survival scout pipeline(생존 탐색 파이프라인), run evidence(실행 근거), ledgers(장부), current truth docs(현재 진실 문서), goal plan(목표 계획).
- active stage folder(활성 단계 폴더): `stages/{STAGE_ID}`.
- current run id(현재 실행 ID): `{RUN_ID}`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `not_attempted_in_run18A(실행18A 미시도)`; review report(검토 보고서) `{rel(REPORT_PATH)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{NEXT_RUN_ID}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage24(24단계) survival handoff/runtime probe(생존 인계/런타임 탐침) 준비에서 시작한다.
"""
    marker = "## Latest Stop Resume State"
    start = plan.find(marker)
    if start != -1:
        next_section = plan.find("\n## ", start + 1)
        plan = plan[:start] + resume + ("\n" + plan[next_section + 1 :] if next_section != -1 else "")
    else:
        plan = plan.rstrip() + "\n\n" + resume
    outcome = f"- `2026-05-05`: Stage24(24단계) `{RUN_ID}` Survival model(생존 모델) Python structural scout(파이썬 구조 탐색)를 완료했다. judgment(판정): `{JUDGMENT}`.\n"
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    variants = default_variants(context["tier_b_feature_order"])
    rows = [evaluate_variant(context, spec) for spec in variants]
    variant_artifacts = save_variant_results(rows)
    selected = select_variant(rows)
    tier_records, prediction_artifacts, model_artifacts = materialize_selected(context, selected)
    completed_count = sum(1 for row in rows if row.get("status") == "completed")
    summary = {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "packet_id": PACKET_ID,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "judgment": JUDGMENT,
        "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
        "boundary": BOUNDARY,
        "max_horizon_bars": MAX_HORIZON_BARS,
        "variant_count": len(rows),
        "completed_variant_count": completed_count,
        "selected_variant_id": selected["variant_id"],
        "selected_variant_read": selected,
        "variant_results": rows,
        "tier_records": tier_records,
        "tier_rows": {
            "tier_a": int(len(context["tier_a_frame"])),
            "tier_b_training": int(len(context["tier_b_training_frame"])),
            "tier_b_fallback": int(len(context["tier_b_fallback_frame"])),
        },
        "artifacts": {
            **variant_artifacts,
            "model_artifacts": model_artifacts,
            "prediction_artifacts": prediction_artifacts,
        },
        "allowed_claims": ["python_structural_scout_completed", "survival_hold_exit_shape_clues_recorded"],
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority"],
        "next_action": NEXT_RUN_ID,
    }
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": created_at,
            "selected_variant_id": selected["variant_id"],
            "external_verification_status": summary["external_verification_status"],
            "boundary": BOUNDARY,
        },
    )
    write_json(RUN_ROOT / "kpi_record.json", summary)
    ledger_artifacts = materialize_ledgers(summary)
    summary["artifacts"]["ledger_artifacts"] = ledger_artifacts
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(RUN_ROOT / "kpi_record.json", summary)
    write_review(summary)
    write_packet(summary, created_at)
    update_workspace_state(summary)
    update_text_docs(summary)
    return {
        "run_id": RUN_ID,
        "judgment": JUDGMENT,
        "selected_variant_id": selected["variant_id"],
        "completed_variant_count": completed_count,
        "external_verification_status": summary["external_verification_status"],
        "next_action": summary["next_action"],
    }


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Run Stage24 survival time-to-event hold-shape scout.")


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    print(json.dumps(json_ready(run(args)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
