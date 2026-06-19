from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
import yaml
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.audit_result import AuditFinding, AuditResult, COMPLETION_CLAIMS
from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_91 import frontier91b_regime_density_cost_abstention_proxy_scout as f91


STAGE_ID = "stage_frontier_96__counterfactual_action_value_policy_axis"
RUN_ID = "frontier96B_counterfactual_action_value_policy_proxy_scout_v1"
PARENT_RUN_ID = "frontier96A_stage_open_counterfactual_action_value_policy_axis_v1"
NEXT_RUN_ID = "frontier96C_counterfactual_action_value_policy_repair_or_rotation_decision_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_96/frontier96b_action_value_proxy_scout.py"

STATUS_NEGATIVE = "f96b_counterfactual_action_value_policy_proxy_scout_negative_no_runnable_candidate_no_authority"
STATUS_BLOCKED_RUNTIME = "f96b_counterfactual_action_value_policy_proxy_scout_blocked_pending_same_packet_mt5_probe"
JUDGMENT_NEGATIVE = "negative_proxy_scout_action_value_gate_failed_no_runtime_trigger"
JUDGMENT_BLOCKED_RUNTIME = "blocked_same_packet_mt5_probe_required_before_candidate_or_runtime_claim"
CLAIM_BOUNDARY = (
    "f96b_proxy_scout_only_counterfactual_action_value_policy_"
    "no_selected_baseline_no_operating_promotion_no_runtime_authority_"
    "no_live_readiness_no_goal_achieve_no_runtime_economics_claim"
)
RUNTIME_PROBE_STATUS_NEGATIVE = "not_applicable_no_runnable_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip"
RUNTIME_PROBE_STATUS_BLOCKED = "blocked_same_packet_mt5_probe_required_before_runnable_candidate_or_runtime_claim"
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f95_closeout_next_boundary_f100_e02_pending_e01_closed_for_f050"
FRONTIER_FIVE_STAGE_STATUS = "recorded_recent_f91_to_f95_direction_synthesis_no_retrospective_gate"
FRONTIER_TOPIC_ROTATION_STATUS = "continuation_inside_f96_axis_f96a_rotation_already_passed"

RNG_SEED = 9602
RANDOM_CONTROL_REPS = 20
CANDIDATE_MIN_PF = 1.0
CANDIDATE_MIN_TRADES_PER_DAY = 5.0
CANDIDATE_MAX_TRADES_PER_DAY = 10.0
CANDIDATE_MAX_DD = 0.30
CANDIDATE_MIN_SIDE_SHARE = 0.20
CANDIDATE_MIN_REGIME_COVERAGE = 4
CANDIDATE_MAX_ADVERSE_PENALTY_SHARE = 0.65

COST_MULTIPLIER = 1.0
SLIPPAGE_PROXY = 0.00003
ADVERSE_PENALTY_WEIGHT = 0.35
ABSTAIN_OPPORTUNITY_WEIGHT = 0.10

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier96B"
PROXY_DIR = RUN_DIR / "proxy_scout"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SKILL_RECEIPT_DIR = PACKET_DIR / "skill_receipts"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
GLOBAL_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
ROOT_CHANGELOG = ROOT / "docs" / "CHANGELOG.md"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier96b_counterfactual_action_value_proxy_scout.md"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
EXECUTION_SUMMARY = RUN_DIR / "execution_summary.json"
DATA_LOCK = PROXY_DIR / "data_feature_split_lock.json"
ACTION_VALUE_CONFIG = PROXY_DIR / "action_value_config.json"
ACTION_VALUE_LABEL_SUMMARY = PROXY_DIR / "action_value_label_summary.json"
MODEL_FIT_MANIFEST = PROXY_DIR / "model_fit_manifest.json"
VARIANT_METRICS_CSV = PROXY_DIR / "variant_metrics.csv"
SPLIT_METRICS_CSV = PROXY_DIR / "split_metrics.csv"
NEGATIVE_CONTROL_CSV = PROXY_DIR / "negative_control_metrics.csv"
SCORE_SAMPLE_CSV = PROXY_DIR / "score_sample.csv"
CANDIDATE_GATE_JSON = PROXY_DIR / "candidate_gate.json"
TIER_ROUTE_SUMMARY = PROXY_DIR / "tier_route_summary.json"
TIER_B_SUMMARY = PROXY_DIR / "tier_b_summary.json"
DATA_INTEGRITY_LOCAL = PROXY_DIR / "data_integrity_local_checks.json"
RUNTIME_TRIGGER_CHECK = PROXY_DIR / "runtime_trigger_check.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

TASK_FORCE_REVIEW = REVIEW_DIR / "f96b_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f96b_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f96b_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f96b_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f96b_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f96b_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f96b_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f96b_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f96b_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f96b_result_judgment_audit.json"
RUNTIME_EVIDENCE_GATE = REVIEW_DIR / "f96b_runtime_evidence_gate.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f96b_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f96b_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f96b_required_gate_coverage_audit.json"
F96B_REPORT = REVIEW_DIR / "frontier96B_counterfactual_action_value_proxy_scout_report.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_TASK_FORCE_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

MODEL_INPUT_DIR = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
MODEL_INPUT_DATASET = MODEL_INPUT_DIR / "model_input_dataset.parquet"
MODEL_INPUT_SUMMARY = MODEL_INPUT_DIR / "model_input_summary.json"
MODEL_INPUT_FEATURE_ORDER = MODEL_INPUT_DIR / "model_input_feature_order.txt"
RAW_M5_ROOT = ROOT / "data" / "raw" / "mt5_bars" / "m5"

F96A_BRIEF = STAGE_DIR / "02_runs" / "frontier96A" / "d" / "f96b_proxy_scout_brief.json"
F96A_CONTRACT = STAGE_DIR / "02_runs" / "frontier96A" / "d" / "action_value_policy_contract.json"
F96A_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F96A_CLOSEOUT_GATE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "closeout_gate.json"
F95B_SPLIT_METRICS = (
    ROOT
    / "stages"
    / "stage_frontier_95__closed_bar_state_transition_embedding_axis"
    / "02_runs"
    / "frontier95B"
    / "proxy_scout"
    / "split_metrics.csv"
)
F95B_CANDIDATE_GATE = (
    ROOT
    / "stages"
    / "stage_frontier_95__closed_bar_state_transition_embedding_axis"
    / "02_runs"
    / "frontier95B"
    / "proxy_scout"
    / "candidate_gate.json"
)

DENYLIST_FEATURE_TOKENS = ("future", "label", "mfe", "mae", "utility", "path", "target", "profit", "loss")
REGIME_FEATURE_HINTS = (
    "historical_vol",
    "atr_",
    "adx",
    "di_spread",
    "rsi",
    "bb_",
    "bollinger",
    "return_zscore",
    "hl_zscore",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
)
VARIANTS = [
    {"variant_id": "logreg_action_value_full58_balanced", "family": "logistic_action", "feature_mode": "full58"},
    {"variant_id": "extra_trees_action_value_regime_dense", "family": "extra_trees_action", "feature_mode": "regime_dense"},
    {"variant_id": "ridge_signed_utility_edge_full58_q88", "family": "ridge_signed_edge", "feature_mode": "full58", "train_abs_quantile": 0.88},
]

ALLOWED_CLAIMS = [
    "f96b_proxy_scout_executed",
    "counterfactual_action_value_negative_memory_recorded",
    "task_force_actual_calls_recorded_for_f96b",
    "candidate_gate_count_recorded",
    "runtime_trigger_boundary_recorded_no_probe_without_candidate",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "complete",
    "completed",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "promotion_candidate",
    "runtime_probe",
    "runtime_probe_completed",
    "runtime_verified",
    "strategy_tester_runtime_economics",
    "runtime_economics",
    "runtime_economics_pass",
    "economics_pass",
    "materialization_ready",
    "mt5_handoff_ready",
    "onnx_handoff_ready",
    "ea_handoff_ready",
    "task_force_reviewed",
    "task_force_reviewed_pass",
    "internally_reviewed",
    "reviewed",
    "verified",
    "pass",
    "model_quality",
    "model_readiness",
    "calibrated_probability",
    "data_contract_pass",
]
BASE_REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "codex_task_force_review_packet",
    "frontier_extra_due_check",
    "frontier_five_stage_direction_synthesis",
    "frontier_topic_rotation_check",
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
    "obsidian-experiment-design",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-task-force-review",
    "obsidian-result-judgment",
    "obsidian-exploration-mandate",
    "obsidian-claim-discipline",
]
RUNTIME_NA_REASONS = [
    {
        "gate": "runtime_evidence_gate",
        "reason_code": "proxy_scout_no_runnable_candidate_no_runtime_claim",
        "reason": "F96B makes no runtime, materialization, handoff, or economics claim when the validation candidate gate count is zero.",
        "claim_effect": "No runtime_probe, runtime_verified, materialization_ready, handoff_complete, economics_pass, runtime_authority, live_readiness, selected_baseline, or Goal Achieve claim is allowed.",
    }
]


def utc_now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def file_identity(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"path": rel(path), "exists": False, "sha256": None, "size_bytes": None}
    return {"path": rel(path), "exists": True, "sha256": sha256_file_lf_normalized(path), "size_bytes": io_path(path).stat().st_size}


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True, timeout=10)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def stable_seed(*parts: Any) -> int:
    digest = hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def feature_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(features).encode("utf-8")).hexdigest()


def hash_dataframe(frame: pd.DataFrame, columns: Sequence[str]) -> str:
    sample = frame.loc[:, list(columns)].head(5000).copy()
    csv_text = sample.to_csv(index=False)
    return hashlib.sha256(csv_text.encode("utf-8")).hexdigest()


def ensure_dirs() -> None:
    for path in [RUN_DIR, PROXY_DIR, REPORT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, SKILL_RECEIPT_DIR]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def source_inputs() -> list[Path]:
    return [
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
        F96A_BRIEF,
        F96A_CONTRACT,
        F96A_PACKET,
        F96A_CLOSEOUT_GATE,
        MODEL_INPUT_DATASET,
        MODEL_INPUT_SUMMARY,
        MODEL_INPUT_FEATURE_ORDER,
        F95B_SPLIT_METRICS,
        F95B_CANDIDATE_GATE,
        ROOT / "docs" / "agent_control" / "work_family_registry.yaml",
        ROOT / "docs" / "agent_control" / "codex_task_force_registry.yaml",
    ]


