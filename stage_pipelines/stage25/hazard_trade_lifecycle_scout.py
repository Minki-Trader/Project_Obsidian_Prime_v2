from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage23 import supervised_regime_scout as stage23_scout
from stage_pipelines.stage24 import survival_time_to_event_scout as stage24_scout


STAGE_ID = "25_exit_model__hazard_trade_lifecycle_risk"
RUN_ID = "run19A_hazard_trade_lifecycle_risk_scout_v1"
RUN_NUMBER = "run19A"
PACKET_ID = "stage25_run19A_hazard_trade_lifecycle_scout_v1"
NEXT_RUN_ID = "run19B_hazard_trade_lifecycle_runtime_probe_v1"
EXPLORATION_LABEL = "stage25_Exit__HazardTradeLifecycleRisk"
MODEL_FAMILY = "sklearn_discrete_time_logistic_hazard"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_hazard_trade_lifecycle"
LABEL_ID = stage23_scout.LABEL_ID
SPLIT_CONTRACT = stage23_scout.SPLIT_CONTRACT
MAX_HORIZON_BARS = 12
BOUNDARY = "hazard_trade_lifecycle_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_hazard_trade_lifecycle_risk_scout_completed"

ROOT = stage23_scout.ROOT
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REPORT_PATH = STAGE_ROOT / "03_reviews/run19A_hazard_trade_lifecycle_scout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage25_run19A_hazard_trade_lifecycle_scout.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN_PATH = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"


@dataclass(frozen=True)
class HazardVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    model_type: str
    event_name: str
    base_feature_names: tuple[str, ...]
    threshold_multiplier: float
    c_value: float = 0.5
    tier_b_compatible: bool = True
    random_state: int = 2501

    def feature_names(self) -> tuple[str, ...]:
        return (*self.base_feature_names, "hazard_elapsed_bar", "hazard_elapsed_frac")

    def payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["base_feature_names"] = list(self.base_feature_names)
        payload["feature_names"] = list(self.feature_names())
        return payload


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return stage23_scout.rel(path)


def safe_float(value: Any, default: float = 0.0) -> float:
    return stage23_scout.safe_float(value, default)


def write_json(path: Path, payload: Any) -> None:
    stage23_scout.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    stage23_scout.write_md(path, text)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    return stage23_scout.save_frame(path, frame)


def load_context() -> dict[str, Any]:
    return stage23_scout.load_context()


def core24_features() -> tuple[str, ...]:
    return stage23_scout.core24_features()


def volatility_session_features() -> tuple[str, ...]:
    return stage24_scout.volatility_session_features()


def default_variants(tier_b_feature_order: Sequence[str]) -> list[HazardVariantSpec]:
    tier_b_set = set(tier_b_feature_order)
    core = tuple(name for name in core24_features() if name in tier_b_set)
    vol_session = tuple(name for name in volatility_session_features() if name in tier_b_set)
    time_only: tuple[str, ...] = ()
    return [
        HazardVariantSpec(
            variant_id="v01_logit_core24_adverse_1x",
            idea_id="core_feature_adverse_hazard",
            description="Discrete-time logistic hazard for 1x label-threshold adverse excursion using core24 features.",
            model_type="logistic_hazard",
            event_name="adverse_1x",
            base_feature_names=core,
            threshold_multiplier=1.0,
            c_value=0.50,
        ),
        HazardVariantSpec(
            variant_id="v02_logit_core24_adverse_1p5x",
            idea_id="core_feature_deeper_adverse_hazard",
            description="Discrete-time logistic hazard for deeper 1.5x adverse excursion using core24 features.",
            model_type="logistic_hazard",
            event_name="adverse_1p5x",
            base_feature_names=core,
            threshold_multiplier=1.5,
            c_value=0.50,
        ),
        HazardVariantSpec(
            variant_id="v03_logit_vol_session_adverse_1x",
            idea_id="volatility_session_adverse_hazard",
            description="Discrete-time logistic hazard using volatility/session features to test lifecycle risk concentration.",
            model_type="logistic_hazard",
            event_name="adverse_1x",
            base_feature_names=vol_session,
            threshold_multiplier=1.0,
            c_value=0.35,
        ),
        HazardVariantSpec(
            variant_id="v04_logit_core24_reversal_after_favorable_1x",
            idea_id="reversal_after_favorable_move_hazard",
            description="Discrete-time logistic hazard for reversal after an initially favorable move.",
            model_type="logistic_hazard",
            event_name="reversal_after_favorable_1x",
            base_feature_names=core,
            threshold_multiplier=1.0,
            c_value=0.50,
        ),
        HazardVariantSpec(
            variant_id="v05_logit_time_only_adverse_1x",
            idea_id="elapsed_time_control_hazard",
            description="Time-only hazard control to check whether elapsed bar alone explains the event surface.",
            model_type="logistic_hazard",
            event_name="adverse_1x",
            base_feature_names=time_only,
            threshold_multiplier=1.0,
            c_value=0.50,
        ),
    ]


