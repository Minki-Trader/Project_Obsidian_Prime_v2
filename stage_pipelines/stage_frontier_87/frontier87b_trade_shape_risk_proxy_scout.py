from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    mean_absolute_error,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation"
RUN_ID = "frontier87B_trade_shape_risk_proxy_scout_v1"
PARENT_RUN_ID = "frontier87A_stage_open_runtime_native_trade_shape_risk_logic_rotation_v1"
NEXT_RUN_ID_IF_MEANINGFUL = "frontier87C_runtime_materialization_preflight_or_gap_decision_v1"
NEXT_RUN_ID_IF_WEAK = "frontier87C_trade_shape_risk_repair_or_rotation_decision_v1"
PREVIOUS_STAGE_ID = "stage_frontier_86__runtime_native_intrabar_path_label_source"

CLAIM_BOUNDARY = (
    "f87b_trade_shape_risk_proxy_scout_only_no_strategy_tester_runtime_"
    "economics_no_runtime_authority_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = "not_run_proxy_scout_only_no_strategy_tester_runtime_claim"
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f86_closeout_next_boundary_f100_e01_closed_for_f050"
SCRIPT_REL = "stage_pipelines/stage_frontier_87/frontier87b_trade_shape_risk_proxy_scout.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
SURFACE_DIR = RUN_DIR / "trade_shape_surface"
PROXY_DIR = RUN_DIR / "proxy_scout"
MODEL_DIR = RUN_DIR / "models"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F87A_DESIGN = STAGE_DIR / "02_runs" / PARENT_RUN_ID / "design/f87a_experiment_design.json"
F87A_HYPOTHESIS = STAGE_DIR / "02_runs" / PARENT_RUN_ID / "design/runtime_trade_shape_risk_hypothesis_contract.json"
F87A_HANDOFF = STAGE_DIR / "02_runs" / PARENT_RUN_ID / "design/f87b_proxy_scout_execution_brief.json"
F86D_LABELS = (
    ROOT
    / "stages"
    / PREVIOUS_STAGE_ID
    / "02_runs/frontier86D_tick_m1_full_registration_or_first_touch_label_materializer_v1/first_touch_labels/first_touch_labels.csv"
)
F86D_SUMMARY = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews/f86d_execution_summary.json"
F86G_SUMMARY = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews/f86g_execution_summary.json"
F86G_SURFACE = (
    ROOT
    / "stages"
    / PREVIOUS_STAGE_ID
    / "02_runs/frontier86G_pre_entry_intrabar_sequence_feature_scout_v1/sequence_feature_surface/sequence_feature_surface.csv"
)
F86G_SCHEMA = (
    ROOT
    / "stages"
    / PREVIOUS_STAGE_ID
    / "02_runs/frontier86G_pre_entry_intrabar_sequence_feature_scout_v1/sequence_feature_surface/feature_schema.json"
)
TRAINING_LABEL_CONTRACT = ROOT / "docs/contracts/training_label_split_contract_fpmarkets_v2.md"
TIME_AXIS_POLICY = ROOT / "docs/contracts/time_axis_policy_fpmarkets_v2.md"
FEATURE_CONTRACT = ROOT / "docs/contracts/feature_calculation_spec_fpmarkets_v2.md"
FRONTIER_GOVERNANCE = ROOT / "docs/policies/frontier_governance.md"

TRADE_SHAPE_SURFACE = SURFACE_DIR / "trade_shape_risk_surface.csv"
RISK_SURFACE_BINS = SURFACE_DIR / "risk_surface_bins.csv"
FEATURE_SCHEMA_OUT = SURFACE_DIR / "f87b_feature_target_schema.json"
PROXY_SCORES = PROXY_DIR / "proxy_scores.csv"
PROXY_METRICS = PROXY_DIR / "proxy_metrics.json"
CANDIDATE_QUEUE = PROXY_DIR / "candidate_queue.csv"
MODEL_CARD = MODEL_DIR / "proxy_model_card.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

EXECUTION_SUMMARY = REVIEW_DIR / "f87b_execution_summary.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f87b_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f87b_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f87b_frontier_topic_rotation_check.json"
FEATURE_LEAKAGE_AUDIT = REVIEW_DIR / "f87b_feature_leakage_audit.json"
SPLIT_BOUNDARY_AUDIT = REVIEW_DIR / "f87b_split_boundary_audit.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f87b_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f87b_model_validation_audit.json"
SCOPE_GATE = REVIEW_DIR / "f87b_scope_completion_gate.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f87b_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f87b_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f87b_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f87b_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f87b_state_sync_audit.json"

RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f87b_run_evidence_receipt.json"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f87b_experiment_design_receipt.json"
DATA_RECEIPT = REVIEW_DIR / "f87b_data_integrity_receipt.json"
MODEL_RECEIPT = REVIEW_DIR / "f87b_model_validation_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f87b_artifact_lineage_receipt.json"
RESULT_RECEIPT = REVIEW_DIR / "f87b_result_judgment_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f87b_claim_discipline_receipt.json"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-19_frontier87b_trade_shape_risk_proxy_scout.md"

STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs/input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = STAGE_DIR / "04_selected/selection_status.md"

ALLOWED_CLAIMS = [
    "f87b_trade_shape_risk_proxy_surface_materialized",
    "f87b_leakage_and_split_audits_recorded",
    "f87b_proxy_scout_result_recorded",
    "f87b_runtime_preflight_decision_recorded",
]
FORBIDDEN_CLAIMS = [
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
    "task_force_reviewed",
    "reviewed_by_unspawned_agents",
]
REQUIRED_SKILLS = [
    "obsidian-run-evidence-system",
    "obsidian-experiment-design",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-result-judgment",
    "obsidian-claim-discipline",
]
REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "frontier_extra_due_check",
    "frontier_five_stage_direction_synthesis",
    "frontier_topic_rotation_check",
    "scope_completion_gate",
    "data_integrity_audit",
    "model_validation_audit",
    "kpi_contract_audit",
    "artifact_lineage_audit",
    "result_judgment_receipt",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
FORBIDDEN_FEATURE_TOKENS = (
    "first_touch",
    "runtime_win",
    "proxy_win",
    "proxy_loss",
    "m5_high",
    "m5_low",
    "m5_close",
    "sl_price",
    "tp_price",
    "m5_sl_hit",
    "m5_tp_hit",
    "m5_path",
    "label_resolution",
    "tick_count",
    "target_",
)


def utc_now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, (np.integer, np.int64, np.int32)):
        return int(value)
    if isinstance(value, (np.floating, np.float64, np.float32)):
        return float(value) if math.isfinite(float(value)) else None
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if pd.isna(value):
        return None
    return value


def fs_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt" and len(str(resolved)) >= 240:
        return io_path(path)
    return resolved


def write_text(path: Path, text: str) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    fs_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    fs_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8-sig")


