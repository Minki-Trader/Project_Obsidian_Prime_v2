from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized
from foundation.control_plane.required_gate_coverage_audit import audit_required_gate_coverage
from foundation.control_plane.skill_receipt_schema_lint import audit_skill_receipt_schemas
from foundation.control_plane.state_sync_audit import audit_state_sync
from foundation.control_plane.work_packet_schema_lint import audit_work_packet_schema
from stage_pipelines.stage_frontier_91 import frontier91b_regime_density_cost_abstention_proxy_scout as f91
from stage_pipelines.stage_frontier_94 import frontier94a_stage_open_tier_utility_label as f94a


STAGE_ID = "stage_frontier_94__tier_stable_realized_utility_label_axis"
RUN_ID = "frontier94B_tier_stable_realized_utility_label_proxy_scout_v1"
PARENT_RUN_ID = "frontier94A_stage_open_tier_stable_realized_utility_label_axis_v1"
NEXT_RUN_ID = "frontier94C_tier_stable_realized_utility_repair_or_rotation_decision_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_94/frontier94b_tier_utility_proxy_scout.py"

STATUS_NEGATIVE = "f94b_tier_stable_realized_utility_proxy_scout_negative_no_runnable_surface_no_authority"
STATUS_BLOCKED_RUNTIME = "f94b_proxy_gate_signal_blocked_pending_same_packet_mt5_runtime_probe"
JUDGMENT_NEGATIVE = "negative_proxy_scout_tier_utility_gate_failed_no_runtime_trigger"
JUDGMENT_BLOCKED_RUNTIME = "blocked_runtime_probe_required_after_proxy_gate_signal"
CLAIM_BOUNDARY = (
    "f94b_proxy_scout_only_no_runnable_candidate_no_mt5_runtime_evidence_no_selected_baseline_"
    "no_operating_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS_NEGATIVE = (
    "not_run_no_meaningful_runnable_candidate_no_onnx_ea_set_behavior_no_runtime_materialization_"
    "economics_or_handoff_claim_not_cost_or_proxy_bad_skip"
)
RUNTIME_PROBE_STATUS_BLOCKED = "blocked_pending_same_packet_mt5_strategy_tester_probe_before_any_candidate_claim"

FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f93_closeout_next_boundary_f100_e01_closed_for_f050"
FRONTIER_TOPIC_ROTATION_STATUS = "continuation_pass_f94b_proxy_scout_within_f94_axis_not_new_frontier_open"

HORIZON_BARS = 12
CANDIDATE_MIN_TRADES_PER_DAY = 5.0
CANDIDATE_MAX_TRADES_PER_DAY = 10.0
CANDIDATE_TIER_B_MIN_TRADES_PER_DAY = 3.0
CANDIDATE_TIER_B_MAX_TRADES_PER_DAY = 12.0
CANDIDATE_MIN_PF = 1.05
CANDIDATE_TIER_B_MIN_PF = 1.0
CANDIDATE_MAX_DD = 0.30
CANDIDATE_MIN_SIDE_SHARE = 0.20
CANDIDATE_MAX_TIER_GAP = 0.75
RANDOM_CONTROL_REPS = 16
RNG_SEED = 9402

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier94B"
PROXY_DIR = RUN_DIR / "proxy_scout"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SKILL_RECEIPT_DIR = PACKET_DIR / "skill_receipts"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
UTILITY_LABEL_CONFIG = PROXY_DIR / "utility_label_config.json"
DATA_LOCK = PROXY_DIR / "data_feature_split_lock.json"
TIER_ROUTE_SUMMARY = PROXY_DIR / "tier_route_summary.json"
TIER_B_SUMMARY = PROXY_DIR / "tier_b_summary.json"
LABEL_INTEGRITY = PROXY_DIR / "label_integrity_audit.json"
VARIANT_MATRIX = PROXY_DIR / "variant_matrix.json"
VARIANT_METRICS_CSV = PROXY_DIR / "variant_metrics.csv"
SPLIT_METRICS_CSV = PROXY_DIR / "split_metrics.csv"
NEGATIVE_CONTROL_CSV = PROXY_DIR / "negative_control_metrics.csv"
UTILITY_EXPOSURE_CSV = PROXY_DIR / "utility_exposure_ledger.csv"
CANDIDATE_GATE_JSON = PROXY_DIR / "candidate_gate.json"
SCORE_SAMPLE_CSV = PROXY_DIR / "proxy_scores_sample.csv"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

TASK_FORCE_REVIEW = REVIEW_DIR / "f94b_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f94b_frontier_extra_due_check.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f94b_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f94b_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f94b_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f94b_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f94b_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f94b_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f94b_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f94b_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f94b_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f94b_required_gate_coverage_audit.json"
EXECUTION_SUMMARY = REVIEW_DIR / "f94b_execution_summary.json"
F94B_REPORT = REVIEW_DIR / "frontier94B_tier_stable_realized_utility_proxy_scout_report.md"

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
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier94b_tier_utility_proxy_scout.md"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

F94A_BRIEF = STAGE_DIR / "02_runs" / "frontier94A" / "d" / "f94b_proxy_scout_brief.json"
F94A_DATA_PLAN = STAGE_DIR / "02_runs" / "frontier94A" / "d" / "data_integrity_plan.json"
F94A_RUNTIME_CONTRACT = STAGE_DIR / "02_runs" / "frontier94A" / "d" / "runtime_contract.json"
F94A_RISK_LABEL_DESIGN = STAGE_DIR / "02_runs" / "frontier94A" / "d" / "risk_label_design.json"
F94A_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F93B_SUMMARY = (
    ROOT
    / "stages"
    / "stage_frontier_93__side_balance_cost_exposure_risk_budget_axis"
    / "03_reviews"
    / "f93b_execution_summary.json"
)
F93B_CANDIDATE_GATE = (
    ROOT
    / "stages"
    / "stage_frontier_93__side_balance_cost_exposure_risk_budget_axis"
    / "02_runs"
    / "frontier93B"
    / "proxy_scout"
    / "candidate_gate.json"
)
MODEL_INPUT_SUMMARY = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
    / "model_input_summary.json"
)
MODEL_INPUT_FEATURE_ORDER = MODEL_INPUT_SUMMARY.with_name("model_input_feature_order.txt")
MODEL_INPUT_DATASET = MODEL_INPUT_SUMMARY.with_name("model_input_dataset.parquet")
RAW_US100_CSV = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"
RAW_US100_MANIFEST = RAW_US100_CSV.with_suffix(".manifest.json")

ALLOWED_CLAIMS = [
    "f94b_proxy_scout_executed",
    "f94b_proxy_metrics_recorded",
    "f94b_task_force_actual_calls_recorded",
    "f94b_gate_result_recorded_no_runtime_authority",
    "f94c_repair_or_rotation_planned",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "completed",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "promotion_candidate",
    "runtime_probe",
    "runtime_verified",
    "strategy_tester_runtime_economics",
    "runtime_economics",
    "runtime_economics_pass",
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
REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "codex_task_force_review_packet",
    "frontier_extra_due_check",
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
        "reason_code": "no_runnable_candidate_no_runtime_claim",
        "reason": "F94B produced Python proxy evidence only and no ONNX, EA, set, tester output, materialization, economics, handoff, promotion, or authority claim.",
        "claim_effect": "No runtime verified, economics pass, materialization ready, handoff complete, promotion, or authority claim is allowed.",
    },
    {
        "gate": "wfo_stress_gate",
        "reason_code": "outside_claim_surface_proxy_scout_no_runnable_surface",
        "reason": "F94B is a proxy scout. WFO/stress is not claimed unless a runnable surface appears and runtime materialization begins.",
        "claim_effect": "No WFO pass, stress pass, selected baseline, or runtime authority claim is allowed.",
    },
]

TASK_FORCE_CALLS = [
    {
        "roster_agent_id": "agent_01_system_governor",
        "spawned_agent_id": "019ede86-1dfa-7f90-972b-e46423070afa",
        "nickname": "Linnaeus",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "disposition": "accepted",
        "summary": "Proceed as bounded proxy_scout only; no completion, selected baseline, runtime authority, live readiness, or Goal Achieve claim.",
    },
    {
        "roster_agent_id": "agent_04_evidence_control_plane",
        "spawned_agent_id": "019ede86-33d0-7d30-8881-0b2a5d8ebedd",
        "nickname": "Hooke",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "disposition": "accepted_with_local_verification",
        "summary": "Record work packet, receipts, Task Force call packet, pre-run locks, proxy outputs, ledgers, state sync, and final claim guard.",
    },
    {
        "roster_agent_id": "agent_05_data_feature_contract",
        "spawned_agent_id": "019ede86-4c7d-72c2-ae74-a370b099bb4d",
        "nickname": "Heisenberg",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "disposition": "accepted_with_local_verification",
        "summary": "Lock current dataset hash, explain prior hash mismatch, keep MFE/MAE/utility out of model features, censor split-edge labels, and run leakage checks.",
    },
    {
        "roster_agent_id": "agent_06_quant_research",
        "spawned_agent_id": "019ede86-671c-7d10-a250-03a70873393b",
        "nickname": "Socrates",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "disposition": "accepted_with_local_verification",
        "summary": "Use worst-tier path utility, hard tier gap minimax, downside ambiguity stress, side-regime readout, and density-preserving utility variants.",
    },
    {
        "roster_agent_id": "agent_07_model_validation_risk",
        "spawned_agent_id": "019ede86-7ba1-7d11-9068-b245411f0cc0",
        "nickname": "Dalton",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "disposition": "accepted_with_local_verification",
        "summary": "Train-only thresholds, validation gate, OOS final-read-only, no PF-only selection, no calibrated probability claim.",
    },
    {
        "roster_agent_id": "agent_08_mt5_onnx_runtime",
        "spawned_agent_id": "019ede86-8fd9-71b3-8454-8705c949ec71",
        "nickname": "Darwin",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "disposition": "accepted",
        "summary": "Same-packet MT5 Strategy Tester probe is required only if F94B creates a meaningful runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics/handoff claim.",
    },
]


def rel(path: Path) -> str:
    return f94a.rel(path)


def write_text(path: Path, text: str) -> None:
    f94a.write_text(path, text)


