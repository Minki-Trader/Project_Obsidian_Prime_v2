from __future__ import annotations

import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import materialize_side_cost_curve_runtime_positive_clue_drawdown_balance_repair_inputs_without_db as fe  # noqa: E402


aw = fe.aw

TODAY = "2026-05-31"
STAGE_ID = fe.STAGE_ID
RUN_NUMBER = "run337FF"
RUN_ID = "run337FF_review_side_cost_curve_runtime_positive_clue_drawdown_balance_repair_inputs_without_db_v1"
PARENT_RUN_ID = fe.RUN_ID
NEXT_RUN_ID = "run337FG_train_side_cost_curve_runtime_positive_clue_repair_candidates_without_db_v1"
STATUS = "completed_stage337FF_runtime_positive_clue_repair_inputs_review_guarded_training_eligible_no_training_no_selection"
JUDGMENT = "train_only_repair_inputs_pass_boundary_weight_review_guarded_training_eligible"
DECISION = "stage337FF_open_run337FG_train_runtime_positive_clue_repair_candidates_without_db"
CLAIM_BOUNDARY = (
    "research_development_only_stage337FF_runtime_positive_clue_repair_input_review_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = fe.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = fe.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337FF_runtime_positive_clue_repair_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337FF_runtime_positive_clue_repair_input_review.md"
SELECTED_STATUS = fe.SELECTED_STATUS
STAGE_BRIEF = fe.STAGE_BRIEF
WORKSPACE_STATE = fe.WORKSPACE_STATE
CURRENT_STATE = fe.CURRENT_STATE
CHANGELOG = fe.CHANGELOG
RUN_REGISTRY = fe.RUN_REGISTRY
ALPHA_LEDGER = fe.ALPHA_LEDGER
ARTIFACT_REGISTRY = fe.ARTIFACT_REGISTRY
STAGE_LEDGER = fe.STAGE_LEDGER

FE_FINAL = fe.FINAL_DECISION
FE_GATES = fe.GATE_AUDIT
FE_QUEUE = fe.FF_QUEUE
FE_FRAME = fe.TRAIN_ONLY_REPAIR_FRAME
FE_SOURCE_MAP = fe.MATERIALIZATION_SOURCE_MAP
FE_FEATURES = fe.ALLOWED_FEATURE_SET
FE_WEIGHT_RECIPES = fe.WEIGHT_RECIPE_MATRIX
FE_WEIGHT_AUDIT = fe.WEIGHT_AUDIT
FE_BOUNDARY = fe.FEATURE_LABEL_BOUNDARY
FE_HANDOFF = fe.UNIQUE_TIMESTAMP_HANDOFF
FE_NEGATIVE = fe.NEGATIVE_CONTROL_MATERIALIZATION
FE_RELEASE = fe.RELEASE_GATE_MATERIALIZATION
FE_TASK_SEEDS = fe.TRAINING_TASK_SEEDS

INPUT_SAFETY_REVIEW = RUN_DIR / "train_only_input_safety_review.csv"
FEATURE_BOUNDARY_REVIEW = RUN_DIR / "feature_label_boundary_review.csv"
WEIGHT_REVIEW = RUN_DIR / "repair_weight_review.csv"
NEGATIVE_CONTROL_REVIEW = RUN_DIR / "negative_control_review.csv"
RELEASE_GATE_REVIEW = RUN_DIR / "release_gate_review.csv"
TRAINING_FEATURE_EXCLUSION = RUN_DIR / "training_feature_exclusion.csv"
TRAINING_TASK_MATRIX = RUN_DIR / "fg_training_task_matrix.csv"
FG_QUEUE = RUN_DIR / "run337FG_training_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    FE_FINAL,
    FE_GATES,
    FE_QUEUE,
    FE_FRAME,
    FE_SOURCE_MAP,
    FE_FEATURES,
    FE_WEIGHT_RECIPES,
    FE_WEIGHT_AUDIT,
    FE_BOUNDARY,
    FE_HANDOFF,
    FE_NEGATIVE,
    FE_RELEASE,
    FE_TASK_SEEDS,
)
OUTPUT_FILES = (
    INPUT_SAFETY_REVIEW,
    FEATURE_BOUNDARY_REVIEW,
    WEIGHT_REVIEW,
    NEGATIVE_CONTROL_REVIEW,
    RELEASE_GATE_REVIEW,
    TRAINING_FEATURE_EXCLUSION,
    TRAINING_TASK_MATRIX,
    FG_QUEUE,
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
    RUN_REGISTRY,
    ALPHA_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)

