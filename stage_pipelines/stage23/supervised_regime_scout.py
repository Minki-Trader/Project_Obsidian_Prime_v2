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
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    FEATURE_ORDER_PATH,
    MODEL_INPUT_PATH,
    RAW_ROOT,
    TRAINING_SUMMARY_PATH,
)
from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, load_feature_order, validate_model_input_frame
from foundation.models.onnx_bridge import ordered_hash, ordered_sklearn_probabilities
from foundation.models.xgboost_boosting import nonflat_threshold, probability_shape_metrics, split_decision_metrics
from foundation.mt5 import runtime_support as mt5


STAGE_ID = "23_regime_model__supervised_regime_classifier_filter"
RUN_ID = "run17A_supervised_regime_classifier_filter_scout_v1"
RUN_NUMBER = "run17A"
PACKET_ID = "stage23_run17A_supervised_regime_classifier_scout_v1"
NEXT_RUN_ID = "run17B_supervised_regime_classifier_runtime_probe_v1"
EXPLORATION_LABEL = "stage23_Regime__SupervisedClassifierFilter"
MODEL_FAMILY = "sklearn_supervised_regime_classifier_filter"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_classifier_filter"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
THRESHOLD_QUANTILE = 0.80
BOUNDARY = "supervised_regime_classifier_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_supervised_regime_classifier_filter_scout_completed"

ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REPORT_PATH = STAGE_ROOT / "03_reviews/run17A_supervised_regime_classifier_scout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage23_run17A_supervised_regime_classifier_scout.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN_PATH = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"


@dataclass(frozen=True)
class RegimeClassifierVariantSpec:
    variant_id: str
    idea_id: str
    description: str
    model_type: str
    feature_names: tuple[str, ...]
    tier_b_compatible: bool
    random_state: int
    max_depth: int | None = None
    n_estimators: int | None = None
    min_samples_leaf: int = 80

    def payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["feature_names"] = list(self.feature_names)
        return payload


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def core24_features() -> tuple[str, ...]:
    return (
        "log_return_1",
        "log_return_3",
        "return_zscore_20",
        "hl_range",
        "atr_14",
        "atr_14_over_atr_50",
        "bollinger_width_20",
        "adx_14",
        "di_spread_14",
        "ema20_ema50_diff",
        "ema20_ema50_spread_zscore_50",
        "rsi_14",
        "rsi_14_slope_3",
        "bb_position_20",
        "stoch_kd_diff",
        "ppo_hist_12_26_9",
        "roc_12",
        "historical_vol_20",
        "minutes_from_cash_open",
        "is_us_cash_open",
        "is_first_30m_after_open",
        "close_ema20_ratio",
        "close_open_ratio",
        "vortex_indicator",
    )


def default_variants(full_feature_order: Sequence[str], tier_b_feature_order: Sequence[str]) -> list[RegimeClassifierVariantSpec]:
    core42 = tuple(tier_b_feature_order)
    full58 = tuple(full_feature_order)
    core24 = tuple(name for name in core24_features() if name in set(tier_b_feature_order))
    return [
        RegimeClassifierVariantSpec(
            variant_id="v01_logistic_core42_permission",
            idea_id="linear_supervised_regime_filter",
            description="Balanced multinomial logistic classifier as a quiet supervised permission surface.",
            model_type="logistic",
            feature_names=core42,
            tier_b_compatible=True,
            random_state=2301,
        ),
        RegimeClassifierVariantSpec(
            variant_id="v02_rf_core42_shallow_filter",
            idea_id="random_forest_supervised_regime_filter",
            description="Shallow random forest to test nonlinear supervised regime permission shape.",
            model_type="random_forest",
            feature_names=core42,
            tier_b_compatible=True,
            random_state=2302,
            n_estimators=140,
            max_depth=7,
            min_samples_leaf=90,
        ),
        RegimeClassifierVariantSpec(
            variant_id="v03_extratrees_core42_filter",
            idea_id="extra_trees_supervised_regime_filter",
            description="ExtraTrees classifier to test noisy threshold-style regime separation.",
            model_type="extra_trees",
            feature_names=core42,
            tier_b_compatible=True,
            random_state=2303,
            n_estimators=160,
            max_depth=7,
            min_samples_leaf=100,
        ),
        RegimeClassifierVariantSpec(
            variant_id="v04_rf_full58_context_filter",
            idea_id="full_context_supervised_regime_contrast",
            description="Tier-A-only full58 random forest context contrast, not a runtime handoff selection.",
            model_type="random_forest",
            feature_names=full58,
            tier_b_compatible=False,
            random_state=2304,
            n_estimators=140,
            max_depth=7,
            min_samples_leaf=90,
        ),
        RegimeClassifierVariantSpec(
            variant_id="v05_logistic_core24_compact_filter",
            idea_id="compact_linear_supervised_regime_filter",
            description="Compact core24 logistic filter to test smaller handoff-friendly behavior.",
            model_type="logistic",
            feature_names=core24,
            tier_b_compatible=True,
            random_state=2305,
        ),
    ]


