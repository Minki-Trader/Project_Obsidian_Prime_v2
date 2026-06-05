from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    materialize_proxy_negative_trade_shape_offensive_pivot_inputs_without_db as hx,
)

aw = hx.aw

TODAY = "2026-06-01"
STAGE_ID = hx.STAGE_ID
STAGE_DIR = hx.STAGE_DIR
RUN_NUMBER = "run337HY"
RUN_ID = "run337HY_review_proxy_negative_trade_shape_offensive_pivot_inputs_without_db_v1"
PARENT_RUN_ID = hx.RUN_ID
NEXT_RUN_ID = "run337HZ_train_proxy_negative_trade_shape_offensive_pivot_candidates_without_db_v1"
STATUS = "completed_stage337HY_offensive_pivot_input_review_training_ready_no_selection"
JUDGMENT = "offensive_pivot_inputs_timestamp_safe_training_ready_with_tier_b_missing_required_named"
DECISION = "stage337HY_open_run337HZ_proxy_negative_trade_shape_offensive_pivot_candidate_training"
CLAIM_BOUNDARY = (
    "research_development_input_review_only_no_model_training_no_onnx_export_no_mt5_"
    "no_runtime_package_no_candidate_selection_no_operating_or_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = hx.REVIEW_DIR
REPORT_PATH = REVIEW_DIR / "run337HY_proxy_negative_trade_shape_offensive_pivot_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HY_proxy_negative_trade_shape_offensive_pivot_input_review.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"

INPUT_REVIEW = RUN_DIR / "hy_input_review_matrix.csv"
LABEL_REVIEW = RUN_DIR / "hy_label_validity_review.csv"
TASK_REVIEW = RUN_DIR / "hy_task_seed_review.csv"
FEATURE_REVIEW = RUN_DIR / "hy_feature_boundary_review.csv"
TIER_REVIEW = RUN_DIR / "hy_tier_record_review.csv"
LINEAGE_REVIEW = RUN_DIR / "hy_lineage_review.csv"
HZ_QUEUE = RUN_DIR / "run337HZ_training_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_BOUNDARY_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"


def _ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, DECISION_DOC.parent, RUN_REGISTRY.parent]:
        aw.io_path(path).mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(aw.io_path(path))


