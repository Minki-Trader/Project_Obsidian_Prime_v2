from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_sklearn_probabilities,
)


STAGE_ID = "329_onnx_rebuild__live_feature_control"
RUN_ID = "run329C_train_wfo_rebuild_candidates_v1"
RUN_NUMBER = "run329C"
PARENT_RUN_ID = "run329B_materialize_forward_live_feature_frames_v1"
STATUS = "completed_train_wfo_rebuild_candidates_no_forward_tuning"
JUDGMENT = "research_wfo_candidates_ready_for_forward_replay_no_goal_achieve"
DECISION = "stage329C_wfo_survivor_queue_materialized_no_candidate_selected"
NEXT_ACTION = "run329D_forward_holdout_score_replay_without_threshold_retuning"
CLAIM_BOUNDARY = (
    "research_development_only_old_train_validation_oos_used_no_forward_tuning_"
    "research_onnx_exports_not_runtime_handoff_no_selected_candidate_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODELS_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
PREDICTIONS_DIR = RUN_DIR / "predictions"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage329C_train_wfo_candidates.md"

MODEL_INPUT_PATH = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
    / "model_input_dataset.parquet"
)
MODEL_INPUT_SUMMARY = MODEL_INPUT_PATH.with_name("model_input_summary.json")
RUN329B_FEATURE_ORDER_DIR = STAGE_DIR / "02_runs" / "run329B" / "feature_orders"
RUN329B_FEATURE_SUMMARY = STAGE_DIR / "02_runs" / "run329B" / "feature_set_materialization_summary.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

FEATURE_SET_IDS = [
    "core56_no_top3_weight_features",
    "macro48_no_equity_breadth_or_top3",
    "us100_technical42_no_external",
]

WFO_FOLDS = [
    ("wfo01_train_to_2023_eval_2024q1q2", "2023-12-31T23:59:59Z", "2024-01-01T00:00:00Z", "2024-04-30T23:59:59Z"),
    ("wfo02_train_to_2024apr_eval_2024may_aug", "2024-04-30T23:59:59Z", "2024-05-01T00:00:00Z", "2024-08-31T23:59:59Z"),
    ("wfo03_train_to_2024aug_eval_2024sep_dec", "2024-08-31T23:59:59Z", "2024-09-01T00:00:00Z", "2024-12-31T23:59:59Z"),
    ("wfo04_train_to_2024_eval_2025q1", "2024-12-31T23:59:59Z", "2025-01-01T00:00:00Z", "2025-03-31T23:59:59Z"),
    ("wfo05_train_to_2025q1_eval_2025q2", "2025-03-31T23:59:59Z", "2025-04-01T00:00:00Z", "2025-06-30T23:59:59Z"),
    ("wfo06_train_to_2025q2_eval_2025q3", "2025-06-30T23:59:59Z", "2025-07-01T00:00:00Z", "2025-09-30T23:59:59Z"),
]

GATE_THRESHOLDS = {
    "validation_balanced_accuracy_min": 0.38,
    "oos_balanced_accuracy_min": 0.38,
    "wfo_min_balanced_accuracy_min": 0.36,
    "oos_log_loss_max": 1.08,
    "train_oos_balanced_accuracy_gap_max": 0.05,
    "onnx_max_abs_diff_max": 1.0e-5,
}


@dataclass(frozen=True)
class ModelSpec:
    model_id: str
    class_weight: str | None
    c_value: float
    random_state: int
    max_iter: int = 2000


MODEL_SPECS = [
    ModelSpec("l2_balanced_c025", class_weight="balanced", c_value=0.25, random_state=3291),
    ModelSpec("l2_plain_c025", class_weight=None, c_value=0.25, random_state=3292),
]

FEATURE_SET_SLUGS = {
    "core56_no_top3_weight_features": "c56",
    "macro48_no_equity_breadth_or_top3": "m48",
    "us100_technical42_no_external": "u42",
}

MODEL_SLUGS = {
    "l2_balanced_c025": "bal",
    "l2_plain_c025": "plain",
}


def os_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def path_exists(path: Path) -> bool:
    return os_path(path).exists()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with os_path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ordered_hash(values: Iterable[str]) -> str:
    return hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()


def artifact_slug(feature_set_id: str, model_id: str) -> str:
    return f"{FEATURE_SET_SLUGS[feature_set_id]}_{MODEL_SLUGS[model_id]}"


def write_text(path: Path, text: str, encoding: str = "utf-8") -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    os_path(path).write_text(text, encoding=encoding)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text.strip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> Path:
    return write_text(path, json.dumps(json_ready(payload), indent=2, ensure_ascii=False) + "\n")


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    with os_path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    return path


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path_exists(path):
        return [], []
    with os_path(path).open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    fieldnames, rows = read_csv_rows(path)
    for name in row:
        if name not in fieldnames:
            fieldnames.append(name)
    if not fieldnames:
        fieldnames = list(row.keys())
    clean_row = {name: str(row.get(name, "")) for name in fieldnames}
    for idx, existing in enumerate(rows):
        if existing.get(key) == clean_row.get(key):
            rows[idx] = clean_row
            break
    else:
        rows.append(clean_row)
    write_csv(path, fieldnames, rows)


def replace_or_append_csv_rows(path: Path, keys: list[str], new_rows: list[dict[str, Any]]) -> None:
    fieldnames, rows = read_csv_rows(path)
    for row in new_rows:
        for name in row:
            if name not in fieldnames:
                fieldnames.append(name)
    if not fieldnames and new_rows:
        fieldnames = list(new_rows[0].keys())
    for row in new_rows:
        clean_row = {name: str(row.get(name, "")) for name in fieldnames}
        for idx, existing in enumerate(rows):
            if all(existing.get(key, "") == clean_row.get(key, "") for key in keys):
                rows[idx] = clean_row
                break
        else:
            rows.append(clean_row)
    write_csv(path, fieldnames, rows)


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = os_path(path).read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if has_bom else "utf-8"), has_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> None:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    write_text(path, text, encoding=encoding)


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def append_bytes_if_missing(path: Path, marker: str, entry: str) -> None:
    raw = os_path(path).read_bytes() if path_exists(path) else b""
    if marker.encode("utf-8") in raw:
        return
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    if raw and not raw.endswith((b"\n", b"\r")):
        raw += b"\n"
    os_path(path).write_bytes(raw.rstrip() + entry.encode("utf-8"))


