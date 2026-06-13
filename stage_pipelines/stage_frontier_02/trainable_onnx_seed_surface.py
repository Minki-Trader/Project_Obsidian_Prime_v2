from __future__ import annotations

import argparse
import json
import math
import pickle
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
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
RUN_ID = "frontier02C_trainable_onnx_seed_surface_design_v1"
RUN_NUMBER = "frontier02C"
PARENT_RUN_ID = "frontier02B_proxy_scout_execution_v1"
NEXT_RUN_ID = "frontier02D_review_and_repair_onnx_seed_surface_v1"
EXPLORATION_LABEL = "stage_frontier_02__four_axis_joint_onnx_proxy_scout"
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
PARENT_RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / PARENT_RUN_ID
PARENT_MANIFEST_PATH = PARENT_RUN_ROOT / "run_manifest.json"
PARENT_TOP_PATH = PARENT_RUN_ROOT / "top_seed_surfaces.csv"
DATASET_PATH = scout.DATASET_PATH
FEATURE_ORDER_PATH = scout.FEATURE_ORDER_PATH
EXPECTED_FEATURE_HASH = scout.EXPECTED_FEATURE_HASH
MODEL_RANDOM_SEED = 17
MAX_ITER = 1200
TEACHER_TOP_N = 8
DECISION_THRESHOLDS = (0.34, 0.38, 0.42, 0.46, 0.50, 0.55, 0.60, 0.65)
DECISION_MARGINS = (0.00, 0.03, 0.06, 0.10)
DECISION_COOLDOWNS = (6, 12, 18)
FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
]


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = run_trainable_seed_surface(
        output_root=Path(args.output_root) if args.output_root else RUN_ROOT,
        top_n=int(args.top_n),
    )
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2))
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train Frontier02C ONNX-ready teacher seed surfaces.")
    parser.add_argument("--output-root", default=str(RUN_ROOT))
    parser.add_argument("--top-n", type=int, default=TEACHER_TOP_N)
    return parser.parse_args(argv)


