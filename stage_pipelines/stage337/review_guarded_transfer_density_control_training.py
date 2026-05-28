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
from stage_pipelines.stage337 import train_guarded_transfer_density_control_repair_candidates as dz  # noqa: E402
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
STAGE_ID = dz.STAGE_ID
RUN_NUMBER = "run337EA"
RUN_ID = "run337EA_review_guarded_transfer_density_control_training_without_db_v1"
PARENT_RUN_ID = dz.RUN_ID
NEXT_RUN_ID = "run337EB_design_validation_density_trade_count_repair_without_db_v1"
STATUS = "completed_stage337EA_guarded_transfer_density_control_training_review_validation_floor_density_blocks_release_no_selection_no_mt5"
JUDGMENT = "onnx_and_controls_clear_but_validation_pf_trade_count_and_density_block_release"
DECISION = "stage337EA_open_run337EB_design_validation_density_trade_count_repair"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EA_guarded_transfer_density_control_training_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dz.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = dz.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EA_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EA_guarded_transfer_density_control_training_review.md"
SELECTED_STATUS = dz.SELECTED_STATUS
STAGE_BRIEF = dz.STAGE_BRIEF
WORKSPACE_STATE = dz.WORKSPACE_STATE
CURRENT_STATE = dz.CURRENT_STATE
CHANGELOG = dz.CHANGELOG
RUN_REGISTRY = dz.RUN_REGISTRY
ALPHA_LEDGER = dz.ALPHA_LEDGER
ARTIFACT_REGISTRY = dz.ARTIFACT_REGISTRY
STAGE_LEDGER = dz.STAGE_LEDGER

DZ_FINAL = dz.FINAL_DECISION
DZ_GATES = dz.REQUIRED_GATE_AUDIT
DZ_QUEUE = dz.EA_QUEUE
MODEL_MANIFEST = dz.TRAINED_MODEL_MANIFEST
ONNX_PARITY = dz.ONNX_PARITY
CANDIDATE_SCORECARD = dz.CANDIDATE_SCORECARD
PROXY_TRADE_SCORECARD = dz.PROXY_TRADE_SCORECARD
NEGATIVE_CONTROL_SCORECARD = dz.NEGATIVE_CONTROL_SCORECARD
DENSITY_GUARD_AUDIT = dz.DENSITY_GUARD_AUDIT
SPLIT_GUARD_AUDIT = dz.SPLIT_GUARD_AUDIT
RUNTIME_FIREWALL_REVIEW = dz.RUNTIME_FIREWALL_REVIEW
RELEASE_DISPOSITION = dz.RELEASE_DISPOSITION

