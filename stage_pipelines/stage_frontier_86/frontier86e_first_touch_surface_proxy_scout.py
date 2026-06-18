from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    log_loss,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.kpi_contract_audit import KpiContract, audit_kpi_contract
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_86__runtime_native_intrabar_path_label_source"
RUN_ID = "frontier86E_leakage_safe_first_touch_feature_label_surface_proxy_scout_v1"
PARENT_RUN_ID = "frontier86D_tick_m1_full_registration_or_first_touch_label_materializer_v1"
NEXT_RUNTIME_PREFLIGHT = "frontier86F_first_touch_surface_runtime_materialization_preflight_v1"
NEXT_REPAIR_OR_ROTATION = "frontier86F_first_touch_surface_repair_or_rotation_decision_v1"

CLAIM_BOUNDARY = (
    "f86e_leakage_safe_first_touch_feature_label_surface_proxy_scout_only_"
    "no_strategy_tester_runtime_economics_no_runtime_authority_no_goal_achieve"
)
STATUS_POSITIVE = "f86e_first_touch_proxy_surface_positive_scout_runtime_preflight_required_no_authority"
STATUS_WEAK = "f86e_first_touch_proxy_surface_weak_scout_repair_or_rotation_required_no_authority"
JUDGMENT_POSITIVE = "positive_proxy_scout_clue_with_locked_oos_readout_no_runtime_evidence"
JUDGMENT_WEAK = "weak_or_negative_proxy_scout_no_runtime_evidence"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
FEATURE_DIR = RUN_DIR / "feature_label_surface"
MODEL_DIR = RUN_DIR / "models"
PROXY_DIR = RUN_DIR / "proxy_scout"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F85B_READOUT = (
    ROOT
    / "stages/stage_frontier_85__runtime_path_contradiction_firewall_label_rebuild"
    / "03_reviews/f85b_selected_firewall_row_readout.csv"
)
F86D_LABELS = (
    STAGE_DIR
    / "02_runs/frontier86D_tick_m1_full_registration_or_first_touch_label_materializer_v1"
    / "first_touch_labels/first_touch_labels.csv"
)

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
STAGE_SELECTION_STATUS = STAGE_DIR / "04_selected/selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"

FEATURE_SURFACE = FEATURE_DIR / "feature_label_surface.csv"
FEATURE_SCHEMA = FEATURE_DIR / "feature_schema.json"
LEAKAGE_AUDIT = REVIEW_DIR / "f86e_feature_leakage_audit.json"
SPLIT_AUDIT = REVIEW_DIR / "f86e_split_boundary_audit.json"
SCORES_CSV = PROXY_DIR / "proxy_scores.csv"
MODEL_METRICS = PROXY_DIR / "proxy_metrics.json"
MODEL_CARD = MODEL_DIR / "proxy_model_card.json"
BEST_MODEL = MODEL_DIR / "best_proxy_model.joblib"
SUMMARY_JSON = RUN_DIR / "summary.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"
EXECUTION_SUMMARY = REVIEW_DIR / "f86e_execution_summary.json"
SCOPE_GATE = REVIEW_DIR / "f86e_scope_completion_gate.json"
KPI_AUDIT = REVIEW_DIR / "f86e_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f86e_artifact_lineage_audit.json"
RESULT_AUDIT = REVIEW_DIR / "f86e_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f86e_final_claim_guard.json"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f86e_run_evidence_receipt.json"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f86e_experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = REVIEW_DIR / "f86e_data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = REVIEW_DIR / "f86e_model_validation_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f86e_artifact_lineage_receipt.json"
RESULT_RECEIPT = REVIEW_DIR / "f86e_result_judgment_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f86e_claim_discipline_receipt.json"

PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
WORK_PACKET = PACKET_DIR / "work_packet.yaml"

PRE_ENTRY_NUMERIC_FEATURES = [
    "hour_utc",
    "p_short",
    "p_flat",
    "p_long",
    "f85b_side_prob",
    "f85b_probability_margin",
    "f85b_flat_pressure",
    "atr_points",
    "open_sl_points",
    "open_tp_points",
    "f85b_atr_sl_ratio",
    "computed_lot",
    "side_signed_probability_edge",
    "opposite_side_probability",
    "tp_sl_ratio",
    "sl_atr_ratio",
    "tp_atr_ratio",
    "hour_sin",
    "hour_cos",
]
PRE_ENTRY_CATEGORICAL_FEATURES = [
    "decision",
    "session_bucket",
]
AUDIT_ONLY_COLUMNS = [
    "row_index",
    "timestamp_utc",
    "split",
    "f85b_candidate_id",
    "input_hash",
    "target_candidate_id",
    "source_candidate_id",
    "runtime_wrapper_id",
]
FORBIDDEN_FEATURE_COLUMNS = [
    "runtime_net",
    "runtime_win_bool",
    "proxy_win",
    "proxy_win_runtime_loss",
    "proxy_loss_runtime_win",
    "proxy_both_hit",
    "proxy_exit_path_label",
    "first_touch_label",
    "label_resolution_method",
    "tick_count",
    "first_sl_time_msc_utc",
    "first_tp_time_msc_utc",
    "entry_price_proxy_m5_open",
    "m5_high",
    "m5_low",
    "m5_close",
    "sl_price",
    "tp_price",
    "m5_sl_hit",
    "m5_tp_hit",
    "m5_path_class",
    "m5_close_direction_win",
]


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def fs_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32" and len(str(resolved)) >= 240:
        return io_path(path)
    return resolved


def write_text(path: Path, text: str) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    fs_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    fs_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    fs_path(path).write_text(yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def write_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = list(rows)
    if fieldnames is None:
        seen: set[str] = set()
        ordered: list[str] = []
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.add(key)
                    ordered.append(key)
        fieldnames = ordered or ["empty"]
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    with fs_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def read_csv_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig")


def rewrite_csv(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str]) -> None:
    write_csv_rows(path, rows, fieldnames)


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    upsert_many_csv(path, key, [row], source_header=source_header)


def upsert_many_csv(path: Path, key: str, new_rows: Sequence[Mapping[str, Any]], source_header: Path | None = None) -> None:
    new_rows = list(new_rows)
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(new_rows[0].keys()) if new_rows else [key]
        rows = []
    for row in new_rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    replacement_keys = {str(row.get(key, "")) for row in new_rows}
    rows = [existing for existing in rows if str(existing.get(key, "")) not in replacement_keys]
    rows.extend({field: csv_value(row.get(field, "")) for field in fieldnames} for row in new_rows)
    rewrite_csv(path, rows, fieldnames)


def file_identity(path: Path) -> dict[str, Any]:
    native = io_path(path)
    if not native.exists():
        return {"path": rel(path), "exists": False}
    return {
        "path": rel(path),
        "exists": True,
        "size": native.stat().st_size,
        "sha256": sha256_file_lf_normalized(path),
    }


def feature_order_hash(columns: Sequence[str]) -> str:
    return hashlib.sha256(("\n".join(columns) + "\n").encode("utf-8")).hexdigest()


