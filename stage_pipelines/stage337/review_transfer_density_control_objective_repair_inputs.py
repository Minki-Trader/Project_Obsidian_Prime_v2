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
from stage_pipelines.stage337 import materialize_transfer_density_control_objective_repair_inputs as dx  # noqa: E402
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
STAGE_ID = dx.STAGE_ID
RUN_NUMBER = "run337DY"
RUN_ID = "run337DY_review_transfer_density_control_objective_repair_inputs_without_db_v1"
PARENT_RUN_ID = dx.RUN_ID
NEXT_RUN_ID = "run337DZ_train_guarded_transfer_density_control_repair_candidates_without_db_v1"
STATUS = "completed_stage337DY_repair_inputs_review_guarded_training_eligible_with_drawdown_tag_limit_no_selection_no_mt5"
JUDGMENT = "inputs_train_only_and_wfo_feasible_but_drawdown_binary_tag_broad_controls_required"
DECISION = "stage337DY_open_run337DZ_train_guarded_transfer_density_control_repair_candidates"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DY_transfer_density_control_objective_input_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dx.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dx.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DY_transfer_density_control_objective_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DY_transfer_density_control_objective_input_review.md"
SELECTED_STATUS = dx.SELECTED_STATUS
STAGE_BRIEF = dx.STAGE_BRIEF
WORKSPACE_STATE = dx.WORKSPACE_STATE
CURRENT_STATE = dx.CURRENT_STATE
CHANGELOG = dx.CHANGELOG
RUN_REGISTRY = dx.RUN_REGISTRY
ALPHA_LEDGER = dx.ALPHA_LEDGER
ARTIFACT_REGISTRY = dx.ARTIFACT_REGISTRY
STAGE_LEDGER = dx.STAGE_LEDGER

DX_FINAL = dx.FINAL_DECISION
DX_GATES = dx.REQUIRED_GATE_AUDIT
DX_QUEUE = dx.DY_QUEUE
OBJECTIVE_FRAME = dx.TRAIN_ONLY_OBJECTIVE_INPUT_FRAME
OBJECTIVE_AUDIT = dx.OBJECTIVE_CONTRACT_AUDIT
DENSITY_MATRIX = dx.DENSITY_DECONCENTRATION_MATRIX
CONTROL_MATRIX = dx.CONTROL_RESIDUAL_ISOLATION_MATRIX
WFO_FEASIBILITY = dx.WFO_EMBARGO_FEASIBILITY
FIREWALL_CARRY = dx.NO_RELEASE_FIREWALL_CARRY

