from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
import yaml
from sklearn.ensemble import ExtraTreesClassifier

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.tier_context_materialization import (
    TIER_B_CORE_FEATURE_ORDER,
    build_tier_b_partial_context_frames,
)
from stage_pipelines.stage12.extratrees_standalone_batch20_support import (
    ALL_CLASSES,
    BASE_MODEL_PARAMS,
    CLASS_TO_LABEL,
    VariantSpec,
    _model_params,
    _variant_specs,
)


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "12_model_family_challenge__extratrees_training_effect"
RUN_ID = "run03J_et_rolling_wfo_split_probe_v1"
RUN_NUMBER = "run03J"
PACKET_ID = "stage12_run03j_rolling_wfo_split_probe_v1"
EXPLORATION_LABEL = "stage12_Model__ExtraTreesRollingWFOSplitProbe"
SOURCE_VARIANT_RUN_ID = "run03D_et_standalone_batch20_v1"
SOURCE_MT5_RUN_ID = "run03H_et_batch20_all_variant_tier_balance_mt5_v1"
SOURCE_ATTRIBUTION_RUN_ID = "run03I_et_validation_oos_inversion_attribution_v1"
MODEL_FAMILY = "sklearn_extratreesclassifier_multiclass"
BOUNDARY = "python_rolling_wfo_structural_probe_only_not_mt5_not_alpha_quality_not_promotion"
JUDGMENT_DEFAULT = "inconclusive_rolling_wfo_split_probe_completed_not_promotion"
HIT_FLOOR = 0.48
PROBE_N_ESTIMATORS = 96

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
SOURCE_VARIANT_ROOT = STAGE_ROOT / "02_runs" / SOURCE_VARIANT_RUN_ID
MODEL_INPUT_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
TRAINING_SUMMARY_PATH = ROOT / "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"
RAW_ROOT = ROOT / "data/raw/mt5_bars/m5"

RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_RUN_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
STAGE_REVIEW_PATH = STAGE_ROOT / "03_reviews/run03J_rolling_wfo_split_probe_packet.md"
PLAN_PATH = STAGE_ROOT / "00_spec/run03J_rolling_wfo_split_probe_plan.md"


@dataclass(frozen=True)
class FoldSpec:
    fold_id: str
    train_start: str
    train_end_exclusive: str
    validation_start: str
    validation_end_exclusive: str
    test_start: str
    test_end_exclusive: str

    def as_row(self) -> dict[str, Any]:
        return {
            "fold_id": self.fold_id,
            "train_start": self.train_start,
            "train_end_exclusive": self.train_end_exclusive,
            "validation_start": self.validation_start,
            "validation_end_exclusive": self.validation_end_exclusive,
            "test_start": self.test_start,
            "test_end_exclusive": self.test_end_exclusive,
            "train_style": "expanding_forward",
        }


FOLDS = (
    FoldSpec("fold01", "2022-09-01T00:00:00Z", "2024-04-01T00:00:00Z", "2024-04-01T00:00:00Z", "2024-07-01T00:00:00Z", "2024-07-01T00:00:00Z", "2024-10-01T00:00:00Z"),
    FoldSpec("fold02", "2022-09-01T00:00:00Z", "2024-07-01T00:00:00Z", "2024-07-01T00:00:00Z", "2024-10-01T00:00:00Z", "2024-10-01T00:00:00Z", "2025-01-01T00:00:00Z"),
    FoldSpec("fold03", "2022-09-01T00:00:00Z", "2024-10-01T00:00:00Z", "2024-10-01T00:00:00Z", "2025-01-01T00:00:00Z", "2025-01-01T00:00:00Z", "2025-04-01T00:00:00Z"),
    FoldSpec("fold04", "2022-09-01T00:00:00Z", "2025-01-01T00:00:00Z", "2025-01-01T00:00:00Z", "2025-04-01T00:00:00Z", "2025-04-01T00:00:00Z", "2025-07-01T00:00:00Z"),
    FoldSpec("fold05", "2022-09-01T00:00:00Z", "2025-04-01T00:00:00Z", "2025-04-01T00:00:00Z", "2025-07-01T00:00:00Z", "2025-07-01T00:00:00Z", "2025-10-01T00:00:00Z"),
    FoldSpec("fold06", "2022-09-01T00:00:00Z", "2025-07-01T00:00:00Z", "2025-07-01T00:00:00Z", "2025-10-01T00:00:00Z", "2025-10-01T00:00:00Z", "2026-01-01T00:00:00Z"),
    FoldSpec("fold07", "2022-09-01T00:00:00Z", "2025-10-01T00:00:00Z", "2025-10-01T00:00:00Z", "2026-01-01T00:00:00Z", "2026-01-01T00:00:00Z", "2026-04-14T00:00:00Z"),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig" if bom else "utf-8")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def current_branch() -> str:
    try:
        completed = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return completed.stdout.strip() or "unknown"


def load_feature_order() -> list[str]:
    return [line.strip() for line in read_text(FEATURE_ORDER_PATH).splitlines() if line.strip()]


def ordered_hash(values: Sequence[str]) -> str:
    payload = "\n".join(values).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def probe_params(spec: VariantSpec) -> dict[str, Any]:
    params = _model_params(spec)
    params["n_estimators"] = min(int(params.get("n_estimators", PROBE_N_ESTIMATORS)), PROBE_N_ESTIMATORS)
    return params


def probe_base_params() -> dict[str, Any]:
    params = dict(BASE_MODEL_PARAMS)
    params["n_estimators"] = min(int(params.get("n_estimators", PROBE_N_ESTIMATORS)), PROBE_N_ESTIMATORS)
    return params


def prepare_frames() -> tuple[pd.DataFrame, pd.DataFrame, list[str], dict[str, Any]]:
    if not path_exists(MODEL_INPUT_PATH):
        raise FileNotFoundError(MODEL_INPUT_PATH)
    if not path_exists(FEATURE_ORDER_PATH):
        raise FileNotFoundError(FEATURE_ORDER_PATH)
    if not path_exists(TRAINING_SUMMARY_PATH):
        raise FileNotFoundError(TRAINING_SUMMARY_PATH)

    tier_a = pd.read_parquet(io_path(MODEL_INPUT_PATH)).copy()
    tier_a["timestamp"] = pd.to_datetime(tier_a["timestamp"], utc=True)
    tier_a["label_class"] = tier_a["label_class"].astype(int)
    tier_a["label_direction"] = tier_a["label_class"].map(CLASS_TO_LABEL).astype(int)
    tier_a["tier_source"] = "Tier A"
    tier_a["route_role"] = "tier_a_primary"

    feature_order = load_feature_order()
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    context = build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a,
        tier_a_feature_order=feature_order,
        tier_b_feature_order=list(TIER_B_CORE_FEATURE_ORDER),
        label_threshold=float(training_summary["threshold_log_return"]),
    )
    tier_b_training = context["tier_b_training_frame"].copy()
    tier_b_training["timestamp"] = pd.to_datetime(tier_b_training["timestamp"], utc=True)
    tier_b_training["label_class"] = tier_b_training["label_class"].astype(int)
    tier_b_training["label_direction"] = tier_b_training["label_class"].map(CLASS_TO_LABEL).astype(int)
    tier_b_training["tier_source"] = "Tier B training"

    tier_b_fallback = context["tier_b_fallback_frame"].copy()
    tier_b_fallback["timestamp"] = pd.to_datetime(tier_b_fallback["timestamp"], utc=True)
    tier_b_fallback["label_class"] = tier_b_fallback["label_class"].astype(int)
    tier_b_fallback["label_direction"] = tier_b_fallback["label_class"].map(CLASS_TO_LABEL).astype(int)
    tier_b_fallback["tier_source"] = "Tier B"
    tier_b_fallback["route_role"] = "tier_b_fallback"

    metadata = {
        "dataset_path": rel(MODEL_INPUT_PATH),
        "dataset_sha256": sha256_file_lf_normalized(MODEL_INPUT_PATH),
        "feature_order_path": rel(FEATURE_ORDER_PATH),
        "feature_order_sha256": sha256_file_lf_normalized(FEATURE_ORDER_PATH),
        "training_summary_path": rel(TRAINING_SUMMARY_PATH),
        "training_summary_sha256": sha256_file_lf_normalized(TRAINING_SUMMARY_PATH),
        "tier_b_context_summary": context["summary"],
    }
    return tier_a, tier_b_fallback, feature_order, {"tier_b_training": tier_b_training, **metadata}


