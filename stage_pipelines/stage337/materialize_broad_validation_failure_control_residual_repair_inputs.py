from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import ordered_sklearn_probabilities, sha256_file  # noqa: E402
from stage_pipelines.stage337 import design_broad_validation_failure_control_residual_repair as dt  # noqa: E402
from stage_pipelines.stage337 import train_guarded_prediction_surface_validation_edge_repair_candidates as do  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
)


TODAY = "2026-05-28"
STAGE_ID = dt.STAGE_ID
RUN_NUMBER = "run337DU"
RUN_ID = "run337DU_materialize_broad_validation_failure_control_residual_repair_inputs_without_db_v1"
PARENT_RUN_ID = dt.RUN_ID
NEXT_RUN_ID = "run337DV_review_broad_validation_failure_control_residual_materialization_without_db_v1"
STATUS = "completed_stage337DU_broad_validation_failure_control_residual_inputs_materialized_no_training_no_selection"
JUDGMENT = "transfer_density_control_family_inputs_materialized_review_required"
DECISION = "stage337DU_open_run337DV_review_broad_validation_failure_control_residual_materialization"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DU_broad_validation_failure_control_residual_input_materialization_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dt.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dt.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DU_broad_validation_failure_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DU_broad_validation_failure_inputs.md"
SELECTED_STATUS = dt.SELECTED_STATUS
STAGE_BRIEF = dt.STAGE_BRIEF
WORKSPACE_STATE = dt.WORKSPACE_STATE
CURRENT_STATE = dt.CURRENT_STATE
CHANGELOG = dt.CHANGELOG
RUN_REGISTRY = dt.RUN_REGISTRY
ALPHA_LEDGER = dt.ALPHA_LEDGER
ARTIFACT_REGISTRY = dt.ARTIFACT_REGISTRY
STAGE_LEDGER = dt.STAGE_LEDGER

DT_FINAL = dt.FINAL_DECISION
DT_GATES = dt.REQUIRED_GATE_AUDIT
DT_QUEUE = dt.DU_QUEUE
DT_BROAD_DESIGN = dt.BROAD_VALIDATION_REPAIR_DESIGN
DT_CONTROL_DESIGN = dt.SHIFTED_CONTROL_REPAIR_DESIGN
DT_FAMILY_CONSTRAINTS = dt.FAMILY_SCOPE_CONSTRAINT_DESIGN
DT_FIREWALL = dt.NO_RELEASE_FIREWALL_DESIGN
DO_MODEL_MANIFEST = do.TRAINED_MODEL_MANIFEST
DO_ONNX_PARITY = do.ONNX_PARITY
SOURCE_MODEL_INPUT = do.SOURCE_MODEL_INPUT
VALIDATION_EDGE_FRAME = do.VALIDATION_EDGE_FRAME

