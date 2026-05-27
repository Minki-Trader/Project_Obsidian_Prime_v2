from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import Counter
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
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337DB"
RUN_ID = "run337DB_review_objective_feature_contract_pivot_training_without_db_v1"
PARENT_RUN_ID = "run337DA_train_objective_feature_contract_pivot_candidates_without_db_v1"
NEXT_RUN_ID = "run337DC_design_cost_shape_two_stage_handoff_repair_without_db_v1"
STATUS = "completed_stage337DB_objective_feature_training_review_cost_shape_blocks_no_selection_no_mt5"
JUDGMENT = "onnx_rank_signal_and_controls_clear_but_cost_shape_blocks_runtime_probe"
DECISION = "stage337DB_open_run337DC_design_cost_shape_two_stage_handoff_repair"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DB_objective_feature_contract_pivot_training_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337DB_objective_feature_contract_pivot_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DB_objective_feature_contract_pivot_training_review.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

DA_DIR = STAGE_DIR / "02_runs" / "run337DA"
DA_FINAL = DA_DIR / "final_decision.json"
DA_GATES = DA_DIR / "required_gate_coverage_audit.csv"
DA_SCORECARD = DA_DIR / "objective_training_scorecard.csv"
DA_CONTROL = DA_DIR / "control_residual_scorecard.csv"
DA_COST = DA_DIR / "cost_curve_scorecard.csv"
DA_RANK = DA_DIR / "rank_monotonicity_review.csv"
DA_RUNTIME = DA_DIR / "runtime_release_disposition.csv"
DA_PARITY = DA_DIR / "onnx_parity_matrix.csv"
DA_MODEL_MANIFEST = DA_DIR / "trained_model_manifest.csv"

