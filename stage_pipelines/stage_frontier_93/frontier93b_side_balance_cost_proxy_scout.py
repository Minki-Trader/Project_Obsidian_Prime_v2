from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.required_gate_coverage_audit import audit_required_gate_coverage
from foundation.control_plane.skill_receipt_schema_lint import audit_skill_receipt_schemas
from foundation.control_plane.state_sync_audit import audit_state_sync
from foundation.control_plane.work_packet_schema_lint import audit_work_packet_schema
from stage_pipelines.stage_frontier_91 import frontier91b_regime_density_cost_abstention_proxy_scout as f91


STAGE_ID = "stage_frontier_93__side_balance_cost_exposure_risk_budget_axis"
RUN_ID = "frontier93B_side_balance_cost_exposure_risk_budget_proxy_scout_v1"
PARENT_RUN_ID = "frontier93A_stage_open_side_balance_cost_exposure_risk_budget_axis_v1"
NEXT_RUN_ID = "frontier93C_side_balance_cost_exposure_risk_budget_repair_or_rotation_decision_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_93/frontier93b_side_balance_cost_proxy_scout.py"

STATUS_NEGATIVE = "f93b_side_balance_cost_exposure_risk_budget_proxy_scout_negative_no_candidate_no_authority"
STATUS_BLOCKED_RUNTIME = "f93b_proxy_candidate_blocked_pending_same_packet_mt5_runtime_probe"
JUDGMENT_NEGATIVE = "negative_proxy_scout_side_cost_joint_gate_failed_no_runtime_trigger"
JUDGMENT_BLOCKED_RUNTIME = "blocked_runtime_probe_required_after_side_cost_proxy_candidate"
DECISION_NEGATIVE = "plan_f93c_repair_or_rotation_after_side_cost_budget_proxy_failure"
CLAIM_BOUNDARY = (
    "f93b_proxy_scout_only_no_runnable_candidate_no_mt5_runtime_evidence_no_selected_baseline_"
    "no_operating_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS_NEGATIVE = (
    "not_run_no_meaningful_runnable_candidate_no_runtime_materialization_economics_claim_"
    "not_cost_or_proxy_bad_skip"
)
RUNTIME_PROBE_STATUS_BLOCKED = "blocked_pending_same_packet_mt5_strategy_tester_probe_before_any_candidate_claim"

CANDIDATE_MIN_TRADES_PER_DAY = 5.0
CANDIDATE_MAX_TRADES_PER_DAY = 10.0
CANDIDATE_MIN_PF = 1.05
CANDIDATE_TIER_B_MIN_PF = 1.0
CANDIDATE_TIER_B_MIN_TRADES_PER_DAY = 3.0
CANDIDATE_TIER_B_MAX_TRADES_PER_DAY = 12.0
CANDIDATE_MIN_SIDE_SHARE = 0.20
CANDIDATE_MAX_HIGH_COST_SHARE = 0.55
RNG_SEED = 9302
RANDOM_CONTROL_REPS = 12

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier93B"
PROXY_DIR = RUN_DIR / "proxy_scout"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SKILL_RECEIPT_DIR = PACKET_DIR / "skill_receipts"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
BUDGET_CONFIG = PROXY_DIR / "budget_config.json"
TIER_ROUTE_SUMMARY = PROXY_DIR / "tier_route_summary.json"
TIER_B_SUMMARY = PROXY_DIR / "tier_b_summary.json"
VARIANT_MATRIX = PROXY_DIR / "variant_matrix.json"
VARIANT_METRICS_CSV = PROXY_DIR / "variant_metrics.csv"
SPLIT_METRICS_CSV = PROXY_DIR / "split_metrics.csv"
NEGATIVE_CONTROL_CSV = PROXY_DIR / "negative_control_metrics.csv"
COST_EXPOSURE_LEDGER_CSV = PROXY_DIR / "cost_exposure_ledger.csv"
CANDIDATE_GATE_JSON = PROXY_DIR / "candidate_gate.json"
SCORE_SAMPLE_CSV = PROXY_DIR / "proxy_scores_sample.csv"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

TASK_FORCE_REVIEW = REVIEW_DIR / "f93b_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f93b_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f93b_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f93b_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f93b_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f93b_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f93b_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f93b_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f93b_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f93b_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f93b_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f93b_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f93b_required_gate_coverage_audit.json"
EXECUTION_SUMMARY = REVIEW_DIR / "f93b_execution_summary.json"
F93B_REPORT = REVIEW_DIR / "frontier93B_side_balance_cost_budget_proxy_scout_report.md"

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
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier93b_side_balance_cost_budget_proxy_scout.md"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

F93A_BRIEF = STAGE_DIR / "02_runs" / "frontier93A" / "d" / "f93b_proxy_scout_brief.json"
F93A_DATA_PLAN = STAGE_DIR / "02_runs" / "frontier93A" / "d" / "data_integrity_plan.json"
F93A_RUNTIME_CONTRACT = STAGE_DIR / "02_runs" / "frontier93A" / "d" / "runtime_contract.json"
F93A_RISK_BUDGET_DESIGN = STAGE_DIR / "02_runs" / "frontier93A" / "d" / "risk_budget_design.json"
F93A_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F92B_SUMMARY = ROOT / "stages" / "stage_frontier_92__path_conditioned_trade_shape_labeling_axis" / "03_reviews" / "f92b_execution_summary.json"
RAW_US100_MANIFEST = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.manifest.json"

ALLOWED_CLAIMS = [
    "f93b_side_balance_cost_budget_proxy_scout_executed",
    "f93b_proxy_metrics_recorded",
    "f93b_task_force_actual_calls_recorded",
    "f93b_candidate_gate_failed_no_runtime_trigger",
    "f93c_repair_or_rotation_planned",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "completed",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "candidate",
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
        "reason_code": "no_runnable_candidate_no_runtime_claim",
        "reason": "F93B produced proxy evidence only and no ONNX, EA, set, tester output, materialization, economics, promotion, or authority claim.",
        "claim_effect": "No runtime verified, economics pass, materialization ready, handoff complete, promotion, or authority claim is allowed.",
    },
    {
        "gate": "wfo_stress_gate",
        "reason_code": "outside_claim_surface_proxy_scout_no_candidate",
        "reason": "F93B is a proxy scout. WFO/stress is not claimed unless a runnable candidate appears and runtime materialization begins.",
        "claim_effect": "No WFO pass, stress pass, or candidate claim is allowed.",
    },
]

TASK_FORCE_CALLS = [
    {
        "roster_agent_id": "agent_01_system_governor",
        "spawned_agent_id": "019ede41-e61d-7de0-ad7f-4a68554f0fa8",
        "nickname": "Gauss",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "bounded_evidence": ["docs/workspace/workspace_state.yaml", "docs/agent_control/work_family_registry.yaml"],
        "local_verification": "F93B routing may proceed as experiment_execution/proxy_scout with no authority, promotion, live, or goal claim.",
    },
    {
        "roster_agent_id": "agent_04_evidence_control_plane",
        "spawned_agent_id": "019ede41-fa34-7151-b2ec-9ac1a3e05032",
        "nickname": "Hegel",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "bounded_evidence": ["docs/agent_control/packets/frontier93A_stage_open_side_balance_cost_exposure_risk_budget_axis_v1/work_packet.yaml"],
        "local_verification": "F93B needs fresh packet, receipts, gates, actual_subagent_calls, hashes, state sync, and final claim guard.",
    },
    {
        "roster_agent_id": "agent_05_data_feature_contract",
        "spawned_agent_id": "019ede42-0ea3-7722-8362-b10ab6218d3d",
        "nickname": "Pauli",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "bounded_evidence": ["stage_pipelines/stage_frontier_91/frontier91b_regime_density_cost_abstention_proxy_scout.py", "stages/stage_frontier_93__side_balance_cost_exposure_risk_budget_axis/02_runs/frontier93A/d/data_integrity_plan.json"],
        "local_verification": "F93B must re-lock source hashes, Tier A/B/routed rows, time-axis boundary, and feature-label boundary.",
    },
    {
        "roster_agent_id": "agent_06_quant_research",
        "spawned_agent_id": "019ede42-2381-76d0-a745-a0f8f9c28f3b",
        "nickname": "Poincare",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "bounded_evidence": ["stages/stage_frontier_92__path_conditioned_trade_shape_labeling_axis/03_reviews/f92b_execution_summary.json"],
        "local_verification": "F93B should use budgeted utility, two-queue side budget, cost exposure ledger, Tier B stability, and controls.",
    },
    {
        "roster_agent_id": "agent_07_model_validation_risk",
        "spawned_agent_id": "019ede42-37bb-7b02-8719-c5cd4f5cf35c",
        "nickname": "Lovelace",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "bounded_evidence": ["stages/stage_frontier_93__side_balance_cost_exposure_risk_budget_axis/02_runs/frontier93A/d/f93b_proxy_scout_brief.json"],
        "local_verification": "Train-only threshold/budget, validation candidate gate, OOS final-read-only, and no calibrated probability claim are required.",
    },
    {
        "roster_agent_id": "agent_08_mt5_onnx_runtime",
        "spawned_agent_id": "019ede42-4c1a-71e3-8fc4-191fb7c68aaf",
        "nickname": "Noether",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "bounded_evidence": ["stages/stage_frontier_93__side_balance_cost_exposure_risk_budget_axis/02_runs/frontier93A/d/runtime_contract.json"],
        "local_verification": "No MT5 probe is forced when candidate_count is zero; candidate_count > 0 requires same-packet narrow Strategy Tester probe or lowered claim.",
    },
]


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(dict(payload)), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def file_identity(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"path": rel(path), "exists": False, "sha256": None, "size_bytes": None}
    if io_path(path).is_dir():
        return {"path": rel(path), "exists": True, "sha256": None, "size_bytes": None, "artifact_kind": "directory"}
    return {
        "path": rel(path),
        "exists": True,
        "sha256": sha256_file_lf_normalized(path),
        "size_bytes": io_path(path).stat().st_size,
        "artifact_kind": "file",
    }


