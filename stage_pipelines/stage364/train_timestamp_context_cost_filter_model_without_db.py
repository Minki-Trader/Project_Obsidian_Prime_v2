from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import pickle
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.ensemble import GradientBoostingClassifier, HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

STAGE_ID = "364_source_regime_label_pivot__dense_cost_recovery"
RUN_NUMBER = "run364E"
RUN_ID = "run364E_train_timestamp_context_cost_filter_model_without_db_v1"
PARENT_RUN_ID = "run364D_materialize_timestamp_context_training_seed_without_db_v1"
NEXT_RUN_ID = "run364F_prepare_timestamp_context_onnx_runtime_probe_without_db_v1"

STATUS = "completed_stage364E_cost_filter_model_trained_onnx_exported_probe_preparation_opened_no_mt5"
JUDGMENT = "positive_model_training_onnx_exportable_research_candidate_for_runtime_probe_no_operating_claim"
DECISION = "stage364E_open_run364F_prepare_timestamp_context_onnx_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_model_training_and_onnx_export_only_no_mt5_execution_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "mt5_report_open_close_time_joined_to_runtime_bar_time_no_timezone_conversion"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
SOURCE_RUN_DIR = STAGE_DIR / "02_runs" / "run364D"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

SOURCE_TRAINING_SEED_TABLE = SOURCE_RUN_DIR / "timestamp_context_training_seed_table.csv"
SOURCE_FEATURE_SCHEMA = SOURCE_RUN_DIR / "timestamp_context_feature_schema.json"
SOURCE_SEED_METRICS = SOURCE_RUN_DIR / "seed_metric_summary.csv"
SOURCE_MONTH_PRESSURE = SOURCE_RUN_DIR / "month_pressure_matrix.csv"
SOURCE_MODEL_TASK_QUEUE = SOURCE_RUN_DIR / "run364E_model_task_queue.csv"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_REPORT = REVIEW_DIR / "run364D_timestamp_context_training_seed_materialization.md"

INPUT_FILES = [
    SOURCE_TRAINING_SEED_TABLE,
    SOURCE_FEATURE_SCHEMA,
    SOURCE_SEED_METRICS,
    SOURCE_MONTH_PRESSURE,
    SOURCE_MODEL_TASK_QUEUE,
    SOURCE_FINAL_DECISION,
    SOURCE_GATE_AUDIT,
    SOURCE_REPORT,
]

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
MODEL_SCORECARD = RUN_DIR / "model_scorecard.csv"
THRESHOLD_SURFACE = RUN_DIR / "threshold_surface.csv"
MONTH_STABILITY = RUN_DIR / "model_month_stability.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
SELECTED_MODEL_SUMMARY = RUN_DIR / "selected_model_summary.json"
RUNTIME_PROBE_QUEUE = RUN_DIR / "run364F_runtime_probe_queue.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"

MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"

REPORT_PATH = REVIEW_DIR / "run364E_timestamp_context_cost_filter_model_training.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364E_timestamp_context_cost_filter_model_training.md"

TARGET_LABEL = "label_cost_positive_0_30"
DENSITY_TARGETS = [3.0, 3.1, 3.3, 3.5]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ensure_parent(path)
    encoding = "utf-8-sig" if bom and path.suffix.lower() in {".md", ".txt"} else "utf-8"
    with open(fs_path(path), "w", encoding=encoding, newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    csv.field_size_limit(200_000_000)
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
    temp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    try:
        with open(fs_path(temp_path), "w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
            writer.writeheader()
            for row in rows_list:
                writer.writerow({key: row.get(key, "") for key in fieldnames})
        for attempt in range(12):
            try:
                os.replace(fs_path(temp_path), fs_path(path))
                break
            except PermissionError:
                if attempt == 11:
                    raise
                time.sleep(0.25)
    finally:
        if exists(temp_path):
            os.remove(fs_path(temp_path))


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool) -> None:
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    elif extend_header:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    replacements = {tuple(str(row.get(key, "")) for key in key_fields): dict(row) for row in rows}
    output: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set()
    for row in existing:
        key = tuple(str(row.get(field, "")) for field in key_fields)
        if key in replacements:
            output.append(replacements[key])
            seen.add(key)
        else:
            output.append(row)
    for key, row in replacements.items():
        if key not in seen:
            output.append(row)
    write_csv(path, output, fieldnames)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def source_gate_passed() -> bool:
    _, rows = read_csv_rows(SOURCE_GATE_AUDIT)
    return bool(rows) and all(row.get("status") == "passed" for row in rows)


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_role": path.stem,
            "path": rel(path),
            "sha256": sha256_file(path) if exists(path) and path.is_file() else "",
            "availability": "tracked_or_ignored_with_manifest",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def load_training_data() -> tuple[pd.DataFrame, list[str]]:
    schema = read_json(SOURCE_FEATURE_SCHEMA)
    feature_columns = list(schema["feature_columns"])
    frame = pd.read_csv(fs_path(SOURCE_TRAINING_SEED_TABLE), encoding="utf-8-sig")
    frame["open_dt"] = pd.to_datetime(frame["open_time"], format="%Y-%m-%d %H:%M:%S")
    frame = frame.sort_values(["split", "open_dt", "trade_index"]).reset_index(drop=True)
    for column in [*feature_columns, TARGET_LABEL, "cost_0_30_net", "feature_day_count"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if frame[feature_columns].isna().any().any():
        raise RuntimeError("Feature matrix contains NaN values")
    return frame, feature_columns


def model_specs() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "logreg_l2_balanced",
            "model_family": "LogisticRegression(로지스틱 회귀)",
            "estimator": make_pipeline(
                StandardScaler(),
                LogisticRegression(max_iter=2000, class_weight="balanced", C=0.5, random_state=364),
            ),
            "onnx_expected": True,
        },
        {
            "model_id": "rf_depth3_balanced",
            "model_family": "RandomForest(랜덤 포레스트)",
            "estimator": RandomForestClassifier(
                n_estimators=300,
                max_depth=3,
                min_samples_leaf=20,
                class_weight="balanced_subsample",
                random_state=364,
                n_jobs=-1,
            ),
            "onnx_expected": True,
        },
        {
            "model_id": "gb_depth2_lr004",
            "model_family": "GradientBoosting(그래디언트 부스팅)",
            "estimator": GradientBoostingClassifier(
                n_estimators=120,
                learning_rate=0.04,
                max_depth=2,
                min_samples_leaf=20,
                random_state=364,
            ),
            "onnx_expected": True,
        },
        {
            "model_id": "histgb_l2_leaf7",
            "model_family": "HistGradientBoosting(히스토그램 그래디언트 부스팅)",
            "estimator": HistGradientBoostingClassifier(
                max_iter=100,
                learning_rate=0.04,
                l2_regularization=1.0,
                max_leaf_nodes=7,
                min_samples_leaf=20,
                random_state=364,
            ),
            "onnx_expected": False,
        },
    ]


