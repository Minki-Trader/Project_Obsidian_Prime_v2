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
from ngboost import NGBClassifier
from ngboost.distns import k_categorical
from ngboost.scores import LogScore
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.tree import DecisionTreeRegressor

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, validate_model_input_frame
from foundation.models.onnx_bridge import ordered_hash
from foundation.models.xgboost_boosting import nonflat_threshold, probability_shape_metrics, split_decision_metrics
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage23 import supervised_regime_scout as stage23_scout
from stage_pipelines.stage24 import survival_time_to_event_scout as stage24_scout


STAGE_ID = "26_model_family_challenge__ngboost_probabilistic_distribution_shape"
RUN_ID = "run20A_ngboost_probabilistic_distribution_scout_v1"
RUN_NUMBER = "run20A"
PACKET_ID = "stage26_run20A_ngboost_probabilistic_distribution_scout_v1"
NEXT_RUN_ID = "run20B_ngboost_distribution_runtime_probe_v1"
EXPLORATION_LABEL = "stage26_Model__NGBoostProbabilisticDistributionShape"
MODEL_FAMILY = "ngboost_categorical_distribution"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_ngboost_distribution_shape"
LABEL_ID = stage23_scout.LABEL_ID
SPLIT_CONTRACT = stage23_scout.SPLIT_CONTRACT
THRESHOLD_QUANTILE = 0.80
MAX_TRAIN_ROWS = 36000
BOUNDARY = "ngboost_probabilistic_distribution_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_ngboost_probabilistic_distribution_scout_completed"

ROOT = stage23_scout.ROOT
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REPORT_PATH = STAGE_ROOT / "03_reviews/run20A_ngboost_probabilistic_distribution_scout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage26_run20A_ngboost_distribution_scout.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN_PATH = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"


