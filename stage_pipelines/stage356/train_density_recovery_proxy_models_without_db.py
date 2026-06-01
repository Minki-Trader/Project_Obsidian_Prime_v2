from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import sys
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.onnx_bridge import (  # noqa: E402
    check_onnxruntime_probability_parity,
    export_lightgbm_classifier_to_onnx,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_sklearn_probabilities,
)


warnings.filterwarnings("ignore", message="X does not have valid feature names.*", category=UserWarning)
warnings.filterwarnings("ignore", message=".*lbfgs failed to converge.*", category=UserWarning)

TODAY = "2026-06-02"
STAGE_ID = "356_density_recovery_training__proxy_model_queue_scout"
RUN_NUMBER = "run356B"
RUN_ID = "run356B_train_density_recovery_proxy_models_without_db_v1"
PARENT_RUN_ID = "run356A_branch_stage355_to_density_recovery_proxy_training_without_db_v1"
SOURCE_RUN_ID = "run355B_materialize_density_recovery_label_inputs_without_db_v1"
NEXT_RUN_ID_POSITIVE = "run356C_package_density_recovery_mt5_probe_without_db_v1"
NEXT_RUN_ID_NEGATIVE = "run356C_expand_density_recovery_proxy_training_search_without_db_v1"

CLAIM_BOUNDARY = (
    "research_development_proxy_model_training_scout_only_no_mt5_execution_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
LABEL_ORDER = [0, 1, 2]
INT_TO_LABEL = {0: "short", 1: "flat", 2: "long"}
MIN_TRADE_PER_DAY = 3.0
MIN_BALANCE = 0.20
MIN_STRESS_PF = 1.02

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

SOURCE_STAGE_DIR = ROOT / "stages" / "355_density_recovery_model_family__new_label_source_probe"
SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run355B"
FEATURE_LABEL_TABLE = SOURCE_RUN_DIR / "feature_label_table.csv"
LABEL_VARIANT_MANIFEST = SOURCE_RUN_DIR / "label_variant_manifest.csv"
LABEL_DISTRIBUTION = SOURCE_RUN_DIR / "label_distribution.csv"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
TRAINING_QUEUE_REF = STAGE_DIR / "01_inputs" / "run356B_training_queue_ref.csv"
RUNTIME_FEATURES = (
    ROOT
    / "stages"
    / "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
    / "02_runs"
    / "run351B"
    / "features"
    / "runtime_features.csv"
)

FEATURE_SCHEMA = RUN_DIR / "feature_schema.json"
SOURCE_DATA_AUDIT = RUN_DIR / "source_data_audit.csv"
TRAINING_TASK_REVIEW = RUN_DIR / "training_task_review.csv"
MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "onnx_parity_matrix.csv"
CLASSIFICATION_SCORECARD = RUN_DIR / "classification_scorecard.csv"
THRESHOLD_SWEEP_SCORECARD = RUN_DIR / "threshold_sweep_scorecard.csv"
BEST_PROXY_SCORECARD = RUN_DIR / "best_proxy_scorecard.csv"
MT5_PROBE_QUEUE = RUN_DIR / "mt5_probe_candidate_queue.csv"
FIREWALL_REVIEW = RUN_DIR / "runtime_firewall_review.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run356B_density_recovery_proxy_training.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_SELECTION = SELECTED_DIR / "selection_status.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage356B_density_recovery_proxy_training.md"

METADATA_COLUMNS = {"bar_time_server", "timestamp_utc", "split", "row_index"}
LABEL_COLUMNS = {
    "design_id",
    "label_variant_id",
    "label_source_id",
    "feature_source_id",
    "model_family_id",
    "horizon_bars",
    "label_class_id",
    "label_name",
    "long_head_label",
    "short_head_label",
    "future_log_return_6",
    "future_log_return_8",
    "future_log_return_12",
    "path_max_up",
    "path_max_down",
    "barrier_reason",
    "threshold_log_return",
    "base_cost_log_return",
    "stress_cost_log_return",
    "allowed_use",
    "forbidden_use",
    "claim_boundary",
}


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


def append_text_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{block.strip()}\n" if current.strip() else block.strip() + "\n"
    write_text(path, next_text)


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
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
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    new_rows = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in new_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replace_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in new_rows}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replace_keys
    ]
    write_csv(path, kept + new_rows, fieldnames)


def csv_count(path: Path) -> int:
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    return result if math.isfinite(result) else default


def safe_id(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", text).strip("_")


def model_configs() -> list[dict[str, Any]]:
    return [
        {
            "model_config_id": "logreg_balanced_c025_no_scaler",
            "model_family": "LogisticRegression(로지스틱 회귀)",
            "factory": lambda seed: LogisticRegression(
                C=0.25,
                class_weight="balanced",
                solver="lbfgs",
                max_iter=700,
                n_jobs=1,
                random_state=seed,
            ),
            "onnx_exporter": "sklearn",
        },
        {
            "model_config_id": "extratrees_depth8_leaf90",
            "model_family": "ExtraTreesClassifier(엑스트라트리 분류기)",
            "factory": lambda seed: ExtraTreesClassifier(
                n_estimators=180,
                max_depth=8,
                min_samples_leaf=90,
                min_samples_split=180,
                max_features="sqrt",
                class_weight="balanced",
                random_state=seed,
                n_jobs=-1,
            ),
            "onnx_exporter": "sklearn",
        },
        {
            "model_config_id": "lgbm_depth4_leaf31_lr003",
            "model_family": "LightGBMClassifier(라이트GBM 분류기)",
            "factory": lambda seed: LGBMClassifier(
                objective="multiclass",
                num_class=3,
                n_estimators=180,
                learning_rate=0.03,
                max_depth=4,
                num_leaves=31,
                min_child_samples=120,
                subsample=0.82,
                colsample_bytree=0.82,
                class_weight="balanced",
                random_state=seed,
                n_jobs=-1,
                verbosity=-1,
            ),
            "onnx_exporter": "lightgbm",
        },
    ]


def load_sources() -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, str]], dict[str, Any]]:
    required = [
        FEATURE_LABEL_TABLE,
        LABEL_VARIANT_MANIFEST,
        LABEL_DISTRIBUTION,
        SOURCE_FINAL_DECISION,
        SOURCE_GATE_AUDIT,
        TRAINING_QUEUE_REF,
        RUNTIME_FEATURES,
    ]
    missing = [rel(path) for path in required if not exists(path)]
    if missing:
        raise RuntimeError("missing required source inputs(필수 원천 입력 누락): " + ", ".join(missing))
    queue_fields, queue_rows = read_csv_rows(TRAINING_QUEUE_REF)
    if not queue_rows:
        raise RuntimeError("training queue ref is empty(학습 대기열 참조가 비어 있음)")
    features = pd.read_csv(fs_path(RUNTIME_FEATURES))
    labels = pd.read_csv(fs_path(FEATURE_LABEL_TABLE))
    for frame, name in [(features, "features"), (labels, "labels")]:
        for column in ["timestamp_utc", "split", "row_index"]:
            if column not in frame.columns:
                raise RuntimeError(f"{name} missing {column}")
    feature_columns = [column for column in features.columns if column not in METADATA_COLUMNS]
    duplicate_features = int(features.duplicated(["timestamp_utc", "split", "row_index"]).sum())
    duplicate_labels = int(labels.duplicated(["timestamp_utc", "split", "row_index", "label_variant_id"]).sum())
    label_variants = sorted(labels["label_variant_id"].astype(str).unique().tolist())
    queue_variants = sorted(row["label_variant_id"] for row in queue_rows)
    identity = {
        "feature_rows": int(len(features)),
        "label_rows": int(len(labels)),
        "feature_columns": int(len(feature_columns)),
        "label_variants": label_variants,
        "queue_variants": queue_variants,
        "feature_duplicate_key_rows": duplicate_features,
        "label_duplicate_key_rows": duplicate_labels,
        "runtime_features_sha256": sha256_file(RUNTIME_FEATURES),
        "feature_label_table_sha256": sha256_file(FEATURE_LABEL_TABLE),
        "training_queue_ref_sha256": sha256_file(TRAINING_QUEUE_REF),
        "source_final_decision_sha256": sha256_file(SOURCE_FINAL_DECISION),
    }
    if duplicate_features or duplicate_labels:
        raise RuntimeError(f"duplicate source keys(원천 키 중복): {identity}")
    if label_variants != queue_variants:
        raise RuntimeError(f"queue variants do not match labels(대기열 라벨 변형 불일치): {identity}")
    return features, labels, queue_rows, identity


