from __future__ import annotations

import csv
import hashlib
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

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337 import design_validation_density_trade_count_repair as eb  # noqa: E402
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
STAGE_ID = eb.STAGE_ID
RUN_NUMBER = "run337EC"
RUN_ID = "run337EC_materialize_validation_density_trade_count_repair_inputs_without_db_v1"
PARENT_RUN_ID = eb.RUN_ID
NEXT_RUN_ID = "run337ED_review_validation_density_trade_count_repair_inputs_without_db_v1"
STATUS = "completed_stage337EC_validation_density_trade_count_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "train_only_validation_density_trade_count_repair_inputs_materialized_review_required"
DECISION = "stage337EC_open_run337ED_review_validation_density_trade_count_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EC_validation_density_trade_count_repair_input_materialization_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = eb.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = eb.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EC_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EC_repair_inputs.md"
SELECTED_STATUS = eb.SELECTED_STATUS
STAGE_BRIEF = eb.STAGE_BRIEF
WORKSPACE_STATE = eb.WORKSPACE_STATE
CURRENT_STATE = eb.CURRENT_STATE
CHANGELOG = eb.CHANGELOG
RUN_REGISTRY = eb.RUN_REGISTRY
ALPHA_LEDGER = eb.ALPHA_LEDGER
ARTIFACT_REGISTRY = eb.ARTIFACT_REGISTRY
STAGE_LEDGER = eb.STAGE_LEDGER

EB_FINAL = eb.FINAL_DECISION
EB_GATES = eb.REQUIRED_GATE_AUDIT
EB_QUEUE = eb.EC_QUEUE
REPAIR_DESIGN = eb.REPAIR_DESIGN
OBJECTIVE_CONTRACTS = eb.OBJECTIVE_CONTRACTS
MODEL_VARIANT_CONTRACTS = eb.MODEL_VARIANT_CONTRACTS
GUARDRAIL_CONTRACTS = eb.GUARDRAIL_CONTRACTS
OOS_QUARANTINE = eb.OOS_QUARANTINE
ARTIFACT_PRESERVATION = eb.ARTIFACT_PRESERVATION
SOURCE_MODEL_INPUT = dz.SOURCE_MODEL_INPUT
FEATURE_SET_MATRIX = dz.FEATURE_SET_MATRIX
OBJECTIVE_FRAME = dz.OBJECTIVE_FRAME
EA_CANDIDATE_REVIEW = eb.CANDIDATE_REVIEW
EA_CONTROL_DENSITY_REVIEW = eb.CONTROL_DENSITY_REVIEW
DZ_DENSITY_AUDIT = dz.DENSITY_GUARD_AUDIT

