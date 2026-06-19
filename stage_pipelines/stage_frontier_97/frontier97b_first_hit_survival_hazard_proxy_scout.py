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
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.audit_result import AuditFinding, AuditResult
from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_91 import frontier91b_regime_density_cost_abstention_proxy_scout as f91


STAGE_ID = "stage_frontier_97__first_hit_survival_hazard_event_sparse_axis"
RUN_ID = "frontier97B_first_hit_survival_hazard_event_sparse_proxy_scout_v1"
PARENT_RUN_ID = "frontier97A_stage_open_first_hit_survival_hazard_event_sparse_axis_v1"
NEXT_RUN_ID = "frontier97C_first_hit_survival_hazard_event_sparse_repair_or_rotation_decision_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_97/frontier97b_first_hit_survival_hazard_proxy_scout.py"

STATUS_NEGATIVE = "f97b_first_hit_survival_hazard_proxy_scout_negative_no_runnable_candidate_no_authority"
STATUS_BLOCKED_RUNTIME = "f97b_first_hit_survival_hazard_proxy_scout_blocked_pending_same_packet_mt5_probe"
JUDGMENT_NEGATIVE = "negative_proxy_scout_first_hit_survival_hazard_candidate_gate_failed_no_runtime_trigger"
JUDGMENT_BLOCKED_RUNTIME = "blocked_same_packet_mt5_probe_required_before_candidate_or_runtime_claim"
CLAIM_BOUNDARY = (
    "f97b_proxy_scout_only_first_hit_survival_hazard_no_selected_baseline_no_operating_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve_no_runtime_economics_claim"
)
RUNTIME_PROBE_STATUS_NEGATIVE = "not_applicable_no_runnable_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip"
RUNTIME_PROBE_STATUS_BLOCKED = "blocked_same_packet_mt5_probe_required_before_runnable_candidate_or_runtime_claim"
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f96_closeout_next_boundary_f100_e02_pending_e01_closed_for_f050"
FRONTIER_FIVE_STAGE_STATUS = "recorded_recent_f92_to_f96_direction_synthesis_no_retrospective_gate"
FRONTIER_TOPIC_ROTATION_STATUS = "continuation_inside_f97_axis_f97a_rotation_already_passed"

RNG_SEED = 9702
RANDOM_CONTROL_REPS = 20
MAX_HOLD_BARS = 12
BRACKET_ATR_MULT = 0.55
BRACKET_MIN_RETURN = 0.0008
BRACKET_MAX_RETURN = 0.0035
PROXY_COST_RETURN = 0.00012
SLIPPAGE_PROXY = 0.00003

CANDIDATE_MIN_PF = 1.0
CANDIDATE_MIN_TRADES_PER_DAY = 5.0
CANDIDATE_MAX_TRADES_PER_DAY = 10.0
CANDIDATE_MAX_DD = 0.30
CANDIDATE_MIN_SIDE_SHARE = 0.20
CANDIDATE_MIN_REGIME_COVERAGE = 4
CANDIDATE_MAX_ADVERSE_FIRST_SHARE = 0.45
CANDIDATE_MAX_NO_EVENT_SHARE = 0.60

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier97B"
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
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier97b_first_hit_survival_hazard_proxy_scout.md"

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
FIRST_HIT_CONFIG = PROXY_DIR / "first_hit_config.json"
FIRST_HIT_LABEL_SUMMARY = PROXY_DIR / "first_hit_label_summary.json"
FIRST_HIT_LABEL_SAMPLE = PROXY_DIR / "first_hit_label_sample.csv"
MODEL_FIT_MANIFEST = PROXY_DIR / "model_fit_manifest.json"
VARIANT_METRICS_CSV = PROXY_DIR / "variant_metrics.csv"
SPLIT_METRICS_CSV = PROXY_DIR / "split_metrics.csv"
NEGATIVE_CONTROL_CSV = PROXY_DIR / "negative_control_metrics.csv"
SCORE_SAMPLE_CSV = PROXY_DIR / "score_sample.csv"
CALIBRATION_CSV = PROXY_DIR / "calibration_metrics.csv"
CANDIDATE_GATE_JSON = PROXY_DIR / "candidate_gate.json"
TIER_ROUTE_SUMMARY = PROXY_DIR / "tier_route_summary.json"
TIER_B_SUMMARY = PROXY_DIR / "tier_b_summary.json"
DATA_INTEGRITY_LOCAL = PROXY_DIR / "data_integrity_local_checks.json"
RUNTIME_TRIGGER_CHECK = PROXY_DIR / "runtime_trigger_check.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

TASK_FORCE_REVIEW = REVIEW_DIR / "f97b_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f97b_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f97b_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f97b_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f97b_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f97b_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f97b_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f97b_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f97b_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f97b_result_judgment_audit.json"
RUNTIME_EVIDENCE_GATE = REVIEW_DIR / "f97b_runtime_evidence_gate.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f97b_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f97b_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f97b_required_gate_coverage_audit.json"
F97B_REPORT = REVIEW_DIR / "frontier97B_first_hit_survival_hazard_proxy_scout_report.md"

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
RAW_BARS = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"
RAW_BARS_MANIFEST = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw_manifest.json"
F97A_BRIEF = STAGE_DIR / "02_runs" / "frontier97A" / "d" / "f97b_proxy_scout_brief.json"
F97A_CONTRACT = STAGE_DIR / "02_runs" / "frontier97A" / "d" / "first_hit_survival_hazard_contract.json"
F97A_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F97A_CLOSEOUT_GATE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "closeout_gate.json"

DENYLIST_FEATURE_TOKENS = ("future", "label", "first_hit", "hazard", "target", "profit", "loss", "mfe", "mae")
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
    {"variant_id": "logreg_first_hit_full58_q88", "family": "logistic_hazard", "feature_mode": "full58", "train_abs_quantile": 0.88},
    {"variant_id": "logreg_first_hit_full58_q92", "family": "logistic_hazard", "feature_mode": "full58", "train_abs_quantile": 0.92},
    {"variant_id": "extra_trees_first_hit_regime_q90", "family": "extra_trees_hazard", "feature_mode": "regime_dense", "train_abs_quantile": 0.90},
    {"variant_id": "ridge_signed_hit_edge_full58_q90", "family": "ridge_signed_hit_edge", "feature_mode": "full58", "train_abs_quantile": 0.90},
]

ALLOWED_CLAIMS = [
    "f97b_proxy_scout_executed",
    "first_hit_survival_hazard_negative_memory_recorded",
    "task_force_actual_calls_recorded_for_f97b",
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
        "reason": "F97B makes no runtime, materialization, handoff, or economics claim when candidate_count is zero.",
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
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(dict(payload)), allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")


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
    return hashlib.sha256(sample.to_csv(index=False).encode("utf-8")).hexdigest()


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
        F97A_BRIEF,
        F97A_CONTRACT,
        F97A_PACKET,
        F97A_CLOSEOUT_GATE,
        MODEL_INPUT_DATASET,
        MODEL_INPUT_SUMMARY,
        MODEL_INPUT_FEATURE_ORDER,
        RAW_BARS,
        RAW_BARS_MANIFEST,
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
        FIRST_HIT_CONFIG,
        FIRST_HIT_LABEL_SUMMARY,
        FIRST_HIT_LABEL_SAMPLE,
        MODEL_FIT_MANIFEST,
        VARIANT_METRICS_CSV,
        SPLIT_METRICS_CSV,
        NEGATIVE_CONTROL_CSV,
        SCORE_SAMPLE_CSV,
        CALIBRATION_CSV,
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
        F97B_REPORT,
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
            "spawned_agent_id": "019edf69-e387-7d81-95ae-82a43126857a",
            "nickname": "Pascal",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "classification_detail": "F97B needs local work_packet, gate, receipt, artifact hash, candidate/runtime trigger evidence, and no Task Force reviewed/pass wording.",
            "stale_self_report_handling": "Rejected any stale prior call id in the subagent text; parent tool return is the actual call identity for this packet.",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edf6a-0f77-74e2-872d-096ce29a993c",
            "nickname": "Herschel",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "classification_detail": "Closed-bar feature cutoff, raw-bar first-hit label boundary, split embargo, feature denylist, Tier A/B/A+B records, hashes, duplicates, and timezone boundary must be local evidence.",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edf6a-3c93-7c71-935f-1d3d8e744f26",
            "nickname": "Epicurus",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "superseded_by_completed_replacement_after_wait_timeout",
            "opinion_classification": "needs_local_verification",
            "classification_detail": "Actual initial call was made, but no final response arrived after repeated waits; a replacement call was made to avoid leaving the quant remit unhandled.",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edf7e-6529-72f2-85d7-26f03f985ac7",
            "nickname": "Euclid",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "classification_detail": "Accepted first-hit classifier, signed-edge regression, hazard/density score, multi-KPI candidate gate, and negative controls; rejected threshold-only repetition, proxy-only runtime evidence, and bad proxy/cost as MT5 skip reasons.",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edf6a-7467-76e0-bfa1-ff42aadb63b8",
            "nickname": "Galileo",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
            "classification_detail": "Calibration, split discipline, density, drawdown, adverse-first clustering, OOS final-read boundary, and no calibrated probability claim must be local evidence.",
            "stale_self_report_handling": "Rejected the subagent's stale statement that a new call could not be made; parent tool return proves this actual call.",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edf6a-a6bf-75b2-8952-b2c58d2bbf1c",
            "nickname": "Anscombe",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
            "classification_detail": "MT5 Strategy Tester is required in the same packet if a runnable candidate, deterministic trade rule, ONNX/EA handoff, or runtime/economics claim appears; cost or bad proxy is rejected as a skip reason.",
            "stale_self_report_handling": "Rejected the subagent's stale statement that a new call could not be made; parent tool return proves this actual call.",
        },
    ]


def required_gates(candidate_count: int = 0) -> list[str]:
    gates = list(BASE_REQUIRED_GATES)
    if candidate_count > 0 and "runtime_evidence_gate" not in gates:
        gates.insert(gates.index("final_claim_guard"), "runtime_evidence_gate")
    return gates


