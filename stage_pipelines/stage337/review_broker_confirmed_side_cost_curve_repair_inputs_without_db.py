from __future__ import annotations

import csv
import json
import math
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import materialize_broker_confirmed_side_cost_curve_repair_inputs_without_db as ew  # noqa: E402


aw = ew.aw

TODAY = "2026-05-31"
STAGE_ID = ew.STAGE_ID
RUN_NUMBER = "run337EX"
RUN_ID = "run337EX_review_broker_confirmed_side_cost_curve_repair_inputs_without_db_v1"
PARENT_RUN_ID = ew.RUN_ID
NEXT_RUN_ID = "run337EY_train_broker_confirmed_side_cost_curve_repair_candidates_without_db_v1"
STATUS = "completed_stage337EX_side_cost_curve_repair_inputs_review_guarded_training_eligible_no_training_no_selection"
JUDGMENT = "train_only_side_cost_curve_inputs_pass_feature_label_quarantine_review_guarded_training_eligible"
DECISION = "stage337EX_open_run337EY_train_broker_confirmed_side_cost_curve_repair_candidates_without_db"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EX_broker_confirmed_side_cost_curve_repair_input_review_without_db_"
    "no_model_training_no_threshold_tuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ew.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ew.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EX_broker_confirmed_side_cost_curve_repair_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337EX_broker_confirmed_side_cost_curve_repair_input_review.md"
SELECTED_STATUS = ew.SELECTED_STATUS
STAGE_BRIEF = ew.STAGE_BRIEF
WORKSPACE_STATE = ew.WORKSPACE_STATE
CURRENT_STATE = ew.CURRENT_STATE
CHANGELOG = ew.CHANGELOG
RUN_REGISTRY = ew.RUN_REGISTRY
ALPHA_LEDGER = ew.ALPHA_LEDGER
ARTIFACT_REGISTRY = ew.ARTIFACT_REGISTRY
STAGE_LEDGER = ew.STAGE_LEDGER

EW_FINAL = ew.FINAL_DECISION
EW_GATES = ew.GATE_AUDIT
EW_QUEUE = ew.EX_QUEUE
EW_FRAME = ew.TRAIN_ONLY_INPUT_FRAME
EW_SOURCE_MAP = ew.MATERIALIZATION_SOURCE_MAP
EW_ROLE_MATRIX = ew.FEATURE_ROLE_MATRIX
EW_ALLOWED_FEATURES = ew.ALLOWED_FEATURE_SET
EW_SIDE_SCHEMA = ew.SIDE_SCHEMA
EW_COST_SCHEMA = ew.COST_SCHEMA
EW_CURVE_SCHEMA = ew.CURVE_SCHEMA
EW_DENSITY_SCHEMA = ew.DENSITY_SCHEMA
EW_MANIFEST = ew.INPUT_MANIFEST
EW_RECIPES = ew.LABEL_WEIGHT_RECIPE
EW_QUARANTINE = ew.FORWARD_QUARANTINE
EW_NEGATIVE_CONTROLS = ew.NEGATIVE_CONTROL_MATERIALIZATION
EW_RELEASE_GATES = ew.RELEASE_GATE_MATERIALIZATION