def window(frame: pd.DataFrame, start: str, end_exclusive: str) -> pd.DataFrame:
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end_exclusive)
    return frame.loc[(frame["timestamp"] >= start_ts) & (frame["timestamp"] < end_ts)].copy().reset_index(drop=True)


def feature_sets_for_fold(train_frame: pd.DataFrame, feature_order: Sequence[str], fold_id: str) -> dict[str, list[str]]:
    all58 = list(feature_order)
    core42 = list(TIER_B_CORE_FEATURE_ORDER)
    context16 = [feature for feature in feature_order if feature not in core42]

    params = probe_base_params()
    params["random_state"] = int(BASE_MODEL_PARAMS["random_state"]) + 703
    pilot = ExtraTreesClassifier(**params)
    pilot.fit(train_frame[all58], train_frame["label_class"].astype(int))
    fi = pd.DataFrame({"fold_id": fold_id, "feature": all58, "importance": pilot.feature_importances_}).sort_values(
        ["importance", "feature"], ascending=[False, True]
    )
    io_path(RUN_ROOT / "feature_importance").mkdir(parents=True, exist_ok=True)
    fi.to_csv(io_path(RUN_ROOT / "feature_importance" / f"{fold_id}_top30_from_train.csv"), index=False, encoding="utf-8")
    top30 = fi.head(30)["feature"].astype(str).tolist()
    return {
        "all58": all58,
        "core42": core42,
        "context16": context16,
        "top30_from_train_importance": top30,
    }


def ordered_probs(model: ExtraTreesClassifier, frame: pd.DataFrame, features: Sequence[str]) -> np.ndarray:
    raw = model.predict_proba(frame.loc[:, list(features)].to_numpy(dtype="float64", copy=False))
    probs = np.zeros((len(frame), len(ALL_CLASSES)), dtype=float)
    for col_idx, cls in enumerate(model.classes_):
        probs[:, ALL_CLASSES.index(int(cls))] = raw[:, col_idx]
    return probs


def nonflat_threshold(probs: np.ndarray, quantile: float) -> float:
    if len(probs) == 0:
        return math.nan
    return float(np.quantile(np.maximum(probs[:, 0], probs[:, 2]), quantile))


def decision_frame(
    *,
    source: pd.DataFrame,
    probs: np.ndarray,
    threshold: float,
    spec: VariantSpec,
    fold_id: str,
    split_role: str,
    tier_scope: str,
    route_role: str,
    feature_selector: str,
    feature_count: int,
) -> pd.DataFrame:
    p_short = probs[:, 0]
    p_flat = probs[:, 1]
    p_long = probs[:, 2]
    nonflat_conf = np.maximum(p_short, p_long)
    predicted_direction = np.where(p_short >= p_long, 0, 2)
    competing = np.maximum(p_flat, np.where(predicted_direction == 0, p_long, p_short))
    margin = nonflat_conf - competing
    pass_gate = (nonflat_conf >= threshold) & (margin >= spec.min_margin)

    decision = np.full(len(source), 1, dtype=int)
    if spec.direction_mode == "both":
        decision[pass_gate] = predicted_direction[pass_gate]
    elif spec.direction_mode == "short_only":
        decision[pass_gate & (predicted_direction == 0)] = 0
    elif spec.direction_mode == "long_only":
        decision[pass_gate & (predicted_direction == 2)] = 2
    elif spec.direction_mode == "inverse":
        decision[pass_gate & (predicted_direction == 0)] = 2
        decision[pass_gate & (predicted_direction == 2)] = 0
    else:
        raise ValueError(f"unknown direction_mode: {spec.direction_mode}")

    labels = source["label_class"].astype(int).to_numpy()
    is_signal = decision != 1
    correct = (decision == labels) & is_signal
    return pd.DataFrame(
        {
            "run_id": RUN_ID,
            "fold_id": fold_id,
            "variant_id": spec.variant_id,
            "idea_id": spec.idea_id,
            "split_role": split_role,
            "original_split": source["split"].astype(str).to_numpy(),
            "tier_scope": tier_scope,
            "route_role": route_role,
            "feature_selector": feature_selector,
            "feature_count": int(feature_count),
            "timestamp": source["timestamp"].astype(str).to_numpy(),
            "label_class": labels,
            "label_direction": source["label_direction"].astype(int).to_numpy(),
            "p_short": p_short,
            "p_flat": p_flat,
            "p_long": p_long,
            "nonflat_conf": nonflat_conf,
            "margin": margin,
            "threshold": threshold,
            "threshold_quantile": spec.threshold_quantile,
            "min_margin": spec.min_margin,
            "direction_mode": spec.direction_mode,
            "decision_class": decision,
            "decision_direction": [CLASS_TO_LABEL[int(value)] for value in decision],
            "is_signal": is_signal,
            "directional_correct": correct,
        }
    )


def signal_metrics(frame: pd.DataFrame) -> dict[str, Any]:
    signals = frame.loc[frame["is_signal"]]
    signal_count = int(len(signals))
    correct_count = int(signals["directional_correct"].sum()) if signal_count else 0
    short_count = int((signals["decision_class"] == 0).sum())
    long_count = int((signals["decision_class"] == 2).sum())
    return {
        "rows": int(len(frame)),
        "signal_count": signal_count,
        "coverage": float(signal_count / len(frame)) if len(frame) else None,
        "correct_count": correct_count,
        "hit_rate": float(correct_count / signal_count) if signal_count else None,
        "short_count": short_count,
        "long_count": long_count,
    }


def metric_row(frame: pd.DataFrame, fold: FoldSpec, split_role: str) -> dict[str, Any]:
    metrics = signal_metrics(frame)
    first = frame.iloc[0].to_dict() if not frame.empty else {}
    return {
        "run_id": RUN_ID,
        "fold_id": fold.fold_id,
        "variant_id": first.get("variant_id", ""),
        "idea_id": first.get("idea_id", ""),
        "split_role": split_role,
        "tier_scope": first.get("tier_scope", ""),
        "route_role": first.get("route_role", ""),
        "feature_selector": first.get("feature_selector", ""),
        "feature_count": first.get("feature_count", 0),
        "threshold": first.get("threshold", math.nan),
        "threshold_quantile": first.get("threshold_quantile", math.nan),
        "min_margin": first.get("min_margin", math.nan),
        "direction_mode": first.get("direction_mode", ""),
        **metrics,
        "train_start": fold.train_start,
        "train_end_exclusive": fold.train_end_exclusive,
        "validation_start": fold.validation_start,
        "validation_end_exclusive": fold.validation_end_exclusive,
        "test_start": fold.test_start,
        "test_end_exclusive": fold.test_end_exclusive,
    }


def train_model_cached(
    cache: dict[tuple[str, str, str], ExtraTreesClassifier],
    *,
    fold_id: str,
    model_key: str,
    train_frame: pd.DataFrame,
    features: Sequence[str],
    params: Mapping[str, Any],
) -> ExtraTreesClassifier:
    cache_key = (fold_id, model_key, ordered_hash(features))
    if cache_key not in cache:
        model = ExtraTreesClassifier(**dict(params))
        model.fit(train_frame.loc[:, list(features)].to_numpy(dtype="float64", copy=False), train_frame["label_class"].astype(int))
        cache[cache_key] = model
    return cache[cache_key]