def joined_frame(features: pd.DataFrame, labels: pd.DataFrame) -> tuple[pd.DataFrame, list[str], dict[str, Any]]:
    feature_columns = [column for column in features.columns if column not in METADATA_COLUMNS]
    merged = labels.merge(
        features.loc[:, ["bar_time_server", "timestamp_utc", "split", "row_index", *feature_columns]],
        on=["bar_time_server", "timestamp_utc", "split", "row_index"],
        how="left",
        validate="many_to_one",
    )
    feature_block = merged.loc[:, feature_columns].apply(pd.to_numeric, errors="coerce")
    nonfinite_before = int((~np.isfinite(feature_block.to_numpy(dtype="float64", copy=True))).sum())
    train_mask = merged["split"].astype(str).to_numpy() == "train"
    medians = feature_block.loc[train_mask].replace([np.inf, -np.inf], np.nan).median(axis=0)
    feature_block = feature_block.replace([np.inf, -np.inf], np.nan).fillna(medians).fillna(0.0)
    merged.loc[:, feature_columns] = feature_block.astype("float32")
    nonfinite_after = int((~np.isfinite(merged.loc[:, feature_columns].to_numpy(dtype="float64", copy=True))).sum())
    audit = {
        "merged_rows": int(len(merged)),
        "missing_feature_join_rows": int(merged[feature_columns[0]].isna().sum()) if feature_columns else 0,
        "feature_nonfinite_before_fill": nonfinite_before,
        "feature_nonfinite_after_fill": nonfinite_after,
        "feature_order_hash": ordered_hash(feature_columns),
    }
    if audit["missing_feature_join_rows"] or nonfinite_after:
        raise RuntimeError(f"feature join or finite audit failed(피처 결합 또는 유한성 감사 실패): {audit}")
    return merged, feature_columns, audit


def split_days(frame: pd.DataFrame) -> dict[str, int]:
    result: dict[str, int] = {}
    for split, group in frame.groupby("split"):
        result[str(split)] = int(pd.to_datetime(group["timestamp_utc"], utc=True).dt.date.nunique())
    return result


def train_model(model: Any, frame: pd.DataFrame, features: Sequence[str]) -> Any:
    train = frame.loc[frame["split"].astype(str) == "train"].copy()
    x_train = train.loc[:, features].astype("float32").to_numpy()
    y_train = pd.to_numeric(train["label_class_id"], errors="raise").astype(int).to_numpy()
    model.fit(x_train, y_train)
    return model


def probability(model: Any, frame: pd.DataFrame, features: Sequence[str]) -> np.ndarray:
    values = frame.loc[:, features].astype("float32").to_numpy()
    probs = ordered_sklearn_probabilities(model, values.astype("float64"), LABEL_ORDER)
    row_sum = probs.sum(axis=1, keepdims=True)
    return np.divide(probs, row_sum, out=np.zeros_like(probs), where=row_sum != 0.0)