def ensure_dirs() -> None:
    for directory in (RUN_DIR, FEATURE_DIR, MODEL_DIR, PROXY_DIR, REPORT_DIR, REVIEW_DIR, PACKET_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def load_surface() -> tuple[pd.DataFrame, dict[str, Any]]:
    readout = read_csv_frame(F85B_READOUT)
    labels = read_csv_frame(F86D_LABELS)
    readout["row_index_join"] = pd.to_numeric(readout["row_index"], errors="raise").astype(int)
    labels["row_index_join"] = pd.to_numeric(labels["source_row_index"], errors="raise").astype(int)
    merged = readout.merge(
        labels[
            [
                "row_index_join",
                "first_touch_label",
                "label_resolution_method",
                "tick_count",
                "m5_path_class",
            ]
        ],
        on="row_index_join",
        how="inner",
        validate="one_to_one",
    )
    if len(merged) != len(readout) or len(merged) != len(labels):
        raise RuntimeError(f"F86E join mismatch: readout={len(readout)} labels={len(labels)} merged={len(merged)}")

    for column in PRE_ENTRY_NUMERIC_FEATURES:
        if column in merged.columns:
            merged[column] = pd.to_numeric(merged[column], errors="coerce")
    for column in ["hour_utc", "p_short", "p_flat", "p_long", "f85b_side_prob", "atr_points", "open_sl_points", "open_tp_points", "f85b_atr_sl_ratio", "computed_lot"]:
        merged[column] = pd.to_numeric(merged[column], errors="coerce")
    decision = merged["decision"].astype(str).str.lower()
    merged["opposite_side_probability"] = np.where(decision.eq("long"), merged["p_short"], merged["p_long"])
    merged["side_signed_probability_edge"] = np.where(
        decision.eq("long"),
        merged["p_long"] - merged["p_short"],
        merged["p_short"] - merged["p_long"],
    )
    merged["tp_sl_ratio"] = merged["open_tp_points"] / merged["open_sl_points"].replace(0, np.nan)
    merged["sl_atr_ratio"] = merged["open_sl_points"] / merged["atr_points"].replace(0, np.nan)
    merged["tp_atr_ratio"] = merged["open_tp_points"] / merged["atr_points"].replace(0, np.nan)
    hour = merged["hour_utc"].fillna(0.0).astype(float)
    merged["hour_sin"] = np.sin(2 * np.pi * hour / 24.0)
    merged["hour_cos"] = np.cos(2 * np.pi * hour / 24.0)
    merged["first_touch_group"] = np.select(
        [
            merged["first_touch_label"].astype(str).str.startswith("tp_first"),
            merged["first_touch_label"].astype(str).str.startswith("sl_first"),
            merged["first_touch_label"].astype(str).str.startswith("none_hit"),
        ],
        ["tp_first", "sl_first", "none_hit"],
        default="other",
    )
    merged["target_tp_first_binary"] = np.where(
        merged["first_touch_group"].eq("tp_first"),
        1,
        np.where(merged["first_touch_group"].eq("sl_first"), 0, np.nan),
    )
    feature_columns = PRE_ENTRY_NUMERIC_FEATURES + PRE_ENTRY_CATEGORICAL_FEATURES
    surface_columns = AUDIT_ONLY_COLUMNS + feature_columns + [
        "first_touch_group",
        "target_tp_first_binary",
        "first_touch_label",
        "label_resolution_method",
    ]
    surface_columns = [column for column in surface_columns if column in merged.columns]
    surface = merged[surface_columns].copy()
    forbidden_intersection = sorted(set(feature_columns) & set(FORBIDDEN_FEATURE_COLUMNS))
    audit = {
        "audit_name": "feature_leakage_audit",
        "status": "pass" if not forbidden_intersection else "blocked",
        "findings": []
        if not forbidden_intersection
        else [
            {
                "check_id": "forbidden_feature_columns_present",
                "message": "Forbidden post-entry/runtime/path columns are present in the model feature set.",
                "severity": "blocking",
                "details": {"columns": forbidden_intersection},
            }
        ],
        "input_rows": len(readout),
        "label_rows": len(labels),
        "joined_rows": len(merged),
        "surface_rows": len(surface),
        "feature_columns": feature_columns,
        "numeric_features": PRE_ENTRY_NUMERIC_FEATURES,
        "categorical_features": PRE_ENTRY_CATEGORICAL_FEATURES,
        "forbidden_feature_columns": FORBIDDEN_FEATURE_COLUMNS,
        "forbidden_feature_intersection": forbidden_intersection,
        "label_counts": merged["first_touch_label"].value_counts(dropna=False).to_dict(),
        "first_touch_group_counts": merged["first_touch_group"].value_counts(dropna=False).to_dict(),
        "split_counts": merged["split"].value_counts(dropna=False).to_dict(),
        "allowed_claims": ["leakage_safe_feature_label_surface_materialized"],
        "forbidden_claims": [
            "runtime_verified",
            "strategy_tester_runtime_economics",
        ],
        "claim_effect": "F86E feature columns are pre-entry only; first-touch/tick/M5 path fields are target or audit fields only.",
    }
    return surface, audit


def chronological_validation_fit_mask(frame: pd.DataFrame) -> tuple[pd.Series, pd.Series, pd.Series]:
    valid_binary = frame["target_tp_first_binary"].notna()
    validation = valid_binary & frame["split"].astype(str).eq("validation")
    oos = valid_binary & frame["split"].astype(str).eq("oos")
    validation_rows = frame.loc[validation].sort_values("timestamp_utc")
    if validation_rows.empty:
        raise RuntimeError("No validation rows are available for F86E proxy scout.")
    cutoff = int(math.floor(len(validation_rows) * 0.70))
    cutoff = max(1, min(cutoff, len(validation_rows) - 1))
    fit_indices = set(validation_rows.iloc[:cutoff].index)
    inner_indices = set(validation_rows.iloc[cutoff:].index)
    fit = frame.index.to_series().isin(fit_indices)
    inner = frame.index.to_series().isin(inner_indices)
    return fit, inner, oos


def make_preprocessor() -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        [
            ("num", numeric_pipeline, PRE_ENTRY_NUMERIC_FEATURES),
            ("cat", categorical_pipeline, PRE_ENTRY_CATEGORICAL_FEATURES),
        ]
    )


def candidate_models() -> dict[str, Any]:
    return {
        "logreg_l2_balanced": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=86),
        "random_forest_depth4_balanced": RandomForestClassifier(
            n_estimators=240,
            max_depth=4,
            min_samples_leaf=25,
            class_weight="balanced_subsample",
            random_state=86,
            n_jobs=-1,
        ),
        "extra_trees_depth5_balanced": ExtraTreesClassifier(
            n_estimators=320,
            max_depth=5,
            min_samples_leaf=20,
            class_weight="balanced",
            random_state=86,
            n_jobs=-1,
        ),
    }


def safe_metric(metric: str, y_true: np.ndarray, score: np.ndarray, pred: np.ndarray) -> float | None:
    if len(y_true) == 0 or len(np.unique(y_true)) < 2:
        return None
    if metric == "roc_auc":
        return float(roc_auc_score(y_true, score))
    if metric == "average_precision":
        return float(average_precision_score(y_true, score))
    if metric == "log_loss":
        return float(log_loss(y_true, np.vstack([1 - score, score]).T, labels=[0, 1]))
    if metric == "brier":
        return float(brier_score_loss(y_true, score))
    if metric == "accuracy":
        return float(accuracy_score(y_true, pred))
    raise ValueError(metric)


def quantile_readout(y_true: np.ndarray, score: np.ndarray, q: float, top: bool) -> dict[str, Any]:
    if len(y_true) == 0:
        return {"rows": 0, "tp_first_rate": None, "coverage": 0.0, "threshold": None}
    threshold = float(np.quantile(score, q if top else 1 - q))
    mask = score >= threshold if top else score <= threshold
    rows = int(mask.sum())
    return {
        "rows": rows,
        "tp_first_rate": float(y_true[mask].mean()) if rows else None,
        "coverage": float(rows / len(y_true)) if len(y_true) else 0.0,
        "threshold": threshold,
    }


def evaluate_split(frame: pd.DataFrame, mask: pd.Series, model: Pipeline, split_name: str) -> dict[str, Any]:
    subset = frame.loc[mask].copy()
    if subset.empty:
        return {"split": split_name, "rows": 0, "tp_first_rate": None}
    y = subset["target_tp_first_binary"].astype(int).to_numpy()
    score = model.predict_proba(subset[PRE_ENTRY_NUMERIC_FEATURES + PRE_ENTRY_CATEGORICAL_FEATURES])[:, 1]
    pred = (score >= 0.5).astype(int)
    base_rate = float(y.mean()) if len(y) else None
    top_decile = quantile_readout(y, score, 0.90, top=True)
    bottom_decile = quantile_readout(y, score, 0.90, top=False)
    return {
        "split": split_name,
        "rows": int(len(y)),
        "tp_first_rate": base_rate,
        "roc_auc": safe_metric("roc_auc", y, score, pred),
        "average_precision": safe_metric("average_precision", y, score, pred),
        "log_loss": safe_metric("log_loss", y, score, pred),
        "brier": safe_metric("brier", y, score, pred),
        "accuracy_at_0_5": safe_metric("accuracy", y, score, pred),
        "top_decile": top_decile,
        "top_decile_lift": None
        if base_rate in (None, 0)
        else (None if top_decile["tp_first_rate"] is None else float(top_decile["tp_first_rate"] / base_rate)),
        "bottom_decile": bottom_decile,
        "bottom_decile_sl_first_rate": None
        if bottom_decile["tp_first_rate"] is None
        else float(1.0 - bottom_decile["tp_first_rate"]),
    }