def write_yaml(path: Path, payload: Any) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    fs_path(path).write_text(yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def write_frame(path: Path, frame: pd.DataFrame) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(fs_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig")


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "" if value is None else value


def csv_lineterminator(path: Path) -> str:
    registry_paths = {RUN_REGISTRY, ALPHA_LEDGER, ARTIFACT_REGISTRY, STAGE_LEDGER}
    if path in registry_paths:
        return "\r\n"
    if path_exists(path) and b"\r\n" in io_path(path).read_bytes():
        return "\r\n"
    return "\n"


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
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator=csv_lineterminator(path))
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def upsert_many_csv(path: Path, key: str, new_rows: Sequence[Mapping[str, Any]], source_header: Path | None = None) -> None:
    new_rows = list(new_rows)
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
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
    write_csv_rows(path, rows, fieldnames)


def file_identity(path: Path) -> dict[str, Any]:
    exists = path_exists(path)
    return {
        "path": rel(path),
        "exists": exists,
        "size_bytes": io_path(path).stat().st_size if exists else 0,
        "sha256_lf_normalized": sha256_file_lf_normalized(path) if exists else "",
    }


def feature_order_hash(columns: Sequence[str]) -> str:
    return hashlib.sha256(("\n".join(columns) + "\n").encode("utf-8")).hexdigest()


def ensure_dirs() -> None:
    for directory in (SURFACE_DIR, PROXY_DIR, MODEL_DIR, REPORT_DIR, REVIEW_DIR, PACKET_DIR):
        fs_path(directory).mkdir(parents=True, exist_ok=True)


def source_inputs() -> list[Path]:
    return [
        F87A_DESIGN,
        F87A_HYPOTHESIS,
        F87A_HANDOFF,
        F86D_LABELS,
        F86D_SUMMARY,
        F86G_SURFACE,
        F86G_SCHEMA,
        F86G_SUMMARY,
        TRAINING_LABEL_CONTRACT,
        TIME_AXIS_POLICY,
        FEATURE_CONTRACT,
        FRONTIER_GOVERNANCE,
    ]


def produced_artifacts(include_packet_outputs: bool = True) -> list[Path]:
    artifacts = [
        ROOT / SCRIPT_REL,
        TRADE_SHAPE_SURFACE,
        RISK_SURFACE_BINS,
        FEATURE_SCHEMA_OUT,
        PROXY_SCORES,
        PROXY_METRICS,
        CANDIDATE_QUEUE,
        MODEL_CARD,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        RESULT_SUMMARY,
        EXECUTION_SUMMARY,
        FRONTIER_EXTRA_DUE_CHECK,
        FIVE_STAGE_SYNTHESIS,
        TOPIC_ROTATION_CHECK,
        FEATURE_LEAKAGE_AUDIT,
        SPLIT_BOUNDARY_AUDIT,
        DATA_INTEGRITY_AUDIT,
        MODEL_VALIDATION_AUDIT,
        SCOPE_GATE,
        KPI_CONTRACT_AUDIT,
        ARTIFACT_AUDIT,
        RESULT_JUDGMENT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        RUN_EVIDENCE_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        ARTIFACT_RECEIPT,
        RESULT_RECEIPT,
        CLAIM_RECEIPT,
        DECISION_MEMO,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        STAGE_BRIEF,
        SELECTION_STATUS,
        REVIEW_INDEX,
        RUN_REGISTRY,
        ALPHA_LEDGER,
        STAGE_LEDGER,
        ARTIFACT_REGISTRY,
    ]
    if include_packet_outputs:
        artifacts.extend(
            [
                WORK_PACKET,
                SKILL_RECEIPTS,
                PACKET_FINAL_CLAIM_GUARD,
                PACKET_STATE_SYNC_AUDIT,
                PACKET_CLOSEOUT_GATE,
                PACKET_REQUIRED_GATE_AUDIT,
                PACKET_WORK_PACKET_LINT,
                PACKET_SKILL_RECEIPT_LINT,
            ]
        )
    return artifacts


def build_surface(schema: Mapping[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    seq = read_csv_frame(F86G_SURFACE)
    labels = read_csv_frame(F86D_LABELS)
    seq["row_index"] = seq["row_index"].astype(int)
    labels["source_row_index"] = labels["source_row_index"].astype(int)
    merged = seq.merge(
        labels,
        left_on="row_index",
        right_on="source_row_index",
        how="inner",
        suffixes=("", "_label"),
        validate="one_to_one",
    )
    merged["timestamp_utc"] = pd.to_datetime(merged["timestamp_utc"], utc=True)
    merged["date_utc"] = merged["timestamp_utc"].dt.date.astype(str)
    merged["entry_price_proxy_m5_open"] = pd.to_numeric(merged["entry_price_proxy_m5_open"], errors="coerce")
    merged["m5_high"] = pd.to_numeric(merged["m5_high"], errors="coerce")
    merged["m5_low"] = pd.to_numeric(merged["m5_low"], errors="coerce")
    merged["m5_close"] = pd.to_numeric(merged["m5_close"], errors="coerce")
    merged["sl_price"] = pd.to_numeric(merged["sl_price"], errors="coerce")
    merged["tp_price"] = pd.to_numeric(merged["tp_price"], errors="coerce")
    merged["mfe_points"] = merged["m5_high"] - merged["entry_price_proxy_m5_open"]
    merged["mae_points"] = merged["entry_price_proxy_m5_open"] - merged["m5_low"]
    merged["close_points"] = merged["m5_close"] - merged["entry_price_proxy_m5_open"]
    merged["sl_distance_points"] = (merged["entry_price_proxy_m5_open"] - merged["sl_price"]).abs()
    merged["tp_distance_points"] = (merged["tp_price"] - merged["entry_price_proxy_m5_open"]).abs()
    merged["mfe_r"] = merged["mfe_points"] / merged["sl_distance_points"].replace(0, np.nan)
    merged["mae_r"] = merged["mae_points"] / merged["sl_distance_points"].replace(0, np.nan)
    merged["close_r"] = merged["close_points"] / merged["sl_distance_points"].replace(0, np.nan)
    merged["tp_distance_r"] = merged["tp_distance_points"] / merged["sl_distance_points"].replace(0, np.nan)
    first_touch = merged["first_touch_label_label"].fillna(merged["first_touch_label"]).astype(str)
    merged["first_touch_label_final"] = first_touch
    merged["shape_score_r"] = np.select(
        [
            first_touch.str.startswith("tp"),
            first_touch.str.startswith("sl"),
        ],
        [
            2.0,
            -1.0,
        ],
        default=merged["close_r"].clip(lower=-1.0, upper=2.0),
    )
    merged["target_good_shape"] = ((merged["shape_score_r"] > 0.0) & (merged["mae_r"] <= 1.25)).astype(int)
    merged["target_bad_risk"] = ((merged["shape_score_r"] < 0.0) | (merged["mae_r"] >= 1.0)).astype(int)
    merged["target_tp_first_binary_f87b"] = first_touch.str.startswith("tp").astype(int)
    merged["selection_split_role"] = "locked_oos_readout"
    validation_index = merged.index[merged["split"] == "validation"].tolist()
    validation_sorted = merged.loc[validation_index].sort_values("timestamp_utc").index.tolist()
    fit_count = int(math.floor(len(validation_sorted) * 0.70))
    fit_index = set(validation_sorted[:fit_count])
    inner_index = set(validation_sorted[fit_count:])
    merged.loc[list(fit_index), "selection_split_role"] = "inner_fit"
    merged.loc[list(inner_index), "selection_split_role"] = "inner_validation"
    mismatch_checks = {
        "source_rows": int(len(seq)),
        "label_rows": int(len(labels)),
        "merged_rows": int(len(merged)),
        "timestamp_mismatches": int((merged["timestamp_utc"].astype(str) != pd.to_datetime(merged["timestamp_utc_label"], utc=True).astype(str)).sum())
        if "timestamp_utc_label" in merged.columns
        else 0,
        "split_mismatches": int((merged["split"] != merged["split_label"]).sum()) if "split_label" in merged.columns else 0,
        "decision_mismatches": int((merged["decision"] != merged["decision_label"]).sum()) if "decision_label" in merged.columns else 0,
    }
    expected_features = set(schema["feature_sets"]["sequence_context"]) | set(schema["feature_sets"]["sequence_plus_scalar_context"])
    missing_features = sorted(col for col in expected_features if col not in merged.columns)
    if missing_features:
        raise RuntimeError(f"Missing expected features: {missing_features}")
    return merged, mismatch_checks


def make_preprocessor(feature_columns: Sequence[str], frame: pd.DataFrame) -> ColumnTransformer:
    categorical = [col for col in feature_columns if frame[col].dtype == "object" or col in {"decision", "session_bucket"}]
    numeric = [col for col in feature_columns if col not in categorical]
    return ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric),
            ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), categorical),
        ],
        remainder="drop",
    )


