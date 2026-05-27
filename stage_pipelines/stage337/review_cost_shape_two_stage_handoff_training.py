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
RUN_NUMBER = "run337DF"
RUN_ID = "run337DF_review_cost_shape_two_stage_handoff_training_without_db_v1"
PARENT_RUN_ID = "run337DE_train_cost_shape_two_stage_handoff_candidates_without_db_v1"
NEXT_RUN_ID = "run337DG_design_validation_pocket_cost_shape_repair_without_db_v1"
STATUS = "completed_stage337DF_two_stage_training_review_validation_cost_shape_blocks_no_selection_no_mt5"
JUDGMENT = "onnx_clear_stage1_signal_present_but_validation_pair_cost_shape_blocks_runtime_probe"
DECISION = "stage337DF_open_run337DG_design_validation_pocket_cost_shape_repair"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DF_cost_shape_two_stage_handoff_training_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337DF_cost_shape_two_stage_handoff_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DF_cost_shape_two_stage_handoff_training_review.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

DE_DIR = STAGE_DIR / "02_runs" / "run337DE"
DE_FINAL = DE_DIR / "final_decision.json"
DE_GATES = DE_DIR / "required_gate_coverage_audit.csv"
DE_MODEL_MANIFEST = DE_DIR / "trained_model_manifest.csv"
DE_PARITY = DE_DIR / "onnx_parity_matrix.csv"
DE_SCORECARD = DE_DIR / "model_metric_scorecard.csv"
DE_SINGLE_COST = DE_DIR / "single_model_cost_curve_scorecard.csv"
DE_RANK = DE_DIR / "rank_monotonicity_review.csv"
DE_PAIR = DE_DIR / "two_stage_pair_scorecard.csv"
DE_RUNTIME = DE_DIR / "runtime_release_disposition.csv"