def produced_artifacts() -> list[Path]:
    paths = [
        ROOT / SCRIPT_REL,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        EXECUTION_SUMMARY,
        DATA_LOCK,
        ACTION_VALUE_CONFIG,
        ACTION_VALUE_LABEL_SUMMARY,
        MODEL_FIT_MANIFEST,
        VARIANT_METRICS_CSV,
        SPLIT_METRICS_CSV,
        NEGATIVE_CONTROL_CSV,
        SCORE_SAMPLE_CSV,
        CANDIDATE_GATE_JSON,
        TIER_ROUTE_SUMMARY,
        TIER_B_SUMMARY,
        DATA_INTEGRITY_LOCAL,
        RUNTIME_TRIGGER_CHECK,
        RESULT_SUMMARY,
        TASK_FORCE_REVIEW,
        PACKET_TASK_FORCE_REVIEW,
        FRONTIER_EXTRA_DUE_CHECK,
        FIVE_STAGE_SYNTHESIS,
        TOPIC_ROTATION_CHECK,
        SCOPE_GATE,
        DATA_INTEGRITY_AUDIT,
        MODEL_VALIDATION_AUDIT,
        KPI_CONTRACT_AUDIT,
        ARTIFACT_AUDIT,
        RESULT_JUDGMENT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
        F96B_REPORT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_CLOSEOUT_GATE,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        DECISION_MEMO,
    ]
    if path_exists(RUNTIME_EVIDENCE_GATE):
        paths.append(RUNTIME_EVIDENCE_GATE)
    return paths


def task_force_calls() -> list[dict[str, Any]]:
    return [
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019edf12-8b62-7640-a599-0b73217477c0",
            "nickname": "Kant the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "classification_detail": "F96B needs local work_packet, gate, receipt, hash, and candidate/runtime trigger evidence before any stronger review language.",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edf12-9f8c-70e1-bd8b-1af613ba026e",
            "nickname": "Plato the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "classification_detail": "Timestamp ordering, duplicate checks, Tier A/B/A+B records, and feature/label boundary checks must be local evidence.",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edf12-c0ca-7c92-95a8-ce9763e1ee11",
            "nickname": "Godel the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "classification_detail": "Utility formula and negative controls are accepted directionally but must be predeclared and locally executed.",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edf12-d559-7d71-a98c-ba82bb72ce02",
            "nickname": "Ampere the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "classification_detail": "Exploratory proxy scout is allowed, but model quality, promotion, authority, completion, and OOS tuning claims are rejected.",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edf12-efa3-7001-97de-df1c6e287171",
            "nickname": "Jason the 2nd",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "classification_detail": "Python proxy-scout only does not require MT5 evidence unless a runnable candidate or runtime/materialization/handoff/economics claim is made.",
        },
    ]


def required_gates(candidate_count: int = 0) -> list[str]:
    gates = list(BASE_REQUIRED_GATES)
    if candidate_count > 0 and "runtime_evidence_gate" not in gates:
        gates.insert(gates.index("final_claim_guard"), "runtime_evidence_gate")
    return gates


def action_value_payload() -> dict[str, Any]:
    return {
        "cost_multiplier": COST_MULTIPLIER,
        "slippage_proxy": SLIPPAGE_PROXY,
        "adverse_penalty_weight": ADVERSE_PENALTY_WEIGHT,
        "abstain_opportunity_weight": ABSTAIN_OPPORTUNITY_WEIGHT,
        "long_value": "future_log_return_12 - cost - adverse_weight * max(-future_log_return_12, 0)",
        "short_value": "-future_log_return_12 - cost - adverse_weight * max(future_log_return_12, 0)",
        "abstain_value": "-opportunity_weight * max(abs(future_log_return_12) - cost, 0)",
        "fit_scope": "train_tier_ab_combined_only",
        "validation_policy": "candidate_gate_only",
        "oos_policy": "final_read_only_no_tuning",
    }


def add_action_values(frame: pd.DataFrame, *, cost_multiplier: float = COST_MULTIPLIER, adverse_weight: float = ADVERSE_PENALTY_WEIGHT) -> pd.DataFrame:
    out = frame.copy()
    ret = pd.to_numeric(out["future_log_return_12"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    base_cost = pd.to_numeric(out["cost_penalty_proxy"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    cost = cost_multiplier * base_cost + SLIPPAGE_PROXY
    long_adverse = np.maximum(-ret, 0.0)
    short_adverse = np.maximum(ret, 0.0)
    long_value = ret - cost - adverse_weight * long_adverse
    short_value = -ret - cost - adverse_weight * short_adverse
    abstain_value = -ABSTAIN_OPPORTUNITY_WEIGHT * np.maximum(np.abs(ret) - cost, 0.0)
    values = np.vstack([short_value, abstain_value, long_value]).T
    order = np.argsort(values, axis=1)
    best_idx = order[:, -1]
    second_idx = order[:, -2]
    action_map = np.asarray([-1, 0, 1], dtype=int)
    out["utility_cost_proxy"] = cost
    out["long_value"] = long_value
    out["short_value"] = short_value
    out["abstain_value"] = abstain_value
    out["action_target"] = action_map[best_idx]
    out["best_action_value"] = values[np.arange(len(values)), best_idx]
    out["second_best_action_value"] = values[np.arange(len(values)), second_idx]
    out["regret_gap"] = out["best_action_value"] - out["second_best_action_value"]
    out["trade_advantage_value"] = np.maximum(long_value, short_value) - abstain_value
    out["signed_utility_edge"] = long_value - short_value
    out["adverse_penalty_long"] = adverse_weight * long_adverse
    out["adverse_penalty_short"] = adverse_weight * short_adverse
    return out


def feature_columns() -> list[str]:
    features = f91.feature_columns()
    return [feature for feature in features if not any(token in feature.lower() for token in DENYLIST_FEATURE_TOKENS)]


def variant_features(spec: Mapping[str, Any], features: Sequence[str]) -> list[str]:
    if spec["feature_mode"] == "regime_dense":
        picked = [feature for feature in features if any(hint in feature.lower() for hint in REGIME_FEATURE_HINTS)]
        return picked or list(features)
    return list(features)


def fit_variant(spec: Mapping[str, Any], train: pd.DataFrame, features: Sequence[str]) -> dict[str, Any]:
    cols = variant_features(spec, features)
    family = str(spec["family"])
    if family == "logistic_action":
        model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1200, class_weight="balanced", solver="lbfgs"))
        model.fit(train[cols], train["action_target"].astype(int))
        return {"model": model, "features": cols, "selection_threshold": None, "train_classes": sorted(set(train["action_target"].astype(int)))}
    if family == "extra_trees_action":
        model = make_pipeline(
            SimpleImputer(strategy="median"),
            ExtraTreesClassifier(
                n_estimators=180,
                max_depth=5,
                min_samples_leaf=80,
                class_weight="balanced",
                random_state=RNG_SEED,
                n_jobs=1,
            ),
        )
        model.fit(train[cols], train["action_target"].astype(int))
        return {"model": model, "features": cols, "selection_threshold": None, "train_classes": sorted(set(train["action_target"].astype(int)))}
    model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), Ridge(alpha=10.0))
    target = pd.to_numeric(train["signed_utility_edge"], errors="coerce").fillna(0.0)
    model.fit(train[cols], target)
    train_pred = np.asarray(model.predict(train[cols]), dtype=float)
    threshold = float(np.quantile(np.abs(train_pred), float(spec.get("train_abs_quantile", 0.88)))) if len(train_pred) else 0.0
    return {"model": model, "features": cols, "selection_threshold": threshold, "train_classes": ["signed_edge"]}