OBJECTIVE_INPUT_REVIEW = RUN_DIR / "objective_input_review.csv"
DENSITY_INPUT_REVIEW = RUN_DIR / "density_input_review.csv"
CONTROL_INPUT_REVIEW = RUN_DIR / "control_input_review.csv"
WFO_INPUT_REVIEW = RUN_DIR / "wfo_input_review.csv"
FIREWALL_REVIEW = RUN_DIR / "firewall_review.csv"
TRAINING_ELIGIBILITY_MATRIX = RUN_DIR / "training_eligibility_matrix.csv"
DZ_QUEUE = RUN_DIR / "run337DZ_training_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DX_FINAL,
    DX_GATES,
    DX_QUEUE,
    OBJECTIVE_FRAME,
    OBJECTIVE_AUDIT,
    DENSITY_MATRIX,
    CONTROL_MATRIX,
    WFO_FEASIBILITY,
    FIREWALL_CARRY,
)
OUTPUT_FILES = (
    OBJECTIVE_INPUT_REVIEW,
    DENSITY_INPUT_REVIEW,
    CONTROL_INPUT_REVIEW,
    WFO_INPUT_REVIEW,
    FIREWALL_REVIEW,
    TRAINING_ELIGIBILITY_MATRIX,
    DZ_QUEUE,
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
ELIGIBILITY_COLUMNS = (
    "eligibility_id",
    "input_subject",
    "eligibility_status",
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


def review_objective_frame() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    df = pd.read_parquet(io_path(OBJECTIVE_FRAME))
    total = len(df)
    split_values = sorted(df["split"].astype(str).unique().tolist())
    low_margin = int(df["low_margin_trade_tag"].sum())
    underwater = int(df["underwater_tag"].sum())
    direction_residual = int(df["direction_residual_tag"].sum())
    abstention = int(df["abstention_candidate_tag"].sum())
    summary = {
        "rows": total,
        "split_values": split_values,
        "models": int(df["model_id"].nunique()),
        "source_rows": int(df["source_row_id"].nunique()),
        "low_margin_rows": low_margin,
        "underwater_rows": underwater,
        "direction_residual_rows": direction_residual,
        "abstention_rows": abstention,
        "underwater_ratio": pct(underwater, total),
        "low_margin_ratio": pct(low_margin, total),
        "direction_residual_ratio": pct(direction_residual, total),
    }
    rows = [
        {
            "review_id": "objective_split_boundary",
            "subject": "train-only split boundary(학습 전용 분할 경계)",
            "rows": total,
            "metric_1": ",".join(split_values),
            "metric_2": f"models={summary['models']};source_rows={summary['source_rows']}",
            "review_status": "passed_train_only" if split_values == ["train"] else "invalid_non_train_rows",
            "allowed_use": "training input candidate after DY review(DY 검토 후 학습 입력 후보)",
            "forbidden_use": "validation/OOS label use(검증/OOS 라벨 사용)",
            "effect": "checks leakage boundary(누수 경계 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "low_margin_tag_review",
            "subject": "low_margin_trade_tag(저여백 거래 태그)",
            "rows": low_margin,
            "metric_1": f"ratio={summary['low_margin_ratio']}",
            "metric_2": "train_trade_abs_pnl_q25",
            "review_status": "usable_as_auxiliary_target" if low_margin > 0 else "blocked_empty_tag",
            "allowed_use": "auxiliary train-only objective(보조 학습 전용 목표)",
            "forbidden_use": "validation density filter(검증 밀도 필터)",
            "effect": "keeps low-margin repair train-only(저여백 수리를 학습 전용으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "underwater_tag_review",
            "subject": "underwater_tag/drawdown_pressure_value(침수 태그/드로다운 압력값)",
            "rows": underwater,
            "metric_1": f"ratio={summary['underwater_ratio']}",
            "metric_2": "binary tag too broad if ratio>0.95(0.95 초과면 이진 태그 과다)",
            "review_status": "continuous_only_binary_target_blocked" if summary["underwater_ratio"] > 0.95 else "usable_as_binary_or_continuous",
            "allowed_use": "continuous diagnostic or sample note(연속 진단값 또는 샘플 참고)",
            "forbidden_use": "binary target when broad(넓을 때 이진 목표 사용)",
            "effect": "prevents broad drawdown tag from becoming weak target(넓은 드로다운 태그가 약한 목표가 되는 것 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "direction_residual_review",
            "subject": "direction_residual_tag(방향 잔차 태그)",
            "rows": direction_residual,
            "metric_1": f"ratio={summary['direction_residual_ratio']}",
            "metric_2": "pred_label != true_label on train trades(학습 거래에서 예측 라벨과 실제 라벨 불일치)",
            "review_status": "usable_as_auxiliary_target" if direction_residual > 0 else "blocked_empty_tag",
            "allowed_use": "auxiliary train-only objective(보조 학습 전용 목표)",
            "forbidden_use": "validation direction filter(검증 방향 필터)",
            "effect": "separates direction repair from OOS selection(방향 수리를 OOS 선택과 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows, summary


def review_density() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows_in = read_csv(DENSITY_MATRIX)
    validation_pressure = [row for row in rows_in if row.get("density_pressure_flag") == "validation_density_pressure"]
    rows = [
        {
            "review_id": "density_matrix_completeness",
            "subject": "density_deconcentration_matrix(밀도 탈집중 행렬)",
            "rows": len(rows_in),
            "metric_1": f"validation_pressure_rows={len(validation_pressure)}",
            "metric_2": "expected_rows=54",
            "review_status": "passed_review_only",
            "allowed_use": "diagnostic feature or audit column(진단 피처 또는 감사 열)",
            "forbidden_use": "threshold tuning(임계값 튜닝)",
            "effect": "keeps density work diagnostic(밀도 작업을 진단으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return rows, {"rows": len(rows_in), "validation_pressure_rows": len(validation_pressure)}


def review_control() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows_in = read_csv(CONTROL_MATRIX)
    blocked = [row for row in rows_in if str(row.get("blocks_review", "")).lower() == "true"]
    blocked_models = sorted({row.get("model_id", "") for row in blocked})
    rows = [
        {
            "review_id": "control_matrix_completeness",
            "subject": "control_residual_isolation_matrix(대조 잔차 격리 행렬)",
            "rows": len(rows_in),
            "metric_1": f"blocked_rows={len(blocked)}",
            "metric_2": ";".join(blocked_models),
            "review_status": "control_blocks_reconfirmed" if blocked else "controls_clear",
            "allowed_use": "hard training guard and post-training blocker(강한 학습 가드와 학습 후 차단)",
            "forbidden_use": "control relaxation(대조 완화)",
            "effect": "keeps shifted-control guard active(이동 대조 방어 활성 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return rows, {"rows": len(rows_in), "blocked_rows": len(blocked), "blocked_models": len(blocked_models)}


def review_wfo() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows_in = read_csv(WFO_FEASIBILITY)
    feasible = [row for row in rows_in if row.get("feasibility_status") == "feasible_precheck_not_training"]
    rows = [
        {
            "review_id": "wfo_embargo_feasibility_review",
            "subject": "WFO/embargo feasibility(WFO/격리 가능성)",
            "rows": len(rows_in),
            "metric_1": f"feasible_rows={len(feasible)}",
            "metric_2": "precheck only, not proof(사전검사일 뿐 증명 아님)",
            "review_status": "feasible_for_guarded_training_design" if len(feasible) == len(rows_in) else "blocked_wfo_geometry",
            "allowed_use": "future training split prerequisite(미래 학습 분할 전제)",
            "forbidden_use": "Forward Passed claim(전진 통과 주장)",
            "effect": "keeps WFO before training, not after selection(WFO를 선택 후가 아니라 학습 전에 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return rows, {"rows": len(rows_in), "feasible_rows": len(feasible)}


def review_firewall() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows_in = read_csv(FIREWALL_CARRY)
    active = [row for row in rows_in if "active" in str(row.get("carry_status", ""))]
    rows = [
        {
            "review_id": "firewall_carry_review",
            "subject": "no-release firewall(무해제 방화벽)",
            "rows": len(rows_in),
            "metric_1": f"active_rows={len(active)}",
            "metric_2": ";".join(row.get("blocked_action_or_claim", "") for row in rows_in),
            "review_status": "active_no_release",
            "allowed_use": "training guard only(학습 가드 전용)",
            "forbidden_use": "candidate selection or MT5 queue(후보 선택 또는 MT5 대기열)",
            "effect": "keeps input review from becoming promotion(입력 검토가 승격으로 변하는 것 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return rows, {"rows": len(rows_in), "active_rows": len(active)}


def build_eligibility(summary: Mapping[str, Any], density: Mapping[str, Any], control: Mapping[str, Any], wfo: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "eligibility_id": "low_margin_auxiliary_target",
            "input_subject": "low_margin_trade_tag(저여백 거래 태그)",
            "eligibility_status": "eligible_for_guarded_training_auxiliary",
            "allowed_training_use": "auxiliary target or sample tag(보조 목표 또는 샘플 태그)",
            "required_guard": "train-only, no validation threshold(학습 전용, 검증 임계값 없음)",
            "blocked_use": "primary release selector(주 해제 선택자)",
            "effect": "allows cost-margin repair without OOS selection(OOS 선택 없이 비용 여백 수리 허용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "eligibility_id": "direction_residual_auxiliary_target",
            "input_subject": "direction_residual_tag(방향 잔차 태그)",
            "eligibility_status": "eligible_for_guarded_training_auxiliary",
            "allowed_training_use": "auxiliary direction repair target(보조 방향 수리 목표)",
            "required_guard": "train-only and post-training control review(학습 전용 및 학습 후 대조 검토)",
            "blocked_use": "validation direction filter(검증 방향 필터)",
            "effect": "opens direction repair while preserving validation boundary(검증 경계 유지하며 방향 수리 열기)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "eligibility_id": "drawdown_pressure_continuous_only",
            "input_subject": "underwater_tag/drawdown_pressure_value(침수 태그/드로다운 압력값)",
            "eligibility_status": "binary_blocked_continuous_diagnostic_allowed",
            "allowed_training_use": "continuous diagnostic or sample weight candidate(연속 진단 또는 샘플 가중 후보)",
            "required_guard": f"underwater_ratio={summary['underwater_ratio']}",
            "blocked_use": "binary target(이진 목표)",
            "effect": "blocks overbroad drawdown binary label(과넓은 드로다운 이진 라벨 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "eligibility_id": "density_diagnostic_only",
            "input_subject": "density_deconcentration_matrix(밀도 탈집중 행렬)",
            "eligibility_status": "diagnostic_allowed_threshold_blocked",
            "allowed_training_use": "audit feature/monitor only(감사 피처/모니터 전용)",
            "required_guard": f"validation_pressure_rows={density['validation_pressure_rows']}",
            "blocked_use": "density threshold search(밀도 임계값 탐색)",
            "effect": "keeps density from becoming post-hoc selector(밀도가 사후 선택자가 되는 것 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "eligibility_id": "shifted_control_required_gate",
            "input_subject": "control_residual_isolation_matrix(대조 잔차 격리 행렬)",
            "eligibility_status": "required_post_training_gate",
            "allowed_training_use": "hard blocker after training(학습 후 강한 차단)",
            "required_guard": f"blocked_rows={control['blocked_rows']}",
            "blocked_use": "control relaxation(대조 완화)",
            "effect": "prevents runtime queue if residual remains(잔차가 남으면 런타임 대기열 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "eligibility_id": "wfo_precheck_required",
            "input_subject": "WFO/embargo feasibility(WFO/격리 가능성)",
            "eligibility_status": "required_training_split_precheck",
            "allowed_training_use": "split feasibility precondition(분할 가능성 전제)",
            "required_guard": f"feasible_rows={wfo['feasible_rows']}",
            "blocked_use": "post-selection WFO backfill(선택 후 WFO 사후 보강)",
            "effect": "keeps WFO before model choice(WFO를 모델 선택 전에 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_dz_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DZ_train_guarded_auxiliary_targets",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train guarded candidates using eligible auxiliary targets(적격 보조 목표로 방어 후보 학습)",
            "required_inputs": f"{rel(OBJECTIVE_FRAME)};{rel(TRAINING_ELIGIBILITY_MATRIX)}",
            "required_outputs": "trained_model_manifest.csv;candidate_scorecard.csv",
            "blocked_if_missing": "objective frame or eligibility matrix(목표 프레임 또는 적격성 행렬)",
            "forbidden_action": "no candidate selection or threshold tuning(후보 선택 또는 임계값 튜닝 금지)",
            "effect": "opens bounded training after input review(입력 검토 후 제한 학습 열기)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DZ_apply_density_diagnostic_only",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "carry density diagnostics without threshold search(임계값 탐색 없이 밀도 진단 전달)",
            "required_inputs": rel(DENSITY_INPUT_REVIEW),
            "required_outputs": "density_guard_audit.csv",
            "blocked_if_missing": "density review(밀도 검토)",
            "forbidden_action": "no density threshold tuning(밀도 임계값 튜닝 금지)",
            "effect": "prevents density repair-overfit(밀도 수리 과적합 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DZ_enforce_shifted_control_gate",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "enforce shifted-control gate after training(학습 후 이동 대조 게이트 강제)",
            "required_inputs": rel(CONTROL_INPUT_REVIEW),
            "required_outputs": "negative_control_scorecard.csv",
            "blocked_if_missing": "control review(대조 검토)",
            "forbidden_action": "no control relaxation(대조 완화 금지)",
            "effect": "keeps overfit guard active after new training(새 학습 후 과적합 방어 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DZ_use_wfo_precheck",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "use WFO precheck as split guard(WFO 사전검사를 분할 가드로 사용)",
            "required_inputs": rel(WFO_INPUT_REVIEW),
            "required_outputs": "split_guard_audit.csv",
            "blocked_if_missing": "WFO review(WFO 검토)",
            "forbidden_action": "no post-selection WFO backfill(선택 후 WFO 사후 보강 금지)",
            "effect": "keeps split discipline before model choice(모델 선택 전 분할 규율 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DZ_keep_runtime_firewall_closed",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "keep runtime firewall closed during training(학습 중 런타임 방화벽 닫힘 유지)",
            "required_inputs": rel(FIREWALL_REVIEW),
            "required_outputs": "release_disposition.csv",
            "blocked_if_missing": "firewall review(방화벽 검토)",
            "forbidden_action": "no MT5/Forward/Goal claim(MT5/전진/목표 주장 금지)",
            "effect": "separates training from release(학습과 해제 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DX inputs exist(필수 DX 입력 존재)"),
        ("parent_dx_gates_passed", final["dx_failed_gate_rows"] == 0, str(final["dx_failed_gate_rows"]), "0", "DX materialization usable(DX 물질화 사용 가능)"),
        ("parent_next_action_matches", final["dx_next_action"] == RUN_ID, str(final["dx_next_action"]), RUN_ID, "continues DX queue(DX 대기열을 이어감)"),
        ("objective_train_only", final["objective_split_values"] == "train", str(final["objective_split_values"]), "train", "objective frame excludes validation/OOS(목표 프레임 검증/OOS 제외)"),
        ("low_margin_tag_nonempty", final["low_margin_rows"] > 0, str(final["low_margin_rows"]), ">0", "low-margin tag populated(저여백 태그 채워짐)"),
        ("direction_residual_nonempty", final["direction_residual_rows"] > 0, str(final["direction_residual_rows"]), ">0", "direction residual tag populated(방향 잔차 태그 채워짐)"),
        ("drawdown_broadness_named", final["underwater_ratio"] > 0.95 and final["drawdown_binary_status"] == "blocked_continuous_only", f"{final['underwater_ratio']};{final['drawdown_binary_status']}", "broad_named", "broad drawdown binary tag limited(넓은 드로다운 이진 태그 제한)"),
        ("control_blocks_reconfirmed", final["control_block_rows"] >= 3, str(final["control_block_rows"]), ">=3", "control blockers remain named(대조 차단 유지 명명)"),
        ("wfo_precheck_feasible", final["wfo_feasible_rows"] == final["wfo_rows"], f"{final['wfo_feasible_rows']}/{final['wfo_rows']}", "all", "WFO precheck feasible(WFO 사전검사 가능)"),
        ("eligibility_rows_materialized", final["eligibility_rows"] == 6, str(final["eligibility_rows"]), "6", "training eligibility matrix materialized(학습 적격성 행렬 물질화)"),
        ("dz_queue_materialized", final["dz_queue_rows"] == 5, str(final["dz_queue_rows"]), "5", "DZ training queue opened(DZ 학습 대기열 열림)"),
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
        "time_axis": "DX train-only frame and review matrices; no new market rows(DX 학습 전용 프레임과 리뷰 행렬, 새 시장 행 없음)",
        "sample_scope": f"objective_rows={final['objective_rows']};split={final['objective_split_values']};models={final['objective_models']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']}",
        "feature_label_boundary": "objective frame train-only; validation/OOS absent(목표 프레임 학습 전용, 검증/OOS 없음)",
        "split_boundary": "WFO feasible as precheck only(WFO는 사전검사 가능성일 뿐)",
        "leakage_risk": "using drawdown binary tag despite broad coverage(넓은 침수 이진 태그를 그대로 쓰는 위험)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_guarded_training_with_limits",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "no model trained in DY; input eligibility review only(DY 모델 학습 없음, 입력 적격성 검토 전용)",
        "target_and_label": "low-margin and direction residual eligible; drawdown binary blocked(저여백/방향 잔차 적격, 드로다운 이진 차단)",
        "split_method": "train-only objective frame, WFO precheck for next run(학습 전용 목표 프레임, 다음 실행용 WFO 사전검사)",
        "selection_metric": "none(없음)",
        "secondary_metrics": "tag coverage, control block, WFO feasibility(태그 커버리지/대조 차단/WFO 가능성)",
        "threshold_policy": "no threshold tuning(임계값 튜닝 없음)",
        "overfit_risk": "auxiliary target overuse and control relaxation(보조 목표 과사용 및 대조 완화)",
        "calibration_risk": "not applicable; no probability calibration(해당 없음, 확률 보정 없음)",
        "comparison_baseline": rel(DX_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"low_margin={final['low_margin_rows']};direction_residual={final['direction_residual_rows']};underwater_ratio={final['underwater_ratio']}",
        "comparison_baseline": rel(DX_FINAL),
        "likely_drivers": "train-only tag coverage and broad drawdown tag(학습 전용 태그 커버리지와 넓은 드로다운 태그)",
        "segment_checks": f"density_pressure={final['density_validation_pressure_rows']};control_blocks={final['control_block_rows']};wfo={final['wfo_feasible_rows']}",
        "trade_shape": "input tag coverage only; no trading result(입력 태그 커버리지 전용, 거래 결과 없음)",
        "alternative_explanations": "tags may describe previous model behavior rather than robust alpha(태그가 강건 알파보다 이전 모델 행동을 설명할 수 있음)",
        "attribution_confidence": "medium_for_input_safety_not_for_performance(입력 안전성 중간, 성과 아님)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "objective/density/control/WFO/firewall reviews and eligibility matrix(목표/밀도/대조/WFO/방화벽 검토와 적격성 행렬)",
        "evidence_missing": "DZ training outputs, ONNX parity, MT5, forward evidence(DZ 학습 출력/ONNX 동등성/MT5/전진 근거)",
        "judgment_label": "input_review_completed_guarded_training_eligible",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "일부 입력은 학습 후보로 열리지만, 넓은 드로다운 이진 태그는 막아둔다.",
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
        "availability": "ignored_review_outputs_with_tracked_report(무시된 리뷰 출력과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DY Transfer Density Control Objective Input Review(전이/밀도/대조/목표 입력 검토)

## Conclusion(결론)

run337DY(337DY 실행)는 DX 입력을 검토했고, 제한된 guarded training(방어 학습)을 열 수 있다고 본다.

허용되는 것은 low_margin_trade_tag(저여백 거래 태그)와 direction_residual_tag(방향 잔차 태그)의 보조 목표 사용이다. underwater_tag(침수 이진 태그)는 `{final["underwater_ratio"]}` 비율로 너무 넓어서 binary target(이진 목표)으로 금지하고, drawdown_pressure_value(드로다운 압력값) 연속 진단으로만 허용한다.

이 작업은 review-only(검토 전용)이다. 새 학습, 후보 선택, 임계값 튜닝, MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 하지 않는다.

Effect(효과): run337DZ(337DZ 실행)는 적격 보조 목표만 사용하고 density/control/WFO/firewall(밀도/대조/WFO/방화벽) 가드를 유지한 guarded training(방어 학습)을 실행한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- objective_rows(목표 행): `{final["objective_rows"]}`
- low_margin_rows(저여백 행): `{final["low_margin_rows"]}`
- direction_residual_rows(방향 잔차 행): `{final["direction_residual_rows"]}`
- underwater_ratio(침수 비율): `{final["underwater_ratio"]}`
- control_block_rows(대조 차단 행): `{final["control_block_rows"]}`
- wfo_feasible_rows(WFO 가능 행): `{final["wfo_feasible_rows"]}/{final["wfo_rows"]}`
- eligibility_rows(적격성 행): `{final["eligibility_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DY

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 입력은 제한 학습에 적격이지만 드로다운 이진 태그는 막고, 학습 후 대조/WFO 검토를 필수로 둔다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(TRAINING_ELIGIBILITY_MATRIX)}`, `{rel(DZ_QUEUE)}`
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
        f"  Stage337 run337DY focus complete: transfer/density/control/objective input review(전이/밀도/대조/목표 입력 검토)를 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DZ(337DZ 실행)에서 guarded auxiliary-target training(보조 목표 방어 학습)을 실행하되 선택/MT5/Forward(전진)는 닫는다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DY focus complete")
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
    section = f"""## Stage337 run337DY(337DY 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 입력 검토로 제한 학습을 열었지만 선택/MT5/Forward(전진)는 주장하지 않는다. Goal(목표)은 주장하지 않는다."""
    current_text = append_once(current_text, section, "Stage337 run337DY(337DY 실행)")
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection_text, _ = read_text_lossless(SELECTED_STATUS)
    selection = selection_text
    for field_name, value in {
        "latest_run": f"`{RUN_ID}`",
        "latest_decision": f"`{DECISION}`",
        "current_run": f"`{NEXT_RUN_ID}`",
        "rebuild_status": f"`{STATUS}`",
        "actual_mt5_execution": "`not_run_dy_review_only`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "effect": "`다음은 guarded auxiliary-target training(보조 목표 방어 학습)이다.`",
    }.items():
        selection = replace_bullet_value(selection, field_name, value)
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337DY(337DY 실행) reviewed transfer/density/control/objective inputs and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DY(337DY 실행) reviewed transfer"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337DY reviewed transfer/density/control/objective inputs and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DY reviewed transfer"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "transfer_density_control_objective_input_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"low_margin={final['low_margin_rows']};direction_residual={final['direction_residual_rows']};underwater_ratio={final['underwater_ratio']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_performance_attribution_result_judgment",
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
        "scoreboard_lane": "data_integrity_model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"low_margin={final['low_margin_rows']};direction_residual={final['direction_residual_rows']};underwater_ratio={final['underwater_ratio']}",
        "guardrail_kpi": "drawdown_binary_blocked;control_gate_required;no_selection;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_performance_attribution",
        "evidence_scope": "repair inputs reviewed",
        "kpi_scope": "input_safety_training_eligibility",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_input_review",
        "family": "data_integrity_model_validation_performance_attribution",
        "question": "are DX repair inputs eligible for guarded training without repair-overfit",
        "metric_scope": "tag_coverage_control_wfo_eligibility",
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

    dx_final = read_json(DX_FINAL)
    dx_failed_gate_rows = sum(1 for row in read_csv(DX_GATES) if row.get("status") != "passed")
    objective_rows, objective_summary = review_objective_frame()
    density_rows, density_summary = review_density()
    control_rows, control_summary = review_control()
    wfo_rows, wfo_summary = review_wfo()
    firewall_rows, firewall_summary = review_firewall()
    eligibility_rows = build_eligibility(objective_summary, density_summary, control_summary, wfo_summary)
    queue_rows = build_dz_queue()
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dx_next_action": dx_final.get("next_action", ""),
        "dx_failed_gate_rows": dx_failed_gate_rows,
        "missing_inputs": len(missing),
        "objective_rows": int(objective_summary["rows"]),
        "objective_split_values": ",".join(objective_summary["split_values"]),
        "objective_models": int(objective_summary["models"]),
        "objective_source_rows": int(objective_summary["source_rows"]),
        "low_margin_rows": int(objective_summary["low_margin_rows"]),
        "direction_residual_rows": int(objective_summary["direction_residual_rows"]),
        "underwater_rows": int(objective_summary["underwater_rows"]),
        "underwater_ratio": float(objective_summary["underwater_ratio"]),
        "drawdown_binary_status": "blocked_continuous_only" if float(objective_summary["underwater_ratio"]) > 0.95 else "binary_allowed",
        "density_rows": int(density_summary["rows"]),
        "density_validation_pressure_rows": int(density_summary["validation_pressure_rows"]),
        "control_rows": int(control_summary["rows"]),
        "control_block_rows": int(control_summary["blocked_rows"]),
        "control_blocked_models": int(control_summary["blocked_models"]),
        "wfo_rows": int(wfo_summary["rows"]),
        "wfo_feasible_rows": int(wfo_summary["feasible_rows"]),
        "firewall_rows": int(firewall_summary["rows"]),
        "firewall_active_rows": int(firewall_summary["active_rows"]),
        "objective_review_rows": len(objective_rows),
        "density_review_rows": len(density_rows),
        "control_review_rows": len(control_rows),
        "wfo_review_rows": len(wfo_rows),
        "firewall_review_rows": len(firewall_rows),
        "eligibility_rows": len(eligibility_rows),
        "dz_queue_rows": len(queue_rows),
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
        write_csv(OBJECTIVE_INPUT_REVIEW, REVIEW_COLUMNS, objective_rows),
        write_csv(DENSITY_INPUT_REVIEW, REVIEW_COLUMNS, density_rows),
        write_csv(CONTROL_INPUT_REVIEW, REVIEW_COLUMNS, control_rows),
        write_csv(WFO_INPUT_REVIEW, REVIEW_COLUMNS, wfo_rows),
        write_csv(FIREWALL_REVIEW, REVIEW_COLUMNS, firewall_rows),
        write_csv(TRAINING_ELIGIBILITY_MATRIX, ELIGIBILITY_COLUMNS, eligibility_rows),
        write_csv(DZ_QUEUE, QUEUE_COLUMNS, queue_rows),
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
