from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
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
STAGE_ID = du.STAGE_ID
RUN_NUMBER = "run337DV"
RUN_ID = "run337DV_review_broad_validation_failure_control_residual_materialization_without_db_v1"
PARENT_RUN_ID = du.RUN_ID
NEXT_RUN_ID = "run337DW_design_transfer_density_control_objective_repair_without_db_v1"
STATUS = "completed_stage337DV_broad_validation_materialization_review_transfer_density_control_blocks_no_training_no_selection"
JUDGMENT = "broad_validation_failure_reconfirmed_transfer_density_control_wfo_blocks_release"
DECISION = "stage337DV_open_run337DW_design_transfer_density_control_objective_repair"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DV_broad_validation_failure_control_residual_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = du.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = du.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DV_broad_validation_materialization_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DV_broad_validation_materialization_review.md"
SELECTED_STATUS = du.SELECTED_STATUS
STAGE_BRIEF = du.STAGE_BRIEF
WORKSPACE_STATE = du.WORKSPACE_STATE
CURRENT_STATE = du.CURRENT_STATE
CHANGELOG = du.CHANGELOG
RUN_REGISTRY = du.RUN_REGISTRY
ALPHA_LEDGER = du.ALPHA_LEDGER
ARTIFACT_REGISTRY = du.ARTIFACT_REGISTRY
STAGE_LEDGER = du.STAGE_LEDGER

DU_FINAL = du.FINAL_DECISION
DU_GATES = du.REQUIRED_GATE_AUDIT
DU_QUEUE = du.DV_QUEUE
TRANSFER_MATRIX = du.TRANSFER_MATRIX
DENSITY_DRAWDOWN_MATRIX = du.DENSITY_DRAWDOWN_MATRIX
CONTROL_ISOLATION_MATRIX = du.CONTROL_ISOLATION_MATRIX
FAMILY_SCOPE_MATRIX = du.FAMILY_SCOPE_MATRIX
FAILURE_MEMORY_UPDATE = du.FAILURE_MEMORY_UPDATE
NO_RELEASE_FIREWALL_CARRY = du.NO_RELEASE_FIREWALL_CARRY

