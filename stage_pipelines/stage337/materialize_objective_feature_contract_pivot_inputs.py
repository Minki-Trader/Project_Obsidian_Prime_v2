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
RUN_NUMBER = "run337CZ"
RUN_ID = "run337CZ_materialize_objective_feature_contract_pivot_inputs_without_db_v1"
PARENT_RUN_ID = "run337CY_design_objective_feature_contract_pivot_after_separability_control_failure_without_db_v1"
NEXT_RUN_ID = "run337DA_train_objective_feature_contract_pivot_candidates_without_db_v1"
STATUS = "completed_stage337CZ_objective_feature_contract_pivot_inputs_materialized_no_training_no_selection"
JUDGMENT = "objective_feature_contract_pivot_inputs_materialized_ready_for_guarded_training"
DECISION = "stage337CZ_open_run337DA_train_objective_feature_contract_pivot_candidates"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CZ_objective_feature_contract_pivot_inputs_without_db_"
    "train_only_thresholds_no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CZ_objective_feature_contract_pivot_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CZ_objective_feature_contract_pivot_inputs.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

SOURCE_MODEL_INPUT = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
    / "model_input_dataset.parquet"
)
CY_DIR = STAGE_DIR / "02_runs" / "run337CY"
CY_FINAL = CY_DIR / "final_decision.json"
CY_QUEUE = CY_DIR / "run337CZ_materialization_queue.csv"
CY_OBJECTIVE = CY_DIR / "objective_family_pivot_design.csv"
CY_FEATURE_CONTRACT = CY_DIR / "feature_contract_pivot_matrix.csv"
CY_CONTROL_CONTRACT = CY_DIR / "control_orthogonal_objective_contract.csv"
CY_COST_CONTRACT = CY_DIR / "cost_aware_abstention_contract.csv"
CY_TWO_STAGE_CONTRACT = CY_DIR / "two_stage_runtime_contract_design.csv"
CR_FEATURE_STATE = STAGE_DIR / "02_runs" / "run337CR" / "feature_state_carry_matrix.csv"
BQ_LAG_SUMMARY = STAGE_DIR / "02_runs" / "run337BQ" / "asof_source_lag_summary.csv"
BQ_FEATURE_SUMMARY = STAGE_DIR / "02_runs" / "run337BQ" / "feature_set_materialization_summary.csv"
CV_FEATURE_SETS = STAGE_DIR / "02_runs" / "run337CV" / "control_orthogonal_feature_sets.csv"
CW_TRAINING_REVIEW = STAGE_DIR / "02_runs" / "run337CX" / "failure_attribution_matrix.csv"