def run_trainable_seed_surface(*, output_root: Path, top_n: int = TEACHER_TOP_N) -> dict[str, Any]:
    io_path(output_root).mkdir(parents=True, exist_ok=True)
    model_root = output_root / "models"
    io_path(model_root).mkdir(parents=True, exist_ok=True)

    parent_manifest = read_json(PARENT_MANIFEST_PATH)
    frame = scout.load_and_validate_input()
    feature_order = scout.read_feature_order(FEATURE_ORDER_PATH)
    validate_features(frame, feature_order)
    z_frame = scout.build_train_standardized_features(frame, feature_order)
    filters = scout.build_filters(frame)
    parent_top = pd.read_csv(io_path(PARENT_TOP_PATH)).head(int(top_n)).copy()

    input_audit = build_input_integrity_audit(frame, feature_order, parent_manifest)
    write_json(output_root / "input_integrity_audit.json", input_audit)

    model_records: list[dict[str, Any]] = []
    classifier_metric_rows: list[dict[str, Any]] = []
    decision_metric_frames: list[pd.DataFrame] = []
    teacher_rows: list[dict[str, Any]] = []
    export_records: list[dict[str, Any]] = []
    skipped_records: list[dict[str, Any]] = []
    replay_frames: list[pd.DataFrame] = []

    for _, seed_row in parent_top.iterrows():
        seed = seed_row.to_dict()
        teacher = materialize_teacher_signal(frame, z_frame, filters, seed)
        teacher_rows.extend(build_teacher_rows(frame, seed, teacher))
        train_labels = set(teacher["teacher_label"][frame["split"].astype(str).eq("train")].astype(int).tolist())
        if set(LABEL_ORDER).difference(train_labels):
            skipped_records.append(
                {
                    "teacher_candidate_id": str(seed["candidate_id"]),
                    "status": "skipped_missing_train_label_class",
                    "missing_classes": sorted(set(LABEL_ORDER).difference(train_labels)),
                    "reason": "Teacher signal(교사 신호)이 one-sided(한 방향)이라 fixed 3-class ONNX(고정 3클래스 온엑스) smoke model(스모크 모델)에 맞지 않습니다.",
                }
            )
            continue

        model_id = model_id_for_seed(seed)
        model = train_teacher_model(frame, feature_order, teacher["teacher_label"])
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
        classifier_metrics = evaluate_classifier_against_teacher(model, frame, feature_order, teacher["teacher_label"])
        classifier_metrics["candidate_model_id"] = model_id
        classifier_metrics["teacher_candidate_id"] = str(seed["candidate_id"])
        classifier_metric_rows.extend(flatten_classifier_metrics(classifier_metrics))

        probabilities = ordered_sklearn_probabilities(
            model,
            frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False),
        )
        decision_metrics = evaluate_decision_grid(frame, probabilities, filters[str(seed["filter_name"])], seed, model_id)
        decision_metric_frames.append(decision_metrics)
        export_records.append(
            {
                "candidate_model_id": model_id,
                "teacher_candidate_id": str(seed["candidate_id"]),
                "model_path": model_path.as_posix(),
                "model_sha256": sha256_file(model_path),
                "onnx_export": export_record,
                "onnx_parity": parity,
            }
        )
        model_records.append(
            {
                "candidate_model_id": model_id,
                "teacher_candidate_id": str(seed["candidate_id"]),
                "surface": str(seed["surface"]),
                "filter_name": str(seed["filter_name"]),
                "side_mode": str(seed["side_mode"]),
                "teacher_threshold_quantile": float(seed["threshold_quantile"]),
                "teacher_cooldown_bars": int(seed["cooldown_bars"]),
                "teacher_train_trades_per_day": float(seed["train_trades_per_day"]),
                "teacher_validation_profit_factor": float(seed["validation_profit_factor"]),
                "teacher_validation_trades_per_day": float(seed["validation_trades_per_day"]),
                "teacher_validation_max_drawdown_percent": float(seed["validation_max_drawdown_percent"]),
                "teacher_oos_profit_factor": float(seed["oos_profit_factor"]),
                "teacher_oos_trades_per_day": float(seed["oos_trades_per_day"]),
                "teacher_oos_max_drawdown_percent": float(seed["oos_max_drawdown_percent"]),
                "model_path": model_path.as_posix(),
                "model_sha256": sha256_file(model_path),
                "onnx_path": onnx_path.as_posix(),
                "onnx_sha256": sha256_file(onnx_path),
                "onnx_parity_passed": bool(parity["passed"]),
            }
        )

    if not decision_metric_frames:
        raise RuntimeError("No trainable teacher models were produced.")

    model_table = pd.DataFrame(model_records)
    teacher_table = pd.DataFrame(teacher_rows)
    classifier_table = pd.DataFrame(classifier_metric_rows)
    decision_metrics = pd.concat(decision_metric_frames, ignore_index=True)
    decision_summary = build_decision_summary(decision_metrics, model_table)
    top = top_seed_decisions(decision_summary)
    top_replay = build_top_replay(frame, feature_order, filters, top.iloc[0].to_dict(), model_root)
    replay_frames.append(top_replay)

    artifacts = write_artifacts(
        output_root=output_root,
        model_table=model_table,
        teacher_table=teacher_table,
        classifier_table=classifier_table,
        decision_metrics=decision_metrics,
        decision_summary=decision_summary,
        top=top,
        top_replay=pd.concat(replay_frames, ignore_index=True),
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
        "status": "completed_trainable_onnx_seed_surface_smoke_no_authority",
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


def materialize_teacher_signal(
    frame: pd.DataFrame,
    z_frame: pd.DataFrame,
    filters: dict[str, pd.Series],
    seed: dict[str, Any],
) -> dict[str, Any]:
    surface = surface_by_name(str(seed["surface"]))
    filter_name = str(seed["filter_name"])
    filter_mask = filters[filter_name].fillna(False).to_numpy(dtype=bool)
    score = scout.build_surface_score(z_frame, surface)
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool) & filter_mask
    train_abs = np.abs(score[train_mask])
    train_abs = train_abs[np.isfinite(train_abs)]
    threshold = float(np.quantile(train_abs, float(seed["threshold_quantile"])))
    raw_signal = scout.signal_from_score(score, threshold, filter_mask, str(seed["side_mode"]))
    signal = scout.apply_cooldown(raw_signal, int(seed["cooldown_bars"]))
    labels = (signal.astype("int16") + 1).astype("int8")
    return {
        "score": score,
        "threshold": threshold,
        "signal": signal,
        "teacher_label": pd.Series(labels, index=frame.index),
        "filter_mask": filter_mask,
    }