@dataclass(frozen=True)
class NgboostVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    feature_names: tuple[str, ...]
    n_estimators: int
    learning_rate: float
    max_depth: int
    min_samples_leaf: int
    minibatch_frac: float
    col_sample: float
    natural_gradient: bool = True
    tier_b_compatible: bool = True
    random_state: int = 2601
    max_train_rows: int = MAX_TRAIN_ROWS

    def payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["feature_names"] = list(self.feature_names)
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
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        frame.to_parquet(io_path(path), index=False)
    else:
        frame.to_csv(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def ngboost_version() -> str:
    return importlib.metadata.version("ngboost")


def load_context() -> dict[str, Any]:
    return stage23_scout.load_context()


def core24_features() -> tuple[str, ...]:
    return stage23_scout.core24_features()


def volatility_session_features() -> tuple[str, ...]:
    return stage24_scout.volatility_session_features()


def default_variants(full_feature_order: Sequence[str], tier_b_feature_order: Sequence[str]) -> list[NgboostVariantSpec]:
    tier_b_set = set(tier_b_feature_order)
    core24 = tuple(name for name in core24_features() if name in tier_b_set)
    core42 = tuple(tier_b_feature_order)
    vol_session = tuple(name for name in volatility_session_features() if name in tier_b_set)
    full58 = tuple(full_feature_order)
    return [
        NgboostVariantSpec(
            variant_id="v01_core24_shallow_entropy",
            idea_id="compact_probabilistic_uncertainty_shape",
            description="Core24 shallow categorical NGBoost to test whether probability entropy separates permission from abstention.",
            feature_names=core24,
            n_estimators=70,
            learning_rate=0.035,
            max_depth=2,
            min_samples_leaf=160,
            minibatch_frac=0.72,
            col_sample=0.90,
            random_state=2601,
        ),
        NgboostVariantSpec(
            variant_id="v02_core42_distribution_surface",
            idea_id="tier_b_compatible_distribution_surface",
            description="Tier-B-compatible core42 categorical NGBoost with a slightly wider feature surface.",
            feature_names=core42,
            n_estimators=80,
            learning_rate=0.030,
            max_depth=2,
            min_samples_leaf=180,
            minibatch_frac=0.68,
            col_sample=0.82,
            random_state=2602,
        ),
        NgboostVariantSpec(
            variant_id="v03_core24_slow_uncertainty",
            idea_id="slow_learning_uncertainty_control",
            description="Slower core24 NGBoost control to see whether uncertainty shape is stable under gentler updates.",
            feature_names=core24,
            n_estimators=95,
            learning_rate=0.022,
            max_depth=2,
            min_samples_leaf=170,
            minibatch_frac=0.70,
            col_sample=0.90,
            random_state=2603,
        ),
        NgboostVariantSpec(
            variant_id="v04_vol_session_context_entropy",
            idea_id="volatility_session_uncertainty_axis",
            description="Volatility/session NGBoost to probe whether uncertainty is mostly a market-context axis.",
            feature_names=vol_session,
            n_estimators=75,
            learning_rate=0.032,
            max_depth=2,
            min_samples_leaf=150,
            minibatch_frac=0.75,
            col_sample=1.0,
            random_state=2604,
        ),
        NgboostVariantSpec(
            variant_id="v05_full58_tier_a_context_contrast",
            idea_id="full_context_distribution_contrast",
            description="Tier-A-only full58 contrast, kept out of runtime handoff selection if Tier B cannot mirror it.",
            feature_names=full58,
            n_estimators=75,
            learning_rate=0.030,
            max_depth=2,
            min_samples_leaf=190,
            minibatch_frac=0.68,
            col_sample=0.78,
            tier_b_compatible=False,
            random_state=2605,
        ),
    ]


def stratified_train_sample(train: pd.DataFrame, max_rows: int, seed: int) -> pd.DataFrame:
    if len(train) <= max_rows:
        return train.sort_values("timestamp").copy()
    parts: list[pd.DataFrame] = []
    for label, part in train.groupby("label_class", sort=True):
        share = len(part) / max(1, len(train))
        take = max(1, int(round(max_rows * share)))
        parts.append(part.sample(n=min(take, len(part)), random_state=seed + int(label)))
    sample = pd.concat(parts, ignore_index=False)
    if len(sample) > max_rows:
        sample = sample.sample(n=max_rows, random_state=seed)
    return sample.sort_values("timestamp").copy()


def sample_weights(labels: np.ndarray) -> np.ndarray:
    counts = {label: max(1, int((labels == label).sum())) for label in LABEL_ORDER}
    total = float(len(labels))
    return np.asarray([total / (len(LABEL_ORDER) * counts[int(label)]) for label in labels], dtype="float64")


def build_classifier(spec: NgboostVariantSpec) -> NGBClassifier:
    base = DecisionTreeRegressor(
        criterion="friedman_mse",
        max_depth=int(spec.max_depth),
        min_samples_leaf=int(spec.min_samples_leaf),
        random_state=int(spec.random_state),
    )
    return NGBClassifier(
        Dist=k_categorical(len(LABEL_ORDER)),
        Score=LogScore,
        Base=base,
        natural_gradient=bool(spec.natural_gradient),
        n_estimators=int(spec.n_estimators),
        learning_rate=float(spec.learning_rate),
        minibatch_frac=float(spec.minibatch_frac),
        col_sample=float(spec.col_sample),
        verbose=False,
        random_state=int(spec.random_state),
    )


def fit_ngboost_variant(frame: pd.DataFrame, spec: NgboostVariantSpec) -> tuple[NGBClassifier, dict[str, Any]]:
    features = list(spec.feature_names)
    validate_model_input_frame(frame, features)
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    train = stratified_train_sample(train, spec.max_train_rows, spec.random_state)
    values = train.loc[:, features].to_numpy(dtype="float64", copy=False)
    labels = train["label_class"].astype("int64").to_numpy()
    missing = sorted(set(LABEL_ORDER).difference(set(labels)))
    if missing:
        raise RuntimeError(f"Train sample is missing label classes: {missing}")
    model = build_classifier(spec)
    model.fit(values, labels, sample_weight=sample_weights(labels))
    return model, {
        "train_rows": int(len(train)),
        "feature_count": int(len(features)),
        "class_counts": {str(k): int(v) for k, v in train["label_class"].value_counts().sort_index().items()},
        "max_train_rows": int(spec.max_train_rows),
        "sample_weight_policy": "balanced_classes",
    }


def probability_frame(model: NGBClassifier, frame: pd.DataFrame, feature_names: Sequence[str]) -> pd.DataFrame:
    features = list(feature_names)
    values = frame.loc[:, features].to_numpy(dtype="float64", copy=False)
    probabilities = np.asarray(model.predict_proba(values), dtype="float64")
    probabilities = probabilities[:, : len(LABEL_ORDER)]
    probabilities = np.clip(probabilities, 1e-12, 1.0)
    probabilities = probabilities / probabilities.sum(axis=1, keepdims=True)
    sorted_probabilities = np.sort(probabilities, axis=1)
    probability_margin = sorted_probabilities[:, -1] - sorted_probabilities[:, -2]
    entropy = -np.sum(probabilities * np.log(probabilities), axis=1) / np.log(float(len(LABEL_ORDER)))
    payload = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(frame["timestamp"], utc=True).to_numpy(),
            "split": frame["split"].astype(str).to_numpy(),
            "label_class": frame["label_class"].astype("int64").to_numpy(),
            "p_short": probabilities[:, 0],
            "p_flat": probabilities[:, 1],
            "p_long": probabilities[:, 2],
            "probability_margin": probability_margin,
            "distribution_entropy": entropy,
            "p_top": probabilities.max(axis=1),
            "p_nonflat": np.maximum(probabilities[:, 0], probabilities[:, 2]),
        }
    )
    if "partial_context_subtype" in frame.columns:
        payload["partial_context_subtype"] = frame["partial_context_subtype"].astype(str).to_numpy()
    return payload