CANDIDATE_TRAINING_REVIEW = RUN_DIR / "candidate_training_review.csv"
ONNX_PARITY_REVIEW = RUN_DIR / "onnx_parity_review.csv"
CONTROL_DENSITY_SPLIT_REVIEW = RUN_DIR / "control_density_split_review.csv"
RELEASE_LOCK_REVIEW = RUN_DIR / "release_lock_review.csv"
FAILURE_MEMORY_UPDATE = RUN_DIR / "failure_memory_update.csv"
EB_QUEUE = RUN_DIR / "run337EB_design_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DZ_FINAL,
    DZ_GATES,
    DZ_QUEUE,
    MODEL_MANIFEST,
    ONNX_PARITY,
    CANDIDATE_SCORECARD,
    PROXY_TRADE_SCORECARD,
    NEGATIVE_CONTROL_SCORECARD,
    DENSITY_GUARD_AUDIT,
    SPLIT_GUARD_AUDIT,
    RUNTIME_FIREWALL_REVIEW,
    RELEASE_DISPOSITION,
)
OUTPUT_FILES = (
    CANDIDATE_TRAINING_REVIEW,
    ONNX_PARITY_REVIEW,
    CONTROL_DENSITY_SPLIT_REVIEW,
    RELEASE_LOCK_REVIEW,
    FAILURE_MEMORY_UPDATE,
    EB_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    RUNTIME_RECEIPT,
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

CANDIDATE_REVIEW_COLUMNS = (
    "model_id",
    "task_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "weight_policy_id",
    "validation_pf",
    "validation_trade_count",
    "validation_balanced_accuracy",
    "oos_pf",
    "oos_trade_count",
    "validation_density_pressure_rows",
    "control_block_rows",
    "review_status",
    "release_blockers",
    "effect",
    "claim_boundary",
)
ONNX_REVIEW_COLUMNS = ("review_id", "rows", "passed_rows", "failed_rows", "review_status", "effect", "claim_boundary")
CONTROL_DENSITY_COLUMNS = (
    "review_id",
    "subject",
    "rows",
    "blocking_rows",
    "review_status",
    "effect",
    "claim_boundary",
)
RELEASE_LOCK_COLUMNS = (
    "review_id",
    "models",
    "release_candidate_rows",
    "auto_mt5_release_rows",
    "release_status",
    "release_blockers",
    "next_condition",
    "effect",
    "claim_boundary",
)
FAILURE_MEMORY_COLUMNS = ("memory_id", "observed", "interpretation", "next_repair_hint", "claim_boundary")
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


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    return result if math.isfinite(result) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def review_candidates() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    release = pd.read_csv(io_path(RELEASE_DISPOSITION))
    class_scores = pd.read_csv(io_path(CANDIDATE_SCORECARD))
    trades = pd.read_csv(io_path(PROXY_TRADE_SCORECARD))
    val_class = class_scores.loc[class_scores["split"].astype(str).eq("validation")].set_index("model_id")
    oos_trades = trades.loc[trades["split"].astype(str).eq("oos")].set_index("model_id")
    rows: list[dict[str, Any]] = []
    for _, item in release.iterrows():
        model_id = str(item["model_id"])
        validation_pf = as_float(item["validation_pf"])
        validation_trade_count = as_int(item["validation_trade_count"])
        validation_balanced = as_float(item["validation_balanced_accuracy"])
        oos_pf = as_float(item["oos_pf"])
        oos_trade_count = as_int(oos_trades.loc[model_id, "trade_count"]) if model_id in oos_trades.index else 0
        density_pressure = as_int(item["density_pressure_rows"])
        control_blocks = as_int(item["control_block_rows"])
        blockers = str(item.get("release_blockers", ""))
        status_bits: list[str] = []
        if validation_pf < 1.05:
            status_bits.append("validation_pf_floor_block")
        if validation_trade_count < 500:
            status_bits.append("validation_trade_count_block")
        if density_pressure > 0:
            status_bits.append("density_pressure_block")
        if control_blocks > 0:
            status_bits.append("control_alignment_block")
        if not status_bits:
            status_bits.append("review_required_no_auto_release")
        val_row = val_class.loc[model_id] if model_id in val_class.index else {}
        rows.append(
            {
                "model_id": model_id,
                "task_id": item["task_id"],
                "cost_policy_id": val_row.get("cost_policy_id", ""),
                "feature_set_id": val_row.get("feature_set_id", ""),
                "model_config_id": val_row.get("model_config_id", ""),
                "weight_policy_id": val_row.get("weight_policy_id", ""),
                "validation_pf": validation_pf,
                "validation_trade_count": validation_trade_count,
                "validation_balanced_accuracy": validation_balanced,
                "oos_pf": oos_pf,
                "oos_trade_count": oos_trade_count,
                "validation_density_pressure_rows": density_pressure,
                "control_block_rows": control_blocks,
                "review_status": ";".join(status_bits),
                "release_blockers": blockers,
                "effect": "reviews trained output without selecting a winner(승자 선택 없이 학습 출력을 검토)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    frame = pd.DataFrame(rows)
    best_validation = frame.sort_values(["validation_pf", "validation_trade_count"], ascending=[False, False]).iloc[0].to_dict()
    best_oos = frame.sort_values(["oos_pf", "oos_trade_count"], ascending=[False, False]).iloc[0].to_dict()
    summary = {
        "candidate_rows": len(rows),
        "validation_pf_floor_pass_rows": int((frame["validation_pf"].astype(float) >= 1.05).sum()),
        "validation_trade_count_pass_rows": int((frame["validation_trade_count"].astype(int) >= 500).sum()),
        "validation_both_floor_pass_rows": int(((frame["validation_pf"].astype(float) >= 1.05) & (frame["validation_trade_count"].astype(int) >= 500)).sum()),
        "density_pressure_rows": int(frame["validation_density_pressure_rows"].astype(int).sum()),
        "control_block_rows": int(frame["control_block_rows"].astype(int).sum()),
        "best_validation_model_id": best_validation["model_id"],
        "best_validation_pf": float(best_validation["validation_pf"]),
        "best_validation_trade_count": int(best_validation["validation_trade_count"]),
        "best_oos_model_id": best_oos["model_id"],
        "best_oos_pf": float(best_oos["oos_pf"]),
        "best_oos_trade_count": int(best_oos["oos_trade_count"]),
    }
    return rows, summary


def review_onnx() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = read_csv(ONNX_PARITY)
    passed = sum(1 for row in rows if row.get("passed") == "true")
    failed = len(rows) - passed
    review_rows = [
        {
            "review_id": "onnx_probability_parity",
            "rows": len(rows),
            "passed_rows": passed,
            "failed_rows": failed,
            "review_status": "passed" if failed == 0 and rows else "failed",
            "effect": "confirms Python/ONNX probability parity before any runtime thought(런타임 검토 전 파이썬/ONNX 확률 동등성 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return review_rows, {"onnx_rows": len(rows), "onnx_passed": passed, "onnx_failed": failed}


def review_controls_density_split() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    controls = read_csv(NEGATIVE_CONTROL_SCORECARD)
    density = read_csv(DENSITY_GUARD_AUDIT)
    split = read_csv(SPLIT_GUARD_AUDIT)
    control_blocks = sum(1 for row in controls if row.get("blocks_training_review") == "true")
    density_validation_pressure = sum(1 for row in density if row.get("split") == "validation" and row.get("density_pressure_flag") == "true")
    density_oos_pressure = sum(1 for row in density if row.get("split") == "oos" and row.get("density_pressure_flag") == "true")
    split_failed = sum(1 for row in split if row.get("status") != "passed")
    review_rows = [
        {
            "review_id": "negative_control_review",
            "subject": "shifted/noise/block controls(이동/잡음/블록 대조)",
            "rows": len(controls),
            "blocking_rows": control_blocks,
            "review_status": "passed_control_clear" if control_blocks == 0 else "blocked_control_alignment",
            "effect": "keeps shifted-control gate hard(이동 대조 게이트를 강하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "density_guard_review",
            "subject": "validation/OOS density pressure(검증/OOS 밀도 압력)",
            "rows": len(density),
            "blocking_rows": density_validation_pressure,
            "review_status": "blocked_density_pressure" if density_validation_pressure else "passed_density_guard",
            "effect": "blocks release when signal density jumps versus train(학습 대비 신호 밀도 급증 시 해제 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "split_guard_review",
            "subject": "train-only auxiliary and WFO precheck(학습 전용 보조와 WFO 사전점검)",
            "rows": len(split),
            "blocking_rows": split_failed,
            "review_status": "passed_split_guard" if split_failed == 0 else "blocked_split_guard",
            "effect": "keeps validation/OOS outside training feedback(검증/OOS를 학습 피드백 밖에 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return review_rows, {
        "control_rows": len(controls),
        "control_block_rows": control_blocks,
        "density_rows": len(density),
        "density_validation_pressure_rows": density_validation_pressure,
        "density_oos_pressure_rows": density_oos_pressure,
        "split_rows": len(split),
        "split_failed_rows": split_failed,
    }


def build_release_lock(summary: Mapping[str, Any], control_density: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    release = read_csv(RELEASE_DISPOSITION)
    release_candidates = sum(1 for row in release if row.get("release_disposition") != "held_for_EA_review_no_selection")
    blockers: list[str] = []
    if summary["best_validation_pf"] < 1.05:
        blockers.append("best_validation_pf_below_1p05")
    if summary["best_validation_trade_count"] < 500:
        blockers.append("best_validation_trade_count_below_500")
    if control_density["density_validation_pressure_rows"] > 0:
        blockers.append("validation_density_pressure")
    if control_density["control_block_rows"] > 0:
        blockers.append("control_alignment")
    if summary["best_oos_pf"] > 1.5 and summary["best_oos_trade_count"] < 100:
        blockers.append("oos_pocket_too_thin_for_selection")
    release_status = "blocked_no_selection_no_mt5" if blockers or release_candidates == 0 else "review_required"
    rows = [
        {
            "review_id": "ea_release_lock",
            "models": len(release),
            "release_candidate_rows": 0,
            "auto_mt5_release_rows": 0,
            "release_status": release_status,
            "release_blockers": ";".join(blockers) or "review_required_no_auto_release",
            "next_condition": NEXT_RUN_ID,
            "effect": "keeps training result from becoming runtime claim(학습 결과가 런타임 주장으로 바뀌지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return rows, {"release_candidate_rows": 0, "auto_mt5_release_rows": 0, "release_blockers": blockers, "release_status": release_status}


def build_failure_memory(summary: Mapping[str, Any], control_density: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "validation_floor_still_below",
            "observed": f"best_validation_pf={summary['best_validation_pf']};trades={summary['best_validation_trade_count']}",
            "interpretation": "validation edge remains below release floor(검증 우위가 해제 하한보다 낮음)",
            "next_repair_hint": "design validation-density/trade-count repair without threshold tuning(임계값 조정 없이 검증-밀도/거래수 수리 설계)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "density_pressure_persists",
            "observed": f"validation_density_pressure_rows={control_density['density_validation_pressure_rows']}",
            "interpretation": "signal density transfer is still unstable(신호 밀도 전이가 여전히 불안정)",
            "next_repair_hint": "deconcentrate objective during training, not post-hoc filter(사후 필터가 아니라 학습 목표에서 탈집중)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "thin_oos_pocket_warning",
            "observed": f"best_oos_pf={summary['best_oos_pf']};trades={summary['best_oos_trade_count']}",
            "interpretation": "high OOS PF is too thin to select(높은 OOS PF는 표본이 얇아 선택 불가)",
            "next_repair_hint": "require validation support before OOS pocket use(OOS 포켓 사용 전 검증 지지 요구)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "shifted_control_clear_but_not_sufficient",
            "observed": f"control_block_rows={control_density['control_block_rows']}",
            "interpretation": "control clearance alone is not release evidence(대조 통과만으로는 해제 근거가 아님)",
            "next_repair_hint": "keep control gate and repair validation/density shape(대조 게이트 유지, 검증/밀도 형태 수리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_eb_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337EB_design_validation_density_trade_count_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design validation-density/trade-count repair(검증-밀도/거래수 수리 설계)",
            "required_inputs": f"{rel(CANDIDATE_TRAINING_REVIEW)};{rel(CONTROL_DENSITY_SPLIT_REVIEW)};{rel(FAILURE_MEMORY_UPDATE)}",
            "required_outputs": "validation_density_trade_count_repair_design.csv",
            "blocked_if_missing": "EA review outputs(EA 검토 출력)",
            "forbidden_action": "no threshold tuning or candidate selection(임계값 조정 또는 후보 선택 금지)",
            "effect": "turns blocked review into next no-overfit design(차단 검토를 다음 무과적합 설계로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EB_preserve_onnx_artifacts",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "preserve DZ ONNX artifacts as research artifacts(DZ ONNX 산출물을 연구 산출물로 보존)",
            "required_inputs": rel(MODEL_MANIFEST),
            "required_outputs": "artifact_preservation_review.csv",
            "blocked_if_missing": "model manifest(모델 목록)",
            "forbidden_action": "no runtime promotion from DZ artifacts(DZ 산출물 런타임 승격 금지)",
            "effect": "keeps useful evidence without operating claim(운영 주장 없이 유용한 근거 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DZ outputs exist(필수 DZ 출력 존재)"),
        ("parent_dz_gates_passed", final["dz_failed_gate_rows"] == 0, str(final["dz_failed_gate_rows"]), "0", "DZ training gates passed(DZ 학습 게이트 통과)"),
        ("parent_next_action_matches", final["dz_next_action"] == RUN_ID, str(final["dz_next_action"]), RUN_ID, "continues DZ queue(DZ 대기열을 이어감)"),
        ("onnx_parity_review_passed", final["onnx_failed_rows"] == 0 and final["onnx_passed_rows"] == final["trained_models"], f"{final['onnx_passed_rows']}/{final['trained_models']}", "all", "ONNX parity clear(ONNX 동등성 명확)"),
        ("control_review_clear", final["control_block_rows"] == 0, str(final["control_block_rows"]), "0", "shifted/noise/block controls clear(이동/잡음/블록 대조 명확)"),
        ("validation_floor_blocks_release", final["best_validation_pf"] < 1.05 or final["best_validation_trade_count"] < 500, f"pf={final['best_validation_pf']};trades={final['best_validation_trade_count']}", "below floor", "validation floor blocks release(검증 하한이 해제 차단)"),
        ("density_pressure_blocks_release", final["density_validation_pressure_rows"] > 0, str(final["density_validation_pressure_rows"]), ">0", "density pressure is recorded as blocker(밀도 압력을 차단 요소로 기록)"),
        ("release_locked", final["release_candidate_rows"] == 0 and final["auto_mt5_release_rows"] == 0, f"release={final['release_candidate_rows']};mt5={final['auto_mt5_release_rows']}", "0/0", "release and MT5 remain blocked(해제와 MT5 계속 차단)"),
        (
            "no_forbidden_claim",
            final["candidate_selection"] == "not_run"
            and final["mt5_runtime_probe"] == "not_run"
            and final["goal_achieve"] == "not_claimed",
            f"selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
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
        "time_axis": "inherits DZ source_row_id split scoring; no new bars joined(DZ source_row_id 분할 점수화를 상속, 새 봉 결합 없음)",
        "sample_scope": f"trained_models={final['trained_models']};reviewed_models={final['candidate_review_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']}",
        "feature_label_boundary": "review only; no labels or thresholds changed(검토 전용, 라벨/임계값 변경 없음)",
        "split_boundary": "train/validation/OOS scorecards read-only(학습/검증/OOS 점수표 읽기 전용)",
        "leakage_risk": "using validation/OOS to select a winner after review(검토 뒤 검증/OOS로 승자를 고르는 위험)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "DZ trained sklearn/ONNX artifacts(DZ 학습 sklearn/ONNX 산출물)",
        "target_and_label": "review of fixed action labels and train-only auxiliary weights(고정 행동 라벨과 학습 전용 보조 가중치 검토)",
        "split_method": "read-only review(읽기 전용 검토)",
        "selection_metric": "none; release locked(없음, 해제 잠금)",
        "secondary_metrics": "validation PF/trade count, controls, density, ONNX parity(검증 PF/거래수/대조/밀도/ONNX 동등성)",
        "threshold_policy": "no threshold tuning(임계값 조정 없음)",
        "overfit_risk": "thin OOS pocket and validation floor miss(얇은 OOS 포켓과 검증 하한 미달)",
        "calibration_risk": "scores remain ranking diagnostics(점수는 순위 진단에 머묾)",
        "comparison_baseline": rel(DZ_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"best_validation_pf={final['best_validation_pf']};best_oos_pf={final['best_oos_pf']};density_pressure={final['density_validation_pressure_rows']}",
        "comparison_baseline": rel(DZ_FINAL),
        "likely_drivers": "auxiliary weighting reduced controls but did not clear validation floor/density(보조 가중치가 대조는 줄였지만 검증 하한/밀도를 통과하지 못함)",
        "segment_checks": "validation, OOS, control, density, release blockers(검증/OOS/대조/밀도/해제 차단)",
        "trade_shape": f"best_validation_trades={final['best_validation_trade_count']};best_oos_trades={final['best_oos_trade_count']}",
        "alternative_explanations": "sample-thin OOS pocket, density transfer mismatch, validation noise(얇은 OOS 포켓/밀도 전이 불일치/검증 잡음)",
        "attribution_confidence": "medium_for_review_low_for_runtime(검토는 중간, 런타임은 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_receipt = {
        "research_path": rel(Path(__file__)),
        "runtime_path": "not_applicable_no_MT5_package(해당 없음, MT5 패키지 없음)",
        "shared_contract": "ONNX parity and release lock only(ONNX 동등성과 해제 잠금만)",
        "known_differences": "no MT5 handoff/tester output(EA에는 MT5 인계/테스터 출력 없음)",
        "parity_check": f"{final['onnx_passed_rows']}/{final['onnx_rows']}",
        "parity_identity": rel(ONNX_PARITY_REVIEW),
        "runtime_claim_boundary": "research-only(연구 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "EA review tables, DZ scorecards, ONNX parity, controls, density(EA 검토표/DZ 점수표/ONNX 동등성/대조/밀도)",
        "evidence_missing": "candidate selection, MT5, forward test(후보 선택/MT5/전진 테스트)",
        "judgment_label": "blocked_release_repair_design_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "ONNX와 대조는 괜찮지만 검증 PF/거래수/밀도 때문에 아직 고를 수 없다.",
    }
    paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(RUNTIME_RECEIPT, runtime_receipt),
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
        "availability": "tracked_review_outputs_with_ignored_parent_artifacts(추적 검토 출력과 무시된 부모 산출물)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EA Guarded Training Review(337EA 방어 학습 검토)

## Conclusion(결론)

run337EA(337EA 실행)는 DZ 후보 54개를 검토했다. ONNX parity(ONNX 동등성)는 `{final["onnx_passed_rows"]}/{final["onnx_rows"]}`이고 negative controls(부정 대조)는 차단 0행이다.

하지만 best_validation_pf(최고 검증 PF)는 `{final["best_validation_pf"]}`로 1.05 하한보다 낮고, 해당 validation_trade_count(검증 거래 수)는 `{final["best_validation_trade_count"]}`로 500 미만이다. validation density pressure(검증 밀도 압력)도 `{final["density_validation_pressure_rows"]}`행이다.

Effect(효과): DZ ONNX는 research artifact(연구 산출물)로 보존하지만 candidate selection(후보 선택), MT5 probe(MT5 탐침), Forward/Goal(전진/목표)은 계속 금지한다. 다음은 validation-density/trade-count repair design(검증-밀도/거래수 수리 설계)이다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- best_validation_model(최고 검증 모델): `{final["best_validation_model_id"]}`
- best_validation_pf(최고 검증 PF): `{final["best_validation_pf"]}`
- best_validation_trade_count(최고 검증 거래 수): `{final["best_validation_trade_count"]}`
- best_oos_pf(최고 OOS PF): `{final["best_oos_pf"]}`
- best_oos_trade_count(최고 OOS 거래 수): `{final["best_oos_trade_count"]}`
- control_block_rows(대조 차단 행): `{final["control_block_rows"]}`
- density_validation_pressure_rows(검증 밀도 압력 행): `{final["density_validation_pressure_rows"]}`
- release_candidate_rows(해제 후보 행): `{final["release_candidate_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EA

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): ONNX와 대조는 통과했지만 검증 하한/거래수/밀도 압력이 해제를 막아 EB 수리 설계를 연다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(CANDIDATE_TRAINING_REVIEW)}`, `{rel(CONTROL_DENSITY_SPLIT_REVIEW)}`
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
        f"  Stage337 run337EA focus complete: guarded transfer/density/control training review(방어 전이/밀도/대조 학습 검토)를 `{STATUS}`로 닫았다. "
        f"Effect(효과): release(해제)는 막고 run337EB(337EB 실행) validation-density/trade-count repair design(검증-밀도/거래수 수리 설계)을 연다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EA focus complete")
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
## Stage337 run337EA(337EA 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): ONNX/control(ONNX/대조)은 통과했지만 validation PF/trade count/density(검증 PF/거래수/밀도)가 release(해제)를 막아 EB 설계로 넘긴다. Goal(목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DZ("
    if "## Stage337 run337EA(337EA 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_ea_review_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): `다음은 validation-density/trade-count repair design(검증-밀도/거래수 수리 설계)이다.`
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EA(337EA 실행) reviewed guarded transfer/density/control training(방어 전이/밀도/대조 학습 검토). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EA(337EA 실행) reviewed guarded transfer"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337EA reviewed guarded transfer/density/control training(방어 전이/밀도/대조 학습 검토) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EA reviewed guarded transfer"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "guarded_transfer_density_control_training_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"best_validation_pf={final['best_validation_pf']};density_pressure={final['density_validation_pressure_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "training_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_training_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "proxy_training_review",
        "scoreboard_lane": "model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_validation_pf={final['best_validation_pf']};best_oos_pf={final['best_oos_pf']}",
        "guardrail_kpi": "release_locked;density_pressure;no_selection;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_performance_attribution_result_judgment",
        "evidence_scope": "DZ training reviewed without release",
        "kpi_scope": "validation_floor_density_control_review",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__training_review",
        "family": "model_validation_performance_attribution_result_judgment",
        "question": "do DZ candidates release or require validation density repair",
        "metric_scope": "validation_pf_trade_count_density_controls",
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
    candidate_rows, candidate_summary = review_candidates()
    onnx_rows, onnx_summary = review_onnx()
    control_density_rows, control_density_summary = review_controls_density_split()
    release_rows, release_summary = build_release_lock(candidate_summary, control_density_summary)
    failure_rows = build_failure_memory(candidate_summary, control_density_summary)
    queue_rows = build_eb_queue()
    artifacts: list[Path] = [
        write_csv(CANDIDATE_TRAINING_REVIEW, CANDIDATE_REVIEW_COLUMNS, candidate_rows),
        write_csv(ONNX_PARITY_REVIEW, ONNX_REVIEW_COLUMNS, onnx_rows),
        write_csv(CONTROL_DENSITY_SPLIT_REVIEW, CONTROL_DENSITY_COLUMNS, control_density_rows),
        write_csv(RELEASE_LOCK_REVIEW, RELEASE_LOCK_COLUMNS, release_rows),
        write_csv(FAILURE_MEMORY_UPDATE, FAILURE_MEMORY_COLUMNS, failure_rows),
        write_csv(EB_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    dz_final = read_json(DZ_FINAL)
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dz_next_action": dz_final.get("next_action", ""),
        "dz_failed_gate_rows": sum(1 for row in read_csv(DZ_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "trained_models": int(dz_final.get("trained_models", len(candidate_rows))),
        "candidate_review_rows": len(candidate_rows),
        "validation_pf_floor_pass_rows": candidate_summary["validation_pf_floor_pass_rows"],
        "validation_trade_count_pass_rows": candidate_summary["validation_trade_count_pass_rows"],
        "validation_both_floor_pass_rows": candidate_summary["validation_both_floor_pass_rows"],
        "best_validation_model_id": candidate_summary["best_validation_model_id"],
        "best_validation_pf": candidate_summary["best_validation_pf"],
        "best_validation_trade_count": candidate_summary["best_validation_trade_count"],
        "best_oos_model_id": candidate_summary["best_oos_model_id"],
        "best_oos_pf": candidate_summary["best_oos_pf"],
        "best_oos_trade_count": candidate_summary["best_oos_trade_count"],
        "onnx_rows": onnx_summary["onnx_rows"],
        "onnx_passed_rows": onnx_summary["onnx_passed"],
        "onnx_failed_rows": onnx_summary["onnx_failed"],
        "control_rows": control_density_summary["control_rows"],
        "control_block_rows": control_density_summary["control_block_rows"],
        "density_rows": control_density_summary["density_rows"],
        "density_validation_pressure_rows": control_density_summary["density_validation_pressure_rows"],
        "density_oos_pressure_rows": control_density_summary["density_oos_pressure_rows"],
        "split_failed_rows": control_density_summary["split_failed_rows"],
        "release_candidate_rows": release_summary["release_candidate_rows"],
        "auto_mt5_release_rows": release_summary["auto_mt5_release_rows"],
        "release_status": release_summary["release_status"],
        "release_blockers": release_summary["release_blockers"],
        "model_training": "not_run_review_only",
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
    artifacts.extend(
        [
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
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision_doc(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": "gate_failed", "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "best_validation_pf": final["best_validation_pf"],
                "best_validation_trade_count": final["best_validation_trade_count"],
                "density_validation_pressure_rows": final["density_validation_pressure_rows"],
                "release_candidate_rows": final["release_candidate_rows"],
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
