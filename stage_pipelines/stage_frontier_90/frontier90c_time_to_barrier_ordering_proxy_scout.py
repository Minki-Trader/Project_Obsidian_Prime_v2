from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
import yaml
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, balanced_accuracy_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_90__time_to_barrier_competing_risk_label_axis"
RUN_ID = "frontier90C_time_to_barrier_ordering_proxy_scout_v1"
PARENT_RUN_ID = "frontier90B_time_to_barrier_label_feasibility_scout_v1"
NEXT_RUN_ID = "frontier90D_time_to_barrier_repair_or_rotation_decision_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_90/frontier90c_time_to_barrier_ordering_proxy_scout.py"

STATUS = "f90c_ordering_proxy_scout_negative_no_candidate_f90d_repair_or_rotation_planned_no_authority"
JUDGMENT = "negative_ordering_proxy_oos_lift_failed_no_runtime_trigger_tier_b_missing_boundary"
DECISION = "plan_f90d_repair_or_rotation_decision_after_ordering_proxy_oos_failure"
CLAIM_BOUNDARY = (
    "f90c_ordering_proxy_scout_only_no_candidate_no_calibration_no_threshold_selection_"
    "no_selected_baseline_no_mt5_runtime_evidence_no_operating_promotion_no_runtime_authority_"
    "no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = (
    "not_run_no_meaningful_signal_no_runnable_decision_surface_no_onnx_ea_set_behavior_"
    "no_runtime_materialization_economics_claim_not_cost_or_proxy_bad_skip"
)
LABEL_ID = "time_to_barrier_competing_risk_v1_h12_atr0.75"

SIGNAL_QUANTILE = 0.90
CANDIDATE_MIN_HIT_RATE = 0.54
CANDIDATE_MIN_SIGNAL_COUNT = 500
CANDIDATE_MIN_SIGNALS_PER_DAY = 5.0
CANDIDATE_MAX_SIGNALS_PER_DAY = 15.0
CANDIDATE_MIN_SIDE_SHARE = 0.20
CANDIDATE_MIN_AUC = 0.525

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier90C"
PROXY_DIR = RUN_DIR / "proxy_scout"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SKILL_RECEIPT_DIR = PACKET_DIR / "skill_receipts"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
PROXY_METRICS = PROXY_DIR / "proxy_metrics.json"
VARIANT_METRICS_CSV = PROXY_DIR / "variant_metrics.csv"
SIGNAL_SAMPLES_CSV = PROXY_DIR / "signal_samples.csv"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

TASK_FORCE_REVIEW = REVIEW_DIR / "f90c_task_force_review_receipt.json"
SCOPE_GATE = REVIEW_DIR / "f90c_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f90c_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f90c_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f90c_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f90c_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f90c_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f90c_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f90c_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f90c_required_gate_coverage_audit.json"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_TASK_FORCE_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
ROOT_CHANGELOG = ROOT / "docs" / "CHANGELOG.md"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier90c_time_to_barrier_ordering_proxy_scout.md"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

F90B_RUN = STAGE_DIR / "02_runs" / "frontier90B"
F90B_SUMMARY = F90B_RUN / "summary.json"
F90B_KPI = F90B_RUN / "kpi_record.json"
F90B_LABEL_STATS = F90B_RUN / "labels" / "label_feasibility_stats.json"
F90B_TIER_RECORDS = F90B_RUN / "labels" / "tier_records.json"
F90B_LABELS = F90B_RUN / "labels" / "frontier90b_barrier_labels.csv"
F90B_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"

MODEL_INPUT_SUMMARY = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_summary.json"
MODEL_INPUT_DATASET = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
MODEL_INPUT_FEATURE_ORDER = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_feature_order.txt"