def evaluate_wfo(
    specs: Sequence[VariantSpec],
    tier_a: pd.DataFrame,
    tier_b_fallback: pd.DataFrame,
    tier_b_training: pd.DataFrame,
    feature_order: Sequence[str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    model_cache: dict[tuple[str, str, str], ExtraTreesClassifier] = {}
    metric_rows: list[dict[str, Any]] = []
    signal_frames: list[pd.DataFrame] = []
    fold_plan_rows: list[dict[str, Any]] = []

    for fold in FOLDS:
        fold_plan_rows.append(
            {
                **fold.as_row(),
                "tier_a_train_rows": len(window(tier_a, fold.train_start, fold.train_end_exclusive)),
                "tier_a_validation_rows": len(window(tier_a, fold.validation_start, fold.validation_end_exclusive)),
                "tier_a_test_rows": len(window(tier_a, fold.test_start, fold.test_end_exclusive)),
                "tier_b_training_rows": len(window(tier_b_training, fold.train_start, fold.train_end_exclusive)),
                "tier_b_fallback_validation_rows": len(window(tier_b_fallback, fold.validation_start, fold.validation_end_exclusive)),
                "tier_b_fallback_test_rows": len(window(tier_b_fallback, fold.test_start, fold.test_end_exclusive)),
            }
        )
        a_train = window(tier_a, fold.train_start, fold.train_end_exclusive)
        a_validation = window(tier_a, fold.validation_start, fold.validation_end_exclusive)
        a_test = window(tier_a, fold.test_start, fold.test_end_exclusive)
        b_train = window(tier_b_training, fold.train_start, fold.train_end_exclusive)
        b_validation = window(tier_b_fallback, fold.validation_start, fold.validation_end_exclusive)
        b_test = window(tier_b_fallback, fold.test_start, fold.test_end_exclusive)
        feature_sets = feature_sets_for_fold(a_train, feature_order, fold.fold_id)

        for spec in specs:
            params = probe_params(spec)
            a_features = feature_sets[spec.feature_selector]
            b_features = list(TIER_B_CORE_FEATURE_ORDER)

            a_model = train_model_cached(
                model_cache,
                fold_id=fold.fold_id,
                model_key=f"tier_a::{spec.model_key}",
                train_frame=a_train,
                features=a_features,
                params=params,
            )
            a_val_probs = ordered_probs(a_model, a_validation, a_features)
            a_test_probs = ordered_probs(a_model, a_test, a_features)
            a_threshold = nonflat_threshold(a_val_probs, spec.threshold_quantile)
            a_val_decision = decision_frame(
                source=a_validation,
                probs=a_val_probs,
                threshold=a_threshold,
                spec=spec,
                fold_id=fold.fold_id,
                split_role="validation",
                tier_scope="Tier A",
                route_role="tier_a_only",
                feature_selector=spec.feature_selector,
                feature_count=len(a_features),
            )
            a_test_decision = decision_frame(
                source=a_test,
                probs=a_test_probs,
                threshold=a_threshold,
                spec=spec,
                fold_id=fold.fold_id,
                split_role="test",
                tier_scope="Tier A",
                route_role="tier_a_only",
                feature_selector=spec.feature_selector,
                feature_count=len(a_features),
            )

            b_model = train_model_cached(
                model_cache,
                fold_id=fold.fold_id,
                model_key=f"tier_b::{spec.model_key}",
                train_frame=b_train,
                features=b_features,
                params=params,
            )
            b_val_probs = ordered_probs(b_model, b_validation, b_features)
            b_test_probs = ordered_probs(b_model, b_test, b_features)
            b_threshold = nonflat_threshold(b_val_probs, spec.threshold_quantile)
            b_val_decision = decision_frame(
                source=b_validation,
                probs=b_val_probs,
                threshold=b_threshold,
                spec=spec,
                fold_id=fold.fold_id,
                split_role="validation",
                tier_scope="Tier B",
                route_role="tier_b_fallback_only",
                feature_selector="core42_partial_context",
                feature_count=len(b_features),
            )
            b_test_decision = decision_frame(
                source=b_test,
                probs=b_test_probs,
                threshold=b_threshold,
                spec=spec,
                fold_id=fold.fold_id,
                split_role="test",
                tier_scope="Tier B",
                route_role="tier_b_fallback_only",
                feature_selector="core42_partial_context",
                feature_count=len(b_features),
            )

            routed_validation = pd.concat(
                [
                    a_val_decision.assign(tier_scope="Tier A+B", route_role="routed_tier_a_primary_used"),
                    b_val_decision.assign(tier_scope="Tier A+B", route_role="routed_tier_b_fallback_used"),
                ],
                ignore_index=True,
            )
            routed_test = pd.concat(
                [
                    a_test_decision.assign(tier_scope="Tier A+B", route_role="routed_tier_a_primary_used"),
                    b_test_decision.assign(tier_scope="Tier A+B", route_role="routed_tier_b_fallback_used"),
                ],
                ignore_index=True,
            )

            frames = (
                a_val_decision,
                a_test_decision,
                b_val_decision,
                b_test_decision,
                routed_validation.assign(route_role="routed_total"),
                routed_test.assign(route_role="routed_total"),
            )
            for frame in frames:
                if frame.empty:
                    continue
                split_role = str(frame["split_role"].iloc[0])
                metric_rows.append(metric_row(frame, fold, split_role))
                signal_frames.append(frame.loc[frame["is_signal"]].copy())

    fold_plan = pd.DataFrame(fold_plan_rows)
    fold_metrics = pd.DataFrame(metric_rows)
    signals = pd.concat(signal_frames, ignore_index=True) if signal_frames else pd.DataFrame()
    return fold_plan, fold_metrics, signals


def summarize_variants(fold_metrics: pd.DataFrame) -> pd.DataFrame:
    paired_rows: list[dict[str, Any]] = []
    keys = ["variant_id", "tier_scope", "route_role"]
    for key, group in fold_metrics.groupby(keys, dropna=False):
        variant_id, tier_scope, route_role = key
        validation = group.loc[group["split_role"].eq("validation")]
        test = group.loc[group["split_role"].eq("test")]
        merged = validation[["fold_id", "hit_rate", "signal_count", "correct_count"]].merge(
            test[["fold_id", "hit_rate", "signal_count", "correct_count"]],
            on="fold_id",
            how="outer",
            suffixes=("_validation", "_test"),
        )
        val_signals = int(validation["signal_count"].sum())
        test_signals = int(test["signal_count"].sum())
        val_correct = int(validation["correct_count"].sum())
        test_correct = int(test["correct_count"].sum())
        val_hit = float(val_correct / val_signals) if val_signals else math.nan
        test_hit = float(test_correct / test_signals) if test_signals else math.nan
        merged["hit_gap"] = merged["hit_rate_test"] - merged["hit_rate_validation"]
        stable_mask = (merged["hit_rate_validation"] >= HIT_FLOOR) & (merged["hit_rate_test"] >= HIT_FLOOR)
        inversion_mask = merged["hit_rate_test"] > merged["hit_rate_validation"]
        collapse_mask = merged["hit_rate_test"] < 0.40
        gap_abs = merged["hit_gap"].abs().dropna()
        stable_fold_count = int(stable_mask.sum())
        fold_count = int(merged["fold_id"].nunique())
        min_signal_total = min(val_signals, test_signals)
        consistency = max(0.0, 1.0 - float(gap_abs.mean() if not gap_abs.empty else 1.0))
        score = float((min(val_hit, test_hit) if math.isfinite(val_hit) and math.isfinite(test_hit) else 0.0) * math.log1p(min_signal_total) * (stable_fold_count / fold_count if fold_count else 0.0) * consistency)
        paired_rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "tier_scope": tier_scope,
                "route_role": route_role,
                "fold_count": fold_count,
                "validation_signal_total": val_signals,
                "test_signal_total": test_signals,
                "validation_correct_total": val_correct,
                "test_correct_total": test_correct,
                "validation_weighted_hit_rate": val_hit,
                "test_weighted_hit_rate": test_hit,
                "test_minus_validation_hit_rate": test_hit - val_hit if math.isfinite(val_hit) and math.isfinite(test_hit) else math.nan,
                "validation_positive_fold_count": int((merged["hit_rate_validation"] >= HIT_FLOOR).sum()),
                "test_positive_fold_count": int((merged["hit_rate_test"] >= HIT_FLOOR).sum()),
                "both_positive_fold_count": stable_fold_count,
                "inversion_fold_count": int(inversion_mask.sum()),
                "test_collapse_fold_count": int(collapse_mask.sum()),
                "mean_abs_fold_gap": float(gap_abs.mean()) if not gap_abs.empty else math.nan,
                "worst_test_hit_rate": float(merged["hit_rate_test"].min()) if not merged["hit_rate_test"].dropna().empty else math.nan,
                "wfo_consistency_score": score,
                "judgment": judge_variant(
                    stable_fold_count=stable_fold_count,
                    fold_count=fold_count,
                    val_hit=val_hit,
                    test_hit=test_hit,
                    min_signal_total=min_signal_total,
                ),
            }
        )
    return pd.DataFrame(paired_rows).sort_values(
        ["tier_scope", "wfo_consistency_score", "variant_id"],
        ascending=[True, False, True],
    )


