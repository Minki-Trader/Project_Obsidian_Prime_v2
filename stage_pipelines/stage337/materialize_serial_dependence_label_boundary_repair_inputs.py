from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
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
from stage_pipelines.stage337.train_guarded_directional_label_action_candidates import (  # noqa: E402
    CANDIDATE_INPUT_MANIFEST,
    LABEL_CANDIDATE_MATRIX,
    SOURCE_MODEL_INPUT,
    label_values,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CN"
RUN_ID = "run337CN_materialize_serial_dependence_label_boundary_repair_inputs_without_db_v1"
PARENT_RUN_ID = "run337CM_design_serial_dependence_label_boundary_repair_without_db_v1"
NEXT_RUN_ID = "run337CO_train_purged_serial_dependence_guarded_candidates_without_db_v1"
STATUS = "completed_stage337CN_serial_dependence_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "repair_inputs_materialized_purged_nonoverlap_controls_ready_for_guarded_training"
DECISION = "stage337CN_open_run337CO_train_purged_serial_dependence_guarded_candidates"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CN_serial_dependence_label_boundary_repair_inputs_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
EXPECTED_FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CN_serial_dependence_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CN_serial_dependence_repair_inputs.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CM_DIR = STAGE_DIR / "02_runs" / "run337CM"
CM_FINAL = CM_DIR / "final_decision.json"
CM_LABEL_AUTOCORR = CM_DIR / "label_autocorrelation_and_shift_gap_matrix.csv"
CM_RETURN_AUTOCORR = CM_DIR / "future_return_autocorrelation_matrix.csv"
CM_PURGED_CONTRACT = CM_DIR / "purged_embargo_split_contract_candidate.csv"
CM_NONOVERLAP_PLAN = CM_DIR / "nonoverlap_horizon_negative_control_plan.csv"
CM_DIRECTION_FLIP = CM_DIR / "direction_flip_attribution_matrix.csv"

PURGED_MEMBERSHIP = RUN_DIR / "purged_embargo_split_membership.parquet"
PURGED_SUMMARY = RUN_DIR / "purged_embargo_split_summary.csv"
CANDIDATE_LABEL_FRAME = RUN_DIR / "candidate_label_frame.parquet"
LABEL_SHIFT_CONTROL_FRAME = RUN_DIR / "label_shift_control_frame.parquet"
BLOCK_PERMUTATION_MANIFEST = RUN_DIR / "block_permutation_control_manifest.csv"
TRAINING_TASK_MATRIX = RUN_DIR / "materialized_training_task_matrix.csv"
REPAIR_INPUT_MANIFEST = RUN_DIR / "repair_input_manifest.json"
CO_QUEUE = RUN_DIR / "run337CO_guarded_training_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CM_FINAL,
    CM_LABEL_AUTOCORR,
    CM_RETURN_AUTOCORR,
    CM_PURGED_CONTRACT,
    CM_NONOVERLAP_PLAN,
    CM_DIRECTION_FLIP,
    SOURCE_MODEL_INPUT,
    LABEL_CANDIDATE_MATRIX,
    CANDIDATE_INPUT_MANIFEST,
)
OUTPUT_FILES = (
    PURGED_MEMBERSHIP,
    PURGED_SUMMARY,
    CANDIDATE_LABEL_FRAME,
    LABEL_SHIFT_CONTROL_FRAME,
    BLOCK_PERMUTATION_MANIFEST,
    TRAINING_TASK_MATRIX,
    REPAIR_INPUT_MANIFEST,
    CO_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
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

PURGED_SUMMARY_COLUMNS = (
    "contract_id",
    "purge_gap_bars",
    "embargo_bars",
    "base_train_rows",
    "base_validation_rows",
    "base_oos_rows",
    "effective_train_rows",
    "effective_validation_rows",
    "effective_oos_rows",
    "holdout_rows",
    "train_boundary_holdout_rows",
    "oos_boundary_holdout_rows",
    "claim_boundary",
)
BLOCK_COLUMNS = (
    "control_id",
    "block_id",
    "block_type",
    "split",
    "start_timestamp",
    "end_timestamp",
    "rows",
    "permutation_seed",
    "claim_boundary",
)
TASK_COLUMNS = (
    "task_id",
    "next_run_id",
    "label_candidate_id",
    "contract_id",
    "model_family",
    "required_label_frame",
    "required_split_membership",
    "required_control_frame",
    "selection_use",
    "blocked_if",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_shortcut",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")

MODEL_FAMILIES = ("logreg_balanced_c075", "extratrees_depth6_leaf160")
SHIFT_CONTROLS = (("label_shift_gap24_control", 24), ("label_shift_gap48_control", 48))


def read_source_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(SOURCE_MODEL_INPUT)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    frame["source_row_id"] = np.arange(len(frame), dtype=np.int64)
    return frame


def write_parquet(path: Path, frame: pd.DataFrame) -> Path:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return path


def split_boundaries(frame: pd.DataFrame) -> tuple[int, int]:
    split = frame["split"].astype(str).to_numpy()
    transitions = np.flatnonzero(split[1:] != split[:-1]) + 1
    if len(transitions) < 2:
        raise RuntimeError("Expected contiguous train, validation, and oos split transitions.")
    train_validation_boundary = int(transitions[0])
    validation_oos_boundary = int(transitions[1])
    observed_order = [split[0], split[train_validation_boundary], split[validation_oos_boundary]]
    if observed_order != ["train", "validation", "oos"]:
        raise RuntimeError(f"Unexpected split order: {observed_order}")
    return train_validation_boundary, validation_oos_boundary


def build_purged_membership(
    frame: pd.DataFrame,
    contracts: Sequence[Mapping[str, str]],
) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    train_validation_boundary, validation_oos_boundary = split_boundaries(frame)
    base_counts = frame["split"].astype(str).value_counts().to_dict()
    positions = frame["source_row_id"].to_numpy()
    chunks: list[pd.DataFrame] = []
    summary_rows: list[dict[str, Any]] = []
    base = frame[["source_row_id", "timestamp", "split"]].rename(columns={"split": "base_split"})
    for contract in contracts:
        contract_id = contract["contract_id"]
        gap = int(contract["purge_gap_bars"])
        embargo = int(contract["embargo_bars"])
        train_boundary_mask = np.abs(positions - train_validation_boundary) < gap
        oos_boundary_mask = np.abs(positions - validation_oos_boundary) < gap
        holdout_mask = train_boundary_mask | oos_boundary_mask
        boundary_distance = np.minimum(
            np.abs(positions - train_validation_boundary),
            np.abs(positions - validation_oos_boundary),
        )
        effective = base["base_split"].astype(str).to_numpy().copy()
        effective[holdout_mask] = "embargo_holdout"
        member = base.copy()
        member["contract_id"] = contract_id
        member["purge_gap_bars"] = gap
        member["embargo_bars"] = embargo
        member["boundary_distance_bars"] = boundary_distance.astype(np.int64)
        member["effective_split"] = effective
        member["train_boundary_holdout"] = train_boundary_mask
        member["oos_boundary_holdout"] = oos_boundary_mask
        member["usable_for_training"] = member["effective_split"].eq("train")
        member["usable_for_validation"] = member["effective_split"].eq("validation")
        member["usable_for_oos"] = member["effective_split"].eq("oos")
        member["claim_boundary"] = CLAIM_BOUNDARY
        chunks.append(member)
        effective_counts = member["effective_split"].value_counts().to_dict()
        summary_rows.append(
            {
                "contract_id": contract_id,
                "purge_gap_bars": gap,
                "embargo_bars": embargo,
                "base_train_rows": int(base_counts.get("train", 0)),
                "base_validation_rows": int(base_counts.get("validation", 0)),
                "base_oos_rows": int(base_counts.get("oos", 0)),
                "effective_train_rows": int(effective_counts.get("train", 0)),
                "effective_validation_rows": int(effective_counts.get("validation", 0)),
                "effective_oos_rows": int(effective_counts.get("oos", 0)),
                "holdout_rows": int(effective_counts.get("embargo_holdout", 0)),
                "train_boundary_holdout_rows": int(train_boundary_mask.sum()),
                "oos_boundary_holdout_rows": int(oos_boundary_mask.sum()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.concat(chunks, ignore_index=True), summary_rows


def build_candidate_label_frame(frame: pd.DataFrame, candidates: Sequence[Mapping[str, str]]) -> pd.DataFrame:
    chunks: list[pd.DataFrame] = []
    base = frame[["source_row_id", "timestamp", "split"]].copy()
    for candidate in candidates:
        y = label_values(frame, candidate)
        candidate_frame = base.copy()
        candidate_frame["label_candidate_id"] = candidate["candidate_id"]
        candidate_frame["label_class"] = y.astype(np.int64)
        candidate_frame["label_name"] = pd.Series(y).map({0: "short", 1: "flat", 2: "long"}).to_numpy()
        candidate_frame["claim_boundary"] = CLAIM_BOUNDARY
        chunks.append(candidate_frame)
    return pd.concat(chunks, ignore_index=True)


def build_shift_control_frame(label_frame: pd.DataFrame) -> pd.DataFrame:
    chunks: list[pd.DataFrame] = []
    ordered = label_frame.sort_values(["label_candidate_id", "split", "source_row_id"]).copy()
    for control_id, gap in SHIFT_CONTROLS:
        control = ordered.copy()
        control["control_id"] = control_id
        control["shift_gap_bars"] = gap
        control["control_label_class"] = (
            control.groupby(["label_candidate_id", "split"], sort=False)["label_class"].shift(gap)
        )
        control["usable"] = control["control_label_class"].notna()
        control["control_label_class"] = control["control_label_class"].fillna(-1).astype(np.int64)
        control["control_label_name"] = control["control_label_class"].map(
            {0: "short", 1: "flat", 2: "long", -1: "missing_shift"}
        )
        control["same_class"] = control["label_class"].eq(control["control_label_class"])
        control["claim_boundary"] = CLAIM_BOUNDARY
        chunks.append(
            control[
                [
                    "control_id",
                    "label_candidate_id",
                    "source_row_id",
                    "timestamp",
                    "split",
                    "label_class",
                    "label_name",
                    "control_label_class",
                    "control_label_name",
                    "usable",
                    "same_class",
                    "shift_gap_bars",
                    "claim_boundary",
                ]
            ].rename(columns={"label_class": "actual_label_class", "label_name": "actual_label_name"})
        )
    return pd.concat(chunks, ignore_index=True)


def build_block_manifest(frame: pd.DataFrame) -> list[dict[str, Any]]:
    source = frame[["source_row_id", "timestamp", "split"]].copy()
    source["date_block"] = source["timestamp"].dt.strftime("%Y-%m-%d")
    iso = source["timestamp"].dt.isocalendar()
    source["week_block"] = iso["year"].astype(str) + "-W" + iso["week"].astype(str).str.zfill(2)
    rows: list[dict[str, Any]] = []
    for control_id, block_type, column, seed_base in (
        ("day_block_permutation_control", "day", "date_block", 337241),
        ("week_block_permutation_control", "week", "week_block", 337481),
    ):
        grouped = source.groupby(["split", column], sort=True)
        for idx, ((split, block_id), group) in enumerate(grouped):
            rows.append(
                {
                    "control_id": control_id,
                    "block_id": str(block_id),
                    "block_type": block_type,
                    "split": str(split),
                    "start_timestamp": str(group["timestamp"].min()),
                    "end_timestamp": str(group["timestamp"].max()),
                    "rows": int(group.shape[0]),
                    "permutation_seed": int(seed_base + idx),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_training_tasks(
    candidates: Sequence[Mapping[str, str]],
    contracts: Sequence[Mapping[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for candidate in candidates:
        candidate_id = candidate["candidate_id"]
        for contract in contracts:
            contract_id = contract["contract_id"]
            for model_family in MODEL_FAMILIES:
                rows.append(
                    {
                        "task_id": f"{candidate_id}__{contract_id}__{model_family}",
                        "next_run_id": NEXT_RUN_ID,
                        "label_candidate_id": candidate_id,
                        "contract_id": contract_id,
                        "model_family": model_family,
                        "required_label_frame": rel(CANDIDATE_LABEL_FRAME),
                        "required_split_membership": rel(PURGED_MEMBERSHIP),
                        "required_control_frame": rel(LABEL_SHIFT_CONTROL_FRAME),
                        "selection_use": "none_training_diagnostic_only(선택 없음, 학습 진단 전용)",
                        "blocked_if": (
                            "shift controls(이동 대조)가 actual(실제)보다 강하거나 purge(제거)가 "
                            "validation/OOS(검증/실외표본) 밀도를 무너뜨리면 차단"
                        ),
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return rows


def build_co_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337CO_purged_guarded_training",
            "next_run_id": NEXT_RUN_ID,
            "task": (
                "CN purged split membership(제거 분할 소속)으로 guarded candidates(방어 후보)를 "
                "학습하고 non-overlap controls(비중첩 대조)를 채점"
            ),
            "required_inputs": ";".join(
                rel(path)
                for path in (
                    CANDIDATE_LABEL_FRAME,
                    PURGED_MEMBERSHIP,
                    LABEL_SHIFT_CONTROL_FRAME,
                    TRAINING_TASK_MATRIX,
                    REPAIR_INPUT_MANIFEST,
                )
            ),
            "required_outputs": (
                "purged_guarded_model_scorecard.csv;nonoverlap_control_scorecard.csv;"
                "onnx_parity_matrix.csv;runtime_probe_disposition.csv"
            ),
            "blocked_if_missing": (
                "label frame(라벨 프레임), split membership(분할 소속), shift control frame(이동 대조 프레임), "
                "training task matrix(학습 작업 행렬) 중 누락 시 차단"
            ),
            "forbidden_shortcut": (
                "threshold tuning(임계값 조정), profit-based purge-gap selection(수익 기반 제거 간격 선택), "
                "negative controls(부정 대조) 전 MT5 probe(MT5 탐침) 금지"
            ),
            "effect": (
                "runtime work(런타임 작업) 전에 candidate signal(후보 신호)이 purge/embargo(제거/격리)와 "
                "shifted-label controls(이동 라벨 대조)를 버티는지 본다"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_manifest(
    frame: pd.DataFrame,
    candidates: Sequence[Mapping[str, str]],
    contracts: Sequence[Mapping[str, str]],
    purged_summary: Sequence[Mapping[str, Any]],
    task_rows: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    source_manifest = read_json(CANDIDATE_INPUT_MANIFEST)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_model_input": rel(SOURCE_MODEL_INPUT),
        "source_sha256": sha256_file(SOURCE_MODEL_INPUT),
        "source_rows": int(len(frame)),
        "feature_columns": source_manifest.get("feature_columns", []),
        "feature_order_hash": source_manifest.get("feature_order_hash", ""),
        "label_candidates": [row["candidate_id"] for row in candidates],
        "purged_contracts": [row["contract_id"] for row in contracts],
        "shift_controls": [item[0] for item in SHIFT_CONTROLS],
        "purged_summary": list(purged_summary),
        "training_task_rows": len(task_rows),
        "outputs": {
            "purged_membership": rel(PURGED_MEMBERSHIP),
            "candidate_label_frame": rel(CANDIDATE_LABEL_FRAME),
            "label_shift_control_frame": rel(LABEL_SHIFT_CONTROL_FRAME),
            "block_permutation_manifest": rel(BLOCK_PERMUTATION_MANIFEST),
            "training_task_matrix": rel(TRAINING_TASK_MATRIX),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


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
        row("cn_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CM design(설계)와 source data(원천 데이터)를 연결했다."),
        row("cn_gate_parent_points_to_cn", final["cm_next_action"] == RUN_ID, final["cm_next_action"], RUN_ID, "CM next_action(다음 행동)과 CN run(실행)이 맞는다."),
        row("cn_gate_source_rows", final["source_rows"] == 46650, final["source_rows"], "46650", "source row count(원천 행 수)이 CM 설계와 같다."),
        row("cn_gate_feature_order_hash", final["feature_order_hash"] == EXPECTED_FEATURE_ORDER_HASH, final["feature_order_hash"], EXPECTED_FEATURE_ORDER_HASH, "feature order(피처 순서)를 고정했다."),
        row("cn_gate_purged_contract_rows", final["purged_contract_rows"] == 4, final["purged_contract_rows"], "4", "purge contracts(제거 계약) 4개를 모두 사용했다."),
        row("cn_gate_purged_membership_rows", final["purged_membership_rows"] == final["source_rows"] * final["purged_contract_rows"], final["purged_membership_rows"], "source_rows*contracts", "모든 행을 모든 purge contract(제거 계약)에 매핑했다."),
        row("cn_gate_label_frame_rows", final["candidate_label_frame_rows"] == final["source_rows"] * final["label_candidate_rows"], final["candidate_label_frame_rows"], "source_rows*candidates", "모든 candidate label(후보 라벨)을 행 단위로 만들었다."),
        row("cn_gate_shift_control_rows", final["shift_control_rows"] == final["source_rows"] * final["label_candidate_rows"] * len(SHIFT_CONTROLS), final["shift_control_rows"], "source_rows*candidates*shift_controls", "split-local shift controls(분할 내부 이동 대조)를 만들었다."),
        row("cn_gate_block_manifest", final["block_manifest_rows"] > 0, final["block_manifest_rows"], ">0", "block permutation manifest(블록 순열 목록)을 만들었다."),
        row("cn_gate_task_matrix", final["training_task_rows"] == final["label_candidate_rows"] * final["purged_contract_rows"] * len(MODEL_FAMILIES), final["training_task_rows"], "candidates*contracts*model_families", "CO training tasks(CO 학습 작업)를 빠짐없이 만들었다."),
        row("cn_gate_no_training_or_selection", True, "training=not_run;selection=not_run", "no training/selection", "CN은 input materialization(입력 물질화)로만 닫는다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "timestamp(시각)을 정렬하고 source_row_id(원천 행 ID)를 부여했다. 새 broker data(브로커 데이터)는 추가하지 않았다.",
        "sample_scope": "2026-04-13까지의 기존 train/validation/OOS(학습/검증/실외표본) 행만 사용",
        "missing_or_duplicate_check": "generated views(생성 보기)에서는 source_row_id(원천 행 ID)가 후보/계약/대조별로 반복되는 것이 정상이다.",
        "feature_label_boundary": "label shifts(라벨 이동)는 split-local(분할 내부)이며 split boundary(분할 경계)를 넘겨 감지 않는다.",
        "split_boundary": "purge/embargo contracts(제거/격리 계약)가 train-validation(학습-검증)과 validation-OOS(검증-실외표본) 경계 주변 행을 holdout(보류)한다.",
        "leakage_risk": "purge gap(제거 간격)이나 controls(대조)를 winner selection(승자 선택)에 쓰는 경로",
        "data_hash_or_identity": {"source_sha256": final["source_sha256"], "source_rows": final["source_rows"]},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "no_model_training_cn_materialization_only(모델 학습 없음, CN 입력 물질화 전용)",
        "target_and_label": "candidate labels(후보 라벨)와 split-local shifted controls(분할 내부 이동 대조)",
        "split_method": "purged/embargo membership(제거/격리 소속) gap12/gap24/gap48/gap72",
        "selection_metric": "not_applicable_no_selection(해당 없음, 선택 없음)",
        "secondary_metrics": "control clearance(대조 통과), density retention(밀도 유지), ONNX parity(CO 온엑스 동등성)",
        "threshold_policy": "not_touched(건드리지 않음)",
        "overfit_risk": "OOS score(실외표본 점수)가 좋아 보여 purge contract(제거 계약)을 고르는 경로",
        "calibration_risk": "not_applicable_until_CO_training(CO 학습 전 해당 없음)",
        "comparison_baseline": "CK unpurged guarded training(미제거 방어 학습)과 CL negative-control review(부정 대조 검토)",
        "validation_judgment": "materialized_inputs_ready_for_guarded_training(방어 학습용 입력 준비)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "purged split membership(제거 분할 소속), candidate label frame(후보 라벨 프레임), label shift controls(라벨 이동 대조), block permutation manifest(블록 순열 목록), training queue(학습 대기열)",
        "evidence_missing": "CO guarded training(CO 방어 학습), ONNX parity(온엑스 동등성), MT5 runtime probe(MT5 런타임 탐침)",
        "judgment_label": "exploratory(탐색)",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "수리 입력은 만들었지만 아직 학습(training, 학습)이나 운영 판정(operating judgment, 운영 판정)은 아니다.",
    }
    receipt_paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
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
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers(02_runs는 목록/해시로 추적, 보고서와 장부는 추적)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipt_paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return receipt_paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CN Serial Dependence Repair Inputs(연속 의존 수리 입력)

## Conclusion(결론)

run337CN(337CN 실행)은 CM design(CM 설계)을 실제 repair input(수리 입력)으로 물질화했다. 산출물은 purged/embargo split membership(제거/격리 분할 소속), candidate label frame(후보 라벨 프레임), split-local shifted controls(분할 내부 이동 대조), block permutation manifest(블록 순열 목록), CO training task matrix(CO 학습 작업 행렬)이다.

Effect(효과): 다음 run337CO(337CO 실행)는 같은 후보를 purge/embargo(제거/격리)와 non-overlap controls(비중첩 대조)로 다시 압박할 수 있다. CN은 selection(선택), threshold tuning(임계값 조정), MT5 probe(MT5 탐침)를 하지 않았다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- source_rows(원천 행): `{final["source_rows"]}`
- label_candidate_rows(라벨 후보 수): `{final["label_candidate_rows"]}`
- purged_contract_rows(제거 계약 수): `{final["purged_contract_rows"]}`
- purged_membership_rows(제거 소속 행): `{final["purged_membership_rows"]}`
- candidate_label_frame_rows(후보 라벨 프레임 행): `{final["candidate_label_frame_rows"]}`
- shift_control_rows(이동 대조 행): `{final["shift_control_rows"]}`
- block_manifest_rows(블록 목록 행): `{final["block_manifest_rows"]}`
- training_task_rows(학습 작업 행): `{final["training_task_rows"]}`
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
    text = f"""# Decision(결정): Stage337 run337CN

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): purged/embargo split(제거/격리 분할)과 split-local shift controls(분할 내부 이동 대조)를 물질화해 CO guarded training(CO 방어 학습)을 열었다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(REPAIR_INPUT_MANIFEST)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs() -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337CN focus complete: serial-dependence repair inputs(연속 의존 수리 입력)를 `{STATUS}`로 닫았다. "
        "Effect(효과): run337CO(337CO 실행)에서 purged/embargo guarded training(제거/격리 방어 학습)을 실행한다."
    )
    if "Stage337 run337CN focus complete" in workspace_text:
        workspace_text = re.sub(
            r"current_focus:\n- >-\n  Stage337 run337CN focus complete:.*?(?=\n- >-\n  Stage337 run337CM|\n[A-Za-z0-9_]+:)",
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
## Stage337 run337CN(337CN 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): purged/embargo split membership(제거/격리 분할 소속), label shift controls(라벨 이동 대조), CO training matrix(CO 학습 행렬)를 만들었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current_text = re.sub(
        r"\n## Stage337 run337CN\(337CN 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CM|\Z)",
        "\n",
        current_text,
        count=1,
        flags=re.DOTALL,
    )
    marker = "## Stage337 run337CM(337CM"
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
- actual_mt5_execution(실제 MT5 실행): `not_run_cn_input_materialization_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 purged/embargo guarded training(제거/격리 방어 학습)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CN(337CN 실행)" not in line)
    stage_entry = (
        f"- {TODAY}: run337CN(337CN 실행) materialized serial-dependence repair inputs(연속 의존 수리 입력). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(
        line for line in changelog_text.splitlines() if "Stage337 run337CN materialized serial-dependence repair inputs" not in line
    )
    changelog_entry = (
        f"- {TODAY}: Stage337 run337CN materialized serial-dependence repair inputs(연속 의존 수리 입력) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "serial_dependence_label_boundary_repair_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": (
            f"purged_membership_rows={final['purged_membership_rows']};"
            f"shift_control_rows={final['shift_control_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed."
        ),
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_input_materialization",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "input_materialization_no_training",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"training_task_rows={final['training_task_rows']};shift_control_rows={final['shift_control_rows']}",
        "guardrail_kpi": "split_local_shift_controls;purged_splits;no_training;no_selection",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "CM repair design materialized into input artifacts",
        "kpi_scope": "input_materialization_no_training",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_inputs",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "question": "can serial-dependence repair inputs be materialized without leakage or selection",
        "metric_scope": "purged_membership_label_shift_controls_training_queue",
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
    frame = read_source_frame()
    cm_final = read_json(CM_FINAL)
    candidates = read_csv(LABEL_CANDIDATE_MATRIX)
    contracts = read_csv(CM_PURGED_CONTRACT)
    source_manifest = read_json(CANDIDATE_INPUT_MANIFEST)

    purged_membership, purged_summary = build_purged_membership(frame, contracts)
    candidate_label_frame = build_candidate_label_frame(frame, candidates)
    shift_control_frame = build_shift_control_frame(candidate_label_frame)
    block_manifest = build_block_manifest(frame)
    task_rows = build_training_tasks(candidates, contracts)
    queue_rows = build_co_queue()
    manifest = build_manifest(frame, candidates, contracts, purged_summary, task_rows)

    artifacts: list[Path] = [
        write_parquet(PURGED_MEMBERSHIP, purged_membership),
        write_csv(PURGED_SUMMARY, PURGED_SUMMARY_COLUMNS, purged_summary),
        write_parquet(CANDIDATE_LABEL_FRAME, candidate_label_frame),
        write_parquet(LABEL_SHIFT_CONTROL_FRAME, shift_control_frame),
        write_csv(BLOCK_PERMUTATION_MANIFEST, BLOCK_COLUMNS, block_manifest),
        write_csv(TRAINING_TASK_MATRIX, TASK_COLUMNS, task_rows),
        write_json(REPAIR_INPUT_MANIFEST, manifest),
        write_csv(CO_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]

    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "cm_next_action": cm_final.get("next_action", ""),
        "source_rows": int(len(frame)),
        "source_sha256": sha256_file(SOURCE_MODEL_INPUT),
        "feature_order_hash": source_manifest.get("feature_order_hash", ""),
        "label_candidate_rows": len(candidates),
        "purged_contract_rows": len(contracts),
        "purged_membership_rows": int(len(purged_membership)),
        "candidate_label_frame_rows": int(len(candidate_label_frame)),
        "shift_control_rows": int(len(shift_control_frame)),
        "block_manifest_rows": len(block_manifest),
        "training_task_rows": len(task_rows),
        "queue_rows": len(queue_rows),
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
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
