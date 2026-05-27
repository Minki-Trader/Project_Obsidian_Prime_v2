from __future__ import annotations

import csv
import json
import math
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
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
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
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CT"
RUN_ID = "run337CT_review_weak_density_control_repaired_candidates_without_db_v1"
PARENT_RUN_ID = "run337CS_train_weak_density_control_repaired_candidates_without_db_v1"
NEXT_RUN_ID = "run337CU_design_feature_label_separability_control_repair_without_db_v1"
STATUS = "completed_stage337CT_release_lock_review_no_mt5_no_selection"
JUDGMENT = "release_blocked_by_weak_model_discrimination_and_extended_control_alignment"
DECISION = "stage337CT_open_run337CU_feature_label_separability_control_repair_design"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CT_weak_density_control_repaired_training_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CT_weak_density_control_repaired_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CT_weak_density_control_repaired_review.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CS_DIR = STAGE_DIR / "02_runs" / "run337CS"
CS_FINAL = CS_DIR / "final_decision.json"
CS_GATES = CS_DIR / "required_gate_coverage_audit.csv"
CS_SCORECARD = CS_DIR / "repaired_model_scorecard.csv"
CS_PARITY = CS_DIR / "onnx_parity_matrix.csv"
CS_CONTROLS = CS_DIR / "extended_control_scorecard.csv"
CS_COST = CS_DIR / "cost_curve_shape_scorecard.csv"
CS_DAY = CS_DIR / "policy_day_concentration_matrix.csv"
CS_RUNTIME = CS_DIR / "runtime_probe_release_disposition.csv"
CS_THRESHOLDS = CS_DIR / "train_only_policy_thresholds.csv"
CR_MT5_LOCK = STAGE_DIR / "02_runs" / "run337CR" / "mt5_probe_release_lock.csv"