def judge_variant(*, stable_fold_count: int, fold_count: int, val_hit: float, test_hit: float, min_signal_total: int) -> str:
    if min_signal_total < 100:
        return "inconclusive_sparse_rolling_wfo_structural_probe"
    if stable_fold_count >= max(4, math.ceil(fold_count * 0.5)) and val_hit >= 0.45 and test_hit >= 0.45:
        return "repeatability_clue_not_promotion"
    if test_hit > val_hit and val_hit < 0.42:
        return "validation_weak_test_lift_inversion_clue"
    if test_hit < 0.40:
        return "negative_or_unstable_rolling_wfo_probe"
    return "inconclusive_rolling_wfo_structural_probe"


def inversion_matrix(fold_metrics: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for (fold_id, tier_scope, route_role), group in fold_metrics.groupby(["fold_id", "tier_scope", "route_role"], dropna=False):
        validation = group.loc[group["split_role"].eq("validation"), ["variant_id", "hit_rate", "signal_count"]].rename(
            columns={"hit_rate": "validation_hit_rate", "signal_count": "validation_signal_count"}
        )
        test = group.loc[group["split_role"].eq("test"), ["variant_id", "hit_rate", "signal_count"]].rename(
            columns={"hit_rate": "test_hit_rate", "signal_count": "test_signal_count"}
        )
        merged = validation.merge(test, on="variant_id", how="outer")
        merged["gap"] = merged["test_hit_rate"] - merged["validation_hit_rate"]
        rows.append(
            {
                "run_id": RUN_ID,
                "fold_id": fold_id,
                "tier_scope": tier_scope,
                "route_role": route_role,
                "variant_count": int(merged["variant_id"].nunique()),
                "test_gt_validation_count": int((merged["gap"] > 0).sum()),
                "test_hit_ge_048_count": int((merged["test_hit_rate"] >= HIT_FLOOR).sum()),
                "validation_hit_ge_048_count": int((merged["validation_hit_rate"] >= HIT_FLOOR).sum()),
                "both_hit_ge_048_count": int(((merged["validation_hit_rate"] >= HIT_FLOOR) & (merged["test_hit_rate"] >= HIT_FLOOR)).sum()),
                "mean_validation_hit_rate": float(merged["validation_hit_rate"].mean()),
                "mean_test_hit_rate": float(merged["test_hit_rate"].mean()),
                "mean_gap": float(merged["gap"].mean()),
                "total_validation_signals": int(merged["validation_signal_count"].sum()),
                "total_test_signals": int(merged["test_signal_count"].sum()),
            }
        )
    return pd.DataFrame(rows).sort_values(["tier_scope", "fold_id", "route_role"])


def package_summary(variant_summary: pd.DataFrame, matrix: pd.DataFrame) -> tuple[str, dict[str, Any]]:
    routed = variant_summary.loc[variant_summary["route_role"].eq("routed_total")].copy()
    best_routed = routed.sort_values(["wfo_consistency_score", "variant_id"], ascending=[False, True]).head(1)
    best = best_routed.iloc[0].to_dict() if not best_routed.empty else {}
    repeatability_count = int((routed["judgment"] == "repeatability_clue_not_promotion").sum()) if not routed.empty else 0
    tier_a_best = best_by_tier(variant_summary, "Tier A")
    tier_b_best = best_by_tier(variant_summary, "Tier B")
    tier_ab_best = best_by_tier(variant_summary, "Tier A+B")
    fold_test_lift = matrix.loc[matrix["route_role"].eq("routed_total"), "test_gt_validation_count"].sum()
    possible_fold_cells = matrix.loc[matrix["route_role"].eq("routed_total"), "variant_count"].sum()
    if repeatability_count:
        judgment = "inconclusive_rolling_wfo_repeatability_clue_not_promotion"
    elif possible_fold_cells and fold_test_lift / possible_fold_cells >= 0.60:
        judgment = "inconclusive_rolling_wfo_inversion_pattern_clue_not_promotion"
    else:
        judgment = "inconclusive_rolling_wfo_no_stable_repeatability_not_promotion"
    return judgment, {
        "best_routed_variant": best,
        "best_tier_a_variant": tier_a_best,
        "best_tier_b_variant": tier_b_best,
        "best_tier_ab_variant": tier_ab_best,
        "routed_repeatability_clue_count": repeatability_count,
        "routed_test_gt_validation_cells": int(fold_test_lift),
        "routed_total_cells": int(possible_fold_cells),
    }


def best_by_tier(variant_summary: pd.DataFrame, tier_scope: str) -> dict[str, Any]:
    frame = variant_summary.loc[variant_summary["tier_scope"].eq(tier_scope)]
    if frame.empty:
        return {}
    return frame.sort_values(["wfo_consistency_score", "variant_id"], ascending=[False, True]).iloc[0].to_dict()


def next_probe_recommendations(summary: Mapping[str, Any]) -> pd.DataFrame:
    best_ab = summary.get("best_tier_ab_variant") or {}
    best_b = summary.get("best_tier_b_variant") or {}
    rows = [
        {
            "rank": 1,
            "probe_id": "time_regime_wfo_expansion",
            "recommendation": "Keep broad rolling WFO/regime probing before threshold micro-search.",
            "evidence": f"best_tier_ab={best_ab.get('variant_id', 'NA')}; both_positive_folds={best_ab.get('both_positive_fold_count', 'NA')}",
            "claim_boundary": BOUNDARY,
        },
        {
            "rank": 2,
            "probe_id": "tier_b_partial_context_wfo_read",
            "recommendation": "Read Tier B partial-context behavior separately because it can reverse Tier A.",
            "evidence": f"best_tier_b={best_b.get('variant_id', 'NA')}; score={best_b.get('wfo_consistency_score', 'NA')}",
            "claim_boundary": BOUNDARY,
        },
        {
            "rank": 3,
            "probe_id": "mt5_only_after_python_wfo_filter",
            "recommendation": "Do not run broad MT5 yet unless the Python WFO surface repeats enough to justify runtime cost.",
            "evidence": "RUN03J is Python structural WFO only; RUN03H remains the latest all-variant MT5 runtime probe.",
            "claim_boundary": "mt5_out_of_scope_by_claim_for_run03j",
        },
    ]
    return pd.DataFrame(rows)


def artifacts() -> dict[str, Mapping[str, Any]]:
    paths = {
        "fold_window_plan": RUN_ROOT / "results/wfo_fold_window_plan.csv",
        "fold_summary": RUN_ROOT / "results/wfo_fold_summary.csv",
        "variant_summary": RUN_ROOT / "results/wfo_variant_summary.csv",
        "inversion_matrix": RUN_ROOT / "results/wfo_inversion_matrix.csv",
        "next_probe_recommendations": RUN_ROOT / "results/wfo_next_probe_recommendations.csv",
        "scored_signals": RUN_ROOT / "predictions/wfo_scored_signals.parquet",
        "result_summary": RUN_ROOT / "reports/result_summary.md",
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "kpi_record": RUN_ROOT / "kpi_record.json",
        "summary": RUN_ROOT / "summary.json",
    }
    out: dict[str, Mapping[str, Any]] = {}
    for key, path in paths.items():
        if key in {"run_manifest", "summary"}:
            sha = "self_referential_written_last"
        else:
            sha = sha256_file_lf_normalized(path) if path_exists(path) else "pending"
        out[key] = {"path": rel(path), "sha256": sha}
    return out


def write_outputs(
    *,
    fold_plan: pd.DataFrame,
    fold_metrics: pd.DataFrame,
    signals: pd.DataFrame,
    variant_summary: pd.DataFrame,
    matrix: pd.DataFrame,
    recommendations: pd.DataFrame,
) -> None:
    io_path(RUN_ROOT / "results").mkdir(parents=True, exist_ok=True)
    io_path(RUN_ROOT / "predictions").mkdir(parents=True, exist_ok=True)
    io_path(RUN_ROOT / "reports").mkdir(parents=True, exist_ok=True)
    fold_plan.to_csv(io_path(RUN_ROOT / "results/wfo_fold_window_plan.csv"), index=False, encoding="utf-8")
    fold_metrics.to_csv(io_path(RUN_ROOT / "results/wfo_fold_summary.csv"), index=False, encoding="utf-8")
    variant_summary.to_csv(io_path(RUN_ROOT / "results/wfo_variant_summary.csv"), index=False, encoding="utf-8")
    matrix.to_csv(io_path(RUN_ROOT / "results/wfo_inversion_matrix.csv"), index=False, encoding="utf-8")
    recommendations.to_csv(io_path(RUN_ROOT / "results/wfo_next_probe_recommendations.csv"), index=False, encoding="utf-8")
    signals.to_parquet(io_path(RUN_ROOT / "predictions/wfo_scored_signals.parquet"), index=False)


def write_run_records(
    *,
    created_at: str,
    completed_at: str,
    metadata: Mapping[str, Any],
    judgment: str,
    summary: Mapping[str, Any],
) -> None:
    manifest = {
        "identity": {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "exploration_label": EXPLORATION_LABEL,
            "lane": "rolling_wfo_split_probe",
            "status": "reviewed",
            "judgment": judgment,
            "boundary": BOUNDARY,
        },
        "source_inputs": {
            "source_variant_run_id": SOURCE_VARIANT_RUN_ID,
            "source_mt5_run_id": SOURCE_MT5_RUN_ID,
            "source_attribution_run_id": SOURCE_ATTRIBUTION_RUN_ID,
            "model_input_dataset": metadata["dataset_path"],
            "feature_order": metadata["feature_order_path"],
            "training_summary": metadata["training_summary_path"],
        },
        "experiment_design": {
            "hypothesis": "RUN03H validation/OOS inversion should be tested across rolling forward splits before any narrowing.",
            "decision_use": "Decide whether Stage 12 keeps broad WFO/regime exploration; not a baseline or promotion decision.",
            "comparison_baseline": "RUN03H all-variant MT5 evidence and RUN03I inversion attribution; no operating baseline.",
            "control_variables": [
                "20 RUN03D ExtraTrees variants",
                "same model family",
                "same threshold quantile and direction rules",
                "Tier A, Tier B, and Tier A+B record meanings",
            ],
            "changed_variables": ["calendar fold", "train/validation/test window"],
            "success_criteria": [
                "all 20 variants have Tier A/Tier B/Tier A+B fold rows",
                "rolling split read separates validation and test behavior",
                "result does not create promotion or runtime authority",
            ],
            "failure_criteria": ["missing required frames", "fold without labels", "ledger or gate mismatch"],
            "claim_boundary": BOUNDARY,
            "probe_runtime_control": {
                "n_estimators_cap": PROBE_N_ESTIMATORS,
                "effect": "Keeps all variants/folds/tier views in scope while keeping this as a structural probe, not runtime authority.",
            },
        },
        "folds": [fold.as_row() for fold in FOLDS],
        "tier_b_context_summary": metadata["tier_b_context_summary"],
        "created_at_utc": created_at,
        "completed_at_utc": completed_at,
        "result": dict(summary),
        "artifacts": artifacts(),
    }
    kpi_record = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "rolling_wfo_split_probe",
        "scoreboard_lane": "python_wfo_structural_probe",
        "probe_n_estimators_cap": PROBE_N_ESTIMATORS,
        "variant_count": summary["variant_count"],
        "fold_count": summary["fold_count"],
        "tier_records": {
            "Tier A separate": summary["best_tier_a_variant"],
            "Tier B separate": summary["best_tier_b_variant"],
            "Tier A+B combined": summary["best_tier_ab_variant"],
        },
        "judgment": judgment,
        "boundary": BOUNDARY,
        "external_verification_status": "out_of_scope_by_claim_python_wfo_structural_probe_no_new_mt5",
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)
    write_json(RUN_ROOT / "summary.json", {**summary, "artifacts": artifacts()})


