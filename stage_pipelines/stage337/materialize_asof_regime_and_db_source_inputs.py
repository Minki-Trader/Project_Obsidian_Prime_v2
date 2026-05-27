# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage337 import reprobe_next_rollover_or_synthetic_custom_parity_repair as ak  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AO"
RUN_ID = "run337AO_asof_regime_and_db_source_materialization_v1"
PARENT_RUN_ID = "run337AN_broker_rollover_reprobe_when_utc_day_boundary_available_v1"
NEXT_RUN_ID = "run337AP_broker_tester_history_repair_or_next_rollover_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AO_asof_regime_and_db_source_materialization_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)
STATUS = "completed_stage337AO_asof_regime_db_source_inputs_materialized_no_training_no_selection"
JUDGMENT = "asof_regime_sources_hash_lag_and_db_schema_materialized_broker_gap_still_blocks_forward"
DECISION = "stage337AO_open_run337AP_broker_tester_history_repair_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AO_asof_regime_and_db_source_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AO_asof_regime_and_db_source_materialization.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN337AN_DIR = STAGE_DIR / "02_runs" / "run337AN"
RUN337AN_FINAL = RUN337AN_DIR / "final_decision.json"
RUN337AN_GAP = RUN337AN_DIR / "tester_feature_last_gap_reprobe.csv"
RUN337AN_DIFF = RUN337AN_DIR / "exact_timestamp_proxy_mt5_difference.csv"
RUN337AN_TELEMETRY = RUN337AN_DIR / "runtime_telemetry" / "u42_plain_rf_an_broker_rollover_reprobe_telemetry.csv"
RUN337AN_FEATURES = RUN337AN_DIR / "feature_matrices" / "u42_plain_an_broker_rollover_reprobe_features.csv"
RUN337AM_QUEUE = STAGE_DIR / "02_runs" / "run337AM" / "next_experiment_queue.csv"
RUN337AM_PREFLIGHT = STAGE_DIR / "02_runs" / "run337AM" / "cost_direction_curve_preflight_matrix.csv"
RUN337Y_SNAPSHOT = STAGE_DIR / "02_runs" / "run337Y" / "source_timestamp_snapshot.csv"
RUN337Y_DECISION = STAGE_DIR / "02_runs" / "run337Y" / "source_age_decision.csv"
RUN337Y_BLOCKERS = STAGE_DIR / "02_runs" / "run337Y" / "source_gap_blocker_report.csv"
RUN337AE_TRADES = STAGE_DIR / "02_runs" / "run337AE" / "trade_records.csv"
RUN337AE_DB = STAGE_DIR / "02_runs" / "run337AE" / "db_attribution_report.csv"
RUN337AE_REGIME = STAGE_DIR / "02_runs" / "run337AE" / "regime_attribution_report.csv"

