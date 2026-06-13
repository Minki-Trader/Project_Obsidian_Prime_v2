from __future__ import annotations

import argparse
import json
import math
import pickle
import sys
import warnings
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready
from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout


STAGE_ID = "stage_frontier_02__four_axis_joint_onnx_proxy_scout"
RUN_ID = "frontier02D_review_and_repair_onnx_seed_surface_v1"
RUN_NUMBER = "frontier02D"
PARENT_RUN_ID = "frontier02C_trainable_onnx_seed_surface_design_v1"
NEXT_RUN_ID = "frontier02E_grok_pre_expensive_review_or_second_repair_v1"
EXPLORATION_LABEL = "stage_frontier_02__four_axis_joint_onnx_proxy_scout"
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
PARENT_RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / PARENT_RUN_ID
PARENT_MANIFEST_PATH = PARENT_RUN_ROOT / "run_manifest.json"
DATASET_PATH = scout.DATASET_PATH
FEATURE_ORDER_PATH = scout.FEATURE_ORDER_PATH
EXPECTED_FEATURE_HASH = scout.EXPECTED_FEATURE_HASH
MODEL_RANDOM_SEED = 29
MAX_ITER = 500
DECISION_THRESHOLDS = (0.34, 0.42, 0.50, 0.60)
DECISION_MARGINS = (0.00, 0.05, 0.10)
DECISION_COOLDOWNS = (6, 12)
SIDE_MODES = ("both", "long_only", "short_only")
FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
]


@dataclass(frozen=True)
class LabelSpec:
    label_id: str
    meaning: str
    return_margin: float | None


@dataclass(frozen=True)
class ModelSpec:
    model_family: str
    suffix: str
    c_value: float | None = None
    max_depth: int | None = None
    min_samples_leaf: int | None = None


LABEL_SPECS = (
    LabelSpec("native", "existing model_input label_class(기존 모델 입력 라벨 클래스)", None),
    LabelSpec("ret_m1c", "return sign action label after one rough-cost margin(1배 비용 마진 후 수익 방향 행동 라벨)", scout.ROUGH_COST_LOG_RETURN),
)
MODEL_SPECS = (
    ModelSpec("logistic_regression", "lr_c050", c_value=0.50),
)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = run_repair_scout(output_root=Path(args.output_root) if args.output_root else RUN_ROOT)
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2))
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Frontier02D ONNX seed surface repair scout.")
    parser.add_argument("--output-root", default=str(RUN_ROOT))
    return parser.parse_args(argv)


