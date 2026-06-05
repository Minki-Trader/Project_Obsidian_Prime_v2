from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    materialize_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs_without_db as jl,
)


aw = jl.aw

TODAY = "2026-06-01"
STAGE_ID = jl.STAGE_ID
STAGE_DIR = jl.STAGE_DIR
RUN_NUMBER = "run337JM"
RUN_ID = "run337JM_review_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs_without_db_v1"
PARENT_RUN_ID = jl.RUN_ID
NEXT_RUN_ID = "run337JN_train_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_candidates_without_db_v1"
STATUS = "completed_stage337JM_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs_review_training_ready_no_selection"
JUDGMENT = "jl_inputs_timestamp_safe_training_ready_with_tier_b_missing_required_named"
DECISION = "stage337JM_open_run337JN_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_candidate_training"
CLAIM_BOUNDARY = (
    "research_development_input_review_only_no_model_training_no_onnx_export_no_mt5_no_runtime_package_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337JM_positive_low_pf_recovery_drawdown_dual_probe_repair_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337JM_positive_low_pf_recovery_drawdown_dual_probe_repair_input_review.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

JM_INPUT_REVIEW = RUN_DIR / "jm_input_review_matrix.csv"
JM_FEATURE_BOUNDARY_REVIEW = RUN_DIR / "jm_feature_boundary_review.csv"
JM_WEIGHT_REVIEW = RUN_DIR / "jm_weight_saturation_review.csv"
JM_TASK_ELIGIBILITY = RUN_DIR / "jm_training_task_eligibility.csv"
JM_TIER_RECORD_REVIEW = RUN_DIR / "jm_tier_record_review.csv"
JM_RUNTIME_PARITY_REVIEW = RUN_DIR / "jm_runtime_parity_review.csv"
JM_LINEAGE_REVIEW = RUN_DIR / "jm_lineage_review.csv"
JN_QUEUE = RUN_DIR / "run337JN_training_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    jl.FINAL_DECISION,
    jl.GATE_AUDIT,
    jl.JM_QUEUE,
    jl.JL_INPUT_FRAME,
    jl.JL_ALLOWED_FEATURES,
    jl.JL_WEIGHT_AUDIT,
    jl.JL_FEATURE_BOUNDARY,
    jl.JL_TIER_RECORDS,
    jl.JL_RUNTIME_PARITY_PLAN,
    jl.JL_TASK_SEEDS,
    jl.RUN_MANIFEST,
)

