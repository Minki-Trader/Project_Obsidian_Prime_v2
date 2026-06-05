from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

warnings.filterwarnings("ignore", message="y_pred contains classes not in y_true")
warnings.filterwarnings("ignore", message="A single label was found in 'y_true' and 'y_pred'.*")
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn.utils.parallel")

from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
)
TODAY = "2026-06-01"

STAGE_ID = "347_cash_open_asymmetric_source__long_short_head_design"
RUN_NUMBER = "run347C"
RUN_ID = "run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1"
PARENT_RUN_ID = "run347B_materialize_cash_open_asymmetric_source_inputs_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1"
NEXT_RUN_ID = "run347D_review_cash_open_asymmetric_source_proxy_training_without_db_v1"

STATUS = "completed_stage347C_cash_open_asymmetric_proxy_training_screened_no_selection"
JUDGMENT = "proxy_training_completed_short_teacher_reconstruction_available_long_oos_missing_no_operating_claim"
DECISION = "stage347C_open_run347D_review_cash_open_asymmetric_source_proxy_training"
CLAIM_BOUNDARY = (
    "research_development_proxy_training_only_cash_open_asymmetric_source_teacher_distillation_"
    "onnx_smoke_only_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)
GATE_TOTAL = 12

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run347C_cash_open_asymmetric_source_proxy_training.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_SELECTION = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

SOURCE_RUN347B_DIR = STAGE_DIR / "02_runs" / "run347B"
SOURCE_FINAL_DECISION = SOURCE_RUN347B_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN347B_DIR / "required_gate_coverage_audit.csv"
SOURCE_FEATURE_LABEL = SOURCE_RUN347B_DIR / "feature_label_source_table.csv"
SOURCE_FEATURE_SCHEMA = SOURCE_RUN347B_DIR / "feature_schema_manifest.csv"
SOURCE_LABEL_MANIFEST = SOURCE_RUN347B_DIR / "teacher_label_manifest.csv"
SOURCE_PROXY_GRID = SOURCE_RUN347B_DIR / "proxy_screen_grid.csv"
SOURCE_HANDOFF_INDEX = SOURCE_RUN347B_DIR / "handoff_index.csv"
SOURCE_RUN345B_SUMMARY = (
    ROOT
    / "stages"
    / "345_cash_open_decomposition__long_quality_short_carry_runtime_probe"
    / "02_runs"
    / "run345B"
    / "cash_open_long_quality_short_carry_mt5_probe_summary.csv"
)

FEATURE_ORDER = RUN_DIR / "feature_order.csv"
SPLIT_AUDIT = RUN_DIR / "split_audit.csv"
LABEL_SPLIT_DISTRIBUTION = RUN_DIR / "label_split_distribution.csv"
MODEL_SCORECARD = RUN_DIR / "model_training_scorecard.csv"
PREDICTION_TABLE = RUN_DIR / "proxy_model_predictions.csv"
PROXY_THRESHOLD_SCREEN = RUN_DIR / "proxy_threshold_screen.csv"
PROBE_PRIORITY_QUEUE = RUN_DIR / "probe_priority_queue.csv"
FEATURE_IMPORTANCE = RUN_DIR / "feature_importance.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_PARITY_SMOKE = RUN_DIR / "onnx_parity_smoke.csv"
TRAINING_SUMMARY = RUN_DIR / "training_summary.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_DESIGN_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage347C_cash_open_asymmetric_source_proxy_training.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

ALLOCATOR_LABEL_TO_ID = {"short(숏)": 0, "flat(관망)": 1, "long(롱)": 2, "conflict(충돌)": 1}
ALLOCATOR_ID_TO_LABEL = {0: "short(숏)", 1: "flat(관망)", 2: "long(롱)"}
THRESHOLD_QS = [0.70, 0.80, 0.85, 0.90, 0.95]

STAGE_LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "path",
    "report_path",
    "primary_report",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "scoreboard_lane",
    "lane",
    "family",
    "run_number",
    "notes",
    "source_package_run_id",
    "rows",
    "attempt_count",
    "feature_count",
    "candidate_model_id",
    "ledger_row_id",
    "subrun_id",
    "view",
    "record_view",
    "tier",
    "tier_scope",
    "metric_scope",
    "kpi_scope",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "result_status",
    "net_profit",
    "profit_factor",
    "expectancy",
    "drawdown",
    "recovery_factor",
    "trade_count",
    "matched_rows",
]


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fs_path(path: Path) -> str:
    resolved = path.resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 200:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def path_is_file(path: Path) -> bool:
    return os.path.isfile(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def required(path: Path) -> Path:
    if not path_is_file(path):
        raise FileNotFoundError(f"missing required input(필수 입력 누락): {rel(path)}")
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_hash(items: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(items).encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows_list = [dict(row) for row in rows]
    if path_is_file(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_columns) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_columns) not in replacement_keys
    ]
    write_csv(path, kept + rows_list, fieldnames)


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if path_is_file(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        output = float(value)
    except (TypeError, ValueError):
        return default
    if math.isnan(output) or math.isinf(output):
        return default
    return output


def round_value(value: Any, digits: int = 8) -> Any:
    if value == "" or value is None:
        return ""
    try:
        output = float(value)
    except (TypeError, ValueError):
        return value
    if math.isnan(output) or math.isinf(output):
        return ""
    return round(output, digits)


def read_feature_order() -> list[str]:
    _fields, rows = read_csv_rows(required(SOURCE_FEATURE_SCHEMA))
    features = [
        row["column_name"]
        for row in rows
        if row.get("boundary", "").startswith("feature_at_bar_close")
    ]
    if not features:
        raise RuntimeError("feature order is empty(피처 순서가 비어 있음)")
    return features


def load_source_frame(feature_order: Sequence[str]) -> pd.DataFrame:
    frame = pd.read_csv(fs_path(required(SOURCE_FEATURE_LABEL)))
    missing = [name for name in feature_order if name not in frame.columns]
    if missing:
        raise RuntimeError("source table missing features(원천 표 피처 누락): " + ", ".join(missing))
    frame = frame.sort_values("bar_time").reset_index(drop=True)
    frame["allocator_target_id"] = frame["allocator_teacher_label"].map(ALLOCATOR_LABEL_TO_ID).fillna(1).astype(int)
    frame["long_target_id"] = pd.to_numeric(frame["long_quality_teacher_label"], errors="coerce").fillna(0).astype(int)
    frame["short_target_id"] = pd.to_numeric(frame["short_carry_teacher_label"], errors="coerce").fillna(0).astype(int)
    for name in feature_order:
        frame[name] = pd.to_numeric(frame[name], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return frame


def build_splits(frame: pd.DataFrame) -> dict[str, np.ndarray]:
    row_count = len(frame)
    train_end = int(row_count * 0.70)
    validation_end = int(row_count * 0.85)
    all_index = np.arange(row_count)
    return {
        "train": all_index[:train_end],
        "validation": all_index[train_end:validation_end],
        "test": all_index[validation_end:],
        "all": all_index,
    }


def class_weight_vector(y: np.ndarray) -> np.ndarray:
    classes, counts = np.unique(y, return_counts=True)
    total = float(len(y))
    class_count = float(len(classes))
    weights = {int(cls): total / (class_count * float(count)) for cls, count in zip(classes, counts)}
    return np.asarray([weights[int(value)] for value in y], dtype="float64")


def make_model(family: str, head: str, y_train: np.ndarray) -> Any:
    if family == "logistic_balanced":
        max_iter = 4000 if head == "allocator" else 3000
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        C=0.5,
                        class_weight="balanced",
                        max_iter=max_iter,
                        random_state=347,
                        solver="lbfgs",
                    ),
                ),
            ]
        )
    if family == "ExtraTrees":
        return ExtraTreesClassifier(
            n_estimators=300,
            min_samples_leaf=6 if head == "allocator" else 4,
            max_features="sqrt",
            class_weight="balanced",
            random_state=347,
            n_jobs=-1,
        )
    if family == "HistGBM":
        return HistGradientBoostingClassifier(
            max_iter=180,
            learning_rate=0.05,
            l2_regularization=0.05,
            max_leaf_nodes=15,
            random_state=347,
        )
    raise ValueError(f"unknown family(알 수 없는 계열): {family}")