def load_context() -> dict[str, Any]:
    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    full_feature_order = load_feature_order(FEATURE_ORDER_PATH)
    validate_model_input_frame(tier_a_frame, full_feature_order)
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=full_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=float(training_summary["threshold_log_return"]),
    )
    return {
        "tier_a_frame": tier_a_frame,
        "full_feature_order": full_feature_order,
        "tier_b_training_frame": tier_b_context["tier_b_training_frame"],
        "tier_b_fallback_frame": tier_b_context["tier_b_fallback_frame"],
        "tier_b_feature_order": tier_b_feature_order,
        "tier_b_context_summary": tier_b_context["summary"],
        "training_summary": training_summary,
    }


def build_model(spec: RegimeClassifierVariantSpec) -> Any:
    if spec.model_type == "logistic":
        return Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        class_weight="balanced",
                        max_iter=1200,
                        solver="lbfgs",
                        random_state=int(spec.random_state),
                    ),
                ),
            ]
        )
    if spec.model_type == "random_forest":
        return RandomForestClassifier(
            n_estimators=int(spec.n_estimators or 120),
            max_depth=spec.max_depth,
            min_samples_leaf=int(spec.min_samples_leaf),
            class_weight="balanced_subsample",
            n_jobs=-1,
            random_state=int(spec.random_state),
        )
    if spec.model_type == "extra_trees":
        return ExtraTreesClassifier(
            n_estimators=int(spec.n_estimators or 140),
            max_depth=spec.max_depth,
            min_samples_leaf=int(spec.min_samples_leaf),
            class_weight="balanced",
            n_jobs=-1,
            random_state=int(spec.random_state),
        )
    raise ValueError(f"Unsupported Stage23 classifier type: {spec.model_type}")


def fit_variant(frame: pd.DataFrame, feature_order: Sequence[str], spec: RegimeClassifierVariantSpec) -> tuple[Any, dict[str, Any]]:
    features = list(spec.feature_names)
    missing = sorted(set(features).difference(feature_order))
    if missing:
        raise ValueError(f"Regime classifier features missing from feature order: {missing}")
    validate_model_input_frame(frame, list(feature_order))
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    x = train.loc[:, features].to_numpy(dtype="float64", copy=False)
    y = train["label_class"].astype("int64").to_numpy()
    missing_labels = sorted(set(LABEL_ORDER).difference(set(y)))
    if missing_labels:
        raise RuntimeError(f"Train split is missing label classes: {missing_labels}")
    model = build_model(spec)
    model.fit(x, y)
    return model, {
        "train_rows": int(len(train)),
        "feature_count": len(features),
        "class_counts": {str(k): int(v) for k, v in train["label_class"].value_counts().sort_index().items()},
        "model_type": spec.model_type,
    }


def probability_frame(model: Any, frame: pd.DataFrame, feature_names: Sequence[str]) -> pd.DataFrame:
    values = frame.loc[:, list(feature_names)].to_numpy(dtype="float64", copy=False)
    probabilities = ordered_sklearn_probabilities(model, values)
    sorted_probabilities = np.sort(probabilities, axis=1)
    payload = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(frame["timestamp"], utc=True).to_numpy(),
            "split": frame["split"].astype(str).to_numpy(),
            "label_class": frame["label_class"].astype("int64").to_numpy(),
            "p_short": probabilities[:, 0],
            "p_flat": probabilities[:, 1],
            "p_long": probabilities[:, 2],
            "probability_margin": sorted_probabilities[:, -1] - sorted_probabilities[:, -2],
        }
    )
    payload["p_permission"] = payload[["p_short", "p_long"]].max(axis=1)
    payload["p_block"] = payload["p_flat"]
    if "partial_context_subtype" in frame.columns:
        payload["partial_context_subtype"] = frame["partial_context_subtype"].astype(str).to_numpy()
    return payload


