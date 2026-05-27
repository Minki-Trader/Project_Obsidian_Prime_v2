from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import design_transfer_density_control_objective_repair as dw  # noqa: E402
from stage_pipelines.stage337 import materialize_broad_validation_failure_control_residual_repair_inputs as du  # noqa: E402
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
STAGE_ID = dw.STAGE_ID
RUN_NUMBER = "run337DX"
RUN_ID = "run337DX_materialize_transfer_density_control_objective_repair_inputs_without_db_v1"
PARENT_RUN_ID = dw.RUN_ID
NEXT_RUN_ID = "run337DY_review_transfer_density_control_objective_repair_inputs_without_db_v1"
STATUS = "completed_stage337DX_transfer_density_control_objective_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "train_only_objective_density_control_wfo_inputs_materialized_review_required"
DECISION = "stage337DX_open_run337DY_review_transfer_density_control_objective_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DX_transfer_density_control_objective_repair_input_materialization_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dw.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dw.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DX_transfer_density_control_objective_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DX_transfer_density_control_objective_repair_inputs.md"
SELECTED_STATUS = dw.SELECTED_STATUS
STAGE_BRIEF = dw.STAGE_BRIEF
WORKSPACE_STATE = dw.WORKSPACE_STATE
CURRENT_STATE = dw.CURRENT_STATE
CHANGELOG = dw.CHANGELOG
RUN_REGISTRY = dw.RUN_REGISTRY
ALPHA_LEDGER = dw.ALPHA_LEDGER
ARTIFACT_REGISTRY = dw.ARTIFACT_REGISTRY
STAGE_LEDGER = dw.STAGE_LEDGER

DW_FINAL = dw.FINAL_DECISION
DW_GATES = dw.REQUIRED_GATE_AUDIT
DW_QUEUE = dw.DX_QUEUE
TRAIN_ONLY_OBJECTIVE_CONTRACTS = dw.TRAIN_ONLY_OBJECTIVE_CONTRACTS
DENSITY_DECONCENTRATION_CONTRACTS = dw.DENSITY_DECONCENTRATION_CONTRACTS
CONTROL_RESIDUAL_ISOLATION_CONTRACTS = dw.CONTROL_RESIDUAL_ISOLATION_CONTRACTS
WFO_EMBARGO_PRECHECK_DESIGN = dw.WFO_EMBARGO_PRECHECK_DESIGN
NO_RELEASE_FIREWALL_DESIGN = dw.NO_RELEASE_FIREWALL_DESIGN
ALL_SPLIT_PREDICTION_TAPE = du.ALL_SPLIT_PREDICTION_TAPE
DENSITY_DRAWDOWN_MATRIX = du.DENSITY_DRAWDOWN_MATRIX
CONTROL_ISOLATION_MATRIX = du.CONTROL_ISOLATION_MATRIX

