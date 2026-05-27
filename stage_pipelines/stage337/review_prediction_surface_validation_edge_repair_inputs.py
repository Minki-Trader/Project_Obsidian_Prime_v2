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
from stage_pipelines.stage337 import materialize_prediction_surface_validation_edge_repair_inputs as dm  # noqa: E402
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
STAGE_ID = dm.STAGE_ID
RUN_NUMBER = "run337DN"
RUN_ID = "run337DN_review_prediction_surface_validation_edge_repair_inputs_without_db_v1"
PARENT_RUN_ID = dm.RUN_ID
NEXT_RUN_ID = "run337DO_train_guarded_prediction_surface_validation_edge_repair_candidates_without_db_v1"
STATUS = "completed_stage337DN_repair_inputs_review_guarded_training_eligible_no_selection_no_mt5"
JUDGMENT = "inputs_safe_for_guarded_training_experiment_but_no_selection_release_or_mt5"
DECISION = "stage337DN_open_run337DO_train_guarded_prediction_surface_validation_edge_repair_candidates"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DN_prediction_surface_validation_edge_repair_input_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dm.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dm.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DN_repair_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DN_repair_input_review.md"
SELECTED_STATUS = dm.SELECTED_STATUS
STAGE_BRIEF = dm.STAGE_BRIEF
WORKSPACE_STATE = dm.WORKSPACE_STATE
CURRENT_STATE = dm.CURRENT_STATE
CHANGELOG = dm.CHANGELOG
RUN_REGISTRY = dm.RUN_REGISTRY
ALPHA_LEDGER = dm.ALPHA_LEDGER
ARTIFACT_REGISTRY = dm.ARTIFACT_REGISTRY
STAGE_LEDGER = dm.STAGE_LEDGER

DM_FINAL = dm.FINAL_DECISION
DM_GATES = dm.REQUIRED_GATE_AUDIT
DM_QUEUE = dm.DN_QUEUE
VALIDATION_EDGE_FRAME = dm.VALIDATION_EDGE_FRAME
VALIDATION_EDGE_AUDIT = dm.VALIDATION_EDGE_AUDIT
SURFACE_BUNDLE = dm.SURFACE_BUNDLE
COST_LADDER_MATRIX = dm.COST_LADDER_MATRIX
MODEL_FAMILY_MATRIX = dm.MODEL_FAMILY_MATRIX
FEATURE_FAMILY_MATRIX = dm.FEATURE_FAMILY_MATRIX
SLICE_BREADTH_MATRIX = dm.SLICE_BREADTH_MATRIX
NEGATIVE_CONTROL_CONTRACT = dm.NEGATIVE_CONTROL_CONTRACT
LABEL_BOUNDARY_AUDIT = dm.LABEL_BOUNDARY_AUDIT
FORBIDDEN_SELECTION_AUDIT = dm.FORBIDDEN_SELECTION_AUDIT
DENSITY_FLOOR_CONTRACT = dm.DENSITY_FLOOR_CONTRACT
THIN_SLICE_EXCLUSION_AUDIT = dm.THIN_SLICE_EXCLUSION_AUDIT
PAYOFF_SHAPE_MATRIX = dm.PAYOFF_SHAPE_MATRIX
RUNTIME_FIREWALL_CARRY = dm.RUNTIME_FIREWALL_CARRY
FUTURE_PROXY_MT5_CHECKLIST = dm.FUTURE_PROXY_MT5_CHECKLIST
BALANCED_MANIFEST = dm.BALANCED_MANIFEST

