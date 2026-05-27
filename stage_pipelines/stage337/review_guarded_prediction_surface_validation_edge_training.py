from __future__ import annotations

import csv
import json
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
from stage_pipelines.stage337 import train_guarded_prediction_surface_validation_edge_repair_candidates as do  # noqa: E402
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
STAGE_ID = do.STAGE_ID
RUN_NUMBER = "run337DP"
RUN_ID = "run337DP_review_guarded_prediction_surface_validation_edge_training_without_db_v1"
PARENT_RUN_ID = do.RUN_ID
NEXT_RUN_ID = "run337DQ_design_validation_support_and_control_residual_repair_without_db_v1"
STATUS = "completed_stage337DP_guarded_training_review_validation_support_and_shifted_control_blocks_release_no_selection_no_mt5"
JUDGMENT = "onnx_clear_but_validation_pf_floor_and_shifted_control_blocks_release"
DECISION = "stage337DP_open_run337DQ_design_validation_support_and_control_residual_repair"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DP_guarded_prediction_surface_validation_edge_training_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = do.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = do.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DP_guarded_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DP_guarded_training_review.md"
SELECTED_STATUS = do.SELECTED_STATUS
STAGE_BRIEF = do.STAGE_BRIEF
WORKSPACE_STATE = do.WORKSPACE_STATE
CURRENT_STATE = do.CURRENT_STATE
CHANGELOG = do.CHANGELOG
RUN_REGISTRY = do.RUN_REGISTRY
ALPHA_LEDGER = do.ALPHA_LEDGER
ARTIFACT_REGISTRY = do.ARTIFACT_REGISTRY
STAGE_LEDGER = do.STAGE_LEDGER

DO_FINAL = do.FINAL_DECISION
DO_GATES = do.REQUIRED_GATE_AUDIT
DO_QUEUE = do.DP_QUEUE
DO_FEATURE_COMPATIBILITY = do.FEATURE_COMPATIBILITY
DO_MODEL_MANIFEST = do.TRAINED_MODEL_MANIFEST
DO_ONNX_PARITY = do.ONNX_PARITY
DO_CLASS_SCORECARD = do.CANDIDATE_SCORECARD
DO_PROXY_TRADE_SCORECARD = do.PROXY_TRADE_SCORECARD
DO_NEGATIVE_CONTROL_SCORECARD = do.NEGATIVE_CONTROL_SCORECARD
DO_SURFACE_BREADTH_SCORECARD = do.SURFACE_BREADTH_SCORECARD
DO_RUNTIME_FIREWALL_REVIEW = do.RUNTIME_FIREWALL_REVIEW
DO_RELEASE_DISPOSITION = do.RELEASE_DISPOSITION