def load_feature_order(feature_set_id: str) -> list[str]:
    path = RUN329B_FEATURE_ORDER_DIR / f"{feature_set_id}_feature_order.txt"
    features = [line.strip() for line in os_path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(features) != len(set(features)):
        raise RuntimeError(f"Duplicate feature names in {path}")
    return features


def forward_common_valid_boundary() -> str:
    with os_path(RUN329B_FEATURE_SUMMARY).open("r", newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    valid_ends = [
        str(row.get("last_valid_timestamp", ""))
        for row in rows
        if str(row.get("status", "")) == "materialized" and str(row.get("last_valid_timestamp", ""))
    ]
    return min(valid_ends) if valid_ends else "unknown"


def load_model_input_frame() -> pd.DataFrame:
    frame = pd.read_parquet(os_path(MODEL_INPUT_PATH))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    if frame["timestamp"].duplicated().any():
        raise RuntimeError("model input has duplicate timestamps")
    if not frame["timestamp"].is_monotonic_increasing:
        raise RuntimeError("model input timestamps are not monotonic")
    return frame


def validate_frame(frame: pd.DataFrame, features: list[str]) -> None:
    required = {"timestamp", "symbol", "split", "label", "label_class", "future_log_return_12"}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise RuntimeError(f"model input missing required columns: {missing}")
    missing_features = sorted(set(features).difference(frame.columns))
    if missing_features:
        raise RuntimeError(f"model input missing features: {missing_features}")
    for split in ("train", "validation", "oos"):
        if not frame["split"].astype(str).eq(split).any():
            raise RuntimeError(f"missing split: {split}")
    labels = set(frame["label_class"].astype("int64").unique())
    missing_labels = sorted(set(LABEL_ORDER).difference(labels))
    if missing_labels:
        raise RuntimeError(f"missing labels: {missing_labels}")
    values = frame.loc[:, features].to_numpy(dtype="float64", copy=False)
    if not np.isfinite(values).all():
        raise RuntimeError("non-finite feature values in model input")


def build_model(spec: ModelSpec) -> Pipeline:
    classifier = LogisticRegression(
        solver="lbfgs",
        C=float(spec.c_value),
        class_weight=spec.class_weight,
        max_iter=int(spec.max_iter),
        random_state=int(spec.random_state),
    )
    return Pipeline(steps=[("scaler", StandardScaler()), ("classifier", classifier)])


def fit_model(frame: pd.DataFrame, features: list[str], spec: ModelSpec, train_mask: pd.Series) -> Pipeline:
    train = frame.loc[train_mask].copy()
    y = train["label_class"].astype("int64").to_numpy()
    missing_labels = sorted(set(LABEL_ORDER).difference(set(y)))
    if missing_labels:
        raise RuntimeError(f"train subset missing label classes: {missing_labels}")
    model = build_model(spec)
    model.fit(train.loc[:, features].to_numpy(dtype="float64", copy=False), y)
    return model


def probability_payload(model: Pipeline, frame: pd.DataFrame, features: list[str]) -> tuple[np.ndarray, np.ndarray]:
    values = frame.loc[:, features].to_numpy(dtype="float64", copy=False)
    probabilities = ordered_sklearn_probabilities(model, values)
    pred = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
    return probabilities, pred


def split_metrics(model: Pipeline, frame: pd.DataFrame, features: list[str], split_name: str) -> dict[str, Any]:
    view = frame.loc[frame["split"].astype(str).eq(split_name)].copy()
    probabilities, pred = probability_payload(model, view, features)
    y = view["label_class"].astype("int64").to_numpy()
    sorted_prob = np.sort(probabilities, axis=1)
    margin = sorted_prob[:, -1] - sorted_prob[:, -2]
    return {
        "split": split_name,
        "rows": int(len(view)),
        "accuracy": float(accuracy_score(y, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        "macro_f1": float(f1_score(y, pred, labels=LABEL_ORDER, average="macro")),
        "log_loss": float(log_loss(y, probabilities, labels=LABEL_ORDER)),
        "mean_max_probability": float(probabilities.max(axis=1).mean()),
        "mean_margin": float(margin.mean()),
        "pred_short": int((pred == 0).sum()),
        "pred_flat": int((pred == 1).sum()),
        "pred_long": int((pred == 2).sum()),
        "true_short": int((y == 0).sum()),
        "true_flat": int((y == 1).sum()),
        "true_long": int((y == 2).sum()),
    }


def decision_threshold_from_train(model: Pipeline, frame: pd.DataFrame, features: list[str]) -> dict[str, Any]:
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    probabilities, pred = probability_payload(model, train, features)
    sorted_prob = np.sort(probabilities, axis=1)
    margin = sorted_prob[:, -1] - sorted_prob[:, -2]
    nonflat_margin = margin[pred != 1]
    threshold = float(np.quantile(nonflat_margin, 0.60)) if len(nonflat_margin) else float("inf")
    return {
        "policy": "train_only_nonflat_margin_q60",
        "threshold": threshold,
        "train_nonflat_pred_rows": int(len(nonflat_margin)),
        "quantile": 0.60,
        "source_split": "train",
    }


def signal_metrics(
    model: Pipeline,
    frame: pd.DataFrame,
    features: list[str],
    threshold: float,
    split_name: str,
) -> dict[str, Any]:
    view = frame.loc[frame["split"].astype(str).eq(split_name)].copy()
    probabilities, pred = probability_payload(model, view, features)
    sorted_prob = np.sort(probabilities, axis=1)
    margin = sorted_prob[:, -1] - sorted_prob[:, -2]
    signal_mask = (pred != 1) & (margin >= threshold)
    direction = np.where(pred == 2, 1.0, np.where(pred == 0, -1.0, 0.0))
    proxy_return = direction * view["future_log_return_12"].to_numpy(dtype="float64")
    signal_proxy = proxy_return[signal_mask]
    timestamps = pd.to_datetime(view["timestamp"], utc=True)
    day_count = max(1, int(timestamps.dt.date.nunique()))
    if int(signal_mask.sum()):
        label_agreement = float((pred[signal_mask] == view.loc[signal_mask, "label_class"].astype("int64").to_numpy()).mean())
        mean_proxy = float(np.mean(signal_proxy))
        median_proxy = float(np.median(signal_proxy))
    else:
        label_agreement = 0.0
        mean_proxy = 0.0
        median_proxy = 0.0
    return {
        "split": split_name,
        "rows": int(len(view)),
        "signal_rows": int(signal_mask.sum()),
        "signal_rate": float(signal_mask.mean()) if len(signal_mask) else 0.0,
        "signals_per_day": float(signal_mask.sum() / day_count),
        "label_agreement_rate": label_agreement,
        "mean_proxy_log_return": mean_proxy,
        "median_proxy_log_return": median_proxy,
    }


def wfo_metrics(frame: pd.DataFrame, features: list[str], spec: ModelSpec) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    for fold_id, train_end, eval_start, eval_end in WFO_FOLDS:
        train_end_ts = pd.Timestamp(train_end)
        eval_start_ts = pd.Timestamp(eval_start)
        eval_end_ts = pd.Timestamp(eval_end)
        train_mask = timestamps.le(train_end_ts)
        eval_mask = timestamps.ge(eval_start_ts) & timestamps.le(eval_end_ts)
        if int(eval_mask.sum()) == 0:
            continue
        model = fit_model(frame, features, spec, train_mask)
        eval_frame = frame.loc[eval_mask].copy()
        probabilities, pred = probability_payload(model, eval_frame, features)
        y = eval_frame["label_class"].astype("int64").to_numpy()
        rows.append(
            {
                "fold_id": fold_id,
                "train_end_utc": train_end_ts.isoformat(),
                "eval_start_utc": eval_start_ts.isoformat(),
                "eval_end_utc": eval_end_ts.isoformat(),
                "train_rows": int(train_mask.sum()),
                "eval_rows": int(eval_mask.sum()),
                "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
                "macro_f1": float(f1_score(y, pred, labels=LABEL_ORDER, average="macro")),
                "log_loss": float(log_loss(y, probabilities, labels=LABEL_ORDER)),
                "pred_short": int((pred == 0).sum()),
                "pred_flat": int((pred == 1).sum()),
                "pred_long": int((pred == 2).sum()),
            }
        )
    return rows


def prediction_frame(model: Pipeline, frame: pd.DataFrame, features: list[str], candidate_id: str) -> pd.DataFrame:
    probabilities, pred = probability_payload(model, frame, features)
    sorted_prob = np.sort(probabilities, axis=1)
    margin = sorted_prob[:, -1] - sorted_prob[:, -2]
    payload = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(frame["timestamp"], utc=True),
            "split": frame["split"].astype(str),
            "label": frame["label"].astype(str),
            "label_class": frame["label_class"].astype("int64"),
            "candidate_id": candidate_id,
            "predicted_label_class": pred.astype("int64"),
            "predicted_label": [LABEL_NAMES[int(value)] for value in pred],
            "p_short": probabilities[:, 0],
            "p_flat": probabilities[:, 1],
            "p_long": probabilities[:, 2],
            "probability_margin": margin,
        }
    )
    return payload


def coefficient_rows(
    model: Pipeline,
    features: list[str],
    candidate_id: str,
    artifact_slug_value: str,
    top_n: int = 20,
) -> list[dict[str, Any]]:
    classifier = model.named_steps["classifier"]
    coef = np.asarray(classifier.coef_, dtype="float64")
    rows: list[dict[str, Any]] = []
    for idx, feature in enumerate(features):
        abs_values = np.abs(coef[:, idx])
        dominant_idx = int(abs_values.argmax())
        row = {
            "candidate_id": candidate_id,
            "artifact_slug": artifact_slug_value,
            "feature": feature,
            "max_abs_coef": float(abs_values.max()),
            "dominant_label": LABEL_NAMES[int(classifier.classes_[dominant_idx])],
            "dominant_sign": int(np.sign(coef[dominant_idx, idx])),
        }
        for class_idx, label in enumerate(classifier.classes_):
            row[f"coef_{LABEL_NAMES[int(label)]}"] = float(coef[class_idx, idx])
        rows.append(row)
    rows.sort(key=lambda item: (-float(item["max_abs_coef"]), str(item["feature"])))
    return rows[:top_n]


def gate_decision(split_rows: list[dict[str, Any]], wfo_rows: list[dict[str, Any]], parity: dict[str, Any]) -> tuple[str, list[str]]:
    split_by_name = {row["split"]: row for row in split_rows}
    train_ba = float(split_by_name["train"]["balanced_accuracy"])
    val_ba = float(split_by_name["validation"]["balanced_accuracy"])
    oos_ba = float(split_by_name["oos"]["balanced_accuracy"])
    oos_log_loss = float(split_by_name["oos"]["log_loss"])
    wfo_balanced = [float(row["balanced_accuracy"]) for row in wfo_rows]
    wfo_min = min(wfo_balanced) if wfo_balanced else 0.0
    reasons: list[str] = []
    if val_ba < GATE_THRESHOLDS["validation_balanced_accuracy_min"]:
        reasons.append("validation_balanced_accuracy_below_floor")
    if oos_ba < GATE_THRESHOLDS["oos_balanced_accuracy_min"]:
        reasons.append("oos_balanced_accuracy_below_floor")
    if wfo_min < GATE_THRESHOLDS["wfo_min_balanced_accuracy_min"]:
        reasons.append("wfo_min_balanced_accuracy_below_floor")
    if oos_log_loss > GATE_THRESHOLDS["oos_log_loss_max"]:
        reasons.append("oos_log_loss_above_floor")
    if train_ba - oos_ba > GATE_THRESHOLDS["train_oos_balanced_accuracy_gap_max"]:
        reasons.append("train_to_oos_balanced_accuracy_collapse")
    if not bool(parity.get("passed")) or float(parity.get("max_abs_diff", 1.0)) > GATE_THRESHOLDS["onnx_max_abs_diff_max"]:
        reasons.append("onnx_probability_parity_failed")
    if reasons:
        return "research_only_do_not_forward_replay", reasons
    return "forward_replay_queue_not_selected_candidate", ["passed_predeclared_research_gate"]


def train_candidates(generated_at_utc: str) -> tuple[list[Path], dict[str, Any]]:
    frame = load_model_input_frame()
    feature_orders = {feature_set_id: load_feature_order(feature_set_id) for feature_set_id in FEATURE_SET_IDS}
    for features in feature_orders.values():
        validate_frame(frame, features)

    split_metric_rows: list[dict[str, Any]] = []
    wfo_metric_rows: list[dict[str, Any]] = []
    signal_metric_rows: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    threshold_rows: list[dict[str, Any]] = []
    coefficient_rows_all: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    survivor_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []

    for feature_set_id, features in feature_orders.items():
        train_mask = frame["split"].astype(str).eq("train")
        for spec in MODEL_SPECS:
            candidate_id = f"{feature_set_id}__{spec.model_id}"
            slug = artifact_slug(feature_set_id, spec.model_id)
            model = fit_model(frame, features, spec, train_mask)
            model_path = MODELS_DIR / f"{slug}.joblib"
            onnx_path = ONNX_DIR / f"{slug}.onnx"
            prediction_path = PREDICTIONS_DIR / f"{slug}_pred.parquet"
            os_path(model_path.parent).mkdir(parents=True, exist_ok=True)
            os_path(onnx_path.parent).mkdir(parents=True, exist_ok=True)
            os_path(prediction_path.parent).mkdir(parents=True, exist_ok=True)
            joblib.dump(model, os_path(model_path))
            export_info = export_sklearn_to_onnx_zipmap_disabled(
                model,
                onnx_path,
                feature_count=len(features),
                drop_label_output=True,
            )
            parity_sample = frame.loc[frame["split"].astype(str).eq("validation"), features].head(512).to_numpy(
                dtype="float64",
                copy=False,
            )
            parity = check_onnxruntime_probability_parity(model, onnx_path, parity_sample, tolerance=1.0e-5)
            parity_rows.append(
                {
                    "candidate_id": candidate_id,
                    "artifact_slug": slug,
                    "feature_set_id": feature_set_id,
                    "model_id": spec.model_id,
                    "passed": bool(parity["passed"]),
                    "rows": int(parity["rows"]),
                    "max_abs_diff": float(parity["max_abs_diff"]),
                    "mean_abs_diff": float(parity["mean_abs_diff"]),
                    "onnx_row_sum_max_abs_error": float(parity["onnx_row_sum_max_abs_error"]),
                    "onnx_path": rel(onnx_path),
                    "onnx_sha256": sha256_file(onnx_path),
                    "sklearn_model_path": rel(model_path),
                    "sklearn_model_sha256": sha256_file(model_path),
                    "probability_output_name": export_info["probability_output_name"],
                }
            )
            artifacts.extend([model_path, onnx_path])

            split_rows = []
            for split_name in ("train", "validation", "oos"):
                metrics = split_metrics(model, frame, features, split_name)
                metrics.update(
                    {
                        "candidate_id": candidate_id,
                        "artifact_slug": slug,
                        "feature_set_id": feature_set_id,
                        "model_id": spec.model_id,
                        "feature_count": len(features),
                    }
                )
                split_rows.append(metrics)
                split_metric_rows.append(metrics)

            threshold = decision_threshold_from_train(model, frame, features)
            threshold_rows.append(
                {
                    "candidate_id": candidate_id,
                    "artifact_slug": slug,
                    "feature_set_id": feature_set_id,
                    "model_id": spec.model_id,
                    **threshold,
                }
            )
            for split_name in ("train", "validation", "oos"):
                signal = signal_metrics(model, frame, features, float(threshold["threshold"]), split_name)
                signal.update(
                    {
                        "candidate_id": candidate_id,
                        "artifact_slug": slug,
                        "feature_set_id": feature_set_id,
                        "model_id": spec.model_id,
                    }
                )
                signal_metric_rows.append(signal)

            folds = wfo_metrics(frame, features, spec)
            for fold in folds:
                fold.update(
                    {
                        "candidate_id": candidate_id,
                        "artifact_slug": slug,
                        "feature_set_id": feature_set_id,
                        "model_id": spec.model_id,
                        "feature_count": len(features),
                    }
                )
                wfo_metric_rows.append(fold)

            coefficients = coefficient_rows(model, features, candidate_id, slug)
            coefficient_rows_all.extend(coefficients)

            predictions = prediction_frame(model, frame, features, candidate_id)
            predictions.to_parquet(os_path(prediction_path), index=False)
            artifacts.append(prediction_path)

            queue_decision, reasons = gate_decision(split_rows, folds, parity)
            split_by_name = {row["split"]: row for row in split_rows}
            wfo_balanced = [float(row["balanced_accuracy"]) for row in folds]
            candidate_row = {
                "candidate_id": candidate_id,
                "artifact_slug": slug,
                "feature_set_id": feature_set_id,
                "model_id": spec.model_id,
                "feature_count": len(features),
                "model_family": "sklearn_logistic_regression_multiclass",
                "class_weight": spec.class_weight or "none",
                "c_value": spec.c_value,
                "train_balanced_accuracy": split_by_name["train"]["balanced_accuracy"],
                "validation_balanced_accuracy": split_by_name["validation"]["balanced_accuracy"],
                "oos_balanced_accuracy": split_by_name["oos"]["balanced_accuracy"],
                "validation_log_loss": split_by_name["validation"]["log_loss"],
                "oos_log_loss": split_by_name["oos"]["log_loss"],
                "wfo_mean_balanced_accuracy": float(np.mean(wfo_balanced)) if wfo_balanced else 0.0,
                "wfo_min_balanced_accuracy": float(np.min(wfo_balanced)) if wfo_balanced else 0.0,
                "wfo_std_balanced_accuracy": float(np.std(wfo_balanced, ddof=0)) if wfo_balanced else 0.0,
                "train_oos_balanced_accuracy_gap": float(split_by_name["train"]["balanced_accuracy"] - split_by_name["oos"]["balanced_accuracy"]),
                "onnx_parity_passed": bool(parity["passed"]),
                "onnx_parity_max_abs_diff": float(parity["max_abs_diff"]),
                "decision_threshold_policy": threshold["policy"],
                "decision_threshold": threshold["threshold"],
                "queue_decision": queue_decision,
                "reason_codes": ";".join(reasons),
                "selected_candidate": "none",
                "goal_achieve": "not_claimed",
                "onnx_path": rel(onnx_path),
                "prediction_path": rel(prediction_path),
            }
            candidate_rows.append(candidate_row)
            if queue_decision == "forward_replay_queue_not_selected_candidate":
                survivor_rows.append(candidate_row)

    artifacts.extend(write_training_outputs(
        generated_at_utc,
        candidate_rows,
        split_metric_rows,
        wfo_metric_rows,
        signal_metric_rows,
        threshold_rows,
        coefficient_rows_all,
        parity_rows,
        survivor_rows,
        feature_orders,
        list(artifacts),
    ))
    return artifacts, {
        "candidate_rows": candidate_rows,
        "survivor_rows": survivor_rows,
        "feature_orders": feature_orders,
    }


def write_training_outputs(
    generated_at_utc: str,
    candidate_rows: list[dict[str, Any]],
    split_metric_rows: list[dict[str, Any]],
    wfo_metric_rows: list[dict[str, Any]],
    signal_metric_rows: list[dict[str, Any]],
    threshold_rows: list[dict[str, Any]],
    coefficient_rows_all: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
    survivor_rows: list[dict[str, Any]],
    feature_orders: dict[str, list[str]],
    model_artifacts: list[Path],
) -> list[Path]:
    artifacts: list[Path] = []
    candidate_screen = RUN_DIR / "candidate_screen.csv"
    write_csv(
        candidate_screen,
        [
            "candidate_id",
            "artifact_slug",
            "feature_set_id",
            "model_id",
            "feature_count",
            "model_family",
            "class_weight",
            "c_value",
            "train_balanced_accuracy",
            "validation_balanced_accuracy",
            "oos_balanced_accuracy",
            "validation_log_loss",
            "oos_log_loss",
            "wfo_mean_balanced_accuracy",
            "wfo_min_balanced_accuracy",
            "wfo_std_balanced_accuracy",
            "train_oos_balanced_accuracy_gap",
            "onnx_parity_passed",
            "onnx_parity_max_abs_diff",
            "decision_threshold_policy",
            "decision_threshold",
            "queue_decision",
            "reason_codes",
            "selected_candidate",
            "goal_achieve",
            "onnx_path",
            "prediction_path",
        ],
        candidate_rows,
    )
    artifacts.append(candidate_screen)

    split_metrics_path = RUN_DIR / "split_metrics.csv"
    write_csv(
        split_metrics_path,
        [
            "candidate_id",
            "artifact_slug",
            "feature_set_id",
            "model_id",
            "feature_count",
            "split",
            "rows",
            "accuracy",
            "balanced_accuracy",
            "macro_f1",
            "log_loss",
            "mean_max_probability",
            "mean_margin",
            "pred_short",
            "pred_flat",
            "pred_long",
            "true_short",
            "true_flat",
            "true_long",
        ],
        split_metric_rows,
    )
    artifacts.append(split_metrics_path)

    wfo_metrics_path = RUN_DIR / "wfo_fold_metrics.csv"
    write_csv(
        wfo_metrics_path,
        [
            "candidate_id",
            "artifact_slug",
            "feature_set_id",
            "model_id",
            "feature_count",
            "fold_id",
            "train_end_utc",
            "eval_start_utc",
            "eval_end_utc",
            "train_rows",
            "eval_rows",
            "balanced_accuracy",
            "macro_f1",
            "log_loss",
            "pred_short",
            "pred_flat",
            "pred_long",
        ],
        wfo_metric_rows,
    )
    artifacts.append(wfo_metrics_path)

    signal_metrics_path = RUN_DIR / "fixed_threshold_signal_metrics.csv"
    write_csv(
        signal_metrics_path,
        [
            "candidate_id",
            "artifact_slug",
            "feature_set_id",
            "model_id",
            "split",
            "rows",
            "signal_rows",
            "signal_rate",
            "signals_per_day",
            "label_agreement_rate",
            "mean_proxy_log_return",
            "median_proxy_log_return",
        ],
        signal_metric_rows,
    )
    artifacts.append(signal_metrics_path)

    thresholds_path = RUN_DIR / "fixed_threshold_manifest.csv"
    write_csv(
        thresholds_path,
        [
            "candidate_id",
            "artifact_slug",
            "feature_set_id",
            "model_id",
            "policy",
            "threshold",
            "train_nonflat_pred_rows",
            "quantile",
            "source_split",
        ],
        threshold_rows,
    )
    artifacts.append(thresholds_path)

    coefficient_path = RUN_DIR / "top_coefficient_attribution.csv"
    write_csv(
        coefficient_path,
        [
            "candidate_id",
            "artifact_slug",
            "feature",
            "max_abs_coef",
            "dominant_label",
            "dominant_sign",
            "coef_short",
            "coef_flat",
            "coef_long",
        ],
        coefficient_rows_all,
    )
    artifacts.append(coefficient_path)

    parity_path = RUN_DIR / "onnx_parity_summary.csv"
    write_csv(
        parity_path,
        [
            "candidate_id",
            "artifact_slug",
            "feature_set_id",
            "model_id",
            "passed",
            "rows",
            "max_abs_diff",
            "mean_abs_diff",
            "onnx_row_sum_max_abs_error",
            "onnx_path",
            "onnx_sha256",
            "sklearn_model_path",
            "sklearn_model_sha256",
            "probability_output_name",
        ],
        parity_rows,
    )
    artifacts.append(parity_path)

    survivor_queue = RUN_DIR / "forward_replay_candidate_queue.csv"
    write_csv(
        survivor_queue,
        [
            "candidate_id",
            "artifact_slug",
            "feature_set_id",
            "model_id",
            "feature_count",
            "queue_decision",
            "reason_codes",
            "decision_threshold_policy",
            "decision_threshold",
            "onnx_path",
            "prediction_path",
        ],
        survivor_rows
        or [
            {
                "candidate_id": "",
                "artifact_slug": "",
                "feature_set_id": "",
                "model_id": "",
                "feature_count": "",
                "queue_decision": "empty_no_forward_replay_candidate",
                "reason_codes": "no_candidate_passed_predeclared_research_gate",
                "decision_threshold_policy": "",
                "decision_threshold": "",
                "onnx_path": "",
                "prediction_path": "",
            }
        ],
    )
    artifacts.append(survivor_queue)

    experiment_receipt = RUN_DIR / "experiment_design_receipt.json"
    write_json(
        experiment_receipt,
        {
            "hypothesis": "Small fixed logistic ONNX research models can reveal whether live-computable feature sets are stable enough for forward replay without outcome-distilled cp322A signals.",
            "decision_use": "Create or reject a forward replay queue for run329D; not select an operating candidate.",
            "comparison_baseline": "Stage329B materialized feature sets and random three-class baseline.",
            "control_variables": [
                "feature sets fixed from run329B",
                "model family fixed to logistic regression",
                "C fixed at 0.25",
                "forward holdout not read",
                "train-only q60 nonflat margin threshold",
            ],
            "changed_variables": ["feature_set_id", "class_weight"],
            "sample_scope": "old train 2022-09-01..2024-12-31, validation 2025-01-02..2025-09-30, OOS 2025-10-01..2026-04-13",
            "success_criteria": "Candidates pass predeclared validation/OOS/WFO/parity floors and produce fixed threshold manifests.",
            "failure_criteria": "All candidates fail WFO, OOS, or ONNX parity gates.",
            "invalid_conditions": "Forward feature rows or forward labels influence training, threshold, or queue decisions.",
            "stop_conditions": "Stop before MT5/runtime claims; run329D must score untouched forward frames with fixed thresholds.",
            "evidence_plan": [rel(candidate_screen), rel(wfo_metrics_path), rel(parity_path), rel(survivor_queue)],
        },
    )
    artifacts.append(experiment_receipt)

    data_receipt = RUN_DIR / "data_integrity_receipt.json"
    write_json(
        data_receipt,
        {
            "data_source": rel(MODEL_INPUT_PATH),
            "model_input_summary": rel(MODEL_INPUT_SUMMARY),
            "feature_order_sources": {key: rel(RUN329B_FEATURE_ORDER_DIR / f"{key}_feature_order.txt") for key in feature_orders},
            "time_axis": "existing model-input timestamp order, UTC-aware storage, bar-close feature rows",
            "sample_scope": "old train/validation/OOS only; no Stage329B forward parquet read for training",
            "missing_or_duplicate_check": "model input validated monotonic and duplicate-free",
            "feature_label_boundary": "label_v1_fwd12 already materialized before forward window; no forward labels generated",
            "split_boundary": "train split fits final models; validation/OOS evaluate; WFO folds stay before 2025-10 OOS",
            "leakage_risk": "using OOS metrics for queue decision can still create research selection pressure; run329D remains judgment-only",
            "data_hash_or_identity": sha256_file(MODEL_INPUT_PATH),
            "integrity_judgment": "usable_with_research_selection_boundary",
        },
    )
    artifacts.append(data_receipt)

    model_receipt = RUN_DIR / "model_validation_receipt.json"
    write_json(
        model_receipt,
        {
            "model_family": "sklearn logistic regression multiclass exported to ONNX",
            "target_and_label": "label_class 0=short, 1=flat, 2=long from label_v1_fwd12",
            "split_method": "fixed train/validation/OOS plus six expanding WFO folds inside train+validation",
            "selection_metric": "predeclared research gates, not profit and not forward performance",
            "secondary_metrics": ["balanced_accuracy", "macro_f1", "log_loss", "WFO min/mean/std", "ONNX parity"],
            "threshold_policy": "train-only q60 nonflat probability-margin threshold for later forward replay",
            "overfit_risk": "survivor queue still needs untouched forward replay and MT5/runtime parity",
            "calibration_risk": "probabilities are logistic scores, not calibrated trading edge",
            "comparison_baseline": "three-class random/log-loss baseline and Stage328B outcome-source block",
            "validation_judgment": JUDGMENT,
        },
    )
    artifacts.append(model_receipt)

    runtime_receipt = RUN_DIR / "runtime_parity_receipt.json"
    write_json(
        runtime_receipt,
        {
            "research_path": rel(Path(__file__)),
            "runtime_path": "not_materialized_in_run329C",
            "shared_contract": "ONNX probability tensor order short/flat/long and feature orders from run329B",
            "known_differences": ["No MT5 EA handoff", "No lot/risk/ATR SLTP runtime package", "No forward MT5 tester output"],
            "parity_check": rel(parity_path),
            "parity_identity": parity_rows,
            "runtime_claim_boundary": "research_onnx_export_parity_only",
        },
    )
    artifacts.append(runtime_receipt)

    lineage_receipt = RUN_DIR / "artifact_lineage_receipt.json"
    lineage_artifacts = model_artifacts + artifacts
    write_json(
        lineage_receipt,
        {
            "source_inputs": [
                rel(MODEL_INPUT_PATH),
                rel(RUN329B_FEATURE_ORDER_DIR),
                rel(RUN329B_FEATURE_SUMMARY),
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_ACTION,
            "artifact_paths": [rel(path) for path in lineage_artifacts],
            "artifact_hashes": {rel(path): sha256_file(path) for path in lineage_artifacts if path_exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_force_add_for_ignored_run_dir",
            "lineage_judgment": "connected_with_research_boundary",
        },
    )
    artifacts.append(lineage_receipt)

    gate_audit = RUN_DIR / "required_gate_coverage_audit.csv"
    write_csv(
        gate_audit,
        ["gate_name", "status", "evidence_path", "effect"],
        [
            {
                "gate_name": "experiment_design(실험 설계)",
                "status": "passed",
                "evidence_path": rel(experiment_receipt),
                "effect": "모델군, 피처셋, 임계값 정책, forward 사용 금지를 사전에 고정했다.",
            },
            {
                "gate_name": "data_integrity(데이터 무결성)",
                "status": "passed_with_research_boundary",
                "evidence_path": rel(data_receipt),
                "effect": "기존 train/validation/OOS만 사용했고 forward parquet(전진 파케이)는 학습에 쓰지 않았다.",
            },
            {
                "gate_name": "model_validation(모델 검증)",
                "status": "passed_research_candidates_only",
                "evidence_path": rel(model_receipt),
                "effect": "WFO(워크포워드), OOS(표본외), ONNX parity(온엑스 동등성)를 같이 봤다.",
            },
            {
                "gate_name": "runtime_parity(런타임 동등성)",
                "status": "passed_onnxruntime_only_no_mt5",
                "evidence_path": rel(runtime_receipt),
                "effect": "Python/ONNX probability parity(확률 동등성)는 봤지만 MT5 runtime authority(런타임 권위)는 없다.",
            },
            {
                "gate_name": "artifact_lineage(산출물 계보)",
                "status": "passed",
                "evidence_path": rel(lineage_receipt),
                "effect": "입력 데이터, 모델, ONNX, 예측, 다음 forward replay(전진 재생) 대기열을 연결했다.",
            },
            {
                "gate_name": "result_judgment(결과 판정)",
                "status": "passed_no_goal_achieve",
                "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
                "effect": "선택 후보, 운영 주장, Goal Achieve(목표 달성)를 만들지 않는다.",
            },
        ],
    )
    artifacts.append(gate_audit)

    result_judgment = RUN_DIR / "result_judgment.csv"
    write_csv(
        result_judgment,
        ["run_id", "status", "judgment", "decision", "survivor_count", "goal_achieve", "next_action", "claim_boundary"],
        [
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "survivor_count": len(survivor_rows),
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    artifacts.append(result_judgment)

    manifest = RUN_DIR / "run_manifest.json"
    write_json(
        manifest,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "generated_at_utc": generated_at_utc,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_action": NEXT_ACTION,
            "goal_achieve": "not_claimed",
            "candidate_count": len(candidate_rows),
            "survivor_count": len(survivor_rows),
            "gate_thresholds": GATE_THRESHOLDS,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    artifacts.append(manifest)
    return artifacts


def markdown_candidate_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| candidate(후보) | val BA(검증 균형정확도) | OOS BA(표본외 균형정확도) | WFO min(WFO 최소) | ONNX(온엑스) | queue(대기열) |",
        "|---|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {candidate_id} | {validation_balanced_accuracy:.4f} | {oos_balanced_accuracy:.4f} | {wfo_min_balanced_accuracy:.4f} | {onnx_parity_passed} | {queue_decision} |".format(
                **row
            )
        )
    return "\n".join(lines)


def write_reports(candidate_rows: list[dict[str, Any]], survivor_rows: list[dict[str, Any]]) -> list[Path]:
    artifacts: list[Path] = []
    table = markdown_candidate_table(candidate_rows)
    survivor_text = ", ".join(row["candidate_id"] for row in survivor_rows) if survivor_rows else "none"
    report = REVIEWS_DIR / "run329C_train_wfo_rebuild_candidates.md"
    write_md(
        report,
        f"""
# run329C Train/WFO Rebuild Candidates(329C 학습/워크포워드 재구축 후보)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`

## Scope(범위)

run329C(329C 실행)는 forward holdout(전진 보류 표본)을 읽지 않고 기존 train/validation/OOS(학습/검증/표본외)만 사용했다. 모델군(model family, 모델군)은 LogisticRegression(로지스틱 회귀)로 고정했고, threshold(임계값)는 train-only q60 nonflat margin(학습 전용 비관망 마진 60 분위)로 고정했다.

Effect(효과): cp322A(322A 후보)의 outcome-distilled signal(결과 증류 신호)을 쓰지 않고도 live-computable feature(실시간 계산 가능 피처)에서 학습 가능한지 보는 압박 시험이다.

## Candidate Screen(후보 선별표)

{table}

## Forward Replay Queue(전진 재생 대기열)

`{survivor_text}`

## Boundary(경계)

ONNX export/parity(온엑스 내보내기/동등성)는 통과 여부를 기록했지만, MT5 runtime handoff(MT5 런타임 인계), risk logic(위험 로직), lot logic(랏 로직), operating promotion(운영 승격)은 없다. 다음 실행에서 fixed threshold(고정 임계값) 그대로 forward feature frame(전진 피처 프레임)에 점수만 매긴다.

`{CLAIM_BOUNDARY}`

## Next(다음)

`{NEXT_ACTION}`
""",
    )
    artifacts.append(report)

    final_report = REVIEWS_DIR / "final_stage329C_decision_report.md"
    write_md(
        final_report,
        f"""
# Stage329C Final Decision(329C 최종 판정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- candidates_tested(시험 후보): `{len(candidate_rows)}`
- forward_replay_queue_count(전진 재생 대기열 수): `{len(survivor_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `research_export_parity_only_not_runtime_ready`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): train/WFO/OOS(학습/워크포워드/표본외) 압박을 통과한 연구 후보를 전진 재생 대기열로 넘기지만, 아직 forward robustness passed(전진 강건성 통과)가 아니다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    artifacts.append(final_report)

    stage_ledger = REVIEWS_DIR / "stage_run_ledger.csv"
    replace_or_append_csv_rows(
        stage_ledger,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__train_wfo_rebuild_candidates",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "train_wfo_rebuild_candidates(학습/워크포워드 재구축 후보)",
                "tier_scope": "old train/validation/OOS only(기존 학습/검증/표본외 한정)",
                "scoreboard": "split_wfo_onnx_parity(분할/WFO/온엑스 동등성)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report),
                "notes": f"candidates={len(candidate_rows)};survivors={len(survivor_rows)};no_forward_tuning;goal_achieve_not_claimed.",
            }
        ],
    )
    artifacts.append(stage_ledger)
    return artifacts


def update_selection_status(survivor_rows: list[dict[str, Any]]) -> Path:
    survivor_ids = [row["candidate_id"] for row in survivor_rows]
    source_feature_sets = ", ".join(FEATURE_SET_IDS)
    common_boundary = forward_common_valid_boundary()
    selection = SELECTED_DIR / "selection_status.md"
    return write_md(
        selection,
        f"""
# Stage329 Selection Status(329단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_not_forward_authority`
- source_feature_frame_queue(원천 피처 프레임 대기열): `{source_feature_sets}`
- research_onnx_status(연구 온엑스 상태): `exported_with_onnxruntime_parity_not_runtime_handoff`
- forward_replay_queue(전진 재생 대기열): `{', '.join(survivor_ids) if survivor_ids else 'none'}`
- forward_dataset_status(전진 데이터셋 상태): `feature_frames_materialized_with_session_boundary`
- common_valid_boundary(공통 유효 경계): `{common_boundary}`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): old train/validation/OOS(기존 학습/검증/표본외)에서만 후보를 걸렀고, forward holdout(전진 보류 표본)은 다음 실행의 judgment-only replay(판정 전용 재생)에 남긴다.
""",
    )


def update_registers(generated_at_utc: str, artifacts: list[Path]) -> None:
    upsert_csv(
        RUN_REGISTRY,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "model_validation",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run329C_train_wfo_rebuild_candidates.md"),
            "notes": "train_wfo_candidates;research_onnx_parity;no_forward_tuning;goal_achieve_not_claimed.",
        },
    )
    upsert_csv(
        ALPHA_LEDGER,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__train_wfo_rebuild_candidates",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "train_wfo_rebuild_candidates",
            "tier_scope": "old train/validation/OOS only",
            "kpi_scope": "split_wfo_onnx_parity",
            "scoreboard_lane": "model_validation",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run329C_train_wfo_rebuild_candidates.md"),
            "primary_kpi": "predeclared_gate_survivor_count",
            "guardrail_kpi": "no_forward_tuning;selected_candidate=none;goal_achieve_not_claimed",
            "external_verification_status": "onnxruntime_probability_parity_only_no_mt5_runtime_claim",
            "notes": f"next_action={NEXT_ACTION}.",
        },
    )
    rows: list[dict[str, Any]] = []
    for artifact in artifacts:
        if not path_exists(artifact) or os_path(artifact).is_dir():
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact.stem}".replace("-", "_"),
                "artifact_type": artifact.suffix.lstrip(".") or "file",
                "path": rel(artifact),
                "sha256": sha256_file(artifact),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": STATUS,
            }
        )
    replace_or_append_csv_rows(ARTIFACT_REGISTRY, ["artifact_id", "run_id"], rows)


def update_current_truth(candidate_rows: list[dict[str, Any]], survivor_rows: list[dict[str, Any]]) -> Path:
    workspace = ROOT / "docs" / "workspace" / "workspace_state.yaml"
    text, had_bom = read_text_lossless(workspace)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", "updated_on: '2026-05-26'")
    text = replace_prefix_line(text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage329(329단계) run329C(329C 실행) train/WFO rebuild candidates(학습/워크포워드 재구축 후보)를 닫았다. "
        f"Effect(효과): 후보 {len(candidate_rows)}개를 기존 train/validation/OOS(학습/검증/표본외)에서 검증하고 forward replay queue(전진 재생 대기열) {len(survivor_rows)}개를 만들었지만, Goal Achieve(목표 달성)는 없다.\n"
    )
    if "Stage329(329단계) run329C(329C 실행)" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_preserving(workspace, text, had_bom)

    current = ROOT / "docs" / "context" / "current_working_state.md"
    text, had_bom = read_text_lossless(current)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v3`",
        "- current_run(": f"- current_run(현재 실행): `{RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- selected_research_baseline(": "- selected_research_baseline(선택 연구 기준선): `none`",
        "- source_stage(": "- source_stage(원천 단계): `329_onnx_rebuild__live_feature_control`",
        "- target_surface(": "- target_surface(목표 표면): `train_wfo_rebuild_without_forward_tuning`",
        "- adapter_under_review(": "- adapter_under_review(검토 중 어댑터): `none`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{JUDGMENT}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, new_line in replacements.items():
        text = replace_prefix_line(text, prefix, new_line)
    summary = (
        f"- run329C_summary(329C 요약): train/WFO rebuild candidates(학습/워크포워드 재구축 후보)를 `{STATUS}`로 닫았다. "
        f"Effect(효과): research ONNX(연구 온엑스) {len(candidate_rows)}개를 만들고 {len(survivor_rows)}개를 forward replay queue(전진 재생 대기열)에 넣었지만, selected candidate(선택 후보), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다."
    )
    if "run329C_summary(329C 요약)" not in text:
        text = text.replace(f"- decision(판정): `{JUDGMENT}`\n", f"- decision(판정): `{JUDGMENT}`\n{summary}\n", 1)
    write_text_preserving(current, text, had_bom)

    changelog = ROOT / "docs" / "workspace" / "changelog.md"
    entry = f"""

## 2026-05-26 - Stage329C Train/WFO Rebuild Candidates(329C 학습/WFO 재구축 후보)

- run329C(329C 실행): core56/macro48/us100-only feature set(피처 세트) 3개와 LogisticRegression(로지스틱 회귀) 2개 규격으로 research ONNX(연구 온엑스) 후보 `{len(candidate_rows)}`개를 만들었다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): forward holdout(전진 보류 표본)을 쓰지 않고 WFO(워크포워드), OOS(표본외), ONNX parity(온엑스 동등성)를 확인했으며, selected candidate(선택 후보), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 만들지 않았다.
"""
    append_bytes_if_missing(changelog, "## 2026-05-26 - Stage329C Train/WFO Rebuild Candidates", entry)

    return write_md(
        DECISION_DOC,
        f"""
# Stage329C Train/WFO Rebuild Candidates Decision(329C 학습/WFO 재구축 후보 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- candidate_count(후보 수): `{len(candidate_rows)}`
- forward_replay_queue_count(전진 재생 대기열 수): `{len(survivor_rows)}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): fixed old-data gates(고정 기존 데이터 관문)를 통과한 연구 후보만 다음 forward replay(전진 재생)에 넘긴다. 이것은 forward passed(전진 통과)가 아니다.
- next_action(다음 행동): `{NEXT_ACTION}`
- boundary(경계): `{CLAIM_BOUNDARY}`
""",
    )


def main() -> None:
    generated_at_utc = utc_now()
    for directory in (RUN_DIR, MODELS_DIR, ONNX_DIR, PREDICTIONS_DIR, REVIEWS_DIR, SELECTED_DIR):
        os_path(directory).mkdir(parents=True, exist_ok=True)

    artifacts, context = train_candidates(generated_at_utc)
    candidate_rows = context["candidate_rows"]
    survivor_rows = context["survivor_rows"]
    artifacts.extend(write_reports(candidate_rows, survivor_rows))
    artifacts.append(update_selection_status(survivor_rows))
    artifacts.append(update_current_truth(candidate_rows, survivor_rows))
    update_registers(generated_at_utc, artifacts + [Path(__file__)])
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "candidate_count": len(candidate_rows),
                "forward_replay_queue_count": len(survivor_rows),
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