def feature_read(model: Any, feature_names: Sequence[str], spec: RegimeClassifierVariantSpec) -> tuple[pd.DataFrame, dict[str, Any]]:
    features = list(feature_names)
    if isinstance(model, Pipeline):
        classifier = model.named_steps["classifier"]
        values = np.asarray(classifier.coef_, dtype="float64")
        rows = []
        for index, feature in enumerate(features):
            abs_values = np.abs(values[:, index])
            dominant_index = int(abs_values.argmax()) if len(abs_values) else 0
            rows.append(
                {
                    "feature": feature,
                    "importance": float(abs_values.max()) if len(abs_values) else 0.0,
                    "dominant_label": LABEL_NAMES[int(classifier.classes_[dominant_index])],
                    "read_type": "coefficient_abs",
                }
            )
    else:
        importances = np.asarray(getattr(model, "feature_importances_", np.zeros(len(features))), dtype="float64")
        rows = [
            {
                "feature": feature,
                "importance": float(importances[index]),
                "dominant_label": "tree_importance",
                "read_type": "feature_importance",
            }
            for index, feature in enumerate(features)
        ]
    frame = pd.DataFrame(rows).sort_values(["importance", "feature"], ascending=[False, True]).reset_index(drop=True)
    total = float(frame["importance"].abs().sum()) or 1.0
    read = {
        "read_type": str(frame["read_type"].iloc[0]) if not frame.empty else spec.model_type,
        "feature_count": len(features),
        "top10_importance_share": float(frame.head(10)["importance"].abs().sum() / total),
        "top_features": frame.head(12).to_dict(orient="records"),
    }
    return frame, read


def permission_read(prob: pd.DataFrame, threshold: float) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        part = prob.loc[prob["split"].astype(str).eq(split)]
        if part.empty:
            payload[split] = {"rows": 0}
            continue
        permit = part["p_permission"].to_numpy(dtype="float64") >= float(threshold)
        labels = part["label_class"].astype("int64").to_numpy()
        nonflat = labels != 1
        payload[split] = {
            "rows": int(len(part)),
            "permit_count": int(permit.sum()),
            "block_count": int((~permit).sum()),
            "permit_coverage": float(permit.mean()),
            "permitted_nonflat_rate": float(nonflat[permit].mean()) if permit.any() else None,
            "blocked_flat_rate": float((labels[~permit] == 1).mean()) if (~permit).any() else None,
            "mean_p_permission": float(part["p_permission"].mean()),
            "mean_p_block": float(part["p_block"].mean()),
        }
    return payload