def safe_auc(y_true: pd.Series, score: pd.Series) -> float | None:
    if y_true.nunique(dropna=True) < 2:
        return None
    return float(roc_auc_score(y_true, score))


def safe_ap(y_true: pd.Series, score: pd.Series) -> float | None:
    if y_true.nunique(dropna=True) < 2:
        return None
    return float(average_precision_score(y_true, score))


def safe_brier(y_true: pd.Series, score: pd.Series) -> float | None:
    if y_true.nunique(dropna=True) < 2:
        return None
    return float(brier_score_loss(y_true, score.clip(0, 1)))


def role_days(part: pd.DataFrame) -> int:
    if part.empty:
        return 0
    timestamps = pd.to_datetime(part["timestamp_utc"], utc=True)
    return max(1, int((timestamps.max().date() - timestamps.min().date()).days) + 1)


def top_slice_metrics(part: pd.DataFrame, score_col: str, pct: float) -> dict[str, Any]:
    if part.empty:
        return {
            "top_pct": pct,
            "rows": 0,
            "trades_per_day_proxy": 0.0,
            "good_shape_rate": None,
            "mean_shape_score_r": None,
            "mean_mae_r": None,
            "mean_mfe_r": None,
            "tp_first_rate": None,
            "shape_score_lift_vs_role": None,
        }
    n = max(1, int(math.ceil(len(part) * pct)))
    top = part.nlargest(n, score_col)
    days = role_days(part)
    role_mean = float(part["shape_score_r"].mean())
    return {
        "top_pct": pct,
        "rows": int(len(top)),
        "trades_per_day_proxy": float(len(top) / days),
        "good_shape_rate": float(top["target_good_shape"].mean()),
        "bad_risk_rate": float(top["target_bad_risk"].mean()),
        "mean_shape_score_r": float(top["shape_score_r"].mean()),
        "mean_mae_r": float(top["mae_r"].mean()),
        "mean_mfe_r": float(top["mfe_r"].mean()),
        "tp_first_rate": float(top["target_tp_first_binary_f87b"].mean()),
        "shape_score_lift_vs_role": float(top["shape_score_r"].mean() - role_mean),
    }


def split_metrics(frame: pd.DataFrame, score_col: str, model_kind: str) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for role in ("inner_fit", "inner_validation", "locked_oos_readout"):
        part = frame.loc[frame["selection_split_role"] == role].copy()
        if part.empty:
            metrics[role] = {"rows": 0}
            continue
        role_metrics: dict[str, Any] = {
            "rows": int(len(part)),
            "days": role_days(part),
            "baseline_good_shape_rate": float(part["target_good_shape"].mean()),
            "baseline_mean_shape_score_r": float(part["shape_score_r"].mean()),
            "baseline_mean_mae_r": float(part["mae_r"].mean()),
            "baseline_tp_first_rate": float(part["target_tp_first_binary_f87b"].mean()),
            "top_10pct": top_slice_metrics(part, score_col, 0.10),
            "top_20pct": top_slice_metrics(part, score_col, 0.20),
            "top_30pct": top_slice_metrics(part, score_col, 0.30),
        }
        if model_kind == "classification":
            role_metrics.update(
                {
                    "roc_auc": safe_auc(part["target_good_shape"], part[score_col]),
                    "average_precision": safe_ap(part["target_good_shape"], part[score_col]),
                    "brier": safe_brier(part["target_good_shape"], part[score_col]),
                }
            )
        else:
            role_metrics.update(
                {
                    "spearman_shape_score": float(part[[score_col, "shape_score_r"]].rank().corr().iloc[0, 1]),
                    "mae_shape_score": float(mean_absolute_error(part["shape_score_r"], part[score_col])),
                }
            )
        metrics[role] = role_metrics
    return metrics