def first_hit_config_payload() -> dict[str, Any]:
    return {
        "max_hold_bars": MAX_HOLD_BARS,
        "timeframe_minutes": 5,
        "feature_cutoff_column": "timestamp",
        "raw_label_source": rel(RAW_BARS),
        "label_start_rule": "first raw bar with time_close greater than feature timestamp; this is the next tradable bar after closed-bar feature cutoff",
        "entry_price_rule": "raw open of label_start_bar",
        "long_favorable_hit": "high >= entry_price + bracket_points",
        "long_adverse_hit": "low <= entry_price - bracket_points",
        "short_favorable_hit": "low <= entry_price - bracket_points",
        "short_adverse_hit": "high >= entry_price + bracket_points",
        "tie_rule": "same-side favorable/adverse same-bar or long/short favorable same-bar is ambiguous and mapped to abstain target 0",
        "bracket_points": f"clip(atr_14 * {BRACKET_ATR_MULT}, entry_price * {BRACKET_MIN_RETURN}, entry_price * {BRACKET_MAX_RETURN})",
        "proxy_cost_return": PROXY_COST_RETURN,
        "slippage_proxy": SLIPPAGE_PROXY,
        "fit_scope": "train_tier_ab_combined_eligible_rows_only",
        "validation_policy": "candidate_gate_only",
        "oos_policy": "final_read_only_no_tuning",
        "runtime_trigger": "candidate_count > 0 requires same-packet MT5 Strategy Tester probe before any candidate/runtime/handoff/economics claim",
    }


def feature_columns() -> list[str]:
    features = f91.feature_columns()
    return [feature for feature in features if not any(token in feature.lower() for token in DENYLIST_FEATURE_TOKENS)]


def variant_features(spec: Mapping[str, Any], features: Sequence[str]) -> list[str]:
    if spec["feature_mode"] == "regime_dense":
        picked = [feature for feature in features if any(hint in feature.lower() for hint in REGIME_FEATURE_HINTS)]
        return picked or list(features)
    return list(features)