TRAIN_ONLY_REPAIR_FRAME = RUN_DIR / "train_only_validation_density_trade_count_frame.parquet"
OBJECTIVE_CONTRACT_AUDIT = RUN_DIR / "objective_contract_audit.csv"
EC_TRAINING_TASK_MATRIX = RUN_DIR / "ec_training_task_matrix.csv"
FEATURE_INPUT_COMPATIBILITY = RUN_DIR / "feature_input_compatibility.csv"
CONTROL_DENSITY_WFO_GUARD_MATRIX = RUN_DIR / "control_density_wfo_guard_matrix.csv"
NO_RELEASE_FIREWALL_CARRY = RUN_DIR / "no_release_firewall_carry.csv"
REPAIR_WEIGHT_SUMMARY = RUN_DIR / "repair_weight_summary.csv"
ED_QUEUE = RUN_DIR / "run337ED_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EB_FINAL,
    EB_GATES,
    EB_QUEUE,
    REPAIR_DESIGN,
    OBJECTIVE_CONTRACTS,
    MODEL_VARIANT_CONTRACTS,
    GUARDRAIL_CONTRACTS,
    OOS_QUARANTINE,
    ARTIFACT_PRESERVATION,
    SOURCE_MODEL_INPUT,
    FEATURE_SET_MATRIX,
    OBJECTIVE_FRAME,
    EA_CANDIDATE_REVIEW,
    EA_CONTROL_DENSITY_REVIEW,
    DZ_DENSITY_AUDIT,
)
OUTPUT_FILES = (
    TRAIN_ONLY_REPAIR_FRAME,
    OBJECTIVE_CONTRACT_AUDIT,
    EC_TRAINING_TASK_MATRIX,
    FEATURE_INPUT_COMPATIBILITY,
    CONTROL_DENSITY_WFO_GUARD_MATRIX,
    NO_RELEASE_FIREWALL_CARRY,
    REPAIR_WEIGHT_SUMMARY,
    ED_QUEUE,
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

AUDIT_COLUMNS = (
    "contract_id",
    "contract_family",
    "materialized_rows",
    "weighted_rows",
    "weight_column",
    "leakage_guard",
    "materialized_status",
    "effect",
    "claim_boundary",
)
TASK_COLUMNS = (
    "task_id",
    "target_id",
    "cost_policy_id",
    "feature_set_id",
    "model_variant_id",
    "objective_contract_id",
    "feature_count",
    "feature_order_hash",
    "onnx_export_feasibility",
    "training_eligibility_status",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
FEATURE_COLUMNS = (
    "feature_set_id",
    "feature_count",
    "missing_count",
    "missing_features",
    "nonfinite_rows",
    "feature_order_hash",
    "compatibility_status",
    "claim_boundary",
)
GUARD_COLUMNS = (
    "guard_id",
    "guard_type",
    "source",
    "source_rows",
    "blocking_rows",
    "review_rule",
    "materialized_status",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "blocked_action_or_claim",
    "blocked_reason",
    "carry_status",
    "effect",
    "claim_boundary",
)
WEIGHT_COLUMNS = (
    "cost_policy_id",
    "train_rows",
    "low_margin_weighted_rows",
    "density_tempered_rows",
    "payoff_tail_weighted_rows",
    "combined_weight_min",
    "combined_weight_mean",
    "combined_weight_max",
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


NON_FEATURE_COLUMNS = {
    "timestamp",
    "split",
    "future_log_return_12",
    "future_return_12",
    "cost_return",
    "label",
    "target",
    "source_row_id",
}


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


def feature_order_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(str(item) for item in features).encode("utf-8")).hexdigest()


def parse_json_list(value: str) -> list[str]:
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        return []
    return [str(item) for item in payload]


def read_source_frame() -> pd.DataFrame:
    source = pd.read_parquet(io_path(SOURCE_MODEL_INPUT)).copy()
    source["timestamp"] = pd.to_datetime(source["timestamp"], utc=True)
    source = source.sort_values("timestamp").reset_index(drop=True)
    source["source_row_id"] = np.arange(len(source), dtype=np.int64)
    return source


def read_feature_sets(source: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    feature_sets: list[dict[str, Any]] = []
    compat_rows: list[dict[str, Any]] = []
    for row in read_csv(FEATURE_SET_MATRIX):
        features = parse_json_list(str(row.get("included_features_json", "[]")))
        missing = [feature for feature in features if feature not in source.columns]
        nonfinite_rows = 0
        if not missing and features:
            nonfinite_rows = int(source.loc[:, features].replace([np.inf, -np.inf], np.nan).isna().any(axis=1).sum())
        order_hash = feature_order_hash(features)
        status = "compatible" if not missing and nonfinite_rows == 0 and features else "blocked_feature_input"
        feature_sets.append(
            {
                "feature_set_id": row.get("feature_set_id", ""),
                "features": features,
                "feature_count": len(features),
                "feature_order_hash": order_hash,
                "compatibility_status": status,
            }
        )
        compat_rows.append(
            {
                "feature_set_id": row.get("feature_set_id", ""),
                "feature_count": len(features),
                "missing_count": len(missing),
                "missing_features": json.dumps(missing, ensure_ascii=False),
                "nonfinite_rows": nonfinite_rows,
                "feature_order_hash": order_hash,
                "compatibility_status": status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return feature_sets, compat_rows


def normalize(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce").fillna(0.0)
    scale = float(numeric.quantile(0.95)) if len(numeric) else 0.0
    if scale <= 0:
        return numeric * 0.0
    return (numeric / scale).clip(lower=0.0, upper=1.0)


def objective_aggregate() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(OBJECTIVE_FRAME)).copy()
    splits = sorted(frame["split"].astype(str).unique().tolist())
    if splits != ["train"]:
        raise ValueError(f"OBJECTIVE_FRAME must be train-only, got {splits}")
    group = (
        frame.groupby(["cost_policy_id", "source_row_id"], sort=True)
        .agg(
            low_margin_rate=("low_margin_trade_tag", "mean"),
            direction_residual_rate=("direction_residual_tag", "mean"),
            underwater_rate=("underwater_tag", "mean"),
            drawdown_pressure_mean=("drawdown_pressure_value", "mean"),
            abstention_rate=("abstention_candidate_tag", "mean"),
            payoff_tail_proxy=("abs_pnl_after_cost", "mean"),
        )
        .reset_index()
    )
    group["drawdown_pressure_norm"] = 0.0
    group["payoff_tail_norm"] = 0.0
    for cost_policy, part in group.groupby("cost_policy_id", sort=False):
        group.loc[part.index, "drawdown_pressure_norm"] = normalize(part["drawdown_pressure_mean"]).to_numpy()
        group.loc[part.index, "payoff_tail_norm"] = normalize(part["payoff_tail_proxy"]).to_numpy()
    return group


def materialize_repair_frame(source: pd.DataFrame, aggregate: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    train_source = source.loc[source["split"].astype(str).eq("train")].copy()
    cost_policies = sorted(aggregate["cost_policy_id"].astype(str).unique().tolist())
    frames: list[pd.DataFrame] = []
    summary_rows: list[dict[str, Any]] = []
    for cost_policy in cost_policies:
        cost_agg = aggregate.loc[aggregate["cost_policy_id"].astype(str).eq(cost_policy)].copy()
        merged = train_source.merge(cost_agg, on="source_row_id", how="left")
        merged["cost_policy_id"] = cost_policy
        for column in (
            "low_margin_rate",
            "direction_residual_rate",
            "underwater_rate",
            "drawdown_pressure_mean",
            "abstention_rate",
            "payoff_tail_proxy",
            "drawdown_pressure_norm",
            "payoff_tail_norm",
        ):
            merged[column] = pd.to_numeric(merged[column], errors="coerce").fillna(0.0)
        merged["near_margin_trade_support_weight"] = (1.0 + 1.25 * merged["low_margin_rate"] + 0.25 * merged["direction_residual_rate"]).clip(0.5, 3.0)
        merged["density_tempered_weight"] = (1.0 + 0.45 * merged["underwater_rate"] + 0.35 * merged["abstention_rate"]).clip(0.5, 2.25)
        merged["payoff_tail_offense_weight"] = (1.0 + 0.80 * merged["payoff_tail_norm"]).clip(0.5, 2.50)
        merged["combined_sample_weight"] = (
            merged["near_margin_trade_support_weight"]
            * merged["density_tempered_weight"]
            * merged["payoff_tail_offense_weight"]
        ).clip(0.25, 4.0)
        merged["allowed_split_scope"] = "train_only"
        merged["leakage_guard"] = "validation_oos_excluded"
        frames.append(merged)
        summary_rows.append(
            {
                "cost_policy_id": cost_policy,
                "train_rows": int(len(merged)),
                "low_margin_weighted_rows": int((merged["low_margin_rate"] > 0).sum()),
                "density_tempered_rows": int(((merged["underwater_rate"] > 0) | (merged["abstention_rate"] > 0)).sum()),
                "payoff_tail_weighted_rows": int((merged["payoff_tail_norm"] > 0).sum()),
                "combined_weight_min": float(merged["combined_sample_weight"].min()) if len(merged) else 0.0,
                "combined_weight_mean": float(merged["combined_sample_weight"].mean()) if len(merged) else 0.0,
                "combined_weight_max": float(merged["combined_sample_weight"].max()) if len(merged) else 0.0,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    repair_frame = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    io_path(TRAIN_ONLY_REPAIR_FRAME).parent.mkdir(parents=True, exist_ok=True)
    repair_frame.to_parquet(io_path(TRAIN_ONLY_REPAIR_FRAME), index=False)
    return repair_frame, summary_rows


def build_objective_audit(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    weight_columns = {
        "train_only_near_margin_trade_support": "near_margin_trade_support_weight",
        "train_only_density_tempered_class_prior": "density_tempered_weight",
        "train_only_payoff_tail_offense": "payoff_tail_offense_weight",
        "control_gate_carry_forward": "combined_sample_weight",
    }
    for contract in read_csv(OBJECTIVE_CONTRACTS):
        contract_id = str(contract.get("contract_id", ""))
        weight_col = weight_columns.get(contract_id, "combined_sample_weight")
        weighted_rows = int((pd.to_numeric(frame[weight_col], errors="coerce").fillna(1.0) != 1.0).sum()) if len(frame) and weight_col in frame else 0
        rows.append(
            {
                "contract_id": contract_id,
                "contract_family": contract.get("contract_family", ""),
                "materialized_rows": int(len(frame)),
                "weighted_rows": weighted_rows,
                "weight_column": weight_col,
                "leakage_guard": "split=train_only; validation/OOS excluded(학습 분할만, 검증/OOS 제외)",
                "materialized_status": "materialized_no_training",
                "effect": "계약을 학습 전용 가중치 열로 물질화했다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_task_matrix(feature_sets: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    objectives = [row for row in read_csv(OBJECTIVE_CONTRACTS) if str(row.get("contract_id", "")).startswith("train_only")]
    variants = read_csv(MODEL_VARIANT_CONTRACTS)
    cost_policies = sorted(pd.read_parquet(io_path(OBJECTIVE_FRAME), columns=["cost_policy_id"])["cost_policy_id"].astype(str).unique().tolist())
    rows: list[dict[str, Any]] = []
    index = 1
    for cost_policy in cost_policies:
        for feature_set in feature_sets:
            if feature_set.get("compatibility_status") != "compatible":
                continue
            for variant in variants:
                variant_id = str(variant.get("variant_id", ""))
                onnx_feas = "supported_review_required" if "extratrees" in variant_id else "unsupported_until_review"
                for objective in objectives:
                    objective_id = str(objective.get("contract_id", ""))
                    rows.append(
                        {
                            "task_id": f"ec{index:03d}",
                            "target_id": "costed_action_label",
                            "cost_policy_id": cost_policy,
                            "feature_set_id": feature_set.get("feature_set_id", ""),
                            "model_variant_id": variant_id,
                            "objective_contract_id": objective_id,
                            "feature_count": feature_set.get("feature_count", 0),
                            "feature_order_hash": feature_set.get("feature_order_hash", ""),
                            "onnx_export_feasibility": onnx_feas,
                            "training_eligibility_status": "review_required_no_training",
                            "forbidden_action": "no threshold tuning, no selection, no MT5(임계값 조정/선택/MT5 금지)",
                            "effect": "ED review(ED 검토) 전 학습 범위를 사전 선언한다.",
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )
                    index += 1
    return rows


def build_guard_matrix() -> list[dict[str, Any]]:
    guardrails = read_csv(GUARDRAIL_CONTRACTS)
    ea_review = read_csv(EA_CONTROL_DENSITY_REVIEW)
    dz_density = read_csv(DZ_DENSITY_AUDIT)
    candidates = read_csv(EA_CANDIDATE_REVIEW)
    rows: list[dict[str, Any]] = []
    for guard in guardrails:
        guard_id = str(guard.get("guardrail_id", ""))
        source = "guardrail_contract"
        source_rows = 1
        blocking_rows = 0
        if guard_id == "density_transfer_guard":
            source = rel(DZ_DENSITY_AUDIT)
            source_rows = len(dz_density)
            blocking_rows = sum(1 for row in dz_density if row.get("split") == "validation" and row.get("density_pressure_flag") == "true")
        elif guard_id == "control_gate_hard_carry":
            source = rel(EA_CONTROL_DENSITY_REVIEW)
            source_rows = len(ea_review)
            blocking_rows = sum(int(float(row.get("blocking_rows") or 0)) for row in ea_review if "control" in row.get("review_id", ""))
        elif guard_id == "validation_pf_trade_floor_joint_gate":
            source = rel(EA_CANDIDATE_REVIEW)
            source_rows = len(candidates)
            blocking_rows = sum(
                1
                for row in candidates
                if float(row.get("validation_pf") or 0) < 1.05 or int(float(row.get("validation_trade_count") or 0)) < 500
            )
        rows.append(
            {
                "guard_id": guard_id,
                "guard_type": guard.get("guard_type", ""),
                "source": source,
                "source_rows": source_rows,
                "blocking_rows": blocking_rows,
                "review_rule": guard.get("review_rule", ""),
                "materialized_status": "carried_forward_active",
                "effect": guard.get("effect", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_firewall_carry() -> list[dict[str, str]]:
    rows = [
        {
            "firewall_id": "no_candidate_selection",
            "blocked_action_or_claim": "candidate selection(후보 선택)",
            "blocked_reason": "EC is input materialization only(EC는 입력 물질화 전용)",
            "carry_status": "active",
            "effect": "좋은 입력이나 OOS 포켓이 선택 주장으로 번지는 것을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_threshold_tuning",
            "blocked_action_or_claim": "threshold tuning(임계값 조정)",
            "blocked_reason": "repair must remain predeclared(수리는 사전 선언 상태여야 함)",
            "carry_status": "active",
            "effect": "과적합 수리를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_mt5_or_forward_claim",
            "blocked_action_or_claim": "MT5/Forward/live readiness(MT5/전진/라이브 준비)",
            "blocked_reason": "no model was trained or exported(학습/내보내기 없음)",
            "carry_status": "active",
            "effect": "입력 물질화와 운영 주장을 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for row in read_csv(OOS_QUARANTINE):
        rows.append(
            {
                "firewall_id": str(row.get("quarantine_id", "")),
                "blocked_action_or_claim": row.get("forbidden_use", ""),
                "blocked_reason": row.get("quarantine_rule", ""),
                "carry_status": "active_oos_quarantine",
                "effect": "얇은 OOS 포켓을 선택기에서 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_ed_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337ED_review_train_only_repair_frame",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review train-only repair frame(학습 전용 수리 프레임 검토).",
            "required_inputs": f"{rel(TRAIN_ONLY_REPAIR_FRAME)};{rel(OBJECTIVE_CONTRACT_AUDIT)}",
            "required_outputs": "train_only_repair_frame_review.csv",
            "blocked_if_missing": "repair frame or objective audit(수리 프레임 또는 목표 감사).",
            "forbidden_action": "no model training from unreviewed inputs(검토 전 학습 금지).",
            "effect": "가중치가 검증/OOS를 먹지 않았는지 먼저 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337ED_review_task_matrix",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review EC task matrix(EC 작업 행렬 검토).",
            "required_inputs": f"{rel(EC_TRAINING_TASK_MATRIX)};{rel(FEATURE_INPUT_COMPATIBILITY)}",
            "required_outputs": "ec_task_matrix_review.csv",
            "blocked_if_missing": "task matrix or feature compatibility(작업 행렬 또는 피처 호환성).",
            "forbidden_action": "no result-driven parameter expansion(결과 기반 파라미터 확장 금지).",
            "effect": "다음 학습 후보 범위를 닫힌 표로 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337ED_review_guards_and_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "review guard matrix and firewall(가드 행렬과 방화벽 검토).",
            "required_inputs": f"{rel(CONTROL_DENSITY_WFO_GUARD_MATRIX)};{rel(NO_RELEASE_FIREWALL_CARRY)}",
            "required_outputs": "guard_firewall_review.csv",
            "blocked_if_missing": "guard matrix or firewall(가드 행렬 또는 방화벽).",
            "forbidden_action": "no release, no MT5, no Forward/Goal(해제/MT5/전진/목표 금지).",
            "effect": "입력이 좋아 보여도 운영 주장으로 새지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    no_forbidden_claim = (
        final["model_training"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["mt5_runtime_probe"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "필수 EB/DZ 입력이 있어야 물질화 근거가 닫힌다."),
        ("parent_eb_gates_passed", final["eb_failed_gate_rows"] == 0, str(final["eb_failed_gate_rows"]), "0", "부모 EB 설계 게이트가 통과해야 한다."),
        ("parent_next_action_matches", final["eb_next_action"] == RUN_ID, str(final["eb_next_action"]), RUN_ID, "라우팅이 EC로 정확히 이어졌는지 본다."),
        ("repair_frame_train_only", final["repair_frame_split_values"] == ["train"], json.dumps(final["repair_frame_split_values"]), "[train]", "수리 프레임은 학습 분할만 포함한다."),
        ("repair_frame_rows_positive", final["repair_frame_rows"] > 10000, str(final["repair_frame_rows"]), ">10000", "충분한 학습 입력 행이 생겼는지 본다."),
        ("objective_audit_rows", final["objective_audit_rows"] >= 4, str(final["objective_audit_rows"]), ">=4", "목표 계약이 실제 열로 연결됐는지 본다."),
        ("task_matrix_rows", final["task_matrix_rows"] >= 72, str(final["task_matrix_rows"]), ">=72", "다음 학습 범위가 충분히 물질화됐는지 본다."),
        ("feature_compatibility_clear", final["feature_block_rows"] == 0, str(final["feature_block_rows"]), "0", "피처 누락/비정상 행을 막는다."),
        ("guard_matrix_rows", final["guard_matrix_rows"] >= 6, str(final["guard_matrix_rows"]), ">=6", "가드레일 이월이 충분한지 본다."),
        ("firewall_rows", final["firewall_rows"] >= 5, str(final["firewall_rows"]), ">=5", "해제 금지 방화벽을 유지한다."),
        ("ed_queue_rows", final["ed_queue_rows"] == 3, str(final["ed_queue_rows"]), "3", "ED 검토 큐가 열렸는지 본다."),
        ("no_forbidden_claim", no_forbidden_claim, str(no_forbidden_claim).lower(), "true", "EC는 입력 물질화 전용이며 운영/목표 주장을 하지 않는다."),
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
    data = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "sample_scope": f"repair_rows={final['repair_frame_rows']};split={final['repair_frame_split_values']};cost_policies={final['cost_policy_rows']}",
        "feature_label_boundary": "repair weights are train-only and validation/OOS excluded(수리 가중치는 학습 전용이고 검증/OOS 제외).",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']};feature_block_rows={final['feature_block_rows']}",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "integrity_judgment": "usable_for_ED_review_no_training(ED 검토 전용, 학습 없음).",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_training": "not_run(미실행)",
        "task_matrix_rows": final["task_matrix_rows"],
        "onnx_feasibility": "ExtraTrees supported review required; HistGradient blocked until review(ExtraTrees 검토 필요, HistGradient는 검토 전 차단).",
        "threshold_policy": "fixed_no_tuning(고정, 조정 없음)",
        "selection_metric": "none(없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "observed_parent_blockers": final["release_blockers"],
        "repair_weight_summary_rows": final["repair_weight_summary_rows"],
        "guard_matrix_rows": final["guard_matrix_rows"],
        "attribution": "trade-count lift, density tempering, payoff-tail support materialized as train-only weights(거래수 증가/밀도 완화/보상 꼬리 지지를 학습 전용 가중치로 물질화).",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": JUDGMENT,
        "evidence_available": "repair frame, objective audit, task matrix, guard matrix, firewall(수리 프레임/목표 감사/작업 행렬/가드 행렬/방화벽).",
        "evidence_missing": "ED review, model training, ONNX, MT5, forward(ED 검토/모델 학습/ONNX/MT5/전진).",
        "next_condition": NEXT_RUN_ID,
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_with_boundary(경계 안에서 연결됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EC Repair Inputs(337EC 수리 입력)

## Conclusion(결론)

run337EC(337EC 실행)는 EB repair design(EB 수리 설계)을 실제 train-only repair frame(학습 전용 수리 프레임), EC task matrix(EC 작업 행렬), guard matrix(가드 행렬), no-release firewall(해제 금지 방화벽)로 물질화했다.

Action(행동): 모델 학습(model training, 모델 학습), threshold tuning(임계값 조정), candidate selection(후보 선택), MT5 probe(MT5 탐침)는 실행하지 않았다.

Effect(효과): 다음 run337ED(337ED 실행)에서 입력 안전성부터 검토할 수 있다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- repair_frame_rows(수리 프레임 행): `{final["repair_frame_rows"]}`
- repair_frame_split_values(수리 프레임 분할): `{final["repair_frame_split_values"]}`
- objective_audit_rows(목표 감사 행): `{final["objective_audit_rows"]}`
- task_matrix_rows(작업 행렬 행): `{final["task_matrix_rows"]}`
- feature_block_rows(피처 차단 행): `{final["feature_block_rows"]}`
- guard_matrix_rows(가드 행렬 행): `{final["guard_matrix_rows"]}`
- firewall_rows(방화벽 행): `{final["firewall_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EC

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): EB 계약을 ED 검토 가능한 학습 전용 입력으로 물질화했다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(OBJECTIVE_CONTRACT_AUDIT)}`, `{rel(EC_TRAINING_TASK_MATRIX)}`
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
        f"  Stage337 run337EC focus complete: validation-density/trade-count repair inputs(검증-밀도/거래수 수리 입력)을 `{STATUS}`로 물질화했다. "
        "Effect(효과): 다음 run337ED에서 train-only frame/task/guard/firewall(학습 전용 프레임/작업/가드/방화벽)을 검토한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EC focus complete")
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
## Stage337 run337EC(337EC 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): EB 설계를 학습 전용 수리 입력으로 물질화했다. 학습/선택/MT5/Forward/Goal(학습/선택/MT5/전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337EB("
    if "## Stage337 run337EC(337EC 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_ec_materialization_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): validation-density/trade-count repair input review(검증-밀도/거래수 수리 입력 검토)로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EC(337EC 실행) materialized validation-density/trade-count repair inputs(검증-밀도/거래수 수리 입력). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EC(337EC 실행) materialized validation-density"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337EC materialized validation-density/trade-count repair inputs(검증-밀도/거래수 수리 입력) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EC materialized validation-density"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "validation_density_trade_count_repair_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"repair_rows={final['repair_frame_rows']};tasks={final['task_matrix_rows']};guards={final['guard_matrix_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_performance_attribution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_input_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization_no_training_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "repair_inputs_no_kpi",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"repair_rows={final['repair_frame_rows']};task_rows={final['task_matrix_rows']}",
        "guardrail_kpi": "train_only;no_training;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_performance_attribution",
        "evidence_scope": "EB design contracts materialized",
        "kpi_scope": "repair_frame_task_guard_firewall",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_input_materialization",
        "family": "data_integrity_model_validation_performance_attribution",
        "question": "are validation density trade-count repair inputs materialized without leakage",
        "metric_scope": "repair_frame_task_guard_firewall",
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

    source = read_source_frame()
    feature_sets, feature_rows = read_feature_sets(source)
    aggregate = objective_aggregate()
    repair_frame, weight_rows = materialize_repair_frame(source, aggregate)
    objective_rows = build_objective_audit(repair_frame)
    task_rows = build_task_matrix(feature_sets)
    guard_rows = build_guard_matrix()
    firewall_rows = build_firewall_carry()
    queue_rows = build_ed_queue()
    artifacts: list[Path] = [
        write_csv(OBJECTIVE_CONTRACT_AUDIT, AUDIT_COLUMNS, objective_rows),
        write_csv(EC_TRAINING_TASK_MATRIX, TASK_COLUMNS, task_rows),
        write_csv(FEATURE_INPUT_COMPATIBILITY, FEATURE_COLUMNS, feature_rows),
        write_csv(CONTROL_DENSITY_WFO_GUARD_MATRIX, GUARD_COLUMNS, guard_rows),
        write_csv(NO_RELEASE_FIREWALL_CARRY, FIREWALL_COLUMNS, firewall_rows),
        write_csv(REPAIR_WEIGHT_SUMMARY, WEIGHT_COLUMNS, weight_rows),
        write_csv(ED_QUEUE, QUEUE_COLUMNS, queue_rows),
        TRAIN_ONLY_REPAIR_FRAME,
    ]

    eb_final = read_json(EB_FINAL)
    split_values = sorted(repair_frame["split"].astype(str).unique().tolist()) if len(repair_frame) else []
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "eb_next_action": eb_final.get("next_action", ""),
        "eb_failed_gate_rows": sum(1 for row in read_csv(EB_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "repair_frame_rows": int(len(repair_frame)),
        "repair_frame_split_values": split_values,
        "cost_policy_rows": int(repair_frame["cost_policy_id"].nunique()) if len(repair_frame) else 0,
        "objective_audit_rows": len(objective_rows),
        "task_matrix_rows": len(task_rows),
        "feature_compatibility_rows": len(feature_rows),
        "feature_block_rows": sum(1 for row in feature_rows if row["compatibility_status"] != "compatible"),
        "guard_matrix_rows": len(guard_rows),
        "firewall_rows": len(firewall_rows),
        "repair_weight_summary_rows": len(weight_rows),
        "ed_queue_rows": len(queue_rows),
        "release_blockers": eb_final.get("release_blockers", []),
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
                "repair_frame_rows": final["repair_frame_rows"],
                "task_matrix_rows": final["task_matrix_rows"],
                "guard_matrix_rows": final["guard_matrix_rows"],
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