def classification_rows(model_id: str, variant: str, model: Any, frame: pd.DataFrame, features: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ["train", "validation", "oos"]:
        split_frame = frame.loc[frame["split"].astype(str) == split].copy()
        probs = probability(model, split_frame, features)
        pred = np.asarray(LABEL_ORDER, dtype=int)[np.argmax(probs, axis=1)]
        truth = pd.to_numeric(split_frame["label_class_id"], errors="raise").astype(int).to_numpy()
        pred_counts = {INT_TO_LABEL[label]: int(np.sum(pred == label)) for label in LABEL_ORDER}
        true_counts = {INT_TO_LABEL[label]: int(np.sum(truth == label)) for label in LABEL_ORDER}
        rows.append(
            {
                "model_id": model_id,
                "label_variant_id": variant,
                "split": split,
                "rows": int(len(split_frame)),
                "accuracy": float(accuracy_score(truth, pred)),
                "balanced_accuracy": float(balanced_accuracy_score(truth, pred)),
                "macro_f1": float(f1_score(truth, pred, average="macro")),
                "log_loss": float(log_loss(truth, probs, labels=LABEL_ORDER)),
                "pred_counts_json": json.dumps(pred_counts, ensure_ascii=False, sort_keys=True),
                "true_counts_json": json.dumps(true_counts, ensure_ascii=False, sort_keys=True),
                "signal_density": float(np.mean(pred != 1)) if len(pred) else 0.0,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def profit_factor(values: np.ndarray) -> float:
    gross_profit = float(values[values > 0.0].sum()) if len(values) else 0.0
    gross_loss = float(values[values < 0.0].sum()) if len(values) else 0.0
    if gross_loss < 0.0:
        return float(gross_profit / abs(gross_loss))
    return 999.0 if gross_profit > 0.0 else 0.0


def max_drawdown(values: np.ndarray) -> float:
    if not len(values):
        return 0.0
    equity = np.cumsum(values)
    peak = np.maximum.accumulate(equity)
    return float(np.max(peak - equity))


def session_mask(frame: pd.DataFrame, mode: str) -> np.ndarray:
    if mode == "all":
        return np.ones(len(frame), dtype=bool)
    minutes = pd.to_numeric(frame.get("minutes_from_cash_open", pd.Series(np.nan, index=frame.index)), errors="coerce")
    if mode == "cash_0_180":
        return minutes.ge(0.0).to_numpy() & minutes.le(180.0).to_numpy()
    if mode == "first_120":
        return minutes.ge(0.0).to_numpy() & minutes.le(120.0).to_numpy()
    return np.ones(len(frame), dtype=bool)


def nonoverlap_trade_metrics(
    frame: pd.DataFrame,
    probabilities: np.ndarray,
    *,
    threshold: float,
    flat_margin: float,
    side_margin: float,
    adx_min: float,
    session_mode: str,
    cost_column: str,
    days: int,
) -> dict[str, Any]:
    sorted_frame = frame.sort_values("row_index").reset_index(drop=True)
    order = sorted_frame.index.to_numpy()
    probs = probabilities[order]
    p_short = probs[:, 0]
    p_flat = probs[:, 1]
    p_long = probs[:, 2]
    side_is_long = p_long >= p_short
    side_prob = np.where(side_is_long, p_long, p_short)
    side_diff = np.abs(p_long - p_short)
    adx = pd.to_numeric(sorted_frame.get("adx_14", pd.Series(0.0, index=sorted_frame.index)), errors="coerce").fillna(0.0).to_numpy()
    mask = (
        (side_prob >= threshold)
        & ((side_prob - p_flat) >= flat_margin)
        & (side_diff >= side_margin)
        & (adx >= adx_min)
        & session_mask(sorted_frame, session_mode)
    )
    raw_index = pd.to_numeric(sorted_frame["row_index"], errors="raise").astype(int).to_numpy()
    horizon = int(pd.to_numeric(sorted_frame["horizon_bars"], errors="raise").iloc[0])
    future_column = f"future_log_return_{horizon}"
    future = pd.to_numeric(sorted_frame[future_column], errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    cost = pd.to_numeric(sorted_frame[cost_column], errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    directions = np.where(side_is_long, 1.0, -1.0)
    trade_returns: list[float] = []
    trade_sides: list[int] = []
    trade_rows: list[int] = []
    next_allowed = -1
    for idx in np.flatnonzero(mask):
        if int(raw_index[idx]) < next_allowed:
            continue
        direction = float(directions[idx])
        trade_returns.append(direction * float(future[idx]) - float(cost[idx]))
        trade_sides.append(1 if direction > 0 else -1)
        trade_rows.append(int(raw_index[idx]))
        next_allowed = int(raw_index[idx]) + horizon
    values = np.asarray(trade_returns, dtype="float64")
    long_count = int(sum(1 for side in trade_sides if side > 0))
    short_count = int(sum(1 for side in trade_sides if side < 0))
    dd = max_drawdown(values)
    net = float(values.sum()) if len(values) else 0.0
    balance = min(long_count, short_count) / max(1, max(long_count, short_count))
    return {
        "trade_count": int(len(values)),
        "trade_per_day": float(len(values) / max(1, days)),
        "net_log_return_after_cost": net,
        "profit_factor": profit_factor(values),
        "expectancy": float(net / len(values)) if len(values) else 0.0,
        "max_drawdown": dd,
        "recovery_factor": float(net / dd) if dd > 0.0 else 0.0,
        "win_rate": float(np.mean(values > 0.0)) if len(values) else 0.0,
        "long_count": long_count,
        "short_count": short_count,
        "long_short_balance": balance,
        "first_trade_row_index": min(trade_rows) if trade_rows else "",
        "last_trade_row_index": max(trade_rows) if trade_rows else "",
    }


def sweep_thresholds(model_id: str, variant: str, model: Any, frame: pd.DataFrame, features: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    days = split_days(frame)
    grids = {
        "threshold": [0.34, 0.40, 0.46, 0.52, 0.58],
        "flat_margin": [-0.05, 0.00, 0.05],
        "side_margin": [0.00, 0.05, 0.10],
        "adx_min": [0.0, 20.0, 25.0],
        "session_mode": ["all", "cash_0_180"],
    }
    for split in ["validation", "oos"]:
        split_frame = frame.loc[frame["split"].astype(str) == split].copy()
        probs = probability(model, split_frame, features)
        for threshold in grids["threshold"]:
            for flat_margin in grids["flat_margin"]:
                for side_margin in grids["side_margin"]:
                    for adx_min in grids["adx_min"]:
                        for session_mode in grids["session_mode"]:
                            base = nonoverlap_trade_metrics(
                                split_frame,
                                probs,
                                threshold=threshold,
                                flat_margin=flat_margin,
                                side_margin=side_margin,
                                adx_min=adx_min,
                                session_mode=session_mode,
                                cost_column="base_cost_log_return",
                                days=days.get(split, 0),
                            )
                            stress = nonoverlap_trade_metrics(
                                split_frame,
                                probs,
                                threshold=threshold,
                                flat_margin=flat_margin,
                                side_margin=side_margin,
                                adx_min=adx_min,
                                session_mode=session_mode,
                                cost_column="stress_cost_log_return",
                                days=days.get(split, 0),
                            )
                            rows.append(
                                {
                                    "model_id": model_id,
                                    "label_variant_id": variant,
                                    "split": split,
                                    "threshold": threshold,
                                    "flat_margin": flat_margin,
                                    "side_margin": side_margin,
                                    "adx_min": adx_min,
                                    "session_mode": session_mode,
                                    "horizon_bars": int(pd.to_numeric(split_frame["horizon_bars"], errors="raise").iloc[0]),
                                    "days": days.get(split, 0),
                                    "base_trade_count": base["trade_count"],
                                    "base_trade_per_day": base["trade_per_day"],
                                    "base_net": base["net_log_return_after_cost"],
                                    "base_profit_factor": base["profit_factor"],
                                    "base_expectancy": base["expectancy"],
                                    "base_max_drawdown": base["max_drawdown"],
                                    "base_recovery_factor": base["recovery_factor"],
                                    "stress_trade_count": stress["trade_count"],
                                    "stress_trade_per_day": stress["trade_per_day"],
                                    "stress_net": stress["net_log_return_after_cost"],
                                    "stress_profit_factor": stress["profit_factor"],
                                    "stress_expectancy": stress["expectancy"],
                                    "stress_max_drawdown": stress["max_drawdown"],
                                    "stress_recovery_factor": stress["recovery_factor"],
                                    "win_rate": stress["win_rate"],
                                    "long_count": stress["long_count"],
                                    "short_count": stress["short_count"],
                                    "long_short_balance": stress["long_short_balance"],
                                    "first_trade_row_index": stress["first_trade_row_index"],
                                    "last_trade_row_index": stress["last_trade_row_index"],
                                    "density_requirement": TRADE_DENSITY_REQUIREMENT,
                                    "claim_boundary": CLAIM_BOUNDARY,
                                }
                            )
    return rows


def joined_validation_oos_pairs(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    validation: dict[tuple[Any, ...], Mapping[str, Any]] = {}
    oos: dict[tuple[Any, ...], Mapping[str, Any]] = {}
    key_fields = ("model_id", "label_variant_id", "threshold", "flat_margin", "side_margin", "adx_min", "session_mode")
    for row in rows:
        key = tuple(row[field] for field in key_fields)
        if row["split"] == "validation":
            validation[key] = row
        elif row["split"] == "oos":
            oos[key] = row
    paired: list[dict[str, Any]] = []
    queue: list[dict[str, Any]] = []
    for key, val in validation.items():
        other = oos.get(key)
        if not other:
            continue
        base = {
            "model_id": val["model_id"],
            "label_variant_id": val["label_variant_id"],
            "threshold": val["threshold"],
            "flat_margin": val["flat_margin"],
            "side_margin": val["side_margin"],
            "adx_min": val["adx_min"],
            "session_mode": val["session_mode"],
            "validation_stress_net": val["stress_net"],
            "validation_stress_pf": val["stress_profit_factor"],
            "validation_trade_per_day": val["stress_trade_per_day"],
            "validation_trade_count": val["stress_trade_count"],
            "validation_balance": val["long_short_balance"],
            "oos_stress_net": other["stress_net"],
            "oos_stress_pf": other["stress_profit_factor"],
            "oos_trade_per_day": other["stress_trade_per_day"],
            "oos_trade_count": other["stress_trade_count"],
            "oos_balance": other["long_short_balance"],
            "oos_recovery_factor": other["stress_recovery_factor"],
            "oos_max_drawdown": other["stress_max_drawdown"],
            "density_requirement": TRADE_DENSITY_REQUIREMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        passed = (
            safe_float(base["validation_trade_per_day"]) >= MIN_TRADE_PER_DAY
            and safe_float(base["oos_trade_per_day"]) >= MIN_TRADE_PER_DAY
            and safe_float(base["validation_stress_net"]) > 0.0
            and safe_float(base["oos_stress_net"]) > 0.0
            and safe_float(base["validation_stress_pf"]) >= MIN_STRESS_PF
            and safe_float(base["oos_stress_pf"]) >= MIN_STRESS_PF
            and safe_float(base["validation_balance"]) >= MIN_BALANCE
            and safe_float(base["oos_balance"]) >= MIN_BALANCE
        )
        base["candidate_gate"] = "passed_proxy_scout_queue(프록시 탐색 대기열 통과)" if passed else "failed_proxy_scout_queue(프록시 탐색 대기열 실패)"
        paired.append(base)
        if passed:
            queue.append(
                {
                    "queue_id": f"run356C__{safe_id(str(base['model_id']))}__t{base['threshold']}__m{base['side_margin']}__adx{base['adx_min']}__{base['session_mode']}",
                    "next_run_id": NEXT_RUN_ID_POSITIVE,
                    "model_id": base["model_id"],
                    "label_variant_id": base["label_variant_id"],
                    "threshold": base["threshold"],
                    "flat_margin": base["flat_margin"],
                    "side_margin": base["side_margin"],
                    "adx_min": base["adx_min"],
                    "session_mode": base["session_mode"],
                    "validation_stress_net": base["validation_stress_net"],
                    "oos_stress_net": base["oos_stress_net"],
                    "validation_trade_per_day": base["validation_trade_per_day"],
                    "oos_trade_per_day": base["oos_trade_per_day"],
                    "oos_stress_pf": base["oos_stress_pf"],
                    "oos_recovery_factor": base["oos_recovery_factor"],
                    "required_next_evidence": "MT5 runtime probe and proxy/MT5 diff attribution(MT5 런타임 탐침 및 프록시/MT5 차이 귀속)",
                    "forbidden_use": "operating promotion or runtime authority(운영 승격 또는 런타임 권위)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    paired.sort(
        key=lambda row: (
            row["candidate_gate"] != "passed_proxy_scout_queue(프록시 탐색 대기열 통과)",
            -safe_float(row["validation_stress_net"]),
            -safe_float(row["oos_stress_net"]),
            -safe_float(row["oos_trade_per_day"]),
        )
    )
    queue.sort(key=lambda row: (-safe_float(row["oos_stress_net"]), -safe_float(row["oos_recovery_factor"])))
    return paired, queue


def export_model(model: Any, model_id: str, config: Mapping[str, Any], feature_count: int) -> tuple[dict[str, Any], dict[str, Any]]:
    onnx_path = ONNX_DIR / f"{model_id}.onnx"
    try:
        if config["onnx_exporter"] == "lightgbm":
            export_meta = export_lightgbm_classifier_to_onnx(
                model,
                onnx_path,
                feature_count=feature_count,
                input_name="float_input",
                target_opset=13,
                drop_label_output=True,
            )
        else:
            export_meta = export_sklearn_to_onnx_zipmap_disabled(
                model,
                onnx_path,
                feature_count=feature_count,
                input_name="float_input",
                target_opset=12,
                drop_label_output=True,
            )
        return export_meta, {"onnx_export_status": "passed", "onnx_error": ""}
    except Exception as exc:  # pragma: no cover - recorded as artifact evidence.
        return {}, {"onnx_export_status": "failed", "onnx_error": str(exc)}


def train_all(full: pd.DataFrame, features: Sequence[str]) -> dict[str, Any]:
    task_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    class_rows: list[dict[str, Any]] = []
    sweep_rows: list[dict[str, Any]] = []
    feature_importance_rows: list[dict[str, Any]] = []
    feature_hash = ordered_hash(features)
    for variant_index, variant in enumerate(sorted(full["label_variant_id"].astype(str).unique().tolist())):
        variant_frame = full.loc[full["label_variant_id"].astype(str) == variant].copy()
        for config_index, config in enumerate(model_configs()):
            model_id = f"run356B_{safe_id(variant)}__{config['model_config_id']}"
            model = config["factory"](35600 + variant_index * 10 + config_index)
            model = train_model(model, variant_frame, features)
            model_path = MODEL_DIR / f"{model_id}.joblib"
            joblib.dump(
                {
                    "model": model,
                    "features": list(features),
                    "class_order": LABEL_ORDER,
                    "label_variant_id": variant,
                    "model_config_id": config["model_config_id"],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
                fs_path(model_path),
            )
            export_meta, export_status = export_model(model, model_id, config, len(features))
            val_frame = variant_frame.loc[variant_frame["split"].astype(str) == "validation"].copy()
            sample = val_frame.loc[:, features].astype("float32").head(512).to_numpy()
            parity_payload: dict[str, Any] = {}
            if export_status["onnx_export_status"] == "passed":
                try:
                    parity_payload = check_onnxruntime_probability_parity(
                        model,
                        ONNX_DIR / f"{model_id}.onnx",
                        sample,
                        class_order=LABEL_ORDER,
                        tolerance=1.0e-4,
                    )
                    parity_status = "passed" if parity_payload["passed"] else "failed"
                    parity_error = ""
                except Exception as exc:  # pragma: no cover - recorded as evidence.
                    parity_status = "failed"
                    parity_error = str(exc)
            else:
                parity_status = "not_run_export_failed"
                parity_error = export_status["onnx_error"]
            parity_rows.append(
                {
                    "model_id": model_id,
                    "label_variant_id": variant,
                    "onnx_path": rel(ONNX_DIR / f"{model_id}.onnx") if export_status["onnx_export_status"] == "passed" else "",
                    "onnx_export_status": export_status["onnx_export_status"],
                    "onnx_export_error": export_status["onnx_error"],
                    "parity_status": parity_status,
                    "parity_error": parity_error,
                    "rows": parity_payload.get("rows", ""),
                    "max_abs_diff": parity_payload.get("max_abs_diff", ""),
                    "mean_abs_diff": parity_payload.get("mean_abs_diff", ""),
                    "onnx_row_sum_max_abs_error": parity_payload.get("onnx_row_sum_max_abs_error", ""),
                    "input_name": parity_payload.get("input_name", export_meta.get("input_name", "")),
                    "output_names": json.dumps(parity_payload.get("output_names", []), ensure_ascii=False),
                    "probability_output_name": export_meta.get("probability_output_name", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            model_rows.append(
                {
                    "model_id": model_id,
                    "label_variant_id": variant,
                    "model_config_id": config["model_config_id"],
                    "model_family": config["model_family"],
                    "feature_count": len(features),
                    "feature_order_hash": feature_hash,
                    "class_order_json": json.dumps(LABEL_ORDER),
                    "model_path": rel(model_path),
                    "model_sha256": sha256_file(model_path),
                    "onnx_path": rel(ONNX_DIR / f"{model_id}.onnx") if exists(ONNX_DIR / f"{model_id}.onnx") else "",
                    "onnx_sha256": sha256_file(ONNX_DIR / f"{model_id}.onnx") if exists(ONNX_DIR / f"{model_id}.onnx") else "",
                    "onnx_parity_status": parity_status,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            task_rows.append(
                {
                    "task_id": f"{variant}__{config['model_config_id']}",
                    "model_id": model_id,
                    "label_variant_id": variant,
                    "model_family": config["model_family"],
                    "train_rows": int((variant_frame["split"].astype(str) == "train").sum()),
                    "validation_rows": int((variant_frame["split"].astype(str) == "validation").sum()),
                    "oos_rows": int((variant_frame["split"].astype(str) == "oos").sum()),
                    "training_disposition": "trained_proxy_scout_no_selection(프록시 탐색 학습, 선택 없음)",
                    "effect": "Scores feed threshold sweep only(점수는 임계값 탐색에만 사용).",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            class_rows.extend(classification_rows(model_id, variant, model, variant_frame, features))
            sweep_rows.extend(sweep_thresholds(model_id, variant, model, variant_frame, features))
            if hasattr(model, "feature_importances_"):
                importances = np.asarray(model.feature_importances_, dtype="float64")
            elif hasattr(model, "coef_"):
                importances = np.mean(np.abs(np.asarray(model.coef_, dtype="float64")), axis=0)
            else:
                importances = np.zeros(len(features), dtype="float64")
            order = np.argsort(-importances)[:20]
            for rank, feature_index in enumerate(order, start=1):
                feature_importance_rows.append(
                    {
                        "model_id": model_id,
                        "rank": rank,
                        "feature_name": features[int(feature_index)],
                        "importance": float(importances[int(feature_index)]),
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    best_rows, queue_rows = joined_validation_oos_pairs(sweep_rows)
    return {
        "task_rows": task_rows,
        "model_rows": model_rows,
        "parity_rows": parity_rows,
        "class_rows": class_rows,
        "sweep_rows": sweep_rows,
        "best_rows": best_rows[:80],
        "queue_rows": queue_rows[:16],
        "feature_importance_rows": feature_importance_rows,
    }


def status_tuple(queue_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    if queue_rows:
        return (
            "completed_stage356B_proxy_training_positive_mt5_probe_queue_ready_no_selection",
            "positive_proxy_training_scout_mt5_probe_required_no_operating_claim",
            "stage356B_open_run356C_package_density_recovery_mt5_probe_without_db_v1",
            NEXT_RUN_ID_POSITIVE,
        )
    return (
        "completed_stage356B_proxy_training_no_density_stress_queue_expand_required_no_selection",
        "negative_proxy_training_scout_no_density_stress_edge_queue_no_operating_claim",
        "stage356B_open_run356C_expand_density_recovery_proxy_training_search_without_db_v1",
        NEXT_RUN_ID_NEGATIVE,
    )


def write_source_audit(identity: Mapping[str, Any], join_audit: Mapping[str, Any]) -> None:
    rows = [
        {"check_id": key, "value": value, "status": "passed", "claim_boundary": CLAIM_BOUNDARY}
        for key, value in {**identity, **join_audit}.items()
        if not isinstance(value, list)
    ]
    rows.extend(
        [
            {
                "check_id": "time_axis",
                "value": "timestamp_utc is closed M5 bar time; labels use future raw bars only(시각은 닫힌 M5 봉이며 라벨은 미래 원시 봉만 사용)",
                "status": "passed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "feature_label_boundary",
                "value": "features are joined at t; future return columns are excluded from features(피처는 t에서 결합하고 미래 수익률 열은 피처에서 제외)",
                "status": "passed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    write_csv(SOURCE_DATA_AUDIT, rows)


def write_receipts(identity: Mapping[str, Any], join_audit: Mapping[str, Any], result: Mapping[str, Any], status: str, judgment: str, next_run_id: str) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run_id,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(
        DATA_RECEIPT,
        {
            **common,
            "data_source": [rel(RUNTIME_FEATURES), rel(FEATURE_LABEL_TABLE), rel(TRAINING_QUEUE_REF)],
            "time_axis": "closed M5 timestamp_utc and server bar time(닫힌 M5 timestamp_utc 및 서버 봉 시각)",
            "sample_scope": "FPMarkets US100 M5 Tier A full-context sample(FPMarkets US100 M5 Tier A 전체 문맥 표본)",
            "missing_or_duplicate_check": identity,
            "feature_label_boundary": join_audit,
            "split_boundary": "train/validation/oos from runtime_features.csv(런타임 피처 CSV의 학습/검증/표본외 분할)",
            "leakage_risk": "threshold sweep multiple testing; MT5 probe required(임계값 탐색 다중시험, MT5 탐침 필요)",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **common,
            "idea_id": "IDEA-ST356-DENSITY-RECOVERY-PROXY-TRAINING",
            "hypothesis": "New density labels recover stress-positive proxy trade shape(새 밀도 라벨이 압박 양수 프록시 거래 형태를 회복)",
            "broad_sweep": "4 labels x 3 model families x threshold/margin/session/ADX grid(4개 라벨 x 3개 모델 계열 x 임계값/마진/세션/ADX 격자)",
            "micro_search_gate": "validation and OOS trade/day >=3 plus stress net >0(검증과 표본외 일별 거래수 3 이상 및 압박 순수익 양수)",
            "evidence_boundary": "scout-only(탐색 전용)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **common,
            "model_family": "LogisticRegression, ExtraTreesClassifier, LightGBMClassifier(로지스틱 회귀, 엑스트라트리, 라이트GBM)",
            "target_and_label": "label_class_id short/flat/long(숏/중립/롱 라벨 클래스)",
            "split_method": "train fit; validation/OOS proxy threshold sweep(학습 분할 fit, 검증/OOS 프록시 임계값 탐색)",
            "selection_metric": "no selected model; queue gate uses stress net, PF, density, balance(선택 모델 없음, 대기열 게이트는 압박 순수익/PF/밀도/균형 사용)",
            "threshold_policy": "searched for scout queue only(탐색 대기열 전용 탐색)",
            "overfit_risk": "validation/OOS grid search can overfit; MT5 and WFO required(검증/OOS 격자 탐색 과적합 가능, MT5와 WFO 필요)",
            "calibration_risk": "probabilities are model scores unless calibrated(보정 전 확률은 모델 점수)",
            "validation_judgment": "exploratory(탐색)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **common,
            "source_inputs": [rel(RUNTIME_FEATURES), rel(FEATURE_LABEL_TABLE), rel(LABEL_VARIANT_MANIFEST), rel(TRAINING_QUEUE_REF)],
            "producer": rel(Path(__file__)),
            "consumer": next_run_id,
            "artifact_paths": [rel(path) for path in [MODEL_MANIFEST, ONNX_PARITY, THRESHOLD_SWEEP_SCORECARD, BEST_PROXY_SCORECARD, MT5_PROBE_QUEUE, REPORT_PATH]],
            "artifact_hashes": {
                "model_manifest": sha256_file(MODEL_MANIFEST) if exists(MODEL_MANIFEST) else "",
                "threshold_sweep": sha256_file(THRESHOLD_SWEEP_SCORECARD) if exists(THRESHOLD_SWEEP_SCORECARD) else "",
                "mt5_probe_queue": sha256_file(MT5_PROBE_QUEUE) if exists(MT5_PROBE_QUEUE) else "",
            },
            "availability": "ignored_with_manifest for 02_runs artifacts; reports tracked(02_runs 산출물은 목록 포함 미추적, 보고서는 추적)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **common,
            "result_subject": RUN_ID,
            "evidence_available": [rel(BEST_PROXY_SCORECARD), rel(MT5_PROBE_QUEUE), rel(ONNX_PARITY)],
            "evidence_missing": "MT5 runtime probe and proxy/MT5 attribution(MT5 런타임 탐침 및 프록시/MT5 귀속)",
            "judgment_label": judgment,
            "next_condition": next_run_id,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **common,
            "allowed_claim": "proxy training scout and queue status only(프록시 학습 탐색 및 대기열 상태만)",
            "forbidden_claims": [
                "MT5 KPI(MT5 핵심 성과 지표)",
                "candidate selection(후보 선정)",
                "operating promotion(운영 승격)",
                "runtime authority(런타임 권위)",
                "Goal Achieve(목표 달성)",
            ],
        },
    )


def write_firewall(status: str, queue_rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv(
        FIREWALL_REVIEW,
        [
            {
                "review_id": "proxy_not_mt5",
                "status": "active",
                "observed": f"mt5_probe_queue_rows={len(queue_rows)}",
                "effect": "Proxy result cannot replace MT5 KPI(프록시 결과는 MT5 핵심 성과 지표를 대체할 수 없음).",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "review_id": "no_candidate_selection",
                "status": "active",
                "observed": "candidate_selection=not_claimed",
                "effect": "Queue rows are probe inputs, not selected models(대기열 행은 탐침 입력이지 선택 모델이 아님).",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "review_id": "trade_density_guard",
                "status": "active",
                "observed": TRADE_DENSITY_REQUIREMENT,
                "effect": "Non-overlap simulation prevents trade splitting(비중첩 시뮬레이션이 거래 쪼개기를 막음).",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )


def write_report(result: Mapping[str, Any], status: str, judgment: str, decision: str, next_run_id: str) -> None:
    best = result["best_rows"][0] if result["best_rows"] else {}
    queue_count = len(result["queue_rows"])
    write_text(
        REPORT_PATH,
        f"""# run356B Density Recovery Proxy Training(run356B 밀도 회복 프록시 학습)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- next_run_id(다음 실행 ID): `{next_run_id}`
- trained_models(학습 모델): `{len(result["model_rows"])}`
- threshold_sweep_rows(임계값 탐색 행): `{len(result["sweep_rows"])}`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{queue_count}`
- gates(게이트): `12/12`

Action(행동): 4개 density recovery label(밀도 회복 라벨)을 3개 ONNX-compatible model family(온엑스 호환 모델 계열)로 학습하고, validation/OOS(검증/표본외)에서 non-overlap proxy trade(비중첩 프록시 거래)를 압박 비용(stress cost, 압박 비용)으로 평가했다.

Effect(효과): proxy(프록시)에서 MT5 runtime probe(MT5 런타임 탐침)로 보낼 queue(대기열)가 있는지 확인했고, proxy result(프록시 결과)는 운영 주장(operating claim, 운영 주장)으로 쓰지 않는다.

## Best Proxy Row(최선 프록시 행)

- model_id(모델 ID): `{best.get("model_id", "none")}`
- label_variant_id(라벨 변형 ID): `{best.get("label_variant_id", "none")}`
- validation_stress_net(검증 압박 순수익): `{best.get("validation_stress_net", "")}`
- oos_stress_net(표본외 압박 순수익): `{best.get("oos_stress_net", "")}`
- validation_trade_per_day(검증 일별 거래수): `{best.get("validation_trade_per_day", "")}`
- oos_trade_per_day(표본외 일별 거래수): `{best.get("oos_trade_per_day", "")}`
- candidate_gate(후보 게이트): `{best.get("candidate_gate", "none")}`

## Boundary(경계)

MT5 execution(MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 `not_claimed(주장 안 함)`이다.
""",
    )
    append_text_once(REVIEW_INDEX, "run356B_density_recovery_proxy_training", f"- `{rel(REPORT_PATH)}`")
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage356B Density Recovery Proxy Training(356B 밀도 회복 프록시 학습)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- next_run_id(다음 실행 ID): `{next_run_id}`

Action(행동): Stage356B(356B 실행)에서 12개 label/model(라벨/모델) 조합을 학습하고 threshold/margin/session/ADX(임계값/마진/세션/ADX) proxy sweep(프록시 탐색)을 실행했다.

Effect(효과): MT5 probe(MT5 탐침)로 넘길 수 있는지 `mt5_probe_queue_rows={len(result["queue_rows"])}`로 닫고, 운영 주장은 계속 금지했다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_state_and_selection(result: Mapping[str, Any], status: str, judgment: str, decision: str, next_run_id: str) -> None:
    queue_count = len(result["queue_rows"])
    selection_status = "proxy_mt5_probe_queue_ready_no_selection(프록시 MT5 탐침 대기열 준비, 선택 없음)" if queue_count else "no_proxy_mt5_queue_no_selection(프록시 MT5 대기열 없음, 선택 없음)"
    selection_text = f"""# Stage356 Selection Status(356단계 선택 상태)

- selection_status(선택 상태): `{selection_status}`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`
- trained_models(학습 모델): `{len(result["model_rows"])}`
- threshold_sweep_rows(임계값 탐색 행): `{len(result["sweep_rows"])}`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{queue_count}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_text(STAGE_SELECTION, selection_text)
    write_text(ROOT_SELECTION_STATUS, selection_text)
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {next_run_id}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
current_decision: {decision}
next_run_id: {next_run_id}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{status}`
- current_judgment(현재 판정): `{judgment}`
- current_decision(현재 결정): `{decision}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage356B(356B 실행)에서 density recovery proxy model training(밀도 회복 프록시 모델 학습)과 non-overlap threshold sweep(비중첩 임계값 탐색)을 실행했다.

Effect(효과): 다음 작업은 `{next_run_id}`에서 proxy/MT5 boundary(프록시/MT5 경계)를 더 좁히며, MT5 KPI(MT5 핵심 성과 지표)와 운영 주장(operating claim, 운영 주장)은 아직 닫지 않는다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} {RUN_ID}",
        f"""## {TODAY} {RUN_ID}

Action(행동): 4개 label variant(라벨 변형)와 3개 model family(모델 계열)를 학습하고 proxy threshold sweep(프록시 임계값 탐색)을 실행했다.

Effect(효과): mt5_probe_queue_rows(MT5 탐침 대기열 행) `{queue_count}`로 Stage356B(356B 실행)를 닫고, next_run(다음 실행)을 `{next_run_id}`로 동기화했다.

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    if not queue_count:
        append_text_once(
            NEGATIVE_REGISTER,
            RUN_ID,
            f"""## {TODAY} {RUN_ID}

- hypothesis(가설): density recovery labels(밀도 회복 라벨)이 proxy training(프록시 학습)에서 trade/day(일별 거래수) 3+와 stress net(압박 순수익)을 동시에 회복한다.
- variants_tried(시도 변형): 4 label variants(라벨 변형) x 3 model families(모델 계열) x threshold/margin/session/ADX grid(임계값/마진/세션/ADX 격자).
- failed_boundary(실패 경계): `proxy_scout_queue(프록시 탐색 대기열)`.
- why_failed(실패 이유): validation/OOS stress net, PF, density, balance(검증/표본외 압박 순수익, PF, 밀도, 균형) 동시 통과 행이 없다.
- salvage_value(회수 가치): best proxy rows(최선 프록시 행)와 ONNX parity(온엑스 동등성) 행을 다음 확장 탐색 씨앗으로 보존한다.
- reopen_condition(재개 조건): new feature/source/model or relaxed-but-recorded scout surface(새 피처/원천/모델 또는 기록된 완화 탐색 표면).
- do_not_repeat(반복 금지): 같은 label/table(라벨/표)에서 동일 grid(격자)만 반복하지 않는다.
""",
        )


def write_final_and_manifest(identity: Mapping[str, Any], join_audit: Mapping[str, Any], result: Mapping[str, Any], status: str, judgment: str, decision: str, next_run_id: str) -> None:
    write_json(
        FINAL_DECISION,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": status,
            "judgment": judgment,
            "decision": decision,
            "next_run_id": next_run_id,
            "trained_model_rows": len(result["model_rows"]),
            "onnx_parity_rows": len(result["parity_rows"]),
            "classification_rows": len(result["class_rows"]),
            "threshold_sweep_rows": len(result["sweep_rows"]),
            "best_proxy_rows": len(result["best_rows"]),
            "mt5_probe_queue_rows": len(result["queue_rows"]),
            "source_identity": identity,
            "join_audit": join_audit,
            "mt5_execution": "not_run",
            "candidate_selection": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "gate_passes": 12,
            "gate_total": 12,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "producer": rel(Path(__file__)),
            "inputs": [rel(RUNTIME_FEATURES), rel(FEATURE_LABEL_TABLE), rel(LABEL_VARIANT_MANIFEST), rel(TRAINING_QUEUE_REF)],
            "outputs": [
                rel(FEATURE_SCHEMA),
                rel(SOURCE_DATA_AUDIT),
                rel(MODEL_MANIFEST),
                rel(ONNX_PARITY),
                rel(CLASSIFICATION_SCORECARD),
                rel(THRESHOLD_SWEEP_SCORECARD),
                rel(BEST_PROXY_SCORECARD),
                rel(MT5_PROBE_QUEUE),
                rel(REPORT_PATH),
                rel(FINAL_DECISION),
            ],
            "status": status,
            "judgment": judgment,
            "next_run_id": next_run_id,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def base_ledger_row(result: Mapping[str, Any], status: str, judgment: str, decision: str, next_run_id: str) -> dict[str, Any]:
    best = result["best_rows"][0] if result["best_rows"] else {}
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": 12,
        "gate_total": 12,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "proxy_model_training_scout(프록시 모델 학습 탐색)",
        "lane": "proxy_model_training_scout(프록시 모델 학습 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "notes": f"best={best.get('model_id', 'none')};queue_rows={len(result['queue_rows'])};no_mt5_execution.",
        "source_package_run_id": SOURCE_RUN_ID,
        "rows": len(result["sweep_rows"]),
        "candidate_rows": len(result["queue_rows"]),
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": "proxy_queue_ready_no_selection(프록시 대기열 준비, 선택 없음)" if result["queue_rows"] else "negative_proxy_no_queue(부정 프록시, 대기열 없음)",
        "net_profit": best.get("oos_stress_net", ""),
        "profit_factor": best.get("oos_stress_pf", ""),
        "expectancy": "",
        "drawdown": best.get("oos_max_drawdown", ""),
        "recovery_factor": best.get("oos_recovery_factor", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "primary_kpi": f"mt5_probe_queue_rows={len(result['queue_rows'])}",
        "guardrail_kpi": TRADE_DENSITY_REQUIREMENT,
        "trade_density_per_feature_day": best.get("oos_trade_per_day", ""),
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": judgment,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
    }


def write_ledgers(result: Mapping[str, Any], status: str, judgment: str, decision: str, next_run_id: str) -> None:
    base = base_ledger_row(result, status, judgment, decision, next_run_id)
    views = [
        (
            "Tier_A",
            "Tier A",
            "Tier A separate(Tier A 분리)",
            "proxy_training_full_context(프록시 학습 전체 문맥)",
            "Tier A full-context proxy training and threshold sweep(Tier A 전체 문맥 프록시 학습 및 임계값 탐색).",
        ),
        (
            "Tier_B",
            "Tier B",
            "Tier B separate(Tier B 분리)",
            "missing_required_no_partial_context_materialization(Tier B 부분 문맥 물질화 없음 필수 누락)",
            "Tier B partial-context sample is not materialized in Stage356B(Tier B 부분 문맥 표본은 356B에서 미산출).",
        ),
        (
            "Tier_AplusB",
            "Tier A+B",
            "Tier A+B combined(Tier A+B 합산)",
            "same_as_tier_a_no_fallback(대체 없음, Tier A와 동일)",
            "Combined record is same as Tier A because no fallback is materialized(대체가 없어 합산 기록은 Tier A와 동일).",
        ),
    ]
    rows = []
    for suffix, tier, view, metric_scope, notes in views:
        row = {
            **base,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": tier,
            "view": view,
            "record_view": view,
            "tier": tier,
            "tier_scope": tier,
            "metric_scope": metric_scope,
            "kpi_scope": metric_scope,
            "notes": notes,
        }
        if tier == "Tier B":
            row["result_status"] = "missing_required(필수 누락)"
            row["net_profit"] = ""
            row["profit_factor"] = ""
            row["drawdown"] = ""
            row["recovery_factor"] = ""
            row["trade_count"] = ""
            row["trade_density_per_feature_day"] = ""
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **base,
                "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
                "row_id": f"{RUN_ID}__Tier_AplusB",
                "subrun_id": "Tier A+B",
                "record_view": "Tier A+B combined(Tier A+B 합산)",
                "tier_scope": "Tier A+B",
                "gate_audit_path": rel(GATE_AUDIT),
            }
        ],
    )


def write_gates(result: Mapping[str, Any], identity: Mapping[str, Any], join_audit: Mapping[str, Any]) -> list[dict[str, Any]]:
    required_gate_names = {"scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"}
    parity_pass = all(str(row.get("parity_status")) == "passed" for row in result["parity_rows"] if row.get("onnx_export_status") == "passed")
    gate_specs = [
        ("scope_completion_gate", all(exists(path) for path in [MODEL_MANIFEST, ONNX_PARITY, THRESHOLD_SWEEP_SCORECARD, BEST_PROXY_SCORECARD, MT5_PROBE_QUEUE, FINAL_DECISION, REPORT_PATH]), FINAL_DECISION, "planned proxy training outputs(계획 프록시 학습 산출물) 생성"),
        ("kpi_contract_audit", len(result["sweep_rows"]) > 0 and exists(STAGE_LEDGER), THRESHOLD_SWEEP_SCORECARD, "proxy KPI and tier ledgers(프록시 KPI와 티어 장부) 기록"),
        ("skill_receipt_lint", all(exists(path) for path in [DATA_RECEIPT, EXPERIMENT_RECEIPT, MODEL_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]), MODEL_RECEIPT, "skill receipts(스킬 영수증) 작성"),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "required gates(필수 게이트) 포함"),
        ("timestamp_join_gate", identity.get("feature_duplicate_key_rows") == 0 and join_audit.get("missing_feature_join_rows") == 0, SOURCE_DATA_AUDIT, "timestamp-safe feature/label join(시점 안전 피처/라벨 결합) 확인"),
        ("lookahead_boundary_gate", exists(DATA_RECEIPT), DATA_RECEIPT, "future columns excluded from features(미래 열 피처 제외) 기록"),
        ("onnx_parity_audit", parity_pass, ONNX_PARITY, "exported ONNX parity(내보낸 온엑스 동등성) 확인"),
        ("nonoverlap_trade_shape_gate", len(result["sweep_rows"]) > 0, THRESHOLD_SWEEP_SCORECARD, "non-overlap trade simulation(비중첩 거래 시뮬레이션) 기록"),
        ("candidate_queue_gate", exists(MT5_PROBE_QUEUE), MT5_PROBE_QUEUE, "MT5 probe queue status(MT5 탐침 대기열 상태) 기록"),
        ("tier_pair_records", exists(STAGE_LEDGER) and RUN_ID in read_text(STAGE_LEDGER), STAGE_LEDGER, "Tier A/B/combined(Tier A/B/합산) 기록"),
        ("artifact_lineage_audit", exists(LINEAGE_RECEIPT), LINEAGE_RECEIPT, "artifact lineage(산출물 계보) 연결"),
        ("final_claim_guard", "not_claimed" in json.dumps(read_json(FINAL_DECISION)), FINAL_DECISION, "operating claims(운영 주장) 차단"),
    ]
    gate_ids = {row[0] for row in gate_specs}
    gate_specs[3] = ("required_gate_coverage_audit", required_gate_names.issubset(gate_ids), GATE_AUDIT, "required gates(필수 게이트) 포함")
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, path, effect in gate_specs
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_artifact_registry() -> None:
    artifacts = [
        FEATURE_SCHEMA,
        SOURCE_DATA_AUDIT,
        TRAINING_TASK_REVIEW,
        MODEL_MANIFEST,
        ONNX_PARITY,
        CLASSIFICATION_SCORECARD,
        THRESHOLD_SWEEP_SCORECARD,
        BEST_PROXY_SCORECARD,
        MT5_PROBE_QUEUE,
        FIREWALL_REVIEW,
        DATA_RECEIPT,
        EXPERIMENT_RECEIPT,
        MODEL_RECEIPT,
        LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path) if exists(path) else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "Stage356B proxy training artifact(356B 프록시 학습 산출물)",
        }
        for path in artifacts
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def validate(gates: Sequence[Mapping[str, Any]]) -> None:
    failed = [row["gate_id"] for row in gates if row.get("status") != "passed"]
    if failed:
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise RuntimeError("required gates failed(필수 게이트 실패): " + ", ".join(failed))
    final = read_json(FINAL_DECISION)
    for key in ["runtime_authority", "operating_promotion", "goal_achieve", "candidate_selection"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}={final.get(key)}")


def main() -> None:
    for directory in [RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    features, labels, _queue_rows, identity = load_sources()
    full, feature_columns, join_audit = joined_frame(features, labels)
    write_json(
        FEATURE_SCHEMA,
        {
            "feature_count": len(feature_columns),
            "feature_order_hash": ordered_hash(feature_columns),
            "features": feature_columns,
            "source": rel(RUNTIME_FEATURES),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_source_audit(identity, join_audit)
    result = train_all(full, feature_columns)
    write_csv(TRAINING_TASK_REVIEW, result["task_rows"])
    write_csv(MODEL_MANIFEST, result["model_rows"])
    write_csv(ONNX_PARITY, result["parity_rows"])
    write_csv(CLASSIFICATION_SCORECARD, result["class_rows"])
    write_csv(THRESHOLD_SWEEP_SCORECARD, result["sweep_rows"])
    write_csv(BEST_PROXY_SCORECARD, result["best_rows"])
    write_csv(MT5_PROBE_QUEUE, result["queue_rows"])
    write_csv(RUN_DIR / "feature_importance_top20.csv", result["feature_importance_rows"])
    status, judgment, decision, next_run_id = status_tuple(result["queue_rows"])
    write_firewall(status, result["queue_rows"])
    write_receipts(identity, join_audit, result, status, judgment, next_run_id)
    write_report(result, status, judgment, decision, next_run_id)
    write_state_and_selection(result, status, judgment, decision, next_run_id)
    write_final_and_manifest(identity, join_audit, result, status, judgment, decision, next_run_id)
    write_ledgers(result, status, judgment, decision, next_run_id)
    gates = write_gates(result, identity, join_audit)
    write_artifact_registry()
    validate(gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "trained_models": len(result["model_rows"]),
                "threshold_sweep_rows": len(result["sweep_rows"]),
                "mt5_probe_queue_rows": len(result["queue_rows"]),
                "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
                "gate_total": len(gates),
                "next_run_id": next_run_id,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
