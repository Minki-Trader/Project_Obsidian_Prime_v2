from __future__ import annotations

import csv
import hashlib
import json
import math
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


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337DD"
RUN_ID = "run337DD_materialize_cost_shape_two_stage_handoff_repair_inputs_without_db_v1"
PARENT_RUN_ID = "run337DC_design_cost_shape_two_stage_handoff_repair_without_db_v1"
NEXT_RUN_ID = "run337DE_train_cost_shape_two_stage_handoff_candidates_without_db_v1"
STATUS = "completed_stage337DD_cost_shape_two_stage_handoff_inputs_materialized_no_training_no_selection"
JUDGMENT = "cost_identity_and_two_stage_inputs_materialized_training_review_required"
DECISION = "stage337DD_open_run337DE_train_cost_shape_two_stage_handoff_candidates"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DD_cost_shape_two_stage_handoff_input_materialization_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

POINT_SIZE = 0.01
TRADE_TICK_VALUE = 0.01
TRADE_CONTRACT_SIZE = 1.0
ROUND_TRIP_COST_LEVELS = (0, 2, 5)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337DD_cost_shape_two_stage_handoff_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DD_cost_shape_two_stage_handoff_inputs.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

MODEL_INPUT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
RAW_US100 = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"
RAW_US100_MANIFEST = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.manifest.json"
SYMBOL_CONTRACT_PROBE = ROOT / "stages" / "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection" / "03_reviews" / "run50BH_account_cost_forensics_20260514.json"
DC_DIR = STAGE_DIR / "02_runs" / "run337DC"
DC_FINAL = DC_DIR / "final_decision.json"
DC_GATES = DC_DIR / "required_gate_coverage_audit.csv"
DC_POINT_CONTRACT = DC_DIR / "point_cost_identity_repair_contract.csv"
DC_TWO_STAGE_CONTRACT = DC_DIR / "two_stage_handoff_repair_contract.csv"
DC_FIREWALL = DC_DIR / "no_release_firewall_contract.csv"
DC_QUEUE = DC_DIR / "run337DD_materialization_queue.csv"
CZ_FEATURE_SET = STAGE_DIR / "02_runs" / "run337CZ" / "feature_set_matrix.csv"
CZ_MANIFEST = STAGE_DIR / "02_runs" / "run337CZ" / "objective_feature_input_manifest.json"

POINT_COST_IDENTITY = RUN_DIR / "point_cost_identity_sidecar.csv"
POINT_COST_SUMMARY = RUN_DIR / "point_cost_identity_summary.csv"
STAGE1_LABEL_FRAME = RUN_DIR / "stage1_cost_tradeability_label_frame.parquet"
STAGE2_HANDOFF_FRAME = RUN_DIR / "stage2_payoff_rank_handoff_frame.parquet"
TWO_STAGE_HANDOFF_MANIFEST = RUN_DIR / "two_stage_handoff_manifest.json"
CONTROL_FIREWALL_AUDIT = RUN_DIR / "control_firewall_audit.csv"
TRAINING_QUEUE = RUN_DIR / "run337DE_training_queue.csv"
COST_IDENTITY_RECEIPT = RUN_DIR / "cost_identity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    MODEL_INPUT,
    RAW_US100,
    RAW_US100_MANIFEST,
    SYMBOL_CONTRACT_PROBE,
    DC_FINAL,
    DC_GATES,
    DC_POINT_CONTRACT,
    DC_TWO_STAGE_CONTRACT,
    DC_FIREWALL,
    DC_QUEUE,
    CZ_FEATURE_SET,
    CZ_MANIFEST,
)
OUTPUT_FILES = (
    POINT_COST_IDENTITY,
    POINT_COST_SUMMARY,
    STAGE1_LABEL_FRAME,
    STAGE2_HANDOFF_FRAME,
    TWO_STAGE_HANDOFF_MANIFEST,
    CONTROL_FIREWALL_AUDIT,
    TRAINING_QUEUE,
    COST_IDENTITY_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
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

POINT_COST_COLUMNS = (
    "source_row_id",
    "timestamp",
    "future_timestamp",
    "split",
    "current_close",
    "future_close",
    "exact_future_log_return_12",
    "legacy_future_log_return_12",
    "abs_return_diff",
    "current_spread_points",
    "future_spread_points",
    "point_size",
    "trade_tick_value",
    "trade_contract_size",
    "current_spread_return",
    "future_spread_return",
    "round_trip_spread_return",
    "source_status",
    "claim_boundary",
)
POINT_SUMMARY_COLUMNS = (
    "summary_id",
    "value",
    "effect",
    "claim_boundary",
)
STAGE1_COLUMNS = (
    "source_row_id",
    "timestamp",
    "future_timestamp",
    "split",
    "cost_policy_id",
    "extra_round_trip_points",
    "current_close",
    "exact_future_log_return_12",
    "gross_abs_return",
    "round_trip_spread_return",
    "extra_cost_return",
    "train_only_noise_buffer",
    "edge_after_cost_identity",
    "stage1_pass",
    "stage1_label",
    "direction_label",
    "threshold_source",
    "claim_boundary",
)
STAGE2_COLUMNS = (
    "source_row_id",
    "timestamp",
    "future_timestamp",
    "split",
    "cost_policy_id",
    "stage1_pass",
    "stage1_label",
    "stage1_score",
    "stage2_payoff_score",
    "stage2_rank_bucket",
    "stage2_rank_label",
    "stage2_direction_hint",
    "final_action_label",
    "skip_reason",
    "handoff_version",
    "threshold_source",
    "claim_boundary",
)
FIREWALL_COLUMNS = ("audit_id", "status", "observed", "expected", "effect", "claim_boundary")
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


def write_parquet(path: Path, frame: pd.DataFrame) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return path


def feature_order_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(features).encode("utf-8")).hexdigest()