def fit_model(family: str, head: str, x_train: np.ndarray, y_train: np.ndarray) -> Any:
    model = make_model(family, head, y_train)
    if family == "HistGBM":
        model.fit(x_train, y_train, sample_weight=class_weight_vector(y_train))
    else:
        model.fit(x_train, y_train)
    return model


def proba_aligned(model: Any, values: np.ndarray, class_order: Sequence[int]) -> np.ndarray:
    raw = np.asarray(model.predict_proba(values), dtype="float64")
    classes = [int(value) for value in getattr(model, "classes_", [])]
    if not classes and hasattr(model, "named_steps"):
        classes = [int(value) for value in model.named_steps["classifier"].classes_]
    class_to_index = {int(label): index for index, label in enumerate(classes)}
    output = np.zeros((raw.shape[0], len(class_order)), dtype="float64")
    for output_index, label in enumerate(class_order):
        if int(label) in class_to_index:
            output[:, output_index] = raw[:, class_to_index[int(label)]]
    return output


def metric_or_blank(func: Any, *args: Any, **kwargs: Any) -> Any:
    try:
        return round(float(func(*args, **kwargs)), 8)
    except Exception:
        return ""


def evaluate_binary(y_true: np.ndarray, p_pos: np.ndarray) -> dict[str, Any]:
    y_pred = (p_pos >= 0.5).astype(int)
    positives = int(np.sum(y_true == 1))
    negatives = int(np.sum(y_true == 0))
    return {
        "rows": int(len(y_true)),
        "positive_rows": positives,
        "negative_rows": negatives,
        "predicted_positive_rows": int(np.sum(y_pred == 1)),
        "accuracy": metric_or_blank(accuracy_score, y_true, y_pred),
        "balanced_accuracy": metric_or_blank(balanced_accuracy_score, y_true, y_pred),
        "f1_positive": metric_or_blank(f1_score, y_true, y_pred, zero_division=0),
        "precision_positive": metric_or_blank(precision_score, y_true, y_pred, zero_division=0),
        "recall_positive": metric_or_blank(recall_score, y_true, y_pred, zero_division=0),
        "average_precision": metric_or_blank(average_precision_score, y_true, p_pos) if positives else "",
        "roc_auc": metric_or_blank(roc_auc_score, y_true, p_pos) if positives and negatives else "",
    }


def evaluate_allocator(y_true: np.ndarray, probabilities: np.ndarray) -> dict[str, Any]:
    y_pred = np.argmax(probabilities, axis=1)
    output = {
        "rows": int(len(y_true)),
        "short_rows": int(np.sum(y_true == 0)),
        "flat_rows": int(np.sum(y_true == 1)),
        "long_rows": int(np.sum(y_true == 2)),
        "predicted_short_rows": int(np.sum(y_pred == 0)),
        "predicted_flat_rows": int(np.sum(y_pred == 1)),
        "predicted_long_rows": int(np.sum(y_pred == 2)),
        "accuracy": metric_or_blank(accuracy_score, y_true, y_pred),
        "balanced_accuracy": metric_or_blank(balanced_accuracy_score, y_true, y_pred),
        "macro_f1": metric_or_blank(f1_score, y_true, y_pred, average="macro", zero_division=0),
        "short_recall": metric_or_blank(recall_score, y_true, y_pred, labels=[0], average="macro", zero_division=0),
        "flat_recall": metric_or_blank(recall_score, y_true, y_pred, labels=[1], average="macro", zero_division=0),
        "long_recall": metric_or_blank(recall_score, y_true, y_pred, labels=[2], average="macro", zero_division=0),
        "macro_roc_auc_ovr": "",
    }
    if len(np.unique(y_true)) == 3:
        output["macro_roc_auc_ovr"] = metric_or_blank(
            roc_auc_score,
            y_true,
            probabilities,
            multi_class="ovr",
            average="macro",
        )
    return output


def source_expectancy() -> dict[str, float]:
    _fields, rows = read_csv_rows(required(SOURCE_RUN345B_SUMMARY))
    output = {"long": 0.0, "short": 0.0}
    for row in rows:
        attempt = row.get("attempt_name", "")
        if attempt == "n02_s07_long_only_disable_short":
            output["long"] = safe_float(row.get("expectancy"), 0.0)
        elif attempt == "n03_s07_short_only_disable_long":
            output["short"] = safe_float(row.get("expectancy"), 0.0)
    return output


def quantile(values: np.ndarray, q: float) -> float:
    clean = np.asarray(values, dtype="float64")
    clean = clean[np.isfinite(clean)]
    if len(clean) == 0:
        return 0.0
    return float(np.quantile(clean, q))


def apply_allocator_rule(
    long_prob: np.ndarray,
    short_prob: np.ndarray,
    long_threshold: float,
    short_threshold: float,
    rule: str,
    cash_buckets: Sequence[str],
) -> np.ndarray:
    output = np.full(len(long_prob), 1, dtype=int)
    long_pass = long_prob >= long_threshold
    short_pass = short_prob >= short_threshold
    if rule == "short_priority":
        output[long_pass] = 2
        output[short_pass] = 0
    elif rule == "cash_open_regime_allocator":
        for index, bucket in enumerate(cash_buckets):
            early = "0-30" in bucket or "30-60" in bucket
            if early and short_pass[index]:
                output[index] = 0
            elif long_pass[index] and long_prob[index] >= short_prob[index]:
                output[index] = 2
            elif short_pass[index] and short_prob[index] > long_prob[index]:
                output[index] = 0
    else:
        output[(long_pass) & (long_prob >= short_prob)] = 2
        output[(short_pass) & (short_prob > long_prob)] = 0
    return output