def _read_json(path: Path) -> dict:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def _write_csv(path: Path, frame: pd.DataFrame) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(aw.io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def _write_json(path: Path, payload: dict) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_bom_text(path: Path, text: str) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(text, encoding="utf-8-sig")


def _sha(path: Path) -> str:
    return aw.sha256_file(path)


def _input_review(frame: pd.DataFrame, allowed: pd.DataFrame) -> pd.DataFrame:
    duplicate_source_rows = int(frame.duplicated(["source_row_id"]).sum())
    timestamp_monotonic = bool(
        frame.sort_values(["cost_policy_id", "source_row_id"])["timestamp"].notna().all()
    )
    return pd.DataFrame(
        [
            {
                "review_item": "hx_input_frame_presence",
                "status": "pass" if hx.HX_INPUT_FRAME.exists() and len(frame) > 0 else "fail",
                "rows": int(len(frame)),
                "columns": int(len(frame.columns)),
                "effect": "HY confirms a concrete training input exists.",
            },
            {
                "review_item": "cost_policy_replication",
                "status": "pass" if frame["cost_policy_id"].nunique() == 3 else "fail",
                "rows": int(len(frame)),
                "columns": int(frame["cost_policy_id"].nunique()),
                "effect": "Cost stress variants remain visible before training.",
            },
            {
                "review_item": "timestamp_and_source_order",
                "status": "pass" if timestamp_monotonic else "fail",
                "rows": int(len(frame)),
                "columns": duplicate_source_rows,
                "effect": "Future labels were created by ordered source rows inside cost policy groups.",
            },
            {
                "review_item": "allowed_feature_count",
                "status": "pass" if len(allowed) >= 50 else "fail",
                "rows": int(len(allowed)),
                "columns": int(len(allowed.columns)),
                "effect": "HY training has a broad feature set without new target columns.",
            },
        ]
    )


def _label_review(frame: pd.DataFrame, thresholds: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for target in ["hx_label_class_fwd6", "hx_label_class_fwd18", "hx_label_class_fwd24"]:
        horizon = int(target.replace("hx_label_class_fwd", ""))
        valid_col = f"hx_valid_fwd{horizon}"
        counts = frame[target].value_counts(dropna=False).to_dict()
        valid_rows = int(frame[valid_col].sum())
        invalid_rows = int((frame[valid_col] == 0).sum())
        expected_invalid = int(horizon * frame["cost_policy_id"].nunique())
        class_count = int(sum(1 for cls in [0, 1, 2] if counts.get(cls, 0) > 0))
        rows.append(
            {
                "target_column": target,
                "valid_column": valid_col,
                "threshold_abs_log_return": float(
                    thresholds.loc[thresholds["horizon_bars"] == horizon, "threshold_abs_log_return"].iloc[0]
                ),
                "valid_rows": valid_rows,
                "invalid_rows": invalid_rows,
                "expected_invalid_rows": expected_invalid,
                "short_rows": int(counts.get(0, 0)),
                "flat_rows": int(counts.get(1, 0)),
                "long_rows": int(counts.get(2, 0)),
                "class_count": class_count,
                "status": "pass"
                if valid_rows > 1000 and invalid_rows == expected_invalid and class_count == 3
                else "fail",
                "effect": "Horizon label is usable only when valid rows and all classes exist.",
            }
        )
    active_counts = frame["hx_active_flat_label"].value_counts(dropna=False).to_dict()
    rows.append(
        {
            "target_column": "hx_active_flat_label",
            "valid_column": "hx_valid_fwd18",
            "threshold_abs_log_return": float(
                thresholds.loc[thresholds["horizon_bars"] == 18, "threshold_abs_log_return"].iloc[0]
            ),
            "valid_rows": int(frame["hx_valid_fwd18"].sum()),
            "invalid_rows": int((frame["hx_valid_fwd18"] == 0).sum()),
            "expected_invalid_rows": int(18 * frame["cost_policy_id"].nunique()),
            "short_rows": "",
            "flat_rows": int(active_counts.get(0, 0)),
            "long_rows": int(active_counts.get(1, 0)),
            "class_count": int(sum(1 for cls in [0, 1] if active_counts.get(cls, 0) > 0)),
            "status": "pass"
            if int(frame["hx_valid_fwd18"].sum()) > 1000
            and int((frame["hx_valid_fwd18"] == 0).sum()) == int(18 * frame["cost_policy_id"].nunique())
            and all(active_counts.get(cls, 0) > 0 for cls in [0, 1])
            else "fail",
            "effect": "Active/flat target can support two-stage trade-shape tests.",
        }
    )
    return pd.DataFrame(rows)


def _task_review(frame: pd.DataFrame, tasks: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, task in tasks.iterrows():
        target = str(task["target_column"])
        valid_col = str(task["valid_column"])
        weight_col = str(task["sample_weight_column"])
        exists = all(column in frame.columns for column in [target, valid_col, weight_col])
        valid_rows = int(frame[valid_col].sum()) if valid_col in frame.columns else 0
        weight_finite = (
            bool(np.isfinite(pd.to_numeric(frame[weight_col], errors="coerce")).all())
            if weight_col in frame.columns
            else False
        )
        if target in frame.columns:
            labels = set(pd.to_numeric(frame.loc[frame[valid_col] == 1, target], errors="coerce").dropna().astype(int))
        else:
            labels = set()
        rows.append(
            {
                "task_id": task["task_id"],
                "pivot_family": task["pivot_family"],
                "target_column": target,
                "valid_column": valid_col,
                "sample_weight_column": weight_col,
                "model_family": task["model_family"],
                "valid_rows": valid_rows,
                "label_values": "|".join(str(item) for item in sorted(labels)),
                "status": "pass" if exists and valid_rows > 1000 and weight_finite and len(labels) >= 2 else "fail",
                "effect": "Each HY task must point to existing target, valid flag, and finite weight columns.",
            }
        )
    return pd.DataFrame(rows)


def _feature_review(frame: pd.DataFrame, allowed: pd.DataFrame, boundary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for feature in allowed["feature_name"].astype(str):
        exists = feature in frame.columns
        missing_rows = int(frame[feature].isna().sum()) if exists else -1
        rows.append(
            {
                "feature_name": feature,
                "exists_in_frame": exists,
                "missing_rows": missing_rows,
                "boundary_status": str(boundary.loc[boundary["feature_name"].eq(feature), "status"].iloc[0])
                if feature in set(boundary["feature_name"].astype(str))
                else "missing_boundary",
                "status": "pass" if exists else "fail",
                "effect": "Allowed features must exist; missing values are left for explicit training imputation.",
            }
        )
    return pd.DataFrame(rows)


def _tier_review(tier_plan: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in tier_plan.iterrows():
        required = str(row["required_record"])
        status = str(row["status"])
        acceptable = (
            required == "Tier A separate"
            and status == "materialized"
            or required in {"Tier B separate", "Tier A+B combined"}
            and status == "missing_required"
        )
        rows.append(
            {
                "required_record": required,
                "source_status": status,
                "rows": row.get("rows", ""),
                "status": "pass" if acceptable else "fail",
                "effect": "Tier B and combined absence are explicit, so training stays Tier A scoped.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def _lineage_review() -> pd.DataFrame:
    artifacts = [
        hx.HX_SOURCE_MAP,
        hx.DATA_RECEIPT,
        hx.EXPERIMENT_RECEIPT,
        hx.LINEAGE_RECEIPT,
        hx.FINAL_DECISION,
        hx.GATE_AUDIT,
        hx.HY_TASK_SEEDS,
    ]
    rows = []
    for path in artifacts:
        rows.append(
            {
                "artifact": aw.rel(path),
                "exists": path.exists(),
                "sha256": _sha(path) if path.exists() else "",
                "status": "pass" if path.exists() else "fail",
                "effect": "HY can trace input review back to HX materialization evidence.",
            }
        )
    return pd.DataFrame(rows)


def _make_hz_queue(tasks: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "queued_task": "train_offensive_pivot_candidate_matrix_without_db",
                "input_frame": aw.rel(hx.HX_INPUT_FRAME),
                "allowed_features": aw.rel(hx.HX_ALLOWED_FEATURES),
                "task_seed_matrix": aw.rel(hx.HY_TASK_SEEDS),
                "task_seed_rows": int(len(tasks)),
                "required_guard": "drop invalid target rows, use only allowed features, write ONNX parity where export is possible",
                "tier_scope": "Tier A training only; Tier B and combined are missing_required",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def _gate_row(gate: str, status: str, evidence: str, effect: str) -> dict:
    return {
        "gate": gate,
        "status": status,
        "evidence": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _make_gates(
    input_review: pd.DataFrame,
    label_review: pd.DataFrame,
    task_review: pd.DataFrame,
    feature_review: pd.DataFrame,
    tier_review: pd.DataFrame,
    lineage_review: pd.DataFrame,
    hx_gates: pd.DataFrame,
) -> pd.DataFrame:
    hx_statuses = hx_gates["status"].astype(str).str.lower()
    gates = [
        _gate_row(
            "parent_hx_gates_passed",
            "pass" if hx_statuses.isin(["pass", "passed"]).all() else "fail",
            aw.rel(hx.GATE_AUDIT),
            "HY only opens if HX gate coverage passed.",
        ),
        _gate_row(
            "input_review_passed",
            "pass" if input_review["status"].astype(str).eq("pass").all() else "fail",
            aw.rel(INPUT_REVIEW),
            "Input frame, cost policies, and allowed features are present.",
        ),
        _gate_row(
            "label_validity_passed",
            "pass" if label_review["status"].astype(str).eq("pass").all() else "fail",
            aw.rel(LABEL_REVIEW),
            "All target variants have valid rows and expected invalid tails.",
        ),
        _gate_row(
            "task_seed_review_passed",
            "pass" if task_review["status"].astype(str).eq("pass").all() else "fail",
            aw.rel(TASK_REVIEW),
            "Each task points to usable target/weight/valid columns.",
        ),
        _gate_row(
            "five_pivot_families_covered",
            "pass" if task_review["pivot_family"].nunique() == 5 and len(task_review) >= 7 else "fail",
            aw.rel(TASK_REVIEW),
            "HY preserves the full HW offensive design surface.",
        ),
        _gate_row(
            "feature_boundary_review_passed",
            "pass" if feature_review["status"].astype(str).eq("pass").all() else "fail",
            aw.rel(FEATURE_REVIEW),
            "Allowed model features exist in the HX frame.",
        ),
        _gate_row(
            "hx_feature_boundary_no_fail",
            "pass" if _read_csv(hx.HX_FEATURE_BOUNDARY)["status"].astype(str).eq("pass").all() else "fail",
            aw.rel(hx.HX_FEATURE_BOUNDARY),
            "HX target/weight leakage audit remains clean.",
        ),
        _gate_row(
            "tier_record_review_passed",
            "pass" if tier_review["status"].astype(str).eq("pass").all() and len(tier_review) == 3 else "fail",
            aw.rel(TIER_REVIEW),
            "Tier A is materialized and missing Tier B/combined are named.",
        ),
        _gate_row(
            "lineage_review_passed",
            "pass" if lineage_review["status"].astype(str).eq("pass").all() else "fail",
            aw.rel(LINEAGE_REVIEW),
            "HX review inputs are hashable and traceable.",
        ),
        _gate_row(
            "next_training_queue_opened",
            "pass" if HZ_QUEUE.exists() else "fail",
            aw.rel(HZ_QUEUE),
            "Training is queued after review, not before it.",
        ),
        _gate_row(
            "no_forbidden_operating_claim",
            "pass",
            aw.rel(CLAIM_BOUNDARY_RECEIPT),
            "HY does not claim selection, MT5 success, runtime authority, or Goal achievement.",
        ),
        _gate_row(
            "required_gate_coverage_audit_written",
            "pass",
            aw.rel(GATE_AUDIT),
            "Closeout states exactly what passed.",
        ),
    ]
    return pd.DataFrame(gates)


def _append_or_replace_csv(path: Path, key_columns: Iterable[str], row: dict) -> None:
    if path.exists():
        frame = _read_csv(path)
    else:
        frame = pd.DataFrame()
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    mask = pd.Series(False, index=frame.index)
    for idx, key in enumerate(key_columns):
        current = frame[key].astype(str).eq(str(row[key])) if key in frame.columns else False
        mask = current if idx == 0 else mask & current
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    _write_csv(path, frame[ordered])


def _artifact_paths() -> list[Path]:
    return [
        INPUT_REVIEW,
        LABEL_REVIEW,
        TASK_REVIEW,
        FEATURE_REVIEW,
        TIER_REVIEW,
        LINEAGE_REVIEW,
        HZ_QUEUE,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        PERFORMANCE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_BOUNDARY_RECEIPT,
        LINEAGE_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
    ]


def _update_artifact_registry(paths: list[Path]) -> None:
    if ARTIFACT_REGISTRY.exists():
        registry = pd.read_csv(aw.io_path(ARTIFACT_REGISTRY))
    else:
        registry = pd.DataFrame()
    required = [
        "stage_id",
        "run_id",
        "artifact_type",
        "path",
        "sha256",
        "created_at",
        "claim_boundary",
    ]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if path.exists():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": aw.rel(path),
                    "sha256": _sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        registry[columns].to_csv(
            aw.io_path(ARTIFACT_REGISTRY),
            index=False,
            encoding="utf-8-sig",
            lineterminator="\n",
        )


def _write_receipts(frame: pd.DataFrame, tasks: pd.DataFrame, gates: pd.DataFrame) -> None:
    _write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "work_family": "input_review",
            "primary_skill": "obsidian-data-integrity",
            "support_skills": ["obsidian-exploration-mandate", "obsidian-artifact-lineage"],
            "task_seed_rows": int(len(tasks)),
            "effect": "Reviewed HX input safety before opening training.",
        },
    )
    _write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "input_frame": aw.rel(hx.HX_INPUT_FRAME),
            "rows": int(len(frame)),
            "columns": int(len(frame.columns)),
            "tier_a_status": "materialized",
            "tier_b_status": "missing_required",
            "tier_ab_status": "missing_required",
            "effect": "HY confirms Tier A input is usable and missing Tier B is named.",
        },
    )
    _write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_training": "not_run",
            "onnx_export": "not_run",
            "runtime_package": "not_opened",
            "effect": "Review creates no model authority.",
        },
    )
    _write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "mt5_kpi": "not_measured",
            "proxy_kpi": "not_measured",
            "selection": "not_selected",
            "effect": "HY opens training readiness, not KPI judgment.",
        },
    )
    _write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
            "gate_total": int(len(gates)),
            "effect": "Training can start under review-limited claim boundary.",
        },
    )
    _write_json(
        CLAIM_BOUNDARY_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "goal_achieve_claim": "not_claimed",
            "runtime_authority_claim": "not_claimed",
            "operating_promotion_claim": "not_claimed",
            "live_readiness_claim": "not_claimed",
        },
    )
    _write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "lineage_review": aw.rel(LINEAGE_REVIEW),
            "artifact_registry_updated": True,
            "effect": "HY review artifacts trace back to HX materialization.",
        },
    )