def run_repair_scout(*, output_root: Path) -> dict[str, Any]:
    io_path(output_root).mkdir(parents=True, exist_ok=True)
    model_root = output_root / "models"
    io_path(model_root).mkdir(parents=True, exist_ok=True)

    parent_manifest = read_json(PARENT_MANIFEST_PATH)
    frame = scout.load_and_validate_input()
    feature_order = scout.read_feature_order(FEATURE_ORDER_PATH)
    validate_features(frame, feature_order)
    filters = build_repair_filters(frame)
    input_audit = build_input_integrity_audit(frame, feature_order, parent_manifest)
    write_json(output_root / "input_integrity_audit.json", input_audit)

    model_records: list[dict[str, Any]] = []
    classifier_metric_rows: list[dict[str, Any]] = []
    export_records: list[dict[str, Any]] = []
    skipped_records: list[dict[str, Any]] = []
    decision_metric_frames: list[pd.DataFrame] = []

    for label_spec in LABEL_SPECS:
        labels = build_labels(frame, label_spec)
        sample_weight = build_sample_weight(frame, labels)
        if set(LABEL_ORDER).difference(set(labels.loc[frame["split"].astype(str).eq("train")].astype(int).tolist())):
            skipped_records.append(
                {
                    "label_id": label_spec.label_id,
                    "status": "skipped_missing_train_label_class",
                    "reason": "train split(학습 구간)에 3개 class(클래스)가 모두 없어 고정 3-class ONNX(고정 3클래스 온엑스)에 맞지 않습니다.",
                }
            )
            continue
        for model_spec in MODEL_SPECS:
            model_id = f"f02d_{label_spec.label_id}_{model_spec.suffix}"
            try:
                model = train_model(frame, feature_order, labels, sample_weight, model_spec)
                model_path = model_root / f"{model_id}.pkl"
                onnx_path = model_root / f"{model_id}.onnx"
                with io_path(model_path).open("wb") as handle:
                    pickle.dump(model, handle)
                export_record = export_sklearn_to_onnx_zipmap_disabled(
                    model,
                    onnx_path,
                    feature_count=len(feature_order),
                    input_name="float_input",
                    target_opset=12,
                    drop_label_output=True,
                )
                parity = check_onnxruntime_probability_parity(
                    model,
                    onnx_path,
                    parity_sample(frame, feature_order),
                    tolerance=1e-5,
                )
            except Exception as exc:
                skipped_records.append(
                    {
                        "candidate_model_id": model_id,
                        "label_id": label_spec.label_id,
                        "model_family": model_spec.model_family,
                        "status": "skipped_training_or_export_failure",
                        "reason": str(exc),
                    }
                )
                continue

            classifier_metrics = evaluate_classifier(model, frame, feature_order, labels)
            classifier_metrics["candidate_model_id"] = model_id
            classifier_metrics["label_id"] = label_spec.label_id
            classifier_metric_rows.extend(flatten_classifier_metrics(classifier_metrics))
            probabilities = ordered_sklearn_probabilities(
                model,
                frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False),
            )
            decision_metric_frames.append(evaluate_decision_grid(frame, probabilities, filters, model_id, label_spec))
            export_records.append(
                {
                    "candidate_model_id": model_id,
                    "label_id": label_spec.label_id,
                    "model_family": model_spec.model_family,
                    "model_path": model_path.as_posix(),
                    "model_sha256": sha256_file(model_path),
                    "onnx_export": export_record,
                    "onnx_parity": parity,
                }
            )
            model_records.append(
                {
                    "candidate_model_id": model_id,
                    "label_id": label_spec.label_id,
                    "label_meaning": label_spec.meaning,
                    "return_margin": label_spec.return_margin if label_spec.return_margin is not None else "",
                    "model_family": model_spec.model_family,
                    "model_suffix": model_spec.suffix,
                    "model_path": model_path.as_posix(),
                    "model_sha256": sha256_file(model_path),
                    "onnx_path": onnx_path.as_posix(),
                    "onnx_sha256": sha256_file(onnx_path),
                    "onnx_parity_passed": bool(parity["passed"]),
                    "onnx_max_abs_diff": float(parity["max_abs_diff"]),
                }
            )

    if not decision_metric_frames:
        raise RuntimeError("No repaired ONNX candidate models were produced.")

    model_table = pd.DataFrame(model_records)
    classifier_table = pd.DataFrame(classifier_metric_rows)
    decision_metrics = pd.concat(decision_metric_frames, ignore_index=True)
    decision_summary = build_decision_summary(decision_metrics, model_table)
    top = top_repaired_surfaces(decision_summary)
    top_replay = build_top_replay(frame, feature_order, filters, top.iloc[0].to_dict(), model_root)

    artifacts = write_artifacts(
        output_root=output_root,
        model_table=model_table,
        classifier_table=classifier_table,
        decision_metrics=decision_metrics,
        decision_summary=decision_summary,
        top=top,
        top_replay=top_replay,
        export_records=export_records,
        skipped_records=skipped_records,
        input_audit=input_audit,
    )
    report = write_report(
        model_table=model_table,
        classifier_table=classifier_table,
        decision_summary=decision_summary,
        top=top,
        artifacts=artifacts,
        skipped_records=skipped_records,
    )
    manifest = write_manifest(
        output_root=output_root,
        frame=frame,
        feature_order=feature_order,
        artifacts=artifacts,
        report=report,
        export_records=export_records,
        skipped_records=skipped_records,
        top=top,
    )
    return {
        "status": "completed_onnx_seed_repair_scout_no_authority",
        "run_id": RUN_ID,
        "output_root": output_root.as_posix(),
        "trained_models": int(len(model_table)),
        "decision_rows": int(len(decision_summary)),
        "top_decision": dict(top.iloc[0]),
        "manifest": manifest,
        "report": report,
    }


def validate_features(frame: pd.DataFrame, feature_order: list[str]) -> None:
    missing = sorted(set(feature_order).difference(frame.columns))
    if missing:
        raise ValueError(f"Missing feature columns: {missing}")
    values = frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
    if not np.isfinite(values).all():
        raise ValueError("Feature matrix contains non-finite values.")
    feature_hash = ordered_hash(feature_order)
    if feature_hash != EXPECTED_FEATURE_HASH:
        raise ValueError(f"Feature order hash mismatch: {feature_hash} != {EXPECTED_FEATURE_HASH}")


def build_repair_filters(frame: pd.DataFrame) -> dict[str, pd.Series]:
    base = scout.build_filters(frame)
    train = frame["split"].astype(str).eq("train")
    cash = pd.to_numeric(frame["is_us_cash_open"], errors="coerce").fillna(0).eq(1)
    vix = pd.to_numeric(frame["vix_zscore_20"], errors="coerce")
    breadth = pd.to_numeric(frame["mega8_pos_breadth_1"], errors="coerce")
    atr = pd.to_numeric(frame["atr_14_over_atr_50"], errors="coerce")
    vix_q75 = float(vix.loc[train].quantile(0.75))
    breadth_median = float(breadth.loc[train].median())
    atr_q90 = float(atr.loc[train].quantile(0.90))
    return {
        "all_cash": base["all_cash"],
        "mid_cash": base["mid_cash"],
        "cash_low_vix": cash & vix.le(vix_q75),
        "cash_breadth_ge_median": cash & breadth.ge(breadth_median),
    }