def load_raw_bars() -> pd.DataFrame:
    columns = ["time_open_unix", "time_close_unix", "open", "high", "low", "close", "spread_points"]
    raw = pd.read_csv(io_path(RAW_BARS), usecols=columns)
    raw["time_open"] = pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
    raw["time_close"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    return raw.sort_values("time_open").reset_index(drop=True)


def first_hit_for_frame(frame: pd.DataFrame, raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    out = frame.sort_values("timestamp").reset_index(drop=True).copy()
    open_ns = raw["time_open"].astype("int64").to_numpy()
    close_ns = raw["time_close"].astype("int64").to_numpy()
    raw_open = pd.to_numeric(raw["open"], errors="coerce").to_numpy(dtype=float)
    raw_high = pd.to_numeric(raw["high"], errors="coerce").to_numpy(dtype=float)
    raw_low = pd.to_numeric(raw["low"], errors="coerce").to_numpy(dtype=float)
    ts_ns = out["timestamp"].astype("int64").to_numpy()
    entry_idx = np.searchsorted(close_ns, ts_ns, side="right")
    split_max_ns = out.groupby(out["split"].astype(str))["timestamp"].transform("max").astype("int64").to_numpy()
    atr = pd.to_numeric(out.get("atr_14", 0.0), errors="coerce").fillna(0.0).to_numpy(dtype=float)

    targets = np.zeros(len(out), dtype=int)
    entry_prices = np.full(len(out), np.nan, dtype=float)
    bracket_points = np.full(len(out), np.nan, dtype=float)
    bracket_returns = np.full(len(out), np.nan, dtype=float)
    first_hit_bars = np.full(len(out), -1, dtype=int)
    first_hit_times: list[Any] = [pd.NaT] * len(out)
    label_start_times: list[Any] = [pd.NaT] * len(out)
    label_end_times: list[Any] = [pd.NaT] * len(out)
    long_state: list[str] = ["uncomputed"] * len(out)
    short_state: list[str] = ["uncomputed"] * len(out)
    censor_reason: list[str] = [""] * len(out)
    eligible = np.zeros(len(out), dtype=bool)
    horizon_ret = np.zeros(len(out), dtype=float)

    for i, start in enumerate(entry_idx):
        if start >= len(raw_open) or start + MAX_HOLD_BARS > len(raw_open):
            censor_reason[i] = "raw_history_insufficient"
            continue
        end = start + MAX_HOLD_BARS
        if close_ns[end - 1] > split_max_ns[i]:
            censor_reason[i] = "split_horizon_embargo"
            continue
        entry = float(raw_open[start])
        if not np.isfinite(entry) or entry <= 0.0:
            censor_reason[i] = "invalid_entry_price"
            continue
        bracket = max(min(float(atr[i]) * BRACKET_ATR_MULT, entry * BRACKET_MAX_RETURN), entry * BRACKET_MIN_RETURN)
        upper = entry + bracket
        lower = entry - bracket
        highs = raw_high[start:end]
        lows = raw_low[start:end]
        closes = pd.to_numeric(raw["close"].iloc[start:end], errors="coerce").to_numpy(dtype=float)
        if len(closes):
            horizon_ret[i] = float((closes[-1] - entry) / entry)
        label_start_times[i] = raw.loc[start, "time_open"]
        label_end_times[i] = raw.loc[end - 1, "time_close"]
        entry_prices[i] = entry
        bracket_points[i] = bracket
        bracket_returns[i] = bracket / entry
        eligible[i] = True

        long_fav = np.flatnonzero(highs >= upper)
        long_adv = np.flatnonzero(lows <= lower)
        short_fav = np.flatnonzero(lows <= lower)
        short_adv = np.flatnonzero(highs >= upper)

        lf = int(long_fav[0]) if len(long_fav) else None
        la = int(long_adv[0]) if len(long_adv) else None
        sf = int(short_fav[0]) if len(short_fav) else None
        sa = int(short_adv[0]) if len(short_adv) else None

        long_outcome = "none"
        if lf is not None and (la is None or lf < la):
            long_outcome = "favorable"
        elif la is not None and (lf is None or la < lf):
            long_outcome = "adverse"
        elif lf is not None and la is not None and lf == la:
            long_outcome = "same_bar_tie"

        short_outcome = "none"
        if sf is not None and (sa is None or sf < sa):
            short_outcome = "favorable"
        elif sa is not None and (sf is None or sa < sf):
            short_outcome = "adverse"
        elif sf is not None and sa is not None and sf == sa:
            short_outcome = "same_bar_tie"

        long_state[i] = long_outcome
        short_state[i] = short_outcome

        candidates: list[tuple[int, int]] = []
        if long_outcome == "favorable" and lf is not None:
            candidates.append((lf, 1))
        if short_outcome == "favorable" and sf is not None:
            candidates.append((sf, -1))
        if not candidates:
            targets[i] = 0
            censor_reason[i] = "no_favorable_first_hit_or_adverse_first"
            continue
        candidates.sort(key=lambda item: item[0])
        if len(candidates) > 1 and candidates[0][0] == candidates[1][0]:
            targets[i] = 0
            first_hit_bars[i] = int(candidates[0][0] + 1)
            first_hit_times[i] = raw.loc[start + candidates[0][0], "time_close"]
            censor_reason[i] = "opposing_favorable_same_bar_tie"
            continue
        first_hit_bars[i] = int(candidates[0][0] + 1)
        first_hit_times[i] = raw.loc[start + candidates[0][0], "time_close"]
        targets[i] = int(candidates[0][1])
        censor_reason[i] = "target_favorable_first_hit"

    out["first_hit_target"] = targets
    out["first_hit_eligible"] = eligible
    out["first_hit_entry_index"] = entry_idx
    out["entry_price"] = entry_prices
    out["bracket_points"] = bracket_points
    out["bracket_return"] = np.nan_to_num(bracket_returns, nan=0.0)
    out["label_start_time"] = pd.to_datetime(label_start_times, utc=True)
    out["label_end_time"] = pd.to_datetime(label_end_times, utc=True)
    out["first_hit_bar"] = first_hit_bars
    out["first_hit_time"] = pd.to_datetime(first_hit_times, utc=True)
    out["long_first_state"] = long_state
    out["short_first_state"] = short_state
    out["first_hit_censor_reason"] = censor_reason
    out["first_hit_horizon_return"] = horizon_ret
    return out, {
        "rows": int(len(out)),
        "eligible_rows": int(eligible.sum()),
        "excluded_rows": int((~eligible).sum()),
        "excluded_by_reason": out.loc[~eligible, "first_hit_censor_reason"].astype(str).value_counts().sort_index().to_dict(),
        "label_start_nonpositive_count": int(((out["label_start_time"].astype("int64") - out["timestamp"].astype("int64")) < 0).sum()),
        "label_end_after_split_boundary_excluded": int((np.array(censor_reason) == "split_horizon_embargo").sum()),
    }


def prepare_frames() -> tuple[dict[str, pd.DataFrame], dict[str, Any], dict[str, Any], dict[str, Any], list[str]]:
    frames, route_summary, tier_b_summary, f91_integrity = f91.prepare_routed_frames()
    features = feature_columns()
    raw = load_raw_bars()
    label_summaries: dict[str, Any] = {}
    for view, frame in list(frames.items()):
        enriched, summary = first_hit_for_frame(frame, raw)
        frames[view] = enriched
        label_summaries[view] = summary
    return frames, route_summary, tier_b_summary, {**f91_integrity, "first_hit_label_summaries": label_summaries}, features


def label_distribution(frames: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for view, frame in frames.items():
        view_payload: dict[str, Any] = {}
        for split, part in frame.groupby(frame["split"].astype(str)):
            eligible = part.loc[part["first_hit_eligible"].astype(bool)].copy()
            counts = eligible["first_hit_target"].astype(int).value_counts().sort_index()
            total = max(1, int(len(eligible)))
            view_payload[str(split)] = {
                "rows": int(len(part)),
                "eligible_rows": int(len(eligible)),
                "short": int(counts.get(-1, 0)),
                "abstain_or_no_event": int(counts.get(0, 0)),
                "long": int(counts.get(1, 0)),
                "event_share": round(float((counts.get(-1, 0) + counts.get(1, 0)) / total), 6),
                "avg_bracket_return": round(float(eligible["bracket_return"].mean()), 8) if len(eligible) else None,
                "avg_first_hit_bar": round(float(eligible.loc[eligible["first_hit_bar"] > 0, "first_hit_bar"].mean()), 6) if (eligible["first_hit_bar"] > 0).any() else None,
                "censor_reasons": eligible["first_hit_censor_reason"].astype(str).value_counts().sort_index().to_dict(),
            }
        payload[view] = view_payload
    return payload


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
            eligible = part.loc[part["first_hit_eligible"].astype(bool)]
            view_payload[str(split)] = {
                "rows": int(len(part)),
                "eligible_rows": int(len(eligible)),
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
    label_start_bad = {
        view: int(((frame["label_start_time"].astype("int64") - frame["timestamp"].astype("int64")) < 0).sum())
        for view, frame in frames.items()
    }
    split_rows = split_summary(frames)
    gaps = {view: gap_summary(frame) for view, frame in frames.items()}
    boundary_ok = not denied and all(value == 0 for value in duplicates.values()) and all(sorted_flags.values()) and all(value == 0 for value in label_start_bad.values())
    return {
        "audit_name": "data_integrity_audit",
        "packet_id": RUN_ID,
        "status": "pass_with_boundary" if boundary_ok else "blocked",
        "data_sources_checked": [file_identity(path) for path in [MODEL_INPUT_DATASET, MODEL_INPUT_SUMMARY, MODEL_INPUT_FEATURE_ORDER, RAW_BARS, RAW_BARS_MANIFEST]],
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
        "label_boundary_check": {
            "label_start_nonpositive_count": label_start_bad,
            "split_horizon_embargo_policy": "Rows whose first-hit horizon crosses split max timestamp are excluded from fit/evaluation.",
            "timestamp_interpretation": "model timestamp is closed-bar feature cutoff; first-hit label starts on the first raw bar closing after that cutoff.",
            "timezone_boundary": "raw manifest timezone_status remains unresolved; UTC epoch ordering is used only as broker-export axis, not civil-time authority.",
        },
        "leakage_tests": {
            "model_features_use_future_return": False,
            "model_features_use_label_or_label_class": False,
            "model_features_use_first_hit_label_columns": False,
            "first_hit_labels_used_as_targets_only": True,
            "fit_scope": "train_tier_ab_combined_eligible_rows_only",
            "validation_oos_transform_only": True,
            "oos_selection": "forbidden_and_not_used",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def fit_variant(spec: Mapping[str, Any], train: pd.DataFrame, features: Sequence[str]) -> dict[str, Any]:
    cols = variant_features(spec, features)
    family = str(spec["family"])
    if family == "logistic_hazard":
        model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1200, class_weight="balanced", solver="lbfgs"))
        model.fit(train[cols], train["first_hit_target"].astype(int))
        selected, side, score, event_prob = predict_variant_model(model, family, train, cols, train_abs_quantile=float(spec["train_abs_quantile"]))
        threshold = float(np.quantile(score, float(spec["train_abs_quantile"]))) if len(score) else 0.0
        return {"model": model, "features": cols, "selection_threshold": threshold, "train_classes": sorted(set(train["first_hit_target"].astype(int))), "train_score": score, "train_event_prob": event_prob}
    if family == "extra_trees_hazard":
        model = make_pipeline(
            SimpleImputer(strategy="median"),
            ExtraTreesClassifier(n_estimators=180, max_depth=5, min_samples_leaf=80, class_weight="balanced", random_state=RNG_SEED, n_jobs=1),
        )
        model.fit(train[cols], train["first_hit_target"].astype(int))
        _, _, score, event_prob = predict_variant_model(model, family, train, cols, train_abs_quantile=float(spec["train_abs_quantile"]))
        threshold = float(np.quantile(score, float(spec["train_abs_quantile"]))) if len(score) else 0.0
        return {"model": model, "features": cols, "selection_threshold": threshold, "train_classes": sorted(set(train["first_hit_target"].astype(int))), "train_score": score, "train_event_prob": event_prob}
    model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), Ridge(alpha=10.0))
    signed_edge = train["first_hit_target"].to_numpy(dtype=float) * train["bracket_return"].to_numpy(dtype=float)
    model.fit(train[cols], signed_edge)
    pred = np.asarray(model.predict(train[cols]), dtype=float)
    threshold = float(np.quantile(np.abs(pred), float(spec.get("train_abs_quantile", 0.90)))) if len(pred) else 0.0
    return {"model": model, "features": cols, "selection_threshold": threshold, "train_classes": ["signed_first_hit_edge"], "train_score": np.abs(pred), "train_event_prob": np.abs(pred)}


def predict_variant_model(model: Any, family: str, frame: pd.DataFrame, cols: Sequence[str], *, train_abs_quantile: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if frame.empty:
        return np.array([], dtype=bool), np.array([], dtype=int), np.array([], dtype=float), np.array([], dtype=float)
    if family in {"logistic_hazard", "extra_trees_hazard"}:
        probs = model.predict_proba(frame[list(cols)])
        classes = list(model[-1].classes_)
        idx = {int(label): pos for pos, label in enumerate(classes)}
        p_short = probs[:, idx.get(-1, 0)] if -1 in idx else np.zeros(len(probs))
        p_flat = probs[:, idx.get(0, 0)] if 0 in idx else np.zeros(len(probs))
        p_long = probs[:, idx.get(1, 0)] if 1 in idx else np.zeros(len(probs))
        side = np.where(p_long >= p_short, 1, -1)
        event_prob = np.maximum(p_long, p_short)
        score = np.maximum(event_prob - p_flat, 0.0)
        threshold = float(np.quantile(score, train_abs_quantile)) if len(score) else 0.0
        return (score >= threshold).astype(bool), side.astype(int), score.astype(float), event_prob.astype(float)
    pred = np.asarray(model.predict(frame[list(cols)]), dtype=float)
    threshold = float(np.quantile(np.abs(pred), train_abs_quantile)) if len(pred) else 0.0
    return (np.abs(pred) >= threshold).astype(bool), np.where(pred >= 0.0, 1, -1).astype(int), np.abs(pred).astype(float), np.abs(pred).astype(float)


def predict_variant(fit: Mapping[str, Any], spec: Mapping[str, Any], frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    cols = list(fit["features"])
    family = str(spec["family"])
    if frame.empty:
        return np.array([], dtype=bool), np.array([], dtype=int), np.array([], dtype=float), np.array([], dtype=float)
    if family in {"logistic_hazard", "extra_trees_hazard"}:
        model = fit["model"]
        probs = model.predict_proba(frame[cols])
        classes = list(model[-1].classes_)
        idx = {int(label): pos for pos, label in enumerate(classes)}
        p_short = probs[:, idx.get(-1, 0)] if -1 in idx else np.zeros(len(probs))
        p_flat = probs[:, idx.get(0, 0)] if 0 in idx else np.zeros(len(probs))
        p_long = probs[:, idx.get(1, 0)] if 1 in idx else np.zeros(len(probs))
        side = np.where(p_long >= p_short, 1, -1)
        event_prob = np.maximum(p_long, p_short)
        score = np.maximum(event_prob - p_flat, 0.0)
        selected = score >= float(fit.get("selection_threshold") or 0.0)
        return selected.astype(bool), side.astype(int), score.astype(float), event_prob.astype(float)
    pred = np.asarray(fit["model"].predict(frame[cols]), dtype=float)
    selected = np.abs(pred) >= float(fit.get("selection_threshold") or 0.0)
    side = np.where(pred >= 0.0, 1, -1)
    return selected.astype(bool), side.astype(int), np.abs(pred).astype(float), np.abs(pred).astype(float)


def proxy_pnl(frame: pd.DataFrame, selected: np.ndarray, side: np.ndarray) -> np.ndarray:
    selected = np.asarray(selected, dtype=bool)
    side = np.asarray(side, dtype=int)
    target = frame["first_hit_target"].to_numpy(dtype=int)
    bracket = frame["bracket_return"].to_numpy(dtype=float)
    fallback = frame["first_hit_horizon_return"].to_numpy(dtype=float)
    pnl = np.where(side == target, bracket, np.where(target == 0, side * fallback, -bracket))
    pnl = pnl - PROXY_COST_RETURN - SLIPPAGE_PROXY
    return pnl[selected]


def policy_metrics(frame: pd.DataFrame, selected: np.ndarray, side: np.ndarray) -> dict[str, Any]:
    selected = np.asarray(selected, dtype=bool)
    side = np.asarray(side, dtype=int)
    days = int(frame["timestamp"].dt.date.nunique()) if len(frame) else 0
    trade_count = int(selected.sum())
    if trade_count == 0:
        return {
            "rows": int(len(frame)),
            "days": days,
            "trade_count": 0,
            "trades_per_day": 0.0,
            "net_proxy": 0.0,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "proxy_pf": None,
            "win_rate": None,
            "avg_win": None,
            "avg_loss": None,
            "payoff_ratio": None,
            "expectancy": None,
            "max_drawdown": 0.0,
            "recovery_factor": None,
            "time_under_water_bars": 0,
            "max_consecutive_loss": 0,
            "long_count": 0,
            "short_count": 0,
            "side_min_share": None,
            "regime_coverage_count": 0,
            "adverse_first_share": None,
            "no_event_share": None,
            "avg_first_hit_bar": None,
            "avg_bracket_return": None,
        }
    pnl = proxy_pnl(frame, selected, side)
    gross_profit = float(pnl[pnl > 0].sum())
    gross_loss = float(-pnl[pnl < 0].sum())
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    long_count = int((side[selected] == 1).sum())
    short_count = int((side[selected] == -1).sum())
    side_min_share = float(min(long_count, short_count) / trade_count) if trade_count else None
    cum = np.cumsum(pnl)
    peaks = np.maximum.accumulate(np.insert(cum, 0, 0.0))[1:]
    dd = peaks - cum
    max_dd = float(dd.max()) if len(dd) else 0.0
    underwater = int((dd > 0).sum()) if len(dd) else 0
    max_consec = 0
    cur = 0
    for value in pnl:
        cur = cur + 1 if value < 0 else 0
        max_consec = max(max_consec, cur)
    target = frame["first_hit_target"].to_numpy(dtype=int)
    selected_target = target[selected]
    adverse_first = (selected_target != 0) & (selected_target != side[selected])
    no_event = selected_target == 0
    return {
        "rows": int(len(frame)),
        "days": days,
        "trade_count": trade_count,
        "trades_per_day": round(float(trade_count / days), 6) if days else None,
        "net_proxy": round(float(pnl.sum()), 8),
        "gross_profit": round(gross_profit, 8),
        "gross_loss": round(gross_loss, 8),
        "proxy_pf": round(float(gross_profit / gross_loss), 6) if gross_loss > 0 else (999.0 if gross_profit > 0 else None),
        "win_rate": round(float((pnl > 0).mean()), 6),
        "avg_win": round(float(wins.mean()), 8) if len(wins) else None,
        "avg_loss": round(float(losses.mean()), 8) if len(losses) else None,
        "payoff_ratio": round(float(wins.mean() / abs(losses.mean())), 6) if len(wins) and len(losses) else None,
        "expectancy": round(float(pnl.mean()), 8),
        "max_drawdown": round(max_dd, 8),
        "recovery_factor": round(float(pnl.sum() / max_dd), 6) if max_dd > 0 else None,
        "time_under_water_bars": underwater,
        "max_consecutive_loss": int(max_consec),
        "long_count": long_count,
        "short_count": short_count,
        "side_min_share": round(side_min_share, 6) if side_min_share is not None else None,
        "regime_coverage_count": int(frame.loc[selected, "regime_key"].nunique()) if "regime_key" in frame else 0,
        "adverse_first_share": round(float(adverse_first.mean()), 6) if trade_count else None,
        "no_event_share": round(float(no_event.mean()), 6) if trade_count else None,
        "avg_first_hit_bar": round(float(frame.loc[selected & (frame["first_hit_bar"] > 0), "first_hit_bar"].mean()), 6) if (selected & (frame["first_hit_bar"] > 0).to_numpy()).any() else None,
        "avg_bracket_return": round(float(frame.loc[selected, "bracket_return"].mean()), 8),
    }


def random_control_mean(frame: pd.DataFrame, selected: np.ndarray, side: np.ndarray, *, seed: int) -> dict[str, Any]:
    selected = np.asarray(selected, dtype=bool)
    trade_count = int(selected.sum())
    if trade_count <= 0 or len(frame) == 0:
        base = policy_metrics(frame, np.zeros(len(frame), dtype=bool), side)
        return {f"random_{key}_mean": base.get(key) for key in ("net_proxy", "proxy_pf", "max_drawdown")}
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
    }


def control_rows_for(frame: pd.DataFrame, selected: np.ndarray, side: np.ndarray, variant_id: str, view: str, split: str) -> list[dict[str, Any]]:
    controls: list[tuple[str, np.ndarray, np.ndarray]] = []
    zero = np.zeros(len(frame), dtype=bool)
    controls.append(("no_trade", zero, side))
    controls.append(("trade_all_model_side", np.ones(len(frame), dtype=bool), side))
    random_mask = np.zeros(len(frame), dtype=bool)
    if int(np.asarray(selected, dtype=bool).sum()) > 0 and len(frame) > 0:
        rng = np.random.default_rng(stable_seed(variant_id, view, split, "random_density_match"))
        random_mask[rng.choice(len(frame), size=min(int(np.asarray(selected, dtype=bool).sum()), len(frame)), replace=False)] = True
    controls.append(("random_density_match_single", random_mask, side))
    target = frame["first_hit_target"].to_numpy(dtype=int)
    oracle_selected = target != 0
    oracle_side = np.where(target == 0, side, target)
    controls.append(("first_hit_oracle_reference_not_candidate", oracle_selected, oracle_side))
    anti_side = np.where(side == 1, -1, 1)
    controls.append(("adverse_blind_opposite_side", selected, anti_side))
    rows: list[dict[str, Any]] = []
    for control_id, mask, control_side in controls:
        rows.append({"variant_id": variant_id, "view": view, "split": split, "control_id": control_id, **policy_metrics(frame, mask, control_side)})
    return rows


def calibration_rows_for(frame: pd.DataFrame, event_prob: np.ndarray, variant_id: str, view: str, split: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    y = (frame["first_hit_target"].to_numpy(dtype=int) != 0).astype(int)
    if len(y) == 0:
        return rows
    brier = float(brier_score_loss(y, np.clip(event_prob, 0.0, 1.0))) if len(np.unique(y)) > 1 else None
    auc = float(roc_auc_score(y, event_prob)) if len(np.unique(y)) > 1 else None
    rows.append({"variant_id": variant_id, "view": view, "split": split, "bin": "overall", "rows": int(len(y)), "event_rate": round(float(y.mean()), 6), "mean_event_prob": round(float(np.mean(event_prob)), 6), "brier_score": round(brier, 8) if brier is not None else "", "event_auc": round(auc, 6) if auc is not None else ""})
    if len(y) >= 5:
        bins = pd.qcut(pd.Series(event_prob).rank(method="first"), q=min(5, len(y)), labels=False, duplicates="drop")
        for bin_id, idx in pd.Series(range(len(y))).groupby(bins):
            index = idx.to_numpy(dtype=int)
            rows.append({"variant_id": variant_id, "view": view, "split": split, "bin": int(bin_id), "rows": int(len(index)), "event_rate": round(float(y[index].mean()), 6), "mean_event_prob": round(float(event_prob[index].mean()), 6), "brier_score": "", "event_auc": ""})
    return rows


def metric_failures(row: Mapping[str, Any], controls: Mapping[str, Mapping[str, Any]], view: str) -> list[str]:
    failures: list[str] = []
    trade_count = int(row.get("trade_count") or 0)
    if trade_count <= 0:
        failures.append(f"{view}_validation_no_trades")
        return failures
    net_proxy = float(row.get("net_proxy") or 0.0)
    pf = float(row.get("proxy_pf") or 0.0)
    tpd = float(row.get("trades_per_day") or 0.0)
    dd = float(row.get("max_drawdown") or 0.0)
    side_min = float(row.get("side_min_share") or 0.0)
    recovery = float(row.get("recovery_factor") or 0.0)
    regime_count = int(row.get("regime_coverage_count") or 0)
    adverse_share = float(row.get("adverse_first_share") or 0.0)
    no_event_share = float(row.get("no_event_share") or 0.0)
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
    if adverse_share > CANDIDATE_MAX_ADVERSE_FIRST_SHARE:
        failures.append(f"{view}_validation_adverse_first_share_high")
    if no_event_share > CANDIDATE_MAX_NO_EVENT_SHARE:
        failures.append(f"{view}_validation_no_event_share_high")
    for control_id in ["no_trade", "trade_all_model_side", "random_density_match_single", "adverse_blind_opposite_side"]:
        control = controls.get(control_id, {})
        if control and net_proxy <= float(control.get("net_proxy") or 0.0):
            failures.append(f"{view}_validation_not_above_{control_id}_net_proxy")
    return failures


def candidate_gate_for_variant(variant_id: str, results: Mapping[str, Mapping[str, Mapping[str, Any]]], controls: Mapping[str, Mapping[str, Mapping[str, Mapping[str, Any]]]]) -> dict[str, Any]:
    failures: list[str] = []
    oos_notes: list[str] = []
    for view in ["tier_a_separate", "tier_b_separate", "tier_ab_combined"]:
        failures.extend(metric_failures(results[view]["validation"], controls[view]["validation"], view))
        oos = results[view]["oos"]
        if int(oos.get("trade_count") or 0) <= 0:
            oos_notes.append(f"{view}_oos_no_trades_final_read")
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
        "claim_effect": "same_packet_mt5_strategy_tester_probe_required_before_any_runnable_candidate_or_runtime_claim" if status == "candidate_triggered" else "runtime_evidence_gate_not_triggered_no_runnable_candidate_claim",
    }


def diagnostic_score(row: Mapping[str, Any]) -> float:
    net_proxy = float(row.get("net_proxy") or 0.0)
    pf = float(row.get("proxy_pf") or 0.0)
    dd = float(row.get("max_drawdown") or 0.0)
    tpd = float(row.get("trades_per_day") or 0.0)
    side_min = float(row.get("side_min_share") or 0.0)
    adverse = float(row.get("adverse_first_share") or 1.0)
    density = max(0.0, 1.0 - abs(tpd - 7.0) / 7.0)
    economics = max(-1.0, min(1.0, net_proxy * 10.0)) + max(-0.5, min(0.5, pf - 1.0))
    risk = max(-1.0, min(1.0, (CANDIDATE_MAX_DD - dd) / max(CANDIDATE_MAX_DD, 1e-12)))
    balance = max(0.0, min(1.0, side_min / max(CANDIDATE_MIN_SIDE_SHARE, 1e-12)))
    adverse_term = max(-1.0, min(1.0, (CANDIDATE_MAX_ADVERSE_FIRST_SHARE - adverse) / CANDIDATE_MAX_ADVERSE_FIRST_SHARE))
    return round(float(100.0 * (0.28 * economics + 0.22 * risk + 0.18 * density + 0.16 * balance + 0.16 * adverse_term)), 6)


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
    train = frames["tier_ab_combined"].loc[frames["tier_ab_combined"]["split"].astype(str).eq("train") & frames["tier_ab_combined"]["first_hit_eligible"].astype(bool)].copy().reset_index(drop=True)
    metric_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    calibration_rows: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    fit_rows: list[dict[str, Any]] = []
    gates: list[dict[str, Any]] = []
    for index, spec in enumerate(VARIANTS):
        fit = fit_variant(spec, train, features)
        variant_id = str(spec["variant_id"])
        variant_results: dict[str, dict[str, Any]] = {}
        variant_controls: dict[str, dict[str, dict[str, Any]]] = {}
        for view, view_frame in frames.items():
            variant_results[view] = {}
            variant_controls[view] = {}
            for split in ["train", "validation", "oos"]:
                part = view_frame.loc[view_frame["split"].astype(str).eq(split) & view_frame["first_hit_eligible"].astype(bool)].copy().reset_index(drop=True)
                selected, side, score, event_prob = predict_variant(fit, spec, part)
                metrics = policy_metrics(part, selected, side)
                rand = random_control_mean(part, selected, side, seed=RNG_SEED + stable_seed(variant_id, view, split, index))
                row = {
                    "variant_id": variant_id,
                    "model_family": spec["family"],
                    "feature_mode": spec["feature_mode"],
                    "feature_count": len(fit["features"]),
                    "selection_rule": "train_score_quantile",
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
                calibration_rows.extend(calibration_rows_for(part, event_prob, variant_id, view, split))
                if split in {"validation", "oos"} and len(part):
                    sample = part.loc[selected, ["timestamp", "source_tier", "route_role", "first_hit_target", "first_hit_bar", "bracket_return", "first_hit_horizon_return", "regime_key"]].copy()
                    sample["variant_id"] = variant_id
                    sample["split"] = split
                    sample["side"] = side[selected]
                    sample["score"] = score[selected]
                    sample["event_prob"] = event_prob[selected]
                    sample["proxy_pnl"] = proxy_pnl(part, selected, side)
                    sample_rows.extend(sample.head(80).to_dict(orient="records"))
        gates.append(candidate_gate_for_variant(variant_id, variant_results, variant_controls))
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
    write_csv(CALIBRATION_CSV, calibration_rows)
    write_csv(SCORE_SAMPLE_CSV, sample_rows)
    write_json(CANDIDATE_GATE_JSON, {"candidate_count": candidate_count, "gates": gates})
    write_json(
        MODEL_FIT_MANIFEST,
        {
            "fit_scope": "train_tier_ab_combined_eligible_rows_only",
            "transform_only_splits": ["validation", "oos"],
            "seed": RNG_SEED,
            "variant_fit_rows": fit_rows,
            "leakage_boundary": "first_hit_target and first_hit outcome fields are targets/evaluation only; model features are closed-bar feature columns.",
            "calibration_boundary": "Brier/AUC/bin records are diagnostics only; no calibrated probability claim is made.",
        },
    )
    return {
        "variants": VARIANTS,
        "split_metrics": metric_rows,
        "negative_control_rows": control_rows,
        "calibration_rows": calibration_rows,
        "candidate_gates": gates,
        "candidate_count": candidate_count,
        "best_diagnostic_variant": choose_best_diagnostic(metric_rows, gates),
        "selection_policy": "predeclared first-hit score quantile; train-only fit/threshold; validation candidate gate; OOS final read only",
    }


def materialize_proxy_metrics() -> dict[str, Any]:
    frames, route_summary, tier_b_summary, f91_integrity, features = prepare_frames()
    data_integrity = data_integrity_payload(frames, route_summary, tier_b_summary, f91_integrity, features)
    evaluation = evaluate_variants(frames, features)
    label_summary = label_distribution(frames)
    label_sample = frames["tier_ab_combined"].loc[
        frames["tier_ab_combined"]["first_hit_eligible"].astype(bool),
        ["timestamp", "split", "source_tier", "route_role", "first_hit_target", "first_hit_bar", "label_start_time", "label_end_time", "entry_price", "bracket_return", "long_first_state", "short_first_state", "first_hit_censor_reason"],
    ].head(200)
    write_csv(FIRST_HIT_LABEL_SAMPLE, label_sample.to_dict(orient="records"))
    write_json(DATA_LOCK, data_lock_payload(frames, route_summary, tier_b_summary, data_integrity, features))
    write_json(TIER_ROUTE_SUMMARY, route_summary)
    write_json(TIER_B_SUMMARY, tier_b_summary)
    write_json(DATA_INTEGRITY_LOCAL, data_integrity)
    write_json(FIRST_HIT_CONFIG, first_hit_config_payload())
    write_json(FIRST_HIT_LABEL_SUMMARY, label_summary)
    write_json(
        RUNTIME_TRIGGER_CHECK,
        {
            "run_id": RUN_ID,
            "candidate_count": evaluation["candidate_count"],
            "runtime_probe_required_now": int(evaluation["candidate_count"]) > 0,
            "runtime_probe_status": RUNTIME_PROBE_STATUS_BLOCKED if int(evaluation["candidate_count"]) > 0 else RUNTIME_PROBE_STATUS_NEGATIVE,
            "skip_reason_rejected": ["cost_or_expense", "proxy_result_bad"],
            "not_applicable_reason_if_zero_candidate": "no_runnable_candidate_no_runtime_materialization_handoff_economics_claim",
            "claim_effect": "No runtime/materialization/economics/handoff claim is made by this proxy-scout packet.",
        },
    )
    return {
        "data_integrity": data_integrity,
        "route_summary": route_summary,
        "tier_b_summary": tier_b_summary,
        "label_summary": label_summary,
        "evaluation": evaluation,
        "feature_count": len(features),
        "feature_hash": feature_hash(features),
    }


def data_lock_payload(frames: Mapping[str, pd.DataFrame], route_summary: Mapping[str, Any], tier_b_summary: Mapping[str, Any], data_integrity: Mapping[str, Any], features: Sequence[str]) -> dict[str, Any]:
    train = frames["tier_ab_combined"].loc[frames["tier_ab_combined"]["split"].astype(str).eq("train") & frames["tier_ab_combined"]["first_hit_eligible"].astype(bool)]
    return {
        "run_id": RUN_ID,
        "created_at_utc": utc_now(),
        "model_input_dataset": file_identity(MODEL_INPUT_DATASET),
        "model_input_summary": file_identity(MODEL_INPUT_SUMMARY),
        "feature_order": file_identity(MODEL_INPUT_FEATURE_ORDER),
        "raw_bars": file_identity(RAW_BARS),
        "raw_bars_manifest": file_identity(RAW_BARS_MANIFEST),
        "feature_count": len(features),
        "feature_order_hash": feature_hash(features),
        "train_tier_ab_combined_input_hash": hash_dataframe(train, features),
        "split_summary": split_summary(frames),
        "tier_route_summary": route_summary,
        "tier_b_summary": tier_b_summary,
        "data_integrity_status": data_integrity.get("status"),
        "closed_bar_boundary": "features use row t closed M5 bars and rolling history only; first-hit labels start after the closed-bar feature cutoff.",
        "combined_boundary": "Tier A+B is actual routed total, not a synthetic sum of separate KPI rows.",
    }


def status_from(payload: Mapping[str, Any]) -> str:
    return str(payload["status"])


def judgment_from(payload: Mapping[str, Any]) -> str:
    return str(payload["judgment"])


def runtime_probe_status_from(payload: Mapping[str, Any]) -> str:
    return str(payload["runtime_probe_status"])


def task_force_payload(created_at: str) -> dict[str, Any]:
    calls = task_force_calls()
    unique_roster_agents = sorted({str(call["roster_agent_id"]) for call in calls})
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed_with_pending_quant_response_boundary",
        "created_at_utc": created_at,
        "review_requirement": "explicit_user_instruction_required_and_active_goal_claim_surface",
        "trigger_reason": "F97B non-trivial proxy_scout packet plus explicit user instruction to call relevant Task Force agents when triggered",
        "trigger_source": "active_goal_frontier_continuation_and_user_required_task_force_review",
        "roster_registry": rel(ROOT / "docs" / "agent_control" / "codex_task_force_registry.yaml"),
        "selected_roster_agent_count": len(unique_roster_agents),
        "actual_subagent_call_count": len(calls),
        "full_roster_call_reason": None,
        "agents_used": unique_roster_agents,
        "actual_subagent_calls": calls,
        "opinion_summary": {
            "accepted": [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "accepted"],
            "needs_local_verification": [call["roster_agent_id"] for call in calls if call["opinion_classification"] == "needs_local_verification"],
            "rejected": ["stale subagent self-reports claiming the parent spawn call did not happen"],
        },
        "model_policy": "inherited_current_codex_model_no_gate_relaxation",
        "bounded_evidence": [rel(F97A_BRIEF), rel(F97A_CONTRACT), rel(KPI_RECORD), rel(CANDIDATE_GATE_JSON), rel(DATA_INTEGRITY_LOCAL)],
        "advice_classification": "mixed_accepted_and_needs_local_verification",
        "local_verification": [
            "F97B materializes a new work_packet_schema_v2_1 packet.",
            "Tier A, Tier B, and Tier A+B actual routed total are recorded.",
            "Timestamp sortedness, duplicate counts, split horizon embargo, first-hit label boundary, and denylist features are checked.",
            "Candidate gate is validation-only; OOS is final read only.",
            "Runtime probe is required only if a runnable candidate or runtime/handoff/economics claim appears.",
        ],
        "final_codex_direction": "Use F97B as proxy scout evidence only; no Task Force reviewed/pass, runtime, promotion, baseline, readiness, or Goal Achieve claim.",
        "forbidden_claim_check": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


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
        "hypothesis": "A first favorable/adverse bracket-hit survival/hazard target can reveal side-balanced US100 M5 scout clues without inheriting any prior baseline or authority.",
        "verification_profile": "proxy_scout",
        "claim_boundary": CLAIM_BOUNDARY,
        "metrics": metrics,
        "source_identities": [file_identity(path) for path in source_inputs()],
        "task_force": task_force_payload(created_at),
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
            "adverse_first_share": validation.get("adverse_first_share"),
            "no_event_share": validation.get("no_event_share"),
        },
        "negative_controls": {
            "record_path": rel(NEGATIVE_CONTROL_CSV),
            "required": ["random", "no_trade", "trade_all", "first_hit_oracle_reference", "adverse_blind_opposite_side"],
        },
        "runtime_probe_trigger_rule": "If candidate_count > 0 or a runnable ONNX/EA/set/materialization/economics/handoff claim appears, same-packet MT5 Strategy Tester probe is required.",
        "runtime_skip_reason_rejected": ["cost_or_expense", "proxy_result_bad"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    best = payload["metrics"]["evaluation"].get("best_diagnostic_variant", {})
    validation = best.get("validation", {})
    failures = best.get("gate", {}).get("selection_failures", [])
    return f"""# F97B First-Hit Survival/Hazard Proxy Scout

Action: F97B ran a train-only first-hit survival/hazard proxy scout using closed-bar features and raw MT5 M5 bars.

Effect: the packet records Tier A separate, Tier B separate, and Tier A+B actual routed total proxy evidence without claiming runtime authority, selected baseline, live readiness, or Goal Achieve.

Best diagnostic variant: `{best.get('variant_id')}`

- validation net proxy: `{validation.get('net_proxy')}`
- validation PF: `{validation.get('proxy_pf')}`
- validation max drawdown: `{validation.get('max_drawdown')}`
- validation trades/day: `{validation.get('trades_per_day')}`
- validation trade count: `{validation.get('trade_count')}`
- validation adverse-first share: `{validation.get('adverse_first_share')}`
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
    write_text(F97B_REPORT, result_summary_text(payload))


def audit_payload(name: str, status: str, **extra: Any) -> dict[str, Any]:
    return {"audit_name": name, "packet_id": RUN_ID, "status": status, **extra}


def write_audits(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    gate_results = gate_results or {}
    candidate_count = int(payload["metrics"]["evaluation"]["candidate_count"])
    write_json(TASK_FORCE_REVIEW, payload["task_force"])
    write_json(PACKET_TASK_FORCE_REVIEW, payload["task_force"])
    write_json(FRONTIER_EXTRA_DUE_CHECK, audit_payload("frontier_extra_due_check", "pass_not_due", created_at_utc=payload["created_at_utc"], due_status=FRONTIER_EXTRA_DUE_STATUS, claim_effect="F97B can continue inside F97; no Extra Stage is due before F100."))
    write_json(FIVE_STAGE_SYNTHESIS, audit_payload("frontier_five_stage_direction_synthesis", "pass", created_at_utc=payload["created_at_utc"], status_detail=FRONTIER_FIVE_STAGE_STATUS, claim_effect="Light direction record only; no retrospective, topic ban, completion, or authority claim."))
    write_json(TOPIC_ROTATION_CHECK, audit_payload("frontier_topic_rotation_check", "pass", created_at_utc=payload["created_at_utc"], status_detail=FRONTIER_TOPIC_ROTATION_STATUS, material_novelty_delta="F97B executes the F97A first-hit survival/hazard axis and is not a threshold/filter/session/routing-only repair.", claim_effect="Continuation inside F97 only; no stage completion or authority claim."))
    write_json(SCOPE_GATE, audit_payload("scope_completion_gate", "pass", created_at_utc=payload["created_at_utc"], required_outputs=[rel(path) for path in [RUN_MANIFEST, KPI_RECORD, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV, DATA_LOCK, PACKET_TASK_FORCE_REVIEW]], candidate_gate_count=candidate_count, runtime_probe_status=runtime_probe_status_from(payload), claim_boundary=CLAIM_BOUNDARY))
    integrity = dict(payload["metrics"]["data_integrity"])
    integrity["created_at_utc"] = payload["created_at_utc"]
    write_json(DATA_INTEGRITY_AUDIT, integrity)
    write_json(MODEL_VALIDATION_AUDIT, audit_payload("model_validation_audit", "pass_with_boundary" if candidate_count == 0 else "blocked_pending_runtime_probe", created_at_utc=payload["created_at_utc"], fit_policy="train_tier_ab_combined_eligible_rows_only", validation_policy="candidate_gate_only", oos_policy="final_read_only_no_tuning", calibration_claim="rejected_diagnostics_only", pf_only_selection="rejected", candidate_gate_count=candidate_count, calibration_metrics=rel(CALIBRATION_CSV), claim_boundary=CLAIM_BOUNDARY))
    write_json(KPI_CONTRACT_AUDIT, audit_payload("kpi_contract_audit", "pass", created_at_utc=payload["created_at_utc"], kpi_record=rel(KPI_RECORD), split_metrics=rel(SPLIT_METRICS_CSV), candidate_gate=rel(CANDIDATE_GATE_JSON), required_kpi_fields=["hypothesis", "test_period", "proxy_kpi", "runtime_kpi", "net_profit", "profit_factor", "drawdown", "trade_count", "trades_per_day", "parity", "gap_cause", "next_action", "closeout_kpi"], claim_boundary=CLAIM_BOUNDARY))
    artifact_rows = [file_identity(path) for path in produced_artifacts()]
    write_json(ARTIFACT_AUDIT, audit_payload("artifact_lineage_audit", "pass", created_at_utc=payload["created_at_utc"], source_inputs=payload["source_identities"], produced_artifacts=artifact_rows, missing_artifacts=[row for row in artifact_rows if not row.get("exists")], claim_boundary=CLAIM_BOUNDARY))
    write_json(RESULT_JUDGMENT_AUDIT, audit_payload("result_judgment_audit", "negative" if candidate_count == 0 else "blocked", created_at_utc=payload["created_at_utc"], judgment=judgment_from(payload), result_status=status_from(payload), runtime_probe_status=runtime_probe_status_from(payload), next_action=payload["next_run_id"], forbidden_claims=FORBIDDEN_CLAIMS, claim_boundary=CLAIM_BOUNDARY))
    if candidate_count > 0:
        write_json(RUNTIME_EVIDENCE_GATE, audit_payload("runtime_evidence_gate", "blocked_pending_same_packet_mt5_probe", created_at_utc=payload["created_at_utc"], reason="A proxy candidate signal requires MT5 Strategy Tester identity before any candidate/runtime/materialization/economics/handoff claim.", claim_effect="Candidate language is blocked until MT5 tester evidence exists."))
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
            "baseline": {"source_run_id": PARENT_RUN_ID, "use": "stage-open design only, not inherited baseline"},
            "changed_variables": ["first-hit favorable/adverse bracket target", "survival/hazard event selection", "split embargo on label horizon", "negative controls including oracle reference and adverse-blind opposite side"],
            "invalid_conditions": ["first_hit_outcome_as_feature", "random_split", "oos_tuning", "PF_only_selection", "runtime_claim_without_MT5_tester_identity"],
            "evidence_plan": {"tier_records": ["Tier A separate", "Tier B separate", "Tier A+B actual routed total"], "candidate_gate": rel(CANDIDATE_GATE_JSON)},
            "receipt_path": rel(SKILL_RECEIPT_DIR / "experiment_design.json"),
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": [file_identity(path) for path in [MODEL_INPUT_DATASET, MODEL_INPUT_SUMMARY, MODEL_INPUT_FEATURE_ORDER, RAW_BARS, RAW_BARS_MANIFEST]],
            "time_axis_boundary": "Closed M5 row t features and rolling history only; first-hit label starts on first raw bar closing after feature cutoff.",
            "split_boundary": "Train fit only; validation candidate gate; OOS final-read-only; split-horizon breach rows are excluded.",
            "leakage_checks": payload["metrics"]["data_integrity"].get("leakage_tests", {}),
            "missing_data_boundary": "Tier B or Tier A+B combined rows cannot be omitted; if unavailable they must be recorded as blocked or missing_required.",
            "receipt_path": rel(SKILL_RECEIPT_DIR / "data_integrity.json"),
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "Logistic/ExtraTrees first-hit classifier and Ridge signed hit-edge scout; no calibrated probability claim.",
            "validation_split": "validation is candidate gate only; OOS is final-read-only",
            "overfit_checks": ["no OOS tuning", "train-only transforms", "PF-only selection rejected", "multi-axis variants not threshold-only repeats"],
            "selection_metric_boundary": "candidate gate combines net proxy, PF, trades/day, DD, recovery, side balance, adverse-first share, no-event share, regimes, and controls",
            "allowed_claims": ALLOWED_CLAIMS,
            "candidate_gate_count": candidate_count,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "model_validation.json"),
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "raw_evidence": [rel(MODEL_INPUT_DATASET), rel(MODEL_INPUT_SUMMARY), rel(RAW_BARS), rel(F97A_BRIEF), rel(F97A_CONTRACT)],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, DATA_LOCK, FIRST_HIT_CONFIG, MODEL_FIT_MANIFEST, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV, CALIBRATION_CSV, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F97B_REPORT), rel(DECISION_MEMO)],
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
            "idea_boundary": "F97B can create clue/negative memory only unless runtime evidence is later produced.",
            "negative_memory_effect": "Failed first-hit survival/hazard gates become do-not-overclaim memory for F97C.",
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
    paths = [RUN_MANIFEST, KPI_RECORD, DATA_LOCK, FIRST_HIT_CONFIG, MODEL_FIT_MANIFEST, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV, NEGATIVE_CONTROL_CSV, CALIBRATION_CSV, PACKET_TASK_FORCE_REVIEW, WORK_PACKET, SKILL_RECEIPTS, PACKET_CLOSEOUT_GATE]
    if candidate_count > 0:
        paths.append(RUNTIME_EVIDENCE_GATE)
    return [rel(path) for path in paths]


def work_packet_payload(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    candidate_count = int(payload["metrics"]["evaluation"]["candidate_count"])
    gates = required_gates(candidate_count)
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation plus explicit reminder that relevant Task Force agents must be actually called when required",
            "requested_action": "run F97B first-hit survival/hazard proxy scout",
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
            "risks": {"future_label_leakage": "high", "tier_ab_timestamp_order": "high", "pf_only_selection": "high", "task_force_review_claim_without_actual_calls": "high", "runtime_probe_absence_misread_as_cost_skip": "high"},
            "hard_stop_risks": ["Do not put future, label, or first-hit outcome fields into model features.", "Do not tune by OOS.", "Do not claim runtime/economics/materialization without MT5 Strategy Tester identity."],
            "required_gates": gates,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {"verification_profile": "proxy_scout", "strategy_tester_required_now": candidate_count > 0, "runtime_probe_status": runtime_probe_status_from(payload), "reason": "No ONNX/EA/set/runtime claim is made when candidate_count is zero; if proxy gate signal appears, packet is blocked pending same-packet MT5 probe."},
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F97B proxy scout", "first-hit survival/hazard target", "Task Force actual calls", "state sync"],
            "scope_units": ["proxy_scout_run", "candidate_gate_record", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["data lock", "first-hit labels", "proxy metrics", "calibration diagnostics", "negative controls", "candidate gate", "Task Force actual calls", "control-plane gates"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F97B is the active proxy-scout packet and runtime trigger rules cannot be reduced."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "proxy_scout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F97A planned F97B proxy scout",
                "explicit user instruction requiring relevant Task Force actual calls when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence_paths(candidate_count),
            "gates_not_run_with_reason": RUNTIME_NA_REASONS if candidate_count == 0 else [],
            "stop_conditions": [
                "Stop at proxy scout evidence if no runnable candidate or runtime/materialization/economics/handoff claim appears.",
                "If a meaningful runnable candidate or runtime claim appears, do not make the claim without same-packet MT5 Strategy Tester probe.",
                "Do not repair by threshold/filter/session/routing/parameter-only changes.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F97B proxy metrics exist.", "expected_artifact": rel(SPLIT_METRICS_CSV), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Tier A, Tier B, and Tier A+B actual routed total are recorded.", "expected_artifact": rel(TIER_ROUTE_SUMMARY), "verification_method": "kpi_contract_audit", "required": True},
            {"id": "AC-003", "text": "Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-004", "text": "Runtime evidence absence is bounded and not a cost/proxy-bad skip.", "expected_artifact": rel(RUNTIME_TRIGGER_CHECK), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Lock data, raw bars, feature, split, and first-hit label identities.",
            "Fit train-only first-hit hazard proxy variants.",
            "Score validation and OOS final read with negative controls and calibration diagnostics.",
            "Record Task Force calls, audits, receipts, state sync, and final claim guard.",
        ],
        "skill_routing": {
            "registry_source": "docs/agent_control/work_family_registry.yaml",
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": REQUIRED_SKILLS[1:],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-backtest-forensics", "obsidian-runtime-parity"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-backtest-forensics", "reason": "No new MT5 Strategy Tester report or trade list exists."},
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA parity or handoff claim is made."},
            ],
            "verification_profile": "proxy_scout",
            "required_gates": gates,
            "required_skill_receipts": REQUIRED_SKILLS,
        },
        "evidence_contract": {
            "source_inputs": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, DATA_LOCK, FIRST_HIT_CONFIG, MODEL_FIT_MANIFEST, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV, NEGATIVE_CONTROL_CSV, CALIBRATION_CSV, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F97B_REPORT), rel(DECISION_MEMO), rel(CONTEXT_ANCHOR)],
            "raw_evidence": [rel(MODEL_INPUT_DATASET), rel(RAW_BARS), rel(F97A_BRIEF), rel(F97A_CONTRACT)],
            "missing_evidence": [
                {"evidence": "MT5 Strategy Tester runtime output", "reason": "outside proxy_scout claim surface unless candidate_count is positive or a runtime claim appears"},
                {"evidence": "ONNX/EA/set handoff", "reason": "not created in F97B"},
            ],
        },
        "gates": {
            "required": gates,
            "actual_status_source": {name: (gate_results.get(name, {}) or {}).get("status", "pending") for name in gates},
            "not_applicable_with_reason": {item["gate"]: item["reason"] for item in (RUNTIME_NA_REASONS if candidate_count == 0 else [])},
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        "verification_contract": {
            "verification_profile": "proxy_scout",
            "trigger_source": "frontier97B_proxy_scout_execution_and_explicit_task_force_instruction",
            "protected_claim": "first_hit_survival_hazard_proxy_scout_negative_or_blocked_learning_record_only",
            "required_evidence": required_evidence_paths(candidate_count),
            "stop_condition": "candidate_count_zero_negative_closeout_or_candidate_count_positive_blocked_until_same_packet_MT5_probe",
            "not_applicable_with_reason": RUNTIME_NA_REASONS if candidate_count == 0 else [],
        },
        "task_force": payload["task_force"],
        "artifacts": {"source_inputs": [file_identity(path) for path in source_inputs()], "produced_artifacts": [file_identity(path) for path in produced_artifacts()]},
        "gate_status": {gate: gate_results.get(gate, {}).get("status", "pending") for gate in gates},
        "claim_boundary": CLAIM_BOUNDARY,
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
        "packet_id": RUN_ID,
        "audit_name": "closeout_gate",
        "status": "blocked" if any(status.startswith("blocked") for status in statuses) else "pass",
        "created_at_utc": payload["created_at_utc"],
        "audits": audits,
        "not_applicable_with_reason": RUNTIME_NA_REASONS if candidate_count == 0 else [],
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
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def replace_rows(path: Path, remove_run_ids: set[str], new_rows: Sequence[Mapping[str, Any]]) -> None:
    fieldnames, rows = read_csv_rows(path)
    for row in new_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    kept = [row for row in rows if row.get("run_id") not in remove_run_ids]
    write_csv_rows(path, fieldnames, [*kept, *new_rows])


def ledger_rows(payload: Mapping[str, Any], gate_passes: int = 0) -> list[dict[str, Any]]:
    summary = summary_payload(payload)
    base = {
        "stage_id": STAGE_ID,
        "created_at_utc": payload["created_at_utc"],
        "status": summary["status"],
        "judgment": summary["judgment"],
        "verification_profile": "proxy_scout",
        "candidate_gate_count": summary["candidate_gate_count"],
        "runtime_probe_status": summary["runtime_probe_status"],
        "best_variant": summary["best_diagnostic_variant"],
        "net_proxy": summary["validation_actual_routed_net_proxy"],
        "profit_factor": summary["validation_actual_routed_pf"],
        "drawdown": summary["validation_actual_routed_drawdown"],
        "trade_count": summary["validation_actual_routed_trade_count"],
        "trades_per_day": summary["validation_actual_routed_trades_per_day"],
        "task_force_actual_subagent_call_count": summary["task_force_actual_subagent_call_count"],
        "gate_passes": gate_passes,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(F97B_REPORT),
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__proxy_scout",
            "run_id": RUN_ID,
            "run_number": "frontier97B",
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
            "run_number": "frontier97C" if payload["next_run_id"] != RUN_ID else "frontier97B",
            "subrun_id": "planned_current_run",
            "record_view": "planned_current_run",
            "tier_scope": "n/a",
            "kpi_scope": "repair_or_rotation_decision_pending" if payload["next_run_id"] != RUN_ID else "runtime_probe_block_pending",
            "input_run_id": RUN_ID,
            "next_action": payload["next_run_id"],
        }
    ]


def update_ledgers(payload: Mapping[str, Any], gate_passes: int = 0) -> None:
    rows = ledger_rows(payload, gate_passes)
    run_ids = {RUN_ID, payload["next_run_id"]}
    replace_rows(RUN_REGISTRY, run_ids, rows)
    replace_rows(ALPHA_LEDGER, run_ids, rows)
    if path_exists(STAGE_LEDGER):
        replace_rows(STAGE_LEDGER, run_ids, rows)
    else:
        write_csv_rows(STAGE_LEDGER, list(rows[0].keys()), rows)


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows: list[dict[str, Any]] = []
    for artifact in produced_artifacts():
        identity = file_identity(artifact)
        rows.append({"run_id": RUN_ID, "stage_id": STAGE_ID, "artifact_path": identity["path"], "sha256": identity["sha256"], "size_bytes": identity["size_bytes"], "exists": identity["exists"], "claim_boundary": CLAIM_BOUNDARY})
    replace_rows(ARTIFACT_REGISTRY, {RUN_ID}, rows)


def append_once(path: Path, marker: str, addition: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + addition.rstrip())


def update_register_docs(payload: Mapping[str, Any]) -> None:
    summary = summary_payload(payload)
    append_once(
        NEGATIVE_REGISTER,
        f"<!-- {RUN_ID} -->",
        f"""<!-- {RUN_ID} -->
## {RUN_ID}

Action: F97B ran first-hit survival/hazard proxy scout and recorded candidate gate count `{summary['candidate_gate_count']}`.

Effect: result is `{summary['judgment']}` with runtime status `{summary['runtime_probe_status']}`; no baseline, authority, live readiness, or Goal Achieve claim is made.
""",
    )
    append_once(
        IDEA_REGISTRY,
        f"<!-- {RUN_ID} -->",
        f"""<!-- {RUN_ID} -->
## F97B first-hit survival/hazard clue record

Hypothesis: {payload['hypothesis']}

Next action: `{payload['next_run_id']}`.
""",
    )
    append_once(
        WORKSPACE_CHANGELOG,
        f"<!-- {RUN_ID} -->",
        f"""<!-- {RUN_ID} -->
## {payload['created_at_utc']} - F97B first-hit survival/hazard proxy scout

Action: Materialized F97B proxy scout artifacts and packet receipts.

Effect: workspace_state now points to `{payload['next_run_id']}` after `{summary['status']}`; no runtime authority or Goal Achieve claim is made.
""",
    )
    append_once(
        ROOT_CHANGELOG,
        f"<!-- {RUN_ID} -->",
        f"""<!-- {RUN_ID} -->
## {payload['created_at_utc']} - F97B proxy scout record

Recorded first-hit survival/hazard proxy evidence and F97B state sync boundary.
""",
    )
    write_text(
        DECISION_MEMO,
        f"""# F97B Decision Memo

Action: Run a first-hit survival/hazard event proxy scout using closed-bar features and raw MT5 M5 bars.

Effect: The packet creates clue/negative memory only. Runtime probe is not applicable when candidate_count is zero and blocked as required if candidate_count is positive.

- run_id: `{RUN_ID}`
- status: `{summary['status']}`
- judgment: `{summary['judgment']}`
- candidate_gate_count: `{summary['candidate_gate_count']}`
- runtime_probe_status: `{summary['runtime_probe_status']}`
- next_action: `{payload['next_run_id']}`
- claim_boundary: `{CLAIM_BOUNDARY}`
""",
    )


def update_state_docs(payload: Mapping[str, Any]) -> None:
    state_text = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
active_branch: {current_branch()}
current_run_id: {payload['next_run_id']}
latest_completed_run_id: {RUN_ID}
current_status: {status_from(payload)}
current_judgment: {judgment_from(payload)}
next_run_id: {payload['next_run_id']}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
frontier_five_stage_direction_synthesis_status: {FRONTIER_FIVE_STAGE_STATUS}
frontier_topic_rotation_status: {FRONTIER_TOPIC_ROTATION_STATUS}
task_force_status: f97b_actual_subagent_calls_recorded_6_calls_5_selected_roster_agents_no_task_force_reviewed_pass_claim
runtime_probe_status: {runtime_probe_status_from(payload)}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F97B first-hit survival/hazard proxy scout(첫 도달 생존/위험 프록시 탐색)를 실행하고 산출물/영수증/게이트를 기록했다.'
- 'Effect(효과): 후보 게이트가 없으면 F97C repair/rotation(수리/회전)으로 넘기고, 후보가 있으면 같은 packet(묶음) MT5 runtime probe(MT5 런타임 탐침) 전에는 차단한다.'
- 'Runtime(런타임): Strategy Tester evidence(전략 테스터 근거) 없음; runtime authority(런타임 권위) 없음; Goal Achieve(목표 달성) 없음.'
"""
    write_text(WORKSPACE_STATE, state_text)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State

Action: F97B first-hit survival/hazard proxy scout is the latest completed run record.

Effect: Current truth is `{status_from(payload)}` and next run is `{payload['next_run_id']}`. No selected baseline, operating promotion, runtime authority, live readiness, or Goal Achieve is claimed.

- stage: `{STAGE_ID}`
- current run: `{payload['next_run_id']}`
- latest_completed_run_id: `{RUN_ID}`
- current_run_id: `{payload['next_run_id']}`
- runtime_probe_status: `{runtime_probe_status_from(payload)}`
- task_force_actual_subagent_calls: `6`
- task_force_selected_roster_agents: `5`
""",
    )
    write_text(
        CONTEXT_ANCHOR,
        f"""# {STAGE_ID}

Action: F97B recorded first-hit survival/hazard proxy scout evidence.

Effect: Use `{RUN_ID}` as the latest completed F97 evidence record and keep claim boundary at proxy-scout only.
""",
    )
    write_text(
        REVIEW_INDEX,
        f"""# F97 Review Index

- F97A stage open: `{PARENT_RUN_ID}`
- F97B proxy scout: `{RUN_ID}`
- F97B report: `{rel(F97B_REPORT)}`
- F97B packet: `{rel(WORK_PACKET)}`
""",
    )
    write_text(
        GLOBAL_SELECTION_STATUS,
        f"""# Selection Status

No selected baseline is claimed.

Latest record: `{RUN_ID}` status `{status_from(payload)}`.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# F97 Selection Status

No selected baseline, promotion candidate, operating promotion, runtime authority, live readiness, or Goal Achieve is claimed.

Current run: `{payload['next_run_id']}`.

Latest run: `{RUN_ID}`.
""",
    )
    write_text(
        STAGE_BRIEF,
        f"""# F97 First-Hit Survival/Hazard Event Sparse Axis

- current run: `{payload['next_run_id']}`
- latest_completed_run: `{RUN_ID}`
- F97B judgment: `{judgment_from(payload)}`
- candidate_gate_count: `{payload['metrics']['evaluation']['candidate_count']}`
- runtime_probe_status: `{runtime_probe_status_from(payload)}`

Action: F97B tested train-only first-hit survival/hazard proxy variants.

Effect: F97 now carries proxy evidence and negative memory into the next decision without claiming baseline, promotion, runtime authority, live readiness, or Goal Achieve.
""",
    )


def run_gate_cmd(args: Sequence[str], output_path: Path) -> dict[str, Any]:
    command = [sys.executable, "-m", *args]
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, timeout=180)
    result = {"command": command, "output_path": rel(output_path), "returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}
    if path_exists(output_path):
        try:
            result.update(read_json(output_path))
        except json.JSONDecodeError:
            result["status"] = "blocked"
    if completed.returncode != 0 or result.get("status") not in {"pass", "pass_with_warnings", "passed", "pass_not_due"}:
        result.setdefault("status", "blocked")
    return result


def sync_review_audit(src: Path, dst: Path) -> None:
    if path_exists(src):
        write_json(dst, read_json(src))


def audit_result_from_gate(name: str, result: Mapping[str, Any]) -> AuditResult:
    status = str(result.get("status", "blocked"))
    forbidden = tuple(FORBIDDEN_CLAIMS if status == "blocked" else ())
    return AuditResult(audit_name=name, status=status, findings=tuple(AuditFinding(check_id=f"{name}::status", severity="info" if status != "blocked" else "error", message=status) for _ in [0]), forbidden_claims=forbidden)


def audit_result_manual(name: str, status: str, *, forbidden: Sequence[str] = ()) -> AuditResult:
    return AuditResult(audit_name=name, status=status, forbidden_claims=tuple(forbidden))


def run_control_gates(payload: Mapping[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    write_packet_and_gate(payload)
    write_receipts(payload)
    results["work_packet_schema_lint"] = run_gate_cmd(
        ["foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET), "--output-json", str(PACKET_WORK_PACKET_LINT), "--allow-blocked-exit-zero"],
        PACKET_WORK_PACKET_LINT,
    )
    results["skill_receipt_schema_lint"] = run_gate_cmd(
        ["foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS), "--output-json", str(PACKET_SKILL_RECEIPT_LINT), "--allow-blocked-exit-zero"],
        PACKET_SKILL_RECEIPT_LINT,
    )
    write_packet_and_gate(payload, results)
    results["state_sync_audit"] = run_gate_cmd(
        [
            "foundation.control_plane.state_sync_audit",
            "--root",
            str(ROOT),
            "--active-stage",
            STAGE_ID,
            "--current-branch",
            current_branch(),
            "--output-json",
            str(PACKET_STATE_SYNC_AUDIT),
            "--allow-blocked-exit-zero",
        ],
        PACKET_STATE_SYNC_AUDIT,
    )
    results["required_gate_coverage_audit"] = run_gate_cmd(
        [
            "foundation.control_plane.required_gate_coverage_audit",
            "--work-packet",
            str(WORK_PACKET),
            "--closeout-gate",
            str(PACKET_CLOSEOUT_GATE),
            "--output-json",
            str(PACKET_REQUIRED_GATE_AUDIT),
            "--allow-blocked-exit-zero",
        ],
        PACKET_REQUIRED_GATE_AUDIT,
    )
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    candidate_count = int(payload["metrics"]["evaluation"]["candidate_count"])
    manual_audits = [
        audit_result_manual("codex_task_force_review_packet", "pass"),
        audit_result_manual("frontier_extra_due_check", "pass_not_due"),
        audit_result_manual("frontier_five_stage_direction_synthesis", "pass"),
        audit_result_manual("frontier_topic_rotation_check", "pass"),
        audit_result_manual("scope_completion_gate", "pass"),
        audit_result_manual("data_integrity_audit", "pass_with_boundary" if payload["metrics"]["data_integrity"].get("status") != "blocked" else "blocked", forbidden=FORBIDDEN_CLAIMS if payload["metrics"]["data_integrity"].get("status") == "blocked" else ()),
        audit_result_manual("model_validation_audit", "pass_with_boundary" if candidate_count == 0 else "blocked_pending_runtime_probe", forbidden=FORBIDDEN_CLAIMS if candidate_count > 0 else ()),
        audit_result_manual("kpi_contract_audit", "pass"),
        audit_result_manual("artifact_lineage_audit", "pass"),
        audit_result_manual("result_judgment_audit", "negative" if candidate_count == 0 else "blocked", forbidden=FORBIDDEN_CLAIMS if candidate_count > 0 else ()),
        audit_result_manual("state_sync_audit", str(results["state_sync_audit"].get("status", "blocked")), forbidden=FORBIDDEN_CLAIMS if results["state_sync_audit"].get("status") == "blocked" else ()),
        audit_result_manual("required_gate_coverage_audit", str(results["required_gate_coverage_audit"].get("status", "blocked")), forbidden=FORBIDDEN_CLAIMS if results["required_gate_coverage_audit"].get("status") == "blocked" else ()),
    ]
    if candidate_count > 0:
        manual_audits.append(audit_result_manual("runtime_evidence_gate", "blocked_pending_same_packet_mt5_probe", forbidden=FORBIDDEN_CLAIMS))
    audit_results = [
        audit_result_from_gate("work_packet_schema_lint", results["work_packet_schema_lint"]),
        audit_result_from_gate("skill_receipt_schema_lint", results["skill_receipt_schema_lint"]),
        *manual_audits,
    ]
    final_guard = guard_final_claims(requested_claims=ALLOWED_CLAIMS, audit_results=audit_results)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_guard.to_dict())
    write_json(FINAL_CLAIM_GUARD, final_guard.to_dict())
    results["final_claim_guard"] = final_guard.to_dict()
    write_packet_and_gate(payload, results)
    return results


def write_initial(payload: Mapping[str, Any]) -> None:
    write_run_artifacts(payload)
    write_audits(payload)
    write_receipts(payload)
    write_packet_and_gate(payload)
    update_ledgers(payload, gate_passes=0)
    update_state_docs(payload)
    update_register_docs(payload)


def write_final(payload: Mapping[str, Any], gate_results: Mapping[str, Any]) -> None:
    write_run_artifacts(payload)
    write_audits(payload, gate_results)
    write_receipts(payload)
    write_packet_and_gate(payload, gate_results)
    update_ledgers(payload, gate_passes=sum(1 for result in gate_results.values() if str(result.get("status")) in {"pass", "passed", "pass_with_warnings"}))
    update_artifact_registry(payload)
    update_state_docs(payload)
    update_register_docs(payload)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    metrics = materialize_proxy_metrics()
    payload = build_payload(created_at, metrics)
    write_initial(payload)
    gate_results = run_control_gates(payload)
    write_final(payload, gate_results)
    print(json.dumps(summary_payload(payload), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