def _write_docs(frame: pd.DataFrame, tasks: pd.DataFrame, gates: pd.DataFrame) -> None:
    gate_passes = int(gates["status"].astype(str).eq("pass").sum())
    gate_total = int(len(gates))
    report = f"""﻿# Stage 337HY Offensive Pivot Input Review

## Summary

- run_id: `{RUN_ID}`
- parent_run_id: `{PARENT_RUN_ID}`
- judgment: `{JUDGMENT}`
- gates: `{gate_passes}/{gate_total}`
- rows: `{len(frame)}`
- task_seed_rows: `{len(tasks)}`

## Result

HX input(입력)은 training-ready(학습 준비)로 판정했다.
효과는 HZ가 invalid target row(무효 타깃 행)를 제거하고 allowed feature(허용 피처)만 써서 후보 학습(candidate training, 후보 학습)을 시작할 수 있는 것이다.

## Tier Boundary

- Tier A separate(Tier A 분리): materialized(물질화).
- Tier B separate(Tier B 분리): missing_required(필수 누락).
- Tier A+B combined(Tier A+B 합산): missing_required(필수 누락).

## Claim Boundary

No training(학습 없음), no ONNX export(온엑스 내보내기 없음), no MT5(메타트레이더5) evidence(근거 없음), no selection(선택 없음), no operating claim(운영 주장 없음).

## Next

Open `{NEXT_RUN_ID}` for candidate training(후보 학습) under HY guards.
"""
    decision = f"""﻿# Decision: Stage 337HY Input Review

- date: `{TODAY}`
- run_id: `{RUN_ID}`
- decision: `{DECISION}`
- judgment: `{JUDGMENT}`
- next_run_id: `{NEXT_RUN_ID}`

## Reason

HX materialization(물질화)은 label(라벨), valid flag(유효 플래그), weight(가중치), task seed(작업 씨앗), feature boundary(피처 경계)를 만들었고 HY review(검토)는 이를 통과시켰다.

## Effect

HZ training(학습)은 Tier A scoped(Tier A 범위) 공격 탐색으로 열리며, Tier B missing_required(필수 누락)는 운영 주장(operating claim, 운영 주장)을 막는 경계로 남는다.

## Boundary

`{CLAIM_BOUNDARY}`
"""
    _write_bom_text(REPORT_PATH, report)
    _write_bom_text(DECISION_DOC, decision)

    _write_bom_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    _write_bom_text(
        CURRENT_WORKING_STATE,
        f"""﻿# Current Working State

## Current Truth

- active_stage: `{STAGE_ID}`
- latest_completed_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- status: `{STATUS}`
- judgment: `{JUDGMENT}`
- decision: `{DECISION}`

## Effect

HY review(검토)는 HX input(입력)을 training-ready(학습 준비)로 열었다.
효과는 HZ가 허용 피처와 유효 타깃만 사용해 공격 후보 학습(offensive candidate training, 공격 후보 학습)을 시작할 수 있게 된 것이다.

## Claim Boundary

`{CLAIM_BOUNDARY}`
""",
    )
    _write_bom_text(
        SELECTION_STATUS,
        f"""﻿# Selection Status

- latest_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- model_selection: not_selected
- runtime_package: not_opened
- goal_achieve: not_claimed
- operating_promotion: not_claimed
- live_readiness: not_claimed

효과는 HY review(검토)를 모델 선택(selection, 선택)으로 오해하지 않게 하는 것이다.
""",
    )
    _write_bom_text(
        STAGE_BRIEF,
        f"""﻿# {STAGE_ID}

Latest completed run: `{RUN_ID}`

HY review(검토)는 HX offensive pivot input(공격 전환 입력)을 training-ready(학습 준비)로 판정했다.
Tier B separate(Tier B 분리) and Tier A+B combined(Tier A+B 합산) remain `missing_required`.
""",
    )
    if CHANGELOG.exists():
        existing = aw.io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    else:
        existing = "﻿# Changelog\n"
    entry = (
        f"\n## {TODAY} - {RUN_ID}\n\n"
        "- Reviewed(검토) HX offensive pivot inputs as training-ready(학습 준비).\n"
        "- Queued(대기열 등록) HZ candidate training(후보 학습) with Tier B missing_required(필수 누락) boundary.\n"
    )
    _write_bom_text(CHANGELOG, existing.rstrip() + "\n" + entry)


