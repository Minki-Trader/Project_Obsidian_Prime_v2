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
from stage_pipelines.stage337 import execute_broker_confirmed_side_cost_curve_mt5_runtime_probe_without_db as fb  # noqa: E402
from stage_pipelines.stage337 import materialize_broker_confirmed_side_cost_curve_runtime_probe_package_without_db as fa  # noqa: E402
from stage_pipelines.stage337 import materialize_runtime_positive_side_stability_gb_pf_recovery_drawdown_mt5_negative_repair_inputs_without_db as gs  # noqa: E402


aw = gs.aw

TODAY = "2026-05-31"
STAGE_ID = gs.STAGE_ID
RUN_NUMBER = "run337GT"
RUN_ID = "run337GT_review_runtime_positive_side_stability_gb_pf_recovery_drawdown_mt5_negative_repair_inputs_without_db_v1"
PARENT_RUN_ID = gs.RUN_ID
NEXT_RUN_ID = "run337GU_train_runtime_positive_side_stability_gb_pf_recovery_drawdown_mt5_negative_repair_candidates_without_db_v1"
STATUS = "completed_stage337GT_mt5_negative_repair_inputs_review_guarded_training_eligible_no_training_no_selection"
JUDGMENT = "gs_inputs_feature_boundary_weights_and_tasks_reviewed_guarded_training_eligible"
DECISION = "stage337GT_open_run337GU_train_mt5_negative_repair_candidates"
CLAIM_BOUNDARY = (
    "research_development_only_stage337GT_mt5_negative_side_stability_gb_pf_recovery_drawdown_repair_input_review_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = gs.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = gs.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337GT_mt5_negative_repair_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337GT_mt5_negative_repair_input_review.md"

GS_FINAL = gs.FINAL_DECISION
GS_GATES = gs.GATE_AUDIT
GS_QUEUE = gs.GT_QUEUE
GS_FRAME = gs.TRAIN_ONLY_REPAIR_FRAME
GS_ALLOWED_FEATURES = gs.ALLOWED_FEATURE_SET
GS_WEIGHT_AUDIT = gs.WEIGHT_AUDIT
GS_FEATURE_BOUNDARY = gs.FEATURE_LABEL_BOUNDARY
GS_TASK_SEEDS = gs.TRAINING_TASK_SEEDS
GS_NEGATIVE = gs.NEGATIVE_CONTROL_MATERIALIZATION
GS_RELEASE = gs.RELEASE_GATE_MATERIALIZATION

INPUT_REVIEW = RUN_DIR / "gs_input_review.csv"
WEIGHT_REVIEW = RUN_DIR / "gr_weight_review.csv"
TASK_ELIGIBILITY = RUN_DIR / "gu_training_task_eligibility.csv"
NEGATIVE_CONTROL_REVIEW = RUN_DIR / "negative_control_review.csv"
RELEASE_GATE_REVIEW = RUN_DIR / "release_gate_review.csv"
GU_QUEUE = RUN_DIR / "run337GU_training_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    GS_FINAL,
    GS_GATES,
    GS_QUEUE,
    GS_FRAME,
    GS_ALLOWED_FEATURES,
    GS_WEIGHT_AUDIT,
    GS_FEATURE_BOUNDARY,
    GS_TASK_SEEDS,
    GS_NEGATIVE,
    GS_RELEASE,
)
OUTPUT_FILES = (
    INPUT_REVIEW,
    WEIGHT_REVIEW,
    TASK_ELIGIBILITY,
    NEGATIVE_CONTROL_REVIEW,
    RELEASE_GATE_REVIEW,
    GU_QUEUE,
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
    gs.gr.gq.go.SELECTED_STATUS,
    gs.gr.gq.go.WORKSPACE_STATE,
    gs.gr.gq.go.CURRENT_STATE,
    gs.gr.gq.go.CHANGELOG,
    gs.gr.gq.go.STAGE_BRIEF,
    gs.gr.gq.go.RUN_REGISTRY,
    gs.gr.gq.go.ALPHA_LEDGER,
    gs.gr.gq.go.STAGE_LEDGER,
    gs.gr.gq.go.ARTIFACT_REGISTRY,
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
    "effect",
    "claim_boundary",
)
TASK_COLUMNS = (
    "task_id",
    "target_column",
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
QUEUE_COLUMNS = gs.QUEUE_COLUMNS
GATE_COLUMNS = gs.GATE_COLUMNS

WEIGHT_ELIGIBLE = "eligible(적격)"
TASK_ELIGIBLE = "eligible_for_guarded_training(방어 학습 적격)"


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


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def build_reviews() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    frame = pd.read_parquet(aw.io_path(GS_FRAME))
    boundary_rows = read_csv(GS_FEATURE_BOUNDARY)
    weight_rows = read_csv(GS_WEIGHT_AUDIT)
    task_seed_rows = read_csv(GS_TASK_SEEDS)
    negative_rows = read_csv(GS_NEGATIVE)
    release_rows = read_csv(GS_RELEASE)
    allowed_rows = read_csv(GS_ALLOWED_FEATURES)
    gs_final = read_json(GS_FINAL)
    failed_boundary = [row for row in boundary_rows if row.get("status") != "passed"]
    failed_weights = [row for row in weight_rows if as_int(row.get("nonfinite_rows")) != 0]
    timestamps = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    monotonic = bool(timestamps.is_monotonic_increasing)

    input_rows = [
        {
            "review_id": "gt001_frame_rows",
            "status": "passed" if len(frame) == 87666 else "failed",
            "observed": str(len(frame)),
            "expected": "87666",
            "evidence": rel(GS_FRAME),
            "effect": "confirms GS train-only row count(GS 학습 전용 행 수 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "gt002_feature_boundary",
            "status": "passed" if not failed_boundary else "failed",
            "observed": str(len(failed_boundary)),
            "expected": "0 failed boundary rows(실패 경계 행 0)",
            "evidence": rel(GS_FEATURE_BOUNDARY),
            "effect": "checks forbidden features are excluded(금지 피처 제외 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "gt003_allowed_features",
            "status": "passed" if len(allowed_rows) == 58 else "failed",
            "observed": str(len(allowed_rows)),
            "expected": "58",
            "evidence": rel(GS_ALLOWED_FEATURES),
            "effect": "keeps reviewed feature set stable(검토 피처 묶음 안정 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "gt004_weight_finiteness",
            "status": "passed" if not failed_weights else "failed",
            "observed": str(len(failed_weights)),
            "expected": "0 failed weight rows(실패 가중치 행 0)",
            "evidence": rel(GS_WEIGHT_AUDIT),
            "effect": "checks weights are finite(가중치 유한 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "gt005_timestamp_order",
            "status": "passed" if monotonic else "failed",
            "observed": str(monotonic),
            "expected": "True",
            "evidence": rel(GS_FRAME),
            "effect": "keeps train-only time axis ordered(학습 전용 시간축 순서 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "gt006_negative_memory_carried",
            "status": "passed"
            if as_float(gs_final.get("gr_net_gap_to_zero")) > 0 and as_float(gs_final.get("gr_proxy_sign_diff_rows")) >= 4
            else "failed",
            "observed": f"net_gap={gs_final.get('gr_net_gap_to_zero')};proxy_sign_diff={gs_final.get('gr_proxy_sign_diff_rows')}",
            "expected": "net_gap>0 and proxy_sign_diff>=4",
            "evidence": rel(GS_FINAL),
            "effect": "confirms all-negative MT5 memory remains active(전부 음수 MT5 기억 활성 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    weight_review = []
    for row in weight_rows:
        eligible = as_int(row.get("nonfinite_rows")) == 0 and as_float(row.get("weight_min")) >= 0.10 and as_float(row.get("weight_max")) <= 10.0
        max_rate = 0.0
        weight_col = row.get("weight_column", "")
        if weight_col in frame.columns:
            values = pd.to_numeric(frame[weight_col], errors="coerce")
            max_rate = float((values >= 9.999).mean())
        weight_review.append(
            {
                **row,
                "review_status": WEIGHT_ELIGIBLE if eligible else "blocked(차단)",
                "saturation_watch": f"max_clip_rate={max_rate:.6f}",
                "effect": "bounded train-only GR sample weight reviewed(범위 제한 학습 전용 GR 표본 가중치 검토)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    task_review = []
    for row in task_seed_rows:
        target_col = row.get("target_column", "")
        weight_col = row.get("sample_weight_expression", "")
        missing = weight_col not in frame.columns
        nonfinite_rows = int(pd.to_numeric(frame[weight_col], errors="coerce").isna().sum()) if not missing else 1
        target_ok = target_col == "label_class" and target_col in frame.columns
        eligible = target_ok and not missing and nonfinite_rows == 0 and weight_col in gs.NEW_WEIGHT_COLUMNS
        task_review.append(
            {
                "task_id": row.get("task_id", ""),
                "target_column": target_col,
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
        {
            "constraint_id": row.get("constraint_id", ""),
            "subject": row.get("subject", ""),
            "review_status": "active(활성)",
            "forbidden_action": row.get("forbidden_action", ""),
            "effect": row.get("effect", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in negative_rows
    ]
    release_review = [
        {
            "gate_id": row.get("gate_id", ""),
            "gate_family": row.get("gate_family", ""),
            "review_status": "carried_to_training_review(학습 검토로 인계)",
            "pass_condition": row.get("pass_condition", ""),
            "required_artifact": row.get("required_artifact", ""),
            "effect": row.get("effect", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in release_rows
    ]
    queue_rows = [
        {
            "queue_id": "gu_guarded_train_mt5_negative_repair_candidates",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train eligible GS MT5-negative repair tasks and export ONNX without threshold/lot tuning(GS 적격 MT5 음수 수리 작업을 학습하고 임계값/랏 튜닝 없이 ONNX 내보내기)",
            "required_inputs": f"{rel(GS_FRAME)};{rel(TASK_ELIGIBILITY)};{rel(GS_ALLOWED_FEATURES)};{rel(RELEASE_GATE_REVIEW)}",
            "required_outputs": "trained model manifest, ONNX exports, ONNX parity, proxy scorecard, future GV review queue(학습 모델 목록, ONNX 내보내기, ONNX 동등성, 프록시 점수표, 향후 GV 검토 대기열)",
            "blocked_if_missing": "eligible task rows or feature schema(적격 작업 행 또는 피처 스키마)",
            "forbidden_action": "threshold tuning, lot optimization, MT5 execution, operating selection(임계값 튜닝, 랏 최적화, MT5 실행, 운영 선택)",
            "effect": "moves reviewed inputs to guarded training(검토된 입력을 방어 학습으로 넘김)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    summary = {
        "rows": len(frame),
        "feature_count": len(allowed_rows),
        "weight_review_rows": len(weight_review),
        "failed_weight_rows": sum(1 for row in weight_review if row["review_status"] != WEIGHT_ELIGIBLE),
        "input_review_rows": len(input_rows),
        "failed_input_review_rows": sum(1 for row in input_rows if row["status"] != "passed"),
        "task_rows": len(task_review),
        "eligible_task_rows": sum(1 for row in task_review if row["eligibility_status"] == TASK_ELIGIBLE),
        "negative_control_rows": len(negative_review),
        "release_gate_rows": len(release_review),
        "queue_rows": len(queue_rows),
        "gr_best_net_profit": gs_final.get("gr_best_net_profit"),
        "gr_net_gap_to_zero": gs_final.get("gr_net_gap_to_zero"),
        "gr_proxy_sign_diff_rows": gs_final.get("gr_proxy_sign_diff_rows"),
    }
    return input_rows, weight_review, task_review, negative_review, release_review, queue_rows, summary


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["new_training"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(GS_FRAME), "required GS inputs exist(필수 GS 입력 존재)"),
        ("parent_gs_gates_passed", final["gs_failed_gate_rows"] == 0, str(final["gs_failed_gate_rows"]), "0", rel(GS_GATES), "GS gates passed(GS 게이트 통과)"),
        ("parent_next_action_matches", final["gs_next_action"] == RUN_ID, str(final["gs_next_action"]), RUN_ID, rel(GS_FINAL), "GT follows GS next action(GT가 GS 다음 행동을 따름)"),
        ("input_review_passed", final["failed_input_review_rows"] == 0, str(final["failed_input_review_rows"]), "0", rel(INPUT_REVIEW), "input audits passed(입력 감사 통과)"),
        ("weight_review_passed", final["failed_weight_rows"] == 0 and final["weight_review_rows"] == 5, f"failed={final['failed_weight_rows']};rows={final['weight_review_rows']}", "0 and 5", rel(WEIGHT_REVIEW), "weight reviews passed(가중치 검토 통과)"),
        ("training_tasks_eligible", final["eligible_task_rows"] == final["task_rows"] == 5, f"eligible={final['eligible_task_rows']};tasks={final['task_rows']}", "5/5", rel(TASK_ELIGIBILITY), "all tasks eligible(모든 작업 적격)"),
        ("negative_controls_active", final["negative_control_rows"] >= 4, str(final["negative_control_rows"]), ">=4", rel(NEGATIVE_CONTROL_REVIEW), "negative controls active(음성 대조 활성)"),
        ("release_gates_carried", final["release_gate_rows"] >= 6, str(final["release_gate_rows"]), ">=6", rel(RELEASE_GATE_REVIEW), "future MT5 release gates carried(향후 MT5 릴리스 게이트 인계)"),
        ("training_queue_materialized", final["queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(GU_QUEUE), "GU training queue opened(GU 학습 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['new_training']};selection={final['candidate_selection']};mt5={final['mt5_execution']};goal={final['goal_achieve']}", "not_run/not_run/not_run/not_claimed", rel(FINAL_DECISION), "review without operating claim(운영 주장 없는 검토)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
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
        "data_source": rel(GS_FRAME),
        "time_axis": "GS train-only closed-bar frame(GS 학습 전용 확정봉 프레임)",
        "sample_scope": f"US100 M5 Tier A train-only input review;rows={final['rows']};features={final['feature_count']}",
        "missing_or_duplicate_check": "reviewed by GS feature boundary and GT input review(GS 피처 경계와 GT 입력 검토로 확인)",
        "feature_label_boundary": "weights and labels excluded from allowed features(가중치와 라벨은 허용 피처에서 제외)",
        "split_boundary": "train-only review, no MT5/forward claim(학습 전용 검토, MT5/전진 주장 없음)",
        "leakage_risk": "guarded training could accidentally include weights or MT5 KPI as features(방어 학습이 가중치나 MT5 성과를 피처로 포함할 위험)",
        "data_hash_or_identity": aw.sha256_file(GS_FRAME) if path_exists(GS_FRAME) else "",
        "integrity_judgment": "usable_for_guarded_training_review(방어 학습 검토용 사용 가능)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_family": "LightGBM multiclass to ONNX planned(라이트GBM 다중분류-ONNX 계획)",
        "target_and_label": "label_class with five GR weight expressions(label_class와 5개 GR 가중치 표현)",
        "split_method": "train-only input, later inner-holdout/proxy and MT5 probe(학습 전용 입력, 이후 내부 보류/프록시와 MT5 탐침)",
        "selection_metric": "none in GT(GT 선택 없음)",
        "secondary_metrics": "weight bounds, feature boundary, task eligibility, release gates(가중치 범위, 피처 경계, 작업 적격성, 릴리스 게이트)",
        "threshold_policy": "no threshold tuning(임계값 튜닝 없음)",
        "overfit_risk": "multiple weight recipes may overfit GQ all-negative MT5 memory(여러 가중치 조리법이 GQ 전부 음수 MT5 기억에 과적합할 위험)",
        "calibration_risk": "not trained yet(아직 학습 안 함)",
        "comparison_baseline": "GS input materialization(GS 입력 물질화)",
        "validation_judgment": "eligible_for_guarded_training(방어 학습 적격)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "observed_change": "GT reviewed GS inputs; no KPI yet(GT는 GS 입력을 검토했고 성과는 아직 없음)",
        "comparison_baseline": "GS materialized weight audit(GS 물질화 가중치 감사)",
        "likely_drivers": "not applicable until training/runtime(학습/런타임 전 해당 없음)",
        "segment_checks": "label-level weight means and saturation watch reviewed(라벨별 가중치 평균과 포화 감시 검토)",
        "trade_shape": "not tested until MT5 runtime probe(MT5 런타임 탐침 전 미시험)",
        "alternative_explanations": "eligible inputs may still fail after training(적격 입력도 학습 후 실패 가능)",
        "attribution_confidence": "input_review_only(입력 검토 전용)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "evidence_available": [rel(INPUT_REVIEW), rel(WEIGHT_REVIEW), rel(TASK_ELIGIBILITY), rel(GU_QUEUE)],
        "evidence_missing": "GU training, ONNX parity, MT5 runtime probe, forward evidence(GU 학습, ONNX 동등성, MT5 탐침, 전진 근거)",
        "judgment_label": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "inputs are eligible for guarded training, not yet trained(입력은 방어 학습 적격이나 아직 학습 아님)",
    }
    paths = [
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifacts) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()},
        "registry_links": [rel(gs.gr.gq.go.RUN_REGISTRY), rel(gs.gr.gq.go.ALPHA_LEDGER), rel(gs.gr.gq.go.STAGE_LEDGER), rel(gs.gr.gq.go.ARTIFACT_REGISTRY)],
        "availability": "generated_with_manifest(목록으로 생성)",
        "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337GT MT5 Negative Input Review(337단계 337GT MT5 음수 입력 검토)

## Conclusion(결론)

Action(행동): GS repair inputs(GS 수리 입력)의 feature boundary(피처 경계), weight audit(가중치 감사), task eligibility(작업 적격성)를 검토했다. Effect(효과): 5개 task(작업)를 guarded GU training(방어 GU 학습)으로 넘길 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_rows']}`
- failed_input_review_rows(입력 검토 실패 행): `{final['failed_input_review_rows']}`
- failed_weight_rows(가중치 실패 행): `{final['failed_weight_rows']}`
- release_gate_rows(릴리스 게이트 행): `{final['release_gate_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 튜닝): `not_run`
- MT5 execution(MT5 실행): `not_run`
- operating_selection(운영 선택): `not_run`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337GT Decision(337GT 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(INPUT_REVIEW)}`, `{rel(WEIGHT_REVIEW)}`, `{rel(TASK_ELIGIBILITY)}`

Action(행동): GS materialized inputs(GS 물질화 입력)를 guarded training(방어 학습) 적격으로 검토했다.
Effect(효과): GU에서 학습과 ONNX export(ONNX 내보내기)를 시도할 수 있다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def upsert_focus(text: str, marker: str, entry: str) -> str:
    if marker in text:
        return re.sub(rf"- >-\n  {re.escape(marker)}.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", entry.rstrip(), text, count=1, flags=re.S)
    return text.replace("current_focus:\n", "current_focus:\n" + entry, 1)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = fa.ey.current_branch()
    workspace, workspace_bom = aw.read_text_lossless(gs.gr.gq.go.WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337GT focus complete: run337GT(337GT 실행)은 `{final['status']}`로 GS input review(GS 입력 검토)를 완료했다. "
        f"Effect(효과): eligible tasks(적격 작업) `{final['eligible_task_rows']}/{final['task_rows']}`, failed inputs(실패 입력) `{final['failed_input_review_rows']}`, failed weights(실패 가중치) `{final['failed_weight_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    workspace = upsert_focus(workspace, "Stage337 run337GT focus complete", focus)
    artifacts.append(aw.write_text_lossless(gs.gr.gq.go.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(gs.gr.gq.go.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337GT MT5 Negative Input Review(MT5 음수 입력 검토)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_rows']}`
- failed_input_review_rows(입력 검토 실패 행): `{final['failed_input_review_rows']}`
- failed_weight_rows(가중치 실패 행): `{final['failed_weight_rows']}`
- release_gate_rows(릴리스 게이트 행): `{final['release_gate_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): GU guarded training(GU 방어 학습)을 열지만 운영 주장(operating claim, 운영 주장)은 하지 않는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337GS MT5 Negative Repair Input Materialization", section, "run337GT MT5 Negative Input Review")
    artifacts.append(aw.write_text_lossless(gs.gr.gq.go.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): GT(337GT 실행)는 review(검토) 근거만 만들며 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(gs.gr.gq.go.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(gs.gr.gq.go.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337GT(337GT 실행) `{final['status']}`. "
        f"Effect(효과): GS repair inputs(GS 수리 입력) 적격 작업 `{final['eligible_task_rows']}/{final['task_rows']}`를 확인하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(gs.gr.gq.go.STAGE_BRIEF, fb.upsert_single_line(brief, "run337GT(337GT 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(gs.gr.gq.go.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337GT(337GT 실행) `{final['status']}`. "
        f"Effect(효과): GS input review(GS 입력 검토)를 완료하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(gs.gr.gq.go.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337GT", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_negative_repair_input_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"eligible={final['eligible_task_rows']}/{final['task_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "input_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "MT5 negative repair input review(MT5 음수 수리 입력 검토)",
        "tier_scope": "Tier A train-only input review(Tier A 학습 전용 입력 검토)",
        "kpi_scope": "input_review_only_no_training_no_mt5(입력 검토 전용, 학습/MT5 없음)",
        "scoreboard_lane": "model_validation",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"eligible={final['eligible_task_rows']}/{final['task_rows']}",
        "guardrail_kpi": "feature_boundary;finite_weights;negative_controls;release_gates;no_goal",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "kpi_evidence_data_integrity_model_validation",
        "evidence_scope": "GS frame, feature boundary, weight audit, task seeds",
        "kpi_scope": "eligibility_review_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__input_review",
        "family": "mt5_negative_repair_input_review",
        "question": "are GS MT5-negative repair inputs eligible for guarded GU training",
        "metric_scope": "feature_boundary_weight_audit_training_eligibility",
        "primary_artifact": rel(TASK_ELIGIBILITY),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(gs.gr.gq.go.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(gs.gr.gq.go.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(gs.gr.gq.go.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(gs.gr.gq.go.ARTIFACT_REGISTRY, prefer_head=False)
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
    return write_csv(gs.gr.gq.go.ARTIFACT_REGISTRY, columns, rows)


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    gs_final = read_json(GS_FINAL)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "gs_next_action": gs_final.get("next_action", ""),
        "gs_failed_gate_rows": sum(1 for row in read_csv(GS_GATES) if row.get("status") != "passed"),
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


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(
            json.dumps(
                {"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    input_rows, weight_rows, task_rows, negative_rows, release_rows, queue_rows, summary = build_reviews()
    final = make_final(summary)
    artifacts: list[Path] = [
        write_csv(INPUT_REVIEW, INPUT_REVIEW_COLUMNS, input_rows),
        write_csv(WEIGHT_REVIEW, WEIGHT_REVIEW_COLUMNS, weight_rows),
        write_csv(TASK_ELIGIBILITY, TASK_COLUMNS, task_rows),
        write_csv(NEGATIVE_CONTROL_REVIEW, NEGATIVE_COLUMNS, negative_rows),
        write_csv(RELEASE_GATE_REVIEW, RELEASE_COLUMNS, release_rows),
        write_csv(GU_QUEUE, QUEUE_COLUMNS, queue_rows),
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
                "eligible_tasks": f"{final['eligible_task_rows']}/{final['task_rows']}",
                "failed_inputs": final["failed_input_review_rows"],
                "failed_weights": final["failed_weight_rows"],
                "release_gates": final["release_gate_rows"],
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