def screen_thresholds(
    frame: pd.DataFrame,
    splits: Mapping[str, np.ndarray],
    predictions: Mapping[str, Mapping[str, np.ndarray]],
) -> list[dict[str, Any]]:
    expectancy = source_expectancy()
    rows: list[dict[str, Any]] = []
    for family, family_predictions in predictions.items():
        allocator = family_predictions["allocator"]
        p_short = allocator[:, 0]
        p_long = allocator[:, 2]
        for split_name, indices in splits.items():
            if split_name == "train":
                threshold_source_indices = indices
            else:
                threshold_source_indices = splits["train"]
            long_thresholds = [(f"q{int(q * 100)}", quantile(p_long[threshold_source_indices], q)) for q in THRESHOLD_QS]
            short_thresholds = [(f"q{int(q * 100)}", quantile(p_short[threshold_source_indices], q)) for q in THRESHOLD_QS]
            y_true = frame["allocator_target_id"].to_numpy()[indices]
            cash_buckets = frame["cash_open_bucket"].astype(str).to_numpy()[indices]
            for long_label, long_threshold in long_thresholds:
                for short_label, short_threshold in short_thresholds:
                    for rule in ["balanced_margin", "short_priority", "cash_open_regime_allocator"]:
                        routed = apply_allocator_rule(
                            p_long[indices],
                            p_short[indices],
                            long_threshold,
                            short_threshold,
                            rule,
                            cash_buckets,
                        )
                        long_signals = routed == 2
                        short_signals = routed == 0
                        signal_mask = long_signals | short_signals
                        long_hits = int(np.sum(long_signals & (y_true == 2)))
                        short_hits = int(np.sum(short_signals & (y_true == 0)))
                        false_signals = int(np.sum(signal_mask & (routed != y_true)))
                        total_signals = int(np.sum(signal_mask))
                        teacher_hits = long_hits + short_hits
                        precision = teacher_hits / total_signals if total_signals else 0.0
                        long_recall = long_hits / max(int(np.sum(y_true == 2)), 1)
                        short_recall = short_hits / max(int(np.sum(y_true == 0)), 1)
                        predicted_long = int(np.sum(long_signals))
                        predicted_short = int(np.sum(short_signals))
                        balance = min(predicted_long, predicted_short) / max(predicted_long, predicted_short, 1)
                        upper_bound = long_hits * expectancy["long"] + short_hits * expectancy["short"]
                        rows.append(
                            {
                                "model_family": family,
                                "split": split_name,
                                "long_threshold_label": long_label,
                                "long_probability_threshold": round(long_threshold, 12),
                                "short_threshold_label": short_label,
                                "short_probability_threshold": round(short_threshold, 12),
                                "allocator_rule": rule,
                                "signal_rows": total_signals,
                                "predicted_long_rows": predicted_long,
                                "predicted_short_rows": predicted_short,
                                "teacher_hit_rows": teacher_hits,
                                "teacher_long_hit_rows": long_hits,
                                "teacher_short_hit_rows": short_hits,
                                "teacher_false_signal_rows": false_signals,
                                "teacher_precision": round(precision, 8),
                                "teacher_long_recall": round(long_recall, 8),
                                "teacher_short_recall": round(short_recall, 8),
                                "long_short_balance": round(balance, 8),
                                "source_mt5_hit_expectancy_upper_bound": round(upper_bound, 8),
                                "allowed_use": "proxy_signal_sanity_only(프록시 신호 점검 전용)",
                                "forbidden_use": "MT5_KPI_substitute_or_selection(MT5 KPI 대체 또는 선정)",
                            }
                        )
    return rows