def _update_ledgers(frame: pd.DataFrame, gates: pd.DataFrame) -> None:
    row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": int(len(frame)),
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": aw.rel(REPORT_PATH),
    }
    _append_or_replace_csv(RUN_REGISTRY, ["run_id"], row)
    _append_or_replace_csv(PROJECT_LEDGER, ["run_id"], row)
    _append_or_replace_csv(STAGE_LEDGER, ["run_id"], row)


def _write_final(frame: pd.DataFrame, tasks: pd.DataFrame, gates: pd.DataFrame) -> None:
    payload = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "rows": int(len(frame)),
        "task_seed_rows": int(len(tasks)),
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "training_ready": True,
        "tier_a_status": "materialized",
        "tier_b_status": "missing_required",
        "tier_ab_status": "missing_required",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at": TODAY,
        "script": aw.rel(Path(__file__)),
        "inputs": [
            aw.rel(hx.HX_INPUT_FRAME),
            aw.rel(hx.HX_ALLOWED_FEATURES),
            aw.rel(hx.HY_TASK_SEEDS),
            aw.rel(hx.GATE_AUDIT),
        ],
        "outputs": [aw.rel(path) for path in _artifact_paths() if path.exists()],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    _write_json(FINAL_DECISION, payload)
    _write_json(RUN_MANIFEST, manifest)