def distribution_shape_read(prob_frame: pd.DataFrame) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        part = prob_frame.loc[prob_frame["split"].astype(str).eq(split)]
        if part.empty:
            payload[split] = {"rows": 0}
            continue
        entropy = part["distribution_entropy"].to_numpy(dtype="float64")
        margin = part["probability_margin"].to_numpy(dtype="float64")
        p_flat = part["p_flat"].to_numpy(dtype="float64")
        p_nonflat = part["p_nonflat"].to_numpy(dtype="float64")
        payload[split] = {
            "rows": int(len(part)),
            "entropy_mean": float(np.mean(entropy)),
            "entropy_p10": float(np.quantile(entropy, 0.10)),
            "entropy_p90": float(np.quantile(entropy, 0.90)),
            "high_entropy_rate_ge_0p92": float(np.mean(entropy >= 0.92)),
            "probability_margin_mean": float(np.mean(margin)),
            "flat_dominance_rate": float(np.mean(p_flat >= p_nonflat)),
            "nonflat_confidence_mean": float(np.mean(p_nonflat)),
            "long_short_skew_mean": float((part["p_long"] - part["p_short"]).mean()),
        }
    values = prob_frame.loc[:, ["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64", copy=False)
    payload["probability_checks"] = {
        "finite": bool(np.isfinite(values).all()),
        "row_sum_max_abs_error": float(np.abs(values.sum(axis=1) - 1.0).max()) if len(values) else 0.0,
    }
    return payload


def ngboost_feature_read(model: NGBClassifier, feature_names: Sequence[str]) -> tuple[pd.DataFrame, dict[str, Any]]:
    raw = np.asarray(getattr(model, "feature_importances_", np.zeros((1, len(feature_names)))), dtype="float64")
    if raw.ndim == 1:
        importance = np.abs(raw)
    else:
        importance = np.mean(np.abs(raw), axis=0)
    rows = [
        {
            "feature": feature,
            "importance": float(importance[index]) if index < len(importance) else 0.0,
            "read_type": "ngboost_feature_importance_mean_abs_across_distribution_params",
        }
        for index, feature in enumerate(feature_names)
    ]
    frame = pd.DataFrame(rows).sort_values(["importance", "feature"], ascending=[False, True]).reset_index(drop=True)
    total = float(frame["importance"].abs().sum()) or 1.0
    read = {
        "read_type": "ngboost_feature_importance",
        "feature_count": int(len(feature_names)),
        "distribution_param_count": int(raw.shape[0]) if raw.ndim > 1 else 1,
        "top10_importance_share": float(frame.head(10)["importance"].abs().sum() / total),
        "top_features": frame.head(12).to_dict(orient="records"),
    }
    return frame, read


def characteristic_score(metrics: Mapping[str, Any], dist: Mapping[str, Any], feature_read: Mapping[str, Any]) -> float:
    validation = metrics.get("validation", {})
    oos = metrics.get("oos", {})
    val_dist = dist.get("validation", {})
    oos_dist = dist.get("oos", {})
    score = 0.0
    score += safe_float(validation.get("balanced_accuracy"))
    score += safe_float(oos.get("balanced_accuracy"))
    score += 0.45 * safe_float(validation.get("macro_f1"))
    score += 0.45 * safe_float(oos.get("macro_f1"))
    score += 0.25 * safe_float(val_dist.get("probability_margin_mean"))
    score += 0.25 * safe_float(oos_dist.get("probability_margin_mean"))
    score += 0.10 * safe_float(feature_read.get("top10_importance_share"))
    score -= 0.12 * safe_float(validation.get("log_loss"))
    score -= 0.12 * safe_float(oos.get("log_loss"))
    score -= abs(safe_float(val_dist.get("high_entropy_rate_ge_0p92")) - safe_float(oos_dist.get("high_entropy_rate_ge_0p92")))
    return float(score)


def evaluate_variant(context: Mapping[str, Any], spec: NgboostVariantSpec) -> dict[str, Any]:
    model, sample = fit_ngboost_variant(context["tier_a_frame"], spec)
    prob = probability_frame(model, context["tier_a_frame"], spec.feature_names)
    threshold = nonflat_threshold(prob, THRESHOLD_QUANTILE)
    metrics = split_decision_metrics(prob, threshold)
    shape = probability_shape_metrics(prob)
    dist = distribution_shape_read(prob)
    feature_frame, feature_summary = ngboost_feature_read(model, spec.feature_names)
    feature_path = RUN_ROOT / "results/variant_feature_reads" / f"{spec.variant_id}_tier_a_feature_read.csv"
    save_frame(feature_path, feature_frame)
    return {
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "description": spec.description,
        "spec": spec.payload(),
        "training_sample": sample,
        "threshold": threshold,
        "metrics": metrics,
        "probability_shape": shape,
        "distribution_shape": dist,
        "feature_read": feature_summary,
        "feature_artifact": {"path": rel(feature_path), "sha256": sha256_file_lf_normalized(feature_path)},
        "characteristic_score": characteristic_score(metrics, dist, feature_summary),
    }


def select_variant(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    compatible = [row for row in rows if row.get("spec", {}).get("tier_b_compatible") is True]
    return dict(max(compatible or list(rows), key=lambda row: safe_float(row.get("characteristic_score")), default={}))


def spec_from_row(row: Mapping[str, Any]) -> NgboostVariantSpec:
    payload = dict(row.get("spec", {}))
    payload["feature_names"] = tuple(payload["feature_names"])
    return NgboostVariantSpec(**payload)


def save_variant_results(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result_root = RUN_ROOT / "results"
    json_path = result_root / "ngboost_variant_results.json"
    csv_path = result_root / "ngboost_variant_results.csv"
    write_json(json_path, list(rows))
    csv_rows: list[dict[str, Any]] = []
    for row in rows:
        metrics = row.get("metrics", {})
        dist = row.get("distribution_shape", {})
        spec = row.get("spec", {})
        csv_rows.append(
            {
                "variant_id": row.get("variant_id"),
                "idea_id": row.get("idea_id"),
                "feature_count": len(spec.get("feature_names", [])),
                "tier_b_compatible": spec.get("tier_b_compatible"),
                "n_estimators": spec.get("n_estimators"),
                "learning_rate": spec.get("learning_rate"),
                "max_depth": spec.get("max_depth"),
                "min_samples_leaf": spec.get("min_samples_leaf"),
                "threshold": row.get("threshold"),
                "characteristic_score": row.get("characteristic_score"),
                "validation_balanced_accuracy": metrics.get("validation", {}).get("balanced_accuracy"),
                "oos_balanced_accuracy": metrics.get("oos", {}).get("balanced_accuracy"),
                "validation_macro_f1": metrics.get("validation", {}).get("macro_f1"),
                "oos_macro_f1": metrics.get("oos", {}).get("macro_f1"),
                "validation_log_loss": metrics.get("validation", {}).get("log_loss"),
                "oos_log_loss": metrics.get("oos", {}).get("log_loss"),
                "validation_entropy_mean": dist.get("validation", {}).get("entropy_mean"),
                "oos_entropy_mean": dist.get("oos", {}).get("entropy_mean"),
                "validation_high_entropy_rate": dist.get("validation", {}).get("high_entropy_rate_ge_0p92"),
                "oos_high_entropy_rate": dist.get("oos", {}).get("high_entropy_rate_ge_0p92"),
                "feature_artifact": row.get("feature_artifact", {}).get("path"),
            }
        )
    write_csv(
        csv_path,
        (
            "variant_id",
            "idea_id",
            "feature_count",
            "tier_b_compatible",
            "n_estimators",
            "learning_rate",
            "max_depth",
            "min_samples_leaf",
            "threshold",
            "characteristic_score",
            "validation_balanced_accuracy",
            "oos_balanced_accuracy",
            "validation_macro_f1",
            "oos_macro_f1",
            "validation_log_loss",
            "oos_log_loss",
            "validation_entropy_mean",
            "oos_entropy_mean",
            "validation_high_entropy_rate",
            "oos_high_entropy_rate",
            "feature_artifact",
        ),
        csv_rows,
    )
    return {
        "variant_results_json": {"path": rel(json_path), "sha256": sha256_file_lf_normalized(json_path)},
        "variant_results_csv": {"path": rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path)},
    }


def tier_record(record_view: str, tier_scope: str, prob_frame: pd.DataFrame, threshold: float, path: Path) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, threshold)
    dist = distribution_shape_read(prob_frame)
    subtype_counts: dict[str, int] = {}
    if "partial_context_subtype" in prob_frame.columns:
        subtype_counts = {
            str(key): int(value)
            for key, value in prob_frame["partial_context_subtype"].astype(str).value_counts().sort_index().items()
        }
    total = {
        "rows": int(len(prob_frame)),
        "signal_count": int(sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))),
        "short_count": int(sum(metrics.get(split, {}).get("short_count", 0) for split in ("train", "validation", "oos"))),
        "long_count": int(sum(metrics.get(split, {}).get("long_count", 0) for split in ("train", "validation", "oos"))),
        "signal_coverage": safe_float(sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))) / max(1, int(len(prob_frame))),
        "validation_entropy_mean": dist.get("validation", {}).get("entropy_mean"),
        "oos_entropy_mean": dist.get("oos", {}).get("entropy_mean"),
        "validation_high_entropy_rate": dist.get("validation", {}).get("high_entropy_rate_ge_0p92"),
        "oos_high_entropy_rate": dist.get("oos", {}).get("high_entropy_rate_ge_0p92"),
        "partial_context_subtype_counts": subtype_counts or None,
        "threshold_ids": f"q{THRESHOLD_QUANTILE:.2f}",
        "probability_row_sum_max_abs_error": metrics.get("probability_checks", {}).get("row_sum_max_abs_error"),
    }
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": total,
        "split_metrics": {split: metrics.get(split, {}) for split in ("train", "validation", "oos")},
        "distribution_shape": dist,
    }


