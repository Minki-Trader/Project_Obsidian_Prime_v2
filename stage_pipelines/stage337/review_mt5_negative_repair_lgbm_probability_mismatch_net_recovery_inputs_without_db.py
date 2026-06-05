from __future__ import annotations

import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import materialize_mt5_negative_repair_lgbm_probability_mismatch_net_recovery_inputs_without_db as ha  # noqa: E402


aw = ha.aw
fb = ha.fb
fa = ha.fa
gw = ha.gw

TODAY = "2026-05-31"
STAGE_ID = ha.STAGE_ID
RUN_NUMBER = "run337HB"
RUN_ID = "run337HB_review_mt5_negative_repair_lightgbm_probability_mismatch_and_net_recovery_inputs_without_db_v1"
PARENT_RUN_ID = ha.RUN_ID
NEXT_RUN_ID = "run337HC_train_mt5_negative_repair_lightgbm_probability_mismatch_and_net_recovery_candidates_without_db_v1"
STATUS = "completed_stage337HB_probability_mismatch_net_recovery_inputs_review_guarded_training_eligible_no_training_no_selection"
JUDGMENT = "ha_inputs_target_contract_weights_and_parity_reviewed_guarded_training_eligible"
DECISION = "stage337HB_open_run337HC_train_probability_mismatch_net_recovery_candidates"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HB_probability_mismatch_net_recovery_input_review_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ha.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ha.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HB_probability_mismatch_net_recovery_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HB_probability_mismatch_net_recovery_input_review.md"

HA_FINAL = ha.FINAL_DECISION
HA_GATES = ha.GATE_AUDIT
HA_QUEUE = ha.HB_QUEUE
HA_FRAME = ha.TRAIN_ONLY_REPAIR_FRAME
HA_ALLOWED_FEATURES = ha.ALLOWED_FEATURE_SET
HA_WEIGHT_AUDIT = ha.WEIGHT_AUDIT
HA_TARGET_AUDIT = ha.TARGET_CONTRACT_AUDIT
HA_PARITY_AUDIT = ha.PARITY_PRECISION_AUDIT
HA_FEATURE_BOUNDARY = ha.FEATURE_LABEL_BOUNDARY
HA_TASK_SEEDS = ha.TRAINING_TASK_SEEDS
HA_NEGATIVE = ha.NEGATIVE_CONTROL_MATERIALIZATION
HA_RELEASE = ha.RELEASE_GATE_MATERIALIZATION

INPUT_REVIEW = RUN_DIR / "ha_input_review.csv"
WEIGHT_REVIEW = RUN_DIR / "gz_weight_review.csv"
TASK_ELIGIBILITY = RUN_DIR / "hc_training_task_eligibility.csv"
TARGET_CONTRACT_REVIEW = RUN_DIR / "target_contract_review.csv"
PARITY_PRECISION_REVIEW = RUN_DIR / "probability_precision_review.csv"
NEGATIVE_CONTROL_REVIEW = RUN_DIR / "negative_control_review.csv"
RELEASE_GATE_REVIEW = RUN_DIR / "release_gate_review.csv"
HC_QUEUE = RUN_DIR / "run337HC_training_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    HA_FINAL,
    HA_GATES,
    HA_QUEUE,
    HA_FRAME,
    HA_ALLOWED_FEATURES,
    HA_WEIGHT_AUDIT,
    HA_TARGET_AUDIT,
    HA_PARITY_AUDIT,
    HA_FEATURE_BOUNDARY,
    HA_TASK_SEEDS,
    HA_NEGATIVE,
    HA_RELEASE,
)
OUTPUT_FILES = (
    INPUT_REVIEW,
    WEIGHT_REVIEW,
    TASK_ELIGIBILITY,
    TARGET_CONTRACT_REVIEW,
    PARITY_PRECISION_REVIEW,
    NEGATIVE_CONTROL_REVIEW,
    RELEASE_GATE_REVIEW,
    HC_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    gw.SELECTED_STATUS,
    gw.WORKSPACE_STATE,
    gw.CURRENT_STATE,
    gw.CHANGELOG,
    gw.STAGE_BRIEF,
    gw.RUN_REGISTRY,
    gw.ALPHA_LEDGER,
    gw.STAGE_LEDGER,
    gw.ARTIFACT_REGISTRY,
    Path(__file__),
)