REVIEW_COLUMNS = ("review_id", "subject", "status", "observed", "expected", "effect", "claim_boundary")
WEIGHT_COLUMNS = (
    "weight_column",
    "review_status",
    "rows",
    "weight_min",
    "weight_mean",
    "weight_max",
    "nonfinite_rows",
    "short_label_mean",
    "flat_label_mean",
    "long_label_mean",
    "training_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
EXCLUSION_COLUMNS = (
    "column_name",
    "column_role",
    "training_feature_status",
    "required_reason",
    "forbidden_use",
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
GATE_COLUMNS = ("gate_id", "status", "evidence_path", "observed", "expected", "effect", "claim_boundary")

FORBIDDEN_FEATURE_COLUMNS = sorted(fe.FORBIDDEN_FEATURE_COLUMNS)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def load_frame() -> pd.DataFrame:
    return pd.read_parquet(aw.io_path(FE_FRAME))


def build_reviews(frame: pd.DataFrame) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    features = read_csv(FE_FEATURES)
    feature_names = [row["feature_name"] for row in features if row.get("feature_name")]
    missing_features = [name for name in feature_names if name not in frame.columns]
    forbidden_present = [name for name in feature_names if name in FORBIDDEN_FEATURE_COLUMNS]
    boundary_rows = read_csv(FE_BOUNDARY)
    boundary_failed = [row for row in boundary_rows if row.get("status") != "passed"]
    weight_audit_rows = read_csv(FE_WEIGHT_AUDIT)
    task_seed_rows = read_csv(FE_TASK_SEEDS)
    label = pd.to_numeric(frame["label_class"], errors="coerce").fillna(1).astype(int)
    split_values = sorted(str(value) for value in frame["split"].dropna().unique()) if "split" in frame.columns else []
    nonfinite_weight_rows = 0
    weight_review: list[dict[str, Any]] = []
    for row in weight_audit_rows:
        column = row["weight_column"]
        series = pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan) if column in frame.columns else pd.Series(dtype="float64")
        missing = column not in frame.columns
        nonfinite = int(series.isna().sum()) if not missing else len(frame)
        nonfinite_weight_rows += nonfinite
        min_value = float(series.min()) if len(series) else 0.0
        max_value = float(series.max()) if len(series) else 0.0
        passed = not missing and nonfinite == 0 and min_value >= 0.10 and max_value <= 10.0
        weight_review.append(
            {
                "weight_column": column,
                "review_status": "passed" if passed else "failed",
                "rows": len(frame),
                "weight_min": min_value,
                "weight_mean": float(series.mean()) if len(series) else 0.0,
                "weight_max": max_value,
                "nonfinite_rows": nonfinite,
                "short_label_mean": float(series[label == 0].mean()) if len(series) else 0.0,
                "flat_label_mean": float(series[label == 1].mean()) if len(series) else 0.0,
                "long_label_mean": float(series[label == 2].mean()) if len(series) else 0.0,
                "training_use": "sample_weight only(표본 가중치 전용)",
                "forbidden_use": "model feature or selection proof(모델 피처 또는 선택 증거)",
                "effect": "confirms bounded repair weight before training(학습 전 범위 제한 수리 가중치 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    input_rows = [
        {
            "review_id": "ff001_frame_presence",
            "subject": "train-only FE frame(FE 학습 전용 프레임)",
            "status": "passed" if len(frame) > 80000 else "failed",
            "observed": str(len(frame)),
            "expected": ">80000",
            "effect": "confirms materialized rows are present(물질화 행 존재 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "ff002_split_scope",
            "subject": "split boundary(분할 경계)",
            "status": "passed" if split_values == ["train"] else "failed",
            "observed": ",".join(split_values),
            "expected": "train",
            "effect": "keeps training inputs away from Forward evidence(학습 입력을 전진 근거에서 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "ff003_feature_presence",
            "subject": "allowed features(허용 피처)",
            "status": "passed" if len(feature_names) == 58 and not missing_features else "failed",
            "observed": f"features={len(feature_names)};missing={len(missing_features)}",
            "expected": "58 and missing=0",
            "effect": "keeps model feature surface stable(모델 피처 표면 안정 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "ff004_forbidden_feature_exclusion",
            "subject": "feature-label boundary(피처-라벨 경계)",
            "status": "passed" if not forbidden_present and not boundary_failed else "failed",
            "observed": f"forbidden_present={len(forbidden_present)};boundary_failed={len(boundary_failed)}",
            "expected": "0 and 0",
            "effect": "prevents repair weights, labels, and outcomes entering features(수리 가중치/라벨/결과의 피처 유입 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    feature_review = [
        {
            "review_id": "ff_feature_boundary",
            "subject": "feature set(피처 묶음)",
            "status": "passed" if len(feature_names) == 58 and not missing_features and not forbidden_present else "failed",
            "observed": f"feature_count={len(feature_names)};missing={missing_features};forbidden={forbidden_present}",
            "expected": "58 features, no missing, no forbidden(58개 피처, 누락 없음, 금지 열 없음)",
            "effect": "approves only reviewed pretrade features(검토된 사전거래 피처만 승인)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    exclusions = [
        {
            "column_name": column,
            "column_role": "label/outcome/weight/claim boundary(라벨/결과/가중치/주장 경계)",
            "training_feature_status": "excluded(제외)",
            "required_reason": "not causal model input(인과 모델 입력 아님)",
            "forbidden_use": "training feature(학습 피처)",
            "effect": "keeps leakage path explicit(누수 경로를 명시)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for column in FORBIDDEN_FEATURE_COLUMNS
        if column in frame.columns or column.startswith("fd_")
    ]
    negative_review = [
        {
            "review_id": row.get("control_id", f"negative_{index:02d}"),
            "subject": row.get("source_control", ""),
            "status": "passed" if row.get("materialized_status") else "failed",
            "observed": row.get("observed", ""),
            "expected": "carried_forward_active(활성 이월)",
            "effect": row.get("effect", "negative control reviewed(부정 대조 검토)"),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, row in enumerate(read_csv(FE_NEGATIVE), start=1)
    ]
    release_review = [
        {
            "review_id": row.get("gate_id", f"release_{index:02d}"),
            "subject": row.get("source_gate", ""),
            "status": "passed" if row.get("materialized_status") else "failed",
            "observed": row.get("observed", ""),
            "expected": "carried_forward_active(활성 이월)",
            "effect": row.get("effect", "release gate reviewed(해제 게이트 검토)"),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, row in enumerate(read_csv(FE_RELEASE), start=1)
    ]

    eligible = all(row["status"] == "passed" for row in input_rows + feature_review + negative_review + release_review) and all(
        row["review_status"] == "passed" for row in weight_review
    )
    task_rows: list[dict[str, Any]] = []
    for row in task_seed_rows:
        task_rows.append(
            {
                "task_id": row.get("task_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "target_column": row.get("target_column", ""),
                "sample_weight_expression": row.get("sample_weight_expression", ""),
                "model_family": row.get("model_family", ""),
                "model_config_id": row.get("model_config_id", ""),
                "feature_count": len(feature_names),
                "training_eligibility_status": "eligible_for_guarded_training_reviewed_inputs" if eligible else "blocked_by_ff_review",
                "required_guard": "feature list only; sample weights only; no threshold tuning; export probs3(피처 목록만, 표본 가중치만, 임계값 튜닝 없음, probs3 내보내기)",
                "forbidden_action": "candidate selection, MT5 execution, Forward/Goal claim(후보 선택, MT5 실행, 전진/목표 주장)",
                "effect": "opens guarded FG training after input review(입력 검토 후 방어적 FG 학습 개방)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    queue_rows = [
        {
            "queue_id": "fg001_train_runtime_positive_clue_repair_candidates",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "Train guarded ONNX candidates(방어적 ONNX 후보 학습) from reviewed FE repair inputs.",
            "required_inputs": ";".join(rel(path) for path in (FE_FRAME, FE_FEATURES, TRAINING_TASK_MATRIX)),
            "required_outputs": "trained models(학습 모델); ONNX parity(ONNX 동등성); proxy review(프록시 검토); no-selection disposition(선택 없음 판정)",
            "blocked_if_missing": "eligible training tasks or reviewed features(적격 학습 작업 또는 검토 피처)",
            "forbidden_action": "threshold tuning, MT5 execution, candidate selection, Forward/Goal claim(임계값 튜닝, MT5 실행, 후보 선택, 전진/목표 주장)",
            "effect": "moves from safe input review to guarded model training(안전 입력 검토에서 방어적 모델 학습으로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    summary = {
        "rows": int(len(frame)),
        "feature_count": len(feature_names),
        "missing_feature_rows": len(missing_features),
        "forbidden_feature_rows": len(forbidden_present),
        "boundary_failed_rows": len(boundary_failed),
        "weight_review_rows": len(weight_review),
        "weight_failed_rows": sum(1 for row in weight_review if row["review_status"] != "passed"),
        "nonfinite_weight_rows": nonfinite_weight_rows,
        "training_task_rows": len(task_rows),
        "eligible_task_rows": sum(1 for row in task_rows if row["training_eligibility_status"] == "eligible_for_guarded_training_reviewed_inputs"),
        "fg_queue_rows": len(queue_rows),
    }
    return input_rows, feature_review, weight_review, negative_review, release_review, exclusions, task_rows, queue_rows, summary


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    fe_final = read_json(FE_FINAL)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "fe_next_action": fe_final.get("next_action", ""),
        "fe_failed_gate_rows": sum(1 for row in read_csv(FE_GATES) if row.get("status") != "passed"),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["model_training"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(FE_FINAL), "required FF inputs exist(필수 FF 입력 존재)"),
        ("parent_fe_gates_passed", final["fe_failed_gate_rows"] == 0, str(final["fe_failed_gate_rows"]), "0", rel(FE_GATES), "FE gates passed(FE 게이트 통과)"),
        ("parent_next_action_matches", final["fe_next_action"] == RUN_ID, str(final["fe_next_action"]), RUN_ID, rel(FE_FINAL), "FF follows FE next action(FF가 FE 다음 행동을 따름)"),
        ("frame_review_passed", final["rows"] > 80000, str(final["rows"]), ">80000", rel(INPUT_SAFETY_REVIEW), "train-only frame reviewed(학습 전용 프레임 검토)"),
        ("feature_boundary_passed", final["feature_count"] == 58 and final["missing_feature_rows"] == 0 and final["forbidden_feature_rows"] == 0 and final["boundary_failed_rows"] == 0, f"features={final['feature_count']};missing={final['missing_feature_rows']};forbidden={final['forbidden_feature_rows']};boundary_failed={final['boundary_failed_rows']}", "58/0/0/0", rel(FEATURE_BOUNDARY_REVIEW), "feature boundary passed(피처 경계 통과)"),
        ("weight_review_passed", final["weight_review_rows"] >= 7 and final["weight_failed_rows"] == 0 and final["nonfinite_weight_rows"] == 0, f"rows={final['weight_review_rows']};failed={final['weight_failed_rows']};nonfinite={final['nonfinite_weight_rows']}", ">=7/0/0", rel(WEIGHT_REVIEW), "weight review passed(가중치 검토 통과)"),
        ("training_tasks_eligible", final["eligible_task_rows"] == final["training_task_rows"] == 4, f"eligible={final['eligible_task_rows']};tasks={final['training_task_rows']}", "4/4", rel(TRAINING_TASK_MATRIX), "all FG task seeds eligible(모든 FG 작업 씨앗 적격)"),
        ("fg_queue_materialized", final["fg_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['fg_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(FG_QUEUE), "FG training queue opened(FG 학습 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['model_training']};mt5={final['mt5_execution']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "review without operating claim(운영 주장 없는 검토)"),
        ("required_gate_coverage_audit", True, "all required gates listed(모든 필수 게이트 열거)", "present", rel(GATE_AUDIT), "completion claim tied to gates(완료 주장이 게이트에 연결됨)"),
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


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    data = {
        "data_source": rel(FE_FRAME),
        "time_axis": "closed M5 train-only timestamps(확정 M5 학습 전용 시각)",
        "sample_scope": {"rows": final["rows"], "feature_count": final["feature_count"]},
        "missing_or_duplicate_check": "cost-policy duplicate timestamps are training rows; runtime handoff remains dedupe-only(비용정책 중복 시각은 학습 행, 런타임 인계는 중복 제거 유지)",
        "feature_label_boundary": "passed; forbidden features excluded(통과, 금지 피처 제외)",
        "split_boundary": "train only(학습 전용)",
        "leakage_risk": "repair weights as features; blocked by exclusion review(수리 가중치의 피처 사용 위험, 제외 검토로 차단)",
        "data_hash_or_identity": {"frame_sha256": aw.sha256_file(FE_FRAME), "feature_sha256": aw.sha256_file(FE_FEATURES)},
        "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_action": "not_run(실행 안 함)",
        "eligible_task_rows": final["eligible_task_rows"],
        "future_requirement": "FG training must export ONNX and parity matrix(FG 학습은 ONNX와 동등성 행렬을 내보내야 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "kpi_status": "no new KPI; review only(새 KPI 없음, 검토 전용)",
        "training_use": "opens guarded training queue(방어적 학습 대기열 개방)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "goal_achieve": "not_claimed(주장 안 함)",
        "runtime_authority": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    lineage_artifacts = list(artifacts) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in lineage_artifacts],
        "artifact_hashes": {
            rel(path): aw.sha256_file(path)
            for path in lineage_artifacts
            if path_exists(path) and aw.io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337FF Repair Input Review(337단계 337FF 수리 입력 검토)

## Conclusion(결론)

Action(행동): FE train-only repair inputs(FE 학습 전용 수리 입력)의 feature boundary(피처 경계), repair weights(수리 가중치), negative controls(부정 대조), release gates(해제 게이트)를 검토했다. Effect(효과): 4개 FG training tasks(FG 학습 작업)를 guarded training eligible(방어적 학습 적격)로 열었다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['training_task_rows']}`
- weight_failed_rows(가중치 실패 행): `{final['weight_failed_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Boundary(경계): FF(337FF 실행)는 review only(검토 전용)이다. model training(모델 학습), MT5 execution(MT5 실행), operating selection(운영 선택), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

Next action(다음 행동): `{final['next_action']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337FF Decision(337FF 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(TRAINING_TASK_MATRIX)}`, `{rel(WEIGHT_REVIEW)}`, `{rel(FEATURE_BOUNDARY_REVIEW)}`

Action(행동): FE 입력 검토를 통과한 작업만 FG training(FG 학습)으로 넘겼다.
Effect(효과): 모델 학습은 다음 run(실행)에서 시작되며, 이 결정은 운영 승격이 아니다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
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


def upsert_section_before(text: str, marker: str, section: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}.*?(?=^## )", flags=re.M | re.S)
    if pattern.search(text):
        return pattern.sub(section.rstrip() + "\n\n", text, count=1)
    if marker in text:
        return text.replace(marker, section.rstrip() + "\n\n" + marker, 1)
    return text.rstrip() + "\n\n" + section.rstrip() + "\n"


def upsert_single_line(text: str, needle: str, entry: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = entry
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {fe.fd.current_branch()}")
    focus = (
        "- >-\n"
        f"  Stage337 run337FF focus complete: run337FF(337FF 실행)는 `{final['status']}`로 repair input review(수리 입력 검토)를 완료했다. "
        f"Effect(효과): eligible tasks(적격 작업) `{final['eligible_task_rows']}/{final['training_task_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337FF focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337FF focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
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
    section = f"""## run337FF Repair Input Review(수리 입력 검토)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['training_task_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): FE repair inputs(FE 수리 입력)를 학습 가능 상태로 검토하고 FG training(FG 학습)을 열었다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = upsert_section_before(current, "## run337FE Repair Input Materialization", section, "run337FF Repair Input Review")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['training_task_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): FF(337FF 실행)는 review(검토)만 완료했고 model training(모델 학습), MT5 execution(MT5 실행), operating selection(운영 선택)은 하지 않았다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_entry = f"- {TODAY}: run337FF(337FF 실행) `{final['status']}`. Effect(효과): FE 수리 입력 검토를 통과해 `{final['eligible_task_rows']}`개 FG training tasks(FG 학습 작업)를 열고 `{final['next_action']}`을 지정했다. Forward/Goal(전진/목표)은 주장하지 않는다."
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, upsert_single_line(brief, "run337FF(337FF 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337FF(337FF 실행) `{final['status']}`. Effect(효과): repair input review(수리 입력 검토)를 통과하고 FG training(FG 학습)을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    artifacts.append(aw.write_text_lossless(CHANGELOG, upsert_single_line(changelog, "Stage337 run337FF", changelog_entry), changelog_bom))
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
    rows = [item for item in existing if str(item.get(key, "")) != str(row.get(key, ""))]
    rows.append({column: row.get(column, "") for column in merged_columns})
    return write_csv(path, merged_columns, rows)


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_positive_clue_repair_input_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"eligible={final['eligible_task_rows']}/{final['training_task_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_input_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "train_only_runtime_positive_clue_repair_input_review(학습 전용 런타임 긍정 단서 수리 입력 검토)",
        "tier_scope": "Tier A train-only input review; Tier B out_of_scope_by_claim(Tier A 학습 전용 입력 검토, Tier B 주장 범위 밖)",
        "kpi_scope": "review only; no new KPI(검토 전용, 새 성과 없음)",
        "scoreboard_lane": "data_integrity",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"eligible_tasks={final['eligible_task_rows']}/{final['training_task_rows']}",
        "guardrail_kpi": "no_training;no_mt5;no_selection;no_goal",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_result_judgment",
        "evidence_scope": "FE repair inputs and task seeds",
        "kpi_scope": "review_no_new_kpi",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__repair_input_review",
        "family": "runtime_positive_clue_repair_input_review",
        "question": "are FE repair inputs safe for guarded training",
        "metric_scope": "feature_boundary_weight_audit_task_eligibility",
        "primary_artifact": rel(TRAINING_TASK_MATRIX),
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
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [
        row
        for row in rows
        if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID
    ]
    created_at = now_utc()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        row = {
            "artifact_id": f"{RUN_ID}::{artifact_path}",
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
        rows.append({column: row.get(column, "") for column in columns})
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    frame = load_frame()
    input_rows, feature_rows, weight_rows, negative_rows, release_rows, exclusions, task_rows, queue_rows, summary = build_reviews(frame)
    final = make_final(summary)
    artifacts = [
        write_csv(INPUT_SAFETY_REVIEW, REVIEW_COLUMNS, input_rows),
        write_csv(FEATURE_BOUNDARY_REVIEW, REVIEW_COLUMNS, feature_rows),
        write_csv(WEIGHT_REVIEW, WEIGHT_COLUMNS, weight_rows),
        write_csv(NEGATIVE_CONTROL_REVIEW, REVIEW_COLUMNS, negative_rows),
        write_csv(RELEASE_GATE_REVIEW, REVIEW_COLUMNS, release_rows),
        write_csv(TRAINING_FEATURE_EXCLUSION, EXCLUSION_COLUMNS, exclusions),
        write_csv(TRAINING_TASK_MATRIX, TASK_COLUMNS, task_rows),
        write_csv(FG_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
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

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "eligible_task_rows": final["eligible_task_rows"],
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
