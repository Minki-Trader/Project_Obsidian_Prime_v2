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
from stage_pipelines.stage337 import design_validation_support_control_residual_repair as dq  # noqa: E402
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
STAGE_ID = dq.STAGE_ID
RUN_NUMBER = "run337DR"
RUN_ID = "run337DR_materialize_validation_support_control_residual_repair_inputs_without_db_v1"
PARENT_RUN_ID = dq.RUN_ID
NEXT_RUN_ID = "run337DS_review_validation_support_control_residual_materialization_without_db_v1"
STATUS = "completed_stage337DR_validation_support_control_residual_inputs_materialized_no_training_no_selection"
JUDGMENT = "row_level_prediction_control_quarantine_tapes_materialized_review_required"
DECISION = "stage337DR_open_run337DS_review_validation_support_control_residual_materialization"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DR_validation_support_control_residual_input_materialization_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dq.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dq.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DR_repair_input_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DR_repair_input_materialization.md"
SELECTED_STATUS = dq.SELECTED_STATUS
STAGE_BRIEF = dq.STAGE_BRIEF
WORKSPACE_STATE = dq.WORKSPACE_STATE
CURRENT_STATE = dq.CURRENT_STATE
CHANGELOG = dq.CHANGELOG
RUN_REGISTRY = dq.RUN_REGISTRY
ALPHA_LEDGER = dq.ALPHA_LEDGER
ARTIFACT_REGISTRY = dq.ARTIFACT_REGISTRY
STAGE_LEDGER = dq.STAGE_LEDGER

DQ_FINAL = dq.FINAL_DECISION
DQ_GATES = dq.REQUIRED_GATE_AUDIT
DQ_QUEUE = dq.DR_QUEUE
DQ_VALIDATION_DESIGN = dq.VALIDATION_SUPPORT_DESIGN
DQ_CONTROL_DESIGN = dq.CONTROL_RESIDUAL_DESIGN
DQ_QUARANTINE = dq.OOS_ONLY_QUARANTINE
DQ_FIREWALL = dq.RUNTIME_FIREWALL_DESIGN
DQ_TAPE_CONTRACT = dq.ROW_LEVEL_TAPE_CONTRACT
DO_MODEL_MANIFEST = do.TRAINED_MODEL_MANIFEST
DO_ONNX_PARITY = do.ONNX_PARITY
SOURCE_MODEL_INPUT = do.SOURCE_MODEL_INPUT
VALIDATION_EDGE_FRAME = do.VALIDATION_EDGE_FRAME