def build_labels(frame: pd.DataFrame, label_spec: LabelSpec) -> pd.Series:
    if label_spec.return_margin is None:
        return frame["label_class"].astype("int64").copy()
    returns = pd.to_numeric(frame["future_log_return_12"], errors="coerce").fillna(0.0)
    labels = pd.Series(np.ones(len(frame), dtype="int8"), index=frame.index)
    labels.loc[returns > float(label_spec.return_margin)] = 2
    labels.loc[returns < -float(label_spec.return_margin)] = 0
    return labels.astype("int64")


def build_sample_weight(frame: pd.DataFrame, labels: pd.Series) -> np.ndarray:
    train_mask = frame["split"].astype(str).eq("train")
    returns = pd.to_numeric(frame["future_log_return_12"], errors="coerce").abs().fillna(0.0)
    scale = float(returns.loc[train_mask].quantile(0.95))
    if not math.isfinite(scale) or scale <= 1e-12:
        scale = 1.0
    capped = np.minimum(returns.to_numpy(dtype="float64") / scale, 1.0)
    weights = 0.75 + (2.5 * capped)
    weights += (labels.to_numpy(dtype="int64") != 1).astype("float64") * 0.35
    return weights.astype("float64")


def train_model(
    frame: pd.DataFrame,
    feature_order: list[str],
    labels: pd.Series,
    sample_weight: np.ndarray,
    model_spec: ModelSpec,
) -> Pipeline:
    train_mask = frame["split"].astype(str).eq("train")
    X_train = frame.loc[train_mask, feature_order].to_numpy(dtype="float64", copy=False)
    y_train = labels.loc[train_mask].astype("int64").to_numpy()
    w_train = sample_weight[train_mask.to_numpy(dtype=bool)]
    if model_spec.model_family == "logistic_regression":
        model = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=MAX_ITER,
                        random_state=MODEL_RANDOM_SEED,
                        solver="lbfgs",
                        class_weight="balanced",
                        C=float(model_spec.c_value),
                    ),
                ),
            ]
        )
    elif model_spec.model_family == "extra_trees":
        model = Pipeline(
            steps=[
                (
                    "classifier",
                    ExtraTreesClassifier(
                        n_estimators=120,
                        max_depth=int(model_spec.max_depth or 6),
                        min_samples_leaf=int(model_spec.min_samples_leaf or 80),
                        random_state=MODEL_RANDOM_SEED,
                        class_weight="balanced",
                        n_jobs=-1,
                    ),
                )
            ]
        )
    else:
        raise ValueError(f"Unknown model family: {model_spec.model_family}")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        model.fit(X_train, y_train, classifier__sample_weight=w_train)
    return model


def parity_sample(frame: pd.DataFrame, feature_order: list[str], max_rows: int = 2048) -> np.ndarray:
    sample = frame.loc[:, feature_order]
    if len(sample) > max_rows:
        sample = sample.sample(n=max_rows, random_state=MODEL_RANDOM_SEED).sort_index()
    return sample.to_numpy(dtype="float64", copy=False)


def evaluate_classifier(model: Pipeline, frame: pd.DataFrame, feature_order: list[str], labels: pd.Series) -> dict[str, Any]:
    out: dict[str, Any] = {"splits": {}}
    for split in ("train", "validation", "oos"):
        split_mask = frame["split"].astype(str).eq(split)
        X = frame.loc[split_mask, feature_order].to_numpy(dtype="float64", copy=False)
        y_true = labels.loc[split_mask].astype("int64").to_numpy()
        probabilities = ordered_sklearn_probabilities(model, X)
        y_pred = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
        out["splits"][split] = {
            "rows": int(len(y_true)),
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
            "macro_f1": float(f1_score(y_true, y_pred, labels=LABEL_ORDER, average="macro")),
            "log_loss": float(log_loss(y_true, probabilities, labels=LABEL_ORDER)),
            "label_distribution": class_distribution(y_true),
            "predicted_distribution": class_distribution(y_pred),
            "mean_probability": {
                LABEL_NAMES[label]: float(probabilities[:, index].mean())
                for index, label in enumerate(LABEL_ORDER)
            },
        }
    return out


def class_distribution(values: np.ndarray) -> dict[str, int]:
    counts = pd.Series(values.astype("int64")).value_counts().to_dict()
    return {LABEL_NAMES[label]: int(counts.get(label, 0)) for label in LABEL_ORDER}