CANDIDATE_TRAINING_REVIEW = RUN_DIR / "candidate_training_review.csv"
ONNX_PARITY_REVIEW = RUN_DIR / "onnx_parity_review.csv"
CONTROL_SURFACE_REVIEW = RUN_DIR / "control_surface_training_review.csv"
VALIDATION_OOS_GAP_REVIEW = RUN_DIR / "validation_oos_gap_review.csv"
RUNTIME_DISPOSITION_REVIEW = RUN_DIR / "training_runtime_disposition_review.csv"
DQ_QUEUE = RUN_DIR / "run337DQ_repair_design_queue.csv"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DO_FINAL,
    DO_GATES,
    DO_QUEUE,
    DO_FEATURE_COMPATIBILITY,
    DO_MODEL_MANIFEST,
    DO_ONNX_PARITY,
    DO_CLASS_SCORECARD,
    DO_PROXY_TRADE_SCORECARD,
    DO_NEGATIVE_CONTROL_SCORECARD,
    DO_SURFACE_BREADTH_SCORECARD,
    DO_RUNTIME_FIREWALL_REVIEW,
    DO_RELEASE_DISPOSITION,
)
OUTPUT_FILES = (
    CANDIDATE_TRAINING_REVIEW,
    ONNX_PARITY_REVIEW,
    CONTROL_SURFACE_REVIEW,
    VALIDATION_OOS_GAP_REVIEW,
    RUNTIME_DISPOSITION_REVIEW,
    DQ_QUEUE,
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

CANDIDATE_COLUMNS = (
    "model_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "validation_pf",
    "oos_pf",
    "pf_gap_oos_minus_validation",
    "validation_net",
    "oos_net",
    "validation_trade_count",
    "oos_trade_count",
    "validation_balanced_accuracy",
    "oos_balanced_accuracy",
    "validation_signal_density",
    "oos_signal_density",
    "validation_control_block_rows",
    "release_blockers",
    "review_status",
    "effect",
    "claim_boundary",
)
PARITY_COLUMNS = (
    "review_id",
    "model_rows",
    "parity_rows",
    "parity_passed_rows",
    "failed_rows",
    "feature_missing_rows",
    "review_status",
    "effect",
    "claim_boundary",
)
CONTROL_SURFACE_COLUMNS = (
    "review_id",
    "review_family",
    "split",
    "subject_id",
    "rows",
    "block_rows",
    "metric_1",
    "metric_2",
    "review_status",
    "effect",
    "claim_boundary",
)
GAP_COLUMNS = (
    "model_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "validation_pf",
    "oos_pf",
    "pf_gap_oos_minus_validation",
    "validation_trade_count",
    "oos_trade_count",
    "gap_status",
    "effect",
    "claim_boundary",
)
RUNTIME_COLUMNS = (
    "review_id",
    "release_rows",
    "held_rows",
    "auto_mt5_rows",
    "mt5_runtime_probe",
    "forward_claim",
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


def bool_count(series: pd.Series) -> int:
    return int(series.astype(str).str.lower().eq("true").sum())


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
        "models": pd.read_csv(io_path(DO_MODEL_MANIFEST)),
        "parity": pd.read_csv(io_path(DO_ONNX_PARITY)),
        "class_score": pd.read_csv(io_path(DO_CLASS_SCORECARD)),
        "trade_score": pd.read_csv(io_path(DO_PROXY_TRADE_SCORECARD)),
        "controls": pd.read_csv(io_path(DO_NEGATIVE_CONTROL_SCORECARD)),
        "surface": pd.read_csv(io_path(DO_SURFACE_BREADTH_SCORECARD)),
        "release": pd.read_csv(io_path(DO_RELEASE_DISPOSITION)),
        "runtime": pd.read_csv(io_path(DO_RUNTIME_FIREWALL_REVIEW)),
        "feature": pd.read_csv(io_path(DO_FEATURE_COMPATIBILITY)),
    }


def split_row(frame: pd.DataFrame, model_id: str, split: str) -> dict[str, Any]:
    rows = frame.loc[frame["model_id"].astype(str).eq(model_id) & frame["split"].astype(str).eq(split)]
    return rows.iloc[0].to_dict() if len(rows) else {}


def build_candidate_review(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    class_frame = frames["class_score"]
    trade_frame = frames["trade_score"]
    control_frame = frames["controls"]
    rows: list[dict[str, Any]] = []
    for release in frames["release"].to_dict("records"):
        model_id = str(release["model_id"])
        val_trade = split_row(trade_frame, model_id, "validation")
        oos_trade = split_row(trade_frame, model_id, "oos")
        val_class = split_row(class_frame, model_id, "validation")
        oos_class = split_row(class_frame, model_id, "oos")
        validation_pf = as_float(val_trade.get("profit_factor"))
        oos_pf = as_float(oos_trade.get("profit_factor"))
        control_blocks = len(
            control_frame.loc[
                control_frame["model_id"].astype(str).eq(model_id)
                & control_frame["split"].astype(str).eq("validation")
                & control_frame["blocks_training_review"].astype(str).str.lower().eq("true")
            ]
        )
        statuses: list[str] = []
        if validation_pf < 1.05:
            statuses.append("validation_pf_floor_block")
        if control_blocks:
            statuses.append("shifted_control_alignment_block")
        if oos_pf >= 1.10 and validation_pf < 1.05:
            statuses.append("oos_only_lift_quarantine")
        if as_int(val_trade.get("trade_count")) < 500:
            statuses.append("validation_trade_count_thin")
        rows.append(
            {
                "model_id": model_id,
                "cost_policy_id": release.get("task_id", "").split("__")[1] if "__" in str(release.get("task_id", "")) else "",
                "feature_set_id": val_trade.get("feature_set_id", ""),
                "model_config_id": val_trade.get("model_config_id", ""),
                "validation_pf": validation_pf,
                "oos_pf": oos_pf,
                "pf_gap_oos_minus_validation": oos_pf - validation_pf,
                "validation_net": as_float(val_trade.get("net_log_return_after_cost")),
                "oos_net": as_float(oos_trade.get("net_log_return_after_cost")),
                "validation_trade_count": as_int(val_trade.get("trade_count")),
                "oos_trade_count": as_int(oos_trade.get("trade_count")),
                "validation_balanced_accuracy": as_float(val_class.get("balanced_accuracy")),
                "oos_balanced_accuracy": as_float(oos_class.get("balanced_accuracy")),
                "validation_signal_density": as_float(val_trade.get("signal_density")),
                "oos_signal_density": as_float(oos_trade.get("signal_density")),
                "validation_control_block_rows": control_blocks,
                "release_blockers": release.get("release_blockers", ""),
                "review_status": ";".join(statuses) if statuses else "review_only_no_release",
                "effect": "blocks selection until validation/control review is repaired(검증/대조 수리 전 선택 차단)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_parity_review(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    parity = frames["parity"]
    feature = frames["feature"]
    failed = len(parity.loc[~parity["passed"].astype(str).str.lower().eq("true")])
    feature_missing = int(pd.to_numeric(feature["missing_count"], errors="coerce").fillna(0).sum())
    return [
        {
            "review_id": "do_onnx_feature_parity",
            "model_rows": len(frames["models"]),
            "parity_rows": len(parity),
            "parity_passed_rows": bool_count(parity["passed"]),
            "failed_rows": failed,
            "feature_missing_rows": feature_missing,
            "review_status": "parity_clear_review_only" if failed == 0 and feature_missing == 0 else "parity_or_feature_block",
            "effect": "permits review but not runtime package(검토는 허용하지만 런타임 패키지는 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_control_surface_review(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    controls = frames["controls"].copy()
    controls["block_bool"] = controls["blocks_training_review"].astype(str).str.lower().eq("true")
    for (split, control_id), group in controls.groupby(["split", "control_id"], dropna=False):
        rows.append(
            {
                "review_id": f"control__{split}__{control_id}",
                "review_family": "negative_control(부정대조)",
                "split": split,
                "subject_id": control_id,
                "rows": len(group),
                "block_rows": int(group["block_bool"].sum()),
                "metric_1": float(pd.to_numeric(group["candidate_balanced_accuracy"], errors="coerce").mean()),
                "metric_2": float(pd.to_numeric(group["control_alignment_balanced_accuracy"], errors="coerce").max()),
                "review_status": "control_blocks_release" if int(group["block_bool"].sum()) else "control_scored_no_block",
                "effect": "finds overfit-like alignment before release(해제 전 과적합성 정렬 탐지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    surface = frames["surface"]
    for row in surface.to_dict("records"):
        mean_pf = as_float(row.get("mean_pf"))
        split = str(row.get("split", ""))
        status = "surface_validation_pf_floor_block" if split == "validation" and mean_pf < 1.05 else "surface_diagnostic_only"
        rows.append(
            {
                "review_id": f"surface__{row.get('surface_id', '')}",
                "review_family": "surface_breadth(표면 폭)",
                "split": split,
                "subject_id": f"{row.get('group_field', '')}={row.get('group_value', '')}",
                "rows": as_int(row.get("model_rows")),
                "block_rows": 1 if status == "surface_validation_pf_floor_block" else 0,
                "metric_1": mean_pf,
                "metric_2": as_float(row.get("mean_signal_density")),
                "review_status": status,
                "effect": "checks whether weak validation is broad or isolated(약한 검증이 넓은지 고립인지 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    blocker_counter: Counter[str] = Counter()
    for value in frames["release"]["release_blockers"].astype(str):
        for blocker in [item for item in value.split(";") if item]:
            blocker_counter[blocker] += 1
    for blocker, count in sorted(blocker_counter.items()):
        rows.append(
            {
                "review_id": f"release_blocker__{blocker}",
                "review_family": "release_blocker(해제 차단)",
                "split": "validation",
                "subject_id": blocker,
                "rows": count,
                "block_rows": count,
                "metric_1": float(count),
                "metric_2": 0.0,
                "review_status": "release_blocker_materialized",
                "effect": "keeps release blocker explicit(해제 차단 사유를 명시)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gap_review(candidate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in candidate_rows:
        validation_pf = as_float(row["validation_pf"])
        oos_pf = as_float(row["oos_pf"])
        gap = oos_pf - validation_pf
        if oos_pf >= 1.10 and validation_pf < 1.05:
            status = "oos_only_lift_quarantined"
        elif validation_pf < 1.05:
            status = "validation_floor_block"
        else:
            status = "gap_review_only_no_selection"
        rows.append(
            {
                "model_id": row["model_id"],
                "cost_policy_id": row["cost_policy_id"],
                "feature_set_id": row["feature_set_id"],
                "model_config_id": row["model_config_id"],
                "validation_pf": validation_pf,
                "oos_pf": oos_pf,
                "pf_gap_oos_minus_validation": gap,
                "validation_trade_count": row["validation_trade_count"],
                "oos_trade_count": row["oos_trade_count"],
                "gap_status": status,
                "effect": "prevents OOS-only lift from becoming selection(표본외 단독 개선이 선택으로 변하는 것을 차단)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_runtime_review(frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    release = frames["release"]
    held_rows = int(release["release_disposition"].astype(str).eq("held_for_review_no_selection").sum())
    return [
        {
            "review_id": "do_runtime_firewall_preserved",
            "release_rows": len(release),
            "held_rows": held_rows,
            "auto_mt5_rows": 0,
            "mt5_runtime_probe": "not_run",
            "forward_claim": "not_claimed",
            "review_status": "runtime_firewall_preserved_no_release",
            "effect": "keeps MT5/Forward authority closed(MT5/전진 권위 닫힘 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_dq_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DQ_design_validation_pf_floor_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design validation support repair without selecting DO winners(DO 승자 선택 없이 검증 지지 수리 설계)",
            "required_inputs": rel(CANDIDATE_TRAINING_REVIEW),
            "required_outputs": "validation_support_repair_design.csv",
            "blocked_if_missing": "candidate training review(후보 학습 검토)",
            "forbidden_action": "no threshold tuning or OOS winner selection(임계값 튜닝 또는 표본외 승자 선택 금지)",
            "effect": "turns validation weakness into a repair question(검증 약점을 수리 질문으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DQ_design_shifted_control_residual_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design shifted-control residual repair(이동 대조 잔차 수리 설계)",
            "required_inputs": rel(CONTROL_SURFACE_REVIEW),
            "required_outputs": "control_residual_repair_design.csv",
            "blocked_if_missing": "control surface review(대조 표면 검토)",
            "forbidden_action": "no runtime probe while shifted controls block(이동 대조 차단 중 런타임 탐침 금지)",
            "effect": "keeps serial/overfit risk ahead of runtime claims(연속/과적합 위험을 런타임 주장보다 앞에 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DQ_quarantine_oos_only_lift",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "quarantine OOS-only lift pockets(표본외 단독 개선 포켓 격리)",
            "required_inputs": rel(VALIDATION_OOS_GAP_REVIEW),
            "required_outputs": "oos_only_lift_quarantine.csv",
            "blocked_if_missing": "validation/OOS gap review(검증/OOS 간극 검토)",
            "forbidden_action": "no selection from OOS gap(OOS 간극으로 선택 금지)",
            "effect": "keeps attractive OOS numbers from becoming overfit pressure(매력적인 OOS 숫자가 과적합 압력이 되는 것을 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DQ_preserve_no_mt5_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "preserve no-MT5/no-Forward firewall(무MT5/무전진 방화벽 보존)",
            "required_inputs": rel(RUNTIME_DISPOSITION_REVIEW),
            "required_outputs": "runtime_firewall_repair_design.csv",
            "blocked_if_missing": "runtime disposition review(런타임 처분 검토)",
            "forbidden_action": "no MT5 package until validation/control repair passes(검증/대조 수리 통과 전 MT5 패키지 금지)",
            "effect": "keeps operating boundary closed(운영 경계 닫힘 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DO outputs exist(필수 DO 출력 존재)"),
        ("parent_do_gates_passed", final["do_failed_gate_rows"] == 0, str(final["do_failed_gate_rows"]), "0", "DO training evidence usable(DO 학습 근거 사용 가능)"),
        ("parent_next_action_matches", final["do_next_action"] == RUN_ID, str(final["do_next_action"]), RUN_ID, "continues DO queue(DO 대기열을 이어감)"),
        ("candidate_rows_reviewed", final["candidate_review_rows"] == final["trained_models"], f"{final['candidate_review_rows']}/{final['trained_models']}", "all", "all trained rows reviewed(모든 학습 행 검토)"),
        ("parity_review_clear", final["parity_failed_rows"] == 0 and final["parity_passed_rows"] == final["parity_rows"], f"failed={final['parity_failed_rows']};passed={final['parity_passed_rows']}/{final['parity_rows']}", "failed=0;passed=all", "ONNX parity remains clear(ONNX 동등성 유지)"),
        ("validation_floor_block_materialized", final["validation_pf_below_1p05_rows"] > 0, str(final["validation_pf_below_1p05_rows"]), ">0", "validation weakness explicitly recorded(검증 약점 명시 기록)"),
        ("control_review_materialized", final["negative_control_rows"] == 108 and final["control_block_rows"] >= 0, f"controls={final['negative_control_rows']};blocks={final['control_block_rows']}", "108;>=0", "controls reviewed(대조 검토 완료)"),
        ("surface_review_materialized", final["surface_review_rows"] >= 24, str(final["surface_review_rows"]), ">=24", "surface breadth reviewed(표면 폭 검토 완료)"),
        ("release_blocked", final["release_candidate_rows"] == 0 and final["auto_mt5_release_rows"] == 0, f"release={final['release_candidate_rows']};mt5={final['auto_mt5_release_rows']}", "0/0", "release and MT5 remain blocked(해제와 MT5 계속 차단)"),
        ("dq_queue_materialized", final["dq_queue_rows"] == 4, str(final["dq_queue_rows"]), "4", "repair queue opened(수리 대기열 열림)"),
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
    model_receipt = {
        "model_family": "review-only of DO logreg/extra-trees ONNX outputs(DO 로지스틱/엑스트라트리 ONNX 출력 검토 전용)",
        "target_and_label": "unchanged DO costed action label(DO 비용 반영 행동 라벨 유지)",
        "split_method": "train was fit in DO; DP reviews validation/OOS only(DO 학습 후 DP는 검증/OOS만 검토)",
        "selection_metric": "none; validation/control blockers prevent selection(없음, 검증/대조 차단으로 선택 금지)",
        "secondary_metrics": "validation PF, OOS PF, PF gap, controls, surface breadth, ONNX parity(검증 PF/OOS PF/PF 간극/대조/표면 폭/ONNX 동등성)",
        "threshold_policy": "unchanged argmax review; no threshold tuning(argmax 검토 유지, 임계값 튜닝 없음)",
        "overfit_risk": "OOS-only lift after weak validation(약한 검증 뒤 표본외 단독 개선)",
        "calibration_risk": "probabilities are not promoted as calibrated(확률을 보정 확률로 승격하지 않음)",
        "comparison_baseline": rel(DO_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherits DO source_row_id UTC bar alignment(DO source_row_id UTC 봉 정렬 상속)",
        "sample_scope": f"trained_models={final['trained_models']};candidate_review_rows={final['candidate_review_rows']}",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']};feature_missing_rows={final['feature_missing_rows']}",
        "feature_label_boundary": "no new feature or label construction in DP(DP에서 새 피처/라벨 생성 없음)",
        "split_boundary": "validation/OOS score review only(검증/OOS 점수 검토 전용)",
        "leakage_risk": "using OOS lift as selection pressure(OOS 개선을 선택 압력으로 쓰는 위험)",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_review_no_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"best_validation_pf={final['best_validation_pf']};best_oos_pf={final['best_oos_pf']};oos_only_lift_rows={final['oos_only_lift_rows']}",
        "comparison_baseline": rel(DO_FINAL),
        "likely_drivers": "validation weakness, cost surface, shifted control residual(검증 약점/비용 표면/이동 대조 잔차)",
        "segment_checks": f"surface_review_rows={final['surface_review_rows']};validation_pf_below_rows={final['validation_pf_below_1p05_rows']}",
        "trade_shape": f"best_validation_trades={final['best_validation_trade_count']};best_oos_trades={final['best_oos_trade_count']}",
        "alternative_explanations": "proxy cost mismatch, residual serial dependence, class imbalance(프록시 비용 불일치/잔여 연속 의존/클래스 불균형)",
        "attribution_confidence": "medium_for_blocker_low_for_runtime(차단 판단은 중간, 런타임은 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "DO scorecards, parity, controls, surface, release disposition(DO 점수표/동등성/대조/표면/해제 처분)",
        "evidence_missing": "repair design, repaired training, MT5 runtime probe, forward data(수리 설계/수리 학습/MT5 런타임 탐침/전진 데이터)",
        "judgment_label": "release_blocked_repair_design_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "ONNX는 맞게 나왔지만 검증 지지가 너무 약하고 일부 대조가 걸려서 아직 고르면 안 된다.",
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
    text = f"""# Stage337 run337DP Guarded Training Review(방어 학습 검토)

## Conclusion(결론)

run337DP(337DP 실행)는 run337DO(337DO 실행)의 ONNX parity(ONNX 동등성), proxy scorecard(프록시 점수표), negative control(부정대조), surface breadth(표면 폭), release disposition(해제 처분)을 검토했다.

ONNX parity(ONNX 동등성)는 clear(명확)하지만, validation PF floor(검증 PF 하한)와 shifted control residual(이동 대조 잔차)이 release(해제)를 막는다.

Effect(효과): attractive OOS lift(매력적인 표본외 개선)는 quarantine(격리)하고, run337DQ(337DQ 실행)에서 validation support/control residual repair design(검증 지지/대조 잔차 수리 설계)을 연다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- candidate_review_rows(후보 검토 행): `{final["candidate_review_rows"]}`
- best_validation_pf(최고 검증 PF): `{final["best_validation_pf"]}`
- best_oos_pf(최고 OOS PF): `{final["best_oos_pf"]}`
- validation_pf_below_1p05_rows(검증 PF 1.05 미만 행): `{final["validation_pf_below_1p05_rows"]}`
- oos_only_lift_rows(OOS 단독 개선 행): `{final["oos_only_lift_rows"]}`
- control_block_rows(대조 차단 행): `{final["control_block_rows"]}`
- release_candidate_rows(해제 후보 행): `{final["release_candidate_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DP

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): ONNX parity(ONNX 동등성)는 보존하지만 validation/control(검증/대조) 차단으로 선택/MT5/Forward(전진)를 계속 닫는다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(CANDIDATE_TRAINING_REVIEW)}`, `{rel(CONTROL_SURFACE_REVIEW)}`
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
        f"  Stage337 run337DP focus complete: guarded training review(방어 학습 검토)를 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DQ(337DQ 실행)에서 validation support/control residual repair design(검증 지지/대조 잔차 수리 설계)을 연다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DP focus complete")
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
    section = f"""## Stage337 run337DP(337DP 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): ONNX parity(ONNX 동등성)는 통과했지만 검증/대조 차단으로 선택/MT5/Forward(전진)는 주장하지 않는다. Goal(목표)은 주장하지 않는다."""
    current_text = append_once(current_text, section, "Stage337 run337DP(337DP 실행)")
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection_text, _ = read_text_lossless(SELECTED_STATUS)
    selection = selection_text
    for field_name, value in {
        "latest_run": f"`{RUN_ID}`",
        "latest_decision": f"`{DECISION}`",
        "current_run": f"`{NEXT_RUN_ID}`",
        "rebuild_status": f"`{STATUS}`",
        "actual_mt5_execution": "`not_run_dp_review_only`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "effect": "`다음은 validation support/control residual repair design(검증 지지/대조 잔차 수리 설계)이다.`",
    }.items():
        selection = replace_bullet_value(selection, field_name, value)
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337DP(337DP 실행) reviewed DO guarded training, blocked release on validation/control, and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DP(337DP 실행) reviewed DO guarded training"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DP reviewed guarded training outputs, kept selection/MT5/Forward closed, "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DP reviewed guarded training"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "guarded_prediction_surface_validation_edge_training_review_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"validation_pf_below={final['validation_pf_below_1p05_rows']};control_blocks={final['control_block_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__guarded_training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "guarded_training_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "proxy_training_review",
        "scoreboard_lane": "model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_validation_pf={final['best_validation_pf']};best_oos_pf={final['best_oos_pf']}",
        "guardrail_kpi": "validation_floor;controls;surface;no_selection;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__guarded_training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_performance_attribution_result_judgment",
        "evidence_scope": "guarded training outputs reviewed",
        "kpi_scope": "proxy_scorecard_control_surface_onnx",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__guarded_training_review",
        "family": "model_validation_performance_attribution_result_judgment",
        "question": "do DO candidates survive validation/control review without selection",
        "metric_scope": "validation_pf_oos_gap_controls_surface_onnx",
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
    candidate_rows = build_candidate_review(frames)
    parity_rows = build_parity_review(frames)
    control_surface_rows = build_control_surface_review(frames)
    gap_rows = build_gap_review(candidate_rows)
    runtime_rows = build_runtime_review(frames)
    queue_rows = build_dq_queue()

    artifacts: list[Path] = [
        write_csv(CANDIDATE_TRAINING_REVIEW, CANDIDATE_COLUMNS, candidate_rows),
        write_csv(ONNX_PARITY_REVIEW, PARITY_COLUMNS, parity_rows),
        write_csv(CONTROL_SURFACE_REVIEW, CONTROL_SURFACE_COLUMNS, control_surface_rows),
        write_csv(VALIDATION_OOS_GAP_REVIEW, GAP_COLUMNS, gap_rows),
        write_csv(RUNTIME_DISPOSITION_REVIEW, RUNTIME_COLUMNS, runtime_rows),
        write_csv(DQ_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]

    do_final = read_json(DO_FINAL)
    do_failed_gate_rows = sum(1 for row in read_csv(DO_GATES) if row.get("status") != "passed")
    best_validation = max(candidate_rows, key=lambda row: as_float(row["validation_pf"])) if candidate_rows else {}
    best_oos = max(candidate_rows, key=lambda row: as_float(row["oos_pf"])) if candidate_rows else {}
    validation_floor_rows = sum(1 for row in candidate_rows if as_float(row["validation_pf"]) < 1.05)
    oos_only_lift_rows = sum(1 for row in gap_rows if row["gap_status"] == "oos_only_lift_quarantined")
    control_block_rows = sum(
        as_int(row["block_rows"])
        for row in control_surface_rows
        if row["review_family"].startswith("negative_control")
    )
    release_candidate_rows = sum(1 for row in frames["release"].to_dict("records") if row.get("release_disposition") != "held_for_review_no_selection")
    parity = frames["parity"]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "do_next_action": do_final.get("next_action", ""),
        "do_failed_gate_rows": do_failed_gate_rows,
        "missing_inputs": len(missing),
        "trained_models": int(do_final.get("trained_models", len(frames["models"]))),
        "candidate_review_rows": len(candidate_rows),
        "parity_rows": len(parity),
        "parity_passed_rows": bool_count(parity["passed"]),
        "parity_failed_rows": len(parity.loc[~parity["passed"].astype(str).str.lower().eq("true")]),
        "feature_missing_rows": int(pd.to_numeric(frames["feature"]["missing_count"], errors="coerce").fillna(0).sum()),
        "negative_control_rows": len(frames["controls"]),
        "control_block_rows": control_block_rows,
        "surface_review_rows": len(control_surface_rows),
        "validation_pf_below_1p05_rows": validation_floor_rows,
        "oos_only_lift_rows": oos_only_lift_rows,
        "best_validation_model_id": best_validation.get("model_id", ""),
        "best_validation_pf": as_float(best_validation.get("validation_pf")),
        "best_validation_trade_count": as_int(best_validation.get("validation_trade_count")),
        "best_oos_model_id": best_oos.get("model_id", ""),
        "best_oos_pf": as_float(best_oos.get("oos_pf")),
        "best_oos_trade_count": as_int(best_oos.get("oos_trade_count")),
        "release_candidate_rows": release_candidate_rows,
        "auto_mt5_release_rows": 0,
        "dq_queue_rows": len(queue_rows),
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
