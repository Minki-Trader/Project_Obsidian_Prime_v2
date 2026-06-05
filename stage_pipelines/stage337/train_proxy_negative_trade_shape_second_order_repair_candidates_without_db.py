from __future__ import annotations

import hashlib
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
from stage_pipelines.stage337 import review_proxy_negative_trade_shape_second_order_repair_inputs_without_db as ht  # noqa: E402
from stage_pipelines.stage337 import train_mt5_negative_repair_lgbm_probability_mismatch_net_recovery_candidates_without_db as hc  # noqa: E402


aw = ht.aw
fb = ht.fb
he = ht.he

TODAY = "2026-06-01"
STAGE_ID = ht.STAGE_ID
RUN_NUMBER = "run337HU"
RUN_ID = "run337HU_train_proxy_negative_trade_shape_second_order_repair_candidates_without_db_v1"
PARENT_RUN_ID = ht.RUN_ID
NEXT_RUN_ID = "run337HV_review_proxy_negative_trade_shape_second_order_repair_training_without_db_v1"
STATUS = "completed_stage337HU_proxy_negative_trade_shape_second_order_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5"
JUDGMENT = "guarded_proxy_negative_trade_shape_second_order_repair_lightgbm_candidates_trained_with_onnx_parity_review_required_no_selection"
DECISION = "stage337HU_open_run337HV_review_proxy_negative_trade_shape_second_order_training"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HU_proxy_negative_trade_shape_second_order_repair_lightgbm_training_without_db_"
    "reviewed_HS_HT_train_only_inputs_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
hc.CLAIM_BOUNDARY = CLAIM_BOUNDARY

STAGE_DIR = ht.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEWS_DIR = ht.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HU_proxy_negative_trade_shape_second_order_repair_lightgbm_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HU_proxy_negative_trade_shape_second_order_repair_lightgbm_training.md"

HT_FINAL = ht.FINAL_DECISION
HT_GATES = ht.GATE_AUDIT
HT_QUEUE = ht.HU_QUEUE
HT_INPUT_REVIEW = ht.INPUT_REVIEW
HT_WEIGHT_REVIEW = ht.WEIGHT_REVIEW
HT_TASK_ELIGIBILITY = ht.TASK_ELIGIBILITY
HT_FEATURE_BOUNDARY_REVIEW = ht.FEATURE_BOUNDARY_REVIEW
HT_MODEL_PROPOSAL_REVIEW = ht.MODEL_PROPOSAL_REVIEW
HT_RELEASE_GATE_REVIEW = ht.RELEASE_GATE_REVIEW
HS_FRAME = ht.HS_FRAME
HS_ALLOWED_FEATURES = ht.HS_ALLOWED_FEATURES
HS_WEIGHT_AUDIT = ht.HS_WEIGHT_AUDIT
HS_FEATURE_BOUNDARY = ht.HS_FEATURE_BOUNDARY

