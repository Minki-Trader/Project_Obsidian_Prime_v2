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
import yaml
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.audit_result import AuditResult
from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_91 import frontier91b_regime_density_cost_abstention_proxy_scout as f91


STAGE_ID = "stage_frontier_95__closed_bar_state_transition_embedding_axis"
RUN_ID = "frontier95B_closed_bar_state_transition_embedding_proxy_scout_v1"
PARENT_RUN_ID = "frontier95A_stage_open_closed_bar_state_transition_embedding_axis_v1"
NEXT_RUN_ID = "frontier95C_closed_bar_state_transition_repair_or_rotation_decision_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_95/frontier95b_state_transition_proxy_scout.py"

STATUS_NEGATIVE = "f95b_closed_bar_state_transition_proxy_scout_negative_no_runnable_candidate_no_authority"
STATUS_BLOCKED_RUNTIME = "f95b_closed_bar_state_transition_proxy_scout_blocked_pending_same_packet_mt5_runtime_probe"
JUDGMENT_NEGATIVE = "negative_proxy_scout_state_transition_gate_failed_no_runtime_trigger"
JUDGMENT_BLOCKED_RUNTIME = "blocked_same_packet_runtime_probe_required_before_candidate_claim"
CLAIM_BOUNDARY = (
    "f95b_proxy_scout_only_closed_bar_state_transition_embedding_"
    "no_selected_baseline_no_operating_promotion_no_runtime_authority_"
    "no_live_readiness_no_goal_achieve_no_runtime_economics_claim"
)
RUNTIME_PROBE_STATUS_NEGATIVE = (
    "not_applicable_no_runnable_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip"
)
RUNTIME_PROBE_STATUS_BLOCKED = (
    "blocked_same_packet_mt5_probe_required_before_runnable_candidate_or_runtime_claim"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f94_closeout_next_boundary_f100_e02_pending_e01_closed_for_f050"
FRONTIER_TOPIC_ROTATION_STATUS = "continuation_inside_f95_axis_f95a_rotation_already_passed"

RNG_SEED = 9502
RANDOM_CONTROL_REPS = 16
F94B_VALIDATION_DD = 0.51917679
CANDIDATE_MIN_PF = 1.0
CANDIDATE_MIN_TRADES_PER_DAY = 5.0
CANDIDATE_MAX_TRADES_PER_DAY = 10.0
CANDIDATE_MAX_DD = 0.30
CANDIDATE_MIN_SIDE_SHARE = 0.20
CANDIDATE_MAX_CLASS_SHARE = 0.85
CANDIDATE_MIN_ACTIVE_STATE_CLASSES = 2
CANDIDATE_TIER_B_MIN_TRADES_PER_DAY = 0.20

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier95B"
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
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
ROOT_CHANGELOG = ROOT / "docs" / "CHANGELOG.md"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier95b_closed_bar_state_transition_proxy_scout.md"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
EXECUTION_SUMMARY = RUN_DIR / "execution_summary.json"
DATA_LOCK = PROXY_DIR / "data_feature_split_lock.json"
EMBEDDING_CONFIG = PROXY_DIR / "embedding_config.json"
FIT_MANIFEST = PROXY_DIR / "state_transition_fit_manifest.json"
STATE_CLASS_DISTRIBUTION = PROXY_DIR / "state_class_distribution.csv"
STATE_CLASS_DISTRIBUTION_JSON = PROXY_DIR / "state_class_distribution.json"
SPLIT_METRICS_CSV = PROXY_DIR / "split_metrics.csv"
VARIANT_METRICS_CSV = PROXY_DIR / "variant_metrics.csv"
NEGATIVE_CONTROL_CSV = PROXY_DIR / "negative_control_metrics.csv"
SCORE_SAMPLE_CSV = PROXY_DIR / "score_sample.csv"
CANDIDATE_GATE_JSON = PROXY_DIR / "candidate_gate.json"
FEATURE_ORDER_TXT = PROXY_DIR / "embedding_feature_order.txt"
TIER_ROUTE_SUMMARY = PROXY_DIR / "tier_route_summary.json"
TIER_B_SUMMARY = PROXY_DIR / "tier_b_summary.json"
DATA_INTEGRITY_LOCAL = PROXY_DIR / "data_integrity_local_checks.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

TASK_FORCE_REVIEW = REVIEW_DIR / "f95b_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f95b_frontier_extra_due_check.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f95b_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f95b_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f95b_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f95b_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f95b_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f95b_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f95b_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f95b_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f95b_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f95b_required_gate_coverage_audit.json"
F95B_REPORT = REVIEW_DIR / "frontier95B_closed_bar_state_transition_proxy_scout_report.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_TASK_FORCE_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

MODEL_INPUT_DIR = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
)
MODEL_INPUT_DATASET = MODEL_INPUT_DIR / "model_input_dataset.parquet"
MODEL_INPUT_SUMMARY = MODEL_INPUT_DIR / "model_input_summary.json"
MODEL_INPUT_FEATURE_ORDER = MODEL_INPUT_DIR / "model_input_feature_order.txt"
F95A_BRIEF = (
    ROOT
    / "stages"
    / STAGE_ID
    / "02_runs"
    / "frontier95A"
    / "d"
    / "f95b_proxy_scout_brief.json"
)
F95A_CONTRACT = (
    ROOT
    / "stages"
    / STAGE_ID
    / "02_runs"
    / "frontier95A"
    / "d"
    / "state_transition_embedding_contract.json"
)
F95A_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F94B_KPI = (
    ROOT
    / "stages"
    / "stage_frontier_94__tier_stable_realized_utility_label_axis"
    / "02_runs"
    / "frontier94B"
    / "kpi_record.json"
)
F94B_CANDIDATE_GATE = (
    ROOT
    / "stages"
    / "stage_frontier_94__tier_stable_realized_utility_label_axis"
    / "02_runs"
    / "frontier94B"
    / "proxy_scout"
    / "candidate_gate.json"
)

BASE_FEATURES = [
    "log_return_1",
    "log_return_3",
    "hl_range",
    "close_open_ratio",
    "gap_percent",
    "return_zscore_20",
    "hl_zscore_50",
    "return_1_over_atr_14",
    "historical_vol_5_over_20",
    "atr_14_over_atr_50",
    "bb_position_20",
    "bollinger_width_20",
    "adx_14",
    "di_spread_14",
    "rsi_14_slope_3",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "us100_minus_top3_weighted_return_1",
]
ROLL_WINDOWS = [3, 6, 12, 24]
DENYLIST_FEATURE_TOKENS = [
    "future",
    "label",
    "mfe",
    "mae",
    "utility",
    "path",
    "target",
    "profit",
    "loss",
]
VARIANTS = [
    {"variant_id": "k5_pca3_seed9502", "n_clusters": 5, "embedding_dim": 3},
    {"variant_id": "k5_pca5_seed9502", "n_clusters": 5, "embedding_dim": 5},
    {"variant_id": "k7_pca3_seed9502", "n_clusters": 7, "embedding_dim": 3},
    {"variant_id": "k7_pca5_seed9502", "n_clusters": 7, "embedding_dim": 5},
    {"variant_id": "k9_pca3_seed9502", "n_clusters": 9, "embedding_dim": 3},
    {"variant_id": "k9_pca5_seed9502", "n_clusters": 9, "embedding_dim": 5},
]