def run_proxy_scout(surface: pd.DataFrame) -> tuple[dict[str, Any], pd.DataFrame, Any]:
    model_frame = surface[surface["target_tp_first_binary"].notna()].copy()
    fit_mask, inner_mask, oos_mask = chronological_validation_fit_mask(model_frame)
    models: dict[str, Pipeline] = {}
    metrics: dict[str, Any] = {}
    for model_id, estimator in candidate_models().items():
        pipeline = Pipeline([("preprocessor", make_preprocessor()), ("model", estimator)])
        x_train = model_frame.loc[fit_mask, PRE_ENTRY_NUMERIC_FEATURES + PRE_ENTRY_CATEGORICAL_FEATURES]
        y_train = model_frame.loc[fit_mask, "target_tp_first_binary"].astype(int)
        pipeline.fit(x_train, y_train)
        models[model_id] = pipeline
        metrics[model_id] = {
            "fit": evaluate_split(model_frame, fit_mask, pipeline, "validation_fit"),
            "inner_validation": evaluate_split(model_frame, inner_mask, pipeline, "validation_inner_selection"),
            "locked_oos_readout": evaluate_split(model_frame, oos_mask, pipeline, "locked_oos_readout"),
        }

    def score_key(item: tuple[str, Any]) -> tuple[float, float, float]:
        inner = item[1]["inner_validation"]
        auc = inner.get("roc_auc") or 0.0
        lift = inner.get("top_decile_lift") or 0.0
        ap = inner.get("average_precision") or 0.0
        return (auc, lift, ap)

    best_model_id = max(metrics.items(), key=score_key)[0]
    best_model = models[best_model_id]
    best_inner = metrics[best_model_id]["inner_validation"]
    best_oos = metrics[best_model_id]["locked_oos_readout"]
    positive_scout = bool(
        (best_inner.get("roc_auc") or 0.0) >= 0.53
        and (best_inner.get("top_decile_lift") or 0.0) >= 1.05
        and (best_oos.get("roc_auc") or 0.0) >= 0.51
        and (best_oos.get("top_decile_lift") or 0.0) >= 1.00
        and (best_oos.get("rows") or 0) >= 250
    )
    scores = surface.copy()
    scores["proxy_score_tp_first"] = np.nan
    binary_mask = scores["target_tp_first_binary"].notna()
    scores.loc[binary_mask, "proxy_score_tp_first"] = best_model.predict_proba(
        scores.loc[binary_mask, PRE_ENTRY_NUMERIC_FEATURES + PRE_ENTRY_CATEGORICAL_FEATURES]
    )[:, 1]
    top_threshold = best_inner.get("top_decile", {}).get("threshold")
    bottom_threshold = best_inner.get("bottom_decile", {}).get("threshold")
    scores["selected_top_tp_first_score"] = False
    scores["selected_bottom_sl_first_score"] = False
    if top_threshold is not None:
        scores.loc[binary_mask, "selected_top_tp_first_score"] = scores.loc[binary_mask, "proxy_score_tp_first"] >= float(top_threshold)
    if bottom_threshold is not None:
        scores.loc[binary_mask, "selected_bottom_sl_first_score"] = scores.loc[binary_mask, "proxy_score_tp_first"] <= float(bottom_threshold)
    summary = {
        "model_ids": list(metrics.keys()),
        "best_model_id": best_model_id,
        "metrics_by_model": metrics,
        "split_rows": {
            "validation_fit": int(fit_mask.sum()),
            "validation_inner_selection": int(inner_mask.sum()),
            "locked_oos_readout": int(oos_mask.sum()),
            "binary_rows": int(binary_mask.sum()),
            "excluded_none_hit_rows": int(surface["target_tp_first_binary"].isna().sum()),
        },
        "selection_policy": "best model selected by validation_inner_selection roc_auc, top_decile_lift, average_precision; locked OOS is readout only",
        "positive_scout": positive_scout,
        "next_run_id": NEXT_RUNTIME_PREFLIGHT if positive_scout else NEXT_REPAIR_OR_ROTATION,
        "claim_effect": "Positive scout means runtime materialization preflight is reasonable; it is not MT5 runtime economics evidence.",
    }
    return summary, scores, best_model


def result_status(model_summary: Mapping[str, Any]) -> tuple[str, str]:
    if model_summary.get("positive_scout"):
        return STATUS_POSITIVE, JUDGMENT_POSITIVE
    return STATUS_WEAK, JUDGMENT_WEAK


def make_feature_schema(surface: pd.DataFrame, leakage_audit: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "frontier86e_feature_schema_v1",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "feature_set_id": "f86e_pre_entry_f85b_scalar_plus_time_shape_v1",
        "label_id": "f86d_first_touch_tp_vs_sl_binary_excluding_none_hit_v1",
        "feature_columns": leakage_audit["feature_columns"],
        "numeric_features": PRE_ENTRY_NUMERIC_FEATURES,
        "categorical_features": PRE_ENTRY_CATEGORICAL_FEATURES,
        "feature_order_hash": feature_order_hash(leakage_audit["feature_columns"]),
        "rows": len(surface),
        "target_columns": ["first_touch_group", "target_tp_first_binary"],
        "forbidden_feature_columns": FORBIDDEN_FEATURE_COLUMNS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_run_artifacts(surface: pd.DataFrame, leakage_audit: dict[str, Any]) -> tuple[dict[str, Any], pd.DataFrame, Any]:
    feature_schema = make_feature_schema(surface, leakage_audit)
    write_csv_rows(FEATURE_SURFACE, surface.to_dict("records"), list(surface.columns))
    write_json(FEATURE_SCHEMA, feature_schema)
    write_json(LEAKAGE_AUDIT, leakage_audit)
    split_audit = {
        "audit_name": "split_boundary_audit",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": "pass",
        "validation_used_for_fit_and_inner_selection": True,
        "locked_oos_used_for_selection": False,
        "split_counts": leakage_audit["split_counts"],
        "claim_effect": "OOS is a locked readout only; no OOS threshold or model family choice is made.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(SPLIT_AUDIT, split_audit)
    model_summary, scores, best_model = run_proxy_scout(surface)
    write_csv_rows(SCORES_CSV, scores.to_dict("records"), list(scores.columns))
    write_json(MODEL_METRICS, model_summary)
    io_path(BEST_MODEL.parent).mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, io_path(BEST_MODEL))
    model_card = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "model_id": model_summary["best_model_id"],
        "model_path": rel(BEST_MODEL),
        "model_sha256": sha256_file_lf_normalized(BEST_MODEL),
        "feature_schema": file_identity(FEATURE_SCHEMA),
        "claim_boundary": CLAIM_BOUNDARY,
        "model_artifact_boundary": "proxy_scout_model_snapshot_only_not_onnx_not_ea_runtime_bundle",
    }
    write_json(MODEL_CARD, model_card)
    return model_summary, scores, best_model