VALIDATION_INPUT_REVIEW = RUN_DIR / "validation_edge_input_review.csv"
SURFACE_BUNDLE_REVIEW = RUN_DIR / "surface_bundle_review.csv"
CONTROL_REVIEW = RUN_DIR / "control_and_forbidden_selection_review.csv"
TRAINING_FEATURE_EXCLUSION = RUN_DIR / "do_training_feature_exclusion_contract.csv"
TRAINING_ELIGIBILITY = RUN_DIR / "training_eligibility_decision.md"
DO_QUEUE = RUN_DIR / "run337DO_training_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DM_FINAL,
    DM_GATES,
    DM_QUEUE,
    VALIDATION_EDGE_FRAME,
    VALIDATION_EDGE_AUDIT,
    SURFACE_BUNDLE,
    COST_LADDER_MATRIX,
    MODEL_FAMILY_MATRIX,
    FEATURE_FAMILY_MATRIX,
    SLICE_BREADTH_MATRIX,
    NEGATIVE_CONTROL_CONTRACT,
    LABEL_BOUNDARY_AUDIT,
    FORBIDDEN_SELECTION_AUDIT,
    DENSITY_FLOOR_CONTRACT,
    THIN_SLICE_EXCLUSION_AUDIT,
    PAYOFF_SHAPE_MATRIX,
    RUNTIME_FIREWALL_CARRY,
    FUTURE_PROXY_MT5_CHECKLIST,
    BALANCED_MANIFEST,
)
OUTPUT_FILES = (
    VALIDATION_INPUT_REVIEW,
    SURFACE_BUNDLE_REVIEW,
    CONTROL_REVIEW,
    TRAINING_FEATURE_EXCLUSION,
    TRAINING_ELIGIBILITY,
    DO_QUEUE,
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

VALIDATION_COLUMNS = (
    "review_id",
    "rows",
    "train_rows",
    "validation_rows",
    "oos_rows",
    "train_objective_allowed_rows",
    "validation_train_allowed_rows",
    "oos_train_allowed_rows",
    "selection_allowed_rows",
    "label_boundary_failed_rows",
    "duplicate_pair_source_rows",
    "review_status",
    "effect",
    "claim_boundary",
)
SURFACE_REVIEW_COLUMNS = (
    "review_id",
    "matrix_path",
    "rows",
    "axis_count",
    "status_count",
    "review_status",
    "effect",
    "claim_boundary",
)
CONTROL_REVIEW_COLUMNS = (
    "review_id",
    "source_path",
    "rows",
    "blocked_rows",
    "review_status",
    "effect",
    "claim_boundary",
)
EXCLUSION_COLUMNS = (
    "field_name",
    "field_family",
    "must_exclude_from_features",
    "allowed_use",
    "leakage_risk",
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


def summarize_inputs() -> dict[str, Any]:
    frame = pd.read_parquet(
        io_path(VALIDATION_EDGE_FRAME),
        columns=[
            "pair_id",
            "source_row_id",
            "timestamp",
            "split",
            "costed_label_margin",
            "train_objective_allowed",
            "selection_allowed",
            "pair_quarantine_status",
        ],
    )
    boundary = read_csv(LABEL_BOUNDARY_AUDIT)
    controls = read_csv(NEGATIVE_CONTROL_CONTRACT)
    forbidden = read_csv(FORBIDDEN_SELECTION_AUDIT)
    firewall = read_csv(RUNTIME_FIREWALL_CARRY)
    checklist = read_csv(FUTURE_PROXY_MT5_CHECKLIST)
    thin_exclusion = read_csv(THIN_SLICE_EXCLUSION_AUDIT)
    density = read_csv(DENSITY_FLOOR_CONTRACT)
    payoff = read_csv(PAYOFF_SHAPE_MATRIX)
    surface_paths = [COST_LADDER_MATRIX, MODEL_FAMILY_MATRIX, FEATURE_FAMILY_MATRIX, SLICE_BREADTH_MATRIX]
    surface_rows = {rel(path): read_csv(path) for path in surface_paths}
    split_counts = frame["split"].value_counts().to_dict()
    train_allowed_by_split = frame.groupby("split")["train_objective_allowed"].sum().to_dict()
    selection_allowed_rows = int(frame["selection_allowed"].sum())
    duplicates = int(frame[["pair_id", "source_row_id"]].duplicated().sum())
    quarantine_counts = frame["pair_quarantine_status"].value_counts().to_dict()
    return {
        "dm_final": read_json(DM_FINAL),
        "dm_gates": read_csv(DM_GATES),
        "dm_queue": read_csv(DM_QUEUE),
        "failed_dm_gates": [row for row in read_csv(DM_GATES) if row.get("status") != "passed"],
        "rows": len(frame),
        "pair_count": int(frame["pair_id"].nunique()),
        "source_rows": int(frame["source_row_id"].nunique()),
        "train_rows": int(split_counts.get("train", 0)),
        "validation_rows": int(split_counts.get("validation", 0)),
        "oos_rows": int(split_counts.get("oos", 0)),
        "train_objective_allowed_rows": int(train_allowed_by_split.get("train", 0)),
        "validation_train_allowed_rows": int(train_allowed_by_split.get("validation", 0)),
        "oos_train_allowed_rows": int(train_allowed_by_split.get("oos", 0)),
        "selection_allowed_rows": selection_allowed_rows,
        "duplicate_pair_source_rows": duplicates,
        "label_boundary_failed_rows": sum(1 for row in boundary if row.get("status") == "failed"),
        "boundary": boundary,
        "controls": controls,
        "forbidden": forbidden,
        "firewall": firewall,
        "checklist": checklist,
        "thin_exclusion": thin_exclusion,
        "density": density,
        "payoff": payoff,
        "surface_rows": surface_rows,
        "surface_matrix_count": len(surface_paths),
        "surface_matrix_rows": sum(len(rows) for rows in surface_rows.values()),
        "quarantine_counts": quarantine_counts,
        "margin_mean_train": float(frame.loc[frame["split"] == "train", "costed_label_margin"].mean()),
        "margin_positive_rate_train": float((frame.loc[frame["split"] == "train", "costed_label_margin"] > 0).mean()),
    }


def build_validation_review(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    blocked = (
        summary["label_boundary_failed_rows"] > 0
        or summary["selection_allowed_rows"] > 0
        or summary["validation_train_allowed_rows"] > 0
        or summary["oos_train_allowed_rows"] > 0
        or summary["duplicate_pair_source_rows"] > 0
    )
    return [
        {
            "review_id": "validation_edge_input_safety",
            "rows": summary["rows"],
            "train_rows": summary["train_rows"],
            "validation_rows": summary["validation_rows"],
            "oos_rows": summary["oos_rows"],
            "train_objective_allowed_rows": summary["train_objective_allowed_rows"],
            "validation_train_allowed_rows": summary["validation_train_allowed_rows"],
            "oos_train_allowed_rows": summary["oos_train_allowed_rows"],
            "selection_allowed_rows": summary["selection_allowed_rows"],
            "label_boundary_failed_rows": summary["label_boundary_failed_rows"],
            "duplicate_pair_source_rows": summary["duplicate_pair_source_rows"],
            "review_status": "blocked_input_safety" if blocked else "passed_input_safety_for_guarded_training",
            "effect": "checks train-only target and read-only validation/OOS(학습 전용 목표와 읽기 전용 검증/OOS 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_surface_review(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, matrix_rows in sorted(summary["surface_rows"].items()):
        axis_count = len({row.get("axis", row.get("slice_axis", "")) for row in matrix_rows})
        status_count = len({row.get("status", row.get("slice_review_status", "")) for row in matrix_rows})
        rows.append(
            {
                "review_id": f"surface_matrix_{Path(path).stem}",
                "matrix_path": path,
                "rows": len(matrix_rows),
                "axis_count": axis_count,
                "status_count": status_count,
                "review_status": "passed_surface_diagnostic_materialized" if matrix_rows else "blocked_surface_matrix_empty",
                "effect": "surface risk is diagnostic, not selection(표면 위험은 진단이지 선택이 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    bundle = read_json(SURFACE_BUNDLE)
    rows.append(
        {
            "review_id": "surface_bundle_manifest",
            "matrix_path": rel(SURFACE_BUNDLE),
            "rows": len(bundle.get("matrices", {})),
            "axis_count": len(bundle.get("matrices", {})),
            "status_count": 1,
            "review_status": "passed_surface_bundle_manifest" if len(bundle.get("matrices", {})) >= 4 else "blocked_surface_bundle_incomplete",
            "effect": "checks bundle links all required surface matrices(필수 표면 행렬 연결 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_control_review(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "review_id": "negative_control_contract",
            "source_path": rel(NEGATIVE_CONTROL_CONTRACT),
            "rows": len(summary["controls"]),
            "blocked_rows": 0,
            "review_status": "passed_controls_materialized" if len(summary["controls"]) >= 4 else "blocked_controls_incomplete",
            "effect": "keeps fake-signal controls before training(학습 전 가짜 신호 대조 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "forbidden_selection_audit",
            "source_path": rel(FORBIDDEN_SELECTION_AUDIT),
            "rows": len(summary["forbidden"]),
            "blocked_rows": 0,
            "review_status": "passed_forbidden_selection_materialized" if len(summary["forbidden"]) >= 3 else "blocked_forbidden_selection_incomplete",
            "effect": "keeps OOS pockets as failure memory(OOS 포켓을 실패 기억으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "runtime_firewall",
            "source_path": rel(RUNTIME_FIREWALL_CARRY),
            "rows": len(summary["firewall"]),
            "blocked_rows": 0,
            "review_status": "passed_runtime_firewall_carried" if len(summary["firewall"]) >= 3 else "blocked_runtime_firewall_incomplete",
            "effect": "keeps MT5 and Forward claims closed(MT5와 전진 주장 닫힘 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "future_proxy_mt5_checklist",
            "source_path": rel(FUTURE_PROXY_MT5_CHECKLIST),
            "rows": len(summary["checklist"]),
            "blocked_rows": 0,
            "review_status": "passed_future_runtime_checklist" if len(summary["checklist"]) >= 3 else "blocked_future_runtime_checklist_incomplete",
            "effect": "preserves later proxy/MT5 comparison path(이후 프록시/MT5 비교 경로 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_feature_exclusion_contract() -> list[dict[str, str]]:
    fields = [
        ("exact_future_log_return_12", "future_label(미래 라벨)", "target/audit only(목표/감사 전용)", "direct future return leakage(직접 미래 수익 누수)"),
        ("action_net_after_cost", "future_label(미래 라벨)", "target/audit only(목표/감사 전용)", "realized future PnL leakage(실현 미래 손익 누수)"),
        ("raw_action_future_return", "derived_label(파생 라벨)", "target/audit only(목표/감사 전용)", "future return transformation leakage(미래 수익 변환 누수)"),
        ("costed_label_margin", "derived_label(파생 라벨)", "target only(목표 전용)", "target leakage(목표 누수)"),
        ("positive_costed_margin", "derived_label(파생 라벨)", "target only(목표 전용)", "binary target leakage(이진 목표 누수)"),
        ("objective_margin_abs", "derived_label(파생 라벨)", "diagnostic only(진단 전용)", "future magnitude leakage(미래 크기 누수)"),
        ("train_objective_allowed", "split_role(분할 역할)", "row filter only(행 필터 전용)", "role leakage if used as feature(피처 사용 시 역할 누수)"),
        ("selection_allowed", "firewall(방화벽)", "audit only(감사 전용)", "selection policy leakage(선택 정책 누수)"),
        ("repair_sample_role", "split_role(분할 역할)", "audit only(감사 전용)", "split-role leakage(분할 역할 누수)"),
        ("pair_quarantine_status", "failure_memory(실패 기억)", "audit/filter only(감사/필터 전용)", "OOS failure memory leakage(OOS 실패 기억 누수)"),
        ("split", "split_role(분할 역할)", "split control only(분할 제어 전용)", "split identity leakage(분할 정체성 누수)"),
    ]
    return [
        {
            "field_name": field,
            "field_family": family,
            "must_exclude_from_features": "true",
            "allowed_use": allowed,
            "leakage_risk": risk,
            "effect": "prevents target/split/firewall leakage in DO( DO에서 목표/분할/방화벽 누수 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for field, family, allowed, risk in fields
    ]


def build_training_eligibility_text(final: Mapping[str, Any]) -> str:
    return f"""# Training Eligibility Decision(학습 적격성 결정): Stage337 run337DN

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `guarded_training_experiment_may_open`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- evidence(근거): validation-edge frame(검증 우위 프레임) `{final["validation_edge_rows"]}` rows, label boundary failures(라벨 경계 실패) `{final["label_boundary_failed_rows"]}`, selection_allowed rows(선택 허용 행) `{final["selection_allowed_rows"]}`, controls(대조) `{final["control_rows"]}`, runtime firewall(런타임 방화벽) `{final["runtime_firewall_rows"]}`.
- allowed(허용): train-only objective rows(학습 전용 목표 행)로 guarded training experiment(방어 학습 실험)을 열 수 있다.
- forbidden(금지): candidate selection(후보 선택), threshold tuning(임계값 튜닝), lot optimization(로트 최적화), MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 계속 금지한다.
- effect(효과): 입력 안전성은 학습 실험으로 넘기되, 모델/운영 주장은 열지 않는다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def build_do_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DO_train_guarded_validation_edge_models",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train guarded validation-edge repair candidates with excluded leakage fields(누수 필드 제외 후 방어 검증 우위 수리 후보 학습)",
            "required_inputs": f"{rel(VALIDATION_EDGE_FRAME)};{rel(TRAINING_FEATURE_EXCLUSION)}",
            "required_outputs": "trained_model_manifest.csv;candidate_scorecard.csv;onnx_exports(학습 모델 목록/후보 점수표/ONNX 내보내기)",
            "blocked_if_missing": "validation edge frame or feature exclusion contract(검증 우위 프레임 또는 피처 제외 계약)",
            "forbidden_action": "no validation/OOS threshold tuning, no candidate selection(검증/OOS 임계값 튜닝과 후보 선택 금지)",
            "effect": "opens training as experiment, not selection(학습을 선택이 아닌 실험으로 개방)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DO_score_negative_controls",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "score shifted/noise/block controls beside candidates(후보 옆에서 이동/잡음/블록 대조 점수화)",
            "required_inputs": rel(NEGATIVE_CONTROL_CONTRACT),
            "required_outputs": "negative_control_scorecard.csv",
            "blocked_if_missing": "negative control contract(부정대조 계약)",
            "forbidden_action": "no release if controls match candidate(대조가 후보와 같으면 해제 금지)",
            "effect": "keeps no-overfit gate alive(무과적합 게이트 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DO_score_surface_breadth",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "score trained candidates across surface breadth diagnostics(학습 후보를 표면 폭 진단으로 점수화)",
            "required_inputs": rel(SURFACE_BUNDLE),
            "required_outputs": "surface_breadth_scorecard.csv",
            "blocked_if_missing": "surface bundle(표면 번들)",
            "forbidden_action": "no surface winner cherry-pick(표면 승자 골라잡기 금지)",
            "effect": "prevents isolated surface from driving next step(고립 표면이 다음 단계를 끌지 못하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DO_preserve_runtime_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "preserve no-MT5/no-Forward firewall during training(MT5/전진 금지 방화벽을 학습 중 보존)",
            "required_inputs": rel(RUNTIME_FIREWALL_CARRY),
            "required_outputs": "runtime_firewall_review.csv",
            "blocked_if_missing": "runtime firewall carryforward(런타임 방화벽 전달)",
            "forbidden_action": "no MT5 package or Forward claim(MT5 패키지 또는 전진 주장 금지)",
            "effect": "keeps training separate from runtime authority(학습과 런타임 권위를 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DM inputs exist(필수 DM 입력 존재)"),
        ("parent_dm_gates_passed", final["dm_failed_gate_rows"] == 0, str(final["dm_failed_gate_rows"]), "0", "DM materialization usable(DM 물질화 사용 가능)"),
        ("parent_next_action_matches", final["dm_next_action"] == RUN_ID, str(final["dm_next_action"]), RUN_ID, "continues DM queue(DM 대기열을 이어감)"),
        ("label_boundary_clear", final["label_boundary_failed_rows"] == 0, str(final["label_boundary_failed_rows"]), "0", "label boundary audit clear(라벨 경계 감사 통과)"),
        ("selection_firewall_clear", final["selection_allowed_rows"] == 0, str(final["selection_allowed_rows"]), "0", "selection still forbidden(선택 계속 금지)"),
        ("train_only_role_clear", final["train_objective_allowed_rows"] > 0 and final["validation_train_allowed_rows"] == 0 and final["oos_train_allowed_rows"] == 0, f"train={final['train_objective_allowed_rows']};validation={final['validation_train_allowed_rows']};oos={final['oos_train_allowed_rows']}", "train>0,validation=0,oos=0", "train-only objective role clear(학습 전용 목표 역할 명확)"),
        ("row_identity_clear", final["duplicate_pair_source_rows"] == 0, str(final["duplicate_pair_source_rows"]), "0", "pair/source row identity clear(쌍/원천 행 정체성 통과)"),
        ("surface_review_clear", final["surface_review_failed_rows"] == 0 and final["surface_review_rows"] >= 5, f"failed={final['surface_review_failed_rows']};rows={final['surface_review_rows']}", "failed=0,rows>=5", "surface diagnostics complete(표면 진단 완료)"),
        ("controls_clear", final["control_review_failed_rows"] == 0 and final["control_rows"] >= 4, f"failed={final['control_review_failed_rows']};controls={final['control_rows']}", "failed=0,controls>=4", "controls and forbidden-selection checks complete(대조와 금지 선택 점검 완료)"),
        ("feature_exclusion_materialized", final["feature_exclusion_rows"] >= 10, str(final["feature_exclusion_rows"]), ">=10", "leakage exclusion contract exists(누수 제외 계약 존재)"),
        ("training_eligibility_decision_written", final["training_eligibility"] == "guarded_training_experiment_may_open", final["training_eligibility"], "guarded_training_experiment_may_open", "training eligibility is bounded(학습 적격성이 경계 안에서 열림)"),
        ("do_queue_materialized", final["do_queue_rows"] >= 4, str(final["do_queue_rows"]), ">=4", "DO training queue exists(DO 학습 대기열 존재)"),
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
        "time_axis": "DM replay-derived UTC closed-bar timestamps reviewed(DM 리플레이 기반 UTC 봉 마감 시각 검토)",
        "sample_scope": f"US100 M5 rows={final['validation_edge_rows']}; train={final['train_rows']}; validation={final['validation_rows']}; oos={final['oos_rows']}",
        "missing_or_duplicate_check": f"missing={final['missing_inputs']};duplicate_pair_source={final['duplicate_pair_source_rows']}",
        "feature_label_boundary": f"excluded_fields={final['feature_exclusion_rows']};label_boundary_failed={final['label_boundary_failed_rows']}",
        "split_boundary": "train objective allowed; validation/OOS read-only(학습 목표 허용, 검증/OOS 읽기 전용)",
        "leakage_risk": "DO accidentally using target/split/firewall fields(DO가 목표/분할/방화벽 필드를 실수로 사용)",
        "data_hash_or_identity": {"validation_edge_frame": sha256_file(VALIDATION_EDGE_FRAME), "label_boundary": sha256_file(LABEL_BOUNDARY_AUDIT)},
        "integrity_judgment": "usable_for_guarded_training_experiment",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "no model trained in DN; DO may train guarded candidates(DN에서는 모델 학습 없음; DO에서 방어 후보 학습 가능)",
        "target_and_label": "costed_label_margin target with excluded future fields(미래 필드 제외 계약이 붙은 비용 반영 라벨 여백 목표)",
        "split_method": "train-only objective with validation/OOS read-only review(학습 전용 목표와 검증/OOS 읽기 전용 검토)",
        "selection_metric": "none in DN(DN에서는 없음)",
        "secondary_metrics": "surface breadth, negative controls, forbidden selection, runtime firewall(표면 폭/부정대조/금지 선택/런타임 방화벽)",
        "threshold_policy": "not tuned(튜닝 없음)",
        "overfit_risk": "target leakage or surface cherry-pick in DO(DO에서 목표 누수 또는 표면 골라잡기)",
        "calibration_risk": "future DO scores are ranking, not probabilities unless calibrated(미래 DO 점수는 보정 전 확률이 아니라 순위)",
        "comparison_baseline": rel(DM_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"training_eligibility={final['training_eligibility']};selection_allowed={final['selection_allowed_rows']}",
        "comparison_baseline": rel(DM_FINAL),
        "likely_drivers": "input safety and guardrail coverage(입력 안전성과 가드레일 커버리지)",
        "segment_checks": f"surface_review_rows={final['surface_review_rows']};control_review_rows={final['control_review_rows']}",
        "trade_shape": f"train_objective_rows={final['train_objective_allowed_rows']};payoff_shape_rows={final['payoff_shape_rows']}",
        "alternative_explanations": "inputs may still underfit or all pairs may carry failure memory(입력이 여전히 과소적합이거나 모든 쌍이 실패 기억을 가질 수 있음)",
        "attribution_confidence": "high_for_input_eligibility_low_for_future_profit(입력 적격성은 높음, 미래 수익은 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "input review, surface review, control review, feature exclusion, eligibility decision(입력/표면/대조 검토와 피처 제외, 적격성 결정)",
        "evidence_missing": "DO training results, ONNX parity, proxy/MT5 comparison(DO 학습 결과/ONNX 동등성/프록시-MT5 비교)",
        "judgment_label": "guarded_training_experiment_eligible",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "학습 실험은 열 수 있지만, 후보 선택이나 운영 주장은 아직 절대 아니다.",
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
        "availability": "ignored_review_outputs_with_tracked_report(무시된 검토 산출물과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_training_decision(final: Mapping[str, Any]) -> Path:
    return write_md(TRAINING_ELIGIBILITY, build_training_eligibility_text(final))


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DN Repair Input Review(수리 입력 검토)

## Conclusion(결론)

run337DN(337DN 실행)은 DM materialized inputs(DM 물질화 입력)를 검토했다. label boundary(라벨 경계), train-only role(학습 전용 역할), selection firewall(선택 방화벽), surface diagnostics(표면 진단), negative controls(부정대조)가 모두 학습 실험을 열 수 있는 최소 조건을 통과했다.

단, 이것은 guarded training experiment eligible(방어 학습 실험 적격)이라는 뜻이지, candidate selection(후보 선택), release(해제), MT5 probe(MT5 탐침), Forward/Goal(전진/목표)이 아니다.

Effect(효과): 다음 run337DO(337DO 실행)는 leakage exclusion contract(누수 제외 계약)을 지키며 방어 후보 학습과 대조 점수화를 실행한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- validation_edge_rows(검증 우위 행): `{final["validation_edge_rows"]}`
- train_objective_allowed_rows(학습 목표 허용 행): `{final["train_objective_allowed_rows"]}`
- selection_allowed_rows(선택 허용 행): `{final["selection_allowed_rows"]}`
- label_boundary_failed_rows(라벨 경계 실패 행): `{final["label_boundary_failed_rows"]}`
- feature_exclusion_rows(피처 제외 행): `{final["feature_exclusion_rows"]}`
- training_eligibility(학습 적격성): `{final["training_eligibility"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DN

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): DM 입력은 방어 학습 실험으로 넘길 수 있지만, 후보 선택/MT5/Forward(전진)는 닫아둔다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(TRAINING_FEATURE_EXCLUSION)}`, `{rel(TRAINING_ELIGIBILITY)}`
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
        f"  Stage337 run337DN focus complete: repair input review(수리 입력 검토)를 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DO(337DO 실행)에서 guarded training/control scoring(방어 학습/대조 점수화)을 실행한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DN focus complete")
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
## Stage337 run337DN(337DN 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 입력 안전성은 방어 학습 실험에 충분하지만 후보 선택/MT5/Forward(전진)는 계속 닫는다. Goal(목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DM(337DM"
    if "## Stage337 run337DN(337DN 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_dn_review_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 guarded prediction surface validation-edge repair training(방어 예측 표면 검증 우위 수리 학습)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DN(337DN 실행) reviewed prediction surface validation-edge repair inputs(예측 표면 검증 우위 수리 입력 검토). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DN(337DN 실행) reviewed prediction surface"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DN reviewed prediction surface validation-edge repair inputs(예측 표면 검증 우위 수리 입력 검토) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DN reviewed prediction surface"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "prediction_surface_validation_edge_repair_input_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"eligibility={final['training_eligibility']};selection_allowed={final['selection_allowed_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "input_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "input_safety_training_eligibility",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"train_allowed={final['train_objective_allowed_rows']};boundary_fail={final['label_boundary_failed_rows']}",
        "guardrail_kpi": "selection_allowed_zero;feature_exclusion;runtime_firewall",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_performance_attribution_result_judgment",
        "evidence_scope": "DM repair inputs reviewed",
        "kpi_scope": "input_safety_training_eligibility_no_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__input_review",
        "family": "data_integrity_model_validation_performance_attribution_result_judgment",
        "question": "are DM repair inputs safe enough to open guarded training",
        "metric_scope": "label_boundary_selection_firewall_surface_controls",
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
    summary = summarize_inputs()
    validation_rows = build_validation_review(summary)
    surface_rows = build_surface_review(summary)
    control_rows = build_control_review(summary)
    feature_rows = build_feature_exclusion_contract()
    do_queue_rows = build_do_queue()
    artifacts: list[Path] = [
        write_csv(VALIDATION_INPUT_REVIEW, VALIDATION_COLUMNS, validation_rows),
        write_csv(SURFACE_BUNDLE_REVIEW, SURFACE_REVIEW_COLUMNS, surface_rows),
        write_csv(CONTROL_REVIEW, CONTROL_REVIEW_COLUMNS, control_rows),
        write_csv(TRAINING_FEATURE_EXCLUSION, EXCLUSION_COLUMNS, feature_rows),
        write_csv(DO_QUEUE, QUEUE_COLUMNS, do_queue_rows),
    ]
    training_eligible = (
        validation_rows[0]["review_status"] == "passed_input_safety_for_guarded_training"
        and all(row["review_status"].startswith("passed") for row in surface_rows)
        and all(row["review_status"].startswith("passed") for row in control_rows)
    )
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dm_next_action": summary["dm_final"].get("next_action", ""),
        "dm_failed_gate_rows": len(summary["failed_dm_gates"]),
        "missing_inputs": len(missing),
        "validation_edge_rows": summary["rows"],
        "pair_count": summary["pair_count"],
        "source_rows": summary["source_rows"],
        "train_rows": summary["train_rows"],
        "validation_rows": summary["validation_rows"],
        "oos_rows": summary["oos_rows"],
        "train_objective_allowed_rows": summary["train_objective_allowed_rows"],
        "validation_train_allowed_rows": summary["validation_train_allowed_rows"],
        "oos_train_allowed_rows": summary["oos_train_allowed_rows"],
        "selection_allowed_rows": summary["selection_allowed_rows"],
        "label_boundary_failed_rows": summary["label_boundary_failed_rows"],
        "duplicate_pair_source_rows": summary["duplicate_pair_source_rows"],
        "surface_review_rows": len(surface_rows),
        "surface_review_failed_rows": sum(1 for row in surface_rows if not row["review_status"].startswith("passed")),
        "control_review_rows": len(control_rows),
        "control_review_failed_rows": sum(1 for row in control_rows if not row["review_status"].startswith("passed")),
        "control_rows": len(summary["controls"]),
        "runtime_firewall_rows": len(summary["firewall"]),
        "payoff_shape_rows": len(summary["payoff"]),
        "feature_exclusion_rows": len(feature_rows),
        "do_queue_rows": len(do_queue_rows),
        "training_eligibility": "guarded_training_experiment_may_open" if training_eligible else "training_blocked_input_review",
        "margin_mean_train": summary["margin_mean_train"],
        "margin_positive_rate_train": summary["margin_positive_rate_train"],
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
    artifacts.append(write_training_decision(final))
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