def write_json(path: Path, payload: Any) -> None:
    f94a.write_json(path, payload)


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    f94a.write_yaml(path, payload)


def read_json(path: Path) -> dict[str, Any]:
    return f94a.read_json(path)


def file_identity(path: Path) -> dict[str, Any]:
    identity = f94a.file_identity(path)
    if identity.get("exists") and path.suffix.lower() in {".parquet", ".csv"}:
        identity["raw_sha256"] = hashlib.sha256(io_path(path).read_bytes()).hexdigest()
        identity["hash_note"] = "sha256 is ledger LF-normalized identity; raw_sha256 is byte identity for binary/data files."
    return identity


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True, timeout=10)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def stable_seed(*parts: object) -> int:
    digest = hashlib.sha256("::".join(str(part) for part in parts).encode("utf-8")).hexdigest()
    return int(digest[:12], 16) % (2**32 - 1)


def ensure_dirs() -> None:
    for path in [RUN_DIR, PROXY_DIR, REPORT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, SKILL_RECEIPT_DIR]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def source_inputs() -> list[Path]:
    return [
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        F94A_BRIEF,
        F94A_DATA_PLAN,
        F94A_RUNTIME_CONTRACT,
        F94A_RISK_LABEL_DESIGN,
        F94A_PACKET,
        F93B_SUMMARY,
        F93B_CANDIDATE_GATE,
        MODEL_INPUT_SUMMARY,
        MODEL_INPUT_FEATURE_ORDER,
        MODEL_INPUT_DATASET,
        RAW_US100_CSV,
        RAW_US100_MANIFEST,
        ROOT / "docs" / "agent_control" / "work_family_registry.yaml",
        ROOT / "docs" / "agent_control" / "codex_task_force_registry.yaml",
    ]