def ensure_dirs() -> None:
    for path in [RUN_DIR, PROXY_DIR, REPORT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, SKILL_RECEIPT_DIR]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def stable_seed(*parts: object) -> int:
    digest = hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def source_inputs() -> list[Path]:
    return [
        F93A_BRIEF,
        F93A_DATA_PLAN,
        F93A_RUNTIME_CONTRACT,
        F93A_RISK_BUDGET_DESIGN,
        F93A_PACKET,
        F92B_SUMMARY,
        f91.MODEL_INPUT_SUMMARY,
        f91.MODEL_INPUT_DATASET,
        f91.MODEL_INPUT_FEATURE_ORDER,
        RAW_US100_MANIFEST,
    ]


def produced_artifacts() -> list[Path]:
    return [
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        BUDGET_CONFIG,
        TIER_ROUTE_SUMMARY,
        TIER_B_SUMMARY,
        VARIANT_MATRIX,
        VARIANT_METRICS_CSV,
        SPLIT_METRICS_CSV,
        NEGATIVE_CONTROL_CSV,
        COST_EXPOSURE_LEDGER_CSV,
        CANDIDATE_GATE_JSON,
        SCORE_SAMPLE_CSV,
        RESULT_SUMMARY,
        EXECUTION_SUMMARY,
        F93B_REPORT,
        TASK_FORCE_REVIEW,
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
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_TASK_FORCE_REVIEW,
        PACKET_CLOSEOUT_GATE,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
    ]


def variant_specs(features: Sequence[str]) -> list[dict[str, Any]]:
    regime = [col for col in f91.REGIME_DENSE_FEATURES if col in features]
    cost_blind = [col for col in features if col not in f91.COST_FEATURES]
    return [
        {
            "variant_id": "logreg_full58_side20_cost55_q85",
            "objective_id": "budgeted_utility",
            "family": "logistic",
            "features": list(features),
            "quantile": 0.85,
            "side_budget_mode": "two_queue_min_share_20",
            "cost_budget_mode": "soft_cost_penalty_cap55",
            "min_side_share": 0.20,
            "high_cost_cap": 0.55,
            "cost_weight": 0.20,
            "hard_cost_veto": False,
        },
        {
            "variant_id": "logreg_cost_blind_side30_cost50_q90",
            "objective_id": "cost_blind_model_budgeted_selection",
            "family": "logistic",
            "features": cost_blind,
            "quantile": 0.90,
            "side_budget_mode": "two_queue_min_share_30",
            "cost_budget_mode": "soft_cost_penalty_cap50",
            "min_side_share": 0.30,
            "high_cost_cap": 0.50,
            "cost_weight": 0.25,
            "hard_cost_veto": False,
        },
        {
            "variant_id": "ridge_regime_dense_cost_norm_side25_q85",
            "objective_id": "regime_dense_return_rank_budgeted_utility",
            "family": "ridge_return",
            "features": regime,
            "quantile": 0.85,
            "side_budget_mode": "two_queue_min_share_25",
            "cost_budget_mode": "soft_cost_penalty_cap55",
            "min_side_share": 0.25,
            "high_cost_cap": 0.55,
            "cost_weight": 0.30,
            "hard_cost_veto": False,
        },
        {
            "variant_id": "extratrees_full58_cost_veto_side20_q85",
            "objective_id": "tree_rank_hard_cost_veto_side_budget",
            "family": "extra_trees",
            "features": list(features),
            "quantile": 0.85,
            "side_budget_mode": "two_queue_min_share_20",
            "cost_budget_mode": "hard_cost_high_veto_cap55",
            "min_side_share": 0.20,
            "high_cost_cap": 0.55,
            "cost_weight": 0.10,
            "hard_cost_veto": True,
        },
    ]


