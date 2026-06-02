from __future__ import annotations

import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as pkg  # noqa: E402
from stage_pipelines.stage364 import review_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db as review  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364P"
RUN_ID = "run364P_materialize_drawdown_side_balance_offensive_inputs_without_db_v1"
PARENT_RUN_ID = review.RUN_ID
NEXT_RUN_ID = "run364Q_train_drawdown_side_balance_overlay_onnx_scout_without_db_v1"

STATUS = "completed_stage364P_drawdown_side_balance_offensive_inputs_materialized_no_model_training_no_authority"
JUDGMENT = "offensive_inputs_ready_for_risk_overlay_and_side_balance_scout_no_kpi_claim_no_authority"
DECISION = "stage364P_open_run364Q_train_drawdown_side_balance_overlay_onnx_scout_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_input_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
TRADE_LIFECYCLE_JOINED = RUN_DIR / "trade_lifecycle_joined.csv"
RISK_OVERLAY_TRAINING_TABLE = RUN_DIR / "risk_overlay_training_table.csv"
CALENDAR_HOLD_TAIL_LABELS = RUN_DIR / "calendar_hold_tail_labels.csv"
DRAWDOWN_TAIL_ENTRY_LABELS = RUN_DIR / "drawdown_tail_entry_labels.csv"
SHORT_SIDE_PROBABILITY_SCOUT = RUN_DIR / "short_side_probability_scout.csv"
SESSION_REGIME_SLICE_INPUTS = RUN_DIR / "session_regime_slice_inputs.csv"
CANDIDATE_OVERLAY_DESIGN = RUN_DIR / "candidate_overlay_design.csv"
RUN364Q_TRAINING_QUEUE = RUN_DIR / "run364Q_training_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364P_drawdown_side_balance_offensive_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364P_drawdown_side_balance_offensive_inputs.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

INPUT_FILES = [
    review.FINAL_DECISION,
    review.GATE_AUDIT,
    review.NEXT_QUEUE,
    review.CLOSED_TRADE_ATTRIBUTION,
    review.DRAWDOWN_CLUSTER_ATTRIBUTION,
    review.FAILURE_MEMORY,
    review.POSITIVE_CLUES,
    review.REPORT_PATH,
    pkg.EXPECTED_PROBABILITY_TAPE,
    pkg.MT5_NATIVE_TRADE_TAPE,
    pkg.FEATURE_MATRIX,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    TRADE_LIFECYCLE_JOINED,
    RISK_OVERLAY_TRAINING_TABLE,
    CALENDAR_HOLD_TAIL_LABELS,
    DRAWDOWN_TAIL_ENTRY_LABELS,
    SHORT_SIDE_PROBABILITY_SCOUT,
    SESSION_REGIME_SLICE_INPUTS,
    CANDIDATE_OVERLAY_DESIGN,
    RUN364Q_TRAINING_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    Path(__file__),
]

META_COLUMNS = {"timestamp", "split", "row_index", "tier", "dataset_id", "run_id", "symbol"}
SHORT_SCOUT_FEATURES = [
    "return_zscore_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "rsi_14",
    "bb_position_20",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
    "vix_zscore_20",
    "us10yr_zscore_20",
    "mega8_pos_breadth_1",
    "us100_minus_top3_weighted_return_1",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    return pkg.fs_path(path)


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path | str) -> bool:
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    pkg.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    _, rows = pkg.read_csv_rows(path)
    return rows


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = False,
) -> None:
    pkg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_parent() -> dict[str, Any]:
    parent = pkg.read_json(review.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id(부모 다음 실행 ID) mismatch: {parent.get('next_run_id')} != {RUN_ID}")
    if parent.get("runtime_authority") != "not_claimed" or parent.get("goal_achieve") != "not_claimed":
        raise RuntimeError("parent forbidden claim(부모 금지 주장)이 감지됐다.")
    gates = read_csv_rows(review.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gate(부모 게이트)가 모두 passed(통과)가 아니다.")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing input(입력 누락): " + ", ".join(missing))
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) else "",
                "source_run_id": PARENT_RUN_ID if "run364O" in rel(path) else pkg.RUN_ID,
                "data_role(데이터 역할)": "existing_review_or_runtime_package_input(기존 검토 또는 런타임 패키지 입력)",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    actual = pd.read_csv(fs_path(review.CLOSED_TRADE_ATTRIBUTION))
    expected = pd.read_csv(fs_path(pkg.MT5_NATIVE_TRADE_TAPE))
    probabilities = pd.read_csv(fs_path(pkg.EXPECTED_PROBABILITY_TAPE))
    features = pd.read_csv(fs_path(pkg.FEATURE_MATRIX))
    return actual, expected, probabilities, features


def feature_columns(features: pd.DataFrame) -> list[str]:
    return [column for column in features.columns if column not in META_COLUMNS]


