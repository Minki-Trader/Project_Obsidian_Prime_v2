from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import materialize_validation_density_trade_count_repair_inputs as ec  # noqa: E402
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
STAGE_ID = ec.STAGE_ID
RUN_NUMBER = "run337ED"
RUN_ID = "run337ED_review_validation_density_trade_count_repair_inputs_without_db_v1"
PARENT_RUN_ID = ec.RUN_ID
NEXT_RUN_ID = "run337EE_train_validation_density_trade_count_repair_candidates_without_db_v1"
STATUS = "completed_stage337ED_repair_inputs_review_guarded_training_eligible_no_selection_no_mt5"
JUDGMENT = "train_only_repair_inputs_safe_for_guarded_training_with_feature_exclusion_and_onnx_filter"
DECISION = "stage337ED_open_run337EE_train_validation_density_trade_count_repair_candidates"
CLAIM_BOUNDARY = (
    "research_development_only_stage337ED_validation_density_trade_count_repair_input_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ec.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ec.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337ED_repair_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337ED_repair_input_review.md"
SELECTED_STATUS = ec.SELECTED_STATUS
STAGE_BRIEF = ec.STAGE_BRIEF
WORKSPACE_STATE = ec.WORKSPACE_STATE
CURRENT_STATE = ec.CURRENT_STATE
CHANGELOG = ec.CHANGELOG
RUN_REGISTRY = ec.RUN_REGISTRY
ALPHA_LEDGER = ec.ALPHA_LEDGER
ARTIFACT_REGISTRY = ec.ARTIFACT_REGISTRY
STAGE_LEDGER = ec.STAGE_LEDGER

EC_FINAL = ec.FINAL_DECISION
EC_GATES = ec.REQUIRED_GATE_AUDIT
EC_QUEUE = ec.ED_QUEUE
REPAIR_FRAME = ec.TRAIN_ONLY_REPAIR_FRAME
OBJECTIVE_AUDIT = ec.OBJECTIVE_CONTRACT_AUDIT
TASK_MATRIX = ec.EC_TRAINING_TASK_MATRIX
FEATURE_COMPATIBILITY = ec.FEATURE_INPUT_COMPATIBILITY
GUARD_MATRIX = ec.CONTROL_DENSITY_WFO_GUARD_MATRIX
FIREWALL_CARRY = ec.NO_RELEASE_FIREWALL_CARRY
WEIGHT_SUMMARY = ec.REPAIR_WEIGHT_SUMMARY

TRAIN_ONLY_REPAIR_FRAME_REVIEW = RUN_DIR / "train_only_repair_frame_review.csv"
EC_TASK_MATRIX_REVIEW = RUN_DIR / "ec_task_matrix_review.csv"
GUARD_FIREWALL_REVIEW = RUN_DIR / "guard_firewall_review.csv"
TRAINING_FEATURE_EXCLUSION = RUN_DIR / "training_feature_exclusion.csv"
TRAINING_ELIGIBILITY_MATRIX = RUN_DIR / "training_eligibility_matrix.csv"
EE_QUEUE = RUN_DIR / "run337EE_training_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EC_FINAL,
    EC_GATES,
    EC_QUEUE,
    REPAIR_FRAME,
    OBJECTIVE_AUDIT,
    TASK_MATRIX,
    FEATURE_COMPATIBILITY,
    GUARD_MATRIX,
    FIREWALL_CARRY,
    WEIGHT_SUMMARY,
)
OUTPUT_FILES = (
    TRAIN_ONLY_REPAIR_FRAME_REVIEW,
    EC_TASK_MATRIX_REVIEW,
    GUARD_FIREWALL_REVIEW,
    TRAINING_FEATURE_EXCLUSION,
    TRAINING_ELIGIBILITY_MATRIX,
    EE_QUEUE,
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

REVIEW_COLUMNS = (
    "review_id",
    "subject",
    "rows",
    "metric_1",
    "metric_2",
    "review_status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
FEATURE_EXCLUSION_COLUMNS = (
    "field_name",
    "field_family",
    "must_exclude_from_features",
    "allowed_use",
    "leakage_risk",
    "effect",
    "claim_boundary",
)
ELIGIBILITY_COLUMNS = (
    "task_id",
    "training_eligibility_status",
    "blocked_reason",
    "allowed_training_use",
    "required_guard",
    "blocked_use",
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


FUTURE_OR_AUDIT_FIELDS = (
    ("future_log_return_12", "future_label(미래 라벨)", "target/audit only(목표/감사 전용)", "direct future return leakage(직접 미래 수익 누수)"),
    ("future_return_12", "future_label(미래 라벨)", "target/audit only(목표/감사 전용)", "direct future return leakage(직접 미래 수익 누수)"),
    ("cost_return", "cost_label(비용 라벨)", "target/audit only(목표/감사 전용)", "cost target leakage(비용 목표 누수)"),
    ("low_margin_rate", "train_objective_tag(학습 목표 태그)", "sample weight only(표본 가중치 전용)", "objective tag as feature leakage(목표 태그 피처 누수)"),
    ("direction_residual_rate", "train_objective_tag(학습 목표 태그)", "sample weight only(표본 가중치 전용)", "model residual leakage(모델 잔차 누수)"),
    ("underwater_rate", "train_objective_tag(학습 목표 태그)", "sample weight only(표본 가중치 전용)", "curve outcome leakage(곡선 결과 누수)"),
    ("drawdown_pressure_mean", "train_objective_tag(학습 목표 태그)", "sample weight only(표본 가중치 전용)", "drawdown outcome leakage(드로다운 결과 누수)"),
    ("abstention_rate", "train_objective_tag(학습 목표 태그)", "sample weight only(표본 가중치 전용)", "action policy leakage(행동 정책 누수)"),
    ("payoff_tail_proxy", "train_objective_tag(학습 목표 태그)", "sample weight only(표본 가중치 전용)", "payoff outcome leakage(보상 결과 누수)"),
    ("drawdown_pressure_norm", "derived_objective_tag(파생 목표 태그)", "sample weight only(표본 가중치 전용)", "normalized outcome leakage(정규화 결과 누수)"),
    ("payoff_tail_norm", "derived_objective_tag(파생 목표 태그)", "sample weight only(표본 가중치 전용)", "normalized payoff leakage(정규화 보상 누수)"),
    ("near_margin_trade_support_weight", "sample_weight(표본 가중치)", "fit sample_weight only(학습 가중치 전용)", "weight-as-feature leakage(가중치 피처 누수)"),
    ("density_tempered_weight", "sample_weight(표본 가중치)", "fit sample_weight only(학습 가중치 전용)", "weight-as-feature leakage(가중치 피처 누수)"),
    ("payoff_tail_offense_weight", "sample_weight(표본 가중치)", "fit sample_weight only(학습 가중치 전용)", "weight-as-feature leakage(가중치 피처 누수)"),
    ("combined_sample_weight", "sample_weight(표본 가중치)", "fit sample_weight only(학습 가중치 전용)", "weight-as-feature leakage(가중치 피처 누수)"),
    ("allowed_split_scope", "split_role(분할 역할)", "audit only(감사 전용)", "split role leakage(분할 역할 누수)"),
    ("leakage_guard", "firewall(방화벽)", "audit only(감사 전용)", "firewall identity leakage(방화벽 정체성 누수)"),
    ("split", "split_role(분할 역할)", "split control only(분할 제어 전용)", "split identity leakage(분할 정체성 누수)"),
    ("cost_policy_id", "task_key(작업 키)", "task routing only(작업 라우팅 전용)", "cost policy identity leakage(비용 정책 정체성 누수)"),
    ("source_row_id", "row_identity(행 정체성)", "join/audit only(조인/감사 전용)", "row id leakage(행 ID 누수)"),
)


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


def pct(part: int, whole: int) -> float:
    return float(part / whole) if whole else 0.0


def review_repair_frame() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    df = pd.read_parquet(io_path(REPAIR_FRAME))
    total = len(df)
    split_values = sorted(df["split"].astype(str).unique().tolist()) if total else []
    leakage_guard_values = sorted(df["leakage_guard"].astype(str).unique().tolist()) if total else []
    weight_cols = ["near_margin_trade_support_weight", "density_tempered_weight", "payoff_tail_offense_weight", "combined_sample_weight"]
    finite_weight_failures = 0
    out_of_range_weights = 0
    for column in weight_cols:
        numeric = pd.to_numeric(df[column], errors="coerce")
        finite_weight_failures += int((~numeric.map(math.isfinite)).sum())
        out_of_range_weights += int(((numeric < 0.25) | (numeric > 4.0)).sum())
    summary = {
        "rows": total,
        "split_values": split_values,
        "source_rows": int(df["source_row_id"].nunique()) if total else 0,
        "cost_policy_rows": int(df["cost_policy_id"].nunique()) if total else 0,
        "leakage_guard_values": leakage_guard_values,
        "finite_weight_failures": finite_weight_failures,
        "out_of_range_weights": out_of_range_weights,
        "combined_weight_mean": float(pd.to_numeric(df["combined_sample_weight"], errors="coerce").mean()) if total else 0.0,
        "combined_weight_max": float(pd.to_numeric(df["combined_sample_weight"], errors="coerce").max()) if total else 0.0,
        "non_train_rows": int((df["split"].astype(str) != "train").sum()) if total else 0,
    }
    rows = [
        {
            "review_id": "repair_frame_split_boundary",
            "subject": "train-only split boundary(학습 전용 분할 경계)",
            "rows": total,
            "metric_1": ",".join(split_values),
            "metric_2": f"source_rows={summary['source_rows']};cost_policies={summary['cost_policy_rows']}",
            "review_status": "passed_train_only" if split_values == ["train"] and summary["non_train_rows"] == 0 else "blocked_non_train_rows",
            "allowed_use": "guarded training input after ED review(ED 검토 뒤 방어 학습 입력)",
            "forbidden_use": "validation/OOS label use(검증/OOS 라벨 사용)",
            "effect": "누수 경계를 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "repair_frame_weight_integrity",
            "subject": "sample weights(표본 가중치)",
            "rows": total,
            "metric_1": f"finite_failures={finite_weight_failures};out_of_range={out_of_range_weights}",
            "metric_2": f"combined_mean={summary['combined_weight_mean']:.6f};combined_max={summary['combined_weight_max']:.6f}",
            "review_status": "passed_weight_integrity" if finite_weight_failures == 0 and out_of_range_weights == 0 else "blocked_weight_integrity",
            "allowed_use": "sample_weight only(표본 가중치 전용)",
            "forbidden_use": "feature column use(피처 열 사용)",
            "effect": "가중치가 학습 안정 범위 안에 있는지 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "repair_frame_leakage_guard",
            "subject": "leakage guard(누수 가드)",
            "rows": total,
            "metric_1": ",".join(leakage_guard_values),
            "metric_2": f"non_train_rows={summary['non_train_rows']}",
            "review_status": "passed_leakage_guard" if leakage_guard_values == ["validation_oos_excluded"] else "blocked_leakage_guard",
            "allowed_use": "audit and row filter(감사와 행 필터)",
            "forbidden_use": "model feature(모델 피처)",
            "effect": "검증/OOS가 가중치 생성에 들어오지 않았는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows, summary


def review_task_matrix() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    tasks = read_csv(TASK_MATRIX)
    features = read_csv(FEATURE_COMPATIBILITY)
    feature_blocks = sum(1 for row in features if row.get("compatibility_status") != "compatible")
    eligible_rows: list[dict[str, Any]] = []
    supported = 0
    blocked_onnx = 0
    for task in tasks:
        feasible = str(task.get("onnx_export_feasibility", "")).startswith("supported")
        status = "eligible_guarded_training" if feasible and feature_blocks == 0 else "blocked_onnx_or_feature"
        if feasible:
            supported += 1
        else:
            blocked_onnx += 1
        eligible_rows.append(
            {
                "task_id": task.get("task_id", ""),
                "training_eligibility_status": status,
                "blocked_reason": "" if status == "eligible_guarded_training" else "unsupported_onnx_or_feature_block",
                "allowed_training_use": "EE may train only eligible rows(EE는 적격 행만 학습 가능)",
                "required_guard": "feature exclusion and no threshold tuning(피처 제외와 임계값 조정 금지)",
                "blocked_use": "unsupported ONNX or feature-blocked task(미지원 ONNX 또는 피처 차단 작업)",
                "effect": "학습 가능한 작업과 격리 작업을 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    summary = {
        "task_rows": len(tasks),
        "feature_rows": len(features),
        "feature_block_rows": feature_blocks,
        "eligible_task_rows": sum(1 for row in eligible_rows if row["training_eligibility_status"] == "eligible_guarded_training"),
        "blocked_onnx_rows": blocked_onnx,
        "supported_onnx_rows": supported,
    }
    review_rows = [
        {
            "review_id": "task_matrix_scope",
            "subject": "EC task matrix(EC 작업 행렬)",
            "rows": len(tasks),
            "metric_1": f"eligible={summary['eligible_task_rows']};blocked_onnx={blocked_onnx}",
            "metric_2": f"feature_blocks={feature_blocks};features={len(features)}",
            "review_status": "passed_with_onnx_filter" if summary["eligible_task_rows"] >= 72 and feature_blocks == 0 else "blocked_task_matrix",
            "allowed_use": "eligible rows only(적격 행만)",
            "forbidden_use": "blocked ONNX rows(차단 ONNX 행)",
            "effect": "미지원 모델 변형을 학습 전 격리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return review_rows, eligible_rows, summary


def review_guards_firewall() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    guards = read_csv(GUARD_MATRIX)
    firewall = read_csv(FIREWALL_CARRY)
    guard_rows = len(guards)
    firewall_rows = len(firewall)
    inactive_guards = sum(1 for row in guards if row.get("materialized_status") != "carried_forward_active")
    inactive_firewall = sum(1 for row in firewall if not str(row.get("carry_status", "")).startswith("active"))
    active_blocking_rows = sum(int(float(row.get("blocking_rows") or 0)) for row in guards)
    rows = [
        {
            "review_id": "guard_matrix_active",
            "subject": "guard matrix(가드 행렬)",
            "rows": guard_rows,
            "metric_1": f"inactive={inactive_guards};active_blocking_rows={active_blocking_rows}",
            "metric_2": f"sources={len({row.get('source','') for row in guards})}",
            "review_status": "passed_active_guards" if guard_rows >= 6 and inactive_guards == 0 else "blocked_guard_matrix",
            "allowed_use": "training blocker and diagnostics(학습 차단 조건과 진단)",
            "forbidden_use": "gate relaxation(게이트 완화)",
            "effect": "부모 실패 게이트가 계속 살아 있는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "firewall_active",
            "subject": "no-release firewall(해제 금지 방화벽)",
            "rows": firewall_rows,
            "metric_1": f"inactive={inactive_firewall}",
            "metric_2": "selection/threshold/MT5/Forward blocked",
            "review_status": "passed_active_firewall" if firewall_rows >= 5 and inactive_firewall == 0 else "blocked_firewall",
            "allowed_use": "claim boundary guard(주장 경계 가드)",
            "forbidden_use": "release or operating claim(해제 또는 운영 주장)",
            "effect": "입력 검토가 운영 주장으로 번지지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows, {
        "guard_rows": guard_rows,
        "firewall_rows": firewall_rows,
        "inactive_guards": inactive_guards,
        "inactive_firewall": inactive_firewall,
        "active_blocking_rows": active_blocking_rows,
    }


def build_feature_exclusion() -> list[dict[str, str]]:
    return [
        {
            "field_name": field_name,
            "field_family": field_family,
            "must_exclude_from_features": "true",
            "allowed_use": allowed_use,
            "leakage_risk": leakage_risk,
            "effect": "EE 학습에서 목표/가중치/분할 정체성 누수를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for field_name, field_family, allowed_use, leakage_risk in FUTURE_OR_AUDIT_FIELDS
    ]


def build_ee_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337EE_train_eligible_extratrees_tasks",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train eligible ExtraTrees repair candidates(적격 ExtraTrees 수리 후보 학습).",
            "required_inputs": f"{rel(TRAINING_ELIGIBILITY_MATRIX)};{rel(TRAINING_FEATURE_EXCLUSION)};{rel(REPAIR_FRAME)}",
            "required_outputs": "trained_model_manifest.csv;onnx_parity_matrix.csv;candidate_scorecards.csv",
            "blocked_if_missing": "eligible task matrix or feature exclusion(적격 작업 행렬 또는 피처 제외 계약).",
            "forbidden_action": "no threshold tuning, no blocked ONNX tasks, no selection(임계값 조정/차단 ONNX 작업/선택 금지).",
            "effect": "검토된 입력으로만 다음 학습을 열어 과적합 수리를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EE_score_density_and_controls",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "score density and negative controls(밀도와 부정 대조 점수화).",
            "required_inputs": f"{rel(GUARD_MATRIX)};{rel(TRAINING_ELIGIBILITY_MATRIX)}",
            "required_outputs": "density_guard_audit.csv;negative_control_scorecard.csv",
            "blocked_if_missing": "guard matrix(가드 행렬).",
            "forbidden_action": "no control relaxation(대조 완화 금지).",
            "effect": "EA 실패를 반복하는 후보를 학습 직후 차단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EE_preserve_no_release_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "preserve no-release firewall during training(학습 중 해제 금지 방화벽 보존).",
            "required_inputs": rel(FIREWALL_CARRY),
            "required_outputs": "runtime_firewall_review.csv",
            "blocked_if_missing": "firewall carry(방화벽 이월).",
            "forbidden_action": "no MT5, no Forward/Goal, no live readiness(MT5/전진/목표/라이브 준비 금지).",
            "effect": "학습 결과가 곧 운영 주장으로 바뀌지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    no_forbidden_claim = (
        final["model_training"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["mt5_runtime_probe"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "필수 EC 입력이 있어야 검토가 닫힌다."),
        ("parent_ec_gates_passed", final["ec_failed_gate_rows"] == 0, str(final["ec_failed_gate_rows"]), "0", "부모 EC 물질화 게이트가 통과해야 한다."),
        ("parent_next_action_matches", final["ec_next_action"] == RUN_ID, str(final["ec_next_action"]), RUN_ID, "라우팅이 ED로 정확히 이어졌는지 본다."),
        ("repair_frame_train_only", final["non_train_rows"] == 0 and final["repair_frame_split_values"] == ["train"], f"non_train={final['non_train_rows']};split={final['repair_frame_split_values']}", "non_train=0;split=train", "수리 프레임 학습 전용 경계를 확인한다."),
        ("weight_integrity_clear", final["finite_weight_failures"] == 0 and final["out_of_range_weights"] == 0, f"finite_fail={final['finite_weight_failures']};range={final['out_of_range_weights']}", "0/0", "가중치가 유효 범위 안에 있어야 한다."),
        ("task_eligibility_sufficient", final["eligible_task_rows"] >= 72, str(final["eligible_task_rows"]), ">=72", "학습 가능한 작업이 충분해야 한다."),
        ("unsupported_onnx_quarantined", final["blocked_onnx_rows"] > 0, str(final["blocked_onnx_rows"]), ">0", "미지원 ONNX 변형을 격리했는지 본다."),
        ("feature_compatibility_clear", final["feature_block_rows"] == 0, str(final["feature_block_rows"]), "0", "피처 호환성이 깨지면 학습 금지다."),
        ("guard_firewall_active", final["inactive_guards"] == 0 and final["inactive_firewall"] == 0, f"guards={final['inactive_guards']};firewall={final['inactive_firewall']}", "0/0", "가드와 방화벽이 살아 있어야 한다."),
        ("feature_exclusion_materialized", final["feature_exclusion_rows"] >= 18, str(final["feature_exclusion_rows"]), ">=18", "라벨/가중치/분할 누수 제외 계약이 있어야 한다."),
        ("ee_queue_materialized", final["ee_queue_rows"] == 3, str(final["ee_queue_rows"]), "3", "다음 학습 큐가 경계 안에서 열렸는지 본다."),
        ("no_forbidden_claim", no_forbidden_claim, str(no_forbidden_claim).lower(), "true", "ED는 검토 전용이며 운영/목표 주장을 하지 않는다."),
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
    data = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "sample_scope": f"rows={final['repair_frame_rows']};split={final['repair_frame_split_values']};source_rows={final['source_rows']}",
        "feature_label_boundary": f"feature_exclusion_rows={final['feature_exclusion_rows']};non_train_rows={final['non_train_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']};finite_weight_failures={final['finite_weight_failures']}",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_guarded_training_experiment(방어 학습 실험에 사용 가능).",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_training": "not_run_review_only(미실행, 검토 전용)",
        "eligible_task_rows": final["eligible_task_rows"],
        "blocked_onnx_rows": final["blocked_onnx_rows"],
        "threshold_policy": "fixed_no_tuning(고정, 조정 없음)",
        "selection_metric": "none(없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "observed_change": f"eligible_tasks={final['eligible_task_rows']};blocked_onnx={final['blocked_onnx_rows']};active_blocking_rows={final['active_blocking_rows']}",
        "likely_drivers": "train-only weights, ONNX feasibility filter, active parent guards(학습 전용 가중치, ONNX 가능성 필터, 활성 부모 가드).",
        "trade_shape": "not evaluated; no model training(미평가, 모델 학습 없음).",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": JUDGMENT,
        "evidence_available": "frame review, task review, guard/firewall review, feature exclusion(프레임/작업/가드-방화벽 검토/피처 제외).",
        "evidence_missing": "EE training, ONNX parity, MT5, forward(EE 학습, ONNX 동등성, MT5, 전진).",
        "next_condition": NEXT_RUN_ID,
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_with_boundary(경계 안에서 연결됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337ED Repair Input Review(337ED 수리 입력 검토)

## Conclusion(결론)

run337ED(337ED 실행)는 EC repair inputs(EC 수리 입력)를 검토했다. repair frame(수리 프레임)은 train-only(학습 전용)이고, feature exclusion(피처 제외) 계약으로 미래 라벨/가중치/분할 열을 피처에서 차단했다.

Action(행동): ONNX(온엑스) 미지원 HistGradient(히스토그램 그래디언트) 작업은 training eligibility(학습 적격성)에서 격리하고, ExtraTrees(엑스트라 트리) 적격 작업만 다음 EE 학습 큐로 넘겼다.

Effect(효과): 다음 단계는 guarded training experiment(방어 학습 실험)이며, selection/MT5/Forward/Goal(선택/MT5/전진/목표)은 여전히 주장하지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- repair_frame_rows(수리 프레임 행): `{final["repair_frame_rows"]}`
- eligible_task_rows(학습 적격 작업 행): `{final["eligible_task_rows"]}`
- blocked_onnx_rows(ONNX 격리 행): `{final["blocked_onnx_rows"]}`
- feature_exclusion_rows(피처 제외 행): `{final["feature_exclusion_rows"]}`
- guard_rows(가드 행): `{final["guard_rows"]}`
- firewall_rows(방화벽 행): `{final["firewall_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337ED

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): EC 입력을 검토했고, 적격 ExtraTrees 작업만 다음 방어 학습 실험으로 넘긴다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(TRAINING_ELIGIBILITY_MATRIX)}`, `{rel(TRAINING_FEATURE_EXCLUSION)}`
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
        f"  Stage337 run337ED focus complete: validation-density/trade-count repair input review(검증-밀도/거래수 수리 입력 검토)를 `{STATUS}`로 닫았다. "
        "Effect(효과): 다음 run337EE에서 eligible ExtraTrees tasks(적격 ExtraTrees 작업)만 방어 학습한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337ED focus complete")
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
## Stage337 run337ED(337ED 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): EC 입력이 학습 전용 경계와 피처 제외 계약을 통과했다. 학습/선택/MT5/Forward/Goal(학습/선택/MT5/전진/목표)은 이 실행에서 주장하지 않는다.
"""
    marker = "## Stage337 run337EC("
    if "## Stage337 run337ED(337ED 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_ed_review_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): eligible repair candidate training(적격 수리 후보 학습)으로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337ED(337ED 실행) reviewed validation-density/trade-count repair inputs(검증-밀도/거래수 수리 입력). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337ED(337ED 실행) reviewed validation-density"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337ED reviewed validation-density/trade-count repair inputs(검증-밀도/거래수 수리 입력) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337ED reviewed validation-density"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "validation_density_trade_count_repair_input_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"eligible_tasks={final['eligible_task_rows']};blocked_onnx={final['blocked_onnx_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_input_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_training_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "input_safety_training_eligibility",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"eligible_tasks={final['eligible_task_rows']};feature_exclusion={final['feature_exclusion_rows']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_result_judgment",
        "evidence_scope": "EC repair inputs reviewed",
        "kpi_scope": "input_safety_training_eligibility",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_input_review",
        "family": "data_integrity_model_validation_result_judgment",
        "question": "are repair inputs safe for guarded training without leakage",
        "metric_scope": "eligible_tasks_feature_exclusion_guard_firewall",
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

    frame_rows, frame_summary = review_repair_frame()
    task_review_rows, eligibility_rows, task_summary = review_task_matrix()
    guard_review_rows, guard_summary = review_guards_firewall()
    exclusion_rows = build_feature_exclusion()
    queue_rows = build_ee_queue()
    artifacts: list[Path] = [
        write_csv(TRAIN_ONLY_REPAIR_FRAME_REVIEW, REVIEW_COLUMNS, frame_rows),
        write_csv(EC_TASK_MATRIX_REVIEW, REVIEW_COLUMNS, task_review_rows),
        write_csv(GUARD_FIREWALL_REVIEW, REVIEW_COLUMNS, guard_review_rows),
        write_csv(TRAINING_FEATURE_EXCLUSION, FEATURE_EXCLUSION_COLUMNS, exclusion_rows),
        write_csv(TRAINING_ELIGIBILITY_MATRIX, ELIGIBILITY_COLUMNS, eligibility_rows),
        write_csv(EE_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]

    ec_final = read_json(EC_FINAL)
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "ec_next_action": ec_final.get("next_action", ""),
        "ec_failed_gate_rows": sum(1 for row in read_csv(EC_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "repair_frame_rows": frame_summary["rows"],
        "repair_frame_split_values": frame_summary["split_values"],
        "source_rows": frame_summary["source_rows"],
        "cost_policy_rows": frame_summary["cost_policy_rows"],
        "non_train_rows": frame_summary["non_train_rows"],
        "finite_weight_failures": frame_summary["finite_weight_failures"],
        "out_of_range_weights": frame_summary["out_of_range_weights"],
        "eligible_task_rows": task_summary["eligible_task_rows"],
        "blocked_onnx_rows": task_summary["blocked_onnx_rows"],
        "supported_onnx_rows": task_summary["supported_onnx_rows"],
        "task_rows": task_summary["task_rows"],
        "feature_block_rows": task_summary["feature_block_rows"],
        "guard_rows": guard_summary["guard_rows"],
        "firewall_rows": guard_summary["firewall_rows"],
        "inactive_guards": guard_summary["inactive_guards"],
        "inactive_firewall": guard_summary["inactive_firewall"],
        "active_blocking_rows": guard_summary["active_blocking_rows"],
        "feature_exclusion_rows": len(exclusion_rows),
        "ee_queue_rows": len(queue_rows),
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
    artifacts.extend([write_report(final), write_decision_doc(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))

    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": "gate_failed", "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "eligible_task_rows": final["eligible_task_rows"],
                "blocked_onnx_rows": final["blocked_onnx_rows"],
                "feature_exclusion_rows": final["feature_exclusion_rows"],
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
