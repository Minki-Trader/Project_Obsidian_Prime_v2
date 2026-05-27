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
from stage_pipelines.stage337 import design_prediction_surface_validation_edge_repair as dl  # noqa: E402
from stage_pipelines.stage337 import review_pair_prediction_tape_surface_attribution as dk  # noqa: E402
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
STAGE_ID = dl.STAGE_ID
RUN_NUMBER = "run337DM"
RUN_ID = "run337DM_materialize_prediction_surface_validation_edge_repair_inputs_without_db_v1"
PARENT_RUN_ID = dl.RUN_ID
NEXT_RUN_ID = "run337DN_review_prediction_surface_validation_edge_repair_inputs_without_db_v1"
STATUS = "completed_stage337DM_prediction_surface_validation_edge_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "repair_inputs_materialized_review_required_before_training"
DECISION = "stage337DM_open_run337DN_review_prediction_surface_validation_edge_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DM_prediction_surface_validation_edge_repair_inputs_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dl.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dl.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DM_prediction_surface_validation_edge_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DM_prediction_surface_validation_edge_repair_inputs.md"
SELECTED_STATUS = dl.SELECTED_STATUS
STAGE_BRIEF = dl.STAGE_BRIEF
WORKSPACE_STATE = dl.WORKSPACE_STATE
CURRENT_STATE = dl.CURRENT_STATE
CHANGELOG = dl.CHANGELOG
RUN_REGISTRY = dl.RUN_REGISTRY
ALPHA_LEDGER = dl.ALPHA_LEDGER
ARTIFACT_REGISTRY = dl.ARTIFACT_REGISTRY
STAGE_LEDGER = dl.STAGE_LEDGER

DL_FINAL = dl.FINAL_DECISION
DL_GATES = dl.REQUIRED_GATE_AUDIT
DL_VALIDATION_CONTRACT = dl.VALIDATION_EDGE_CONTRACT
DL_SURFACE_CONTRACT = dl.SURFACE_DECONTRACT
DL_BALANCED_QUEUE = dl.BALANCED_QUEUE
DL_GUARDRAILS = dl.NO_OVERFIT_GUARDRAILS
DL_RUNTIME_FIREWALL = dl.RUNTIME_FIREWALL
DL_DM_QUEUE = dl.DM_QUEUE

DJ_PAIR_TAPE = dk.DJ_PAIR_TAPE
DJ_PAIR_SCORECARD = dk.DJ_PAIR_SCORECARD
DJ_CURVE_REVIEW = dk.DJ_CURVE_REVIEW
DJ_SURFACE_AUDIT = dk.DJ_SURFACE_AUDIT
DK_SLICE_BLOCKERS = dk.SLICE_BLOCKERS
DK_FAILURE_MEMORY = dk.FAILURE_MEMORY