ALL_MODEL_PREDICTION_TAPE = RUN_DIR / "all_model_prediction_tape.parquet"
VALIDATION_CURVE_POCKET_SLICES = RUN_DIR / "validation_curve_pocket_slices.csv"
SHIFTED_CONTROL_RESIDUAL_TAPE = RUN_DIR / "shifted_control_residual_tape.csv"
OOS_QUARANTINE_LEDGER = RUN_DIR / "oos_only_lift_quarantine_ledger.csv"
RUNTIME_FIREWALL_CARRY = RUN_DIR / "runtime_firewall_carry.csv"
MATERIALIZATION_SUMMARY = RUN_DIR / "materialization_summary.csv"
DS_QUEUE = RUN_DIR / "run337DS_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DQ_FINAL,
    DQ_GATES,
    DQ_QUEUE,
    DQ_VALIDATION_DESIGN,
    DQ_CONTROL_DESIGN,
    DQ_QUARANTINE,
    DQ_FIREWALL,
    DQ_TAPE_CONTRACT,
    DO_MODEL_MANIFEST,
    DO_ONNX_PARITY,
    SOURCE_MODEL_INPUT,
    VALIDATION_EDGE_FRAME,
)
OUTPUT_FILES = (
    ALL_MODEL_PREDICTION_TAPE,
    VALIDATION_CURVE_POCKET_SLICES,
    SHIFTED_CONTROL_RESIDUAL_TAPE,
    OOS_QUARANTINE_LEDGER,
    RUNTIME_FIREWALL_CARRY,
    MATERIALIZATION_SUMMARY,
    DS_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
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

SLICE_COLUMNS = (
    "slice_id",
    "model_id",
    "slice_family",
    "slice_value",
    "rows",
    "trade_count",
    "net_log_return_after_cost",
    "profit_factor",
    "expectancy",
    "max_drawdown",
    "long_count",
    "short_count",
    "slice_status",
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
    "effect",
    "claim_boundary",
)
QUARANTINE_COLUMNS = (
    "model_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "validation_pf",
    "oos_pf",
    "tape_validation_trade_count",
    "tape_oos_trade_count",
    "ledger_status",
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
SUMMARY_COLUMNS = (
    "summary_id",
    "value",
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


def profit_factor(values: np.ndarray) -> float:
    positive = float(values[values > 0].sum())
    negative = abs(float(values[values < 0].sum()))
    if negative == 0:
        return 999.0 if positive > 0 else 0.0
    return positive / negative


def safe_balanced(y_true: np.ndarray, pred: np.ndarray) -> float:
    return do.safe_balanced(y_true, pred)


def load_inputs() -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, dict[str, Any]], pd.DataFrame]:
    source = do.read_source_frame()
    feature_sets, _ = do.read_feature_sets(source)
    _, targets = do.read_targets()
    target_by_cost = {target["cost_policy_id"]: target for target in targets}
    manifest = pd.read_csv(io_path(DO_MODEL_MANIFEST))
    return source, feature_sets, target_by_cost, manifest


def materialize_prediction_tape() -> tuple[pd.DataFrame, dict[str, Any]]:
    source, feature_sets, target_by_cost, manifest = load_inputs()
    feature_by_id = {row["feature_set_id"]: row for row in feature_sets}
    split_mask = source["split"].astype(str).isin(["validation", "oos"]).to_numpy()
    split_idx = np.flatnonzero(split_mask)
    base = source.iloc[split_idx][["source_row_id", "timestamp", "split"]].copy()
    base["timestamp"] = pd.to_datetime(base["timestamp"], utc=True)
    frames: list[pd.DataFrame] = []
    x_cache: dict[str, np.ndarray] = {}

    for model_row in manifest.to_dict("records"):
        model_path = ROOT / str(model_row["model_path"])
        model = joblib.load(io_path(model_path))
        feature_set_id = str(model_row["feature_set_id"])
        cost_policy_id = str(model_row["cost_policy_id"])
        features = feature_by_id[feature_set_id]["features"]
        if feature_set_id not in x_cache:
            x_cache[feature_set_id] = source.loc[:, features].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float64)
        X = x_cache[feature_set_id][split_idx]
        probs = ordered_sklearn_probabilities(model, X, class_order=LABEL_ORDER)
        pred = np.asarray(LABEL_ORDER, dtype=np.int64)[probs.argmax(axis=1)]
        target = target_by_cost[cost_policy_id]
        future_returns = target["future_returns"][split_idx]
        cost_returns = target["cost_returns"][split_idx]
        y_true = target["y"][split_idx]
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
    tape["hour_utc"] = pd.to_datetime(tape["timestamp"], utc=True).dt.hour
    tape["month"] = pd.to_datetime(tape["timestamp"], utc=True).dt.strftime("%Y-%m")
    io_path(ALL_MODEL_PREDICTION_TAPE).parent.mkdir(parents=True, exist_ok=True)
    tape.to_parquet(io_path(ALL_MODEL_PREDICTION_TAPE), index=False)
    summary = {
        "source_rows": len(source),
        "scored_source_rows": int(split_mask.sum()),
        "model_rows": len(manifest),
        "prediction_tape_rows": len(tape),
        "expected_prediction_tape_rows": int(split_mask.sum()) * len(manifest),
    }
    return tape, summary


def summarize_slice(group: pd.DataFrame) -> dict[str, Any]:
    trade = group.loc[group["is_trade"].astype(bool)]
    values = trade["pnl_after_cost"].to_numpy(dtype=float)
    net = float(values.sum()) if len(values) else 0.0
    pf = profit_factor(values)
    return {
        "rows": len(group),
        "trade_count": len(trade),
        "net_log_return_after_cost": net,
        "profit_factor": pf,
        "expectancy": float(values.mean()) if len(values) else 0.0,
        "max_drawdown": max_drawdown(values),
        "long_count": int((group["pred_label"] == LABEL_TO_INT["long"]).sum()),
        "short_count": int((group["pred_label"] == LABEL_TO_INT["short"]).sum()),
    }