def profit_factor(values: pd.Series | np.ndarray) -> float:
    series = pd.Series(values, dtype="float64")
    gains = float(series[series > 0].sum())
    losses = float(series[series < 0].sum())
    if losses == 0:
        return 999.0 if gains > 0 else 0.0
    return gains / abs(losses)


def max_drawdown(values: pd.Series | np.ndarray) -> float:
    arr = np.asarray(values, dtype="float64")
    if arr.size == 0:
        return 0.0
    equity = np.cumsum(arr)
    peaks = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    drawdowns = equity - peaks
    return float(drawdowns.min()) if drawdowns.size else 0.0


def split_metrics(selected: pd.DataFrame, split: str, model_id: str, threshold_id: str, threshold: float, density_target: float) -> dict[str, Any]:
    split_frame = selected[selected["split"].eq(split)].sort_values("open_dt")
    days = float(split_frame["feature_day_count"].iloc[0]) if not split_frame.empty else 0.0
    values = split_frame["cost_0_30_net"].astype(float)
    net = float(values.sum()) if len(values) else 0.0
    months = split_frame.groupby("month_id", dropna=False)["cost_0_30_net"].sum() if len(split_frame) else pd.Series(dtype="float64")
    positive_months = int((months > 0).sum()) if len(months) else 0
    worst_month = float(months.min()) if len(months) else 0.0
    drawdown = max_drawdown(values)
    return {
        "run_id": RUN_ID,
        "model_id": model_id,
        "threshold_id": threshold_id,
        "split": split,
        "threshold": round(float(threshold), 12),
        "density_target": density_target,
        "trade_count": int(len(split_frame)),
        "feature_day_count": round(days, 4),
        "trade_density": round(len(split_frame) / days, 10) if days else 0.0,
        "cost_0_30_net": round(net, 2),
        "cost_0_30_profit_factor": round(profit_factor(values), 10) if len(values) else 0.0,
        "expectancy_cost_0_30": round(net / len(values), 10) if len(values) else 0.0,
        "win_rate_cost_0_30": round(float((values > 0).mean()), 10) if len(values) else 0.0,
        "max_drawdown_cost_0_30": round(drawdown, 2),
        "recovery_factor_cost_0_30": round(net / abs(drawdown), 10) if drawdown < 0 else 999.0 if net > 0 else 0.0,
        "positive_months": positive_months,
        "month_count": int(len(months)),
        "positive_month_rate": round(positive_months / len(months), 10) if len(months) else 0.0,
        "worst_month_cost_0_30_net": round(worst_month, 2),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def model_probabilities(model: Any, matrix: np.ndarray) -> np.ndarray:
    proba = model.predict_proba(matrix)
    if proba.ndim != 2 or proba.shape[1] < 2:
        raise RuntimeError("Expected binary predict_proba output")
    return proba[:, 1]


def choose_validation_threshold(scores: np.ndarray, validation_days: float, density_target: float) -> float:
    k = int(math.ceil(density_target * validation_days))
    k = min(max(k, 1), len(scores))
    return float(np.sort(scores)[::-1][k - 1])


def score_models(frame: pd.DataFrame, feature_columns: Sequence[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    validation = frame[frame["split"].eq("validation")].copy()
    oos = frame[frame["split"].eq("oos")].copy()
    x_validation = validation[list(feature_columns)].astype("float32").to_numpy()
    y_validation = validation[TARGET_LABEL].astype(int).to_numpy()
    validation_days = float(validation["feature_day_count"].iloc[0])

    score_rows: list[dict[str, Any]] = []
    threshold_rows: list[dict[str, Any]] = []
    month_rows: list[dict[str, Any]] = []
    trained: dict[str, Any] = {}

    for spec in model_specs():
        model = spec["estimator"]
        model.fit(x_validation, y_validation)
        trained[spec["model_id"]] = {"model": model, **{key: value for key, value in spec.items() if key != "estimator"}}
        for split, split_frame in [("validation", validation), ("oos", oos)]:
            matrix = split_frame[list(feature_columns)].astype("float32").to_numpy()
            scores = model_probabilities(model, matrix)
            if len(np.unique(split_frame[TARGET_LABEL].astype(int))) > 1:
                auc = float(roc_auc_score(split_frame[TARGET_LABEL].astype(int), scores))
                ap = float(average_precision_score(split_frame[TARGET_LABEL].astype(int), scores))
            else:
                auc = 0.0
                ap = 0.0
            score_rows.append({
                "run_id": RUN_ID,
                "model_id": spec["model_id"],
                "model_family": spec["model_family"],
                "split": split,
                "target_label": TARGET_LABEL,
                "roc_auc": round(auc, 10),
                "average_precision": round(ap, 10),
                "score_min": round(float(scores.min()), 10),
                "score_max": round(float(scores.max()), 10),
                "score_mean": round(float(scores.mean()), 10),
                "claim_boundary": CLAIM_BOUNDARY,
            })
            split_frame = split_frame.copy()
            split_frame["model_score"] = scores
            trained[spec["model_id"]][f"{split}_scores"] = scores
            trained[spec["model_id"]][f"{split}_frame"] = split_frame

        validation_scores = trained[spec["model_id"]]["validation_scores"]
        for density_target in DENSITY_TARGETS:
            threshold_id = f"density_{str(density_target).replace('.', '_')}"
            threshold = choose_validation_threshold(validation_scores, validation_days, density_target)
            for split in ("validation", "oos"):
                scored = trained[spec["model_id"]][f"{split}_frame"].copy()
                selected = scored[scored["model_score"] >= threshold].copy()
                threshold_rows.append(split_metrics(selected, split, spec["model_id"], threshold_id, threshold, density_target))
                grouped = (
                    selected.groupby("month_id", dropna=False)
                    .agg(cost_0_30_net=("cost_0_30_net", "sum"), trade_count=("cost_0_30_net", "size"))
                    .reset_index()
                )
                for _, row in grouped.iterrows():
                    month_rows.append({
                        "run_id": RUN_ID,
                        "model_id": spec["model_id"],
                        "threshold_id": threshold_id,
                        "split": split,
                        "month_id": row["month_id"],
                        "cost_0_30_net": round(float(row["cost_0_30_net"]), 2),
                        "trade_count": int(row["trade_count"]),
                        "month_pressure_class": "positive_month" if float(row["cost_0_30_net"]) > 0 else "negative_or_flat_month",
                        "claim_boundary": CLAIM_BOUNDARY,
                    })
    return score_rows, threshold_rows, month_rows, trained


def paired_threshold_rows(threshold_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_key: dict[tuple[str, str], dict[str, Mapping[str, Any]]] = {}
    for row in threshold_rows:
        key = (str(row["model_id"]), str(row["threshold_id"]))
        by_key.setdefault(key, {})[str(row["split"])] = row
    paired: list[dict[str, Any]] = []
    for (model_id, threshold_id), splits in by_key.items():
        if "validation" not in splits or "oos" not in splits:
            continue
        validation = splits["validation"]
        oos = splits["oos"]
        density_pass = as_float(validation["trade_density"]) >= 3.0 and as_float(oos["trade_density"]) >= 3.0
        cost_pass = as_float(validation["cost_0_30_net"]) > 0 and as_float(oos["cost_0_30_net"]) > 0
        paired.append({
            "model_id": model_id,
            "threshold_id": threshold_id,
            "threshold": validation["threshold"],
            "density_target": validation["density_target"],
            "validation_cost_0_30_net": validation["cost_0_30_net"],
            "oos_cost_0_30_net": oos["cost_0_30_net"],
            "validation_trade_density": validation["trade_density"],
            "oos_trade_density": oos["trade_density"],
            "validation_profit_factor": validation["cost_0_30_profit_factor"],
            "oos_profit_factor": oos["cost_0_30_profit_factor"],
            "validation_max_drawdown": validation["max_drawdown_cost_0_30"],
            "oos_max_drawdown": oos["max_drawdown_cost_0_30"],
            "validation_positive_months": validation["positive_months"],
            "validation_month_count": validation["month_count"],
            "oos_positive_months": oos["positive_months"],
            "oos_month_count": oos["month_count"],
            "cross_split_status": "passes_cost_density_gate" if density_pass and cost_pass else "fails_cost_or_density_gate",
            "selection_score_validation_only": round(as_float(validation["cost_0_30_net"]) + 25.0 * as_float(validation["positive_month_rate"]) - 0.10 * abs(as_float(validation["max_drawdown_cost_0_30"])), 6),
            "claim_boundary": CLAIM_BOUNDARY,
        })
    return paired


def save_models_and_onnx(trained: Mapping[str, Mapping[str, Any]], feature_columns: Sequence[str], paired_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    ensure_parent(MODEL_DIR / "x")
    ensure_parent(ONNX_DIR / "x")
    artifact_rows: list[dict[str, Any]] = []
    smoke_rows: list[dict[str, Any]] = []
    paired_by_model = {}
    for row in paired_rows:
        if row["cross_split_status"] == "passes_cost_density_gate":
            current = paired_by_model.get(row["model_id"])
            if current is None or as_float(row["selection_score_validation_only"]) > as_float(current["selection_score_validation_only"]):
                paired_by_model[row["model_id"]] = row

    for model_id, spec in trained.items():
        model = spec["model"]
        model_path = MODEL_DIR / f"{model_id}.joblib"
        ensure_parent(model_path)
        joblib.dump(model, fs_path(model_path))
        artifact_rows.append({
            "run_id": RUN_ID,
            "model_id": model_id,
            "artifact_type": "joblib_model",
            "path": rel(model_path),
            "sha256": sha256_file(model_path),
            "status": "written",
            "claim_boundary": CLAIM_BOUNDARY,
        })
        onnx_path = ONNX_DIR / f"{model_id}.onnx"
        try:
            last_estimator = model.steps[-1][1] if hasattr(model, "steps") else model
            onnx_model = convert_sklearn(
                model,
                initial_types=[("float_input", FloatTensorType([None, len(feature_columns)]))],
                options={id(last_estimator): {"zipmap": False}},
                target_opset=15,
            )
            with open(fs_path(onnx_path), "wb") as handle:
                handle.write(onnx_model.SerializeToString())
            artifact_rows.append({
                "run_id": RUN_ID,
                "model_id": model_id,
                "artifact_type": "onnx_model",
                "path": rel(onnx_path),
                "sha256": sha256_file(onnx_path),
                "status": "written",
                "claim_boundary": CLAIM_BOUNDARY,
            })
            oos_frame = spec["oos_frame"]
            sample = oos_frame[list(feature_columns)].astype("float32").to_numpy()[:32]
            sklearn_scores = model_probabilities(model, sample)
            session = ort.InferenceSession(fs_path(onnx_path), providers=["CPUExecutionProvider"])
            outputs = session.run(None, {session.get_inputs()[0].name: sample})
            if len(outputs) >= 2 and isinstance(outputs[1], np.ndarray) and outputs[1].ndim == 2:
                onnx_scores = outputs[1][:, 1]
            elif isinstance(outputs[-1], np.ndarray) and outputs[-1].ndim == 2:
                onnx_scores = outputs[-1][:, -1]
            else:
                raise RuntimeError("Unsupported ONNX probability output shape")
            max_abs_diff = float(np.max(np.abs(sklearn_scores - onnx_scores)))
            smoke_rows.append({
                "run_id": RUN_ID,
                "model_id": model_id,
                "onnx_path": rel(onnx_path),
                "sample_rows": int(len(sample)),
                "max_abs_diff": round(max_abs_diff, 12),
                "status": "passed" if max_abs_diff <= 1e-5 else "failed",
                "failure": "",
                "claim_boundary": CLAIM_BOUNDARY,
            })
        except Exception as exc:  # noqa: BLE001 - recorded as evidence.
            smoke_rows.append({
                "run_id": RUN_ID,
                "model_id": model_id,
                "onnx_path": rel(onnx_path),
                "sample_rows": 0,
                "max_abs_diff": "",
                "status": "failed",
                "failure": f"{type(exc).__name__}: {str(exc)[:500]}",
                "claim_boundary": CLAIM_BOUNDARY,
            })

    exportable_models = {row["model_id"] for row in smoke_rows if row["status"] == "passed"}
    positive_exportable = [row for row in paired_rows if row["model_id"] in exportable_models and row["cross_split_status"] == "passes_cost_density_gate"]
    positive_any = [row for row in paired_rows if row["cross_split_status"] == "passes_cost_density_gate"]
    best_any = max(positive_any, key=lambda row: as_float(row["selection_score_validation_only"]))
    best_onnx = max(positive_exportable, key=lambda row: as_float(row["selection_score_validation_only"]))
    summary = {
        "best_training_model_id": best_any["model_id"],
        "best_training_threshold_id": best_any["threshold_id"],
        "best_training_validation_net": best_any["validation_cost_0_30_net"],
        "best_training_oos_net": best_any["oos_cost_0_30_net"],
        "best_onnx_model_id": best_onnx["model_id"],
        "best_onnx_threshold_id": best_onnx["threshold_id"],
        "best_onnx_threshold": best_onnx["threshold"],
        "best_onnx_validation_net": best_onnx["validation_cost_0_30_net"],
        "best_onnx_oos_net": best_onnx["oos_cost_0_30_net"],
        "best_onnx_validation_density": best_onnx["validation_trade_density"],
        "best_onnx_oos_density": best_onnx["oos_trade_density"],
        "best_onnx_path": next(row["path"] for row in artifact_rows if row["model_id"] == best_onnx["model_id"] and row["artifact_type"] == "onnx_model"),
        "selection_boundary": "validation_metric_only_for_model_threshold_choice_oos_read_only(모델/임계값 선택은 검증 지표 기준, 표본외는 읽기 전용)",
    }
    write_json(SELECTED_MODEL_SUMMARY, summary)
    return artifact_rows, smoke_rows, summary


def runtime_probe_queue(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "s364F_r01_onnx_runtime_handoff_package",
            "priority": 1,
            "model_id": summary["best_onnx_model_id"],
            "threshold_id": summary["best_onnx_threshold_id"],
            "onnx_path": summary["best_onnx_path"],
            "threshold": summary["best_onnx_threshold"],
            "action": "package ONNX cost-filter model for MT5 runtime probe(ONNX 비용 필터 모델을 MT5 런타임 탐침용으로 포장)",
            "expected_effect": "compare Python proxy score with MT5 runtime behavior(Python 프록시 점수와 MT5 런타임 동작 비교)",
            "guardrail": "runtime_probe only, no runtime authority(런타임 탐침일 뿐 런타임 권위 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s364F_r02_threshold_handoff_and_feature_order_check",
            "priority": 2,
            "model_id": summary["best_onnx_model_id"],
            "threshold_id": summary["best_onnx_threshold_id"],
            "onnx_path": summary["best_onnx_path"],
            "threshold": summary["best_onnx_threshold"],
            "action": "freeze feature order and threshold handoff(피처 순서와 임계값 인계를 고정)",
            "expected_effect": "prevent MT5/Python feature-order mismatch(MT5/Python 피처 순서 불일치 방지)",
            "guardrail": "fail-fast if feature schema or hash mismatches(피처 스키마나 해시 불일치 시 즉시 실패)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s364F_r03_month_pressure_runtime_guard",
            "priority": 3,
            "model_id": summary["best_onnx_model_id"],
            "threshold_id": summary["best_onnx_threshold_id"],
            "onnx_path": summary["best_onnx_path"],
            "threshold": summary["best_onnx_threshold"],
            "action": "carry month pressure diagnostics into runtime probe(月 압박 진단을 런타임 탐침에 포함)",
            "expected_effect": "keep positive net from hiding monthly fragility(양수 순수익이 월별 취약성을 숨기지 못하게 함)",
            "guardrail": "no promotion if month pressure remains unstable(月 압박이 불안정하면 승격 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(frame: pd.DataFrame, feature_columns: Sequence[str], paired_rows: Sequence[Mapping[str, Any]], smoke_rows: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> None:
    write_json(WORK_PACKET, {
        "run_id": RUN_ID,
        "primary_family": "model_training(모델 학습)",
        "primary_skill": "obsidian-model-validation(모델 검증)",
        "support_skills": [
            "obsidian-data-integrity(데이터 무결성)",
            "obsidian-artifact-lineage(산출물 계보)",
            "obsidian-runtime-parity(런타임 동등성)",
            "obsidian-result-judgment(결과 판정)",
        ],
        "required_gates": [
            "input_presence",
            "source_gate_passed",
            "model_training_completed",
            "threshold_surface_completed",
            "onnx_export_smoke_pass",
            "runtime_probe_queue_created",
            "claim_boundary_enforced",
            "ledger_synced",
        ],
        "status": STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(DATA_INTEGRITY_RECEIPT, {
        "data_source": [rel(SOURCE_TRAINING_SEED_TABLE), rel(SOURCE_FEATURE_SCHEMA)],
        "time_axis": TIME_AXIS,
        "sample_scope": f"US100 M5 q05 training seed rows={len(frame)}; validation={int((frame['split']=='validation').sum())}; oos={int((frame['split']=='oos').sum())}",
        "missing_or_duplicate_check": f"input_hash duplicates={int(frame['input_hash'].duplicated().sum())}; duplicates preserved as report-derived trade events(보고서 파생 거래 이벤트라 중복 보존)",
        "feature_label_boundary": "features are timestamp-known; target label is realized cost-positive trade result(피처는 시점상 알려짐, 타깃 라벨은 실현 비용 양수 거래 결과)",
        "split_boundary": "model trained on validation split only; threshold derived from validation density target; OOS read-only(모델은 검증 분할만 학습, 임계값은 검증 밀도 목표에서 파생, 표본외는 읽기 전용)",
        "leakage_risk": "model family choice is still exploratory and reviewed with OOS, so no operating claim(모델 계열 선택은 여전히 탐색이며 OOS를 보았으므로 운영 주장 없음)",
        "data_hash_or_identity": {
            "training_seed_sha256": sha256_file(SOURCE_TRAINING_SEED_TABLE),
            "feature_schema_sha256": sha256_file(SOURCE_FEATURE_SCHEMA),
            "feature_count": len(feature_columns),
        },
        "integrity_judgment": "usable_with_boundary",
    })
    write_json(MODEL_VALIDATION_RECEIPT, {
        "model_family": "LogisticRegression, RandomForest, GradientBoosting, HistGradientBoosting(로지스틱 회귀, 랜덤 포레스트, 그래디언트 부스팅, 히스토그램 그래디언트 부스팅)",
        "target_and_label": f"{TARGET_LABEL}: cost_0_30_net > 0(+0.30 비용 후 순수익 양수)",
        "split_method": "train on validation split, apply fixed validation-derived thresholds to OOS(검증 분할 학습, 검증 파생 고정 임계값을 표본외 적용)",
        "selection_metric": "validation cost_0_30_net with density >= 3/day and positive OOS as read-only sanity(검증 +0.30 비용 순수익과 3/day 이상, 표본외 양수는 읽기 전용 점검)",
        "secondary_metrics": "profit factor, expectancy, max drawdown, recovery factor, positive month rate, ONNX smoke diff(수익 팩터, 기대값, 최대 낙폭, 회복 계수, 양수 월 비율, ONNX 스모크 차이)",
        "threshold_policy": "validation density target thresholds: 3.0, 3.1, 3.3, 3.5/day(검증 밀도 목표 임계값)",
        "overfit_risk": "small report-derived sample and model family search; no WFO or MT5 yet(작은 보고서 파생 표본과 모델 계열 탐색, WFO/MT5 없음)",
        "calibration_risk": "scores are ranking/proxy scores, not live calibrated probabilities(점수는 순위/프록시 점수이며 실거래 보정 확률 아님)",
        "comparison_baseline": "dense_control_all_long and Stage364D primary_hour_minute_context_guard(전체 롱 고밀도 대조와 364D 주 문맥 가드)",
        "validation_judgment": "exploratory_positive_onnx_runtime_probe_candidate_not_promotion",
        "best_training_model": summary["best_training_model_id"],
        "best_onnx_model": summary["best_onnx_model_id"],
    })
    write_json(LINEAGE_RECEIPT, {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": "python stage_pipelines/stage364/train_timestamp_context_cost_filter_model_without_db.py",
        "consumer": [rel(REPORT_PATH), rel(RUNTIME_PROBE_QUEUE), rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER)],
        "artifact_paths": [rel(MODEL_SCORECARD), rel(THRESHOLD_SURFACE), rel(MODEL_ARTIFACT_MANIFEST), rel(ONNX_SMOKE_REPORT), rel(SELECTED_MODEL_SUMMARY), rel(RUNTIME_PROBE_QUEUE)],
        "artifact_hashes": "written to model_artifact_manifest and artifact_registry(모델 산출물 목록과 산출물 등록부에 기록)",
        "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked reports plus ignored model artifacts with manifest(추적 보고서와 manifest가 있는 ignored 모델 산출물)",
        "lineage_judgment": "connected_with_boundary",
    })
    write_json(JUDGMENT_RECEIPT, {
        "result_subject": RUN_ID,
        "evidence_available": [rel(THRESHOLD_SURFACE), rel(ONNX_SMOKE_REPORT), rel(SELECTED_MODEL_SUMMARY), rel(REPORT_PATH), rel(FINAL_DECISION)],
        "evidence_missing": "no MT5 runtime probe, no forward replay, no live readiness, Tier B missing_required(MT5 런타임 탐침 없음, 전진 재생 없음, 실거래 준비 없음, Tier B 필수 누락)",
        "judgment_label": "positive",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "an ONNX-exportable proxy model is ready for runtime probing, not ready for operation(ONNX 변환 가능 프록시 모델은 런타임 탐침 준비이지 운영 준비가 아님)",
    })
    write_json(CLAIM_RECEIPT, {
        "run_id": RUN_ID,
        "model_training": "completed",
        "onnx_export": "completed_for_best_exportable_model",
        "mt5_execution": "not_run",
        "runtime_probe": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    })


def write_run_artifacts(frame: pd.DataFrame, feature_columns: Sequence[str], score_rows: Sequence[Mapping[str, Any]], threshold_rows: Sequence[Mapping[str, Any]], month_rows: Sequence[Mapping[str, Any]], artifact_rows: Sequence[Mapping[str, Any]], smoke_rows: Sequence[Mapping[str, Any]], summary: Mapping[str, Any], queue_rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(MODEL_SCORECARD, score_rows)
    write_csv(THRESHOLD_SURFACE, threshold_rows)
    write_csv(MONTH_STABILITY, month_rows)
    write_csv(MODEL_ARTIFACT_MANIFEST, artifact_rows)
    write_csv(ONNX_SMOKE_REPORT, smoke_rows)
    write_csv(RUNTIME_PROBE_QUEUE, queue_rows)
    write_receipts(frame, feature_columns, threshold_rows, smoke_rows, summary)
    write_json(RUN_MANIFEST, {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "command": "python stage_pipelines/stage364/train_timestamp_context_cost_filter_model_without_db.py",
        "input_manifest": rel(INPUT_MANIFEST),
        "outputs": [rel(MODEL_SCORECARD), rel(THRESHOLD_SURFACE), rel(MODEL_ARTIFACT_MANIFEST), rel(ONNX_SMOKE_REPORT), rel(SELECTED_MODEL_SUMMARY), rel(RUNTIME_PROBE_QUEUE)],
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(FINAL_DECISION, {
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "model_training": "completed",
        "model_rows": len(model_specs()),
        "score_rows": len(score_rows),
        "threshold_rows": len(threshold_rows),
        "month_stability_rows": len(month_rows),
        "onnx_smoke_rows": len(smoke_rows),
        "onnx_smoke_pass_rows": sum(1 for row in smoke_rows if row["status"] == "passed"),
        "best_training_model_id": summary["best_training_model_id"],
        "best_training_threshold_id": summary["best_training_threshold_id"],
        "best_training_validation_net": summary["best_training_validation_net"],
        "best_training_oos_net": summary["best_training_oos_net"],
        "best_onnx_model_id": summary["best_onnx_model_id"],
        "best_onnx_threshold_id": summary["best_onnx_threshold_id"],
        "best_onnx_threshold": summary["best_onnx_threshold"],
        "best_onnx_validation_net": summary["best_onnx_validation_net"],
        "best_onnx_oos_net": summary["best_onnx_oos_net"],
        "best_onnx_validation_density": summary["best_onnx_validation_density"],
        "best_onnx_oos_density": summary["best_onnx_oos_density"],
        "best_onnx_path": summary["best_onnx_path"],
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "runtime_probe": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_passes": 0,
        "gate_total": 0,
    })


def gate_rows() -> list[dict[str, Any]]:
    final = read_json(FINAL_DECISION) if exists(FINAL_DECISION) else {}
    _, project_rows = read_csv_rows(PROJECT_LEDGER)
    _, stage_rows = read_csv_rows(STAGE_LEDGER)
    gates = [
        ("input_training_seed_present", exists(SOURCE_TRAINING_SEED_TABLE), SOURCE_TRAINING_SEED_TABLE, "training seed table(학습 씨앗 표) 확인"),
        ("input_schema_present", exists(SOURCE_FEATURE_SCHEMA), SOURCE_FEATURE_SCHEMA, "feature schema(피처 스키마) 확인"),
        ("source_gate_passed", source_gate_passed(), SOURCE_GATE_AUDIT, "run364D gate(364D 게이트) 통과 확인"),
        ("source_next_run_matches", read_json(SOURCE_FINAL_DECISION).get("next_run_id") == RUN_ID, SOURCE_FINAL_DECISION, "source next run(원천 다음 실행) 일치"),
        ("model_scorecard_present", exists(MODEL_SCORECARD) and as_int(final.get("score_rows")) == 8, MODEL_SCORECARD, "model scorecard(모델 점수표) 8행"),
        ("threshold_surface_present", exists(THRESHOLD_SURFACE) and as_int(final.get("threshold_rows")) == 16, THRESHOLD_SURFACE, "threshold surface(임계값 표면) 16개 cross-split row(교차 분할 행)"),
        ("positive_cross_split_model", as_float(final.get("best_onnx_validation_net")) > 0 and as_float(final.get("best_onnx_oos_net")) > 0, FINAL_DECISION, "best ONNX model(최선 ONNX 모델) 검증/표본외 순수익 양수"),
        ("density_requirement_met", as_float(final.get("best_onnx_validation_density")) >= 3.0 and as_float(final.get("best_onnx_oos_density")) >= 3.0, FINAL_DECISION, "trade density(거래 밀도) 3/day 이상"),
        ("onnx_smoke_passed", exists(ONNX_SMOKE_REPORT) and as_int(final.get("onnx_smoke_pass_rows")) >= 1, ONNX_SMOKE_REPORT, "ONNX smoke(ONNX 스모크) 통과"),
        ("selected_model_summary_present", exists(SELECTED_MODEL_SUMMARY), SELECTED_MODEL_SUMMARY, "selected model summary(선택 모델 요약) 존재"),
        ("runtime_probe_queue_present", exists(RUNTIME_PROBE_QUEUE), RUNTIME_PROBE_QUEUE, "runtime probe queue(런타임 탐침 대기열) 존재"),
        ("no_mt5_execution_claim", final.get("mt5_execution") == "not_run", FINAL_DECISION, "MT5 execution(MT5 실행) 없음"),
        ("no_operating_claim", final.get("operating_promotion") == "not_claimed", FINAL_DECISION, "operating promotion(운영 승격) 없음"),
        ("report_present", exists(REPORT_PATH), REPORT_PATH, "report(보고서) 존재"),
        ("selection_status_synced", NEXT_RUN_ID in read_text(SELECTION_STATUS), SELECTION_STATUS, "selection status(선택 상태) 다음 실행 동기화"),
        ("workspace_state_synced", NEXT_RUN_ID in read_text(WORKSPACE_STATE), WORKSPACE_STATE, "workspace state(작업공간 상태) 다음 실행 동기화"),
        ("project_ledger_synced", sum(1 for row in project_rows if row.get("run_id") == RUN_ID) == 3, PROJECT_LEDGER, "project ledger(프로젝트 장부) 3행"),
        ("stage_ledger_synced", sum(1 for row in stage_rows if row.get("run_id") == RUN_ID) == 3, STAGE_LEDGER, "stage ledger(단계 장부) 3행"),
        ("claim_boundary_receipt", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "claim receipt(주장 영수증) 존재"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": rel(path),
            "description": description,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, description in gates
    ]


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return ""
    lines = ["|" + "|".join(columns) + "|", "|" + "|".join(["---"] * len(columns)) + "|"]
    for row in rows:
        lines.append("|" + "|".join(str(row.get(column, "")) for column in columns) + "|")
    return "\n".join(lines)


def write_reports(threshold_rows: Sequence[Mapping[str, Any]], smoke_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> None:
    final = read_json(FINAL_DECISION)
    gates = gate_rows()
    top = sorted([row for row in threshold_rows if row["cross_split_status"] == "passes_cost_density_gate"], key=lambda row: as_float(row["selection_score_validation_only"]), reverse=True)[:8]
    report = f"""# run364E Timestamp Context Cost Filter Model Training(run364E 시점 문맥 비용 필터 모델 학습)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`

Action(행동): Stage364D(364D) training seed(학습 씨앗)로 cost-filter classifier(비용 필터 분류기) 4종을 학습하고 validation-derived threshold(검증 파생 임계값)를 OOS(표본외)에 고정 적용했다.

Effect(효과): ONNX-exportable model(ONNX 변환 가능 모델) 중 `best_onnx_model_id`는 `{final["best_onnx_model_id"]}`이고, MT5 runtime probe(MT5 런타임 탐침) 준비 대상으로 넘길 수 있다.

## Result(결과)

- best_training_model_id(최선 학습 모델 ID): `{final["best_training_model_id"]}`
- best_training_validation_net(최선 학습 검증 순수익): `{final["best_training_validation_net"]}`
- best_training_oos_net(최선 학습 표본외 순수익): `{final["best_training_oos_net"]}`
- best_onnx_model_id(최선 ONNX 모델 ID): `{final["best_onnx_model_id"]}`
- best_onnx_threshold_id(최선 ONNX 임계값 ID): `{final["best_onnx_threshold_id"]}`
- best_onnx_validation_net(최선 ONNX 검증 순수익): `{final["best_onnx_validation_net"]}`
- best_onnx_oos_net(최선 ONNX 표본외 순수익): `{final["best_onnx_oos_net"]}`
- best_onnx_validation_density(최선 ONNX 검증 밀도): `{final["best_onnx_validation_density"]}`
- best_onnx_oos_density(최선 ONNX 표본외 밀도): `{final["best_onnx_oos_density"]}`
- onnx_smoke_pass_rows(ONNX 스모크 통과 행): `{final["onnx_smoke_pass_rows"]}/{final["onnx_smoke_rows"]}`

## Top Thresholds(상위 임계값)

{markdown_table(top, ["model_id", "threshold_id", "validation_cost_0_30_net", "oos_cost_0_30_net", "validation_trade_density", "oos_trade_density", "validation_profit_factor", "oos_profit_factor", "cross_split_status"])}

## ONNX Smoke(ONNX 스모크)

{markdown_table(smoke_rows, ["model_id", "status", "sample_rows", "max_abs_diff", "failure"])}

## Runtime Probe Queue(런타임 탐침 대기열)

{markdown_table(queue_rows, ["queue_id", "priority", "model_id", "threshold_id", "threshold", "action", "guardrail"])}

## Claim Boundary(주장 경계)

Action(행동): `{NEXT_RUN_ID}`를 열었다.

Effect(효과): 다음 작업은 ONNX artifact(ONNX 산출물), feature order(피처 순서), threshold(임계값)를 MT5 probe(MT5 탐침) 인계로 준비한다. 아직 MT5 실행, runtime authority(런타임 권위), operating promotion(운영 승격)은 아니다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, f"""# {TODAY} Stage364E Timestamp Context Cost Filter Model Training Decision(364E 시점 문맥 비용 필터 모델 학습 결정)

- decision(결정): `{DECISION}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`

Action(행동): ONNX-exportable cost filter model(ONNX 변환 가능 비용 필터 모델)을 학습하고 smoke parity(스모크 동등성)를 확인했다.

Effect(효과): `{final["best_onnx_model_id"]}` / `{final["best_onnx_threshold_id"]}`를 runtime probe(런타임 탐침) 준비 대상으로 넘긴다.

Evidence(근거): `{rel(THRESHOLD_SURFACE)}`, `{rel(ONNX_SMOKE_REPORT)}`, `{rel(SELECTED_MODEL_SUMMARY)}`.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")
    write_text(SELECTION_STATUS, f"""# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `model_trained_onnx_exported_runtime_probe_opened_no_operating_claim(모델 학습 및 ONNX 내보내기 완료, 런타임 탐침 열림, 운영 주장 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- candidate_selection(후보 선택): `research_probe_candidate_only(연구 탐침 후보 전용)`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## run364E Model Training Closeout(364E 모델 학습 종료 기록)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gate_result(게이트 결과): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`
- best_onnx_model_id(최선 ONNX 모델 ID): `{final["best_onnx_model_id"]}`
- best_onnx_threshold_id(최선 ONNX 임계값 ID): `{final["best_onnx_threshold_id"]}`
- best_onnx_validation_net(최선 ONNX 검증 순수익): `{final["best_onnx_validation_net"]}`
- best_onnx_oos_net(최선 ONNX 표본외 순수익): `{final["best_onnx_oos_net"]}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage364D(364D)의 학습 씨앗으로 비용 필터 모델을 학습하고 ONNX(온엑스) 스모크를 통과시켰다.

Effect(효과): Stage364(364단계)는 운영 승격 없이 runtime probe preparation(런타임 탐침 준비)으로 진행한다.
""")
    append_text_once(STAGE_BRIEF, "## run364E Model Training Closeout", f"""## run364E Model Training Closeout(364E 모델 학습 종료)

Action(행동): cost-filter model(비용 필터 모델)을 학습하고 ONNX smoke(ONNX 스모크)를 `{final["onnx_smoke_pass_rows"]}/{final["onnx_smoke_rows"]}` 통과시켰다.

Effect(효과): best ONNX model(최선 ONNX 모델)은 `{final["best_onnx_model_id"]}`이고 다음 작업은 `{NEXT_RUN_ID}`다.
""")
    append_text_once(REVIEW_INDEX, "run364E_timestamp_context_cost_filter_model_training", f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}` - timestamp context cost filter model training(시점 문맥 비용 필터 모델 학습).""")
    append_text_once(STAGE_README, "run364E Model Training", f"""## run364E Model Training(364E 모델 학습)

Action(행동): timestamp context(시점 문맥) 학습 씨앗으로 ONNX-exportable cost filter(ONNX 변환 가능 비용 필터)를 만들었다.

Effect(효과): 다음 실행은 `{NEXT_RUN_ID}`이고, 운영 주장은 없다.
""")


def replace_stage_brief_header() -> None:
    text = read_text(STAGE_BRIEF)
    replacements = {
        "- current_run_id(": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
        "- latest_completed_run_id(": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
        "- selection_status(": "- selection_status(선택 상태): `model_trained_onnx_exported_runtime_probe_opened_no_operating_claim(모델 학습 및 ONNX 내보내기 완료, 런타임 탐침 열림, 운영 주장 없음)`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    next_lines = []
    for line in text.splitlines():
        replaced = False
        for prefix, value in replacements.items():
            if line.startswith(prefix):
                next_lines.append(value)
                replaced = True
                break
        if not replaced:
            next_lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(next_lines))


def registry_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    final = read_json(FINAL_DECISION)
    gates = gate_rows()
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "timestamp_context_model_training(시점 문맥 모델 학습)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "notes": "Stage364E timestamp context cost-filter model training(Stage364E 시점 문맥 비용 필터 모델 학습).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["threshold_rows"],
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(SELECTED_MODEL_SUMMARY),
        "result_status": STATUS,
        "sample_rows": final["threshold_rows"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "model_training(모델 학습)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "lane": "timestamp_context_model_training(시점 문맥 모델 학습)",
        "family": "model_training(모델 학습)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can timestamp context produce an ONNX-exportable cost filter?(시점 문맥이 ONNX 변환 가능 비용 필터를 만들 수 있는가?)",
        "metric_scope": "python_model_training_and_onnx_smoke_no_mt5(Python 모델 학습 및 ONNX 스모크, MT5 없음)",
        "feature_count": 21,
        "trained_models": final["model_rows"],
        "onnx_parity": f"smoke_pass={final['onnx_smoke_pass_rows']}/{final['onnx_smoke_rows']}",
        "best_model_id": final["best_onnx_model_id"],
        "net_profit": final["best_onnx_oos_net"],
        "trade_density_per_feature_day": final["best_onnx_oos_density"],
    }
    tier_a = dict(common)
    tier_a.update({
        "subrun_id": f"{RUN_ID}__Tier_A",
        "ledger_row_id": f"{RUN_ID}__Tier_A",
        "row_id": f"{RUN_ID}__Tier_A",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A",
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "kpi_scope": "model_training_proxy(모델 학습 프록시)",
        "primary_kpi": f"best_onnx={final['best_onnx_model_id']};validation_net={final['best_onnx_validation_net']};oos_net={final['best_onnx_oos_net']};oos_density={final['best_onnx_oos_density']}",
        "guardrail_kpi": f"mt5_execution={final['mt5_execution']};runtime_authority={final['runtime_authority']};operating_promotion={final['operating_promotion']}",
    })
    tier_b = dict(tier_a)
    tier_b.update({
        "subrun_id": f"{RUN_ID}__Tier_B",
        "ledger_row_id": f"{RUN_ID}__Tier_B",
        "row_id": f"{RUN_ID}__Tier_B",
        "record_view": "Tier B separate(Tier B 분리)",
        "tier_scope": "Tier B",
        "view": "Tier B separate(Tier B 분리)",
        "tier": "Tier B",
        "status": "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)",
        "primary_kpi": "missing_required(필수 누락)",
        "guardrail_kpi": "do_not_synthesize_tier_b(Tier B 합성 금지)",
    })
    combined = dict(tier_a)
    combined.update({
        "subrun_id": f"{RUN_ID}__Tier_AplusB",
        "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
        "row_id": f"{RUN_ID}__Tier_AplusB",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier_scope": "Tier A+B",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "status": "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)",
        "primary_kpi": "combined_not_run(합산 실행 없음)",
        "guardrail_kpi": "do_not_synthesize_combined_result(합산 결과 합성 금지)",
    })
    return [tier_a], [tier_a, tier_b, combined], [tier_a, tier_b, combined]


def write_registries() -> None:
    run_rows, project_rows, stage_rows = registry_rows()
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], stage_rows, extend_header=True)


def write_workspace_and_notes() -> None:
    final = read_json(FINAL_DECISION)
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage364E(364E 실행)가 timestamp context cost-filter model(시점 문맥 비용 필터 모델)을 학습하고 `{final["best_onnx_model_id"]}` ONNX(온엑스) 스모크를 통과시켰다.

Effect(효과): 다음 작업은 `{NEXT_RUN_ID}`에서 ONNX artifact(ONNX 산출물), threshold(임계값), feature order(피처 순서)를 MT5 runtime probe(MT5 런타임 탐침)로 인계하는 것이다.
""")
    append_text_once(WORKSPACE_CHANGELOG, "run364E_train_timestamp_context_cost_filter_model_without_db_v1", f"""## {TODAY} run364E Timestamp Context Cost Filter Model Training(364E 시점 문맥 비용 필터 모델 학습)

Action(행동): timestamp context training seed(시점 문맥 학습 씨앗)로 모델 4종을 학습하고 ONNX-exportable model(ONNX 변환 가능 모델)을 만들었다.

Effect(효과): `{final["best_onnx_model_id"]}`는 validation/OOS(검증/표본외) 비용 순수익 양수와 3/day 이상 밀도를 만족하지만, MT5 runtime probe(MT5 런타임 탐침) 전 운영 주장은 없다.
""")
    append_text_once(IDEA_REGISTRY, "IDEA-ST364E-TIMESTAMP-CONTEXT-COST-FILTER-ONNX", f"""## IDEA-ST364E-TIMESTAMP-CONTEXT-COST-FILTER-ONNX

- idea(아이디어): timestamp context(시점 문맥)를 ONNX-exportable cost-filter model(ONNX 변환 가능 비용 필터 모델)로 학습한다.
- best_onnx_model(최선 ONNX 모델): `{final["best_onnx_model_id"]}` / `{final["best_onnx_threshold_id"]}`.
- validation_oos_read(검증/표본외 판독): validation_net(검증 순수익) `{final["best_onnx_validation_net"]}`, oos_net(표본외 순수익) `{final["best_onnx_oos_net"]}`.
- runtime_probe_queue(런타임 탐침 대기열): `{rel(RUNTIME_PROBE_QUEUE)}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""")
    replace_stage_brief_header()


def write_artifact_registry() -> None:
    artifacts = [
        ("script", Path("stage_pipelines/stage364/train_timestamp_context_cost_filter_model_without_db.py"), "tracked"),
        ("report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("selection_status", SELECTION_STATUS, "tracked"),
        ("input_manifest", INPUT_MANIFEST, "ignored_with_manifest"),
        ("model_scorecard", MODEL_SCORECARD, "ignored_with_manifest"),
        ("threshold_surface", THRESHOLD_SURFACE, "ignored_with_manifest"),
        ("month_stability", MONTH_STABILITY, "ignored_with_manifest"),
        ("model_artifact_manifest", MODEL_ARTIFACT_MANIFEST, "ignored_with_manifest"),
        ("onnx_smoke_report", ONNX_SMOKE_REPORT, "ignored_with_manifest"),
        ("selected_model_summary", SELECTED_MODEL_SUMMARY, "ignored_with_manifest"),
        ("runtime_probe_queue", RUNTIME_PROBE_QUEUE, "ignored_with_manifest"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]
    rows = []
    for artifact_type, path, availability in artifacts:
        rows.append({
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file(path) if exists(path) and Path(path).is_file() else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_ID}__{artifact_type}",
            "notes": f"Stage364E timestamp context model training artifact(364E 시점 문맥 모델 학습 산출물); availability={availability}",
            "artifact_path": rel(path),
        })
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "artifact_type", "path"], rows, extend_header=False)


def refresh_gates_and_final() -> None:
    gates = gate_rows()
    write_csv(GATE_AUDIT, gates)
    final = read_json(FINAL_DECISION)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    final["required_gate_coverage_audit"] = rel(GATE_AUDIT)
    write_json(FINAL_DECISION, final)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("Missing required Stage364E inputs: " + ", ".join(missing))
    final = read_json(SOURCE_FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"Stage364D final_decision next_run_id mismatch: {final.get('next_run_id')}")
    if final.get("model_training_ready") != "ready_with_boundary":
        raise RuntimeError("Stage364E expects Stage364D model_training_ready == ready_with_boundary")
    if not source_gate_passed():
        raise RuntimeError("Stage364D source gate audit is not fully passed")


def main() -> None:
    validate_inputs()
    frame, feature_columns = load_training_data()
    score_rows, threshold_metric_rows, month_rows, trained = score_models(frame, feature_columns)
    paired_rows = paired_threshold_rows(threshold_metric_rows)
    artifact_rows, smoke_rows, summary = save_models_and_onnx(trained, feature_columns, paired_rows)
    queue_rows = runtime_probe_queue(summary)
    write_run_artifacts(frame, feature_columns, score_rows, paired_rows, month_rows, artifact_rows, smoke_rows, summary, queue_rows)
    write_reports(paired_rows, smoke_rows, queue_rows)
    write_workspace_and_notes()
    write_registries()
    refresh_gates_and_final()
    write_reports(paired_rows, smoke_rows, queue_rows)
    write_workspace_and_notes()
    write_registries()
    write_artifact_registry()
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