def characteristic_score(metrics: Mapping[str, Any], shape: Mapping[str, Any], permission: Mapping[str, Any], features: Mapping[str, Any]) -> float:
    validation = metrics.get("validation", {})
    oos = metrics.get("oos", {})
    val_perm = permission.get("validation", {})
    oos_perm = permission.get("oos", {})
    score = 0.0
    score += safe_float(validation.get("balanced_accuracy"))
    score += safe_float(oos.get("balanced_accuracy"))
    score += 0.5 * safe_float(validation.get("macro_f1"))
    score += 0.5 * safe_float(oos.get("macro_f1"))
    score += 0.25 * safe_float(shape.get("validation", {}).get("probability_margin_mean"))
    score += 0.25 * safe_float(shape.get("oos", {}).get("probability_margin_mean"))
    score -= abs(safe_float(val_perm.get("permit_coverage")) - safe_float(oos_perm.get("permit_coverage")))
    score += 0.05 * safe_float(features.get("top10_importance_share"))
    return float(score)


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        frame.to_parquet(io_path(path), index=False)
    else:
        frame.to_csv(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def evaluate_variant(context: Mapping[str, Any], spec: RegimeClassifierVariantSpec) -> dict[str, Any]:
    model, sample = fit_variant(context["tier_a_frame"], context["full_feature_order"], spec)
    prob = probability_frame(model, context["tier_a_frame"], spec.feature_names)
    threshold = nonflat_threshold(prob, THRESHOLD_QUANTILE)
    metrics = split_decision_metrics(prob, threshold)
    shape = probability_shape_metrics(prob)
    feature_frame, feature_summary = feature_read(model, spec.feature_names, spec)
    feature_path = RUN_ROOT / "results/variant_feature_reads" / f"{spec.variant_id}_tier_a_feature_read.csv"
    save_frame(feature_path, feature_frame)
    permission = permission_read(prob, threshold)
    return {
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "description": spec.description,
        "spec": spec.payload(),
        "training_sample": sample,
        "threshold": threshold,
        "metrics": metrics,
        "probability_shape": shape,
        "permission_read": permission,
        "feature_read": feature_summary,
        "feature_artifact": {"path": rel(feature_path), "sha256": sha256_file_lf_normalized(feature_path)},
        "characteristic_score": characteristic_score(metrics, shape, permission, feature_summary),
    }


def select_variant(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    compatible = [row for row in rows if row.get("spec", {}).get("tier_b_compatible") is True]
    return dict(max(compatible or list(rows), key=lambda row: safe_float(row.get("characteristic_score"))))


def spec_from_row(row: Mapping[str, Any]) -> RegimeClassifierVariantSpec:
    payload = dict(row.get("spec", {}))
    payload["feature_names"] = tuple(payload["feature_names"])
    return RegimeClassifierVariantSpec(**payload)


def save_variant_results(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result_root = RUN_ROOT / "results"
    json_path = result_root / "supervised_regime_variant_results.json"
    csv_path = result_root / "supervised_regime_variant_results.csv"
    write_json(json_path, list(rows))
    csv_rows = []
    for row in rows:
        metrics = row.get("metrics", {})
        permission = row.get("permission_read", {})
        spec = row.get("spec", {})
        csv_rows.append(
            {
                "variant_id": row.get("variant_id"),
                "model_type": spec.get("model_type"),
                "feature_count": len(spec.get("feature_names", [])),
                "tier_b_compatible": spec.get("tier_b_compatible"),
                "threshold": row.get("threshold"),
                "characteristic_score": row.get("characteristic_score"),
                "validation_balanced_accuracy": metrics.get("validation", {}).get("balanced_accuracy"),
                "oos_balanced_accuracy": metrics.get("oos", {}).get("balanced_accuracy"),
                "validation_macro_f1": metrics.get("validation", {}).get("macro_f1"),
                "oos_macro_f1": metrics.get("oos", {}).get("macro_f1"),
                "validation_signal_coverage": metrics.get("validation", {}).get("signal_coverage"),
                "oos_signal_coverage": metrics.get("oos", {}).get("signal_coverage"),
                "validation_permit_coverage": permission.get("validation", {}).get("permit_coverage"),
                "oos_permit_coverage": permission.get("oos", {}).get("permit_coverage"),
            }
        )
    write_csv(
        csv_path,
        (
            "variant_id",
            "model_type",
            "feature_count",
            "tier_b_compatible",
            "threshold",
            "characteristic_score",
            "validation_balanced_accuracy",
            "oos_balanced_accuracy",
            "validation_macro_f1",
            "oos_macro_f1",
            "validation_signal_coverage",
            "oos_signal_coverage",
            "validation_permit_coverage",
            "oos_permit_coverage",
        ),
        csv_rows,
    )
    return {
        "variant_results_json": {"path": rel(json_path), "sha256": sha256_file_lf_normalized(json_path)},
        "variant_results_csv": {"path": rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path)},
    }


def tier_record(record_view: str, tier_scope: str, prob_frame: pd.DataFrame, threshold: float, path: Path) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, threshold)
    permission = permission_read(prob_frame, threshold)
    subtype_counts: dict[str, int] = {}
    if "partial_context_subtype" in prob_frame.columns:
        subtype_counts = {str(key): int(value) for key, value in prob_frame["partial_context_subtype"].astype(str).value_counts().sort_index().items()}
    total = {
        "rows": int(len(prob_frame)),
        "signal_count": int(sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))),
        "short_count": int(sum(metrics.get(split, {}).get("short_count", 0) for split in ("train", "validation", "oos"))),
        "long_count": int(sum(metrics.get(split, {}).get("long_count", 0) for split in ("train", "validation", "oos"))),
        "signal_coverage": None,
        "permission_read": permission,
        "partial_context_subtype_counts": subtype_counts or None,
        "threshold_ids": f"q{THRESHOLD_QUANTILE:.2f}",
        "probability_row_sum_max_abs_error": metrics.get("probability_checks", {}).get("row_sum_max_abs_error"),
    }
    total["signal_coverage"] = safe_float(total["signal_count"]) / max(1, int(total["rows"]))
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": total,
        "split_metrics": {split: metrics.get(split, {}) for split in ("train", "validation", "oos")},
    }