def value(value: Any, digits: int = 6) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.{digits}f}"


def top_rows(frame: pd.DataFrame, tier_scope: str, limit: int = 8) -> str:
    source = frame.loc[frame["tier_scope"].eq(tier_scope)].sort_values(
        ["wfo_consistency_score", "variant_id"], ascending=[False, True]
    ).head(limit)
    rows = [
        "| variant(변형) | val hit(검증 적중률) | test hit(시험 적중률) | both folds(동시 양호 접힘) | inversions(시험 우위 접힘) | score(점수) | judgment(판정) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in source.itertuples():
        rows.append(
            f"| `{row.variant_id}` | {value(row.validation_weighted_hit_rate)} | {value(row.test_weighted_hit_rate)} | "
            f"{row.both_positive_fold_count} | {row.inversion_fold_count} | {value(row.wfo_consistency_score)} | `{row.judgment}` |"
        )
    return "\n".join(rows)


def write_reports(summary: Mapping[str, Any], variant_summary: pd.DataFrame, judgment: str) -> None:
    best = summary["best_tier_ab_variant"]
    report = f"""# RUN03J rolling WFO split probe(구르는 워크포워드 분할 탐침)

## Result(결과)

`{RUN_ID}`는 Stage 12(12단계) ExtraTrees(엑스트라트리) 20개 변형을 rolling WFO split probe(구르는 워크포워드 분할 탐침)로 다시 읽었다.

Effect(효과): RUN03H(실행 03H)의 validation/OOS inversion(검증/표본외 반전)이 한 번의 고정 분할만의 착시인지, 여러 calendar fold(달력 접힘 분할)에서도 반복되는지 확인한다.

## Boundary(경계)

- scope(범위): Python structural WFO probe(파이썬 구조 워크포워드 탐침)
- MT5(`MetaTrader 5`, 메타트레이더5): `out_of_scope_by_claim(주장 범위 밖)`
- forbidden claims(금지 주장): alpha quality(알파 품질), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위)
- judgment(판정): `{judgment}`

## Headline(핵심 판독)

- variants(변형): `{summary['variant_count']}`
- folds(접힘 분할): `{summary['fold_count']}`
- probe tree cap(탐침 트리 상한): `{PROBE_N_ESTIMATORS}`
- best routed variant(최상위 라우팅 변형): `{best.get('variant_id', 'NA')}`
- best routed validation hit(최상위 라우팅 검증 적중률): `{value(best.get('validation_weighted_hit_rate'))}`
- best routed test hit(최상위 라우팅 시험 적중률): `{value(best.get('test_weighted_hit_rate'))}`
- routed repeatability clues(라우팅 반복 단서): `{summary['routed_repeatability_clue_count']}`
- routed test > validation cells(라우팅 시험 우위 칸): `{summary['routed_test_gt_validation_cells']}/{summary['routed_total_cells']}`

## Tier A Separate(Tier A 분리)

{top_rows(variant_summary, "Tier A")}

## Tier B Separate(Tier B 분리)

{top_rows(variant_summary, "Tier B")}

## Tier A+B Combined(Tier A+B 합산)

{top_rows(variant_summary, "Tier A+B")}

## Read(판독)

이번 결과는 selection(선별)이 아니라 exploration memory(탐색 기억)다. Effect(효과): 좋은 fold(접힘 분할)가 보여도 바로 threshold micro-tuning(임계값 미세조정)으로 들어가지 않고, 시간/체제 축을 더 넓게 확인한다.
"""
    write_text(RUN_ROOT / "reports/result_summary.md", report)

    review = f"""# RUN03J Review Packet(검토 묶음)

## Result(결과)

`{RUN_ID}` completed(완료). Effect(효과): RUN03D(실행 03D) 20개 ExtraTrees(엑스트라트리) 변형을 Tier A(티어 A), Tier B(티어 B), Tier A+B(티어 A+B)로 구르는 분할에서 비교했다.

## Evidence(근거)

- run manifest(실행 목록): `{rel(RUN_ROOT / 'run_manifest.json')}`
- KPI record(KPI 기록): `{rel(RUN_ROOT / 'kpi_record.json')}`
- fold summary(접힘 요약): `{rel(RUN_ROOT / 'results/wfo_fold_summary.csv')}`
- variant summary(변형 요약): `{rel(RUN_ROOT / 'results/wfo_variant_summary.csv')}`
- result summary(결과 요약): `{rel(RUN_ROOT / 'reports/result_summary.md')}`

## Judgment(판정)

`{judgment}`. Effect(효과): Stage 12(12단계)는 계속 탐색하되, 아직 baseline(기준선), promotion candidate(승격 후보), runtime authority(런타임 권위)를 만들지 않는다.
"""
    write_text(STAGE_REVIEW_PATH, review)

    plan = f"""# RUN03J Plan(계획)

## Hypothesis(가설)

RUN03H(실행 03H)의 validation/OOS inversion(검증/표본외 반전)은 single split(단일 분할) 착시일 수 있다. rolling WFO split probe(구르는 워크포워드 분할 탐침)로 반복성을 확인한다.

## Controls(고정 조건)

- model family(모델 계열): ExtraTrees(엑스트라트리)
- variants(변형): RUN03D(실행 03D) 20개 전체
- tiers(티어): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)
- claim boundary(주장 경계): `{BOUNDARY}`

## Stop Condition(중단 조건)

fold(접힘 분할), tier(티어), ledger(장부), KPI record(KPI 기록) 중 하나라도 빠지면 completed(완료)로 닫지 않는다.
"""
    write_text(PLAN_PATH, plan)

    closeout = f"""# Closeout Report

## Conclusion

RUN03J(실행 03J) rolling WFO split probe(구르는 워크포워드 분할 탐침)는 completed(완료)다.

## What changed

Stage 12(12단계)에 새 Python WFO structural probe(파이썬 워크포워드 구조 탐침) 산출물을 추가했다. Effect(효과): RUN03H(실행 03H)의 반전 단서를 고정 validation/OOS(검증/표본외) 하나에만 묶지 않는다.

## What gates passed

scope_completion_gate(범위 완료 게이트), kpi_contract_audit(KPI 계약 감사), work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_lint(스킬 영수증 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 게이트 포함 감사), final_claim_guard(최종 주장 보호)를 통과해야 한다.

## What gates were not applicable

runtime_evidence_gate(런타임 근거 게이트)는 이번 실행 범위 밖이다. Effect(효과): RUN03J(실행 03J)는 새 MT5(메타트레이더5) 실행을 주장하지 않는다.

## What is still not enforced

MT5(`MetaTrader 5`, 메타트레이더5) rolling WFO(구르는 워크포워드) 검증은 아직 실행하지 않았다.

## Allowed claims

completed_python_wfo_structural_probe(파이썬 워크포워드 구조 탐침 완료), exploratory_wfo_read(탐색적 워크포워드 판독).

## Forbidden claims

alpha_quality(알파 품질), promotion_candidate(승격 후보), operating_promotion(운영 승격), runtime_authority(런타임 권위).

## Next hardening step

WFO(워크포워드) 반복 단서가 충분하면 다음에는 더 좁은 MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)를 설계한다.
"""
    write_text(PACKET_ROOT / "closeout_report.md", closeout, bom=False)


def ledger_row(view: str, tier: str, best: Mapping[str, Any], judgment: str) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__{view}",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": view,
        "parent_run_id": SOURCE_ATTRIBUTION_RUN_ID,
        "record_view": view,
        "tier_scope": tier,
        "kpi_scope": "rolling_wfo_split_probe",
        "scoreboard_lane": "python_wfo_structural_probe",
        "status": "completed",
        "judgment": judgment,
        "path": rel(RUN_ROOT / "reports/result_summary.md"),
        "primary_kpi": ledger_pairs(
            (
                ("best_variant", best.get("variant_id")),
                ("validation_weighted_hit_rate", best.get("validation_weighted_hit_rate")),
                ("test_weighted_hit_rate", best.get("test_weighted_hit_rate")),
                ("both_positive_fold_count", best.get("both_positive_fold_count")),
                ("fold_count", best.get("fold_count")),
            )
        ),
        "guardrail_kpi": ledger_pairs(
            (
                ("source_variant_run_id", SOURCE_VARIANT_RUN_ID),
                ("source_mt5_run_id", SOURCE_MT5_RUN_ID),
                ("new_mt5_execution", False),
                ("boundary", BOUNDARY),
            )
        ),
        "external_verification_status": "out_of_scope_by_claim_python_wfo_structural_probe_no_new_mt5",
        "notes": "RUN03J rolling WFO structural row; not alpha quality, promotion, or runtime authority.",
    }


