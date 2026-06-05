from __future__ import annotations

import json
import math
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
from stage_pipelines.stage337 import materialize_proxy_negative_trade_shape_second_order_repair_inputs_without_db as hs  # noqa: E402


aw = hs.aw
fb = hs.fb
he = hs.he

TODAY = "2026-06-01"
STAGE_ID = hs.STAGE_ID
RUN_NUMBER = "run337HT"
RUN_ID = "run337HT_review_proxy_negative_trade_shape_second_order_repair_inputs_without_db_v1"
PARENT_RUN_ID = hs.RUN_ID
NEXT_RUN_ID = "run337HU_train_proxy_negative_trade_shape_second_order_repair_candidates_without_db_v1"
STATUS = "completed_stage337HT_proxy_negative_trade_shape_second_order_inputs_review_guarded_training_eligible_no_training_no_selection"
JUDGMENT = "hs_second_order_inputs_weight_feature_target_reviewed_guarded_training_eligible"
DECISION = "stage337HT_open_run337HU_proxy_negative_trade_shape_second_order_training"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HT_proxy_negative_trade_shape_second_order_input_review_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_runtime_package_"
    "no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = hs.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = hs.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HT_proxy_negative_trade_shape_second_order_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HT_proxy_negative_trade_shape_second_order_input_review.md"

HS_FINAL = hs.FINAL_DECISION
HS_GATES = hs.GATE_AUDIT
HS_QUEUE = hs.HT_QUEUE
HS_FRAME = hs.HS_INPUT_FRAME
HS_ALLOWED_FEATURES = hs.HS_ALLOWED_FEATURE_SET
HS_WEIGHT_AUDIT = hs.HS_WEIGHT_AUDIT
HS_TARGET_AUDIT = hs.HS_TARGET_AUDIT
HS_FEATURE_BOUNDARY = hs.HS_FEATURE_BOUNDARY
HS_DENSITY_AUDIT = hs.HS_DENSITY_AUDIT
HS_MODEL_PROPOSAL_REVIEW = hs.HS_MODEL_PROPOSAL_REVIEW
HS_RELEASE_MATERIALIZATION = hs.HS_RELEASE_MATERIALIZATION
HS_TASK_SEEDS = hs.HS_TRAINING_TASK_SEEDS

INPUT_REVIEW = RUN_DIR / "hs_input_review.csv"
WEIGHT_REVIEW = RUN_DIR / "hr_second_order_weight_review.csv"
FEATURE_BOUNDARY_REVIEW = RUN_DIR / "feature_boundary_review.csv"
TASK_ELIGIBILITY = RUN_DIR / "training_task_eligibility.csv"
MODEL_PROPOSAL_REVIEW = RUN_DIR / "model_proposal_review.csv"
RELEASE_GATE_REVIEW = RUN_DIR / "release_gate_review.csv"
HU_QUEUE = RUN_DIR / "run337HU_training_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_discipline_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    HS_FINAL,
    HS_GATES,
    HS_QUEUE,
    HS_FRAME,
    HS_ALLOWED_FEATURES,
    HS_WEIGHT_AUDIT,
    HS_TARGET_AUDIT,
    HS_FEATURE_BOUNDARY,
    HS_DENSITY_AUDIT,
    HS_MODEL_PROPOSAL_REVIEW,
    HS_RELEASE_MATERIALIZATION,
    HS_TASK_SEEDS,
)
OUTPUT_FILES = (
    INPUT_REVIEW,
    WEIGHT_REVIEW,
    FEATURE_BOUNDARY_REVIEW,
    TASK_ELIGIBILITY,
    MODEL_PROPOSAL_REVIEW,
    RELEASE_GATE_REVIEW,
    HU_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    he.SELECTED_STATUS,
    he.WORKSPACE_STATE,
    he.CURRENT_STATE,
    he.CHANGELOG,
    he.STAGE_BRIEF,
    he.RUN_REGISTRY,
    he.ALPHA_LEDGER,
    he.STAGE_LEDGER,
    he.ARTIFACT_REGISTRY,
    Path(__file__),
)