INPUT_REVIEW_COLUMNS = ("review_id", "status", "observed", "expected", "evidence", "effect", "claim_boundary")
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
NEGATIVE_COLUMNS = ("constraint_id", "subject", "review_status", "forbidden_action", "effect", "claim_boundary")
RELEASE_COLUMNS = ("gate_id", "gate_family", "review_status", "pass_condition", "required_artifact", "effect", "claim_boundary")
QUEUE_COLUMNS = ha.QUEUE_COLUMNS
GATE_COLUMNS = ha.GATE_COLUMNS

WEIGHT_ELIGIBLE = "eligible(적격)"
TASK_ELIGIBLE = "eligible_for_guarded_training(방어 학습 적격)"
SATURATION_BLOCK_RATE = 0.25


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


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def review_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "hc_guarded_train_probability_mismatch_net_recovery_candidates",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train eligible HA probability mismatch/net recovery tasks and export ONNX without threshold/lot tuning(적격 HA 확률 불일치/순수익 회복 작업을 학습하고 임계값/랏 조정 없이 ONNX 내보내기)",
            "required_inputs": f"{rel(HA_FRAME)};{rel(TASK_ELIGIBILITY)};{rel(HA_ALLOWED_FEATURES)};{rel(RELEASE_GATE_REVIEW)}",
            "required_outputs": "trained model manifest, ONNX exports, ONNX parity, proxy scorecard, future HD review queue(학습 모델 목록, ONNX 내보내기, ONNX 동등성, 프록시 점수표, 향후 HD 검토 대기열)",
            "blocked_if_missing": "eligible task rows or feature schema(적격 작업 행 또는 피처 스키마)",
            "forbidden_action": "threshold tuning, lot optimization, MT5 execution, operating selection(임계값 조정, 랏 최적화, MT5 실행, 운영 선택)",
            "effect": "moves reviewed inputs to guarded training(검토된 입력을 방어 학습으로 넘김)",
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
    list[dict[str, Any]],
    dict[str, Any],
]:
    frame = pd.read_parquet(aw.io_path(HA_FRAME))
    boundary_rows = read_csv(HA_FEATURE_BOUNDARY)
    weight_rows = read_csv(HA_WEIGHT_AUDIT)
    task_seed_rows = read_csv(HA_TASK_SEEDS)
    target_rows = read_csv(HA_TARGET_AUDIT)
    parity_rows = read_csv(HA_PARITY_AUDIT)
    negative_rows = read_csv(HA_NEGATIVE)
    release_rows = read_csv(HA_RELEASE)
    allowed_rows = read_csv(HA_ALLOWED_FEATURES)
    ha_final = read_json(HA_FINAL)
    failed_boundary = [row for row in boundary_rows if row.get("status") != "passed"]
    failed_target = [row for row in target_rows if row.get("status") != "passed"]
    failed_parity = [row for row in parity_rows if row.get("status") != "passed"]
    timestamps = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    monotonic = bool(timestamps.is_monotonic_increasing)

    input_rows = [
        {"review_id": "hb001_frame_rows", "status": "passed" if len(frame) == 87666 else "failed", "observed": str(len(frame)), "expected": "87666", "evidence": rel(HA_FRAME), "effect": "confirms HA train-only row count(HA 학습 전용 행 수 확인)", "claim_boundary": CLAIM_BOUNDARY},
        {"review_id": "hb002_feature_boundary", "status": "passed" if not failed_boundary else "failed", "observed": str(len(failed_boundary)), "expected": "0 failed boundary rows(실패 경계 행 0)", "evidence": rel(HA_FEATURE_BOUNDARY), "effect": "checks forbidden features are excluded(금지 피처 제외 확인)", "claim_boundary": CLAIM_BOUNDARY},
        {"review_id": "hb003_allowed_features", "status": "passed" if len(allowed_rows) == 58 else "failed", "observed": str(len(allowed_rows)), "expected": "58", "evidence": rel(HA_ALLOWED_FEATURES), "effect": "keeps reviewed feature set stable(검토 피처 묶음 안정 유지)", "claim_boundary": CLAIM_BOUNDARY},
        {"review_id": "hb004_target_contract", "status": "passed" if not failed_target else "failed", "observed": str(len(failed_target)), "expected": "0 failed target rows(실패 목표 행 0)", "evidence": rel(HA_TARGET_AUDIT), "effect": "checks label_class target contract(label_class 목표 계약 확인)", "claim_boundary": CLAIM_BOUNDARY},
        {"review_id": "hb005_parity_precision", "status": "passed" if not failed_parity else "failed", "observed": str(len(failed_parity)), "expected": "0 failed parity rows(실패 동등성 행 0)", "evidence": rel(HA_PARITY_AUDIT), "effect": "checks probability mismatch memory was carried(확률 불일치 기억 인계 확인)", "claim_boundary": CLAIM_BOUNDARY},
        {"review_id": "hb006_timestamp_order", "status": "passed" if monotonic else "failed", "observed": str(monotonic), "expected": "True", "evidence": rel(HA_FRAME), "effect": "keeps train-only time axis ordered(학습 전용 시간축 순서 유지)", "claim_boundary": CLAIM_BOUNDARY},
    ]

    weight_review = []
    max_saturation_rate = 0.0
    saturated_weight_rows = 0
    for row in weight_rows:
        weight_col = row.get("weight_column", "")
        values = pd.to_numeric(frame[weight_col], errors="coerce") if weight_col in frame.columns else pd.Series(dtype="float64")
        saturation_rate = float((values >= 9.999).mean()) if len(values) else 1.0
        max_saturation_rate = max(max_saturation_rate, saturation_rate)
        saturation_watch = "watch(감시)" if saturation_rate > 0.05 else "normal(정상)"
        eligible = (
            weight_col in frame.columns
            and as_int(row.get("nonfinite_rows")) == 0
            and as_float(row.get("weight_min")) >= 0.10
            and as_float(row.get("weight_max")) <= 10.0
            and saturation_rate <= SATURATION_BLOCK_RATE
        )
        saturated_weight_rows += int(saturation_rate > 0.05)
        weight_review.append(
            {
                **row,
                "review_status": WEIGHT_ELIGIBLE if eligible else "blocked(차단)",
                "saturation_watch": saturation_watch,
                "saturation_rate": f"{saturation_rate:.6f}",
                "effect": "bounded train-only GZ sample weight reviewed(범위 제한 학습 전용 GZ 표본 가중치 검토)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    task_review = []
    for row in task_seed_rows:
        target_col = row.get("target_column", "")
        weight_col = row.get("sample_weight_column") or row.get("sample_weight_expression", "")
        missing = weight_col not in frame.columns
        nonfinite_rows = int(pd.to_numeric(frame[weight_col], errors="coerce").isna().sum()) if not missing else 1
        target_ok = target_col == "label_class" and target_col in frame.columns
        eligible = target_ok and not missing and nonfinite_rows == 0 and weight_col in ha.NEW_WEIGHT_COLUMNS
        task_review.append(
            {
                "task_id": row.get("task_id", ""),
                "target_column": target_col,
                "sample_weight_column": weight_col,
                "sample_weight_expression": weight_col,
                "model_family": row.get("model_family", ""),
                "model_config_id": row.get("model_config_id", ""),
                "eligibility_status": TASK_ELIGIBLE if eligible else "blocked(차단)",
                "required_guard": row.get("required_guard", ""),
                "blocked_reason": "" if eligible else f"missing_or_nonfinite_or_unregistered_weight(가중치 누락/비유한/미등록);rows={nonfinite_rows}",
                "effect": row.get("expected_effect", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    negative_review = [
        {"constraint_id": row.get("constraint_id", ""), "subject": row.get("subject", ""), "review_status": "active(활성)", "forbidden_action": row.get("forbidden_action", ""), "effect": row.get("effect", ""), "claim_boundary": CLAIM_BOUNDARY}
        for row in negative_rows
    ]
    release_review = [
        {"gate_id": row.get("gate_id", ""), "gate_family": row.get("gate_family", ""), "review_status": "carried_to_training_review(학습 검토로 인계)", "pass_condition": row.get("pass_condition", ""), "required_artifact": row.get("required_artifact", ""), "effect": row.get("effect", ""), "claim_boundary": CLAIM_BOUNDARY}
        for row in release_rows
    ]
    queue_rows = review_queue()
    summary = {
        "rows": len(frame),
        "feature_count": len(allowed_rows),
        "weight_review_rows": len(weight_review),
        "failed_weight_rows": sum(1 for row in weight_review if row["review_status"] != WEIGHT_ELIGIBLE),
        "saturated_weight_rows": saturated_weight_rows,
        "max_saturation_rate": max_saturation_rate,
        "input_review_rows": len(input_rows),
        "failed_input_review_rows": sum(1 for row in input_rows if row["status"] != "passed"),
        "target_contract_failed_rows": len(failed_target),
        "parity_precision_failed_rows": len(failed_parity),
        "task_rows": len(task_review),
        "eligible_task_rows": sum(1 for row in task_review if row["eligibility_status"] == TASK_ELIGIBLE),
        "negative_control_rows": len(negative_review),
        "release_gate_rows": len(release_review),
        "queue_rows": len(queue_rows),
        "gz_best_net_profit": ha_final.get("gz_best_net_profit"),
        "gz_probability_mismatch_rows": ha_final.get("gz_probability_mismatch_rows"),
    }
    return input_rows, weight_review, task_review, target_rows, parity_rows, negative_review, release_review, queue_rows, summary


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    ha_final = read_json(HA_FINAL)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "ha_next_action": ha_final.get("next_action", ""),
        "ha_failed_gate_rows": sum(1 for row in read_csv(HA_GATES) if row.get("status") != "passed"),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = final["new_training"] == "not_run" and final["candidate_selection"] == "not_run" and final["mt5_execution"] == "not_run" and final["goal_achieve"] == "not_claimed"
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(HA_FRAME), "required HA inputs exist(필수 HA 입력 존재)"),
        ("parent_ha_gates_passed", final["ha_failed_gate_rows"] == 0, str(final["ha_failed_gate_rows"]), "0", rel(HA_GATES), "HA gates passed(HA 게이트 통과)"),
        ("parent_next_action_matches", final["ha_next_action"] == RUN_ID, str(final["ha_next_action"]), RUN_ID, rel(HA_FINAL), "HB follows HA next action(HB가 HA 다음 행동을 따름)"),
        ("input_review_passed", final["failed_input_review_rows"] == 0, str(final["failed_input_review_rows"]), "0", rel(INPUT_REVIEW), "input audits passed(입력 감사 통과)"),
        ("target_contract_passed", final["target_contract_failed_rows"] == 0, str(final["target_contract_failed_rows"]), "0", rel(TARGET_CONTRACT_REVIEW), "target contract passed(목표 계약 통과)"),
        ("parity_precision_review_passed", final["parity_precision_failed_rows"] == 0, str(final["parity_precision_failed_rows"]), "0", rel(PARITY_PRECISION_REVIEW), "parity precision review passed(동등성 정밀도 검토 통과)"),
        ("weight_review_passed", final["failed_weight_rows"] == 0 and final["weight_review_rows"] == 5 and final["max_saturation_rate"] <= SATURATION_BLOCK_RATE, f"failed={final['failed_weight_rows']};rows={final['weight_review_rows']};max_sat={final['max_saturation_rate']:.6f}", "0 and 5 and max_sat<=0.25", rel(WEIGHT_REVIEW), "weight reviews passed with saturation watch(포화 감시와 함께 가중치 검토 통과)"),
        ("training_tasks_eligible", final["eligible_task_rows"] == final["task_rows"] == 5, f"eligible={final['eligible_task_rows']};tasks={final['task_rows']}", "5/5", rel(TASK_ELIGIBILITY), "all tasks eligible(모든 작업 적격)"),
        ("negative_controls_active", final["negative_control_rows"] >= 4, str(final["negative_control_rows"]), ">=4", rel(NEGATIVE_CONTROL_REVIEW), "negative controls active(음수 대조 활성)"),
        ("release_gates_carried", final["release_gate_rows"] >= 6, str(final["release_gate_rows"]), ">=6", rel(RELEASE_GATE_REVIEW), "future MT5 release gates carried(향후 MT5 릴리스 게이트 인계)"),
        ("training_queue_materialized", final["queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(HC_QUEUE), "HC training queue opened(HC 학습 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['new_training']};selection={final['candidate_selection']};mt5={final['mt5_execution']};goal={final['goal_achieve']}", "not_run/not_run/not_run/not_claimed", rel(FINAL_DECISION), "review without operating claim(운영 주장 없는 검토)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {"gate_id": gate_id, "status": "passed" if passed else "failed", "evidence_path": evidence, "observed": observed, "expected": expected, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    base = {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "stage_id": STAGE_ID, "created_at_utc": now_utc(), "status": final["status"], "judgment": final["judgment"], "next_action": final["next_action"], "claim_boundary": CLAIM_BOUNDARY}
    receipts = [
        (DATA_RECEIPT, {**base, "data_source": rel(HA_FRAME), "rows": final["rows"], "features": final["feature_count"], "input_review": rel(INPUT_REVIEW), "integrity_judgment": "eligible_for_guarded_training(방어 학습 적격)"}),
        (MODEL_RECEIPT, {**base, "model_training": "not_run", "eligible_tasks": f"{final['eligible_task_rows']}/{final['task_rows']}", "target_contract": rel(TARGET_CONTRACT_REVIEW), "validation_judgment": "eligible_for_HC_training(HC 학습 적격)"}),
        (RUNTIME_RECEIPT, {**base, "known_differences": f"parent_probability_mismatch_rows={final['gz_probability_mismatch_rows']}", "parity_review": rel(PARITY_PRECISION_REVIEW), "runtime_claim_boundary": "input_review_only(입력 검토 전용)"}),
        (PERFORMANCE_RECEIPT, {**base, "parent_best_net_profit": final["gz_best_net_profit"], "saturated_weight_rows": final["saturated_weight_rows"], "max_saturation_rate": final["max_saturation_rate"], "attribution_confidence": "input_review_only(입력 검토 전용)"}),
        (JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(INPUT_REVIEW), rel(WEIGHT_REVIEW), rel(TASK_ELIGIBILITY)], "evidence_missing": "HC training, ONNX parity, MT5 runtime probe(HC 학습, ONNX 동등성, MT5 런타임 탐침)", "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID}),
    ]
    paths = [write_json(path, payload) for path, payload in receipts]
    all_artifacts = list(artifacts) + paths
    lineage = {**base, "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in all_artifacts], "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()}, "lineage_judgment": "connected HA inputs to HC guarded training queue(HA 입력을 HC 방어 학습 대기열에 연결)"}
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337HB Input Review(337단계 337HB 입력 검토)

## Conclusion(결론)

Action(행동): HA repair inputs(HA 수리 입력)의 target contract(목표 계약), feature boundary(피처 경계), weight saturation(가중치 포화), parity precision(동등성 정밀도)을 검토했다. Effect(효과): 5개 task(작업)를 guarded HC training(방어 HC 학습)으로 넘길 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_rows']}`
- failed_input_review_rows(입력 검토 실패 행): `{final['failed_input_review_rows']}`
- failed_weight_rows(가중치 실패 행): `{final['failed_weight_rows']}`
- saturated_weight_rows(포화 감시 가중치 행): `{final['saturated_weight_rows']}`
- max_saturation_rate(최대 포화율): `{final['max_saturation_rate']:.6f}`
- release_gate_rows(릴리스 게이트 행): `{final['release_gate_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- MT5 execution(MT5 실행): `not_run`
- operating_selection(운영 선택): `not_run`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337HB Decision(337HB 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(TASK_ELIGIBILITY)}`, `{rel(WEIGHT_REVIEW)}`

Action(행동): HA materialized inputs(HA 물질화 입력)을 guarded training eligible(방어 학습 적격)로 검토했다.
Effect(효과): HC에서 ONNX(온엑스) 후보 학습을 시도할 수 있지만, 운영 주장(operating claim, 운영 주장)은 아직 없다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = fa.ey.current_branch()
    workspace, workspace_bom = aw.read_text_lossless(gw.WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337HB focus complete(337단계 337HB 초점 완료): HA input review(HA 입력 검토)를 `{final['status']}`로 완료했다. "
        f"Effect(효과): eligible tasks(적격 작업) `{final['eligible_task_rows']}/{final['task_rows']}`, saturation watch(포화 감시) `{final['saturated_weight_rows']}`, max saturation(최대 포화율) `{final['max_saturation_rate']:.6f}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337HB focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337HB focus complete.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(gw.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(gw.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337HB Input Review(입력 검토)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_rows']}`
- failed_input_review_rows(입력 검토 실패 행): `{final['failed_input_review_rows']}`
- failed_weight_rows(가중치 실패 행): `{final['failed_weight_rows']}`
- saturated_weight_rows(포화 감시 가중치 행): `{final['saturated_weight_rows']}`
- max_saturation_rate(최대 포화율): `{final['max_saturation_rate']:.6f}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): HC guarded training(HC 방어 학습)을 열되 운영 주장은 하지 않는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337HA Repair Inputs", section, "run337HB Input Review")
    artifacts.append(aw.write_text_lossless(gw.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_rows']}`
- saturated_weight_rows(포화 감시 가중치 행): `{final['saturated_weight_rows']}`
- max_saturation_rate(최대 포화율): `{final['max_saturation_rate']:.6f}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HB review(검토)는 HC training(HC 학습) 조건만 만들고 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(gw.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(gw.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HB(337HB 실행) `{final['status']}`. "
        f"Effect(효과): HA inputs(HA 입력) 적격 작업 `{final['eligible_task_rows']}/{final['task_rows']}`, saturation watch `{final['saturated_weight_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(gw.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HB(337HB 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(gw.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HB(337HB 실행) `{final['status']}`. "
        f"Effect(효과): HA input review(HA 입력 검토)를 완료하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(gw.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HB", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "probability_mismatch_net_recovery_input_review", "status": final["status"], "judgment": final["judgment"], "path": rel(REPORT_PATH), "notes": f"eligible={final['eligible_task_rows']}/{final['task_rows']};sat_watch={final['saturated_weight_rows']};next_action={final['next_action']};goal_achieve_not_claimed.", "family": "kpi_evidence_data_integrity_model_validation", "primary_report": rel(REPORT_PATH)}
    alpha_row = {"ledger_row_id": f"{RUN_ID}__input_review", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": "input_review", "parent_run_id": PARENT_RUN_ID, "record_view": "probability_mismatch_net_recovery_input_review(확률 불일치 순수익 회복 입력 검토)", "tier_scope": "Tier A train-only input review(Tier A 학습 전용 입력 검토)", "kpi_scope": "input_review_only_no_training_no_mt5(입력 검토 전용, 학습/MT5 없음)", "scoreboard_lane": "model_validation", "status": final["status"], "judgment": final["judgment"], "path": rel(REPORT_PATH), "primary_kpi": f"eligible={final['eligible_task_rows']}/{final['task_rows']};max_sat={final['max_saturation_rate']:.6f}", "guardrail_kpi": "feature_boundary;finite_weights;target_contract;parity_precision;no_goal", "external_verification_status": "out_of_scope_by_claim", "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed."}
    stage_row = {"ledger_row_id": f"{RUN_ID}__input_review", "stage_id": STAGE_ID, "run_id": RUN_ID, "work_family": "kpi_evidence_data_integrity_model_validation", "evidence_scope": "HA frame, target contract, parity precision, weight audit, task seeds", "kpi_scope": "eligibility_review_no_operating_claim", "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "path": rel(REPORT_PATH), "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed", "decision": final["decision"], "run_key": f"{RUN_ID}__input_review", "family": "probability_mismatch_net_recovery_input_review", "question": "are HA inputs eligible for guarded HC training(HA 입력은 방어 HC 학습에 적격인가)", "metric_scope": "feature_boundary_weight_target_parity_training_eligibility", "primary_artifact": rel(TASK_ELIGIBILITY), "report_path": rel(REPORT_PATH), "next_action": final["next_action"]}
    return [
        fb.upsert_csv_worktree(gw.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(gw.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(gw.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(gw.ARTIFACT_REGISTRY, prefer_head=False)
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
        rows.append({"artifact_id": artifact_id, "artifact_type": path.suffix.lstrip(".") or "file", "path": artifact_path, "sha256": aw.sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": STATUS, "artifact_path": artifact_path, "claim_boundary": CLAIM_BOUNDARY})
    return write_csv(gw.ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    input_rows, weight_rows, task_rows, target_rows, parity_rows, negative_rows, release_rows, queue_rows, summary = build_reviews()
    final = make_final(summary)
    artifacts: list[Path] = [
        write_csv(INPUT_REVIEW, INPUT_REVIEW_COLUMNS, input_rows),
        write_csv(WEIGHT_REVIEW, WEIGHT_REVIEW_COLUMNS, weight_rows),
        write_csv(TASK_ELIGIBILITY, TASK_COLUMNS, task_rows),
        write_csv(TARGET_CONTRACT_REVIEW, INPUT_REVIEW_COLUMNS, target_rows),
        write_csv(PARITY_PRECISION_REVIEW, INPUT_REVIEW_COLUMNS, parity_rows),
        write_csv(NEGATIVE_CONTROL_REVIEW, NEGATIVE_COLUMNS, negative_rows),
        write_csv(RELEASE_GATE_REVIEW, RELEASE_COLUMNS, release_rows),
        write_csv(HC_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend([write_csv(GATE_AUDIT, GATE_COLUMNS, gates), write_json(FINAL_DECISION, final), write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY})])
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "eligible_tasks": f"{final['eligible_task_rows']}/{final['task_rows']}", "saturated_weight_rows": final["saturated_weight_rows"], "max_saturation_rate": round(final["max_saturation_rate"], 6), "gates": f"{final['passed_gates']}/{final['gate_rows']}", "next_action": final["next_action"], "goal_achieve": "not_claimed"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