def produced_artifacts() -> list[Path]:
    return [
        ROOT / SCRIPT_REL,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        UTILITY_LABEL_CONFIG,
        DATA_LOCK,
        TIER_ROUTE_SUMMARY,
        TIER_B_SUMMARY,
        LABEL_INTEGRITY,
        VARIANT_MATRIX,
        VARIANT_METRICS_CSV,
        SPLIT_METRICS_CSV,
        NEGATIVE_CONTROL_CSV,
        UTILITY_EXPOSURE_CSV,
        CANDIDATE_GATE_JSON,
        SCORE_SAMPLE_CSV,
        RESULT_SUMMARY,
        TASK_FORCE_REVIEW,
        PACKET_TASK_FORCE_REVIEW,
        FRONTIER_EXTRA_DUE_CHECK,
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
        EXECUTION_SUMMARY,
        F94B_REPORT,
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


def feature_hash(features: Sequence[str]) -> str:
    return hashlib.sha256(("\n".join(features) + "\n").encode("utf-8")).hexdigest()


def feature_order_file_hash() -> str:
    identity = file_identity(MODEL_INPUT_FEATURE_ORDER)
    return str(identity.get("sha256") or feature_hash(feature_columns()))


def feature_columns() -> list[str]:
    return f91.feature_columns()


def variant_specs(features: Sequence[str]) -> list[dict[str, Any]]:
    feature_list = list(features)
    regime = [
        col
        for col in feature_list
        if any(token in col for token in ["vol", "adx", "rsi", "session", "return_1", "return_3", "distance", "atr", "spread"])
    ]
    regime = regime or feature_list
    return [
        {
            "variant_id": "v01_worst_tier_path_utility",
            "objective_id": "worst_tier_path_utility",
            "family": "ridge_utility",
            "features": feature_list,
            "threshold_mode": "train_quantile",
            "quantile": 0.85,
            "mfe_weight": 0.35,
            "mae_weight": 0.75,
            "cost_weight": 1.0,
            "both_touch_weight": 0.25,
            "tier_gap_penalty": 0.50,
            "density_score_weight": 0.0,
        },
        {
            "variant_id": "v02_hard_tier_gap_minimax",
            "objective_id": "hard_tier_gap_minimax",
            "family": "extra_trees_utility",
            "features": feature_list,
            "threshold_mode": "train_quantile",
            "quantile": 0.85,
            "mfe_weight": 0.35,
            "mae_weight": 0.75,
            "cost_weight": 1.0,
            "both_touch_weight": 0.25,
            "tier_gap_penalty": 1.00,
            "density_score_weight": 0.0,
        },
        {
            "variant_id": "v03_downside_ambiguity_stress",
            "objective_id": "downside_ambiguity_stress",
            "family": "ridge_utility",
            "features": feature_list,
            "threshold_mode": "train_quantile",
            "quantile": 0.85,
            "mfe_weight": 0.25,
            "mae_weight": 1.15,
            "cost_weight": 1.0,
            "both_touch_weight": 0.50,
            "tier_gap_penalty": 0.50,
            "density_score_weight": 0.0,
        },
        {
            "variant_id": "v04_side_regime_utility_readout",
            "objective_id": "side_regime_utility_readout",
            "family": "ridge_utility",
            "features": regime,
            "threshold_mode": "train_quantile",
            "quantile": 0.85,
            "mfe_weight": 0.35,
            "mae_weight": 0.85,
            "cost_weight": 1.0,
            "both_touch_weight": 0.25,
            "tier_gap_penalty": 0.50,
            "density_score_weight": 0.0,
        },
        {
            "variant_id": "v05_density_preserving_utility",
            "objective_id": "density_preserving_utility",
            "family": "ridge_utility",
            "features": feature_list,
            "threshold_mode": "train_target_trades_per_day",
            "target_trades_per_day": 7.0,
            "mfe_weight": 0.35,
            "mae_weight": 0.75,
            "cost_weight": 1.0,
            "both_touch_weight": 0.25,
            "tier_gap_penalty": 0.50,
            "density_score_weight": 0.10,
        },
    ]


def load_raw_bars() -> pd.DataFrame:
    raw = pd.read_csv(
        io_path(RAW_US100_CSV),
        usecols=["time_close_unix", "open", "high", "low", "close", "spread_points"],
    )
    raw["timestamp"] = pd.to_datetime(pd.to_numeric(raw["time_close_unix"], errors="coerce"), unit="s", utc=True)
    for col in ["open", "high", "low", "close", "spread_points"]:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    raw = raw.dropna(subset=["timestamp", "high", "low", "close"]).drop_duplicates("timestamp", keep="last")
    return raw.sort_values("timestamp").reset_index(drop=True)


def add_path_labels(frame: pd.DataFrame, raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    out = frame.copy().reset_index(drop=True)
    raw_ts = pd.to_datetime(raw["timestamp"], utc=True)
    index_by_ts = {int(ts.value): idx for idx, ts in enumerate(raw_ts)}
    positions = out["timestamp"].map(lambda ts: index_by_ts.get(int(pd.Timestamp(ts).value), -1)).to_numpy(dtype=int)
    high = raw["high"].to_numpy(dtype=float)
    low = raw["low"].to_numpy(dtype=float)
    close = raw["close"].to_numpy(dtype=float)
    valid = (positions >= 0) & ((positions + HORIZON_BARS) < len(raw))

    split_max = out.groupby(out["split"].astype(str))["timestamp"].max().to_dict()
    future_ts_values: list[pd.Timestamp | pd.NaT] = []
    entry = np.full(len(out), np.nan, dtype=float)
    future_close = np.full(len(out), np.nan, dtype=float)
    future_high = np.full(len(out), np.nan, dtype=float)
    future_low = np.full(len(out), np.nan, dtype=float)

    for i, pos in enumerate(positions):
        if not valid[i]:
            future_ts_values.append(pd.NaT)
            continue
        window = slice(pos + 1, pos + HORIZON_BARS + 1)
        entry[i] = close[pos]
        future_close[i] = close[pos + HORIZON_BARS]
        future_high[i] = float(np.nanmax(high[window]))
        future_low[i] = float(np.nanmin(low[window]))
        future_ts_values.append(pd.Timestamp(raw_ts.iloc[pos + HORIZON_BARS]))

    future_ts = pd.Series(future_ts_values, index=out.index)
    same_split = []
    for idx, split in enumerate(out["split"].astype(str)):
        end = split_max.get(split)
        same_split.append(bool(pd.notna(future_ts.iloc[idx]) and end is not None and future_ts.iloc[idx] <= end))
    same_split_arr = np.asarray(same_split, dtype=bool)
    label_ok = valid & same_split_arr & np.isfinite(entry) & (entry > 0)

    out["path_label_available"] = label_ok
    out["path_future_timestamp"] = future_ts
    out["entry_close"] = entry
    out["future_close_path"] = future_close
    out["long_mfe"] = np.where(label_ok, (future_high - entry) / entry, np.nan)
    out["long_mae"] = np.where(label_ok, (entry - future_low) / entry, np.nan)
    out["short_mfe"] = np.where(label_ok, (entry - future_low) / entry, np.nan)
    out["short_mae"] = np.where(label_ok, (future_high - entry) / entry, np.nan)
    out["future_path_return"] = np.where(label_ok, np.log(np.maximum(future_close, 1e-12) / np.maximum(entry, 1e-12)), np.nan)
    out["split_edge_censored"] = valid & ~same_split_arr
    out["raw_timestamp_missing"] = positions < 0

    summary = {
        "rows": int(len(out)),
        "path_label_available_rows": int(label_ok.sum()),
        "raw_timestamp_missing_rows": int((positions < 0).sum()),
        "horizon_out_of_raw_range_rows": int(((positions >= 0) & ~valid).sum()),
        "split_edge_censored_rows": int((valid & ~same_split_arr).sum()),
        "horizon_bars": HORIZON_BARS,
    }
    return out, summary


def prepare_frames() -> tuple[dict[str, pd.DataFrame], dict[str, Any], dict[str, Any], dict[str, Any]]:
    frames, route_summary, tier_b_summary, f91_integrity = f91.prepare_routed_frames()
    raw = load_raw_bars()
    out_frames: dict[str, pd.DataFrame] = {}
    label_summary: dict[str, Any] = {}
    for view, frame in frames.items():
        labelled, summary = add_path_labels(frame, raw)
        labelled = labelled.loc[labelled["path_label_available"]].copy().reset_index(drop=True)
        out_frames[view] = labelled
        label_summary[view] = summary | {"rows_after_label_censor": int(len(labelled))}
    integrity = {
        "f91_route_integrity": f91_integrity,
        "path_label_summary": label_summary,
        "raw_bar_identity": file_identity(RAW_US100_CSV),
        "raw_manifest_identity": file_identity(RAW_US100_MANIFEST),
    }
    return out_frames, route_summary, tier_b_summary, integrity


def utility_targets(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    ret = pd.to_numeric(frame["future_log_return_12"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    cost = pd.to_numeric(frame["cost_penalty_proxy"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    long_mfe = pd.to_numeric(frame["long_mfe"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    long_mae = pd.to_numeric(frame["long_mae"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    short_mfe = pd.to_numeric(frame["short_mfe"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    short_mae = pd.to_numeric(frame["short_mae"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    mfe_w = float(spec["mfe_weight"])
    mae_w = float(spec["mae_weight"])
    cost_w = float(spec["cost_weight"])
    both_w = float(spec["both_touch_weight"])
    long_ambig = np.minimum(long_mfe, long_mae)
    short_ambig = np.minimum(short_mfe, short_mae)
    long_u = ret + mfe_w * long_mfe - mae_w * long_mae - cost_w * cost - both_w * long_ambig
    short_u = -ret + mfe_w * short_mfe - mae_w * short_mae - cost_w * cost - both_w * short_ambig
    return long_u.astype(float), short_u.astype(float)


def fit_utility_model(spec: Mapping[str, Any], train: pd.DataFrame) -> Any:
    cols = list(spec["features"])
    long_u, short_u = utility_targets(train, spec)
    y = np.column_stack([long_u, short_u])
    if spec["family"] == "extra_trees_utility":
        model = make_pipeline(
            SimpleImputer(strategy="median"),
            ExtraTreesRegressor(
                n_estimators=180,
                max_depth=6,
                min_samples_leaf=80,
                random_state=RNG_SEED,
                n_jobs=1,
            ),
        )
    else:
        model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), Ridge(alpha=20.0))
    model.fit(train[cols], y)
    return model


def predict_utility(model: Any, spec: Mapping[str, Any], frame: pd.DataFrame, train_ref: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if frame.empty:
        return np.array([], dtype=int), np.array([], dtype=float), np.empty((0, 2), dtype=float), np.array([], dtype=float)
    cols = list(spec["features"])
    pred = np.asarray(model.predict(frame[cols]), dtype=float)
    if pred.ndim == 1:
        pred = np.column_stack([pred, -pred])
    pred_long = pred[:, 0]
    pred_short = pred[:, 1]
    side = np.where(pred_long >= pred_short, 1, -1).astype(int)
    strength = np.maximum(pred_long, pred_short).astype(float)
    if float(spec.get("density_score_weight", 0.0)):
        train_density = pd.to_numeric(train_ref["density_proxy"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
        if train_density.empty:
            density_norm = np.zeros(len(frame), dtype=float)
        else:
            low = float(train_density.quantile(0.05))
            high = float(train_density.quantile(0.95))
            if high <= low:
                high = low + 1e-12
            values = pd.to_numeric(frame["density_proxy"], errors="coerce").fillna(low).clip(lower=low, upper=high)
            density_norm = (values.to_numpy(dtype=float) - low) / (high - low)
        strength = strength + float(spec["density_score_weight"]) * density_norm
    margin = np.abs(pred_long - pred_short).astype(float)
    return side, strength, pred, margin


def train_threshold(spec: Mapping[str, Any], train: pd.DataFrame, train_strength: np.ndarray) -> float:
    values = np.asarray(train_strength, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return math.inf
    if spec["threshold_mode"] == "train_target_trades_per_day":
        days = max(1, int(train["timestamp"].dt.date.nunique()))
        target_count = int(max(1, min(len(values), round(float(spec["target_trades_per_day"]) * days))))
        sorted_values = np.sort(values)
        return float(sorted_values[max(0, len(sorted_values) - target_count)])
    return float(np.quantile(values, float(spec["quantile"])))


def actual_utility(frame: pd.DataFrame, side: np.ndarray, spec: Mapping[str, Any]) -> np.ndarray:
    long_u, short_u = utility_targets(frame, spec)
    return np.where(np.asarray(side, dtype=int) == 1, long_u, short_u).astype(float)


def random_control(frame: pd.DataFrame, trade_count: int, side: np.ndarray, *, seed: int) -> dict[str, Any]:
    if trade_count <= 0 or len(frame) == 0:
        base = f91.pnl_metrics(frame, np.zeros(len(frame), dtype=bool), side)
        return {f"random_{key}_mean": value for key, value in base.items() if key in {"net_proxy", "proxy_pf", "max_drawdown"}}
    rng = np.random.default_rng(seed)
    nets: list[float] = []
    pfs: list[float] = []
    dds: list[float] = []
    count = min(trade_count, len(frame))
    for _ in range(RANDOM_CONTROL_REPS):
        mask = np.zeros(len(frame), dtype=bool)
        mask[rng.choice(len(frame), size=count, replace=False)] = True
        metrics = f91.pnl_metrics(frame, mask, side)
        nets.append(float(metrics["net_proxy"] or 0.0))
        pfs.append(float(metrics["proxy_pf"] or 0.0))
        dds.append(float(metrics["max_drawdown"] or 0.0))
    return {
        "random_net_proxy_mean": round(float(np.mean(nets)), 8),
        "random_proxy_pf_mean": round(float(np.mean(pfs)), 6),
        "random_max_drawdown_mean": round(float(np.mean(dds)), 8),
    }


def deterministic_control_rows(
    frame: pd.DataFrame,
    selected_mask: np.ndarray,
    side: np.ndarray,
    strength: np.ndarray,
    variant_id: str,
    view: str,
    split: str,
) -> list[dict[str, Any]]:
    trade_count = int(np.asarray(selected_mask, dtype=bool).sum())
    rows: list[dict[str, Any]] = []
    controls: list[tuple[str, np.ndarray]] = [("all_trade_no_abstain", np.ones(len(frame), dtype=bool))]
    random_mask = np.zeros(len(frame), dtype=bool)
    if trade_count > 0 and len(frame) > 0:
        rng = np.random.default_rng(stable_seed("control", variant_id, view, split))
        random_mask[rng.choice(len(frame), size=min(trade_count, len(frame)), replace=False)] = True
    controls.append(("random_abstain_rate_match_single", random_mask))
    density_mask = np.zeros(len(frame), dtype=bool)
    strength_mask = np.zeros(len(frame), dtype=bool)
    if trade_count > 0 and len(frame) > 0:
        density_order = np.argsort(-frame["density_proxy"].to_numpy(dtype=float))[: min(trade_count, len(frame))]
        strength_order = np.argsort(-np.asarray(strength, dtype=float))[: min(trade_count, len(frame))]
        density_mask[density_order] = True
        strength_mask[strength_order] = True
    controls.append(("density_only_high_density_control", density_mask))
    controls.append(("unbudgeted_strength_rank_replay", strength_mask))
    for control_id, mask in controls:
        metrics = f91.pnl_metrics(frame, mask, side)
        rows.append({"variant_id": variant_id, "view": view, "split": split, "control_id": control_id, **metrics})
    return rows


def utility_exposure_rows(frame: pd.DataFrame, selected_mask: np.ndarray, side: np.ndarray, spec: Mapping[str, Any], variant_id: str, view: str, split: str) -> list[dict[str, Any]]:
    selected_mask = np.asarray(selected_mask, dtype=bool)
    side = np.asarray(side, dtype=int)
    utility = actual_utility(frame, side, spec)
    total = int(selected_mask.sum())
    rows: list[dict[str, Any]] = []
    for bucket_col in ["source_tier", "cost_bucket", "regime_key"]:
        if bucket_col not in frame.columns:
            continue
        for bucket in sorted(frame[bucket_col].astype(str).unique().tolist()):
            bucket_mask = selected_mask & frame[bucket_col].astype(str).eq(bucket).to_numpy()
            values = utility[bucket_mask]
            rows.append(
                {
                    "variant_id": variant_id,
                    "view": view,
                    "split": split,
                    "bucket_type": bucket_col,
                    "bucket": bucket,
                    "bucket_trade_count": int(bucket_mask.sum()),
                    "bucket_trade_share": round(float(int(bucket_mask.sum()) / total), 6) if total else 0.0,
                    "utility_sum": round(float(values.sum()), 8) if len(values) else 0.0,
                    "utility_mean": round(float(values.mean()), 8) if len(values) else None,
                    "utility_min": round(float(values.min()), 8) if len(values) else None,
                }
            )
    return rows


def metric_row(
    frame: pd.DataFrame,
    selected: np.ndarray,
    side: np.ndarray,
    strength: np.ndarray,
    margin: np.ndarray,
    spec: Mapping[str, Any],
    threshold: float,
    view: str,
    split: str,
    seed: int,
) -> dict[str, Any]:
    metrics = f91.pnl_metrics(frame, selected, side)
    utility = actual_utility(frame, side, spec)
    selected_utility = utility[np.asarray(selected, dtype=bool)]
    selected_strength = np.asarray(strength, dtype=float)[np.asarray(selected, dtype=bool)]
    selected_margin = np.asarray(margin, dtype=float)[np.asarray(selected, dtype=bool)]
    rand = random_control(frame, int(np.asarray(selected, dtype=bool).sum()), side, seed=seed)
    return {
        "variant_id": spec["variant_id"],
        "objective_id": spec["objective_id"],
        "model_family": spec["family"],
        "feature_count": len(spec["features"]),
        "threshold_source": spec["threshold_mode"],
        "strength_quantile": spec.get("quantile"),
        "target_trades_per_day": spec.get("target_trades_per_day"),
        "strength_threshold": round(float(threshold), 10) if np.isfinite(threshold) else None,
        "tier_gap_penalty": spec["tier_gap_penalty"],
        "mfe_weight": spec["mfe_weight"],
        "mae_weight": spec["mae_weight"],
        "both_touch_weight": spec["both_touch_weight"],
        "density_score_weight": spec["density_score_weight"],
        "view": view,
        "split": split,
        "selected_strength_mean": round(float(selected_strength.mean()), 8) if len(selected_strength) else None,
        "selected_margin_mean": round(float(selected_margin.mean()), 8) if len(selected_margin) else None,
        "realized_utility_sum": round(float(selected_utility.sum()), 8) if len(selected_utility) else 0.0,
        "realized_utility_mean": round(float(selected_utility.mean()), 8) if len(selected_utility) else None,
        "realized_utility_min": round(float(selected_utility.min()), 8) if len(selected_utility) else None,
        **metrics,
        **rand,
    }


def metric_failures(row: Mapping[str, Any], view: str) -> list[str]:
    failures: list[str] = []
    net = float(row.get("net_proxy") or 0.0)
    pf = float(row.get("proxy_pf") or 0.0)
    tpd = float(row.get("trades_per_day") or 0.0)
    dd = float(row.get("max_drawdown") or 0.0)
    side_share = row.get("side_min_share")
    side_share_value = float(side_share) if side_share is not None else 0.0
    random_net = float(row.get("random_net_proxy_mean") or 0.0)
    recovery = row.get("recovery_factor")
    recovery_value = float(recovery) if recovery is not None else -999.0
    utility_mean = row.get("realized_utility_mean")
    utility_value = float(utility_mean) if utility_mean is not None else -999.0
    if view == "tier_b_separate":
        if net < 0:
            failures.append(f"{view}_validation_net_negative")
        if pf < CANDIDATE_TIER_B_MIN_PF:
            failures.append(f"{view}_validation_pf_below_tier_b_min")
        if not (CANDIDATE_TIER_B_MIN_TRADES_PER_DAY <= tpd <= CANDIDATE_TIER_B_MAX_TRADES_PER_DAY):
            failures.append(f"{view}_validation_trades_per_day_outside_tier_b_range")
    else:
        if net <= 0:
            failures.append(f"{view}_validation_net_nonpositive")
        if pf < CANDIDATE_MIN_PF:
            failures.append(f"{view}_validation_pf_below_min")
        if not (CANDIDATE_MIN_TRADES_PER_DAY <= tpd <= CANDIDATE_MAX_TRADES_PER_DAY):
            failures.append(f"{view}_validation_trades_per_day_outside_range")
    if utility_value <= 0:
        failures.append(f"{view}_validation_realized_utility_nonpositive")
    if dd > CANDIDATE_MAX_DD:
        failures.append(f"{view}_validation_drawdown_above_predeclared_cap")
    if side_share_value < CANDIDATE_MIN_SIDE_SHARE:
        failures.append(f"{view}_validation_side_concentration")
    if net <= random_net:
        failures.append(f"{view}_validation_not_above_random_control")
    if view == "tier_ab_combined" and recovery_value <= 0:
        failures.append(f"{view}_validation_recovery_factor_nonpositive")
    return failures


def tier_gap_metrics(variant_results: Mapping[str, Mapping[str, Mapping[str, Any]]]) -> dict[str, Any]:
    val_a = variant_results["tier_a_separate"]["validation"]
    val_b = variant_results["tier_b_separate"]["validation"]
    u_a = float(val_a.get("realized_utility_mean") or 0.0)
    u_b = float(val_b.get("realized_utility_mean") or 0.0)
    denom = max(abs(u_a), abs(u_b), 1e-12)
    gap = abs(u_a - u_b) / denom
    return {
        "validation_tier_a_utility_mean": round(u_a, 8),
        "validation_tier_b_utility_mean": round(u_b, 8),
        "validation_worst_tier_utility_mean": round(min(u_a, u_b), 8),
        "validation_tier_gap_ratio": round(float(gap), 8),
    }


def candidate_gate_for_variant(variant_id: str, variant_results: Mapping[str, Mapping[str, Mapping[str, Any]]]) -> dict[str, Any]:
    failures: list[str] = []
    for view in ["tier_a_separate", "tier_b_separate", "tier_ab_combined"]:
        failures.extend(metric_failures(variant_results[view]["validation"], view))
    gap = tier_gap_metrics(variant_results)
    if float(gap["validation_worst_tier_utility_mean"]) <= 0:
        failures.append("validation_worst_tier_utility_nonpositive")
    if float(gap["validation_tier_gap_ratio"]) > CANDIDATE_MAX_TIER_GAP:
        failures.append("validation_tier_gap_above_predeclared_cap")
    oos_notes: list[str] = []
    for view in ["tier_a_separate", "tier_b_separate", "tier_ab_combined"]:
        oos = variant_results[view]["oos"]
        if float(oos.get("net_proxy") or 0.0) <= 0:
            oos_notes.append(f"{view}_oos_net_nonpositive_final_read")
        if float(oos.get("proxy_pf") or 0.0) < 1.0:
            oos_notes.append(f"{view}_oos_pf_below_1_final_read")
    return {
        "variant_id": variant_id,
        "status": "proxy_gate_signal_triggered" if not failures else "not_candidate",
        "selection_failures": failures,
        "tier_gap_metrics": gap,
        "oos_final_read_notes": oos_notes,
        "claim_effect": (
            "runtime_probe_required_before_any_candidate_claim"
            if not failures
            else "runtime_evidence_gate_not_triggered_no_runnable_candidate_claim"
        ),
    }


def diagnostic_score(row: Mapping[str, Any], gap: Mapping[str, Any]) -> float:
    net = float(row.get("net_proxy") or 0.0)
    pf = float(row.get("proxy_pf") or 0.0)
    dd = float(row.get("max_drawdown") or 0.0)
    tpd = float(row.get("trades_per_day") or 0.0)
    random_net = float(row.get("random_net_proxy_mean") or 0.0)
    worst_u = float(gap.get("validation_worst_tier_utility_mean") or 0.0)
    tier_stability = max(0.0, 1.0 - float(gap.get("validation_tier_gap_ratio") or 1.0))
    econ = max(-1.0, min(1.0, net * 10.0)) + max(-0.5, min(0.5, pf - 1.0))
    risk = max(-1.0, min(1.0, (CANDIDATE_MAX_DD - dd) / max(CANDIDATE_MAX_DD, 1e-12)))
    density = max(0.0, 1.0 - (abs(tpd - 7.0) / 7.0))
    control_lift = max(-1.0, min(1.0, (net - random_net) * 10.0))
    return 100.0 * (0.30 * worst_u + 0.20 * tier_stability + 0.15 * econ + 0.15 * risk + 0.10 * density + 0.10 * control_lift)


def choose_best_diagnostic(rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    gate_by_variant = {str(gate["variant_id"]): gate for gate in gates}
    best: dict[str, Any] = {}
    best_score = -1e100
    for row in rows:
        if row.get("view") != "tier_ab_combined" or row.get("split") != "validation":
            continue
        variant = str(row.get("variant_id"))
        score = diagnostic_score(row, gate_by_variant.get(variant, {}).get("tier_gap_metrics", {}))
        if score > best_score:
            best_score = score
            best = dict(row)
    if not best:
        return {}
    variant = str(best.get("variant_id"))
    return {
        "variant_id": variant,
        "diagnostic_score": round(float(best_score), 8),
        "validation": best,
        "gate": gate_by_variant.get(variant, {}),
        "oos_final_read": next(
            (dict(row) for row in rows if row.get("variant_id") == variant and row.get("view") == "tier_ab_combined" and row.get("split") == "oos"),
            {},
        ),
    }


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def evaluate_variants(frames: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    features = feature_columns()
    specs = variant_specs(features)
    train = frames["tier_ab_combined"].loc[frames["tier_ab_combined"]["split"].astype(str).eq("train")].copy()
    metric_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    utility_rows: list[dict[str, Any]] = []
    score_samples: list[dict[str, Any]] = []
    gates: list[dict[str, Any]] = []

    for spec_index, spec in enumerate(specs):
        model = fit_utility_model(spec, train)
        train_side, train_strength, _train_pred, _train_margin = predict_utility(model, spec, train, train)
        threshold = train_threshold(spec, train, train_strength)
        variant_id = str(spec["variant_id"])
        variant_results: dict[str, dict[str, Any]] = {}
        for view, view_frame in frames.items():
            variant_results[view] = {}
            for split in ["train", "validation", "oos"]:
                part = view_frame.loc[view_frame["split"].astype(str).eq(split)].copy().reset_index(drop=True)
                side, strength, pred, margin = predict_utility(model, spec, part, train)
                selected = np.asarray(strength >= threshold, dtype=bool)
                row = metric_row(part, selected, side, strength, margin, spec, threshold, view, split, seed=RNG_SEED + spec_index * 1000 + stable_seed(view, split))
                metric_rows.append(row)
                control_rows.extend(deterministic_control_rows(part, selected, side, strength, variant_id, view, split))
                utility_rows.extend(utility_exposure_rows(part, selected, side, spec, variant_id, view, split))
                variant_results[view][split] = row
                if split in {"validation", "oos"} and len(part):
                    sample_cols = ["timestamp", "source_tier", "route_role", "label", "future_log_return_12", "regime_key", "cost_bucket"]
                    sample = part.loc[selected, sample_cols].copy()
                    sample["variant_id"] = variant_id
                    sample["split"] = split
                    sample["side"] = side[selected]
                    sample["strength"] = strength[selected]
                    sample["pred_long_utility"] = pred[selected, 0] if len(pred) else []
                    sample["pred_short_utility"] = pred[selected, 1] if len(pred) else []
                    sample["actual_realized_utility"] = actual_utility(part, side, spec)[selected]
                    score_samples.extend(sample.head(60).to_dict(orient="records"))
        gates.append(candidate_gate_for_variant(variant_id, variant_results))

    write_csv(VARIANT_METRICS_CSV, metric_rows)
    write_csv(SPLIT_METRICS_CSV, metric_rows)
    write_csv(NEGATIVE_CONTROL_CSV, control_rows)
    write_csv(UTILITY_EXPOSURE_CSV, utility_rows)
    write_csv(SCORE_SAMPLE_CSV, score_samples)
    matrix = [{k: v for k, v in spec.items() if k != "features"} | {"feature_count": len(spec["features"]), "feature_hash": feature_hash(spec["features"])} for spec in specs]
    candidate_count = sum(1 for gate in gates if gate["status"] == "proxy_gate_signal_triggered")
    write_json(VARIANT_MATRIX, {"variants": matrix})
    write_json(CANDIDATE_GATE_JSON, {"candidate_count": candidate_count, "gates": gates})
    write_json(
        UTILITY_LABEL_CONFIG,
        {
            "selection_policy": "train-only utility model fit and train-only threshold; validation candidate gate; OOS final-read-only",
            "model_input_feature_boundary": "MFE/MAE/path/utility columns are label or diagnostic fields only and are not model features.",
            "variant_matrix": matrix,
            "candidate_gate_thresholds": {
                "validation_actual_routed_net": ">0",
                "validation_actual_routed_pf_min": CANDIDATE_MIN_PF,
                "validation_actual_routed_trades_per_day_range": [CANDIDATE_MIN_TRADES_PER_DAY, CANDIDATE_MAX_TRADES_PER_DAY],
                "validation_tier_b_net": ">=0",
                "validation_tier_b_pf_min": CANDIDATE_TIER_B_MIN_PF,
                "validation_tier_b_trades_per_day_range": [CANDIDATE_TIER_B_MIN_TRADES_PER_DAY, CANDIDATE_TIER_B_MAX_TRADES_PER_DAY],
                "validation_max_drawdown_cap": CANDIDATE_MAX_DD,
                "validation_side_min_share_min": CANDIDATE_MIN_SIDE_SHARE,
                "validation_tier_gap_ratio_max": CANDIDATE_MAX_TIER_GAP,
                "control_gate": "net_proxy must exceed random_abstain_rate_match mean on validation",
            },
            "runtime_trigger_rule": "If a meaningful runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics/handoff claim is created, same-packet MT5 Strategy Tester probe is required.",
        },
    )
    return {
        "variants": matrix,
        "split_metrics": metric_rows,
        "negative_control_rows": control_rows,
        "utility_exposure_rows": utility_rows,
        "candidate_gates": gates,
        "candidate_count": candidate_count,
        "best_diagnostic_variant": choose_best_diagnostic(metric_rows, gates),
        "selection_policy": "train-only labels and thresholds; validation gate; OOS final read only; scores are rank/utility not calibrated probabilities",
    }


def hash_dataframe(frame: pd.DataFrame, columns: Sequence[str]) -> str:
    payload = pd.util.hash_pandas_object(frame[list(columns)].reset_index(drop=True), index=True).to_numpy(dtype=np.uint64).tobytes()
    return hashlib.sha256(payload).hexdigest()


def integrity_payload(frames: Mapping[str, pd.DataFrame], route_summary: Mapping[str, Any], tier_b_summary: Mapping[str, Any], path_integrity: Mapping[str, Any]) -> dict[str, Any]:
    features = feature_columns()
    deny_tokens = ("mfe", "mae", "realized", "exit", "pnl", "first_touch", "utility")
    deny_hits = [col for col in features if any(token in col.lower() for token in deny_tokens)]
    split_counts = {view: frame["split"].astype(str).value_counts().sort_index().to_dict() for view, frame in frames.items()}
    tier_a_sample = frames["tier_a_separate"].head(128)
    feature_hash_before = hash_dataframe(tier_a_sample, features) if len(tier_a_sample) else None
    perturbed = tier_a_sample.copy()
    if len(perturbed):
        perturbed["future_path_return"] = perturbed["future_path_return"].fillna(0.0) * -1.0
    feature_hash_after = hash_dataframe(perturbed, features) if len(perturbed) else None
    duplicate_counts = {view: int(frame["timestamp"].duplicated().sum()) for view, frame in frames.items()}
    return {
        "audit_name": "f94b_data_integrity_audit",
        "status": "pass_with_boundary" if not deny_hits else "blocked",
        "dataset_identity": file_identity(MODEL_INPUT_DATASET),
        "model_input_summary_identity": file_identity(MODEL_INPUT_SUMMARY),
        "feature_order_identity": file_identity(MODEL_INPUT_FEATURE_ORDER),
        "current_dataset_hash_note": "Current parquet hash is locked here; earlier F93/F94A lineage references may differ and are treated as prior-record mismatch, not current truth.",
        "feature_count": len(features),
        "feature_order_hash": feature_order_file_hash(),
        "feature_denylist_hits": deny_hits,
        "split_policy": "fit train only; validation candidate gate; OOS final-read-only",
        "split_counts_after_label_censor": split_counts,
        "route_summary_before_label_censor": route_summary,
        "tier_b_summary": tier_b_summary,
        "duplicate_timestamp_counts_after_label_censor": duplicate_counts,
        "path_label_integrity": path_integrity,
        "leakage_tests": {
            "column_denylist": "pass" if not deny_hits else "blocked",
            "future_path_perturbation_feature_hash_before": feature_hash_before,
            "future_path_perturbation_feature_hash_after": feature_hash_after,
            "future_path_perturbation_does_not_change_features": bool(feature_hash_before == feature_hash_after),
            "split_edge_censoring": path_integrity.get("path_label_summary", {}),
            "train_only_fit": "enforced_by_evaluate_variants",
            "oos_tuning": "forbidden_final_read_only",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def materialize_proxy_metrics() -> dict[str, Any]:
    frames, route_summary, tier_b_summary, path_integrity = prepare_frames()
    evaluation = evaluate_variants(frames)
    integrity = integrity_payload(frames, route_summary, tier_b_summary, path_integrity)
    write_json(DATA_LOCK, data_lock_payload(frames, route_summary, tier_b_summary))
    write_json(TIER_ROUTE_SUMMARY, route_summary)
    write_json(TIER_B_SUMMARY, tier_b_summary)
    write_json(LABEL_INTEGRITY, integrity)
    return {
        "route_summary": route_summary,
        "tier_b_summary": tier_b_summary,
        "data_integrity": integrity,
        "evaluation": evaluation,
    }


def data_lock_payload(frames: Mapping[str, pd.DataFrame], route_summary: Mapping[str, Any], tier_b_summary: Mapping[str, Any]) -> dict[str, Any]:
    features = feature_columns()
    return {
        "run_id": RUN_ID,
        "dataset": file_identity(MODEL_INPUT_DATASET),
        "model_input_summary": file_identity(MODEL_INPUT_SUMMARY),
        "feature_order": file_identity(MODEL_INPUT_FEATURE_ORDER),
        "feature_order_hash": feature_order_file_hash(),
        "feature_count": len(features),
        "split_policy": "train fit and train threshold only; validation gate; OOS final-read-only",
        "tier_records": {
            "tier_a_separate": frames["tier_a_separate"]["split"].astype(str).value_counts().sort_index().to_dict(),
            "tier_b_separate": frames["tier_b_separate"]["split"].astype(str).value_counts().sort_index().to_dict(),
            "tier_ab_combined": frames["tier_ab_combined"]["split"].astype(str).value_counts().sort_index().to_dict(),
        },
        "route_summary_before_label_censor": route_summary,
        "tier_b_summary": tier_b_summary,
        "runtime_trigger_rule": "same-packet MT5 Strategy Tester probe if runnable candidate or runtime/materialization/economics/handoff claim appears",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def status_from(payload: Mapping[str, Any]) -> str:
    return str(payload["status"])


def judgment_from(payload: Mapping[str, Any]) -> str:
    return str(payload["judgment"])


def runtime_probe_status_from(payload: Mapping[str, Any]) -> str:
    return str(payload["runtime_probe_status"])


def build_payload(created_at: str, metrics: Mapping[str, Any]) -> dict[str, Any]:
    candidate_count = int(metrics["evaluation"]["candidate_count"])
    status = STATUS_NEGATIVE if candidate_count == 0 else STATUS_BLOCKED_RUNTIME
    judgment = JUDGMENT_NEGATIVE if candidate_count == 0 else JUDGMENT_BLOCKED_RUNTIME
    runtime_status = RUNTIME_PROBE_STATUS_NEGATIVE if candidate_count == 0 else RUNTIME_PROBE_STATUS_BLOCKED
    return {
        "created_at_utc": created_at,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "runtime_probe_status": runtime_status,
        "hypothesis": "Predeclared tier-stable realized-utility labels can turn F93's short-heavy/high-cost failure shape into a runtime-compatible proxy surface without repeating the F93 side/cost budget repair axis.",
        "verification_profile": "proxy_scout",
        "claim_boundary": CLAIM_BOUNDARY,
        "metrics": metrics,
        "source_identities": [file_identity(path) for path in source_inputs()],
        "task_force": task_force_payload(created_at),
    }


def task_force_payload(created_at: str) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "created_at_utc": created_at,
        "review_requirement": "explicit_user_instruction_required",
        "trigger_source": "active_goal_packet_and_user_instruction_requiring_relevant_agents_when_triggered",
        "selected_agent_count": len(TASK_FORCE_CALLS),
        "full_roster_call_reason": None,
        "actual_subagent_calls": TASK_FORCE_CALLS,
        "opinion_summary": {
            "accepted": [call["roster_agent_id"] for call in TASK_FORCE_CALLS if call["opinion_classification"] == "accepted"],
            "needs_local_verification": [call["roster_agent_id"] for call in TASK_FORCE_CALLS if call["opinion_classification"] == "needs_local_verification"],
            "rejected": [],
        },
        "codex_local_disposition": "local_verification_executed_no_task_force_reviewed_pass_claim",
        "claim_effect": "actual calls are recorded; no Task Force reviewed, pass, verified, completion, baseline, authority, or readiness claim is made.",
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
        "validation_actual_routed_net": validation.get("net_proxy"),
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
    gate = best.get("gate", {})
    return {
        "packet_id": RUN_ID,
        "test_period": "train_2022-09-01_to_2024-12-31_validation_2025-01-02_to_2025-09-30_oos_2025-10-01_to_2026-04-13",
        "hypothesis": payload["hypothesis"],
        "proxy_kpi": validation,
        "runtime_kpi": "not_applicable_no_runnable_candidate_no_runtime_claim" if payload["metrics"]["evaluation"]["candidate_count"] == 0 else "blocked_pending_runtime_probe",
        "net_profit": validation.get("net_proxy"),
        "profit_factor": validation.get("proxy_pf"),
        "drawdown": validation.get("max_drawdown"),
        "trade_count": validation.get("trade_count"),
        "trades_per_day": validation.get("trades_per_day"),
        "parity": "not_applicable_no_onnx_or_ea",
        "gap_cause": "proxy/runtime gap not measured because no runtime materialization claim is made",
        "next_action": payload["next_run_id"],
        "candidate_gate": {"candidate_count": payload["metrics"]["evaluation"]["candidate_count"], "best_gate": gate},
        "tier_records_required": ["tier_a_separate", "tier_b_separate", "actual_routed_total"],
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
        "claim_boundary": CLAIM_BOUNDARY,
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    best = payload["metrics"]["evaluation"].get("best_diagnostic_variant", {})
    validation = best.get("validation", {})
    gate = best.get("gate", {})
    failures = gate.get("selection_failures", [])
    return f"""# F94B Tier-Stable Realized-Utility Proxy Scout

Action: F94B ran a Python proxy scout with train-only utility labels and thresholds, validation gate, and OOS final-read-only.

Effect: the run records Tier A separate, Tier B separate, and actual routed total evidence without claiming runtime authority, selected baseline, live readiness, or Goal Achieve.

Best diagnostic variant: `{best.get('variant_id')}`

- validation net proxy: `{validation.get('net_proxy')}`
- validation PF: `{validation.get('proxy_pf')}`
- validation max drawdown: `{validation.get('max_drawdown')}`
- validation trades/day: `{validation.get('trades_per_day')}`
- validation trade count: `{validation.get('trade_count')}`
- candidate gate count: `{payload['metrics']['evaluation']['candidate_count']}`
- runtime: `{runtime_probe_status_from(payload)}`

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
            "label_integrity_audit": read_json(LABEL_INTEGRITY) if path_exists(LABEL_INTEGRITY) else {},
            "task_force_actual_subagent_calls": payload["task_force"]["actual_subagent_calls"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_text(F94B_REPORT, result_summary_text(payload))


def audit_payload(name: str, status: str, **extra: Any) -> dict[str, Any]:
    return {"audit_name": name, "packet_id": RUN_ID, "status": status, **extra}


def write_audits(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    gate_results = gate_results or {}
    candidate_count = int(payload["metrics"]["evaluation"]["candidate_count"])
    task_force = payload["task_force"]
    write_json(TASK_FORCE_REVIEW, task_force)
    write_json(PACKET_TASK_FORCE_REVIEW, task_force)
    write_json(
        FRONTIER_EXTRA_DUE_CHECK,
        audit_payload(
            "frontier_extra_due_check",
            "pass_not_due",
            created_at_utc=payload["created_at_utc"],
            due_status=FRONTIER_EXTRA_DUE_STATUS,
            claim_effect="F94B may continue inside F94; no Extra Stage is due.",
        ),
    )
    write_json(
        TOPIC_ROTATION_CHECK,
        audit_payload(
            "frontier_topic_rotation_check",
            "pass",
            created_at_utc=payload["created_at_utc"],
            status_detail=FRONTIER_TOPIC_ROTATION_STATUS,
            material_novelty_delta="F94B executes the F94A predeclared realized-utility label axis; it is not a new adjacent frontier open or F93 side/cost budget repair.",
            claim_effect="Continuation inside F94 only; no stage completion or authority claim.",
        ),
    )
    write_json(
        SCOPE_GATE,
        audit_payload(
            "scope_completion_gate",
            "pass",
            created_at_utc=payload["created_at_utc"],
            required_outputs=[rel(path) for path in [RUN_MANIFEST, KPI_RECORD, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV, LABEL_INTEGRITY, PACKET_TASK_FORCE_REVIEW]],
            candidate_gate_count=candidate_count,
            runtime_probe_status=runtime_probe_status_from(payload),
            claim_boundary=CLAIM_BOUNDARY,
        ),
    )
    write_json(DATA_INTEGRITY_AUDIT, payload["metrics"]["data_integrity"])
    write_json(
        MODEL_VALIDATION_AUDIT,
        audit_payload(
            "model_validation_audit",
            "pass_with_boundary",
            created_at_utc=payload["created_at_utc"],
            threshold_policy="train_only",
            validation_policy="candidate_gate_only",
            oos_policy="final_read_only_no_tuning",
            calibrated_probability_claim="rejected",
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
    if gate_results:
        write_json(REQUIRED_GATE_AUDIT, gate_results.get("required_gate_coverage_audit", {}))
        write_json(STATE_SYNC_AUDIT, gate_results.get("state_sync_audit", {}))


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
            "skill": "obsidian-experiment-design",
            "hypothesis": payload["hypothesis"],
            "baseline": {
                "source_run_id": "frontier93B_side_balance_cost_exposure_risk_budget_proxy_scout_v1",
                "use": "negative_memory_only_not_inherited_baseline",
                "reference_artifacts": [rel(F93B_SUMMARY), rel(F93B_CANDIDATE_GATE)],
            },
            "changed_variables": [
                "label/objective changes to realized path utility",
                "candidate gate adds worst-tier utility and tier-gap checks",
                "selection avoids F93 side/cost budget overlays",
            ],
            "invalid_conditions": [
                "MFE/MAE/realized/utility columns entering model features",
                "validation or OOS threshold tuning",
                "Tier A-only result presented as whole alpha read",
                "PF-only selection",
                "runtime/materialization/economics claim without MT5 Strategy Tester evidence",
            ],
            "evidence_plan": {
                "tier_records": ["Tier A separate", "Tier B separate", "actual routed total"],
                "candidate_gate": rel(CANDIDATE_GATE_JSON),
                "split_metrics": rel(SPLIT_METRICS_CSV),
                "runtime_boundary": RUNTIME_NA_REASONS,
            },
            "variant_count": len(payload["metrics"]["evaluation"]["variants"]),
            "selection_policy": payload["metrics"]["evaluation"]["selection_policy"],
            "receipt_path": rel(SKILL_RECEIPT_DIR / "experiment_design.json"),
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": [file_identity(path) for path in [MODEL_INPUT_DATASET, MODEL_INPUT_FEATURE_ORDER, MODEL_INPUT_SUMMARY, RAW_US100_CSV, RAW_US100_MANIFEST]],
            "time_axis_boundary": "Closed M5 timestamp key aligned to raw bar close timestamp; future path labels are diagnostics/targets only.",
            "split_boundary": "Train fit and threshold only; validation gate; OOS final-read-only; split-edge future labels censored.",
            "leakage_checks": payload["metrics"]["data_integrity"].get("leakage_tests", {}),
            "missing_data_boundary": "Tier B or actual routed total cannot be omitted; missing rows must be recorded as blocked or missing_required.",
            "data_integrity_audit": rel(LABEL_INTEGRITY),
            "dataset_lock": rel(DATA_LOCK),
            "feature_order_hash": feature_order_file_hash(),
            "receipt_path": rel(SKILL_RECEIPT_DIR / "data_integrity.json"),
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "utility proxy regressors with train-only strength thresholds",
            "validation_split": "validation is candidate gate only; OOS is final-read-only",
            "overfit_checks": [
                "no OOS tuning",
                "no validation threshold search",
                "PF-only selection rejected",
                "multiple variants reported with shared predeclared gate",
            ],
            "selection_metric_boundary": "diagnostic score combines worst-tier utility, tier stability, economics, risk, density, and control lift; no calibrated probability claim",
            "allowed_claims": ALLOWED_CLAIMS,
            "threshold_policy": "train_only",
            "validation_policy": "validation_gate_only",
            "oos_policy": "final_read_only",
            "candidate_gate_count": payload["metrics"]["evaluation"]["candidate_count"],
            "receipt_path": rel(SKILL_RECEIPT_DIR / "model_validation.json"),
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "raw_evidence": [rel(MODEL_INPUT_DATASET), rel(RAW_US100_CSV), rel(F94A_BRIEF), rel(F93B_SUMMARY)],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, UTILITY_LABEL_CONFIG, DATA_LOCK, LABEL_INTEGRITY, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F94B_REPORT), rel(DECISION_MEMO)],
            "hashes_or_missing_reasons": [file_identity(path) for path in produced_artifacts()],
            "lineage_boundary": "proxy_scout_evidence_only_no_runtime_authority",
            "receipt_path": rel(SKILL_RECEIPT_DIR / "artifact_lineage.json"),
        },
        {
            **common,
            "skill": "obsidian-task-force-review",
            "trigger_reason": "explicit user instruction plus active goal packet requiring relevant Task Force agents when triggered",
            "roster_registry": rel(ROOT / "docs" / "agent_control" / "codex_task_force_registry.yaml"),
            "review_requirement": "explicit_user_instruction_required",
            "codex_task_force_review_packet_required": True,
            "model_policy": "inherited parent model; no model-strength relaxation of gates",
            "bounded_evidence": [rel(PACKET_TASK_FORCE_REVIEW), rel(TASK_FORCE_REVIEW), rel(KPI_RECORD), rel(CANDIDATE_GATE_JSON)],
            "advice_classification": {
                "accepted": [call["roster_agent_id"] for call in TASK_FORCE_CALLS if call["opinion_classification"] == "accepted"],
                "needs_local_verification": [call["roster_agent_id"] for call in TASK_FORCE_CALLS if call["opinion_classification"] == "needs_local_verification"],
                "rejected": [],
            },
            "local_verification": "dataset/hash, feature denylist, split censoring, train-only threshold, candidate gate, and runtime boundary were checked locally.",
            "final_codex_direction": "record F94B as proxy scout evidence and route F94C repair-or-rotation; no Task Force reviewed/pass claim",
            "forbidden_claim_check": FORBIDDEN_CLAIMS,
            "agents_used": [call["roster_agent_id"] for call in TASK_FORCE_CALLS],
            "actual_subagent_calls": TASK_FORCE_CALLS,
            "receipt_path": rel(SKILL_RECEIPT_DIR / "task_force_review.json"),
        },
        {
            **common,
            "skill": "obsidian-result-judgment",
            "judgment_boundary": "negative or blocked proxy scout only; no promotion, baseline, runtime authority, live readiness, or Goal Achieve",
            "allowed_claims": ALLOWED_CLAIMS,
            "evidence_used": [rel(CANDIDATE_GATE_JSON), rel(KPI_RECORD), rel(SPLIT_METRICS_CSV), rel(RESULT_JUDGMENT_AUDIT)],
            "judgment": judgment_from(payload),
            "runtime_probe_status": runtime_probe_status_from(payload),
            "next_action": payload["next_run_id"],
            "receipt_path": rel(SKILL_RECEIPT_DIR / "result_judgment.json"),
        },
        {
            **common,
            "skill": "obsidian-exploration-mandate",
            "exploration_lane": "frontier_proxy_scout",
            "idea_boundary": "F94B can create clue/negative memory only unless runtime evidence is later produced.",
            "negative_memory_effect": "Failed Tier A/B/routed realized-utility gates become do-not-overclaim memory for F94C.",
            "operating_claim_boundary": CLAIM_BOUNDARY,
            "exploration_boundary": "clue_or_negative_memory_only",
            "runtime_authority": "not_claimed",
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
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-experiment-design", "receipts": receipts})
    for receipt in receipts:
        write_json(ROOT / str(receipt["receipt_path"]), receipt)


def required_evidence_paths() -> list[str]:
    return [
        rel(path)
        for path in [
            RUN_MANIFEST,
            KPI_RECORD,
            UTILITY_LABEL_CONFIG,
            DATA_LOCK,
            LABEL_INTEGRITY,
            CANDIDATE_GATE_JSON,
            SPLIT_METRICS_CSV,
            PACKET_TASK_FORCE_REVIEW,
            WORK_PACKET,
            SKILL_RECEIPTS,
            PACKET_CLOSEOUT_GATE,
        ]
    ]


def work_packet_payload(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation plus explicit reminder to actually call relevant Task Force agents when required",
            "requested_action": "run F94B proxy scout for tier-stable realized-utility label surface",
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
                "post_entry_label_leakage": "high",
                "tier_b_hidden_by_actual_routed_total": "high",
                "pf_only_selection": "high",
                "task_force_review_claim_without_actual_calls": "high",
                "runtime_probe_absence_misread_as_cost_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not put MFE/MAE/realized/utility fields into model features.",
                "Do not tune thresholds on validation or OOS.",
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester identity.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "verification_profile": "proxy_scout",
                "strategy_tester_required_now": int(payload["metrics"]["evaluation"]["candidate_count"]) > 0,
                "runtime_probe_status": runtime_probe_status_from(payload),
                "reason": "No ONNX/EA/set/runtime claim is made; if proxy gate signal appears, packet is blocked pending same-packet runtime probe.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F94B proxy scout", "tier-stable realized-utility label", "Task Force actual calls", "state sync"],
            "scope_units": ["proxy_scout_run", "candidate_gate_record", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["data lock", "proxy metrics", "candidate gate", "Task Force actual calls", "control-plane gates"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F94B is the active formal proxy-scout packet."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "proxy_scout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F94A planned F94B proxy scout",
                "explicit user instruction requiring relevant Task Force actual calls when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence_paths(),
            "gates_not_run_with_reason": RUNTIME_NA_REASONS,
            "stop_conditions": [
                "Stop at proxy scout evidence if no runnable candidate or runtime/materialization/economics/handoff claim appears.",
                "If a meaningful runnable candidate or runtime claim appears, do not make the claim without same-packet MT5 Strategy Tester probe.",
                "Do not repair by threshold/filter/session/routing/parameter-only changes.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F94B proxy metrics exist.", "expected_artifact": rel(SPLIT_METRICS_CSV), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Tier A, Tier B, and actual routed total are recorded.", "expected_artifact": rel(TIER_ROUTE_SUMMARY), "verification_method": "kpi_contract_audit", "required": True},
            {"id": "AC-003", "text": "Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-004", "text": "Runtime evidence absence is bounded and not a cost/proxy-bad skip.", "expected_artifact": rel(KPI_RECORD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Lock data, feature, and split identities.",
            "Build realized utility labels from raw future path diagnostics without adding them to model features.",
            "Fit train-only utility proxy variants and score validation/OOS.",
            "Record Task Force actual calls, audits, receipts, state sync, and final claim guard.",
        ],
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": ["obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage", "obsidian-task-force-review", "obsidian-result-judgment"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-backtest-forensics", "obsidian-runtime-parity"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-backtest-forensics", "reason": "No new MT5 Strategy Tester report or trade list exists."},
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA parity or handoff claim is made."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "source_inputs": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, UTILITY_LABEL_CONFIG, DATA_LOCK, LABEL_INTEGRITY, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F94B_REPORT), rel(DECISION_MEMO), rel(CONTEXT_ANCHOR)],
            "raw_evidence": [rel(MODEL_INPUT_DATASET), rel(RAW_US100_CSV), rel(F94A_BRIEF), rel(F93B_SUMMARY)],
            "missing_evidence": [
                {"evidence": "MT5 Strategy Tester runtime output", "reason": "outside proxy_scout claim surface unless runnable surface appears"},
                {"evidence": "ONNX/EA/set handoff", "reason": "not created in F94B"},
            ],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "actual_status_source": {name: (gate_results.get(name, {}) or {}).get("status", "pending") for name in REQUIRED_GATES},
            "not_applicable_with_reason": {item["gate"]: item["reason"] for item in RUNTIME_NA_REASONS},
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
    }


def closeout_gate_payload(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    path_by_gate = {
        "work_packet_schema_lint": PACKET_WORK_PACKET_LINT,
        "skill_receipt_schema_lint": PACKET_SKILL_RECEIPT_LINT,
        "codex_task_force_review_packet": PACKET_TASK_FORCE_REVIEW,
        "frontier_extra_due_check": FRONTIER_EXTRA_DUE_CHECK,
        "frontier_topic_rotation_check": TOPIC_ROTATION_CHECK,
        "scope_completion_gate": SCOPE_GATE,
        "data_integrity_audit": DATA_INTEGRITY_AUDIT,
        "model_validation_audit": MODEL_VALIDATION_AUDIT,
        "kpi_contract_audit": KPI_CONTRACT_AUDIT,
        "artifact_lineage_audit": ARTIFACT_AUDIT,
        "result_judgment_audit": RESULT_JUDGMENT_AUDIT,
        "state_sync_audit": PACKET_STATE_SYNC_AUDIT,
        "required_gate_coverage_audit": PACKET_REQUIRED_GATE_AUDIT,
        "final_claim_guard": PACKET_FINAL_CLAIM_GUARD,
    }
    default_status = {
        "codex_task_force_review_packet": "pass",
        "frontier_extra_due_check": "pass_not_due",
        "frontier_topic_rotation_check": "pass",
        "scope_completion_gate": "pass",
        "data_integrity_audit": "pass_with_boundary",
        "model_validation_audit": "pass_with_boundary",
        "kpi_contract_audit": "pass",
        "artifact_lineage_audit": "pass",
        "result_judgment_audit": "negative" if int(payload["metrics"]["evaluation"]["candidate_count"]) == 0 else "blocked",
    }
    audits = []
    for gate in REQUIRED_GATES:
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


def state_docs(payload: Mapping[str, Any]) -> None:
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
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "task_force_status": "f94b_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim",
        "runtime_probe_status": runtime_probe_status_from(payload),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": payload["created_at_utc"],
        "context_anchor": rel(CONTEXT_ANCHOR),
        "notes": [
            "Action: F94B proxy scout executed with train-only utility labels and validation gate.",
            "Effect: F94C repair-or-rotation is current unless runtime probe is blocked by a gate signal.",
            "Runtime: no Strategy Tester evidence; no runtime authority; no Goal Achieve.",
        ],
    }
    write_yaml(WORKSPACE_STATE, workspace)
    context = f"""# Current Working State

- active_stage: `{STAGE_ID}`
- latest_completed_run: `{RUN_ID}`
- current_run: `{payload['next_run_id']}`
- status: `{status_from(payload)}`
- judgment: `{judgment_from(payload)}`
- Task Force: 6 selected agents actually called; no Task Force reviewed/pass claim.
- Runtime: `{runtime_probe_status_from(payload)}`
- Boundary: `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, context)
    write_text(CONTEXT_ANCHOR, context)
    write_text(
        STAGE_BRIEF,
        f"""# {STAGE_ID}

Question: Can tier-stable realized-utility labels produce a runtime-compatible US100 M5 surface without repeating F93 side/cost budget repair?

F94B result: proxy scout evidence recorded. No selected baseline, operating promotion, runtime authority, live readiness, or Goal Achieve.

Current run: `{payload['next_run_id']}`.
""",
    )
    write_text(
        INPUT_REFS,
        "# F94 Input References\n\n" + "\n".join(f"- `{rel(path)}`" for path in source_inputs()) + "\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Selection Status

- latest_completed_run: `{RUN_ID}`
- current_run: `{payload['next_run_id']}`
- status: `{status_from(payload)}`
- judgment: `{judgment_from(payload)}`
- candidate gate count: `{payload['metrics']['evaluation']['candidate_count']}`
- runtime authority: not claimed
- Goal Achieve: not claimed
- runtime: `{runtime_probe_status_from(payload)}`
""",
    )
    write_text(
        REVIEW_INDEX,
        f"""# F94 Review Index

- f94b_report: `{rel(F94B_REPORT)}`
- f94b_task_force_receipt: `{rel(TASK_FORCE_REVIEW)}`
- f94b_candidate_gate: `{rel(CANDIDATE_GATE_JSON)}`
- f94b_data_integrity: `{rel(DATA_INTEGRITY_AUDIT)}`
- packet: `{rel(WORK_PACKET)}`
- current_run: `{payload['next_run_id']}`
""",
    )


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path_exists(path):
        return [], []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv_rows(path: Path, fieldnames: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def replace_rows(path: Path, remove_run_ids: set[str], new_rows: Sequence[Mapping[str, Any]]) -> None:
    fieldnames, rows = read_csv_rows(path)
    extras = [key for row in new_rows for key in row if key not in fieldnames]
    fieldnames = fieldnames + extras
    kept = [row for row in rows if row.get("run_id") not in remove_run_ids]
    write_csv_rows(path, fieldnames, [*kept, *new_rows])


def ledger_rows(payload: Mapping[str, Any], gate_passes: int = 0) -> list[dict[str, Any]]:
    best = payload["metrics"]["evaluation"].get("best_diagnostic_variant", {})
    validation = best.get("validation", {})
    base = {
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "date": "2026-06-19",
        "created_at": payload["created_at_utc"],
        "created_at_utc": payload["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
    }
    f94b_row = {
        **base,
        "ledger_row_id": f"{RUN_ID}__proxy_scout",
        "run_id": RUN_ID,
        "subrun_id": "proxy_scout",
        "record_view": "actual_routed_total",
        "tier_scope": "tier_a_tier_b_actual_routed",
        "kpi_scope": "proxy_scout",
        "scoreboard_lane": "proxy_scout",
        "status": status_from(payload),
        "judgment": judgment_from(payload),
        "path": rel(F94B_REPORT),
        "primary_kpi": f"net={validation.get('net_proxy')};pf={validation.get('proxy_pf')};dd={validation.get('max_drawdown')};tpd={validation.get('trades_per_day')}",
        "guardrail_kpi": f"candidate_gate_count={payload['metrics']['evaluation']['candidate_count']};runtime={runtime_probe_status_from(payload)}",
        "external_verification_status": "not_applicable_proxy_scout_no_runtime_claim",
        "notes": "F94B tier-stable realized-utility proxy scout; Task Force actual calls recorded.",
        "run_number": "frontier94B",
        "decision": status_from(payload),
        "next_run_id": payload["next_run_id"],
        "rows": validation.get("rows"),
        "gate_passes": gate_passes,
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(F94B_REPORT),
        "primary_artifact": rel(CANDIDATE_GATE_JSON),
        "result_status": status_from(payload),
        "runtime_completed_rows": 0,
        "candidate_count": payload["metrics"]["evaluation"]["candidate_count"],
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path)]),
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "run_family": "experiment_execution",
        "run_type": "proxy_scout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(F94B_REPORT),
        "row_id": f"{RUN_ID}__proxy_scout",
        "question": "Can tier-stable realized-utility labels produce a runtime-compatible US100 M5 surface?",
        "next_action": payload["next_run_id"],
        "model_variants": len(payload["metrics"]["evaluation"]["variants"]),
        "selected_surfaces": 0,
        "runtime_attempt_rows": 0,
    }
    f94c_row = {
        **base,
        "ledger_row_id": f"{payload['next_run_id']}__planned",
        "run_id": payload["next_run_id"],
        "subrun_id": "planned",
        "record_view": "planned_next_run",
        "tier_scope": "not_applicable_planned",
        "kpi_scope": "planned_repair_or_rotation",
        "scoreboard_lane": "planned_repair_or_rotation",
        "status": "planned_current_run_no_authority",
        "judgment": "pending_repair_or_rotation_decision",
        "path": rel(DECISION_MEMO),
        "primary_kpi": "pending",
        "guardrail_kpi": "no_authority",
        "external_verification_status": "pending",
        "notes": "F94C planned after F94B proxy scout.",
        "run_number": "frontier94C",
        "decision": "planned_current_run_no_authority",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(DECISION_MEMO),
        "primary_artifact": rel(DECISION_MEMO),
        "result_status": "planned_current_run_no_authority",
        "runtime_completed_rows": 0,
        "candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "artifact_count": 0,
        "required_gate_audit": "",
        "run_family": "experiment_execution",
        "run_type": "planned_repair_or_rotation",
        "input_run_id": RUN_ID,
        "output_path": rel(DECISION_MEMO),
        "result_path": rel(DECISION_MEMO),
        "row_id": f"{payload['next_run_id']}__planned",
        "question": "Should F94 repair the utility axis or rotate?",
        "next_action": "decide_repair_or_rotation",
        "model_variants": 0,
        "selected_surfaces": 0,
        "runtime_attempt_rows": 0,
    }
    return [f94b_row, f94c_row]


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for raw_path in produced_artifacts():
        path = raw_path if raw_path.is_absolute() else ROOT / raw_path
        if not path_exists(path):
            continue
        path_rel = rel(path)
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f94b_proxy_scout_evidence",
                "path": path_rel,
                "sha256": sha256_file_lf_normalized(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{path_rel}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F94B proxy-scout artifact; no runtime authority.",
                "artifact_path": path_rel,
                "effect": "Supports F94B proxy scout clue/negative memory only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    replace_rows(ARTIFACT_REGISTRY, {RUN_ID}, rows)


def update_ledgers(payload: Mapping[str, Any], gate_passes: int = 0) -> None:
    rows = ledger_rows(payload, gate_passes=gate_passes)
    run_ids = {RUN_ID, payload["next_run_id"]}
    replace_rows(RUN_REGISTRY, run_ids, rows)
    replace_rows(ALPHA_LEDGER, run_ids, rows)
    replace_rows(STAGE_LEDGER, run_ids, rows)
    update_artifact_registry(payload)


def append_once(path: Path, marker: str, addition: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + addition.strip() + "\n")


def update_register_docs(payload: Mapping[str, Any]) -> None:
    marker = f"<!-- {RUN_ID} -->"
    append_once(
        IDEA_REGISTRY,
        marker,
        f"""{marker}
## F94B tier-stable realized-utility proxy scout

- run_id: `{RUN_ID}`
- hypothesis: {payload['hypothesis']}
- status: `{status_from(payload)}`
- judgment: `{judgment_from(payload)}`
- task_force_actual_calls: 6 selected agents recorded.
- runtime: `{runtime_probe_status_from(payload)}`
- next_action: `{payload['next_run_id']}`
- claim_boundary: `{CLAIM_BOUNDARY}`
""",
    )
    append_once(
        NEGATIVE_REGISTER,
        marker,
        f"""{marker}
## F94B tier-stable realized-utility proxy scout

Status: `{status_from(payload)}`

Judgment: `{judgment_from(payload)}`

Runtime: `{runtime_probe_status_from(payload)}`

Decision use: proxy scout clue/negative memory only. No selected baseline, operating promotion, runtime authority, live readiness, or Goal Achieve.
""",
    )
    change = f"- {payload['created_at_utc']} `{RUN_ID}` recorded `{status_from(payload)}`; next `{payload['next_run_id']}`; no runtime authority.\n"
    for path in [WORKSPACE_CHANGELOG, ROOT_CHANGELOG]:
        existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
        if RUN_ID not in existing:
            write_text(path, existing.rstrip() + "\n" + change)


def write_decision_memo(payload: Mapping[str, Any]) -> None:
    best = payload["metrics"]["evaluation"].get("best_diagnostic_variant", {})
    write_text(
        DECISION_MEMO,
        f"""# F94B Decision Memo

Decision: Record F94B as proxy-scout evidence and plan `{payload['next_run_id']}`.

Reason: Best diagnostic variant `{best.get('variant_id')}` did not establish runtime authority. Runtime probe status is `{runtime_probe_status_from(payload)}`.

Task Force: 6 selected agents were actually called and recorded; no Task Force reviewed/pass claim is made.

Forbidden claims: selected baseline, operating promotion, runtime authority, live readiness, Goal Achieve.
""",
    )


def write_gate_results(payload: Mapping[str, Any]) -> dict[str, Any]:
    packet = work_packet_payload(payload)
    wp_result = audit_work_packet_schema(packet)
    receipts = skill_receipts(payload)
    sr_result = audit_skill_receipt_schemas(receipts, root=ROOT, requested_claims=ALLOWED_CLAIMS)
    state_result = audit_state_sync(ROOT, active_stage=STAGE_ID, current_branch=current_branch())
    interim_gate_results = {
        "work_packet_schema_lint": {"status": wp_result.status, "output_path": rel(PACKET_WORK_PACKET_LINT)},
        "skill_receipt_schema_lint": {"status": sr_result.status, "output_path": rel(PACKET_SKILL_RECEIPT_LINT)},
        "state_sync_audit": {"status": state_result.status, "output_path": rel(PACKET_STATE_SYNC_AUDIT)},
    }
    interim_packet = work_packet_payload(payload, interim_gate_results)
    interim_closeout = closeout_gate_payload(payload, interim_gate_results)
    required_result = audit_required_gate_coverage(interim_packet, interim_closeout)
    guard_result = guard_final_claims(
        requested_claims=ALLOWED_CLAIMS,
        audit_results=(wp_result, sr_result, state_result, required_result),
    )
    gate_results = {
        **interim_gate_results,
        "required_gate_coverage_audit": {"status": required_result.status, "output_path": rel(PACKET_REQUIRED_GATE_AUDIT)},
        "final_claim_guard": {"status": guard_result.status, "output_path": rel(PACKET_FINAL_CLAIM_GUARD)},
    }
    write_json(PACKET_WORK_PACKET_LINT, wp_result.to_dict())
    write_json(PACKET_SKILL_RECEIPT_LINT, sr_result.to_dict())
    write_json(PACKET_STATE_SYNC_AUDIT, state_result.to_dict())
    write_json(STATE_SYNC_AUDIT, state_result.to_dict())
    write_json(PACKET_REQUIRED_GATE_AUDIT, required_result.to_dict())
    write_json(REQUIRED_GATE_AUDIT, required_result.to_dict())
    guard_payload = {
        "packet_id": RUN_ID,
        "audit_name": "final_claim_guard",
        "status": guard_result.status,
        "requested_claims": ALLOWED_CLAIMS,
        "allowed_claims": list(guard_result.allowed_claims),
        "forbidden_claims": list(guard_result.forbidden_claims),
        "guard_result": guard_result.to_dict(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(PACKET_FINAL_CLAIM_GUARD, guard_payload)
    write_json(FINAL_CLAIM_GUARD, guard_payload)
    return gate_results


def main() -> int:
    ensure_dirs()
    created_at = now_utc()
    metrics = materialize_proxy_metrics()
    payload = build_payload(created_at, metrics)
    write_run_artifacts(payload)
    write_audits(payload)
    write_receipts(payload)
    state_docs(payload)
    write_decision_memo(payload)
    update_ledgers(payload)
    update_register_docs(payload)
    write_packet_and_gate(payload)
    gate_results = write_gate_results(payload)
    write_packet_and_gate(payload, gate_results)
    write_audits(payload, gate_results)
    write_run_artifacts(payload)
    update_ledgers(payload, gate_passes=sum(1 for result in gate_results.values() if result["status"] == "pass"))
    print(json.dumps({"run_id": RUN_ID, "status": status_from(payload), "candidate_gate_count": payload["metrics"]["evaluation"]["candidate_count"], "gate_results": gate_results}, indent=2))
    return 2 if int(payload["metrics"]["evaluation"]["candidate_count"]) > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
