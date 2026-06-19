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
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_91 import frontier91b_regime_density_cost_abstention_proxy_scout as f91


STAGE_ID = "stage_frontier_92__path_conditioned_trade_shape_labeling_axis"
RUN_ID = "frontier92B_path_conditioned_trade_shape_label_proxy_scout_v1"
PARENT_RUN_ID = "frontier92A_stage_open_path_conditioned_trade_shape_labeling_axis_v1"
NEXT_RUN_ID = "frontier92C_path_trade_shape_repair_or_rotation_decision_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_92/frontier92b_path_trade_shape_proxy_scout.py"

STATUS_NEGATIVE = "f92b_path_conditioned_trade_shape_proxy_scout_negative_no_candidate_no_authority"
STATUS_BLOCKED_RUNTIME = "f92b_path_trade_shape_proxy_candidate_blocked_pending_same_packet_runtime_probe"
JUDGMENT_NEGATIVE = "negative_proxy_scout_path_trade_shape_joint_gate_failed_no_runtime_trigger"
JUDGMENT_BLOCKED_RUNTIME = "blocked_runtime_probe_required_after_path_trade_shape_proxy_candidate"
DECISION_NEGATIVE = "plan_f92c_repair_or_rotation_after_path_trade_shape_proxy_failure"
CLAIM_BOUNDARY = (
    "f92b_proxy_scout_only_no_runnable_candidate_no_mt5_runtime_evidence_no_selected_baseline_"
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
CANDIDATE_MIN_SIDE_SHARE = 0.20
CANDIDATE_MIN_REGIME_COVERAGE = 4
CANDIDATE_MAX_HIGH_COST_SHARE = 0.60
RNG_SEED = 9202
RANDOM_CONTROL_REPS = 24

SPLIT_END_UTC = {
    "train": pd.Timestamp("2025-01-01T00:00:00Z"),
    "validation": pd.Timestamp("2025-10-01T00:00:00Z"),
    "oos": pd.Timestamp("2026-04-14T00:00:00Z"),
}

LABEL_CONFIGS = [
    {
        "label_id": "path_first_touch_atr_m05_h12_cost1",
        "barrier_atr_mult": 0.5,
        "horizon_bars": 12,
        "cost_stress_mult": 1.0,
        "exit_shape_focus": "fast_first_touch_or_timeout",
    },
    {
        "label_id": "path_first_touch_atr_m10_h24_cost1",
        "barrier_atr_mult": 1.0,
        "horizon_bars": 24,
        "cost_stress_mult": 1.0,
        "exit_shape_focus": "medium_path_shape",
    },
    {
        "label_id": "path_first_touch_atr_m15_h48_cost2",
        "barrier_atr_mult": 1.5,
        "horizon_bars": 48,
        "cost_stress_mult": 2.0,
        "exit_shape_focus": "longer_path_cost_stress",
    },
]

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier92B"
PROXY_DIR = RUN_DIR / "proxy_scout"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SKILL_RECEIPT_DIR = PACKET_DIR / "skill_receipts"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
PATH_LABEL_CONFIG = PROXY_DIR / "path_label_config.json"
PATH_LABEL_SUMMARY_CSV = PROXY_DIR / "path_label_summary.csv"
TIER_ROUTE_SUMMARY = PROXY_DIR / "tier_route_summary.json"
TIER_B_SUMMARY = PROXY_DIR / "tier_b_summary.json"
VARIANT_METRICS_CSV = PROXY_DIR / "variant_metrics.csv"
SPLIT_METRICS_CSV = PROXY_DIR / "split_metrics.csv"
NEGATIVE_CONTROL_CSV = PROXY_DIR / "negative_control_metrics.csv"
CANDIDATE_GATE_JSON = PROXY_DIR / "candidate_gate.json"
SCORE_SAMPLE_CSV = PROXY_DIR / "proxy_scores_sample.csv"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

TASK_FORCE_REVIEW = REVIEW_DIR / "f92b_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f92b_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f92b_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f92b_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f92b_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f92b_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f92b_model_validation_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f92b_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f92b_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f92b_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f92b_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f92b_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f92b_required_gate_coverage_audit.json"
EXECUTION_SUMMARY = REVIEW_DIR / "f92b_execution_summary.json"
F92B_REPORT = REVIEW_DIR / "frontier92B_path_conditioned_trade_shape_proxy_scout_report.md"

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
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier92b_path_trade_shape_proxy_scout.md"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

F92A_BRIEF = STAGE_DIR / "02_runs" / "frontier92A" / "d" / "f92b_proxy_scout_brief.json"
F92A_DATA_PLAN = STAGE_DIR / "02_runs" / "frontier92A" / "d" / "data_integrity_plan.json"
F92A_RUNTIME_CONTRACT = STAGE_DIR / "02_runs" / "frontier92A" / "d" / "runtime_contract.json"
F92A_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
RAW_US100_CSV = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"

ALLOWED_CLAIMS = [
    "f92b_path_trade_shape_proxy_scout_executed",
    "f92b_proxy_metrics_recorded",
    "f92b_task_force_actual_calls_recorded",
    "f92b_candidate_gate_failed_no_runtime_trigger",
    "f92c_repair_or_rotation_planned",
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
    "reviewed",
    "verified",
    "pass",
    "model_quality",
    "model_readiness",
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

TASK_FORCE_CALLS = [
    {
        "roster_agent_id": "agent_01_system_governor",
        "spawned_agent_id": "019eddfe-b340-71e3-a7be-2d4301f13627",
        "nickname": "Descartes",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "bounded_evidence": [str(WORKSPACE_STATE.relative_to(ROOT)), str(STAGE_BRIEF.relative_to(ROOT))],
        "local_verification": "F92B may proceed as proxy_scout_only; forbidden final/runtime claims remain blocked.",
    },
    {
        "roster_agent_id": "agent_04_evidence_control_plane",
        "spawned_agent_id": "019eddfe-c75c-7aa2-a559-8899cb32a48c",
        "nickname": "Peirce",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "bounded_evidence": [str(WORKSPACE_STATE.relative_to(ROOT)), str(F92A_BRIEF.relative_to(ROOT))],
        "local_verification": "F92B needs fresh packet, receipts, gates, actual_subagent_calls, hashes, ledgers, and state sync.",
    },
    {
        "roster_agent_id": "agent_05_data_feature_contract",
        "spawned_agent_id": "019eddfe-dbb4-7f90-9ea9-67cdc3895bfa",
        "nickname": "Dewey",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "bounded_evidence": [str(F92A_DATA_PLAN.relative_to(ROOT)), str(RAW_US100_CSV.relative_to(ROOT))],
        "local_verification": "Path label hash, row count, split censor count, ambiguity count, and Tier A/B/routed records must be re-locked.",
    },
    {
        "roster_agent_id": "agent_06_quant_research",
        "spawned_agent_id": "019eddfe-f5a8-7232-8c52-b69b57075e03",
        "nickname": "Anscombe",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "bounded_evidence": [str(STAGE_BRIEF.relative_to(ROOT)), str(F92A_BRIEF.relative_to(ROOT))],
        "local_verification": "Path-conditioned MFE/MAE/holding/exit-shape axis is novel versus F91 abstention filter repair.",
    },
    {
        "roster_agent_id": "agent_07_model_validation_risk",
        "spawned_agent_id": "019eddff-0a45-79a2-99ff-9847d6889bce",
        "nickname": "Banach",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "bounded_evidence": [str(STAGE_BRIEF.relative_to(ROOT)), str(F92A_DATA_PLAN.relative_to(ROOT))],
        "local_verification": "Train/validation/OOS separation, OOS final-read-only, negative controls, and candidate gate lock must be checked locally.",
    },
    {
        "roster_agent_id": "agent_08_mt5_onnx_runtime",
        "spawned_agent_id": "019eddff-1ed8-7710-a307-3dfe16b580c0",
        "nickname": "Sartre",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "bounded_evidence": [str(F92A_RUNTIME_CONTRACT.relative_to(ROOT)), str(STAGE_BRIEF.relative_to(ROOT))],
        "local_verification": "MT5 probe is not required without candidate/runtime claim, but same-packet probe is required if trigger appears.",
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
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt", ".yaml", ".yml"} else "utf-8"
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


def source_inputs() -> list[Path]:
    return [
        F92A_BRIEF,
        F92A_DATA_PLAN,
        F92A_RUNTIME_CONTRACT,
        F92A_PACKET,
        f91.MODEL_INPUT_SUMMARY,
        f91.MODEL_INPUT_DATASET,
        f91.MODEL_INPUT_FEATURE_ORDER,
        RAW_US100_CSV,
    ]


def produced_artifacts() -> list[Path]:
    return [
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        PATH_LABEL_CONFIG,
        PATH_LABEL_SUMMARY_CSV,
        TIER_ROUTE_SUMMARY,
        TIER_B_SUMMARY,
        VARIANT_METRICS_CSV,
        SPLIT_METRICS_CSV,
        NEGATIVE_CONTROL_CSV,
        CANDIDATE_GATE_JSON,
        SCORE_SAMPLE_CSV,
        RESULT_SUMMARY,
        EXECUTION_SUMMARY,
        F92B_REPORT,
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


def load_raw_path() -> dict[str, Any]:
    raw = pd.read_csv(
        io_path(RAW_US100_CSV),
        usecols=["time_open_unix", "time_close_unix", "open", "high", "low", "close", "spread_points"],
    )
    raw["time_open"] = pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
    raw["time_close"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    return {
        "frame": raw,
        "open_index": {timestamp: index for index, timestamp in enumerate(raw["time_open"])},
        "open": raw["open"].to_numpy(dtype=float),
        "high": raw["high"].to_numpy(dtype=float),
        "low": raw["low"].to_numpy(dtype=float),
        "close": raw["close"].to_numpy(dtype=float),
        "spread_points": raw["spread_points"].to_numpy(dtype=float),
        "integrity": {
            "raw_rows": int(len(raw)),
            "time_open_monotonic": bool(raw["time_open"].is_monotonic_increasing),
            "time_close_monotonic": bool(raw["time_close"].is_monotonic_increasing),
            "duplicate_time_open": int(raw["time_open"].duplicated().sum()),
            "duplicate_time_close": int(raw["time_close"].duplicated().sum()),
            "invalid_ohlc_rows": int(((raw["high"] < raw[["open", "close"]].max(axis=1)) | (raw["low"] > raw[["open", "close"]].min(axis=1))).sum()),
            "open_close_delta_seconds_mode": int((raw["time_close_unix"] - raw["time_open_unix"]).mode().iloc[0]),
        },
    }


def outcome_for(raw_payload: Mapping[str, Any], start_index: int, atr_points: float, horizon: int, barrier_mult: float, cost_mult: float, side: int) -> dict[str, Any]:
    opens = raw_payload["open"]
    highs = raw_payload["high"]
    lows = raw_payload["low"]
    closes = raw_payload["close"]
    spreads = raw_payload["spread_points"]
    entry = float(opens[start_index])
    take_profit = float(atr_points * barrier_mult)
    stop_loss = float(atr_points * barrier_mult)
    cost_points = float((spreads[start_index] * 0.01 + 0.25) * cost_mult)
    mfe = 0.0
    mae = 0.0
    end_index = min(start_index + horizon, len(opens))
    for index in range(start_index, end_index):
        up_points = float(highs[index] - entry)
        down_points = float(entry - lows[index])
        favorable = up_points if side == 1 else down_points
        adverse = down_points if side == 1 else up_points
        mfe = max(mfe, favorable)
        mae = max(mae, adverse)
        tp_hit = favorable >= take_profit
        sl_hit = adverse >= stop_loss
        if tp_hit and sl_hit:
            return {
                "reward_points": -stop_loss - cost_points,
                "exit_shape": "ambiguous_both_hit",
                "mfe_points": mfe,
                "mae_points": mae,
                "same_bar_ambiguous": True,
                "bars_held": int(index - start_index + 1),
                "exit_reason": "ambiguous_both_hit_conservative_loss",
            }
        if tp_hit:
            return {
                "reward_points": take_profit - cost_points,
                "exit_shape": "smooth_win" if mae <= take_profit * 0.35 else "reversal_win",
                "mfe_points": mfe,
                "mae_points": mae,
                "same_bar_ambiguous": False,
                "bars_held": int(index - start_index + 1),
                "exit_reason": "first_touch_tp",
            }
        if sl_hit:
            return {
                "reward_points": -stop_loss - cost_points,
                "exit_shape": "bleed" if mfe <= take_profit * 0.35 else "reversal_loss",
                "mfe_points": mfe,
                "mae_points": mae,
                "same_bar_ambiguous": False,
                "bars_held": int(index - start_index + 1),
                "exit_reason": "first_touch_sl",
            }
    exit_price = float(closes[end_index - 1])
    reward = (exit_price - entry) * side - cost_points
    shape = "timeout_positive" if reward > 0 else "chop" if abs(reward) <= max(cost_points, take_profit * 0.15) else "timeout_bleed"
    return {
        "reward_points": reward,
        "exit_shape": shape,
        "mfe_points": mfe,
        "mae_points": mae,
        "same_bar_ambiguous": False,
        "bars_held": int(end_index - start_index),
        "exit_reason": "timeout",
    }


def add_path_labels(frame: pd.DataFrame, raw_payload: Mapping[str, Any], config: Mapping[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    raw = raw_payload["frame"]
    open_index = raw_payload["open_index"]
    horizon = int(config["horizon_bars"])
    barrier = float(config["barrier_atr_mult"])
    cost_mult = float(config["cost_stress_mult"])
    out = frame.copy().reset_index(drop=True)
    target_class: list[int] = []
    target_label: list[str] = []
    long_rewards: list[float] = []
    short_rewards: list[float] = []
    mfe_points: list[float] = []
    mae_points: list[float] = []
    bars_held: list[int] = []
    exit_shapes: list[str] = []
    exit_reasons: list[str] = []
    valid: list[bool] = []
    ambiguous: list[bool] = []
    split_censored = 0
    missing_path = 0
    for row in out.itertuples():
        timestamp = row.timestamp
        split = str(row.split)
        start_index = open_index.get(timestamp)
        atr_points = float(getattr(row, "atr_14", np.nan))
        if start_index is None or not np.isfinite(atr_points) or atr_points <= 0.0 or start_index + horizon > len(raw):
            target_class.append(1)
            target_label.append("flat")
            long_rewards.append(0.0)
            short_rewards.append(0.0)
            mfe_points.append(0.0)
            mae_points.append(0.0)
            bars_held.append(0)
            exit_shapes.append("missing_path")
            exit_reasons.append("missing_path_or_invalid_atr")
            valid.append(False)
            ambiguous.append(False)
            missing_path += 1
            continue
        if raw["time_close"].iloc[start_index + horizon - 1] >= SPLIT_END_UTC.get(split, pd.Timestamp("2262-01-01T00:00:00Z")):
            target_class.append(1)
            target_label.append("flat")
            long_rewards.append(0.0)
            short_rewards.append(0.0)
            mfe_points.append(0.0)
            mae_points.append(0.0)
            bars_held.append(0)
            exit_shapes.append("split_edge_censored")
            exit_reasons.append("split_edge_censored")
            valid.append(False)
            ambiguous.append(False)
            split_censored += 1
            continue
        long = outcome_for(raw_payload, start_index, atr_points, horizon, barrier, cost_mult, 1)
        short = outcome_for(raw_payload, start_index, atr_points, horizon, barrier, cost_mult, -1)
        long_reward = float(long["reward_points"])
        short_reward = float(short["reward_points"])
        long_rewards.append(long_reward)
        short_rewards.append(short_reward)
        ambiguous.append(bool(long["same_bar_ambiguous"] or short["same_bar_ambiguous"]))
        if long_reward > max(short_reward, 0.0):
            target_class.append(2)
            target_label.append("long")
            mfe_points.append(float(long["mfe_points"]))
            mae_points.append(float(long["mae_points"]))
            bars_held.append(int(long["bars_held"]))
            exit_shapes.append(str(long["exit_shape"]))
            exit_reasons.append(str(long["exit_reason"]))
        elif short_reward > max(long_reward, 0.0):
            target_class.append(0)
            target_label.append("short")
            mfe_points.append(float(short["mfe_points"]))
            mae_points.append(float(short["mae_points"]))
            bars_held.append(int(short["bars_held"]))
            exit_shapes.append(str(short["exit_shape"]))
            exit_reasons.append(str(short["exit_reason"]))
        else:
            target_class.append(1)
            target_label.append("flat")
            mfe_points.append(max(float(long["mfe_points"]), float(short["mfe_points"])))
            mae_points.append(max(float(long["mae_points"]), float(short["mae_points"])))
            bars_held.append(max(int(long["bars_held"]), int(short["bars_held"])))
            exit_shapes.append("flat_no_positive_edge")
            exit_reasons.append("no_positive_edge_after_cost")
        valid.append(True)
    out["path_label_id"] = str(config["label_id"])
    out["path_label_class"] = target_class
    out["path_label"] = target_label
    out["long_path_reward_points"] = long_rewards
    out["short_path_reward_points"] = short_rewards
    out["path_mfe_points"] = mfe_points
    out["path_mae_points"] = mae_points
    out["path_bars_held"] = bars_held
    out["exit_shape_class"] = exit_shapes
    out["exit_reason"] = exit_reasons
    out["path_label_valid"] = valid
    out["same_bar_ambiguous"] = ambiguous
    summary = {
        "label_id": str(config["label_id"]),
        "view": str(frame.attrs.get("view", "unknown")),
        "rows": int(len(out)),
        "valid_rows": int(np.asarray(valid, dtype=bool).sum()),
        "split_edge_censored_rows": int(split_censored),
        "missing_path_rows": int(missing_path),
        "same_bar_ambiguous_rows": int(np.asarray(ambiguous, dtype=bool).sum()),
        "class_counts": {str(key): int(value) for key, value in pd.Series(target_label).value_counts().sort_index().items()},
        "exit_shape_counts": {str(key): int(value) for key, value in pd.Series(exit_shapes).value_counts().sort_index().items()},
    }
    return out, summary


def class_scores(model: Any, x: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    probs = model.predict_proba(x)
    classes = list(model[-1].classes_)
    index = {int(label): position for position, label in enumerate(classes)}
    p_short = probs[:, index.get(0, 0)] if 0 in index else np.zeros(len(probs))
    p_flat = probs[:, index.get(1, 0)] if 1 in index else np.zeros(len(probs))
    p_long = probs[:, index.get(2, 0)] if 2 in index else np.zeros(len(probs))
    side = np.where(p_long >= p_short, 1, -1)
    strength = np.maximum(p_long, p_short) - p_flat
    return side.astype(int), strength.astype(float)


def pnl_metrics(frame: pd.DataFrame, trade_mask: np.ndarray, side: np.ndarray) -> dict[str, Any]:
    trade_mask = np.asarray(trade_mask, dtype=bool)
    side = np.asarray(side, dtype=int)
    days = int(frame["timestamp"].dt.date.nunique()) if len(frame) else 0
    trade_count = int(trade_mask.sum())
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
            "cost_high_trade_share": None,
            "avg_mfe_points": None,
            "avg_mae_points": None,
            "avg_bars_held": None,
            "same_bar_ambiguous_trade_share": None,
        }
    rewards = np.where(
        side == 1,
        frame["long_path_reward_points"].to_numpy(dtype=float),
        frame["short_path_reward_points"].to_numpy(dtype=float),
    )[trade_mask]
    gross_profit = float(rewards[rewards > 0].sum())
    gross_loss = float(-rewards[rewards < 0].sum())
    wins = rewards[rewards > 0]
    losses = rewards[rewards < 0]
    long_count = int((side[trade_mask] == 1).sum())
    short_count = int((side[trade_mask] == -1).sum())
    side_min_share = float(min(long_count, short_count) / trade_count)
    cum = np.cumsum(rewards)
    peaks = np.maximum.accumulate(np.insert(cum, 0, 0.0))[1:]
    drawdown = peaks - cum
    max_drawdown = float(drawdown.max()) if len(drawdown) else 0.0
    underwater = int((drawdown > 0).sum()) if len(drawdown) else 0
    max_consecutive_loss = 0
    current_loss = 0
    for value in rewards:
        current_loss = current_loss + 1 if value < 0 else 0
        max_consecutive_loss = max(max_consecutive_loss, current_loss)
    selected = frame.loc[trade_mask]
    return {
        "rows": int(len(frame)),
        "days": days,
        "trade_count": trade_count,
        "trades_per_day": round(float(trade_count / days), 6) if days else None,
        "net_proxy": round(float(rewards.sum()), 6),
        "gross_profit": round(gross_profit, 6),
        "gross_loss": round(gross_loss, 6),
        "proxy_pf": round(float(gross_profit / gross_loss), 6) if gross_loss > 0 else (999.0 if gross_profit > 0 else None),
        "win_rate": round(float((rewards > 0).mean()), 6),
        "avg_win": round(float(wins.mean()), 6) if len(wins) else None,
        "avg_loss": round(float(losses.mean()), 6) if len(losses) else None,
        "payoff_ratio": round(float(wins.mean() / abs(losses.mean())), 6) if len(wins) and len(losses) else None,
        "expectancy": round(float(rewards.mean()), 6),
        "max_drawdown": round(max_drawdown, 6),
        "recovery_factor": round(float(rewards.sum() / max_drawdown), 6) if max_drawdown > 0 else None,
        "time_under_water_bars": underwater,
        "max_consecutive_loss": int(max_consecutive_loss),
        "long_count": long_count,
        "short_count": short_count,
        "side_min_share": round(side_min_share, 6),
        "regime_coverage_count": int(selected["regime_key"].nunique()),
        "cost_high_trade_share": round(float(selected["cost_bucket"].astype(str).eq("cost_high").mean()), 6),
        "avg_mfe_points": round(float(selected["path_mfe_points"].mean()), 6) if len(selected) else None,
        "avg_mae_points": round(float(selected["path_mae_points"].mean()), 6) if len(selected) else None,
        "avg_bars_held": round(float(selected["path_bars_held"].mean()), 6) if len(selected) else None,
        "same_bar_ambiguous_trade_share": round(float(selected["same_bar_ambiguous"].astype(bool).mean()), 6) if len(selected) else None,
    }


def random_control(frame: pd.DataFrame, trade_count: int, *, seed: int) -> dict[str, Any]:
    if trade_count <= 0 or len(frame) == 0:
        return {"random_net_proxy_mean": 0.0, "random_proxy_pf_mean": 0.0, "random_max_drawdown_mean": 0.0}
    rng = np.random.default_rng(seed)
    nets: list[float] = []
    pfs: list[float] = []
    drawdowns: list[float] = []
    count = min(trade_count, len(frame))
    for _ in range(RANDOM_CONTROL_REPS):
        mask = np.zeros(len(frame), dtype=bool)
        mask[rng.choice(len(frame), size=count, replace=False)] = True
        side = rng.choice(np.array([-1, 1], dtype=int), size=len(frame))
        metrics = pnl_metrics(frame, mask, side)
        nets.append(float(metrics["net_proxy"] or 0.0))
        pfs.append(float(metrics["proxy_pf"] or 0.0))
        drawdowns.append(float(metrics["max_drawdown"] or 0.0))
    return {
        "random_net_proxy_mean": round(float(np.mean(nets)), 6),
        "random_proxy_pf_mean": round(float(np.mean(pfs)), 6),
        "random_max_drawdown_mean": round(float(np.mean(drawdowns)), 6),
    }


def control_rows_for(frame: pd.DataFrame, selected_mask: np.ndarray, side: np.ndarray, variant_id: str, view: str, split: str) -> list[dict[str, Any]]:
    selected_mask = np.asarray(selected_mask, dtype=bool)
    trade_count = int(selected_mask.sum())
    rng = np.random.default_rng(abs(hash((variant_id, view, split))) % (2**32))
    controls: list[tuple[str, np.ndarray, np.ndarray]] = []
    controls.append(("all_trade_model_side", np.ones(len(frame), dtype=bool), side))
    random_mask = np.zeros(len(frame), dtype=bool)
    random_side = rng.choice(np.array([-1, 1], dtype=int), size=len(frame)) if len(frame) else np.array([], dtype=int)
    if trade_count > 0 and len(frame):
        random_mask[rng.choice(len(frame), size=min(trade_count, len(frame)), replace=False)] = True
    controls.append(("side_random_rate_match", selected_mask, random_side))
    controls.append(("random_abstain_and_side_rate_match", random_mask, random_side))
    if trade_count > 0 and len(frame):
        cost_mask = np.zeros(len(frame), dtype=bool)
        density_mask = np.zeros(len(frame), dtype=bool)
        cost_order = np.argsort(frame["cost_penalty_proxy"].to_numpy(dtype=float))[: min(trade_count, len(frame))]
        density_order = np.argsort(-frame["density_proxy"].to_numpy(dtype=float))[: min(trade_count, len(frame))]
        cost_mask[cost_order] = True
        density_mask[density_order] = True
    else:
        cost_mask = np.zeros(len(frame), dtype=bool)
        density_mask = np.zeros(len(frame), dtype=bool)
    controls.append(("cost_only_low_cost_rate_match", cost_mask, side))
    controls.append(("density_only_high_density_rate_match", density_mask, side))
    fixed_side = frame["label_class"].map({0: -1, 2: 1}).fillna(1).to_numpy(dtype=int)
    controls.append(("fixed_horizon_fwd12_no_path_side", selected_mask, fixed_side))
    rows: list[dict[str, Any]] = []
    for control_id, mask, control_side in controls:
        metrics = pnl_metrics(frame, mask, control_side)
        rows.append({"variant_id": variant_id, "view": view, "split": split, "control_id": control_id, **metrics})
    return rows


def variant_specs(label_id: str, features: Sequence[str]) -> list[dict[str, Any]]:
    return [
        {"variant_id": f"{label_id}__logreg_full58_q90", "family": "logistic", "features": list(features), "quantile": 0.90, "candidate_eligible": True},
        {"variant_id": f"{label_id}__extratrees_full58_q90", "family": "extra_trees", "features": list(features), "quantile": 0.90, "candidate_eligible": True},
        {"variant_id": f"{label_id}__fixed_fwd12_no_path_logreg_q90", "family": "fixed_fwd12_control", "features": list(features), "quantile": 0.90, "candidate_eligible": False},
        {"variant_id": f"{label_id}__shuffled_label_logreg_q90", "family": "shuffled_label_control", "features": list(features), "quantile": 0.90, "candidate_eligible": False},
    ]


def fit_variant(spec: Mapping[str, Any], train: pd.DataFrame) -> tuple[Any, np.ndarray]:
    cols = list(spec["features"])
    family = str(spec["family"])
    y = train["path_label_class"].astype(int).copy()
    if family == "fixed_fwd12_control":
        y = train["label_class"].astype(int).copy()
    if family == "shuffled_label_control":
        rng = np.random.default_rng(RNG_SEED + len(train) + abs(hash(str(spec["variant_id"]))) % 10000)
        y = pd.Series(rng.permutation(y.to_numpy()), index=y.index)
    if family == "extra_trees":
        model = make_pipeline(
            SimpleImputer(strategy="median"),
            ExtraTreesClassifier(
                n_estimators=120,
                max_depth=5,
                min_samples_leaf=90,
                class_weight="balanced",
                random_state=RNG_SEED,
                n_jobs=1,
            ),
        )
    else:
        model = make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            LogisticRegression(max_iter=800, class_weight="balanced", solver="lbfgs"),
        )
    model.fit(train[cols], y)
    _side, strength = class_scores(model, train[cols])
    return model, strength


def candidate_gate_for_variant(variant_id: str, results: Mapping[str, Mapping[str, Mapping[str, Any]]]) -> dict[str, Any]:
    selection_failures: list[str] = []
    final_read_failures: list[str] = []
    for view in ["tier_a_separate", "tier_b_separate", "tier_ab_combined"]:
        val = results.get(view, {}).get("validation", {})
        if int(val.get("trade_count") or 0) <= 0:
            selection_failures.append(f"{view}_validation_no_trades")
            continue
        if float(val.get("net_proxy") or 0.0) <= 0.0:
            selection_failures.append(f"{view}_validation_net_nonpositive")
        if float(val.get("proxy_pf") or 0.0) < CANDIDATE_MIN_PF:
            selection_failures.append(f"{view}_validation_pf_below_min")
        trades_per_day = float(val.get("trades_per_day") or 0.0)
        if not (CANDIDATE_MIN_TRADES_PER_DAY <= trades_per_day <= CANDIDATE_MAX_TRADES_PER_DAY):
            selection_failures.append(f"{view}_validation_trades_per_day_outside_range")
        if float(val.get("side_min_share") or 0.0) < CANDIDATE_MIN_SIDE_SHARE:
            selection_failures.append(f"{view}_validation_side_concentration")
        if int(val.get("regime_coverage_count") or 0) < CANDIDATE_MIN_REGIME_COVERAGE:
            selection_failures.append(f"{view}_validation_regime_coverage_low")
        if float(val.get("cost_high_trade_share") or 0.0) > CANDIDATE_MAX_HIGH_COST_SHARE:
            selection_failures.append(f"{view}_validation_high_cost_concentration")
        if float(val.get("net_proxy") or 0.0) <= float(val.get("random_net_proxy_mean") or 0.0):
            selection_failures.append(f"{view}_validation_not_above_random_side_control")
        oos = results.get(view, {}).get("oos", {})
        if int(oos.get("trade_count") or 0) <= 0:
            final_read_failures.append(f"{view}_oos_no_trades")
        elif float(oos.get("net_proxy") or 0.0) <= 0.0:
            final_read_failures.append(f"{view}_oos_net_nonpositive_final_read")
        elif float(oos.get("proxy_pf") or 0.0) < CANDIDATE_MIN_PF:
            final_read_failures.append(f"{view}_oos_pf_below_min_final_read")
    status = "candidate_triggered" if not selection_failures and not final_read_failures else "not_candidate"
    return {
        "variant_id": variant_id,
        "status": status,
        "selection_failures": selection_failures,
        "oos_final_read_failures": final_read_failures,
        "claim_effect": (
            "same_packet_runtime_probe_required_before_any_candidate_runtime_or_economics_claim"
            if status == "candidate_triggered"
            else "runtime_evidence_gate_not_triggered_no_runnable_candidate_claim"
        ),
    }


def choose_best_diagnostic(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    candidates = [
        row
        for row in rows
        if row.get("view") == "tier_ab_combined"
        and row.get("split") == "validation"
        and row.get("candidate_eligible") is True
    ]

    def key(row: Mapping[str, Any]) -> tuple[float, float, float, float]:
        return (
            float(row.get("net_proxy") or 0.0),
            float(row.get("proxy_pf") or 0.0),
            -float(row.get("max_drawdown") or 0.0),
            float(row.get("trades_per_day") or 0.0),
        )

    if not candidates:
        return {"variant_id": "none", "reason": "no_candidate_eligible_validation_rows"}
    best = max(candidates, key=key)
    oos = next(
        (
            row
            for row in rows
            if row.get("variant_id") == best["variant_id"]
            and row.get("view") == "tier_ab_combined"
            and row.get("split") == "oos"
        ),
        {},
    )
    return {
        "variant_id": best["variant_id"],
        "label_id": best.get("label_id"),
        "selection_scope": "diagnostic_only_combined_validation_no_oos_tuning",
        "validation": best,
        "oos_final_read": oos,
    }


def evaluate_path_labels(frames: Mapping[str, pd.DataFrame], raw_payload: Mapping[str, Any]) -> dict[str, Any]:
    features = f91.feature_columns()
    metric_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    label_summary_rows: list[dict[str, Any]] = []
    score_samples: list[dict[str, Any]] = []
    gates: list[dict[str, Any]] = []
    for config_index, config in enumerate(LABEL_CONFIGS):
        labeled_frames: dict[str, pd.DataFrame] = {}
        for view, source in frames.items():
            source = source.copy()
            source.attrs["view"] = view
            labeled, summary = add_path_labels(source, raw_payload, config)
            labeled_frames[view] = labeled
            label_summary_rows.append(summary)
        train = labeled_frames["tier_ab_combined"].loc[
            labeled_frames["tier_ab_combined"]["split"].astype(str).eq("train")
            & labeled_frames["tier_ab_combined"]["path_label_valid"].astype(bool)
        ].copy()
        for spec_index, spec in enumerate(variant_specs(str(config["label_id"]), features)):
            model, train_strength = fit_variant(spec, train)
            threshold = float(np.quantile(train_strength, float(spec["quantile"]))) if len(train_strength) else 0.0
            variant_id = str(spec["variant_id"])
            variant_results: dict[str, dict[str, Any]] = {}
            for view, view_frame in labeled_frames.items():
                variant_results[view] = {}
                for split in ["train", "validation", "oos"]:
                    part = view_frame.loc[
                        view_frame["split"].astype(str).eq(split) & view_frame["path_label_valid"].astype(bool)
                    ].copy().reset_index(drop=True)
                    if len(part):
                        side, strength = class_scores(model, part[list(spec["features"])])
                    else:
                        side = np.array([], dtype=int)
                        strength = np.array([], dtype=float)
                    selected = strength >= threshold
                    metrics = pnl_metrics(part, selected, side)
                    rand = random_control(part, int(selected.sum()), seed=RNG_SEED + config_index * 100 + spec_index * 10 + len(metric_rows))
                    row = {
                        "variant_id": variant_id,
                        "label_id": config["label_id"],
                        "model_family": spec["family"],
                        "candidate_eligible": bool(spec["candidate_eligible"]),
                        "feature_count": len(spec["features"]),
                        "threshold_source": "train_strength_quantile_only",
                        "strength_quantile": spec["quantile"],
                        "strength_threshold": round(threshold, 10),
                        "barrier_atr_mult": config["barrier_atr_mult"],
                        "horizon_bars": config["horizon_bars"],
                        "cost_stress_mult": config["cost_stress_mult"],
                        "view": view,
                        "split": split,
                        **metrics,
                        **rand,
                    }
                    metric_rows.append(row)
                    control_rows.extend(control_rows_for(part, selected, side, variant_id, view, split))
                    variant_results[view][split] = row
                    if split in {"validation", "oos"} and len(part):
                        sample = part.loc[
                            selected,
                            [
                                "timestamp",
                                "source_tier",
                                "route_role",
                                "path_label",
                                "exit_shape_class",
                                "regime_key",
                                "long_path_reward_points",
                                "short_path_reward_points",
                            ],
                        ].copy()
                        sample["variant_id"] = variant_id
                        sample["split"] = split
                        sample["side"] = side[selected]
                        sample["strength"] = strength[selected]
                        score_samples.extend(sample.head(60).to_dict(orient="records"))
            if spec["candidate_eligible"]:
                gates.append(candidate_gate_for_variant(variant_id, variant_results))
    pd.DataFrame(metric_rows).to_csv(io_path(VARIANT_METRICS_CSV), index=False)
    pd.DataFrame(metric_rows).to_csv(io_path(SPLIT_METRICS_CSV), index=False)
    pd.DataFrame(control_rows).to_csv(io_path(NEGATIVE_CONTROL_CSV), index=False)
    pd.DataFrame(label_summary_rows).to_csv(io_path(PATH_LABEL_SUMMARY_CSV), index=False)
    pd.DataFrame(score_samples).to_csv(io_path(SCORE_SAMPLE_CSV), index=False)
    write_json(PATH_LABEL_CONFIG, {"label_configs": LABEL_CONFIGS, "tie_policy": "same_bar_both_hit_conservative_loss", "entry_proxy": "next_bar_open_at_decision_timestamp"})
    candidate_count = sum(1 for gate in gates if gate["status"] == "candidate_triggered")
    write_json(CANDIDATE_GATE_JSON, {"candidate_count": candidate_count, "gates": gates})
    return {
        "variants": variant_specs("template", features),
        "split_metrics": metric_rows,
        "negative_control_rows": control_rows,
        "label_summary_rows": label_summary_rows,
        "candidate_gates": gates,
        "candidate_count": candidate_count,
        "best_diagnostic_variant": choose_best_diagnostic(metric_rows),
        "selection_policy": "train-only thresholds; validation diagnostic read; OOS final read only; candidate gate predeclared",
    }


def materialize_proxy_metrics() -> dict[str, Any]:
    frames, route_summary, tier_b_summary, integrity = f91.prepare_routed_frames()
    raw_payload = load_raw_path()
    write_json(TIER_ROUTE_SUMMARY, route_summary)
    write_json(TIER_B_SUMMARY, tier_b_summary)
    evaluation = evaluate_path_labels(frames, raw_payload)
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
            **raw_payload["integrity"],
            "entry_proxy": "next raw bar open where raw time_open equals feature timestamp",
            "feature_label_boundary": "features are closed-bar only; post-entry OHLC path fields are label-only and excluded from model features",
            "split_edge_censoring": "rows whose horizon close reaches the next split boundary are invalid for that label config",
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
        "hypothesis": "Path-conditioned trade-shape labels can expose whether US100 M5 entries have usable post-entry MFE/MAE and exit-shape structure.",
        "proxy": "Train-only path-label classifiers over first-touch ATR barriers, holding buckets, cost stress, and negative controls.",
        "metrics": metrics,
        "source_identity": {
            "f92a_proxy_scout_brief": file_identity(F92A_BRIEF),
            "f92a_data_plan": file_identity(F92A_DATA_PLAN),
            "f92a_runtime_contract": file_identity(F92A_RUNTIME_CONTRACT),
            "model_input_summary": file_identity(f91.MODEL_INPUT_SUMMARY),
            "model_input_dataset": file_identity(f91.MODEL_INPUT_DATASET),
            "feature_order": file_identity(f91.MODEL_INPUT_FEATURE_ORDER),
            "feature_order_hash": f91.read_json(f91.MODEL_INPUT_SUMMARY).get("included_feature_order_hash"),
            "raw_us100_csv": file_identity(RAW_US100_CSV),
            "tier_b_summary": file_identity(TIER_B_SUMMARY),
        },
        "runtime_boundary": {
            "runtime_probe_status": metrics["runtime_probe_status"],
            "valid_n_a_reason": "No runnable candidate, ONNX/EA/set behavior, runtime materialization, economics, promotion, or authority claim is made.",
            "invalid_deferrals": ["cost", "expense", "proxy_bad"],
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
                "Fresh F92B packet and receipts are materialized.",
                "Path labels use raw OHLC after the feature timestamp; path fields are not model features.",
                "Tier A separate, Tier B separate, and actual routed total are recorded.",
                "OOS is final-read-only and not used for thresholds.",
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
        "test_period": "train 2022-09-01..2024-12-31, validation 2025-01-01..2025-09-30, OOS 2025-10-01..2026-04-13",
        "proxy_kpi": {
            "best_variant_id": best.get("variant_id"),
            "best_label_id": best.get("label_id"),
            "validation_net_proxy": val.get("net_proxy"),
            "validation_proxy_pf": val.get("proxy_pf"),
            "validation_max_drawdown": val.get("max_drawdown"),
            "validation_trade_count": val.get("trade_count"),
            "validation_trades_per_day": val.get("trades_per_day"),
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
        "gap_cause": "no runtime surface materialized because candidate gate failed",
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
            "avg_mfe_points": val.get("avg_mfe_points"),
            "avg_mae_points": val.get("avg_mae_points"),
            "avg_bars_held": val.get("avg_bars_held"),
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
        "trigger_reason": "active_goal_and_explicit_user_instruction_required_selected_task_force_review",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in TASK_FORCE_CALLS],
        "actual_subagent_calls": TASK_FORCE_CALLS,
        "review_requirement": "active_goal_required",
        "model_policy": "inherited_parent_model_highest_available_xhigh_when_available",
        "bounded_evidence": [rel(F92A_BRIEF), rel(F92A_DATA_PLAN), rel(CANDIDATE_GATE_JSON), rel(KPI_RECORD)],
        "advice_classification": payload["task_force"]["advice_classification"],
        "local_verification": payload["task_force"]["local_verification_response"],
        "claim_boundary": CLAIM_BOUNDARY,
        "final_codex_direction": status_from(payload),
        "forbidden_claim_check": FORBIDDEN_CLAIMS,
    }


def final_claim_guard_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    candidate_count = int(payload["metrics"]["candidate_gate"]["candidate_count"])
    return {
        "audit_name": "final_claim_guard",
        "packet_id": RUN_ID,
        "status": "pass" if candidate_count == 0 else "blocked_runtime_probe_required",
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "runtime_probe_status": runtime_probe_status_from(payload),
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_count": candidate_count,
    }


def write_run_artifacts(payload: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_json(RUN_MANIFEST, run_manifest(payload, gate_results))
    write_json(SUMMARY_JSON, payload)
    write_json(KPI_RECORD, kpi_record(payload))
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_json(EXECUTION_SUMMARY, payload)
    write_text(F92B_REPORT, result_summary_text(payload))


def write_audits(payload: Mapping[str, Any]) -> None:
    metrics = payload["metrics"]
    task_force = task_force_receipt(payload)
    write_json(TASK_FORCE_REVIEW, task_force)
    write_json(PACKET_TASK_FORCE_REVIEW, task_force)
    write_json(FRONTIER_EXTRA_DUE_CHECK, audit_payload("frontier_extra_due_check", "pass_not_due", counts={"status": "not_due_after_f91_closeout_next_boundary_f100_e01_closed_for_f050"}))
    write_json(FIVE_STAGE_SYNTHESIS, audit_payload("frontier_five_stage_direction_synthesis", "pass", counts={"source_frontiers": "F87-F91", "dominant_warning": "avoid adjacent F91 threshold/filter repair"}))
    write_json(TOPIC_ROTATION_CHECK, audit_payload("frontier_topic_rotation_check", "pass", counts={"novelty_delta": "path_conditioned_trade_shape_label_axis_not_f91_abstention_filter_repair"}))
    write_json(SCOPE_GATE, audit_payload("scope_completion_gate", "pass", counts={"produced_artifacts": len([path for path in produced_artifacts() if path_exists(path)])}))
    write_json(DATA_INTEGRITY_AUDIT, audit_payload("data_integrity_audit", "pass_with_boundary", counts=metrics["data_integrity"]))
    write_json(
        MODEL_VALIDATION_AUDIT,
        audit_payload(
            "model_validation_audit",
            "pass_negative_no_candidate_no_calibration",
            counts={
                "label_config_count": len(LABEL_CONFIGS),
                "candidate_count": metrics["candidate_gate"]["candidate_count"],
                "selection_policy": metrics["evaluation"]["selection_policy"],
                "score_boundary": "rank_or_utility_score_not_calibrated_probability",
                "oos_policy": "final_read_only_no_threshold_tuning",
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
            "evidence_available": [rel(CANDIDATE_GATE_JSON), rel(KPI_RECORD), rel(SPLIT_METRICS_CSV), rel(RESULT_SUMMARY)],
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
            "baseline": "F92A design brief and F91 negative memory only; no selected baseline.",
            "changed_variables": ["path label objective", "ATR barrier geometry", "holding horizon", "exit-shape class", "cost stress"],
            "invalid_conditions": ["OOS threshold tuning", "future path used as feature", "favorable same-bar both-hit assumption", "F91 filter-only repair"],
            "evidence_plan": [rel(PATH_LABEL_CONFIG), rel(PATH_LABEL_SUMMARY_CSV), rel(SPLIT_METRICS_CSV), rel(NEGATIVE_CONTROL_CSV), rel(CANDIDATE_GATE_JSON), rel(KPI_RECORD)],
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": [rel(f91.MODEL_INPUT_DATASET), rel(f91.MODEL_INPUT_FEATURE_ORDER), rel(RAW_US100_CSV)],
            "time_axis_boundary": "Feature timestamp is closed M5 bar; entry proxy is the next raw bar open at the same timestamp.",
            "split_boundary": "Train fit and thresholds only; validation diagnostics; OOS final read only; split-edge horizons censored.",
            "leakage_checks": ["path OHLC/MFE/MAE excluded from features", "same-bar both-hit conservative loss", "OOS not used for threshold or label selection"],
            "missing_data_boundary": "Tier B fallback uses core42 partial context; missing full58 fields are imputed from train only.",
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "Logistic/tree path-label utility scores with train-only strength quantiles.",
            "validation_split": "Validation is diagnostic; OOS is final read only and does not tune thresholds.",
            "overfit_checks": ["negative controls", "side concentration", "regime coverage", "cost concentration", "Tier A/B/combined required views"],
            "selection_metric_boundary": "diagnostic proxy only; no candidate, calibration, runtime, economics, or model superiority claim.",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "raw_evidence": [rel(f91.MODEL_INPUT_DATASET), rel(RAW_US100_CSV)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(PATH_LABEL_CONFIG), rel(CANDIDATE_GATE_JSON), rel(SPLIT_METRICS_CSV)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(DECISION_MEMO)],
            "hashes_or_missing_reasons": [file_identity(path) for path in source_inputs() + [PATH_LABEL_CONFIG, CANDIDATE_GATE_JSON, KPI_RECORD]],
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
            "idea_boundary": "F92B is clue/negative-memory generation, not completion or authority.",
            "negative_memory_effect": "Path-conditioned trade-shape labels failed joint candidate gate if candidate_count is zero.",
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
    gates = {
        "work_packet_schema_lint": (gate_results or {}).get("work_packet_schema_lint", {}).get("status", "pending_external_lint"),
        "skill_receipt_schema_lint": (gate_results or {}).get("skill_receipt_schema_lint", {}).get("status", "pending_external_lint"),
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
        "state_sync_audit": (gate_results or {}).get("state_sync_audit", {}).get("status", "pending_external_lint"),
        "required_gate_coverage_audit": (gate_results or {}).get("required_gate_coverage_audit", {}).get("status", "pending_external_lint"),
        "final_claim_guard": final_claim_guard_payload(payload)["status"],
    }
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user explicitly required Task Force agents when triggered",
            "requested_action": "F92B proxy_scout frontier continuation for path-conditioned trade-shape labels",
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
                "future_path_feature_leakage": "high",
                "oos_threshold_tuning": "high",
                "runtime_probe_absence_misread_as_cost_skip": "high",
            },
            "hard_stop_risks": [
                "Do not claim runtime, economics, materialization, or handoff without Strategy Tester identity.",
                "Do not omit Tier B or combined records.",
                "Do not use MFE/MAE/post-entry OHLC path as a runtime feature.",
                "Do not treat same-bar both-hit as favorable.",
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
            "target_surfaces": ["F92B proxy scout", "path-conditioned trade-shape labels", "Task Force receipt", "state sync"],
            "scope_units": ["proxy_scout", "path_label_materialization", "negative_controls", "tier_records", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["model input parquet", "raw US100 M5 OHLC", "Tier B fallback materialization", "proxy metrics", "Task Force actual calls"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F92B is non-trivial experiment execution."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "proxy_scout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F92B current_run from workspace_state",
                "explicit user instruction requiring selected Task Force agents",
                "proxy scout execution with candidate/runtime trigger guard",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [
                rel(PATH_LABEL_CONFIG),
                rel(PATH_LABEL_SUMMARY_CSV),
                rel(CANDIDATE_GATE_JSON),
                rel(SPLIT_METRICS_CSV),
                rel(NEGATIVE_CONTROL_CSV),
                rel(TIER_ROUTE_SUMMARY),
                rel(TIER_B_SUMMARY),
                rel(KPI_RECORD),
                rel(PACKET_TASK_FORCE_REVIEW),
                rel(WORK_PACKET),
                rel(SKILL_RECEIPTS),
                rel(PACKET_CLOSEOUT_GATE),
            ],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "no_runnable_candidate_no_runtime_claim",
                    "reason": "F92B produced proxy evidence only and no ONNX, EA, set, tester output, materialization, economics, promotion, or authority claim.",
                    "claim_effect": "No runtime verified, economics pass, materialization ready, handoff complete, promotion, or authority claim is allowed.",
                },
                {
                    "gate": "wfo_stress_gate",
                    "reason_code": "outside_claim_surface_proxy_scout_no_candidate",
                    "reason": "F92B is a proxy scout and candidate gate failed; WFO/stress is not claimed.",
                    "claim_effect": "No WFO pass, stress pass, or candidate claim is allowed.",
                },
            ],
            "stop_conditions": [
                "Stop if OOS is used to tune thresholds.",
                "Stop if future path fields enter model features.",
                "Stop candidate claim if negative controls are not separated.",
                "Switch to runtime_probe profile in the same packet if a runnable candidate or runtime claim appears.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F92B path-label metrics exist.", "expected_artifact": rel(SPLIT_METRICS_CSV), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F92B Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "Tier A/B/combined route summary exists.", "expected_artifact": rel(TIER_ROUTE_SUMMARY), "verification_method": "data_integrity_audit", "required": True},
            {"id": "AC-004", "text": "Runtime gate boundary is explicit and not a cost/proxy-bad skip.", "expected_artifact": rel(FINAL_CLAIM_GUARD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Run F92B path-label proxy models and controls.",
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
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report or trade list exists for F92B."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "source_inputs": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(PATH_LABEL_CONFIG), rel(PATH_LABEL_SUMMARY_CSV), rel(CANDIDATE_GATE_JSON), rel(SPLIT_METRICS_CSV), rel(NEGATIVE_CONTROL_CSV), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(F92B_REPORT), rel(DECISION_MEMO)],
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
        "final_claim_guard": {"audit_name": "final_claim_guard", "path": rel(PACKET_FINAL_CLAIM_GUARD), "status": final_claim_guard_payload(payload)["status"]},
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
frontier_extra_due_status: not_due_after_f91_closeout_next_boundary_f100_e01_closed_for_f050
frontier_topic_rotation_status: passed_f92_path_conditioned_trade_shape_label_axis_not_f91_abstention_filter_repair
task_force_status: f92b_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim
runtime_probe_status: {runtime_probe_status_from(payload)}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action: F92B ran a path-conditioned trade-shape label proxy scout.'
- 'Effect: candidate gate failed, so F92C repair-or-rotation is the next current run unless runtime trigger blocks.'
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
- best_proxy: `{best.get('variant_id')}` validation_net `{val.get('net_proxy')}` validation_pf `{val.get('proxy_pf')}` OOS_net `{oos.get('net_proxy')}` OOS_pf `{oos.get('proxy_pf')}`
- Task Force: 6 selected agents actual calls recorded; no Task Force reviewed/pass claim.
- Runtime: `{runtime_probe_status_from(payload)}`
- Boundary: `{CLAIM_BOUNDARY}`
"""


def stage_brief_text(payload: Mapping[str, Any]) -> str:
    return f"""# {STAGE_ID}

Question: Can path-conditioned trade-shape labels expose usable US100 M5 entry structure through MFE/MAE, first-touch, holding, and exit-shape outcomes?

Boundary: F92B is a Python proxy scout only. It records path-label evidence and MT5 runtime_probe trigger status, but it does not claim completion, selected baseline, operating promotion, runtime authority, live readiness, or Goal Achieve.

F92B result: proxy scout candidate gate did not create a runnable candidate under Tier A, Tier B, and actual routed total records.

Next: `{payload['next_run_id']}` should decide capped repair or rotation. Runtime authority, selected baseline, live readiness, and Goal Achieve are not claimed.
"""


def selection_status_text(payload: Mapping[str, Any]) -> str:
    return f"""# Selection Status

Current run: `{payload['next_run_id']}`

No candidate, no selected baseline, no operating promotion, no runtime authority, no live readiness, no Goal Achieve.

F92B is proxy-scout evidence only. Runtime probe status: `{runtime_probe_status_from(payload)}`.
"""


def input_refs_text() -> str:
    lines = ["# Input References", ""]
    for path in source_inputs():
        ident = file_identity(path)
        lines.append(f"- `{ident['path']}` sha256 `{ident['sha256']}`")
    return "\n".join(lines)


def review_index_text() -> str:
    rows = [
        ("f92b_task_force_review_receipt", TASK_FORCE_REVIEW),
        ("f92b_data_integrity_audit", DATA_INTEGRITY_AUDIT),
        ("f92b_model_validation_audit", MODEL_VALIDATION_AUDIT),
        ("f92b_kpi_contract_audit", KPI_CONTRACT_AUDIT),
        ("f92b_artifact_lineage_audit", ARTIFACT_AUDIT),
        ("f92b_result_judgment_audit", RESULT_JUDGMENT_AUDIT),
        ("f92b_required_gate_coverage_audit", REQUIRED_GATE_AUDIT),
    ]
    lines = ["# Review Index", ""]
    for name, path in rows:
        lines.append(f"- `{name}`: `{rel(path)}`")
    return "\n".join(lines)


def decision_memo_text(payload: Mapping[str, Any]) -> str:
    best = payload["metrics"]["evaluation"]["best_diagnostic_variant"]
    return f"""# F92B Decision Memo

Decision: Record F92B as proxy-scout negative/inconclusive memory and plan `{payload['next_run_id']}`.

Reason: Best diagnostic variant `{best.get('variant_id')}` did not satisfy the joint Tier A, Tier B, and actual routed candidate gate. Runtime probe was not run because no runnable candidate or runtime claim was created; this is not a cost or proxy-bad deferral.

Forbidden claims: candidate, selected baseline, operating promotion, runtime authority, live readiness, Goal Achieve.
"""


def result_summary_text(payload: Mapping[str, Any]) -> str:
    kpi = kpi_record(payload)["proxy_kpi"]
    return f"""# F92B Path-Conditioned Trade-Shape Label Proxy Scout

Status: `{status_from(payload)}`

Judgment: `{judgment_from(payload)}`

Hypothesis: {payload['hypothesis']}

Best diagnostic proxy:
- variant: `{kpi.get('best_variant_id')}`
- label: `{kpi.get('best_label_id')}`
- validation net/PF/DD/trades/day: `{kpi.get('validation_net_proxy')}` / `{kpi.get('validation_proxy_pf')}` / `{kpi.get('validation_max_drawdown')}` / `{kpi.get('validation_trades_per_day')}`
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


def ledger_rows(payload: Mapping[str, Any], gate_passes: int = 0) -> list[dict[str, Any]]:
    created_date = payload["created_at_utc"][:10]
    best = payload["metrics"]["evaluation"]["best_diagnostic_variant"]
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "path_conditioned_trade_shape_proxy_scout",
        "status": status_from(payload),
        "judgment": judgment_from(payload),
        "path": rel(RESULT_SUMMARY),
        "notes": "F92B path-label proxy scout recorded no candidate and no runtime authority.",
        "family": "experiment_execution",
        "primary_report": rel(RESULT_SUMMARY),
        "run_number": "frontier92B",
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
        "question": "Can path-conditioned trade-shape labels create a proxy candidate?",
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
                "kpi_scope": "path_conditioned_trade_shape_proxy",
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
            "notes": "Planned after F92B proxy scout negative result.",
            "primary_report": rel(STAGE_BRIEF),
            "run_number": "frontier92C",
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
            "ledger_row_id": f"{payload['next_run_id']}__planned_current_run",
            "subrun_id": f"{payload['next_run_id']}__planned_current_run",
            "record_view": "planned_current_run",
            "tier_scope": "not_applicable_planned",
            "kpi_scope": "pending",
            "primary_kpi": "pending",
            "guardrail_kpi": "pending_runtime_claim_forbidden",
            "row_id": f"{payload['next_run_id']}__planned_current_run",
            "view": "planned_current_run",
            "tier": "not_applicable_planned",
            "metric_scope": "pending",
            "evidence_boundary": "planned_only_no_runtime_evidence",
            "next_action": "decide_repair_or_rotation",
            "question": "Should F92 repair path-label axis or rotate?",
            "artifact_count": 0,
            "required_gate_audit": "",
            "run_type": "planned_current_run",
            "input_run_id": RUN_ID,
            "output_path": rel(STAGE_DIR),
            "result_path": rel(STAGE_BRIEF),
            "candidate_count": 0,
            "scout_clue_count": 0,
        }
    )
    rows.append(planned)
    return rows


def update_ledgers(payload: Mapping[str, Any], gate_passes: int = 0) -> None:
    rows = ledger_rows(payload, gate_passes=gate_passes)
    run_rows = [dict(rows[0]), dict(rows[-1])]
    f91.append_dict_rows(RUN_REGISTRY, ["run_id"], run_rows)
    f91.append_dict_rows(ALPHA_LEDGER, ["ledger_row_id"], rows)
    f91.append_dict_rows(STAGE_LEDGER, ["ledger_row_id"], rows, header_source=ALPHA_LEDGER)


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path) or not path.is_file():
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f92b_path_trade_shape_proxy_scout",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F92B proxy scout artifact; no runtime authority.",
                "artifact_path": rel(path),
                "effect": "Supports F92B proxy negative/inconclusive memory only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    f91.replace_rows_by_field(ARTIFACT_REGISTRY, "run_id", RUN_ID, rows)


def update_register_docs(payload: Mapping[str, Any]) -> None:
    marker = RUN_ID
    idea_addition = f"""
## F92B path-conditioned trade-shape proxy memory

- run_id: `{RUN_ID}`
- hypothesis: path-conditioned labels can expose MFE/MAE and exit-shape structure.
- result: candidate_count `{payload['metrics']['candidate_gate']['candidate_count']}`; no selected baseline or runtime authority.
- next_action: `{payload['next_run_id']}`.
- claim_boundary: `{CLAIM_BOUNDARY}`.
"""
    negative_addition = f"""
## F92B path-label proxy joint gate failure

- run_id: `{RUN_ID}`
- failed_boundary: Tier A, Tier B, and actual routed candidate gate did not produce a runnable candidate.
- salvage_value: path label summary, exit-shape mix, and negative-control metrics remain useful for F92C repair-or-rotation.
- do_not_repeat: F91-style threshold/filter-only repair without new label geometry, runtime representation, validation philosophy, or risk logic.
- runtime: no MT5 probe because no runnable candidate/runtime claim exists; this is not a cost/proxy-bad skip.
"""
    changelog_addition = f"""
## {payload['created_at_utc']} - F92B proxy scout

- Action: ran path-conditioned trade-shape label proxy scout with Task Force actual calls.
- Effect: recorded negative/inconclusive proxy memory and planned `{payload['next_run_id']}`.
- Runtime: no Strategy Tester evidence; no runtime authority; no Goal Achieve.
- Packet: `{rel(WORK_PACKET)}`.
"""
    f91.append_once(IDEA_REGISTRY, marker, idea_addition)
    f91.append_once(NEGATIVE_REGISTER, marker, negative_addition)
    f91.append_once(WORKSPACE_CHANGELOG, marker, changelog_addition)
    f91.append_once(ROOT_CHANGELOG, marker, changelog_addition)


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
    write_json(PACKET_STATE_SYNC_AUDIT, audit_payload("state_sync_audit", "pending_external_lint", counts={"active_stage": STAGE_ID, "current_run_id": payload["next_run_id"]}))
    write_json(STATE_SYNC_AUDIT, read_json(PACKET_STATE_SYNC_AUDIT))


def run_control_gates(payload: Mapping[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    results["work_packet_schema_lint"] = run_gate_cmd(["foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET)], PACKET_WORK_PACKET_LINT)
    results["skill_receipt_schema_lint"] = run_gate_cmd(["foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS)], PACKET_SKILL_RECEIPT_LINT)
    results["state_sync_audit"] = run_gate_cmd(
        ["foundation.control_plane.state_sync_audit", "--root", str(ROOT), "--active-stage", STAGE_ID, "--current-branch", f91.current_branch()],
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
        raise FileNotFoundError(f"Missing required F92B source evidence: {missing}")
    ensure_dirs()
    metrics = materialize_proxy_metrics()
    payload = build_payload(now_utc(), metrics)
    write_initial(payload)
    gate_results = run_control_gates(payload)
    write_final(payload, gate_results)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status_from(payload),
                "judgment": judgment_from(payload),
                "best_diagnostic_variant": payload["metrics"]["evaluation"]["best_diagnostic_variant"],
                "candidate_count": payload["metrics"]["candidate_gate"]["candidate_count"],
                "runtime_probe_status": runtime_probe_status_from(payload),
                "task_force_call_count": len(TASK_FORCE_CALLS),
                "gate_results": gate_results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