TRAIN_ONLY_OBJECTIVE_INPUT_FRAME = RUN_DIR / "train_only_objective_input_frame.parquet"
OBJECTIVE_CONTRACT_AUDIT = RUN_DIR / "objective_contract_audit.csv"
DENSITY_DECONCENTRATION_MATRIX = RUN_DIR / "density_deconcentration_matrix.csv"
CONTROL_RESIDUAL_ISOLATION_MATRIX = RUN_DIR / "control_residual_isolation_matrix.csv"
WFO_EMBARGO_FEASIBILITY = RUN_DIR / "wfo_embargo_feasibility.csv"
NO_RELEASE_FIREWALL_CARRY = RUN_DIR / "no_release_firewall_carry.csv"
DY_QUEUE = RUN_DIR / "run337DY_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DW_FINAL,
    DW_GATES,
    DW_QUEUE,
    TRAIN_ONLY_OBJECTIVE_CONTRACTS,
    DENSITY_DECONCENTRATION_CONTRACTS,
    CONTROL_RESIDUAL_ISOLATION_CONTRACTS,
    WFO_EMBARGO_PRECHECK_DESIGN,
    NO_RELEASE_FIREWALL_DESIGN,
    ALL_SPLIT_PREDICTION_TAPE,
    DENSITY_DRAWDOWN_MATRIX,
    CONTROL_ISOLATION_MATRIX,
)
OUTPUT_FILES = (
    TRAIN_ONLY_OBJECTIVE_INPUT_FRAME,
    OBJECTIVE_CONTRACT_AUDIT,
    DENSITY_DECONCENTRATION_MATRIX,
    CONTROL_RESIDUAL_ISOLATION_MATRIX,
    WFO_EMBARGO_FEASIBILITY,
    NO_RELEASE_FIREWALL_CARRY,
    DY_QUEUE,
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

AUDIT_COLUMNS = (
    "contract_id",
    "contract_rows",
    "materialized_rows",
    "materialized_status",
    "leakage_guard",
    "effect",
    "claim_boundary",
)
DENSITY_COLUMNS = (
    "model_id",
    "split",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "rows",
    "trade_count",
    "signal_density",
    "train_reference_density",
    "density_gap_vs_train",
    "density_pressure_flag",
    "max_drawdown",
    "recovery_factor",
    "materialized_status",
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
    "lineage_family",
    "cost_ladder",
    "materialized_status",
    "effect",
    "claim_boundary",
)
WFO_COLUMNS = (
    "fold_id",
    "train_start",
    "train_end",
    "embargo_rows",
    "validation_start",
    "validation_end",
    "train_rows",
    "validation_rows",
    "feasibility_status",
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


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def parse_lineage(model_id: str) -> tuple[str, str]:
    if "technical_session_vol_lag_safe" in model_id:
        family = "technical_session_vol_lag_safe"
    elif "macro_equity_lag_safe_rescue" in model_id:
        family = "macro_equity_lag_safe_rescue"
    else:
        family = "unknown"
    if "spread_plus_extra0" in model_id:
        cost = "spread_plus_extra0"
    elif "spread_plus_extra2" in model_id:
        cost = "spread_plus_extra2"
    elif "spread_plus_extra5" in model_id:
        cost = "spread_plus_extra5"
    else:
        cost = "unknown"
    return family, cost


def materialize_objective_frame() -> tuple[pd.DataFrame, dict[str, int]]:
    tape = pd.read_parquet(io_path(ALL_SPLIT_PREDICTION_TAPE))
    train = tape.loc[tape["split"] == "train"].copy()
    train["timestamp"] = pd.to_datetime(train["timestamp"], utc=True)
    train.sort_values(["model_id", "source_row_id"], inplace=True)
    train["abs_pnl_after_cost"] = train["pnl_after_cost"].abs()
    train["trade_abs_pnl_after_cost"] = np.where(train["is_trade"].astype(bool), train["abs_pnl_after_cost"], np.nan)
    grouped = train.groupby("model_id", group_keys=False)
    train["train_model_trade_abs_pnl_q25"] = grouped["trade_abs_pnl_after_cost"].transform(lambda x: float(x.dropna().quantile(0.25)) if x.notna().any() else 0.0)
    train["low_margin_trade_tag"] = train["is_trade"].astype(bool) & (train["abs_pnl_after_cost"] <= train["train_model_trade_abs_pnl_q25"])
    train["curve_cumsum"] = grouped["pnl_after_cost"].cumsum()
    train["curve_peak"] = grouped["curve_cumsum"].cummax()
    train["underwater_tag"] = train["curve_cumsum"] < train["curve_peak"]
    train["drawdown_pressure_value"] = train["curve_peak"] - train["curve_cumsum"]
    train["direction_residual_tag"] = (train["is_trade"].astype(bool)) & (train["pred_label"].astype(int) != train["true_label"].astype(int))
    train["abstention_candidate_tag"] = (~train["is_trade"].astype(bool)) | train["low_margin_trade_tag"]
    train["oos_lift_quarantine_tag"] = False
    train["allowed_split_scope"] = "train_only"
    columns = [
        "source_row_id",
        "timestamp",
        "split",
        "model_id",
        "task_id",
        "target_id",
        "cost_policy_id",
        "feature_set_id",
        "model_config_id",
        "true_label",
        "pred_label",
        "pred_name",
        "prob_short",
        "prob_flat",
        "prob_long",
        "future_log_return_12",
        "cost_return",
        "direction",
        "is_trade",
        "pnl_after_cost",
        "abs_pnl_after_cost",
        "trade_abs_pnl_after_cost",
        "train_model_trade_abs_pnl_q25",
        "low_margin_trade_tag",
        "underwater_tag",
        "drawdown_pressure_value",
        "direction_residual_tag",
        "abstention_candidate_tag",
        "oos_lift_quarantine_tag",
        "allowed_split_scope",
    ]
    out = train.loc[:, columns].copy()
    io_path(TRAIN_ONLY_OBJECTIVE_INPUT_FRAME).parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(io_path(TRAIN_ONLY_OBJECTIVE_INPUT_FRAME), index=False)
    return out, {
        "rows": len(out),
        "models": int(out["model_id"].nunique()),
        "source_rows": int(out["source_row_id"].nunique()),
        "low_margin_rows": int(out["low_margin_trade_tag"].sum()),
        "underwater_rows": int(out["underwater_tag"].sum()),
        "direction_residual_rows": int(out["direction_residual_tag"].sum()),
    }


def build_objective_audit(objective_summary: Mapping[str, int]) -> list[dict[str, str]]:
    contract_rows = read_csv(TRAIN_ONLY_OBJECTIVE_CONTRACTS)
    rows: list[dict[str, str]] = []
    for contract in contract_rows:
        rows.append(
            {
                "contract_id": str(contract.get("contract_id", "")),
                "contract_rows": "1",
                "materialized_rows": str(objective_summary["rows"]),
                "materialized_status": "materialized_train_only_no_training",
                "leakage_guard": "split=train only; validation/OOS excluded(학습 분할만, 검증/OOS 제외)",
                "effect": "confirms objective contract has train-only materialization(목표 계약의 학습 전용 물질화 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_density_matrix() -> list[dict[str, Any]]:
    density = pd.read_csv(io_path(DENSITY_DRAWDOWN_MATRIX))
    train_reference = (
        density.loc[density["split"] == "train", ["model_id", "signal_density"]]
        .rename(columns={"signal_density": "train_reference_density"})
    )
    merged = density.merge(train_reference, on="model_id", how="left")
    merged["density_gap_vs_train"] = pd.to_numeric(merged["signal_density"], errors="coerce") - pd.to_numeric(merged["train_reference_density"], errors="coerce")
    rows: list[dict[str, Any]] = []
    for row in merged.to_dict("records"):
        status = "review_only"
        if row.get("split") == "validation" and "high_density_pressure" in str(row.get("pressure_status", "")):
            status = "validation_density_pressure"
        rows.append(
            {
                "model_id": row.get("model_id", ""),
                "split": row.get("split", ""),
                "cost_policy_id": row.get("cost_policy_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "model_config_id": row.get("model_config_id", ""),
                "rows": row.get("rows", 0),
                "trade_count": row.get("trade_count", 0),
                "signal_density": row.get("signal_density", 0),
                "train_reference_density": row.get("train_reference_density", 0),
                "density_gap_vs_train": row.get("density_gap_vs_train", 0),
                "density_pressure_flag": status,
                "max_drawdown": row.get("max_drawdown", 0),
                "recovery_factor": row.get("recovery_factor", 0),
                "materialized_status": "review_only_no_threshold_tuning",
                "effect": "materializes density deconcentration inputs without tuning(튜닝 없이 밀도 탈집중 입력 물질화)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_control_matrix() -> list[dict[str, Any]]:
    control = pd.read_csv(io_path(CONTROL_ISOLATION_MATRIX))
    rows: list[dict[str, Any]] = []
    for row in control.to_dict("records"):
        family, cost = parse_lineage(str(row.get("model_id", "")))
        status = "blocked_lineage_review" if str(row.get("blocks_review", "")).lower() == "true" else "control_context"
        rows.append(
            {
                "model_id": row.get("model_id", ""),
                "task_id": row.get("task_id", ""),
                "split": row.get("split", ""),
                "control_id": row.get("control_id", ""),
                "rows": row.get("rows", 0),
                "candidate_balanced_accuracy": row.get("candidate_balanced_accuracy", 0),
                "control_alignment_balanced_accuracy": row.get("control_alignment_balanced_accuracy", 0),
                "blocks_review": row.get("blocks_review", ""),
                "lineage_family": family,
                "cost_ladder": cost,
                "materialized_status": status,
                "effect": "materializes control residual isolation without rule relaxation(규칙 완화 없이 대조 잔차 격리 물질화)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_wfo_feasibility() -> list[dict[str, Any]]:
    tape = pd.read_parquet(io_path(ALL_SPLIT_PREDICTION_TAPE), columns=["source_row_id", "timestamp", "split"])
    base = tape.drop_duplicates("source_row_id").sort_values("source_row_id").copy()
    base["timestamp"] = pd.to_datetime(base["timestamp"], utc=True)
    n = len(base)
    embargo_rows = 12
    rows: list[dict[str, Any]] = []
    boundaries = [(0.50, 0.60), (0.60, 0.70), (0.70, 0.80), (0.80, 0.90)]
    for idx, (train_end_frac, validation_end_frac) in enumerate(boundaries, start=1):
        train_end_raw = int(n * train_end_frac)
        validation_end = int(n * validation_end_frac)
        train_end = max(0, train_end_raw - embargo_rows)
        train = base.iloc[:train_end]
        validation = base.iloc[train_end_raw:validation_end]
        feasible = len(train) > 5000 and len(validation) > 1000
        rows.append(
            {
                "fold_id": f"rolling_origin_precheck_{idx:02d}",
                "train_start": train["timestamp"].min().isoformat() if len(train) else "",
                "train_end": train["timestamp"].max().isoformat() if len(train) else "",
                "embargo_rows": embargo_rows,
                "validation_start": validation["timestamp"].min().isoformat() if len(validation) else "",
                "validation_end": validation["timestamp"].max().isoformat() if len(validation) else "",
                "train_rows": len(train),
                "validation_rows": len(validation),
                "feasibility_status": "feasible_precheck_not_training" if feasible else "infeasible_geometry",
                "effect": "materializes WFO/embargo feasibility without model fitting(모델 적합 없이 WFO/격리 가능성 물질화)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_firewall_carry() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(NO_RELEASE_FIREWALL_DESIGN):
        rows.append(
            {
                "firewall_id": str(row.get("firewall_id", "")),
                "blocked_action_or_claim": str(row.get("blocked_action_or_claim", "")),
                "blocked_reason": str(row.get("blocked_reason", "")),
                "carry_status": "carried_forward_active",
                "effect": "keeps no-release firewall active in DX(DX에서 무해제 방화벽 활성 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_dy_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DY_review_objective_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review train-only objective inputs(학습 전용 목표 입력 검토)",
            "required_inputs": f"{rel(TRAIN_ONLY_OBJECTIVE_INPUT_FRAME)};{rel(OBJECTIVE_CONTRACT_AUDIT)}",
            "required_outputs": "objective_input_review.csv",
            "blocked_if_missing": "objective frame/audit(목표 프레임/감사)",
            "forbidden_action": "no model training from unreviewed inputs(미검토 입력으로 모델 학습 금지)",
            "effect": "checks objective materialization before training(학습 전 목표 물질화 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DY_review_density_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review density deconcentration inputs(밀도 탈집중 입력 검토)",
            "required_inputs": rel(DENSITY_DECONCENTRATION_MATRIX),
            "required_outputs": "density_input_review.csv",
            "blocked_if_missing": "density matrix(밀도 행렬)",
            "forbidden_action": "no density threshold tuning(밀도 임계값 튜닝 금지)",
            "effect": "checks density inputs remain diagnostic(밀도 입력이 진단 전용인지 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DY_review_control_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review control residual isolation inputs(대조 잔차 격리 입력 검토)",
            "required_inputs": rel(CONTROL_RESIDUAL_ISOLATION_MATRIX),
            "required_outputs": "control_input_review.csv",
            "blocked_if_missing": "control matrix(대조 행렬)",
            "forbidden_action": "no control relaxation(대조 완화 금지)",
            "effect": "checks shifted residual isolation before training(학습 전 이동 잔차 격리 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DY_review_wfo_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "review WFO/embargo feasibility(WFO/격리 가능성 검토)",
            "required_inputs": rel(WFO_EMBARGO_FEASIBILITY),
            "required_outputs": "wfo_input_review.csv",
            "blocked_if_missing": "WFO feasibility(WFO 가능성)",
            "forbidden_action": "no post-selection WFO backfill(선택 후 WFO 사후 보강 금지)",
            "effect": "checks split geometry before future training(미래 학습 전 분할 구조 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DY_review_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "review no-release firewall carry(무해제 방화벽 전달 검토)",
            "required_inputs": rel(NO_RELEASE_FIREWALL_CARRY),
            "required_outputs": "firewall_review.csv",
            "blocked_if_missing": "firewall carry(방화벽 전달)",
            "forbidden_action": "no candidate selection/MT5/Forward/Goal(후보 선택/MT5/전진/목표 금지)",
            "effect": "keeps DX from being interpreted as promotion(DX를 승격으로 해석하지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DW/DU inputs exist(필수 DW/DU 입력 존재)"),
        ("parent_dw_gates_passed", final["dw_failed_gate_rows"] == 0, str(final["dw_failed_gate_rows"]), "0", "DW design usable(DW 설계 사용 가능)"),
        ("parent_next_action_matches", final["dw_next_action"] == RUN_ID, str(final["dw_next_action"]), RUN_ID, "continues DW queue(DW 대기열을 이어감)"),
        ("objective_frame_materialized", final["objective_frame_rows"] == final["expected_objective_frame_rows"], f"{final['objective_frame_rows']}/{final['expected_objective_frame_rows']}", "all", "train-only objective frame materialized(학습 전용 목표 프레임 물질화)"),
        ("objective_audit_materialized", final["objective_audit_rows"] >= 5, str(final["objective_audit_rows"]), ">=5", "objective audit materialized(목표 감사 물질화)"),
        ("density_matrix_materialized", final["density_matrix_rows"] == 54, str(final["density_matrix_rows"]), "54", "density matrix materialized(밀도 행렬 물질화)"),
        ("control_matrix_materialized", final["control_matrix_rows"] == 162, str(final["control_matrix_rows"]), "162", "control matrix materialized(대조 행렬 물질화)"),
        ("wfo_feasibility_materialized", final["wfo_feasibility_rows"] == 4, str(final["wfo_feasibility_rows"]), "4", "WFO feasibility materialized(WFO 가능성 물질화)"),
        ("firewall_carried", final["firewall_rows"] >= 5, str(final["firewall_rows"]), ">=5", "firewall carried(방화벽 전달)"),
        ("dy_queue_materialized", final["dy_queue_rows"] == 5, str(final["dy_queue_rows"]), "5", "DY review queue opened(DY 검토 대기열 열림)"),
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
        "time_axis": "DU prediction tape UTC timestamps; objective frame train split only(DU 예측 테이프 UTC 시점, 목표 프레임은 학습 분할만)",
        "sample_scope": f"objective_rows={final['objective_frame_rows']};train_source_rows={final['train_source_rows']};models={final['objective_model_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']};expected_objective_rows={final['expected_objective_frame_rows']}",
        "feature_label_boundary": "train-only tags use train split rows; validation/OOS excluded from objective frame(학습 전용 태그는 학습 분할 행만 사용, 검증/OOS는 목표 프레임 제외)",
        "split_boundary": "validation/OOS kept only in density/control diagnostics, not objective labels(검증/OOS는 밀도/대조 진단만, 목표 라벨 아님)",
        "leakage_risk": "future training may overuse train objective tags without DY review(DY 검토 없이 미래 학습이 목표 태그를 과사용할 위험)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_review_no_training",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "no new model; existing DU predictions transformed into repair inputs(새 모델 없음, 기존 DU 예측을 수리 입력으로 변환)",
        "target_and_label": "train-only audit tags materialized; no validation/OOS labels reused(학습 전용 감사 태그 물질화, 검증/OOS 라벨 재사용 없음)",
        "split_method": "train objective frame plus review-only validation/OOS diagnostics(학습 목표 프레임과 검토 전용 검증/OOS 진단)",
        "selection_metric": "none(없음)",
        "secondary_metrics": "low margin, underwater, direction residual, density gap, control block, WFO feasibility(저여백/침수/방향 잔차/밀도 차이/대조 차단/WFO 가능성)",
        "threshold_policy": "no threshold tuning(임계값 튜닝 없음)",
        "overfit_risk": "training directly from unreviewed tags(미검토 태그로 직접 학습하는 위험)",
        "calibration_risk": "probabilities carried from parent as diagnostics(확률은 부모 산출 진단값으로만 전달)",
        "comparison_baseline": rel(DW_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"low_margin_rows={final['low_margin_rows']};underwater_rows={final['underwater_rows']};direction_residual_rows={final['direction_residual_rows']}",
        "comparison_baseline": rel(DW_FINAL),
        "likely_drivers": "train-only low margin, drawdown pressure, direction residual, density/control blockers(학습 전용 저여백/드로다운 압력/방향 잔차/밀도·대조 차단)",
        "segment_checks": f"density_rows={final['density_matrix_rows']};control_rows={final['control_matrix_rows']};wfo_rows={final['wfo_feasibility_rows']}",
        "trade_shape": "train-only objective frame includes trade and drawdown tags(학습 전용 목표 프레임에 거래/드로다운 태그 포함)",
        "alternative_explanations": "train tags may describe model behavior rather than market signal(학습 태그가 시장 신호보다 모델 행동을 설명할 수 있음)",
        "attribution_confidence": "materialized_for_DY_review(DY 검토용 물질화)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "objective frame, density matrix, control matrix, WFO feasibility, firewall(목표 프레임/밀도 행렬/대조 행렬/WFO 가능성/방화벽)",
        "evidence_missing": "DY review, model training, MT5, forward evidence(DY 검토/모델 학습/MT5/전진 근거)",
        "judgment_label": "materialized_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "DX는 학습 재료를 만들었지만 아직 써도 되는지 검토하지 않았다.",
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
        "availability": "ignored_materialization_outputs_with_tracked_report(무시된 물질화 출력과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DX Transfer Density Control Objective Repair Inputs(전이/밀도/대조/목표 수리 입력)

## Conclusion(결론)

run337DX(337DX 실행)는 DW 설계를 실제 입력으로 물질화했다.

train-only objective frame(학습 전용 목표 프레임)은 `{final["objective_frame_rows"]}`행이고, validation/OOS(검증/OOS)는 목표 프레임에서 제외했다. 밀도 행렬 `{final["density_matrix_rows"]}`행, 대조 격리 행렬 `{final["control_matrix_rows"]}`행, WFO/embargo feasibility(WFO/격리 가능성) `{final["wfo_feasibility_rows"]}`행도 만들었다.

이 작업은 materialization-only(물질화 전용)이다. 새 학습, 후보 선택, 임계값 튜닝, MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 하지 않는다.

Effect(효과): run337DY(337DY 실행)가 이 입력이 학습에 적합한지, 또는 leakage/repair-overfit(누수/수리 과적합) 위험 때문에 다시 설계해야 하는지 검토한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- objective_frame_rows(목표 프레임 행): `{final["objective_frame_rows"]}`
- train_source_rows(학습 원천 행): `{final["train_source_rows"]}`
- low_margin_rows(저여백 행): `{final["low_margin_rows"]}`
- underwater_rows(침수 행): `{final["underwater_rows"]}`
- direction_residual_rows(방향 잔차 행): `{final["direction_residual_rows"]}`
- density_matrix_rows(밀도 행렬 행): `{final["density_matrix_rows"]}`
- control_matrix_rows(대조 행렬 행): `{final["control_matrix_rows"]}`
- wfo_feasibility_rows(WFO 가능성 행): `{final["wfo_feasibility_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DX

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 학습 전용 수리 입력을 만들었지만 DY 검토 전에는 학습/선택/MT5/Forward(전진)를 열지 않는다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(OBJECTIVE_CONTRACT_AUDIT)}`, `{rel(DY_QUEUE)}`
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
        f"  Stage337 run337DX focus complete: transfer/density/control/objective repair inputs(전이/밀도/대조/목표 수리 입력)을 `{STATUS}`로 물질화했다. "
        f"Effect(효과): run337DY(337DY 실행)에서 objective/density/control/WFO input safety(목표/밀도/대조/WFO 입력 안전성)를 검토한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DX focus complete")
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
    section = f"""## Stage337 run337DX(337DX 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 학습 전용 수리 입력을 만들었지만 학습/선택/MT5/Forward(전진)는 주장하지 않는다. Goal(목표)은 주장하지 않는다."""
    current_text = append_once(current_text, section, "Stage337 run337DX(337DX 실행)")
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection_text, _ = read_text_lossless(SELECTED_STATUS)
    selection = selection_text
    for field_name, value in {
        "latest_run": f"`{RUN_ID}`",
        "latest_decision": f"`{DECISION}`",
        "current_run": f"`{NEXT_RUN_ID}`",
        "rebuild_status": f"`{STATUS}`",
        "actual_mt5_execution": "`not_run_dx_materialization_only`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "effect": "`다음은 transfer/density/control/objective input review(전이/밀도/대조/목표 입력 검토)다.`",
    }.items():
        selection = replace_bullet_value(selection, field_name, value)
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337DX(337DX 실행) materialized transfer/density/control/objective repair inputs and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DX(337DX 실행) materialized transfer"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337DX materialized transfer/density/control/objective repair inputs and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DX materialized transfer"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "transfer_density_control_objective_repair_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"objective_rows={final['objective_frame_rows']};density_rows={final['density_matrix_rows']};control_rows={final['control_matrix_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
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
        "kpi_scope": "objective_density_control_wfo_inputs",
        "scoreboard_lane": "data_integrity_model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"objective_rows={final['objective_frame_rows']};low_margin={final['low_margin_rows']};underwater={final['underwater_rows']}",
        "guardrail_kpi": "train_only_objective;no_training;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_performance_attribution",
        "evidence_scope": "repair inputs materialized",
        "kpi_scope": "objective_density_control_wfo_inputs",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_input_materialization",
        "family": "data_integrity_model_validation_performance_attribution",
        "question": "are transfer density control objective repair inputs safely materialized",
        "metric_scope": "objective_frame_density_control_wfo",
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

    dw_final = read_json(DW_FINAL)
    dw_failed_gate_rows = sum(1 for row in read_csv(DW_GATES) if row.get("status") != "passed")
    objective_frame, objective_summary = materialize_objective_frame()
    objective_audit_rows = build_objective_audit(objective_summary)
    density_rows = build_density_matrix()
    control_rows = build_control_matrix()
    wfo_rows = build_wfo_feasibility()
    firewall_rows = build_firewall_carry()
    queue_rows = build_dy_queue()
    expected_objective_rows = int(objective_summary["source_rows"] * objective_summary["models"])
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dw_next_action": dw_final.get("next_action", ""),
        "dw_failed_gate_rows": dw_failed_gate_rows,
        "missing_inputs": len(missing),
        "objective_frame_rows": int(objective_summary["rows"]),
        "expected_objective_frame_rows": expected_objective_rows,
        "objective_model_rows": int(objective_summary["models"]),
        "train_source_rows": int(objective_summary["source_rows"]),
        "low_margin_rows": int(objective_summary["low_margin_rows"]),
        "underwater_rows": int(objective_summary["underwater_rows"]),
        "direction_residual_rows": int(objective_summary["direction_residual_rows"]),
        "objective_audit_rows": len(objective_audit_rows),
        "density_matrix_rows": len(density_rows),
        "control_matrix_rows": len(control_rows),
        "wfo_feasibility_rows": len(wfo_rows),
        "firewall_rows": len(firewall_rows),
        "dy_queue_rows": len(queue_rows),
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
        TRAIN_ONLY_OBJECTIVE_INPUT_FRAME,
        write_csv(OBJECTIVE_CONTRACT_AUDIT, AUDIT_COLUMNS, objective_audit_rows),
        write_csv(DENSITY_DECONCENTRATION_MATRIX, DENSITY_COLUMNS, density_rows),
        write_csv(CONTROL_RESIDUAL_ISOLATION_MATRIX, CONTROL_COLUMNS, control_rows),
        write_csv(WFO_EMBARGO_FEASIBILITY, WFO_COLUMNS, wfo_rows),
        write_csv(NO_RELEASE_FIREWALL_CARRY, FIREWALL_COLUMNS, firewall_rows),
        write_csv(DY_QUEUE, QUEUE_COLUMNS, queue_rows),
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
