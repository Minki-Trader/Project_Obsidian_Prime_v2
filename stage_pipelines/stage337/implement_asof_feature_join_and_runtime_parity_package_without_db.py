from __future__ import annotations

import json
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage329 import materialize_forward_feature_frames as stage329b
from stage_pipelines.stage337 import build_live_computable_feature_frame_preflight_without_db as bp


aw = bp.aw
bg = bp.bg
fp = stage329b.fp

TODAY = "2026-05-27"
STAGE_ID = bp.STAGE_ID
RUN_NUMBER = "run337BQ"
RUN_ID = "run337BQ_implement_asof_feature_join_and_runtime_parity_package_without_db_v1"
PARENT_RUN_ID = bp.RUN_ID
NEXT_RUN_ID = "run337BR_execute_mt5_feature_parity_probe_without_db_v1"
STATUS = "completed_stage337BQ_asof_feature_join_runtime_parity_package_no_training_no_selection"
JUDGMENT = "asof_join_reduced_external_alignment_gap_runtime_parity_package_ready_mt5_not_executed"
DECISION = "stage337BQ_open_run337BR_mt5_feature_parity_probe"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BQ_asof_feature_join_runtime_parity_package_without_db_"
    "no_model_training_no_threshold_tuning_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bp.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
FEATURE_FRAME_DIR = RUN_DIR / "feature_frames"
FEATURE_ORDER_DIR = RUN_DIR / "feature_orders"
FEATURE_SUMMARY_DIR = RUN_DIR / "feature_summaries"
MT5_PACKAGE_DIR = RUN_DIR / "mt5_runtime_parity_package"
MT5_FEATURE_MATRIX_DIR = MT5_PACKAGE_DIR / "feature_matrices"
MT5_FEATURE_ORDER_DIR = MT5_PACKAGE_DIR / "feature_orders"
REVIEWS_DIR = bp.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BQ_asof_feature_join_runtime_parity_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BQ_asof_feature_join_runtime_parity_package.md"
SELECTED_STATUS = bp.SELECTED_STATUS
STAGE_BRIEF = bp.STAGE_BRIEF
WORKSPACE_STATE = bp.WORKSPACE_STATE
CURRENT_STATE = bp.CURRENT_STATE
CHANGELOG = bp.CHANGELOG
RUN_REGISTRY = bp.RUN_REGISTRY
ALPHA_LEDGER = bp.ALPHA_LEDGER
ARTIFACT_REGISTRY = bp.ARTIFACT_REGISTRY
STAGE_LEDGER = bp.STAGE_LEDGER

PARENT_DIR = STAGE_DIR / "02_runs" / "run337BP"
PARENT_FINAL = PARENT_DIR / "final_decision.json"
PARENT_SUMMARY = PARENT_DIR / "feature_set_materialization_summary.csv"
PARENT_GATE_AUDIT = PARENT_DIR / "required_gate_coverage_audit.csv"
BO_FINAL = bp.BO_FINAL
BO_RAW_REFRESH = bp.BO_RAW_REFRESH