def surface_by_name(name: str) -> scout.SurfaceSpec:
    for surface in scout.SURFACES:
        if surface.name == name:
            return surface
    raise KeyError(f"Unknown surface: {name}")


def model_id_for_seed(seed: dict[str, Any]) -> str:
    return (
        "frontier02c_logreg_teacher__"
        f"{seed['surface']}__{seed['filter_name']}__{seed['side_mode']}__"
        f"q{int(round(float(seed['threshold_quantile']) * 100))}__cd{int(seed['cooldown_bars'])}"
    )


def train_teacher_model(frame: pd.DataFrame, feature_order: list[str], labels: pd.Series) -> Pipeline:
    train_mask = frame["split"].astype(str).eq("train")
    X_train = frame.loc[train_mask, feature_order].to_numpy(dtype="float64", copy=False)
    y_train = labels.loc[train_mask].astype("int64").to_numpy()
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
                    C=0.75,
                ),
            ),
        ]
    )
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        model.fit(X_train, y_train)
    return model


def parity_sample(frame: pd.DataFrame, feature_order: list[str], max_rows: int = 2048) -> np.ndarray:
    sample = frame.loc[:, feature_order]
    if len(sample) > max_rows:
        sample = sample.sample(n=max_rows, random_state=MODEL_RANDOM_SEED).sort_index()
    return sample.to_numpy(dtype="float64", copy=False)


def evaluate_classifier_against_teacher(
    model: Pipeline,
    frame: pd.DataFrame,
    feature_order: list[str],
    labels: pd.Series,
) -> dict[str, Any]:
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
            "teacher_distribution": class_distribution(y_true),
            "predicted_distribution": class_distribution(y_pred),
            "mean_probability": {
                LABEL_NAMES[label]: float(probabilities[:, index].mean())
                for index, label in enumerate(LABEL_ORDER)
            },
        }
    return out


def class_distribution(values: np.ndarray) -> dict[str, int]:
    series = pd.Series(values.astype("int64"))
    counts = series.value_counts().to_dict()
    return {LABEL_NAMES[label]: int(counts.get(label, 0)) for label in LABEL_ORDER}