ALL_SPLIT_PREDICTION_TAPE = RUN_DIR / "all_split_prediction_tape.parquet"
TRANSFER_MATRIX = RUN_DIR / "train_validation_transfer_matrix.csv"
DENSITY_DRAWDOWN_MATRIX = RUN_DIR / "density_drawdown_pressure_matrix.csv"
CONTROL_ISOLATION_MATRIX = RUN_DIR / "shifted_control_residual_isolation_matrix.csv"
FAMILY_SCOPE_MATRIX = RUN_DIR / "family_scope_constraint_matrix.csv"
FAILURE_MEMORY_UPDATE = RUN_DIR / "failure_memory_update.csv"
NO_RELEASE_FIREWALL_CARRY = RUN_DIR / "no_release_firewall_carry.csv"
DV_QUEUE = RUN_DIR / "run337DV_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DT_FINAL,
    DT_GATES,
    DT_QUEUE,
    DT_BROAD_DESIGN,
    DT_CONTROL_DESIGN,
    DT_FAMILY_CONSTRAINTS,
    DT_FIREWALL,
    DO_MODEL_MANIFEST,
    DO_ONNX_PARITY,
    SOURCE_MODEL_INPUT,
    VALIDATION_EDGE_FRAME,
)
OUTPUT_FILES = (
    ALL_SPLIT_PREDICTION_TAPE,
    TRANSFER_MATRIX,
    DENSITY_DRAWDOWN_MATRIX,
    CONTROL_ISOLATION_MATRIX,
    FAMILY_SCOPE_MATRIX,
    FAILURE_MEMORY_UPDATE,
    NO_RELEASE_FIREWALL_CARRY,
    DV_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

TRANSFER_COLUMNS = (
    "model_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "train_pf",
    "validation_pf",
    "oos_pf",
    "train_net",
    "validation_net",
    "oos_net",
    "train_trade_count",
    "validation_trade_count",
    "oos_trade_count",
    "validation_minus_train_pf",
    "oos_minus_validation_pf",
    "transfer_status",
    "effect",
    "claim_boundary",
)
DENSITY_COLUMNS = (
    "model_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "split",
    "rows",
    "trade_count",
    "signal_density",
    "net_log_return_after_cost",
    "profit_factor",
    "max_drawdown",
    "recovery_factor",
    "long_count",
    "short_count",
    "max_underwater_trade_stretch",
    "pressure_status",
    "effect",
    "claim_boundary",
)
CONTROL_COLUMNS = (
    "model_id",
    "task_id",
    "split",
    "control_id",
    "rows",
    "candidate_balanced_accuracy",
    "control_alignment_balanced_accuracy",
    "blocks_review",
    "isolation_status",
    "effect",
    "claim_boundary",
)
FAMILY_COLUMNS = (
    "constraint_id",
    "scope_axis",
    "observed_status",
    "constraint_rule",
    "materialized_status",
    "supporting_rows",
    "effect",
    "claim_boundary",
)
MEMORY_COLUMNS = (
    "memory_id",
    "source_evidence",
    "failure_signature",
    "severity",
    "future_block_rule",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "blocked_action_or_claim",
    "blocked_reason",
    "carry_status",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")

LABEL_ORDER = do.LABEL_ORDER
LABEL_TO_INT = do.LABEL_TO_INT
INT_TO_LABEL = do.INT_TO_LABEL


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def max_drawdown(values: np.ndarray) -> float:
    if len(values) == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    return float(np.max(peak - curve))


def max_underwater_stretch(values: np.ndarray) -> int:
    if len(values) == 0:
        return 0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    underwater = curve < peak
    max_run = 0
    current = 0
    for flag in underwater:
        if bool(flag):
            current += 1
            max_run = max(max_run, current)
        else:
            current = 0
    return max_run


def profit_factor(values: np.ndarray) -> float:
    positive = float(values[values > 0].sum())
    negative = abs(float(values[values < 0].sum()))
    if negative == 0:
        return 999.0 if positive > 0 else 0.0
    return positive / negative


def load_source_and_models() -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, dict[str, Any]], pd.DataFrame]:
    source = do.read_source_frame()
    feature_sets, _ = do.read_feature_sets(source)
    _, targets = do.read_targets()
    target_by_cost = {target["cost_policy_id"]: target for target in targets}
    manifest = pd.read_csv(io_path(DO_MODEL_MANIFEST))
    return source, feature_sets, target_by_cost, manifest


def materialize_all_split_tape() -> tuple[pd.DataFrame, dict[str, int]]:
    source, feature_sets, target_by_cost, manifest = load_source_and_models()
    feature_by_id = {row["feature_set_id"]: row for row in feature_sets}
    base = source[["source_row_id", "timestamp", "split"]].copy()
    base["timestamp"] = pd.to_datetime(base["timestamp"], utc=True)
    frames: list[pd.DataFrame] = []
    x_cache: dict[str, np.ndarray] = {}
    all_idx = np.arange(len(source), dtype=np.int64)
    for model_row in manifest.to_dict("records"):
        model_path = ROOT / str(model_row["model_path"])
        model = joblib.load(io_path(model_path))
        feature_set_id = str(model_row["feature_set_id"])
        cost_policy_id = str(model_row["cost_policy_id"])
        features = feature_by_id[feature_set_id]["features"]
        if feature_set_id not in x_cache:
            x_cache[feature_set_id] = source.loc[:, features].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float64)
        X = x_cache[feature_set_id]
        probs = ordered_sklearn_probabilities(model, X, class_order=LABEL_ORDER)
        pred = np.asarray(LABEL_ORDER, dtype=np.int64)[probs.argmax(axis=1)]
        target = target_by_cost[cost_policy_id]
        future_returns = target["future_returns"][all_idx]
        cost_returns = target["cost_returns"][all_idx]
        y_true = target["y"][all_idx]
        direction = np.where(pred == LABEL_TO_INT["long"], 1.0, np.where(pred == LABEL_TO_INT["short"], -1.0, 0.0))
        is_trade = direction != 0
        pnl = np.where(is_trade, direction * future_returns - cost_returns, 0.0)
        frame = base.copy()
        frame["model_id"] = str(model_row["model_id"])
        frame["task_id"] = str(model_row["task_id"])
        frame["target_id"] = str(model_row["target_id"])
        frame["cost_policy_id"] = cost_policy_id
        frame["feature_set_id"] = feature_set_id
        frame["model_config_id"] = str(model_row["model_config_id"])
        frame["true_label"] = y_true.astype(np.int64)
        frame["pred_label"] = pred.astype(np.int64)
        frame["pred_name"] = [INT_TO_LABEL[int(value)] for value in pred]
        frame["prob_short"] = probs[:, 0]
        frame["prob_flat"] = probs[:, 1]
        frame["prob_long"] = probs[:, 2]
        frame["future_log_return_12"] = future_returns
        frame["cost_return"] = cost_returns
        frame["direction"] = direction
        frame["is_trade"] = is_trade
        frame["pnl_after_cost"] = pnl
        frames.append(frame)
    tape = pd.concat(frames, ignore_index=True)
    io_path(ALL_SPLIT_PREDICTION_TAPE).parent.mkdir(parents=True, exist_ok=True)
    tape.to_parquet(io_path(ALL_SPLIT_PREDICTION_TAPE), index=False)
    return tape, {
        "source_rows": len(source),
        "model_rows": len(manifest),
        "tape_rows": len(tape),
        "expected_tape_rows": len(source) * len(manifest),
    }