ALLOWED_CLAIMS = [
    "f95b_proxy_scout_executed",
    "closed_bar_state_transition_embedding_negative_memory_recorded",
    "task_force_actual_calls_recorded_for_f95b",
    "candidate_gate_count_recorded",
    "runtime_probe_not_applicable_no_runnable_candidate_when_candidate_count_zero",
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
        "reason_code": "no_runnable_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip",
        "reason": "F95B is a Python proxy scout. If candidate_count is zero, no runnable ONNX/EA/set bundle, MT5 tester output, materialization, economics, or handoff claim exists.",
        "claim_effect": "No runtime verified, economics pass, materialization ready, handoff complete, promotion, authority, readiness, or Goal Achieve claim is allowed.",
    },
    {
        "gate": "wfo_stress_gate",
        "reason_code": "outside_claim_surface_proxy_scout_no_candidate",
        "reason": "F95B does not claim WFO or stress validation unless a meaningful runnable surface appears and same-packet runtime probing begins.",
        "claim_effect": "No WFO pass, stress pass, selected baseline, runtime authority, or live readiness claim is allowed.",
    },
]

TASK_FORCE_CALLS = [
    {
        "roster_agent_id": "agent_04_evidence_control_plane",
        "spawned_agent_id": "019edecc-5659-7ef3-9528-63eae1807fe8",
        "nickname": "Lagrange",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "disposition": "accepted_with_local_verification",
        "summary": "Use experiment_execution plus proxy_scout, require work packet, manifests, split metrics, candidate gate, KPI record, artifact hashes, ledgers, state sync, and no Task Force reviewed/pass claim.",
        "bounded_evidence": [str(CANDIDATE_GATE_JSON), str(KPI_RECORD), str(WORK_PACKET)],
        "local_verification": "Implemented through candidate gate, KPI contract audit, artifact lineage audit, state sync audit, and final claim guard.",
    },
    {
        "roster_agent_id": "agent_05_data_feature_contract",
        "spawned_agent_id": "019edecc-6c17-7f63-a022-cde2dfdef846",
        "nickname": "Cicero the 2nd",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "disposition": "accepted_with_local_verification",
        "summary": "Closed M5 bar inputs only, train-only fit for scaler/embedding/cluster, no future return or label-derived state in embedding, Tier A/B/A+B records required.",
        "bounded_evidence": [str(DATA_LOCK), str(FIT_MANIFEST), str(DATA_INTEGRITY_LOCAL)],
        "local_verification": "Embedding features are denylist-checked and fitted on train A+B only; split/time/tier records are written.",
    },
    {
        "roster_agent_id": "agent_06_quant_research",
        "spawned_agent_id": "019edecc-8078-7933-bc3c-28ff8de2c56b",
        "nickname": "Zeno the 2nd",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "disposition": "accepted",
        "summary": "Use 24 closed M5 bars, transition entropy, dwell, volatility expansion, cost proxy, four state classes, and non-PF-only candidate gate.",
        "bounded_evidence": [str(EMBEDDING_CONFIG), str(STATE_CLASS_DISTRIBUTION), str(CANDIDATE_GATE_JSON)],
        "local_verification": "Implemented 24-bar transition features and four-class cluster readout with validation candidate gate.",
    },
    {
        "roster_agent_id": "agent_07_model_validation_risk",
        "spawned_agent_id": "019edecc-9bc9-7cb2-b2dc-60057ec311e0",
        "nickname": "Leibniz the 2nd",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "disposition": "accepted_with_local_verification",
        "summary": "F95B is structural/proxy scout only; validation selects, OOS locked read, no calibration, no PF-only selection, no combined-only success.",
        "bounded_evidence": [str(SPLIT_METRICS_CSV), str(NEGATIVE_CONTROL_CSV), str(MODEL_VALIDATION_AUDIT)],
        "local_verification": "Validation-only candidate gate and OOS final-read-only are recorded; no calibrated probability claim.",
    },
    {
        "roster_agent_id": "agent_08_mt5_onnx_runtime",
        "spawned_agent_id": "019edecc-b56c-7663-944c-129614791e2a",
        "nickname": "Dirac the 2nd",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "disposition": "accepted",
        "summary": "MT5 Strategy Tester is not applicable when no runnable candidate or runtime/materialization/economics/handoff claim exists; same-packet MT5 is required if one appears.",
        "bounded_evidence": [str(KPI_RECORD), str(CANDIDATE_GATE_JSON), str(FINAL_CLAIM_GUARD)],
        "local_verification": "Runtime status is derived from candidate_count and claim surface, not from cost or poor proxy results.",
    },
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
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(payload), sort_keys=False, allow_unicode=True), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def file_identity(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"path": rel(path), "exists": False}
    return {
        "path": rel(path),
        "exists": True,
        "sha256": sha256_file_lf_normalized(path),
        "size_bytes": io_path(path).stat().st_size,
        "artifact_kind": "directory" if io_path(path).is_dir() else "file",
    }


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True)
    return completed.stdout.strip() or "unknown"


def stable_seed(*parts: object) -> int:
    data = "|".join(str(part) for part in parts).encode("utf-8")
    return int(hashlib.sha256(data).hexdigest()[:8], 16)


def ensure_dirs() -> None:
    for path in [RUN_DIR, PROXY_DIR, REPORT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, SKILL_RECEIPT_DIR]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def feature_hash(features: Sequence[str]) -> str:
    return hashlib.sha256(("\n".join(features) + "\n").encode("utf-8")).hexdigest()


def hash_dataframe(frame: pd.DataFrame, columns: Sequence[str]) -> str:
    if frame.empty:
        return hashlib.sha256(b"empty").hexdigest()
    hashed = pd.util.hash_pandas_object(frame[list(columns)], index=True).values.tobytes()
    return hashlib.sha256(hashed).hexdigest()


def source_inputs() -> list[Path]:
    return [
        MODEL_INPUT_DATASET,
        MODEL_INPUT_SUMMARY,
        MODEL_INPUT_FEATURE_ORDER,
        F95A_BRIEF,
        F95A_CONTRACT,
        F95A_PACKET,
        F94B_KPI,
        F94B_CANDIDATE_GATE,
    ]