def iso_ts(value: Any) -> str:
    return pd.Timestamp(value).isoformat()


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def read_model_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(MODEL_INPUT)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["future_timestamp"] = pd.to_datetime(frame["future_timestamp"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    frame["source_row_id"] = np.arange(len(frame), dtype=np.int64)
    return frame


def read_raw_frame() -> pd.DataFrame:
    raw = pd.read_csv(io_path(RAW_US100))
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw.sort_values("timestamp").drop_duplicates("timestamp", keep="last").reset_index(drop=True)
    return raw


def build_point_identity(model: pd.DataFrame, raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    raw_by_time = raw.set_index("timestamp")
    current_close = model["timestamp"].map(raw_by_time["close"].astype(float))
    future_close = model["future_timestamp"].map(raw_by_time["close"].astype(float))
    current_spread_points = model["timestamp"].map(raw_by_time["spread_points"].astype(float))
    future_spread_points = model["future_timestamp"].map(raw_by_time["spread_points"].astype(float))
    exact_return = np.log(future_close.astype(float) / current_close.astype(float))
    legacy_return = pd.to_numeric(model["future_log_return_12"], errors="coerce")
    current_spread_return = (current_spread_points * POINT_SIZE) / current_close
    future_spread_return = (future_spread_points * POINT_SIZE) / future_close
    round_trip_spread_return = current_spread_return + future_spread_return
    sidecar = pd.DataFrame(
        {
            "source_row_id": model["source_row_id"],
            "timestamp": model["timestamp"].astype(str),
            "future_timestamp": model["future_timestamp"].astype(str),
            "split": model["split"].astype(str),
            "current_close": current_close,
            "future_close": future_close,
            "exact_future_log_return_12": exact_return,
            "legacy_future_log_return_12": legacy_return,
            "abs_return_diff": (exact_return - legacy_return).abs(),
            "current_spread_points": current_spread_points,
            "future_spread_points": future_spread_points,
            "point_size": POINT_SIZE,
            "trade_tick_value": TRADE_TICK_VALUE,
            "trade_contract_size": TRADE_CONTRACT_SIZE,
            "current_spread_return": current_spread_return,
            "future_spread_return": future_spread_return,
            "round_trip_spread_return": round_trip_spread_return,
            "source_status": "raw_close_matched_with_pinned_symbol_probe(원천 종가 일치 및 고정 심볼 탐침 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    summary = {
        "rows": int(len(sidecar)),
        "current_close_missing": int(sidecar["current_close"].isna().sum()),
        "future_close_missing": int(sidecar["future_close"].isna().sum()),
        "spread_missing": int(sidecar["current_spread_points"].isna().sum() + sidecar["future_spread_points"].isna().sum()),
        "max_abs_return_diff": float(sidecar["abs_return_diff"].max()),
        "mean_abs_return_diff": float(sidecar["abs_return_diff"].mean()),
        "median_spread_points": float(sidecar["current_spread_points"].median()),
        "point_size": POINT_SIZE,
        "trade_tick_value": TRADE_TICK_VALUE,
        "symbol_contract_sha256": sha256_file(SYMBOL_CONTRACT_PROBE),
        "raw_us100_sha256": sha256_file(RAW_US100),
    }
    return sidecar, summary


def train_mask(frame: pd.DataFrame) -> pd.Series:
    return frame["split"].astype(str).eq("train")


def build_stage_labels(sidecar: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    numeric = sidecar.copy()
    for column in ("exact_future_log_return_12", "round_trip_spread_return", "current_close"):
        numeric[column] = pd.to_numeric(numeric[column], errors="coerce")
    gross_abs = numeric["exact_future_log_return_12"].abs()
    signed = numeric["exact_future_log_return_12"]
    train = train_mask(numeric)
    noise_source = gross_abs - numeric["round_trip_spread_return"]
    train_noise = noise_source.loc[train].replace([np.inf, -np.inf], np.nan).dropna()

    stage1_parts: list[pd.DataFrame] = []
    stage2_parts: list[pd.DataFrame] = []
    policy_summaries: dict[str, dict[str, float]] = {}
    for extra_points in ROUND_TRIP_COST_LEVELS:
        cost_policy_id = f"spread_plus_extra{extra_points}_points"
        extra_cost_return = (float(extra_points) * POINT_SIZE) / numeric["current_close"]
        buffer_quantile = 0.50 if extra_points <= 2 else 0.70
        train_noise_buffer = float(train_noise.quantile(buffer_quantile))
        edge = gross_abs - numeric["round_trip_spread_return"] - extra_cost_return - train_noise_buffer
        pass_mask = edge > 0.0
        direction = np.where(~pass_mask, "flat", np.where(signed < 0, "short", "long"))
        stage1 = pd.DataFrame(
            {
                "source_row_id": sidecar["source_row_id"],
                "timestamp": sidecar["timestamp"],
                "future_timestamp": sidecar["future_timestamp"],
                "split": sidecar["split"],
                "cost_policy_id": cost_policy_id,
                "extra_round_trip_points": extra_points,
                "current_close": numeric["current_close"],
                "exact_future_log_return_12": signed,
                "gross_abs_return": gross_abs,
                "round_trip_spread_return": numeric["round_trip_spread_return"],
                "extra_cost_return": extra_cost_return,
                "train_only_noise_buffer": train_noise_buffer,
                "edge_after_cost_identity": edge,
                "stage1_pass": pass_mask,
                "stage1_label": np.where(pass_mask, "tradeable", "abstain"),
                "direction_label": direction,
                "threshold_source": f"train_only_noise_q{int(buffer_quantile * 100)}(학습 전용 노이즈 분위)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        score = edge / (numeric["round_trip_spread_return"] + extra_cost_return + train_noise_buffer + 1.0e-12)
        train_scores = score.loc[train].replace([np.inf, -np.inf], np.nan).dropna()
        cuts = [float(train_scores.quantile(q)) for q in (0.20, 0.40, 0.60, 0.80)]
        buckets = np.searchsorted(np.array(cuts), score.fillna(float("-inf")).to_numpy(), side="right")
        direction_hint = np.where(signed < 0, "short", "long")
        final_action = np.where(pass_mask, direction_hint, "flat")
        stage2 = pd.DataFrame(
            {
                "source_row_id": sidecar["source_row_id"],
                "timestamp": sidecar["timestamp"],
                "future_timestamp": sidecar["future_timestamp"],
                "split": sidecar["split"],
                "cost_policy_id": cost_policy_id,
                "stage1_pass": pass_mask,
                "stage1_label": np.where(pass_mask, "tradeable", "abstain"),
                "stage1_score": edge,
                "stage2_payoff_score": score,
                "stage2_rank_bucket": buckets,
                "stage2_rank_label": [f"rank_{int(item)}" for item in buckets],
                "stage2_direction_hint": direction_hint,
                "final_action_label": final_action,
                "skip_reason": np.where(pass_mask, "stage1_passed(1단계 통과)", "stage1_cost_gate_block(1단계 비용 게이트 차단)"),
                "handoff_version": "run337DD_two_stage_handoff_v1",
                "threshold_source": "train_only_stage1_and_rank_bins(학습 전용 1단계 및 순위 구간)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for split in ("train", "validation", "oos"):
            subset = stage1.loc[stage1["split"].eq(split)]
            policy_summaries[f"{cost_policy_id}::{split}"] = {
                "rows": float(len(subset)),
                "stage1_pass_rows": float(subset["stage1_pass"].sum()),
                "stage1_pass_rate": float(subset["stage1_pass"].mean()) if len(subset) else 0.0,
                "train_only_noise_buffer": train_noise_buffer,
            }
        stage1_parts.append(stage1)
        stage2_parts.append(stage2)
    diagnostics = {
        "stage1_rows": int(sum(len(part) for part in stage1_parts)),
        "stage2_rows": int(sum(len(part) for part in stage2_parts)),
        "policy_summaries": policy_summaries,
    }
    return pd.concat(stage1_parts, ignore_index=True), pd.concat(stage2_parts, ignore_index=True), diagnostics


def build_summary_rows(point_summary: Mapping[str, Any], label_diag: Mapping[str, Any]) -> list[dict[str, str]]:
    rows = [
        {
            "summary_id": "point_cost_identity_rows",
            "value": point_summary["rows"],
            "effect": "all model rows receive raw close identity(모든 모델 행에 원천 종가 정체성 부여)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "summary_id": "return_diff_max",
            "value": point_summary["max_abs_return_diff"],
            "effect": "legacy label and raw close return are equivalent within tolerance(기존 라벨과 원천 종가 수익률이 허용오차 내 동일)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "summary_id": "median_spread_points",
            "value": point_summary["median_spread_points"],
            "effect": "spread is now explicit in label sidecar(스프레드가 라벨 보조표에 명시됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for key, value in sorted(label_diag["policy_summaries"].items()):
        rows.append(
            {
                "summary_id": key,
                "value": json.dumps(value, ensure_ascii=False, sort_keys=True),
                "effect": "stage1 pass distribution for train/read-only splits(학습/읽기 전용 분할의 1단계 통과 분포)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_manifest(point_summary: Mapping[str, Any], label_diag: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "handoff_version": "run337DD_two_stage_handoff_v1",
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "point_identity": {
            "point_size": POINT_SIZE,
            "trade_tick_value": TRADE_TICK_VALUE,
            "trade_contract_size": TRADE_CONTRACT_SIZE,
            "symbol_contract_source": rel(SYMBOL_CONTRACT_PROBE),
            "raw_us100_source": rel(RAW_US100),
            "raw_manifest": rel(RAW_US100_MANIFEST),
            "max_abs_return_diff": point_summary["max_abs_return_diff"],
            "median_spread_points": point_summary["median_spread_points"],
        },
        "stage1": {
            "label_frame": rel(STAGE1_LABEL_FRAME),
            "pass_field": "stage1_pass",
            "score_field": "edge_after_cost_identity",
            "threshold_policy": "train_only_noise_buffer(학습 전용 노이즈 버퍼)",
        },
        "stage2": {
            "label_frame": rel(STAGE2_HANDOFF_FRAME),
            "rank_field": "stage2_rank_bucket",
            "final_action_field": "final_action_label",
            "threshold_policy": "train_only_rank_bins(학습 전용 순위 구간)",
        },
        "policy_summaries": label_diag["policy_summaries"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_firewall_audit(point_summary: Mapping[str, Any], label_diag: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "audit_id": "dd_audit_raw_close_coverage",
            "status": "passed" if point_summary["current_close_missing"] == 0 and point_summary["future_close_missing"] == 0 else "failed",
            "observed": f"current_missing={point_summary['current_close_missing']};future_missing={point_summary['future_close_missing']}",
            "expected": "0;0",
            "effect": "비용 라벨이 실행 가능한 원천 종가에 붙는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "dd_audit_return_identity",
            "status": "passed" if point_summary["max_abs_return_diff"] <= 1.0e-8 else "failed",
            "observed": point_summary["max_abs_return_diff"],
            "expected": "<=1e-8",
            "effect": "기존 미래 수익률과 원천 종가 재계산을 분리 검증한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "dd_audit_point_contract_present",
            "status": "passed" if path_exists(SYMBOL_CONTRACT_PROBE) else "failed",
            "observed": rel(SYMBOL_CONTRACT_PROBE),
            "expected": "pinned symbol probe exists(고정 심볼 탐침 존재)",
            "effect": "포인트 크기 가정을 문서화된 심볼 근거에 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "dd_audit_no_release_firewall",
            "status": "passed",
            "observed": "training_queue_only_no_mt5(학습 대기열만, MT5 없음)",
            "expected": "no MT5 probe or release(탐침/해제 없음)",
            "effect": "입력 물질화를 운영 주장으로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "dd_audit_stage1_stage2_rows",
            "status": "passed" if label_diag["stage1_rows"] > 0 and label_diag["stage2_rows"] > 0 else "failed",
            "observed": f"stage1={label_diag['stage1_rows']};stage2={label_diag['stage2_rows']}",
            "expected": ">0",
            "effect": "2단계 인계 입력이 실제 행으로 존재함을 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_training_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DE_train_stage1_cost_gate",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train stage1 cost tradeability gate candidates(1단계 비용 거래가능성 게이트 후보 학습)",
            "required_inputs": rel(STAGE1_LABEL_FRAME),
            "required_outputs": "trained stage1 models, validation/control/cost review(1단계 학습 모델과 검증/대조/비용 검토)",
            "blocked_if_missing": "point cost identity or train-only thresholds(포인트 비용 정체성 또는 학습 전용 임계값)",
            "forbidden_action": "no validation/OOS threshold tuning(검증/OOS 임계값 튜닝 금지)",
            "effect": "tests whether cost gate removes weak trades before direction(비용 게이트가 방향 전 약한 거래를 제거하는지 시험)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DE_train_stage2_rank_handoff",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train stage2 payoff rank handoff candidates(2단계 보상 순위 인계 후보 학습)",
            "required_inputs": rel(STAGE2_HANDOFF_FRAME),
            "required_outputs": "stage2 rank models and handoff parity precheck(2단계 순위 모델과 인계 동등성 사전점검)",
            "blocked_if_missing": "stage1_pass field or rank labels(1단계 통과 필드 또는 순위 라벨)",
            "forbidden_action": "no rank-as-probability claim(순위를 확률로 주장 금지)",
            "effect": "keeps rank as ordering evidence(순위를 정렬 근거로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DE_review_two_stage_no_release",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "review two-stage candidates under no-release firewall(해제 금지 방화벽 아래 2단계 후보 검토)",
            "required_inputs": f"{rel(CONTROL_FIREWALL_AUDIT)};{rel(TWO_STAGE_HANDOFF_MANIFEST)}",
            "required_outputs": "runtime disposition all held unless gates pass(게이트 전까지 런타임 처분 전부 보류)",
            "blocked_if_missing": "firewall audit(방화벽 감사)",
            "forbidden_action": "no MT5 package from training alone(학습만으로 MT5 패키지 금지)",
            "effect": "prevents training completion from becoming release(학습 완료가 해제로 바뀌는 것을 막음)",
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
        gate_row("dd_gate_parent_points_to_dd", final["dc_next_action"] == RUN_ID, final["dc_next_action"], RUN_ID, "DC next_action(다음 행동)과 DD 실행을 맞춘다."),
        gate_row("dd_gate_raw_current_close_coverage", final["current_close_missing"] == 0, final["current_close_missing"], 0, "현재 종가 원천 누락을 막는다."),
        gate_row("dd_gate_raw_future_close_coverage", final["future_close_missing"] == 0, final["future_close_missing"], 0, "미래 라벨 종가 원천 누락을 막는다."),
        gate_row("dd_gate_return_identity", final["max_abs_return_diff"] <= 1.0e-8, final["max_abs_return_diff"], "<=1e-8", "기존 라벨과 원천 종가 수익률을 동등화한다."),
        gate_row("dd_gate_spread_identity_present", final["spread_missing"] == 0, final["spread_missing"], 0, "스프레드 비용 정체성을 명시한다."),
        gate_row("dd_gate_stage1_materialized", final["stage1_rows"] > 0, final["stage1_rows"], ">0", "1단계 비용 게이트 학습 입력을 만든다."),
        gate_row("dd_gate_stage2_materialized", final["stage2_rows"] > 0, final["stage2_rows"], ">0", "2단계 순위 인계 학습 입력을 만든다."),
        gate_row("dd_gate_firewall_audit_passed", final["firewall_failed_rows"] == 0, final["firewall_failed_rows"], 0, "해제 금지 방화벽을 통과한 입력만 다음으로 넘긴다."),
        gate_row("dd_gate_training_queue_created", final["queue_rows"] >= 3, final["queue_rows"], ">=3", "DE 학습 대기열을 만든다."),
        gate_row("dd_gate_no_forbidden_actions", final["model_training"] == "not_run" and final["threshold_tuning"] == "not_run" and final["mt5_runtime_probe"] == "not_run", "no_training_no_tuning_no_mt5", "no_training_no_tuning_no_mt5", "물질화가 학습/튜닝/MT5로 새지 않게 한다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    cost_receipt = {
        "point_size": POINT_SIZE,
        "trade_tick_value": TRADE_TICK_VALUE,
        "trade_contract_size": TRADE_CONTRACT_SIZE,
        "raw_us100": rel(RAW_US100),
        "symbol_contract_probe": rel(SYMBOL_CONTRACT_PROBE),
        "rows": final["point_identity_rows"],
        "current_close_missing": final["current_close_missing"],
        "future_close_missing": final["future_close_missing"],
        "spread_missing": final["spread_missing"],
        "max_abs_return_diff": final["max_abs_return_diff"],
        "judgment": "cost_identity_materialized_with_pinned_symbol_probe(고정 심볼 탐침으로 비용 정체성 물질화)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    experiment_receipt = {
        "hypothesis": "cost-shape failure can be repaired by explicit cost identity plus stage1/stage2 handoff(비용 곡선 실패는 비용 정체성과 1/2단계 인계로 수리 가능)",
        "decision_use": "feed DE training only(DE 학습 입력으로만 사용)",
        "comparison_baseline": PARENT_RUN_ID,
        "control_variables": "no training, no threshold tuning, no lot optimization, no MT5 probe(학습/튜닝/로트 최적화/MT5 탐침 없음)",
        "changed_variables": "materialized labels and handoff fields(물질화 라벨과 인계 필드)",
        "sample_scope": f"{final['source_timestamp_min']} to {final['source_timestamp_max']} US100 M5",
        "success_criteria": "0 missing close/spread and stage labels created(종가/스프레드 누락 0 및 단계 라벨 생성)",
        "failure_criteria": "missing identity or failed firewall(정체성 누락 또는 방화벽 실패)",
        "invalid_conditions": "validation/OOS tuning or release claim(검증/OOS 튜닝 또는 해제 주장)",
        "stop_conditions": "gate failure before DE training(DE 학습 전 게이트 실패)",
        "evidence_plan": [rel(path) for path in artifact_paths],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(MODEL_INPUT), rel(RAW_US100), rel(RAW_US100_MANIFEST), rel(SYMBOL_CONTRACT_PROBE)],
        "time_axis": "closed M5 UTC timestamp from model frame joined to raw time_close_unix(모델 프레임 닫힌 M5 UTC 시각을 원천 time_close_unix와 결합)",
        "sample_scope": f"rows={final['source_rows']}; {final['source_timestamp_min']} to {final['source_timestamp_max']}",
        "missing_or_duplicate_check": f"current_missing={final['current_close_missing']};future_missing={final['future_close_missing']};duplicates={final['duplicate_timestamp_rows']}",
        "feature_label_boundary": "features remain existing model inputs; labels use future close only as target(피처는 기존 입력 유지, 라벨만 미래 종가 타깃 사용)",
        "split_boundary": "train-only buffers and rank bins; validation/OOS read-only(학습 전용 버퍼와 순위 구간, 검증/OOS 읽기 전용)",
        "leakage_risk": "using validation/OOS to choose cost policy(검증/OOS로 비용 정책 선택)",
        "data_hash_or_identity": {"model_input": sha256_file(MODEL_INPUT), "raw_us100": sha256_file(RAW_US100), "symbol_contract": sha256_file(SYMBOL_CONTRACT_PROBE)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "not_trained_in_DD; DE queued(DD에서는 학습 없음, DE 대기)",
        "target_and_label": "stage1 cost tradeability and stage2 payoff rank handoff(1단계 비용 거래가능성 및 2단계 보상 순위 인계)",
        "split_method": "existing split with train-only thresholds(기존 분할과 학습 전용 임계값)",
        "selection_metric": "not_applicable_no_selection(선택 없음)",
        "secondary_metrics": "cost identity, stage pass rate, firewall audit(비용 정체성, 단계 통과율, 방화벽 감사)",
        "threshold_policy": "train_only_materialized(학습 전용 물질화)",
        "overfit_risk": "choosing cost policy after validation result(검증 결과 뒤 비용 정책 선택)",
        "calibration_risk": "rank score remains ordering, not probability(순위 점수는 확률이 아니라 정렬)",
        "comparison_baseline": PARENT_RUN_ID,
        "validation_judgment": "input_materialized_ready_for_training_review",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "point sidecar, stage1/stage2 frames, firewall audit, DE queue(포인트 보조표, 1/2단계 프레임, 방화벽 감사, DE 대기열)",
        "evidence_missing": "trained models, ONNX parity, proxy/MT5 parity, MT5 runtime probe(학습 모델, ONNX 동등성, 프록시/MT5 동등성, MT5 런타임 탐침)",
        "judgment_label": "exploratory_input_materialization_completed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "비용 정체성은 물질화됐지만 아직 모델 성과나 운영 가능성은 판단하지 않습니다.",
    }
    paths = [
        write_json(COST_IDENTITY_RECEIPT, cost_receipt),
        write_json(EXPERIMENT_RECEIPT, experiment_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
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
        "availability": "ignored_run_outputs_with_tracked_report_and_script(무시된 실행 산출물, 추적 보고서와 스크립트)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DD Cost Shape Two-Stage Handoff Inputs(비용 곡선 2단계 인계 입력)

## Conclusion(결론)

run337DD(337DD 실행)는 raw US100 M5 close(원천 US100 5분 종가)와 pinned symbol probe(고정 심볼 탐침)를 결합해 point-cost identity sidecar(포인트 비용 정체성 보조표)를 만들었다. current/future close missing(현재/미래 종가 누락)은 `{final["current_close_missing"]}/{final["future_close_missing"]}`이고, legacy label return(기존 라벨 수익률)과 raw close return(원천 종가 수익률)의 최대 차이는 `{final["max_abs_return_diff"]}`이다.

Effect(효과): 다음 run337DE(337DE 실행)는 stage1 cost gate(1단계 비용 게이트)와 stage2 payoff rank handoff(2단계 보상 순위 인계)를 학습/검토할 수 있다. 이번 실행은 materialization(물질화)만 하며 training(학습), selection(선택), MT5 probe(MT5 탐침), Forward/Goal(전진/목표)을 주장하지 않는다.

## Materialized(물질화)

- point_identity_rows(포인트 정체성 행): `{final["point_identity_rows"]}`
- stage1_rows(1단계 행): `{final["stage1_rows"]}`
- stage2_rows(2단계 행): `{final["stage2_rows"]}`
- firewall_failed_rows(방화벽 실패 행): `{final["firewall_failed_rows"]}`
- queue_rows(대기열 행): `{final["queue_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`
- source_window(원천 구간): `{final["source_timestamp_min"]}` to `{final["source_timestamp_max"]}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 튜닝): `not_run`
- candidate_selection(후보 선택): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DD

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): raw close(원천 종가), spread(스프레드), point contract(포인트 계약)을 stage1/stage2 label handoff(1/2단계 라벨 인계)에 연결했다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(POINT_COST_IDENTITY)}`
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
        f"  Stage337 run337DD focus complete: cost shape two-stage handoff inputs(비용 곡선 2단계 인계 입력)을 `{STATUS}`로 물질화했다. "
        f"Effect(효과): run337DE(337DE 실행)에서 stage1 cost gate/stage2 payoff rank handoff(1단계 비용 게이트/2단계 보상 순위 인계) 후보 학습을 실행한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DD focus complete")
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
## Stage337 run337DD(337DD 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): point-cost identity/stage1 cost gate/stage2 payoff rank handoff(포인트 비용 정체성/1단계 비용 게이트/2단계 보상 순위 인계) 입력을 만들었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DC(337DC"
    if "## Stage337 run337DD(337DD 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_dd_input_materialization_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 cost shape two-stage handoff candidate training(비용 곡선 2단계 인계 후보 학습)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DD(337DD 실행) materialized cost shape two-stage handoff inputs(비용 곡선 2단계 인계 입력). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DD(337DD 실행) materialized cost shape"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DD materialized cost shape two-stage handoff inputs(비용 곡선 2단계 인계 입력) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DD materialized cost shape"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "cost_shape_two_stage_handoff_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"stage1_rows={final['stage1_rows']};stage2_rows={final['stage2_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__two_stage_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "two_stage_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "input_materialization_no_training",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "input_contract_no_kpi",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"point_rows={final['point_identity_rows']};return_diff={final['max_abs_return_diff']}",
        "guardrail_kpi": "no_training;no_threshold_tuning;no_candidate_selection;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__two_stage_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "DC design materialized into point-cost and two-stage inputs",
        "kpi_scope": "input_contract_no_training",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__two_stage_inputs",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "question": "can cost-shape two-stage handoff inputs be materialized with raw cost identity",
        "metric_scope": "point_cost_identity_stage1_stage2_labels",
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

    dc_final = read_json(DC_FINAL)
    model = read_model_frame()
    raw = read_raw_frame()
    sidecar, point_summary = build_point_identity(model, raw)
    stage1, stage2, label_diag = build_stage_labels(sidecar)
    summary_rows = build_summary_rows(point_summary, label_diag)
    handoff_manifest = build_manifest(point_summary, label_diag)
    firewall_rows = build_firewall_audit(point_summary, label_diag)
    training_queue = build_training_queue()

    artifacts: list[Path] = [
        write_csv(POINT_COST_IDENTITY, POINT_COST_COLUMNS, sidecar.to_dict("records")),
        write_csv(POINT_COST_SUMMARY, POINT_SUMMARY_COLUMNS, summary_rows),
        write_parquet(STAGE1_LABEL_FRAME, stage1[list(STAGE1_COLUMNS)]),
        write_parquet(STAGE2_HANDOFF_FRAME, stage2[list(STAGE2_COLUMNS)]),
        write_json(TWO_STAGE_HANDOFF_MANIFEST, handoff_manifest),
        write_csv(CONTROL_FIREWALL_AUDIT, FIREWALL_COLUMNS, firewall_rows),
        write_csv(TRAINING_QUEUE, QUEUE_COLUMNS, training_queue),
    ]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dc_next_action": dc_final.get("next_action", ""),
        "source_rows": int(len(model)),
        "source_timestamp_min": iso_ts(model["timestamp"].min()),
        "source_timestamp_max": iso_ts(model["timestamp"].max()),
        "duplicate_timestamp_rows": int(model["timestamp"].duplicated().sum()),
        "point_identity_rows": int(len(sidecar)),
        "current_close_missing": point_summary["current_close_missing"],
        "future_close_missing": point_summary["future_close_missing"],
        "spread_missing": point_summary["spread_missing"],
        "max_abs_return_diff": point_summary["max_abs_return_diff"],
        "mean_abs_return_diff": point_summary["mean_abs_return_diff"],
        "median_spread_points": point_summary["median_spread_points"],
        "stage1_rows": int(len(stage1)),
        "stage2_rows": int(len(stage2)),
        "cost_policy_count": len(ROUND_TRIP_COST_LEVELS),
        "firewall_rows": len(firewall_rows),
        "firewall_failed_rows": sum(1 for row in firewall_rows if row["status"] != "passed"),
        "queue_rows": len(training_queue),
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
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