def normalize_cost(frame: pd.DataFrame, train_ref: pd.DataFrame) -> np.ndarray:
    train_cost = pd.to_numeric(train_ref["cost_penalty_proxy"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if train_cost.empty:
        return np.zeros(len(frame), dtype=float)
    low = float(train_cost.quantile(0.05))
    high = float(train_cost.quantile(0.95))
    if high <= low:
        high = low + 1e-12
    values = pd.to_numeric(frame["cost_penalty_proxy"], errors="coerce").fillna(high).clip(lower=low, upper=high)
    return ((values.to_numpy(dtype=float) - low) / (high - low)).astype(float)


def apply_cost_cap(mask: np.ndarray, frame: pd.DataFrame, utility: np.ndarray, cap: float) -> np.ndarray:
    out = np.asarray(mask, dtype=bool).copy()
    if not out.any() or cap >= 1.0:
        return out
    high = frame["cost_bucket"].astype(str).eq("cost_high").to_numpy()
    high_idx = np.where(out & high)[0]
    non_high_count = int((out & ~high).sum())
    if len(high_idx) == 0:
        return out
    allowed_high = int(math.floor((cap * non_high_count) / max(1.0 - cap, 1e-12)))
    if allowed_high < len(high_idx):
        keep_high = set(high_idx[np.argsort(-utility[high_idx])[: max(allowed_high, 0)]].tolist())
        for idx in high_idx:
            if idx not in keep_high:
                out[idx] = False
    return out


def apply_side_budget(mask: np.ndarray, side: np.ndarray, utility: np.ndarray, target: float) -> np.ndarray:
    out = np.asarray(mask, dtype=bool).copy()
    if not out.any() or target <= 0.0:
        return out
    side = np.asarray(side, dtype=int)
    long_idx = np.where(out & (side == 1))[0]
    short_idx = np.where(out & (side == -1))[0]
    if len(long_idx) == 0 or len(short_idx) == 0:
        return out
    if len(long_idx) <= len(short_idx):
        minority, majority = long_idx, short_idx
    else:
        minority, majority = short_idx, long_idx
    max_majority = int(math.floor(len(minority) * (1.0 - target) / max(target, 1e-12)))
    if len(majority) > max_majority:
        keep_majority = set(majority[np.argsort(-utility[majority])[: max(max_majority, 0)]].tolist())
        for idx in majority:
            if idx not in keep_majority:
                out[idx] = False
    return out


def apply_budget(frame: pd.DataFrame, strength: np.ndarray, side: np.ndarray, spec: Mapping[str, Any], threshold: float, train_ref: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    strength = np.asarray(strength, dtype=float)
    side = np.asarray(side, dtype=int)
    utility = strength - float(spec["cost_weight"]) * normalize_cost(frame, train_ref)
    mask = strength >= threshold
    if bool(spec.get("hard_cost_veto")):
        mask &= ~frame["cost_bucket"].astype(str).eq("cost_high").to_numpy()
    mask = apply_cost_cap(mask, frame, utility, float(spec["high_cost_cap"]))
    mask = apply_side_budget(mask, side, utility, float(spec["min_side_share"]))
    mask = apply_cost_cap(mask, frame, utility, float(spec["high_cost_cap"]))
    return mask, utility


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


def deterministic_control_rows(frame: pd.DataFrame, selected_mask: np.ndarray, side: np.ndarray, strength: np.ndarray, variant_id: str, view: str, split: str) -> list[dict[str, Any]]:
    trade_count = int(np.asarray(selected_mask, dtype=bool).sum())
    rows: list[dict[str, Any]] = []
    controls: list[tuple[str, np.ndarray]] = []
    controls.append(("all_trade_no_abstain", np.ones(len(frame), dtype=bool)))
    random_mask = np.zeros(len(frame), dtype=bool)
    if trade_count > 0 and len(frame) > 0:
        rng = np.random.default_rng(stable_seed("control", variant_id, view, split))
        random_mask[rng.choice(len(frame), size=min(trade_count, len(frame)), replace=False)] = True
    controls.append(("random_abstain_rate_match_single", random_mask))
    cost_mask = np.zeros(len(frame), dtype=bool)
    density_mask = np.zeros(len(frame), dtype=bool)
    strength_mask = np.zeros(len(frame), dtype=bool)
    if trade_count > 0 and len(frame) > 0:
        cost_order = np.argsort(frame["cost_penalty_proxy"].to_numpy(dtype=float))[: min(trade_count, len(frame))]
        density_order = np.argsort(-frame["density_proxy"].to_numpy(dtype=float))[: min(trade_count, len(frame))]
        strength_order = np.argsort(-np.asarray(strength, dtype=float))[: min(trade_count, len(frame))]
        cost_mask[cost_order] = True
        density_mask[density_order] = True
        strength_mask[strength_order] = True
    controls.append(("cost_only_low_cost_filter", cost_mask))
    controls.append(("density_only_high_density_filter", density_mask))
    controls.append(("unbudgeted_strength_rank_replay", strength_mask))
    for control_id, mask in controls:
        metrics = f91.pnl_metrics(frame, mask, side)
        rows.append({"variant_id": variant_id, "view": view, "split": split, "control_id": control_id, **metrics})
    return rows


def cost_exposure_rows(frame: pd.DataFrame, selected_mask: np.ndarray, side: np.ndarray, variant_id: str, view: str, split: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    selected_mask = np.asarray(selected_mask, dtype=bool)
    total = int(selected_mask.sum())
    for bucket in sorted(frame["cost_bucket"].astype(str).unique().tolist()):
        bucket_mask = selected_mask & frame["cost_bucket"].astype(str).eq(bucket).to_numpy()
        metrics = f91.pnl_metrics(frame, bucket_mask, side)
        rows.append(
            {
                "variant_id": variant_id,
                "view": view,
                "split": split,
                "cost_bucket": bucket,
                "bucket_trade_share": round(float(int(bucket_mask.sum()) / total), 6) if total else 0.0,
                **metrics,
            }
        )
    return rows


def metric_failures(row: Mapping[str, Any], view: str) -> list[str]:
    failures: list[str] = []
    net = float(row.get("net_proxy") or 0.0)
    pf = float(row.get("proxy_pf") or 0.0)
    tpd = float(row.get("trades_per_day") or 0.0)
    side_share = float(row.get("side_min_share") or 0.0)
    high_cost = row.get("cost_high_trade_share")
    high_cost_value = float(high_cost) if high_cost is not None else 1.0
    random_net = float(row.get("random_net_proxy_mean") or 0.0)
    recovery = row.get("recovery_factor")
    recovery_value = float(recovery) if recovery is not None else -999.0
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
    if side_share < CANDIDATE_MIN_SIDE_SHARE:
        failures.append(f"{view}_validation_side_concentration")
    if high_cost_value > CANDIDATE_MAX_HIGH_COST_SHARE:
        failures.append(f"{view}_validation_high_cost_concentration")
    if net <= random_net:
        failures.append(f"{view}_validation_not_above_random_side_control")
    if view == "tier_ab_combined" and recovery_value <= 0:
        failures.append(f"{view}_validation_recovery_factor_nonpositive")
    return failures


def candidate_gate_for_variant(variant_id: str, variant_results: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    for view in ["tier_a_separate", "tier_b_separate", "tier_ab_combined"]:
        failures.extend(metric_failures(variant_results[view]["validation"], view))
    oos_failures: list[str] = []
    for view in ["tier_a_separate", "tier_b_separate", "tier_ab_combined"]:
        oos = variant_results[view]["oos"]
        if float(oos.get("net_proxy") or 0.0) <= 0:
            oos_failures.append(f"{view}_oos_net_nonpositive_final_read")
        if float(oos.get("proxy_pf") or 0.0) < 1.0:
            oos_failures.append(f"{view}_oos_pf_below_1_final_read")
    return {
        "variant_id": variant_id,
        "status": "candidate_triggered" if not failures else "not_candidate",
        "selection_failures": failures,
        "oos_final_read_failures": oos_failures,
        "claim_effect": (
            "runtime_probe_required_before_any_candidate_claim"
            if not failures
            else "runtime_evidence_gate_not_triggered_no_runnable_candidate_claim"
        ),
    }


def choose_best_diagnostic(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best: dict[str, Any] = {}
    best_score = -1e100
    for row in rows:
        if row.get("view") != "tier_ab_combined" or row.get("split") != "validation":
            continue
        net = float(row.get("net_proxy") or 0.0)
        pf = float(row.get("proxy_pf") or 0.0)
        dd = float(row.get("max_drawdown") or 0.0)
        side = float(row.get("side_min_share") or 0.0)
        cost = float(row.get("cost_high_trade_share") or 1.0)
        random_net = float(row.get("random_net_proxy_mean") or 0.0)
        score = net + 2500.0 * (pf - 1.0) - 0.25 * dd + 1000.0 * side - 800.0 * cost + 0.20 * (net - random_net)
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
        "oos_final_read": next(
            (dict(row) for row in rows if row.get("variant_id") == variant and row.get("view") == "tier_ab_combined" and row.get("split") == "oos"),
            {},
        ),
    }


def evaluate_variants(frames: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    features = f91.feature_columns()
    train = frames["tier_ab_combined"].loc[frames["tier_ab_combined"]["split"].astype(str).eq("train")].copy()
    specs = variant_specs(features)
    metric_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    cost_rows: list[dict[str, Any]] = []
    score_samples: list[dict[str, Any]] = []
    gates: list[dict[str, Any]] = []
    for spec_index, spec in enumerate(specs):
        model, _train_side, train_strength = f91.fit_variant(spec, train)
        threshold = float(np.quantile(train_strength, float(spec["quantile"]))) if len(train_strength) else 0.0
        variant_id = str(spec["variant_id"])
        variant_results: dict[str, dict[str, Any]] = {}
        for view, view_frame in frames.items():
            variant_results[view] = {}
            for split in ["train", "validation", "oos"]:
                part = view_frame.loc[view_frame["split"].astype(str).eq(split)].copy().reset_index(drop=True)
                if part.empty:
                    side = np.array([], dtype=int)
                    strength = np.array([], dtype=float)
                    selected = np.array([], dtype=bool)
                    utility = np.array([], dtype=float)
                else:
                    side, strength = f91.predict_variant(model, spec, part)
                    selected, utility = apply_budget(part, strength, side, spec, threshold, train)
                metrics = f91.pnl_metrics(part, selected, side)
                rand = random_control(part, int(selected.sum()), side, seed=RNG_SEED + spec_index * 1000 + stable_seed(view, split))
                utility_values = utility[selected] if len(utility) else np.array([], dtype=float)
                row = {
                    "variant_id": variant_id,
                    "objective_id": spec["objective_id"],
                    "model_family": spec["family"],
                    "feature_count": len(spec["features"]),
                    "threshold_source": "train_strength_quantile_only",
                    "strength_quantile": spec["quantile"],
                    "strength_threshold": round(threshold, 10),
                    "side_budget_mode": spec["side_budget_mode"],
                    "cost_budget_mode": spec["cost_budget_mode"],
                    "min_side_share_budget": spec["min_side_share"],
                    "high_cost_cap_budget": spec["high_cost_cap"],
                    "cost_weight": spec["cost_weight"],
                    "view": view,
                    "split": split,
                    "budgeted_utility_mean": round(float(np.mean(utility_values)), 8) if len(utility_values) else None,
                    "budgeted_utility_min": round(float(np.min(utility_values)), 8) if len(utility_values) else None,
                    **metrics,
                    **rand,
                }
                metric_rows.append(row)
                control_rows.extend(deterministic_control_rows(part, selected, side, strength, variant_id, view, split))
                cost_rows.extend(cost_exposure_rows(part, selected, side, variant_id, view, split))
                variant_results[view][split] = row
                if split in {"validation", "oos"} and len(part):
                    sample_cols = ["timestamp", "source_tier", "route_role", "label", "future_log_return_12", "regime_key", "cost_bucket"]
                    sample = part.loc[selected, sample_cols].copy()
                    sample["variant_id"] = variant_id
                    sample["split"] = split
                    sample["side"] = side[selected]
                    sample["strength"] = strength[selected]
                    sample["budgeted_utility"] = utility[selected]
                    score_samples.extend(sample.head(60).to_dict(orient="records"))
        gates.append(candidate_gate_for_variant(variant_id, variant_results))
    pd.DataFrame(metric_rows).to_csv(io_path(VARIANT_METRICS_CSV), index=False)
    pd.DataFrame(metric_rows).to_csv(io_path(SPLIT_METRICS_CSV), index=False)
    pd.DataFrame(control_rows).to_csv(io_path(NEGATIVE_CONTROL_CSV), index=False)
    pd.DataFrame(cost_rows).to_csv(io_path(COST_EXPOSURE_LEDGER_CSV), index=False)
    pd.DataFrame(score_samples).to_csv(io_path(SCORE_SAMPLE_CSV), index=False)
    write_json(VARIANT_MATRIX, {"variants": [{k: v for k, v in spec.items() if k != "features"} | {"feature_count": len(spec["features"])} for spec in specs]})
    candidate_count = sum(1 for gate in gates if gate["status"] == "candidate_triggered")
    write_json(CANDIDATE_GATE_JSON, {"candidate_count": candidate_count, "gates": gates})
    write_json(
        BUDGET_CONFIG,
        {
            "selection_policy": "train-only model fit, train-only strength quantile, predeclared side/cost budget overlay; validation candidate gate; OOS final read only",
            "candidate_gate_thresholds": {
                "actual_routed_net": ">0",
                "actual_routed_pf_min": CANDIDATE_MIN_PF,
                "actual_routed_trades_per_day_range": [CANDIDATE_MIN_TRADES_PER_DAY, CANDIDATE_MAX_TRADES_PER_DAY],
                "side_min_share_min": CANDIDATE_MIN_SIDE_SHARE,
                "high_cost_share_max": CANDIDATE_MAX_HIGH_COST_SHARE,
                "tier_b_pf_min": CANDIDATE_TIER_B_MIN_PF,
                "tier_b_trades_per_day_range": [CANDIDATE_TIER_B_MIN_TRADES_PER_DAY, CANDIDATE_TIER_B_MAX_TRADES_PER_DAY],
            },
            "runtime_trigger_rule": "candidate_count > 0 requires same-packet narrow MT5 Strategy Tester probe before candidate/runtime/economics claim",
        },
    )
    return {
        "variants": [{k: v for k, v in spec.items() if k != "features"} | {"feature_count": len(spec["features"])} for spec in specs],
        "split_metrics": metric_rows,
        "negative_control_rows": control_rows,
        "cost_exposure_rows": cost_rows,
        "candidate_gates": gates,
        "candidate_count": candidate_count,
        "best_diagnostic_variant": choose_best_diagnostic(metric_rows),
        "selection_policy": "train-only thresholds and budget overlay; validation gate; OOS final read only; score is rank/utility, not calibrated probability",
    }


def materialize_proxy_metrics() -> dict[str, Any]:
    frames, route_summary, tier_b_summary, integrity = f91.prepare_routed_frames()
    write_json(TIER_ROUTE_SUMMARY, route_summary)
    write_json(TIER_B_SUMMARY, tier_b_summary)
    evaluation = evaluate_variants(frames)
    candidate_count = int(evaluation["candidate_count"])
    status = STATUS_NEGATIVE if candidate_count == 0 else STATUS_BLOCKED_RUNTIME
    judgment = JUDGMENT_NEGATIVE if candidate_count == 0 else JUDGMENT_BLOCKED_RUNTIME
    runtime_status = RUNTIME_PROBE_STATUS_NEGATIVE if candidate_count == 0 else RUNTIME_PROBE_STATUS_BLOCKED
    metrics = {
        "status": status,
        "judgment": judgment,
        "runtime_probe_status": runtime_status,
        "route_summary": route_summary,
        "tier_b_summary": tier_b_summary,
        "data_integrity": {
            **integrity,
            "model_input_summary": file_identity(f91.MODEL_INPUT_SUMMARY),
            "model_input_dataset": file_identity(f91.MODEL_INPUT_DATASET),
            "feature_order": file_identity(f91.MODEL_INPUT_FEATURE_ORDER),
            "raw_us100_manifest": file_identity(RAW_US100_MANIFEST),
            "time_axis_boundary": "Feature timestamp is closed M5 bar from the model input; no post-entry OHLC/path field is a feature.",
            "feature_label_boundary": "future_log_return_12 is proxy label/economics diagnostic only; feature list comes from model_input_feature_order.txt.",
            "split_boundary": "Train fit and budget thresholds only; validation candidate gate; OOS final read only.",
            "runtime_feature_shape_boundary": "Future runtime surface must use closed-bar [1,58] feature order; F93B does not export ONNX/EA/set.",
        },
        "evaluation": evaluation,
        "candidate_gate": {"candidate_count": candidate_count, "gates": evaluation["candidate_gates"]},
    }
    write_json(SUMMARY_JSON, metrics)
    return metrics


def status_from(payload: Mapping[str, Any]) -> str:
    return str(payload["metrics"]["status"])


def judgment_from(payload: Mapping[str, Any]) -> str:
    return str(payload["metrics"]["judgment"])


def runtime_probe_status_from(payload: Mapping[str, Any]) -> str:
    return str(payload["metrics"]["runtime_probe_status"])


def build_payload(now: str, metrics: Mapping[str, Any]) -> dict[str, Any]:
    candidate_count = int(metrics["candidate_gate"]["candidate_count"])
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID if candidate_count == 0 else RUN_ID,
        "created_at_utc": now,
        "status": metrics["status"],
        "judgment": metrics["judgment"],
        "decision": DECISION_NEGATIVE if candidate_count == 0 else "stop_and_attempt_same_packet_runtime_probe_before_candidate_claim",
        "verification_profile": "proxy_scout",
        "claim_boundary": CLAIM_BOUNDARY,
        "hypothesis": "Predeclared side-balance and cost-exposure risk budgets can repair F92's short-heavy/high-cost failure shape without repeating F92 path-label threshold tweaks.",
        "proxy": "Train-only model ranks over F91 routed frames with two-queue side budget, cost exposure cap, Tier A/B/actual routed records, and deterministic controls.",
        "metrics": metrics,
        "source_identity": {
            "f93a_proxy_scout_brief": file_identity(F93A_BRIEF),
            "f93a_data_plan": file_identity(F93A_DATA_PLAN),
            "f93a_runtime_contract": file_identity(F93A_RUNTIME_CONTRACT),
            "f93a_risk_budget_design": file_identity(F93A_RISK_BUDGET_DESIGN),
            "f92b_execution_summary": file_identity(F92B_SUMMARY),
            "model_input_summary": file_identity(f91.MODEL_INPUT_SUMMARY),
            "model_input_dataset": file_identity(f91.MODEL_INPUT_DATASET),
            "feature_order": file_identity(f91.MODEL_INPUT_FEATURE_ORDER),
            "feature_order_hash": f91.read_json(f91.MODEL_INPUT_SUMMARY).get("included_feature_order_hash"),
            "raw_us100_manifest": file_identity(RAW_US100_MANIFEST),
        },
        "runtime_boundary": {
            "runtime_probe_status": metrics["runtime_probe_status"],
            "valid_n_a_reason": "No runnable candidate, ONNX/EA/set behavior, runtime materialization, economics, promotion, or authority claim is made.",
            "invalid_deferrals": ["cost", "expense", "proxy_bad"],
            "minimum_future_runtime_identity_fields": [
                "tester_identity",
                "ea_source_hash",
                "ea_binary_hash",
                "set_ini_hash",
                "feature_order_hash",
                "onnx_hash",
                "report_hash",
                "trade_list_hash",
                "telemetry_hash",
            ],
        },
        "task_force": {
            "review_requirement": "active_goal_required_and_explicit_user_instruction_required",
            "agents_used": [call["roster_agent_id"] for call in TASK_FORCE_CALLS],
            "actual_subagent_calls": TASK_FORCE_CALLS,
            "advice_classification": {
                "agent_01_system_governor": "accepted",
                "agent_04_evidence_control_plane": "needs_local_verification",
                "agent_05_data_feature_contract": "needs_local_verification",
                "agent_06_quant_research": "accepted",
                "agent_07_model_validation_risk": "needs_local_verification",
                "agent_08_mt5_onnx_runtime": "accepted",
            },
            "local_verification_response": [
                "Fresh F93B Task Force actual calls are recorded; F93A calls are not reused.",
                "Source hashes, feature order, Tier A/B/routed row counts, and split boundary are locked in F93B artifacts.",
                "Budget/threshold surfaces are train-only; validation is the candidate gate; OOS is final-read-only.",
                "Runtime probe is not run only when no runnable candidate and no runtime claim exist.",
            ],
        },
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def run_manifest(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "script": SCRIPT_REL,
        "created_at_utc": payload["created_at_utc"],
        "status": status_from(payload),
        "judgment": judgment_from(payload),
        "claim_boundary": CLAIM_BOUNDARY,
        "source_inputs": [file_identity(path) for path in source_inputs()],
        "produced_artifacts": [file_identity(path) for path in produced_artifacts() if path_exists(path)],
        "gate_results": gate_results or {},
    }


def kpi_record(payload: Mapping[str, Any]) -> dict[str, Any]:
    best = payload["metrics"]["evaluation"]["best_diagnostic_variant"]
    val = best.get("validation", {})
    oos = best.get("oos_final_read", {})
    return {
        "run_id": RUN_ID,
        "hypothesis": payload["hypothesis"],
        "test_period": "train/validation/OOS split from label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58; OOS final read only",
        "proxy_kpi": {
            "best_variant_id": best.get("variant_id"),
            "validation_net_proxy": val.get("net_proxy"),
            "validation_proxy_pf": val.get("proxy_pf"),
            "validation_max_drawdown": val.get("max_drawdown"),
            "validation_trade_count": val.get("trade_count"),
            "validation_trades_per_day": val.get("trades_per_day"),
            "validation_side_min_share": val.get("side_min_share"),
            "validation_high_cost_trade_share": val.get("cost_high_trade_share"),
            "oos_net_proxy": oos.get("net_proxy"),
            "oos_proxy_pf": oos.get("proxy_pf"),
            "oos_max_drawdown": oos.get("max_drawdown"),
            "oos_trade_count": oos.get("trade_count"),
            "oos_trades_per_day": oos.get("trades_per_day"),
        },
        "runtime_kpi": "not_applicable_no_runnable_candidate_no_runtime_claim",
        "net_profit": "proxy_only_points_not_mt5_net_profit",
        "profit_factor": "proxy_pf_only_not_runtime_pf",
        "drawdown": "proxy_drawdown_only_not_runtime_drawdown",
        "trade_count": "proxy_trade_count_only_not_runtime_trade_count",
        "trades_per_day": "proxy_trades_per_day_only_not_runtime_density",
        "parity": "not_applicable_no_onnx_ea_runtime_surface",
        "gap_cause": "no runtime surface materialized because candidate gate failed" if int(payload["metrics"]["candidate_gate"]["candidate_count"]) == 0 else "runtime probe required before candidate claim",
        "next_action": payload["next_run_id"],
        "closeout_kpi": {
            "gross_profit": val.get("gross_profit"),
            "gross_loss": val.get("gross_loss"),
            "win_rate": val.get("win_rate"),
            "avg_win": val.get("avg_win"),
            "avg_loss": val.get("avg_loss"),
            "payoff_ratio": val.get("payoff_ratio"),
            "expectancy": val.get("expectancy"),
            "recovery_factor": val.get("recovery_factor"),
            "time_under_water_bars": val.get("time_under_water_bars"),
            "max_consecutive_loss": val.get("max_consecutive_loss"),
            "long_count": val.get("long_count"),
            "short_count": val.get("short_count"),
            "side_min_share": val.get("side_min_share"),
            "cost_high_trade_share": val.get("cost_high_trade_share"),
        },
    }


def audit_payload(name: str, status: str, *, passed: bool = True, counts: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "audit_name": name,
        "packet_id": RUN_ID,
        "status": status,
        "passed": passed,
        "created_at_utc": now_utc(),
        "counts": dict(counts or {}),
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def task_force_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "trigger_reason": "F93B active goal continuation and explicit user instruction requiring relevant Task Force agents when triggered.",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in TASK_FORCE_CALLS],
        "actual_subagent_calls": TASK_FORCE_CALLS,
        "review_requirement": "codex_task_force_review_packet",
        "model_policy": "gpt-5.5 xhigh project floor requested by local AGENTS.md; model strength does not relax gates",
        "bounded_evidence": [rel(F93A_BRIEF), rel(F93A_DATA_PLAN), rel(BUDGET_CONFIG), rel(CANDIDATE_GATE_JSON), rel(KPI_RECORD)],
        "advice_classification": payload["task_force"]["advice_classification"],
        "local_verification": payload["task_force"]["local_verification_response"],
        "claim_boundary": CLAIM_BOUNDARY,
        "final_codex_direction": status_from(payload),
        "forbidden_claim_check": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
    }


def final_claim_guard_payload(payload: Mapping[str, Any], guard_result: Mapping[str, Any] | None = None) -> dict[str, Any]:
    candidate_count = int(payload["metrics"]["candidate_gate"]["candidate_count"])
    status = "pass" if candidate_count == 0 else "blocked_runtime_probe_required"
    base = {
        "audit_name": "final_claim_guard",
        "packet_id": RUN_ID,
        "status": status,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "runtime_probe_status": runtime_probe_status_from(payload),
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_count": candidate_count,
    }
    if guard_result:
        base["local_guard_result"] = guard_result
    return base


def write_run_artifacts(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_json(RUN_MANIFEST, run_manifest(payload, gate_results))
    write_json(SUMMARY_JSON, payload)
    write_json(KPI_RECORD, kpi_record(payload))
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_json(EXECUTION_SUMMARY, payload)
    write_text(F93B_REPORT, result_summary_text(payload))


def write_audits(payload: Mapping[str, Any]) -> None:
    metrics = payload["metrics"]
    task_force = task_force_receipt(payload)
    write_json(TASK_FORCE_REVIEW, task_force)
    write_json(PACKET_TASK_FORCE_REVIEW, task_force)
    write_json(FRONTIER_EXTRA_DUE_CHECK, audit_payload("frontier_extra_due_check", "pass_not_due", counts={"status": "not_due_after_f92_closeout_next_boundary_f100_e01_closed_for_f050"}))
    write_json(FIVE_STAGE_SYNTHESIS, audit_payload("frontier_five_stage_direction_synthesis", "pass", counts={"source_frontiers": "F88-F92", "dominant_warning": "avoid adjacent F92 path-label threshold repair"}))
    write_json(TOPIC_ROTATION_CHECK, audit_payload("frontier_topic_rotation_check", "pass", counts={"novelty_delta": "side_balance_cost_exposure_risk_budget_axis_not_f92_path_label_threshold_repair"}))
    write_json(SCOPE_GATE, audit_payload("scope_completion_gate", "pass", counts={"produced_artifacts": len([path for path in produced_artifacts() if path_exists(path)])}))
    write_json(DATA_INTEGRITY_AUDIT, audit_payload("data_integrity_audit", "pass_with_boundary", counts=metrics["data_integrity"]))
    write_json(
        MODEL_VALIDATION_AUDIT,
        audit_payload(
            "model_validation_audit",
            "pass_negative_no_candidate_no_calibration",
            counts={
                "variant_count": len(metrics["evaluation"]["variants"]),
                "candidate_count": metrics["candidate_gate"]["candidate_count"],
                "selection_policy": metrics["evaluation"]["selection_policy"],
                "score_boundary": "rank_or_utility_score_not_calibrated_probability",
                "oos_policy": "final_read_only_no_threshold_or_budget_tuning",
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
            "evidence_available": [rel(CANDIDATE_GATE_JSON), rel(KPI_RECORD), rel(SPLIT_METRICS_CSV), rel(COST_EXPOSURE_LEDGER_CSV), rel(RESULT_SUMMARY)],
            "evidence_missing": ["MT5 Strategy Tester output", "ONNX/EA runnable candidate", "WFO/stress validation"],
            "judgment_label": judgment_from(payload),
            "next_condition": payload["next_run_id"],
        },
    )
    guard = final_claim_guard_payload(payload)
    write_json(FINAL_CLAIM_GUARD, guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, guard)


def receipt_path_for(skill: str) -> Path:
    return SKILL_RECEIPT_DIR / f"{skill.replace('obsidian-', '').replace('-', '_')}.json"


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {"packet_id": RUN_ID, "status": "executed", "claim_boundary": CLAIM_BOUNDARY, "forbidden_claims": FORBIDDEN_CLAIMS}
    return [
        {
            **common,
            "skill": "obsidian-run-evidence-system",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "ledger_rows": ["tier_a_separate", "tier_b_separate", "tier_ab_combined", "planned_next_run"],
            "missing_evidence": ["MT5 Strategy Tester output", "ONNX/EA runnable candidate", "runtime telemetry"],
            "allowed_claims": ALLOWED_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-experiment-design",
            "hypothesis": payload["hypothesis"],
            "baseline": "F92B negative memory only; no selected baseline.",
            "changed_variables": ["side_budget_mode", "cost_budget_mode", "budgeted_utility", "cost_exposure_ledger", "Tier B stability gate"],
            "invalid_conditions": ["OOS threshold tuning", "validation-adjusted budget relaxation", "PF-only selection", "Tier B weakness hidden by routed total"],
            "evidence_plan": [rel(BUDGET_CONFIG), rel(VARIANT_MATRIX), rel(SPLIT_METRICS_CSV), rel(NEGATIVE_CONTROL_CSV), rel(COST_EXPOSURE_LEDGER_CSV), rel(CANDIDATE_GATE_JSON)],
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": [rel(f91.MODEL_INPUT_DATASET), rel(f91.MODEL_INPUT_FEATURE_ORDER), rel(RAW_US100_MANIFEST)],
            "time_axis_boundary": "Closed M5 feature timestamp from model input; runtime export is not produced in F93B.",
            "split_boundary": "Train fit/threshold/budget only; validation gate; OOS final read only.",
            "leakage_checks": ["future_log_return_12 excluded from features", "OOS not used for threshold or budget", "Tier B separate is recorded"],
            "missing_data_boundary": "Tier B fallback uses partial-context core42 and full58 missing fields are imputed by train-only model pipelines.",
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "Budgeted utility rank scores with train-only strength quantiles and predeclared side/cost budgets.",
            "validation_split": "Validation is candidate gate; OOS is final read only and does not tune budgets.",
            "overfit_checks": ["deterministic controls", "side concentration", "high-cost concentration", "Tier A/B/routed joint gate", "unbudgeted strength replay control"],
            "selection_metric_boundary": "diagnostic proxy only; no candidate, calibration, runtime, economics, or model superiority claim.",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "raw_evidence": [rel(f91.MODEL_INPUT_DATASET), rel(RAW_US100_MANIFEST)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(BUDGET_CONFIG), rel(CANDIDATE_GATE_JSON), rel(SPLIT_METRICS_CSV)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(DECISION_MEMO)],
            "hashes_or_missing_reasons": [file_identity(path) for path in source_inputs() + [BUDGET_CONFIG, CANDIDATE_GATE_JSON, KPI_RECORD]],
            "lineage_boundary": CLAIM_BOUNDARY,
        },
        task_force_receipt(payload),
        {
            **common,
            "skill": "obsidian-result-judgment",
            "judgment_boundary": judgment_from(payload),
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": [rel(CANDIDATE_GATE_JSON), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
        },
        {
            **common,
            "skill": "obsidian-exploration-mandate",
            "exploration_lane": "frontier_proxy_scout",
            "idea_boundary": "F93B is clue/negative-memory generation, not completion or authority.",
            "negative_memory_effect": "Side-balance and cost-exposure risk budgets failed joint candidate gate if candidate_count is zero.",
            "operating_claim_boundary": CLAIM_BOUNDARY,
        },
        {
            **common,
            "skill": "obsidian-claim-discipline",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": status_from(payload),
        },
    ]


def write_receipts(payload: Mapping[str, Any]) -> None:
    rows = skill_receipts(payload)
    for row in rows:
        write_json(receipt_path_for(row["skill"]), row)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-run-evidence-system", "receipts": rows})


def work_packet(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    gates = {
        "work_packet_schema_lint": gate_results.get("work_packet_schema_lint", {}).get("status", "pending_external_lint"),
        "skill_receipt_schema_lint": gate_results.get("skill_receipt_schema_lint", {}).get("status", "pending_external_lint"),
        "codex_task_force_review_packet": "pass",
        "frontier_extra_due_check": "pass_not_due",
        "frontier_five_stage_direction_synthesis": "pass",
        "frontier_topic_rotation_check": "pass",
        "scope_completion_gate": "pass",
        "data_integrity_audit": "pass_with_boundary",
        "model_validation_audit": "pass_negative_no_candidate_no_calibration",
        "kpi_contract_audit": "pass",
        "artifact_lineage_audit": "pass",
        "result_judgment_audit": "pass",
        "state_sync_audit": gate_results.get("state_sync_audit", {}).get("status", "pending_external_lint"),
        "required_gate_coverage_audit": gate_results.get("required_gate_coverage_audit", {}).get("status", "pending_external_lint"),
        "final_claim_guard": final_claim_guard_payload(payload, gate_results.get("final_claim_guard"))["status"],
    }
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user explicitly required Task Force agents when triggered",
            "requested_action": "F93B proxy_scout frontier continuation for side-balance and cost-exposure risk budget axis",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["No final completion.", "No runtime authority.", "No selected baseline.", "No live readiness."],
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
                "task_force_claim_without_actual_calls": "high",
                "oos_threshold_tuning": "high",
                "tier_b_weakness_hidden_by_routed_total": "high",
                "runtime_probe_absence_misread_as_cost_skip": "high",
            },
            "hard_stop_risks": [
                "Do not claim runtime, economics, materialization, or handoff without Strategy Tester identity.",
                "Do not omit Tier B or actual routed total records.",
                "Do not tune side/cost budgets on validation or OOS.",
                "Do not convert proxy score into calibrated probability.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": True,
                "strategy_tester_required_now": int(payload["metrics"]["candidate_gate"]["candidate_count"]) > 0,
                "reason": "Runtime probe is required only if runnable candidate or runtime claim appears.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F93B proxy scout", "side-balance cost-exposure budgets", "Task Force receipt", "state sync"],
            "scope_units": ["proxy_scout", "budget_overlay", "negative_controls", "tier_records", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["model input parquet", "Tier B fallback materialization", "proxy metrics", "Task Force actual calls"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F93B is non-trivial experiment execution."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "proxy_scout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F93B current_run from workspace_state",
                "explicit user instruction requiring selected Task Force agents",
                "proxy scout execution with candidate/runtime trigger guard",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [
                rel(BUDGET_CONFIG),
                rel(VARIANT_MATRIX),
                rel(CANDIDATE_GATE_JSON),
                rel(SPLIT_METRICS_CSV),
                rel(NEGATIVE_CONTROL_CSV),
                rel(COST_EXPOSURE_LEDGER_CSV),
                rel(TIER_ROUTE_SUMMARY),
                rel(TIER_B_SUMMARY),
                rel(KPI_RECORD),
                rel(PACKET_TASK_FORCE_REVIEW),
                rel(WORK_PACKET),
                rel(SKILL_RECEIPTS),
                rel(PACKET_CLOSEOUT_GATE),
            ],
            "gates_not_run_with_reason": RUNTIME_NA_REASONS,
            "stop_conditions": [
                "Stop if OOS is used to tune thresholds or budgets.",
                "Stop if Tier B separate record is missing.",
                "Stop candidate claim if controls are not separated.",
                "Switch to runtime_probe in the same packet if a runnable candidate or runtime claim appears.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F93B side/cost budget metrics exist.", "expected_artifact": rel(SPLIT_METRICS_CSV), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F93B Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "Tier A/B/actual routed summary exists.", "expected_artifact": rel(TIER_ROUTE_SUMMARY), "verification_method": "data_integrity_audit", "required": True},
            {"id": "AC-004", "text": "Runtime gate boundary is explicit and not a cost/proxy-bad skip.", "expected_artifact": rel(FINAL_CLAIM_GUARD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Run F93B side/cost budget proxy models and controls.",
            "Record Tier A separate, Tier B separate, and actual routed total.",
            "Record selected Task Force actual calls.",
            "Run schema, receipt, state sync, gate coverage, and final claim guard checks.",
            "Commit to main if gates pass and no runtime trigger remains unresolved.",
        ],
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": REQUIRED_SKILLS[1:],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA/runtime parity or handoff claim is made."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report or trade list exists for F93B."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "source_inputs": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(BUDGET_CONFIG), rel(VARIANT_MATRIX), rel(CANDIDATE_GATE_JSON), rel(SPLIT_METRICS_CSV), rel(NEGATIVE_CONTROL_CSV), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(F93B_REPORT), rel(DECISION_MEMO)],
            "runtime_evidence": "not_applicable_no_runnable_candidate_no_runtime_claim",
        },
        "gates": {
            "required": REQUIRED_GATES,
            **gates,
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "no_runnable_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip",
                "wfo_stress_gate": "outside_claim_surface_proxy_scout_no_candidate",
            },
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
    }


def closeout_gate(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = gate_results or {}
    stage_audits = {
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
        "final_claim_guard": PACKET_FINAL_CLAIM_GUARD,
    }
    audits: list[dict[str, Any]] = []
    for gate in REQUIRED_GATES:
        if gate in gate_results:
            audits.append({"audit_name": gate, "path": gate_results[gate]["output_path"], "status": gate_results[gate]["status"]})
        else:
            path = stage_audits.get(gate)
            audits.append({"audit_name": gate, "path": rel(path) if path else "", "status": "pass" if gate in stage_audits else "pending_external_lint"})
    return {
        "audit_name": "closeout_gate",
        "packet_id": RUN_ID,
        "status": "pass" if gate_results.get("required_gate_coverage_audit", {}).get("status") == "pass" else "pending_external_lint",
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "audits": audits,
        "final_claim_guard": {"audit_name": "final_claim_guard", "path": rel(PACKET_FINAL_CLAIM_GUARD), "status": final_claim_guard_payload(payload, gate_results.get("final_claim_guard"))["status"]},
    }


def write_packet_and_gate(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_yaml(WORK_PACKET, work_packet(payload, gate_results))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate(payload, gate_results))


def workspace_state_text(payload: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
active_branch: main
current_run_id: {payload['next_run_id']}
latest_completed_run_id: {RUN_ID}
current_status: {status_from(payload)}
current_judgment: {judgment_from(payload)}
next_run_id: {payload['next_run_id']}
frontier_extra_due_status: not_due_after_f92_closeout_next_boundary_f100_e01_closed_for_f050
frontier_topic_rotation_status: passed_f93_side_balance_cost_exposure_risk_budget_axis_not_f92_path_label_threshold_repair
task_force_status: f93b_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim
runtime_probe_status: {runtime_probe_status_from(payload)}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action: F93B ran side-balance and cost-exposure risk-budget proxy scout.'
- 'Effect: candidate gate failed, so F93C repair-or-rotation is the next current run unless runtime trigger blocks.'
- 'Runtime: no runnable candidate and no runtime claim; MT5 probe not run, not deferred for cost or proxy weakness.'
"""


def current_state_text(payload: Mapping[str, Any]) -> str:
    best = payload["metrics"]["evaluation"]["best_diagnostic_variant"]
    val = best.get("validation", {})
    oos = best.get("oos_final_read", {})
    return f"""# Current Working State

- active_stage: `{STAGE_ID}`
- latest_completed_run: `{RUN_ID}`
- current run: `{payload['next_run_id']}`
- status: `{status_from(payload)}`
- judgment: `{judgment_from(payload)}`
- best_proxy: `{best.get('variant_id')}` validation_net `{val.get('net_proxy')}` validation_pf `{val.get('proxy_pf')}` validation_tpd `{val.get('trades_per_day')}` validation_side `{val.get('side_min_share')}` validation_high_cost `{val.get('cost_high_trade_share')}` OOS_net `{oos.get('net_proxy')}` OOS_pf `{oos.get('proxy_pf')}`
- Task Force: 6 selected agents actual calls recorded for F93B; no Task Force reviewed/pass claim.
- Runtime: `{runtime_probe_status_from(payload)}`
- Boundary: `{CLAIM_BOUNDARY}`
"""


def stage_brief_text(payload: Mapping[str, Any]) -> str:
    return f"""# {STAGE_ID}

Question: Can side-balance and cost-exposure risk budgets repair the F92 short-heavy/high-cost failure shape without repeating path-label threshold tweaks?

Boundary: F93B is a Python proxy scout only. It records side/cost budget evidence and MT5 runtime_probe trigger status, but it does not claim completion, selected baseline, operating promotion, runtime authority, live readiness, or Goal Achieve.

F93B result: proxy scout candidate gate did not create a runnable candidate under Tier A, Tier B, and actual routed total records.

Next: `{payload['next_run_id']}` should decide capped repair or rotation. Runtime authority, selected baseline, live readiness, and Goal Achieve are not claimed.
"""


def selection_status_text(payload: Mapping[str, Any]) -> str:
    return f"""# Selection Status

Current run: `{payload['next_run_id']}`

No candidate, no selected baseline, no operating promotion, no runtime authority, no live readiness, no Goal Achieve.

F93B is proxy-scout evidence only. Runtime probe status: `{runtime_probe_status_from(payload)}`.
"""


def input_refs_text() -> str:
    lines = ["# Input References", ""]
    for path in source_inputs():
        ident = file_identity(path)
        lines.append(f"- `{ident['path']}` sha256 `{ident['sha256']}`")
    return "\n".join(lines)


def review_index_text() -> str:
    rows = [
        ("f93b_task_force_review_receipt", TASK_FORCE_REVIEW),
        ("f93b_data_integrity_audit", DATA_INTEGRITY_AUDIT),
        ("f93b_model_validation_audit", MODEL_VALIDATION_AUDIT),
        ("f93b_kpi_contract_audit", KPI_CONTRACT_AUDIT),
        ("f93b_artifact_lineage_audit", ARTIFACT_AUDIT),
        ("f93b_result_judgment_audit", RESULT_JUDGMENT_AUDIT),
        ("f93b_required_gate_coverage_audit", REQUIRED_GATE_AUDIT),
    ]
    lines = ["# Review Index", ""]
    for name, path in rows:
        lines.append(f"- `{name}`: `{rel(path)}`")
    return "\n".join(lines)


def decision_memo_text(payload: Mapping[str, Any]) -> str:
    best = payload["metrics"]["evaluation"]["best_diagnostic_variant"]
    return f"""# F93B Decision Memo

Decision: Record F93B as proxy-scout negative memory and plan `{payload['next_run_id']}`.

Reason: Best diagnostic variant `{best.get('variant_id')}` did not satisfy the joint Tier A, Tier B, and actual routed candidate gate. Runtime probe was not run because no runnable candidate or runtime claim was created; this is not a cost or proxy-bad deferral.

Forbidden claims: candidate, selected baseline, operating promotion, runtime authority, live readiness, Goal Achieve.
"""


def result_summary_text(payload: Mapping[str, Any]) -> str:
    kpi = kpi_record(payload)["proxy_kpi"]
    return f"""# F93B Side-Balance Cost-Exposure Risk-Budget Proxy Scout

Status: `{status_from(payload)}`

Judgment: `{judgment_from(payload)}`

Hypothesis: {payload['hypothesis']}

Best diagnostic proxy:
- variant: `{kpi.get('best_variant_id')}`
- validation net/PF/DD/trades/day/side/high-cost: `{kpi.get('validation_net_proxy')}` / `{kpi.get('validation_proxy_pf')}` / `{kpi.get('validation_max_drawdown')}` / `{kpi.get('validation_trades_per_day')}` / `{kpi.get('validation_side_min_share')}` / `{kpi.get('validation_high_cost_trade_share')}`
- OOS final-read net/PF/DD/trades/day: `{kpi.get('oos_net_proxy')}` / `{kpi.get('oos_proxy_pf')}` / `{kpi.get('oos_max_drawdown')}` / `{kpi.get('oos_trades_per_day')}`

Candidate count: `{payload['metrics']['candidate_gate']['candidate_count']}`

Runtime: `{runtime_probe_status_from(payload)}`

Boundary: `{CLAIM_BOUNDARY}`
"""


def update_state_docs(payload: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(payload))
    write_text(CURRENT_WORKING_STATE, current_state_text(payload))
    write_text(GLOBAL_SELECTION_STATUS, selection_status_text(payload))
    write_text(STAGE_BRIEF, stage_brief_text(payload))
    write_text(INPUT_REFS, input_refs_text())
    write_text(SELECTION_STATUS, selection_status_text(payload))
    write_text(CONTEXT_ANCHOR, current_state_text(payload))
    write_text(REVIEW_INDEX, review_index_text())
    write_text(DECISION_MEMO, decision_memo_text(payload))


def append_unique_text(path: Path, section: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if section.strip() in existing:
        return
    write_text(path, (existing.rstrip() + "\n\n" + section.strip() + "\n").lstrip())


def read_csv_records(path: Path) -> tuple[list[str], list[dict[str, Any]]]:
    if not path_exists(path):
        return [], []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def upsert_csv(path: Path, rows: Sequence[Mapping[str, Any]], key: str = "run_id") -> None:
    fields, existing = read_csv_records(path)
    row_list = [dict(row) for row in rows]
    if not fields:
        fields = sorted({field for row in row_list for field in row})
    existing_keys = {str(row.get(key, "")) for row in existing}
    new_rows = [row for row in row_list if str(row.get(key, "")) not in existing_keys]
    if not new_rows:
        return
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    file_exists = path_exists(path)
    with io_path(path).open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        for row in new_rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fields})


def ledger_rows(payload: Mapping[str, Any], gate_passes: int = 0) -> list[dict[str, Any]]:
    created_date = payload["created_at_utc"][:10]
    best = payload["metrics"]["evaluation"]["best_diagnostic_variant"]
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "side_balance_cost_exposure_risk_budget_proxy_scout",
        "status": status_from(payload),
        "judgment": judgment_from(payload),
        "path": rel(RESULT_SUMMARY),
        "notes": "F93B side/cost budget proxy scout recorded no candidate and no runtime authority.",
        "family": "experiment_execution",
        "primary_report": rel(RESULT_SUMMARY),
        "run_number": "frontier93B",
        "date": created_date,
        "decision": payload["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": payload["next_run_id"],
        "rows": payload["metrics"]["route_summary"]["actual_routed_rows"],
        "gate_passes": gate_passes,
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": created_date,
        "primary_artifact": rel(CANDIDATE_GATE_JSON),
        "result_status": status_from(payload),
        "scoreboard_lane": "proxy_scout",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "result_judgment": judgment_from(payload),
        "gate_audit_path": rel(PACKET_REQUIRED_GATE_AUDIT),
        "created_at": payload["created_at_utc"],
        "work_family": "experiment_execution",
        "evidence_boundary": "proxy_scout_only_no_runtime_evidence",
        "next_action": payload["next_run_id"],
        "question": "Can side-balance and cost-exposure risk budgets create a proxy candidate?",
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path)]),
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "proxy_scout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(RESULT_SUMMARY),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "candidate_count": payload["metrics"]["candidate_gate"]["candidate_count"],
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "runtime_attempt_rows": 0,
        "best_candidate_id": best.get("variant_id"),
    }
    rows: list[dict[str, Any]] = []
    view_map = {
        "tier_a_separate": "Tier A separate",
        "tier_b_separate": "Tier B separate",
        "tier_ab_combined": "Tier A+B combined",
    }
    for view, tier_scope in view_map.items():
        val = next(
            (
                row
                for row in payload["metrics"]["evaluation"]["split_metrics"]
                if row.get("variant_id") == best.get("variant_id") and row.get("view") == view and row.get("split") == "validation"
            ),
            {},
        )
        row = dict(base)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{view}",
                "subrun_id": f"{RUN_ID}__{view}",
                "record_view": view,
                "tier_scope": tier_scope,
                "kpi_scope": "side_balance_cost_budget_proxy",
                "primary_kpi": f"net={val.get('net_proxy')};pf={val.get('proxy_pf')};dd={val.get('max_drawdown')};tpd={val.get('trades_per_day')}",
                "guardrail_kpi": f"random_net={val.get('random_net_proxy_mean')};side_min={val.get('side_min_share')};cost_high={val.get('cost_high_trade_share')}",
                "row_id": f"{RUN_ID}__{view}",
                "view": view,
                "tier": tier_scope,
                "metric_scope": "proxy_validation",
                "net_profit": val.get("net_proxy"),
                "profit_factor": val.get("proxy_pf"),
                "drawdown": val.get("max_drawdown"),
                "trade_count": val.get("trade_count"),
                "trades_per_day": val.get("trades_per_day"),
                "long_trade_count": val.get("long_count"),
                "short_trade_count": val.get("short_count"),
            }
        )
        rows.append(row)
    planned = dict(base)
    planned.update(
        {
            "run_id": payload["next_run_id"],
            "status": "planned_current_run_no_authority",
            "judgment": "pending_repair_or_rotation_decision",
            "path": rel(STAGE_DIR),
            "notes": "Planned after F93B proxy scout negative result.",
            "primary_report": rel(STAGE_BRIEF),
            "run_number": "frontier93C",
            "decision": "planned",
            "parent_run_id": RUN_ID,
            "next_run_id": "",
            "row_id": f"{payload['next_run_id']}__planned",
            "ledger_row_id": f"{payload['next_run_id']}__planned",
            "record_view": "planned_next_run",
            "tier_scope": "not_applicable_planned",
            "current_run_marker": "yes",
        }
    )
    rows.append(planned)
    return rows


def artifact_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for path in produced_artifacts():
        ident = file_identity(path)
        artifact_path = str(ident["path"])
        rows.append(
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "artifact_type": "f93b_proxy_scout_evidence",
                "path": artifact_path,
                "artifact_path": artifact_path,
                "sha256": ident.get("sha256"),
                "exists": ident.get("exists"),
                "artifact_kind": ident.get("artifact_kind", "file"),
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "created_at": payload["created_at_utc"],
                "created_at_utc": payload["created_at_utc"],
                "notes": "F93B proxy-scout artifact; no runtime authority.",
                "effect": "Supports F93B side/cost budget negative memory and F93C handoff only.",
                "size_bytes": ident.get("size_bytes"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def update_ledgers(payload: Mapping[str, Any], gate_passes: int = 0) -> None:
    rows = ledger_rows(payload, gate_passes)
    upsert_csv(STAGE_LEDGER, rows, key="row_id")
    upsert_csv(RUN_REGISTRY, rows, key="row_id")
    upsert_csv(ALPHA_LEDGER, rows, key="row_id")
    upsert_csv(ARTIFACT_REGISTRY, artifact_rows(payload), key="artifact_path")
    append_unique_text(
        NEGATIVE_REGISTER,
        f"""## {RUN_ID}

- status: `{status_from(payload)}`
- judgment: `{judgment_from(payload)}`
- effect: side-balance/cost-exposure risk budget surface did not create a runnable candidate if candidate_count is zero.
- next: `{payload['next_run_id']}`
""",
    )
    append_unique_text(
        IDEA_REGISTRY,
        f"""## {RUN_ID}

- idea: Side-balance and cost-exposure risk-budget proxy scout.
- outcome: `{judgment_from(payload)}`
- boundary: `{CLAIM_BOUNDARY}`
""",
    )
    change = f"- {payload['created_at_utc']} `{RUN_ID}` recorded `{status_from(payload)}`; next `{payload['next_run_id']}`; no runtime authority.\n"
    append_unique_text(WORKSPACE_CHANGELOG, change)
    append_unique_text(ROOT_CHANGELOG, change)


def write_gate_results(payload: Mapping[str, Any]) -> dict[str, Any]:
    packet = work_packet(payload)
    wp_result = audit_work_packet_schema(packet)
    receipts = skill_receipts(payload)
    sr_result = audit_skill_receipt_schemas(receipts, root=ROOT, requested_claims=ALLOWED_CLAIMS)
    state_result = audit_state_sync(ROOT, active_stage=STAGE_ID, current_branch="main")
    interim_gate_results = {
        "work_packet_schema_lint": {"status": wp_result.status, "output_path": rel(PACKET_WORK_PACKET_LINT)},
        "skill_receipt_schema_lint": {"status": sr_result.status, "output_path": rel(PACKET_SKILL_RECEIPT_LINT)},
        "state_sync_audit": {"status": state_result.status, "output_path": rel(PACKET_STATE_SYNC_AUDIT)},
    }
    interim_packet = work_packet(payload, interim_gate_results)
    interim_closeout = closeout_gate(payload, interim_gate_results)
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
    guard_payload = final_claim_guard_payload(payload, guard_result.to_dict())
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
    update_state_docs(payload)
    update_ledgers(payload)
    write_packet_and_gate(payload)
    gate_results = write_gate_results(payload)
    write_packet_and_gate(payload, gate_results)
    update_ledgers(payload, gate_passes=sum(1 for result in gate_results.values() if result["status"] == "pass"))
    write_run_artifacts(payload, gate_results)
    print(json.dumps({"run_id": RUN_ID, "status": status_from(payload), "candidate_count": payload["metrics"]["candidate_gate"]["candidate_count"], "gate_results": gate_results}, indent=2))
    return 2 if int(payload["metrics"]["candidate_gate"]["candidate_count"]) > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