TARGET_FAMILY_SUMMARY = RUN_DIR / "target_family_summary.csv"
TOP_VALIDATION_POCKETS = RUN_DIR / "top_validation_diagnostic_pockets.csv"
RELEASE_BLOCKER_SUMMARY = RUN_DIR / "release_blocker_summary.csv"
CONTROL_COST_RANK_SUMMARY = RUN_DIR / "control_cost_rank_summary.csv"
RANK_SIGNAL_HANDOFF_REVIEW = RUN_DIR / "rank_signal_handoff_review.csv"
NEXT_REPAIR_QUEUE = RUN_DIR / "run337DC_repair_design_queue.csv"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DA_FINAL,
    DA_GATES,
    DA_SCORECARD,
    DA_CONTROL,
    DA_COST,
    DA_RANK,
    DA_RUNTIME,
    DA_PARITY,
    DA_MODEL_MANIFEST,
)
OUTPUT_FILES = (
    TARGET_FAMILY_SUMMARY,
    TOP_VALIDATION_POCKETS,
    RELEASE_BLOCKER_SUMMARY,
    CONTROL_COST_RANK_SUMMARY,
    RANK_SIGNAL_HANDOFF_REVIEW,
    NEXT_REPAIR_QUEUE,
    MODEL_RECEIPT,
    DATA_RECEIPT,
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

GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")
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


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def load_frames() -> dict[str, pd.DataFrame]:
    return {
        "score": pd.read_csv(io_path(DA_SCORECARD)),
        "control": pd.read_csv(io_path(DA_CONTROL)),
        "cost": pd.read_csv(io_path(DA_COST)),
        "rank": pd.read_csv(io_path(DA_RANK)),
        "runtime": pd.read_csv(io_path(DA_RUNTIME)),
        "parity": pd.read_csv(io_path(DA_PARITY)),
        "models": pd.read_csv(io_path(DA_MODEL_MANIFEST)),
    }


def is_true(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower().eq("true")


def build_target_family_summary(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    score = frames["score"].copy()
    runtime = frames["runtime"].copy()
    control = frames["control"].copy()
    cost = frames["cost"].copy()
    rank = frames["rank"].copy()
    rows: list[dict[str, Any]] = []
    for family, group in score.groupby("target_family"):
        validation = group.loc[group["split"].astype(str).eq("validation")]
        oos = group.loc[group["split"].astype(str).eq("oos")]
        family_runtime = runtime.loc[runtime["target_family"].astype(str).eq(str(family))]
        family_control = control.loc[control["target_family"].astype(str).eq(str(family))]
        family_cost = cost.loc[cost["target_family"].astype(str).eq(str(family))]
        family_rank = rank.loc[rank["model_id"].isin(group["model_id"].unique())]
        rows.append(
            {
                "target_family": family,
                "model_rows": int(group["model_id"].nunique()),
                "validation_balanced_max": float(validation["balanced_accuracy"].astype(float).max()),
                "validation_balanced_mean": float(validation["balanced_accuracy"].astype(float).mean()),
                "oos_balanced_max": float(oos["balanced_accuracy"].astype(float).max()),
                "review_eligible_rows": int(family_runtime["mt5_probe_disposition"].astype(str).eq("review_eligible_no_auto_mt5_release").sum()),
                "held_rows": int(family_runtime["mt5_probe_disposition"].astype(str).eq("held_for_review").sum()),
                "control_block_rows": int(is_true(family_control["blocks_runtime_probe"]).sum()),
                "cost_block_rows": int(is_true(family_cost["blocks_runtime_probe"]).sum()),
                "rank_pass_rows": int(family_rank["monotonic_status"].astype(str).eq("passed_rank_monotonic").sum()) if not family_rank.empty else 0,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_top_validation(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    score = frames["score"].copy()
    runtime = frames["runtime"].copy()
    validation = score.loc[score["split"].astype(str).eq("validation")].copy()
    validation["balanced_accuracy"] = validation["balanced_accuracy"].astype(float)
    joined = validation.merge(runtime[["model_id", "release_blockers", "mt5_probe_disposition"]], on="model_id", how="left")
    joined = joined.sort_values("balanced_accuracy", ascending=False).head(30)
    rows = []
    for _, row in joined.iterrows():
        rows.append(
            {
                "model_id": row["model_id"],
                "target_family": row["target_family"],
                "target_id": row["target_id"],
                "balanced_accuracy": float(row["balanced_accuracy"]),
                "accuracy": float(row["accuracy"]),
                "signal_density": float(row["signal_density"]),
                "mt5_probe_disposition": row.get("mt5_probe_disposition", ""),
                "release_blockers": row.get("release_blockers", ""),
                "diagnostic_use": "read_only_no_selection(읽기 전용, 선택 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_release_blocker_summary(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    runtime = frames["runtime"].copy()
    counts = Counter(runtime["release_blockers"].astype(str))
    return [
        {
            "release_blockers": key,
            "rows": int(value),
            "interpretation": "runtime_probe_held(런타임 탐침 보류)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def build_control_cost_rank_summary(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    control = frames["control"].copy()
    cost = frames["cost"].copy()
    rank = frames["rank"].copy()
    rows = [
        {
            "summary_id": "control_alignment",
            "total_rows": int(len(control)),
            "passed_rows": int(control["control_status"].astype(str).eq("passed_control_weakened").sum()),
            "blocked_rows": int(is_true(control["blocks_runtime_probe"]).sum()),
            "worst_value": float(control["control_minus_actual"].astype(float).max()),
            "judgment": "controls_cleared(대조 통과)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "summary_id": "cost_shape",
            "total_rows": int(len(cost)),
            "passed_rows": int(cost["cost_status"].astype(str).eq("passed_cost_shape").sum()),
            "blocked_rows": int(is_true(cost["blocks_runtime_probe"]).sum()),
            "worst_value": float(cost.loc[~cost["cost_status"].astype(str).str.startswith("out_of_scope_rank_target"), "net_proxy_return"].astype(float).min()),
            "judgment": "cost_shape_blocks_release(비용 곡선이 해제 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "summary_id": "rank_monotonicity",
            "total_rows": int(len(rank)),
            "passed_rows": int(rank["monotonic_status"].astype(str).eq("passed_rank_monotonic").sum()),
            "blocked_rows": int(rank["monotonic_status"].astype(str).ne("passed_rank_monotonic").sum()),
            "worst_value": 0.0,
            "judgment": "rank_signal_present_but_not_trade_surface(순위 신호는 있으나 단독 거래 표면 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def build_rank_signal_review(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    top = pd.DataFrame(build_top_validation(frames))
    rank_top = top.loc[top["target_family"].astype(str).str.startswith("payoff_rank3")].head(12)
    rows = []
    for _, row in rank_top.iterrows():
        rows.append(
            {
                "model_id": row["model_id"],
                "target_id": row["target_id"],
                "validation_balanced_accuracy": row["balanced_accuracy"],
                "signal_density": row["signal_density"],
                "handoff_judgment": "rank_signal_requires_stage1_tradeability_and_cost_action_policy(순위 신호는 1단계 거래가능성과 비용 행동 정책 필요)",
                "forbidden_action": "no_rank_only_mt5_probe(순위 단독 MT5 탐침 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_next_queue() -> list[dict[str, str]]:
    required = ";".join(rel(path) for path in (TARGET_FAMILY_SUMMARY, CONTROL_COST_RANK_SUMMARY, RANK_SIGNAL_HANDOFF_REVIEW, DA_SCORECARD, DA_RUNTIME))
    return [
        {
            "queue_id": "run337DC_design_cost_shape_action_policy",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design train-only action policy for cost-shape failure(비용 곡선 실패용 학습 전용 행동 정책 설계)",
            "required_inputs": required,
            "required_outputs": "cost_shape_action_policy_contract.csv;train_only_action_threshold_plan.csv",
            "blocked_if_missing": "DB review summaries missing(DB 검토 요약 누락)",
            "forbidden_action": "no validation/OOS threshold tuning(검증/OOS 임계값 조정 금지)",
            "effect": "비용 실패를 로트가 아니라 행동 정책에서 다룬다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DC_design_two_stage_rank_handoff",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design explicit rank-as-stage2 handoff(순위를 2단계로 쓰는 명시 인계 설계)",
            "required_inputs": required,
            "required_outputs": "two_stage_rank_handoff_contract.csv;proxy_mt5_stage_compare_requirement.csv",
            "blocked_if_missing": "rank signal review missing(순위 신호 검토 누락)",
            "forbidden_action": "no fake single ONNX claim(가짜 단일 ONNX 주장 금지)",
            "effect": "순위 신호를 단독 매매 표면으로 과장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DC_design_point_cost_identity_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "design point-cost identity repair using close/point source(종가/포인트 원천으로 포인트 비용 정체성 수리 설계)",
            "required_inputs": required,
            "required_outputs": "point_cost_identity_contract.csv;source_price_requirement.csv",
            "blocked_if_missing": "price/point source unavailable(가격/포인트 원천 없음)",
            "forbidden_action": "no cost proxy promotion to operating claim(비용 프록시 운영 주장 금지)",
            "effect": "비용 프록시 한계를 다음 물질화에서 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DC_preserve_no_release_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "preserve no-release firewall before MT5 package(MT5 패키지 전 해제 금지 방화벽 유지)",
            "required_inputs": required,
            "required_outputs": "no_release_firewall.csv",
            "blocked_if_missing": "runtime disposition missing(런타임 처분 누락)",
            "forbidden_action": "no MT5 probe from DA held rows(DA 보류 행으로 MT5 탐침 금지)",
            "effect": "review eligible 0행을 성공처럼 포장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]

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
        row("db_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "DA 산출물을 모두 연결한다."),
        row("db_gate_parent_points_to_db", final["da_next_action"] == RUN_ID, final["da_next_action"], RUN_ID, "DA next_action(다음 행동)과 DB 실행을 맞춘다."),
        row("db_gate_da_gates_clean", final["da_failed_gates"] == 0, final["da_failed_gates"], "0", "실패한 DA 게이트 위에서 판정하지 않는다."),
        row("db_gate_onnx_parity_cleared", final["onnx_parity_passed"] == final["onnx_parity_rows"], f"{final['onnx_parity_passed']}/{final['onnx_parity_rows']}", "all parity passed", "ONNX 문제와 성능 문제를 분리한다."),
        row("db_gate_review_eligible_zero_recorded", final["review_eligible_rows"] == 0, final["review_eligible_rows"], "0", "해제 후보 없음이 명시된다."),
        row("db_gate_controls_cleared", final["control_block_rows"] == 0, final["control_block_rows"], "0", "대조 실패가 이번 차단 원인이 아님을 분리한다."),
        row("db_gate_cost_blocks_recorded", final["cost_block_rows"] > 0, final["cost_block_rows"], ">0", "비용 곡선 차단을 다음 수리 원인으로 기록한다."),
        row("db_gate_rank_signal_recorded", final["rank_pass_rows"] == final["rank_rows"] and final["rank_rows"] > 0, f"{final['rank_pass_rows']}/{final['rank_rows']}", "all rank monotonic rows pass", "순위 신호를 단독 표면이 아닌 인계 재료로 보존한다."),
        row("db_gate_next_queue", final["queue_rows"] >= 4, final["queue_rows"], ">=4", "DC 수리 설계를 구체화한다."),
        row("db_gate_no_selection_mt5", True, "selection=not_run;mt5=not_run", "no selection/MT5", "검토 결과를 즉시 운영 주장으로 바꾸지 않는다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    model_receipt = {
        "model_family": "DA trained candidates reviewed only(DA 학습 후보 검토 전용)",
        "target_and_label": "cost direction, payoff rank3, control residual(비용 방향, 보상 순위, 대조 잔차)",
        "split_method": "DA train/validation/OOS diagnostics(DA 학습/검증/OOS 진단)",
        "selection_metric": "not_applicable_no_selection(선택 없음)",
        "secondary_metrics": "ONNX parity, validation balanced, controls, cost, rank(ONNX 동등성, 검증 균형, 대조, 비용, 순위)",
        "threshold_policy": "not_tuned_in_DB(DB에서 조정 안 함)",
        "overfit_risk": "selecting top validation rank pocket without cost action repair(비용 행동 수리 없이 상위 검증 순위 포켓 선택)",
        "calibration_risk": "rank signal is not calibrated probability(순위 신호는 보정 확률 아님)",
        "comparison_baseline": PARENT_RUN_ID,
        "validation_judgment": "review_completed_cost_shape_blocks",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherited from DA outputs(DA 산출물 상속)",
        "sample_scope": "review only, no new rows(검토 전용, 새 행 없음)",
        "missing_or_duplicate_check": "input presence gate(입력 존재 게이트)",
        "feature_label_boundary": "review consumes DA metrics only(DB는 DA 지표만 소비)",
        "split_boundary": "validation/OOS read-only diagnostics(검증/OOS 읽기 전용 진단)",
        "leakage_risk": "using top validation pocket as selected candidate(상위 검증 포켓을 선택 후보로 쓰는 위험)",
        "data_hash_or_identity": {rel(DA_FINAL): sha256_file(DA_FINAL)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": "rank and controls improved but cost release blocked(순위와 대조는 개선, 비용 해제 차단)",
        "comparison_baseline": PARENT_RUN_ID,
        "likely_drivers": "payoff-rank target separates magnitude but not trade action(보상 순위 타깃이 크기는 분리하나 거래 행동은 아님)",
        "segment_checks": "target family, control, cost, rank(타깃 계열, 대조, 비용, 순위)",
        "trade_shape": "proxy cost shape only, no MT5 fills(프록시 비용 모양 전용, MT5 체결 없음)",
        "alternative_explanations": "point-cost proxy mismatch or action conversion gap(포인트 비용 프록시 불일치 또는 행동 전환 공백)",
        "attribution_confidence": "medium_for_review_low_for_operation(검토에는 중간, 운영에는 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "DA scorecards, control/cost/rank summaries, next queue(DA 점수표, 대조/비용/순위 요약, 다음 대기열)",
        "evidence_missing": "repair materialization, retraining, MT5 runtime probe(수리 물질화, 재학습, MT5 런타임 탐침)",
        "judgment_label": "review_completed_no_selection_cost_shape_blocks",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "모델은 만들어졌지만 비용 곡선이 막아 바로 탐침으로 보내지 않는다.",
    }
    paths = [
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifact_paths] + [rel(path) for path in paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_review_and_ignored_run_outputs(추적 검토와 무시 실행 산출물)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DB Training Review(학습 검토)

## Conclusion(결론)

run337DB(337DB 실행)는 DA 학습 결과를 review(검토)했다. ONNX parity(ONNX 동등성)는 `{final["onnx_parity_passed"]}/{final["onnx_parity_rows"]}`로 통과했고, control alignment(대조 정렬)는 차단 행 `0`이다. payoff rank(보상 순위)는 rank monotonicity(순위 단조성) `{final["rank_pass_rows"]}/{final["rank_rows"]}`로 살아 있다.

Effect(효과): 핵심 차단은 cost shape(비용 곡선)이다. review eligible(검토 가능) `0`행이므로 candidate selection(후보 선택), MT5 probe(MT5 탐침), Forward/Goal(전진/목표)은 주장하지 않는다.

## Read(판독)

- best_validation_balanced(최고 검증 균형): `{final["best_validation_balanced"]}`
- review_eligible_rows(검토 가능 행): `{final["review_eligible_rows"]}`
- control_block_rows(대조 차단 행): `{final["control_block_rows"]}`
- cost_block_rows(비용 차단 행): `{final["cost_block_rows"]}`
- rank_pass_rows(순위 통과 행): `{final["rank_pass_rows"]}/{final["rank_rows"]}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Boundary(경계)

- new_training(새 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- candidate_selection(후보 선택): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DB

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): cost shape/two-stage handoff(비용 곡선/2단계 인계) 수리 설계로 넘긴다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(TARGET_FAMILY_SUMMARY)}`
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
    workspace_text = re.sub(
        r"- >-\n  Stage337 run337DB focus complete:.*?(?=\n- >-|\n[A-Za-z0-9_]+:|\Z)",
        "",
        workspace_text,
        flags=re.S,
    )
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337DB focus complete: objective/feature training review(목표/피처 학습 검토)를 `{STATUS}`로 닫았다. "
        "Effect(효과): ONNX/rank/control(ONNX/순위/대조)은 보존하고 cost shape/two-stage handoff(비용 곡선/2단계 인계) 수리 설계를 연다.\n"
    )
    workspace_text = workspace_text.replace("current_focus:\n", focus_entry, 1)
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
    current_text = re.sub(
        r"\n## Stage337 run337DB\(337DB 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337DA|\n## |\Z)",
        "\n",
        current_text,
        flags=re.S,
    )
    section = f"""
## Stage337 run337DB(337DB 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): ONNX/rank/control(ONNX/순위/대조)은 보존하고 cost shape(비용 곡선) 차단을 다음 수리 설계로 넘긴다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DA(337DA"
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
- actual_mt5_execution(실제 MT5 실행): `not_run_db_review_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 cost shape/two-stage handoff repair design(비용 곡선/2단계 인계 수리 설계)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337DB(337DB 실행) reviewed objective/feature" not in line)
    stage_entry = (
        f"- {TODAY}: run337DB(337DB 실행) reviewed objective/feature contract pivot training(목표/피처 계약 전환 학습). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337DB reviewed objective/feature" not in line)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DB reviewed objective/feature contract pivot training(목표/피처 계약 전환 학습) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "objective_feature_contract_pivot_training_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"best_validation={final['best_validation_balanced']};cost_blocks={final['cost_block_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "result_judgment_model_validation_performance_attribution_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "training_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "model_validation_control_cost_rank_review",
        "scoreboard_lane": "result_judgment",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"review_eligible={final['review_eligible_rows']};cost_blocks={final['cost_block_rows']}",
        "guardrail_kpi": "no_selection;no_mt5;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "result_judgment_model_validation_performance_attribution_artifact_lineage",
        "evidence_scope": "DA training reviewed for release disposition",
        "kpi_scope": "model_validation_control_cost_rank_review",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__training_review",
        "family": "result_judgment_model_validation_performance_attribution_artifact_lineage",
        "question": "why did objective feature pivot training not release to MT5 probe",
        "metric_scope": "target_family_control_cost_rank_release",
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
    frames = load_frames()
    family_rows = build_target_family_summary(frames)
    top_rows = build_top_validation(frames)
    blocker_rows = build_release_blocker_summary(frames)
    summary_rows = build_control_cost_rank_summary(frames)
    rank_rows = build_rank_signal_review(frames)
    queue_rows = build_next_queue()
    artifacts: list[Path] = [
        write_csv(TARGET_FAMILY_SUMMARY, tuple(family_rows[0].keys()), family_rows),
        write_csv(TOP_VALIDATION_POCKETS, tuple(top_rows[0].keys()), top_rows),
        write_csv(RELEASE_BLOCKER_SUMMARY, tuple(blocker_rows[0].keys()), blocker_rows),
        write_csv(CONTROL_COST_RANK_SUMMARY, tuple(summary_rows[0].keys()), summary_rows),
        write_csv(RANK_SIGNAL_HANDOFF_REVIEW, tuple(rank_rows[0].keys()), rank_rows),
        write_csv(NEXT_REPAIR_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    da_final = read_json(DA_FINAL)
    parity_passed = int(is_true(frames["parity"]["passed"]).sum())
    control_blocks = int(is_true(frames["control"]["blocks_runtime_probe"]).sum())
    cost_blocks = int(is_true(frames["cost"]["blocks_runtime_probe"]).sum())
    rank_pass_rows = int(frames["rank"]["monotonic_status"].astype(str).eq("passed_rank_monotonic").sum())
    rank_total = int(len(frames["rank"]))
    best_validation = float(frames["score"].loc[frames["score"]["split"].astype(str).eq("validation"), "balanced_accuracy"].astype(float).max())
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "da_next_action": da_final.get("next_action", ""),
        "da_failed_gates": len(da_final.get("failed_gates", [])),
        "onnx_parity_rows": int(len(frames["parity"])),
        "onnx_parity_passed": parity_passed,
        "best_validation_balanced": best_validation,
        "review_eligible_rows": int(da_final.get("review_eligible_rows", 0)),
        "control_block_rows": control_blocks,
        "cost_block_rows": cost_blocks,
        "rank_rows": rank_total,
        "rank_pass_rows": rank_pass_rows,
        "queue_rows": len(queue_rows),
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
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