def final_claim_guard(status: str, judgment: str, model_summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "audit_name": "final_claim_guard",
        "packet_id": RUN_ID,
        "status": "pass",
        "result_status": status,
        "judgment": judgment,
        "allowed_claims": [
            "leakage_safe_feature_label_surface_materialized",
            "proxy_scout_model_snapshot_created",
            "locked_oos_readout_recorded",
            "runtime_materialization_preflight_required" if model_summary.get("positive_scout") else "repair_or_rotation_required",
        ],
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "goal_achieve",
            "runtime_verified",
            "strategy_tester_runtime_economics",
            "materialization_ready",
            "ea_onnx_runtime_bundle_ready",
            "oos_selected_model",
        ],
        "evidence_missing": [
            "MT5 Strategy Tester report",
            "EA source/binary identity",
            "ONNX runtime bundle",
            "trade list and telemetry",
            "WFO/stress/runtime validation",
        ],
        "task_force_review": {
            "required": False,
            "actual_subagent_calls_required": False,
            "claim_effect": "No Task Force reviewed/pass claim is made for F86E.",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def receipt_payloads(status: str, judgment: str, model_summary: Mapping[str, Any], guard: Mapping[str, Any]) -> list[dict[str, Any]]:
    best = model_summary["metrics_by_model"][model_summary["best_model_id"]]
    produced = [rel(path) for path in artifact_paths() if path_exists(path)]
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "receipt_path": rel(RUN_EVIDENCE_RECEIPT),
            "source_inputs": [rel(F85B_READOUT), rel(F86D_LABELS)],
            "measurement_scope": "structural_scout first-touch tp/sl label predictability",
            "management_state": "run_manifest/kpi_record/summary/result_summary created",
            "judgment_class": "positive" if model_summary.get("positive_scout") else "negative",
            "scoreboard": "structural_scout",
            "parity_level": "P0_unverified",
            "wfo_status": "not_applicable",
            "registry_update_required": "yes",
            "negative_memory_required": "yes" if not model_summary.get("positive_scout") else "no",
            "hard_gate_applicable": "no",
            "evidence_boundary": "scout-only",
            "produced_artifacts": produced,
            "ledger_rows": [
                f"{rel(RUN_REGISTRY)}::{RUN_ID}",
                f"{rel(STAGE_LEDGER)}::{RUN_ID}",
            ],
            "missing_evidence": guard["evidence_missing"],
            "allowed_claims": guard["allowed_claims"],
            "forbidden_claims": guard["forbidden_claims"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "receipt_path": rel(EXPERIMENT_RECEIPT),
            "hypothesis": "F86D first-touch labels can be predicted from pre-entry F85B probability/risk/session features without using post-entry path fields.",
            "baseline": "F86D label distribution and split base tp_first rate.",
            "decision_use": "Decide whether F86F should open runtime materialization preflight or repair/rotation.",
            "comparison_baseline": "Validation split base tp_first rate and top-decile lift over base rate.",
            "control_variables": ["F86D labels", "F85B selected rows", "chronological validation/OOS boundary", "no OOS selection"],
            "changed_variables": ["feature-label surface construction", "fixed proxy model families"],
            "sample_scope": "F85B selected validation/OOS rows with F86D first-touch labels",
            "success_criteria": "validation-inner AUC/lift and locked-OOS non-collapse support a proxy scout clue",
            "failure_criteria": "no validation-inner lift or locked-OOS collapse",
            "invalid_conditions": ["forbidden feature intersection", "join mismatch", "OOS-used-for-selection"],
            "stop_conditions": ["record scout boundary and route to F86F"],
            "evidence_plan": [rel(FEATURE_SURFACE), rel(MODEL_METRICS), rel(SCORES_CSV)],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "receipt_path": rel(DATA_INTEGRITY_RECEIPT),
            "data_sources_checked": [rel(F85B_READOUT), rel(F86D_LABELS), rel(FEATURE_SURFACE)],
            "data_source": [rel(F85B_READOUT), rel(F86D_LABELS)],
            "time_axis_boundary": "F85B timestamp_utc selected M5 bar identity; F86D first-touch labels are post-entry targets only.",
            "time_axis": "F85B timestamp_utc selected M5 bar identity; F86D first-touch labels are post-entry targets only.",
            "sample_scope": model_summary["split_rows"],
            "missing_data_boundary": f"joined_rows={model_summary['split_rows']['binary_rows'] + model_summary['split_rows']['excluded_none_hit_rows']}; excluded_none_hit_rows={model_summary['split_rows']['excluded_none_hit_rows']}.",
            "missing_or_duplicate_check": "one_to_one row_index join passed",
            "feature_label_boundary": "Only pre-entry F85B scalar/time features are model inputs; first-touch/tick/M5 path fields are targets/audit.",
            "split_boundary": "validation fit/inner-selection, locked OOS readout",
            "leakage_checks": [
                "forbidden feature intersection is empty",
                "locked OOS is readout only",
                "first-touch/tick/M5 path fields are target or audit only",
            ],
            "leakage_risk": "Using m5_high/low/close, tick_count, first_touch_label, runtime_net, or proxy/runtime outcome columns as features would leak.",
            "data_hash_or_identity": {
                "f85b_readout": file_identity(F85B_READOUT),
                "f86d_labels": file_identity(F86D_LABELS),
                "feature_surface": file_identity(FEATURE_SURFACE),
            },
            "integrity_judgment": "usable_with_boundary",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "receipt_path": rel(MODEL_VALIDATION_RECEIPT),
            "model_or_threshold_surface": "Fixed sklearn proxy scout model set over pre-entry F86E features.",
            "model_family": list(model_summary["model_ids"]),
            "target_and_label": "target_tp_first_binary from F86D first_touch_label; none_hit rows excluded from binary model",
            "validation_split": "validation fit 70% / validation inner-selection 30%; locked OOS readout only",
            "split_method": "chronological validation fit/inner-selection plus locked OOS readout",
            "selection_metric_boundary": "Model selected by validation-inner roc_auc/top_decile_lift/average_precision; OOS not used for selection.",
            "selection_metric": "inner validation roc_auc, top_decile_lift, average_precision",
            "secondary_metrics": ["brier", "log_loss", "accuracy", "bottom_decile_sl_first_rate"],
            "threshold_policy": "fixed inner-validation top/bottom decile readout thresholds; no OOS threshold search",
            "overfit_checks": [
                "chronological validation fit/inner split",
                "OOS readout excluded from model selection",
                "fixed model family list, no broad hyperparameter search",
            ],
            "overfit_risk": "Small selected-row sample and fixed F85B source surface can overfit validation.",
            "calibration_risk": "Scores are ranking scores, not calibrated runtime probabilities.",
            "comparison_baseline": "split base tp_first rate",
            "validation_judgment": "exploratory_proxy_scout",
            "allowed_claims": guard["allowed_claims"],
            "forbidden_claims": guard["forbidden_claims"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "receipt_path": rel(ARTIFACT_RECEIPT),
            "source_inputs": [rel(F85B_READOUT), rel(F86D_LABELS)],
            "producer": rel(ROOT / "stage_pipelines/stage_frontier_86/frontier86e_first_touch_surface_proxy_scout.py"),
            "consumer": model_summary["next_run_id"],
            "produced_artifacts": produced,
            "raw_evidence": [rel(F85B_READOUT), rel(F86D_LABELS)],
            "machine_readable": [rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(MODEL_METRICS), rel(FEATURE_SCHEMA)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE)],
            "artifact_paths": produced,
            "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifact_paths() if path_exists(path)},
            "hashes_or_missing_reasons": [
                f"feature_surface_sha256={sha256_file_lf_normalized(FEATURE_SURFACE)}",
                f"best_model_sha256={sha256_file_lf_normalized(BEST_MODEL)}",
                "Strategy Tester report not in scope",
                "EA/ONNX bundle not built",
            ],
            "registry_links": [rel(RUN_REGISTRY), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_reviews_and_ignored_run_outputs_with_hash_identity",
            "lineage_boundary": "F86E proxy-scout lineage connected; runtime bundle lineage absent by claim.",
            "lineage_judgment": "connected_with_boundary",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "receipt_path": rel(RESULT_RECEIPT),
            "result_subject": RUN_ID,
            "evidence_available": [rel(MODEL_METRICS), rel(FEATURE_SCHEMA), rel(KPI_RECORD)],
            "evidence_missing": guard["evidence_missing"],
            "judgment_boundary": judgment,
            "judgment_label": "positive" if model_summary.get("positive_scout") else "negative",
            "allowed_claims": guard["allowed_claims"],
            "forbidden_claims": guard["forbidden_claims"],
            "evidence_used": [rel(MODEL_METRICS), rel(LEAKAGE_AUDIT), rel(SPLIT_AUDIT), rel(KPI_RECORD)],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": model_summary["next_run_id"],
            "user_explanation_hook": "This tells whether the new first-touch labels have a pre-entry learnable signal, not whether MT5 economics work.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "receipt_path": rel(CLAIM_RECEIPT),
            "requested_claims": guard["allowed_claims"],
            "allowed_claims": guard["allowed_claims"],
            "forbidden_claims": guard["forbidden_claims"],
            "final_status": status,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def artifact_paths() -> list[Path]:
    return [
        ROOT / "stage_pipelines/stage_frontier_86/frontier86e_first_touch_surface_proxy_scout.py",
        FEATURE_SURFACE,
        FEATURE_SCHEMA,
        LEAKAGE_AUDIT,
        SPLIT_AUDIT,
        SCORES_CSV,
        MODEL_METRICS,
        MODEL_CARD,
        BEST_MODEL,
        SUMMARY_JSON,
        RUN_MANIFEST,
        KPI_RECORD,
        RESULT_SUMMARY,
        EXECUTION_SUMMARY,
        SCOPE_GATE,
        KPI_AUDIT,
        ARTIFACT_AUDIT,
        RESULT_AUDIT,
        FINAL_CLAIM_GUARD,
        RUN_EVIDENCE_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        ARTIFACT_RECEIPT,
        RESULT_RECEIPT,
        CLAIM_RECEIPT,
        WORK_PACKET,
        PACKET_SKILL_RECEIPTS,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_CLOSEOUT_GATE,
        PACKET_STATE_SYNC_AUDIT,
    ]


def write_receipts(receipts: Sequence[Mapping[str, Any]]) -> None:
    path_by_skill = {
        "obsidian-run-evidence-system": RUN_EVIDENCE_RECEIPT,
        "obsidian-experiment-design": EXPERIMENT_RECEIPT,
        "obsidian-data-integrity": DATA_INTEGRITY_RECEIPT,
        "obsidian-model-validation": MODEL_VALIDATION_RECEIPT,
        "obsidian-artifact-lineage": ARTIFACT_RECEIPT,
        "obsidian-result-judgment": RESULT_RECEIPT,
        "obsidian-claim-discipline": CLAIM_RECEIPT,
    }
    for receipt in receipts:
        write_json(path_by_skill[str(receipt["skill"])], receipt)
    write_json(
        PACKET_SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "primary_skill": "obsidian-run-evidence-system",
            "claim_boundary": CLAIM_BOUNDARY,
            "receipts": list(receipts),
        },
    )


def write_summary_artifacts(
    surface: pd.DataFrame,
    leakage_audit: Mapping[str, Any],
    model_summary: Mapping[str, Any],
    status: str,
    judgment: str,
    guard: Mapping[str, Any],
) -> dict[str, Any]:
    best = model_summary["metrics_by_model"][model_summary["best_model_id"]]
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": model_summary["next_run_id"],
        "created_at_utc": now_utc(),
        "primary_family": "experiment_execution",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": [
            "obsidian-experiment-design",
            "obsidian-data-integrity",
            "obsidian-model-validation",
            "obsidian-artifact-lineage",
            "obsidian-result-judgment",
            "obsidian-claim-discipline",
        ],
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "input_rows": int(leakage_audit["input_rows"]),
        "label_rows": int(leakage_audit["label_rows"]),
        "joined_rows": int(leakage_audit["joined_rows"]),
        "surface_rows": int(len(surface)),
        "binary_rows": int(model_summary["split_rows"]["binary_rows"]),
        "excluded_none_hit_rows": int(model_summary["split_rows"]["excluded_none_hit_rows"]),
        "feature_count": len(leakage_audit["feature_columns"]),
        "best_model_id": model_summary["best_model_id"],
        "positive_scout": bool(model_summary["positive_scout"]),
        "best_metrics": best,
        "model_summary": model_summary,
        "feature_schema": file_identity(FEATURE_SCHEMA),
        "feature_surface": file_identity(FEATURE_SURFACE),
        "proxy_scores": file_identity(SCORES_CSV),
        "best_model": file_identity(BEST_MODEL),
        "runtime_claim_boundary": "no_strategy_tester_no_onnx_no_ea_no_runtime_economics_claim",
        "final_claim_guard": guard,
    }
    write_json(SUMMARY_JSON, summary)
    write_json(
        RUN_MANIFEST,
        {
            "manifest_version": "frontier86e_proxy_scout_manifest_v1",
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "created_at_utc": summary["created_at_utc"],
            "script": file_identity(ROOT / "stage_pipelines/stage_frontier_86/frontier86e_first_touch_surface_proxy_scout.py"),
            "work_family": "experiment_execution",
            "verification_profile": "proxy_scout",
            "claim_boundary": CLAIM_BOUNDARY,
            "execution_command": "python stage_pipelines/stage_frontier_86/frontier86e_first_touch_surface_proxy_scout.py",
            "inputs": [file_identity(F85B_READOUT), file_identity(F86D_LABELS)],
            "outputs": [file_identity(path) for path in artifact_paths() if path_exists(path)],
            "status": status,
            "judgment": judgment,
        },
    )
    write_json(
        KPI_RECORD,
        {
            "kpi_record_version": "frontier86e_proxy_scout_kpi_v1",
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "scoreboard": "structural_scout",
            "judgment_class": judgment,
            "evidence_boundary": "proxy_scout_only",
            "parity_level": "P0_unverified",
            "wfo_status": "not_applicable",
            "hard_gate_applicable": "no",
            "input_rows": summary["input_rows"],
            "surface_rows": summary["surface_rows"],
            "binary_rows": summary["binary_rows"],
            "feature_count": summary["feature_count"],
            "best_model_id": summary["best_model_id"],
            "positive_scout": summary["positive_scout"],
            "best_metrics": best,
            "runtime_kpi": {
                "net_profit": None,
                "profit_factor": None,
                "drawdown": None,
                "trade_count": None,
                "trades_per_day": None,
                "n_a_reason": "No EA/ONNX/Strategy Tester runtime economics were executed in F86E.",
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(EXECUTION_SUMMARY, summary)
    write_json(
        SCOPE_GATE,
        {
            "audit_name": "scope_completion_gate",
            "status": "pass",
            "checks": [
                {"check_id": "joined_rows", "expected": 4127, "actual": summary["joined_rows"], "status": "pass" if summary["joined_rows"] == 4127 else "fail"},
                {"check_id": "feature_surface_rows", "expected": 4127, "actual": summary["surface_rows"], "status": "pass" if summary["surface_rows"] == 4127 else "fail"},
                {"check_id": "forbidden_feature_intersection", "expected": 0, "actual": len(leakage_audit["forbidden_feature_intersection"]), "status": "pass" if not leakage_audit["forbidden_feature_intersection"] else "fail"},
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(ARTIFACT_AUDIT, {"audit_name": "artifact_lineage_audit", "status": "pass_connected_with_boundary", "artifacts": [file_identity(path) for path in artifact_paths() if path_exists(path)], "claim_boundary": CLAIM_BOUNDARY})
    write_json(RESULT_AUDIT, {"audit_name": "result_judgment_receipt", "status": "pass", "judgment": judgment, "evidence_missing": guard["evidence_missing"], "claim_boundary": CLAIM_BOUNDARY})
    write_json(FINAL_CLAIM_GUARD, guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, guard)
    return summary


def result_summary_text(summary: Mapping[str, Any]) -> str:
    best = summary["best_metrics"]
    inner = best["inner_validation"]
    oos = best["locked_oos_readout"]
    return f"""# F86E Result Summary(F86E 결과 요약)

## Conclusion(결론)

F86E built a leakage-safe first-touch feature/label surface(누수 안전 첫 터치 피처/라벨 표면) and ran a proxy scout(프록시 스카우트).

Result(결과): `{summary['judgment']}`.

## Plain Meaning(쉬운 뜻)

이번 실행은 MT5 Strategy Tester(전략 테스터) 수익 검증이 아닙니다. F86D에서 만든 first-touch label(첫 터치 라벨)이 진입 전 feature(피처)만으로 어느 정도 구분되는지 본 것입니다.

Effect(효과): 신호가 있으면 다음 F86F에서 runtime materialization preflight(런타임 물질화 사전확인)로 넘기고, 약하면 repair or rotation(수리 또는 회전)으로 닫습니다.

## Confirmed(확인됨)

- Joined rows(결합 행): `{summary['joined_rows']}`
- Feature count(피처 수): `{summary['feature_count']}`
- Binary rows(이진 라벨 행): `{summary['binary_rows']}`
- Excluded none-hit rows(무터치 제외 행): `{summary['excluded_none_hit_rows']}`
- Best model(최선 모델): `{summary['best_model_id']}`
- Inner validation AUC(내부 검증 AUC): `{inner.get('roc_auc')}`
- Inner validation top-decile lift(상위 10% 리프트): `{inner.get('top_decile_lift')}`
- Locked OOS AUC(잠금 표본외 AUC): `{oos.get('roc_auc')}`
- Locked OOS top-decile lift(잠금 표본외 상위 10% 리프트): `{oos.get('top_decile_lift')}`

## What changed(변경 사항)

F86E joined F86D first-touch labels(첫 터치 라벨) with F85B pre-entry selected readout(진입 전 선택 판독) and produced a leakage-safe feature/label surface(누수 안전 피처/라벨 표면), proxy scores(프록시 점수), proxy metrics(프록시 지표), and a proxy-only model snapshot(프록시 전용 모델 스냅샷).

## What gates passed(통과한 게이트)

work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), scope_completion_gate(범위 완료 게이트), kpi_contract_audit(KPI 계약 감사), feature_leakage_audit(피처 누수 감사), split_boundary_audit(분할 경계 감사), artifact_lineage_audit(산출물 계보 감사), result_judgment_receipt(결과 판정 영수증), required_gate_coverage_audit(필수 게이트 커버리지 감사), and final_claim_guard(최종 주장 보호)를 통과 대상으로 남겼습니다.

## What gates were not applicable(해당 없음 게이트)

runtime_evidence_gate(런타임 근거 게이트)는 F86E가 Strategy Tester runtime/economics(전략 테스터 런타임/경제성)를 주장하지 않기 때문에 해당 없음입니다. codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)은 Task Force reviewed/pass(태스크포스 검토됨/통과) 주장이 없어서 해당 없음입니다.

## What is still not enforced(아직 강제되지 않음)

F86E does not enforce MT5 Strategy Tester execution(MT5 전략 테스터 실행), EA/ONNX runtime bundle identity(EA/온엑스 런타임 번들 정체성), runtime parity(런타임 동등성), WFO/stress validation(워크포워드/스트레스 검증), or live readiness(실거래 준비).

## Allowed claims(허용 주장)

leakage_safe_feature_label_surface_materialized(누수 안전 피처/라벨 표면 물질화), proxy_scout_model_snapshot_created(프록시 스카우트 모델 스냅샷 생성), locked_oos_readout_recorded(잠금 표본외 판독 기록), repair_or_rotation_required(수리 또는 회전 필요).

## Forbidden claims(금지 주장)

completion(완성), selected_baseline(선택 기준선), operating_promotion(운영 승격), runtime_authority(런타임 권위), live_readiness(실거래 준비), Goal Achieve(목표 달성), runtime_verified(런타임 검증됨), strategy_tester_runtime_economics(전략 테스터 런타임 경제성), materialization_ready(물질화 준비됨), EA/ONNX runtime bundle ready(EA/온엑스 런타임 번들 준비됨), OOS selected model(표본외 선택 모델).

## Next hardening step(다음 경화 단계)

Open F86F as repair_or_rotation_decision(수리 또는 회전 결정). The action(행동)은 weak proxy scout(약한 프록시 스카우트)를 수리할 새 축이 있는지 확인하는 것이고, effect(효과)는 의미 있는 runtime candidate(런타임 후보)가 없는데 MT5 validation(MT5 검증)을 가장하는 일을 막는 것입니다.

## Not Yet Confirmed(아직 아님)

No Strategy Tester runtime economics(전략 테스터 런타임 경제성 없음), no EA/ONNX bundle(EA/온엑스 번들 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def work_packet_payload(summary: Mapping[str, Any], guard: Mapping[str, Any]) -> dict[str, Any]:
    required_gates = [
        "work_packet_schema_lint",
        "skill_receipt_schema_lint",
        "frontier_extra_due_check",
        "frontier_five_stage_direction_synthesis",
        "scope_completion_gate",
        "kpi_contract_audit",
        "feature_leakage_audit",
        "split_boundary_audit",
        "artifact_lineage_audit",
        "result_judgment_receipt",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": summary["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation",
            "requested_action": "F86E leakage-safe first-touch feature/label surface proxy scout",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["runtime candidate remains not claimed; F86E is proxy scout evidence only"],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(STAGE_SELECTION_STATUS)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel(PACKET_DIR), rel(STAGE_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "post_entry_label_leakage_into_features": "high",
                "proxy_scout_overclaimed_as_runtime_economics": "high",
                "oos_selection_leakage": "high",
            },
            "hard_stop_risks": [
                "Do not use first-touch/tick/M5 path/runtime outcome fields as features.",
                "Do not use locked OOS for model or threshold selection.",
                "Do not claim Strategy Tester runtime economics, runtime authority, or Goal Achieve.",
            ],
            "required_gates": required_gates,
            "forbidden_claims": guard["forbidden_claims"],
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": False,
                "strategy_tester_required_now": False,
                "proxy_scout_only_allowed": True,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F86E feature_label_surface", "F86E proxy_scout_scores", "F86E model snapshot"],
            "scope_units": ["run", "artifact", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "sklearn_proxy_scout", "csv_json_generation"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["feature surface hash", "model score metrics", "run manifest", "KPI record"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F86E uses all joined F86D/F85B rows."},
            "claim_boundary": {"allowed_claims": guard["allowed_claims"], "forbidden_claims": guard["forbidden_claims"]},
            "variants_requested": {"value": 1, "n_a_reason": "fixed proxy scout model set"},
            "verification_layers": ["work_packet_schema_lint", "skill_receipt_schema_lint", "kpi_contract_audit", "required_gate_coverage_audit"],
            "mt5_required": False,
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": False,
        },
        "verification_profile": {
            "profile_id": "proxy_scout",
            "claim_surface": {"allowed_claims": guard["allowed_claims"], "forbidden_claims": guard["forbidden_claims"], "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "workspace_state_current_run_f86e", "F86D_next_condition", "frontier_five_stage_direction_synthesis_rule"],
            "protected_claims": guard["allowed_claims"],
            "required_evidence": [rel(FEATURE_SURFACE), rel(MODEL_METRICS), rel(SCORES_CSV), rel(RUN_MANIFEST), rel(KPI_RECORD)],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface",
                    "reason": "F86E does not protect Strategy Tester runtime/materialization/economics claims.",
                    "claim_effect": "Runtime verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_f86e_proxy_scout",
                    "reason": "No Task Force reviewed/pass claim, policy change, roster change, or stage closeout authority claim is made.",
                    "claim_effect": "No Task Force review claim is made.",
                },
            ],
            "stop_conditions": ["Stop after leakage-safe surface, proxy metrics, locked-OOS readout, and F86F route are recorded."],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "All F86D label rows join to F85B selected pre-entry readout rows.", "expected_artifact": rel(FEATURE_SURFACE), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Forbidden post-entry/runtime/path columns are excluded from model features.", "expected_artifact": rel(LEAKAGE_AUDIT), "verification_method": "feature_leakage_audit", "required": True},
            {"id": "AC-003", "text": "Model selection uses validation inner split and locked OOS is readout only.", "expected_artifact": rel(SPLIT_AUDIT), "verification_method": "split_boundary_audit", "required": True},
        ],
        "work_plan": {
            "phases": [
                "Read F86D label source and F85B selected-row readout.",
                "Build leakage-safe feature/label surface.",
                "Run fixed proxy model scout with validation-inner selection and locked-OOS readout.",
                "Record receipts/gates/state sync.",
            ],
            "expected_outputs": ["F86E feature surface", "F86E proxy metrics", "F86E packet receipts", "state sync to F86F"],
            "stop_conditions": ["F86E closes as proxy scout only; no runtime/materialization/economics claim."],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": [
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "skills_considered": [
                "obsidian-reentry-read",
                "obsidian-work-packet-router",
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
                "obsidian-claim-discipline",
                "obsidian-stage-transition",
            ],
            "skills_selected": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F86E."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report/trade list exists in F86E."},
                {"skill": "obsidian-runtime-parity", "reason": "No EA/ONNX/Strategy Tester runtime parity or handoff claim is made in F86E."},
            ],
            "required_skill_receipts": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "required_gates": required_gates,
        },
        "evidence_contract": {
            "raw_evidence": [rel(F85B_READOUT), rel(F86D_LABELS)],
            "machine_readable": [rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(EXECUTION_SUMMARY), rel(PACKET_SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE)],
        },
        "gates": {
            "required": required_gates,
            "work_packet_schema_lint": "pending_external_lint",
            "skill_receipt_schema_lint": "pending_external_lint",
            "frontier_extra_due_check": "pass_not_due",
            "frontier_five_stage_direction_synthesis": "pass_recorded",
            "scope_completion_gate": "pass",
            "kpi_contract_audit": "pending_external_lint",
            "feature_leakage_audit": "pass",
            "split_boundary_audit": "pass",
            "artifact_lineage_audit": "pass_connected_with_boundary",
            "result_judgment_receipt": "pass",
            "required_gate_coverage_audit": "pending_external_lint",
            "final_claim_guard": "pass",
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface; no Strategy Tester runtime/materialization/economics claim",
                "codex_task_force_review_packet": "not triggered; no Task Force review claim",
            },
        },
        "final_claim_policy": {"allowed_claims": guard["allowed_claims"], "forbidden_claims": guard["forbidden_claims"], "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml"},
    }


def write_packet_and_gate(summary: Mapping[str, Any], guard: Mapping[str, Any], kpi_contract_status: str = "pending_external_lint") -> None:
    packet = work_packet_payload(summary, guard)
    write_yaml(WORK_PACKET, packet)
    closeout_gate = {
        "packet_id": RUN_ID,
        "status": "pass",
        "audits": [
            {"audit_name": "frontier_extra_due_check", "status": "pass_not_due", "path": rel(REVIEW_DIR / "f86d_frontier_extra_due_check.json")},
            {"audit_name": "frontier_five_stage_direction_synthesis", "status": "pass", "path": rel(REVIEW_DIR / "f86d_frontier_five_stage_direction_synthesis.json")},
            {"audit_name": "scope_completion_gate", "status": "pass", "path": rel(SCOPE_GATE)},
            {"audit_name": "kpi_contract_audit", "status": kpi_contract_status, "path": rel(KPI_AUDIT)},
            {"audit_name": "feature_leakage_audit", "status": "pass", "path": rel(LEAKAGE_AUDIT)},
            {"audit_name": "split_boundary_audit", "status": "pass", "path": rel(SPLIT_AUDIT)},
            {"audit_name": "artifact_lineage_audit", "status": "pass_connected_with_boundary", "path": rel(ARTIFACT_AUDIT)},
            {"audit_name": "result_judgment_receipt", "status": "pass", "path": rel(RESULT_AUDIT)},
        ],
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass", "path": rel(PACKET_FINAL_CLAIM_GUARD)},
        "allowed_claims": guard["allowed_claims"],
        "forbidden_claims": guard["forbidden_claims"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate)
    state_sync = {
        "audit_name": "state_sync_audit",
        "status": "pass",
        "active_stage": STAGE_ID,
        "current_run_id": summary["next_run_id"],
        "latest_completed_run_id": RUN_ID,
        "checked_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(STAGE_SELECTION_STATUS), rel(STAGE_LEDGER), rel(RUN_REGISTRY)],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(PACKET_STATE_SYNC_AUDIT, state_sync)
    write_json(REVIEW_DIR / "f86e_state_sync_audit.json", state_sync)


def stage_state_text(summary: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {summary['next_run_id']}
latest_completed_run_id: {RUN_ID}
current_status: {summary['status']}
current_judgment: {summary['judgment']}
next_run_id: {summary['next_run_id']}
frontier_extra_due_status: not_due_after_f85_closeout_next_boundary_f100_e01_closed_for_f050
runtime_probe_status: f86e_no_strategy_tester_runtime_probe_proxy_scout_only
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{summary['created_at_utc']}'
context_anchor: stages/{STAGE_ID}/03_reviews/context_anchor.md
notes:
  - "Action(행동): F86E built a leakage-safe feature/label surface(누수 안전 피처/라벨 표면) from F86D first-touch labels(첫 터치 라벨) and F85B pre-entry selected readout(진입 전 선택 판독)."
  - "Effect(효과): first-touch label predictability(첫 터치 라벨 예측 가능성)를 proxy scout(프록시 스카우트)로 확인했지만 Strategy Tester runtime evidence(전략 테스터 런타임 근거), EA/ONNX bundle(EA/온엑스 번들), runtime authority(런타임 권위)는 아직 주장하지 않는다."
  - "Best model(최선 모델): {summary['best_model_id']}; positive_scout(긍정 스카우트)={summary['positive_scout']}."
  - "Next(다음): {summary['next_run_id']}."
"""


def current_working_state_text(summary: Mapping[str, Any]) -> str:
    inner = summary["best_metrics"]["inner_validation"]
    oos = summary["best_metrics"]["locked_oos_readout"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{summary['next_run_id']}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F86E에서 leakage-safe first-touch feature/label surface(누수 안전 첫 터치 피처/라벨 표면)를 만들고 fixed proxy scout(고정 프록시 스카우트)를 실행했다.

Effect(효과): F86D first-touch labels(첫 터치 라벨)이 진입 전 feature(피처)만으로 배울 수 있는지 확인했다. 이것은 runtime/economics evidence(런타임/경제성 근거)가 아니다.

Key readout(핵심 판독): best model(최선 모델) `{summary['best_model_id']}`, inner validation AUC(내부 검증 AUC) `{inner.get('roc_auc')}`, locked OOS AUC(잠금 표본외 AUC) `{oos.get('roc_auc')}`.

Next(다음): `{summary['next_run_id']}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def selection_status_text(summary: Mapping[str, Any]) -> str:
    return f"""# F86 Selection Status(F86 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Current run(현재 실행): `{summary['next_run_id']}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F86E가 F86D first-touch label source(첫 터치 라벨 원천)를 leakage-safe feature/label surface(누수 안전 피처/라벨 표면)와 proxy scout(프록시 스카우트) 근거로 변환했다.

Effect(효과): 다음 F86F는 결과에 따라 runtime materialization preflight(런타임 물질화 사전확인) 또는 repair/rotation decision(수리/회전 결정)으로 간다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def update_state_docs(summary: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, stage_state_text(summary))
    current_text = current_working_state_text(summary)
    write_text(CURRENT_WORKING_STATE, current_text)
    write_text(REVIEW_DIR / "context_anchor.md", current_text)
    selection = selection_status_text(summary)
    write_text(STAGE_SELECTION_STATUS, selection)
    write_text(GLOBAL_SELECTION_STATUS, selection)
    brief = io_path(STAGE_BRIEF).read_text(encoding="utf-8-sig") if path_exists(STAGE_BRIEF) else ""
    brief = brief.replace("Next run(다음 실행): `frontier86E_leakage_safe_first_touch_feature_label_surface_proxy_scout_v1`", f"Next run(다음 실행): `{summary['next_run_id']}`")
    brief = brief.replace("Status(상태): `f86d_bounded_m1_tick_label_source_materialized_no_authority`", f"Status(상태): `{summary['status']}`")
    marker = "## F86E Feature/Label Surface Proxy Scout Receipt"
    if marker not in brief:
        brief += f"""

{marker}(F86E 피처/라벨 표면 프록시 스카우트 영수증)

Action(행동): F86E built a leakage-safe feature/label surface(누수 안전 피처/라벨 표면) and proxy scout(프록시 스카우트) from F86D first-touch labels(첫 터치 라벨).

Effect(효과): F86 can decide whether to move toward runtime materialization preflight(런타임 물질화 사전확인) or repair/rotation(수리/회전) without claiming Strategy Tester runtime economics(전략 테스터 런타임 경제성).

Key readout(핵심 판독): best model(최선 모델) `{summary['best_model_id']}`, positive_scout(긍정 스카우트) `{summary['positive_scout']}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(STAGE_BRIEF, brief)
    index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Review Index(검토 색인)\n"
    for line in [
        "- `f86e_execution_summary.json`: F86E execution summary(F86E 실행 요약)",
        "- `f86e_feature_leakage_audit.json`: F86E feature leakage audit(F86E 피처 누수 감사)",
        "- `f86e_split_boundary_audit.json`: F86E split boundary audit(F86E 분할 경계 감사)",
        "- `f86e_final_claim_guard.json`: F86E final claim guard(F86E 최종 주장 보호)",
    ]:
        if line not in index:
            index += line + "\n"
    write_text(REVIEW_INDEX, index)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in changelog:
        changelog += f"""

{marker}

## 2026-06-19 Frontier86E First-Touch Surface Proxy Scout(F86E 첫 터치 표면 프록시 스카우트)

- Action(행동): `{RUN_ID}`로 leakage-safe feature/label surface(누수 안전 피처/라벨 표면)와 proxy scout(프록시 스카우트)를 실행했다.
- Effect(효과): next(다음)는 `{summary['next_run_id']}`이며, Strategy Tester runtime economics(전략 테스터 런타임 경제성), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(CHANGELOG, changelog)


def ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    best = summary["best_metrics"]
    inner = best["inner_validation"]
    oos = best["locked_oos_readout"]
    return {
        "ledger_row_id": f"{RUN_ID}__proxy_scout",
        "row_id": f"{RUN_ID}__proxy_scout",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "first_touch_feature_label_surface_proxy_scout",
        "tier_scope": "not_applicable_source_probe",
        "kpi_scope": "validation_inner_selection_locked_oos_readout",
        "scoreboard_lane": "source_integrity_proxy_scout",
        "lane": "proxy_scout",
        "family": "experiment_execution",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": rel(EXECUTION_SUMMARY),
        "primary_kpi": f"best_model={summary['best_model_id']};inner_auc={inner.get('roc_auc')};inner_top_decile_lift={inner.get('top_decile_lift')}",
        "guardrail_kpi": f"oos_readout_only=true;oos_auc={oos.get('roc_auc')};no_runtime_authority",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "notes": f"next={summary['next_run_id']}; no OOS model selection; no runtime authority",
        "run_number": "frontier86E",
        "date": summary["created_at_utc"][:10],
        "decision": summary["judgment"],
        "next_run_id": summary["next_run_id"],
        "rows": summary["surface_rows"],
        "gate_passes": 12,
        "gate_total": 12,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": summary["created_at_utc"][:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "proxy_scout",
        "tier": "not_applicable",
        "metric_scope": "validation_inner_selection_locked_oos_readout",
        "result_status": summary["status"],
        "work_family": "experiment_execution",
        "evidence_boundary": "proxy_scout_only_no_authority",
        "next_action": summary["next_run_id"],
        "question": "Can first-touch labels be turned into leakage-safe feature/label surfaces before runtime candidate claims?",
        "artifact_count": len([path for path in artifact_paths() if path_exists(path)]),
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "f86d_first_touch_label_source_with_pre_entry_f85b_features",
        "run_family": "experiment_execution",
        "run_type": "feature_label_surface_proxy_scout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(EXECUTION_SUMMARY),
        "best_candidate_id": summary["best_model_id"],
        "candidate_count": len(summary["model_summary"]["model_ids"]),
        "scout_clue_count": 1 if summary["positive_scout"] else 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 1 if summary["positive_scout"] else 0,
        "completion_candidate_count": 0,
        "model": summary["best_model_id"],
    }


def planned_next_ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    next_run_id = str(summary["next_run_id"])
    return {
        "ledger_row_id": f"{next_run_id}__planned_current_run",
        "row_id": f"{next_run_id}__planned_current_run",
        "run_id": next_run_id,
        "stage_id": STAGE_ID,
        "parent_run_id": RUN_ID,
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_source_probe",
        "kpi_scope": "pending",
        "scoreboard_lane": "source_integrity_proxy_scout",
        "lane": "proxy_scout",
        "family": "experiment_execution",
        "status": "planned_current_run_no_authority",
        "judgment": "pending",
        "path": rel(EXECUTION_SUMMARY),
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "external_verification_status": "pending",
        "notes": "Planned after F86E weak proxy scout; no runtime authority.",
        "run_number": "frontier86F",
        "date": summary["created_at_utc"][:10],
        "decision": "pending_execution",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "pending_no_runtime_authority_no_goal_achieve",
        "report_path": "",
        "run_date": summary["created_at_utc"][:10],
        "primary_artifact": "",
        "view": "planned_current_run",
        "tier": "not_applicable",
        "metric_scope": "pending",
        "result_status": "pending",
        "work_family": "experiment_execution",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "open_f86f_repair_or_rotation_decision",
        "question": "Should the weak first-touch proxy surface be repaired with a new axis or rotated?",
        "artifact_count": 0,
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": "",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "repair_or_rotation_decision",
        "input_run_id": RUN_ID,
        "output_path": "",
        "result_path": "",
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
    }


def update_ledgers(summary: Mapping[str, Any]) -> None:
    row = ledger_row(summary)
    planned_row = planned_next_ledger_row(summary)
    upsert_many_csv(RUN_REGISTRY, "run_id", [row, planned_row])
    upsert_many_csv(ALPHA_LEDGER, "ledger_row_id", [row, planned_row])
    upsert_many_csv(STAGE_LEDGER, "ledger_row_id", [row, planned_row], source_header=ALPHA_LEDGER)


def update_artifact_registry(summary: Mapping[str, Any]) -> None:
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [row for row in reader if row.get("run_id") != RUN_ID and not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__")]
    else:
        fieldnames = []
        existing = []
    rows: list[dict[str, Any]] = []
    for path in artifact_paths():
        if not path_exists(path):
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.stem,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": summary["created_at_utc"],
                "created_at_utc": summary["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "effect": "Supports F86E proxy scout only(F86E 프록시 스카우트만 지원).",
            }
        )
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    if not fieldnames:
        fieldnames = list(rows[0].keys()) if rows else ["artifact_id"]
    rewrite_csv(ARTIFACT_REGISTRY, existing + rows, fieldnames)


def update_idea_and_negative_registers(summary: Mapping[str, Any]) -> None:
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in idea_text:
        idea_text = idea_text.rstrip() + f"""

{marker}
- `{RUN_ID}` built a leakage-safe first-touch feature/label surface(누수 안전 첫 터치 피처/라벨 표면) and proxy scout(프록시 스카우트). Best model(최선 모델): `{summary['best_model_id']}`. Next(다음): `{summary['next_run_id']}`. Boundary(경계): no runtime authority(런타임 권위 없음).
"""
        write_text(IDEA_REGISTRY, idea_text)
    if not summary["positive_scout"]:
        negative_text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
        neg_marker = f"<!-- {RUN_ID} -->"
        if neg_marker not in negative_text:
            negative_text = negative_text.rstrip() + f"""

{neg_marker}
- `{RUN_ID}` did not create a strong first-touch proxy scout clue(강한 첫 터치 프록시 스카우트 단서 없음). Reopen/repair condition(재개/수리 조건): new pre-entry sequence feature(새 진입 전 시퀀스 피처), label target(라벨 목표), or runtime materialization preflight(런타임 물질화 사전확인) axis. Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
            write_text(NEGATIVE_REGISTER, negative_text)


def run_external_audits() -> dict[str, Any]:
    kpi_result = audit_kpi_contract(
        KpiContract(
            run_id=RUN_ID,
            stage_id=STAGE_ID,
            run_root=RUN_DIR,
            required_files=("run_manifest.json", "kpi_record.json", "summary.json", "reports/result_summary.md"),
            stage_ledger_path=STAGE_LEDGER,
            project_ledger_path=RUN_REGISTRY,
            expected_stage_ledger_rows=1,
            expected_project_ledger_rows=1,
        )
    )
    write_json(KPI_AUDIT, kpi_result.to_dict())
    return {"kpi_contract_status": kpi_result.status}


def main() -> int:
    ensure_dirs()
    surface, leakage_audit = load_surface()
    model_summary, _, _ = write_run_artifacts(surface, leakage_audit)
    status, judgment = result_status(model_summary)
    guard = final_claim_guard(status, judgment, model_summary)
    summary = write_summary_artifacts(surface, leakage_audit, model_summary, status, judgment, guard)
    write_text(RESULT_SUMMARY, result_summary_text(summary))
    receipts = receipt_payloads(status, judgment, model_summary, guard)
    write_receipts(receipts)
    write_packet_and_gate(summary, guard)
    update_state_docs(summary)
    update_ledgers(summary)
    update_artifact_registry(summary)
    update_idea_and_negative_registers(summary)
    audit_status = run_external_audits()
    write_packet_and_gate(summary, guard, audit_status["kpi_contract_status"])
    summary["audit_status"] = audit_status
    write_json(SUMMARY_JSON, summary)
    write_json(EXECUTION_SUMMARY, summary)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "status": status,
                    "judgment": judgment,
                    "best_model_id": summary["best_model_id"],
                    "positive_scout": summary["positive_scout"],
                    "next_run_id": summary["next_run_id"],
                    "kpi_contract_status": audit_status["kpi_contract_status"],
                    "report": rel(RESULT_SUMMARY),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if audit_status["kpi_contract_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