def flatten_classifier_metrics(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, values in metrics["splits"].items():
        rows.append(
            {
                "candidate_model_id": metrics["candidate_model_id"],
                "label_id": metrics["label_id"],
                "split": split,
                "rows": values["rows"],
                "accuracy": values["accuracy"],
                "balanced_accuracy": values["balanced_accuracy"],
                "macro_f1": values["macro_f1"],
                "log_loss": values["log_loss"],
                "label_short": values["label_distribution"]["short"],
                "label_flat": values["label_distribution"]["flat"],
                "label_long": values["label_distribution"]["long"],
                "pred_short": values["predicted_distribution"]["short"],
                "pred_flat": values["predicted_distribution"]["flat"],
                "pred_long": values["predicted_distribution"]["long"],
                "mean_p_short": values["mean_probability"]["short"],
                "mean_p_flat": values["mean_probability"]["flat"],
                "mean_p_long": values["mean_probability"]["long"],
            }
        )
    return rows


def evaluate_decision_grid(
    frame: pd.DataFrame,
    probabilities: np.ndarray,
    filters: dict[str, pd.Series],
    model_id: str,
    label_spec: LabelSpec,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for filter_name, filter_series in filters.items():
        filter_values = filter_series.fillna(False).to_numpy(dtype=bool)
        for side_mode in SIDE_MODES:
            for threshold in DECISION_THRESHOLDS:
                for margin in DECISION_MARGINS:
                    raw_signal = signal_from_probabilities(
                        probabilities,
                        threshold=float(threshold),
                        margin=float(margin),
                        filter_mask=filter_values,
                        side_mode=side_mode,
                    )
                    for cooldown in DECISION_COOLDOWNS:
                        signal = scout.apply_cooldown(raw_signal, int(cooldown))
                        candidate_id = (
                            f"{model_id}__{filter_name}__{side_mode}"
                            f"__p{int(round(float(threshold) * 100))}"
                            f"__m{int(round(float(margin) * 100))}__cd{int(cooldown)}"
                        )
                        for split in ("train", "validation", "oos"):
                            rows.append(
                                evaluate_model_split(
                                    frame=frame,
                                    signal=signal,
                                    split=split,
                                    candidate_id=candidate_id,
                                    model_id=model_id,
                                    label_id=label_spec.label_id,
                                    filter_name=filter_name,
                                    side_mode=side_mode,
                                    probability_threshold=float(threshold),
                                    probability_margin=float(margin),
                                    cooldown=int(cooldown),
                                )
                            )
    return pd.DataFrame(rows)


def signal_from_probabilities(
    probabilities: np.ndarray,
    *,
    threshold: float,
    margin: float,
    filter_mask: np.ndarray,
    side_mode: str,
) -> np.ndarray:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    signal = np.zeros(probabilities.shape[0], dtype="int8")
    long_edge = p_long - np.maximum(p_short, p_flat)
    short_edge = p_short - np.maximum(p_long, p_flat)
    if side_mode in {"both", "long_only"}:
        signal[(p_long >= threshold) & (long_edge >= margin) & filter_mask] = 1
    if side_mode in {"both", "short_only"}:
        signal[(p_short >= threshold) & (short_edge >= margin) & filter_mask] = -1
    return signal


def evaluate_model_split(
    *,
    frame: pd.DataFrame,
    signal: np.ndarray,
    split: str,
    candidate_id: str,
    model_id: str,
    label_id: str,
    filter_name: str,
    side_mode: str,
    probability_threshold: float,
    probability_margin: float,
    cooldown: int,
) -> dict[str, Any]:
    split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
    split_frame = frame.loc[split_mask, ["timestamp", "future_log_return_12"]].copy()
    split_signal = signal[split_mask].astype("int8")
    trade_mask = split_signal != 0
    days = scout.count_scope_days(split_frame["timestamp"])
    pnl = (
        split_signal.astype("float64")
        * pd.to_numeric(split_frame["future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
        - (trade_mask.astype("float64") * scout.ROUGH_COST_LOG_RETURN)
    )
    trade_pnl = pnl[trade_mask]
    trade_times = split_frame.loc[trade_mask, "timestamp"]
    metrics = scout.trade_metrics(trade_pnl, trade_times)
    trade_count = int(len(trade_pnl))
    trades_per_day = float(trade_count / days) if days else 0.0
    sparse_floor = max(30, int(math.ceil(days)))
    sparse_flag = trade_count < sparse_floor
    pf999_sparse_flag = bool(metrics["profit_factor"] >= 999.0 and sparse_flag)
    density_distance = scout.density_axis_distance(trades_per_day)
    pf_distance = scout.profit_factor_axis_distance(metrics["profit_factor"], trade_count, sparse_flag, pf999_sparse_flag)
    dd_risk = max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"]))
    dd_distance = max(0.0, (dd_risk - scout.DD_TARGET_PERCENT) / scout.DD_TARGET_PERCENT)
    smoothness_distance = scout.smoothness_axis_distance(metrics)
    aspiration_score = density_distance + pf_distance + dd_distance + smoothness_distance
    density_pass = scout.DENSITY_TARGET_LOW <= trades_per_day <= scout.DENSITY_TARGET_HIGH
    pf_pass = metrics["profit_factor"] >= scout.PF_TARGET and not sparse_flag and metrics["net_profit"] > 0
    dd_pass = dd_risk < scout.DD_TARGET_PERCENT
    smoothness_pass = (
        metrics["net_profit"] > 0
        and metrics["underwater_ratio"] <= 0.45
        and metrics["equity_trend_r2"] >= 0.35
        and metrics["max_loss_streak"] <= 6
    )
    return {
        "candidate_id": candidate_id,
        "candidate_model_id": model_id,
        "label_id": label_id,
        "filter_name": filter_name,
        "side_mode": side_mode,
        "probability_threshold": float(probability_threshold),
        "probability_margin": float(probability_margin),
        "cooldown_bars": int(cooldown),
        "hold_bars": scout.HOLD_BARS,
        "split": split,
        "tier_scope": "Tier A",
        "record_view": "Tier A separate",
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": trades_per_day,
        "sparse_floor": sparse_floor,
        "sparse_flag": bool(sparse_flag),
        "pf999_sparse_flag": pf999_sparse_flag,
        "long_trade_count": int((split_signal == 1).sum()),
        "short_trade_count": int((split_signal == -1).sum()),
        "net_profit": metrics["net_profit"],
        "profit_factor": metrics["profit_factor"],
        "expectancy": metrics["expectancy"],
        "win_rate": metrics["win_rate"],
        "max_drawdown_percent": metrics["max_drawdown_percent"],
        "max_monthly_drawdown_percent": metrics["max_monthly_drawdown_percent"],
        "underwater_ratio": metrics["underwater_ratio"],
        "max_loss_streak": metrics["max_loss_streak"],
        "equity_trend_r2": metrics["equity_trend_r2"],
        "density_axis_distance": density_distance,
        "pf_axis_distance": pf_distance,
        "dd_axis_distance": dd_distance,
        "smoothness_axis_distance": smoothness_distance,
        "aspiration_distance_score": aspiration_score,
        "density_pass": bool(density_pass),
        "pf_pass": bool(pf_pass),
        "dd_pass": bool(dd_pass),
        "smoothness_pass": bool(smoothness_pass),
        "joint_pass_count": int(density_pass) + int(pf_pass) + int(dd_pass) + int(smoothness_pass),
        "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
    }


def build_decision_summary(metrics: pd.DataFrame, model_table: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "candidate_id",
        "candidate_model_id",
        "label_id",
        "filter_name",
        "side_mode",
        "probability_threshold",
        "probability_margin",
        "cooldown_bars",
        "hold_bars",
    ]
    parity_lookup = model_table.set_index("candidate_model_id")["onnx_parity_passed"].to_dict()
    rows: list[dict[str, Any]] = []
    for key_values, group in metrics.groupby(keys, sort=False):
        base = dict(zip(keys, key_values))
        base["onnx_parity_passed"] = bool(parity_lookup.get(base["candidate_model_id"], False))
        for split in ("train", "validation", "oos"):
            row = group.loc[group["split"].eq(split)]
            if row.empty:
                continue
            item = row.iloc[0]
            for column in (
                "trade_count",
                "days_in_scope",
                "trades_per_day",
                "sparse_flag",
                "pf999_sparse_flag",
                "long_trade_count",
                "short_trade_count",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "max_drawdown_percent",
                "max_monthly_drawdown_percent",
                "underwater_ratio",
                "max_loss_streak",
                "equity_trend_r2",
                "aspiration_distance_score",
                "joint_pass_count",
                "density_pass",
                "pf_pass",
                "dd_pass",
                "smoothness_pass",
            ):
                base[f"{split}_{column}"] = item[column]
        base["non_sparse_validation_oos"] = bool(
            not base.get("validation_sparse_flag", True) and not base.get("oos_sparse_flag", True)
        )
        base["positive_validation_oos"] = bool(base.get("validation_net_profit", 0) > 0 and base.get("oos_net_profit", 0) > 0)
        base["repair_observation_flag"] = bool(
            base["onnx_parity_passed"]
            and base["non_sparse_validation_oos"]
            and base["positive_validation_oos"]
            and float(base.get("validation_aspiration_distance_score", 99.0)) < 3.0
            and float(base.get("oos_aspiration_distance_score", 99.0)) < 3.5
        )
        rows.append(base)
    summary = pd.DataFrame(rows)
    summary["validation_rank"] = summary["validation_aspiration_distance_score"].rank(method="first")
    return summary


def top_repaired_surfaces(summary: pd.DataFrame) -> pd.DataFrame:
    return (
        summary.sort_values(
            ["validation_aspiration_distance_score", "validation_joint_pass_count", "oos_aspiration_distance_score"],
            ascending=[True, False, True],
        )
        .head(30)
        .reset_index(drop=True)
    )


def build_top_replay(
    frame: pd.DataFrame,
    feature_order: list[str],
    filters: dict[str, pd.Series],
    top: dict[str, Any],
    model_root: Path,
) -> pd.DataFrame:
    with io_path(model_root / f"{top['candidate_model_id']}.pkl").open("rb") as handle:
        model = pickle.load(handle)
    probabilities = ordered_sklearn_probabilities(
        model,
        frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False),
    )
    raw_signal = signal_from_probabilities(
        probabilities,
        threshold=float(top["probability_threshold"]),
        margin=float(top["probability_margin"]),
        filter_mask=filters[str(top["filter_name"])].fillna(False).to_numpy(dtype=bool),
        side_mode=str(top["side_mode"]),
    )
    signal = scout.apply_cooldown(raw_signal, int(top["cooldown_bars"]))
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(frame["timestamp"], utc=True).astype(str),
            "split": frame["split"].astype(str),
            "candidate_id": top["candidate_id"],
            "candidate_model_id": top["candidate_model_id"],
            "signal": signal,
            "p_short": probabilities[:, 0],
            "p_flat": probabilities[:, 1],
            "p_long": probabilities[:, 2],
            "future_log_return_12": pd.to_numeric(frame["future_log_return_12"], errors="coerce"),
        }
    )


def write_artifacts(
    *,
    output_root: Path,
    model_table: pd.DataFrame,
    classifier_table: pd.DataFrame,
    decision_metrics: pd.DataFrame,
    decision_summary: pd.DataFrame,
    top: pd.DataFrame,
    top_replay: pd.DataFrame,
    export_records: list[dict[str, Any]],
    skipped_records: list[dict[str, Any]],
    input_audit: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    paths = {
        "repair_model_training_summary": output_root / "repair_model_training_summary.csv",
        "repair_classifier_metrics": output_root / "repair_classifier_metrics.csv",
        "repair_decision_surface_metrics": output_root / "repair_decision_surface_metrics.csv",
        "repair_decision_surface_summary": output_root / "repair_decision_surface_summary.csv",
        "top_repaired_onnx_seed_surfaces": output_root / "top_repaired_onnx_seed_surfaces.csv",
        "top_repair_signal_replay": output_root / "top_repair_signal_replay.csv",
    }
    model_table.to_csv(io_path(paths["repair_model_training_summary"]), index=False, lineterminator="\n")
    classifier_table.to_csv(io_path(paths["repair_classifier_metrics"]), index=False, lineterminator="\n")
    decision_metrics.to_csv(io_path(paths["repair_decision_surface_metrics"]), index=False, lineterminator="\n")
    decision_summary.to_csv(io_path(paths["repair_decision_surface_summary"]), index=False, lineterminator="\n")
    top.to_csv(io_path(paths["top_repaired_onnx_seed_surfaces"]), index=False, lineterminator="\n")
    top_replay.to_csv(io_path(paths["top_repair_signal_replay"]), index=False, lineterminator="\n")

    write_json(output_root / "repair_model_export_records.json", {"exports": export_records, "skipped": skipped_records})
    write_json(output_root / "repair_onnx_parity_audit.json", {"records": [record["onnx_parity"] for record in export_records]})
    write_json(output_root / "repair_seed_surface_spec.json", build_repair_spec(top.iloc[0].to_dict(), model_table))
    write_json(output_root / "input_integrity_audit.json", input_audit)

    artifacts: dict[str, dict[str, Any]] = {}
    for role, path in paths.items():
        artifacts[role] = {"path": path.as_posix(), "sha256": sha256_file(path)}
    for role in ("repair_model_export_records", "repair_onnx_parity_audit", "repair_seed_surface_spec", "input_integrity_audit"):
        path = output_root / f"{role}.json"
        artifacts[role] = {"path": path.as_posix(), "sha256": sha256_file(path)}
    for record in export_records:
        artifacts[f"onnx_model__{record['candidate_model_id']}"] = {
            "path": record["onnx_export"]["path"],
            "sha256": record["onnx_export"]["sha256"],
        }
    return artifacts


def build_repair_spec(top: dict[str, Any], model_table: pd.DataFrame) -> dict[str, Any]:
    model_row = model_table.loc[model_table["candidate_model_id"].eq(top["candidate_model_id"])].iloc[0].to_dict()
    return {
        "run_id": RUN_ID,
        "status": "onnx_repair_seed_observation_no_authority",
        "candidate_id": str(top["candidate_id"]),
        "candidate_model_id": str(top["candidate_model_id"]),
        "label_id": str(top["label_id"]),
        "onnx_path": model_row["onnx_path"],
        "onnx_sha256": model_row["onnx_sha256"],
        "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        "feature_order_hash": EXPECTED_FEATURE_HASH,
        "input_name": "float_input",
        "probability_order": ["short", "flat", "long"],
        "runtime_filter_name": str(top["filter_name"]),
        "side_mode": str(top["side_mode"]),
        "probability_threshold": float(top["probability_threshold"]),
        "probability_margin": float(top["probability_margin"]),
        "cooldown_bars": int(top["cooldown_bars"]),
        "hold_bars": scout.HOLD_BARS,
        "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
        "selector_scope": "validation_only",
        "oos_use": "diagnostic_only",
        "claim_boundary": "onnx_repair_seed_observation_only_no_runtime_authority",
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def write_report(
    *,
    model_table: pd.DataFrame,
    classifier_table: pd.DataFrame,
    decision_summary: pd.DataFrame,
    top: pd.DataFrame,
    artifacts: dict[str, dict[str, Any]],
    skipped_records: list[dict[str, Any]],
) -> dict[str, Any]:
    io_path(REPORT_PATH.parent).mkdir(parents=True, exist_ok=True)
    best = top.iloc[0].to_dict()
    observation_rows = int(decision_summary["repair_observation_flag"].sum())
    parity_passes = int(model_table["onnx_parity_passed"].sum())
    lines = [
        "# frontier02D ONNX Seed Repair Report(전선02D 온엑스 씨앗 수리 보고)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        "- status(상태): `completed_onnx_seed_repair_scout_no_authority(온엑스 씨앗 수리 탐색 완료, 권위 없음)`",
        f"- trained_models(학습 모델 수): `{len(model_table)}`",
        f"- ONNX parity pass(온엑스 동등성 통과): `{parity_passes}/{len(model_table)}`",
        f"- decision_rows(결정 표면 행): `{len(decision_summary)}`",
        f"- repair_observation_rows(수리 관찰 행): `{observation_rows}`",
        "",
        "## Boundary(경계)",
        "",
        "이번 실행(run, 실행)은 cheap ONNX repair scout(저비용 온엑스 수리 탐색)입니다. WFO(워크포워드), MT5 runtime validation(MT5 런타임 검증), baseline selection(기준선 선택), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않습니다.",
        "",
        "## Best Validation Rank(검증 순위 1위)",
        "",
        f"- candidate_id(후보 ID): `{best.get('candidate_id')}`",
        f"- candidate_model_id(후보 모델 ID): `{best.get('candidate_model_id')}`",
        f"- label_id(라벨 ID): `{best.get('label_id')}`",
        f"- filter/side(필터/방향): `{best.get('filter_name')}` / `{best.get('side_mode')}`",
        f"- threshold/margin/cooldown(임계값/마진/쿨다운): `{format_float(best.get('probability_threshold'))}` / `{format_float(best.get('probability_margin'))}` / `{best.get('cooldown_bars')}`",
        f"- validation net/PF/density/DD(검증 순수익/수익 팩터/밀도/손실폭): `{format_float(best.get('validation_net_profit'))}` / `{format_float(best.get('validation_profit_factor'))}` / `{format_float(best.get('validation_trades_per_day'))}` / `{format_float(best.get('validation_max_drawdown_percent'))}%`",
        f"- OOS net/PF/density/DD(표본외 순수익/수익 팩터/밀도/손실폭): `{format_float(best.get('oos_net_profit'))}` / `{format_float(best.get('oos_profit_factor'))}` / `{format_float(best.get('oos_trades_per_day'))}` / `{format_float(best.get('oos_max_drawdown_percent'))}%`",
        f"- joint_pass_count(동시 통과 수): validation(검증) `{best.get('validation_joint_pass_count')}`, OOS(표본외) `{best.get('oos_joint_pass_count')}`",
        "",
        "## Read(판독)",
        "",
        read_text(best, observation_rows),
        "",
        "## Skipped Models(건너뛴 모델)",
        "",
    ]
    if skipped_records:
        for record in skipped_records:
            lines.append(f"- `{record.get('candidate_model_id', record.get('label_id', 'unknown'))}`: `{record['status']}`")
    else:
        lines.append("- none(없음)")
    lines.extend(["", "## Artifacts(산출물)", ""])
    for role, record in artifacts.items():
        lines.append(f"- {role}: `{record['path']}` sha256(해시) `{record['sha256']}`")
    lines.extend(
        [
            "",
            "## Gate Boundary(게이트 경계)",
            "",
            "- Tier A separate(Tier A 분리): materialized(물질화)",
            "- Tier B separate(Tier B 분리): partial-context Tier B artifact(부분 문맥 Tier B 산출물)를 만들지 않았으므로 `missing_required(필수 누락)`입니다.",
            "- Tier A+B combined(Tier A+B 합산): routed Tier B fallback(라우팅 Tier B 대체)을 실행하지 않았으므로 `out_of_scope_by_claim(주장 범위 밖)`입니다.",
            "- Grok pre-expensive review(비싼 검증 전 그록 검토): 이번 cheap repair scout(저비용 수리 탐색)에는 새 호출을 하지 않았고, WFO/MT5(워크포워드/MT5) 전에는 required(필요)입니다.",
        ]
    )
    io_path(REPORT_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    return {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)}


def read_text(best: dict[str, Any], observation_rows: int) -> str:
    if observation_rows > 0:
        return "Repair observation(수리 관찰)은 있습니다. 다만 PF(수익 팩터) 목표와 smoothness(매끄러움)가 여전히 약하면 다음 행동(action, 행동)은 수리 표면을 더 좁히거나 WFO/MT5(워크포워드/MT5) 전 Grok review(그록 검토)로 넘어갈지 판정하는 것입니다."
    return "ONNX repair scout(온엑스 수리 탐색)는 완료됐지만 새 수리 관찰은 약합니다. 다음 행동(action, 행동)은 label/objective(라벨/목적)를 바꾸거나 frontier hypothesis(전선 가설)를 닫을 조건을 검토하는 것입니다."


def write_manifest(
    *,
    output_root: Path,
    frame: pd.DataFrame,
    feature_order: list[str],
    artifacts: dict[str, dict[str, Any]],
    report: dict[str, Any],
    export_records: list[dict[str, Any]],
    skipped_records: list[dict[str, Any]],
    top: pd.DataFrame,
) -> dict[str, Any]:
    manifest_path = output_root / "run_manifest.json"
    best = top.iloc[0].to_dict()
    manifest = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "exploration_label": EXPLORATION_LABEL,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": "completed_onnx_seed_repair_scout_no_authority",
        "created_at_utc": utc_now(),
        "script_path": "stage_pipelines/stage_frontier_02/repair_onnx_seed_surface.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_02/repair_onnx_seed_surface.py")),
        "inputs": {
            "model_input_dataset_path": DATASET_PATH.as_posix(),
            "model_input_dataset_sha256": sha256_file(DATASET_PATH),
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
            "feature_order_hash": ordered_hash(feature_order),
            "parent_manifest_path": PARENT_MANIFEST_PATH.as_posix(),
            "rows": int(len(frame)),
            "split_counts": {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()},
        },
        "model_contract": {
            "model_families": sorted({record["model_family"] for record in export_records}),
            "label_specs": [spec.__dict__ for spec in LABEL_SPECS],
            "class_order": LABEL_ORDER,
            "label_names": LABEL_NAMES,
            "feature_count": len(feature_order),
            "selector_scope": "validation_only",
            "oos_use": "diagnostic_only",
        },
        "decision_contract": {
            "density_target_trades_per_day": [scout.DENSITY_TARGET_LOW, scout.DENSITY_TARGET_HIGH],
            "profit_factor_target_low": scout.PF_TARGET,
            "drawdown_target_percent": scout.DD_TARGET_PERCENT,
            "rough_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
            "hold_bars": scout.HOLD_BARS,
            "probability_thresholds": list(DECISION_THRESHOLDS),
            "probability_margins": list(DECISION_MARGINS),
            "cooldown_bars": list(DECISION_COOLDOWNS),
            "side_modes": list(SIDE_MODES),
            "selection_boundary": "validation_rank_only_oos_diagnostic_no_completion_claim",
        },
        "outputs": artifacts,
        "exports": export_records,
        "skipped_models": skipped_records,
        "best_validation_rank": json_ready(best),
        "report": report,
        "external_verification_status": "out_of_scope_by_claim_no_mt5",
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    write_json(manifest_path, manifest)
    return {"path": manifest_path.as_posix(), "sha256": sha256_file(manifest_path)}


def build_input_integrity_audit(
    frame: pd.DataFrame,
    feature_order: list[str],
    parent_manifest: dict[str, Any],
) -> dict[str, Any]:
    return {
        "status": "pass",
        "dataset_path": DATASET_PATH.as_posix(),
        "dataset_sha256": sha256_file(DATASET_PATH),
        "parent_dataset_sha256": parent_manifest["inputs"]["model_input_dataset_sha256"],
        "dataset_hash_matches_parent": sha256_file(DATASET_PATH) == parent_manifest["inputs"]["model_input_dataset_sha256"],
        "rows": int(len(frame)),
        "split_counts": {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()},
        "first_timestamp": pd.to_datetime(frame["timestamp"].min()).isoformat(),
        "last_timestamp": pd.to_datetime(frame["timestamp"].max()).isoformat(),
        "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        "feature_order_hash": ordered_hash(feature_order),
        "feature_count": len(feature_order),
        "label_boundary": "labels built from existing label_class or future_log_return_12 target only; features remain closed-bar inputs",
        "split_boundary": "train fit, validation rank, OOS diagnostic only",
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def format_float(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
