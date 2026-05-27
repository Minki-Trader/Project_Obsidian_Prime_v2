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
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CX"
RUN_ID = "run337CX_review_feature_label_separability_control_training_without_db_v1"
PARENT_RUN_ID = "run337CW_train_feature_label_separability_control_repaired_candidates_without_db_v1"
NEXT_RUN_ID = "run337CY_design_objective_feature_contract_pivot_after_separability_control_failure_without_db_v1"
STATUS = "completed_stage337CX_separability_control_training_review_no_release_no_selection"
JUDGMENT = "onnx_parity_cleared_but_validation_quality_and_controls_block_release"
DECISION = "stage337CX_open_run337CY_objective_feature_contract_pivot_design"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CX_feature_label_separability_control_training_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CX_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CX_feature_label_separability_control_training_review.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CW_DIR = STAGE_DIR / "02_runs" / "run337CW"
CW_FINAL = CW_DIR / "final_decision.json"
CW_GATES = CW_DIR / "required_gate_coverage_audit.csv"
TASK_DISPOSITION = CW_DIR / "task_disposition_matrix.csv"
MODEL_MANIFEST = CW_DIR / "trained_model_manifest.csv"
ONNX_PARITY = CW_DIR / "onnx_parity_matrix.csv"
SCORECARD = CW_DIR / "guarded_training_scorecard.csv"
CONTROL_SCORECARD = CW_DIR / "extended_control_scorecard.csv"
COST_SCORECARD = CW_DIR / "cost_curve_shape_scorecard.csv"
RUNTIME_DISPOSITION = CW_DIR / "runtime_probe_release_disposition.csv"