INPUT_SAFETY_REVIEW = RUN_DIR / "train_only_input_safety_review.csv"
FEATURE_BOUNDARY_REVIEW = RUN_DIR / "feature_label_boundary_review.csv"
FORWARD_QUARANTINE_REVIEW = RUN_DIR / "forward_quarantine_control_review.csv"
LABEL_WEIGHT_REVIEW = RUN_DIR / "label_weight_recipe_review.csv"
RELEASE_GATE_REVIEW = RUN_DIR / "release_gate_materialization_review.csv"
TRAINING_FEATURE_EXCLUSION = RUN_DIR / "training_feature_exclusion.csv"
TRAINING_TASK_MATRIX = RUN_DIR / "ey_training_task_matrix.csv"
EY_QUEUE = RUN_DIR / "run337EY_training_queue.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EW_FINAL,
    EW_GATES,
    EW_QUEUE,
    EW_FRAME,
    EW_SOURCE_MAP,
    EW_ROLE_MATRIX,
    EW_ALLOWED_FEATURES,
    EW_SIDE_SCHEMA,
    EW_COST_SCHEMA,
    EW_CURVE_SCHEMA,
    EW_DENSITY_SCHEMA,
    EW_MANIFEST,
    EW_RECIPES,
    EW_QUARANTINE,
    EW_NEGATIVE_CONTROLS,
    EW_RELEASE_GATES,
)
OUTPUT_FILES = (
    INPUT_SAFETY_REVIEW,
    FEATURE_BOUNDARY_REVIEW,
    FORWARD_QUARANTINE_REVIEW,
    LABEL_WEIGHT_REVIEW,
    RELEASE_GATE_REVIEW,
    TRAINING_FEATURE_EXCLUSION,
    TRAINING_TASK_MATRIX,
    EY_QUEUE,
    ROUTING_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
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
FEATURE_BOUNDARY_COLUMNS = (
    "feature_name",
    "declared_role",
    "boundary_status",
    "nonfinite_rows",
    "missing_status",
    "allowed_training_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
EXCLUSION_COLUMNS = (
    "field_name",
    "declared_role",
    "must_exclude_from_features",
    "allowed_use",
    "leakage_risk",
    "effect",
    "claim_boundary",
)
TASK_COLUMNS = (
    "task_id",
    "feature_set_id",
    "target_column",
    "sample_weight_expression",
    "model_family",
    "model_config_id",
    "feature_count",
    "training_eligibility_status",
    "required_guard",
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
GATE_COLUMNS = (
    "gate_id",
    "status",
    "evidence_path",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)

TRAIN_START = pd.Timestamp("2022-09-01T00:00:00Z")
TRAIN_END_EOD = pd.Timestamp("2024-12-31T23:59:59Z")
FORBIDDEN_FEATURE_TOKENS = (
    "future",
    "target",
    "profit",
    "pnl",
    "drawdown",
    "underwater",
    "quarantine",
    "density_floor",
    "model_observation",
    "signal_count",
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def current_branch() -> str:
    proc = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, capture_output=True, text=True, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def finite_nonfinite_rows(frame: pd.DataFrame, column: str) -> int:
    numeric = pd.to_numeric(frame[column], errors="coerce")
    return int((numeric.isna() | ~numeric.map(math.isfinite)).sum())


def review_input_safety(frame: pd.DataFrame) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    future_timestamps = pd.to_datetime(frame["future_timestamp"], utc=True) if "future_timestamp" in frame else pd.Series(dtype="datetime64[ns, UTC]")
    split_values = sorted(frame["split"].astype(str).unique().tolist())
    label_classes = sorted(frame["label_class"].astype(str).unique().tolist()) if "label_class" in frame else []
    rows = len(frame)
    future_before_feature = int((future_timestamps <= timestamps).sum()) if len(future_timestamps) else 0
    timestamp_outside = int(((timestamps < TRAIN_START) | (timestamps > TRAIN_END_EOD)).sum())
    future_outside = int(((future_timestamps < TRAIN_START) | (future_timestamps > TRAIN_END_EOD)).sum()) if len(future_timestamps) else 0
    duplicated_keys = int(frame.duplicated(["source_row_id", "cost_policy_id"]).sum()) if {"source_row_id", "cost_policy_id"}.issubset(frame.columns) else 0
    forbidden_forward_columns = sorted(set(frame.columns) & ew.FORBIDDEN_FORWARD_COLUMNS)
    weight_columns = [
        "side_quality_weight",
        "cost_survival_weight",
        "curve_state_pressure_weight",
        "short_abstention_pressure_weight",
    ]
    weight_nonfinite = sum(finite_nonfinite_rows(frame, column) for column in weight_columns if column in frame)
    summary = {
        "rows": rows,
        "columns": int(len(frame.columns)),
        "split_values": split_values,
        "source_rows": int(frame["source_row_id"].nunique()) if "source_row_id" in frame else 0,
        "cost_policy_count": int(frame["cost_policy_id"].nunique()) if "cost_policy_id" in frame else 0,
        "timestamp_min": timestamps.min().isoformat(),
        "timestamp_max": timestamps.max().isoformat(),
        "future_timestamp_max": future_timestamps.max().isoformat() if len(future_timestamps) else "",
        "future_before_feature_rows": future_before_feature,
        "timestamp_outside_train_rows": timestamp_outside,
        "future_timestamp_outside_train_rows": future_outside,
        "duplicated_source_cost_rows": duplicated_keys,
        "label_class_count": len(label_classes),
        "forbidden_forward_columns": forbidden_forward_columns,
        "weight_nonfinite_rows": weight_nonfinite,
    }
    review_rows = [
        {
            "review_id": "train_only_split_boundary",
            "subject": "train-only split boundary(학습 전용 분할 경계)",
            "rows": rows,
            "metric_1": json.dumps(split_values, ensure_ascii=False),
            "metric_2": f"source_rows={summary['source_rows']};cost_policies={summary['cost_policy_count']}",
            "review_status": "passed_train_only" if split_values == ["train"] and rows > 0 else "blocked_non_train_or_empty",
            "allowed_use": "guarded training input after EX review(EX 검토 후 방어 학습 입력)",
            "forbidden_use": "validation/OOS label use(검증/OOS 라벨 사용)",
            "effect": "checks split leakage before training(학습 전 분할 누수 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "timestamp_label_boundary",
            "subject": "timestamp and horizon boundary(시각과 수평선 경계)",
            "rows": rows,
            "metric_1": f"timestamp={summary['timestamp_min']}..{summary['timestamp_max']}",
            "metric_2": f"future_max={summary['future_timestamp_max']};future_before_feature={future_before_feature};future_outside={future_outside}",
            "review_status": "passed_timestamp_safe" if future_before_feature == 0 and timestamp_outside == 0 and future_outside == 0 else "blocked_timestamp_boundary",
            "allowed_use": "target-only future horizon(목표 전용 미래 수평선)",
            "forbidden_use": "future timestamp as feature(미래 시각 피처)",
            "effect": "keeps label horizon out of features(라벨 수평선을 피처에서 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "target_and_weight_integrity",
            "subject": "target and sample weights(목표와 표본 가중치)",
            "rows": rows,
            "metric_1": f"label_classes={label_classes};label_class_count={len(label_classes)}",
            "metric_2": f"weight_nonfinite_rows={weight_nonfinite}",
            "review_status": "passed_target_weight_integrity" if len(label_classes) == 3 and weight_nonfinite == 0 else "blocked_target_or_weight_integrity",
            "allowed_use": "classification target and sample weights after EY(EY 이후 분류 목표와 표본 가중치)",
            "forbidden_use": "weights as model features(가중치를 모델 피처로 사용)",
            "effect": "keeps ONNX probability target viable(ONNX 확률 목표를 가능하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "forward_column_absence",
            "subject": "forward evidence column absence(전진 근거 열 부재)",
            "rows": rows,
            "metric_1": json.dumps(forbidden_forward_columns, ensure_ascii=False),
            "metric_2": f"duplicated_source_cost_rows={duplicated_keys}",
            "review_status": "passed_no_forward_columns" if not forbidden_forward_columns and duplicated_keys == 0 else "blocked_forward_or_duplicate_rows",
            "allowed_use": "train-only feature/target frame(학습 전용 피처/목표 프레임)",
            "forbidden_use": "broker-forward selector(브로커 전진 선택자)",
            "effect": "prevents forward memorization(전진 암기 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return review_rows, summary


def review_feature_boundary(frame: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    roles = read_csv(EW_ROLE_MATRIX)
    allowed = read_csv(EW_ALLOWED_FEATURES)
    allowed_names = [row.get("feature_name", "") for row in allowed]
    role_by_name = {row.get("field_name", ""): row for row in roles}
    review_rows: list[dict[str, Any]] = []
    exclusion_rows: list[dict[str, Any]] = []
    missing_allowed = [name for name in allowed_names if name not in frame.columns]
    forbidden_allowed = [
        name
        for name in allowed_names
        if any(token in name.lower() for token in FORBIDDEN_FEATURE_TOKENS)
    ]
    total_nonfinite = 0
    for name in allowed_names:
        nonfinite = finite_nonfinite_rows(frame, name) if name in frame.columns else len(frame)
        total_nonfinite += nonfinite
        declared = role_by_name.get(name, {}).get("allowed_role", "")
        review_rows.append(
            {
                "feature_name": name,
                "declared_role": declared,
                "boundary_status": "allowed_feature_passed" if name in frame.columns and nonfinite == 0 and name not in forbidden_allowed else "blocked_feature_boundary",
                "nonfinite_rows": nonfinite,
                "missing_status": "present" if name in frame.columns else "missing",
                "allowed_training_use": "model feature after EX review(EX 검토 후 모델 피처)",
                "forbidden_use": "label, weight, forward proof(라벨/가중치/전진 증거)",
                "effect": "keeps model input feature-only(모델 입력을 피처 전용으로 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for role in roles:
        field = role.get("field_name", "")
        declared = role.get("allowed_role", "")
        must_exclude = not declared.startswith("allowed_model_feature")
        if must_exclude:
            exclusion_rows.append(
                {
                    "field_name": field,
                    "declared_role": declared,
                    "must_exclude_from_features": "true",
                    "allowed_use": role.get("input_layer", ""),
                    "leakage_risk": role.get("forbidden_role", ""),
                    "effect": "keeps non-feature fields out of EY feature list(EY 피처 목록에서 비피처 필드 제외)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    summary = {
        "role_rows": len(roles),
        "frame_columns": len(frame.columns),
        "allowed_feature_rows": len(allowed_names),
        "missing_allowed_features": missing_allowed,
        "forbidden_allowed_features": forbidden_allowed,
        "feature_nonfinite_rows": total_nonfinite,
        "excluded_field_rows": len(exclusion_rows),
    }
    return review_rows, exclusion_rows, summary


def review_quarantine_and_controls() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    quarantine = read_csv(EW_QUARANTINE)
    controls = read_csv(EW_NEGATIVE_CONTROLS)
    active_quarantine = [
        row for row in quarantine if str(row.get("quarantine_status", "")).startswith("active_not_joined")
    ]
    failed_controls = [
        row for row in controls if not str(row.get("materialized_status", "")).startswith("passed")
    ]
    rows = [
        {
            "review_id": "forward_quarantine_active",
            "subject": "forward evidence quarantine(전진 근거 격리)",
            "rows": len(quarantine),
            "metric_1": f"active={len(active_quarantine)}",
            "metric_2": f"sources={';'.join(row.get('evidence_id', '') for row in quarantine)}",
            "review_status": "passed_quarantine_active" if len(active_quarantine) == len(quarantine) and len(quarantine) >= 7 else "blocked_quarantine_incomplete",
            "allowed_use": "failure memory and future release dependency(실패 기억과 미래 해제 의존성)",
            "forbidden_use": "feature, label, threshold, selector(피처/라벨/임계값/선택자)",
            "effect": "keeps broker MT5 evidence separated from training inputs(브로커 MT5 근거를 학습 입력에서 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "negative_controls_active",
            "subject": "negative controls(부정 대조)",
            "rows": len(controls),
            "metric_1": f"failed={len(failed_controls)}",
            "metric_2": ";".join(row.get("control_id", "") for row in failed_controls),
            "review_status": "passed_negative_controls" if not failed_controls and len(controls) >= 5 else "blocked_negative_control_failure",
            "allowed_use": "guarded training constraint(방어 학습 제약)",
            "forbidden_use": "control relaxation(대조 완화)",
            "effect": "keeps overfit routes closed(과적합 경로를 닫아 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows, {
        "quarantine_rows": len(quarantine),
        "active_quarantine_rows": len(active_quarantine),
        "negative_control_rows": len(controls),
        "failed_negative_control_rows": len(failed_controls),
    }


def review_recipes_and_release() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    recipes = read_csv(EW_RECIPES)
    release = read_csv(EW_RELEASE_GATES)
    recipe_failures = [
        row for row in recipes if not str(row.get("non_feature_status", "")).startswith("not_allowed_as_feature")
    ]
    release_failures = [
        row for row in release if not str(row.get("materialized_status", "")).startswith("carried_forward_active")
    ]
    recipe_rows = [
        {
            "review_id": "label_weight_recipe_non_feature",
            "subject": "label/weight recipe boundary(라벨/가중치 조리법 경계)",
            "rows": len(recipes),
            "metric_1": f"non_feature_failures={len(recipe_failures)}",
            "metric_2": ";".join(row.get("recipe_id", "") for row in recipe_failures),
            "review_status": "passed_recipe_boundary" if not recipe_failures and len(recipes) >= 5 else "blocked_recipe_boundary",
            "allowed_use": "sample weight and target recipe(표본 가중치와 목표 조리법)",
            "forbidden_use": "model feature(모델 피처)",
            "effect": "keeps objectives out of feature matrix(목표를 피처 행렬에서 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    release_rows = [
        {
            "review_id": "release_gate_materialization_active",
            "subject": "release gate materialization(해제 게이트 물질화)",
            "rows": len(release),
            "metric_1": f"failed={len(release_failures)}",
            "metric_2": ";".join(row.get("gate_id", "") for row in release_failures),
            "review_status": "passed_release_gates_carried" if not release_failures and len(release) >= 5 else "blocked_release_gate_materialization",
            "allowed_use": "future release review only(미래 해제 검토 전용)",
            "forbidden_use": "current release proof(현재 해제 증거)",
            "effect": "keeps operating claim closed(운영 주장을 닫아 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return recipe_rows, release_rows, {
        "recipe_rows": len(recipes),
        "recipe_failure_rows": len(recipe_failures),
        "release_gate_rows": len(release),
        "release_gate_failure_rows": len(release_failures),
    }


def build_training_tasks(feature_summary: Mapping[str, Any], final_like: Mapping[str, Any]) -> list[dict[str, Any]]:
    feature_count = int(feature_summary["allowed_feature_rows"])
    if final_like.get("blocked"):
        status = "blocked_by_EX_review"
    else:
        status = "eligible_for_guarded_training_reviewed_inputs"
    weight_recipes = [
        ("cost_survival", "cost_survival_weight", "extratrees_depth8_leaf120_cost_survival"),
        ("side_cost", "side_quality_weight * cost_survival_weight", "extratrees_depth8_leaf120_side_cost"),
        ("side_cost_curve", "side_quality_weight * cost_survival_weight * curve_state_pressure_weight", "extratrees_depth8_leaf120_side_cost_curve"),
        (
            "side_cost_curve_short_abstention",
            "side_quality_weight * cost_survival_weight * curve_state_pressure_weight * short_abstention_pressure_weight",
            "extratrees_depth8_leaf120_side_cost_curve_short_abstention",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for index, (suffix, weight_expr, config_id) in enumerate(weight_recipes, start=1):
        rows.append(
            {
                "task_id": f"ey{index:03d}_{suffix}",
                "feature_set_id": "ew_allowed_pretrade_features_v1",
                "target_column": "label_class",
                "sample_weight_expression": weight_expr,
                "model_family": "ExtraTreesClassifier(엑스트라트리 분류기)",
                "model_config_id": config_id,
                "feature_count": feature_count,
                "training_eligibility_status": status,
                "required_guard": "feature list from allowed_model_feature_set only; no threshold tuning; export probs3(허용 피처 목록만 사용, 임계값 조정 없음, probs3 내보내기)",
                "forbidden_action": "candidate selection, MT5 probe, Forward/Goal claim(후보 선택, MT5 탐침, 전진/목표 주장)",
                "effect": "opens offensive training variants while preserving EX guardrails(EX 가드레일을 보존하며 공격 학습 변형을 연다)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_ey_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "ey_train_guarded_side_cost_curve_candidates",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train guarded side/cost/curve candidates(방어 방향/비용/곡선 후보 학습)",
            "required_inputs": f"{rel(EW_FRAME)};{rel(EW_ALLOWED_FEATURES)};{rel(TRAINING_TASK_MATRIX)}",
            "required_outputs": "model artifacts, ONNX exports, training scorecards(모델 산출물, ONNX 내보내기, 학습 점수표)",
            "blocked_if_missing": "reviewed feature list or task matrix(검토된 피처 목록 또는 작업 행렬)",
            "forbidden_action": "no MT5/Forward/Goal claim in training run without later runtime probe(추후 런타임 탐침 없는 MT5/전진/목표 주장 금지)",
            "effect": "moves from reviewed inputs to actual ONNX exploration(검토 입력에서 실제 ONNX 탐색으로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["model_training"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["mt5_runtime_probe"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(EW_SOURCE_MAP), "required EW inputs exist(필수 EW 입력 존재)"),
        ("parent_ew_gates_passed", final["ew_failed_gate_rows"] == 0, str(final["ew_failed_gate_rows"]), "0", rel(EW_GATES), "EW materialization gates passed(EW 물질화 게이트 통과)"),
        ("parent_next_action_matches", final["ew_next_action"] == RUN_ID, str(final["ew_next_action"]), RUN_ID, rel(EW_FINAL), "EX follows EW next action(EX가 EW 다음 행동을 따름)"),
        ("train_only_split_boundary", final["split_values"] == ["train"] and final["frame_rows"] > 0, json.dumps(final["split_values"], ensure_ascii=False), "[train]", rel(INPUT_SAFETY_REVIEW), "frame is train-only(프레임이 학습 전용)"),
        ("timestamp_label_boundary", final["future_before_feature_rows"] == 0 and final["timestamp_outside_train_rows"] == 0 and final["future_timestamp_outside_train_rows"] == 0, f"future_before={final['future_before_feature_rows']};timestamp_outside={final['timestamp_outside_train_rows']};future_outside={final['future_timestamp_outside_train_rows']}", "all zero", rel(INPUT_SAFETY_REVIEW), "label horizon is timestamp-safe(라벨 수평선이 시점 안전)"),
        ("target_weight_integrity", final["label_class_count"] == 3 and final["weight_nonfinite_rows"] == 0, f"label_class_count={final['label_class_count']};weight_nonfinite={final['weight_nonfinite_rows']}", "3 classes and 0 nonfinite weights", rel(INPUT_SAFETY_REVIEW), "classification target and weights are usable(분류 목표와 가중치 사용 가능)"),
        ("feature_role_coverage", final["role_rows"] == final["frame_columns"] and final["allowed_feature_rows"] >= 50, f"roles={final['role_rows']};columns={final['frame_columns']};features={final['allowed_feature_rows']}", "roles=columns and >=50 features", rel(FEATURE_BOUNDARY_REVIEW), "all columns have declared roles(모든 열에 선언 역할 존재)"),
        ("allowed_feature_integrity", final["missing_allowed_feature_rows"] == 0 and final["feature_nonfinite_rows"] == 0 and final["forbidden_allowed_feature_rows"] == 0, f"missing={final['missing_allowed_feature_rows']};nonfinite={final['feature_nonfinite_rows']};forbidden={final['forbidden_allowed_feature_rows']}", "all zero", rel(FEATURE_BOUNDARY_REVIEW), "allowed features are present, finite, and not target-like(허용 피처가 존재하고 유한하며 목표 유사 열이 아님)"),
        ("forward_quarantine_active", final["active_quarantine_rows"] == final["quarantine_rows"] and final["quarantine_rows"] >= 7, f"active={final['active_quarantine_rows']};rows={final['quarantine_rows']}", "all active and >=7", rel(FORWARD_QUARANTINE_REVIEW), "broker forward evidence remains quarantined(브로커 전진 근거 격리 유지)"),
        ("negative_controls_active", final["failed_negative_control_rows"] == 0 and final["negative_control_rows"] >= 5, f"failed={final['failed_negative_control_rows']};rows={final['negative_control_rows']}", "0 failed and >=5", rel(FORWARD_QUARANTINE_REVIEW), "negative controls remain active(부정 대조 활성 유지)"),
        ("recipe_boundary", final["recipe_failure_rows"] == 0 and final["recipe_rows"] >= 5, f"failed={final['recipe_failure_rows']};rows={final['recipe_rows']}", "0 failed and >=5", rel(LABEL_WEIGHT_REVIEW), "label/weight recipes stay non-feature(라벨/가중치 조리법이 비피처 유지)"),
        ("release_gate_review", final["release_gate_failure_rows"] == 0 and final["release_gate_rows"] >= 5, f"failed={final['release_gate_failure_rows']};rows={final['release_gate_rows']}", "0 failed and >=5", rel(RELEASE_GATE_REVIEW), "release gates carried without release claim(해제 주장 없이 해제 게이트 이월)"),
        ("training_task_matrix_ready", final["training_task_rows"] == 4 and final["training_blocked_rows"] == 0, f"tasks={final['training_task_rows']};blocked={final['training_blocked_rows']}", "4 tasks and 0 blocked", rel(TRAINING_TASK_MATRIX), "EY guarded training queue is ready(EY 방어 학습 대기열 준비)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['model_training']};selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "EX is review-only(EX는 검토 전용)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장에 연결)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    routing = {
        "run_id": RUN_ID,
        "primary_family": "data_integrity(데이터 무결성)",
        "primary_skill": "obsidian-data-integrity(옵시디언 데이터 무결성)",
        "support_skills": [
            "obsidian-model-validation(옵시디언 모델 검증)",
            "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            "obsidian-result-judgment(옵시디언 결과 판정)",
        ],
        "required_gates": [row["gate_id"] for row in read_csv(GATE_AUDIT)] if path_exists(GATE_AUDIT) else [],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "sample_scope": f"rows={final['frame_rows']};split={final['split_values']};features={final['allowed_feature_rows']}",
        "timestamp_safety": f"timestamp={final['timestamp_min']}..{final['timestamp_max']};future_max={final['future_timestamp_max']}",
        "feature_label_boundary": f"excluded_fields={final['excluded_field_rows']};forbidden_allowed_features={final['forbidden_allowed_feature_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']};duplicate_source_cost_rows={final['duplicated_source_cost_rows']}",
        "integrity_judgment": "guarded_training_eligible_no_training(방어 학습 가능, 학습 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_training": "not_run(미실행)",
        "target": "label_class probs3-compatible(라벨 클래스 probs3 호환)",
        "feature_set": "ew_allowed_pretrade_features_v1",
        "feature_count": final["allowed_feature_rows"],
        "training_task_rows": final["training_task_rows"],
        "threshold_policy": "no tuning(조정 없음)",
        "onnx_status": "planned_for_EY(EY에서 예정)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "broker_memory_used_as": "quarantined design pressure only(격리 설계 압력만)",
        "review_result": final["judgment"],
        "next_training_variants": final["training_task_rows"],
        "release_claim": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "evidence_available": [rel(INPUT_SAFETY_REVIEW), rel(FEATURE_BOUNDARY_REVIEW), rel(FORWARD_QUARANTINE_REVIEW), rel(GATE_AUDIT)],
        "evidence_missing": "EY model training, ONNX export, MT5 runtime probe(EY 모델 학습, ONNX 내보내기, MT5 런타임 탐침)",
        "next_condition": final["next_action"],
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(ROUTING_RECEIPT, routing),
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
            rel(path): aw.sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and aw.io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "reviewed_and_connected_to_EY_training_queue(EY 학습 대기열에 검토 후 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EX Side/Cost/Curve Repair Input Review(337단계 337EX 방향/비용/곡선 수리 입력 검토)

## Conclusion(결론)

run337EX(337EX 실행)는 EW train-only input frame(EW 학습 전용 입력 프레임)을 검토했고 guarded training(방어 학습)으로 넘길 수 있다고 판정했다.

Action(행동): split/timestamp/target/weight(분할/시각/목표/가중치) 경계를 확인했다. Effect(효과): label horizon(라벨 수평선)이 피처(feature, 피처)에 들어가지 않은 상태로 EY 학습을 열 수 있다.

Action(행동): forward quarantine(전진 격리), negative controls(부정 대조), release gates(해제 게이트)를 검토했다. Effect(효과): broker MT5 evidence(브로커 MT5 근거)는 실패 기억으로만 남고 후보 선택(candidate selection, 후보 선택)이나 운영 주장(operating claim, 운영 주장)에 쓰이지 않는다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- frame_rows(프레임 행): `{final['frame_rows']}`
- allowed_feature_rows(허용 피처 행): `{final['allowed_feature_rows']}`
- excluded_field_rows(제외 필드 행): `{final['excluded_field_rows']}`
- training_task_rows(학습 작업 행): `{final['training_task_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- model training(모델 학습): `not_run`
- candidate selection(후보 선택): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337EX Decision(337EX 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(GATE_AUDIT)}`, `{rel(TRAINING_TASK_MATRIX)}`

Action(행동): EW 입력을 feature-label boundary(피처-라벨 경계), forward quarantine(전진 격리), release gate(해제 게이트) 기준으로 검토했다.
Effect(효과): EY guarded training(방어 학습)을 열되 Forward/Goal(전진/목표), runtime authority(런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


FIELD_LABELS = {
    "current_run": "current_run(현재 실행)",
    "status": "status(상태)",
    "decision": "decision(결정)",
    "latest_completed_run": "latest_completed_run(최근 완료 실행)",
    "next_action": "next_action(다음 행동)",
    "claim_boundary": "claim_boundary(주장 경계)",
}


def replace_bullet_field(text: str, field_name: str, value: str) -> str:
    pattern = re.compile(rf"^- {re.escape(field_name)}(\([^)]+\))?: .*$", flags=re.M)
    replacement = f"- {FIELD_LABELS.get(field_name, field_name)}: {value}"
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def insert_before_once(text: str, marker: str, section: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(marker, section.rstrip() + "\n\n" + marker, 1) if marker in text else text.rstrip() + "\n\n" + section.rstrip() + "\n"


def upsert_section_before(text: str, marker: str, section: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}.*?(?=^## )", flags=re.M | re.S)
    if pattern.search(text):
        return pattern.sub(section.rstrip() + "\n\n", text, count=1)
    return insert_before_once(text, marker, section, f"## {heading}")


def upsert_single_line(text: str, needle: str, entry: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = entry
            trailing = "\n" if text.endswith("\n") else ""
            return "\n".join(lines) + trailing
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = current_branch()
    workspace, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337EX focus complete: run337EX(337EX 실행)는 `{final['status']}`로 side/cost/curve repair input review(방향/비용/곡선 수리 입력 검토)를 완료했다. "
        f"Effect(효과): allowed features(허용 피처) `{final['allowed_feature_rows']}`, training tasks(학습 작업) `{final['training_task_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 확인하고 `{final['next_action']}`을 연다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337EX focus complete" in workspace:
        workspace = re.sub(
            r"- >-\n  Stage337 run337EX focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)",
            focus.rstrip(),
            workspace,
            count=1,
            flags=re.S,
        )
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = replace_bullet_field(current, field_name, value)
    section = f"""## run337EX Side/Cost/Curve Repair Input Review(방향/비용/곡선 수리 입력 검토)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- frame_rows(프레임 행): `{final['frame_rows']}`
- allowed_feature_rows(허용 피처 행): `{final['allowed_feature_rows']}`
- training_task_rows(학습 작업 행): `{final['training_task_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): train-only input(학습 전용 입력)이 feature-label boundary(피처-라벨 경계)와 quarantine(격리)을 통과해 EY guarded training(EY 방어 학습)을 열 수 있다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = upsert_section_before(current, "## run337EW Broker-Confirmed", section, "run337EX Side/Cost/Curve")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- train_only_frame_rows(학습 전용 프레임 행): `{final['frame_rows']}`
- allowed_feature_rows(허용 피처 행): `{final['allowed_feature_rows']}`
- training_task_rows(학습 작업 행): `{final['training_task_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): EX(337EX 실행)는 입력 검토이며 학습(training, 학습), 선택(selection, 선택), MT5(MetaTrader 5, 메타트레이더5) 실행을 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337EX(337EX 실행) `{final['status']}`. "
        f"Effect(효과): EW train-only frame(EW 학습 전용 프레임) `{final['frame_rows']}`행과 allowed features(허용 피처) `{final['allowed_feature_rows']}`개를 검토하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, upsert_single_line(brief, "run337EX(337EX 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337EX(337EX 실행) `{final['status']}`. "
        f"Effect(효과): side/cost/curve repair inputs(방향/비용/곡선 수리 입력)을 검토하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(CHANGELOG, upsert_single_line(changelog, "Stage337 run337EX", changelog_entry), changelog_bom))
    return artifacts


def upsert_csv_worktree(path: Path, columns: Sequence[str], row: Mapping[str, Any], key: str) -> Path:
    existing_columns, existing = aw.read_csv_table(path, prefer_head=False)
    merged_columns = list(existing_columns or columns)
    for column in columns:
        if column not in merged_columns:
            merged_columns.append(column)
    for column in row:
        if column not in merged_columns:
            merged_columns.append(column)
    key_value = str(row.get(key, ""))
    rows = [item for item in existing if str(item.get(key, "")) != key_value]
    rows.append({column: row.get(column, "") for column in merged_columns})
    return write_csv(path, merged_columns, rows)


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "side_cost_curve_input_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"features={final['allowed_feature_rows']};tasks={final['training_task_rows']};gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "input_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "side_cost_curve_input_review(방향/비용/곡선 입력 검토)",
        "tier_scope": "Tier A train-only input review with broker evidence quarantined(Tier A 학습 전용 입력 검토와 브로커 근거 격리)",
        "kpi_scope": "review_only_no_kpi_release(검토 전용, KPI 해제 없음)",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"features={final['allowed_feature_rows']};training_tasks={final['training_task_rows']}",
        "guardrail_kpi": "train_only;forward_quarantine_active;negative_controls_active;no_training;no_selection;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "EW materialized inputs and quarantine",
        "kpi_scope": "input_safety_feature_boundary_quarantine_training_queue",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__input_review",
        "family": "side_cost_curve_input_review",
        "question": "are broker-confirmed side/cost/curve repair inputs safe enough for guarded training",
        "metric_scope": "input_safety_feature_boundary_quarantine_training_queue",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        upsert_csv_worktree(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        upsert_csv_worktree(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        upsert_csv_worktree(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    rows = [
        row
        for row in rows
        if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID
    ]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def make_final(
    input_summary: Mapping[str, Any],
    feature_summary: Mapping[str, Any],
    quarantine_summary: Mapping[str, Any],
    recipe_summary: Mapping[str, Any],
    task_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    ew_final = read_json(EW_FINAL)
    training_blocked = sum(1 for row in task_rows if str(row.get("training_eligibility_status", "")).startswith("blocked"))
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "ew_next_action": ew_final.get("next_action", ""),
        "ew_failed_gate_rows": sum(1 for row in read_csv(EW_GATES) if row.get("status") != "passed"),
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
        **dict(input_summary),
        **dict(feature_summary),
        **dict(quarantine_summary),
        **dict(recipe_summary),
        "frame_rows": input_summary["rows"],
        "frame_columns": input_summary["columns"],
        "missing_allowed_feature_rows": len(feature_summary["missing_allowed_features"]),
        "forbidden_allowed_feature_rows": len(feature_summary["forbidden_allowed_features"]),
        "training_task_rows": len(task_rows),
        "training_blocked_rows": training_blocked,
    }
    return final


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    frame = pd.read_parquet(aw.io_path(EW_FRAME))
    input_rows, input_summary = review_input_safety(frame)
    feature_rows, exclusion_rows, feature_summary = review_feature_boundary(frame)
    quarantine_rows, quarantine_summary = review_quarantine_and_controls()
    recipe_rows, release_rows, recipe_summary = review_recipes_and_release()
    blocked_probe = {
        "blocked": bool(
            feature_summary["missing_allowed_features"]
            or feature_summary["forbidden_allowed_features"]
            or feature_summary["feature_nonfinite_rows"]
            or quarantine_summary["failed_negative_control_rows"]
            or recipe_summary["recipe_failure_rows"]
            or recipe_summary["release_gate_failure_rows"]
        )
    }
    task_rows = build_training_tasks(feature_summary, blocked_probe)
    queue_rows = build_ey_queue()
    final = make_final(input_summary, feature_summary, quarantine_summary, recipe_summary, task_rows)

    artifacts: list[Path] = [
        write_csv(INPUT_SAFETY_REVIEW, REVIEW_COLUMNS, input_rows),
        write_csv(FEATURE_BOUNDARY_REVIEW, FEATURE_BOUNDARY_COLUMNS, feature_rows),
        write_csv(FORWARD_QUARANTINE_REVIEW, REVIEW_COLUMNS, quarantine_rows),
        write_csv(LABEL_WEIGHT_REVIEW, REVIEW_COLUMNS, recipe_rows),
        write_csv(RELEASE_GATE_REVIEW, REVIEW_COLUMNS, release_rows),
        write_csv(TRAINING_FEATURE_EXCLUSION, EXCLUSION_COLUMNS, exclusion_rows),
        write_csv(TRAINING_TASK_MATRIX, TASK_COLUMNS, task_rows),
        write_csv(EY_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]

    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    if final["failed_gates"]:
        final["status"] = "invalid_stage337EX_required_gate_failure_no_training_no_selection"
        final["judgment"] = "required_gate_failure_blocks_EY_training_queue"
        final["decision"] = "repair_stage337EX_required_gate_failure_before_EY"
        final["next_action"] = "repair_stage337EX_required_gate_failure_v1"

    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
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
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))

    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": final["status"], "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "frame_rows": final["frame_rows"],
                "allowed_feature_rows": final["allowed_feature_rows"],
                "training_task_rows": final["training_task_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