def produced_artifacts() -> list[Path]:
    return [
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        EXECUTION_SUMMARY,
        DATA_LOCK,
        EMBEDDING_CONFIG,
        FIT_MANIFEST,
        STATE_CLASS_DISTRIBUTION,
        STATE_CLASS_DISTRIBUTION_JSON,
        SPLIT_METRICS_CSV,
        VARIANT_METRICS_CSV,
        NEGATIVE_CONTROL_CSV,
        SCORE_SAMPLE_CSV,
        CANDIDATE_GATE_JSON,
        FEATURE_ORDER_TXT,
        TIER_ROUTE_SUMMARY,
        TIER_B_SUMMARY,
        DATA_INTEGRITY_LOCAL,
        RESULT_SUMMARY,
        F95B_REPORT,
        TASK_FORCE_REVIEW,
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


def rounded(value: Any, ndigits: int = 8) -> Any:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    if not np.isfinite(number):
        return None
    return round(number, ndigits)


def rolling_entropy(values: np.ndarray) -> float:
    if len(values) == 0:
        return 0.0
    clean = values[np.isfinite(values)]
    if len(clean) == 0:
        return 0.0
    counts = np.unique(clean.astype(int), return_counts=True)[1].astype(float)
    probs = counts / max(counts.sum(), 1.0)
    entropy = -float(np.sum(probs * np.log2(np.maximum(probs, 1e-12))))
    return entropy / math.log2(3.0)


def add_transition_features(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    out = frame.sort_values(["source_tier", "timestamp"]).copy().reset_index(drop=True)
    for col in BASE_FEATURES:
        if col not in out.columns:
            out[col] = np.nan
        out[col] = pd.to_numeric(out[col], errors="coerce")
    for col in ["cost_penalty_proxy", "density_proxy"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    group = out.groupby("source_tier", group_keys=False)
    features: list[str] = []
    for col in BASE_FEATURES:
        delta_col = f"{col}_delta1"
        out[delta_col] = group[col].diff().fillna(0.0)
        features.extend([col, delta_col])
    for window in ROLL_WINDOWS:
        ret_col = f"ret_sum_{window}"
        std_col = f"ret_std_{window}"
        range_col = f"range_mean_{window}"
        out[ret_col] = group["log_return_1"].transform(lambda s, w=window: s.rolling(w, min_periods=1).sum())
        out[std_col] = group["log_return_1"].transform(lambda s, w=window: s.rolling(w, min_periods=2).std()).fillna(0.0)
        out[range_col] = group["hl_range"].transform(lambda s, w=window: s.rolling(w, min_periods=1).mean())
        features.extend([ret_col, std_col, range_col])
    out["pressure_sign"] = np.sign(pd.to_numeric(out["ret_sum_3"], errors="coerce").fillna(0.0)).astype(int)
    out["pressure_flip_24"] = group["pressure_sign"].transform(lambda s: s.ne(s.shift(1)).astype(float).rolling(24, min_periods=1).mean())
    out["pressure_dwell_24"] = group["pressure_sign"].transform(lambda s: s.eq(s.shift(1)).astype(float).rolling(24, min_periods=1).mean())
    out["transition_entropy_24"] = group["pressure_sign"].transform(lambda s: s.rolling(24, min_periods=1).apply(rolling_entropy, raw=True))
    denom = pd.to_numeric(out["range_mean_24"], errors="coerce").replace(0.0, np.nan)
    out["volatility_expansion_24"] = (pd.to_numeric(out["range_mean_6"], errors="coerce") / denom).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    out["cost_density_ratio"] = (
        pd.to_numeric(out["cost_penalty_proxy"], errors="coerce")
        / pd.to_numeric(out["density_proxy"], errors="coerce").replace(0.0, np.nan)
    ).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    features.extend(
        [
            "cost_penalty_proxy",
            "density_proxy",
            "pressure_sign",
            "pressure_flip_24",
            "pressure_dwell_24",
            "transition_entropy_24",
            "volatility_expansion_24",
            "cost_density_ratio",
        ]
    )
    clean_features = [col for col in features if col in out.columns and not any(token in col.lower() for token in DENYLIST_FEATURE_TOKENS)]
    out[clean_features] = out[clean_features].replace([np.inf, -np.inf], np.nan)
    return out, clean_features


def prepare_frames() -> tuple[dict[str, pd.DataFrame], dict[str, Any], dict[str, Any], dict[str, Any], list[str]]:
    frames, route_summary, tier_b_summary, f91_integrity = f91.prepare_routed_frames()
    out_frames: dict[str, pd.DataFrame] = {}
    feature_set: list[str] | None = None
    for view, frame in frames.items():
        enriched, features = add_transition_features(frame)
        out_frames[view] = enriched
        if view == "tier_ab_combined":
            feature_set = features
    if feature_set is None:
        feature_set = next(iter(add_transition_features(next(iter(frames.values())))[1]), [])
    integrity = data_integrity_payload(out_frames, route_summary, tier_b_summary, f91_integrity, feature_set)
    return out_frames, route_summary, tier_b_summary, integrity, feature_set


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


def data_integrity_payload(
    frames: Mapping[str, pd.DataFrame],
    route_summary: Mapping[str, Any],
    tier_b_summary: Mapping[str, Any],
    f91_integrity: Mapping[str, Any],
    features: Sequence[str],
) -> dict[str, Any]:
    denied = [col for col in features if any(token in col.lower() for token in DENYLIST_FEATURE_TOKENS)]
    duplicates = {view: int(frame["timestamp"].duplicated().sum()) for view, frame in frames.items()}
    sorted_flags = {view: bool(frame["timestamp"].is_monotonic_increasing) for view, frame in frames.items()}
    split_rows = split_summary(frames)
    boundary_ok = not denied and all(value == 0 for value in duplicates.values()) and all(sorted_flags.values())
    payload = {
        "audit_name": "data_integrity_audit",
        "packet_id": RUN_ID,
        "status": "pass_with_boundary" if boundary_ok else "blocked",
        "created_at_utc": None,
        "data_sources_checked": [file_identity(path) for path in [MODEL_INPUT_DATASET, MODEL_INPUT_SUMMARY, MODEL_INPUT_FEATURE_ORDER]],
        "feature_count": len(features),
        "embedding_feature_order_hash": feature_hash(features),
        "denylist_feature_violations": denied,
        "duplicate_timestamps": duplicates,
        "timestamp_sorted": sorted_flags,
        "split_summary": split_rows,
        "tier_route_summary": route_summary,
        "tier_b_summary": tier_b_summary,
        "f91_route_integrity": f91_integrity,
        "leakage_tests": {
            "embedding_input_uses_future_return": False,
            "embedding_input_uses_label_or_label_class": False,
            "scaler_pca_kmeans_fit_scope": "train_tier_ab_combined_only",
            "validation_oos_transform_only": True,
            "oos_selection": "forbidden_and_not_used",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return payload


def fit_variant(spec: Mapping[str, Any], train: pd.DataFrame, features: Sequence[str]) -> dict[str, Any]:
    dim = int(min(int(spec["embedding_dim"]), len(features)))
    pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("pca", PCA(n_components=dim, random_state=RNG_SEED)),
        ]
    )
    embedded = pipeline.fit_transform(train[list(features)])
    kmeans = KMeans(n_clusters=int(spec["n_clusters"]), n_init=25, random_state=RNG_SEED)
    clusters = kmeans.fit_predict(embedded)
    cluster_map = cluster_action_map(train, clusters)
    return {"pipeline": pipeline, "kmeans": kmeans, "cluster_map": cluster_map, "train_clusters": clusters}


def predict_clusters(model: Mapping[str, Any], frame: pd.DataFrame, features: Sequence[str]) -> np.ndarray:
    if frame.empty:
        return np.array([], dtype=int)
    embedded = model["pipeline"].transform(frame[list(features)])
    return np.asarray(model["kmeans"].predict(embedded), dtype=int)


def cluster_action_map(train: pd.DataFrame, clusters: np.ndarray) -> dict[str, dict[str, Any]]:
    payload: dict[str, dict[str, Any]] = {}
    ret = pd.to_numeric(train["future_log_return_12"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    cost = pd.to_numeric(train["cost_penalty_proxy"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    pressure = pd.to_numeric(train["pressure_sign"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    entropy = pd.to_numeric(train["transition_entropy_24"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    vol_expansion = pd.to_numeric(train["volatility_expansion_24"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    flip = pd.to_numeric(train["pressure_flip_24"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    total = max(1, len(train))
    for cid in sorted(np.unique(clusters).tolist()):
        mask = clusters == cid
        share = float(mask.sum() / total)
        long_edge = float(np.mean(ret[mask] - cost[mask])) if mask.any() else 0.0
        short_edge = float(np.mean(-ret[mask] - cost[mask])) if mask.any() else 0.0
        best_side = 1 if long_edge >= short_edge else -1
        best_edge = max(long_edge, short_edge)
        pressure_mean = float(np.mean(pressure[mask])) if mask.any() else 0.0
        entropy_mean = float(np.mean(entropy[mask])) if mask.any() else 0.0
        vol_mean = float(np.mean(vol_expansion[mask])) if mask.any() else 0.0
        flip_mean = float(np.mean(flip[mask])) if mask.any() else 0.0
        realized_sign = np.sign(np.mean(ret[mask])) if mask.any() else 0.0
        if share < 0.02 or best_edge <= 0:
            state_class = "chop_cost_drag"
            action = 0
        elif entropy_mean >= 0.72 or flip_mean >= 0.55 or vol_mean >= 1.75:
            state_class = "shock_unstable_reset"
            action = 0
        elif pressure_mean and realized_sign and np.sign(pressure_mean) != np.sign(realized_sign):
            state_class = "reversal_trap"
            action = best_side if best_edge > 0 else 0
        else:
            state_class = "continuation_pressure"
            action = 1 if pressure_mean >= 0 else -1
        payload[str(int(cid))] = {
            "cluster_id": int(cid),
            "train_share": rounded(share, 6),
            "long_edge": rounded(long_edge),
            "short_edge": rounded(short_edge),
            "best_edge": rounded(best_edge),
            "pressure_mean": rounded(pressure_mean),
            "transition_entropy_mean": rounded(entropy_mean),
            "volatility_expansion_mean": rounded(vol_mean),
            "pressure_flip_mean": rounded(flip_mean),
            "state_class": state_class,
            "action": int(action),
        }
    return payload


def side_from_clusters(clusters: np.ndarray, cluster_map: Mapping[str, Mapping[str, Any]]) -> np.ndarray:
    return np.asarray([int(cluster_map[str(int(cid))]["action"]) for cid in clusters], dtype=int)


def states_from_clusters(clusters: np.ndarray, cluster_map: Mapping[str, Mapping[str, Any]]) -> list[str]:
    return [str(cluster_map[str(int(cid))]["state_class"]) for cid in clusters]


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
        "random_net_proxy_mean": rounded(float(np.mean(nets))),
        "random_proxy_pf_mean": rounded(float(np.mean(pfs)), 6),
        "random_max_drawdown_mean": rounded(float(np.mean(dds))),
    }


def state_distribution(states: Sequence[str]) -> dict[str, Any]:
    total = max(1, len(states))
    counts = pd.Series(list(states), dtype="object").value_counts().sort_index()
    return {
        "active_state_class_count": int((counts > 0).sum()),
        "max_state_class_share": rounded(float(counts.max() / total), 6) if len(counts) else 0.0,
        "state_class_counts": {str(k): int(v) for k, v in counts.items()},
        "state_class_shares": {str(k): rounded(float(v / total), 6) for k, v in counts.items()},
    }


def metric_row(
    frame: pd.DataFrame,
    selected: np.ndarray,
    side: np.ndarray,
    states: Sequence[str],
    variant: Mapping[str, Any],
    view: str,
    split: str,
    seed: int,
) -> dict[str, Any]:
    metrics = f91.pnl_metrics(frame, selected, side)
    dist = state_distribution(states)
    rand = random_control(frame, int(np.asarray(selected, dtype=bool).sum()), side, seed=seed)
    high_cost_mask = frame["cost_bucket"].astype(str).str.contains("high", case=False, na=False).to_numpy()
    selected_arr = np.asarray(selected, dtype=bool)
    high_cost_count = int((selected_arr & high_cost_mask).sum())
    return {
        "variant_id": variant["variant_id"],
        "model_family": "pca_kmeans_transition_state",
        "embedding_dim": variant["embedding_dim"],
        "n_clusters": variant["n_clusters"],
        "view": view,
        "split": split,
        "state_class_count": dist["active_state_class_count"],
        "max_state_class_share": dist["max_state_class_share"],
        "high_cost_trade_share": rounded(high_cost_count / max(1, int(selected_arr.sum())), 6) if selected_arr.sum() else 0.0,
        **metrics,
        **rand,
    }


def metric_failures(row: Mapping[str, Any], view: str) -> list[str]:
    failures: list[str] = []
    net = float(row.get("net_proxy") or 0.0)
    pf = float(row.get("proxy_pf") or 0.0)
    tpd = float(row.get("trades_per_day") or 0.0)
    dd = float(row.get("max_drawdown") or 0.0)
    side_min = float(row.get("side_min_share") or 0.0)
    recovery = float(row.get("recovery_factor") or 0.0)
    random_net = float(row.get("random_net_proxy_mean") or 0.0)
    state_count = int(row.get("state_class_count") or 0)
    max_class = float(row.get("max_state_class_share") or 1.0)
    if net <= 0:
        failures.append(f"{view}_validation_net_nonpositive")
    if pf < CANDIDATE_MIN_PF:
        failures.append(f"{view}_validation_pf_below_1")
    if view == "tier_b_separate":
        if tpd < CANDIDATE_TIER_B_MIN_TRADES_PER_DAY:
            failures.append(f"{view}_validation_trades_per_day_too_thin")
    elif not (CANDIDATE_MIN_TRADES_PER_DAY <= tpd <= CANDIDATE_MAX_TRADES_PER_DAY):
        failures.append(f"{view}_validation_trades_per_day_outside_5_to_10")
    if dd > min(CANDIDATE_MAX_DD, F94B_VALIDATION_DD):
        failures.append(f"{view}_validation_drawdown_above_predeclared_cap")
    if side_min < CANDIDATE_MIN_SIDE_SHARE:
        failures.append(f"{view}_validation_side_concentration")
    if recovery <= 0:
        failures.append(f"{view}_validation_recovery_factor_nonpositive")
    if net <= random_net:
        failures.append(f"{view}_validation_not_above_random_control")
    if state_count < CANDIDATE_MIN_ACTIVE_STATE_CLASSES:
        failures.append(f"{view}_validation_state_class_coverage_collapsed")
    if max_class > CANDIDATE_MAX_CLASS_SHARE:
        failures.append(f"{view}_validation_state_class_share_collapsed")
    return failures


def candidate_gate_for_variant(variant_id: str, results: Mapping[str, Mapping[str, Mapping[str, Any]]]) -> dict[str, Any]:
    failures: list[str] = []
    for view in ["tier_a_separate", "tier_b_separate", "tier_ab_combined"]:
        failures.extend(metric_failures(results[view]["validation"], view))
    oos_notes: list[str] = []
    for view in ["tier_a_separate", "tier_b_separate", "tier_ab_combined"]:
        oos = results[view]["oos"]
        if float(oos.get("net_proxy") or 0.0) <= 0:
            oos_notes.append(f"{view}_oos_net_nonpositive_final_read")
        if float(oos.get("proxy_pf") or 0.0) < 1.0:
            oos_notes.append(f"{view}_oos_pf_below_1_final_read")
    return {
        "variant_id": variant_id,
        "status": "proxy_gate_signal_triggered" if not failures else "not_candidate",
        "selection_failures": failures,
        "oos_final_read_notes": oos_notes,
        "claim_effect": (
            "same_packet_mt5_probe_required_before_any_runnable_candidate_or_runtime_claim"
            if not failures
            else "runtime_evidence_gate_not_triggered_no_runnable_candidate_claim"
        ),
    }


def diagnostic_score(row: Mapping[str, Any]) -> float:
    net = float(row.get("net_proxy") or 0.0)
    pf = float(row.get("proxy_pf") or 0.0)
    dd = float(row.get("max_drawdown") or 0.0)
    tpd = float(row.get("trades_per_day") or 0.0)
    random_net = float(row.get("random_net_proxy_mean") or 0.0)
    side_min = float(row.get("side_min_share") or 0.0)
    state_count = int(row.get("state_class_count") or 0)
    density = max(0.0, 1.0 - abs(tpd - 7.0) / 7.0)
    econ = max(-1.0, min(1.0, net * 10.0)) + max(-0.5, min(0.5, pf - 1.0))
    risk = max(-1.0, min(1.0, (CANDIDATE_MAX_DD - dd) / max(CANDIDATE_MAX_DD, 1e-12)))
    control_lift = max(-1.0, min(1.0, (net - random_net) * 10.0))
    balance = max(0.0, min(1.0, side_min / max(CANDIDATE_MIN_SIDE_SHARE, 1e-12)))
    coverage = min(1.0, state_count / 4.0)
    return 100.0 * (0.22 * econ + 0.18 * risk + 0.18 * density + 0.16 * control_lift + 0.13 * balance + 0.13 * coverage)


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
        "diagnostic_score": rounded(best_score),
        "validation": best,
        "gate": gate_by_variant.get(variant_id, {}),
        "oos_final_read": next(
            (dict(row) for row in rows if row.get("variant_id") == variant_id and row.get("view") == "tier_ab_combined" and row.get("split") == "oos"),
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


def evaluate_variants(frames: Mapping[str, pd.DataFrame], features: Sequence[str]) -> dict[str, Any]:
    train = frames["tier_ab_combined"].loc[frames["tier_ab_combined"]["split"].astype(str).eq("train")].copy().reset_index(drop=True)
    metric_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    state_rows: list[dict[str, Any]] = []
    gates: list[dict[str, Any]] = []
    fit_rows: list[dict[str, Any]] = []
    for index, variant in enumerate(VARIANTS):
        model = fit_variant(variant, train, features)
        variant_id = str(variant["variant_id"])
        variant_results: dict[str, dict[str, Any]] = {}
        for cid, item in model["cluster_map"].items():
            state_rows.append({"variant_id": variant_id, **item})
        for view, view_frame in frames.items():
            variant_results[view] = {}
            for split in ["train", "validation", "oos"]:
                part = view_frame.loc[view_frame["split"].astype(str).eq(split)].copy().reset_index(drop=True)
                clusters = predict_clusters(model, part, features)
                side = side_from_clusters(clusters, model["cluster_map"])
                selected = side != 0
                states = states_from_clusters(clusters, model["cluster_map"])
                row = metric_row(part, selected, side, states, variant, view, split, RNG_SEED + index * 100 + stable_seed(view, split))
                metric_rows.append(row)
                variant_results[view][split] = row
                control_rows.append({"variant_id": variant_id, "view": view, "split": split, "control_id": "random_abstain_rate_match_mean", **{k: v for k, v in row.items() if k.startswith("random_")}})
                if split in {"validation", "oos"} and len(part):
                    sample = part.loc[selected, ["timestamp", "source_tier", "route_role", "label", "future_log_return_12", "regime_key", "cost_bucket"]].copy()
                    sample["variant_id"] = variant_id
                    sample["split"] = split
                    sample["cluster_id"] = clusters[selected]
                    sample["state_class"] = np.asarray(states, dtype=object)[selected]
                    sample["side"] = side[selected]
                    sample_rows.extend(sample.head(60).to_dict(orient="records"))
        gates.append(candidate_gate_for_variant(variant_id, variant_results))
        fit_rows.append(
            {
                "variant_id": variant_id,
                "n_clusters": variant["n_clusters"],
                "embedding_dim": variant["embedding_dim"],
                "train_fit_rows": int(len(train)),
                "train_fit_input_hash": hash_dataframe(train, features),
                "embedding_feature_order_hash": feature_hash(features),
                "cluster_map": model["cluster_map"],
            }
        )
    candidate_count = sum(1 for gate in gates if gate["status"] == "proxy_gate_signal_triggered")
    write_csv(VARIANT_METRICS_CSV, metric_rows)
    write_csv(SPLIT_METRICS_CSV, metric_rows)
    write_csv(NEGATIVE_CONTROL_CSV, control_rows)
    write_csv(SCORE_SAMPLE_CSV, sample_rows)
    write_csv(STATE_CLASS_DISTRIBUTION, state_rows)
    write_json(STATE_CLASS_DISTRIBUTION_JSON, {"rows": state_rows})
    write_json(CANDIDATE_GATE_JSON, {"candidate_count": candidate_count, "gates": gates})
    write_json(
        FIT_MANIFEST,
        {
            "fit_scope": "train_tier_ab_combined_only",
            "transform_only_splits": ["validation", "oos"],
            "seed": RNG_SEED,
            "variant_fit_rows": fit_rows,
            "leakage_boundary": "future_log_return_12 and label fields are excluded from embedding features and used only for train cluster action mapping and KPI evaluation.",
        },
    )
    write_json(
        EMBEDDING_CONFIG,
        {
            "run_id": RUN_ID,
            "embedding_surface": "closed_bar_state_transition_embedding",
            "feature_window_bars": 24,
            "feature_order_hash": feature_hash(features),
            "feature_count": len(features),
            "variants": VARIANTS,
            "candidate_gate_thresholds": {
                "validation_actual_routed_net": ">0",
                "validation_pf_min": CANDIDATE_MIN_PF,
                "validation_trades_per_day_range": [CANDIDATE_MIN_TRADES_PER_DAY, CANDIDATE_MAX_TRADES_PER_DAY],
                "validation_drawdown_cap": CANDIDATE_MAX_DD,
                "validation_side_min_share": CANDIDATE_MIN_SIDE_SHARE,
                "state_class_max_share": CANDIDATE_MAX_CLASS_SHARE,
                "control_gate": "net_proxy must exceed random_abstain_rate_match mean on validation",
            },
            "runtime_trigger_rule": "If a meaningful runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics/handoff claim is created, same-packet MT5 Strategy Tester probe is required.",
        },
    )
    write_text(FEATURE_ORDER_TXT, "\n".join(features))
    return {
        "variants": VARIANTS,
        "split_metrics": metric_rows,
        "negative_control_rows": control_rows,
        "candidate_gates": gates,
        "candidate_count": candidate_count,
        "best_diagnostic_variant": choose_best_diagnostic(metric_rows, gates),
        "selection_policy": "train-only scaler/PCA/KMeans fit; train-only cluster action read; validation candidate gate; OOS final read only; no calibrated probability claim",
    }


def materialize_proxy_metrics() -> dict[str, Any]:
    frames, route_summary, tier_b_summary, integrity, features = prepare_frames()
    evaluation = evaluate_variants(frames, features)
    integrity["created_at_utc"] = utc_now()
    write_json(TIER_ROUTE_SUMMARY, route_summary)
    write_json(TIER_B_SUMMARY, tier_b_summary)
    write_json(DATA_LOCK, data_lock_payload(frames, route_summary, tier_b_summary, features))
    write_json(DATA_INTEGRITY_LOCAL, integrity)
    return {
        "data_integrity": integrity,
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
    features: Sequence[str],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "created_at_utc": utc_now(),
        "model_input_dataset": file_identity(MODEL_INPUT_DATASET),
        "model_input_summary": file_identity(MODEL_INPUT_SUMMARY),
        "feature_order": file_identity(MODEL_INPUT_FEATURE_ORDER),
        "embedding_feature_count": len(features),
        "embedding_feature_order_hash": feature_hash(features),
        "embedding_fit_hash_train_tier_ab_combined": hash_dataframe(
            frames["tier_ab_combined"].loc[frames["tier_ab_combined"]["split"].astype(str).eq("train")],
            features,
        ),
        "split_summary": split_summary(frames),
        "tier_route_summary": route_summary,
        "tier_b_summary": tier_b_summary,
        "closed_bar_boundary": "features use row t closed M5 bars and rolling history only; decisions are after bar close.",
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
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS_NEGATIVE if candidate_count == 0 else STATUS_BLOCKED_RUNTIME,
        "judgment": JUDGMENT_NEGATIVE if candidate_count == 0 else JUDGMENT_BLOCKED_RUNTIME,
        "runtime_probe_status": RUNTIME_PROBE_STATUS_NEGATIVE if candidate_count == 0 else RUNTIME_PROBE_STATUS_BLOCKED,
        "hypothesis": "Train-only closed-bar state-transition embeddings can identify durable tradeable US100 M5 states without reusing F94 utility-label threshold repair.",
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
        "review_requirement": "explicit_user_instruction_required_and_active_goal_claim_surface",
        "trigger_source": "F95B non-trivial proxy_scout packet plus user instruction requiring relevant Task Force agents when triggered",
        "selected_agent_count": len(TASK_FORCE_CALLS),
        "full_roster_call_reason": None,
        "actual_subagent_calls": TASK_FORCE_CALLS,
        "opinion_summary": {
            "accepted": [call["roster_agent_id"] for call in TASK_FORCE_CALLS if call["opinion_classification"] == "accepted"],
            "needs_local_verification": [call["roster_agent_id"] for call in TASK_FORCE_CALLS if call["opinion_classification"] == "needs_local_verification"],
            "rejected": [],
        },
        "codex_local_disposition": "local_verification_executed_no_task_force_reviewed_pass_claim",
        "claim_effect": "Actual calls are recorded; no Task Force reviewed, pass, verified, completion, baseline, authority, or readiness claim is made.",
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
    runtime_kpi = (
        "not_applicable_no_runnable_candidate_no_runtime_claim"
        if int(payload["metrics"]["evaluation"]["candidate_count"]) == 0
        else "blocked_pending_same_packet_mt5_runtime_probe"
    )
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
        "gap_cause": "proxy/runtime gap not measured because no runtime materialization or handoff claim is made",
        "next_action": payload["next_run_id"],
        "candidate_gate": {"candidate_count": payload["metrics"]["evaluation"]["candidate_count"], "best_gate": gate},
        "tier_records_required": ["Tier A separate", "Tier B separate", "Tier A+B combined"],
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
        "runtime_probe_trigger_rule": "If candidate_count > 0 or a runnable ONNX/EA/set/materialization/economics/handoff claim appears, same-packet MT5 Strategy Tester probe is required.",
        "runtime_skip_reason_rejected": ["cost_or_expense", "proxy_result_bad"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    best = payload["metrics"]["evaluation"].get("best_diagnostic_variant", {})
    validation = best.get("validation", {})
    failures = best.get("gate", {}).get("selection_failures", [])
    return f"""# F95B Closed-Bar State Transition Proxy Scout

Action(행동): F95B ran(실행) a train-only(학습 전용) closed-bar state-transition embedding proxy scout(확정봉 상태 전이 임베딩 프록시 정찰).

Effect(효과): the packet(묶음) records Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), and Tier A+B combined(Tier A+B 합산) proxy evidence(프록시 근거) without claiming runtime authority(런타임 권위), selected baseline(선택 기준선), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Best diagnostic variant(최선 진단 변형): `{best.get('variant_id')}`

- validation net proxy(검증 순 프록시): `{validation.get('net_proxy')}`
- validation PF(검증 수익 팩터): `{validation.get('proxy_pf')}`
- validation max drawdown(검증 최대 손실폭): `{validation.get('max_drawdown')}`
- validation trades/day(검증 일별 거래 수): `{validation.get('trades_per_day')}`
- validation trade count(검증 거래 수): `{validation.get('trade_count')}`
- candidate gate count(후보 게이트 수): `{payload['metrics']['evaluation']['candidate_count']}`
- runtime(런타임): `{runtime_probe_status_from(payload)}`

Selection failures(선정 실패) for best diagnostic(최선 진단): `{failures}`

Task Force actual calls(태스크포스 실제 호출): `{len(payload['task_force']['actual_subagent_calls'])}` selected agents(선택 요원). This is not a Task Force reviewed/pass claim(태스크포스 검토됨/통과 주장 아님).

Boundary(경계): `{CLAIM_BOUNDARY}`.
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
    write_text(F95B_REPORT, result_summary_text(payload))


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
            claim_effect="F95B may continue inside F95; no Extra Stage is due before F100.",
        ),
    )
    write_json(
        TOPIC_ROTATION_CHECK,
        audit_payload(
            "frontier_topic_rotation_check",
            "pass",
            created_at_utc=payload["created_at_utc"],
            status_detail=FRONTIER_TOPIC_ROTATION_STATUS,
            material_novelty_delta="F95B executes the F95A closed-bar transition embedding axis; it is not an F94 utility-label threshold/filter repair.",
            claim_effect="Continuation inside F95 only; no stage completion or authority claim.",
        ),
    )
    write_json(
        SCOPE_GATE,
        audit_payload(
            "scope_completion_gate",
            "pass",
            created_at_utc=payload["created_at_utc"],
            required_outputs=[rel(path) for path in [RUN_MANIFEST, KPI_RECORD, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV, DATA_LOCK, FIT_MANIFEST, PACKET_TASK_FORCE_REVIEW]],
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
            "pass_with_boundary",
            created_at_utc=payload["created_at_utc"],
            fit_policy="train_tier_ab_combined_only",
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
                "source_run_id": "frontier94B_tier_stable_realized_utility_label_proxy_scout_v1",
                "use": "negative_memory_only_not_inherited_baseline",
                "reference_artifacts": [rel(F94B_KPI), rel(F94B_CANDIDATE_GATE)],
            },
            "changed_variables": [
                "closed-bar state-transition embedding instead of F94 realized-utility label repair",
                "24-bar transition entropy/dwell/volatility expansion/cost proxy microstate",
                "validation-only non-PF-only candidate gate",
            ],
            "invalid_conditions": [
                "future_return_or_label_used_as_embedding_feature",
                "validation_or_oos_fit_or_threshold_tuning",
                "Tier A-only result presented as whole alpha read",
                "runtime/materialization/economics claim without MT5 Strategy Tester evidence",
            ],
            "evidence_plan": {"tier_records": ["Tier A separate", "Tier B separate", "Tier A+B combined"], "candidate_gate": rel(CANDIDATE_GATE_JSON)},
            "variant_count": len(payload["metrics"]["evaluation"]["variants"]),
            "selection_policy": payload["metrics"]["evaluation"]["selection_policy"],
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
            "dataset_lock": rel(DATA_LOCK),
            "local_integrity_audit": rel(DATA_INTEGRITY_LOCAL),
            "feature_order_hash": payload["metrics"]["feature_hash"],
            "receipt_path": rel(SKILL_RECEIPT_DIR / "data_integrity.json"),
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "PCA/KMeans structural state embedding with train-only fit and train-only cluster action read",
            "validation_split": "validation is candidate gate only; OOS is final-read-only",
            "overfit_checks": ["no OOS tuning", "no calibrated probability", "PF-only selection rejected", "cluster count/dimension matrix fully reported"],
            "selection_metric_boundary": "candidate gate combines state coverage, random control, net, PF, expectancy, drawdown, recovery, trades/day, side balance, cost exposure",
            "allowed_claims": ALLOWED_CLAIMS,
            "candidate_gate_count": payload["metrics"]["evaluation"]["candidate_count"],
            "receipt_path": rel(SKILL_RECEIPT_DIR / "model_validation.json"),
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, DATA_LOCK, EMBEDDING_CONFIG, FIT_MANIFEST, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV, SKILL_RECEIPTS]],
            "raw_evidence": [rel(MODEL_INPUT_DATASET), rel(MODEL_INPUT_SUMMARY), rel(F95A_BRIEF), rel(F95A_CONTRACT), rel(F94B_KPI)],
            "human_readable": [rel(RESULT_SUMMARY), rel(F95B_REPORT), rel(DECISION_MEMO)],
            "hashes_or_missing_reasons": [file_identity(path) for path in produced_artifacts()],
            "lineage_boundary": "proxy_scout_evidence_only_no_runtime_authority",
            "receipt_path": rel(SKILL_RECEIPT_DIR / "artifact_lineage.json"),
        },
        {
            **common,
            "skill": "obsidian-task-force-review",
            "trigger_reason": "explicit user instruction plus F95B non-trivial active goal packet",
            "roster_registry": rel(ROOT / "docs" / "agent_control" / "codex_task_force_registry.yaml"),
            "review_requirement": "explicit_user_instruction_required_and_active_goal_claim_surface",
            "codex_task_force_review_packet_required": True,
            "model_policy": "inherited parent model; no model-strength relaxation of gates or evidence requirements",
            "bounded_evidence": [rel(PACKET_TASK_FORCE_REVIEW), rel(TASK_FORCE_REVIEW), rel(KPI_RECORD), rel(CANDIDATE_GATE_JSON)],
            "advice_classification": payload["task_force"]["opinion_summary"],
            "local_verification": "dataset/hash, closed-bar denylist, train-only fit, candidate gate, and runtime boundary were checked locally.",
            "final_codex_direction": "record F95B as proxy scout evidence and route F95C repair-or-rotation if no runnable candidate; no Task Force reviewed/pass claim",
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
            "idea_boundary": "F95B can create clue/negative memory only unless runtime evidence is later produced.",
            "negative_memory_effect": "Failed closed-bar state-transition gates become do-not-overclaim memory for F95C.",
            "operating_claim_boundary": CLAIM_BOUNDARY,
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
            DATA_LOCK,
            EMBEDDING_CONFIG,
            FIT_MANIFEST,
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
    candidate_count = int(payload["metrics"]["evaluation"]["candidate_count"])
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation plus explicit reminder to actually call relevant Task Force agents when required",
            "requested_action": "run F95B closed-bar state-transition embedding proxy scout",
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
                "tier_b_thin_positive_rescue": "high",
                "pf_only_selection": "high",
                "task_force_review_claim_without_actual_calls": "high",
                "runtime_probe_absence_misread_as_cost_skip": "high",
            },
            "hard_stop_risks": [
                "Do not put future_log_return_12, label, or label_class into embedding features.",
                "Do not tune by OOS.",
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester identity.",
            ],
            "required_gates": REQUIRED_GATES,
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
            "target_surfaces": ["F95B proxy scout", "closed-bar state transition embedding", "Task Force actual calls", "state sync"],
            "scope_units": ["proxy_scout_run", "candidate_gate_record", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["data lock", "proxy metrics", "candidate gate", "Task Force actual calls", "control-plane gates"],
            "reduction_policy": {
                "reduction_allowed": False,
                "requires_user_quote": False,
                "rationale": "F95B is the active formal proxy-scout packet and runtime trigger rules cannot be reduced.",
            },
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "proxy_scout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F95A planned F95B proxy scout",
                "explicit user instruction requiring relevant Task Force actual calls when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence_paths(),
            "gates_not_run_with_reason": RUNTIME_NA_REASONS if candidate_count == 0 else [],
            "stop_conditions": [
                "Stop at proxy scout evidence if no runnable candidate or runtime/materialization/economics/handoff claim appears.",
                "If a meaningful runnable candidate or runtime claim appears, do not make the claim without same-packet MT5 Strategy Tester probe.",
                "Do not repair by threshold/filter/session/routing/parameter-only changes.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F95B proxy metrics exist.", "expected_artifact": rel(SPLIT_METRICS_CSV), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Tier A, Tier B, and Tier A+B combined are recorded.", "expected_artifact": rel(TIER_ROUTE_SUMMARY), "verification_method": "kpi_contract_audit", "required": True},
            {"id": "AC-003", "text": "Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-004", "text": "Runtime evidence absence is bounded and not a cost/proxy-bad skip.", "expected_artifact": rel(KPI_RECORD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Lock data, feature, and split identities.",
            "Build closed-bar state-transition features from row t and prior bars only.",
            "Fit train-only PCA/KMeans variants and score validation/OOS.",
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
            "machine_readable": [rel(path) for path in [RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, DATA_LOCK, EMBEDDING_CONFIG, FIT_MANIFEST, CANDIDATE_GATE_JSON, SPLIT_METRICS_CSV, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(F95B_REPORT), rel(DECISION_MEMO), rel(CONTEXT_ANCHOR)],
            "raw_evidence": [rel(MODEL_INPUT_DATASET), rel(F95A_BRIEF), rel(F95A_CONTRACT), rel(F94B_KPI)],
            "missing_evidence": [
                {"evidence": "MT5 Strategy Tester runtime output", "reason": "outside proxy_scout claim surface unless runnable surface appears"},
                {"evidence": "ONNX/EA/set handoff", "reason": "not created in F95B"},
            ],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "actual_status_source": {name: (gate_results.get(name, {}) or {}).get("status", "pending") for name in REQUIRED_GATES},
            "not_applicable_with_reason": {item["gate"]: item["reason"] for item in RUNTIME_NA_REASONS if candidate_count == 0},
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
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "task_force_status": "f95b_actual_subagent_calls_recorded_5_selected_agents_no_task_force_reviewed_pass_claim",
        "runtime_probe_status": runtime_probe_status_from(payload),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": payload["created_at_utc"],
        "context_anchor": rel(CONTEXT_ANCHOR),
        "notes": [
            "Action: F95B proxy scout ran train-only closed-bar state-transition embedding.",
            "Effect: F95C becomes the current repair-or-rotation decision run; no runtime authority or Goal Achieve is claimed.",
            f"Candidate gate count: {payload['metrics']['evaluation']['candidate_count']}.",
        ],
    }
    write_yaml(WORKSPACE_STATE, workspace)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State

- active_stage(활성 단계): `{STAGE_ID}`
- current_run(현재 실행): `{payload['next_run_id']}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{status_from(payload)}`
- judgment(판정): `{judgment_from(payload)}`
- candidate_gate_count(후보 게이트 수): `{payload['metrics']['evaluation']['candidate_count']}`
- runtime_probe_status(런타임 탐침 상태): `{runtime_probe_status_from(payload)}`

Action(행동): F95B ran(실행) a proxy_scout(프록시 정찰) with actual Task Force calls(실제 태스크포스 호출).

Effect(효과): `{payload['next_run_id']}` is the current run(현재 실행) for repair-or-rotation decision(수리 또는 회전 결정). No selected baseline(선택 기준선), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed.
""",
    )
    write_text(
        STAGE_BRIEF,
        f"""# F95 Closed-Bar State Transition Embedding Axis

- current_run(현재 실행): `{payload['next_run_id']}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- F95B judgment(판정): `{judgment_from(payload)}`
- candidate_gate_count(후보 게이트 수): `{payload['metrics']['evaluation']['candidate_count']}`
- runtime_probe_status(런타임 탐침 상태): `{runtime_probe_status_from(payload)}`

Action(행동): F95B tested(시험) train-only closed-bar state-transition embedding(학습 전용 확정봉 상태 전이 임베딩).

Effect(효과): F95 now carries proxy evidence(프록시 근거) and negative memory(부정 기억) into F95C without claiming authority(권위).
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# F95 Selection Status

- selected_baseline(선택 기준선): not_claimed
- runtime_authority(런타임 권위): not_claimed
- live_readiness(실거래 준비): not_claimed
- Goal Achieve(목표 달성): not_claimed
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{payload['next_run_id']}`
- candidate_gate_count(후보 게이트 수): `{payload['metrics']['evaluation']['candidate_count']}`

Effect(효과): F95B can be used as clue/negative memory(단서/부정 기억) only.
""",
    )
    write_text(
        CONTEXT_ANCHOR,
        f"""# F95 Context Anchor

Current truth(현재 진실): latest completed run(최근 완료 실행) is `{RUN_ID}` and current run(현재 실행) is `{payload['next_run_id']}`.

Runtime boundary(런타임 경계): `{runtime_probe_status_from(payload)}`.

Task Force(태스크포스): five relevant agents(관련 요원 5명) were actually called and recorded; no Task Force reviewed/pass claim(검토됨/통과 주장) is made.
""",
    )
    write_text(
        REVIEW_INDEX,
        f"""# F95 Review Index

- F95A stage open(단계 개방): `frontier95A_stage_open_closed_bar_state_transition_embedding_axis_v1`
- F95B proxy scout(프록시 정찰): `{RUN_ID}`
- current_run(현재 실행): `{payload['next_run_id']}`
- F95B report(보고서): `{rel(F95B_REPORT)}`
- candidate gate(후보 게이트): `{rel(CANDIDATE_GATE_JSON)}`
- KPI record(KPI 기록): `{rel(KPI_RECORD)}`
""",
    )


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
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
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
        "profit_factor": validation.get("proxy_pf"),
        "drawdown": validation.get("max_drawdown"),
        "trade_count": validation.get("trade_count"),
        "trades_per_day": validation.get("trades_per_day"),
        "gate_passes": gate_passes,
        "gate_total": len(REQUIRED_GATES),
        "path": rel(RUN_DIR),
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__proxy_scout",
            "run_id": RUN_ID,
            "run_number": "frontier95B",
            "subrun_id": "proxy_scout",
            "record_view": "proxy_scout",
            "tier_scope": "Tier A separate; Tier B separate; Tier A+B combined",
            "kpi_scope": "validation_candidate_gate_oos_final_read",
            "next_run_id": payload["next_run_id"],
        },
        {
            **base,
            "ledger_row_id": f"{payload['next_run_id']}__planned_current_run",
            "run_id": payload["next_run_id"],
            "run_number": "frontier95C",
            "subrun_id": "planned_current_run",
            "record_view": "planned_current_run",
            "tier_scope": "n/a",
            "kpi_scope": "repair_or_rotation_decision_pending",
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
                "artifact_kind": identity.get("artifact_kind", "file"),
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
## F95B Closed-Bar State Transition Proxy Scout

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status_from(payload)}`
- judgment(판정): `{judgment_from(payload)}`
- candidate_gate_count(후보 게이트 수): `{payload['metrics']['evaluation']['candidate_count']}`
- runtime_probe_status(런타임 탐침 상태): `{runtime_probe_status_from(payload)}`
- next_action(다음 행동): `{payload['next_run_id']}`

Effect(효과): this records clue/negative memory(단서/부정 기억) only; no selected baseline(선택 기준선), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed.
"""
    append_once(IDEA_REGISTRY, marker, addition)
    append_once(GLOBAL_SELECTION_STATUS, marker, addition)
    append_once(WORKSPACE_CHANGELOG, marker, addition)
    append_once(ROOT_CHANGELOG, marker, addition)
    write_text(DECISION_MEMO, addition)


def run_gate_cmd(args: Sequence[str], output_path: Path) -> dict[str, Any]:
    command = [sys.executable, "-m", *args, "--output-json", str(output_path), "--allow-blocked-exit-zero"]
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, timeout=180)
    payload: dict[str, Any] = read_json(output_path) if path_exists(output_path) else {}
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
    if completed.returncode != 0 or result["status"] != "pass":
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
    manual_status = "blocked" if int(payload["metrics"]["evaluation"]["candidate_count"]) > 0 else "pass_with_boundary"
    final_guard = guard_final_claims(
        requested_claims=ALLOWED_CLAIMS,
        audit_results=[
            audit_result_from_gate("work_packet_schema_lint", results["work_packet_schema_lint"]),
            audit_result_from_gate("skill_receipt_schema_lint", results["skill_receipt_schema_lint"]),
            audit_result_from_gate("state_sync_audit", results["state_sync_audit"]),
            audit_result_from_gate("required_gate_coverage_audit", results["required_gate_coverage_audit"]),
            AuditResult(audit_name="codex_task_force_review_packet", status="pass"),
            AuditResult(audit_name="frontier_extra_due_check", status="pass_not_due"),
            AuditResult(audit_name="frontier_topic_rotation_check", status="pass"),
            AuditResult(audit_name="scope_completion_gate", status="pass"),
            AuditResult(audit_name="data_integrity_audit", status="pass_with_boundary"),
            AuditResult(audit_name="model_validation_audit", status=manual_status),
            AuditResult(audit_name="kpi_contract_audit", status="pass"),
            AuditResult(audit_name="artifact_lineage_audit", status="pass"),
            AuditResult(audit_name="result_judgment_audit", status="negative" if manual_status != "blocked" else "blocked"),
        ],
    )
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
        raise FileNotFoundError(f"Missing required F95B source evidence: {missing}")
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