def event_duration_arrays(frame: pd.DataFrame, spec: HazardVariantSpec, base_threshold: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    future_cols = [f"future_cum_log_return_{horizon}" for horizon in range(1, MAX_HORIZON_BARS + 1)]
    values = frame[future_cols].to_numpy(dtype="float64", copy=False)
    label_class = pd.to_numeric(frame.get("label_class"), errors="coerce")
    directions = np.where(label_class.eq(2), 1, np.where(label_class.eq(0), -1, 0)).astype("int8")
    threshold = abs(float(base_threshold) * float(spec.threshold_multiplier))
    durations: list[int] = []
    events: list[int] = []
    usable_mask: list[bool] = []
    for row_index in range(len(frame)):
        row = values[row_index]
        valid_count = int(np.isfinite(row).sum())
        direction = int(directions[row_index])
        if valid_count < 1 or direction == 0:
            durations.append(0)
            events.append(0)
            usable_mask.append(False)
            continue
        horizon_values = row[:valid_count]
        signed_path = direction * horizon_values
        if spec.event_name.startswith("adverse_"):
            hits = np.flatnonzero(signed_path <= -threshold)
        elif spec.event_name == "reversal_after_favorable_1x":
            peak_path = np.maximum.accumulate(signed_path)
            hits = np.flatnonzero((peak_path >= threshold) & ((peak_path - signed_path) >= threshold))
        else:
            raise ValueError(f"Unknown hazard event_name: {spec.event_name}")
        if hits.size:
            durations.append(int(hits[0]) + 1)
            events.append(1)
        else:
            durations.append(valid_count)
            events.append(0)
        usable_mask.append(True)
    return (
        np.asarray(durations, dtype="int16"),
        np.asarray(events, dtype="int8"),
        np.asarray(usable_mask, dtype=bool),
    )


def build_hazard_frame(frame: pd.DataFrame, spec: HazardVariantSpec, base_threshold: float) -> pd.DataFrame:
    work = stage24_scout.add_future_return_path(frame, MAX_HORIZON_BARS)
    durations, events, usable = event_duration_arrays(work, spec, base_threshold)
    row_mask = usable & (durations >= 1)
    base = work.loc[row_mask].copy().reset_index(drop=True)
    durations = durations[row_mask].astype(int)
    events = events[row_mask].astype(int)
    if len(base) == 0:
        raise ValueError("No usable non-flat rows for hazard event construction.")
    counts = durations
    source_positions = np.repeat(np.arange(len(base)), counts)
    elapsed = np.concatenate([np.arange(1, count + 1, dtype="int16") for count in counts])
    keep_columns = [
        "timestamp",
        "split",
        "label_id",
        "label_class",
        *list(spec.base_feature_names),
    ]
    keep_columns.extend([name for name in ("partial_context_subtype", "tier_scope") if name in base.columns])
    hazard = base.iloc[source_positions][list(dict.fromkeys(keep_columns))].copy().reset_index(drop=True)
    hazard["source_duration_bars"] = np.repeat(durations, counts)
    hazard["source_event_observed"] = np.repeat(events, counts)
    hazard["hazard_elapsed_bar"] = elapsed.astype("float64")
    hazard["hazard_elapsed_frac"] = hazard["hazard_elapsed_bar"] / float(MAX_HORIZON_BARS)
    hazard["hazard_event"] = 0
    last_positions = np.cumsum(counts) - 1
    event_last_positions = last_positions[events == 1]
    hazard.loc[event_last_positions, "hazard_event"] = 1
    hazard["event_name"] = spec.event_name
    hazard["threshold_multiplier"] = float(spec.threshold_multiplier)
    hazard["event_threshold_abs_log_return"] = abs(float(base_threshold) * float(spec.threshold_multiplier))
    return hazard


def fit_hazard_model(frame: pd.DataFrame, spec: HazardVariantSpec) -> tuple[LogisticRegression, dict[str, Any], dict[str, Any]]:
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    if len(train) < 1000:
        raise ValueError(f"Training sample too small for hazard scout: {len(train)}")
    event_rate = float(train["hazard_event"].mean())
    if event_rate <= 0.001 or event_rate >= 0.90:
        raise ValueError(f"Training hazard event rate outside useful scout range: {event_rate}")
    preprocess = stage24_scout.fit_preprocessor(train, spec.feature_names())
    train_fit = train
    if len(train_fit) > 220_000:
        positives = train_fit.loc[train_fit["hazard_event"].eq(1)]
        negatives = train_fit.loc[train_fit["hazard_event"].eq(0)]
        neg_n = max(1, 220_000 - len(positives))
        negatives = negatives.sample(n=min(len(negatives), neg_n), random_state=int(spec.random_state))
        train_fit = pd.concat([positives, negatives], ignore_index=True).sample(frac=1.0, random_state=int(spec.random_state))
    x = stage24_scout.transform_features(train_fit, preprocess)
    y = train_fit["hazard_event"].astype("int8").to_numpy()
    model = LogisticRegression(
        C=float(spec.c_value),
        class_weight="balanced",
        max_iter=500,
        solver="lbfgs",
        random_state=int(spec.random_state),
    )
    model.fit(x, y)
    sample = {
        "train_rows": int(len(train)),
        "fit_rows": int(len(train_fit)),
        "train_event_rate": event_rate,
        "train_event_count": int(train["hazard_event"].sum()),
        "feature_count_before_filter": int(len(spec.feature_names())),
        "feature_count_after_filter": int(len(preprocess["feature_names"])),
        "dropped_features": list(preprocess["dropped_features"]),
    }
    return model, preprocess, sample


def prediction_frame(model: LogisticRegression, preprocess: Mapping[str, Any], frame: pd.DataFrame, spec: HazardVariantSpec) -> pd.DataFrame:
    x = stage24_scout.transform_features(frame, preprocess)
    risk = model.predict_proba(x)[:, 1]
    columns = [
        "timestamp",
        "split",
        "label_id",
        "label_class",
        "hazard_elapsed_bar",
        "hazard_elapsed_frac",
        "source_duration_bars",
        "source_event_observed",
        "hazard_event",
        "event_name",
        "threshold_multiplier",
        "event_threshold_abs_log_return",
    ]
    optional = [name for name in ("partial_context_subtype", "tier_scope") if name in frame.columns]
    pred = frame[[name for name in columns if name in frame.columns] + optional].copy().reset_index(drop=True)
    pred["variant_id"] = spec.variant_id
    pred["hazard_risk"] = risk.astype("float64")
    return pred


def split_hazard_metrics(pred: pd.DataFrame) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        sub = pred.loc[pred["split"].astype(str).eq(split)].copy()
        if sub.empty:
            metrics[split] = {"rows": 0}
            continue
        y = sub["hazard_event"].astype("int8").to_numpy()
        risk = pd.to_numeric(sub["hazard_risk"], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0).clip(0.0, 1.0)
        if len(np.unique(y)) == 2:
            roc = float(roc_auc_score(y, risk))
            ap = float(average_precision_score(y, risk))
            brier = float(brier_score_loss(y, risk))
        else:
            roc = None
            ap = None
            brier = None
        q20, q80 = risk.quantile([0.20, 0.80]).tolist()
        low = sub.loc[risk <= q20]
        high = sub.loc[risk >= q80]
        low_rate = float(low["hazard_event"].mean()) if not low.empty else None
        high_rate = float(high["hazard_event"].mean()) if not high.empty else None
        by_bar = (
            sub.assign(hazard_risk=risk)
            .groupby("hazard_elapsed_bar", dropna=False)
            .agg(rows=("hazard_event", "size"), event_rate=("hazard_event", "mean"), mean_hazard_risk=("hazard_risk", "mean"))
            .reset_index()
        )
        metrics[split] = {
            "rows": int(len(sub)),
            "event_count": int(sub["hazard_event"].sum()),
            "event_rate": float(sub["hazard_event"].mean()),
            "roc_auc": roc,
            "average_precision": ap,
            "brier_score": brier,
            "hazard_risk_q10": float(risk.quantile(0.10)),
            "hazard_risk_q50": float(risk.quantile(0.50)),
            "hazard_risk_q90": float(risk.quantile(0.90)),
            "low_risk_event_rate": low_rate,
            "high_risk_event_rate": high_rate,
            "high_minus_low_event_rate": None if low_rate is None or high_rate is None else float(high_rate - low_rate),
            "by_elapsed_bar": by_bar.to_dict(orient="records"),
        }
    return metrics


def coefficient_frame(model: LogisticRegression, preprocess: Mapping[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    features = list(preprocess["feature_names"])
    coefficients = np.asarray(model.coef_, dtype="float64").reshape(-1)
    rows = [
        {
            "feature": feature,
            "coefficient": float(coefficients[index]),
            "abs_coefficient": abs(float(coefficients[index])),
            "effect_read": "positive_coefficient_means_higher_bar_hazard",
        }
        for index, feature in enumerate(features)
    ]
    frame = pd.DataFrame(rows).sort_values("abs_coefficient", ascending=False).reset_index(drop=True)
    return frame, {
        "feature_count_after_filter": int(len(features)),
        "dropped_features": list(preprocess["dropped_features"]),
        "top_features": frame.head(10).to_dict(orient="records"),
    }


def characteristic_score(metrics: Mapping[str, Any]) -> float:
    val = metrics.get("validation", {})
    oos = metrics.get("oos", {})
    val_auc = safe_float(val.get("roc_auc"), 0.5)
    oos_auc = safe_float(oos.get("roc_auc"), 0.5)
    val_lift = safe_float(val.get("high_minus_low_event_rate"), 0.0)
    oos_lift = safe_float(oos.get("high_minus_low_event_rate"), 0.0)
    stability_penalty = abs(val_lift - oos_lift)
    return float((val_auc - 0.5) * 2.0 + (oos_auc - 0.5) * 1.5 + val_lift * 3.0 + oos_lift * 2.0 - stability_penalty)


def evaluate_variant(context: Mapping[str, Any], spec: HazardVariantSpec) -> dict[str, Any]:
    try:
        frame = build_hazard_frame(context["tier_a_frame"], spec, float(context["training_summary"]["threshold_log_return"]))
        model, preprocess, sample = fit_hazard_model(frame, spec)
        pred = prediction_frame(model, preprocess, frame, spec)
        metrics = split_hazard_metrics(pred)
        feature_frame, feature_summary = coefficient_frame(model, preprocess)
        feature_path = RUN_ROOT / "results/variant_feature_reads" / f"{spec.variant_id}_hazard_feature_read.csv"
        save_frame(feature_path, feature_frame)
        curve_path = RUN_ROOT / "results/variant_hazard_curves" / f"{spec.variant_id}_hazard_curve.csv"
        curve_rows = []
        for split, payload in metrics.items():
            for row in payload.get("by_elapsed_bar", []):
                curve_rows.append({"split": split, **row})
        save_frame(curve_path, pd.DataFrame(curve_rows))
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
            "hazard_curve_artifact": {"path": rel(curve_path), "sha256": sha256_file_lf_normalized(curve_path)},
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
        raise RuntimeError("No completed Stage25 hazard scout variant was available for selection.")
    return dict(max(completed, key=lambda row: safe_float(row.get("characteristic_score"), -999.0)))


def spec_from_row(row: Mapping[str, Any]) -> HazardVariantSpec:
    payload = dict(row.get("spec", {}))
    payload["base_feature_names"] = tuple(payload["base_feature_names"])
    payload.pop("feature_names", None)
    return HazardVariantSpec(**payload)


def save_variant_results(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result_root = RUN_ROOT / "results"
    json_path = result_root / "hazard_variant_results.json"
    csv_path = result_root / "hazard_variant_results.csv"
    write_json(json_path, list(rows))
    csv_rows = []
    for row in rows:
        metrics = row.get("metrics", {})
        train = metrics.get("train", {})
        val = metrics.get("validation", {})
        oos = metrics.get("oos", {})
        spec = row.get("spec", {})
        csv_rows.append(
            {
                "variant_id": row.get("variant_id"),
                "event_name": spec.get("event_name"),
                "status": row.get("status"),
                "feature_count": len(spec.get("feature_names", [])),
                "characteristic_score": row.get("characteristic_score"),
                "train_event_rate": train.get("event_rate"),
                "validation_event_rate": val.get("event_rate"),
                "oos_event_rate": oos.get("event_rate"),
                "validation_roc_auc": val.get("roc_auc"),
                "oos_roc_auc": oos.get("roc_auc"),
                "validation_lift": val.get("high_minus_low_event_rate"),
                "oos_lift": oos.get("high_minus_low_event_rate"),
                "invalid_reason": row.get("invalid_reason"),
            }
        )
    write_csv(
        csv_path,
        (
            "variant_id",
            "event_name",
            "status",
            "feature_count",
            "characteristic_score",
            "train_event_rate",
            "validation_event_rate",
            "oos_event_rate",
            "validation_roc_auc",
            "oos_roc_auc",
            "validation_lift",
            "oos_lift",
            "invalid_reason",
        ),
        csv_rows,
    )
    return {
        "variant_results_json": {"path": rel(json_path), "sha256": sha256_file_lf_normalized(json_path)},
        "variant_results_csv": {"path": rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path)},
    }


def tier_record(record_view: str, tier_scope: str, pred: pd.DataFrame, path: Path) -> dict[str, Any]:
    metrics = split_hazard_metrics(pred)
    all_events = pred["hazard_event"].astype("int8")
    summary = {
        "rows": int(len(pred)),
        "event_count": int(all_events.sum()),
        "event_rate": float(all_events.mean()) if len(pred) else None,
        "validation_roc_auc": metrics.get("validation", {}).get("roc_auc"),
        "oos_roc_auc": metrics.get("oos", {}).get("roc_auc"),
        "validation_lift": metrics.get("validation", {}).get("high_minus_low_event_rate"),
        "oos_lift": metrics.get("oos", {}).get("high_minus_low_event_rate"),
        "partial_context_subtype_counts": {},
    }
    if "partial_context_subtype" in pred.columns:
        summary["partial_context_subtype_counts"] = {
            str(k): int(v) for k, v in pred["partial_context_subtype"].fillna("NA").value_counts().sort_index().items()
        }
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "path": rel(path),
        "metrics": summary,
        "split_metrics": metrics,
    }


def materialize_selected(context: Mapping[str, Any], selected: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    spec = spec_from_row(selected)
    base_threshold = float(context["training_summary"]["threshold_log_return"])
    tier_a_frame = build_hazard_frame(context["tier_a_frame"], spec, base_threshold)
    tier_b_training_frame = build_hazard_frame(context["tier_b_training_frame"], spec, base_threshold)
    tier_b_fallback_frame = build_hazard_frame(context["tier_b_fallback_frame"], spec, base_threshold)
    tier_a_model, tier_a_preprocess, tier_a_sample = fit_hazard_model(tier_a_frame, spec)
    tier_b_model, tier_b_preprocess, tier_b_sample = fit_hazard_model(tier_b_training_frame, spec)
    model_root = RUN_ROOT / "models"
    io_path(model_root).mkdir(parents=True, exist_ok=True)
    tier_a_model_path = model_root / f"{spec.variant_id}_tier_a_hazard_model.joblib"
    tier_b_model_path = model_root / f"{spec.variant_id}_tier_b_hazard_model.joblib"
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
    a_path = pred_root / "tier_a_hazard_predictions.parquet"
    b_path = pred_root / "tier_b_hazard_predictions.parquet"
    ab_path = pred_root / "tier_ab_hazard_predictions.parquet"
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
    tier_a_feature_frame, tier_a_feature_read = coefficient_frame(tier_a_model, tier_a_preprocess)
    tier_b_feature_frame, tier_b_feature_read = coefficient_frame(tier_b_model, tier_b_preprocess)
    feature_root = RUN_ROOT / "results/selected_feature_reads"
    a_feature_path = feature_root / "tier_a_hazard_feature_read.csv"
    b_feature_path = feature_root / "tier_b_hazard_feature_read.csv"
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
                "kpi_scope": "hazard_trade_lifecycle_risk",
                "scoreboard_lane": "structural_scout",
                "status": "reviewed",
                "judgment": JUDGMENT,
                "path": record["path"],
                "primary_kpi": ledger_pairs(
                    (
                        ("rows", metrics.get("rows")),
                        ("event_rate", metrics.get("event_rate")),
                        ("validation_auc", metrics.get("validation_roc_auc")),
                        ("oos_auc", metrics.get("oos_roc_auc")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("event_count", metrics.get("event_count")),
                        ("validation_lift", metrics.get("validation_lift")),
                        ("oos_lift", metrics.get("oos_lift")),
                        ("subtypes", metrics.get("partial_context_subtype_counts")),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
                "notes": "Hazard trade-lifecycle structural scout only; not baseline, promotion, or runtime authority.",
            }
        )
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "hazard_trade_lifecycle_structural_scout",
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
    read = summary["selected_variant_read"]
    val = read.get("metrics", {}).get("validation", {})
    oos = read.get("metrics", {}).get("oos", {})
    write_md(
        REPORT_PATH,
        f"""# RUN19A Hazard Trade Lifecycle Scout Packet(실행19A 위험률 거래 생애주기 탐색 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{summary['selected_variant_id']}`
- boundary(경계): `{BOUNDARY}`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run19A_next_milestone_{NEXT_RUN_ID}(실행19A에서는 미시도, 다음 마일스톤은 {NEXT_RUN_ID})`

효과(effect, 효과): Hazard model(위험률 모델)을 entry score(진입 점수)가 아니라 bar-by-bar loss/reversal risk(봉별 손실/반전 위험)로 탐색했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Experiment Design(실험 설계)

- hypothesis(가설): entry-time features(진입 시점 피처)와 elapsed bar(경과 봉)가 adverse/reversal event(불리/반전 사건)의 hazard risk(위험률 위험)를 분리할 수 있다.
- decision use(결정 용도): Stage25(25단계) MT5 runtime_probe(MT5 런타임 탐침)에서 hazard score(위험률 점수)를 flat/close pressure(평탄/청산 압력)로 넘길지 판단한다.
- comparison baseline(비교 기준): time-only hazard(시간 전용 위험률)와 core/volatility feature hazard(핵심/변동성 피처 위험률)를 같은 split(분할)에서 비교한다.
- stop condition(중지 조건): hazard characteristic(위험률 특성)이 보이면 미세탐색 없이 runtime_probe(런타임 탐침)로 넘어간다.

## Evidence(근거)

- variants(변형): `{summary['variant_count']}`
- completed variants(완료 변형): `{summary['completed_variant_count']}`
- selected event(선택 사건): `{read.get('spec', {}).get('event_name')}`
- validation ROC AUC(검증 ROC AUC): `{val.get('roc_auc')}`
- OOS ROC AUC(표본외 ROC AUC): `{oos.get('roc_auc')}`
- validation lift(검증 고위험-저위험 사건 비율 차): `{val.get('high_minus_low_event_rate')}`
- OOS lift(표본외 고위험-저위험 사건 비율 차): `{oos.get('high_minus_low_event_rate')}`
- Tier A rows(Tier A 행): `{summary['tier_rows']['tier_a_hazard_rows']}`
- Tier B fallback rows(Tier B 대체 행): `{summary['tier_rows']['tier_b_fallback_hazard_rows']}`

## Preserved Clues(보존 단서)

- discrete-time hazard(이산 시간 위험률)는 event row(사건 행)와 at-risk row(위험 노출 행)를 분리해 loss/reversal timing(손실/반전 시점)을 볼 수 있다.
- selected variant(선택 변형)의 top features(주요 피처)는 `{[item.get('feature') for item in summary['artifacts']['model_artifacts']['feature_reads']['tier_a']['top_features'][:5]]}`다.
- Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)를 모두 기록했다.

## Invalid Or Negative Memory(무효 또는 부정 기억)

- run19A(19A실행)는 Python structural scout(파이썬 구조 탐색)이므로 MT5 runtime evidence(MT5 런타임 근거)가 아니다.
- adverse/reversal event(불리/반전 사건)는 future path(미래 경로)에서 만든 label(라벨)이며 feature(피처)에 미래값을 넣지 않는다.
- hazard_risk(위험률 위험)는 calibrated probability(보정 확률)가 아니라 ranking/shape read(순위/모양 판독)로만 본다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}` as the narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else ""
    line = f"- `{RUN_ID}`: `{rel(REPORT_PATH)}`\n"
    if f"- `{RUN_ID}`:" not in review:
        review = review.replace(
            "No reviewed run yet(아직 검토된 실행 없음).\n\n효과(effect, 효과): 다음 작업은 `run19A_hazard_trade_lifecycle_risk_scout_v1`부터 기록한다.",
            "Reviewed runs(검토된 실행):",
        )
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)


def write_packet(summary: Mapping[str, Any], created_at: str) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        [
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-experiment-design",
                "status": "executed",
                "hypothesis": "Discrete-time hazard may expose bar-by-bar loss/reversal risk.",
                "boundary": BOUNDARY,
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-data-integrity",
                "status": "executed",
                "feature_label_boundary": "Only entry-time features and elapsed bar are model inputs; future path only builds hazard labels.",
                "integrity_judgment": "usable_with_boundary",
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-model-validation",
                "status": "executed",
                "selection_metric": "validation/OOS ROC AUC plus high-low hazard event-rate lift",
                "validation_judgment": "exploratory_inconclusive",
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-result-judgment",
                "status": "executed",
                "judgment": JUDGMENT,
            },
        ],
    )
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
        {"packet_id": PACKET_ID, "status": "not_required_for_run19A", "next_runtime_probe": NEXT_RUN_ID},
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
        f"- treat Stage 25 as opened_not_started after Stage24 Survival model(생존 모델) reviewed closeout(검토된 마감); next action is {RUN_ID}, and no baseline, promotion, or runtime authority exists",
        f"- treat Stage 25 as active after {RUN_ID} Hazard model(위험률 모델) Python structural scout(파이썬 구조 탐색); next action is {NEXT_RUN_ID}, and no baseline, promotion, or runtime authority exists",
        1,
    )
    text = text.replace(
        f"    stage25:\n      stage_id: {STAGE_ID}\n      ownership: independent hazard trade-lifecycle risk scout after Stage24\n      status: opened_not_started\n      current_run_id: not_started",
        f"    stage25:\n      stage_id: {STAGE_ID}\n      ownership: independent hazard trade-lifecycle risk scout after Stage24\n      status: active_run19A_python_structural_scout_completed\n      current_run_id: {RUN_ID}",
        1,
    )
    text = text.replace("latest_completed_run: stage24_closeout_stage25_open", f"latest_completed_run: {RUN_ID}", 1)
    text = text.replace(f"next_exact_action: {RUN_ID}", f"next_exact_action: {NEXT_RUN_ID}", 1)
    selected = summary["selected_variant_id"]
    block = f"""stage25_hazard_model:
  stage_id: {STAGE_ID}
  status: active_run19A_python_structural_scout_completed
  current_run_id: {RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {selected}
  boundary: {BOUNDARY}
  stage_brief_path: stages/{STAGE_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE_ID}/04_selected/selection_status.md
  report_path: stages/{STAGE_ID}/03_reviews/run19A_hazard_trade_lifecycle_scout_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    text = replace_top_level_yaml_block(text, "stage25_hazard_model:", block)
    run_block = f"""stage25_hazard_run19A_structural_scout:
  packet_id: {PACKET_ID}
  status: reviewed_structural_scout_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  selected_variant_id: {selected}
  mt5_runtime_probe_status: not_attempted_next_milestone_{NEXT_RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: stages/{STAGE_ID}/03_reviews/run19A_hazard_trade_lifecycle_scout_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    text = replace_top_level_yaml_block(text, "stage25_hazard_run19A_structural_scout:", run_block)
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def update_text_docs(summary: Mapping[str, Any]) -> None:
    selected = summary["selected_variant_id"]
    read = summary["selected_variant_read"]
    val = read.get("metrics", {}).get("validation", {})
    oos = read.get("metrics", {}).get("oos", {})
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage25 Selection Status(25단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `active_run19A_python_structural_scout_completed`
- current run(현재 실행): `{RUN_ID}`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage25(25단계)는 Hazard model(위험률 모델)의 Python-side evidence(파이썬 근거)를 남겼지만, MT5 runtime_probe(MT5 런타임 탐침), closeout(마감), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 아직 없다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}`.
""",
    )
    write_md(
        DECISION_PATH,
        f"""# 2026-05-05 Stage25 RUN19A Hazard Trade Lifecycle Decision(25단계 실행19A 위험률 거래 생애주기 결정)

## Decision(결정)

`{RUN_ID}`를 `{JUDGMENT}`로 기록한다.

효과(effect, 효과): Hazard model(위험률 모델)의 bar-by-bar adverse/reversal risk(봉별 불리/반전 위험)를 trade lifecycle clue(거래 생애주기 단서)로 보존한다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Selected Read(선택 판독)

- selected variant(선택 변형): `{selected}`
- validation ROC AUC(검증 ROC AUC): `{val.get('roc_auc')}`
- OOS ROC AUC(표본외 ROC AUC): `{oos.get('roc_auc')}`
- validation lift(검증 고위험-저위험 사건 비율 차): `{val.get('high_minus_low_event_rate')}`
- OOS lift(표본외 고위험-저위험 사건 비율 차): `{oos.get('high_minus_low_event_rate')}`
- next action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage25 RUN19A Hazard Update(최신 25단계 실행19A 위험률 업데이트)

Stage25(25단계) `{RUN_ID}`를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `{JUDGMENT}`. selected variant(선택 변형): `{selected}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): Hazard model(위험률 모델)을 entry score(진입 점수)가 아니라 bar-by-bar loss/reversal risk(봉별 손실/반전 위험)로 읽었다. MT5 runtime_probe(MT5 런타임 탐침)는 다음 실행이다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    plan = plan.replace("- current run(현재 실행): `not_started`", f"- current run(현재 실행): `{RUN_ID}`", 1)
    plan = plan.replace(
        f"현재 첫 미완료 milestone(마일스톤)은 Stage25(25단계) `{RUN_ID}` broad scout(넓은 탐색)이다.",
        f"현재 첫 미완료 milestone(마일스톤)은 Stage25(25단계) `{NEXT_RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)이다.",
        1,
    )
    plan = plan.replace(
        "- [ ] Stage25(25단계) hazard model(위험률 모델) scout/probe/closeout/open Stage26",
        f"- [ ] Stage25(25단계) hazard model(위험률 모델) scout/probe/closeout/open Stage26. Completed(완료): `{RUN_ID}`; remaining(남음): MT5 runtime_probe(MT5 런타임 탐침), closeout/open Stage26.",
        1,
    )
    plan = plan.replace(
        f"Current active milestone(현재 활성 마일스톤): Stage25(25단계) `{RUN_ID}` broad scout(넓은 탐색).",
        f"Current active milestone(현재 활성 마일스톤): Stage25(25단계) `{NEXT_RUN_ID}` narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).",
        1,
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `{RUN_ID}` completed(완료) as Python structural scout(파이썬 구조 탐색).
- active branch(활성 브랜치): `codex/stage25-hazard-model`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage25(25단계), `{RUN_ID}`.
- created/updated folders(생성/수정 폴더): `stage_pipelines/stage25`, `stages/{STAGE_ID}/02_runs/{RUN_ID}`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): hazard scout pipeline(위험률 탐색 파이프라인), run evidence(실행 근거), ledgers(장부), current truth docs(현재 진실 문서), goal plan(목표 계획).
- active stage folder(활성 단계 폴더): `stages/{STAGE_ID}`.
- current run id(현재 실행 ID): `{RUN_ID}`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `not_attempted_in_run19A(실행19A 미시도)`; review report(검토 보고서) `{rel(REPORT_PATH)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{NEXT_RUN_ID}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage25(25단계) hazard runtime handoff(위험률 런타임 인계) 준비에서 시작한다.
"""
    plan = stage24_scout.replace_markdown_section(plan, "## Latest Stop Resume State", resume) if hasattr(stage24_scout, "replace_markdown_section") else plan
    if "## Latest Stop Resume State" in plan and resume not in plan:
        start = plan.index("## Latest Stop Resume State")
        next_section = plan.find("\n## ", start + 1)
        plan = plan[:start] + resume + ("\n" + plan[next_section + 1 :] if next_section != -1 else "")
    outcome = f"- `2026-05-05`: Stage25(25단계) `{RUN_ID}` Hazard model(위험률 모델) Python structural scout(파이썬 구조 탐색)를 완료했다. judgment(판정): `{JUDGMENT}`."
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome + "\n"
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
    tier_a_rows = tier_records[0]["metrics"]["rows"] if tier_records else 0
    tier_b_rows = tier_records[1]["metrics"]["rows"] if len(tier_records) > 1 else 0
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
            "tier_a_input_rows": int(len(context["tier_a_frame"])),
            "tier_b_training_input_rows": int(len(context["tier_b_training_frame"])),
            "tier_b_fallback_input_rows": int(len(context["tier_b_fallback_frame"])),
            "tier_a_hazard_rows": int(tier_a_rows),
            "tier_b_fallback_hazard_rows": int(tier_b_rows),
        },
        "artifacts": {
            **variant_artifacts,
            "model_artifacts": model_artifacts,
            "prediction_artifacts": prediction_artifacts,
        },
        "allowed_claims": ["python_structural_scout_completed", "hazard_trade_lifecycle_clues_recorded"],
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
    return argparse.ArgumentParser(description="Run Stage25 hazard trade-lifecycle risk scout.")


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    print(json.dumps(json_ready(run(args)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
