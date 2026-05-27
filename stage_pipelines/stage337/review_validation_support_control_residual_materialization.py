from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import materialize_validation_support_control_residual_repair_inputs as dr  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
)


TODAY = "2026-05-28"
STAGE_ID = dr.STAGE_ID
RUN_NUMBER = "run337DS"
RUN_ID = "run337DS_review_validation_support_control_residual_materialization_without_db_v1"
PARENT_RUN_ID = dr.RUN_ID
NEXT_RUN_ID = "run337DT_design_broad_validation_failure_control_residual_repair_without_db_v1"
STATUS = "completed_stage337DS_row_level_materialization_review_broad_validation_and_shifted_control_blocks_release_no_selection_no_mt5"
JUDGMENT = "broad_validation_failure_and_shifted_control_residual_require_repair_design"
DECISION = "stage337DS_open_run337DT_design_broad_validation_failure_control_residual_repair"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DS_validation_support_control_residual_materialization_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dr.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dr.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DS_row_level_materialization_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DS_row_level_materialization_review.md"
SELECTED_STATUS = dr.SELECTED_STATUS
STAGE_BRIEF = dr.STAGE_BRIEF
WORKSPACE_STATE = dr.WORKSPACE_STATE
CURRENT_STATE = dr.CURRENT_STATE
CHANGELOG = dr.CHANGELOG
RUN_REGISTRY = dr.RUN_REGISTRY
ALPHA_LEDGER = dr.ALPHA_LEDGER
ARTIFACT_REGISTRY = dr.ARTIFACT_REGISTRY
STAGE_LEDGER = dr.STAGE_LEDGER

DR_FINAL = dr.FINAL_DECISION
DR_GATES = dr.REQUIRED_GATE_AUDIT
DR_QUEUE = dr.DS_QUEUE
PREDICTION_TAPE = dr.ALL_MODEL_PREDICTION_TAPE
VALIDATION_SLICES = dr.VALIDATION_CURVE_POCKET_SLICES
CONTROL_TAPE = dr.SHIFTED_CONTROL_RESIDUAL_TAPE
QUARANTINE_LEDGER = dr.OOS_QUARANTINE_LEDGER
FIREWALL_CARRY = dr.RUNTIME_FIREWALL_CARRY
MATERIALIZATION_SUMMARY = dr.MATERIALIZATION_SUMMARY