def build_validation_slices(tape: pd.DataFrame) -> list[dict[str, Any]]:
    validation = tape.loc[tape["split"].astype(str).eq("validation")].copy()
    rows: list[dict[str, Any]] = []
    slice_specs = [
        ("hour_utc", "hour"),
        ("month", "month"),
        ("cost_policy_id", "cost_policy"),
        ("feature_set_id", "feature_set"),
        ("model_config_id", "model_config"),
    ]
    for model_id, model_group in validation.groupby("model_id", dropna=False):
        for column, family in slice_specs:
            for value, group in model_group.groupby(column, dropna=False):
                summary = summarize_slice(group)
                status = "weak_validation_slice" if summary["trade_count"] > 0 and summary["profit_factor"] < 1.05 else "diagnostic_slice"
                rows.append(
                    {
                        "slice_id": f"{model_id}__{family}__{value}",
                        "model_id": model_id,
                        "slice_family": family,
                        "slice_value": str(value),
                        **summary,
                        "slice_status": status,
                        "effect": "attributes validation weakness by row slice(검증 약점을 행 슬라이스별 귀인)",
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
        candidate_balanced = safe_balanced(true, pred)
        for control_id in ("shifted_return_control", "noise_label_control", "block_shuffle_control"):
            y_control = do.control_labels(control_id, true, source_ids)
            alignment = safe_balanced(y_control, pred)
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
                    "effect": "scores row-level control residual(행 단위 대조 잔차 점수화)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_quarantine_ledger(tape: pd.DataFrame) -> list[dict[str, Any]]:
    quarantine_rows = read_csv(DQ_QUARANTINE)
    rows: list[dict[str, Any]] = []
    for row in quarantine_rows:
        model_id = row["model_id"]
        model_tape = tape.loc[tape["model_id"].astype(str).eq(model_id)]
        validation_trades = int(model_tape.loc[model_tape["split"].astype(str).eq("validation"), "is_trade"].astype(bool).sum())
        oos_trades = int(model_tape.loc[model_tape["split"].astype(str).eq("oos"), "is_trade"].astype(bool).sum())
        rows.append(
            {
                "model_id": model_id,
                "cost_policy_id": row.get("cost_policy_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "model_config_id": row.get("model_config_id", ""),
                "validation_pf": row.get("validation_pf", ""),
                "oos_pf": row.get("oos_pf", ""),
                "tape_validation_trade_count": validation_trades,
                "tape_oos_trade_count": oos_trades,
                "ledger_status": "quarantined_no_release",
                "allowed_use": "failure memory and attribution(실패 기억과 귀인)",
                "forbidden_use": "candidate selection, threshold tuning, MT5 queue(후보 선택/임계값 튜닝/MT5 대기열)",
                "effect": "keeps OOS lift out of release queue(OOS 개선을 해제 대기열 밖에 둠)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_firewall_carry() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(DQ_FIREWALL):
        rows.append(
            {
                "firewall_id": row.get("firewall_id", ""),
                "blocked_action_or_claim": row.get("blocked_action_or_claim", ""),
                "blocked_reason": row.get("blocked_reason", ""),
                "carry_status": "carried_forward_no_release",
                "effect": "preserves no MT5/Forward boundary(MT5/전진 경계 보존)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_summary_rows(final_like: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {"summary_id": key, "value": value, "effect": "materialization summary(물질화 요약)", "claim_boundary": CLAIM_BOUNDARY}
        for key, value in final_like.items()
        if key
        in {
            "prediction_tape_rows",
            "expected_prediction_tape_rows",
            "model_rows",
            "validation_slice_rows",
            "weak_validation_slice_rows",
            "control_rows",
            "control_block_rows",
            "quarantine_rows",
        }
    ]


def build_ds_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DS_review_prediction_tape_integrity",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review prediction tape integrity(예측 테이프 무결성 검토)",
            "required_inputs": rel(ALL_MODEL_PREDICTION_TAPE),
            "required_outputs": "prediction_tape_integrity_review.csv",
            "blocked_if_missing": "all-model prediction tape(전체 모델 예측 테이프)",
            "forbidden_action": "no model selection from tape(테이프에서 모델 선택 금지)",
            "effect": "checks row-level handoff before interpretation(해석 전 행 단위 인계 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DS_review_validation_curve_pockets",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review validation curve pockets(검증 곡선 포켓 검토)",
            "required_inputs": rel(VALIDATION_CURVE_POCKET_SLICES),
            "required_outputs": "validation_curve_pocket_review.csv",
            "blocked_if_missing": "validation slice attribution(검증 슬라이스 귀인)",
            "forbidden_action": "no release filter mining(해제용 필터 채굴 금지)",
            "effect": "finds where validation breaks(검증이 깨지는 위치 탐색)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DS_review_control_residuals",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review shifted-control residuals(이동 대조 잔차 검토)",
            "required_inputs": rel(SHIFTED_CONTROL_RESIDUAL_TAPE),
            "required_outputs": "control_residual_review.csv",
            "blocked_if_missing": "shifted control residual tape(이동 대조 잔차 테이프)",
            "forbidden_action": "no control threshold relaxation(대조 임계값 완화 금지)",
            "effect": "keeps overfit check active(과적합 점검 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DS_review_quarantine_and_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "review OOS quarantine and runtime firewall(OOS 격리와 런타임 방화벽 검토)",
            "required_inputs": f"{rel(OOS_QUARANTINE_LEDGER)};{rel(RUNTIME_FIREWALL_CARRY)}",
            "required_outputs": "quarantine_firewall_review.csv",
            "blocked_if_missing": "quarantine or firewall ledger(격리 또는 방화벽 장부)",
            "forbidden_action": "no MT5/Forward claim(MT5/전진 주장 금지)",
            "effect": "preserves claim boundary(주장 경계 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DQ/DO inputs exist(필수 DQ/DO 입력 존재)"),
        ("parent_dq_gates_passed", final["dq_failed_gate_rows"] == 0, str(final["dq_failed_gate_rows"]), "0", "DQ design evidence usable(DQ 설계 근거 사용 가능)"),
        ("parent_next_action_matches", final["dq_next_action"] == RUN_ID, str(final["dq_next_action"]), RUN_ID, "continues DQ queue(DQ 대기열을 이어감)"),
        ("prediction_tape_complete", final["prediction_tape_rows"] == final["expected_prediction_tape_rows"], f"{final['prediction_tape_rows']}/{final['expected_prediction_tape_rows']}", "all", "all model-row predictions materialized(전체 모델-행 예측 물질화)"),
        ("all_models_scored", final["model_rows"] == 18, str(final["model_rows"]), "18", "all DO models scored(DO 모델 전체 점수화)"),
        ("validation_slices_materialized", final["validation_slice_rows"] > 0, str(final["validation_slice_rows"]), ">0", "validation slices exist(검증 슬라이스 존재)"),
        ("control_rows_materialized", final["control_rows"] == 18 * 2 * 3, str(final["control_rows"]), "108", "controls scored for validation/OOS(검증/OOS 대조 점수화)"),
        ("quarantine_ledger_complete", final["quarantine_rows"] == 10, str(final["quarantine_rows"]), "10", "OOS-only lift ledger complete(OOS 단독 개선 장부 완전)"),
        ("runtime_firewall_carried", final["runtime_firewall_rows"] >= 3, str(final["runtime_firewall_rows"]), ">=3", "runtime firewall carried(런타임 방화벽 전달)"),
        ("ds_queue_materialized", final["ds_queue_rows"] == 4, str(final["ds_queue_rows"]), "4", "DS review queue opened(DS 검토 대기열 열림)"),
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
        "data_source": [rel(SOURCE_MODEL_INPUT), rel(VALIDATION_EDGE_FRAME), rel(DO_MODEL_MANIFEST)],
        "time_axis": "UTC source_row_id aligned validation/OOS rows(UTC source_row_id 정렬 검증/OOS 행)",
        "sample_scope": f"prediction_tape_rows={final['prediction_tape_rows']};models={final['model_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']};expected_rows={final['expected_prediction_tape_rows']}",
        "feature_label_boundary": "no new labels; DO target arrays reused for scoring only(새 라벨 없음, DO 목표 배열 점수화 전용 재사용)",
        "split_boundary": "validation/OOS only, no train fit(검증/OOS 전용, 학습 적합 없음)",
        "leakage_risk": "row tape could be used for filter mining(행 테이프가 필터 채굴에 오용될 위험)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_review_no_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "materialized predictions from frozen DO sklearn artifacts(DO 고정 sklearn 산출물 예측 물질화)",
        "target_and_label": "unchanged DO costed action labels(DO 비용 반영 행동 라벨 유지)",
        "split_method": "validation/OOS scoring only(검증/OOS 점수화 전용)",
        "selection_metric": "none; all models scored(없음, 전체 모델 점수화)",
        "secondary_metrics": "row pnl, validation slices, shifted controls, quarantine ledger(행 손익/검증 슬라이스/이동 대조/격리 장부)",
        "threshold_policy": "argmax from DO model, no threshold tuning(DO 모델 argmax, 임계값 튜닝 없음)",
        "overfit_risk": "using tape slices as release filters(테이프 슬라이스를 해제 필터로 쓰는 위험)",
        "calibration_risk": "probabilities remain diagnostic(확률은 진단 전용)",
        "comparison_baseline": rel(DQ_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"weak_validation_slice_rows={final['weak_validation_slice_rows']};control_block_rows={final['control_block_rows']}",
        "comparison_baseline": rel(DQ_FINAL),
        "likely_drivers": "time pockets, feature family, shifted control residual(시간 포켓/피처 계열/이동 대조 잔차)",
        "segment_checks": f"validation_slice_rows={final['validation_slice_rows']}",
        "trade_shape": f"prediction_tape_rows={final['prediction_tape_rows']};quarantine_rows={final['quarantine_rows']}",
        "alternative_explanations": "proxy cost mismatch or sample accident(프록시 비용 불일치 또는 표본 사고)",
        "attribution_confidence": "materialized_for_DS_review(DS 검토용 물질화)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_receipt = {
        "runtime_subject": "no MT5 runtime, Python artifact scoring only(MT5 런타임 없음, 파이썬 산출물 점수화만)",
        "parity_check": "inherits DO ONNX parity but does not run MT5(DO ONNX 동등성 상속, MT5 미실행)",
        "mt5_runtime_probe": "not_run",
        "usable_for": "DS review and repair evidence(DS 검토와 수리 근거)",
        "not_usable_for": "runtime authority, Forward Passed, live readiness(런타임 권위/전진 통과/실거래 준비)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "prediction tape, validation slices, controls, quarantine, firewall(예측 테이프/검증 슬라이스/대조/격리/방화벽)",
        "evidence_missing": "DS review, repaired training, MT5 runtime, forward evidence(DS 검토/수리 학습/MT5 런타임/전진 근거)",
        "judgment_label": "materialized_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "이제 집계표가 아니라 실제 행 단위로 어디서 깨지는지 볼 재료가 생겼다.",
    }
    paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(RUNTIME_RECEIPT, runtime_receipt),
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
    text = f"""# Stage337 run337DR Repair Input Materialization(수리 입력 물질화)

## Conclusion(결론)

run337DR(337DR 실행)는 run337DQ(337DQ 실행)의 설계에 따라 all-model prediction tape(전체 모델 예측 테이프), validation curve pockets(검증 곡선 포켓), shifted-control residuals(이동 대조 잔차), OOS quarantine ledger(OOS 격리 장부)를 물질화했다.

이 작업은 materialization-only(물질화 전용)이다. 새 학습, 후보 선택, 임계값 튜닝, MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 하지 않는다.

Effect(효과): run337DS(337DS 실행)는 행 단위 근거로 validation weakness/control residual(검증 약점/대조 잔차)을 검토한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- prediction_tape_rows(예측 테이프 행): `{final["prediction_tape_rows"]}`
- validation_slice_rows(검증 슬라이스 행): `{final["validation_slice_rows"]}`
- weak_validation_slice_rows(약한 검증 슬라이스 행): `{final["weak_validation_slice_rows"]}`
- control_rows(대조 행): `{final["control_rows"]}`
- control_block_rows(대조 차단 행): `{final["control_block_rows"]}`
- quarantine_rows(격리 행): `{final["quarantine_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DR

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): row-level evidence(행 단위 근거)를 만들었지만 선택/MT5/Forward(전진)는 계속 닫는다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(VALIDATION_CURVE_POCKET_SLICES)}`, `{rel(SHIFTED_CONTROL_RESIDUAL_TAPE)}`
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
        f"  Stage337 run337DR focus complete: validation support/control residual inputs(검증 지지/대조 잔차 입력)을 `{STATUS}`로 물질화했다. "
        f"Effect(효과): run337DS(337DS 실행)에서 row-level prediction/control/quarantine tape(행 단위 예측/대조/격리 테이프)를 검토한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DR focus complete")
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
    section = f"""## Stage337 run337DR(337DR 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 행 단위 예측/대조/격리 입력을 만들었지만 선택/MT5/Forward(전진)는 주장하지 않는다. Goal(목표)은 주장하지 않는다."""
    current_text = append_once(current_text, section, "Stage337 run337DR(337DR 실행)")
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection_text, _ = read_text_lossless(SELECTED_STATUS)
    selection = selection_text
    for field_name, value in {
        "latest_run": f"`{RUN_ID}`",
        "latest_decision": f"`{DECISION}`",
        "current_run": f"`{NEXT_RUN_ID}`",
        "rebuild_status": f"`{STATUS}`",
        "actual_mt5_execution": "`not_run_dr_materialization_only`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "effect": "`다음은 row-level materialization review(행 단위 물질화 검토)다.`",
    }.items():
        selection = replace_bullet_value(selection, field_name, value)
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337DR(337DR 실행) materialized row-level validation/control repair inputs and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DR(337DR 실행) materialized row-level validation/control"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337DR materialized row-level validation/control repair inputs and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DR materialized row-level validation/control"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "validation_support_control_residual_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"tape_rows={final['prediction_tape_rows']};control_blocks={final['control_block_rows']};quarantine={final['quarantine_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_input_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization_no_training_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "row_level_proxy_materialization",
        "scoreboard_lane": "data_integrity_model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"tape_rows={final['prediction_tape_rows']};control_rows={final['control_rows']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_performance_attribution_result_judgment",
        "evidence_scope": "row-level repair inputs materialized",
        "kpi_scope": "prediction_tape_validation_slices_controls_quarantine",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_input_materialization",
        "family": "data_integrity_model_validation_performance_attribution_result_judgment",
        "question": "where do validation weakness and shifted control residual occur row by row",
        "metric_scope": "tape_rows_slice_rows_control_rows",
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

    tape, tape_summary = materialize_prediction_tape()
    slice_rows = build_validation_slices(tape)
    control_rows = build_control_rows(tape)
    quarantine_rows = build_quarantine_ledger(tape)
    firewall_rows = build_firewall_carry()
    queue_rows = build_ds_queue()

    weak_slice_rows = sum(1 for row in slice_rows if row["slice_status"] == "weak_validation_slice")
    control_block_rows = sum(1 for row in control_rows if row["blocks_review"] == "true")
    dq_final = read_json(DQ_FINAL)
    dq_failed_gate_rows = sum(1 for row in read_csv(DQ_GATES) if row.get("status") != "passed")
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dq_next_action": dq_final.get("next_action", ""),
        "dq_failed_gate_rows": dq_failed_gate_rows,
        "missing_inputs": len(missing),
        "prediction_tape_rows": int(tape_summary["prediction_tape_rows"]),
        "expected_prediction_tape_rows": int(tape_summary["expected_prediction_tape_rows"]),
        "model_rows": int(tape_summary["model_rows"]),
        "scored_source_rows": int(tape_summary["scored_source_rows"]),
        "validation_slice_rows": len(slice_rows),
        "weak_validation_slice_rows": weak_slice_rows,
        "control_rows": len(control_rows),
        "control_block_rows": control_block_rows,
        "quarantine_rows": len(quarantine_rows),
        "runtime_firewall_rows": len(firewall_rows),
        "ds_queue_rows": len(queue_rows),
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
    summary_rows = build_summary_rows(final)
    artifacts: list[Path] = [
        ALL_MODEL_PREDICTION_TAPE,
        write_csv(VALIDATION_CURVE_POCKET_SLICES, SLICE_COLUMNS, slice_rows),
        write_csv(SHIFTED_CONTROL_RESIDUAL_TAPE, CONTROL_COLUMNS, control_rows),
        write_csv(OOS_QUARANTINE_LEDGER, QUARANTINE_COLUMNS, quarantine_rows),
        write_csv(RUNTIME_FIREWALL_CARRY, FIREWALL_COLUMNS, firewall_rows),
        write_csv(MATERIALIZATION_SUMMARY, SUMMARY_COLUMNS, summary_rows),
        write_csv(DS_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
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
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