PAIR_SUMMARY = RUN_DIR / "pair_validation_oos_summary.csv"
VALIDATION_OOS_DIVERGENCE = RUN_DIR / "validation_oos_divergence_review.csv"
RELEASE_BLOCKERS = RUN_DIR / "release_blocker_summary.csv"
MODEL_FAMILY_SUMMARY = RUN_DIR / "model_family_summary.csv"
RANK_STAGE_SUMMARY = RUN_DIR / "rank_stage_review_summary.csv"
DG_QUEUE = RUN_DIR / "run337DG_repair_design_queue.csv"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DE_FINAL,
    DE_GATES,
    DE_MODEL_MANIFEST,
    DE_PARITY,
    DE_SCORECARD,
    DE_SINGLE_COST,
    DE_RANK,
    DE_PAIR,
    DE_RUNTIME,
)
OUTPUT_FILES = (
    PAIR_SUMMARY,
    VALIDATION_OOS_DIVERGENCE,
    RELEASE_BLOCKERS,
    MODEL_FAMILY_SUMMARY,
    RANK_STAGE_SUMMARY,
    DG_QUEUE,
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

PAIR_SUMMARY_COLUMNS = (
    "pair_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "validation_pf",
    "validation_net",
    "validation_trades",
    "validation_status",
    "oos_pf",
    "oos_net",
    "oos_trades",
    "oos_status",
    "review_status",
    "effect",
    "claim_boundary",
)
DIVERGENCE_COLUMNS = (
    "pair_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "validation_pf",
    "oos_pf",
    "pf_gap_oos_minus_validation",
    "validation_net",
    "oos_net",
    "divergence_status",
    "effect",
    "claim_boundary",
)
BLOCKER_COLUMNS = ("release_blocker", "rows", "effect", "claim_boundary")
MODEL_SUMMARY_COLUMNS = (
    "target_family",
    "validation_balanced_max",
    "validation_balanced_mean",
    "oos_balanced_max",
    "model_rows",
    "effect",
    "claim_boundary",
)
RANK_SUMMARY_COLUMNS = (
    "cost_policy_id",
    "split",
    "rank_rows",
    "passed_rank_rows",
    "pass_rate",
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


def is_true_series(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower().eq("true")


def load_frames() -> dict[str, pd.DataFrame]:
    return {
        "models": pd.read_csv(io_path(DE_MODEL_MANIFEST)),
        "parity": pd.read_csv(io_path(DE_PARITY)),
        "score": pd.read_csv(io_path(DE_SCORECARD)),
        "single_cost": pd.read_csv(io_path(DE_SINGLE_COST)),
        "rank": pd.read_csv(io_path(DE_RANK)),
        "pair": pd.read_csv(io_path(DE_PAIR)),
        "runtime": pd.read_csv(io_path(DE_RUNTIME)),
    }


def build_pair_summary(pair: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pair_id, group in pair.groupby("pair_id"):
        parts = {str(row["split"]): row for _, row in group.iterrows()}
        validation = parts.get("validation")
        oos = parts.get("oos")
        if validation is None or oos is None:
            continue
        validation_pf = as_float(validation["profit_factor"])
        oos_pf = as_float(oos["profit_factor"])
        validation_status = str(validation["pair_status"])
        oos_status = str(oos["pair_status"])
        if validation_status == "passed_pair_cost_shape" and oos_status == "passed_pair_cost_shape":
            review_status = "review_candidate_no_auto_release(검토 후보, 자동 해제 아님)"
        elif oos_status == "passed_pair_cost_shape" and validation_status != "passed_pair_cost_shape":
            review_status = "oos_positive_validation_thin_block(전진외 표본 긍정이나 검증 얇음 차단)"
        else:
            review_status = "blocked_pair_cost_shape(쌍 비용 곡선 차단)"
        rows.append(
            {
                "pair_id": pair_id,
                "cost_policy_id": validation["cost_policy_id"],
                "feature_set_id": validation["feature_set_id"],
                "model_config_id": validation["model_config_id"],
                "validation_pf": validation_pf,
                "validation_net": as_float(validation["net_log_return_after_cost"]),
                "validation_trades": as_int(validation["trade_count"]),
                "validation_status": validation_status,
                "oos_pf": oos_pf,
                "oos_net": as_float(oos["net_log_return_after_cost"]),
                "oos_trades": as_int(oos["trade_count"]),
                "oos_status": oos_status,
                "review_status": review_status,
                "effect": "separates validation survival from OOS pocket(검증 생존과 OOS 포켓을 분리)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(rows, key=lambda row: (-as_float(row["validation_pf"]), -as_float(row["oos_pf"])))


def build_divergence(pair_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in pair_rows:
        gap = as_float(row["oos_pf"]) - as_float(row["validation_pf"])
        if as_float(row["oos_pf"]) >= 1.10 and as_float(row["validation_pf"]) < 1.05:
            status = "oos_up_validation_thin_overfit_watch(OOS 상승/검증 얇음 과적합 관찰)"
        elif as_float(row["validation_pf"]) >= 1.05 and as_float(row["oos_pf"]) >= 1.05:
            status = "both_splits_cost_shape_pass(양쪽 분할 비용 곡선 통과)"
        else:
            status = "no_stable_pair_edge(안정 쌍 우위 없음)"
        rows.append(
            {
                "pair_id": row["pair_id"],
                "cost_policy_id": row["cost_policy_id"],
                "feature_set_id": row["feature_set_id"],
                "model_config_id": row["model_config_id"],
                "validation_pf": row["validation_pf"],
                "oos_pf": row["oos_pf"],
                "pf_gap_oos_minus_validation": gap,
                "validation_net": row["validation_net"],
                "oos_net": row["oos_net"],
                "divergence_status": status,
                "effect": "prevents choosing the OOS pocket as a winner(OOS 포켓을 승자로 고르는 것을 막음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(rows, key=lambda row: -as_float(row["pf_gap_oos_minus_validation"]))


def build_blockers(runtime: pd.DataFrame, pair_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    counts = Counter()
    for value in runtime["release_blockers"].astype(str):
        for item in value.split(";"):
            if item:
                counts[item] += 1
    validation_thin = sum(1 for row in pair_rows if as_float(row["validation_pf"]) < 1.05)
    oos_positive_validation_thin = sum(1 for row in pair_rows if as_float(row["oos_pf"]) >= 1.10 and as_float(row["validation_pf"]) < 1.05)
    counts["validation_pf_below_1p05"] += validation_thin
    counts["oos_positive_validation_thin_watch"] += oos_positive_validation_thin
    return [
        {
            "release_blocker": key,
            "rows": value,
            "effect": "keeps runtime probe blocked until DF evidence is repaired(DF 근거 수리 전 런타임 탐침 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def build_model_summary(score: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for family, group in score.groupby("target_family"):
        validation = group.loc[group["split"].astype(str).eq("validation")]
        oos = group.loc[group["split"].astype(str).eq("oos")]
        rows.append(
            {
                "target_family": family,
                "validation_balanced_max": float(validation["balanced_accuracy"].astype(float).max()),
                "validation_balanced_mean": float(validation["balanced_accuracy"].astype(float).mean()),
                "oos_balanced_max": float(oos["balanced_accuracy"].astype(float).max()),
                "model_rows": int(group["model_id"].nunique()),
                "effect": "shows what part of the two-stage stack learned signal(2단계 스택 중 어느 부분이 신호를 배웠는지 표시)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_rank_summary(rank: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (cost_policy, split), group in rank.groupby(["cost_policy_id", "split"]):
        passed = int(group["monotonic_status"].astype(str).eq("passed_rank_monotonic").sum())
        total = int(len(group))
        rows.append(
            {
                "cost_policy_id": cost_policy,
                "split": split,
                "rank_rows": total,
                "passed_rank_rows": passed,
                "pass_rate": passed / total if total else 0.0,
                "effect": "rank signal review for stage2 only(2단계 전용 순위 신호 검토)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DG_design_validation_pf_floor_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design validation PF floor repair without OOS selection(검증 PF 하한 수리를 OOS 선택 없이 설계)",
            "required_inputs": f"{rel(PAIR_SUMMARY)};{rel(VALIDATION_OOS_DIVERGENCE)}",
            "required_outputs": "train-only guard and validation-pocket failure memory(학습 전용 가드와 검증 포켓 실패 기억)",
            "blocked_if_missing": "validation pair rows(검증 쌍 행)",
            "forbidden_action": "no threshold lowering, no choosing OOS winner(임계값 낮추기 금지, OOS 승자 선택 금지)",
            "effect": "turns thin validation PF into repair design(얇은 검증 PF를 수리 설계로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DG_design_pair_stability_slices",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design pair stability slices by session/month/volatility(세션/월/변동성별 쌍 안정성 슬라이스 설계)",
            "required_inputs": rel(DE_PAIR),
            "required_outputs": "slice attribution materialization queue(슬라이스 귀속 물질화 대기열)",
            "blocked_if_missing": "pair scorecard(쌍 점수표)",
            "forbidden_action": "no pair selection before slice review(슬라이스 검토 전 쌍 선택 금지)",
            "effect": "checks whether OOS pocket is a regime artifact(OOS 포켓이 레짐 산물인지 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DG_preserve_no_mt5_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "preserve no-MT5 firewall before DF repair closes(DF 수리 전 MT5 금지 방화벽 유지)",
            "required_inputs": rel(RELEASE_BLOCKERS),
            "required_outputs": "no-release design gate(해제 금지 설계 게이트)",
            "blocked_if_missing": "release blockers(해제 차단 요소)",
            "forbidden_action": "no MT5 package from OOS-positive pocket(OOS 양수 포켓만으로 MT5 패키지 금지)",
            "effect": "keeps positive-looking OOS from becoming runtime claim(좋아 보이는 OOS가 런타임 주장으로 바뀌지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_row(gate_id: str, ok: bool, observed: Any, expected: Any, effect: str) -> dict[str, str]:
    return {
        "gate_id": gate_id,
        "status": "passed" if ok else "failed",
        "observed": str(observed),
        "expected": str(expected),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        gate_row("df_gate_parent_de_passed", final["de_failed_gate_rows"] == 0, final["de_failed_gate_rows"], 0, "DE 실패 게이트가 리뷰로 전파되지 않게 한다."),
        gate_row("df_gate_parent_points_to_df", final["de_next_action"] == RUN_ID, final["de_next_action"], RUN_ID, "DE next_action(다음 행동)과 DF 실행을 맞춘다."),
        gate_row("df_gate_onnx_parity_clear", final["onnx_parity_passed"] == final["onnx_parity_rows"], f"{final['onnx_parity_passed']}/{final['onnx_parity_rows']}", "all", "ONNX 동등성을 성능 문제와 분리한다."),
        gate_row("df_gate_runtime_release_zero", final["runtime_release_rows"] == 0, final["runtime_release_rows"], 0, "리뷰 전 해제를 금지한다."),
        gate_row("df_gate_validation_block_recorded", final["validation_pf_below_1p05_rows"] > 0, final["validation_pf_below_1p05_rows"], ">0", "검증 비용 곡선 차단을 기록한다."),
        gate_row("df_gate_oos_positive_watch_recorded", final["oos_positive_validation_thin_rows"] > 0, final["oos_positive_validation_thin_rows"], ">0", "OOS 양수/검증 얇음 감시 포켓을 기록한다."),
        gate_row("df_gate_stage1_signal_present", final["best_stage1_validation_balanced"] >= 0.60, final["best_stage1_validation_balanced"], ">=0.60", "1단계 신호가 완전히 무작위가 아님을 기록한다."),
        gate_row("df_gate_next_queue_created", final["queue_rows"] >= 3, final["queue_rows"], ">=3", "DG 수리 설계 대기열을 만든다."),
        gate_row("df_gate_no_selection", final["candidate_selection"] == "not_run", final["candidate_selection"], "not_run", "OOS 포켓 선택을 막는다."),
        gate_row("df_gate_no_mt5_probe", final["mt5_runtime_probe"] == "not_run", final["mt5_runtime_probe"], "not_run", "검증 차단 중 MT5 탐침을 막는다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    model_receipt = {
        "model_family": "DE two-stage training review(DE 2단계 학습 검토)",
        "target_and_label": "stage1 cost gate, stage2 rank/action(1단계 비용 게이트, 2단계 순위/행동)",
        "split_method": "train fit; validation/oos read-only(학습 fit, 검증/OOS 읽기 전용)",
        "selection_metric": "not_applicable_no_selection(선택 없음)",
        "secondary_metrics": "validation PF floor, OOS divergence, rank monotonicity(검증 PF 하한, OOS 괴리, 순위 단조성)",
        "threshold_policy": "no tuning in DF(DF 튜닝 없음)",
        "overfit_risk": "OOS-positive validation-thin pocket(OOS 양수/검증 얇음 포켓)",
        "calibration_risk": "classifier outputs not live probabilities(분류기 출력은 실거래 확률 아님)",
        "comparison_baseline": PARENT_RUN_ID,
        "validation_judgment": "review_blocks_runtime_probe",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherits DE/DD closed M5 UTC identity(DE/DD 닫힌 M5 UTC 정체성 상속)",
        "sample_scope": "review only of DE outputs(DE 산출물 검토 전용)",
        "missing_or_duplicate_check": "input presence gate(입력 존재 게이트)",
        "feature_label_boundary": "no new labels or features(새 라벨/피처 없음)",
        "split_boundary": "validation and OOS are read-only review(검증/OOS 읽기 전용 검토)",
        "leakage_risk": "choosing OOS-positive pair(OOS 양수 쌍 선택)",
        "data_hash_or_identity": {"de_final": sha256_file(DE_FINAL), "pair_scorecard": sha256_file(DE_PAIR)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "attribution_subject": RUN_ID,
        "best_validation_pf": final["best_validation_pf"],
        "best_oos_pf": final["best_oos_pf"],
        "oos_positive_validation_thin_rows": final["oos_positive_validation_thin_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "pair review, blockers, rank/model summaries(쌍 리뷰, 차단 요소, 순위/모델 요약)",
        "evidence_missing": "repair design, rerun, proxy/MT5 parity, MT5 probe(수리 설계, 재실행, 프록시/MT5 동등성, MT5 탐침)",
        "judgment_label": "training_review_blocks_runtime_probe",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "OOS는 좋아 보이는 포켓이 있지만 검증 PF가 얇아 아직 선택이나 MT5로 갈 수 없습니다.",
    }
    paths = [
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage = {
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
        "availability": "ignored_review_outputs_with_tracked_report(무시된 리뷰 산출물과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DF Two-Stage Training Review(2단계 학습 검토)

## Conclusion(결론)

run337DF(337DF 실행)는 run337DE(337DE 실행)를 review(검토)했다. ONNX parity(ONNX 동등성)는 `{final["onnx_parity_passed"]}/{final["onnx_parity_rows"]}`로 통과했고 stage1 signal(1단계 신호)은 validation balanced(검증 균형정확도) `{final["best_stage1_validation_balanced"]}`까지 확인됐다.

하지만 best validation PF(최고 검증 PF)는 `{final["best_validation_pf"]}`로 1.05를 넘지 못했다. 반면 best OOS PF(최고 OOS PF)는 `{final["best_oos_pf"]}`라서, 이 결과는 “선택 후보”가 아니라 OOS-positive/validation-thin overfit watch(OOS 양수/검증 얇음 과적합 관찰)이다.

Effect(효과): MT5 probe(MT5 탐침), candidate selection(후보 선택), Forward/Goal(전진/목표)을 모두 보류하고, run337DG(337DG 실행)에서 validation PF floor repair(검증 PF 하한 수리)와 slice stability(슬라이스 안정성)를 설계한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- validation_pf_below_1p05_rows(검증 PF 1.05 미만 행): `{final["validation_pf_below_1p05_rows"]}`
- oos_positive_validation_thin_rows(OOS 양수/검증 얇음 행): `{final["oos_positive_validation_thin_rows"]}`
- runtime_release_rows(런타임 해제 행): `{final["runtime_release_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DF

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): OOS positive pocket(OOS 양수 포켓)을 선택하지 않고 validation PF floor repair(검증 PF 하한 수리)로 넘긴다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(PAIR_SUMMARY)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337DF focus complete: two-stage training review(2단계 학습 검토)를 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DG(337DG 실행)에서 validation PF floor/slice stability(검증 PF 하한/슬라이스 안정성) 수리 설계를 연다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DF focus complete")
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
## Stage337 run337DF(337DF 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): ONNX parity(ONNX 동등성)는 통과했지만 validation PF(검증 PF)가 얇아 MT5/선택을 보류했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DE(337DE"
    if "## Stage337 run337DF(337DF 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_df_review_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 validation pocket cost-shape repair design(검증 포켓 비용 곡선 수리 설계)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DF(337DF 실행) reviewed cost shape two-stage handoff training(비용 곡선 2단계 인계 학습 검토). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DF(337DF 실행) reviewed cost shape"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DF reviewed cost shape two-stage handoff training(비용 곡선 2단계 인계 학습 검토) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DF reviewed cost shape"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "cost_shape_two_stage_handoff_training_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"best_validation_pf={final['best_validation_pf']};best_oos_pf={final['best_oos_pf']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_performance_attribution_result_judgment_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__two_stage_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "two_stage_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "pair_cost_validation_oos_review",
        "scoreboard_lane": "model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"validation_pf={final['best_validation_pf']};oos_pf={final['best_oos_pf']}",
        "guardrail_kpi": "no_selection;no_mt5;validation_pf_floor",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__two_stage_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_performance_attribution_result_judgment_artifact_lineage",
        "evidence_scope": "DE two-stage training reviewed without selection",
        "kpi_scope": "pair_validation_oos_divergence",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__two_stage_review",
        "family": "model_validation_performance_attribution_result_judgment_artifact_lineage",
        "question": "does two-stage training survive validation enough for runtime probe",
        "metric_scope": "pair_cost_curve_rank_onnx_release_blockers",
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
    de_final = read_json(DE_FINAL)
    frames = load_frames()
    pair_rows = build_pair_summary(frames["pair"])
    divergence_rows = build_divergence(pair_rows)
    blocker_rows = build_blockers(frames["runtime"], pair_rows)
    model_summary_rows = build_model_summary(frames["score"])
    rank_summary_rows = build_rank_summary(frames["rank"])
    queue_rows = build_queue()
    artifacts: list[Path] = [
        write_csv(PAIR_SUMMARY, PAIR_SUMMARY_COLUMNS, pair_rows),
        write_csv(VALIDATION_OOS_DIVERGENCE, DIVERGENCE_COLUMNS, divergence_rows),
        write_csv(RELEASE_BLOCKERS, BLOCKER_COLUMNS, blocker_rows),
        write_csv(MODEL_FAMILY_SUMMARY, MODEL_SUMMARY_COLUMNS, model_summary_rows),
        write_csv(RANK_STAGE_SUMMARY, RANK_SUMMARY_COLUMNS, rank_summary_rows),
        write_csv(DG_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    validation_pf_below = sum(1 for row in pair_rows if as_float(row["validation_pf"]) < 1.05)
    oos_positive_thin = sum(1 for row in pair_rows if as_float(row["oos_pf"]) >= 1.10 and as_float(row["validation_pf"]) < 1.05)
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "de_next_action": de_final.get("next_action", ""),
        "de_failed_gate_rows": len(de_final.get("failed_gates", [])),
        "onnx_parity_rows": int(len(frames["parity"])),
        "onnx_parity_passed": int(is_true_series(frames["parity"]["passed"]).sum()),
        "runtime_release_rows": int((frames["runtime"]["mt5_probe_disposition"].astype(str) != "held_for_review").sum()),
        "pair_rows": len(pair_rows),
        "best_validation_pf": max((as_float(row["validation_pf"]) for row in pair_rows), default=0.0),
        "best_oos_pf": max((as_float(row["oos_pf"]) for row in pair_rows), default=0.0),
        "validation_pf_below_1p05_rows": validation_pf_below,
        "oos_positive_validation_thin_rows": oos_positive_thin,
        "best_stage1_validation_balanced": float(de_final.get("best_stage1_validation_balanced") or 0.0),
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