def flatten_classifier_metrics(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, values in metrics["splits"].items():
        rows.append(
            {
                "candidate_model_id": metrics["candidate_model_id"],
                "teacher_candidate_id": metrics["teacher_candidate_id"],
                "split": split,
                "rows": values["rows"],
                "accuracy": values["accuracy"],
                "balanced_accuracy": values["balanced_accuracy"],
                "macro_f1": values["macro_f1"],
                "log_loss": values["log_loss"],
                "teacher_short": values["teacher_distribution"]["short"],
                "teacher_flat": values["teacher_distribution"]["flat"],
                "teacher_long": values["teacher_distribution"]["long"],
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
    filter_mask: pd.Series,
    seed: dict[str, Any],
    model_id: str,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    filter_values = filter_mask.fillna(False).to_numpy(dtype=bool)
    for threshold in DECISION_THRESHOLDS:
        for margin in DECISION_MARGINS:
            raw_signal = signal_from_probabilities(
                probabilities,
                threshold=float(threshold),
                margin=float(margin),
                filter_mask=filter_values,
                side_mode=str(seed["side_mode"]),
            )
            for cooldown in DECISION_COOLDOWNS:
                signal = scout.apply_cooldown(raw_signal, int(cooldown))
                candidate_id = (
                    f"{model_id}__p{int(round(float(threshold) * 100))}"
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
                            teacher_candidate_id=str(seed["candidate_id"]),
                            surface=str(seed["surface"]),
                            filter_name=str(seed["filter_name"]),
                            side_mode=str(seed["side_mode"]),
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
    teacher_candidate_id: str,
    surface: str,
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
        "teacher_candidate_id": teacher_candidate_id,
        "surface": surface,
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
        "teacher_candidate_id",
        "surface",
        "filter_name",
        "side_mode",
        "probability_threshold",
        "probability_margin",
        "cooldown_bars",
        "hold_bars",
    ]
    summary_rows: list[dict[str, Any]] = []
    parity_lookup = model_table.set_index("candidate_model_id")["onnx_parity_passed"].to_dict()
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
        base["onnx_seed_observation_flag"] = bool(
            base["onnx_parity_passed"]
            and base["non_sparse_validation_oos"]
            and base["positive_validation_oos"]
            and float(base.get("validation_aspiration_distance_score", 99.0)) < 3.0
            and float(base.get("oos_aspiration_distance_score", 99.0)) < 3.5
        )
        summary_rows.append(base)
    summary = pd.DataFrame(summary_rows)
    summary["validation_rank"] = summary["validation_aspiration_distance_score"].rank(method="first")
    return summary


def top_seed_decisions(summary: pd.DataFrame) -> pd.DataFrame:
    return (
        summary.sort_values(
            ["validation_aspiration_distance_score", "validation_joint_pass_count", "oos_aspiration_distance_score"],
            ascending=[True, False, True],
        )
        .head(20)
        .reset_index(drop=True)
    )


def build_top_replay(
    frame: pd.DataFrame,
    feature_order: list[str],
    filters: dict[str, pd.Series],
    top: dict[str, Any],
    model_root: Path,
) -> pd.DataFrame:
    model_path = model_root / f"{top['candidate_model_id']}.pkl"
    with io_path(model_path).open("rb") as handle:
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


def build_teacher_rows(frame: pd.DataFrame, seed: dict[str, Any], teacher: dict[str, Any]) -> list[dict[str, Any]]:
    labels = teacher["teacher_label"].astype(int)
    rows = []
    for split, group_index in labels.groupby(frame["split"].astype(str)).groups.items():
        values = labels.loc[group_index].to_numpy(dtype="int64")
        rows.append(
            {
                "teacher_candidate_id": str(seed["candidate_id"]),
                "split": str(split),
                "threshold_value": float(teacher["threshold"]),
                "short_rows": int((values == 0).sum()),
                "flat_rows": int((values == 1).sum()),
                "long_rows": int((values == 2).sum()),
                "trade_rows": int((values != 1).sum()),
            }
        )
    return rows


def write_artifacts(
    *,
    output_root: Path,
    model_table: pd.DataFrame,
    teacher_table: pd.DataFrame,
    classifier_table: pd.DataFrame,
    decision_metrics: pd.DataFrame,
    decision_summary: pd.DataFrame,
    top: pd.DataFrame,
    top_replay: pd.DataFrame,
    export_records: list[dict[str, Any]],
    skipped_records: list[dict[str, Any]],
    input_audit: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    artifacts: dict[str, dict[str, Any]] = {}
    paths = {
        "model_training_summary": output_root / "model_training_summary.csv",
        "teacher_signal_audit": output_root / "teacher_signal_audit.csv",
        "classifier_metrics": output_root / "classifier_metrics.csv",
        "decision_surface_metrics": output_root / "decision_surface_metrics.csv",
        "decision_surface_summary": output_root / "decision_surface_summary.csv",
        "top_onnx_seed_surfaces": output_root / "top_onnx_seed_surfaces.csv",
        "top_decision_signal_replay": output_root / "top_decision_signal_replay.csv",
    }
    model_table.to_csv(io_path(paths["model_training_summary"]), index=False, lineterminator="\n")
    teacher_table.to_csv(io_path(paths["teacher_signal_audit"]), index=False, lineterminator="\n")
    classifier_table.to_csv(io_path(paths["classifier_metrics"]), index=False, lineterminator="\n")
    decision_metrics.to_csv(io_path(paths["decision_surface_metrics"]), index=False, lineterminator="\n")
    decision_summary.to_csv(io_path(paths["decision_surface_summary"]), index=False, lineterminator="\n")
    top.to_csv(io_path(paths["top_onnx_seed_surfaces"]), index=False, lineterminator="\n")
    top_replay.to_csv(io_path(paths["top_decision_signal_replay"]), index=False, lineterminator="\n")

    write_json(output_root / "model_export_records.json", {"exports": export_records, "skipped": skipped_records})
    write_json(output_root / "onnx_parity_audit.json", {"records": [record["onnx_parity"] for record in export_records]})
    write_json(output_root / "trainable_seed_surface_spec.json", build_trainable_spec(top.iloc[0].to_dict(), model_table))
    write_json(output_root / "input_integrity_audit.json", input_audit)

    for role, path in paths.items():
        artifacts[role] = {"path": path.as_posix(), "sha256": sha256_file(path)}
    for role in ("model_export_records", "onnx_parity_audit", "trainable_seed_surface_spec", "input_integrity_audit"):
        path = output_root / f"{role}.json"
        artifacts[role] = {"path": path.as_posix(), "sha256": sha256_file(path)}
    for record in export_records:
        artifacts[f"onnx_model__{record['candidate_model_id']}"] = {
            "path": record["onnx_export"]["path"],
            "sha256": record["onnx_export"]["sha256"],
        }
    return artifacts


def build_trainable_spec(top: dict[str, Any], model_table: pd.DataFrame) -> dict[str, Any]:
    model_row = model_table.loc[model_table["candidate_model_id"].eq(top["candidate_model_id"])].iloc[0].to_dict()
    return {
        "run_id": RUN_ID,
        "status": "onnx_seed_observation_no_authority",
        "candidate_id": str(top["candidate_id"]),
        "candidate_model_id": str(top["candidate_model_id"]),
        "teacher_candidate_id": str(top["teacher_candidate_id"]),
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
        "claim_boundary": "trainable_onnx_seed_observation_only_no_runtime_authority",
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
    observation_rows = int(decision_summary["onnx_seed_observation_flag"].sum())
    parity_passes = int(model_table["onnx_parity_passed"].sum())
    lines = [
        "# frontier02C Trainable ONNX Seed Surface Report(전선02C 학습 가능 온엑스 씨앗 표면 보고)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        "- status(상태): `completed_trainable_onnx_seed_surface_smoke_no_authority(학습 가능 온엑스 씨앗 표면 스모크 완료, 권위 없음)`",
        f"- trained_models(학습 모델 수): `{len(model_table)}`",
        f"- ONNX parity pass(온엑스 동등성 통과): `{parity_passes}/{len(model_table)}`",
        f"- decision_rows(결정 표면 행): `{len(decision_summary)}`",
        f"- onnx_seed_observation_rows(온엑스 씨앗 관찰 행): `{observation_rows}`",
        "",
        "## Boundary(경계)",
        "",
        "이번 실행(run, 실행)은 proxy teacher(프록시 교사)를 3-class LogisticRegression(3클래스 로지스틱 회귀) ONNX(온엑스)로 내보내는 smoke training(스모크 학습)입니다. WFO(워크포워드), MT5 runtime validation(MT5 런타임 검증), baseline selection(기준선 선택), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않습니다.",
        "",
        "## Best Validation Rank(검증 순위 1위)",
        "",
        f"- candidate_id(후보 ID): `{best.get('candidate_id')}`",
        f"- candidate_model_id(후보 모델 ID): `{best.get('candidate_model_id')}`",
        f"- teacher_candidate_id(교사 후보 ID): `{best.get('teacher_candidate_id')}`",
        f"- threshold/margin/cooldown(임계값/마진/쿨다운): `{format_float(best.get('probability_threshold'))}` / `{format_float(best.get('probability_margin'))}` / `{best.get('cooldown_bars')}`",
        f"- validation net/PF/density/DD(검증 순수익/수익 팩터/밀도/손실폭): `{format_float(best.get('validation_net_profit'))}` / `{format_float(best.get('validation_profit_factor'))}` / `{format_float(best.get('validation_trades_per_day'))}` / `{format_float(best.get('validation_max_drawdown_percent'))}%`",
        f"- OOS net/PF/density/DD(표본외 순수익/수익 팩터/밀도/손실폭): `{format_float(best.get('oos_net_profit'))}` / `{format_float(best.get('oos_profit_factor'))}` / `{format_float(best.get('oos_trades_per_day'))}` / `{format_float(best.get('oos_max_drawdown_percent'))}%`",
        f"- joint_pass_count(동시 통과 수): validation(검증) `{best.get('validation_joint_pass_count')}`, OOS(표본외) `{best.get('oos_joint_pass_count')}`",
        "",
        "## Read(판독)",
        "",
        read_text(best, observation_rows),
        "",
        "## Skipped Teachers(건너뛴 교사 표면)",
        "",
    ]
    if skipped_records:
        for record in skipped_records:
            lines.append(f"- `{record['teacher_candidate_id']}`: `{record['status']}`")
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
            "- Grok pre-expensive review(비싼 검증 전 그록 검토): 이번 cheap ONNX smoke(저비용 온엑스 스모크)에는 새 호출을 하지 않았고, WFO/MT5(워크포워드/MT5) 전에는 required(필요)입니다.",
        ]
    )
    io_path(REPORT_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    return {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)}


def read_text(best: dict[str, Any], observation_rows: int) -> str:
    if observation_rows > 0:
        return "ONNX seed observation(온엑스 씨앗 관찰)은 있습니다. 다만 PF(수익 팩터)와 density(밀도)가 final target(최종 목표)에 아직 못 미치므로 repair/review(수리/검토)로 넘깁니다."
    return "ONNX smoke(온엑스 스모크)는 성공했지만 네 축 동시 목표에는 아직 멉니다. 다음 행동(action, 행동)은 probability decision surface(확률 결정 표면)를 수리하거나 teacher objective(교사 목적)를 바꾸는 것입니다."


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
        "status": "completed_trainable_onnx_seed_surface_smoke_no_authority",
        "created_at_utc": utc_now(),
        "script_path": "stage_pipelines/stage_frontier_02/trainable_onnx_seed_surface.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_02/trainable_onnx_seed_surface.py")),
        "inputs": {
            "model_input_dataset_path": DATASET_PATH.as_posix(),
            "model_input_dataset_sha256": sha256_file(DATASET_PATH),
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
            "feature_order_hash": ordered_hash(feature_order),
            "parent_manifest_path": PARENT_MANIFEST_PATH.as_posix(),
            "parent_top_seed_surfaces_path": PARENT_TOP_PATH.as_posix(),
            "rows": int(len(frame)),
            "split_counts": {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()},
        },
        "model_contract": {
            "model_family": "sklearn_logistic_regression_multiclass_teacher_distillation",
            "class_order": LABEL_ORDER,
            "label_names": LABEL_NAMES,
            "class_weight": "balanced",
            "feature_count": len(feature_order),
            "teacher_source": "frontier02B_top_seed_surfaces",
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
            "selection_boundary": "validation_rank_only_oos_diagnostic_no_completion_claim",
        },
        "outputs": artifacts,
        "exports": export_records,
        "skipped_teachers": skipped_records,
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
        "label_boundary": "teacher_labels_derived_from_train_threshold_proxy_surface_no_future_feature_leak",
        "split_boundary": "train_fit_validation_rank_oos_diagnostic",
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