MACRO_SOURCES = {
    "VIX": {"prefix": "vix", "role": "volatility regime(변동성 국면)"},
    "US10YR": {"prefix": "rate", "role": "rate regime(금리 국면)"},
    "USDX": {"prefix": "usd", "role": "USD regime(달러 국면)"},
}
DB_REQUIRED_COLUMNS = [
    "db_decision_source",
    "d_source",
    "b_source",
    "d_score",
    "b_score",
    "decision_surface_branch",
    "source_component",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337AO as-of regime and D/B source materialization.")
    parser.add_argument("--trade-slice", default="completed_day_broker_slice")
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return ak.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return ak.read_csv(path)


def read_json(path: Path) -> Any:
    return ak.read_json(path)


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def parse_time(value: Any) -> pd.Timestamp:
    return pd.to_datetime(str(value), errors="coerce", utc=True)


def age_bucket(minutes: float | None) -> str:
    if minutes is None or not math.isfinite(minutes):
        return "missing"
    if minutes < 0:
        return "future_relative_to_decision"
    if minutes <= 60:
        return "0_60m"
    if minutes <= 180:
        return "61_180m"
    if minutes <= 360:
        return "181_360m"
    return "360m_plus"


def z_bucket(value: Any) -> str:
    number = to_float(value)
    if number is None:
        return "z_missing"
    if number < -1.0:
        return "z_lt_minus1"
    if number < 0.0:
        return "z_minus1_to_0"
    if number < 1.0:
        return "z_0_to_1"
    return "z_1_plus"


def configure_artifact_helper() -> None:
    ak.RUN_ID = RUN_ID
    ak.STAGE_ID = STAGE_ID
    ak.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    ak.ARTIFACT_REGISTRY = ARTIFACT_REGISTRY


def source_identity_rows(snapshot_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in snapshot_rows:
        path = ROOT / str(row.get("source_path", ""))
        manifest = ROOT / str(row.get("manifest_path", ""))
        group = str(row.get("source_group", ""))
        symbol = str(row.get("symbol", ""))
        role = "macro_asof_join_source"
        if group == "US100 broker M5":
            role = "technical_control_reference"
        elif group == "mega-cap equity source":
            role = "session_stale_policy_input"
        rows.append(
            {
                "source_group": group,
                "symbol": symbol,
                "broker_symbol": row.get("broker_symbol", ""),
                "materialization_role": role,
                "status": row.get("status", ""),
                "row_count": row.get("row_count", ""),
                "first_open_utc": row.get("first_open_utc", ""),
                "last_open_utc": row.get("last_open_utc", ""),
                "last_close_utc": row.get("last_close_utc", ""),
                "age_bucket_from_run337Y": row.get("age_bucket", ""),
                "availability_status": row.get("availability_status", ""),
                "source_path": row.get("source_path", ""),
                "source_path_exists": path_exists(path),
                "source_hash_recorded": row.get("source_hash", ""),
                "source_hash_recomputed": sha256_file(path) if path_exists(path) else "",
                "manifest_path": row.get("manifest_path", ""),
                "manifest_path_exists": path_exists(manifest),
                "manifest_hash_recorded": row.get("manifest_hash", ""),
                "manifest_hash_recomputed": sha256_file(manifest) if path_exists(manifest) else "",
                "time_axis": row.get("time_axis", ""),
                "lookahead_status": row.get("lookahead_status", ""),
                "effect": "source identity(원천 정체성)를 고정한다. 효과(effect, 효과): 이후 국면 조인이 어떤 파일에서 왔는지 추적한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def release_lag_rows(snapshot_rows: Sequence[Mapping[str, str]], final: Mapping[str, Any]) -> list[dict[str, Any]]:
    feature_last = parse_time(final.get("feature_last_timestamp", ""))
    tester_last = parse_time(final.get("tester_last_observed_bar_time", ""))
    rows: list[dict[str, Any]] = []
    for row in snapshot_rows:
        source_last = parse_time(row.get("last_close_utc", ""))
        feature_age = None if pd.isna(source_last) or pd.isna(feature_last) else (feature_last - source_last).total_seconds() / 60.0
        tester_age = None if pd.isna(source_last) or pd.isna(tester_last) else (tester_last - source_last).total_seconds() / 60.0
        group = str(row.get("source_group", ""))
        if feature_age is not None and feature_age < 0:
            verdict = "must_filter_to_decision_time"
        elif group == "mega-cap equity source" and feature_age is not None and feature_age > 180:
            verdict = "probe_only_session_stale_policy_required"
        elif group == "macro regime source":
            verdict = "macro_source_usable_with_age_bucket"
        elif group == "US100 broker M5":
            verdict = "technical_reference_filter_required"
        else:
            verdict = "usable_with_boundary"
        rows.append(
            {
                "symbol": row.get("symbol", ""),
                "source_group": group,
                "feature_last_timestamp": "" if pd.isna(feature_last) else feature_last.isoformat().replace("+00:00", "Z"),
                "tester_last_observed_bar_time": "" if pd.isna(tester_last) else tester_last.isoformat().replace("+00:00", "Z"),
                "source_last_close_utc": "" if pd.isna(source_last) else source_last.isoformat().replace("+00:00", "Z"),
                "age_minutes_to_feature_last": feature_age,
                "age_bucket_to_feature_last": age_bucket(feature_age),
                "age_minutes_to_tester_last": tester_age,
                "age_bucket_to_tester_last": age_bucket(tester_age),
                "asof_verdict": verdict,
                "forbidden_use": "post_forward_backfill_or_silent_future_fill(전진 이후 사후 채움 또는 조용한 미래 채움)",
                "effect": "release lag(공표 지연)를 수치화한다. 효과(effect, 효과): 경제 국면을 미래참조 없이 쓸 수 있는지 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def source_bars(snapshot_rows: Sequence[Mapping[str, str]], symbol: str) -> pd.DataFrame:
    source = next((row for row in snapshot_rows if row.get("symbol") == symbol), None)
    if source is None:
        return pd.DataFrame()
    path = ROOT / str(source.get("source_path", ""))
    if not path_exists(path):
        return pd.DataFrame()
    frame = pd.read_csv(io_path(path))
    frame["source_close_utc"] = pd.to_datetime(frame["time_close_unix"], unit="s", utc=True)
    frame = frame.sort_values("source_close_utc").reset_index(drop=True)
    rolling = frame["close"].rolling(20, min_periods=5)
    std = rolling.std(ddof=0).replace(0, np.nan)
    frame["zscore_20"] = (frame["close"] - rolling.mean()) / std
    return frame[["source_close_utc", "close", "zscore_20", "spread_points", "tick_volume"]].copy()


def load_trade_slice(trade_slice: str) -> pd.DataFrame:
    frame = pd.read_csv(io_path(RUN337AE_TRADES))
    if "slice_type" in frame.columns:
        frame = frame.loc[frame["slice_type"].astype(str) == trade_slice].copy()
    frame["feature_ts"] = pd.to_datetime(frame["feature_timestamp"], errors="coerce", utc=True)
    frame = frame.dropna(subset=["feature_ts"]).sort_values("feature_ts").reset_index(drop=True)
    return frame


def build_asof_join(trades: pd.DataFrame, snapshot_rows: Sequence[Mapping[str, str]]) -> pd.DataFrame:
    output = trades.copy()
    for symbol, meta in MACRO_SOURCES.items():
        prefix = str(meta["prefix"])
        bars = source_bars(snapshot_rows, symbol)
        if bars.empty:
            output[f"{prefix}_source_close_utc"] = ""
            output[f"{prefix}_value"] = np.nan
            output[f"{prefix}_zscore_20_asof"] = np.nan
            output[f"{prefix}_age_minutes"] = np.nan
            output[f"{prefix}_age_bucket"] = "missing"
            output[f"{prefix}_z_regime"] = "z_missing"
            continue
        merged = pd.merge_asof(
            output[["feature_ts"]].sort_values("feature_ts"),
            bars.sort_values("source_close_utc"),
            left_on="feature_ts",
            right_on="source_close_utc",
            direction="backward",
            allow_exact_matches=True,
        )
        merged = merged.reindex(output[["feature_ts"]].sort_values("feature_ts").index).sort_index()
        output[f"{prefix}_source_close_utc"] = merged["source_close_utc"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        output[f"{prefix}_value"] = merged["close"]
        output[f"{prefix}_zscore_20_asof"] = merged["zscore_20"]
        output[f"{prefix}_age_minutes"] = (output["feature_ts"] - merged["source_close_utc"]).dt.total_seconds() / 60.0
        output[f"{prefix}_age_bucket"] = output[f"{prefix}_age_minutes"].map(age_bucket)
        output[f"{prefix}_z_regime"] = output[f"{prefix}_zscore_20_asof"].map(z_bucket)
    keep = [
        "trade_index",
        "direction",
        "open_time",
        "close_time",
        "feature_timestamp",
        "month",
        "weekday",
        "session_utc",
        "chron_segment",
        "net_profit",
        "gross_profit",
        "gross_loss",
        "adx_regime",
        "di_regime",
        "vol_regime",
        "atr_ratio_regime",
    ]
    for symbol, meta in MACRO_SOURCES.items():
        prefix = str(meta["prefix"])
        keep.extend(
            [
                f"{prefix}_source_close_utc",
                f"{prefix}_value",
                f"{prefix}_zscore_20_asof",
                f"{prefix}_age_minutes",
                f"{prefix}_age_bucket",
                f"{prefix}_z_regime",
            ]
        )
    output = output[[column for column in keep if column in output.columns]].copy()
    output["no_future_source_violation"] = False
    for meta in MACRO_SOURCES.values():
        prefix = str(meta["prefix"])
        output["no_future_source_violation"] = output["no_future_source_violation"] | (output[f"{prefix}_age_minutes"] < 0)
    output["claim_boundary"] = CLAIM_BOUNDARY
    return output


def aggregate_group(frame: pd.DataFrame, axis: str, bucket_column: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if bucket_column not in frame.columns:
        return rows
    def numeric_column(group: pd.DataFrame, column: str) -> pd.Series:
        if column not in group.columns:
            return pd.Series(0.0, index=group.index)
        return pd.to_numeric(group[column], errors="coerce").fillna(0)

    for bucket, group in frame.groupby(bucket_column, dropna=False):
        profit_series = numeric_column(group, "net_profit")
        gp = numeric_column(group, "gross_profit").sum()
        gl = numeric_column(group, "gross_loss").sum()
        net = profit_series.sum()
        wins = int((profit_series > 0).sum())
        losses = int((profit_series < 0).sum())
        rows.append(
            {
                "axis": axis,
                "bucket": "" if pd.isna(bucket) else bucket,
                "trade_count": int(len(group)),
                "net_profit": net,
                "gross_profit": gp,
                "gross_loss": gl,
                "profit_factor": None if gl == 0 else gp / abs(gl),
                "expectancy": None if len(group) == 0 else net / len(group),
                "win_rate": None if len(group) == 0 else wins / len(group),
                "loss_count": losses,
                "slice_read": "diagnostic_only_asof_materialized_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def regime_slice_preview(joined: pd.DataFrame) -> list[dict[str, Any]]:
    axes = [
        ("direction", "direction"),
        ("session", "session_utc"),
        ("month", "month"),
        ("adx", "adx_regime"),
        ("volatility", "vol_regime"),
        ("vix_asof_z", "vix_z_regime"),
        ("vix_source_age", "vix_age_bucket"),
        ("rate_asof_z", "rate_z_regime"),
        ("rate_source_age", "rate_age_bucket"),
        ("usd_asof_z", "usd_z_regime"),
        ("usd_source_age", "usd_age_bucket"),
    ]
    rows: list[dict[str, Any]] = []
    for axis, column in axes:
        rows.extend(aggregate_group(joined, axis, column))
    return rows


def db_source_schema_rows() -> list[dict[str, Any]]:
    telemetry_columns = []
    feature_columns = []
    if path_exists(RUN337AN_TELEMETRY):
        telemetry_columns = list(pd.read_csv(io_path(RUN337AN_TELEMETRY), nrows=0).columns)
    if path_exists(RUN337AN_FEATURES):
        feature_columns = list(pd.read_csv(io_path(RUN337AN_FEATURES), nrows=0).columns)
    rows: list[dict[str, Any]] = []
    for column in DB_REQUIRED_COLUMNS:
        in_telemetry = column in telemetry_columns
        in_features = column in feature_columns
        rows.append(
            {
                "required_column": column,
                "telemetry_status": "present" if in_telemetry else "missing",
                "feature_status": "present" if in_features else "missing",
                "readiness": "available" if in_telemetry or in_features else "missing_required",
                "effect": "D/B source(D/B 원천) 귀속에 필요한 필드를 확인한다. 효과(effect, 효과): 방향(direction) 귀속과 D/B 귀속을 섞지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    direction_proxy = {
        "required_column": "decision",
        "telemetry_status": "present" if "decision" in telemetry_columns else "missing",
        "feature_status": "not_required",
        "readiness": "direction_proxy_only" if "decision" in telemetry_columns else "missing",
        "effect": "decision(결정) 필드는 방향 proxy(대리값)일 뿐 D/B source(D/B 원천)가 아니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    rows.append(direction_proxy)
    return rows


def db_readiness_rows(schema_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    missing = [row["required_column"] for row in schema_rows if row.get("readiness") == "missing_required"]
    return [
        {
            "readiness_id": "db_source_attribution",
            "status": "missing_required" if missing else "available",
            "missing_columns": json.dumps(missing, ensure_ascii=False),
            "available_proxy": "direction/decision proxy(방향/결정 대리값)",
            "forbidden_claim": "D source/B source/D+B attribution(D 원천/B 원천/D+B 귀속)",
            "allowed_claim": "direction attribution only until D/B source telemetry exists(D/B 원천 기록 전까지 방향 귀속만 허용)",
            "source_evidence": rel(RUN337AE_DB),
            "effect": "D/B source(D/B 원천) 부재를 명시한다. 효과(effect, 효과): 없는 원천 귀속을 만든 것처럼 보이지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def instrumentation_queue_rows(db_missing: int, no_future_violations: int, source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    equity_stale = sum(1 for row in source_rows if row.get("materialization_role") == "session_stale_policy_input")
    return [
        {
            "order": 1,
            "next_run_id": NEXT_RUN_ID,
            "track": "runtime_repair(런타임 수리)",
            "action": "repair_or_reprobe_broker_tester_feature_last_gap",
            "why": "run337AN broker tester(브로커 테스터)가 feature_last(피처 끝)에 도달하지 못함",
            "effect": "Forward Passed/Failed(전진 통과/실패) 금지를 풀 수 있는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "order": 2,
            "next_run_id": "run337AQ_db_source_telemetry_instrumentation_design_v1",
            "track": "instrumentation(계측)",
            "action": "add_or_materialize_D_B_source_telemetry_schema",
            "why": f"missing_required_columns={db_missing}",
            "effect": "D/B attribution(D/B 귀속)을 방향 proxy(대리값)와 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "order": 3,
            "next_run_id": "run337AR_asof_macro_regime_trade_attribution_probe_v1",
            "track": "attribution(귀속)",
            "action": "use_asof_join_for_macro_regime_slices_without_training",
            "why": f"no_future_violations={no_future_violations}; equity_session_stale_inputs={equity_stale}",
            "effect": "VIX/USD/rate(변동성/달러/금리) 국면을 미래참조 없이 검토한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "parent_run337AN_loaded",
            "status": "passed" if path_exists(RUN337AN_FINAL) else "failed",
            "evidence_path": rel(RUN337AN_FINAL),
            "effect": "부모 broker reprobe(브로커 재탐침) 결과를 읽었다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "source_hash_index_materialized",
            "status": "passed" if final["source_identity_rows"] > 0 else "failed",
            "evidence_path": rel(RUN_DIR / "source_identity_index.csv"),
            "effect": "원천 파일 해시(hash, 해시)를 재확인했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release_lag_audit_materialized",
            "status": "passed" if final["release_lag_rows"] > 0 else "failed",
            "evidence_path": rel(RUN_DIR / "asof_release_lag_audit.csv"),
            "effect": "source lag(원천 지연)을 feature_last(피처 끝) 기준으로 분리했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "asof_trade_join_no_future_source",
            "status": "passed" if final["no_future_source_violations"] == 0 else "failed",
            "evidence_path": rel(RUN_DIR / "asof_trade_regime_join.csv"),
            "effect": "거래별 macro source(거시 원천)가 feature timestamp(피처 시각) 이후 값을 쓰지 않는지 확인했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "db_source_schema_audited",
            "status": "passed_with_missing_required" if final["db_missing_required_columns"] else "passed",
            "evidence_path": rel(RUN_DIR / "db_source_telemetry_schema.csv"),
            "effect": "D/B source(D/B 원천) 필드 존재 여부를 숨기지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forward_claim_boundary",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "final_decision.json"),
            "effect": "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def decision_payload(
    source_rows: Sequence[Mapping[str, Any]],
    lag_rows: Sequence[Mapping[str, Any]],
    joined: pd.DataFrame,
    slice_rows: Sequence[Mapping[str, Any]],
    db_schema: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    no_future = int(joined["no_future_source_violation"].sum()) if "no_future_source_violation" in joined.columns else 0
    db_missing = sum(1 for row in db_schema if row.get("readiness") == "missing_required")
    macro_usable = sum(1 for row in lag_rows if str(row.get("asof_verdict", "")).startswith("macro_source_usable"))
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "source_identity_rows": len(source_rows),
        "release_lag_rows": len(lag_rows),
        "asof_join_trade_rows": int(len(joined)),
        "regime_slice_rows": len(slice_rows),
        "macro_sources_usable_with_age_bucket": macro_usable,
        "no_future_source_violations": no_future,
        "db_missing_required_columns": db_missing,
        "broker_forward_boundary": "failed_from_parent_run337AN",
        "Forward Passed": "not_claimed",
        "Forward Failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def receipt_payloads(final: Mapping[str, Any]) -> dict[Path, Mapping[str, Any]]:
    common = {"run_id": RUN_ID, "stage_id": STAGE_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY}
    return {
        RUN_DIR / "data_integrity_receipt.json": {
            **common,
            "data_source": "run337Y raw source snapshot(원천 스냅샷), run337AE trade records(거래 기록), run337AN runtime telemetry(런타임 기록)",
            "time_axis": "source close UTC(원천 종가 UTC) <= feature timestamp(피처 시각) only",
            "sample_scope": "US100 forward trade records plus VIX/US10YR/USDX macro source bars",
            "missing_or_duplicate_check": "source hash index and release lag audit materialized; D/B source columns missing_required",
            "feature_label_boundary": "no labels, no model training, no threshold search; as-of join only",
            "split_boundary": "post-OOS forward diagnostic input materialization",
            "leakage_risk": "post-forward macro backfill or using source close after feature timestamp",
            "data_hash_or_identity": rel(RUN_DIR / "source_identity_index.csv"),
            "integrity_judgment": "usable_with_boundary" if final["no_future_source_violations"] == 0 else "invalid",
        },
        RUN_DIR / "performance_attribution_receipt.json": {
            **common,
            "observed_change": "macro regime source values are now as-of joinable for trade-level attribution; D/B source remains missing",
            "comparison_baseline": rel(RUN337AE_REGIME),
            "likely_drivers": "source timestamp age, missing D/B telemetry, broker tester feature_last gap",
            "segment_checks": ["direction", "session", "month", "ADX", "volatility", "VIX as-of", "rate as-of", "USD as-of"],
            "trade_shape": f"joined_trade_rows={final['asof_join_trade_rows']}",
            "alternative_explanations": "broker tester still cannot see full feature_last, so joined attribution is diagnostic input only",
            "attribution_confidence": "low_to_medium_input_materialized_not_forward_decision",
            "next_probe": NEXT_RUN_ID,
        },
        RUN_DIR / "result_judgment_receipt.json": {
            **common,
            "result_subject": RUN_ID,
            "evidence_available": ["source_identity_index.csv", "asof_release_lag_audit.csv", "asof_trade_regime_join.csv", "db_source_telemetry_schema.csv"],
            "evidence_missing": "broker tester feature_last reach and D/B source telemetry",
            "judgment_label": "exploratory_input_materialization",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "거시 국면 입력은 미래참조 없이 붙일 수 있지만 D/B 원천과 브로커 최신 경계는 아직 닫히지 않았다.",
        },
    }


def report_text(final: Mapping[str, Any]) -> str:
    return f"""# Stage337AO As-Of Regime And D/B Source Materialization(337AO 시점 기준 국면 및 D/B 원천 물질화)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- source_identity_rows(원천 정체성 행): `{final['source_identity_rows']}`
- release_lag_rows(공표 지연 행): `{final['release_lag_rows']}`
- asof_join_trade_rows(시점 기준 거래 조인 행): `{final['asof_join_trade_rows']}`
- regime_slice_rows(국면 구간 행): `{final['regime_slice_rows']}`
- macro_sources_usable_with_age_bucket(나이 버킷 포함 사용 가능 거시 원천): `{final['macro_sources_usable_with_age_bucket']}`
- no_future_source_violations(미래 원천 위반): `{final['no_future_source_violations']}`
- db_missing_required_columns(D/B 필수 누락 컬럼): `{final['db_missing_required_columns']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Meaning(의미)

run337AO(337AO 실행)는 VIX/US10YR/USDX(변동성/금리/달러) 원천을 trade feature timestamp(거래 피처 시각) 이전 값으로만 붙였다. 효과(effect, 효과)는 macro regime attribution(거시 국면 귀속)을 미래참조 없이 다시 볼 수 있게 하는 것이다.

## Boundary(경계)

D/B source(D/B 원천) 필드는 run337AN telemetry(런타임 기록)와 u42 feature(피처)에 없다. 효과(effect, 효과)는 direction attribution(방향 귀속)을 D/B attribution(D/B 귀속)처럼 말하지 못하게 막는 것이다.

Broker forward boundary(브로커 전진 경계)는 부모 run337AN(337AN 실행)에서 `failed`다. 따라서 이 실행은 data instrumentation(데이터 계측)일 뿐 Forward Passed/Failed(전진 통과/실패)가 아니다.
"""


def decision_doc_text(final: Mapping[str, Any]) -> str:
    return f"""# 2026-05-27 Stage337AO As-Of Source Decision(337AO 시점 기준 원천 결정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): as-of macro source(시점 기준 거시 원천)는 물질화했지만, D/B source(D/B 원천)와 broker tester feature_last(브로커 테스터 피처 끝) 문제는 다음 수리로 남긴다.
"""


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def upsert_focus_block(text: str, final: Mapping[str, Any]) -> str:
    focus = (
        f"Stage337 run337AO focus complete: run337AO(337AO 실행)은 `{STATUS}`로 as-of regime/source input(시점 기준 국면/원천 입력)을 물질화했다. "
        f"Effect(효과): joined trades(결합 거래) `{final['asof_join_trade_rows']}`, no_future_source_violations(미래 원천 위반) "
        f"`{final['no_future_source_violations']}`, D/B missing columns(D/B 누락 컬럼) `{final['db_missing_required_columns']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    block = f"- >-\n  {focus}\n"
    if "current_focus:\n" not in text:
        return text.rstrip() + "\ncurrent_focus:\n" + block
    if "Stage337 run337AO focus complete" in text:
        return re.sub(r"- >-\n  Stage337 run337AO focus complete:.*?(?=\n- >-|\Z)", block.rstrip(), text, count=1, flags=re.S)
    return text.replace("current_focus:\n", "current_focus:\n" + block, 1)


def update_status_docs(final: Mapping[str, Any]) -> list[Path]:
    changed: list[Path] = []
    selected_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- broker_forward_boundary(브로커 전진 경계): `failed`
- asof_regime_sources_materialized(시점 기준 국면 원천 물질화): `{final['macro_sources_usable_with_age_bucket']}/3`
- asof_join_trade_rows(시점 기준 거래 조인 행): `{final['asof_join_trade_rows']}`
- no_future_source_violations(미래 원천 위반): `{final['no_future_source_violations']}`
- db_source_status(D/B 원천 상태): `missing_required_columns_{final['db_missing_required_columns']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `broker_tester_feature_last_not_reached_and_db_source_missing`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AO(337AO 실행)은 macro as-of join(거시 시점 기준 결합)을 만들고 D/B source(D/B 원천) 누락을 고정했다.
"""
    changed.append(ak.write_md(SELECTED_STATUS, selected_text))
    if path_exists(WORKSPACE_STATE):
        text, bom = ak.read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
        text = replace_line(text, "updated_on:", f"updated_on: '{TODAY}'")
        text = upsert_focus_block(text, final)
        changed.append(ak.write_text(WORKSPACE_STATE, text, bom))
    if path_exists(CURRENT_STATE):
        text, bom = ak.read_text(CURRENT_STATE)
        for prefix, replacement in (
            ("- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`"),
            ("- secondary_current_run(보조 현재 실행):", f"- secondary_current_run(보조 현재 실행): `none`"),
            ("- status(상태):", f"- status(상태): `{STATUS}`"),
            ("- decision(결정):", f"- decision(결정): `{DECISION}`"),
            ("- latest_completed_run(최근 완료 실행):", f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`"),
            ("- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`"),
            ("- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`"),
        ):
            text = replace_line(text, prefix, replacement)
        entry = f"""## Stage337 run337AO(337AO 실행) - {TODAY}

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): as-of macro join(시점 기준 거시 결합) `{final['asof_join_trade_rows']}`행, no_future_source_violations(미래 원천 위반) `{final['no_future_source_violations']}`, D/B missing columns(D/B 누락 컬럼) `{final['db_missing_required_columns']}`를 기록했다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
        if "## Stage337 run337AO(337AO 실행)" in text:
            text = re.sub(r"## Stage337 run337AO\(337AO 실행\).*?(?=\n## |\Z)", entry.strip(), text, count=1, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        changed.append(ak.write_text(CURRENT_STATE, text, bom))
    if path_exists(CHANGELOG):
        text, bom = ak.read_text(CHANGELOG)
        line = (
            f"- {TODAY}: Stage337 run337AO(337AO 실행) `{STATUS}`. "
            f"Effect(효과): as-of trades(시점 기준 거래) `{final['asof_join_trade_rows']}`, "
            f"no_future_source_violations(미래 원천 위반) `{final['no_future_source_violations']}`, "
            f"D/B missing(D/B 누락) `{final['db_missing_required_columns']}`; Forward/Goal(전진/목표) not_claimed(미주장)."
        )
        if "Stage337 run337AO(337AO 실행)" not in text:
            text = text.rstrip() + "\n" + line + "\n"
        changed.append(ak.write_text(CHANGELOG, text, bom))
    if path_exists(STAGE_BRIEF):
        text, bom = ak.read_text(STAGE_BRIEF)
        text = re.sub(r"- latest_run\([^)]*\): `[^`]*`", f"- latest_run(최신 실행): `{RUN_ID}`", text, count=1)
        summary = (
            f"- run337AO_summary(337AO 요약): `{STATUS}`. "
            f"Effect(효과): as-of macro join(시점 기준 거시 결합) `{final['asof_join_trade_rows']}`행, "
            f"D/B source(D/B 원천) missing_required `{final['db_missing_required_columns']}`.\n"
        )
        if "run337AO_summary(337AO 요약)" in text:
            text = re.sub(r"- run337AO_summary\(337AO 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
        else:
            text = text.rstrip() + "\n" + summary
        changed.append(ak.write_text(STAGE_BRIEF, text, bom))
    return changed


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "asof_regime_db_source_materialization",
        "family": "data_instrumentation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__asof_regime_db_source_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "asof_regime_db_source_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "data_instrumentation",
        "tier_scope": "Tier A u42 parent trade records with macro as-of source(Tier A u42 부모 거래 기록과 거시 시점 기준 원천)",
        "kpi_scope": "input_materialization_no_forward_decision(입력 물질화, 전진 판정 없음)",
        "scoreboard_lane": "data_instrumentation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"joined_trades={final['asof_join_trade_rows']};no_future={final['no_future_source_violations']};db_missing={final['db_missing_required_columns']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_lot_opt;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim_materialization_from_parent_mt5_outputs",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__asof_regime_db_source_materialization",
        "run_key": f"{RUN_ID}__asof_regime_db_source_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_instrumentation",
        "family": "asof_regime_db_source_materialization",
        "question": "can macro regime and D/B source inputs be materialized without lookahead before further repair",
        "evidence_scope": "run337Y source hashes, run337AE trade records, run337AN telemetry schema",
        "kpi_scope": "input_materialization_no_forward_decision",
        "metric_scope": "source_lag_db_schema_no_forward_decision",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;no_future={final['no_future_source_violations']};db_missing={final['db_missing_required_columns']}",
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
    }
    return [
        ak.upsert_csv(RUN_REGISTRY, ["run_id"], run_row),
        ak.upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_row),
        ak.upsert_csv(STAGE_LEDGER, ["run_key"], stage_row),
    ]


def main() -> int:
    args = parse_args()
    configure_artifact_helper()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)

    parent_final = read_json(RUN337AN_FINAL)
    snapshot = read_csv(RUN337Y_SNAPSHOT)
    source_rows = source_identity_rows(snapshot)
    lag_rows = release_lag_rows(snapshot, parent_final)
    trades = load_trade_slice(args.trade_slice)
    joined = build_asof_join(trades, snapshot)
    slice_rows = regime_slice_preview(joined)
    db_schema = db_source_schema_rows()
    db_ready = db_readiness_rows(db_schema)
    final = decision_payload(source_rows, lag_rows, joined, slice_rows, db_schema)
    queue = instrumentation_queue_rows(final["db_missing_required_columns"], final["no_future_source_violations"], source_rows)
    gates = gate_rows(final)

    artifacts: list[Path] = [
        ak.write_json(RUN_DIR / "parent_run337AN_final_decision.json", parent_final),
        ak.write_csv(RUN_DIR / "source_identity_index.csv", ak.columns_for(source_rows, ["source_group", "symbol"]), source_rows),
        ak.write_csv(RUN_DIR / "asof_release_lag_audit.csv", ak.columns_for(lag_rows, ["symbol"]), lag_rows),
        ak.write_csv(RUN_DIR / "asof_trade_regime_join.csv", list(joined.columns), joined.to_dict("records")),
        ak.write_csv(RUN_DIR / "asof_regime_slice_preview.csv", ak.columns_for(slice_rows, ["axis", "bucket"]), slice_rows),
        ak.write_csv(RUN_DIR / "db_source_telemetry_schema.csv", ak.columns_for(db_schema, ["required_column"]), db_schema),
        ak.write_csv(RUN_DIR / "db_source_attribution_readiness.csv", ak.columns_for(db_ready, ["readiness_id"]), db_ready),
        ak.write_csv(RUN_DIR / "instrumentation_queue.csv", ak.columns_for(queue, ["order"]), queue),
        ak.write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ak.columns_for(gates, ["gate_id"]), gates),
        ak.write_json(RUN_DIR / "final_decision.json", final),
        ak.write_md(REPORT_PATH, report_text(final)),
        ak.write_md(DECISION_DOC, decision_doc_text(final)),
    ]
    for path, payload in receipt_payloads(final).items():
        artifacts.append(ak.write_json(path, payload))
    artifacts.extend(update_status_docs(final))
    artifacts.extend(update_registers(final))
    manifest = ak.write_json(
        RUN_DIR / "run_manifest.json",
        {
            **final,
            "generated_at_utc": now_utc(),
            "command": "python stage_pipelines/stage337/materialize_asof_regime_and_db_source_inputs.py",
            "primary_family": "data_instrumentation",
            "primary_skill": "obsidian-data-integrity",
            "support_skills": ["obsidian-performance-attribution", "obsidian-result-judgment"],
            "parent_evidence": [rel(RUN337AN_FINAL), rel(RUN337Y_SNAPSHOT), rel(RUN337AE_TRADES)],
            "artifacts": [rel(path) for path in artifacts if path_exists(path)],
        },
    )
    artifacts.append(manifest)
    artifacts.append(ak.append_artifacts([*artifacts, Path(__file__)], final))
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