TRANSFER_BREAK_REVIEW = RUN_DIR / "transfer_break_review.csv"
DENSITY_DRAWDOWN_REVIEW = RUN_DIR / "density_drawdown_pressure_review.csv"
CONTROL_ISOLATION_REVIEW = RUN_DIR / "control_isolation_review.csv"
FAMILY_MEMORY_FIREWALL_REVIEW = RUN_DIR / "family_memory_firewall_review.csv"
WFO_OBJECTIVE_PRECHECK_REVIEW = RUN_DIR / "wfo_objective_precheck_review.csv"
DW_QUEUE = RUN_DIR / "run337DW_repair_design_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DU_FINAL,
    DU_GATES,
    DU_QUEUE,
    TRANSFER_MATRIX,
    DENSITY_DRAWDOWN_MATRIX,
    CONTROL_ISOLATION_MATRIX,
    FAMILY_SCOPE_MATRIX,
    FAILURE_MEMORY_UPDATE,
    NO_RELEASE_FIREWALL_CARRY,
)
OUTPUT_FILES = (
    TRANSFER_BREAK_REVIEW,
    DENSITY_DRAWDOWN_REVIEW,
    CONTROL_ISOLATION_REVIEW,
    FAMILY_MEMORY_FIREWALL_REVIEW,
    WFO_OBJECTIVE_PRECHECK_REVIEW,
    DW_QUEUE,
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
    "review_id",
    "scope_axis",
    "scope_value",
    "rows",
    "validation_floor_block_rows",
    "train_validation_transfer_break_rows",
    "oos_only_lift_rows",
    "min_validation_pf",
    "max_validation_pf",
    "mean_validation_pf",
    "min_validation_net",
    "worst_model_id",
    "review_status",
    "effect",
    "claim_boundary",
)
DENSITY_COLUMNS = (
    "review_id",
    "split",
    "scope_axis",
    "scope_value",
    "rows",
    "high_density_rows",
    "drawdown_dominates_rows",
    "mean_signal_density",
    "max_drawdown",
    "min_recovery_factor",
    "worst_model_id",
    "review_status",
    "effect",
    "claim_boundary",
)
CONTROL_COLUMNS = (
    "review_id",
    "split",
    "control_id",
    "rows",
    "block_rows",
    "affected_model_count",
    "max_candidate_balanced_accuracy",
    "max_control_alignment_balanced_accuracy",
    "blocked_models",
    "review_status",
    "effect",
    "claim_boundary",
)
FAMILY_COLUMNS = (
    "review_id",
    "subject",
    "rows",
    "high_severity_rows",
    "blocking_rows",
    "observed_signature",
    "review_status",
    "effect",
    "claim_boundary",
)
WFO_COLUMNS = (
    "review_id",
    "check_subject",
    "input_status",
    "review_status",
    "required_next_design",
    "forbidden_action",
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


def as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def load_frames() -> dict[str, pd.DataFrame]:
    return {
        "transfer": pd.read_csv(io_path(TRANSFER_MATRIX)),
        "density": pd.read_csv(io_path(DENSITY_DRAWDOWN_MATRIX)),
        "control": pd.read_csv(io_path(CONTROL_ISOLATION_MATRIX)),
        "family": pd.read_csv(io_path(FAMILY_SCOPE_MATRIX)),
        "memory": pd.read_csv(io_path(FAILURE_MEMORY_UPDATE)),
        "firewall": pd.read_csv(io_path(NO_RELEASE_FIREWALL_CARRY)),
    }


def add_transfer_group(rows: list[dict[str, Any]], group: pd.DataFrame, axis: str, value: str) -> None:
    group = group.copy()
    for column in ("validation_pf", "validation_net"):
        group[column] = pd.to_numeric(group[column], errors="coerce")
    worst = group.sort_values("validation_pf", ascending=True).iloc[0]
    validation_floor = group["transfer_status"].astype(str).str.contains("validation_floor_block", regex=False)
    transfer_break = group["transfer_status"].astype(str).str.contains("train_validation_transfer_break", regex=False)
    oos_lift = group["transfer_status"].astype(str).str.contains("oos_only_lift_reconfirmed", regex=False)
    floor_count = int(validation_floor.sum())
    transfer_break_count = int(transfer_break.sum())
    oos_lift_count = int(oos_lift.sum())
    status = "blocks_release_broad_validation_failure" if floor_count else "diagnostic_only"
    if transfer_break_count:
        status += ";transfer_break_present"
    if oos_lift_count:
        status += ";oos_lift_quarantined"
    rows.append(
        {
            "review_id": f"transfer__{axis}__{value}",
            "scope_axis": axis,
            "scope_value": value,
            "rows": len(group),
            "validation_floor_block_rows": floor_count,
            "train_validation_transfer_break_rows": transfer_break_count,
            "oos_only_lift_rows": oos_lift_count,
            "min_validation_pf": float(group["validation_pf"].min()),
            "max_validation_pf": float(group["validation_pf"].max()),
            "mean_validation_pf": float(group["validation_pf"].mean()),
            "min_validation_net": float(group["validation_net"].min()),
            "worst_model_id": str(worst.get("model_id", "")),
            "review_status": status,
            "effect": "reviews transfer failure without selecting winners(승자 선택 없이 전이 실패를 검토)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )


def build_transfer_review(transfer: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    add_transfer_group(rows, transfer, "all", "all_models")
    for axis in ("cost_policy_id", "feature_set_id", "model_config_id"):
        for value, group in transfer.groupby(axis, dropna=False):
            add_transfer_group(rows, group, axis, str(value))
    return rows


def add_density_group(rows: list[dict[str, Any]], group: pd.DataFrame, split: str, axis: str, value: str) -> None:
    group = group.copy()
    for column in ("signal_density", "max_drawdown", "recovery_factor", "profit_factor"):
        group[column] = pd.to_numeric(group[column], errors="coerce")
    high_density = group["pressure_status"].astype(str).str.contains("high_density_pressure", regex=False)
    drawdown_dominates = group["pressure_status"].astype(str).str.contains("drawdown_dominates_net", regex=False)
    worst = group.sort_values("profit_factor", ascending=True).iloc[0]
    high_density_count = int(high_density.sum())
    dd_count = int(drawdown_dominates.sum())
    status = "density_pressure_blocks_release" if split == "validation" and high_density_count else "diagnostic_only"
    if dd_count:
        status += ";drawdown_dominates_net"
    rows.append(
        {
            "review_id": f"density__{split}__{axis}__{value}",
            "split": split,
            "scope_axis": axis,
            "scope_value": value,
            "rows": len(group),
            "high_density_rows": high_density_count,
            "drawdown_dominates_rows": dd_count,
            "mean_signal_density": float(group["signal_density"].mean()),
            "max_drawdown": float(group["max_drawdown"].max()),
            "min_recovery_factor": float(group["recovery_factor"].min()),
            "worst_model_id": str(worst.get("model_id", "")),
            "review_status": status,
            "effect": "reviews action density and drawdown pressure without threshold tuning(임계값 튜닝 없이 행동 밀도와 드로다운 압력 검토)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )


def build_density_review(density: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split, group in density.groupby("split", dropna=False):
        add_density_group(rows, group, str(split), "all", "all_models")
        for value, sub_group in group.groupby("model_config_id", dropna=False):
            add_density_group(rows, sub_group, str(split), "model_config_id", str(value))
    return rows


def build_control_review(control: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    control = control.copy()
    for column in ("candidate_balanced_accuracy", "control_alignment_balanced_accuracy"):
        control[column] = pd.to_numeric(control[column], errors="coerce")
    for (split, control_id), group in control.groupby(["split", "control_id"], dropna=False):
        blocked = group.loc[group["blocks_review"].astype(str).str.lower() == "true"]
        blocked_models = sorted(blocked["model_id"].astype(str).unique().tolist())
        block_count = len(blocked)
        rows.append(
            {
                "review_id": f"control__{split}__{control_id}",
                "split": split,
                "control_id": control_id,
                "rows": len(group),
                "block_rows": block_count,
                "affected_model_count": len(blocked_models),
                "max_candidate_balanced_accuracy": float(group["candidate_balanced_accuracy"].max()),
                "max_control_alignment_balanced_accuracy": float(group["control_alignment_balanced_accuracy"].max()),
                "blocked_models": ";".join(blocked_models),
                "review_status": "blocks_release_shifted_control_residual" if block_count else "diagnostic_only",
                "effect": "reviews control residual without relaxing the control rule(대조 규칙 완화 없이 대조 잔차 검토)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_family_memory_firewall_review(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    family = frames["family"]
    memory = frames["memory"]
    firewall = frames["firewall"]
    broad_family = family["observed_status"].astype(str).str.contains("broad_validation_failure", regex=False)
    high_memory = memory["severity"].astype(str).str.lower() == "high"
    firewall_blocking = firewall["carry_status"].astype(str).str.contains("carried_forward", regex=False)
    return [
        {
            "review_id": "family_constraints_review",
            "subject": "family_scope_constraints(계열 범위 제약)",
            "rows": len(family),
            "high_severity_rows": int(broad_family.sum()),
            "blocking_rows": int(broad_family.sum()),
            "observed_signature": ";".join(family.loc[broad_family, "scope_axis"].astype(str).tolist()),
            "review_status": "blocks_axis_level_selection",
            "effect": "keeps broad family failures from becoming selection shortcuts(넓은 계열 실패가 선택 지름길이 되는 것 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "failure_memory_review",
            "subject": "failure_memory(실패 기억)",
            "rows": len(memory),
            "high_severity_rows": int(high_memory.sum()),
            "blocking_rows": int(high_memory.sum()),
            "observed_signature": ";".join(memory.loc[high_memory, "memory_id"].astype(str).tolist()),
            "review_status": "blocks_release_until_repair_design",
            "effect": "keeps repeated failure signatures active(반복 실패 서명 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "firewall_review",
            "subject": "no_release_firewall(무해제 방화벽)",
            "rows": len(firewall),
            "high_severity_rows": 0,
            "blocking_rows": int(firewall_blocking.sum()),
            "observed_signature": ";".join(firewall["blocked_action_or_claim"].astype(str).tolist()),
            "review_status": "release_and_runtime_claims_blocked",
            "effect": "preserves no-selection/no-MT5 boundary(무선택/무MT5 경계 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_wfo_objective_precheck_review(final: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "review_id": "single_split_evidence_gap",
            "check_subject": "WFO/embargo readiness(WFO/격리 준비성)",
            "input_status": f"validation_rows={final['transfer_rows']};mt5={final['mt5_runtime_probe']}",
            "review_status": "blocks_release_to_training_without_precheck",
            "required_next_design": "DW must design WFO/embargo feasibility before future training(DW가 미래 학습 전 WFO/격리 가능성 설계)",
            "forbidden_action": "no single-split release(단일 분할 해제 금지)",
            "effect": "prevents single split review from becoming readiness(단일 분할 검토가 준비성 주장으로 변하는 것 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "objective_rebuild_design_only",
            "check_subject": "train-only objective repair(학습 전용 목표 수리)",
            "input_status": "needed_after_broad_validation_failure(넓은 검증 실패 후 필요)",
            "review_status": "design_allowed_training_blocked",
            "required_next_design": "abstention/cost/drawdown/direction residual contracts(보류/비용/드로다운/방향 잔차 계약)",
            "forbidden_action": "no objective retune from validation/OOS(검증/OOS 기반 목표 재튜닝 금지)",
            "effect": "opens aggressive repair without repair-overfit(수리 과적합 없이 공격 수리 열기)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "control_policy_fixed",
            "check_subject": "shifted-control rule(이동 대조 규칙)",
            "input_status": f"control_block_rows={final['control_block_rows']}",
            "review_status": "control_repair_required_no_relaxation",
            "required_next_design": "isolate technical ExtraTrees serial residual(technical ExtraTrees 연속 잔차 격리)",
            "forbidden_action": "no control threshold relaxation(대조 임계값 완화 금지)",
            "effect": "keeps overfit guard stable(과적합 방어 안정 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "density_policy_fixed",
            "check_subject": "action density pressure(행동 밀도 압력)",
            "input_status": f"high_density_validation_rows={final['high_density_validation_rows']}",
            "review_status": "density_repair_required_no_threshold_search",
            "required_next_design": "deconcentration inputs with train-only policy(학습 전용 정책 기반 탈집중 입력)",
            "forbidden_action": "no validation density threshold search(검증 밀도 임계값 탐색 금지)",
            "effect": "keeps density repair from becoming post-hoc filter(밀도 수리가 사후 필터가 되는 것 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_dw_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DW_design_train_only_objective_contracts",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design train-only objective contracts(학습 전용 목표 계약 설계)",
            "required_inputs": f"{rel(TRANSFER_BREAK_REVIEW)};{rel(WFO_OBJECTIVE_PRECHECK_REVIEW)}",
            "required_outputs": "train_only_objective_contracts.csv",
            "blocked_if_missing": "transfer/WFO review(전이/WFO 검토)",
            "forbidden_action": "no training or validation retune(학습 또는 검증 재튜닝 금지)",
            "effect": "turns broad failure into objective design constraints(넓은 실패를 목표 설계 제약으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DW_design_density_deconcentration_contracts",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design density deconcentration contracts(밀도 탈집중 계약 설계)",
            "required_inputs": rel(DENSITY_DRAWDOWN_REVIEW),
            "required_outputs": "density_deconcentration_contracts.csv",
            "blocked_if_missing": "density review(밀도 검토)",
            "forbidden_action": "no validation density threshold search(검증 밀도 임계값 탐색 금지)",
            "effect": "separates action overbreadth from signal weakness(행동 과다와 신호 약점 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DW_design_control_residual_isolation_contracts",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design shifted-control residual isolation contracts(이동 대조 잔차 격리 계약 설계)",
            "required_inputs": rel(CONTROL_ISOLATION_REVIEW),
            "required_outputs": "control_residual_isolation_contracts.csv",
            "blocked_if_missing": "control review(대조 검토)",
            "forbidden_action": "no control relaxation(대조 완화 금지)",
            "effect": "keeps serial residual repair explicit(연속 잔차 수리 명시 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DW_design_wfo_embargo_precheck",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "design WFO/embargo precheck(WFO/격리 사전검사 설계)",
            "required_inputs": rel(WFO_OBJECTIVE_PRECHECK_REVIEW),
            "required_outputs": "wfo_embargo_precheck_design.csv",
            "blocked_if_missing": "WFO precheck review(WFO 사전검사 검토)",
            "forbidden_action": "no post-selection WFO backfill(선택 후 WFO 사후 보강 금지)",
            "effect": "keeps forward robustness standard active(전진 강건성 기준 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DW_design_no_release_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "carry no-release firewall into repair design(무해제 방화벽을 수리 설계로 전달)",
            "required_inputs": rel(FAMILY_MEMORY_FIREWALL_REVIEW),
            "required_outputs": "no_release_firewall_design.csv",
            "blocked_if_missing": "family/memory/firewall review(계열/기억/방화벽 검토)",
            "forbidden_action": "no candidate selection, MT5, Forward, Goal claim(후보 선택/MT5/전진/목표 주장 금지)",
            "effect": "keeps DV as review, not promotion(승격이 아니라 검토로 DV 경계 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DU inputs exist(필수 DU 입력 존재)"),
        ("parent_du_gates_passed", final["du_failed_gate_rows"] == 0, str(final["du_failed_gate_rows"]), "0", "DU materialization usable(DU 물질화 사용 가능)"),
        ("parent_next_action_matches", final["du_next_action"] == RUN_ID, str(final["du_next_action"]), RUN_ID, "continues DU queue(DU 대기열을 이어감)"),
        ("transfer_review_materialized", final["transfer_review_rows"] >= 7, str(final["transfer_review_rows"]), ">=7", "transfer review rows materialized(전이 검토 행 물질화)"),
        ("density_review_materialized", final["density_review_rows"] >= 6, str(final["density_review_rows"]), ">=6", "density review rows materialized(밀도 검토 행 물질화)"),
        ("control_review_materialized", final["control_review_rows"] == 9, str(final["control_review_rows"]), "9", "controls reviewed by split/control(분할/대조별 검토)"),
        ("family_memory_firewall_review_materialized", final["family_memory_firewall_review_rows"] >= 3, str(final["family_memory_firewall_review_rows"]), ">=3", "family/memory/firewall reviewed(계열/기억/방화벽 검토)"),
        ("wfo_precheck_materialized", final["wfo_precheck_rows"] == 4, str(final["wfo_precheck_rows"]), "4", "WFO/objective precheck reviewed(WFO/목표 사전검사 검토)"),
        ("dw_queue_materialized", final["dw_queue_rows"] == 5, str(final["dw_queue_rows"]), "5", "DW design queue opened(DW 설계 대기열 열림)"),
        ("release_blocked_not_selected", final["release_disposition"] == "blocked_no_selection_no_mt5", str(final["release_disposition"]), "blocked_no_selection_no_mt5", "release boundary preserved(해제 경계 보존)"),
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
        "time_axis": "DU scored source_row_id UTC split rows reviewed only(DU 점수화 source_row_id UTC 분할 행 검토 전용)",
        "sample_scope": f"transfer_rows={final['transfer_rows']};density_rows={final['density_rows']};control_rows={final['control_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']}",
        "feature_label_boundary": "no new features or labels; DU materialization is reviewed as frozen evidence(새 피처/라벨 없음, DU 물질화 근거 검토)",
        "split_boundary": "train/validation/OOS compared without fitting or threshold choice(적합/임계값 선택 없이 학습/검증/OOS 비교)",
        "leakage_risk": "turning review results into model choice before DW design(DW 설계 전 리뷰 결과를 모델 선택으로 바꾸는 위험)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_review_no_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "existing DO trained artifacts reviewed through DU outputs(기존 DO 학습 산출물을 DU 출력으로 검토)",
        "target_and_label": "unchanged DU costed action labels(변경 없는 DU 비용 반영 행동 라벨)",
        "split_method": "review of train/validation/OOS transfer(학습/검증/OOS 전이 검토)",
        "selection_metric": "none; release is blocked(없음, 해제 차단)",
        "secondary_metrics": "validation floor, transfer breaks, density, drawdown, controls, WFO precheck(검증 하한/전이 단절/밀도/드로다운/대조/WFO 사전검사)",
        "threshold_policy": "fixed from parent, no tuning(부모 기준 고정, 튜닝 없음)",
        "overfit_risk": "using OOS-only lift or weak validation pocket as selector(OOS 단독 개선이나 약한 검증 포켓을 선택자로 쓰는 위험)",
        "calibration_risk": "scores remain diagnostic only(점수는 진단 전용)",
        "comparison_baseline": rel(DU_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"validation_floor_blocks={final['validation_floor_block_rows']};transfer_breaks={final['transfer_break_rows']};control_blocks={final['control_block_rows']};high_density_validation={final['high_density_validation_rows']}",
        "comparison_baseline": rel(DU_FINAL),
        "likely_drivers": "broad validation weakness, train-validation transfer break, action density, shifted-control residual(넓은 검증 약점/학습-검증 전이 단절/행동 밀도/이동 대조 잔차)",
        "segment_checks": f"transfer_review_rows={final['transfer_review_rows']};density_review_rows={final['density_review_rows']};control_review_rows={final['control_review_rows']}",
        "trade_shape": "density/drawdown pressure reviewed from DU matrix(DU 행렬 기반 밀도/드로다운 압력 검토)",
        "alternative_explanations": "single split regime drift, label-action mismatch, overbroad argmax action(단일 분할 레짐 변화/라벨-행동 불일치/과넓은 argmax 행동)",
        "attribution_confidence": "medium_for_review_low_for_release(검토는 중간, 해제는 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "DU transfer/density/control/family/memory/firewall review(DU 전이/밀도/대조/계열/기억/방화벽 검토)",
        "evidence_missing": "DW design, future materialization, training, MT5, forward evidence(DW 설계/미래 물질화/학습/MT5/전진 근거)",
        "judgment_label": "review_completed_release_blocked",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "DU 근거는 선택 근거가 아니라 왜 아직 수리 설계가 필요한지 보여준다.",
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
        "availability": "ignored_review_outputs_with_tracked_report(무시된 검토 출력과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DV Broad Validation Materialization Review(넓은 검증 물질화 검토)

## Conclusion(결론)

run337DV(337DV 실행)는 DU 물질화 결과를 검토했고 release(해제)를 계속 차단한다.

주요 이유는 validation floor block(검증 하한 차단) `{final["validation_floor_block_rows"]}`행, train-validation transfer break(학습-검증 전이 단절) `{final["transfer_break_rows"]}`행, validation high-density pressure(검증 고밀도 압력) `{final["high_density_validation_rows"]}`행, shifted-control block(이동 대조 차단) `{final["control_block_rows"]}`행이다.

이 작업은 review-only(검토 전용)이다. 새 학습, 후보 선택, 임계값 튜닝, MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 하지 않는다.

Effect(효과): run337DW(337DW 실행)는 train-only objective(학습 전용 목표), density deconcentration(밀도 탈집중), shifted-control isolation(이동 대조 격리), WFO/embargo precheck(WFO/격리 사전검사)를 설계해야 한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- transfer_review_rows(전이 검토 행): `{final["transfer_review_rows"]}`
- density_review_rows(밀도 검토 행): `{final["density_review_rows"]}`
- control_review_rows(대조 검토 행): `{final["control_review_rows"]}`
- family_memory_firewall_review_rows(계열/기억/방화벽 검토 행): `{final["family_memory_firewall_review_rows"]}`
- wfo_precheck_rows(WFO 사전검사 행): `{final["wfo_precheck_rows"]}`
- dw_queue_rows(DW 대기열 행): `{final["dw_queue_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DV

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): DU 근거는 해제 근거가 아니라 전이/밀도/대조/WFO 수리 설계 근거로만 쓴다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(TRANSFER_BREAK_REVIEW)}`, `{rel(CONTROL_ISOLATION_REVIEW)}`
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
        f"  Stage337 run337DV focus complete: broad validation materialization review(넓은 검증 물질화 검토)를 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DW(337DW 실행)에서 train-only objective/density/control/WFO repair design(학습 전용 목표/밀도/대조/WFO 수리 설계)을 연다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DV focus complete")
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
    section = f"""## Stage337 run337DV(337DV 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 전이/밀도/대조/WFO 차단을 검토했고 선택/MT5/Forward(전진)는 주장하지 않는다. Goal(목표)은 주장하지 않는다."""
    current_text = append_once(current_text, section, "Stage337 run337DV(337DV 실행)")
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection_text, _ = read_text_lossless(SELECTED_STATUS)
    selection = selection_text
    for field_name, value in {
        "latest_run": f"`{RUN_ID}`",
        "latest_decision": f"`{DECISION}`",
        "current_run": f"`{NEXT_RUN_ID}`",
        "rebuild_status": f"`{STATUS}`",
        "actual_mt5_execution": "`not_run_dv_review_only`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "effect": "`다음은 train-only objective/density/control/WFO repair design(학습 전용 목표/밀도/대조/WFO 수리 설계)이다.`",
    }.items():
        selection = replace_bullet_value(selection, field_name, value)
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337DV(337DV 실행) reviewed broad validation materialization and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DV(337DV 실행) reviewed broad validation"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337DV reviewed broad validation materialization and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DV reviewed broad validation"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "broad_validation_failure_control_residual_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"validation_floor_blocks={final['validation_floor_block_rows']};transfer_breaks={final['transfer_break_rows']};control_blocks={final['control_block_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__broad_failure_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "broad_failure_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_training_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "transfer_density_control_wfo_review",
        "scoreboard_lane": "model_validation_performance_attribution_result_judgment",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"validation_floor_blocks={final['validation_floor_block_rows']};transfer_breaks={final['transfer_break_rows']};control_blocks={final['control_block_rows']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__broad_failure_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_performance_attribution_result_judgment",
        "evidence_scope": "broad validation materialization reviewed",
        "kpi_scope": "transfer_density_control_wfo_review",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__broad_failure_review",
        "family": "model_validation_performance_attribution_result_judgment",
        "question": "does DU materialization release or require transfer density control repair design",
        "metric_scope": "validation_floor_transfer_density_control",
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

    frames = load_frames()
    transfer_rows = build_transfer_review(frames["transfer"])
    density_rows = build_density_review(frames["density"])
    control_rows = build_control_review(frames["control"])
    family_rows = build_family_memory_firewall_review(frames)

    du_final = read_json(DU_FINAL)
    du_failed_gate_rows = sum(1 for row in read_csv(DU_GATES) if row.get("status") != "passed")
    validation_floor_block_rows = sum("validation_floor_block" in str(row.get("transfer_status", "")) for row in frames["transfer"].to_dict("records"))
    transfer_break_rows = sum("train_validation_transfer_break" in str(row.get("transfer_status", "")) for row in frames["transfer"].to_dict("records"))
    oos_lift_rows = sum("oos_only_lift_reconfirmed" in str(row.get("transfer_status", "")) for row in frames["transfer"].to_dict("records"))
    high_density_validation_rows = sum(
        row.get("split") == "validation" and "high_density_pressure" in str(row.get("pressure_status", ""))
        for row in frames["density"].to_dict("records")
    )
    control_block_rows = sum(str(row.get("blocks_review", "")).lower() == "true" for row in frames["control"].to_dict("records"))
    wfo_rows = build_wfo_objective_precheck_review(
        {
            **du_final,
            "transfer_rows": len(frames["transfer"]),
            "control_block_rows": int(control_block_rows),
            "high_density_validation_rows": int(high_density_validation_rows),
        }
    )
    queue_rows = build_dw_queue()
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "du_next_action": du_final.get("next_action", ""),
        "du_failed_gate_rows": du_failed_gate_rows,
        "missing_inputs": len(missing),
        "transfer_rows": len(frames["transfer"]),
        "density_rows": len(frames["density"]),
        "control_rows": len(frames["control"]),
        "validation_floor_block_rows": int(validation_floor_block_rows),
        "transfer_break_rows": int(transfer_break_rows),
        "oos_lift_rows": int(oos_lift_rows),
        "high_density_validation_rows": int(high_density_validation_rows),
        "control_block_rows": int(control_block_rows),
        "transfer_review_rows": len(transfer_rows),
        "density_review_rows": len(density_rows),
        "control_review_rows": len(control_rows),
        "family_memory_firewall_review_rows": len(family_rows),
        "wfo_precheck_rows": len(wfo_rows),
        "dw_queue_rows": len(queue_rows),
        "release_disposition": "blocked_no_selection_no_mt5",
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
        write_csv(TRANSFER_BREAK_REVIEW, TRANSFER_COLUMNS, transfer_rows),
        write_csv(DENSITY_DRAWDOWN_REVIEW, DENSITY_COLUMNS, density_rows),
        write_csv(CONTROL_ISOLATION_REVIEW, CONTROL_COLUMNS, control_rows),
        write_csv(FAMILY_MEMORY_FIREWALL_REVIEW, FAMILY_COLUMNS, family_rows),
        write_csv(WFO_OBJECTIVE_PRECHECK_REVIEW, WFO_COLUMNS, wfo_rows),
        write_csv(DW_QUEUE, QUEUE_COLUMNS, queue_rows),
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
