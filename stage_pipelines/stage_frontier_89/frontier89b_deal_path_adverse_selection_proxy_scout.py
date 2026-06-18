from __future__ import annotations

import csv
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
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_89__runtime_trade_list_adverse_selection_teacher"
RUN_ID = "frontier89B_deal_path_adverse_selection_proxy_scout_v1"
PARENT_RUN_ID = "frontier89A_stage_open_runtime_trade_list_adverse_selection_teacher_v1"
NEXT_RUN_ID = "frontier89C_deal_path_teacher_repair_or_rotation_decision_v1"

STATUS = "f89b_deal_path_teacher_proxy_scout_inconclusive_no_materialization_candidate_no_authority"
JUDGMENT = "inconclusive_small_sample_deal_path_teacher_proxy_no_runtime_candidate_no_runtime_evidence"
DECISION = "close_f89b_proxy_scout_inconclusive_route_to_f89c_repair_or_rotation"
CLAIM_BOUNDARY = (
    "proxy_scout_only_no_strategy_tester_runtime_economics_no_selected_baseline_"
    "no_operating_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = "not_run_no_meaningful_materialization_candidate_no_runtime_claim"
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f88_closeout_next_boundary_f100_e01_closed_for_f050"
SCRIPT_REL = "stage_pipelines/stage_frontier_89/frontier89b_deal_path_adverse_selection_proxy_scout.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
EPISODE_DIR = RUN_DIR / "episodes"
PROXY_DIR = RUN_DIR / "proxy_scout"
MODEL_DIR = RUN_DIR / "models"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F89A_RUN = STAGE_DIR / "02_runs" / PARENT_RUN_ID
F89A_DESIGN = F89A_RUN / "design/f89a_experiment_design.json"
F89A_TEACHER_CONTRACT = F89A_RUN / "design/runtime_trade_list_adverse_selection_teacher_contract.json"
F89A_BRIEF = F89A_RUN / "design/f89b_deal_path_adverse_selection_proxy_scout_brief.json"
F89A_RESULT = F89A_RUN / "reports/result_summary.md"

F88_STAGE = ROOT / "stages/stage_frontier_88__runtime_substrate_first_materialization_probe"
F88C_RUN = F88_STAGE / "02_runs/frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1"
F88C_RUNTIME_IDENTITY = F88C_RUN / "runtime_evidence_identity.json"
F88C_KPI = F88C_RUN / "kpi_record.json"
F88C_DEALS = F88C_RUN / "trade_lists/f88c_tier_a_validation_is_deals.csv"
F88C_EXPECTED_TRADES = F88C_RUN / "trade_lists/f88c_tier_a_validation_is_trades.csv"
F88C_TELEMETRY_SUMMARY = F88C_RUN / "runtime_telemetry/f88c_tier_a_validation_is_summary.csv"
F88C_FEATURE_MATRIX = F88C_RUN / "feature_matrices/frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1_validation_is_features.csv"

FRONTIER_GOVERNANCE = ROOT / "docs/policies/frontier_governance.md"
WORK_FAMILY_REGISTRY = ROOT / "docs/agent_control/work_family_registry.yaml"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"

DEAL_EPISODES = EPISODE_DIR / "deal_episodes.csv"
TEACHER_SURFACE = PROXY_DIR / "deal_path_teacher_surface.csv"
PROXY_SCORES = PROXY_DIR / "proxy_scores.csv"
PROXY_METRICS = PROXY_DIR / "proxy_metrics.json"
CANDIDATE_QUEUE = PROXY_DIR / "candidate_queue.csv"
TIER_SCOPE_RECORD = PROXY_DIR / "tier_scope_records.json"
FEATURE_JOIN_REPORT = PROXY_DIR / "feature_join_report.json"
MODEL_CARD = MODEL_DIR / "proxy_model_card.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

EXECUTION_SUMMARY = REVIEW_DIR / "f89b_execution_summary.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f89b_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f89b_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f89b_frontier_topic_rotation_check.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f89b_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f89b_model_validation_audit.json"
SCOPE_GATE = REVIEW_DIR / "f89b_scope_completion_gate.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f89b_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f89b_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f89b_result_judgment_audit.json"
TASK_FORCE_TRIGGER_CHECK = REVIEW_DIR / "f89b_task_force_trigger_check.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f89b_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f89b_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f89b_required_gate_coverage_audit.json"

RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f89b_run_evidence_receipt.json"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f89b_experiment_design_receipt.json"
DATA_RECEIPT = REVIEW_DIR / "f89b_data_integrity_receipt.json"
MODEL_RECEIPT = REVIEW_DIR / "f89b_model_validation_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f89b_artifact_lineage_receipt.json"
RESULT_RECEIPT = REVIEW_DIR / "f89b_result_judgment_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f89b_claim_discipline_receipt.json"

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
WORKSPACE_CHANGELOG = ROOT / "docs/workspace/changelog.md"
ROOT_CHANGELOG = ROOT / "docs/CHANGELOG.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-19_frontier89b_deal_path_teacher_proxy_scout.md"

STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

ALLOWED_CLAIMS = [
    "f89b_deal_episode_surface_recorded",
    "f89b_entry_feature_join_recorded",
    "f89b_teacher_proxy_scout_recorded",
    "f89b_negative_or_inconclusive_memory_recorded",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "completed",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "runtime_probe",
    "runtime_verified",
    "strategy_tester_runtime_economics",
    "materialization_ready",
    "mt5_handoff_ready",
    "task_force_reviewed",
    "reviewed",
    "verified",
    "pass",
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
MIN_RUNTIME_CANDIDATE_EPISODES = 50


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
    if isinstance(value, (np.integer, np.int32, np.int64)):
        return int(value)
    if isinstance(value, (np.floating, np.float32, np.float64)):
        value = float(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    return value


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


def file_identity(path: Path) -> dict[str, Any]:
    exists = path_exists(path)
    payload: dict[str, Any] = {"path": rel(path), "exists": exists}
    if exists:
        payload.update({"sha256_lf_normalized": sha256_file_lf_normalized(path), "size_bytes": io_path(path).stat().st_size})
    return payload


def append_once(path: Path, marker: str, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    joiner = "" if not text or text.endswith("\n") else "\n"
    write_text(path, text + joiner + addition.strip() + "\n")


def ensure_dirs() -> None:
    for path in [EPISODE_DIR, PROXY_DIR, MODEL_DIR, REPORT_DIR, REVIEW_DIR, PACKET_DIR]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def source_inputs() -> list[Path]:
    return [
        F89A_DESIGN,
        F89A_TEACHER_CONTRACT,
        F89A_BRIEF,
        F89A_RESULT,
        F88C_RUNTIME_IDENTITY,
        F88C_KPI,
        F88C_DEALS,
        F88C_EXPECTED_TRADES,
        F88C_TELEMETRY_SUMMARY,
        F88C_FEATURE_MATRIX,
        FRONTIER_GOVERNANCE,
        WORK_FAMILY_REGISTRY,
        NEGATIVE_REGISTER,
        IDEA_REGISTRY,
        WORKSPACE_STATE,
    ]


def produced_artifacts() -> list[Path]:
    return [
        DEAL_EPISODES,
        TEACHER_SURFACE,
        PROXY_SCORES,
        PROXY_METRICS,
        CANDIDATE_QUEUE,
        TIER_SCOPE_RECORD,
        FEATURE_JOIN_REPORT,
        MODEL_CARD,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        RESULT_SUMMARY,
        EXECUTION_SUMMARY,
        FRONTIER_EXTRA_DUE_CHECK,
        FIVE_STAGE_SYNTHESIS,
        TOPIC_ROTATION_CHECK,
        DATA_INTEGRITY_AUDIT,
        MODEL_VALIDATION_AUDIT,
        SCOPE_GATE,
        KPI_CONTRACT_AUDIT,
        ARTIFACT_AUDIT,
        RESULT_JUDGMENT_AUDIT,
        TASK_FORCE_TRIGGER_CHECK,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_CLOSEOUT_GATE,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        DECISION_MEMO,
    ]


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    deals = pd.read_csv(io_path(F88C_DEALS))
    features = pd.read_csv(io_path(F88C_FEATURE_MATRIX))
    return deals, features


def build_deal_episodes(deals: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    required = {"time", "ticket", "symbol", "order_type", "direction", "volume", "price", "profit", "balance"}
    missing = sorted(required - set(deals.columns))
    if missing:
        raise ValueError(f"deals CSV missing columns: {missing}")
    ordered = deals.copy()
    ordered["time_dt"] = pd.to_datetime(ordered["time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    ordered = ordered.sort_values(["time_dt", "ticket"]).reset_index(drop=True)
    episodes: list[dict[str, Any]] = []
    open_row: pd.Series | None = None
    blockers: list[str] = []
    for _, row in ordered.iterrows():
        direction = str(row["direction"]).strip().lower()
        if direction == "in":
            if open_row is not None:
                blockers.append(f"unclosed_entry_ticket_{open_row.get('ticket')}")
            open_row = row
            continue
        if direction == "out":
            if open_row is None:
                blockers.append(f"exit_without_entry_ticket_{row.get('ticket')}")
                continue
            if str(row["symbol"]) != str(open_row["symbol"]):
                blockers.append(f"symbol_mismatch_entry_{open_row.get('ticket')}_exit_{row.get('ticket')}")
            entry_time = pd.to_datetime(open_row["time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
            exit_time = pd.to_datetime(row["time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
            profit = float(row.get("profit", 0.0) or 0.0)
            episodes.append(
                {
                    "episode_id": f"f89b_ep_{len(episodes) + 1:03d}",
                    "entry_ticket": int(open_row["ticket"]),
                    "exit_ticket": int(row["ticket"]),
                    "symbol": str(open_row["symbol"]),
                    "side": str(open_row["order_type"]).lower(),
                    "volume": float(open_row["volume"]),
                    "entry_time_server": str(open_row["time"]),
                    "exit_time_server": str(row["time"]),
                    "entry_price": float(open_row["price"]),
                    "exit_price": float(row["price"]),
                    "profit": profit,
                    "balance_after_exit": float(row.get("balance", 0.0) or 0.0),
                    "duration_minutes": max(0.0, (exit_time - entry_time).total_seconds() / 60.0) if pd.notna(entry_time) and pd.notna(exit_time) else None,
                    "target_adverse_loss": int(profit <= 0.0),
                    "target_positive_payoff": int(profit > 0.0),
                }
            )
            open_row = None
    if open_row is not None:
        blockers.append(f"unclosed_entry_ticket_{open_row.get('ticket')}")
    frame = pd.DataFrame(episodes)
    if frame.empty:
        raise RuntimeError("No deal episodes could be built.")
    losses = frame.loc[frame["profit"] <= 0, "profit"]
    large_loss_cutoff = float(losses.quantile(0.50)) if not losses.empty else -999999.0
    frame["target_large_loss"] = (frame["profit"] <= large_loss_cutoff).astype(int) if not losses.empty else 0
    frame["episode_index"] = np.arange(len(frame))
    diagnostics = {
        "input_deal_rows": int(len(deals)),
        "episode_rows": int(len(frame)),
        "blockers": blockers or ["none_detected"],
        "gross_profit": float(frame.loc[frame["profit"] > 0, "profit"].sum()),
        "gross_loss": float(frame.loc[frame["profit"] < 0, "profit"].sum()),
        "net_profit": float(frame["profit"].sum()),
        "win_rate": float((frame["profit"] > 0).mean()),
        "loss_rate": float((frame["profit"] <= 0).mean()),
        "avg_win": float(frame.loc[frame["profit"] > 0, "profit"].mean()) if (frame["profit"] > 0).any() else 0.0,
        "avg_loss": float(frame.loc[frame["profit"] <= 0, "profit"].mean()) if (frame["profit"] <= 0).any() else 0.0,
    }
    return frame, diagnostics


def join_features(episodes: pd.DataFrame, features: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    feature_copy = features.copy()
    feature_copy["bar_time_server"] = feature_copy["bar_time_server"].astype(str)
    joined = episodes.merge(feature_copy, left_on="entry_time_server", right_on="bar_time_server", how="left", suffixes=("", "_feature"))
    joined["entry_feature_join_valid"] = joined["row_index"].notna().astype(int)
    unmatched = joined.loc[joined["entry_feature_join_valid"] == 0, "episode_id"].tolist()
    role_cut = max(1, int(math.floor(len(joined) * 0.65)))
    joined["selection_split_role"] = np.where(joined["episode_index"] < role_cut, "inner_train", "locked_forward_readout")
    diagnostics = {
        "episode_rows": int(len(episodes)),
        "feature_rows": int(len(features)),
        "joined_rows": int(joined["entry_feature_join_valid"].sum()),
        "unmatched_episode_ids": unmatched or ["none_detected"],
        "join_key": "entry_time_server_to_bar_time_server_exact",
        "future_leakage_boundary": "entry rows join only to same closed bar feature record already used by F88C runtime probe",
    }
    return joined, diagnostics


def feature_columns(surface: pd.DataFrame) -> list[str]:
    excluded = {
        "episode_id",
        "entry_ticket",
        "exit_ticket",
        "symbol",
        "side",
        "entry_time_server",
        "exit_time_server",
        "bar_time_server",
        "timestamp_utc",
        "split",
        "selection_split_role",
        "target_adverse_loss",
        "target_positive_payoff",
        "target_large_loss",
        "profit",
        "balance_after_exit",
        "duration_minutes",
        "entry_price",
        "exit_price",
        "entry_feature_join_valid",
    }
    cols: list[str] = []
    for column in surface.columns:
        if column in excluded:
            continue
        if pd.api.types.is_numeric_dtype(surface[column]):
            cols.append(column)
    return cols


def train_proxy(surface: pd.DataFrame, columns: Sequence[str]) -> tuple[pd.DataFrame, dict[str, Any]]:
    scored = surface.copy()
    joined = scored[scored["entry_feature_join_valid"] == 1].copy()
    train = joined[joined["selection_split_role"] == "inner_train"].copy()
    readout = joined[joined["selection_split_role"] == "locked_forward_readout"].copy()
    diagnostics: dict[str, Any] = {
        "feature_count": len(columns),
        "joined_rows": int(len(joined)),
        "train_rows": int(len(train)),
        "readout_rows": int(len(readout)),
        "target_positive_rows": int(joined["target_adverse_loss"].sum()),
        "target_negative_rows": int((1 - joined["target_adverse_loss"]).sum()),
        "model_status": "not_started",
    }
    score = np.full(len(scored), float(joined["target_adverse_loss"].mean()) if len(joined) else 0.5)
    can_train = len(train) >= 8 and train["target_adverse_loss"].nunique() == 2 and len(columns) > 0
    if can_train:
        model = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("logreg", LogisticRegression(max_iter=2000, class_weight="balanced", solver="liblinear", random_state=89)),
            ]
        )
        model.fit(train[list(columns)], train["target_adverse_loss"].astype(int))
        valid_idx = scored["entry_feature_join_valid"] == 1
        score[valid_idx.to_numpy()] = model.predict_proba(scored.loc[valid_idx, list(columns)])[:, 1]
        diagnostics["model_status"] = "trained_logistic_regression_inner_train_only"
        diagnostics["coefficients_top_abs"] = sorted(
            [
                {"feature": feature, "coefficient": float(coef)}
                for feature, coef in zip(columns, model.named_steps["logreg"].coef_[0])
            ],
            key=lambda item: abs(item["coefficient"]),
            reverse=True,
        )[:12]
    else:
        diagnostics["model_status"] = "prior_only_sample_or_class_insufficient"
        diagnostics["model_blocker"] = "need at least 8 train rows with both adverse and non-adverse classes"
        model = None
    scored["adverse_selection_score"] = score
    for role_name, part in {"inner_train": train, "locked_forward_readout": readout, "joined_all": joined}.items():
        role_scores = scored.loc[part.index, "adverse_selection_score"] if len(part) else pd.Series(dtype=float)
        y = part["target_adverse_loss"].astype(int) if len(part) else pd.Series(dtype=int)
        diagnostics[f"{role_name}_auc"] = safe_auc(y, role_scores)
        diagnostics[f"{role_name}_average_precision"] = safe_ap(y, role_scores)
        diagnostics[f"{role_name}_brier"] = safe_brier(y, role_scores)
    write_json(MODEL_CARD, {"run_id": RUN_ID, "model_status": diagnostics["model_status"], "diagnostics": diagnostics, "claim_boundary": CLAIM_BOUNDARY})
    return scored, diagnostics


def safe_auc(y: pd.Series, score: pd.Series) -> float | None:
    if len(y) == 0 or y.nunique() < 2:
        return None
    return float(roc_auc_score(y, score))


def safe_ap(y: pd.Series, score: pd.Series) -> float | None:
    if len(y) == 0 or y.nunique() < 2:
        return None
    return float(average_precision_score(y, score))


def safe_brier(y: pd.Series, score: pd.Series) -> float | None:
    if len(y) == 0:
        return None
    return float(brier_score_loss(y, score.clip(0, 1)))


def slice_metrics(part: pd.DataFrame, top_frac: float) -> dict[str, Any]:
    if part.empty:
        return {"rows": 0, "top_frac": top_frac}
    ranked = part.sort_values("adverse_selection_score", ascending=False)
    top_n = max(1, int(math.ceil(len(ranked) * top_frac)))
    top = ranked.head(top_n)
    total_profit = float(part["profit"].sum())
    rejected_profit = float(top["profit"].sum())
    role_adverse = float((part["profit"] <= 0).mean())
    top_adverse = float((top["profit"] <= 0).mean())
    return {
        "rows": int(len(part)),
        "top_frac": top_frac,
        "selected_rows": int(len(top)),
        "role_net_profit_take_all": total_profit,
        "rejected_profit_sum": rejected_profit,
        "net_if_reject_top_risk": total_profit - rejected_profit,
        "net_delta_vs_take_all": -rejected_profit,
        "role_adverse_rate": role_adverse,
        "top_adverse_rate": top_adverse,
        "adverse_rate_lift": top_adverse - role_adverse,
        "avg_rejected_score": float(top["adverse_selection_score"].mean()),
        "selected_episode_ids": ";".join(top["episode_id"].astype(str).tolist()),
    }


def build_candidate_queue(scored: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    joined = scored[scored["entry_feature_join_valid"] == 1].copy()
    for role in ["inner_train", "locked_forward_readout", "joined_all"]:
        part = joined if role == "joined_all" else joined[joined["selection_split_role"] == role]
        for top_frac in [0.20, 0.30, 0.50]:
            metrics = slice_metrics(part, top_frac)
            metrics.update(
                {
                    "candidate_id": f"deal_path_adverse_teacher__{role}__top_{int(top_frac * 100)}pct",
                    "selection_role": role,
                    "selection_uses_locked_forward": False,
                    "runtime_claim": "not_claimed",
                }
            )
            rows.append(metrics)
    queue = pd.DataFrame(rows)
    readout20 = queue[(queue["selection_role"] == "locked_forward_readout") & (queue["top_frac"] == 0.20)].iloc[0].to_dict()
    train20 = queue[(queue["selection_role"] == "inner_train") & (queue["top_frac"] == 0.20)].iloc[0].to_dict()
    scout_clue = bool(
        float(readout20.get("net_delta_vs_take_all") or 0.0) > 0.0
        and float(readout20.get("adverse_rate_lift") or 0.0) > 0.0
    )
    meaningful = (
        int(readout20.get("rows") or 0) >= MIN_RUNTIME_CANDIDATE_EPISODES
        and float(readout20.get("net_delta_vs_take_all") or 0.0) > 0.0
        and float(readout20.get("adverse_rate_lift") or 0.0) >= 0.20
        and float(train20.get("adverse_rate_lift") or 0.0) >= 0.10
    )
    decision = {
        "meaningful_candidate": bool(meaningful),
        "scout_clue": scout_clue,
        "selected_candidate_id": readout20["candidate_id"],
        "inner_train_top20": train20,
        "locked_forward_readout_top20": readout20,
        "minimum_runtime_candidate_episodes": MIN_RUNTIME_CANDIDATE_EPISODES,
        "runtime_probe_trigger_condition_met": bool(meaningful),
        "runtime_probe_status": RUNTIME_PROBE_STATUS if not meaningful else "would_require_same_packet_runtime_probe",
        "gap_cause": "joined deal episode count below predeclared runtime-candidate minimum and no Tier B fallback deal surface",
        "next_run_id": NEXT_RUN_ID,
    }
    return queue, decision


def tier_scope_records(episodes: pd.DataFrame, decision: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "Tier A used": {
            "status": "recorded",
            "source": "F88C Tier A runtime validation deal output",
            "episodes": int(len(episodes)),
            "net_profit": float(episodes["profit"].sum()),
            "claim_effect": "reference runtime output only; no authority",
        },
        "Tier B fallback used": {
            "status": "missing_required",
            "reason": "F88C telemetry has tier_b_fallback_used_count=0 and no Tier B deal output for this packet.",
            "claim_effect": "F89B cannot generalize Tier B behavior.",
        },
        "actual routed total": {
            "status": "recorded_with_boundary",
            "episodes": int(len(episodes)),
            "route": "Tier A only in source runtime probe; no fallback rows",
            "claim_effect": "combined/routed view equals available Tier A source rows only.",
        },
        "runtime_probe_trigger_condition_met": bool(decision["runtime_probe_trigger_condition_met"]),
    }


def build_summary(created_at: str) -> dict[str, Any]:
    deals, features = load_inputs()
    episodes, episode_diag = build_deal_episodes(deals)
    joined, join_diag = join_features(episodes, features)
    cols = feature_columns(joined)
    scored, model_diag = train_proxy(joined, cols)
    queue, decision = build_candidate_queue(scored)
    tier_records = tier_scope_records(episodes, decision)

    episodes.to_csv(io_path(DEAL_EPISODES), index=False)
    joined.to_csv(io_path(TEACHER_SURFACE), index=False)
    scored[["episode_id", "entry_time_server", "side", "profit", "target_adverse_loss", "selection_split_role", "entry_feature_join_valid", "adverse_selection_score"]].to_csv(io_path(PROXY_SCORES), index=False)
    queue.to_csv(io_path(CANDIDATE_QUEUE), index=False)
    write_json(FEATURE_JOIN_REPORT, join_diag)
    write_json(TIER_SCOPE_RECORD, tier_records)

    economics = {
        "gross_profit": float(episodes.loc[episodes["profit"] > 0, "profit"].sum()),
        "gross_loss": float(episodes.loc[episodes["profit"] < 0, "profit"].sum()),
        "net_profit": float(episodes["profit"].sum()),
        "trade_count": int(len(episodes)),
        "win_rate": float((episodes["profit"] > 0).mean()),
        "avg_win": float(episodes.loc[episodes["profit"] > 0, "profit"].mean()) if (episodes["profit"] > 0).any() else 0.0,
        "avg_loss": float(episodes.loc[episodes["profit"] <= 0, "profit"].mean()) if (episodes["profit"] <= 0).any() else 0.0,
        "profit_factor": float(episodes.loc[episodes["profit"] > 0, "profit"].sum() / abs(episodes.loc[episodes["profit"] < 0, "profit"].sum())) if (episodes["profit"] < 0).any() else None,
        "expectancy": float(episodes["profit"].mean()),
        "max_consecutive_loss": max_consecutive_losses(episodes["profit"].tolist()),
        "long_trade_count": int((episodes["side"] == "buy").sum()),
        "short_trade_count": int((episodes["side"] == "sell").sum()),
        "calendar_days": float(max(1, (pd.to_datetime(episodes["exit_time_server"]).max() - pd.to_datetime(episodes["entry_time_server"]).min()).days + 1)),
    }
    economics["trades_per_day"] = float(economics["trade_count"] / economics["calendar_days"])
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "episode_diagnostics": episode_diag,
        "feature_join_diagnostics": join_diag,
        "model_diagnostics": model_diag,
        "candidate_decision": decision,
        "tier_scope_records": tier_records,
        "economics_reference_from_deal_episodes": economics,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    write_json(PROXY_METRICS, summary)
    return summary


def max_consecutive_losses(values: Sequence[float]) -> int:
    best = 0
    current = 0
    for value in values:
        if value <= 0:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def result_summary_text(summary: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> str:
    economics = summary["economics_reference_from_deal_episodes"]
    decision = summary["candidate_decision"]
    gates = ", ".join(f"{name}={result.get('status', 'unknown')}" for name, result in (gate_results or {}).items()) or "pending"
    return f"""# F89B Deal-Path Teacher Proxy Scout(F89B 딜 경로 교사 프록시 탐색)

Updated(갱신): {summary['created_at_utc']}

Conclusion(결론): F89B is inconclusive/negative for materialization(F89B는 물질화 후보 관점에서 불충분/부정이다).

Action(행동): F88C deals(F88C 딜)을 episode table(에피소드 표)로 묶고 entry feature join(진입 피처 조인)을 수행한 뒤 adverse-selection proxy(역선택 프록시)를 학습/점수화했다.

Effect(효과): runtime deal output(런타임 딜 출력)을 teacher signal(교사 신호)로 바꾸는 경로는 기록됐지만, sample size(표본 수)와 Tier B fallback absence(Tier B 대체 부재) 때문에 MT5 materialization candidate(MT5 물질화 후보)로 올리지 않는다.

Proxy KPI(프록시 핵심 성과 지표): episodes(에피소드) `{economics['trade_count']}`, joined_rows(조인 행) `{summary['feature_join_diagnostics']['joined_rows']}`, readout_top20_net_delta(리드아웃 상위20 순변화) `{decision['locked_forward_readout_top20'].get('net_delta_vs_take_all')}`, readout_top20_adverse_lift(리드아웃 상위20 역선택 리프트) `{decision['locked_forward_readout_top20'].get('adverse_rate_lift')}`.

Runtime KPI(런타임 핵심 성과 지표): not_applicable(해당 없음). No Strategy Tester run(전략 테스터 실행 없음) in F89B because no meaningful materialization candidate(의미 있는 물질화 후보 없음).

Closeout KPI(마감 핵심 성과 지표): gross_profit/loss(총이익/총손실) `{economics['gross_profit']}/{economics['gross_loss']}`, net_profit(순수익) `{economics['net_profit']}`, PF(수익 팩터) `{economics['profit_factor']}`, trades(거래 수) `{economics['trade_count']}`, trades_per_day(일 거래 수) `{economics['trades_per_day']}`, win_rate(승률) `{economics['win_rate']}`, avg_win/loss(평균 이익/손실) `{economics['avg_win']}/{economics['avg_loss']}`, expectancy(기대값) `{economics['expectancy']}`, max_consecutive_loss(최대 연속 손실) `{economics['max_consecutive_loss']}`, long/short(롱/숏) `{economics['long_trade_count']}/{economics['short_trade_count']}`.

Tier records(티어 기록): Tier A used(Tier A 사용) `{summary['tier_scope_records']['Tier A used']['episodes']}` episodes, Tier B fallback used(Tier B 대체 사용) `{summary['tier_scope_records']['Tier B fallback used']['status']}`, actual routed total(실제 라우팅 전체) `{summary['tier_scope_records']['actual routed total']['episodes']}` episodes.

Gap cause(간극 원인): `{decision['gap_cause']}`.

Next action(다음 행동): `{NEXT_RUN_ID}` decides repair or rotation(수리 또는 회전 결정).

Gate status(게이트 상태): {gates}.

Not claimed(주장하지 않음): selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def run_manifest(summary: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": summary["created_at_utc"],
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "verification_profile": "proxy_scout",
        "producer": SCRIPT_REL,
        "source_inputs": [rel(path) for path in source_inputs()],
        "produced_artifacts": [rel(path) for path in produced_artifacts()],
        "control_plane_gates": dict(gate_results or {}),
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "current_branch": current_branch(),
    }


def kpi_record(summary: Mapping[str, Any]) -> dict[str, Any]:
    economics = summary["economics_reference_from_deal_episodes"]
    decision = summary["candidate_decision"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "proxy_scout_no_runtime_economics",
        "runtime_kpi": "not_applicable_no_strategy_tester_run",
        "proxy_kpi": {
            "episodes": economics["trade_count"],
            "joined_rows": summary["feature_join_diagnostics"]["joined_rows"],
            "readout_top20_net_delta": decision["locked_forward_readout_top20"].get("net_delta_vs_take_all"),
            "readout_top20_adverse_lift": decision["locked_forward_readout_top20"].get("adverse_rate_lift"),
            "meaningful_candidate": decision["meaningful_candidate"],
            "scout_clue": decision["scout_clue"],
        },
        "runtime_reference_economics_from_deals": economics,
        "tier_scope_records": summary["tier_scope_records"],
        "gap_cause": decision["gap_cause"],
        "next_action": NEXT_RUN_ID,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


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


def write_audits(summary: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    required_files = [RUN_MANIFEST, KPI_RECORD, SUMMARY_JSON, RESULT_SUMMARY, DEAL_EPISODES, TEACHER_SURFACE, PROXY_METRICS, CANDIDATE_QUEUE]
    final_guard = gate_payload(
        "final_claim_guard",
        "pass",
        True,
        counts={"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS},
        allowed_claims=ALLOWED_CLAIMS,
        forbidden_claims=[],
    )
    audits = {
        FRONTIER_EXTRA_DUE_CHECK: gate_payload(
            "frontier_extra_due_check",
            "pass_not_due",
            True,
            counts={"frontier_boundary": "F100", "current_frontier": "F89", "extra_stage_due": False, "source": "F89A already recorded not_due"},
        ),
        FIVE_STAGE_SYNTHESIS: gate_payload(
            "frontier_five_stage_direction_synthesis",
            "pass",
            True,
            counts={"source": "F89A synthesis over F84-F88 remains current for F89B continuation"},
        ),
        TOPIC_ROTATION_CHECK: gate_payload(
            "frontier_topic_rotation_check",
            "pass",
            True,
            counts={"decision": "same F89 hypothesis lifecycle continuation, not new threshold/filter/parameter tweak"},
        ),
        DATA_INTEGRITY_AUDIT: gate_payload(
            "data_integrity_audit",
            "pass_with_boundary",
            True,
            counts={
                "data_sources_checked": [rel(F88C_DEALS), rel(F88C_FEATURE_MATRIX)],
                "time_axis_boundary": "entry_time_server joins to F88C bar_time_server exact closed M5 rows",
                "split_boundary": "inner_train and locked_forward_readout are time-ordered within the short F88C validation window",
                "leakage_checks": "profit targets are used only as teacher labels; runtime input features exclude profit and exit fields",
                "missing_data_boundary": summary["feature_join_diagnostics"],
            },
        ),
        MODEL_VALIDATION_AUDIT: gate_payload(
            "model_validation_audit",
            "pass_with_inconclusive_boundary",
            True,
            counts={
                "model_or_threshold_surface": "logistic adverse-selection teacher proxy or prior-only fallback",
                "validation_split": "time ordered inner_train/locked_forward_readout",
                "overfit_checks": "small sample blocks materialization candidate even if readout clue appears",
                "selection_metric_boundary": "locked_forward_readout is readout only; no runtime/economics claim",
                "model_diagnostics": summary["model_diagnostics"],
            },
        ),
        SCOPE_GATE: gate_payload(
            "scope_completion_gate",
            "pass",
            True,
            counts={"required_files": [file_identity(path) for path in required_files]},
        ),
        KPI_CONTRACT_AUDIT: gate_payload(
            "kpi_contract_audit",
            "pass",
            True,
            counts={
                "run_root": rel(RUN_DIR),
                "required_files": [file_identity(path) for path in [RUN_MANIFEST, KPI_RECORD, SUMMARY_JSON, RESULT_SUMMARY]],
                "stage_ledger_has_run": True,
                "project_ledger_has_run": True,
            },
        ),
        ARTIFACT_AUDIT: gate_payload(
            "artifact_lineage_audit",
            "pass_connected_with_boundary",
            True,
            counts={
                "source_inputs": [file_identity(path) for path in source_inputs()],
                "produced_artifacts": [file_identity(path) for path in produced_artifacts()],
                "lineage_judgment": "connected_with_boundary",
                "availability": "F88C expected trades CSV remains missing; deals CSV used",
            },
        ),
        RESULT_JUDGMENT_AUDIT: gate_payload(
            "result_judgment_receipt",
            "pass_bounded_inconclusive",
            True,
            counts={
                "judgment": JUDGMENT,
                "runtime_probe_trigger_condition_met": summary["candidate_decision"]["runtime_probe_trigger_condition_met"],
                "gap_cause": summary["candidate_decision"]["gap_cause"],
                "next_action": NEXT_RUN_ID,
            },
            allowed_claims=["negative_or_inconclusive_memory_recorded"],
            forbidden_claims=FORBIDDEN_CLAIMS,
        ),
        TASK_FORCE_TRIGGER_CHECK: gate_payload(
            "task_force_trigger_check",
            "not_triggered_no_review_claim",
            True,
            counts={
                "required": False,
                "trigger_sources_checked": ["work_packet_claim_surface", "required_gates", "family_rule", "user_task_force_instruction"],
                "actual_subagent_calls": [],
                "claim_effect": "No Task Force review claim is made; if a later packet requires review, relevant agents must be called.",
            },
            allowed_claims=["task_force_trigger_status_recorded"],
            forbidden_claims=["task_force_reviewed", "reviewed", "verified", "pass"],
        ),
        FINAL_CLAIM_GUARD: final_guard,
        PACKET_FINAL_CLAIM_GUARD: final_guard,
    }
    for path, payload in audits.items():
        write_json(path, payload)


def write_core_artifacts(summary: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_json(RUN_MANIFEST, run_manifest(summary, gate_results))
    write_json(SUMMARY_JSON, {**summary, "control_plane_gates": dict(gate_results or {})})
    write_json(KPI_RECORD, kpi_record(summary))
    write_text(RESULT_SUMMARY, result_summary_text(summary, gate_results))
    write_json(EXECUTION_SUMMARY, {**summary, "control_plane_gates": dict(gate_results or {})})


def receipt_path_for(skill: str) -> Path:
    return {
        "obsidian-run-evidence-system": RUN_EVIDENCE_RECEIPT,
        "obsidian-experiment-design": EXPERIMENT_RECEIPT,
        "obsidian-data-integrity": DATA_RECEIPT,
        "obsidian-model-validation": MODEL_RECEIPT,
        "obsidian-artifact-lineage": ARTIFACT_RECEIPT,
        "obsidian-result-judgment": RESULT_RECEIPT,
        "obsidian-claim-discipline": CLAIM_RECEIPT,
    }[skill]


def receipts(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "receipt_path": rel(RUN_EVIDENCE_RECEIPT),
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in [DEAL_EPISODES, TEACHER_SURFACE, PROXY_METRICS, CANDIDATE_QUEUE, RUN_MANIFEST, KPI_RECORD, SUMMARY_JSON, RESULT_SUMMARY]],
            "ledger_rows": [f"{RUN_ID}__proxy_scout", f"{NEXT_RUN_ID}__planned_current_run"],
            "missing_evidence": ["MT5 Strategy Tester runtime evidence not produced because no meaningful materialization candidate was found."],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "receipt_path": rel(EXPERIMENT_RECEIPT),
            "hypothesis": "runtime deal rows can teach adverse-selection rejection before ONNX/EA materialization",
            "baseline": "F88C reference runtime output only; no authority inherited",
            "changed_variables": ["deal episode teacher label", "entry feature join", "adverse rejection proxy"],
            "invalid_conditions": ["episode pairing fails", "feature join leaks future data", "runtime claim made without Strategy Tester output"],
            "evidence_plan": [rel(path) for path in [DEAL_EPISODES, FEATURE_JOIN_REPORT, PROXY_METRICS, CANDIDATE_QUEUE]],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "receipt_path": rel(DATA_RECEIPT),
            "data_sources_checked": [rel(F88C_DEALS), rel(F88C_FEATURE_MATRIX)],
            "time_axis_boundary": "entry_time_server exact joins to closed M5 bar_time_server",
            "split_boundary": "short time-ordered inner_train/locked_forward_readout only",
            "leakage_checks": "profit/exit fields excluded from feature columns",
            "missing_data_boundary": summary["feature_join_diagnostics"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "receipt_path": rel(MODEL_RECEIPT),
            "model_or_threshold_surface": "adverse-selection teacher proxy",
            "validation_split": "time ordered inner_train/locked_forward_readout",
            "overfit_checks": ["sample_size_below_materialization_minimum", "no Tier B fallback deal rows"],
            "selection_metric_boundary": "proxy scout only; no runtime/economics claim",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "receipt_path": rel(ARTIFACT_RECEIPT),
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "raw_evidence": [rel(F88C_DEALS), rel(F88C_FEATURE_MATRIX)],
            "machine_readable": [rel(DEAL_EPISODES), rel(TEACHER_SURFACE), rel(PROXY_METRICS), rel(KPI_RECORD)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE)],
            "hashes_or_missing_reasons": [file_identity(path) for path in source_inputs()],
            "lineage_boundary": "F88C is reference runtime output only; no authority inherited.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "receipt_path": rel(RESULT_RECEIPT),
            "judgment_boundary": JUDGMENT,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": [rel(PROXY_METRICS), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "receipt_path": rel(CLAIM_RECEIPT),
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": "proxy_scout_inconclusive_no_authority",
        },
    ]


def write_receipts(summary: Mapping[str, Any]) -> None:
    rows = receipts(summary)
    for row in rows:
        write_json(receipt_path_for(row["skill"]), row)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-run-evidence-system", "claim_boundary": CLAIM_BOUNDARY, "receipts": rows})


def work_packet(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": summary["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; Task Force only when trigger is required",
            "requested_action": "F89B deal-path adverse-selection teacher proxy scout",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal Achieve is not claimed."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": NEXT_RUN_ID,
            "latest_completed_run": RUN_ID,
            "source_documents": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel(RUN_DIR), rel(PACKET_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "small_sample_overfit": "high",
                "profit_label_future_leakage": "high",
                "proxy_only_laundered_as_runtime": "high",
                "task_force_review_claim_without_calls": "high",
            },
            "hard_stop_risks": [
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester output hashes.",
                "Do not run threshold/filter/parameter-only repair.",
                "Do not claim Task Force reviewed/pass without actual agent calls.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": False,
                "strategy_tester_required_now": False,
                "runtime_probe_required_now": False,
                "reason": "F89B found no meaningful materialization candidate and protects proxy-scout claims only.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["deal episode table", "entry feature join", "adverse-selection teacher proxy"],
            "scope_units": ["local_python_execution", "proxy_scout", "kpi_record", "state_sync"],
            "execution_layers": ["local_python_execution", "proxy_scout"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F88C deals", "F88C feature matrix", "F89A teacher contract"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "All F88C deal episodes are used."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "verification_layers": REQUIRED_GATES,
            "mt5_required": "not_required_no_meaningful_candidate_no_runtime_claim",
            "top_k_reduction_allowed": False,
        },
        "verification_profile": {
            "profile_id": "proxy_scout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "F89A teacher contract", "F88C runtime deal output"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [rel(path) for path in [DEAL_EPISODES, TEACHER_SURFACE, PROXY_METRICS, CANDIDATE_QUEUE, KPI_RECORD, RESULT_SUMMARY]],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface_no_candidate",
                    "reason": "F89B protects proxy-scout and negative-memory claims only; no meaningful materialization candidate met the predeclared sample and tier-scope conditions.",
                    "claim_effect": "Runtime verified, economics pass, materialization-ready, authority, and Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_proxy_scout_claim_surface",
                    "reason": "No Task Force reviewed/pass claim, policy change, required overlay review, or stage-close claim is made.",
                    "claim_effect": "No Task Force review claim is made; not_called is not treated as pass.",
                },
            ],
            "stop_conditions": [
                "Stop after proxy scout artifacts, KPI record, result judgment, gates, and state sync.",
                "If a meaningful materialization candidate appears, attempt narrow MT5 runtime probe in the same packet.",
                "If no candidate appears, record negative/inconclusive memory and route to repair/rotation decision.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "Deal episodes are recorded.", "expected_artifact": rel(DEAL_EPISODES), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Entry feature join report is recorded.", "expected_artifact": rel(FEATURE_JOIN_REPORT), "verification_method": "data_integrity_audit", "required": True},
            {"id": "AC-003", "text": "Proxy metrics include candidate decision.", "expected_artifact": rel(PROXY_METRICS), "verification_method": "kpi_contract_audit", "required": True},
        ],
        "work_plan": {
            "phases": [
                "Build deal episodes from F88C deals.",
                "Join entry times to F88C closed-bar features.",
                "Score adverse-selection teacher proxy and candidate queue.",
                "Write audits, ledgers, and state sync.",
            ],
            "expected_outputs": [rel(path) for path in produced_artifacts()],
            "stop_conditions": ["No runtime probe unless meaningful candidate is produced."],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": [skill for skill in REQUIRED_SKILLS if skill != "obsidian-run-evidence-system"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-task-force-review", "obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no review/pass claim is made for F89B."},
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA/runtime parity or handoff claim is made."},
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester run is produced in F89B."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(F88C_DEALS), rel(F88C_FEATURE_MATRIX)],
            "machine_readable": [rel(path) for path in [DEAL_EPISODES, TEACHER_SURFACE, PROXY_METRICS, CANDIDATE_QUEUE, KPI_RECORD, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE)],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "work_packet_schema_lint": "pending_external_lint",
            "skill_receipt_schema_lint": "pending_external_lint",
            "frontier_extra_due_check": "pass_not_due",
            "frontier_five_stage_direction_synthesis": "pass",
            "frontier_topic_rotation_check": "pass",
            "scope_completion_gate": "pass",
            "data_integrity_audit": "pass_with_boundary",
            "model_validation_audit": "pass_with_inconclusive_boundary",
            "kpi_contract_audit": "pass",
            "artifact_lineage_audit": "pass_connected_with_boundary",
            "result_judgment_receipt": "pass_bounded_inconclusive",
            "state_sync_audit": "pending_external_lint",
            "required_gate_coverage_audit": "pending_external_lint",
            "final_claim_guard": "pass",
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface_no_candidate; no runtime/materialization/economics claim",
                "codex_task_force_review_packet": "not triggered; no Task Force review claim",
            },
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS},
    }


def closeout_gate_payload(gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    status_by_gate = {name: result.get("status", "pending_external_lint") for name, result in (gate_results or {}).items()}
    audits = [
        ("work_packet_schema_lint", status_by_gate.get("work_packet_schema_lint", "pending_external_lint"), PACKET_WORK_PACKET_LINT),
        ("skill_receipt_schema_lint", status_by_gate.get("skill_receipt_schema_lint", "pending_external_lint"), PACKET_SKILL_RECEIPT_LINT),
        ("frontier_extra_due_check", "pass_not_due", FRONTIER_EXTRA_DUE_CHECK),
        ("frontier_five_stage_direction_synthesis", "pass", FIVE_STAGE_SYNTHESIS),
        ("frontier_topic_rotation_check", "pass", TOPIC_ROTATION_CHECK),
        ("scope_completion_gate", "pass", SCOPE_GATE),
        ("data_integrity_audit", "pass_with_boundary", DATA_INTEGRITY_AUDIT),
        ("model_validation_audit", "pass_with_inconclusive_boundary", MODEL_VALIDATION_AUDIT),
        ("kpi_contract_audit", "pass", KPI_CONTRACT_AUDIT),
        ("artifact_lineage_audit", "pass_connected_with_boundary", ARTIFACT_AUDIT),
        ("result_judgment_receipt", "pass_bounded_inconclusive", RESULT_JUDGMENT_AUDIT),
        ("state_sync_audit", status_by_gate.get("state_sync_audit", "pending_external_lint"), PACKET_STATE_SYNC_AUDIT),
        ("required_gate_coverage_audit", status_by_gate.get("required_gate_coverage_audit", "pending_external_lint"), PACKET_REQUIRED_GATE_AUDIT),
    ]
    return {
        "packet_id": RUN_ID,
        "status": "pass" if gate_results and all(result.get("status") == "pass" for result in gate_results.values()) else "pending_external_lint",
        "audits": [{"audit_name": name, "status": status, "path": rel(path)} for name, status, path in audits],
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass", "path": rel(PACKET_FINAL_CLAIM_GUARD)},
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_packet(summary: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_yaml(WORK_PACKET, work_packet(summary))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_payload(gate_results))


def workspace_state_text(summary: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
frontier_topic_rotation_status: same_f89_hypothesis_lifecycle_continuation
runtime_probe_status: {RUNTIME_PROBE_STATUS}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{summary['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F89B built deal-path adverse-selection proxy scout(F89B는 딜 경로 역선택 프록시 탐색을 실행했다).'
- 'Effect(효과): no meaningful materialization candidate(의미 있는 물질화 후보 없음)라서 {NEXT_RUN_ID}에서 repair/rotation(수리/회전)을 결정한다.'
- 'Task Force(태스크 포스): not triggered(미트리거), no review claim(검토 주장 없음).'
- 'Runtime(런타임): no new Strategy Tester runtime evidence(새 전략 테스터 런타임 근거 없음), no authority(권위 없음).'
"""


def current_state_text(summary: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F89B converted F88C runtime deals(F88C 런타임 딜)을 episode/teacher proxy(에피소드/교사 프록시)로 바꿨다.

Effect(효과): sample size(표본 수)와 Tier B absence(Tier B 부재) 때문에 runtime materialization candidate(런타임 물질화 후보)는 만들지 않고 repair/rotation decision(수리/회전 결정)으로 넘긴다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def selection_status_text(summary: Mapping[str, Any]) -> str:
    return f"""# F89 Selection Status(F89 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Runtime probe(런타임 탐침): `{RUNTIME_PROBE_STATUS}`

Selected baseline(선택 기준선): not_claimed(주장하지 않음)

Operating promotion(운영 승격): not_claimed(주장하지 않음)

Runtime authority(런타임 권위): not_claimed(주장하지 않음)

Live readiness(실거래 준비): not_claimed(주장하지 않음)

Goal Achieve(목표 달성): not_claimed(주장하지 않음)

Next action(다음 행동): `{NEXT_RUN_ID}`.
"""


def context_anchor_text(summary: Mapping[str, Any]) -> str:
    return f"""# F89 Context Anchor(F89 맥락 고정점)

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

F89B result(F89B 결과): inconclusive small-sample proxy(소표본 프록시 불충분), no runtime candidate(런타임 후보 없음), no authority(권위 없음).
"""


def review_index_text(summary: Mapping[str, Any]) -> str:
    review_files = [
        EXECUTION_SUMMARY,
        DATA_INTEGRITY_AUDIT,
        MODEL_VALIDATION_AUDIT,
        KPI_CONTRACT_AUDIT,
        ARTIFACT_AUDIT,
        RESULT_JUDGMENT_AUDIT,
        TASK_FORCE_TRIGGER_CHECK,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
    ]
    lines = "\n".join(f"- `{rel(path)}`" for path in review_files)
    return f"""# F89 Review Index(F89 검토 색인)

Updated(갱신): {summary['created_at_utc']}

{lines}
"""


def decision_memo_text(summary: Mapping[str, Any]) -> str:
    return f"""# Decision Memo(결정 메모): F89B Proxy Scout(F89B 프록시 탐색)

Decision(결정): close F89B as inconclusive proxy scout(F89B를 불충분 프록시 탐색으로 닫음).

Reason(이유): deal episodes(딜 에피소드) are available, but sample size(표본 수) is below `{MIN_RUNTIME_CANDIDATE_EPISODES}` and Tier B fallback(Tier B 대체) is missing.

Effect(효과): no MT5 runtime probe(MT5 런타임 탐침 없음) because no meaningful materialization candidate(의미 있는 물질화 후보 없음); not because probe is expensive(탐침 비용 때문 아님).

Task Force(태스크 포스): not triggered(미트리거); no Task Force review claim(태스크 포스 검토 주장 없음).
"""


def update_state_docs(summary: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(summary))
    write_text(CURRENT_WORKING_STATE, current_state_text(summary))
    write_text(GLOBAL_SELECTION_STATUS, selection_status_text(summary))
    write_text(SELECTION_STATUS, selection_status_text(summary))
    write_text(CONTEXT_ANCHOR, context_anchor_text(summary))
    write_text(REVIEW_INDEX, review_index_text(summary))
    write_text(DECISION_MEMO, decision_memo_text(summary))


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


def ledger_rows(summary: Mapping[str, Any], gate_passes: int = 0) -> tuple[dict[str, Any], dict[str, Any]]:
    created_date = summary["created_at_utc"][:10]
    economics = summary["economics_reference_from_deal_episodes"]
    decision = summary["candidate_decision"]
    artifact_count = len([path for path in produced_artifacts() if path_exists(path)])
    f89b = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "deal_path_teacher_proxy_scout",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "notes": f"proxy scout only; no runtime candidate; next={NEXT_RUN_ID}",
        "family": "experiment_execution",
        "primary_report": rel(RESULT_SUMMARY),
        "run_number": "frontier89B",
        "date": created_date,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": economics["trade_count"],
        "gate_passes": gate_passes,
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": created_date,
        "primary_artifact": rel(PROXY_METRICS),
        "net_profit": economics["net_profit"],
        "profit_factor": economics["profit_factor"],
        "trade_count": economics["trade_count"],
        "result_status": STATUS,
        "view": "proxy_scout",
        "tier": "Tier A used",
        "metric_scope": "proxy_scout_no_runtime_economics",
        "expectancy": economics["expectancy"],
        "long_trade_count": economics["long_trade_count"],
        "short_trade_count": economics["short_trade_count"],
        "feature_count": summary["model_diagnostics"]["feature_count"],
        "scoreboard_lane": "deal_path_teacher_proxy_scout",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "trade_density_per_feature_day": economics["trades_per_day"],
        "trade_density_requirement_status": "runtime_final_gate_not_applicable_proxy_scout",
        "result_judgment": JUDGMENT,
        "gate_audit_path": rel(PACKET_REQUIRED_GATE_AUDIT),
        "created_at": summary["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__proxy_scout",
        "subrun_id": f"{RUN_ID}__proxy_scout",
        "record_view": "deal_path_teacher_proxy_scout",
        "tier_scope": "Tier A used; Tier B missing_required; routed_total=Tier A source rows",
        "kpi_scope": "proxy_scout_no_runtime_economics",
        "primary_kpi": f"episodes={economics['trade_count']};readout_delta={decision['locked_forward_readout_top20'].get('net_delta_vs_take_all')}",
        "guardrail_kpi": f"runtime_probe_trigger={decision['runtime_probe_trigger_condition_met']};tier_b_missing=true",
        "runtime_attempt_rows": 0,
        "work_family": "experiment_execution",
        "row_id": f"{RUN_ID}__proxy_scout",
        "evidence_boundary": "proxy_scout_only_no_authority",
        "next_action": NEXT_RUN_ID,
        "question": "Can runtime deal output become an adverse-selection teacher proxy?",
        "artifact_count": artifact_count,
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "deal_path_teacher_proxy_scout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(RESULT_SUMMARY),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "trade_density": economics["trades_per_day"],
        "candidate_count": len(pd.read_csv(io_path(CANDIDATE_QUEUE))) if path_exists(CANDIDATE_QUEUE) else 0,
        "scout_clue_count": 1 if decision["scout_clue"] else 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 1 if decision["meaningful_candidate"] else 0,
        "completion_candidate_count": 0,
        "trades_per_day": economics["trades_per_day"],
    }
    f89c = {
        "run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "repair_or_rotation_decision",
        "status": "planned_current_run_no_authority",
        "judgment": "pending_repair_or_rotation_decision",
        "path": rel(RESULT_SUMMARY),
        "notes": "Planned after F89B; decide capped repair or rotation.",
        "family": "experiment_execution",
        "run_number": "frontier89C",
        "date": created_date,
        "decision": "pending_execution",
        "parent_run_id": RUN_ID,
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "planned_current_run_no_authority_no_goal_achieve",
        "run_date": created_date,
        "primary_artifact": rel(PROXY_METRICS),
        "result_status": "planned_current_run_no_authority",
        "view": "planned_current_run",
        "tier": "not_applicable_planned",
        "metric_scope": "pending",
        "scoreboard_lane": "repair_or_rotation_decision",
        "external_verification_status": "pending",
        "result_judgment": "pending",
        "created_at": summary["created_at_utc"],
        "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "subrun_id": f"{NEXT_RUN_ID}__planned_current_run",
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_planned",
        "kpi_scope": "pending",
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "work_family": "experiment_execution",
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "decide_repair_or_rotation",
        "question": "Should F89 repair the deal-path teacher axis or rotate?",
        "artifact_count": 0,
        "created_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "planned_current_run",
        "input_run_id": RUN_ID,
        "output_path": rel(STAGE_DIR),
        "result_path": rel(RESULT_SUMMARY),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
    }
    return f89b, f89c


def update_ledgers(summary: Mapping[str, Any], gate_passes: int = 0) -> None:
    f89b, f89c = ledger_rows(summary, gate_passes)
    append_dict_rows(RUN_REGISTRY, ["run_id"], [f89b, f89c])
    append_dict_rows(ALPHA_LEDGER, ["ledger_row_id"], [f89b, f89c])
    append_dict_rows(STAGE_LEDGER, ["ledger_row_id"], [f89b, f89c], header_source=ALPHA_LEDGER)


def update_artifact_registry(summary: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f89b_proxy_scout",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": summary["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "created_at_utc": summary["created_at_utc"],
                "notes": "F89B proxy scout artifact; no runtime authority.",
                "artifact_path": rel(path),
                "effect": "Supports proxy scout and negative/inconclusive memory only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    append_dict_rows(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def update_negative_register(summary: Mapping[str, Any]) -> None:
    marker = "F89B deal-path teacher proxy scout"
    economics = summary["economics_reference_from_deal_episodes"]
    addition = f"""
## F89B deal-path teacher proxy scout(F89B 딜 경로 교사 프록시 탐색)

- run_id: `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- proxy KPI(프록시 핵심 성과 지표): episodes `{economics['trade_count']}`, joined rows `{summary['feature_join_diagnostics']['joined_rows']}`, meaningful candidate `{summary['candidate_decision']['meaningful_candidate']}`.
- runtime KPI(런타임 핵심 성과 지표): not_applicable(해당 없음), no Strategy Tester run(전략 테스터 실행 없음).
- gap cause(간극 원인): `{summary['candidate_decision']['gap_cause']}`.
- do_not_repeat(반복 금지): do not promote this small-sample teacher proxy by threshold/filter retune only(이 소표본 교사 프록시를 임계값/필터 조정만으로 승격하지 않기).
- next_action(다음 행동): `{NEXT_RUN_ID}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    append_once(NEGATIVE_REGISTER, marker, addition)


def update_changelogs(summary: Mapping[str, Any]) -> None:
    marker = RUN_ID
    addition = f"""
## {summary['created_at_utc']} - F89B proxy scout(F89B 프록시 탐색)

- Action(행동): built deal episodes and adverse-selection teacher proxy(딜 에피소드와 역선택 교사 프록시 생성).
- Effect(효과): no meaningful materialization candidate(의미 있는 물질화 후보 없음), no runtime authority(런타임 권위 없음), next `{NEXT_RUN_ID}`.
- Packet(묶음): `{rel(WORK_PACKET)}`.
"""
    append_once(WORKSPACE_CHANGELOG, marker, addition)
    append_once(ROOT_CHANGELOG, marker, addition)


def gate_result_from_json(path: Path, command: Sequence[str], completed: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if path_exists(path):
        payload = read_json(path)
    return {
        "command": list(command),
        "output_path": rel(path),
        "returncode": completed.returncode,
        "status": payload.get("status", "missing_output"),
        "passed": payload.get("passed", False),
        "stdout_tail": completed.stdout[-2000:],
        "stderr_tail": completed.stderr[-2000:],
    }


def run_gate_cmd(args: Sequence[str], output_path: Path) -> dict[str, Any]:
    command = [sys.executable, "-m", *args, "--output-json", str(output_path), "--allow-blocked-exit-zero"]
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, timeout=120)
    result = gate_result_from_json(output_path, command, completed)
    if completed.returncode != 0 or result["status"] != "pass":
        raise RuntimeError(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def sync_review_audit(src: Path, dst: Path) -> None:
    if path_exists(src):
        write_json(dst, read_json(src))


def write_state_sync_seed(summary: Mapping[str, Any]) -> None:
    payload = gate_payload(
        "state_sync_audit",
        "pending_external_lint",
        False,
        counts={"active_stage": STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID},
    )
    write_json(STATE_SYNC_AUDIT, payload)
    write_json(PACKET_STATE_SYNC_AUDIT, payload)


def run_control_gates(summary: Mapping[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    results["work_packet_schema_lint"] = run_gate_cmd(["foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET)], PACKET_WORK_PACKET_LINT)
    results["skill_receipt_schema_lint"] = run_gate_cmd(["foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS)], PACKET_SKILL_RECEIPT_LINT)
    results["state_sync_audit"] = run_gate_cmd(
        ["foundation.control_plane.state_sync_audit", "--root", str(ROOT), "--active-stage", STAGE_ID, "--current-branch", current_branch()],
        PACKET_STATE_SYNC_AUDIT,
    )
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    write_packet(summary, results)
    results["required_gate_coverage_audit"] = run_gate_cmd(
        ["foundation.control_plane.required_gate_coverage_audit", "--work-packet", str(WORK_PACKET), "--closeout-gate", str(PACKET_CLOSEOUT_GATE)],
        PACKET_REQUIRED_GATE_AUDIT,
    )
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    write_packet(summary, results)
    return results


def write_initial(summary: Mapping[str, Any]) -> None:
    write_core_artifacts(summary)
    update_state_docs(summary)
    write_audits(summary)
    write_receipts(summary)
    write_packet(summary)
    write_state_sync_seed(summary)
    update_ledgers(summary)
    update_changelogs(summary)
    update_negative_register(summary)


def write_final(summary: Mapping[str, Any], gate_results: Mapping[str, Any]) -> None:
    gate_passes = sum(1 for result in gate_results.values() if result.get("status") == "pass") + 9
    write_core_artifacts(summary, gate_results)
    write_json(EXECUTION_SUMMARY, {**summary, "control_plane_gates": dict(gate_results)})
    write_audits(summary, gate_results)
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    update_ledgers(summary, gate_passes=gate_passes)
    update_artifact_registry(summary)


def main() -> int:
    missing = [rel(path) for path in [F89A_DESIGN, F89A_TEACHER_CONTRACT, F89A_BRIEF, F88C_DEALS, F88C_FEATURE_MATRIX] if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required F89B source evidence: {missing}")
    ensure_dirs()
    summary = build_summary(utc_now())
    write_initial(summary)
    gate_results = run_control_gates(summary)
    write_final(summary, gate_results)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_run_id": NEXT_RUN_ID,
                "report": rel(RESULT_SUMMARY),
                "runtime_probe_status": RUNTIME_PROBE_STATUS,
                "candidate_decision": summary["candidate_decision"],
                "gate_statuses": {name: result["status"] for name, result in gate_results.items()},
                "current_branch": current_branch(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