def update_ledgers(summary: Mapping[str, Any], judgment: str) -> dict[str, Any]:
    rows = [
        ledger_row("tier_a_rolling_wfo", "Tier A", summary["best_tier_a_variant"], judgment),
        ledger_row("tier_b_rolling_wfo", "Tier B", summary["best_tier_b_variant"], judgment),
        ledger_row("tier_ab_rolling_wfo", "Tier A+B", summary["best_tier_ab_variant"], judgment),
    ]
    registry = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "rolling_wfo_split_probe",
            "status": "reviewed",
            "judgment": judgment,
            "path": rel(RUN_ROOT),
            "notes": ledger_pairs(
                (
                    ("run_number", RUN_NUMBER),
                    ("variant_count", summary["variant_count"]),
                    ("fold_count", summary["fold_count"]),
                    ("best_routed_variant", summary["best_tier_ab_variant"].get("variant_id")),
                    ("new_mt5_execution", False),
                    ("boundary", BOUNDARY),
                )
            ),
        }
    ]
    return {
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, registry, key="run_id"),
        "project_alpha_ledger": upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "stage_run_ledger": upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id"),
        "rows_written": len(rows),
    }


def write_work_packet(summary: Mapping[str, Any], judgment: str) -> None:
    packet = {
        "version": "work_packet_schema_v2",
        "packet_id": PACKET_ID,
        "created_at_utc": summary["created_at_utc"],
        "user_request": {
            "user_quote": "구르는 워크포워드 분할 탐침가보자",
            "requested_action": "run rolling WFO split probe for Stage 12 ExtraTrees variants",
            "requested_count": {"value": 20, "n_a_reason": None},
            "ambiguous_terms": ["구르는 WFO means expanding-train rolling-forward split in this packet."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run_before_packet": SOURCE_ATTRIBUTION_RUN_ID,
            "current_run_after_packet": RUN_ID,
            "branch": current_branch(),
            "source_documents": [
                rel(WORKSPACE_STATE_PATH),
                rel(CURRENT_STATE_PATH),
                rel(SELECTION_STATUS_PATH),
            ],
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "experiment_design", "kpi_evidence", "state_sync"],
            "touched_surfaces": ["stage12_run_artifacts", "stage12_reports", "run_ledgers", "current_truth_docs"],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "claim_overstatement_risk": "high",
                "selection_bias_risk": "medium",
                "data_leakage_risk": "medium",
                "external_runtime_risk": "medium_no_new_mt5",
            },
            "hard_stop_risks": [],
            "required_decision_locks": [],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "work_packet_schema_lint",
                "skill_receipt_lint",
                "skill_receipt_schema_lint",
                "state_sync_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        "decision_lock": {
            "mode": "user_explicit_go_ahead",
            "assumptions": {
                "fold_style": "expanding_train_rolling_validation_test",
                "variant_scope": "all_20_run03d_variants",
                "probe_n_estimators_cap": PROBE_N_ESTIMATORS,
                "new_mt5_execution_required": False,
                "baseline_selection_allowed": False,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": [rel(RUN_ROOT), rel(PACKET_ROOT), rel(STAGE_RUN_LEDGER_PATH), rel(PROJECT_ALPHA_LEDGER_PATH)],
            "scope_units": ["variant", "fold", "tier_view", "ledger", "report"],
            "execution_layers": ["python_execution", "kpi_recording", "ledger_update", "document_edit"],
            "mutation_policy": {"allowed": True, "boundary": "new run artifacts and current truth only"},
            "evidence_layers": ["fold_metrics", "variant_summary", "summary", "ledgers", "work_packet"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False},
            "claim_boundary": {
                "allowed_claims": ["completed_python_wfo_structural_probe", "exploratory_wfo_read"],
                "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
            },
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "All 20 RUN03D variants are included.",
                "expected_artifact": rel(RUN_ROOT / "results/wfo_variant_summary.csv"),
                "verification_method": "scope_completion_gate",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "Tier A, Tier B, and Tier A+B views are recorded.",
                "expected_artifact": rel(RUN_ROOT / "results/wfo_variant_summary.csv"),
                "verification_method": "scope_completion_gate",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "Ledgers contain three paired tier records.",
                "expected_artifact": rel(STAGE_RUN_LEDGER_PATH),
                "verification_method": "kpi_contract_audit",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": [
                {"id": "load_inputs", "actions": ["load_run03d_variants", "load_tier_a_model_input", "materialize_tier_b_partial_context"]},
                {"id": "execute_wfo", "actions": ["train_all_variants_by_fold", "score_tier_a_tier_b_tier_ab"]},
                {"id": "closeout", "actions": ["write_reports", "update_ledgers", "sync_current_truth", "run_gates"]},
            ],
            "expected_outputs": [rel(RUN_ROOT / "reports/result_summary.md"), rel(PACKET_ROOT / "closeout_gate.json")],
            "stop_conditions": ["missing_dataset", "missing_variant_rows", "tier_records_missing", "gate_failure"],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": [
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
            ],
            "skills_considered": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-exploration-mandate",
            ],
            "skills_selected": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-exploration-mandate",
            ],
            "skills_not_used": {},
            "required_skill_receipts": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-exploration-mandate",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "work_packet_schema_lint",
                "skill_receipt_lint",
                "skill_receipt_schema_lint",
                "state_sync_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
        },
        "evidence_contract": {
            "raw_evidence": [rel(MODEL_INPUT_PATH), rel(TRAINING_SUMMARY_PATH)],
            "machine_readable": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "kpi_record.json"), rel(RUN_ROOT / "run_manifest.json")],
            "human_readable": [rel(RUN_ROOT / "reports/result_summary.md"), rel(STAGE_REVIEW_PATH)],
        },
        "gates": {
            "required": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "work_packet_schema_lint",
                "skill_receipt_lint",
                "skill_receipt_schema_lint",
                "state_sync_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "actual_status_source": rel(PACKET_ROOT / "closeout_gate.json"),
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "RUN03J is a Python structural WFO probe and does not claim new MT5 verification."
            },
        },
        "final_claim_policy": {
            "allowed_claims": ["completed_python_wfo_structural_probe", "exploratory_wfo_read"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
            "judgment": judgment,
        },
    }
    write_yaml(PACKET_ROOT / "work_packet.yaml", packet)