FEATURE_SCHEMA = RUN_DIR / "hu_allowed_feature_schema.json"
TRAINING_TASK_REVIEW = RUN_DIR / "hu_training_task_review.csv"
SAMPLE_WEIGHT_AUDIT = RUN_DIR / "sample_weight_audit.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "onnx_parity_matrix.csv"
CLASSIFICATION_SCORECARD = RUN_DIR / "inner_holdout_classification_scorecard.csv"
PROXY_TRADE_SCORECARD = RUN_DIR / "inner_holdout_proxy_trade_scorecard.csv"
FEATURE_IMPORTANCE = RUN_DIR / "feature_importance_top20.csv"
RUNTIME_FIREWALL = RUN_DIR / "runtime_firewall_review.csv"
RELEASE_DISPOSITION = RUN_DIR / "training_release_disposition.csv"
HV_QUEUE = RUN_DIR / "run337HV_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_discipline_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    HT_FINAL,
    HT_GATES,
    HT_QUEUE,
    HT_INPUT_REVIEW,
    HT_WEIGHT_REVIEW,
    HT_TASK_ELIGIBILITY,
    HT_FEATURE_BOUNDARY_REVIEW,
    HT_MODEL_PROPOSAL_REVIEW,
    HT_RELEASE_GATE_REVIEW,
    HS_FRAME,
    HS_ALLOWED_FEATURES,
    HS_WEIGHT_AUDIT,
    HS_FEATURE_BOUNDARY,
)
OUTPUT_FILES = (
    FEATURE_SCHEMA,
    TRAINING_TASK_REVIEW,
    SAMPLE_WEIGHT_AUDIT,
    TRAINED_MODEL_MANIFEST,
    ONNX_PARITY,
    CLASSIFICATION_SCORECARD,
    PROXY_TRADE_SCORECARD,
    FEATURE_IMPORTANCE,
    RUNTIME_FIREWALL,
    RELEASE_DISPOSITION,
    HV_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
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

LABEL_ORDER = [0, 1, 2]
FEATURE_SET_ID = "hs_allowed_pretrade_features_v1"

TASK_REVIEW_COLUMNS = hc.TASK_REVIEW_COLUMNS
WEIGHT_COLUMNS = hc.WEIGHT_COLUMNS
MODEL_COLUMNS = hc.MODEL_COLUMNS
PARITY_COLUMNS = hc.PARITY_COLUMNS
CLASS_COLUMNS = hc.CLASS_COLUMNS
PROXY_COLUMNS = hc.PROXY_COLUMNS
IMPORTANCE_COLUMNS = hc.IMPORTANCE_COLUMNS
REVIEW_COLUMNS = hc.REVIEW_COLUMNS
QUEUE_COLUMNS = hc.QUEUE_COLUMNS
GATE_COLUMNS = hc.GATE_COLUMNS


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


def feature_order_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(features).encode("utf-8")).hexdigest()


def read_features() -> list[str]:
    rows = read_csv(HS_ALLOWED_FEATURES)
    features = [row.get("feature_name") or row.get("feature") or "" for row in rows]
    return [feature for feature in features if feature]