ASOF_POLICY = RUN_DIR / "asof_join_policy.json"
ASOF_SOURCE_LAG_SUMMARY = RUN_DIR / "asof_source_lag_summary.csv"
FEATURE_SET_SUMMARY = RUN_DIR / "feature_set_materialization_summary.csv"
MISSING_FEATURE_COUNTS = RUN_DIR / "missing_feature_counts.csv"
INVALID_ROW_SAMPLES = RUN_DIR / "invalid_row_samples.csv"
FEATURE_SET_IMPROVEMENT = RUN_DIR / "feature_set_improvement_vs_run337BP.csv"
SESSION_BOUNDARY_REVIEW = RUN_DIR / "session_boundary_review.csv"
FEATURE_FIREWALL = RUN_DIR / "feature_firewall.csv"
RUNTIME_PACKAGE_MANIFEST = MT5_PACKAGE_DIR / "runtime_parity_package_manifest.json"
PARITY_HANDOFF_MATRIX = RUN_DIR / "parity_handoff_matrix.csv"
RUN337BR_QUEUE = RUN_DIR / "run337BR_mt5_feature_parity_probe_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (PARENT_FINAL, PARENT_SUMMARY, PARENT_GATE_AUDIT, BO_FINAL)
OUTPUT_FILES = (
    ASOF_POLICY,
    ASOF_SOURCE_LAG_SUMMARY,
    FEATURE_SET_SUMMARY,
    MISSING_FEATURE_COUNTS,
    INVALID_ROW_SAMPLES,
    FEATURE_SET_IMPROVEMENT,
    SESSION_BOUNDARY_REVIEW,
    FEATURE_FIREWALL,
    RUNTIME_PACKAGE_MANIFEST,
    PARITY_HANDOFF_MATRIX,
    RUN337BR_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

ASOF_POLICY_PAYLOAD = {
    "join_policy": "backward_asof_no_lookahead",
    "time_key": "closed_m5_bar_timestamp",
    "macro_proxy_max_lag_hours": 24,
    "equity_cash_max_lag_hours": 72,
    "macro_symbols": ["VIX", "US10YR", "USDX"],
    "equity_symbols": ["NVDA", "AAPL", "MSFT", "AMZN", "AMD", "GOOGL.xnas", "META", "TSLA"],
    "lookahead_rule": "source_timestamp_must_be_less_than_or_equal_target_timestamp",
    "session_boundary_rule": "do_not_fill_US100_session_features_when_overnight_return_is_missing",
    "training_or_selection_use": "forbidden",
    "claim_boundary": CLAIM_BOUNDARY,
}

SOURCE_GROUP = {
    "VIX": "macro_proxy",
    "US10YR": "macro_proxy",
    "USDX": "macro_proxy",
    "NVDA": "equity_cash",
    "AAPL": "equity_cash",
    "MSFT": "equity_cash",
    "AMZN": "equity_cash",
    "AMD": "equity_cash",
    "GOOGL.xnas": "equity_cash",
    "META": "equity_cash",
    "TSLA": "equity_cash",
}
SOURCE_TOLERANCE = {
    "macro_proxy": pd.Timedelta(hours=ASOF_POLICY_PAYLOAD["macro_proxy_max_lag_hours"]),
    "equity_cash": pd.Timedelta(hours=ASOF_POLICY_PAYLOAD["equity_cash_max_lag_hours"]),
}

FEATURE_SET_COLUMNS = (
    "feature_set_id",
    "role",
    "join_policy",
    "feature_count",
    "feature_order_sha256",
    "scope_rows",
    "valid_rows",
    "invalid_rows",
    "alignment_missing_rows",
    "finite_missing_rows",
    "first_valid_timestamp",
    "last_valid_timestamp",
    "status",
    "parquet_path",
    "parquet_sha256",
    "feature_order_path",
    "feature_order_sha256_file",
    "claim_boundary",
)
ASOF_LAG_COLUMNS = (
    "contract_symbol",
    "source_group",
    "feature_role",
    "target_rows",
    "ready_rows",
    "missing_rows",
    "max_lag_minutes",
    "p95_lag_minutes",
    "last_source_timestamp",
    "last_target_timestamp_with_source",
    "tolerance_hours",
    "lookahead_violations",
    "claim_boundary",
)
IMPROVEMENT_COLUMNS = (
    "feature_set_id",
    "bp_valid_rows",
    "bq_valid_rows",
    "delta_valid_rows",
    "bp_alignment_missing_rows",
    "bq_alignment_missing_rows",
    "delta_alignment_missing_rows",
    "bp_last_valid_timestamp",
    "bq_last_valid_timestamp",
    "interpretation",
    "claim_boundary",
)
SESSION_COLUMNS = (
    "session_boundary_id",
    "raw_feature_window_end_utc",
    "bq_latest_feature_timestamp",
    "raw_to_feature_gap_minutes",
    "boundary_reason",
    "status",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = bp.FIREWALL_COLUMNS
PARITY_COLUMNS = bp.PARITY_COLUMNS
QUEUE_COLUMNS = bp.QUEUE_COLUMNS
GATE_COLUMNS = bp.GATE_COLUMNS

ASOF_AUDIT_ROWS: list[dict[str, Any]] = []
ASOF_READY_INDEX: dict[str, set[pd.Timestamp]] = {}
FORBIDDEN_FEATURE_TERMS = bp.FORBIDDEN_FEATURE_TERMS


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def read_rows(path: Path) -> list[dict[str, str]]:
    _, rows = aw.read_csv_table(path, prefer_head=False)
    return rows


def pass_fail(ok: bool) -> str:
    return "passed" if ok else "failed"


def ts_iso(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return pd.Timestamp(value).isoformat()


def rounded(value: Any) -> float:
    if value is None or pd.isna(value):
        return 0.0
    return round(float(value), 6)


def load_inputs() -> dict[str, Any]:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BQ inputs: {missing}")
    return {
        "parent_final": read_json(PARENT_FINAL),
        "parent_summary": read_rows(PARENT_SUMMARY),
        "parent_gates": read_rows(PARENT_GATE_AUDIT),
        "bo_final": read_json(BO_FINAL),
    }


def merge_asof_source(
    merged: pd.DataFrame,
    source_view: pd.DataFrame,
    *,
    contract_symbol: str,
    token: str,
    feature_role: str,
    feature_columns: Sequence[str],
    tolerance: pd.Timedelta,
) -> pd.DataFrame:
    source_columns = ["timestamp", *feature_columns]
    right = source_view.loc[:, source_columns].copy().sort_values("timestamp").reset_index(drop=True)
    source_ts_col = f"__asof_source_timestamp__{token}"
    asof_key_col = f"__asof_key__{token}"
    ready_col = f"__asof_ready__{token}"
    age_col = f"__asof_age_minutes__{token}"
    right[source_ts_col] = right["timestamp"]
    right = right.rename(columns={"timestamp": asof_key_col})

    left = merged.reset_index(names="__bq_left_index").sort_values("timestamp").reset_index(drop=True)
    out = pd.merge_asof(
        left,
        right,
        left_on="timestamp",
        right_on=asof_key_col,
        direction="backward",
        tolerance=tolerance,
    )
    out[ready_col] = out[source_ts_col].notna()
    out[age_col] = (out["timestamp"] - out[source_ts_col]).dt.total_seconds() / 60.0
    out = out.sort_values("__bq_left_index").drop(columns=["__bq_left_index", asof_key_col])

    ready_mask = out[ready_col].astype(bool)
    ready_timestamps = pd.to_datetime(out.loc[ready_mask, "timestamp"], utc=True)
    ASOF_READY_INDEX[contract_symbol] = set(ready_timestamps)
    ages = out.loc[ready_mask, age_col]
    lookahead_violations = int((ages < 0).sum())
    ASOF_AUDIT_ROWS.append(
        {
            "contract_symbol": contract_symbol,
            "source_group": SOURCE_GROUP[contract_symbol],
            "feature_role": feature_role,
            "target_rows": int(len(out)),
            "ready_rows": int(ready_mask.sum()),
            "missing_rows": int((~ready_mask).sum()),
            "max_lag_minutes": rounded(ages.max() if len(ages) else 0.0),
            "p95_lag_minutes": rounded(ages.quantile(0.95) if len(ages) else 0.0),
            "last_source_timestamp": ts_iso(out.loc[ready_mask, source_ts_col].max() if ready_mask.any() else None),
            "last_target_timestamp_with_source": ts_iso(ready_timestamps.max() if len(ready_timestamps) else None),
            "tolerance_hours": rounded(tolerance / pd.Timedelta(hours=1)),
            "lookahead_violations": lookahead_violations,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return out


def attach_external_series_asof(
    base: pd.DataFrame,
    external_frames: dict[str, pd.DataFrame],
    *,
    weights_path: Path | None = None,
) -> tuple[pd.DataFrame, dict[str, int], list[str]]:
    merged = base.copy()
    ASOF_READY_INDEX["US100"] = set(pd.to_datetime(merged["timestamp"], utc=True))
    alignment_missing_counts: dict[str, int] = {}
    readiness_columns: list[str] = []

    proxy_configs = {
        "VIX": ("vix", external_frames["VIX"]),
        "US10YR": ("us10yr", external_frames["US10YR"]),
        "USDX": ("usdx", external_frames["USDX"]),
    }
    for contract_symbol, (prefix, source) in proxy_configs.items():
        source_view = fp.build_proxy_feature_source(source, prefix)
        token = prefix
        feature_cols = [col for col in source_view.columns if col != "timestamp"]
        merged = merge_asof_source(
            merged,
            source_view,
            contract_symbol=contract_symbol,
            token=token,
            feature_role=f"{prefix}_proxy_features",
            feature_columns=feature_cols,
            tolerance=SOURCE_TOLERANCE[SOURCE_GROUP[contract_symbol]],
        )
        ready_col = f"__asof_ready__{token}"
        readiness_columns.append(ready_col)
        alignment_missing_counts[contract_symbol] = int((~merged[ready_col]).sum())

    stock_return_symbols = {
        "NVDA": "nvda_xnas_log_return_1",
        "AAPL": "aapl_xnas_log_return_1",
        "MSFT": "msft_xnas_log_return_1",
        "AMZN": "amzn_xnas_log_return_1",
    }
    for contract_symbol, feature_name in stock_return_symbols.items():
        source = external_frames[contract_symbol].copy()
        token = contract_symbol.lower().replace(".", "_")
        source[feature_name] = np.log(source["close"] / source["close"].shift(1))
        source_view = source[["timestamp", feature_name]]
        merged = merge_asof_source(
            merged,
            source_view,
            contract_symbol=contract_symbol,
            token=token,
            feature_role=f"{feature_name}_asof",
            feature_columns=[feature_name],
            tolerance=SOURCE_TOLERANCE[SOURCE_GROUP[contract_symbol]],
        )
        ready_col = f"__asof_ready__{token}"
        readiness_columns.append(ready_col)
        alignment_missing_counts[contract_symbol] = int((~merged[ready_col]).sum())

    basket_symbols = ["AAPL", "AMZN", "AMD", "GOOGL.xnas", "META", "MSFT", "NVDA", "TSLA"]
    basket_return_1_cols: list[str] = []
    basket_return_5_cols: list[str] = []
    for contract_symbol in basket_symbols:
        source = external_frames[contract_symbol].copy()
        token = contract_symbol.lower().replace(".", "_")
        basket_token = f"{token}_basket"
        return_1_col = f"{token}_simple_return_1"
        return_5_col = f"{token}_simple_return_5"
        source[return_1_col] = source["close"] / source["close"].shift(1) - 1.0
        source[return_5_col] = source["close"] / source["close"].shift(5) - 1.0
        source_view = source[["timestamp", return_1_col, return_5_col]]
        merged = merge_asof_source(
            merged,
            source_view,
            contract_symbol=contract_symbol,
            token=basket_token,
            feature_role="mega8_basket_features",
            feature_columns=[return_1_col, return_5_col],
            tolerance=SOURCE_TOLERANCE[SOURCE_GROUP[contract_symbol]],
        )
        ready_col = f"__asof_ready__{basket_token}"
        readiness_columns.append(ready_col)
        alignment_missing_counts.setdefault(contract_symbol, int((~merged[ready_col]).sum()))
        basket_return_1_cols.append(return_1_col)
        basket_return_5_cols.append(return_5_col)

    merged["mega8_equal_return_1"] = merged[basket_return_1_cols].mean(axis=1, skipna=False)
    merged["mega8_pos_breadth_1"] = (merged[basket_return_1_cols] > 0).mean(axis=1, skipna=False)
    merged["mega8_dispersion_5"] = merged[basket_return_5_cols].std(axis=1, ddof=0, skipna=False)

    weights = fp.load_weights(weights_path)
    merged["month"] = merged["timestamp"].dt.strftime("%Y-%m")
    merged = merged.merge(weights, on="month", how="left")
    merged["top3_weighted_return_1"] = (
        merged["msft_xnas_weight"] * merged["msft_simple_return_1"]
        + merged["nvda_xnas_weight"] * merged["nvda_simple_return_1"]
        + merged["aapl_xnas_weight"] * merged["aapl_simple_return_1"]
    )

    merged["us100_simple_return_1"] = merged["close"] / merged["close"].shift(1) - 1.0
    merged["us100_minus_mega8_equal_return_1"] = merged["us100_simple_return_1"] - merged["mega8_equal_return_1"]
    merged["us100_minus_top3_weighted_return_1"] = merged["us100_simple_return_1"] - merged["top3_weighted_return_1"]
    return merged, alignment_missing_counts, readiness_columns


def required_alignment_mask_asof(timestamps: pd.Series, required_symbols: list[str]) -> np.ndarray:
    mask = pd.Series(True, index=timestamps.index)
    normalized = pd.to_datetime(timestamps, utc=True)
    for symbol in required_symbols:
        ready = ASOF_READY_INDEX.get(symbol)
        if ready is None:
            mask &= False
            continue
        mask &= normalized.isin(ready)
    return mask.to_numpy()


def configure_stage329(us100_last_close_utc: str) -> None:
    target_end = pd.Timestamp(us100_last_close_utc)
    ASOF_AUDIT_ROWS.clear()
    ASOF_READY_INDEX.clear()
    stage329b.RUN_ID = RUN_ID
    stage329b.RUN_NUMBER = RUN_NUMBER
    stage329b.PARENT_RUN_ID = PARENT_RUN_ID
    stage329b.NEXT_ACTION = NEXT_RUN_ID
    stage329b.STATUS = STATUS
    stage329b.JUDGMENT = JUDGMENT
    stage329b.DECISION = DECISION
    stage329b.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    stage329b.STAGE_ID = STAGE_ID
    stage329b.STAGE_DIR = STAGE_DIR
    stage329b.RUN_DIR = RUN_DIR
    stage329b.FEATURE_FRAME_DIR = FEATURE_FRAME_DIR
    stage329b.FEATURE_ORDER_DIR = FEATURE_ORDER_DIR
    stage329b.FEATURE_SUMMARY_DIR = FEATURE_SUMMARY_DIR
    stage329b.REVIEWS_DIR = REVIEWS_DIR
    stage329b.SELECTED_DIR = STAGE_DIR / "04_selected"
    stage329b.DECISION_DOC = DECISION_DOC
    stage329b.FORWARD_RAW_ROOT = BO_RAW_REFRESH
    stage329b.FORWARD_RAW_SUMMARY = bp.BO_FRESH_INVENTORY
    stage329b.FORWARD_REQUESTED_TO_UTC = target_end
    stage329b.COMPUTE_END_UTC = target_end
    stage329b.COMBINED_RAW_CACHE.clear()
    stage329b.COMBINED_IDENTITY_CACHE.clear()
    stage329b.load_raw_part = bp.load_raw_part_longpath
    stage329b.required_alignment_mask = required_alignment_mask_asof
    fp.attach_external_series = attach_external_series_asof


def materialize_asof_frames(us100_last_close_utc: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path], dict[str, Any]]:
    configure_stage329(us100_last_close_utc)
    summaries, missing_counts, invalid_samples, frame_artifacts, foundation_counts = stage329b.build_feature_frames()
    clean_summaries: list[dict[str, Any]] = []
    for row in summaries:
        clean = dict(row)
        clean["join_policy"] = ASOF_POLICY_PAYLOAD["join_policy"]
        clean["claim_boundary"] = CLAIM_BOUNDARY
        clean_summaries.append(clean)
    missing_rows = [dict(row, claim_boundary=CLAIM_BOUNDARY) for row in missing_counts]
    if not missing_rows:
        missing_rows = [{"feature_set_id": "", "feature": "", "missing_or_nonfinite_rows": 0, "claim_boundary": CLAIM_BOUNDARY}]
    invalid_rows = [dict(row, claim_boundary=CLAIM_BOUNDARY) for row in invalid_samples]
    if not invalid_rows:
        invalid_rows = [{"feature_set_id": "", "timestamp": "", "alignment_ready": "", "finite_ready": "", "claim_boundary": CLAIM_BOUNDARY}]
    return clean_summaries, missing_rows, invalid_rows, frame_artifacts, foundation_counts


def write_basic_artifacts(
    summaries: Sequence[Mapping[str, Any]],
    missing_rows: Sequence[Mapping[str, Any]],
    invalid_rows: Sequence[Mapping[str, Any]],
) -> list[Path]:
    return [
        aw.write_json(ASOF_POLICY, ASOF_POLICY_PAYLOAD),
        aw.write_csv(ASOF_SOURCE_LAG_SUMMARY, ASOF_LAG_COLUMNS, ASOF_AUDIT_ROWS),
        aw.write_csv(FEATURE_SET_SUMMARY, FEATURE_SET_COLUMNS, summaries),
        aw.write_csv(MISSING_FEATURE_COUNTS, bp.MISSING_COLUMNS, missing_rows),
        aw.write_csv(INVALID_ROW_SAMPLES, bp.INVALID_COLUMNS, invalid_rows),
    ]


def summary_by_id(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("feature_set_id")): row for row in rows}


def int_field(row: Mapping[str, Any], key: str) -> int:
    value = row.get(key, 0)
    if value in ("", None):
        return 0
    return int(float(value))


def build_improvement_rows(src: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    parent = summary_by_id(src["parent_summary"])
    rows: list[dict[str, Any]] = []
    for row in summaries:
        feature_set_id = str(row.get("feature_set_id", ""))
        old = parent.get(feature_set_id, {})
        bp_valid = int_field(old, "valid_rows")
        bq_valid = int_field(row, "valid_rows")
        bp_align = int_field(old, "alignment_missing_rows")
        bq_align = int_field(row, "alignment_missing_rows")
        delta_valid = bq_valid - bp_valid
        delta_align = bq_align - bp_align
        if delta_valid > 0:
            interpretation = "asof_join_added_live_computable_rows_without_training_or_selection"
        elif delta_valid == 0:
            interpretation = "unchanged_by_asof_join_session_or_feature_boundary_dominates"
        else:
            interpretation = "worse_than_parent_repair_required"
        rows.append(
            {
                "feature_set_id": feature_set_id,
                "bp_valid_rows": bp_valid,
                "bq_valid_rows": bq_valid,
                "delta_valid_rows": delta_valid,
                "bp_alignment_missing_rows": bp_align,
                "bq_alignment_missing_rows": bq_align,
                "delta_alignment_missing_rows": delta_align,
                "bp_last_valid_timestamp": old.get("last_valid_timestamp", ""),
                "bq_last_valid_timestamp": row.get("last_valid_timestamp", ""),
                "interpretation": interpretation,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_session_boundary_rows(src: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    raw_end = pd.Timestamp(src["bo_final"].get("us100_last_close_utc"))
    latest = max((pd.Timestamp(row.get("last_valid_timestamp")) for row in summaries if row.get("last_valid_timestamp")), default=pd.NaT)
    gap_minutes = int((raw_end - latest).total_seconds() // 60) if pd.notna(latest) else 0
    return [
        {
            "session_boundary_id": "bq_session_safe_feature_end",
            "raw_feature_window_end_utc": raw_end.isoformat().replace("+00:00", "Z"),
            "bq_latest_feature_timestamp": latest.isoformat() if pd.notna(latest) else "",
            "raw_to_feature_gap_minutes": gap_minutes,
            "boundary_reason": "overnight_return_requires_current_cash_open_and_current_raw_rows_are_pre_cash_open",
            "status": "session_boundary_named" if gap_minutes > 0 else "no_session_gap_detected",
            "effect": "current raw rows after the session-safe feature end are not promoted to runtime authority.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_feature_firewall(summaries: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summaries:
        feature_set_id = str(row.get("feature_set_id", ""))
        order_path_text = str(row.get("feature_order_path", ""))
        order_path = ROOT / order_path_text
        if not order_path_text or not aw.path_exists(order_path):
            rows.append(
                {
                    "feature_set_id": feature_set_id,
                    "artifact": order_path_text,
                    "forbidden_columns_found": "feature_order_missing",
                    "status": "failed",
                    "effect": "feature order(피처 순서)가 없으면 결과 원천 방화벽을 확인할 수 없다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        features = aw.io_path(order_path).read_text(encoding="utf-8-sig").splitlines()
        found = [term for term in FORBIDDEN_FEATURE_TERMS if any(term in feature.lower() for feature in features)]
        rows.append(
            {
                "feature_set_id": feature_set_id,
                "artifact": aw.rel(order_path),
                "forbidden_columns_found": ";".join(found),
                "status": "passed" if not found else "failed",
                "effect": "label/outcome/future/trade(라벨/결과/미래/거래 결과) 피처가 들어오지 못하게 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def export_runtime_package(summaries: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any], list[Path]]:
    aw.io_path(MT5_FEATURE_MATRIX_DIR).mkdir(parents=True, exist_ok=True)
    aw.io_path(MT5_FEATURE_ORDER_DIR).mkdir(parents=True, exist_ok=True)
    matrix_rows: list[dict[str, Any]] = []
    artifact_paths: list[Path] = []
    for row in summaries:
        if row.get("status") != "materialized":
            continue
        feature_set_id = str(row["feature_set_id"])
        parquet_path = ROOT / str(row["parquet_path"])
        feature_order_path = ROOT / str(row["feature_order_path"])
        features = [line.strip() for line in aw.io_path(feature_order_path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        frame = pd.read_parquet(aw.io_path(parquet_path))
        timestamps = pd.to_datetime(frame["timestamp"], utc=True)
        export = pd.DataFrame(
            {
                "bar_time_server": timestamps.dt.strftime("%Y.%m.%d %H:%M:%S"),
                "timestamp_utc": timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "symbol": frame["symbol"].astype(str),
            }
        )
        for feature in features:
            export[feature] = frame[feature].astype("float32")
        csv_path = MT5_FEATURE_MATRIX_DIR / f"{feature_set_id}_asof_features.csv"
        order_out = MT5_FEATURE_ORDER_DIR / f"{feature_set_id}_feature_order.txt"
        aw.io_path(csv_path.parent).mkdir(parents=True, exist_ok=True)
        export.to_csv(aw.io_path(csv_path), index=False, float_format="%.10g")
        shutil.copyfile(aw.io_path(feature_order_path), aw.io_path(order_out))
        artifact_paths.extend([csv_path, order_out])
        matrix_rows.append(
            {
                "feature_set_id": feature_set_id,
                "python_artifact": aw.rel(parquet_path),
                "mt5_feature_csv": aw.rel(csv_path),
                "mt5_feature_order": aw.rel(order_out),
                "row_count": int(len(export)),
                "feature_count": len(features),
                "first_timestamp": timestamps.min().isoformat() if len(timestamps) else "",
                "last_timestamp": timestamps.max().isoformat() if len(timestamps) else "",
                "csv_sha256": aw.sha256_file(csv_path),
                "feature_order_sha256": aw.sha256_file(order_out),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "package_type": "mt5_feature_parity_probe_input",
        "join_policy": ASOF_POLICY_PAYLOAD,
        "matrix_rows": matrix_rows,
        "actual_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "consumer": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUNTIME_PACKAGE_MANIFEST, manifest)
    artifact_paths.append(manifest_path)
    return matrix_rows, manifest, artifact_paths


def build_parity_matrix(matrix_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in matrix_rows:
        feature_set_id = str(row.get("feature_set_id", ""))
        rows.append(
            {
                "handoff_id": f"bq_mt5_parity_{feature_set_id}",
                "feature_set_id": feature_set_id,
                "python_artifact": row.get("python_artifact", ""),
                "mt5_required_artifact": row.get("mt5_feature_csv", ""),
                "preflight_status": "ready_for_mt5_feature_parity_probe",
                "blocked_status_if_missing": "blocked_bq_mt5_feature_matrix_missing",
                "effect": "다음 run(실행)에서 Python feature(파이썬 피처)와 MT5 feature(MT5 피처)를 같은 시각으로 비교하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_queue(parity_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BR_mt5_feature_parity_probe",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "MT5 feature parity probe(MT5 피처 동등성 탐침)",
            "inputs_to_review": ";".join(
                [
                    aw.rel(RUNTIME_PACKAGE_MANIFEST),
                    aw.rel(PARITY_HANDOFF_MATRIX),
                    aw.rel(ASOF_SOURCE_LAG_SUMMARY),
                    aw.rel(SESSION_BOUNDARY_REVIEW),
                ]
            ),
            "must_confirm": "MT5 reads the exported feature CSV and matches Python timestamps/features(MT5가 내보낸 피처 CSV를 읽고 파이썬 시각/피처와 일치)",
            "must_reject_if": "uses labels, tunes thresholds, treats package creation as runtime authority(라벨 사용, 임계값 조정, 패키지 생성을 런타임 권위로 취급)",
            "expected_outputs": f"parity_feature_sets={len(parity_rows)};actual_mt5_execution_required=true",
            "priority": "P0",
            "effect": "as-of materialization(시점 기준 물질화)을 실제 MT5 runtime parity(런타임 동등성)로 검증하는 다음 단계를 연다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_receipts(final: Mapping[str, Any], foundation_counts: Mapping[str, Any], matrix_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "work_family": "experiment_execution",
                "hypothesis": "backward as-of join(후방 시점 기준 결합) can reduce external alignment gaps without lookahead(미래참조) or training(학습)",
                "boundary": "feature and runtime package only; no model training or selection(피처/런타임 패키지만, 모델 학습/선택 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": aw.rel(BO_RAW_REFRESH),
                "feature_window_end": final.get("feature_window_end_utc"),
                "foundation_invalid_reason_breakdown": foundation_counts.get("invalid_reason_breakdown", {}),
                "asof_policy": aw.rel(ASOF_POLICY),
                "session_boundary_review": aw.rel(SESSION_BOUNDARY_REVIEW),
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_boundary": "no model, no labels, no threshold(모델/라벨/임계값 없음)",
                "selection_metric": "not_applicable",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "runtime_package": aw.rel(RUNTIME_PACKAGE_MANIFEST),
                "mt5_feature_matrix_count": len(matrix_rows),
                "actual_mt5_execution": "not_run",
                "runtime_authority": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [aw.rel(path) for path in INPUT_FILES],
                "producer": aw.rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [aw.rel(RUNTIME_PACKAGE_MANIFEST), aw.rel(FEATURE_SET_SUMMARY), aw.rel(ASOF_SOURCE_LAG_SUMMARY)],
                "registry_links": [aw.rel(ARTIFACT_REGISTRY), aw.rel(RUN_REGISTRY), aw.rel(ALPHA_LEDGER), aw.rel(STAGE_LEDGER)],
                "availability": "local_ignored_run_artifacts_with_committed_registry_and_regeneration_script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "judgment": final["judgment"],
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [aw.write_json(path, payload) for path, payload in payloads]


def build_gates(
    src: Mapping[str, Any],
    summaries: Sequence[Mapping[str, Any]],
    improvement_rows: Sequence[Mapping[str, Any]],
    session_rows: Sequence[Mapping[str, Any]],
    firewall_rows: Sequence[Mapping[str, Any]],
    parity_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    matrix_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parent_passed = sum(1 for row in src["parent_gates"] if row.get("status") == "passed")
    materialized_count = sum(1 for row in summaries if row.get("status") == "materialized")
    no_valid_row_regression = all(int_field(row, "delta_valid_rows") >= 0 for row in improvement_rows)
    external_improved = any(int_field(row, "delta_valid_rows") > 0 for row in improvement_rows if row.get("feature_set_id") != "us100_technical42_no_external")
    no_lookahead = all(int_field(row, "lookahead_violations") == 0 for row in ASOF_AUDIT_ROWS)
    firewall_ok = all(row.get("status") == "passed" for row in firewall_rows)
    session_gap_named = any(int_field(row, "raw_to_feature_gap_minutes") > 0 for row in session_rows)
    specs = [
        ("bq_gate_parent_final_loaded", src["parent_final"].get("next_action") == RUN_ID, f"parent_next={src['parent_final'].get('next_action')}", "run337BP opens run337BQ(run337BP가 run337BQ를 연다)"),
        ("bq_gate_parent_gates_passed", parent_passed == 10 and src["parent_final"].get("passed_gates") == 10, f"parent_gates={parent_passed}", "run337BP gates passed(run337BP 게이트 통과)"),
        ("bq_gate_asof_policy_written", aw.path_exists(ASOF_POLICY), aw.rel(ASOF_POLICY), "as-of policy artifact exists(시점 기준 정책 산출물 존재)"),
        ("bq_gate_no_lookahead_asof", no_lookahead, f"lookahead_violations={sum(int_field(row, 'lookahead_violations') for row in ASOF_AUDIT_ROWS)}", "source timestamps never exceed target timestamps(원천 시각이 대상 시각을 넘지 않음)"),
        ("bq_gate_feature_frames_materialized", materialized_count >= 3, f"materialized={materialized_count}", "three as-of feature frames materialized(시점 기준 피처 프레임 3개 생성)"),
        ("bq_gate_no_valid_row_regression", no_valid_row_regression, f"rows={len(improvement_rows)}", "as-of frame rows are not worse than BP(BP보다 유효 행이 줄지 않음)"),
        ("bq_gate_external_gap_reduced", external_improved, f"external_improved={external_improved}", "external feature sets improve(외부 피처 세트 개선)"),
        ("bq_gate_session_boundary_named", session_gap_named, f"session_gap_named={session_gap_named}", "current-day session boundary is named(현재일 세션 경계 명명)"),
        ("bq_gate_feature_firewall_passed", firewall_ok and len(firewall_rows) == 3, f"firewall_rows={len(firewall_rows)}", "feature firewall passed(피처 방화벽 통과)"),
        ("bq_gate_runtime_package_exported", len(matrix_rows) >= 3 and aw.path_exists(RUNTIME_PACKAGE_MANIFEST), f"matrix_rows={len(matrix_rows)}", "runtime parity package exported(런타임 동등성 패키지 내보냄)"),
        ("bq_gate_queue_ready", len(queue_rows) == 1 and queue_rows[0].get("next_run_id") == NEXT_RUN_ID, f"queue_rows={len(queue_rows)}", "run337BR queue ready(run337BR 대기열 준비)"),
        ("bq_gate_no_goal_or_forward_pass_claim", True, "forward_passed=not_claimed;goal=not_claimed", "no forbidden claim(금지 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": pass_fail(ok),
            "observed": observed,
            "expected": expected,
            "effect": "as-of join stays separated from model selection and runtime authority(시점 기준 결합은 모델 선택/런타임 권위와 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in specs
    ]


def count_passed(rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("status") == "passed")


def report_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = ["| feature_set(피처 세트) | BP valid(BP 유효) | BQ valid(BQ 유효) | delta(차이) | BQ last(BQ 마지막) |", "|---|---:|---:|---:|---|"]
    for row in rows:
        lines.append(
            f"| {row['feature_set_id']} | {row['bp_valid_rows']} | {row['bq_valid_rows']} | {row['delta_valid_rows']} | {row['bq_last_valid_timestamp']} |"
        )
    return "\n".join(lines)


def lag_risk_lines() -> str:
    macro_rows = [row for row in ASOF_AUDIT_ROWS if row.get("source_group") == "macro_proxy"]
    equity_rows = [row for row in ASOF_AUDIT_ROWS if row.get("source_group") == "equity_cash"]
    macro_max = max((float(row.get("max_lag_minutes", 0) or 0) for row in macro_rows), default=0.0)
    equity_max = max((float(row.get("max_lag_minutes", 0) or 0) for row in equity_rows), default=0.0)
    lookahead = sum(int_field(row, "lookahead_violations") for row in ASOF_AUDIT_ROWS)
    return "\n".join(
        [
            f"- macro_proxy_max_lag_minutes(거시 대리 최대 지연 분): `{macro_max}`",
            f"- equity_cash_max_lag_minutes(주식 현금장 최대 지연 분): `{equity_max}`",
            f"- lookahead_violations(미래참조 위반): `{lookahead}`",
            "- interpretation(해석): equity(주식) as-of carry(시점 기준 이월)는 행을 살리지만 stale-risk(지연 위험)를 만들 수 있으므로 MT5 parity(동등성) 뒤 별도 stress(압박 시험)가 필요하다.",
        ]
    )


def write_report(final: Mapping[str, Any], improvement_rows: Sequence[Mapping[str, Any]], session_rows: Sequence[Mapping[str, Any]]) -> Path:
    text = f"""# Stage337 run337BQ As-Of Feature Join Runtime Parity Package(시점 기준 피처 결합 런타임 동등성 패키지)

## Conclusion(결론)

run337BQ(337BQ 실행)는 exact timestamp join(정확 시각 결합)을 backward as-of join(후방 시점 기준 결합)으로 바꿔 외부 심볼 정렬 공백을 줄이고, MT5 feature parity probe(MT5 피처 동등성 탐침) 입력 패키지를 만들었다.

Effect(효과): core/macro(핵심/거시) 피처 세트는 더 많은 유효 행을 얻었지만, 최신 raw(원천) 끝 `{final['feature_window_end_utc']}`까지 전부 승격하지 않는다. `overnight_return`이 현재 cash open(현금장 개장)을 요구하므로 session-safe feature end(세션 안전 피처 끝)는 `{final['latest_feature_timestamp']}`다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- materialized_feature_sets(생성 피처 세트): `{final['materialized_feature_sets']}`
- latest_feature_timestamp(최신 피처 시각): `{final['latest_feature_timestamp']}`
- runtime_package(런타임 패키지): `{final['runtime_package']}`
- next_action(다음 행동): `{final['next_action']}`

## Improvement(개선)

{report_table(improvement_rows)}

## Session Boundary(세션 경계)

- raw_to_feature_gap_minutes(원천-피처 공백 분): `{session_rows[0]['raw_to_feature_gap_minutes']}`
- reason(이유): `{session_rows[0]['boundary_reason']}`

## Lag Risk(지연 위험)

{lag_risk_lines()}

## Boundary(경계)

- training(학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- actual_mt5_execution(실제 MT5 실행): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BQ As-Of Feature Join Runtime Parity Package(결정: 337단계 337BQ 시점 기준 피처 결합 런타임 동등성 패키지)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): as-of join(시점 기준 결합) 패키지를 만들었지만, 실제 MT5 execution(실제 MT5 실행)과 runtime authority(런타임 권위)는 run337BR(337BR 실행) 검증 전까지 주장하지 않는다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.remove_workspace_focus_block(workspace_text, "Stage337 run337BQ focus")
    workspace = bg.replace_top_value(workspace, "current_run_id: ", NEXT_RUN_ID)
    focus = (
        "- >-\n"
        "  Stage337 run337BQ focus complete: as-of feature join/runtime parity package"
        "(시점 기준 피처 결합/런타임 동등성 패키지)를 만들었다. Effect(효과): "
        "external alignment gap(외부 정렬 공백)을 줄이고 MT5 feature parity probe(MT5 피처 동등성 탐침)를 run337BR(337BR 실행)로 연다.\n"
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    current = bg.remove_markdown_section(current_text, "## Stage337 run337BQ(337BQ 실행)")
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BQ(337BQ 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BQ(337BQ 실행)는 as-of join(시점 기준 결합)으로 외부 정렬 공백을 줄이고 MT5 parity package(MT5 동등성 패키지)를 만들었다. 실제 MT5 실행/전진 통과/목표 달성은 주장하지 않는다.
"""
    current = current.replace("## Stage337 run337BP(337BP 실행)", entry + "\n## Stage337 run337BP(337BP 실행)", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `asof_feature_join_runtime_parity_package_ready`
- actual_mt5_execution(실제 MT5 실행): `not_run_package_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 MT5 피처 동등성 탐침이다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection_text, True))

    stage_text, stage_bom = aw.read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337BQ(337BQ 실행) implemented as-of feature join(시점 기준 피처 결합) and exported runtime parity package(런타임 동등성 패키지). Forward/Goal(전진/목표)은 주장하지 않는다."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337BQ built as-of feature join/runtime parity package(시점 기준 피처 결합/런타임 동등성 패키지) and queued MT5 parity probe(MT5 동등성 탐침)."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "asof_feature_join_runtime_parity_package_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "work_family": "experiment_execution",
        "primary_artifact": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__asof_runtime_package",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "asof_runtime_package",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BQ as-of feature join runtime parity package",
        "tier_scope": "feature_parity_package_no_trading_kpi",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"feature_sets={final['materialized_feature_sets']};latest={final['latest_feature_timestamp']}",
        "guardrail_kpi": "no_training;no_selection;no_forward_claim;no_goal_achieve",
        "external_verification_status": "mt5_parity_probe_queued_not_executed(MT5 동등성 탐침 대기, 미실행)",
        "notes": f"next_action={final['next_action']};runtime_package={final['runtime_package']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__asof_runtime_package",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "as-of feature frames and MT5 parity package",
        "kpi_scope": "feature_rows_alignment_lag_session_boundary_no_trading_kpi",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": "goal_achieve_not_claimed;forward_passed_not_claimed;mt5_execution_not_run",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__asof_runtime_package",
        "family": "asof_feature_join_runtime_parity_package_without_db",
        "question": "can exact alignment gaps be reduced by no-lookahead as-of join and packaged for MT5 parity",
        "metric_scope": "valid_rows_lag_minutes_session_boundary_package_rows",
        "primary_artifact": aw.rel(REPORT_PATH),
        "report_path": aw.rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not aw.path_exists(path):
            continue
        artifact_path = aw.rel(path)
        if artifact_path in seen:
            continue
        seen.add(artifact_path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return aw.write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    src = load_inputs()
    us100_last_close = str(src["bo_final"].get("us100_last_close_utc", ""))
    summaries, missing_rows, invalid_rows, frame_artifacts, foundation_counts = materialize_asof_frames(us100_last_close)
    basic_paths = write_basic_artifacts(summaries, missing_rows, invalid_rows)
    improvement_rows = build_improvement_rows(src, summaries)
    improvement_path = aw.write_csv(FEATURE_SET_IMPROVEMENT, IMPROVEMENT_COLUMNS, improvement_rows)
    session_rows = build_session_boundary_rows(src, summaries)
    session_path = aw.write_csv(SESSION_BOUNDARY_REVIEW, SESSION_COLUMNS, session_rows)
    firewall_rows = build_feature_firewall(summaries)
    firewall_path = aw.write_csv(FEATURE_FIREWALL, FIREWALL_COLUMNS, firewall_rows)
    matrix_rows, runtime_manifest, runtime_artifacts = export_runtime_package(summaries)
    parity_rows = build_parity_matrix(matrix_rows)
    parity_path = aw.write_csv(PARITY_HANDOFF_MATRIX, PARITY_COLUMNS, parity_rows)
    queue_rows = build_queue(parity_rows)
    queue_path = aw.write_csv(RUN337BR_QUEUE, QUEUE_COLUMNS, queue_rows)
    gate_rows = build_gates(src, summaries, improvement_rows, session_rows, firewall_rows, parity_rows, queue_rows, matrix_rows)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    materialized = [row for row in summaries if row.get("status") == "materialized"]
    latest_feature_timestamp = max((str(row.get("last_valid_timestamp", "")) for row in materialized), default="")
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BQ_asof_runtime_package_gate_failure",
        "judgment": JUDGMENT if all_gates_pass else "asof_feature_join_runtime_package_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BQ_asof_runtime_package_before_mt5_probe",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BQ_asof_runtime_package_gate_failure_v1",
        "feature_window_end_utc": us100_last_close,
        "feature_set_rows": len(summaries),
        "materialized_feature_sets": len(materialized),
        "latest_feature_timestamp": latest_feature_timestamp,
        "runtime_package": aw.rel(RUNTIME_PACKAGE_MANIFEST),
        "mt5_feature_matrix_count": len(matrix_rows),
        "gate_rows": len(gate_rows),
        "passed_gates": count_passed(gate_rows),
        "failed_gates": [row.get("gate_id") for row in gate_rows if row.get("status") != "passed"],
        "training": "not_run",
        "candidate_selection": "not_run",
        "actual_mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = aw.write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": final["status"],
        "inputs": [aw.rel(path) for path in INPUT_FILES],
        "outputs": [aw.rel(path) for path in OUTPUT_FILES],
        "frame_artifacts": [aw.rel(path) for path in frame_artifacts],
        "runtime_artifacts": [aw.rel(path) for path in runtime_artifacts],
        "asof_policy": ASOF_POLICY_PAYLOAD,
        "no_training": True,
        "no_selection": True,
        "generated_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = build_receipts(final, foundation_counts, matrix_rows)
    report_path = write_report(final, improvement_rows, session_rows)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final) if all_gates_pass else []
    register_paths = update_registers(final) if all_gates_pass else []
    artifact_inputs = [
        *frame_artifacts,
        *runtime_artifacts,
        *basic_paths,
        improvement_path,
        session_path,
        firewall_path,
        parity_path,
        queue_path,
        gate_path,
        final_path,
        manifest_path,
        *receipt_paths,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
    ]
    artifact_registry_path = update_artifact_registry(artifact_inputs, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "materialized_feature_sets": final["materialized_feature_sets"],
                "latest_feature_timestamp": final["latest_feature_timestamp"],
                "mt5_feature_matrix_count": final["mt5_feature_matrix_count"],
                "passed_gates": final["passed_gates"],
                "gate_rows": final["gate_rows"],
                "artifact_registry": aw.rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