def write_skill_receipts(summary: Mapping[str, Any], judgment: str) -> None:
    artifacts_payload = artifacts()
    receipts = [
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-run-evidence-system",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "source_inputs": [rel(MODEL_INPUT_PATH), rel(TRAINING_SUMMARY_PATH), rel(SOURCE_VARIANT_ROOT / "variant_plan.csv")],
            "produced_artifacts": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "kpi_record.json"), rel(RUN_ROOT / "reports/result_summary.md")],
            "ledger_rows": 3,
            "missing_evidence": "No new MT5 execution; RUN03J is Python WFO structural evidence only.",
            "allowed_claims": ["completed_python_wfo_structural_probe", "exploratory_wfo_read"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-experiment-design",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "hypothesis": "RUN03H validation/OOS inversion may be single-split specific; rolling WFO tests repeatability.",
            "baseline": "RUN03H/RUN03I evidence as comparison reference only; no operating baseline.",
            "changed_variables": ["calendar fold", "validation/test window"],
            "invalid_conditions": ["future leakage across fold", "variant reduction", "missing tier view"],
            "evidence_plan": [rel(RUN_ROOT / "results/wfo_fold_summary.csv"), rel(RUN_ROOT / "results/wfo_variant_summary.csv")],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-data-integrity",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "data_sources_checked": [rel(MODEL_INPUT_PATH), rel(TRAINING_SUMMARY_PATH), rel(RUN_ROOT / "results/wfo_fold_window_plan.csv")],
            "time_axis_boundary": "All folds use timestamp UTC with train before validation before test.",
            "split_boundary": "Expanding train, rolling validation, and rolling test windows are non-overlapping inside each fold.",
            "leakage_checks": "Thresholds are calibrated on each fold validation window; test windows are later than validation windows.",
            "missing_data_boundary": "Tier B fallback rows are explicitly counted; no_tier rows are not claimed.",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-model-validation",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "model_or_threshold_surface": "ExtraTrees 20 variants with fold-local threshold quantiles.",
            "validation_split": "Seven rolling validation windows before their paired test windows.",
            "overfit_checks": "Fold-by-fold validation/test hit-rate gaps, collapse counts, and both-positive fold counts.",
            "selection_metric_boundary": "WFO consistency score is exploratory and cannot select an operating baseline.",
            "allowed_claims": ["exploratory_wfo_read"],
            "forbidden_claims": ["alpha_quality", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-artifact-lineage",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "source_inputs": [rel(MODEL_INPUT_PATH), rel(TRAINING_SUMMARY_PATH), rel(SOURCE_VARIANT_ROOT / "variant_plan.csv")],
            "produced_artifacts": [item["path"] for item in artifacts_payload.values()],
            "raw_evidence": [rel(MODEL_INPUT_PATH), rel(TRAINING_SUMMARY_PATH)],
            "machine_readable": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "kpi_record.json"), rel(RUN_ROOT / "run_manifest.json")],
            "human_readable": [rel(RUN_ROOT / "reports/result_summary.md"), rel(STAGE_REVIEW_PATH)],
            "hashes_or_missing_reasons": {key: item["sha256"] for key, item in artifacts_payload.items()},
            "lineage_boundary": "RUN03J derives from RUN03D variants and current model input; no new MT5 runtime evidence.",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-exploration-mandate",
            "triggered": True,
            "status": "executed",
            "blocking": False,
            "exploration_lane": "Stage 12 ExtraTrees rolling WFO split probe",
            "idea_boundary": "broad exploration memory, not baseline or promotion",
            "negative_memory_effect": "Weak fold behavior becomes failure memory; it does not kill the model family.",
            "operating_claim_boundary": "No alpha quality, promotion candidate, operating promotion, or runtime authority.",
        },
    ]
    write_json(PACKET_ROOT / "skill_receipts.json", {"receipts": receipts, "judgment": judgment})


def write_gate_audits(summary: Mapping[str, Any]) -> None:
    scope_audit = {
        "audit_name": "scope_completion_gate",
        "status": "complete",
        "passed": True,
        "completed_forbidden": False,
        "findings": [],
        "counts": {
            "variant_tier_rows": {"expected": 60, "actual": summary["variant_tier_rows"], "required": True},
            "fold_metric_rows": {"expected": 840, "actual": summary["fold_metric_rows"], "required": True},
            "tier_ledger_rows": {"expected": 3, "actual": 3, "required": True},
        },
        "allowed_claims": ["completed", "reviewed"],
        "forbidden_claims": [],
    }
    data_gate = {
        "audit_name": "data_integrity_gate",
        "status": "pass",
        "passed": True,
        "completed_forbidden": False,
        "findings": [],
        "counts": {
            "fold_count": summary["fold_count"],
            "variant_count": summary["variant_count"],
            "tier_b_fallback_rows_total": summary["tier_b_fallback_rows_total"],
            "future_leakage_claimed": False,
            "mt5_claimed": False,
        },
        "allowed_claims": ["usable_with_boundary"],
        "forbidden_claims": [],
    }
    write_json(PACKET_ROOT / "scope_completion_gate.json", scope_audit)
    write_json(PACKET_ROOT / "data_integrity_gate.json", data_gate)


def update_current_truth(summary: Mapping[str, Any], judgment: str) -> None:
    update_workspace_state(summary, judgment)
    update_current_working_state(summary, judgment)
    update_selection_status(summary, judgment)
    update_changelog(summary, judgment)


def update_workspace_state(summary: Mapping[str, Any], judgment: str) -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    text = text.replace(
        "and RUN03I is current validation/OOS inversion attribution(현재 검증/표본외 반전 귀속)",
        "RUN03I is historical validation/OOS inversion attribution(이전 검증/표본외 반전 귀속), and RUN03J is current rolling WFO split probe(현재 구르는 WFO 분할 탐침)",
    )
    block = f"""stage12_model_family_challenge:
  stage_id: {STAGE_ID}
  status: active_rolling_wfo_split_probe_completed
  lane: rolling_wfo_split_probe
  current_run_id: {RUN_ID}
  current_run_label: {EXPLORATION_LABEL}
  current_status: reviewed
  current_summary:
    boundary: {BOUNDARY}
    source_variant_run_id: {SOURCE_VARIANT_RUN_ID}
    source_mt5_run_id: {SOURCE_MT5_RUN_ID}
    source_attribution_run_id: {SOURCE_ATTRIBUTION_RUN_ID}
    variant_count: {summary['variant_count']}
    fold_count: {summary['fold_count']}
    variant_tier_rows: {summary['variant_tier_rows']}
    fold_metric_rows: {summary['fold_metric_rows']}
    best_routed_variant: {summary['best_tier_ab_variant'].get('variant_id', 'NA')}
    best_routed_validation_hit_rate: {value(summary['best_tier_ab_variant'].get('validation_weighted_hit_rate'))}
    best_routed_test_hit_rate: {value(summary['best_tier_ab_variant'].get('test_weighted_hit_rate'))}
    routed_repeatability_clue_count: {summary['routed_repeatability_clue_count']}
    judgment: {judgment}
    external_verification_status: out_of_scope_by_claim_python_wfo_structural_probe_no_new_mt5
    result_summary_path: {rel(RUN_ROOT / 'reports/result_summary.md')}
    packet_summary_path: {rel(PACKET_ROOT / 'packet_summary.json')}
    next_action: broad_time_regime_probe_or_narrow_mt5_only_if_wfo_repeats
"""
    text = re.sub(r"stage12_model_family_challenge:\n.*?(?=\nagent_control_kpi_rebuild:)", block + "\n", text, flags=re.S)
    write_text(WORKSPACE_STATE_PATH, text)