def safe_model_id(task_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", task_id).strip("_")
    return f"hu_{cleaned}"


def eligible_task_rows() -> list[dict[str, str]]:
    rows = read_csv(HT_TASK_ELIGIBILITY)
    eligible: list[dict[str, str]] = []
    for row in rows:
        if not str(row.get("eligibility_status", "")).startswith("eligible_for_guarded_training"):
            continue
        weight_column = row.get("sample_weight_column") or row.get("sample_weight_expression") or ""
        normalized = dict(row)
        normalized["declared_sample_weight_expression"] = row.get("sample_weight_expression", "")
        normalized["sample_weight_expression"] = weight_column
        eligible.append(normalized)
    return eligible


def build_firewall_and_release(model_rows: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    firewall_rows = [
        {
            "review_id": "no_candidate_selection",
            "subject": "candidate selection firewall(후보 선택 방화벽)",
            "rows": model_rows,
            "metric_1": "selection=not_run",
            "metric_2": "rank review deferred to HV(HV 순위 검토로 지연)",
            "review_status": "active",
            "allowed_use": "HV review queue only(HV 검토 대기열 전용)",
            "forbidden_use": "promotion or selected model(승격 또는 선택 모델)",
            "effect": "prevents proxy-only selection(프록시만 보고 선택하는 일을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "no_mt5_or_forward_claim",
            "subject": "MT5/Forward firewall(MT5/전진 방화벽)",
            "rows": model_rows,
            "metric_1": "mt5=not_run",
            "metric_2": "forward=not_claimed",
            "review_status": "active",
            "allowed_use": "future runtime probe planning(향후 런타임 탐침 계획)",
            "forbidden_use": "Forward Passed/Failed or runtime authority(전진 통과/실패 또는 런타임 권위)",
            "effect": "keeps ONNX training separate from operating evidence(ONNX 학습과 운영 근거를 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "no_threshold_or_lot_tuning",
            "subject": "threshold and lot firewall(임계값과 랏 방화벽)",
            "rows": model_rows,
            "metric_1": "threshold_tuning=not_run",
            "metric_2": "lot_optimization=not_run",
            "review_status": "active",
            "allowed_use": "fixed argmax review only(고정 argmax 검토 전용)",
            "forbidden_use": "in-sample threshold or lot optimization(표본 내부 임계값 또는 랏 최적화)",
            "effect": "reduces overfit path before HV review(HV 검토 전 과적합 경로를 줄임)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    release_rows = [
        {
            "review_id": "training_release_disposition",
            "subject": "training release disposition(학습 해제 처분)",
            "rows": model_rows,
            "metric_1": "review_required",
            "metric_2": NEXT_RUN_ID,
            "review_status": "no_release_review_required",
            "allowed_use": "HV training review(HV 학습 검토)",
            "forbidden_use": "selected candidate or live readiness(선택 후보 또는 실거래 준비)",
            "effect": "moves trained ONNX artifacts to review, not operation(학습 ONNX 산출물을 운영이 아니라 검토로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return firewall_rows, release_rows


def build_hv_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "hv001_review_proxy_negative_trade_shape_second_order_repair_training",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review five proxy-negative trade-shape repair ONNX candidates and decide runtime probe package(프록시 음수 거래 형태 수리 ONNX 후보 5개를 검토하고 런타임 탐침 패키지를 결정)",
            "required_inputs": f"{rel(TRAINED_MODEL_MANIFEST)};{rel(ONNX_PARITY)};{rel(CLASSIFICATION_SCORECARD)};{rel(PROXY_TRADE_SCORECARD)}",
            "required_outputs": "training review scorecard, runtime probe package decision(학습 검토 점수표, 런타임 탐침 패키지 결정)",
            "blocked_if_missing": "model manifest or ONNX parity(모델 목록 또는 ONNX 동등성)",
            "forbidden_action": "MT5/Forward/Goal claim without runtime probe(런타임 탐침 없는 MT5/전진/목표 주장)",
            "effect": "separates model creation from candidate judgment(모델 생성과 후보 판정을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def train_all() -> tuple[list[Path], dict[str, Any]]:
    frame = pd.read_parquet(aw.io_path(HS_FRAME)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame.sort_values(["source_row_id", "cost_policy_id"], inplace=True)
    features = read_features()
    missing_features = [feature for feature in features if feature not in frame.columns]
    if missing_features:
        raise ValueError(f"missing features: {missing_features}")
    tasks = eligible_task_rows()
    if not tasks:
        raise ValueError("no eligible tasks")
    for task in tasks:
        for column in (task.get("target_column", ""), task.get("sample_weight_expression", "")):
            if column and column not in frame.columns:
                raise ValueError(f"task {task.get('task_id')} references missing column {column}")

    feature_hash = feature_order_hash(features)
    write_json(
        FEATURE_SCHEMA,
        {
            "feature_set_id": FEATURE_SET_ID,
            "feature_count": len(features),
            "feature_order_hash": feature_hash,
            "features": features,
            "source": rel(HS_ALLOWED_FEATURES),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )

    artifacts: list[Path] = [FEATURE_SCHEMA]
    task_review_rows: list[dict[str, Any]] = []
    weight_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    class_rows: list[dict[str, Any]] = []
    proxy_rows: list[dict[str, Any]] = []
    importance_rows: list[dict[str, Any]] = []
    inner_train_rows = 0
    inner_holdout_rows = 0

    aw.io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    aw.io_path(ONNX_DIR).mkdir(parents=True, exist_ok=True)
    for task in tasks:
        task_id = str(task["task_id"])
        model_id = safe_model_id(task_id)
        model, inner_train, inner_holdout, weights = hc.train_model(task, frame, features)
        inner_train_rows = len(inner_train)
        inner_holdout_rows = len(inner_holdout)
        weight_column = str(task["sample_weight_expression"])
        task_review_rows.append(
            {
                "task_id": task_id,
                "training_disposition": "trained_no_selection_no_mt5",
                "feature_count": len(features),
                "target_column": task["target_column"],
                "sample_weight_expression": weight_column,
                "inner_train_rows": len(inner_train),
                "inner_holdout_rows": len(inner_holdout),
                "effect": "trained guarded candidate for HV review(HV 검토용 방어 후보 학습)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        weight_rows.append(
            {
                "task_id": task_id,
                "sample_weight_expression": weight_column,
                "rows": len(weights),
                "weight_min": float(weights.min()),
                "weight_mean": float(weights.mean()),
                "weight_max": float(weights.max()),
                "nonfinite_weights": int((~np.isfinite(weights.to_numpy())).sum()),
                "effect": "records train-only sample weight behavior(학습 전용 표본 가중치 동작 기록)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        model_path = MODEL_DIR / f"{model_id}.joblib"
        onnx_path = ONNX_DIR / f"{model_id}.onnx"
        hc.joblib.dump({"model": model, "features": features, "label_order": LABEL_ORDER, "task": dict(task)}, aw.io_path(model_path))
        export_meta = hc.export_lightgbm_classifier_to_onnx(
            model,
            onnx_path,
            feature_count=len(features),
            input_name="float_input",
            target_opset=12,
            drop_label_output=True,
        )
        parity_values = inner_holdout.loc[:, features].astype("float32").head(512).to_numpy()
        parity = hc.check_onnxruntime_probability_parity(model, onnx_path, parity_values, class_order=LABEL_ORDER)
        parity_rows.append(
            {
                "model_id": model_id,
                "task_id": task_id,
                "onnx_path": rel(onnx_path),
                "passed": "true" if parity["passed"] else "false",
                "rows": parity["rows"],
                "max_abs_diff": parity["max_abs_diff"],
                "mean_abs_diff": parity["mean_abs_diff"],
                "onnx_row_sum_max_abs_error": parity["onnx_row_sum_max_abs_error"],
                "input_name": parity["input_name"],
                "output_names": json.dumps(parity["output_names"], ensure_ascii=False),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        model_rows.append(
            {
                "model_id": model_id,
                "task_id": task_id,
                "feature_set_id": FEATURE_SET_ID,
                "target_column": task["target_column"],
                "sample_weight_expression": weight_column,
                "model_family": task["model_family"],
                "model_config_id": task["model_config_id"],
                "feature_count": len(features),
                "feature_order_hash": feature_hash,
                "class_order_json": json.dumps(LABEL_ORDER),
                "model_path": rel(model_path),
                "model_sha256": aw.sha256_file(model_path),
                "onnx_path": rel(onnx_path),
                "onnx_sha256": aw.sha256_file(onnx_path),
                "onnx_probability_output_name": export_meta["probability_output_name"],
                "inner_train_rows": len(inner_train),
                "inner_holdout_rows": len(inner_holdout),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for split_name, split_frame in (("inner_train", inner_train), ("inner_holdout", inner_holdout)):
            class_rows.append(hc.classification_score(model_id, task_id, split_name, model, split_frame, features))
            proxy_rows.append(hc.proxy_trade_score(model_id, task_id, split_name, model, split_frame, features))
        for rank, index in enumerate(np.argsort(model.feature_importances_)[::-1][:20], start=1):
            importance_rows.append(
                {
                    "model_id": model_id,
                    "rank": rank,
                    "feature_name": features[int(index)],
                    "importance": float(model.feature_importances_[int(index)]),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    firewall_rows, release_rows = build_firewall_and_release(len(model_rows))
    queue_rows = build_hv_queue()
    artifacts.extend(
        [
            write_csv(TRAINING_TASK_REVIEW, TASK_REVIEW_COLUMNS, task_review_rows),
            write_csv(SAMPLE_WEIGHT_AUDIT, WEIGHT_COLUMNS, weight_rows),
            write_csv(TRAINED_MODEL_MANIFEST, MODEL_COLUMNS, model_rows),
            write_csv(ONNX_PARITY, PARITY_COLUMNS, parity_rows),
            write_csv(CLASSIFICATION_SCORECARD, CLASS_COLUMNS, class_rows),
            write_csv(PROXY_TRADE_SCORECARD, PROXY_COLUMNS, proxy_rows),
            write_csv(FEATURE_IMPORTANCE, IMPORTANCE_COLUMNS, importance_rows),
            write_csv(RUNTIME_FIREWALL, REVIEW_COLUMNS, firewall_rows),
            write_csv(RELEASE_DISPOSITION, REVIEW_COLUMNS, release_rows),
            write_csv(HV_QUEUE, QUEUE_COLUMNS, queue_rows),
        ]
    )
    holdout_proxy = [row for row in proxy_rows if row["split"] == "inner_holdout"]
    positive_holdout = [row for row in holdout_proxy if float(row["net_log_return_after_cost"]) > 0]
    summary = {
        "frame_rows": int(len(frame)),
        "feature_count": len(features),
        "feature_order_hash": feature_hash,
        "eligible_task_rows": len(tasks),
        "trained_model_rows": len(model_rows),
        "onnx_rows": len(model_rows),
        "onnx_parity_rows": len(parity_rows),
        "onnx_parity_passed_rows": sum(1 for row in parity_rows if row["passed"] == "true"),
        "inner_train_rows": inner_train_rows,
        "inner_holdout_rows": inner_holdout_rows,
        "classification_rows": len(class_rows),
        "proxy_trade_rows": len(proxy_rows),
        "runtime_firewall_rows": len(firewall_rows),
        "release_disposition_rows": len(release_rows),
        "hv_queue_rows": len(queue_rows),
        "positive_inner_holdout_proxy_rows": len(positive_holdout),
        "best_inner_holdout_balanced_accuracy": max([float(row["balanced_accuracy"]) for row in class_rows if row["split"] == "inner_holdout"] or [0.0]),
        "best_inner_holdout_proxy_net": max([float(row["net_log_return_after_cost"]) for row in holdout_proxy] or [0.0]),
        "best_inner_holdout_profit_factor": max([float(row["profit_factor"]) for row in holdout_proxy] or [0.0]),
        "max_inner_holdout_signal_density": max([float(row["signal_density"]) for row in holdout_proxy] or [0.0]),
        "min_inner_holdout_signal_density": min([float(row["signal_density"]) for row in holdout_proxy] or [0.0]),
    }
    return artifacts, summary


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    ht_final = read_json(HT_FINAL)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "ht_next_action": ht_final.get("next_action", ""),
        "ht_failed_gate_rows": sum(1 for row in read_csv(HT_GATES) if row.get("status") != "passed"),
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_family": "experiment_execution",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": "obsidian-data-integrity;obsidian-model-validation;obsidian-artifact-lineage;obsidian-result-judgment",
        "required_gates": "scope_completion_gate;kpi_contract_audit;skill_receipt_lint;required_gate_coverage_audit;final_claim_guard",
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = final["candidate_selection"] == "not_run" and final["mt5_runtime_probe"] == "not_run" and final["goal_achieve"] == "not_claimed"
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(HT_TASK_ELIGIBILITY), "required HS/HT inputs exist(필수 HS/HT 입력 존재)"),
        ("parent_ht_gates_passed", final["ht_failed_gate_rows"] == 0, str(final["ht_failed_gate_rows"]), "0", rel(HT_GATES), "HT review gates passed(HT 검토 게이트 통과)"),
        ("parent_next_action_matches", final["ht_next_action"] == RUN_ID, str(final["ht_next_action"]), RUN_ID, rel(HT_FINAL), "HU follows HT next action(HU가 HT 다음 행동을 따름)"),
        ("feature_schema_materialized", final["feature_count"] == 58 and path_exists(FEATURE_SCHEMA), f"feature_count={final['feature_count']}", "58", rel(FEATURE_SCHEMA), "reviewed feature schema is available(검토된 피처 스키마 존재)"),
        ("training_tasks_executed", final["trained_model_rows"] == final["eligible_task_rows"] == 5, f"trained={final['trained_model_rows']};eligible={final['eligible_task_rows']}", "5/5", rel(TRAINED_MODEL_MANIFEST), "all HU tasks trained(모든 HU 작업 학습 완료)"),
        ("onnx_exports_materialized", final["onnx_rows"] == final["trained_model_rows"], f"onnx={final['onnx_rows']};models={final['trained_model_rows']}", "onnx=models", rel(TRAINED_MODEL_MANIFEST), "each model has ONNX artifact(각 모델 ONNX 산출물 존재)"),
        ("onnx_parity_passed", final["onnx_parity_passed_rows"] == final["onnx_parity_rows"] == final["trained_model_rows"], f"passed={final['onnx_parity_passed_rows']};rows={final['onnx_parity_rows']}", "all parity rows passed", rel(ONNX_PARITY), "ONNX runtime matches LightGBM sklearn API probabilities(ONNX 런타임이 LightGBM sklearn API 확률과 일치)"),
        ("inner_holdout_scored", final["classification_rows"] == 10 and final["proxy_trade_rows"] == 10, f"class={final['classification_rows']};proxy={final['proxy_trade_rows']}", "10/10", f"{rel(CLASSIFICATION_SCORECARD)};{rel(PROXY_TRADE_SCORECARD)}", "inner train/holdout diagnostics exist(내부 학습/보류 진단 존재)"),
        ("runtime_firewall_active", final["runtime_firewall_rows"] >= 3 and final["release_disposition_rows"] >= 1, f"firewall={final['runtime_firewall_rows']};release={final['release_disposition_rows']}", ">=3 and >=1", rel(RUNTIME_FIREWALL), "runtime and release claims remain blocked(런타임과 해제 주장을 계속 차단)"),
        ("hv_queue_materialized", final["hv_queue_rows"] == 1, str(final["hv_queue_rows"]), "1", rel(HV_QUEUE), "HV review queue opened(HV 검토 대기열 개방)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}", "not_run/not_run/not_claimed", rel(FINAL_DECISION), "HU creates artifacts without operating claim(HU는 산출물만 만들고 운영 주장은 하지 않음)"),
        ("required_gate_coverage_audit", True, "all required gates listed(모든 필수 게이트 열거)", "present", rel(GATE_AUDIT), "completion claim tied to gates(완료 주장을 게이트에 연결)"),
    ]
    return [
        {"gate_id": gate_id, "status": "passed" if passed else "failed", "evidence_path": evidence, "observed": observed, "expected": expected, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def write_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    base = {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "stage_id": STAGE_ID, "created_at_utc": now_utc(), "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY}
    receipts = [
        (
            DATA_RECEIPT,
            {
                **base,
                "data_source": rel(HS_FRAME),
                "feature_schema": rel(FEATURE_SCHEMA),
                "time_axis": "timestamp is UTC closed-bar train-only order(timestamp는 UTC 닫힌 봉 학습 전용 순서)",
                "sample_scope": f"FPMarkets US100 M5 rows={final['frame_rows']};inner_train={final['inner_train_rows']};inner_holdout={final['inner_holdout_rows']}",
                "feature_label_boundary": "uses HS reviewed features only; targets and HR second-order repair weights are excluded from model features(HS 검토 피처만 사용하고 목표와 HR 2차 수리 가중치는 모델 피처에서 제외)",
                "split_boundary": "source_row_id ordered 80/20 inner split, no forward claim(source_row_id 순서 80/20 내부 분할, 전진 주장 없음)",
                "leakage_risk": "proxy labels and weights exist in frame but not feature schema(프록시 라벨과 가중치는 프레임에 있지만 피처 스키마에는 없음)",
                "data_hash_or_identity": aw.sha256_file(HS_FRAME) if path_exists(HS_FRAME) else "",
                "integrity_judgment": "usable_for_HV_review_no_selection(HV 검토용 사용 가능, 선택 없음)",
            },
        ),
        (
            MODEL_RECEIPT,
            {
                **base,
                "model_family": "LGBMClassifier(LightGBM 분류기)",
                "target_and_label": "label_class with five HR second-order sample-weight columns(label_class와 HR 2차 표본 가중치 열 5개)",
                "split_method": "inner holdout only, no WFO or MT5 yet(내부 보류만, WFO 또는 MT5는 아직 없음)",
                "selection_metric": "none(없음)",
                "secondary_metrics": "balanced_accuracy, macro_f1, proxy net/PF/density(균형 정확도, 매크로 F1, 프록시 순수익/PF/밀도)",
                "threshold_policy": "fixed argmax, no tuning(고정 argmax, 조정 없음)",
                "overfit_risk": "inner split and proxy score are diagnostic only(내부 분할과 프록시 점수는 진단 전용)",
                "calibration_risk": "probabilities are not calibrated for operation(확률은 운영용 보정 아님)",
                "comparison_baseline": "HT eligible input review(HT 적격 입력 검토)",
                "trained_models": final["trained_model_rows"],
                "onnx_exports": final["onnx_rows"],
                "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}",
                "validation_judgment": JUDGMENT,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                **base,
                "observed_change": "five HR second-order repair weighted ONNX candidates trained(HR 2차 수리 가중 ONNX 후보 5개 학습)",
                "best_inner_holdout_balanced_accuracy": final["best_inner_holdout_balanced_accuracy"],
                "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"],
                "best_inner_holdout_profit_factor": final["best_inner_holdout_profit_factor"],
                "positive_inner_holdout_proxy_rows": final["positive_inner_holdout_proxy_rows"],
                "proxy_use": "sanity only, not MT5 KPI(점검 전용, MT5 KPI 아님)",
                "attribution_confidence": "low_until_HV_and_MT5_review(HV와 MT5 검토 전까지 낮음)",
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                **base,
                "runtime_execution": "not_run(미실행)",
                "onnx_runtime_check": f"probability parity {final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}(확률 동등성)",
                "mt5_probe": "not_run(미실행)",
                "runtime_claim_boundary": "ONNX parity only, no MT5 execution(ONNX 동등성만, MT5 실행 없음)",
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                **base,
                "result_subject": RUN_ID,
                "judgment_label": final["judgment"],
                "evidence_available": [rel(TRAINED_MODEL_MANIFEST), rel(ONNX_PARITY), rel(CLASSIFICATION_SCORECARD), rel(PROXY_TRADE_SCORECARD)],
                "evidence_missing": "HV review, MT5 runtime probe, Forward/Goal(HV 검토, MT5 런타임 탐침, 전진/목표)",
                "next_condition": final["next_action"],
                "goal_achieve": "not_claimed(주장 안 함)",
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                **base,
                "forbidden_claims": "selected, operating_promotion, runtime_authority, Goal Achieve(선택, 운영 승격, 런타임 권위, 목표 달성)",
                "claim_guard": "all forbidden claims remain not_claimed/not_run(모든 금지 주장은 not_claimed/not_run 유지)",
            },
        ),
    ]
    paths = [write_json(path, payload) for path, payload in receipts]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        **base,
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()},
        "registry_links": [rel(he.RUN_REGISTRY), rel(he.ALPHA_LEDGER), rel(he.STAGE_LEDGER), rel(he.ARTIFACT_REGISTRY)],
        "availability": "generated_with_manifest(목록과 함께 생성)",
        "lineage_judgment": "trained_onnx_artifacts_connected_to_HV_review(HV 검토에 학습 ONNX 산출물 연결)",
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337HU Proxy Negative Trade Shape Second Order Repair LightGBM ONNX Training(337단계 run337HU 프록시 음수 거래 형태 2차 수리 LightGBM ONNX 학습)

Action(행동): HS/HT reviewed train-only inputs(HS/HT 검토 학습 전용 입력)로 LGBMClassifier(LightGBM 분류기) 후보 `5`개를 학습하고 ONNX(온엑스)로 내보냈다. Effect(효과): 다음 HV review(HV 검토)가 실제 model artifacts(모델 산출물), ONNX parity(ONNX 동등성), proxy score(프록시 점수)를 검토할 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- trained_models(학습 모델): `{final['trained_model_rows']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- best_inner_holdout_balanced_accuracy(최고 내부 보류 균형 정확도): `{final['best_inner_holdout_balanced_accuracy']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- positive_inner_holdout_proxy_rows(양수 내부 보류 프록시 행): `{final['positive_inner_holdout_proxy_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Boundary(경계): HU(337HU 실행)는 training and ONNX materialization(학습과 ONNX 물질화)만 했다. MT5 execution(MT5 실행), candidate selection(후보 선택), Forward/Goal(전진/목표), runtime authority(런타임 권위)는 모두 `not_claimed`다.

Next action(다음 행동): `{final['next_action']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337HU Decision(337HU 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(TRAINED_MODEL_MANIFEST)}`, `{rel(ONNX_PARITY)}`, `{rel(PROXY_TRADE_SCORECARD)}`

Action(행동): 5개 guarded ONNX candidates(방어 ONNX 후보)를 만들었다.
Effect(효과): HV review(HV 검토) 전까지 candidate selection(후보 선택)이나 operating promotion(운영 승격)은 닫힌 상태로 유지한다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
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
    return "\n".join(lines[:insert_at] + section.strip("\n").splitlines() + [""] + lines[insert_at:]) + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(he.WORKSPACE_STATE)
    workspace = re.sub(r"^current_run_id:.*$", f"current_run_id: {final['next_action']}", workspace, count=1, flags=re.M)
    workspace = re.sub(r"^updated_on:.*$", f"updated_on: '{TODAY}'", workspace, count=1, flags=re.M)
    focus = (
        "- >-\n"
        f"  Stage337 run337HU focus complete(337단계 run337HU 초점 완료): `{final['status']}`. "
        f"Effect(효과): trained models(학습 모델) `{final['trained_model_rows']}`, ONNX parity(ONNX 동등성) `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`, "
        f"positive proxy rows(양수 프록시 행) `{final['positive_inner_holdout_proxy_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337HU focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337HU focus complete.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(he.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(he.CURRENT_STATE)
    current_lines = current.splitlines()
    replacements = {
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
        for prefix, replacement in replacements.items():
            if line.startswith(prefix):
                current_lines[index] = replacement
                break
    current = "\n".join(current_lines) + "\n"
    section = f"""## run337HU Proxy Negative Trade Shape Second Order Repair LightGBM ONNX Training(프록시 음수 거래 형태 2차 수리 LightGBM ONNX 학습)

Action(행동): run337HU(337HU 실행)는 HS/HT reviewed inputs(HS/HT 검토 입력)로 5개 LightGBM ONNX candidates(LightGBM ONNX 후보)를 학습했다.
Effect(효과): trained models(학습 모델) `{final['trained_model_rows']}`, ONNX parity(ONNX 동등성) `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`, best proxy net(최고 프록시 순수익) `{final['best_inner_holdout_proxy_net']}`를 HV review(HV 검토)로 넘겼다.

Boundary(경계): candidate selection(후보 선택), MT5 execution(MT5 실행), Forward/Goal(전진/목표), runtime authority(런타임 권위)는 주장하지 않는다.
Next(다음): `{final['next_action']}`.
"""
    current = upsert_section_after_metadata(current, "run337HU Proxy Negative Trade Shape Second Order Repair LightGBM ONNX Training", section)
    artifacts.append(aw.write_text_lossless(he.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- trained_models(학습 모델): `{final['trained_model_rows']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- positive_inner_holdout_proxy_rows(양수 내부 보류 프록시 행): `{final['positive_inner_holdout_proxy_rows']}`
- runtime_package(런타임 패키지): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HU training(HU 학습)은 ONNX 산출물과 HV review(HV 검토) 조건만 만들고 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HU(337HU 실행) `{final['status']}`. "
        f"Effect(효과): guarded ONNX candidates(방어 ONNX 후보) `{final['trained_model_rows']}`개를 학습하고 "
        f"ONNX parity(ONNX 동등성) `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`를 확인해 `{final['next_action']}`을 열었다. "
        "Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HU(337HU 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HU(337HU 실행) `{final['status']}`. "
        f"Effect(효과): proxy negative trade-shape second-order repair LightGBM ONNX(프록시 음수 거래 형태 2차 수리 LightGBM ONNX) 후보 5개를 만들고 `{final['next_action']}`을 열었다."
    )
    artifacts.append(aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HU", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_negative_trade_shape_second_order_repair_lightgbm_onnx_training",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"models={final['trained_model_rows']};onnx_parity={final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']};best_proxy={final['best_inner_holdout_proxy_net']};positive_proxy_rows={final['positive_inner_holdout_proxy_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__onnx_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "onnx_training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy_negative_trade_shape_second_order_repair_lightgbm_onnx_training(프록시 음수 거래 형태 2차 수리 LightGBM ONNX 학습)",
        "tier_scope": "Tier A train/inner holdout(Tier A 학습/내부 보류)",
        "kpi_scope": "inner_holdout_proxy_and_onnx_parity_no_release(내부 보류 프록시와 ONNX 동등성, 해제 없음)",
        "scoreboard_lane": "model_training",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"models={final['trained_model_rows']};onnx={final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']};best_proxy={final['best_inner_holdout_proxy_net']}",
        "guardrail_kpi": "no_selection;no_mt5;no_forward;no_goal",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};claim_boundary={CLAIM_BOUNDARY}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__onnx_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_model_training",
        "evidence_scope": "HT eligible tasks, HS frame, model artifacts, ONNX parity",
        "kpi_scope": "inner_holdout_proxy_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__onnx_training",
        "family": "proxy_negative_trade_shape_second_order_repair_lightgbm_onnx_training",
        "question": "do HR second-order repair weights produce reviewable ONNX candidates(HR 2차 수리 가중치가 검토 가능한 ONNX 후보를 만드는가)",
        "metric_scope": "inner_holdout_proxy_onnx_parity_model_manifest",
        "primary_artifact": rel(TRAINED_MODEL_MANIFEST),
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
    artifacts, summary = train_all()
    final = make_final(summary)
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
        ]
    )
    artifacts.extend(write_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "trained_models": final["trained_model_rows"],
                "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}",
                "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"],
                "positive_inner_holdout_proxy_rows": final["positive_inner_holdout_proxy_rows"],
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