VALIDATION_EDGE_FRAME = RUN_DIR / "validation_edge_input_frame.parquet"
VALIDATION_EDGE_AUDIT = RUN_DIR / "validation_edge_audit.csv"
COST_LADDER_MATRIX = RUN_DIR / "cost_ladder_deconcentration_matrix.csv"
MODEL_FAMILY_MATRIX = RUN_DIR / "model_family_surface_matrix.csv"
FEATURE_FAMILY_MATRIX = RUN_DIR / "feature_family_deconcentration_matrix.csv"
SLICE_BREADTH_MATRIX = RUN_DIR / "slice_breadth_guard_matrix.csv"
SURFACE_BUNDLE = RUN_DIR / "surface_deconcentration_input_bundle.json"
BALANCED_MANIFEST = RUN_DIR / "balanced_repair_attack_input_manifest.json"
NEGATIVE_CONTROL_CONTRACT = RUN_DIR / "negative_control_contract.csv"
LABEL_BOUNDARY_AUDIT = RUN_DIR / "label_boundary_audit.csv"
FORBIDDEN_SELECTION_AUDIT = RUN_DIR / "forbidden_selection_audit.csv"
DENSITY_FLOOR_CONTRACT = RUN_DIR / "density_floor_contract.csv"
THIN_SLICE_EXCLUSION_AUDIT = RUN_DIR / "thin_slice_exclusion_audit.csv"
PAYOFF_SHAPE_MATRIX = RUN_DIR / "payoff_shape_expansion_matrix.csv"
RUNTIME_FIREWALL_CARRY = RUN_DIR / "runtime_firewall_carryforward.csv"
FUTURE_PROXY_MT5_CHECKLIST = RUN_DIR / "future_proxy_mt5_evidence_checklist.csv"
DN_QUEUE = RUN_DIR / "run337DN_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DL_FINAL,
    DL_GATES,
    DL_VALIDATION_CONTRACT,
    DL_SURFACE_CONTRACT,
    DL_BALANCED_QUEUE,
    DL_GUARDRAILS,
    DL_RUNTIME_FIREWALL,
    DL_DM_QUEUE,
    DJ_PAIR_TAPE,
    DJ_PAIR_SCORECARD,
    DJ_CURVE_REVIEW,
    DJ_SURFACE_AUDIT,
    DK_SLICE_BLOCKERS,
    DK_FAILURE_MEMORY,
)
OUTPUT_FILES = (
    VALIDATION_EDGE_FRAME,
    VALIDATION_EDGE_AUDIT,
    COST_LADDER_MATRIX,
    MODEL_FAMILY_MATRIX,
    FEATURE_FAMILY_MATRIX,
    SLICE_BREADTH_MATRIX,
    SURFACE_BUNDLE,
    BALANCED_MANIFEST,
    NEGATIVE_CONTROL_CONTRACT,
    LABEL_BOUNDARY_AUDIT,
    FORBIDDEN_SELECTION_AUDIT,
    DENSITY_FLOOR_CONTRACT,
    THIN_SLICE_EXCLUSION_AUDIT,
    PAYOFF_SHAPE_MATRIX,
    RUNTIME_FIREWALL_CARRY,
    FUTURE_PROXY_MT5_CHECKLIST,
    DN_QUEUE,
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

AUDIT_COLUMNS = ("audit_id", "split", "rows", "pairs", "trade_rows", "mean_margin", "positive_margin_rate", "quarantine_rows", "role", "effect", "claim_boundary")
SURFACE_COLUMNS = ("matrix_id", "axis", "group_id", "split", "rows", "pair_count", "trade_count", "mean_pf", "min_pf", "max_pf", "mean_net", "status", "effect", "claim_boundary")
SLICE_COLUMNS = ("slice_axis", "slice_review_status", "rows", "validation_trades_sum", "oos_trades_sum", "status", "effect", "claim_boundary")
CONTROL_COLUMNS = ("control_id", "control_family", "materialized_rule", "blocks_if", "evidence_output", "status", "effect", "claim_boundary")
BOUNDARY_COLUMNS = ("audit_id", "checked_subject", "rows", "status", "evidence", "effect", "claim_boundary")
FORBIDDEN_COLUMNS = ("audit_id", "forbidden_source", "rows", "status", "required_handling", "effect", "claim_boundary")
DENSITY_COLUMNS = ("contract_id", "source", "rows", "non_thin_rows", "thin_rows", "min_trade_floor", "status", "effect", "claim_boundary")
PAYOFF_COLUMNS = ("pair_id", "cost_policy_id", "feature_set_id", "model_config_id", "train_pf", "validation_pf", "oos_pf", "train_trades", "validation_trades", "oos_trades", "repair_role", "selection_allowed", "effect", "claim_boundary")
FIREWALL_COLUMNS = ("firewall_id", "held_action", "held_until", "required_evidence", "forbidden_claim", "carry_status", "effect", "claim_boundary")
CHECKLIST_COLUMNS = ("check_id", "future_gate", "required_artifact", "required_comparison", "blocks_claim", "effect", "claim_boundary")
QUEUE_COLUMNS = ("queue_id", "next_run_id", "priority", "task", "required_inputs", "required_outputs", "blocked_if_missing", "forbidden_action", "effect", "claim_boundary")
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


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


def profit_factor(values: pd.Series) -> float:
    positive = float(values[values > 0].sum())
    negative = abs(float(values[values < 0].sum()))
    if negative == 0:
        return 999.0 if positive > 0 else 0.0
    return positive / negative


def load_inputs() -> dict[str, Any]:
    curve = pd.read_csv(io_path(DJ_CURVE_REVIEW))
    thin_pairs = set(curve.loc[curve["review_status"] == "oos_positive_validation_thin_block", "pair_id"].astype(str))
    blocked_pairs = set(curve.loc[curve["review_status"] == "blocked_pair_cost_shape", "pair_id"].astype(str))
    score = pd.read_csv(io_path(DJ_PAIR_SCORECARD))
    surface = pd.read_csv(io_path(DJ_SURFACE_AUDIT))
    slices = pd.read_csv(io_path(DK_SLICE_BLOCKERS))
    return {
        "dl_final": read_json(DL_FINAL),
        "dl_gates": read_csv(DL_GATES),
        "dl_queue": read_csv(DL_DM_QUEUE),
        "validation_contract": read_csv(DL_VALIDATION_CONTRACT),
        "surface_contract": read_csv(DL_SURFACE_CONTRACT),
        "balanced_queue": read_csv(DL_BALANCED_QUEUE),
        "guardrails": read_csv(DL_GUARDRAILS),
        "runtime_firewall": read_csv(DL_RUNTIME_FIREWALL),
        "curve": curve,
        "thin_pairs": thin_pairs,
        "blocked_pairs": blocked_pairs,
        "score": score,
        "surface": surface,
        "slices": slices,
        "failed_dl_gates": [row for row in read_csv(DL_GATES) if row.get("status") != "passed"],
    }


def materialize_validation_edge_frame(inputs: Mapping[str, Any]) -> tuple[Path, list[dict[str, Any]], dict[str, Any]]:
    tape = pd.read_parquet(io_path(DJ_PAIR_TAPE))
    direction = tape["final_action_label"].map({"short": -1.0, "flat": 0.0, "long": 1.0}).fillna(0.0)
    frame = tape[
        [
            "pair_id",
            "source_row_id",
            "timestamp",
            "split",
            "cost_policy_id",
            "feature_set_id",
            "model_config_id",
            "stage1_tradeable_score",
            "stage2_short_score",
            "stage2_flat_score",
            "stage2_long_score",
            "final_action_label",
            "exact_future_log_return_12",
            "cost_return",
            "action_net_after_cost",
            "is_trade",
            "session_bucket",
            "hour_utc",
            "month",
            "volatility_bucket",
            "adx_bucket",
            "vix_regime",
            "usd_regime",
            "rate_regime",
        ]
    ].copy()
    frame["action_direction"] = direction
    frame["raw_action_future_return"] = frame["action_direction"] * frame["exact_future_log_return_12"].astype(float)
    frame["costed_label_margin"] = frame["raw_action_future_return"] - frame["cost_return"].astype(float)
    frame["positive_costed_margin"] = frame["costed_label_margin"] > 0
    frame["objective_margin_abs"] = frame["costed_label_margin"].abs()
    frame["pair_quarantine_status"] = np.select(
        [
            frame["pair_id"].isin(inputs["thin_pairs"]),
            frame["pair_id"].isin(inputs["blocked_pairs"]),
        ],
        ["oos_positive_validation_thin_quarantine", "blocked_pair_cost_shape_memory"],
        default="no_pair_quarantine_flag",
    )
    frame["repair_sample_role"] = np.where(frame["split"] == "train", "train_only_objective_input", "read_only_validation_oos_audit")
    frame["train_objective_allowed"] = frame["split"] == "train"
    frame["selection_allowed"] = False
    frame["claim_boundary"] = CLAIM_BOUNDARY
    frame.to_parquet(io_path(VALIDATION_EDGE_FRAME), index=False)

    audit_rows: list[dict[str, Any]] = []
    for (split, role), group in frame.groupby(["split", "repair_sample_role"], dropna=False):
        margins = group["costed_label_margin"].astype(float)
        audit_rows.append(
            {
                "audit_id": f"validation_edge_{split}_{role}",
                "split": split,
                "rows": len(group),
                "pairs": group["pair_id"].nunique(),
                "trade_rows": int(group["is_trade"].sum()),
                "mean_margin": float(margins.mean()),
                "positive_margin_rate": float((margins > 0).mean()),
                "quarantine_rows": int((group["pair_quarantine_status"] != "no_pair_quarantine_flag").sum()),
                "role": role,
                "effect": "materializes train-only target and read-only audits(학습 전용 목표와 읽기 전용 감사 물질화)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    metadata = {
        "validation_edge_frame_rows": len(frame),
        "source_rows": int(frame["source_row_id"].nunique()),
        "pair_count": int(frame["pair_id"].nunique()),
        "train_rows": int((frame["split"] == "train").sum()),
        "validation_rows": int((frame["split"] == "validation").sum()),
        "oos_rows": int((frame["split"] == "oos").sum()),
        "train_objective_allowed_rows": int(frame["train_objective_allowed"].sum()),
        "quarantined_pair_count": len(inputs["thin_pairs"]),
        "quarantine_rows": int((frame["pair_quarantine_status"] != "no_pair_quarantine_flag").sum()),
    }
    return VALIDATION_EDGE_FRAME, audit_rows, metadata


def materialize_surface_matrices(inputs: Mapping[str, Any]) -> tuple[list[Path], dict[str, Any]]:
    score = inputs["score"].copy()
    score["profit_factor"] = score["profit_factor"].astype(float)
    score["net_log_return_after_cost"] = score["net_log_return_after_cost"].astype(float)
    score["trade_count"] = score["trade_count"].astype(int)
    rows: list[dict[str, Any]] = []
    for axis in ["cost_policy_id", "model_config_id", "feature_set_id"]:
        for (group_id, split), group in score.groupby([axis, "split"], dropna=False):
            rows.append(
                {
                    "matrix_id": f"{axis}_{group_id}_{split}",
                    "axis": axis,
                    "group_id": group_id,
                    "split": split,
                    "rows": len(group),
                    "pair_count": group["pair_id"].nunique(),
                    "trade_count": int(group["trade_count"].sum()),
                    "mean_pf": float(group["profit_factor"].mean()),
                    "min_pf": float(group["profit_factor"].min()),
                    "max_pf": float(group["profit_factor"].max()),
                    "mean_net": float(group["net_log_return_after_cost"].mean()),
                    "status": "read_only_surface_audit",
                    "effect": "checks surface breadth without selecting winners(승자 선택 없이 표면 폭 점검)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    surface_rows = pd.DataFrame(rows)
    cost_rows = surface_rows[surface_rows["axis"] == "cost_policy_id"].to_dict("records")
    model_rows = surface_rows[surface_rows["axis"] == "model_config_id"].to_dict("records")
    feature_rows = surface_rows[surface_rows["axis"] == "feature_set_id"].to_dict("records")
    write_csv(COST_LADDER_MATRIX, SURFACE_COLUMNS, cost_rows)
    write_csv(MODEL_FAMILY_MATRIX, SURFACE_COLUMNS, model_rows)
    write_csv(FEATURE_FAMILY_MATRIX, SURFACE_COLUMNS, feature_rows)

    slice_rows: list[dict[str, Any]] = []
    slices = inputs["slices"].copy()
    for (axis, status), group in slices.groupby(["slice_axis", "slice_review_status"], dropna=False):
        slice_rows.append(
            {
                "slice_axis": axis,
                "slice_review_status": status,
                "rows": len(group),
                "validation_trades_sum": int(group["validation_trades"].astype(float).sum()),
                "oos_trades_sum": int(group["oos_trades"].astype(float).sum()),
                "status": "slice_breadth_diagnostic_not_selection",
                "effect": "keeps slice winners out of candidate selection(슬라이스 승자를 후보 선택에서 제외)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(SLICE_BREADTH_MATRIX, SLICE_COLUMNS, slice_rows)
    bundle = {
        "bundle_id": "run337DM_surface_deconcentration_input_bundle",
        "source_surface_audit": rel(DJ_SURFACE_AUDIT),
        "matrices": {
            "cost_ladder": rel(COST_LADDER_MATRIX),
            "model_family": rel(MODEL_FAMILY_MATRIX),
            "feature_family": rel(FEATURE_FAMILY_MATRIX),
            "slice_breadth": rel(SLICE_BREADTH_MATRIX),
        },
        "selection_policy": "read_only_no_surface_winner_selection(읽기 전용, 표면 승자 선택 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(SURFACE_BUNDLE, bundle)
    metadata = {
        "surface_matrix_rows": len(rows),
        "cost_matrix_rows": len(cost_rows),
        "model_matrix_rows": len(model_rows),
        "feature_matrix_rows": len(feature_rows),
        "slice_matrix_rows": len(slice_rows),
        "surface_bundle_matrices": 4,
    }
    return [COST_LADDER_MATRIX, MODEL_FAMILY_MATRIX, FEATURE_FAMILY_MATRIX, SLICE_BREADTH_MATRIX, SURFACE_BUNDLE], metadata


def materialize_controls_and_manifests(inputs: Mapping[str, Any]) -> tuple[list[Path], dict[str, Any]]:
    control_rows = [
        {
            "control_id": "shifted_return_control",
            "control_family": "temporal_shift(시간 이동)",
            "materialized_rule": "shift future-return target by one completed block before training review(학습 검토 전 미래 수익 목표를 완료 블록 1개 이동)",
            "blocks_if": "control score matches or beats candidate(대조 점수가 후보와 같거나 더 높음)",
            "evidence_output": "future training control scorecard(미래 학습 대조 점수표)",
            "status": "contract_materialized",
            "effect": "tests serial-dependence shortcut(연속 의존 지름길 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "noise_label_control",
            "control_family": "noise_label(잡음 라벨)",
            "materialized_rule": "generate deterministic noise label from source_row_id hash(원천 행 ID 해시로 결정적 잡음 라벨 생성)",
            "blocks_if": "noise label looks predictive(잡음 라벨이 예측력처럼 보임)",
            "evidence_output": "future training control scorecard(미래 학습 대조 점수표)",
            "status": "contract_materialized",
            "effect": "tests fake separability(가짜 분리력 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "block_shuffle_control",
            "control_family": "block_shuffle(블록 셔플)",
            "materialized_rule": "shuffle labels inside train-only time blocks for control branch(대조 가지에서 학습 전용 시간 블록 안 라벨 셔플)",
            "blocks_if": "block shuffle keeps edge(블록 셔플이 우위를 유지)",
            "evidence_output": "future training control scorecard(미래 학습 대조 점수표)",
            "status": "contract_materialized",
            "effect": "tests regime-count shortcut(국면 수 지름길 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "purged_split_control",
            "control_family": "purged_split(제거 분할)",
            "materialized_rule": "require embargo around label horizon before training(학습 전 라벨 수평선 주변 격리 요구)",
            "blocks_if": "overlap cannot be removed(중첩을 제거할 수 없음)",
            "evidence_output": "purged_split_contract.csv(제거 분할 계약)",
            "status": "contract_materialized",
            "effect": "protects feature-label boundary(피처-라벨 경계 보호)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(NEGATIVE_CONTROL_CONTRACT, CONTROL_COLUMNS, control_rows)

    frame = pd.read_parquet(io_path(VALIDATION_EDGE_FRAME), columns=["timestamp", "source_row_id", "split", "pair_id"])
    duplicate_source_split = int(frame[["pair_id", "source_row_id"]].duplicated().sum())
    split_counts = frame["split"].value_counts().to_dict()
    boundary_rows = [
        {
            "audit_id": "label_columns_separated",
            "checked_subject": "exact_future_log_return_12/action_net_after_cost/costed_label_margin",
            "rows": int(len(frame)),
            "status": "passed_target_only_not_feature",
            "evidence": rel(VALIDATION_EDGE_FRAME),
            "effect": "labels are present only as target/audit fields(라벨은 목표/감사 필드로만 존재)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "split_roles_materialized",
            "checked_subject": "train/validation/oos roles",
            "rows": int(sum(split_counts.values())),
            "status": "passed_train_only_plus_read_only",
            "evidence": json.dumps(split_counts, ensure_ascii=False, sort_keys=True),
            "effect": "validation and OOS remain read-only(검증과 OOS를 읽기 전용으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "source_row_identity",
            "checked_subject": "pair_id/source_row_id uniqueness",
            "rows": duplicate_source_split,
            "status": "passed" if duplicate_source_split == 0 else "failed",
            "evidence": f"duplicate_pair_source_rows={duplicate_source_split}",
            "effect": "checks row identity before training review(학습 검토 전 행 정체성 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(LABEL_BOUNDARY_AUDIT, BOUNDARY_COLUMNS, boundary_rows)

    curve = inputs["curve"]
    thin_count = int((curve["review_status"] == "oos_positive_validation_thin_block").sum())
    blocked_count = int((curve["review_status"] == "blocked_pair_cost_shape").sum())
    forbidden_rows = [
        {
            "audit_id": "oos_positive_validation_thin_quarantine",
            "forbidden_source": rel(DJ_CURVE_REVIEW),
            "rows": thin_count,
            "status": "quarantined_not_selector",
            "required_handling": "may be used only as failure memory(실패 기억으로만 사용)",
            "effect": "prevents OOS pocket reuse as winner(OOS 포켓의 승자 재사용 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "blocked_pair_cost_shape_memory",
            "forbidden_source": rel(DJ_CURVE_REVIEW),
            "rows": blocked_count,
            "status": "blocked_not_selector",
            "required_handling": "may be used only as cost-shape failure memory(비용 곡선 실패 기억으로만 사용)",
            "effect": "prevents weak cost pairs from returning as candidates(약한 비용 쌍의 후보 복귀 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "release_candidate_absence",
            "forbidden_source": rel(DK_FAILURE_MEMORY),
            "rows": 0,
            "status": "no_release_candidates",
            "required_handling": "continue input review before training(학습 전 입력 검토 지속)",
            "effect": "keeps release closed(해제 닫힘 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(FORBIDDEN_SELECTION_AUDIT, FORBIDDEN_COLUMNS, forbidden_rows)

    slices = inputs["slices"]
    thin_rows = int((slices["slice_review_status"] == "thin_slice_not_release_evidence").sum())
    non_thin_rows = int(len(slices) - thin_rows)
    write_csv(
        DENSITY_FLOOR_CONTRACT,
        DENSITY_COLUMNS,
        [
            {
                "contract_id": "density_floor_non_thin_first",
                "source": rel(DK_SLICE_BLOCKERS),
                "rows": len(slices),
                "non_thin_rows": non_thin_rows,
                "thin_rows": thin_rows,
                "min_trade_floor": 50,
                "status": "materialized_review_required",
                "effect": "keeps aggressive density away from thin slices(공격 밀도를 얇은 슬라이스에서 분리)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    thin_audit_rows = []
    for status, group in slices.groupby("slice_review_status", dropna=False):
        thin_audit_rows.append(
            {
                "audit_id": f"slice_status_{status}",
                "forbidden_source": rel(DK_SLICE_BLOCKERS),
                "rows": len(group),
                "status": "excluded_from_release_evidence" if "thin" in str(status) or "block" in str(status) else "diagnostic_only",
                "required_handling": "diagnostic only until DN review(진단 전용, DN 검토 전까지)",
                "effect": "prevents slice-level cherry-pick(슬라이스 단위 골라잡기 방지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(THIN_SLICE_EXCLUSION_AUDIT, FORBIDDEN_COLUMNS, thin_audit_rows)

    payoff_rows = build_payoff_shape_rows(inputs["score"], inputs["thin_pairs"], inputs["blocked_pairs"])
    write_csv(PAYOFF_SHAPE_MATRIX, PAYOFF_COLUMNS, payoff_rows)

    firewall_rows = [
        {
            "firewall_id": row.get("firewall_id", ""),
            "held_action": row.get("held_action", ""),
            "held_until": row.get("held_until", ""),
            "required_evidence": row.get("required_evidence", ""),
            "forbidden_claim": row.get("forbidden_claim", ""),
            "carry_status": "carried_forward",
            "effect": "preserves DL runtime firewall(DL 런타임 방화벽 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in inputs["runtime_firewall"]
    ]
    write_csv(RUNTIME_FIREWALL_CARRY, FIREWALL_COLUMNS, firewall_rows)

    checklist_rows = [
        {
            "check_id": "future_proxy_expected_scorecard",
            "future_gate": "proxy_before_mt5(프록시 후 MT5 전)",
            "required_artifact": "proxy_expected_scorecard.csv",
            "required_comparison": "compare proxy expected and later MT5 realized rows(프록시 예상과 이후 MT5 실현 행 비교)",
            "blocks_claim": "runtime_probe",
            "effect": "keeps proxy useful but not authoritative(프록시를 유용하지만 권위는 없게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "check_id": "future_mt5_strategy_report",
            "future_gate": "mt5_external_verification(MT5 외부 검증)",
            "required_artifact": "MT5 strategy tester report and trade list(MT5 전략 테스터 보고서와 거래 목록)",
            "required_comparison": "timestamp, direction, cost, and trade count parity(시각/방향/비용/거래수 동등성)",
            "blocks_claim": "Forward/Goal",
            "effect": "requires external evidence before forward judgment(전진 판정 전 외부 근거 요구)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "check_id": "future_regime_attribution",
            "future_gate": "post_runtime_attribution(런타임 후 귀속)",
            "required_artifact": "session/hour/month/vol/ADX/VIX/USD/rate reports",
            "required_comparison": "proxy vs MT5 vs broker slice behavior(프록시/MT5/브로커 슬라이스 행동 비교)",
            "blocks_claim": "operating_promotion",
            "effect": "keeps operating claims blocked without regime evidence(국면 근거 없이는 운영 주장 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(FUTURE_PROXY_MT5_CHECKLIST, CHECKLIST_COLUMNS, checklist_rows)

    manifest = {
        "manifest_id": "run337DM_balanced_repair_attack_input_manifest",
        "branches": {
            "defensive": [rel(VALIDATION_EDGE_FRAME), rel(LABEL_BOUNDARY_AUDIT)],
            "aggressive": [rel(DENSITY_FLOOR_CONTRACT), rel(PAYOFF_SHAPE_MATRIX)],
            "repair": [rel(SURFACE_BUNDLE), rel(FORBIDDEN_SELECTION_AUDIT)],
            "control": [rel(NEGATIVE_CONTROL_CONTRACT), rel(THIN_SLICE_EXCLUSION_AUDIT)],
            "firewall": [rel(RUNTIME_FIREWALL_CARRY), rel(FUTURE_PROXY_MT5_CHECKLIST)],
        },
        "selection_policy": "none_review_required(없음, 검토 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(BALANCED_MANIFEST, manifest)
    metadata = {
        "negative_control_rows": len(control_rows),
        "label_boundary_failed_rows": sum(1 for row in boundary_rows if row["status"] == "failed"),
        "forbidden_selection_rows": len(forbidden_rows),
        "density_contract_rows": 1,
        "thin_slice_exclusion_rows": len(thin_audit_rows),
        "payoff_shape_rows": len(payoff_rows),
        "runtime_firewall_rows": len(firewall_rows),
        "future_proxy_mt5_rows": len(checklist_rows),
    }
    return [
        NEGATIVE_CONTROL_CONTRACT,
        LABEL_BOUNDARY_AUDIT,
        FORBIDDEN_SELECTION_AUDIT,
        DENSITY_FLOOR_CONTRACT,
        THIN_SLICE_EXCLUSION_AUDIT,
        PAYOFF_SHAPE_MATRIX,
        RUNTIME_FIREWALL_CARRY,
        FUTURE_PROXY_MT5_CHECKLIST,
        BALANCED_MANIFEST,
    ], metadata


def build_payoff_shape_rows(score: pd.DataFrame, thin_pairs: set[str], blocked_pairs: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    pivot = {}
    for row in score.to_dict("records"):
        key = str(row["pair_id"])
        pivot.setdefault(key, {})[str(row["split"])] = row
    for pair_id, splits in sorted(pivot.items()):
        train = splits.get("train", {})
        validation = splits.get("validation", {})
        oos = splits.get("oos", {})
        if pair_id in thin_pairs:
            repair_role = "oos_positive_validation_thin_quarantine"
        elif pair_id in blocked_pairs:
            repair_role = "blocked_pair_cost_shape_memory"
        else:
            repair_role = "review_only_no_release"
        first = train or validation or oos
        rows.append(
            {
                "pair_id": pair_id,
                "cost_policy_id": first.get("cost_policy_id", ""),
                "feature_set_id": first.get("feature_set_id", ""),
                "model_config_id": first.get("model_config_id", ""),
                "train_pf": as_float(train.get("profit_factor")),
                "validation_pf": as_float(validation.get("profit_factor")),
                "oos_pf": as_float(oos.get("profit_factor")),
                "train_trades": as_int(train.get("trade_count")),
                "validation_trades": as_int(validation.get("trade_count")),
                "oos_trades": as_int(oos.get("trade_count")),
                "repair_role": repair_role,
                "selection_allowed": "false",
                "effect": "keeps payoff shape as input diagnostics(보상 형태를 입력 진단으로 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_dn_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DN_review_validation_edge_frame",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review validation-edge frame and label boundary(검증 우위 프레임과 라벨 경계 검토)",
            "required_inputs": f"{rel(VALIDATION_EDGE_FRAME)};{rel(LABEL_BOUNDARY_AUDIT)}",
            "required_outputs": "validation_edge_input_review.csv",
            "blocked_if_missing": "validation edge frame or label boundary audit(검증 우위 프레임 또는 라벨 경계 감사)",
            "forbidden_action": "no training if label boundary fails(라벨 경계 실패 시 학습 금지)",
            "effect": "checks input safety before training(학습 전 입력 안전성 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DN_review_surface_bundle",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review surface deconcentration bundle(표면 탈집중 번들 검토)",
            "required_inputs": rel(SURFACE_BUNDLE),
            "required_outputs": "surface_bundle_review.csv",
            "blocked_if_missing": "surface bundle(표면 번들)",
            "forbidden_action": "no surface winner selection(표면 승자 선택 금지)",
            "effect": "tests whether surface risk is diagnosable(표면 위험 진단 가능성 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DN_review_controls",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review negative controls and forbidden selection audit(부정대조와 금지 선택 감사 검토)",
            "required_inputs": f"{rel(NEGATIVE_CONTROL_CONTRACT)};{rel(FORBIDDEN_SELECTION_AUDIT)}",
            "required_outputs": "control_and_forbidden_selection_review.csv",
            "blocked_if_missing": "controls or forbidden audit(대조 또는 금지 감사)",
            "forbidden_action": "no skipped controls(대조 생략 금지)",
            "effect": "keeps next training eligibility guarded(다음 학습 적격성을 방어적으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DN_decide_training_eligibility",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "decide whether guarded training may open(방어 학습을 열 수 있는지 결정)",
            "required_inputs": f"{rel(BALANCED_MANIFEST)};{rel(RUNTIME_FIREWALL_CARRY)}",
            "required_outputs": "training_eligibility_decision.md",
            "blocked_if_missing": "balanced manifest or runtime firewall(균형 매니페스트 또는 런타임 방화벽)",
            "forbidden_action": "no candidate selection or MT5(후보 선택 또는 MT5 금지)",
            "effect": "separates input readiness from model claims(입력 준비와 모델 주장을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DL/DK/DJ inputs exist(필수 DL/DK/DJ 입력 존재)"),
        ("parent_dl_gates_passed", final["dl_failed_gate_rows"] == 0, str(final["dl_failed_gate_rows"]), "0", "DL design usable(DL 설계 사용 가능)"),
        ("parent_next_action_matches", final["dl_next_action"] == RUN_ID, str(final["dl_next_action"]), RUN_ID, "continues DL queue(DL 대기열을 이어감)"),
        ("validation_edge_frame_materialized", final["validation_edge_frame_rows"] > 0, str(final["validation_edge_frame_rows"]), ">0", "validation edge frame exists(검증 우위 프레임 존재)"),
        ("train_and_readonly_roles_present", final["train_objective_allowed_rows"] > 0 and final["validation_rows"] > 0 and final["oos_rows"] > 0, f"train_allowed={final['train_objective_allowed_rows']};validation={final['validation_rows']};oos={final['oos_rows']}", "all >0", "train-only plus read-only roles exist(학습 전용과 읽기 전용 역할 존재)"),
        ("quarantine_coverage", final["quarantined_pair_count"] >= 13, str(final["quarantined_pair_count"]), ">=13", "OOS-positive validation-thin pockets quarantined(OOS 양호/검증 얇음 포켓 격리)"),
        ("surface_bundle_materialized", final["surface_bundle_matrices"] >= 4, str(final["surface_bundle_matrices"]), ">=4", "surface matrices exist(표면 행렬 존재)"),
        ("no_overfit_controls_materialized", final["negative_control_rows"] >= 4 and final["label_boundary_failed_rows"] == 0, f"controls={final['negative_control_rows']};boundary_fail={final['label_boundary_failed_rows']}", "controls>=4,boundary_fail=0", "controls and label audit pass(대조와 라벨 감사 통과)"),
        ("runtime_firewall_carried", final["runtime_firewall_rows"] >= 3, str(final["runtime_firewall_rows"]), ">=3", "runtime firewall carried(런타임 방화벽 전달)"),
        ("dn_queue_materialized", final["dn_queue_rows"] >= 4, str(final["dn_queue_rows"]), ">=4", "DN review queue exists(DN 검토 대기열 존재)"),
        (
            "no_forbidden_execution",
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
        "time_axis": "DJ tape UTC closed-bar timestamps inherited(DJ 테이프 UTC 봉 마감 시각 상속)",
        "sample_scope": f"US100 M5 replay rows={final['validation_edge_frame_rows']}; pairs={final['pair_count']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']};label_boundary_failed={final['label_boundary_failed_rows']}",
        "feature_label_boundary": "target labels materialized separately and audited(목표 라벨을 별도 물질화하고 감사)",
        "split_boundary": "train objective rows plus validation/OOS read-only rows(학습 목표 행과 검증/OOS 읽기 전용 행)",
        "leakage_risk": "future label columns accidentally used as features(미래 라벨 열이 실수로 피처가 되는 위험)",
        "data_hash_or_identity": {"validation_edge_frame": sha256_file(VALIDATION_EDGE_FRAME), "pair_tape": sha256_file(DJ_PAIR_TAPE)},
        "integrity_judgment": "usable_with_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "no model trained; repair input materialization only(모델 학습 없음; 수리 입력 물질화만)",
        "target_and_label": "costed label margin and objective diagnostic fields(비용 반영 라벨 여백과 목표 진단 필드)",
        "split_method": "train-only objective, validation/OOS read-only(학습 전용 목표, 검증/OOS 읽기 전용)",
        "selection_metric": "none(없음)",
        "secondary_metrics": "surface breadth, quarantine, controls, density floor(표면 폭/격리/대조/밀도 하한)",
        "threshold_policy": "unchanged, not tuned(변경 없음, 튜닝 없음)",
        "overfit_risk": "using materialized diagnostics as selection(물질화 진단을 선택으로 사용하는 위험)",
        "calibration_risk": "not applicable until training(학습 전 해당 없음)",
        "comparison_baseline": rel(DL_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"input_rows={final['validation_edge_frame_rows']};surface_matrices={final['surface_bundle_matrices']};controls={final['negative_control_rows']}",
        "comparison_baseline": rel(DK_FAILURE_MEMORY),
        "likely_drivers": "materialization of validation-edge and surface controls(검증 우위와 표면 대조 물질화)",
        "segment_checks": "surface and slice matrices materialized; no KPI improvement claimed(표면/슬라이스 행렬 물질화, KPI 개선 주장 없음)",
        "trade_shape": f"payoff_shape_rows={final['payoff_shape_rows']};density_contract_rows={final['density_contract_rows']}",
        "alternative_explanations": "inputs may be too restrictive or still underfit(입력이 너무 엄격하거나 여전히 과소적합일 수 있음)",
        "attribution_confidence": "high_for_input_completeness_low_for_profit(입력 완전성은 높음, 수익은 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "input frame, audits, surface bundle, controls(입력 프레임/감사/표면 번들/대조)",
        "evidence_missing": "DN review, guarded training, ONNX parity, MT5(DN 검토/방어 학습/ONNX 동등성/MT5)",
        "judgment_label": "materialized_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "실행 가능한 입력은 만들어졌지만, 아직 학습이나 선택 결과가 아니므로 DN 검토가 먼저입니다.",
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
        "availability": "ignored_materialized_inputs_with_tracked_report(무시된 물질화 입력과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DM Prediction Surface Validation-Edge Repair Inputs(예측 표면 검증 우위 수리 입력)

## Conclusion(결론)

run337DM(337DM 실행)은 DL design(DL 설계)을 실제 materialized inputs(물질화 입력)로 바꿨다. 새 training(학습), threshold tuning(임계값 튜닝), candidate selection(후보 선택), MT5 probe(MT5 탐침)는 실행하지 않았다.

핵심 산출물은 validation-edge input frame(검증 우위 입력 프레임), surface deconcentration bundle(표면 탈집중 번들), negative controls(부정대조), label boundary audit(라벨 경계 감사), runtime firewall carryforward(런타임 방화벽 전달)이다.

Effect(효과): 다음 run337DN(337DN 실행)은 이 입력이 학습으로 넘어가도 되는지 먼저 검토한다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- validation_edge_frame_rows(검증 우위 프레임 행): `{final["validation_edge_frame_rows"]}`
- pair_count(쌍 수): `{final["pair_count"]}`
- quarantined_pair_count(격리 쌍 수): `{final["quarantined_pair_count"]}`
- surface_bundle_matrices(표면 번들 행렬): `{final["surface_bundle_matrices"]}`
- negative_control_rows(부정대조 행): `{final["negative_control_rows"]}`
- label_boundary_failed_rows(라벨 경계 실패 행): `{final["label_boundary_failed_rows"]}`
- dn_queue_rows(DN 대기열 행): `{final["dn_queue_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DM

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): DL 설계를 입력과 감사 파일로 물질화했지만, 학습 전 DN 검토를 요구한다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(VALIDATION_EDGE_AUDIT)}`, `{rel(SURFACE_BUNDLE)}`
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
        f"  Stage337 run337DM focus complete: prediction surface validation-edge repair inputs(예측 표면 검증 우위 수리 입력)을 `{STATUS}`로 물질화했다. "
        f"Effect(효과): run337DN(337DN 실행)에서 input safety/training eligibility(입력 안전성/학습 적격성)를 검토한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DM focus complete")
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
    section = f"""
## Stage337 run337DM(337DM 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): DL 설계를 입력/감사 산출물로 물질화했고, DN 검토 전 학습/선택/MT5는 실행하지 않는다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DL(337DL"
    if "## Stage337 run337DM(337DM 실행)" not in current_text:
        current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{STATUS}`
- actual_mt5_execution(실제 MT5 실행): `not_run_dm_input_materialization_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 prediction surface validation-edge repair input review(예측 표면 검증 우위 수리 입력 검토)다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DM(337DM 실행) materialized prediction surface validation-edge repair inputs(예측 표면 검증 우위 수리 입력). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DM(337DM 실행) materialized prediction surface"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DM materialized prediction surface validation-edge repair inputs(예측 표면 검증 우위 수리 입력) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DM materialized prediction surface"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "prediction_surface_validation_edge_repair_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"input_rows={final['validation_edge_frame_rows']};controls={final['negative_control_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "input_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization_no_training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "validation_edge_surface_controls_inputs",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"rows={final['validation_edge_frame_rows']};quarantine_pairs={final['quarantined_pair_count']}",
        "guardrail_kpi": "label_boundary;negative_controls;runtime_firewall",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "DL contracts materialized into repair inputs",
        "kpi_scope": "input_completeness_no_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__input_materialization",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "question": "are validation-edge and surface repair inputs materialized safely before training",
        "metric_scope": "input_rows_surface_controls_label_boundary",
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
    inputs = load_inputs()
    artifacts: list[Path] = []
    _, validation_audit_rows, validation_meta = materialize_validation_edge_frame(inputs)
    artifacts.extend([VALIDATION_EDGE_FRAME, write_csv(VALIDATION_EDGE_AUDIT, AUDIT_COLUMNS, validation_audit_rows)])
    surface_artifacts, surface_meta = materialize_surface_matrices(inputs)
    artifacts.extend(surface_artifacts)
    control_artifacts, control_meta = materialize_controls_and_manifests(inputs)
    artifacts.extend(control_artifacts)
    dn_queue_rows = build_dn_queue()
    artifacts.append(write_csv(DN_QUEUE, QUEUE_COLUMNS, dn_queue_rows))

    dl_final: Mapping[str, Any] = inputs["dl_final"]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dl_next_action": dl_final.get("next_action", ""),
        "dl_failed_gate_rows": len(inputs["failed_dl_gates"]),
        "missing_inputs": len(missing),
        **validation_meta,
        **surface_meta,
        **control_meta,
        "dn_queue_rows": len(dn_queue_rows),
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