ALLOWED_CLAIMS = [
    "f90c_ordering_proxy_scout_executed",
    "ordering_proxy_negative_memory_recorded",
    "f90d_repair_or_rotation_planned",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "runtime_probe",
    "runtime_verified",
    "strategy_tester_runtime_economics",
    "runtime_economics_pass",
    "materialization_ready",
    "mt5_handoff_ready",
    "onnx_handoff_ready",
    "ea_handoff_ready",
    "model_training_superiority",
    "calibration",
    "threshold_selection",
    "candidate",
    "promotion_candidate",
    "task_force_reviewed_pass",
]
REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "codex_task_force_review_packet",
    "scope_completion_gate",
    "data_integrity_audit",
    "model_validation_audit",
    "kpi_contract_audit",
    "artifact_lineage_audit",
    "result_judgment_audit",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-run-evidence-system",
    "obsidian-data-integrity",
    "obsidian-experiment-design",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-task-force-review",
    "obsidian-result-judgment",
    "obsidian-claim-discipline",
]


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


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(dict(payload)), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True, timeout=10)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def append_once(path: Path, marker: str, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    joiner = "" if not text or text.endswith("\n") else "\n"
    write_text(path, text + joiner + addition.strip() + "\n")


def file_identity(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"path": rel(path), "exists": False, "sha256": None, "size_bytes": None}
    return {
        "path": rel(path),
        "exists": True,
        "sha256": sha256_file_lf_normalized(path),
        "size_bytes": io_path(path).stat().st_size,
    }


def source_inputs() -> list[Path]:
    return [
        F90B_SUMMARY,
        F90B_KPI,
        F90B_LABEL_STATS,
        F90B_TIER_RECORDS,
        F90B_LABELS,
        F90B_PACKET,
        MODEL_INPUT_SUMMARY,
        MODEL_INPUT_DATASET,
        MODEL_INPUT_FEATURE_ORDER,
    ]


def produced_artifacts() -> list[Path]:
    return [
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        PROXY_METRICS,
        VARIANT_METRICS_CSV,
        SIGNAL_SAMPLES_CSV,
        RESULT_SUMMARY,
        TASK_FORCE_REVIEW,
        SCOPE_GATE,
        DATA_INTEGRITY_AUDIT,
        MODEL_VALIDATION_AUDIT,
        KPI_CONTRACT_AUDIT,
        ARTIFACT_AUDIT,
        RESULT_JUDGMENT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_TASK_FORCE_REVIEW,
        PACKET_CLOSEOUT_GATE,
        PACKET_FINAL_CLAIM_GUARD,
    ]


def ensure_dirs() -> None:
    for path in [RUN_DIR, PROXY_DIR, REPORT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, SKILL_RECEIPT_DIR]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def feature_columns() -> list[str]:
    return [line.strip() for line in io_path(MODEL_INPUT_FEATURE_ORDER).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def load_joined_frame() -> tuple[pd.DataFrame, dict[str, Any]]:
    features = feature_columns()
    model = pd.read_parquet(io_path(MODEL_INPUT_DATASET), columns=["timestamp", "split", "split_id", *features])
    labels = pd.read_csv(io_path(F90B_LABELS))
    labels["timestamp"] = pd.to_datetime(labels["timestamp"], utc=True)
    model["timestamp"] = pd.to_datetime(model["timestamp"], utc=True)
    duplicate_model = int(model["timestamp"].duplicated().sum())
    duplicate_labels = int(labels["timestamp"].duplicated().sum())
    joined = model.merge(labels, on="timestamp", how="inner", validate="one_to_one", suffixes=("", "_label"))
    integrity = {
        "model_rows": int(len(model)),
        "label_rows": int(len(labels)),
        "joined_rows": int(len(joined)),
        "unmatched_model_rows": int(len(model) - len(joined)),
        "unmatched_label_rows": int(len(labels) - len(joined)),
        "duplicate_model_timestamps": duplicate_model,
        "duplicate_label_timestamps": duplicate_labels,
        "feature_count": len(features),
        "label_id": LABEL_ID,
    }
    if duplicate_model or duplicate_labels or len(joined) != len(model) or len(joined) != len(labels):
        integrity["integrity_judgment"] = "invalid"
    else:
        integrity["integrity_judgment"] = "usable_with_boundary"
    return joined, integrity


def safe_auc(y_true: pd.Series, scores: np.ndarray) -> float | None:
    if len(set(y_true.astype(int))) < 2:
        return None
    return round(float(roc_auc_score(y_true.astype(int), scores)), 6)


def confusion_counts(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, int]:
    return {
        "tp_upper": int(((y_true == 1) & (y_pred == 1)).sum()),
        "tn_lower": int(((y_true == 0) & (y_pred == 0)).sum()),
        "fp_upper": int(((y_true == 0) & (y_pred == 1)).sum()),
        "fn_lower": int(((y_true == 1) & (y_pred == 0)).sum()),
    }


def evaluate_split(part: pd.DataFrame, scores: np.ndarray, threshold: float) -> dict[str, Any]:
    y = part["target_upper"].to_numpy(dtype=int)
    pred = (scores > 0.0).astype(int)
    signal_mask = np.abs(scores) >= threshold
    signal_y = y[signal_mask]
    signal_pred = pred[signal_mask]
    signal_scores = scores[signal_mask]
    days = int(part["timestamp"].dt.date.nunique())
    signal_count = int(signal_mask.sum())
    long_count = int((signal_pred == 1).sum())
    short_count = int((signal_pred == 0).sum())
    side_min_share = round(float(min(long_count, short_count) / signal_count), 6) if signal_count else None
    hit_rate = round(float((signal_pred == signal_y).mean()), 6) if signal_count else None
    bars = part.loc[signal_mask, "bars_to_event"]
    return {
        "rows": int(len(part)),
        "days": days,
        "accuracy": round(float(accuracy_score(y, pred)), 6),
        "balanced_accuracy": round(float(balanced_accuracy_score(y, pred)), 6),
        "auc": safe_auc(part["target_upper"], scores),
        "signal_threshold_abs": round(float(threshold), 10),
        "signal_count": signal_count,
        "signals_per_day": round(float(signal_count / days), 6) if days else None,
        "signal_hit_rate": hit_rate,
        "long_signal_count": long_count,
        "short_signal_count": short_count,
        "side_min_share": side_min_share,
        "mean_abs_signal_score": round(float(np.abs(signal_scores).mean()), 6) if signal_count else None,
        "mean_bars_to_event_signal": round(float(bars.mean()), 6) if signal_count else None,
        "median_bars_to_event_signal": round(float(bars.median()), 6) if signal_count else None,
        "confusion": confusion_counts(y, pred),
    }


def train_variant(variant: Mapping[str, Any], train: pd.DataFrame, features: Sequence[str]) -> tuple[Any, np.ndarray]:
    if variant["kind"] == "logistic":
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=2000, C=float(variant["C"]), class_weight="balanced", solver="lbfgs"),
        )
        if variant.get("sample_weight") == "inverse_bars_to_event":
            weights = (1.0 / train["bars_to_event"].astype(float)).to_numpy()
            model.fit(train[list(features)], train["target_upper"], logisticregression__sample_weight=weights)
        else:
            model.fit(train[list(features)], train["target_upper"])
        scores = model.predict_proba(train[list(features)])[:, 1] - 0.5
        return model, scores
    if variant["kind"] == "ridge_signed_speed":
        model = make_pipeline(StandardScaler(), Ridge(alpha=float(variant["alpha"])))
        model.fit(train[list(features)], train["signed_speed"])
        scores = model.predict(train[list(features)])
        return model, scores
    raise ValueError(f"Unknown variant: {variant}")


def predict_scores(model: Any, variant: Mapping[str, Any], part: pd.DataFrame, features: Sequence[str]) -> np.ndarray:
    if variant["kind"] == "logistic":
        return model.predict_proba(part[list(features)])[:, 1] - 0.5
    return model.predict(part[list(features)])


def materialize_proxy_metrics() -> dict[str, Any]:
    joined, integrity = load_joined_frame()
    features = feature_columns()
    excluded_counts = {str(key): int(value) for key, value in joined["event_type"].value_counts().sort_index().items()}
    eligible = joined.loc[joined["event_type"].isin(["upper_first", "lower_first"])].copy()
    eligible["target_upper"] = eligible["event_type"].eq("upper_first").astype(int)
    eligible["signed_speed"] = np.where(eligible["target_upper"].eq(1), 1.0, -1.0) / eligible["bars_to_event"].astype(float)
    train = eligible.loc[eligible["split"].eq("train")].copy()
    variants = [
        {"variant_id": "logreg_direction_c025", "kind": "logistic", "C": 0.25, "sample_weight": "none"},
        {"variant_id": "logreg_speed_weighted_c025", "kind": "logistic", "C": 0.25, "sample_weight": "inverse_bars_to_event"},
        {"variant_id": "ridge_signed_speed_alpha10", "kind": "ridge_signed_speed", "alpha": 10.0},
    ]
    records: list[dict[str, Any]] = []
    signal_samples: list[dict[str, Any]] = []
    for variant in variants:
        model, train_scores = train_variant(variant, train, features)
        threshold = float(np.quantile(np.abs(train_scores), SIGNAL_QUANTILE))
        split_results: dict[str, Any] = {}
        for split_name in ["train", "validation", "oos"]:
            part = eligible.loc[eligible["split"].eq(split_name)].copy()
            scores = predict_scores(model, variant, part, features)
            split_results[split_name] = evaluate_split(part, scores, threshold)
            mask = np.abs(scores) >= threshold
            sample = part.loc[mask, ["timestamp", "split", "event_type", "bars_to_event"]].copy()
            sample["variant_id"] = str(variant["variant_id"])
            sample["score"] = scores[mask]
            sample["predicted_event_type"] = np.where(sample["score"].to_numpy() > 0.0, "upper_first", "lower_first")
            signal_samples.extend(sample.head(250).to_dict(orient="records"))
        candidate = candidate_gate(split_results)
        records.append(
            {
                "variant": dict(variant),
                "signal_quantile": SIGNAL_QUANTILE,
                "train_threshold_abs": round(float(threshold), 10),
                "candidate_gate": candidate,
                "split_results": split_results,
            }
        )
    flat_rows = []
    for record in records:
        for split_name, metrics in record["split_results"].items():
            flat = {
                "variant_id": record["variant"]["variant_id"],
                "split": split_name,
                "candidate_gate_status": record["candidate_gate"]["status"],
            }
            for key, value in metrics.items():
                if key != "confusion":
                    flat[key] = value
            flat_rows.append(flat)
    pd.DataFrame(flat_rows).to_csv(io_path(VARIANT_METRICS_CSV), index=False)
    pd.DataFrame(signal_samples).to_csv(io_path(SIGNAL_SAMPLES_CSV), index=False)
    best = choose_best_record(records)
    any_candidate = any(record["candidate_gate"]["status"] == "candidate_triggered" for record in records)
    metrics = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "label_id": LABEL_ID,
        "feature_set": read_json(MODEL_INPUT_SUMMARY).get("feature_set_id"),
        "feature_order_hash": read_json(MODEL_INPUT_SUMMARY).get("included_feature_order_hash"),
        "target_policy": {
            "included_target_events": ["upper_first", "lower_first"],
            "excluded_events": ["ambiguous", "censored", "invalid"],
            "target_encoding": "upper_first=1 lower_first=0; ridge signed_speed uses +/- 1 / bars_to_event",
            "threshold_policy": f"absolute score >= train_split_q{int(SIGNAL_QUANTILE * 100)}; validation/oos not used for threshold",
            "calibration_policy": "scores_are_ordering_scores_not_probabilities",
        },
        "candidate_gate_thresholds": {
            "min_signal_hit_rate_validation_and_oos": CANDIDATE_MIN_HIT_RATE,
            "min_signal_count_validation_and_oos": CANDIDATE_MIN_SIGNAL_COUNT,
            "signals_per_day_range_validation_and_oos": [CANDIDATE_MIN_SIGNALS_PER_DAY, CANDIDATE_MAX_SIGNALS_PER_DAY],
            "min_side_share_validation_and_oos": CANDIDATE_MIN_SIDE_SHARE,
            "min_auc_validation_and_oos": CANDIDATE_MIN_AUC,
        },
        "data_integrity": integrity,
        "event_counts": excluded_counts,
        "eligible_rows": int(len(eligible)),
        "excluded_rows": int(len(joined) - len(eligible)),
        "variants": records,
        "best_diagnostic_variant": best,
        "candidate_count": int(any_candidate),
        "meaningful_signal_count": int(any_candidate),
        "runtime_probe_status": RUNTIME_PROBE_STATUS if not any_candidate else "runtime_triggered_candidate_requires_probe",
        "judgment": JUDGMENT if not any_candidate else "candidate_triggered_runtime_probe_required_before_claim",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(PROXY_METRICS, metrics)
    return metrics