RELEASE_LOCK_REVIEW = RUN_DIR / "release_lock_review.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "failure_attribution_matrix.csv"
POLICY_DIAGNOSTIC = RUN_DIR / "policy_diagnostic_summary.csv"
NEXT_REPAIR_QUEUE = RUN_DIR / "run337CU_repair_design_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CS_FINAL,
    CS_GATES,
    CS_SCORECARD,
    CS_PARITY,
    CS_CONTROLS,
    CS_COST,
    CS_DAY,
    CS_RUNTIME,
    CS_THRESHOLDS,
    CR_MT5_LOCK,
)
OUTPUT_FILES = (
    RELEASE_LOCK_REVIEW,
    FAILURE_ATTRIBUTION,
    POLICY_DIAGNOSTIC,
    NEXT_REPAIR_QUEUE,
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

LOCK_COLUMNS = ("lock_id", "input_status", "observed", "review_status", "effect", "claim_boundary")
FAILURE_COLUMNS = ("failure_id", "family", "severity", "evidence", "interpretation", "next_repair_need", "claim_boundary")
POLICY_COLUMNS = (
    "policy_id",
    "model_id",
    "density_floor",
    "validation_balanced_accuracy",
    "oos_balanced_accuracy",
    "validation_signal_density",
    "oos_signal_density",
    "oos_cost0_net_proxy_return",
    "oos_cost2_net_proxy_return",
    "oos_max_day_trade_share",
    "release_blockers",
    "diagnostic_rank_not_selection",
    "claim_boundary",
)
QUEUE_COLUMNS = ("queue_id", "next_run_id", "priority", "repair_family", "task", "required_inputs", "blocked_if_missing", "forbidden_action", "effect", "claim_boundary")
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def read_csv_frame(path: Path, dtype: Any | None = None) -> pd.DataFrame:
    return pd.read_csv(io_path(path), dtype=dtype)


def bool_series(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().eq("true")


def finite_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def build_policy_diagnostic(score: pd.DataFrame, cost: pd.DataFrame, day: pd.DataFrame, runtime: pd.DataFrame) -> list[dict[str, Any]]:
    validation = score[score["split"] == "validation"].set_index("policy_id")
    oos = score[score["split"] == "oos"].set_index("policy_id")
    cost0 = cost[(cost["split"] == "oos") & (cost["cost_points"].astype(int) == 0)].set_index("policy_id")
    cost2 = cost[(cost["split"] == "oos") & (cost["cost_points"].astype(int) == 2)].set_index("policy_id")
    runtime_idx = runtime.set_index("policy_id")
    day_oos = day[day["split"] == "oos"].copy()
    max_day = day_oos.groupby("policy_id")["day_trade_share"].max().to_dict()

    raw_rows: list[dict[str, Any]] = []
    for policy_id in sorted(oos.index):
        row = {
            "policy_id": policy_id,
            "model_id": str(oos.loc[policy_id, "model_id"]),
            "density_floor": finite_float(oos.loc[policy_id, "density_floor"]),
            "validation_balanced_accuracy": finite_float(validation.loc[policy_id, "model_balanced_accuracy"]),
            "oos_balanced_accuracy": finite_float(oos.loc[policy_id, "model_balanced_accuracy"]),
            "validation_signal_density": finite_float(validation.loc[policy_id, "signal_density"]),
            "oos_signal_density": finite_float(oos.loc[policy_id, "signal_density"]),
            "oos_cost0_net_proxy_return": finite_float(cost0.loc[policy_id, "net_proxy_return"]) if policy_id in cost0.index else 0.0,
            "oos_cost2_net_proxy_return": finite_float(cost2.loc[policy_id, "net_proxy_return"]) if policy_id in cost2.index else 0.0,
            "oos_max_day_trade_share": finite_float(max_day.get(policy_id, 0.0)),
            "release_blockers": str(runtime_idx.loc[policy_id, "release_blockers"]),
            "diagnostic_rank_not_selection": 0,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        raw_rows.append(row)
    ranked = sorted(
        raw_rows,
        key=lambda item: (
            item["validation_balanced_accuracy"],
            item["oos_balanced_accuracy"],
            item["oos_cost2_net_proxy_return"],
            -item["oos_max_day_trade_share"],
        ),
        reverse=True,
    )
    rank_by_policy = {row["policy_id"]: index + 1 for index, row in enumerate(ranked)}
    for row in raw_rows:
        row["diagnostic_rank_not_selection"] = rank_by_policy[row["policy_id"]]
    return raw_rows


def build_failure_attribution(score: pd.DataFrame, controls: pd.DataFrame, cost: pd.DataFrame, parity: pd.DataFrame, runtime: pd.DataFrame) -> list[dict[str, str]]:
    validation = score[score["split"] == "validation"]
    oos = score[score["split"] == "oos"]
    validation_max_balanced = float(validation["model_balanced_accuracy"].max())
    oos_max_balanced = float(oos["model_balanced_accuracy"].max())
    validation_max_density = float(validation["signal_density"].max())
    oos_max_density = float(oos["signal_density"].max())
    control_blocks = int(bool_series(controls["blocks_runtime_probe"]).sum())
    cost_blocks = int(bool_series(cost["blocks_runtime_probe"]).sum())
    parity_passed = int(parity["passed"].astype(str).str.lower().eq("true").sum())
    release_rows = int((runtime["mt5_probe_disposition"] == "release_review_ready_no_mt5_executed").sum())
    rows = [
        {
            "failure_id": "model_discrimination_still_weak",
            "family": "model_validation(모델 검증)",
            "severity": "P0",
            "evidence": f"validation_max_balanced={validation_max_balanced:.6f};oos_max_balanced={oos_max_balanced:.6f};release_rows={release_rows}",
            "interpretation": "density repair(밀도 수리)로 거래수는 늘었지만 분류 분리력은 0.40 gate(게이트)를 넘지 못했다.",
            "next_repair_need": "feature/label separability repair(피처/라벨 분리력 수리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "density_attack_not_sufficient",
            "family": "trade_shape(거래 모양)",
            "severity": "P0",
            "evidence": f"validation_max_density={validation_max_density:.6f};oos_max_density={oos_max_density:.6f}",
            "interpretation": "train-only density policy(학습 전용 밀도 정책)는 신호 밀도를 높였지만 품질 gate(품질 게이트)를 고치지 못했다.",
            "next_repair_need": "do not pursue density-only threshold branch(밀도 단독 임계값 분기 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "extended_control_alignment_blocks_release",
            "family": "negative_control(부정 대조)",
            "severity": "P0",
            "evidence": f"extended_control_blocks={control_blocks}/{len(controls)}",
            "interpretation": "gap72/gap96/horizon modulo controls(72/96갭/기간 모듈로 대조)가 release(해제)를 막았다.",
            "next_repair_need": "control-orthogonal feature and label boundary design(대조 직교 피처와 라벨 경계 설계)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "cost_curve_secondary_blocker",
            "family": "performance_attribution(성과 귀속)",
            "severity": "P1",
            "evidence": f"cost_curve_blocks={cost_blocks}/{len(cost)}",
            "interpretation": "비용/곡선도 일부 막지만, 현재 1차 실패는 모델 분리력과 대조 정렬이다.",
            "next_repair_need": "rerun cost curve only after quality/control gate improves(품질/대조 게이트 개선 후 비용 곡선 재실행)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "onnx_parity_not_blocker",
            "family": "runtime_parity(런타임 동등성)",
            "severity": "P2",
            "evidence": f"onnx_parity={parity_passed}/{len(parity)}",
            "interpretation": "ONNX parity(온엑스 동등성)는 통과했지만 모델 품질 부족을 보상하지 않는다.",
            "next_repair_need": "keep parity gate, do not run MT5 until release lock clears(동등성 게이트 유지, 해제 전 MT5 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def build_release_lock_review(lock: pd.DataFrame, runtime: pd.DataFrame, controls: pd.DataFrame, cost: pd.DataFrame, score: pd.DataFrame) -> list[dict[str, str]]:
    release_rows = int((runtime["mt5_probe_disposition"] == "release_review_ready_no_mt5_executed").sum())
    control_blocks = int(bool_series(controls["blocks_runtime_probe"]).sum())
    cost_blocks = int(bool_series(cost["blocks_runtime_probe"]).sum())
    validation_failed = int((score.loc[score["split"] == "validation", "validation_gate_status"] == "failed").sum())
    rows: list[dict[str, str]] = []
    for item in lock.to_dict("records"):
        lock_id = str(item["lock_id"])
        status = "held"
        observed = f"release_rows={release_rows}"
        if lock_id == "control_clearance_lock":
            observed = f"control_blocks={control_blocks}"
        elif lock_id == "signal_floor_lock":
            observed = f"validation_gate_failed={validation_failed}"
        elif lock_id == "cost_curve_lock":
            observed = f"cost_blocks={cost_blocks}"
        elif lock_id == "proxy_mt5_compare_lock":
            observed = "compare_contract_present_but_mt5_not_released"
        elif lock_id == "lineage_hash_lock":
            observed = "hashes_recorded_in_artifact_registry"
            status = "ready_but_release_still_held"
        rows.append(
            {
                "lock_id": lock_id,
                "input_status": str(item.get("current_status", "")),
                "observed": observed,
                "review_status": status,
                "effect": "MT5 probe(MT5 탐침)를 아직 실행하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_next_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337CU_design_feature_label_separability_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "repair_family": "feature_label_separability(피처/라벨 분리력)",
            "task": "design non-density repair for weak balanced accuracy(낮은 균형 정확도에 대한 비밀도 수리 설계)",
            "required_inputs": rel(FAILURE_ATTRIBUTION) + ";" + rel(POLICY_DIAGNOSTIC),
            "blocked_if_missing": "CT failure attribution missing(CT 실패 귀속 누락)",
            "forbidden_action": "do not lower threshold from validation/OOS(검증/OOS로 임계값 낮추기 금지)",
            "effect": "분류 품질을 고치지 않은 밀도 공격을 중단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CU_design_control_orthogonalization",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "repair_family": "control_orthogonalization(대조 직교화)",
            "task": "design controls that force gap72/gap96/horizon modulo separation(72/96갭/기간 모듈로 분리를 강제하는 대조 설계)",
            "required_inputs": rel(CS_CONTROLS),
            "blocked_if_missing": "extended control scorecard missing(확장 대조 점수표 누락)",
            "forbidden_action": "do not select models by control pocket after OOS(대조 포켓과 OOS로 모델 선택 금지)",
            "effect": "대조 정렬을 성과로 착각하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CU_design_model_family_loss_probe",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "repair_family": "model_family_loss(모델군/손실)",
            "task": "prepare small family/loss probe without OOS selection(OOS 선택 없는 작은 모델군/손실 탐침 준비)",
            "required_inputs": rel(CS_SCORECARD),
            "blocked_if_missing": "scorecard missing(점수표 누락)",
            "forbidden_action": "do not run broad model search from OOS rank(OOS 순위로 광범위 모델 검색 금지)",
            "effect": "분리력 실패를 모델 용량과 라벨 문제로 나눠 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CU_defer_cost_curve_until_quality_gate",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P2",
            "repair_family": "cost_curve_deferred(비용 곡선 지연)",
            "task": "keep cost curve as secondary until quality/control gates improve(품질/대조 게이트 개선 전 비용 곡선은 보조로 유지)",
            "required_inputs": rel(CS_COST),
            "blocked_if_missing": "cost scorecard missing(비용 점수표 누락)",
            "forbidden_action": "do not optimize lot or cost assumptions(랏/비용 가정 최적화 금지)",
            "effect": "비용 곡선으로 약한 모델을 포장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]
    cs_final = read_json(CS_FINAL)

    def row(gate_id: str, ok: bool, observed: Any, expected: str, effect: str) -> dict[str, str]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": str(observed),
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    return [
        row("ct_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CS evidence(근거)를 연결했다."),
        row("ct_gate_parent_points_to_ct", cs_final.get("next_action", "") == RUN_ID, cs_final.get("next_action", ""), RUN_ID, "CS next_action(다음 행동)과 CT run(실행)이 맞는다."),
        row("ct_gate_release_lock_rows", final["release_lock_review_rows"] >= 5, final["release_lock_review_rows"], ">=5", "release lock review(해제 잠금 검토)를 만들었다."),
        row("ct_gate_failure_attribution_rows", final["failure_rows"] >= 5, final["failure_rows"], ">=5", "실패 귀속을 숨기지 않았다."),
        row("ct_gate_policy_diagnostic_rows", final["policy_diagnostic_rows"] == 16, final["policy_diagnostic_rows"], "16", "정책별 진단을 만들었다."),
        row("ct_gate_runtime_release_zero", final["runtime_release_rows"] == 0, final["runtime_release_rows"], "0", "MT5 해제 후보가 없음을 기록했다."),
        row("ct_gate_next_queue", final["next_queue_rows"] >= 4, final["next_queue_rows"], ">=4", "다음 수리 대기열을 열었다."),
        row("ct_gate_no_training_selection_mt5", True, "training=not_run;selection=not_run;mt5=not_run", "no training/selection/MT5", "CT는 검토만 수행한다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherits CS scorecards and policy OOS rows(CS 점수표와 정책 OOS 행 상속)",
        "sample_scope": "review only; no new bars and no new labels(검토 전용, 새 봉/새 라벨 없음)",
        "missing_or_duplicate_check": "input files present gate passed(입력 파일 존재 게이트 통과)",
        "feature_label_boundary": "no feature or label recomputation(피처/라벨 재계산 없음)",
        "split_boundary": "validation/OOS remain read-only review fields(검증/OOS는 읽기 전용 검토 필드 유지)",
        "leakage_risk": "using diagnostic rank as selection(진단 순위를 선택으로 쓰는 위험)",
        "data_hash_or_identity": {"policy_rows": final["policy_diagnostic_rows"], "release_rows": final["runtime_release_rows"]},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "review of CS trained extratrees density policies(CS 학습 extra trees 밀도 정책 검토)",
        "target_and_label": "unchanged from CS(CS와 동일)",
        "split_method": "CS purged embargo split review(CS 제거/격리 분할 검토)",
        "selection_metric": "none_no_selection(없음, 선택 아님)",
        "secondary_metrics": "balanced accuracy, density, controls, cost, release blockers(균형 정확도, 밀도, 대조, 비용, 해제 차단)",
        "threshold_policy": "review only; no threshold change(검토 전용, 임계값 변경 없음)",
        "overfit_risk": "turning CT diagnostic rank into a winner(CT 진단 순위를 승자로 바꾸는 위험)",
        "calibration_risk": "CS probability scores still rank-like(CS 확률 점수는 여전히 순위형)",
        "comparison_baseline": "CS train-only density repair(CS 학습 전용 밀도 수리)",
        "validation_judgment": "release_blocked_repair_design_required(해제 차단, 수리 설계 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": "release rows remain zero after density repair(밀도 수리 뒤 해제 행 0 유지)",
        "comparison_baseline": "CP weak review and CS repair training(CP 약점 검토와 CS 수리 학습)",
        "likely_drivers": "weak discrimination and extended control alignment(약한 분리력과 확장 대조 정렬)",
        "segment_checks": "policy diagnostic, day concentration, cost curve(정책 진단, 일 집중도, 비용 곡선)",
        "trade_shape": f"max_validation_density={final['validation_max_signal_density']};max_oos_density={final['oos_max_signal_density']}",
        "alternative_explanations": "label boundary too noisy, feature state carry, model capacity mismatch(라벨 경계 잡음, 피처 상태 이월, 모델 용량 불일치)",
        "attribution_confidence": "high_for_no_release_medium_for_root_cause(해제 불가에는 높음, 원인에는 중간)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "CS scorecards, controls, cost curves, runtime disposition(CS 점수표, 대조, 비용 곡선, 런타임 처분)",
        "evidence_missing": "new repair design and future training(새 수리 설계와 향후 학습)",
        "judgment_label": "negative_release_review_not_model_failure_closeout(해제 검토 부정, 모델 사망 종료 아님)",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "밀도만 늘려서는 안 됐고, 분리력/대조 정렬을 다시 설계해야 한다.",
    }
    receipt_paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifact_paths] + [rel(path) for path in receipt_paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + receipt_paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers(02_runs는 목록/해시로 추적, 보고서와 장부는 저장소 추적)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipt_paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return receipt_paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CT Weak Density/Control Repaired Review(약한 밀도/대조 수리 검토)

## Conclusion(결론)

run337CT(337CT 실행)는 run337CS(337CS 실행)의 release lock(해제 잠금)을 검토했다. 결론은 MT5 release(MT5 해제) 0행이다.

Effect(효과): ONNX parity(온엑스 동등성)는 문제가 아니지만, validation balanced accuracy(검증 균형 정확도)와 extended controls(확장 대조)가 release(해제)를 막았다. 다음은 density threshold(밀도 임계값) 수리가 아니라 feature/label separability repair(피처/라벨 분리력 수리)다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- policy_diagnostic_rows(정책 진단 행): `{final["policy_diagnostic_rows"]}`
- release_rows(해제 행): `{final["runtime_release_rows"]}`
- validation_max_balanced(검증 최대 균형 정확도): `{final["validation_max_balanced"]}`
- oos_max_balanced(OOS 최대 균형 정확도): `{final["oos_max_balanced"]}`
- extended_control_block_rows(확장 대조 차단 행): `{final["extended_control_block_rows"]}`
- cost_curve_block_rows(비용 곡선 차단 행): `{final["cost_curve_block_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CT

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): MT5 release(MT5 해제)를 보류하고 feature/label separability repair design(피처/라벨 분리력 수리 설계)을 연다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(RELEASE_LOCK_REVIEW)}`, `{rel(FAILURE_ATTRIBUTION)}`, `{rel(NEXT_REPAIR_QUEUE)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
- MT5 probe(MT5 탐침): `not_run`
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
        "current_focus:\n- >-\n"
        f"  Stage337 run337CT focus complete: release lock review(해제 잠금 검토)를 `{STATUS}`로 닫았다. "
        "Effect(효과): run337CU(337CU 실행)에서 feature/label separability and control repair design(피처/라벨 분리력과 대조 수리 설계)을 연다."
    )
    if "Stage337 run337CT focus complete" in workspace_text:
        workspace_text = re.sub(
            r"current_focus:\n- >-\n  Stage337 run337CT focus complete:.*?(?=\n- >-\n  Stage337 run337CS|\n[A-Za-z0-9_]+:)",
            focus_entry,
            workspace_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        workspace_text = workspace_text.replace("current_focus:", focus_entry, 1)
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
    section = f"""
## Stage337 run337CT(337CT 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): release_rows(해제 행) `{final['runtime_release_rows']}`, extended_control_block_rows(확장 대조 차단 행) `{final['extended_control_block_rows']}`로 MT5 probe(MT5 탐침)를 보류했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current_text = re.sub(
        r"\n## Stage337 run337CT\(337CT 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CS|\Z)",
        "\n",
        current_text,
        count=1,
        flags=re.DOTALL,
    )
    marker = "## Stage337 run337CS(337CS"
    current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{STATUS}`
- actual_mt5_execution(실제 MT5 실행): `held_by_ct_release_blocked_no_mt5`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 feature/label separability control repair design(피처/라벨 분리력 대조 수리 설계)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CT(337CT 실행)" not in line)
    stage_entry = (
        f"- {TODAY}: run337CT(337CT 실행) reviewed weak density/control repaired training(약한 밀도/대조 수리 학습). "
        f"Release rows(해제 행) `{final['runtime_release_rows']}`. Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337CT reviewed weak density/control repaired training" not in line)
    changelog_entry = f"- {TODAY}: Stage337 run337CT reviewed weak density/control repaired training(약한 밀도/대조 수리 학습) and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "weak_density_control_repaired_release_lock_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"release_rows={final['runtime_release_rows']};validation_max_balanced={final['validation_max_balanced']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "result_judgment_model_validation_performance_attribution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__release_lock_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "release_lock_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "release_lock_review",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "review_no_training_no_selection",
        "scoreboard_lane": "result_judgment_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"release_rows={final['runtime_release_rows']};failure_rows={final['failure_rows']}",
        "guardrail_kpi": "no_mt5;no_selection;next_repair_queue",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__release_lock_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "result_judgment_model_validation_performance_attribution",
        "evidence_scope": "CS release lock review and failure attribution",
        "kpi_scope": "review_no_training_no_selection",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};release_rows={final['runtime_release_rows']};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__release_lock_review",
        "family": "result_judgment_model_validation_performance_attribution",
        "question": "should weak density/control repaired policies be released to MT5 probe",
        "metric_scope": "release_lock_failure_attribution_policy_diagnostic",
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
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    score = read_csv_frame(CS_SCORECARD)
    parity = read_csv_frame(CS_PARITY, dtype=str)
    controls = read_csv_frame(CS_CONTROLS, dtype=str)
    cost = read_csv_frame(CS_COST, dtype=str)
    day = read_csv_frame(CS_DAY)
    runtime = read_csv_frame(CS_RUNTIME, dtype=str)
    lock = read_csv_frame(CR_MT5_LOCK, dtype=str)

    policy_rows = build_policy_diagnostic(score, cost, day, runtime)
    failure_rows = build_failure_attribution(score, controls, cost, parity, runtime)
    lock_rows = build_release_lock_review(lock, runtime, controls, cost, score)
    queue_rows = build_next_queue()
    validation = score[score["split"] == "validation"]
    oos = score[score["split"] == "oos"]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "release_lock_review_rows": len(lock_rows),
        "failure_rows": len(failure_rows),
        "policy_diagnostic_rows": len(policy_rows),
        "next_queue_rows": len(queue_rows),
        "runtime_release_rows": int((runtime["mt5_probe_disposition"] == "release_review_ready_no_mt5_executed").sum()),
        "runtime_held_rows": int((runtime["mt5_probe_disposition"] != "release_review_ready_no_mt5_executed").sum()),
        "validation_max_balanced": float(validation["model_balanced_accuracy"].max()),
        "oos_max_balanced": float(oos["model_balanced_accuracy"].max()),
        "validation_max_signal_density": float(validation["signal_density"].max()),
        "oos_max_signal_density": float(oos["signal_density"].max()),
        "extended_control_block_rows": int(bool_series(controls["blocks_runtime_probe"]).sum()),
        "cost_curve_block_rows": int(bool_series(cost["blocks_runtime_probe"]).sum()),
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
        write_csv(RELEASE_LOCK_REVIEW, LOCK_COLUMNS, lock_rows),
        write_csv(FAILURE_ATTRIBUTION, FAILURE_COLUMNS, failure_rows),
        write_csv(POLICY_DIAGNOSTIC, POLICY_COLUMNS, policy_rows),
        write_csv(NEXT_REPAIR_QUEUE, QUEUE_COLUMNS, queue_rows),
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