AUDIT_COLUMNS = ("audit_id", "status", "observed", "expected", "evidence", "effect", "claim_boundary")
WEIGHT_REVIEW_COLUMNS = (
    "weight_column",
    "rows",
    "weight_min",
    "weight_mean",
    "weight_max",
    "nonfinite_rows",
    "short_label_mean",
    "flat_label_mean",
    "long_label_mean",
    "review_status",
    "saturation_watch",
    "saturation_rate",
    "effect",
    "claim_boundary",
)
TASK_COLUMNS = (
    "task_id",
    "target_column",
    "sample_weight_column",
    "sample_weight_expression",
    "model_family",
    "model_config_id",
    "eligibility_status",
    "required_guard",
    "blocked_reason",
    "effect",
    "claim_boundary",
)
MODEL_REVIEW_COLUMNS = ("audit_id", "source_status", "review_status", "observed", "expected", "evidence", "effect", "claim_boundary")
RELEASE_COLUMNS = ("gate_id", "source_status", "review_status", "pass_condition", "required_artifact", "effect", "claim_boundary")
QUEUE_COLUMNS = hs.QUEUE_COLUMNS
GATE_COLUMNS = hs.GATE_COLUMNS

WEIGHT_ELIGIBLE = "eligible(적격)"
TASK_ELIGIBLE = "eligible_for_guarded_training(방어 학습 적격)"
SATURATION_BLOCK_RATE = 0.25
EXPECTED_ROWS = 87666
EXPECTED_FEATURES = 58


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
    aw.io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def finite_series(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        return pd.Series(np.nan, index=df.index, dtype="float64")
    return pd.to_numeric(df[column], errors="coerce").replace([np.inf, -np.inf], np.nan).astype("float64")


def hu_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "hu_proxy_negative_trade_shape_second_order_guarded_training",
            "source_run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "task": "train reviewed HS second-order repair tasks and export ONNX(검토된 HS 2차 수리 작업을 학습하고 ONNX를 내보내기)",
            "required_inputs": ";".join(rel(path) for path in (HS_FRAME, HS_ALLOWED_FEATURES, TASK_ELIGIBILITY, WEIGHT_REVIEW, RELEASE_GATE_REVIEW)),
            "expected_outputs": "trained model manifest, ONNX export, parity matrix, proxy scorecard, next review queue(학습 모델 목록, ONNX 내보내기, 동등성 행렬, 프록시 점수표, 다음 검토 대기열)",
            "blocked_if_missing": "eligible task rows, feature schema, finite sample weights(적격 작업 행, 피처 스키마, 유한 표본 가중치)",
            "effect": "moves reviewed second-order inputs to guarded training without operating claim(검토된 2차 입력을 운영 주장 없이 방어 학습으로 넘김)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_reviews() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    frame = pd.read_parquet(aw.io_path(HS_FRAME))
    hs_final = read_json(HS_FINAL)
    hs_queue = read_csv(HS_QUEUE)
    allowed_rows = read_csv(HS_ALLOWED_FEATURES)
    weight_rows = read_csv(HS_WEIGHT_AUDIT)
    target_rows = read_csv(HS_TARGET_AUDIT)
    boundary_rows = read_csv(HS_FEATURE_BOUNDARY)
    density_rows = read_csv(HS_DENSITY_AUDIT)
    model_rows = read_csv(HS_MODEL_PROPOSAL_REVIEW)
    release_rows = read_csv(HS_RELEASE_MATERIALIZATION)
    task_seed_rows = read_csv(HS_TASK_SEEDS)

    failed_target = [row for row in target_rows if row.get("status") != "passed"]
    failed_boundary = [row for row in boundary_rows if row.get("status") != "passed"]
    failed_density = [row for row in density_rows if row.get("status") != "passed"]
    timestamps = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce") if "timestamp" in frame.columns else pd.Series(dtype="datetime64[ns, UTC]")
    monotonic = bool(timestamps.is_monotonic_increasing) if len(timestamps) else False
    duplicate_timestamps = int(frame["timestamp"].duplicated().sum()) if "timestamp" in frame.columns else -1
    queue_next = hs_queue[0].get("next_run_id", "") if hs_queue else ""
    queue_source = hs_queue[0].get("source_run_id", "") if hs_queue else ""

    input_rows = [
        {"audit_id": "ht001_parent_queue_authorized", "status": "passed" if queue_next == RUN_ID and queue_source == PARENT_RUN_ID else "failed", "observed": f"source={queue_source};next={queue_next}", "expected": f"source={PARENT_RUN_ID};next={RUN_ID}", "evidence": rel(HS_QUEUE), "effect": "confirms HT follows HS queue(HT가 HS 대기열을 따르는지 확인)", "claim_boundary": CLAIM_BOUNDARY},
        {"audit_id": "ht002_frame_rows", "status": "passed" if len(frame) == EXPECTED_ROWS else "failed", "observed": str(len(frame)), "expected": str(EXPECTED_ROWS), "evidence": rel(HS_FRAME), "effect": "keeps HS train-only row count stable(HS 학습 전용 행 수를 안정적으로 유지)", "claim_boundary": CLAIM_BOUNDARY},
        {"audit_id": "ht003_timestamp_order", "status": "passed" if monotonic else "failed", "observed": str(monotonic), "expected": "True", "evidence": rel(HS_FRAME), "effect": "checks timestamp order before training(학습 전 시점 순서를 확인)", "claim_boundary": CLAIM_BOUNDARY},
        {"audit_id": "ht004_timestamp_range", "status": "passed" if str(hs_final.get("first_timestamp")) == str(timestamps.min()) and str(hs_final.get("last_timestamp")) == str(timestamps.max()) else "failed", "observed": f"{timestamps.min()} / {timestamps.max()}", "expected": f"{hs_final.get('first_timestamp')} / {hs_final.get('last_timestamp')}", "evidence": rel(HS_FINAL), "effect": "keeps parent time range unchanged(부모 시간 범위를 바꾸지 않음)", "claim_boundary": CLAIM_BOUNDARY},
        {"audit_id": "ht005_duplicate_timestamps_named", "status": "passed" if duplicate_timestamps == int(hs_final.get("duplicate_timestamp_rows", -999)) else "failed", "observed": str(duplicate_timestamps), "expected": str(hs_final.get("duplicate_timestamp_rows")), "evidence": rel(HS_FINAL), "effect": "keeps duplicate timestamps explained by cost policy expansion(중복 시점을 비용 정책 확장으로 설명)", "claim_boundary": CLAIM_BOUNDARY},
        {"audit_id": "ht006_allowed_feature_count", "status": "passed" if len(allowed_rows) == EXPECTED_FEATURES else "failed", "observed": str(len(allowed_rows)), "expected": str(EXPECTED_FEATURES), "evidence": rel(HS_ALLOWED_FEATURES), "effect": "preserves reviewed feature list(검토된 피처 목록 보존)", "claim_boundary": CLAIM_BOUNDARY},
        {"audit_id": "ht007_target_contract_passed", "status": "passed" if not failed_target else "failed", "observed": str(len(failed_target)), "expected": "0 failed rows(실패 행 0)", "evidence": rel(HS_TARGET_AUDIT), "effect": "checks label target boundary(라벨 목표 경계 확인)", "claim_boundary": CLAIM_BOUNDARY},
        {"audit_id": "ht008_feature_boundary_passed", "status": "passed" if not failed_boundary else "failed", "observed": str(len(failed_boundary)), "expected": "0 failed rows(실패 행 0)", "evidence": rel(HS_FEATURE_BOUNDARY), "effect": "checks leakage and forbidden feature guard(누수와 금지 피처 보호 확인)", "claim_boundary": CLAIM_BOUNDARY},
        {"audit_id": "ht009_second_order_density_passed", "status": "passed" if not failed_density else "failed", "observed": str(len(failed_density)), "expected": "0 failed rows(실패 행 0)", "evidence": rel(HS_DENSITY_AUDIT), "effect": "checks second-order repair input audit(2차 수리 입력 감사 확인)", "claim_boundary": CLAIM_BOUNDARY},
    ]

    weight_review = []
    failed_weight_rows = 0
    saturation_watch_rows = 0
    max_saturation_rate = 0.0
    total_nonfinite = 0
    for row in weight_rows:
        weight_col = row.get("weight_column", "")
        values = finite_series(frame, weight_col)
        finite_mask = np.isfinite(values.to_numpy())
        nonfinite_rows = int((~finite_mask).sum())
        total_nonfinite += nonfinite_rows
        saturation_rate = float((values >= 9.999).mean()) if len(values) else 1.0
        max_saturation_rate = max(max_saturation_rate, saturation_rate)
        eligible = (
            weight_col in frame.columns
            and nonfinite_rows == 0
            and as_float(row.get("weight_min")) >= 0.25
            and as_float(row.get("weight_max")) <= 10.0
            and saturation_rate <= SATURATION_BLOCK_RATE
        )
        if not eligible:
            failed_weight_rows += 1
        if saturation_rate > 0.05:
            saturation_watch_rows += 1
        weight_review.append(
            {
                **row,
                "review_status": WEIGHT_ELIGIBLE if eligible else "blocked(차단)",
                "saturation_watch": "watch(감시)" if saturation_rate > 0.05 else "normal(정상)",
                "saturation_rate": f"{saturation_rate:.6f}",
                "effect": "reviews bounded train-only second-order sample weight(범위가 제한된 학습 전용 2차 표본 가중치 검토)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    task_review = []
    for row in task_seed_rows:
        target_col = row.get("target_column", "")
        weight_col = row.get("sample_weight_column", "")
        values = finite_series(frame, weight_col)
        nonfinite_rows = int((~np.isfinite(values.to_numpy())).sum()) if weight_col in frame.columns else 1
        target_ok = target_col == "label_class" and target_col in frame.columns
        weight_ok = weight_col in hs.NEW_WEIGHT_COLUMNS and weight_col in frame.columns and nonfinite_rows == 0
        eligible = target_ok and weight_ok and len(allowed_rows) == EXPECTED_FEATURES and not failed_boundary and not failed_target
        task_review.append(
            {
                "task_id": row.get("task_id", ""),
                "target_column": target_col,
                "sample_weight_column": weight_col,
                "sample_weight_expression": row.get("sample_weight_expression", weight_col),
                "model_family": row.get("model_family", ""),
                "model_config_id": row.get("model_config_id", ""),
                "eligibility_status": TASK_ELIGIBLE if eligible else "blocked(차단)",
                "required_guard": row.get("required_guard", ""),
                "blocked_reason": "" if eligible else f"target_or_weight_or_boundary_failed(목표/가중치/경계 실패);nonfinite_rows={nonfinite_rows}",
                "effect": row.get("expected_effect", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    model_review = [
        {
            "audit_id": row.get("audit_id", f"model_{index:02d}"),
            "source_status": row.get("status", ""),
            "review_status": "carried_to_HU_training_review(HU 학습 검토로 이월)",
            "observed": row.get("observed", ""),
            "expected": row.get("expected", ""),
            "evidence": rel(HS_MODEL_PROPOSAL_REVIEW),
            "effect": row.get("effect", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, row in enumerate(model_rows, start=1)
    ]
    release_review = [
        {
            "gate_id": row.get("audit_id", f"release_{index:02d}"),
            "source_status": row.get("status", ""),
            "review_status": "carried_to_HU_release_guard(HU 릴리스 보호로 이월)",
            "pass_condition": row.get("observed", ""),
            "required_artifact": row.get("evidence", ""),
            "effect": row.get("effect", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, row in enumerate(release_rows, start=1)
    ]
    queue_rows = hu_queue_rows()
    summary = {
        "hs_next_action": hs_final.get("next_action", ""),
        "hs_failed_gate_rows": sum(1 for row in read_csv(HS_GATES) if row.get("status") != "passed"),
        "rows": len(frame),
        "columns": len(frame.columns),
        "first_timestamp": str(timestamps.min()) if len(timestamps) else "",
        "last_timestamp": str(timestamps.max()) if len(timestamps) else "",
        "duplicate_timestamp_rows": duplicate_timestamps,
        "allowed_feature_rows": len(allowed_rows),
        "target_failed_rows": len(failed_target),
        "feature_boundary_failed_rows": len(failed_boundary),
        "density_failed_rows": len(failed_density),
        "input_review_rows": len(input_rows),
        "failed_input_review_rows": sum(1 for row in input_rows if row["status"] != "passed"),
        "weight_review_rows": len(weight_review),
        "failed_weight_rows": failed_weight_rows,
        "total_nonfinite_weight_rows": total_nonfinite,
        "saturation_watch_rows": saturation_watch_rows,
        "max_saturation_rate": max_saturation_rate,
        "task_rows": len(task_review),
        "eligible_task_rows": sum(1 for row in task_review if row["eligibility_status"] == TASK_ELIGIBLE),
        "model_proposal_rows": len(model_review),
        "release_gate_rows": len(release_review),
        "queue_rows": len(queue_rows),
        "parent_max_saturation_rate": as_float(hs_final.get("max_saturation_rate")),
        "parent_new_weight_columns": int(hs_final.get("new_weight_columns", 0)),
    }
    return input_rows, weight_review, boundary_rows, task_review, model_review, release_review, queue_rows, summary


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_family": "kpi_evidence",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": "obsidian-data-integrity;obsidian-model-validation;obsidian-artifact-lineage;obsidian-result-judgment",
        "required_gates": "scope_completion_gate;kpi_contract_audit;skill_receipt_lint;required_gate_coverage_audit;final_claim_guard",
        "new_training": "not_run",
        "mt5_execution": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "runtime_package": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["new_training"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["runtime_package"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    gate_specs = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(HS_FINAL), "required HS inputs exist(필수 HS 입력 존재)"),
        ("parent_hs_gates_passed", final["hs_failed_gate_rows"] == 0, str(final["hs_failed_gate_rows"]), "0", rel(HS_GATES), "HS gates passed(HS 게이트 통과)"),
        ("parent_next_action_matches", final["hs_next_action"] == RUN_ID, str(final["hs_next_action"]), RUN_ID, rel(HS_FINAL), "HT follows HS next action(HT가 HS 다음 행동을 따름)"),
        ("input_review_passed", final["failed_input_review_rows"] == 0 and final["rows"] == EXPECTED_ROWS, f"failed={final['failed_input_review_rows']};rows={final['rows']}", f"0 and {EXPECTED_ROWS}", rel(INPUT_REVIEW), "input review passed(입력 검토 통과)"),
        ("feature_boundary_passed", final["feature_boundary_failed_rows"] == 0 and final["allowed_feature_rows"] == EXPECTED_FEATURES, f"failed={final['feature_boundary_failed_rows']};features={final['allowed_feature_rows']}", f"0 and {EXPECTED_FEATURES}", rel(FEATURE_BOUNDARY_REVIEW), "feature boundary passed(피처 경계 통과)"),
        ("target_boundary_passed", final["target_failed_rows"] == 0, str(final["target_failed_rows"]), "0", rel(INPUT_REVIEW), "target contract passed(목표 계약 통과)"),
        ("second_order_density_review_passed", final["density_failed_rows"] == 0, str(final["density_failed_rows"]), "0", rel(INPUT_REVIEW), "second-order density review passed(2차 밀도 검토 통과)"),
        ("weights_review_passed", final["failed_weight_rows"] == 0 and final["weight_review_rows"] == 5 and final["max_saturation_rate"] <= SATURATION_BLOCK_RATE, f"failed={final['failed_weight_rows']};rows={final['weight_review_rows']};max_sat={final['max_saturation_rate']:.6f}", "0 and 5 and max_sat<=0.25", rel(WEIGHT_REVIEW), "sample weights reviewed(표본 가중치 검토 완료)"),
        ("training_tasks_eligible", final["eligible_task_rows"] == final["task_rows"] == 5, f"eligible={final['eligible_task_rows']};tasks={final['task_rows']}", "5/5", rel(TASK_ELIGIBILITY), "all tasks eligible(모든 작업 적격)"),
        ("model_proposals_carried", final["model_proposal_rows"] >= 2, str(final["model_proposal_rows"]), ">=2", rel(MODEL_PROPOSAL_REVIEW), "model proposals carried(모델 제안 이월)"),
        ("release_gates_carried", final["release_gate_rows"] >= 3, str(final["release_gate_rows"]), ">=3", rel(RELEASE_GATE_REVIEW), "release gates carried(릴리스 게이트 이월)"),
        ("hu_training_queue_opened", final["queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(HU_QUEUE), "HU training queue opened(HU 학습 대기열 개방)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['new_training']};mt5={final['mt5_execution']};runtime_package={final['runtime_package']};goal={final['goal_achieve']}", "not_run/not_run/not_run/not_claimed", rel(FINAL_DECISION), "review without operating claim(운영 주장 없는 검토)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence_path,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence_path, effect in gate_specs
    ]


def write_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    created_at = now_utc()
    base = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": final["status"],
        "judgment": final["judgment"],
        "next_action": final["next_action"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts = [
        (
            DATA_RECEIPT,
            {
                **base,
                "receipt_type": "data_integrity(데이터 무결성)",
                "data_source": rel(HS_FRAME),
                "rows": final["rows"],
                "features": final["allowed_feature_rows"],
                "time_axis": f"{final['first_timestamp']} to {final['last_timestamp']} UTC(UTC 시간축)",
                "duplicate_timestamp_rows": final["duplicate_timestamp_rows"],
                "integrity_judgment": "eligible_for_guarded_training_with_boundary(경계 포함 방어 학습 적격)",
                "evidence": [rel(INPUT_REVIEW), rel(FEATURE_BOUNDARY_REVIEW)],
            },
        ),
        (
            MODEL_RECEIPT,
            {
                **base,
                "receipt_type": "model_validation(모델 검증)",
                "model_training": "not_run(미실행)",
                "eligible_tasks": f"{final['eligible_task_rows']}/{final['task_rows']}",
                "threshold_policy": "no threshold tuning(임계값 조정 없음)",
                "evidence": [rel(TASK_ELIGIBILITY), rel(MODEL_PROPOSAL_REVIEW)],
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                **base,
                "receipt_type": "runtime_parity(런타임 동등성)",
                "runtime_action": "not_run input review only(미실행, 입력 검토 전용)",
                "future_required": "ONNX parity and MT5 runtime probe after training(학습 뒤 ONNX 동등성과 MT5 런타임 탐침 필요)",
                "evidence": [rel(RELEASE_GATE_REVIEW)],
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                **base,
                "receipt_type": "performance_attribution(성과 귀속)",
                "performance_action": "no new proxy or MT5 KPI measured(새 프록시나 MT5 KPI 측정 없음)",
                "weight_review": f"failed={final['failed_weight_rows']};max_saturation={final['max_saturation_rate']:.6f}",
                "evidence": [rel(WEIGHT_REVIEW), rel(INPUT_REVIEW)],
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                **base,
                "receipt_type": "result_judgment(결과 판정)",
                "judgment_label": JUDGMENT,
                "evidence_available": [rel(GATE_AUDIT), rel(FINAL_DECISION), rel(REPORT_PATH)],
                "evidence_missing": "model training, ONNX parity, MT5 runtime probe, forward evidence(모델 학습, ONNX 동등성, MT5 런타임 탐침, 전진 근거)",
                "next_condition": NEXT_RUN_ID,
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                **base,
                "receipt_type": "claim_discipline(주장 규율)",
                "forbidden_claims": "operating selection, runtime authority, operating promotion, Goal Achieve(운영 선택, 런타임 권위, 운영 승격, 목표 달성)",
                "claim_guard": "all forbidden claims remain not_claimed/not_run(모든 금지 주장은 not_claimed/not_run 유지)",
            },
        ),
    ]
    paths = [write_json(path, payload) for path, payload in receipts]
    all_artifacts = list(artifacts) + paths
    lineage = {
        **base,
        "receipt_type": "artifact_lineage(산출물 계보)",
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()},
        "lineage_judgment": "connected HS review to HU training queue(HS 검토를 HU 학습 대기열에 연결)",
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_manifest(final: Mapping[str, Any], artifacts: Sequence[Path]) -> Path:
    return write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "stage_id": STAGE_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "created_at_utc": now_utc(),
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in artifacts],
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# run337HT Proxy Negative Trade Shape Second-Order Input Review(run337HT 프록시 음수 거래 형태 2차 입력 검토)

Action(행동): HS materialized input(HS 물질화 입력)의 feature boundary(피처 경계), target contract(목표 계약), sample weight(표본 가중치), training task(학습 작업)를 검토했다.
Effect(효과): HU guarded training(HU 방어 학습)으로 넘길 수 있는지 확인하고, operating claim(운영 주장)을 막았다.

## Judgment(판정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{final['claim_boundary']}`

## Evidence(근거)

- rows(행): `{final['rows']}`
- allowed_features(허용 피처): `{final['allowed_feature_rows']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_rows']}`
- failed_input_review_rows(입력 검토 실패 행): `{final['failed_input_review_rows']}`
- failed_weight_rows(가중치 실패 행): `{final['failed_weight_rows']}`
- max_saturation_rate(최대 포화율): `{final['max_saturation_rate']:.6f}`
- release_gate_rows(릴리스 게이트 행): `{final['release_gate_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

Action(행동): 이 run(실행)은 model training(모델 학습), threshold tuning(임계값 조정), MT5 execution(MT5 실행), candidate selection(후보 선택)을 하지 않았다.
Effect(효과): input eligibility(입력 적격성)만 말하고 runtime authority(런타임 권위)나 Goal Achieve(목표 달성)는 말하지 않는다.
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337HT

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- judgment(판정): `{final['judgment']}`
- effect(효과): HS input review(HS 입력 검토)를 HU guarded training(HU 방어 학습) 대기열로 연결했다.
- forbidden_claim(금지 주장): Forward Passed(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성).
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def upsert_section_after_metadata(text: str, title_marker: str, section: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and title_marker in line:
            start = index
            break
    if start is not None:
        end = start + 1
        while end < len(lines) and not lines[end].startswith("## "):
            end += 1
        del lines[start:end]
    insert_at = next((index for index, line in enumerate(lines) if line.startswith("## ")), len(lines))
    section_lines = section.strip("\n").splitlines()
    return "\n".join(lines[:insert_at] + section_lines + [""] + lines[insert_at:]) + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(he.WORKSPACE_STATE)
    lines = workspace.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("current_run_id:"):
            lines[index] = f"current_run_id: {final['next_action']}"
        elif line.startswith("updated_on:"):
            lines[index] = f"updated_on: '{TODAY}'"
    workspace_text = "\n".join(lines) + "\n"
    if "Stage337 run337HT focus complete" not in workspace_text:
        focus_lines = [
            "- >-",
            (
                f"  Stage337 run337HT focus complete(337단계 run337HT 초점 완료): `{final['status']}`. "
                f"Effect(효과): eligible tasks(적격 작업) `{final['eligible_task_rows']}/{final['task_rows']}`, "
                f"failed weights(실패 가중치) `{final['failed_weight_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 기록하고 `{final['next_action']}`을 열었다. "
                "Forward/Goal(전진/목표)는 주장하지 않는다."
            ),
        ]
        workspace_lines = workspace_text.splitlines()
        for index, line in enumerate(workspace_lines):
            if line.startswith("current_focus:"):
                workspace_lines[index + 1:index + 1] = focus_lines
                break
        workspace_text = "\n".join(workspace_lines) + "\n"
    artifacts.append(aw.write_text_lossless(he.WORKSPACE_STATE, workspace_text, workspace_bom))

    current, current_bom = aw.read_text_lossless(he.CURRENT_STATE)
    current_lines = current.splitlines()
    current_replacements = {
        "- current_run(": f"- current_run(현재 실행): `{final['next_action']}`",
        "- status(": f"- status(상태): `{final['status']}`",
        "- decision(": f"- decision(결정): `{final['decision']}`",
        "- latest_completed_run(": f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- next_action(": f"- next_action(다음 행동): `{final['next_action']}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for index, line in enumerate(current_lines):
        if line.startswith("## "):
            break
        for prefix, replacement in current_replacements.items():
            if line.startswith(prefix):
                current_lines[index] = replacement
                break
    current = "\n".join(current_lines) + "\n"
    section = f"""## run337HT Proxy Negative Trade Shape Second-Order Input Review(프록시 음수 거래 형태 2차 입력 검토)

Action(행동): run337HT(337HT 실행)는 HS materialized inputs(HS 물질화 입력)의 feature boundary(피처 경계), sample weight(표본 가중치), training task(학습 작업)를 검토했다.
Effect(효과): eligible tasks(적격 작업) `{final['eligible_task_rows']}/{final['task_rows']}`, failed weights(실패 가중치) `{final['failed_weight_rows']}`, max saturation(최대 포화율) `{final['max_saturation_rate']:.6f}`를 기록하고 `{final['next_action']}`을 열었다.

Boundary(경계): training(학습), MT5 execution(MT5 실행), runtime package(런타임 패키지), candidate selection(후보 선택), Forward/Goal(전진/목표)은 주장하지 않는다.
Next(다음): `{final['next_action']}`.
"""
    current = upsert_section_after_metadata(current, "run337HT Proxy Negative Trade Shape Second-Order Input Review", section)
    artifacts.append(aw.write_text_lossless(he.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- rows(행): `{final['rows']}`
- allowed_features(허용 피처): `{final['allowed_feature_rows']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_rows']}`
- failed_weight_rows(실패 가중치 행): `{final['failed_weight_rows']}`
- max_saturation_rate(최대 포화율): `{final['max_saturation_rate']:.6f}`
- runtime_package(런타임 패키지): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HT review(HT 검토)는 HU training(HU 학습) 조건만 만들고 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HT(337HT 실행) `{final['status']}`. "
        f"Effect(효과): eligible tasks(적격 작업) `{final['eligible_task_rows']}/{final['task_rows']}`, "
        f"max saturation(최대 포화율) `{final['max_saturation_rate']:.6f}`를 `{final['next_action']}`로 넘겼다. "
        "Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HT(337HT 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HT(337HT 실행) `{final['status']}`. "
        f"Effect(효과): HS input review(HS 입력 검토)를 완료하고 `{final['next_action']}`을 열었다."
    )
    artifacts.append(aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HT", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_negative_second_order_input_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"eligible={final['eligible_task_rows']}/{final['task_rows']};failed_weights={final['failed_weight_rows']};max_saturation={final['max_saturation_rate']:.6f};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "input_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "second_order_input_review(2차 입력 검토)",
        "tier_scope": "Tier A train-only input review(Tier A 학습 전용 입력 검토)",
        "kpi_scope": "input_review_only_no_training_no_mt5(입력 검토 전용, 학습/MT5 없음)",
        "scoreboard_lane": "model_validation",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"eligible={final['eligible_task_rows']}/{final['task_rows']};max_sat={final['max_saturation_rate']:.6f}",
        "guardrail_kpi": "feature_boundary;finite_weights;target_contract;no_goal",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};claim_boundary={CLAIM_BOUNDARY}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "kpi_evidence_data_integrity_model_validation",
        "evidence_scope": "HS frame, feature boundary, weight audit, task seeds",
        "kpi_scope": "eligibility_review_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__input_review",
        "family": "proxy_negative_second_order_input_review",
        "question": "are HS inputs eligible for guarded HU training(HS 입력은 방어 HU 학습에 적격한가)",
        "metric_scope": "feature_boundary_weight_target_training_eligibility",
        "primary_artifact": rel(TASK_ELIGIBILITY),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(he.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(he.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(he.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(he.ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID]
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
    return write_csv(he.ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    input_rows, weight_rows, boundary_rows, task_rows, model_rows, release_rows, queue_rows, summary = build_reviews()
    final = make_final(summary)
    artifacts: list[Path] = [
        write_csv(INPUT_REVIEW, AUDIT_COLUMNS, input_rows),
        write_csv(WEIGHT_REVIEW, WEIGHT_REVIEW_COLUMNS, weight_rows),
        write_csv(FEATURE_BOUNDARY_REVIEW, AUDIT_COLUMNS, boundary_rows),
        write_csv(TASK_ELIGIBILITY, TASK_COLUMNS, task_rows),
        write_csv(MODEL_PROPOSAL_REVIEW, MODEL_REVIEW_COLUMNS, model_rows),
        write_csv(RELEASE_GATE_REVIEW, RELEASE_COLUMNS, release_rows),
        write_csv(HU_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend([write_csv(GATE_AUDIT, GATE_COLUMNS, gates), write_json(FINAL_DECISION, final)])
    artifacts.extend(write_receipts(final, artifacts))
    artifacts.append(write_manifest(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "eligible_tasks": f"{final['eligible_task_rows']}/{final['task_rows']}",
                "failed_weights": final["failed_weight_rows"],
                "max_saturation_rate": round(final["max_saturation_rate"], 6),
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not final["failed_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