TAPE_INTEGRITY_REVIEW = RUN_DIR / "prediction_tape_integrity_review.csv"
VALIDATION_POCKET_REVIEW = RUN_DIR / "validation_curve_pocket_review.csv"
CONTROL_RESIDUAL_REVIEW = RUN_DIR / "control_residual_review.csv"
QUARANTINE_FIREWALL_REVIEW = RUN_DIR / "quarantine_firewall_review.csv"
DT_QUEUE = RUN_DIR / "run337DT_repair_design_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DR_FINAL,
    DR_GATES,
    DR_QUEUE,
    PREDICTION_TAPE,
    VALIDATION_SLICES,
    CONTROL_TAPE,
    QUARANTINE_LEDGER,
    FIREWALL_CARRY,
    MATERIALIZATION_SUMMARY,
)
OUTPUT_FILES = (
    TAPE_INTEGRITY_REVIEW,
    VALIDATION_POCKET_REVIEW,
    CONTROL_RESIDUAL_REVIEW,
    QUARANTINE_FIREWALL_REVIEW,
    DT_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    REQUIRED_GATE_AUDIT,
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

INTEGRITY_COLUMNS = (
    "review_id",
    "rows",
    "expected_rows",
    "model_rows",
    "split_values",
    "duplicate_model_source_rows",
    "missing_probability_rows",
    "review_status",
    "effect",
    "claim_boundary",
)
POCKET_COLUMNS = (
    "review_id",
    "slice_family",
    "slice_rows",
    "weak_slice_rows",
    "weak_slice_ratio",
    "worst_model_id",
    "worst_slice_value",
    "worst_net_log_return_after_cost",
    "worst_profit_factor",
    "review_status",
    "effect",
    "claim_boundary",
)
CONTROL_COLUMNS = (
    "review_id",
    "split",
    "control_id",
    "rows",
    "block_rows",
    "affected_model_count",
    "max_control_alignment",
    "blocked_models",
    "review_status",
    "effect",
    "claim_boundary",
)
QUARANTINE_COLUMNS = (
    "review_id",
    "rows",
    "coverage_status",
    "blocked_action",
    "review_status",
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
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def load_frames() -> dict[str, pd.DataFrame]:
    return {
        "tape": pd.read_parquet(io_path(PREDICTION_TAPE)),
        "slices": pd.read_csv(io_path(VALIDATION_SLICES)),
        "controls": pd.read_csv(io_path(CONTROL_TAPE)),
        "quarantine": pd.read_csv(io_path(QUARANTINE_LEDGER)),
        "firewall": pd.read_csv(io_path(FIREWALL_CARRY)),
        "summary": pd.read_csv(io_path(MATERIALIZATION_SUMMARY)),
    }


def build_integrity_review(frames: Mapping[str, pd.DataFrame], dr_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    tape = frames["tape"]
    duplicate_rows = int(tape.duplicated(["model_id", "source_row_id"]).sum())
    probability_cols = ["prob_short", "prob_flat", "prob_long"]
    missing_prob = int(tape[probability_cols].isna().any(axis=1).sum())
    expected = as_int(dr_final.get("expected_prediction_tape_rows"))
    status = "tape_integrity_passed" if len(tape) == expected and duplicate_rows == 0 and missing_prob == 0 else "tape_integrity_block"
    return [
        {
            "review_id": "all_model_prediction_tape_integrity",
            "rows": len(tape),
            "expected_rows": expected,
            "model_rows": tape["model_id"].nunique(),
            "split_values": ";".join(sorted(tape["split"].astype(str).unique())),
            "duplicate_model_source_rows": duplicate_rows,
            "missing_probability_rows": missing_prob,
            "review_status": status,
            "effect": "checks row-level materialization before interpretation(해석 전 행 단위 물질화 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_pocket_review(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    slices = frames["slices"].copy()
    slices["is_weak"] = slices["slice_status"].astype(str).eq("weak_validation_slice")
    rows: list[dict[str, Any]] = []
    for family, group in slices.groupby("slice_family", dropna=False):
        weak = group.loc[group["is_weak"]]
        worst = group.sort_values("net_log_return_after_cost", ascending=True).iloc[0].to_dict()
        weak_ratio = float(len(weak) / len(group)) if len(group) else 0.0
        if weak_ratio >= 0.75:
            status = "broad_validation_failure"
        elif weak_ratio >= 0.35:
            status = "mixed_validation_failure"
        else:
            status = "localized_validation_failure"
        rows.append(
            {
                "review_id": f"validation_pocket__{family}",
                "slice_family": family,
                "slice_rows": len(group),
                "weak_slice_rows": len(weak),
                "weak_slice_ratio": weak_ratio,
                "worst_model_id": worst.get("model_id", ""),
                "worst_slice_value": worst.get("slice_value", ""),
                "worst_net_log_return_after_cost": as_float(worst.get("net_log_return_after_cost")),
                "worst_profit_factor": as_float(worst.get("profit_factor")),
                "review_status": status,
                "effect": "classifies validation weakness breadth(검증 약점 폭 분류)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    all_weak_ratio = float(slices["is_weak"].mean()) if len(slices) else 0.0
    worst_all = slices.sort_values("net_log_return_after_cost", ascending=True).iloc[0].to_dict()
    rows.append(
        {
            "review_id": "validation_pocket__all",
            "slice_family": "all",
            "slice_rows": len(slices),
            "weak_slice_rows": int(slices["is_weak"].sum()),
            "weak_slice_ratio": all_weak_ratio,
            "worst_model_id": worst_all.get("model_id", ""),
            "worst_slice_value": worst_all.get("slice_value", ""),
            "worst_net_log_return_after_cost": as_float(worst_all.get("net_log_return_after_cost")),
            "worst_profit_factor": as_float(worst_all.get("profit_factor")),
            "review_status": "broad_validation_failure" if all_weak_ratio >= 0.75 else "mixed_validation_failure",
            "effect": "overall validation weakness breadth(전체 검증 약점 폭)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_control_review(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    controls = frames["controls"].copy()
    controls["block_bool"] = controls["blocks_review"].astype(str).str.lower().eq("true")
    rows: list[dict[str, Any]] = []
    for (split, control_id), group in controls.groupby(["split", "control_id"], dropna=False):
        blocked = group.loc[group["block_bool"]]
        blocked_models = sorted(blocked["model_id"].astype(str).unique())
        status = "control_blocks_release" if len(blocked) else "control_clear"
        rows.append(
            {
                "review_id": f"control__{split}__{control_id}",
                "split": split,
                "control_id": control_id,
                "rows": len(group),
                "block_rows": len(blocked),
                "affected_model_count": len(blocked_models),
                "max_control_alignment": float(pd.to_numeric(group["control_alignment_balanced_accuracy"], errors="coerce").max()),
                "blocked_models": ";".join(blocked_models),
                "review_status": status,
                "effect": "reviews residual control alignment(잔여 대조 정렬 검토)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_quarantine_review(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    quarantine = frames["quarantine"]
    firewall = frames["firewall"]
    return [
        {
            "review_id": "oos_quarantine_coverage",
            "rows": len(quarantine),
            "coverage_status": "complete" if len(quarantine) == 10 else "incomplete",
            "blocked_action": "candidate_selection;mt5_queue",
            "review_status": "quarantine_preserved_no_release",
            "effect": "keeps OOS-only lift out of release(OOS 단독 개선을 해제 밖에 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "runtime_firewall_carry",
            "rows": len(firewall),
            "coverage_status": "complete" if len(firewall) >= 3 else "incomplete",
            "blocked_action": "MT5;Forward;runtime_authority",
            "review_status": "firewall_preserved_no_release",
            "effect": "keeps operating claims closed(운영 주장 닫힘 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_dt_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DT_design_broad_validation_failure_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design broad validation failure repair(넓은 검증 실패 수리 설계)",
            "required_inputs": rel(VALIDATION_POCKET_REVIEW),
            "required_outputs": "broad_validation_failure_repair_design.csv",
            "blocked_if_missing": "validation curve pocket review(검증 곡선 포켓 검토)",
            "forbidden_action": "no slice filter mining or candidate selection(슬라이스 필터 채굴 또는 후보 선택 금지)",
            "effect": "turns broad weakness into repair constraints(넓은 약점을 수리 제약으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DT_design_shifted_control_technical_et_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design shifted-control residual repair for technical ExtraTrees(technical ExtraTrees 이동 대조 잔차 수리 설계)",
            "required_inputs": rel(CONTROL_RESIDUAL_REVIEW),
            "required_outputs": "shifted_control_residual_repair_design.csv",
            "blocked_if_missing": "control residual review(대조 잔차 검토)",
            "forbidden_action": "no control threshold relaxation(대조 임계값 완화 금지)",
            "effect": "keeps serial residual as blocker(연속 잔차를 차단 사유로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DT_design_family_scope_constraints",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "design feature/model family scope constraints without selecting winners(승자 선택 없이 피처/모델 계열 범위 제약 설계)",
            "required_inputs": f"{rel(VALIDATION_POCKET_REVIEW)};{rel(CONTROL_RESIDUAL_REVIEW)}",
            "required_outputs": "family_scope_constraint_design.csv",
            "blocked_if_missing": "pocket/control reviews(포켓/대조 검토)",
            "forbidden_action": "no winner pruning as selection(선택성 승자 가지치기 금지)",
            "effect": "turns weak families into constraints, not selected winners(약한 계열을 선택이 아닌 제약으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DT_preserve_no_release_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "preserve no-release firewall(무해제 방화벽 보존)",
            "required_inputs": rel(QUARANTINE_FIREWALL_REVIEW),
            "required_outputs": "no_release_firewall_design.csv",
            "blocked_if_missing": "quarantine/firewall review(격리/방화벽 검토)",
            "forbidden_action": "no MT5/Forward claim(MT5/전진 주장 금지)",
            "effect": "keeps runtime boundary closed(런타임 경계 닫힘 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DR outputs exist(필수 DR 출력 존재)"),
        ("parent_dr_gates_passed", final["dr_failed_gate_rows"] == 0, str(final["dr_failed_gate_rows"]), "0", "DR materialization usable(DR 물질화 사용 가능)"),
        ("parent_next_action_matches", final["dr_next_action"] == RUN_ID, str(final["dr_next_action"]), RUN_ID, "continues DR queue(DR 대기열을 이어감)"),
        ("prediction_tape_integrity_passed", final["duplicate_model_source_rows"] == 0 and final["missing_probability_rows"] == 0, f"dup={final['duplicate_model_source_rows']};missing_prob={final['missing_probability_rows']}", "0/0", "tape integrity clear(테이프 무결성 통과)"),
        ("broad_validation_failure_recorded", final["overall_weak_slice_ratio"] >= 0.75, str(final["overall_weak_slice_ratio"]), ">=0.75", "broad validation failure named(넓은 검증 실패 명명)"),
        ("control_blocks_recorded", final["control_block_rows"] == 3, str(final["control_block_rows"]), "3", "shifted-control blockers recorded(이동 대조 차단 기록)"),
        ("quarantine_firewall_reviewed", final["quarantine_rows"] == 10 and final["firewall_rows"] >= 3, f"quarantine={final['quarantine_rows']};firewall={final['firewall_rows']}", "10/>=3", "quarantine and firewall preserved(격리와 방화벽 보존)"),
        ("dt_queue_materialized", final["dt_queue_rows"] == 4, str(final["dt_queue_rows"]), "4", "DT design queue opened(DT 설계 대기열 열림)"),
        (
            "no_forbidden_claim",
            final["model_training"] == "not_run"
            and final["candidate_selection"] == "not_run"
            and final["mt5_runtime_probe"] == "not_run"
            and final["goal_achieve"] == "not_claimed",
            f"training={final['model_training']};selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            "claim boundary preserved(주장 경계 보존)",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherits DR source_row_id UTC row tape(DR source_row_id UTC 행 테이프 상속)",
        "sample_scope": f"tape_rows={final['tape_rows']};slice_rows={final['slice_rows']}",
        "missing_or_duplicate_check": f"duplicate_model_source_rows={final['duplicate_model_source_rows']};missing_probability_rows={final['missing_probability_rows']}",
        "feature_label_boundary": "review-only; no feature/label recomputation(검토 전용, 피처/라벨 재계산 없음)",
        "split_boundary": "validation/OOS row tape review(검증/OOS 행 테이프 검토)",
        "leakage_risk": "turning weak slices into release filters(약한 슬라이스를 해제 필터로 바꾸는 위험)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_review_no_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "review-only of DR row-level predictions(DR 행 단위 예측 검토 전용)",
        "target_and_label": "unchanged DO costed labels(DO 비용 반영 라벨 유지)",
        "split_method": "validation/OOS review only(검증/OOS 검토 전용)",
        "selection_metric": "none; release blocked(없음, 해제 차단)",
        "secondary_metrics": "weak slice ratio, shifted control blocks, quarantine coverage(약한 슬라이스 비율/이동 대조 차단/격리 커버리지)",
        "threshold_policy": "no threshold tuning(임계값 튜닝 없음)",
        "overfit_risk": "slice-mining from row tape(행 테이프 슬라이스 채굴)",
        "calibration_risk": "probabilities remain diagnostic(확률은 진단 전용)",
        "comparison_baseline": rel(DR_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"overall_weak_slice_ratio={final['overall_weak_slice_ratio']};control_block_rows={final['control_block_rows']}",
        "comparison_baseline": rel(DR_FINAL),
        "likely_drivers": "broad validation weakness plus technical ExtraTrees shifted residual(넓은 검증 약점과 technical ExtraTrees 이동 잔차)",
        "segment_checks": f"pocket_review_rows={final['pocket_review_rows']};control_review_rows={final['control_review_rows']}",
        "trade_shape": f"worst_net={final['worst_net_log_return_after_cost']};worst_pf={final['worst_profit_factor']}",
        "alternative_explanations": "proxy cost mismatch, regime shift, class imbalance(프록시 비용 불일치/레짐 전환/클래스 불균형)",
        "attribution_confidence": "medium_for_proxy_review_low_for_runtime(프록시 검토 중간, 런타임 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "integrity, pocket, control, quarantine/firewall reviews(무결성/포켓/대조/격리 방화벽 검토)",
        "evidence_missing": "DT repair design, repaired materialization/training, MT5, forward evidence(DT 수리 설계/수리 물질화/학습/MT5/전진 근거)",
        "judgment_label": "broad_failure_repair_design_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "행 단위로 봐도 검증 실패가 넓다. 이제 승자 고르기가 아니라 넓은 실패 구조를 수리해야 한다.",
    }
    paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in list(artifact_paths) + paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_review_outputs_with_tracked_report(무시된 검토 산출물과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DS Row-Level Materialization Review(행 단위 물질화 검토)

## Conclusion(결론)

run337DS(337DS 실행)는 run337DR(337DR 실행)의 prediction tape(예측 테이프), validation pockets(검증 포켓), shifted-control residuals(이동 대조 잔차), quarantine/firewall(격리/방화벽)을 검토했다.

판정은 broad validation failure(넓은 검증 실패)다. weak validation slice ratio(약한 검증 슬라이스 비율)가 `{final["overall_weak_slice_ratio"]}`이고, shifted-control blockers(이동 대조 차단)는 `3`개다.

Effect(효과): run337DT(337DT 실행)는 넓은 검증 실패와 technical ExtraTrees shifted residual(technical ExtraTrees 이동 잔차)을 수리 설계로 다룬다. 선택/MT5/Forward(전진)는 계속 닫는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- tape_rows(테이프 행): `{final["tape_rows"]}`
- overall_weak_slice_ratio(전체 약한 슬라이스 비율): `{final["overall_weak_slice_ratio"]}`
- worst_net_log_return_after_cost(최악 비용 후 로그수익): `{final["worst_net_log_return_after_cost"]}`
- worst_profit_factor(최악 PF): `{final["worst_profit_factor"]}`
- control_block_rows(대조 차단 행): `{final["control_block_rows"]}`
- quarantine_rows(격리 행): `{final["quarantine_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DS

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 행 단위 검토에서 넓은 검증 실패와 이동 대조 잔차를 확인했고, 선택/MT5/Forward(전진)는 계속 닫는다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(VALIDATION_POCKET_REVIEW)}`, `{rel(CONTROL_RESIDUAL_REVIEW)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337DS focus complete: row-level materialization review(행 단위 물질화 검토)를 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DT(337DT 실행)에서 broad validation failure/control residual repair design(넓은 검증 실패/대조 잔차 수리 설계)을 연다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DS focus complete")
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{STATUS}`",
        "decision": f"`{DECISION}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""## Stage337 run337DS(337DS 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 넓은 검증 실패와 이동 대조 잔차를 확인했지만 선택/MT5/Forward(전진)는 주장하지 않는다. Goal(목표)은 주장하지 않는다."""
    current_text = append_once(current_text, section, "Stage337 run337DS(337DS 실행)")
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection_text, _ = read_text_lossless(SELECTED_STATUS)
    selection = selection_text
    for field_name, value in {
        "latest_run": f"`{RUN_ID}`",
        "latest_decision": f"`{DECISION}`",
        "current_run": f"`{NEXT_RUN_ID}`",
        "rebuild_status": f"`{STATUS}`",
        "actual_mt5_execution": "`not_run_ds_review_only`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "effect": "`다음은 broad validation failure/control residual repair design(넓은 검증 실패/대조 잔차 수리 설계)이다.`",
    }.items():
        selection = replace_bullet_value(selection, field_name, value)
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337DS(337DS 실행) reviewed row-level materialization, blocked release on broad validation failure/control residual, and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DS(337DS 실행) reviewed row-level materialization"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337DS reviewed row-level materialization and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DS reviewed row-level materialization"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "validation_support_control_residual_materialization_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"weak_slice_ratio={final['overall_weak_slice_ratio']};control_blocks={final['control_block_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__row_level_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "row_level_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_training_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "row_level_proxy_review",
        "scoreboard_lane": "model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"weak_slice_ratio={final['overall_weak_slice_ratio']};control_blocks={final['control_block_rows']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__row_level_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_performance_attribution_result_judgment",
        "evidence_scope": "row-level materialization reviewed",
        "kpi_scope": "weak_slice_ratio_control_blocks_quarantine",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__row_level_review",
        "family": "model_validation_performance_attribution_result_judgment",
        "question": "is validation failure localized or broad after row-level materialization",
        "metric_scope": "weak_slice_ratio_control_blocks",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    artifacts = [
        upsert_csv(RUN_REGISTRY, "run_id", run_row),
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row),
        upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row),
    ]
    artifact_columns: list[str] = []
    artifact_rows: list[dict[str, str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            artifact_columns = list(reader.fieldnames or [])
            artifact_rows = [dict(row) for row in reader]
    if not artifact_columns:
        artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    frames = load_frames()
    dr_final = read_json(DR_FINAL)
    integrity_rows = build_integrity_review(frames, dr_final)
    pocket_rows = build_pocket_review(frames)
    control_rows = build_control_review(frames)
    quarantine_rows = build_quarantine_review(frames)
    queue_rows = build_dt_queue()

    overall = next(row for row in pocket_rows if row["slice_family"] == "all")
    control_block_rows = sum(as_int(row["block_rows"]) for row in control_rows)
    dr_failed_gate_rows = sum(1 for row in read_csv(DR_GATES) if row.get("status") != "passed")
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dr_next_action": dr_final.get("next_action", ""),
        "dr_failed_gate_rows": dr_failed_gate_rows,
        "missing_inputs": len(missing),
        "tape_rows": len(frames["tape"]),
        "slice_rows": len(frames["slices"]),
        "duplicate_model_source_rows": as_int(integrity_rows[0]["duplicate_model_source_rows"]),
        "missing_probability_rows": as_int(integrity_rows[0]["missing_probability_rows"]),
        "pocket_review_rows": len(pocket_rows),
        "overall_weak_slice_ratio": as_float(overall["weak_slice_ratio"]),
        "overall_weak_slice_rows": as_int(overall["weak_slice_rows"]),
        "worst_net_log_return_after_cost": as_float(overall["worst_net_log_return_after_cost"]),
        "worst_profit_factor": as_float(overall["worst_profit_factor"]),
        "control_review_rows": len(control_rows),
        "control_block_rows": control_block_rows,
        "quarantine_rows": len(frames["quarantine"]),
        "firewall_rows": len(frames["firewall"]),
        "dt_queue_rows": len(queue_rows),
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
    }
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts: list[Path] = [
        write_csv(TAPE_INTEGRITY_REVIEW, INTEGRITY_COLUMNS, integrity_rows),
        write_csv(VALIDATION_POCKET_REVIEW, POCKET_COLUMNS, pocket_rows),
        write_csv(CONTROL_RESIDUAL_REVIEW, CONTROL_COLUMNS, control_rows),
        write_csv(QUARANTINE_FIREWALL_REVIEW, QUARANTINE_COLUMNS, quarantine_rows),
        write_csv(DT_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
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
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