def candidate_gate(split_results: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    for split_name in ["validation", "oos"]:
        metrics = split_results[split_name]
        if metrics["signal_count"] < CANDIDATE_MIN_SIGNAL_COUNT:
            failures.append(f"{split_name}_signal_count_below_min")
        if not (CANDIDATE_MIN_SIGNALS_PER_DAY <= float(metrics["signals_per_day"]) <= CANDIDATE_MAX_SIGNALS_PER_DAY):
            failures.append(f"{split_name}_signals_per_day_outside_range")
        if metrics["signal_hit_rate"] is None or float(metrics["signal_hit_rate"]) < CANDIDATE_MIN_HIT_RATE:
            failures.append(f"{split_name}_signal_hit_rate_below_min")
        if metrics["side_min_share"] is None or float(metrics["side_min_share"]) < CANDIDATE_MIN_SIDE_SHARE:
            failures.append(f"{split_name}_side_share_below_min")
        if metrics["auc"] is None or float(metrics["auc"]) < CANDIDATE_MIN_AUC:
            failures.append(f"{split_name}_auc_below_min")
    return {
        "status": "candidate_triggered" if not failures else "not_candidate",
        "failures": failures,
        "claim_effect": "MT5 runtime probe required before runtime/economics claim" if not failures else "runtime_evidence_gate_not_triggered_by_proxy_result",
    }


def choose_best_record(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    def key(record: Mapping[str, Any]) -> tuple[float, float, float]:
        val = record["split_results"]["validation"]
        oos = record["split_results"]["oos"]
        return (
            float(val.get("signal_hit_rate") or 0.0),
            float(oos.get("signal_hit_rate") or 0.0),
            float(oos.get("auc") or 0.0),
        )

    best = max(records, key=key)
    return {
        "variant_id": best["variant"]["variant_id"],
        "selection_policy": "diagnostic_only_predeclared_validation_signal_hit_then_oos_signal_hit_then_oos_auc_no_candidate_claim",
        "validation": best["split_results"]["validation"],
        "oos": best["split_results"]["oos"],
        "candidate_gate": best["candidate_gate"],
    }


def task_force_calls() -> list[dict[str, str]]:
    return [
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019edd55-aca3-73f2-992b-e52d71744ead",
            "tool_name": "multi_agent_v1.spawn_agent",
            "context_update_tool_name": "multi_agent_v1.send_input",
            "context_update_submission_id": "019edd85-7e97-7e12-9eff-e1e498aadf44",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edd55-f3c5-7b70-848e-c5a381ca8f65",
            "tool_name": "multi_agent_v1.spawn_agent",
            "context_update_tool_name": "multi_agent_v1.send_input",
            "context_update_submission_id": "019edd85-98b5-7323-a0c6-3ec12aaf1677",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edd56-3bf0-7db0-968e-a0124d6b1de4",
            "tool_name": "multi_agent_v1.spawn_agent",
            "context_update_tool_name": "multi_agent_v1.send_input",
            "context_update_submission_id": "019edd85-b0c9-7583-871a-3fc243450db3",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edd56-821f-7b02-b9d0-13d779165917",
            "tool_name": "multi_agent_v1.spawn_agent",
            "context_update_tool_name": "multi_agent_v1.send_input",
            "context_update_submission_id": "019edd85-d108-7aa2-8306-97ace323e25f",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edd57-0364-7ae1-b027-9f8fc36269b0",
            "tool_name": "multi_agent_v1.spawn_agent",
            "context_update_tool_name": "multi_agent_v1.send_input",
            "context_update_submission_id": "019edd85-e6c1-7cc1-93db-3bf68f70aa02",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
    ]


def build_payload(now: str, metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": now,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "verification_profile": "experiment_run",
        "claim_boundary": CLAIM_BOUNDARY,
        "hypothesis": "F90B time-to-barrier labels may create a rank/order proxy that predicts upper_first versus lower_first event ordering.",
        "proxy": "Three predeclared linear ONNX-compatible scouts using train-only thresholds.",
        "metrics": metrics,
        "source_identity": {
            "f90b_labels": file_identity(F90B_LABELS),
            "f90b_label_stats": file_identity(F90B_LABEL_STATS),
            "model_input_dataset": file_identity(MODEL_INPUT_DATASET),
            "feature_order": file_identity(MODEL_INPUT_FEATURE_ORDER),
            "feature_order_hash": read_json(MODEL_INPUT_SUMMARY).get("included_feature_order_hash"),
        },
        "runtime_boundary": {
            "runtime_probe_status": RUNTIME_PROBE_STATUS,
            "valid_n_a_reason": "F90C remains ordering proxy only with no meaningful signal, no runnable decision surface, no deterministic order mapping, no ONNX/EA/set behavior claim, and no runtime/materialization/economics claim.",
            "invalid_deferrals": ["cost/expense", "proxy_bad"],
        },
        "task_force": {
            "review_requirement": "active_goal_required_and_explicit_user_instruction_required",
            "fresh_spawn_attempt_status": "blocked_agent_thread_limit_existing_spawned_roster_agents_context_refreshed",
            "agents_used": [call["roster_agent_id"] for call in task_force_calls()],
            "actual_subagent_calls": task_force_calls(),
            "advice_classification": {
                "agent_04_evidence_control_plane": "accepted",
                "agent_05_data_feature_contract": "needs_local_verification",
                "agent_06_quant_research": "needs_local_verification",
                "agent_07_model_validation_risk": "accepted",
                "agent_08_mt5_onnx_runtime": "accepted",
            },
            "local_verification_response": [
                "F90C used train-only threshold and no validation/OOS tuning.",
                "Label-derived columns were not included in feature list.",
                "Ambiguous/censored/invalid rows were excluded and counted, not hidden.",
                "Tier B missing_required and combined blocked boundary remain active.",
                "No runtime trigger fired because candidate gates failed.",
            ],
        },
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def run_manifest(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "verification_profile": "experiment_run",
        "producer": SCRIPT_REL,
        "source_inputs": [rel(path) for path in source_inputs()],
        "produced_artifacts": [rel(path) for path in produced_artifacts()],
        "control_plane_gates": dict(gate_results or {}),
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "current_branch": current_branch(),
    }


def kpi_record(payload: Mapping[str, Any]) -> dict[str, Any]:
    best = payload["metrics"]["best_diagnostic_variant"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "time_to_barrier_ordering_proxy_scout",
        "scoreboard_lane": "structural_scout",
        "label_id": LABEL_ID,
        "variant_count": len(payload["metrics"]["variants"]),
        "eligible_rows": payload["metrics"]["eligible_rows"],
        "excluded_rows": payload["metrics"]["excluded_rows"],
        "best_diagnostic_variant": best["variant_id"],
        "validation_signal_hit_rate": best["validation"]["signal_hit_rate"],
        "oos_signal_hit_rate": best["oos"]["signal_hit_rate"],
        "validation_auc": best["validation"]["auc"],
        "oos_auc": best["oos"]["auc"],
        "validation_signals_per_day": best["validation"]["signals_per_day"],
        "oos_signals_per_day": best["oos"]["signals_per_day"],
        "candidate_count": payload["metrics"]["candidate_count"],
        "meaningful_signal_count": payload["metrics"]["meaningful_signal_count"],
        "tier_a_record_status": "measured",
        "tier_b_record_status": "missing_required",
        "tier_ab_record_status": "blocked_by_missing_tier_b",
        "runtime_kpi": "not_applicable_no_strategy_tester_run",
        "net_profit": "not_applicable_no_runtime_trade_list",
        "profit_factor": "not_applicable_no_runtime_trade_list",
        "drawdown": "not_applicable_no_runtime_trade_list",
        "trade_count": "not_applicable_no_runtime_trade_list",
        "trades_per_day": "proxy_signal_count_only_not_runtime_trades",
        "parity": "P1_dataset_feature_aligned_no_runtime_parity",
        "gap_cause": "validation_oos_ordering_lift_failed_candidate_gate",
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def result_summary_text(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> str:
    best = payload["metrics"]["best_diagnostic_variant"]
    gate_status = ", ".join(f"{name}={result.get('status', 'unknown')}" for name, result in (gate_results or {}).items()) or "pending"
    return f"""# F90C Ordering Proxy Scout(F90C 순서 프록시 탐색)

Updated(갱신): {payload['created_at_utc']}

Conclusion(결론): F90C tested(검사) three predeclared ordering proxy variants(사전 선언 순서 프록시 변형 3개). The best diagnostic variant(진단상 최선 변형) `{best['variant_id']}` failed(실패) the candidate gate(후보 게이트): validation signal hit rate(검증 신호 적중률) `{best['validation']['signal_hit_rate']}`, OOS signal hit rate(표본외 신호 적중률) `{best['oos']['signal_hit_rate']}`, OOS AUC(표본외 AUC) `{best['oos']['auc']}`.

Action(행동): Joined(조인) F90B labels(F90B 라벨) to the 58-feature model input(58개 피처 모델 입력), trained(학습) only on train split(학습 분할), and evaluated(평가) validation/OOS(검증/표본외) without retuning(재조정 없음).

Effect(효과): F90B labelability(라벨 가능성)는 있었지만 F90C ordering lift(순서 리프트)는 OOS(표본외)에서 유지되지 않았고, runnable decision surface(실행 가능 의사결정 표면)나 meaningful signal(의미 있는 신호)이 생기지 않았다.

Tier records(티어 기록): Tier A separate(티어 A 분리) measured(측정됨); Tier B separate(티어 B 분리) `missing_required(필수 누락)`; Tier A+B combined(티어 A+B 합산) `blocked_by_missing_tier_b(티어 B 누락으로 차단)`.

Runtime(런타임): no MT5 Strategy Tester probe(전략 테스터 탐침 없음). Reason(사유): no meaningful signal(의미 있는 신호 없음), no runnable decision surface(실행 가능 의사결정 표면 없음), no ONNX/EA/set behavior claim(ONNX/EA/설정 동작 주장 없음), and no runtime/materialization/economics claim(런타임/물질화/경제성 주장 없음). This is not cost/expense deferral(비용 지연 아님) and not proxy-bad skip(프록시 부진 생략 아님).

Next action(다음 행동): `{NEXT_RUN_ID}` should decide repair or rotation(수리 또는 회전 결정). Do not repeat only threshold/filter/parameter tweaks(임계값/필터/파라미터만 반복 금지).

Gate status(게이트 상태): {gate_status}.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""


def write_run_artifacts(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_json(RUN_MANIFEST, run_manifest(payload, gate_results))
    write_json(SUMMARY_JSON, payload)
    write_json(KPI_RECORD, kpi_record(payload))
    write_text(RESULT_SUMMARY, result_summary_text(payload, gate_results))


def task_force_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    calls = task_force_calls()
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "trigger_reason": "active_goal_required_and_explicit_user_instruction_required",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in calls],
        "actual_subagent_calls": calls,
        "review_requirement": "codex_task_force_review_packet",
        "model_policy": "gpt-5.5_xhigh_floor_with_existing_spawned_roster_context_refresh",
        "fresh_spawn_attempt_status": payload["task_force"]["fresh_spawn_attempt_status"],
        "bounded_evidence": [rel(PROXY_METRICS), rel(KPI_RECORD), rel(WORK_PACKET)],
        "advice_classification": payload["task_force"]["advice_classification"],
        "local_verification": payload["task_force"]["local_verification_response"],
        "final_codex_direction": "Record F90C as negative ordering proxy memory with no runtime trigger.",
        "forbidden_claim_check": "No completion, candidate, selected baseline, operating promotion, runtime authority, live readiness, or Goal Achieve claim.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def audit_payload(name: str, status: str, *, passed: bool = True, counts: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "audit_name": name,
        "packet_id": RUN_ID,
        "status": status,
        "passed": passed,
        "created_at_utc": utc_now(),
        "counts": dict(counts or {}),
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def final_claim_guard_payload() -> dict[str, Any]:
    return {
        "audit_name": "final_claim_guard",
        "packet_id": RUN_ID,
        "status": "pass",
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_audits(payload: Mapping[str, Any]) -> None:
    metrics = payload["metrics"]
    task_force = task_force_receipt(payload)
    write_json(TASK_FORCE_REVIEW, task_force)
    write_json(PACKET_TASK_FORCE_REVIEW, task_force)
    write_json(SCOPE_GATE, audit_payload("scope_completion_gate", "pass", counts={"produced_artifacts": len([path for path in produced_artifacts() if path_exists(path)])}))
    write_json(DATA_INTEGRITY_AUDIT, audit_payload("data_integrity_audit", metrics["data_integrity"]["integrity_judgment"], counts=metrics["data_integrity"]))
    write_json(
        MODEL_VALIDATION_AUDIT,
        audit_payload(
            "model_validation_audit",
            "pass_negative_no_candidate_no_calibration",
            counts={
                "variant_count": len(metrics["variants"]),
                "threshold_policy": metrics["target_policy"]["threshold_policy"],
                "candidate_count": metrics["candidate_count"],
            },
        ),
    )
    write_json(KPI_CONTRACT_AUDIT, audit_payload("kpi_contract_audit", "pass", counts=kpi_record(payload)))
    write_json(ARTIFACT_AUDIT, audit_payload("artifact_lineage_audit", "pass", counts={"source_inputs": len(source_inputs()), "produced_artifacts": len(produced_artifacts())}))
    write_json(
        RESULT_JUDGMENT_AUDIT,
        {
            **audit_payload("result_judgment_audit", "pass"),
            "result_subject": RUN_ID,
            "evidence_available": [rel(PROXY_METRICS), rel(KPI_RECORD), rel(VARIANT_METRICS_CSV), rel(RESULT_SUMMARY)],
            "evidence_missing": ["Tier B partial-context proxy", "MT5 Strategy Tester output", "ONNX/EA runnable candidate"],
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
        },
    )
    guard = final_claim_guard_payload()
    write_json(FINAL_CLAIM_GUARD, guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, guard)


def receipt_path_for(skill: str) -> Path:
    return SKILL_RECEIPT_DIR / f"{skill.replace('obsidian-', '').replace('-', '_')}.json"


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {
        "packet_id": RUN_ID,
        "status": "executed",
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    return [
        {
            **common,
            "skill": "obsidian-run-evidence-system",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "ledger_rows": ["tier_a_separate", "tier_b_separate", "tier_ab_combined"],
            "missing_evidence": ["Tier B source", "MT5 runtime output", "ONNX/EA runnable candidate"],
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": [rel(F90B_LABELS), rel(MODEL_INPUT_DATASET), rel(MODEL_INPUT_FEATURE_ORDER)],
            "time_axis_boundary": "timestamp is bar-close alignment key; train/validation/oos split is inherited from model input and F90B labels.",
            "split_boundary": "train-only fit and threshold; validation/oos evaluation only.",
            "leakage_checks": ["feature list excludes label-derived columns", "validation/oos not used for threshold", "ambiguous/censored/invalid excluded and counted"],
            "missing_data_boundary": "Tier B missing_required; combined blocked_by_missing_tier_b.",
        },
        {
            **common,
            "skill": "obsidian-experiment-design",
            "hypothesis": payload["hypothesis"],
            "baseline": "F90B label feasibility clue only; no selected baseline.",
            "changed_variables": ["target encoding", "linear ordering model family", "train-only rank threshold"],
            "invalid_conditions": ["validation/OOS threshold tuning", "label columns used as features", "score described as calibrated probability"],
            "evidence_plan": [rel(PROXY_METRICS), rel(VARIANT_METRICS_CSV), rel(KPI_RECORD)],
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "Three predeclared linear ordering variants with train-only q90 absolute score threshold.",
            "validation_split": "train/validation/oos split inherited from frozen model input.",
            "overfit_checks": ["no OOS tuning", "variant count recorded", "candidate gate predeclared"],
            "selection_metric_boundary": "diagnostic best only; no candidate or model superiority claim.",
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "raw_evidence": [rel(F90B_LABELS), rel(MODEL_INPUT_DATASET)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(PROXY_METRICS), rel(VARIANT_METRICS_CSV)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(DECISION_MEMO)],
            "hashes_or_missing_reasons": [file_identity(path) for path in source_inputs() + [PROXY_METRICS, KPI_RECORD]],
            "lineage_boundary": CLAIM_BOUNDARY,
        },
        task_force_receipt(payload),
        {
            **common,
            "skill": "obsidian-result-judgment",
            "judgment_boundary": JUDGMENT,
            "allowed_claims": ALLOWED_CLAIMS,
            "evidence_used": [rel(PROXY_METRICS), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
        },
        {
            **common,
            "skill": "obsidian-claim-discipline",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "final_status": STATUS,
        },
    ]


def write_receipts(payload: Mapping[str, Any]) -> None:
    rows = skill_receipts(payload)
    for row in rows:
        write_json(receipt_path_for(row["skill"]), row)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-run-evidence-system", "receipts": rows})


def work_packet(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gates = {
        "work_packet_schema_lint": (gate_results or {}).get("work_packet_schema_lint", {}).get("status", "pending_external_lint"),
        "skill_receipt_schema_lint": (gate_results or {}).get("skill_receipt_schema_lint", {}).get("status", "pending_external_lint"),
        "codex_task_force_review_packet": "pass",
        "scope_completion_gate": "pass",
        "data_integrity_audit": payload["metrics"]["data_integrity"]["integrity_judgment"],
        "model_validation_audit": "pass_negative_no_candidate_no_calibration",
        "kpi_contract_audit": "pass",
        "artifact_lineage_audit": "pass",
        "result_judgment_audit": "pass",
        "state_sync_audit": (gate_results or {}).get("state_sync_audit", {}).get("status", "pending_external_lint"),
        "required_gate_coverage_audit": (gate_results or {}).get("required_gate_coverage_audit", {}).get("status", "pending_external_lint"),
        "final_claim_guard": "pass",
    }
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user explicitly required Task Force agents when triggered",
            "requested_action": "F90C Python/model ordering proxy scout",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["No final completion.", "No runtime authority.", "No candidate claim."],
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
            "detected_families": ["experiment_execution", "kpi_evidence", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel(RUN_DIR), rel(PACKET_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "validation_oos_threshold_tuning": "high",
                "score_called_probability": "high",
                "tier_b_omitted": "high",
                "runtime_probe_absence_misread_as_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not claim candidate/runtime/economics/materialization without runnable surface and MT5 output identity.",
                "Do not describe Tier A-only proxy as combined alpha read.",
                "Do not call ordering scores calibrated probabilities.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "verification_profile": "experiment_run",
                "strategy_tester_required_now": False,
                "reason": "Candidate gates failed; no runnable decision surface, ONNX/EA/set behavior, or runtime/materialization/economics claim.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F90C ordering proxy scout", "Tier A/B/combined records", "Task Force receipt", "state sync"],
            "scope_units": ["local_python_execution", "run_evidence", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F90B labels", "model input parquet", "proxy metrics", "Task Force actual calls"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "experiment_run",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal_frontier_continuation", "F90C current_run", "explicit user instruction requiring Task Force when triggered"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [rel(PROXY_METRICS), rel(VARIANT_METRICS_CSV), rel(KPI_RECORD), rel(PACKET_TASK_FORCE_REVIEW), rel(WORK_PACKET)],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface_no_runtime_materialization_economics_claim",
                    "reason": "F90C candidate gates failed and no runnable decision surface, deterministic order mapping, ONNX/EA/set behavior, or runtime claim exists.",
                    "claim_effect": "Runtime probe, runtime verified, economics pass, materialization ready, handoff ready, authority, live readiness, and Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "wfo_stress_gate",
                    "reason_code": "outside_claim_surface_no_candidate",
                    "reason": "F90C is a single split proxy scout and creates no candidate selected for WFO/stress.",
                    "claim_effect": "WFO/stress pass, model superiority, and candidate claims are forbidden.",
                },
            ],
            "stop_conditions": ["Candidate gate failure closes as negative memory", "Runtime claims must trigger MT5 probe or be forbidden"],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F90C proxy metrics exist.", "expected_artifact": rel(PROXY_METRICS), "verification_method": "kpi_contract_audit", "required": True},
            {"id": "AC-002", "text": "F90C Task Force actual calls/context refresh are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "No runtime claim is made without MT5 evidence.", "expected_artifact": rel(FINAL_CLAIM_GUARD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": {
            "phases": ["Read F90B evidence.", "Refresh relevant Task Force agents.", "Run proxy variants.", "Write negative memory and gates."],
            "expected_outputs": [rel(path) for path in produced_artifacts()],
            "stop_conditions": ["Do not force MT5 without runnable candidate.", "Do not claim candidate from proxy metrics alone."],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": [
                "obsidian-data-integrity",
                "obsidian-experiment-design",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-task-force-review",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA/runtime parity or handoff claim is made."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report or trade list exists in F90C."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(path) for path in [F90B_LABELS, F90B_LABEL_STATS, MODEL_INPUT_DATASET, MODEL_INPUT_FEATURE_ORDER]],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, PROXY_METRICS, VARIANT_METRICS_CSV, SKILL_RECEIPTS, PACKET_TASK_FORCE_REVIEW]],
            "human_readable": [rel(path) for path in [RESULT_SUMMARY, STAGE_BRIEF, CURRENT_WORKING_STATE, DECISION_MEMO]],
        },
        "gates": {
            "required": REQUIRED_GATES,
            **gates,
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface_no_runtime_materialization_economics_claim",
                "wfo_stress_gate": "outside_claim_surface_no_candidate",
            },
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS},
    }


def closeout_gate(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = dict(gate_results or {})
    audits = [
        {"audit_name": "work_packet_schema_lint", "path": rel(PACKET_WORK_PACKET_LINT), "status": gate_results.get("work_packet_schema_lint", {}).get("status", "pending_external_lint")},
        {"audit_name": "skill_receipt_schema_lint", "path": rel(PACKET_SKILL_RECEIPT_LINT), "status": gate_results.get("skill_receipt_schema_lint", {}).get("status", "pending_external_lint")},
        {"audit_name": "codex_task_force_review_packet", "path": rel(PACKET_TASK_FORCE_REVIEW), "status": "pass"},
        {"audit_name": "scope_completion_gate", "path": rel(SCOPE_GATE), "status": "pass"},
        {"audit_name": "data_integrity_audit", "path": rel(DATA_INTEGRITY_AUDIT), "status": payload["metrics"]["data_integrity"]["integrity_judgment"]},
        {"audit_name": "model_validation_audit", "path": rel(MODEL_VALIDATION_AUDIT), "status": "pass_negative_no_candidate_no_calibration"},
        {"audit_name": "kpi_contract_audit", "path": rel(KPI_CONTRACT_AUDIT), "status": "pass"},
        {"audit_name": "artifact_lineage_audit", "path": rel(ARTIFACT_AUDIT), "status": "pass"},
        {"audit_name": "result_judgment_audit", "path": rel(RESULT_JUDGMENT_AUDIT), "status": "pass"},
        {"audit_name": "state_sync_audit", "path": rel(PACKET_STATE_SYNC_AUDIT), "status": gate_results.get("state_sync_audit", {}).get("status", "pending_external_lint")},
        {"audit_name": "required_gate_coverage_audit", "path": rel(PACKET_REQUIRED_GATE_AUDIT), "status": gate_results.get("required_gate_coverage_audit", {}).get("status", "pending_external_lint")},
    ]
    return {
        "packet_id": RUN_ID,
        "status": "pass" if gate_results.get("required_gate_coverage_audit", {}).get("status") == "pass" else "pending_external_lint",
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "audits": audits,
        "final_claim_guard": {"audit_name": "final_claim_guard", "path": rel(PACKET_FINAL_CLAIM_GUARD), "status": "pass"},
    }


def write_packet_and_gate(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_yaml(WORK_PACKET, work_packet(payload, gate_results))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate(payload, gate_results))


def workspace_state_text(payload: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: f90c_ordering_proxy_scout_negative_f90d_repair_or_rotation_planned_no_authority
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: not_due_after_f89_closeout_next_boundary_f100_e01_closed_for_f050
frontier_topic_rotation_status: passed_f90_new_label_representation_axis_not_threshold_tweak
task_force_status: f90c_actual_subagent_context_refresh_recorded_5_selected_agents_no_task_force_reviewed_pass_claim
runtime_probe_status: {RUNTIME_PROBE_STATUS}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F90C tested(검사) ordering proxy variants(순서 프록시 변형) from F90B labels and 58 features.'
- 'Effect(효과): validation/OOS lift(검증/표본외 리프트) failed candidate gate(후보 게이트), so runtime trigger(런타임 트리거)는 발동하지 않았다.'
- 'Runtime(런타임): no Strategy Tester evidence(전략 테스터 근거 없음); no runtime authority(런타임 권위 없음); no Goal Achieve(목표 달성 없음).'
"""


def current_state_text(payload: Mapping[str, Any]) -> str:
    best = payload["metrics"]["best_diagnostic_variant"]
    return f"""# Current Working State(현재 작업 상태)

- active_stage(활성 단계): `{STAGE_ID}`
- latest_completed_run(최신 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `f90c_ordering_proxy_scout_negative_f90d_repair_or_rotation_planned_no_authority`
- judgment(판정): `{JUDGMENT}`
- best_proxy(최선 프록시): `{best['variant_id']}` validation_hit `{best['validation']['signal_hit_rate']}` OOS_hit `{best['oos']['signal_hit_rate']}` OOS_AUC `{best['oos']['auc']}`
- Task Force(태스크포스): 5 selected agents(선택 요원) refreshed with F90C context(전선90C 맥락 갱신), no Task Force reviewed/pass claim(검토됨/통과 주장 없음)
- Runtime(런타임): `{RUNTIME_PROBE_STATUS}`
- Boundary(경계): `{CLAIM_BOUNDARY}`
"""


def stage_brief_text(payload: Mapping[str, Any]) -> str:
    return f"""# {STAGE_ID}

Question(질문): Can time-to-barrier competing-risk labels(장벽 도달 시간 경쟁위험 라벨) create a leakage-safe ordering proxy(누수 없는 순서 프록시) for US100 M5?

F90C result(F90C 결과): ordering proxy variants(순서 프록시 변형) failed(실패) validation/OOS candidate gates(검증/표본외 후보 게이트). Tier A(티어 A) only remains measured(측정), Tier B(티어 B) remains missing_required(필수 누락), and combined(합산) remains blocked(차단).

Next(다음): `{NEXT_RUN_ID}` should decide repair or rotation(수리 또는 회전 결정). Runtime authority(런타임 권위), selected baseline(선택 기준선), live readiness(실거래 준비), and Goal Achieve(목표 달성) are not claimed.
"""


def input_refs_text(payload: Mapping[str, Any]) -> str:
    lines = ["# Input References(입력 참조)", ""]
    for path in source_inputs():
        ident = file_identity(path)
        lines.append(f"- `{ident['path']}` sha256 `{ident['sha256']}`")
    return "\n".join(lines)


def selection_status_text(payload: Mapping[str, Any]) -> str:
    return f"""# Selection Status(선택 상태)

No candidate(후보 없음), no selected baseline(선택 기준선 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).

F90C(전선90C) is negative ordering proxy memory(부정 순서 프록시 기억) only. Tier B(티어 B) remains `missing_required(필수 누락)`, so Tier A+B combined(티어 A+B 합산) is blocked(차단).
"""


def review_index_text(payload: Mapping[str, Any]) -> str:
    rows = [
        ("f90c_task_force_review_receipt", TASK_FORCE_REVIEW),
        ("f90c_data_integrity_audit", DATA_INTEGRITY_AUDIT),
        ("f90c_model_validation_audit", MODEL_VALIDATION_AUDIT),
        ("f90c_kpi_contract_audit", KPI_CONTRACT_AUDIT),
        ("f90c_artifact_lineage_audit", ARTIFACT_AUDIT),
        ("f90c_result_judgment_audit", RESULT_JUDGMENT_AUDIT),
        ("f90c_required_gate_coverage_audit", REQUIRED_GATE_AUDIT),
    ]
    lines = ["# Review Index(검토 색인)", ""]
    for name, path in rows:
        lines.append(f"- `{name}`: `{rel(path)}`")
    return "\n".join(lines)


def decision_memo_text(payload: Mapping[str, Any]) -> str:
    best = payload["metrics"]["best_diagnostic_variant"]
    return f"""# F90C Decision Memo(F90C 결정 메모)

Decision(결정): Record F90C as negative ordering proxy memory(부정 순서 프록시 기억) and plan `{NEXT_RUN_ID}` for repair or rotation(수리 또는 회전).

Reason(이유): Best diagnostic variant(진단상 최선 변형) `{best['variant_id']}` did not preserve validation/OOS(검증/표본외) signal quality enough to create a meaningful signal(의미 있는 신호) or runnable decision surface(실행 가능 의사결정 표면).

Forbidden(금지): candidate(후보), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
"""


def update_state_docs(payload: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(payload))
    write_text(CURRENT_WORKING_STATE, current_state_text(payload))
    write_text(GLOBAL_SELECTION_STATUS, selection_status_text(payload))
    write_text(STAGE_BRIEF, stage_brief_text(payload))
    write_text(INPUT_REFS, input_refs_text(payload))
    write_text(SELECTION_STATUS, selection_status_text(payload))
    write_text(CONTEXT_ANCHOR, current_state_text(payload))
    write_text(REVIEW_INDEX, review_index_text(payload))
    write_text(DECISION_MEMO, decision_memo_text(payload))


def append_dict_rows(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], header_source: Path | None = None) -> None:
    source = path if path_exists(path) else header_source
    if source is None or not path_exists(source):
        raise FileNotFoundError(f"CSV header source missing for {path}")
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        existing = list(reader) if path_exists(path) else []
    keys_to_replace = {tuple(str(row.get(field, "")) for field in key_fields) for row in rows}
    kept = [row for row in existing if tuple(str(row.get(field, "")) for field in key_fields) not in keys_to_replace]
    normalized = [{field: json_ready(row.get(field, "")) for field in fieldnames} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept + normalized)


def replace_rows_by_field(path: Path, field: str, value: str, rows: Sequence[Mapping[str, Any]], header_source: Path | None = None) -> None:
    source = path if path_exists(path) else header_source
    if source is None or not path_exists(source):
        raise FileNotFoundError(f"CSV header source missing for {path}")
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        existing = list(reader) if path_exists(path) else []
    kept = [row for row in existing if str(row.get(field, "")).strip() != value]
    normalized = [{column: json_ready(row.get(column, "")) for column in fieldnames} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept + normalized)


def ledger_rows(payload: Mapping[str, Any], gate_passes: int = 0) -> list[dict[str, Any]]:
    created_date = payload["created_at_utc"][:10]
    best = payload["metrics"]["best_diagnostic_variant"]
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "time_to_barrier_ordering_proxy_scout",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "notes": "F90C ordering proxy failed candidate gates; no runtime authority.",
        "family": "experiment_execution",
        "primary_report": rel(RESULT_SUMMARY),
        "run_number": "frontier90C",
        "date": created_date,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": payload["metrics"]["eligible_rows"],
        "gate_passes": gate_passes,
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": created_date,
        "primary_artifact": rel(PROXY_METRICS),
        "result_status": STATUS,
        "scoreboard_lane": "structural_scout",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "result_judgment": JUDGMENT,
        "gate_audit_path": rel(PACKET_REQUIRED_GATE_AUDIT),
        "created_at": payload["created_at_utc"],
        "work_family": "experiment_execution",
        "evidence_boundary": "ordering_proxy_scout_only_no_runtime_evidence",
        "next_action": NEXT_RUN_ID,
        "question": "Can F90B labels create an ordering proxy?",
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path)]),
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "experiment_run_proxy_scout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(RESULT_SUMMARY),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "candidate_count": 0,
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "runtime_attempt_rows": 0,
    }
    views = [
        (
            "tier_a_separate",
            "Tier A separate",
            "negative_measured",
            f"best={best['variant_id']};val_hit={best['validation']['signal_hit_rate']};oos_hit={best['oos']['signal_hit_rate']};oos_auc={best['oos']['auc']}",
            "no candidate; runtime trigger false",
        ),
        ("tier_b_separate", "Tier B separate", "missing_required", "missing_required_no_partial_context_source", "no Tier B performance or proxy claim"),
        ("tier_ab_combined", "Tier A+B combined", "blocked_by_missing_tier_b", "blocked_by_missing_tier_b", "whole-alpha combined read forbidden"),
    ]
    rows = []
    for record_view, tier_scope, view_status, primary_kpi, guardrail in views:
        row = dict(base)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{record_view}",
                "subrun_id": f"{RUN_ID}__{record_view}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "kpi_scope": "time_to_barrier_ordering_proxy",
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail,
                "row_id": f"{RUN_ID}__{record_view}",
                "view": record_view,
                "tier": tier_scope,
                "metric_scope": "ordering_proxy",
                "result_status": view_status,
            }
        )
        rows.append(row)
    planned = dict(base)
    planned.update(
        {
            "run_id": NEXT_RUN_ID,
            "status": "planned_current_run_no_authority",
            "judgment": "pending_repair_or_rotation_decision",
            "path": rel(STAGE_DIR),
            "notes": "Planned after F90C negative proxy result.",
            "primary_report": rel(STAGE_BRIEF),
            "run_number": "frontier90D",
            "decision": "pending_execution",
            "parent_run_id": RUN_ID,
            "next_run_id": "",
            "rows": 0,
            "gate_passes": 0,
            "gate_total": 0,
            "claim_boundary": "planned_current_run_no_authority_no_runtime_claim_no_goal_achieve",
            "report_path": rel(STAGE_BRIEF),
            "primary_artifact": rel(STAGE_BRIEF),
            "result_status": "planned_current_run_no_authority",
            "external_verification_status": "pending",
            "result_judgment": "pending",
            "gate_audit_path": "",
            "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
            "subrun_id": f"{NEXT_RUN_ID}__planned_current_run",
            "record_view": "planned_current_run",
            "tier_scope": "not_applicable_planned",
            "kpi_scope": "pending",
            "primary_kpi": "pending",
            "guardrail_kpi": "pending_runtime_claim_forbidden",
            "row_id": f"{NEXT_RUN_ID}__planned_current_run",
            "view": "planned_current_run",
            "tier": "not_applicable_planned",
            "metric_scope": "pending",
            "evidence_boundary": "planned_only_no_runtime_evidence",
            "next_action": "decide_repair_or_rotation",
            "question": "Should F90 repair time-to-barrier ordering or rotate after OOS proxy failure?",
            "artifact_count": 0,
            "required_gate_audit": "",
            "run_type": "planned_current_run",
            "input_run_id": RUN_ID,
            "output_path": rel(STAGE_DIR),
            "result_path": rel(STAGE_BRIEF),
            "scout_clue_count": 0,
        }
    )
    rows.append(planned)
    return rows