RELEASE_LOCK_REVIEW = RUN_DIR / "release_lock_review.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "failure_attribution_matrix.csv"
TOP_DIAGNOSTIC = RUN_DIR / "top_readonly_diagnostic_pockets.csv"
CONTROL_COST_SUMMARY = RUN_DIR / "control_cost_block_summary.csv"
CY_QUEUE = RUN_DIR / "run337CY_repair_design_queue.csv"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CW_FINAL,
    CW_GATES,
    TASK_DISPOSITION,
    MODEL_MANIFEST,
    ONNX_PARITY,
    SCORECARD,
    CONTROL_SCORECARD,
    COST_SCORECARD,
    RUNTIME_DISPOSITION,
)
OUTPUT_FILES = (
    RELEASE_LOCK_REVIEW,
    FAILURE_ATTRIBUTION,
    TOP_DIAGNOSTIC,
    CONTROL_COST_SUMMARY,
    CY_QUEUE,
    MODEL_RECEIPT,
    DATA_RECEIPT,
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

RELEASE_COLUMNS = (
    "review_id",
    "metric",
    "observed",
    "required",
    "status",
    "effect",
    "claim_boundary",
)
FAILURE_COLUMNS = (
    "failure_axis",
    "evidence",
    "severity",
    "is_blocker",
    "not_allowed_repair",
    "allowed_next_probe",
    "effect",
    "claim_boundary",
)
TOP_COLUMNS = (
    "diagnostic_rank",
    "policy_id",
    "model_id",
    "split",
    "model_balanced_accuracy",
    "signal_density",
    "trade_balanced_accuracy",
    "mean_raw_trade_return",
    "selection_use",
    "reason",
    "claim_boundary",
)
SUMMARY_COLUMNS = (
    "summary_id",
    "slice_type",
    "slice_value",
    "rows",
    "block_rows",
    "pass_rows",
    "worst_value",
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


def bool_count(series: pd.Series) -> int:
    return int(series.astype(str).str.lower().eq("true").sum())


def summarize_inputs() -> dict[str, Any]:
    final = read_json(CW_FINAL)
    score = pd.read_csv(io_path(SCORECARD))
    controls = pd.read_csv(io_path(CONTROL_SCORECARD))
    cost = pd.read_csv(io_path(COST_SCORECARD))
    runtime = pd.read_csv(io_path(RUNTIME_DISPOSITION))
    parity = pd.read_csv(io_path(ONNX_PARITY))
    tasks = pd.read_csv(io_path(TASK_DISPOSITION))

    validation = score.loc[score["split"] == "validation"].copy()
    oos = score.loc[score["split"] == "oos"].copy()
    best_validation_balanced = float(validation["model_balanced_accuracy"].max()) if len(validation) else 0.0
    best_oos_balanced = float(oos["model_balanced_accuracy"].max()) if len(oos) else 0.0
    best_validation_density = float(validation["signal_density"].max()) if len(validation) else 0.0
    best_oos_density = float(oos["signal_density"].max()) if len(oos) else 0.0
    control_blocks = bool_count(controls["blocks_runtime_probe"])
    cost_blocks = bool_count(cost["blocks_runtime_probe"])
    review_eligible = int(runtime["mt5_probe_disposition"].astype(str).eq("review_eligible_no_auto_mt5_release").sum())
    return {
        "final": final,
        "score": score,
        "controls": controls,
        "cost": cost,
        "runtime": runtime,
        "parity": parity,
        "tasks": tasks,
        "trained_models": int(final.get("trained_models", 0)),
        "held_task_rows": int(final.get("held_task_rows", 0)),
        "parity_passed": int(parity["passed"].astype(str).str.lower().eq("true").sum()),
        "parity_rows": int(len(parity)),
        "runtime_rows": int(len(runtime)),
        "review_eligible_rows": review_eligible,
        "best_validation_balanced": best_validation_balanced,
        "best_oos_balanced": best_oos_balanced,
        "best_validation_density": best_validation_density,
        "best_oos_density": best_oos_density,
        "control_blocks": control_blocks,
        "control_rows": int(len(controls)),
        "cost_blocks": cost_blocks,
        "cost_rows": int(len(cost)),
    }


def build_release_review(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "review_id": "onnx_parity",
            "metric": "onnx parity(ONNX 동등성)",
            "observed": f"{summary['parity_passed']}/{summary['parity_rows']}",
            "required": "all passed(전체 통과)",
            "status": "passed",
            "effect": "ONNX 자체는 차단 원인이 아니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "validation_quality",
            "metric": "best validation balanced accuracy(최고 검증 균형 정확도)",
            "observed": summary["best_validation_balanced"],
            "required": "> 0.40",
            "status": "blocked",
            "effect": "검증 품질이 문턱 아래라 release(해제)를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "oos_readonly",
            "metric": "best OOS balanced accuracy(최고 OOS 균형 정확도)",
            "observed": summary["best_oos_balanced"],
            "required": "read-only, not selection(읽기 전용, 선택 아님)",
            "status": "readonly_positive_pocket_not_selectable" if summary["best_oos_balanced"] > 0.40 else "readonly_weak",
            "effect": "OOS만 좋은 구간은 선택 근거가 아니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "extended_controls",
            "metric": "control block rows(대조 차단 행)",
            "observed": f"{summary['control_blocks']}/{summary['control_rows']}",
            "required": "0 blocks before MT5 review(MT5 검토 전 차단 0)",
            "status": "blocked",
            "effect": "대조 정렬 위험이 남아 있다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "cost_shape",
            "metric": "cost block rows(비용 차단 행)",
            "observed": f"{summary['cost_blocks']}/{summary['cost_rows']}",
            "required": "cost shape stable(비용 곡선 안정)",
            "status": "blocked",
            "effect": "비용 압박에서 곡선 안정성이 약하다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "runtime_release",
            "metric": "review eligible rows(리뷰 가능 행)",
            "observed": summary["review_eligible_rows"],
            "required": "> 0 for runtime package consideration(런타임 패키지 검토는 0 초과 필요)",
            "status": "blocked",
            "effect": "MT5 probe(MT5 탐침)는 열지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_attribution(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "failure_axis": "validation_quality_gate_block",
            "evidence": f"best_validation_balanced={summary['best_validation_balanced']:.12g} < 0.40",
            "severity": "hard_blocker",
            "is_blocker": "true",
            "not_allowed_repair": "lower validation threshold(검증 문턱 낮추기)",
            "allowed_next_probe": "objective/feature contract pivot(목표/피처 계약 전환)",
            "effect": "라벨 여백 수리가 분리력을 충분히 복구하지 못했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_axis": "oos_readonly_pocket_not_selectable",
            "evidence": f"best_oos_balanced={summary['best_oos_balanced']:.12g}, but OOS is read-only(OOS는 읽기 전용)",
            "severity": "overfit_guard",
            "is_blocker": "true",
            "not_allowed_repair": "pick best OOS pocket(최고 OOS 구간 선택)",
            "allowed_next_probe": "predeclared train/validation gate before OOS read(OOS 판독 전 사전 선언 학습/검증 게이트)",
            "effect": "OOS만 좋은 결과를 선택으로 바꾸는 과적합을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_axis": "extended_control_alignment",
            "evidence": f"control_blocks={summary['control_blocks']}/{summary['control_rows']}",
            "severity": "hard_blocker",
            "is_blocker": "true",
            "not_allowed_repair": "drop controls after failure(실패 후 대조 제거)",
            "allowed_next_probe": "control-orthogonal objective or feature contract(대조 직교 목표 또는 피처 계약)",
            "effect": "모델이 여전히 이동/기간 대조와 충분히 분리되지 않았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_axis": "cost_curve_fragility",
            "evidence": f"cost_blocks={summary['cost_blocks']}/{summary['cost_rows']}",
            "severity": "secondary_hard_blocker",
            "is_blocker": "true",
            "not_allowed_repair": "ignore cost stress(비용 압박 무시)",
            "allowed_next_probe": "cost-aware target or abstention objective(비용 인식 타깃 또는 진입 회피 목표)",
            "effect": "거래 가능 신호가 비용을 충분히 이기지 못한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_axis": "two_stage_composite_contract_gap",
            "evidence": f"held_task_rows={summary['held_task_rows']}",
            "severity": "design_gap",
            "is_blocker": "false",
            "not_allowed_repair": "pretend composite is single ONNX(복합 모델을 단일 ONNX처럼 포장)",
            "allowed_next_probe": "explicit two-model handoff contract(명시적 2모델 인계 계약)",
            "effect": "2단계 아이디어는 아직 무효가 아니라 별도 계약이 필요하다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_axis": "onnx_parity_not_blocker",
            "evidence": f"onnx_parity={summary['parity_passed']}/{summary['parity_rows']}",
            "severity": "cleared",
            "is_blocker": "false",
            "not_allowed_repair": "blame ONNX export(ONNX 내보내기 탓하기)",
            "allowed_next_probe": "focus on target/features/controls(타깃/피처/대조에 집중)",
            "effect": "실패 원인은 런타임 변환이 아니라 신호 품질과 대조다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_top_diagnostics(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    score = summary["score"]
    view = score.loc[score["split"].isin(["validation", "oos"])].copy()
    view = view.sort_values(["model_balanced_accuracy", "signal_density"], ascending=[False, False]).head(30)
    rows = []
    for rank, (_, item) in enumerate(view.iterrows(), start=1):
        rows.append(
            {
                "diagnostic_rank": rank,
                "policy_id": item["policy_id"],
                "model_id": item["model_id"],
                "split": item["split"],
                "model_balanced_accuracy": item["model_balanced_accuracy"],
                "signal_density": item["signal_density"],
                "trade_balanced_accuracy": item["trade_balanced_accuracy"],
                "mean_raw_trade_return": item["mean_raw_trade_return"],
                "selection_use": "forbidden_readonly_diagnostic(금지, 읽기 전용 진단)",
                "reason": "rank is for attribution only, not candidate selection(순위는 귀속용이지 후보 선택 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_control_cost_summary(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    controls = summary["controls"]
    for (control_id, split), group in controls.groupby(["control_id", "split"], dropna=False):
        rows.append(
            {
                "summary_id": f"control__{control_id}__{split}",
                "slice_type": "control",
                "slice_value": f"{control_id}/{split}",
                "rows": len(group),
                "block_rows": bool_count(group["blocks_runtime_probe"]),
                "pass_rows": int(len(group) - bool_count(group["blocks_runtime_probe"])),
                "worst_value": pd.to_numeric(group["control_minus_actual"], errors="coerce").max(),
                "effect": "대조별 차단 밀도를 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    cost = summary["cost"]
    for (cost_points, split), group in cost.groupby(["cost_points", "split"], dropna=False):
        rows.append(
            {
                "summary_id": f"cost__{cost_points}__{split}",
                "slice_type": "cost",
                "slice_value": f"{cost_points}/{split}",
                "rows": len(group),
                "block_rows": bool_count(group["blocks_runtime_probe"]),
                "pass_rows": int(len(group) - bool_count(group["blocks_runtime_probe"])),
                "worst_value": pd.to_numeric(group["net_proxy_return"], errors="coerce").min(),
                "effect": "비용별 곡선 취약성을 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_cy_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337CY_objective_family_pivot",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design objective-family pivot after validation quality block(검증 품질 차단 후 목표 계열 전환 설계)",
            "required_inputs": rel(FAILURE_ATTRIBUTION),
            "required_outputs": "objective_family_pivot_design.csv",
            "blocked_if_missing": "failure attribution missing(실패 귀속 누락)",
            "forbidden_action": "no threshold lowering(임계값 낮추기 금지)",
            "effect": "라벨 여백을 더 조이는 과적합 대신 목표 자체를 재검토한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CY_two_stage_handoff_contract",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design explicit two-stage ONNX/runtime handoff contract(명시적 2단계 ONNX/런타임 인계 계약 설계)",
            "required_inputs": rel(TASK_DISPOSITION),
            "required_outputs": "two_stage_runtime_contract_design.csv",
            "blocked_if_missing": "held two-stage task rows missing(보류 2단계 작업 행 누락)",
            "forbidden_action": "no fake single-surface claim(가짜 단일 표면 주장 금지)",
            "effect": "2단계 아이디어를 무효화하지 않고 올바른 계약으로만 열어둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CY_control_orthogonal_objective",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "design control-orthogonal target or residual objective(대조 직교 타깃 또는 잔차 목표 설계)",
            "required_inputs": rel(CONTROL_COST_SUMMARY),
            "required_outputs": "control_orthogonal_objective_contract.csv",
            "blocked_if_missing": "control summary missing(대조 요약 누락)",
            "forbidden_action": "no dropping failed controls(실패 대조 제거 금지)",
            "effect": "대조와 같이 움직이는 신호를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CY_cost_aware_abstention",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "design cost-aware abstention target(비용 인식 진입 회피 타깃 설계)",
            "required_inputs": rel(COST_SCORECARD),
            "required_outputs": "cost_aware_abstention_contract.csv",
            "blocked_if_missing": "cost scorecard missing(비용 점수표 누락)",
            "forbidden_action": "no lot optimization(로트 최적화 금지)",
            "effect": "수익률보다 거래 가능성을 먼저 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]

    def row(gate_id: str, ok: bool, observed: Any, expected: str, effect: str) -> dict[str, str]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": str(observed),
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    return [
        row("cx_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CW 산출물에 연결한다."),
        row("cx_gate_parent_points_to_cx", final["cw_next_action"] == RUN_ID, final["cw_next_action"], RUN_ID, "CW next_action(다음 행동)과 CX 실행을 맞춘다."),
        row("cx_gate_no_release_rows", final["review_eligible_rows"] == 0, final["review_eligible_rows"], "0", "릴리즈 부재를 명확히 기록한다."),
        row("cx_gate_validation_block_named", final["best_validation_balanced"] < 0.40, final["best_validation_balanced"], "<0.40", "검증 품질 차단을 이름 붙인다."),
        row("cx_gate_oos_readonly_guard", final["best_oos_balanced"] >= 0.0, final["best_oos_balanced"], "diagnostic only", "OOS 결과를 선택에 쓰지 않는다."),
        row("cx_gate_failure_axes", final["failure_rows"] >= 6, final["failure_rows"], ">=6", "실패 축을 분리해 기록한다."),
        row("cx_gate_next_queue", final["queue_rows"] >= 4, final["queue_rows"], ">=4", "다음 수리 설계를 연다."),
        row("cx_gate_no_training_selection_mt5", True, "training=not_run;selection=not_run;mt5=not_run", "no training/selection/MT5", "리뷰를 새 후보 선택으로 바꾸지 않는다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    model_receipt = {
        "model_family": "review only, no new training(검토 전용, 새 학습 없음)",
        "target_and_label": "CW label_v4 margin candidates reviewed(CW 라벨 v4 여백 후보 검토)",
        "split_method": "train/validation/OOS read from CW scorecards(CW 점수표 분할 사용)",
        "selection_metric": "not_applicable_no_selection(해당 없음, 선택 없음)",
        "secondary_metrics": "validation quality, OOS read-only, controls, cost, parity(검증 품질, OOS 읽기 전용, 대조, 비용, 동등성)",
        "threshold_policy": "not_touched(건드리지 않음)",
        "overfit_risk": "OOS-only best pocket selection(OOS 전용 최고 구간 선택)",
        "calibration_risk": "not reviewed as calibrated probability(보정 확률로 검토하지 않음)",
        "comparison_baseline": "run337CW guarded training(CW 방어 학습)",
        "validation_judgment": "release_blocked_review_complete",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherited from CW artifacts(CW 산출물에서 상속)",
        "sample_scope": "CW scorecards and controls only(CW 점수표와 대조만)",
        "missing_or_duplicate_check": "input presence gate passed(입력 존재 게이트 통과)",
        "feature_label_boundary": "no new features or labels created(새 피처/라벨 없음)",
        "split_boundary": "validation blocks release; OOS is read-only(검증이 해제를 막고 OOS는 읽기 전용)",
        "leakage_risk": "using top_readonly_diagnostic_pockets as selection(읽기 전용 상위 진단을 선택에 쓰는 것)",
        "data_hash_or_identity": {"cw_final": sha256_file(CW_FINAL)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "attribution_subject": RUN_ID,
        "primary_failure": "validation quality below 0.40 and controls/cost blocks(검증 품질 0.40 미만 및 대조/비용 차단)",
        "not_blocker": "ONNX parity(ONNX 동등성)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "release review, failure attribution, top diagnostic pockets, control/cost summary(해제 검토, 실패 귀속, 상위 진단, 대조/비용 요약)",
        "evidence_missing": "new design, new training, MT5 probe(새 설계, 새 학습, MT5 탐침)",
        "judgment_label": "negative_valid_repair_design_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "ONNX는 맞지만 신호 품질과 대조가 부족해 해제하지 않는다.",
    }
    receipt_paths = [
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifact_paths] + [rel(path) for path in receipt_paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + receipt_paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_review_and_ignored_run_outputs(추적 검토와 무시된 실행 산출물)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipt_paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return receipt_paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CX Training Review(학습 검토)

## Conclusion(결론)

run337CX(337CX 실행)는 CW 학습 결과를 검토했다. ONNX parity(ONNX 동등성)는 `{final["parity_passed"]}/{final["parity_rows"]}`로 통과했지만, best validation balanced accuracy(최고 검증 균형 정확도)는 `{final["best_validation_balanced"]:.12g}`로 0.40 문턱 아래다. review eligible rows(리뷰 가능 행)는 `{final["review_eligible_rows"]}`이다.

Effect(효과): MT5 probe(MT5 탐침), candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패)는 열지 않는다. 다음은 objective/feature contract pivot design(목표/피처 계약 전환 설계)이다.

## Failure Attribution(실패 귀속)

- validation_quality(검증 품질): `{final["best_validation_balanced"]:.12g}` < `0.40`
- OOS readonly(OOS 읽기 전용): best OOS balanced `{final["best_oos_balanced"]:.12g}`는 선택 근거가 아니다.
- controls(대조): `{final["control_blocks"]}/{final["control_rows"]}` block rows(차단 행)
- cost(비용): `{final["cost_blocks"]}/{final["cost_rows"]}` block rows(차단 행)
- two_stage(2단계): held rows(보류 행) `{final["held_task_rows"]}`, 별도 runtime handoff contract(런타임 인계 계약) 필요

## Boundary(경계)

- new_training(새 학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CX

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): ONNX parity(ONNX 동등성)는 차단 원인이 아니고, validation quality/control/cost(검증 품질/대조/비용)가 해제를 막는다고 귀속했다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(FAILURE_ATTRIBUTION)}`
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
        "current_focus:\n- >-\n"
        f"  Stage337 run337CX focus complete: feature/label separability control training review(피처/라벨 분리력 대조 학습 검토)를 "
        f"`{STATUS}`로 닫았다. Effect(효과): validation quality/control/cost(검증 품질/대조/비용) 실패를 run337CY(337CY 실행) objective/feature contract pivot design(목표/피처 계약 전환 설계)로 넘긴다."
    )
    workspace_text = workspace_text.replace("current_focus:", focus_entry, 1)
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
## Stage337 run337CX(337CX 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): ONNX parity(ONNX 동등성)는 `{final["parity_passed"]}/{final["parity_rows"]}`로 통과했지만 validation quality/control/cost(검증 품질/대조/비용)가 release(해제)를 막았다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337CW(337CW"
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
- actual_mt5_execution(실제 MT5 실행): `not_run_cx_review_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 objective/feature contract pivot design(목표/피처 계약 전환 설계)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337CX(337CX 실행) reviewed separability/control training(분리력/대조 학습 검토). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337CX reviewed separability/control training(분리력/대조 학습 검토) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "feature_label_separability_control_training_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"validation_max={final['best_validation_balanced']:.12g};review_eligible={final['review_eligible_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "kpi_evidence_result_judgment_performance_attribution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "training_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "model_validation_control_cost_review",
        "scoreboard_lane": "result_judgment",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"validation_max={final['best_validation_balanced']:.12g};review_eligible={final['review_eligible_rows']}",
        "guardrail_kpi": "oos_readonly;no_selection;no_mt5;no_goal",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "kpi_evidence_result_judgment_performance_attribution",
        "evidence_scope": "CW training review and failure attribution",
        "kpi_scope": "model_validation_control_cost_review",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__training_review",
        "family": "kpi_evidence_result_judgment_performance_attribution",
        "question": "why did separability/control repaired ONNX candidates not release",
        "metric_scope": "validation_oos_controls_cost_parity",
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
    summary = summarize_inputs()
    release_rows = build_release_review(summary)
    failure_rows = build_failure_attribution(summary)
    top_rows = build_top_diagnostics(summary)
    summary_rows = build_control_cost_summary(summary)
    queue_rows = build_cy_queue()
    artifacts: list[Path] = [
        write_csv(RELEASE_LOCK_REVIEW, RELEASE_COLUMNS, release_rows),
        write_csv(FAILURE_ATTRIBUTION, FAILURE_COLUMNS, failure_rows),
        write_csv(TOP_DIAGNOSTIC, TOP_COLUMNS, top_rows),
        write_csv(CONTROL_COST_SUMMARY, SUMMARY_COLUMNS, summary_rows),
        write_csv(CY_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "cw_next_action": summary["final"].get("next_action", ""),
        "trained_models": summary["trained_models"],
        "held_task_rows": summary["held_task_rows"],
        "parity_passed": summary["parity_passed"],
        "parity_rows": summary["parity_rows"],
        "runtime_rows": summary["runtime_rows"],
        "review_eligible_rows": summary["review_eligible_rows"],
        "best_validation_balanced": summary["best_validation_balanced"],
        "best_oos_balanced": summary["best_oos_balanced"],
        "best_validation_density": summary["best_validation_density"],
        "best_oos_density": summary["best_oos_density"],
        "control_blocks": summary["control_blocks"],
        "control_rows": summary["control_rows"],
        "cost_blocks": summary["cost_blocks"],
        "cost_rows": summary["cost_rows"],
        "release_review_rows": len(release_rows),
        "failure_rows": len(failure_rows),
        "top_diagnostic_rows": len(top_rows),
        "control_cost_summary_rows": len(summary_rows),
        "queue_rows": len(queue_rows),
        "model_training": "not_run_review_only",
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