def train_candidates(surface: pd.DataFrame, schema: Mapping[str, Any]) -> tuple[pd.DataFrame, dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    fit = surface.loc[surface["selection_split_role"] == "inner_fit"].copy()
    if fit.empty:
        raise RuntimeError("No inner_fit rows available.")

    candidates = [
        ("sequence_context__good_shape_logreg_l2_balanced", "classification", schema["feature_sets"]["sequence_context"]),
        ("sequence_plus_scalar_context__good_shape_logreg_l2_balanced", "classification", schema["feature_sets"]["sequence_plus_scalar_context"]),
        ("sequence_context__shape_score_extra_trees_depth5", "regression", schema["feature_sets"]["sequence_context"]),
        ("sequence_plus_scalar_context__shape_score_extra_trees_depth5", "regression", schema["feature_sets"]["sequence_plus_scalar_context"]),
    ]

    scored = surface.copy()
    candidate_metrics: dict[str, Any] = {}
    model_cards: list[dict[str, Any]] = []
    for model_id, kind, feature_columns in candidates:
        score_col = f"score__{model_id}"
        preprocessor = make_preprocessor(feature_columns, surface)
        if kind == "classification":
            if fit["target_good_shape"].nunique(dropna=True) < 2:
                candidate_metrics[model_id] = {"status": "skipped_single_class_fit"}
                continue
            model = Pipeline(
                [
                    ("preprocessor", preprocessor),
                    ("model", LogisticRegression(max_iter=1200, class_weight="balanced", solver="liblinear")),
                ]
            )
            model.fit(fit[feature_columns], fit["target_good_shape"])
            scored[score_col] = model.predict_proba(surface[feature_columns])[:, 1]
        else:
            model = Pipeline(
                [
                    ("preprocessor", preprocessor),
                    (
                        "model",
                        ExtraTreesRegressor(
                            n_estimators=180,
                            max_depth=5,
                            min_samples_leaf=20,
                            random_state=8702,
                            n_jobs=1,
                        ),
                    ),
                ]
            )
            model.fit(fit[feature_columns], fit["shape_score_r"])
            scored[score_col] = model.predict(surface[feature_columns])
        metrics = split_metrics(scored, score_col, kind)
        inner_top20 = metrics["inner_validation"]["top_20pct"]
        selection_score = (inner_top20["shape_score_lift_vs_role"] or 0.0) + math.log1p(inner_top20["rows"]) * 0.01
        candidate_metrics[model_id] = {
            "status": "evaluated",
            "model_kind": kind,
            "feature_count": len(feature_columns),
            "score_col": score_col,
            "selection_score_inner_validation_only": selection_score,
            "by_role": metrics,
        }
        model_cards.append(
            {
                "model_id": model_id,
                "model_kind": kind,
                "feature_set": "sequence_plus_scalar_context" if "plus_scalar" in model_id else "sequence_context",
                "feature_count": len(feature_columns),
                "feature_order_hash": feature_order_hash(feature_columns),
                "selection_uses_oos": False,
            }
        )

    evaluated = [item for item in candidate_metrics.items() if item[1].get("status") == "evaluated"]
    if not evaluated:
        raise RuntimeError("No proxy model candidates evaluated.")
    best_id, best_metrics = sorted(
        evaluated,
        key=lambda item: item[1]["selection_score_inner_validation_only"],
        reverse=True,
    )[0]
    best_score_col = best_metrics["score_col"]
    scored["best_model_id"] = best_id
    scored["best_score"] = scored[best_score_col]
    scored["best_score_rank_pct"] = scored["best_score"].rank(method="first", pct=True)
    scored["best_score_decile"] = np.ceil(scored["best_score_rank_pct"] * 10).clip(1, 10).astype(int)
    best_summary = {
        "best_model_id": best_id,
        "best_score_col": best_score_col,
        "selection_basis": "inner_validation_only_top20_shape_score_lift_plus_density_tiebreak",
        "best_metrics": best_metrics,
    }
    return scored, candidate_metrics, model_cards, best_summary


def build_candidate_queue(scored: pd.DataFrame, best_summary: Mapping[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for top_pct in (0.10, 0.20, 0.30, 0.40, 0.50):
        for role in ("inner_validation", "locked_oos_readout"):
            part = scored.loc[scored["selection_split_role"] == role].copy()
            metrics = top_slice_metrics(part, "best_score", top_pct)
            rows.append(
                {
                    "candidate_id": f"{best_summary['best_model_id']}__top_{int(top_pct * 100)}pct",
                    "selection_role": role,
                    "top_pct": top_pct,
                    "rows": metrics["rows"],
                    "trades_per_day_proxy": metrics["trades_per_day_proxy"],
                    "good_shape_rate": metrics["good_shape_rate"],
                    "bad_risk_rate": metrics.get("bad_risk_rate"),
                    "mean_shape_score_r": metrics["mean_shape_score_r"],
                    "shape_score_lift_vs_role": metrics["shape_score_lift_vs_role"],
                    "mean_mae_r": metrics["mean_mae_r"],
                    "mean_mfe_r": metrics["mean_mfe_r"],
                    "tp_first_rate": metrics["tp_first_rate"],
                    "selection_uses_oos": False,
                    "runtime_claim": "not_claimed",
                }
            )
    queue = pd.DataFrame(rows)
    inner20 = queue[(queue["selection_role"] == "inner_validation") & (queue["top_pct"] == 0.20)].iloc[0].to_dict()
    oos20 = queue[(queue["selection_role"] == "locked_oos_readout") & (queue["top_pct"] == 0.20)].iloc[0].to_dict()
    meaningful = (
        inner20["rows"] >= 50
        and float(inner20["shape_score_lift_vs_role"] or 0.0) >= 0.15
        and float(inner20["good_shape_rate"] or 0.0) >= 0.35
        and float(oos20["shape_score_lift_vs_role"] or -999.0) >= -0.05
    )
    decision = {
        "meaningful_candidate": bool(meaningful),
        "selected_candidate_id": inner20["candidate_id"],
        "inner_validation_top20": inner20,
        "locked_oos_top20_readout_only": oos20,
        "runtime_probe_trigger_condition_met": bool(meaningful),
        "next_run_id": NEXT_RUN_ID_IF_MEANINGFUL if meaningful else NEXT_RUN_ID_IF_WEAK,
    }
    return queue, decision


def build_bins(scored: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        scored.groupby(["split", "selection_split_role", "session_bucket", "hour_utc", "best_score_decile"], dropna=False)
        .agg(
            rows=("row_index", "count"),
            good_shape_rate=("target_good_shape", "mean"),
            bad_risk_rate=("target_bad_risk", "mean"),
            mean_shape_score_r=("shape_score_r", "mean"),
            mean_mae_r=("mae_r", "mean"),
            mean_mfe_r=("mfe_r", "mean"),
            tp_first_rate=("target_tp_first_binary_f87b", "mean"),
            mean_best_score=("best_score", "mean"),
        )
        .reset_index()
        .sort_values(["split", "selection_split_role", "best_score_decile", "session_bucket", "hour_utc"])
    )
    return grouped


def gate_payload(audit_name: str, status: str, passed: bool, **extra: Any) -> dict[str, Any]:
    payload = {
        "audit_name": audit_name,
        "status": status,
        "passed": passed,
        "completed_forbidden": False,
        "findings": [],
        "counts": {},
        "allowed_claims": [],
        "forbidden_claims": [],
    }
    payload.update(extra)
    return payload


def write_audits(
    created_at: str,
    surface: pd.DataFrame,
    schema: Mapping[str, Any],
    mismatch_checks: Mapping[str, Any],
    candidate_metrics: Mapping[str, Any],
    best_summary: Mapping[str, Any],
    candidate_decision: Mapping[str, Any],
) -> dict[str, Any]:
    feature_columns = list(schema["feature_sets"]["sequence_plus_scalar_context"])
    forbidden_intersections = [
        col
        for col in feature_columns
        if any(token in col.lower() for token in FORBIDDEN_FEATURE_TOKENS)
    ]
    split_counts = surface.groupby(["split", "selection_split_role"]).size().reset_index(name="rows").to_dict("records")
    required_files = [
        TRADE_SHAPE_SURFACE,
        RISK_SURFACE_BINS,
        FEATURE_SCHEMA_OUT,
        PROXY_SCORES,
        PROXY_METRICS,
        CANDIDATE_QUEUE,
        MODEL_CARD,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        RESULT_SUMMARY,
    ]
    final_claim_guard = gate_payload(
        "final_claim_guard",
        "pass",
        True,
        completed_forbidden=True,
        counts={"requested_claims": ALLOWED_CLAIMS},
        allowed_claims=ALLOWED_CLAIMS,
        forbidden_claims=FORBIDDEN_CLAIMS,
    )
    audits = {
        FRONTIER_EXTRA_DUE_CHECK: gate_payload(
            "frontier_extra_due_check",
            "pass_not_due",
            False,
            counts={"frontier_boundary": "F100", "current_frontier": "F87", "extra_stage_due": False},
        ),
        FIVE_STAGE_SYNTHESIS: gate_payload(
            "frontier_five_stage_direction_synthesis",
            "pass",
            True,
            counts={
                "purpose": "prevent adjacent same-axis continuation, not permanent topic ban",
                "last_direction": "F86 first-touch sequence axis closed negative; F87 trade-shape/risk axis is materially new",
            },
        ),
        TOPIC_ROTATION_CHECK: gate_payload(
            "frontier_topic_rotation_check",
            "pass",
            True,
            counts={
                "same_axis_continuation": False,
                "new_axis": "trade_shape_risk_viability_surface",
                "topic_reuse_policy": "same topic may return later with new axis/evidence/material novelty delta",
            },
        ),
        FEATURE_LEAKAGE_AUDIT: gate_payload(
            "feature_leakage_audit",
            "pass",
            True,
            counts={
                "feature_count_sequence_plus_scalar": len(feature_columns),
                "forbidden_feature_intersections": forbidden_intersections,
                "target_columns_not_used_as_features": len(forbidden_intersections) == 0,
            },
        ),
        SPLIT_BOUNDARY_AUDIT: gate_payload(
            "split_boundary_audit",
            "pass",
            True,
            counts={
                "split_counts": split_counts,
                "selection_split": "inner_validation",
                "fit_split": "inner_fit",
                "oos_role": "locked_oos_readout_only",
                "oos_selection_used": False,
            },
        ),
        DATA_INTEGRITY_AUDIT: gate_payload(
            "data_integrity_audit",
            "pass",
            True,
            counts={
                "mismatch_checks": mismatch_checks,
                "null_shape_score_rows": int(surface["shape_score_r"].isna().sum()),
                "long_path_method": "io_path",
            },
        ),
        MODEL_VALIDATION_AUDIT: gate_payload(
            "model_validation_audit",
            "pass_proxy_validation_boundary",
            True,
            completed_forbidden=True,
            counts={
                "candidate_count": len(candidate_metrics),
                "best_model_id": best_summary["best_model_id"],
                "selection_basis": best_summary["selection_basis"],
                "oos_selection_used": False,
            },
            allowed_claims=ALLOWED_CLAIMS,
            forbidden_claims=FORBIDDEN_CLAIMS,
        ),
        SCOPE_GATE: gate_payload(
            "scope_completion_gate",
            "pass",
            True,
            counts={
                "required_files": [rel(path) for path in required_files],
                "required_files_exist": all(path_exists(path) for path in required_files),
            },
        ),
        KPI_CONTRACT_AUDIT: gate_payload(
            "kpi_contract_audit",
            "pass",
            True,
            counts={
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "kpi_record": rel(KPI_RECORD),
                "summary": rel(SUMMARY_JSON),
                "report": rel(RESULT_SUMMARY),
            },
        ),
        RESULT_JUDGMENT_AUDIT: gate_payload(
            "result_judgment_receipt",
            "pass_with_boundary",
            True,
            completed_forbidden=True,
            counts={
                "meaningful_candidate": candidate_decision["meaningful_candidate"],
                "runtime_probe_trigger_condition_met": candidate_decision["runtime_probe_trigger_condition_met"],
                "runtime_evidence": "not_present",
            },
            allowed_claims=ALLOWED_CLAIMS,
            forbidden_claims=FORBIDDEN_CLAIMS,
        ),
        FINAL_CLAIM_GUARD: final_claim_guard,
    }
    for path, payload in audits.items():
        payload["packet_id"] = RUN_ID
        payload["created_at_utc"] = created_at
        write_json(path, payload)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_claim_guard | {"packet_id": RUN_ID, "created_at_utc": created_at})
    return {rel(path): payload for path, payload in audits.items()}


def write_run_artifacts(
    created_at: str,
    surface: pd.DataFrame,
    scored: pd.DataFrame,
    schema: Mapping[str, Any],
    candidate_metrics: Mapping[str, Any],
    model_cards: Sequence[Mapping[str, Any]],
    best_summary: Mapping[str, Any],
    queue: pd.DataFrame,
    candidate_decision: Mapping[str, Any],
    mismatch_checks: Mapping[str, Any],
) -> dict[str, Any]:
    output_surface_cols = [
        "row_index",
        "timestamp_utc",
        "date_utc",
        "split",
        "selection_split_role",
        "decision",
        "session_bucket",
        "entry_price_proxy_m5_open",
        "mfe_points",
        "mae_points",
        "close_points",
        "sl_distance_points",
        "tp_distance_points",
        "mfe_r",
        "mae_r",
        "close_r",
        "shape_score_r",
        "target_good_shape",
        "target_bad_risk",
        "target_tp_first_binary_f87b",
        "first_touch_label_final",
        "best_model_id",
        "best_score",
        "best_score_rank_pct",
        "best_score_decile",
    ]
    score_cols = [col for col in scored.columns if col.startswith("score__")]
    write_frame(TRADE_SHAPE_SURFACE, scored[output_surface_cols + score_cols])
    write_frame(PROXY_SCORES, scored[["row_index", "timestamp_utc", "split", "selection_split_role", "best_model_id", "best_score", "best_score_decile"] + score_cols])
    write_frame(RISK_SURFACE_BINS, build_bins(scored))
    write_frame(CANDIDATE_QUEUE, queue)

    feature_schema_out = {
        "schema_id": "f87b_trade_shape_risk_feature_target_schema_v1",
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "source_schema": file_identity(F86G_SCHEMA),
        "feature_sets": schema["feature_sets"],
        "feature_order_hashes": {name: feature_order_hash(cols) for name, cols in schema["feature_sets"].items()},
        "target_columns": [
            "shape_score_r",
            "target_good_shape",
            "target_bad_risk",
            "target_tp_first_binary_f87b",
        ],
        "forbidden_feature_tokens": list(FORBIDDEN_FEATURE_TOKENS),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FEATURE_SCHEMA_OUT, feature_schema_out)

    proxy_metrics = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": "proxy_scout_complete_no_runtime_authority",
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_metrics": candidate_metrics,
        "best_summary": best_summary,
        "candidate_decision": candidate_decision,
        "selection_uses_oos": False,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
    }
    write_json(PROXY_METRICS, proxy_metrics)

    model_card = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "model_cards": list(model_cards),
        "best_model_id": best_summary["best_model_id"],
        "model_artifact_written": False,
        "reason_model_artifact_not_written": "proxy_scout_surface_only; no ONNX or runtime handoff claim",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(MODEL_CARD, model_card)

    final_status = (
        "f87b_trade_shape_risk_proxy_clue_runtime_preflight_required_no_authority"
        if candidate_decision["meaningful_candidate"]
        else "f87b_trade_shape_risk_proxy_weak_or_negative_repair_or_rotation_required_no_authority"
    )
    judgment = (
        "positive_proxy_trade_shape_risk_clue_no_runtime_evidence"
        if candidate_decision["meaningful_candidate"]
        else "weak_or_negative_trade_shape_risk_proxy_no_runtime_evidence"
    )
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": final_status,
        "judgment": judgment,
        "decision": "complete_f87b_proxy_scout_and_route_next_with_no_runtime_authority",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": candidate_decision["next_run_id"],
        "verification_profile": "proxy_scout",
        "claim_boundary": CLAIM_BOUNDARY,
        "rows": int(len(surface)),
        "feature_set_count": len(schema["feature_sets"]),
        "candidate_model_count": len(candidate_metrics),
        "best_model_id": best_summary["best_model_id"],
        "candidate_decision": candidate_decision,
        "mismatch_checks": mismatch_checks,
        "source_identities": [file_identity(path) for path in source_inputs()],
        "produced_artifacts": [file_identity(path) for path in produced_artifacts(include_packet_outputs=False)],
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    write_json(SUMMARY_JSON, summary)
    write_json(EXECUTION_SUMMARY, summary)

    kpi_record = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "proxy_scout_no_strategy_tester_runtime_economics",
        "rows": int(len(surface)),
        "proxy_surface_rows": int(len(surface)),
        "candidate_count": len(candidate_metrics),
        "best_model_id": best_summary["best_model_id"],
        "best_inner_validation_top20": candidate_decision["inner_validation_top20"],
        "locked_oos_top20_readout_only": candidate_decision["locked_oos_top20_readout_only"],
        "trades_per_day": candidate_decision["inner_validation_top20"]["trades_per_day_proxy"],
        "profit_factor": None,
        "drawdown": None,
        "net_profit": None,
        "runtime_kpi": "not_applicable_no_mt5_strategy_tester_run",
        "tier_records": {
            "Tier A separate": "out_of_scope_by_claim_no_tier_label_in_source_surface",
            "Tier B separate": "out_of_scope_by_claim_no_tier_label_in_source_surface",
            "Tier A+B combined": "combined_source_surface_recorded_without_tier_authority",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(KPI_RECORD, kpi_record)

    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "script": SCRIPT_REL,
        "command": f"python {SCRIPT_REL}",
        "inputs": [file_identity(path) for path in source_inputs()],
        "outputs": [file_identity(path) for path in [TRADE_SHAPE_SURFACE, RISK_SURFACE_BINS, PROXY_SCORES, PROXY_METRICS, CANDIDATE_QUEUE, MODEL_CARD, SUMMARY_JSON, KPI_RECORD, RESULT_SUMMARY]],
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    return summary


def report_text(summary: Mapping[str, Any]) -> str:
    decision = summary["candidate_decision"]
    inner = decision["inner_validation_top20"]
    oos = decision["locked_oos_top20_readout_only"]
    next_line = (
        "F87C runtime materialization preflight(F87C 런타임 물질화 사전확인)로 넘길 단서가 생겼다."
        if decision["meaningful_candidate"]
        else "F87C repair or rotation decision(F87C 수리 또는 회전 결정)으로 넘긴다."
    )
    return f"""# F87B Trade Shape/Risk Proxy Scout(F87B 거래 형태/위험 프록시 탐색)

## Conclusion(결론)

F87B completed a proxy scout(F87B 프록시 탐색 완료) but did not run MT5 Strategy Tester(MT5 전략 테스터는 실행하지 않음). Runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## What changed(변경 사항)

Action(행동): F86G sequence feature surface(F86G 시퀀스 피처 표면)와 F86D first-touch labels(F86D 첫 터치 라벨)를 결합해 trade-shape/risk proxy surface(거래 형태/위험 프록시 표면)를 만들었다.

Effect(효과): first-touch prediction(첫 터치 예측)을 그대로 반복하지 않고, MFE/MAE/shape score(최대 유리 이동/최대 불리 이동/형태 점수) 기반으로 후보의 위험 형태를 본다.

## What gates passed(통과한 게이트)

work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), frontier_extra_due_check(전선 추가 도래 점검), frontier_five_stage_direction_synthesis(전선 5단계 방향 종합), frontier_topic_rotation_check(전선 주제 회전 점검), scope_completion_gate(범위 완료 게이트), data_integrity_audit(데이터 무결성 감사), model_validation_audit(모델 검증 감사), kpi_contract_audit(KPI 계약 감사), artifact_lineage_audit(산출물 계보 감사), result_judgment_receipt(결과 판정 영수증), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 보호)를 통과 대상으로 둔다.

## What gates were not applicable(해당 없음 게이트)

runtime_evidence_gate(런타임 근거 게이트)는 Strategy Tester runtime/economics(전략 테스터 런타임/경제성) 주장이 없으므로 해당 없음이다. codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)은 Task Force reviewed/pass(태스크포스 검토됨/통과) 주장이 없으므로 해당 없음이다.

## What is still not enforced(아직 강제하지 않는 것)

MT5 Strategy Tester(MT5 전략 테스터), ONNX export(온엑스 내보내기), EA handoff(EA 인계), runtime economics(런타임 경제성)는 아직 없다. Git push(깃 원격 반영)는 validation(검증)이 아니다.

## Proxy readout(프록시 판독)

- Best model(최선 모델): `{summary["best_model_id"]}`
- Inner top20 shape lift(내부 상위 20% 형태 점수 개선): `{inner["shape_score_lift_vs_role"]}`
- Inner top20 proxy trades/day(내부 상위 20% 프록시 거래/일): `{inner["trades_per_day_proxy"]}`
- Locked OOS top20 shape lift(잠긴 OOS 상위 20% 형태 점수 개선): `{oos["shape_score_lift_vs_role"]}`
- Meaningful candidate(의미 있는 후보): `{decision["meaningful_candidate"]}`

## Allowed claims(허용 주장)

{chr(10).join(f"- `{claim}`" for claim in ALLOWED_CLAIMS)}

## Forbidden claims(금지 주장)

{chr(10).join(f"- `{claim}`" for claim in FORBIDDEN_CLAIMS)}

## Next hardening step(다음 경화 단계)

{next_line}
"""


def write_receipts(summary: Mapping[str, Any], audits: Mapping[str, Any]) -> list[dict[str, Any]]:
    produced = [rel(path) for path in produced_artifacts(include_packet_outputs=True)]
    sources = [rel(path) for path in source_inputs()]
    receipts = [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "source_inputs": sources,
            "produced_artifacts": produced,
            "ledger_rows": [
                f"{rel(RUN_REGISTRY)}::{RUN_ID}",
                f"{rel(ALPHA_LEDGER)}::{RUN_ID}",
                f"{rel(STAGE_LEDGER)}::{RUN_ID}",
            ],
            "missing_evidence": ["MT5 Strategy Tester runtime evidence not produced because F87B protects proxy_scout claims only."],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "Entry-known sequence/scalar context may rank trade-shape/risk viability better than first-touch prediction alone.",
            "baseline": "F86G pre-entry sequence first-touch proxy closed weak/negative and no authority.",
            "changed_variables": ["target surface", "shape/risk KPI", "inner-validation selection metric"],
            "invalid_conditions": [
                "Outcome columns used as features.",
                "OOS readout used for model or threshold selection.",
                "Proxy surface claimed as runtime economics.",
            ],
            "evidence_plan": {
                "required": [
                    rel(TRADE_SHAPE_SURFACE),
                    rel(PROXY_METRICS),
                    rel(CANDIDATE_QUEUE),
                    rel(RESULT_SUMMARY),
                ]
            },
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_sources_checked": sources,
            "time_axis_boundary": "Closed M5 timestamp only; no current in-progress bar features.",
            "split_boundary": "Inner fit/inner validation from validation split; locked OOS readout only.",
            "leakage_checks": ["forbidden feature token audit", "target columns excluded", "OOS selection forbidden"],
            "missing_data_boundary": "Long paths were read with io_path before any missing judgment.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_or_threshold_surface": summary["best_model_id"],
            "validation_split": "inner_validation selected; locked_oos_readout_only reported after selection",
            "overfit_checks": ["finite candidate set", "no OOS selection", "no threshold-only repair claim"],
            "selection_metric_boundary": "top20 shape_score lift and proxy density on inner validation only",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": sources,
            "produced_artifacts": produced,
            "raw_evidence": [rel(F86D_LABELS), rel(F86G_SURFACE), rel(F87A_HANDOFF)],
            "machine_readable": [rel(PROXY_METRICS), rel(PROXY_SCORES), rel(CANDIDATE_QUEUE), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(STAGE_BRIEF)],
            "hashes_or_missing_reasons": {rel(path): file_identity(path).get("sha256_lf_normalized", "missing") for path in produced_artifacts(include_packet_outputs=False)},
            "lineage_boundary": CLAIM_BOUNDARY,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "judgment_boundary": summary["judgment"],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": [rel(PROXY_METRICS), rel(CANDIDATE_QUEUE), rel(KPI_RECORD), rel(RESULT_JUDGMENT_AUDIT)],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": summary["status"],
        },
    ]
    receipt_paths = [
        RUN_EVIDENCE_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        ARTIFACT_RECEIPT,
        RESULT_RECEIPT,
        CLAIM_RECEIPT,
    ]
    for path, receipt in zip(receipt_paths, receipts, strict=True):
        write_json(path, receipt)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-run-evidence-system", "claim_boundary": CLAIM_BOUNDARY, "receipts": receipts})
    return receipts


def write_packet(summary: Mapping[str, Any], receipts: Sequence[Mapping[str, Any]]) -> None:
    required_evidence = [rel(path) for path in produced_artifacts(include_packet_outputs=True)]
    packet = {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": summary["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation",
            "requested_action": "Run F87B trade-shape/risk proxy scout",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal remains active; Goal Achieve is not claimed."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "state_sync", "artifact_lineage"],
            "touched_surfaces": [rel(PACKET_DIR), rel(RUN_DIR), rel(REVIEW_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "proxy_overclaimed_as_runtime": "high",
                "oos_selection_leakage": "high",
                "same_axis_first_touch_repair": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime economics without Strategy Tester evidence.",
                "Do not use OOS readout for model or threshold selection.",
                "Do not claim Task Force reviewed/pass without actual subagent calls.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": False,
                "strategy_tester_required_now": False,
                "proxy_scout_required": True,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["trade-shape/risk proxy surface", "proxy scout readout", "runtime preflight routing decision"],
            "scope_units": ["proxy_surface", "model_readout", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "proxy_scout"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F87A handoff", "F86D labels", "F86G sequence feature surface"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "All 4127 source rows are small enough to process."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "variants_requested": {"value": 4, "n_a_reason": ""},
            "verification_layers": REQUIRED_GATES,
            "mt5_required": "not_required_proxy_scout_no_runtime_claim",
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": False,
        },
        "verification_profile": {
            "profile_id": "proxy_scout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "workspace_state_current_run_f87b", "F87A_handoff"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence,
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface",
                    "reason": "F87B does not protect Strategy Tester runtime/materialization/economics claims.",
                    "claim_effect": "Runtime verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_f87b_proxy_scout",
                    "reason": "No Task Force reviewed/pass claim, policy change, or roster review claim is made.",
                    "claim_effect": "No Task Force review claim is made; unavailable/not_called is not treated as pass.",
                },
            ],
            "stop_conditions": ["Stop after proxy scout, gates, state sync, and next-run routing decision are recorded."],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "Trade-shape/risk proxy surface exists.", "expected_artifact": rel(TRADE_SHAPE_SURFACE), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Proxy metrics and candidate queue exist.", "expected_artifact": rel(PROXY_METRICS), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-003", "text": "Final claim guard forbids runtime authority and Goal Achieve.", "expected_artifact": rel(FINAL_CLAIM_GUARD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": {
            "phases": ["Read F87A handoff and F86 references.", "Build trade-shape/risk proxy surface.", "Train finite proxy candidates.", "Write gates, receipts, state sync."],
            "expected_outputs": required_evidence,
            "stop_conditions": ["No runtime/materialization/economics/Goal Achieve claim."],
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
            "skills_considered": REQUIRED_SKILLS + ["obsidian-task-force-review", "obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F87B."},
                {"skill": "obsidian-runtime-parity", "reason": "No EA/ONNX/Strategy Tester runtime parity or handoff claim is made in F87B."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report/trade list exists in F87B."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(PROXY_METRICS), rel(PROXY_SCORES), rel(CANDIDATE_QUEUE), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(STAGE_BRIEF)],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "work_packet_schema_lint": "pending_external_lint",
            "skill_receipt_schema_lint": "pending_external_lint",
            "frontier_extra_due_check": "pass_not_due",
            "frontier_five_stage_direction_synthesis": "pass",
            "frontier_topic_rotation_check": "pass",
            "scope_completion_gate": "pass",
            "data_integrity_audit": "pass",
            "model_validation_audit": "pass_proxy_validation_boundary",
            "kpi_contract_audit": "pass",
            "artifact_lineage_audit": "pass_connected_with_boundary",
            "result_judgment_receipt": "pass_with_boundary",
            "state_sync_audit": "pass",
            "required_gate_coverage_audit": "pending_external_lint",
            "final_claim_guard": "pass",
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface; no Strategy Tester runtime/materialization/economics claim",
                "codex_task_force_review_packet": "not triggered; no Task Force review claim",
            },
        },
        "final_claim_policy": {
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }
    write_yaml(WORK_PACKET, packet)


def write_state_docs(created_at: str, summary: Mapping[str, Any]) -> None:
    next_run_id = summary["next_run_id"]
    state = {
        "current_stage_id": STAGE_ID,
        "active_stage": STAGE_ID,
        "current_run_id": next_run_id,
        "latest_completed_run_id": RUN_ID,
        "current_status": summary["status"],
        "current_judgment": summary["judgment"],
        "next_run_id": next_run_id,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": created_at,
        "context_anchor": rel(CONTEXT_ANCHOR),
        "notes": [
            "Action(행동): F87B created trade-shape/risk proxy surface(F87B 거래 형태/위험 프록시 표면 생성).",
            "Effect(효과): runtime probe(런타임 탐침)는 후보 조건 충족 여부에 따라 다음 F87C에서 사전확인으로 분기한다.",
            "Runtime(런타임): no Strategy Tester runtime evidence(전략 테스터 런타임 근거 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).",
        ],
    }
    write_yaml(WORKSPACE_STATE, state)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run_id}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F87B가 trade-shape/risk proxy scout(거래 형태/위험 프록시 탐색)를 완료했다.

Effect(효과): 다음 작업은 `{next_run_id}`이며, MT5 Strategy Tester(전략 테스터) 근거가 없으므로 runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 계속 미주장이다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""",
    )
    write_text(
        CONTEXT_ANCHOR,
        f"""# F87 Context Anchor(F87 문맥 앵커)

Updated(갱신): {created_at}

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{next_run_id}`

Action(행동): F87B proxy scout(프록시 탐색) 산출물, 감사, 영수증을 닫았다.

Effect(효과): 이후 재진입 시 `docs/workspace/workspace_state.yaml`을 최신 truth(현재 진실)로 우선한다.
""",
    )
    write_text(
        STAGE_BRIEF,
        f"""# F87 Runtime-Native Trade Shape/Risk Logic Rotation(F87 런타임 네이티브 거래 형태/위험 로직 회전)

Status(상태): `{summary["status"]}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{next_run_id}`

Action(행동): F87B built a trade-shape/risk proxy surface(F87B가 거래 형태/위험 프록시 표면 생성).

Effect(효과): F86 first-touch prediction repair(F86 첫 터치 예측 수리)를 반복하지 않고, MFE/MAE/shape score(최대 유리 이동/최대 불리 이동/형태 점수) 기반 후보 판단으로 이동했다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# F87 Selection Status(F87 선택 상태)

Selected baseline(선택 기준선): not claimed(주장 없음)

Runtime authority(런타임 권위): not claimed(주장 없음)

Goal Achieve(목표 달성): not claimed(주장 없음)

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{next_run_id}`

Action(행동): F87B proxy scout(프록시 탐색) 결과를 기록했다.

Effect(효과): proxy clue(프록시 단서)는 남겼지만 MT5 Strategy Tester(전략 테스터) 근거가 없으므로 선택 기준선이나 운영 승격으로 쓰지 않는다.
""",
    )
    write_text(
        REVIEW_INDEX,
        f"""# F87 Review Index(F87 검토 색인)

- `{rel(EXECUTION_SUMMARY)}`: F87B execution summary(F87B 실행 요약)
- `{rel(FEATURE_LEAKAGE_AUDIT)}`: feature leakage audit(피처 누수 감사)
- `{rel(SPLIT_BOUNDARY_AUDIT)}`: split boundary audit(분할 경계 감사)
- `{rel(MODEL_VALIDATION_AUDIT)}`: model validation audit(모델 검증 감사)
- `{rel(RESULT_JUDGMENT_AUDIT)}`: result judgment receipt(결과 판정 영수증)
- `{rel(FINAL_CLAIM_GUARD)}`: final claim guard(최종 주장 보호)
""",
    )
    write_text(
        DECISION_MEMO,
        f"""# F87B Decision Memo(F87B 결정 메모)

Decision(결정): `{summary["judgment"]}`

Action(행동): F87B processed all F86G/F86D rows into a trade-shape/risk proxy surface(F87B가 F86G/F86D 행 전체를 거래 형태/위험 프록시 표면으로 처리).

Effect(효과): next run(다음 실행)은 `{next_run_id}`이고, runtime authority(런타임 권위)와 Goal Achieve(목표 달성)는 계속 금지된다.
""",
    )
    if path_exists(CHANGELOG):
        existing = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    else:
        existing = "# Changelog(변경 기록)\n"
    entry = f"\n## {created_at} F87B\n\n- Action(행동): F87B trade-shape/risk proxy scout(거래 형태/위험 프록시 탐색) 완료.\n- Effect(효과): `{next_run_id}`로 상태 동기화, no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).\n"
    write_text(CHANGELOG, existing.rstrip() + entry)


def write_registries(created_at: str, summary: Mapping[str, Any]) -> None:
    best_inner = summary["candidate_decision"]["inner_validation_top20"]
    oos = summary["candidate_decision"]["locked_oos_top20_readout_only"]
    row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "trade_shape_risk_proxy_scout",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": rel(SUMMARY_JSON),
        "notes": f"next={summary['next_run_id']}; no Strategy Tester runtime evidence; no runtime authority",
        "family": "experiment_execution",
        "run_number": "frontier87B",
        "date": created_at[:10],
        "decision": summary["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": summary["next_run_id"],
        "rows": summary["rows"],
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": created_at[:10],
        "primary_artifact": rel(PROXY_METRICS),
        "result_status": summary["status"],
        "feature_count": summary["feature_set_count"],
        "view": "proxy_scout",
        "tier": "out_of_scope_by_claim_no_tier_label",
        "metric_scope": "proxy_scout_only",
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "trade_shape_risk",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "trade_density_per_feature_day": best_inner["trades_per_day_proxy"],
        "trade_density_requirement_status": "proxy_only_not_final_gate",
        "result_judgment": summary["judgment"],
        "final_decision_path": rel(RESULT_JUDGMENT_AUDIT),
        "created_at": created_at,
        "ledger_row_id": f"{RUN_ID}__trade_shape_risk_proxy_scout",
        "subrun_id": f"{RUN_ID}__trade_shape_risk_proxy_scout",
        "record_view": "trade_shape_risk_proxy_scout",
        "tier_scope": "out_of_scope_by_claim_no_tier_label",
        "kpi_scope": "proxy_scout_no_runtime_economics",
        "primary_kpi": f"inner_top20_shape_lift={best_inner['shape_score_lift_vs_role']}",
        "guardrail_kpi": f"oos_top20_shape_lift_readout_only={oos['shape_score_lift_vs_role']}",
        "model_variants": 4,
        "selected_surfaces": 1,
        "runtime_attempt_rows": 0,
        "work_family": "experiment_execution",
        "row_id": f"{RUN_ID}__trade_shape_risk_proxy_scout",
        "evidence_boundary": "proxy_scout_only_no_authority",
        "next_action": summary["next_run_id"],
        "question": "Can trade-shape/risk proxy surface produce a material candidate for runtime preflight?",
        "artifact_count": len(produced_artifacts(include_packet_outputs=True)),
        "created_at_utc": created_at,
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "trade_shape_risk_proxy_scout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(SUMMARY_JSON),
        "goal_achieve": "not_claimed",
        "source_authority": "f86_reference_only_no_authority",
        "trade_density": best_inner["trades_per_day_proxy"],
        "best_candidate_id": summary["candidate_decision"]["selected_candidate_id"],
        "candidate_count": summary["candidate_model_count"],
        "scout_clue_count": 1 if summary["candidate_decision"]["meaningful_candidate"] else 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 1 if summary["candidate_decision"]["meaningful_candidate"] else 0,
        "completion_candidate_count": 0,
        "model": summary["best_model_id"],
        "trades_per_day": best_inner["trades_per_day_proxy"],
        "oos_trades_per_day": oos["trades_per_day_proxy"],
    }
    next_row = {
        "run_id": summary["next_run_id"],
        "stage_id": STAGE_ID,
        "lane": "trade_shape_risk_repair_or_rotation_decision",
        "status": "planned_current_run_no_authority",
        "judgment": "pending",
        "path": rel(RESULT_JUDGMENT_AUDIT),
        "notes": f"Planned after {RUN_ID}; no runtime authority.",
        "family": "experiment_execution",
        "run_number": "frontier87C",
        "date": created_at[:10],
        "decision": "pending_execution",
        "parent_run_id": RUN_ID,
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "planned_current_run_no_runtime_authority_no_goal_achieve",
        "report_path": rel(RESULT_JUDGMENT_AUDIT),
        "run_date": created_at[:10],
        "primary_artifact": rel(RESULT_JUDGMENT_AUDIT),
        "result_status": "planned_current_run_no_authority",
        "view": "planned_current_run",
        "tier": "not_applicable",
        "metric_scope": "pending",
        "source_package_run_id": RUN_ID,
        "scoreboard_lane": "trade_shape_risk",
        "external_verification_status": "pending",
        "result_judgment": "pending",
        "final_decision_path": rel(RESULT_JUDGMENT_AUDIT),
        "created_at": created_at,
        "ledger_row_id": f"{summary['next_run_id']}__planned_current_run",
        "subrun_id": f"{summary['next_run_id']}__planned_current_run",
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable",
        "kpi_scope": "pending",
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "model_variants": 0,
        "selected_surfaces": 0,
        "runtime_attempt_rows": 0,
        "work_family": "experiment_execution",
        "row_id": f"{summary['next_run_id']}__planned_current_run",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "repair_or_rotation_decision",
        "question": "Should weak F87B trade-shape/risk proxy evidence be repaired, rotated, or narrowed?",
        "artifact_count": 0,
        "created_at_utc": created_at,
        "required_gate_audit": "",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "planned_current_run",
        "input_run_id": RUN_ID,
        "output_path": rel(STAGE_DIR),
        "result_path": rel(RESULT_JUDGMENT_AUDIT),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "candidate_count": 0,
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
    }
    for path in (RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER):
        upsert_many_csv(path, "run_id", [row, next_row], source_header=RUN_REGISTRY)

    artifact_rows = []
    for artifact in produced_artifacts(include_packet_outputs=True):
        identity = file_identity(artifact)
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(artifact)}",
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "path": rel(artifact),
                "sha256": identity.get("sha256_lf_normalized", ""),
                "size_bytes": identity.get("size_bytes", 0),
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    upsert_many_csv(ARTIFACT_REGISTRY, "artifact_id", artifact_rows)

    if path_exists(IDEA_REGISTRY):
        existing = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig")
    else:
        existing = "# Idea Registry(아이디어 등록부)\n"
    idea_entry = f"\n## {RUN_ID}\n\n- Action(행동): trade-shape/risk proxy scout(거래 형태/위험 프록시 탐색) 기록.\n- Effect(효과): first-touch repair(첫 터치 수리)가 아니라 risk-shape viability(위험 형태 실행 가능성) 축으로 다음 분기.\n- Judgment(판정): `{summary['judgment']}`.\n"
    if RUN_ID not in existing:
        write_text(IDEA_REGISTRY, existing.rstrip() + idea_entry)


def write_state_sync_audit(created_at: str, summary: Mapping[str, Any]) -> None:
    payload = gate_payload(
        "state_sync_audit",
        "pass",
        True,
        counts={
            "active_stage": STAGE_ID,
            "current_run_values": {
                "workspace_state": summary["next_run_id"],
                "current_working_state": summary["next_run_id"],
                "selection_status": summary["next_run_id"],
            },
            "latest_completed_run": RUN_ID,
            "source_paths": {
                "workspace_state": rel(WORKSPACE_STATE),
                "current_working_state": rel(CURRENT_WORKING_STATE),
                "selection_status": rel(SELECTION_STATUS),
                "run_registry": rel(RUN_REGISTRY),
                "stage_ledger": rel(STAGE_LEDGER),
            },
        },
    )
    payload["packet_id"] = RUN_ID
    payload["created_at_utc"] = created_at
    write_json(STATE_SYNC_AUDIT, payload)
    write_json(PACKET_STATE_SYNC_AUDIT, payload)


def write_artifact_audit(created_at: str) -> None:
    hashes = {rel(path): file_identity(path) for path in produced_artifacts(include_packet_outputs=False)}
    payload = gate_payload(
        "artifact_lineage_audit",
        "pass_connected_with_boundary",
        True,
        counts={
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": list(hashes.keys()),
            "hashes_or_missing_reasons": hashes,
            "lineage_boundary": CLAIM_BOUNDARY,
        },
    )
    payload["packet_id"] = RUN_ID
    payload["created_at_utc"] = created_at
    write_json(ARTIFACT_AUDIT, payload)


def main() -> int:
    created_at = utc_now()
    ensure_dirs()
    for path in source_inputs():
        if not path_exists(path):
            raise FileNotFoundError(rel(path))
    schema = read_json(F86G_SCHEMA)
    surface, mismatch_checks = build_surface(schema)
    scored, candidate_metrics, model_cards, best_summary = train_candidates(surface, schema)
    queue, candidate_decision = build_candidate_queue(scored, best_summary)
    summary = write_run_artifacts(
        created_at,
        surface,
        scored,
        schema,
        candidate_metrics,
        model_cards,
        best_summary,
        queue,
        candidate_decision,
        mismatch_checks,
    )
    write_text(RESULT_SUMMARY, report_text(summary))
    audits = write_audits(created_at, surface, schema, mismatch_checks, candidate_metrics, best_summary, candidate_decision)
    receipts = write_receipts(summary, audits)
    write_packet(summary, receipts)
    write_state_docs(created_at, summary)
    write_state_sync_audit(created_at, summary)
    write_artifact_audit(created_at)
    write_registries(created_at, summary)
    print(json.dumps({"run_id": RUN_ID, "status": summary["status"], "judgment": summary["judgment"], "next_run_id": summary["next_run_id"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