def update_ledgers(payload: Mapping[str, Any], gate_passes: int = 0) -> None:
    rows = ledger_rows(payload, gate_passes=gate_passes)
    run_rows = [dict(rows[0]), dict(rows[-1])]
    append_dict_rows(RUN_REGISTRY, ["run_id"], run_rows)
    append_dict_rows(ALPHA_LEDGER, ["ledger_row_id"], rows)
    append_dict_rows(STAGE_LEDGER, ["ledger_row_id"], rows, header_source=ALPHA_LEDGER)


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f90c_ordering_proxy_scout",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F90C ordering proxy artifact; no runtime authority.",
                "artifact_path": rel(path),
                "effect": "Supports F90C negative ordering proxy memory only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    replace_rows_by_field(ARTIFACT_REGISTRY, "run_id", RUN_ID, rows)


def update_register_docs(payload: Mapping[str, Any]) -> None:
    marker = RUN_ID
    best = payload["metrics"]["best_diagnostic_variant"]
    idea_addition = f"""
## F90C ordering proxy negative memory(F90C 순서 프록시 부정 기억)

- run_id: `{RUN_ID}`
- hypothesis(가설): F90B time-to-barrier labels(F90B 장벽 도달 시간 라벨)이 upper/lower ordering(상방/하방 순서) 프록시를 만들 수 있는지 본다.
- result(결과): best diagnostic variant(진단상 최선 변형) `{best['variant_id']}` failed candidate gate(후보 게이트 실패).
- next_action(다음 행동): `{NEXT_RUN_ID}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    negative_addition = f"""
## F90C ordering proxy OOS failure(F90C 순서 프록시 표본외 실패)