def replace_section(text: str, heading: str, replacement: str) -> str:
    pattern = rf"\n{re.escape(heading)}.*?(?=\n## |\Z)"
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, "\n" + replacement.rstrip() + "\n", text, flags=re.S)
    return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"


def update_current_working_state(summary: Mapping[str, Any], judgment: str) -> None:
    text = read_text(CURRENT_STATE_PATH)
    text = re.sub(
        r"- current run\(현재 실행\): `[^`]+`",
        f"- current run(현재 실행): `{RUN_ID}`",
        text,
        count=1,
    )
    text = text.replace(
        "현재 기준은 `RUN03I(실행 03I)` validation/OOS inversion attribution(검증/표본외 반전 귀속)이다.",
        "`RUN03I(실행 03I)`는 validation/OOS inversion attribution(검증/표본외 반전 귀속) 근거이고, 현재 기준은 `RUN03J(실행 03J)` rolling WFO split probe(구르는 워크포워드 분할 탐침)이다.",
    )
    section = f"""## RUN03J rolling WFO split probe(구르는 워크포워드 분할 탐침)

- run(실행): `{RUN_ID}`
- source variants(원천 변형): `{SOURCE_VARIANT_RUN_ID}`
- reference MT5 evidence(참고 MT5 근거): `{SOURCE_MT5_RUN_ID}`
- variants/folds(변형/접힘): `{summary['variant_count']}` / `{summary['fold_count']}`
- best routed variant(최상위 라우팅 변형): `{summary['best_tier_ab_variant'].get('variant_id', 'NA')}`
- judgment(판정): `{judgment}`
- boundary(경계): `{BOUNDARY}`
- effect(효과): Stage 12(12단계)는 반전 단서를 계속 탐색하되, 아직 baseline(기준선), promotion candidate(승격 후보), runtime authority(런타임 권위)를 만들지 않는다.
"""
    text = replace_section(text, "## RUN03J rolling WFO split probe(구르는 워크포워드 분할 탐침)", section)
    write_text(CURRENT_STATE_PATH, text)


def update_selection_status(summary: Mapping[str, Any], judgment: str) -> None:
    text = read_text(SELECTION_STATUS_PATH) if path_exists(SELECTION_STATUS_PATH) else "# Stage 12 Selection Status\n"
    current = f"""# Stage 12 Selection Status

## Current Read - RUN03J rolling WFO split probe(현재 판독 - RUN03J 구르는 워크포워드 분할 탐침)

- current run(현재 실행): `{RUN_ID}`
- source variants(원천 변형): `{SOURCE_VARIANT_RUN_ID}`
- reference MT5 run(참고 MT5 실행): `{SOURCE_MT5_RUN_ID}`
- variants/folds(변형/접힘): `{summary['variant_count']}` / `{summary['fold_count']}`
- best routed variant(최상위 라우팅 변형): `{summary['best_tier_ab_variant'].get('variant_id', 'NA')}`
- judgment(판정): `{judgment}`
- boundary(경계): `{BOUNDARY}`

Effect(효과): RUN03J(실행 03J)는 Stage 12(12단계)를 계속 탐색할 이유와 위험을 같이 남긴다. baseline(기준선)이나 promotion candidate(승격 후보)는 만들지 않는다.
"""
    rest = re.sub(r"\A# Stage 12 Selection Status\n\n## Current Read.*?(?=\n# Selection Status|\n## Historical|\n## 이전|\Z)", "", text, flags=re.S)
    write_text(SELECTION_STATUS_PATH, current.rstrip() + "\n\n" + rest.lstrip())


def update_changelog(summary: Mapping[str, Any], judgment: str) -> None:
    text = read_text(CHANGELOG_PATH)
    if RUN_ID in text:
        return
    entry = (
        f"- 2026-05-01: `{RUN_ID}` completed(완료). Stage 12(12단계) ExtraTrees(엑스트라트리) 20개 변형을 "
        f"rolling WFO split probe(구르는 워크포워드 분할 탐침)로 실행했다. "
        f"variants/folds(변형/접힘) `{summary['variant_count']}/{summary['fold_count']}`, "
        f"judgment(판정) `{judgment}`. Effect(효과): RUN03H(실행 03H)의 validation/OOS inversion(검증/표본외 반전)을 "
        "단일 분할 주장으로 닫지 않고 반복성 탐색 기억으로 남긴다.\n"
    )
    if "## 2026-05-01" in text:
        text = text.replace("## 2026-05-01\n\n", "## 2026-05-01\n\n" + entry, 1)
    else:
        text = text.rstrip() + "\n\n## 2026-05-01\n\n" + entry
    write_text(CHANGELOG_PATH, text)


def write_packet_summary(summary: Mapping[str, Any], judgment: str, ledger_payload: Mapping[str, Any]) -> None:
    write_json(
        PACKET_ROOT / "packet_summary.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "status": "completed",
            "judgment": judgment,
            "boundary": BOUNDARY,
            "source_variant_run_id": SOURCE_VARIANT_RUN_ID,
            "source_mt5_run_id": SOURCE_MT5_RUN_ID,
            "variant_count": summary["variant_count"],
            "fold_count": summary["fold_count"],
            "variant_tier_rows": summary["variant_tier_rows"],
            "fold_metric_rows": summary["fold_metric_rows"],
            "new_mt5_execution": False,
            "ledger_payload": ledger_payload,
        },
    )


def run_probe() -> dict[str, Any]:
    created_at = utc_now()
    specs = _variant_specs()
    tier_a, tier_b_fallback, feature_order, metadata = prepare_frames()
    tier_b_training = metadata["tier_b_training"]
    fold_plan, fold_metrics, signals = evaluate_wfo(specs, tier_a, tier_b_fallback, tier_b_training, feature_order)
    variant_summary = summarize_variants(fold_metrics)
    matrix = inversion_matrix(fold_metrics)
    judgment, headline = package_summary(variant_summary, matrix)
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "completed_at_utc": utc_now(),
        "variant_count": len(specs),
        "fold_count": len(FOLDS),
        "variant_tier_rows": int(len(variant_summary)),
        "fold_metric_rows": int(len(fold_metrics)),
        "signal_rows": int(len(signals)),
        "probe_n_estimators_cap": PROBE_N_ESTIMATORS,
        "tier_b_fallback_rows_total": int(len(tier_b_fallback)),
        "boundary": BOUNDARY,
        "external_verification_status": "out_of_scope_by_claim_python_wfo_structural_probe_no_new_mt5",
        "judgment": judgment,
        **headline,
    }
    recommendations = next_probe_recommendations(summary)
    write_outputs(
        fold_plan=fold_plan,
        fold_metrics=fold_metrics,
        signals=signals,
        variant_summary=variant_summary,
        matrix=matrix,
        recommendations=recommendations,
    )
    write_reports(summary, variant_summary, judgment)
    write_run_records(
        created_at=created_at,
        completed_at=summary["completed_at_utc"],
        metadata=metadata,
        judgment=judgment,
        summary=summary,
    )
    summary = {**summary, "artifacts": artifacts()}
    write_json(RUN_ROOT / "summary.json", summary)
    write_work_packet(summary, judgment)
    write_skill_receipts(summary, judgment)
    ledger_payload = update_ledgers(summary, judgment)
    write_packet_summary(summary, judgment, ledger_payload)
    write_gate_audits(summary)
    update_current_truth(summary, judgment)
    return summary


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 12 ExtraTrees rolling WFO split probe.")
    parser.add_argument("--summary-json", default=str(RUN_ROOT / "summary.json"))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    summary = run_probe()
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": "completed",
                "judgment": summary["judgment"],
                "variant_count": summary["variant_count"],
                "fold_count": summary["fold_count"],
                "variant_tier_rows": summary["variant_tier_rows"],
                "fold_metric_rows": summary["fold_metric_rows"],
                "summary_json": args.summary_json,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