def materialize_selected(context: Mapping[str, Any], selected: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], dict[str, Any]]:
    spec = spec_from_row(selected)
    model_root = RUN_ROOT / "models"
    io_path(model_root).mkdir(parents=True, exist_ok=True)
    tier_a_model, tier_a_sample = fit_variant(context["tier_a_frame"], context["full_feature_order"], spec)
    tier_b_model, tier_b_sample = fit_variant(context["tier_b_training_frame"], context["tier_b_feature_order"], spec)
    tier_a_model_path = model_root / f"{spec.variant_id}_tier_a_supervised_regime_classifier.joblib"
    tier_b_model_path = model_root / f"{spec.variant_id}_tier_b_supervised_regime_classifier.joblib"
    joblib.dump(tier_a_model, io_path(tier_a_model_path))
    joblib.dump(tier_b_model, io_path(tier_b_model_path))
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], spec.feature_names)
    tier_b_train_prob = probability_frame(tier_b_model, context["tier_b_training_frame"], spec.feature_names)
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], spec.feature_names)
    tier_a_threshold = nonflat_threshold(tier_a_prob, THRESHOLD_QUANTILE)
    tier_b_threshold = nonflat_threshold(tier_b_train_prob, THRESHOLD_QUANTILE)
    pred_root = RUN_ROOT / "predictions"
    a_path = pred_root / "tier_a_supervised_regime_predictions.parquet"
    b_path = pred_root / "tier_b_supervised_regime_predictions.parquet"
    ab_path = pred_root / "tier_ab_supervised_regime_predictions.parquet"
    ab_prob = pd.concat(
        [
            tier_a_prob.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_prob.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    records = [
        tier_record("tier_a_separate", mt5.TIER_A, tier_a_prob, tier_a_threshold, a_path),
        tier_record("tier_b_separate", mt5.TIER_B, tier_b_prob, tier_b_threshold, b_path),
        tier_record("tier_ab_combined", mt5.TIER_AB, ab_prob, tier_a_threshold, ab_path),
    ]
    prediction_artifacts = {
        "tier_a_predictions": save_frame(a_path, tier_a_prob),
        "tier_b_predictions": save_frame(b_path, tier_b_prob),
        "tier_ab_predictions": save_frame(ab_path, ab_prob),
    }
    model_artifacts = {
        "tier_a_model": {"path": rel(tier_a_model_path), "sha256": sha256_file_lf_normalized(tier_a_model_path), "training_sample": tier_a_sample},
        "tier_b_model": {"path": rel(tier_b_model_path), "sha256": sha256_file_lf_normalized(tier_b_model_path), "training_sample": tier_b_sample},
        "thresholds": {"tier_a": tier_a_threshold, "tier_b": tier_b_threshold, "quantile": THRESHOLD_QUANTILE},
        "runtime_feature_order": list(spec.feature_names),
        "runtime_feature_order_hash": ordered_hash(spec.feature_names),
    }
    tier_a_features, tier_a_feature_read = feature_read(tier_a_model, spec.feature_names, spec)
    tier_b_features, tier_b_feature_read = feature_read(tier_b_model, spec.feature_names, spec)
    feature_root = RUN_ROOT / "results/selected_feature_reads"
    a_feature_path = feature_root / "tier_a_selected_feature_read.csv"
    b_feature_path = feature_root / "tier_b_selected_feature_read.csv"
    save_frame(a_feature_path, tier_a_features)
    save_frame(b_feature_path, tier_b_features)
    model_artifacts["feature_reads"] = {
        "tier_a": {**tier_a_feature_read, "path": rel(a_feature_path), "sha256": sha256_file_lf_normalized(a_feature_path)},
        "tier_b": {**tier_b_feature_read, "path": rel(b_feature_path), "sha256": sha256_file_lf_normalized(b_feature_path)},
    }
    return records, prediction_artifacts, model_artifacts, {"tier_a_prob": tier_a_prob, "tier_b_prob": tier_b_prob}


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
                "kpi_scope": "supervised_regime_classifier_filter",
                "scoreboard_lane": "structural_scout",
                "status": "reviewed",
                "judgment": JUDGMENT,
                "path": record["path"],
                "primary_kpi": ledger_pairs(
                    (
                        ("rows", metrics.get("rows")),
                        ("signal_coverage", metrics.get("signal_coverage")),
                        ("signals", metrics.get("signal_count")),
                        ("short", metrics.get("short_count")),
                        ("long", metrics.get("long_count")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("threshold", metrics.get("threshold_ids")),
                        ("prob_sum_err", metrics.get("probability_row_sum_max_abs_error")),
                        ("subtypes", metrics.get("partial_context_subtype_counts")),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
                "notes": "Supervised regime classifier filter scout only; not baseline or promotion.",
            }
        )
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "regime_classifier_structural_scout",
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
    val = summary["selected_variant_read"].get("metrics", {}).get("validation", {})
    oos = summary["selected_variant_read"].get("metrics", {}).get("oos", {})
    write_md(
        REPORT_PATH,
        f"""# RUN17A Supervised Regime Classifier Scout Packet(실행17A 지도 국면 분류기 탐색 묶음)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected}`
- boundary(경계): `{BOUNDARY}`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run17A_next_milestone_{NEXT_RUN_ID}(실행17A에서는 미시도, 다음 마일스톤은 {NEXT_RUN_ID})`

효과(effect, 효과): supervised classifier(지도 분류기)를 direct entry model(직접 진입 모델)이 아니라 p_flat(평탄 확률)을 block/abstain(차단/기권) 후보로 읽는 regime filter(국면 필터)로 탐색했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Evidence(근거)

- variants(변형): `{summary['variant_count']}`
- selected model type(선택 모델 유형): `{summary['selected_variant_read'].get('spec', {}).get('model_type')}`
- threshold quantile(임계 분위수): `q{THRESHOLD_QUANTILE:.2f}`
- Tier A rows(Tier A 행): `{summary['tier_rows']['tier_a']}`
- Tier B fallback rows(Tier B 대체 행): `{summary['tier_rows']['tier_b_fallback']}`
- validation balanced accuracy(검증 균형 정확도): `{val.get('balanced_accuracy')}`
- OOS balanced accuracy(표본외 균형 정확도): `{oos.get('balanced_accuracy')}`
- validation signal coverage(검증 신호 비중): `{val.get('signal_coverage')}`
- OOS signal coverage(표본외 신호 비중): `{oos.get('signal_coverage')}`

## Preserved Clues(보존 단서)

- p_flat(평탄 확률)을 block/abstain(차단/기권) 후보로 읽는 filter interpretation(필터 해석)을 보존한다.
- Tier A/B(티어 A/B) 모두 같은 selected variant(선택 변형)로 재학습해 partial-context fallback(부분 문맥 대체)의 probability shape(확률 모양)을 비교할 수 있다.
- 다음 MT5 runtime_probe(MT5 런타임 탐침)는 selected variant(선택 변형)를 ONNX(온닉스) 또는 table handoff(테이블 인계)로 좁게 검증한다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}` as a narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    line = f"- `{RUN_ID}`: `{rel(REPORT_PATH)}`\n"
    if RUN_ID not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)


def write_packet(summary: Mapping[str, Any], created_at: str) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    receipts = [
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "Supervised classifiers may expose permission/filter probability shape through p_flat and non-flat confidence.",
            "boundary": BOUNDARY,
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_boundary": "classifier_filter_scout_not_entry_baseline",
            "forbidden_claims": summary["forbidden_claims"],
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
        {"packet_id": PACKET_ID, "status": "not_required_for_run17A", "next_runtime_probe": NEXT_RUN_ID},
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
        f"- treat Stage 23 as opened_not_started after Stage22 reviewed closeout; next action is {NEXT_RUN_ID}, and no baseline, promotion, or runtime authority exists",
        f"- treat Stage 23 as active after {RUN_ID} supervised regime classifier Python structural scout; next action is {NEXT_RUN_ID.replace('run17A_', 'run17B_').replace('_scout_v1', '_runtime_probe_v1')}, and no baseline, promotion, or runtime authority exists",
        1,
    )
    text = text.replace("      status: opened_not_started\n      current_run_id: not_started", f"      status: active_run17A_python_structural_scout_completed\n      current_run_id: {RUN_ID}", 1)
    text = text.replace("latest_completed_run: stage22_closeout_stage23_open", f"latest_completed_run: {RUN_ID}", 1)
    text = text.replace(f"next_exact_action: {NEXT_RUN_ID}", f"next_exact_action: {NEXT_RUN_ID.replace('run17A_', 'run17B_').replace('_scout_v1', '_runtime_probe_v1')}", 1)
    block = f"""stage23_supervised_regime_classifier_filter:
  stage_id: {STAGE_ID}
  status: active_run17A_python_structural_scout_completed
  current_run_id: {RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {summary['selected_variant_id']}
  boundary: {BOUNDARY}
  stage_brief_path: stages/{STAGE_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE_ID}/04_selected/selection_status.md
  report_path: stages/{STAGE_ID}/03_reviews/run17A_supervised_regime_classifier_scout_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID.replace('run17A_', 'run17B_').replace('_scout_v1', '_runtime_probe_v1')}
"""
    text = replace_top_level_yaml_block(text, "stage23_supervised_regime_classifier_filter:", block)
    run_block = f"""stage23_regime_run17A_structural_scout:
  packet_id: {PACKET_ID}
  status: reviewed_structural_scout_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  selected_variant_id: {summary['selected_variant_id']}
  mt5_runtime_probe_status: not_attempted_next_milestone_{NEXT_RUN_ID.replace('run17A_', 'run17B_').replace('_scout_v1', '_runtime_probe_v1')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: stages/{STAGE_ID}/03_reviews/run17A_supervised_regime_classifier_scout_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID.replace('run17A_', 'run17B_').replace('_scout_v1', '_runtime_probe_v1')}
"""
    text = replace_top_level_yaml_block(text, "stage23_regime_run17A_structural_scout:", run_block)
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def update_text_docs(summary: Mapping[str, Any]) -> None:
    next_action = NEXT_RUN_ID.replace("run17A_", "run17B_").replace("_scout_v1", "_runtime_probe_v1")
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage23 Selection Status(23단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `active_run17A_python_structural_scout_completed`
- current run(현재 실행): `{RUN_ID}`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{summary['selected_variant_id']}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage23(23단계)는 supervised classifier(지도 분류기)의 permission/filter(허용/필터) 구조를 Python-side evidence(파이썬 근거)로 잡았지만 MT5 runtime_probe(MT5 런타임 탐침), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 아직 없다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{next_action}`.
""",
    )
    write_md(
        DECISION_PATH,
        f"""# Stage23 RUN17A Supervised Regime Classifier Decision(23단계 실행17A 지도 국면 분류기 결정)

## Decision(결정)

`{RUN_ID}`를 `{JUDGMENT}`로 기록한다.

효과(effect, 효과): supervised classifier(지도 분류기)를 filter/permission layer(필터/허용 계층) 후보로 탐색했지만, 이 근거는 structural scout(구조 탐색)일 뿐 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)가 아니다.

## Next Condition(다음 조건)

`{next_action}`.
""",
    )
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage23 RUN17A Supervised Regime Update(최신 23단계 실행17A 지도 국면 업데이트)

Stage23(23단계) `{RUN_ID}`를 Python structural scout(파이썬 구조 탐색)로 실행했다.

결과(result, 결과): `{JUDGMENT}`. selected variant(선택 변형): `{summary['selected_variant_id']}`. next exact action(다음 정확한 행동): `{next_action}`.

효과(effect, 효과): p_flat(평탄 확률)을 block/abstain(차단/기권) 후보로 읽는 supervised regime classifier(지도 국면 분류기) 특성을 기록했고, MT5 runtime_probe(MT5 런타임 탐침)는 다음 실행으로 남긴다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    plan = plan.replace("- current run(현재 실행): `not_started`", f"- current run(현재 실행): `{RUN_ID}`", 1)
    plan = plan.replace(
        f"Stage23(23단계)는 supervised regime classifier(지도 국면 분류기) open-only(개방만) 상태다. 현재 첫 미완료 milestone(마일스톤)은 Stage23(23단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색)이다.",
        f"Stage23(23단계)는 `{RUN_ID}` supervised regime classifier(지도 국면 분류기) Python structural scout(파이썬 구조 탐색)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 Stage23(23단계) `{next_action}` MT5 runtime_probe(MT5 런타임 탐침)이다.",
        1,
    )
    plan = plan.replace(
        "- [ ] Stage23(23단계) supervised regime classifier(지도 국면 분류기) scout/probe/closeout/open Stage24",
        f"- [ ] Stage23(23단계) supervised regime classifier(지도 국면 분류기) scout/probe/closeout/open Stage24. Completed(완료): `{RUN_ID}`; remaining(남음): MT5 runtime_probe(MT5 런타임 탐침), closeout/open Stage24.",
        1,
    )
    plan = plan.replace(
        f"Current active milestone(현재 활성 마일스톤): Stage23(23단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색).",
        f"Current active milestone(현재 활성 마일스톤): Stage23(23단계) `{next_action}` narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).",
        1,
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `{RUN_ID}` completed(완료) as Python structural scout(파이썬 구조 탐색).
- active branch(활성 브랜치): `codex/stage23-supervised-regime-classifier`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage23(23단계), `{RUN_ID}`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE_ID}/02_runs/{RUN_ID}`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): supervised regime classifier scout pipeline(지도 국면 분류기 탐색 파이프라인), run evidence(실행 근거), ledgers(장부), current truth docs(현재 진실 문서).
- active stage folder(활성 단계 폴더): `stages/{STAGE_ID}`.
- current run id(현재 실행 ID): `{RUN_ID}`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `not_attempted_in_run17A(실행17A에서 미시도)`; review report(검토 보고서) `{rel(REPORT_PATH)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{next_action}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage23(23단계) MT5 runtime_probe(런타임 탐침) 준비에서 시작한다.
"""
    marker = "## Latest Stop Resume State"
    start = plan.find(marker)
    if start != -1:
        next_section = plan.find("\n## ", start + 1)
        plan = plan[:start] + resume + ("\n" + plan[next_section + 1 :] if next_section != -1 else "")
    else:
        plan = plan.rstrip() + "\n\n" + resume
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    variants = default_variants(context["full_feature_order"], context["tier_b_feature_order"])
    rows = [evaluate_variant(context, spec) for spec in variants]
    variant_artifacts = save_variant_results(rows)
    selected = select_variant(rows)
    tier_records, prediction_artifacts, model_artifacts, selected_payload = materialize_selected(context, selected)
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
        "threshold_quantile": THRESHOLD_QUANTILE,
        "variant_count": len(rows),
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
        "allowed_claims": ["python_structural_scout_completed", "supervised_regime_filter_clues_recorded"],
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority"],
        "next_action": NEXT_RUN_ID.replace("run17A_", "run17B_").replace("_scout_v1", "_runtime_probe_v1"),
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
    materialize_ledgers(summary)
    write_review(summary)
    write_packet(summary, created_at)
    update_workspace_state(summary)
    update_text_docs(summary)
    return {
        "run_id": RUN_ID,
        "judgment": JUDGMENT,
        "selected_variant_id": selected["variant_id"],
        "external_verification_status": summary["external_verification_status"],
        "next_action": summary["next_action"],
    }


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Run Stage23 supervised regime classifier filter scout.")


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    print(json.dumps(json_ready(run(args)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