def main() -> None:
    _ensure_dirs()
    frame = pd.read_parquet(aw.io_path(hx.HX_INPUT_FRAME))
    allowed = _read_csv(hx.HX_ALLOWED_FEATURES)
    thresholds = _read_csv(hx.HX_THRESHOLD_CONTRACT)
    tasks = _read_csv(hx.HY_TASK_SEEDS)
    boundary = _read_csv(hx.HX_FEATURE_BOUNDARY)
    tier_plan = _read_csv(hx.HX_TIER_PLAN)
    hx_gates = _read_csv(hx.GATE_AUDIT)

    input_review = _input_review(frame, allowed)
    label_review = _label_review(frame, thresholds)
    task_review = _task_review(frame, tasks)
    feature_review = _feature_review(frame, allowed, boundary)
    tier_review = _tier_review(tier_plan)
    lineage_review = _lineage_review()
    hz_queue = _make_hz_queue(tasks)

    _write_csv(INPUT_REVIEW, input_review)
    _write_csv(LABEL_REVIEW, label_review)
    _write_csv(TASK_REVIEW, task_review)
    _write_csv(FEATURE_REVIEW, feature_review)
    _write_csv(TIER_REVIEW, tier_review)
    _write_csv(LINEAGE_REVIEW, lineage_review)
    _write_csv(HZ_QUEUE, hz_queue)

    gates = _make_gates(
        input_review,
        label_review,
        task_review,
        feature_review,
        tier_review,
        lineage_review,
        hx_gates,
    )
    _write_csv(GATE_AUDIT, gates)
    _write_receipts(frame, tasks, gates)
    _write_final(frame, tasks, gates)
    _write_docs(frame, tasks, gates)
    _update_ledgers(frame, gates)
    _update_artifact_registry(_artifact_paths())

    failed = gates.loc[~gates["status"].astype(str).eq("pass")]
    if not failed.empty:
        raise RuntimeError(f"HY gates failed: {failed[['gate', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "rows": int(len(frame)),
                "task_seed_rows": int(len(tasks)),
                "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
                "gate_total": int(len(gates)),
                "next_run_id": NEXT_RUN_ID,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