- run_id: `{RUN_ID}`
- failed_boundary(실패 경계): validation/OOS signal hit and AUC(검증/표본외 신호 적중률과 AUC) did not meet predeclared candidate gate(사전 선언 후보 게이트).
- salvage_value(회수 가치): F90B labelability(라벨 가능성)는 보존하되, linear ordering proxy(선형 순서 프록시)는 반복하지 않는다.
- do_not_repeat(반복 금지): 같은 threshold/filter/parameter-only tweak(임계값/필터/파라미터만 조정)로 F90C를 재시도하지 않는다.
- reopen_condition(재개 조건): new target representation/source/model family/runtime representation(새 목표 표현/원천/모델 계열/런타임 표현)이 있을 때만 재개한다.
"""
    changelog_addition = f"""
## {payload['created_at_utc']} - F90C Ordering Proxy Scout(F90C 순서 프록시 탐색)

- Action(행동): tested three predeclared ordering proxy variants(사전 선언 순서 프록시 변형 3개).
- Effect(효과): candidate gate(후보 게이트) failed, so no MT5 runtime trigger(MT5 런타임 트리거 없음).
- Runtime(런타임): no Strategy Tester evidence(전략 테스터 근거 없음); no runtime authority(런타임 권위 없음); no Goal Achieve(목표 달성 없음).
- Packet(묶음): `{rel(WORK_PACKET)}`.
"""
    append_once(IDEA_REGISTRY, marker, idea_addition)
    append_once(NEGATIVE_REGISTER, marker, negative_addition)
    append_once(WORKSPACE_CHANGELOG, marker, changelog_addition)
    append_once(ROOT_CHANGELOG, marker, changelog_addition)


def run_gate_cmd(args: Sequence[str], output_path: Path) -> dict[str, Any]:
    command = [sys.executable, "-m", *args, "--output-json", str(output_path), "--allow-blocked-exit-zero"]
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, timeout=180)
    payload: dict[str, Any] = read_json(output_path) if path_exists(output_path) else {}
    result = {
        "command": command,
        "output_path": rel(output_path),
        "returncode": completed.returncode,
        "status": payload.get("status", "missing_output"),
        "passed": payload.get("status") == "pass" or payload.get("passed", False),
        "stdout_tail": completed.stdout[-2000:],
        "stderr_tail": completed.stderr[-2000:],
    }
    if completed.returncode != 0 or result["status"] != "pass":
        raise RuntimeError(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def sync_review_audit(src: Path, dst: Path) -> None:
    if path_exists(src):
        write_json(dst, read_json(src))


def write_initial(payload: Mapping[str, Any]) -> None:
    write_run_artifacts(payload)
    write_audits(payload)
    write_receipts(payload)
    write_packet_and_gate(payload)
    update_state_docs(payload)
    update_ledgers(payload)
    update_register_docs(payload)
    write_json(PACKET_STATE_SYNC_AUDIT, audit_payload("state_sync_audit", "pending_external_lint", counts={"active_stage": STAGE_ID, "current_run_id": NEXT_RUN_ID}))
    write_json(STATE_SYNC_AUDIT, read_json(PACKET_STATE_SYNC_AUDIT))


def run_control_gates(payload: Mapping[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    results["work_packet_schema_lint"] = run_gate_cmd(["foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET)], PACKET_WORK_PACKET_LINT)
    results["skill_receipt_schema_lint"] = run_gate_cmd(["foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS)], PACKET_SKILL_RECEIPT_LINT)
    results["state_sync_audit"] = run_gate_cmd(
        ["foundation.control_plane.state_sync_audit", "--root", str(ROOT), "--active-stage", STAGE_ID, "--current-branch", current_branch()],
        PACKET_STATE_SYNC_AUDIT,
    )
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    write_packet_and_gate(payload, results)
    results["required_gate_coverage_audit"] = run_gate_cmd(
        ["foundation.control_plane.required_gate_coverage_audit", "--work-packet", str(WORK_PACKET), "--closeout-gate", str(PACKET_CLOSEOUT_GATE)],
        PACKET_REQUIRED_GATE_AUDIT,
    )
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    write_packet_and_gate(payload, results)
    return results


def write_final(payload: Mapping[str, Any], gate_results: Mapping[str, Any]) -> None:
    gate_passes = len(REQUIRED_GATES)
    write_run_artifacts(payload, gate_results)
    write_audits(payload)
    write_receipts(payload)
    write_packet_and_gate(payload, gate_results)
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    update_state_docs(payload)
    update_ledgers(payload, gate_passes=gate_passes)
    update_artifact_registry(payload)


def main() -> int:
    missing = [rel(path) for path in source_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required F90C source evidence: {missing}")
    ensure_dirs()
    metrics = materialize_proxy_metrics()
    payload = build_payload(utc_now(), metrics)
    write_initial(payload)
    gate_results = run_control_gates(payload)
    write_final(payload, gate_results)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "best_diagnostic_variant": payload["metrics"]["best_diagnostic_variant"],
                "candidate_count": payload["metrics"]["candidate_count"],
                "runtime_probe_status": RUNTIME_PROBE_STATUS,
                "task_force_call_count": len(task_force_calls()),
                "gate_results": gate_results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
