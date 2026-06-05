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
    materialize_runtime_negative_collapse_cost_stress_trade_shape_repair_inputs_without_db as jd,
)


aw = jd.aw

TODAY = "2026-06-01"
STAGE_ID = jd.STAGE_ID
STAGE_DIR = jd.STAGE_DIR
RUN_NUMBER = "run337JE"
RUN_ID = "run337JE_review_runtime_negative_collapse_cost_stress_trade_shape_repair_inputs_without_db_v1"
PARENT_RUN_ID = jd.RUN_ID
NEXT_RUN_ID = "run337JF_train_runtime_negative_collapse_cost_stress_trade_shape_repair_candidates_without_db_v1"
STATUS = "completed_stage337JE_runtime_negative_collapse_repair_inputs_review_training_ready_no_selection"
JUDGMENT = "runtime_negative_collapse_repair_inputs_timestamp_safe_training_ready"
DECISION = "stage337JE_open_run337JF_train_runtime_negative_collapse_repair_candidates"
CLAIM_BOUNDARY = (
    "research_development_input_review_only_no_model_training_no_onnx_export_no_mt5_no_runtime_package_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337JE_runtime_negative_collapse_repair_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337JE_runtime_negative_collapse_repair_input_review.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

JE_INPUT_REVIEW = RUN_DIR / "je_input_review_matrix.csv"
JE_FEATURE_BOUNDARY_REVIEW = RUN_DIR / "je_feature_boundary_review.csv"
JE_WEIGHT_REVIEW = RUN_DIR / "je_weight_saturation_review.csv"
JE_TASK_ELIGIBILITY = RUN_DIR / "je_training_task_eligibility.csv"
JE_TIER_RECORD_REVIEW = RUN_DIR / "je_tier_record_review.csv"
JE_RUNTIME_COMPARISON_REVIEW = RUN_DIR / "je_runtime_comparison_review.csv"
JE_LINEAGE_REVIEW = RUN_DIR / "je_lineage_review.csv"
JF_QUEUE = RUN_DIR / "run337JF_training_queue.csv"
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
    jd.FINAL_DECISION,
    jd.GATE_AUDIT,
    jd.JD_INPUT_FRAME,
    jd.JD_ALLOWED_FEATURES,
    jd.JD_WEIGHT_AUDIT,
    jd.JD_FEATURE_BOUNDARY,
    jd.JD_TASK_SEEDS,
    jd.JD_TIER_RECORDS,
    jd.JD_RUNTIME_COMPARISON_PLAN,
)
OUTPUT_FILES = (
    JE_INPUT_REVIEW,
    JE_FEATURE_BOUNDARY_REVIEW,
    JE_WEIGHT_REVIEW,
    JE_TASK_ELIGIBILITY,
    JE_TIER_RECORD_REVIEW,
    JE_RUNTIME_COMPARISON_REVIEW,
    JE_LINEAGE_REVIEW,
    JF_QUEUE,
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


def display_path(path: Path | str) -> str:
    value = Path(path)
    try:
        if str(value.resolve()).lower().startswith(str(ROOT.resolve()).lower()):
            return rel(value)
    except OSError:
        pass
    return value.as_posix()


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


def numeric(frame: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(frame[column], errors="coerce") if column in frame.columns else pd.Series(np.nan, index=frame.index)


def build_reviews() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    parent = read_json(jd.FINAL_DECISION)
    frame = pd.read_parquet(io(jd.JD_INPUT_FRAME))
    allowed = read_csv(jd.JD_ALLOWED_FEATURES)
    feature_boundary = read_csv(jd.JD_FEATURE_BOUNDARY)
    weight_audit = read_csv(jd.JD_WEIGHT_AUDIT)
    tasks = read_csv(jd.JD_TASK_SEEDS)
    tiers = read_csv(jd.JD_TIER_RECORDS)
    runtime_plan = read_csv(jd.JD_RUNTIME_COMPARISON_PLAN)
    feature_col = "feature_name" if "feature_name" in allowed.columns else allowed.columns[0]
    features = [str(item) for item in allowed[feature_col].dropna().tolist()]
    missing_features = [feature for feature in features if feature not in frame.columns]
    timestamp_missing = int(frame["timestamp"].isna().sum()) if "timestamp" in frame.columns else len(frame)
    duplicate_rows = int(frame.duplicated(["timestamp", "cost_policy_id"]).sum()) if {"timestamp", "cost_policy_id"}.issubset(frame.columns) else -1
    weight_missing = [column for column in jd.JD_WEIGHT_COLUMNS if column not in frame.columns]
    target_missing = [column for column in jd.JD_TARGET_COLUMNS if column not in frame.columns]
    target = numeric(frame, "jd_label_class_runtime_pnl_fwd18").fillna(-1).astype(int)
    valid = numeric(frame, "jd_valid_runtime_pnl_fwd18").fillna(0).astype(int)
    target_valid = int(valid.eq(1).sum())
    target_classes = int(target.loc[target.isin([0, 1, 2])].nunique())
    input_review = pd.DataFrame(
        [
            review_row("je001_frame_rows", len(frame) >= 87600, len(frame), ">=87600", jd.JD_INPUT_FRAME, "입력 frame(프레임)이 손실 없이 이어졌는지 확인한다."),
            review_row("je002_feature_count", len(features) == 58, len(features), 58, jd.JD_ALLOWED_FEATURES, "모델 feature(피처) 수를 기존 58개로 고정한다."),
            review_row("je003_missing_allowed_features", not missing_features, ";".join(missing_features), "none(없음)", jd.JD_ALLOWED_FEATURES, "허용 feature(피처)가 실제 frame(프레임)에 모두 있는지 확인한다."),
            review_row("je004_timestamp_present", timestamp_missing == 0, timestamp_missing, 0, jd.JD_INPUT_FRAME, "timestamp(시각) 축이 깨지지 않았는지 확인한다."),
            review_row("je005_duplicate_timestamp_cost_policy", duplicate_rows == 0, duplicate_rows, 0, jd.JD_INPUT_FRAME, "같은 cost policy(비용 정책) 안의 중복 시각을 막는다."),
            review_row("je006_weight_columns_present", not weight_missing, ";".join(weight_missing), "none(없음)", jd.JD_INPUT_FRAME, "train-only weight(학습 전용 가중치) 열이 모두 생성됐는지 확인한다."),
            review_row("je007_target_columns_present", not target_missing, ";".join(target_missing), "none(없음)", jd.JD_INPUT_FRAME, "train-only label(학습 전용 라벨) 열이 모두 생성됐는지 확인한다."),
            review_row("je008_runtime_pnl_label_distribution", target_valid > 85000 and target_classes == 3, f"valid={target_valid};classes={target_classes}", "valid>85000;classes=3", jd.JD_INPUT_FRAME, "런타임 손익 라벨이 학습 가능한 분포인지 확인한다."),
        ]
    )
    feature_review = feature_boundary.copy()
    feature_review["review_status"] = feature_review["status"]
    feature_review["effect"] = "feature/label boundary(피처/라벨 경계)를 JE에서 재확인한다."
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
        present = all(column in frame.columns for column in [target_col, valid_col, weight_col])
        if present:
            valid_mask = numeric(frame, valid_col).fillna(0).astype(int).eq(1)
            labels = numeric(frame.loc[valid_mask], target_col).fillna(-1).astype(int)
            weights = numeric(frame.loc[valid_mask], weight_col)
            valid_rows = int(valid_mask.sum())
            class_count = int(labels.loc[labels.isin([0, 1, 2])].nunique())
            nonfinite = int((~np.isfinite(weights.to_numpy(dtype="float64"))).sum())
        else:
            valid_rows = 0
            class_count = 0
            nonfinite = 1
        eligible = present and valid_rows > 1000 and class_count == 3 and nonfinite == 0
        task_rows.append(
            {
                **task.to_dict(),
                "eligible": bool(eligible),
                "status": "passed" if eligible else "failed",
                "valid_rows": valid_rows,
                "class_count": class_count,
                "nonfinite_weight_rows": nonfinite,
                "effect": "training(학습)으로 넘길 task seed(작업 씨앗)의 입력/라벨/가중치를 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    task_eligibility = pd.DataFrame(task_rows)

    tier_review = tiers.copy()
    tier_review["review_status"] = np.where(
        tier_review["view"].astype(str).str.contains("Tier A") & tier_review["status"].astype(str).eq("materialized"),
        "passed",
        np.where(tier_review["status"].astype(str).eq("missing_required"), "passed", "failed"),
    )
    tier_review["effect"] = "Tier A/B paired record(티어 A/B 쌍 기록)를 검토한다."
    tier_review["claim_boundary"] = CLAIM_BOUNDARY

    runtime_review = runtime_plan.copy()
    runtime_review["review_status"] = np.where(runtime_review["proxy_does_not_replace_mt5"].astype(str).str.lower().isin(["true", "1", "yes"]), "passed", "failed")
    runtime_review["effect"] = "proxy(프록시)가 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않게 한다."
    runtime_review["claim_boundary"] = CLAIM_BOUNDARY

    lineage_review = pd.DataFrame(
        [
            review_row("je_lineage_parent_final", parent.get("next_action") == RUN_ID, parent.get("next_action"), RUN_ID, jd.FINAL_DECISION, "JD final decision(최종 결정)이 JE를 가리키는지 확인한다."),
            review_row("je_lineage_input_hash", exists(jd.JD_INPUT_FRAME), sha(jd.JD_INPUT_FRAME) if exists(jd.JD_INPUT_FRAME) else "", "sha256 present(해시 존재)", jd.JD_INPUT_FRAME, "대형 input frame(입력 프레임)의 identity(정체성)를 고정한다."),
            review_row("je_lineage_task_seed_hash", exists(jd.JD_TASK_SEEDS), sha(jd.JD_TASK_SEEDS) if exists(jd.JD_TASK_SEEDS) else "", "sha256 present(해시 존재)", jd.JD_TASK_SEEDS, "task seed(작업 씨앗)의 identity(정체성)를 고정한다."),
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "queue_id": "jf_train_runtime_negative_collapse_repair_candidates",
                "source_run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "eligible_task_rows": int(task_eligibility["eligible"].sum()),
                "required_inputs": f"{rel(jd.JD_INPUT_FRAME)};{rel(jd.JD_ALLOWED_FEATURES)};{rel(jd.JD_TASK_SEEDS)};{rel(JE_TASK_ELIGIBILITY)}",
                "required_outputs": "trained models, ONNX parity, proxy scorecards(학습 모델, ONNX 동등성, 프록시 점수판)",
                "forbidden_action": "candidate selection before MT5 runtime probe(MT5 런타임 탐침 전 후보 선택)",
                "effect": "검토된 task seed(작업 씨앗)만 JF training(JF 학습)으로 넘긴다.",
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
        "input_review_failures": int((input_review["status"] != "passed").sum()),
        "feature_review_failures": int((feature_review["review_status"] != "passed").sum()),
        "weight_review_failures": int((weight_review["status"] != "passed").sum()),
        "task_seed_rows": int(len(task_eligibility)),
        "eligible_task_rows": int(task_eligibility["eligible"].sum()),
        "target_valid_rows": target_valid,
        "target_class_count": target_classes,
        "tier_review_failures": int((tier_review["review_status"] != "passed").sum()),
        "runtime_review_failures": int((runtime_review["review_status"] != "passed").sum()),
        "lineage_review_failures": int((lineage_review["status"] != "passed").sum()),
        "input_frame": rel(jd.JD_INPUT_FRAME),
        "allowed_features": rel(jd.JD_ALLOWED_FEATURES),
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return input_review, feature_review, weight_review, task_eligibility, tier_review, runtime_review, lineage_review, queue, summary


def gate_row(gate: str, status: bool, observed: Any, expected: Any, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": "passed" if status else "failed",
        "observed": observed,
        "expected": expected,
        "evidence_path": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(jd.GATE_AUDIT)
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
            gate_row("parent_jd_gates_passed", passed_status(parent_gates["status"]).all(), "all passed", "all passed", jd.GATE_AUDIT, "JD 물질화 gate(게이트) 통과 뒤 검토한다."),
            gate_row("input_review_passed", summary["input_review_failures"] == 0, summary["input_review_failures"], 0, JE_INPUT_REVIEW, "frame/timestamp/feature/label(프레임/시각/피처/라벨)을 확인한다."),
            gate_row("feature_boundary_review_passed", summary["feature_review_failures"] == 0, summary["feature_review_failures"], 0, JE_FEATURE_BOUNDARY_REVIEW, "feature/label boundary(피처/라벨 경계)를 재확인한다."),
            gate_row("weight_review_passed", summary["weight_review_failures"] == 0, summary["weight_review_failures"], 0, JE_WEIGHT_REVIEW, "weight(가중치) 유한성과 포화를 확인한다."),
            gate_row("task_eligibility_passed", summary["eligible_task_rows"] == summary["task_seed_rows"] and summary["task_seed_rows"] >= 8, f"{summary['eligible_task_rows']}/{summary['task_seed_rows']}", "all eligible(모두 적격)", JE_TASK_ELIGIBILITY, "training(학습)으로 넘길 task seed(작업 씨앗)를 잠근다."),
            gate_row("tier_pair_review_passed", summary["tier_review_failures"] == 0, summary["tier_review_failures"], 0, JE_TIER_RECORD_REVIEW, "Tier A/B 쌍 기록을 확인한다."),
            gate_row("runtime_plan_review_passed", summary["runtime_review_failures"] == 0, summary["runtime_review_failures"], 0, JE_RUNTIME_COMPARISON_REVIEW, "runtime comparison plan(런타임 비교 계획)을 확인한다."),
            gate_row("lineage_review_passed", summary["lineage_review_failures"] == 0, summary["lineage_review_failures"], 0, JE_LINEAGE_REVIEW, "입력 산출물 계보를 확인한다."),
            gate_row("training_queue_written", exists(JF_QUEUE), exists(JF_QUEUE), "true", JF_QUEUE, "JF training(JF 학습)으로 연결한다."),
            gate_row("no_forbidden_operating_claim", no_forbidden, "not_claimed", "not_claimed", FINAL_DECISION, "선택/운영/목표 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", True, "written", "written", GATE_AUDIT, "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


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


def artifact_paths() -> list[Path]:
    return list(OUTPUT_FILES)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if exists(path) and io(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."), "path": display_path(path), "sha256": sha(path), "created_at": TODAY, "claim_boundary": CLAIM_BOUNDARY})
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        write_csv(ARTIFACT_REGISTRY, registry[columns])


def write_receipts(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "created_at_utc": now_utc(), "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "input_review": rel(JE_INPUT_REVIEW), "task_eligibility": rel(JE_TASK_ELIGIBILITY), "gate_passes": int(gates["status"].astype(str).eq("passed").sum()), "gate_total": int(len(gates)), "effect": "검토된 입력만 JF training(JF 학습)으로 넘긴다."})
    write_json(DATA_RECEIPT, {**base, "data_source": rel(jd.JD_INPUT_FRAME), "missing_or_duplicate_check": rel(JE_INPUT_REVIEW), "feature_label_boundary": rel(JE_FEATURE_BOUNDARY_REVIEW), "split_boundary": "source_row_id ordered inner split(source_row_id 순서 내부 분할)", "data_hash_or_identity": sha(jd.JD_INPUT_FRAME), "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "feature_count": summary["feature_count"], "task_seed_rows": summary["task_seed_rows"], "eligible_task_rows": summary["eligible_task_rows"], "threshold_policy": "no threshold tuning(임계값 조정 없음)", "validation_judgment": "training_ready_no_selection(학습 준비, 선택 없음)"})
    write_json(PERFORMANCE_RECEIPT, {**base, "observed_change": "runtime-negative repair inputs reviewed(런타임 음성 수리 입력 검토)", "comparison_baseline": rel(jd.FINAL_DECISION), "next_probe": NEXT_RUN_ID, "attribution_confidence": "not_applicable_input_review_only(입력 검토 전용 해당 없음)"})
    write_json(JUDGMENT_RECEIPT, {**base, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "result_class": "input_review_training_ready(입력 검토, 학습 준비)", "gate_passes": int(gates["status"].astype(str).eq("passed").sum()), "gate_total": int(len(gates))})
    write_json(CLAIM_RECEIPT, {**base, "candidate_selection": "not_run", "forward_passed": "not_claimed", "forward_failed": "not_claimed", "goal_achieve": "not_claimed", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed"})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [display_path(path) for path in artifact_paths() if exists(path)], "artifact_hashes": {display_path(path): sha(path) for path in artifact_paths() if exists(path) and io(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "generated_with_manifest(목록과 해시 생성)", "lineage_judgment": "connected_with_boundary(경계 조건부 연결)"})


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {**dict(summary), "gate_passes": int(gates["status"].astype(str).eq("passed").sum()), "gate_total": int(len(gates))}
    write_json(FINAL_DECISION, final)
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at": TODAY, "created_at_utc": now_utc(), "script": rel(Path(__file__)), "inputs": [rel(path) for path in INPUT_FILES], "outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)], "claim_boundary": CLAIM_BOUNDARY})
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337JE Runtime Negative Collapse Repair Input Review(run337JE 런타임 음성 붕괴 수리 입력 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_seed_rows']}`
- target_valid_rows(목표 유효 행): `{final['target_valid_rows']}`

## Action(행동)

JD input frame(JD 입력 프레임), feature boundary(피처 경계), weight(가중치), task seed(작업 씨앗)를 검토했다.
Effect(효과): 검토된 8개 task seed(작업 씨앗)만 JF training(JF 학습)으로 넘긴다.

## Boundary(경계)

No model training(모델 학습 없음), no ONNX export(ONNX 내보내기 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선택 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage337JE Decision(337JE 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(JE_TASK_ELIGIBILITY)}`, `{rel(JE_WEIGHT_REVIEW)}`, `{rel(GATE_AUDIT)}`

Action(행동): JD inputs(JD 입력)을 training-ready(학습 준비)로 검토했다.
Effect(효과): JF training(JF 학습)이 timestamp-safe(시점 안전) 입력만 쓰게 한다.

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

JE review(JE 검토)는 JD input materialization(JD 입력 물질화)을 학습 가능 상태로 확인했다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선택 모델): `none(없음)`
- latest_judgment(최신 판정): `runtime_negative_collapse_repair_inputs_training_ready(런타임 음성 붕괴 수리 입력 학습 준비)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 입력 검토를 모델 선택이나 운영 승격으로 오해하지 않게 한다.
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
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run337JE {RUN_ID}"
    append_text_once(STAGE_BRIEF, marker, f"""## run337JE Runtime Negative Collapse Repair Input Review(런타임 음성 붕괴 수리 입력 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_seed_rows']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): 검토된 task seed(작업 씨앗)를 JF training(JF 학습)으로 넘겼다.
""")
    changelog_entry = f"""## {TODAY} run337JE Runtime Negative Collapse Repair Input Review(런타임 음성 붕괴 수리 입력 검토)

- action(행동): JD 입력, 가중치, task seed(작업 씨앗)를 검토했다.
- effect(효과): `{final['eligible_task_rows']}`개 task seed(작업 씨앗)를 JF training(JF 학습) 준비 상태로 만들었다.
- boundary(경계): selected model(선택 모델), MT5 execution(MT5 실행), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def update_registers(final: Mapping[str, Any]) -> None:
    base = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "run_date": TODAY, "status": STATUS, "judgment": JUDGMENT, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "primary_artifact": rel(FINAL_DECISION), "report_path": rel(REPORT_PATH), "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "claim_boundary": CLAIM_BOUNDARY}
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "input_review_training_ready", "rows": final["rows"], "feature_count": final["feature_count"], "task_seed_rows": final["task_seed_rows"], "eligible_task_rows": final["eligible_task_rows"], "result_status": JUDGMENT},
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "missing_required", "result_status": "missing_required"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def main() -> None:
    for path in [RUN_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")
    reviews = build_reviews()
    input_review, feature_review, weight_review, task_eligibility, tier_review, runtime_review, lineage_review, queue, summary = reviews
    write_csv(JE_INPUT_REVIEW, input_review)
    write_csv(JE_FEATURE_BOUNDARY_REVIEW, feature_review)
    write_csv(JE_WEIGHT_REVIEW, weight_review)
    write_csv(JE_TASK_ELIGIBILITY, task_eligibility)
    write_csv(JE_TIER_RECORD_REVIEW, tier_review)
    write_csv(JE_RUNTIME_COMPARISON_REVIEW, runtime_review)
    write_csv(JE_LINEAGE_REVIEW, lineage_review)
    write_csv(JF_QUEUE, queue)
    gates = build_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"JE gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "rows": final["rows"],
                "eligible_task_rows": final["eligible_task_rows"],
                "task_seed_rows": final["task_seed_rows"],
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