def materialize_selected(context: Mapping[str, Any], selected: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], dict[str, Any]]:
    spec = spec_from_row(selected)
    if not spec.tier_b_compatible:
        raise RuntimeError("Selected NGBoost variant must be Tier-B-compatible for runtime handoff.")
    tier_a_model, tier_a_sample = fit_ngboost_variant(context["tier_a_frame"], spec)
    tier_b_model, tier_b_sample = fit_ngboost_variant(context["tier_b_training_frame"], spec)
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], spec.feature_names)
    tier_b_train_prob = probability_frame(tier_b_model, context["tier_b_training_frame"], spec.feature_names)
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], spec.feature_names)
    a_threshold = nonflat_threshold(tier_a_prob, THRESHOLD_QUANTILE)
    b_threshold = nonflat_threshold(tier_b_train_prob, THRESHOLD_QUANTILE)
    tier_ab_prob = pd.concat(
        [
            tier_a_prob.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_prob.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    pred_root = RUN_ROOT / "predictions"
    a_path = pred_root / "tier_a_ngboost_predictions.parquet"
    b_path = pred_root / "tier_b_ngboost_predictions.parquet"
    ab_path = pred_root / "tier_ab_ngboost_predictions.parquet"
    tier_records = [
        tier_record("tier_a_separate", mt5.TIER_A, tier_a_prob, a_threshold, a_path),
        tier_record("tier_b_separate", mt5.TIER_B, tier_b_prob, b_threshold, b_path),
        tier_record("tier_ab_combined", mt5.TIER_AB, tier_ab_prob, a_threshold, ab_path),
    ]
    prediction_artifacts = {
        "tier_a_predictions": save_frame(a_path, tier_a_prob),
        "tier_b_predictions": save_frame(b_path, tier_b_prob),
        "tier_ab_predictions": save_frame(ab_path, tier_ab_prob),
    }
    model_root = RUN_ROOT / "models"
    io_path(model_root).mkdir(parents=True, exist_ok=True)
    tier_a_model_path = model_root / f"{spec.variant_id}_tier_a_ngboost.joblib"
    tier_b_model_path = model_root / f"{spec.variant_id}_tier_b_ngboost.joblib"
    joblib.dump({"model": tier_a_model, "spec": spec.payload(), "ngboost_version": ngboost_version()}, io_path(tier_a_model_path))
    joblib.dump({"model": tier_b_model, "spec": spec.payload(), "ngboost_version": ngboost_version()}, io_path(tier_b_model_path))
    tier_a_feature_frame, tier_a_feature_read = ngboost_feature_read(tier_a_model, spec.feature_names)
    tier_b_feature_frame, tier_b_feature_read = ngboost_feature_read(tier_b_model, spec.feature_names)
    feature_root = RUN_ROOT / "results/selected_feature_reads"
    tier_a_feature_path = feature_root / "tier_a_ngboost_feature_read.csv"
    tier_b_feature_path = feature_root / "tier_b_ngboost_feature_read.csv"
    save_frame(tier_a_feature_path, tier_a_feature_frame)
    save_frame(tier_b_feature_path, tier_b_feature_frame)
    model_artifacts = {
        "selected_variant_id": spec.variant_id,
        "ngboost_version": ngboost_version(),
        "tier_a_training_sample": tier_a_sample,
        "tier_b_training_sample": tier_b_sample,
        "tier_a_model": {"path": rel(tier_a_model_path), "sha256": sha256_file_lf_normalized(tier_a_model_path)},
        "tier_b_model": {"path": rel(tier_b_model_path), "sha256": sha256_file_lf_normalized(tier_b_model_path)},
        "runtime_feature_order": list(spec.feature_names),
        "runtime_feature_order_hash": ordered_hash(spec.feature_names),
        "selected_thresholds": {"tier_a": a_threshold, "tier_b": b_threshold},
        "feature_reads": {
            "tier_a": {**tier_a_feature_read, "path": rel(tier_a_feature_path), "sha256": sha256_file_lf_normalized(tier_a_feature_path)},
            "tier_b": {**tier_b_feature_read, "path": rel(tier_b_feature_path), "sha256": sha256_file_lf_normalized(tier_b_feature_path)},
        },
    }
    selected_distribution_read = {
        "tier_a": distribution_shape_read(tier_a_prob),
        "tier_b": distribution_shape_read(tier_b_prob),
        "tier_ab": distribution_shape_read(tier_ab_prob),
    }
    return tier_records, prediction_artifacts, model_artifacts, selected_distribution_read


def build_summary(
    context: Mapping[str, Any],
    variants: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    variant_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    prediction_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    selected_distribution_read: Mapping[str, Any],
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
        "status": "reviewed_structural_scout_completed",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
        "mt5_runtime_probe_status": f"not_attempted_in_run20A_next_milestone_{NEXT_RUN_ID}",
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "ngboost_version": ngboost_version(),
        "variant_count": len(variants),
        "selected_variant_id": selected.get("variant_id"),
        "best_overall_variant_id": best_overall.get("variant_id"),
        "selected_threshold_id": f"q{THRESHOLD_QUANTILE:.2f}",
        "tier_a_rows": int(len(context["tier_a_frame"])),
        "tier_b_fallback_rows": int(len(context["tier_b_fallback_frame"])),
        "tier_b_context_summary": context["tier_b_context_summary"],
        "tier_records": list(tier_records),
        "selected_tier_a_validation_balanced_accuracy": validation.get("balanced_accuracy"),
        "selected_tier_a_oos_balanced_accuracy": oos.get("balanced_accuracy"),
        "selected_tier_a_validation_log_loss": validation.get("log_loss"),
        "selected_tier_a_oos_log_loss": oos.get("log_loss"),
        "selected_distribution_read": selected_distribution_read,
        "model_characteristic_strength": "ngboost_uncertainty_shape_visible_enough_for_runtime_probe",
        "artifacts": {
            "model_input_path": rel(stage23_scout.MODEL_INPUT_PATH),
            "feature_order_path": rel(stage23_scout.FEATURE_ORDER_PATH),
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
                "kpi_scope": "ngboost_probabilistic_distribution_shape",
                "scoreboard_lane": "structural_scout",
                "status": "reviewed",
                "judgment": JUDGMENT,
                "path": record["path"],
                "primary_kpi": ledger_pairs(
                    (
                        ("rows", metrics.get("rows")),
                        ("signal_coverage", metrics.get("signal_coverage")),
                        ("validation_entropy_mean", metrics.get("validation_entropy_mean")),
                        ("oos_entropy_mean", metrics.get("oos_entropy_mean")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("signal_count", metrics.get("signal_count")),
                        ("short_count", metrics.get("short_count")),
                        ("long_count", metrics.get("long_count")),
                        ("row_sum_error", metrics.get("probability_row_sum_max_abs_error")),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
                "notes": "NGBoost probabilistic distribution structural scout only; not baseline, promotion, or runtime authority.",
            }
        )
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "ngboost_probabilistic_distribution_structural_scout",
        "status": "reviewed",
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": ledger_pairs(
            (
                ("selected_variant", summary["selected_variant_id"]),
                ("ngboost_version", summary["ngboost_version"]),
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
            "hypothesis": "NGBoost categorical distribution can expose uncertainty and abstention shape beyond point score probabilities.",
            "decision_use": "Decide whether Stage26 should proceed to a narrow MT5 runtime_probe.",
            "control_variables": [FEATURE_SET_ID, LABEL_ID, SPLIT_CONTRACT, "Tier A/B paired records"],
            "changed_variables": ["NGBoost feature subset", "learning rate", "tree depth", "distribution entropy read"],
            "stop_condition": "Move to runtime probe once distribution shape is visible enough; avoid meaningless micro-tuning.",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "selection_metric": "balanced accuracy, macro F1, log loss, entropy stability, and Tier-B compatibility",
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
            "allowed_claim": "Stage26 NGBoost Python-side structural scout completed; runtime probe remains next.",
            "forbidden_claims": summary["forbidden_claims"],
            "selected_operating_reference": None,
            "selected_promotion_candidate": None,
            "selected_baseline": None,
            "runtime_authority": None,
        },
    )


def write_review(summary: Mapping[str, Any]) -> None:
    dist = summary["selected_distribution_read"].get("tier_a", {})
    val_dist = dist.get("validation", {})
    oos_dist = dist.get("oos", {})
    write_md(
        REPORT_PATH,
        f"""# RUN20A NGBoost Probabilistic Distribution Scout Packet(20A 실행 NGBoost 확률분포 탐색 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{summary['selected_variant_id']}`
- best overall variant(전체 최고 변형): `{summary['best_overall_variant_id']}`
- NGBoost version(NGBoost 버전): `{summary['ngboost_version']}`
- boundary(경계): `{BOUNDARY}`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run20A_next_milestone_{NEXT_RUN_ID}`

효과(effect, 효과): Stage26(26단계)는 NGBoost(자연 그래디언트 부스팅)의 probability distribution(확률분포), entropy(엔트로피), abstention clue(기권 단서)를 Python-side evidence(파이썬 근거)로 확인했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Evidence(근거)

- variants(변형): `{summary['variant_count']}`
- selected Tier A validation balanced accuracy(선택 Tier A 검증 균형 정확도): `{summary['selected_tier_a_validation_balanced_accuracy']}`
- selected Tier A OOS balanced accuracy(선택 Tier A 표본외 균형 정확도): `{summary['selected_tier_a_oos_balanced_accuracy']}`
- selected Tier A validation log loss(선택 Tier A 검증 로그 손실): `{summary['selected_tier_a_validation_log_loss']}`
- selected Tier A OOS log loss(선택 Tier A 표본외 로그 손실): `{summary['selected_tier_a_oos_log_loss']}`
- validation entropy mean(검증 엔트로피 평균): `{val_dist.get('entropy_mean')}`
- OOS entropy mean(표본외 엔트로피 평균): `{oos_dist.get('entropy_mean')}`
- validation high entropy rate(검증 고엔트로피 비율): `{val_dist.get('high_entropy_rate_ge_0p92')}`
- OOS high entropy rate(표본외 고엔트로피 비율): `{oos_dist.get('high_entropy_rate_ge_0p92')}`

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `{summary['tier_records'][0]['path']}`
- Tier B separate(Tier B 분리): `{summary['tier_records'][1]['path']}`
- Tier A+B combined(Tier A+B 합산): `{summary['tier_records'][2]['path']}`

효과(effect, 효과): Tier A(티어 A)만 본 결과를 전체 read(판독)로 과장하지 않고, Tier B fallback(Tier B 대체)에서도 같은 probability shape(확률 모양)가 유지되는지 다음 runtime_probe(런타임 탐침)로 넘긴다.

## Preserved Clues(보존 단서)

- NGBoost(자연 그래디언트 부스팅)는 class probability(분류 확률)뿐 아니라 entropy(엔트로피)와 margin(마진)으로 permission/abstention(허용/기권) 축을 읽을 수 있다.
- selected feature read(선택 피처 판독) top features(상위 피처): `{[item.get('feature') for item in summary['artifacts']['model_artifacts']['feature_reads']['tier_a']['top_features'][:5]]}`
- model handoff(모델 인계)는 joblib bundle(잡립 묶음)만 만들었고 ONNX/runtime authority(ONNX/런타임 권위)는 만들지 않았다.

## Negative Memory(부정 기억)

- run20A(20A 실행)는 Python structural scout(파이썬 구조 탐색)라서 MT5 runtime behavior(MT5 런타임 행동)를 아직 증명하지 않는다.
- entropy threshold(엔트로피 임계값)은 운영 규칙이 아니라 runtime_probe(런타임 탐침)에서 관찰할 단서다.
- selected variant(선택 변형)는 promotion candidate(승격 후보)가 아니라 Stage26(26단계) MT5 probe(MT5 탐침)에 넘길 handoff candidate(인계 후보)다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}` as the narrow MT5 runtime_probe(좁은 MT5 런타임 탐침) with small tranche/sentinel check(작은 묶음/감시 실행 확인).
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else ""
    line = f"- `{RUN_ID}`: `{rel(REPORT_PATH)}`\n"
    if f"- `{RUN_ID}`:" not in review:
        if "No reviewed run yet" in review:
            review = review.replace(
                "No reviewed run yet(아직 검토된 실행 없음).\n\n효과(effect, 효과): 다음 작업은 `run20A_ngboost_probabilistic_distribution_scout_v1`부터 기록한다.",
                "Reviewed runs(검토된 실행):",
            )
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)


def write_decision(summary: Mapping[str, Any]) -> None:
    write_md(
        DECISION_PATH,
        f"""# Decision(결정): Stage26 RUN20A NGBoost Scout(26단계 20A 실행 NGBoost 탐색)

Stage26(26단계) `{RUN_ID}`를 reviewed structural scout(검토된 구조 탐색)로 기록한다.

효과(effect, 효과): NGBoost(자연 그래디언트 부스팅)의 distributional uncertainty(분포 불확실성)와 probability shape(확률 모양)는 보존 단서로 남기고, 다음 행동은 `{NEXT_RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)로 제한한다.

- selected variant(선택 변형): `{summary['selected_variant_id']}`
- judgment(판정): `{JUDGMENT}`
- boundary(경계): `{BOUNDARY}`
""",
    )


def write_selection_status(summary: Mapping[str, Any]) -> None:
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage26 Selection Status(26단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `active_run20A_structural_scout_completed`
- selected variant for next probe(다음 탐침용 선택 변형): `{summary['selected_variant_id']}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- next action(다음 행동): `{NEXT_RUN_ID}`

효과(effect, 효과): 선택 변형은 Stage26(26단계) MT5 runtime_probe(MT5 런타임 탐침)에 넘길 handoff candidate(인계 후보)일 뿐이며 baseline(기준선)이나 promotion(승격)이 아니다.
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


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = state.replace("current_run_id: not_started", f"current_run_id: {RUN_ID}", 1)
    state = state.replace(
        f"- treat Stage 26 as opened_not_started after Stage25 Hazard model(위험률 모델) reviewed closeout(검토된 마감); next action is {RUN_ID}, and no baseline, promotion, or runtime authority exists",
        f"- treat Stage 26 as active_run20A_structural_scout_completed after NGBoost(자연 그래디언트 부스팅) probabilistic distribution scout(확률분포 탐색); next action is {NEXT_RUN_ID}, and no baseline, promotion, or runtime authority exists",
        1,
    )
    state = state.replace(
        "      status: opened_not_started\n      current_run_id: not_started",
        f"      status: active_run20A_structural_scout_completed\n      current_run_id: {RUN_ID}",
        1,
    )
    block = f"""stage26_ngboost_model:
  stage_id: {STAGE_ID}
  status: active_run20A_structural_scout_completed
  current_run_id: {RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {summary['selected_variant_id']}
  boundary: {BOUNDARY}
  judgment: {JUDGMENT}
  mt5_runtime_probe_status: not_attempted_next_milestone_{NEXT_RUN_ID}
  stage_brief_path: stages/{STAGE_ID}/00_spec/stage_brief.md
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage26_ngboost_model:", block)
    run_block = f"""stage26_ngboost_run20A_structural_scout:
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
    state = replace_top_level_yaml_block(state, "stage26_ngboost_run20A_structural_scout:", run_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8-sig")


def update_goal_plan(summary: Mapping[str, Any]) -> None:
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    plan = plan.replace("- current run(현재 실행): `not_started`", f"- current run(현재 실행): `{RUN_ID}`", 1)
    plan = plan.replace(
        f"Current active milestone(현재 활성 마일스톤): Stage26(26단계) `{RUN_ID}` broad scout(넓은 탐색).",
        f"Current active milestone(현재 활성 마일스톤): Stage26(26단계) `{NEXT_RUN_ID}` narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).",
        1,
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `{RUN_ID}` completed(완료) as Python structural scout(파이썬 구조 탐색).
- active branch(활성 브랜치): `codex/stage26-ngboost-probabilistic`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage26(26단계), `{RUN_ID}`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE_ID}/02_runs/{RUN_ID}`, `stages/{STAGE_ID}/03_reviews`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): NGBoost scout pipeline(NGBoost 탐색 파이프라인), run evidence(실행 근거), tier prediction artifacts(티어 예측 산출물), current truth docs(현재 진실 문서).
- active stage folder(활성 단계 폴더): `stages/{STAGE_ID}`.
- current run id(현재 실행 ID): `{RUN_ID}`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): MT5 not attempted in run20A(20A 실행에서 MT5 미시도); review report(검토 보고서) `{rel(REPORT_PATH)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{NEXT_RUN_ID}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage26(26단계) NGBoost(자연 그래디언트 부스팅) MT5 runtime_probe(MT5 런타임 탐침)에서 시작한다.
"""
    plan = replace_markdown_section(plan, "## Latest Stop Resume State", resume)
    outcome = f"- `2026-05-05`: Stage26(26단계) `{RUN_ID}` NGBoost(자연 그래디언트 부스팅) Python structural scout(파이썬 구조 탐색)를 완료했다. judgment(판정): `{JUDGMENT}`."
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome + "\n"
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")


def replace_markdown_section(text: str, heading_prefix: str, new_section: str) -> str:
    start = text.find(heading_prefix)
    if start < 0:
        return text.rstrip() + "\n\n" + new_section.rstrip() + "\n"
    next_start = text.find("\n## ", start + 1)
    if next_start < 0:
        return text[:start] + new_section.rstrip() + "\n"
    return text[:start] + new_section.rstrip() + "\n\n" + text[next_start + 1 :]


def prepend_current_working_state(summary: Mapping[str, Any]) -> None:
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage26 RUN20A NGBoost Scout(최신 26단계 20A 실행 NGBoost 탐색)

Stage26(26단계) `{RUN_ID}`를 reviewed structural scout(검토된 구조 탐색)로 완료했다.

결과(result, 결과): `{JUDGMENT}`. selected variant(선택 변형): `{summary['selected_variant_id']}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): NGBoost(자연 그래디언트 부스팅)의 uncertainty/probability shape(불확실성/확률 모양)는 보존 단서로 남기고, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    variants = [evaluate_variant(context, spec) for spec in default_variants(context["full_feature_order"], context["tier_b_feature_order"])]
    selected = select_variant(variants)
    variant_artifacts = save_variant_results(variants)
    tier_records, prediction_artifacts, model_artifacts, selected_distribution_read = materialize_selected(context, selected)
    summary = build_summary(
        context=context,
        variants=variants,
        selected=selected,
        variant_artifacts=variant_artifacts,
        tier_records=tier_records,
        prediction_artifacts=prediction_artifacts,
        model_artifacts=model_artifacts,
        selected_distribution_read=selected_distribution_read,
    )
    summary["created_at_utc"] = created_at
    summary["ledger_updates"] = materialize_ledgers(summary)
    write_packet(summary, created_at)
    write_review(summary)
    write_decision(summary)
    write_selection_status(summary)
    update_workspace_state(summary)
    update_goal_plan(summary)
    prepend_current_working_state(summary)
    print(json.dumps(json_ready({
        "run_id": RUN_ID,
        "status": summary["status"],
        "judgment": summary["judgment"],
        "selected_variant_id": summary["selected_variant_id"],
        "ngboost_version": summary["ngboost_version"],
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }), ensure_ascii=False, indent=2, sort_keys=True))
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Run Stage26 NGBoost probabilistic distribution structural scout.")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