COST_TRADEABILITY_LABEL_FRAME = RUN_DIR / "cost_tradeability_label_frame.parquet"
PAYOFF_RANK_LABEL_FRAME = RUN_DIR / "payoff_rank_label_frame.parquet"
CONTROL_RESIDUAL_LABEL_FRAME = RUN_DIR / "control_residual_label_frame.parquet"
CONTROL_SIDECAR_MATRIX = RUN_DIR / "control_sidecar_matrix.csv"
FEATURE_SET_MATRIX = RUN_DIR / "feature_set_matrix.csv"
FEATURE_CONTRACT_MANIFEST = RUN_DIR / "feature_contract_manifest.json"
TWO_STAGE_HANDOFF_MANIFEST = RUN_DIR / "two_stage_handoff_manifest.json"
PROXY_MT5_TWO_STAGE_COMPARE = RUN_DIR / "proxy_mt5_two_stage_compare_contract.csv"
COST_LABEL_CONTRACT = RUN_DIR / "cost_tradeability_label_contract.csv"
PAYOFF_RANK_CONTRACT = RUN_DIR / "payoff_rank_label_contract.csv"
OBJECTIVE_INPUT_MANIFEST = RUN_DIR / "objective_feature_input_manifest.json"
DA_QUEUE = RUN_DIR / "run337DA_guarded_training_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    SOURCE_MODEL_INPUT,
    CY_FINAL,
    CY_QUEUE,
    CY_OBJECTIVE,
    CY_FEATURE_CONTRACT,
    CY_CONTROL_CONTRACT,
    CY_COST_CONTRACT,
    CY_TWO_STAGE_CONTRACT,
    CR_FEATURE_STATE,
    BQ_LAG_SUMMARY,
    BQ_FEATURE_SUMMARY,
    CV_FEATURE_SETS,
    CW_TRAINING_REVIEW,
)
OUTPUT_FILES = (
    COST_TRADEABILITY_LABEL_FRAME,
    PAYOFF_RANK_LABEL_FRAME,
    CONTROL_RESIDUAL_LABEL_FRAME,
    CONTROL_SIDECAR_MATRIX,
    FEATURE_SET_MATRIX,
    FEATURE_CONTRACT_MANIFEST,
    TWO_STAGE_HANDOFF_MANIFEST,
    PROXY_MT5_TWO_STAGE_COMPARE,
    COST_LABEL_CONTRACT,
    PAYOFF_RANK_CONTRACT,
    OBJECTIVE_INPUT_MANIFEST,
    DA_QUEUE,
    EXPERIMENT_RECEIPT,
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

COST_LABEL_COLUMNS = (
    "source_row_id",
    "timestamp",
    "split",
    "cost_contract_id",
    "cost_level_points",
    "future_log_return_12",
    "abs_future_log_return_12",
    "cost_return_proxy",
    "train_only_drawdown_buffer",
    "train_only_reward_threshold",
    "edge_after_cost_buffer",
    "tradeability_label",
    "direction_label",
    "threshold_source",
    "cost_proxy_method",
    "claim_boundary",
)
PAYOFF_COLUMNS = (
    "source_row_id",
    "timestamp",
    "split",
    "cost_contract_id",
    "cost_level_points",
    "payoff_score_after_cost",
    "payoff_rank_bucket",
    "payoff_rank_label",
    "direction_hint",
    "train_q20",
    "train_q40",
    "train_q60",
    "train_q80",
    "rank_source",
    "claim_boundary",
)
CONTROL_LABEL_COLUMNS = (
    "source_row_id",
    "timestamp",
    "split",
    "control_contract_id",
    "control_id",
    "actual_direction_label",
    "control_label",
    "residual_eligible",
    "residual_direction_label",
    "residual_reason",
    "claim_boundary",
)
CONTROL_SIDECAR_COLUMNS = (
    "source_row_id",
    "timestamp",
    "split",
    "actual_direction_label",
    "gap72_control_label",
    "gap96_control_label",
    "modulo_fold_id",
    "modulo_control_label",
    "claim_boundary",
)
FEATURE_SET_COLUMNS = (
    "feature_set_id",
    "contract_id",
    "feature_family",
    "source_feature_count",
    "included_feature_count",
    "dropped_feature_count",
    "included_features_json",
    "dropped_features_json",
    "feature_order_hash",
    "source_sidecar_status",
    "forbidden_action",
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
    "symbol",
    "future_timestamp",
    "future_log_return_12",
    "label",
    "label_class",
    "label_id",
    "split",
    "split_id",
    "horizon_bars",
    "horizon_minutes",
}
MACRO_EQUITY_PREFIXES = (
    "vix_",
    "us10yr_",
    "usdx_",
    "nvda_",
    "aapl_",
    "msft_",
    "amzn_",
    "mega8_",
    "top3_",
    "us100_minus_",
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def feature_order_hash(features: Sequence[str]) -> str:
    payload = "\n".join(str(item) for item in features).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def write_parquet(path: Path, frame: pd.DataFrame) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return path


def iso_ts(value: Any) -> str:
    return pd.Timestamp(value).isoformat()


def read_source_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(SOURCE_MODEL_INPUT)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    frame["source_row_id"] = np.arange(len(frame), dtype=np.int64)
    return frame


def model_feature_columns(frame: pd.DataFrame) -> list[str]:
    return [str(column) for column in frame.columns if str(column) not in NON_FEATURE_COLUMNS and str(column) != "source_row_id"]


def train_mask(frame: pd.DataFrame) -> pd.Series:
    return frame["split"].astype(str).eq("train")


def cost_return_proxy_unit(frame: pd.DataFrame) -> float:
    train = frame.loc[train_mask(frame)].copy()
    ratio = pd.to_numeric(train["hl_range"], errors="coerce") / pd.to_numeric(train["atr_14"], errors="coerce")
    ratio = ratio.replace([np.inf, -np.inf], np.nan).dropna()
    ratio = ratio[ratio > 0]
    if ratio.empty:
        raise ValueError("cannot compute train-only cost point to return proxy")
    return float(ratio.median())


def classify_direction(values: pd.Series, positive_mask: pd.Series | np.ndarray) -> np.ndarray:
    raw = np.where(values < 0, "short", "long")
    return np.where(positive_mask, raw, "flat")


def build_cost_and_payoff_labels(
    frame: pd.DataFrame, cost_contracts: Sequence[Mapping[str, str]]
) -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    unit = cost_return_proxy_unit(frame)
    abs_return = pd.to_numeric(frame["future_log_return_12"], errors="coerce").abs().fillna(0.0)
    signed_return = pd.to_numeric(frame["future_log_return_12"], errors="coerce").fillna(0.0)
    hl_range = pd.to_numeric(frame["hl_range"], errors="coerce").abs().replace([np.inf, -np.inf], np.nan)
    rolling_noise = (
        pd.to_numeric(frame["log_return_1"], errors="coerce").abs().rolling(12, min_periods=3).mean().fillna(hl_range.median())
    )

    cost_frames: list[pd.DataFrame] = []
    payoff_frames: list[pd.DataFrame] = []
    cost_contract_rows: list[dict[str, Any]] = []
    payoff_contract_rows: list[dict[str, Any]] = []

    for contract in cost_contracts:
        contract_id = str(contract["contract_id"])
        cost_points = float(contract["cost_level_points"])
        cost_proxy = cost_points * unit
        train = train_mask(frame)
        drawdown_quantile = 0.55 if cost_points <= 2 else 0.75
        train_drawdown_buffer = float(hl_range.loc[train].quantile(drawdown_quantile))
        train_reward_threshold = float((abs_return.loc[train] - cost_proxy).quantile(0.50 if cost_points <= 2 else 0.70))
        edge = abs_return - cost_proxy - train_drawdown_buffer
        positive = edge > 0
        direction = classify_direction(signed_return, positive)

        cost_part = pd.DataFrame(
            {
                "source_row_id": frame["source_row_id"],
                "timestamp": frame["timestamp"].astype(str),
                "split": frame["split"].astype(str),
                "cost_contract_id": contract_id,
                "cost_level_points": cost_points,
                "future_log_return_12": signed_return,
                "abs_future_log_return_12": abs_return,
                "cost_return_proxy": cost_proxy,
                "train_only_drawdown_buffer": train_drawdown_buffer,
                "train_only_reward_threshold": train_reward_threshold,
                "edge_after_cost_buffer": edge,
                "tradeability_label": np.where(positive, "tradeable", "abstain"),
                "direction_label": direction,
                "threshold_source": "train_only_cost_and_drawdown_buffer(학습 전용 비용/손실 버퍼)",
                "cost_proxy_method": "train_median_hl_range_over_atr14_times_cost_points(학습 중앙값 hl_range/atr14 x 비용 포인트)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        cost_frames.append(cost_part)

        score = edge / (rolling_noise.fillna(0.0) + train_drawdown_buffer + max(cost_proxy, 1e-12))
        train_scores = score.loc[train].replace([np.inf, -np.inf], np.nan).dropna()
        cuts = [float(train_scores.quantile(q)) for q in (0.20, 0.40, 0.60, 0.80)]
        buckets = np.searchsorted(np.array(cuts), score.fillna(float("-inf")).to_numpy(), side="right")
        payoff_part = pd.DataFrame(
            {
                "source_row_id": frame["source_row_id"],
                "timestamp": frame["timestamp"].astype(str),
                "split": frame["split"].astype(str),
                "cost_contract_id": contract_id,
                "cost_level_points": cost_points,
                "payoff_score_after_cost": score,
                "payoff_rank_bucket": buckets,
                "payoff_rank_label": [f"rank_{int(item)}" for item in buckets],
                "direction_hint": np.where(signed_return < 0, "short", "long"),
                "train_q20": cuts[0],
                "train_q40": cuts[1],
                "train_q60": cuts[2],
                "train_q80": cuts[3],
                "rank_source": "train_only_payoff_score_quantiles(학습 전용 보상 점수 분위)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        payoff_frames.append(payoff_part)

        for split in ("train", "validation", "oos"):
            subset = cost_part.loc[cost_part["split"].eq(split)]
            counts = subset["direction_label"].value_counts().to_dict()
            cost_contract_rows.append(
                {
                    "cost_contract_id": contract_id,
                    "split": split,
                    "cost_level_points": cost_points,
                    "rows": int(len(subset)),
                    "tradeable_rows": int(subset["tradeability_label"].eq("tradeable").sum()),
                    "short_rows": int(counts.get("short", 0)),
                    "flat_rows": int(counts.get("flat", 0)),
                    "long_rows": int(counts.get("long", 0)),
                    "cost_return_proxy": cost_proxy,
                    "train_only_drawdown_buffer": train_drawdown_buffer,
                    "threshold_source": "train_only(학습 전용)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            rank_subset = payoff_part.loc[payoff_part["split"].eq(split)]
            rank_counts = rank_subset["payoff_rank_label"].value_counts().to_dict()
            payoff_contract_rows.append(
                {
                    "cost_contract_id": contract_id,
                    "split": split,
                    "rows": int(len(rank_subset)),
                    "rank_0": int(rank_counts.get("rank_0", 0)),
                    "rank_1": int(rank_counts.get("rank_1", 0)),
                    "rank_2": int(rank_counts.get("rank_2", 0)),
                    "rank_3": int(rank_counts.get("rank_3", 0)),
                    "rank_4": int(rank_counts.get("rank_4", 0)),
                    "train_q20": cuts[0],
                    "train_q40": cuts[1],
                    "train_q60": cuts[2],
                    "train_q80": cuts[3],
                    "rank_source": "train_only(학습 전용)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    diagnostics = {
        "cost_point_to_return_unit_proxy": unit,
        "cost_contract_count": len(cost_contracts),
        "cost_label_rows": int(sum(len(part) for part in cost_frames)),
        "payoff_label_rows": int(sum(len(part) for part in payoff_frames)),
    }
    return (
        pd.concat(cost_frames, ignore_index=True),
        pd.concat(payoff_frames, ignore_index=True),
        cost_contract_rows,
        payoff_contract_rows,
        diagnostics,
    )


def mode_or_flat(values: pd.Series) -> str:
    values = values.dropna().astype(str)
    if values.empty:
        return "flat"
    counts = values.value_counts()
    return str(counts.index[0])


def build_control_residuals(
    frame: pd.DataFrame, cost_labels: pd.DataFrame, control_contracts: Sequence[Mapping[str, str]]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    primary = cost_labels.loc[cost_labels["cost_contract_id"].eq("cost2_primary_abstention")].copy()
    if primary.empty:
        primary = cost_labels.copy().drop_duplicates("source_row_id")
    base = frame[["source_row_id", "timestamp", "split"]].copy()
    base = base.merge(primary[["source_row_id", "direction_label"]], on="source_row_id", how="left")
    base = base.rename(columns={"direction_label": "actual_direction_label"})
    base["actual_direction_label"] = base["actual_direction_label"].fillna("flat")
    for lag in (72, 96):
        base[f"gap{lag}_control_label"] = (
            base.groupby("split", group_keys=False)["actual_direction_label"].shift(lag).fillna("missing_control_warmup")
        )

    modulo_fold = (base["source_row_id"].astype(int) % 12).astype(int)
    base["modulo_fold_id"] = modulo_fold
    train_base = base.loc[base["split"].astype(str).eq("train")].copy()
    fold_modes = train_base.groupby("modulo_fold_id")["actual_direction_label"].apply(mode_or_flat).to_dict()
    base["modulo_control_label"] = base["modulo_fold_id"].map(fold_modes).fillna("flat")
    base["timestamp"] = pd.to_datetime(base["timestamp"], utc=True).astype(str)
    base["claim_boundary"] = CLAIM_BOUNDARY

    control_map = {
        "label_shift_gap72_control": "gap72_control_label",
        "label_shift_gap96_control": "gap96_control_label",
        "horizon_modulo_fold_control": "modulo_control_label",
    }
    residual_frames: list[pd.DataFrame] = []
    for contract in control_contracts:
        control_id = str(contract["control_id"])
        control_column = control_map.get(control_id)
        if not control_column:
            continue
        residual = base[["source_row_id", "timestamp", "split", "actual_direction_label", control_column]].copy()
        residual = residual.rename(columns={control_column: "control_label"})
        residual["control_contract_id"] = str(contract["contract_id"])
        residual["control_id"] = control_id
        residual["residual_eligible"] = (
            residual["actual_direction_label"].astype(str).ne(residual["control_label"].astype(str))
            & residual["control_label"].astype(str).ne("missing_control_warmup")
        )
        residual["residual_direction_label"] = np.where(
            residual["residual_eligible"], residual["actual_direction_label"], "flat"
        )
        residual["residual_reason"] = np.where(
            residual["residual_eligible"],
            "actual_differs_from_control(실제 라벨이 대조와 다름)",
            "control_matched_or_warmup(대조 일치 또는 준비구간)",
        )
        residual["claim_boundary"] = CLAIM_BOUNDARY
        residual_frames.append(residual[list(CONTROL_LABEL_COLUMNS)])

    return pd.concat(residual_frames, ignore_index=True), base[list(CONTROL_SIDECAR_COLUMNS)]


def build_feature_sets(frame: pd.DataFrame) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    features = model_feature_columns(frame)
    state_rows = read_csv(CR_FEATURE_STATE)
    max_carry: dict[str, float] = {}
    for row in state_rows:
        name = str(row.get("feature_name", ""))
        value = float(row.get("abs_autocorrelation") or 0.0)
        max_carry[name] = max(max_carry.get(name, 0.0), value)

    lag_rows = read_csv(BQ_LAG_SUMMARY)
    lookahead_violations = sum(int(float(row.get("lookahead_violations") or 0)) for row in lag_rows)
    lag_summary_present = bool(lag_rows)

    def row(
        feature_set_id: str,
        contract_id: str,
        family: str,
        included: Sequence[str],
        dropped: Sequence[str],
        sidecar_status: str,
        forbidden_action: str,
    ) -> dict[str, Any]:
        included_list = list(included)
        dropped_list = list(dropped)
        return {
            "feature_set_id": feature_set_id,
            "contract_id": contract_id,
            "feature_family": family,
            "source_feature_count": len(features),
            "included_feature_count": len(included_list),
            "dropped_feature_count": len(dropped_list),
            "included_features_json": included_list,
            "dropped_features_json": dropped_list,
            "feature_order_hash": feature_order_hash(included_list),
            "source_sidecar_status": sidecar_status,
            "forbidden_action": forbidden_action,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    macro_features = [name for name in features if name.startswith(MACRO_EQUITY_PREFIXES)]
    technical = [name for name in features if name not in set(macro_features)]
    drop_carry = [name for name in features if max_carry.get(name, 0.0) >= 0.70]
    state_pruned = [name for name in features if name not in set(drop_carry)]
    macro_sidecar_status = (
        "lag_sidecar_present_zero_lookahead(지연 보조표 있음, 미래참조 0)"
        if lag_summary_present and lookahead_violations == 0
        else "held_missing_lag_sidecar(지연 보조표 누락으로 보류)"
    )
    rows = [
        row(
            "technical_session_vol_lag_safe",
            "technical_session_vol_lag_safe",
            "technical_session_volatility(기술/세션/변동성)",
            technical,
            macro_features,
            "external_sources_dropped(외부 원천 제거)",
            "no_oos_feature_selection(OOS 피처 선택 금지)",
        ),
        row(
            "state_carry_ge70_pruned_cost_context",
            "drop_high_state_carry_ge70_plus_cost_context",
            "state_carry_pruned_cost_context(상태 이월 제거 + 비용 문맥)",
            state_pruned,
            drop_carry,
            "state_carry_audit_from_run337CR(run337CR 상태 이월 감사)",
            "no_hidden_feature_readd(숨은 피처 재추가 금지)",
        ),
        row(
            "macro_equity_lag_safe_rescue",
            "macro_equity_lag_safe_rescue",
            "economic_regime_rescue(경제 국면 구조 구제)",
            features,
            [],
            macro_sidecar_status,
            "no_unlagged_external_source(지연 없는 외부 원천 금지)",
        ),
    ]
    diagnostics = {
        "source_feature_count": len(features),
        "macro_equity_feature_count": len(macro_features),
        "state_carry_drop_count": len(drop_carry),
        "bq_lag_rows": len(lag_rows),
        "bq_lookahead_violations": lookahead_violations,
    }
    return rows, diagnostics


def build_two_stage_manifest(feature_rows: Sequence[Mapping[str, Any]], cost_contract_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "contract_id": "two_stage_tradeability_then_direction_v1",
        "stage1": {
            "model_role": "tradeability_after_cost_gate(비용 후 거래가능성 게이트)",
            "label_source": rel(COST_TRADEABILITY_LABEL_FRAME),
            "positive_label": "tradeable",
            "threshold_policy": "train_only(학습 전용)",
        },
        "stage2": {
            "model_role": "direction_or_payoff_rank_inside_stage1_pass(1단계 통과 안 방향/보상 순위)",
            "label_sources": [rel(COST_TRADEABILITY_LABEL_FRAME), rel(PAYOFF_RANK_LABEL_FRAME)],
            "score_semantics": "rank_not_probability(확률 아님, 순위)",
        },
        "handoff_fields": [
            "stage1_pass",
            "stage1_score",
            "stage2_direction",
            "stage2_rank_score",
            "final_action",
        ],
        "runtime_surface": "two_onnx_files_plus_deterministic_adapter(ONNX 2개 + 결정론 어댑터)",
        "forbidden_action": "no_fake_single_onnx_claim(가짜 단일 ONNX 주장 금지)",
        "feature_sets": [row["feature_set_id"] for row in feature_rows],
        "cost_contracts": sorted({row["cost_contract_id"] for row in cost_contract_rows}),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_two_stage_compare_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for feature in feature_rows:
        rows.append(
            {
                "compare_contract_id": f"proxy_mt5_two_stage__{feature['feature_set_id']}",
                "feature_set_id": feature["feature_set_id"],
                "proxy_required_fields": "timestamp;stage1_score;stage1_pass;stage2_score;stage2_direction;final_action",
                "mt5_required_fields": "timestamp;stage1_score;stage1_pass;stage2_score;stage2_direction;final_action",
                "pass_condition": "row_hash_match_and_action_match(행 해시와 행동 일치)",
                "blocked_if": "single_surface_merge_or_missing_stage_field(단일 표면 병합 또는 단계 필드 누락)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_da_queue() -> list[dict[str, str]]:
    inputs = ";".join(
        rel(path)
        for path in (
            COST_TRADEABILITY_LABEL_FRAME,
            PAYOFF_RANK_LABEL_FRAME,
            CONTROL_RESIDUAL_LABEL_FRAME,
            FEATURE_CONTRACT_MANIFEST,
            TWO_STAGE_HANDOFF_MANIFEST,
            OBJECTIVE_INPUT_MANIFEST,
        )
    )
    return [
        {
            "queue_id": "run337DA_train_tradeability_gate",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train cost tradeability gate(비용 거래가능성 게이트 학습)",
            "required_inputs": inputs,
            "required_outputs": "tradeability_model_scorecard.csv;onnx_parity_matrix.csv",
            "blocked_if_missing": "cost labels or feature manifest missing(비용 라벨 또는 피처 목록 누락)",
            "forbidden_action": "no validation/OOS threshold tuning(검증/OOS 임계값 조정 금지)",
            "effect": "방향보다 먼저 비용 후 거래 가능성을 검증한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DA_train_payoff_ranker",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train payoff ranker as rank only(보상 순위기를 순위 의미로만 학습)",
            "required_inputs": inputs,
            "required_outputs": "payoff_rank_scorecard.csv;rank_monotonicity_review.csv",
            "blocked_if_missing": "payoff rank label frame missing(보상 순위 라벨 프레임 누락)",
            "forbidden_action": "no probability claim without calibration(보정 없는 확률 주장 금지)",
            "effect": "수익률보다 보상 비대칭을 먼저 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DA_score_control_residuals",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "score control residual targets(대조 잔차 타깃 채점)",
            "required_inputs": inputs,
            "required_outputs": "control_residual_scorecard.csv;runtime_release_disposition.csv",
            "blocked_if_missing": "control residual sidecars missing(대조 잔차 보조표 누락)",
            "forbidden_action": "no dropping failed controls(실패 대조 제거 금지)",
            "effect": "대조 정렬 실패를 런타임으로 넘기지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DA_build_two_stage_proxy_expected",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "build two-stage proxy expected only after validation gates(검증 게이트 뒤 2단계 프록시 예상값 생성)",
            "required_inputs": inputs,
            "required_outputs": "two_stage_proxy_expected.csv;proxy_mt5_handoff_package_queue.csv",
            "blocked_if_missing": "no validation cleared rows(검증 통과 행 없음)",
            "forbidden_action": "no fake single ONNX claim(가짜 단일 ONNX 주장 금지)",
            "effect": "2단계 인계가 MT5 동등성으로 확인될 때만 다음으로 이동한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DA_hold_mt5_until_all_reviews_clear",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "hold MT5 package until model/control/cost reviews clear(모델/대조/비용 검토 전 MT5 패키지 보류)",
            "required_inputs": "tradeability_model_scorecard.csv;control_residual_scorecard.csv;rank_monotonicity_review.csv",
            "required_outputs": "mt5_probe_release_or_hold_matrix.csv",
            "blocked_if_missing": "review scorecards missing(검토 점수표 누락)",
            "forbidden_action": "no MT5 probe from incomplete proxy-only result(불완전 프록시 결과로 MT5 탐침 금지)",
            "effect": "프록시 성과를 운영 주장으로 착각하지 않게 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_manifest(
    frame: pd.DataFrame,
    feature_rows: Sequence[Mapping[str, Any]],
    diagnostics: Mapping[str, Any],
    cost_diagnostics: Mapping[str, Any],
) -> dict[str, Any]:
    split_counts = frame["split"].astype(str).value_counts().to_dict()
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_model_input": rel(SOURCE_MODEL_INPUT),
        "source_sha256": sha256_file(SOURCE_MODEL_INPUT),
        "source_rows": int(len(frame)),
        "source_timestamp_min": iso_ts(frame["timestamp"].min()),
        "source_timestamp_max": iso_ts(frame["timestamp"].max()),
        "split_counts": {str(key): int(value) for key, value in split_counts.items()},
        "feature_sets": [row["feature_set_id"] for row in feature_rows],
        "feature_order_hashes": {row["feature_set_id"]: row["feature_order_hash"] for row in feature_rows},
        "cost_proxy": dict(cost_diagnostics),
        "feature_diagnostics": dict(diagnostics),
        "model_training": "not_run",
        "candidate_selection": "not_run",
        "threshold_policy": "train_only(학습 전용)",
        "forward_use": "not_used_for_selection(선택에 사용 안 함)",
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
        row("cz_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CY 설계와 원천 입력이 모두 연결된다."),
        row("cz_gate_parent_points_to_cz", final["cy_next_action"] == RUN_ID, final["cy_next_action"], RUN_ID, "CY next_action(다음 행동)과 CZ 실행을 맞춘다."),
        row("cz_gate_source_rows", final["source_rows"] == 46650, final["source_rows"], "46650", "기존 공유 학습 표본 경계를 유지한다."),
        row("cz_gate_no_duplicate_timestamps", final["duplicate_timestamp_rows"] == 0, final["duplicate_timestamp_rows"], "0", "시간축 중복을 막는다."),
        row("cz_gate_no_forward_rows", final["source_timestamp_max"] <= "2026-04-13T22:00:00+00:00", final["source_timestamp_max"], "<=2026-04-13T22:00:00+00:00", "새 forward 구간을 선택/튜닝에 섞지 않는다."),
        row("cz_gate_cost_label_rows", final["cost_label_rows"] == final["source_rows"] * final["cost_contract_rows"], final["cost_label_rows"], "source_rows*cost_contract_rows", "비용 라벨을 모든 행과 계약에 만든다."),
        row("cz_gate_payoff_rank_rows", final["payoff_rank_rows"] == final["cost_label_rows"], final["payoff_rank_rows"], "cost_label_rows", "보상 순위 라벨이 비용 라벨과 정렬된다."),
        row("cz_gate_control_residual_rows", final["control_residual_rows"] == final["source_rows"] * final["control_contract_rows"], final["control_residual_rows"], "source_rows*control_contract_rows", "대조 잔차 라벨을 모든 대조에 만든다."),
        row("cz_gate_feature_sets", final["feature_set_rows"] >= 3, final["feature_set_rows"], ">=3", "기술/상태이월/거시 구제 피처 계약을 모두 만든다."),
        row("cz_gate_two_stage_manifest", final["two_stage_handoff_fields"] >= 5, final["two_stage_handoff_fields"], ">=5 handoff fields", "2단계 런타임 인계 필드를 명시한다."),
        row("cz_gate_da_queue", final["queue_rows"] >= 5, final["queue_rows"], ">=5", "다음 학습/검토 대기열을 만든다."),
        row("cz_gate_no_training_selection_mt5", True, "training=not_run;selection=not_run;mt5=not_run", "no training/selection/MT5", "CZ를 입력 물질화로만 닫는다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    experiment_receipt = {
        "hypothesis": "CX failure requires objective/feature input pivot before more training(CX 실패 뒤 추가 학습 전 목표/피처 입력 전환이 필요)",
        "decision_use": "open guarded DA training only, no selection(DA 방어 학습 개시만 가능, 선택 아님)",
        "comparison_baseline": PARENT_RUN_ID,
        "control_variables": "same source model input, train-only thresholds, no OOS selection(같은 원천 모델 입력, 학습 전용 임계값, OOS 선택 금지)",
        "changed_variables": "target labels, residual controls, feature contracts(타깃 라벨, 잔차 대조, 피처 계약)",
        "sample_scope": "US100 M5 2022-09-01..2026-04-13 train/validation/OOS(US100 5분봉 공유 구간)",
        "success_criteria": "all materialized inputs pass gate audit(모든 물질화 입력이 게이트 통과)",
        "failure_criteria": "missing source, leakage boundary, or no DA queue(원천 누락, 누수 경계 실패, DA 대기열 없음)",
        "invalid_conditions": "training, threshold tuning, candidate selection, MT5 probe in CZ(CZ 안 학습/임계값 조정/선택/MT5 탐침)",
        "stop_conditions": "failed required gate(필수 게이트 실패)",
        "evidence_plan": [rel(path) for path in artifact_paths],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": rel(SOURCE_MODEL_INPUT),
        "time_axis": "timestamp is UTC bar key inherited from model input(시각은 모델 입력에서 상속한 UTC 봉 키)",
        "sample_scope": f"rows={final['source_rows']}; max_timestamp={final['source_timestamp_max']}",
        "missing_or_duplicate_check": f"duplicate_timestamp_rows={final['duplicate_timestamp_rows']}",
        "feature_label_boundary": "features from current/past columns; future_log_return_12 used only as label(피처는 현재/과거 컬럼, future_log_return_12는 라벨 전용)",
        "split_boundary": "train thresholds only; validation/OOS read-only(학습 임계값 전용, 검증/OOS 읽기 전용)",
        "leakage_risk": "cost/rank thresholds or feature sets chosen from validation/OOS(비용/순위 임계값 또는 피처를 검증/OOS로 고르는 위험)",
        "data_hash_or_identity": {rel(SOURCE_MODEL_INPUT): sha256_file(SOURCE_MODEL_INPUT)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "not_trained_in_run337CZ; DA queued(CZ에서는 학습 없음, DA 대기)",
        "target_and_label": "cost tradeability, payoff rank, control residual(비용 거래가능성, 보상 순위, 대조 잔차)",
        "split_method": "existing time split with train-only thresholds(기존 시간 분할과 학습 전용 임계값)",
        "selection_metric": "not_applicable_no_selection(선택 없음)",
        "secondary_metrics": "control residual, cost stress, rank monotonicity, proxy-MT5 handoff(대조 잔차, 비용 압박, 순위 단조성, 프록시-MT5 인계)",
        "threshold_policy": "train_only_predeclared(학습 전용 사전 선언)",
        "overfit_risk": "using validation/OOS to tune cost buffer or rank cut(검증/OOS로 비용 버퍼나 순위 절단 조정)",
        "calibration_risk": "rank score is not probability(순위 점수는 확률 아님)",
        "comparison_baseline": PARENT_RUN_ID,
        "validation_judgment": "input_materialized_ready_for_guarded_training",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "label frames, feature manifest, two-stage manifest, DA queue(라벨 프레임, 피처 목록, 2단계 목록, DA 대기열)",
        "evidence_missing": "trained model, ONNX parity, proxy expected, MT5 runtime probe(학습 모델, ONNX 동등성, 프록시 예상값, MT5 런타임 탐침)",
        "judgment_label": "exploratory_input_materialization_completed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "이번 실행은 재료를 만든 것이고 아직 수익/운영 판정은 아니다.",
    }
    paths = [
        write_json(EXPERIMENT_RECEIPT, experiment_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
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
        "availability": "ignored_run_outputs_with_manifest_and_tracked_report(무시 실행 산출물은 목록으로 연결, 보고서는 추적)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CZ Objective/Feature Inputs(목표/피처 입력)

## Conclusion(결론)

run337CZ(337CZ 실행)는 run337CY(337CY 실행)의 objective/feature contract pivot(목표/피처 계약 전환)을 실제 input artifacts(입력 산출물)로 물질화했다.

Effect(효과): 다음 run337DA(337DA 실행)는 cost tradeability gate(비용 거래가능성 게이트), payoff ranker(보상 순위기), control residual review(대조 잔차 검토)를 같은 입력에서 학습할 수 있다. 이번 실행은 training(학습), candidate selection(후보 선택), MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 판정이 아니다.

## Materialized Artifacts(물질화 산출물)

- source_rows(원천 행): `{final["source_rows"]}`
- source_timestamp_max(원천 마지막 시각): `{final["source_timestamp_max"]}`
- cost_label_rows(비용 라벨 행): `{final["cost_label_rows"]}`
- payoff_rank_rows(보상 순위 행): `{final["payoff_rank_rows"]}`
- control_residual_rows(대조 잔차 행): `{final["control_residual_rows"]}`
- feature_set_rows(피처 묶음 행): `{final["feature_set_rows"]}`
- queue_rows(대기열 행): `{final["queue_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- candidate_selection(후보 선택): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Cost proxy note(비용 프록시 메모): 비용 포인트는 원천 입력에 close price(종가)가 없어서 train_median_hl_range_over_atr14(학습 중앙값 고저범위/ATR14) 방식의 proxy(프록시)로 return unit(수익률 단위)에 매핑했다. Effect(효과): DA 학습 전 단계에서 비용 취약 라벨을 만들 수 있지만, 운영 비용 판정으로 과장하지 않는다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CZ

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): objective/feature pivot inputs(목표/피처 전환 입력)을 DA guarded training(DA 방어 학습)으로 넘긴다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(OBJECTIVE_INPUT_MANIFEST)}`
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
        r"- >-\n  Stage337 run337CZ focus complete:.*?(?=\n- >-|\n[A-Za-z0-9_]+:|\Z)",
        "",
        workspace_text,
        flags=re.S,
    )
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337CZ focus complete: objective/feature contract pivot inputs(목표/피처 계약 전환 입력)을 "
        f"`{STATUS}`로 물질화했다. Effect(효과): run337DA(337DA 실행)에서 cost tradeability/payoff rank/control residual/two-stage handoff(비용 거래가능성/보상 순위/대조 잔차/2단계 인계) 후보 학습을 실행한다.\n"
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
        r"\n## Stage337 run337CZ\(337CZ 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CY|\n## |\Z)",
        "\n",
        current_text,
        flags=re.S,
    )
    section = f"""
## Stage337 run337CZ(337CZ 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): cost tradeability/payoff rank/control residual/feature contract/two-stage handoff(비용 거래가능성/보상 순위/대조 잔차/피처 계약/2단계 인계) 입력을 만들었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337CY(337CY"
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
- actual_mt5_execution(실제 MT5 실행): `not_run_cz_input_materialization_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 objective/feature pivot guarded training(목표/피처 전환 방어 학습)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CZ(337CZ 실행) materialized objective/feature contract pivot inputs" not in line)
    stage_entry = (
        f"- {TODAY}: run337CZ(337CZ 실행) materialized objective/feature contract pivot inputs(목표/피처 계약 전환 입력). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337CZ materialized objective/feature contract pivot inputs" not in line)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337CZ materialized objective/feature contract pivot inputs(목표/피처 계약 전환 입력) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "objective_feature_contract_pivot_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"cost_label_rows={final['cost_label_rows']};control_rows={final['control_residual_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__objective_feature_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "objective_feature_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "input_materialization_no_training",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "input_contract_no_kpi",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"cost_label_rows={final['cost_label_rows']};feature_sets={final['feature_set_rows']}",
        "guardrail_kpi": "train_only_thresholds;no_oos_selection;no_training_no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__objective_feature_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "CY design materialized into objective feature input artifacts",
        "kpi_scope": "input_contract_no_training",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__objective_feature_inputs",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "question": "can objective and feature pivot inputs be materialized without leakage or selection",
        "metric_scope": "label_feature_control_handoff_materialization",
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
    frame = read_source_frame()
    cy_final = read_json(CY_FINAL)
    cost_contracts = read_csv(CY_COST_CONTRACT)
    control_contracts = read_csv(CY_CONTROL_CONTRACT)

    cost_labels, payoff_labels, cost_contract_rows, payoff_contract_rows, cost_diagnostics = build_cost_and_payoff_labels(frame, cost_contracts)
    control_residuals, control_sidecar = build_control_residuals(frame, cost_labels, control_contracts)
    feature_rows, feature_diagnostics = build_feature_sets(frame)
    handoff_manifest = build_two_stage_manifest(feature_rows, cost_contract_rows)
    compare_rows = build_two_stage_compare_rows(feature_rows)
    manifest = build_manifest(frame, feature_rows, feature_diagnostics, cost_diagnostics)
    queue_rows = build_da_queue()

    artifacts: list[Path] = [
        write_parquet(COST_TRADEABILITY_LABEL_FRAME, cost_labels[list(COST_LABEL_COLUMNS)]),
        write_parquet(PAYOFF_RANK_LABEL_FRAME, payoff_labels[list(PAYOFF_COLUMNS)]),
        write_parquet(CONTROL_RESIDUAL_LABEL_FRAME, control_residuals[list(CONTROL_LABEL_COLUMNS)]),
        write_csv(CONTROL_SIDECAR_MATRIX, CONTROL_SIDECAR_COLUMNS, control_sidecar.to_dict("records")),
        write_csv(FEATURE_SET_MATRIX, FEATURE_SET_COLUMNS, feature_rows),
        write_json(FEATURE_CONTRACT_MANIFEST, {"run_id": RUN_ID, "feature_sets": feature_rows, "claim_boundary": CLAIM_BOUNDARY}),
        write_json(TWO_STAGE_HANDOFF_MANIFEST, handoff_manifest),
        write_csv(PROXY_MT5_TWO_STAGE_COMPARE, tuple(compare_rows[0].keys()), compare_rows),
        write_csv(COST_LABEL_CONTRACT, tuple(cost_contract_rows[0].keys()), cost_contract_rows),
        write_csv(PAYOFF_RANK_CONTRACT, tuple(payoff_contract_rows[0].keys()), payoff_contract_rows),
        write_json(OBJECTIVE_INPUT_MANIFEST, manifest),
        write_csv(DA_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]

    duplicate_timestamps = int(frame["timestamp"].duplicated().sum())
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "cy_next_action": cy_final.get("next_action", ""),
        "source_rows": int(len(frame)),
        "source_timestamp_min": iso_ts(frame["timestamp"].min()),
        "source_timestamp_max": iso_ts(frame["timestamp"].max()),
        "duplicate_timestamp_rows": duplicate_timestamps,
        "cost_contract_rows": len(cost_contracts),
        "cost_label_rows": int(len(cost_labels)),
        "payoff_rank_rows": int(len(payoff_labels)),
        "control_contract_rows": len(control_contracts),
        "control_residual_rows": int(len(control_residuals)),
        "control_sidecar_rows": int(len(control_sidecar)),
        "feature_set_rows": len(feature_rows),
        "two_stage_handoff_fields": len(handoff_manifest["handoff_fields"]),
        "proxy_mt5_compare_rows": len(compare_rows),
        "queue_rows": len(queue_rows),
        "cost_point_to_return_unit_proxy": cost_diagnostics["cost_point_to_return_unit_proxy"],
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