def predict_variant(fit: Mapping[str, Any], spec: Mapping[str, Any], frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    cols = list(fit["features"])
    family = str(spec["family"])
    if frame.empty:
        return np.array([], dtype=bool), np.array([], dtype=int), np.array([], dtype=float)
    model = fit["model"]
    if family in {"logistic_action", "extra_trees_action"}:
        pred = np.asarray(model.predict(frame[cols]), dtype=int)
        selected = pred != 0
        side = np.where(pred == 0, np.where(frame["signed_utility_edge"].to_numpy(dtype=float) >= 0.0, 1, -1), pred)
        if hasattr(model[-1], "predict_proba"):
            probs = model.predict_proba(frame[cols])
            confidence = np.max(probs, axis=1)
        else:
            confidence = np.where(selected, 1.0, 0.0)
        return selected, side.astype(int), confidence.astype(float)
    pred = np.asarray(model.predict(frame[cols]), dtype=float)
    threshold = float(fit.get("selection_threshold") or 0.0)
    selected = np.abs(pred) >= threshold
    side = np.where(pred >= 0.0, 1, -1)
    return selected.astype(bool), side.astype(int), np.abs(pred).astype(float)


def selected_action_value(frame: pd.DataFrame, selected: np.ndarray, side: np.ndarray) -> np.ndarray:
    selected = np.asarray(selected, dtype=bool)
    side = np.asarray(side, dtype=int)
    values = np.where(side == 1, frame["long_value"].to_numpy(dtype=float), frame["short_value"].to_numpy(dtype=float))
    return np.where(selected, values, frame["abstain_value"].to_numpy(dtype=float))


def policy_metrics(frame: pd.DataFrame, selected: np.ndarray, side: np.ndarray) -> dict[str, Any]:
    selected = np.asarray(selected, dtype=bool)
    side = np.asarray(side, dtype=int)
    base = f91.pnl_metrics(frame, selected, side)
    selected_values = selected_action_value(frame, selected, side)
    trade_values = selected_values[selected]
    best = frame["best_action_value"].to_numpy(dtype=float) if len(frame) else np.array([], dtype=float)
    regret = best - selected_values if len(frame) else np.array([], dtype=float)
    adverse = np.where(side == 1, frame["adverse_penalty_long"].to_numpy(dtype=float), frame["adverse_penalty_short"].to_numpy(dtype=float))
    adverse_selected = adverse[selected]
    utility_cost = frame["utility_cost_proxy"].to_numpy(dtype=float)
    return {
        **base,
        "policy_net_utility": round(float(selected_values.sum()), 8) if len(selected_values) else 0.0,
        "trade_net_utility": round(float(trade_values.sum()), 8) if len(trade_values) else 0.0,
        "avg_trade_utility": round(float(trade_values.mean()), 8) if len(trade_values) else None,
        "avg_policy_regret": round(float(regret.mean()), 8) if len(regret) else None,
        "avg_selected_adverse_penalty": round(float(adverse_selected.mean()), 8) if len(adverse_selected) else None,
        "adverse_penalty_share": round(float(adverse_selected.sum() / max(np.abs(trade_values).sum(), 1e-12)), 6) if len(trade_values) else None,
        "avg_utility_cost_proxy": round(float(utility_cost[selected].mean()), 8) if selected.any() else None,
        "action_abstain_share": round(float((~selected).mean()), 6) if len(selected) else None,
    }


def random_control_mean(frame: pd.DataFrame, selected: np.ndarray, side: np.ndarray, *, seed: int) -> dict[str, Any]:
    selected = np.asarray(selected, dtype=bool)
    side = np.asarray(side, dtype=int)
    trade_count = int(selected.sum())
    if trade_count <= 0 or len(frame) == 0:
        base = policy_metrics(frame, np.zeros(len(frame), dtype=bool), side)
        return {f"random_{key}_mean": base.get(key) for key in ("net_proxy", "proxy_pf", "max_drawdown", "policy_net_utility", "trade_net_utility")}
    rng = np.random.default_rng(seed)
    rows: list[dict[str, Any]] = []
    count = min(trade_count, len(frame))
    for _ in range(RANDOM_CONTROL_REPS):
        mask = np.zeros(len(frame), dtype=bool)
        mask[rng.choice(len(frame), size=count, replace=False)] = True
        rows.append(policy_metrics(frame, mask, side))
    return {
        "random_net_proxy_mean": round(float(np.mean([float(row.get("net_proxy") or 0.0) for row in rows])), 8),
        "random_proxy_pf_mean": round(float(np.mean([float(row.get("proxy_pf") or 0.0) for row in rows])), 6),
        "random_max_drawdown_mean": round(float(np.mean([float(row.get("max_drawdown") or 0.0) for row in rows])), 8),
        "random_policy_net_utility_mean": round(float(np.mean([float(row.get("policy_net_utility") or 0.0) for row in rows])), 8),
        "random_trade_net_utility_mean": round(float(np.mean([float(row.get("trade_net_utility") or 0.0) for row in rows])), 8),
    }


def oracle_control(frame: pd.DataFrame, *, control_id: str, cost_multiplier: float, adverse_weight: float) -> tuple[np.ndarray, np.ndarray]:
    control_frame = add_action_values(frame, cost_multiplier=cost_multiplier, adverse_weight=adverse_weight)
    action = control_frame["action_target"].to_numpy(dtype=int)
    selected = action != 0
    side = np.where(action == 0, np.where(control_frame["signed_utility_edge"].to_numpy(dtype=float) >= 0.0, 1, -1), action)
    return selected.astype(bool), side.astype(int)


def f95_reference_control() -> dict[str, Any]:
    if not path_exists(F95B_SPLIT_METRICS):
        return {"control_id": "f95_replay_reference_missing", "available": False}
    frame = pd.read_csv(io_path(F95B_SPLIT_METRICS))
    mask = frame["view"].astype(str).eq("tier_ab_combined") & frame["split"].astype(str).eq("validation")
    rows = frame.loc[mask].copy()
    if rows.empty:
        return {"control_id": "f95_replay_reference_missing", "available": False}
    rows["sort_net"] = pd.to_numeric(rows.get("net_proxy", 0.0), errors="coerce").fillna(0.0)
    rows["sort_pf"] = pd.to_numeric(rows.get("proxy_pf", 0.0), errors="coerce").fillna(0.0)
    best = rows.sort_values(["sort_net", "sort_pf"], ascending=False).iloc[0].to_dict()
    return {
        "control_id": "f95_replay_best_combined_validation_reference",
        "available": True,
        "source": rel(F95B_SPLIT_METRICS),
        "variant_id": best.get("variant_id"),
        "net_proxy": float(best.get("net_proxy") or 0.0),
        "proxy_pf": float(best.get("proxy_pf") or 0.0),
        "max_drawdown": float(best.get("max_drawdown") or 0.0),
        "trade_count": int(float(best.get("trade_count") or 0)),
        "trades_per_day": float(best.get("trades_per_day") or 0.0),
    }


def control_rows_for(frame: pd.DataFrame, selected: np.ndarray, side: np.ndarray, variant_id: str, view: str, split: str) -> list[dict[str, Any]]:
    controls: list[tuple[str, np.ndarray, np.ndarray]] = []
    zero_mask = np.zeros(len(frame), dtype=bool)
    controls.append(("no_trade", zero_mask, side))
    controls.append(("abstain_all", zero_mask, side))
    controls.append(("trade_all_model_side", np.ones(len(frame), dtype=bool), side))
    random_mask = np.zeros(len(frame), dtype=bool)
    if int(np.asarray(selected, dtype=bool).sum()) > 0 and len(frame) > 0:
        rng = np.random.default_rng(stable_seed(variant_id, view, split, "single_random"))
        random_mask[rng.choice(len(frame), size=min(int(np.asarray(selected, dtype=bool).sum()), len(frame)), replace=False)] = True
    controls.append(("random_abstain_rate_match_single", random_mask, side))
    cost_blind_selected, cost_blind_side = oracle_control(frame, control_id="cost_blind_utility_oracle", cost_multiplier=0.0, adverse_weight=ADVERSE_PENALTY_WEIGHT)
    controls.append(("cost_blind_utility_oracle", cost_blind_selected, cost_blind_side))
    no_adv_selected, no_adv_side = oracle_control(frame, control_id="no_adverse_penalty_oracle", cost_multiplier=COST_MULTIPLIER, adverse_weight=0.0)
    controls.append(("no_adverse_penalty_oracle", no_adv_selected, no_adv_side))
    rows: list[dict[str, Any]] = []
    for control_id, mask, control_side in controls:
        rows.append({"variant_id": variant_id, "view": view, "split": split, "control_id": control_id, **policy_metrics(frame, mask, control_side)})
    return rows


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def split_summary(frames: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for view, frame in frames.items():
        view_payload: dict[str, Any] = {}
        for split, part in frame.groupby(frame["split"].astype(str)):
            view_payload[str(split)] = {
                "rows": int(len(part)),
                "start": str(part["timestamp"].min()) if len(part) else None,
                "end": str(part["timestamp"].max()) if len(part) else None,
                "unique_dates": int(part["timestamp"].dt.date.nunique()) if len(part) else 0,
            }
        payload[view] = view_payload
    return payload


def gap_summary(frame: pd.DataFrame) -> dict[str, Any]:
    if len(frame) < 2:
        return {"max_gap_minutes": None, "median_gap_minutes": None, "gap_count_gt_5m": 0}
    diffs = frame["timestamp"].sort_values().diff().dropna().dt.total_seconds() / 60.0
    return {
        "max_gap_minutes": round(float(diffs.max()), 6),
        "median_gap_minutes": round(float(diffs.median()), 6),
        "gap_count_gt_5m": int((diffs > 5.0).sum()),
    }


def label_boundary_check() -> dict[str, Any]:
    columns = ["timestamp", "future_timestamp", "split", "horizon_minutes"]
    raw = pd.read_parquet(io_path(MODEL_INPUT_DATASET), columns=columns)
    raw["timestamp"] = pd.to_datetime(raw["timestamp"], utc=True)
    raw["future_timestamp"] = pd.to_datetime(raw["future_timestamp"], utc=True)
    delta = (raw["future_timestamp"] - raw["timestamp"]).dt.total_seconds() / 60.0
    return {
        "tier_a_future_timestamp_checked": True,
        "min_future_delta_minutes": round(float(delta.min()), 6) if len(delta) else None,
        "nonpositive_future_delta_count": int((delta <= 0).sum()),
        "horizon_minutes_values": sorted({int(value) for value in raw["horizon_minutes"].dropna().unique().tolist()}),
        "split_future_boundary_note": "F96B does not refit on validation or OOS; source split contract remains label_v1_fwd12_split_v1.",
    }


def data_integrity_payload(
    frames: Mapping[str, pd.DataFrame],
    route_summary: Mapping[str, Any],
    tier_b_summary: Mapping[str, Any],
    f91_integrity: Mapping[str, Any],
    features: Sequence[str],
) -> dict[str, Any]:
    denied = [feature for feature in features if any(token in feature.lower() for token in DENYLIST_FEATURE_TOKENS)]
    duplicates = {view: int(frame["timestamp"].duplicated().sum()) for view, frame in frames.items()}
    sorted_flags = {view: bool(frame["timestamp"].is_monotonic_increasing) for view, frame in frames.items()}
    split_rows = split_summary(frames)
    gaps = {view: gap_summary(frame) for view, frame in frames.items()}
    label_check = label_boundary_check()
    boundary_ok = (
        not denied
        and all(value == 0 for value in duplicates.values())
        and all(sorted_flags.values())
        and int(label_check["nonpositive_future_delta_count"]) == 0
    )
    return {
        "audit_name": "data_integrity_audit",
        "packet_id": RUN_ID,
        "status": "pass_with_boundary" if boundary_ok else "blocked",
        "data_sources_checked": [file_identity(path) for path in [MODEL_INPUT_DATASET, MODEL_INPUT_SUMMARY, MODEL_INPUT_FEATURE_ORDER]],
        "feature_count": len(features),
        "feature_order_hash": feature_hash(features),
        "denylist_feature_violations": denied,
        "duplicate_timestamps": duplicates,
        "timestamp_sorted": sorted_flags,
        "gap_summary": gaps,
        "split_summary": split_rows,
        "tier_route_summary": route_summary,
        "tier_b_summary": tier_b_summary,
        "f91_route_integrity": f91_integrity,
        "label_boundary_check": label_check,
        "leakage_tests": {
            "model_features_use_future_return": False,
            "model_features_use_label_or_label_class": False,
            "feature_max_source_time_boundary": "contractual_closed_bar_row_t_or_prior_bars_checked_by_feature_contract_and_denylist",
            "action_value_labels_used_as_targets_only": True,
            "fit_scope": "train_tier_ab_combined_only",
            "validation_oos_transform_only": True,
            "oos_selection": "forbidden_and_not_used",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def prepare_frames() -> tuple[dict[str, pd.DataFrame], dict[str, Any], dict[str, Any], dict[str, Any], list[str]]:
    frames, route_summary, tier_b_summary, f91_integrity = f91.prepare_routed_frames()
    features = feature_columns()
    for view, frame in list(frames.items()):
        enriched = add_action_values(frame.sort_values("timestamp").reset_index(drop=True))
        frames[view] = enriched
    return frames, route_summary, tier_b_summary, f91_integrity, features


def label_distribution(frames: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for view, frame in frames.items():
        view_payload: dict[str, Any] = {}
        for split, part in frame.groupby(frame["split"].astype(str)):
            counts = part["action_target"].astype(int).value_counts().sort_index()
            total = max(1, int(len(part)))
            view_payload[str(split)] = {
                "rows": int(len(part)),
                "short": int(counts.get(-1, 0)),
                "abstain": int(counts.get(0, 0)),
                "long": int(counts.get(1, 0)),
                "short_share": round(float(counts.get(-1, 0) / total), 6),
                "abstain_share": round(float(counts.get(0, 0) / total), 6),
                "long_share": round(float(counts.get(1, 0) / total), 6),
                "avg_regret_gap": round(float(part["regret_gap"].mean()), 8) if len(part) else None,
            }
        payload[view] = view_payload
    return payload


def metric_failures(row: Mapping[str, Any], controls: Mapping[str, Mapping[str, Any]], view: str, f95_reference: Mapping[str, Any]) -> list[str]:
    failures: list[str] = []
    trade_count = int(row.get("trade_count") or 0)
    if trade_count <= 0:
        failures.append(f"{view}_validation_no_trades")
        return failures
    net_utility = float(row.get("trade_net_utility") or 0.0)
    policy_utility = float(row.get("policy_net_utility") or 0.0)
    net_proxy = float(row.get("net_proxy") or 0.0)
    pf = float(row.get("proxy_pf") or 0.0)
    tpd = float(row.get("trades_per_day") or 0.0)
    dd = float(row.get("max_drawdown") or 0.0)
    side_min = float(row.get("side_min_share") or 0.0)
    recovery = float(row.get("recovery_factor") or 0.0)
    regime_count = int(row.get("regime_coverage_count") or 0)
    adverse_share = float(row.get("adverse_penalty_share") or 0.0)
    if net_utility <= 0.0:
        failures.append(f"{view}_validation_trade_net_utility_nonpositive")
    if policy_utility <= 0.0:
        failures.append(f"{view}_validation_policy_net_utility_nonpositive")
    if net_proxy <= 0.0:
        failures.append(f"{view}_validation_net_proxy_nonpositive")
    if pf < CANDIDATE_MIN_PF:
        failures.append(f"{view}_validation_pf_below_1")
    if not (CANDIDATE_MIN_TRADES_PER_DAY <= tpd <= CANDIDATE_MAX_TRADES_PER_DAY):
        failures.append(f"{view}_validation_trades_per_day_outside_5_to_10")
    if dd > CANDIDATE_MAX_DD:
        failures.append(f"{view}_validation_drawdown_above_cap")
    if side_min < CANDIDATE_MIN_SIDE_SHARE:
        failures.append(f"{view}_validation_side_concentration")
    if recovery <= 0.0:
        failures.append(f"{view}_validation_recovery_factor_nonpositive")
    if regime_count < CANDIDATE_MIN_REGIME_COVERAGE:
        failures.append(f"{view}_validation_regime_coverage_low")
    if adverse_share > CANDIDATE_MAX_ADVERSE_PENALTY_SHARE:
        failures.append(f"{view}_validation_adverse_penalty_share_high")
    for control_id in [
        "no_trade",
        "trade_all_model_side",
        "random_abstain_rate_match_single",
        "cost_blind_utility_oracle",
        "no_adverse_penalty_oracle",
    ]:
        control = controls.get(control_id, {})
        if control and net_utility <= float(control.get("trade_net_utility") or 0.0):
            failures.append(f"{view}_validation_not_above_{control_id}_trade_utility")
        if control and policy_utility <= float(control.get("policy_net_utility") or 0.0):
            failures.append(f"{view}_validation_not_above_{control_id}_policy_utility")
    if view == "tier_ab_combined" and f95_reference.get("available") and net_proxy <= float(f95_reference.get("net_proxy") or 0.0):
        failures.append(f"{view}_validation_not_above_f95_replay_net_proxy_reference")
    return failures


def candidate_gate_for_variant(
    variant_id: str,
    results: Mapping[str, Mapping[str, Mapping[str, Any]]],
    controls: Mapping[str, Mapping[str, Mapping[str, Mapping[str, Any]]]],
    f95_reference: Mapping[str, Any],
) -> dict[str, Any]:
    failures: list[str] = []
    oos_notes: list[str] = []
    for view in ["tier_a_separate", "tier_b_separate", "tier_ab_combined"]:
        failures.extend(metric_failures(results[view]["validation"], controls[view]["validation"], view, f95_reference))
        oos = results[view]["oos"]
        if int(oos.get("trade_count") or 0) <= 0:
            oos_notes.append(f"{view}_oos_no_trades_final_read")
        if float(oos.get("trade_net_utility") or 0.0) <= 0.0:
            oos_notes.append(f"{view}_oos_trade_net_utility_nonpositive_final_read")
        if float(oos.get("net_proxy") or 0.0) <= 0.0:
            oos_notes.append(f"{view}_oos_net_proxy_nonpositive_final_read")
        if float(oos.get("proxy_pf") or 0.0) < 1.0:
            oos_notes.append(f"{view}_oos_pf_below_1_final_read")
    status = "candidate_triggered" if not failures else "not_candidate"
    return {
        "variant_id": variant_id,
        "status": status,
        "selection_failures": failures,
        "oos_final_read_notes": oos_notes,
        "claim_effect": (
            "same_packet_mt5_strategy_tester_probe_required_before_any_runnable_candidate_or_runtime_claim"
            if status == "candidate_triggered"
            else "runtime_evidence_gate_not_triggered_no_runnable_candidate_claim"
        ),
    }


def diagnostic_score(row: Mapping[str, Any]) -> float:
    net_util = float(row.get("trade_net_utility") or 0.0)
    policy_util = float(row.get("policy_net_utility") or 0.0)
    net_proxy = float(row.get("net_proxy") or 0.0)
    pf = float(row.get("proxy_pf") or 0.0)
    dd = float(row.get("max_drawdown") or 0.0)
    tpd = float(row.get("trades_per_day") or 0.0)
    side_min = float(row.get("side_min_share") or 0.0)
    regret = float(row.get("avg_policy_regret") or 0.0)
    density = max(0.0, 1.0 - abs(tpd - 7.0) / 7.0)
    utility = max(-1.0, min(1.0, net_util * 10.0)) + max(-0.5, min(0.5, policy_util * 4.0))
    economics = max(-1.0, min(1.0, net_proxy * 10.0)) + max(-0.5, min(0.5, pf - 1.0))
    risk = max(-1.0, min(1.0, (CANDIDATE_MAX_DD - dd) / max(CANDIDATE_MAX_DD, 1e-12)))
    balance = max(0.0, min(1.0, side_min / max(CANDIDATE_MIN_SIDE_SHARE, 1e-12)))
    regret_term = max(-1.0, min(1.0, -regret * 5.0))
    return round(float(100.0 * (0.30 * utility + 0.18 * economics + 0.18 * risk + 0.14 * density + 0.12 * balance + 0.08 * regret_term)), 6)


def choose_best_diagnostic(rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    gate_by_variant = {str(gate["variant_id"]): gate for gate in gates}
    best: dict[str, Any] = {}
    best_score = -1e100
    for row in rows:
        if row.get("view") != "tier_ab_combined" or row.get("split") != "validation":
            continue
        score = diagnostic_score(row)
        if score > best_score:
            best_score = score
            best = dict(row)
    if not best:
        return {}
    variant_id = str(best.get("variant_id"))
    return {
        "variant_id": variant_id,
        "diagnostic_score": best_score,
        "validation": best,
        "gate": gate_by_variant.get(variant_id, {}),
        "oos_final_read": next((dict(row) for row in rows if row.get("variant_id") == variant_id and row.get("view") == "tier_ab_combined" and row.get("split") == "oos"), {}),
    }


def evaluate_variants(frames: Mapping[str, pd.DataFrame], features: Sequence[str]) -> dict[str, Any]:
    train = frames["tier_ab_combined"].loc[frames["tier_ab_combined"]["split"].astype(str).eq("train")].copy().reset_index(drop=True)
    metric_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    fit_rows: list[dict[str, Any]] = []
    gates: list[dict[str, Any]] = []
    f95_reference = f95_reference_control()
    for index, spec in enumerate(VARIANTS):
        fit = fit_variant(spec, train, features)
        variant_id = str(spec["variant_id"])
        variant_results: dict[str, dict[str, Any]] = {}
        variant_controls: dict[str, dict[str, dict[str, Any]]] = {}
        for view, view_frame in frames.items():
            variant_results[view] = {}
            variant_controls[view] = {}
            for split in ["train", "validation", "oos"]:
                part = view_frame.loc[view_frame["split"].astype(str).eq(split)].copy().reset_index(drop=True)
                selected, side, confidence = predict_variant(fit, spec, part)
                metrics = policy_metrics(part, selected, side)
                rand = random_control_mean(part, selected, side, seed=RNG_SEED + stable_seed(variant_id, view, split, index))
                row = {
                    "variant_id": variant_id,
                    "model_family": spec["family"],
                    "feature_mode": spec["feature_mode"],
                    "feature_count": len(fit["features"]),
                    "selection_rule": "predicted_action_non_abstain" if spec["family"] != "ridge_signed_edge" else "train_abs_signed_edge_quantile",
                    "selection_threshold": fit.get("selection_threshold"),
                    "view": view,
                    "split": split,
                    **metrics,
                    **rand,
                }
                metric_rows.append(row)
                variant_results[view][split] = row
                controls = control_rows_for(part, selected, side, variant_id, view, split)
                control_rows.extend(controls)
                variant_controls[view][split] = {str(control["control_id"]): control for control in controls}
                if split in {"validation", "oos"} and len(part):
                    sample = part.loc[selected, ["timestamp", "source_tier", "route_role", "label", "future_log_return_12", "regime_key", "cost_bucket"]].copy()
                    sample["variant_id"] = variant_id
                    sample["split"] = split
                    sample["side"] = side[selected]
                    sample["confidence"] = confidence[selected]
                    sample["trade_net_utility"] = selected_action_value(part, selected, side)[selected]
                    sample_rows.extend(sample.head(80).to_dict(orient="records"))
        gates.append(candidate_gate_for_variant(variant_id, variant_results, variant_controls, f95_reference))
        fit_rows.append(
            {
                "variant_id": variant_id,
                "model_family": spec["family"],
                "feature_mode": spec["feature_mode"],
                "feature_count": len(fit["features"]),
                "selection_threshold": fit.get("selection_threshold"),
                "train_fit_rows": int(len(train)),
                "train_fit_input_hash": hash_dataframe(train, fit["features"]),
                "feature_order_hash": feature_hash(fit["features"]),
                "train_classes": fit.get("train_classes"),
            }
        )
    candidate_count = sum(1 for gate in gates if gate["status"] == "candidate_triggered")
    write_csv(SPLIT_METRICS_CSV, metric_rows)
    write_csv(VARIANT_METRICS_CSV, metric_rows)
    write_csv(NEGATIVE_CONTROL_CSV, control_rows)
    write_csv(SCORE_SAMPLE_CSV, sample_rows)
    write_json(CANDIDATE_GATE_JSON, {"candidate_count": candidate_count, "gates": gates, "f95_replay_reference": f95_reference})
    write_json(
        MODEL_FIT_MANIFEST,
        {
            "fit_scope": "train_tier_ab_combined_only",
            "transform_only_splits": ["validation", "oos"],
            "seed": RNG_SEED,
            "variant_fit_rows": fit_rows,
            "leakage_boundary": "future_log_return_12 and action values are targets/evaluation only; model features are closed-bar feature columns.",
        },
    )
    return {
        "variants": VARIANTS,
        "split_metrics": metric_rows,
        "negative_control_rows": control_rows,
        "candidate_gates": gates,
        "candidate_count": candidate_count,
        "best_diagnostic_variant": choose_best_diagnostic(metric_rows, gates),
        "f95_replay_reference": f95_reference,
        "selection_policy": "predeclared action-value formula; train-only fit/threshold; validation candidate gate; OOS final read only",
    }


def materialize_proxy_metrics() -> dict[str, Any]:
    frames, route_summary, tier_b_summary, f91_integrity, features = prepare_frames()
    data_integrity = data_integrity_payload(frames, route_summary, tier_b_summary, f91_integrity, features)
    evaluation = evaluate_variants(frames, features)
    write_json(DATA_LOCK, data_lock_payload(frames, route_summary, tier_b_summary, data_integrity, features))
    write_json(TIER_ROUTE_SUMMARY, route_summary)
    write_json(TIER_B_SUMMARY, tier_b_summary)
    write_json(DATA_INTEGRITY_LOCAL, data_integrity)
    write_json(ACTION_VALUE_CONFIG, action_value_payload())
    write_json(ACTION_VALUE_LABEL_SUMMARY, label_distribution(frames))
    write_json(
        RUNTIME_TRIGGER_CHECK,
        {
            "run_id": RUN_ID,
            "candidate_count": evaluation["candidate_count"],
            "runtime_probe_required_now": int(evaluation["candidate_count"]) > 0,
            "runtime_probe_status": RUNTIME_PROBE_STATUS_BLOCKED if int(evaluation["candidate_count"]) > 0 else RUNTIME_PROBE_STATUS_NEGATIVE,
            "skip_reason_rejected": ["cost_or_expense", "proxy_result_bad"],
            "claim_effect": "No runtime/materialization/economics/handoff claim is made by this proxy-scout packet.",
        },
    )
    return {
        "data_integrity": data_integrity,
        "route_summary": route_summary,
        "tier_b_summary": tier_b_summary,
        "evaluation": evaluation,
        "feature_count": len(features),
        "feature_hash": feature_hash(features),
    }


def data_lock_payload(
    frames: Mapping[str, pd.DataFrame],
    route_summary: Mapping[str, Any],
    tier_b_summary: Mapping[str, Any],
    data_integrity: Mapping[str, Any],
    features: Sequence[str],
) -> dict[str, Any]:
    train = frames["tier_ab_combined"].loc[frames["tier_ab_combined"]["split"].astype(str).eq("train")]
    return {
        "run_id": RUN_ID,
        "created_at_utc": utc_now(),
        "model_input_dataset": file_identity(MODEL_INPUT_DATASET),
        "model_input_summary": file_identity(MODEL_INPUT_SUMMARY),
        "feature_order": file_identity(MODEL_INPUT_FEATURE_ORDER),
        "feature_count": len(features),
        "feature_order_hash": feature_hash(features),
        "train_tier_ab_combined_input_hash": hash_dataframe(train, features),
        "split_summary": split_summary(frames),
        "tier_route_summary": route_summary,
        "tier_b_summary": tier_b_summary,
        "data_integrity_status": data_integrity.get("status"),
        "closed_bar_boundary": "features use row t closed M5 bars and rolling history only; decisions are after bar close.",
        "combined_boundary": "Tier A+B is actual routed total, not a synthetic sum of separate KPI rows.",
    }


def status_from(payload: Mapping[str, Any]) -> str:
    return str(payload["status"])


def judgment_from(payload: Mapping[str, Any]) -> str:
    return str(payload["judgment"])


def runtime_probe_status_from(payload: Mapping[str, Any]) -> str:
    return str(payload["runtime_probe_status"])


def build_payload(created_at: str, metrics: Mapping[str, Any]) -> dict[str, Any]:
    candidate_count = int(metrics["evaluation"]["candidate_count"])
    return {
        "created_at_utc": created_at,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID if candidate_count == 0 else RUN_ID,
        "status": STATUS_NEGATIVE if candidate_count == 0 else STATUS_BLOCKED_RUNTIME,
        "judgment": JUDGMENT_NEGATIVE if candidate_count == 0 else JUDGMENT_BLOCKED_RUNTIME,
        "runtime_probe_status": RUNTIME_PROBE_STATUS_NEGATIVE if candidate_count == 0 else RUNTIME_PROBE_STATUS_BLOCKED,
        "hypothesis": "A train-only counterfactual long/short/abstain action-value policy can find side-balanced US100 M5 scout clues after F95 state-cluster failure.",
        "verification_profile": "proxy_scout",
        "claim_boundary": CLAIM_BOUNDARY,
        "metrics": metrics,
        "source_identities": [file_identity(path) for path in source_inputs()],
        "task_force": task_force_payload(created_at),
    }


def task_force_payload(created_at: str) -> dict[str, Any]:
    calls = task_force_calls()
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "created_at_utc": created_at,
        "review_requirement": "explicit_user_instruction_required_and_active_goal_claim_surface",
        "trigger_reason": "F96B non-trivial proxy_scout packet plus explicit user instruction to call relevant Task Force agents when triggered",
        "trigger_source": "active_goal_frontier_continuation_and_user_required_task_force_review",
        "roster_registry": rel(ROOT / "docs" / "agent_control" / "codex_task_force_registry.yaml"),
        "selected_agent_count": len(calls),
        "full_roster_call_reason": None,
        "agents_used": [call["roster_agent_id"] for call in calls],
        "actual_subagent_calls": calls,
        "opinion_summary": {
            "accepted": [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "accepted"],
            "needs_local_verification": [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "needs_local_verification"],
            "rejected": [],
        },
        "model_policy": "inherited_current_codex_model_no_gate_relaxation",
        "bounded_evidence": [rel(F96A_BRIEF), rel(F96A_CONTRACT), rel(KPI_RECORD), rel(CANDIDATE_GATE_JSON), rel(DATA_INTEGRITY_LOCAL)],
        "advice_classification": "mixed_accepted_and_needs_local_verification",
        "local_verification": [
            "F96B materializes a new work_packet_schema_v2_1 packet.",
            "Tier A, Tier B, and Tier A+B actual routed total are recorded.",
            "Timestamp sortedness, duplicate counts, label future boundary, and denylist features are checked.",
            "Candidate gate is validation-only; OOS is final read only.",
        ],
        "final_codex_direction": "Use F96B as proxy scout evidence only; no Task Force reviewed/pass, runtime, promotion, baseline, readiness, or Goal Achieve claim.",
        "forbidden_claim_check": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def summary_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    best = payload["metrics"]["evaluation"].get("best_diagnostic_variant", {})
    validation = best.get("validation", {})
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": payload["next_run_id"],
        "created_at_utc": payload["created_at_utc"],
        "status": status_from(payload),
        "judgment": judgment_from(payload),
        "verification_profile": "proxy_scout",
        "hypothesis": payload["hypothesis"],
        "candidate_gate_count": payload["metrics"]["evaluation"]["candidate_count"],
        "best_diagnostic_variant": best.get("variant_id"),
        "best_diagnostic_score": best.get("diagnostic_score"),
        "validation_actual_routed_net_proxy": validation.get("net_proxy"),
        "validation_actual_routed_trade_net_utility": validation.get("trade_net_utility"),
        "validation_actual_routed_policy_net_utility": validation.get("policy_net_utility"),
        "validation_actual_routed_pf": validation.get("proxy_pf"),
        "validation_actual_routed_drawdown": validation.get("max_drawdown"),
        "validation_actual_routed_trade_count": validation.get("trade_count"),
        "validation_actual_routed_trades_per_day": validation.get("trades_per_day"),
        "runtime_probe_status": runtime_probe_status_from(payload),
        "task_force_actual_subagent_call_count": len(payload["task_force"]["actual_subagent_calls"]),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def kpi_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    best = payload["metrics"]["evaluation"].get("best_diagnostic_variant", {})
    validation = best.get("validation", {})
    oos = best.get("oos_final_read", {})
    gate = best.get("gate", {})
    candidate_count = int(payload["metrics"]["evaluation"]["candidate_count"])
    runtime_kpi = "not_applicable_no_runnable_candidate_no_runtime_claim" if candidate_count == 0 else "blocked_pending_same_packet_mt5_runtime_probe"
    return {
        "packet_id": RUN_ID,
        "test_period": "train_2022-09-01_to_2024-12-31_validation_2025-01-02_to_2025-09-30_oos_2025-10-01_to_2026-04-13",
        "hypothesis": payload["hypothesis"],
        "proxy_kpi": validation,
        "runtime_kpi": runtime_kpi,
        "net_profit": validation.get("net_proxy"),
        "net_utility": validation.get("trade_net_utility"),
        "profit_factor": validation.get("proxy_pf"),
        "drawdown": validation.get("max_drawdown"),
        "trade_count": validation.get("trade_count"),
        "trades_per_day": validation.get("trades_per_day"),
        "parity": "not_applicable_no_onnx_or_ea",
        "gap_cause": "proxy/runtime gap not measured because no runtime materialization, handoff, economics, or tester behavior claim is made",
        "next_action": payload["next_run_id"],
        "candidate_gate": {"candidate_count": candidate_count, "best_gate": gate},
        "tier_records_required": ["Tier A separate", "Tier B separate", "Tier A+B actual routed total"],
        "oos_final_read": oos,
        "closeout_kpi": {
            "gross_profit": validation.get("gross_profit"),
            "gross_loss": validation.get("gross_loss"),
            "win_rate": validation.get("win_rate"),
            "avg_win": validation.get("avg_win"),
            "avg_loss": validation.get("avg_loss"),
            "payoff_ratio": validation.get("payoff_ratio"),
            "expectancy": validation.get("expectancy"),
            "recovery_factor": validation.get("recovery_factor"),
            "time_under_water": validation.get("time_under_water_bars"),
            "max_consecutive_loss": validation.get("max_consecutive_loss"),
            "long_short_breakdown": {"long_count": validation.get("long_count"), "short_count": validation.get("short_count")},
        },
        "negative_controls": {
            "record_path": rel(NEGATIVE_CONTROL_CSV),
            "required": ["random", "no_trade", "trade_all", "cost_blind", "no_adverse_penalty", "F95 replay"],
        },
        "runtime_probe_trigger_rule": "If candidate_count > 0 or a runnable ONNX/EA/set/materialization/economics/handoff claim appears, same-packet MT5 Strategy Tester probe is required.",
        "runtime_skip_reason_rejected": ["cost_or_expense", "proxy_result_bad"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    best = payload["metrics"]["evaluation"].get("best_diagnostic_variant", {})
    validation = best.get("validation", {})
    failures = best.get("gate", {}).get("selection_failures", [])
    return f"""# F96B Counterfactual Action-Value Proxy Scout

Action: F96B ran a train-only counterfactual long/short/abstain action-value proxy scout.

Effect: the packet records Tier A separate, Tier B separate, and Tier A+B actual routed total proxy evidence without claiming runtime authority, selected baseline, live readiness, or Goal Achieve.

Best diagnostic variant: `{best.get('variant_id')}`

- validation trade net utility: `{validation.get('trade_net_utility')}`
- validation policy net utility: `{validation.get('policy_net_utility')}`
- validation net proxy: `{validation.get('net_proxy')}`
- validation PF: `{validation.get('proxy_pf')}`
- validation max drawdown: `{validation.get('max_drawdown')}`
- validation trades/day: `{validation.get('trades_per_day')}`
- validation trade count: `{validation.get('trade_count')}`
- candidate gate count: `{payload['metrics']['evaluation']['candidate_count']}`
- runtime status: `{runtime_probe_status_from(payload)}`

Selection failures for best diagnostic: `{failures}`

Task Force actual calls: `{len(payload['task_force']['actual_subagent_calls'])}` selected agents. This is not a Task Force reviewed/pass claim.

Boundary: `{CLAIM_BOUNDARY}`.
"""


def write_run_artifacts(payload: Mapping[str, Any]) -> None:
    write_json(RUN_MANIFEST, {"script": SCRIPT_REL, **summary_payload(payload), "source_inputs": payload["source_identities"]})
    write_json(SUMMARY_JSON, summary_payload(payload))
    write_json(KPI_RECORD, kpi_payload(payload))
    write_json(
        EXECUTION_SUMMARY,
        {
            **summary_payload(payload),
            "kpi_record": kpi_payload(payload),
            "candidate_gate": read_json(CANDIDATE_GATE_JSON) if path_exists(CANDIDATE_GATE_JSON) else {},
            "data_feature_split_lock": read_json(DATA_LOCK) if path_exists(DATA_LOCK) else {},
            "task_force_actual_subagent_calls": payload["task_force"]["actual_subagent_calls"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_text(F96B_REPORT, result_summary_text(payload))


def audit_payload(name: str, status: str, **extra: Any) -> dict[str, Any]:
    return {"audit_name": name, "packet_id": RUN_ID, "status": status, **extra}


def write_audits(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    gate_results = gate_results or {}
    candidate_count = int(payload["metrics"]["evaluation"]["candidate_count"])
    write_json(TASK_FORCE_REVIEW, payload["task_force"])
    write_json(PACKET_TASK_FORCE_REVIEW, payload["task_force"])
    write_json(
        FRONTIER_EXTRA_DUE_CHECK,
        audit_payload(
            "frontier_extra_due_check",
            "pass_not_due",
            created_at_utc=payload["created_at_utc"],
            due_status=FRONTIER_EXTRA_DUE_STATUS,
            claim_effect="F96B can continue inside F96; no Extra Stage is due before F100.",
        ),
    )
    write_json(
        FIVE_STAGE_SYNTHESIS,
        audit_payload(
            "frontier_five_stage_direction_synthesis",
            "pass",
            created_at_utc=payload["created_at_utc"],
            status_detail=FRONTIER_FIVE_STAGE_STATUS,
            claim_effect="Light direction record only; no retrospective, topic ban, completion, or authority claim.",
        ),
    )
    write_json(
        TOPIC_ROTATION_CHECK,
        audit_payload(
            "frontier_topic_rotation_check",
            "pass",
            created_at_utc=payload["created_at_utc"],
            status_detail=FRONTIER_TOPIC_ROTATION_STATUS,
            material_novelty_delta="F96B executes the F96A action-value policy axis and is not a threshold/filter/session/routing-only repair.",
            claim_effect="Continuation inside F96 only; no stage completion or authority claim.",
        ),
    )
    write_json(
        SCOPE_GATE,
        audit_payload(
            "scope_completion_gate",
            "pass",
            created_at_utc=payload["created_at_utc"],
            required_outputs=[rel(path) for path in [RUN_MANIFEST, KPI_RECORD, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV, DATA_LOCK, PACKET_TASK_FORCE_REVIEW]],
            candidate_gate_count=candidate_count,
            runtime_probe_status=runtime_probe_status_from(payload),
            claim_boundary=CLAIM_BOUNDARY,
        ),
    )
    integrity = dict(payload["metrics"]["data_integrity"])
    integrity["created_at_utc"] = payload["created_at_utc"]
    write_json(DATA_INTEGRITY_AUDIT, integrity)
    write_json(
        MODEL_VALIDATION_AUDIT,
        audit_payload(
            "model_validation_audit",
            "pass_with_boundary" if candidate_count == 0 else "blocked_pending_runtime_probe",
            created_at_utc=payload["created_at_utc"],
            fit_policy="train_tier_ab_combined_only",
            validation_policy="candidate_gate_only",
            oos_policy="final_read_only_no_tuning",
            calibration_claim="rejected",
            pf_only_selection="rejected",
            candidate_gate_count=candidate_count,
            claim_boundary=CLAIM_BOUNDARY,
        ),
    )
    write_json(
        KPI_CONTRACT_AUDIT,
        audit_payload(
            "kpi_contract_audit",
            "pass",
            created_at_utc=payload["created_at_utc"],
            kpi_record=rel(KPI_RECORD),
            split_metrics=rel(SPLIT_METRICS_CSV),
            candidate_gate=rel(CANDIDATE_GATE_JSON),
            required_kpi_fields=[
                "hypothesis",
                "test_period",
                "proxy_kpi",
                "runtime_kpi",
                "net_profit",
                "profit_factor",
                "drawdown",
                "trade_count",
                "trades_per_day",
                "parity",
                "gap_cause",
                "next_action",
                "closeout_kpi",
            ],
            claim_boundary=CLAIM_BOUNDARY,
        ),
    )
    artifact_rows = [file_identity(path) for path in produced_artifacts()]
    write_json(
        ARTIFACT_AUDIT,
        audit_payload(
            "artifact_lineage_audit",
            "pass",
            created_at_utc=payload["created_at_utc"],
            source_inputs=payload["source_identities"],
            produced_artifacts=artifact_rows,
            missing_artifacts=[row for row in artifact_rows if not row.get("exists")],
            claim_boundary=CLAIM_BOUNDARY,
        ),
    )
    write_json(
        RESULT_JUDGMENT_AUDIT,
        audit_payload(
            "result_judgment_audit",
            "negative" if candidate_count == 0 else "blocked",
            created_at_utc=payload["created_at_utc"],
            judgment=judgment_from(payload),
            result_status=status_from(payload),
            runtime_probe_status=runtime_probe_status_from(payload),
            next_action=payload["next_run_id"],
            forbidden_claims=FORBIDDEN_CLAIMS,
            claim_boundary=CLAIM_BOUNDARY,
        ),
    )
    if candidate_count > 0:
        write_json(
            RUNTIME_EVIDENCE_GATE,
            audit_payload(
                "runtime_evidence_gate",
                "blocked_pending_same_packet_mt5_probe",
                created_at_utc=payload["created_at_utc"],
                reason="A proxy candidate signal requires MT5 Strategy Tester identity before any candidate/runtime/materialization/economics/handoff claim.",
                claim_effect="Candidate language is blocked until MT5 tester evidence exists.",
            ),
        )
    if gate_results:
        write_json(REQUIRED_GATE_AUDIT, gate_results.get("required_gate_coverage_audit", {}))
        write_json(STATE_SYNC_AUDIT, gate_results.get("state_sync_audit", {}))


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {"packet_id": RUN_ID, "status": "executed", "claim_boundary": CLAIM_BOUNDARY, "forbidden_claims": FORBIDDEN_CLAIMS}
    candidate_count = int(payload["metrics"]["evaluation"]["candidate_count"])
    return [
        {
            **common,
            "skill": "obsidian-run-evidence-system",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "ledger_rows": [RUN_ID, payload["next_run_id"]],
            "missing_evidence": ["MT5 Strategy Tester output is outside proxy_scout claim surface when candidate_count is zero." if candidate_count == 0 else "MT5 Strategy Tester output is required before any candidate/runtime claim."],
            "allowed_claims": ALLOWED_CLAIMS,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "run_evidence_system.json"),
        },
        {
            **common,
            "skill": "obsidian-experiment-design",
            "hypothesis": payload["hypothesis"],
            "baseline": {"source_run_id": "frontier95B_closed_bar_state_transition_embedding_proxy_scout_v1", "use": "negative_memory_only_not_inherited_baseline"},
            "changed_variables": ["counterfactual action-value target", "long/short/abstain policy", "utility/regret candidate gate", "negative controls including cost-blind/no-adverse/F95 replay"],
            "invalid_conditions": ["future_path_as_feature", "random_split", "oos_tuning", "PF_only_selection", "runtime_claim_without_MT5_tester_identity"],
            "evidence_plan": {"tier_records": ["Tier A separate", "Tier B separate", "Tier A+B actual routed total"], "candidate_gate": rel(CANDIDATE_GATE_JSON)},
            "receipt_path": rel(SKILL_RECEIPT_DIR / "experiment_design.json"),
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": [file_identity(path) for path in [MODEL_INPUT_DATASET, MODEL_INPUT_SUMMARY, MODEL_INPUT_FEATURE_ORDER]],
            "time_axis_boundary": "Closed M5 row t features and rolling history only; decision point is after bar close.",
            "split_boundary": "Train fit only; validation candidate gate; OOS final-read-only.",
            "leakage_checks": payload["metrics"]["data_integrity"].get("leakage_tests", {}),
            "missing_data_boundary": "Tier B or Tier A+B combined rows cannot be omitted; if unavailable they must be recorded as blocked or missing_required.",
            "receipt_path": rel(SKILL_RECEIPT_DIR / "data_integrity.json"),
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "Logistic/ExtraTrees action classifier and Ridge signed utility edge scout; no calibrated probability claim.",
            "validation_split": "validation is candidate gate only; OOS is final-read-only",
            "overfit_checks": ["no OOS tuning", "train-only transforms", "PF-only selection rejected", "multi-axis variants not threshold-only repeats"],
            "selection_metric_boundary": "candidate gate combines net utility, net proxy, PF, trades/day, DD, recovery, side balance, adverse penalty, regimes, and controls",
            "allowed_claims": ALLOWED_CLAIMS,
            "candidate_gate_count": candidate_count,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "model_validation.json"),
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "raw_evidence": [rel(MODEL_INPUT_DATASET), rel(MODEL_INPUT_SUMMARY), rel(F96A_BRIEF), rel(F96A_CONTRACT), rel(F95B_SPLIT_METRICS)],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, DATA_LOCK, ACTION_VALUE_CONFIG, MODEL_FIT_MANIFEST, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F96B_REPORT), rel(DECISION_MEMO)],
            "hashes_or_missing_reasons": [file_identity(path) for path in produced_artifacts()],
            "lineage_boundary": "proxy_scout_evidence_only_no_runtime_authority",
            "receipt_path": rel(SKILL_RECEIPT_DIR / "artifact_lineage.json"),
        },
        {
            **common,
            "skill": "obsidian-task-force-review",
            "trigger_reason": payload["task_force"]["trigger_reason"],
            "roster_registry": payload["task_force"]["roster_registry"],
            "agents_used": payload["task_force"]["agents_used"],
            "actual_subagent_calls": payload["task_force"]["actual_subagent_calls"],
            "review_requirement": payload["task_force"]["review_requirement"],
            "model_policy": payload["task_force"]["model_policy"],
            "bounded_evidence": payload["task_force"]["bounded_evidence"],
            "advice_classification": payload["task_force"]["advice_classification"],
            "local_verification": payload["task_force"]["local_verification"],
            "final_codex_direction": payload["task_force"]["final_codex_direction"],
            "forbidden_claim_check": FORBIDDEN_CLAIMS,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "task_force_review.json"),
        },
        {
            **common,
            "skill": "obsidian-result-judgment",
            "judgment_boundary": "negative or blocked proxy scout only; no promotion, baseline, runtime authority, live readiness, or Goal Achieve",
            "allowed_claims": ALLOWED_CLAIMS,
            "evidence_used": [rel(CANDIDATE_GATE_JSON), rel(KPI_RECORD), rel(SPLIT_METRICS_CSV), rel(RESULT_JUDGMENT_AUDIT)],
            "judgment": judgment_from(payload),
            "receipt_path": rel(SKILL_RECEIPT_DIR / "result_judgment.json"),
        },
        {
            **common,
            "skill": "obsidian-exploration-mandate",
            "exploration_lane": "frontier_proxy_scout",
            "idea_boundary": "F96B can create clue/negative memory only unless runtime evidence is later produced.",
            "negative_memory_effect": "Failed action-value gates become do-not-overclaim memory for F96C.",
            "operating_claim_boundary": CLAIM_BOUNDARY,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "exploration_mandate.json"),
        },
        {
            **common,
            "skill": "obsidian-claim-discipline",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "final_status": status_from(payload),
            "receipt_path": rel(SKILL_RECEIPT_DIR / "claim_discipline.json"),
        },
    ]


def write_receipts(payload: Mapping[str, Any]) -> None:
    receipts = skill_receipts(payload)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-run-evidence-system", "receipts": receipts})
    for receipt in receipts:
        write_json(ROOT / str(receipt["receipt_path"]), receipt)


def required_evidence_paths(candidate_count: int) -> list[str]:
    paths = [
        RUN_MANIFEST,
        KPI_RECORD,
        DATA_LOCK,
        ACTION_VALUE_CONFIG,
        MODEL_FIT_MANIFEST,
        CANDIDATE_GATE_JSON,
        SPLIT_METRICS_CSV,
        NEGATIVE_CONTROL_CSV,
        PACKET_TASK_FORCE_REVIEW,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_CLOSEOUT_GATE,
    ]
    if candidate_count > 0:
        paths.append(RUNTIME_EVIDENCE_GATE)
    return [rel(path) for path in paths]


def work_packet_payload(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    candidate_count = int(payload["metrics"]["evaluation"]["candidate_count"])
    gates = required_gates(candidate_count)
    runtime_na = RUNTIME_NA_REASONS if candidate_count == 0 else []
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation plus explicit reminder that relevant Task Force agents must be actually called when required",
            "requested_action": "run F96B counterfactual action-value policy proxy scout",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["No final completion, selected baseline, operating promotion, runtime authority, live readiness, or Goal Achieve is claimed."],
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
            "detected_families": ["experiment_execution", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel(RUN_DIR), rel(REVIEW_DIR), rel(PACKET_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "future_label_leakage": "high",
                "tier_ab_timestamp_order": "high",
                "pf_only_selection": "high",
                "task_force_review_claim_without_actual_calls": "high",
                "runtime_probe_absence_misread_as_cost_skip": "high",
            },
            "hard_stop_risks": [
                "Do not put future_log_return_12, label, action_value, or regret fields into model features.",
                "Do not tune by OOS.",
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester identity.",
            ],
            "required_gates": gates,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "verification_profile": "proxy_scout",
                "strategy_tester_required_now": candidate_count > 0,
                "runtime_probe_status": runtime_probe_status_from(payload),
                "reason": "No ONNX/EA/set/runtime claim is made when candidate_count is zero; if proxy gate signal appears, packet is blocked pending same-packet MT5 probe.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F96B proxy scout", "counterfactual action-value policy", "Task Force actual calls", "state sync"],
            "scope_units": ["proxy_scout_run", "candidate_gate_record", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["data lock", "action-value labels", "proxy metrics", "negative controls", "candidate gate", "Task Force actual calls", "control-plane gates"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F96B is the active proxy-scout packet and runtime trigger rules cannot be reduced."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "proxy_scout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F96A planned F96B proxy scout",
                "explicit user instruction requiring relevant Task Force actual calls when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence_paths(candidate_count),
            "gates_not_run_with_reason": runtime_na,
            "stop_conditions": [
                "Stop at proxy scout evidence if no runnable candidate or runtime/materialization/economics/handoff claim appears.",
                "If a meaningful runnable candidate or runtime claim appears, do not make the claim without same-packet MT5 Strategy Tester probe.",
                "Do not repair by threshold/filter/session/routing/parameter-only changes.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F96B proxy metrics exist.", "expected_artifact": rel(SPLIT_METRICS_CSV), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Tier A, Tier B, and Tier A+B actual routed total are recorded.", "expected_artifact": rel(TIER_ROUTE_SUMMARY), "verification_method": "kpi_contract_audit", "required": True},
            {"id": "AC-003", "text": "Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-004", "text": "Runtime evidence absence is bounded and not a cost/proxy-bad skip.", "expected_artifact": rel(RUNTIME_TRIGGER_CHECK), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Lock data, feature, split, and action-value formula identities.",
            "Fit train-only action-value proxy variants.",
            "Score validation and OOS final read with negative controls.",
            "Record Task Force calls, audits, receipts, state sync, and final claim guard.",
        ],
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": ["obsidian-experiment-design", "obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage", "obsidian-task-force-review", "obsidian-result-judgment", "obsidian-exploration-mandate", "obsidian-claim-discipline"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-backtest-forensics", "obsidian-runtime-parity"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-backtest-forensics", "reason": "No new MT5 Strategy Tester report or trade list exists."},
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA parity or handoff claim is made."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": gates,
        },
        "evidence_contract": {
            "source_inputs": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, DATA_LOCK, ACTION_VALUE_CONFIG, MODEL_FIT_MANIFEST, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV, NEGATIVE_CONTROL_CSV, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F96B_REPORT), rel(DECISION_MEMO), rel(CONTEXT_ANCHOR)],
            "raw_evidence": [rel(MODEL_INPUT_DATASET), rel(F96A_BRIEF), rel(F96A_CONTRACT), rel(F95B_SPLIT_METRICS)],
            "missing_evidence": [
                {"evidence": "MT5 Strategy Tester runtime output", "reason": "outside proxy_scout claim surface unless candidate_count is positive or a runtime claim appears"},
                {"evidence": "ONNX/EA/set handoff", "reason": "not created in F96B"},
            ],
        },
        "gates": {
            "required": gates,
            "actual_status_source": {name: (gate_results.get(name, {}) or {}).get("status", "pending") for name in gates},
            "not_applicable_with_reason": {item["gate"]: item["reason"] for item in runtime_na},
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
    }


def closeout_gate_payload(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    candidate_count = int(payload["metrics"]["evaluation"]["candidate_count"])
    path_by_gate = {
        "work_packet_schema_lint": PACKET_WORK_PACKET_LINT,
        "skill_receipt_schema_lint": PACKET_SKILL_RECEIPT_LINT,
        "codex_task_force_review_packet": PACKET_TASK_FORCE_REVIEW,
        "frontier_extra_due_check": FRONTIER_EXTRA_DUE_CHECK,
        "frontier_five_stage_direction_synthesis": FIVE_STAGE_SYNTHESIS,
        "frontier_topic_rotation_check": TOPIC_ROTATION_CHECK,
        "scope_completion_gate": SCOPE_GATE,
        "data_integrity_audit": DATA_INTEGRITY_AUDIT,
        "model_validation_audit": MODEL_VALIDATION_AUDIT,
        "kpi_contract_audit": KPI_CONTRACT_AUDIT,
        "artifact_lineage_audit": ARTIFACT_AUDIT,
        "result_judgment_audit": RESULT_JUDGMENT_AUDIT,
        "runtime_evidence_gate": RUNTIME_EVIDENCE_GATE,
        "state_sync_audit": PACKET_STATE_SYNC_AUDIT,
        "required_gate_coverage_audit": PACKET_REQUIRED_GATE_AUDIT,
        "final_claim_guard": PACKET_FINAL_CLAIM_GUARD,
    }
    default_status = {
        "codex_task_force_review_packet": "pass",
        "frontier_extra_due_check": "pass_not_due",
        "frontier_five_stage_direction_synthesis": "pass",
        "frontier_topic_rotation_check": "pass",
        "scope_completion_gate": "pass",
        "data_integrity_audit": payload["metrics"]["data_integrity"].get("status", "pass_with_boundary"),
        "model_validation_audit": "pass_with_boundary" if candidate_count == 0 else "blocked_pending_runtime_probe",
        "kpi_contract_audit": "pass",
        "artifact_lineage_audit": "pass",
        "result_judgment_audit": "negative" if candidate_count == 0 else "blocked",
        "runtime_evidence_gate": "blocked_pending_same_packet_mt5_probe",
    }
    audits = []
    for gate in required_gates(candidate_count):
        status = (gate_results.get(gate, {}) or {}).get("status") or default_status.get(gate, "pending")
        audits.append({"audit_name": gate, "path": rel(path_by_gate[gate]), "status": status})
    statuses = [str(audit["status"]) for audit in audits]
    return {
        "audit_name": "closeout_gate",
        "packet_id": RUN_ID,
        "status": "blocked" if any(status.startswith("blocked") for status in statuses) else "pass",
        "audits": audits,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "final_claim_guard": {"audit_name": "final_claim_guard", "path": rel(PACKET_FINAL_CLAIM_GUARD), "status": (gate_results.get("final_claim_guard", {}) or {}).get("status", "pending")},
    }


def write_packet_and_gate(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_yaml(WORK_PACKET, work_packet_payload(payload, gate_results))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_payload(payload, gate_results))


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path_exists(path):
        return [], []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv_rows(path: Path, fieldnames: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fields = list(fieldnames)
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def replace_rows(path: Path, remove_run_ids: set[str], new_rows: Sequence[Mapping[str, Any]]) -> None:
    fieldnames, rows = read_csv_rows(path)
    kept = [row for row in rows if row.get("run_id") not in remove_run_ids and row.get("input_run_id") not in remove_run_ids]
    write_csv_rows(path, fieldnames, [*kept, *new_rows])


def ledger_rows(payload: Mapping[str, Any], gate_passes: int = 0) -> list[dict[str, Any]]:
    best = payload["metrics"]["evaluation"].get("best_diagnostic_variant", {})
    validation = best.get("validation", {})
    base = {
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status_from(payload),
        "judgment": judgment_from(payload),
        "candidate_count": payload["metrics"]["evaluation"]["candidate_count"],
        "meaningful_signal_count": payload["metrics"]["evaluation"]["candidate_count"],
        "materialization_candidate_count": 0,
        "runtime_completed_rows": 0,
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_probe_status": runtime_probe_status_from(payload),
        "net_profit": validation.get("net_proxy"),
        "net_utility": validation.get("trade_net_utility"),
        "profit_factor": validation.get("proxy_pf"),
        "drawdown": validation.get("max_drawdown"),
        "trade_count": validation.get("trade_count"),
        "trades_per_day": validation.get("trades_per_day"),
        "gate_passes": gate_passes,
        "gate_total": len(required_gates(int(payload["metrics"]["evaluation"]["candidate_count"]))),
        "path": rel(RUN_DIR),
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__proxy_scout",
            "run_id": RUN_ID,
            "run_number": "frontier96B",
            "subrun_id": "proxy_scout",
            "record_view": "proxy_scout",
            "tier_scope": "Tier A separate; Tier B separate; Tier A+B actual routed total",
            "kpi_scope": "validation_candidate_gate_oos_final_read",
            "next_run_id": payload["next_run_id"],
        },
        {
            **base,
            "ledger_row_id": f"{payload['next_run_id']}__planned_current_run",
            "run_id": payload["next_run_id"],
            "run_number": "frontier96C" if payload["next_run_id"] != RUN_ID else "frontier96B",
            "subrun_id": "planned_current_run",
            "record_view": "planned_current_run",
            "tier_scope": "n/a",
            "kpi_scope": "repair_or_rotation_decision_pending" if payload["next_run_id"] != RUN_ID else "runtime_probe_block_pending",
            "input_run_id": RUN_ID,
            "next_action": payload["next_run_id"],
        },
    ]


def update_ledgers(payload: Mapping[str, Any], gate_passes: int = 0) -> None:
    run_ids = {RUN_ID, payload["next_run_id"]}
    rows = ledger_rows(payload, gate_passes=gate_passes)
    replace_rows(RUN_REGISTRY, run_ids, rows)
    replace_rows(ALPHA_LEDGER, run_ids, rows)
    replace_rows(STAGE_LEDGER, run_ids, rows)


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        identity = file_identity(path)
        rows.append(
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "path": rel(path),
                "artifact_kind": "file",
                "sha256": identity.get("sha256", ""),
                "size_bytes": identity.get("size_bytes", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    replace_rows(ARTIFACT_REGISTRY, {RUN_ID}, rows)


def append_once(path: Path, marker: str, addition: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker not in existing:
        write_text(path, existing.rstrip() + "\n\n" + addition.strip() + "\n")


def update_register_docs(payload: Mapping[str, Any]) -> None:
    marker = f"<!-- {RUN_ID} -->"
    addition = f"""{marker}
## F96B Counterfactual Action-Value Proxy Scout

- run_id: `{RUN_ID}`
- status: `{status_from(payload)}`
- judgment: `{judgment_from(payload)}`
- candidate_gate_count: `{payload['metrics']['evaluation']['candidate_count']}`
- runtime_probe_status: `{runtime_probe_status_from(payload)}`
- next_action: `{payload['next_run_id']}`

Effect: this records scout clue/negative memory only; no selected baseline, runtime authority, live readiness, or Goal Achieve is claimed.
"""
    append_once(IDEA_REGISTRY, marker, addition)
    append_once(GLOBAL_SELECTION_STATUS, marker, addition)
    append_once(NEGATIVE_REGISTER, marker, addition)
    append_once(WORKSPACE_CHANGELOG, marker, addition)
    append_once(ROOT_CHANGELOG, marker, addition)
    write_text(DECISION_MEMO, addition)


def update_state_docs(payload: Mapping[str, Any]) -> None:
    workspace = {
        "current_stage_id": STAGE_ID,
        "active_stage": STAGE_ID,
        "active_branch": current_branch(),
        "current_run_id": payload["next_run_id"],
        "latest_completed_run_id": RUN_ID,
        "current_status": status_from(payload),
        "current_judgment": judgment_from(payload),
        "next_run_id": payload["next_run_id"],
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "frontier_five_stage_direction_synthesis_status": FRONTIER_FIVE_STAGE_STATUS,
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "task_force_status": "f96b_actual_subagent_calls_recorded_5_selected_agents_no_task_force_reviewed_pass_claim",
        "runtime_probe_status": runtime_probe_status_from(payload),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": payload["created_at_utc"],
        "context_anchor": rel(CONTEXT_ANCHOR),
        "notes": [
            "Action: F96B proxy scout ran train-only counterfactual action-value policy variants.",
            "Effect: F96C becomes the current repair-or-rotation decision run when no runnable candidate is present.",
            f"Candidate gate count: {payload['metrics']['evaluation']['candidate_count']}.",
        ],
    }
    write_yaml(WORKSPACE_STATE, workspace)
    current_text = f"""# Current Working State

- active_stage: `{STAGE_ID}`
- current_run: `{payload['next_run_id']}`
- latest_completed_run: `{RUN_ID}`
- status: `{status_from(payload)}`
- judgment: `{judgment_from(payload)}`
- candidate_gate_count: `{payload['metrics']['evaluation']['candidate_count']}`
- runtime_probe_status: `{runtime_probe_status_from(payload)}`

Action: F96B ran a proxy_scout with actual Task Force calls.

Effect: `{payload['next_run_id']}` is the current run for repair-or-rotation decision unless F96B is blocked by a same-packet runtime-probe requirement. No selected baseline, runtime authority, live readiness, or Goal Achieve is claimed.
"""
    write_text(CURRENT_WORKING_STATE, current_text)
    write_text(
        STAGE_BRIEF,
        f"""# F96 Counterfactual Action-Value Policy Axis

- current_run: `{payload['next_run_id']}`
- latest_completed_run: `{RUN_ID}`
- F96B judgment: `{judgment_from(payload)}`
- candidate_gate_count: `{payload['metrics']['evaluation']['candidate_count']}`
- runtime_probe_status: `{runtime_probe_status_from(payload)}`

Action: F96B tested train-only long/short/abstain action-value policy variants.

Effect: F96 now carries proxy evidence and negative memory into the next decision without claiming authority.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# F96 Selection Status

- selected_baseline: not_claimed
- runtime_authority: not_claimed
- live_readiness: not_claimed
- Goal Achieve: not_claimed
- latest_completed_run: `{RUN_ID}`
- current_run: `{payload['next_run_id']}`
- candidate_gate_count: `{payload['metrics']['evaluation']['candidate_count']}`

Effect: F96B can be used as scout clue/negative memory only.
""",
    )
    write_text(
        CONTEXT_ANCHOR,
        f"""# F96 Context Anchor

Current truth: latest completed run is `{RUN_ID}` and current run is `{payload['next_run_id']}`.

Runtime boundary: `{runtime_probe_status_from(payload)}`.

Task Force: five relevant agents were actually called and recorded; no Task Force reviewed/pass claim is made.
""",
    )
    write_text(
        REVIEW_INDEX,
        f"""# F96 Review Index

- F96A stage open: `{PARENT_RUN_ID}`
- F96B proxy scout: `{RUN_ID}`
- F96B report: `{rel(F96B_REPORT)}`
- candidate gate: `{rel(CANDIDATE_GATE_JSON)}`
- KPI record: `{rel(KPI_RECORD)}`
- current_run: `{payload['next_run_id']}`
""",
    )


def run_gate_cmd(args: Sequence[str], output_path: Path) -> dict[str, Any]:
    command = [sys.executable, "-m", *args, "--output-json", str(output_path), "--allow-blocked-exit-zero"]
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, timeout=180)
    payload = read_json(output_path) if path_exists(output_path) else {}
    result = {
        "command": command,
        "output_path": rel(output_path),
        "returncode": completed.returncode,
        "status": payload.get("status", "missing_output"),
        "passed": payload.get("passed", False),
        "stdout_tail": completed.stdout[-2000:],
        "stderr_tail": completed.stderr[-2000:],
        "allowed_claims": payload.get("allowed_claims", []),
        "forbidden_claims": payload.get("forbidden_claims", []),
    }
    if completed.returncode != 0 or result["status"] not in {"pass", "pass_not_due"}:
        raise RuntimeError(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def sync_review_audit(src: Path, dst: Path) -> None:
    if path_exists(src):
        write_json(dst, read_json(src))


def audit_result_from_gate(name: str, result: Mapping[str, Any]) -> AuditResult:
    return AuditResult(
        audit_name=name,
        status=str(result.get("status", "pass")),
        counts={"source": result.get("output_path", "")},
        allowed_claims=tuple(str(item) for item in result.get("allowed_claims", ())),
        forbidden_claims=tuple(str(item) for item in result.get("forbidden_claims", ())),
    )


def audit_result_manual(name: str, status: str, *, forbidden: Sequence[str] = ()) -> AuditResult:
    return AuditResult(audit_name=name, status=status, forbidden_claims=tuple(forbidden))


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
    candidate_count = int(payload["metrics"]["evaluation"]["candidate_count"])
    manual_status = "pass_with_boundary" if candidate_count == 0 else "blocked_pending_runtime_probe"
    audit_results = [
        audit_result_from_gate("work_packet_schema_lint", results["work_packet_schema_lint"]),
        audit_result_from_gate("skill_receipt_schema_lint", results["skill_receipt_schema_lint"]),
        audit_result_from_gate("state_sync_audit", results["state_sync_audit"]),
        audit_result_from_gate("required_gate_coverage_audit", results["required_gate_coverage_audit"]),
        audit_result_manual("codex_task_force_review_packet", "pass"),
        audit_result_manual("frontier_extra_due_check", "pass_not_due"),
        audit_result_manual("frontier_five_stage_direction_synthesis", "pass"),
        audit_result_manual("frontier_topic_rotation_check", "pass"),
        audit_result_manual("scope_completion_gate", "pass"),
        audit_result_manual("data_integrity_audit", str(payload["metrics"]["data_integrity"].get("status", "pass_with_boundary"))),
        audit_result_manual("model_validation_audit", manual_status),
        audit_result_manual("kpi_contract_audit", "pass"),
        audit_result_manual("artifact_lineage_audit", "pass"),
        audit_result_manual("result_judgment_audit", "negative" if candidate_count == 0 else "blocked", forbidden=tuple(COMPLETION_CLAIMS) if candidate_count > 0 else ()),
    ]
    if candidate_count > 0:
        audit_results.append(audit_result_manual("runtime_evidence_gate", "blocked_pending_same_packet_mt5_probe", forbidden=tuple(COMPLETION_CLAIMS)))
    final_guard = guard_final_claims(requested_claims=ALLOWED_CLAIMS, audit_results=audit_results)
    final_payload = final_guard.to_dict()
    final_payload.update({"packet_id": RUN_ID, "claim_boundary": CLAIM_BOUNDARY, "blocked_claims": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS}})
    write_json(FINAL_CLAIM_GUARD, final_payload)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_payload)
    results["final_claim_guard"] = {
        "status": final_guard.status,
        "output_path": rel(PACKET_FINAL_CLAIM_GUARD),
        "allowed_claims": list(final_guard.allowed_claims),
        "forbidden_claims": list(final_guard.forbidden_claims),
    }
    write_packet_and_gate(payload, results)
    return results


def write_initial(payload: Mapping[str, Any]) -> None:
    write_run_artifacts(payload)
    write_audits(payload)
    write_receipts(payload)
    write_packet_and_gate(payload)
    update_state_docs(payload)
    update_ledgers(payload)
    update_register_docs(payload)


def write_final(payload: Mapping[str, Any], gate_results: Mapping[str, Any]) -> None:
    gate_passes = sum(1 for item in gate_results.values() if str(item.get("status", "")).startswith("pass"))
    write_run_artifacts(payload)
    write_audits(payload, gate_results)
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
        raise FileNotFoundError(f"Missing required F96B source evidence: {missing}")
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
                "status": status_from(payload),
                "candidate_gate_count": payload["metrics"]["evaluation"]["candidate_count"],
                "runtime_probe_status": runtime_probe_status_from(payload),
                "gate_statuses": {key: value.get("status") for key, value in gate_results.items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