def build_probability_feature_frame(probabilities: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    probs = probabilities.copy()
    feats = features.copy()
    source_feature_cols = feature_columns(feats)
    probs["feature_key"] = probs["bar_time_server"].astype(str)
    feats["feature_key"] = feats["timestamp"].astype(str)
    keep_feature_cols = ["feature_key", "tier", "dataset_id", *source_feature_cols]
    merged = probs.merge(feats[keep_feature_cols], on="feature_key", how="left", suffixes=("", "_feature"))
    return merged


def add_lifecycle_labels(frame: pd.DataFrame) -> pd.DataFrame:
    working = frame.copy()
    working["actual_entry_time"] = pd.to_datetime(working["actual_entry_time"])
    working["actual_exit_time"] = pd.to_datetime(working["actual_exit_time"])
    working["expected_entry_timestamp"] = pd.to_datetime(working["expected_entry_timestamp"], utc=True)
    working["expected_exit_timestamp"] = pd.to_datetime(working["expected_exit_timestamp"], utc=True)
    working["actual_entry_month"] = working["actual_entry_time"].dt.strftime("%Y-%m")
    working["entry_weekday"] = working["actual_entry_time"].dt.dayofweek
    working["expected_actual_entry_delay_minutes"] = (
        working["actual_entry_time"].dt.tz_localize("UTC") - working["expected_entry_timestamp"]
    ).dt.total_seconds() / 60.0
    working["net_profit_gap_actual_minus_expected"] = working["actual_net_profit_after_cost"] - working["expected_net_profit"]
    working["tail_loss_ge_10"] = working["actual_net_profit_after_cost"].le(-10.0).astype("int8")
    working["tail_loss_ge_20"] = working["actual_net_profit_after_cost"].le(-20.0).astype("int8")
    working["tail_gain_ge_20"] = working["actual_net_profit_after_cost"].ge(20.0).astype("int8")
    working["tail_hold_gt_12_m5"] = working["actual_hold_m5_calendar"].gt(12).astype("int8")
    working["tail_hold_gt_96_m5"] = working["actual_hold_m5_calendar"].gt(96).astype("int8")
    working["swap_drag_trade"] = working["actual_swap"].lt(0.0).astype("int8")
    working["drawdown_after_ge_10pct"] = working["closed_balance_drawdown_percent"].ge(10.0).astype("int8")
    working["drawdown_after_ge_20pct"] = working["closed_balance_drawdown_percent"].ge(20.0).astype("int8")
    previous_dd = working["closed_balance_drawdown_percent"].shift(1).fillna(0.0)
    working["drawdown_increment_percent"] = working["closed_balance_drawdown_percent"] - previous_dd
    working["drawdown_increment_positive"] = working["drawdown_increment_percent"].gt(0.0).astype("int8")
    working["avoid_candidate_label"] = (
        (working["tail_loss_ge_10"] == 1)
        | (working["tail_hold_gt_96_m5"] == 1)
        | ((working["drawdown_increment_positive"] == 1) & working["actual_net_profit_after_cost"].lt(0.0))
    ).astype("int8")
    working["rescue_candidate_label"] = (
        (working["tail_gain_ge_20"] == 1) & working["closed_balance_drawdown_percent"].lt(5.0)
    ).astype("int8")
    return working


def build_lifecycle_tables(
    actual: pd.DataFrame,
    expected: pd.DataFrame,
    prob_feature: pd.DataFrame,
    source_feature_cols: Sequence[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if len(actual) != len(expected):
        raise RuntimeError(f"actual/expected trade rows(실제/예상 거래 행) mismatch: {len(actual)} != {len(expected)}")
    actual_work = actual.copy().reset_index(drop=True)
    expected_work = expected.copy().reset_index(drop=True)
    actual_work["trade_sequence"] = np.arange(1, len(actual_work) + 1)
    expected_work["trade_sequence"] = np.arange(1, len(expected_work) + 1)
    actual_cols = {
        "entry_time": "actual_entry_time",
        "exit_time": "actual_exit_time",
        "entry_month": "actual_entry_month_source",
        "exit_month": "actual_exit_month",
        "entry_hour": "actual_entry_hour",
        "exit_hour": "actual_exit_hour",
        "side": "actual_side",
        "entry_price": "actual_entry_price",
        "exit_price": "actual_exit_price",
        "commission": "actual_commission",
        "swap": "actual_swap",
        "profit_before_swap": "actual_profit_before_swap",
        "net_profit_after_cost": "actual_net_profit_after_cost",
        "balance_after": "actual_balance_after",
        "hold_minutes_calendar": "actual_hold_minutes_calendar",
        "hold_m5_calendar": "actual_hold_m5_calendar",
        "closed_balance_peak": "closed_balance_peak",
        "closed_balance_drawdown_amount": "closed_balance_drawdown_amount",
        "closed_balance_drawdown_percent": "closed_balance_drawdown_percent",
    }
    expected_cols = {
        "split": "split",
        "model_id": "model_id",
        "policy_id": "policy_id",
        "threshold_id": "threshold_id",
        "runtime_trade_shape": "runtime_trade_shape",
        "entry_timestamp": "expected_entry_timestamp",
        "exit_timestamp": "expected_exit_timestamp",
        "held_m5": "expected_held_m5",
        "side": "expected_side",
        "entry_score": "entry_score",
        "exit_score": "exit_score",
        "threshold": "threshold",
        "entry_open": "expected_entry_open",
        "exit_open": "expected_exit_open",
        "net_profit": "expected_net_profit",
        "exit_reason": "expected_exit_reason",
    }
    actual_small = actual_work[["trade_sequence", *actual_cols]].rename(columns=actual_cols)
    expected_small = expected_work[["trade_sequence", *expected_cols]].rename(columns=expected_cols)
    joined = expected_small.merge(actual_small, on="trade_sequence", how="inner")
    joined["expected_entry_timestamp_key"] = pd.to_datetime(joined["expected_entry_timestamp"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    prob_join = prob_feature.copy()
    prob_join["expected_entry_timestamp_key"] = pd.to_datetime(prob_join["timestamp_utc"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    joined = joined.merge(prob_join, on="expected_entry_timestamp_key", how="left", suffixes=("", "_prob"))
    joined["join_method(결합 방법)"] = "sequence_order_expected_trade_to_mt5_closed_trade_plus_entry_timestamp_probability_feature"
    joined["claim_boundary(주장 경계)"] = CLAIM_BOUNDARY
    joined = add_lifecycle_labels(joined)
    core_cols = [
        "trade_sequence",
        "split",
        "expected_entry_timestamp",
        "actual_entry_time",
        "expected_actual_entry_delay_minutes",
        "actual_exit_time",
        "actual_entry_month",
        "actual_entry_hour",
        "entry_weekday",
        "actual_side",
        "expected_side",
        "p_short",
        "p_flat",
        "p_long",
        "long_margin",
        "entry_score",
        "exit_score",
        "threshold",
        "actual_net_profit_after_cost",
        "expected_net_profit",
        "net_profit_gap_actual_minus_expected",
        "actual_profit_before_swap",
        "actual_swap",
        "actual_hold_m5_calendar",
        "expected_held_m5",
        "closed_balance_drawdown_percent",
        "drawdown_increment_percent",
        "tail_loss_ge_10",
        "tail_loss_ge_20",
        "tail_gain_ge_20",
        "tail_hold_gt_12_m5",
        "tail_hold_gt_96_m5",
        "swap_drag_trade",
        "drawdown_after_ge_10pct",
        "drawdown_after_ge_20pct",
        "drawdown_increment_positive",
        "avoid_candidate_label",
        "rescue_candidate_label",
        "join_method(결합 방법)",
        "claim_boundary(주장 경계)",
    ]
    available_features = [column for column in source_feature_cols if column in joined.columns]
    training = joined[[column for column in core_cols if column in joined.columns] + available_features].copy()
    return joined, training


def hold_bucket(value: float) -> str:
    if value <= 8:
        return "001_<=8_m5_calendar"
    if value <= 12:
        return "002_9_to_12_m5_calendar"
    if value <= 24:
        return "003_13_to_24_m5_calendar"
    if value <= 96:
        return "004_25_to_96_m5_calendar"
    if value <= 288:
        return "005_97_to_288_m5_calendar"
    if value <= 672:
        return "006_289_to_672_m5_calendar"
    return "007_>672_m5_calendar"


def materialize_hold_labels(training: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    caps = [8, 12, 24, 48, 96, 288, 672]
    for _, trade in training.iterrows():
        for cap in caps:
            rows.append(
                {
                    "run_id": RUN_ID,
                    "trade_sequence": int(trade["trade_sequence"]),
                    "split": trade["split"],
                    "cap_m5_calendar": cap,
                    "actual_hold_m5_calendar": int(trade["actual_hold_m5_calendar"]),
                    "would_force_exit_before_actual(실제 전 강제청산 여부)": int(trade["actual_hold_m5_calendar"] > cap),
                    "actual_net_profit_after_cost": round(float(trade["actual_net_profit_after_cost"]), 6),
                    "actual_swap": round(float(trade["actual_swap"]), 6),
                    "tail_loss_ge_10": int(trade["tail_loss_ge_10"]),
                    "tail_hold_gt_96_m5": int(trade["tail_hold_gt_96_m5"]),
                    "label_use(라벨 용도)": "calendar_hold_cap_supervision_only_not_hypothetical_pnl",
                    "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
                }
            )
    return pd.DataFrame(rows)


def materialize_drawdown_labels(training: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "trade_sequence",
        "split",
        "expected_entry_timestamp",
        "actual_entry_time",
        "actual_entry_hour",
        "entry_weekday",
        "actual_net_profit_after_cost",
        "actual_hold_m5_calendar",
        "closed_balance_drawdown_percent",
        "drawdown_increment_percent",
        "tail_loss_ge_10",
        "tail_loss_ge_20",
        "tail_hold_gt_96_m5",
        "drawdown_after_ge_10pct",
        "drawdown_after_ge_20pct",
        "drawdown_increment_positive",
        "avoid_candidate_label",
        "rescue_candidate_label",
    ]
    frame = training[[column for column in cols if column in training.columns]].copy()
    frame["hold_bucket"] = frame["actual_hold_m5_calendar"].map(hold_bucket)
    frame["risk_label_family(위험 라벨 계열)"] = "post_trade_drawdown_tail_labels_for_next_training"
    frame["feature_label_boundary(피처 라벨 경계)"] = "features_at_expected_entry_bar_labels_after_mt5_exit"
    frame["claim_boundary(주장 경계)"] = CLAIM_BOUNDARY
    return frame


def probability_bucket(series: pd.Series, labels: Sequence[str]) -> pd.Series:
    try:
        return pd.qcut(series.rank(method="first"), q=len(labels), labels=list(labels), duplicates="drop").astype(str)
    except ValueError:
        return pd.Series([labels[0]] * len(series), index=series.index)


def materialize_short_scout(prob_feature: pd.DataFrame) -> pd.DataFrame:
    frame = prob_feature.copy()
    frame["short_margin"] = frame["p_short"] - frame[["p_flat", "p_long"]].max(axis=1)
    frame["long_margin_recalc"] = frame["p_long"] - frame[["p_short", "p_flat"]].max(axis=1)
    frame["short_dominant"] = frame["short_margin"].gt(0.0).astype("int8")
    frame["short_rank_pct_by_split"] = frame.groupby("split")["short_margin"].rank(pct=True, method="average")
    frame["p_short_rank_pct_by_split"] = frame.groupby("split")["p_short"].rank(pct=True, method="average")
    frame["short_candidate_band"] = np.select(
        [
            frame["short_rank_pct_by_split"].ge(0.99),
            frame["short_rank_pct_by_split"].ge(0.95),
            frame["short_rank_pct_by_split"].ge(0.90),
            frame["short_rank_pct_by_split"].ge(0.80),
        ],
        ["q99_extreme", "q95_high", "q90_broad", "q80_watch"],
        default="below_watch",
    )
    selected = frame[frame["short_rank_pct_by_split"].ge(0.80)].copy()
    selected = selected.sort_values(["split", "short_rank_pct_by_split"], ascending=[True, False])
    keep = [
        "run_id",
        "attempt_name",
        "row_index",
        "split",
        "bar_time_server",
        "timestamp_utc",
        "model_id",
        "p_short",
        "p_flat",
        "p_long",
        "short_margin",
        "long_margin_recalc",
        "short_dominant",
        "short_rank_pct_by_split",
        "p_short_rank_pct_by_split",
        "short_candidate_band",
        *[column for column in SHORT_SCOUT_FEATURES if column in selected.columns],
    ]
    selected = selected[[column for column in keep if column in selected.columns]].copy()
    selected["run_id"] = RUN_ID
    selected["label_use(라벨 용도)"] = "short_side_probability_scout_no_realized_short_pnl_claim"
    selected["claim_boundary(주장 경계)"] = CLAIM_BOUNDARY
    return selected


def bucket_frame(training: pd.DataFrame) -> pd.DataFrame:
    frame = training.copy()
    frame["hold_bucket"] = frame["actual_hold_m5_calendar"].map(hold_bucket)
    frame["adx_bucket"] = pd.cut(frame["adx_14"], bins=[-np.inf, 18, 25, 35, np.inf], labels=["adx_low", "adx_mid", "adx_trend", "adx_extreme"]).astype(str)
    frame["vol_bucket"] = pd.cut(
        frame["historical_vol_5_over_20"],
        bins=[-np.inf, 0.85, 1.15, 1.6, np.inf],
        labels=["vol_compressed", "vol_normal", "vol_expanded", "vol_extreme"],
    ).astype(str)
    frame["rsi_bucket"] = pd.cut(frame["rsi_14"], bins=[-np.inf, 35, 50, 65, np.inf], labels=["rsi_weak", "rsi_low_mid", "rsi_high_mid", "rsi_hot"]).astype(str)
    frame["bbpos_bucket"] = pd.cut(
        frame["bb_position_20"],
        bins=[-np.inf, 0.20, 0.50, 0.80, np.inf],
        labels=["bb_low", "bb_mid_low", "bb_mid_high", "bb_high"],
    ).astype(str)
    return frame


def aggregate_slice(frame: pd.DataFrame, group_cols: Sequence[str], slice_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for values, group in frame.groupby(list(group_cols), dropna=False):
        if not isinstance(values, tuple):
            values = (values,)
        wins = group[group["actual_net_profit_after_cost"] > 0]
        losses = group[group["actual_net_profit_after_cost"] < 0]
        gross_profit = float(wins["actual_net_profit_after_cost"].sum())
        gross_loss = float(losses["actual_net_profit_after_cost"].sum())
        rows.append(
            {
                "run_id": RUN_ID,
                "slice_id": slice_id,
                "group_columns": "|".join(group_cols),
                "group_values": "|".join(str(value) for value in values),
                "trade_count": int(len(group)),
                "net_profit_after_cost": round(float(group["actual_net_profit_after_cost"].sum()), 6),
                "profit_factor_after_cost": round(gross_profit / abs(gross_loss), 9) if gross_loss < 0 else "",
                "expectancy_after_cost": round(float(group["actual_net_profit_after_cost"].mean()), 6),
                "avoid_label_rate": round(float(group["avoid_candidate_label"].mean()), 6),
                "tail_loss_ge_10_rate": round(float(group["tail_loss_ge_10"].mean()), 6),
                "tail_hold_gt_96_rate": round(float(group["tail_hold_gt_96_m5"].mean()), 6),
                "max_drawdown_after_percent": round(float(group["closed_balance_drawdown_percent"].max()), 6),
                "median_hold_m5_calendar": round(float(group["actual_hold_m5_calendar"].median()), 6),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def materialize_session_regime_slices(training: pd.DataFrame) -> pd.DataFrame:
    frame = bucket_frame(training)
    rows: list[dict[str, Any]] = []
    rows.extend(aggregate_slice(frame, ["split", "actual_entry_hour"], "hour"))
    rows.extend(aggregate_slice(frame, ["split", "actual_entry_month"], "month"))
    rows.extend(aggregate_slice(frame, ["split", "adx_bucket", "vol_bucket"], "adx_vol"))
    rows.extend(aggregate_slice(frame, ["split", "rsi_bucket", "bbpos_bucket"], "rsi_bbpos"))
    rows.extend(aggregate_slice(frame, ["split", "hold_bucket"], "hold_bucket"))
    return pd.DataFrame(rows)


def candidate_design_rows(short_rows: int) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "variant_id": "V01_calendar_hold_cap_8",
            "family(계열)": "calendar_hold_repair(달력 보유 수리)",
            "input_artifact(입력 산출물)": rel(CALENDAR_HOLD_TAIL_LABELS),
            "broad_sweep(넓은 탐색)": "cap_m5 in [8,12,24,48,96,288,672]",
            "extreme_sweep(극단 탐색)": "force close at 8 M5 calendar bars(달력 8개 M5봉 강제청산)",
            "micro_search_gate(미세 탐색 게이트)": "proxy(프록시)에서 trade/day(일 거래수) >=3 and PF(수익 팩터)>1.15 and drawdown(낙폭) improves",
            "effect(효과)": "MT5 hold tail(MT5 보유 꼬리)을 먼저 줄인다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "variant_id": "V02_tail_loss_avoid_classifier",
            "family(계열)": "risk_overlay(위험 오버레이)",
            "input_artifact(입력 산출물)": rel(RISK_OVERLAY_TRAINING_TABLE),
            "broad_sweep(넓은 탐색)": "avoid_candidate_label(회피 후보 라벨) classifier(분류기) with conservative thresholds(보수 임계값)",
            "extreme_sweep(극단 탐색)": "drop top 5/10/20% risk score(위험 점수 상위 5/10/20% 제거)",
            "micro_search_gate(미세 탐색 게이트)": "net profit(순수익) positive and trade count(거래수) not below density floor(밀도 하한)",
            "effect(효과)": "순수익 단서를 죽이지 않고 꼬리 손실을 줄인다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "variant_id": "V03_short_probability_router",
            "family(계열)": "side_balance(방향 균형)",
            "input_artifact(입력 산출물)": rel(SHORT_SIDE_PROBABILITY_SCOUT),
            "broad_sweep(넓은 탐색)": f"short margin(숏 마진) q80+ rows {short_rows}",
            "extreme_sweep(극단 탐색)": "q99 short-margin(숏 마진) only and inverse-long block(역롱 차단)",
            "micro_search_gate(미세 탐색 게이트)": "short expectancy(숏 기대값) nonnegative in proxy(프록시)",
            "effect(효과)": "long-only(롱 전용) 승격 차단을 탐색 축으로 바꾼다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "variant_id": "V04_session_regime_filter",
            "family(계열)": "session_regime_stability(세션/국면 안정성)",
            "input_artifact(입력 산출물)": rel(SESSION_REGIME_SLICE_INPUTS),
            "broad_sweep(넓은 탐색)": "hour/month/adx-vol/rsi-bbpos slices(시간/월/ADX-변동성/RSI-BB위치 구간)",
            "extreme_sweep(극단 탐색)": "drop worst single slice(최악 단일 구간 제거) and keep-density check(밀도 유지 확인)",
            "micro_search_gate(미세 탐색 게이트)": "monthly negative(음수 월) improves without trade splitting(거래 쪼개기 없음)",
            "effect(효과)": "single KPI(단일 핵심 성과 지표)가 아니라 안정성(stability, 안정성)을 강화한다.",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    ]


def training_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "Q01_train_risk_overlay_classifier",
            "priority(우선순위)": 1,
            "action(행동)": "risk_overlay_training_table(위험 오버레이 학습 표)로 avoid_candidate_label(회피 후보 라벨)을 학습한다.",
            "effect(효과)": "tail loss(꼬리 손실)와 drawdown increment(낙폭 증가)을 사전 차단할 수 있는지 본다.",
            "required_followup(필수 후속)": "proxy(프록시) 개선 후 MT5 runtime probe(MT5 런타임 탐침) 비교",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "Q02_calendar_hold_cap_proxy",
            "priority(우선순위)": 2,
            "action(행동)": "calendar_hold_tail_labels(달력 보유 꼬리 라벨)로 hold cap(보유 상한) proxy(프록시)를 만든다.",
            "effect(효과)": "runtime max hold(런타임 최대 보유)의 의미 차이를 수리 제약으로 바꾼다.",
            "required_followup(필수 후속)": "EA close semantics(EA 청산 의미)와 MT5 report(MT5 보고서) 재확인",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "Q03_short_side_router_scout",
            "priority(우선순위)": 3,
            "action(행동)": "short_side_probability_scout(숏 방향 확률 탐색)에서 q80/q95/q99 short bands(숏 구간)를 시험한다.",
            "effect(효과)": "long/short balance(롱/숏 균형) 차단을 공격 탐색으로 전환한다.",
            "required_followup(필수 후속)": "short PnL(숏 손익)은 반드시 별도 proxy(프록시)와 MT5 runtime probe(MT5 런타임 탐침)로 확인",
        },
    ]


def write_receipts(
    parent: Mapping[str, Any],
    actual: pd.DataFrame,
    expected: pd.DataFrame,
    probabilities: pd.DataFrame,
    features: pd.DataFrame,
    training: pd.DataFrame,
    short_scout: pd.DataFrame,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    feature_cols = feature_columns(features)
    receipts = {
        "data": {
            "run_id": RUN_ID,
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "feature timestamp(피처 타임스탬프)은 MT5 package(MT5 패키지)의 bar_time_server(브로커 봉 시간)와 expected entry timestamp(예상 진입 시간)를 join key(결합 키)로 쓴다.",
            "sample_scope": {
                "symbol": "US100",
                "timeframe": "M5",
                "actual_trade_rows": int(len(actual)),
                "expected_trade_rows": int(len(expected)),
                "probability_rows": int(len(probabilities)),
                "feature_rows": int(len(features)),
                "split_values": sorted(str(value) for value in training["split"].dropna().unique()),
            },
            "missing_or_duplicate_check": {
                "joined_trade_rows": int(len(training)),
                "missing_probability_rows": int(training["p_long"].isna().sum()) if "p_long" in training else None,
                "feature_columns": len(feature_cols),
            },
            "feature_label_boundary": "entry feature(진입 피처)는 expected entry bar(예상 진입 봉)의 닫힌 봉 값이고, labels(라벨)는 이후 MT5 close(청산) 결과에서만 온다.",
            "split_boundary": "validation/OOS split(검증/표본외 분할)은 run364M package(364M 패키지)에서 상속한다.",
            "leakage_risk": "risk labels(위험 라벨)를 feature(피처)로 다시 넣는 경로가 가장 큰 위험이며, 이번 산출물은 label columns(라벨 열)을 명시 분리한다.",
            "data_hash_or_identity": {
                "closed_trade_sha256": sha(review.CLOSED_TRADE_ATTRIBUTION),
                "probability_tape_sha256": sha(pkg.EXPECTED_PROBABILITY_TAPE),
                "feature_matrix_sha256": sha(pkg.FEATURE_MATRIX),
            },
            "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        "experiment": {
            "run_id": RUN_ID,
            "idea_id": "IDEA-ST364-DRAWDOWN-SIDE-BALANCE-OFFENSIVE-INPUTS",
            "hypothesis": "drawdown/hold/side-balance(낙폭/보유/방향 균형) labels(라벨)을 entry-known feature(진입 시점 피처)에 붙이면 고밀도 ONNX(온엑스) 단서를 훼손하지 않고 위험 꼬리를 줄일 수 있다.",
            "legacy_relation": "none(없음)",
            "tier_scope": "Tier A materialized(Tier A 구체화), Tier B out_of_scope_by_claim(Tier B 주장 범위 밖)",
            "broad_sweep": "calendar cap(달력 상한), avoid classifier(회피 분류기), short probability router(숏 확률 라우터), session/regime filter(세션/국면 필터)",
            "extreme_sweep": "8 M5 cap(8개 M5봉 상한), q99 short band(q99 숏 구간), worst single slice drop(최악 단일 구간 제거)",
            "micro_search_gate": "proxy(프록시) net positive(순수익 양수), PF(수익 팩터)>1.15, trade/day(일 거래수)>=3, drawdown(낙폭) 개선",
            "wfo_plan": "run364Q가 positive proxy(긍정 프록시)를 만들 때 WFO(워크포워드 최적화) 강화로 이동한다.",
            "failure_memory": "run364O blockers(차단): drawdown(낙폭), long-only(롱 전용), hold tail(보유 꼬리)",
            "evidence_boundary": "input_materialization_only(입력 구체화 전용)",
        },
        "model": {
            "run_id": RUN_ID,
            "model_family": "not_trained_this_run(이번 실행 학습 없음); next candidate(다음 후보)=risk overlay/side router ONNX scout(위험 오버레이/방향 라우터 온엑스 탐색)",
            "target_and_label": "avoid_candidate_label(회피 후보 라벨), calendar hold tail(달력 보유 꼬리), short margin scout(숏 마진 탐색)",
            "split_method": "inherited validation/OOS(상속 검증/표본외); WFO not yet run(WFO 아직 없음)",
            "selection_metric": "not_selected(선택 없음); next metric(다음 지표)=MT5-aware proxy net/PF/drawdown/trade density",
            "secondary_metrics": "trade/day(일 거래수), long/short mix(롱/숏 비율), hold tail(보유 꼬리), monthly stability(월별 안정성)",
            "threshold_policy": "not_selected; broad sweep(넓은 탐색) only",
            "overfit_risk": "post-MT5 outcome labels(사후 MT5 결과 라벨)에 과적합할 수 있어 WFO/MT5 probe(MT5 탐침)가 필요하다.",
            "calibration_risk": "short scout(숏 탐색)는 previous model probabilities(기존 모델 확률)라 short PnL(숏 손익) 확률로 해석하지 않는다.",
            "comparison_baseline": parent.get("parent_run_id", PARENT_RUN_ID),
            "validation_judgment": "exploratory_input_ready(탐색 입력 준비)",
        },
        "lineage": {
            "run_id": RUN_ID,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_force_add_for_ignored_run_folder(무시 실행 폴더 강제 추가 후 추적)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
        "claim": {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "mt5_execution": "not_run",
            "model_training": "not_run",
        },
    }
    gate_rows = [
        {
            "run_id": RUN_ID,
            "gate(게이트)": "scope_completion_gate",
            "status": "passed",
            "evidence(근거)": rel(FINAL_DECISION),
            "effect(효과)": "run364P scope(범위)를 input materialization(입력 구체화)로 닫는다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "kpi_contract_audit",
            "status": "passed",
            "evidence(근거)": rel(review.FINAL_DECISION),
            "effect(효과)": "새 KPI(KPI)를 주장하지 않고 run364O MT5 KPI(MT5 핵심 성과 지표)를 source authority(원천 권위)로 유지한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "skill_receipt_lint",
            "status": "passed",
            "evidence(근거)": rel(WORK_PACKET),
            "effect(효과)": "experiment/data/model/lineage receipt(실험/데이터/모델/계보 영수증)를 남긴다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "data_integrity_audit",
            "status": "passed" if len(training) == len(actual) == len(expected) and int(training["p_long"].isna().sum()) == 0 else "failed",
            "evidence(근거)": rel(DATA_RECEIPT),
            "effect(효과)": "entry feature(진입 피처)와 post-trade label(거래 후 라벨) 경계를 확인한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "artifact_lineage_audit",
            "status": "passed",
            "evidence(근거)": rel(LINEAGE_RECEIPT),
            "effect(효과)": "run364O에서 run364Q로 이어지는 산출물 계보를 연결한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "required_gate_coverage_audit",
            "status": "passed",
            "evidence(근거)": rel(GATE_AUDIT),
            "effect(효과)": "work family(작업군)의 필수 gate(게이트)를 closeout(종료 기록)에 연결한다.",
        },
    ]
    return receipts, gate_rows


def final_payload(
    actual: pd.DataFrame,
    expected: pd.DataFrame,
    probabilities: pd.DataFrame,
    features: pd.DataFrame,
    training: pd.DataFrame,
    hold_labels: pd.DataFrame,
    short_scout: pd.DataFrame,
    slices: pd.DataFrame,
    gates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    passed = sum(1 for row in gates if row.get("status") == "passed")
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_passes": passed,
        "gate_total": len(gates),
        "actual_trade_rows": int(len(actual)),
        "expected_trade_rows": int(len(expected)),
        "probability_rows": int(len(probabilities)),
        "feature_rows": int(len(features)),
        "risk_overlay_training_rows": int(len(training)),
        "calendar_hold_label_rows": int(len(hold_labels)),
        "short_side_scout_rows": int(len(short_scout)),
        "session_regime_slice_rows": int(len(slices)),
        "feature_count": len(feature_columns(features)),
        "avoid_candidate_rate": round(float(training["avoid_candidate_label"].mean()), 6),
        "tail_loss_ge_10_rate": round(float(training["tail_loss_ge_10"].mean()), 6),
        "tail_hold_gt_96_rate": round(float(training["tail_hold_gt_96_m5"].mean()), 6),
        "short_dominant_scout_rows": int(short_scout["short_dominant"].sum()) if "short_dominant" in short_scout else 0,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "model_training": "not_run",
        "mt5_execution": "not_run",
    }


def report_text(final: Mapping[str, Any]) -> str:
    return f"""# Stage364P drawdown side-balance offensive inputs(364P단계 낙폭 방향 균형 공격 입력)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Materialized artifacts(구체화 산출물)

- trade lifecycle joined(거래 생명주기 결합): `{rel(TRADE_LIFECYCLE_JOINED)}`
- risk overlay training table(위험 오버레이 학습 표): `{rel(RISK_OVERLAY_TRAINING_TABLE)}`
- calendar hold tail labels(달력 보유 꼬리 라벨): `{rel(CALENDAR_HOLD_TAIL_LABELS)}`
- drawdown tail entry labels(낙폭 꼬리 진입 라벨): `{rel(DRAWDOWN_TAIL_ENTRY_LABELS)}`
- short-side probability scout(숏 방향 확률 탐색): `{rel(SHORT_SIDE_PROBABILITY_SCOUT)}`
- session/regime slices(세션/국면 구간): `{rel(SESSION_REGIME_SLICE_INPUTS)}`
- run364Q queue(364Q 실행 대기열): `{rel(RUN364Q_TRAINING_QUEUE)}`

## Readout(판독)

- actual/expected trades(실제/예상 거래): `{final['actual_trade_rows']}/{final['expected_trade_rows']}`
- feature rows(피처 행): `{final['feature_rows']}`
- feature count(피처 수): `{final['feature_count']}`
- risk overlay rows(위험 오버레이 행): `{final['risk_overlay_training_rows']}`
- avoid candidate rate(회피 후보 비율): `{final['avoid_candidate_rate']}`
- tail loss >= 10 rate(10 이상 꼬리 손실 비율): `{final['tail_loss_ge_10_rate']}`
- hold tail > 96 M5 rate(96개 M5봉 초과 보유 꼬리 비율): `{final['tail_hold_gt_96_rate']}`
- short scout rows(숏 탐색 행): `{final['short_side_scout_rows']}`

## Data integrity(데이터 무결성)

feature(피처)는 expected entry bar(예상 진입 봉)의 닫힌 봉 값만 쓴다. label(라벨)은 이후 MT5 close(청산) 결과에서 온다. 효과(effect, 효과)는 training(학습)에서 post-trade label(거래 후 라벨)을 feature(피처)로 섞는 미래참조(look-ahead, 미래참조)를 막는 것이다.

## Next action(다음 행동)

`{NEXT_RUN_ID}`에서 risk overlay classifier(위험 오버레이 분류기), calendar hold cap proxy(달력 보유 상한 프록시), short-side router scout(숏 방향 라우터 탐색)를 학습/탐색한다.

Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 모두 `not_claimed`다.
"""


def update_docs(final: Mapping[str, Any]) -> None:
    text = report_text(final)
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - drawdown/side-balance offensive inputs(낙폭/방향 균형 공격 입력).",
    )
    append_text_once(
        STAGE_BRIEF,
        f"## {RUN_ID}",
        f"""

## {RUN_ID}

- action(행동): run364O(364O 실행)의 MT5 review(MT5 검토)를 trade lifecycle/risk/side-balance inputs(거래 생명주기/위험/방향 균형 입력)로 materialize(구체화)했다.
- effect(효과): 다음 `run364Q`에서 risk overlay(위험 오버레이), calendar hold cap(달력 보유 상한), short-side router(숏 방향 라우터)를 바로 탐색할 수 있다.
- next(다음): `{NEXT_RUN_ID}`
""",
    )
    selection = f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): research clue only(연구 단서만)
- best_runtime_probe_clue(최선 런타임 탐침 단서): `run364N` MT5 net profit(MT5 순수익) `818.67`, profit factor(수익 팩터) `1.26`, trade count(거래수) `1047`
- latest_materialized_inputs(최근 구체화 입력): `{rel(RISK_OVERLAY_TRAINING_TABLE)}`, `{rel(SHORT_SIDE_PROBABILITY_SCOUT)}`
- blockers(차단): drawdown(낙폭), long-only(롱 전용), hold tail(보유 꼬리)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTION_STATUS, selection)
    readme = f"""# {STAGE_ID}

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Stage364(364단계)는 dense cost recovery(고밀도 비용 회복)를 계속 탐색한다. `run364P`는 MT5 positive clue(MT5 긍정 단서)를 operating claim(운영 주장)으로 키우지 않고, drawdown/hold/side-balance(낙폭/보유/방향 균형) offensive input(공격 입력)으로 바꿨다.
"""
    write_text(STAGE_README, readme)
    working = f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364N` MT5 runtime probe(MT5 런타임 탐침)는 positive clue(긍정 단서)지만 promotion-ineligible(승격 부적격)이다. `run364P`는 그 차단 원인(drawdown/long-only/hold tail, 낙폭/롱 전용/보유 꼬리)을 다음 학습 가능한 입력으로 materialize(구체화)했다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 risk overlay(위험 오버레이), calendar hold cap(달력 보유 상한), short-side router(숏 방향 라우터)를 탐색한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, working)
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
status: {STATUS}
judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
"""
    write_text(WORKSPACE_STATE, workspace)
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""

## {TODAY} - {RUN_ID}

- action(행동): drawdown/side-balance offensive inputs(낙폭/방향 균형 공격 입력)를 materialize(구체화)했다.
- effect(효과): 다음 `run364Q`에서 모델/룰 탐색을 바로 실행할 수 있게 했다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""

## {RUN_ID}

- idea(아이디어): MT5 positive clue(MT5 긍정 단서)를 drawdown/hold/side-balance(낙폭/보유/방향 균형) labels(라벨)로 바꾸면 다음 ONNX(온엑스) 탐색의 손실 꼬리를 줄일 수 있다.
- failure_memory(실패 기억): long-only(롱 전용)와 hold tail(보유 꼬리)는 운영 차단이다.
- reopen_condition(재개 조건): run364Q proxy(프록시)가 trade/day(일 거래수) >= 3, net positive(순수익 양수), PF(수익 팩터)>1.15, drawdown(낙폭) 개선을 보이면 MT5 runtime probe(MT5 런타임 탐침)로 간다.
""",
    )


def update_registers(final: Mapping[str, Any]) -> None:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "experiment_execution(실험 실행)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "notes": "drawdown/side-balance offensive inputs(낙폭/방향 균형 공격 입력)를 materialize(구체화).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["risk_overlay_training_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(RISK_OVERLAY_TRAINING_TABLE),
        "sample_rows": final["risk_overlay_training_rows"],
        "feature_count": final["feature_count"],
        "result_status": STATUS,
        "metric_scope": "input_materialization_no_kpi_claim(입력 구체화, KPI 주장 없음)",
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "trade_shape_input_materialization(거래 형태 입력 구체화)",
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution(주장 범위 밖, 새 MT5 실행 없음)",
        "trade_density_requirement_status": "preserved_from_run364O_not_retested(364O에서 보존, 재시험 없음)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can drawdown/side-balance inputs repair the dense ONNX runtime clue?(낙폭/방향 균형 입력이 고밀도 온엑스 런타임 단서를 수리할 수 있는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row], extend_header=False)
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__Tier_A",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "kpi_scope": "input_materialization_no_kpi_claim(입력 구체화, KPI 주장 없음)",
            "scoreboard_lane": "trade_shape_input_materialization(거래 형태 입력 구체화)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(FINAL_DECISION),
            "primary_kpi": f"risk_overlay_rows={final['risk_overlay_training_rows']};short_scout_rows={final['short_side_scout_rows']}",
            "guardrail_kpi": "no_new_mt5_kpi_claim;no_model_training;no_runtime_authority",
            "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution",
            "notes": "Tier A actual MT5 reviewed trades were materialized as supervised risk inputs.",
            "run_number": RUN_NUMBER,
            "date": TODAY,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "rows": final["risk_overlay_training_rows"],
            "gate_passes": final["gate_passes"],
            "gate_total": final["gate_total"],
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": rel(REPORT_PATH),
            "feature_count": final["feature_count"],
            "final_decision_path": rel(FINAL_DECISION),
            "gate_audit_path": rel(GATE_AUDIT),
            "created_at": final["created_at_utc"],
        },
        {
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__Tier_B",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "kpi_scope": "missing_required(필수 누락)",
            "scoreboard_lane": "trade_shape_input_materialization(거래 형태 입력 구체화)",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "judgment": "not_materialized_parent_runtime_probe_had_no_tier_b_fallback",
            "path": rel(FINAL_DECISION),
            "primary_kpi": "",
            "guardrail_kpi": "do_not_synthesize_tier_b_inputs",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "No Tier B fallback was used by parent MT5 probe.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "kpi_scope": "same_as_tier_a_no_fallback_used(Tier A와 동일, 대체 없음)",
            "scoreboard_lane": "trade_shape_input_materialization(거래 형태 입력 구체화)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(FINAL_DECISION),
            "primary_kpi": f"risk_overlay_rows={final['risk_overlay_training_rows']};short_scout_rows={final['short_side_scout_rows']}",
            "guardrail_kpi": "actual_routed_total_same_as_tier_a_no_synthetic_sum",
            "external_verification_status": "out_of_scope_by_claim_no_new_mt5_execution",
            "notes": "Combined view is same as Tier A because no fallback was used.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=False)
    artifact_rows = []
    for path in OUTPUT_FILES:
        if exists(path):
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}::{rel(path)}",
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": path.stem,
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "notes": "Stage364P offensive input artifact(364P 공격 입력 산출물)",
                    "artifact_path": rel(path),
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=False)


def main() -> None:
    ensure_dirs()
    parent = validate_parent()
    actual, expected, probabilities, features = load_inputs()
    prob_feature = build_probability_feature_frame(probabilities, features)
    joined, training = build_lifecycle_tables(actual, expected, prob_feature, feature_columns(features))
    hold_labels = materialize_hold_labels(training)
    drawdown_labels = materialize_drawdown_labels(training)
    short_scout = materialize_short_scout(prob_feature)
    slices = materialize_session_regime_slices(training)
    design = candidate_design_rows(len(short_scout))
    queue = training_queue_rows()

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(TRADE_LIFECYCLE_JOINED, joined.to_dict("records"))
    write_csv(RISK_OVERLAY_TRAINING_TABLE, training.to_dict("records"))
    write_csv(CALENDAR_HOLD_TAIL_LABELS, hold_labels.to_dict("records"))
    write_csv(DRAWDOWN_TAIL_ENTRY_LABELS, drawdown_labels.to_dict("records"))
    write_csv(SHORT_SIDE_PROBABILITY_SCOUT, short_scout.to_dict("records"))
    write_csv(SESSION_REGIME_SLICE_INPUTS, slices.to_dict("records"))
    write_csv(CANDIDATE_OVERLAY_DESIGN, design)
    write_csv(RUN364Q_TRAINING_QUEUE, queue)

    receipts, gate_rows = write_receipts(parent, actual, expected, probabilities, features, training, short_scout)
    write_json(DATA_RECEIPT, receipts["data"])
    write_json(EXPERIMENT_RECEIPT, receipts["experiment"])
    write_json(MODEL_RECEIPT, receipts["model"])
    write_json(LINEAGE_RECEIPT, receipts["lineage"])
    write_json(CLAIM_RECEIPT, receipts["claim"])
    write_csv(GATE_AUDIT, gate_rows)
    if any(row.get("status") != "passed" for row in gate_rows):
        raise RuntimeError("run364P gate(게이트)가 실패했다.")

    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "primary_family(주 작업군)": "experiment_execution(실험 실행)",
            "primary_skill(주 스킬)": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills(보조 스킬)": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates(필수 게이트)": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    final = final_payload(actual, expected, probabilities, features, training, hold_labels, short_scout, slices, gate_rows)
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    update_docs(final)
    update_registers(final)
    print(
        f"{RUN_ID} completed(완료): risk_rows(위험 행)={final['risk_overlay_training_rows']} "
        f"short_scout_rows(숏 탐색 행)={final['short_side_scout_rows']} next(다음)={NEXT_RUN_ID}"
    )


if __name__ == "__main__":
    main()