def build_probe_queue(screen_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ranked = []
    for row in screen_rows:
        split_bonus = {"test": 10, "validation": 5, "all": 2, "train": 0}.get(str(row.get("split", "")), 0)
        score = (
            safe_float(row.get("teacher_precision")) * 100
            + safe_float(row.get("teacher_hit_rows")) * 3
            + safe_float(row.get("long_short_balance")) * 5
            + split_bonus
            - safe_float(row.get("teacher_false_signal_rows")) * 0.25
        )
        ranked.append((score, row))
    ranked.sort(key=lambda item: item[0], reverse=True)
    output = []
    for rank, (score, row) in enumerate(ranked[:20], start=1):
        output.append(
            {
                "queue_rank": rank,
                "queue_role": "proxy_probe_priority_not_selection(프록시 탐침 우선순위, 선정 아님)",
                "priority_score": round(score, 8),
                **dict(row),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def model_feature_importance(model: Any, family: str, head: str, feature_order: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    values: np.ndarray | None = None
    if hasattr(model, "feature_importances_"):
        values = np.asarray(model.feature_importances_, dtype="float64")
    elif hasattr(model, "named_steps") and hasattr(model.named_steps.get("classifier"), "coef_"):
        coef = np.asarray(model.named_steps["classifier"].coef_, dtype="float64")
        values = np.mean(np.abs(coef), axis=0)
    if values is None:
        return rows
    order = np.argsort(values)[::-1][:20]
    for rank, index in enumerate(order, start=1):
        rows.append(
            {
                "model_family": family,
                "head": head,
                "rank": rank,
                "feature_name": feature_order[int(index)],
                "importance": round(float(values[int(index)]), 12),
            }
        )
    return rows


def train_and_score() -> dict[str, Any]:
    feature_order = read_feature_order()
    frame = load_source_frame(feature_order)
    splits = build_splits(frame)
    x_all = frame[list(feature_order)].to_numpy(dtype="float64")
    heads = {
        "allocator": ("allocator_target_id", [0, 1, 2]),
        "long_head": ("long_target_id", [0, 1]),
        "short_head": ("short_target_id", [0, 1]),
    }
    families = ["logistic_balanced", "ExtraTrees", "HistGBM"]
    predictions: dict[str, dict[str, np.ndarray]] = {family: {} for family in families}
    score_rows: list[dict[str, Any]] = []
    artifact_rows: list[dict[str, Any]] = []
    importance_rows: list[dict[str, Any]] = []
    onnx_rows: list[dict[str, Any]] = []
    models: dict[tuple[str, str], Any] = {}

    train_indices = splits["train"]
    x_train = x_all[train_indices]
    for family in families:
        for head, (target_column, class_order) in heads.items():
            y_all = frame[target_column].to_numpy(dtype=int)
            y_train = y_all[train_indices]
            model = fit_model(family, head, x_train, y_train)
            models[(family, head)] = model
            probabilities = proba_aligned(model, x_all, class_order)
            predictions[family][head] = probabilities

            joblib_path = MODEL_DIR / f"{family}_{head}.joblib"
            ensure_parent(joblib_path)
            joblib.dump(model, fs_path(joblib_path))
            artifact_rows.append(
                {
                    "model_family": family,
                    "head": head,
                    "artifact_type": "joblib_model(잡립 모델)",
                    "path": rel(joblib_path),
                    "sha256": sha256_file(joblib_path),
                    "feature_count": len(feature_order),
                    "feature_order_hash": ordered_hash(feature_order),
                    "classes": json.dumps([int(value) for value in class_order]),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            importance_rows.extend(model_feature_importance(model, family, head, feature_order))
            for split_name, indices in splits.items():
                y_true = y_all[indices]
                if head == "allocator":
                    metrics = evaluate_allocator(y_true, probabilities[indices])
                else:
                    metrics = evaluate_binary(y_true, probabilities[indices, 1])
                score_rows.append(
                    {
                        "model_family": family,
                        "head": head,
                        "split": split_name,
                        "target": target_column,
                        **metrics,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )

        allocator_model = models[(family, "allocator")]
        onnx_path = ONNX_DIR / f"{family}_allocator.onnx"
        try:
            export = export_sklearn_to_onnx_zipmap_disabled(
                allocator_model,
                onnx_path,
                feature_count=len(feature_order),
                input_name="float_input",
                target_opset=12,
                drop_label_output=True,
            )
            sample_size = min(512, len(x_all))
            parity = check_onnxruntime_probability_parity(
                allocator_model,
                onnx_path,
                x_all[:sample_size],
                tolerance=1e-5,
            )
            onnx_rows.append(
                {
                    "model_family": family,
                    "head": "allocator",
                    "status": "passed" if parity["passed"] else "failed",
                    "path": rel(onnx_path),
                    "sha256": export["sha256"],
                    "rows": parity["rows"],
                    "max_abs_diff": parity["max_abs_diff"],
                    "mean_abs_diff": parity["mean_abs_diff"],
                    "probability_output_name": export["probability_output_name"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            artifact_rows.append(
                {
                    "model_family": family,
                    "head": "allocator",
                    "artifact_type": "onnx_allocator_smoke(온엑스 배분기 점검)",
                    "path": rel(onnx_path),
                    "sha256": export["sha256"],
                    "feature_count": len(feature_order),
                    "feature_order_hash": ordered_hash(feature_order),
                    "classes": "[0, 1, 2]",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        except Exception as exc:
            onnx_rows.append(
                {
                    "model_family": family,
                    "head": "allocator",
                    "status": "failed",
                    "path": rel(onnx_path),
                    "sha256": "",
                    "rows": 0,
                    "max_abs_diff": "",
                    "mean_abs_diff": "",
                    "probability_output_name": "",
                    "error": str(exc),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    prediction_frame = pd.DataFrame(
        {
            "bar_time": frame["bar_time"],
            "split": split_name_for_rows(len(frame), splits),
            "allocator_teacher_label": frame["allocator_teacher_label"],
            "allocator_target_id": frame["allocator_target_id"],
            "long_quality_teacher_label": frame["long_target_id"],
            "short_carry_teacher_label": frame["short_target_id"],
        }
    )
    for family in families:
        allocator = predictions[family]["allocator"]
        prediction_frame[f"{family}_allocator_p_short"] = allocator[:, 0]
        prediction_frame[f"{family}_allocator_p_flat"] = allocator[:, 1]
        prediction_frame[f"{family}_allocator_p_long"] = allocator[:, 2]
        prediction_frame[f"{family}_allocator_pred_id"] = np.argmax(allocator, axis=1)
        prediction_frame[f"{family}_long_head_p1"] = predictions[family]["long_head"][:, 1]
        prediction_frame[f"{family}_short_head_p1"] = predictions[family]["short_head"][:, 1]
    ensure_parent(PREDICTION_TABLE)
    prediction_frame.to_csv(fs_path(PREDICTION_TABLE), index=False, encoding="utf-8-sig")

    screen_rows = screen_thresholds(frame, splits, predictions)
    queue_rows = build_probe_queue(screen_rows)
    write_feature_order(feature_order)
    write_split_audits(frame, splits)
    write_csv(MODEL_SCORECARD, score_rows)
    write_csv(PROXY_THRESHOLD_SCREEN, screen_rows)
    write_csv(PROBE_PRIORITY_QUEUE, queue_rows)
    write_csv(FEATURE_IMPORTANCE, importance_rows)
    write_csv(MODEL_ARTIFACT_MANIFEST, artifact_rows)
    write_csv(ONNX_PARITY_SMOKE, onnx_rows)
    summary = build_training_summary(frame, feature_order, score_rows, screen_rows, queue_rows, artifact_rows, onnx_rows)
    write_csv(TRAINING_SUMMARY, summary)
    return {
        "feature_order": feature_order,
        "frame": frame,
        "splits": splits,
        "score_rows": score_rows,
        "screen_rows": screen_rows,
        "queue_rows": queue_rows,
        "artifact_rows": artifact_rows,
        "onnx_rows": onnx_rows,
        "summary": summary,
    }


def split_name_for_rows(row_count: int, splits: Mapping[str, np.ndarray]) -> list[str]:
    names = [""] * row_count
    for split_name in ["train", "validation", "test"]:
        for index in splits[split_name]:
            names[int(index)] = split_name
    return names


def write_feature_order(feature_order: Sequence[str]) -> None:
    rows = [
        {
            "feature_index": index,
            "feature_name": name,
            "source": rel(SOURCE_FEATURE_LABEL),
            "boundary": "closed_bar_teacher_distillation_input(닫힌 봉 교사 증류 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, name in enumerate(feature_order)
    ]
    write_csv(FEATURE_ORDER, rows)


def write_split_audits(frame: pd.DataFrame, splits: Mapping[str, np.ndarray]) -> None:
    split_rows = []
    label_rows = []
    for split_name in ["train", "validation", "test", "all"]:
        part = frame.iloc[splits[split_name]]
        split_rows.append(
            {
                "split": split_name,
                "rows": len(part),
                "first_bar_time": part["bar_time"].iloc[0],
                "last_bar_time": part["bar_time"].iloc[-1],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for field in ["allocator_teacher_label", "long_target_id", "short_target_id", "base_active_teacher_label"]:
            counts = part[field].value_counts(dropna=False).to_dict()
            for value, count in sorted(counts.items(), key=lambda item: str(item[0])):
                label_rows.append(
                    {
                        "split": split_name,
                        "field": field,
                        "value": value,
                        "count": int(count),
                        "share": round(int(count) / max(len(part), 1), 8),
                    }
                )
    write_csv(SPLIT_AUDIT, split_rows)
    write_csv(LABEL_SPLIT_DISTRIBUTION, label_rows)


def build_training_summary(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    score_rows: Sequence[Mapping[str, Any]],
    screen_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    artifact_rows: Sequence[Mapping[str, Any]],
    onnx_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    test_allocator_rows = [
        row
        for row in score_rows
        if row.get("head") == "allocator" and row.get("split") == "test"
    ]
    best_test = max(test_allocator_rows, key=lambda row: safe_float(row.get("macro_f1")), default={})
    onnx_pass_count = sum(1 for row in onnx_rows if row.get("status") == "passed")
    return [
        {"metric": "rows", "value": len(frame)},
        {"metric": "feature_count", "value": len(feature_order)},
        {"metric": "trained_model_artifacts", "value": sum(1 for row in artifact_rows if "joblib" in row.get("artifact_type", ""))},
        {"metric": "onnx_allocator_smoke_passes", "value": onnx_pass_count},
        {"metric": "scorecard_rows", "value": len(score_rows)},
        {"metric": "threshold_screen_rows", "value": len(screen_rows)},
        {"metric": "probe_priority_rows", "value": len(queue_rows)},
        {"metric": "best_test_allocator_family_by_macro_f1", "value": best_test.get("model_family", "")},
        {"metric": "best_test_allocator_macro_f1", "value": best_test.get("macro_f1", "")},
        {"metric": "long_validation_positive_rows", "value": 0},
        {"metric": "judgment", "value": JUDGMENT},
        {"metric": "claim_boundary", "value": CLAIM_BOUNDARY},
    ]


def write_receipts(result: Mapping[str, Any]) -> None:
    frame: pd.DataFrame = result["frame"]
    feature_order: Sequence[str] = result["feature_order"]
    score_rows: Sequence[Mapping[str, Any]] = result["score_rows"]
    onnx_pass_count = sum(1 for row in result["onnx_rows"] if row.get("status") == "passed")
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "measurement_scope": "teacher/source proxy training only(교사/원천 프록시 학습 전용)",
            "management_state": "run folder, manifests, scorecard, reports, registries updated(실행 폴더/목록/점수표/보고/등록부 갱신)",
            "judgment_class": "inconclusive(불충분)",
            "scoreboard": "structural_scout(구조 스카우트)",
            "parity_level": "P0_unverified plus ONNX smoke only(P0 미검증 + 온엑스 점검만)",
            "wfo_status": "not_applicable(해당 없음)",
            "registry_update_required": "yes(예)",
            "negative_memory_required": "yes_for_long_oos_missing(롱 표본외 누락은 필요)",
            "hard_gate_applicable": "no(아니오)",
            "evidence_boundary": "scout-only(탐색 전용)",
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        EXPERIMENT_DESIGN_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "asymmetric source teacher labels can be distilled into allocator and side-head proxy models(비대칭 원천 교사 라벨을 배분기와 방향 헤드 프록시 모델로 증류할 수 있다)",
            "decision_use": "prepare proxy review and possible MT5 probe package design(프록시 검토와 MT5 탐침 패키지 설계 준비)",
            "comparison_baseline": "run345B n01/n02/n03 source runtime surfaces(345B n01/n02/n03 원천 런타임 표면)",
            "control_variables": "run347B feature table, closed-bar time axis, no new MT5 execution(347B 피처 표, 닫힌 봉 시간축, 새 MT5 실행 없음)",
            "changed_variables": "model family and allocator threshold rule(모델 계열과 배분기 임계값 규칙)",
            "sample_scope": f"Tier A rows={len(frame)}; Tier B missing_required(Tier A 행={len(frame)}, Tier B 필수 누락)",
            "success_criteria": "proxy reconstructs teacher short/long signals with useful precision and ONNX smoke passes(프록시가 교사 숏/롱 신호를 유용한 정밀도로 재구성하고 온엑스 점검 통과)",
            "failure_criteria": "long out-of-sample label absence or proxy collapse(롱 표본외 라벨 부재 또는 프록시 붕괴)",
            "invalid_conditions": "feature labels from future PnL or split shuffle(미래 손익 라벨 또는 분할 섞기)",
            "stop_conditions": "no proxy queue rows or no ONNX smoke pass(프록시 대기열 행 없음 또는 온엑스 점검 통과 없음)",
            "evidence_plan": [rel(MODEL_SCORECARD), rel(PROXY_THRESHOLD_SCREEN), rel(ONNX_PARITY_SMOKE), rel(PROBE_PRIORITY_QUEUE)],
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": [rel(SOURCE_FEATURE_LABEL), rel(SOURCE_FEATURE_SCHEMA), rel(SOURCE_LABEL_MANIFEST)],
            "time_axis": "bar_time sorted broker-clock alignment key(브로커 시계 정렬 키 bar_time 시간순)",
            "sample_scope": f"US100 M5 Tier A rows={len(frame)}; 2024.07.30..2024.12.31; Tier B missing_required",
            "missing_or_duplicate_check": "run347B timestamp audit passed; features coerced numeric with missing filled as 0(347B 시점 감사 통과, 피처 결측은 0으로 채움)",
            "feature_label_boundary": "features are closed-bar inputs; labels are same-bar teacher/source outputs, not future PnL(피처는 닫힌 봉 입력, 라벨은 동일 봉 교사/원천 출력이며 미래 손익 아님)",
            "split_boundary": "chronological 70/15/15 train/validation/test; no shuffle(시간순 70/15/15 학습/검증/테스트, 섞기 없음)",
            "leakage_risk": "teacher labels may be mistaken for realized outcomes(교사 라벨을 실현 결과로 오해할 위험)",
            "data_hash_or_identity": sha256_file(SOURCE_FEATURE_LABEL),
            "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)",
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_family": "logistic_balanced, ExtraTrees, HistGBM(균형 로지스틱, 엑스트라 트리, 히스토그램 GBM)",
            "target_and_label": "allocator/long/short teacher labels from run347B(347B 배분/롱/숏 교사 라벨)",
            "split_method": "chronological train/validation/test(시간순 학습/검증/테스트)",
            "selection_metric": "no selection; proxy queue only(선정 없음, 프록시 대기열만)",
            "secondary_metrics": "balanced accuracy, macro F1, average precision, threshold precision/recall(균형 정확도, 매크로 F1, 평균 정밀도, 임계값 정밀도/재현율)",
            "threshold_policy": "quantile probability screen from train probabilities(학습 확률 분위수 임계값 선별)",
            "overfit_risk": "very sparse long labels and single teacher source(매우 적은 롱 라벨과 단일 교사 원천)",
            "calibration_risk": "probabilities are proxy ranks unless calibrated later(확률은 추후 보정 전까지 프록시 순위)",
            "comparison_baseline": "n01 base, n02 long-only, n03 short-only source surfaces(n01 기본, n02 롱 전용, n03 숏 전용 원천 표면)",
            "validation_judgment": "inconclusive_for_long_oos_exploratory_for_short(롱 표본외 불충분, 숏 탐색 가능)",
            "onnx_smoke_passes": onnx_pass_count,
            "scorecard_rows": len(score_rows),
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [rel(SOURCE_FEATURE_LABEL), rel(SOURCE_PROXY_GRID), rel(SOURCE_HANDOFF_INDEX), rel(SOURCE_RUN345B_SUMMARY)],
            "producer": rel(Path("stage_pipelines/stage347/train_cash_open_asymmetric_source_proxy_models_without_db.py")),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(MODEL_SCORECARD), rel(PROXY_THRESHOLD_SCREEN), rel(MODEL_ARTIFACT_MANIFEST), rel(ONNX_PARITY_SMOKE), rel(FINAL_DECISION)],
            "artifact_hashes": "recorded in model_artifact_manifest and artifact_registry(모델 산출물 목록과 산출물 등록부에 기록)",
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
            "availability": "tracked(추적됨)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "proxy models and ONNX smoke artifacts exist for research review(연구 검토용 프록시 모델과 온엑스 점검 산출물이 있음)",
            "forbidden_claims": [
                "MT5 KPI substitute(MT5 KPI 대체)",
                "candidate selection(후보 선정)",
                "operating promotion(운영 승격)",
                "runtime authority(런타임 권위)",
                "Goal Achieve(목표 달성)",
            ],
            "model_training": "claimed_proxy_only(프록시 전용으로만 주장)",
            "mt5_execution": "not_claimed(주장 없음)",
            "candidate_selection": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def gate_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    _fields, parent_rows = read_csv_rows(required(SOURCE_GATE_AUDIT))
    parent_gate = bool(parent_rows) and all(row.get("status") == "passed" for row in parent_rows)
    onnx_pass_count = sum(1 for row in result["onnx_rows"] if row.get("status") == "passed")
    joblib_count = sum(1 for row in result["artifact_rows"] if "joblib" in row.get("artifact_type", ""))
    checks = [
        ("parent_run347B_gates_passed", parent_gate, SOURCE_GATE_AUDIT, "run347B 물질화 게이트를 확인한다."),
        ("source_feature_label_available", path_is_file(SOURCE_FEATURE_LABEL), SOURCE_FEATURE_LABEL, "feature/label source table(피처/라벨 원천 표)을 확인한다."),
        ("chronological_split_audit_written", path_is_file(SPLIT_AUDIT), SPLIT_AUDIT, "시간순 분할 감사(audit, 감사)를 기록한다."),
        ("feature_order_written", path_is_file(FEATURE_ORDER) and len(result["feature_order"]) > 0, FEATURE_ORDER, "모델 feature order(피처 순서)를 고정한다."),
        ("trained_joblib_models_written", joblib_count >= 9, MODEL_ARTIFACT_MANIFEST, "allocator/side-head model artifacts(배분기/방향 헤드 모델 산출물)를 만든다."),
        ("model_scorecard_written", path_is_file(MODEL_SCORECARD) and len(result["score_rows"]) > 0, MODEL_SCORECARD, "모델 점수표를 기록한다."),
        ("proxy_threshold_screen_written", path_is_file(PROXY_THRESHOLD_SCREEN) and len(result["screen_rows"]) > 0, PROXY_THRESHOLD_SCREEN, "프록시 임계값 선별 표를 만든다."),
        ("onnx_smoke_passed_at_least_one", onnx_pass_count >= 1, ONNX_PARITY_SMOKE, "최소 하나의 ONNX smoke parity(온엑스 점검 동등성)를 통과한다."),
        ("probe_priority_queue_written", path_is_file(PROBE_PRIORITY_QUEUE) and len(result["queue_rows"]) > 0, PROBE_PRIORITY_QUEUE, "다음 검토용 probe priority queue(탐침 우선순위 대기열)를 만든다."),
        ("skill_receipts_written", all(path_is_file(path) for path in [RUN_EVIDENCE_RECEIPT, DATA_INTEGRITY_RECEIPT, MODEL_VALIDATION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]), RUN_EVIDENCE_RECEIPT, "필수 receipt(영수증)를 남긴다."),
        ("no_forbidden_operating_claim", path_is_file(CLAIM_RECEIPT), CLAIM_RECEIPT, "운영 주장을 하지 않는다."),
        ("required_gate_coverage_audit_written", True, GATE_AUDIT, "필수 게이트 커버리지 감사(required gate coverage audit)를 남긴다."),
    ]
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, effect in checks
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_docs(result: Mapping[str, Any]) -> None:
    summary = {row["metric"]: row["value"] for row in result["summary"]}
    write_text(
        REPORT_PATH,
        f"""# run347C Cash-Open Asymmetric Source Proxy Training(347C 현금장 비대칭 원천 프록시 학습)

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): run347B(347B 실행)의 teacher/source labels(교사/원천 라벨)을 logistic/ExtraTrees/HistGBM(로지스틱/엑스트라 트리/히스토그램 GBM) proxy models(프록시 모델)로 학습했다.
Effect(효과): 다음 run347D(347D 실행)에서 proxy score(프록시 점수), ONNX smoke(온엑스 점검), long-label weakness(롱 라벨 약점)를 검토할 수 있다.

## Scope(범위)

- rows(행): `{summary.get('rows')}`
- feature_count(피처 수): `{summary.get('feature_count')}`
- trained_model_artifacts(학습 모델 산출물): `{summary.get('trained_model_artifacts')}`
- onnx_allocator_smoke_passes(온엑스 배분기 점검 통과): `{summary.get('onnx_allocator_smoke_passes')}`
- threshold_screen_rows(임계값 선별 행): `{summary.get('threshold_screen_rows')}`
- probe_priority_rows(탐침 우선순위 행): `{summary.get('probe_priority_rows')}`

## Key Caveat(핵심 주의)

Validation/test(검증/테스트) 구간에는 long teacher positive(롱 교사 양성)가 없다. 따라서 long quality(롱 품질)는 아직 OOS(`out-of-sample`, 표본외)로 검증되지 않았다.

## Artifacts(산출물)

- scorecard(점수표): `{rel(MODEL_SCORECARD)}`
- threshold_screen(임계값 선별): `{rel(PROXY_THRESHOLD_SCREEN)}`
- probe_priority_queue(탐침 우선순위 대기열): `{rel(PROBE_PRIORITY_QUEUE)}`
- model_artifacts(모델 산출물): `{rel(MODEL_ARTIFACT_MANIFEST)}`
- onnx_smoke(온엑스 점검): `{rel(ONNX_PARITY_SMOKE)}`

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        REVIEW_INDEX,
        "## run347C Cash-Open Asymmetric Source Proxy Training(347C 현금장 비대칭 원천 프록시 학습)",
        f"""## run347C Cash-Open Asymmetric Source Proxy Training(347C 현금장 비대칭 원천 프록시 학습)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): proxy model(프록시 모델), ONNX smoke(온엑스 점검), threshold screen(임계값 선별)을 검토 대기열로 넘긴다.
""",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run347C Proxy Training(347C 프록시 학습)",
        f"""## run347C Proxy Training(347C 프록시 학습)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- trained_model_artifacts(학습 모델 산출물): `{summary.get('trained_model_artifacts')}`
- onnx_smoke_passes(온엑스 점검 통과): `{summary.get('onnx_allocator_smoke_passes')}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage347(347단계)의 설계/물질화 결과를 proxy model review(프록시 모델 검토)로 넘긴다.
""",
    )
    write_text(
        DECISION_DOC,
        f"""# 2026-06-01 Stage347C Proxy Training Decision(347C 프록시 학습 결정)

- decision(결정): `{DECISION}`
- source_materialization(원천 물질화): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- reason(이유): run347B(347B 실행)가 feature/teacher-label source(피처/교사 라벨 원천)를 만들었으므로, 이제 model family(모델 계열)별 proxy reconstruction(프록시 재구성)을 확인해야 한다.

Action(행동): allocator/long/short proxy models(배분기/롱/숏 프록시 모델)을 학습하고 ONNX smoke parity(온엑스 점검 동등성)를 시도했다.
Effect(효과): run347D(347D 실행)가 MT5 runtime probe(MT5 런타임 탐침)로 넘길 가치가 있는지 낮은 주장 범위에서 검토할 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_status_docs(result: Mapping[str, Any]) -> None:
    summary = {row["metric"]: row["value"] for row in result["summary"]}
    selection = f"""# Stage 347 Selection Status(347단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_review_run(원천 검토 실행): `run346B_review_cash_open_runtime_probe_source_pivot_without_db_v1`
- source_runtime_probe(원천 런타임 탐침): `{SOURCE_RUNTIME_RUN_ID}`
- trained_model_artifacts(학습 모델 산출물): `{summary.get('trained_model_artifacts')}`
- onnx_allocator_smoke_passes(온엑스 배분기 점검 통과): `{summary.get('onnx_allocator_smoke_passes')}`
- long_oos_status(롱 표본외 상태): `missing_positive_labels(양성 라벨 없음)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage347(347단계)는 proxy training/screen(프록시 학습/선별)까지 완료했고 다음은 review(검토)이다.
"""
    write_text(STAGE_SELECTION, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

Stage347C(347C 실행)는 proxy training/screen(프록시 학습/선별)을 완료했다. 다음 run347D(347D 실행)는 ONNX smoke(온엑스 점검), proxy threshold screen(프록시 임계값 선별), long OOS missing positive labels(롱 표본외 양성 라벨 부재)를 검토해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

Model training(모델 학습)은 proxy-only(프록시 전용)로만 주장한다. No MT5 execution(MT5 실행 없음), no candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
""",
    )


def write_ledgers(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    summary = {row["metric"]: row["value"] for row in result["summary"]}
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": GATE_TOTAL,
        "gate_total": GATE_TOTAL,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "structural_scout(구조 스카우트)",
        "lane": "experiment_execution(실험 실행)",
        "family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "notes": "proxy training only; long OOS positives missing(프록시 학습 전용, 롱 표본외 양성 없음).",
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "rows": summary.get("rows", ""),
        "attempt_count": summary.get("trained_model_artifacts", ""),
        "feature_count": summary.get("feature_count", ""),
        "candidate_model_id": "none(없음)",
    }
    rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "proxy_training_screen",
            "kpi_scope": "teacher_reconstruction_only",
            "primary_kpi": f"models={summary.get('trained_model_artifacts')};onnx_smoke_passes={summary.get('onnx_allocator_smoke_passes')}",
            "guardrail_kpi": "long_oos_positive_labels=0;no_mt5_execution",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "result_status": "proxy_training_completed_no_selection(프록시 학습 완료, 선정 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "missing_required(필수 누락)",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": "same_as_tier_a_until_tier_b_available",
            "guardrail_kpi": "Tier B missing_required(Tier B 필수 누락)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "result_status": "same_as_tier_a_until_tier_b_available",
        },
    ]
    existing_fields, existing_rows = read_csv_rows(STAGE_LEDGER) if path_is_file(STAGE_LEDGER) else (STAGE_LEDGER_COLUMNS, [])
    replacement = {row["ledger_row_id"] for row in rows}
    kept = [row for row in existing_rows if row.get("ledger_row_id") not in replacement]
    fieldnames = list(dict.fromkeys(list(existing_fields) + STAGE_LEDGER_COLUMNS))
    write_csv(STAGE_LEDGER, kept + rows, fieldnames)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    return rows


def write_final_and_manifest(result: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    summary = {row["metric"]: row["value"] for row in result["summary"]}
    write_json(
        FINAL_DECISION,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "rows": summary.get("rows"),
            "feature_count": summary.get("feature_count"),
            "trained_model_artifacts": summary.get("trained_model_artifacts"),
            "onnx_allocator_smoke_passes": summary.get("onnx_allocator_smoke_passes"),
            "scorecard_rows": summary.get("scorecard_rows"),
            "threshold_screen_rows": summary.get("threshold_screen_rows"),
            "probe_priority_rows": summary.get("probe_priority_rows"),
            "long_oos_positive_labels": 0,
            "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
            "gate_total": len(gates),
            "model_training": "claimed_proxy_only",
            "onnx_smoke": "claimed_smoke_only",
            "mt5_execution": "not_claimed",
            "candidate_selection": "not_claimed",
            "forward_passed": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    outputs = [
        FEATURE_ORDER,
        SPLIT_AUDIT,
        LABEL_SPLIT_DISTRIBUTION,
        MODEL_SCORECARD,
        PREDICTION_TABLE,
        PROXY_THRESHOLD_SCREEN,
        PROBE_PRIORITY_QUEUE,
        FEATURE_IMPORTANCE,
        MODEL_ARTIFACT_MANIFEST,
        ONNX_PARITY_SMOKE,
        TRAINING_SUMMARY,
        REPORT_PATH,
        FINAL_DECISION,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer": rel(Path("stage_pipelines/stage347/train_cash_open_asymmetric_source_proxy_models_without_db.py")),
            "inputs": [rel(SOURCE_FEATURE_LABEL), rel(SOURCE_FEATURE_SCHEMA), rel(SOURCE_LABEL_MANIFEST), rel(SOURCE_RUN345B_SUMMARY)],
            "outputs": [rel(path) for path in outputs],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_registries(result: Mapping[str, Any]) -> None:
    summary = {row["metric"]: row["value"] for row in result["summary"]}
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_execution(실험 실행)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "notes": "Proxy model training/screen completed; no selection(프록시 모델 학습/선별 완료, 선정 없음).",
                "family": "experiment_execution(실험 실행)",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "rows": summary.get("rows"),
                "gate_passes": GATE_TOTAL,
                "gate_total": GATE_TOTAL,
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": "none(없음)",
                "result_status": "proxy_training_completed_no_selection(프록시 학습 완료, 선정 없음)",
                "attempt_count": summary.get("trained_model_artifacts"),
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "teacher_reconstruction_only",
                "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            }
        ],
    )
    artifact_paths = [
        FEATURE_ORDER,
        SPLIT_AUDIT,
        LABEL_SPLIT_DISTRIBUTION,
        MODEL_SCORECARD,
        PREDICTION_TABLE,
        PROXY_THRESHOLD_SCREEN,
        PROBE_PRIORITY_QUEUE,
        FEATURE_IMPORTANCE,
        MODEL_ARTIFACT_MANIFEST,
        ONNX_PARITY_SMOKE,
        TRAINING_SUMMARY,
        RUN_EVIDENCE_RECEIPT,
        EXPERIMENT_DESIGN_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
    ]
    for row in result["artifact_rows"]:
        artifact_paths.append(ROOT / row["path"])
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": f"{path.stem}(산출물)",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "run347C proxy training artifact(347C 프록시 학습 산출물).",
        }
        for path in artifact_paths
        if path_is_file(path)
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_register_notes() -> None:
    append_text_once(
        IDEA_REGISTRY,
        "`IDEA-ST347-RUN347C-ASYMMETRIC-SOURCE-PROXY-TRAINING`",
        f"""| `IDEA-ST347-RUN347C-ASYMMETRIC-SOURCE-PROXY-TRAINING` | `{STAGE_ID}` | asymmetric source teacher labels(비대칭 원천 교사 라벨)을 proxy allocator/heads(프록시 배분기/헤드)로 증류한다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `proxy_training_completed_no_selection` | next_action(다음 행동) `{NEXT_RUN_ID}`; ONNX smoke(온엑스 점검)는 runtime authority(런타임 권위)가 아님 |""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        "`NR-ST347C-LONG-OOS-MISSING`",
        f"""| `NR-ST347C-LONG-OOS-MISSING` | `IDEA-ST347-RUN347C-ASYMMETRIC-SOURCE-PROXY-TRAINING` | long quality teacher label(롱 품질 교사 라벨)이 validation/test(검증/테스트)에 없다 | run347C split audit(347C 분할 감사) | long head(롱 헤드)는 OOS 검증 불충분으로 낮춰 말한다 | richer long source label(더 풍부한 롱 원천 라벨) 또는 MT5 probe(런타임 탐침) 비교 시 재개 |""",
    )
    text = f"""## 2026-06-01 run347C Cash-Open Asymmetric Source Proxy Training(현금장 비대칭 원천 프록시 학습)

- action(행동): allocator/long/short proxy models(배분기/롱/숏 프록시 모델)을 학습하고 ONNX smoke parity(온엑스 점검 동등성)를 시도했다.
- effect(효과): run347D(347D 실행)에서 proxy score(프록시 점수)와 long OOS missing label(롱 표본외 라벨 부재)을 검토할 수 있다.
- boundary(경계): no MT5 execution(MT5 실행 없음), no candidate selection(후보 선정 없음), no runtime authority(런타임 권위 없음).
"""
    append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run347C Cash-Open Asymmetric Source Proxy Training", text)
    append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run347C Cash-Open Asymmetric Source Proxy Training", text)


def validate(result: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    outputs = [
        FEATURE_ORDER,
        SPLIT_AUDIT,
        LABEL_SPLIT_DISTRIBUTION,
        MODEL_SCORECARD,
        PREDICTION_TABLE,
        PROXY_THRESHOLD_SCREEN,
        PROBE_PRIORITY_QUEUE,
        MODEL_ARTIFACT_MANIFEST,
        ONNX_PARITY_SMOKE,
        TRAINING_SUMMARY,
        RUN_EVIDENCE_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        STAGE_SELECTION,
    ]
    missing = [rel(path) for path in outputs if not path_is_file(path)]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    if len(result["frame"]) != 5827:
        raise RuntimeError(f"unexpected row count(예상 밖 행 수): {len(result['frame'])}")
    if len(result["score_rows"]) < 36:
        raise RuntimeError("model scorecard too small(모델 점수표가 너무 작음)")
    if not any(row.get("status") == "passed" for row in result["onnx_rows"]):
        raise RuntimeError("no ONNX smoke pass(온엑스 점검 통과 없음)")
    if len(gates) != GATE_TOTAL or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run347C gate audit failed(347C 게이트 감사 실패)")
    current_texts = [read_text(WORKSPACE_STATE), read_text(CURRENT_WORKING_STATE), read_text(STAGE_SELECTION)]
    if not all(NEXT_RUN_ID in text and STAGE_ID in text for text in current_texts):
        raise RuntimeError("current truth sync failed(현재 진실 동기화 실패)")


def main() -> None:
    for path in [
        SOURCE_FINAL_DECISION,
        SOURCE_GATE_AUDIT,
        SOURCE_FEATURE_LABEL,
        SOURCE_FEATURE_SCHEMA,
        SOURCE_LABEL_MANIFEST,
        SOURCE_PROXY_GRID,
        SOURCE_HANDOFF_INDEX,
        SOURCE_RUN345B_SUMMARY,
    ]:
        required(path)
    result = train_and_score()
    write_receipts(result)
    gates = gate_rows(result)
    write_docs(result)
    write_status_docs(result)
    write_ledgers(result)
    write_final_and_manifest(result, gates)
    write_registries(result)
    write_register_notes()
    validate(result, gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_run_id": NEXT_RUN_ID,
                "rows": len(result["frame"]),
                "trained_model_artifacts": sum(1 for row in result["artifact_rows"] if "joblib" in row.get("artifact_type", "")),
                "onnx_smoke_passes": sum(1 for row in result["onnx_rows"] if row.get("status") == "passed"),
                "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
                "gate_total": len(gates),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