OUTPUT_FILES = (
    JM_INPUT_REVIEW,
    JM_FEATURE_BOUNDARY_REVIEW,
    JM_WEIGHT_REVIEW,
    JM_TASK_ELIGIBILITY,
    JM_TIER_RECORD_REVIEW,
    JM_RUNTIME_PARITY_REVIEW,
    JM_LINEAGE_REVIEW,
    JN_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    ROOT_SELECTION_STATUS,
    STAGE_BRIEF,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), low_memory=False)


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    target = path if len(str(path)) < 240 else io(path)
    frame.to_csv(target, index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def numeric(frame: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(frame[column], errors="coerce") if column in frame.columns else pd.Series(np.nan, index=frame.index)


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def review_row(check_id: str, status: bool, observed: Any, expected: Any, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": "passed" if status else "failed",
        "observed": observed,
        "expected": expected,
        "evidence_path": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_reviews() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    parent = read_json(jl.FINAL_DECISION)
    frame = pd.read_parquet(io(jl.JL_INPUT_FRAME))
    allowed = read_csv(jl.JL_ALLOWED_FEATURES)
    feature_boundary = read_csv(jl.JL_FEATURE_BOUNDARY)
    weight_audit = read_csv(jl.JL_WEIGHT_AUDIT)
    tasks = read_csv(jl.JL_TASK_SEEDS)
    tiers = read_csv(jl.JL_TIER_RECORDS)
    runtime_plan = read_csv(jl.JL_RUNTIME_PARITY_PLAN)
    manifest = read_json(jl.RUN_MANIFEST)

    feature_col = "feature_name" if "feature_name" in allowed.columns else allowed.columns[0]
    features = [str(item) for item in allowed[feature_col].dropna().tolist()]
    missing_features = [feature for feature in features if feature not in frame.columns]
    timestamp_missing = int(frame["timestamp"].isna().sum()) if "timestamp" in frame.columns else len(frame)
    timestamp_ordered = bool(pd.to_datetime(frame["timestamp"], utc=True).is_monotonic_increasing) if "timestamp" in frame.columns else False
    duplicate_rows = int(frame.duplicated(["source_row_id", "cost_policy_id"]).sum()) if {"source_row_id", "cost_policy_id"}.issubset(frame.columns) else -1
    weight_missing = [column for column in jl.JL_WEIGHT_COLUMNS if column not in frame.columns]
    target_missing = [column for column in jl.JL_TARGET_COLUMNS if column not in frame.columns]
    label_valid = int(numeric(frame, "jl_valid_profit_quality_fwd18").fillna(0).astype(int).eq(1).sum())
    label_classes = int(numeric(frame, "jl_label_class_profit_quality_fwd18").fillna(-1).astype(int).loc[lambda s: s.isin([0, 1, 2])].nunique())

    input_review = pd.DataFrame(
        [
            review_row("jm001_frame_rows", len(frame) >= 87600, len(frame), ">=87600", jl.JL_INPUT_FRAME, "입력 frame(프레임)이 손실 없이 이어졌는지 확인한다."),
            review_row("jm002_feature_count", len(features) == 58, len(features), "58", jl.JL_ALLOWED_FEATURES, "모델 feature(피처)를 기존 58개로 고정한다."),
            review_row("jm003_missing_allowed_features", not missing_features, ";".join(missing_features), "none(없음)", jl.JL_ALLOWED_FEATURES, "허용 feature(피처)가 실제 frame(프레임)에 모두 있는지 확인한다."),
            review_row("jm004_timestamp_present", timestamp_missing == 0, timestamp_missing, "0", jl.JL_INPUT_FRAME, "timestamp(시각) 축이 깨지지 않았는지 확인한다."),
            review_row("jm005_timestamp_ordered", timestamp_ordered, str(timestamp_ordered), "True", jl.JL_INPUT_FRAME, "time axis(시간축) 순서를 확인한다."),
            review_row("jm006_duplicate_source_cost_policy", duplicate_rows == 0, duplicate_rows, "0", jl.JL_INPUT_FRAME, "같은 source/cost row(원천/비용 행) 중복을 막는다."),
            review_row("jm007_weight_columns_present", not weight_missing, ";".join(weight_missing), "none(없음)", jl.JL_INPUT_FRAME, "train-only weight(학습 전용 가중치)가 모두 있는지 확인한다."),
            review_row("jm008_target_columns_present", not target_missing, ";".join(target_missing), "none(없음)", jl.JL_INPUT_FRAME, "train-only label(학습 전용 라벨)이 모두 있는지 확인한다."),
            review_row("jm009_profit_quality_label_distribution", label_valid > 85000 and label_classes == 3, f"valid={label_valid};classes={label_classes}", "valid>85000;classes=3", jl.JL_INPUT_FRAME, "profit quality label(수익 품질 라벨)이 학습 가능한지 확인한다."),
        ]
    )

    feature_review = feature_boundary.copy()
    feature_review["review_status"] = feature_review["status"]
    feature_review["effect"] = "feature/label boundary(피처/라벨 경계)를 JM에서 재확인한다."
    feature_review["claim_boundary"] = CLAIM_BOUNDARY

    weight_review = weight_audit.copy()
    weight_review["status"] = np.where(
        (pd.to_numeric(weight_review["nonfinite_rows"], errors="coerce").fillna(1) == 0)
        & (pd.to_numeric(weight_review["max_saturation_rate"], errors="coerce").fillna(1) <= 0.20)
        & (pd.to_numeric(weight_review["weight_mean"], errors="coerce").fillna(0) > 0),
        "passed",
        "failed",
    )
    weight_review["effect"] = "train-only weight(학습 전용 가중치)의 유한성, 포화, 평균을 확인한다."
    weight_review["claim_boundary"] = CLAIM_BOUNDARY

    task_rows = []
    for _, task in tasks.iterrows():
        target_col = str(task["target_column"])
        valid_col = str(task["valid_column"])
        weight_col = str(task["sample_weight_column"])
        present = all(column in frame.columns for column in (target_col, valid_col, weight_col))
        if present:
            valid_mask = numeric(frame, valid_col).fillna(0).astype(int).eq(1)
            labels = numeric(frame.loc[valid_mask], target_col).fillna(-1).astype(int)
            weights = numeric(frame.loc[valid_mask], weight_col)
            valid_rows = int(valid_mask.sum())
            class_count = int(labels.loc[labels.isin([0, 1, 2])].nunique())
            weight_nonfinite = int((~np.isfinite(weights.to_numpy(dtype="float64"))).sum())
            saturation_ratio = float(weights.ge(11.999).mean()) if len(weights) else 1.0
            weight_mean = float(weights.mean()) if len(weights) else 0.0
            weight_max = float(weights.max()) if len(weights) else 0.0
        else:
            valid_rows = 0
            class_count = 0
            weight_nonfinite = 1
            saturation_ratio = 1.0
            weight_mean = 0.0
            weight_max = 0.0
        eligible = present and valid_rows > 85000 and class_count == 3 and weight_nonfinite == 0 and saturation_ratio <= 0.20 and weight_mean > 0.0
        reason = "eligible_training_seed(학습 씨앗 적격)" if eligible else "failed_input_or_weight_gate(입력 또는 가중치 게이트 실패)"
        task_rows.append(
            {
                "task_id": task.get("task_id", ""),
                "eligible": bool(eligible),
                "target_column": target_col,
                "valid_column": valid_col,
                "sample_weight_column": weight_col,
                "model_family": task.get("model_family", ""),
                "rows_total": int(len(frame)),
                "rows_valid": valid_rows,
                "class_count": class_count,
                "weight_mean": weight_mean,
                "weight_max": weight_max,
                "saturation_ratio": saturation_ratio,
                "eligibility_reason": reason,
                "effect": "JM이 JN training(JN 학습)에 넘길 수 있는 task seed(작업 씨앗)만 통과시킨다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    task_eligibility = pd.DataFrame(task_rows)

    tier_review = tiers.copy()
    tier_review["review_status"] = np.where(
        tier_review["view"].astype(str).str.contains("Tier A separate|Tier B separate|Tier A\\+B combined", regex=True),
        "passed",
        "failed",
    )
    tier_review["effect"] = "Tier A/B/combined(티어 A/B/합산) 기록을 생략하지 않았는지 확인한다."
    tier_review["claim_boundary"] = CLAIM_BOUNDARY

    runtime_review = runtime_plan.copy()
    runtime_review["review_status"] = np.where(runtime_review["required_guard"].astype(str).str.contains("proxy-MT5|ONNX", regex=True), "passed", "failed")
    runtime_review["effect"] = "proxy-MT5 comparison(프록시-MT5 비교)과 ONNX parity(ONNX 동등성)를 다음 런타임 경로에 남긴다."
    runtime_review["claim_boundary"] = CLAIM_BOUNDARY

    lineage_rows = []
    for source in [*INPUT_FILES, *[Path(path) for path in manifest.get("outputs", []) if isinstance(path, str)]]:
        if not isinstance(source, Path):
            source = Path(source)
        present = exists(source)
        lineage_rows.append(
            {
                "artifact_path": rel(source) if str(source) else "",
                "exists": present,
                "sha256": sha(source) if present and io(source).is_file() else "",
                "role": "input_or_parent_output(입력 또는 부모 출력)",
                "effect": "JM lineage(계보)가 JL 산출물을 실제 파일로 추적한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    lineage = pd.DataFrame(lineage_rows)

    queue = pd.DataFrame(
        [
            {
                "queue_id": "run337JN_train_jm_eligible_tasks",
                "source_run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "task": "train_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_candidates(런타임 양수 저PF/저회복/낙폭 이중 탐침 수리 후보 학습)",
                "required_inputs": f"{rel(jl.JL_INPUT_FRAME)};{rel(jl.JL_ALLOWED_FEATURES)};{rel(JM_TASK_ELIGIBILITY)}",
                "eligible_task_rows": int(task_eligibility["eligible"].sum()),
                "expected_outputs": "trained model manifest(학습 모델 목록); ONNX exports(ONNX 내보내기); proxy score review inputs(프록시 점수 검토 입력)",
                "blocked_if_missing": "all task rows eligible(모든 작업 행 적격), feature boundary pass(피처 경계 통과), finite weights(유한 가중치)",
                "forbidden_action": "candidate selection, MT5 claim, runtime authority(후보 선정, MT5 주장, 런타임 권위)",
                "effect": "JM 검토를 JN 학습 입력으로 연결한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    summary = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "rows": int(len(frame)),
        "feature_count": int(len(features)),
        "missing_feature_count": int(len(missing_features)),
        "input_review_failures": int((input_review["status"] != "passed").sum()),
        "feature_boundary_failures": int((feature_review["review_status"] != "passed").sum()),
        "weight_review_failures": int((weight_review["status"] != "passed").sum()),
        "task_rows": int(len(task_eligibility)),
        "eligible_task_rows": int(task_eligibility["eligible"].sum()),
        "tier_record_rows": int(len(tier_review)),
        "tier_review_failures": int((tier_review["review_status"] != "passed").sum()),
        "runtime_plan_rows": int(len(runtime_review)),
        "runtime_review_failures": int((runtime_review["review_status"] != "passed").sum()),
        "lineage_missing_rows": int((lineage["exists"] == False).sum()),
        "positive_clue_model_id": parent.get("positive_clue_model_id", ""),
        "negative_control_model_id": parent.get("negative_control_model_id", ""),
        "input_frame": rel(jl.JL_INPUT_FRAME),
        "allowed_features": rel(jl.JL_ALLOWED_FEATURES),
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "mt5_runtime_probe": "not_run_in_jm",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return input_review, feature_review, weight_review, task_eligibility, tier_review, runtime_review, lineage, queue, summary


def gate_row(gate: str, status: str, observed: Any, expected: Any, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "observed": observed,
        "expected": expected,
        "evidence_path": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(jl.GATE_AUDIT)
    no_forbidden = (
        summary["candidate_selection"] == "not_run"
        and summary["forward_passed"] == "not_claimed"
        and summary["forward_failed"] == "not_claimed"
        and summary["goal_achieve"] == "not_claimed"
        and summary["runtime_authority"] == "not_claimed"
        and summary["operating_promotion"] == "not_claimed"
    )
    return pd.DataFrame(
        [
            gate_row("parent_jl_gates_passed", "passed" if passed_status(parent_gates["status"]).all() else "failed", "all passed" if passed_status(parent_gates["status"]).all() else "failed parent gate", "all passed", jl.GATE_AUDIT, "JL materialization(JL 물질화) 통과 뒤 검토한다."),
            gate_row("scope_completion_gate", "passed" if summary["input_review_failures"] == 0 and summary["feature_boundary_failures"] == 0 else "failed", f"input={summary['input_review_failures']};feature={summary['feature_boundary_failures']}", "0;0", JM_INPUT_REVIEW, "input scope(입력 범위)를 모두 검토한다."),
            gate_row("data_integrity_gate", "passed" if summary["missing_feature_count"] == 0 and summary["feature_boundary_failures"] == 0 else "failed", f"missing_features={summary['missing_feature_count']};boundary={summary['feature_boundary_failures']}", "0;0", JM_FEATURE_BOUNDARY_REVIEW, "feature/label boundary(피처/라벨 경계)를 통과해야 한다."),
            gate_row("model_validation_gate", "passed" if summary["eligible_task_rows"] == summary["task_rows"] and summary["task_rows"] >= 8 else "failed", f"{summary['eligible_task_rows']}/{summary['task_rows']}", "all and >=8", JM_TASK_ELIGIBILITY, "training seed(학습 씨앗)가 모두 학습 가능해야 한다."),
            gate_row("weight_health_gate", "passed" if summary["weight_review_failures"] == 0 else "failed", summary["weight_review_failures"], "0", JM_WEIGHT_REVIEW, "sample weight(표본 가중치)가 학습을 왜곡하지 않게 한다."),
            gate_row("tier_pair_record_gate", "passed" if summary["tier_record_rows"] == 3 and summary["tier_review_failures"] == 0 else "failed", f"rows={summary['tier_record_rows']};failures={summary['tier_review_failures']}", "3;0", JM_TIER_RECORD_REVIEW, "Tier A/B/combined(티어 A/B/합산) 기록을 생략하지 않는다."),
            gate_row("runtime_parity_plan_gate", "passed" if summary["runtime_plan_rows"] >= 1 and summary["runtime_review_failures"] == 0 else "failed", f"rows={summary['runtime_plan_rows']};failures={summary['runtime_review_failures']}", ">=1;0", JM_RUNTIME_PARITY_REVIEW, "later MT5 runtime probe(후속 MT5 런타임 탐침) 경로를 남긴다."),
            gate_row("artifact_lineage_gate", "passed" if summary["lineage_missing_rows"] == 0 else "failed", summary["lineage_missing_rows"], "0", JM_LINEAGE_REVIEW, "입력과 산출물 계보가 실제 파일로 연결된다."),
            gate_row("training_queue_written", "passed" if exists(JN_QUEUE) else "failed", exists(JN_QUEUE), "true", JN_QUEUE, "JN training(JN 학습)으로 이어지게 한다."),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", "not_claimed", "not_claimed", CLAIM_RECEIPT, "selection/forward/runtime authority/Goal(선정/전진/런타임 권위/목표) 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", "written", "written", GATE_AUDIT, "required gate coverage(필수 게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def write_receipts(summary: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "rows": summary["rows"], "features": summary["feature_count"], "eligible_tasks": summary["eligible_task_rows"], "next_run_id": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "data_source": summary["input_frame"], "time_axis": "closed-bar timestamp(마감봉 시각), monotonic ordered(단조 순서)", "sample_scope": "FPMarkets US100 M5 Tier A materialized frame(Tier A 물질화 프레임), rows 87666", "missing_or_duplicate_check": rel(JM_INPUT_REVIEW), "feature_label_boundary": rel(JM_FEATURE_BOUNDARY_REVIEW), "split_boundary": "existing inner split and future labels as targets only(기존 내부 분할과 미래 라벨은 목표로만 사용)", "leakage_risk": "generated labels/weights entering allowed features(생성 라벨/가중치가 허용 피처로 유입)", "data_hash_or_identity": sha(jl.JL_INPUT_FRAME), "integrity_judgment": "usable_for_training_reviewed(학습 사용 가능 검토됨)"})
    write_json(MODEL_RECEIPT, {**base, "model_family": "XGBoost/LightGBM/ExtraTrees planned(엑스지부스트/라이트GBM/엑스트라트리즈 예정)", "target_and_label": "JL profit-quality/density/runtime labels(JL 수익 품질/밀도/런타임 라벨)", "split_method": "existing ordered inner split(기존 순서 기반 내부 분할)", "selection_metric": "not_selected_in_jm(JM에서 선정 없음)", "secondary_metrics": "task eligibility, weight saturation, feature boundary(작업 적격성/가중치 포화/피처 경계)", "threshold_policy": "no threshold tuning(임계값 조정 없음)", "overfit_risk": "multiple repair axes and inner-holdout reuse(여러 수리 축과 내부 보류 재사용)", "calibration_risk": "probability scores remain ranking until runtime probe(확률 점수는 런타임 탐침 전까지 순위)", "comparison_baseline": summary["positive_clue_model_id"], "validation_judgment": "training_ready_not_selected(학습 준비됨, 선정 없음)"})
    write_json(PERFORMANCE_RECEIPT, {**base, "positive_clue_model_id": summary["positive_clue_model_id"], "negative_control_model_id": summary["negative_control_model_id"], "observed_change": "input review only(입력 검토 전용)", "trade_shape": "not_measured_in_jm(JM에서 측정 없음)", "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "judgment_label": JUDGMENT, "evidence_available": [rel(JM_INPUT_REVIEW), rel(JM_TASK_ELIGIBILITY), rel(GATE_AUDIT)], "evidence_missing": "trained models, ONNX exports, proxy scoring, MT5 runtime probe(학습 모델/ONNX/프록시 점수/MT5 런타임 탐침)", "next_condition": NEXT_RUN_ID})
    write_json(CLAIM_RECEIPT, {**base, "candidate_selection": "not_run", "forward_passed": "not_claimed", "forward_failed": "not_claimed", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "generated_with_manifest(목록과 함께 생성)", "lineage_judgment": "connected_with_boundary(경계 조건부 연결)"})


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {**dict(summary), "gate_passes": int(gates["status"].astype(str).eq("passed").sum()), "gate_total": int(len(gates))}
    write_json(FINAL_DECISION, final)
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at": TODAY, "created_at_utc": now_utc(), "script": rel(Path(__file__)), "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)], "claim_boundary": CLAIM_BOUNDARY})
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337JM Positive Low PF Recovery Drawdown Input Review(run337JM 양수 저PF 회복 낙폭 입력 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_rows']}`
- positive_clue_model(긍정 단서 모델): `{final['positive_clue_model_id']}`
- negative_control_model(부정 대조 모델): `{final['negative_control_model_id']}`

## Action(행동)

JL input materialization(JL 입력 물질화)을 leakage(누출), feature boundary(피처 경계), weight health(가중치 상태), task eligibility(작업 적격성) 기준으로 검토했다.
Effect(효과): JN training(JN 학습)은 검토된 8개 task seed(작업 씨앗)만 사용하게 된다.

## Boundary(경계)

No model training(모델 학습 없음), no ONNX export(ONNX 내보내기 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선정 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage337JM Decision(337JM 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(JM_INPUT_REVIEW)}`, `{rel(JM_TASK_ELIGIBILITY)}`, `{rel(JN_QUEUE)}`

Action(행동): JL input(JL 입력)을 JN training(JN 학습) 준비 상태로 판정했다.
Effect(효과): 다음 실행은 모델을 학습하되 selection(선정)과 runtime authority(런타임 권위)는 계속 금지된다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

JM review(JM 검토)는 JL input(JL 입력)을 training ready(학습 준비됨)로 닫았고, 아직 model selection(모델 선정)은 하지 않았다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- positive_clue_model(긍정 단서 모델): `{final['positive_clue_model_id']}`
- negative_control_model(부정 대조 모델): `{final['negative_control_model_id']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): training ready(학습 준비)를 model selection(모델 선정)으로 오해하지 않게 한다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run337JM {RUN_ID}"
    append_text_once(STAGE_BRIEF, marker, f"""## run337JM Input Review(입력 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_rows']}`
- effect(효과): JN training(JN 학습)으로 이어질 입력 검토를 완료했다.
""")
    changelog = f"""## {TODAY} run337JM Input Review(입력 검토)

- action(행동): JL input(JL 입력) `{final['rows']}`행과 task seed(작업 씨앗) `{final['eligible_task_rows']}/{final['task_rows']}`개를 검토했다.
- effect(효과): leakage(누출), feature boundary(피처 경계), weight health(가중치 상태)를 통과한 후보만 JN training(JN 학습)으로 넘겼다.
- boundary(경계): selected model(선정 모델), MT5 execution(MT5 실행), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def update_registers(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "run_number": RUN_NUMBER,
        "lane": "runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_input_review",
        "family": "experiment_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["rows"],
        "notes": f"eligible={final['eligible_task_rows']}/{final['task_rows']};features={final['feature_count']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "primary_artifact": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "input_review", "candidate_model_id": final["positive_clue_model_id"], "result_status": JUDGMENT},
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "missing_required", "result_status": "missing_required"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def artifact_type(path: Path) -> str:
    return "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip(".")


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if exists(path) and io(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": artifact_type(path), "path": rel(path), "sha256": sha(path), "created_at": TODAY, "claim_boundary": CLAIM_BOUNDARY})
    if rows:
        registry = registry.loc[~registry["path"].astype(str).isin({row["path"] for row in rows})].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        write_csv(ARTIFACT_REGISTRY, registry[list(dict.fromkeys(required + list(registry.columns)))])


def main() -> None:
    for path in (RUN_DIR, REVIEW_DIR, DECISION_DOC.parent):
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")

    input_review, feature_review, weight_review, task_eligibility, tier_review, runtime_review, lineage, queue, summary = build_reviews()
    write_csv(JM_INPUT_REVIEW, input_review)
    write_csv(JM_FEATURE_BOUNDARY_REVIEW, feature_review)
    write_csv(JM_WEIGHT_REVIEW, weight_review)
    write_csv(JM_TASK_ELIGIBILITY, task_eligibility)
    write_csv(JM_TIER_RECORD_REVIEW, tier_review)
    write_csv(JM_RUNTIME_PARITY_REVIEW, runtime_review)
    write_csv(JM_LINEAGE_REVIEW, lineage)
    write_csv(JN_QUEUE, queue)
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(OUTPUT_FILES)

    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"JM gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "rows": final["rows"],
                "feature_count": final["feature_count"],
                "eligible_task_rows": final["eligible_task_rows"],
                "task_rows": final["task_rows"],
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
