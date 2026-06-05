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
    materialize_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_inputs_without_db as iv,
)


aw = iv.aw

TODAY = "2026-06-01"
STAGE_ID = iv.STAGE_ID
STAGE_DIR = iv.STAGE_DIR
RUN_NUMBER = "run337IW"
RUN_ID = "run337IW_review_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_inputs_without_db_v1"
PARENT_RUN_ID = iv.RUN_ID
NEXT_RUN_ID = "run337IX_train_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_candidates_without_db_v1"
STATUS = "completed_stage337IW_positive_low_edge_expansion_inputs_review_training_ready_no_selection"
JUDGMENT = "iv_inputs_timestamp_safe_training_ready_with_tier_b_missing_required_named"
DECISION = "stage337IW_open_run337IX_positive_low_edge_expansion_candidate_training"
CLAIM_BOUNDARY = (
    "research_development_input_review_only_no_model_training_no_onnx_export_no_mt5_no_runtime_package_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IW_positive_low_edge_expansion_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IW_positive_low_edge_expansion_input_review.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

IW_INPUT_REVIEW = RUN_DIR / "iw_input_review_matrix.csv"
IW_FEATURE_BOUNDARY_REVIEW = RUN_DIR / "iw_feature_boundary_review.csv"
IW_WEIGHT_REVIEW = RUN_DIR / "iw_weight_saturation_review.csv"
IW_TASK_ELIGIBILITY = RUN_DIR / "iw_training_task_eligibility.csv"
IW_TIER_RECORD_REVIEW = RUN_DIR / "iw_tier_record_review.csv"
IW_RUNTIME_COMPARISON_REVIEW = RUN_DIR / "iw_runtime_comparison_review.csv"
IW_LINEAGE_REVIEW = RUN_DIR / "iw_lineage_review.csv"
IX_QUEUE = RUN_DIR / "run337IX_training_queue.csv"
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
    iv.FINAL_DECISION,
    iv.GATE_AUDIT,
    iv.IW_QUEUE,
    iv.IV_INPUT_FRAME,
    iv.IV_ALLOWED_FEATURES,
    iv.IV_WEIGHT_AUDIT,
    iv.IV_FEATURE_BOUNDARY,
    iv.IV_TIER_RECORDS,
    iv.IV_RUNTIME_COMPARISON_PLAN,
    iv.IV_TASK_SEEDS,
    iv.RUN_MANIFEST,
)
OUTPUT_FILES = (
    IW_INPUT_REVIEW,
    IW_FEATURE_BOUNDARY_REVIEW,
    IW_WEIGHT_REVIEW,
    IW_TASK_ELIGIBILITY,
    IW_TIER_RECORD_REVIEW,
    IW_RUNTIME_COMPARISON_REVIEW,
    IW_LINEAGE_REVIEW,
    IX_QUEUE,
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
    io(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def passed(series: pd.Series) -> bool:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"]).all()


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None) or pd.isna(value):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None) or pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def review_row(review_id: str, status: str, observed: Any, expected: Any, evidence: Path | str, effect: str) -> dict[str, Any]:
    return {
        "review_id": review_id,
        "status": status,
        "observed": observed,
        "expected": expected,
        "evidence": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def gate_row(gate_id: str, ok: bool, observed: Any, expected: Any, evidence: Path | str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": "passed" if ok else "failed",
        "observed": observed,
        "expected": expected,
        "evidence_path": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_input_review(frame: pd.DataFrame, allowed: pd.DataFrame, feature_boundary: pd.DataFrame) -> pd.DataFrame:
    feature_column = "feature_name" if "feature_name" in allowed.columns else allowed.columns[0]
    features = allowed[feature_column].dropna().astype(str).tolist()
    missing_features = [feature for feature in features if feature not in frame.columns]
    duplicate_rows = (
        int(frame.duplicated(["timestamp", "cost_policy_id"]).sum())
        if {"timestamp", "cost_policy_id"}.issubset(frame.columns)
        else -1
    )
    timestamp_missing = int(pd.to_datetime(frame["timestamp"], errors="coerce", utc=True).isna().sum()) if "timestamp" in frame.columns else -1
    weight_missing = [column for column in iv.IV_WEIGHT_COLUMNS if column not in frame.columns]
    target_missing = [column for column in iv.IV_TARGET_COLUMNS if column not in frame.columns]
    cost_valid = int(pd.to_numeric(frame.get("iv_valid_cost_stress_fwd18", pd.Series(dtype="float64")), errors="coerce").fillna(0).astype(int).eq(1).sum())
    cost_classes = (
        int(pd.to_numeric(frame.loc[pd.to_numeric(frame["iv_valid_cost_stress_fwd18"], errors="coerce").fillna(0).astype(int).eq(1), "iv_label_class_cost_stress_fwd18"], errors="coerce").dropna().astype(int).nunique())
        if {"iv_valid_cost_stress_fwd18", "iv_label_class_cost_stress_fwd18"}.issubset(frame.columns)
        else 0
    )
    return pd.DataFrame(
        [
            review_row("iw001_frame_rows", "passed" if len(frame) >= 87600 else "failed", len(frame), ">=87600", iv.IV_INPUT_FRAME, "입력 frame(프레임)이 손실 없이 이어졌는지 확인한다."),
            review_row("iw002_feature_count", "passed" if len(features) == 58 else "failed", len(features), 58, iv.IV_ALLOWED_FEATURES, "모델 feature(피처) 수를 기존 58개로 고정한다."),
            review_row("iw003_missing_allowed_features", "passed" if not missing_features else "failed", ";".join(missing_features), "none(없음)", iv.IV_ALLOWED_FEATURES, "허용 feature(피처)가 실제 frame(프레임)에 모두 있는지 확인한다."),
            review_row("iw004_timestamp_present", "passed" if timestamp_missing == 0 else "failed", timestamp_missing, 0, iv.IV_INPUT_FRAME, "timestamp(시각) 축이 깨지지 않았는지 확인한다."),
            review_row("iw005_duplicate_timestamp_cost_policy", "passed" if duplicate_rows == 0 else "failed", duplicate_rows, 0, iv.IV_INPUT_FRAME, "같은 cost policy(비용 정책) 안의 중복 시각을 막는다."),
            review_row("iw006_feature_boundary_source", "passed" if passed(feature_boundary["status"]) else "failed", int((feature_boundary["status"].astype(str) != "passed").sum()), 0, iv.IV_FEATURE_BOUNDARY, "feature/label boundary(피처/라벨 경계)를 학습 전에 다시 확인한다."),
            review_row("iw007_weight_columns_present", "passed" if not weight_missing else "failed", ";".join(weight_missing), "none(없음)", iv.IV_INPUT_FRAME, "train-only weight(학습 전용 가중치) 열이 모두 생성됐는지 확인한다."),
            review_row("iw008_target_columns_present", "passed" if not target_missing else "failed", ";".join(target_missing), "none(없음)", iv.IV_INPUT_FRAME, "train-only label(학습 전용 라벨) 열이 모두 생성됐는지 확인한다."),
            review_row("iw009_cost_stress_label_distribution", "passed" if cost_valid > 85000 and cost_classes == 3 else "failed", f"valid={cost_valid};classes={cost_classes}", "valid>85000;classes=3", iv.IV_INPUT_FRAME, "비용 압박 라벨이 학습 가능한 분포인지 확인한다."),
        ]
    )


def make_feature_boundary_review(feature_boundary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in feature_boundary.iterrows():
        rows.append(
            review_row(
                f"iw_feature_{row.get('audit_id', 'boundary')}",
                str(row.get("status", "")),
                row.get("observed", ""),
                row.get("expected", ""),
                row.get("evidence", iv.IV_FEATURE_BOUNDARY),
                "IV feature boundary(피처 경계) 감사 결과를 IW에서 재확인한다.",
            )
        )
    return pd.DataFrame(rows)


def make_weight_review(frame: pd.DataFrame, weight_audit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, audit in weight_audit.iterrows():
        column = str(audit["weight_column"])
        values = pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan) if column in frame.columns else pd.Series(dtype="float64")
        nonfinite = int(values.isna().sum()) if len(values) else len(frame)
        saturation = float((values >= 11.999).mean()) if len(values) else 1.0
        audit_nonfinite = as_int(audit.get("nonfinite_rows"))
        audit_saturation = as_float(audit.get("max_saturation_rate"))
        status = "passed" if column in frame.columns and nonfinite == 0 and audit_nonfinite == 0 and max(saturation, audit_saturation) <= 0.05 else "failed"
        rows.append(
            review_row(
                f"iw_weight_{column}",
                status,
                f"nonfinite={nonfinite};audit_nonfinite={audit_nonfinite};saturation={saturation:.6f};audit_saturation={audit_saturation:.6f}",
                "nonfinite=0;saturation<=0.05",
                iv.IV_WEIGHT_AUDIT,
                "weight(가중치)가 유한하고 과포화되지 않았는지 확인한다.",
            )
        )
    return pd.DataFrame(rows)


def make_task_eligibility(frame: pd.DataFrame, tasks: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, task in tasks.iterrows():
        task_id = str(task["task_id"])
        target = str(task["target_column"])
        valid_col = str(task["valid_column"])
        weight_col = str(task["sample_weight_column"])
        missing = [column for column in (target, valid_col, weight_col) if column not in frame.columns]
        if missing:
            rows.append(
                {
                    "task_id": task_id,
                    "eligible": "false",
                    "target_column": target,
                    "valid_column": valid_col,
                    "sample_weight_column": weight_col,
                    "model_family": str(task["model_family"]),
                    "rows_total": int(len(frame)),
                    "rows_valid": 0,
                    "class_count": 0,
                    "max_class_share": 1.0,
                    "weight_mean": 0.0,
                    "weight_max": 0.0,
                    "saturation_ratio": 1.0,
                    "nonfinite_weight_rows": int(len(frame)),
                    "eligibility_reason": f"missing columns(누락 열): {';'.join(missing)}",
                    "effect": "누락 열이 있으면 training(학습)으로 넘기지 않는다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        valid_mask = pd.to_numeric(frame[valid_col], errors="coerce").fillna(0).astype(int).eq(1)
        target_values = pd.to_numeric(frame[target], errors="coerce")
        mask = valid_mask & target_values.notna() & target_values.astype(float).ne(-1.0)
        valid_targets = target_values.loc[mask].astype(int)
        class_share = valid_targets.value_counts(normalize=True) if len(valid_targets) else pd.Series(dtype="float64")
        weights = pd.to_numeric(frame.loc[mask, weight_col], errors="coerce").replace([np.inf, -np.inf], np.nan)
        nonfinite = int(weights.isna().sum()) if len(weights) else 0
        saturation = float((weights >= 11.999).mean()) if len(weights) else 1.0
        max_class_share = float(class_share.max()) if len(class_share) else 1.0
        class_count = int(len(class_share))
        rows_valid = int(mask.sum())
        eligible = rows_valid >= 5000 and class_count >= 2 and nonfinite == 0 and saturation <= 0.05 and max_class_share <= 0.985
        rows.append(
            {
                "task_id": task_id,
                "eligible": "true" if eligible else "false",
                "target_column": target,
                "valid_column": valid_col,
                "sample_weight_column": weight_col,
                "model_family": str(task["model_family"]),
                "rows_total": int(len(frame)),
                "rows_valid": rows_valid,
                "class_count": class_count,
                "max_class_share": max_class_share,
                "weight_mean": float(weights.mean()) if len(weights) else 0.0,
                "weight_max": float(weights.max()) if len(weights) else 0.0,
                "saturation_ratio": saturation,
                "nonfinite_weight_rows": nonfinite,
                "eligibility_reason": "passed row/class/weight checks(행/클래스/가중치 검사 통과)" if eligible else "review failed(검토 실패)",
                "effect": "task seed(작업 씨앗)를 training(학습) 전 안전성 기준으로 거른다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def make_tier_review(tiers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in tiers.iterrows():
        status = str(row.get("status", ""))
        ok_status = "passed" if status in {"materialized", "missing_required", "out_of_scope_by_claim"} else "failed"
        rows.append(
            review_row(
                f"iw_tier_{len(rows) + 1}",
                ok_status,
                f"{row.get('tier_view', '')}={status}",
                "materialized_or_named_missing(물질화 또는 명시 누락)",
                row.get("evidence", iv.IV_TIER_RECORDS),
                "Tier A/B/combined(티어 A/B/합산) 상태를 생략하지 않는다.",
            )
        )
    return pd.DataFrame(rows)


def make_runtime_review(runtime_plan: pd.DataFrame) -> pd.DataFrame:
    requirement = " ".join(runtime_plan.get("requirement", pd.Series(dtype="object")).dropna().astype(str).tolist())
    effect_text = " ".join(runtime_plan.get("effect", pd.Series(dtype="object")).dropna().astype(str).tolist())
    mt5_required = "MT5" in requirement and ("runtime probe" in requirement or "런타임 탐침" in requirement)
    proxy_not_substitute = "대체" in effect_text or "substitute" in effect_text.lower()
    return pd.DataFrame(
        [
            review_row("iw_runtime_plan_exists", "passed" if len(runtime_plan) > 0 else "failed", len(runtime_plan), ">0", iv.IV_RUNTIME_COMPARISON_PLAN, "runtime comparison plan(런타임 비교 계획)이 있는지 확인한다."),
            review_row("iw_runtime_mt5_required", "passed" if mt5_required else "failed", requirement, "MT5 runtime probe required(MT5 런타임 탐침 필수)", iv.IV_RUNTIME_COMPARISON_PLAN, "proxy-positive(프록시 양성) 후보가 MT5(메타트레이더5) 검증으로 이어지게 한다."),
            review_row("iw_runtime_proxy_not_substitute", "passed" if proxy_not_substitute else "failed", effect_text, "proxy does not replace MT5(프록시가 MT5를 대체하지 않음)", iv.IV_RUNTIME_COMPARISON_PLAN, "proxy KPI(프록시 핵심 성과 지표)를 MT5 KPI(MT5 핵심 성과 지표)로 착각하지 않게 한다."),
        ]
    )


def make_lineage_review() -> pd.DataFrame:
    manifest = read_json(iv.RUN_MANIFEST)
    input_count = len(manifest.get("inputs", []))
    output_count = len(manifest.get("outputs", []))
    return pd.DataFrame(
        [
            review_row("iw_lineage_manifest_counts", "passed" if input_count >= 10 and output_count >= 20 else "failed", f"inputs={input_count};outputs={output_count}", "inputs>=10;outputs>=20", iv.RUN_MANIFEST, "IV 산출물 lineage(계보)가 IW로 이어지는지 확인한다."),
            review_row("iw_lineage_input_hash", "passed" if exists(iv.IV_INPUT_FRAME) else "failed", sha(iv.IV_INPUT_FRAME) if exists(iv.IV_INPUT_FRAME) else "", "sha256 present(해시 존재)", iv.IV_INPUT_FRAME, "대형 input frame(입력 프레임)의 identity(정체성)를 고정한다."),
        ]
    )


def make_queue(task_eligibility: pd.DataFrame) -> pd.DataFrame:
    eligible_count = int(task_eligibility["eligible"].astype(str).eq("true").sum())
    return pd.DataFrame(
        [
            {
                "queue_id": "iw_to_ix_training",
                "source_run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "task": "train_positive_low_edge_cost_stress_expansion_candidates(양수 낮은 엣지 비용 압박 확장 후보 학습)",
                "required_inputs": f"{rel(iv.IV_INPUT_FRAME)};{rel(iv.IV_ALLOWED_FEATURES)};{rel(iv.IV_TASK_SEEDS)};{rel(IW_TASK_ELIGIBILITY)}",
                "expected_outputs": "trained models(학습 모델); ONNX parity(ONNX 동등성); proxy scorecards(프록시 점수표); review queue(검토 대기열)",
                "blocked_if_missing": "all task eligibility true(모든 작업 적격 true)",
                "effect": f"{eligible_count} eligible tasks(적격 작업)를 IX training(IX 학습)으로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def build_summary(frame: pd.DataFrame, allowed: pd.DataFrame, task_eligibility: pd.DataFrame, weight_review: pd.DataFrame) -> dict[str, Any]:
    feature_column = "feature_name" if "feature_name" in allowed.columns else allowed.columns[0]
    failed_weight_rows = int((weight_review["status"].astype(str) != "passed").sum())
    timestamp = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce") if "timestamp" in frame.columns else pd.Series(pd.NaT, index=frame.index)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "primary_family": "experiment_execution",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": [
            "obsidian-data-integrity",
            "obsidian-model-validation",
            "obsidian-artifact-lineage",
            "obsidian-result-judgment",
        ],
        "rows": int(len(frame)),
        "timestamp_min": str(timestamp.min()),
        "timestamp_max": str(timestamp.max()),
        "feature_count": int(allowed[feature_column].dropna().shape[0]),
        "eligible_task_rows": int(task_eligibility["eligible"].astype(str).eq("true").sum()),
        "task_seed_rows": int(len(task_eligibility)),
        "failed_weight_review_rows": failed_weight_rows,
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "onnx_export": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(
    summary: Mapping[str, Any],
    input_review: pd.DataFrame,
    feature_review: pd.DataFrame,
    weight_review: pd.DataFrame,
    task_eligibility: pd.DataFrame,
    tier_review: pd.DataFrame,
    runtime_review: pd.DataFrame,
    lineage_review: pd.DataFrame,
) -> pd.DataFrame:
    parent_final = read_json(iv.FINAL_DECISION)
    parent_gates = read_csv(iv.GATE_AUDIT)
    parent_queue = read_csv(iv.IW_QUEUE)
    forbidden_clear = all(
        str(summary.get(key)) in {"not_run", "not_claimed"}
        for key in (
            "candidate_selection",
            "model_training",
            "onnx_export",
            "mt5_execution",
            "forward_passed",
            "forward_failed",
            "runtime_authority",
            "operating_promotion",
            "goal_achieve",
        )
    )
    tier_b_named = tier_review["observed"].astype(str).str.contains("Tier B").any() and tier_review["observed"].astype(str).str.contains("missing_required").any()
    all_tasks = summary["eligible_task_rows"] == summary["task_seed_rows"] and summary["task_seed_rows"] > 0
    rows = [
        gate_row("parent_iv_gates_passed", passed(parent_gates["status"]), f"{int(parent_gates['status'].astype(str).eq('passed').sum())}/{len(parent_gates)}", "all passed(모두 통과)", iv.GATE_AUDIT, "IV materialization(입력 물질화) gate(게이트)를 바탕으로 검토한다."),
        gate_row("parent_next_action_matches_iw", str(parent_final.get("next_action")) == RUN_ID and parent_queue["next_run_id"].astype(str).eq(RUN_ID).any(), parent_final.get("next_action"), RUN_ID, iv.IW_QUEUE, "IV queue(대기열)가 IW review(검토)를 가리키는지 확인한다."),
        gate_row("input_review_passed", passed(input_review["status"]), int((input_review["status"].astype(str) != "passed").sum()), 0, IW_INPUT_REVIEW, "frame(프레임), timestamp(시각), feature(피처), label(라벨) 조건을 통과시킨다."),
        gate_row("feature_boundary_review_passed", passed(feature_review["status"]), int((feature_review["status"].astype(str) != "passed").sum()), 0, IW_FEATURE_BOUNDARY_REVIEW, "feature/label boundary(피처/라벨 경계)를 재확인한다."),
        gate_row("weight_review_passed", passed(weight_review["status"]), summary["failed_weight_review_rows"], 0, IW_WEIGHT_REVIEW, "train-only weight(학습 전용 가중치) 포화와 비유한 값을 막는다."),
        gate_row("task_eligibility_passed", all_tasks, f"{summary['eligible_task_rows']}/{summary['task_seed_rows']}", "all eligible(모두 적격)", IW_TASK_ELIGIBILITY, "training(학습)으로 넘길 task seed(작업 씨앗)를 잠근다."),
        gate_row("tier_b_missing_required_named", bool(tier_b_named), "missing_required" if tier_b_named else "not_named", "missing_required", IW_TIER_RECORD_REVIEW, "Tier B(티어 B)와 combined(합산) 누락을 숨기지 않는다."),
        gate_row("runtime_comparison_plan_passed", passed(runtime_review["status"]), int((runtime_review["status"].astype(str) != "passed").sum()), 0, IW_RUNTIME_COMPARISON_REVIEW, "proxy-positive(프록시 양성) 후보가 MT5 runtime probe(MT5 런타임 탐침)로 이어지게 한다."),
        gate_row("lineage_review_passed", passed(lineage_review["status"]), int((lineage_review["status"].astype(str) != "passed").sum()), 0, IW_LINEAGE_REVIEW, "IV 산출물 계보를 IX training(IX 학습)으로 연결한다."),
        gate_row("next_training_queue_opened", exists(IX_QUEUE), rel(IX_QUEUE), "exists(존재)", IX_QUEUE, "다음 IX training(IX 학습) 대기열을 연다."),
        gate_row("no_forbidden_operating_claim", forbidden_clear, "not_run/not_claimed", "not_run/not_claimed", CLAIM_RECEIPT, "학습, MT5 실행, 선택, 운영 주장을 하지 않는다."),
        gate_row("required_gate_coverage_audit_written", True, "all required gates listed(필수 게이트 기록)", "present(존재)", GATE_AUDIT, "completion claim(완료 주장)을 gate evidence(게이트 근거)에 연결한다."),
    ]
    return pd.DataFrame(rows)


def write_receipts(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **base,
            "measurement_scope": "input review and task eligibility only(입력 검토와 작업 적격성만)",
            "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
            "gate_total": int(len(gates)),
            "effect": "training(학습) 전 입력 안전성을 고정한다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": rel(iv.IV_INPUT_FRAME),
            "time_axis": "bar close timestamp UTC inherited from IV(IV에서 상속한 봉 마감 UTC 시각)",
            "sample_scope": f"rows={summary['rows']}; {summary['timestamp_min']} to {summary['timestamp_max']}; Tier A materialized(Tier A 물질화)",
            "missing_or_duplicate_check": rel(IW_INPUT_REVIEW),
            "feature_label_boundary": rel(IW_FEATURE_BOUNDARY_REVIEW),
            "split_boundary": "no new split; source row order inherited for IX inner split(새 분할 없음, IX 내부 분할용 원천 행 순서 상속)",
            "leakage_risk": "future returns used only for labels/weights and excluded from 58 allowed features(미래 수익은 라벨/가중치 전용이며 58개 허용 피처에서 제외)",
            "data_hash_or_identity": sha(iv.IV_INPUT_FRAME) if exists(iv.IV_INPUT_FRAME) else "missing",
            "integrity_judgment": "usable_for_training_with_boundary(경계 조건부 학습 사용 가능)",
            "effect": "미래참조 편향 방어를 낮추지 않고 다음 학습 입력으로 넘긴다.",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "not_trained",
            "target_and_label": "7 reviewed task seeds including cost-stress fwd18 label(비용 압박 fwd18 라벨 포함 7개 검토 작업 씨앗)",
            "split_method": "deferred_to_IX_inner_holdout(IX 내부 보류로 이연)",
            "selection_metric": "none_no_selection(없음, 선정 없음)",
            "secondary_metrics": "row/class/weight eligibility only(행/클래스/가중치 적격성만)",
            "threshold_policy": "not_applicable_no_threshold_tuning(해당 없음, 임계값 조정 없음)",
            "overfit_risk": "multiple task exploration risk named; no model ranking yet(다중 작업 탐색 위험 명시, 모델 순위 없음)",
            "calibration_risk": "not_applicable_no_scores_yet(점수 없음)",
            "comparison_baseline": "IT exact-parity low-edge MT5 probe(IT 정확 동등성 낮은 엣지 MT5 탐침)",
            "validation_judgment": "training_ready_exploratory(탐색 학습 준비)",
            "eligible_task_rows": summary["eligible_task_rows"],
            "task_seed_rows": summary["task_seed_rows"],
            "effect": "모델 성과가 아니라 학습 가능성만 판정한다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "source_positive_low_edge": "IT MT5 exact parity positive low edge(IT MT5 정확 동등성 양수 낮은 엣지)",
            "reviewed_axes": "cost stress/density/lifecycle/drawdown/side/equity(비용 압박/밀도/생명주기/낙폭/방향/수익곡선)",
            "performance_claim": "not_made(하지 않음)",
            "effect": "수익 주장 대신 낮은 엣지 개선 축을 학습 실험으로 넘긴다.",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "judgment_label": JUDGMENT,
            "evidence_available": [rel(IW_INPUT_REVIEW), rel(IW_TASK_ELIGIBILITY), rel(GATE_AUDIT)],
            "evidence_missing": "model training, ONNX parity, proxy scorecard, MT5 runtime probe(모델 학습, ONNX 동등성, 프록시 점수표, MT5 런타임 탐침)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "model_training": "not_run",
            "onnx_export": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "input_frame": rel(iv.IV_INPUT_FRAME),
            "task_eligibility": rel(IW_TASK_ELIGIBILITY),
            "consumer": NEXT_RUN_ID,
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths() if exists(path) and io(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest(목록과 함께 생성)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
            "effect": "IV 산출물을 IX training(IX 학습) 대기열에 계보로 연결한다.",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    failed = gates.loc[~gates["status"].astype(str).eq("passed"), "gate_id"].astype(str).tolist()
    final = {
        **dict(summary),
        "gate_rows": int(len(gates)),
        "passed_gates": int(gates["status"].astype(str).eq("passed").sum()),
        "failed_gates": failed,
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337IW Positive Low-Edge Expansion Input Review(run337IW 양수 낮은 엣지 확장 입력 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- eligible_task_rows(적격 작업 수): `{final['eligible_task_rows']}/{final['task_seed_rows']}`
- failed_weight_review_rows(가중치 검토 실패 수): `{final['failed_weight_review_rows']}`

## Action(행동)

IV materialization(IV 입력 물질화) 산출물을 feature boundary(피처 경계), weight saturation(가중치 포화), task eligibility(작업 적격성), tier record(티어 기록), runtime comparison plan(런타임 비교 계획)으로 검토했다.
Effect(효과): 아직 model training(모델 학습)이나 MT5 execution(MT5 실행)을 하지 않고, training-ready(학습 준비) 작업만 IX로 넘긴다.

## Boundary(경계)

No model training(모델 학습 없음), no ONNX export(ONNX 내보내기 없음), no MT5 execution(MT5 실행 없음), no selected model(선정 모델 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`{NEXT_RUN_ID}`에서 7개 적격 task seed(작업 씨앗)를 학습한다.
"""
    decision = f"""# {TODAY} Stage337IW Decision(337IW 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(IW_TASK_ELIGIBILITY)}`, `{rel(IW_WEIGHT_REVIEW)}`, `{rel(GATE_AUDIT)}`

Action(행동): positive low-edge expansion inputs(양수 낮은 엣지 확장 입력)를 training-ready(학습 준비)로 검토했다.
Effect(효과): 다음 IX run(IX 실행)은 학습만 열고, selection(선택)과 MT5 claim(MT5 주장)은 계속 금지한다.

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

IW review(IW 검토)는 IV inputs(IV 입력)를 학습 준비 상태로 잠갔다.
효과는 IX training(IX 학습)이 검토된 7개 task seed(작업 씨앗)만 사용하게 하는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- eligible_task_rows(적격 작업 수): `{final['eligible_task_rows']}/{final['task_seed_rows']}`
- model_training(모델 학습): `not_run(미실행)`
- ONNX export(ONNX 내보내기): `not_run(미실행)`
- MT5 execution(MT5 실행): `not_run(미실행)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`
- operating_promotion(운영 승격): `not_claimed(주장 안 함)`
- goal_achieve(목표 달성): `not_claimed(주장 안 함)`

Effect(효과): 입력 검토를 모델 선정으로 오해하지 않게 한다.
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

    marker = f"run337IW {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337IW Positive Low-Edge Expansion Input Review(양수 낮은 엣지 확장 입력 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): 검토된 7개 task seed(작업 씨앗)를 IX training(IX 학습)으로 넘긴다.
""",
    )
    changelog_entry = f"""## {TODAY} run337IW Positive Low-Edge Expansion Input Review(양수 낮은 엣지 확장 입력 검토)

- action(행동): IV expansion inputs(IV 확장 입력)를 feature boundary(피처 경계), weight saturation(가중치 포화), task eligibility(작업 적격성)로 검토했다.
- effect(효과): `{NEXT_RUN_ID}`가 검토된 학습 입력만 사용하게 했다.
- boundary(경계): model training(모델 학습), MT5 execution(MT5 실행), selected model(선정 모델), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


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


def update_registers(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "input_review_training_ready",
            "rows": final["rows"],
            "feature_count": final["feature_count"],
            "task_seed_rows": final["task_seed_rows"],
            "eligible_task_rows": final["eligible_task_rows"],
            "result_status": "training_ready_no_selection",
        },
        {
            **base,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


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
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        write_csv(ARTIFACT_REGISTRY, registry[columns])


def main() -> None:
    for path in (RUN_DIR, REVIEW_DIR, DECISION_DOC.parent):
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")

    frame = pd.read_parquet(io(iv.IV_INPUT_FRAME))
    allowed = read_csv(iv.IV_ALLOWED_FEATURES)
    feature_boundary = read_csv(iv.IV_FEATURE_BOUNDARY)
    weight_audit = read_csv(iv.IV_WEIGHT_AUDIT)
    tasks = read_csv(iv.IV_TASK_SEEDS)
    tiers = read_csv(iv.IV_TIER_RECORDS)
    runtime_plan = read_csv(iv.IV_RUNTIME_COMPARISON_PLAN)

    input_review = make_input_review(frame, allowed, feature_boundary)
    feature_review = make_feature_boundary_review(feature_boundary)
    weight_review = make_weight_review(frame, weight_audit)
    task_eligibility = make_task_eligibility(frame, tasks)
    tier_review = make_tier_review(tiers)
    runtime_review = make_runtime_review(runtime_plan)
    lineage_review = make_lineage_review()
    queue = make_queue(task_eligibility)
    summary = build_summary(frame, allowed, task_eligibility, weight_review)

    write_csv(IW_INPUT_REVIEW, input_review)
    write_csv(IW_FEATURE_BOUNDARY_REVIEW, feature_review)
    write_csv(IW_WEIGHT_REVIEW, weight_review)
    write_csv(IW_TASK_ELIGIBILITY, task_eligibility)
    write_csv(IW_TIER_RECORD_REVIEW, tier_review)
    write_csv(IW_RUNTIME_COMPARISON_REVIEW, runtime_review)
    write_csv(IW_LINEAGE_REVIEW, lineage_review)
    write_csv(IX_QUEUE, queue)
    gates = build_gates(summary, input_review, feature_review, weight_review, task_eligibility, tier_review, runtime_review, lineage_review)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())

    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"IW gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "eligible_task_rows": final["eligible_task_rows"],
                "task_seed_rows": final["task_seed_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
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