def summarize_trade(group: pd.DataFrame) -> dict[str, Any]:
    trade = group.loc[group["is_trade"].astype(bool)]
    values = trade["pnl_after_cost"].to_numpy(dtype=float)
    net = float(values.sum()) if len(values) else 0.0
    dd = max_drawdown(values)
    return {
        "rows": len(group),
        "trade_count": len(trade),
        "signal_density": float(len(trade) / len(group)) if len(group) else 0.0,
        "net_log_return_after_cost": net,
        "profit_factor": profit_factor(values),
        "max_drawdown": dd,
        "recovery_factor": (net / dd) if dd > 0 else (999.0 if net > 0 else 0.0),
        "long_count": int((group["pred_label"] == LABEL_TO_INT["long"]).sum()),
        "short_count": int((group["pred_label"] == LABEL_TO_INT["short"]).sum()),
        "max_underwater_trade_stretch": max_underwater_stretch(values),
    }


def build_density_rows(tape: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (model_id, split), group in tape.groupby(["model_id", "split"], dropna=False):
        first = group.iloc[0].to_dict()
        summary = summarize_trade(group)
        status_parts: list[str] = []
        if split == "validation" and summary["profit_factor"] < 1.05:
            status_parts.append("validation_pf_pressure")
        if summary["signal_density"] > 0.55:
            status_parts.append("high_density_pressure")
        if summary["max_drawdown"] > abs(summary["net_log_return_after_cost"]):
            status_parts.append("drawdown_dominates_net")
        rows.append(
            {
                "model_id": model_id,
                "cost_policy_id": first.get("cost_policy_id", ""),
                "feature_set_id": first.get("feature_set_id", ""),
                "model_config_id": first.get("model_config_id", ""),
                "split": split,
                **summary,
                "pressure_status": ";".join(status_parts) if status_parts else "diagnostic_only",
                "effect": "materializes density and drawdown pressure(밀도와 드로다운 압력 물질화)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def row_by_split(rows: Sequence[Mapping[str, Any]], model_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row["model_id"] == model_id and row["split"] == split:
            return row
    return {}


def build_transfer_rows(density_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    model_ids = sorted({str(row["model_id"]) for row in density_rows})
    rows: list[dict[str, Any]] = []
    for model_id in model_ids:
        train = row_by_split(density_rows, model_id, "train")
        validation = row_by_split(density_rows, model_id, "validation")
        oos = row_by_split(density_rows, model_id, "oos")
        train_pf = as_float(train.get("profit_factor"))
        val_pf = as_float(validation.get("profit_factor"))
        oos_pf = as_float(oos.get("profit_factor"))
        statuses: list[str] = []
        if train_pf >= 1.05 and val_pf < 1.05:
            statuses.append("train_validation_transfer_break")
        if oos_pf >= 1.10 and val_pf < 1.05:
            statuses.append("oos_only_lift_reconfirmed")
        if val_pf < 1.05:
            statuses.append("validation_floor_block")
        rows.append(
            {
                "model_id": model_id,
                "cost_policy_id": validation.get("cost_policy_id", train.get("cost_policy_id", "")),
                "feature_set_id": validation.get("feature_set_id", train.get("feature_set_id", "")),
                "model_config_id": validation.get("model_config_id", train.get("model_config_id", "")),
                "train_pf": train_pf,
                "validation_pf": val_pf,
                "oos_pf": oos_pf,
                "train_net": as_float(train.get("net_log_return_after_cost")),
                "validation_net": as_float(validation.get("net_log_return_after_cost")),
                "oos_net": as_float(oos.get("net_log_return_after_cost")),
                "train_trade_count": as_int(train.get("trade_count")),
                "validation_trade_count": as_int(validation.get("trade_count")),
                "oos_trade_count": as_int(oos.get("trade_count")),
                "validation_minus_train_pf": val_pf - train_pf,
                "oos_minus_validation_pf": oos_pf - val_pf,
                "transfer_status": ";".join(statuses) if statuses else "diagnostic_only",
                "effect": "materializes split transfer failure(분할 전이 실패 물질화)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_control_rows(tape: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (model_id, task_id, split), group in tape.groupby(["model_id", "task_id", "split"], dropna=False):
        pred = group["pred_label"].to_numpy(dtype=np.int64)
        true = group["true_label"].to_numpy(dtype=np.int64)
        source_ids = group["source_row_id"].to_numpy(dtype=np.int64)
        candidate_balanced = do.safe_balanced(true, pred)
        for control_id in ("shifted_return_control", "noise_label_control", "block_shuffle_control"):
            y_control = do.control_labels(control_id, true, source_ids)
            alignment = do.safe_balanced(y_control, pred)
            blocks = split == "validation" and alignment >= max(0.45, candidate_balanced - 0.02)
            rows.append(
                {
                    "model_id": model_id,
                    "task_id": task_id,
                    "split": split,
                    "control_id": control_id,
                    "rows": len(group),
                    "candidate_balanced_accuracy": candidate_balanced,
                    "control_alignment_balanced_accuracy": alignment,
                    "blocks_review": "true" if blocks else "false",
                    "isolation_status": "blocks_release" if blocks else "diagnostic_only",
                    "effect": "isolates shifted-control residual across all splits(전체 분할 이동 대조 잔차 격리)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_family_rows(transfer_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    constraints = read_csv(DT_FAMILY_CONSTRAINTS)
    rows: list[dict[str, Any]] = []
    transfer_breaks = sum("train_validation_transfer_break" in str(row.get("transfer_status", "")) for row in transfer_rows)
    oos_lifts = sum("oos_only_lift_reconfirmed" in str(row.get("transfer_status", "")) for row in transfer_rows)
    for row in constraints:
        rows.append(
            {
                "constraint_id": row.get("constraint_id", ""),
                "scope_axis": row.get("scope_axis", ""),
                "observed_status": row.get("observed_status", ""),
                "constraint_rule": row.get("constraint_rule", ""),
                "materialized_status": "carried_forward_with_transfer_context",
                "supporting_rows": f"transfer_breaks={transfer_breaks};oos_lifts={oos_lifts}",
                "effect": "keeps family constraints active after DU materialization(DU 물질화 후 계열 제약 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_failure_memory(transfer_rows: Sequence[Mapping[str, Any]], density_rows: Sequence[Mapping[str, Any]], control_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    transfer_breaks = sum("train_validation_transfer_break" in str(row.get("transfer_status", "")) for row in transfer_rows)
    oos_lifts = sum("oos_only_lift_reconfirmed" in str(row.get("transfer_status", "")) for row in transfer_rows)
    high_density = sum("high_density_pressure" in str(row.get("pressure_status", "")) and row.get("split") == "validation" for row in density_rows)
    control_blocks = sum(str(row.get("blocks_review", "")).lower() == "true" for row in control_rows)
    family_constraints = read_csv(DT_FAMILY_CONSTRAINTS)
    broad_family_axes = [
        row.get("scope_axis", "")
        for row in family_constraints
        if "broad_validation_failure" in str(row.get("observed_status", ""))
    ]
    control_design = read_csv(DT_CONTROL_DESIGN)
    shifted_scope = ";".join(
        str(row.get("affected_scope", ""))
        for row in control_design
        if row.get("design_id") == "technical_extratrees_shifted_residual_isolation"
    )
    broad_design = read_csv(DT_BROAD_DESIGN)
    wfo_contracts = sum(row.get("design_id") == "wfo_precheck_contract" for row in broad_design)
    return [
        {
            "memory_id": "broad_validation_failure_reconfirmed",
            "source_evidence": rel(TRANSFER_MATRIX),
            "failure_signature": f"validation_floor_blocks={sum('validation_floor_block' in str(row.get('transfer_status', '')) for row in transfer_rows)}",
            "severity": "high",
            "future_block_rule": "no candidate selection until repaired validation review passes(수리 검증 리뷰 통과 전 후보 선택 금지)",
            "allowed_use": "repair design and diagnostics(수리 설계와 진단)",
            "forbidden_use": "release or MT5 queue(해제 또는 MT5 대기열)",
            "effect": "preserves broad validation failure memory(넓은 검증 실패 기억 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "train_validation_transfer_break",
            "source_evidence": rel(TRANSFER_MATRIX),
            "failure_signature": f"transfer_breaks={transfer_breaks}",
            "severity": "high" if transfer_breaks else "watch",
            "future_block_rule": "new training must include transfer checks(새 학습은 전이 점검 포함)",
            "allowed_use": "future training prerequisite(미래 학습 전제)",
            "forbidden_use": "post-hoc validation filter(사후 검증 필터)",
            "effect": "separates train fit from validation support(학습 적합과 검증 지지 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "oos_only_lift_reconfirmed",
            "source_evidence": rel(TRANSFER_MATRIX),
            "failure_signature": f"oos_lifts={oos_lifts}",
            "severity": "medium",
            "future_block_rule": "OOS lift cannot enter shortlist without validation repair(OOS 개선은 검증 수리 없이는 후보 목록 금지)",
            "allowed_use": "regime clue(레짐 단서)",
            "forbidden_use": "winner selection(승자 선택)",
            "effect": "keeps OOS lift from overfit pressure(OOS 개선 과적합 압력 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "density_drawdown_pressure",
            "source_evidence": rel(DENSITY_DRAWDOWN_MATRIX),
            "failure_signature": f"validation_high_density_rows={high_density}",
            "severity": "medium",
            "future_block_rule": "future action policy must report density/drawdown(미래 행동 정책은 밀도/드로다운 보고 필수)",
            "allowed_use": "diagnostic pressure(진단 압력)",
            "forbidden_use": "density threshold tuning(밀도 임계값 튜닝)",
            "effect": "names action overbreadth risk(행동 과다 위험 명명)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "shifted_control_residual_reconfirmed",
            "source_evidence": rel(CONTROL_ISOLATION_MATRIX),
            "failure_signature": f"control_blocks={control_blocks}",
            "severity": "high" if control_blocks else "watch",
            "future_block_rule": "shifted-control block prevents runtime probe(이동 대조 차단은 런타임 탐침 차단)",
            "allowed_use": "control repair(대조 수리)",
            "forbidden_use": "control relaxation(대조 완화)",
            "effect": "preserves overfit guard(과적합 방어 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "family_axis_broad_failure_constraint",
            "source_evidence": rel(FAMILY_SCOPE_MATRIX),
            "failure_signature": f"broad_family_axes={','.join(axis for axis in broad_family_axes if axis)}",
            "severity": "high",
            "future_block_rule": "future packets must not reuse broad failed axes as selection shortcuts(미래 묶음은 넓게 실패한 축을 선택 지름길로 재사용 금지)",
            "allowed_use": "family-scope repair constraint(계열 범위 수리 제약)",
            "forbidden_use": "axis-level winner claim(축 단위 승자 주장)",
            "effect": "keeps broad-axis failure from becoming another overfit selector(넓은 축 실패가 또 다른 과적합 선택자가 되는 것 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "technical_extratrees_shifted_residual",
            "source_evidence": rel(DT_CONTROL_DESIGN),
            "failure_signature": f"affected_scope={shifted_scope or 'not_found'}",
            "severity": "high",
            "future_block_rule": "technical ExtraTrees lineage needs shifted-control isolation before runtime queue(technical ExtraTrees 계열은 런타임 대기 전 이동 대조 격리 필요)",
            "allowed_use": "serial residual isolation design(연속 잔차 격리 설계)",
            "forbidden_use": "treat shifted residual as harmless noise(이동 잔차를 무해한 잡음으로 취급)",
            "effect": "keeps the known shifted-control blocker explicit(알려진 이동 대조 차단을 명시 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "wfo_precheck_single_split_risk",
            "source_evidence": rel(DT_BROAD_DESIGN),
            "failure_signature": f"wfo_precheck_contracts={wfo_contracts};single_split_review_insufficient=true",
            "severity": "medium",
            "future_block_rule": "future ONNX packet must expose WFO or embargo feasibility before stronger claims(미래 ONNX 묶음은 강한 주장 전 WFO 또는 embargo 가능성 노출 필요)",
            "allowed_use": "forward robustness prerequisite(전진 강건성 전제)",
            "forbidden_use": "retrofit WFO after model choice(모델 선택 후 WFO 사후 끼워넣기)",
            "effect": "prevents single-split evidence from becoming readiness language(단일 분할 근거가 준비성 언어가 되는 것 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_firewall_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(DT_FIREWALL):
        rows.append(
            {
                "firewall_id": row.get("firewall_id", ""),
                "blocked_action_or_claim": row.get("blocked_action_or_claim", ""),
                "blocked_reason": row.get("blocked_reason", ""),
                "carry_status": "carried_forward_no_release",
                "effect": "preserves no-release boundary(무해제 경계 보존)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_dv_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DV_review_transfer_breaks",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review train-validation transfer breaks(학습-검증 전이 단절 검토)",
            "required_inputs": rel(TRANSFER_MATRIX),
            "required_outputs": "transfer_break_review.csv",
            "blocked_if_missing": "transfer matrix(전이 행렬)",
            "forbidden_action": "no model selection from transfer matrix(전이 행렬로 모델 선택 금지)",
            "effect": "judges whether current surface overfits train(현재 표면의 학습 과적합 여부 판정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DV_review_density_drawdown_pressure",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review density/drawdown pressure(밀도/드로다운 압력 검토)",
            "required_inputs": rel(DENSITY_DRAWDOWN_MATRIX),
            "required_outputs": "density_drawdown_pressure_review.csv",
            "blocked_if_missing": "density/drawdown matrix(밀도/드로다운 행렬)",
            "forbidden_action": "no threshold tuning(임계값 튜닝 금지)",
            "effect": "tests action overbreadth hypothesis(행동 과다 가설 검토)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DV_review_control_isolation",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review shifted-control isolation(이동 대조 격리 검토)",
            "required_inputs": rel(CONTROL_ISOLATION_MATRIX),
            "required_outputs": "control_isolation_review.csv",
            "blocked_if_missing": "control isolation matrix(대조 격리 행렬)",
            "forbidden_action": "no control threshold relaxation(대조 임계값 완화 금지)",
            "effect": "judges serial residual blocker(연속 잔차 차단 판정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DV_review_family_memory_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "review family constraints, failure memory, firewall(계열 제약/실패 기억/방화벽 검토)",
            "required_inputs": f"{rel(FAMILY_SCOPE_MATRIX)};{rel(FAILURE_MEMORY_UPDATE)};{rel(NO_RELEASE_FIREWALL_CARRY)}",
            "required_outputs": "family_memory_firewall_review.csv",
            "blocked_if_missing": "family/memory/firewall outputs(계열/기억/방화벽 출력)",
            "forbidden_action": "no MT5/Forward claim(MT5/전진 주장 금지)",
            "effect": "keeps repair evidence bounded(수리 근거 경계 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DV_review_wfo_objective_precheck",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "review WFO/objective precheck before any repair training(WFO/목표 사전검사를 수리 학습 전 검토)",
            "required_inputs": f"{rel(DT_BROAD_DESIGN)};{rel(FAILURE_MEMORY_UPDATE)}",
            "required_outputs": "wfo_objective_precheck_review.csv",
            "blocked_if_missing": "DT broad design or DU failure memory(DT 넓은 설계 또는 DU 실패 기억)",
            "forbidden_action": "no single-split release or objective retune(단일 분할 해제 또는 목표 재튜닝 금지)",
            "effect": "keeps future repair training from becoming repair-overfit(미래 수리 학습이 수리 과적합이 되는 것 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DT/DO inputs exist(필수 DT/DO 입력 존재)"),
        ("parent_dt_gates_passed", final["dt_failed_gate_rows"] == 0, str(final["dt_failed_gate_rows"]), "0", "DT design usable(DT 설계 사용 가능)"),
        ("parent_next_action_matches", final["dt_next_action"] == RUN_ID, str(final["dt_next_action"]), RUN_ID, "continues DT queue(DT 대기열을 이어감)"),
        ("all_split_tape_complete", final["all_split_tape_rows"] == final["expected_all_split_tape_rows"], f"{final['all_split_tape_rows']}/{final['expected_all_split_tape_rows']}", "all", "all split predictions materialized(전체 분할 예측 물질화)"),
        ("transfer_rows_materialized", final["transfer_rows"] == 18, str(final["transfer_rows"]), "18", "transfer rows per model(모델별 전이 행 존재)"),
        ("density_rows_materialized", final["density_rows"] == 54, str(final["density_rows"]), "54", "density rows per model/split(모델/분할별 밀도 행 존재)"),
        ("control_rows_materialized", final["control_rows"] == 162, str(final["control_rows"]), "162", "controls scored for train/validation/OOS(학습/검증/OOS 대조 점수화)"),
        ("failure_memory_materialized", final["failure_memory_rows"] >= 7, str(final["failure_memory_rows"]), ">=7", "failure memory updated(실패 기억 업데이트)"),
        ("firewall_carried", final["firewall_rows"] >= 4, str(final["firewall_rows"]), ">=4", "no-release firewall carried(무해제 방화벽 전달)"),
        ("dv_queue_materialized", final["dv_queue_rows"] == 5, str(final["dv_queue_rows"]), "5", "DV review queue opened(DV 검토 대기열 열림)"),
        (
            "no_forbidden_claim",
            final["model_training"] == "not_run"
            and final["candidate_selection"] == "not_run"
            and final["mt5_runtime_probe"] == "not_run"
            and final["goal_achieve"] == "not_claimed",
            f"training={final['model_training']};selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            "claim boundary preserved(주장 경계 보존)",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "source_row_id UTC rows across train/validation/OOS(source_row_id UTC 행, 학습/검증/OOS 전체)",
        "sample_scope": f"all_split_tape_rows={final['all_split_tape_rows']};model_rows={final['model_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']};expected_rows={final['expected_all_split_tape_rows']}",
        "feature_label_boundary": "no new labels; existing DO labels reused for scoring only(새 라벨 없음, 기존 DO 라벨 점수화 전용 재사용)",
        "split_boundary": "train scored for transfer only, not fitted(학습은 전이 확인용 점수화만, 적합 아님)",
        "leakage_risk": "using transfer results to tune thresholds(전이 결과로 임계값 조정하는 위험)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_review_no_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "existing DO trained artifacts scored across all splits(기존 DO 학습 산출물 전체 분할 점수화)",
        "target_and_label": "unchanged costed action labels(비용 반영 행동 라벨 유지)",
        "split_method": "no fitting; train/validation/OOS scoring only(적합 없음, 학습/검증/OOS 점수화만)",
        "selection_metric": "none; all models materialized(없음, 전체 모델 물질화)",
        "secondary_metrics": "transfer PF, density, drawdown, controls, failure memory(전이 PF/밀도/드로다운/대조/실패 기억)",
        "threshold_policy": "no threshold tuning(임계값 튜닝 없음)",
        "overfit_risk": "using train/validation transfer as selection(학습/검증 전이를 선택에 쓰는 위험)",
        "calibration_risk": "probabilities diagnostic only(확률은 진단 전용)",
        "comparison_baseline": rel(DT_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"transfer_break_rows={final['transfer_break_rows']};control_block_rows={final['control_block_rows']};high_density_validation_rows={final['high_density_validation_rows']}",
        "comparison_baseline": rel(DT_FINAL),
        "likely_drivers": "train-validation transfer, high action density, shifted-control residual(학습-검증 전이/높은 행동 밀도/이동 대조 잔차)",
        "segment_checks": f"density_rows={final['density_rows']};control_rows={final['control_rows']}",
        "trade_shape": f"all_split_tape_rows={final['all_split_tape_rows']}",
        "alternative_explanations": "regime drift, proxy cost mismatch, target/action mismatch(레짐 드리프트/프록시 비용 불일치/목표 행동 불일치)",
        "attribution_confidence": "materialized_for_DV_review(DV 검토용 물질화)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "transfer, density/drawdown, control, family, failure memory, firewall(전이/밀도 드로다운/대조/계열/실패 기억/방화벽)",
        "evidence_missing": "DV review, repair training, MT5, forward evidence(DV 검토/수리 학습/MT5/전진 근거)",
        "judgment_label": "materialized_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "이제 학습-검증 전이와 밀도/대조 압력을 실제 행렬로 볼 수 있다. 아직 고르는 단계는 아니다.",
    }
    paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in list(artifact_paths) + paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_materialization_outputs_with_tracked_report(무시된 물질화 산출물과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DU Broad Validation Failure Inputs(넓은 검증 실패 입력)

## Conclusion(결론)

run337DU(337DU 실행)는 run337DT(337DT 실행)의 설계를 train-validation transfer(학습-검증 전이), density/drawdown pressure(밀도/드로다운 압력), shifted-control isolation(이동 대조 격리), family constraints(계열 제약), failure memory(실패 기억) 입력으로 물질화했다.

이 작업은 materialization-only(물질화 전용)이다. 새 학습, 후보 선택, 임계값 튜닝, MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 하지 않는다.

Effect(효과): run337DV(337DV 실행)는 current surface(현재 표면)가 train-fit overreach(학습 적합 과다), action density pressure(행동 밀도 압력), control residual(대조 잔차) 중 무엇에 가까운지 검토한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- all_split_tape_rows(전체 분할 테이프 행): `{final["all_split_tape_rows"]}`
- transfer_rows(전이 행): `{final["transfer_rows"]}`
- transfer_break_rows(전이 단절 행): `{final["transfer_break_rows"]}`
- density_rows(밀도 행): `{final["density_rows"]}`
- high_density_validation_rows(검증 고밀도 행): `{final["high_density_validation_rows"]}`
- control_block_rows(대조 차단 행): `{final["control_block_rows"]}`
- failure_memory_rows(실패 기억 행): `{final["failure_memory_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DU

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 전이/밀도/대조 수리 입력을 만들었지만 선택/MT5/Forward(전진)는 계속 닫는다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(TRANSFER_MATRIX)}`, `{rel(DENSITY_DRAWDOWN_MATRIX)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337DU focus complete: broad validation failure/control residual inputs(넓은 검증 실패/대조 잔차 입력)을 `{STATUS}`로 물질화했다. "
        f"Effect(효과): run337DV(337DV 실행)에서 train-validation transfer/density/control isolation(학습-검증 전이/밀도/대조 격리)을 검토한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DU focus complete")
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{STATUS}`",
        "decision": f"`{DECISION}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""## Stage337 run337DU(337DU 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 전이/밀도/대조 입력을 만들었지만 선택/MT5/Forward(전진)는 주장하지 않는다. Goal(목표)은 주장하지 않는다."""
    current_text = append_once(current_text, section, "Stage337 run337DU(337DU 실행)")
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection_text, _ = read_text_lossless(SELECTED_STATUS)
    selection = selection_text
    for field_name, value in {
        "latest_run": f"`{RUN_ID}`",
        "latest_decision": f"`{DECISION}`",
        "current_run": f"`{NEXT_RUN_ID}`",
        "rebuild_status": f"`{STATUS}`",
        "actual_mt5_execution": "`not_run_du_materialization_only`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "effect": "`다음은 transfer/density/control materialization review(전이/밀도/대조 물질화 검토)다.`",
    }.items():
        selection = replace_bullet_value(selection, field_name, value)
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337DU(337DU 실행) materialized broad validation failure/control residual repair inputs and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DU(337DU 실행) materialized broad validation failure"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337DU materialized broad validation failure/control residual repair inputs and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DU materialized broad validation failure"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "broad_validation_failure_control_residual_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"transfer_breaks={final['transfer_break_rows']};density_rows={final['density_rows']};control_blocks={final['control_block_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__broad_failure_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "broad_failure_input_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization_no_training_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "proxy_transfer_density_control_materialization",
        "scoreboard_lane": "data_integrity_model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"transfer_breaks={final['transfer_break_rows']};control_blocks={final['control_block_rows']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__broad_failure_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_performance_attribution_result_judgment",
        "evidence_scope": "broad failure repair inputs materialized",
        "kpi_scope": "transfer_density_control_failure_memory",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__broad_failure_input_materialization",
        "family": "data_integrity_model_validation_performance_attribution_result_judgment",
        "question": "does broad validation failure show train-transfer, density, or control pressure",
        "metric_scope": "transfer_breaks_density_control_blocks",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    artifacts = [
        upsert_csv(RUN_REGISTRY, "run_id", run_row),
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row),
        upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row),
    ]
    artifact_columns: list[str] = []
    artifact_rows: list[dict[str, str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            artifact_columns = list(reader.fieldnames or [])
            artifact_rows = [dict(row) for row in reader]
    if not artifact_columns:
        artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    tape, tape_summary = materialize_all_split_tape()
    density_rows = build_density_rows(tape)
    transfer_rows = build_transfer_rows(density_rows)
    control_rows = build_control_rows(tape)
    family_rows = build_family_rows(transfer_rows)
    failure_memory_rows = build_failure_memory(transfer_rows, density_rows, control_rows)
    firewall_rows = build_firewall_rows()
    queue_rows = build_dv_queue()

    dt_final = read_json(DT_FINAL)
    dt_failed_gate_rows = sum(1 for row in read_csv(DT_GATES) if row.get("status") != "passed")
    transfer_break_rows = sum("train_validation_transfer_break" in str(row["transfer_status"]) for row in transfer_rows)
    high_density_validation_rows = sum(
        row["split"] == "validation" and "high_density_pressure" in str(row["pressure_status"])
        for row in density_rows
    )
    control_block_rows = sum(str(row["blocks_review"]).lower() == "true" for row in control_rows)
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dt_next_action": dt_final.get("next_action", ""),
        "dt_failed_gate_rows": dt_failed_gate_rows,
        "missing_inputs": len(missing),
        "model_rows": int(tape_summary["model_rows"]),
        "source_rows": int(tape_summary["source_rows"]),
        "all_split_tape_rows": int(tape_summary["tape_rows"]),
        "expected_all_split_tape_rows": int(tape_summary["expected_tape_rows"]),
        "transfer_rows": len(transfer_rows),
        "transfer_break_rows": int(transfer_break_rows),
        "density_rows": len(density_rows),
        "high_density_validation_rows": int(high_density_validation_rows),
        "control_rows": len(control_rows),
        "control_block_rows": int(control_block_rows),
        "family_constraint_rows": len(family_rows),
        "failure_memory_rows": len(failure_memory_rows),
        "firewall_rows": len(firewall_rows),
        "dv_queue_rows": len(queue_rows),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts: list[Path] = [
        ALL_SPLIT_PREDICTION_TAPE,
        write_csv(TRANSFER_MATRIX, TRANSFER_COLUMNS, transfer_rows),
        write_csv(DENSITY_DRAWDOWN_MATRIX, DENSITY_COLUMNS, density_rows),
        write_csv(CONTROL_ISOLATION_MATRIX, CONTROL_COLUMNS, control_rows),
        write_csv(FAMILY_SCOPE_MATRIX, FAMILY_COLUMNS, family_rows),
        write_csv(FAILURE_MEMORY_UPDATE, MEMORY_COLUMNS, failure_memory_rows),
        write_csv(NO_RELEASE_FIREWALL_CARRY, FIREWALL_COLUMNS, firewall_rows),
        write_csv(DV_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(
            RUN_MANIFEST,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "inputs": [rel(path) for path in INPUT_FILES],
                "outputs": [rel(path) for path in OUTPUT_FILES],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
